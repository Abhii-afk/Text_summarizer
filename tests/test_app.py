import importlib

from fastapi.testclient import TestClient


class FakeTokenizer:
    pad_token_id = 0

    def __call__(self, *_args, **_kwargs):
        return {"input_ids": self, "attention_mask": self}

    def to(self, _device):
        return self

    def decode(self, *_args, **_kwargs):
        return "A short summary."


class FakeModel:
    def to(self, _device):
        return self

    def eval(self):
        return self

    def generate(self, **_kwargs):
        return [[1, 2, 3]]


def client(monkeypatch):
    import transformers

    monkeypatch.setattr(
        transformers.T5Tokenizer,
        "from_pretrained",
        lambda _model_id: FakeTokenizer(),
    )
    monkeypatch.setattr(
        transformers.T5ForConditionalGeneration,
        "from_pretrained",
        lambda _model_id: FakeModel(),
    )
    import app.summarizer
    import app.main

    importlib.reload(app.summarizer)
    importlib.reload(app.main)
    return TestClient(app.main.app)


def test_health_returns_200(monkeypatch):
    response = client(monkeypatch).get("/health")
    assert response.status_code == 200


def test_summarize_returns_summary(monkeypatch):
    response = client(monkeypatch).post("/summarize", json={"text": "Hello there."})
    assert response.status_code == 200
    assert response.json() == {"summary": "A short summary."}


def test_empty_input_is_rejected(monkeypatch):
    response = client(monkeypatch).post("/summarize", json={"text": "   "})
    assert response.status_code == 400
