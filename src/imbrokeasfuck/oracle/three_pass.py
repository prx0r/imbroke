"""3-Pass Validator — verify key opportunity data from multiple sources."""
from __future__ import annotations
import asyncio
import httpx
import hashlib
from datetime import datetime
from typing import Any
from dataclasses import dataclass, field


async def check_url(url: str, term: str) -> dict:
    try:
        r = httpx.get(url, timeout=10, follow_redirects=True)
        return {"live": r.status_code < 400, "found": term.lower() in r.text.lower()}
    except:
        return {"live": False, "found": False}


KEY_FACTS = [
    {"fact": "OpenAIRE grand prize: €500", "sources": [
        {"name": "hackathon_page", "url": "https://innovation.openaire.eu/component/content/article/openaire-ai-hackathon.html", "term": "500 euros"},
        {"name": "submission_template", "url": "https://docs.google.com/document/d/13dKS8ir8YonmLUVggLCdxy0bEVlCkx2P/edit", "term": "500"},
    ]},
    {"fact": "Hack Hydra prize: $5,000", "sources": [
        {"name": "hackathons_space", "url": "https://www.hackathons.space/hackathons/hack-hydra-the-hydradb-open-source-hackathon", "term": "$5,000"},
        {"name": "luma", "url": "https://luma.com/h038glzk", "term": "5,000"},
    ]},
    {"fact": "Ditto eval fee: 0.04 TAO", "sources": [
        {"name": "ditto_docs", "url": "https://raw.githubusercontent.com/ditto-assistant/ditto-subnet/main/docs/MINER.md", "term": "0.04 TAO"},
    ]},
    {"fact": "OpenAIRE deadline: 23:59", "sources": [
        {"name": "hackathon_page", "url": "https://innovation.openaire.eu/component/content/article/openaire-ai-hackathon.html", "term": "23:59"},
        {"name": "faq", "url": "https://innovation.openaire.eu/component/content/article/faqs.html?catid=8", "term": "23:59"},
    ]},
    {"fact": "Hack Hydra deadline: 11:59 PM", "sources": [
        {"name": "hackathons_space", "url": "https://www.hackathons.space/hackathons/hack-hydra-the-hydradb-open-source-hackathon", "term": "11:59 PM"},
    ]},
    {"fact": "TAO price ~$192", "sources": [
        {"name": "defillama", "url": "https://coins.llama.fi/prices/current/coingecko:bittensor", "term": "price"},
    ]},
    {"fact": "OpenAIRE has 386M+ entities", "sources": [
        {"name": "api", "url": "https://api.openaire.eu/graph/v3/research-products?pageSize=1", "term": "numFound"},
    ]},
    {"fact": "Fear and Greed: 46", "sources": [
        {"name": "alternative_me", "url": "https://api.alternative.me/fng/?limit=1", "term": "46"},
    ]},
]


async def check_source(src: dict) -> dict:
    try:
        r = httpx.get(src["url"], timeout=10, follow_redirects=True)
        return {"live": r.status_code < 400, "found": src["term"].lower() in r.text.lower()}
    except:
        return {"live": False, "found": False}


async def main():
    print("=" * 60)
    print("  3-PASS VALIDATION")
    print("=" * 60)
    results = []
    for f in KEY_FACTS:
        checks = []
        for src in f["sources"]:
            c = await check_source(src)
            checks.append({"name": src["name"], **c})
        confirmed = sum(1 for c in checks if c["live"] and c["found"])
        status = "VERIFIED" if confirmed >= 2 else "SINGLE" if confirmed == 1 else "UNVERIFIED"
        results.append({"fact": f["fact"], "status": status, "confirmed": confirmed, "total": len(checks)})
        icon = "✅" if status == "VERIFIED" else "⚠️"
        print(f"  {icon} {f['fact']}: {status} ({confirmed}/{len(checks)})")
    
    ok = sum(1 for r in results if r["status"] == "VERIFIED")
    single = sum(1 for r in results if r["status"] == "SINGLE")
    print(f"\n  {ok} verified, {single} single-source, {len(results)-ok-single} unverified")
    print(f"{'='*60}")


if __name__ == "__main__":
    asyncio.run(main())
