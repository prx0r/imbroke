# Repo Review — What's Interesting

**Date:** 2026-08-19

---

## Tier 1: Directly useful for OpenAIRE hackathon

### chainwake (taostat/chainwake)
**What:** Event-driven chain watcher for AI agents. Watches Bittensor, Ethereum, Base, BNB.
**Why useful:** Could watch OpenAIRE Graph releases as events. "Set a hook on graph state, wake when it changes."
**Reuse:** High — the watcher pattern maps directly to GraphGit.

### ditto-subnet (ditto-assistant/ditto-subnet)
**What:** Bittensor SN118 — agent memory harness competition.
**Why useful:** Our primary Bittensor target. Full miner CLI, validator, scoring, benchmark.
**Reuse:** Direct — this is what we're competing against.

### dfresearch (BitMind-AI/dfresearch)
**What:** Autonomous deepfake detection research loop.
**Why useful:** Reference implementation of "agent modifies code → trains → evaluates → keeps/discards → repeats."
**Reuse:** Medium — pattern maps to our evolutionary factories.

### gasbench (BitMind-AI/gasbench)
**What:** Benchmark evaluation for discriminative models.
**Why useful:** Reference for how to build evaluation harnesses.
**Reuse:** Medium — pattern useful for MemoryProof.

---

## Tier 2: Interesting reference

### G.O.D (gradients-ai/G.O.D)
**What:** Gradients on Demand subnet — training tournaments.
**Why useful:** Public tournament APIs, winning repos published as open source.
**Reuse:** Medium — reference for Gradients factory.

### RedTeam (RedTeamSubnet/RedTeam)
**What:** Decentralized cybersecurity challenges.
**Why useful:** Similarity checking, originality scoring, softmax normalization.
**Reuse:** Low — different domain, but mechanics are interesting.

### trajrl-bench (trajectoryRL/trajrl-bench)
**What:** Benchmark scenarios for TrajectoryRL SN11.
**Why useful:** Docker-based sandbox with Hermes, per-scenario images.
**Reuse:** Medium — reference for benchmark design.

### bittensor-auth (ORO-AI/bittensor-auth)
**What:** SR25519 auth for Bittensor subnets.
**Why useful:** Drop-in auth layer for any subnet API.
**Reuse:** High if we build subnet APIs.

---

## Tier 3: Reference only

### iis (openaire/iis)
**What:** OpenAIRE's Information Inference Service. Java/Spark/Hadoop.
**Why useful:** Shows how OpenAIRE does inference at scale. Workflows: citation matching, affiliation matching, document classification, collapsing.
**Reuse:** Low — too heavy to run, but shows their inference pipeline.

### wiggly (prx0r/wiggly)
**What:** OpenPatala — our core evidence-state machine.
**Why useful:** THE product. Everything else builds on this.
**Reuse:** 100% — this is the submission.

---

## Tier 4: Forked repos

### neverbrokeagain-dell
**What:** Dell — inference economics data for LLM routing.
**Why useful:** Could provide cost data for Research CI (how much did this analysis cost to run?).
**Reuse:** Medium — economics layer.

### neverbrokeagain-qdw
**What:** QDW — autonomous agent factory.
**Why useful:** Competition factory, evolutionary search, cemetery system.
**Reuse:** Medium — behind-the-scenes machinery.

### neverbrokeagain-gitgoblin
**What:** GitGoblin — frontier discovery, repo scanning.
**Why useful:** Could watch OpenAIRE repos/changes.
**Reuse:** Medium — sensor layer.

---

## What to actually use tomorrow

For the OpenAIRE hackathon:

1. **wiggly** — core evidence-state machine
2. **chainwake** — pattern for watching graph changes
3. **patalacheckpoints** — demo UI (ReactFlow graph)

For Bittensor:

1. **ditto-subnet** — primary target
2. **dfresearch** — evolutionary loop pattern
3. **trajrl-bench** — benchmark design reference
4. **bittensor-auth** — auth layer if needed
