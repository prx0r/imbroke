"""Web server — API endpoints matching Dell patterns."""
from __future__ import annotations
import asyncio
import json
import os
from datetime import datetime
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
from pathlib import Path

WEB_DIR = Path(__file__).resolve().parent.parent.parent / "web"


class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        routes = {
            "/api/v1/models": self._models,
            "/api/v1/opportunities": self._opportunities,
            "/api/v1/hackathons": self._hackathons,
            "/api/v1/subnets": self._subnets,
            "/api/v1/economics": self._economics,
            "/api/v1/deals": self._deals,
            "/api/v1/deals/live": self._deals_live,
            "/api/v1/deals/expiring": self._deals_expiring,
            "/api/v1/prices": self._prices,
            "/api/v1/fear-greed": self._fear_greed,
            "/api/v1/stats": self._stats,
            "/api/v1/validate": self._validate,
            "/api/v1/strategy": self._strategy,
        }
        handler = routes.get(self.path)
        if handler:
            self._serve_json(handler())
        elif self.path == "/" or self.path == "/index.html":
            self.path = "/index.html"
            super().do_GET()
        else:
            super().do_GET()

    def _serve_json(self, data):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, default=str).encode())

    def _models(self):
        from imbrokeasfuck.tracker import PROJECTS
        return {k: {"name": v.get("name", k), "category": v.get("category")} for k, v in PROJECTS.items()}

    def _opportunities(self):
        from imbrokeasfuck.oracle.feeds import ingest_all
        return asyncio.run(ingest_all())

    def _hackathons(self):
        from imbrokeasfuck.earn.hackathons import HACKATHONS
        return {k: {"name": v.name, "deadline": v.deadline, "prize": v.prize_pool} for k, v in HACKATHONS.items()}

    def _subnets(self):
        from imbrokeasfuck.oracle.bittensor_economics import SUBNET_CONTRACTS
        return {str(k): {"name": v.name, "miner_pool": v.miner_pool_tao_day} for k, v in SUBNET_CONTRACTS.items()}

    def _economics(self):
        from imbrokeasfuck.oracle.bittensor_economics import SUBNET_CONTRACTS
        return {str(k): {"pool": v.miner_pool_tao_day, "fee": v.submission_cost_tao} for k, v in SUBNET_CONTRACTS.items()}

    def _deals(self):
        from imbrokeasfuck.tracker import PROJECTS
        return [{"id": k, **v} for k, v in PROJECTS.items()]

    def _deals_live(self):
        from imbrokeasfuck.tracker import PROJECTS
        return [{"id": k, **v} for k, v in PROJECTS.items()]

    def _deals_expiring(self):
        from imbrokeasfuck.tracker import PROJECTS
        return [{"id": k, **v} for k, v in PROJECTS.items()]

    def _prices(self):
        from imbrokeasfuck.apis import coingecko_price
        return asyncio.run(coingecko_price(["bitcoin", "ethereum", "bittensor"]))

    def _fear_greed(self):
        from imbrokeasfuck.apis import fear_greed
        try:
            fg = asyncio.run(fear_greed(1))
            return fg[0] if fg else {}
        except:
            return {}

    def _stats(self):
        from imbrokeasfuck.oracle.sources import ALL_SOURCES
        return {"sources": len(ALL_SOURCES), "status": "ok"}

    def _validate(self):
        from imbrokeasfuck.oracle.three_pass import KEY_FACTS, check_source
        async def _run():
            results = []
            for f in KEY_FACTS:
                checks = []
                for src in f["sources"]:
                    c = await check_source(src)
                    checks.append(c)
                confirmed = sum(1 for c in checks if c["live"] and c["found"])
                results.append({"fact": f["fact"], "status": "VERIFIED" if confirmed >= 2 else "SINGLE"})
            return {"results": results, "timestamp": datetime.now().isoformat()}
        return asyncio.run(_run())

    def _strategy(self):
        from imbrokeasfuck.earn.strategy import STRATEGY
        return {k: {"allocation": f"{v.allocation_pct}%", "target": v.primary_target} for k, v in STRATEGY.items()}

    def log_message(self, format, *args):
        pass


def main():
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--port", type=int, default=8420)
    p.add_argument("--host", default="0.0.0.0")
    args = p.parse_args()
    os.chdir(WEB_DIR)
    with TCPServer((args.host, args.port), Handler) as httpd:
        print(f"imbrokeasfuck hub at http://localhost:{args.port}")
        httpd.serve_forever()


if __name__ == "__main__":
    main()
