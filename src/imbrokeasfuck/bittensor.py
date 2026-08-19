"""Bittensor subnet data and opportunity tracker."""
from __future__ import annotations
import httpx
from typing import Any

TIMEOUT = httpx.Timeout(15.0)

# ── TAO.app API (unofficial, public) ──────────────────────────────────────

async def tao_subnet_info(netuid: int) -> dict[str, Any]:
    """Fetch subnet info from TAO.app."""
    async with httpx.AsyncClient(timeout=TIMEOUT) as c:
        r = await c.get(f"https://www.tao.app/api/subnets/{netuid}")
        if r.status_code == 200:
            return r.json()
        return {}

async def tao_all_subnets() -> list[dict[str, Any]]:
    """Fetch all subnet data."""
    async with httpx.AsyncClient(timeout=TIMEOUT) as c:
        r = await c.get("https://www.tao.app/api/subnets")
        if r.status_code == 200:
            return r.json()
        return []

async def tao_price() -> float:
    """Get current TAO price from DefiLlama."""
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as c:
            r = await c.get("https://coins.llama.fi/prices/current/coingecko:bittensor")
            if r.status_code == 200:
                data = r.json()
                coins = data.get("coins", {})
                return coins.get("coingecko:bittensor", {}).get("price", 0.0)
    except Exception:
        pass
    return 0.0

# ── Bittensor subnet registry ─────────────────────────────────────────────

BITTENSOR_SUBNETS = {
    118: {
        "name": "Ditto",
        "slug": "ditto",
        "description": "Agent-memory harness — submit Docker artifact, validators run it",
        "emission_pct": 0.0,
        "miner_reward": "top 5 paid (65/14/10/7/4)",
        "cost_per_eval": "0.04 TAO (~$8)",
        "gpu_required": False,
        "qdw_fit": "memory/context",
        "rank": 1,
        "leaderboard": "~65 submissions, top composites 0.955, 0.944, 0.918, 0.910",
        "github": "https://github.com/ditto-assistant/ditto-subnet",
        "status": "active",
        "strategy": "Build QDW factory: memory bridge → context compilation → hashed handovers → Ditto harness variants → local eval → only then pay 0.04 TAO",
    },
    11: {
        "name": "TrajectoryRL",
        "slug": "trajectoryrl",
        "description": "Open skill factory — SKILL.md packs tested in real sandboxes",
        "emission_pct": 0.47,
        "miner_reward": "winner-take-all",
        "cost_per_eval": "50 α (~0.44 TAO ~$90)",
        "gpu_required": False,
        "qdw_fit": "GitGoblin + skill factory",
        "rank": 2,
        "terms": "Copyright transfers on reward-earning win",
        "github": "https://github.com/trajectoryRL/trajectoryRL",
        "status": "active",
        "strategy": "Run 500 local mutations, pay once for genuine frontier improvement. 249/256 miners but only 1 earning.",
    },
    62: {
        "name": "Ridges",
        "slug": "ridges",
        "description": "Autonomous SWE agent — submit agent.py, validators throw real problems",
        "emission_pct": 1.29,
        "miner_reward": "winner-take-all",
        "cost_per_eval": "low–medium (own provider for local testing)",
        "gpu_required": False,
        "qdw_fit": "autonomous coding",
        "rank": 3,
        "terms": "IP irrevocably assigned to Hidden Harvest Ventures",
        "upload_credits": "Available from Ridges team",
        "github": "https://github.com/ridgesai/ridges",
        "status": "active",
        "strategy": "Isolate submission — QDW core stays yours, generated agent.py is disposable",
    },
    61: {
        "name": "RedTeam",
        "slug": "redteam",
        "description": "Rotating authorized programming/security challenges",
        "emission_pct": 0.59,
        "miner_reward": "proportional",
        "cost_per_eval": "cheap VPS",
        "gpu_required": "8GB server",
        "qdw_fit": "experiment/search",
        "rank": 4,
        "allocation": "41% miners, 41% validators, 18% owner",
        "docs": "https://docs.theredteam.io",
        "status": "active",
        "strategy": "Challenge spec → auto-evaluator → candidate generation → mutation → regression test → submit",
    },
    15: {
        "name": "ORO",
        "slug": "oro",
        "description": "Shopping agent evaluation on real commerce tasks",
        "emission_pct": 0.0,
        "miner_reward": "king-of-hill",
        "cost_per_eval": "higher inference spend",
        "gpu_required": False,
        "qdw_fit": "agent evolution",
        "rank": 5,
        "status": "monitor",
    },
    60: {
        "name": "BitSec",
        "slug": "bitsec",
        "description": "Vulnerability-finding AI agent benchmark",
        "emission_pct": 0.01,
        "miner_reward": "winner-take-all",
        "cost_per_eval": "API inference + local testing",
        "gpu_required": False,
        "qdw_fit": "security research",
        "rank": 13,
        "leaderboard": "Agent 3030 at 16.7% (Aug 9, 2026)",
        "docs": "https://docs.bitsec.ai",
        "status": "active",
        "strategy": "Study winning agents → reproduce → enter when expected reward > inference cost. $30/day current emissions.",
    },
    34: {
        "name": "BitMind/GAS",
        "slug": "bitmind",
        "description": "AI-generated-content detection — submit models, rewarded by accuracy",
        "emission_pct": 0.0,
        "miner_reward": "accuracy-based",
        "cost_per_eval": "low",
        "gpu_required": False,
        "qdw_fit": "model research automation",
        "rank": 15,
        "github": "https://github.com/BitMind-AI/bitmind-subnet",
        "status": "active",
    },
}

# ── Grant programs ─────────────────────────────────────────────────────────

GRANTS = {
    "nosana": {
        "name": "Nosana Grants",
        "amount": "$5K–$50K + compute",
        "review_time": "~2 weeks",
        "eligible": "AI infrastructure, tooling, orchestration, agents, decentralized compute",
        "url": "https://nosana.com/grants/",
        "rank": 1,
        "status": "year-round",
        "proposal": "Decentralized-compute observatory (Akash + Nosana + Chutes + others)",
    },
    "akash": {
        "name": "Akash Ecosystem Grants",
        "amount": "Ecosystem grant",
        "eligible": "Open-source tools, infrastructure, specialized interfaces",
        "url": "https://akash.network/development/funding-program/",
        "rank": 2,
        "status": "open",
        "proposal": "Akash adapter + neutral compute comparison/probing layer",
    },
    "heurist": {
        "name": "Heurist Developer Program",
        "amount": "2K–10K free credits",
        "eligible": "Agent/inference applications",
        "url": "https://sdk.heurist.ai",
        "rank": 3,
        "status": "open",
    },
    "litvm": {
        "name": "LitVM Builders",
        "amount": "Testnet prizes + post-mainnet grants",
        "eligible": "AI apps/agents, dev tooling",
        "url": "https://builders.litvm.com",
        "rank": 4,
        "status": "testnet live",
        "proposal": "QDW Forge for LitVM — verified machine-to-machine capabilities/payments",
    },
    "vana": {
        "name": "Vana Grants",
        "amount": "Rolling data grants",
        "eligible": "Data rights, agent context infrastructure",
        "url": "https://vana.org/participate",
        "rank": 5,
        "status": "rolling",
        "proposal": "DataRightsBackend/LifeGit → data-rights/agent-context infrastructure",
    },
    "arweave": {
        "name": "Arweave/AO Onboard",
        "amount": "$1.5K–$10K credits",
        "eligible": "Storage/compute infrastructure",
        "url": "https://onboard.arweave.net",
        "rank": 6,
        "status": "open",
    },
}

# ── Bounty platforms ───────────────────────────────────────────────────────

BOUNTY_PLATFORMS = {
    "superteam": {
        "name": "Superteam Earn",
        "description": "Agent-eligible bounties with autonomous agent API",
        "url": "https://superteam.fun/earn/agents",
        "rank": 1,
        "features": ["AGENT_ALLOWED listings", "AGENT_ONLY work", "human payout claiming"],
        "example": "Zeroclaw Solana plugin — $5,000 USDG pool ($1.8K/$1.2K/$1K + bonuses)",
    },
    "tether": {
        "name": "Tether.dev Developer Grants",
        "description": "Specific deliverables, $1.5K–$5K per task",
        "url": "https://tether.io",
        "rank": 2,
        "current_tasks": ["5,000 USD₮ llama.cpp/CoreML/QVAC", "3,000 USD₮ Swift SDK"],
    },
    "risein": {
        "name": "RiseIn",
        "description": "300+ opportunities, $1.1M in open rewards",
        "url": "https://www.risein.com/earn",
        "rank": 3,
    },
}


async def fetch_bittensor_data() -> dict[str, Any]:
    """Fetch live Bittensor data."""
    price = 0.0
    try:
        price = await tao_price()
    except Exception:
        pass

    subnets = {}
    for netuid, info in BITTENSOR_SUBNETS.items():
        subnets[str(netuid)] = {
            **info,
            "tao_price": price,
        }

    return {
        "tao_price": price,
        "subnets": subnets,
        "daily_emissions": 3600,
        "halving_date": "2025-12",
    }


def format_opportunities(data: dict[str, Any]) -> str:
    lines = []
    lines.append("=" * 70)
    lines.append("  IMBROKEASFK — Opportunity Radar")
    lines.append("=" * 70)

    tao = data.get("tao_price", 0)
    lines.append(f"\n  TAO: ${tao:.2f}")
    lines.append(f"  Daily emissions: {data.get('daily_emissions', 3600)} TAO")
    lines.append("")

    lines.append("  BITTENSOR SUBNETS (ranked)")
    lines.append("  " + "-" * 66)
    for netuid, info in sorted(data.get("subnets", {}).items(), key=lambda x: x[1].get("rank", 99)):
        rank = info.get("rank", "?")
        name = info.get("name", "")
        slug = info.get("slug", "")
        emission = info.get("emission_pct", 0)
        reward = info.get("miner_reward", "")
        gpu = "GPU" if info.get("gpu_required") else "No GPU"
        fit = info.get("qdw_fit", "")
        lines.append(f"  #{rank:<3} SN{netuid:<4} {name:<15} {emission:>5.2f}% emit  {reward:<20} {gpu}")
        lines.append(f"       {fit}")
        terms = info.get("terms")
        if terms:
            lines.append(f"       ⚠ {terms}")
        lines.append("")

    lines.append("  GRANT PROGRAMS")
    lines.append("  " + "-" * 66)
    for key, g in sorted(GRANTS.items(), key=lambda x: x[1].get("rank", 99)):
        lines.append(f"  #{g['rank']:<3} {g['name']:<25} {g['amount']:<20} {g['status']}")
        lines.append(f"       {g['eligible']}")
        lines.append("")

    lines.append("  BOUNTY PLATFORMS")
    lines.append("  " + "-" * 66)
    for key, b in sorted(BOUNTY_PLATFORMS.items(), key=lambda x: x[1].get("rank", 99)):
        lines.append(f"  #{b['rank']:<3} {b['name']:<25} {b['description'][:50]}")
        lines.append("")

    lines.append("=" * 70)
    return "\n".join(lines)
