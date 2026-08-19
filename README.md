# imbrokeasfuck

Crypto AI opportunity tracker + economic factory system.

## What it does

```
15 sources → Oracle → Validation → Deadline → Priority
     ↓
  23 opportunities (DB-backed)
     ↓
  MCP exposure for Dell/agents
     ↓
  Autonomous orchestration
```

## Quick start

```bash
cd imbrokeasfuck
pip install -e .

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

## Architecture

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
├── merkle.py            # Data integrity proofs
├── verifier.py          # Verification ladder
├── scoring.py           # Opportunity scoring
├── expiry.py            # Deadline tracking
├── tracker.py           # 17 project tracking
├── oracle/              # 15 sources, 54+ opportunities
│   ├── sources/         # 15 adapters
│   ├── feeds.py         # Ingestion
│   └── three_pass.py    # Validation
└── earn/                # Factories, evolution, revenue
    ├── factory.py       # MAP-Elites
    ├── genome.py        # Candidates
    ├── revenue.py       # Serve-to-earn
    └── strategy.py      # 60/25/15
```

## API Endpoints

```
GET /api/v1/models          # project registry
GET /api/v1/opportunities   # oracle feed
GET /api/v1/hackathons      # 7 targets
GET /api/v1/subnets         # 8 Bittensor subnets
GET /api/v1/economics       # miner math
GET /api/v1/deals           # tracked opportunities
GET /api/v1/prices          # token prices
GET /api/v1/fear-greed      # market sentiment
GET /api/v1/stats           # system stats
GET /api/v1/validate        # 3-pass validation
GET /api/v1/strategy        # 60/25/15
```

## MCP Tools

```
qdw_opportunities — list all tracked opportunities
qdw_validate — verify against multiple sources
qdw_stats — system statistics
```

## What's next

1. Real polling (not just seed data)
2. Blog monitoring for new opportunities
3. Make MCP tools do real verification
4. Autonomous Hermes execution
