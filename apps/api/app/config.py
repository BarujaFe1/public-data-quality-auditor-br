"""Shared constants and configuration."""

from __future__ import annotations

import os
from pathlib import Path

# Project root: apps/api/app/config.py -> parents[3]
# In Docker, set PROJECT_ROOT / DEMO_DIR / AUDIT_OUTPUT_DIR explicitly.
_DEFAULT_ROOT = Path(__file__).resolve().parents[3]
PROJECT_ROOT = Path(os.environ.get("PROJECT_ROOT", _DEFAULT_ROOT))
DEMO_DIR = Path(os.environ.get("DEMO_DIR", PROJECT_ROOT / "data" / "demo"))
AUDIT_OUTPUT_DIR = Path(
    os.environ.get("AUDIT_OUTPUT_DIR", PROJECT_ROOT / "data" / "audit_outputs")
)

MAX_UPLOAD_BYTES = int(os.environ.get("MAX_UPLOAD_MB", "5")) * 1024 * 1024
MAX_ROWS = int(os.environ.get("MAX_ROWS", "50000"))
NULL_RATE_THRESHOLD = float(os.environ.get("NULL_RATE_THRESHOLD", "0.20"))
SAMPLE_SIZE = 5

VALID_UFS = {
    "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA",
    "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN",
    "RS", "RO", "RR", "SC", "SP", "SE", "TO",
}

DIMENSION_WEIGHTS = {
    "completeness": 25,
    "uniqueness": 20,
    "validity": 25,
    "consistency": 20,
    "documentation": 10,
}

DEMO_DATASETS = {
    "municipios": {
        "filename": "municipios_demo.csv",
        "title": "Municípios BR (demo)",
        "description": "Dataset sintético-realista de municípios com problemas intencionais de qualidade.",
        "kind": "synthetic",
    },
    "escolas": {
        "filename": "escolas_demo.csv",
        "title": "Escolas BR (demo)",
        "description": "Dataset sintético-realista de escolas com nulos, categorias inconsistentes e duplicidades.",
        "kind": "synthetic",
    },
    "contratos": {
        "filename": "contratos_demo.csv",
        "title": "Contratos públicos (demo)",
        "description": "Dataset sintético-realista de contratos com valores negativos, datas invertidas e CNPJ inválido.",
        "kind": "synthetic",
    },
    "ibge_municipios": {
        "filename": "ibge_municipios_amostra.csv",
        "title": "IBGE municípios (amostra pública)",
        "description": "Amostra curada de códigos oficiais IBGE com proveniência documentada (não é o dump completo).",
        "kind": "public_sample",
        "dir": "public",
    },
}

BAD_COLUMN_NAMES = {
    "col1", "col2", "col3", "x", "y", "z", "unnamed: 0", "unnamed:0",
    "...", "column1", "column2", "campo1", "campo2", "var1", "var2",
}

ID_HINTS = ("id", "codigo", "código", "cod_", "cnpj", "cpf", "chave")
QUANTITY_HINTS = (
    "valor", "preco", "preço", "quantidade", "qtd", "alunos", "populacao",
    "população", "area", "área", "matriculados",
)
DATE_HINTS = ("data", "date", "dt_", "inicio", "início", "fim", "censo", "atualizacao", "atualização")
UF_HINTS = ("uf", "estado", "sigla_uf")
EMAIL_HINTS = ("email", "e-mail", "mail")
CEP_HINTS = ("cep",)
CNPJ_HINTS = ("cnpj",)
