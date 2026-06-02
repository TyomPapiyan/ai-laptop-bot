import json

def build_final_answer(query, ranked, llm_text):

    return {
        "query": query,
        "top_results": [
            {
                "name": r["item"].get("name_hint"),
                "price": r["item"].get("price"),
                "ram": r["item"].get("ram"),
                "score": r["score"]
            }
            for r in ranked[:5]
        ],
        "ai_reasoning": llm_text,
        "status": "success"
    }


def pretty_print(data):

    print("\n🏆 FINAL ANSWER\n")
    print("Query:", data["query"])

    print("\nTop results:\n")

    for i, r in enumerate(data["top_results"], 1):
        print(f"{i}. {r['name']}")
        print(f"   💰 {r['price']}")
        print(f"   🧠 {r['score']}\n")

    print("🧠 AI REASONING:\n")
    print(data["ai_reasoning"])