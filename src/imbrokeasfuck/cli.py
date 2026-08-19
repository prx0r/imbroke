"""CLI for imbrokeasfuck."""
from __future__ import annotations
import asyncio
import json
import sys
from .tracker import fetch_all, format_report


def main():
    import argparse
    p = argparse.ArgumentParser(prog="ibf", description="Crypto AI project tracker")
    p.add_argument("--json", action="store_true", help="Output raw JSON")
    p.add_argument("--project", "-p", help="Show single project by slug")
    args = p.parse_args()

    data = asyncio.run(fetch_all())

    if args.json:
        print(json.dumps(data, indent=2, default=str))
    elif args.project:
        proj = data.get("projects", {}).get(args.project)
        if proj:
            print(json.dumps(proj, indent=2, default=str))
        else:
            print(f"Unknown project: {args.project}")
            print(f"Available: {', '.join(sorted(data.get('projects', {}).keys()))}")
            sys.exit(1)
    else:
        print(format_report(data))


if __name__ == "__main__":
    main()
