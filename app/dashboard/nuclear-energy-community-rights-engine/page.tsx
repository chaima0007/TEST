"use client";
import { useEffect, useState } from "react";

interface Entity {
  id: string;
  name: string;
  country: string;
  composite_score: number;
  risk_level: string;
  primary_pattern: string;
  estimated_nuclear_energy_community_rights_index: number;
}
interface EngineData {
  agent: string;
  total_entities: number;
  avg_composite: number;
  confidence_score: number;
  avg_estimated_nuclear_energy_community_rights_index: number;
  risk_distribution: Record<string, number>;
  critical_alerts: string[];
  data_sources: string[];
  entities: Entity[];
}

const ACCENT = "#14532d";
const RC: Record<string, string> = {
  critique: "#ef4444",
  "élevé": "#f97316",
  "modéré": "#eab308",
  faible: "#22c55e",
};
const INDEX_KEY = "estimated_nuclear_energy_community_rights_index";

const FALLBACK_ENTITIES: Entity[] = [
  { id: "NEC-001", name: "EDF France", country: "France", composite_score: 87.75, risk_level: "critique", primary_pattern: "impacts_communautaires_centrales_nucleaires", estimated_nuclear_energy_community_rights_index: 8.775 },
  { id: "NEC-002", name: "Tepco", country: "Japon", composite_score: 89.30, risk_level: "critique", primary_pattern: "fukushima_droits_evacuations_forcees", estimated_nuclear_energy_community_rights_index: 8.93 },
  { id: "NEC-003", name: "Rosatom", country: "Russie", composite_score: 83.55, risk_level: "critique", primary_pattern: "droits_communautes_sites_nucleaires_exportes", estimated_nuclear_energy_community_rights_index: 8.355 },
  { id: "NEC-004", name: "EDF Cattenom", country: "France", composite_score: 81.75, risk_level: "critique", primary_pattern: "risques_nucleaires_populations_frontalières", estimated_nuclear_energy_community_rights_index: 8.175 },
  { id: "NEC-005", name: "Exelon", country: "États-Unis", composite_score: 54.05, risk_level: "élevé", primary_pattern: "consultation_insuffisante_communautes_locales", estimated_nuclear_energy_community_rights_index: 5.405 },
  { id: "NEC-006", name: "EDF Energy UK", country: "Royaume-Uni", composite_score: 50.05, risk_level: "élevé", primary_pattern: "transparence_lacunaire_gestion_dechets_nucleaires", estimated_nuclear_energy_community_rights_index: 5.005 },
  { id: "NEC-007", name: "Vattenfall", country: "Suède", composite_score: 27.75, risk_level: "modéré", primary_pattern: "engagement_partiel_parties_prenantes_nucleaire", estimated_nuclear_energy_community_rights_index: 2.775 },
  { id: "NEC-008", name: "NFLA", country: "International", composite_score: 11.95, risk_level: "faible", primary_pattern: "plaidoyer_droits_communautes_anti_nucleaires", estimated_nuclear_energy_community_rights_index: 1.195 },
];

const FALLBACK: EngineData = {
  agent: "Nucléaire & Droits Communautés",
  total_entities: 8,
  avg_composite: 60.77,
  confidence_score: 0.88,
  avg_estimated_nuclear_energy_community_rights_index: 6.077,
  risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
  critical_alerts: [
    "Tepco: fukushima_droits_evacuations_forcees",
    "EDF France: impacts_communautaires_centrales_nucleaires",
    "Rosatom: droits_communautes_sites_nucleaires_exportes",
    "EDF Cattenom: risques_nucleaires_populations_frontalières",
  ],
  data_sources: ["iaea_nuclear_safety_community_reports", "greenpeace_nuclear_rights_tracker", "who_radiation_health_impacts", "nfla_community_rights_database"],
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

export default function NuclearEnergyCommunityRightsPage() {
  const [data, setData] = useState<EngineData | null>(null);
  const [selected, setSelected] = useState<Entity | null>(null);

  useEffect(() => {
    fetch("/api/nuclear-energy-community-rights-engine")
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
            <h1 style={{ fontSize: 24, fontWeight: "bold", color: "white" }}>Nucléaire &amp; Droits Communautés</h1>
            <p style={{ color: "#94a3b8", fontSize: 14, marginTop: 4 }}>
              {d.total_entities} entités · Confiance {(d.confidence_score * 100).toFixed(0)}% · MAJ 2026-06-22
            </p>
          </div>
          <GaugeRing value={d.avg_estimated_nuclear_energy_community_rights_index} accent={ACCENT} />
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
