"""Regenerate UTF-8 lab snapshots from the quality engine (no live API required)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
API_ROOT = ROOT / "apps" / "api"
sys.path.insert(0, str(API_ROOT))

from app.config import DEMO_DATASETS  # noqa: E402
from app.services.audit_service import (  # noqa: E402
    _demo_path,
    _read_csv_bytes,
    audit_dataframe,
)

OUT = ROOT / "apps" / "web" / "src" / "lib" / "snapshots"

_MOJIBAKE_MARKERS = ("├", "┬", "Ã©", "Ã¡", "Ã£", "Â ")


def _write_utf8_json(path: Path, payload: object) -> str:
    text = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    path.write_text(text, encoding="utf-8", newline="\n")
    decoded = path.read_bytes().decode("utf-8")
    if decoded != text:
        raise SystemExit(f"UTF-8 round-trip mismatch for {path}")
    return decoded


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)

    for key, meta in DEMO_DATASETS.items():
        path = _demo_path(meta)
        if not path.exists():
            raise SystemExit(f"Missing demo file: {path}")
        content = path.read_bytes()
        df = _read_csv_bytes(content, meta["filename"])
        audit = audit_dataframe(
            df, dataset_name=meta["title"], filename=meta["filename"]
        )
        out_path = OUT / f"{key}.json"
        text = _write_utf8_json(out_path, audit.model_dump(mode="json"))

        if any(m in text for m in _MOJIBAKE_MARKERS):
            raise SystemExit(f"Mojibake detected in {out_path}")
        if key == "municipios":
            if "utilizável" not in text or "São Paulo" not in text:
                raise SystemExit(
                    f"Encoding check failed for {out_path}: "
                    "expected 'utilizável' and 'São Paulo'"
                )
        print(
            f"{key}: score={audit.overall_score} issues={len(audit.issues)} -> {out_path}"
        )


if __name__ == "__main__":
    main()
