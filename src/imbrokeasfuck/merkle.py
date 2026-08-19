"""Merkle proofs — data integrity for opportunity records."""
from __future__ import annotations
import hashlib
import json
from typing import Any


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def merkle_root(leaves: list[str]) -> str:
    """Compute Merkle root from leaf hashes."""
    if not leaves:
        return sha256(b"empty")
    current = [sha256(l.encode()) for l in leaves]
    while len(current) > 1:
        next_level = []
        for i in range(0, len(current), 2):
            left = current[i]
            right = current[i + 1] if i + 1 < len(current) else left
            combined = sha256((left + right).encode())
            next_level.append(combined)
        current = next_level
    return current[0]


def record_hash(record: dict) -> str:
    """Hash a record for Merkle tree."""
    canonical = json.dumps(record, sort_keys=True, default=str)
    return sha256(canonical.encode())


def create_merkle_proof(records: list[dict]) -> dict:
    """Create Merkle proof for a set of records."""
    hashes = [record_hash(r) for r in records]
    root = merkle_root(hashes)
    return {
        "root": root,
        "count": len(records),
        "hashes": hashes,
        "created_at": __import__("datetime").datetime.now().isoformat(),
    }


def verify_proof(proof: dict, records: list[dict]) -> bool:
    """Verify Merkle proof matches records."""
    hashes = [record_hash(r) for r in records]
    root = merkle_root(hashes)
    return root == proof["root"]
