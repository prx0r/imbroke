"""RevenueChannel — serve-to-earn recurring revenue."""
from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Any, Optional


@dataclass
class RevenueChannel:
    """A recurring revenue channel from a capability/service."""

    channel_id: str = ""
    name: str = ""
    capability: str = ""

    # Platform
    platform: str = ""  # apify|x402|virtuals|heurist|olas|manual
    platform_url: str = ""
    platform_api: str = ""

    # Economics
    pricing_model: str = ""  # per_call|per_job|subscription|freemium
    price_per_call_usd: float = 0.0
    estimated_monthly_calls: int = 0
    estimated_monthly_revenue_usd: float = 0.0

    # Requirements
    infrastructure_cost_usd: float = 0.0
    inference_cost_per_call: float = 0.0
    max_concurrent: int = 10

    # Status
    status: str = "planned"  # planned|building|live|paused
    live_since: Optional[str] = None
    total_invocations: int = 0
    total_revenue_usd: float = 0.0

    # Quality
    avg_rating: float = 0.0
    repeat_buyer_rate: float = 0.0

    def net_monthly_revenue(self) -> float:
        return self.estimated_monthly_revenue_usd - self.infrastructure_cost_usd

    def roi(self) -> float:
        if self.infrastructure_cost_usd == 0:
            return float("inf") if self.estimated_monthly_revenue_usd > 0 else 0
        return self.net_monthly_revenue() / self.infrastructure_cost_usd

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["net_monthly_revenue"] = self.net_monthly_revenue()
        d["roi"] = self.roi()
        return d


# ── Pre-configured channels ───────────────────────────────────────────────

RECOMMENDED_CHANNELS = [
    RevenueChannel(
        channel_id="apify-gitgoblin",
        name="GitGoblin Technical Research",
        capability="gitgoblin_research",
        platform="apify",
        pricing_model="per_call",
        price_per_call_usd=0.05,
        estimated_monthly_calls=100,
        estimated_monthly_revenue_usd=5.0,
        infrastructure_cost_usd=1.0,
    ),
    RevenueChannel(
        channel_id="apify-repo-audit",
        name="Repository Evidence Audit",
        capability="repo_audit",
        platform="apify",
        pricing_model="per_call",
        price_per_call_usd=0.10,
        estimated_monthly_calls=50,
        estimated_monthly_revenue_usd=5.0,
        infrastructure_cost_usd=2.0,
    ),
    RevenueChannel(
        channel_id="x402-dell-compute",
        name="Dell Compute Resolve",
        capability="dell_compute",
        platform="x402",
        pricing_model="per_call",
        price_per_call_usd=0.01,
        estimated_monthly_calls=500,
        estimated_monthly_revenue_usd=5.0,
        infrastructure_cost_usd=0.5,
    ),
    RevenueChannel(
        channel_id="x402-opportunity-research",
        name="Opportunity Research API",
        capability="opportunity_research",
        platform="x402",
        pricing_model="per_call",
        price_per_call_usd=0.02,
        estimated_monthly_calls=200,
        estimated_monthly_revenue_usd=4.0,
        infrastructure_cost_usd=0.5,
    ),
    RevenueChannel(
        channel_id="virtuals-verification",
        name="QDW Verification Service",
        capability="qdw_verification",
        platform="virtuals",
        pricing_model="per_job",
        price_per_call_usd=0.50,
        estimated_monthly_calls=10,
        estimated_monthly_revenue_usd=5.0,
        infrastructure_cost_usd=1.0,
    ),
]
