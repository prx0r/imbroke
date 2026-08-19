"""Real polling — fetches live data from sources."""
from __future__ import annotations
import sqlite3
import json
from datetime import datetime
from typing import Any

from .canonical_db import connect


def poll_bittensor() -> list[dict]:
    """Poll Bittensor subnet data from CoinGecko API."""
    import urllib.request
    try:
        req = urllib.request.Request(
            "https://api.coingecko.com/api/v3/simple/price?ids=bittensor&vs_currencies=usd",
            headers={"User-Agent": "Mozilla/5.0"}
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
            price = data.get("bittensor", {}).get("usd", 0)
            return [{"type": "price", "asset": "TAO", "price_usd": price, "timestamp": datetime.now().isoformat()}]
    except Exception as e:
        return [{"type": "error", "source": "bittensor", "error": str(e)}]


def poll_fear_greed() -> list[dict]:
    """Poll Fear & Greed Index."""
    import urllib.request
    try:
        req = urllib.request.Request(
            "https://api.alternative.me/fng/?limit=1",
            headers={"User-Agent": "Mozilla/5.0"}
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
            item = data.get("data", [{}])[0]
            return [{"type": "fear_greed", "value": int(item.get("value", 50)), "classification": item.get("value_classification", ""), "timestamp": datetime.now().isoformat()}]
    except Exception as e:
        return [{"type": "error", "source": "fear_greed", "error": str(e)}]


def poll_algora() -> list[dict]:
    """Poll Algora bounties."""
    import urllib.request
    try:
        req = urllib.request.Request(
            "https://api.algora.io/v1/bounties?status=open&limit=10",
            headers={"User-Agent": "Mozilla/5.0"}
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
            return [{"type": "bounty", "source": "algora", "title": b.get("title", ""), "prize": b.get("prize", ""), "url": b.get("url", "")} for b in data.get("bounties", [])]
    except Exception as e:
        return [{"type": "error", "source": "algora", "error": str(e)}]


def poll_x402() -> list[dict]:
    """Poll x402 bounties."""
    import urllib.request
    try:
        req = urllib.request.Request(
            "https://api.x402.org/v1/bounties?limit=10",
            headers={"User-Agent": "Mozilla/5.0"}
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
            return [{"type": "bounty", "source": "x402", "title": b.get("title", ""), "prize": b.get("prize", "")} for b in data.get("bounties", [])]
    except Exception as e:
        return [{"type": "error", "source": "x402", "error": str(e)}]


def poll_all_sources() -> dict:
    """Poll all registered sources and record observations."""
    conn = connect()
    results = {}

    sources = {
        "bittensor": poll_bittensor,
        "fear_greed": poll_fear_greed,
        "algora": poll_algora,
        "x402": poll_x402,
    }

    for source_id, poll_fn in sources.items():
        try:
            observations = poll_fn()
            results[source_id] = observations

            # Record observations in events
            for obs in observations:
                if obs.get("type") != "error":
                    conn.execute(
                        "INSERT INTO events (opportunity_id, event_type, new_value, created_at) VALUES (?, ?, ?, ?)",
                        (source_id, "poll", json.dumps(obs, default=str), datetime.now().isoformat())
                    )

            # Update last_polled
            conn.execute(
                "UPDATE sources SET last_polled = ? WHERE source_id = ?",
                (datetime.now().isoformat(), source_id)
            )

        except Exception as e:
            results[source_id] = [{"type": "error", "error": str(e)}]

    conn.commit()
    conn.close()
    return results
