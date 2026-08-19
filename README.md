# imbrokeasfuck — What We Actually Have

## The system

**imbrokeasfuck** is a crypto AI opportunity tracker + economic factory system.

```
15 sources → Oracle → Deadline Tracker → Priority Ranker
     ↓
  61+ opportunities
     ↓
  ranked by: urgency × value × reuse
     ↓
  what to work on RIGHT NOW
```

## What works (tested)

| Component | Commands | Status |
|-----------|----------|--------|
| Oracle (15 sources) | `ibf --oracle` | ✅ 61 opportunities |
| Deadline tracker | `ibf --expiring 7` | ✅ |
| Priority ranker | `ibf --prioritize` | ✅ |
| Validation | `ibf --validate` | ✅ 8/9 checks pass |
| Bittensor economics | `ibf --economics` | ✅ |
| Factories (4) | `ibf --factory 118` | ✅ MAP-Elites |
| Revenue channels | `ibf --revenue` | ✅ 5 channels |
| Hackathons | `ibf --hackathons` | ✅ 7 targets |
| Strategy | `ibf --strategy` | ✅ 60/25/15 |
| Web dashboard | localhost:8420 | ✅ |
| Hermes | mimo-v2.5 via opencode-go | ✅ |

## What's stale (should delete)

| Path | Why |
|------|-----|
| `hydrabite/` | Replaced by submission ZIP |
| `hydraroute/` | Replaced by HydraBite |
| `patala_research_ci/` | Replaced by submission ZIP |
| `proposals/` | Superseded by focused strategy |

## What's reference only (keep but don't build on)

| Path | What |
|------|------|
| `vendor/wiggly/` | Evidence-state machine |
| `vendor/hydradb/` | Graph database |
| `vendor/ditto-subnet/` | Bittensor competition |
| `vendor/dfresearch/` | Autonomous research loop |
| `vendor/chainwake/` | Event-driven watcher |
| `vendor/text-fabric/` | Scholarly text annotation |

## File structure

```
imbrokeasfuck/
├── src/imbrokeasfuck/          # Core system (43 Python files)
│   ├── apis.py                # CoinGecko, DefiLlama, Fear/Greed
│   ├── bittensor.py           # Subnet economics
│   ├── tracker.py             # 17 project tracking
│   ├── oracle/                # 15 sources, 61+ opportunities
│   ├── earn/                  # Factories, evolution, revenue
│   ├── cli.py                 # 15+ commands
│   ├── server.py              # Web dashboard
│   └── validator.py           # Dell-style validation
├── hackathons/                # Hackathon plans
│   ├── openaire/             # OpenAIRE submission
│   └── hydra/                # Hack Hydra submission
├── data/                      # Validation results, feeds
├── vendor/                    # 35 reference repos
└── web/                       # Dashboard UI
```
