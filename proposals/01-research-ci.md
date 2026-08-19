# Proposal 1: Patala Research CI

## Tagline
> CI/CD assumes software changes. Research infrastructure should assume knowledge changes too.

## What it does
Continuous verification for research built on evolving scholarly graphs.

## Problem
Researchers query OpenAIRE, build analyses, publish conclusions. Six months later the Graph has changed. Their conclusions may no longer hold. Nobody tells them.

## Solution
Register analyses against OpenAIRE. When the Graph changes, detect which tracked conclusions are affected and emit proof obligations for re-verification.

## Architecture
```
OpenAIRE Graph API V3
    │
    ▼
TrackedQuery (analysis_id, filters, observed_at)
    │
    ▼
Patala Snapshot (canonical result + content digest + claims)
    │
    ▼
New Graph Release
    │
    ▼
Rerun query → Semantic Diff
    │
    ▼
Impact Graph (what depended on this?)
    │
    ▼
Proof Obligation (what needs re-verification?)
```

## Key primitive: TrackedAnalysis
```json
{
  "analysis_id": "...",
  "query": {"entity": "research-products", "filters": {...}},
  "results": ["doi:..."],
  "graph_state": {"version": "11.3.0"},
  "input_digest": "sha512:...",
  "claims": ["claim:17"]
}
```

## Demo
1. Track "Open software in AI research" against OpenAIRE V3
2. Snapshot results + digest
3. Simulate graph change (v11.3 removed 318M relations)
4. Show semantic diff
5. Show which claims are affected
6. Emit proof obligations

## Why it wins
- Nobody does end-to-end analysis → claim dependency → change → impact → obligation
- Uses OpenAIRE's own versioning (not competing)
- TerminusDB/RDF Delta do versioning; nobody does epistemic impact
- Reproducible: query at version X, get results Y, digest Z

## Tech stack
- OpenAIRE Graph API V3 (stable)
- Wiggly append-only events + Merkle checkpoints
- Content-addressed digests (JCS + SHA-512)
- Python + FastAPI

## Files
- `hackathons/openaire/ideas4.md` — architecture
- `hackathons/openaire/PROOFGRAPH.md` — original (now subset)
- `vendor/wiggly/patala/events.py` — event store
- `vendor/wiggly/patala/completeness.py` — coverage model
