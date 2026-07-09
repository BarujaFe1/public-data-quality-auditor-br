"""Public Data Quality Auditor BR — FastAPI application."""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router

app = FastAPI(
    title="Public Data Quality Auditor BR",
    description=(
        "API para auditar qualidade de bases públicas brasileiras em CSV. "
        "Gera profiling, score por dimensão, issues, dicionário e datapackage."
    ),
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "public-data-quality-auditor-br"}
