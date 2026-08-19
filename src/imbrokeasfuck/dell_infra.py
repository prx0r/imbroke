"""Dell-style infrastructure — stolen from neverbrokeagain-dell.

Key patterns:
- Source health tracking (degradation detection)
- Provider hot-swap (failover on errors)
- Canary checks (daily liveness)
- Event recording (append-only changes)
- CandidateOffer (typed validation)
"""
from __future__ import annotations
import time
import httpx
from dataclasses import dataclass, field
from typing import Any, Optional


# ── Source Health (from source_health.py) ──────────────────────────────────

DEGRADATION_THRESHOLD = 3
RECOVERY_THRESHOLD = 2

_health_state: dict[str, dict] = {}

def record_fetch(source_id: str, success: bool, latency_ms: float = 0, error: str = None):
    """Record a fetch attempt for a source."""
    now = time.time()
    if source_id not in _health_state:
        _health_state[source_id] = {
            "total_fetches": 0, "successes": 0, "failures": 0,
            "consecutive_failures": 0, "consecutive_successes": 0,
            "last_fetch_time": None, "last_success_time": None,
            "status": "unknown", "degraded_since": None,
        }
    s = _health_state[source_id]
    s["total_fetches"] += 1
    s["last_fetch_time"] = now
    if success:
        s["successes"] += 1
        s["consecutive_successes"] += 1
        s["consecutive_failures"] = 0
        s["last_success_time"] = now
        if s["consecutive_successes"] >= RECOVERY_THRESHOLD:
            s["status"] = "healthy"
            s["degraded_since"] = None
    else:
        s["failures"] += 1
        s["consecutive_failures"] += 1
        s["consecutive_successes"] = 0
        s["last_error"] = error
        if s["consecutive_failures"] >= DEGRADATION_THRESHOLD:
            s["status"] = "failed"
            s["degraded_since"] = now
        elif s["consecutive_failures"] >= 1:
            s["status"] = "degraded"

def get_source_health(source_id: str) -> dict:
    return _health_state.get(source_id, {"status": "unknown"})


# ── Canary (from canary.py) ───────────────────────────────────────────────

async def canary_check(url: str, name: str) -> dict:
    """Daily liveness check for a source."""
    try:
        start = time.time()
        async with httpx.AsyncClient(timeout=10) as c:
            r = await c.get(url, follow_redirects=True)
            latency = (time.time() - start) * 1000
            return {
                "source": name,
                "status": "live" if r.status_code < 400 else "error",
                "http_status": r.status_code,
                "latency_ms": round(latency, 2),
                "checked_at": datetime.now().isoformat(),
            }
    except Exception as e:
        return {"source": name, "status": "unreachable", "error": str(e)[:50]}


# ── Event Recorder (from event_recorder.py) ───────────────────────────────

_events: list[dict] = []

def record_event(event_type: str, entity_id: str, details: dict = None):
    """Append-only event recording."""
    event = {
        "event_type": event_type,
        "entity_id": entity_id,
        "timestamp": datetime.now().isoformat(),
        "details": details or {},
    }
    _events.append(event)
    return event

def get_events(entity_id: str = None) -> list[dict]:
    if entity_id:
        return [e for e in _events if e["entity_id"] == entity_id]
    return _events


# ── CandidateOffer (from candidate.py) ────────────────────────────────────

@dataclass
class CandidateOffer:
    """Typed candidate with validation."""
    provider_id: str
    model_id: str = ""
    offer_type: str = "metered_api"
    input_per_m: float = 0
    output_per_m: float = 0
    free: bool = False
    context_tokens: int = 0
    max_output_tokens: int = 0
    eligible: bool = True
    notes: str = ""

    def to_dict(self) -> dict:
        return {k: v for k, v in self.__dict__.items()}

    def validate(self) -> list[str]:
        """Validate offer fields."""
        errors = []
        if not self.provider_id:
            errors.append("missing provider_id")
        if self.input_per_m < 0:
            errors.append("negative input_per_m")
        return errors

from datetime import datetime
