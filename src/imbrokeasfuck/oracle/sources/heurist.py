"""Heurist Mesh adapter — specialist agent services."""
from __future__ import annotations
import httpx
from typing import Any
from ..opportunity import Opportunity

TIMEOUT = httpx.Timeout(15.0)


async def discover_heurist_services() -> list[Opportunity]:
    """Discover services on Heurist Mesh."""
    opps = []
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as c:
            r = await c.get("https://mesh.heurist.ai/metadata.json")
            if r.status_code == 200:
                data = r.json()
                agents = data.get("agents", data.get("tools", []))
                if isinstance(agents, list):
                    for agent in agents[:20]:
                        opps.append(Opportunity(
                            kind="service",
                            title=f"Heurist: {agent.get('name', agent.get('tool_name', ''))[:80]}",
                            sponsor="Heurist",
            discovered_at="",
                            reward_type="recurring_revenue",
                            source="heurist",
                            source_url="https://mesh.heurist.ai",
                            source_data=agent if isinstance(agent, dict) else {},
                            rating="B",
                            reuse_score=0.5,
                            recommendation="MONITOR",
                        ))
    except Exception:
        pass
    return opps
