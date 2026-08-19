"""NEAR funding adapter — grants + protocol rewards."""
from __future__ import annotations
import httpx
from typing import Any
from ..opportunity import Opportunity, estimate_qdw_fit

TIMEOUT = httpx.Timeout(15.0)


async def fetch_near_funding() -> list[Opportunity]:
    """Fetch NEAR ecosystem funding opportunities."""
    opps = []
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as c:
            r = await c.get("https://gov.near.org/latest.json")
            if r.status_code == 200:
                data = r.json()
                topics = data.get("topic_list", {}).get("topics", [])
                for t in topics[:15]:
                    title = t.get("title", "")
                    if any(kw in title.lower() for kw in ["grant", "funding", "reward", "bounty", "builder"]):
                        opps.append(Opportunity(
                            kind="grant",
                            title=f"NEAR: {title[:80]}",
                            sponsor="NEAR",
                            source="near_gov",
                            source_url=f"https://gov.near.org/t/{t.get('slug', '')}",
                            rating="B",
                            reuse_score=estimate_qdw_fit(title, "", "grant"),
                            recommendation="MONITOR",
                        ))
    except Exception:
        pass
    return opps
