import type { AuditRun, DemoDataset } from "@/types/audit";
import municipios from "./snapshots/municipios.json";
import escolas from "./snapshots/escolas.json";
import contratos from "./snapshots/contratos.json";

export const DEMO_CATALOG: DemoDataset[] = [
  {
    id: "municipios",
    title: "Municípios BR (demo)",
    description:
      "Dataset sintético-realista de municípios com problemas intencionais de qualidade.",
    filename: "municipios_demo.csv",
    available: true,
  },
  {
    id: "escolas",
    title: "Escolas BR (demo)",
    description:
      "Dataset sintético-realista de escolas com nulos, categorias inconsistentes e duplicidades.",
    filename: "escolas_demo.csv",
    available: true,
  },
  {
    id: "contratos",
    title: "Contratos públicos (demo)",
    description:
      "Dataset sintético-realista de contratos com valores negativos, datas invertidas e CNPJ inválido.",
    filename: "contratos_demo.csv",
    available: true,
  },
];

const SNAPSHOTS: Record<string, AuditRun> = {
  municipios: municipios as AuditRun,
  escolas: escolas as AuditRun,
  contratos: contratos as AuditRun,
};

const STORAGE_KEY = "pdqa-lab-audits";

function readStore(): Record<string, AuditRun> {
  if (typeof window === "undefined") return {};
  try {
    const raw = sessionStorage.getItem(STORAGE_KEY);
    return raw ? (JSON.parse(raw) as Record<string, AuditRun>) : {};
  } catch {
    return {};
  }
}

function writeStore(store: Record<string, AuditRun>) {
  if (typeof window === "undefined") return;
  sessionStorage.setItem(STORAGE_KEY, JSON.stringify(store));
}

export function cloneDemoAudit(datasetName: string): AuditRun {
  const base = SNAPSHOTS[datasetName];
  if (!base) {
    throw new Error(`Dataset demo '${datasetName}' não encontrado no lab.`);
  }
  const id =
    typeof crypto !== "undefined" && "randomUUID" in crypto
      ? crypto.randomUUID()
      : `lab-${datasetName}-${Date.now()}`;
  const audit: AuditRun = {
    ...structuredClone(base),
    id,
    created_at: new Date().toISOString(),
    status: "completed",
  };
  const store = readStore();
  store[id] = audit;
  writeStore(store);
  return audit;
}

export function getStoredAudit(auditId: string): AuditRun | null {
  const store = readStore();
  if (store[auditId]) return store[auditId];
  // Fallback: match original snapshot ids if someone deep-links a baked id
  for (const snap of Object.values(SNAPSHOTS)) {
    if (snap.id === auditId) return snap;
  }
  return null;
}

export function listSnapshotKeys(): string[] {
  return Object.keys(SNAPSHOTS);
}
