"""Simple Frictionless-inspired datapackage descriptor."""

from __future__ import annotations

from typing import Any

from app.schemas.audit import AuditRun

TYPE_MAP = {
    "integer": "integer",
    "number": "number",
    "date": "date",
    "category": "string",
    "string": "string",
    "text": "string",
    "email": "string",
    "empty": "any",
}


def build_datapackage(audit: AuditRun) -> dict[str, Any]:
    fields = []
    for item in audit.data_dictionary:
        fields.append(
            {
                "name": item.column_name,
                "type": TYPE_MAP.get(item.inferred_type, "string"),
                "description": item.description_suggestion,
                "constraints": {"required": not item.nullable},
                "examples": item.example_values,
            }
        )

    return {
        "name": audit.dataset_name.lower().replace(" ", "-"),
        "title": audit.dataset_name,
        "description": (
            f"Descriptor gerado automaticamente pela auditoria {audit.id}. "
            "Revise tipos e descrições antes de publicar."
        ),
        "profile": "tabular-data-package",
        "resources": [
            {
                "name": audit.dataset_name.lower().replace(" ", "-"),
                "path": audit.uploaded_filename,
                "format": "csv",
                "mediatype": "text/csv",
                "schema": {
                    "fields": fields,
                },
                "dialect": {
                    "delimiter": ",",
                    "header": True,
                },
            }
        ],
        "licenses": [
            {
                "name": "UNKNOWN",
                "title": "Licença não informada no MVP",
                "path": "",
            }
        ],
        "contributors": [
            {
                "title": "Public Data Quality Auditor BR",
                "role": "author",
            }
        ],
    }
