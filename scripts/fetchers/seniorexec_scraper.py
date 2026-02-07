"""Scrape Senior Executive AI Think Tank profile for published articles."""

import requests
from bs4 import BeautifulSoup
from typing import List, Dict


def fetch_senior_exec_articles(
    profile_url: str,
    max_items: int = 5,
    source_label: str = "Senior Executive AI Think Tank"
) -> List[Dict]:
    """
    Scrape published articles from Senior Executive profile page.
    The profile page has a "Published content" section with article cards.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; GitHub-Profile-Bot/1.0)"
    }

    try:
        response = requests.get(profile_url, headers=headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        articles = []
        # Senior Executive profile lists articles as linked cards
        for link in soup.select("a[href*='/ai-'], a[href*='/how-'], a[href*='/what-']"):
            title_text = link.get_text(strip=True)
            href = link.get("href", "")

            if title_text and len(title_text) > 20 and href.startswith("http"):
                if not any(a["url"] == href for a in articles):
                    articles.append({
                        "title": title_text,
                        "url": href,
                        "date": "",
                        "source": source_label,
                    })

            if len(articles) >= max_items:
                break

        return articles
    except Exception:
        return []
