# Handoff — portfolio quality pass

**Branch:** `chore/portfolio-quality-pass`  
**Date:** 2026-07-13

## What was found

- Lab snapshots on Vercel had **mojibake** (broken Portuguese accents).
- CSV parser preferred `,` and could accept **1-column** parses for `;` files.
- Score card could say “boa exploração” while critical issues existed.
- Local `.env.local` contained a **Vercel OIDC token** (gitignored) and wrong port.
- CORS used `*` with credentials; no CI; docs still implied UI always needs API.

## What was fixed / improved

- Regenerated UTF-8 snapshots + `scripts/refresh_lab_snapshots.py`
- Best-of delimiter detection (`;`, `,`, tab)
- Severity-aware `QualityScoreCard` + sorted top issues
- Lab-aware home CTAs; methodology `#limitations` anchor
- CORS allowlist; config env vars; scrubbed local token (`SECURITY_NOTES.md`)
- Regression tests; GitHub Actions CI; architecture/deploy/testing docs
- Removed unused `lucide-react`

## Commands run

```bash
git checkout -b chore/portfolio-quality-pass
python -m venv apps/api/.venv && pip install -r apps/api/requirements.txt
python scripts/refresh_lab_snapshots.py
cd apps/api && pytest tests -q   # 22 passed
cd apps/web && npx tsc --noEmit  # OK
```

## Tests

- API: 22 pytest cases (quality + API + regressions)
- Web: TypeScript `tsc --noEmit`

## Still missing / residual risks

- Redeploy Vercel so production serves new snapshots (do after merge or from this branch)
- Real UI screenshots (README still has generated mockups)
- Playwright e2e not added
- FastAPI not on Vercel (intentional)
- Unauthenticated local upload remains (local MVP)

## Portfolio suggestions

- Lead with live demo + “diagnóstico ≠ certificação”
- Show municípios 87.4 with **critical duplicate ID** — honesty of scoring
- Mention lab vs full-stack as an intentional deploy trade-off

## Suggested commit message

```txt
chore: improve portfolio quality, docs, tests and stability
```

## Next steps

1. Push branch / open PR
2. Redeploy Vercel from updated `apps/web`
3. Optionally commit portfolio `site.ts` Abrir demo (already done earlier) if not pushed
