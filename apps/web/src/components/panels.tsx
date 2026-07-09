"use client";

import { API_BASE, IS_LAB } from "@/lib/api";

export function RecommendationPanel({ text }: { text: string }) {
  return (
    <aside className="rounded-2xl border border-forest/20 bg-forest/5 p-6 shadow-soft">
      <p className="text-xs uppercase tracking-[0.2em] text-forest">Recomendação executiva</p>
      <p className="mt-3 font-display text-xl leading-snug text-ink">{text}</p>
    </aside>
  );
}

export function MethodologyCallout() {
  return (
    <div className="rounded-2xl border border-ink/10 bg-sand/40 p-5 text-sm text-slate leading-relaxed">
      <p className="font-medium text-ink">Como ler o score</p>
      <p className="mt-2">
        Completude (25), Unicidade (20), Validade (25), Consistência (20) e Documentabilidade (10)
        formam o score 0–100. Penalidades vêm de issues por severidade. O resultado é diagnóstico —
        não certifica verdade factual nem conformidade legal.
      </p>
    </div>
  );
}

export function EmptyState({ title, body }: { title: string; body: string }) {
  return (
    <div className="rounded-2xl border border-dashed border-ink/20 bg-white/50 px-6 py-16 text-center">
      <p className="font-display text-2xl text-ink">{title}</p>
      <p className="mt-2 text-slate">{body}</p>
    </div>
  );
}

export function ErrorState({ message }: { message: string }) {
  return (
    <div className="rounded-2xl border border-red-200 bg-red-50 px-5 py-4 text-sm text-red-800">
      {message}
    </div>
  );
}

export function ReportExportButton({
  auditId,
  reportMarkdown,
  datapackage,
}: {
  auditId: string;
  reportMarkdown: string;
  datapackage?: Record<string, unknown>;
}) {
  const download = (filename: string, content: string, type: string) => {
    const blob = new Blob([content], { type });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    a.click();
    URL.revokeObjectURL(url);
  };

  const openHtml = () => {
    const html = `<!DOCTYPE html><html><head><meta charset="utf-8"><title>Relatório ${auditId}</title>
<style>body{font-family:Georgia,serif;max-width:900px;margin:2rem auto;padding:0 1rem;line-height:1.5;background:#f7f4ef;color:#1a1a1a}
pre{white-space:pre-wrap;background:#fff;padding:1.5rem;border:1px solid #ddd}</style></head>
<body><pre>${reportMarkdown
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")}</pre></body></html>`;
    const blob = new Blob([html], { type: "text/html" });
    const url = URL.createObjectURL(blob);
    window.open(url, "_blank", "noopener,noreferrer");
  };

  return (
    <div className="flex flex-wrap gap-3">
      <button
        type="button"
        onClick={() => download(`relatorio-${auditId}.md`, reportMarkdown, "text/markdown")}
        className="rounded-full bg-ink px-5 py-2.5 text-sm text-paper hover:bg-forest transition-colors"
      >
        Exportar Markdown
      </button>
      {IS_LAB || datapackage ? (
        <button
          type="button"
          onClick={openHtml}
          className="rounded-full border border-ink/20 bg-white px-5 py-2.5 text-sm text-ink hover:border-forest hover:text-forest transition-colors"
        >
          Abrir HTML
        </button>
      ) : (
        <a
          href={`${API_BASE}/audit/${auditId}/report?format=html`}
          target="_blank"
          rel="noreferrer"
          className="rounded-full border border-ink/20 bg-white px-5 py-2.5 text-sm text-ink hover:border-forest hover:text-forest transition-colors"
        >
          Abrir HTML
        </a>
      )}
      {datapackage ? (
        <button
          type="button"
          onClick={() =>
            download(
              `datapackage-${auditId}.json`,
              JSON.stringify(datapackage, null, 2),
              "application/json"
            )
          }
          className="rounded-full border border-ink/20 bg-white px-5 py-2.5 text-sm text-ink hover:border-forest hover:text-forest transition-colors"
        >
          datapackage.json
        </button>
      ) : (
        <a
          href={`${API_BASE}/audit/${auditId}/datapackage.json`}
          target="_blank"
          rel="noreferrer"
          className="rounded-full border border-ink/20 bg-white px-5 py-2.5 text-sm text-ink hover:border-forest hover:text-forest transition-colors"
        >
          datapackage.json
        </a>
      )}
    </div>
  );
}
