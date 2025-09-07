from __future__ import annotations

from pathlib import Path
from typing import Any, Dict
import json


def read_json(path: str | Path) -> Dict[str, Any]:
    return json.loads(Path(path).read_text())


def read_csv(path: str | Path) -> str:
    return Path(path).read_text()

