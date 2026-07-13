# Architecture

## Overview

Monorepo with two apps:

| App | Role |
|-----|------|
| `apps/api` | FastAPI quality engine (Pandas profiling, checks, scoring, reports) |
| `apps/web` | Next.js UI — lab snapshots by default, optional live API |

```txt
CSV / Demo
  → parse (encoding + delimiter)
  → profile + rule checks
  → dimensional score
  → issues + dictionary + markdown + datapackage
  → UI (lab snapshot OR live API)
```

## Lab vs full stack

| Mode | How | Upload | Where |
|------|-----|--------|-------|
| **Lab** (default) | `NEXT_PUBLIC_USE_API` unset; JSON under `apps/web/src/lib/snapshots/` | Disabled | Vercel + local web-only |
| **Full stack** | `NEXT_PUBLIC_USE_API=true` + API on `:8000` | Enabled | Local / Docker |

Refresh lab snapshots:

```bash
apps/api/.venv/Scripts/python scripts/refresh_lab_snapshots.py
```

## API surface

- `GET /health`
- `GET /demos`
- `POST /audit/demo/{name}`
- `POST /audit/upload`
- `GET /audit/{id}` (+ summary, columns, issues, data-dictionary, report, datapackage.json)

## Quality domain (`apps/api/app/quality`)

- `profiling.py` — types, parse helpers
- `checks.py` — testable issue detectors
- `scoring.py` — penalties + executive recommendation
- `engine.py` — orchestration

## Persistence

MVP: in-memory store + JSON files in `data/audit_outputs/` (gitignored contents). Not multi-tenant.

## Frontend

App Router pages: `/`, `/audit`, `/audit/[id]`, `/methodology`.  
Client API facade: `src/lib/api.ts` switches lab vs HTTP.
