"""Grant programs adapter — Sentient, Arbitrum, COTI, etc."""
from __future__ import annotations
import httpx
from typing import Any
from ..opportunity import Opportunity

TIMEOUT = httpx.Timeout(15.0)

GRANT_PROGRAMS = [
    {"name": "Sentient Foundation AGI Grants", "amount": "$42M pool", "url": "https://deep-projects.ai", "focus": "open-source AI research"},
    {"name": "Arbitrum Trailblazer AI", "amount": "up to $10K/project", "url": "https://arbitrum.io", "focus": "on-chain AI products"},
    {"name": "COTI Web4 Bootstrap", "amount": "free gas allocation", "url": "https://coti.io", "focus": "agent infrastructure"},
    {"name": "GRIFFAIN Incubation", "amount": "TBD", "url": "https://griffain.com", "focus": "autonomous trading"},
    {"name": "Solidus AITECH Grants", "amount": "compute subsidies", "url": "https://solidusai.tech", "focus": "GPU marketplace"},
    {"name": "Hyperliquid Cortex", "amount": "TBD", "url": "https://hyperliquid.xyz", "focus": "AI copilots for perps"},
]

async def fetch_grants() -> list[Opportunity]:
    """Fetch grant programs."""
    opps = []
    for g in GRANT_PROGRAMS:
        opps.append(Opportunity(
            kind="grant",
            title=g["name"],
            sponsor=g["name"].split()[0],
            discovered_at="",
            reward_type="grant",
            source="grants_research",
            source_url=g["url"],
            rating="B",
            reuse_score=0.4,
            recommendation="MONITOR",
        ))
    return opps
