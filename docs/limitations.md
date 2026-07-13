# Limitações

- Score é **diagnóstico**, não certificação de verdade factual.
- Checks são heurísticos (falsos positivos/negativos possíveis).
- CNPJ: validação de formato (14 dígitos), não algoritmo completo.
- Limites do MVP: 5 MB e 50 mil linhas (configuráveis via env).
- Sem autenticação na API local (uso local / lab).
- **Demo pública (Vercel):** snapshots pré-computados; upload CSV desabilitado. Full stack requer `NEXT_PUBLIC_USE_API=true` + FastAPI local.
- Frontend lab não depende da API; modo full-stack depende de `NEXT_PUBLIC_API_URL`.
- Datasets demo são sintéticos e intencionalmente “sujos”.
