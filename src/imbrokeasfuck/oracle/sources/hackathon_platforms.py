"""Hackathon platform adapters — fetch real hackathons from major platforms."""
from __future__ import annotations
import httpx
from typing import Any
from ..opportunity import Opportunity

TIMEOUT = httpx.Timeout(15.0)


async def fetch_devpost() -> list:
    """Fetch from Devpost API."""
    opps = []
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as c:
            r = await c.get("https://devpost.com/api/hackathons", params={"status": "open"})
            if r.status_code == 200:
                for h in r.json()[:10]:
                    opps.append(Opportunity(
                        kind="hackathon",
                        title=f"Devpost: {h.get('name', '')[:80]}",
                        sponsor="Devpost",
                        discovered_at="",
                        deadline=h.get("submission_unix_timestamp", ""),
                        reward_type="cash",
                        source="devpost",
                        source_url=h.get("url", "https://devpost.com/hackathons"),
                        rating="B",
                        reuse_score=0.4,
                        recommendation="MONITOR",
                    ))
    except Exception:
        pass
    return opps


async def fetch_devfolio() -> list:
    """Fetch from Devfolio API."""
    opps = []
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as c:
            r = await c.get("https://devfolio.co/api/hackathons")
            if r.status_code == 200:
                data = r.json()
                hackathons = data.get("hackathons", data) if isinstance(data, dict) else data
                for h in (hackathons if isinstance(hackathons, list) else [])[:10]:
                    opps.append(Opportunity(
                        kind="hackathon",
                        title=f"Devfolio: {h.get('name', '')[:80]}",
                        sponsor="Devfolio",
                        discovered_at="",
                        deadline=h.get("end_date", h.get("deadline", "")),
                        reward_type="cash",
                        source="devfolio",
                        source_url=h.get("url", "https://devfolio.co/explore"),
                        rating="B",
                        reuse_score=0.5,
                        recommendation="MONITOR",
                    ))
    except Exception:
        pass
    return opps


async def fetch_hackerone() -> list:
    """Fetch HackerOne bug bounties."""
    opps = []
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as c:
            r = await c.get("https://hackerone.com/directory/hacktivity")
            if r.status_code == 200:
                opps.append(Opportunity(
                    kind="bounty",
                    title="HackerOne: Security bounties",
                    sponsor="HackerOne",
                    discovered_at="",
                    source="hackerone",
                    source_url="https://hackerone.com/directory/hacktivity",
                    rating="A",
                    reuse_score=0.3,
                    recommendation="MONITOR",
                ))
    except Exception:
        pass
    return opps


async def fetch_all_hackathon_platforms() -> list:
    """Fetch from all major hackathon platforms."""
    opps = []
    opps.extend(await fetch_devpost())
    opps.extend(await fetch_devfolio())
    opps.extend(await fetch_hackerone())
    return opps
