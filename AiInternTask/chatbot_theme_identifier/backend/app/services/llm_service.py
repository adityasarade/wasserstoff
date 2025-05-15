import os
import requests
from dotenv import load_dotenv
import tiktoken
from app.core.config import params
import time
from requests.exceptions import HTTPError

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

def truncate_text(text: str, max_tokens: int = None) -> str:
    max_toks = params["llm"]["max_tokens"]
    # tiktoken doesn't officially support LLaMA, using GPT-3.5 tokenizer instead
    enc = tiktoken.encoding_for_model("gpt-3.5-turbo")
    tokens = enc.encode(text)
    if len(tokens) <= max_toks:
        return text
    return enc.decode(tokens[:max_toks])

def query_llm(system_prompt: str, user_prompt: str, model: str = None) -> str:
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": params["llm"]["model_name"],
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": truncate_text(user_prompt)}
        ],
        "temperature": params["llm"]["temperature"]
    }

    max_retries = 3
    for attempt in range(max_retries):
        response = requests.post(GROQ_API_URL, headers=headers, json=payload, verify=False)
        if response.status_code == 429:
            wait = 2 ** attempt  # exponential back-off: 1s, 2s, 4s
            time.sleep(wait)
            continue
        try:
            response.raise_for_status()
        except HTTPError as e:
            # re-raise non-rate-limit errors immediately
            raise
        return response.json()["choices"][0]["message"]["content"]

    # If we get here, we retried max_retries times
    raise Exception("Rate limit exceeded. Please try again later.")