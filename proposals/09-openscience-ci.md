# Proposal 9: OpenScience CI

## Tagline
> Property-based testing for scholarly graphs.

## What it does
Generates adversarial test cases for scholarly knowledge graphs, finds inconsistencies, produces regression suites.

## Problem
Scholarly graphs have errors: conflicting metadata, missing links, inconsistent records. No systematic way to find them.

## Solution
Generate hard questions from graph invariants, run them, detect failures.

## Architecture
```
Graph / Repository / CRIS
    │
    ▼
Invariant Suite
    │
    ├── identity checks
    ├── relation checks
    └── provenance checks
    │
    ▼
Adversarial Case Generator
    │
    ▼
Regression Corpus
```

## Example tests
```
same surname + different country → identity conflict
paper has DOI in Crossref but another in repository
dataset relation exists but cited DOI resolves elsewhere
grant relation inferred but publication predates project
```

## CLI
```bash
scholar-ci test openaire
scholar-ci test repository.xml
scholar-ci adversarial
```

## Why it wins
- Maps QDW verification philosophy to research infrastructure
- Useful to OpenAIRE (they just cleaned 300M relations)
- Novel testing framework

## Files
- `src/imbrokeasfuck/earn/factory.py` — evolutionary testing pattern
