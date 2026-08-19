"""Virtuals ACP adapter — agent service marketplace."""
from __future__ import annotations
import httpx
from typing import Any
from ..opportunity import Opportunity

TIMEOUT = httpx.Timeout(15.0)


async def discover_virtuals_services() -> list[Opportunity]:
    """Discover services on Virtuals ACP."""
    opps = []
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as c:
            r = await c.get("https://api.virtuals.io/agents", params={"limit": 20})
            if r.status_code == 200:
                data = r.json()
                if isinstance(data, list):
                    for agent in data[:20]:
                        opps.append(Opportunity(
                            kind="service",
                            title=f"Virtuals: {agent.get('name', '')[:80]}",
                            sponsor="Virtuals",
                            reward_type="recurring_revenue",
                            source="virtuals",
                            source_url=f"https://virtuals.io/agent/{agent.get('id', '')}",
                            source_data=agent if isinstance(agent, dict) else {},
                            rating="B",
                            reuse_score=0.5,
                            recommendation="MONITOR",
                        ))
    except Exception:
        pass
    return opps
