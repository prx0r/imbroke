"""DeFAI hackathon adapter — lablab, DoraHacks, Encode Club, etc."""
from __future__ import annotations
import httpx
from typing import Any
from ..opportunity import Opportunity, estimate_qdw_fit

TIMEOUT = httpx.Timeout(15.0)

async def fetch_defai_hackathons() -> list[Opportunity]:
    """Fetch DeFAI hackathons from multiple sources."""
    opps = []

    # Lablab.ai
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as c:
            r = await c.get("https://lablab.ai/api/hackathons", params={"status": "active"})
            if r.status_code == 200:
                for h in r.json()[:10]:
                    opps.append(Opportunity(
                        kind="hackathon",
                        title=f"Lablab: {h.get('name', '')[:80]}",
                        sponsor="Lablab.ai",
            discovered_at="",
                        deadline=h.get("end_date", ""),
                        reward_type="cash",
                        source="lablab",
                        source_url=h.get("url", "https://lablab.ai/ai-hackathons"),
                        rating="B",
                        reuse_score=0.5,
                        recommendation="MONITOR",
                    ))
    except Exception:
        pass

    # DoraHacks
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as c:
            r = await c.get("https://dorahacks.io/api/hackathons", params={"status": "active"})
            if r.status_code == 200:
                for h in r.json()[:10]:
                    opps.append(Opportunity(
                        kind="hackathon",
                        title=f"DoraHacks: {h.get('title', '')[:80]}",
                        sponsor="DoraHacks",
            discovered_at="",
                        deadline=h.get("end_date", ""),
                        reward_type="cash",
                        reward_confidence=0.7,
                        source="dorahacks",
                        source_url="https://dorahacks.io/hackathon",
                        rating="B",
                        reuse_score=0.5,
                        recommendation="MONITOR",
                    ))
    except Exception:
        pass

    return opps
