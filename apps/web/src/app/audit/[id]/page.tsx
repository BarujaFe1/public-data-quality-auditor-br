"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useParams } from "next/navigation";
import { api } from "@/lib/api";
import type { AuditRun } from "@/types/audit";
import { QualityScoreCard, countBySeverity } from "@/components/QualityScoreCard";
import { DimensionScoreChart } from "@/components/DimensionScoreChart";
import { IssueTable } from "@/components/IssueTable";
import { ColumnProfileTable } from "@/components/ColumnProfileTable";
import { DataDictionaryTable } from "@/components/DataDictionaryTable";
import {
  ErrorState,
  MethodologyCallout,
  RecommendationPanel,
  ReportExportButton,
} from "@/components/panels";
import type { Severity } from "@/types/audit";

type Tab = "summary" | "columns" | "issues" | "dictionary";

const SEVERITY_RANK: Record<Severity, number> = {
  critical: 0,
  high: 1,
  warning: 2,
  info: 3,
};

export default function AuditDetailPage() {
  const params = useParams<{ id: string }>();
  const auditId = params.id;
  const [audit, setAudit] = useState<AuditRun | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [tab, setTab] = useState<Tab>("summary");
  const [severity, setSeverity] = useState("");
  const [dimension, setDimension] = useState("");
  const [column, setColumn] = useState("");

  useEffect(() => {
    if (!auditId) return;
    api
      .getAudit(auditId)
      .then(setAudit)
      .catch((err: Error) => setError(err.message));
  }, [auditId]);

  if (error) {
    return (
      <div className="mx-auto max-w-6xl px-4 py-12">
        <ErrorState message={error} />
      </div>
    );
  }

  if (!audit) {
    return (
      <div className="mx-auto max-w-6xl px-4 py-12 text-slate">Carregando auditoria…</div>
    );
  }

  const dimensions = {
    completeness: audit.completeness_score,
    uniqueness: audit.uniqueness_score,
    validity: audit.validity_score,
    consistency: audit.consistency_score,
    documentation: audit.documentation_score,
  };

  const tabs: { id: Tab; label: string }[] = [
    { id: "summary", label: "Resumo" },
    { id: "columns", label: "Colunas" },
    { id: "issues", label: "Issues" },
    { id: "dictionary", label: "Dicionário" },
  ];

  const severityCounts = countBySeverity(audit.issues);
  const topIssues = [...audit.issues]
    .sort(
      (a, b) =>
        (SEVERITY_RANK[a.severity] ?? 9) - (SEVERITY_RANK[b.severity] ?? 9) ||
        b.affected_rows_count - a.affected_rows_count
    )
    .slice(0, 6);

  return (
    <div className="mx-auto max-w-6xl px-4 py-10 space-y-8">
      <div className="flex flex-wrap items-end justify-between gap-4 animate-rise">
        <div>
          <p className="text-xs uppercase tracking-[0.2em] text-slate">Auditoria</p>
          <h1 className="font-display text-4xl text-ink mt-1">{audit.dataset_name}</h1>
          <p className="mt-2 text-sm text-slate">
            {audit.uploaded_filename} · {audit.row_count} linhas · {audit.column_count} colunas ·{" "}
            {new Date(audit.created_at).toLocaleString("pt-BR")}
          </p>
        </div>
        <Link href="/audit" className="text-sm text-forest hover:underline">
          Nova auditoria
        </Link>
      </div>

      <div className="flex flex-wrap gap-2 border-b border-ink/10 pb-3">
        {tabs.map((item) => (
          <button
            key={item.id}
            type="button"
            data-testid={`tab-${item.id}`}
            onClick={() => setTab(item.id)}
            className={
              tab === item.id
                ? "rounded-full bg-ink px-4 py-2 text-sm text-paper"
                : "rounded-full px-4 py-2 text-sm text-slate hover:text-ink"
            }
          >
            {item.label}
          </button>
        ))}
      </div>

      {tab === "summary" && (
        <div className="space-y-6 animate-rise">
          <div className="grid lg:grid-cols-[280px_1fr] gap-6">
            <div className="animate-score">
              <QualityScoreCard
                score={audit.overall_score}
                criticalCount={severityCounts.critical}
                highCount={severityCounts.high}
                recommendation={audit.executive_recommendation}
              />
            </div>
            <DimensionScoreChart dimensions={dimensions} />
          </div>
          <RecommendationPanel text={audit.executive_recommendation} />
          <MethodologyCallout />
          <div>
            <h2 className="font-display text-2xl text-ink mb-3">Principais problemas</h2>
            <ul className="space-y-3">
              {topIssues.map((issue) => (
                <li
                  key={issue.id}
                  className="rounded-xl border border-ink/10 bg-white/70 px-4 py-3 text-sm"
                >
                  <span className="font-medium text-ink">[{issue.severity}]</span>{" "}
                  {issue.message}
                </li>
              ))}
            </ul>
          </div>
          <ReportExportButton
            auditId={audit.id}
            reportMarkdown={audit.report_markdown}
            datapackage={audit.datapackage}
          />
        </div>
      )}

      {tab === "columns" && <ColumnProfileTable columns={audit.columns} />}

      {tab === "issues" && (
        <IssueTable
          issues={audit.issues}
          severity={severity}
          dimension={dimension}
          column={column}
          onSeverity={setSeverity}
          onDimension={setDimension}
          onColumn={setColumn}
        />
      )}

      {tab === "dictionary" && <DataDictionaryTable fields={audit.data_dictionary} />}
    </div>
  );
}
