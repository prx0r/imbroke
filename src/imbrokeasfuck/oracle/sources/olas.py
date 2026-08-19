"""Olas Mech Marketplace adapter — agent-to-agent services."""
from __future__ import annotations
import httpx
from typing import Any
from ..opportunity import Opportunity

TIMEOUT = httpx.Timeout(15.0)


async def discover_olas_mechs() -> list[Opportunity]:
    """Discover services on Olas Mech Marketplace."""
    opps = []
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as c:
            r = await c.get("https://api.olas.network/v1/mechs", params={"limit": 20})
            if r.status_code == 200:
                data = r.json()
                mechs = data.get("mechs", data.get("results", []))
                if isinstance(mechs, list):
                    for mech in mechs[:20]:
                        opps.append(Opportunity(
                            kind="service",
                            title=f"Olas: {mech.get('name', mech.get('service_id', ''))[:80]}",
                            sponsor="Olas",
            discovered_at="",
                            reward_type="recurring_revenue",
                            source="olas",
                            source_url="https://olas.network/mech-marketplace",
                            source_data=mech if isinstance(mech, dict) else {},
                            rating="B",
                            reuse_score=0.5,
                            recommendation="MONITOR",
                        ))
    except Exception:
        pass
    return opps
