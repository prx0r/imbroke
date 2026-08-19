# Ideas2 — Revised Analysis After Deep OpenAIRE Comparison

**Date:** 2026-08-19
**Source:** Full comparison of Wiggly implementation vs OpenAIRE capabilities

---

## Key revision

Previous thesis was wrong about several things:

1. **"OpenAIRE doesn't have Sanskrit"** — FALSE. Mangalam Corpus, helayo software, Intellexus (€9.9M ERC) all indexed.
2. **"OpenAIRE lacks provenance"** — FALSE. They have relation-level provenance, trust scores, validation flags, semantic versioning, changelog.
3. **"ProofGraph adds provenance to OpenAIRE"** — NOT UNIQUE ENOUGH. They already have most of it.

## What Wiggly actually has that's different

### 1. Sub-document scholarly ontology

OpenAIRE thinks in: ResearchProduct, Publication, Dataset, Software, Person, Organisation, Project.

Wiggly implements: Work, Witness, Edition, EText, Translation, LogicalPassage, TextOccurrence, TextSpan.

**This is the real differentiator.** OpenAIRE stops at the paper level. Wiggly goes down to manuscript witnesses, editions, passages, readings.

### 2. Epistemic state machine

Wiggly's resolver: R0 (external ID) → R1 (crosswalk) → R2 (bibliographic) → R3 (fuzzy) → R4 (corroboration) → R5 (adjudication).

OpenAIRE has deduplication but not this explicit epistemic progression.

### 3. Three distinct evidence types

- RAW BYTE DIGEST (archive bytes)
- JCS RECORD DIGEST (structured observation)
- SEMANTIC FINGERPRINT (text equivalence)

OpenAIRE tracks source/provenance but not at this object level.

### 4. Coverage / Frontier model

Each dimension: state + confidence + evidence_count + last_checked + next_action.

This is more interesting than a completeness score. It's a **research frontier**.

## Revised ranking for OpenAIRE hackathon

| Rank | Idea | Score | Why |
|------|------|-------|-----|
| **1** | **Patala Frontier** | 9/10 | Extends OpenAIRE down to primary evidence. Most original. |
| **2** | **Proof-obligation engine** | 8.5/10 | CoverageDimension → next_action is unexpectedly strong. |
| **3** | **Scholar Relay** | 7/10 | Interesting but too speculative for tomorrow. |
| **4** | Generic ProofGraph | 5/10 | OpenAIRE already has more provenance than we thought. |
| **5** | Generic RAG/MCP | 2/10 | Already solved. |

## The claim that survives

> **OpenAIRE maps the products and people of scholarship. Patala maps the primary evidence, uncertainty and adjudication underneath scholarship. Connecting them creates an end-to-end open research graph from physical manuscript witness to modern research output.**

## Demo panels

1. "What scholarship knows" — OpenAIRE (papers, people, projects)
2. "What scholarship rests on" — Patala (works, witnesses, editions, passages)
3. "What remains unresolved" — Coverage Frontier
4. "Click the uncertainty" — Proof obligations
5. "Scholar adjudicates" — Decision recorded
6. "Event history" — Append-only ledger

## Sanskrit framing

> "Scientific graphs begin where research outputs are published. In manuscript-based humanities, evidence begins much earlier. OpenPatala extends the research graph downward."

Sanskrit = stress test, not excuse.

## Funding reality

- OpenAIRE = technical ecosystem / collaborator, not primary funder
- DARIAH = natural CONNECT community
- ERC/Horizon = actual funding source (Intellexus: €9.9M)
- Zenodo deposit → OpenAIRE indexes → interoperable infrastructure
