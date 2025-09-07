## E-commerce Customer Service Chatbot (Python)

An offline, classical-ML chatbot for e-commerce support. Features:
- Intent classification (scikit-learn TF-IDF + Logistic Regression)
- FAQ retrieval (TF-IDF cosine similarity)
- Simple entity extraction for order IDs and product names
- Dialogue manager with slot filling for order tracking and product queries
- CLI interface for demo
- Evaluation script for NLU (cross-validation) and FAQ (top-1)

### Quickstart

1) Install dependencies
- Preferred (venv):
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```
- If venv is unavailable, install with:
```bash
python3 -m pip install --break-system-packages -r requirements.txt
```

2) Run the chatbot (CLI)
```bash
PYTHONPATH=$(pwd) python3 -m src.app
```
- Type your messages. Examples:
  - "hi"
  - "where is my order ORD12345"
  - "is iPhone 13 in stock"
  - "what is your return policy"
  - "shipping fee"
  - "cancel my order ORD54321"
- Type `exit` or `quit` to leave.

The first run will auto-train and save an intent model under `models/intent_pipeline.joblib` using `data/intents.json`.

3) Evaluate
```bash
PYTHONPATH=$(pwd) python3 evaluate.py
```
Reports NLU cross-validation metrics and FAQ top-1 accuracy.

### Project Structure
```
ecom_chatbot/
├── data/
│   ├── intents.json
│   ├── faqs.csv
│   ├── products.csv
│   └── orders.csv
├── models/                # created on first run
├── src/
│   ├── __init__.py
│   └── app.py
├── evaluate.py
├── requirements.txt
└── README.md
```

### Notes for the Report (Documentation Part 1)
- Section 1 (Intro): Problem: automate e-commerce customer support (order tracking, returns, FAQs).
- Section 2 (Background): Compare rule-based vs classical ML vs LLM; justify TF-IDF+LR for simplicity and transparency.
- Section 3 (Methodology): Provide flowchart: User -> NLU -> Dialogue -> Action/FAQ -> Response. Describe dataset (toy), algorithms, and test plan.
- Section 4 (Result): Include evaluation script outputs.
- Section 5 (Discussion): Achievements, limitations (toy data, no DB), and future work (web UI, larger corpora, LLMs, Rasa/Dialogflow integration).

### Extending
- Add more intents, examples, and entities in `data/intents.json`.
- Grow `data/faqs.csv`, `data/products.csv` and integrate a real DB or API.
- Replace Logistic Regression with SVM/ANN, add confidence calibration, or integrate a seq2seq/transformer model.

### License
For academic use.
