import Link from "next/link";
import { ReactNode } from "react";
import { IS_LAB } from "@/lib/api";
import { LabBanner } from "@/components/LabBanner";

export function SiteHeader() {
  return (
    <header className="border-b border-ink/10 bg-paper/80 backdrop-blur-md sticky top-0 z-40">
      <LabBanner />
      <div className="mx-auto flex max-w-6xl items-center justify-between gap-4 px-4 py-4">
        <Link href="/" className="group">
          <p className="font-display text-xl tracking-tight text-ink group-hover:text-forest transition-colors">
            Public Data Quality Auditor BR
          </p>
          <p className="text-xs uppercase tracking-[0.18em] text-slate">auditoria de dados abertos</p>
        </Link>
        <nav className="flex items-center gap-5 text-sm text-ink/80">
          <Link href="/audit" className="hover:text-forest transition-colors">
            Auditar
          </Link>
          <Link href="/methodology" className="hover:text-forest transition-colors">
            Metodologia
          </Link>
          {IS_LAB ? (
            <Link href="/methodology#limitations" className="hover:text-forest transition-colors">
              Limitações
            </Link>
          ) : (
            <a
              href={`${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/docs`}
              target="_blank"
              rel="noreferrer"
              className="hover:text-forest transition-colors"
            >
              API
            </a>
          )}
        </nav>
      </div>
    </header>
  );
}

export function SiteFooter() {
  return (
    <footer className="mt-auto border-t border-ink/10 bg-ink text-paper">
      <div className="mx-auto max-w-6xl px-4 py-8 text-sm leading-relaxed text-paper/80">
        <p className="font-display text-lg text-paper">Diagnóstico, não certificação.</p>
        <p className="mt-2 max-w-2xl">
          O score indica riscos de qualidade observáveis no CSV. Não valida verdade factual,
          licença legal nem adequação política do conteúdo.
        </p>
      </div>
    </footer>
  );
}

export function PageShell({ children }: { children: ReactNode }) {
  return (
    <div className="min-h-screen flex flex-col bg-paper text-ink">
      <SiteHeader />
      <main className="flex-1">{children}</main>
      <SiteFooter />
    </div>
  );
}
