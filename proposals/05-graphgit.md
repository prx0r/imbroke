# Proposal 5: GraphGit (Semantic Diffs)

## Tagline
> How did scientific knowledge change?

## What it does
Semantic diffs between OpenAIRE Graph versions, showing exactly what changed and why it matters.

## Problem
OpenAIRE versions its graph but doesn't tell you how changes affect your specific analyses.

## Solution
Track queries, snapshot results, diff between versions, map changes to claims.

## Architecture
```
Old Graph Version → Snapshot → Content Digest
New Graph Version → Rerun → Semantic Diff
    │
    ├── entity added/removed
    ├── field changed
    └── relation changed
    │
    ▼
Impact on tracked claims
```

## Key primitive: GraphDiff
```json
{
  "from_version": "11.2.0",
  "to_version": "11.3.0",
  "records_tracked": 81,
  "unchanged": 67,
  "added": 9,
  "removed": 2,
  "metadata_changed": 3,
  "relations_changed": 7,
  "claims_affected": 3
}
```

## Demo
Use v11.3 release (318M relations removed) as real example.

## Why it wins
- Nobody does semantic diffs for scholarly graphs
- Uses OpenAIRE's own versioning
- Builds on Wiggly's append-only events

## Note
This is now a **component of Research CI**, not standalone.

## Files
- `hackathons/openaire/ideas1.md`
- `vendor/wiggly/patala/events.py`
