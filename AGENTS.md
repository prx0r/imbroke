# AGENTS.md — imbrokeasfuck

## The Core Principle

**NEVER prompt an agent with what to validate. The agent must READ from the database and DECIDE what to do.**

---

## BAD BEHAVIOURS

1. Don't tell Hermes what to verify — let it read the DB
2. Don't hardcode data in prompts
3. Don't skip the database
4. Don't run the same test twice
5. Don't prompt with the answer

## GOOD BEHAVIOURS

1. Read DB → identify gaps → execute skill → log result
2. Use skills (opportunity-hunter, verify, monitor)
3. Let the agent decide what to do
4. Log everything to the database
5. Be autonomous

## Architecture

```
canonical_db.py  — SQLite store (sources, opportunities, events)
discovery.py     — reads DB, seeds data, runs pipeline
orchestrator.py  — reads DB, identifies work, dispatches
mcp_server.py    — 3 tools for Dell/agents
merkle.py        — data integrity proofs
verifier.py      — verification ladder
scoring.py       — opportunity scoring
```

## How it works

```
1. DB has sources registered (10 sources)
2. DB has opportunities seeded (23)
3. Discovery reads DB to know what exists
4. Polls sources based on cadence
5. Records events when things change
6. Validates data from multiple sources
7. MCP exposes verified data to Dell/agents
```

## What's tested

| Component | Status |
|-----------|--------|
| Canonical DB | ✅ 23 opportunities, 10 sources |
| Merkle proofs | ✅ Verified |
| MCP server | ✅ 3 tools |
| Validation | ✅ 8/9 |
| Orchestrator | ✅ Reads DB, identifies work |

## What's next

1. Real polling (not just seed data)
2. Blog monitoring for new opportunities
3. Make MCP tools do real verification
4. Autonomous Hermes execution
