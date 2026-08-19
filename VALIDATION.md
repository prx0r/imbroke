# Fact Validation — All claims verified against sources

**Date:** 2026-08-19
**Status:** All key facts checked and confirmed

---

## Verified facts

| Claim | Source | Status |
|-------|--------|--------|
| OpenAIRE grand prize: €500 | hackathon page + submission template | ✅ VERIFIED |
| Hack Hydra prize: $5,000 | hackathons.space + Luma page | ✅ VERIFIED |
| Ditto miner pool: 34.16 TAO/day | bittensor.ai/subnets/118 | ✅ VERIFIED |
| TAO price: ~$192 | DefiLlama API live query | ✅ VERIFIED |
| OpenAIRE entities: 386M+ | API query returns 386,595,732 | ✅ VERIFIED |
| Hack Hydra deadline: Aug 20, 11:59 PM PT | hackathons.space + Luma | ✅ VERIFIED |
| OpenAIRE deadline: Aug 20, 23:59 CEST | hackathon page FAQ | ✅ VERIFIED |
| HydraDB backed by Sky9 Capital | hackathons.space page | ✅ VERIFIED |
| Ditto: 65/14/10/7/4 distribution | ditto-subnet repo docs | ✅ VERIFIED |
| Ditto: no GPU required | ditto-subnet README | ✅ VERIFIED |
| OpenAIRE: 386M+ entities | API live query | ✅ VERIFIED |

## API endpoints verified working

| Endpoint | Status |
|----------|--------|
| `api.openaire.eu/graph/v3/research-products` | ✅ Returns 386M+ |
| `coins.llama.fi/prices/current/coingecko:bittensor` | ✅ Returns $191.63 |
| `api.alternative.me/fng/` | ✅ Returns Fear & Greed |
| `127.0.0.1:9902/v1/health` | ✅ qdw-node running |
| `127.0.0.1:9911/health` | ✅ bridge running |

## Code verified working

| Component | Status |
|-----------|--------|
| imbrokeasfuck CLI | ✅ 15+ commands |
| Oracle (15 sources) | ✅ 61 opportunities |
| Deadline tracker | ✅ Expiring filter works |
| Priority ranker | ✅ Urgency × value × reuse |
| qdw-node | ✅ All 12 endpoints |
| QDW bridge | ✅ All 15 endpoints |
| HydraBite | ✅ 12/12 tests pass |
