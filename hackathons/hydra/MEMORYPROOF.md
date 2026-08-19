# Hack Hydra — MemoryProof

## Submission for Hack Hydra: The HydraDB Open Source Hackathon
**Deadline:** August 20, 2026, 11:59 PM PT (~48 hours)
**Prize:** $5,000 total
**Track:** 03 — Memory + Context Retrieval

---

## TL;DR

> **MemoryProof is a benchmark and debugger for graph memory systems.** It uses Wiggly's verified scholarly corpus as ground truth to test whether HydraDB's recall actually returns attributable, temporally correct, cross-source consistent context.

---

## The Problem

Agent memory systems retrieve plausible context. Nobody systematically tests whether it's actually correct, attributable, or consistent.

HydraDB has `fast` and `thinking` recall modes, knowledge-graph enrichment, and Cypher graph queries. But there's no standard benchmark that measures:

- Does the recalled context match ground truth?
- Is the attribution correct?
- Are temporal facts current?
- Does graph traversal find the right paths?

---

## What We Built

### 1. Wiggly → HydraDB Export

Export Wiggly's verified scholarly corpus into HydraDB as knowledge sources:

```python
from research_ci.source import WigglyExporter
exporter = WigglyExporter()
exporter.export_to_hydradb(
    corpus_path="vendor/wiggly/data/",
    hydradb_url="https://mcp.hydradb.com/mcp"
)
```

### 2. Auto-generated Benchmark Questions

From Wiggly's ground truth, generate questions with known answers:

```python
from research_ci.benchmark import QuestionGenerator
gen = QuestionGenerator(ground_truth)
questions = gen.generate(count=50)
# Returns: factual, multi-hop, contradiction, temporal, negative questions
```

### 3. HydraDB Evaluation

Run questions through HydraDB's `hydradb_query` in both modes:

```python
from research_ci.evaluator import HydraEvaluator
eval = HydraEvaluator(hydradb_url="https://mcp.hydradb.com/mcp")
results = eval.run(questions, modes=["fast", "thinking"])
```

### 4. Failure Taxonomy

```python
from research_ci.failures import classify_failures
failures = classify_failures(questions, results, ground_truth)
# Returns: WRONG_ENTITY, STALE_FACT, MISSING_EDGE, FALSE_EDGE, etc.
```

### 5. Auto-tune Hydra Config

Use evolutionary search to find optimal recall parameters:

```python
from research_ci.optimizer import HydraOptimizer
opt = HydraOptimizer(eval)
best_config = opt.optimize(population_size=20, generations=10)
```

---

## Architecture

```
           WIGGLY GROUND TRUTH
           (verified corpus)
                  │
                  ▼
         HydraDB Knowledge Sources
         (via hydradb_ingest)
                  │
         ┌────────┼────────┐
         ▼        ▼        ▼
      fast    thinking   graph
      query    query     query
         │        │        │
         └────────┼────────┘
                  ▼
           HydraEvaluator
                  │
                  ▼
         BenchmarkResults
                  │
         ┌────────┼────────┐
         ▼        ▼        ▼
      accuracy  latency  attribution
         │        │        │
         └────────┼────────┘
                  ▼
           FailureAnalysis
                  │
                  ▼
         Auto-tune Config
```

---

## HydraDB MCP Integration

We use the official HydraDB MCP server:

```python
import httpx

HYDRADB_MCP = "https://mcp.hydradb.com/mcp"

def hydradb_query(query: str, mode: str = "fast") -> dict:
    """Query HydraDB via MCP."""
    r = httpx.post(HYDRADB_MCP, json={
        "method": "tools/call",
        "params": {"name": "hydradb_query", "arguments": {"query": query, "mode": mode}}
    })
    return r.json()

def hydradb_ingest(text: str, title: str = "") -> dict:
    """Ingest content into HydraDB."""
    r = httpx.post(HYDRADB_MCP, json={
        "method": "tools/call",
        "params": {"name": "hydradb_ingest", "arguments": {"text": text, "title": title}}
    })
    return r.json()
```

---

## Demo

```bash
# 1. Export Wiggly corpus to HydraDB
python -m memoryproof.export --corpus vendor/wiggly/data/

# 2. Generate benchmark questions
python -m memoryproof.benchmark --count 50 --output questions.json

# 3. Run evaluation
python -m memoryproof.evaluate --questions questions.json --modes fast thinking

# 4. Show results
python -m memoryproof.report

# Output:
# Questions: 50
# Fast accuracy: 0.82
# Thinking accuracy: 0.94
# Entity resolution: 0.91
# Attribution accuracy: 0.96
# Temporal accuracy: 0.88
# Latency fast: 340ms
# Latency thinking: 1180ms
```

---

## What Makes This Different

| Other projects | MemoryProof |
|----------------|-------------|
| Build agent memory | **Test** agent memory |
| Use HydraDB | **Benchmark** HydraDB |
| Demo a chatbot | **Prove** recall correctness |
| One-shot evaluation | **Continuous** regression suite |

---

## Reusable Outputs

- Benchmark question format (JSON schema)
- Evaluation metrics (accuracy, attribution, temporal)
- Failure taxonomy (9 categories)
- Hydra config optimization
- CLI for reproducible benchmarks

---

## Links

- HydraDB: https://hydradb.com
- HydraDB MCP: https://github.com/hydra-db/hydradb-mcp
- Wiggly: https://github.com/prx0r/neverbrokeagain-wiggly
- Hackathon: https://www.hackathons.space/hackathons/hack-hydra-the-hydradb-open-source-hackathon
