from __future__ import annotations

import argparse
from pathlib import Path
import json

# Allow running without installing the package
import sys
sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from ecom_chatbot.nlu.intent_classifier import train_and_save  # type: ignore


def main() -> None:
    parser = argparse.ArgumentParser(description="Train intent classifier")
    parser.add_argument(
        "--intents", default="data/raw/intents.json", help="Path to intents JSON"
    )
    parser.add_argument(
        "--output", default="models/intent_model.pkl", help="Model output path"
    )
    parser.add_argument("--test-size", type=float, default=0.2)
    args = parser.parse_args()

    metrics = train_and_save(args.intents, args.output, test_size=args.test_size)
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()

