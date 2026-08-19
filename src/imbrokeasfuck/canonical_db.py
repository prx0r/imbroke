"""Canonical DB — SQLite store for opportunities, sources, events."""
from __future__ import annotations
import sqlite3
import json
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Any

DB_PATH = Path(__file__).parent.parent.parent / "data" / "opportunities.db"

def connect() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("PRAGMA journal_mode=WAL")
    return conn

def migrate(conn: sqlite3.Connection):
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS sources (
        source_id TEXT PRIMARY KEY,
        source_type TEXT,
        priority TEXT,
        cadence_minutes INTEGER DEFAULT 3600,
        last_polled TEXT,
        status TEXT DEFAULT 'unknown'
    );
    CREATE TABLE IF NOT EXISTS opportunities (
        opportunity_id TEXT PRIMARY KEY,
        source_id TEXT,
        kind TEXT,
        title TEXT,
        sponsor TEXT,
        deadline TEXT,
        reward_type TEXT,
        reward_amount REAL,
        reuse_score REAL,
        rating TEXT,
        status TEXT DEFAULT 'active',
        first_seen TEXT,
        last_verified TEXT,
        metadata_json TEXT
    );
    CREATE TABLE IF NOT EXISTS events (
        event_id INTEGER PRIMARY KEY AUTOINCREMENT,
        opportunity_id TEXT,
        event_type TEXT,
        old_value TEXT,
        new_value TEXT,
        created_at TEXT,
        source_url TEXT
    );
    CREATE TABLE IF NOT EXISTS validation_results (
        fact TEXT,
        source_1 TEXT,
        source_1_status TEXT,
        source_2 TEXT,
        source_2_status TEXT,
        overall_status TEXT,
        verified_at TEXT
    );
    CREATE TABLE IF NOT EXISTS poll_state (
        source_id TEXT PRIMARY KEY,
        last_polled TEXT,
        next_polled TEXT,
        consecutive_failures INTEGER DEFAULT 0
    );
    """)

def upsert_opportunity(conn, opp_id: str, data: dict):
    now = datetime.now().isoformat()
    conn.execute("""
        INSERT OR REPLACE INTO opportunities 
        (opportunity_id, source_id, kind, title, sponsor, deadline, 
         reward_type, reward_amount, reuse_score, rating, status, first_seen, last_verified, metadata_json)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (opp_id, data.get("source"), data.get("kind"), data.get("title"),
          data.get("sponsor"), data.get("deadline"), data.get("reward_type"),
          data.get("reward_amount", 0), data.get("reuse_score", 0),
          data.get("rating", "B"), "active", now, now,
          json.dumps(data, default=str)))

def get_opportunities(conn, kind: str = None) -> list[dict]:
    if kind:
        rows = conn.execute("SELECT * FROM opportunities WHERE kind=? ORDER BY rating", (kind,)).fetchall()
    else:
        rows = conn.execute("SELECT * FROM opportunities ORDER BY rating").fetchall()
    cols = [d[0] for d in conn.execute("SELECT * FROM opportunities LIMIT 0").description]
    return [dict(zip(cols, row)) for row in rows]

def record_event(conn, opp_id: str, event_type: str, old_value: str = None, new_value: str = None):
    conn.execute("INSERT INTO events (opportunity_id, event_type, old_value, new_value, created_at) VALUES (?,?,?,?,?)",
                 (opp_id, event_type, old_value, new_value, datetime.now().isoformat()))
    conn.commit()

def record_validation(conn, fact: str, s1_name: str, s1_status: str, s2_name: str = None, s2_status: str = None):
    overall = "VERIFIED" if s1_status == "VERIFIED" and (s2_status == "VERIFIED" or s2_status is None) else "SINGLE"
    conn.execute("INSERT INTO validation_results VALUES (?,?,?,?,?,?,?)",
                 (fact, s1_name, s1_status, s2_name or "", s2_status or "", overall, datetime.now().isoformat()))
    conn.commit()

def get_stats(conn) -> dict:
    return {
        "opportunities": conn.execute("SELECT COUNT(*) FROM opportunities").fetchone()[0],
        "events": conn.execute("SELECT COUNT(*) FROM events").fetchone()[0],
        "validations": conn.execute("SELECT COUNT(*) FROM validation_results").fetchone()[0],
        "sources": conn.execute("SELECT COUNT(*) FROM sources").fetchone()[0],
    }
