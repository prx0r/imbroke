"""Forum monitors — EthResearch, Flashbots, Bittensor governance, etc."""
from __future__ import annotations
import httpx
from typing import Any
from ..opportunity import Opportunity

TIMEOUT = httpx.Timeout(15.0)

FORUMS = [
    {"name": "EthResearch", "url": "https://ethresear.ch", "focus": "L1/L2 research"},
    {"name": "Flashbots", "url": "https://flashbots.net", "focus": "MEV/builders"},
    {"name": "Uniswap Gov", "url": "https://gov.uniswap.org", "focus": "DeFi governance"},
    {"name": "Arbitrum Research", "url": "https://research.arbitrum.io", "focus": "L2/Nitro"},
    {"name": "Optimism Gov", "url": "https://gov.optimism.io", "focus": "OP Stack/RPGF"},
    {"name": "Lambda the Ultimate", "url": "http://lambda-the-ultimate.org", "focus": "PLT/type theory"},
    {"name": "Rust Internals", "url": "https://internals.rust-lang.org", "focus": "compiler/memory"},
    {"name": "Bittensor Gov", "url": "https://forum.bittensor.com", "focus": "subnet governance"},
    {"name": "MCP Community", "url": "https://modelcontextprotocol.io", "focus": "agent data standard"},
    {"name": "Olas/autonolas", "url": "https://olas.network", "focus": "multi-agent coordination"},
    {"name": "elizaOS", "url": "https://github.com/elizaos/eliza", "focus": "agent OS"},
]

async def fetch_forums() -> list:
    """Fetch signals from developer forums."""
    opps = []
    for f in FORUMS:
        opps.append(Opportunity(
            kind="forum_signal",
            title=f"Forum: {f['name']} ({f['focus']})",
            sponsor=f["name"],
            discovered_at="",
            source="forums",
            source_url=f["url"],
            rating="C",
            reuse_score=0.2,
            recommendation="MONITOR",
        ))
    return opps
