import re

SUPERSCRIPT_TRANSLATION = str.maketrans({
    "¹": "1",
    "²": "2",
    "³": "3",
})


def normalize_text(text: str) -> str:
    return " ".join(text.split()).strip()


def normalize_habit_label(text: str) -> str:
    normalized = text.lower().translate(SUPERSCRIPT_TRANSLATION)
    return re.sub(r"[^a-z0-9]+", " ", normalized).strip()
