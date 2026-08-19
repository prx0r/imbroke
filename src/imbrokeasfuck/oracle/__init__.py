"""Opportunity Oracle — machine-readable market for autonomous coding agents."""
from .opportunity import Opportunity
from .feeds import ingest_all
from .github_signals import scan_all_github_signals
from .bittensor_economics import SUBNET_CONTRACTS, format_all_economics, format_economics, MinerContract

__all__ = [
    "Opportunity",
    "ingest_all",
    "scan_all_github_signals",
    "fetch_subnet_economics",
    "SUBNET_ECONOMICS",
]
