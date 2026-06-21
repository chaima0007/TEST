"use client";
import { useEffect, useState } from "react";

// ── Types ─────────────────────────────────────────────────────────────────────

type ChainEntity = {
  id: string;
  region: string;
  chain_type: string;
  chain_risk: string;
  chain_pattern: string;
  chain_severity: string;
  recommended_action: string;
  concentration_score: number;
  fragility_score: number;
  risk_score: number;
  adaptation_score: number;
  chain_composite: number;
  is_chain_crisis: boolean;
  requires_chain_intervention: boolean;
  chain_signal: string;
};

type ApiData = {
  module: string;
  engine: string;
  analyst: string;
  timestamp: string;
  total_entities_assessed: number;
  critical_chains: number;
  high_risk_chains: number;
  chain_crises_detected: number;
  requires_intervention: number;
  dominant_pattern: string;
  avg_estimated_chain_fragility_index: number;
  risk_distribution: Record<string, number>;
  entities: ChainEntity[];
};

// ── Colour maps ───────────────────────────────────────────────────────────────

const RISK_COLOR: Record<string, string> = {
  low:      "#10b981",
  moderate: "#f59e0b",
  high:     "#f97316",
  critical: "#ef4444",
};
const RISK_BADGE: Record<string, string> = {
  low:      "bg-emerald-500/20 border border-emerald-500/30 text-emerald-300",
  moderate: "bg-amber-500/20 border border-amber-500/30 text-amber-300",
  high:     "bg-orange-500/20 border border-orange-500/30 text-orange-300",
  critical: "bg-red-500/20 border border-red-500/30 text-red-300",
};
const PAT_BADGE: Record<string, string> = {
  none:                    "bg-slate-700/50 text-slate-400",
  single_source_crisis:    "bg-red-500/20 text-red-300",
  jit_shock_cascade:       "bg-orange-500/20 text-orange-300",
  supplier_bankruptcy_wave:"bg-amber-500/20 text-amber-300",
  cyber_supply_attack:     "bg-violet-500/20 text-violet-300",
  regulatory_fragmentation:"bg-sky-500/20 text-sky-300",
};
const SEV_COLOR: Record<string, string> = {
  chain_robust:    "#10b981",
  supply_tension:  "#f59e0b",
  high_fragility:  "#f97316",
  supply_emergency:"#ef4444",
};

// ── SVG Gauge Ring ────────────────────────────────────────────────────────────

function GaugeRing({ value, label, color }: { value: number; label: string; color: string }) {
  const r = 38;
  const circ = 2 * Math.PI * r;
  const offset = circ * (1 - value / 100);
  return (
    <div className="flex flex-col items-center gap-2">
      <svg width="96" height="96" viewBox="0 0 96 96">
        <circle cx="48" cy="48" r={r} fill="none" stroke="#1e293b" strokeWidth="9" />
        <circle
          cx="48" cy="48" r={r} fill="none"
          stroke={color} strokeWidth="9"
          strokeDasharray={circ}
          strokeDashoffset={offset}
          strokeLinecap="round"
          transform="rotate(-90 48 48)"
        />
        <text x="48" y="53" textAnchor="middle" fill="white" fontSize="14" fontWeight="bold">
          {Math.round(value)}
        </text>
      </svg>
      <span className="text-xs text-slate-400 text-center leading-tight max-w-[88px]">{label}</span>
    </div>
  );
}

// ── Distribution Bar ──────────────────────────────────────────────────────────

function DistBar({ label, value, max, color }: { label: string; value: number; max: number; color: string }) {
  const pct = max > 0 ? (value / max) * 100 : 0;
  return (
    <div className="flex items-center gap-3">
      <span className="text-xs text-slate-400 w-28 shrink-0 truncate">{label}</span>
      <div className="flex-1 h-2 bg-slate-800 rounded-full overflow-hidden">
        <div className="h-2 rounded-full transition-all" style={{ width: `${pct}%`, background: color }} />
      </div>
      <span className="text-xs font-semibold text-slate-300 w-10 text-right">{value.toFixed(1)}</span>
    </div>
  );
}

// ── Detail Modal ──────────────────────────────────────────────────────────────

function DetailModal({ entity, onClose }: { entity: ChainEntity; onClose: () => void }) {
  const [tab, setTab] = useState<"scores" | "analyse" | "recommandations">("scores");

  useEffect(() => {
    const h = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", h);
    return () => window.removeEventListener("keydown", h);
  }, [onClose]);

  const color = RISK_COLOR[entity.chain_risk] ?? "#94a3b8";
  const r = 42;
  const circ = 2 * Math.PI * r;
  const offset = circ * (1 - entity.chain_composite / 100);

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm"
      onClick={onClose}
    >
      <div
        className="relative w-full max-w-2xl rounded-2xl border border-slate-700 bg-slate-900 shadow-2xl mx-4"
        onClick={e => e.stopPropagation()}
      >
        <button
          onClick={onClose}
          className="absolute top-4 right-4 text-slate-400 hover:text-white text-xl font-bold transition-colors"
        >✕</button>

        {/* Header */}
        <div className="p-6 border-b border-slate-800 flex items-center gap-5">
          <svg width="96" height="96" viewBox="0 0 96 96" className="shrink-0">
            <circle cx="48" cy="48" r={r} fill="none" stroke="#1e293b" strokeWidth="9" />
            <circle cx="48" cy="48" r={r} fill="none"
              stroke={color} strokeWidth="9"
              strokeDasharray={circ}
              strokeDashoffset={offset}
              strokeLinecap="round"
              transform="rotate(-90 48 48)"
            />
            <text x="48" y="53" textAnchor="middle" fill={color} fontSize="15" fontWeight="bold">
              {entity.chain_composite.toFixed(0)}
            </text>
          </svg>
          <div>
            <h2 className="text-xl font-bold text-slate-100">{entity.id}</h2>
            <p className="text-slate-400 text-sm mt-0.5">{entity.chain_type.replace(/_/g, " ")} · {entity.region}</p>
            <div className="flex flex-wrap gap-2 mt-2">
              <span className={`px-2 py-0.5 rounded-full text-xs font-semibold uppercase tracking-wide ${RISK_BADGE[entity.chain_risk]}`}>
                {entity.chain_risk}
              </span>
              <span className={`px-2 py-0.5 rounded-full text-xs font-semibold ${PAT_BADGE[entity.chain_pattern]}`}>
                {entity.chain_pattern.replace(/_/g, " ")}
              </span>
              {entity.is_chain_crisis && (
                <span className="px-2 py-0.5 rounded-full bg-red-500/20 text-red-300 border border-red-500/30 text-xs font-semibold">CRISE</span>
              )}
            </div>
          </div>
        </div>

        {/* Tabs */}
        <div className="flex border-b border-slate-800">
          {(["scores", "analyse", "recommandations"] as const).map(t => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`flex-1 px-4 py-3 text-sm font-medium transition-colors capitalize ${tab === t ? "text-orange-400 border-b-2 border-orange-400" : "text-slate-500 hover:text-slate-300"}`}
            >{t}</button>
          ))}
        </div>

        {/* Tab content */}
        <div className="p-6">
          {tab === "scores" && (
            <div className="space-y-4">
              <div className="grid grid-cols-2 gap-3">
                {[
                  { label: "Concentration", value: entity.concentration_score, color: "#ef4444" },
                  { label: "Fragilité Opérationnelle", value: entity.fragility_score, color: "#f97316" },
                  { label: "Exposition Risques", value: entity.risk_score, color: "#a855f7" },
                  { label: "Adaptation Structurelle", value: entity.adaptation_score, color: "#f59e0b" },
                ].map(({ label, value, color: c }) => (
                  <div key={label} className="bg-slate-800/50 rounded-xl p-4">
                    <p className="text-slate-400 text-xs mb-1">{label}</p>
                    <p className="text-white font-bold text-lg">{value.toFixed(1)}</p>
                    <div className="h-1.5 rounded-full bg-slate-700 mt-2">
                      <div className="h-1.5 rounded-full" style={{ width: `${Math.min(value, 100)}%`, background: c }} />
                    </div>
                  </div>
                ))}
              </div>
              <div className="bg-slate-800/30 rounded-xl p-4 text-center">
                <p className="text-slate-400 text-xs mb-1">Composite Fragilité Chaîne</p>
                <p className="text-2xl font-bold" style={{ color }}>{entity.chain_composite.toFixed(1)}</p>
              </div>
            </div>
          )}

          {tab === "analyse" && (
            <div className="space-y-4">
              <div className="bg-slate-800/30 rounded-xl p-4">
                <p className="text-orange-400 text-xs font-semibold uppercase tracking-wide mb-2">Signal Chaîne</p>
                <p className="text-slate-200 text-sm leading-relaxed">{entity.chain_signal}</p>
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div className="bg-slate-800/50 rounded-xl p-3">
                  <p className="text-slate-400 text-xs mb-1">Sévérité</p>
                  <p className="text-white font-semibold text-sm capitalize" style={{ color: SEV_COLOR[entity.chain_severity] }}>
                    {entity.chain_severity.replace(/_/g, " ")}
                  </p>
                </div>
                <div className="bg-slate-800/50 rounded-xl p-3">
                  <p className="text-slate-400 text-xs mb-1">Intervention Requise</p>
                  <p className={`font-semibold text-sm ${entity.requires_chain_intervention ? "text-orange-400" : "text-slate-500"}`}>
                    {entity.requires_chain_intervention ? "OUI" : "Non"}
                  </p>
                </div>
              </div>
              <div className="bg-slate-800/50 rounded-xl p-3">
                <p className="text-slate-400 text-xs mb-1">Pattern Détecté</p>
                <p className="text-white font-semibold text-sm capitalize">{entity.chain_pattern.replace(/_/g, " ")}</p>
              </div>
            </div>
          )}

          {tab === "recommandations" && (
            <div className="space-y-4">
              <div className="bg-orange-500/10 border border-orange-500/20 rounded-xl p-4">
                <p className="text-orange-400 text-xs font-semibold uppercase tracking-wide mb-2">Action Recommandée</p>
                <p className="text-slate-100 font-semibold text-base capitalize">
                  {entity.recommended_action.replace(/_/g, " ")}
                </p>
              </div>
              <div className="bg-slate-800/30 rounded-xl p-4 space-y-2">
                {[
                  { label: "Crise Chaîne", value: entity.is_chain_crisis, yes: "text-red-400", no: "text-slate-500" },
                  { label: "Intervention Requise", value: entity.requires_chain_intervention, yes: "text-orange-400", no: "text-slate-500" },
                ].map(({ label, value, yes, no }) => (
                  <div key={label} className="flex justify-between text-sm">
                    <span className="text-slate-400">{label}</span>
                    <span className={`font-semibold ${value ? yes : no}`}>{value ? "OUI" : "Non"}</span>
                  </div>
                ))}
                <div className="flex justify-between text-sm">
                  <span className="text-slate-400">Risque</span>
                  <span className="font-semibold capitalize" style={{ color: RISK_COLOR[entity.chain_risk] }}>{entity.chain_risk}</span>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

// ── Main Page ─────────────────────────────────────────────────────────────────

export default function SupplyChainFragilityPage() {
  const [data, setData]       = useState<ApiData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError]     = useState<string | null>(null);
  const [riskFilter, setRisk] = useState<string>("all");
  const [selected, setSelected] = useState<ChainEntity | null>(null);

  useEffect(() => {
    setLoading(true);
    setError(null);
    fetch("/api/supply-chain-fragility-engine")
      .then(r => {
        if (!r.ok) throw new Error(`HTTP ${r.status}`);
        return r.json();
      })
      .then(setData)
      .catch(e => setError(String(e)))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center">
        <div className="text-orange-400 text-lg animate-pulse">
          Chargement Intelligence Chaîne d'Approvisionnement…
        </div>
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center">
        <div className="text-red-400 text-base">
          Erreur: {error ?? "Données indisponibles"}
        </div>
      </div>
    );
  }

  const filtered = data.entities.filter(e =>
    riskFilter === "all" || e.chain_risk === riskFilter
  );

  // Average sub-scores
  const n = data.entities.length;
  const avgConc  = data.entities.reduce((s, e) => s + e.concentration_score, 0) / n;
  const avgFrag  = data.entities.reduce((s, e) => s + e.fragility_score, 0) / n;
  const avgRisk  = data.entities.reduce((s, e) => s + e.risk_score, 0) / n;
  const avgAdapt = data.entities.reduce((s, e) => s + e.adaptation_score, 0) / n;

  const kpis = [
    { label: "Entités Évaluées",        value: data.total_entities_assessed,            color: "text-orange-400" },
    { label: "Chaînes Critiques",        value: data.critical_chains,                    color: "text-red-400" },
    { label: "Risque Élevé",             value: data.high_risk_chains,                   color: "text-orange-300" },
    { label: "Crises Détectées",         value: data.chain_crises_detected,              color: "text-red-400" },
    { label: "Intervention Requise",     value: data.requires_intervention,              color: "text-amber-400" },
    { label: "Indice Fragilité Moyen",   value: data.avg_estimated_chain_fragility_index, color: "text-orange-400" },
  ];

  const gauges = [
    { label: "Concentration", value: avgConc,  color: "#ef4444" },
    { label: "Fragilité",     value: avgFrag,  color: "#f97316" },
    { label: "Risques",       value: avgRisk,  color: "#a855f7" },
    { label: "Adaptation",    value: avgAdapt, color: "#f59e0b" },
  ];

  const distBars = [
    { label: "Concentration",    value: avgConc,  max: 100, color: "#ef4444" },
    { label: "Fragilité",        value: avgFrag,  max: 100, color: "#f97316" },
    { label: "Risques",          value: avgRisk,  max: 100, color: "#a855f7" },
    { label: "Adaptation",       value: avgAdapt, max: 100, color: "#f59e0b" },
  ];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {selected && <DetailModal entity={selected} onClose={() => setSelected(null)} />}

      {/* Title */}
      <div>
        <h1 className="text-2xl font-bold text-orange-400">
          Fragilité Chaîne d'Approvisionnement Mondiale — Module 311
        </h1>
        <p className="text-slate-400 text-sm mt-1">
          {data.engine} · {data.analyst}
        </p>
        <p className="text-slate-600 text-xs mt-0.5">
          Pattern dominant: <span className="text-orange-400 capitalize">{data.dominant_pattern.replace(/_/g, " ")}</span>
        </p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-4">
        {kpis.map(({ label, value, color }) => (
          <div key={label} className="bg-slate-900 border border-slate-500/30 rounded-2xl p-4 text-center">
            <p className={`text-2xl font-bold ${color}`}>{value}</p>
            <p className="text-slate-400 text-xs mt-1 leading-tight">{label}</p>
          </div>
        ))}
      </div>

      {/* Gauge Rings */}
      <div className="bg-slate-900 border border-slate-500/30 rounded-2xl p-6">
        <h2 className="text-sm font-semibold text-slate-400 uppercase tracking-wide mb-5">
          Scores Moyens par Dimension
        </h2>
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-6">
          {gauges.map(g => <GaugeRing key={g.label} {...g} />)}
        </div>
      </div>

      {/* Distribution Bars */}
      <div className="bg-slate-900 border border-slate-500/30 rounded-2xl p-6">
        <h2 className="text-sm font-semibold text-slate-400 uppercase tracking-wide mb-5">
          Distribution des Scores (Moyenne Portefeuille)
        </h2>
        <div className="space-y-4">
          {distBars.map(d => <DistBar key={d.label} {...d} />)}
        </div>
      </div>

      {/* Risk Distribution Mini-chart */}
      <div className="bg-slate-900 border border-slate-500/30 rounded-2xl p-5">
        <h2 className="text-sm font-semibold text-slate-400 uppercase tracking-wide mb-3">
          Distribution des Risques
        </h2>
        <div className="flex h-4 rounded-full overflow-hidden gap-0.5 mb-3">
          {(["low", "moderate", "high", "critical"] as const).map(r => {
            const pct = ((data.risk_distribution[r] || 0) / n) * 100;
            return pct > 0 ? (
              <div
                key={r}
                style={{ width: `${pct}%`, background: RISK_COLOR[r] }}
                title={`${r}: ${data.risk_distribution[r]}`}
                className="relative group"
              >
                <span className="absolute bottom-full mb-1 left-1/2 -translate-x-1/2 bg-slate-800 text-xs rounded px-2 py-1 whitespace-nowrap opacity-0 group-hover:opacity-100 transition-opacity z-10">
                  {r}: {data.risk_distribution[r]}
                </span>
              </div>
            ) : null;
          })}
        </div>
        <div className="flex flex-wrap gap-4">
          {(["low", "moderate", "high", "critical"] as const).map(r => (
            <div key={r} className="flex items-center gap-1.5">
              <div className="w-2.5 h-2.5 rounded-full" style={{ background: RISK_COLOR[r] }} />
              <span className="text-slate-400 text-xs capitalize">
                {r} ({data.risk_distribution[r] || 0})
              </span>
            </div>
          ))}
        </div>
      </div>

      {/* Filter Pills */}
      <div className="flex flex-wrap gap-2">
        {["all", "critical", "high", "moderate", "low"].map(r => (
          <button
            key={r}
            onClick={() => setRisk(r)}
            className={`px-3 py-1.5 rounded-full text-xs font-medium border transition-colors ${
              riskFilter === r
                ? "bg-orange-600 border-orange-500 text-white"
                : "bg-slate-900 border-slate-700 text-slate-400 hover:text-slate-200"
            }`}
          >
            {r === "all" ? "Tous les risques" : r.charAt(0).toUpperCase() + r.slice(1)}
          </button>
        ))}
      </div>

      {/* Entity Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {filtered.map(entity => {
          const color = RISK_COLOR[entity.chain_risk] ?? "#94a3b8";
          const sz = 56;
          const er = sz * 0.38;
          const ec = 2 * Math.PI * er;
          const eo = ec * (1 - entity.chain_composite / 100);
          return (
            <button
              key={entity.id}
              onClick={() => setSelected(entity)}
              className="bg-slate-900 border border-slate-800 rounded-2xl p-5 text-left hover:border-orange-500/50 transition-all hover:bg-slate-800/50 group"
            >
              <div className="flex items-center justify-between mb-3">
                <div className="flex-1 min-w-0 mr-3">
                  <p className="text-slate-100 font-semibold text-sm truncate">{entity.id}</p>
                  <p className="text-slate-400 text-xs">{entity.region}</p>
                </div>
                <svg width={sz} height={sz} viewBox={`0 0 ${sz} ${sz}`} className="shrink-0">
                  <circle cx={sz / 2} cy={sz / 2} r={er} fill="none" stroke="#1e293b" strokeWidth={sz * 0.09} />
                  <circle cx={sz / 2} cy={sz / 2} r={er} fill="none"
                    stroke={color} strokeWidth={sz * 0.09}
                    strokeDasharray={ec}
                    strokeDashoffset={eo}
                    strokeLinecap="round"
                    transform={`rotate(-90 ${sz / 2} ${sz / 2})`}
                  />
                  <text x={sz / 2} y={sz / 2 + 4} textAnchor="middle" fill={color} fontSize={sz * 0.19} fontWeight="bold">
                    {entity.chain_composite.toFixed(0)}
                  </text>
                </svg>
              </div>

              <p className="text-slate-400 text-xs mb-3 truncate capitalize">
                {entity.chain_type.replace(/_/g, " ")}
              </p>

              <div className="flex flex-wrap gap-1.5 mb-3">
                <span className={`px-2 py-0.5 rounded-full text-xs font-semibold ${RISK_BADGE[entity.chain_risk]}`}>
                  {entity.chain_risk}
                </span>
                {entity.chain_pattern !== "none" && (
                  <span className={`px-2 py-0.5 rounded-full text-xs font-semibold ${PAT_BADGE[entity.chain_pattern]}`}>
                    {entity.chain_pattern.replace(/_/g, " ")}
                  </span>
                )}
              </div>

              <div className="flex gap-1.5 flex-wrap mb-2">
                {entity.is_chain_crisis && (
                  <span className="px-1.5 py-0.5 rounded bg-red-500/20 text-red-300 text-xs font-semibold">CRISE</span>
                )}
                {entity.requires_chain_intervention && (
                  <span className="px-1.5 py-0.5 rounded bg-orange-500/20 text-orange-300 text-xs">Intervention</span>
                )}
              </div>

              <p className="text-slate-500 text-xs line-clamp-2 group-hover:text-slate-400 transition-colors">
                {entity.chain_signal}
              </p>
            </button>
          );
        })}
      </div>
    </div>
  );
}
