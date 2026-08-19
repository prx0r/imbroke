"""API clients for crypto AI project data."""
from __future__ import annotations
import httpx
import asyncio
import time
from typing import Any

TIMEOUT = httpx.Timeout(15.0)
_last_cg_call = 0.0

# ── DefiLlama ──────────────────────────────────────────────────────────────

async def defillama_protocols() -> list[dict[str, Any]]:
    async with httpx.AsyncClient(timeout=TIMEOUT) as c:
        r = await c.get("https://api.llama.fi/protocols")
        r.raise_for_status()
        return r.json()

async def defillama_tvl(slug: str) -> float:
    async with httpx.AsyncClient(timeout=TIMEOUT) as c:
        r = await c.get(f"https://api.llama.fi/tvl/{slug}")
        r.raise_for_status()
        return float(r.json())

async def defillama_fees(protocol: str | None = None) -> Any:
    url = f"https://api.llama.fi/summary/fees/{protocol}" if protocol else "https://api.llama.fi/overview/fees"
    async with httpx.AsyncClient(timeout=TIMEOUT) as c:
        r = await c.get(url)
        r.raise_for_status()
        return r.json()

async def defillama_price(chain: str, address: str) -> dict[str, Any]:
    async with httpx.AsyncClient(timeout=TIMEOUT) as c:
        r = await c.get(f"https://coins.llama.fi/prices/current/{chain}:{address}")
        r.raise_for_status()
        return r.json().get("coins", {}).get(f"{chain}:{address}", {})

# ── Fear & Greed ──────────────────────────────────────────────────────────

async def fear_greed(limit: int = 1) -> list[dict[str, Any]]:
    async with httpx.AsyncClient(timeout=TIMEOUT) as c:
        r = await c.get(f"https://api.alternative.me/fng/?limit={limit}&format=json")
        r.raise_for_status()
        return r.json().get("data", [])

# ── CoinGecko ──────────────────────────────────────────────────────────────

async def coingecko_price(ids: list[str], vs: str = "usd") -> dict[str, Any]:
    global _last_cg_call
    # Rate limit: max 1 request per 1.5s
    elapsed = time.time() - _last_cg_call
    if elapsed < 1.5:
        await asyncio.sleep(1.5 - elapsed)

    async with httpx.AsyncClient(timeout=TIMEOUT) as c:
        for attempt in range(3):
            _last_cg_call = time.time()
            r = await c.get("https://api.coingecko.com/api/v3/simple/price", params={
                "ids": ",".join(ids), "vs_currencies": vs,
                "include_24hr_change": "true", "include_market_cap": "true",
            })
            if r.status_code == 429:
                await asyncio.sleep(2 ** (attempt + 1))
                continue
            r.raise_for_status()
            return r.json()
    return {}

# ── Bittensor ──────────────────────────────────────────────────────────────

BITTENSOR_SUBNETS = {
    64: "chutes",
    28: "gm",
    62: "ridges",
    11: "trajectory-rl",
    15: "oro",
    22: "desearch",
    60: "bitsec",
    87: "provenonce",
    31: "reccall",
}

# ── Project registry ───────────────────────────────────────────────────────

PROJECTS = {
    "chutes": {"name": "Chutes", "subnet": 64, "token": "bittensor", "defillama": "chutes", "category": "inference"},
    "virtuals": {"name": "Virtuals / ACP", "token": "virtuals-protocol", "defillama": "virtuals-protocol", "category": "agent-economy"},
    "olas": {"name": "Olas / Mech", "token": "olas", "defillama": "autonolas", "category": "agent-marketplace"},
    "akash": {"name": "Akash", "token": "akash", "defillama": "akash", "category": "compute", "chain": "cosmos"},
    "venice": {"name": "Venice", "token": "venice-ai", "api": "https://api.venice.ai/api/v1", "category": "inference"},
    "0g": {"name": "0G", "token": "0g-protocol", "category": "compute-storage"},
    "eigen": {"name": "EigenCloud", "token": "eigenlayer", "defillama": "eigenlayer", "category": "verification"},
    "phala": {"name": "Phala", "token": "pha", "defillama": "phala-network", "category": "tee-compute"},
    "lit": {"name": "Lit Protocol", "token": "litentry", "defillama": "lit-protocol", "category": "agent-keys"},
    "aethir": {"name": "Aethir", "token": "aethir", "defillama": "aethir", "category": "gpu-compute"},
    "nosana": {"name": "Nosana", "token": "nosana", "defillama": "nosana", "category": "compute"},
    "ionet": {"name": "io.net", "token": "io-net", "defillama": "ionet", "category": "compute"},
    "openledger": {"name": "OpenLedger", "token": "openledger-network", "category": "provenance"},
    "flock": {"name": "FLock", "token": "flock-ai", "defillama": "flock", "category": "training"},
    "vana": {"name": "Vana", "token": "vana", "defillama": "vana", "category": "data"},
    "sahara": {"name": "Sahara AI", "token": "sahara-ai", "category": "data-marketplace"},
    "arweave": {"name": "Arweave / AO", "token": "arweave", "defillama": "arweave", "category": "storage-compute"},
}
