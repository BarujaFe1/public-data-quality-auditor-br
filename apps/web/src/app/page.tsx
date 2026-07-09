import Link from "next/link";

export default function HomePage() {
  return (
    <div>
      <section className="relative overflow-hidden border-b border-ink/10">
        <div
          className="absolute inset-0 opacity-40"
          style={{
            backgroundImage:
              "linear-gradient(120deg, rgba(20,33,61,0.06) 1px, transparent 1px), linear-gradient(rgba(20,33,61,0.05) 1px, transparent 1px)",
            backgroundSize: "28px 28px",
          }}
        />
        <div className="relative mx-auto max-w-6xl px-4 py-20 md:py-28 animate-rise">
          <p className="font-display text-4xl md:text-6xl leading-[1.05] text-ink max-w-3xl">
            Public Data Quality Auditor BR
          </p>
          <h1 className="mt-6 max-w-2xl text-xl md:text-2xl text-ink/80 leading-snug">
            Antes de usar dados públicos, audite se eles sustentam a análise.
          </h1>
          <p className="mt-4 max-w-xl text-slate">
            Profiling, checks explicáveis, score por dimensão, registro de problemas e relatório
            executivo — para CSV de dados abertos brasileiros.
          </p>
          <div className="mt-10 flex flex-wrap gap-4">
            <Link
              href="/audit"
              className="rounded-full bg-forest px-6 py-3 text-paper shadow-soft hover:bg-ink transition-colors"
            >
              Rodar demo
            </Link>
            <Link
              href="/audit#upload"
              className="rounded-full border border-ink/20 bg-white/70 px-6 py-3 text-ink hover:border-forest transition-colors"
            >
              Enviar CSV
            </Link>
          </div>
        </div>
      </section>

      <section className="mx-auto max-w-6xl px-4 py-16 grid md:grid-cols-3 gap-6">
        {[
          {
            title: "Diagnóstico transparente",
            body: "Cinco dimensões ponderadas, penalidades por severidade e amostras de linhas afetadas.",
          },
          {
            title: "Produto, não notebook",
            body: "API FastAPI + interface analítica com exportação de relatório e datapackage.json.",
          },
          {
            title: "Utilidade pública",
            body: "Feito para jornalistas, pesquisadores e analistas que consomem bases abertas.",
          },
        ].map((item, idx) => (
          <article
            key={item.title}
            className="rounded-2xl border border-ink/10 bg-white/60 p-6 animate-rise"
            style={{ animationDelay: `${0.1 * (idx + 1)}s` }}
          >
            <h2 className="font-display text-2xl text-ink">{item.title}</h2>
            <p className="mt-3 text-slate leading-relaxed">{item.body}</p>
          </article>
        ))}
      </section>
    </div>
  );
}
