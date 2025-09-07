import os
import sys
import json
import re
import difflib
import csv
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import joblib
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.pipeline import Pipeline


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
MODELS_DIR = PROJECT_ROOT / "models"
INTENT_MODEL_PATH = MODELS_DIR / "intent_pipeline.joblib"


class IntentClassifier:
	def __init__(self, model_path: Path):
		self.model_path = model_path
		self.pipeline: Optional[Pipeline] = None

	def train_from_intents(self, intents_json_path: Path) -> None:
		with open(intents_json_path, "r", encoding="utf-8") as f:
			data = json.load(f)
		texts: List[str] = []
		labels: List[str] = []
		for item in data.get("intents", []):
			intent = item["intent"]
			for ex in item["examples"]:
				texts.append(ex)
				labels.append(intent)
		self.pipeline = Pipeline([
			("tfidf", TfidfVectorizer(ngram_range=(1, 2), lowercase=True, min_df=1)),
			("clf", LogisticRegression(max_iter=200, n_jobs=None))
		])
		self.pipeline.fit(texts, labels)

	def save(self) -> None:
		if self.pipeline is None:
			raise ValueError("Pipeline is not trained.")
		MODELS_DIR.mkdir(parents=True, exist_ok=True)
		joblib.dump(self.pipeline, self.model_path)

	def load(self) -> None:
		self.pipeline = joblib.load(self.model_path)

	def predict(self, text: str) -> Tuple[str, float]:
		if self.pipeline is None:
			raise ValueError("Pipeline is not loaded.")
		probas = self.pipeline.predict_proba([text])[0]
		classes = list(self.pipeline.classes_)
		best_idx = int(np.argmax(probas))
		return classes[best_idx], float(probas[best_idx])


class FAQRetriever:
	def __init__(self, faq_csv_path: Path):
		self.rows: List[Dict[str, str]] = []
		with open(faq_csv_path, "r", encoding="utf-8") as f:
			reader = csv.DictReader(f)
			for row in reader:
				self.rows.append({"question": row.get("question", ""), "answer": row.get("answer", "")})
		texts = [f"{r['question']} \n {r['answer']}".strip() for r in self.rows]
		self.vectorizer = TfidfVectorizer(ngram_range=(1, 2), lowercase=True)
		self.matrix = self.vectorizer.fit_transform(texts)

	def retrieve(self, query: str) -> Tuple[Dict[str, str], float]:
		q_vec = self.vectorizer.transform([query])
		sims = cosine_similarity(q_vec, self.matrix)[0]
		idx = int(np.argmax(sims))
		score = float(sims[idx])
		row = self.rows[idx]
		return row, score


class EntityExtractor:
	ORDER_ID_PATTERN = re.compile(r"\bORD\d{5}\b", re.IGNORECASE)

	def __init__(self, products_csv_path: Path):
		self.products: List[Dict[str, str]] = []
		with open(products_csv_path, "r", encoding="utf-8") as f:
			reader = csv.DictReader(f)
			for row in reader:
				self.products.append({
					"name": row.get("name", ""),
					"stock": row.get("stock", "0"),
					"price": row.get("price", "0")
				})
		self.product_names = [p["name"] for p in self.products]

	def extract_order_id(self, text: str) -> Optional[str]:
		match = self.ORDER_ID_PATTERN.search(text)
		if match:
			return match.group(0).upper()
		return None

	def extract_product_name(self, text: str) -> Optional[str]:
		candidates = difflib.get_close_matches(text, self.product_names, n=1, cutoff=0.6)
		if candidates:
			return candidates[0]
		lowered = text.lower()
		for name in self.product_names:
			if name.lower() in lowered:
				return name
		return None

	def find_product(self, name: str) -> Optional[Dict[str, str]]:
		for p in self.products:
			if p["name"] == name:
				return p
		return None


class DialogueManager:
	def __init__(self, intent_clf: IntentClassifier, faq: FAQRetriever, ner: EntityExtractor, orders_csv_path: Path):
		self.intent_clf = intent_clf
		self.faq = faq
		self.ner = ner
		self.orders: List[Dict[str, str]] = []
		with open(orders_csv_path, "r", encoding="utf-8") as f:
			reader = csv.DictReader(f)
			for row in reader:
				self.orders.append({
					"order_id": row.get("order_id", "").upper(),
					"product_name": row.get("product_name", ""),
					"status": row.get("status", "")
				})
		self.state: Dict[str, Optional[str]] = {"pending_slot": None, "order_id": None, "product_name": None}

	def respond(self, user_text: str) -> str:
		if self.state["pending_slot"] == "order_id":
			order_id = self.ner.extract_order_id(user_text) or user_text.strip().upper()
			if re.match(r"^ORD\d{5}$", order_id):
				self.state["order_id"] = order_id
				self.state["pending_slot"] = None
				return self._handle_track_order()
			return "Please provide a valid order ID like ORD12345."

		if self.state["pending_slot"] == "product_name":
			product_name = self.ner.extract_product_name(user_text)
			if product_name:
				self.state["product_name"] = product_name
				self.state["pending_slot"] = None
				return self._handle_product_availability()
			return "Sorry, I couldn't find that product. Could you rephrase the name?"

		intent, conf = self.intent_clf.predict(user_text)

		if intent == "greet":
			return "Hello! How can I help you today?"
		if intent == "goodbye":
			return "Goodbye! Have a great day."
		if intent == "thanks":
			return "You're welcome!"

		if intent == "track_order":
			self.state["order_id"] = self.ner.extract_order_id(user_text)
			if not self.state["order_id"]:
				self.state["pending_slot"] = "order_id"
				return "Sure—what is your order ID? (e.g., ORD12345)"
			return self._handle_track_order()

		if intent == "cancel_order":
			self.state["order_id"] = self.ner.extract_order_id(user_text)
			if not self.state["order_id"]:
				self.state["pending_slot"] = "order_id"
				return "I can help cancel your order. What is your order ID?"
			return self._handle_cancel_order()

		if intent in ("return_policy", "refund_policy", "faq"):
			doc, score = self.faq.retrieve(user_text)
			return f"{doc['answer']}"

		if intent == "product_search":
			names = self.ner.product_names
			suggestions = difflib.get_close_matches(user_text, names, n=5, cutoff=0.3)
			if not suggestions:
				return "I can help with products. Try asking about a specific item name."
			return "Here are some products you might be interested in: " + ", ".join(suggestions)

		if intent == "product_availability":
			self.state["product_name"] = self.ner.extract_product_name(user_text)
			if not self.state["product_name"]:
				self.state["pending_slot"] = "product_name"
				return "Which product are you asking about?"
			return self._handle_product_availability()

		doc, score = self.faq.retrieve(user_text)
		if score >= 0.2:
			return f"{doc['answer']}"
		return "Sorry, I didn't understand that. You can ask me about orders, products, shipping, returns, or refunds."

	def _handle_track_order(self) -> str:
		order_id = self.state.get("order_id")
		if not order_id:
			return "Please provide your order ID (e.g., ORD12345)."
		row = next((o for o in self.orders if o["order_id"] == order_id), None)
		if row is None:
			return f"I couldn't find order {order_id}. Please check the ID."
		status = row["status"]
		product = row["product_name"]
		return f"Order {order_id} for {product}: current status is '{status}'."

	def _handle_cancel_order(self) -> str:
		order_id = self.state.get("order_id")
		if not order_id:
			return "Please provide your order ID (e.g., ORD12345)."
		row = next((o for o in self.orders if o["order_id"] == order_id), None)
		if row is None:
			return f"I couldn't find order {order_id}. Please check the ID."
		status = row["status"].lower()
		if status in {"processing", "placed"}:
			return f"Order {order_id} has been cancelled. You will receive a confirmation email shortly."
		return f"Order {order_id} is '{status}' and cannot be cancelled at this stage."

	def _handle_product_availability(self) -> str:
		product_name = self.state.get("product_name")
		if not product_name:
			return "Which product are you asking about?"
		row = self.ner.find_product(product_name)
		if row is None:
			return f"I couldn't find '{product_name}'."
		stock = int(float(row.get("stock", 0)))
		price = float(row.get("price", 0))
		if stock > 0:
			return f"Yes, {product_name} is in stock ({stock} units) at ${price:.2f}."
		return f"{product_name} is currently out of stock."


def bootstrap_intent_model() -> IntentClassifier:
	clf = IntentClassifier(INTENT_MODEL_PATH)
	if not INTENT_MODEL_PATH.exists():
		print("[setup] Training intent classifier...")
		clf.train_from_intents(DATA_DIR / "intents.json")
		clf.save()
		print("[setup] Intent model saved to", INTENT_MODEL_PATH)
	else:
		clf.load()
	return clf


def build_chatbot() -> DialogueManager:
	intent_clf = bootstrap_intent_model()
	faq = FAQRetriever(DATA_DIR / "faqs.csv")
	ner = EntityExtractor(DATA_DIR / "products.csv")
	dm = DialogueManager(intent_clf, faq, ner, DATA_DIR / "orders.csv")
	return dm


def main() -> None:
	print("E-commerce Customer Service Chatbot")
	print("Type 'exit' or 'quit' to leave.\n")
	dm = build_chatbot()
	while True:
		try:
			user = input("you: ").strip()
		except (EOFError, KeyboardInterrupt):
			print()
			break
		if user.lower() in {"exit", "quit"}:
			break
		if not user:
			continue
		reply = dm.respond(user)
		print("bot:", reply)


if __name__ == "__main__":
	sys.path.append(str(PROJECT_ROOT / "src"))
	main()
