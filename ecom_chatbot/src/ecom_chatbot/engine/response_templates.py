from __future__ import annotations

from typing import Dict, Any, List


GENERIC_FALLBACKS: List[str] = [
    "I'm not sure I understood that. Could you rephrase?",
    "Sorry, I didn't catch that. Can you try asking in a different way?",
]


TEMPLATES: Dict[str, str] = {
    "greet": "Hello! How can I help you today?",
    "goodbye": "Goodbye! If you need anything else, I'm here.",
    "return_policy": "You can return items within 30 days in original condition. Would you like to start a return?",
    "shipping_info": "Standard shipping is 3-5 business days. Expedited options are available at checkout.",
    "order_id_request": "Please provide your order ID (e.g., ORD-123456) to check the status.",
    "order_status_found": "Order {order_id} is currently {status}. Estimated delivery: {eta}.",
}


def render(template_key: str, **kwargs: Any) -> str:
    if template_key in TEMPLATES:
        return TEMPLATES[template_key].format(**kwargs)
    return GENERIC_FALLBACKS[0]

