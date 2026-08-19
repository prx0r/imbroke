"""Bug bounty adapter — Immunefi, Sherlock, Code4rena, HackenProof."""
from __future__ import annotations
import httpx
from typing import Any
from ..opportunity import Opportunity

TIMEOUT = httpx.Timeout(15.0)

BUG_BOUNTY_PLATFORMS = [
    {"name": "Immunefi", "url": "https://immunefi.com", "focus": "Web3 DeFi security"},
    {"name": "Sherlock", "url": "https://sherlock.xyz", "focus": "smart contract audits"},
    {"name": "Code4rena", "url": "https://code4rena.com", "focus": "competitive auditing"},
    {"name": "HackenProof", "url": "https://hackenproof.com", "focus": "crowdsourced bugs"},
]

async def fetch_bug_bounties() -> list[Opportunity]:
    opps = []
    for p in BUG_BOUNTY_PLATFORMS:
        opps.append(Opportunity(
            kind="bounty",
            title=f"Security: {p['name']}",
            sponsor=p["name"],
            discovered_at="",
            reward_type="cash",
            source="bug_bounties",
            source_url=p["url"],
            rating="A",
            reuse_score=0.3,
            recommendation="MONITOR",
        ))
    return opps
