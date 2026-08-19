"""Hackathons.space adapter — discover hackathons."""
from __future__ import annotations
import httpx
from typing import Any
from ..oracle.opportunity import Opportunity, estimate_qdw_fit

TIMEOUT = httpx.Timeout(15.0)


async def fetch_hackathons_space() -> list[Opportunity]:
    """Fetch hackathons from hackathons.space."""
    opps = []
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as c:
            r = await c.get("https://www.hackathons.space/api/hackathons")
            if r.status_code == 200:
                data = r.json()
                if isinstance(data, list):
                    for h in data[:20]:
                        title = h.get("name", h.get("title", ""))
                        desc = h.get("description", "")
                        deadline = h.get("end_date", h.get("deadline", ""))
                        prize = h.get("prize_pool", h.get("prize", ""))

                        opps.append(Opportunity(
                            kind="hackathon",
                            title=title[:100],
                            sponsor=h.get("organizer", ""),
                            deadline=deadline,
                            reward_type="cash",
                            reward_confidence=0.7,
                            source="hackathons_space",
                            source_url=h.get("url", ""),
                            source_data=h if isinstance(h, dict) else {},
                            rating="B",
                            reuse_score=estimate_qdw_fit(title, desc, "hackathon"),
                            recommendation="MONITOR",
                        ))
    except Exception:
        pass
    return opps
