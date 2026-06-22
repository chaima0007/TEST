"use client";
import { useState, useEffect } from "react";

const ACCENT = "#1f2d0a";
const INDEX_KEY = "estimated_indigenous_land_rights_index";

const RISK_COLORS: Record<string, string> = {
  critique: "#ef4444",
  "élevé": "#f97316",
  modéré: "#eab308",
  faible: "#22c55e",
};

const RISK_CONFIG: Record<string, { label: string; color: string; bg: string; border: string }> = {
  critique: { label: "Critique", color: "#ef4444", bg: "rgba(239,68,68,0.10)", border: "rgba(239,68,68,0.25)" },
  "élevé": { label: "Élevé", color: "#f97316", bg: "rgba(249,115,22,0.10)", border: "rgba(249,115,22,0.25)" },
  modéré: { label: "Modéré", color: "#eab308", bg: "rgba(234,179,8,0.10)", border: "rgba(234,179,8,0.25)" },
  faible: { label: "Faible", color: "#22c55e", bg: "rgba(34,197,94,0.10)", border: "rgba(34,197,94,0.25)" },
};

const FALLBACK_ENTITIES = [
  { id: "ILR-001", name: "Brazil/Amazonie", country: "Amérique du Sud", sector: "1 000+ terres autochtones menacées, garimpos illégaux & défenseurs assassinés", composite_score: 93, risk_level: "critique", estimated_indigenous_land_rights_index: 9.3 },
  { id: "ILR-002", name: "Canada/Premières Nations", country: "Amérique du Nord", sector: "Traités non-respectés, Pipeline Trans Mountain & RCAANC — consultation factice", composite_score: 88, risk_level: "critique", estimated_indigenous_land_rights_index: 8.8 },
  { id: "ILR-003", name: "Papouasie/Indonésie", country: "Asie du Sud-Est", sector: "Déforestation forêts papouanes, transmigration & mines Freeport", composite_score: 88, risk_level: "critique", estimated_indigenous_land_rights_index: 8.8 },
  { id: "ILR-004", name: "Philippines/Lumad", country: "Asie du Sud-Est", sector: "IPRA non-appliqué, mines Mindanao & déplacements forcés 3 000+", composite_score: 83, risk_level: "critique", estimated_indigenous_land_rights_index: 8.3 },
  { id: "ILR-005", name: "Kenya/Maasaï", country: "Afrique de l&apos;Est", sector: "Ngorongoro expulsions 2022 sans CLPE — terres cédées au tourisme safari", composite_score: 54, risk_level: "élevé", estimated_indigenous_land_rights_index: 5.4 },
  { id: "ILR-006", name: "Australia", country: "Océanie", sector: "Fracking Northern Territory, sites sacrés détruits & Land Rights Act contourné", composite_score: 53, risk_level: "élevé", estimated_indigenous_land_rights_index: 5.3 },
  { id: "ILR-007", name: "Bolivia", country: "Amérique du Sud", sector: "TIPNIS menacé, extraction hydrocarbures terres autochtones & tensions légales", composite_score: 28, risk_level: "modéré", estimated_indigenous_land_rights_index: 2.8 },
  { id: "ILR-008", name: "New Zealand/Maori", country: "Océanie", sector: "Waitangi partiellement respecté — He Puapua & co-gouvernance en progrès", composite_score: 4, risk_level: "faible", estimated_indigenous_land_rights_index: 0.4 },
];

const FALLBACK_DATA = {
  total_entities: 8,
  avg_composite: 61.32,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  avg_estimated_indigenous_land_rights_index: 6.13,
  confidence_score: 0.83,
  last_analysis: "2026-06-22",
  data_sources: ["forest_peoples_programme", "cultural_survival", "undrip_monitoring", "oxfam_land_rights"],
  critical_alerts: ["Brazil: déforestation_accélérée_amazonie", "Canada: MMIWG_Non_Résolues", "Papouasie: extraction_minière_forcée"],
  entities: FALLBACK_ENTITIES,
};

interface Entity {
  id: string;
  name: string;
  country: string;
  sector: string;
  composite_score: number;
  risk_level: string;
  [key: string]: unknown;
}

interface DashData {
  total_entities: number;
  avg_composite: number;
  risk_distribution: Record<string, number>;
  avg_estimated_indigenous_land_rights_index?: number;
  confidence_score?: number;
  last_analysis?: string;
  data_sources?: string[];
  critical_alerts?: string[];
  entities: Entity[];
  [key: string]: unknown;
}

function GaugeRing({ value, stroke }: { value: number; stroke: string }) {
  const r = 36, cx = 44, cy = 44;
  const circ = 2 * Math.PI * r;
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

function DetailModal({ entity, onClose }: { entity: Entity; onClose: () => void }) {
  const cfg = RISK_CONFIG[entity.risk_level] ?? RISK_CONFIG.faible;
  const indexVal = entity[INDEX_KEY] as number | undefined;
  return (
    <div
      style={{ position: "fixed", inset: 0, background: "rgba(0,0,0,0.72)", zIndex: 50, display: "flex", alignItems: "center", justifyContent: "center", padding: 16 }}
      onClick={onClose}
    >
      <div
        style={{ background: "#0f172a", border: "1px solid #334155", borderRadius: 16, width: "100%", maxWidth: 560, maxHeight: "85vh", overflowY: "auto" }}
        onClick={e => e.stopPropagation()}
      >
        <div style={{ padding: "24px 24px 16px", borderBottom: "1px solid #1e293b", display: "flex", justifyContent: "space-between", alignItems: "flex-start", gap: 16 }}>
          <div>
            <span style={{ fontSize: 11, fontWeight: 700, textTransform: "uppercase", color: cfg.color }}>{cfg.label}</span>
            <h2 style={{ fontSize: 17, fontWeight: 700, color: "white", margin: "4px 0 4px" }}>{entity.name}</h2>
            <p style={{ fontSize: 13, color: "#94a3b8" }}>{entity.country} &mdash; {entity.sector}</p>
          </div>
          <button onClick={onClose} style={{ background: "none", border: "none", color: "#64748b", fontSize: 22, cursor: "pointer", lineHeight: 1 }}>&#x2715;</button>
        </div>
        <div style={{ padding: "20px 24px 24px" }}>
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12, marginBottom: 16 }}>
            {[
              { label: "Score Composite", value: `${entity.composite_score}/100` },
              { label: "Index ILR", value: indexVal !== undefined ? `${indexVal}/10` : "—" },
              { label: "Niveau de risque", value: cfg.label },
              { label: "Entité", value: entity.id },
              { label: "Pays / Région", value: entity.country },
              { label: "Contexte", value: entity.sector },
            ].map(({ label, value }) => (
              <div key={label} style={{ background: "rgba(255,255,255,0.04)", borderRadius: 10, padding: "10px 14px" }}>
                <p style={{ fontSize: 11, color: "#64748b", margin: "0 0 2px" }}>{label}</p>
                <p style={{ fontSize: 14, fontWeight: 600, color: "white", margin: 0 }}>{value}</p>
              </div>
            ))}
          </div>
          <div style={{ background: "rgba(255,255,255,0.04)", borderRadius: 10, padding: "12px 16px" }}>
            <p style={{ fontSize: 12, color: "#94a3b8", margin: "0 0 6px" }}>Score Composite</p>
            <div style={{ height: 6, background: "#1e293b", borderRadius: 4, overflow: "hidden" }}>
              <div style={{ height: "100%", width: `${Math.min(100, entity.composite_score)}%`, background: cfg.color, borderRadius: 4 }} />
            </div>
            <p style={{ fontSize: 11, color: "#475569", margin: "6px 0 0" }}>
              Droits fonciers peuples autochtones &amp; CLPE
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default function Page() {
  const [data, setData] = useState<DashData | null>(null);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState("tous");
  const [selected, setSelected] = useState<Entity | null>(null);

  useEffect(() => {
    fetch("/api/indigenous-land-rights-engine")
      .then(r => r.json())
      .then(d => { setData(d.payload ?? d); setLoading(false); })
      .catch(() => { setData(FALLBACK_DATA); setLoading(false); });
  }, []);

  const dash = data ?? FALLBACK_DATA;
  const entities: Entity[] = dash.entities ?? [];
  const filtered = filter === "tous" ? entities : entities.filter(e => e.risk_level === filter);

  return (
    <div style={{ minHeight: "100vh", background: "#020817", color: "white", padding: 24 }}>
      {/* Header */}
      <div style={{ display: "flex", alignItems: "flex-start", justifyContent: "space-between", gap: 16, marginBottom: 32 }}>
        <div>
          <h1 style={{ fontSize: 22, fontWeight: 700, color: "#86efac", margin: "0 0 4px" }}>
            Droits Fonciers Peuples Autochtones
          </h1>
          <p style={{ fontSize: 13, color: "#64748b", margin: 0 }}>
            Indigenous Land Rights Engine &middot; Wave 211
          </p>
        </div>
        <span style={{ fontSize: 12, color: "#64748b", background: "rgba(255,255,255,0.05)", border: "1px solid rgba(255,255,255,0.1)", borderRadius: 8, padding: "6px 12px" }}>
          {dash.total_entities} entit&eacute;s analys&eacute;es
        </span>
      </div>

      {loading && (
        <div style={{ display: "flex", justifyContent: "center", alignItems: "center", minHeight: 200 }}>
          <div style={{ width: 32, height: 32, border: "2px solid #86efac", borderTopColor: "transparent", borderRadius: "50%", animation: "spin 0.8s linear infinite" }} />
        </div>
      )}

      {!loading && (
        <>
          {/* KPI Grid */}
          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(140px, 1fr))", gap: 12, marginBottom: 28 }}>
            <div style={{ background: "rgba(255,255,255,0.04)", border: "1px solid rgba(255,255,255,0.08)", borderRadius: 12, padding: "16px 18px" }}>
              <p style={{ fontSize: 11, color: "#64748b", textTransform: "uppercase", letterSpacing: "0.05em", margin: "0 0 6px" }}>Critiques</p>
              <p style={{ fontSize: 28, fontWeight: 700, color: "#ef4444", margin: 0 }}>{dash.risk_distribution?.critique ?? 0}</p>
            </div>
            <div style={{ background: "rgba(255,255,255,0.04)", border: "1px solid rgba(255,255,255,0.08)", borderRadius: 12, padding: "16px 18px", display: "flex", flexDirection: "column", alignItems: "center" }}>
              <p style={{ fontSize: 11, color: "#64748b", textTransform: "uppercase", letterSpacing: "0.05em", margin: "0 0 6px" }}>Score Moyen</p>
              <GaugeRing value={dash.avg_composite} stroke="#86efac" />
            </div>
            <div style={{ background: "rgba(255,255,255,0.04)", border: "1px solid rgba(255,255,255,0.08)", borderRadius: 12, padding: "16px 18px" }}>
              <p style={{ fontSize: 11, color: "#64748b", textTransform: "uppercase", letterSpacing: "0.05em", margin: "0 0 6px" }}>Index ILR Moyen</p>
              <p style={{ fontSize: 28, fontWeight: 700, color: "#86efac", margin: 0 }}>{dash.avg_estimated_indigenous_land_rights_index ?? "—"}</p>
            </div>
            <div style={{ background: "rgba(255,255,255,0.04)", border: "1px solid rgba(255,255,255,0.08)", borderRadius: 12, padding: "16px 18px" }}>
              <p style={{ fontSize: 11, color: "#64748b", textTransform: "uppercase", letterSpacing: "0.05em", margin: "0 0 6px" }}>Entit&eacute;s</p>
              <p style={{ fontSize: 28, fontWeight: 700, color: "#86efac", margin: 0 }}>{dash.total_entities}</p>
            </div>
            <div style={{ background: "rgba(255,255,255,0.04)", border: "1px solid rgba(255,255,255,0.08)", borderRadius: 12, padding: "16px 18px" }}>
              <p style={{ fontSize: 11, color: "#64748b", textTransform: "uppercase", letterSpacing: "0.05em", margin: "0 0 6px" }}>Confiance</p>
              <p style={{ fontSize: 28, fontWeight: 700, color: "#22c55e", margin: 0 }}>{Math.round((dash.confidence_score ?? 0) * 100)}%</p>
            </div>
            <div style={{ background: "rgba(255,255,255,0.04)", border: "1px solid rgba(255,255,255,0.08)", borderRadius: 12, padding: "16px 18px" }}>
              <p style={{ fontSize: 11, color: "#64748b", textTransform: "uppercase", letterSpacing: "0.05em", margin: "0 0 6px" }}>Derni&egrave;re Analyse</p>
              <p style={{ fontSize: 14, fontWeight: 700, color: "#e2e8f0", margin: 0 }}>{dash.last_analysis ?? "—"}</p>
            </div>
          </div>

          {/* Critical Alerts */}
          {(dash.critical_alerts ?? []).length > 0 && (
            <div style={{ background: "rgba(239,68,68,0.07)", border: "1px solid rgba(239,68,68,0.2)", borderRadius: 12, padding: "14px 18px", marginBottom: 24 }}>
              <p style={{ fontSize: 13, fontWeight: 600, color: "#ef4444", margin: "0 0 6px" }}>Alertes Critiques</p>
              <div style={{ display: "flex", flexWrap: "wrap", gap: 8 }}>
                {(dash.critical_alerts ?? []).map((alert: string, i: number) => (
                  <span key={i} style={{ fontSize: 12, color: "#fca5a5", background: "rgba(239,68,68,0.12)", border: "1px solid rgba(239,68,68,0.2)", borderRadius: 6, padding: "3px 10px" }}>
                    {alert}
                  </span>
                ))}
              </div>
            </div>
          )}

          {/* Data Sources */}
          {(dash.data_sources ?? []).length > 0 && (
            <div style={{ background: "rgba(134,239,172,0.05)", border: "1px solid rgba(134,239,172,0.15)", borderRadius: 12, padding: "14px 18px", marginBottom: 24 }}>
              <p style={{ fontSize: 12, color: "#94a3b8", margin: "0 0 8px", fontWeight: 600, textTransform: "uppercase", letterSpacing: "0.04em" }}>Sources de Donn&eacute;es</p>
              <div style={{ display: "flex", flexWrap: "wrap", gap: 8 }}>
                {(dash.data_sources ?? []).map((src: string, i: number) => (
                  <span key={i} style={{ fontSize: 12, color: "#86efac", background: "rgba(134,239,172,0.08)", border: "1px solid rgba(134,239,172,0.15)", borderRadius: 6, padding: "3px 10px" }}>
                    {src}
                  </span>
                ))}
              </div>
            </div>
          )}

          {/* Filter Pills */}
          <div style={{ display: "flex", gap: 8, flexWrap: "wrap", marginBottom: 20 }}>
            {["tous", "critique", "élevé", "modéré", "faible"].map(f => {
              const isActive = filter === f;
              const cfg = f !== "tous" ? RISK_CONFIG[f] : null;
              return (
                <button
                  key={f}
                  onClick={() => setFilter(f)}
                  style={{
                    padding: "6px 16px",
                    borderRadius: 999,
                    fontSize: 13,
                    fontWeight: 500,
                    cursor: "pointer",
                    border: isActive && cfg ? `1px solid ${cfg.border}` : "1px solid rgba(255,255,255,0.1)",
                    background: isActive && cfg ? cfg.bg : isActive ? "rgba(255,255,255,0.08)" : "transparent",
                    color: isActive && cfg ? cfg.color : isActive ? "white" : "#94a3b8",
                    transition: "all 0.15s",
                  }}
                >
                  {f.charAt(0).toUpperCase() + f.slice(1)}
                </button>
              );
            })}
          </div>

          {/* Entity Grid */}
          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(280px, 1fr))", gap: 16 }}>
            {filtered.map(e => {
              const cfg = RISK_CONFIG[e.risk_level] ?? RISK_CONFIG.faible;
              const indexVal = e[INDEX_KEY] as number | undefined;
              return (
                <button
                  key={e.id}
                  onClick={() => setSelected(e)}
                  style={{
                    textAlign: "left",
                    border: `1px solid ${cfg.border}`,
                    background: cfg.bg,
                    borderRadius: 14,
                    padding: 16,
                    cursor: "pointer",
                    transition: "transform 0.1s",
                    width: "100%",
                  }}
                  onMouseEnter={ev => { (ev.currentTarget as HTMLButtonElement).style.transform = "scale(1.01)"; }}
                  onMouseLeave={ev => { (ev.currentTarget as HTMLButtonElement).style.transform = "scale(1)"; }}
                >
                  <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 12, gap: 8 }}>
                    <div style={{ minWidth: 0 }}>
                      <span style={{ fontSize: 11, fontFamily: "monospace", color: "#64748b" }}>{e.id}</span>
                      <p style={{ fontWeight: 600, fontSize: 14, color: "white", margin: "2px 0", overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>{e.name}</p>
                      <p style={{ fontSize: 12, color: "#94a3b8", margin: 0 }}>{e.country}</p>
                    </div>
                    <div style={{ flexShrink: 0 }}>
                      <GaugeRing value={e.composite_score} stroke={RISK_COLORS[e.risk_level] ?? "#86efac"} />
                    </div>
                  </div>
                  <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
                    <span style={{ fontSize: 11, fontWeight: 700, textTransform: "uppercase", color: cfg.color }}>{cfg.label}</span>
                    <span style={{ fontSize: 12, color: "#64748b" }}>
                      Index: <span style={{ fontWeight: 700, color: "#86efac" }}>{indexVal ?? "—"}</span>
                    </span>
                  </div>
                </button>
              );
            })}
            {filtered.length === 0 && (
              <div style={{ gridColumn: "1 / -1", textAlign: "center", padding: "48px 0", color: "#64748b", fontSize: 14 }}>
                Aucune entit&eacute; dans ce niveau de risque
              </div>
            )}
          </div>
        </>
      )}

      {selected && <DetailModal entity={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
