import re

BRANDS = [
    "asus", "lenovo", "dell", "hp", "acer",
    "msi", "apple", "thinkpad", "vivobook",
    "legion", "rog", "macbook", "inspiron", "pavilion"
]

BAD_WORDS = [
    "guide", "review", "article", "blog",
    "comparison", "tips", "how to",
    "battery life", "vs", "difference", "explained"
]


def is_valid(line: str) -> bool:

    line_low = line.lower()

    # ❌ SEO filter
    if any(w in line_low for w in BAD_WORDS):
        return False

    # ✅ FLEXIBLE KEYWORDS (важный FIX)
    if not any(x in line_low for x in [
        "laptop", "macbook", "notebook",
        "intel", "amd", "ryzen", "gaming"
    ]):
        return False

    # ❌ brand OR model OR keyword (НЕ строго)
    if not any(b in line_low for b in BRANDS):
        if "ryzen" not in line_low and "intel" not in line_low:
            return False

    # ❌ noise filter
    if len(line.split()) < 4:
        return False

    return True


def extract_structured_items(text):

    items = []
    seen = set()

    for line in text.split("\n"):

        line = line.strip()
        if not is_valid(line):
            continue

        price = None

        # 💰 flexible price extraction (VERY IMPORTANT FIX)
        price_match = re.search(r"(\$|usd|price)?\s*([\d,]{2,6})", line.lower())

        if price_match:
            try:
                price = int(price_match.group(2).replace(",", ""))
            except:
                price = None

        # ❌ skip insane prices
        if price is not None and price > 10000:
            continue

        # 🧠 RAM detection
        ram = None
        line_low = line.lower()

        if "64gb" in line_low:
            ram = "64GB"
        elif "32gb" in line_low:
            ram = "32GB"
        elif "16gb" in line_low:
            ram = "16GB"
        elif "8gb" in line_low:
            ram = "8GB"

        # 🏷️ name
        name = line[:140]

        key = name.lower()
        if key in seen:
            continue
        seen.add(key)

        items.append({
            "raw": line,
            "price": price,
            "ram": ram,
            "name_hint": name
        })

    # ⚠️ IMPORTANT FIX: NO HARD FAKE FALLBACK
    # (раньше ты сам себе ломал ranking)
    return items