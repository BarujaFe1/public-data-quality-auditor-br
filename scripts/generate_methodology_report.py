"""Generate reproducible methodological audit reports for demo + public datasets."""

from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
API_ROOT = ROOT / "apps" / "api"
sys.path.insert(0, str(API_ROOT))

from app.config import DEMO_DATASETS  # noqa: E402
from app.services.audit_service import (  # noqa: E402
    _demo_path,
    _read_csv_bytes,
    audit_dataframe,
)

OUT_DIR = ROOT / "docs" / "reports"


def _run_one(key: str, title: str, path: Path, filename: str, kind: str) -> str:
    content = path.read_bytes()
    df = _read_csv_bytes(content, filename)
    audit = audit_dataframe(df, dataset_name=title, filename=filename)
    lines = [
        f"## Dataset: {title}",
        "",
        f"- **Id:** `{key}`",
        f"- **Tipo:** `{kind}`",
        f"- **Arquivo:** `{filename}`",
        f"- **Audit id:** `{audit.id}`",
        f"- **Linhas / colunas:** {audit.row_count} / {audit.column_count}",
        f"- **Score geral:** {audit.overall_score}/100",
        f"- **Completude:** {audit.completeness_score}",
        f"- **Unicidade:** {audit.uniqueness_score}",
        f"- **Validade:** {audit.validity_score}",
        f"- **Consistência:** {audit.consistency_score}",
        f"- **Documentabilidade:** {audit.documentation_score}",
        f"- **Issues:** {len(audit.issues)}",
        "",
        "### Recomendação executiva",
        "",
        audit.executive_recommendation,
        "",
        "### Top issues (até 8)",
        "",
    ]
    ranked = sorted(
        audit.issues,
        key=lambda i: (
            {"critical": 0, "high": 1, "warning": 2, "info": 3}.get(i.severity.value, 9),
            -i.affected_rows_count,
        ),
    )[:8]
    if not ranked:
        lines.append("_Nenhum issue detectado._")
    else:
        for issue in ranked:
            col = issue.column_name or "—"
            lines.append(
                f"- **[{issue.severity.value}]** `{issue.issue_type}` @ `{col}` — {issue.message}"
            )
    if kind == "public_sample":
        lines.extend(["", f"_Proveniência: [docs/PROVENANCE.md](../PROVENANCE.md)._"])
    lines.extend(["", "---", ""])
    return "\n".join(lines)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ")
    parts = [
        "# Relatório metodológico reproduzível",
        "",
        f"_Gerado em {stamp} UTC por `scripts/generate_methodology_report.py`._",
        "",
        "Este relatório documenta o resultado do **mesmo motor** usado na API "
        "(profiling + checks + score). O score é **diagnóstico**, não certificação.",
        "",
        "## Como reproduzir",
        "",
        "```bash",
        "cd apps/api",
        "python -m venv .venv && .venv/Scripts/activate  # Windows",
        "pip install -r requirements.txt",
        "cd ../..",
        "apps/api/.venv/Scripts/python scripts/generate_methodology_report.py",
        "```",
        "",
        "---",
        "",
    ]

    for key, meta in DEMO_DATASETS.items():
        path = _demo_path(meta)
        if not path.exists():
            raise SystemExit(f"Missing file for {key}: {path}")
        parts.append(
            _run_one(
                key,
                meta["title"],
                path,
                meta["filename"],
                meta.get("kind", "synthetic"),
            )
        )

    parts.extend(
        [
            "## Limitações deste relatório",
            "",
            "- Snapshots/lab na demo pública podem diferir se o motor mudar sem refresh.",
            "- A amostra IBGE não é o catálogo completo.",
            "- Não valida verdade factual dos registros.",
            "- Score ponderado por dimensões; ver `docs/METHODOLOGY.md` quando existir.",
            "",
        ]
    )

    out = OUT_DIR / "methodology_run.md"
    out.write_text("\n".join(parts), encoding="utf-8")
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
