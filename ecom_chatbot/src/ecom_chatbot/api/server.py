from __future__ import annotations

from pathlib import Path
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

from ..engine.dialog_manager import DialogManager


class Message(BaseModel):
    text: str


def create_app(
    model_path: str | Path = "models/intent_model.pkl",
    catalog_path: str | Path = "data/catalog/products.csv",
) -> FastAPI:
    app = FastAPI(title="E-commerce Chatbot")
    dm = DialogManager(model_path, catalog_path)

    @app.get("/healthz")
    def healthz() -> dict:
        return {"status": "ok"}

    @app.post("/chat")
    def chat(msg: Message) -> dict:
        reply = dm.respond(msg.text)
        return {"reply": reply}

    return app


app = create_app()

