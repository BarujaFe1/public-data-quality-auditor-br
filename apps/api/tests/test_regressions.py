"""Extra regression tests for CSV parsing and scoring honesty."""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

API_ROOT = Path(__file__).resolve().parents[1]
if str(API_ROOT) not in sys.path:
    sys.path.insert(0, str(API_ROOT))

from app.quality.engine import run_audit  # noqa: E402
from app.quality.scoring import executive_recommendation  # noqa: E402
from app.schemas.audit import QualityIssue, Severity  # noqa: E402
from app.services.audit_service import _read_csv_bytes  # noqa: E402
from datetime import datetime, timezone  # noqa: E402


def test_semicolon_csv_detects_multiple_columns():
    content = (
        "codigo_municipio;municipio;uf;populacao\n"
        "3550308;São Paulo;SP;100\n"
        "3304557;Rio de Janeiro;RJ;200\n"
    ).encode("utf-8")
    df = _read_csv_bytes(content, "semi.csv")
    assert df.shape[1] == 4
    assert list(df.columns) == ["codigo_municipio", "municipio", "uf", "populacao"]


def test_tab_csv_detects_multiple_columns():
    content = b"a\tb\tc\n1\t2\t3\n"
    df = _read_csv_bytes(content, "tabs.csv")
    assert df.shape[1] == 3


def test_executive_recommendation_flags_critical_even_if_score_high():
    issues = [
        QualityIssue(
            id="1",
            audit_run_id="a",
            column_name="id",
            issue_type="duplicate_id",
            dimension="uniqueness",
            severity=Severity.CRITICAL,
            message="dup",
            affected_rows_count=2,
            recommendation="fix",
            created_at=datetime.now(timezone.utc),
        )
    ]
    text = executive_recommendation(87.4, issues)
    assert "ressalvas" in text.lower() or "crítica" in text.lower() or "critica" in text.lower()


def test_municipios_demo_utf8_name():
    root = Path(__file__).resolve().parents[3]
    path = root / "data" / "demo" / "municipios_demo.csv"
    df = pd.read_csv(path, dtype=str)
    audit = run_audit(df, dataset_name="Municípios BR (demo)", uploaded_filename="municipios_demo.csv")
    assert "Municípios" in audit.dataset_name
    assert "São Paulo" in str(audit.columns[1].sample_values) or any(
        "São" in str(v) or "Sao" in str(v) for v in audit.columns[1].sample_values
    )


def test_ibge_public_sample_resolves_and_audits():
    from app.config import DEMO_DATASETS
    from app.services.audit_service import _demo_path, audit_demo

    meta = DEMO_DATASETS["ibge_municipios"]
    path = _demo_path(meta)
    assert path.exists()
    assert "public" in str(path).replace("\\", "/")
    audit = audit_demo("ibge_municipios")
    assert audit.row_count == 31
    assert audit.overall_score >= 0
    assert "IBGE" in audit.dataset_name
