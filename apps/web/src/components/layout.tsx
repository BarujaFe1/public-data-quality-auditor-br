"use client";

import Link from "next/link";
import { ReactNode } from "react";
import { IS_LAB } from "@/lib/api";
import { LabBanner } from "@/components/LabBanner";
import { locales, useI18n } from "@/lib/i18n";

export function SiteHeader() {
  const { locale, setLocale, t } = useI18n();

  return (
    <header className="border-b border-ink/10 bg-paper/80 backdrop-blur-md sticky top-0 z-40">
      <LabBanner />
      <div className="mx-auto flex max-w-6xl items-center justify-between gap-4 px-4 py-4">
        <Link href="/" className="group">
          <p className="font-display text-xl tracking-tight text-ink group-hover:text-forest transition-colors">
            Public Data Quality Auditor BR
          </p>
          <p className="text-xs uppercase tracking-[0.18em] text-slate">{t("brand.tagline")}</p>
        </Link>
        <nav className="flex items-center gap-5 text-sm text-ink/80">
          <Link href="/audit" className="hover:text-forest transition-colors">
            {t("nav.audit")}
          </Link>
          <Link href="/methodology" className="hover:text-forest transition-colors">
            {t("nav.methodology")}
          </Link>
          {IS_LAB ? (
            <Link href="/methodology#limitations" className="hover:text-forest transition-colors">
              {t("nav.limitations")}
            </Link>
          ) : (
            <a
              href={`${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/docs`}
              target="_blank"
              rel="noreferrer"
              className="hover:text-forest transition-colors"
            >
              {t("nav.api")}
            </a>
          )}
        </nav>
        <button
          type="button"
          data-testid="locale-toggle"
          aria-label={t("lang.label")}
          onClick={() => setLocale(locale === "pt-BR" ? "en" : "pt-BR")}
          className="rounded-full border border-ink/20 px-3 py-1.5 text-xs font-medium hover:border-forest hover:text-forest transition-colors"
        >
          {locales.map((item) => t(`lang.${item}`)).join(" / ")}
        </button>
      </div>
    </header>
  );
}

export function SiteFooter() {
  const { t } = useI18n();

  return (
    <footer className="mt-auto border-t border-ink/10 bg-ink text-paper">
      <div className="mx-auto max-w-6xl px-4 py-8 text-sm leading-relaxed text-paper/80">
        <p className="font-display text-lg text-paper">{t("footer.title")}</p>
        <p className="mt-2 max-w-2xl">
          {t("footer.body")}
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
