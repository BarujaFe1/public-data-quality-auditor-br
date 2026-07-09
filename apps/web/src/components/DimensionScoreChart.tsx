"use client";

import {
  Bar,
  BarChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
  Cell,
} from "recharts";
import type { DimensionScores } from "@/types/audit";

const LABELS: Record<keyof DimensionScores, string> = {
  completeness: "Completude",
  uniqueness: "Unicidade",
  validity: "Validade",
  consistency: "Consistência",
  documentation: "Documentação",
};

function barColor(value: number) {
  if (value >= 85) return "#1f6f5b";
  if (value >= 70) return "#14213d";
  if (value >= 50) return "#c45c26";
  return "#b91c1c";
}

export function DimensionScoreChart({ dimensions }: { dimensions: DimensionScores }) {
  const data = (Object.keys(LABELS) as (keyof DimensionScores)[]).map((key) => ({
    name: LABELS[key],
    score: dimensions[key],
  }));

  return (
    <div className="rounded-2xl border border-ink/10 bg-white/70 p-6 shadow-soft h-80">
      <p className="text-xs uppercase tracking-[0.2em] text-slate mb-4">Scores por dimensão</p>
      <ResponsiveContainer width="100%" height="85%">
        <BarChart data={data} margin={{ top: 8, right: 8, left: -12, bottom: 0 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#d6d0c4" />
          <XAxis dataKey="name" tick={{ fill: "#4a5568", fontSize: 12 }} />
          <YAxis domain={[0, 100]} tick={{ fill: "#4a5568", fontSize: 12 }} />
          <Tooltip
            contentStyle={{
              background: "#f4efe6",
              border: "1px solid #d6d0c4",
              borderRadius: 12,
            }}
          />
          <Bar dataKey="score" radius={[8, 8, 0, 0]}>
            {data.map((entry) => (
              <Cell key={entry.name} fill={barColor(entry.score)} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
