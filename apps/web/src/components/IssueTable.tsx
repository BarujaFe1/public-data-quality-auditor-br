"use client";

import clsx from "clsx";
import type { QualityIssue, Severity } from "@/types/audit";

const SEVERITY_STYLES: Record<Severity, string> = {
  critical: "bg-red-100 text-red-800",
  high: "bg-orange-100 text-orange-800",
  warning: "bg-amber-100 text-amber-900",
  info: "bg-sky-100 text-sky-800",
};

export function IssueTable({
  issues,
  severity,
  dimension,
  column,
  onSeverity,
  onDimension,
  onColumn,
}: {
  issues: QualityIssue[];
  severity: string;
  dimension: string;
  column: string;
  onSeverity: (v: string) => void;
  onDimension: (v: string) => void;
  onColumn: (v: string) => void;
}) {
  const columns = Array.from(
    new Set(issues.map((i) => i.column_name).filter(Boolean) as string[])
  ).sort();

  const filtered = issues.filter((issue) => {
    if (severity && issue.severity !== severity) return false;
    if (dimension && issue.dimension !== dimension) return false;
    if (column && issue.column_name !== column) return false;
    return true;
  });

  return (
    <div className="space-y-4">
      <div className="flex flex-wrap gap-3">
        <select
          className="rounded-xl border border-ink/15 bg-white px-3 py-2 text-sm"
          value={severity}
          onChange={(e) => onSeverity(e.target.value)}
        >
          <option value="">Todas severidades</option>
          <option value="critical">crítica</option>
          <option value="high">alta</option>
          <option value="warning">alerta</option>
          <option value="info">info</option>
        </select>
        <select
          className="rounded-xl border border-ink/15 bg-white px-3 py-2 text-sm"
          value={dimension}
          onChange={(e) => onDimension(e.target.value)}
        >
          <option value="">Todas dimensões</option>
          <option value="completeness">completude</option>
          <option value="uniqueness">unicidade</option>
          <option value="validity">validade</option>
          <option value="consistency">consistência</option>
          <option value="documentation">documentação</option>
        </select>
        <select
          className="rounded-xl border border-ink/15 bg-white px-3 py-2 text-sm"
          value={column}
          onChange={(e) => onColumn(e.target.value)}
        >
          <option value="">Todas colunas</option>
          {columns.map((c) => (
            <option key={c} value={c}>
              {c}
            </option>
          ))}
        </select>
      </div>

      <div className="overflow-x-auto rounded-2xl border border-ink/10 bg-white/80">
        <table className="min-w-full text-sm">
          <thead className="bg-sand/60 text-left text-xs uppercase tracking-wider text-slate">
            <tr>
              <th className="px-4 py-3">Severidade</th>
              <th className="px-4 py-3">Dimensão</th>
              <th className="px-4 py-3">Coluna</th>
              <th className="px-4 py-3">Problema</th>
              <th className="px-4 py-3">Linhas</th>
              <th className="px-4 py-3">Recomendação</th>
            </tr>
          </thead>
          <tbody>
            {filtered.map((issue) => (
              <tr key={issue.id} className="border-t border-ink/5 align-top">
                <td className="px-4 py-3">
                  <span
                    className={clsx(
                      "inline-flex rounded-full px-2.5 py-1 text-xs font-medium",
                      SEVERITY_STYLES[issue.severity]
                    )}
                  >
                    {issue.severity}
                  </span>
                </td>
                <td className="px-4 py-3 text-slate">{issue.dimension}</td>
                <td className="px-4 py-3 font-mono text-xs">{issue.column_name || "—"}</td>
                <td className="px-4 py-3 max-w-md">
                  <p className="font-medium text-ink">{issue.issue_type}</p>
                  <p className="mt-1 text-slate">{issue.message}</p>
                  {issue.affected_rows_sample?.length > 0 && (
                    <details className="mt-2">
                      <summary className="cursor-pointer text-xs text-forest">
                        Amostra de linhas
                      </summary>
                      <pre className="mt-2 max-h-40 overflow-auto rounded-lg bg-sand/50 p-2 text-[11px]">
                        {JSON.stringify(issue.affected_rows_sample, null, 2)}
                      </pre>
                    </details>
                  )}
                </td>
                <td className="px-4 py-3 tabular-nums">{issue.affected_rows_count}</td>
                <td className="px-4 py-3 max-w-xs text-slate">{issue.recommendation}</td>
              </tr>
            ))}
            {filtered.length === 0 && (
              <tr>
                <td colSpan={6} className="px-4 py-10 text-center text-slate">
                  Nenhum issue com os filtros atuais.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
