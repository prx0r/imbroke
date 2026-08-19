"""CLI for imbrokeasfuck."""
from __future__ import annotations
import asyncio
import json
import sys
from .tracker import fetch_all, format_report
from .bittensor import fetch_bittensor_data, format_opportunities


def main():
    import argparse
    p = argparse.ArgumentParser(prog="ibf", description="Crypto AI project tracker + opportunity radar")
    p.add_argument("--json", action="store_true", help="Output raw JSON")
    p.add_argument("--project", "-p", help="Show single project by slug")
    p.add_argument("--ops", action="store_true", help="Show opportunity radar")
    p.add_argument("--bittensor", action="store_true", help="Show Bittensor subnet data")
    p.add_argument("--grants", action="store_true", help="Show grant programs")
    p.add_argument("--tao", action="store_true", help="Show TAO price only")
    args = p.parse_args()

    if args.ops:
        data = asyncio.run(fetch_bittensor_data())
        if args.json:
            print(json.dumps(data, indent=2, default=str))
        else:
            print(format_opportunities(data))
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
            print(f"Unknown project: {args.project}")
            print(f"Available: {', '.join(sorted(data.get('projects', {}).keys()))}")
            sys.exit(1)
    elif args.json:
        data = asyncio.run(fetch_all())
        print(json.dumps(data, indent=2, default=str))
    else:
        data = asyncio.run(fetch_all())
        print(format_report(data))


if __name__ == "__main__":
    main()
