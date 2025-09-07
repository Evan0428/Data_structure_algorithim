from __future__ import annotations

import re
from typing import List


_URL_PATTERN = re.compile(r"https?://\S+")
_NON_ALNUM = re.compile(r"[^a-z0-9\s]")


def normalize_text(text: str) -> str:
    """Lowercase, strip URLs/punctuation, collapse whitespace.

    Keeps it simple for classic ML features. Avoids heavy tokenization libs.
    """
    text = text.lower()
    text = _URL_PATTERN.sub(" ", text)
    text = _NON_ALNUM.sub(" ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def normalize_corpus(texts: List[str]) -> List[str]:
    return [normalize_text(t) for t in texts]

