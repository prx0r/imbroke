"""Seed all reference opportunities into the database."""
from __future__ import annotations
from .canonical_db import connect, migrate, upsert_opportunity


ALL_OPPORTUNITIES = [
    # Bittensor subnets
    ("bittensor:ditto", "bittensor", "subnet", "SN118 Ditto Memory Harness", "Ditto", None, "token_emission", 7.993, 0.96, "A"),
    ("bittensor:trajectoryrl", "bittensor", "subnet", "SN11 TrajectoryRL Skills", "TrajectoryRL", None, "token_emission", 5.08, 0.94, "A"),
    ("bittensor:ridges", "bittensor", "subnet", "SN62 Ridges SWE Agent", "Ridges", None, "token_emission", 9.136, 0.92, "A"),
    ("bittensor:redteam", "bittensor", "subnet", "SN61 RedTeam Security", "RedTeam", None, "token_emission", 3.84, 0.72, "B"),
    ("bittensor:oro", "bittensor", "subnet", "SN15 ORO Shopping Agent", "ORO", None, "token_emission", 10.0, 0.65, "B"),
    # Hackathons
    ("hack_hydra", "hackathons_space", "hackathon", "Hack Hydra $5K", "HydraDB", "2026-08-21T06:59:00Z", "cash", 5000, 0.70, "A"),
    ("openaire", "hackathons_space", "hackathon", "OpenAIRE AI Hackathon €500", "OpenAIRE", "2026-08-21T04:59:00Z", "cash", 500, 0.85, "A"),
    ("telegraph", "hackathons_space", "hackathon", "Telegraph Hackathon $5K", "Telegraph", "2026-09-07T00:00:00Z", "cash", 5000, 0.80, "A"),
    ("decentralize_ai", "hackathons_space", "hackathon", "Decentralize AI Hackathon", "HackerNoon", "2026-10-31T00:00:00Z", "cash", 0, 0.60, "B"),
    # Bug bounties
    ("bounty:immunefi", "bug_bounties", "bounty", "Immunefi Web3 Bounties", "Immunefi", None, "cash", 0, 0.30, "A"),
    ("bounty:sherlock", "bug_bounties", "bounty", "Sherlock DeFi Audits", "Sherlock", None, "cash", 0, 0.30, "A"),
    ("bounty:code4rena", "bug_bounties", "bounty", "Code4rena Audits", "Code4rena", None, "cash", 0, 0.30, "A"),
    ("bounty:hackenproof", "bug_bounties", "bounty", "HackenProof Bounties", "HackenProof", None, "cash", 0, 0.30, "A"),
    # Grants
    ("grant:nosana", "grants", "grant", "Nosana Grants $5K-$50K", "Nosana", None, "grant", 50000, 0.80, "A"),
    ("grant:akash", "grants", "grant", "Akash Ecosystem Grants", "Akash", None, "grant", 0, 0.70, "A"),
    ("grant:heurist", "grants", "grant", "Heurist Developer Credits", "Heurist", None, "credits", 10000, 0.60, "B"),
    ("grant:litvm", "grants", "grant", "LitVM Builders Testnet", "LitVM", None, "grant", 0, 0.50, "B"),
    ("grant:vana", "grants", "grant", "Vana Data Grants", "Vana", None, "grant", 0, 0.50, "B"),
    ("grant:arweave", "grants", "grant", "Arweave/AO Onboard $1.5K-$10K", "Arweave", None, "credits", 10000, 0.50, "B"),
    # DeFAI
    ("defai:bite", "defai", "protocol", "Bitte/Amadeus Agent Hub", "Amadeus", None, "token_emission", 0, 0.30, "B"),
    ("defai:wayfinder", "defai", "protocol", "Wayfinder Protocol", "Parallel", None, "token_emission", 0, 0.30, "B"),
    ("defai:debank", "defai", "protocol", "DeBank Cloud API", "DeBank", None, "service", 0, 0.30, "B"),
]

def seed_all():
    conn = connect()
    migrate(conn)
    for opp_id, src, kind, title, sponsor, deadline, rtype, amount, reuse, rating in ALL_OPPORTUNITIES:
        upsert_opportunity(conn, opp_id, {
            "source": src, "kind": kind, "title": title, "sponsor": sponsor,
            "deadline": deadline, "reward_type": rtype, "reward_amount": amount,
            "reuse_score": reuse, "rating": rating,
        })
    conn.commit()
    count = conn.execute("SELECT COUNT(*) FROM opportunities").fetchone()[0]
    conn.close()
    print(f"Seeded {count} opportunities")
