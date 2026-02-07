"""Fetch repository data from GitHub REST API."""

import os
import requests
from typing import List, Dict

GITHUB_API_BASE = "https://api.github.com"


def fetch_repo_data(username: str) -> List[Dict]:
    headers = {"Accept": "application/vnd.github.v3+json"}
    token = os.environ.get("GITHUB_TOKEN", "")
    if token:
        headers["Authorization"] = f"token {token}"

    repos = []
    page = 1
    while True:
        response = requests.get(
            f"{GITHUB_API_BASE}/users/{username}/repos",
            headers=headers,
            params={"type": "public", "sort": "updated", "direction": "desc",
                    "per_page": 100, "page": page},
            timeout=10,
        )
        response.raise_for_status()
        batch = response.json()
        if not batch:
            break
        repos.extend(batch)
        page += 1

    return repos
