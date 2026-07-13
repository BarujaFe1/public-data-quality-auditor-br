# Security notes

## Finding (2026-07-13)

- A **Vercel OIDC token** was present in the local (gitignored) file `apps/web/.env.local`, likely written by `vercel link`.
- The file is covered by `.gitignore` and was **not** committed to git.
- The token was **removed** from the local file during the portfolio quality pass.
- Action for the maintainer: if the token was ever shared outside the machine, rotate/revoke via Vercel project settings. Do not paste the token into issues, docs, or chat.

## Hardening applied in this pass

- CORS no longer uses `allow_origins=["*"]` with `allow_credentials=True`.
- `.env.local.example` documents only non-secret config.
- Lab demo does not require exposing the FastAPI surface publicly.

## Residual risks

- Local FastAPI upload endpoint remains unauthenticated by design (MVP / local stack).
- `data/audit_outputs/` may contain user-uploaded CSV content on disk — keep it local and gitignored.
