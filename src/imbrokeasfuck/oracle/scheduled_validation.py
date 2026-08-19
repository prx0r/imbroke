#!/usr/bin/env python3
"""Scheduled validator — run via Hermes cron to verify opportunity data."""
import asyncio
import json
import httpx
from datetime import datetime

async def validate_opportunities():
    """Validate all core opportunity data."""
    results = []
    
    # 1. Check deadlines
    deadlines = [
        ("OpenAIRE", "2026-08-20T23:59:00+02:00"),
        ("Hack Hydra", "2026-08-21T06:59:00+00:00"),
    ]
    for name, dl in deadlines:
        d = datetime.fromisoformat(dl)
        days = (d - datetime.now(d.tzinfo)).days
        results.append({
            "check": f"deadline_{name}",
            "status": "OK" if days > 0 else "EXPIRED",
            "days_remaining": days,
        })
    
    # 2. Check URLs are live
    urls = [
        ("OpenAIRE", "https://innovation.openaire.eu/component/content/article/openaire-ai-hackathon.html"),
        ("Hack Hydra", "https://www.hackathons.space/hackathons/hack-hydra-the-hydradb-open-source-hackathon"),
        ("Ditto", "https://bittensor.ai/subnets/118"),
        ("HydraDB", "https://hydradb.com"),
    ]
    async with httpx.AsyncClient(timeout=10) as c:
        for name, url in urls:
            try:
                r = await c.get(url, follow_redirects=True)
                results.append({
                    "check": f"url_{name}",
                    "status": "OK" if r.status_code < 400 else f"HTTP_{r.status_code}",
                    "url": url,
                })
            except Exception as e:
                results.append({
                    "check": f"url_{name}",
                    "status": "ERROR",
                    "error": str(e)[:50],
                })
    
    # 3. Check TAO price
    try:
        async with httpx.AsyncClient(timeout=10) as c:
            r = await c.get("https://coins.llama.fi/prices/current/coingecko:bittensor")
            data = r.json()
            price = data.get("coins", {}).get("coingecko:bittensor", {}).get("price", 0)
            results.append({
                "check": "tao_price",
                "status": "OK",
                "price": f"${price:.2f}",
            })
    except Exception as e:
        results.append({"check": "tao_price", "status": "ERROR", "error": str(e)[:50]})
    
    # 4. Check OpenAIRE entities
    try:
        async with httpx.AsyncClient(timeout=10) as c:
            r = await c.get("https://api.openaire.eu/graph/v3/research-products?pageSize=1")
            data = r.json()
            count = data.get("header", {}).get("numFound", 0)
            results.append({
                "check": "openaire_entities",
                "status": "OK",
                "count": f"{count:,}",
            })
    except Exception as e:
        results.append({"check": "openaire_entities", "status": "ERROR", "error": str(e)[:50]})
    
    # 5. Check Fear & Greed
    try:
        async with httpx.AsyncClient(timeout=10) as c:
            r = await c.get("https://api.alternative.me/fng/?limit=1")
            data = r.json()
            fg = data["data"][0]
            results.append({
                "check": "fear_greed",
                "status": "OK",
                "value": fg["value"],
                "classification": fg["value_classification"],
            })
    except Exception as e:
        results.append({"check": "fear_greed", "status": "ERROR", "error": str(e)[:50]})
    
    return results

async def main():
    print(f"[{datetime.now().isoformat()}] Running validation...")
    results = await validate_opportunities()
    
    ok = sum(1 for r in results if r["status"] == "OK")
    errors = sum(1 for r in results if r["status"] in ("ERROR", "EXPIRED"))
    
    print(f"Results: {ok} OK, {errors} errors")
    for r in results:
        icon = "✅" if r["status"] == "OK" else "⚠️"
        print(f"  {icon} {r['check']}: {r['status']}")
    
    # Save results
    with open("/home/box/imbrokeasfuck/data/validation_results.json", "w") as f:
        json.dump({"timestamp": datetime.now().isoformat(), "results": results}, f, indent=2)
    
    return results

if __name__ == "__main__":
    asyncio.run(main())
