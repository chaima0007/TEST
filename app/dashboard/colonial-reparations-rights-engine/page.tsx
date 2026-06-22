"use client";
import { useState, useEffect } from "react";

const ACCENT = "#6b3a2a";
const DOMAIN_SLUG = "colonial-reparations-rights-engine";

const RC: Record<string, string> = { critique: "text-red-400", "élevé": "text-orange-400", modéré: "text-yellow-400", faible: "text-emerald-400" };
const RB: Record<string, string> = { critique: "border-red-500/30 bg-red-500/10", "élevé": "border-orange-500/30 bg-orange-500/10", modéré: "border-yellow-500/30 bg-yellow-500/10", faible: "border-emerald-500/30 bg-emerald-500/10" };

const FALLBACK_ENTITIES = [
  { id: "CRR-001", name: "UK / British Museum", country: "United Kingdom", sector: "Cultural Institution", composite_score: 87.80, risk_level: "critique", primary_pattern: "Cultural Appropriation", key_signals: ["Elgin Marbles retention", "Benin Bronzes dispute", "Repatriation refusal"], last_updated: "2026-06-22" },
  { id: "CRR-002", name: "France / Louvre", country: "France", sector: "Cultural Institution", composite_score: 85.55, risk_level: "critique", primary_pattern: "Colonial Collection", key_signals: ["African art retention", "Partial restitution only", "Systemic legal barriers"], last_updated: "2026-06-22" },
  { id: "CRR-003", name: "Belgium / Congo", country: "Belgium", sector: "State Accountability", composite_score: 81.55, risk_level: "critique", primary_pattern: "Genocide Denial", key_signals: ["Congo Free State atrocities", "Royal Museum retention", "Partial acknowledgment"], last_updated: "2026-06-22" },
  { id: "CRR-004", name: "Netherlands / VOC", country: "Netherlands", sector: "State Accountability", composite_score: 75.80, risk_level: "critique", primary_pattern: "Trade Exploitation Legacy", key_signals: ["Slavery reparations delayed", "Indonesian artifacts", "Apology without compensation"], last_updated: "2026-06-22" },
  { id: "CRR-005", name: "Germany / Herero", country: "Germany", sector: "State Accountability", composite_score: 59.35, risk_level: "élevé", primary_pattern: "Genocide Acknowledgment Gap", key_signals: ["Herero-Nama genocide", "Compensation insufficiency", "Namibia negotiations"], last_updated: "2026-06-22" },
  { id: "CRR-006", name: "Portugal", country: "Portugal", sector: "State Accountability", composite_score: 53.35, risk_level: "élevé", primary_pattern: "Historical Denial", key_signals: ["Slave trade minimization", "Angola/Mozambique legacy", "Restitution absence"], last_updated: "2026-06-22" },
  { id: "CRR-007", name: "Italy", country: "Italy", sector: "State Accountability", composite_score: 34.40, risk_level: "modéré", primary_pattern: "Partial Engagement", key_signals: ["Libya reparations partial", "Ethiopian artifacts partial", "Ongoing dialogue"], last_updated: "2026-06-22" },
  { id: "CRR-008", name: "ICOM", country: "International", sector: "Cultural Governance", composite_score: 14.60, risk_level: "faible", primary_pattern: "Reform Engagement", key_signals: ["Repatriation guidelines", "Ethics framework update", "Member state cooperation"], last_updated: "2026-06-22" },
];

function GaugeRing({ value, stroke }: { value: number; stroke: string }) {
  const r = 36, cx = 44, cy = 44, circ = 2 * Math.PI * r;
  const pct = Math.min(Math.max(value, 0), 100) / 100;
  return (
    <svg viewBox="0 0 88 88" style={{ width: 80, height: 80 }}>
      <circle cx={cx} cy={cy} r={r} fill="none" stroke="#1e293b" strokeWidth={8} />
      <circle cx={cx} cy={cy} r={r} fill="none" stroke={stroke} strokeWidth={8}
        strokeDasharray={circ} strokeDashoffset={circ * (1 - pct)}
        strokeLinecap="round" transform="rotate(-90 44 44)" />
      <text x={cx} y={cy} textAnchor="middle" dominantBaseline="central"
        fill="white" fontSize={14} fontWeight="bold">{Math.round(value)}</text>
    </svg>
  );
}

interface CRREntity {
  id: string;
  name: string;
  country: string;
  sector: string;
  composite_score: number;
  risk_level: string;
  primary_pattern: string;
  key_signals: string[];
  last_updated: string;
  [key: string]: unknown;
}

interface CRRData {
  total_entities?: number;
  avg_composite?: number;
  risk_distribution?: Record<string, number>;
  confidence_score?: number;
  last_analysis?: string;
  entities: CRREntity[];
  [key: string]: unknown;
}

export default function ColonialReparationsRightsPage() {
  const [data, setData] = useState<CRRData | null>(null);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState("tous");
  const [selected, setSelected] = useState<CRREntity | null>(null);
  const [tab, setTab] = useState(0);

  useEffect(() => {
    fetch(`/api/${DOMAIN_SLUG}`)
      .then(r => r.json())
      .then(d => {
        const payload = d.payload ?? d;
        if (!payload.entities || payload.entities.length === 0) {
          setData({ ...payload, entities: FALLBACK_ENTITIES });
        } else {
          setData(payload);
        }
        setLoading(false);
      })
      .catch(() => {
        setData({ entities: FALLBACK_ENTITIES });
        setLoading(false);
      });
  }, []);

  if (loading) return (
    <div style={{ minHeight: "100vh", background: "#020617", display: "flex", alignItems: "center", justifyContent: "center" }}>
      <div style={{ color: ACCENT, animation: "pulse 2s infinite" }}>Chargement des données réparations coloniales…</div>
    </div>
  );
  if (!data) return (
    <div style={{ minHeight: "100vh", background: "#020617", display: "flex", alignItems: "center", justifyContent: "center" }}>
      <div style={{ color: "#f87171" }}>Données indisponibles</div>
    </div>
  );

  const entities: CRREntity[] = data.entities ?? FALLBACK_ENTITIES;
  const filtered = filter === "tous" ? entities : entities.filter(e => e.risk_level === filter);
  const total = data.total_entities ?? entities.length;
  const avgScore = data.avg_composite ?? (entities.length ? entities.reduce((a, e) => a + e.composite_score, 0) / entities.length : 0);
  const riskDist = data.risk_distribution ?? entities.reduce((acc, e) => { acc[e.risk_level] = (acc[e.risk_level] ?? 0) + 1; return acc; }, {} as Record<string, number>);

  return (
    <div style={{ minHeight: "100vh", background: "#020617", color: "white", padding: "24px" }}>
      <div style={{ maxWidth: 1200, margin: "0 auto 32px" }}>
        <div style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 8 }}>
          <div style={{ width: 12, height: 12, borderRadius: "50%", background: ACCENT }} />
          <h1 style={{ fontSize: 24, fontWeight: 700, letterSpacing: "-0.025em", margin: 0 }}>Réparations Coloniales</h1>
        </div>
        <p style={{ color: "#94a3b8", fontSize: 14, marginLeft: 24 }}>Colonial Reparations Rights Engine · Restitution, réparations et responsabilité coloniale</p>
      </div>

      <div style={{ maxWidth: 1200, margin: "0 auto" }}>
        {/* KPI Cards */}
        <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: 16, marginBottom: 24 }}>
          {[
            { label: "Entités", value: total },
            { label: "Score Moyen", value: avgScore.toFixed(1) },
            { label: "Critique", value: riskDist["critique"] ?? 0 },
            { label: "Élevé", value: riskDist["élevé"] ?? 0 },
            { label: "Modéré", value: riskDist["modéré"] ?? 0 },
            { label: "Confidence", value: data.confidence_score ? `${Math.round((data.confidence_score as number) * 100)}%` : "—" },
          ].map(k => (
            <div key={k.label} style={{ background: "#0f172a", border: "1px solid #1e293b", borderRadius: 12, padding: 16 }}>
              <div style={{ fontSize: 12, color: "#64748b", marginBottom: 4 }}>{k.label}</div>
              <div style={{ fontSize: 20, fontWeight: 700, color: ACCENT }}>{k.value}</div>
            </div>
          ))}
        </div>

        {/* Risk Distribution */}
        <div style={{ background: "#0f172a", border: "1px solid #1e293b", borderRadius: 12, padding: 20, marginBottom: 24 }}>
          <h2 style={{ fontSize: 12, fontWeight: 600, color: "#94a3b8", textTransform: "uppercase", letterSpacing: "0.1em", marginBottom: 12, marginTop: 0 }}>Distribution des Risques</h2>
          <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
            {[
              { label: "Critique", key: "critique", color: "#ef4444" },
              { label: "Élevé", key: "élevé", color: "#f97316" },
              { label: "Modéré", key: "modéré", color: "#eab308" },
              { label: "Faible", key: "faible", color: "#10b981" },
            ].map(({ label, key, color }) => {
              const val = riskDist[key] ?? 0;
              const pct = total > 0 ? Math.round(val / total * 100) : 0;
              return (
                <div key={key} style={{ display: "flex", alignItems: "center", gap: 12 }}>
                  <span style={{ fontSize: 12, color: "#94a3b8", width: 64, flexShrink: 0 }}>{label}</span>
                  <div style={{ flex: 1, height: 10, background: "#1e293b", borderRadius: 999, overflow: "hidden" }}>
                    <div style={{ height: "100%", width: `${pct}%`, background: color, borderRadius: 999 }} />
                  </div>
                  <span style={{ fontSize: 12, color: "#cbd5e1", width: 24, textAlign: "right" }}>{val}</span>
                </div>
              );
            })}
          </div>
        </div>

        {/* Filter pills */}
        <div style={{ display: "flex", gap: 8, flexWrap: "wrap", marginBottom: 24 }}>
          {["tous", "critique", "élevé", "modéré", "faible"].map(f => (
            <button key={f} onClick={() => setFilter(f)}
              style={{
                padding: "6px 16px", borderRadius: 999, fontSize: 14, border: "1px solid",
                borderColor: filter === f ? ACCENT : "#334155",
                background: filter === f ? ACCENT : "#1e293b",
                color: filter === f ? "white" : "#94a3b8",
                cursor: "pointer", textTransform: "capitalize"
              }}>
              {f}
            </button>
          ))}
        </div>

        {/* Entity grid */}
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(300px, 1fr))", gap: 16, marginBottom: 24 }}>
          {filtered.map(entity => (
            <div key={entity.id} onClick={() => { setSelected(entity); setTab(0); }}
              style={{
                background: "#0f172a", border: "1px solid",
                borderColor: entity.risk_level === "critique" ? "rgba(239,68,68,0.3)" : entity.risk_level === "élevé" ? "rgba(249,115,22,0.3)" : entity.risk_level === "modéré" ? "rgba(234,179,8,0.3)" : entity.risk_level === "faible" ? "rgba(16,185,129,0.3)" : "#1e293b",
                borderRadius: 12, padding: 16, cursor: "pointer"
              }}>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 12 }}>
                <div style={{ flex: 1, minWidth: 0 }}>
                  <p style={{ fontSize: 11, fontFamily: "monospace", color: "#64748b", margin: "0 0 2px" }}>{entity.id}</p>
                  <p style={{ fontSize: 14, fontWeight: 600, color: "white", margin: "0 0 2px", overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>{entity.name}</p>
                  <p style={{ fontSize: 12, color: "#64748b", margin: 0 }}>{entity.country}</p>
                </div>
                <GaugeRing value={entity.composite_score} stroke={ACCENT} />
              </div>
              <div style={{ display: "flex", justifyContent: "space-between", fontSize: 12 }}>
                <span style={{ color: RC[entity.risk_level] ?? "#94a3b8" }}>{entity.risk_level}</span>
                <span style={{ color: "#64748b" }}>{entity.sector}</span>
              </div>
            </div>
          ))}
        </div>

        <p style={{ fontSize: 12, color: "#475569", textAlign: "center" }}>Caelum Partners · Réparations Coloniales · {data.last_analysis ?? "2026-06-22"}</p>
      </div>

      {/* Detail Modal */}
      {selected && (
        <div style={{ position: "fixed", inset: 0, background: "rgba(0,0,0,0.7)", display: "flex", alignItems: "center", justifyContent: "center", zIndex: 50, padding: 16 }}
          onClick={() => setSelected(null)}>
          <div style={{ background: "#0f172a", border: "1px solid #334155", borderRadius: 16, width: "100%", maxWidth: 640, maxHeight: "85vh", overflowY: "auto" }}
            onClick={e => e.stopPropagation()}>
            <div style={{ padding: 24, borderBottom: "1px solid #1e293b", display: "flex", justifyContent: "space-between", alignItems: "flex-start" }}>
              <div>
                <p style={{ fontSize: 12, color: "#64748b", margin: "0 0 4px" }}>{selected.id}</p>
                <h3 style={{ fontWeight: 700, fontSize: 18, margin: "0 0 4px" }}>{selected.name}</h3>
                <p style={{ fontSize: 12, color: "#94a3b8", margin: "0 0 4px" }}>{selected.country} · {selected.sector}</p>
                <p style={{ fontSize: 12, fontWeight: 700, textTransform: "uppercase", margin: 0, color: RC[selected.risk_level] ?? "#94a3b8" }}>{selected.risk_level}</p>
              </div>
              <button onClick={() => setSelected(null)} style={{ color: "#64748b", background: "none", border: "none", fontSize: 24, cursor: "pointer", lineHeight: 1 }}>×</button>
            </div>
            <div style={{ display: "flex", borderBottom: "1px solid #1e293b" }}>
              {["Vue générale", "Signaux", "Pattern"].map((t, i) => (
                <button key={t} onClick={() => setTab(i)}
                  style={{
                    padding: "12px 24px", fontSize: 14, fontWeight: 500, background: "none", border: "none", cursor: "pointer",
                    borderBottom: tab === i ? `2px solid ${ACCENT}` : "2px solid transparent",
                    color: tab === i ? ACCENT : "#64748b"
                  }}>
                  {t}
                </button>
              ))}
            </div>
            <div style={{ padding: 24 }}>
              {tab === 0 && (
                <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
                  <div style={{ display: "flex", alignItems: "center", gap: 16 }}>
                    <GaugeRing value={selected.composite_score} stroke={ACCENT} />
                    <div>
                      <div style={{ fontSize: 28, fontWeight: 700, color: ACCENT }}>{selected.composite_score.toFixed(1)}</div>
                      <div style={{ fontSize: 12, color: "#94a3b8" }}>Score composite</div>
                    </div>
                  </div>
                  <div style={{ background: "#1e293b", borderRadius: 8, padding: 12 }}>
                    <div style={{ fontSize: 12, color: "#64748b", marginBottom: 4 }}>Pattern principal</div>
                    <div style={{ fontSize: 14, fontWeight: 600, color: "white" }}>{selected.primary_pattern}</div>
                  </div>
                  <div style={{ background: "#1e293b", borderRadius: 8, padding: 12 }}>
                    <div style={{ fontSize: 12, color: "#64748b", marginBottom: 4 }}>Dernière mise à jour</div>
                    <div style={{ fontSize: 14, color: "white" }}>{selected.last_updated}</div>
                  </div>
                </div>
              )}
              {tab === 1 && (
                <ul style={{ listStyle: "none", padding: 0, margin: 0, display: "flex", flexDirection: "column", gap: 8 }}>
                  {(selected.key_signals ?? []).map((s, i) => (
                    <li key={i} style={{ display: "flex", gap: 8, fontSize: 14, color: "#cbd5e1" }}>
                      <span style={{ color: ACCENT, flexShrink: 0, marginTop: 2 }}>▸</span>{s}
                    </li>
                  ))}
                </ul>
              )}
              {tab === 2 && (
                <div style={{ background: "#1e293b", borderRadius: 8, padding: 16 }}>
                  <div style={{ fontSize: 12, color: "#64748b", marginBottom: 8, textTransform: "uppercase", letterSpacing: "0.1em" }}>Pattern d&apos;Exploitation</div>
                  <div style={{ fontSize: 16, fontWeight: 600, color: "white" }}>{selected.primary_pattern}</div>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
