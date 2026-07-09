"""Quality checks that produce QualityIssue records."""

from __future__ import annotations

import re
import uuid
from collections import defaultdict
from datetime import datetime, timezone
from typing import Any

import pandas as pd

from app.config import (
    BAD_COLUMN_NAMES,
    CEP_HINTS,
    CNPJ_HINTS,
    DATE_HINTS,
    EMAIL_HINTS,
    ID_HINTS,
    NULL_RATE_THRESHOLD,
    QUANTITY_HINTS,
    SAMPLE_SIZE,
    UF_HINTS,
    VALID_UFS,
)
from app.quality.profiling import (
    column_name_looks_like,
    detect_mixed_types,
    is_nullish,
    is_valid_cep,
    is_valid_cnpj_format,
    is_valid_email,
    normalize_text,
    serialize_value,
    try_parse_date,
    try_parse_number,
)
from app.schemas.audit import QualityIssue, Severity


def _issue(
    audit_id: str,
    *,
    issue_type: str,
    dimension: str,
    severity: Severity,
    message: str,
    recommendation: str,
    column_name: str | None = None,
    affected_rows_count: int = 0,
    affected_rows_sample: list[dict[str, Any]] | None = None,
) -> QualityIssue:
    return QualityIssue(
        id=str(uuid.uuid4()),
        audit_run_id=audit_id,
        column_name=column_name,
        issue_type=issue_type,
        dimension=dimension,
        severity=severity,
        message=message,
        affected_rows_count=affected_rows_count,
        affected_rows_sample=affected_rows_sample or [],
        recommendation=recommendation,
        created_at=datetime.now(timezone.utc),
    )


def _row_sample(df: pd.DataFrame, mask: pd.Series, limit: int = SAMPLE_SIZE) -> list[dict[str, Any]]:
    if mask is None or not mask.any():
        return []
    subset = df.loc[mask].head(limit)
    records: list[dict[str, Any]] = []
    for idx, row in subset.iterrows():
        payload = {"_row_index": int(idx) if isinstance(idx, (int, float)) else str(idx)}
        for col in df.columns:
            payload[str(col)] = serialize_value(row[col])
        records.append(payload)
    return records


def check_empty_columns(df: pd.DataFrame, audit_id: str) -> list[QualityIssue]:
    issues: list[QualityIssue] = []
    for col in df.columns:
        series = df[col]
        if series.isna().all() or series.astype(str).str.strip().eq("").all():
            issues.append(
                _issue(
                    audit_id,
                    column_name=str(col),
                    issue_type="empty_column",
                    dimension="completeness",
                    severity=Severity.CRITICAL,
                    message=f"A coluna '{col}' está totalmente vazia.",
                    recommendation="Remova a coluna ou preencha com dados válidos antes da análise.",
                    affected_rows_count=len(df),
                )
            )
    return issues


def check_null_rates(df: pd.DataFrame, audit_id: str, threshold: float = NULL_RATE_THRESHOLD) -> list[QualityIssue]:
    issues: list[QualityIssue] = []
    for col in df.columns:
        series = df[col]
        null_mask = series.isna() | series.astype(str).str.strip().eq("")
        rate = float(null_mask.mean()) if len(series) else 0.0
        if rate > threshold and rate < 1.0:
            severity = Severity.HIGH if rate > 0.5 else Severity.WARNING
            issues.append(
                _issue(
                    audit_id,
                    column_name=str(col),
                    issue_type="high_null_rate",
                    dimension="completeness",
                    severity=severity,
                    message=f"A coluna '{col}' tem {rate:.1%} de valores nulos/vazios (limite {threshold:.0%}).",
                    recommendation="Investigue a origem dos nulos e documente se a ausência é esperada.",
                    affected_rows_count=int(null_mask.sum()),
                    affected_rows_sample=_row_sample(df, null_mask),
                )
            )
    return issues


def check_empty_rows(df: pd.DataFrame, audit_id: str) -> list[QualityIssue]:
    if df.empty:
        return []
    empty_mask = df.apply(lambda row: all(is_nullish(v) for v in row), axis=1)
    count = int(empty_mask.sum())
    if count == 0:
        return []
    return [
        _issue(
            audit_id,
            issue_type="empty_rows",
            dimension="completeness",
            severity=Severity.HIGH,
            message=f"Há {count} linha(s) totalmente vazia(s).",
            recommendation="Remova linhas vazias no pré-processamento.",
            affected_rows_count=count,
            affected_rows_sample=_row_sample(df, empty_mask),
        )
    ]


def check_duplicate_rows(df: pd.DataFrame, audit_id: str) -> list[QualityIssue]:
    if df.empty:
        return []
    dup_mask = df.duplicated(keep=False)
    count = int(dup_mask.sum())
    if count == 0:
        return []
    return [
        _issue(
            audit_id,
            issue_type="duplicate_rows",
            dimension="uniqueness",
            severity=Severity.HIGH,
            message=f"Há {count} linha(s) envolvida(s) em duplicidade completa.",
            recommendation="Deduplique com chave de negócio ou remova cópias exatas.",
            affected_rows_count=count,
            affected_rows_sample=_row_sample(df, dup_mask),
        )
    ]


def check_duplicate_ids(df: pd.DataFrame, audit_id: str) -> list[QualityIssue]:
    issues: list[QualityIssue] = []
    for col in df.columns:
        if not column_name_looks_like(str(col), ID_HINTS):
            continue
        series = df[col]
        non_null = series.dropna()
        if non_null.empty:
            continue
        dup_mask = series.duplicated(keep=False) & series.notna()
        # also treat empty string as null-ish for id
        empty = series.astype(str).str.strip().eq("")
        dup_mask = dup_mask & ~empty
        count = int(dup_mask.sum())
        if count == 0:
            continue
        issues.append(
            _issue(
                audit_id,
                column_name=str(col),
                issue_type="duplicate_id",
                dimension="uniqueness",
                severity=Severity.CRITICAL,
                message=f"Possível chave '{col}' com {count} valor(es) duplicado(s).",
                recommendation="Garanta unicidade da chave primária ou revise a granularidade do dataset.",
                affected_rows_count=count,
                affected_rows_sample=_row_sample(df, dup_mask),
            )
        )
    return issues


def check_invalid_dates(df: pd.DataFrame, audit_id: str) -> list[QualityIssue]:
    issues: list[QualityIssue] = []
    for col in df.columns:
        if not column_name_looks_like(str(col), DATE_HINTS):
            # also check if majority look like dates but some fail
            sample = df[col].dropna().head(50)
            if sample.empty:
                continue
            date_like = sample.map(lambda v: try_parse_date(v) is not None).mean()
            if date_like < 0.5:
                continue

        mask_invalid = []
        for value in df[col]:
            if is_nullish(value):
                mask_invalid.append(False)
            else:
                mask_invalid.append(try_parse_date(value) is None)
        invalid_mask = pd.Series(mask_invalid, index=df.index)
        count = int(invalid_mask.sum())
        if count == 0:
            continue
        issues.append(
            _issue(
                audit_id,
                column_name=str(col),
                issue_type="invalid_date",
                dimension="validity",
                severity=Severity.HIGH,
                message=f"A coluna '{col}' tem {count} data(s) inválida(s).",
                recommendation="Padronize datas em ISO 8601 (YYYY-MM-DD) e rejeite valores não parseáveis.",
                affected_rows_count=count,
                affected_rows_sample=_row_sample(df, invalid_mask),
            )
        )
    return issues


def check_invalid_numbers(df: pd.DataFrame, audit_id: str) -> list[QualityIssue]:
    issues: list[QualityIssue] = []
    for col in df.columns:
        if not column_name_looks_like(str(col), QUANTITY_HINTS):
            continue
        mask_invalid = []
        for value in df[col]:
            if is_nullish(value):
                mask_invalid.append(False)
            else:
                mask_invalid.append(try_parse_number(value) is None)
        invalid_mask = pd.Series(mask_invalid, index=df.index)
        count = int(invalid_mask.sum())
        if count == 0:
            continue
        issues.append(
            _issue(
                audit_id,
                column_name=str(col),
                issue_type="invalid_number",
                dimension="validity",
                severity=Severity.HIGH,
                message=f"A coluna '{col}' tem {count} valor(es) numérico(s) inválido(s).",
                recommendation="Converta para número e trate separadores BR (1.234,56) de forma consistente.",
                affected_rows_count=count,
                affected_rows_sample=_row_sample(df, invalid_mask),
            )
        )
    return issues


def check_negative_quantities(df: pd.DataFrame, audit_id: str) -> list[QualityIssue]:
    issues: list[QualityIssue] = []
    for col in df.columns:
        if not column_name_looks_like(str(col), QUANTITY_HINTS):
            continue
        negatives = []
        for value in df[col]:
            num = try_parse_number(value)
            negatives.append(num is not None and num < 0)
        neg_mask = pd.Series(negatives, index=df.index)
        count = int(neg_mask.sum())
        if count == 0:
            continue
        issues.append(
            _issue(
                audit_id,
                column_name=str(col),
                issue_type="negative_quantity",
                dimension="validity",
                severity=Severity.HIGH,
                message=f"A coluna '{col}' tem {count} valor(es) negativo(s) suspeito(s).",
                recommendation="Valide se negativos fazem sentido; para população/valor/quantidade, corrija ou documente.",
                affected_rows_count=count,
                affected_rows_sample=_row_sample(df, neg_mask),
            )
        )
    return issues


def check_invalid_uf(df: pd.DataFrame, audit_id: str) -> list[QualityIssue]:
    issues: list[QualityIssue] = []
    for col in df.columns:
        if not column_name_looks_like(str(col), UF_HINTS):
            continue
        invalid = []
        for value in df[col]:
            if is_nullish(value):
                invalid.append(False)
            else:
                uf = str(value).strip().upper()
                invalid.append(uf not in VALID_UFS)
        inv_mask = pd.Series(invalid, index=df.index)
        count = int(inv_mask.sum())
        if count == 0:
            continue
        issues.append(
            _issue(
                audit_id,
                column_name=str(col),
                issue_type="invalid_uf",
                dimension="validity",
                severity=Severity.HIGH,
                message=f"A coluna '{col}' tem {count} UF(s) inválida(s).",
                recommendation="Normalize UFs para as 27 siglas oficiais (ex.: SP, RJ, MG).",
                affected_rows_count=count,
                affected_rows_sample=_row_sample(df, inv_mask),
            )
        )
    return issues


def check_email_cep_cnpj(df: pd.DataFrame, audit_id: str) -> list[QualityIssue]:
    issues: list[QualityIssue] = []
    for col in df.columns:
        name = str(col)
        if column_name_looks_like(name, EMAIL_HINTS):
            bad = [not is_valid_email(v) and not is_nullish(v) for v in df[col]]
            mask = pd.Series(bad, index=df.index)
            if mask.any():
                issues.append(
                    _issue(
                        audit_id,
                        column_name=name,
                        issue_type="invalid_email",
                        dimension="validity",
                        severity=Severity.WARNING,
                        message=f"A coluna '{name}' tem {int(mask.sum())} e-mail(s) com formato inválido.",
                        recommendation="Valide formato de e-mail e remova valores placeholder.",
                        affected_rows_count=int(mask.sum()),
                        affected_rows_sample=_row_sample(df, mask),
                    )
                )
        if column_name_looks_like(name, CEP_HINTS):
            bad = [not is_valid_cep(v) and not is_nullish(v) for v in df[col]]
            mask = pd.Series(bad, index=df.index)
            if mask.any():
                issues.append(
                    _issue(
                        audit_id,
                        column_name=name,
                        issue_type="invalid_cep",
                        dimension="validity",
                        severity=Severity.WARNING,
                        message=f"A coluna '{name}' tem {int(mask.sum())} CEP(s) com formato inválido.",
                        recommendation="Padronize CEP como NNNNN-NNN ou 8 dígitos.",
                        affected_rows_count=int(mask.sum()),
                        affected_rows_sample=_row_sample(df, mask),
                    )
                )
        if column_name_looks_like(name, CNPJ_HINTS):
            bad = [not is_valid_cnpj_format(v) and not is_nullish(v) for v in df[col]]
            mask = pd.Series(bad, index=df.index)
            if mask.any():
                issues.append(
                    _issue(
                        audit_id,
                        column_name=name,
                        issue_type="invalid_cnpj",
                        dimension="validity",
                        severity=Severity.HIGH,
                        message=f"A coluna '{name}' tem {int(mask.sum())} CNPJ(s) com formato inválido.",
                        recommendation="Armazene CNPJ com 14 dígitos e valide dígitos verificadores quando possível.",
                        affected_rows_count=int(mask.sum()),
                        affected_rows_sample=_row_sample(df, mask),
                    )
                )
    return issues


def check_category_case_accent(df: pd.DataFrame, audit_id: str) -> list[QualityIssue]:
    issues: list[QualityIssue] = []
    for col in df.columns:
        series = df[col].dropna()
        if series.empty:
            continue
        # only categorical-ish columns
        nunique = series.nunique()
        if nunique > 40 or nunique < 2:
            continue
        if series.map(lambda v: try_parse_number(v) is not None).mean() > 0.8:
            continue

        groups: dict[str, set[str]] = defaultdict(set)
        for value in series.astype(str):
            raw = value.strip()
            if not raw:
                continue
            groups[normalize_text(raw)].add(raw)

        variants = {k: sorted(v) for k, v in groups.items() if len(v) > 1}
        if not variants:
            continue

        examples = list(variants.values())[:3]
        affected = sum(len(v) for v in variants.values())
        issues.append(
            _issue(
                audit_id,
                column_name=str(col),
                issue_type="inconsistent_category",
                dimension="consistency",
                severity=Severity.WARNING,
                message=(
                    f"A coluna '{col}' tem categorias com variação de caixa/acento "
                    f"({affected} variantes em {len(variants)} grupo(s)). Exemplos: {examples}."
                ),
                recommendation="Normalize categorias (caixa, acentos) com um dicionário canônico.",
                affected_rows_count=int(
                    series.astype(str).map(lambda v: normalize_text(v) in variants).sum()
                ),
            )
        )
    return issues


def check_mixed_types(df: pd.DataFrame, audit_id: str) -> list[QualityIssue]:
    issues: list[QualityIssue] = []
    for col in df.columns:
        if detect_mixed_types(df[col]):
            issues.append(
                _issue(
                    audit_id,
                    column_name=str(col),
                    issue_type="mixed_types",
                    dimension="consistency",
                    severity=Severity.WARNING,
                    message=f"A coluna '{col}' parece misturar tipos (números e texto).",
                    recommendation="Separe tipos ou force conversão com tratamento de erros.",
                    affected_rows_count=int(df[col].notna().sum()),
                )
            )
    return issues


def check_future_dates(df: pd.DataFrame, audit_id: str) -> list[QualityIssue]:
    issues: list[QualityIssue] = []
    today = pd.Timestamp.now(tz=None).normalize()
    for col in df.columns:
        if not column_name_looks_like(str(col), DATE_HINTS):
            continue
        # skip end dates that may be future contracts
        name = normalize_text(str(col))
        if "fim" in name or "end" in name or "venc" in name:
            continue
        future = []
        for value in df[col]:
            parsed = try_parse_date(value)
            future.append(parsed is not None and parsed.normalize() > today + pd.Timedelta(days=365))
        mask = pd.Series(future, index=df.index)
        if mask.any():
            issues.append(
                _issue(
                    audit_id,
                    column_name=str(col),
                    issue_type="suspicious_future_date",
                    dimension="consistency",
                    severity=Severity.INFO,
                    message=f"A coluna '{col}' tem {int(mask.sum())} data(s) mais de 1 ano no futuro.",
                    recommendation="Confirme se datas futuras são esperadas (ex.: vigência).",
                    affected_rows_count=int(mask.sum()),
                    affected_rows_sample=_row_sample(df, mask),
                )
            )
    return issues


def check_date_order_dependencies(df: pd.DataFrame, audit_id: str) -> list[QualityIssue]:
    """Simple dependency: data_fim >= data_inicio when both present."""
    cols = {normalize_text(str(c)): str(c) for c in df.columns}
    start_col = None
    end_col = None
    for key, original in cols.items():
        if "data_inicio" in key or key.endswith("inicio") or "start" in key:
            start_col = original
        if "data_fim" in key or key.endswith("fim") or "end" in key:
            end_col = original
    if not start_col or not end_col:
        return []

    bad = []
    for _, row in df.iterrows():
        start = try_parse_date(row[start_col])
        end = try_parse_date(row[end_col])
        if start is not None and end is not None and end < start:
            bad.append(True)
        else:
            bad.append(False)
    mask = pd.Series(bad, index=df.index)
    if not mask.any():
        return []
    return [
        _issue(
            audit_id,
            column_name=end_col,
            issue_type="date_order_violation",
            dimension="consistency",
            severity=Severity.HIGH,
            message=f"Há {int(mask.sum())} registro(s) com '{end_col}' anterior a '{start_col}'.",
            recommendation="Corrija a ordem temporal ou revise o cadastro da vigência.",
            affected_rows_count=int(mask.sum()),
            affected_rows_sample=_row_sample(df, mask),
        )
    ]


def check_bad_column_names(df: pd.DataFrame, audit_id: str) -> list[QualityIssue]:
    issues: list[QualityIssue] = []
    for col in df.columns:
        name = str(col).strip()
        lowered = name.lower()
        bad = (
            lowered in BAD_COLUMN_NAMES
            or lowered.startswith("unnamed")
            or re.fullmatch(r"col\d+", lowered)
            or name in {"...", "x", "y"}
        )
        if bad:
            issues.append(
                _issue(
                    audit_id,
                    column_name=name,
                    issue_type="bad_column_name",
                    dimension="documentation",
                    severity=Severity.WARNING,
                    message=f"Nome de coluna pouco descritivo: '{name}'.",
                    recommendation="Renomeie para um identificador semântico (ex.: codigo_municipio).",
                )
            )
    return issues


def run_all_checks(df: pd.DataFrame, audit_id: str) -> list[QualityIssue]:
    checks = [
        check_empty_columns,
        check_null_rates,
        check_empty_rows,
        check_duplicate_rows,
        check_duplicate_ids,
        check_invalid_dates,
        check_invalid_numbers,
        check_negative_quantities,
        check_invalid_uf,
        check_email_cep_cnpj,
        check_category_case_accent,
        check_mixed_types,
        check_future_dates,
        check_date_order_dependencies,
        check_bad_column_names,
    ]
    issues: list[QualityIssue] = []
    for fn in checks:
        issues.extend(fn(df, audit_id))
    return issues
