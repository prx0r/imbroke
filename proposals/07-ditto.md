# Proposal 7: Ditto Memory Harness (Bittensor SN118)

## Tagline
> Compete on memory architecture, not GPU ownership.

## What it does
Submit an agent-memory harness to Ditto SN118 for evaluation on DittoBench.

## Problem
Ditto benchmarks memory harnesses. Current leaderboard has ~65 submissions, top scores 0.955/0.944/0.918.

## Solution
Build QDW factory that evolves memory harness variants against DittoBench locally, then submits the best.

## Architecture
```
Wiggly memory primitives
    │
    ▼
CandidateGenome (retriever, embedding, schema, compression, prompt)
    │
    ▼
Local DittoBench evaluation
    │
    ▼
MAP-Elites evolution (50 candidates, 15 niches)
    │
    ▼
Top candidate → 0.04 TAO submission
```

## Economics
- Submission cost: 0.04 TAO (~$8)
- #5 position: ~$266/day
- 5 paying slots (65/14/10/7/4 distribution)
- No GPU required

## Why it wins
- Deterministic public benchmark
- Local practice before paying
- QDW memory/context primitives directly applicable

## Files
- `vendor/ditto-subnet/` — reference implementation
- `vendor/dfresearch/` — evolutionary loop pattern
- `src/imbrokeasfuck/earn/factory.py` — CompetitionFactory
- `src/imbrokeasfuck/earn/genome.py` — CandidateGenome
