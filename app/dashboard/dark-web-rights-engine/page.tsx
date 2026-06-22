"use client";
import { useState, useEffect } from "react";

const RC: Record<string, string> = { critique: "#ef4444", "élevé": "#f97316", modéré: "#eab308", faible: "#22c55e" };

const ACCENT = "#0a0a1a";
const ACCENT_LIGHT = "#818cf8";

interface Entity {
  id: string;
  name: string;
  country: string;
  composite_score: number;
  state_sponsored_cyber_rights_violations_score: number;
  dark_web_criminal_exploitation_score: number;
  digital_privacy_anonymity_rights_score: number;
  law_enforcement_accountability_deficit_score: number;
  estimated_dark_web_rights_index: number;
  risk_level: string;
  primary_pattern: string;
  last_updated: string;
  [key: string]: unknown;
}

interface DashData {
  total_entities?: number;
  avg_composite?: number;
  avg_estimated_dark_web_rights_index?: number;
  risk_distribution?: Record<string, number>;
  confidence_score?: number;
  data_sources?: string[];
  entities?: Entity[];
  [key: string]: unknown;
}

const FALLBACK_ENTITIES: Entity[] = [
  {
    id: "DWR-001",
    name: "North Korea Lazarus Group — Cyberattaques étatiques, droits numériques violés",
    country: "North Korea",
    state_sponsored_cyber_rights_violations_score: 95.0,
    dark_web_criminal_exploitation_score: 90.0,
    digital_privacy_anonymity_rights_score: 94.0,
    law_enforcement_accountability_deficit_score: 92.0,
    composite_score: 92.80,
    risk_level: "critique",
    primary_pattern: "Lazarus Group vole 3Mrd$ crypto, finance armes nucléaires, viole droits numériques globaux",
    estimated_dark_web_rights_index: 9.28,
    last_updated: "2026-06-22",
  },
  {
    id: "DWR-002",
    name: "Russia APT Groups — Désinformation, cyberespionnage, violations droits",
    country: "Russia",
    state_sponsored_cyber_rights_violations_score: 91.0,
    dark_web_criminal_exploitation_score: 88.0,
    digital_privacy_anonymity_rights_score: 89.0,
    law_enforcement_accountability_deficit_score: 89.0,
    composite_score: 89.10,
    risk_level: "critique",
    primary_pattern: "APT28/29 ciblent journalistes, Killnet attaque infrastr. civiles, RuTor marché dark web",
    estimated_dark_web_rights_index: 8.91,
    last_updated: "2026-06-22",
  },
  {
    id: "DWR-003",
    name: "China MSS APT41 — Surveillance citoyens, droits numériques bafoués",
    country: "China",
    state_sponsored_cyber_rights_violations_score: 88.0,
    dark_web_criminal_exploitation_score: 84.0,
    digital_privacy_anonymity_rights_score: 87.0,
    law_enforcement_accountability_deficit_score: 87.0,
    composite_score: 86.65,
    risk_level: "critique",
    primary_pattern: "Great Firewall, MSS surveillance diaspora, APT41 espionnage industriel et dissidents",
    estimated_dark_web_rights_index: 8.67,
    last_updated: "2026-06-22",
  },
  {
    id: "DWR-004",
    name: "Iran IRGC Cyber — Répression numérique opposants",
    country: "Iran",
    state_sponsored_cyber_rights_violations_score: 83.0,
    dark_web_criminal_exploitation_score: 80.0,
    digital_privacy_anonymity_rights_score: 82.0,
    law_enforcement_accountability_deficit_score: 81.0,
    composite_score: 81.60,
    risk_level: "critique",
    primary_pattern: "IRGC traque opposants via dark web, Charming Kitten cible activistes, internet coupé",
    estimated_dark_web_rights_index: 8.16,
    last_updated: "2026-06-22",
  },
  {
    id: "DWR-005",
    name: "Criminal Marketplaces Dark Web — Trafic humains, drogues, armes",
    country: "Global",
    state_sponsored_cyber_rights_violations_score: 50.0,
    dark_web_criminal_exploitation_score: 62.0,
    digital_privacy_anonymity_rights_score: 55.0,
    law_enforcement_accountability_deficit_score: 52.0,
    composite_score: 54.65,
    risk_level: "élevé",
    primary_pattern: "Hydra/Alphabay trafic drogues, CSAM vendu crypto, passeports falsifiés, identités volées",
    estimated_dark_web_rights_index: 5.47,
    last_updated: "2026-06-22",
  },
  {
    id: "DWR-006",
    name: "Dark Web CSAM Networks — Exploitation enfants en ligne",
    country: "Global",
    state_sponsored_cyber_rights_violations_score: 45.0,
    dark_web_criminal_exploitation_score: 68.0,
    digital_privacy_anonymity_rights_score: 53.0,
    law_enforcement_accountability_deficit_score: 52.0,
    composite_score: 54.15,
    risk_level: "élevé",
    primary_pattern: "Réseaux CSAM cryptés, 400K images/vidéos/jour identifiées IWF, victimes non protégées",
    estimated_dark_web_rights_index: 5.42,
    last_updated: "2026-06-22",
  },
  {
    id: "DWR-007",
    name: "EU Authorities Europol — Lutte dark web, lacunes droits numériques",
    country: "European Union",
    state_sponsored_cyber_rights_violations_score: 25.0,
    dark_web_criminal_exploitation_score: 28.0,
    digital_privacy_anonymity_rights_score: 30.0,
    law_enforcement_accountability_deficit_score: 28.0,
    composite_score: 27.75,
    risk_level: "modéré",
    primary_pattern: "Europol démantèle marchés mais RGPD vs surveillance débat, lacunes juridiques cross-border",
    estimated_dark_web_rights_index: 2.78,
    last_updated: "2026-06-22",
  },
  {
    id: "DWR-008",
    name: "Tor Project — Anonymat légitime, protection lanceurs d&apos;alerte",
    country: "Global",
    state_sponsored_cyber_rights_violations_score: 7.0,
    dark_web_criminal_exploitation_score: 9.0,
    digital_privacy_anonymity_rights_score: 8.0,
    law_enforcement_accountability_deficit_score: 8.0,
    composite_score: 8.00,
    risk_level: "faible",
    primary_pattern: "Tor protège journalistes, lanceurs alerte, dissidents — usage légitime droits humains",
    estimated_dark_web_rights_index: 0.80,
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
    { label: "Violations Cyber Droits Étatiques", value: entity.state_sponsored_cyber_rights_violations_score, weight: "0.30" },
    { label: "Exploitation Criminelle Dark Web", value: entity.dark_web_criminal_exploitation_score, weight: "0.25" },
    { label: "Droits Vie Privée & Anonymat Numérique", value: entity.digital_privacy_anonymity_rights_score, weight: "0.25" },
    { label: "Déficit Responsabilité Forces de l&apos;Ordre", value: entity.law_enforcement_accountability_deficit_score, weight: "0.20" },
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
                    {typeof entity.estimated_dark_web_rights_index === "number" ? entity.estimated_dark_web_rights_index.toFixed(2) : "—"}
                  </div>
                  <div style={{ fontSize: 11, color: "#94a3b8", marginTop: 4 }}>Index Droits Web Sombre</div>
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

export default function DarkWebRightsEnginePage() {
  const [data, setData] = useState<DashData | null>(null);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState("tous");
  const [selected, setSelected] = useState<Entity | null>(null);

  useEffect(() => {
    fetch("/api/dark-web-rights-engine")
      .then(r => r.json())
      .then(d => { setData(d.payload ?? d); setLoading(false); })
      .catch(() => { setLoading(false); });
  }, []);

  if (loading) {
    return (
      <div style={{ background: "#030712", minHeight: "100vh", display: "flex", alignItems: "center", justifyContent: "center" }}>
        <div style={{ color: ACCENT_LIGHT, fontSize: 13, animation: "pulse 2s infinite" }}>Initialisation Droits &amp; Dark Web…</div>
      </div>
    );
  }

  const allEntities: Entity[] = data?.entities ?? FALLBACK_ENTITIES;
  const filtered = filter === "tous" ? allEntities : allEntities.filter(e => e.risk_level === filter);
  const avg = (arr: number[]) => arr.length ? arr.reduce((a, b) => a + b, 0) / arr.length : 0;
  const avgComposite = data?.avg_composite ?? avg(allEntities.map(e => e.composite_score));
  const avgIndex = data?.avg_estimated_dark_web_rights_index ?? avg(allEntities.map(e => e.estimated_dark_web_rights_index));
  const rd = data?.risk_distribution ?? {};
  const countCritique = rd["critique"] ?? allEntities.filter(e => e.risk_level === "critique").length;
  const countEleve = rd["élevé"] ?? allEntities.filter(e => e.risk_level === "élevé").length;
  const sources = data?.data_sources ?? [];
  const confidence = typeof data?.confidence_score === "number" ? `${(data.confidence_score * 100).toFixed(0)}%` : "—";

  const avgStateSponsored = avg(allEntities.map(e => e.state_sponsored_cyber_rights_violations_score));
  const avgCriminal = avg(allEntities.map(e => e.dark_web_criminal_exploitation_score));
  const avgPrivacy = avg(allEntities.map(e => e.digital_privacy_anonymity_rights_score));
  const avgLawEnforcement = avg(allEntities.map(e => e.law_enforcement_accountability_deficit_score));

  const kpis = [
    { label: "Entités Analysées", value: data?.total_entities ?? allEntities.length },
    { label: "Score Moyen", value: avgComposite.toFixed(1) },
    { label: "Index Droits Web Sombre", value: avgIndex.toFixed(2) },
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
          <h1 style={{ fontSize: 24, fontWeight: 700, letterSpacing: "-0.025em", margin: 0 }}>Droits &amp; Dark Web</h1>
        </div>
        <p style={{ color: "#94a3b8", fontSize: 13, marginLeft: 24, margin: "0 0 0 24px" }}>
          Dark Web Rights Engine — Caelum Partners · Chaima Mhadbi, Fondatrice, Bruxelles
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
          <GaugeRing value={avgStateSponsored} label="Cyber Étatique" />
          <GaugeRing value={avgCriminal} label="Exploitation Criminelle" />
          <GaugeRing value={avgPrivacy} label="Vie Privée Numérique" />
          <GaugeRing value={avgLawEnforcement} label="Déficit Responsabilité" />
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
                Index Web Sombre: <span style={{ fontWeight: 500, color: ACCENT_LIGHT }}>{typeof e.estimated_dark_web_rights_index === "number" ? e.estimated_dark_web_rights_index.toFixed(2) : "—"}</span>
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
