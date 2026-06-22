"use client";
import { useState, useEffect } from "react";

const ACCENT = "#ef4444";

const RC: Record<string, string> = {
  critique: "#f87171",
  "élevé": "#fb923c",
  modéré: "#facc15",
  faible: "#34d399",
};
const RB: Record<string, { border: string; bg: string }> = {
  critique: { border: "1px solid rgba(239,68,68,0.3)", bg: "rgba(239,68,68,0.08)" },
  "élevé": { border: "1px solid rgba(249,115,22,0.3)", bg: "rgba(249,115,22,0.08)" },
  modéré: { border: "1px solid rgba(234,179,8,0.3)", bg: "rgba(234,179,8,0.08)" },
  faible: { border: "1px solid rgba(52,211,153,0.3)", bg: "rgba(52,211,153,0.08)" },
};

interface Entity {
  entity_id: string;
  name: string;
  country: string;
  sector: string;
  composite_score: number;
  aid_blockade_score: number;
  humanitarian_worker_attacks_score: number;
  civilian_siege_score: number;
  medical_neutrality_violation_score: number;
  estimated_humanitarian_access_rights_index: number;
  risk_level: string;
  primary_pattern: string;
  key_signals?: string[];
  last_updated: string;
  [key: string]: unknown;
}

interface DashData {
  total_entities?: number;
  avg_composite?: number;
  avg_estimated_humanitarian_access_rights_index?: number;
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
    <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 4 }}>
      <svg viewBox="0 0 88 88" width={88} height={88}>
        <circle cx={44} cy={44} r={r} fill="none" stroke="#1e293b" strokeWidth={8} />
        <circle cx={44} cy={44} r={r} fill="none" stroke={ACCENT} strokeWidth={8}
          strokeDasharray={circ} strokeDashoffset={fill}
          strokeLinecap="round" transform="rotate(-90 44 44)" />
        <text x={44} y={49} textAnchor="middle" fill="white" fontSize={13} fontWeight="bold">
          {value.toFixed(1)}
        </text>
      </svg>
      <span style={{ fontSize: 11, color: "#94a3b8", textAlign: "center", maxWidth: 80 }}>{label}</span>
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
    { label: "Blocus de l'Aide", value: entity.aid_blockade_score, weight: "0.30" },
    { label: "Attaques Travailleurs Humanitaires", value: entity.humanitarian_worker_attacks_score, weight: "0.25" },
    { label: "Siège Civil", value: entity.civilian_siege_score, weight: "0.25" },
    { label: "Violations Neutralité Médicale", value: entity.medical_neutrality_violation_score, weight: "0.20" },
  ];
  const color = RC[entity.risk_level] ?? "#94a3b8";
  const rb = RB[entity.risk_level] ?? { border: "1px solid #334155", bg: "rgba(51,65,85,0.3)" };

  return (
    <div
      style={{ position: "fixed", inset: 0, zIndex: 50, display: "flex", alignItems: "center", justifyContent: "center", background: "rgba(0,0,0,0.7)", backdropFilter: "blur(4px)", padding: 16 }}
      onClick={onClose}
    >
      <div
        style={{ background: "#0f172a", border: "1px solid #334155", borderRadius: 16, width: "100%", maxWidth: 640, maxHeight: "90vh", overflowY: "auto", boxShadow: "0 25px 50px rgba(0,0,0,0.5)" }}
        onClick={(e) => e.stopPropagation()}
      >
        <div style={{ padding: "24px 24px 20px", borderBottom: "1px solid #1e293b", display: "flex", alignItems: "flex-start", justifyContent: "space-between", gap: 16 }}>
          <div>
            <h2 style={{ fontSize: 18, fontWeight: 700, color: "#f8fafc", marginBottom: 4 }}>{entity.name}</h2>
            <p style={{ fontSize: 13, color: "#94a3b8" }}>{entity.country}</p>
            <span style={{ fontSize: 11, fontWeight: 700, textTransform: "uppercase", color }}>{entity.risk_level}</span>
          </div>
          <button onClick={onClose} style={{ color: "#94a3b8", fontSize: 24, lineHeight: 1, background: "none", border: "none", cursor: "pointer" }}>&times;</button>
        </div>
        <div style={{ display: "flex", borderBottom: "1px solid #1e293b" }}>
          {tabs.map((t) => (
            <button key={t.key} onClick={() => setTab(t.key)}
              style={{ flex: 1, padding: "12px 0", fontSize: 13, fontWeight: 500, background: "none", border: "none", cursor: "pointer", borderBottom: tab === t.key ? `2px solid ${ACCENT}` : "2px solid transparent", color: tab === t.key ? ACCENT : "#64748b" }}>
              {t.label}
            </button>
          ))}
        </div>
        <div style={{ padding: 24 }}>
          {tab === "apercu" && (
            <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12 }}>
                <div style={{ background: "rgba(255,255,255,0.04)", borderRadius: 12, padding: 16, textAlign: "center" }}>
                  <div style={{ fontSize: 28, fontWeight: 700, color: ACCENT }}>{entity.composite_score.toFixed(1)}</div>
                  <div style={{ fontSize: 11, color: "#64748b", marginTop: 4 }}>Score Composite</div>
                </div>
                <div style={{ background: "rgba(255,255,255,0.04)", borderRadius: 12, padding: 16, textAlign: "center" }}>
                  <div style={{ fontSize: 28, fontWeight: 700, color: ACCENT }}>{typeof entity.estimated_humanitarian_access_rights_index === "number" ? entity.estimated_humanitarian_access_rights_index.toFixed(2) : "—"}</div>
                  <div style={{ fontSize: 11, color: "#64748b", marginTop: 4 }}>Index Accès Humanitaire</div>
                </div>
              </div>
              <div style={{ borderRadius: 8, padding: 12, border: rb.border, background: rb.bg }}>
                <span style={{ fontSize: 13, fontWeight: 600, color }}>{entity.risk_level.charAt(0).toUpperCase() + entity.risk_level.slice(1)}</span>
              </div>
              <div style={{ background: "rgba(255,255,255,0.04)", borderRadius: 12, padding: 16 }}>
                <div style={{ fontSize: 11, color: "#64748b", marginBottom: 6 }}>Pattern Principal</div>
                <div style={{ fontSize: 13, fontWeight: 600, color: ACCENT }}>{entity.primary_pattern}</div>
              </div>
              <div style={{ background: "rgba(255,255,255,0.04)", borderRadius: 12, padding: 16 }}>
                <div style={{ fontSize: 11, color: "#64748b", marginBottom: 6 }}>Secteur / Contexte</div>
                <div style={{ fontSize: 12, color: "#cbd5e1", lineHeight: 1.6 }}>{entity.sector}</div>
              </div>
            </div>
          )}
          {tab === "metriques" && (
            <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
              {subScores.map((s) => (
                <div key={s.label} style={{ background: "rgba(255,255,255,0.04)", borderRadius: 10, padding: 12 }}>
                  <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 6 }}>
                    <span style={{ fontSize: 13, color: "#cbd5e1" }}>{s.label}</span>
                    <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
                      <span style={{ fontSize: 11, color: "#64748b" }}>×{s.weight}</span>
                      <span style={{ fontSize: 14, fontWeight: 700, color: "#f8fafc" }}>{typeof s.value === "number" ? s.value.toFixed(1) : "—"}</span>
                    </div>
                  </div>
                  <div style={{ height: 6, background: "#1e293b", borderRadius: 3, overflow: "hidden" }}>
                    <div style={{ height: "100%", borderRadius: 3, background: ACCENT, width: `${Math.min(typeof s.value === "number" ? s.value : 0, 100)}%` }} />
                  </div>
                </div>
              ))}
            </div>
          )}
          {tab === "sources" && (
            <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
              <div style={{ background: "rgba(255,255,255,0.04)", borderRadius: 12, padding: 16 }}>
                <div style={{ fontSize: 11, color: "#64748b", marginBottom: 10 }}>Signaux Clés Détectés</div>
                <ul style={{ listStyle: "none", padding: 0, margin: 0, display: "flex", flexDirection: "column", gap: 8 }}>
                  {(entity.key_signals ?? []).map((sig, i) => (
                    <li key={i} style={{ display: "flex", alignItems: "flex-start", gap: 8, fontSize: 12, color: "#94a3b8", lineHeight: 1.6 }}>
                      <span style={{ width: 6, height: 6, borderRadius: "50%", background: ACCENT, flexShrink: 0, marginTop: 5 }} />
                      {sig}
                    </li>
                  ))}
                </ul>
              </div>
              <div style={{ fontSize: 11, color: "#475569" }}>
                Dernière mise à jour : {new Date(entity.last_updated).toLocaleDateString("fr-FR")}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default function HumanitarianAccessRightsEnginePage() {
  const [data, setData] = useState<DashData | null>(null);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState("tous");
  const [selected, setSelected] = useState<Entity | null>(null);

  useEffect(() => {
    fetch("/api/humanitarian-access-rights-engine")
      .then(r => r.json())
      .then(d => { setData(d.payload ?? d); setLoading(false); })
      .catch(() => { setLoading(false); });
  }, []);

  if (loading) {
    return (
      <div style={{ background: "#020617", minHeight: "100vh", display: "flex", alignItems: "center", justifyContent: "center" }}>
        <div style={{ color: ACCENT, fontSize: 14 }}>Initialisation Accès Humanitaire &amp; Droits en Zone de Conflit…</div>
      </div>
    );
  }

  const allEntities: Entity[] = data?.entities ?? [];
  const filtered = filter === "tous" ? allEntities : allEntities.filter(e => e.risk_level === filter);
  const avg = (arr: number[]) => arr.length ? arr.reduce((a, b) => a + b, 0) / arr.length : 0;
  const avgComposite = data?.avg_composite ?? avg(allEntities.map(e => e.composite_score));
  const avgIndex = data?.avg_estimated_humanitarian_access_rights_index ?? avg(allEntities.map(e => e.estimated_humanitarian_access_rights_index));
  const rd = data?.risk_distribution ?? {};
  const countCritique = rd["critique"] ?? allEntities.filter(e => e.risk_level === "critique").length;
  const countEleve = rd["élevé"] ?? allEntities.filter(e => e.risk_level === "élevé").length;
  const sources = data?.data_sources ?? [];
  const confidence = typeof data?.confidence_score === "number" ? `${(data.confidence_score * 100).toFixed(0)}%` : "—";

  const avgAidBlockade = avg(allEntities.map(e => e.aid_blockade_score));
  const avgWorkerAttacks = avg(allEntities.map(e => e.humanitarian_worker_attacks_score));
  const avgCivilianSiege = avg(allEntities.map(e => e.civilian_siege_score));
  const avgMedicalNeutrality = avg(allEntities.map(e => e.medical_neutrality_violation_score));

  const kpis = [
    { label: "Entités Analysées", value: data?.total_entities ?? allEntities.length },
    { label: "Score Moyen", value: avgComposite.toFixed(1) },
    { label: "Index Accès Humanitaire", value: avgIndex.toFixed(2) },
    { label: "Confiance", value: confidence },
    { label: "Critique", value: countCritique },
    { label: "Élevé", value: countEleve },
  ];

  const filters = ["tous", "critique", "élevé", "modéré", "faible"];

  return (
    <div style={{ minHeight: "100vh", background: "#020617", color: "#f8fafc", padding: 24, display: "flex", flexDirection: "column", gap: 24 }}>
      {selected && <DetailModal entity={selected} onClose={() => setSelected(null)} />}

      <div>
        <div style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 4 }}>
          <div style={{ width: 4, height: 32, borderRadius: 4, background: ACCENT }} />
          <h1 style={{ fontSize: 22, fontWeight: 700, letterSpacing: "-0.5px" }}>Accès Humanitaire &amp; Droits en Zone de Conflit</h1>
        </div>
        <p style={{ fontSize: 13, color: "#64748b", marginLeft: 16 }}>
          Humanitarian Access Rights Engine — Caelum Partners · Chaima Mhadbi, Fondatrice, Bruxelles
        </p>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(140px, 1fr))", gap: 12 }}>
        {kpis.map(k => (
          <div key={k.label} style={{ background: "#0f172a", border: "1px solid #1e293b", borderRadius: 12, padding: 16 }}>
            <div style={{ fontSize: 11, color: "#64748b", marginBottom: 4 }}>{k.label}</div>
            <div style={{ fontSize: 20, fontWeight: 700, color: ACCENT }}>{k.value}</div>
          </div>
        ))}
      </div>

      <div style={{ background: "#0f172a", border: "1px solid #1e293b", borderRadius: 12, padding: 20 }}>
        <h2 style={{ fontSize: 13, fontWeight: 600, color: "#94a3b8", marginBottom: 16 }}>Scores Moyens par Dimension</h2>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(100px, 1fr))", gap: 24 }}>
          <GaugeRing value={avgAidBlockade} label="Blocus de l'Aide" />
          <GaugeRing value={avgWorkerAttacks} label="Attaques Humanitaires" />
          <GaugeRing value={avgCivilianSiege} label="Siège Civil" />
          <GaugeRing value={avgMedicalNeutrality} label="Neutralité Médicale" />
        </div>
      </div>

      <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
        {filters.map(f => (
          <button key={f} onClick={() => setFilter(f)}
            style={{ padding: "6px 16px", borderRadius: 20, fontSize: 13, fontWeight: 500, cursor: "pointer", border: "none", background: filter === f ? ACCENT : "#1e293b", color: filter === f ? "#fff" : "#94a3b8" }}>
            {f.charAt(0).toUpperCase() + f.slice(1)}
          </button>
        ))}
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(300px, 1fr))", gap: 16 }}>
        {filtered.map(e => {
          const rb = RB[e.risk_level] ?? { border: "1px solid #334155", bg: "rgba(51,65,85,0.3)" };
          const color = RC[e.risk_level] ?? "#94a3b8";
          return (
            <div key={e.entity_id} onClick={() => setSelected(e)}
              style={{ border: rb.border, background: rb.bg, borderRadius: 12, padding: 16, cursor: "pointer", transition: "transform 0.15s" }}
              onMouseEnter={el => (el.currentTarget.style.transform = "scale(1.01)")}
              onMouseLeave={el => (el.currentTarget.style.transform = "scale(1)")}>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 8 }}>
                <div style={{ flex: 1, minWidth: 0 }}>
                  <div style={{ fontWeight: 600, fontSize: 13, lineHeight: 1.4, marginBottom: 4 }}>{e.name}</div>
                  <div style={{ fontSize: 11, color: "#94a3b8" }}>{e.country}</div>
                </div>
                <div style={{ textAlign: "right", marginLeft: 12, flexShrink: 0 }}>
                  <div style={{ fontSize: 20, fontWeight: 700, color: "#f8fafc" }}>{e.composite_score.toFixed(1)}</div>
                  <div style={{ fontSize: 10, fontWeight: 700, textTransform: "uppercase", color }}>{e.risk_level}</div>
                </div>
              </div>
              <div style={{ height: 4, background: "#1e293b", borderRadius: 2, overflow: "hidden", marginBottom: 8 }}>
                <div style={{ height: "100%", borderRadius: 2, background: ACCENT, width: `${Math.min(e.composite_score, 100)}%` }} />
              </div>
              <div style={{ fontSize: 11, color: "#64748b" }}>
                Index: <span style={{ fontWeight: 600, color: ACCENT }}>{typeof e.estimated_humanitarian_access_rights_index === "number" ? e.estimated_humanitarian_access_rights_index.toFixed(2) : "—"}</span>
              </div>
            </div>
          );
        })}
      </div>

      {filtered.length === 0 && (
        <div style={{ textAlign: "center", padding: "48px 0", color: "#475569", fontSize: 14 }}>Aucune entité pour ce niveau de risque.</div>
      )}

      {sources.length > 0 && (
        <div style={{ background: "#0f172a", border: "1px solid #1e293b", borderRadius: 12, padding: 16 }}>
          <h3 style={{ fontSize: 11, textTransform: "uppercase", letterSpacing: "0.08em", color: "#64748b", marginBottom: 12 }}>Sources de données</h3>
          <div style={{ display: "flex", flexWrap: "wrap", gap: 8 }}>
            {sources.map((src) => (
              <span key={src} style={{ fontSize: 11, background: "#1e293b", color: "#94a3b8", padding: "4px 12px", borderRadius: 20, border: "1px solid rgba(51,65,85,0.5)" }}>{src}</span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
