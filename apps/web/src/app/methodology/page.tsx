import Link from "next/link";

export default function MethodologyPage() {
  return (
    <div className="mx-auto max-w-3xl px-4 py-12 space-y-8 animate-rise">
      <div>
        <h1 className="font-display text-4xl text-ink">Metodologia</h1>
        <p className="mt-3 text-slate leading-relaxed">
          A auditoria combina profiling estatístico e regras heurísticas sobre CSV. O score é um
          diagnóstico explicável — não uma certificação de verdade factual.
        </p>
      </div>

      <section className="space-y-3">
        <h2 className="font-display text-2xl">Dimensões e pesos</h2>
        <ul className="list-disc pl-5 text-slate space-y-1">
          <li>Completude — 25 pontos</li>
          <li>Unicidade — 20 pontos</li>
          <li>Validade — 25 pontos</li>
          <li>Consistência — 20 pontos</li>
          <li>Documentabilidade — 10 pontos</li>
        </ul>
      </section>

      <section id="limitations" className="space-y-3 scroll-mt-28">
        <h2 className="font-display text-2xl">Limitações</h2>
        <ul className="list-disc pl-5 text-slate space-y-1">
          <li>Não valida se os fatos são verdadeiros no mundo real.</li>
          <li>Não corrige dados automaticamente de forma irreversível.</li>
          <li>Não avalia viés político do conteúdo.</li>
          <li>Não substitui revisão humana do dicionário e da licença.</li>
          <li>
            A demo pública usa snapshots pré-computados (lab). Upload CSV e API live exigem stack
            local com <code className="rounded bg-sand px-1">NEXT_PUBLIC_USE_API=true</code>.
          </li>
          <li>Checks são heurísticos — podem gerar falsos positivos/negativos.</li>
        </ul>
      </section>

      <p className="text-sm text-slate">
        Documentação completa em{" "}
        <code className="rounded bg-sand px-1.5 py-0.5">docs/methodology.md</code>.{" "}
        <Link href="/audit" className="text-forest hover:underline">
          Voltar para auditar
        </Link>
        .
      </p>
    </div>
  );
}
