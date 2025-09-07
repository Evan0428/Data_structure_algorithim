from __future__ import annotations

from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from ecom_chatbot.nlu.intent_classifier import load_model, predict_intent  # type: ignore


def test_basic_intents():
    model = load_model(Path(__file__).resolve().parents[1] / "models/intent_model.pkl")
    label, score, _ = predict_intent(model, "hi there")
    assert label in {"greet", "goodbye", "order_status", "return_policy", "shipping_info", "product_search"}
    assert 0.0 <= score <= 1.0

