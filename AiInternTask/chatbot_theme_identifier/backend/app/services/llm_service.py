import os
import requests
from dotenv import load_dotenv
import tiktoken

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

def truncate_text(text: str, max_tokens: int = 3000) -> str:
    # tiktoken doesn't officially support LLaMA, using GPT-3.5 tokenizer instead
    enc = tiktoken.encoding_for_model("gpt-3.5-turbo")
    tokens = enc.encode(text)
    if len(tokens) <= max_tokens:
        return text
    return enc.decode(tokens[:max_tokens])

def query_llm(system_prompt: str, user_prompt: str, model: str = "llama3-70b-8192") -> str:
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": truncate_text(user_prompt)}
        ],
        "temperature": 0.3
    }

    response = requests.post(
    GROQ_API_URL,
    headers=headers,
    json=payload,
    verify=False
)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]