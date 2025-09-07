from __future__ import annotations

from typing import Dict, Any


def format_classification_report(report: Dict[str, Any]) -> str:
    lines = ["label,precision,recall,f1,support"]
    for label, stats in report.items():
        if label in {"accuracy", "macro avg", "weighted avg"}:
            continue
        lines.append(
            f"{label},{stats['precision']:.3f},{stats['recall']:.3f},{stats['f1-score']:.3f},{stats['support']}"
        )
    return "\n".join(lines)

