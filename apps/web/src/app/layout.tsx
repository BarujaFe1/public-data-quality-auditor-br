import type { Metadata } from "next";
import "./globals.css";
import { PageShell } from "@/components/layout";
import { I18nProvider } from "@/lib/i18n";

export const metadata: Metadata = {
  title: "Public Data Quality Auditor BR",
  description:
    "Audite qualidade de bases públicas brasileiras em CSV: profiling, validações, score e relatório. Diagnóstico explicável, não certificação.",
  openGraph: {
    title: "Public Data Quality Auditor BR",
    description:
      "Profiling, checks, dimensional score, issues register and datapackage for Brazilian public CSVs.",
    url: "https://public-data-quality-auditor-br-nu.vercel.app",
    siteName: "Public Data Quality Auditor BR",
    locale: "pt_BR",
    type: "website",
  },
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="pt-BR">
      <body>
        <I18nProvider>
          <PageShell>{children}</PageShell>
        </I18nProvider>
      </body>
    </html>
  );
}
