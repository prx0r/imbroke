"""Bittensor subnet economics — correct calculations from chain data."""
from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Any, Optional
import json

# ── Constants ──────────────────────────────────────────────────────────────

TAO_PRICE_USD = 195.0  # working conversion
DAILY_EMISSIONS_TAO = 3600.0  # post-halving Dec 2025
BLOCKS_PER_DAY = 7200
MINER_SHARE = 0.41  # 41% of subnet alpha output
VALIDATOR_SHARE = 0.41
OWNER_SHARE = 0.18
MONTHLY_TARGET_USD = 150.0
DAILY_TARGET_USD = MONTHLY_TARGET_USD / 30.0
DAILY_TARGET_TAO = DAILY_TARGET_USD / TAO_PRICE_USD


# ── MinerContract schema ───────────────────────────────────────────────────

@dataclass
class MinerContract:
    netuid: int
    name: str
    identity_epoch: str = ""

    # Artifact
    artifact_type: str = ""  # docker_memory_harness|SKILL.md|agent.py|training_repo|solution_code|vulnerability_agent|detection_model
    artifact_entrypoint: str = ""
    artifact_max_size: str = ""
    artifact_packaging: str = ""
    artifact_upload_method: str = ""

    # Evaluator
    evaluator_repo: str = ""
    evaluator_command: str = ""
    evaluator_deterministic: bool = True
    evaluator_local_reproducible: bool = False
    evaluator_hidden_tests: bool = False
    evaluator_interval: str = ""

    # Scoring
    scoring_metric: str = ""
    scoring_aggregation: str = ""
    scoring_incumbent_mechanism: str = ""
    scoring_decay: str = ""
    scoring_originality_check: bool = False

    # Economics
    paying_slots: int = 0
    reward_distribution: str = ""  # "65/14/10/7/4" or "winner-take-all" or "proportional"
    registration_cost_tao: float = 0.0
    submission_cost_tao: float = 0.0
    recurring_compute_cost: str = ""
    validator_compute_subsidized: bool = False

    # Infrastructure
    gpu_required: bool = False
    ram_gb: int = 0
    persistent_server: bool = False
    docker_required: bool = False
    storage_required: str = ""
    external_api_costs: str = ""

    # Legal
    license: str = ""
    submission_ip_terms: str = ""
    winning_ip_terms: str = ""

    # QDW
    qdw_factory_type: str = ""
    qdw_reuse_score: float = 0.0
    qdw_existing_assets: list[str] = field(default_factory=list)
    qdw_evaluator_adapter: str = ""
    qdw_expected_iteration_cost_usd: float = 0.0

    # Chain data
    miner_pool_tao_day: float = 0.0
    alpha_price_tao: float = 0.0
    emission_pct: float = 0.0

    # Source
    github: str = ""
    docs: str = ""
    status: str = "active"
    recommendation: str = "MONITOR"

    def daily_reward_for_rank(self, rank: int) -> float:
        """Calculate daily TAO reward for a given rank."""
        if self.reward_distribution == "winner-take-all":
            return self.miner_pool_tao_day if rank == 1 else 0.0
        if "/" in self.reward_distribution:
            parts = [float(x) / 100.0 for x in self.reward_distribution.split("/")]
            if rank <= len(parts):
                return self.miner_pool_tao_day * parts[rank - 1]
        if self.reward_distribution == "proportional":
            return self.miner_pool_tao_day * 0.01  # assume 1% share
        return 0.0

    def daily_reward_usd(self, rank: int) -> float:
        return self.daily_reward_for_rank(rank) * TAO_PRICE_USD

    def monthly_reward_usd(self, rank: int) -> float:
        return self.daily_reward_usd(rank) * 30

    def target_tao_per_day(self) -> float:
        """How much TAO/day needed for $150/month."""
        return DAILY_TARGET_TAO

    def shares_needed_for_target(self) -> float:
        """What fraction of miner pool needed for $150/month."""
        if self.miner_pool_tao_day == 0:
            return 0.0
        return DAILY_TARGET_TAO / self.miner_pool_tao_day

    def difficulty(self) -> str:
        if self.qdw_reuse_score > 0.9 and not self.gpu_required:
            return "4/5"
        if self.qdw_reuse_score > 0.7:
            return "3-4/5"
        return "5/5"

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["daily_reward_rank1_usd"] = self.daily_reward_usd(1)
        d["daily_reward_rank5_usd"] = self.daily_reward_usd(5) if self.paying_slots >= 5 else 0
        d["monthly_reward_rank1_usd"] = self.monthly_reward_usd(1)
        d["shares_needed_for_150mo"] = self.shares_needed_for_target()
        d["difficulty"] = self.difficulty()
        d["target_tao_per_day"] = DAILY_TARGET_TAO
        return d


# ── Subnet contracts (from research) ───────────────────────────────────────

SUBNET_CONTRACTS = {
    118: MinerContract(
        netuid=118, name="Ditto",
        artifact_type="docker_memory_harness",
        artifact_entrypoint="harness HTTP contract",
        artifact_packaging="Docker build context",
        evaluator_repo="ditto-assistant/ditto-subnet",
        evaluator_deterministic=True,
        evaluator_local_reproducible=True,
        evaluator_hidden_tests=True,
        scoring_metric="composite (tool + memory)",
        scoring_aggregation="DittoBench",
        scoring_incumbent_mechanism="top 5 eligible",
        paying_slots=5,
        reward_distribution="65/14/10/7/4",
        submission_cost_tao=0.04,
        validator_compute_subsidized=True,
        gpu_required=False,
        docker_required=True,
        submission_ip_terms="Platform-owned on reward-earning win",
        qdw_factory_type="agent-memory",
        qdw_reuse_score=0.96,
        qdw_existing_assets=["qdw", "memory_bridge", "context_compiler", "handover"],
        qdw_evaluator_adapter="ditto-bench-local",
        qdw_expected_iteration_cost_usd=0.0,
        miner_pool_tao_day=34.16,
        github="https://github.com/ditto-assistant/ditto-subnet",
        recommendation="ATTACK",
    ),
    56: MinerContract(
        netuid=56, name="Gradients / G.O.D",
        artifact_type="training_repo",
        artifact_entrypoint="open-source training repository",
        artifact_packaging="git repo",
        evaluator_repo="gradients-ai/G.O.D",
        evaluator_deterministic=False,
        evaluator_local_reproducible=False,
        scoring_metric="tournament ranking",
        scoring_aggregation="text/image/environment tournaments",
        paying_slots=2,
        reward_distribution="top_2_per_tournament",
        submission_cost_tao=0.25,
        validator_compute_subsidized=True,
        gpu_required=False,
        submission_ip_terms="Retained by miner",
        qdw_factory_type="training-recipe",
        qdw_reuse_score=0.88,
        qdw_existing_assets=["qdw", "gitgoblin"],
        qdw_evaluator_adapter="gradients-api",
        qdw_expected_iteration_cost_usd=48.0,
        miner_pool_tao_day=54.32,
        github="https://github.com/gradients-ai/G.O.D",
        recommendation="ATTACK",
    ),
    11: MinerContract(
        netuid=11, name="TrajectoryRL",
        artifact_type="SKILL.md",
        artifact_entrypoint="skill pack",
        artifact_packaging="SKILL.md + metadata",
        evaluator_repo="trajectoryRL/trajrl-bench",
        evaluator_deterministic=True,
        evaluator_local_reproducible=True,
        scoring_metric="verified task outcomes",
        scoring_aggregation="Hermes in sandbox",
        scoring_incumbent_mechanism="must beat by 3%",
        paying_slots=1,
        reward_distribution="winner-take-all",
        submission_cost_tao=0.44,
        validator_compute_subsidized=True,
        gpu_required=False,
        submission_ip_terms="Copyright transfers on reward-earning win",
        qdw_factory_type="skill-factory",
        qdw_reuse_score=0.94,
        qdw_existing_assets=["qdw", "gitgoblin", "superpowers"],
        qdw_evaluator_adapter="trajrl-local-eval",
        qdw_expected_iteration_cost_usd=86.0,
        miner_pool_tao_day=26.05,
        github="https://github.com/trajectoryRL/trajectoryRL",
        recommendation="INVESTIGATE",
    ),
    62: MinerContract(
        netuid=62, name="Ridges",
        artifact_type="agent.py",
        artifact_entrypoint="agent.py",
        artifact_packaging="python file",
        evaluator_repo="ridgesai/ridges",
        evaluator_deterministic=False,
        evaluator_local_reproducible=True,
        scoring_metric="SWE benchmark score",
        scoring_aggregation="highest overall scorer",
        paying_slots=1,
        reward_distribution="winner-take-all",
        submission_cost_tao=0.0,
        validator_compute_subsidized=True,
        gpu_required=False,
        submission_ip_terms="IP irrevocably assigned to Hidden Harvest Ventures",
        qdw_factory_type="swe-agent",
        qdw_reuse_score=0.92,
        qdw_existing_assets=["qdw", "gitgoblin", "qdw-workbench"],
        qdw_evaluator_adapter="ridges-local",
        qdw_expected_iteration_cost_usd=0.0,
        miner_pool_tao_day=46.85,
        github="https://github.com/ridgesai/ridges",
        recommendation="INVESTIGATE",
    ),
    61: MinerContract(
        netuid=61, name="RedTeam",
        artifact_type="solution_code",
        artifact_entrypoint="authorized challenge solution",
        artifact_packaging="code submission",
        evaluator_repo="RedTeamSubnet/RedTeam",
        evaluator_deterministic=True,
        evaluator_local_reproducible=True,
        scoring_metric="performance-proportional weight",
        scoring_aggregation="validator consensus",
        scoring_decay="10 days full, decay to ~15 days",
        paying_slots=45,
        reward_distribution="proportional",
        submission_cost_tao=0.0,
        gpu_required=False,
        ram_gb=8,
        submission_ip_terms="Retained by miner",
        qdw_factory_type="challenge-solver",
        qdw_reuse_score=0.72,
        qdw_existing_assets=["qdw", "qdw-workbench"],
        qdw_evaluator_adapter="redteam-local",
        qdw_expected_iteration_cost_usd=0.0,
        miner_pool_tao_day=26.44,
        github="https://github.com/RedTeamSubnet/RedTeam",
        recommendation="INVESTIGATE",
    ),
    15: MinerContract(
        netuid=15, name="ORO",
        artifact_type="shopping_agent",
        artifact_entrypoint="Python shopping agent",
        artifact_packaging="python code",
        evaluator_repo="ORO-AI/oro",
        evaluator_deterministic=False,
        evaluator_local_reproducible=False,
        scoring_metric="difficulty-adjusted avg of last 3 races",
        scoring_aggregation="daily races",
        paying_slots=1,
        reward_distribution="winner-take-all-93%",
        submission_cost_tao=0.0,
        gpu_required=False,
        submission_ip_terms="Unknown",
        qdw_factory_type="shopping-agent",
        qdw_reuse_score=0.65,
        qdw_existing_assets=["qdw"],
        qdw_evaluator_adapter="oro-docker",
        qdw_expected_iteration_cost_usd=0.0,
        miner_pool_tao_day=55.0,
        github="https://github.com/ORO-AI/oro",
        recommendation="MONITOR",
    ),
    60: MinerContract(
        netuid=60, name="BitSec",
        artifact_type="vulnerability_agent",
        artifact_entrypoint="vulnerability analysis agent",
        artifact_packaging="agent code",
        evaluator_repo="Bitsec-AI/subnet",
        evaluator_deterministic=False,
        evaluator_local_reproducible=False,
        scoring_metric="comparison with known audit findings",
        scoring_aggregation="highest scoring eligible agent",
        paying_slots=1,
        reward_distribution="winner-take-all",
        submission_cost_tao=0.0,
        gpu_required=False,
        submission_ip_terms="Public after rounds",
        qdw_factory_type="security-agent",
        qdw_reuse_score=0.60,
        qdw_existing_assets=["qdw"],
        qdw_expected_iteration_cost_usd=0.0,
        miner_pool_tao_day=0.148,
        github="https://github.com/Bitsec-AI/subnet",
        recommendation="MONITOR",
    ),
    34: MinerContract(
        netuid=34, name="BitMind / GAS",
        artifact_type="detection_model",
        artifact_entrypoint="detection model",
        artifact_packaging="model checkpoint",
        evaluator_repo="BitMind-AI/bitmind-subnet",
        evaluator_deterministic=True,
        evaluator_local_reproducible=True,
        scoring_metric="accuracy",
        scoring_aggregation="cloud evaluation",
        paying_slots=5,
        reward_distribution="accuracy-based",
        submission_cost_tao=0.0,
        gpu_required=False,
        submission_ip_terms="Retained by miner",
        qdw_factory_type="model-research",
        qdw_reuse_score=0.45,
        qdw_existing_assets=["qdw"],
        qdw_evaluator_adapter="gasbench-local",
        qdw_expected_iteration_cost_usd=0.0,
        miner_pool_tao_day=0.0,
        github="https://github.com/BitMind-AI/bitmind-subnet",
        recommendation="MONITOR",
    ),
}


# ── Identity epoch model ──────────────────────────────────────────────────

@dataclass
class SubnetIdentityEpoch:
    netuid: int
    owner_hotkey: str = ""
    owner_coldkey: str = ""
    observed_from_block: int = 0
    observed_to_block: int = 0
    name: str = ""
    token_symbol: str = ""
    github: str = ""
    website: str = ""
    repo_commit: str = ""
    evidence: list[str] = field(default_factory=list)


# ── Economics calculations ────────────────────────────────────────────────

def calculate_subnet_economics(
    netuid: int,
    alpha_price_tao: float,
    subnet_emission_pct: float,
    blocks_per_day: int = 7200,
    miner_share: float = 0.41,
) -> dict[str, Any]:
    """Calculate economics from chain data."""
    subnet_tao_day = DAILY_EMISSIONS_TAO * (subnet_emission_pct / 100.0)
    miner_pool_tao = subnet_tao_day * miner_share

    return {
        "netuid": netuid,
        "subnet_tao_day": subnet_tao_day,
        "miner_pool_tao_day": miner_pool_tao,
        "miner_pool_usd_day": miner_pool_tao * TAO_PRICE_USD,
        "alpha_price_tao": alpha_price_tao,
        "daily_target_tao": DAILY_TARGET_TAO,
        "daily_target_usd": DAILY_TARGET_USD,
        "monthly_target_usd": MONTHLY_TARGET_USD,
    }


def rank_economics(contract: MinerContract) -> list[dict[str, Any]]:
    """Show economics for each paying rank."""
    rows = []
    for rank in range(1, contract.paying_slots + 1):
        tao = contract.daily_reward_for_rank(rank)
        usd = tao * TAO_PRICE_USD
        monthly = usd * 30
        rows.append({
            "rank": rank,
            "daily_tao": round(tao, 4),
            "daily_usd": round(usd, 2),
            "monthly_usd": round(monthly, 2),
        })
    return rows


def format_economics(contract: MinerContract) -> str:
    """Format economics report for a subnet."""
    lines = []
    lines.append(f"{'='*60}")
    lines.append(f"  SN{contract.netuid} {contract.name}")
    lines.append(f"{'='*60}")
    lines.append(f"  Miner pool: {contract.miner_pool_tao_day:.2f} TAO/day (${contract.miner_pool_tao_day * TAO_PRICE_USD:,.0f}/day)")
    lines.append(f"  Submission cost: {contract.submission_cost_tao} TAO (${contract.submission_cost_tao * TAO_PRICE_USD:.2f})")
    lines.append(f"  Paying slots: {contract.paying_slots}")
    lines.append(f"  Distribution: {contract.reward_distribution}")
    lines.append(f"  GPU required: {'Yes' if contract.gpu_required else 'No'}")
    lines.append(f"  QDW fit: {contract.qdw_reuse_score:.0%}")
    lines.append(f"  Difficulty: {contract.difficulty()}")
    lines.append(f"  IP terms: {contract.submission_ip_terms}")
    lines.append("")
    lines.append(f"  Daily rewards by rank:")
    for r in rank_economics(contract):
        marker = " <-- target" if r["monthly_usd"] >= MONTHLY_TARGET_USD else ""
        lines.append(f"    #{r['rank']}: {r['daily_tao']:.4f} TAO/day = ${r['daily_usd']:,.2f}/day = ${r['monthly_usd']:,.2f}/mo{marker}")
    lines.append("")
    shares = contract.shares_needed_for_target()
    if shares > 0:
        lines.append(f"  Shares needed for $150/mo: {shares:.4%} of miner pool")
    lines.append(f"  Recommendation: {contract.recommendation}")
    lines.append(f"{'='*60}")
    return "\n".join(lines)


def format_all_economics() -> str:
    """Format economics for all tracked subnets."""
    lines = []
    lines.append(f"{'='*70}")
    lines.append(f"  BITTENSOR MINER ECONOMICS — TAO=${TAO_PRICE_USD}")
    lines.append(f"  Daily target: ${DAILY_TARGET_USD:.2f}/day = {DAILY_TARGET_TAO:.4f} TAO/day")
    lines.append(f"{'='*70}")
    lines.append("")

    for netuid, contract in sorted(SUBNET_CONTRACTS.items(), key=lambda x: -x[1].miner_pool_tao_day):
        lines.append(format_economics(contract))
        lines.append("")

    return "\n".join(lines)
