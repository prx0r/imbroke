"""Candidate genome — parameterized representation of what to submit."""
from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Any, Optional
import hashlib
import json
import random


@dataclass
class CandidateGenome:
    """A parameterized candidate for competition submission."""

    # Identity
    genome_id: str = ""
    parent_ids: list[str] = field(default_factory=list)
    generation: int = 0

    # Behavioral niche (MAP-Elites dimensions)
    niche_cost: str = "medium"  # cheap|medium|expensive
    niche_approach: str = "structured"  # minimal|retrieval_heavy|planning|chaotic|structured

    # Core parameters (subnet-specific)
    params: dict[str, Any] = field(default_factory=dict)

    # Metadata
    factory: str = ""  # which factory created this
    subnet: int = 0
    artifact_type: str = ""

    # Evaluation history
    local_scores: list[float] = field(default_factory=list)
    mainnet_scores: list[float] = field(default_factory=list)
    cost_usd: float = 0.0
    engineering_hours: float = 0.0

    # Status
    status: str = "new"  # new|evaluating|submitted|retired|cemetery
    submission_count: int = 0
    last_submitted_at: str = ""

    def __post_init__(self):
        if not self.genome_id:
            raw = json.dumps(self.params, sort_keys=True, default=str)
            self.genome_id = hashlib.sha256(raw.encode()).hexdigest()[:12]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def local_score(self) -> Optional[float]:
        return self.local_scores[-1] if self.local_scores else None

    def mainnet_score(self) -> Optional[float]:
        return self.mainnet_scores[-1] if self.mainnet_scores else None

    def dominates(self, other: "CandidateGenome") -> bool:
        """Does this candidate dominate the other? (higher is better)"""
        s1 = self.local_score() or 0
        s2 = other.local_score() or 0
        c1 = self.cost_usd or 999
        c2 = other.cost_usd or 999
        return s1 >= s2 and c1 <= c2 and (s1 > s2 or c1 < c2)


@dataclass
class GenomeSpace:
    """Defines the parameter space for a specific factory."""

    factory: str
    subnet: int = 0

    # Dimensions for MAP-Elites
    cost_bins: list[str] = field(default_factory=lambda: ["cheap", "medium", "expensive"])
    approach_bins: list[str] = field(default_factory=lambda: [
        "minimal", "retrieval_heavy", "planning", "chaotic", "structured",
    ])

    # Parameter ranges (subnet-specific)
    param_ranges: dict[str, list[Any]] = field(default_factory=dict)

    def random_genome(self) -> CandidateGenome:
        """Generate a random candidate."""
        params = {}
        for key, values in self.param_ranges.items():
            params[key] = random.choice(values)

        return CandidateGenome(
            factory=self.factory,
            subnet=self.subnet,
            niche_cost=random.choice(self.cost_bins),
            niche_approach=random.choice(self.approach_bins),
            params=params,
        )

    def mutate(self, genome: CandidateGenome, rate: float = 0.2) -> CandidateGenome:
        """Mutate a candidate genome."""
        new_params = dict(genome.params)
        for key, values in self.param_ranges.items():
            if random.random() < rate:
                new_params[key] = random.choice(values)

        # Occasionally mutate niche
        niche_cost = genome.niche_cost
        niche_approach = genome.niche_approach
        if random.random() < rate / 2:
            niche_cost = random.choice(self.cost_bins)
        if random.random() < rate / 2:
            niche_approach = random.choice(self.approach_bins)

        return CandidateGenome(
            factory=genome.factory,
            subnet=genome.subnet,
            parent_ids=[genome.genome_id] + genome.parent_ids[:4],
            generation=genome.generation + 1,
            niche_cost=niche_cost,
            niche_approach=niche_approach,
            params=new_params,
        )

    def crossover(self, a: CandidateGenome, b: CandidateGenome) -> CandidateGenome:
        """Crossover two candidate genomes."""
        new_params = {}
        all_keys = set(list(a.params.keys()) + list(b.params.keys()))
        for key in all_keys:
            if random.random() < 0.5:
                new_params[key] = a.params.get(key)
            else:
                new_params[key] = b.params.get(key)

        return CandidateGenome(
            factory=a.factory,
            subnet=a.subnet,
            parent_ids=[a.genome_id, b.genome_id],
            generation=max(a.generation, b.generation) + 1,
            niche_cost=random.choice([a.niche_cost, b.niche_cost]),
            niche_approach=random.choice([a.niche_approach, b.niche_approach]),
            params=new_params,
        )


# ── Predefined genome spaces per subnet ───────────────────────────────────

DITTO_GENOME = GenomeSpace(
    factory="ditto",
    subnet=118,
    param_ranges={
        "retriever": ["tfidf", "embedding", "hybrid", "bm25"],
        "embedding_strategy": ["static", "contextual", "late_interaction"],
        "memory_segmentation": ["fixed", "semantic", "event", "hierarchical"],
        "memory_schema": ["plain", "structured", "entity_relation", "knowledge_graph"],
        "retrieval_k": [3, 5, 10, 20, 50],
        "reranker": ["none", "cross_encoder", "llm_rerank", "reciprocal_rank"],
        "context_compression": ["none", "summary", "extractive", "lossy"],
        "memory_write_policy": ["append", "replace", "merge", "dedup"],
        "prompt_architecture": ["direct", "chain_of_thought", "tree_of_thought", "react"],
        "tool_strategy": ["none", "single", "multi", "planned"],
        "reasoning_effort": ["low", "medium", "high"],
        "failure_recovery": ["none", "retry", "rephrase", "fallback_chain"],
    },
)

TRAJECTORYRL_GENOME = GenomeSpace(
    factory="trajectoryrl",
    subnet=11,
    param_ranges={
        "skill_type": ["task_decomposition", "error_recovery", "tool_usage", "planning"],
        "verification_level": ["none", "assertions", "tests", "formal"],
        "context_window": ["minimal", "moderate", "full"],
        "planning_strategy": ["none", "linear", "hierarchical", "reactive"],
        "recovery_mechanism": ["none", "checkpoint", "undo", "rollback"],
        "tool_integration": ["none", "basic", "composable", "planned"],
    },
)

GRADIENTS_GENOME = GenomeSpace(
    factory="gradients",
    subnet=56,
    param_ranges={
        "base_model": ["llama-7b", "llama-13b", "mistral-7b", "qwen-7b"],
        "optimizer": ["adam", "adamw", "sgd", "lion"],
        "lr": [1e-5, 3e-5, 5e-5, 1e-4],
        "scheduler": ["cosine", "linear", "constant", "warmup_cosine"],
        "lora_rank": [4, 8, 16, 32, 64],
        "lora_alpha": [8, 16, 32, 64],
        "batch_size": [4, 8, 16, 32],
        "gradient_accumulation": [1, 2, 4, 8],
        "warmup_steps": [100, 200, 500, 1000],
        "max_steps": [1000, 2000, 5000],
        "loss_function": ["cross_entropy", "focal", "label_smoothing"],
        "data_mixing": ["equal", "curriculum", "difficulty_weighted"],
    },
)

RIDGES_GENOME = GenomeSpace(
    factory="ridges",
    subnet=62,
    param_ranges={
        "agent_kernel": ["ralph_loop", "hermes", "qdw_structured", "tree_search", "reflexion"],
        "model": ["gpt-4o", "claude-sonnet", "deepseek-coder", "qwen-coder"],
        "context_strategy": ["full_repo", "relevant_files", "chunked", "graph_based"],
        "test_strategy": ["none", "unit", "integration", "property"],
        "repair_strategy": ["retry", "rephrase", "diff_based", "test_guided"],
        "max_iterations": [3, 5, 10, 20],
        "token_budget": [4000, 8000, 16000, 32000],
    },
)

GENOME_SPACES = {
    118: DITTO_GENOME,
    11: TRAJECTORYRL_GENOME,
    56: GRADIENTS_GENOME,
    62: RIDGES_GENOME,
}
