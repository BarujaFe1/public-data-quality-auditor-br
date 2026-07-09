import type {
  AuditRun,
  AuditSummary,
  ColumnProfile,
  DataDictionaryField,
  DemoDataset,
  QualityIssue,
} from "@/types/audit";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    ...init,
    cache: "no-store",
  });
  if (!res.ok) {
    let detail = res.statusText;
    try {
      const body = await res.json();
      detail = body.detail || JSON.stringify(body);
    } catch {
      /* ignore */
    }
    throw new Error(typeof detail === "string" ? detail : JSON.stringify(detail));
  }
  const contentType = res.headers.get("content-type") || "";
  if (contentType.includes("application/json")) {
    return res.json() as Promise<T>;
  }
  return res.text() as Promise<T>;
}

export const api = {
  health: () => request<{ status: string }>("/health"),
  listDemos: () => request<DemoDataset[]>("/demos"),
  runDemo: (name: string) =>
    request<AuditRun>(`/audit/demo/${name}`, { method: "POST" }),
  upload: async (file: File) => {
    const form = new FormData();
    form.append("file", file);
    return request<AuditRun>("/audit/upload", { method: "POST", body: form });
  },
  getAudit: (id: string) => request<AuditRun>(`/audit/${id}`),
  getSummary: (id: string) => request<AuditSummary>(`/audit/${id}/summary`),
  getColumns: (id: string) => request<ColumnProfile[]>(`/audit/${id}/columns`),
  getIssues: (id: string, params?: Record<string, string>) => {
    const qs = params ? `?${new URLSearchParams(params)}` : "";
    return request<QualityIssue[]>(`/audit/${id}/issues${qs}`);
  },
  getDictionary: (id: string) =>
    request<DataDictionaryField[]>(`/audit/${id}/data-dictionary`),
  reportUrl: (id: string, format: "markdown" | "html" = "markdown") =>
    `${API_BASE}/audit/${id}/report?format=${format}`,
  datapackageUrl: (id: string) => `${API_BASE}/audit/${id}/datapackage.json`,
};

export { API_BASE };
