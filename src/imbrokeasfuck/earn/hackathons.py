"""Hackathon targets — what to submit and when."""
from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Any, Optional


@dataclass
class HackathonTarget:
    name: str
    organizer: str
    deadline: str
    prize_pool: str
    url: str
    status: str = "open"  # open|closed|upcoming

    # What to submit
    submission_name: str = ""
    submission_description: str = ""
    reuse_percentage: float = 0.0  # how much is existing code

    # Categories
    categories: list[str] = field(default_factory=list)

    # Eligibility
    eligibility: str = "open"
    existing_projects_allowed: bool = True
    team_allowed: bool = True

    # Reuse policy
    prior_art_policy: str = ""  # EXCLUDE_SAME_COMPETITION|ALLOWED
    must_build_during_event: bool = False
    license_requirements: list[str] = field(default_factory=list)

    # Reuse breakdown
    reuse_breakdown: dict[str, float] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


HACKATHONS = {
    "telegraph": HackathonTarget(
        name="Telegraph Hackathon",
        organizer="Telegraph",
        deadline="2026-09-07",
        prize_pool="$5,000",
        url="https://telegraph",
        categories=["verifiable intelligence", "knowledge APIs", "evaluators"],
        submission_name="Patala Miner — provenance-backed scholarly intelligence",
        submission_description="Wrap Wiggly as a Miner providing verifiable intelligence with canonical entity resolution, append-only provenance, assertions with evidence, and machine-verifiable state.",
        reuse_percentage=0.85,
        reuse_breakdown={"wiggly": 0.70, "qdw_memory": 0.15, "new_ui": 0.15},
        existing_projects_allowed=True,
        prior_art_policy="EXCLUDE_SAME_COMPETITION",
        license_requirements=["open source"],
    ),
    "decentralize_ai": HackathonTarget(
        name="Decentralize AI",
        organizer="HackerNoon",
        deadline="2026-10-31",
        prize_pool="varies",
        url="https://decentralizeai.tech",
        categories=["decentralized GPU orchestration", "verifiable AI", "open inference", "permanent storage"],
        submission_name="OpenPatala Permanent Scholarly Memory",
        submission_description="A provenance protocol for AI-generated and human scholarly claims with Arweave permanent evidence.",
        reuse_percentage=0.80,
        reuse_breakdown={"wiggly": 0.55, "qdw_proof": 0.30, "arweave": 0.10, "new_ui": 0.05},
        existing_projects_allowed=True,
        prior_art_policy="ALLOWED",
        license_requirements=["open source"],
    ),
    "openaire": HackathonTarget(
        name="OpenAIRE AI Hackathon",
        organizer="OpenAIRE",
        deadline="2026-08-20",
        prize_pool="credits + exposure",
        url="https://innovation.openaire.eu",
        categories=["Theme B: Build", "Theme C: Analyse"],
        submission_name="OpenAIRE Research Graph Auditor",
        submission_description="Reconstruct scholarly lineage while showing exactly where every author/work/institution/funding assertion came from.",
        reuse_percentage=0.75,
        reuse_breakdown={"wiggly": 0.60, "openaire_adapter": 0.15, "new_analysis": 0.25},
        existing_projects_allowed=True,
        prior_art_policy="ALLOWED",
        license_requirements=["CC-BY"],
    ),
    "hack_hydra": HackathonTarget(
        name="Hack Hydra",
        organizer="HydraDB",
        deadline="2026-08-20",
        prize_pool="$5,000",
        url="https://www.hackathons.space/hackathons/hack-hydra-the-hydradb-open-source-hackathon",
        categories=["graph infrastructure", "agent memory", "context retrieval", "knowledge systems"],
        submission_name="Patala-on-Hydra — provenance-aware long-term memory",
        submission_description="Provenance-aware long-term memory where agents distinguish evidence, assertions and interpretations.",
        reuse_percentage=0.70,
        reuse_breakdown={"wiggly": 0.50, "qdw_memory": 0.20, "hydra_adapter": 0.20, "new_ui": 0.10},
        existing_projects_allowed=True,
        prior_art_policy="ALLOWED",
        license_requirements=["open source"],
    ),
}


def format_hackathons() -> str:
    lines = []
    lines.append("=" * 70)
    lines.append("  HACKATHON TARGETS — Wiggly as reusable kernel")
    lines.append("=" * 70)
    lines.append("")

    for key, h in HACKATHONS.items():
        status_icon = "🟢" if h.status == "open" else "🔴"
        lines.append(f"  {status_icon} {h.name}")
        lines.append(f"     Deadline: {h.deadline} | Prize: {h.prize_pool}")
        lines.append(f"     Submit: {h.submission_name}")
        lines.append(f"     Reuse: {h.reuse_percentage:.0%}")
        for k, v in h.reuse_breakdown.items():
            lines.append(f"       {k}: {v:.0%}")
        lines.append(f"     Categories: {', '.join(h.categories)}")
        lines.append("")

    lines.append("  " + "=" * 66)
    lines.append("  Wiggly is a provenance/knowledge-state kernel, not one submission.")
    lines.append("  Adapt to different sponsor problems.")
    lines.append("  " + "=" * 66)
    return "\n".join(lines)


def hackathon_dict() -> dict[str, Any]:
    return {k: v.to_dict() for k, v in HACKATHONS.items()}

# Add additional hackathons found
HACKATHONS["0g_wavehack"] = HackathonTarget(
    name="0G WaveHack Buildathon",
    organizer="0G",
    deadline="2026-09-15",
    prize_pool="$50,000 grant",
    url="https://0g.ai",
    categories=["AI infrastructure", "decentralized compute", "agent tooling"],
    submission_name="0G Compute Adapter for Dell",
    submission_description="Integrate 0G Compute into Dell's decentralized compute observatory.",
    reuse_percentage=0.60,
    existing_projects_allowed=True,
    prior_art_policy="ALLOWED",
)

HACKATHONS["lukso"] = HackathonTarget(
    name="LUKSO Final Hackathon",
    organizer="LUKSO",
    deadline="2026-09-30",
    prize_pool="$150,000",
    url="https://luksо.com",
    categories=["gasless accounts", "programmable accounts", "web3 tooling"],
    submission_name="TBD — evaluate fit",
    submission_description="LUKSO's final hackathon round for gasless programmable accounts.",
    reuse_percentage=0.30,
    existing_projects_allowed=True,
    prior_art_policy="ALLOWED",
)

HACKATHONS["cronos_x402"] = HackathonTarget(
    name="Cronos x402 PayTech Hackathon",
    organizer="Cronos",
    deadline="2026-09-15",
    prize_pool="TBD",
    url="https://cronos.org",
    categories=["x402 payments", "agent payments", "AI infrastructure"],
    submission_name="x402 Payment Adapter",
    submission_description="Can AI agents pay each other? Build x402 payment infrastructure.",
    reuse_percentage=0.50,
    existing_projects_allowed=True,
    prior_art_policy="ALLOWED",
)
