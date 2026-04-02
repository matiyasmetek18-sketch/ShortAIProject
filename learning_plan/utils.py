from __future__ import annotations

import re
from html import unescape
from urllib.parse import parse_qs, quote_plus, unquote, urlparse


def clean_text(text: str) -> str:
    text = unescape(text or "")
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def slugify_company(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", name.lower())


def normalize_space(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def decode_duckduckgo_url(url: str) -> str:
    if "duckduckgo.com/l/" not in url:
        return url
    parsed = urlparse(url)
    query = parse_qs(parsed.query)
    target = query.get("uddg", [url])[0]
    return unquote(target)


def make_search_url(query: str) -> str:
    return f"https://duckduckgo.com/html/?q={quote_plus(query)}"
