# OpenAIRE — Highest Signal Ideas

**Source:** Full site scrape (about, hackathon, resources, FAQs, innovation tracks, case studies)
**Date:** 2026-08-19
**Purpose:** What to build and why

---

## Key facts from the site

- **Graph size:** 350M entities, 7B relationships
- **Hackathon deadline:** Aug 20, 23:59 CEST (corrected from CET — it's summer time)
- **Evaluation criteria:** Novelty + innovation, Use of OpenAIRE Graph + AI, Impact
- **Prize:** €500 + pilot partnership + Alien Gateway credits
- **License:** CC-BY
- **Submission:** artifact + 1-2 page story
- **Community voting:** Aug 21-29
- **Awards:** Sep 16 at OpenAIRE Graph Community Call

---

## #1 EvidenceReceipts (ProofGraph) — HIGHEST SIGNAL

**Why this wins:**

1. **Addresses their own community pain point.** Their forum shows users confused about relation provenance — "Why is this dataset linked to this grant?" OpenAIRE admitted provenance isn't in normal API responses.

2. **Complements their MCP.** Alien built the AI access layer. We build the evidence layer underneath. No competition.

3. **Fits their strategy.** Trust + intelligence + responsible AI. Evidence receipts = trust.

4. **Could become a service.** Grand prize = pilot partnership. This is something they could adopt.

5. **Reusable.** Others can build on the receipt format, adapter, CLI.

6. **Deterministic.** Not LLM vibes — named pass/fail checks.

7. **F-UJI pattern.** Decompose score into explicit tests. Judges understand this.

**What to build:**
```
OpenAIRE V3 → cross-source reconciliation → EvidenceReceipt → 12 checks → conflicts/gaps → RO-Crate export
```

**Demo:** "Can AI research reproduce itself?" — bounded sample of European AI research.

---

## #2 Reproducibility Auditor — STRONG SIGNAL

**Why this works:**

1. **Their strategy explicitly mentions "trust" and "responsible AI."**
2. **Funders care about this.** "Is the research we funded actually reproducible?"
3. **Real question, real metrics.** % with PIDs, % linked to software/datasets, cross-source agreement.
4. **Decision-maker actionable.** A policy maker can act on "40% of AI papers lack linked datasets."

**What to build:**
```
OpenAIRE V3 → extract metadata completeness → cross-source verification → reproducibility score → case study
```

**Demo:** Measure reproducibility of a bounded field (AI, climate, biology).

---

## #3 Graph Quality Monitor — GOOD SIGNAL

**Why this works:**

1. **They just cleaned 300M redundant relationships.** Quality matters to them.
2. **Detects real issues.** Conflicting metadata, missing links, inconsistent records.
3. **Useful to OpenAIRE internally.** Could become an ongoing service.
4. **Deterministic.** No guessing — just systematic checks.

**What to build:**
```
OpenAIRE V3 → systematic quality checks → conflict detection → gap identification → report
```

**Demo:** Show real quality issues found in the current graph.

---

## #4 Research Object Completeness Scorer — GOOD SIGNAL

**Why this works:**

1. **FAIRness assessment is core to their mission.**
2. **Visual and intuitive.** A scorecard for any paper.
3. **Reusable.** Others can run it on any DOI.
4. **Fits Theme B (Build) perfectly.**

**What to build:**
```
OpenAIRE V3 → extract research object → check completeness (PIDs, datasets, software, funding) → score → visualize
```

**Demo:** Score 100 papers, show distribution.

---

## #5 Provenance Visualizer — SIMPLER BUT USEFUL

**Why this works:**

1. **Directly answers community questions.** "Why is this linked?"
2. **Visual.** Judges understand it in 5 seconds.
3. **Complements their MCP.** Shows what the MCP returns in a human-readable way.

**What to build:**
```
OpenAIRE V3 → extract relations → show source/method/trust/corroboration → graph UI
```

**Demo:** Click a relation → see evidence path.

---

## What NOT to build

| Idea | Why not |
|------|---------|
| "AI research assistant" | Alien already does this |
| "Sanskrit knowledge graph" | Too narrow, won't be adopted |
| "Another scholarly KG viewer" | They have EXPLORE/MONITOR |
| "Generic RAG/search" | They have the MCP |
| "LLM summarization" | Theme A already permits this |

---

## The winning formula

```
THEY solved:     constructing the graph (350M entities)
THEY solved:     AI access to the graph (MCP + Alien)
THEY NEED:       evidence/verification between them
WE provide:      ProofGraph = evidence receipts
```

---

## Innovation Tracks alignment

Their five tracks tell us what collaborations they want:

| Track | What they want | Our fit |
|-------|---------------|---------|
| **Data Partnerships** | FAIR, lawful reuse | ✅ OpenAIRE V3 adapter |
| **Innovation Labs** | Co-develop analytics/indicators | ✅ EvidenceReceipt as new indicator |
| **Compliance & Policy** | EU law frameworks | ✅ Deterministic, auditable |
| **Training & Capacity** | Bootcamps, courses | ✅ CLI + docs = reusable |
| **Community & Ecosystem** | Roundtables, sprints | ✅ Open source, CC-BY |

---

## Their partners tell us what's credible

- **Alien Intelligence** — AI analytics (already integrated)
- **CITE** — CIT services (infrastructure)
- **OPIX** — policy/business consulting with AI (innovation)
- **4Science** — open-source research solutions (tools)

We should position as: **"open-source evidence infrastructure"** — similar to 4Science but focused on epistemic verification.

---

## Technical resources from their site

| Resource | URL | Relevance |
|----------|-----|-----------|
| OpenAIRE Graph docs | graph.openaire.eu/docs | API reference |
| Innovation Indicators | monitor.openaire.eu/support/indicator-themes.html | Existing metrics |
| OpenAIRE Guidelines | guidelines.openaire.eu | Metadata standards |
| AI Service Setup Guide | PDF (downloaded) | MCP configuration |
| Submission template | Google Doc | Required format |

---

## Files

```
hackathons/openaire/
  NORTHSTAR.md      — guiding principles (always compare against)
  PROOFGRAPH.md     — refined proposal
  BRAINSTORM.md     — what they want
  PLAN.md           — execution plan
  HIGH-SIGNAL.md    — this file
  resources/
    setup-guide.pdf — OpenAIRE AI Service setup guide
```
