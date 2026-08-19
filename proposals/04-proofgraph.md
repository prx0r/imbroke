# Proposal 4: ProofGraph (Evidence Receipts)

## Tagline
> Evidence you can inspect, not just answers you can trust.

## What it does
Turns OpenAIRE entities into machine-readable evidence receipts: what is claimed, where each relationship came from, which sources corroborate, what conflicts, what's missing.

## Problem
OpenAIRE gives you the graph. It doesn't give you a portable evidence object for each claim.

## Solution
Cross-source reconciliation + deterministic checks + EvidenceReceipt export.

## Architecture
```
OpenAIRE V3 + Crossref + DataCite + OpenAlex
    │
    ▼
Canonical PID normalization
    │
    ▼
EvidenceReceipt (12 deterministic checks)
    │
    ├── conflicts
    ├── gaps
    ├── reproducibility score
    └── provenance chain
```

## Key primitive: EvidenceReceipt
```json
{
  "subject": {"id": "doi:...", "type": "research_product"},
  "claim": {"predicate": "isProducedBy", "object": "project:..."},
  "observations": [{"source": "OpenAIRE", "method": "inferred", "trust": 0.90}],
  "agreement": {"supporting": 2, "contradicting": 0},
  "validation": {"proofgraph_status": "CORROBORATED"},
  "state_digest": "sha256:..."
}
```

## Demo
Run on 250 records, show agreement/conflicts/missing data.

## Why it wins
- Addresses community pain (relation provenance not in API)
- Deterministic, not LLM vibes
- Could become an OpenAIRE service

## Note
This is now a **component of Research CI**, not a standalone product.

## Files
- `hackathons/openaire/PROOFGRAPH.md`
