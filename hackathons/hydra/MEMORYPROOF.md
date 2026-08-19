# Hack Hydra — MemoryProof

**Deadline:** August 20, 2026, 11:59 PM PT (~52 hours)
**Prize:** $5,000
**Focus:** Technical depth, originality, execution, meaningful use of HydraDB

## Product: MemoryProof

> **Property-based testing and evolutionary optimization for graph memory.**

NOT "agent that remembers things." NOT "Sanskrit chatbot."

A **benchmark + debugger for graph memory correctness**.

## What to build

MemoryProof automatically constructs hard, provenance-backed memory tasks from real evolving knowledge graphs, evaluates HydraDB retrieval under multiple configurations, diagnoses why recalls fail, and generates reproducible regression suites.

## Architecture

```
           WIGGLY / PATALA
        evidence-state machine
                │
         ground truth graph
                │
                ▼
             HydraDB
      graph-memory projection
                │
    ┌───────────┼───────────┐
    ▼           ▼           ▼
 fast       thinking    multi-hop
    │           │           │
    └───────────┼───────────┘
                ▼
            MEMORYPROOF
                │
    expected answer vs actual
                │
    ┌───────────┼───────────┐
    ▼           ▼           ▼
accuracy   provenance   temporal
    │           │           │
    └───────────┼───────────┘
                ▼
              DEMO
```

## Auto-generated questions

From Wiggly's ground truth:

```
FACTUAL: Who authored Work A?
MULTI-HOP: Which institution is associated with the author of Work A?
PROVENANCE: Which independent sources support the authorship?
CONTRADICTION: Which provider disagrees about the author?
TEMPORAL: What was the accepted title before event t2?
SUPERSESSION: Which translation is currently authoritative?
NEGATIVE: Is there sufficient evidence to claim Person C authored Work A?
```

## Metrics

```json
{
  "questions": 50,
  "fast": {"accuracy": 0.82, "median_latency_ms": 340},
  "thinking": {"accuracy": 0.94, "median_latency_ms": 1180},
  "entity_resolution_accuracy": 0.91,
  "attribution_accuracy": 0.96,
  "temporal_accuracy": 0.88
}
```

## Failure taxonomy

```
WRONG_ENTITY
STALE_FACT
MISSING_EDGE
FALSE_EDGE
SOURCE_COLLAPSE
TEMPORAL_COLLAPSE
OVER_RETRIEVAL
UNDER_RETRIEVAL
UNSUPPORTED_SYNTHESIS
```

## Killer feature: AutoML for memory

Hydra knobs become genome:
```python
Candidate(
    mode="thinking",
    graph_context=True,
    alpha=0.71,
    recency_bias=0.25,
    max_results=8
)
```

QDW evolutionary search:
```
population → benchmark → score → mutate → repeat
```

Result:
```
Generic Hydra: 78%
MemoryProof-optimized: 91%
Latency: -17%
```

## CLI deliverables

```bash
memoryproof run corpus/
memoryproof compare --mode fast,thinking
memoryproof regress baseline.json
memoryproof optimize
```

## Why this wins

- **Real contribution to HydraDB** — a benchmark they should ship
- **Technically deep** — not a wrapper, a testing framework
- **Uses HydraDB meaningfully** — fast vs thinking comparison
- **Reproducible** — anyone can run the benchmark
- **"What your project makes possible"** — every Hydra developer can regression-test memory

## Files

```
hackathons/hydra/MEMORYPROOF.md
hackathons/hydra/PLAN.md
```
