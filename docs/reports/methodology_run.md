# Relatório metodológico reproduzível

_Gerado em 2026-07-13T20:26Z UTC por `scripts/generate_methodology_report.py`._

Este relatório documenta o resultado do **mesmo motor** usado na API (profiling + checks + score). O score é **diagnóstico**, não certificação.

## Como reproduzir

```bash
cd apps/api
python -m venv .venv && .venv/Scripts/activate  # Windows
pip install -r requirements.txt
cd ../..
apps/api/.venv/Scripts/python scripts/generate_methodology_report.py
```

---

## Dataset: Municípios BR (demo)

- **Id:** `municipios`
- **Tipo:** `synthetic`
- **Arquivo:** `municipios_demo.csv`
- **Audit id:** `5b44c9f9-2499-4e11-b35c-a23d9aa91a33`
- **Linhas / colunas:** 32 / 6
- **Score geral:** 87.4/100
- **Completude:** 92.0
- **Unicidade:** 85.0
- **Validade:** 76.0
- **Consistência:** 92.0
- **Documentabilidade:** 100.0
- **Issues:** 7

### Recomendação executiva

A base é utilizável com ressalvas. Priorize correção de issues de severidade alta/crítica e normalize categorias e datas antes de análises sensíveis.

### Top issues (até 8)

- **[critical]** `duplicate_id` @ `codigo_municipio` — Possível chave 'codigo_municipio' com 4 valor(es) duplicado(s).
- **[high]** `invalid_date` @ `data_atualizacao` — A coluna 'data_atualizacao' tem 2 data(s) inválida(s).
- **[high]** `empty_rows` @ `—` — Há 1 linha(s) totalmente vazia(s).
- **[high]** `negative_quantity` @ `populacao` — A coluna 'populacao' tem 1 valor(es) negativo(s) suspeito(s).
- **[high]** `invalid_uf` @ `uf` — A coluna 'uf' tem 1 UF(s) inválida(s).
- **[warning]** `inconsistent_category` @ `municipio` — A coluna 'municipio' tem categorias com variação de caixa/acento (2 variantes em 1 grupo(s)). Exemplos: [['Sao Paulo', 'São Paulo']].
- **[warning]** `inconsistent_category` @ `uf` — A coluna 'uf' tem categorias com variação de caixa/acento (2 variantes em 1 grupo(s)). Exemplos: [['PR', 'pr']].

---

## Dataset: Escolas BR (demo)

- **Id:** `escolas`
- **Tipo:** `synthetic`
- **Arquivo:** `escolas_demo.csv`
- **Audit id:** `4987488f-9511-4a1e-961c-3168df83925c`
- **Linhas / colunas:** 26 / 8
- **Score geral:** 82.44/100
- **Completude:** 100.0
- **Unicidade:** 77.0
- **Validade:** 68.0
- **Consistência:** 75.2
- **Documentabilidade:** 100.0
- **Issues:** 9

### Recomendação executiva

A base é utilizável com ressalvas. Priorize correção de issues de severidade alta/crítica e normalize categorias e datas antes de análises sensíveis.

### Top issues (até 8)

- **[critical]** `duplicate_id` @ `id_escola` — Possível chave 'id_escola' com 2 valor(es) duplicado(s).
- **[high]** `duplicate_rows` @ `—` — Há 2 linha(s) envolvida(s) em duplicidade completa.
- **[high]** `invalid_date` @ `data_censo` — A coluna 'data_censo' tem 1 data(s) inválida(s).
- **[high]** `invalid_number` @ `alunos_matriculados` — A coluna 'alunos_matriculados' tem 1 valor(es) numérico(s) inválido(s).
- **[high]** `negative_quantity` @ `alunos_matriculados` — A coluna 'alunos_matriculados' tem 1 valor(es) negativo(s) suspeito(s).
- **[high]** `invalid_uf` @ `uf` — A coluna 'uf' tem 1 UF(s) inválida(s).
- **[warning]** `mixed_types` @ `alunos_matriculados` — A coluna 'alunos_matriculados' parece misturar tipos (números e texto).
- **[warning]** `inconsistent_category` @ `etapa_ensino` — A coluna 'etapa_ensino' tem categorias com variação de caixa/acento (4 variantes em 2 grupo(s)). Exemplos: [['Fundamental', 'fundamental'], ['Médio', 'médio']].

---

## Dataset: Contratos públicos (demo)

- **Id:** `contratos`
- **Tipo:** `synthetic`
- **Arquivo:** `contratos_demo.csv`
- **Audit id:** `dd7b68ba-29d1-4894-9ff9-09bb396dea1a`
- **Linhas / colunas:** 26 / 8
- **Score geral:** 78.72/100
- **Completude:** 100.0
- **Unicidade:** 26.0
- **Validade:** 84.0
- **Consistência:** 87.6
- **Documentabilidade:** 100.0
- **Issues:** 8

### Recomendação executiva

A base é utilizável com ressalvas. Priorize correção de issues de severidade alta/crítica e normalize categorias e datas antes de análises sensíveis.

### Top issues (até 8)

- **[critical]** `duplicate_id` @ `modalidade` — Possível chave 'modalidade' com 24 valor(es) duplicado(s).
- **[critical]** `duplicate_id` @ `cnpj` — Possível chave 'cnpj' com 3 valor(es) duplicado(s).
- **[critical]** `duplicate_id` @ `id_contrato` — Possível chave 'id_contrato' com 2 valor(es) duplicado(s).
- **[high]** `duplicate_rows` @ `—` — Há 2 linha(s) envolvida(s) em duplicidade completa.
- **[high]** `date_order_violation` @ `data_fim` — Há 2 registro(s) com 'data_fim' anterior a 'data_inicio'.
- **[high]** `negative_quantity` @ `valor_contrato` — A coluna 'valor_contrato' tem 1 valor(es) negativo(s) suspeito(s).
- **[high]** `invalid_cnpj` @ `cnpj` — A coluna 'cnpj' tem 1 CNPJ(s) com formato inválido.
- **[warning]** `inconsistent_category` @ `modalidade` — A coluna 'modalidade' tem categorias com variação de caixa/acento (3 variantes em 1 grupo(s)). Exemplos: [['PREGAO ELETRONICO', 'Pregão Eletrônico', 'pregão eletrônico']].

---

## Dataset: IBGE municípios (amostra pública)

- **Id:** `ibge_municipios`
- **Tipo:** `public_sample`
- **Arquivo:** `ibge_municipios_amostra.csv`
- **Audit id:** `d2bd6f51-568d-404b-a100-a8697790f0b8`
- **Linhas / colunas:** 31 / 4
- **Score geral:** 100.0/100
- **Completude:** 100.0
- **Unicidade:** 100.0
- **Validade:** 100.0
- **Consistência:** 100.0
- **Documentabilidade:** 100.0
- **Issues:** 0

### Recomendação executiva

A base apresenta qualidade boa para exploração inicial. Revise os avisos restantes e documente o dicionário antes de publicar análises.

### Top issues (até 8)

_Nenhum issue detectado._

_Proveniência: [docs/PROVENANCE.md](../PROVENANCE.md)._

---

## Limitações deste relatório

- Snapshots/lab na demo pública podem diferir se o motor mudar sem refresh.
- A amostra IBGE não é o catálogo completo.
- Não valida verdade factual dos registros.
- Score ponderado por dimensões; ver `docs/METHODOLOGY.md` quando existir.
