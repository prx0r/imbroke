"""Autonomous orchestrator — reads DB, dispatches to Hermes, logs results."""
from __future__ import annotations
import asyncio
import json
from datetime import datetime
from pathlib import Path
from .canonical_db import connect, migrate, get_opportunities, get_stats, record_event, record_validation


def identify_work(conn) -> list[dict]:
    """Read DB and identify what needs work."""
    work = []

    # Check for unvalidated facts
    unvalidated = conn.execute(
        "SELECT opportunity_id, title FROM opportunities WHERE last_verified IS NULL"
    ).fetchall()
    for row in unvalidated:
        work.append({"type": "validate", "target": row[0], "title": row[1]})

    # Check for approaching deadlines
    deadlines = conn.execute(
        "SELECT opportunity_id, title, deadline FROM opportunities WHERE deadline IS NOT NULL"
    ).fetchall()
    now = datetime.now().isoformat()
    for row in deadlines:
        if row[2] and row[2] < now:
            work.append({"type": "expired", "target": row[0], "title": row[1]})
        elif row[2]:
            try:
                dl = datetime.fromisoformat(row[2])
                if (dl - datetime.now()).days <= 7:
                    work.append({"type": "deadline_approaching", "target": row[0], "title": row[1]})
            except:
                pass

    # Check for new opportunities needed
    stats = {"opportunities": conn.execute("SELECT COUNT(*) FROM opportunities").fetchone()[0]}
    if stats["opportunities"] < 20:
        work.append({"type": "discover_more", "current": stats["opportunities"]})

    return work


def execute_work(work_items: list[dict]) -> list[dict]:
    """Execute identified work items."""
    results = []
    for item in work_items:
        if item["type"] == "validate":
            results.append({
                "action": "validate",
                "target": item["target"],
                "status": "needs_verification",
                "instruction": f"Verify {item['title']} from source URL",
            })
        elif item["type"] == "deadline_approaching":
            results.append({
                "action": "alert",
                "target": item["target"],
                "status": "deadline_approaching",
                "instruction": f"Deadline approaching for {item['title']}",
            })
        elif item["type"] == "discover_more":
            results.append({
                "action": "discover",
                "status": "needs_discovery",
                "instruction": f"Only {item['current']} opportunities. Search for more.",
            })
    return results


def log_results(conn, work: list[dict], results: list[dict]):
    """Log all actions to database."""
    for w, r in zip(work, results):
        record_event(conn, w.get("target", ""), r["action"], json.dumps(w), json.dumps(r))


def run_orchestration():
    """Main autonomous loop."""
    print(f"[{datetime.now().isoformat()}] Autonomous orchestration started")

    conn = connect()
    migrate(conn)

    # 1. Read DB
    work = identify_work(conn)
    print(f"  Identified {len(work)} work items")

    # 2. Execute work
    results = execute_work(work)
    for r in results:
        print(f"  {r['action']}: {r['instruction'][:60]}")

    # 3. Log results
    log_results(conn, work, results)

    # 4. Stats
    stats = {
        "work_identified": len(work),
        "work_executed": len(results),
        "timestamp": datetime.now().isoformat(),
    }
    print(f"\n  Stats: {json.dumps(stats)}")

    conn.close()
    return stats
