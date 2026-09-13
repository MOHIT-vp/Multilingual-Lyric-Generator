"""Multilingual Song Lyric Generator with Cultural Context — Streamlit UI (PS-C2).

Two modes:
  • Single language  — generate + analyse one set of lyrics.
  • Compare 3 languages — same theme/emotion/style rendered natively in
    Kannada, Hindi and English, side by side (the headline demo deliverable).

Run:  streamlit run app.py
"""

from __future__ import annotations

import io
import os

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

from src import llm
from src.analysis import StanzaAnalysis
from src.config import (
    COMPARE_ORDER,
    EMOTIONS,
    GenSpec,
    LANGUAGES,
    METRES,
    RHYME_SCHEMES,
    STYLES,
    default_model_for,
    models_for,
)
from src.lyrics import LyricResult, generate_comparison, generate_one
from src.retrieval import corpus_stats

st.set_page_config(
    page_title="Multilingual Lyric Generator — Cultural Context",
    page_icon="🎵",
    layout="wide",
)


# --------------------------------------------------------------------------- #
# Sidebar — engine config + data provenance
# --------------------------------------------------------------------------- #
def sidebar() -> dict:
    st.sidebar.title("🎛️ Engine")

    prov = llm.provider()
    if prov == "gemini":
        st.sidebar.success("Google Gemini key detected ✓")
    elif prov == "openrouter":
        st.sidebar.success("OpenRouter key detected ✓ (Gemini fallback)")
    else:
        st.sidebar.warning(
            "No API key found — running in **mock mode**. Add a free "
            "`GEMINI_API_KEY` to `.env` (aistudio.google.com/apikey) for real lyrics."
        )
        with st.sidebar.expander("Paste a Gemini key for this session"):
            k = st.text_input("GEMINI_API_KEY", type="password",
                              label_visibility="collapsed")
            if k:
                os.environ["GEMINI_API_KEY"] = k.strip()
                st.rerun()

    ui_prov = prov if prov != "mock" else "gemini"
    model_list = models_for(ui_prov)
    default_model = os.getenv("LLM_MODEL", default_model_for(ui_prov))
    idx = model_list.index(default_model) if default_model in model_list else 0
    model = st.sidebar.selectbox(f"Model ({ui_prov})", model_list, index=idx)
    custom = st.sidebar.text_input("…or a custom model id", "")
    if custom.strip():
        model = custom.strip()

    temperature = st.sidebar.slider("Creativity (temperature)", 0.0, 1.3, 0.9, 0.05)
    use_retrieval = st.sidebar.checkbox(
        "Ground in real dataset examples (RAG)", value=True,
        help="Inject style/theme-relevant snippets from the public datasets.",
    )

    st.sidebar.divider()
    st.sidebar.subheader("📚 Dataset provenance")
    stats = corpus_stats()
    st.sidebar.caption(
        "Grounding corpus built from the listed public datasets "
        "(ai4bharat/sangraha, huggingartists, Kaggle Hindi lyrics) plus "
        "bundled public-domain folk/classical samples."
    )
    st.sidebar.metric("Total grounding snippets", stats["total"])
    st.sidebar.write("By language:", stats["by_language"])
    with st.sidebar.expander("By source"):
        st.write(stats["by_source"])
    st.sidebar.caption(
        "Empty/low? Run `python scripts/prepare_data.py` to pull the full "
        "datasets (needs internet)."
    )

    return {"model": model, "temperature": temperature,
            "use_retrieval": use_retrieval}


# --------------------------------------------------------------------------- #
# Shared input controls
# --------------------------------------------------------------------------- #
def song_inputs(key_prefix: str) -> dict:
    c1, c2 = st.columns([2, 1])
    theme = c1.text_input("Theme", "first rain after a long summer",
                          key=f"{key_prefix}_theme")
    emotion = c2.selectbox("Emotion / mood", EMOTIONS, index=3,
                           key=f"{key_prefix}_emotion")

    c3, c4, c5 = st.columns(3)
    style = c3.selectbox(
        "Musical style", list(STYLES.keys()),
        format_func=lambda s: STYLES[s]["label"], key=f"{key_prefix}_style",
    )
    rhyme = c4.selectbox(
        "Rhyme scheme", list(RHYME_SCHEMES.keys()),
        format_func=lambda r: RHYME_SCHEMES[r]["label"], key=f"{key_prefix}_rhyme",
    )
    metre = c5.selectbox(
        "Metre", list(METRES.keys()),
        format_func=lambda m: METRES[m]["label"], key=f"{key_prefix}_metre",
    )
    st.caption(
        f"💡 {RHYME_SCHEMES[rhyme]['hint']}  •  {METRES[metre]['hint']}  •  "
        f"{STYLES[style]['description']}"
    )

    c6, c7, c8, c9 = st.columns(4)
    verses = c6.number_input("Verses", 1, 4, 2, key=f"{key_prefix}_verses")
    lpv = c7.number_input("Lines / verse", 2, 8, 4, key=f"{key_prefix}_lpv")
    chorus = c8.checkbox("Chorus", True, key=f"{key_prefix}_chorus")
    gloss = c9.checkbox("English gloss", True, key=f"{key_prefix}_gloss",
                        help="Adds line-by-line English meaning for Indic lyrics.")

    extra = st.text_input("Extra instructions (optional)", "",
                          key=f"{key_prefix}_extra")

    return dict(theme=theme, emotion=emotion, style=style, rhyme_scheme=rhyme,
                metre=metre, num_verses=int(verses), lines_per_verse=int(lpv),
                include_chorus=chorus, include_gloss=gloss, extra_instructions=extra)


def spec_from_inputs(language: str, inp: dict) -> GenSpec:
    return GenSpec(language=language, **inp)


# --------------------------------------------------------------------------- #
# Rendering
# --------------------------------------------------------------------------- #
def _analysis_table(analyses: list[StanzaAnalysis]):
    rows = []
    for i, st_an in enumerate(analyses, 1):
        for j, line in enumerate(st_an.lines, 1):
            rows.append({
                "stanza": i,
                "line": j,
                "rhyme": line.rhyme_label,
                "syllables": line.syllables,
                "text": line.text,
            })
    if rows:
        st.dataframe(rows, hide_index=True, use_container_width=True)


def render_result(res: LyricResult, show_details: bool = True):
    if res.error:
        st.error(f"Generation failed: {res.error}")
        return

    if res.is_mock:
        st.info("🔧 Mock output (no API key). Add OPENROUTER_API_KEY for real lyrics.")

    st.markdown(f"### 🎵 {res.title}")
    lang = LANGUAGES[res.spec.language]
    st.caption(
        f"{lang.name} ({lang.native_name}) • {STYLES[res.spec.style]['label']} • "
        f"{res.spec.emotion} • {RHYME_SCHEMES[res.spec.rhyme_scheme]['label']} • "
        f"model: {res.model}"
    )

    st.text(res.lyrics)

    if res.gloss:
        with st.expander("🌐 English gloss (line-by-line meaning)"):
            st.text(res.gloss)

    # Prosody scorecard
    m1, m2, m3 = st.columns(3)
    m1.metric("Rhyme match vs target", f"{res.avg_rhyme_match:.0f}%")
    m2.metric("Metre match vs target", f"{res.avg_metre_match:.0f}%")
    avg_syll = (
        sum(s.avg_syllables for s in res.stanza_analyses) / len(res.stanza_analyses)
        if res.stanza_analyses else 0
    )
    m3.metric("Avg syllables / line", f"{avg_syll:.1f}")

    if show_details:
        with st.expander("🔎 Rhyme & metre analysis (detected scheme per stanza)"):
            for i, an in enumerate(res.stanza_analyses, 1):
                st.write(
                    f"**Stanza {i}** — detected `{an.detected_scheme}` "
                    f"vs target `{an.target_scheme}` • "
                    f"avg {an.avg_syllables} syllables"
                )
            _analysis_table(res.stanza_analyses)

        if res.examples:
            with st.expander("📖 Real dataset snippets used for grounding"):
                st.caption("Used as cultural/idiomatic inspiration only — outputs are original.")
                for ex in res.examples:
                    st.markdown(f"- *{ex.text}*  \n  <small>— {ex.source}</small>",
                                unsafe_allow_html=True)

    st.download_button(
        "⬇️ Download lyrics (.txt)",
        data=_as_text(res),
        file_name=f"lyrics_{res.spec.language}_{res.spec.style}.txt",
        mime="text/plain",
        key=f"dl_{res.spec.language}_{id(res)}",
    )


def _as_text(res: LyricResult) -> str:
    buf = io.StringIO()
    buf.write(f"TITLE: {res.title}\n")
    buf.write(f"Language: {res.language_name} | Style: {res.spec.style} | "
              f"Emotion: {res.spec.emotion}\n")
    buf.write(f"Rhyme: {res.spec.rhyme_scheme} | Metre: {res.spec.metre} | "
              f"Model: {res.model}\n")
    buf.write("=" * 50 + "\n\n")
    buf.write(res.lyrics + "\n")
    if res.gloss:
        buf.write("\n[English Gloss]\n" + res.gloss + "\n")
    return buf.getvalue()


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #
def main():
    cfg = sidebar()

    st.title("🎶 Multilingual Song Lyric Generator")
    st.markdown(
        "Original lyrics in **Kannada · Hindi · English**, grounded in real "
        "public lyric datasets and each language's own cultural traditions. "
        "_(PS-C2)_"
    )

    tab_compare, tab_single = st.tabs(
        ["🌍 Compare 3 languages", "🎤 Single language"]
    )

    # ---- Compare mode (headline demo) -------------------------------------- #
    with tab_compare:
        st.subheader("Same theme, three languages — side by side")
        inp = song_inputs("cmp")
        langs = st.multiselect(
            "Languages", COMPARE_ORDER, default=COMPARE_ORDER,
            format_func=lambda l: f"{LANGUAGES[l].name} ({LANGUAGES[l].native_name})",
        )
        if st.button("✨ Generate in all selected languages", type="primary",
                     key="gen_cmp"):
            if not inp["theme"].strip():
                st.warning("Please enter a theme.")
            elif not langs:
                st.warning("Pick at least one language.")
            else:
                base = spec_from_inputs(langs[0], inp)
                with st.spinner("Composing across languages…"):
                    results = generate_comparison(
                        base, langs, model=cfg["model"],
                        temperature=cfg["temperature"],
                        use_retrieval=cfg["use_retrieval"],
                    )
                st.session_state["cmp_results"] = results

        results = st.session_state.get("cmp_results")
        if results:
            cols = st.columns(len(results))
            for col, (lang, res) in zip(cols, results.items()):
                with col:
                    render_result(res, show_details=True)

    # ---- Single mode ------------------------------------------------------- #
    with tab_single:
        st.subheader("Generate & fine-tune one language")
        language = st.selectbox(
            "Language", list(LANGUAGES.keys()),
            format_func=lambda l: f"{LANGUAGES[l].name} ({LANGUAGES[l].native_name})",
            key="single_lang",
        )
        inp = song_inputs("sng")
        if st.button("✨ Generate", type="primary", key="gen_single"):
            if not inp["theme"].strip():
                st.warning("Please enter a theme.")
            else:
                spec = spec_from_inputs(language, inp)
                with st.spinner("Composing…"):
                    res = generate_one(
                        spec, model=cfg["model"],
                        temperature=cfg["temperature"],
                        use_retrieval=cfg["use_retrieval"],
                    )
                st.session_state["single_result"] = res

        res = st.session_state.get("single_result")
        if res:
            render_result(res, show_details=True)

    st.divider()
    st.caption(
        "Built for PS-C2 • LLM via Google Gemini (free; OpenRouter fallback) • "
        "RAG grounding on ai4bharat/sangraha + huggingartists + Kaggle Hindi "
        "lyrics • prosody analysis is heuristic (akshara-based for Indic scripts)."
    )


if __name__ == "__main__":
    main()
