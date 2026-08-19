# Proposal 8: Manuscript Reality Bridge

## Tagline
> AI can read a million papers. It cannot visit an archive.

## What it does
Connects OpenAIRE's scholarly graph to physical manuscript evidence through Patala's sub-document ontology.

## Problem
OpenAIRE stops at the paper level. Manuscript scholarship depends on physical witnesses, editions, passages, readings.

## Solution
Extend OpenAIRE's research graph downward to primary evidence.

## Architecture
```
OpenAIRE (publications, people, projects)
    │
    ▼
Patala Resolver
    │
    ▼
Work → Witness → Edition → EText → Translation → Passage
    │
    ▼
Physical manuscript evidence
```

## Key differentiator
OpenAIRE thinks: ResearchProduct, Publication, Dataset, Software, Person
Patala thinks: Work, Witness, Edition, EText, Translation, LogicalPassage, TextOccurrence

## Demo
1. Find Sanskrit publication in OpenAIRE
2. Trace down to manuscript witnesses
3. Show competing readings
4. Emit proof obligation for human adjudication

## Why it wins
- Most distinctive domain demo
- Makes Sanskrit angle tangible
- Connects two different ontologies

## Note
Needs domain adapters (IIIF, TEI-XML, CollateX) — harder for hackathon.

## Files
- `vendor/wiggly/patala/` — entity models
- `vendor/wiggly/patala/adapters/` — scholarly adapters
