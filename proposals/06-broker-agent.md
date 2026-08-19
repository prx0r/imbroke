# Proposal 6: Broker Agent (Evidence Layer)

## Tagline
> Does this enrichment actually hold up?

## What it does
Adds evidence quality verification over OpenAIRE Broker enrichment events.

## Problem
Broker tells you "we found an ORCID for this author." It doesn't tell you how confident that match is or whether independent sources agree.

## Solution
When Broker emits an enrichment event, verify it against Crossref/ORCID/OpenAlex before accepting.

## Architecture
```
OpenAIRE Broker Event
    │
    ▼
Evidence Verification
    │
    ├── Crossref check
    ├── ORCID check
    ├── OpenAlex check
    └── Confidence score
    │
    ▼
Propose / Escalate
```

## Key primitive: EnrichmentEvidence
```json
{
  "broker_event": "...",
  "proposed_change": {"author": "...", "orcid": "..."},
  "support": ["OpenAIRE", "ORCID", "Crossref"],
  "contradictions": [],
  "confidence": 0.97,
  "decision": "PROPOSE_ACCEPT"
}
```

## Why it wins
- Immediately useful
- Broker API exists
- Not competing with Broker (adding quality layer)

## Files
- `vendor/wiggly/patala/` — evidence verification
