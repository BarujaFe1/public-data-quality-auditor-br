"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { api, IS_LAB } from "@/lib/api";
import type { DemoDataset } from "@/types/audit";
import { EmptyState, ErrorState } from "@/components/panels";

export default function AuditEntryPage() {
  const router = useRouter();
  const [demos, setDemos] = useState<DemoDataset[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [busyLabel, setBusyLabel] = useState<string | null>(null);

  useEffect(() => {
    api
      .listDemos()
      .then(setDemos)
      .catch((err: Error) =>
        setError(
          err.message ||
            `Não foi possível carregar demos. Confirme se a API está em ${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}.`
        )
      );
  }, []);

  const runDemo = async (id: string) => {
    setLoading(true);
    setBusyLabel(id);
    setError(null);
    try {
      const audit = await api.runDemo(id);
      router.push(`/audit/${audit.id}`);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Falha ao auditar demo.");
    } finally {
      setLoading(false);
      setBusyLabel(null);
    }
  };

  const onUpload = async (file: File | null) => {
    if (!file) return;
    setLoading(true);
    setBusyLabel("upload");
    setError(null);
    try {
      const audit = await api.upload(file);
      router.push(`/audit/${audit.id}`);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Falha no upload.");
    } finally {
      setLoading(false);
      setBusyLabel(null);
    }
  };

  return (
    <div className="mx-auto max-w-6xl px-4 py-12 space-y-10">
      <div className="animate-rise">
        <h1 className="font-display text-4xl text-ink">Auditar dataset</h1>
        <p className="mt-3 max-w-2xl text-slate">
          {IS_LAB
            ? "Escolha um dataset demo sintético-realista. Nesta demo pública o resultado vem de snapshots pré-computados (mesmo motor de qualidade do MVP)."
            : "Escolha um dataset demo sintético-realista ou envie um CSV (até 5 MB / 50 mil linhas). Encoding UTF-8 ou Latin-1; separador vírgula, ponto-e-vírgula ou tab."}
        </p>
      </div>

      {error && <ErrorState message={error} />}

      <section>
        <h2 className="font-display text-2xl text-ink mb-4">Datasets demo</h2>
        {demos.length === 0 && !error ? (
          <EmptyState
            title="Carregando demos…"
            body={IS_LAB ? "Carregando catálogo lab…" : "Consultando a API local."}
          />
        ) : (
          <div className="grid md:grid-cols-3 gap-4">
            {demos.map((demo) => (
              <button
                key={demo.id}
                type="button"
                disabled={loading || !demo.available}
                onClick={() => runDemo(demo.id)}
                className="text-left rounded-2xl border border-ink/10 bg-white/70 p-5 shadow-soft hover:border-forest transition-colors disabled:opacity-60"
              >
                <p className="font-display text-xl text-ink">{demo.title}</p>
                <p className="mt-2 text-sm text-slate leading-relaxed">{demo.description}</p>
                <p className="mt-4 text-xs uppercase tracking-wider text-forest">
                  {busyLabel === demo.id ? "Processando…" : "Auditar agora"}
                </p>
              </button>
            ))}
          </div>
        )}
      </section>

      <section id="upload" className="rounded-2xl border border-ink/10 bg-white/70 p-6 shadow-soft">
        <h2 className="font-display text-2xl text-ink">Upload de CSV</h2>
        {IS_LAB ? (
          <p className="mt-2 text-sm text-slate">
            Upload está desabilitado nesta demo pública (lab/snapshot). Para auditar um CSV próprio,
            rode a stack local com{" "}
            <code className="rounded bg-sand px-1">NEXT_PUBLIC_USE_API=true</code> e a API FastAPI.
          </p>
        ) : (
          <>
            <p className="mt-2 text-sm text-slate">
              Preferencialmente com cabeçalho na primeira linha. O MVP não corrige dados — apenas
              diagnostica.
            </p>
            <label className="mt-6 flex cursor-pointer flex-col items-start gap-3 rounded-xl border border-dashed border-ink/25 bg-sand/30 px-5 py-8 hover:border-forest transition-colors">
              <span className="text-sm font-medium text-ink">
                {busyLabel === "upload" ? "Enviando e auditando…" : "Selecionar arquivo .csv"}
              </span>
              <input
                type="file"
                accept=".csv,text/csv"
                className="text-sm"
                disabled={loading}
                onChange={(e) => onUpload(e.target.files?.[0] ?? null)}
              />
            </label>
          </>
        )}
      </section>
    </div>
  );
}
