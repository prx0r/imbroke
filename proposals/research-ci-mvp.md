# Research CI — Advanced MVP Tech Spec

**Status:** Ready to build
**Deadline:** Aug 20, 23:59 CEST

---

## What this is

A Python package that tracks research analyses against OpenAIRE, detects when the Graph changes, maps changes to claims, and emits proof obligations.

## Repo structure

```
patala-research-ci/
├── README.md
├── STORY.md
├── pyproject.toml
├── src/
│   └── research_ci/
│       ├── __init__.py
│       ├── openaire.py          # OpenAIRE V3 adapter
│       ├── normalize.py         # Canonical record normalization
│       ├── snapshot.py          # Content-addressed snapshots
│       ├── tracked.py           # TrackedAnalysis + TrackedClaim
│       ├── diff.py              # Semantic diff engine
│       ├── impact.py            # Dependency → impact mapping
│       ├── obligations.py       # Proof obligation generator
│       ├── ledger.py            # Append-only event store
│       ├── materiality.py       # Change classification
│       └── cli.py               # CLI entry point
├── fixtures/
│   ├── before/                  # Old OpenAIRE state
│   └── after/                   # New OpenAIRE state
├── tests/
│   ├── test_openaire.py
│   ├── test_diff.py
│   ├── test_impact.py
│   └── test_obligations.py
└── examples/
    └── funding_analysis/
```

---

## API Integration

### OpenAIRE Graph V3 (PRIMARY)

```python
# research_ci/openaire.py

import httpx
from typing import Any

V3_BASE = "https://api.openaire.eu/graph/v3"

class OpenAIREClient:
    """OpenAIRE Graph V3 adapter."""

    def __init__(self, mailto: str | None = None):
        self.base = V3_BASE
        self.client = httpx.Client(timeout=30)
        self.mailto = mailto

    def search_products(
        self,
        search: str = "",
        filters: dict[str, str] | None = None,
        page_size: int = 100,
        include_stats: bool = True,
    ) -> dict[str, Any]:
        """Search research products via V3 API."""
        params = {"pageSize": page_size, "includeStats": str(include_stats).lower()}
        if search:
            params["search"] = search
        if filters:
            for k, v in filters.items():
                params[k] = v
        if self.mailto:
            params["mailto"] = self.mailto
        r = self.client.get(f"{V3_BASE}/research-products", params=params)
        r.raise_for_status()
        return r.json()

    def get_product(self, openaire_id: str) -> dict[str, Any]:
        """Fetch single research product by OpenAIRE ID."""
        r = self.client.get(f"{V3_BASE}/research-products/{openaire_id}")
        r.raise_for_status()
        return r.json()

    def search_projects(self, filters: dict[str, str]) -> dict[str, Any]:
        params = {"pageSize": 50}
        params.update(filters)
        r = self.client.get(f"{V3_BASE}/projects", params=params)
        r.raise_for_status()
        return r.json()

    def search_persons(self, filters: dict[str, str]) -> dict[str, Any]:
        params = {"pageSize": 50}
        params.update(filters)
        r = self.client.get(f"{V3_BASE}/persons", params=params)
        r.raise_for_status()
        return r.json()
```

### ScholeXplorer V3 (RELATIONS)

```python
# research_ci/scholexplorer.py

SCHOPEX_BASE = "https://api.scholexplorer.openaire.eu/v3"

class ScholeXplorerClient:
    """ScholeXplorer for typed scholarly relationships."""

    def get_relations(
        self, source_doi: str, target_doi: str | None = None
    ) -> list[dict]:
        """Get typed relations between entities."""
        params = {"source": source_doi}
        if target_doi:
            params["target"] = target_doi
        r = self.client.get(f"{SCHOPEX_BASE}/links", params=params)
        r.raise_for_status()
        return r.json().get("results", [])

    def get_outgoing(self, source_doi: str) -> list[dict]:
        """Get all outgoing relations from a source."""
        return self.get_relations(source_doi)
```

### OpenAIRE V4 (EXPERIMENTAL — optional)

```python
# research_ci/openaire_v4.py

V4_BASE = "https://api-beta.openaire.eu/graph/v4"

class OpenAIREV4Client:
    """V4 beta with unified filter syntax."""

    def search_products(
        self, search: str, filter: str, sort: str = "relevance:desc"
    ) -> dict[str, Any]:
        params = {"search": search, "filter": filter, "sort": sort}
        r = self.client.get(f"{V4_BASE}/research-products", params=params)
        r.raise_for_status()
        return r.json()
```

---

## Core data model

```python
# research_ci/tracked.py

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

@dataclass
class TrackedAnalysis:
    analysis_id: str
    title: str
    source_provider: str  # "openaire"
    source_api: str       # "v3"
    query: dict[str, Any] # {entity, search, filters}
    observed_at: datetime
    source_version: str
    result_ids: list[str]
    snapshot_digest: str  # sha512 of canonical state
    claims: list[str]     # claim IDs

@dataclass
class TrackedClaim:
    claim_id: str
    text: str
    dependencies: list[dict]  # [{kind, ref/predicate/target}]
    status: str  # CURRENT | SOURCE_CHANGED | RECOMPUTE | HUMAN_REVIEW

@dataclass
class Dependency:
    kind: str  # entity | relation | field
    ref: str | None = None
    source: str | None = None
    predicate: str | None = None
    target: str | None = None
```

---

## Semantic diff engine

```python
# research_ci/diff.py

from dataclasses import dataclass

MATERIALITY = {
    "cosmetic": ["display_name", "formatting"],
    "identity": ["orcid", "doi", "openaire_id"],
    "metadata": ["title", "abstract", "publication_date", "language"],
    "relation": ["relProject", "relOrganization", "relDataSource"],
    "availability": ["access_right", "oa_status", "embargo"],
    "version": ["isVersionOf", "hasVersion"],
    "correction": ["isCorrectedVersionOf"],
    "retraction": ["isRetractionOf"],
}

@dataclass
class SemanticDiff:
    added_entities: list[str]
    removed_entities: list[str]
    changed_fields: list[dict]  # [{id, field, old, new, materiality}]
    added_relations: list[dict]  # [{source, predicate, target}]
    removed_relations: list[dict]
    unchanged_count: int

def compute_diff(old_records: list[dict], new_records: list[dict]) -> SemanticDiff:
    """Compute semantic diff between two snapshots."""
    old_by_id = {r["id"]: r for r in old_records}
    new_by_id = {r["id"]: r for r in new_records}

    added = [r["id"] for r in new_records if r["id"] not in old_by_id]
    removed = [r["id"] for r in old_records if r["id"] not in new_by_id]

    changed_fields = []
    for rid in old_by_id:
        if rid not in new_by_id:
            continue
        old_r, new_r = old_by_id[rid], new_by_id[rid]
        for field in set(list(old_r.keys()) + list(new_r.keys())):
            if old_r.get(field) != new_r.get(field):
                mat = classify_materiality(field)
                changed_fields.append({
                    "id": rid, "field": field,
                    "old": old_r.get(field), "new": new_r.get(field),
                    "materiality": mat,
                })

    return SemanticDiff(
        added_entities=added,
        removed_entities=removed,
        changed_fields=changed_fields,
        added_relations=[],  # from ScholeXplorer
        removed_relations=[],
        unchanged_count=len(old_by_id) - len(removed),
    )

def classify_materiality(field: str) -> str:
    for mat, keywords in MATERIALITY.items():
        if any(kw in field.lower() for kw in keywords):
            return mat
    return "metadata"
```

---

## Impact engine

```python
# research_ci/impact.py

def compute_impact(
    diff: "SemanticDiff",
    claims: list["TrackedClaim"],
) -> dict[str, list[str]]:
    """Map diff changes to claim impacts."""
    result = {"unaffected": [], "source_changed": [], "recompute": [], "human_review": []}

    # Build change index
    changed_ids = set(diff.added_entities + diff.removed_entities)
    changed_fields = {c["id"] for c in diff.changed_fields}
    changed_relations = set()
    for r in diff.added_relations + diff.removed_relations:
        changed_relations.add((r.get("source"), r.get("predicate")))

    for claim in claims:
        affected = False
        for dep in claim.dependencies:
            if dep["kind"] == "entity" and dep.get("ref") in changed_ids:
                affected = True
                break
            if dep["kind"] == "relation":
                key = (dep.get("source"), dep.get("predicate"))
                if key in changed_relations:
                    affected = True
                    break
            if dep["kind"] == "field" and dep.get("ref") in changed_fields:
                affected = True
                break

        if affected:
            # Check materiality of the change
            mat = classify_impact_materiality(dep, diff)
            if mat == "high":
                result["recompute"].append(claim.claim_id)
            elif mat == "medium":
                result["source_changed"].append(claim.claim_id)
            else:
                result["unaffected"].append(claim.claim_id)
        else:
            result["unaffected"].append(claim.claim_id)

    return result
```

---

## CLI

```bash
# Track an analysis
patala track \
  --name "funding-landscape" \
  --query "type=project&fundingShortName=EC&fromStartYear=2020" \
  --claims claims.json

# Verify after graph change
patala verify funding-landscape

# Output:
# 83 tracked entities
# 70 unchanged, 6 added, 2 removed, 5 changed
# CLAIM-01: CURRENT
# CLAIM-02: RECOMPUTE
# CLAIM-03: CURRENT
# PROOF OBLIGATION PO-002: relation removed

# Register a claim
patala claim add \
  --analysis funding-landscape \
  --text "EC funds 42% of AI research" \
  --depends entity:openaire:xxx \
  --depends relation:openaire:yyy:isFundedBy

# Inspect history
patala log funding-landscape

# Compare two snapshots
patala diff --old snapshot1.json --new snapshot2.json
```

---

## What NOT to build

- ❌ LLMs in the core path (deterministic only)
- ❌ UI (CLI first, UI later)
- ❌ Sanskrit demo (one paragraph)
- ❌ Scholar Relay (future extension)
- ❌ Crux (stretch feature)
- ❌ Payment systems
- ❌ Any other hackathon idea

## What to build

```
1. openaire.py — V3 client (2 hours)
2. normalize.py — canonical record format (1 hour)
3. snapshot.py — content-addressed snapshots (2 hours)
4. tracked.py — TrackedAnalysis + TrackedClaim (1 hour)
5. diff.py — semantic diff with materiality (3 hours)
6. impact.py — dependency → impact mapping (3 hours)
7. obligations.py — proof obligation generator (1 hour)
8. ledger.py — append-only event store (1 hour)
9. cli.py — CLI entry point (2 hours)
10. tests + fixtures + README (4 hours)
```

Total: ~20 hours of focused work.

## From hackathon1 repo

Take:
- `explore_api.py` — adapt V3 client
- `search.py` — adapt V4 filter syntax (optional)
- Dossier scoring format — use for README

## From imbrokeasfuck repo

Take:
- Wiggly `events.py` — append-only event store pattern
- Wiggly `completeness.py` — CoverageDimension pattern
- `earn/prioritizer.py` — deadline awareness
- `oracle/bittensor_economics.py` — data model pattern

## Deadline
**Aug 20, 23:59 CEST** — ~24 hours from now.
