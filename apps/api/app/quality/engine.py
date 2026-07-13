"""Orchestrates profiling, checks, scoring, dictionary and report generation."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any

import pandas as pd

from app.quality.checks import run_all_checks
from app.quality.profiling import infer_series_type, serialize_value, try_parse_number
from app.quality.scoring import compute_all_scores, executive_recommendation
from app.reports.datapackage import build_datapackage
from app.reports.markdown_report import build_markdown_report
from app.schemas.audit import AuditRun, ColumnProfile, DataDictionaryField


DESCRIPTION_TEMPLATES: dict[str, str] = {
    "codigo_municipio": "Código IBGE do município (7 dígitos).",
    "municipio": "Nome do município.",
    "uf": "Sigla da Unidade Federativa.",
    "populacao": "População estimada ou censitária.",
    "area_km2": "Área territorial em km².",
    "data_atualizacao": "Data de atualização do registro.",
    "id_escola": "Identificador da escola.",
    "nome_escola": "Nome da unidade escolar.",
    "rede": "Rede de ensino (Municipal, Estadual, Federal, Privada).",
    "alunos_matriculados": "Quantidade de alunos matriculados.",
    "etapa_ensino": "Etapa/modalidade de ensino.",
    "data_censo": "Data de referência do censo escolar.",
    "id_contrato": "Identificador do contrato.",
    "orgao": "Órgão contratante.",
    "fornecedor": "Razão social do fornecedor.",
    "cnpj": "CNPJ do fornecedor.",
    "valor_contrato": "Valor contratado em reais.",
    "data_inicio": "Data de início da vigência.",
    "data_fim": "Data de fim da vigência.",
    "modalidade": "Modalidade de licitação/contratação.",
}


def _suggest_description(column: str, inferred_type: str) -> str:
    key = column.strip().lower()
    if key in DESCRIPTION_TEMPLATES:
        return DESCRIPTION_TEMPLATES[key]
    readable = column.replace("_", " ").strip()
    return f"Campo '{readable}' com tipo inferido {inferred_type}. Descrição automática — revise com o produtor dos dados."


def profile_columns(df: pd.DataFrame, audit_id: str) -> list[ColumnProfile]:
    profiles: list[ColumnProfile] = []
    n = len(df)
    for col in df.columns:
        series = df[col]
        null_mask = series.isna() | series.astype(str).str.strip().eq("")
        null_count = int(null_mask.sum())
        non_null = series[~null_mask]
        distinct_count = int(non_null.nunique()) if len(non_null) else 0
        inferred = infer_series_type(series, str(col))

        sample_values = [serialize_value(v) for v in non_null.head(5).tolist()]
        most_common: list[dict[str, Any]] = []
        if len(non_null):
            vc = non_null.astype(str).value_counts().head(5)
            most_common = [{"value": k, "count": int(v)} for k, v in vc.items()]

        min_value = max_value = None
        if inferred in {"integer", "number"}:
            nums = [try_parse_number(v) for v in non_null]
            nums = [x for x in nums if x is not None]
            if nums:
                min_value = min(nums)
                max_value = max(nums)
        elif inferred == "date":
            dates = pd.to_datetime(non_null, errors="coerce").dropna()
            if len(dates):
                min_value = dates.min().isoformat()
                max_value = dates.max().isoformat()

        warnings: list[str] = []
        if null_count == n and n > 0:
            warnings.append("Coluna totalmente vazia")
        elif n and null_count / n > 0.2:
            warnings.append(f"Alta taxa de nulos ({null_count / n:.0%})")
        if inferred == "empty":
            warnings.append("Sem valores para inferir tipo")

        profiles.append(
            ColumnProfile(
                id=str(uuid.uuid4()),
                audit_run_id=audit_id,
                column_name=str(col),
                inferred_type=inferred,
                null_count=null_count,
                null_rate=round(null_count / n, 4) if n else 0.0,
                distinct_count=distinct_count,
                distinct_rate=round(distinct_count / n, 4) if n else 0.0,
                sample_values=sample_values,
                min_value=min_value,
                max_value=max_value,
                most_common_values=most_common,
                warnings=warnings,
            )
        )
    return profiles


def build_data_dictionary(
    profiles: list[ColumnProfile],
    issues: list,
    audit_id: str,
) -> list[DataDictionaryField]:
    issues_by_col: dict[str, list[str]] = {}
    for issue in issues:
        if issue.column_name:
            issues_by_col.setdefault(issue.column_name, []).append(issue.issue_type)

    fields: list[DataDictionaryField] = []
    for profile in profiles:
        notes = ""
        related = issues_by_col.get(profile.column_name, [])
        if related:
            notes = "Issues: " + ", ".join(sorted(set(related)))
        if profile.warnings:
            notes = (notes + "; " if notes else "") + "; ".join(profile.warnings)

        fields.append(
            DataDictionaryField(
                id=str(uuid.uuid4()),
                audit_run_id=audit_id,
                column_name=profile.column_name,
                inferred_type=profile.inferred_type,
                nullable=profile.null_count > 0,
                description_suggestion=_suggest_description(
                    profile.column_name, profile.inferred_type
                ),
                example_values=profile.sample_values[:3],
                quality_notes=notes,
            )
        )
    return fields


def run_audit(
    df: pd.DataFrame,
    *,
    dataset_name: str,
    uploaded_filename: str,
) -> AuditRun:
    audit_id = str(uuid.uuid4())
    created_at = datetime.now(timezone.utc)

    # Normalize empty strings to NA for consistent profiling, keep original for samples via copy
    working = df.copy()
    for col in working.columns:
        if working[col].dtype == object:
            working[col] = working[col].map(
                lambda v: pd.NA if (isinstance(v, str) and v.strip() == "") else v
            )

    profiles = profile_columns(working, audit_id)
    issues = run_all_checks(working, audit_id)
    scores = compute_all_scores(issues)
    dictionary = build_data_dictionary(profiles, issues, audit_id)
    recommendation = executive_recommendation(scores["overall"], issues)

    audit = AuditRun(
        id=audit_id,
        dataset_name=dataset_name,
        uploaded_filename=uploaded_filename,
        row_count=int(len(working)),
        column_count=int(len(working.columns)),
        overall_score=scores["overall"],
        completeness_score=scores["completeness"],
        uniqueness_score=scores["uniqueness"],
        validity_score=scores["validity"],
        consistency_score=scores["consistency"],
        documentation_score=scores["documentation"],
        created_at=created_at,
        status="completed",
        executive_recommendation=recommendation,
        columns=profiles,
        issues=issues,
        data_dictionary=dictionary,
    )

    audit.datapackage = build_datapackage(audit)
    audit.report_markdown = build_markdown_report(audit)
    return audit
