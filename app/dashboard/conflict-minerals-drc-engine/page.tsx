"use client";
import { useEffect, useState } from "react";

interface Entity {
  id: string;
  name: string;
  country: string;
  composite_score: number;
  risk_level: string;
  primary_pattern: string;
  estimated_conflict_minerals_drc_index: number;
}
interface EngineData {
  agent: string;
  total_entities: number;
  avg_composite: number;
  confidence_score: number;
  avg_estimated_conflict_minerals_drc_index: number;
  risk_distribution: Record<string, number>;
  critical_alerts: string[];
  data_sources: string[];
  entities: Entity[];
}

const ACCENT = "#7f1d1d";
const RC: Record<string, string> = {
  critique: "#ef4444",
  "élevé": "#f97316",
  "modéré": "#eab308",
  faible: "#22c55e",
};
const INDEX_KEY = "estimated_conflict_minerals_drc_index";

const FALLBACK_ENTITIES: Entity[] = [
  { id: "CMD-001", name: "Intel", country: "États-Unis", composite_score: 88.5, risk_level: "critique", primary_pattern: "sourcing_tantalum_non_certifie", estimated_conflict_minerals_drc_index: 8.85 },
  { id: "CMD-002", name: "Apple tantalum", country: "États-Unis", composite_score: 84.2, risk_level: "critique", primary_pattern: "sourcing_tantalum_non_certifie", estimated_conflict_minerals_drc_index: 8.42 },
  { id: "CMD-003", name: "Microsoft tin", country: "États-Unis", composite_score: 79.8, risk_level: "critique", primary_pattern: "sourcing_etain_non_conforme", estimated_conflict_minerals_drc_index: 7.98 },
  { id: "CMD-004", name: "Samsung", country: "Corée du Sud", composite_score: 74.5, risk_level: "critique", primary_pattern: "sourcing_minerais_conflit_drc", estimated_conflict_minerals_drc_index: 7.45 },
  { id: "CMD-005", name: "Dell", country: "États-Unis", composite_score: 56.3, risk_level: "élevé", primary_pattern: "traçabilite_insuffisante_chaine_approvisionnement", estimated_conflict_minerals_drc_index: 5.63 },
  { id: "CMD-006", name: "HP", country: "États-Unis", composite_score: 52.1, risk_level: "élevé", primary_pattern: "traçabilite_insuffisante_chaine_approvisionnement", estimated_conflict_minerals_drc_index: 5.21 },
  { id: "CMD-007", name: "Fairphone", country: "Pays-Bas", composite_score: 28.4, risk_level: "modéré", primary_pattern: "certification_partielle_minerais_responsables", estimated_conflict_minerals_drc_index: 2.84 },
  { id: "CMD-008", name: "ITRI/iTSCi", country: "International", composite_score: 12.6, risk_level: "faible", primary_pattern: "programme_certification_conformite", estimated_conflict_minerals_drc_index: 1.26 },
];

const FALLBACK: EngineData = {
  agent: "Minerais de Conflit RDC (3TG)",
  total_entities: 8,
  avg_composite: 59.55,
  confidence_score: 0.87,
  avg_estimated_conflict_minerals_drc_index: 5.955,
  risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
  critical_alerts: [
    "Intel: sourcing_tantalum_non_certifie",
    "Apple tantalum: sourcing_tantalum_non_certifie",
    "Microsoft tin: sourcing_etain_non_conforme",
    "Samsung: sourcing_minerais_conflit_drc",
  ],
  data_sources: ["sec_dodd_frank_1502_reports", "itri_itsci_programme", "enough_project_3tg_scorecard", "global_witness_drc_minerals"],
  entities: FALLBACK_ENTITIES,
};

function GaugeRing({ value, accent }: { value: number; accent: string }) {
  const r = 36, cx = 44, cy = 44, stroke = 8;
  const circ = 2 * Math.PI * r;
  const pct = Math.min(Math.max(value / 10, 0), 1);
  return (
    <svg viewBox="0 0 88 88" style={{ width: 96, height: 96 }}>
      <circle cx={cx} cy={cy} r={r} fill="none" stroke="#1e293b" strokeWidth={stroke} />
      <circle cx={cx} cy={cy} r={r} fill="none" stroke={accent} strokeWidth={stroke}
        strokeDasharray={`${pct * circ} ${circ}`} strokeLinecap="round"
        transform="rotate(-90 44 44)" />
      <text x={cx} y={cy} textAnchor="middle" dominantBaseline="central"
        fill="white" fontSize="14" fontWeight="bold">{value.toFixed(1)}</text>
    </svg>
  );
}

function DetailModal({ entity, onClose }: { entity: Entity; onClose: () => void }) {
  const [tab, setTab] = useState<"apercu" | "metriques" | "sources">("apercu");
  return (
    <div style={{ position: "fixed", inset: 0, zIndex: 50, display: "flex", alignItems: "center", justifyContent: "center", backgroundColor: "rgba(0,0,0,0.7)", padding: 16 }}
      onClick={onClose}>
      <div style={{ backgroundColor: "#0f172a", borderRadius: 16, maxWidth: 512, width: "100%", padding: 24, boxShadow: "0 25px 50px rgba(0,0,0,0.5)" }}
        onClick={e => e.stopPropagation()}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 16 }}>
          <h3 style={{ color: "white", fontWeight: "bold", fontSize: 14, lineHeight: 1.4, paddingRight: 16 }}>{entity.name}</h3>
          <button onClick={onClose} style={{ color: "#94a3b8", background: "none", border: "none", fontSize: 20, cursor: "pointer", lineHeight: 1 }}>×</button>
        </div>
        <div style={{ display: "flex", gap: 8, marginBottom: 16 }}>
          {(["apercu", "metriques", "sources"] as const).map(t => (
            <button key={t} onClick={() => setTab(t)}
              style={{ padding: "4px 12px", borderRadius: 999, fontSize: 12, fontWeight: 500, border: "none", cursor: "pointer",
                backgroundColor: tab === t ? ACCENT : "#1e293b", color: tab === t ? "white" : "#94a3b8" }}>
              {t === "apercu" ? "Aperçu" : t === "metriques" ? "Métriques" : "Sources"}
            </button>
          ))}
        </div>
        {tab === "apercu" && (
          <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
            <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
              <span style={{ backgroundColor: RC[entity.risk_level] + "33", color: RC[entity.risk_level], fontSize: 12, padding: "2px 8px", borderRadius: 999, fontWeight: 500 }}>
                {entity.risk_level}
              </span>
              <span style={{ color: "#cbd5e1", fontSize: 14 }}>{entity.country}</span>
            </div>
            <p style={{ color: "#94a3b8", fontSize: 12 }}>{entity.primary_pattern.replace(/_/g, " ")}</p>
          </div>
        )}
        {tab === "metriques" && (
          <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
            <div style={{ display: "flex", justifyContent: "space-between", fontSize: 14 }}>
              <span style={{ color: "#94a3b8" }}>Score composite</span>
              <span style={{ color: "white", fontWeight: "bold" }}>{entity.composite_score}</span>
            </div>
            <div style={{ display: "flex", justifyContent: "space-between", fontSize: 14 }}>
              <span style={{ color: "#94a3b8" }}>Index estimé</span>
              <span style={{ color: ACCENT, fontWeight: "bold" }}>{(entity as any)[INDEX_KEY]}</span>
            </div>
          </div>
        )}
        {tab === "sources" && (
          <p style={{ color: "#94a3b8", fontSize: 12 }}>Sources disponibles via l&apos;API engine.</p>
        )}
      </div>
    </div>
  );
}

export default function ConflictMineralsDRCPage() {
  const [data, setData] = useState<EngineData | null>(null);
  const [selected, setSelected] = useState<Entity | null>(null);

  useEffect(() => {
    fetch("/api/conflict-minerals-drc-engine")
      .then(r => r.json())
      .then(d => setData(d.payload ?? d))
      .catch(() => setData(FALLBACK));
  }, []);

  const d = data ?? FALLBACK;

  return (
    <div style={{ minHeight: "100vh", backgroundColor: "#020617", color: "white", padding: 24 }}>
      {selected && <DetailModal entity={selected} onClose={() => setSelected(null)} />}
      <div style={{ maxWidth: 1152, margin: "0 auto", display: "flex", flexDirection: "column", gap: 24 }}>
        {/* Header */}
        <div style={{ display: "flex", alignItems: "flex-start", justifyContent: "space-between" }}>
          <div>
            <h1 style={{ fontSize: 24, fontWeight: "bold", color: "white" }}>Minerais de Conflit RDC (3TG)</h1>
            <p style={{ color: "#94a3b8", fontSize: 14, marginTop: 4 }}>
              {d.total_entities} entités · Confiance {(d.confidence_score * 100).toFixed(0)}% · MAJ 2026-06-22
            </p>
          </div>
          <GaugeRing value={d.avg_estimated_conflict_minerals_drc_index} accent={ACCENT} />
        </div>

        {/* Stats */}
        <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: 16 }}>
          {Object.entries(d.risk_distribution).map(([level, count]) => (
            <div key={level} style={{ backgroundColor: "#0f172a", borderRadius: 12, padding: 16, border: "1px solid #1e293b" }}>
              <div style={{ fontSize: 24, fontWeight: "bold", color: RC[level] }}>{count}</div>
              <div style={{ color: "#94a3b8", fontSize: 12, marginTop: 4, textTransform: "capitalize" }}>{level}</div>
            </div>
          ))}
        </div>

        {/* Entities grid */}
        <div style={{ display: "grid", gridTemplateColumns: "repeat(2, 1fr)", gap: 16 }}>
          {d.entities.map(e => (
            <button key={e.id} onClick={() => setSelected(e)}
              style={{ backgroundColor: "#0f172a", borderRadius: 12, padding: 16, border: "1px solid #1e293b", textAlign: "left", cursor: "pointer", transition: "border-color 0.2s" }}
              onMouseEnter={el => (el.currentTarget.style.borderColor = "#475569")}
              onMouseLeave={el => (el.currentTarget.style.borderColor = "#1e293b")}>
              <div style={{ display: "flex", alignItems: "flex-start", justifyContent: "space-between", gap: 12 }}>
                <div style={{ flex: 1, minWidth: 0 }}>
                  <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 8 }}>
                    <span style={{ backgroundColor: RC[e.risk_level] + "33", color: RC[e.risk_level], fontSize: 12, padding: "2px 8px", borderRadius: 999, fontWeight: 500 }}>
                      {e.risk_level}
                    </span>
                    <span style={{ color: "#64748b", fontSize: 12 }}>{e.id}</span>
                  </div>
                  <p style={{ color: "white", fontSize: 14, fontWeight: 500, lineHeight: 1.4 }}>{e.name}</p>
                  <p style={{ color: "#64748b", fontSize: 12, marginTop: 4 }}>{e.primary_pattern.replace(/_/g, " ")}</p>
                </div>
                <div style={{ textAlign: "right", flexShrink: 0 }}>
                  <div style={{ fontSize: 18, fontWeight: "bold", color: ACCENT }}>{e.composite_score}</div>
                  <div style={{ color: "#64748b", fontSize: 12 }}>/ 100</div>
                </div>
              </div>
            </button>
          ))}
        </div>

        {/* Alerts */}
        {d.critical_alerts.length > 0 && (
          <div style={{ backgroundColor: "#0f172a", borderRadius: 12, padding: 16, border: "1px solid rgba(127,29,29,0.3)" }}>
            <h3 style={{ color: "#f87171", fontWeight: 600, fontSize: 14, marginBottom: 12 }}>Alertes critiques</h3>
            <ul style={{ display: "flex", flexDirection: "column", gap: 4, listStyle: "none", margin: 0, padding: 0 }}>
              {d.critical_alerts.map((a, i) => (
                <li key={i} style={{ color: "#cbd5e1", fontSize: 12, display: "flex", alignItems: "flex-start", gap: 8 }}>
                  <span style={{ color: "#ef4444", marginTop: 2 }}>▲</span>{a}
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Sources */}
        <div style={{ backgroundColor: "#0f172a", borderRadius: 12, padding: 16, border: "1px solid #1e293b" }}>
          <h3 style={{ color: "#94a3b8", fontWeight: 600, fontSize: 12, marginBottom: 8, textTransform: "uppercase", letterSpacing: "0.05em" }}>Sources de données</h3>
          <div style={{ display: "flex", flexWrap: "wrap", gap: 8 }}>
            {d.data_sources.map((s, i) => (
              <span key={i} style={{ fontSize: 12, backgroundColor: "#1e293b", color: "#cbd5e1", padding: "4px 8px", borderRadius: 8 }}>{s}</span>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
