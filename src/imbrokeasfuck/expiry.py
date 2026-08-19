"""Expiry tracker — precise deal expiry with hour-level precision."""
from __future__ import annotations
import json
import re
from datetime import datetime, timezone, timedelta
from typing import Optional


def parse_expiry(text: str) -> Optional[dict]:
    """Extract expiry information from text."""
    patterns = [
        (r'ends?\s+(\w+\s+\d{1,2},?\s+\d{4})', "%B %d, %Y"),
        (r'ends?\s+in\s+(\d+)\s+days?', None),
        (r'deadline[:\s]+(\w+\s+\d{1,2},?\s+\d{4})', "%B %d, %Y"),
        (r'(\d{4}-\d{2}-\d{2})', None),
    ]
    for pattern, fmt in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            try:
                if fmt:
                    dt = datetime.strptime(match.group(1), fmt)
                else:
                    dt = datetime.fromisoformat(match.group(1).replace("Z", "+00:00"))
                hours = (dt - datetime.now()).total_seconds() / 3600
                return {
                    "expires_at": dt.isoformat(),
                    "hours_remaining": round(hours, 1),
                    "status": "active" if hours > 24 else "expiring_soon" if hours > 0 else "expired",
                    "raw": match.group(1),
                }
            except:
                pass
    return None


def classify_status(expires_at: str) -> str:
    try:
        dt = datetime.fromisoformat(expires_at)
        hours = (dt - datetime.now()).total_seconds() / 3600
        if hours <= 0: return "expired"
        if hours <= 24: return "expiring_soon"
        if hours <= 168: return "active"
        return "future"
    except:
        return "unknown"
