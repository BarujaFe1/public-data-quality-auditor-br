export type Severity = "info" | "warning" | "high" | "critical";

export type DimensionScores = {
  completeness: number;
  uniqueness: number;
  validity: number;
  consistency: number;
  documentation: number;
};

export type QualityIssue = {
  id: string;
  audit_run_id: string;
  column_name: string | null;
  issue_type: string;
  dimension: string;
  severity: Severity;
  message: string;
  affected_rows_count: number;
  affected_rows_sample: Record<string, unknown>[];
  recommendation: string;
  created_at: string;
};

export type ColumnProfile = {
  id: string;
  audit_run_id: string;
  column_name: string;
  inferred_type: string;
  null_count: number;
  null_rate: number;
  distinct_count: number;
  distinct_rate: number;
  sample_values: unknown[];
  min_value: unknown;
  max_value: unknown;
  most_common_values: { value: string; count: number }[];
  warnings: string[];
};

export type DataDictionaryField = {
  id: string;
  audit_run_id: string;
  column_name: string;
  inferred_type: string;
  nullable: boolean;
  description_suggestion: string;
  example_values: unknown[];
  quality_notes: string;
};

export type AuditRun = {
  id: string;
  dataset_name: string;
  uploaded_filename: string;
  row_count: number;
  column_count: number;
  overall_score: number;
  completeness_score: number;
  uniqueness_score: number;
  validity_score: number;
  consistency_score: number;
  documentation_score: number;
  created_at: string;
  status: string;
  executive_recommendation: string;
  columns: ColumnProfile[];
  issues: QualityIssue[];
  data_dictionary: DataDictionaryField[];
  report_markdown: string;
  datapackage: Record<string, unknown>;
};

export type AuditSummary = {
  id: string;
  dataset_name: string;
  uploaded_filename: string;
  row_count: number;
  column_count: number;
  overall_score: number;
  dimensions: DimensionScores;
  top_issues: QualityIssue[];
  executive_recommendation: string;
  created_at: string;
  status: string;
};

export type DemoDataset = {
  id: string;
  title: string;
  description: string;
  filename: string;
  available: boolean;
  kind?: "synthetic" | "public_sample";
};
