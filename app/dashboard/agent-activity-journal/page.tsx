"use client";
import { useEffect, useState } from "react";

type EventType = "SCAN_STARTED" | "SCORE_COMPUTED" | "THRESHOLD_BREACH" | "ALERT_TRIGGERED" | "CERT_VERIFIED" | "UPSTREAM_ERROR" | "REVALIDATION" | "RISK_ELEVATED";

interface JournalEntry {
  id: string;
  timestamp: string;
  eventType: EventType;
  agentId: string;
  entityId?: string;
  score?: number;
  riskLevel?: string;
  message: string;
}

const EVENT_COLOR: Record<string, string> = {
  SCAN_STARTED: "#6366f1",
  SCORE_COMPUTED: "#0369a1",
  RISK_ELEVATED: "#ea580c",
  THRESHOLD_BREACH: "#dc2626",
  ALERT_TRIGGERED: "#b91c1c",
  CERT_VERIFIED: "#16a34a",
  UPSTREAM_ERROR: "#9f1239",
  REVALIDATION: "#6b7280",
};

const EVENT_ICON: Record<string, string> = {
  SCAN_STARTED: "▶",
  SCORE_COMPUTED: "📊",
  RISK_ELEVATED: "⬆",
  THRESHOLD_BREACH: "⚠",
  ALERT_TRIGGERED: "🔴",
  CERT_VERIFIED: "✓",
  UPSTREAM_ERROR: "✗",
  REVALIDATION: "↻",
};

const MOCK_AGENTS = [
  "influencer-marketing-agency", "content-creator-platform", "brand-ambassador-program",
  "micro-influencer-network", "viral-content-marketing", "user-generated-content",
  "podcast-advertising", "streaming-content", "augmented-reality-ads",
];

function generateMockJournal(): JournalEntry[] {
  const entries: JournalEntry[] = [];
  const now = Date.now();
  for (const agent of MOCK_AGENTS) {
    const base = now - Math.random() * 3600000;
    entries.push({ id: Math.random().toString(36).slice(2), timestamp: new Date(base).toISOString(), eventType: "SCAN_STARTED", agentId: agent, message: `Analyse démarrée — ${agent}` });
    const scores = [96, 89, 82, 76, 58, 47, 29, 10];
    const risks = ["critique", "critique", "critique", "critique", "élevé", "élevé", "modéré", "faible"];
    scores.forEach((sc, i) => {
      const eid = `${agent.slice(0, 3).toUpperCase()}-00${i + 1}`;
      entries.push({ id: Math.random().toString(36).slice(2), timestamp: new Date(base + 5000 + i * 3000).toISOString(), eventType: "SCORE_COMPUTED", agentId: agent, entityId: eid, score: sc, riskLevel: risks[i], message: `Score ${sc} — risque ${risks[i]}` });
      if (sc >= 60) {
        entries.push({ id: Math.random().toString(36).slice(2), timestamp: new Date(base + 10000 + i * 3000).toISOString(), eventType: "THRESHOLD_BREACH", agentId: agent, entityId: eid, score: sc, message: `⚠ Seuil critique dépassé (${sc} ≥ 60) — ${eid}` });
        entries.push({ id: Math.random().toString(36).slice(2), timestamp: new Date(base + 15000 + i * 3000).toISOString(), eventType: "ALERT_TRIGGERED", agentId: agent, entityId: eid, score: sc, message: `🔴 Alerte déclenchée — action corrective requise` });
      }
    });
    entries.push({ id: Math.random().toString(36).slice(2), timestamp: new Date(base + 120000).toISOString(), eventType: "REVALIDATION", agentId: agent, message: `Revalidation ISR planifiée — 30 s` });
  }
  return entries.sort((a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime());
}

export default function AgentActivityJournalPage() {
  const [entries, setEntries] = useState<JournalEntry[]>([]);
  const [filter, setFilter] = useState<string>("ALL");
  const [agentFilter, setAgentFilter] = useState<string>("ALL");
  const [search, setSearch] = useState("");
  const [page, setPage] = useState(0);
  const PAGE_SIZE = 25;

  useEffect(() => { setEntries(generateMockJournal()); }, []);

  const filtered = entries.filter(e => {
    if (filter !== "ALL" && e.eventType !== filter) return false;
    if (agentFilter !== "ALL" && e.agentId !== agentFilter) return false;
    if (search && !e.message.toLowerCase().includes(search.toLowerCase()) && !(e.entityId ?? "").toLowerCase().includes(search.toLowerCase())) return false;
    return true;
  });

  const paginated = filtered.slice(page * PAGE_SIZE, (page + 1) * PAGE_SIZE);
  const totalPages = Math.ceil(filtered.length / PAGE_SIZE);

  const criticalCount = entries.filter(e => e.eventType === "THRESHOLD_BREACH").length;
  const alertCount = entries.filter(e => e.eventType === "ALERT_TRIGGERED").length;
  const agentCount = new Set(entries.map(e => e.agentId)).size;

  return (
    <div style={{ padding: 32, fontFamily: "sans-serif", maxWidth: 1100, margin: "0 auto" }}>
      <h1 style={{ fontSize: 26, fontWeight: "bold", color: "#1e293b", marginBottom: 4 }}>Journal d&apos;Activité des Agents</h1>
      <p style={{ color: "#6b7280", marginBottom: 24 }}>Traçabilité en temps réel — tous les événements CaelumSwarm™</p>

      <div style={{ display: "flex", gap: 16, marginBottom: 24, flexWrap: "wrap" }}>
        {[
          { label: "Agents actifs", value: agentCount, color: "#6366f1" },
          { label: "Événements totaux", value: entries.length, color: "#0369a1" },
          { label: "Seuils dépassés", value: criticalCount, color: "#dc2626" },
          { label: "Alertes déclenchées", value: alertCount, color: "#b91c1c" },
        ].map(card => (
          <div key={card.label} style={{ background: "#fff", border: "1px solid #e5e7eb", borderRadius: 10, padding: "12px 20px", minWidth: 150, textAlign: "center", boxShadow: "0 1px 3px rgba(0,0,0,0.06)" }}>
            <div style={{ fontSize: 28, fontWeight: "bold", color: card.color }}>{card.value}</div>
            <div style={{ fontSize: 12, color: "#6b7280" }}>{card.label}</div>
          </div>
        ))}
      </div>

      <div style={{ display: "flex", gap: 12, marginBottom: 20, flexWrap: "wrap", alignItems: "center" }}>
        <input value={search} onChange={e => { setSearch(e.target.value); setPage(0); }}
          placeholder="Rechercher…" style={{ padding: "6px 12px", borderRadius: 6, border: "1px solid #d1d5db", fontSize: 13, minWidth: 200 }} />
        <select value={filter} onChange={e => { setFilter(e.target.value); setPage(0); }}
          style={{ padding: "6px 12px", borderRadius: 6, border: "1px solid #d1d5db", fontSize: 13 }}>
          <option value="ALL">Tous les événements</option>
          {Object.keys(EVENT_COLOR).map(k => <option key={k} value={k}>{k}</option>)}
        </select>
        <select value={agentFilter} onChange={e => { setAgentFilter(e.target.value); setPage(0); }}
          style={{ padding: "6px 12px", borderRadius: 6, border: "1px solid #d1d5db", fontSize: 13 }}>
          <option value="ALL">Tous les agents</option>
          {MOCK_AGENTS.map(a => <option key={a} value={a}>{a}</option>)}
        </select>
        <span style={{ marginLeft: "auto", fontSize: 12, color: "#6b7280" }}>{filtered.length} résultats</span>
      </div>

      <div style={{ background: "#fff", border: "1px solid #e5e7eb", borderRadius: 10, overflow: "hidden" }}>
        <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 13 }}>
          <thead>
            <tr style={{ background: "#f8fafc", borderBottom: "1px solid #e5e7eb" }}>
              {["Horodatage", "Événement", "Agent", "Entité", "Score", "Message"].map(h => (
                <th key={h} style={{ padding: "10px 14px", textAlign: "left", fontWeight: 600, color: "#374151", fontSize: 12, textTransform: "uppercase", letterSpacing: "0.05em" }}>{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {paginated.map((entry, i) => (
              <tr key={entry.id} style={{ borderBottom: "1px solid #f1f5f9", background: i % 2 === 0 ? "#fff" : "#fafafa" }}>
                <td style={{ padding: "8px 14px", color: "#6b7280", whiteSpace: "nowrap", fontFamily: "monospace", fontSize: 11 }}>
                  {new Date(entry.timestamp).toLocaleString("fr-FR", { day: "2-digit", month: "2-digit", hour: "2-digit", minute: "2-digit", second: "2-digit" })}
                </td>
                <td style={{ padding: "8px 14px" }}>
                  <span style={{ display: "inline-flex", alignItems: "center", gap: 4, fontSize: 11, fontWeight: 600, padding: "2px 8px", borderRadius: 9999, background: (EVENT_COLOR[entry.eventType] ?? "#6b7280") + "18", color: EVENT_COLOR[entry.eventType] ?? "#6b7280" }}>
                    {EVENT_ICON[entry.eventType] ?? "•"} {entry.eventType}
                  </span>
                </td>
                <td style={{ padding: "8px 14px", fontSize: 11, color: "#374151", maxWidth: 180, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>{entry.agentId}</td>
                <td style={{ padding: "8px 14px", fontFamily: "monospace", fontSize: 11, color: "#6b7280" }}>{entry.entityId ?? "—"}</td>
                <td style={{ padding: "8px 14px", fontWeight: 600, color: entry.score !== undefined ? (entry.score >= 60 ? "#dc2626" : entry.score >= 40 ? "#ea580c" : "#16a34a") : "#6b7280" }}>
                  {entry.score !== undefined ? entry.score : "—"}
                </td>
                <td style={{ padding: "8px 14px", color: "#374151", maxWidth: 320, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>{entry.message}</td>
              </tr>
            ))}
            {paginated.length === 0 && (
              <tr><td colSpan={6} style={{ padding: 32, textAlign: "center", color: "#9ca3af" }}>Aucun événement trouvé</td></tr>
            )}
          </tbody>
        </table>
      </div>

      {totalPages > 1 && (
        <div style={{ display: "flex", gap: 8, justifyContent: "center", marginTop: 16 }}>
          <button onClick={() => setPage(p => Math.max(0, p - 1))} disabled={page === 0}
            style={{ padding: "6px 14px", borderRadius: 6, border: "1px solid #d1d5db", cursor: page === 0 ? "not-allowed" : "pointer", background: "#fff", color: "#374151" }}>←</button>
          <span style={{ padding: "6px 14px", fontSize: 13, color: "#6b7280" }}>Page {page + 1} / {totalPages}</span>
          <button onClick={() => setPage(p => Math.min(totalPages - 1, p + 1))} disabled={page >= totalPages - 1}
            style={{ padding: "6px 14px", borderRadius: 6, border: "1px solid #d1d5db", cursor: page >= totalPages - 1 ? "not-allowed" : "pointer", background: "#fff", color: "#374151" }}>→</button>
        </div>
      )}
    </div>
  );
}
