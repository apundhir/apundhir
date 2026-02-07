#!/usr/bin/env python3
"""
Auto-update GitHub profile README.
Fetches dynamic content, merges with config, renders template.
"""

import sys
import yaml
import json
import os
from datetime import datetime, timezone, timedelta
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

# Ensure the project root is on the path for imports
ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.fetchers.rss_fetcher import fetch_rss_feed
from scripts.fetchers.github_fetcher import fetch_repo_data
from scripts.fetchers.seniorexec_scraper import fetch_senior_exec_articles
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


def fetch_blog_posts(config):
    """Fetch blog posts from all configured RSS feeds, sorted by priority."""
    posts = []
    cache = load_cache(CACHE_PATH)

    for feed_name, feed_config in sorted(
        config.get("rss_feeds", {}).items(),
        key=lambda x: x[1].get("priority", 99)
    ):
        try:
            feed_posts = fetch_rss_feed(
                url=feed_config["url"],
                max_items=feed_config.get("max_items", 5),
                source_label=feed_config.get("label", feed_name)
            )
            posts.extend(feed_posts)
            logger.info(f"Fetched {len(feed_posts)} posts from {feed_name}")
        except Exception as e:
            logger.warning(f"Failed to fetch {feed_name}: {e}")
            cached = cache.get(f"blog_{feed_name}", [])
            posts.extend(cached)

    # Deduplicate by URL, sort by date descending
    seen = set()
    unique_posts = []
    for p in sorted(posts, key=lambda x: x.get("date", ""), reverse=True):
        if p["url"] not in seen:
            seen.add(p["url"])
            unique_posts.append(p)

    return unique_posts[:7]


def fetch_external_publications(config):
    """Fetch articles from scrapers (Senior Executive, etc.)."""
    articles = []
    cache = load_cache(CACHE_PATH)

    for scraper_name, scraper_config in config.get("scrapers", {}).items():
        if not scraper_config.get("enabled", False):
            continue

        if scraper_name == "senior_executive":
            try:
                scraped = fetch_senior_exec_articles(
                    profile_url=scraper_config["url"],
                    max_items=scraper_config.get("max_items", 5),
                    source_label=scraper_config.get("label", "Senior Executive")
                )
                articles.extend(scraped)
                logger.info(f"Scraped {len(scraped)} articles from Senior Executive")
            except Exception as e:
                logger.warning(f"Senior Executive scraper failed: {e}")
                articles.extend(cache.get("scraper_senior_executive", []))

    return articles


def enrich_repos(config):
    """Enrich featured_repos from config with live GitHub API data."""
    github_username = "apundhir"
    enriched = []

    try:
        all_repos = fetch_repo_data(github_username)
        repo_map = {r["name"]: r for r in all_repos}
        logger.info(f"Fetched {len(all_repos)} repos from GitHub API")
    except Exception as e:
        logger.warning(f"GitHub API failed: {e}")
        repo_map = {}

    for repo_config in config.get("featured_repos", []):
        repo_name = repo_config["name"]
        github_data = repo_map.get(repo_name, {})

        enriched.append({
            "name": repo_name,
            "display_name": repo_config.get("display_name", repo_name),
            "tagline": repo_config["tagline"],
            "stars": github_data.get("stargazers_count", ""),
            "language": github_data.get("language", ""),
            "url": f"https://github.com/{github_username}/{repo_name}",
        })

    return enriched


def format_publication_date(date_str):
    """Convert 2026-01-20 to Jan 2026."""
    if not date_str:
        return ""
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        return dt.strftime("%b %Y")
    except ValueError:
        return date_str


def render_readme(context):
    env = Environment(
        loader=FileSystemLoader(str(ROOT)),
        keep_trailing_newline=True
    )
    template = env.get_template("TEMPLATE.md")
    return template.render(**context)


def main():
    logger.info("Starting README update...")

    config = load_config()
    blog_posts = fetch_blog_posts(config)
    external_pubs = fetch_external_publications(config)
    featured_repos = enrich_repos(config)

    # Merge external publications into manual publications
    all_publications = config.get("publications", [])
    for pub in all_publications:
        pub["date_formatted"] = format_publication_date(pub.get("date", ""))

    dubai_tz = timezone(timedelta(hours=4))
    context = {
        "name": config["name"],
        "title": config["title"],
        "tagline": config["tagline"],
        "mission_statement": config["mission_statement"],
        "philosophy": config.get("philosophy", []),
        "credentials": config.get("credentials", []),
        "currently_exploring": config["currently_exploring"],
        "links": config["links"],
        "impact": config["impact"],
        "speaking": config["speaking"],
        "connect_text": config["connect_text"],
        "aiexponent_tagline": config.get("aiexponent_tagline", ""),
        "signature_quote": config.get("signature_quote", ""),
        "settings": config["settings"],
        "publications": all_publications,
        "blog_posts": blog_posts,
        "featured_repos": featured_repos,
        "last_updated": datetime.now(dubai_tz).strftime("%B %d, %Y at %I:%M %p GST"),
    }

    new_readme = render_readme(context)

    existing = ""
    if README_PATH.exists():
        existing = README_PATH.read_text()

    def strip_timestamp(text):
        return "\n".join(
            line for line in text.split("\n")
            if "auto-updated on" not in line
        )

    if strip_timestamp(new_readme) != strip_timestamp(existing):
        README_PATH.write_text(new_readme)
        logger.info("README.md updated with new content")

        save_cache(CACHE_PATH, {
            "blog_aiexponent": [p for p in blog_posts if p.get("source") == "AiExponent"],
            "blog_medium": [p for p in blog_posts if p.get("source") == "Medium"],
            "scraper_senior_executive": external_pubs,
            "last_successful_fetch": datetime.now(dubai_tz).isoformat(),
        })
    else:
        logger.info("No content changes detected — skipping write")


if __name__ == "__main__":
    main()
