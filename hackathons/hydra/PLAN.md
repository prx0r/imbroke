# Hack Hydra — HydraPāṭala ProvenanceBench

**Deadline:** August 20, 2026, 11:59 PM PT (~52 hours from now)
**Prize:** $5,000 total
**Focus:** Technical depth, originality, execution

## Pitch

> Agent memory systems retrieve plausible context. HydraPāṭala tests whether retrieved context is actually attributable, temporally correct, cross-source consistent, and reproducible.

**NOT** "Sanskrit chatbot." A **benchmark for graph memory correctness**.

## Architecture

```
                SOURCE DATA

    GRETIL    OpenAlex    PANDiT    Crossref
       \         |          |          /
        \        |          |         /
                 ▼
            WIGGLY CORE
       canonical truth/evidence
                 │
          ground-truth graph
                 │
                 ▼
              HydraDB
       graph-memory projection
                 │
    ┌────────────┼──────────────┐
    ▼            ▼              ▼
fast query   thinking query   multi-hop
    │            │              │
    └────────────┼──────────────┘
                 ▼
             HYDRABENCH
                 │
     expected answer vs actual
                 │
  ┌──────────────┼────────────────┐
  ▼              ▼                ▼
accuracy      latency      attribution
  │              │                │
  └──────────────┼────────────────┘
                 ▼
               DEMO
```

## What we build

### 1. Wiggly → HydraDB export
- Export canonical entities, assertions, provenance into HydraDB graph
- Map Wiggly's evidence model to HydraDB's graph model

### 2. Auto-generated benchmark questions
From Wiggly's ground truth, generate 30-50 hard questions:

```text
Which sources identify person X as author of work Y?
Did the title/metadata for work X change between observations?
Which two databases disagree about authorship?
Find a work connected to researcher A through publication B and institution C.
Which claims about text X have independent evidence from at least two sources?
Which retrieved answer is supported only by a single provider?
```

### 3. HydraBench evaluator
- Run questions through HydraDB's fast and thinking query modes
- Compare answers against Wiggly's ground truth
- Measure accuracy, latency, attribution correctness

### 4. Demo UI (from patalacheckpoints)
- ReactFlow graph visualization
- Show: Question → Hydra answer → retrieved graph → expected graph
- Visualize: ✓ correct edges, ✗ hallucinated, ? unsupported

## Expected output

```json
{
  "questions": 50,
  "fast": {
    "accuracy": 0.82,
    "median_latency_ms": 340
  },
  "thinking": {
    "accuracy": 0.94,
    "median_latency_ms": 1180
  },
  "entity_resolution_accuracy": 0.91,
  "attribution_accuracy": 0.96,
  "temporal_accuracy": 0.88
}
```

**Only real measured numbers.**

## Repo structure

```
hydrapatala/
    README.md
    export_to_hydra.py     # Wiggly → HydraDB
    generate_questions.py  # Auto-generate benchmark
    evaluate.py            # Run benchmark
    hydrabench.py          # Scoring logic
    demo/
        index.html         # Reuse patalacheckpoints UI
    results/
        questions.json     # Generated questions
        results.json       # Evaluation results
        metrics.json       # Computed metrics
    STORY.md               # Technical write-up
```

## Source code to use

From Wiggly:
- `entities.py`, `annotation.py`, `events.py` — ground truth generation
- `adapters/` — source data ingestion
- `completeness.py` — coverage checks

From patalacheckpoints:
- `frontend/` — ReactFlow graph visualization
- `patala/` — structured data models

New code:
- `export_to_hydra.py` — HydraDB integration (~150 lines)
- `generate_questions.py` — question generator (~100 lines)
- `evaluate.py` — benchmark runner (~120 lines)
- `hydrabench.py` — scoring (~80 lines)

## Execution plan (52 hours)

| Hour | Task |
|------|------|
| 0-4 | Register, read HydraDB MCP docs, set up env |
| 4-10 | Build Wiggly → HydraDB export |
| 10-16 | Export 500+ entities to HydraDB |
| 16-22 | Auto-generate 50 benchmark questions |
| 22-30 | Build evaluator, run fast/thinking comparison |
| 30-36 | Compute metrics, analyze results |
| 36-42 | Build demo UI (adapt patalacheckpoints) |
| 42-48 | Write technical README + STORY |
| 48-50 | Record demo video |
| 50-52 | **SUBMIT** |

## Why this wins

1. **Real contribution to HydraDB** — a benchmark for graph memory correctness
2. **Technically deep** — not a wrapper, a testing framework
3. **Uses HydraDB meaningfully** — fast vs thinking query comparison
4. **Reproducible** — anyone can run the benchmark
5. **Unique angle** — nobody else is testing graph memory correctness

## Key files to read first

- HydraDB MCP repo: `github.com/usecortex/hydradb-mcp`
- `vendor/wiggly/patala/` — all source code
- `vendor/patalacheckpoints/` — demo UI
