import json
import time

from search import find_sources
from scraper import get_text
from extractor import extract_structured_items
from analyzer import rank_structured
from llm import explain_results
from formatter import build_final_answer, pretty_print
from memory import add_to_memory


class WebIntelligenceAgent:

    def run(self, query):

        print(f"\n🔎 AI AGENT PRO MODE: {query}\n")
        print("🧠 USING HYBRID PIPELINE")

        start_time = time.time()

        all_items = []
        visited = set()

        urls = find_sources(query) or []

        print("DEBUG URLS:", urls)
        print("FINAL QUERY:", query)

        BAD_SITES = [
            "quora", "pinterest", "scribd",
            "google", "youtube", "reddit",
            "facebook", "caratlane"
        ]

        urls = [u for u in urls if not any(b in u for b in BAD_SITES)]
        urls = urls[:4]

        for url in urls:

            if time.time() - start_time > 18:
                break

            if url in visited:
                continue

            visited.add(url)

            print("SCRAPING:", url)

            try:
                text = get_text(url)

                if not text or len(text) < 80:
                    continue

                items = extract_structured_items(text)

                # ✅ always extend even partial
                all_items.extend(items)

            except Exception as e:
                print("SKIP URL:", url, e)

        print("ITEMS FOUND:", len(all_items))

        # ⚠️ REAL FALLBACK ONLY IF EMPTY
        if len(all_items) == 0:

            print("⚠️ NO DATA → fallback mode")

            return {
                "ai_mode": True,
                "raw_context": [],
                "query": query,
                "status": "fallback"
            }

        ranked = rank_structured(all_items)

        top_products = []

        for r in ranked[:5]:

            item = r["item"]

            top_products.append({
                "name": item.get("name_hint"),
                "price": item.get("price"),
                "ram": item.get("ram"),
                "confidence": r.get("confidence", 0)
            })

        context = json.dumps(top_products, indent=2, ensure_ascii=False)

        llm_input = f"""
Query:
{query}

DATA:
{context}
"""

        llm_text = explain_results(query, llm_input)

        result = build_final_answer(query, ranked, llm_text)

        pretty_print(result)

        add_to_memory(query, result)

        return result