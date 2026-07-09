"""API routes for audits."""

from __future__ import annotations

from fastapi import APIRouter, File, HTTPException, Query, UploadFile
from fastapi.responses import JSONResponse, PlainTextResponse

from app.schemas.audit import AuditRun, AuditSummary, DimensionScores, Severity
from app.services import audit_service
from app.services.store import get_audit

router = APIRouter()


def _get_or_404(audit_id: str) -> AuditRun:
    audit = get_audit(audit_id)
    if not audit:
        raise HTTPException(status_code=404, detail=f"Auditoria '{audit_id}' não encontrada.")
    return audit


@router.get("/demos")
def list_demos() -> list[dict]:
    return audit_service.list_demos()


@router.post("/audit/upload", response_model=AuditRun)
async def upload_audit(file: UploadFile = File(...)) -> AuditRun:
    return await audit_service.audit_upload(file)


@router.post("/audit/demo/{dataset_name}", response_model=AuditRun)
def demo_audit(dataset_name: str) -> AuditRun:
    return audit_service.audit_demo(dataset_name)


@router.get("/audit/{audit_id}", response_model=AuditRun)
def get_full_audit(audit_id: str) -> AuditRun:
    return _get_or_404(audit_id)


@router.get("/audit/{audit_id}/summary", response_model=AuditSummary)
def get_summary(audit_id: str) -> AuditSummary:
    audit = _get_or_404(audit_id)
    severity_rank = {
        Severity.CRITICAL: 0,
        Severity.HIGH: 1,
        Severity.WARNING: 2,
        Severity.INFO: 3,
    }
    top = sorted(
        audit.issues,
        key=lambda i: (severity_rank.get(i.severity, 9), -i.affected_rows_count),
    )[:8]
    return AuditSummary(
        id=audit.id,
        dataset_name=audit.dataset_name,
        uploaded_filename=audit.uploaded_filename,
        row_count=audit.row_count,
        column_count=audit.column_count,
        overall_score=audit.overall_score,
        dimensions=DimensionScores(
            completeness=audit.completeness_score,
            uniqueness=audit.uniqueness_score,
            validity=audit.validity_score,
            consistency=audit.consistency_score,
            documentation=audit.documentation_score,
        ),
        top_issues=top,
        executive_recommendation=audit.executive_recommendation,
        created_at=audit.created_at,
        status=audit.status,
    )


@router.get("/audit/{audit_id}/columns")
def get_columns(audit_id: str):
    return _get_or_404(audit_id).columns


@router.get("/audit/{audit_id}/issues")
def get_issues(
    audit_id: str,
    severity: str | None = Query(default=None),
    dimension: str | None = Query(default=None),
    column: str | None = Query(default=None),
):
    issues = _get_or_404(audit_id).issues
    if severity:
        issues = [i for i in issues if i.severity.value == severity.lower()]
    if dimension:
        issues = [i for i in issues if i.dimension == dimension.lower()]
    if column:
        issues = [i for i in issues if (i.column_name or "") == column]
    return issues


@router.get("/audit/{audit_id}/data-dictionary")
def get_dictionary(audit_id: str):
    return _get_or_404(audit_id).data_dictionary


@router.get("/audit/{audit_id}/report")
def get_report(audit_id: str, format: str = Query(default="markdown")):
    audit = _get_or_404(audit_id)
    if format.lower() in {"md", "markdown", "text"}:
        return PlainTextResponse(audit.report_markdown, media_type="text/markdown; charset=utf-8")
    if format.lower() == "html":
        html = (
            "<!DOCTYPE html><html><head><meta charset='utf-8'>"
            f"<title>Relatório — {audit.dataset_name}</title>"
            "<style>body{font-family:Georgia,serif;max-width:900px;margin:2rem auto;padding:0 1rem;"
            "line-height:1.5;color:#1a1a1a;background:#f7f4ef}"
            "pre{white-space:pre-wrap;background:#fff;padding:1.5rem;border:1px solid #ddd}</style>"
            "</head><body><pre>"
            + audit.report_markdown.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            + "</pre></body></html>"
        )
        return PlainTextResponse(html, media_type="text/html; charset=utf-8")
    raise HTTPException(status_code=400, detail="format deve ser markdown ou html")


@router.get("/audit/{audit_id}/datapackage.json")
def get_datapackage(audit_id: str):
    audit = _get_or_404(audit_id)
    return JSONResponse(audit.datapackage)
