"""Pydantic schemas for audit results."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class Severity(str, Enum):
    INFO = "info"
    WARNING = "warning"
    HIGH = "high"
    CRITICAL = "critical"


class DimensionScores(BaseModel):
    completeness: float = Field(ge=0, le=100)
    uniqueness: float = Field(ge=0, le=100)
    validity: float = Field(ge=0, le=100)
    consistency: float = Field(ge=0, le=100)
    documentation: float = Field(ge=0, le=100)


class QualityIssue(BaseModel):
    id: str
    audit_run_id: str
    column_name: str | None = None
    issue_type: str
    dimension: str
    severity: Severity
    message: str
    affected_rows_count: int = 0
    affected_rows_sample: list[dict[str, Any]] = Field(default_factory=list)
    recommendation: str
    created_at: datetime


class ColumnProfile(BaseModel):
    id: str
    audit_run_id: str
    column_name: str
    inferred_type: str
    null_count: int
    null_rate: float
    distinct_count: int
    distinct_rate: float
    sample_values: list[Any] = Field(default_factory=list)
    min_value: Any | None = None
    max_value: Any | None = None
    most_common_values: list[dict[str, Any]] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)


class DataDictionaryField(BaseModel):
    id: str
    audit_run_id: str
    column_name: str
    inferred_type: str
    nullable: bool
    description_suggestion: str
    example_values: list[Any] = Field(default_factory=list)
    quality_notes: str = ""


class AuditRun(BaseModel):
    id: str
    dataset_name: str
    uploaded_filename: str
    row_count: int
    column_count: int
    overall_score: float
    completeness_score: float
    uniqueness_score: float
    validity_score: float
    consistency_score: float
    documentation_score: float
    created_at: datetime
    status: str = "completed"
    executive_recommendation: str = ""
    columns: list[ColumnProfile] = Field(default_factory=list)
    issues: list[QualityIssue] = Field(default_factory=list)
    data_dictionary: list[DataDictionaryField] = Field(default_factory=list)
    report_markdown: str = ""
    datapackage: dict[str, Any] = Field(default_factory=dict)


class AuditSummary(BaseModel):
    id: str
    dataset_name: str
    uploaded_filename: str
    row_count: int
    column_count: int
    overall_score: float
    dimensions: DimensionScores
    top_issues: list[QualityIssue]
    executive_recommendation: str
    created_at: datetime
    status: str
