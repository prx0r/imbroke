# OpenAIRE Graph API — Technical Reference

**Version:** 11.3.0
**Base URL:** `https://api.openaire.eu/graph/v3`
**Total entities:** 380M+ research products
**Source:** https://graph.openaire.eu/docs/

---

## Endpoints

| Entity | Endpoint | Description |
|--------|----------|-------------|
| Research Products | `/v3/research-products` | Publications, datasets, software |
| Organizations | `/v3/organizations` | Institutions, funders |
| Data Sources | `/v3/datasources` | Journals, repositories |
| Projects | `/v3/projects` | Funded research projects |
| Persons | `/v3/persons` | Researchers, authors |

---

## Research Products API

### Quick examples

```
# Search AI papers
/v3/research-products?search=artificial+intelligence&type=publication&pageSize=5

# Peer-reviewed open access
/v3/research-products?type=publication&isPeerReviewed=true&accessRightLabel="Open Access"

# Datasets from 2025
/v3/research-products?type=dataset&publicationYear=2025

# Citations sorted
/v3/research-products?search=climate&sortBy=citationCount DESC

# With statistics
/v3/research-products?search=covid&includeStats=true

# Single entity
/v3/research-products/{openaire_id}
```

### Key filters

| Category | Parameters |
|----------|-----------|
| **Identity** | `search`, `mainTitle`, `description`, `id`, `pid`, `originalId` |
| **Classification** | `type` (publication/dataset/software/other), `subjects`, `fos`, `sdgLabel` |
| **Dates** | `publicationYear`, `fromPublicationDate`, `toPublicationDate` |
| **Authors** | `authorFullName`, `authorId`, `rorId` |
| **Access** | `accessRightLabel`, `isPeerReviewed`, `isPubliclyFunded`, `hasLicense` |
| **Impact** | `influenceClass`, `popularityClass`, `citationCountClass` (C1-C5) |
| **Relations** | `relProjectId`, `relProjectCode`, `relOrganizationId`, `relHostingDataSourceId` |

### Response format

```json
{
  "header": {
    "numFound": 380394070,
    "maxScore": 1.0,
    "queryTime": 2441,
    "page": 1,
    "pageSize": 10,
    "nextCursor": "..."
  },
  "results": [...]
}
```

### Statistics (includeStats=true)

```json
{
  "header": {
    "totalCitationsCount": 13107275,
    "countsByType": {
      "publication": 1544760,
      "dataset": 55356,
      "software": 3812,
      "other": 83686
    }
  }
}
```

### Logical operators

```
AND: type=("publication" OR "dataset")
OR:  search="climate" OR "weather"
NOT: search="semantic" NOT "web"
```

### Cursor paging (for >10K results)

```
/v3/research-products?type=publication&pageSize=100&cursor=*
→ returns nextCursor
→ use nextCursor for next page
```

---

## Other APIs

### ScholeXplorer

Publication ↔ dataset ↔ software links:
```
GET /v3/scholexplorer?source={doi}&target={doi}
```

### Organizations

```
/v3/organizations?countryCode=GR
/v3/organizations?rorId=https://ror.org/05a28rw58
```

### Projects

```
/v3/projects?fundingShortName=EC&fromStartYear=2025
/v3/projects?projectId=101086775
```

### Persons

```
/v3/persons?givenName=Paolo&lastName=Manghi
/v3/persons?orcid=0000-0002-...
```

---

## V4 Beta (unified filters)

```
https://api-beta.openaire.eu/graph/v4/research-products
```

Same API but with unified `filter=` parameter:
```
/v4/research-products?search=climate&filter=type:publication,is_peer_reviewed:true&sort=citation_count:desc
```

---

## Python quickstart

```python
import requests

# Search AI papers
r = requests.get("https://api.openaire.eu/graph/v3/research-products", params={
    "search": "artificial intelligence",
    "type": "publication",
    "pageSize": 10,
    "includeStats": True,
})
data = r.json()
print(f"Found: {data['header']['numFound']:,}")
for p in data['results']:
    print(f"  {p.get('mainTitle', '')[:60]}")
```

---

## Key data model fields

A Research Product object contains:

```json
{
  "id": "doi_dedup___::...",
  "mainTitle": "...",
  "type": "publication",
  "doi": "...",
  "publicationYear": 2025,
  "citationCount": 42,
  "accessRightLabel": "Open Access",
  "isPeerReviewed": true,
  "isPubliclyFunded": false,
  "subjects": [...],
  "relProjects": [...],
  "relOrganizations": [...],
  "relDataSources": [...]
}
```

---

## Rate limits

- Public: generous (no auth needed for basic queries)
- Authenticated: higher rate limits
- Mailto parameter: polite pool access

---

## What we can build

With this API, ProofGraph can:

1. **Query research products** by type, year, access, peer review, funding
2. **Follow relations** to projects, organizations, data sources
3. **Get statistics** on citation counts, type breakdowns
4. **Detect gaps** — publications without datasets/software/PIDs
5. **Cross-reference** with Crossref, DataCite, OpenAlex
6. **Generate EvidenceReceipts** for any entity
