# 🎶 Multilingual Song Lyric Generator with Cultural Context (PS-C2)

A GenAI tool that produces **original song lyrics in Kannada, Hindi and English**
for a given **theme, emotion and musical style** — grounded in **real public
lyric datasets** and each language's own cultural traditions.

Built for the 12-hour GenAI Hackathon, problem statement **PS-C2**.

---

## ✨ What it does (deliverables)

| Deliverable | How it's met |
|---|---|
| **Lyric generator for all 3 languages** | Kannada / Hindi / English, each written *natively* (not translated) via a culturally-aware prompt. |
| **Style selector (folk, pop, classical, rap)** | Each style carries language-specific tradition notes (e.g. Kannada *janapada*, Hindi *ghazal*, desi hip-hop). |
| **Rhyme scheme & metre options** | AABB / ABAB / ABCB / AAAA / free verse, and short/medium/long/free metre — and the app **measures** how well the output matches them. |
| **Demo: compare same theme in 3 languages** | "Compare 3 languages" tab renders Kannada, Hindi and English side by side, each with an English gloss. |

## 🧠 Why it respects "cultural context"

1. **Native re-imagining, not translation.** Each language gets its own prompt
   with curated cultural guidance — traditions (Dasa-sahitya, ghazal, Americana
   folk…), authentic imagery, idioms and a tasteful Hindustani / code-mixing
   register where appropriate.
2. **Retrieval-augmented grounding (RAG).** Before generating, the app retrieves
   real style/theme-relevant snippets from the public datasets and feeds them as
   *flavour-only inspiration* (never to copy) — so the vocabulary and idiom feel
   authentic while the lyrics stay original.
3. **Prosody verification.** An akshara-aware analyzer counts syllables and
   detects the realised rhyme scheme per stanza, scoring it against the target.

---

## 🏗️ Architecture

```
                ┌──────────────────────────────────────────────┐
  Public datasets│ ai4bharat/sangraha (Kannada)                 │
  (problem stmt) │ huggingartists (English lyrics)              │
                │ Kaggle isrc-data-with-lyrics (Hindi)         │
                └───────────────┬──────────────────────────────┘
                                │  scripts/prepare_data.py
                                ▼
                   data/corpus/*.jsonl  +  data/samples/*.jsonl
                                │
        theme / emotion / style │  (TF-IDF char-ngram retrieval)
        rhyme / metre           ▼
   UI (app.py) ─► retrieval.py ─► prompts.py ─► llm.py (Gemini) ─► lyrics.py
                                                                          │
                                                  analysis.py (rhyme/metre) ◄┘
                                                                          │
                                            Streamlit render (lyrics + gloss + scorecard)
```

| Module | Responsibility |
|---|---|
| `src/config.py` | Languages, styles, rhyme schemes, metres, **cultural-context KB** |
| `src/retrieval.py` | Loads corpus, TF-IDF char-ngram retrieval of real snippets |
| `src/prompts.py` | Builds the culturally-grounded system/user prompt |
| `src/llm.py` | Gemini REST client, OpenRouter fallback (+ offline mock) |
| `src/lyrics.py` | Orchestration + output parsing + per-stanza analysis |
| `src/analysis.py` | Akshara/syllable counting, rhyme detection, scheme/metre scoring |
| `src/dataset_loader.py` | Ingests the real public datasets into the corpus |
| `app.py` | Streamlit UI (compare + single modes) |

---

## 🚀 Quickstart

```bash
# 1. (recommended) virtual env
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # macOS/Linux

# 2. install
pip install -r requirements.txt

# 3. add your free Google Gemini key (NOT paid OpenAI)
copy .env.example .env          # Windows  (cp on macOS/Linux)
#   then edit .env -> GEMINI_API_KEY=AIza...

# 4. build the corpus from the listed public datasets (needs internet)
python scripts/prepare_data.py

# 5. run the app
streamlit run app.py
```

The app runs **even without** step 3 (mock mode) and step 4 (uses bundled
public-domain samples) — but do both for the real, dataset-grounded demo.

### Getting a free LLM key
Create a free **Google Gemini** key at **https://aistudio.google.com/apikey**
(free tier; strong Kannada/Hindi). Default model `gemini-2.0-flash`. The app
auto-detects the provider from your key: if you instead set `OPENROUTER_API_KEY`
(free key at https://openrouter.ai/keys), it uses OpenRouter as a fallback.
**No paid OpenAI API is used anywhere.**

---

## ✅ Hackathon rule compliance

- **No paid OpenAI API** — generation is via Google Gemini's free tier (with an
  optional OpenRouter free-model fallback).
- **Uses a listed public dataset** — `scripts/prepare_data.py` ingests
  `ai4bharat/sangraha`, `huggingartists` and the Kaggle Hindi lyrics set into the
  retrieval corpus; the sidebar shows live per-source counts as proof.
- **Not only dummy/synthetic data** — grounding uses real dataset lines plus
  bundled **public-domain** folk/classical lyrics (attributed in each record).
- **Attribution** — every snippet stores its `source`; the UI surfaces which real
  lines informed each generation.

## 🔧 Tech stack
Python · Streamlit · Google Gemini (multilingual LLM, free tier; OpenRouter
fallback) · scikit-learn (TF-IDF RAG) · Hugging Face `datasets` · pandas.
*(IndicTrans-compatible: ISO codes are tracked per language; the English gloss
can be swapped for IndicTrans2 if desired.)*

## ⚠️ Notes & limitations
- Prosody analysis is heuristic (akshara approximation for Indic scripts); it is
  feedback, not a strict constraint on the model.
- Bundled samples are short public-domain excerpts for grounding; the richer
  contemporary/pop/rap material comes from running `prepare_data.py`.
