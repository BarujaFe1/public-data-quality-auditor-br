# Testing

## API (pytest)

```bash
cd apps/api
python -m venv .venv
# Windows:
.venv\Scripts\activate
pip install -r requirements.txt
pytest tests -q
```

Coverage includes:

- core checks (nulls, empty column, duplicates, IDs, dates, numbers, categories)
- completeness / overall scoring
- dictionary, report, datapackage
- API demo + upload flow
- regressions: semicolon/tab CSV, UTF-8 demo names, executive recommendation with critical issues

## Web

```bash
cd apps/web
npm install
npm run typecheck
npm run build
```

Lab mode build: leave `NEXT_PUBLIC_USE_API` unset.

## CI

GitHub Actions (`.github/workflows/ci.yml`): pytest on Python 3.12 + `tsc` + `next build`.

## Refresh lab fixtures after engine changes

```bash
apps/api/.venv/Scripts/python scripts/refresh_lab_snapshots.py
```

Commit updated `apps/web/src/lib/snapshots/*.json` when scores/issues intentionally change.
