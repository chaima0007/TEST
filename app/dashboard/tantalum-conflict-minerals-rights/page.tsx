"use client";
import { useEffect, useState } from "react";

const RC: Record<string, string> = { critique: "text-red-400", "élevé": "text-orange-400", modéré: "text-yellow-400", faible: "text-emerald-400" };
const RB: Record<string, string> = { critique: "border-red-500/30 bg-red-500/10", "élevé": "border-orange-500/30 bg-orange-500/10", modéré: "border-yellow-500/30 bg-yellow-500/10", faible: "border-emerald-500/30 bg-emerald-500/10" };

const ACCENT = "#7c3aed";

interface Entity {
  id: string;
  name: string;
  country: string;
  composite_score: number;
  risk_level: string;
  primary_pattern: string;
  estimated_tantalum_conflict_minerals_rights_index: number;
  [key: string]: unknown;
}

interface DashData {
  total_entities?: number;
  avg_composite?: number;
  avg_estimated_tantalum_conflict_minerals_rights_index?: number;
  risk_distribution?: Record<string, number>;
  confidence_score?: number;
  data_sources?: string[];
  entities?: Entity[];
  [key: string]: unknown;
}

function GaugeRing({ score }: { score: number }) {
  const r = 36, cx = 44, cy = 44, sw = 8;
  const circ = 2 * Math.PI * r;
  const pct = Math.max(0, Math.min(100, score));
  const offset = circ * (1 - pct / 100);
  const color = score >= 60 ? "#dc2626" : score >= 40 ? "#f97316" : score >= 20 ? "#eab308" : "#22c55e";
  return (
    <svg viewBox="0 0 88 88" width={88} height={88}>
      <circle cx={cx} cy={cy} r={r} fill="none" stroke="#e5e7eb" strokeWidth={sw} />
      <circle cx={cx} cy={cy} r={r} fill="none" stroke={color} strokeWidth={sw}
        strokeDasharray={circ} strokeDashoffset={offset}
        strokeLinecap="round" transform={`rotate(-90 ${cx} ${cy})`} />
      <text x={cx} y={cy} textAnchor="middle" dominantBaseline="central"
        style={{ fontSize: 16, fontWeight: 700, fill: color }}>{score}</text>
    </svg>
  );
}

function DetailModal({ entity, onClose }: { entity: Entity; onClose: () => void }) {
  return (
    <div style={{ position: "fixed", inset: 0, background: "rgba(0,0,0,0.5)", zIndex: 50, display: "flex", alignItems: "center", justifyContent: "center" }} onClick={onClose}>
      <div style={{ background: "#0f172a", border: "1px solid #334155", borderRadius: 12, padding: 24, maxWidth: 480, width: "90%", maxHeight: "80vh", overflowY: "auto" }} onClick={e => e.stopPropagation()}>
        <h3 style={{ fontWeight: 700, fontSize: 18, marginBottom: 12, color: "#fff" }}>{entity.name}</h3>
        <div style={{ display: "flex", gap: 8, marginBottom: 16 }}>
          {["Analyse", "Entités", "Méthodologie"].map(tab => (
            <span key={tab} style={{ padding: "4px 12px", borderRadius: 20, background: "#1e293b", fontSize: 13, color: "#94a3b8" }}>{tab}</span>
          ))}
        </div>
        <p style={{ color: "#64748b", fontSize: 14 }}>Score composite : <strong style={{ color: "#fff" }}>{entity.composite_score}</strong></p>
        <p style={{ color: "#64748b", fontSize: 14 }}>Niveau de risque : <strong style={{ color: "#fff" }}>{entity.risk_level}</strong></p>
        <p style={{ color: "#64748b", fontSize: 14 }}>Pattern principal : <strong style={{ color: "#fff" }}>{entity.primary_pattern}</strong></p>
        <button onClick={onClose} style={{ marginTop: 16, padding: "8px 20px", background: "#1e293b", color: "#fff", borderRadius: 8, border: "none", cursor: "pointer" }}>Fermer</button>
      </div>
    </div>
  );
}

export default function TantalumConflictMineralsRightsPage() {
  const [data, setData] = useState<DashData | null>(null);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState("tous");
  const [selected, setSelected] = useState<Entity | null>(null);

  useEffect(() => {
    fetch("/api/tantalum-conflict-minerals-rights")
      .then(r => r.json())
      .then(d => { setData(d.payload ?? d); setLoading(false); })
      .catch(() => { setLoading(false); });
  }, []);

  if (loading) {
    return (
      <div style={{ background: "#020617", minHeight: "100vh", display: "flex", alignItems: "center", justifyContent: "center" }}>
        <div style={{ color: ACCENT, fontSize: 14 }}>Initialisation Droits — Tantale et Minerais de Conflit…</div>
      </div>
    );
  }

  const allEntities: Entity[] = data?.entities ?? [];
  const filtered = filter === "tous" ? allEntities : allEntities.filter(e => e.risk_level === filter);
  const avg = (arr: number[]) => arr.length ? arr.reduce((a, b) => a + b, 0) / arr.length : 0;
  const avgComposite = data?.avg_composite ?? avg(allEntities.map(e => e.composite_score));
  const avgIndex = data?.avg_estimated_tantalum_conflict_minerals_rights_index ?? avg(allEntities.map(e => e.estimated_tantalum_conflict_minerals_rights_index));
  const rd = data?.risk_distribution ?? {};
  const countCritique = rd["critique"] ?? allEntities.filter(e => e.risk_level === "critique").length;
  const countEleve = rd["élevé"] ?? allEntities.filter(e => e.risk_level === "élevé").length;
  const sources = data?.data_sources ?? [];
  const confidence = typeof data?.confidence_score === "number" ? `${(data.confidence_score * 100).toFixed(0)}%` : "—";

  const kpis = [
    { label: "Entités Analysées", value: data?.total_entities ?? allEntities.length },
    { label: "Score Moyen", value: avgComposite.toFixed(1) },
    { label: "Index Tantale", value: avgIndex.toFixed(2) },
    { label: "Confiance", value: confidence },
    { label: "Critique", value: countCritique },
    { label: "Élevé", value: countEleve },
  ];

  const filters = ["tous", "critique", "élevé", "modéré", "faible"];

  return (
    <div style={{ minHeight: "100vh", background: "#020617", color: "#fff", padding: 24, display: "flex", flexDirection: "column", gap: 24 }}>
      {selected && <DetailModal entity={selected} onClose={() => setSelected(null)} />}

      {/* Header */}
      <div>
        <div style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 4 }}>
          <div style={{ width: 4, height: 32, borderRadius: 4, background: ACCENT }} />
          <h1 style={{ fontSize: 24, fontWeight: 700, letterSpacing: "-0.02em" }}>Droits — Tantale et Minerais de Conflit</h1>
        </div>
        <p style={{ color: "#94a3b8", fontSize: 14, marginLeft: 16 }}>
          Tantalum Conflict Minerals Rights Engine — Caelum Partners · Chaima Mhadbi, Fondatrice, Bruxelles
        </p>
      </div>

      {/* KPI Cards */}
      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(140px, 1fr))", gap: 16 }}>
        {kpis.map(k => (
          <div key={k.label} style={{ background: "#0f172a", border: "1px solid #1e293b", borderRadius: 12, padding: 16 }}>
            <div style={{ color: "#64748b", fontSize: 11, marginBottom: 4 }}>{k.label}</div>
            <div style={{ fontSize: 20, fontWeight: 700, color: ACCENT }}>{k.value}</div>
          </div>
        ))}
      </div>

      {/* Gauge Rings */}
      <div style={{ background: "#0f172a", border: "1px solid #1e293b", borderRadius: 12, padding: 20 }}>
        <h2 style={{ fontSize: 13, fontWeight: 600, color: "#94a3b8", marginBottom: 16 }}>Scores Moyens par Dimension</h2>
        <div style={{ display: "flex", gap: 32, flexWrap: "wrap", justifyContent: "space-around" }}>
          <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 8 }}>
            <GaugeRing score={Math.round(avgComposite)} />
            <span style={{ fontSize: 12, color: "#94a3b8" }}>Score Composite</span>
          </div>
          <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 8 }}>
            <GaugeRing score={Math.round(avgIndex * 10)} />
            <span style={{ fontSize: 12, color: "#94a3b8" }}>Index Tantale (×10)</span>
          </div>
          <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 8 }}>
            <GaugeRing score={countCritique > 0 ? Math.round((countCritique / Math.max(allEntities.length, 1)) * 100) : 0} />
            <span style={{ fontSize: 12, color: "#94a3b8" }}>% Critique</span>
          </div>
        </div>
      </div>

      {/* Filter Pills */}
      <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
        {filters.map(f => (
          <button key={f} onClick={() => setFilter(f)}
            style={{
              padding: "6px 16px", borderRadius: 20, fontSize: 13, fontWeight: 500, border: "none", cursor: "pointer",
              background: filter === f ? ACCENT : "#1e293b",
              color: filter === f ? "#fff" : "#94a3b8",
            }}>
            {f.charAt(0).toUpperCase() + f.slice(1)}
          </button>
        ))}
      </div>

      {/* Entity Grid */}
      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(300px, 1fr))", gap: 16 }}>
        {filtered.map(e => (
          <div key={e.id} onClick={() => setSelected(e)}
            style={{
              border: "1px solid",
              borderColor: e.risk_level === "critique" ? "rgba(239,68,68,0.3)" : e.risk_level === "élevé" ? "rgba(249,115,22,0.3)" : e.risk_level === "modéré" ? "rgba(234,179,8,0.3)" : "rgba(34,197,94,0.3)",
              background: e.risk_level === "critique" ? "rgba(239,68,68,0.07)" : e.risk_level === "élevé" ? "rgba(249,115,22,0.07)" : e.risk_level === "modéré" ? "rgba(234,179,8,0.07)" : "rgba(34,197,94,0.07)",
              borderRadius: 12, padding: 16, cursor: "pointer",
            }}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 8 }}>
              <div style={{ flex: 1, minWidth: 0 }}>
                <div style={{ fontWeight: 600, fontSize: 13, lineHeight: 1.4, color: "#fff" }}>{e.name}</div>
                <div style={{ fontSize: 11, color: "#94a3b8", marginTop: 4 }}>{e.country}</div>
              </div>
              <div style={{ textAlign: "right", marginLeft: 12, flexShrink: 0 }}>
                <div style={{ fontSize: 20, fontWeight: 700, color: "#fff" }}>{typeof e.composite_score === "number" ? e.composite_score.toFixed(1) : "—"}</div>
                <div style={{ fontSize: 10, fontWeight: 700, textTransform: "uppercase", marginTop: 2 }}
                  className={RC[e.risk_level] ?? "text-slate-400"}>{e.risk_level}</div>
              </div>
            </div>
            <div style={{ height: 4, background: "#1e293b", borderRadius: 4, overflow: "hidden", marginTop: 8 }}>
              <div style={{ height: "100%", borderRadius: 4, background: ACCENT, width: `${Math.min(typeof e.composite_score === "number" ? e.composite_score : 0, 100)}%` }} />
            </div>
            <div style={{ fontSize: 11, color: "#64748b", marginTop: 8 }}>
              Index Tantale: <span style={{ fontWeight: 600, color: ACCENT }}>{typeof e.estimated_tantalum_conflict_minerals_rights_index === "number" ? e.estimated_tantalum_conflict_minerals_rights_index.toFixed(2) : "—"}</span>
            </div>
          </div>
        ))}
      </div>

      {filtered.length === 0 && (
        <div style={{ textAlign: "center", padding: "48px 0", color: "#64748b", fontSize: 14 }}>Aucune entité pour ce niveau de risque.</div>
      )}

      {/* Sources */}
      {sources.length > 0 && (
        <div style={{ background: "#0f172a", border: "1px solid #1e293b", borderRadius: 12, padding: 16 }}>
          <h3 style={{ color: "#94a3b8", fontSize: 11, textTransform: "uppercase", letterSpacing: "0.08em", marginBottom: 12 }}>Sources de données</h3>
          <div style={{ display: "flex", flexWrap: "wrap", gap: 8 }}>
            {sources.map((src) => (
              <span key={src} style={{ fontSize: 11, background: "#1e293b", color: "#94a3b8", padding: "4px 12px", borderRadius: 20, border: "1px solid rgba(51,65,85,0.5)" }}>{src}</span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
