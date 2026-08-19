# Proposal 3: MemoryProof (Hack Hydra)

## Tagline
> A benchmark and debugger for graph memory.

## What it does
Tests whether graph memory systems return attributable, temporally correct, cross-source consistent, reproducible context.

## Problem
Agent memory systems retrieve plausible context. Nobody systematically tests whether it's actually correct.

## Solution
Use Wiggly as ground truth oracle. Auto-generate hard questions. Evaluate HydraDB. Diagnose failures.

## Architecture
```
Wiggly (ground truth)
    │
    ▼
HydraDB (graph-memory projection)
    │
    ├── fast query
    ├── thinking query
    └── multi-hop
    │
    ▼
HydraBench (expected vs actual)
    │
    ▼
Metrics: accuracy, latency, attribution, temporal
```

## Key primitive: BenchmarkSuite
```json
{
  "questions": 50,
  "fast": {"accuracy": 0.82, "median_latency_ms": 340},
  "thinking": {"accuracy": 0.94, "median_latency_ms": 1180},
  "failure_taxonomy": ["WRONG_ENTITY", "STALE_FACT", "FALSE_EDGE"]
}
```

## Demo
1. Export Wiggly corpus to HydraDB
2. Auto-generate 50 benchmark questions
3. Run fast vs thinking evaluation
4. Show accuracy/latency/attribution metrics
5. Show failure analysis
6. Auto-tune Hydra config via evolutionary search

## Why it wins
- Real contribution to HydraDB (benchmark they should ship)
- Not another wrapper — a testing framework
- Uses HydraDB meaningfully (fast vs thinking comparison)

## Tech stack
- Wiggly ground truth engine
- HydraDB MCP (fast/thinking queries)
- QDW evolutionary search for config optimization
- ReactFlow visualization (patalacheckpoints)

## Deadline
Aug 20, 11:59 PM PT (~52 hours)

## Files
- `hackathons/hydra/PLAN.md`
- `vendor/wiggly/patala/` — ground truth
- `vendor/patalacheckpoints/` — demo UI
