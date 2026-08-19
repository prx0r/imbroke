"""Apify store adapter — sell capabilities as Actors."""
from __future__ import annotations
import httpx
from typing import Any
from ..opportunity import Opportunity

TIMEOUT = httpx.Timeout(15.0)


async def discover_apify_actors() -> list[Opportunity]:
    """Discover agent-callable Actors on Apify."""
    opps = []
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as c:
            r = await c.get("https://api.apify.com/v2/store", params={
                "allowsAgenticUsers": "true",
                "limit": 20,
            })
            if r.status_code == 200:
                data = r.json()
                items = data.get("data", {}).get("items", [])
                for actor in items[:20]:
                    opps.append(Opportunity(
                        kind="service",
                        title=f"Apify: {actor.get('name', '')[:80]}",
                        sponsor=actor.get("username", ""),
            discovered_at="",
                        reward_type="recurring_revenue",
                        source="apify",
                        source_url=actor.get("url", ""),
                        source_data=actor if isinstance(actor, dict) else {},
                        rating="B",
                        reuse_score=0.5,
                        recommendation="MONITOR",
                    ))
    except Exception:
        pass
    return opps
