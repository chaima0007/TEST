"use client";
import { useEffect, useState } from "react";

interface Entity {
  id: string;
  name: string;
  country: string;
  composite_score: number;
  risk_level: string;
  primary_pattern: string;
  estimated_environmental_racism_rights_index: number;
}

interface DashboardData {
  avg_composite: number;
  confidence_score: number;
  total_entities: number;
  critical_alerts: string[];
  data_sources: string[];
  entities: Entity[];
}

const FALLBACK: DashboardData = {
  avg_composite: 61.03,
  confidence_score: 0.87,
  total_entities: 8,
  critical_alerts: [
    "Nigeria Delta Niger: toxic_exposure",
    "Flint Michigan: environmental_justice_denial",
    "DRC Congo: regulatory_capture",
    "Bangladesh Tanneries: toxic_exposure",
  ],
  data_sources: [
    "unep_environmental_racism_report_2024",
    "hrw_pollution_human_rights_2024",
    "amnesty_oil_pollution_niger_delta",
    "who_chemical_exposure_communities",
  ],
  entities: [
    { id: "ERR-001", name: "Nigeria Delta Niger — Shell/TotalEnergies 50 Ans Pollution Pétrolière", country: "Nigeria", composite_score: 87.15, risk_level: "critique", primary_pattern: "toxic_exposure", estimated_environmental_racism_rights_index: 8.72 },
    { id: "ERR-002", name: "Flint Michigan USA — Crise Eau Plombée Communauté Noire", country: "États-Unis", composite_score: 84.15, risk_level: "critique", primary_pattern: "environmental_justice_denial", estimated_environmental_racism_rights_index: 8.42 },
    { id: "ERR-003", name: "DRC Congo Cobalt Mining — Enfants Exposés Métaux Lourds", country: "DRC", composite_score: 81.15, risk_level: "critique", primary_pattern: "regulatory_capture", estimated_environmental_racism_rights_index: 8.12 },
    { id: "ERR-004", name: "Bangladesh Tanneries Hazaribagh — Ouvriers Exposés Chrome/Arsenic", country: "Bangladesh", composite_score: 78.15, risk_level: "critique", primary_pattern: "toxic_exposure", estimated_environmental_racism_rights_index: 7.82 },
    { id: "ERR-005", name: "Brazil Amazonie — Orpaillage Mercure Yanomami", country: "Brésil", composite_score: 57.15, risk_level: "élevé", primary_pattern: "community_displacement", estimated_environmental_racism_rights_index: 5.72 },
    { id: "ERR-006", name: "India Bhopal Legacy — Contamination Persistante UCC", country: "Inde", composite_score: 54.15, risk_level: "élevé", primary_pattern: "environmental_justice_denial", estimated_environmental_racism_rights_index: 5.42 },
    { id: "ERR-007", name: "EU Environmental Justice — REACH Partielles, Exceptions Industrielles", country: "Union Européenne", composite_score: 32.15, risk_level: "modéré", primary_pattern: "regulatory_capture", estimated_environmental_racism_rights_index: 3.22 },
    { id: "ERR-008", name: "Costa Rica/Ecuador Green Rights — Droits Nature Constitutionnels", country: "Costa Rica/Équateur", composite_score: 14.15, risk_level: "faible", primary_pattern: "environmental_justice_denial", estimated_environmental_racism_rights_index: 1.42 },
  ],
};

const RISK_COLORS: Record<string, string> = {
  critique: "#ef4444",
  "élevé": "#f97316",
  "modéré": "#eab308",
  faible: "#22c55e",
};

function GaugeRing({ score, color }: { score: number; color: string }) {
  const r = 36, cx = 44, cy = 44, stroke = 8;
  const circ = 2 * Math.PI * r;
  const offset = circ - (score / 100) * circ;
  return (
    <svg viewBox="0 0 88 88" style={{ width: 96, height: 96 }}>
      <circle cx={cx} cy={cy} r={r} fill="none" stroke="#1f2937" strokeWidth={stroke} />
      <circle cx={cx} cy={cy} r={r} fill="none" stroke={color} strokeWidth={stroke}
        strokeDasharray={circ} strokeDashoffset={offset} strokeLinecap="round"
        transform={`rotate(-90 ${cx} ${cy})`} />
      <text x={cx} y={cy + 5} textAnchor="middle" fill="#f9fafb" fontSize="14" fontWeight="bold">{score.toFixed(0)}</text>
    </svg>
  );
}

function DetailModal({ entity, onClose }: { entity: Entity; onClose: () => void }) {
  const [tab, setTab] = useState<"apercu" | "metriques" | "sources">("apercu");
  const color = RISK_COLORS[entity.risk_level] ?? "#6b7280";
  return (
    <div style={{ position: "fixed", inset: 0, background: "rgba(0,0,0,0.7)", zIndex: 50, display: "flex", alignItems: "center", justifyContent: "center" }}>
      <div style={{ background: "#111827", border: "1px solid #374151", borderRadius: 12, width: "90%", maxWidth: 600, padding: 24 }}>
        <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 16 }}>
          <span style={{ color: "#f9fafb", fontWeight: "bold", fontSize: 16 }}>{entity.id}</span>
          <button onClick={onClose} style={{ background: "none", border: "none", color: "#9ca3af", cursor: "pointer", fontSize: 20 }}>×</button>
        </div>
        <p style={{ color: "#e5e7eb", marginBottom: 16 }}>{entity.name}</p>
        <div style={{ display: "flex", gap: 8, marginBottom: 20 }}>
          {(["apercu", "metriques", "sources"] as const).map(t => (
            <button key={t} onClick={() => setTab(t)} style={{ padding: "6px 14px", borderRadius: 6, border: "none", cursor: "pointer", background: tab === t ? color : "#1f2937", color: tab === t ? "#fff" : "#9ca3af", fontWeight: tab === t ? "bold" : "normal" }}>{t}</button>
          ))}
        </div>
        {tab === "apercu" && (
          <div style={{ color: "#d1d5db" }}>
            <p><strong>Pays:</strong> {entity.country}</p>
            <p><strong>Niveau de risque:</strong> <span style={{ color }}>{entity.risk_level}</span></p>
            <p><strong>Pattern principal:</strong> {entity.primary_pattern}</p>
          </div>
        )}
        {tab === "metriques" && (
          <div style={{ color: "#d1d5db" }}>
            <p><strong>Score composite:</strong> {entity.composite_score}</p>
            <p><strong>Index racisme environnemental:</strong> {entity.estimated_environmental_racism_rights_index}</p>
          </div>
        )}
        {tab === "sources" && (
          <div style={{ color: "#d1d5db" }}>
            <p>Sources disponibles via l&apos;API upstream.</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default function EnvironmentalRacismRightsDashboard() {
  const [data, setData] = useState<DashboardData>(FALLBACK);
  const [selected, setSelected] = useState<Entity | null>(null);

  useEffect(() => {
    fetch("/api/environmental-racism-rights-engine")
      .then(r => r.json())
      .then(d => setData(d.payload ?? d))
      .catch(() => setData(FALLBACK));
  }, []);

  const accent = "#0a150a";
  const avgColor = RISK_COLORS["élevé"];

  return (
    <div style={{ minHeight: "100vh", background: "#030712", color: "#f9fafb", fontFamily: "system-ui, sans-serif", padding: 24 }}>
      {selected && <DetailModal entity={selected} onClose={() => setSelected(null)} />}
      <div style={{ maxWidth: 1100, margin: "0 auto" }}>
        <div style={{ background: accent, borderRadius: 12, padding: "24px 32px", marginBottom: 32, borderLeft: "4px solid #22c55e" }}>
          <h1 style={{ fontSize: 28, fontWeight: "bold", margin: 0 }}>Environmental Racism Rights Engine</h1>
          <p style={{ color: "#9ca3af", marginTop: 8, marginBottom: 0 }}>Surveillance des violations des droits liées au racisme environnemental — Wave 217</p>
        </div>

        <div style={{ display: "grid", gridTemplateColumns: "repeat(3,1fr)", gap: 16, marginBottom: 32 }}>
          <div style={{ background: "#111827", borderRadius: 10, padding: 20, textAlign: "center" }}>
            <GaugeRing score={data.avg_composite} color={avgColor} />
            <p style={{ color: "#9ca3af", marginTop: 8, fontSize: 13 }}>Score Composite Moyen</p>
          </div>
          <div style={{ background: "#111827", borderRadius: 10, padding: 20, display: "flex", flexDirection: "column", justifyContent: "center" }}>
            <p style={{ color: "#9ca3af", fontSize: 13, margin: 0 }}>Entités surveillées</p>
            <p style={{ fontSize: 36, fontWeight: "bold", margin: "4px 0", color: "#f9fafb" }}>{data.total_entities}</p>
            <p style={{ color: "#9ca3af", fontSize: 13, margin: 0 }}>Confiance: {(data.confidence_score * 100).toFixed(0)}%</p>
          </div>
          <div style={{ background: "#111827", borderRadius: 10, padding: 20 }}>
            <p style={{ color: "#ef4444", fontSize: 13, fontWeight: "bold", margin: "0 0 8px" }}>Alertes Critiques</p>
            {data.critical_alerts.map((a, i) => (
              <p key={i} style={{ color: "#fca5a5", fontSize: 12, margin: "2px 0" }}>• {a}</p>
            ))}
          </div>
        </div>

        <div style={{ display: "grid", gridTemplateColumns: "repeat(2,1fr)", gap: 16 }}>
          {data.entities.map(e => {
            const color = RISK_COLORS[e.risk_level] ?? "#6b7280";
            return (
              <div key={e.id} onClick={() => setSelected(e)} style={{ background: "#111827", borderRadius: 10, padding: 20, cursor: "pointer", border: "1px solid #1f2937", transition: "border-color 0.2s" }}>
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 12 }}>
                  <div style={{ flex: 1 }}>
                    <span style={{ color: "#6b7280", fontSize: 11 }}>{e.id}</span>
                    <p style={{ color: "#f9fafb", fontWeight: "bold", margin: "4px 0", fontSize: 14 }}>{e.name}</p>
                    <p style={{ color: "#9ca3af", fontSize: 12, margin: 0 }}>{e.country}</p>
                  </div>
                  <GaugeRing score={e.composite_score} color={color} />
                </div>
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                  <span style={{ background: color + "22", color, padding: "2px 10px", borderRadius: 20, fontSize: 12 }}>{e.risk_level}</span>
                  <span style={{ color: "#6b7280", fontSize: 11 }}>{e.primary_pattern}</span>
                  <span style={{ color: "#9ca3af", fontSize: 12 }}>Idx: {e.estimated_environmental_racism_rights_index}</span>
                </div>
              </div>
            );
          })}
        </div>

        <div style={{ marginTop: 24, background: "#111827", borderRadius: 10, padding: 20 }}>
          <p style={{ color: "#9ca3af", fontSize: 12, margin: "0 0 8px" }}>Sources de données:</p>
          <div style={{ display: "flex", flexWrap: "wrap", gap: 8 }}>
            {data.data_sources.map((s, i) => (
              <span key={i} style={{ background: "#1f2937", color: "#9ca3af", padding: "4px 10px", borderRadius: 6, fontSize: 11 }}>{s}</span>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
