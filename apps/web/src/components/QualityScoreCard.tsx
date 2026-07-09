"use client";

import clsx from "clsx";

export function QualityScoreCard({
  score,
  label = "Score geral",
  size = "lg",
}: {
  score: number;
  label?: string;
  size?: "lg" | "sm";
}) {
  const tone =
    score >= 85 ? "text-forest" : score >= 70 ? "text-ink" : score >= 50 ? "text-clay" : "text-red-700";

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
      <p className="mt-4 text-sm text-slate">
        {score >= 85
          ? "Boa para exploração com revisão pontual."
          : score >= 70
            ? "Utilizável com ressalvas."
            : score >= 50
              ? "Requer limpeza antes de uso crítico."
              : "Insuficiente para análise confiável."}
      </p>
    </div>
  );
}
