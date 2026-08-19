"""Feed ingestion — normalize all sources into Opportunities."""
from __future__ import annotations
import asyncio
import httpx
from typing import Any
from .opportunity import (
    Opportunity, HACKATHON_SOURCES, BOUNTY_SOURCES, GRANT_SOURCES,
    classify_reward, estimate_qdw_fit,
)
from .github_signals import scan_all_github_signals, signal_to_opportunity
from .bittensor_economics import fetch_subnet_economics

TIMEOUT = httpx.Timeout(15.0)


async def fetch_superteam_live(tao_price: float = 0.0) -> list[Opportunity]:
    """Fetch live Superteam bounties."""
    opps = []
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as c:
            r = await c.get("https://superteam.fun/api/agents/listings/live")
            if r.status_code == 200:
                data = r.json()
                if isinstance(data, list):
                    for item in data[:20]:
                        title = item.get("title", item.get("name", ""))
                        desc = item.get("description", item.get("body", ""))
                        reward = item.get("reward", item.get("compensation", ""))
                        opps.append(Opportunity(
                            kind="bounty",
                            title=title[:100],
                            sponsor="Superteam",
                            discovered_at=item.get("createdAt", ""),
                            deadline=item.get("deadline"),
                            reward_type="cash",
                            reward_confidence=0.8,
                            source="superteam",
                            source_url=item.get("url", "https://superteam.fun/earn/agents"),
                            source_data=item if isinstance(item, dict) else {},
                            rating="A",
                            reuse_score=0.7,
                            recommendation="INVESTIGATE",
                        ))
    except Exception:
        pass
    return opps


async def fetch_hackernoon_hackathons() -> list[Opportunity]:
    """Fetch HackerNoon hackathon RSS."""
    opps = []
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as c:
            r = await c.get("https://hackernoon.com/tagged/hackathon/feed")
            if r.status_code == 200:
                # Simple XML parsing for RSS
                content = r.text
                import re
                titles = re.findall(r"<title><!\[CDATA\[(.*?)\]\]></title>", content)
                links = re.findall(r"<link>(.*?)</link>", content)
                for i, title in enumerate(titles[:10]):
                    opps.append(Opportunity(
                        kind="hackathon",
                        title=title[:100],
                        sponsor="HackerNoon",
                        source="hackernoon",
                        source_url=links[i] if i < len(links) else "",
                        rating="B",
                        reuse_score=0.5,
                        recommendation="MONITOR",
                    ))
    except Exception:
        pass
    return opps


async def fetch_devfolio_hackathons() -> list[Opportunity]:
    """Fetch Devfolio hackathons."""
    opps = []
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as c:
            r = await c.get("https://ses.devfolio.co/api/hackathons")
            if r.status_code == 200:
                data = r.json()
                if isinstance(data, dict) and "hackathons" in data:
                    for h in data["hackathons"][:15]:
                        opps.append(Opportunity(
                            kind="hackathon",
                            title=h.get("name", "")[:100],
                            sponsor=h.get("organization", {}).get("name", "Unknown"),
                            opens_at=h.get("start_date"),
                            deadline=h.get("end_date"),
                            source="devfolio",
                            source_url=f"https://devfolio.co/hackathons/{h.get('slug', '')}",
                            rating="B",
                            reuse_score=0.5,
                            recommendation="MONITOR",
                        ))
    except Exception:
        pass
    return opps


async def fetch_ethglobal_events() -> list[Opportunity]:
    """Fetch ETHGlobal events."""
    opps = []
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as c:
            r = await c.get("https://ethglobal.com/api/events")
            if r.status_code == 200:
                data = r.json()
                if isinstance(data, list):
                    for e in data[:10]:
                        opps.append(Opportunity(
                            kind="hackathon",
                            title=e.get("name", "")[:100],
                            sponsor="ETHGlobal",
                            opens_at=e.get("start_date"),
                            deadline=e.get("end_date"),
                            source="ethglobal",
                            source_url=f"https://ethglobal.com/events/{e.get('slug', '')}",
                            rating="B",
                            reuse_score=0.5,
                            recommendation="MONITOR",
                        ))
    except Exception:
        pass
    return opps


async def fetch_bittensor_subnets(tao_price: float) -> list[Opportunity]:
    """Fetch Bittensor subnet data."""
    return await fetch_subnet_economics(tao_price)


async def ingest_all(tao_price: float = 190.0) -> dict[str, Any]:
    """Ingest from all sources and return unified opportunity feed."""
    tasks = [
        fetch_superteam_live(tao_price),
        fetch_hackernoon_hackathons(),
        fetch_devfolio_hackathons(),
        fetch_ethglobal_events(),
        fetch_bittensor_subnets(tao_price),
        scan_all_github_signals(),
    ]

    results = await asyncio.gather(*tasks, return_exceptions=True)

    all_opps = []
    sources_used = set()

    for r in results:
        if isinstance(r, list):
            for item in r:
                if isinstance(item, Opportunity):
                    all_opps.append(item)
                elif isinstance(item, dict):
                    opp = signal_to_opportunity(item)
                    all_opps.append(item)
                    sources_used.add(item.get("repo", "github"))

    # Dedupe by id
    seen = set()
    unique_opps = []
    for opp in all_opps:
        opp_id = opp.id() if isinstance(opp, Opportunity) else opp.get("id", "")
        if opp_id not in seen:
            seen.add(opp_id)
            unique_opps.append(opp)

    # Sort by rating then reuse_score
    def sort_key(opp):
        if isinstance(opp, Opportunity):
            rating_order = {"A": 0, "B": 1, "C": 2, "REJECT": 3}
            return (rating_order.get(opp.rating, 9), -opp.reuse_score)
        return (9, 0)

    unique_opps.sort(key=sort_key)

    return {
        "total": len(unique_opps),
        "opportunities": [o.to_dict() if isinstance(o, Opportunity) else o for o in unique_opps],
        "sources": list(sources_used),
        "tao_price": tao_price,
    }
