FROM python:3.11-slim

ARG MODEL_ID=google-t5/t5-small
ENV MODEL_ID=${MODEL_ID} \
    HF_HOME=/opt/huggingface \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN python -c "from transformers import T5ForConditionalGeneration, T5Tokenizer; model_id='${MODEL_ID}'; T5Tokenizer.from_pretrained(model_id); T5ForConditionalGeneration.from_pretrained(model_id)"

COPY app ./app

RUN useradd --create-home --shell /usr/sbin/nologin appuser && chown -R appuser:appuser /app /opt/huggingface
USER appuser

EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
