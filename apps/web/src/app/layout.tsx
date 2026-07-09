import type { Metadata } from "next";
import "./globals.css";
import { PageShell } from "@/components/layout";

export const metadata: Metadata = {
  title: "Public Data Quality Auditor BR",
  description:
    "Audite qualidade de bases públicas brasileiras em CSV: profiling, validações, score e relatório.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="pt-BR">
      <body>
        <PageShell>{children}</PageShell>
      </body>
    </html>
  );
}
