import requests
from bs4 import BeautifulSoup


def get_text(url):

    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        r = requests.get(
            url,
            headers=headers,
            timeout=5,
            allow_redirects=True
        )

        # ❌ bad response
        if r.status_code != 200:
            return ""

        # ❌ huge page protection
        if len(r.text) > 2_000_000:
            return ""

        text_lower = r.text.lower()

        # ❌ block junk pages
        if any(x in text_lower for x in [
            "captcha",
            "subscribe",
            "login",
            "enable javascript"
        ]):
            return ""

        soup = BeautifulSoup(r.text, "html.parser")

        # 🧹 clean html
        for tag in soup([
            "script",
            "style",
            "noscript",
            "header",
            "footer",
            "nav",
            "aside"
        ]):
            tag.extract()

        lines = []

        for tag in soup.find_all(["h1", "h2", "h3", "li", "p"]):

            text = tag.get_text(" ", strip=True)

            if len(text) < 40:
                continue

            lines.append(text)

            # 🔥 HARD LIMIT
            if len(lines) >= 150:
                break

        return "\n".join(lines)

    except requests.exceptions.Timeout:
        print(f"TIMEOUT: {url}")
        return ""

    except Exception as e:
        print(f"SCRAPER ERROR {url}: {e}")
        return ""