"""x402 Bazaar discovery — payable HTTP services."""
from __future__ import annotations
import httpx
from typing import Any
from ..opportunity import Opportunity

TIMEOUT = httpx.Timeout(15.0)
CDP_BAZAAR = "https://api.cdp.coinbase.com/platform/v2/x402/discovery"


async def discover_x402_services(query: str = "") -> list[Opportunity]:
    """Discover payable services on x402 Bazaar."""
    opps = []
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as c:
            params = {"limit": 50}
            if query:
                params["q"] = query
            r = await c.get(f"{CDP_BAZAAR}/resources", params=params)
            if r.status_code == 200:
                data = r.json()
                if isinstance(data, dict) and "resources" in data:
                    for svc in data["resources"][:30]:
                        opps.append(Opportunity(
                            kind="service",
                            title=svc.get("name", svc.get("description", ""))[:100],
                            sponsor=svc.get("merchant", "unknown"),
                            reward_type="recurring_revenue",
                            source="x402_bazaar",
                            source_url=svc.get("url", ""),
                            source_data=svc if isinstance(svc, dict) else {},
                            rating="B",
                            reuse_score=0.5,
                            recommendation="MONITOR",
                        ))
    except Exception:
        pass
    return opps
