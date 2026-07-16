<div align="center">
  <img src="./assets/icon.png" alt="Public Data Quality Auditor BR Logo" width="120" height="120" />

  <h1>Public Data Quality Auditor BR</h1>

  <p><strong>Auditoria explicável de qualidade para CSVs de dados públicos brasileiros.</strong></p>
  <p><strong>Explainable data-quality auditing for Brazilian public CSV datasets.</strong></p>

  <p>
    <a href="#pt-br">PT-BR</a> ·
    <a href="#english">English</a> ·
    <a href="#live-demo">Live Demo</a> ·
    <a href="#stack">Stack</a> ·
    <a href="#architecture">Architecture</a> ·
    <a href="#quick-start">Quick Start</a> ·
    <a href="#author">Author</a>
  </p>

  <p>
    <img alt="Next.js" src="https://img.shields.io/badge/Next.js-15-000000?style=for-the-badge&logo=nextdotjs" />
    <img alt="TypeScript" src="https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white" />
    <img alt="FastAPI" src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" />
    <img alt="Pandas" src="https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white" />
    <img alt="Status" src="https://img.shields.io/badge/Status-Lab%20demo-22C55E?style=for-the-badge" />
    <img alt="License" src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" />
  </p>

  <p>
    <a href="https://public-data-quality-auditor-br.vercel.app"><strong>Live Demo</strong></a> ·
    <a href="https://github.com/BarujaFe1/public-data-quality-auditor-br"><strong>Repo</strong></a> ·
    <a href="https://barujafe.vercel.app/"><strong>Portfolio</strong></a> ·
    <a href="https://www.linkedin.com/in/barujafe/"><strong>LinkedIn</strong></a>
  </p>
</div>

<p align="center">
  <img src="./assets/hero-cover.jpg" alt="Public Data Quality Auditor BR overview" width="100%" />
</p>

> **Lab / demo notice:** the public Vercel demo runs **precomputed snapshots** (municípios / escolas / contratos). It is a diagnostic lab — **not** a certification authority, crawler farm or production open-data platform. CSV upload needs the local FastAPI stack.

---

## PT-BR

### Visão geral
Ferramenta que audita CSVs de dados públicos: profiling, checks, score dimensional 0–100 explicável, issues com amostra, dicionário sugerido e export de relatório + `datapackage.json`.

### Problema
Dados abertos sustentam jornalismo e políticas, mas chegam com nulos, duplicidades, formatos quebrados e metadados fracos — e análises seguem sem diagnóstico prévio.

### Para quem
Jornalistas de dados, pesquisadores, analistas cívicos e profissionais de data quality interessados em bases brasileiras.

### Funcionalidades
- Demos sintético-realistas: municípios, escolas, contratos
- Checks de completude, unicidade, validade, consistência e documentabilidade
- Score geral + por dimensão, issues com severidade e recomendação
- Perfil por coluna e dicionário de dados
- Export Markdown/HTML e datapackage
- API FastAPI testada (`pytest`) + UI Next.js

### Escopo e limites (honestos)
- Score é **diagnóstico heurístico**, não certificação factual/legal
- Pode haver falsos positivos; CNPJ validado principalmente por formato no MVP
- Limites de tamanho no MVP
- Demo pública **sem** FastAPI hospedado (snapshots); upload CSV = stack local

---

## English

### Overview
A tool that audits public-data CSVs: profiling, checks, explainable dimensional 0–100 score, issues with samples, suggested dictionary and report + `datapackage.json` export.

### Problem
Open data fuels journalism and policy, but arrives with nulls, duplicates, broken formats and weak metadata — while analysis often skips a prior diagnosis.

### Who it is for
Data journalists, researchers, civic analysts and data-quality practitioners working with Brazilian datasets.

### Features
- Synthetic-realistic demos: municipalities, schools, contracts
- Completeness, uniqueness, validity, consistency and documentability checks
- Overall + dimensional scores, severity-ranked issues with recommendations
- Column profiling and data dictionary
- Markdown/HTML report and datapackage export
- Tested FastAPI API (`pytest`) + Next.js UI

### Scope and honest limits
- Score is a **heuristic diagnosis**, not factual/legal certification
- False positives possible; CNPJ checks are mostly format-based in the MVP
- Size limits in the MVP
- Public demo has **no** hosted FastAPI (snapshots); CSV upload needs local stack

---

## Live Demo

| Surface | URL |
|---|---|
| **Public lab (snapshots)** | [https://public-data-quality-auditor-br.vercel.app](https://public-data-quality-auditor-br.vercel.app) |
| **GitHub** | [https://github.com/BarujaFe1/public-data-quality-auditor-br](https://github.com/BarujaFe1/public-data-quality-auditor-br) |

**How to try:** open the lab → pick a demo dataset → inspect score + issues → open column profile / dictionary. For CSV upload, run the full local stack below.

---

## Screenshots

<table>
  <tr>
    <td width="50%"><img src="./assets/screenshots/01-audit-summary.jpg" alt="Summary" /><br /><sub><strong>Audit summary</strong></sub></td>
    <td width="50%"><img src="./assets/screenshots/02-issues-register.jpg" alt="Issues" /><br /><sub><strong>Issues register</strong></sub></td>
  </tr>
  <tr>
    <td width="50%"><img src="./assets/screenshots/03-column-profile.jpg" alt="Profile" /><br /><sub><strong>Column profile</strong></sub></td>
    <td width="50%"><img src="./assets/screenshots/04-data-dictionary.jpg" alt="Dictionary" /><br /><sub><strong>Data dictionary</strong></sub></td>
  </tr>
</table>

---

## Stack

| Layer | Technology |
|---|---|
| Web | Next.js 15, React 19, TypeScript, Tailwind, Recharts |
| API | FastAPI, Pandas, NumPy, Pydantic, pytest |
| Ops | Docker Compose |

---

## Architecture

```txt
apps/
  api/app/
    quality/     checks, profiling, scoring, engine
    reports/     Markdown/HTML + datapackage
    services/
  web/           Next.js UI (snapshot mode or API mode)
data/            demo CSVs
assets/          icon, hero, screenshots
```

Flow: CSV/demo → profiling → checks → dimensional score → issues → dictionary → report/datapackage.

---

## Quick Start

**Prerequisites:** Node.js 20+, Python 3.12+, Git.

### Lab frontend only (same mode as public demo)
```bash
cd apps/web
npm install
npm run dev
```
Leave `NEXT_PUBLIC_USE_API` unset. UI: [http://localhost:3000](http://localhost:3000)

### Full stack (API + upload)
```bash
# API
cd apps/api
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# Web
cd apps/web
copy .env.local.example .env.local
# NEXT_PUBLIC_USE_API=true
# NEXT_PUBLIC_API_URL=http://localhost:8000
npm install
npm run dev
```

### Docker (optional)
```bash
docker compose up --build
```

---

## Technical decisions

- **Explainable dimensional scoring** so quality is discussable, not a black box
- **Snapshot mode on Vercel** for a reliable one-click demo without hosting Pandas
- **Datapackage export** as a reusable handoff artifact
- **Methodological honesty:** diagnosis ≠ certification

---

## Roadmap

- Audit history / persistence
- Score diff across dataset versions
- Stronger BR validators (CNPJ/CPF, IBGE codes)
- CLI (`pdqa audit file.csv`)
- Light auth for team deploys

---

## Author

**Felipe Alirio Baruja** — data / product / full-stack portfolio.

- Portfolio: [https://barujafe.vercel.app/](https://barujafe.vercel.app/)
- GitHub: [https://github.com/BarujaFe1](https://github.com/BarujaFe1)
- LinkedIn: [https://www.linkedin.com/in/barujafe/](https://www.linkedin.com/in/barujafe/)

---

## License

MIT — see [`LICENSE`](./LICENSE).
