"use client";
import { useEffect, useState } from "react";

const ACCENT = "#1a0505";
const INDEX_KEY = "estimated_corporate_impunity_rights_index";

const SEVERITY_COLORS: Record<string, string> = {
  critique: "#ef4444",
  élevé: "#f97316",
  modéré: "#eab308",
  faible: "#22c55e",
};

const FALLBACK_ENTITIES = [
  { id: "CIR-001", name: "Shell Nigeria", severity: "critique", score: 90 },
  { id: "CIR-002", name: "Chevron Ecuador", severity: "critique", score: 86 },
  { id: "CIR-003", name: "Rio Tinto Papua", severity: "critique", score: 83 },
  { id: "CIR-004", name: "Vale Brumadinho", severity: "critique", score: 79 },
  { id: "CIR-005", name: "Glencore", severity: "élevé", score: 57 },
  { id: "CIR-006", name: "Volkswagen", severity: "élevé", score: 54 },
  { id: "CIR-007", name: "BP", severity: "modéré", score: 31 },
  { id: "CIR-008", name: "Patagonia", severity: "faible", score: 8 },
];

const FALLBACK_DATA_SOURCES = [
  "business_human_rights_resource_centre",
  "global_witness_corporate",
  "amnesty_oil_niger_delta",
  "csddd_eu_2024_1760",
];

const FALLBACK_CRITICAL_ALERTS = [
  "Shell Nigeria: pollution_delta_niger_50_ans_impunie",
  "Chevron: contamination_amazonie_equateur_30000_habitants",
];

function GaugeRing({ score, color }: { score: number; color: string }) {
  const r = 36;
  const cx = 44;
  const cy = 44;
  const strokeWidth = 8;
  const circumference = 2 * Math.PI * r;
  const offset = circumference - (score / 100) * circumference;
  return (
    <svg viewBox="0 0 88 88" width={88} height={88}>
      <circle cx={cx} cy={cy} r={r} fill="none" stroke="#1e293b" strokeWidth={strokeWidth} />
      <circle
        cx={cx}
        cy={cy}
        r={r}
        fill="none"
        stroke={color}
        strokeWidth={strokeWidth}
        strokeDasharray={circumference}
        strokeDashoffset={offset}
        strokeLinecap="round"
        transform={`rotate(-90 ${cx} ${cy})`}
      />
      <text x={cx} y={cy + 5} textAnchor="middle" fill="#f1f5f9" fontSize={14} fontWeight="bold">
        {score}
      </text>
    </svg>
  );
}

export default function CorporateImpunityRightsDashboard() {
  const [entities, setEntities] = useState(FALLBACK_ENTITIES);
  const [index, setIndex] = useState<number | null>(null);
  const [dataSources, setDataSources] = useState(FALLBACK_DATA_SOURCES);
  const [criticalAlerts, setCriticalAlerts] = useState(FALLBACK_CRITICAL_ALERTS);

  useEffect(() => {
    fetch("/api/corporate-impunity-rights-engine")
      .then((r) => r.json())
      .then((d) => {
        const payload = d.payload ?? d;
        if (payload.entities) setEntities(payload.entities);
        if (payload[INDEX_KEY] !== undefined) setIndex(payload[INDEX_KEY]);
        if (payload.data_sources) setDataSources(payload.data_sources);
        if (payload.critical_alerts) setCriticalAlerts(payload.critical_alerts);
      })
      .catch(() => {});
  }, []);

  const critiques = entities.filter((e) => e.severity === "critique");

  return (
    <div style={{ minHeight: "100vh", background: "#0f172a", color: "#f1f5f9", fontFamily: "system-ui, sans-serif", padding: "2rem" }}>
      <div style={{ maxWidth: 1100, margin: "0 auto" }}>
        {/* Header */}
        <div style={{ marginBottom: "2rem", borderLeft: `4px solid ${ACCENT}`, paddingLeft: "1rem" }}>
          <h1 style={{ fontSize: "1.75rem", fontWeight: 700, margin: 0 }}>Impunité Corporative — Responsabilité Entreprises</h1>
          <p style={{ color: "#94a3b8", marginTop: "0.5rem" }}>Wave 213 · Indice des violations responsabilité corporative</p>
          {index !== null && (
            <p style={{ color: "#22c55e", fontWeight: 600, marginTop: "0.25rem" }}>
              Index estimé : {index} / 10
            </p>
          )}
        </div>

        {/* Critical alerts */}
        {criticalAlerts.length > 0 && (
          <div style={{ background: "#1e0a0a", border: "1px solid #ef4444", borderRadius: 8, padding: "1rem", marginBottom: "2rem" }}>
            <p style={{ color: "#ef4444", fontWeight: 700, marginBottom: "0.5rem" }}>Alertes critiques</p>
            {criticalAlerts.map((alert, i) => (
              <p key={i} style={{ color: "#fca5a5", margin: "0.25rem 0", fontSize: "0.875rem" }}>⚠ {alert}</p>
            ))}
          </div>
        )}

        {/* Entities grid */}
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(240px, 1fr))", gap: "1rem", marginBottom: "2rem" }}>
          {entities.map((entity) => {
            const color = SEVERITY_COLORS[entity.severity] ?? "#94a3b8";
            return (
              <div
                key={entity.id}
                style={{ background: "#1e293b", borderRadius: 10, padding: "1.25rem", border: `1px solid ${color}33`, display: "flex", flexDirection: "column", alignItems: "center", gap: "0.75rem" }}
              >
                <GaugeRing score={entity.score} color={color} />
                <div style={{ textAlign: "center" }}>
                  <p style={{ fontWeight: 600, margin: 0 }}>{entity.name}</p>
                  <p style={{ fontSize: "0.75rem", color: "#64748b", margin: "0.25rem 0 0" }}>{entity.id}</p>
                  <span style={{ fontSize: "0.75rem", background: color + "22", color, padding: "0.2rem 0.6rem", borderRadius: 20, display: "inline-block", marginTop: "0.4rem" }}>
                    {entity.severity}
                  </span>
                </div>
              </div>
            );
          })}
        </div>

        {/* Critique summary */}
        <div style={{ background: "#1e293b", borderRadius: 10, padding: "1.25rem", marginBottom: "1.5rem" }}>
          <p style={{ fontWeight: 700, marginBottom: "0.75rem" }}>Entités critiques ({critiques.length})</p>
          {critiques.map((e) => (
            <div key={e.id} style={{ display: "flex", justifyContent: "space-between", padding: "0.4rem 0", borderBottom: "1px solid #0f172a" }}>
              <span style={{ color: "#f1f5f9" }}>{e.name}</span>
              <span style={{ color: "#ef4444", fontWeight: 600 }}>{e.score}/100</span>
            </div>
          ))}
        </div>

        {/* Data sources */}
        <div style={{ background: "#1e293b", borderRadius: 10, padding: "1.25rem" }}>
          <p style={{ fontWeight: 700, marginBottom: "0.5rem" }}>Sources de données</p>
          <div style={{ display: "flex", flexWrap: "wrap", gap: "0.5rem" }}>
            {dataSources.map((src, i) => (
              <span key={i} style={{ fontSize: "0.75rem", background: "#0f172a", color: "#94a3b8", padding: "0.25rem 0.75rem", borderRadius: 20 }}>
                {src}
              </span>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
