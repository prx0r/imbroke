"""MAP-Elites population manager — behavioral niches with diversity."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Optional
import random
import json
from .genome import CandidateGenome, GenomeSpace


@dataclass
class Niche:
    """A behavioral niche in MAP-Elites."""
    cost: str
    approach: str
    best_candidate: Optional[CandidateGenome] = None
    candidates: list[str] = field(default_factory=list)  # genome_ids
    evaluations: int = 0

    @property
    def key(self) -> str:
        return f"{self.cost}:{self.approach}"

    @property
    def filled(self) -> bool:
        return self.best_candidate is not None


@dataclass
class MAPElites:
    """MAP-Elites population manager."""

    space: GenomeSpace
    max_niches: int = 50
    max_per_niche: int = 10
    mutation_rate: float = 0.2
    crossover_rate: float = 0.3

    # Storage
    niches: dict[str, Niche] = field(default_factory=dict)
    all_candidates: dict[str, CandidateGenome] = field(default_factory=dict)
    cemetery: list[CandidateGenome] = field(default_factory=list)

    # Stats
    total_generations: int = 0
    total_evaluations: int = 0

    def __post_init__(self):
        # Initialize niches
        for cost in self.space.cost_bins:
            for approach in self.space.approach_bins:
                key = f"{cost}:{approach}"
                self.niches[key] = Niche(cost=cost, approach=approach)

    def seed_population(self, count: int = 50):
        """Generate initial random population."""
        for _ in range(count):
            genome = self.space.random_genome()
            self.all_candidates[genome.genome_id] = genome
            niche_key = f"{genome.niche_cost}:{genome.niche_approach}"
            if niche_key in self.niches:
                self.niches[niche_key].candidates.append(genome.genome_id)

    def select_parent(self) -> CandidateGenome:
        """Tournament selection."""
        candidates = [c for c in self.all_candidates.values() if c.status != "cemetery"]
        if not candidates:
            return self.space.random_genome()
        tournament = random.sample(candidates, min(3, len(candidates)))
        return max(tournament, key=lambda c: c.local_score() or 0)

    def evolve_generation(self) -> list[CandidateGenome]:
        """Generate next generation of candidates."""
        new_candidates = []

        # Fill empty niches with random
        for niche in self.niches.values():
            if not niche.filled and len(niche.candidates) < 3:
                genome = self.space.random_genome()
                genome.niche_cost = niche.cost
                genome.niche_approach = niche.approach
                new_candidates.append(genome)

        # Generate mutations
        target = max(10, len(self.all_candidates) // 5)
        for _ in range(target):
            if random.random() < self.crossover_rate and len(self.all_candidates) >= 2:
                parents = random.sample(list(self.all_candidates.values()), 2)
                child = self.space.crossover(parents[0], parents[1])
            else:
                parent = self.select_parent()
                child = self.space.mutate(parent, self.mutation_rate)
            new_candidates.append(child)

        # Register new candidates
        for genome in new_candidates:
            self.all_candidates[genome.genome_id] = genome
            niche_key = f"{genome.niche_cost}:{genome.niche_approach}"
            if niche_key in self.niches:
                self.niches[niche_key].candidates.append(genome.genome_id)

        self.total_generations += 1
        return new_candidates

    def update_niche(self, genome: CandidateGenome):
        """Update niche with evaluated candidate."""
        niche_key = f"{genome.niche_cost}:{genome.niche_approach}"
        if niche_key not in self.niches:
            return

        niche = self.niches[niche_key]
        niche.evaluations += 1

        score = genome.local_score() or 0
        if niche.best_candidate is None or score > (niche.best_candidate.local_score() or 0):
            niche.best_candidate = genome

        # Trim niche if too large
        if len(niche.candidates) > self.max_per_niche:
            # Keep best scoring
            scored = []
            for gid in niche.candidates:
                c = self.all_candidates.get(gid)
                if c and c.status != "cemetery":
                    scored.append((c.local_score() or 0, gid))
            scored.sort(reverse=True)
            niche.candidates = [gid for _, gid in scored[:self.max_per_niche]]

    def retire(self, genome: CandidateGenome, reason: str = "outperformed"):
        """Move candidate to cemetery."""
        genome.status = "cemetery"
        self.cemetery.append(genome)
        # Remove from niche
        niche_key = f"{genome.niche_cost}:{genome.niche_approach}"
        if niche_key in self.niches:
            niche = self.niches[niche_key]
            niche.candidates = [gid for gid in niche.candidates if gid != genome.genome_id]
            if niche.best_candidate and niche.best_candidate.genome_id == genome.genome_id:
                niche.best_candidate = None

    def revive(self, genome_id: str) -> Optional[CandidateGenome]:
        """Revive from cemetery (e.g. after benchmark change)."""
        for i, g in enumerate(self.cemetery):
            if g.genome_id == genome_id:
                g.status = "new"
                self.cemetery.pop(i)
                self.all_candidates[g.genome_id] = g
                niche_key = f"{g.niche_cost}:{g.niche_approach}"
                if niche_key in self.niches:
                    self.niches[niche_key].candidates.append(g.genome_id)
                return g
        return None

    def stats(self) -> dict[str, Any]:
        filled = sum(1 for n in self.niches.values() if n.filled)
        total = len(self.niches)
        return {
            "niches_filled": filled,
            "niches_total": total,
            "niche_fill_rate": filled / total if total else 0,
            "total_candidates": len(self.all_candidates),
            "total_cemetery": len(self.cemetery),
            "total_generations": self.total_generations,
            "total_evaluations": self.total_evaluations,
            "best_per_niche": {
                k: {
                    "score": v.best_candidate.local_score() if v.best_candidate else None,
                    "candidates": len(v.candidates),
                }
                for k, v in self.niches.items()
                if v.filled
            },
        }

    def to_dict(self) -> dict[str, Any]:
        return {
            "factory": self.space.factory,
            "subnet": self.space.subnet,
            "stats": self.stats(),
            "niches": {
                k: {
                    "cost": v.cost,
                    "approach": v.approach,
                    "filled": v.filled,
                    "best_score": v.best_candidate.local_score() if v.best_candidate else None,
                    "candidate_count": len(v.candidates),
                }
                for k, v in self.niches.items()
            },
        }
