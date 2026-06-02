import json
import os

FILE = "memory.json"

def load_memory():
    if not os.path.exists(FILE):
        return []
    return json.load(open(FILE, "r", encoding="utf-8"))

def save_memory(data):
    json.dump(data, open(FILE, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

def add_to_memory(query, result):
    data = load_memory()
    data.append({"query": query, "result": result})
    save_memory(data[-20:])

def get_memory():
    return load_memory()