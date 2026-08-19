"""Superteam Earn adapter — agent-compatible bounty discovery."""
from __future__ import annotations
import httpx
from typing import Any, Optional
from ..oracle.opportunity import Opportunity, classify_reward, estimate_qdw_fit

TIMEOUT = httpx.Timeout(15.0)

SUPERTEAM_AGENT_URL = "https://superteam.fun/api/agents/listings/live"
SUPERTEAM_DOCS_URL = "https://superteam.fun/earn/agents"


async def fetch_superteam_agent_listings() -> list[Opportunity]:
    """Fetch agent-compatible listings from Superteam."""
    opportunities = []

    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as c:
            r = await c.get(SUPERTEAM_AGENT_URL)
            if r.status_code != 200:
                return opportunities

            data = r.json()
            if not isinstance(data, list):
                return opportunities

            for item in data[:30]:
                title = item.get("title", item.get("name", ""))
                desc = item.get("description", item.get("body", ""))
                reward = item.get("reward", item.get("compensation", ""))
                deadline = item.get("deadline")
                url = item.get("url", "")

                # Determine kind
                kind = "bounty"
                text = f"{title} {desc}".lower()
                if "grant" in text:
                    kind = "grant"
                elif "hackathon" in text:
                    kind = "hackathon"
                elif "project" in text:
                    kind = "project"

                rating = classify_reward(kind, title, desc)
                fit = estimate_qdw_fit(title, desc, kind)

                # Extract reward amount
                amount_min = None
                amount_max = None
                if isinstance(reward, (int, float)):
                    amount_min = amount_max = float(reward)
                elif isinstance(reward, str):
                    # Try to extract number
                    import re
                    nums = re.findall(r'[\d,]+(?:\.\d+)?', reward.replace(",", ""))
                    if nums:
                        amounts = [float(n) for n in nums]
                        amount_min = min(amounts)
                        amount_max = max(amounts)

                opportunities.append(Opportunity(
                    kind=kind,
                    title=title[:100],
                    sponsor="Superteam",
                    discovered_at=item.get("createdAt", ""),
                    deadline=deadline,
                    reward_type="cash",
                    amount_min_usd=amount_min,
                    amount_max_usd=amount_max,
                    reward_confidence=0.8,
                    source="superteam",
                    source_url=url or SUPERTEAM_DOCS_URL,
                    source_data=item if isinstance(item, dict) else {},
                    rating=rating,
                    reuse_score=fit,
                    estimated_engineering_hours=20 if fit > 0.7 else 40,
                    recommendation="INVESTIGATE" if rating in ("A", "B") and fit > 0.6 else "MONITOR",
                ))

    except Exception:
        pass

    return opportunities


async def check_superteam_api_health() -> dict[str, Any]:
    """Check if Superteam agent API is available."""
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as c:
            r = await c.get(SUPERTEAM_AGENT_URL)
            return {
                "status": "ok" if r.status_code == 200 else "error",
                "status_code": r.status_code,
                "listings_count": len(r.json()) if r.status_code == 200 and isinstance(r.json(), list) else 0,
                "url": SUPERTEAM_AGENT_URL,
            }
    except Exception as e:
        return {"status": "error", "error": str(e), "url": SUPERTEAM_AGENT_URL}
