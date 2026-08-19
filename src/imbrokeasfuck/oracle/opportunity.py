"""Opportunity Oracle — normalized opportunity feed from all sources."""
from __future__ import annotations
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Any, Optional
import hashlib
import json


@dataclass
class Opportunity:
    kind: str  # hackathon|bounty|grant|subnet|builder_program|testnet|rfp|service|deliverable
    title: str
    sponsor: str
    discovered_at: str
    opens_at: Optional[str] = None
    deadline: Optional[str] = None

    # Reward
    reward_type: str = ""  # cash|token_emission|credits|grant|accelerator
    amount_min_usd: Optional[float] = None
    amount_max_usd: Optional[float] = None
    reward_confidence: float = 0.0

    # Artifact required
    artifact_type: str = ""  # repo|agent.py|SKILL.md|docker|api|prototype|proposal
    open_source_required: bool = True

    # Constraints
    eligibility: list[str] = field(default_factory=list)
    eligibility_status: str = "UNKNOWN"  # ELIGIBLE|BLOCKED|UNKNOWN
    ip_assignment: Optional[str] = None
    submission_fee: Optional[str] = None
    hardware: Optional[str] = None
    prior_art_policy: str = ""  # EXCLUDE_SAME_COMPETITION_SUBMISSIONS|ALLOWED|UNKNOWN
    age_min: Optional[int] = None
    kyc_required: bool = False
    human_required: bool = False

    # QDW fit
    reuse_score: float = 0.0
    estimated_engineering_hours: float = 0.0
    local_evaluator_available: bool = False
    factory_candidate: str = ""
    existing_assets: list[str] = field(default_factory=list)

    # Economics
    cash_at_risk: float = 0.0
    expected_value_confidence: str = ""  # LOW|MEDIUM|HIGH
    paying_slots: int = 0

    # Source
    source: str = ""
    source_url: str = ""
    source_data: dict[str, Any] = field(default_factory=dict)

    # Rating
    rating: str = ""  # A|B|C|REJECT
    recommendation: str = ""  # ATTACK|INVESTIGATE|MONITOR|SKIP

    def id(self) -> str:
        raw = f"{self.kind}:{self.title}:{self.sponsor}"
        return hashlib.sha256(raw.encode()).hexdigest()[:16]

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["id"] = self.id()
        return d


# ── Source registries ──────────────────────────────────────────────────────

HACKATHON_SOURCES = {
    "devfolio": {
        "name": "Devfolio",
        "url": "https://ses.devfolio.co/hackathons",
        "type": "html_poll",
    },
    "ethglobal": {
        "name": "ETHGlobal",
        "url": "https://ethglobal.com/events",
        "type": "html_poll",
    },
    "colosseum": {
        "name": "Colosseum",
        "url": "https://www.colosseum.org/",
        "type": "page_poll",
    },
    "hackernoon": {
        "name": "HackerNoon",
        "url": "https://hackernoon.com/tagged/hackathon/feed",
        "type": "rss",
    },
    "devpost": {
        "name": "Devpost",
        "url": "https://devpost.com/hackathons",
        "type": "html_poll",
    },
    "dorahacks": {
        "name": "DoraHacks",
        "url": "https://dorahacks.io/",
        "type": "page_poll",
    },
}

BOUNTY_SOURCES = {
    "superteam": {
        "name": "Superteam Earn",
        "url": "https://superteam.fun/earn/agents",
        "type": "api",
        "rating": "A",
    },
    "tether": {
        "name": "Tether.dev",
        "url": "https://tether.io",
        "type": "page_poll",
        "rating": "A",
    },
    "opire": {
        "name": "Opire",
        "url": "https://docs.opire.dev",
        "type": "github_issues",
        "rating": "B",
    },
    "algora": {
        "name": "Algora",
        "url": "https://algora.io",
        "type": "bounty_listings",
        "rating": "B",
    },
}

GRANT_SOURCES = {
    "nosana": {"name": "Nosana Grants", "url": "https://nosana.com/grants/", "rating": "A"},
    "akash": {"name": "Akash Grants", "url": "https://akash.network/development/funding-program/", "rating": "A"},
    "heurist": {"name": "Heurist", "url": "https://sdk.heurist.ai", "rating": "B"},
    "litvm": {"name": "LitVM Builders", "url": "https://builders.litvm.com", "rating": "B"},
    "vana": {"name": "Vana Grants", "url": "https://vana.org/participate", "rating": "B"},
    "arweave": {"name": "Arweave/AO Onboard", "url": "https://onboard.arweave.net", "rating": "B"},
    "gitcoin": {"name": "Gitcoin", "url": "https://gitcoin.co", "rating": "C"},
    "grants_gov": {"name": "Grants.gov", "url": "https://www.grants.gov", "type": "rss", "rating": "C"},
}

BITTENSOR_SUBNET_SOURCES = {
    "bittensor_ai": {"name": "Bittensor.ai", "url": "https://bittensor.ai/subnets", "type": "api"},
    "tao_app": {"name": "TAO.app", "url": "https://www.tao.app/subnets", "type": "api"},
}

GITHUB_EARLY_SIGNAL_REPOS = [
    # Bittensor subnets
    "ditto-assistant/ditto-subnet",
    "trajectoryRL/trajectoryRL",
    "ridgesai/ridges",
    "theredteam/subnet",
    "BitMind-AI/bitmind-subnet",
    # Grant/program repos
    "nosana-com/nosana",
    "akashproject/akash",
    "vitelabs/vite",
    "vara-network/ vara",
    # Agent platforms
    "langchain-ai/langchain",
    "openai/openai-python",
    "anthropics/anthropic-sdk-python",
    # Crypto AI
    "virtuals-protocol/virtuals-sdk",
    "olas-network/olas",
]

GITHUB_EARLY_SIGNAL_KEYWORDS = [
    "testnet", "incentive", "reward", "grant", "bounty", "hackathon",
    "builder", "cohort", "submission", "opens", "submissions open",
    "miner", "challenge", "programme", "program", "funding",
    "developer", "ecosystem", "integration", "rfp", "request for",
]


def classify_reward(kind: str, title: str, description: str) -> str:
    text = f"{title} {description}".lower()
    if any(w in text for w in ["bounty", "deliverable", "task", "paid"]):
        return "A"  # PAID_BUILD
    if any(w in text for w in ["hackathon", "competition", "benchmark", "contest"]):
        return "A"  # COMPETITION
    if any(w in text for w in ["grant", "milestone", "funding"]):
        return "A"  # GRANT
    if any(w in text for w in ["builder program", "credits", "accelerator"]):
        return "B"  # BUILDER_PROGRAM
    if any(w in text for w in ["testnet", "incentivized", "contribution required"]):
        return "B"  # INCENTIVIZED_TESTNET
    if any(w in text for w in ["points", "referral", "trading volume", "deposit"]):
        return "REJECT"
    return "C"  # POSSIBLE_FUTURE_REWARD


def estimate_qdw_fit(title: str, description: str, kind: str) -> float:
    text = f"{title} {description}".lower()
    score = 0.5  # baseline

    # High fit signals
    if any(w in text for w in ["agent", "ai", "llm", "inference", "model"]):
        score += 0.2
    if any(w in text for w in ["memory", "context", "retrieval", "rag"]):
        score += 0.15
    if any(w in text for w in ["code", "swe", "software", "engineering", "coding"]):
        score += 0.15
    if any(w in text for w in ["security", "audit", "vulnerability"]):
        score += 0.1
    if any(w in text for w in ["compute", "gpu", "inference", "training"]):
        score += 0.1
    if any(w in text for w in ["docker", "container", "api"]):
        score += 0.05

    # Negative signals
    if any(w in text for w in ["trading", "defi", "yield", "liquidity"]):
        score -= 0.2
    if any(w in text for w in ["nft", "collectible", "art"]):
        score -= 0.3

    return min(1.0, max(0.0, score))
