"""Deadline-aware prioritizer — decides what to work on right now."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
from datetime import datetime, timedelta
import json


@dataclass
class WorkItem:
    id: str
    name: str
    deadline: str  # ISO date
    priority: str  # S|A|B|C
    effort_hours: float
    reuse_score: float  # 0-1
    reward_usd: float
    type: str  # hackathon|bounty|factory|grant
    status: str = "pending"
    dependencies: list[str] = field(default_factory=list)
    notes: str = ""


def days_until(deadline: str) -> int:
    try:
        target = datetime.fromisoformat(deadline).date()
        today = datetime.now().date()
        return (target - today).days
    except Exception:
        return 999


def urgency_score(item: WorkItem) -> float:
    days = days_until(item.deadline)
    if days <= 0:
        return 0.0
    if days <= 2:
        return 1.0
    if days <= 7:
        return 0.8
    if days <= 14:
        return 0.5
    return 0.2


def value_score(item: WorkItem) -> float:
    if item.effort_hours == 0:
        return 0.0
    hourly_rate = item.reward_usd / item.effort_hours
    return min(1.0, hourly_rate / 100.0)  # normalize to 100$/hr


def composite_score(item: WorkItem) -> float:
    u = urgency_score(item)
    v = value_score(item)
    r = item.reuse_score
    priority_weight = {"S": 1.0, "A": 0.8, "B": 0.5, "C": 0.3}.get(item.priority, 0.5)
    return (u * 0.4 + v * 0.3 + r * 0.3) * priority_weight


# ── Current work items ────────────────────────────────────────────────────

WORK_ITEMS = [
    # Aug 20 deadlines (URGENT)
    WorkItem(
        id="openaire",
        name="OpenAIRE Research Graph Auditor",
        deadline="2026-08-20",
        priority="S",
        effort_hours=8,
        reuse_score=0.75,
        reward_usd=0,  # credits/exposure
        type="hackathon",
        notes="Deadline in 1 day. Wiggly scholarly adapters + OpenAIRE adapter. Minimal new code.",
    ),
    WorkItem(
        id="hack_hydra",
        name="Patala-on-Hydra provenance memory",
        deadline="2026-08-20",
        priority="S",
        effort_hours=10,
        reuse_score=0.70,
        reward_usd=5000,
        type="hackathon",
        notes="Deadline in 1 day. Wiggly knowledge graph + HydraDB adapter.",
    ),
    # Sep 7 deadline
    WorkItem(
        id="telegraph",
        name="Telegraph Patala Miner",
        deadline="2026-09-07",
        priority="A",
        effort_hours=15,
        reuse_score=0.85,
        reward_usd=5000,
        type="hackathon",
        notes="2 weeks out. Wiggly provenance-backed intelligence miner.",
    ),
    # Oct 31 deadline (strategic)
    WorkItem(
        id="decentralize_ai",
        name="OpenPatala Permanent Scholarly Memory",
        deadline="2026-10-31",
        priority="A",
        effort_hours=20,
        reuse_score=0.80,
        reward_usd=0,  # varies
        type="hackathon",
        notes="6 weeks out. Same Wiggly kernel + Arweave permanent evidence.",
    ),
    # Bittensor (continuous)
    WorkItem(
        id="ditto_factory",
        name="Ditto SN118 CompetitionFactory",
        deadline="2026-12-31",
        priority="S",
        effort_hours=40,
        reuse_score=0.96,
        reward_usd=7993,  # monthly #5
        type="factory",
        notes="Continuous. Build evolutionary machinery once, use forever.",
    ),
    # Superteam (continuous)
    WorkItem(
        id="superteam_feed",
        name="Superteam Earn bounty feed",
        deadline="2026-12-31",
        priority="B",
        effort_hours=5,
        reuse_score=0.70,
        reward_usd=500,
        type="bounty",
        notes="Background. Only pursue high-reuse listings.",
    ),
]


def prioritize() -> list[dict[str, Any]]:
    """Return work items sorted by priority."""
    items = []
    for item in WORK_ITEMS:
        score = composite_score(item)
        days = days_until(item.deadline)
        items.append({
            "id": item.id,
            "name": item.name,
            "deadline": item.deadline,
            "days_left": days,
            "priority": item.priority,
            "score": round(score, 3),
            "reuse": f"{item.reuse_score:.0%}",
            "effort": f"{item.effort_hours}h",
            "reward": f"${item.reward_usd:,}",
            "type": item.type,
            "status": item.status,
            "notes": item.notes,
            "urgency": round(urgency_score(item), 2),
            "value": round(value_score(item), 2),
        })
    items.sort(key=lambda x: -x["score"])
    return items


def format_priorities() -> str:
    items = prioritize()
    lines = []
    lines.append("=" * 70)
    lines.append("  WHAT TO WORK ON RIGHT NOW — deadline-aware prioritizer")
    lines.append(f"  Today: {datetime.now().strftime('%Y-%m-%d')}")
    lines.append("=" * 70)
    lines.append("")

    for i, item in enumerate(items, 1):
        urgent = " !!!" if item["days_left"] <= 2 else " !" if item["days_left"] <= 7 else ""
        lines.append(f"  #{i} [{item['priority']}] {item['name']}{urgent}")
        lines.append(f"     Deadline: {item['deadline']} ({item['days_left']} days)")
        lines.append(f"     Score: {item['score']} | Reuse: {item['reuse']} | Effort: {item['effort']} | Reward: {item['reward']}")
        lines.append(f"     {item['notes']}")
        lines.append("")

    lines.append("  " + "=" * 66)
    lines.append("  AUG 20 DEADLINES: OpenAIRE + Hack Hydra (1 day left)")
    lines.append("  Focus on these first, then Telegraph (Sep 7), then Ditto (continuous)")
    lines.append("  " + "=" * 66)
    return "\n".join(lines)
