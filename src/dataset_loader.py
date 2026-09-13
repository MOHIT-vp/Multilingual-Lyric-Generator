"""Ingest the REAL public datasets listed in the problem statement into a local
JSONL corpus used for retrieval-augmented grounding.

Sources (problem statement PS-C2):
  1. ai4bharat/sangraha          — high-quality Kannada text (HF)        -> Kannada
  2. huggingartists/*            — real song lyrics (HF)                 -> English
  3. ishikajohari/isrc-data-with-lyrics — Bollywood Hindi lyrics (Kaggle)-> Hindi

Every source is wrapped in try/except: if one is unavailable (gated, offline, no
Kaggle creds) we skip it and report, rather than failing the whole build. The
bundled public-domain samples in data/samples guarantee the app is never empty.

Run via `python scripts/prepare_data.py` (see that script for CLI options).
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from .config import CORPUS_DIR

# Script detection ----------------------------------------------------------- #
_KANNADA = re.compile(r"[ಀ-೿]")
_DEVANAGARI = re.compile(r"[ऀ-ॿ]")
_LATIN = re.compile(r"[A-Za-z]")
_SPLIT = re.compile(r"[\n।॥\.!?]+")


def _segment(text: str, script_re: re.Pattern, min_len=8, max_len=120) -> list[str]:
    out = []
    for part in _SPLIT.split(text or ""):
        s = " ".join(part.split())
        if not (min_len <= len(s) <= max_len):
            continue
        if not script_re.search(s):
            continue
        out.append(s)
    return out


class CorpusWriter:
    """Appends de-duplicated snippet records to a JSONL file."""

    def __init__(self, path: Path):
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._seen: set[str] = set()
        self._records: list[dict] = []

    def add(self, language: str, style: str, text: str, source: str) -> None:
        key = text.strip()
        if not key or key in self._seen:
            return
        self._seen.add(key)
        self._records.append(
            {"language": language, "style": style, "text": key, "source": source}
        )

    def flush(self) -> int:
        with self.path.open("w", encoding="utf-8") as fh:
            for rec in self._records:
                fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
        return len(self._records)


# --------------------------------------------------------------------------- #
# 1. Indic text — ai4bharat/sangraha  (multilingual: Kannada AND Hindi)
# --------------------------------------------------------------------------- #
# sangraha is the listed Kannada dataset, but it is in fact a 20+ language Indic
# corpus, so we draw both Kannada (verified/kan) and Hindi (verified/hin) real
# text from it for vocabulary/idiom grounding.
_SANGRAHA_DIR = {"kannada": "kan", "hindi": "hin"}
_SANGRAHA_SCRIPT = {"kannada": _KANNADA, "hindi": _DEVANAGARI}


def ingest_sangraha(writer: CorpusWriter, language: str, limit: int = 400) -> int:
    """Stream real <language> text from ai4bharat/sangraha; segment into lines."""
    from datasets import load_dataset  # lazy import

    code = _SANGRAHA_DIR[language]
    script_re = _SANGRAHA_SCRIPT[language]
    added = 0
    # Try a few known config/path shapes — the dataset layout has evolved.
    attempts = [
        dict(path="ai4bharat/sangraha", data_dir=f"verified/{code}", split="train"),
        dict(path="ai4bharat/sangraha", name="verified", split="train"),
        dict(path="ai4bharat/sangraha", split="train"),
    ]
    last_err = None
    for kw in attempts:
        try:
            ds = load_dataset(**kw, streaming=True)
            for row in ds:
                text = row.get("text") or row.get("content") or ""
                for line in _segment(text, script_re):
                    writer.add(language, "unknown", line, "ai4bharat/sangraha")
                    added += 1
                    if added >= limit:
                        return added
            if added:
                return added
        except Exception as exc:  # gated/offline/layout change
            last_err = exc
            continue
    if last_err:
        print(f"  [{language}/sangraha] skipped: {last_err}")
    return added


def ingest_kannada_sangraha(writer: CorpusWriter, limit: int = 400) -> int:
    """Backwards-compatible alias."""
    return ingest_sangraha(writer, "kannada", limit)


# --------------------------------------------------------------------------- #
# 2. English + Hindi — genius-song-lyrics (parquet, streamed, no credentials)
# --------------------------------------------------------------------------- #
# A large real lyric corpus with `language` and genre `tag` columns. We stream
# it (no full download) and keep only rows in the languages we want, mapping the
# Genius genre tag onto our {folk, pop, classical, rap} style taxonomy.
GENIUS_DATASET = "sebastiandizon/genius-song-lyrics"

_TAG_TO_STYLE = {
    "pop": "pop", "rap": "rap", "rb": "pop", "rock": "pop",
    "country": "folk", "misc": "unknown",
}


def ingest_genius_lyrics(
    writer: CorpusWriter,
    per_language: dict[str, int] | None = None,
    scan_cap: int = 60000,
) -> int:
    """Stream genius-song-lyrics and harvest English & Hindi lines.

    `per_language` maps language code -> max lines to keep (e.g. {"en":120,
    "hi":120}). `scan_cap` bounds how many rows we read so the run always
    terminates even when a language is rare in the stream.
    """
    from datasets import load_dataset  # lazy import

    per_language = per_language or {"en": 120, "hi": 120}
    lang_name = {"en": "english", "hi": "hindi"}
    script_re = {"en": _LATIN, "hi": re.compile(r"[ऀ-ॿA-Za-z]")}
    kept = {code: 0 for code in per_language}

    try:
        ds = load_dataset(GENIUS_DATASET, split="train", streaming=True)
    except Exception as exc:
        print(f"  [genius] skipped (could not open stream): {exc}")
        return 0

    added = 0
    scanned = 0
    try:
        for row in ds:
            scanned += 1
            if scanned > scan_cap:
                break
            code = (row.get("language") or "").lower()
            if code not in per_language or kept[code] >= per_language[code]:
                if all(kept[c] >= per_language[c] for c in per_language):
                    break
                continue
            style = _TAG_TO_STYLE.get((row.get("tag") or "").lower(), "unknown")
            text = row.get("lyrics") or row.get("text") or ""
            for line in _segment(text, script_re[code], min_len=12, max_len=100):
                writer.add(lang_name[code], style, line, f"hf:{GENIUS_DATASET}")
                added += 1
                kept[code] += 1
                if kept[code] >= per_language[code]:
                    break
    except Exception as exc:
        print(f"  [genius] stream interrupted after {scanned} rows: {exc}")

    print(f"  [genius] scanned {scanned} rows, kept {kept}")
    return added


# --------------------------------------------------------------------------- #
# 3. Hindi — Kaggle Bollywood lyrics (optional, needs creds)
# --------------------------------------------------------------------------- #
def ingest_hindi_kaggle(writer: CorpusWriter, limit: int = 400) -> int:
    """Download the Kaggle Hindi lyrics dataset if KAGGLE creds are present."""
    import os

    if not (os.getenv("KAGGLE_USERNAME") and os.getenv("KAGGLE_KEY")):
        print("  [hindi/kaggle] skipped: no KAGGLE_USERNAME / KAGGLE_KEY set")
        return 0
    try:
        import kaggle  # noqa: F401  (auth happens on import)
        import pandas as pd
    except Exception as exc:
        print(f"  [hindi/kaggle] skipped: {exc} (pip install kaggle)")
        return 0

    dest = CORPUS_DIR / "_kaggle_hindi"
    dest.mkdir(parents=True, exist_ok=True)
    try:
        from kaggle.api.kaggle_api_extended import KaggleApi

        api = KaggleApi()
        api.authenticate()
        api.dataset_download_files(
            "ishikajohari/isrc-data-with-lyrics", path=str(dest), unzip=True
        )
    except Exception as exc:
        print(f"  [hindi/kaggle] download failed: {exc}")
        return 0

    added = 0
    for csv in dest.glob("*.csv"):
        try:
            df = pd.read_csv(csv)
        except Exception:
            continue
        col = next(
            (c for c in df.columns if "lyric" in c.lower() or "text" in c.lower()),
            None,
        )
        if not col:
            continue
        for val in df[col].dropna().astype(str):
            # Hindi lyrics CSVs may be romanised or in Devanagari — accept both.
            for line in _segment(val, re.compile(r"[ऀ-ॿA-Za-z]"),
                                 min_len=12, max_len=100):
                style = "pop"  # Bollywood filmi ≈ pop for our taxonomy
                writer.add("hindi", style, line,
                           "kaggle:ishikajohari/isrc-data-with-lyrics")
                added += 1
                if added >= limit:
                    return added
    return added


# --------------------------------------------------------------------------- #
# Orchestration
# --------------------------------------------------------------------------- #
def build_corpus(
    kannada_limit: int = 400,
    english_limit: int = 150,
    hindi_limit: int = 150,
    genius_scan_cap: int = 40000,
) -> dict:
    """Build data/corpus/public_datasets.jsonl from all available sources."""
    writer = CorpusWriter(CORPUS_DIR / "public_datasets.jsonl")
    report = {}

    print("Ingesting Kannada (ai4bharat/sangraha verified/kan)…")
    report["kannada"] = ingest_sangraha(writer, "kannada", kannada_limit)

    print("Ingesting Hindi (ai4bharat/sangraha verified/hin)…")
    report["hindi_sangraha"] = ingest_sangraha(writer, "hindi", hindi_limit)

    print("Ingesting English (genius-song-lyrics, streamed)…")
    before = len(writer._records)
    ingest_genius_lyrics(
        writer,
        per_language={"en": english_limit},
        scan_cap=genius_scan_cap,
    )
    report["english"] = sum(
        1 for r in writer._records[before:] if r["language"] == "english"
    )

    print("Ingesting Hindi (Kaggle Bollywood lyrics, optional)…")
    report["hindi_kaggle"] = ingest_hindi_kaggle(writer, hindi_limit)
    report["hindi"] = report["hindi_sangraha"] + report["hindi_kaggle"]

    report["total_written"] = writer.flush()
    return report
