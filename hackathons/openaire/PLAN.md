# OpenAIRE AI Hackathon — OpenPāṭala Research Graph Auditor

**Deadline:** August 20, 2026, 23:59 CET (~43 hours from now)
**Theme:** B: Build
**Prize:** €500 grand prize + partnership + Alien Gateway credits
**License:** CC-BY

## Pitch

> OpenPāṭala turns fragmented scholarly records into provenance-backed research objects. It reconciles the same work, author, institution, dataset, and claim across OpenAIRE and external scholarly sources, preserves where every assertion came from, surfaces contradictions and missing evidence, and exposes the result to humans and agents through an API/MCP interface.

## What we submit

**NOT** all of Pāṭala. One narrow, beautiful pipeline.

## Architecture

```
OpenAIRE Graph
      │
      ▼
OpenAIREAdapter
      │
      ├────────────── OpenAlex
      ├────────────── Crossref
      └────────────── ORCID
      │
      ▼
canonical identity resolver
      │
      ▼
evidence-backed assertions
      │
      ▼
Research Dossier
      │
      ├── provenance
      ├── conflicts
      ├── missing metadata
      ├── source agreement
      └── reproducible state digest
      │
      ▼
tiny web UI + JSON API
```

## Demo question

> "How much do major scholarly databases agree about authors, institutions, funding, datasets and publication identity for the same research objects?"

Run across 100-500 OpenAIRE records. Show:

```
Records ingested:       250
Cross-source matches:   183
Conflicts detected:      27
Missing identifiers:     61
Source agreement:       88%
Reproducible digest:    ...
```

**Numbers must come from actual runs, not invented.**

## Repo structure

```
patala-openaire/
    README.md
    adapter.py           # OpenAIRE → Wiggly adapter
    run_demo.py          # Run the pipeline
    evaluation.py        # Compute metrics
    demo/
        index.html       # Tiny web UI
    evidence/
        run.json         # Actual run output
        metrics.json     # Computed metrics
    STORY.md             # 1-2 page write-up
```

## Source code to use

From Wiggly (`vendor/wiggly/patala/`):
- `entities.py` — canonical entity resolution
- `annotation.py` — assertions with evidence
- `events.py` — append-only provenance
- `adapters/` — OpenAlex, Crossref, DOI adapters
- `completeness.py` — coverage verification
- `api.py` — FastAPI endpoints

New code needed:
- `adapter.py` — OpenAIRE Graph API adapter (~100 lines)
- `run_demo.py` — orchestration script (~80 lines)
- `evaluation.py` — metrics computation (~60 lines)
- `demo/index.html` — simple web UI (~150 lines)

## Execution plan (43 hours)

| Hour | Task |
|------|------|
| 0-2 | Register, read OpenAIRE MCP docs, set up env |
| 2-6 | Build OpenAIRE adapter, test with 10 records |
| 6-12 | Run on 250+ records, collect real metrics |
| 12-16 | Build cross-source identity resolution |
| 16-20 | Compute provenance, conflicts, agreement |
| 20-24 | Build tiny web UI |
| 24-30 | Write STORY.md (1-2 pages) |
| 30-36 | Polish, test reproducibility |
| 36-40 | Record demo video |
| 40-43 | **SUBMIT** |

## Story outline (1-2 pages)

1. **The question:** How much do scholarly databases agree?
2. **The journey:** Built OpenPāṭala to find out
3. **The insight:** 88% agreement, but 27 conflicts and 61 missing identifiers
4. **What others can reuse:** OpenAIRE adapter, cross-source identity resolver, provenance system
5. **Reproducibility:** Run the same pipeline, get the same numbers

## Key files to read first

- `vendor/wiggly/patala/adapters/` — existing scholarly adapters
- `vendor/wiggly/patala/entities.py` — entity resolution
- `vendor/wiggly/patala/annotation.py` — assertion tracking
- OpenAIRE MCP docs
