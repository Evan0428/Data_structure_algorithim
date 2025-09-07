from __future__ import annotations

import re
from typing import Optional, List


_ORDER_ID_PATTERNS = [
    re.compile(r"\b(?:ord|order)[-\s:]*(?:id)?[-\s:]*(?:#)?([a-z0-9-]{6,})\b", re.I),
    re.compile(r"\b([A-Z]{2,3}\d{6,})\b"),
]


def extract_order_id(text: str) -> Optional[str]:
    for pat in _ORDER_ID_PATTERNS:
        m = pat.search(text)
        if m:
            return m.group(1)
    return None


def extract_search_keywords(text: str, max_terms: int = 6) -> List[str]:
    # naive keyword split; real systems would use POS tagging
    text = re.sub(r"[^a-zA-Z0-9\s]", " ", text).lower()
    tokens = [t for t in text.split() if len(t) > 2]
    stop = {
        "show",
        "find",
        "need",
        "have",
        "with",
        "for",
        "the",
        "and",
        "you",
        "your",
        "please",
        "looking",
        "search",
        "product",
        "products",
    }
    keywords = [t for t in tokens if t not in stop]
    return keywords[:max_terms]

