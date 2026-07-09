"""In-memory audit store with optional JSON persistence."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from app.config import AUDIT_OUTPUT_DIR
from app.schemas.audit import AuditRun

_STORE: dict[str, AuditRun] = {}


def save_audit(audit: AuditRun) -> AuditRun:
    AUDIT_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    _STORE[audit.id] = audit
    path = AUDIT_OUTPUT_DIR / f"{audit.id}.json"
    path.write_text(audit.model_dump_json(indent=2), encoding="utf-8")
    # also write report and datapackage side files
    (AUDIT_OUTPUT_DIR / f"{audit.id}_report.md").write_text(
        audit.report_markdown, encoding="utf-8"
    )
    (AUDIT_OUTPUT_DIR / f"{audit.id}_datapackage.json").write_text(
        json.dumps(audit.datapackage, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return audit


def get_audit(audit_id: str) -> AuditRun | None:
    if audit_id in _STORE:
        return _STORE[audit_id]
    path = AUDIT_OUTPUT_DIR / f"{audit_id}.json"
    if path.exists():
        data = json.loads(path.read_text(encoding="utf-8"))
        audit = AuditRun.model_validate(data)
        _STORE[audit_id] = audit
        return audit
    return None


def list_audit_ids() -> list[str]:
    AUDIT_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    ids = set(_STORE.keys())
    for path in AUDIT_OUTPUT_DIR.glob("*.json"):
        if path.name.endswith("_datapackage.json"):
            continue
        ids.add(path.stem)
    return sorted(ids)
