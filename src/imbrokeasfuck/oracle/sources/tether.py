"""Tether.dev adapter — fixed engineering deliverables."""
from __future__ import annotations
import httpx
from typing import Any
from ..opportunity import Opportunity, estimate_qdw_fit

TIMEOUT = httpx.Timeout(15.0)


async def fetch_tether_bounties() -> list[Opportunity]:
    """Fetch Tether developer grant tasks."""
    opps = []
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as c:
            r = await c.get("https://tether.dev")
            if r.status_code == 200:
                content = r.text.lower()
                # Extract task patterns
                import re
                amounts = re.findall(r'(\d[\d,]*)\s*(?:USD[₮]|USDT|USD)', content)
                tasks = re.findall(r'(?:task|bounty|grant)[^<]*?(\d[\d,]*)\s*(?:USD[₮]|USDT|USD)[^<]*?([^\n<]{20,80})', content, re.IGNORECASE)

                for amount_str, desc in tasks[:5]:
                    amount = float(amount_str.replace(",", ""))
                    opps.append(Opportunity(
                        kind="deliverable",
                        title=f"Tether: {desc.strip()[:80]}",
                        sponsor="Tether",
                        reward_type="cash",
                        amount_min_usd=amount,
                        amount_max_usd=amount,
                        reward_confidence=0.7,
                        artifact_type="code_library",
                        source="tether",
                        source_url="https://tether.dev",
                        rating="A",
                        reuse_score=estimate_qdw_fit(desc, "", "deliverable"),
                        recommendation="INVESTIGATE",
                    ))
    except Exception:
        pass
    return opps
