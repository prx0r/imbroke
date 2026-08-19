# Handover — imbrokeasfuck Project

**Date:** 2026-08-19
**Status:** MVP complete, ready for next phase

---

## What we built

**imbrokeasfuck** is a crypto AI opportunity tracker + economic factory system.

```
15 sources → Oracle → Validation → Deadline → Priority
     ↓
  23 opportunities (DB-backed)
     ↓
  MCP exposure for Dell/agents
     ↓
  Autonomous orchestration
```

## What works (tested)

| Component | Status | Test |
|-----------|--------|------|
| Canonical DB | ✅ | 23 opportunities, 10 sources |
| MCP server | ✅ | 3 tools, 23 opportunities exposed |
| Validation | ✅ | 8/9 key facts verified |
| Orchestrator | ✅ | Reads DB, identifies work |
| Scheduler | ✅ | Systemd services ready |
| 3 Hermes skills | ✅ | Hunter, verify, monitor |
| AGENTS.md | ✅ | Good/bad behaviours documented |

## What's NOT done (honest)

| Gap | Impact | How to fix |
|-----|--------|-----------|
| Sources never polled | Data is static | Run orchestrator hourly |
| MCP tools are shells | No real logic | Implement actual verification |
| No blog monitoring | Missing new opportunities | Add RSS/scraper adapters |
| No Merkle proofs | Data integrity unverified | Add hash chain to ledger |
| No live validation | Only string matching | Add semantic verification |

## Files

```
src/imbrokeasfuck/
├── apis.py              # CoinGecko, DefiLlama, Fear/Greed
├── bittensor.py         # Subnet economics
├── cli.py               # 15+ commands
├── canonical_db.py      # SQLite store
├── discovery.py         # Autonomous pipeline
├── orchestrator.py      # Reads DB, identifies work
├── mcp_server.py        # 3 MCP tools
├── server.py            # 14 API endpoints
├── scorer.py            # Opportunity scoring
├── verifier.py          # Verification ladder
├── expiry.py            # Deadline tracking
├── tracker.py           # 17 project tracking
├── oracle/              # 15 sources, 54+ opportunities
│   ├── sources/         # 15 adapters
│   ├── feeds.py         # Ingestion
│   ├── three_pass.py    # Validation
│   └── validator.py     # Dell-style checks
└── earn/                # Factories, evolution, revenue
    ├── factory.py       # MAP-Elites
    ├── genome.py        # Candidates
    ├── revenue.py       # Serve-to-earn
    └── strategy.py      # 60/25/15
```

## How to use

```bash
# Run orchestrator
PYTHONPATH=src python3 -m imbrokeasfuck.orchestrator

# Run validation
PYTHONPATH=src python3 -m imbrokeasfuck.oracle.three_pass

# Start MCP server
PYTHONPATH=src python3 -m imbrokeasfuck.mcp_server

# CLI
PYTHONPATH=src python3 -m imbrokeasfuck.cli --oracle
PYTHONPATH=src python3 -m imbrokeasfuck.cli --validate
PYTHONPATH=src python3 -m imbrokeasfuck.cli --strategy
```

## What's next

1. Implement real polling (not just seed data)
2. Add blog monitoring for new opportunities
3. Add Merkle proofs for data integrity
4. Make MCP tools do real verification
5. Wire Hermes to execute skills autonomously
