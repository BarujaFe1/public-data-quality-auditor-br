"use client";

import clsx from "clsx";
import type { Severity } from "@/types/audit";

export function QualityScoreCard({
  score,
  label = "Score geral",
  size = "lg",
  criticalCount = 0,
  highCount = 0,
  recommendation,
}: {
  score: number;
  label?: string;
  size?: "lg" | "sm";
  criticalCount?: number;
  highCount?: number;
  recommendation?: string;
}) {
  const hasCritical = criticalCount > 0;
  const tone = hasCritical
    ? "text-clay"
    : score >= 85
      ? "text-forest"
      : score >= 70
        ? "text-ink"
        : score >= 50
          ? "text-clay"
          : "text-red-700";

  const blurb =
    recommendation?.trim() ||
    (hasCritical
      ? `Há ${criticalCount} issue(s) crítica(s)${highCount ? ` e ${highCount} alta(s)` : ""}. Trate antes de análises sensíveis.`
      : score >= 85
        ? "Boa para exploração com revisão pontual."
        : score >= 70
          ? "Utilizável com ressalvas."
          : score >= 50
            ? "Requer limpeza antes de uso crítico."
            : "Insuficiente para análise confiável.");

  return (
    <div
      className={clsx(
        "rounded-2xl border border-ink/10 bg-white/70 shadow-soft",
        size === "lg" ? "p-8" : "p-4"
      )}
    >
      <p className="text-xs uppercase tracking-[0.2em] text-slate">{label}</p>
      <p
        className={clsx(
          "font-display tabular-nums leading-none mt-3",
          tone,
          size === "lg" ? "text-7xl" : "text-4xl"
        )}
      >
        {score.toFixed(1)}
        <span className={clsx("text-slate/60", size === "lg" ? "text-2xl" : "text-lg")}>/100</span>
      </p>
      <p className="mt-4 text-sm text-slate leading-relaxed">{blurb}</p>
      {(criticalCount > 0 || highCount > 0) && (
        <p className="mt-2 text-xs text-slate">
          Severidade:{" "}
          <span className="font-medium text-ink">
            {criticalCount} critical · {highCount} high
          </span>
          . Score é diagnóstico, não certificação.
        </p>
      )}
    </div>
  );
}

export function countBySeverity(issues: { severity: Severity }[]) {
  return {
    critical: issues.filter((i) => i.severity === "critical").length,
    high: issues.filter((i) => i.severity === "high").length,
  };
}
