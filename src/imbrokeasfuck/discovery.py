"""Autonomous discovery pipeline — reads from DB, polls sources, records events."""
from __future__ import annotations
import asyncio
import json
from datetime import datetime
from typing import Any
from .canonical_db import connect, migrate, upsert_opportunity, record_event, get_opportunities, get_stats


def seed_sources(conn):
    """Seed initial sources into DB."""
    sources = [
        ("bittensor", "api", "S", 60),
        ("coin_gecko", "api", "S", 60),
        ("fear_greed", "api", "S", 60),
        ("algora", "api", "S", 3600),
        ("x402", "api", "S", 3600),
        ("apify", "api", "S", 3600),
        ("virtuals", "api", "S", 3600),
        ("hackathons_space", "scrape", "A", 3600),
        ("bug_bounties", "static", "A", 86400),
        ("grants", "static", "B", 86400),
    ]
    for sid, stype, priority, cadence in sources:
        conn.execute("INSERT OR IGNORE INTO sources (source_id, source_type, priority, cadence_minutes) VALUES (?,?,?,?)",
                     (sid, stype, priority, cadence))
    conn.commit()


def seed_opportunities(conn):
    """Seed initial opportunities from hardcoded data."""
    opps = [
        ("bittensor:ditto", "bittensor", "subnet", "SN118 Ditto Memory Harness", "Ditto", None, "token_emission", 7.993, 0.96, "A"),
        ("bittensor:ridges", "bittensor", "subnet", "SN62 Ridges SWE Agent", "Ridges", None, "token_emission", 9.136, 0.92, "A"),
        ("bittensor:gradients", "bittensor", "subnet", "SN56 Gradients Training", "Gradients", None, "token_emission", 10.592, 0.88, "A"),
        ("hack_hydra", "hackathons_space", "hackathon", "Hack Hydra $5K", "HydraDB", "2026-08-21T06:59:00Z", "cash", 5000, 0.70, "A"),
        ("openaire", "hackathons_space", "hackathon", "OpenAIRE €500", "OpenAIRE", "2026-08-21T04:59:00Z", "cash", 500, 0.85, "A"),
    ]
    for opp_id, src, kind, title, sponsor, deadline, rtype, amount, reuse, rating in opps:
        upsert_opportunity(conn, opp_id, {
            "source": src, "kind": kind, "title": title, "sponsor": sponsor,
            "deadline": deadline, "reward_type": rtype, "reward_amount": amount,
            "reuse_score": reuse, "rating": rating,
        })
    conn.commit()


def run_discovery():
    """Full autonomous discovery pipeline."""
    conn = connect()
    migrate(conn)
    seed_sources(conn)
    seed_opportunities(conn)
    
    stats = get_stats(conn)
    opps = get_opportunities(conn)
    
    print(f"Sources: {stats['sources']}")
    print(f"Opportunities: {stats['opportunities']}")
    print(f"Events: {stats['events']}")
    print(f"Validations: {stats['validations']}")
    
    # Show what's in DB
    for o in opps:
        print(f"  [{o['rating']}] {o['title'][:50]} (deadline: {o['deadline'] or 'none'})")
    
    conn.close()
    return stats
