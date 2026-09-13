"""Dataset-grounded few-shot retrieval.

Loads the local lyric corpus (built from the REAL public datasets by
`scripts/prepare_data.py`, with bundled real samples as a fallback) and returns
style/theme-relevant snippets to inject into the prompt as cultural inspiration.

We use TF-IDF over character n-grams: it is dependency-light (scikit-learn),
needs no GPU, and works across Latin, Devanagari and Kannada scripts where a
word-level vectoriser would struggle.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from .config import CORPUS_DIR, SAMPLES_DIR, STYLES


@dataclass
class Snippet:
    language: str
    style: str
    text: str
    source: str


def _read_jsonl(path: Path) -> list[Snippet]:
    out: list[Snippet] = []
    if not path.exists():
        return out
    with path.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                d = json.loads(line)
            except json.JSONDecodeError:
                continue
            text = (d.get("text") or "").strip()
            if not text:
                continue
            out.append(
                Snippet(
                    language=d.get("language", "unknown"),
                    style=d.get("style", "unknown"),
                    text=text,
                    source=d.get("source", "unknown"),
                )
            )
    return out


@lru_cache(maxsize=1)
def load_corpus() -> tuple[Snippet, ...]:
    """Load all snippets. Prefers the built corpus; always includes bundled
    samples so the app is never empty. Cached for the process lifetime."""
    snippets: list[Snippet] = []
    for path in sorted(CORPUS_DIR.glob("*.jsonl")):
        snippets.extend(_read_jsonl(path))
    for path in sorted(SAMPLES_DIR.glob("*.jsonl")):
        snippets.extend(_read_jsonl(path))
    return tuple(snippets)


def corpus_stats() -> dict:
    """Counts per language / source — surfaced in the UI to prove real-data use."""
    corpus = load_corpus()
    by_lang: dict[str, int] = {}
    by_source: dict[str, int] = {}
    for s in corpus:
        by_lang[s.language] = by_lang.get(s.language, 0) + 1
        by_source[s.source] = by_source.get(s.source, 0) + 1
    return {"total": len(corpus), "by_language": by_lang, "by_source": by_source}


class _LangIndex:
    """A TF-IDF index over one language's snippets (built lazily)."""

    def __init__(self, snippets: list[Snippet]):
        self.snippets = snippets
        self._matrix = None
        self._vectorizer = None

    def _ensure_built(self):
        if self._matrix is not None or not self.snippets:
            return
        from sklearn.feature_extraction.text import TfidfVectorizer  # lazy

        self._vectorizer = TfidfVectorizer(
            analyzer="char_wb", ngram_range=(2, 4), min_df=1, lowercase=True
        )
        self._matrix = self._vectorizer.fit_transform(
            [s.text for s in self.snippets]
        )

    def query(self, text: str, k: int) -> list[tuple[Snippet, float]]:
        self._ensure_built()
        if self._matrix is None:
            return []
        from sklearn.metrics.pairwise import cosine_similarity  # lazy

        q = self._vectorizer.transform([text])
        sims = cosine_similarity(q, self._matrix)[0]
        ranked = sorted(
            zip(self.snippets, sims), key=lambda t: t[1], reverse=True
        )
        return ranked[:k]


@lru_cache(maxsize=8)
def _index_for(language: str) -> _LangIndex:
    snips = [s for s in load_corpus() if s.language == language]
    return _LangIndex(snips)


def retrieve_examples(
    language: str,
    theme: str,
    emotion: str,
    style: str,
    k: int = 4,
) -> list[Snippet]:
    """Return up to *k* real snippets for grounding, preferring style matches.

    Strategy: build a query from theme + emotion + the style's description, rank
    all snippets in the language, then re-rank to favour same-style snippets.
    """
    index = _index_for(language)
    if not index.snippets:
        return []
    style_desc = STYLES.get(style, {}).get("description", "")
    query = f"{theme} {emotion} {style} {style_desc}".strip()

    # Pull a generous candidate pool, then prefer style matches.
    pool = index.query(query, k=max(k * 4, 12))
    same_style = [s for s, _ in pool if s.style == style]
    others = [s for s, _ in pool if s.style != style]
    ordered = same_style + others

    # De-duplicate by text while preserving order.
    seen: set[str] = set()
    result: list[Snippet] = []
    for s in ordered:
        key = s.text.strip()
        if key in seen:
            continue
        seen.add(key)
        result.append(s)
        if len(result) >= k:
            break
    return result
