# Changelog — portfolio tier A

## 2026-07-13 — feat/portfolio-tier-a

### Added
- Amostra pública IBGE (`data/public/ibge_municipios_amostra.csv`) + `docs/PROVENANCE.md`
- Snapshot lab `ibge_municipios.json` e card no catálogo (kind `public_sample`)
- Relatório metodológico reproduzível: `scripts/generate_methodology_report.py` → `docs/reports/methodology_run.md`
- Playwright E2E do caminho crítico (`apps/web/e2e/critical-path.spec.ts`)
- `docs/PORTFOLIO_HANDOFF.md`, `docs/DEMO_SCRIPT.md`, roteiro de screenshots
- Screenshots reais (PNG) do resumo e issues na demo viva

### Fixed / improved
- Resolução de demos em `data/public/` via `_demo_path`
- Banner lab menciona amostra IBGE
- CI: job E2E após build
- Redeploy da demo em team Vercel acessível (`baruja-fe`)

### Deploy note
- **Canônica atual:** https://public-data-quality-auditor-br-nu.vercel.app  
- **Legado (stale):** https://public-data-quality-auditor-br.vercel.app (conta/time antiga)
