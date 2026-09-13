"""CLI to build the lyric corpus from the REAL public datasets (PS-C2).

Usage:
    python scripts/prepare_data.py                 # default sizes
    python scripts/prepare_data.py --kannada 800 --english 120 --hindi 600

This downloads/streams the listed datasets and writes
    data/corpus/public_datasets.jsonl
The Streamlit app reads this automatically (plus the bundled public-domain
samples). Re-run any time to refresh or grow the corpus.

Requires: pip install datasets huggingface_hub   (+ kaggle for the Hindi set)
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Allow running as a plain script: add project root to sys.path.
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.dataset_loader import build_corpus  # noqa: E402
from src.retrieval import corpus_stats, load_corpus  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser(description="Build the PS-C2 lyric corpus.")
    ap.add_argument("--kannada", type=int, default=400,
                    help="max Kannada lines from ai4bharat/sangraha")
    ap.add_argument("--english", type=int, default=150,
                    help="max English lines from genius-song-lyrics (streamed)")
    ap.add_argument("--hindi", type=int, default=150,
                    help="max Hindi lines (genius stream + optional Kaggle)")
    ap.add_argument("--scan-cap", type=int, default=60000,
                    help="max rows to scan in the genius stream before stopping")
    args = ap.parse_args()

    print("=" * 64)
    print("Building corpus from listed public datasets (PS-C2)…")
    print("=" * 64)
    report = build_corpus(
        kannada_limit=args.kannada,
        english_limit=args.english,
        hindi_limit=args.hindi,
        genius_scan_cap=args.scan_cap,
    )

    print("\nPer-language lines added this run:")
    for k in ("kannada", "english", "hindi"):
        print(f"  {k:8s}: {report.get(k, 0)}")
    print(f"  written : {report.get('total_written', 0)} "
          f"-> data/corpus/public_datasets.jsonl")

    # Clear the load_corpus cache so stats reflect the new file.
    load_corpus.cache_clear()
    stats = corpus_stats()
    print("\nTotal corpus now available to the app (incl. bundled samples):")
    print(f"  total snippets: {stats['total']}")
    print(f"  by language   : {stats['by_language']}")
    print(f"  by source     : {stats['by_source']}")

    if report.get("total_written", 0) == 0:
        print(
            "\nNOTE: No external lines were ingested (offline or sources "
            "gated). The app will still run on the bundled public-domain "
            "samples. Re-run with internet to pull the listed datasets."
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
