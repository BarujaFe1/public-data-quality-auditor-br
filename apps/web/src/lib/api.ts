import type {
  AuditRun,
  AuditSummary,
  ColumnProfile,
  DataDictionaryField,
  DemoDataset,
  QualityIssue,
  Severity,
} from "@/types/audit";
import {
  DEMO_CATALOG,
  cloneDemoAudit,
  getStoredAudit,
} from "@/lib/demo-store";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

/** Live lab defaults to embedded snapshots. Opt into FastAPI with NEXT_PUBLIC_USE_API=true. */
export const USE_API = process.env.NEXT_PUBLIC_USE_API === "true";
export const IS_LAB = !USE_API;

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

function toSummary(audit: AuditRun): AuditSummary {
  const rank: Record<Severity, number> = {
    critical: 0,
    high: 1,
    warning: 2,
    info: 3,
  };
  const top = [...audit.issues]
    .sort(
      (a, b) =>
        (rank[a.severity] ?? 9) - (rank[b.severity] ?? 9) ||
        b.affected_rows_count - a.affected_rows_count
    )
    .slice(0, 8);
  return {
    id: audit.id,
    dataset_name: audit.dataset_name,
    uploaded_filename: audit.uploaded_filename,
    row_count: audit.row_count,
    column_count: audit.column_count,
    overall_score: audit.overall_score,
    dimensions: {
      completeness: audit.completeness_score,
      uniqueness: audit.uniqueness_score,
      validity: audit.validity_score,
      consistency: audit.consistency_score,
      documentation: audit.documentation_score,
    },
    top_issues: top,
    executive_recommendation: audit.executive_recommendation,
    created_at: audit.created_at,
    status: audit.status,
  };
}

function requireStored(id: string): AuditRun {
  const audit = getStoredAudit(id);
  if (!audit) {
    throw new Error(
      "Auditoria lab não encontrada nesta sessão. Volte em /audit e rode um dataset demo."
    );
  }
  return audit;
}

export const api = {
  health: async () => {
    if (!USE_API) {
      return { status: "ok", mode: "lab-snapshot" as const };
    }
    return request<{ status: string }>("/health");
  },

  listDemos: async (): Promise<DemoDataset[]> => {
    if (!USE_API) return DEMO_CATALOG;
    return request<DemoDataset[]>("/demos");
  },

  runDemo: async (name: string): Promise<AuditRun> => {
    if (!USE_API) {
      // Tiny delay so the UI shows processing feedback
      await new Promise((r) => setTimeout(r, 350));
      return cloneDemoAudit(name);
    }
    return request<AuditRun>(`/audit/demo/${name}`, { method: "POST" });
  },

  upload: async (file: File): Promise<AuditRun> => {
    if (!USE_API) {
      throw new Error(
        "Upload de CSV exige a API local (NEXT_PUBLIC_USE_API=true). Nesta demo pública use os datasets sintéticos."
      );
    }
    const form = new FormData();
    form.append("file", file);
    return request<AuditRun>("/audit/upload", { method: "POST", body: form });
  },

  getAudit: async (id: string): Promise<AuditRun> => {
    if (!USE_API) return requireStored(id);
    return request<AuditRun>(`/audit/${id}`);
  },

  getSummary: async (id: string): Promise<AuditSummary> => {
    if (!USE_API) return toSummary(requireStored(id));
    return request<AuditSummary>(`/audit/${id}/summary`);
  },

  getColumns: async (id: string): Promise<ColumnProfile[]> => {
    if (!USE_API) return requireStored(id).columns;
    return request<ColumnProfile[]>(`/audit/${id}/columns`);
  },

  getIssues: async (
    id: string,
    params?: Record<string, string>
  ): Promise<QualityIssue[]> => {
    if (!USE_API) {
      let issues = requireStored(id).issues;
      if (params?.severity) {
        issues = issues.filter((i) => i.severity === params.severity);
      }
      if (params?.dimension) {
        issues = issues.filter((i) => i.dimension === params.dimension);
      }
      if (params?.column) {
        issues = issues.filter((i) => (i.column_name || "") === params.column);
      }
      return issues;
    }
    const qs = params ? `?${new URLSearchParams(params)}` : "";
    return request<QualityIssue[]>(`/audit/${id}/issues${qs}`);
  },

  getDictionary: async (id: string): Promise<DataDictionaryField[]> => {
    if (!USE_API) return requireStored(id).data_dictionary;
    return request<DataDictionaryField[]>(`/audit/${id}/data-dictionary`);
  },

  reportUrl: (id: string, format: "markdown" | "html" = "markdown") =>
    `${API_BASE}/audit/${id}/report?format=${format}`,

  datapackageUrl: (id: string) => `${API_BASE}/audit/${id}/datapackage.json`,
};

export { API_BASE };
