"""Feed ingestion — normalize all sources into Opportunities."""
from __future__ import annotations
import asyncio
import httpx
from typing import Any
from .opportunity import (
    Opportunity, HACKATHON_SOURCES, BOUNTY_SOURCES, GRANT_SOURCES,
    classify_reward, estimate_qdw_fit,
)
from .github_signals import scan_all_github_signals, signal_to_opportunity
from .bittensor_economics import SUBNET_CONTRACTS
from .sources.algora import fetch_algora_bounties
from .sources.x402 import discover_x402_services
from .sources.tether import fetch_tether_bounties
from .sources.near import fetch_near_funding
from .sources.apify import discover_apify_actors
from .sources.virtuals import discover_virtuals_services
from .sources.heurist import discover_heurist_services
from .sources.olas import discover_olas_mechs
from .sources.hackathons_space import fetch_hackathons_space

TIMEOUT = httpx.Timeout(15.0)


async def fetch_superteam_live(tao_price: float = 0.0) -> list[Opportunity]:
    """Fetch live Superteam bounties."""
    opps = []
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as c:
            r = await c.get("https://superteam.fun/api/agents/listings/live")
            if r.status_code == 200:
                data = r.json()
                if isinstance(data, list):
                    for item in data[:20]:
                        title = item.get("title", item.get("name", ""))
                        desc = item.get("description", item.get("body", ""))
                        reward = item.get("reward", item.get("compensation", ""))
                        opps.append(Opportunity(
                            kind="bounty",
                            title=title[:100],
                            sponsor="Superteam",
                            discovered_at=item.get("createdAt", ""),
                            deadline=item.get("deadline"),
                            reward_type="cash",
                            reward_confidence=0.8,
                            source="superteam",
                            source_url=item.get("url", "https://superteam.fun/earn/agents"),
                            source_data=item if isinstance(item, dict) else {},
                            rating="A",
                            reuse_score=0.7,
                            recommendation="INVESTIGATE",
                        ))
    except Exception:
        pass
    return opps


async def fetch_hackernoon_hackathons() -> list[Opportunity]:
    """Fetch HackerNoon hackathon RSS."""
    opps = []
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as c:
            r = await c.get("https://hackernoon.com/tagged/hackathon/feed")
            if r.status_code == 200:
                # Simple XML parsing for RSS
                content = r.text
                import re
                titles = re.findall(r"<title><!\[CDATA\[(.*?)\]\]></title>", content)
                links = re.findall(r"<link>(.*?)</link>", content)
                for i, title in enumerate(titles[:10]):
                    opps.append(Opportunity(
                        kind="hackathon",
                        title=title[:100],
                        sponsor="HackerNoon",
                        source="hackernoon",
                        source_url=links[i] if i < len(links) else "",
                        rating="B",
                        reuse_score=0.5,
                        recommendation="MONITOR",
                    ))
    except Exception:
        pass
    return opps


async def fetch_devfolio_hackathons() -> list[Opportunity]:
    """Fetch Devfolio hackathons."""
    opps = []
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as c:
            r = await c.get("https://ses.devfolio.co/api/hackathons")
            if r.status_code == 200:
                data = r.json()
                if isinstance(data, dict) and "hackathons" in data:
                    for h in data["hackathons"][:15]:
                        opps.append(Opportunity(
                            kind="hackathon",
                            title=h.get("name", "")[:100],
                            sponsor=h.get("organization", {}).get("name", "Unknown"),
                            opens_at=h.get("start_date"),
                            deadline=h.get("end_date"),
                            source="devfolio",
                            source_url=f"https://devfolio.co/hackathons/{h.get('slug', '')}",
                            rating="B",
                            reuse_score=0.5,
                            recommendation="MONITOR",
                        ))
    except Exception:
        pass
    return opps


async def fetch_ethglobal_events() -> list[Opportunity]:
    """Fetch ETHGlobal events."""
    opps = []
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as c:
            r = await c.get("https://ethglobal.com/api/events")
            if r.status_code == 200:
                data = r.json()
                if isinstance(data, list):
                    for e in data[:10]:
                        opps.append(Opportunity(
                            kind="hackathon",
                            title=e.get("name", "")[:100],
                            sponsor="ETHGlobal",
                            opens_at=e.get("start_date"),
                            deadline=e.get("end_date"),
                            source="ethglobal",
                            source_url=f"https://ethglobal.com/events/{e.get('slug', '')}",
                            rating="B",
                            reuse_score=0.5,
                            recommendation="MONITOR",
                        ))
    except Exception:
        pass
    return opps


async def fetch_bittensor_subnets(tao_price: float) -> list[Opportunity]:
    """Convert known subnet contracts to Opportunities."""
    opps = []
    for netuid, contract in SUBNET_CONTRACTS.items():
        opps.append(Opportunity(
            kind="subnet",
            title=f"SN{netuid} {contract.name}: {contract.artifact_type}",
            sponsor=contract.name,
            discovered_at="",
            reward_type="token_emission",
            amount_min_usd=contract.submission_cost_tao * tao_price * -1 if contract.submission_cost_tao else 0,
            amount_max_usd=contract.miner_pool_tao_day * tao_price,
            reward_confidence=0.7 if contract.miner_pool_tao_day else 0.3,
            artifact_type=contract.artifact_type,
            hardware=f"{contract.ram_gb}GB RAM" if contract.ram_gb else None,
            ip_assignment=contract.submission_ip_terms,
            submission_fee=f"{contract.submission_cost_tao} TAO" if contract.submission_cost_tao else None,
            reuse_score=contract.qdw_reuse_score,
            estimated_engineering_hours=20 if contract.qdw_reuse_score > 0.8 else 40,
            local_evaluator_available=contract.evaluator_local_reproducible,
            factory_candidate=contract.name.lower(),
            existing_assets=contract.qdw_existing_assets,
            cash_at_risk=contract.submission_cost_tao * tao_price,
            expected_value_confidence="MEDIUM" if contract.miner_pool_tao_day else "LOW",
            paying_slots=contract.paying_slots,
            source="bittensor_research",
            source_url=contract.github,
            source_data=contract.to_dict(),
            rating="A" if contract.qdw_reuse_score > 0.85 else "B" if contract.qdw_reuse_score > 0.6 else "C",
            recommendation=contract.recommendation,
        ))
    return opps


async def ingest_all(tao_price: float = 190.0) -> dict[str, Any]:
    """Ingest from all sources and return unified opportunity feed."""
    tasks = [
        fetch_superteam_live(tao_price),
        fetch_hackernoon_hackathons(),
        fetch_devfolio_hackathons(),
        fetch_ethglobal_events(),
        fetch_bittensor_subnets(tao_price),
        scan_all_github_signals(),
        fetch_algora_bounties(),
        discover_x402_services(),
        fetch_tether_bounties(),
        fetch_near_funding(),
        discover_apify_actors(),
        discover_virtuals_services(),
        discover_heurist_services(),
        discover_olas_mechs(),
        fetch_hackathons_space(),
    ]

    results = await asyncio.gather(*tasks, return_exceptions=True)

    all_opps = []
    sources_used = set()

    for r in results:
        if isinstance(r, list):
            for item in r:
                if isinstance(item, Opportunity):
                    all_opps.append(item)
                elif isinstance(item, dict):
                    opp = signal_to_opportunity(item)
                    all_opps.append(item)
                    sources_used.add(item.get("repo", "github"))

    # Dedupe by id
    seen = set()
    unique_opps = []
    for opp in all_opps:
        opp_id = opp.id() if isinstance(opp, Opportunity) else opp.get("id", "")
        if opp_id not in seen:
            seen.add(opp_id)
            unique_opps.append(opp)

    # Sort by rating then reuse_score
    def sort_key(opp):
        if isinstance(opp, Opportunity):
            rating_order = {"A": 0, "B": 1, "C": 2, "REJECT": 3}
            return (rating_order.get(opp.rating, 9), -opp.reuse_score)
        return (9, 0)

    unique_opps.sort(key=sort_key)

    return {
        "total": len(unique_opps),
        "opportunities": [o.to_dict() if isinstance(o, Opportunity) else o for o in unique_opps],
        "sources": list(sources_used),
        "tao_price": tao_price,
    }
