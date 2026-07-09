# Notas sobre o `datapackage.json`

## O que é gerado

Um descriptor inspirado em [Frictionless Data Package](https://specs.frictionlessdata.io/), contendo:

- `name`, `title`, `description`, `profile`
- `resources[]` com `path`/`filename`, `format`, `mediatype`
- `schema.fields[]` com `name`, `type` inferido, `description`, `constraints.required`, `examples`
- placeholder de `licenses` (`UNKNOWN`) e `contributors`

Endpoint: `GET /audit/{audit_id}/datapackage.json`

## Limitações

- Não implementa a especificação completa (foreign keys, dialects avançados, hashing, etc.).
- Tipos e descrições são **inferidos/sugeridos** — exigem revisão humana.
- Licença não é detectada automaticamente.
- O `path` aponta para o nome do arquivo auditado, não para um pacote publicado.

## Por que existe no MVP

Demonstra mentalidade de **documentação de dados**: schema versionável, metadados mínimos e interoperabilidade com ecossistema de dados abertos.
