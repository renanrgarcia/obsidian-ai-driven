import re


def normalize_text(text: str) -> str:
    return " ".join(text.split()).strip()


def normalize_habit_label(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()
