# Audit Report — Public Data Quality Auditor BR

**Date:** 2026-07-13  
**Branch:** `chore/portfolio-quality-pass`  
**Auditor role:** portfolio quality pass (architecture, QA, DX, security, UX, docs)

## Executive summary

O projeto já era um MVP sólido de data quality (FastAPI + Next.js, demos, metodologia, lab mode no Vercel). A revisão encontrou **bugs de portfólio bloqueantes** (mojibake nos snapshots da demo pública, parser CSV com `;` frágil, mensagem de score contraditória com issues críticas, token OIDC local, CORS permissivo) e lacunas de DX (venv quebrado, sem CI, docs desatualizadas sobre lab vs API).

**Nota antes:** ~6.5/10  
**Nota alvo após este pass:** ~8.0/10 (demo pública legível + testes de regressão + CI + docs honestas)

## Main risks (found)

| Risk | Severity | Status |
|------|----------|--------|
| Mojibake nos JSON de lab (`Munic├¡pios`) | Critical | Fixed via `scripts/refresh_lab_snapshots.py` |
| CSV `;` aceito como 1 coluna | Critical | Fixed — best-of parse by column count |
| `VERCEL_OIDC_TOKEN` em `.env.local` | High | Scrubbed; see `SECURITY_NOTES.md` |
| Score card “boa” com issue critical | High | Fixed — severity-aware copy |
| CORS `*` + credentials | High | Fixed — explicit origins |
| CTA “Enviar CSV” no lab | Medium | Fixed |
| Sem CI | Medium | Added `.github/workflows/ci.yml` |
| `.env.example` vs config real | Medium | Aligned |

## Quick wins completed

- Regenerar snapshots UTF-8
- Parser multi-separador
- QualityScoreCard alinhado à recomendação executiva
- Lab CTAs / âncora de limitações
- Testes de regressão (`;`, tabs, UTF-8)
- CI api + web
- Remoção de `lucide-react` não usado
- Config lê `MAX_UPLOAD_MB` / `MAX_ROWS` / `CORS_ORIGINS`

## Structural improvements (done / deferred)

**Done:** scripts de refresh, CI, SECURITY_NOTES, docs de arquitetura/deploy/testes/decisões, HANDOFF.

**Deferred:** SQLite history, Playwright e2e, CNPJ check digits, deploy FastAPI no Vercel, screenshots reais da UI.

## Bugs found & fixed

1. Encoding dos snapshots lab  
2. Heurística CSV `,` early-return  
3. Score UI vs critical issues  
4. Home CTA falsa no lab  
5. Nav Limitações sem âncora  
6. CORS inseguro  
7. Import morto `is_nullish`  
8. Top issues não ordenados por severidade  
9. Port/API token no `.env.local`

## Execution plan

1. Diagnóstico + branch  
2. Correções críticas + testes  
3. Docs + CI + README/HANDOFF  
4. Commit + push da branch

## Final checklist

- [x] Branch `chore/portfolio-quality-pass`
- [x] Pytest passando (incl. regressões)
- [x] Typecheck web
- [x] CI workflow
- [x] Secrets scrubbed
- [x] Docs de auditoria/arquitetura/handoff
- [ ] Redeploy Vercel com snapshots limpos (após merge/push)
- [ ] Screenshots reais (opcional)
