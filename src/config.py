"""Central configuration: languages, styles, rhyme schemes, metres and the
cultural-context knowledge base that makes generations linguistically faithful.

Keeping all of this declarative (plain dicts) means the UI, prompt builder and
analysis modules read from a single source of truth.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

# --------------------------------------------------------------------------- #
# Paths
# --------------------------------------------------------------------------- #
ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
CORPUS_DIR = DATA_DIR / "corpus"
SAMPLES_DIR = DATA_DIR / "samples"

# --------------------------------------------------------------------------- #
# Languages
# --------------------------------------------------------------------------- #
@dataclass(frozen=True)
class Language:
    code: str           # internal key
    name: str           # English name
    native_name: str    # endonym
    script: str         # script family used by the analysis module
    iso: str            # ISO 639 code (handy for IndicTrans / datasets)


LANGUAGES: dict[str, Language] = {
    "kannada": Language("kannada", "Kannada", "ಕನ್ನಡ", "kannada", "kn"),
    "hindi": Language("hindi", "Hindi", "हिन्दी", "devanagari", "hi"),
    "english": Language("english", "English", "English", "latin", "en"),
}

# Order used for the 3-language comparison demo.
COMPARE_ORDER = ["kannada", "hindi", "english"]

# --------------------------------------------------------------------------- #
# Musical styles
# --------------------------------------------------------------------------- #
STYLES: dict[str, dict] = {
    "folk": {
        "label": "Folk",
        "description": (
            "Rooted, communal, oral-tradition feel. Simple, repetitive, "
            "singable lines; nature and everyday imagery; call-and-response."
        ),
    },
    "pop": {
        "label": "Pop",
        "description": (
            "Catchy, contemporary, radio-friendly. Strong hook/chorus, "
            "verse-chorus structure, accessible language, emotional punch."
        ),
    },
    "classical": {
        "label": "Classical",
        "description": (
            "Refined, literary, devotional or romantic. Rich metaphor, "
            "elevated diction, slower contemplative cadence."
        ),
    },
    "rap": {
        "label": "Rap / Hip-hop",
        "description": (
            "Rhythmic, dense internal rhyme, wordplay, attitude and social "
            "commentary; conversational flow with punchlines."
        ),
    },
}

# --------------------------------------------------------------------------- #
# Rhyme schemes
# --------------------------------------------------------------------------- #
RHYME_SCHEMES: dict[str, dict] = {
    "AABB": {"label": "AABB (couplets)", "pattern": "AABB",
             "hint": "Lines rhyme in pairs — common in folk & nursery-like songs."},
    "ABAB": {"label": "ABAB (alternating)", "pattern": "ABAB",
             "hint": "Alternating rhyme — typical of pop verses."},
    "ABCB": {"label": "ABCB (ballad)", "pattern": "ABCB",
             "hint": "Only 2nd & 4th lines rhyme — classic ballad/storytelling feel."},
    "AAAA": {"label": "AAAA (monorhyme)", "pattern": "AAAA",
             "hint": "Every line rhymes — punchy, used in rap & qawwali-like forms."},
    "free": {"label": "Free verse", "pattern": "FREE",
             "hint": "No fixed end-rhyme; rhythm carries the line."},
}

# --------------------------------------------------------------------------- #
# Metre presets (syllables/aksharas per line are *targets*, not hard limits)
# --------------------------------------------------------------------------- #
METRES: dict[str, dict] = {
    "short": {"label": "Short (~6 syllables)", "syllables": 6,
              "hint": "Light, fast, folk-like lines."},
    "medium": {"label": "Medium (~9 syllables)", "syllables": 9,
               "hint": "Balanced pop/ballad line length."},
    "long": {"label": "Long (~12 syllables)", "syllables": 12,
             "hint": "Flowing, classical / ghazal-like lines."},
    "free": {"label": "Free metre", "syllables": 0,
             "hint": "No syllable target — natural phrasing."},
}

EMOTIONS = [
    "joyful", "melancholic", "romantic", "hopeful", "nostalgic",
    "defiant", "devotional", "playful", "heartbroken", "triumphant",
]

# --------------------------------------------------------------------------- #
# Cultural-context knowledge base
# --------------------------------------------------------------------------- #
# This is the heart of "Cultural Context". For each language we give the model
# (a) general linguistic guidance and (b) per-style traditions, idioms, imagery
# and forms to honour. Kept concise so it fits comfortably in the prompt.
# --------------------------------------------------------------------------- #
CULTURAL_CONTEXT: dict[str, dict] = {
    "kannada": {
        "general": (
            "Write in natural, idiomatic Kannada as a native lyricist would. "
            "Prefer everyday Kannada words over heavy Sanskritisation unless the "
            "classical style calls for it. Use authentic imagery from Karnataka: "
            "the Western Ghats (ಮಲೆನಾಡು), Kaveri/Tunga rivers, paddy fields, "
            "jasmine (ಮಲ್ಲಿಗೆ), monsoon, and rural life. Honour Kannada poetic "
            "sensibility (ಭಾವ / bhāva)."
        ),
        "styles": {
            "folk": (
                "Janapada (ಜನಪದ) folk tradition — Sobane/Lavani/Gee Gee Pada, "
                "harvest and work songs, lullabies (ಜೋಗುಳ). Simple repeated "
                "refrains, call-and-response, earthy rural imagery."
            ),
            "pop": (
                "Modern Sandalwood / indie-Kannada pop sensibility. Catchy hook, "
                "code-mixing with a little English is acceptable, youthful and "
                "urban Bengaluru imagery alongside emotion."
            ),
            "classical": (
                "Draw on Dasa Sahitya (Purandaradasa, Kanakadasa) and Vachana "
                "(Basavanna) traditions, devotional bhakti or refined romance, "
                "Carnatic-raga lyricism, elevated but musical diction."
            ),
            "rap": (
                "Contemporary Kannada hip-hop (Bengaluru rap scene). Punchy, "
                "rhythmic, code-mixed Kannada-English flow, local slang, "
                "attitude and social/everyday commentary."
            ),
        },
    },
    "hindi": {
        "general": (
            "Write in natural, singable Hindi as a film/indie lyricist would. "
            "A tasteful Hindi-Urdu blend (Hindustani) is authentic and welcome. "
            "Use evocative imagery: monsoon (सावन), the moon (चाँद), "
            "longing (इंतज़ार), the heart (दिल). Keep it emotionally direct."
        ),
        "styles": {
            "folk": (
                "Loka-geet / folk traditions — bhajan, wedding & festival songs "
                "(Holi, Teej), regional flavours. Simple refrains, devotional or "
                "celebratory warmth, repetition."
            ),
            "pop": (
                "Bollywood / indie-pop filmi sensibility. Strong mukhda (hook) "
                "and antara (verse) structure, romantic and contemporary, "
                "radio-friendly phrasing."
            ),
            "classical": (
                "Ghazal / nazm / thumri tradition with refined Urdu-Hindi "
                "diction. Use the matla/maqta and radif-qaafiya feel of ghazal, "
                "rich metaphor, shayari elegance."
            ),
            "rap": (
                "Indian hip-hop (Gully Boy / desi hip-hop). Dense rhyme, "
                "street imagery, code-mixing, social commentary, swagger and flow."
            ),
        },
    },
    "english": {
        "general": (
            "Write in natural, contemporary English with strong, concrete "
            "imagery and a clear emotional through-line. Avoid clichés; favour "
            "fresh, specific detail and a memorable hook."
        ),
        "styles": {
            "folk": (
                "Singer-songwriter / Americana-folk storytelling. Narrative "
                "verses, plainspoken warmth, nature and home imagery, a "
                "repeatable refrain."
            ),
            "pop": (
                "Modern pop craft — instantly memorable chorus/hook, "
                "verse-pre-chorus-chorus structure, universal emotion, "
                "conversational lines."
            ),
            "classical": (
                "Lyrical, poetic register drawing on art-song / hymn tradition. "
                "Elevated but sincere diction, sustained metaphor, measured cadence."
            ),
            "rap": (
                "Hip-hop craft — multisyllabic and internal rhyme, wordplay, "
                "rhythmic pocket, punchlines, voice and perspective."
            ),
        },
    },
}

# --------------------------------------------------------------------------- #
# Generation defaults
# --------------------------------------------------------------------------- #
@dataclass
class GenSpec:
    """A fully-specified generation request for one language."""
    language: str
    theme: str
    emotion: str
    style: str
    rhyme_scheme: str = "AABB"
    metre: str = "medium"
    num_verses: int = 2
    lines_per_verse: int = 4
    include_chorus: bool = True
    include_gloss: bool = True          # add an English gloss for Indic outputs
    extra_instructions: str = ""
    retrieved_examples: list[str] = field(default_factory=list)


# --------------------------------------------------------------------------- #
# LLM providers & models (NO paid OpenAI anywhere)
# --------------------------------------------------------------------------- #
GEMINI_MODELS = [
    "gemini-2.0-flash",          # fast, free, strong multilingual (default)
    "gemini-2.0-flash-lite",
    "gemini-1.5-flash",
    "gemini-1.5-flash-8b",
    "gemini-1.5-pro",
]
DEFAULT_GEMINI_MODEL = "gemini-2.0-flash"

GROQ_MODELS = [
    "qwen/qwen3-32b",                       # strong multilingual, good Indic support
    "llama-3.3-70b-versatile",               # large, good English
    "meta-llama/llama-4-scout-17b-16e-instruct",  # Llama 4 Scout
    "llama-3.1-8b-instant",                  # fast, lightweight
    "openai/gpt-oss-120b",                   # GPT open-source 120B
    "openai/gpt-oss-20b",                    # GPT open-source 20B
]
DEFAULT_GROQ_MODEL = "qwen/qwen3-32b"

OPENROUTER_MODELS = [
    "google/gemini-2.0-flash-exp:free",
    "meta-llama/llama-3.3-70b-instruct:free",
    "qwen/qwen-2.5-72b-instruct:free",
    "deepseek/deepseek-chat-v3-0324:free",
    "mistralai/mistral-small-3.1-24b-instruct:free",
]
DEFAULT_OPENROUTER_MODEL = OPENROUTER_MODELS[0]


def models_for(provider: str) -> list[str]:
    if provider == "gemini":
        return GEMINI_MODELS
    if provider == "groq":
        return GROQ_MODELS
    return OPENROUTER_MODELS


def default_model_for(provider: str) -> str:
    if provider == "gemini":
        return DEFAULT_GEMINI_MODEL
    if provider == "groq":
        return DEFAULT_GROQ_MODEL
    return DEFAULT_OPENROUTER_MODEL


# Backwards-compatible aliases.
RECOMMENDED_MODELS = GEMINI_MODELS
DEFAULT_MODEL = DEFAULT_GEMINI_MODEL

