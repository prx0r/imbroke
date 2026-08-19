"""Deadline tracker — what's coming up soon."""
from __future__ import annotations
from datetime import datetime, timedelta
from typing import Any
from ..oracle.opportunity import Opportunity

def days_until(date_str: str) -> int:
    try:
        target = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        return (target - datetime.now(target.tzinfo)).days
    except Exception:
        return 999

def urgency_tag(days: int) -> str:
    if days <= 0: return "EXPIRED"
    if days <= 2: return "URGENT"
    if days <= 7: return "SOON"
    if days <= 30: return "UPCOMING"
    return "FUTURE"

def prioritize_by_deadline(opportunities: list) -> list:
    """Sort opportunities by deadline urgency."""
    return sorted(opportunities, key=lambda o: days_until(o.deadline) if o.deadline else 999)

def get_expiring_soon(opportunities: list, within_days: int = 7) -> list:
    """Get opportunities expiring within N days."""
    return [o for o in opportunities if o.deadline and days_until(o.deadline) <= within_days]
