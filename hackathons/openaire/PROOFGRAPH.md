# OpenAIRE — ProofGraph

**Deadline:** August 20, 2026, 23:59 CET (~43 hours)
**Theme:** B: Build
**Prize:** €500 + pilot partnership + Alien Gateway credits
**License:** CC-BY

## Product: ProofGraph

> **A reproducible evidence compiler for open science.**

Converts OpenAIRE's scholarly knowledge graph into reproducible evidence dossiers for humans and AI agents.

## What to build

NOT "Sanskrit knowledge graph." NOT "chat with papers."

An **auditing/enrichment layer over OpenAIRE** that answers:

- Which assertions should I trust?
- Which sources independently agree?
- Where do metadata providers disagree?
- Is this research object actually reproducible?
- Where is the dataset? Where is the software?
- Does the claimed grant relationship have corroborating evidence?
- Which missing links are likely data-quality defects?

## Architecture

```
OpenAIRE Graph V3
      │
      ▼
ProofGraph / Patala
      │
      ├── Crossref
      ├── OpenAlex
      └── ORCID
      │
      ▼
identity reconciliation
      │
      ▼
claim/evidence graph
      │
      ├── conflicts
      ├── missing links
      └── provenance
      │
      ▼
Reproducibility Dossier
```

## Output format

```json
{
  "research_product": "...",
  "canonical_identity": "...",
  "evidence": {
    "sources": 4,
    "independent_sources": 3,
    "persistent_identifiers": ["doi:...", "orcid:..."]
  },
  "open_science": {
    "publication_open": true,
    "dataset_linked": false,
    "software_linked": true,
    "software_open_source": true
  },
  "conflicts": [{"field": "affiliation", "values": ["...", "..."], "sources": ["...", "..."]}],
  "reproducibility": {"score": 0.72, "missing": ["linked_dataset"]},
  "state_digest": "sha256:..."
}
```

## Demo case study

"How reproducible is AI research on cultural heritage and manuscript digitisation?"

Query OpenAIRE, measure across hundreds of works:
- % with persistent identifiers
- % linked to software/datasets
- % with funding relationships
- Cross-source identity agreement
- Source conflicts

## Killer feature: gap suggestions

Turn gaps into actionable fixes:
```
Publication X mentions Dataset Y
  → no OpenAIRE publication→dataset relation
  → Crossref/DataCite corroboration found
  → POSSIBLE MISSING LINK
  → evidence bundle
```

## Why this wins

- **Useful public infrastructure** — OpenAIRE could adopt this
- **Reusable** — generic `proofgraph audit --query "X" --limit 500`
- **Reproducible** — run same pipeline, get same numbers
- **Not a chatbot** — an evidence auditor

## Files

```
hackathons/openaire/PROOFGRAPH.md
hackathons/openaire/PLAN.md
```
