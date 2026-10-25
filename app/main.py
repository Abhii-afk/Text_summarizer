from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel

from app.summarizer import summarize


app = FastAPI(title="T5 SAMSum Summarizer")
INDEX_FILE = Path(__file__).parent / "static" / "index.html"


class SummarizeRequest(BaseModel):
    text: str


@app.get("/")
def index() -> FileResponse:
    return FileResponse(INDEX_FILE)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/summarize")
def summarize_text(request: SummarizeRequest) -> dict[str, str]:
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text must not be empty.")
    return {"summary": summarize(request.text)}
