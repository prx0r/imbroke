# Proposal 1: Patala Research CI — FINAL

## Tagline
> When the evidence changes, know what to recheck.

## One-sentence
> Patala Research CI tracks the OpenAIRE evidence behind research conclusions and identifies exactly which conclusions require re-verification when that evidence changes.

## Core promise
> OpenAIRE tells you what the research graph knows. Patala remembers what your conclusions depended on—and tells you when they need to be checked again.

---

## Why it wins

1. **Nobody does this end-to-end.** TerminusDB does versioning. OpenAIRE does versioning. Neither tells you "your conclusion just broke."

2. **OpenAIRE actually changes enough for this to matter.** v11.3 removed 318.7M relations and 1.05M funding links.

3. **Deterministic, not LLM.** Core path has no AI. Pure dependency tracking.

4. **Fits Theme B perfectly.** Reusable tool, others can build on it.

5. **Strategic alignment.** OpenAIRE's strategy says research intelligence should be inspectable and governable. This extends that downstream.

---

## Architecture

```
OPENAIRE V3
    │
    ▼
Normalizer (stable identity / relations)
    │
    ▼
Canonical Snapshot (JCS + digest)
    │
    ▼
TrackedAnalysis
    │
    ├── snapshot T₁
    └── snapshot T₂
    │
    ▼
Semantic Diff
    │
    ▼
Dependency Matcher
    │
    ├── unaffected
    └── affected
    │
    ▼
Impact Report
    │
    ▼
Proof Obligation
    │
    ▼
Append-only Evidence Log
```

---

## Data model

### TrackedAnalysis
```json
{
  "analysis_id": "analysis:funding-landscape",
  "title": "EC-funded open-source AI software",
  "source": {"provider": "openaire", "api": "v3"},
  "query": {"entity": "research-products", "search": "agentic AI", "filters": {"type": "software"}},
  "observed_at": "2026-08-19T...",
  "source_version": "11.3.0",
  "result_ids": ["openaire:..."],
  "snapshot_digest": "sha512:...",
  "claims": ["claim:software-growth"]
}
```

### TrackedClaim
```json
{
  "claim_id": "claim:dataset-linkage",
  "text": "Most sampled software outputs have linked datasets.",
  "dependencies": [
    {"kind": "entity", "ref": "openaire:..."},
    {"kind": "relation", "source": "openaire:...", "predicate": "IsRelatedTo", "target": "doi:..."}
  ],
  "status": "CURRENT"
}
```

### SemanticDiff
```json
{
  "added_entities": [],
  "removed_entities": [],
  "changed_fields": [],
  "added_relations": [],
  "removed_relations": []
}
```

### ImpactReport
```json
{
  "unaffected": ["claim:1"],
  "source_changed": ["claim:2"],
  "recompute": ["claim:3"],
  "human_review": []
}
```

### ProofObligation
```json
{
  "claim": "claim:3",
  "reason": "Supporting relation absent in current state",
  "change_ref": "diff:...",
  "recommended_action": "RECOMPUTE",
  "status": "OPEN"
}
```

---

## Materiality taxonomy

Not all changes matter equally:

```
COSMETIC      — formatting, punctuation
IDENTITY      — ORCID added/resolved
METADATA      — title, abstract, dates
RELATION      — dataset/software/project links
AVAILABILITY  — OA status, embargo changes
VERSION       — new version of dataset/software
CORRECTION    — error fixed in record
RETRACTION    — paper retracted
```

Claim policies: "depends on DATASET_RELATION → removal = RECOMPUTE"

---

## Hard invariants

```
R1. Source change ≠ claim invalidation.
R2. Claim affected only through explicit dependency.
R3. Absence recorded, not interpreted as falsehood.
R4. Patala reports input changed, never claims OpenAIRE invalidated.
R5. Every obligation identifies exact change.
R6. Same snapshots + same deps → same ImpactReport.
R7. History is append-only.
R8. Machine dependencies are PROPOSED until human accepts.
```

---

## Demo (4 screens)

**Screen 1:** Track analysis against OpenAIRE V3
**Screen 2:** Register claims with dependencies
**Screen 3:** Verify after graph change (use v11.3 real changes)
**Screen 4:** Show impact report + proof obligations

---

## OpenAIRE V3 API usage

```
# Track
GET /v3/research-products?search=...&pageSize=100&includeStats=true

# Verify (after new release)
GET /v3/research-products?search=...&pageSize=100
→ semantic diff against snapshot

# ScholeXplorer for relation types
GET /v3/scholexplorer?source={doi}&target={doi}
```

**V3 (stable), not V4 (beta).**

---

## What NOT to build

- ❌ AI peer reviewer (crowded)
- ❌ Generic KG versioning (TerminusDB exists)
- ❌ Generic OpenAIRE MCP/RAG (Alien did it)
- ❌ Research dashboards (MONITOR exists)
- ❌ Scholar Relay (future extension, not P0)
- ❌ Crux (stretch feature, not headline)
- ❌ Sanskrit demo (one paragraph origin story, not the demo)

---

## Files
- `hackathons/openaire/ideas4.md` — architecture
- `proposals/01-research-ci.md` — this file
- `vendor/wiggly/patala/events.py` — event store
- `vendor/wiggly/patala/completeness.py` — coverage model
- `vendor/iis/` — OpenAIRE IIS reference
