# Proposal 2: Patala Crux

## Tagline
> Find the load-bearing premise in any argument.

## What it does
Identifies the minimal premise-set whose removal changes a conclusion.

## Problem
Arguments have hidden dependencies. Removing one premise can collapse a conclusion. No tool systematically identifies which premises are load-bearing.

## Solution
Given a structured argument, perturb each premise and measure impact on conclusions.

## Architecture
```
Input: Structured Argument
    P1 ─┐
    P2 ─┼→ I1 → C
    P3 ─┘

Perturbation Engine
    │
    ├── Remove P1 → C survives
    ├── Remove P2 → C collapses ← CRUX
    └── Remove P3 → C survives

Output:
    CRUX: P2
    Resolution: "Is P2 independently supported?"
    Affected: C, C4, Analysis A
```

## Key primitive: CruxResult
```json
{
  "argument_id": "...",
  "cruxes": [
    {
      "premise": "P2",
      "removal_impact": "COLLAPSES",
      "affected_conclusions": ["C", "C4"],
      "resolution_question": "Is P2 independently supported?",
      "affected_analyses": ["analysis:17"]
    }
  ],
  "stable_premises": ["P1", "P3"]
}
```

## Demo
1. Load a real scholarly argument (Sanskrit textual analysis)
2. Run crux engine
3. Show which premise is load-bearing
4. Simulate rejection
5. Show downstream impact

## Why it wins
- Existing reviewers ask "is this good?" — Crux asks "what breaks if this is wrong?"
- Maps to Patala's existing perturbation/impact machinery
- Useful as a component inside OpenReview, CMU Paper Reviewer, agents

## Tech stack
- Wiggly Crux engine (already implemented)
- Proposition/Argument/Attack models
- Perturbation simulation
- Impact propagation

## Files
- `vendor/wiggly/patala/` — Crux model, scholar_review kernel
- `hackathons/openaire/ideas3.md` — context
