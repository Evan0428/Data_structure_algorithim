from __future__ import annotations

from dataclasses import dataclass
from typing import List, Dict, Any
from pathlib import Path
import csv
import math
from collections import Counter, defaultdict

from ..nlu.preprocess import normalize_corpus


@dataclass
class Product:
    product_id: str
    title: str
    category: str
    brand: str
    price: float
    description: str


class ProductSearchEngine:
    def __init__(self, catalog_csv_path: str | Path) -> None:
        self.products: List[Dict[str, Any]] = []
        with open(catalog_csv_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                row["price"] = float(row.get("price", 0) or 0)
                self.products.append(row)

        docs = [
            f"{p.get('title','')} {p.get('description','')} {p.get('category','')} {p.get('brand','')}"
            for p in self.products
        ]
        self.norm_docs = normalize_corpus(docs)
        self.doc_term_counts: List[Counter[str]] = [Counter(d.split()) for d in self.norm_docs]
        self.df: Counter[str] = Counter()
        for counts in self.doc_term_counts:
            for term in counts.keys():
                self.df[term] += 1
        self.N = len(self.products)

    def _tfidf_vector(self, terms: Counter[str]) -> Dict[str, float]:
        vec: Dict[str, float] = {}
        for term, tf in terms.items():
            idf = math.log((1 + self.N) / (1 + self.df.get(term, 0))) + 1.0
            vec[term] = tf * idf
        return vec

    @staticmethod
    def _cosine(a: Dict[str, float], b: Dict[str, float]) -> float:
        if not a or not b:
            return 0.0
        dot = 0.0
        for t, va in a.items():
            vb = b.get(t)
            if vb is not None:
                dot += va * vb
        na = math.sqrt(sum(v * v for v in a.values()))
        nb = math.sqrt(sum(v * v for v in b.values()))
        if na == 0.0 or nb == 0.0:
            return 0.0
        return dot / (na * nb)

    def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        if not query.strip():
            return []
        q_norm = normalize_corpus([query])[0]
        q_counts = Counter(q_norm.split())
        q_vec = self._tfidf_vector(q_counts)

        scores: List[float] = []
        doc_vecs = [self._tfidf_vector(c) for c in self.doc_term_counts]
        for dv in doc_vecs:
            scores.append(self._cosine(q_vec, dv))

        ranked = sorted(enumerate(scores), key=lambda kv: kv[1], reverse=True)[:top_k]
        results: List[Dict[str, Any]] = []
        for idx, s in ranked:
            p = self.products[idx]
            results.append(
                {
                    "product_id": p.get("product_id", ""),
                    "title": p.get("title", ""),
                    "category": p.get("category", ""),
                    "brand": p.get("brand", ""),
                    "price": float(p.get("price", 0.0)),
                    "score": float(s),
                }
            )
        return results

