#!/usr/bin/env python3
"""Continuous opportunity poller — runs every hour, updates feed."""
import asyncio
import json
import time
from pathlib import Path

FEED_FILE = Path(__file__).parent.parent.parent / "data" / "opportunity_feed.json"

async def poll_once():
    from .oracle.feeds import ingest_all
    from .bittensor import tao_price
    from .oracle.deadline import get_expiring_soon

    tao = await tao_price()
    data = await ingest_all(tao)

    # Add deadline info
    for opp in data["opportunities"]:
        if opp.get("deadline"):
            from datetime import datetime
            try:
                days = (datetime.fromisoformat(opp["deadline"]) - datetime.now()).days
                opp["days_left"] = days
                opp["urgency"] = "URGENT" if days <= 2 else "SOON" if days <= 7 else "UPCOMING"
            except:
                opp["days_left"] = 999
                opp["urgency"] = "FUTURE"

    # Save feed
    FEED_FILE.parent.mkdir(parents=True, exist_ok=True)
    FEED_FILE.write_text(json.dumps(data, indent=2, default=str))

    # Summary
    expiring = [o for o in data["opportunities"] if o.get("days_left", 999) <= 7]
    print(f"[{datetime.now().isoformat()}] Polled {data['total']} opportunities, {len(expiring)} expiring soon")

async def poll_loop(interval=3600):
    """Poll every hour."""
    while True:
        try:
            await poll_once()
        except Exception as e:
            print(f"Poll error: {e}")
        await asyncio.sleep(interval)

if __name__ == "__main__":
    asyncio.run(poll_loop())
