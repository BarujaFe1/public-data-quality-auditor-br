"""API integration tests."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

API_ROOT = Path(__file__).resolve().parents[1]
if str(API_ROOT) not in sys.path:
    sys.path.insert(0, str(API_ROOT))

from app.main import app  # noqa: E402

client = TestClient(app)


def test_health():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"


def test_list_demos():
    res = client.get("/demos")
    assert res.status_code == 200
    data = res.json()
    assert len(data) >= 3
    ids = {d["id"] for d in data}
    assert {"municipios", "escolas", "contratos"} <= ids


def test_demo_audit_flow():
    res = client.post("/audit/demo/municipios")
    assert res.status_code == 200
    audit = res.json()
    audit_id = audit["id"]
    assert audit["overall_score"] is not None
    assert len(audit["issues"]) > 0

    summary = client.get(f"/audit/{audit_id}/summary")
    assert summary.status_code == 200
    assert "dimensions" in summary.json()

    columns = client.get(f"/audit/{audit_id}/columns")
    assert columns.status_code == 200
    assert len(columns.json()) == audit["column_count"]

    issues = client.get(f"/audit/{audit_id}/issues")
    assert issues.status_code == 200

    dictionary = client.get(f"/audit/{audit_id}/data-dictionary")
    assert dictionary.status_code == 200
    assert len(dictionary.json()) > 0

    report = client.get(f"/audit/{audit_id}/report")
    assert report.status_code == 200
    assert "Relatório de Qualidade" in report.text

    pkg = client.get(f"/audit/{audit_id}/datapackage.json")
    assert pkg.status_code == 200
    assert pkg.json()["resources"]


def test_upload_csv():
    content = (
        b"id_item,nome,uf,valor\n"
        b"1,Alpha,SP,10\n"
        b"1,Alpha,SP,10\n"
        b"2,Beta,XX,-5\n"
    )
    res = client.post(
        "/audit/upload",
        files={"file": ("amostra.csv", content, "text/csv")},
    )
    assert res.status_code == 200
    body = res.json()
    assert body["row_count"] == 3
    assert body["overall_score"] <= 100
