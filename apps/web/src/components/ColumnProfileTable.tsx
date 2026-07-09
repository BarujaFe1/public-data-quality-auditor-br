"use client";

import type { ColumnProfile } from "@/types/audit";

export function ColumnProfileTable({ columns }: { columns: ColumnProfile[] }) {
  return (
    <div className="overflow-x-auto rounded-2xl border border-ink/10 bg-white/80">
      <table className="min-w-full text-sm">
        <thead className="bg-sand/60 text-left text-xs uppercase tracking-wider text-slate">
          <tr>
            <th className="px-4 py-3">Coluna</th>
            <th className="px-4 py-3">Tipo</th>
            <th className="px-4 py-3">Nulos</th>
            <th className="px-4 py-3">Distintos</th>
            <th className="px-4 py-3">Min / Max</th>
            <th className="px-4 py-3">Exemplos</th>
            <th className="px-4 py-3">Warnings</th>
          </tr>
        </thead>
        <tbody>
          {columns.map((col) => (
            <tr key={col.id} className="border-t border-ink/5 align-top">
              <td className="px-4 py-3 font-mono text-xs">{col.column_name}</td>
              <td className="px-4 py-3">{col.inferred_type}</td>
              <td className="px-4 py-3 tabular-nums">
                {col.null_count} ({(col.null_rate * 100).toFixed(1)}%)
              </td>
              <td className="px-4 py-3 tabular-nums">
                {col.distinct_count} ({(col.distinct_rate * 100).toFixed(1)}%)
              </td>
              <td className="px-4 py-3 text-xs text-slate">
                {col.min_value != null || col.max_value != null
                  ? `${String(col.min_value ?? "—")} → ${String(col.max_value ?? "—")}`
                  : "—"}
              </td>
              <td className="px-4 py-3 max-w-xs text-xs text-slate">
                {col.sample_values.map(String).join(", ") || "—"}
              </td>
              <td className="px-4 py-3 text-xs text-clay">
                {col.warnings.length ? col.warnings.join("; ") : "—"}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
