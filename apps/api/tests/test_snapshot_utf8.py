"""Smoke: lab snapshots must be valid UTF-8 without CP850 mojibake."""

from __future__ import annotations

import json
from pathlib import Path

SNAPSHOTS = Path(__file__).resolve().parents[2] / "web" / "src" / "lib" / "snapshots"
_MOJIBAKE = (chr(0x251C), "Ã©", "Â ")


def test_snapshots_are_utf8_without_mojibake() -> None:
    files = sorted(SNAPSHOTS.glob("*.json"))
    assert files, f"No snapshots in {SNAPSHOTS}"
    for path in files:
        text = path.read_bytes().decode("utf-8")
        json.loads(text)
        for marker in _MOJIBAKE:
            assert marker not in text, f"Mojibake {marker!r} in {path.name}"
        if path.name == "municipios.json":
            assert "utilizável" in text
            assert "São Paulo" in text
