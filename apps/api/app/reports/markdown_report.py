"""Markdown report builder."""

from __future__ import annotations

from app.schemas.audit import AuditRun, Severity

SEVERITY_ORDER = {
    Severity.CRITICAL: 0,
    Severity.HIGH: 1,
    Severity.WARNING: 2,
    Severity.INFO: 3,
}


def build_markdown_report(audit: AuditRun) -> str:
    top_issues = sorted(
        audit.issues,
        key=lambda i: (SEVERITY_ORDER.get(i.severity, 9), -i.affected_rows_count),
    )[:10]

    col_problem_counts: dict[str, int] = {}
    for issue in audit.issues:
        if issue.column_name:
            col_problem_counts[issue.column_name] = col_problem_counts.get(issue.column_name, 0) + 1
    worst_cols = sorted(col_problem_counts.items(), key=lambda x: -x[1])[:8]

    lines = [
        f"# Relatório de Qualidade — {audit.dataset_name}",
        "",
        f"- **Arquivo:** `{audit.uploaded_filename}`",
        f"- **Data da auditoria:** {audit.created_at.isoformat()}",
        f"- **Linhas:** {audit.row_count}",
        f"- **Colunas:** {audit.column_count}",
        f"- **Score geral:** {audit.overall_score}/100",
        "",
        "## Scores por dimensão",
        "",
        f"| Dimensão | Score |",
        f"|---|---:|",
        f"| Completude | {audit.completeness_score} |",
        f"| Unicidade | {audit.uniqueness_score} |",
        f"| Validade | {audit.validity_score} |",
        f"| Consistência | {audit.consistency_score} |",
        f"| Documentabilidade | {audit.documentation_score} |",
        "",
        "## Recomendação executiva",
        "",
        audit.executive_recommendation,
        "",
        "## Top 10 issues",
        "",
    ]

    if not top_issues:
        lines.append("_Nenhum issue detectado._")
    else:
        for i, issue in enumerate(top_issues, 1):
            col = issue.column_name or "—"
            lines.append(
                f"{i}. **[{issue.severity.value}]** `{issue.issue_type}` em `{col}` "
                f"({issue.dimension}) — {issue.message}"
            )
            lines.append(f"   - Recomendação: {issue.recommendation}")

    lines.extend(["", "## Colunas mais problemáticas", ""])
    if not worst_cols:
        lines.append("_Sem colunas com issues associados._")
    else:
        for name, count in worst_cols:
            lines.append(f"- `{name}`: {count} issue(s)")

    lines.extend(["", "## Recomendações gerais", ""])
    lines.extend(
        [
            "1. Trate issues críticos e de alta severidade antes de análises públicas.",
            "2. Normalize categorias, datas e chaves.",
            "3. Publique dicionário de dados revisado por um humano.",
            "4. Documente licença, frequência de atualização e origem.",
            "5. Reexecute a auditoria após limpeza.",
        ]
    )

    lines.extend(["", "## Dicionário resumido", ""])
    lines.append("| Coluna | Tipo | Nullable | Descrição sugerida |")
    lines.append("|---|---|---|---|")
    for field in audit.data_dictionary:
        desc = field.description_suggestion.replace("|", "/")
        lines.append(
            f"| `{field.column_name}` | {field.inferred_type} | "
            f"{'sim' if field.nullable else 'não'} | {desc} |"
        )

    lines.extend(
        [
            "",
            "## Limitações",
            "",
            "- O score é **diagnóstico**, não certificação absoluta.",
            "- A auditoria **não valida a verdade factual** dos dados.",
            "- Checks são heurísticos e podem gerar falsos positivos/negativos.",
            "- Formatos brasileiros e encoding podem exigir ajustes manuais.",
            "",
            "## Próximos passos",
            "",
            "1. Exportar este relatório e o `datapackage.json`.",
            "2. Corrigir issues prioritários na origem.",
            "3. Versionar o dataset limpo com metadados.",
            "4. Reauditar e comparar scores.",
            "",
        ]
    )
    return "\n".join(lines)
