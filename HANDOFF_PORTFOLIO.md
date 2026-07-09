# HANDOFF — Public Data Quality Auditor BR

## Título curto

Public Data Quality Auditor BR

## Descrição curta

Ferramenta local para auditar qualidade de CSVs de dados públicos brasileiros: profiling, checks, score por dimensão, issues e relatório exportável.

## Descrição média

Aplicação full-stack (FastAPI + Next.js) que recebe CSV demo ou upload, infere schema, aplica validações de completude/unicidade/validade/consistência/documentabilidade, calcula score 0–100 explicável, gera dicionário de dados, relatório Markdown/HTML e `datapackage.json`. Feita para portfólio de data quality com utilidade cívica.

## Descrição longa

Dados abertos sustentam jornalismo, pesquisa e políticas públicas, mas muitas bases chegam com nulos, duplicidades, formatos quebrados e metadados fracos. O Public Data Quality Auditor BR transforma essa dor em um produto auditável: o usuário escolhe um dataset demo sintético-realista (municípios, escolas, contratos) ou envia um CSV; a API executa profiling e checks testáveis; a interface mostra score geral, scores por dimensão, issues com amostra de linhas e recomendações, perfil por coluna e dicionário sugerido. O projeto enfatiza responsabilidade metodológica — o score é diagnóstico, não certificação — e entrega documentação completa para apresentação em entrevistas e portfólio.

## Bullets de impacto

- Reduz risco de análises sobre bases públicas sem diagnóstico prévio.
- Torna problemas de qualidade **explicáveis** (dimensão, severidade, amostra, recomendação).
- Entrega artefatos reutilizáveis: relatório executivo + datapackage.
- Demonstra pipeline Python de data quality com API e UI analítica.
- Funciona offline com demos locais (sem depender de crawlers).

## Stack

Python 3.12, FastAPI, Pandas, Pydantic, pytest, Next.js, TypeScript, Tailwind, Recharts.

## Competências provadas

- Data quality engineering (regras, scoring, issues register)
- Analytics engineering / profiling
- API design (OpenAPI, schemas Pydantic)
- Frontend analítico
- Documentação metodológica e handoff de portfólio
- Testes automatizados de checks e endpoints

## Como apresentar em entrevista

1. **Problema:** “Dados públicos sujos quebram análises silenciosamente.”
2. **Demo ao vivo:** rodar `municipios` e mostrar score + issue de UF inválida / ID duplicado.
3. **Método:** explicar pesos das dimensões e por que não é certificação.
4. **Engenharia:** apontar checks testáveis e geração de datapackage.
5. **Próximo passo:** histórico SQLite, validadores BR mais fortes, comparação de versões.

## Limitações honestas

- Heurístico; pode haver falsos positivos.
- Não valida verdade factual nem licença.
- Limites de tamanho no MVP.
- CNPJ só por formato.
- UI depende da API local.

## Próximos passos

- Persistência e histórico de auditorias
- Diff de scores entre versões do mesmo dataset
- Validação completa de CNPJ/CPF e códigos IBGE
- Pacote CLI (`pdqa audit arquivo.csv`)
- Deploy com autenticação leve para times

## Post de LinkedIn

Auditar dados públicos antes de analisar deveria ser o padrão — não o afterthought.

Construí o **Public Data Quality Auditor BR**: uma app local (FastAPI + Next.js) que recebe CSV, faz profiling, aplica checks de completude, unicidade, validade, consistência e documentabilidade, calcula um score 0–100 explicável e exporta relatório + `datapackage.json`.

O ponto não é “certificar” a base. É tornar os riscos visíveis — com issues, amostras de linhas e recomendações — para jornalistas, pesquisadores e analistas que dependem de dados abertos.

Demos sintético-realistas (municípios, escolas, contratos) rodam sem depender de crawler. Metodologia e limitações documentadas.

Se você trabalha com dados abertos no Brasil: qual foi o último problema de qualidade que quase passou batido?
