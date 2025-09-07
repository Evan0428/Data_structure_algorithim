from __future__ import annotations

from dataclasses import dataclass
from typing import List, Dict, Any, Tuple
import json
from pathlib import Path
import math
import pickle
from collections import defaultdict, Counter

from .preprocess import normalize_corpus


@dataclass
class IntentExample:
    text: str
    label: str


def load_intent_examples(intents_json_path: str | Path) -> Tuple[List[str], List[str]]:
    path = Path(intents_json_path)
    data = json.loads(path.read_text())
    texts: List[str] = []
    labels: List[str] = []
    for intent in data.get("intents", []):
        label = intent["name"]
        for utt in intent.get("utterances", []):
            texts.append(utt)
            labels.append(label)
    return texts, labels


class NaiveBayesIntent:
    def __init__(self) -> None:
        self.class_to_token_counts: Dict[str, Counter[str]] = {}
        self.class_to_total_tokens: Dict[str, int] = {}
        self.class_priors: Dict[str, float] = {}
        self.vocab: set[str] = set()

    @staticmethod
    def _tokenize(text: str) -> List[str]:
        return text.split()

    def fit(self, texts: List[str], labels: List[str]) -> None:
        docs_per_class: Dict[str, int] = defaultdict(int)
        token_counts: Dict[str, Counter[str]] = defaultdict(Counter)
        for text, label in zip(texts, labels):
            docs_per_class[label] += 1
            for tok in self._tokenize(text):
                token_counts[label][tok] += 1
                self.vocab.add(tok)

        total_docs = sum(docs_per_class.values())
        self.class_priors = {c: docs_per_class[c] / total_docs for c in docs_per_class}
        self.class_to_token_counts = dict(token_counts)
        self.class_to_total_tokens = {
            c: sum(token_counts[c].values()) for c in token_counts
        }

    def predict_proba(self, text: str) -> Dict[str, float]:
        tokens = self._tokenize(text)
        vocab_size = max(1, len(self.vocab))
        log_probs: Dict[str, float] = {}
        for cls, prior in self.class_priors.items():
            logp = math.log(prior + 1e-12)
            total = self.class_to_total_tokens[cls]
            counts = self.class_to_token_counts[cls]
            for tok in tokens:
                # Laplace smoothing
                tok_count = counts.get(tok, 0)
                logp += math.log((tok_count + 1) / (total + vocab_size))
            log_probs[cls] = logp
        # convert to normalised probabilities
        max_log = max(log_probs.values())
        exps = {c: math.exp(lp - max_log) for c, lp in log_probs.items()}
        z = sum(exps.values())
        return {c: v / z for c, v in exps.items()}

    def predict(self, text: str) -> Tuple[str, float, Dict[str, float]]:
        proba = self.predict_proba(text)
        label = max(proba.items(), key=lambda kv: kv[1])[0]
        return label, proba[label], proba


def _stratified_split(
    texts: List[str], labels: List[str], test_ratio: float = 0.2
) -> Tuple[List[str], List[str], List[str], List[str]]:
    by_label: Dict[str, List[int]] = defaultdict(list)
    for idx, lbl in enumerate(labels):
        by_label[lbl].append(idx)
    test_indices: List[int] = []
    train_indices: List[int] = []
    for lbl, idxs in by_label.items():
        n = len(idxs)
        n_test = max(1, int(round(n * test_ratio))) if n > 1 else 1
        # take last n_test examples as test for determinism
        test_indices.extend(idxs[-n_test:])
        train_indices.extend(idxs[:-n_test] if n_test < n else idxs[:-1])
    # ensure unique and preserve original order for stability
    train_indices = sorted(set(train_indices))
    test_indices = sorted(set(test_indices))
    x_train = [texts[i] for i in train_indices]
    y_train = [labels[i] for i in train_indices]
    x_test = [texts[i] for i in test_indices]
    y_test = [labels[i] for i in test_indices]
    return x_train, x_test, y_train, y_test


def train_and_save(
    intents_json_path: str | Path,
    model_output_path: str | Path,
    test_size: float = 0.2,
    random_state: int = 42,
) -> Dict[str, Any]:
    texts, labels = load_intent_examples(intents_json_path)
    texts = normalize_corpus(texts)
    x_train, x_test, y_train, y_test = _stratified_split(texts, labels, test_ratio=test_size)

    model = NaiveBayesIntent()
    model.fit(x_train, y_train)

    # Evaluate
    correct = 0
    for t, y in zip(x_test, y_test):
        pred, _, _ = model.predict(t)
        correct += int(pred == y)
    acc = correct / max(1, len(x_test))

    model_output_path = Path(model_output_path)
    model_output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(model_output_path, "wb") as f:
        pickle.dump(model, f)

    metrics = {"accuracy": acc, "n_train": len(x_train), "n_test": len(x_test)}
    return metrics


def load_model(model_path: str | Path) -> NaiveBayesIntent:
    with open(model_path, "rb") as f:
        return pickle.load(f)


def predict_intent(model: NaiveBayesIntent, text: str) -> Tuple[str, float, Dict[str, float]]:
    norm = normalize_corpus([text])[0]
    label, score, proba = model.predict(norm)
    return label, float(score), {k: float(v) for k, v in proba.items()}

