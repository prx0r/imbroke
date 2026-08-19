# Opportunities — Bittensor, Grants, Bounties

**Last updated:** 2026-08-19
**Strategy:** QDW continuously identify and manufacture the best available $200–$5,000 development shots

## Priority Ranking

| Rank | Target | Upfront Cost | GPU? | Reward Shape | QDW Reuse | Notes |
|------|--------|-------------|------|--------------|-----------|-------|
| **#1** | **SN118 Ditto** | Low — 0.04 TAO/eval + registration | No GPU; validators execute artifact | **Top 5 paid** | Workbench memory/context | **Best first target** |
| **#2** | **SN11 TrajectoryRL** | Medium — dynamic registration + 50 α/submission | No GPU/server | Winner-takes-all | GitGoblin + skill factory | Copyright transfers on win |
| **#3** | **SN62 Ridges** | Low–medium testing costs | No production GPU | Winner-takes-all | QDW autonomous coding | IP assigned to Hidden Harvest |
| **#4** | **SN61 RedTeam** | Cheap VPS | 8GB-ish server, no GPU | **Proportional rewards** | QDW experiment/search | Best reward structure |
| **#5** | **SN15 ORO** | Higher inference iteration spend | No owned GPU | King-of-hill heavy | Agent evolution | Monitor only |

**Key metric:** `expected payout × probability / (cash cost + QDW engineering hours)`

---

## #1 — SN118 Ditto: THE Strongest Discovery

This is the strongest discovery from the deeper search.

Ditto isn't selling inference. **You submit an agent-memory harness as a Docker artifact, and validators run it.** You can build and practice before you even need a Bittensor wallet/TAO. The production model is locked by the platform, so you aren't competing by buying better inference; you compete on memory architecture, prompting, tool use, retrieval and agent scaffolding.

That maps almost comically well onto what QDW Workbench already contains: memory bridge, context compilation, hashed handovers, session state and the distinction between candidate memory and authoritative QDW state.

And unlike SN11/Ridges, **Ditto spreads competitive miner rewards across five distinct miners**. Its current miner guide specifies a `65% / 14% / 10% / 7% / 4%` distribution. It also uses fresh procedurally generated cases, deterministic grading, equal weighting of tool and memory performance, and shared-seed re-evaluation for near misses.

The current public leaderboard is not empty either: it showed roughly **65 submissions**, with leading composites around `0.955`, `0.944`, `0.918`, and `0.910`.

So you have a concrete target:

> **Build a QDW factory whose objective is to move a Ditto memory harness from the starter baseline toward ≥0.91 composite.**

And importantly, **do nearly all experimentation before paying anything**.

Ditto's current evaluation fee is 0.04 TAO per submitted artifact. The docs explicitly let you run fixed evaluation and rotating practice locally first.

That means:

```
GitGoblin
  ↓
find frontier agent-memory work
  ↓
extract mechanisms
  ↓
QDW Ideas
  ↓
candidate memory architectures
  ↓
QDW Factory
  ↓
20 harness variants
  ↓
Ditto local evaluator
  ↓
cemetery losers
  ↓
mutate winners
  ↓
adversarial evaluation
  ↓
ONLY THEN pay for one real evaluation
```

**Do not rent a Vast GPU for this.** The actual mining artifact doesn't need one.

Your $150/month requirement is only about **$5/day**. The current SN118 miner pool is vastly larger than that when expressed at current subnet value; the problem is not the size of a paying slot, it's **getting and retaining one of the rewarded positions**. Bittensor rewards are volatile subnet alpha, so I would not treat leaderboard revenue as reliable rent money until you have actual on-chain earning history.

One wrinkle: the public leaderboard snapshot showed rollout-specific "Champion 90% / Tail 2.5%" labels while the current miner guide specifies 65/14/10/7/4. That means **check the live contract immediately before a paid submission**; these incentive mechanics are actively evolving.

**Economics:**
- 0.04 TAO per evaluation (~$8 at $204/TAO)
- Top 5 miners paid: 65/14/10/7/4 distribution
- No GPU, no server, no always-on infrastructure
- Can practice locally before paying
- Leaderboard: ~65 submissions, top composites 0.955, 0.944, 0.918, 0.910

**GitHub:** https://github.com/ditto-assistant/ditto-subnet

---

## #2 — SN11 TrajectoryRL: Purest QDW Factory Problem

TrajectoryRL remains an excellent fit:

> write SKILL.md → validator runs Hermes in real sandboxes → tests determine score → best skill wins.

No GPU. No always-on miner server. A 4GB-class dev machine is actually listed as sufficient in one current mining playbook.

This is essentially:

**GitGoblin + QDW Ideas + cemetery + factory evolution → SKILL.md**

And there is even recent research specifically on automatically extracting agent skills from open-source agent repositories, which is extremely close to the GitGoblin→QDW mechanism you're proposing.

**However, I found an economic catch.**

The current TrajectoryRL miner guide says each managed submission recycles **50 subnet alpha by default**, in addition to dynamic subnet registration.

At TAO.app's recent SN11 alpha price of `0.008849 TAO/α`, 50 α is roughly **0.44 TAO per submission** before price changes.

That is materially more expensive than Ditto's current 0.04-TAO evaluation fee.

And SN11 is **winner-take-all**: recent mining data showed 249/256 miner slots but only **one earning miner**.

So the correct QDW strategy is not spamming 30 submissions.

**Run 500 local mutations, pay once when you think you've found a genuine frontier improvement.**

Also note the terms: if your skill ever becomes reward-earning, copyright in that skill transfers to TrajectoryRL.

**Economics:**
- 0.47% of network emissions ≈ 6.94 TAO/day miner capacity ≈ $1,400/day theoretical
- 50 α per submission ≈ 0.44 TAO (~$90) per submission
- Winner-take-all: only 1 earning miner out of 256 slots

**GitHub:** https://github.com/trajectoryRL/trajectoryRL

---

## #3 — SN62 Ridges: Biggest QDW Overlap, But IP Terms Suck

Ridges lets miners submit an agent.py; validators throw real SWE problems at it and reward the best-performing coding agent. Production inference is provided through the subnet sandbox, while local testing uses your own provider.

Your existing QDW mechanisms are almost exactly the variables that matter:

```
repository reconnaissance
→ hypothesis formation
→ context selection
→ coding
→ test
→ failure classification
→ repair
→ verification
→ patch
```

So you could make a dedicated:

**QDW SWE Miner Factory**

and have GitGoblin continuously inspect strong coding-agent projects/papers for mechanisms.

**The problem is contractual rather than technical:** Ridges' February 2026 terms currently say a submitted agent's IP is **irrevocably assigned to Hidden Harvest Ventures**, with no retained ownership rights after upload for reward.

For something built from your valuable generic QDW machinery, I'd therefore isolate the submission:

```
QDW core      ← yours
   ↓
competition adapter
   ↓
generated Ridges-specific agent.py ← disposable
```

**Do not submit your general QDW IP.**

**Economics:**
- 1.29% emissions ≈ 19 TAO/day miner capacity
- One-shot upload credits available from Ridges team
- Local testing uses your own provider (OpenRouter, Targon, Chutes)

**GitHub:** https://github.com/ridgesai/ridges

---

## #4 — SN61 RedTeam: One Property The Others Lack

SN61's reward is **performance-proportional**, rather pure winner-take-all, and accepted challenge solutions can continue earning while their score decays.

That arguably makes it structurally better for your **$150/month reliability goal**.

The downside is that it's a more specialized authorized security competition, requires persistent infrastructure, and rewards currently sit below the larger agent subnets. I would keep all work strictly inside the published challenge/evaluation environment.

QDW could nevertheless treat every active authorized challenge as a `CompetitionSpec`, generate implementations, benchmark them locally, then submit the strongest legitimate solution.

I wouldn't make it project #1 because you already have much better primitives for memory and coding-agent work.

**Economics:**
- 0.59% emissions ≈ 8.71 TAO/day miner capacity
- 41% miners, 41% validators, 18% owner
- Accepted solutions stay reward-active while scores decay

**Docs:** https://docs.theredteam.io

---

## #5 — SN60 BitSec: Real But Poor Economics

BitSec is Bittensor subnet 60. Its miner system is currently active.

The live leaderboard recently showed Agent 3030 with a 16.7% score dated **August 9, 2026**, so this isn't an abandoned 2024 experiment.

The current miner architecture is:

miner writes vulnerability-analysis agent → agent is screened → validators execute it against sandboxed audited projects → results are compared with known audit findings → highest scoring eligible agent wins the round.

**It is explicitly winner-take-all.** Miners can submit repeatedly, but they pay their own inference costs; after submission closes, the miner agents and evaluation results become public.

BitSec also changed its system in May so that when a round completes evaluation, subnet emissions **automatically switch to that round's winning miner**.

So:

> **Are BitSec miners actually getting paid?**

**The winning miner is receiving Bittensor emissions. Other miners can spend inference money and receive nothing.**

TAO.app currently puts SN60 at only around **0.01% of network emissions**. Using the same rough 41%-miner-share comparison gives only about **0.148 TAO/day** of miner-side capacity at the present network allocation. At today's spot, that's only about **$30/day**.

So you could potentially spend serious OpenRouter/Chutes inference competing for a winner-takes-all pool whose *current* emissions are modest.

### But BitSec has a potentially much bigger second business

BitSec says its goal is not merely benchmarking. It plans to use the resulting security agents in its SaaS product **and in authorized bug-bounty/audit competitions**, with part of successful proceeds flowing back to miners whose agents contributed.

That could eventually dwarf its Bittensor emissions.

However, I could **not find evidence that those external bounty proceeds are already producing regular miner distributions today**. Their documentation talks about this as the intended commercialization path. Therefore I would value BitSec based on current emissions and treat external bounty revenue as unproven upside.

BitSec itself is nevertheless valuable as an **open research laboratory for security-agent architecture** because after rounds end, agent code, scores and evaluation logs become public.

That makes the rational play less "mine BitSec for income immediately" and more:

**study winning agents → reproduce benchmark → create stronger security-agent orchestration → enter when expected reward exceeds inference cost.**

Keep any security work strictly within these authorized benchmark/bounty environments.

**Docs:** https://docs.bitsec.ai

---

## Grant Programs

### Nosana Grants — High Priority

- **Amount:** $5K–$50K + compute/infrastructure
- **Review:** ~2 weeks, year-round
- **Eligible:** AI infrastructure, tooling, orchestration, agents, decentralized compute
- **URL:** https://nosana.com/grants/
- **Also:** Decentralize AI hackathon with free compute for builders
- **Proposal:** Decentralized-compute observatory (Akash + Nosana + Chutes + others)

### Akash Grants — High Priority

- **Amount:** Ecosystem grant (unspecified)
- **Eligible:** Open-source tools, infrastructure, specialized interfaces
- **URL:** https://akash.network/development/funding-program/
- **Proposal:** Akash adapter + neutral compute comparison/probing layer

### Heurist Developer Program

- **Amount:** 2K–10K free dev credits
- **Also:** x402 facilitator for paid API endpoints
- **URL:** https://sdk.heurist.ai

### LitVM Builders

- **Amount:** Incentivized testnet prize pool + post-mainnet grants
- **Eligible:** AI apps/agents, dev tooling
- **Status:** LiteForge testnet live April 2026
- **URL:** https://builders.litvm.com
- **Proposal:** QDW Forge for LitVM — verified machine-to-machine capabilities/payments

### Vana Grants

- **Amount:** Rolling data grants
- **Status:** Builder Cohort 2 opening soon
- **URL:** https://vana.org/participate
- **Proposal:** DataRightsBackend/LifeGit → actual data-rights/agent-context infrastructure

### Arweave/AO Onboard

- **Amount:** $1.5K+ and $10K+ tiers (mostly storage/compute credits)
- **URL:** https://onboard.arweave.net

---

## Bounty Firehoses

### Superteam Earn — #2 Overall (Bigger Than Bittensor For Paying Expenses)

Superteam now exposes an official **API specifically for autonomous agents**:

> agent registers → discovers `AGENT_ALLOWED` / `AGENT_ONLY` work → submits artifacts → human operator claims a winning payout.

That means they have effectively already defined an API contract for your `CompetitionFactory`.

You could make:

```
qdw-opportunity-superteam
```

which does:

```
poll agent-eligible listings
        ↓
normalize → Opportunity
        ↓
estimate:
  expected value
  build difficulty
  QDW reuse %
  deadline
  competition
  required skills
        ↓
GitGoblin prior-art research
        ↓
Idea portfolio
        ↓
factory
        ↓
verification
        ↓
human review
        ↓
submission
```

This is **literally a platform encouraging agents to autonomously find and complete paid work**.

And meaningful dev prizes exist: for example the current Zeroclaw Solana-plugin competition has a **$5,000 USDG pool**, split $1,800/$1,200/$1,000 plus bonuses.

That type of opportunity is far more sensible for your $150 survival target than needing to dethrone the best Bittensor miner every month.

Eligibility matters: Superteam explicitly keeps human payout claiming separate from the agent, and some grants/listings require KYC or regional eligibility. Only target opportunities you're actually eligible to claim; don't try to route around those requirements.

**URL:** https://superteam.fun/earn/agents

### Tether.dev — #3 Overall (Favorite Non-Bittensor Cash Target)

Its developer program opened in May 2026 and pays against specific completed technical deliverables rather than vague startup promises. Tether says current individual payouts are generally around **$1,500–$4,000**, and its live board presently shows a **5,000 USD₮ llama.cpp/CoreML/QVAC task** and **3,000 USD₮ Swift SDK task**.

That is exactly what QDW factories should eat:

`spec → GitGoblin research → implementation → upstream tests → adversarial verification → PR/deliverable`.

**URL:** https://tether.io/news/tether-launches-developer-grants-program

### RiseIn

- 300+ Web3/AI opportunities, $1.1M in open rewards
- **URL:** https://www.risein.com/earn

---

## The Strategy I Would Actually Run

Don't make "Bittensor mining" a separate life project.

Build **QDW Earn**:

```
                  GitGoblin
                      ↓
              opportunity radar
                      ↓
 ┌─────────────────────────────────────┐
 │ Bittensor SN118      benchmark      │
 │ Bittensor SN11       benchmark      │
 │ Bittensor SN62       benchmark      │
 │ Superteam            bounty         │
 │ Tether.dev           deliverable    │
 │ Nosana               grant          │
 │ Akash                grant/RFP      │
 │ LitVM                builder prog   │
 │ Vana                 grant/cohort   │
 └─────────────────────────────────────┘
                      ↓
               OpportunitySpec
                      ↓
          expected-value / reuse score
                      ↓
                 QDW Ideas
               ↙     ↓      ↘
          variants cemetery variants
               \      ↓      /
                  factory
                      ↓
                  evaluator
                      ↓
                   product
                      ↓
                 human gate
                      ↓
                  submission
                      ↓
                    $$$
```

The important objective becomes:

**`expected payout × probability of success / (cash cost + QDW engineering hours)`**

with an additional bonus for **reusable infrastructure**.

On that metric, today I would allocate your development attention roughly:

**Ditto SN118 → Superteam Earn adapter → Tether.dev radar → SN11 → Nosana/Akash proposals → Ridges → LitVM/Vana experiments.**

And I would **not rent a GPU yet**. None of my top four targets requires one. Only rent compute when a local benchmark or specific bounty demonstrably benefits from it.

The useful target isn't "make $150 every month from one subnet." It's **make QDW continuously identify and manufacture the best available $200–$5,000 development shots**, while Ditto/SN11 run as recurring upside. That is much more robust—and it turns work you were going to do anyway into a portfolio of paid external objectives.

---

## Stack Grants For Maximum Leverage

```
Akash grant    → development funding
Nosana grant   → development funding + GPU compute
Heurist        → inference credits
Bittensor/Chutes → inference source
same open-source core → useful independent product
```

without purchasing any of their tokens.

Heurist adds another clever mechanism: besides free development credits, it currently exposes an **x402 facilitator** intended to let developers charge for APIs/services through machine-readable payments.

So the infrastructure itself could eventually expose paid agent endpoints rather than depending forever on grants.
