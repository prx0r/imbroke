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
