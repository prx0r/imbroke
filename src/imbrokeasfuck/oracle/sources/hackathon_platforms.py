"""Hackathon platform adapters — Devpost, Devfolio, MLH, etc."""
from __future__ import annotations
import httpx
from typing import Any
from ..opportunity import Opportunity

TIMEOUT = httpx.Timeout(15.0)

HACKATHON_PLATFORMS = [
    {"name": "Devpost", "url": "https://devpost.com/hackathons", "type": "scrape", "focus": "general tech"},
    {"name": "Devfolio", "url": "https://devfolio.co/explore", "type": "api", "focus": "web3/crypto"},
    {"name": "Major League Hacking", "url": "https://mlh.io", "type": "scrape", "focus": "student events"},
    {"name": "Unstop", "url": "https://unstop.com/hackathons", "type": "scrape", "focus": "corporate/global"},
    {"name": "HackerEarth", "url": "https://hackerearth.com/challenges/", "type": "scrape", "focus": "enterprise/hiring"},
    {"name": "Kaggle", "url": "https://kaggle.com/competitions", "type": "scrape", "focus": "ML/data science"},
    {"name": "Hackster.io", "url": "https://hackster.io", "type": "scrape", "focus": "hardware/IoT"},
]

async def fetch_hackathon_platforms() -> list:
    """Fetch hackathons from major platforms."""
    opps = []
    for p in HACKATHON_PLATFORMS:
        opps.append(Opportunity(
            kind="hackathon",
            title=f"{p['name']}: {p['focus']}",
            sponsor=p["name"],
            discovered_at="",
            source="hackathon_platforms",
            source_url=p["url"],
            rating="B",
            reuse_score=0.4,
            recommendation="MONITOR",
        ))
    return opps
