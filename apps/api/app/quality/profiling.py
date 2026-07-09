"""Type inference and column profiling helpers."""

from __future__ import annotations

import re
import unicodedata
from typing import Any

import pandas as pd

from app.config import DATE_HINTS, EMAIL_HINTS, QUANTITY_HINTS, UF_HINTS


def normalize_text(value: str) -> str:
    """Lowercase and strip accents for category comparison."""
    text = str(value).strip().lower()
    normalized = unicodedata.normalize("NFKD", text)
    return "".join(ch for ch in normalized if not unicodedata.combining(ch))


def column_name_looks_like(column: str, hints: tuple[str, ...]) -> bool:
    name = normalize_text(column)
    return any(hint in name for hint in hints)


def is_nullish(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, float) and pd.isna(value):
        return True
    if isinstance(value, str) and value.strip() == "":
        return True
    return bool(pd.isna(value))


def try_parse_number(value: Any) -> float | None:
    if is_nullish(value):
        return None
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if pd.isna(value):
            return None
        return float(value)
    text = str(value).strip().replace(" ", "")
    if not text:
        return None
    # Brazilian decimal: 1.234,56
    if re.match(r"^-?\d{1,3}(\.\d{3})+(,\d+)?$", text):
        text = text.replace(".", "").replace(",", ".")
    else:
        text = text.replace(",", ".")
    try:
        return float(text)
    except ValueError:
        return None


def try_parse_date(value: Any) -> pd.Timestamp | None:
    if is_nullish(value):
        return None
    if isinstance(value, pd.Timestamp):
        return value if not pd.isna(value) else None
    text = str(value).strip()
    if not text:
        return None
    # Reject obviously invalid patterns early
    if re.search(r"[^\d/\-\s:T]", text) and not re.match(r"^\d{4}-\d{2}-\d{2}", text):
        # allow ISO; otherwise if letters present likely invalid
        if re.search(r"[A-Za-zÀ-ÿ]", text):
            return None
    parsed = pd.to_datetime(text, errors="coerce", dayfirst=False)
    if pd.isna(parsed):
        parsed = pd.to_datetime(text, errors="coerce", dayfirst=True)
    if pd.isna(parsed):
        return None
    return parsed


EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
CEP_RE = re.compile(r"^\d{5}-?\d{3}$")
CNPJ_DIGITS_RE = re.compile(r"^\d{14}$")


def is_valid_email(value: Any) -> bool:
    if is_nullish(value):
        return True
    return bool(EMAIL_RE.match(str(value).strip()))


def is_valid_cep(value: Any) -> bool:
    if is_nullish(value):
        return True
    return bool(CEP_RE.match(str(value).strip()))


def is_valid_cnpj_format(value: Any) -> bool:
    """Synthetic format check only (not full CNPJ algorithm)."""
    if is_nullish(value):
        return True
    digits = re.sub(r"\D", "", str(value))
    if not CNPJ_DIGITS_RE.match(digits):
        return False
    if digits == digits[0] * 14:
        return False
    return True


def infer_series_type(series: pd.Series, column_name: str) -> str:
    non_null = series.dropna()
    if non_null.empty:
        return "empty"

    # Prefer hint-based date detection
    if column_name_looks_like(column_name, DATE_HINTS):
        parsed = non_null.map(try_parse_date)
        ok = parsed.notna().mean()
        if ok >= 0.7:
            return "date"

    if column_name_looks_like(column_name, UF_HINTS):
        return "category"

    if column_name_looks_like(column_name, EMAIL_HINTS):
        return "email"

    sample = non_null.head(200)
    numeric_ok = sample.map(lambda v: try_parse_number(v) is not None).mean()
    date_ok = sample.map(lambda v: try_parse_date(v) is not None).mean()

    if numeric_ok >= 0.85:
        # integer-like?
        nums = [try_parse_number(v) for v in sample if try_parse_number(v) is not None]
        if nums and all(float(n).is_integer() for n in nums):
            return "integer"
        return "number"

    if date_ok >= 0.85:
        return "date"

    distinct_rate = non_null.nunique(dropna=True) / max(len(non_null), 1)
    if distinct_rate <= 0.2 and non_null.nunique(dropna=True) <= 50:
        return "category"

    avg_len = non_null.astype(str).str.len().mean()
    if avg_len > 40:
        return "text"
    return "string"


def detect_mixed_types(series: pd.Series) -> bool:
    """True when non-null values mix numeric and non-numeric strings."""
    non_null = series.dropna()
    if len(non_null) < 3:
        return False
    kinds: set[str] = set()
    for value in non_null.head(300):
        if try_parse_number(value) is not None and not isinstance(value, bool):
            # pure numeric string or number
            text = str(value).strip()
            if re.fullmatch(r"-?\d+([.,]\d+)?", text.replace(" ", "")) or isinstance(value, (int, float)):
                kinds.add("number")
            else:
                kinds.add("string")
        else:
            kinds.add("string")
        if len(kinds) > 1:
            return True
    return False


def serialize_value(value: Any) -> Any:
    if is_nullish(value):
        return None
    if isinstance(value, pd.Timestamp):
        return value.isoformat()
    if hasattr(value, "item"):
        try:
            return value.item()
        except Exception:
            return str(value)
    if isinstance(value, (int, float, str, bool)):
        return value
    return str(value)
