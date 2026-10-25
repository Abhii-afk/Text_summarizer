# T5 SAMSum Summarizer

This project serves the `google-t5/t5-small` model through a small FastAPI web
UI and JSON API.

## Run with Docker

Build and run the default image:

```bash
docker build -t t5-summarizer .
docker run -p 8000:8000 t5-summarizer
```

The default image downloads `google-t5/t5-small` during the build. To build
with another model on the Hugging Face Hub, pass its ID:

```bash
docker build --build-arg MODEL_ID=google-t5/t5-small -t t5-summarizer .
```

Open <http://localhost:8000>, or call the API:

```bash
curl -X POST http://localhost:8000/summarize \
  -H "Content-Type: application/json" \
  -d '{"text":"John: Are we meeting tomorrow? Sarah: Yes, at ten."}'
```

The local `saved_summary_model/` directory is ignored. To use it locally,
set `MODEL_ID=./saved_summary_model` before starting the app.

[![CI](https://github.com/Abhii-afk/Text_summarizer/actions/workflows/ci.yml/badge.svg)](https://github.com/Abhii-afk/Text_summarizer/actions/workflows/ci.yml)
