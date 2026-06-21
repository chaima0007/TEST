"use client";
import { useState, useEffect } from "react";

const RC: Record<string, string> = { critique: "text-red-400", "élevé": "text-orange-400", modéré: "text-yellow-400", faible: "text-emerald-400" };
const RB: Record<string, string> = { critique: "border-red-500/30 bg-red-500/10", "élevé": "border-orange-500/30 bg-orange-500/10", modéré: "border-yellow-500/30 bg-yellow-500/10", faible: "border-emerald-500/30 bg-emerald-500/10" };

const ACCENT = "#0e7490";

interface Entity {
  id: string;
  name: string;
  country: string;
  composite_score: number;
  corporate_water_capture_score: number;
  access_denial_marginalized_communities_score: number;
  commodification_human_right_violation_score: number;
  regulatory_capture_accountability_score: number;
  estimated_water_privatization_commons_index: number;
  risk_level: string;
  primary_pattern: string;
  last_updated: string;
  [key: string]: unknown;
}

interface DashData {
  total_entities?: number;
  avg_composite?: number;
  avg_estimated_water_privatization_commons_index?: number;
  risk_distribution?: Record<string, number>;
  confidence_score?: number;
  data_sources?: string[];
  entities?: Entity[];
  [key: string]: unknown;
}

function GaugeRing({ value, label }: { value: number; label: string }) {
  const r = 36;
  const circ = 2 * Math.PI * r;
  const fill = circ * (1 - Math.min(value, 100) / 100);
  return (
    <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: "4px" }}>
      <svg width="88" height="88" viewBox="0 0 88 88">
        <circle cx="44" cy="44" r={r} fill="none" stroke="#1e293b" strokeWidth={8} />
        <circle
          cx="44" cy="44" r={r} fill="none" stroke={ACCENT} strokeWidth={8}
          strokeDasharray={circ} strokeDashoffset={fill}
          strokeLinecap="round" transform="rotate(-90 44 44)"
        />
        <text x="44" y="49" textAnchor="middle" fill="white" fontSize="13" fontWeight="bold">
          {value.toFixed(1)}
        </text>
      </svg>
      <span style={{ fontSize: "11px", color: "#94a3b8", textAlign: "center" }}>{label}</span>
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
  const subScores = [
    { label: "Capture Corporative Eau", value: entity.corporate_water_capture_score, weight: "0.30" },
    { label: "Déni Accès Communautés Marginalisées", value: entity.access_denial_marginalized_communities_score, weight: "0.25" },
    { label: "Marchandisation Droit Humain", value: entity.commodification_human_right_violation_score, weight: "0.25" },
    { label: "Capture Régulatoire & Responsabilité", value: entity.regulatory_capture_accountability_score, weight: "0.20" },
  ];
  return (
    <div style={{ position: "fixed", inset: 0, zIndex: 50, display: "flex", alignItems: "center", justifyContent: "center", background: "rgba(0,0,0,0.7)", backdropFilter: "blur(4px)", padding: "16px" }} onClick={onClose}>
      <div style={{ background: "#0f172a", border: "1px solid #334155", borderRadius: "16px", width: "100%", maxWidth: "672px", maxHeight: "90vh", overflowY: "auto" }} onClick={(e) => e.stopPropagation()}>
        <div style={{ padding: "24px", borderBottom: "1px solid #1e293b", display: "flex", justifyContent: "space-between", alignItems: "flex-start", gap: "16px" }}>
          <div>
            <h2 style={{ fontSize: "20px", fontWeight: "bold", color: "white" }}>{entity.name}</h2>
            <p style={{ fontSize: "14px", color: "#94a3b8", marginTop: "2px" }}>{entity.country}</p>
            <span style={{ fontSize: "12px", fontWeight: 600, textTransform: "uppercase", marginTop: "4px", display: "inline-block" }} className={RC[entity.risk_level] ?? ""}>{entity.risk_level}</span>
          </div>
          <button onClick={onClose} style={{ color: "#94a3b8", fontSize: "24px", lineHeight: 1, background: "none", border: "none", cursor: "pointer" }}>&times;</button>
        </div>
        <div style={{ display: "flex", borderBottom: "1px solid #1e293b" }}>
          {tabs.map((t) => (
            <button key={t.key} onClick={() => setTab(t.key)}
              style={{ flex: 1, padding: "12px", fontSize: "14px", fontWeight: 500, background: "none", border: "none", cursor: "pointer", borderBottom: tab === t.key ? `2px solid ${ACCENT}` : "2px solid transparent", color: tab === t.key ? ACCENT : "#64748b" }}>
              {t.label}
            </button>
          ))}
        </div>
        <div style={{ padding: "24px" }}>
          {tab === "apercu" && (
            <div style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "16px" }}>
                <div style={{ background: "rgba(30,41,59,0.5)", borderRadius: "12px", padding: "16px", textAlign: "center" }}>
                  <div style={{ fontSize: "30px", fontWeight: "bold", color: ACCENT }}>{entity.composite_score.toFixed(1)}</div>
                  <div style={{ fontSize: "12px", color: "#94a3b8", marginTop: "4px" }}>Score Composite</div>
                </div>
                <div style={{ background: "rgba(30,41,59,0.5)", borderRadius: "12px", padding: "16px", textAlign: "center" }}>
                  <div style={{ fontSize: "30px", fontWeight: "bold", color: ACCENT }}>{typeof entity.estimated_water_privatization_commons_index === "number" ? entity.estimated_water_privatization_commons_index.toFixed(2) : "—"}</div>
                  <div style={{ fontSize: "12px", color: "#94a3b8", marginTop: "4px" }}>Index Eau &amp; Droits Communs</div>
                </div>
              </div>
              <div style={{ borderRadius: "8px", padding: "12px" }} className={RB[entity.risk_level] ?? ""}>
                <span style={{ fontSize: "14px", fontWeight: 600, textTransform: "capitalize" }} className={RC[entity.risk_level] ?? ""}>
                  Niveau de risque : {entity.risk_level}
                </span>
              </div>
              <div style={{ background: "rgba(30,41,59,0.5)", borderRadius: "12px", padding: "16px" }}>
                <div style={{ fontSize: "12px", color: "#94a3b8", marginBottom: "8px" }}>Pattern Principal</div>
                <div style={{ fontSize: "14px", fontWeight: 500, color: ACCENT }}>{entity.primary_pattern}</div>
              </div>
            </div>
          )}
          {tab === "metriques" && (
            <div style={{ display: "flex", flexDirection: "column", gap: "12px" }}>
              {subScores.map((s) => (
                <div key={s.label} style={{ background: "rgba(30,41,59,0.5)", borderRadius: "8px", padding: "12px" }}>
                  <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "6px" }}>
                    <span style={{ fontSize: "14px", color: "#cbd5e1" }}>{s.label}</span>
                    <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
                      <span style={{ fontSize: "12px", color: "#64748b" }}>×{s.weight}</span>
                      <span style={{ fontSize: "14px", fontWeight: "bold", color: "white" }}>{typeof s.value === "number" ? s.value.toFixed(1) : "—"}</span>
                    </div>
                  </div>
                  <div style={{ height: "8px", background: "#1e293b", borderRadius: "999px", overflow: "hidden" }}>
                    <div style={{ height: "100%", borderRadius: "999px", width: `${Math.min(typeof s.value === "number" ? s.value : 0, 100)}%`, background: ACCENT }} />
                  </div>
                </div>
              ))}
            </div>
          )}
          {tab === "sources" && (
            <div style={{ background: "rgba(30,41,59,0.5)", borderRadius: "12px", padding: "16px" }}>
              <div style={{ fontSize: "12px", color: "#94a3b8", marginBottom: "8px" }}>Dernière mise à jour</div>
              <div style={{ fontSize: "14px", color: "#cbd5e1" }}>{new Date(entity.last_updated).toLocaleDateString("fr-FR")}</div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default function WaterPrivatizationCommonsRightsEnginePage() {
  const [data, setData] = useState<DashData | null>(null);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState("tous");
  const [selected, setSelected] = useState<Entity | null>(null);

  useEffect(() => {
    fetch("/api/water-privatization-commons-rights-engine")
      .then(r => r.json())
      .then(d => { setData(d.payload ?? d); setLoading(false); })
      .catch(() => { setLoading(false); });
  }, []);

  if (loading) {
    return (
      <div style={{ background: "#020617", minHeight: "100vh", display: "flex", alignItems: "center", justifyContent: "center" }}>
        <div style={{ fontSize: "14px", color: ACCENT }}>Initialisation Privatisation Eau &amp; Droits Communs…</div>
      </div>
    );
  }

  const allEntities: Entity[] = data?.entities ?? (Array.isArray(data) ? data as unknown as Entity[] : []);
  const filtered = filter === "tous" ? allEntities : allEntities.filter(e => e.risk_level === filter);
  const avg = (arr: number[]) => arr.length ? arr.reduce((a, b) => a + b, 0) / arr.length : 0;
  const avgComposite = data?.avg_composite ?? avg(allEntities.map(e => e.composite_score));
  const avgIndex = data?.avg_estimated_water_privatization_commons_index ?? avg(allEntities.map(e => e.estimated_water_privatization_commons_index));
  const rd = data?.risk_distribution ?? {};
  const countCritique = rd["critique"] ?? allEntities.filter(e => e.risk_level === "critique").length;
  const countEleve = rd["élevé"] ?? allEntities.filter(e => e.risk_level === "élevé").length;
  const sources = data?.data_sources ?? [];
  const confidence = typeof data?.confidence_score === "number" ? `${(data.confidence_score * 100).toFixed(0)}%` : "—";

  const avgCorporate = avg(allEntities.map(e => e.corporate_water_capture_score));
  const avgAccess = avg(allEntities.map(e => e.access_denial_marginalized_communities_score));
  const avgCommodification = avg(allEntities.map(e => e.commodification_human_right_violation_score));
  const avgRegulatory = avg(allEntities.map(e => e.regulatory_capture_accountability_score));

  const kpis = [
    { label: "Entités Analysées", value: data?.total_entities ?? allEntities.length },
    { label: "Score Moyen", value: avgComposite.toFixed(1) },
    { label: "Index Eau & Communs", value: avgIndex.toFixed(2) },
    { label: "Confiance", value: confidence },
    { label: "Critique", value: countCritique },
    { label: "Élevé", value: countEleve },
  ];

  const filters = ["tous", "critique", "élevé", "modéré", "faible"];

  return (
    <div style={{ minHeight: "100vh", background: "#020617", color: "white", padding: "24px", display: "flex", flexDirection: "column", gap: "24px" }}>
      {selected && <DetailModal entity={selected} onClose={() => setSelected(null)} />}

      <div>
        <div style={{ display: "flex", alignItems: "center", gap: "12px", marginBottom: "4px" }}>
          <div style={{ width: "12px", height: "32px", borderRadius: "999px", background: ACCENT }} />
          <h1 style={{ fontSize: "24px", fontWeight: "bold", letterSpacing: "-0.025em" }}>Privatisation Eau &amp; Droits Communs</h1>
        </div>
        <p style={{ color: "#94a3b8", fontSize: "14px", marginLeft: "24px" }}>
          Water Privatization &amp; Commons Rights Engine — Caelum Partners · Chaima Mhadbi, Fondatrice, Bruxelles
        </p>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(120px, 1fr))", gap: "16px" }}>
        {kpis.map(k => (
          <div key={k.label} style={{ background: "#0f172a", border: "1px solid #1e293b", borderRadius: "12px", padding: "16px" }}>
            <div style={{ fontSize: "12px", color: "#64748b", marginBottom: "4px" }}>{k.label}</div>
            <div style={{ fontSize: "20px", fontWeight: "bold", color: ACCENT }}>{k.value}</div>
          </div>
        ))}
      </div>

      <div style={{ background: "#0f172a", border: "1px solid #1e293b", borderRadius: "12px", padding: "20px" }}>
        <h2 style={{ fontSize: "14px", fontWeight: 600, color: "#94a3b8", marginBottom: "16px" }}>Scores Moyens par Dimension</h2>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(100px, 1fr))", gap: "24px" }}>
          <GaugeRing value={avgCorporate} label="Capture Corporative" />
          <GaugeRing value={avgAccess} label="Déni Accès" />
          <GaugeRing value={avgCommodification} label="Marchandisation" />
          <GaugeRing value={avgRegulatory} label="Capture Régulatoire" />
        </div>
      </div>

      <div style={{ display: "flex", gap: "8px", flexWrap: "wrap" }}>
        {filters.map(f => (
          <button key={f} onClick={() => setFilter(f)}
            style={{ padding: "6px 16px", borderRadius: "999px", fontSize: "14px", fontWeight: 500, border: "none", cursor: "pointer", background: filter === f ? ACCENT : "#1e293b", color: filter === f ? "white" : "#94a3b8" }}>
            {f.charAt(0).toUpperCase() + f.slice(1)}
          </button>
        ))}
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(300px, 1fr))", gap: "16px" }}>
        {filtered.map(e => (
          <div key={e.id} onClick={() => setSelected(e)}
            style={{ border: "1px solid", borderRadius: "12px", padding: "16px", cursor: "pointer", transition: "transform 0.1s" }}
            className={RB[e.risk_level] ?? "border-slate-700 bg-slate-900"}
            onMouseEnter={el => (el.currentTarget.style.transform = "scale(1.01)")}
            onMouseLeave={el => (el.currentTarget.style.transform = "scale(1)")}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: "8px" }}>
              <div style={{ flex: 1, minWidth: 0 }}>
                <div style={{ fontWeight: 600, fontSize: "14px", lineHeight: 1.3, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>{e.name}</div>
                <div style={{ fontSize: "12px", color: "#94a3b8", marginTop: "4px" }}>{e.country}</div>
              </div>
              <div style={{ textAlign: "right", marginLeft: "12px", flexShrink: 0 }}>
                <div style={{ fontSize: "20px", fontWeight: "bold", color: "white" }}>{e.composite_score.toFixed(1)}</div>
                <div style={{ fontSize: "12px", fontWeight: "bold", textTransform: "uppercase", marginTop: "4px" }} className={RC[e.risk_level] ?? ""}>{e.risk_level}</div>
              </div>
            </div>
            <div style={{ height: "6px", background: "#1e293b", borderRadius: "999px", overflow: "hidden", marginTop: "8px" }}>
              <div style={{ height: "100%", borderRadius: "999px", width: `${Math.min(e.composite_score, 100)}%`, background: ACCENT }} />
            </div>
            <div style={{ fontSize: "12px", color: "#64748b", marginTop: "8px" }}>
              Index Eau &amp; Communs: <span style={{ fontWeight: 500, color: ACCENT }}>{typeof e.estimated_water_privatization_commons_index === "number" ? e.estimated_water_privatization_commons_index.toFixed(2) : "—"}</span>
            </div>
          </div>
        ))}
      </div>

      {filtered.length === 0 && (
        <div style={{ textAlign: "center", padding: "48px 0", color: "#64748b", fontSize: "14px" }}>Aucune entité pour ce niveau de risque.</div>
      )}

      {sources.length > 0 && (
        <div style={{ background: "#0f172a", border: "1px solid #1e293b", borderRadius: "12px", padding: "16px" }}>
          <h3 style={{ fontSize: "12px", color: "#94a3b8", textTransform: "uppercase", letterSpacing: "0.05em", marginBottom: "12px" }}>Sources de données</h3>
          <div style={{ display: "flex", flexWrap: "wrap", gap: "8px" }}>
            {sources.map((src) => (
              <span key={src} style={{ fontSize: "12px", background: "#1e293b", color: "#94a3b8", padding: "4px 12px", borderRadius: "999px", border: "1px solid rgba(51,65,85,0.5)" }}>{src}</span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
