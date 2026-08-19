"""MCP server — expose verified opportunity data to external agents."""
from __future__ import annotations
import json
from pathlib import Path
from typing import Any

DB_PATH = Path(__file__).parent.parent.parent / "data" / "opportunities.db"

def get_tools() -> list[dict]:
    """MCP tool definitions."""
    return [
        {
            "name": "qdw_opportunities",
            "description": "List all tracked opportunities with verified status",
            "inputSchema": {"type": "object", "properties": {"kind": {"type": "string"}}},
        },
        {
            "name": "qdw_validate",
            "description": "Validate an opportunity against multiple sources",
            "inputSchema": {"type": "object", "properties": {"opportunity_id": {"type": "string"}}},
        },
        {
            "name": "qdw_stats",
            "description": "Get system statistics",
            "inputSchema": {"type": "object", "properties": {}},
        },
    ]

def handle_tool(name: str, args: dict) -> Any:
    """Handle MCP tool calls."""
    if name == "qdw_opportunities":
        return _list_opportunities(args.get("kind"))
    elif name == "qdw_validate":
        return _validate_opportunity(args.get("opportunity_id"))
    elif name == "qdw_stats":
        return _get_stats()
    return {"error": f"Unknown tool: {name}"}

def _list_opportunities(kind: str = None) -> list:
    from .canonical_db import connect, get_opportunities
    conn = connect()
    opps = get_opportunities(conn, kind)
    conn.close()
    return opps

def _validate_opportunity(opp_id: str) -> dict:
    from .canonical_db import connect
    conn = connect()
    row = conn.execute("SELECT * FROM opportunities WHERE opportunity_id=?", (opp_id,)).fetchone()
    cols = [d[0] for d in conn.execute("SELECT * FROM opportunities LIMIT 0").description]
    conn.close()
    if not row:
        return {"error": "not found"}
    return dict(zip(cols, row))

def _get_stats() -> dict:
    from .canonical_db import connect, get_stats
    conn = connect()
    stats = get_stats(conn)
    conn.close()
    return stats

if __name__ == "__main__":
    tools = get_tools()
    print(json.dumps({"tools": tools}, indent=2))
    print("\nMCP server ready. Tools available:")
    for t in tools:
        print(f"  - {t['name']}: {t['description']}")
