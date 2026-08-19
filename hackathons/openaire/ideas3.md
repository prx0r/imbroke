# Ideas3 — Final Read: What to Actually Build

**Date:** 2026-08-19
**Source:** Full audit of Wiggly/Patalacheckpoints codebase + OpenAIRE comparison

---

## What we already built (and forgot about)

From `patalacheckpoints` alone:

- 57 Python files in openpatalanew
- 1399 works, 605 assertions, 2181 append-only events with Merkle state digests
- 13 adapters (GRETIL, PANDiT, Archive.org, Crossref, OpenAlex, ORCID, ROR, WikiData)
- 7 serializers (PROV-O, Web Annotation, DataCite, CIDOC CRM, RO-Crate, C2PA, HuggingFace)
- Translation factory with deepfinder, download proof, pipeline verification, 257-work index
- 17 proven ML kernels (review, scholar_review, staleness, discovery, education, organism)
- Complete epistemic model: SourceAssertion, EvidenceUse, Proposition, Argument, Attack, Crux
- MCP server with 20 tools
- Conformance tests: 5/5 pass, 6 proofs A-F pass, 26 release gates pass

**The GraphGit idea maps directly onto existing code.** The append-only event store with Merkle checkpoints IS proto-GraphGit. Just point it at OpenAIRE releases.

---

## Tier 1: Build tomorrow (hackathon winner)

### 1. GraphGit — THE ONE

**Already built:**
- `events.py` / `events_v2.py` — append-only event store with Merkle checkpoints
- `state_cursor`, `state_digest` — state digests
- "affected claims" concept when something changes
- OpenAIRE's own contract-test repo as reference architecture

**Demo:**
```
graphgit log doi:10.xxx/foo
```
Returns how a paper's metadata evolved across OpenAIRE graph versions.

**Nobody has this.** OpenAIRE's contract tests check "did the API break?" — you generalize to "how did knowledge change?"

### 2. Scholar Relay — second place

**Already built:**
- Crux detection (Crux model + scholar_review.py)
- Evidence packets (EvidenceUse model)
- OpenAIRE Person graph as expertise router
- MyResearchFolio as receiving end

**Demo:**
Agent discovers conflicting readings → proof obligation → OpenAIRE suggests scholars → human adjudicates → contribution recorded.

---

## Tier 2: Strong but needs work

### 3. Broker Agent
Most immediately useful but least distinctive. Broker already does enrichment; adding evidence quality is good but not a winner.

### 4. OpenScience CI
Novel testing philosophy, maps to QDW. But adversarial case generator is ambitious for hackathon.

---

## Tier 3: Cool but not for hackathon

### 5. Manuscript Reality Bridge
Beautiful but needs domain adapters (IIIF, TEI-XML, CollateX) that don't exist yet.

### 6. Contribution Ledger
Strategic killer but needs MyResearchFolio to mature.

---

## What to build: GraphGit + Scholar Relay combined

**"Patala — Git for Scholarly Knowledge"**

1. OpenAIRE Graph version N releases
2. GraphGit detects what changed (new papers, updated affiliations, new dataset links)
3. For each change, Patala checks: "Does this affect any existing claim?"
4. If yes → proof obligation emitted
5. Human reviews if needed
6. Event recorded, state digest updated
7. Reproducible: query OpenAIRE at version X, get results Y, state digest Z

**Tagline:** "OpenAIRE tells you what the graph knows. Patala tells you what changed, what's uncertain, and what still needs a human."

**Not competing with IIS/Broker/AffRo.** This is the missing trust layer on top.
