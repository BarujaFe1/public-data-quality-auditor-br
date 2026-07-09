# Limitações

- Diagnóstico estrutural/sintático, não validação factual.
- Heurísticas dependem de nomes de colunas em português/inglês comuns.
- Limites do MVP: 5 MB e 50 mil linhas por arquivo.
- Encoding/separador ambíguos podem exigir ajuste manual.
- CNPJ: validação de formato (14 dígitos), não algoritmo completo de dígitos verificadores.
- Sem autenticação, histórico multi-usuário ou agendamento.
- Frontend assume API em `http://localhost:8000` por padrão.
- Docker é opcional; o ambiente de desenvolvimento validado é venv + npm locais.
- Datasets demo são sintéticos e intencionalmente “sujos”.
