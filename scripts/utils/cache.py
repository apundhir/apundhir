"""Simple JSON file cache for resilience against API failures."""

import json
from pathlib import Path
from typing import Dict, Any


def load_cache(cache_path: Path) -> Dict[str, Any]:
    if cache_path.exists():
        try:
            with open(cache_path, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    return {}


def save_cache(cache_path: Path, data: Dict[str, Any]) -> None:
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    with open(cache_path, "w") as f:
        json.dump(data, f, indent=2, default=str)
