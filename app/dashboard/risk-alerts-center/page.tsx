"use client";
import { useEffect, useState } from "react";

type Severity = "CRITIQUE" | "ÉLEVÉ" | "MODÉRÉ" | "INFO";
type AlertStatus = "ACTIF" | "ACQUITTÉ" | "RÉSOLU";

interface RiskAlert {
  id: string;
  severity: Severity;
  status: AlertStatus;
  agentId: string;
  domain: string;
  entityId: string;
  score: number;
  threshold: number;
  message: string;
  triggeredAt: string;
  actions: string[];
}

const SEV_COLOR: Record<Severity, string> = {
  CRITIQUE: "#dc2626", ÉLEVÉ: "#ea580c", MODÉRÉ: "#d97706", INFO: "#6366f1",
};
const SEV_BG: Record<Severity, string> = {
  CRITIQUE: "#fef2f2", ÉLEVÉ: "#fff7ed", MODÉRÉ: "#fffbeb", INFO: "#eef2ff",
};
const STATUS_COLOR: Record<AlertStatus, string> = {
  ACTIF: "#dc2626", ACQUITTÉ: "#d97706", RÉSOLU: "#16a34a",
};

const AGENTS = [
  { id: "influencer-marketing-agency", scores: [96, 89, 82, 76, 58, 47, 29, 10] },
  { id: "content-creator-platform", scores: [96, 89, 82, 76, 58, 47, 29, 10] },
  { id: "brand-ambassador-program", scores: [96, 89, 82, 76, 58, 47, 29, 10] },
  { id: "micro-influencer-network", scores: [96, 89, 82, 76, 58, 47, 29, 10] },
  { id: "viral-content-marketing", scores: [96, 89, 82, 76, 58, 47, 29, 10] },
  { id: "user-generated-content", scores: [96, 89, 82, 76, 58, 47, 29, 10] },
  { id: "podcast-advertising", scores: [96, 89, 82, 76, 58, 47, 29, 10] },
  { id: "streaming-content", scores: [96, 89, 82, 76, 58, 47, 29, 10] },
  { id: "augmented-reality-ads", scores: [96, 89, 82, 76, 58, 47, 29, 10] },
];

function makeSeverity(score: number): Severity {
  if (score >= 60) return "CRITIQUE";
  if (score >= 40) return "ÉLEVÉ";
  if (score >= 20) return "MODÉRÉ";
  return "INFO";
}

const ACTIONS: Record<Severity, string[]> = {
  CRITIQUE: ["Audit CSDDD immédiat", "Suspension contrats fournisseurs", "Notification autorités", "Plan remédiation 30 j"],
  ÉLEVÉ: ["Révision plan vigilance", "Justificatifs partenaires", "Suivi mensuel renforcé"],
  MODÉRÉ: ["Surveillance trimestrielle", "Formation équipes conformité"],
  INFO: ["Documenter et archiver"],
};

function generateAlerts(): RiskAlert[] {
  const alerts: RiskAlert[] = [];
  const now = Date.now();
  for (const agent of AGENTS) {
    agent.scores.forEach((sc, i) => {
      if (sc < 20) return;
      const sev = makeSeverity(sc);
      const eid = `${agent.id.slice(0, 3).toUpperCase()}-00${i + 1}`;
      alerts.push({
        id: "ALT-" + Math.random().toString(36).slice(2, 8).toUpperCase(),
        severity: sev,
        status: sev === "CRITIQUE" ? "ACTIF" : sev === "ÉLEVÉ" ? "ACQUITTÉ" : "RÉSOLU",
        agentId: agent.id,
        domain: agent.id.replace(/-/g, " "),
        entityId: eid,
        score: sc,
        threshold: sev === "CRITIQUE" ? 60 : sev === "ÉLEVÉ" ? 40 : 20,
        message: `Entité ${eid} — score ${sc} dépasse le seuil ${sev.toLowerCase()}`,
        triggeredAt: new Date(now - Math.random() * 7200000).toISOString(),
        actions: ACTIONS[sev],
      });
    });
  }
  return alerts.sort((a, b) => {
    const sevOrder = { CRITIQUE: 0, ÉLEVÉ: 1, MODÉRÉ: 2, INFO: 3 };
    return (sevOrder[a.severity] - sevOrder[b.severity]) || new Date(b.triggeredAt).getTime() - new Date(a.triggeredAt).getTime();
  });
}

export default function RiskAlertsCenterPage() {
  const [alerts, setAlerts] = useState<RiskAlert[]>([]);
  const [sevFilter, setSevFilter] = useState<string>("ALL");
  const [statusFilter, setStatusFilter] = useState<string>("ALL");
  const [expanded, setExpanded] = useState<string | null>(null);

  useEffect(() => { setAlerts(generateAlerts()); }, []);

  const filtered = alerts.filter(a => {
    if (sevFilter !== "ALL" && a.severity !== sevFilter) return false;
    if (statusFilter !== "ALL" && a.status !== statusFilter) return false;
    return true;
  });

  const critCount = alerts.filter(a => a.severity === "CRITIQUE" && a.status === "ACTIF").length;
  const elevCount = alerts.filter(a => a.severity === "ÉLEVÉ").length;
  const resolvedCount = alerts.filter(a => a.status === "RÉSOLU").length;

  return (
    <div style={{ padding: 32, fontFamily: "sans-serif", maxWidth: 1100, margin: "0 auto" }}>
      <h1 style={{ fontSize: 26, fontWeight: "bold", color: "#1e293b", marginBottom: 4 }}>Centre d&apos;Alertes Risque</h1>
      <p style={{ color: "#6b7280", marginBottom: 24 }}>Alertes automatiques — dépassement de seuils CSDDD 2024/1760</p>

      {critCount > 0 && (
        <div style={{ background: "#fef2f2", border: "1px solid #fca5a5", borderRadius: 10, padding: "12px 20px", marginBottom: 24, display: "flex", alignItems: "center", gap: 12 }}>
          <span style={{ fontSize: 20 }}>🔴</span>
          <div>
            <strong style={{ color: "#dc2626" }}>{critCount} alerte{critCount > 1 ? "s" : ""} critique{critCount > 1 ? "s" : ""} active{critCount > 1 ? "s" : ""}</strong>
            <p style={{ margin: 0, fontSize: 13, color: "#7f1d1d" }}>Action corrective immédiate requise — conformité CSDDD 2024/1760</p>
          </div>
        </div>
      )}

      <div style={{ display: "flex", gap: 16, marginBottom: 24, flexWrap: "wrap" }}>
        {[
          { label: "CRITIQUE actives", value: critCount, color: "#dc2626" },
          { label: "ÉLEVÉ", value: elevCount, color: "#ea580c" },
          { label: "Alertes totales", value: alerts.length, color: "#374151" },
          { label: "Résolues", value: resolvedCount, color: "#16a34a" },
        ].map(c => (
          <div key={c.label} style={{ background: "#fff", border: "1px solid #e5e7eb", borderRadius: 10, padding: "12px 20px", minWidth: 140, textAlign: "center", boxShadow: "0 1px 3px rgba(0,0,0,0.06)" }}>
            <div style={{ fontSize: 26, fontWeight: "bold", color: c.color }}>{c.value}</div>
            <div style={{ fontSize: 12, color: "#6b7280" }}>{c.label}</div>
          </div>
        ))}
      </div>

      <div style={{ display: "flex", gap: 12, marginBottom: 20, flexWrap: "wrap" }}>
        <select value={sevFilter} onChange={e => setSevFilter(e.target.value)}
          style={{ padding: "6px 12px", borderRadius: 6, border: "1px solid #d1d5db", fontSize: 13 }}>
          <option value="ALL">Toutes sévérités</option>
          {(["CRITIQUE", "ÉLEVÉ", "MODÉRÉ", "INFO"] as const).map(s => <option key={s} value={s}>{s}</option>)}
        </select>
        <select value={statusFilter} onChange={e => setStatusFilter(e.target.value)}
          style={{ padding: "6px 12px", borderRadius: 6, border: "1px solid #d1d5db", fontSize: 13 }}>
          <option value="ALL">Tous statuts</option>
          {(["ACTIF", "ACQUITTÉ", "RÉSOLU"] as const).map(s => <option key={s} value={s}>{s}</option>)}
        </select>
        <span style={{ marginLeft: "auto", fontSize: 12, color: "#6b7280", alignSelf: "center" }}>{filtered.length} alertes</span>
      </div>

      <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
        {filtered.map(alert => (
          <div key={alert.id} style={{ background: SEV_BG[alert.severity], border: `1px solid ${SEV_COLOR[alert.severity]}40`, borderRadius: 10, overflow: "hidden" }}>
            <div onClick={() => setExpanded(expanded === alert.id ? null : alert.id)}
              style={{ display: "flex", alignItems: "center", gap: 12, padding: "12px 16px", cursor: "pointer" }}>
              <span style={{ fontSize: 12, fontWeight: 700, padding: "2px 10px", borderRadius: 9999, background: SEV_COLOR[alert.severity], color: "#fff", whiteSpace: "nowrap" }}>{alert.severity}</span>
              <span style={{ fontSize: 11, fontWeight: 600, padding: "2px 8px", borderRadius: 9999, border: `1px solid ${STATUS_COLOR[alert.status]}`, color: STATUS_COLOR[alert.status], whiteSpace: "nowrap" }}>{alert.status}</span>
              <span style={{ fontSize: 13, color: "#374151", flex: 1, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>{alert.message}</span>
              <span style={{ fontSize: 11, color: "#6b7280", whiteSpace: "nowrap" }}>{new Date(alert.triggeredAt).toLocaleString("fr-FR", { day: "2-digit", month: "2-digit", hour: "2-digit", minute: "2-digit" })}</span>
              <span style={{ color: "#9ca3af", fontSize: 14 }}>{expanded === alert.id ? "▲" : "▼"}</span>
            </div>
            {expanded === alert.id && (
              <div style={{ padding: "0 16px 16px", borderTop: `1px solid ${SEV_COLOR[alert.severity]}20` }}>
                <div style={{ display: "flex", gap: 24, flexWrap: "wrap", marginTop: 12, marginBottom: 12 }}>
                  <div><span style={{ fontSize: 11, color: "#6b7280" }}>Agent</span><div style={{ fontWeight: 600, fontSize: 13 }}>{alert.agentId}</div></div>
                  <div><span style={{ fontSize: 11, color: "#6b7280" }}>Entité</span><div style={{ fontWeight: 600, fontSize: 13, fontFamily: "monospace" }}>{alert.entityId}</div></div>
                  <div><span style={{ fontSize: 11, color: "#6b7280" }}>Score</span><div style={{ fontWeight: 700, fontSize: 18, color: SEV_COLOR[alert.severity] }}>{alert.score}</div></div>
                  <div><span style={{ fontSize: 11, color: "#6b7280" }}>Seuil</span><div style={{ fontWeight: 600, fontSize: 13 }}>{alert.threshold}</div></div>
                  <div><span style={{ fontSize: 11, color: "#6b7280" }}>Delta</span><div style={{ fontWeight: 700, fontSize: 14, color: SEV_COLOR[alert.severity] }}>+{(alert.score - alert.threshold).toFixed(0)}</div></div>
                </div>
                <div style={{ background: "#fff", borderRadius: 8, padding: 12, border: "1px solid #e5e7eb" }}>
                  <p style={{ fontWeight: 600, fontSize: 12, color: "#374151", marginBottom: 8 }}>Actions correctives requises :</p>
                  <ul style={{ margin: 0, paddingLeft: 20 }}>
                    {alert.actions.map((a, i) => <li key={i} style={{ fontSize: 13, color: "#374151", marginBottom: 4 }}>{a}</li>)}
                  </ul>
                </div>
              </div>
            )}
          </div>
        ))}
        {filtered.length === 0 && <div style={{ textAlign: "center", padding: 32, color: "#9ca3af" }}>Aucune alerte</div>}
      </div>
    </div>
  );
}
