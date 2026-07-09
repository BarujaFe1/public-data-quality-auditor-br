# Fontes públicas brasileiras (referência futura)

O MVP **não depende** destas fontes. Use-as quando quiser substituir os CSVs demo.

| Fonte | Conteúdo típico | Observação |
|-------|-----------------|------------|
| [Portal Brasileiro de Dados Abertos](https://dados.gov.br/) | Catálogo federal | Verificar licença e atualização |
| [IBGE](https://www.ibge.gov.br/) | Municípios, demografia, malhas | Códigos oficiais de município |
| [INEP / Dados Abertos](https://www.gov.br/inep/) | Censo escolar | Bases grandes — amostrar no MVP |
| [Portal da Transparência](https://portaldatransparencia.gov.br/) | Despesas, contratos, favorecidos | CNPJ e valores sensíveis a formato |
| [TSE Dados Abertos](https://dadosabertos.tse.jus.br/) | Eleições | Encoding e layouts variam por ano |
| [DATASUS](https://datasus.saude.gov.br/) | Saúde | Frequentemente em formatos legados |
| [Compras.gov.br](https://www.gov.br/compras/) | Licitações | Modalidades e vigências |

## Como trocar no projeto

1. Baixe o CSV e documente URL, data de download e licença.
2. Salve em `data/demo/` **ou** faça upload pela UI.
3. Se necessário, registre o dataset em `DEMO_DATASETS` (`apps/api/app/config.py`).
4. Rode a auditoria e anote o score no README/portfólio.

## Cuidados

- Respeite termos de uso e robots/políticas de acesso.
- Não faça scraping agressivo sem permissão.
- Prefira downloads oficiais e APIs documentadas.
