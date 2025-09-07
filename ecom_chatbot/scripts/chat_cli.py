from __future__ import annotations

from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from ecom_chatbot.engine.dialog_manager import DialogManager  # type: ignore


def main() -> None:
    dm = DialogManager(
        intent_model_path="models/intent_model.pkl",
        catalog_csv_path="data/catalog/products.csv",
    )
    print("E-commerce Chatbot (type 'quit' to exit)")
    while True:
        try:
            user = input("You: ")
        except EOFError:
            break
        if user.strip().lower() in {"quit", "exit"}:
            break
        reply = dm.respond(user)
        print(f"Bot: {reply}")


if __name__ == "__main__":
    main()

