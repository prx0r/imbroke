"""Scoring — legitimate scoring based on real data."""
from __future__ import annotations
from typing import Any


def score_opportunity(opp: dict) -> dict:
    """Score an opportunity based on real metrics."""
    score = 0.0
    reasons = []

    # Prize amount (higher = better)
    prize = opp.get("reward_amount", 0)
    if prize > 0:
        score += min(1.0, prize / 10000) * 0.3
        reasons.append(f"prize=${prize}")

    # Reuse score (higher = better)
    reuse = opp.get("reuse_score", 0)
    score += reuse * 0.3
    reasons.append(f"reuse={reuse:.0%}")

    # Rating (A=better)
    rating = opp.get("rating", "C")
    rating_score = {"A": 1.0, "B": 0.7, "C": 0.4}.get(rating, 0.2)
    score += rating_score * 0.2

    # Deadline urgency (closer = more urgent but less time)
    from datetime import datetime
    deadline = opp.get("deadline")
    if deadline:
        try:
            days = (datetime.fromisoformat(deadline) - datetime.now()).days
            if days <= 0:
                score += 0  # expired
            elif days <= 7:
                score += 0.2  # urgent
            elif days <= 30:
                score += 0.1
        except:
            pass

    return {"score": round(score, 3), "reasons": reasons}
