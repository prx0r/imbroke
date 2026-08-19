"""Fetch and display project data."""
from __future__ import annotations
import asyncio
from typing import Any
from .apis import (
    defillama_tvl, defillama_fees, fear_greed, coingecko_price,
    PROJECTS, BITTENSOR_SUBNETS,
)

async def fetch_project(slug: str, proj: dict[str, Any], all_prices: dict | None = None) -> dict[str, Any]:
    result = {
        "slug": slug,
        "name": proj["name"],
        "token": proj.get("token"),
        "category": proj.get("category"),
        "tvl": None,
        "revenue_30d": None,
        "price": None,
        "market_cap": None,
        "change_24h": None,
    }

    # DefiLlama TVL
    if "defillama" in proj:
        try:
            result["tvl"] = await defillama_tvl(proj["defillama"])
        except Exception:
            pass

    # CoinGecko price (from pre-fetched batch)
    if proj.get("token") and all_prices:
        data = all_prices.get(proj["token"], {})
        result["price"] = data.get("usd")
        result["market_cap"] = data.get("usd_market_cap")
        result["change_24h"] = data.get("usd_24h_change")

    return result


async def fetch_all() -> dict[str, Any]:
    # First, fetch all CoinGecko prices in one batch
    token_ids = []
    slug_to_token = {}
    for slug, proj in PROJECTS.items():
        if proj.get("token"):
            token_ids.append(proj["token"])
            slug_to_token[slug] = proj["token"]

    all_prices = {}
    try:
        all_prices = await coingecko_price(list(set(token_ids)))
    except Exception:
        pass

    # Then fetch per-project data (DefiLlama TVL etc)
    tasks = [fetch_project(slug, proj, all_prices) for slug, proj in PROJECTS.items()]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    projects = {}
    for r in results:
        if isinstance(r, dict):
            projects[r["slug"]] = r

    fg = []
    try:
        fg = await fear_greed(1)
    except Exception:
        pass

    fear_greed_data = fg[0] if fg else None

    return {
        "fear_greed": fear_greed_data,
        "projects": projects,
    }


def format_report(data: dict[str, Any]) -> str:
    lines = []
    lines.append("=" * 60)
    lines.append("  IMBROKEASFK — Crypto AI Tracker")
    lines.append("=" * 60)

    fg = data.get("fear_greed")
    if fg:
        lines.append(f"\n  Fear & Greed: {fg.get('value', '?')} ({fg.get('value_classification', '?')})")
    else:
        lines.append("\n  Fear & Greed: unavailable")

    lines.append("")
    lines.append(f"  {'Project':<20} {'Token':<8} {'Price':>10} {'24h':>8} {'MCap':>15} {'TVL':>15}")
    lines.append("  " + "-" * 76)

    for slug, p in sorted(data.get("projects", {}).items()):
        name = p.get("name", slug)[:20]
        token = (p.get("token") or "")[:8]
        price = f"${p['price']:,.4f}" if p.get("price") else "—"
        change = f"{p['change_24h']:+.1f}%" if p.get("change_24h") else "—"
        mcap = f"${p['market_cap']:,.0f}" if p.get("market_cap") else "—"
        tvl = f"${p['tvl']:,.0f}" if p.get("tvl") else "—"
        lines.append(f"  {name:<20} {token:<8} {price:>10} {change:>8} {mcap:>15} {tvl:>15}")

    lines.append("\n" + "=" * 60)
    return "\n".join(lines)
