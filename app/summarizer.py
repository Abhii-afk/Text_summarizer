import os
import re

import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer


MODEL_ID = os.getenv("MODEL_ID", "google-t5/t5-small")
tokenizer = T5Tokenizer.from_pretrained(MODEL_ID)
model = T5ForConditionalGeneration.from_pretrained(MODEL_ID)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
model.eval()


def clean_data(text: str) -> str:
    text = re.sub(r"\r\n", " ", text)
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"<.*?>", " ", text)
    return text.strip()


def summarize(text: str) -> str:
    if not text or not text.strip():
        raise ValueError("Text must not be empty.")

    dialogue = "summarize: " + clean_data(text)
    inputs = tokenizer(
        dialogue,
        padding=True,
        truncation=True,
        max_length=512,
        return_tensors="pt",
    )
    inputs = {key: value.to(device) for key, value in inputs.items()}

    with torch.no_grad():
        targets = model.generate(
            input_ids=inputs["input_ids"],
            attention_mask=inputs["attention_mask"],
            max_new_tokens=120,
            num_beams=4,
            length_penalty=1.2,
            no_repeat_ngram_size=3,
            early_stopping=True,
        )

    return tokenizer.decode(targets[0], skip_special_tokens=True)
