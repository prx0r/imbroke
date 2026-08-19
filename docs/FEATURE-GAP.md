# Feature Gap Analysis — Dell vs imbrokeasfuck

## Critical gaps (must have)

| Dell Feature | Lines | What it does | Our status | Priority |
|-------------|-------|-------------|-----------|----------|
| **router.py** | 464 | 3-stage LLM routing with quota shadow pricing | MISSING | P0 |
| **scoring.py** | 352 | Legitimate scoring (intelligence, speed, cost, reliability) | MISSING | P0 |
| **verification.py** | 355 | Verification ladder with evidence requirements | MISSING | P0 |
| **expiry.py** | 308 | Precise deal expiry tracking | MISSING | P0 |
| **poll.py** | 267 | Autonomous polling scheduler | MISSING | P0 |
| **source_diff.py** | 116 | Detect changes between polls | MISSING | P1 |
| **source_health.py** | 147 | Health tracking per source | MISSING | P1 |
| **event_recorder.py** | 74 | Append-only event log | MISSING | P1 |
| **claims.py** | 213 | Claim management | MISSING | P1 |
| **freshness.py** | 80 | Data freshness tracking | MISSING | P1 |

## What we have

| Our Feature | Lines | Status |
|------------|-------|--------|
| canonical_db.py | 108 | ✅ Basic |
| discovery.py | 68 | ✅ Basic |
| orchestrator.py | ~50 | ✅ Basic |
| mcp_server.py | ~50 | ✅ Basic |
| server.py | ~80 | ✅ Basic |
| cli.py | 238 | ✅ Full |
| oracle/ | ~500 | ✅ Full |

## What to build

1. **router.py** — CPVS routing with quota shadow pricing
2. **scoring.py** — legitimate scoring (intelligence, speed, cost, reliability)
3. **verification.py** — verification ladder with evidence requirements
4. **expiry.py** — precise deal expiry tracking
5. **poll.py** — autonomous polling scheduler
6. **source_diff.py** — detect changes between polls
7. **source_health.py** — health tracking per source
8. **event_recorder.py** — append-only event log
