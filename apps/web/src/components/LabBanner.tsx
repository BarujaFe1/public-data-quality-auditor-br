import { IS_LAB } from "@/lib/api";

export function LabBanner() {
  if (!IS_LAB) return null;
  return (
    <div className="border-b border-forest/25 bg-forest/10 text-ink">
      <div className="mx-auto max-w-6xl px-4 py-2.5 text-sm leading-snug">
        <span className="font-medium text-forest">Lab / portfolio demo</span>
        <span className="text-slate">
          {" "}
          — snapshots sintéticos (municípios, escolas, contratos). Score é diagnóstico
          explicável, não certificação. Upload CSV e API live exigem stack local com{" "}
          <code className="rounded bg-white/70 px-1 text-xs">NEXT_PUBLIC_USE_API=true</code>.
        </span>
      </div>
    </div>
  );
}
