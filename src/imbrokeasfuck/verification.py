"""Verification ladder — evidence requirements for each level."""
from __future__ import annotations
from typing import Any


VERIFICATION_LEVELS = [
    "LEAD",           # opportunity identified
    "SOURCE_FETCHED", # URL is live
    "CLAIM_EXTRACTED",# prize/deadline extracted
    "PRIMARY_EVIDENCE",# found on source page
    "PRIMARY_CORROBORATED",# confirmed by 2nd source
]

VERIFICATION_PREDICATES = {
    "LEAD": {"requirements": []},
    "SOURCE_FETCHED": {"requirements": ["url_returns_200"]},
    "CLAIM_EXTRACTED": {"requirements": ["url_returns_200", "prize_found_on_page"]},
    "PRIMARY_EVIDENCE": {"requirements": ["url_returns_200", "prize_found_on_page", "deadline_found"]},
    "PRIMARY_CORROBORATED": {"requirements": ["url_returns_200", "prize_found_on_page", "confirmed_by_second_source"]},
}


def verify_level(level: str, evidence: dict) -> bool:
    """Check if evidence meets verification level requirements."""
    preds = VERIFICATION_PREDICATES.get(level, {})
    for req in preds.get("requirements", []):
        if not evidence.get(req, False):
            return False
    return True


def next_level(current: str) -> str | None:
    """Get the next verification level."""
    idx = VERIFICATION_LEVELS.index(current) if current in VERIFICATION_LEVELS else -1
    if idx < len(VERIFICATION_LEVELS) - 1:
        return VERIFICATION_LEVELS[idx + 1]
    return None
