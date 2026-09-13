"""Prompt construction: turns a GenSpec + retrieved real examples into the
system/user messages sent to the LLM.

Design goals:
* Bake in *cultural context* (language + style traditions, imagery, idioms).
* State the structural constraints (rhyme scheme, metre, verses, chorus) clearly.
* Use retrieved real lyric snippets as *inspiration only* — never to copy — to
  keep outputs original (a hackathon rule) while staying culturally grounded.
* Force a parseable output so the app can split sections and add an English gloss.
"""

from __future__ import annotations

from .config import (
    CULTURAL_CONTEXT,
    GenSpec,
    LANGUAGES,
    METRES,
    RHYME_SCHEMES,
    STYLES,
)

SYSTEM_PROMPT = (
    "You are a master multilingual songwriter. You output ONLY lyrics — no "
    "thinking, no planning, no commentary, no explanations. Your output is "
    "ALWAYS in this exact format:\n\n"
    "TITLE: <title>\n\n"
    "[Verse 1]\n<lyrics lines>\n\n"
    "[Chorus]\n<lyrics lines>\n\n"
    "[Verse 2]\n<lyrics lines>\n\n"
    "(optionally) [English Gloss]\n<gloss lines>\n\n"
    "RULES:\n"
    "- Output ONLY the title line and lyrics. Nothing else. No meta-text.\n"
    "- Do NOT write planning notes, structure descriptions, or English "
    "annotations inside lyrics (e.g. NO '(Unique opening...)' or "
    "'(Chorus that is...)').\n"
    "- If writing in Kannada or Hindi, ALL lyrics must be in that script. "
    "Do NOT mix English planning text into Indic lyrics.\n"
    "- Write ORIGINAL lyrics. Never translate word-for-word across languages; "
    "re-imagine the theme natively in each language's own idiom.\n"
    "- Every song must start with a UNIQUE opening line.\n"
    "- Be creative with imagery. No generic fillers or stock phrases.\n"
    "- Honour the requested rhyme scheme, metre, and structure."
)


def _rhyme_instruction(spec: GenSpec) -> str:
    rs = RHYME_SCHEMES.get(spec.rhyme_scheme, RHYME_SCHEMES["free"])
    if rs["pattern"] == "FREE":
        return "Rhyme: free verse — no fixed end-rhyme, let rhythm carry the lines."
    return (
        f"Rhyme scheme: {rs['pattern']} per stanza "
        f"(lines marked with the same letter must rhyme at the line end). "
        f"{rs['hint']}"
    )


def _metre_instruction(spec: GenSpec) -> str:
    m = METRES.get(spec.metre, METRES["free"])
    if not m["syllables"]:
        return "Metre: free — natural phrasing, roughly even line lengths."
    base = m["syllables"]
    # Indic aksharas are denser — scale target up for natural line lengths
    if spec.language in ("kannada", "hindi"):
        target = int(base * 1.6)  # 6→10, 9→14, 12→19
        return (
            f"Metre: aim for about {target} aksharas per line "
            f"(±2 is fine). Count each consonant-vowel unit as one akshara. "
            f"Keep lines consistent so they sing to a steady beat."
        )
    return (
        f"Metre: aim for about {base} syllables per line "
        f"(±1 is fine). Keep lines consistent so they sing to a steady beat."
    )


def _examples_block(spec: GenSpec) -> str:
    if not spec.retrieved_examples:
        return ""
    lines = "\n".join(f"  • {ex}" for ex in spec.retrieved_examples)
    return (
        "\nReal reference snippets of authentic text in this language (drawn from "
        "public datasets — for natural idiom, vocabulary and FLAVOUR ONLY; do NOT "
        "copy or translate these, write something entirely new):\n" + lines + "\n"
    )


def build_messages(spec: GenSpec) -> list[dict]:
    lang = LANGUAGES[spec.language]
    style = STYLES.get(spec.style, STYLES["pop"])
    ctx = CULTURAL_CONTEXT[spec.language]
    style_ctx = ctx["styles"].get(spec.style, "")

    structure_bits = [
        f"Write {spec.num_verses} verse(s), {spec.lines_per_verse} lines each.",
    ]
    if spec.include_chorus:
        structure_bits.append(
            "Include a CHORUS (hook) that repeats; place it between verses."
        )

    gloss_bits = ""
    if spec.include_gloss and spec.language != "english":
        gloss_bits = (
            "\nAfter the lyrics, add a section titled exactly '[English Gloss]' "
            "with a plain line-by-line English meaning (not a singable "
            "translation) so non-speakers can follow along."
        )

    user = f"""Write original {lang.name} ({lang.native_name}) song lyrics.

THEME (understand this carefully — preserve all names, references, and context exactly):
"{spec.theme}"
Interpret this theme faithfully. If it contains proper nouns (names of people, teams, places, brands), keep them AS-IS in the lyrics — do NOT translate, substitute, or generalize them. Understand the FULL meaning and sentiment behind the theme before writing.

EMOTION / MOOD: {spec.emotion}
MUSICAL STYLE: {style['label']} — {style['description']}

CULTURAL CONTEXT (honour this carefully):
- Language voice: {ctx['general']}
- Style tradition: {style_ctx}

STRUCTURE:
- {' '.join(structure_bits)}
- {_rhyme_instruction(spec)}
- {_metre_instruction(spec)}
{_examples_block(spec)}
CRITICAL QUALITY RULES:
1. THEME FIDELITY: The lyrics MUST be specifically about "{spec.theme}" — not a vague interpretation. Use concrete details, names, and imagery from the theme.
2. UNIQUE OPENING: Start with a creative, unique first line that immediately connects to this specific theme. Never use a generic or formulaic opening.
3. VARIETY: Each verse and chorus must use different vocabulary and imagery. Do NOT repeat the same words or phrases across verses.
4. NATURAL {lang.name.upper()}: Write as a native {lang.name} speaker would — use natural idiom, colloquial expressions, and culturally authentic imagery. The lyrics should feel native, not translated.
5. SINGABILITY: Lines must flow musically. Read them aloud — they should have rhythm and melody.
6. NO FILLER: Every line must carry meaning. No padding lines, no empty repetition just to fill space.

OUTPUT FORMAT (follow EXACTLY — any deviation will be rejected):
- Your response must start with: TITLE: <a short evocative title in {lang.name}>
- Then the lyrics with section headers: [Verse 1], [Chorus], [Verse 2], etc.
- Write ALL lyrics in {lang.name} script. Every line of lyrics must be in {lang.name}.
- Do NOT include ANY of the following in your output:
  * Planning notes (e.g. "I'll start with...", "Let me craft...")
  * Structure annotations (e.g. "(Unique opening connecting to...)")
  * English descriptions inside non-English lyrics
  * Commentary before or after lyrics
- Output ONLY: TITLE line + lyrics sections{(' + [English Gloss] section') if gloss_bits else ''}.{gloss_bits}
{('Extra instructions: ' + spec.extra_instructions) if spec.extra_instructions else ''}"""

    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user.strip()},
    ]

