def rank_structured(items):

    ranked = []

    for item in items:

        score = 0
        confidence = 0

        price = item.get("price")

        # 💰 PRICE LOGIC (CLEAN FIX)
        if price is None or price == "":
            score -= 0.8
        else:
            score += 1
            confidence += 1

            if price < 500:
                score += 0.7
            elif price < 1000:
                score += 0.5
            elif price < 1500:
                score += 0.3

        # 🧠 RAM BONUS
        ram = item.get("ram")

        if ram == "32GB":
            score += 0.5
        elif ram == "16GB":
            score += 0.4
        elif ram == "8GB":
            score += 0.2

        # 📏 QUALITY BONUS
        if len(item.get("raw", "")) > 80:
            score += 0.2

        # 🧠 SAFE NAME CHECK (FIXED)
        name_hint = item.get("name_hint", "").lower()

        if price and any(x in name_hint for x in [
            "asus", "lenovo", "dell", "hp", "acer", "msi", "apple"
        ]):
            confidence += 1

        # 🔥 FINAL SCORE PACK
        ranked.append({
            "item": item,
            "score": round(score, 3),
            "confidence": round(confidence, 3)
        })

    return sorted(ranked, key=lambda x: x["score"], reverse=True)