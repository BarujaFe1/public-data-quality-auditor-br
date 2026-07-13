# Deployment

## Public lab demo (Vercel)

- **URL:** https://public-data-quality-auditor-br.vercel.app
- **Root Directory:** `apps/web`
- **Config:** `apps/web/vercel.json`
- **Mode:** lab snapshots (`NEXT_PUBLIC_USE_API` unset)
- No FastAPI on Vercel for the portfolio demo

After changing snapshots or UI:

```bash
cd apps/web
vercel deploy --prod --yes --scope barujafe1s-projects
```

Or push to `main` if the GitHub integration is linked.

## Local full stack

```bash
# API
cd apps/api
.venv\Scripts\uvicorn app.main:app --reload --port 8000

# Web
cd apps/web
# .env.local:
# NEXT_PUBLIC_USE_API=true
# NEXT_PUBLIC_API_URL=http://localhost:8000
npm run dev
```

## Docker

```bash
docker compose up --build
```

Note: Next.js bakes `NEXT_PUBLIC_*` at **build** time. The compose file documents lab vs full-stack; rebuild the web image when flipping `USE_API`.

## Environment

See root `.env.example` and `apps/web/.env.local.example`.
