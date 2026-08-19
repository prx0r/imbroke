"""Wiggly adapter — provenance/knowledge-state kernel for hackathons."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


@dataclass
class WigglyCapability:
    """A reusable capability from Wiggly."""
    name: str
    description: str
    reuse_score: float  # 0-1
    hackathon_fit: dict[str, float] = field(default_factory=dict)  # hackathon -> fit score


WIGGLY_CAPABILITIES = [
    WigglyCapability(
        name="canonical_entity_resolution",
        description="Resolve fragmented entity references across sources",
        reuse_score=0.95,
        hackathon_fit={"telegraph": 0.9, "openaire": 0.95, "hack_hydra": 0.8, "decentralize_ai": 0.7},
    ),
    WigglyCapability(
        name="append_only_provenance",
        description="Immutable history with content-addressed records",
        reuse_score=0.90,
        hackathon_fit={"telegraph": 0.85, "openaire": 0.8, "hack_hydra": 0.9, "decentralize_ai": 0.95},
    ),
    WigglyCapability(
        name="assertions_with_evidence",
        description="Claims backed by source evidence and provenance paths",
        reuse_score=0.92,
        hackathon_fit={"telegraph": 0.95, "openaire": 0.9, "hack_hydra": 0.85, "decentralize_ai": 0.8},
    ),
    WigglyCapability(
        name="machine_verifiable_state",
        description="Cryptographic verification of knowledge state",
        reuse_score=0.88,
        hackathon_fit={"telegraph": 0.9, "openaire": 0.7, "hack_hydra": 0.85, "decentralize_ai": 0.9},
    ),
    WigglyCapability(
        name="scholarly_data_adapters",
        description="OpenAlex, Crossref, DOI, ORCID adapters",
        reuse_score=0.85,
        hackathon_fit={"openaire": 0.95, "telegraph": 0.6, "hack_hydra": 0.5, "decentralize_ai": 0.5},
    ),
    WigglyCapability(
        name="provenance_serializers",
        description="PROV-O, CIDOC CRM, RO-Crate, C2PA output formats",
        reuse_score=0.80,
        hackathon_fit={"decentralize_ai": 0.85, "openaire": 0.7, "telegraph": 0.5, "hack_hydra": 0.6},
    ),
    WigglyCapability(
        name="knowledge_graph",
        description="Entity-relation graph with provenance edges",
        reuse_score=0.85,
        hackathon_fit={"hack_hydra": 0.95, "openaire": 0.9, "telegraph": 0.7, "decentralize_ai": 0.6},
    ),
]


def calculate_hackathon_reuse(hackathon_key: str) -> dict[str, Any]:
    """Calculate how much of Wiggly can be reused for a hackathon."""
    scores = []
    for cap in WIGGLY_CAPABILITIES:
        fit = cap.hackathon_fit.get(hackathon_key, 0)
        scores.append({
            "capability": cap.name,
            "reuse": cap.reuse_score,
            "fit": fit,
            "combined": cap.reuse_score * fit,
        })

    scores.sort(key=lambda x: -x["combined"])
    total_combined = sum(s["combined"] for s in scores)

    return {
        "hackathon": hackathon_key,
        "capabilities": scores,
        "total_reuse_score": total_combined / len(scores) if scores else 0,
        "top_capabilities": [s["capability"] for s in scores[:3]],
    }


def format_wiggly_reuse(hackathon_key: str) -> str:
    data = calculate_hackathon_reuse(hackathon_key)
    lines = []
    lines.append(f"  Wiggly reuse for {hackathon_key}:")
    for cap in data["capabilities"][:5]:
        bar = "█" * int(cap["combined"] * 20) + "░" * (20 - int(cap["combined"] * 20))
        lines.append(f"    {cap['capability']:<30} {bar} {cap['combined']:.2f}")
    lines.append(f"  Top 3: {', '.join(data['top_capabilities'])}")
    return "\n".join(lines)
