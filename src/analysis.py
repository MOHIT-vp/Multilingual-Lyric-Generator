"""Prosody analysis: syllable/akshara counting, rhyme detection and scoring.

This module lets us *verify* that generated lyrics actually honour the requested
rhyme scheme and metre, rather than just asking the model to do so. It works
across Latin (English), Devanagari (Hindi) and Kannada scripts.

The Indic syllable counter uses an "akshara" heuristic:
    syllables ≈ (independent vowels) + (consonants NOT followed by a virama)
A consonant followed by a virama (halant) joins the next consonant into a
conjunct (one akshara); vowel signs (matras) attach to a consonant and add no
new akshara. This is a well-known, dependency-free approximation that is more
than accurate enough for metre feedback.
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, field

# --------------------------------------------------------------------------- #
# Unicode ranges per script
# --------------------------------------------------------------------------- #
_SCRIPTS = {
    "devanagari": {
        "ind_vowels": (0x0904, 0x0914),   # independent vowels अ..औ
        "consonants": [(0x0915, 0x0939), (0x0958, 0x095F)],
        "matras": (0x093A, 0x094C),       # dependent vowel signs
        "virama": 0x094D,
    },
    "kannada": {
        "ind_vowels": (0x0C85, 0x0C94),   # ಅ..ಔ
        "consonants": [(0x0C95, 0x0CB9)],
        "matras": (0x0CBE, 0x0CCC),
        "virama": 0x0CCD,
    },
}


def _in_ranges(cp: int, ranges) -> bool:
    if isinstance(ranges, tuple):
        ranges = [ranges]
    return any(lo <= cp <= hi for lo, hi in ranges)


# --------------------------------------------------------------------------- #
# Syllable counting
# --------------------------------------------------------------------------- #
def _count_syllables_latin(word: str) -> int:
    """Classic heuristic English syllable counter (vowel-group based)."""
    word = word.lower()
    word = re.sub(r"[^a-z]", "", word)
    if not word:
        return 0
    groups = re.findall(r"[aeiouy]+", word)
    count = len(groups)
    # Silent trailing 'e' (but not 'le' after a consonant, e.g. "table").
    if word.endswith("e") and not word.endswith(("le", "ye", "ee")) and count > 1:
        count -= 1
    return max(1, count)


def _count_aksharas(text: str, script: str) -> int:
    s = _SCRIPTS[script]
    chars = list(text)
    n = len(chars)
    count = 0
    for i, ch in enumerate(chars):
        cp = ord(ch)
        if _in_ranges(cp, s["ind_vowels"]):
            count += 1
        elif _in_ranges(cp, s["consonants"]):
            nxt = ord(chars[i + 1]) if i + 1 < n else None
            if nxt != s["virama"]:
                count += 1
    return count


def count_syllables(text: str, script: str) -> int:
    """Approximate syllable/akshara count for a line of lyrics."""
    if not text or not text.strip():
        return 0
    if script in ("kannada", "devanagari"):
        return _count_aksharas(text, script)
    # Latin / default
    return sum(_count_syllables_latin(w) for w in re.findall(r"[A-Za-z']+", text))


# --------------------------------------------------------------------------- #
# Rhyme detection
# --------------------------------------------------------------------------- #
_PUNCT = "।॥.,!?;:\"'`()[]{}—–-…"


def _last_token(line: str) -> str:
    line = line.strip().strip(_PUNCT).strip()
    if not line:
        return ""
    return line.split()[-1].strip(_PUNCT)


def _rhyme_key_latin(word: str) -> str:
    """Approx rhyme = from the last stressed vowel to the end (simplified to the
    final vowel group + trailing consonants)."""
    w = re.sub(r"[^a-z]", "", word.lower())
    if not w:
        return ""
    m = list(re.finditer(r"[aeiouy]+", w))
    if not m:
        return w[-2:]
    start = m[-1].start()
    return w[start:]


def _rhyme_key_indic(word: str, script: str) -> str:
    """Approx Indic rhyme = the trailing rhyming unit: the last vowel sound plus
    everything after it. We take the last independent vowel or matra position to
    the end; fall back to the final two characters."""
    s = _SCRIPTS[script]
    chars = list(word)
    last_vowel_idx = -1
    for i, ch in enumerate(chars):
        cp = ord(ch)
        if _in_ranges(cp, s["ind_vowels"]) or _in_ranges(cp, s["matras"]):
            last_vowel_idx = i
    if last_vowel_idx == -1:
        return word[-2:]
    return "".join(chars[last_vowel_idx:])


def rhyme_key(line: str, script: str) -> str:
    """A normalised string that two rhyming lines should share."""
    word = _last_token(line)
    if not word:
        return ""
    word = unicodedata.normalize("NFC", word)
    if script in ("kannada", "devanagari"):
        return _rhyme_key_indic(word, script)
    return _rhyme_key_latin(word)


def detect_scheme(lines: list[str], script: str) -> str:
    """Assign rhyme letters (A, B, C…) to non-empty lines by matching keys."""
    keys = [rhyme_key(ln, script) for ln in lines]
    labels: list[str] = []
    seen: dict[str, str] = {}
    next_ord = ord("A")
    for k in keys:
        if not k:
            labels.append("-")
            continue
        # Fuzzy match: share the key, or one key is a suffix of the other.
        matched = None
        for prev_key, lab in seen.items():
            if k == prev_key or k.endswith(prev_key) or prev_key.endswith(k):
                matched = lab
                break
        if matched:
            labels.append(matched)
        else:
            lab = chr(next_ord)
            next_ord += 1
            seen[k] = lab
            labels.append(lab)
    return "".join(labels)


# --------------------------------------------------------------------------- #
# Scoring
# --------------------------------------------------------------------------- #
@dataclass
class LineAnalysis:
    text: str
    syllables: int
    rhyme_label: str


@dataclass
class StanzaAnalysis:
    lines: list[LineAnalysis] = field(default_factory=list)
    detected_scheme: str = ""
    target_scheme: str = ""
    target_syllables: int = 0
    rhyme_match_pct: float = 0.0
    metre_match_pct: float = 0.0

    @property
    def avg_syllables(self) -> float:
        vals = [l.syllables for l in self.lines if l.syllables]
        return round(sum(vals) / len(vals), 1) if vals else 0.0


def _scheme_match(detected: str, target: str) -> float:
    """How well the detected rhyme *pattern* matches the target pattern.

    Compares the equivalence structure (which lines rhyme with which) rather than
    the literal letters, so AABB matches CCDD. 'free' always scores 100%.
    """
    if target.upper() in ("FREE", ""):
        return 100.0
    d = detected[: len(target)]
    if len(d) < 2:
        return 0.0

    def pairs(seq):
        out = set()
        for i in range(len(seq)):
            for j in range(i + 1, len(seq)):
                if seq[i] != "-" and seq[j] != "-":
                    out.add((i, j, seq[i] == seq[j]))
        return out

    tp, dp = pairs(target), pairs(d)
    if not tp:
        return 100.0
    agree = sum(
        1 for (i, j, same) in tp
        if (i, j, same) in dp
    )
    return round(100.0 * agree / len(tp), 1)


def analyze_stanza(
    lines: list[str],
    script: str,
    target_scheme: str = "FREE",
    target_syllables: int = 0,
) -> StanzaAnalysis:
    clean = [ln for ln in lines if ln.strip()]
    detected = detect_scheme(clean, script)
    line_objs = [
        LineAnalysis(ln, count_syllables(ln, script), lab)
        for ln, lab in zip(clean, detected)
    ]
    st = StanzaAnalysis(
        lines=line_objs,
        detected_scheme=detected,
        target_scheme=target_scheme,
        target_syllables=target_syllables,
    )
    st.rhyme_match_pct = _scheme_match(detected, target_scheme)
    if target_syllables and line_objs:
        # within ±3 syllables/aksharas counts as "on metre"
        # (±3 tolerance because akshara counting is approximate for Indic,
        #  and even English syllable counting is heuristic)
        ok = sum(1 for l in line_objs if abs(l.syllables - target_syllables) <= 3)
        st.metre_match_pct = round(100.0 * ok / len(line_objs), 1)
    else:
        st.metre_match_pct = 100.0
    return st


def split_stanzas(text: str) -> list[list[str]]:
    """Split a lyric block into stanzas (blank-line separated) of lines.

    Section headers like [Chorus] / (Verse 1) are kept out of prosody analysis.
    """
    stanzas: list[list[str]] = []
    current: list[str] = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            if current:
                stanzas.append(current)
                current = []
            continue
        if re.fullmatch(r"[\[\(].*[\]\)]", line):  # section header
            if current:
                stanzas.append(current)
                current = []
            continue
        current.append(line)
    if current:
        stanzas.append(current)
    return stanzas
