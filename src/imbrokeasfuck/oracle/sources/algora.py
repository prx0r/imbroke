"""Algora API adapter — paid OSS bounties."""
from __future__ import annotations
import httpx
from typing import Any
from ..opportunity import Opportunity, classify_reward, estimate_qdw_fit

TIMEOUT = httpx.Timeout(15.0)
ALGORA_API = "https://api.algora.io/v1"


async def fetch_algora_bounties() -> list[Opportunity]:
    """Fetch bounties from Algora API."""
    opps = []
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as c:
            r = await c.get(f"{ALGORA_API}/bounties", params={"status": "open", "limit": 50})
            if r.status_code == 200:
                data = r.json()
                if isinstance(data, list):
                    for b in data:
                        title = b.get("title", "")
                        desc = b.get("description", "")
                        repo = b.get("repo", {})
                        reward = b.get("reward_amount")
                        currency = b.get("reward_currency", "USD")

                        opps.append(Opportunity(
                            kind="bounty",
                            title=f"{repo.get('full_name', '')}: {title}"[:100],
                            sponsor=repo.get("owner", ""),
            discovered_at="",
                            deadline=b.get("deadline"),
                            reward_type="cash",
                            amount_max_usd=float(reward) if reward else None,
                            reward_confidence=0.8,
                            artifact_type="pull_request",
                            open_source_required=True,
                            source="algora",
                            source_url=b.get("html_url", ""),
                            source_data=b if isinstance(b, dict) else {},
                            rating="A",
                            reuse_score=estimate_qdw_fit(title, desc, "bounty"),
                            recommendation="INVESTIGATE",
                        ))
    except Exception:
        pass
    return opps
