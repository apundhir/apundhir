"""Fetch and parse RSS feeds (AiExponent, Medium, etc.)"""

import feedparser
from datetime import datetime
from typing import List, Dict


def fetch_rss_feed(url: str, max_items: int = 5, source_label: str = "") -> List[Dict]:
    feed = feedparser.parse(url)

    if feed.bozo and not feed.entries:
        raise Exception(f"RSS parse error for {url}: {feed.bozo_exception}")

    posts = []
    for entry in feed.entries[:max_items]:
        date_str = ""
        if hasattr(entry, "published_parsed") and entry.published_parsed:
            date_str = datetime(*entry.published_parsed[:6]).strftime("%Y-%m-%d")
        elif hasattr(entry, "updated_parsed") and entry.updated_parsed:
            date_str = datetime(*entry.updated_parsed[:6]).strftime("%Y-%m-%d")

        posts.append({
            "title": entry.get("title", "Untitled"),
            "url": entry.get("link", ""),
            "date": date_str,
            "source": source_label,
            "summary": entry.get("summary", "")[:200],
        })

    return posts
