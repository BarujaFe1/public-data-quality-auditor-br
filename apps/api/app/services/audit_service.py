"""CSV loading and audit orchestration service."""

from __future__ import annotations

import io
from pathlib import Path

import pandas as pd
from fastapi import HTTPException, UploadFile

from app.config import DEMO_DATASETS, DEMO_DIR, MAX_ROWS, MAX_UPLOAD_BYTES
from app.quality.engine import run_audit
from app.schemas.audit import AuditRun
from app.services.store import save_audit


def _candidate_score(df: pd.DataFrame) -> tuple[int, int]:
    """Prefer parses with more columns, then more non-empty rows."""
    cols = int(df.shape[1])
    rows = int(df.dropna(how="all").shape[0]) if cols else 0
    return cols, rows


def _read_csv_bytes(content: bytes, filename: str) -> pd.DataFrame:
    if not content:
        raise HTTPException(status_code=400, detail="Arquivo CSV vazio.")
    if len(content) > MAX_UPLOAD_BYTES:
        raise HTTPException(
            status_code=400,
            detail=f"Arquivo excede o limite de {MAX_UPLOAD_BYTES // (1024 * 1024)} MB.",
        )

    last_error: Exception | None = None
    best: pd.DataFrame | None = None
    best_score = (-1, -1)

    for encoding in ("utf-8-sig", "utf-8", "latin-1", "cp1252"):
        for sep in (",", ";", "\t"):
            try:
                df = pd.read_csv(
                    io.BytesIO(content),
                    encoding=encoding,
                    sep=sep,
                    dtype=str,
                    keep_default_na=True,
                    na_values=["", "NA", "N/A", "null", "None", "nan"],
                    on_bad_lines="skip",
                    engine="python",
                )
                if df.shape[1] == 0:
                    continue
                score = _candidate_score(df)
                # Never accept a 1-column parse when another sep yields more columns
                if score > best_score:
                    best = df
                    best_score = score
            except Exception as exc:  # noqa: BLE001
                last_error = exc
                continue

    if best is not None and best_score[0] >= 1:
        return best

    raise HTTPException(
        status_code=400,
        detail=(
            f"Não foi possível ler o CSV '{filename}'. "
            f"Verifique encoding/separador. Erro: {last_error}"
        ),
    )


def _validate_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty and len(df.columns) == 0:
        raise HTTPException(status_code=400, detail="CSV sem colunas detectáveis.")
    if len(df) > MAX_ROWS:
        raise HTTPException(
            status_code=400,
            detail=(
                f"CSV excede o limite de {MAX_ROWS} linhas no MVP. "
                "Filtre ou amostragem antes do upload."
            ),
        )
    df = df.copy()
    df.columns = [str(c).strip() for c in df.columns]
    return df


def audit_dataframe(df: pd.DataFrame, dataset_name: str, filename: str) -> AuditRun:
    df = _validate_dataframe(df)
    audit = run_audit(df, dataset_name=dataset_name, uploaded_filename=filename)
    return save_audit(audit)


async def audit_upload(file: UploadFile) -> AuditRun:
    if not file.filename:
        raise HTTPException(status_code=400, detail="Nome de arquivo ausente.")
    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Apenas arquivos .csv são aceitos no MVP.")

    content = await file.read()
    df = _read_csv_bytes(content, file.filename)
    name = Path(file.filename).stem
    return audit_dataframe(df, dataset_name=name, filename=file.filename)


def audit_demo(dataset_name: str) -> AuditRun:
    meta = DEMO_DATASETS.get(dataset_name)
    if not meta:
        raise HTTPException(
            status_code=404,
            detail=f"Dataset demo '{dataset_name}' não encontrado. Opções: {list(DEMO_DATASETS)}",
        )
    path = DEMO_DIR / meta["filename"]
    if not path.exists():
        raise HTTPException(status_code=500, detail=f"Arquivo demo ausente: {path}")
    content = path.read_bytes()
    df = _read_csv_bytes(content, meta["filename"])
    return audit_dataframe(df, dataset_name=meta["title"], filename=meta["filename"])


def list_demos() -> list[dict]:
    items = []
    for key, meta in DEMO_DATASETS.items():
        path = DEMO_DIR / meta["filename"]
        items.append(
            {
                "id": key,
                "title": meta["title"],
                "description": meta["description"],
                "filename": meta["filename"],
                "available": path.exists(),
            }
        )
    return items
