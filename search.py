from ddgs import DDGS


def find_sources(query, max_results=10):

    urls = []

    blacklist = [
        "youtube",
        "facebook",
        "instagram",
        "reddit",
        "tiktok",
        "twitter",
        "x.com"
    ]

    with DDGS() as ddgs:

        results = ddgs.text(
            query,
            max_results=max_results
        )

        for r in results:

            url = r.get("href")

            if not url:
                continue

            if any(b in url.lower() for b in blacklist):
                continue

            urls.append(url)

    return urls