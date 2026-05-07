
import re

REVERSE_LEET_MAP = {
    "4": "a",
    "3": "e",
    "1": "i",
    "0": "o",
    "$": "s",
    "7": "t",
    "@": "a"
}


def normalize_text(text):
    text = str(text).lower()

    for src, tgt in REVERSE_LEET_MAP.items():
        text = text.replace(src, tgt)

    text = re.sub(r"(.)\1{2,}", r"\1\1", text)

    spaced_patterns = {
        r"\bi\s+d\s+i\s+o\s+t\b": "idiot",
        r"\bs\s+t\s+u\s+p\s+i\s+d\b": "stupid",
        r"\bm\s+o\s+r\s+o\s+n\b": "moron",
        r"\bf\s+u\s+c\s+k\b": "fuck",
        r"\bb\s+i\s+t\s+c\s+h\b": "bitch",
        r"\bk\s+i\s+l\s+l\b": "kill",

        r"\bi\s+h\s+a\s+t\s+e\s+y\s+o\s+u\b": "i hate you",
        r"\bh\s+a\s+t\s+e\s+y\s+o\s+u\b": "hate you",
        r"\bh\s+a\s+t\s+e\b": "hate",
        r"\by\s+o\s+u\b": "you",

        r"\bihateyou\b": "i hate you",
        r"\bhateyou\b": "hate you"
    }

    for pattern, replacement in spaced_patterns.items():
        text = re.sub(pattern, replacement, text)

    text = re.sub(r"\s+", " ", text).strip()

    return text
