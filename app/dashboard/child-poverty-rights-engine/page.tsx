"use client";
import { useEffect, useState } from "react";

interface Entity {
  id: string;
  name: string;
  country: string;
  composite_score: number;
  risk_level: string;
  primary_pattern: string;
  estimated_child_poverty_rights_index: number;
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
  confidence_score: 0.89,
  total_entities: 8,
  critical_alerts: [
    "Somalia: malnutrition_stunting",
    "CAR Centrafrique: education_deprivation",
    "Madagascar: malnutrition_stunting",
    "Nigeria Northern: education_deprivation",
  ],
  data_sources: [
    "unicef_state_worlds_children_2024",
    "world_bank_child_poverty_2024",
    "save_children_global_index_2024",
    "fao_food_security_report_2024",
  ],
  entities: [
    { id: "CPR-001", name: "Somalia — 1.8M Enfants Risque Famine Aiguë", country: "Somalie", composite_score: 87.15, risk_level: "critique", primary_pattern: "malnutrition_stunting", estimated_child_poverty_rights_index: 8.72 },
    { id: "CPR-002", name: "CAR Centrafrique — 73% Enfants Pauvreté Extrême", country: "Centrafrique", composite_score: 84.15, risk_level: "critique", primary_pattern: "education_deprivation", estimated_child_poverty_rights_index: 8.42 },
    { id: "CPR-003", name: "Madagascar — 77% Enfants Pauvreté, Retard Croissance 49%", country: "Madagascar", composite_score: 81.15, risk_level: "critique", primary_pattern: "malnutrition_stunting", estimated_child_poverty_rights_index: 8.12 },
    { id: "CPR-004", name: "Nigeria Northern States — 10.5M Enfants Non-Scolarisés", country: "Nigeria", composite_score: 78.15, risk_level: "critique", primary_pattern: "education_deprivation", estimated_child_poverty_rights_index: 7.82 },
    { id: "CPR-005", name: "India Bihar/UP — Travail Enfants Mines Mica/Briques", country: "Inde", composite_score: 57.15, risk_level: "élevé", primary_pattern: "child_labor_exploitation", estimated_child_poverty_rights_index: 5.72 },
    { id: "CPR-006", name: "Brazil Favelas — 40% Enfants Pauvreté, Recrutement Gangs", country: "Brésil", composite_score: 54.15, risk_level: "élevé", primary_pattern: "social_protection_absence", estimated_child_poverty_rights_index: 5.42 },
    { id: "CPR-007", name: "USA Child Poverty — 12M Enfants, Food Stamps Lacunes", country: "États-Unis", composite_score: 32.15, risk_level: "modéré", primary_pattern: "social_protection_absence", estimated_child_poverty_rights_index: 3.22 },
    { id: "CPR-008", name: "Nordic Countries — Filet Social Universel, Pauvreté <3%", country: "Pays Nordiques", composite_score: 14.15, risk_level: "faible", primary_pattern: "malnutrition_stunting", estimated_child_poverty_rights_index: 1.42 },
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
            <p><strong>Index pauvreté enfants:</strong> {entity.estimated_child_poverty_rights_index}</p>
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

export default function ChildPovertyRightsDashboard() {
  const [data, setData] = useState<DashboardData>(FALLBACK);
  const [selected, setSelected] = useState<Entity | null>(null);

  useEffect(() => {
    fetch("/api/child-poverty-rights-engine")
      .then(r => r.json())
      .then(d => setData(d.payload ?? d))
      .catch(() => setData(FALLBACK));
  }, []);

  const accent = "#1a0f06";
  const avgColor = RISK_COLORS["élevé"];

  return (
    <div style={{ minHeight: "100vh", background: "#030712", color: "#f9fafb", fontFamily: "system-ui, sans-serif", padding: 24 }}>
      {selected && <DetailModal entity={selected} onClose={() => setSelected(null)} />}
      <div style={{ maxWidth: 1100, margin: "0 auto" }}>
        <div style={{ background: accent, borderRadius: 12, padding: "24px 32px", marginBottom: 32, borderLeft: "4px solid #f97316" }}>
          <h1 style={{ fontSize: 28, fontWeight: "bold", margin: 0 }}>Child Poverty Rights Engine</h1>
          <p style={{ color: "#9ca3af", marginTop: 8, marginBottom: 0 }}>Surveillance des violations des droits liées à la pauvreté des enfants — Wave 217</p>
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
                  <span style={{ color: "#9ca3af", fontSize: 12 }}>Idx: {e.estimated_child_poverty_rights_index}</span>
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
