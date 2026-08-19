# Ideas4 — Final Architecture: Research CI

**Date:** 2026-08-19
**Status:** WINNING APPROACH

---

## Core realization

**Don't compete with OpenAIRE's infrastructure.** Their stack is absurdly mature:
- Graph API for entities/search
- ScholeXplorer for typed scholarly relationships
- Broker for incremental enrichment
- Monthly live graph updates
- Six-month DOI-pinned snapshots for reproducible analysis
- Semantic Graph releases with detailed changes

**Patala becomes more interesting when it treats OpenAIRE as a sensor feeding observations into a smaller epistemic state machine.**

This matches Wiggly's design principle: **tools don't become truth; their outputs become observations.**

---

## The product

# **Patala Research CI**

> **OpenAIRE tells researchers what the scholarly graph knows. Patala tells them when that knowledge changes, what downstream conclusions are affected, and what needs to be verified again.**

Not "Git for the graph." That describes the mechanism.

**Research CI describes why anyone cares.**

---

## Architecture

```
OPENAIRE
    │
Graph API / ScholeXplorer
    │
    ▼
TRACKED QUERY
    │
canonical result
    │
content digest
    │
    ▼
PATALA SNAPSHOT
    │
    ▼
new Graph release
    │
    ▼
rerun query
    │
    ▼
SEMANTIC DIFF
    │
entity/field/relation changed
    │
    ▼
IMPACT GRAPH
    │
"what depended on this?"
    │
unaffected / affected
    │
    ▼
PROOF OBLIGATION
```

---

## Killer primitive: TrackedAnalysis

```json
{
  "analysis_id": "analysis:agent-memory-landscape",
  "source": {"provider": "openaire", "api": "v3"},
  "query": {"entity": "research-products", "filters": {"keywords": "agent memory"}},
  "observed_at": "...",
  "results": ["doi:..."],
  "graph_state": {"version": "..."},
  "input_digest": "sha512:...",
  "claims": ["claim:17"]
}
```

Then: `patala verify analysis:agent-memory-landscape`

Returns:
```
SOURCE CHANGED
  Tracked: 81  Unchanged: 67  Added: 9  Removed: 2  Changed: 3
DOWNSTREAM
  Claims unaffected: 14  Need recompute: 3  Invalidated: 1
PROOF OBLIGATIONS
  PO-17 funding relation removed
  PO-18 dataset relation changed
```

---

## Why this wins

1. **OpenAIRE's own versioning is the input** — not competing
2. **Nobody has this** — OpenAIRE checks "did API break?", you check "how did knowledge change"
3. **Uses v11.3 changes as demo** — 318.7M relations removed, 1.05M funding relations cleaned
4. **Reproducible** — query at version X, get results Y, digest Z
5. **Broker becomes event source** — "something changed" → "does it matter?"

---

## Build hierarchy

**P0 (must work):**
- OpenAIRE V3 adapter
- TrackedQuery + snapshot
- Semantic diff
- Event ledger
- CLI/API

**P1 (impressive):**
- Claim dependency
- Impact analysis
- Staleness
- Proof obligations

**P2 (polish):**
- Timeline UI
- Before/after visualization
- State digest

**P3 (if time):**
- Scholar Relay
- Sanskrit manuscript crux

---

## Don't build

- Payment systems
- Scholar profiles
- Marketplace
- New scholarly graph
- Generic RAG/MCP
- Another dashboard

---

## Tagline

> **OpenAIRE tells you what the graph knows. Patala tells you what changed, what's uncertain, and what still needs a human.**

> **CI/CD assumes software changes. Research infrastructure should assume knowledge changes too.**
