"use client";
import { useState, useEffect } from "react";

const RC: Record<string, string> = { critique: "#ef4444", "élevé": "#f97316", modéré: "#eab308", faible: "#22c55e" };

const ACCENT = "#1a1a06";
const ACCENT_LIGHT = "#c9b800";

interface Entity {
  id: string;
  name: string;
  country: string;
  composite_score: number;
  pension_coverage_adequacy_score: number;
  elderly_healthcare_access_deficit_score: number;
  age_discrimination_employment_score: number;
  state_social_protection_elderly_deficit_score: number;
  estimated_pension_elderly_rights_index: number;
  risk_level: string;
  primary_pattern: string;
  last_updated: string;
  [key: string]: unknown;
}

interface DashData {
  total_entities?: number;
  avg_composite?: number;
  avg_estimated_pension_elderly_rights_index?: number;
  risk_distribution?: Record<string, number>;
  confidence_score?: number;
  data_sources?: string[];
  entities?: Entity[];
  [key: string]: unknown;
}

const FALLBACK_ENTITIES: Entity[] = [
  {
    id: "PER-001",
    name: "Somalia — Absence totale système retraite, vieillards sans filet",
    country: "Somalia",
    pension_coverage_adequacy_score: 96.0,
    elderly_healthcare_access_deficit_score: 94.0,
    age_discrimination_employment_score: 93.0,
    state_social_protection_elderly_deficit_score: 95.0,
    composite_score: 94.55,
    risk_level: "critique",
    primary_pattern: "Aucun système de retraite formel, 97% personnes âgées sans pension, dépendance totale famille",
    estimated_pension_elderly_rights_index: 9.46,
    last_updated: "2026-06-22",
  },
  {
    id: "PER-002",
    name: "Afghanistan — Retraites inexistantes, personnes âgées dépendantes",
    country: "Afghanistan",
    pension_coverage_adequacy_score: 91.0,
    elderly_healthcare_access_deficit_score: 90.0,
    age_discrimination_employment_score: 89.0,
    state_social_protection_elderly_deficit_score: 90.0,
    composite_score: 90.10,
    risk_level: "critique",
    primary_pattern: "Taliban suspend pensions fonctionnaires, femmes âgées exclues, système santé effondré",
    estimated_pension_elderly_rights_index: 9.01,
    last_updated: "2026-06-22",
  },
  {
    id: "PER-003",
    name: "Yemen — Crise pensions fonctionnaires, aînés en famine",
    country: "Yemen",
    pension_coverage_adequacy_score: 89.0,
    elderly_healthcare_access_deficit_score: 88.0,
    age_discrimination_employment_score: 86.0,
    state_social_protection_elderly_deficit_score: 88.0,
    composite_score: 87.85,
    risk_level: "critique",
    primary_pattern: "Pensions non versées depuis 2016, 21M en insécurité alimentaire incluant aînés, hôpitaux détruits",
    estimated_pension_elderly_rights_index: 8.79,
    last_updated: "2026-06-22",
  },
  {
    id: "PER-004",
    name: "Haiti — Effondrement système retraite, personnes âgées abandonnées",
    country: "Haiti",
    pension_coverage_adequacy_score: 83.0,
    elderly_healthcare_access_deficit_score: 82.0,
    age_discrimination_employment_score: 81.0,
    state_social_protection_elderly_deficit_score: 83.0,
    composite_score: 82.40,
    risk_level: "critique",
    primary_pattern: "ONA (retraite) insolvable, gangs contrôlent accès soins, aînés victimes violence",
    estimated_pension_elderly_rights_index: 8.24,
    last_updated: "2026-06-22",
  },
  {
    id: "PER-005",
    name: "India — Couverture pension fragmentée, 90% sans protection formelle",
    country: "India",
    pension_coverage_adequacy_score: 53.0,
    elderly_healthcare_access_deficit_score: 52.0,
    age_discrimination_employment_score: 51.0,
    state_social_protection_elderly_deficit_score: 53.0,
    composite_score: 52.40,
    risk_level: "élevé",
    primary_pattern: "90% travailleurs informels sans retraite, Ayushman Bharat limité, discrimination âge marché emploi",
    estimated_pension_elderly_rights_index: 5.24,
    last_updated: "2026-06-22",
  },
  {
    id: "PER-006",
    name: "Nigeria — Pensions impayées, fonctionnaires retraités sans revenus",
    country: "Nigeria",
    pension_coverage_adequacy_score: 52.0,
    elderly_healthcare_access_deficit_score: 51.0,
    age_discrimination_employment_score: 52.0,
    state_social_protection_elderly_deficit_score: 52.0,
    composite_score: 51.90,
    risk_level: "élevé",
    primary_pattern: "Pensions fonctionnaires impayées 14 États, Contributory Pension Scheme exclu informel",
    estimated_pension_elderly_rights_index: 5.19,
    last_updated: "2026-06-22",
  },
  {
    id: "PER-007",
    name: "USA — Inégalités retraite raciales, Medicare gaps, pauvreté seniors",
    country: "USA",
    pension_coverage_adequacy_score: 30.0,
    elderly_healthcare_access_deficit_score: 31.0,
    age_discrimination_employment_score: 29.0,
    state_social_protection_elderly_deficit_score: 30.0,
    composite_score: 30.00,
    risk_level: "modéré",
    primary_pattern: "Écart pension racial 40%, Medicare lacunes soins dentaires/vision, ADEA sous-appliqué",
    estimated_pension_elderly_rights_index: 3.00,
    last_updated: "2026-06-22",
  },
  {
    id: "PER-008",
    name: "Denmark — Modèle pension universel, protection seniors exemplaire",
    country: "Denmark",
    pension_coverage_adequacy_score: 5.0,
    elderly_healthcare_access_deficit_score: 5.0,
    age_discrimination_employment_score: 5.0,
    state_social_protection_elderly_deficit_score: 5.0,
    composite_score: 5.00,
    risk_level: "faible",
    primary_pattern: "Folkepension universel, Ældrebolig soins seniors, taux pauvreté personnes âgées 3%",
    estimated_pension_elderly_rights_index: 0.50,
    last_updated: "2026-06-22",
  },
];

function GaugeRing({ value, label }: { value: number; label: string }) {
  const r = 36;
  const circ = 2 * Math.PI * r;
  const fill = circ * (1 - Math.min(value, 100) / 100);
  return (
    <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 4 }}>
      <svg viewBox="0 0 88 88" style={{ width: 96, height: 96 }}>
        <circle cx={44} cy={44} r={r} fill="none" stroke="#1e293b" strokeWidth={8} />
        <circle
          cx={44} cy={44} r={r} fill="none" stroke={ACCENT_LIGHT} strokeWidth={8}
          strokeDasharray={circ} strokeDashoffset={fill}
          strokeLinecap="round" transform="rotate(-90 44 44)"
        />
        <text x={44} y={49} textAnchor="middle" fill="white" fontSize={13} fontWeight="bold">
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
  const subScores = [
    { label: "Couverture & Adéquation Pension", value: entity.pension_coverage_adequacy_score, weight: "0.30" },
    { label: "Déficit Accès Soins Personnes Âgées", value: entity.elderly_healthcare_access_deficit_score, weight: "0.25" },
    { label: "Discrimination Âge & Emploi", value: entity.age_discrimination_employment_score, weight: "0.25" },
    { label: "Déficit Protection Sociale État", value: entity.state_social_protection_elderly_deficit_score, weight: "0.20" },
  ];
  const riskColor = RC[entity.risk_level] ?? "#94a3b8";
  return (
    <div
      style={{ position: "fixed", inset: 0, zIndex: 50, display: "flex", alignItems: "center", justifyContent: "center", background: "rgba(0,0,0,0.7)", backdropFilter: "blur(4px)", padding: 16 }}
      onClick={onClose}
    >
      <div
        style={{ background: "#0f172a", border: "1px solid #334155", borderRadius: 16, width: "100%", maxWidth: 672, maxHeight: "90vh", overflowY: "auto", boxShadow: "0 25px 50px rgba(0,0,0,0.5)" }}
        onClick={(e) => e.stopPropagation()}
      >
        <div style={{ padding: 24, borderBottom: "1px solid #1e293b", display: "flex", justifyContent: "space-between", gap: 16 }}>
          <div>
            <h2 style={{ fontSize: 20, fontWeight: 700, color: "white", margin: 0 }}>{entity.name}</h2>
            <p style={{ fontSize: 13, color: "#94a3b8", marginTop: 2 }}>{entity.country}</p>
            <span style={{ fontSize: 11, fontWeight: 700, textTransform: "uppercase", color: riskColor, marginTop: 4, display: "inline-block" }}>{entity.risk_level}</span>
          </div>
          <button onClick={onClose} style={{ color: "#94a3b8", background: "none", border: "none", fontSize: 24, cursor: "pointer", lineHeight: 1 }}>&times;</button>
        </div>
        <div style={{ display: "flex", borderBottom: "1px solid #1e293b" }}>
          {tabs.map((t) => (
            <button key={t.key} onClick={() => setTab(t.key)}
              style={{ flex: 1, padding: "12px 0", fontSize: 13, fontWeight: 500, background: "none", border: "none", cursor: "pointer", borderBottom: tab === t.key ? `2px solid ${ACCENT_LIGHT}` : "2px solid transparent", color: tab === t.key ? ACCENT_LIGHT : "#64748b", transition: "color 0.2s" }}>
              {t.label}
            </button>
          ))}
        </div>
        <div style={{ padding: 24 }}>
          {tab === "apercu" && (
            <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16 }}>
                <div style={{ background: "rgba(255,255,255,0.04)", borderRadius: 12, padding: 16, textAlign: "center" }}>
                  <div style={{ fontSize: 30, fontWeight: 700, color: ACCENT_LIGHT }}>{entity.composite_score.toFixed(1)}</div>
                  <div style={{ fontSize: 11, color: "#94a3b8", marginTop: 4 }}>Score Composite</div>
                </div>
                <div style={{ background: "rgba(255,255,255,0.04)", borderRadius: 12, padding: 16, textAlign: "center" }}>
                  <div style={{ fontSize: 30, fontWeight: 700, color: ACCENT_LIGHT }}>
                    {typeof entity.estimated_pension_elderly_rights_index === "number" ? entity.estimated_pension_elderly_rights_index.toFixed(2) : "—"}
                  </div>
                  <div style={{ fontSize: 11, color: "#94a3b8", marginTop: 4 }}>Index Droits Pension & Aînés</div>
                </div>
              </div>
              <div style={{ background: `${riskColor}18`, border: `1px solid ${riskColor}4d`, borderRadius: 8, padding: 12 }}>
                <span style={{ fontSize: 13, fontWeight: 600, color: riskColor, textTransform: "capitalize" }}>Niveau de risque : {entity.risk_level}</span>
              </div>
              <div style={{ background: "rgba(255,255,255,0.04)", borderRadius: 12, padding: 16 }}>
                <div style={{ fontSize: 11, color: "#94a3b8", marginBottom: 8 }}>Pattern Principal</div>
                <div style={{ fontSize: 13, fontWeight: 500, color: ACCENT_LIGHT }}>{entity.primary_pattern}</div>
              </div>
            </div>
          )}
          {tab === "metriques" && (
            <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
              {subScores.map((s) => (
                <div key={s.label} style={{ background: "rgba(255,255,255,0.04)", borderRadius: 8, padding: 12 }}>
                  <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 6 }}>
                    <span style={{ fontSize: 13, color: "#cbd5e1" }}>{s.label}</span>
                    <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
                      <span style={{ fontSize: 11, color: "#64748b" }}>×{s.weight}</span>
                      <span style={{ fontSize: 13, fontWeight: 700, color: "white" }}>{typeof s.value === "number" ? s.value.toFixed(1) : "—"}</span>
                    </div>
                  </div>
                  <div style={{ height: 6, background: "#1e293b", borderRadius: 9999, overflow: "hidden" }}>
                    <div style={{ height: "100%", borderRadius: 9999, background: ACCENT_LIGHT, width: `${Math.min(typeof s.value === "number" ? s.value : 0, 100)}%` }} />
                  </div>
                </div>
              ))}
            </div>
          )}
          {tab === "sources" && (
            <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
              <div style={{ background: "rgba(255,255,255,0.04)", borderRadius: 12, padding: 16 }}>
                <div style={{ fontSize: 11, color: "#94a3b8", marginBottom: 8 }}>Dernière mise à jour</div>
                <div style={{ fontSize: 13, color: "#cbd5e1" }}>{new Date(entity.last_updated).toLocaleDateString("fr-FR")}</div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default function PensionElderlyRightsEnginePage() {
  const [data, setData] = useState<DashData | null>(null);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState("tous");
  const [selected, setSelected] = useState<Entity | null>(null);

  useEffect(() => {
    fetch("/api/pension-elderly-rights-engine")
      .then(r => r.json())
      .then(d => { setData(d.payload ?? d); setLoading(false); })
      .catch(() => { setLoading(false); });
  }, []);

  if (loading) {
    return (
      <div style={{ background: "#030712", minHeight: "100vh", display: "flex", alignItems: "center", justifyContent: "center" }}>
        <div style={{ color: ACCENT_LIGHT, fontSize: 13, animation: "pulse 2s infinite" }}>Initialisation Droits Pension &amp; Personnes Âgées…</div>
      </div>
    );
  }

  const allEntities: Entity[] = data?.entities ?? FALLBACK_ENTITIES;
  const filtered = filter === "tous" ? allEntities : allEntities.filter(e => e.risk_level === filter);
  const avg = (arr: number[]) => arr.length ? arr.reduce((a, b) => a + b, 0) / arr.length : 0;
  const avgComposite = data?.avg_composite ?? avg(allEntities.map(e => e.composite_score));
  const avgIndex = data?.avg_estimated_pension_elderly_rights_index ?? avg(allEntities.map(e => e.estimated_pension_elderly_rights_index));
  const rd = data?.risk_distribution ?? {};
  const countCritique = rd["critique"] ?? allEntities.filter(e => e.risk_level === "critique").length;
  const countEleve = rd["élevé"] ?? allEntities.filter(e => e.risk_level === "élevé").length;
  const sources = data?.data_sources ?? [];
  const confidence = typeof data?.confidence_score === "number" ? `${(data.confidence_score * 100).toFixed(0)}%` : "—";

  const avgPension = avg(allEntities.map(e => e.pension_coverage_adequacy_score));
  const avgHealthcare = avg(allEntities.map(e => e.elderly_healthcare_access_deficit_score));
  const avgDiscrimination = avg(allEntities.map(e => e.age_discrimination_employment_score));
  const avgStateProtection = avg(allEntities.map(e => e.state_social_protection_elderly_deficit_score));

  const kpis = [
    { label: "Entités Analysées", value: data?.total_entities ?? allEntities.length },
    { label: "Score Moyen", value: avgComposite.toFixed(1) },
    { label: "Index Droits Aînés", value: avgIndex.toFixed(2) },
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
          <div style={{ width: 12, height: 32, borderRadius: 9999, background: ACCENT_LIGHT }} />
          <h1 style={{ fontSize: 24, fontWeight: 700, letterSpacing: "-0.025em", margin: 0 }}>Droits Pension &amp; Personnes Âgées</h1>
        </div>
        <p style={{ color: "#94a3b8", fontSize: 13, marginLeft: 24, margin: "0 0 0 24px" }}>
          Pension &amp; Elderly Rights Engine — Caelum Partners · Chaima Mhadbi, Fondatrice, Bruxelles
        </p>
      </div>

      {/* KPI Cards */}
      <div style={{ display: "grid", gridTemplateColumns: "repeat(6, 1fr)", gap: 16 }}>
        {kpis.map(k => (
          <div key={k.label} style={{ background: "#0f172a", border: "1px solid #1e293b", borderRadius: 12, padding: 16 }}>
            <div style={{ fontSize: 11, color: "#64748b", marginBottom: 4 }}>{k.label}</div>
            <div style={{ fontSize: 20, fontWeight: 700, color: ACCENT_LIGHT }}>{k.value}</div>
          </div>
        ))}
      </div>

      {/* Gauge Rings */}
      <div style={{ background: "#0f172a", border: "1px solid #1e293b", borderRadius: 12, padding: 20 }}>
        <h2 style={{ fontSize: 13, fontWeight: 600, color: "#94a3b8", marginBottom: 16, margin: "0 0 16px 0" }}>Scores Moyens par Dimension</h2>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: 24 }}>
          <GaugeRing value={avgPension} label="Couverture Pension" />
          <GaugeRing value={avgHealthcare} label="Accès Soins Aînés" />
          <GaugeRing value={avgDiscrimination} label="Discrimination Âge" />
          <GaugeRing value={avgStateProtection} label="Déficit Protection État" />
        </div>
      </div>

      {/* Filter Pills */}
      <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
        {filters.map(f => (
          <button key={f} onClick={() => setFilter(f)}
            style={{
              padding: "6px 16px", borderRadius: 9999, fontSize: 13, fontWeight: filter === f ? 700 : 500,
              background: filter === f ? ACCENT_LIGHT : "#1e293b",
              color: filter === f ? "#030712" : "#94a3b8",
              border: "none", cursor: "pointer", transition: "all 0.2s"
            }}>
            {f.charAt(0).toUpperCase() + f.slice(1)}
          </button>
        ))}
      </div>

      {/* Entity Grid */}
      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(300px, 1fr))", gap: 16 }}>
        {filtered.map(e => {
          const riskColor = RC[e.risk_level] ?? "#94a3b8";
          return (
            <div key={e.id} onClick={() => setSelected(e)}
              style={{ border: `1px solid ${riskColor}4d`, background: `${riskColor}1a`, borderRadius: 12, padding: 16, cursor: "pointer", transition: "transform 0.15s" }}
              onMouseEnter={el => (el.currentTarget.style.transform = "scale(1.01)")}
              onMouseLeave={el => (el.currentTarget.style.transform = "scale(1)")}>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 8 }}>
                <div style={{ flex: 1, minWidth: 0 }}>
                  <div style={{ fontWeight: 600, fontSize: 13, lineHeight: 1.3, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>{e.name}</div>
                  <div style={{ fontSize: 11, color: "#94a3b8", marginTop: 4 }}>{e.country}</div>
                </div>
                <div style={{ textAlign: "right", marginLeft: 12, flexShrink: 0 }}>
                  <div style={{ fontSize: 20, fontWeight: 700, color: "white" }}>{e.composite_score.toFixed(1)}</div>
                  <div style={{ fontSize: 11, fontWeight: 700, textTransform: "uppercase", color: riskColor, marginTop: 4 }}>{e.risk_level}</div>
                </div>
              </div>
              <div style={{ height: 6, background: "#1e293b", borderRadius: 9999, overflow: "hidden", marginTop: 8 }}>
                <div style={{ height: "100%", borderRadius: 9999, background: ACCENT_LIGHT, width: `${Math.min(e.composite_score, 100)}%`, transition: "width 0.3s" }} />
              </div>
              <div style={{ fontSize: 11, color: "#64748b", marginTop: 8 }}>
                Index Droits Aînés: <span style={{ fontWeight: 500, color: ACCENT_LIGHT }}>{typeof e.estimated_pension_elderly_rights_index === "number" ? e.estimated_pension_elderly_rights_index.toFixed(2) : "—"}</span>
              </div>
            </div>
          );
        })}
      </div>

      {filtered.length === 0 && (
        <div style={{ textAlign: "center", padding: "48px 0", color: "#64748b", fontSize: 13 }}>Aucune entité pour ce niveau de risque.</div>
      )}

      {/* Sources */}
      {sources.length > 0 && (
        <div style={{ background: "#0f172a", border: "1px solid #1e293b", borderRadius: 12, padding: 16 }}>
          <h3 style={{ fontSize: 11, color: "#94a3b8", textTransform: "uppercase", letterSpacing: "0.05em", marginBottom: 12, margin: "0 0 12px 0" }}>Sources de données</h3>
          <div style={{ display: "flex", flexWrap: "wrap", gap: 8 }}>
            {sources.map((src) => (
              <span key={src} style={{ fontSize: 11, background: "#1e293b", color: "#94a3b8", padding: "4px 12px", borderRadius: 9999, border: "1px solid rgba(148,163,184,0.2)" }}>{src}</span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
