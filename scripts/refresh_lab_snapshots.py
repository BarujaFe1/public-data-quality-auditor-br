"""Regenerate UTF-8 lab snapshots from the quality engine (no live API required)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
API_ROOT = ROOT / "apps" / "api"
sys.path.insert(0, str(API_ROOT))

from app.config import DEMO_DATASETS, DEMO_DIR  # noqa: E402
from app.services.audit_service import _read_csv_bytes, audit_dataframe  # noqa: E402

OUT = ROOT / "apps" / "web" / "src" / "lib" / "snapshots"


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for key, meta in DEMO_DATASETS.items():
        path = DEMO_DIR / meta["filename"]
        content = path.read_bytes()
        df = _read_csv_bytes(content, meta["filename"])
        # Avoid writing to audit_outputs during refresh: call engine via audit_dataframe
        # which saves — that's fine for local refresh.
        audit = audit_dataframe(df, dataset_name=meta["title"], filename=meta["filename"])
        out_path = OUT / f"{key}.json"
        payload = json.loads(audit.model_dump_json())
        out_path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        # Sanity: Portuguese accents must survive
        text = out_path.read_text(encoding="utf-8")
        if "Municípios" not in text and key == "municipios":
            raise SystemExit(f"Encoding check failed for {out_path}")
        if "├" in text or "┬" in text:
            raise SystemExit(f"Mojibake detected in {out_path}")
        print(
            f"{key}: score={audit.overall_score} issues={len(audit.issues)} -> {out_path}"
        )


if __name__ == "__main__":
    main()
