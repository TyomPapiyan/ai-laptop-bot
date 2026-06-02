import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

# 🟡 OLLAMA
OLLAMA_URL = "http://localhost:11434/api/chat"


def call_ollama(prompt: str) -> str:
    try:
        res = requests.post(
            OLLAMA_URL,
            json={
                "model": "llama3:latest",  # или llama3
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "stream": False
            },
            timeout=10
        )

        return res.json()["message"]["content"]

    except Exception as e:
        return f"[Ollama error: {e}]"


# ❌ OpenAI временно отключён
# from openai import OpenAI
# openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def explain_results(query, context):

    prompt = f"""
You are a strict product AI.

ONLY use provided DATA.
DO NOT invent products.

Query: {query}

DATA:
{context}

Return:
- Best Choice
- Why
- Alternatives
- Short Conclusion
"""

    # 🔥 ALWAYS USE OLLAMA NOW
    return call_ollama(prompt)