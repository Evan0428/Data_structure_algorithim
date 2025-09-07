# E-commerce Customer Service Chatbot (Python)

This repository contains a pure-Python e-commerce customer service chatbot with:
intent recognition, product search, order status flow, and basic FAQs.

## Quickstart

```bash
python3 -m venv .venv --without-pip
source .venv/bin/activate
curl -sS https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py && rm get-pip.py
pip install -r requirements.txt

# Train
python scripts/train_intents.py --intents data/raw/intents.json --output models/intent_model.pkl

# Run API
python scripts/run_api.py
```

