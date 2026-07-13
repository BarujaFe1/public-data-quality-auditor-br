# PORTFOLIO_HANDOFF — Public Data Quality Auditor BR

**Branch:** `feat/portfolio-tier-a`  
**Date:** 2026-07-13  
**Author project:** Felipe Alírio Baruja  
**Recommendation:** **selecionado** (quase destaque) — lab/MVP honesto com demo viva, motor testado e narrativa de entrevista clara.

---

## Resumo

Peça de portfólio de **auditoria explicável de CSVs públicos brasileiros**: profiling → checks → score dimensional → issues → dicionário → datapackage. A demo pública roda em modo **lab** (snapshots embutidos no Next.js); a API FastAPI/Pandas é a fonte de verdade do motor e roda localmente.

## Before / After

| Área | Antes | Depois |
|------|--------|--------|
| Demo Vercel | Build antigo (`Enviar CSV`, snapshots com mojibake) em conta/time inacessível à CLI atual | Demo atualizada em https://public-data-quality-auditor-br-nu.vercel.app (UTF-8, lab CTAs, IBGE) |
| Datasets | 3 sintéticos | + amostra pública IBGE com `docs/PROVENANCE.md` |
| Metodologia | docs estáticos | `scripts/generate_methodology_report.py` → `docs/reports/methodology_run.md` |
| Testes | pytest + tsc | + regressão IBGE + Playwright E2E caminho crítico |
| Claims | URL canônica apontava build stale | README/handoff documentam URL viva vs legado |

## Comandos

```bash
# Snapshots lab (UTF-8)
apps/api/.venv/Scripts/python scripts/refresh_lab_snapshots.py

# Relatório metodológico
apps/api/.venv/Scripts/python scripts/generate_methodology_report.py

# API tests
cd apps/api && .venv/Scripts/python -m pytest tests -q

# Web
cd apps/web && npx tsc --noEmit && npm run build
npm run test:e2e   # após build; sobe next start

# Deploy (conta Vercel acessível: team baruja-fe)
cd apps/web && vercel deploy --prod --yes --scope baruja-fe
```

## Gates (baseline nesta entrega)

- pytest: **23 passed**
- `tsc --noEmit`: OK
- `next build` (lab): OK
- E2E Playwright: adicionado (rodar localmente/`CI`)
- Live verified: score **87.4**, UTF-8 “Municípios” / “São Paulo”, 1 critical · 4 high

## Limitações remanescentes

1. URL legada `https://public-data-quality-auditor-br.vercel.app` ainda serve build **pré-quality-pass** (projeto em team `barujafe1s-projects` sem auth na CLI atual). Preferir a URL `-nu` até migrar o domínio.
2. Demo pública **não** executa FastAPI no Vercel (intencional).
3. Screenshot `04-data-dictionary` ainda pode ser o JPG mockup; PNGs 01–03 são capturas reais 2026-07-13.
4. Upload sem auth no modo full-stack local (MVP).
5. Amostra IBGE ≠ dump completo.

## Próximos passos

1. Transferir domínio `public-data-quality-auditor-br.vercel.app` para o projeto `baruja-fe` **ou** fazer login na conta que o possui e redeployar.
2. Completar PNG do dicionário + social preview atualizado.
3. Validadores BR mais fortes (CNPJ dígitos verificadores).
4. Histórico SQLite / score delta (roadmap).

## Arquivos-chave desta entrega

- `data/public/ibge_municipios_amostra.csv`, `docs/PROVENANCE.md`
- `docs/reports/methodology_run.md`
- `apps/web/src/lib/snapshots/ibge_municipios.json`
- `apps/web/e2e/critical-path.spec.ts`
- `docs/PORTFOLIO_HANDOFF.md`, `CHANGELOG.md`, `docs/DEMO_SCRIPT.md`
- `assets/screenshots/01-audit-summary.png`, `02-issues-register.png`, `03-column-profile.png`
