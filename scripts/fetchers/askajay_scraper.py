"""Scrape AskAjay.ai profile for published articles."""

import requests
import re
from bs4 import BeautifulSoup
from typing import List, Dict

def fetch_askajay_articles(
    profile_url: str = "https://askajay.ai/thinking",
    max_items: int = 5,
    source_label: str = "AskAjay"
) -> List[Dict]:
    """
    Scrape published articles from AskAjay thinking page.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; GitHub-Profile-Bot/1.0)"
    }

    try:
        response = requests.get(profile_url, headers=headers, timeout=15)
        response.raise_for_status()
        
        articles = []
        seen = set()
        
        # Method 1: Regex parse the Next.js JSON state
        # The titles and links are baked into __next_f.push payload
        matches = re.finditer(r'"href":"(/thinking/[^"]+)",.*?"children":"([^"]+)"', response.text)
        for match in matches:
            href = match.group(1)
            title = match.group(2)
            
            if len(title) > 15 and "Latest Thinking" not in title and href not in seen:
                seen.add(href)
                articles.append({
                    "title": title.replace('\\"', '"'),
                    "url": f"https://askajay.ai{href}",
                    "date": "",
                    "source": source_label,
                })
                
            if len(articles) >= max_items:
                return articles
                
        # Method 2: Fallback to BeautifulSoup if JS parsing failed
        if not articles:
            soup = BeautifulSoup(response.text, "html.parser")
            for link in soup.find_all("a"):
                href = link.get("href", "")
                if href.startswith("/thinking/") and len(href) > 10:
                    title_elem = link.find(["h2", "h3"])
                    title_text = title_elem.get_text(strip=True) if title_elem else link.get_text(strip=True)
                    
                    if title_text and len(title_text) > 15 and href not in seen:
                        seen.add(href)
                        articles.append({
                            "title": title_text,
                            "url": f"https://askajay.ai{href}",
                            "date": "",
                            "source": source_label,
                        })
                        
                    if len(articles) >= max_items:
                        break

        return articles
    except Exception as repr_err:
        return []
