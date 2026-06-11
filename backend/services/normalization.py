import re

URDU_MAP = {
    "محمد": "muhammad",
    "احمد": "ahmed",
    "علی": "ali",
    "خان": "khan",
    "رضا": "raza",
    "بیگ": "baig",
}


def normalize_text(text):
    if not text:
        return ""

    text = text.strip().lower()

    for urdu, english in URDU_MAP.items():
        text = text.replace(urdu, english)

    text = re.sub(r"\s+", " ", text)

    return text