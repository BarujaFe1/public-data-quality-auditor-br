"use client";

import type { DataDictionaryField } from "@/types/audit";
import { useI18n } from "@/lib/i18n";

export function DataDictionaryTable({ fields }: { fields: DataDictionaryField[] }) {
  const { t } = useI18n();

  return (
    <div className="overflow-x-auto rounded-2xl border border-ink/10 bg-white/80">
      <table className="min-w-full text-sm">
        <thead className="bg-sand/60 text-left text-xs uppercase tracking-wider text-slate">
          <tr>
            <th className="px-4 py-3">{t("dict.field")}</th>
            <th className="px-4 py-3">{t("dict.type")}</th>
            <th className="px-4 py-3">{t("dict.nullable")}</th>
            <th className="px-4 py-3">{t("dict.description")}</th>
            <th className="px-4 py-3">{t("dict.examples")}</th>
            <th className="px-4 py-3">{t("dict.qualityNotes")}</th>
          </tr>
        </thead>
        <tbody>
          {fields.map((field) => (
            <tr key={field.id} className="border-t border-ink/5 align-top">
              <td className="px-4 py-3 font-mono text-xs">{field.column_name}</td>
              <td className="px-4 py-3">{field.inferred_type}</td>
              <td className="px-4 py-3">{field.nullable ? t("dict.yes") : t("dict.no")}</td>
              <td className="px-4 py-3 max-w-md text-slate">{field.description_suggestion}</td>
              <td className="px-4 py-3 max-w-xs text-xs text-slate">
                {field.example_values.map(String).join(", ") || "—"}
              </td>
              <td className="px-4 py-3 max-w-xs text-xs text-clay">
                {field.quality_notes || "—"}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
