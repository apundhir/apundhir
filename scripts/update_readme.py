#!/usr/bin/env python3
"""
Auto-update GitHub profile README.
Fetches the latest AskAjay.ai articles, merges them with config.yaml and
renders TEMPLATE.md into README.md.
"""

import sys
import yaml
from datetime import datetime
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

# Ensure the project root is on the path for imports
ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.fetchers.askajay_scraper import fetch_askajay_articles
from scripts.utils.cache import load_cache, save_cache
from scripts.utils.logger import setup_logger

logger = setup_logger()

CONFIG_PATH = ROOT / "config.yaml"
TEMPLATE_PATH = ROOT / "TEMPLATE.md"
README_PATH = ROOT / "README.md"
CACHE_PATH = ROOT / "data" / "cache.json"


def load_config():
    with open(CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)


def fetch_latest_writing(config, cache):
    """Fetch the newest AskAjay.ai articles; fall back to the cache on failure."""
    feed = config.get("latest_writing") or {}
    if not feed.get("enabled", False):
        return []

    try:
        articles = fetch_askajay_articles(
            profile_url=feed["url"],
            max_items=feed.get("max_items", 5),
            source_label=feed.get("label", "AskAjay.ai")
        )
        logger.info(f"Fetched {len(articles)} articles from {feed['url']}")
        cache["latest_writing"] = articles
        return articles
    except Exception as e:
        cached = cache.get("latest_writing", [])
        logger.warning(f"AskAjay.ai fetch failed ({e}); using {len(cached)} cached articles")
        return cached


def format_publication_date(date_str):
    """Convert 2026-01-20 to Jan 2026."""
    if not date_str:
        return ""
    try:
        dt = datetime.strptime(str(date_str), "%Y-%m-%d")
        return dt.strftime("%b %Y")
    except ValueError:
        return str(date_str)


def render_readme(context):
    env = Environment(
        loader=FileSystemLoader(str(ROOT)),
        keep_trailing_newline=True,
        trim_blocks=True,
        lstrip_blocks=True,
    )
    template = env.get_template("TEMPLATE.md")
    return template.render(**context)


def main():
    logger.info("Starting README update...")

    config = load_config()
    cache = load_cache(CACHE_PATH)
    latest_writing = fetch_latest_writing(config, cache)

    publications = config.get("publications") or []
    for pub in publications:
        pub["date_formatted"] = format_publication_date(pub.get("date", ""))

    context = {
        **config,
        "publications": publications,
        "latest_writing": latest_writing,
    }

    new_readme = render_readme(context)
    existing = README_PATH.read_text() if README_PATH.exists() else ""

    if new_readme != existing:
        README_PATH.write_text(new_readme)
        logger.info("README.md updated with new content")
    else:
        logger.info("No content changes detected; README left as is")

    save_cache(CACHE_PATH, cache)


if __name__ == "__main__":
    main()
