"""Quality engine unit tests."""

from __future__ import annotations

import io
import sys
from pathlib import Path

import pandas as pd
import pytest

API_ROOT = Path(__file__).resolve().parents[1]
if str(API_ROOT) not in sys.path:
    sys.path.insert(0, str(API_ROOT))

from app.quality.checks import (  # noqa: E402
    check_bad_column_names,
    check_category_case_accent,
    check_duplicate_ids,
    check_duplicate_rows,
    check_empty_columns,
    check_empty_rows,
    check_invalid_dates,
    check_invalid_numbers,
    check_null_rates,
)
from app.quality.engine import build_data_dictionary, profile_columns, run_audit  # noqa: E402
from app.quality.scoring import compute_all_scores, score_dimension  # noqa: E402
from app.reports.datapackage import build_datapackage  # noqa: E402
from app.reports.markdown_report import build_markdown_report  # noqa: E402
from app.schemas.audit import QualityIssue, Severity  # noqa: E402
from datetime import datetime, timezone  # noqa: E402


def _issue(dimension: str, severity: Severity, rows: int = 0) -> QualityIssue:
    return QualityIssue(
        id="x",
        audit_run_id="a",
        column_name="c",
        issue_type="t",
        dimension=dimension,
        severity=severity,
        message="m",
        affected_rows_count=rows,
        recommendation="r",
        created_at=datetime.now(timezone.utc),
    )


def test_detect_nulls_and_empty_column():
    df = pd.DataFrame({"a": [1, None, 3], "b": [None, None, None]})
    empty = check_empty_columns(df, "audit1")
    assert any(i.issue_type == "empty_column" and i.column_name == "b" for i in empty)

    nulls = check_null_rates(df, "audit1", threshold=0.2)
    assert any(i.issue_type == "high_null_rate" and i.column_name == "a" for i in nulls)


def test_empty_rows():
    df = pd.DataFrame({"a": [1, None], "b": [2, None]})
    issues = check_empty_rows(df, "audit1")
    assert len(issues) == 1
    assert issues[0].affected_rows_count == 1


def test_duplicate_rows():
    df = pd.DataFrame({"id": [1, 1, 2], "name": ["a", "a", "b"]})
    issues = check_duplicate_rows(df, "audit1")
    assert len(issues) == 1
    assert issues[0].affected_rows_count == 2


def test_duplicate_id():
    df = pd.DataFrame({"id_escola": ["A", "A", "B"], "nome": ["x", "y", "z"]})
    issues = check_duplicate_ids(df, "audit1")
    assert any(i.issue_type == "duplicate_id" for i in issues)


def test_invalid_date():
    df = pd.DataFrame({"data_atualizacao": ["2024-01-01", "não-é-data", "2023-13-40"]})
    issues = check_invalid_dates(df, "audit1")
    assert any(i.issue_type == "invalid_date" for i in issues)
    assert issues[0].affected_rows_count >= 2


def test_invalid_number():
    df = pd.DataFrame({"alunos_matriculados": ["10", "abc", "30"]})
    issues = check_invalid_numbers(df, "audit1")
    assert any(i.issue_type == "invalid_number" for i in issues)
    assert issues[0].affected_rows_count == 1


def test_inconsistent_category():
    df = pd.DataFrame({"rede": ["Municipal", "municipal", "Municipal", "Estadual", "ESTADUAL"]})
    issues = check_category_case_accent(df, "audit1")
    assert any(i.issue_type == "inconsistent_category" for i in issues)


def test_completeness_score_penalizes_nulls():
    issues = [
        _issue("completeness", Severity.HIGH, rows=20),
        _issue("completeness", Severity.CRITICAL, rows=5),
    ]
    score = score_dimension(issues, "completeness")
    assert score < 100
    assert score >= 0


def test_overall_score_weighted():
    issues = [
        _issue("completeness", Severity.WARNING, rows=5),
        _issue("validity", Severity.HIGH, rows=10),
    ]
    scores = compute_all_scores(issues)
    assert "overall" in scores
    assert 0 <= scores["overall"] <= 100
    assert scores["uniqueness"] == 100


def test_dictionary_generation():
    df = pd.DataFrame({"municipio": ["São Paulo", "Recife"], "uf": ["SP", "PE"]})
    audit = run_audit(df, dataset_name="teste", uploaded_filename="teste.csv")
    assert len(audit.data_dictionary) == 2
    assert all(f.description_suggestion for f in audit.data_dictionary)


def test_report_generation():
    df = pd.DataFrame(
        {
            "id_contrato": ["1", "1"],
            "valor_contrato": ["100", "-50"],
            "data_inicio": ["2024-01-01", "2024-06-01"],
            "data_fim": ["2024-12-01", "2024-01-01"],
        }
    )
    audit = run_audit(df, dataset_name="contratos", uploaded_filename="c.csv")
    report = build_markdown_report(audit)
    assert "Relatório de Qualidade" in report
    assert "Score geral" in report
    assert audit.overall_score >= 0


def test_datapackage_generation():
    df = pd.DataFrame({"codigo_municipio": ["1", "2"], "municipio": ["A", "B"]})
    audit = run_audit(df, dataset_name="Municipios Demo", uploaded_filename="m.csv")
    pkg = build_datapackage(audit)
    assert pkg["profile"] == "tabular-data-package"
    assert pkg["resources"][0]["schema"]["fields"]
    assert pkg["resources"][0]["format"] == "csv"


def test_bad_column_names():
    df = pd.DataFrame({"Unnamed: 0": [1, 2], "col1": [3, 4]})
    issues = check_bad_column_names(df, "audit1")
    assert len(issues) >= 2


def test_demo_municipios_end_to_end():
    root = Path(__file__).resolve().parents[3]
    path = root / "data" / "demo" / "municipios_demo.csv"
    df = pd.read_csv(path, dtype=str)
    audit = run_audit(df, dataset_name="Municípios", uploaded_filename="municipios_demo.csv")
    assert audit.row_count > 0
    assert audit.column_count == 6
    assert len(audit.issues) > 0
    assert audit.report_markdown
    assert audit.datapackage["resources"]
