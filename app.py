"""Multilingual Song Lyric Generator — Cyberpunk UI with Animations.

PS-C2: Produces original song lyrics in Kannada, Hindi, and English
for a given theme, emotion, and musical style.

Run: streamlit run app.py
"""

from __future__ import annotations

import io
import os

import streamlit as st
import streamlit.components.v1 as components
from dotenv import load_dotenv

load_dotenv()

from src import llm
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

# ─────────────────────────────────────────────────────────────────────────────
# Page Configuration
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Lyric Forge — Multilingual Song Lyric Generator",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────────────────────────────────────
# CYBERPUNK THEME + ANIMATIONS CSS
# ─────────────────────────────────────────────────────────────────────────────
CYBERPUNK_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@300;400;500;600;700&family=Inter:wght@400;500;600;700;800;900&display=swap');

    /* ── Hide Streamlit default chrome ── */
    #MainMenu {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    header {visibility: hidden !important;}
    [data-testid="stDecoration"] {visibility: hidden !important;}
    [data-testid="stStatusWidget"] {visibility: hidden !important;}
    [data-testid="stToolbar"] {visibility: hidden !important;}
    [data-testid="collapsedControl"] {display: none !important;}

    /* ── Global dark theme ── */
    .stApp {
        background-color: #000 !important;
        color: #fff !important;
        font-family: 'Inter', sans-serif !important;
    }

    .block-container {
        max-width: 1200px !important;
        padding-top: 0 !important;
    }

    /* ── Form controls - cyberpunk HUD style ── */
    .stSelectbox > div > div,
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stTextArea > div > div > textarea {
        background-color: #0a0a0a !important;
        color: #fff !important;
        border: 1px solid rgba(255,255,255,0.15) !important;
        border-radius: 4px !important;
        font-family: 'IBM Plex Mono', monospace !important;
        font-size: 13px !important;
    }
    .stSelectbox > div > div:hover,
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #c0fb50 !important;
        box-shadow: 0 0 0 1px rgba(192,251,80,0.3) !important;
    }

    /* ── Labels ── */
    .stSelectbox label,
    .stTextInput label,
    .stNumberInput label,
    .stTextArea label,
    .stCheckbox label,
    .stMultiSelect label {
        font-family: 'IBM Plex Mono', monospace !important;
        font-size: 11px !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
        color: rgba(255,255,255,0.6) !important;
        font-weight: 500 !important;
    }

    /* ── Buttons ── */
    .stButton > button {
        background-color: #c0fb50 !important;
        color: #000 !important;
        border: none !important;
        border-radius: 4px !important;
        font-family: 'IBM Plex Mono', monospace !important;
        font-weight: 700 !important;
        font-size: 13px !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
        padding: 0.75rem 2rem !important;
        transition: all 0.3s cubic-bezier(0.4,0,0.2,1) !important;
        width: 100% !important;
    }
    .stButton > button:hover {
        background-color: #fff !important;
        color: #000 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 30px rgba(192,251,80,0.4) !important;
    }

    /* ── Download button ── */
    .stDownloadButton > button {
        background-color: transparent !important;
        color: #c0fb50 !important;
        border: 1px solid rgba(192,251,80,0.4) !important;
        border-radius: 4px !important;
        font-family: 'IBM Plex Mono', monospace !important;
        font-size: 11px !important;
        text-transform: uppercase !important;
    }
    .stDownloadButton > button:hover {
        background-color: rgba(192,251,80,0.1) !important;
        border-color: #c0fb50 !important;
    }

    /* ── Tabs ── */
    .stTabs [data-baseweb="tab-list"] {
        background-color: transparent !important;
        border-bottom: 1px solid rgba(255,255,255,0.1) !important;
        gap: 0 !important;
    }
    .stTabs [data-baseweb="tab"] {
        font-family: 'IBM Plex Mono', monospace !important;
        font-size: 12px !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
        color: rgba(255,255,255,0.4) !important;
        border: none !important;
        background: transparent !important;
        padding: 1rem 1.5rem !important;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        color: #c0fb50 !important;
        border-bottom: 2px solid #c0fb50 !important;
        background: transparent !important;
    }

    /* ── Metrics ── */
    [data-testid="stMetric"] {
        background: rgba(255,255,255,0.03) !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        border-radius: 4px !important;
        padding: 1rem !important;
    }
    [data-testid="stMetricValue"] {
        font-family: 'Inter', sans-serif !important;
        font-weight: 700 !important;
        color: #c0fb50 !important;
    }
    [data-testid="stMetricLabel"] {
        font-family: 'IBM Plex Mono', monospace !important;
        font-size: 11px !important;
        text-transform: uppercase !important;
        color: rgba(255,255,255,0.5) !important;
    }

    /* ── Expanders ── */
    .streamlit-expanderHeader {
        font-family: 'IBM Plex Mono', monospace !important;
        font-size: 12px !important;
        text-transform: uppercase !important;
        color: rgba(255,255,255,0.6) !important;
        background: rgba(255,255,255,0.03) !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
    }

    /* ── Spinner ── */
    .stSpinner > div {
        border-top-color: #c0fb50 !important;
    }
    .stSpinner > div > span {
        color: rgba(255,255,255,0.6) !important;
        font-family: 'IBM Plex Mono', monospace !important;
    }

    /* ── Alerts ── */
    .stAlert {
        background: rgba(255,255,255,0.03) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        color: #fff !important;
        font-family: 'IBM Plex Mono', monospace !important;
        font-size: 12px !important;
    }

    /* ── Caption ── */
    .stCaption, .stMarkdown small {
        font-family: 'IBM Plex Mono', monospace !important;
        color: rgba(255,255,255,0.35) !important;
    }

    /* ── MultiSelect ── */
    .stMultiSelect > div > div {
        background-color: #0a0a0a !important;
        border: 1px solid rgba(255,255,255,0.15) !important;
        color: #fff !important;
    }
    .stMultiSelect [data-baseweb="tag"] {
        background-color: rgba(192,251,80,0.15) !important;
        color: #c0fb50 !important;
        border: 1px solid rgba(192,251,80,0.3) !important;
    }

    /* ── Divider ── */
    hr {
        border-color: rgba(255,255,255,0.08) !important;
    }

    /* ── Scrollbar ── */
    ::-webkit-scrollbar { width: 4px; }
    ::-webkit-scrollbar-track { background: #000; }
    ::-webkit-scrollbar-thumb { background: rgba(192,251,80,0.3); border-radius: 2px; }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background-color: #050505 !important;
        border-right: 1px solid rgba(192, 251, 80, 0.15) !important;
    }
    [data-testid="stSidebar"] .stMarkdown,
    [data-testid="stSidebar"] label {
        color: #fff !important;
        font-family: 'IBM Plex Mono', monospace !important;
    }
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stSlider label {
        text-transform: uppercase !important;
        font-size: 11px !important;
        letter-spacing: 0.05em !important;
        color: rgba(255,255,255,0.6) !important;
    }
</style>
"""

st.markdown(CYBERPUNK_CSS, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# Animated Hero Banner (HTML/CSS/JS — lightweight, no KPR iframe)
# ─────────────────────────────────────────────────────────────────────────────
HERO_HTML = """
<div id="hero-banner">
  <canvas id="particle-canvas"></canvas>
  <div class="hero-content">
    <div class="hero-badge">
      <span class="badge-dot"></span>
      PS-C2 · MULTILINGUAL SONG LYRIC GENERATOR
    </div>
    <h1 class="hero-title">
      <span class="title-line">LYRIC</span>
      <span class="title-line title-accent">FORGE</span>
    </h1>
    <p class="hero-desc">
      GENERATE ORIGINAL SONG LYRICS IN <span class="hl">KANNADA</span> · 
      <span class="hl">HINDI</span> · <span class="hl">ENGLISH</span><br>
      WITH CULTURAL CONTEXT, RHYME SCHEMES & METRE CONTROL
    </p>
    <div class="hero-stats">
      <div class="stat">
        <span class="stat-num">3</span>
        <span class="stat-label">LANGUAGES</span>
      </div>
      <div class="stat-sep"></div>
      <div class="stat">
        <span class="stat-num">4</span>
        <span class="stat-label">MUSICAL STYLES</span>
      </div>
      <div class="stat-sep"></div>
      <div class="stat">
        <span class="stat-num">5</span>
        <span class="stat-label">RHYME SCHEMES</span>
      </div>
      <div class="stat-sep"></div>
      <div class="stat">
        <span class="stat-num">10</span>
        <span class="stat-label">EMOTIONS</span>
      </div>
    </div>
    <div class="scroll-hint">
      <span>SCROLL TO COMPOSE</span>
      <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
        <path d="M8 2V14M8 14L2 8M8 14L14 8" stroke="#c0fb50" stroke-width="1.5"/>
      </svg>
    </div>
  </div>
  <div class="hero-grid-lines">
    <div class="grid-line grid-line-h1"></div>
    <div class="grid-line grid-line-h2"></div>
    <div class="grid-line grid-line-v1"></div>
    <div class="grid-line grid-line-v2"></div>
  </div>
  <div class="corner-mark corner-tl">◢</div>
  <div class="corner-mark corner-tr">◣</div>
  <div class="corner-mark corner-bl">◥</div>
  <div class="corner-mark corner-br">◤</div>
  <div class="music-notes">
    <span class="note" style="left:5%;animation-delay:0s;animation-duration:8s">♪</span>
    <span class="note" style="left:15%;animation-delay:1.2s;animation-duration:10s">♫</span>
    <span class="note" style="left:25%;animation-delay:3s;animation-duration:9s">♩</span>
    <span class="note" style="left:35%;animation-delay:0.5s;animation-duration:11s">♬</span>
    <span class="note" style="left:45%;animation-delay:2.5s;animation-duration:8.5s">𝄞</span>
    <span class="note" style="left:55%;animation-delay:1.8s;animation-duration:10.5s">♪</span>
    <span class="note" style="left:65%;animation-delay:4s;animation-duration:9.5s">♫</span>
    <span class="note" style="left:75%;animation-delay:0.8s;animation-duration:11.5s">♩</span>
    <span class="note" style="left:85%;animation-delay:3.5s;animation-duration:8s">♬</span>
    <span class="note" style="left:92%;animation-delay:2s;animation-duration:10s">𝄞</span>
    <span class="note" style="left:10%;animation-delay:5s;animation-duration:9s">𝄢</span>
    <span class="note" style="left:50%;animation-delay:6s;animation-duration:12s">♪</span>
  </div>
</div>

<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { background: #000; overflow: hidden; }

  #hero-banner {
    position: relative;
    width: 100%;
    height: 100%;
    min-height: 520px;
    background: #000;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    font-family: 'Inter', 'Segoe UI', sans-serif;
  }

  #particle-canvas {
    position: absolute;
    top: 0; left: 0;
    width: 100%; height: 100%;
    pointer-events: none;
  }

  .hero-content {
    position: relative;
    z-index: 2;
    text-align: center;
    padding: 2rem;
  }

  .hero-badge {
    font-family: 'IBM Plex Mono', 'Courier New', monospace;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: rgba(255,255,255,0.4);
    margin-bottom: 1.5rem;
    opacity: 0;
    animation: fadeSlideUp 0.8s ease 0.3s forwards;
  }
  .badge-dot {
    display: inline-block;
    width: 6px; height: 6px;
    border-radius: 50%;
    background: #c0fb50;
    margin-right: 8px;
    vertical-align: middle;
    animation: pulse 2s ease infinite;
  }

  .hero-title {
    display: flex;
    flex-direction: row;
    align-items: baseline;
    justify-content: center;
    gap: 0.4em;
    margin-bottom: 1.2rem;
  }
  .title-line {
    font-weight: 900;
    font-size: clamp(3.5rem, 10vw, 8rem);
    letter-spacing: -0.07em;
    line-height: 1;
    color: #fff;
    opacity: 0;
    animation: titleReveal 1s cubic-bezier(0.16,1,0.3,1) 0.5s forwards;
  }
  .title-accent {
    color: #c0fb50;
    animation-delay: 0.7s;
    text-shadow: 0 0 80px rgba(192,251,80,0.3);
  }

  .hero-desc {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 12px;
    letter-spacing: 0.06em;
    line-height: 1.8;
    color: rgba(255,255,255,0.45);
    max-width: 600px;
    margin: 0 auto 2rem;
    opacity: 0;
    animation: fadeSlideUp 0.8s ease 1s forwards;
  }
  .hero-desc .hl {
    color: #c0fb50;
    font-weight: 600;
  }

  .hero-stats {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 1.5rem;
    opacity: 0;
    animation: fadeSlideUp 0.8s ease 1.2s forwards;
  }
  .stat { text-align: center; }
  .stat-num {
    display: block;
    font-weight: 800;
    font-size: 2rem;
    color: #fff;
    letter-spacing: -0.04em;
  }
  .stat-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 9px;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: rgba(255,255,255,0.35);
  }
  .stat-sep {
    width: 1px;
    height: 30px;
    background: rgba(255,255,255,0.1);
  }

  .scroll-hint {
    position: absolute;
    bottom: 0;
    left: 50%; transform: translateX(-50%);
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: rgba(255,255,255,0.25);
    display: flex;
    align-items: center;
    gap: 6px;
    opacity: 0;
    animation: fadeSlideUp 0.8s ease 1.5s forwards, float 3s ease-in-out 2s infinite;
  }

  /* Grid lines */
  .hero-grid-lines { position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; }
  .grid-line { position: absolute; background: rgba(255,255,255,0.04); }
  .grid-line-h1 { top: 30%; left: 0; width: 100%; height: 1px; animation: gridFade 3s ease 0.5s forwards; opacity: 0; }
  .grid-line-h2 { top: 70%; left: 0; width: 100%; height: 1px; animation: gridFade 3s ease 0.8s forwards; opacity: 0; }
  .grid-line-v1 { left: 25%; top: 0; width: 1px; height: 100%; animation: gridFade 3s ease 1.1s forwards; opacity: 0; }
  .grid-line-v2 { left: 75%; top: 0; width: 1px; height: 100%; animation: gridFade 3s ease 1.4s forwards; opacity: 0; }

  /* Corner marks */
  .corner-mark {
    position: absolute;
    font-size: 10px;
    color: rgba(192,251,80,0.2);
    opacity: 0;
    animation: fadeIn 1s ease 1.5s forwards;
  }
  .corner-tl { top: 12px; left: 12px; }
  .corner-tr { top: 12px; right: 12px; }
  .corner-bl { bottom: 12px; left: 12px; }
  .corner-br { bottom: 12px; right: 12px; }

  /* Floating musical symbols */
  .music-notes {
    position: absolute;
    top: 0; left: 0;
    width: 100%; height: 100%;
    pointer-events: none;
    overflow: hidden;
    z-index: 1;
  }
  .note {
    position: absolute;
    bottom: -30px;
    font-size: 22px;
    color: rgba(192, 251, 80, 0.4);
    animation: floatUp linear infinite;
    will-change: transform, opacity;
    text-shadow: 0 0 8px rgba(192, 251, 80, 0.2);
  }
  .note:nth-child(odd) {
    font-size: 18px;
    color: rgba(255, 255, 255, 0.25);
  }
  .note:nth-child(3n) {
    font-size: 26px;
    color: rgba(192, 251, 80, 0.35);
    text-shadow: 0 0 12px rgba(192, 251, 80, 0.15);
  }

  @keyframes floatUp {
    0% {
      transform: translateY(0) rotate(0deg) scale(1);
      opacity: 0;
    }
    10% {
      opacity: 1;
    }
    50% {
      transform: translateY(-250px) rotate(15deg) scale(1.1) translateX(20px);
      opacity: 0.8;
    }
    90% {
      opacity: 0.3;
    }
    100% {
      transform: translateY(-550px) rotate(-10deg) scale(0.8) translateX(-15px);
      opacity: 0;
    }
  }

  @keyframes fadeSlideUp {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
  }
  @keyframes titleReveal {
    from { opacity: 0; transform: translateY(40px) scale(0.95); filter: blur(8px); }
    to { opacity: 1; transform: translateY(0) scale(1); filter: blur(0); }
  }
  @keyframes pulse {
    0%, 100% { opacity: 1; box-shadow: 0 0 0 0 rgba(192,251,80,0.4); }
    50% { opacity: 0.6; box-shadow: 0 0 0 6px rgba(192,251,80,0); }
  }
  @keyframes float {
    0%, 100% { transform: translateX(-50%) translateY(0); }
    50% { transform: translateX(-50%) translateY(-6px); }
  }
  @keyframes gridFade {
    from { opacity: 0; }
    to { opacity: 1; }
  }
  @keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
  }
</style>

<script>
(function() {
  const canvas = document.getElementById('particle-canvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  let w, h, particles = [], mouse = {x: -1000, y: -1000};

  function resize() {
    w = canvas.width = canvas.offsetWidth;
    h = canvas.height = canvas.offsetHeight;
  }
  resize();
  window.addEventListener('resize', resize);

  // Create particles
  for (let i = 0; i < 80; i++) {
    particles.push({
      x: Math.random() * w,
      y: Math.random() * h,
      vx: (Math.random() - 0.5) * 0.4,
      vy: (Math.random() - 0.5) * 0.4,
      r: Math.random() * 1.5 + 0.5,
      alpha: Math.random() * 0.3 + 0.05
    });
  }

  canvas.addEventListener('mousemove', e => {
    const rect = canvas.getBoundingClientRect();
    mouse.x = e.clientX - rect.left;
    mouse.y = e.clientY - rect.top;
  });
  canvas.addEventListener('mouseleave', () => { mouse.x = -1000; mouse.y = -1000; });

  function draw() {
    ctx.clearRect(0, 0, w, h);

    for (let i = 0; i < particles.length; i++) {
      const p = particles[i];
      p.x += p.vx;
      p.y += p.vy;
      if (p.x < 0) p.x = w;
      if (p.x > w) p.x = 0;
      if (p.y < 0) p.y = h;
      if (p.y > h) p.y = 0;

      ctx.beginPath();
      ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(192, 251, 80, ${p.alpha})`;
      ctx.fill();

      // Draw connections
      for (let j = i + 1; j < particles.length; j++) {
        const q = particles[j];
        const dx = p.x - q.x, dy = p.y - q.y;
        const dist = Math.sqrt(dx*dx + dy*dy);
        if (dist < 120) {
          ctx.beginPath();
          ctx.moveTo(p.x, p.y);
          ctx.lineTo(q.x, q.y);
          ctx.strokeStyle = `rgba(192, 251, 80, ${0.06 * (1 - dist/120)})`;
          ctx.lineWidth = 0.5;
          ctx.stroke();
        }
      }

      // Mouse interaction
      const mdx = p.x - mouse.x, mdy = p.y - mouse.y;
      const mdist = Math.sqrt(mdx*mdx + mdy*mdy);
      if (mdist < 150) {
        ctx.beginPath();
        ctx.moveTo(p.x, p.y);
        ctx.lineTo(mouse.x, mouse.y);
        ctx.strokeStyle = `rgba(192, 251, 80, ${0.15 * (1 - mdist/150)})`;
        ctx.lineWidth = 0.8;
        ctx.stroke();

        // Push particles away slightly
        p.vx += mdx * 0.0001;
        p.vy += mdy * 0.0001;
      }

      // Dampen velocity
      p.vx *= 0.999;
      p.vy *= 0.999;
    }

    requestAnimationFrame(draw);
  }
  draw();
})();
</script>
"""

# ─────────────────────────────────────────────────────────────────────────────
# Sidebar — Engine config
# ─────────────────────────────────────────────────────────────────────────────
def sidebar() -> dict:
    st.sidebar.markdown("### ⚡ ENGINE CONFIG")

    prov = llm.provider()
    if prov == "gemini":
        st.sidebar.success("GEMINI KEY ACTIVE ✓")
    elif prov == "groq":
        st.sidebar.success("GROQ KEY ACTIVE ✓")
    elif prov == "openrouter":
        st.sidebar.success("OPENROUTER KEY ACTIVE ✓")
    else:
        st.sidebar.warning(
            "NO API KEY — MOCK MODE. Set `GEMINI_API_KEY` in `.env`"
        )
        with st.sidebar.expander("PASTE GEMINI KEY"):
            k = st.text_input("GEMINI_API_KEY", type="password",
                              label_visibility="collapsed")
            if k:
                os.environ["GEMINI_API_KEY"] = k.strip()
                st.rerun()

    ui_prov = prov if prov != "mock" else "gemini"
    model_list = models_for(ui_prov)
    default_model = os.getenv("LLM_MODEL", default_model_for(ui_prov))
    idx = model_list.index(default_model) if default_model in model_list else 0
    model = st.sidebar.selectbox(f"MODEL ({ui_prov.upper()})", model_list, index=idx)
    custom = st.sidebar.text_input("CUSTOM MODEL ID", "")
    if custom.strip():
        model = custom.strip()

    temperature = st.sidebar.slider("CREATIVITY", 0.0, 1.3, 0.9, 0.05)
    use_retrieval = st.sidebar.checkbox(
        "RAG GROUNDING", value=True,
        help="Inject style/theme-relevant snippets from public datasets.",
    )

    st.sidebar.divider()
    st.sidebar.markdown("### 📚 CORPUS STATS")
    stats = corpus_stats()
    st.sidebar.metric("TOTAL SNIPPETS", stats["total"])
    with st.sidebar.expander("BY LANGUAGE"):
        st.write(stats["by_language"])

    return {"model": model, "temperature": temperature,
            "use_retrieval": use_retrieval}


# ─────────────────────────────────────────────────────────────────────────────
# Lyrics result renderer
# ─────────────────────────────────────────────────────────────────────────────
def render_result(res: LyricResult, show_details: bool = True):
    if res.error:
        st.error(f"GENERATION FAILED: {res.error}")
        return

    if res.is_mock:
        st.info("🔧 MOCK OUTPUT — ADD API KEY FOR REAL LYRICS")

    lang = LANGUAGES[res.spec.language]
    st.markdown(
        f'<div style="font-family:Inter,sans-serif;font-weight:800;font-size:1.3rem;'
        f'color:#c0fb50;text-transform:uppercase;letter-spacing:-0.03em;'
        f'margin-bottom:4px">🎵 {res.title}</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        f'<div style="font-family:\'IBM Plex Mono\',monospace;font-size:10px;'
        f'color:rgba(255,255,255,0.4);text-transform:uppercase;margin-bottom:12px;'
        f'padding-bottom:8px;border-bottom:1px solid rgba(255,255,255,0.08)">'
        f'{lang.name} ({lang.native_name}) · {STYLES[res.spec.style]["label"]} · '
        f'{res.spec.emotion} · {RHYME_SCHEMES[res.spec.rhyme_scheme]["label"]} · '
        f'MODEL: {res.model}</div>',
        unsafe_allow_html=True
    )

    # Lyrics body
    st.markdown(
        f'<div style="font-size:0.95rem;line-height:1.9;color:rgba(255,255,255,0.9);'
        f'white-space:pre-wrap;padding:1rem;background:rgba(255,255,255,0.02);'
        f'border:1px solid rgba(255,255,255,0.06);border-radius:4px">'
        f'{res.lyrics}</div>',
        unsafe_allow_html=True
    )

    if res.gloss:
        with st.expander("🌐 ENGLISH GLOSS"):
            st.text(res.gloss)

    # Prosody metrics — custom HTML to avoid truncation in narrow columns
    avg_syll = (
        sum(s.avg_syllables for s in res.stanza_analyses) / len(res.stanza_analyses)
        if res.stanza_analyses else 0
    )
    st.markdown(
        f'''<div style="display:flex;gap:8px;margin:12px 0">
          <div style="flex:1;background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);
                      border-radius:4px;padding:10px;text-align:center">
            <div style="font-family:'IBM Plex Mono',monospace;font-size:10px;text-transform:uppercase;
                        color:rgba(255,255,255,0.5);margin-bottom:4px">RHYME</div>
            <div style="font-family:Inter,sans-serif;font-weight:700;font-size:1.4rem;
                        color:#c0fb50">{res.avg_rhyme_match:.0f}%</div>
          </div>
          <div style="flex:1;background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);
                      border-radius:4px;padding:10px;text-align:center">
            <div style="font-family:'IBM Plex Mono',monospace;font-size:10px;text-transform:uppercase;
                        color:rgba(255,255,255,0.5);margin-bottom:4px">METRE</div>
            <div style="font-family:Inter,sans-serif;font-weight:700;font-size:1.4rem;
                        color:#c0fb50">{res.avg_metre_match:.0f}%</div>
          </div>
          <div style="flex:1;background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);
                      border-radius:4px;padding:10px;text-align:center">
            <div style="font-family:'IBM Plex Mono',monospace;font-size:10px;text-transform:uppercase;
                        color:rgba(255,255,255,0.5);margin-bottom:4px">SYLLABLES</div>
            <div style="font-family:Inter,sans-serif;font-weight:700;font-size:1.4rem;
                        color:#c0fb50">{avg_syll:.1f}</div>
          </div>
        </div>''',
        unsafe_allow_html=True
    )

    if show_details:
        with st.expander("🔎 RHYME & METRE ANALYSIS"):
            for i, an in enumerate(res.stanza_analyses, 1):
                st.write(
                    f"**STANZA {i}** — detected `{an.detected_scheme}` "
                    f"vs target `{an.target_scheme}` · "
                    f"avg {an.avg_syllables} syllables"
                )

        if res.examples:
            with st.expander("📖 GROUNDING SNIPPETS"):
                st.caption("Cultural/idiomatic inspiration — outputs are original.")
                for ex in res.examples:
                    st.markdown(
                        f"- *{ex.text}*  \n  <small>— {ex.source}</small>",
                        unsafe_allow_html=True
                    )

    st.download_button(
        "⬇ DOWNLOAD .TXT",
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


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────
def main():
    cfg = sidebar()

    # ─── Animated Hero Banner ────────────────────────────────────────────
    components.html(HERO_HTML, height=540, scrolling=False)

    # ─── Thin accent divider ─────────────────────────────────────────────
    st.markdown(
        '<div style="width:100%;height:1px;background:linear-gradient(90deg,'
        'transparent,rgba(192,251,80,0.4) 20%,rgba(192,251,80,0.4) 80%,'
        'transparent);margin:0 0 2rem 0"></div>',
        unsafe_allow_html=True
    )

    # ─── Input Controls ──────────────────────────────────────────────────

    # Row 1: Theme + Emotion
    col_theme, col_emotion = st.columns([3, 1])
    with col_theme:
        theme = st.text_input(
            "THEME",
            "first rain after a long summer",
            key="theme_input",
            help="Describe the theme or subject of your song"
        )
    with col_emotion:
        emotion = st.selectbox(
            "EMOTION / MOOD",
            EMOTIONS,
            index=3,
            key="emotion_select",
            format_func=lambda x: x.upper()
        )

    # Row 2: Musical Style + Rhyme Scheme + Metre
    col_style, col_rhyme, col_metre = st.columns(3)
    with col_style:
        style = st.selectbox(
            "MUSICAL STYLE",
            list(STYLES.keys()),
            format_func=lambda s: STYLES[s]["label"].upper(),
            key="style_select"
        )
    with col_rhyme:
        rhyme = st.selectbox(
            "RHYME SCHEME",
            list(RHYME_SCHEMES.keys()),
            format_func=lambda r: RHYME_SCHEMES[r]["label"].upper(),
            key="rhyme_select"
        )
    with col_metre:
        metre = st.selectbox(
            "METRE",
            list(METRES.keys()),
            format_func=lambda m: METRES[m]["label"].upper(),
            key="metre_select"
        )

    # Hint line
    st.caption(
        f"💡 {RHYME_SCHEMES[rhyme]['hint']}  ·  {METRES[metre]['hint']}  ·  "
        f"{STYLES[style]['description']}"
    )

    # Row 3: Verses + Lines/Verse + Chorus + Gloss
    col_v, col_l, col_ch, col_gl = st.columns(4)
    with col_v:
        verses = st.number_input("VERSES", 1, 4, 2, key="verses_input")
    with col_l:
        lpv = st.number_input("LINES / VERSE", 2, 8, 4, key="lpv_input")
    with col_ch:
        chorus = st.checkbox("CHORUS", True, key="chorus_check")
    with col_gl:
        gloss = st.checkbox("ENGLISH GLOSS", True, key="gloss_check",
                           help="Line-by-line English meaning for Indic lyrics.")

    # Row 4: Extra instructions
    extra = st.text_input("EXTRA INSTRUCTIONS (OPTIONAL)", "",
                         key="extra_input")

    st.markdown(
        '<div style="height:1px;background:rgba(255,255,255,0.06);margin:1rem 0"></div>',
        unsafe_allow_html=True
    )

    # ─── Tabs ────────────────────────────────────────────────────────────
    tab_compare, tab_single = st.tabs(
        ["⚡ COMPARE 3 LANGUAGES", "🎤 SINGLE LANGUAGE"]
    )

    # ── Compare Mode ─────────────────────────────────────────────────────
    with tab_compare:
        st.markdown(
            '<div style="font-family:\'IBM Plex Mono\',monospace;font-size:11px;'
            'text-transform:uppercase;letter-spacing:0.08em;'
            'color:rgba(255,255,255,0.35);padding:0.8rem 0">'
            '<span style="display:inline-block;width:6px;height:6px;'
            'border-radius:50%;background:#c0fb50;margin-right:8px;'
            'vertical-align:middle"></span>'
            'SAME THEME · THREE LANGUAGES · SIDE BY SIDE</div>',
            unsafe_allow_html=True
        )

        langs = st.multiselect(
            "LANGUAGES",
            COMPARE_ORDER,
            default=COMPARE_ORDER,
            format_func=lambda l: f"{LANGUAGES[l].name.upper()} ({LANGUAGES[l].native_name})",
            key="compare_langs"
        )

        if st.button("⚡ GENERATE IN ALL LANGUAGES", type="primary",
                     key="gen_cmp"):
            if not theme.strip():
                st.warning("⚠ ENTER A THEME FIRST")
            elif not langs:
                st.warning("⚠ SELECT AT LEAST ONE LANGUAGE")
            else:
                inp = dict(theme=theme, emotion=emotion, style=style,
                          rhyme_scheme=rhyme, metre=metre,
                          num_verses=int(verses), lines_per_verse=int(lpv),
                          include_chorus=chorus, include_gloss=gloss,
                          extra_instructions=extra)
                base = GenSpec(language=langs[0], **inp)
                with st.spinner("COMPOSING ACROSS LANGUAGES…"):
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

    # ── Single Mode ──────────────────────────────────────────────────────
    with tab_single:
        st.markdown(
            '<div style="font-family:\'IBM Plex Mono\',monospace;font-size:11px;'
            'text-transform:uppercase;letter-spacing:0.08em;'
            'color:rgba(255,255,255,0.35);padding:0.8rem 0">'
            '<span style="display:inline-block;width:6px;height:6px;'
            'border-radius:50%;background:#c0fb50;margin-right:8px;'
            'vertical-align:middle"></span>'
            'GENERATE & FINE-TUNE ONE LANGUAGE</div>',
            unsafe_allow_html=True
        )

        language = st.selectbox(
            "LANGUAGE",
            list(LANGUAGES.keys()),
            format_func=lambda l: f"{LANGUAGES[l].name.upper()} ({LANGUAGES[l].native_name})",
            key="single_lang",
        )

        if st.button("⚡ GENERATE", type="primary", key="gen_single"):
            if not theme.strip():
                st.warning("⚠ ENTER A THEME FIRST")
            else:
                inp = dict(theme=theme, emotion=emotion, style=style,
                          rhyme_scheme=rhyme, metre=metre,
                          num_verses=int(verses), lines_per_verse=int(lpv),
                          include_chorus=chorus, include_gloss=gloss,
                          extra_instructions=extra)
                spec = GenSpec(language=language, **inp)
                with st.spinner("COMPOSING…"):
                    res = generate_one(
                        spec, model=cfg["model"],
                        temperature=cfg["temperature"],
                        use_retrieval=cfg["use_retrieval"],
                    )
                st.session_state["single_result"] = res

        res = st.session_state.get("single_result")
        if res:
            render_result(res, show_details=True)

    # ─── Footer ──────────────────────────────────────────────────────────
    st.markdown(
        '<div style="height:1px;background:rgba(255,255,255,0.06);'
        'margin:3rem 0 1rem 0"></div>',
        unsafe_allow_html=True
    )
    st.caption(
        "BUILT FOR PS-C2 · LLM: GEMINI (FREE) / OPENROUTER · "
        "RAG: AI4BHARAT/SANGRAHA + HUGGINGARTISTS + KAGGLE HINDI LYRICS · "
        "PROSODY ANALYSIS: HEURISTIC (AKSHARA-BASED FOR INDIC)"
    )


if __name__ == "__main__":
    main()
