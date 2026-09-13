"""LLM access — Google Gemini (primary), Groq, or OpenRouter fallback.

NO paid OpenAI is used anywhere. The active provider is auto-detected from the
API key that is present, with this precedence:

    1. Google Gemini   — GEMINI_API_KEY / GOOGLE_API_KEY  (free, aistudio.google.com)
    2. Groq            — GROQ_API_KEY                     (free, console.groq.com)
    3. OpenRouter      — OPENROUTER_API_KEY               (free multilingual models)
    4. Mock            — no key: offline templated output so the demo still runs.

All real providers are called over plain REST with `requests`, so there is no
dependency on any vendor SDK.
"""

from __future__ import annotations

import os
import re
import time
from dataclasses import dataclass

import requests

from .config import default_model_for

GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


class LLMError(RuntimeError):
    pass


@dataclass
class LLMResult:
    text: str
    model: str
    provider: str
    is_mock: bool = False
    usage: dict | None = None


# --------------------------------------------------------------------------- #
# Provider detection
# --------------------------------------------------------------------------- #
def gemini_key() -> str | None:
    key = (os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY") or "").strip()
    return key or None


def groq_key() -> str | None:
    return (os.getenv("GROQ_API_KEY") or "").strip() or None


def openrouter_key() -> str | None:
    return (os.getenv("OPENROUTER_API_KEY") or "").strip() or None


def provider() -> str:
    if gemini_key():
        return "gemini"
    if groq_key():
        return "groq"
    if openrouter_key():
        return "openrouter"
    return "mock"


def is_configured() -> bool:
    return provider() != "mock"


# --------------------------------------------------------------------------- #
# Public entry point
# --------------------------------------------------------------------------- #
def generate(
    messages: list[dict],
    model: str | None = None,
    temperature: float = 0.9,
    max_tokens: int = 1400,
    timeout: int = 90,
) -> LLMResult:
    """Generate a completion using the auto-detected provider."""
    prov = provider()
    model = model or os.getenv("LLM_MODEL") or default_model_for(prov)

    if prov == "gemini":
        return _gemini_generate(messages, model, temperature, max_tokens, timeout)
    if prov == "groq":
        return _groq_generate(messages, model, temperature, max_tokens, timeout)
    if prov == "openrouter":
        return _openrouter_generate(messages, model, temperature, max_tokens, timeout)
    return _mock_generate(messages, model)


# --------------------------------------------------------------------------- #
# Google Gemini
# --------------------------------------------------------------------------- #
def _gemini_generate(messages, model, temperature, max_tokens, timeout) -> LLMResult:
    # Gemini wants system text separately and roles of "user"/"model".
    system_parts = [m["content"] for m in messages if m["role"] == "system"]
    contents = []
    for m in messages:
        if m["role"] == "system":
            continue
        role = "model" if m["role"] == "assistant" else "user"
        contents.append({"role": role, "parts": [{"text": m["content"]}]})

    body: dict = {
        "contents": contents,
        "generationConfig": {
            "temperature": temperature,
            "maxOutputTokens": max_tokens,
        },
    }
    if system_parts:
        body["systemInstruction"] = {"parts": [{"text": "\n".join(system_parts)}]}

    url = GEMINI_URL.format(model=model)
    try:
        resp = requests.post(
            url, params={"key": gemini_key()}, json=body, timeout=timeout
        )
    except requests.RequestException as exc:
        raise LLMError(f"Network error contacting Gemini: {exc}") from exc

    if resp.status_code != 200:
        raise LLMError(f"Gemini returned {resp.status_code}: {resp.text[:500]}")

    data = resp.json()
    candidates = data.get("candidates") or []
    if not candidates:
        fb = data.get("promptFeedback", {})
        raise LLMError(f"Gemini returned no candidates (blocked?): {fb or data}")

    parts = candidates[0].get("content", {}).get("parts", [])
    text = "".join(p.get("text", "") for p in parts).strip()
    if not text:
        reason = candidates[0].get("finishReason", "unknown")
        raise LLMError(f"Gemini returned empty text (finishReason={reason}).")

    return LLMResult(
        text=text, model=model, provider="gemini",
        usage=data.get("usageMetadata"),
    )


# --------------------------------------------------------------------------- #
# Groq
# --------------------------------------------------------------------------- #
def _groq_generate(messages, model, temperature, max_tokens, timeout) -> LLMResult:
    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    headers = {
        "Authorization": f"Bearer {groq_key()}",
        "Content-Type": "application/json",
    }

    # Retry up to 3 times on rate-limit (429)
    for attempt in range(3):
        try:
            resp = requests.post(
                GROQ_URL, headers=headers, json=payload, timeout=timeout
            )
        except requests.RequestException as exc:
            raise LLMError(f"Network error contacting Groq: {exc}") from exc

        if resp.status_code == 429:
            # Rate limited — wait and retry
            wait = 20 * (attempt + 1)  # 20s, 40s, 60s
            time.sleep(wait)
            continue

        if resp.status_code != 200:
            raise LLMError(f"Groq returned {resp.status_code}: {resp.text[:500]}")
        break
    else:
        raise LLMError("Groq rate limit exceeded after 3 retries. Wait a minute and try again.")

    data = resp.json()
    try:
        text = data["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError) as exc:
        raise LLMError(f"Unexpected Groq response shape: {data}") from exc

    # Strip qwen3's <think>...</think> reasoning blocks
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()

    return LLMResult(
        text=text, model=model, provider="groq", usage=data.get("usage")
    )


# --------------------------------------------------------------------------- #
# OpenRouter (fallback)
# --------------------------------------------------------------------------- #
def _openrouter_headers() -> dict:
    h = {
        "Authorization": f"Bearer {openrouter_key()}",
        "Content-Type": "application/json",
    }
    site = os.getenv("OPENROUTER_SITE_URL", "").strip()
    title = os.getenv("OPENROUTER_APP_TITLE", "").strip()
    if site:
        h["HTTP-Referer"] = site
    if title:
        h["X-Title"] = title
    return h


def _openrouter_generate(messages, model, temperature, max_tokens, timeout) -> LLMResult:
    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    try:
        resp = requests.post(
            OPENROUTER_URL, headers=_openrouter_headers(), json=payload, timeout=timeout
        )
    except requests.RequestException as exc:
        raise LLMError(f"Network error contacting OpenRouter: {exc}") from exc

    if resp.status_code != 200:
        raise LLMError(f"OpenRouter returned {resp.status_code}: {resp.text[:500]}")

    data = resp.json()
    try:
        text = data["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError) as exc:
        raise LLMError(f"Unexpected OpenRouter response shape: {data}") from exc

    return LLMResult(
        text=text, model=model, provider="openrouter", usage=data.get("usage")
    )


# --------------------------------------------------------------------------- #
# Offline mock — keeps the demo alive without any key.
# --------------------------------------------------------------------------- #
def _mock_generate(messages, model) -> LLMResult:
    user = next((m["content"] for m in messages if m["role"] == "user"), "")

    def _field(label: str) -> str:
        for line in user.splitlines():
            if line.strip().upper().startswith(label.upper()):
                return line.split(":", 1)[-1].strip()
        return ""

    theme = _field("THEME") or "love"
    emotion = _field("EMOTION") or "hopeful"

    body = (
        "TITLE: [MOCK] {t}\n\n"
        "[Verse 1]\n"
        "(offline mock — add GEMINI_API_KEY in .env for real lyrics)\n"
        "A song about {t}, sung with a {e} heart\n"
        "Words placed here only to show the app's every part\n\n"
        "[Chorus]\n"
        "This is a preview, the engine runs true\n"
        "Plug in your key and it sings just for you\n"
    ).format(t=theme, e=emotion)

    return LLMResult(text=body, model=f"{model} (MOCK)", provider="mock", is_mock=True)
