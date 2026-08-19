"""Calibration model — learn mainnet ↔ local score correlation."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Optional
import json


@dataclass
class CalibrationPoint:
    """A single calibration observation."""
    genome_id: str
    local_score: float
    mainnet_score: float
    rank_achieved: Optional[int] = None
    paid: bool = False
    timestamp: str = ""


@dataclass
class CalibrationModel:
    """Learn the mapping between local and mainnet scores."""

    factory: str = ""
    subnet: int = 0

    # Observations
    points: list[CalibrationPoint] = field(default_factory=list)

    # Learned parameters (simple linear for now)
    slope: float = 1.0
    intercept: float = 0.0
    r_squared: float = 0.0

    # Uncertainty
    residual_std: float = 0.1
    min_observations: int = 5

    def add_observation(
        self,
        genome_id: str,
        local_score: float,
        mainnet_score: float,
        rank_achieved: Optional[int] = None,
        paid: bool = False,
        timestamp: str = "",
    ):
        """Add a calibration observation."""
        self.points.append(CalibrationPoint(
            genome_id=genome_id,
            local_score=local_score,
            mainnet_score=mainnet_score,
            rank_achieved=rank_achieved,
            paid=paid,
            timestamp=timestamp,
        ))
        self._recalculate()

    def _recalculate(self):
        """Recalculate linear regression parameters."""
        if len(self.points) < 2:
            return

        xs = [p.local_score for p in self.points]
        ys = [p.mainnet_score for p in self.points]
        n = len(xs)

        mean_x = sum(xs) / n
        mean_y = sum(ys) / n

        ss_xy = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys))
        ss_xx = sum((x - mean_x) ** 2 for x in xs)
        ss_yy = sum((y - mean_y) ** 2 for y in ys)

        if ss_xx > 0:
            self.slope = ss_xy / ss_xx
            self.intercept = mean_y - self.slope * mean_x

        if ss_yy > 0 and ss_xx > 0:
            self.r_squared = (ss_xy ** 2) / (ss_xx * ss_yy)

        # Calculate residual standard deviation
        residuals = [y - (self.slope * x + self.intercept) for x, y in zip(xs, ys)]
        if len(residuals) > 2:
            self.residual_std = (sum(r ** 2 for r in residuals) / (len(residuals) - 2)) ** 0.5

    def predict_mainnet(self, local_score: float) -> dict[str, Any]:
        """Predict mainnet score from local score."""
        predicted = self.slope * local_score + self.intercept
        ci_lower = predicted - 1.96 * self.residual_std
        ci_upper = predicted + 1.96 * self.residual_std

        return {
            "predicted_mainnet": predicted,
            "confidence_interval_lower": ci_lower,
            "confidence_interval_upper": ci_upper,
            "residual_std": self.residual_std,
            "r_squared": self.r_squared,
            "calibrated": len(self.points) >= self.min_observations,
        }

    def predict_top5_probability(self, local_score: float) -> float:
        """Estimate probability of reaching top-5 based on calibration."""
        if len(self.points) < self.min_observations:
            return 0.5  # uninformative prior

        pred = self.predict_mainnet(local_score)
        if not pred["calibrated"]:
            return 0.5

        # Estimate from historical paid thresholds
        paid_scores = [p.mainnet_score for p in self.points if p.paid]
        if not paid_scores:
            return 0.3

        min_paid = min(paid_scores)
        mean = pred["predicted_mainnet"]
        std = pred["residual_std"]

        if std == 0:
            return 1.0 if mean >= min_paid else 0.0

        # P(score >= min_paid) using normal approximation
        z = (mean - min_paid) / std
        # Approximate normal CDF
        return 0.5 * (1 + _erf(z / (2 ** 0.5)))

    def should_submit(self, local_score: float, cost_usd: float) -> dict[str, Any]:
        """Decide whether to submit based on calibration + cost."""
        pred = self.predict_mainnet(local_score)
        p_top5 = self.predict_top5_probability(local_score)

        # Expected value calculation
        # Simplified: assume $266/day for #5 position if we get paid
        daily_reward_if_paid = 266.0  # conservative estimate
        ev = p_top5 * daily_reward_if_paid
        net_ev = ev - cost_usd

        return {
            "should_submit": net_ev > 0 and p_top5 > 0.1,
            "probability_top5": p_top5,
            "expected_value_usd": ev,
            "net_expected_value_usd": net_ev,
            "cost_usd": cost_usd,
            "calibrated": pred["calibrated"],
            "prediction": pred,
        }

    def stats(self) -> dict[str, Any]:
        paid_count = sum(1 for p in self.points if p.paid)
        return {
            "observations": len(self.points),
            "paid_observations": paid_count,
            "slope": self.slope,
            "intercept": self.intercept,
            "r_squared": self.r_squared,
            "residual_std": self.residual_std,
            "calibrated": len(self.points) >= self.min_observations,
        }

    def to_dict(self) -> dict[str, Any]:
        return {
            "factory": self.factory,
            "subnet": self.subnet,
            "stats": self.stats(),
            "points": [
                {
                    "local": p.local_score,
                    "mainnet": p.mainnet_score,
                    "rank": p.rank_achieved,
                    "paid": p.paid,
                }
                for p in self.points
            ],
        }


def _erf(x: float) -> float:
    """Approximation of the error function."""
    a1 = 0.254829592
    a2 = -0.284496736
    a3 = 1.421413741
    a4 = -1.453152027
    a5 = 1.061405429
    p = 0.3275911
    sign = 1 if x >= 0 else -1
    x = abs(x)
    t = 1.0 / (1.0 + p * x)
    y = 1.0 - (((((a5 * t + a4) * t) + a3) * t + a2) * t + a1) * t * (x ** 2 * -1).exp()
    return sign * y
