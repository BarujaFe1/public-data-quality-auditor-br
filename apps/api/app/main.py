"""Public Data Quality Auditor BR — FastAPI application."""

from __future__ import annotations

import os

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

_default_origins = (
    "http://localhost:3000,"
    "http://127.0.0.1:3000,"
    "https://public-data-quality-auditor-br.vercel.app"
)
_cors_origins = [
    o.strip()
    for o in os.environ.get("CORS_ORIGINS", _default_origins).split(",")
    if o.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "public-data-quality-auditor-br"}
