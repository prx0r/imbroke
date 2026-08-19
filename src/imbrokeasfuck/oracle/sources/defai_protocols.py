"""DeFAI infrastructure adapters — Bitte, Wayfinder, DeBank, PropellerHeads."""
from __future__ import annotations
import httpx
from typing import Any
from ..opportunity import Opportunity

TIMEOUT = httpx.Timeout(15.0)

DEFAI_PROTOCOLS = [
    {"name": "Bitte/Amadeus", "url": "https://thegrid.id", "focus": "conversational agent hub", "token": "AMA"},
    {"name": "Wayfinder Protocol", "url": "https://wayfinder.ai", "focus": "omnichain intent mapping", "token": "PROMPT"},
    {"name": "DeBank Cloud API", "url": "https://debank.com", "focus": "portfolio/whale tracking", "token": None},
    {"name": "PropellerHeads", "url": "https://www.propellerheads.xyz", "focus": "solver infrastructure", "token": None},
]

async def fetch_defai_protocols() -> list:
    """Fetch DeFAI protocol opportunities."""
    opps = []
    for p in DEFAI_PROTOCOLS:
        opps.append(Opportunity(
            kind="protocol",
            title=f"DeFAI: {p['name']} ({p['focus']})",
            sponsor=p["name"],
            discovered_at="",
            source="defai_protocols",
            source_url=p["url"],
            rating="B",
            reuse_score=0.3,
            recommendation="MONITOR",
        ))
    return opps
