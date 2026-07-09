# Metodologia de auditoria

## Objetivo

Produzir um **diagnóstico explicável** da qualidade estrutural e sintática de um CSV, com score 0–100, issues acionáveis e artefatos de documentação (dicionário + datapackage).

## Pipeline

1. **Ingestão** — leitura com fallback de encoding (`utf-8-sig`, `utf-8`, `latin-1`, `cp1252`) e separador (`,`, `;`, tab).
2. **Profiling** — tipo inferido, nulos, distintos, min/max, amostras, valores mais frequentes.
3. **Checks** — regras testáveis por dimensão (completude, unicidade, validade, consistência, documentabilidade).
4. **Scoring** — cada dimensão começa em 100; issues reduzem pontos conforme severidade e volume afetado; score geral é média ponderada.
5. **Artefatos** — issues register, dicionário sugerido, relatório Markdown/HTML, `datapackage.json`.

## Severidades

| Severidade | Penalidade base | Exemplos |
|------------|-----------------|----------|
| info | 1 | data futura suspeita |
| warning | 4 | categoria com variação de caixa |
| high | 8 | data inválida, nulos altos |
| critical | 15 | coluna vazia, ID duplicado |

O fator de linhas amplifica levemente a penalidade (teto baixo) para não zerar o score com um único outlier.

## O que a metodologia assume

- O arquivo é tabular CSV com cabeçalho.
- Nomes de colunas carregam semântica útil (ex.: `data_*`, `id_*`, `uf`, `cnpj`).
- Valores vazios e strings em branco são tratados como nulos.

## O que a metodologia **não** afirma

- Que os dados são factualmente verdadeiros.
- Que a base está apta a qualquer uso analítico.
- Que a ausência de issues implica qualidade perfeita.
- Que a licença, a atualização ou a governança estão corretas.

## Reprodutibilidade

Os mesmos checks e pesos estão implementados em `apps/api/app/quality/` e cobertos por testes em `apps/api/tests/`. Reexecute a auditoria após limpeza para comparar scores.
