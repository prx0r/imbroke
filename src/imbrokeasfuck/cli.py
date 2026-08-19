"""CLI for imbrokeasfuck."""
from __future__ import annotations
import asyncio
import json
import sys
from .tracker import fetch_all, format_report
from .bittensor import fetch_bittensor_data, format_opportunities
from .oracle import ingest_all
from .oracle.github_signals import scan_all_github_signals
from .oracle.bittensor_economics import format_all_economics, format_economics, SUBNET_CONTRACTS
from .earn.factory import FACTORY_REGISTRY, FactoryState
from .earn.revenue import RECOMMENDED_CHANNELS
from .earn.strategy import format_strategy, strategy_dict
from .earn.hackathons import format_hackathons, hackathon_dict
from .earn.wiggly import format_wiggly_reuse


def main():
    import argparse
    p = argparse.ArgumentParser(prog="ibf", description="Crypto AI project tracker + opportunity oracle")
    p.add_argument("--json", action="store_true", help="Output raw JSON")
    p.add_argument("--project", "-p", help="Show single project by slug")
    p.add_argument("--ops", action="store_true", help="Show opportunity radar")
    p.add_argument("--oracle", action="store_true", help="Run full opportunity oracle")
    p.add_argument("--bittensor", action="store_true", help="Show Bittensor subnet data")
    p.add_argument("--tao", action="store_true", help="Show TAO price only")
    p.add_argument("--github", action="store_true", help="Scan GitHub for early signals")
    p.add_argument("--economics", action="store_true", help="Show miner economics calculations")
    p.add_argument("--contract", type=int, help="Show contract details for subnet (e.g. --contract 118)")
    p.add_argument("--factory", type=int, help="Run factory for subnet (e.g. --factory 118)")
    p.add_argument("--factories", action="store_true", help="Show all factory statuses")
    p.add_argument("--superteam", action="store_true", help="Check Superteam agent API")
    p.add_argument("--revenue", action="store_true", help="Show serve-to-earn revenue channels")
    p.add_argument("--strategy", action="store_true", help="Show 60/25/15 strategy")
    p.add_argument("--hackathons", action="store_true", help="Show hackathon targets")
    p.add_argument("--wiggly", type=str, help="Show Wiggly reuse for hackathon (e.g. --wiggly telegraph)")
    args = p.parse_args()

    if args.oracle:
        data = asyncio.run(ingest_all())
        if args.json:
            print(json.dumps(data, indent=2, default=str))
        else:
            print(f"\n{'='*70}")
            print(f"  OPPORTUNITY ORACLE - {data['total']} opportunities")
            print(f"{'='*70}\n")
            for opp in data["opportunities"]:
                r = opp.get("rating", "?")
                rec = opp.get("recommendation", "?")
                kind = opp.get("kind", "?")
                title = opp.get("title", "?")[:55]
                fit = opp.get("reuse_score", 0)
                print(f"  [{r}] {rec:<12} {kind:<12} fit={fit:.0%}  {title}")
            print(f"\n{'='*70}")
    elif args.github:
        data = asyncio.run(scan_all_github_signals())
        if args.json:
            print(json.dumps(data, indent=2, default=str))
        else:
            print(f"\n{'='*70}")
            print(f"  GITHUB EARLY SIGNALS - {len(data)} signals")
            print(f"{'='*70}\n")
            for s in data:
                print(f"  [{s['type']:<8}] {s['repo']:<30} {s.get('keyword','')}")
            print(f"\n{'='*70}")
    elif args.ops:
        data = asyncio.run(fetch_bittensor_data())
        if args.json:
            print(json.dumps(data, indent=2, default=str))
        else:
            print(format_opportunities(data))
    elif args.economics:
        if args.json:
            data = {str(k): v.to_dict() for k, v in SUBNET_CONTRACTS.items()}
            print(json.dumps(data, indent=2, default=str))
        else:
            print(format_all_economics())
    elif args.contract:
        contract = SUBNET_CONTRACTS.get(args.contract)
        if contract:
            if args.json:
                print(json.dumps(contract.to_dict(), indent=2, default=str))
            else:
                print(format_economics(contract))
        else:
            print(f"Unknown subnet: {args.contract}")
            print(f"Available: {', '.join(str(k) for k in sorted(SUBNET_CONTRACTS.keys()))}")
    elif args.factory:
        subnet = args.factory
        if subnet in FACTORY_REGISTRY:
            factory = FACTORY_REGISTRY[subnet]()
            factory.initialize()
            print(f"\n{'='*60}")
            print(f"  Factory: {factory.name} (SN{subnet})")
            print(f"{'='*60}\n")
            for i in range(5):
                result = factory.step()
                print(f"  Step {i+1}: {result.get('action')} - gen={result.get('generation', factory.generation)}")
                if "population_stats" in result:
                    ps = result["population_stats"]
                    print(f"    Niches: {ps['niches_filled']}/{ps['niches_total']} filled, {ps['total_candidates']} candidates")
            print(f"\n  Summary:")
            s = factory.summary()
            for k, v in s.items():
                if isinstance(v, dict):
                    print(f"    {k}: ...")
                else:
                    print(f"    {k}: {v}")
        else:
            print(f"No factory for subnet {subnet}")
            print(f"Available: {', '.join(str(k) for k in sorted(FACTORY_REGISTRY.keys()))}")
    elif args.factories:
        print(f"\n{'='*60}")
        print(f"  FACTORY STATUS")
        print(f"{'='*60}\n")
        for subnet, creator in sorted(FACTORY_REGISTRY.items()):
            factory = creator()
            print(f"  SN{subnet:<4} {factory.name:<25} {factory.state.value:<12} {factory.artifact_type}")
        print(f"\n{'='*60}")
    elif args.superteam:
        from .earn.superteam import check_superteam_api_health, fetch_superteam_agent_listings
        health = asyncio.run(check_superteam_api_health())
        print(f"\n  Superteam API: {health['status']}")
        if health["status"] == "ok":
            print(f"  Listings: {health['listings_count']}")
            listings = asyncio.run(fetch_superteam_agent_listings())
            print(f"  Opportunities: {len(listings)}")
            for opp in listings[:5]:
                print(f"    [{opp.rating}] {opp.kind:<10} fit={opp.reuse_score:.0%}  {opp.title[:50]}")
    elif args.revenue:
        print(f"\n{'='*60}")
        print(f"  SERVE-TO-EARN REVENUE CHANNELS")
        print(f"{'='*60}\n")
        for ch in RECOMMENDED_CHANNELS:
            print(f"  {ch.name}")
            print(f"    Platform: {ch.platform} | Model: {ch.pricing_model}")
            print(f"    Price: ${ch.price_per_call_usd}/call | Est: {ch.estimated_monthly_calls} calls/mo")
            print(f"    Revenue: ${ch.estimated_monthly_revenue_usd}/mo | Cost: ${ch.infrastructure_cost_usd}/mo")
            print(f"    Net: ${ch.net_monthly_revenue():.2f}/mo | ROI: {ch.roi():.1f}x")
            print()
        total_rev = sum(ch.estimated_monthly_revenue_usd for ch in RECOMMENDED_CHANNELS)
        total_cost = sum(ch.infrastructure_cost_usd for ch in RECOMMENDED_CHANNELS)
        print(f"  {'='*50}")
        print(f"  Total estimated: ${total_rev:.2f}/mo revenue, ${total_cost:.2f}/mo cost")
        print(f"  Net: ${total_rev - total_cost:.2f}/mo")
        print(f"{'='*60}")
    elif args.strategy:
        if args.json:
            print(json.dumps(strategy_dict(), indent=2, default=str))
        else:
            print(format_strategy())
    elif args.hackathons:
        if args.json:
            print(json.dumps(hackathon_dict(), indent=2, default=str))
        else:
            print(format_hackathons())
    elif args.wiggly:
        print(format_wiggly_reuse(args.wiggly))
    elif args.bittensor:
        data = asyncio.run(fetch_bittensor_data())
        if args.json:
            print(json.dumps(data.get("subnets", {}), indent=2, default=str))
        else:
            print(format_opportunities(data))
    elif args.tao:
        from .bittensor import tao_price
        price = asyncio.run(tao_price())
        print(f"${price:.2f}")
    elif args.project:
        data = asyncio.run(fetch_all())
        proj = data.get("projects", {}).get(args.project)
        if proj:
            print(json.dumps(proj, indent=2, default=str))
        else:
            print(f"Unknown: {args.project}")
            sys.exit(1)
    elif args.json:
        data = asyncio.run(fetch_all())
        print(json.dumps(data, indent=2, default=str))
    else:
        data = asyncio.run(fetch_all())
        print(format_report(data))


if __name__ == "__main__":
    main()
