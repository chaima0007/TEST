"use client";
import { useState, useEffect } from "react";

const ACCENT = "#0f0f1a";
const ACCENT_LIGHT = "#818cf8";
const RC: Record<string, string> = { critique: "#ef4444", "élevé": "#f97316", modéré: "#eab308", faible: "#22c55e" };

interface Entity {
  id: string;
  name: string;
  country: string;
  composite_score: number;
  risk_level: string;
  primary_pattern: string;
  estimated_anti_corruption_rights_index: number;
  [key: string]: unknown;
}

interface DashData {
  total_entities?: number;
  avg_composite?: number;
  confidence_score?: number;
  risk_distribution?: Record<string, number>;
  critical_alerts?: string[];
  data_sources?: string[];
  estimated_anti_corruption_rights_index?: number;
  entities?: Entity[];
}

function GaugeRing({ value, max = 100 }: { value: number; max?: number }) {
  const r = 36, cx = 44, cy = 44, circ = 2 * Math.PI * r;
  const pct = Math.min(value / max, 1);
  const dash = pct * circ;
  return (
    <svg viewBox="0 0 88 88" style={{ width: 96, height: 96 }}>
      <circle cx={cx} cy={cy} r={r} fill="none" stroke="#1e293b" strokeWidth={8} />
      <circle cx={cx} cy={cy} r={r} fill="none" stroke={ACCENT_LIGHT} strokeWidth={8}
        strokeDasharray={`${dash} ${circ}`} strokeLinecap="round"
        transform="rotate(-90 44 44)" />
      <text x={cx} y={cy + 1} textAnchor="middle" dominantBaseline="middle"
        fill={ACCENT_LIGHT} fontSize="14" fontWeight="700">{Math.round(value)}</text>
    </svg>
  );
}

function DetailModal({ entity, onClose }: { entity: Entity; onClose: () => void }) {
  const [tab, setTab] = useState<"apercu" | "metriques" | "sources">("apercu");
  const tabs: { key: "apercu" | "metriques" | "sources"; label: string }[] = [
    { key: "apercu", label: "Aperçu" },
    { key: "metriques", label: "Métriques" },
    { key: "sources", label: "Sources" },
  ];
  const color = RC[entity.risk_level] ?? ACCENT_LIGHT;
  return (
    <div style={{ position: "fixed", inset: 0, background: "rgba(0,0,0,0.75)", zIndex: 50, display: "flex", alignItems: "center", justifyContent: "center", padding: 16 }}
      onClick={onClose}>
      <div style={{ background: "#0f172a", border: "1px solid #334155", borderRadius: 16, width: "100%", maxWidth: 640, maxHeight: "85vh", overflowY: "auto" }}
        onClick={e => e.stopPropagation()}>
        <div style={{ padding: "24px 24px 16px", borderBottom: "1px solid #1e293b", display: "flex", justifyContent: "space-between", alignItems: "flex-start" }}>
          <div>
            <span style={{ fontSize: 11, fontWeight: 700, textTransform: "uppercase", color }}>{entity.risk_level}</span>
            <h2 style={{ fontSize: 17, fontWeight: 700, color: "#f1f5f9", margin: "4px 0 2px" }}>{entity.name}</h2>
            <p style={{ fontSize: 13, color: "#94a3b8" }}>{entity.country}</p>
          </div>
          <button onClick={onClose} style={{ background: "none", border: "none", color: "#64748b", fontSize: 20, cursor: "pointer" }}>✕</button>
        </div>
        <div style={{ display: "flex", borderBottom: "1px solid #1e293b" }}>
          {tabs.map(t => (
            <button key={t.key} onClick={() => setTab(t.key)}
              style={{ flex: 1, padding: "12px 0", fontSize: 13, fontWeight: 500, background: "none", border: "none", cursor: "pointer", borderBottom: tab === t.key ? `2px solid ${ACCENT_LIGHT}` : "2px solid transparent", color: tab === t.key ? ACCENT_LIGHT : "#64748b" }}>
              {t.label}
            </button>
          ))}
        </div>
        <div style={{ padding: 24 }}>
          {tab === "apercu" && (
            <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                <span style={{ color: "#94a3b8", fontSize: 14 }}>Score composite</span>
                <span style={{ fontSize: 24, fontWeight: 700, color: ACCENT_LIGHT }}>{entity.composite_score.toFixed(1)}/100</span>
              </div>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                <span style={{ color: "#94a3b8", fontSize: 14 }}>Indice Anticorruption Estimé</span>
                <span style={{ fontSize: 20, fontWeight: 700, color: ACCENT_LIGHT }}>{typeof entity.estimated_anti_corruption_rights_index === "number" ? entity.estimated_anti_corruption_rights_index.toFixed(2) : "—"}</span>
              </div>
              <div style={{ height: 1, background: "#1e293b" }} />
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                <span style={{ color: "#94a3b8", fontSize: 14 }}>Patron principal</span>
                <span style={{ fontSize: 13, color: "#e2e8f0", fontWeight: 500 }}>{String(entity.primary_pattern).replace(/_/g, " ")}</span>
              </div>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                <span style={{ color: "#94a3b8", fontSize: 14 }}>Niveau de risque</span>
                <span style={{ fontSize: 13, fontWeight: 700, color }}>{entity.risk_level}</span>
              </div>
            </div>
          )}
          {tab === "metriques" && (
            <div style={{ display: "flex", flexDirection: "column", gap: 14 }}>
              {[
                { label: "Score Composite", value: entity.composite_score },
                { label: "Indice ACR Estimé", value: (entity.estimated_anti_corruption_rights_index as number) * 10 },
              ].map(s => (
                <div key={s.label}>
                  <div style={{ display: "flex", justifyContent: "space-between", fontSize: 13, marginBottom: 4 }}>
                    <span style={{ color: "#94a3b8" }}>{s.label}</span>
                    <span style={{ color: "#e2e8f0" }}>{typeof s.value === "number" ? s.value.toFixed(1) : "—"}</span>
                  </div>
                  <div style={{ height: 6, background: "#1e293b", borderRadius: 999, overflow: "hidden" }}>
                    <div style={{ height: "100%", borderRadius: 999, background: ACCENT_LIGHT, width: `${Math.min(typeof s.value === "number" ? s.value : 0, 100)}%` }} />
                  </div>
                </div>
              ))}
            </div>
          )}
          {tab === "sources" && (
            <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
              {["transparency_international_cpi_2024", "un_convention_against_corruption", "world_bank_governance_indicators_2024", "global_integrity_report_2024"].map(s => (
                <div key={s} style={{ display: "flex", gap: 8, fontSize: 13, alignItems: "flex-start" }}>
                  <span style={{ color: ACCENT_LIGHT, marginTop: 2 }}>▸</span>
                  <span style={{ color: "#cbd5e1" }}>{s.replace(/_/g, " ")}</span>
                </div>
              ))}
            </div>
          )}
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
    fetch("/api/anti-corruption-rights-engine")
      .then(r => r.json())
      .then(d => { setData(d.payload ?? d); setLoading(false); })
      .catch(() => setLoading(false));
  }, []);

  if (loading) return (
    <div style={{ minHeight: "100vh", background: "#020617", display: "flex", alignItems: "center", justifyContent: "center" }}>
      <div style={{ color: ACCENT_LIGHT, fontSize: 14 }}>Initialisation Anti-Corruption Rights Engine…</div>
    </div>
  );

  const entities = data?.entities ?? [];
  const filtered = entities.filter(e => filter === "tous" || e.risk_level === filter);
  const dist = data?.risk_distribution ?? {};

  return (
    <div style={{ minHeight: "100vh", background: "#020617", color: "#f1f5f9", padding: 24 }}>
      {selected && <DetailModal entity={selected} onClose={() => setSelected(null)} />}

      {/* Header */}
      <div style={{ marginBottom: 32 }}>
        <div style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 8 }}>
          <div style={{ width: 4, height: 32, borderRadius: 999, background: ACCENT_LIGHT }} />
          <h1 style={{ fontSize: 28, fontWeight: 800, color: ACCENT_LIGHT, margin: 0 }}>Anti-Corruption Rights Engine</h1>
        </div>
        <p style={{ color: "#64748b", fontSize: 14, margin: 0, paddingLeft: 16 }}>Transparency International · ONU · Banque Mondiale · IPC · Gouvernance</p>
      </div>

      {/* KPIs */}
      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(140px, 1fr))", gap: 16, marginBottom: 32 }}>
        {[
          { label: "Entités", value: String(data?.total_entities ?? 8) },
          { label: "Critiques", value: String(dist.critique ?? 4), color: "#ef4444" },
          { label: "Élevés", value: String(dist["élevé"] ?? 2), color: "#f97316" },
          { label: "Indice ACR", value: String(data?.estimated_anti_corruption_rights_index ?? 6.18) },
          { label: "Confiance", value: `${Math.round((data?.confidence_score ?? 0.87) * 100)}%` },
        ].map(k => (
          <div key={k.label} style={{ background: "#0f172a", border: "1px solid #1e293b", borderRadius: 12, padding: 16 }}>
            <p style={{ fontSize: 11, color: "#64748b", textTransform: "uppercase", letterSpacing: "0.05em", margin: "0 0 6px" }}>{k.label}</p>
            <p style={{ fontSize: 26, fontWeight: 700, margin: 0, color: k.color ?? ACCENT_LIGHT }}>{k.value}</p>
          </div>
        ))}
        <div style={{ background: "#0f172a", border: "1px solid #1e293b", borderRadius: 12, padding: 16, display: "flex", flexDirection: "column", alignItems: "center" }}>
          <p style={{ fontSize: 11, color: "#64748b", textTransform: "uppercase", letterSpacing: "0.05em", margin: "0 0 6px" }}>Score Moyen</p>
          <GaugeRing value={data?.avg_composite ?? 61.77} />
        </div>
      </div>

      {/* Filter pills */}
      <div style={{ display: "flex", gap: 8, marginBottom: 24, flexWrap: "wrap" }}>
        {["tous", "critique", "élevé", "modéré", "faible"].map(f => (
          <button key={f} onClick={() => setFilter(f)}
            style={{ padding: "6px 16px", borderRadius: 999, fontSize: 13, fontWeight: 500, cursor: "pointer", border: `1px solid ${filter === f ? ACCENT_LIGHT : "#334155"}`, background: filter === f ? "rgba(129,140,248,0.1)" : "transparent", color: filter === f ? ACCENT_LIGHT : "#94a3b8" }}>
            {f.charAt(0).toUpperCase() + f.slice(1)}
          </button>
        ))}
      </div>

      {/* Entity grid */}
      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(300px, 1fr))", gap: 16, marginBottom: 32 }}>
        {filtered.map(e => {
          const color = RC[e.risk_level] ?? ACCENT_LIGHT;
          return (
            <button key={e.id} onClick={() => setSelected(e)}
              style={{ textAlign: "left", background: "#0f172a", border: `1px solid ${color}33`, borderRadius: 12, padding: 16, cursor: "pointer", transition: "transform 0.1s" }}
              onMouseEnter={ev => (ev.currentTarget.style.transform = "scale(1.01)")}
              onMouseLeave={ev => (ev.currentTarget.style.transform = "scale(1)")}>
              <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 8 }}>
                <span style={{ fontSize: 11, fontFamily: "monospace", color: "#64748b" }}>{e.id}</span>
                <span style={{ fontSize: 11, fontWeight: 700, textTransform: "uppercase", color }}>{e.risk_level}</span>
              </div>
              <p style={{ fontSize: 13, fontWeight: 600, color: "#f1f5f9", margin: "0 0 4px", lineHeight: 1.4 }}>{e.name}</p>
              <p style={{ fontSize: 12, color: "#64748b", margin: "0 0 12px" }}>{e.country}</p>
              <div style={{ height: 4, background: "#1e293b", borderRadius: 999, overflow: "hidden", marginBottom: 8 }}>
                <div style={{ height: "100%", background: color, borderRadius: 999, width: `${Math.min(e.composite_score, 100)}%` }} />
              </div>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                <span style={{ fontSize: 11, color: "#64748b" }}>Composite</span>
                <span style={{ fontSize: 18, fontWeight: 700, color: ACCENT_LIGHT }}>{e.composite_score}</span>
              </div>
              <div style={{ fontSize: 11, color: "#64748b", marginTop: 4 }}>
                Indice ACR: <span style={{ color: ACCENT_LIGHT, fontWeight: 600 }}>{typeof e.estimated_anti_corruption_rights_index === "number" ? e.estimated_anti_corruption_rights_index.toFixed(2) : "—"}</span>
              </div>
            </button>
          );
        })}
      </div>

      {/* Critical alerts */}
      {data?.critical_alerts && data.critical_alerts.length > 0 && (
        <div style={{ background: "#0f172a", border: "1px solid #ef444433", borderRadius: 12, padding: 20 }}>
          <h3 style={{ fontSize: 13, fontWeight: 700, color: "#ef4444", textTransform: "uppercase", letterSpacing: "0.05em", margin: "0 0 12px" }}>Alertes Critiques</h3>
          <ul style={{ listStyle: "none", margin: 0, padding: 0, display: "flex", flexDirection: "column", gap: 8 }}>
            {data.critical_alerts.map((a, i) => (
              <li key={i} style={{ fontSize: 13, color: "#fca5a5", display: "flex", gap: 8 }}>
                <span style={{ color: "#ef4444" }}>▸</span>{a}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
