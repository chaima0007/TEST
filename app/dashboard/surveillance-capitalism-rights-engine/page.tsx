"use client";
import { useEffect, useState } from "react";

const RC: Record<string, string> = { critique: "text-red-400", "élevé": "text-orange-400", modéré: "text-yellow-400", faible: "text-emerald-400" };
const RB: Record<string, string> = { critique: "border-red-500/30 bg-red-500/10", "élevé": "border-orange-500/30 bg-orange-500/10", modéré: "border-yellow-500/30 bg-yellow-500/10", faible: "border-emerald-500/30 bg-emerald-500/10" };

const ACCENT = "#1a0533";
const ACCENT_DISPLAY = "#a855f7";

interface Entity {
  id: string;
  name: string;
  country: string;
  composite_score: number;
  estimated_surveillance_capitalism_rights_index: number;
  risk_level: string;
  primary_pattern: string;
  last_updated: string;
  [key: string]: unknown;
}

interface DashData {
  total_entities?: number;
  avg_composite?: number;
  avg_estimated_surveillance_capitalism_rights_index?: number;
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
        <circle cx="44" cy="44" r={r} fill="none" stroke="#1e293b" strokeWidth="8" />
        <circle
          cx="44" cy="44" r={r} fill="none" stroke={ACCENT_DISPLAY} strokeWidth="8"
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

const FALLBACK: Entity[] = [
  { id: "SCR-001", name: "Meta Platforms", country: "USA", composite_score: 92.3, risk_level: "critique", primary_pattern: "surveillance_comportementale_massive", estimated_surveillance_capitalism_rights_index: 9.23, last_updated: "2026-06-22" },
  { id: "SCR-002", name: "Google/Alphabet", country: "USA", composite_score: 88.3, risk_level: "critique", primary_pattern: "monetisation_donnees_personnelles", estimated_surveillance_capitalism_rights_index: 8.83, last_updated: "2026-06-22" },
  { id: "SCR-003", name: "TikTok/ByteDance", country: "Chine/USA", composite_score: 83.6, risk_level: "critique", primary_pattern: "algorithme_manipulation_psychologique", estimated_surveillance_capitalism_rights_index: 8.36, last_updated: "2026-06-22" },
  { id: "SCR-004", name: "Amazon Surveillance", country: "USA", composite_score: 75.1, risk_level: "critique", primary_pattern: "tracking_omnipresent_consommateurs", estimated_surveillance_capitalism_rights_index: 7.51, last_updated: "2026-06-22" },
  { id: "SCR-005", name: "Apple Data", country: "USA", composite_score: 56.0, risk_level: "élevé", primary_pattern: "consentement_insuffisant_publicite", estimated_surveillance_capitalism_rights_index: 5.60, last_updated: "2026-06-22" },
  { id: "SCR-006", name: "Microsoft Azure AI", country: "USA", composite_score: 52.75, risk_level: "élevé", primary_pattern: "surveillance_workplace_numérique", estimated_surveillance_capitalism_rights_index: 5.28, last_updated: "2026-06-22" },
  { id: "SCR-007", name: "Twitter/X Corp", country: "USA", composite_score: 30.3, risk_level: "modéré", primary_pattern: "données_publiques_exploitation", estimated_surveillance_capitalism_rights_index: 3.03, last_updated: "2026-06-22" },
  { id: "SCR-008", name: "Signal Foundation", country: "USA", composite_score: 9.3, risk_level: "faible", primary_pattern: "protection_données_exemplaire", estimated_surveillance_capitalism_rights_index: 0.93, last_updated: "2026-06-22" },
];

export default function SurveillanceCapitalismRightsEnginePage() {
  const [data, setData] = useState<DashData | null>(null);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState("tous");
  const [selected, setSelected] = useState<Entity | null>(null);

  useEffect(() => {
    fetch("/api/surveillance-capitalism-rights-engine")
      .then(r => r.json())
      .then(d => { setData(d.payload ?? d); setLoading(false); })
      .catch(() => { setLoading(false); });
  }, []);

  if (loading) {
    return (
      <div style={{ background: "#020617", minHeight: "100vh", display: "flex", alignItems: "center", justifyContent: "center" }}>
        <div style={{ color: ACCENT_DISPLAY, fontSize: "14px" }}>Initialisation Capitalisme de Surveillance…</div>
      </div>
    );
  }

  const allEntities: Entity[] = data?.entities ?? FALLBACK;
  const filtered = filter === "tous" ? allEntities : allEntities.filter(e => e.risk_level === filter);
  const avg = (arr: number[]) => arr.length ? arr.reduce((a, b) => a + b, 0) / arr.length : 0;
  const avgComposite = data?.avg_composite ?? avg(allEntities.map(e => e.composite_score));
  const avgIndex = data?.avg_estimated_surveillance_capitalism_rights_index ?? avg(allEntities.map(e => e.estimated_surveillance_capitalism_rights_index));
  const rd = data?.risk_distribution ?? {};
  const countCritique = rd["critique"] ?? allEntities.filter(e => e.risk_level === "critique").length;
  const countEleve = rd["élevé"] ?? allEntities.filter(e => e.risk_level === "élevé").length;
  const sources = data?.data_sources ?? [];
  const confidence = typeof data?.confidence_score === "number" ? `${(data.confidence_score * 100).toFixed(0)}%` : "—";

  const kpis = [
    { label: "Entités Analysées", value: data?.total_entities ?? allEntities.length },
    { label: "Score Moyen", value: avgComposite.toFixed(1) },
    { label: "Index Surveillance Capitalisme", value: avgIndex.toFixed(2) },
    { label: "Confiance", value: confidence },
    { label: "Critique", value: countCritique },
    { label: "Élevé", value: countEleve },
  ];

  const filters = ["tous", "critique", "élevé", "modéré", "faible"];

  return (
    <div style={{ minHeight: "100vh", background: "#020617", color: "white", padding: "24px", display: "flex", flexDirection: "column", gap: "24px" }}>
      {selected && (
        <div style={{ position: "fixed", inset: 0, zIndex: 50, display: "flex", alignItems: "center", justifyContent: "center", background: "rgba(0,0,0,0.7)", backdropFilter: "blur(4px)", padding: "16px" }}
          onClick={() => setSelected(null)}>
          <div style={{ background: "#0f172a", border: "1px solid #334155", borderRadius: "16px", width: "100%", maxWidth: "640px", maxHeight: "90vh", overflowY: "auto", boxShadow: "0 25px 50px rgba(0,0,0,0.5)" }}
            onClick={e => e.stopPropagation()}>
            <div style={{ padding: "24px", borderBottom: "1px solid #1e293b", display: "flex", justifyContent: "space-between", alignItems: "flex-start", gap: "16px" }}>
              <div>
                <h2 style={{ fontSize: "18px", fontWeight: "bold", color: "white", margin: 0 }}>{selected.name}</h2>
                <p style={{ color: "#94a3b8", fontSize: "13px", margin: "4px 0 0" }}>{selected.country}</p>
                <span style={{ fontSize: "11px", fontWeight: 600, textTransform: "uppercase" }} className={RC[selected.risk_level] ?? ""}>{selected.risk_level}</span>
              </div>
              <button onClick={() => setSelected(null)} style={{ color: "#94a3b8", background: "none", border: "none", fontSize: "24px", cursor: "pointer", lineHeight: 1 }}>&times;</button>
            </div>
            <div style={{ padding: "24px", display: "flex", flexDirection: "column", gap: "16px" }}>
              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "16px" }}>
                <div style={{ background: "rgba(30,41,59,0.5)", borderRadius: "12px", padding: "16px", textAlign: "center" }}>
                  <div style={{ fontSize: "28px", fontWeight: "bold", color: ACCENT_DISPLAY }}>{selected.composite_score.toFixed(1)}</div>
                  <div style={{ fontSize: "11px", color: "#94a3b8", marginTop: "4px" }}>Score Composite</div>
                </div>
                <div style={{ background: "rgba(30,41,59,0.5)", borderRadius: "12px", padding: "16px", textAlign: "center" }}>
                  <div style={{ fontSize: "28px", fontWeight: "bold", color: ACCENT_DISPLAY }}>{selected.estimated_surveillance_capitalism_rights_index.toFixed(2)}</div>
                  <div style={{ fontSize: "11px", color: "#94a3b8", marginTop: "4px" }}>Index Surveillance</div>
                </div>
              </div>
              <div style={{ background: "rgba(30,41,59,0.5)", borderRadius: "12px", padding: "16px" }}>
                <div style={{ fontSize: "11px", color: "#94a3b8", marginBottom: "8px" }}>Pattern Principal</div>
                <div style={{ fontSize: "14px", fontWeight: 500, color: ACCENT_DISPLAY }}>{selected.primary_pattern}</div>
              </div>
              <div style={{ fontSize: "11px", color: "#64748b" }}>
                Dernière mise à jour : {new Date(selected.last_updated).toLocaleDateString("fr-FR")}
              </div>
            </div>
          </div>
        </div>
      )}

      <div>
        <div style={{ display: "flex", alignItems: "center", gap: "12px", marginBottom: "4px" }}>
          <div style={{ width: "12px", height: "32px", borderRadius: "9999px", background: ACCENT_DISPLAY }} />
          <h1 style={{ fontSize: "22px", fontWeight: "bold", letterSpacing: "-0.025em", margin: 0 }}>Capitalisme de Surveillance &amp; Droits</h1>
        </div>
        <p style={{ color: "#94a3b8", fontSize: "13px", marginLeft: "24px" }}>
          Surveillance Capitalism Rights Engine — Caelum Partners · Wave 208
        </p>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: "16px" }}>
        {kpis.map(k => (
          <div key={k.label} style={{ background: "#0f172a", border: "1px solid #1e293b", borderRadius: "12px", padding: "16px" }}>
            <div style={{ fontSize: "11px", color: "#64748b", marginBottom: "4px" }}>{k.label}</div>
            <div style={{ fontSize: "20px", fontWeight: "bold", color: ACCENT_DISPLAY }}>{k.value}</div>
          </div>
        ))}
      </div>

      <div style={{ background: "#0f172a", border: "1px solid #1e293b", borderRadius: "12px", padding: "20px" }}>
        <h2 style={{ fontSize: "13px", fontWeight: 600, color: "#94a3b8", marginBottom: "16px" }}>Score Global — Surveillance Capitalisme</h2>
        <div style={{ display: "flex", justifyContent: "center" }}>
          <GaugeRing value={avgComposite} label="Score Composite Moyen" />
        </div>
      </div>

      <div style={{ display: "flex", gap: "8px", flexWrap: "wrap" }}>
        {filters.map(f => (
          <button key={f} onClick={() => setFilter(f)}
            style={{ padding: "6px 16px", borderRadius: "9999px", fontSize: "13px", fontWeight: filter === f ? "bold" : "normal", border: "none", cursor: "pointer", background: filter === f ? ACCENT_DISPLAY : "#1e293b", color: filter === f ? "white" : "#94a3b8", transition: "all 0.15s" }}>
            {f.charAt(0).toUpperCase() + f.slice(1)}
          </button>
        ))}
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(300px, 1fr))", gap: "16px" }}>
        {filtered.map(e => (
          <div key={e.id} onClick={() => setSelected(e)}
            style={{ border: "1px solid", borderRadius: "12px", padding: "16px", cursor: "pointer", transition: "transform 0.1s" }}
            className={RB[e.risk_level] ?? ""}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: "8px" }}>
              <div style={{ flex: 1, minWidth: 0 }}>
                <div style={{ fontWeight: 600, fontSize: "13px", lineHeight: 1.3 }}>{e.name}</div>
                <div style={{ fontSize: "11px", color: "#94a3b8", marginTop: "4px" }}>{e.country}</div>
              </div>
              <div style={{ textAlign: "right", marginLeft: "12px", flexShrink: 0 }}>
                <div style={{ fontSize: "20px", fontWeight: "bold", color: "white" }}>{e.composite_score.toFixed(1)}</div>
                <div style={{ fontSize: "10px", fontWeight: "bold", textTransform: "uppercase" }} className={RC[e.risk_level] ?? ""}>{e.risk_level}</div>
              </div>
            </div>
            <div style={{ height: "6px", background: "#1e293b", borderRadius: "9999px", overflow: "hidden", marginTop: "8px" }}>
              <div style={{ height: "100%", borderRadius: "9999px", width: `${Math.min(e.composite_score, 100)}%`, background: ACCENT_DISPLAY, transition: "all 0.3s" }} />
            </div>
            <div style={{ fontSize: "11px", color: "#64748b", marginTop: "8px" }}>
              Index: <span style={{ fontWeight: 500, color: ACCENT_DISPLAY }}>{e.estimated_surveillance_capitalism_rights_index.toFixed(2)}</span>
            </div>
            <div style={{ fontSize: "10px", color: "#475569", marginTop: "4px" }}>{e.primary_pattern}</div>
          </div>
        ))}
      </div>

      {filtered.length === 0 && (
        <div style={{ textAlign: "center", padding: "48px 0", color: "#64748b", fontSize: "13px" }}>Aucune entité pour ce niveau de risque.</div>
      )}

      {sources.length > 0 && (
        <div style={{ background: "#0f172a", border: "1px solid #1e293b", borderRadius: "12px", padding: "16px" }}>
          <h3 style={{ fontSize: "11px", color: "#94a3b8", textTransform: "uppercase", letterSpacing: "0.05em", marginBottom: "12px" }}>Sources de données</h3>
          <div style={{ display: "flex", flexWrap: "wrap", gap: "8px" }}>
            {sources.map((src) => (
              <span key={src} style={{ fontSize: "11px", background: "#1e293b", color: "#94a3b8", padding: "4px 12px", borderRadius: "9999px", border: "1px solid rgba(51,65,85,0.5)" }}>{src}</span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
