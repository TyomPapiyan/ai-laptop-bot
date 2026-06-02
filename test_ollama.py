print("START TEST")

import requests

try:
    print("SENDING REQUEST...")

    res = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3:latest",
            "prompt": "hello",
            "stream": False
        },
        timeout=30
    )

    print("STATUS:", res.status_code)
    print("TEXT:", res.text)

except Exception as e:
    print("ERROR:", e)

print("END TEST")