"""Cascade evaluator — cheap→expensive evaluation pipeline."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Optional, Callable
from .genome import CandidateGenome


@dataclass
class EvalStage:
    """A stage in the cascade evaluation pipeline."""
    name: str
    cost_per_eval: float  # USD
    model_tier: str  # "static", "cheap", "medium", "production"
    max_candidates: int
    evaluator: Optional[Callable] = None  # (genome) -> score or None
    pass_threshold: float = 0.0
    description: str = ""


@dataclass
class CascadeEvaluator:
    """Multi-stage evaluation cascade."""

    stages: list[EvalStage] = field(default_factory=list)
    calibration_model: Any = None  # CalibrationModel reference

    # Tracking
    evaluations_run: int = 0
    total_cost: float = 0.0

    def default_ditto_cascade(self) -> "CascadeEvaluator":
        """Default cascade for Ditto SN118."""
        return CascadeEvaluator(stages=[
            EvalStage(
                name="static_gates",
                cost_per_eval=0.0,
                model_tier="static",
                max_candidates=1000,
                pass_threshold=0.3,
                description="Regex/structural checks, format validation",
            ),
            EvalStage(
                name="cheap_model",
                cost_per_eval=0.001,
                model_tier="cheap",
                max_candidates=200,
                pass_threshold=0.5,
                description="Fast model on subset of cases",
            ),
            EvalStage(
                name="medium_model",
                cost_per_eval=0.01,
                model_tier="medium",
                max_candidates=40,
                pass_threshold=0.7,
                description="Capable model on full benchmark",
            ),
            EvalStage(
                name="production_model",
                cost_per_eval=0.05,
                model_tier="production",
                max_candidates=8,
                pass_threshold=0.85,
                description="Production model, full evaluation",
            ),
            EvalStage(
                name="rotating_practice",
                cost_per_eval=0.04,
                model_tier="production",
                max_candidates=2,
                pass_threshold=0.88,
                description="Multiple seeds, rotating cases",
            ),
            EvalStage(
                name="mainnet",
                cost_per_eval=0.04,
                model_tier="mainnet",
                max_candidates=1,
                pass_threshold=0.0,
                description="Paid mainnet evaluation",
            ),
        ])

    def default_trajectoryrl_cascade(self) -> "CascadeEvaluator":
        """Default cascade for TrajectoryRL SN11."""
        return CascadeEvaluator(stages=[
            EvalStage(
                name="static_gates",
                cost_per_eval=0.0,
                model_tier="static",
                max_candidates=500,
                pass_threshold=0.3,
                description="Format validation, skill structure checks",
            ),
            EvalStage(
                name="local_eval",
                cost_per_eval=0.10,
                model_tier="medium",
                max_candidates=50,
                pass_threshold=0.6,
                description="Local TrajRL evaluator on sandbox",
            ),
            EvalStage(
                name="adversarial_holdout",
                cost_per_eval=0.20,
                model_tier="production",
                max_candidates=10,
                pass_threshold=0.75,
                description="Hidden test cases",
            ),
            EvalStage(
                name="mainnet",
                cost_per_eval=0.44,
                model_tier="mainnet",
                max_candidates=1,
                pass_threshold=0.0,
                description="Paid submission (must beat incumbent by 3%)",
            ),
        ])

    def default_gradients_cascade(self) -> "CascadeEvaluator":
        """Default cascade for Gradients SN56."""
        return CascadeEvaluator(stages=[
            EvalStage(
                name="code_review",
                cost_per_eval=0.0,
                model_tier="static",
                max_candidates=100,
                pass_threshold=0.5,
                description="Code quality, reproducibility checks",
            ),
            EvalStage(
                name="quick_train",
                cost_per_eval=0.05,
                model_tier="cheap",
                max_candidates=20,
                pass_threshold=0.4,
                description="Short training run on small subset",
            ),
            EvalStage(
                name="tournament_submit",
                cost_per_eval=0.25,
                model_tier="production",
                max_candidates=3,
                pass_threshold=0.0,
                description="Submit to validator-provided GPU",
            ),
        ])

    def evaluate_cascade(
        self,
        candidates: list[CandidateGenome],
        custom_evaluators: Optional[dict[str, Callable]] = None,
    ) -> list[CandidateGenome]:
        """Run candidates through the cascade."""
        remaining = list(candidates)

        for stage in self.stages:
            if not remaining:
                break

            # Trim to stage capacity
            remaining = remaining[:stage.max_candidates]

            # Apply custom evaluator if available
            if custom_evaluators and stage.name in custom_evaluators:
                evaluator = custom_evaluators[stage.name]
            elif stage.evaluator:
                evaluator = stage.evaluator
            else:
                # Default: pass through with simulated score
                evaluator = None

            passed = []
            for genome in remaining:
                if evaluator:
                    score = evaluator(genome)
                    if score is not None:
                        genome.local_scores.append(score)
                        self.evaluations_run += 1
                        self.total_cost += stage.cost_per_eval
                        if score >= stage.pass_threshold:
                            passed.append(genome)
                    else:
                        passed.append(genome)  # pass if evaluator returns None
                else:
                    # Simulate pass
                    genome.local_scores.append(0.5)
                    passed.append(genome)

            remaining = passed

        return remaining

    def estimate_cost(self, num_candidates: int) -> dict[str, Any]:
        """Estimate total cost for evaluating N candidates."""
        costs = []
        remaining = num_candidates
        total = 0.0

        for stage in self.stages:
            if remaining <= 0:
                break
            stage_count = min(remaining, stage.max_candidates)
            stage_cost = stage_count * stage.cost_per_eval
            costs.append({
                "stage": stage.name,
                "candidates": stage_count,
                "cost_per_eval": stage.cost_per_eval,
                "stage_total": stage_cost,
            })
            total += stage_cost
            remaining -= stage_count

        return {
            "stages": costs,
            "total_cost_usd": total,
            "total_candidates": num_candidates,
            "surviving_candidates": remaining,
        }

    def stats(self) -> dict[str, Any]:
        return {
            "stages": len(self.stages),
            "evaluations_run": self.evaluations_run,
            "total_cost_usd": self.total_cost,
            "stage_names": [s.name for s in self.stages],
        }
