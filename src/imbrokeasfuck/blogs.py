"""Blog monitoring — RSS feeds + web scrapers for new opportunities."""
from __future__ import annotations
import sqlite3
import json
import re
from datetime import datetime
from typing import Any
import urllib.request
import xml.etree.ElementTree as ET

from .canonical_db import connect


BLOG_FEEDS = {
    "bittensor_blog": "https://bittensor.com/blog/feed.xml",
    "superteam": "https://superteam.substack.com/feed",
    "algora_blog": "https://algora.io/blog/rss",
    "virtuals_blog": "https://virtuals.io/blog/feed",
}


def fetch_rss(feed_url: str) -> list[dict]:
    """Fetch RSS feed and extract entries."""
    try:
        req = urllib.request.Request(feed_url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            xml_data = resp.read().decode()
        root = ET.fromstring(xml_data)
        items = []
        for item in root.findall(".//item")[:10]:
            title = item.findtext("title", "")
            link = item.findtext("link", "")
            pub_date = item.findtext("pubDate", "")
            items.append({"title": title, "url": link, "published": pub_date})
        return items
    except Exception as e:
        return [{"error": str(e)}]


def scan_opportunities(text: str) -> list[dict]:
    """Extract opportunity signals from text."""
    patterns = [
        (r"(\d[\d,]*)\s*(?:USD|USDC|USDT|\$)", "prize"),
        (r"bounty", "bounty"),
        (r"grant", "grant"),
        (r"hackathon", "hackathon"),
        (r"deadline", "deadline"),
        (r"submit", "submission"),
    ]
    signals = []
    for pattern, sig_type in patterns:
        if re.search(pattern, text, re.IGNORECASE):
            signals.append({"type": sig_type, "text": text[:100]})
    return signals


def monitor_blogs() -> list[dict]:
    """Scan all blog feeds for new opportunities."""
    conn = connect()
    new_items = []

    for feed_name, feed_url in BLOG_FEEDS.items():
        entries = fetch_rss(feed_url)
        for entry in entries:
            if "error" in entry:
                continue

            # Check if we've seen this URL
            existing = conn.execute(
                "SELECT 1 FROM events WHERE new_value LIKE ?",
                (f"%{entry['url']}%",)
            ).fetchone()

            if not existing and entry["url"]:
                # Scan for opportunity signals
                signals = scan_opportunities(entry["title"])
                if signals:
                    new_items.append({
                        "source": feed_name,
                        "title": entry["title"],
                        "url": entry["url"],
                        "signals": signals,
                    })
                    # Record event
                    conn.execute(
                        "INSERT INTO events (opportunity_id, event_type, new_value, created_at) VALUES (?, ?, ?, ?)",
                        (feed_name, "blog_scan", json.dumps(entry, default=str), datetime.now().isoformat())
                    )

    conn.commit()
    conn.close()
    return new_items
