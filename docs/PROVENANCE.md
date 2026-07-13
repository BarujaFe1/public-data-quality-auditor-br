# Proveniência — amostra IBGE de municípios

## Dataset

| Campo | Valor |
|--------|--------|
| Arquivo | `data/public/ibge_municipios_amostra.csv` |
| Título | Amostra de municípios brasileiros (códigos IBGE) |
| Linhas | 31 (capitais + municípios selecionados) |
| Colunas | `codigo_municipio`, `municipio`, `uf`, `regiao` |

## Fonte e licença

- **Origem conceitual:** códigos oficiais de municípios do **IBGE** (Instituto Brasileiro de Geografia e Estatística), domínio público / dados abertos oficiais.
- **Natureza deste arquivo:** **amostra curada** para demo de portfólio — **não** é o dump completo do IBGE e **não** substitui download oficial.
- **Licença de uso neste repositório:** redistribuição educacional da amostra com atribuição ao IBGE. Consulte os termos vigentes em [ibge.gov.br](https://www.ibge.gov.br/) e catálogos oficiais antes de uso operacional.

## O que NÃO é

- Não é scraping não autorizado.
- Não inclui dados pessoais (PII).
- Não garante atualização contínua — a amostra é estática para reprodutibilidade do MVP.

## Como regenerar / ampliar

1. Baixe a tabela oficial de municípios (IBGE / dados.gov.br).
2. Selecione colunas mínimas: código (7 dígitos), nome, UF.
3. Documente URL, data de download e licença em um PR.
4. Rode a auditoria: `POST /audit/demo/ibge_municipios` (após registrar no catálogo) ou upload local.

## Por que existe no projeto

Complementa os CSVs **sintéticos intencionalmente sujos** (`data/demo/*`) com um exemplo de **dado público real** (estrutura oficial), para discutir proveniência, licença e qualidade sem depender de crawler.
