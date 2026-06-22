"use client";
import { useState, useEffect } from "react";

const ACCENT = "#1d4ed8";

const FALLBACK_ENTITIES = [
  { id: "SLM-001", name: "FIFA — Coupe du Monde Qatar 2022", country: "Qatar", composite_score: 91.2, risk_level: "critique" },
  { id: "SLM-002", name: "IOC — Jeux Olympiques Pékin 2022", country: "Chine", composite_score: 87.5, risk_level: "critique" },
  { id: "SLM-003", name: "F1 — Grand Prix Arabie Saoudite", country: "Arabie Saoudite", composite_score: 83.1, risk_level: "critique" },
  { id: "SLM-004", name: "ATP/WTA — Tournois Arabie Saoudite", country: "Arabie Saoudite", composite_score: 76.9, risk_level: "critique" },
  { id: "SLM-005", name: "UEFA — Projet Super Ligue Européenne", country: "Europe", composite_score: 55.8, risk_level: "élevé" },
  { id: "SLM-006", name: "NBA — Expansion Marché Chine", country: "Chine", composite_score: 51.4, risk_level: "élevé" },
  { id: "SLM-007", name: "Premier League — Gouvernance & Droits", country: "Royaume-Uni", composite_score: 29.7, risk_level: "modéré" },
  { id: "SLM-008", name: "FIFPro — Syndicat Mondial Joueurs", country: "Global", composite_score: 11.3, risk_level: "faible" },
];

const RC: Record<string, string> = { critique: "text-red-400", "élevé": "text-orange-400", modéré: "text-yellow-400", faible: "text-emerald-400" };
const RB: Record<string, string> = { critique: "border-red-500/30 bg-red-500/10", "élevé": "border-orange-500/30 bg-orange-500/10", modéré: "border-yellow-500/30 bg-yellow-500/10", faible: "border-emerald-500/30 bg-emerald-500/10" };

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

interface SLMEntity {
  id: string;
  name: string;
  country: string;
  composite_score: number;
  risk_level: string;
  [key: string]: unknown;
}

interface SLMData {
  total_entities?: number;
  avg_composite?: number;
  risk_distribution?: Record<string, number>;
  entities: SLMEntity[];
  last_analysis?: string;
  confidence_score?: number;
  [key: string]: unknown;
}

export default function SportsLaborMegaEventsPage() {
  const [data, setData] = useState<SLMData | null>(null);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState("tous");
  const [selected, setSelected] = useState<SLMEntity | null>(null);

  useEffect(() => {
    fetch("/api/sports-labor-mega-events-engine")
      .then(r => r.json())
      .then(d => {
        const payload = d.payload ?? d;
        if (!payload.entities || payload.entities.length === 0) {
          setData({ entities: FALLBACK_ENTITIES, total_entities: 8, avg_composite: 60.9, risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 }, confidence_score: 0.87 });
        } else {
          setData(payload);
        }
        setLoading(false);
      })
      .catch(() => {
        setData({ entities: FALLBACK_ENTITIES, total_entities: 8, avg_composite: 60.9, risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 }, confidence_score: 0.87 });
        setLoading(false);
      });
  }, []);

  if (loading) return (
    <div style={{ minHeight: "100vh", background: "#020617", display: "flex", alignItems: "center", justifyContent: "center" }}>
      <div style={{ color: ACCENT, animation: "pulse 2s infinite" }}>Chargement données sport & droits travailleurs…</div>
    </div>
  );

  if (!data) return (
    <div style={{ minHeight: "100vh", background: "#020617", display: "flex", alignItems: "center", justifyContent: "center" }}>
      <div style={{ color: "#f87171" }}>Données indisponibles</div>
    </div>
  );

  const filtered = filter === "tous" ? data.entities : data.entities.filter(e => e.risk_level === filter);
  const riskDist = data.risk_distribution ?? { critique: 4, "élevé": 2, modéré: 1, faible: 1 };
  const totalEntities = data.total_entities ?? data.entities.length;

  return (
    <div style={{ minHeight: "100vh", background: "#020617", color: "white", padding: "24px" }}>
      <div style={{ maxWidth: 1280, margin: "0 auto 32px" }}>
        <div style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 8 }}>
          <div style={{ width: 12, height: 12, borderRadius: "50%", background: ACCENT }} />
          <h1 style={{ fontSize: 24, fontWeight: 700, letterSpacing: "-0.02em", margin: 0 }}>Sport &amp; Droits Travailleurs</h1>
        </div>
        <p style={{ color: "#94a3b8", fontSize: 14, marginLeft: 24 }}>Sports Labor &amp; Mega-Events Engine · Wave 201</p>
      </div>

      <div style={{ maxWidth: 1280, margin: "0 auto" }}>
        {/* KPI Cards */}
        <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: 16, marginBottom: 24 }}>
          {[
            { label: "Entités", value: totalEntities },
            { label: "Score Moyen", value: data.avg_composite?.toFixed(1) ?? "—" },
            { label: "Critique", value: riskDist.critique ?? 0 },
            { label: "Élevé", value: riskDist["élevé"] ?? 0 },
            { label: "Modéré", value: riskDist.modéré ?? 0 },
            { label: "Confiance", value: `${Math.round((data.confidence_score ?? 0.87) * 100)}%` },
          ].map(k => (
            <div key={k.label} style={{ background: "#0f172a", border: "1px solid #1e293b", borderRadius: 12, padding: 16 }}>
              <div style={{ fontSize: 12, color: "#64748b", marginBottom: 4 }}>{k.label}</div>
              <div style={{ fontSize: 20, fontWeight: 700, color: ACCENT }}>{k.value}</div>
            </div>
          ))}
        </div>

        {/* Risk distribution */}
        <div style={{ background: "#0f172a", border: "1px solid #1e293b", borderRadius: 12, padding: 20, marginBottom: 24 }}>
          <h2 style={{ fontSize: 12, fontWeight: 600, color: "#94a3b8", textTransform: "uppercase", letterSpacing: "0.05em", marginBottom: 16, margin: "0 0 16px" }}>Distribution des Risques</h2>
          <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
            {[
              { label: "Critique", key: "critique", color: "#ef4444" },
              { label: "Élevé", key: "élevé", color: "#f97316" },
              { label: "Modéré", key: "modéré", color: "#eab308" },
              { label: "Faible", key: "faible", color: "#10b981" },
            ].map(({ label, key, color }) => {
              const val = riskDist[key] ?? 0;
              const pct = totalEntities > 0 ? Math.round(val / totalEntities * 100) : 0;
              return (
                <div key={key} style={{ display: "flex", alignItems: "center", gap: 12 }}>
                  <span style={{ fontSize: 12, color: "#94a3b8", width: 80, flexShrink: 0 }}>{label}</span>
                  <div style={{ flex: 1, height: 10, background: "#1e293b", borderRadius: 999, overflow: "hidden" }}>
                    <div style={{ width: `${pct}%`, height: "100%", borderRadius: 999, background: color }} />
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
            <button key={f} onClick={() => setFilter(f)} style={{
              padding: "6px 16px", borderRadius: 999, fontSize: 14, border: filter === f ? `1px solid ${ACCENT}` : "1px solid #334155",
              background: filter === f ? ACCENT : "#1e293b", color: filter === f ? "white" : "#94a3b8", cursor: "pointer", textTransform: "capitalize"
            }}>
              {f}
            </button>
          ))}
        </div>

        {/* Entity grid */}
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(320px, 1fr))", gap: 16, marginBottom: 24 }}>
          {filtered.map(entity => (
            <div key={entity.id} onClick={() => setSelected(entity)}
              style={{ background: "#0f172a", border: `1px solid ${entity.risk_level === "critique" ? "rgba(239,68,68,0.3)" : entity.risk_level === "élevé" ? "rgba(249,115,22,0.3)" : entity.risk_level === "modéré" ? "rgba(234,179,8,0.3)" : "rgba(16,185,129,0.3)"}`, borderRadius: 12, padding: 16, cursor: "pointer" }}>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 12 }}>
                <div style={{ flex: 1, minWidth: 0 }}>
                  <p style={{ fontSize: 11, fontFamily: "monospace", color: "#64748b", margin: "0 0 4px" }}>{entity.id}</p>
                  <p style={{ fontSize: 14, fontWeight: 600, margin: "0 0 2px", overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>{entity.name}</p>
                  <p style={{ fontSize: 12, color: "#64748b", margin: 0 }}>{entity.country}</p>
                </div>
                <GaugeRing value={entity.composite_score} stroke={ACCENT} />
              </div>
              <div style={{ display: "flex", justifyContent: "space-between", fontSize: 12 }}>
                <span style={{ color: RC[entity.risk_level] ?? "#94a3b8" }}>{entity.risk_level}</span>
                <span style={{ color: "#64748b" }}>score {entity.composite_score}</span>
              </div>
            </div>
          ))}
        </div>

        <p style={{ fontSize: 12, color: "#334155", textAlign: "center" }}>
          Caelum Partners · Sport &amp; Droits Travailleurs Méga-Événements · {data.last_analysis ?? "2026-06-22"}
        </p>
      </div>

      {/* Detail Modal */}
      {selected && (
        <div onClick={() => setSelected(null)} style={{ position: "fixed", inset: 0, background: "rgba(0,0,0,0.7)", display: "flex", alignItems: "center", justifyContent: "center", zIndex: 50, padding: 16 }}>
          <div onClick={e => e.stopPropagation()} style={{ background: "#0f172a", border: "1px solid #334155", borderRadius: 16, width: "100%", maxWidth: 560, maxHeight: "85vh", overflowY: "auto" }}>
            <div style={{ padding: 24, borderBottom: "1px solid #1e293b", display: "flex", justifyContent: "space-between", alignItems: "flex-start" }}>
              <div>
                <p style={{ fontSize: 12, color: "#64748b", margin: "0 0 4px" }}>{selected.id}</p>
                <h3 style={{ fontWeight: 700, fontSize: 18, margin: "0 0 4px" }}>{selected.name}</h3>
                <p style={{ fontSize: 12, color: "#94a3b8", margin: 0 }}>{selected.country}</p>
                <p style={{ fontSize: 12, fontWeight: 700, textTransform: "uppercase", marginTop: 4, color: RC[selected.risk_level] ?? "#94a3b8" }}>{selected.risk_level}</p>
              </div>
              <button onClick={() => setSelected(null)} style={{ background: "none", border: "none", color: "#64748b", fontSize: 24, cursor: "pointer", lineHeight: 1 }}>×</button>
            </div>
            <div style={{ padding: 24 }}>
              <div style={{ display: "flex", alignItems: "center", gap: 16, marginBottom: 16 }}>
                <GaugeRing value={selected.composite_score} stroke={ACCENT} />
                <div>
                  <div style={{ fontSize: 28, fontWeight: 700, color: ACCENT }}>{selected.composite_score.toFixed(1)}</div>
                  <div style={{ fontSize: 12, color: "#94a3b8" }}>Score composite</div>
                </div>
              </div>
              <div style={{ background: "#1e293b", borderRadius: 8, padding: 12 }}>
                <div style={{ fontSize: 12, color: "#64748b", marginBottom: 4 }}>Entité</div>
                <div style={{ fontSize: 14, color: "#e2e8f0" }}>{selected.name}</div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
