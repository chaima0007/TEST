"use client";
import { useEffect, useState } from "react";

// Housing Crisis & Accessibilité Immobilière — Caelum Partners

type RiskLevel = "critique" | "élevé" | "modéré" | "faible";

interface HCEEntity {
  entity_id: string;
  market_type: string;
  region: string;
  affordability_score: number;
  speculation_score: number;
  supply_score: number;
  homelessness_score: number;
  composite_score: number;
  risk_level: RiskLevel;
  housing_pattern: string;
  severity: string;
  recommended_action: string;
  signal: string;
  price_to_income_ratio: number;
  rent_burden_rate: number;
}

interface HCESummary {
  module_id: number;
  module_name: string;
  total: number;
  critical: number;
  high: number;
  moderate: number;
  low: number;
  avg_composite: number;
  pattern_distribution: Record<string, number>;
  risk_distribution: Record<string, number>;
  severity_distribution: Record<string, number>;
  action_distribution: Record<string, number>;
  avg_estimated_housing_affordability_index: number;
}

const ACCENT = "#f43f5e";

const RISK_META: Record<RiskLevel, { label: string; badge: string; color: string }> = {
  critique: { label: "Critique", badge: "bg-red-900/60 text-red-300 border border-red-700",         color: "#ef4444" },
  élevé:    { label: "Élevé",    badge: "bg-orange-900/60 text-orange-300 border border-orange-700", color: "#f97316" },
  modéré:   { label: "Modéré",   badge: "bg-amber-900/60 text-amber-300 border border-amber-700",   color: "#f59e0b" },
  faible:   { label: "Faible",   badge: "bg-emerald-900/60 text-emerald-300 border border-emerald-700", color: "#10b981" },
};

const RISK_COLORS: Record<string, string> = {
  critique: "#ef4444", élevé: "#f97316", modéré: "#f59e0b", faible: "#10b981",
};

const PAT_COLORS: Record<string, string> = {
  none:                              "#10b981",
  homelessness_crisis_explosion:     "#ef4444",
  financialization_speculation_trap: "#a855f7",
  rental_market_collapse:            "#f97316",
  displacement_gentrification:       "#3b82f6",
  social_housing_defunding:          "#f59e0b",
};

const SEV_COLORS: Record<string, string> = {
  "marché_logement_sous_surveillance":       "#10b981",
  "tension_marché_immobilier_structurelle":  "#f59e0b",
  "crise_accessibilité_immobilière_majeure": "#f97316",
  "crise_logement_systémique_critique":      "#ef4444",
};

const ACT_COLORS: Record<string, string> = {
  "veille_marché_logement_continue":                   "#10b981",
  "renforcement_politiques_accessibilité_logement":    "#f59e0b",
  "régulation_marché_immobilier_accélérée":            "#f97316",
  "intervention_urgente_crise_logement_systémique":    "#ef4444",
};

function GaugeRing({ value, label, color }: { value: number; label: string; color: string }) {
  const r = 36;
  const circ = 2 * Math.PI * r;
  const fill = circ * (1 - value / 100);
  return (
    <div className="flex flex-col items-center gap-1">
      <svg width="88" height="88" viewBox="0 0 88 88">
        <circle cx="44" cy="44" r={r} fill="none" stroke="#0f172a" strokeWidth="8" />
        <circle cx="44" cy="44" r={r} fill="none" stroke={color} strokeWidth="8"
          strokeDasharray={circ} strokeDashoffset={fill}
          strokeLinecap="round" transform="rotate(-90 44 44)" />
        <text x="44" y="49" textAnchor="middle" fill="white" fontSize="13" fontWeight="bold">
          {Math.round(value)}
        </text>
      </svg>
      <span className="text-xs text-rose-400/70 text-center leading-tight">{label}</span>
    </div>
  );
}

function DistBar({ title, counts, colors }: { title: string; counts: Record<string, number>; colors: Record<string, string> }) {
  const total = Object.values(counts).reduce((a, b) => a + b, 0) || 1;
  return (
    <div className="flex flex-col gap-1">
      <span className="text-xs text-rose-400/70 font-medium">{title}</span>
      <div className="flex h-3 rounded overflow-hidden gap-px">
        {Object.entries(counts).map(([k, v]) => (
          <div key={k} style={{ width: `${v / total * 100}%`, background: colors[k] || "#881337" }} title={`${k}: ${v}`} />
        ))}
      </div>
      <div className="flex flex-wrap gap-x-3 gap-y-0.5">
        {Object.entries(counts).map(([k, v]) => (
          <span key={k} className="text-xs text-rose-400/60">
            <span style={{ color: colors[k] || "#f43f5e" }}>■</span> {k.replace(/_/g, " ")} {v}
          </span>
        ))}
      </div>
    </div>
  );
}

function DetailModal({ entity, onClose }: { entity: HCEEntity; onClose: () => void }) {
  const [tab, setTab] = useState<"scores" | "signaux" | "actions">("scores");
  const meta = RISK_META[entity.risk_level];

  useEffect(() => {
    const h = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", h);
    return () => window.removeEventListener("keydown", h);
  }, [onClose]);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/75" onClick={onClose}>
      <div className="bg-slate-900 border border-rose-700/30 rounded-xl w-full max-w-lg p-6 shadow-2xl" onClick={e => e.stopPropagation()}>
        <div className="flex items-center justify-between mb-4">
          <div>
            <span className="text-lg font-bold text-white">{entity.entity_id}</span>
            <span className="ml-2 text-rose-400 text-xs">{entity.region}</span>
            <span className="ml-2 text-slate-400 text-xs">{entity.market_type.replace(/_/g, " ")}</span>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl leading-none">✕</button>
        </div>

        <div className="flex gap-2 mb-4">
          {(["scores", "signaux", "actions"] as const).map(t => (
            <button key={t} onClick={() => setTab(t)}
              className={`px-3 py-1 rounded text-xs font-medium transition-colors ${tab === t ? "bg-rose-800 text-white" : "bg-slate-800 text-slate-400 hover:text-white"}`}>
              {t === "scores" ? "Scores" : t === "signaux" ? "Signaux" : "Actions"}
            </button>
          ))}
        </div>

        {tab === "scores" && (
          <div className="grid grid-cols-2 gap-3 text-sm">
            {([
              ["Accessibilité",  entity.affordability_score,  "#f43f5e"],
              ["Spéculation",    entity.speculation_score,    "#a855f7"],
              ["Offre",          entity.supply_score,         "#10b981"],
              ["Sans-Abrisme",   entity.homelessness_score,   "#ef4444"],
            ] as [string, number, string][]).map(([l, v, c]) => (
              <div key={l} className="bg-slate-800 border border-rose-700/20 rounded-lg p-3">
                <div className="text-slate-400 text-xs mb-1">{l}</div>
                <div className="text-white font-bold text-lg">{v.toFixed(1)}</div>
                <div className="h-1.5 rounded mt-1 bg-slate-700">
                  <div className="h-1.5 rounded" style={{ width: `${Math.min(v, 100)}%`, background: c }} />
                </div>
              </div>
            ))}
            <div className="col-span-2 bg-slate-800 border border-rose-700/20 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Score Composite</div>
              <div className="text-white font-bold text-2xl">{entity.composite_score.toFixed(1)}</div>
            </div>
          </div>
        )}

        {tab === "signaux" && (
          <div className="bg-slate-800 border border-rose-700/20 rounded-lg p-4 text-sm text-slate-200 leading-relaxed">
            {entity.signal}
            <div className="mt-3 flex gap-2 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${meta?.badge || "bg-slate-700 text-slate-300"}`}>
                {meta?.label || entity.risk_level}
              </span>
              <span className="px-2 py-0.5 rounded text-xs font-medium bg-slate-700 text-rose-300">
                {entity.severity.replace(/_/g, " ")}
              </span>
            </div>
            <div className="mt-3 grid grid-cols-2 gap-2 text-xs text-slate-400">
              <div>Ratio Prix/Revenu: <span className="text-rose-300">{Math.round(entity.price_to_income_ratio * 100)}%</span></div>
              <div>Charge Locative: <span className="text-rose-300">{Math.round(entity.rent_burden_rate * 100)}%</span></div>
            </div>
          </div>
        )}

        {tab === "actions" && (
          <div className="space-y-3 text-sm">
            <div className="bg-slate-800 border border-rose-700/20 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Niveau de Risque</div>
              <div className={`inline-block px-2 py-0.5 rounded text-xs font-medium ${meta?.badge || "bg-slate-700 text-slate-300"}`}>
                {meta?.label || entity.risk_level}
              </div>
            </div>
            <div className="bg-slate-800 border border-rose-700/20 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Action Recommandée</div>
              <div className="text-white font-medium">{entity.recommended_action.replace(/_/g, " ")}</div>
            </div>
            <div className="bg-slate-800 border border-rose-700/20 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Patron Détecté</div>
              <div className="font-medium capitalize" style={{ color: ACCENT }}>{entity.housing_pattern.replace(/_/g, " ")}</div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function HousingCrisisDashboard() {
  const [data, setData] = useState<{
    entities: HCEEntity[];
    summary: HCESummary;
    avg_affordability: number;
  } | null>(null);
  const [riskFilter, setRisk] = useState<string>("tous");
  const [patFilter, setPat] = useState<string>("tous");
  const [selected, setSelected] = useState<HCEEntity | null>(null);

  useEffect(() => {
    fetch("/api/housing-crisis-engine")
      .then(r => r.json())
      .then(setData)
      .catch(console.error);
  }, []);

  if (!data) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="animate-pulse" style={{ color: ACCENT }}>Initialisation Moteur Crise Logement — Caelum Partners...</div>
    </div>
  );

  const { entities, summary } = data;
  const filtered = entities.filter(e =>
    (riskFilter === "tous" || e.risk_level === riskFilter) &&
    (patFilter === "tous" || e.housing_pattern === patFilter)
  );

  const n = entities.length || 1;
  const avgAff  = entities.reduce((s, e) => s + e.affordability_score, 0) / n;
  const avgSpe  = entities.reduce((s, e) => s + e.speculation_score,  0) / n;
  const avgSup  = entities.reduce((s, e) => s + e.supply_score,        0) / n;
  const avgHom  = entities.reduce((s, e) => s + e.homelessness_score,  0) / n;

  const critCount = summary.risk_distribution["critique"] || 0;
  const elevCount = summary.risk_distribution["élevé"]    || 0;

  const dists = [
    { title: "Niveau de Risque",  counts: summary.risk_distribution,     colors: RISK_COLORS },
    { title: "Patron Logement",   counts: summary.pattern_distribution,  colors: PAT_COLORS  },
    { title: "Sévérité",          counts: summary.severity_distribution, colors: SEV_COLORS  },
    { title: "Action Déclenchée", counts: summary.action_distribution,   colors: ACT_COLORS  },
  ] as Array<{ title: string; counts: Record<string, number>; colors: Record<string, string> }>;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-300 p-6 space-y-6">
      {selected && <DetailModal entity={selected} onClose={() => setSelected(null)} />}

      <div>
        <h1 className="text-2xl font-bold" style={{ color: ACCENT }}>
          Crise Logement &amp; Accessibilité Immobilière
        </h1>
        <p className="text-slate-400 text-sm mt-1">
          Accessibilité · Spéculation · Offre · Sans-Abrisme — Caelum Partners
        </p>
        <p className="text-slate-500 text-xs mt-0.5">Chaima Mhadbi — Bruxelles</p>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {([
          ["Total Marchés",     summary.total,                                                      "text-slate-300"],
          ["Critique",          critCount,                                                           "text-red-400"],
          ["Élevé",             elevCount,                                                           "text-orange-400"],
          ["Composite Moyen",   summary.avg_composite.toFixed(1),                                   "text-rose-300"],
          ["Index Accessib.",   summary.avg_estimated_housing_affordability_index.toFixed(2) + "/10","text-rose-400"],
          ["Modérés + Faibles", (summary.moderate + summary.low),                                   "text-emerald-400"],
        ] as [string, string | number, string][]).map(([l, v, c]) => (
          <div key={String(l)} className="bg-slate-900 border border-rose-800/30 rounded-xl p-3 text-center">
            <div className={`text-xl font-bold ${c}`}>{v}</div>
            <div className="text-xs text-slate-500 mt-0.5 leading-tight">{l}</div>
          </div>
        ))}
      </div>

      <div className="bg-slate-900 border border-rose-800/30 rounded-xl p-5">
        <p className="text-xs text-slate-500 mb-4 font-medium">Scores Moyens par Dimension</p>
        <div className="grid grid-cols-4 gap-4">
          <GaugeRing value={avgAff} label="Accessibilité (×0.30)" color="#f43f5e" />
          <GaugeRing value={avgSpe} label="Spéculation (×0.25)"   color="#a855f7" />
          <GaugeRing value={avgSup} label="Offre (×0.25)"         color="#10b981" />
          <GaugeRing value={avgHom} label="Sans-Abrisme (×0.20)"  color="#ef4444" />
        </div>
      </div>

      <div className="bg-slate-900 border border-rose-800/30 rounded-xl p-5 grid grid-cols-1 md:grid-cols-2 gap-5">
        {dists.map(d => <DistBar key={d.title} {...d} />)}
      </div>

      <div className="flex flex-wrap gap-2">
        {["tous", "critique", "élevé", "modéré", "faible"].map(r => (
          <button key={r} onClick={() => setRisk(r)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${
              riskFilter === r
                ? "bg-rose-800 border-rose-700 text-white"
                : "bg-slate-900 border-rose-800/30 text-slate-400 hover:text-white"
            }`}>
            {r === "tous" ? "Tous" : r.charAt(0).toUpperCase() + r.slice(1)}
          </button>
        ))}
        <span className="w-px h-5 self-center bg-rose-800/30" />
        {["tous", "none", "homelessness_crisis_explosion", "financialization_speculation_trap", "rental_market_collapse", "displacement_gentrification", "social_housing_defunding"].map(p => (
          <button key={p} onClick={() => setPat(p)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${
              patFilter === p
                ? "bg-red-950 border-red-700 text-white"
                : "bg-slate-900 border-rose-800/30 text-slate-400 hover:text-white"
            }`}>
            {p === "tous" ? "Tous" : p.replace(/_/g, " ")}
          </button>
        ))}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {filtered.map(e => {
          const meta = RISK_META[e.risk_level];
          return (
            <div key={e.entity_id} onClick={() => setSelected(e)}
              className="bg-slate-900 border border-slate-800 rounded-xl p-4 cursor-pointer hover:border-rose-700/50 transition-colors">
              <div className="flex items-center justify-between mb-1">
                <span className="font-bold text-white">{e.entity_id}</span>
                <span className="text-xs text-slate-400">{e.region}</span>
              </div>
              <div className="text-xs text-rose-400 mb-2">{e.market_type.replace(/_/g, " ")}</div>
              <div className="flex gap-1 mb-3 flex-wrap">
                <span className={`px-2 py-0.5 rounded text-xs font-medium ${meta?.badge || "bg-slate-700 text-slate-300"}`}>
                  {meta?.label || e.risk_level}
                </span>
              </div>
              <div className="text-2xl font-black text-white mb-1">{e.composite_score.toFixed(1)}</div>
              <div className="text-xs text-slate-500 mb-2 capitalize">{e.housing_pattern.replace(/_/g, " ")}</div>
              <div className="text-xs text-slate-400 truncate">{e.signal}</div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
