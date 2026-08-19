# ProofGraph — Evidence Receipts for Open Science

**Hackathon:** OpenAIRE AI Hackathon — Powered by Alien Intelligence
**Deadline:** August 20, 2026, 23:59 CET (~43 hours)
**Theme:** B: Build
**Prize:** €500 grand prize + pilot partnership + Alien Gateway credits
**License:** CC-BY
**URL:** https://innovation.openaire.eu/component/content/article/openaire-ai-hackathon.html

---

## Pitch

> OpenAIRE has solved a difficult first problem: constructing an open, interconnected scholarly graph from thousands of sources. Its new AI integrations make that graph directly accessible to autonomous agents. A second problem now becomes important: when an agent encounters a relationship in a scholarly graph, can it determine why that relationship exists, how strongly it is supported, whether independent sources agree, and whether the conclusion can be reproduced later? ProofGraph turns OpenAIRE entities and relationships into portable Evidence Receipts that answer those questions.

---

## The Problem

OpenAIRE's own user forum exposes a specific missing layer:

> "The provenance of project → research-output relationships is present in the Graph, but is not currently included in normal Graph API responses."

A user asked how to determine *why* a dataset was linked to a grant. OpenAIRE replied that provenance is available in the full Graph dump/Explore rather than the API, and said they could extend the API if there were community demand.

**That is almost a product brief handed to you by OpenAIRE.**

---

## What ProofGraph Does

Turn any OpenAIRE paper, dataset, software artifact, researcher or project into a machine-readable evidence receipt: what is claimed, where each relationship came from, which independent sources corroborate it, what conflicts, what is missing, and what an AI agent may safely assert.

---

## Architecture

```
OpenAIRE Graph V3
      │
      ▼
ProofGraph / Patala
      │
      ├── Crossref
      ├── DataCite
      └── OpenAlex
      │
      ▼
canonical PID normalization
      │
      ▼
EvidenceReceipt
      │
      ├── 12 deterministic checks
      ├── conflicts
      ├── gaps
      └── provenance
      │
      ▼
RO-Crate export + tiny graph UI
```

---

## EvidenceReceipt Schema

```json
{
  "subject": {
    "id": "doi:...",
    "type": "research_product"
  },
  "claim": {
    "predicate": "isProducedBy",
    "object": "project:..."
  },
  "observations": [
    {
      "source": "OpenAIRE",
      "method": "inferred",
      "trust": 0.90
    },
    {
      "source": "DataCite",
      "method": "metadata",
      "trust": null
    }
  ],
  "agreement": {
    "supporting_sources": 2,
    "contradicting_sources": 0,
    "independence": 0.72
  },
  "validation": {
    "native_validated": false,
    "proofgraph_status": "CORROBORATED"
  },
  "gaps": [
    "no linked software artifact"
  ],
  "provenance": {
    "retrieved_at": "...",
    "openaire_graph_version": "11.3.0",
    "input_digests": {},
    "receipt_digest": "sha256:..."
  }
}
```

---

## Deterministic Checks (12)

```
IDENTITY
✓ persistent product identifier
✓ author PID
? organization PID

PROVENANCE
✓ source recorded
✓ relationship method known
✗ no native validation

RESEARCH OBJECT
✓ publication
✓ dataset
✗ software
? protocol

REUSE
✓ CC licence
? software licence
✓ repository resolvable

CORROBORATION
✓ sources independent
✓ no conflicts

HISTORY
✓ graph version recorded
✓ query reproducible
✓ receipt content-addressed
```

**Score = named pass/fail reasons, not LLM vibes.**

---

## Case Study

**"Can AI research reproduce itself?"**

Take a bounded sample of recent European AI-agent/LLM/reproducibility research from OpenAIRE. For each publication ask:

- Does a dataset exist?
- Does software exist?
- Does software have a PID?
- Is it openly accessible?
- Is the funding relationship attributable?
- Are authors ORCID-linked?
- Do OpenAIRE / Crossref / DataCite / OpenAlex agree?
- Can the complete research object be reconstructed?

Produce real metrics:

```
n = actual number

publication → data linkage       x%
publication → software linkage   y%
PID complete                     z%
multi-source corroborated        ...
conflicting metadata             ...
```

---

## Killer Features

### 1. Gap Suggestions

Turn missing links into actionable repairs:

```
MISSING RELATION CANDIDATE

Publication: 10.xxxx/foo
Candidate dataset: 10.xxxx/bar

Evidence:
  DataCite RelatedIdentifier       +0.45
  Crossref supplementary relation  +0.25
  title/author overlap              +0.12

Confidence: 0.82
Suggested: publication IsSupplementedBy dataset
STATUS: PROPOSED — NOT OPENAIRE VERIFIED
```

### 2. Version Pinning

OpenAIRE versions its Graph semantically (MAJOR/MINOR/PATCH). Put Graph version into every receipt. Then:

```
proofgraph diff receipt-old.json receipt-new.json
```

shows exactly what changed between Graph versions.

### 3. RO-Crate Export

Wiggly already has an RO-Crate serializer. Make a ProofGraph audit downloadable as an actual research object.

---

## Positioning

> OpenCitations reconciles bibliographic identity; F-UJI assesses FAIRness; RO-Crate packages research objects; OpenAIRE builds the scholarly graph. ProofGraph compiles the evidence behind graph claims into agent-consumable, reproducible receipts.

---

## Technical Details

- **API:** OpenAIRE Graph V3 (stable, not V4 beta)
- **Adapters:** OpenAIRE, Crossref, DataCite, OpenAlex
- **Core:** Wiggly/Patala evidence-state machine
- **Export:** RO-Crate, SKG-IF, JSON
- **UI:** Patalacheckpoints graph visualization

---

## Story Structure (1-2 pages)

### The question
How can researchers and AI agents distinguish a graph relationship from the evidence supporting that relationship?

### The journey
Patala → OpenAIRE V3 adapter → cross-source observations → receipt compiler → real case study.

### The insight
In our sample of N records, X% of apparent research objects had no observable software relationship; Y relationships were supported by multiple sources; Z conflicts occurred...

### What others can reuse
Python package, OpenAIRE V3 adapter, EvidenceReceipt JSON schema, CLI, REST API, RO-Crate exporter, SKG-IF exporter, evaluation dataset, reproduction command.

---

## Why This Wins

- **Missing primitive** — not another app, a missing layer in the ecosystem
- **OpenAIRE could adopt this** — pilot partnership is the grand prize
- **Reusable** — generic `proofgraph audit --query "X" --limit 500`
- **Reproducible** — run same pipeline, get same numbers
- **Not a chatbot** — an evidence auditor
- **Fits their 2026 strategy** — trust + intelligence + responsible AI

---

## Execution (43 hours)

| Hour | Task |
|------|------|
| 0-2 | Register, read OpenAIRE MCP/V3 docs |
| 2-6 | Build OpenAIRE V3 adapter |
| 6-12 | Run on 250+ records, collect real metrics |
| 12-16 | Cross-source identity + provenance |
| 16-20 | Build EvidenceReceipt compiler |
| 20-24 | Build tiny web UI |
| 24-30 | Write story (1-2 pages) |
| 30-36 | Polish, test reproducibility |
| 36-40 | Record demo |
| 40-43 | **SUBMIT** |
