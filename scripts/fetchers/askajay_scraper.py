"""Scrape the latest articles from askajay.ai/thinking."""

import requests
from bs4 import BeautifulSoup
from typing import List, Dict

BASE_URL = "https://askajay.ai"


def fetch_askajay_articles(
    profile_url: str = f"{BASE_URL}/thinking",
    max_items: int = 5,
    source_label: str = "AskAjay.ai"
) -> List[Dict]:
    """
    Return the newest articles on the thinking page, in page order.

    Each article card is an <a href="/thinking/<slug>"> wrapping an <h2> or
    <h3> title. Raises on network or parse failure so the caller can fall
    back to the cache instead of silently publishing an empty list.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; GitHub-Profile-Bot/1.0)"
    }
    response = requests.get(profile_url, headers=headers, timeout=15)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    articles = []
    seen = set()

    for link in soup.select('a[href^="/thinking/"]'):
        href = link.get("href", "").split("#")[0].split("?")[0]
        title_elem = link.find(["h2", "h3"])
        if not title_elem or href in seen:
            continue

        seen.add(href)
        articles.append({
            "title": title_elem.get_text(" ", strip=True),
            "url": f"{BASE_URL}{href}",
            "source": source_label,
        })
        if len(articles) >= max_items:
            break

    if not articles:
        raise ValueError(f"No article cards found on {profile_url}")

    return articles
