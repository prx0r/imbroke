"""Competition factory — orchestrates the full lifecycle."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Optional
from enum import Enum
from .genome import CandidateGenome, GenomeSpace, GENOME_SPACES
from .evolution import MAPElites
from .evaluator import CascadeEvaluator
from .calibration import CalibrationModel


class FactoryState(str, Enum):
    INIT = "init"
    SEEDING = "seeding"
    EVOLVING = "evolving"
    EVALUATING = "evaluating"
    SUBMITTING = "submitting"
    LEARNING = "learning"
    PAUSED = "paused"


@dataclass
class CompetitionFactory:
    """A factory that continuously evolves candidates for one competition."""

    factory_id: str
    subnet: int
    name: str
    artifact_type: str

    # Components
    space: Optional[GenomeSpace] = None
    population: Optional[MAPElites] = None
    evaluator: Optional[CascadeEvaluator] = None
    calibration: Optional[CalibrationModel] = None

    # State
    state: FactoryState = FactoryState.INIT
    generation: int = 0
    total_submissions: int = 0
    total_cost_usd: float = 0.0
    best_score_ever: float = 0.0
    current_incumbent_score: float = 0.0

    # Economics
    submission_cost_tao: float = 0.0
    paying_slots: int = 0
    reward_distribution: str = ""

    # Config
    population_size: int = 50
    generations_between_submissions: int = 10

    def __post_init__(self):
        if self.space is None and self.subnet in GENOME_SPACES:
            self.space = GENOME_SPACES[self.subnet]
        if self.space is None:
            self.space = GenomeSpace(factory=self.factory_id, subnet=self.subnet)
        if self.population is None:
            self.population = MAPElites(space=self.space)
        if self.evaluator is None:
            self.evaluator = CascadeEvaluator()
        if self.calibration is None:
            self.calibration = CalibrationModel(factory=self.factory_id, subnet=self.subnet)

    def initialize(self):
        """Initialize the factory with a random population."""
        self.state = FactoryState.SEEDING
        self.population.seed_population(self.population_size)
        self.state = FactoryState.EVOLVING

    def step(self) -> dict[str, Any]:
        """Run one step of the factory loop."""
        if self.state == FactoryState.INIT:
            self.initialize()

        if self.state == FactoryState.EVOLVING:
            new_candidates = self.population.evolve_generation()
            self.generation += 1

            # Evaluate new candidates
            self.state = FactoryState.EVALUATING
            passed = self.evaluator.evaluate_cascade(new_candidates)

            # Update niches
            for genome in passed:
                self.population.update_niche(genome)

            # Check if ready to submit
            best = self._get_best_candidate()
            if best and self.generation % self.generations_between_submissions == 0:
                self.state = FactoryState.SUBMITTING
                decision = self.calibration.should_submit(
                    best.local_score() or 0,
                    self.submission_cost_tao * 195.0,  # approximate TAO price
                )
                self.total_cost_usd += self.submission_cost_tao * 195.0
                self.state = FactoryState.EVOLVING
                return {
                    "action": "submit_decision",
                    "candidate": best.to_dict(),
                    "decision": decision,
                    "generation": self.generation,
                }

            self.state = FactoryState.EVOLVING
            return {
                "action": "evolve",
                "new_candidates": len(new_candidates),
                "surviving": len(passed),
                "generation": self.generation,
                "population_stats": self.population.stats(),
            }

        return {"action": "none", "state": self.state.value}

    def record_submission(self, genome: CandidateGenome, mainnet_score: float, rank: Optional[int] = None):
        """Record a mainnet submission result."""
        genome.mainnet_scores.append(mainnet_score)
        genome.submission_count += 1
        self.total_submissions += 1

        paid = rank is not None and rank <= self.paying_slots
        self.calibration.add_observation(
            genome_id=genome.genome_id,
            local_score=genome.local_score() or 0,
            mainnet_score=mainnet_score,
            rank_achieved=rank,
            paid=paid,
        )

        if mainnet_score > self.best_score_ever:
            self.best_score_ever = mainnet_score

    def _get_best_candidate(self) -> Optional[CandidateGenome]:
        best = None
        for niche in self.population.niches.values():
            if niche.best_candidate:
                if best is None or (niche.best_candidate.local_score() or 0) > (best.local_score() or 0):
                    best = niche.best_candidate
        return best

    def summary(self) -> dict[str, Any]:
        best = self._get_best_candidate()
        return {
            "factory_id": self.factory_id,
            "subnet": self.subnet,
            "name": self.name,
            "state": self.state.value,
            "generation": self.generation,
            "total_submissions": self.total_submissions,
            "total_cost_usd": self.total_cost_usd,
            "best_score_ever": self.best_score_ever,
            "current_best": best.local_score() if best else None,
            "population": self.population.stats(),
            "calibration": self.calibration.stats(),
            "evaluator": self.evaluator.stats(),
        }


# ── Pre-configured factories ──────────────────────────────────────────────

def create_ditto_factory() -> CompetitionFactory:
    return CompetitionFactory(
        factory_id="bittensor-118",
        subnet=118,
        name="Ditto Memory Harness",
        artifact_type="docker_memory_harness",
        submission_cost_tao=0.04,
        paying_slots=5,
        reward_distribution="65/14/10/7/4",
        evaluator=CascadeEvaluator().default_ditto_cascade(),
        population_size=50,
    )


def create_trajectoryrl_factory() -> CompetitionFactory:
    return CompetitionFactory(
        factory_id="bittensor-11",
        subnet=11,
        name="TrajectoryRL Skills",
        artifact_type="SKILL.md",
        submission_cost_tao=0.44,
        paying_slots=1,
        reward_distribution="winner-take-all",
        evaluator=CascadeEvaluator().default_trajectoryrl_cascade(),
        population_size=30,
    )


def create_gradients_factory() -> CompetitionFactory:
    return CompetitionFactory(
        factory_id="bittensor-56",
        subnet=56,
        name="Gradients Training",
        artifact_type="training_repo",
        submission_cost_tao=0.25,
        paying_slots=2,
        reward_distribution="top_2_per_tournament",
        evaluator=CascadeEvaluator().default_gradients_cascade(),
        population_size=40,
    )


def create_ridges_factory() -> CompetitionFactory:
    return CompetitionFactory(
        factory_id="bittensor-62",
        subnet=62,
        name="Ridges SWE Agent",
        artifact_type="agent.py",
        submission_cost_tao=0.0,
        paying_slots=1,
        reward_distribution="winner-take-all",
        population_size=30,
    )


FACTORY_REGISTRY = {
    118: create_ditto_factory,
    11: create_trajectoryrl_factory,
    56: create_gradients_factory,
    62: create_ridges_factory,
}
