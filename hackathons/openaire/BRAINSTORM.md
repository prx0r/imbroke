# OpenAIRE Hackathon — Brainstorm: What They Actually Want

## What they already have

- **OpenAIRE MCP** — AI agents can query the Graph directly via Alien Intelligence
- **350M entities, 7B relationships** — massive scholarly knowledge graph
- **Provenance tracked at record/property level** — they already know where data comes from
- **Alien AI Gateway** — AI integration layer
- **ARGOS** — machine-actionable Data Management Plans
- **OpenOrgs** — entity disambiguation with human-in-loop
- **Scholexplorer** — publication↔dataset↔software links

## What they DON'T need

- ❌ Another chatbot over OpenAIRE
- ❌ Another scholarly graph viewer
- ❌ "Provenance for OpenAIRE" (they already have it)
- ❌ Generic RAG/search

## What their strategy says

Their 2026-2028 strategy is: **trust + intelligence + responsible AI**

> "AI used in research should stand on open, FAIR and traceable foundations"

> "Intelligence as public infrastructure"

> "Co-create new indicators, tools, services"

## What their case studies show they value

1. **AI-Ready Scientific Corpora** — FAIR, provenance-rich, responsible AI training
2. **Innovation Foresight Dashboard** — evidence-based analytics from open research

## What their community is asking for

From their forum:
- **Relation provenance** — "Why is this dataset linked to this grant?" (not in API responses)
- **Cross-source agreement** — "Do OpenAIRE/Crossref/DataCite agree?"
- **Missing links** — "This publication mentions a dataset but there's no relation"

## What the hackathon actually asks

| Theme | What they want |
|-------|---------------|
| **B: Build** | "Something that makes the Graph more useful. Others can reuse or build on." |
| **C: Analyse** | "Produce evidence. Answer a real question. Decision-maker could act on it." |

## The gap we fill

```
OpenAIRE provides:     the graph (350M entities)
Alien provides:        AI access to the graph
ProofGraph provides:   the evidence layer between them
```

When an agent asks "Is this claim safe to cite?", ProofGraph returns a deterministic evidence object — not another prose response.

## Ideas ranked by fit

### 1. EvidenceReceipts for Open Science ✅ BEST FIT

**What:** Turn any OpenAIRE entity into a machine-readable evidence receipt.

**Why they care:** Their MCP gives agents access to the graph, but agents can't determine WHY relationships exist or HOW strongly they're supported.

**Evidence:** Their own forum shows users confused about relation provenance.

**Reuse:** Others can build on the receipt format, adapter, CLI.

### 2. Open Science Reproducibility Auditor ✅ STRONG

**What:** Measure how reproducible a research field is using OpenAIRE data.

**Why they care:** Their strategy explicitly mentions "trust" and "responsible AI."

**Case study:** "Can AI research reproduce itself?" — bounded sample of European AI research.

**Metrics:** % with PIDs, % linked to software/datasets, cross-source agreement.

### 3. Graph Quality Monitor ✅ GOOD

**What:** Detect inconsistencies, missing links, conflicting metadata across OpenAIRE sources.

**Why they care:** They just cleaned 300M redundant relationships. Quality matters.

**Demo:** Show real conflicts found in the current graph.

### 4. Research Object Completeness Scorer ✅ GOOD

**What:** Given a DOI, score how complete the research object is (publications, datasets, software, funding, PIDs).

**Why they care:** FAIRness assessment is core to their mission.

**Demo:** Visual scorecard for any paper.

### 5. Provenance Visualizer ✅ GOOD (but simpler)

**What:** Visualize WHY a relationship exists in the graph.

**Why they care:** Their community explicitly asks for this.

**Demo:** Click a relation → see source, method, trust, corroboration.

## What would be MEDIOCRE

- Generic "ask questions about papers" — Alien already does this
- Sanskrit-specific tool — too narrow
- Another scholarly KG viewer — they already have EXPLORE/MONITOR
- LLM summarization — Theme A already permits this

## The winning formula

```
THEY solved:     constructing the graph
THEY solved:     AI access to the graph
THEY NEED:       evidence/verification between them
WE provide:      ProofGraph = evidence receipts
```

## Story structure (matches their template exactly)

### The question
"How can researchers and AI agents distinguish a graph relationship from the evidence supporting that relationship?"

### The journey
OpenPatala → OpenAIRE V3 adapter → cross-source observations → receipt compiler → real case study.

### The insight
Empirical findings from running on N records.

### What others can reuse
Adapter, receipt schema, CLI, API, RO-Crate exporter, evaluation dataset.

## Key technical decisions

- **Use V3 API** (stable, not V4 beta)
- **CC-BY license** (required)
- **Reproducible** (run same pipeline, get same numbers)
- **Artifact + 1-2 page story** (their submission model)

## What makes this "OpenAIRE could adopt this"

- Fits their "co-create new tools/services" model
- Addresses real community pain points (relation provenance)
- Complements their MCP (doesn't compete)
- Uses their versioning system (Graph versions)
- Could become a permanent service after the hackathon
