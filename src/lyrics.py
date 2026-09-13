"""Generation orchestration.

Pipeline per language:
    retrieve real examples  →  build culturally-grounded prompt  →  call LLM
        →  parse (title / sections / English gloss)  →  analyse prosody.

Also provides `generate_comparison()` which runs the same theme across all three
languages for the side-by-side demo deliverable.
"""

from __future__ import annotations

import re
import time
from dataclasses import dataclass, field

from . import llm
from .analysis import StanzaAnalysis, analyze_stanza, split_stanzas
from .config import LANGUAGES, METRES, RHYME_SCHEMES, GenSpec
from .prompts import build_messages
from .retrieval import Snippet, retrieve_examples


@dataclass
class LyricResult:
    spec: GenSpec
    title: str
    lyrics: str                      # lyrics only (gloss stripped out)
    gloss: str                       # English gloss (Indic langs), may be ""
    raw: str                         # full raw model output
    model: str
    is_mock: bool
    examples: list[Snippet] = field(default_factory=list)
    stanza_analyses: list[StanzaAnalysis] = field(default_factory=list)
    error: str | None = None

    @property
    def language_name(self) -> str:
        return LANGUAGES[self.spec.language].name

    @property
    def avg_rhyme_match(self) -> float:
        vals = [s.rhyme_match_pct for s in self.stanza_analyses]
        return round(sum(vals) / len(vals), 1) if vals else 0.0

    @property
    def avg_metre_match(self) -> float:
        vals = [s.metre_match_pct for s in self.stanza_analyses]
        return round(sum(vals) / len(vals), 1) if vals else 0.0


# --------------------------------------------------------------------------- #
# Output parsing
# --------------------------------------------------------------------------- #
_TITLE_RE = re.compile(r"^\s*TITLE\s*[:\-]\s*(.+)$", re.IGNORECASE | re.MULTILINE)
_GLOSS_RE = re.compile(
    r"\[\s*english\s+gloss\s*\]\s*", re.IGNORECASE
)


def _parse_output(raw: str) -> tuple[str, str, str]:
    """Return (title, lyrics_without_gloss, gloss)."""
    # 1. Strip <think>...</think> blocks (qwen3 reasoning)
    raw = re.sub(r"<think>.*?</think>", "", raw, flags=re.DOTALL).strip()

    # 2. Strip everything before TITLE: or [Verse — model reasoning/planning
    title_pos = re.search(r"(?i)^\s*TITLE\s*[:\-]", raw, re.MULTILINE)
    verse_pos = re.search(r"\[Verse", raw, re.IGNORECASE)
    start = None
    if title_pos:
        start = title_pos.start()
    elif verse_pos:
        start = verse_pos.start()
    if start and start > 0:
        raw = raw[start:]

    # 3. Extract title
    title = ""
    m = _TITLE_RE.search(raw)
    body = raw
    if m:
        title = m.group(1).strip().strip("\"'")
        body = raw[m.end():]

    # 4. Extract gloss
    gloss = ""
    gm = _GLOSS_RE.search(body)
    if gm:
        gloss = body[gm.end():].strip()
        body = body[: gm.start()].strip()

    # 5. Clean meta-commentary lines from the body
    # Remove lines that are planning/annotations, not actual lyrics
    clean_lines = []
    for line in body.splitlines():
        stripped = line.strip()
        # Skip empty lines — preserve them as stanza breaks
        if not stripped:
            clean_lines.append("")
            continue
        # Skip meta-commentary patterns
        if re.match(r"^(Now let me|I'll start|Let me|I need to|I should|Here's|Here are|Okay|Starting with|Next)", stripped, re.IGNORECASE):
            continue
        # Skip structural annotations like "(Unique opening connecting to...)"
        if re.match(r"^\(.*\)\s*$", stripped) and len(stripped) > 15:
            continue
        # Skip lines that are just English instructions inside Indic sections
        # (contains section-like annotations with colons)
        if re.match(r"^\[.*\]:\s*\(", stripped):
            continue
        # Skip Talwaar/annotation-style bracketed descriptions
        if re.match(r"^\[(?!Verse|Chorus|Bridge|Outro|Intro|English)", stripped) and ":" in stripped:
            continue
        clean_lines.append(line)

    body = "\n".join(clean_lines).strip()
    # Collapse triple+ newlines to double
    body = re.sub(r"\n{3,}", "\n\n", body)

    return title, body, gloss


# --------------------------------------------------------------------------- #
# Single-language generation
# --------------------------------------------------------------------------- #
def generate_one(
    spec: GenSpec,
    model: str | None = None,
    temperature: float = 0.9,
    use_retrieval: bool = True,
) -> LyricResult:
    examples: list[Snippet] = []
    if use_retrieval:
        examples = retrieve_examples(
            spec.language, spec.theme, spec.emotion, spec.style, k=4
        )
        spec.retrieved_examples = [e.text for e in examples]

    messages = build_messages(spec)

    try:
        res = llm.generate(messages, model=model, temperature=temperature)
    except llm.LLMError as exc:
        return LyricResult(
            spec=spec, title="", lyrics="", gloss="", raw="",
            model=model or "?", is_mock=False, examples=examples,
            error=str(exc),
        )

    title, lyrics, gloss = _parse_output(res.text)

    script = LANGUAGES[spec.language].script
    target_scheme = RHYME_SCHEMES.get(spec.rhyme_scheme, {}).get("pattern", "FREE")
    target_syll = METRES.get(spec.metre, {}).get("syllables", 0)
    # Scale target for Indic languages (aksharas are denser than English syllables)
    if target_syll and spec.language in ("kannada", "hindi"):
        target_syll = int(target_syll * 1.6)
    analyses = [
        analyze_stanza(stanza, script, target_scheme, target_syll)
        for stanza in split_stanzas(lyrics)
    ]

    return LyricResult(
        spec=spec,
        title=title or "(untitled)",
        lyrics=lyrics,
        gloss=gloss,
        raw=res.text,
        model=res.model,
        is_mock=res.is_mock,
        examples=examples,
        stanza_analyses=analyses,
    )


# --------------------------------------------------------------------------- #
# Three-language comparison
# --------------------------------------------------------------------------- #
def generate_comparison(
    base: GenSpec,
    languages: list[str],
    model: str | None = None,
    temperature: float = 0.9,
    use_retrieval: bool = True,
) -> dict[str, LyricResult]:
    """Generate the same theme/emotion/style across multiple languages."""
    results: dict[str, LyricResult] = {}
    for i, lang in enumerate(languages):
        # Pause between generations to avoid Groq rate limits (free tier: 6K TPM)
        if i > 0:
            time.sleep(15)
        spec = GenSpec(
            language=lang,
            theme=base.theme,
            emotion=base.emotion,
            style=base.style,
            rhyme_scheme=base.rhyme_scheme,
            metre=base.metre,
            num_verses=base.num_verses,
            lines_per_verse=base.lines_per_verse,
            include_chorus=base.include_chorus,
            include_gloss=base.include_gloss,
            extra_instructions=base.extra_instructions,
        )
        results[lang] = generate_one(
            spec, model=model, temperature=temperature, use_retrieval=use_retrieval
        )
    return results
