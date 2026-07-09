# Dimensões de qualidade

## Completude (peso 25)

Avalia presença de informação.

**Checks:** coluna totalmente vazia; taxa de nulos acima de 20%; linhas totalmente vazias.

**Penalidades típicas:** critical para coluna vazia; high/warning conforme taxa de nulos.

## Unicidade (peso 20)

Avalia duplicidade de registros e chaves.

**Checks:** linhas duplicadas completas; possível ID duplicado (`id_*`, `codigo_*`, etc.).

**Penalidades típicas:** high/critical — chaves repetidas quebram joins e contagens.

## Validade (peso 25)

Avalia conformidade de domínio/formato.

**Checks:** datas inválidas; números inválidos; valores negativos suspeitos; UF inválida; e-mail/CEP/CNPJ quando detectáveis.

**Penalidades típicas:** high para domínio quebrado; warning para formatos leves.

## Consistência (peso 20)

Avalia coerência interna.

**Checks:** categorias com variação de caixa/acento; tipos mistos; datas futuras suspeitas; `data_fim` < `data_inicio`.

**Penalidades típicas:** warning/high conforme impacto.

## Documentabilidade (peso 10)

Avalia capacidade de documentar o dataset.

**Checks:** nomes ruins (`col1`, `Unnamed: 0`, `x`); geração de dicionário com descrições sugeridas.

**Penalidades típicas:** warning por coluna mal nomeada.

## Score geral

```
overall = completeness*0.25 + uniqueness*0.20 + validity*0.25
        + consistency*0.20 + documentation*0.10
```

Interpretação sugerida: ≥85 exploração com revisão; 70–84 uso com ressalvas; 50–69 limpeza necessária; <50 inadequado para análise confiável.
