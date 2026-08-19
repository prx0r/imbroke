# imbrokeasfuck

Crypto AI project tracker — Bittensor subnets, Virtuals, Akash, Venice, and 20+ protocols.

## What it tracks

| Category | Projects |
|----------|----------|
| **Decentralized Inference** | Chutes (SN64), Venice, FLock, 0G |
| **Compute Markets** | Akash, Nosana, io.net, Aethir |
| **Agent Economy** | Virtuals/ACP, Olas/Mech |
| **Verification** | EigenCloud, Phala (TEE), Lit Protocol |
| **Data/Provenance** | OpenLedger, Vana, Sahara AI |
| **Storage + Persistent Compute** | Arweave/AO |
| **Payments** | x402/PayAI |

## Data sources

- **DefiLlama** — TVL, fees, revenue, protocol metrics (free, no key)
- **CoinGecko** — prices, market cap, 24h change (free tier)
- **Fear & Greed Index** — Alternative.me (free)
- **Bittensor** — subnet registry via btcli/SDK (on-chain)
- **CoinMarketCap** — via x402 micropayments (optional)

## Quick start

```bash
cd imbrokeasfuck
python3 -m pip install -e .

# Full report
ibf

# JSON output
ibf --json

# Single project
ibf --project chutes
ibf --project venice
ibf --project virtuals
```

## Without install

```bash
cd imbrokeasfuck
PYTHONPATH=src python3 -m imbrokeasfuck.cli
```

## Available MCP servers

| Server | Install |
|--------|---------|
| CoinGecko | `npx -y @coingecko/coingecko-mcp` or remote `https://mcp.api.coingecko.com/mcp` |
| Venice | `npx -y @veniceai/mcp-server` |
| x402 wrapper | `@x402/mcp` — wraps any MCP tool with payment |

## Project slugs

```
chutes virtuals olas akash venice 0g eigen phala lit aethir
nosana ionet openledger flock vana sahara arweave
```
