"use client";

import { createContext, useContext, useEffect, useMemo, useState, type ReactNode } from "react";

export const locales = ["pt-BR", "en"] as const;
export type Locale = (typeof locales)[number];

const storageKey = "pdqa-locale";

const messages = {
  "pt-BR": {
    "brand.tagline": "auditoria de dados abertos",
    "nav.audit": "Auditar",
    "nav.methodology": "Metodologia",
    "nav.limitations": "Limitações",
    "nav.api": "API",
    "lang.label": "Idioma",
    "lang.pt-BR": "PT",
    "lang.en": "EN",
    "footer.title": "Diagnóstico, não certificação.",
    "footer.body":
      "O score indica riscos de qualidade observáveis no CSV. Não valida verdade factual, licença legal nem adequação política do conteúdo.",
    "lab.banner": "Lab / demo de portfólio — snapshots (municípios, escolas, contratos + amostra IBGE). O score é um diagnóstico explicável, não uma certificação. Upload de CSV e API ao vivo exigem a stack local com",
    "home.headline": "Antes de usar dados públicos, audite se eles sustentam a análise.",
    "home.description":
      "Profiling, checks explicáveis, score por dimensão, registro de problemas e relatório executivo — para CSV de dados abertos brasileiros. O score é diagnóstico, não certificação.",
    "home.runDemo": "Rodar demo",
    "home.limitations": "Ver limitações",
    "home.upload": "Enviar CSV",
    "home.transparent.title": "Diagnóstico transparente",
    "home.transparent.body": "Cinco dimensões ponderadas, penalidades por severidade e amostras de linhas afetadas.",
    "home.product.title": "Produto, não notebook",
    "home.product.labBody": "Demo pública com snapshots do motor FastAPI/Pandas. Upload ao vivo exige stack local.",
    "home.product.body": "API FastAPI + interface analítica com exportação de relatório e datapackage.json.",
    "home.public.title": "Utilidade pública",
    "home.public.body": "Feito para jornalistas, pesquisadores e analistas que consomem bases abertas.",
    "audit.title": "Auditar dataset",
    "audit.labDescription": "Escolha um demo sintético (intencionalmente sujo) ou a amostra pública IBGE. Nesta demo, o resultado vem de snapshots pré-computados pelo mesmo motor da API.",
    "audit.description": "Escolha um demo sintético, a amostra pública IBGE, ou envie um CSV (até 5 MB / 50 mil linhas). Encoding UTF-8 ou Latin-1; separador vírgula, ponto-e-vírgula ou tab.",
    "audit.loadError": "Não foi possível carregar demos. Confirme se a API está em",
    "audit.runError": "Falha ao auditar demo.",
    "audit.uploadError": "Falha no upload.",
    "audit.demos": "Datasets demo",
    "audit.loadingDemos": "Carregando demos…",
    "audit.loadingLab": "Carregando catálogo lab…",
    "audit.loadingApi": "Consultando a API local.",
    "audit.publicSample": "Amostra pública",
    "audit.synthetic": "Sintético",
    "audit.processing": "Processando…",
    "audit.runNow": "Auditar agora",
    "audit.uploadTitle": "Upload de CSV",
    "audit.uploadDisabled": "Upload está desabilitado nesta demo pública (lab/snapshot). Para auditar um CSV próprio, rode a stack local com",
    "audit.uploadHelp": "Preferencialmente com cabeçalho na primeira linha. O MVP não corrige dados — apenas diagnostica.",
    "audit.uploading": "Enviando e auditando…",
    "audit.selectFile": "Selecionar arquivo .csv",
    "audit.loading": "Carregando auditoria…",
    "audit.label": "Auditoria",
    "audit.rows": "linhas",
    "audit.columns": "colunas",
    "audit.new": "Nova auditoria",
    "tab.summary": "Resumo",
    "tab.columns": "Colunas",
    "tab.issues": "Issues",
    "tab.dictionary": "Dicionário",
    "dict.field": "Campo",
    "dict.type": "Tipo",
    "dict.nullable": "Nullable",
    "dict.description": "Descrição sugerida",
    "dict.examples": "Exemplos",
    "dict.qualityNotes": "Notas de qualidade",
    "dict.yes": "sim",
    "dict.no": "não",
    "score.label": "Score de qualidade",
    "issues.top": "Principais problemas",
  },
  en: {
    "brand.tagline": "open data auditing",
    "nav.audit": "Audit",
    "nav.methodology": "Methodology",
    "nav.limitations": "Limitations",
    "nav.api": "API",
    "lang.label": "Language",
    "lang.pt-BR": "PT",
    "lang.en": "EN",
    "footer.title": "Diagnosis, not certification.",
    "footer.body":
      "The score identifies observable quality risks in the CSV. It does not verify factual truth, legal licensing, or the policy suitability of its content.",
    "lab.banner": "Lab / portfolio demo — snapshots (municipalities, schools, contracts + IBGE sample). The score is an explainable diagnosis, not a certification. CSV upload and the live API require a local stack with",
    "home.headline": "Before using public data, audit whether it supports your analysis.",
    "home.description":
      "Profiling, explainable checks, dimension-level scoring, an issue register, and an executive report — for Brazilian open-data CSVs. The score is a diagnosis, not certification.",
    "home.runDemo": "Run demo",
    "home.limitations": "View limitations",
    "home.upload": "Upload CSV",
    "home.transparent.title": "Transparent diagnosis",
    "home.transparent.body": "Five weighted dimensions, severity penalties, and samples of affected rows.",
    "home.product.title": "Product, not notebook",
    "home.product.labBody": "Public demo using snapshots from the FastAPI/Pandas engine. Live upload requires a local stack.",
    "home.product.body": "FastAPI API plus an analytical interface with report and datapackage.json exports.",
    "home.public.title": "Public value",
    "home.public.body": "Built for journalists, researchers, and analysts who use open datasets.",
    "audit.title": "Audit dataset",
    "audit.labDescription": "Choose a deliberately messy synthetic demo or the public IBGE sample. In this demo, the result comes from pre-computed snapshots generated by the same API engine.",
    "audit.description": "Choose a synthetic demo, the public IBGE sample, or upload a CSV (up to 5 MB / 50,000 rows). UTF-8 or Latin-1 encoding; comma, semicolon, or tab separator.",
    "audit.loadError": "Could not load demos. Confirm that the API is running at",
    "audit.runError": "Could not audit the demo.",
    "audit.uploadError": "Upload failed.",
    "audit.demos": "Demo datasets",
    "audit.loadingDemos": "Loading demos…",
    "audit.loadingLab": "Loading lab catalog…",
    "audit.loadingApi": "Contacting the local API.",
    "audit.publicSample": "Public sample",
    "audit.synthetic": "Synthetic",
    "audit.processing": "Processing…",
    "audit.runNow": "Audit now",
    "audit.uploadTitle": "CSV upload",
    "audit.uploadDisabled": "Upload is disabled in this public demo (lab/snapshot). To audit your own CSV, run the local stack with",
    "audit.uploadHelp": "A header on the first row is preferred. The MVP does not fix data — it only diagnoses it.",
    "audit.uploading": "Uploading and auditing…",
    "audit.selectFile": "Select .csv file",
    "audit.loading": "Loading audit…",
    "audit.label": "Audit",
    "audit.rows": "rows",
    "audit.columns": "columns",
    "audit.new": "New audit",
    "tab.summary": "Summary",
    "tab.columns": "Columns",
    "tab.issues": "Issues",
    "tab.dictionary": "Dictionary",
    "dict.field": "Field",
    "dict.type": "Type",
    "dict.nullable": "Nullable",
    "dict.description": "Suggested description",
    "dict.examples": "Examples",
    "dict.qualityNotes": "Quality notes",
    "dict.yes": "yes",
    "dict.no": "no",
    "score.label": "Quality score",
    "issues.top": "Top issues",
  },
} as const;

type MessageKey = keyof (typeof messages)["pt-BR"];
type I18nContextValue = {
  locale: Locale;
  setLocale: (locale: Locale) => void;
  t: (key: MessageKey) => string;
};

const I18nContext = createContext<I18nContextValue | null>(null);

export function I18nProvider({ children }: { children: ReactNode }) {
  const [locale, setLocaleState] = useState<Locale>("pt-BR");

  useEffect(() => {
    const savedLocale = window.localStorage.getItem(storageKey);
    if (savedLocale && locales.includes(savedLocale as Locale)) {
      setLocaleState(savedLocale as Locale);
    }
  }, []);

  useEffect(() => {
    document.documentElement.lang = locale;
    window.localStorage.setItem(storageKey, locale);
  }, [locale]);

  const value = useMemo(
    () => ({
      locale,
      setLocale: setLocaleState,
      t: (key: MessageKey) => messages[locale][key],
    }),
    [locale]
  );

  return <I18nContext.Provider value={value}>{children}</I18nContext.Provider>;
}

export function useI18n() {
  const context = useContext(I18nContext);
  if (!context) throw new Error("useI18n must be used within I18nProvider");
  return context;
}
