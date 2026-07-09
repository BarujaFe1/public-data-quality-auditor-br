# Public Data Quality Auditor BR

Auditoria de qualidade para bases públicas brasileiras em CSV — profiling, validações, score explicável, registro de problemas, dicionário de dados, relatório executivo e `datapackage.json`.

## Problema

Dados abertos são úteis, mas frequentemente chegam com nulos, duplicidades, datas inválidas, categorias inconsistentes e metadados fracos. Usar essas bases sem diagnóstico coloca análises, reportagens e políticas em risco.

## Solução

Uma aplicação local (API FastAPI + frontend Next.js) que:

1. carrega datasets demo ou CSV enviado pelo usuário;
2. detecta schema/tipos;
3. executa checks de qualidade;
4. calcula score geral e por dimensão;
5. lista issues com amostras e recomendações;
6. gera dicionário, relatório Markdown/HTML e descriptor Frictionless-simples.

## Stack

| Camada | Tecnologia |
|--------|------------|
| API | Python 3.12, FastAPI, Pandas, Pydantic, pytest |
| Web | Next.js (App Router), TypeScript, Tailwind, Recharts |
| Dados | CSV demo locais (sem dependência de rede) |
| Ops | docker-compose (opcional) |

## Como rodar (local)

### 1. API

```powershell
cd apps/api
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
# Se a porta 8000 estiver ocupada:
# uvicorn app.main:app --reload --port 8001
```

Health: http://localhost:8000/health (ou a porta escolhida)  
OpenAPI: http://localhost:8000/docs

> Se usar outra porta, ajuste `NEXT_PUBLIC_API_URL` em `apps/web/.env.local`.

### 2. Web

```powershell
cd apps/web
copy .env.local.example .env.local   # se existir; senão NEXT_PUBLIC_API_URL=http://localhost:8000
npm install
npm run dev
```

UI: http://localhost:3000

### Docker (opcional)

```powershell
docker compose up --build
```

> No Windows, se o disco estiver cheio, prefira o modo local (venv + npm) e limpe caches antes.

## Como testar

```powershell
cd apps/api
.\.venv\Scripts\Activate.ps1
pytest tests -q
```

## Como usar a demo

1. Abra http://localhost:3000/audit
2. Escolha **Municípios**, **Escolas** ou **Contratos**
3. Veja score, dimensões, issues, colunas e dicionário
4. Exporte o relatório Markdown ou abra o `datapackage.json`

Via API:

```powershell
curl -X POST http://localhost:8000/audit/demo/municipios
```

## Como auditar um CSV próprio

- UI: `/audit` → upload `.csv` (até 5 MB / 50 mil linhas)
- API: `POST /audit/upload` (multipart `file`)

Encoding UTF-8/Latin-1; separadores `,`, `;` ou tab.

## Dimensões de qualidade

| Dimensão | Peso | Foco |
|----------|------|------|
| Completude | 25 | nulos, colunas/linhas vazias |
| Unicidade | 20 | duplicatas e IDs repetidos |
| Validade | 25 | datas, números, UF, CNPJ, faixas |
| Consistência | 20 | caixa/acento, tipos mistos, ordem de datas |
| Documentabilidade | 10 | nomes de colunas e dicionário |

Detalhes: [docs/quality-dimensions.md](docs/quality-dimensions.md) · [docs/methodology.md](docs/methodology.md)

## Screenshots (placeholders)

- `docs/screenshots/home.png` — home com tese e CTAs
- `docs/screenshots/summary.png` — score geral + dimensões
- `docs/screenshots/issues.png` — issues register filtrável

## Limitações

- Score é **diagnóstico**, não certificação.
- Não valida verdade factual nem licença legal.
- Checks são heurísticos (falsos positivos/negativos possíveis).
- MVP sem autenticação, crawler ou correção automática irreversível.
- Fontes públicas reais são opcionais; demos locais bastam.

## Trocar demos por fontes públicas reais

1. Baixe um CSV de fonte aberta (ver [docs/public-data-sources.md](docs/public-data-sources.md))
2. Coloque em `data/demo/` ou faça upload pela UI
3. Ajuste nomes de colunas se necessário
4. Reexecute a auditoria e compare scores

## Próximos passos

- Persistência SQLite de histórico de auditorias
- Comparação de versões (score delta)
- Mais validadores BR (CPF/CNPJ completo, IBGE)
- Export PDF e integração com Great Expectations / Pandera
- Deploy containerizado com volume para outputs

## Estrutura

```txt
public-data-quality-auditor-br/
  apps/api/          # FastAPI + motor de qualidade
  apps/web/          # Next.js
  data/demo/         # CSVs sintético-realistas
  data/audit_outputs/
  docs/
  HANDOFF_PORTFOLIO.md
```

## Licença

Projeto de portfólio / demonstração educacional. Datasets demo são sintéticos.
