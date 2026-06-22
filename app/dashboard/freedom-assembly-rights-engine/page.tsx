"use client";
import { useState, useEffect } from "react";

const RC: Record<string, string> = { critique: "#ef4444", "élevé": "#f97316", modéré: "#eab308", faible: "#22c55e" };
const ACCENT = "#0a1a05";
const ACCENT_VIS = "#22c55e";

interface Entity {
  id: string;
  name: string;
  country: string;
  composite_score: number;
  risk_level: string;
  primary_pattern: string;
  estimated_freedom_assembly_rights_index: number;
  last_updated: string;
  [key: string]: unknown;
}

interface DashData {
  total_entities?: number;
  avg_composite?: number;
  avg_estimated_freedom_assembly_rights_index?: number;
  risk_distribution?: Record<string, number>;
  confidence_score?: number;
  data_sources?: string[];
  critical_alerts?: string[];
  entities?: Entity[];
  [key: string]: unknown;
}

function GaugeRing({ value, label }: { value: number; label: string }) {
  const r = 36;
  const circ = 2 * Math.PI * r;
  const fill = circ * (1 - Math.min(value, 100) / 100);
  return (
    <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 4 }}>
      <svg viewBox="0 0 88 88" style={{ width: 96, height: 96 }}>
        <circle cx="44" cy="44" r={r} fill="none" stroke="#1e293b" strokeWidth="8" />
        <circle
          cx="44" cy="44" r={r} fill="none" stroke={ACCENT_VIS} strokeWidth="8"
          strokeDasharray={circ} strokeDashoffset={fill}
          strokeLinecap="round" transform="rotate(-90 44 44)"
        />
        <text x="44" y="49" textAnchor="middle" fill="white" fontSize="13" fontWeight="bold">
          {value.toFixed(1)}
        </text>
      </svg>
      <span style={{ fontSize: 11, color: "#94a3b8", textAlign: "center" }}>{label}</span>
    </div>
  );
}

function DetailModal({ entity, onClose }: { entity: Entity; onClose: () => void }) {
  const [tab, setTab] = useState<"apercu" | "metriques" | "sources">("apercu");
  const tabs: { key: "apercu" | "metriques" | "sources"; label: string }[] = [
    { key: "apercu", label: "Aperçu" },
    { key: "metriques", label: "Métriques" },
    { key: "sources", label: "Sources" },
  ];
  return (
    <div
      style={{ position: "fixed", inset: 0, zIndex: 50, display: "flex", alignItems: "center", justifyContent: "center", background: "rgba(0,0,0,0.7)", backdropFilter: "blur(4px)", padding: 16 }}
      onClick={onClose}
    >
      <div
        style={{ background: "#0f172a", border: "1px solid #334155", borderRadius: 16, width: "100%", maxWidth: 640, maxHeight: "90vh", overflowY: "auto", boxShadow: "0 25px 50px rgba(0,0,0,0.5)" }}
        onClick={(e) => e.stopPropagation()}
      >
        <div style={{ padding: "24px 24px 16px", borderBottom: "1px solid #1e293b", display: "flex", alignItems: "flex-start", justifyContent: "space-between", gap: 16 }}>
          <div>
            <h2 style={{ fontSize: 18, fontWeight: 700, color: "white", margin: 0 }}>{entity.name}</h2>
            <p style={{ fontSize: 13, color: "#94a3b8", margin: "4px 0 0" }}>{entity.country}</p>
            <span style={{ fontSize: 12, fontWeight: 700, textTransform: "uppercase", color: RC[entity.risk_level] ?? "#94a3b8" }}>{entity.risk_level}</span>
          </div>
          <button onClick={onClose} style={{ color: "#94a3b8", background: "none", border: "none", fontSize: 24, cursor: "pointer", lineHeight: 1 }}>&times;</button>
        </div>
        <div style={{ display: "flex", borderBottom: "1px solid #1e293b" }}>
          {tabs.map((t) => (
            <button
              key={t.key}
              onClick={() => setTab(t.key)}
              style={{
                flex: 1, padding: "12px 0", fontSize: 14, fontWeight: 500, background: "none", border: "none", cursor: "pointer",
                borderBottom: tab === t.key ? `2px solid ${ACCENT_VIS}` : "2px solid transparent",
                color: tab === t.key ? ACCENT_VIS : "#64748b",
              }}
            >
              {t.label}
            </button>
          ))}
        </div>
        <div style={{ padding: 24 }}>
          {tab === "apercu" && (
            <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16 }}>
                <div style={{ background: "#1e293b", borderRadius: 12, padding: 16, textAlign: "center" }}>
                  <div style={{ fontSize: 32, fontWeight: 700, color: ACCENT_VIS }}>{entity.composite_score.toFixed(1)}</div>
                  <div style={{ fontSize: 11, color: "#94a3b8", marginTop: 4 }}>Score Composite</div>
                </div>
                <div style={{ background: "#1e293b", borderRadius: 12, padding: 16, textAlign: "center" }}>
                  <div style={{ fontSize: 32, fontWeight: 700, color: ACCENT_VIS }}>{typeof entity.estimated_freedom_assembly_rights_index === "number" ? entity.estimated_freedom_assembly_rights_index.toFixed(2) : "—"}</div>
                  <div style={{ fontSize: 11, color: "#94a3b8", marginTop: 4 }}>Index Liberté Réunion</div>
                </div>
              </div>
              <div style={{ background: "#1e293b", borderRadius: 10, padding: 12, border: `1px solid ${RC[entity.risk_level] ?? "#475569"}33` }}>
                <span style={{ fontSize: 14, fontWeight: 600, color: RC[entity.risk_level] ?? "#94a3b8", textTransform: "capitalize" }}>
                  Niveau de risque : {entity.risk_level}
                </span>
              </div>
              <div style={{ background: "#1e293b", borderRadius: 12, padding: 16 }}>
                <div style={{ fontSize: 11, color: "#94a3b8", marginBottom: 6 }}>Pattern Principal</div>
                <div style={{ fontSize: 14, fontWeight: 500, color: ACCENT_VIS }}>{entity.primary_pattern}</div>
              </div>
            </div>
          )}
          {tab === "metriques" && (
            <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
              <div style={{ background: "#1e293b", borderRadius: 10, padding: 12 }}>
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 6 }}>
                  <span style={{ fontSize: 13, color: "#cbd5e1" }}>Score Composite</span>
                  <span style={{ fontSize: 14, fontWeight: 700, color: "white" }}>{entity.composite_score.toFixed(1)}</span>
                </div>
                <div style={{ height: 6, background: "#334155", borderRadius: 9999, overflow: "hidden" }}>
                  <div style={{ height: "100%", borderRadius: 9999, width: `${Math.min(entity.composite_score, 100)}%`, background: ACCENT_VIS }} />
                </div>
              </div>
              <div style={{ background: "#1e293b", borderRadius: 10, padding: 12 }}>
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 6 }}>
                  <span style={{ fontSize: 13, color: "#cbd5e1" }}>Index Liberté Réunion</span>
                  <span style={{ fontSize: 14, fontWeight: 700, color: "white" }}>{typeof entity.estimated_freedom_assembly_rights_index === "number" ? entity.estimated_freedom_assembly_rights_index.toFixed(2) : "—"}</span>
                </div>
                <div style={{ height: 6, background: "#334155", borderRadius: 9999, overflow: "hidden" }}>
                  <div style={{ height: "100%", borderRadius: 9999, width: `${Math.min((entity.estimated_freedom_assembly_rights_index ?? 0) * 10, 100)}%`, background: ACCENT_VIS }} />
                </div>
              </div>
            </div>
          )}
          {tab === "sources" && (
            <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
              <div style={{ background: "#1e293b", borderRadius: 12, padding: 16 }}>
                <div style={{ fontSize: 11, color: "#94a3b8", marginBottom: 8 }}>Informations Entité</div>
                <div style={{ fontSize: 13, color: "#cbd5e1" }}>ID : {entity.id}</div>
                <div style={{ fontSize: 13, color: "#cbd5e1", marginTop: 4 }}>Pays : {entity.country}</div>
                <div style={{ fontSize: 13, color: "#cbd5e1", marginTop: 4 }}>Pattern : {entity.primary_pattern}</div>
              </div>
              <div style={{ fontSize: 11, color: "#64748b" }}>
                Dernière mise à jour : {entity.last_updated ? new Date(entity.last_updated).toLocaleDateString("fr-FR") : "—"}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default function FreedomAssemblyRightsEnginePage() {
  const [data, setData] = useState<DashData | null>(null);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState("tous");
  const [selected, setSelected] = useState<Entity | null>(null);

  useEffect(() => {
    fetch("/api/freedom-assembly-rights-engine")
      .then(r => r.json())
      .then(d => { setData(d.payload ?? d); setLoading(false); })
      .catch(() => { setLoading(false); });
  }, []);

  if (loading) {
    return (
      <div style={{ background: "#030712", minHeight: "100vh", display: "flex", alignItems: "center", justifyContent: "center" }}>
        <div style={{ fontSize: 14, color: ACCENT_VIS }}>Initialisation Liberté de Réunion &amp; Association…</div>
      </div>
    );
  }

  const allEntities: Entity[] = data?.entities ?? (Array.isArray(data) ? data as unknown as Entity[] : []);
  const filtered = filter === "tous" ? allEntities : allEntities.filter(e => e.risk_level === filter);
  const avg = (arr: number[]) => arr.length ? arr.reduce((a, b) => a + b, 0) / arr.length : 0;
  const avgComposite = data?.avg_composite ?? avg(allEntities.map(e => e.composite_score));
  const avgIndex = data?.avg_estimated_freedom_assembly_rights_index ?? avg(allEntities.map(e => e.estimated_freedom_assembly_rights_index));
  const rd = data?.risk_distribution ?? {};
  const countCritique = rd["critique"] ?? allEntities.filter(e => e.risk_level === "critique").length;
  const countEleve = rd["élevé"] ?? allEntities.filter(e => e.risk_level === "élevé").length;
  const sources = data?.data_sources ?? [];
  const confidence = typeof data?.confidence_score === "number" ? `${(data.confidence_score * 100).toFixed(0)}%` : "—";
  const alerts = data?.critical_alerts ?? [];

  const kpis = [
    { label: "Entités Analysées", value: data?.total_entities ?? allEntities.length },
    { label: "Score Moyen", value: avgComposite.toFixed(1) },
    { label: "Index Liberté Réunion", value: avgIndex.toFixed(2) },
    { label: "Confiance", value: confidence },
    { label: "Critique", value: countCritique },
    { label: "Élevé", value: countEleve },
  ];

  const filters = ["tous", "critique", "élevé", "modéré", "faible"];

  return (
    <div style={{ minHeight: "100vh", background: "#030712", color: "white", padding: 24, display: "flex", flexDirection: "column", gap: 24 }}>
      {selected && <DetailModal entity={selected} onClose={() => setSelected(null)} />}

      {/* Header */}
      <div>
        <div style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 4 }}>
          <div style={{ width: 12, height: 32, borderRadius: 9999, background: ACCENT_VIS }} />
          <h1 style={{ fontSize: 24, fontWeight: 700, margin: 0, letterSpacing: "-0.025em" }}>Liberté de Réunion &amp; Association</h1>
        </div>
        <p style={{ color: "#94a3b8", fontSize: 13, margin: "0 0 0 24px" }}>
          Freedom Assembly Rights Engine — Caelum Partners · Chaima Mhadbi, Fondatrice, Bruxelles
        </p>
      </div>

      {/* KPI Cards */}
      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(140px, 1fr))", gap: 16 }}>
        {kpis.map(k => (
          <div key={k.label} style={{ background: "#0f172a", border: "1px solid #1e293b", borderRadius: 12, padding: 16 }}>
            <div style={{ fontSize: 11, color: "#64748b", marginBottom: 4 }}>{k.label}</div>
            <div style={{ fontSize: 20, fontWeight: 700, color: ACCENT_VIS }}>{k.value}</div>
          </div>
        ))}
      </div>

      {/* Gauges */}
      <div style={{ background: "#0f172a", border: "1px solid #1e293b", borderRadius: 12, padding: 20 }}>
        <h2 style={{ fontSize: 13, fontWeight: 600, color: "#94a3b8", margin: "0 0 16px" }}>Scores Moyens par Indicateur</h2>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(120px, 1fr))", gap: 24 }}>
          <GaugeRing value={avgComposite} label="Score Composite Moyen" />
          <GaugeRing value={avgIndex * 10} label="Index Réunion (×10)" />
          <GaugeRing value={countCritique * 12.5} label="% Critique" />
          <GaugeRing value={typeof data?.confidence_score === "number" ? data.confidence_score * 100 : 0} label="Confiance" />
        </div>
      </div>

      {/* Alerts */}
      {alerts.length > 0 && (
        <div style={{ background: "#0f172a", border: "1px solid #ef444430", borderRadius: 12, padding: 16 }}>
          <h3 style={{ fontSize: 12, fontWeight: 600, color: "#94a3b8", textTransform: "uppercase", letterSpacing: "0.05em", margin: "0 0 12px" }}>Alertes Critiques</h3>
          <div style={{ display: "flex", flexDirection: "column", gap: 6 }}>
            {alerts.map((a, i) => (
              <div key={i} style={{ fontSize: 13, color: "#ef4444", display: "flex", alignItems: "center", gap: 8 }}>
                <span style={{ width: 6, height: 6, borderRadius: 9999, background: "#ef4444", flexShrink: 0 }} />
                {a}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Filter Pills */}
      <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
        {filters.map(f => (
          <button
            key={f}
            onClick={() => setFilter(f)}
            style={{
              padding: "6px 16px", borderRadius: 9999, fontSize: 13, fontWeight: 500, cursor: "pointer", border: "none",
              background: filter === f ? ACCENT_VIS : "#1e293b",
              color: filter === f ? "white" : "#94a3b8",
            }}
          >
            {f.charAt(0).toUpperCase() + f.slice(1)}
          </button>
        ))}
      </div>

      {/* Entity Grid */}
      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(300px, 1fr))", gap: 16 }}>
        {filtered.map(e => (
          <div
            key={e.id}
            onClick={() => setSelected(e)}
            style={{
              border: `1px solid ${RC[e.risk_level] ?? "#475569"}40`,
              background: `${RC[e.risk_level] ?? "#475569"}10`,
              borderRadius: 12, padding: 16, cursor: "pointer", transition: "transform 0.15s",
            }}
            onMouseEnter={el => { if (el.currentTarget) el.currentTarget.style.transform = "scale(1.01)"; }}
            onMouseLeave={el => { if (el.currentTarget) el.currentTarget.style.transform = "scale(1)"; }}
          >
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 8 }}>
              <div style={{ flex: 1, minWidth: 0 }}>
                <div style={{ fontWeight: 600, fontSize: 13, lineHeight: 1.3 }}>{e.name}</div>
                <div style={{ fontSize: 11, color: "#94a3b8", marginTop: 4 }}>{e.country}</div>
              </div>
              <div style={{ textAlign: "right", marginLeft: 12, flexShrink: 0 }}>
                <div style={{ fontSize: 20, fontWeight: 700, color: "white" }}>{e.composite_score.toFixed(1)}</div>
                <div style={{ fontSize: 11, fontWeight: 700, textTransform: "uppercase", color: RC[e.risk_level] ?? "#94a3b8" }}>{e.risk_level}</div>
              </div>
            </div>
            <div style={{ height: 4, background: "#334155", borderRadius: 9999, overflow: "hidden", marginTop: 8 }}>
              <div style={{ height: "100%", borderRadius: 9999, width: `${Math.min(e.composite_score, 100)}%`, background: RC[e.risk_level] ?? ACCENT_VIS }} />
            </div>
            <div style={{ fontSize: 11, color: "#64748b", marginTop: 8 }}>
              Index Liberté Réunion: <span style={{ fontWeight: 500, color: ACCENT_VIS }}>{typeof e.estimated_freedom_assembly_rights_index === "number" ? e.estimated_freedom_assembly_rights_index.toFixed(2) : "—"}</span>
            </div>
            <div style={{ fontSize: 11, color: "#64748b", marginTop: 4 }}>Pattern: {e.primary_pattern}</div>
          </div>
        ))}
      </div>

      {filtered.length === 0 && (
        <div style={{ textAlign: "center", padding: "48px 0", color: "#64748b", fontSize: 14 }}>Aucune entité pour ce niveau de risque.</div>
      )}

      {/* Sources */}
      {sources.length > 0 && (
        <div style={{ background: "#0f172a", border: "1px solid #1e293b", borderRadius: 12, padding: 16 }}>
          <h3 style={{ fontSize: 11, fontWeight: 600, color: "#94a3b8", textTransform: "uppercase", letterSpacing: "0.05em", margin: "0 0 12px" }}>Sources de données</h3>
          <div style={{ display: "flex", flexWrap: "wrap", gap: 8 }}>
            {sources.map(src => (
              <span key={src} style={{ fontSize: 11, background: "#1e293b", color: "#94a3b8", padding: "4px 12px", borderRadius: 9999, border: "1px solid #334155" }}>{src}</span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
