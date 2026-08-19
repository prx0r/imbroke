"""Data Validator — uses Dell patterns to verify opportunity data."""
from __future__ import annotations
import time
import httpx
from typing import Any, Optional
from dataclasses import dataclass, field


@dataclass
class ValidationResult:
    field: str
    expected: Any
    actual: Any
    status: str  # VERIFIED | MISMATCH | UNVERIFIED | ERROR
    source: str = ""
    confidence: float = 0.0


@dataclass
class OpportunityValidator:
    """Validate opportunity data using Dell-style health checks."""
    
    def validate_prize(self, name: str, expected: float, source_url: str) -> ValidationResult:
        """Validate prize amount against source."""
        return ValidationResult(
            field="prize",
            expected=expected,
            actual=expected,  # would fetch from URL
            status="UNVERIFIED",
            source=source_url,
            confidence=0.5,
        )
    
    def validate_deadline(self, name: str, deadline: str) -> ValidationResult:
        """Validate deadline is in the future."""
        from datetime import datetime
        try:
            d = datetime.fromisoformat(deadline.replace("Z", "+00:00"))
            now = datetime.now(d.tzinfo)
            days = (d - now).days
            status = "VERIFIED" if days > 0 else "EXPIRED"
            return ValidationResult(
                field="deadline",
                expected=deadline,
                actual=f"{days} days remaining",
                status=status,
                confidence=1.0 if days > 0 else 0.0,
            )
        except Exception:
            return ValidationResult(
                field="deadline", expected=deadline, actual="parse error",
                status="ERROR", confidence=0.0,
            )
    
    def validate_url(self, url: str) -> ValidationResult:
        """Check if URL is reachable."""
        try:
            r = httpx.get(url, timeout=10, follow_redirects=True)
            return ValidationResult(
                field="url",
                expected=url,
                actual=f"HTTP {r.status_code}",
                status="VERIFIED" if r.status_code < 400 else "ERROR",
                confidence=1.0 if r.status_code < 400 else 0.0,
            )
        except Exception as e:
            return ValidationResult(
                field="url", expected=url, actual=str(e)[:50],
                status="ERROR", confidence=0.0,
            )
    
    def validate_live(self, name: str, url: str) -> ValidationResult:
        """Check if service/competition is actually live."""
        try:
            r = httpx.get(url, timeout=10, follow_redirects=True)
            live = r.status_code == 200
            return ValidationResult(
                field="live",
                expected=True,
                actual=live,
                status="VERIFIED" if live else "DOWN",
                source=url,
                confidence=1.0 if live else 0.0,
            )
        except Exception:
            return ValidationResult(
                field="live", expected=True, actual=False,
                status="DOWN", confidence=0.0,
            )
    
    def validate_opportunity(self, opp: dict) -> list[ValidationResult]:
        """Validate all fields of an opportunity."""
        results = []
        
        # Validate deadline
        if opp.get("deadline"):
            results.append(self.validate_deadline(opp.get("title", ""), opp["deadline"]))
        
        # Validate source URL
        if opp.get("source_url"):
            results.append(self.validate_url(opp["source_url"]))
        
        # Validate prize
        if opp.get("reward_usd"):
            results.append(self.validate_prize(
                opp.get("title", ""), opp["reward_usd"],
                opp.get("source_url", ""),
            ))
        
        return results
