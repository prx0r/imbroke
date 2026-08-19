"""Hermes integration — autonomous execution without prompts."""
from __future__ import annotations
import sqlite3
import json
from datetime import datetime
from typing import Any

from .canonical_db import connect
from .merkle import create_merkle_proof, verify_proof


def hermes_decide() -> dict:
    """Hermes reads DB and decides what to do. NO prompts."""
    conn = connect()

    # 1. Check what needs work
    unvalidated = conn.execute(
        "SELECT COUNT(*) FROM opportunities WHERE last_verified IS NULL"
    ).fetchone()[0]

    never_polled = conn.execute(
        "SELECT COUNT(*) FROM sources WHERE last_polled IS NULL"
    ).fetchone()[0]

    # 2. Check approaching deadlines
    deadlines = conn.execute(
        "SELECT opportunity_id, title, deadline FROM opportunities WHERE deadline IS NOT NULL"
    ).fetchall()
    approaching = []
    for row in deadlines:
        try:
            dl = datetime.fromisoformat(row[2])
            days_left = (dl - datetime.now()).days
            if days_left <= 30:
                approaching.append({"id": row[0], "title": row[1], "days_left": days_left})
        except:
            pass

    # 3. Decide actions
    actions = []
    if unvalidated > 0:
        actions.append({"action": "validate", "count": unvalidated})
    if never_polled > 0:
        actions.append({"action": "poll", "count": never_polled})
    if approaching:
        actions.append({"action": "check_deadlines", "items": approaching})

    # 4. Execute
    results = []
    for action in actions:
        if action["action"] == "validate":
            # Run validation
            results.append({"action": "validate", "status": "scheduled"})
        elif action["action"] == "poll":
            # Run polling
            results.append({"action": "poll", "status": "scheduled"})
        elif action["action"] == "check_deadlines":
            results.append({"action": "check_deadlines", "status": "checked", "items": action["items"]})

    # 5. Record decision
    conn.execute(
        "INSERT INTO events (opportunity_id, event_type, new_value, created_at) VALUES (?, ?, ?, ?)",
        ("hermes", "decide", json.dumps({"actions": actions, "results": results}, default=str), datetime.now().isoformat())
    )
    conn.commit()
    conn.close()

    return {
        "unvalidated": unvalidated,
        "never_polled": never_polled,
        "approaching_deadlines": approaching,
        "actions": actions,
        "results": results,
    }


def hermes_execute() -> dict:
    """Execute actions from hermes_decide."""
    decision = hermes_decide()

    # Run polling
    from .poller import poll_all_sources
    poll_results = poll_all_sources()

    # Run validation
    from .oracle.three_pass import run_validation
    val_results = run_validation()

    # Run blog monitoring
    from .blogs import monitor_blogs
    blog_results = monitor_blogs()

    return {
        "decision": decision,
        "polling": poll_results,
        "validation": val_results,
        "blogs": blog_results,
    }
