from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List, Tuple
from pathlib import Path

from ..nlu.intent_classifier import load_model, predict_intent
from ..nlu.entities import extract_order_id, extract_search_keywords
from .product_search import ProductSearchEngine
from .response_templates import render


@dataclass
class Turn:
    user_text: str
    intent: Optional[str] = None
    confidence: float = 0.0
    response: Optional[str] = None


@dataclass
class DialogState:
    context: Dict[str, Any] = field(default_factory=dict)
    history: List[Turn] = field(default_factory=list)


class DialogManager:
    def __init__(
        self,
        intent_model_path: str | Path,
        catalog_csv_path: str | Path,
        confidence_threshold: float = 0.45,
    ) -> None:
        self.model = load_model(intent_model_path)
        self.product_search = ProductSearchEngine(catalog_csv_path)
        self.threshold = confidence_threshold
        self.state = DialogState()

    def _classify(self, text: str) -> Tuple[str, float]:
        label, score, _ = predict_intent(self.model, text)
        return label, score

    def _handle_order_status(self, text: str) -> str:
        order_id = extract_order_id(text) or self.state.context.get("order_id")
        if not order_id:
            self.state.context["awaiting_order_id"] = True
            return render("order_id_request")
        # Fake order lookup for prototype
        self.state.context["order_id"] = order_id
        status = "shipped"
        eta = "3 days"
        self.state.context.pop("awaiting_order_id", None)
        return render("order_status_found", order_id=order_id, status=status, eta=eta)

    def _handle_product_search(self, text: str) -> str:
        keywords = extract_search_keywords(text)
        query = " ".join(keywords) if keywords else text
        results = self.product_search.search(query, top_k=5)
        if not results:
            return "I couldn't find matching products. Could you be more specific?"
        lines = [
            f"{r['title']} ({r['brand']}) - ${r['price']:.2f} [ID: {r['product_id']}]"
            for r in results
        ]
        return "Here are some options:\n" + "\n".join(lines)

    def respond(self, text: str) -> str:
        label, score = self._classify(text)
        turn = Turn(user_text=text, intent=label, confidence=score)

        if score < self.threshold:
            # Check if awaiting order ID
            if self.state.context.get("awaiting_order_id"):
                # try to capture order ID
                oid = extract_order_id(text)
                if oid:
                    reply = self._handle_order_status(text)
                else:
                    reply = render("order_id_request")
            else:
                reply = "Sorry, I didn't understand. Could you rephrase?"
        else:
            if label == "greet":
                reply = render("greet")
            elif label == "goodbye":
                reply = render("goodbye")
            elif label == "return_policy":
                reply = render("return_policy")
            elif label == "shipping_info":
                reply = render("shipping_info")
            elif label == "order_status":
                reply = self._handle_order_status(text)
            elif label == "product_search":
                reply = self._handle_product_search(text)
            else:
                reply = "How can I assist you with your shopping today?"

        turn.response = reply
        self.state.history.append(turn)
        return reply

