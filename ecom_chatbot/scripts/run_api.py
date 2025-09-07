from __future__ import annotations

from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

import uvicorn  # type: ignore


def main() -> None:
    uvicorn.run("ecom_chatbot.api.server:app", host="0.0.0.0", port=8000, reload=False)


if __name__ == "__main__":
    main()

