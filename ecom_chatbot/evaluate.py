import json
from pathlib import Path
from typing import List

import csv
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.metrics.pairwise import cosine_similarity

PROJECT_ROOT = Path(__file__).resolve().parent
DATA_DIR = PROJECT_ROOT / "data"


def evaluate_nlu() -> None:
	with open(DATA_DIR / "intents.json", "r", encoding="utf-8") as f:
		data = json.load(f)
	texts: List[str] = []
	labels: List[str] = []
	for item in data.get("intents", []):
		for ex in item["examples"]:
			texts.append(ex)
			labels.append(item["intent"])
	pipeline = Pipeline([
		("tfidf", TfidfVectorizer(ngram_range=(1, 2), lowercase=True)),
		("clf", LogisticRegression(max_iter=200))
	])
	skf = StratifiedKFold(n_splits=min(5, len(set(labels))), shuffle=True, random_state=42)
	scores = cross_val_score(pipeline, texts, labels, cv=skf, scoring="accuracy")
	print("NLU Intent Classification (cross-val accuracy):")
	print(f"  mean={scores.mean():.3f} std={scores.std():.3f} folds={len(scores)}")


def evaluate_faq_top1() -> None:
	rows: List[dict] = []
	with open(DATA_DIR / "faqs.csv", "r", encoding="utf-8") as f:
		reader = csv.DictReader(f)
		for row in reader:
			rows.append({"question": row.get("question", ""), "answer": row.get("answer", "")})
	texts = [f"{r['question']} \n {r['answer']}".strip() for r in rows]
	vec = TfidfVectorizer(ngram_range=(1, 2), lowercase=True)
	mat = vec.fit_transform(texts)
	q_vecs = vec.transform([r["question"] for r in rows])
	sims = cosine_similarity(q_vecs, mat)
	pred = sims.argmax(axis=1)
	acc = np.mean(pred == np.arange(len(rows)))
	print("FAQ Retrieval Top-1 (self-query by question):")
	print(f"  accuracy={acc:.3f} over {len(rows)} questions")


if __name__ == "__main__":
	print("Running evaluation...\n")
	evaluate_nlu()
	print()
	evaluate_faq_top1()
