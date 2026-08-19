# Proposal 10: Contribution Ledger

## Tagline
> Beyond h-index: credit for the work that actually matters.

## What it does
Tracks diverse scholarly contributions (cruxes resolved, readings adjudicated, evidence acquired) as attributable, citable events.

## Problem
Academic assessment counts papers. But AI makes processing cheap, so judgment becomes scarce. Current systems don't see that work.

## Solution
Record structured contribution events that map to OpenAIRE Person entities and MyResearchFolio.

## Architecture
```
Scholarly Contribution Event
    │
    ├── contributor (ORCID, OpenAIRE Person)
    ├── role (ADJUDICATION, TRANSCRIPTION, EVIDENCE_ACQUISITION)
    ├── object (crux, passage, reading)
    ├── evidence (provenance, reasoning)
    ├── decision (accepted/rejected)
    └── credit (named, citable)
    │
    ▼
OpenAIRE Person Profile
    │
    ▼
MyResearchFolio (diverse contributions)
```

## Contribution types
```
DATA_CURATION, VALIDATION, ADJUDICATION, TRANSCRIPTION,
ENTITY_RESOLUTION, REPRODUCTION, COUNTEREXAMPLE,
ONTOLOGY_CURRATION, EVIDENCE_ACQUISITION
```

## Why it wins
- Aligns with OpenAIRE's research assessment reform
- Uses Person entities + MyResearchFolio
- Strategic longer-term value

## Note
Needs MyResearchFolio to mature first. Better as "future work" in hackathon.

## Files
- `vendor/wiggly/patala/` — event models
