"""Web server for imbrokeasfuck dashboard."""
from __future__ import annotations
import asyncio
import json
import os
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
from pathlib import Path

WEB_DIR = Path(__file__).resolve().parent.parent.parent / "web"

class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/api/projects":
            self._serve_json(self._fetch_projects())
        elif self.path == "/api/opps":
            self._serve_json(self._fetch_opps())
        elif self.path.startswith("/api/fear-greed"):
            self._serve_json(self._fetch_fg())
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

    def _fetch_projects(self):
        from imbrokeasfuck.tracker import fetch_all
        return asyncio.run(fetch_all())

    def _fetch_opps(self):
        from imbrokeasfuck.bittensor import fetch_bittensor_data, GRANTS, BOUNTY_PLATFORMS
        data = asyncio.run(fetch_bittensor_data())
        data["grants"] = GRANTS
        data["bounties"] = BOUNTY_PLATFORMS
        return data

    def _fetch_fg(self):
        from imbrokeasfuck.apis import fear_greed
        try:
            fg = asyncio.run(fear_greed(1))
            return fg[0] if fg else {}
        except Exception:
            return {}

    def log_message(self, format, *args):
        pass  # Suppress logs


def main():
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--port", type=int, default=8420)
    p.add_argument("--host", default="0.0.0.0")
    args = p.parse_args()

    os.chdir(WEB_DIR)
    with TCPServer((args.host, args.port), Handler) as httpd:
        print(f"imbrokeasfuck hub running at http://localhost:{args.port}")
        httpd.serve_forever()


if __name__ == "__main__":
    main()
