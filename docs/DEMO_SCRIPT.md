# Demo guiada (3–5 minutos)

**URL:** https://public-data-quality-auditor-br-nu.vercel.app

## Roteiro

1. **Hook (20s)** — “Dados públicos brasileiros frequentemente chegam sujos. Antes de analisar, preciso de um diagnóstico explicável — não um selo de certificação.”
2. **Home (30s)** — Mostrar lab banner, CTA **Rodar demo** + **Ver limitações**. Enfatizar: upload live exige stack local.
3. **Catálogo (40s)** — Três demos sintéticos intencionalmente sujos + **IBGE amostra pública** com proveniência documentada.
4. **Municípios → Resumo (90s)** — Score **87.4/100** com **1 critical / 4 high**. Destacar que o card não diz “tudo ótimo”: ID duplicado crítico aparece junto do score alto.
5. **Issues (60s)** — Filtrar severidade; abrir amostra de linhas; citar UF inválida, população negativa, “Sao Paulo” vs “São Paulo”.
6. **Colunas / Dicionário / Export (40s)** — Profiling + dicionário sugerido + datapackage/Markdown.
7. **Fecho (30s)** — Metodologia reproduzível (`docs/reports/methodology_run.md`); testes pytest + E2E; lab vs full-stack como trade-off de portfólio.

## Frases permitidas
- “diagnóstico explicável”
- “lab / portfolio demo com snapshots do mesmo motor”
- “amostra pública com proveniência”

## Frases a evitar
- “enterprise / produção / IA / certificação de qualidade”
- “processamos todo o IBGE”
- “demo Vercel roda FastAPI”
