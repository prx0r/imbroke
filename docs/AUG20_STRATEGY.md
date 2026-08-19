# Aug 20 Hackathon Strategy — Win Tomorrow

**Status:** Both OpenAIRE and Hack Hydra are due TOMORROW (Aug 20, 2026)
**Time available:** ~24 hours
**Key insight:** We don't build from scratch. We repackage Wiggly.

---

## Hack Hydra ($5K) — HIGHER PRIORITY

### What they want
Graph-based infrastructure, ontologies, agent memory, context retrieval, knowledge systems.
$5K prize pool. Build something technically interesting with HydraDB.

### Our pitch: Patala-on-Hydra
**Provenance-aware long-term memory where agents distinguish evidence, assertions and interpretations instead of throwing everything into embeddings.**

### What we already have (70% reuse)

| Component | Source | What it does |
|-----------|--------|-------------|
| `entities.py` | Wiggly | Canonical entity resolution |
| `annotation.py` | Wiggly | Assertions with evidence |
| `events.py` | Wiggly | Append-only provenance |
| `knowledge_graph` | Wiggly | Entity-relation graph |
| `completeness.py` | Wiggly | Coverage verification |
| `audit.py` | Wiggly | State verification |
| `api.py` | Wiggly | FastAPI endpoints |

### What we build (30% new code)

1. **HydraDB adapter** (~2 hours)
   - Map Wiggly's entity graph to HydraDB's graph model
   - Use HydraDB's object storage for provenance records
   - Wire up live connectors (Slack, GitHub, Notion)

2. **Demo UI** (~3 hours)
   - Simple web interface showing provenance graph
   - Show: claim → evidence → sources → confidence
   - Contrast with "just embeddings" approach

3. **Demo narrative** (~1 hour)
   - Sanskrit texts as showcase dataset
   - Show entity resolution across fragmented sources
   - Show how provenance enables verification

### Submission package
- Working HydraDB integration
- GitHub repo with clean README
- 2-page write-up: "Why agents need provenance, not just embeddings"
- Demo video/screenshots

### Why we win
- **Technically deep** — real provenance graph, not a toy
- **Addresses real problem** — agents currently can't distinguish evidence from assertion
- **Uses HydraDB meaningfully** — not just as a backend, but as the graph substrate
- **Unique angle** — nobody else is doing provenance-aware agent memory

---

## OpenAIRE (credits + exposure) — LOWER PRIORITY

### What they want
Build with OpenAIRE scholarly graph. Theme B (Build) or Theme C (Analyze).
Reusable artifacts, reproducible evidence, CC-BY license.

### Our pitch: OpenAIRE Research Graph Auditor
**Reconstruct scholarly lineage while showing exactly where every assertion came from.**

### What we already have (75% reuse)

| Component | Source | What it does |
|-----------|--------|-------------|
| `adapters/` | Wiggly | OpenAlex, Crossref, DOI adapters |
| `entities.py` | Wiggly | Entity resolution |
| `annotation.py` | Wiggly | Assertion tracking |
| `completeness.py` | Wiggly | Coverage analysis |

### What we build (25% new code)

1. **OpenAIRE adapter** (~2 hours)
   - Query OpenAIRE Graph API
   - Map to Wiggly's entity model
   - Handle OpenAIRE-specific fields (funding, relations)

2. **Analysis notebook** (~2 hours)
   - "Trace the provenance of a research claim"
   - Show conflicting sources, coverage gaps
   - Reproducible with CC-BY

### Why we win
- **Directly answers their question** — "what can you do with the OpenAIRE Graph?"
- **Reusable** — others can build on our adapter
- **Reproducible** — notebook runs from scratch

---

## Execution plan (24 hours)

### Hour 0-2: Setup
- Clone HydraDB repo
- Set up dev environment
- Read HydraDB API docs

### Hour 2-6: HydraDB adapter
- Write Wiggly → HydraDB mapping
- Test with Sanskrit entities
- Verify graph queries work

### Hour 6-9: Demo UI
- Build simple web interface
- Show provenance graph visualization
- Add claim → evidence → sources flow

### Hour 9-11: OpenAIRE adapter
- Query OpenAIRE Graph
- Map to Wiggly entities
- Create analysis notebook

### Hour 11-13: Write-up + packaging
- Write 2-page narrative for each
- Clean up code
- Create GitHub repos

### Hour 13-14: Submit
- Submit to both hackathons
- Verify submission received

---

## Key files to use

From Wiggly:
```
vendor/wiggly/patala/entities.py     — entity resolution
vendor/wiggly/patala/annotation.py   — assertions
vendor/wiggly/patala/events.py       — provenance
vendor/wiggly/patala/api.py          — FastAPI
vendor/wiggly/patala/completeness.py — coverage
vendor/wiggly/patala/audit.py        — verification
vendor/wiggly/patala/adapters/       — scholarly adapters
```

From imbrokeasfuck:
```
src/imbrokeasfuck/earn/hackathons.py — target details
src/imbrokeasfuck/earn/wiggly.py     — capability mapping
```

---

## What NOT to do

1. Don't build a new database — use HydraDB as-is
2. Don't build a chatbot — build a provenance system
3. Don't promise more than we can demo — focus on the verified slice
4. Don't copy competitor submissions — our approach is original
5. Don't skip the write-up — it's part of the submission
