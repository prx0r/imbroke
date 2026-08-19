"""QDW Earn Strategy — 60/25/15 allocation."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


@dataclass
class StrategyLane:
    name: str
    allocation_pct: float
    description: str
    primary_target: str
    status: str = "active"
    key_metrics: dict[str, Any] = field(default_factory=dict)


STRATEGY = {
    "bittensor": StrategyLane(
        name="Bittensor",
        allocation_pct=60,
        description="Build reusable CompetitionFactory, attack Ditto SN118 first",
        primary_target="SN118 Ditto — memory harness, 0.04 TAO/eval, 5 paying slots",
        key_metrics={
            "factory": "bittensor-118",
            "artifact": "docker_memory_harness",
            "daily_pool": "34.16 TAO/day",
            "reward_distribution": "65/14/10/7/4",
            "local_evaluator": True,
            "gpu_required": False,
            "submission_cost": "0.04 TAO ($7.80)",
            "target": "continuous evolutionary improvement → top-5 position",
        },
    ),
    "hackathon": StrategyLane(
        name="Decentralize AI Hackathon",
        allocation_pct=25,
        description="Dell Compute Observatory — same infrastructure, different packaging",
        primary_target="Decentralize AI (deadline: Oct 31, 2026)",
        key_metrics={
            "submission": "Dell Compute Observatory / Compute Radar",
            "categories": [
                "decentralized GPU orchestration",
                "verifiable/reproducible AI",
                "open inference infrastructure",
                "permanent storage/provenance",
            ],
            "integrations": ["Nosana", "Akash", "Bittensor", "Arweave"],
            "prize": "first 500 participants get $70 Nosana credits",
            "judge_note": "solve real problem, make decentralized infra materially useful",
        },
    ),
    "superteam": StrategyLane(
        name="Superteam Earn",
        allocation_pct=15,
        description="Continuous bounty feed — boring cashflow attempts",
        primary_target="Agent-eligible bounties with high code reuse",
        key_metrics={
            "api": "https://superteam.fun/api/agents/listings/live",
            "approach": "poll → score → build if reuse > 0.8 → human gate → submit",
            "rule": "only pursue listings with very high code reuse",
        },
    ),
}


def format_strategy() -> str:
    lines = []
    lines.append("=" * 70)
    lines.append("  QDW EARN STRATEGY — 60/25/15")
    lines.append("=" * 70)
    lines.append("")

    for key, lane in STRATEGY.items():
        bar = "█" * int(lane.allocation_pct / 5) + "░" * (20 - int(lane.allocation_pct / 5))
        lines.append(f"  {lane.allocation_pct:>3}% {bar} {lane.name}")
        lines.append(f"       {lane.description}")
        lines.append(f"       Target: {lane.primary_target}")
        for k, v in lane.key_metrics.items():
            if isinstance(v, list):
                lines.append(f"       {k}: {', '.join(v)}")
            else:
                lines.append(f"       {k}: {v}")
        lines.append("")

    lines.append("  " + "=" * 66)
    lines.append("  One development programme, multiple ways to get paid.")
    lines.append("  Bittensor improves core tech even when you lose.")
    lines.append("  Hackathon wraps same infrastructure for different reward.")
    lines.append("  Superteam runs continuously in background.")
    lines.append("  " + "=" * 66)
    return "\n".join(lines)


def strategy_dict() -> dict[str, Any]:
    return {k: {
        "allocation": f"{v.allocation_pct}%",
        "description": v.description,
        "target": v.primary_target,
        "metrics": v.key_metrics,
    } for k, v in STRATEGY.items()}
