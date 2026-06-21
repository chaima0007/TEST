"use client";
import { useEffect, useState } from "react";

type FoodEntity = {
  id: string;
  region: string;
  food_system_type: string;
  food_risk: string;
  food_pattern: string;
  food_severity: string;
  recommended_action: string;
  production_score: number;
  supply_score: number;
  access_score: number;
  resilience_score: number;
  food_composite: number;
  is_food_crisis: boolean;
  requires_food_intervention: boolean;
  food_signal: string;
};

type FoodSummary = {
  total_entities: number;
  critical_count: number;
  high_count: number;
  moderate_count: number;
  low_count: number;
  food_crisis_count: number;
  requires_intervention_count: number;
  avg_food_composite: number;
  avg_estimated_food_crisis_index: number;
  dominant_food_pattern: string;
  most_vulnerable_region: string;
  risk_counts: Record<string, number>;
  pattern_counts: Record<string, number>;
  severity_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_production_score: number;
  avg_supply_score: number;
  avg_access_score: number;
  avg_resilience_score: number;
};

function GaugeRing({ value, label, color }: { value: number; label: string; color: string }) {
  const r = 36;
  const circ = 2 * Math.PI * r;
  const fill = circ * (1 - value / 100);
  return (
    <div className="flex flex-col items-center gap-1">
      <svg width="88" height="88" viewBox="0 0 88 88">
        <circle cx="44" cy="44" r={r} fill="none" stroke="#0a1628" strokeWidth="8" />
        <circle cx="44" cy="44" r={r} fill="none" stroke={color} strokeWidth="8"
          strokeDasharray={circ} strokeDashoffset={fill}
          strokeLinecap="round" transform="rotate(-90 44 44)" />
        <text x="44" y="49" textAnchor="middle" fill="white" fontSize="13" fontWeight="bold">
          {Math.round(value)}
        </text>
      </svg>
      <span className="text-xs text-green-300/70 text-center">{label}</span>
    </div>
  );
}

function DistBar({ title, counts, colors }: { title: string; counts: Record<string, number>; colors: Record<string, string> }) {
  const total = Object.values(counts).reduce((a, b) => a + b, 0) || 1;
  return (
    <div className="flex flex-col gap-1">
      <span className="text-xs text-green-300/70 font-medium">{title}</span>
      <div className="flex h-3 rounded overflow-hidden gap-px">
        {Object.entries(counts).map(([k, v]) => (
          <div key={k} style={{ width: `${(v / total) * 100}%`, background: colors[k] || "#475569" }} title={`${k}: ${v}`} />
        ))}
      </div>
      <div className="flex flex-wrap gap-x-3 gap-y-0.5">
        {Object.entries(counts).map(([k, v]) => (
          <span key={k} className="text-xs text-green-300/60">
            <span style={{ color: colors[k] || "#94a3b8" }}>■</span> {k.replace(/_/g, " ")} {v}
          </span>
        ))}
      </div>
    </div>
  );
}

const RISK_COLORS = { low: "#10b981", moderate: "#f59e0b", high: "#3b82f6", critical: "#ef4444" };
const PAT_COLORS = {
  none: "#10b981",
  famine_cascade: "#ef4444",
  monoculture_collapse: "#f97316",
  price_shock_explosion: "#a855f7",
  soil_death_spiral: "#92400e",
  protein_transition_shock: "#06b6d4",
};
const SEV_COLORS = {
  food_secure: "#10b981",
  food_stress: "#f59e0b",
  food_crisis: "#3b82f6",
  food_emergency: "#ef4444",
};
const ACTION_COLORS = {
  no_action: "#10b981",
  food_monitoring: "#06b6d4",
  food_resilience_program: "#3b82f6",
  emergency_food_reserves: "#f97316",
  food_emergency_protocol: "#ef4444",
};
const RISK_BADGE: Record<string, string> = {
  low: "bg-emerald-900 text-emerald-300",
  moderate: "bg-amber-900 text-amber-300",
  high: "bg-blue-900 text-blue-300",
  critical: "bg-red-950 text-red-400",
};
const SEV_BADGE: Record<string, string> = {
  food_secure: "bg-emerald-900 text-emerald-300",
  food_stress: "bg-amber-900 text-amber-300",
  food_crisis: "bg-blue-900 text-blue-300",
  food_emergency: "bg-red-950 text-red-400",
};

function DetailModal({ entity, onClose }: { entity: FoodEntity; onClose: () => void }) {
  const [tab, setTab] = useState<"scores" | "signal" | "action">("scores");
  useEffect(() => {
    const h = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", h);
    return () => window.removeEventListener("keydown", h);
  }, [onClose]);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80" onClick={onClose}>
      <div className="bg-slate-950 border border-yellow-700/30 rounded-xl w-full max-w-lg p-6 shadow-2xl" onClick={e => e.stopPropagation()}>
        <div className="flex items-center justify-between mb-4">
          <div>
            <span className="text-lg font-bold text-white">{entity.id}</span>
            <span className="ml-2 text-green-400 text-xs">{entity.region}</span>
            <span className="ml-2 text-slate-500 text-xs">{entity.food_system_type.replace(/_/g, " ")}</span>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl leading-none">✕</button>
        </div>
        <div className="flex gap-2 mb-4">
          {(["scores", "signal", "action"] as const).map(t => (
            <button key={t} onClick={() => setTab(t)}
              className={`px-3 py-1 rounded text-xs font-medium transition-colors ${tab === t ? "bg-green-900 text-white" : "bg-slate-900 text-slate-400 hover:text-white"}`}>
              {t === "scores" ? "Scores" : t === "signal" ? "Signal" : "Action"}
            </button>
          ))}
        </div>

        {tab === "scores" && (
          <div className="grid grid-cols-2 gap-3 text-sm">
            {[
              ["Score Production",      entity.production_score, "#10b981"],
              ["Score Approvisionnement", entity.supply_score,   "#f59e0b"],
              ["Score Accès",           entity.access_score,     "#a855f7"],
              ["Score Résilience",      entity.resilience_score, "#06b6d4"],
            ].map(([l, v, c]) => (
              <div key={String(l)} className="bg-slate-900 border border-yellow-700/20 rounded-lg p-3">
                <div className="text-green-300/60 text-xs mb-1">{String(l)}</div>
                <div className="text-white font-bold text-lg">{Number(v).toFixed(1)}</div>
                <div className="h-1.5 rounded mt-1 bg-slate-800">
                  <div className="h-1.5 rounded" style={{ width: `${Math.min(Number(v), 100)}%`, background: String(c) }} />
                </div>
              </div>
            ))}
            <div className="col-span-2 bg-slate-900 border border-yellow-700/20 rounded-lg p-3">
              <div className="text-green-300/60 text-xs mb-1">Composite Alimentaire</div>
              <div className="text-white font-bold text-2xl">{entity.food_composite.toFixed(1)}</div>
            </div>
          </div>
        )}

        {tab === "signal" && (
          <div className="bg-slate-900 border border-yellow-700/20 rounded-lg p-4 text-sm text-slate-200 leading-relaxed">
            {entity.food_signal}
            <div className="mt-3 flex gap-2 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[entity.food_risk] || "bg-slate-700 text-slate-300"}`}>
                {entity.food_risk}
              </span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[entity.food_severity] || "bg-slate-700 text-slate-300"}`}>
                {entity.food_severity.replace(/_/g, " ")}
              </span>
            </div>
          </div>
        )}

        {tab === "action" && (
          <div className="space-y-3 text-sm">
            <div className="bg-slate-900 border border-yellow-700/20 rounded-lg p-3">
              <div className="text-green-300/60 text-xs mb-1">Action Recommandée</div>
              <div className="text-white font-medium">{entity.recommended_action.replace(/_/g, " ")}</div>
            </div>
            <div className="bg-slate-900 border border-yellow-700/20 rounded-lg p-3">
              <div className="text-green-300/60 text-xs mb-1">Système Alimentaire</div>
              <div className="text-white font-medium">{entity.food_system_type.replace(/_/g, " ")}</div>
            </div>
            <div className="bg-slate-900 border border-yellow-700/20 rounded-lg p-3">
              <div className="text-green-300/60 text-xs mb-1">Motif Détecté</div>
              <div className="text-green-400 font-medium">{entity.food_pattern.replace(/_/g, " ")}</div>
            </div>
            <div className="flex gap-1 flex-wrap">
              {entity.is_food_crisis && (
                <span className="px-2 py-1 rounded bg-red-950 text-red-400 text-xs font-medium">CRISE ALIMENTAIRE</span>
              )}
              {entity.requires_food_intervention && (
                <span className="px-2 py-1 rounded bg-yellow-950 text-yellow-400 text-xs font-medium">INTERVENTION REQ.</span>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function FoodSystemCollapseDashboard() {
  const [data, setData]           = useState<{ entities: FoodEntity[]; summary: FoodSummary } | null>(null);
  const [filter, setFilter]       = useState<string>("all");
  const [patFilter, setPatFilter] = useState<string>("all");
  const [selected, setSelected]   = useState<FoodEntity | null>(null);

  useEffect(() => {
    fetch("/api/food-system-collapse-engine")
      .then(r => r.json())
      .then(setData)
      .catch(console.error);
  }, []);

  if (!data) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-green-400 text-lg animate-pulse">Initialisation du Moteur Effondrement Système Alimentaire...</div>
    </div>
  );

  const { entities, summary } = data;
  const filtered = entities.filter(e =>
    (filter === "all" || e.food_risk === filter) &&
    (patFilter === "all" || e.food_pattern === patFilter)
  );

  const dists = [
    { title: "Niveau de Risque Alimentaire", counts: summary.risk_counts,     colors: RISK_COLORS   },
    { title: "Motif Alimentaire Détecté",    counts: summary.pattern_counts,  colors: PAT_COLORS    },
    { title: "Sévérité Alimentaire",         counts: summary.severity_counts, colors: SEV_COLORS    },
    { title: "Action Déclenchée",            counts: summary.action_counts,   colors: ACTION_COLORS },
  ] as Array<{ title: string; counts: Record<string, number>; colors: Record<string, string> }>;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {selected && <DetailModal entity={selected} onClose={() => setSelected(null)} />}

      <div>
        <h1 className="text-2xl font-bold text-green-400">Effondrement Système Alimentaire — Module 319</h1>
        <p className="text-green-300/50 text-sm mt-1">
          Production Agricole · Approvisionnement Alimentaire · Accès &amp; Prix · Résilience Agro-Alimentaire
        </p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {[
          ["Entités Analysées",        summary.total_entities,                                              "text-green-400"],
          ["En Crise Alimentaire",     summary.food_crisis_count,                                           "text-red-400"],
          ["Intervention Requise",     summary.requires_intervention_count,                                 "text-yellow-400"],
          ["Composite Moyen",          `${summary.avg_food_composite.toFixed(1)}`,                         "text-green-300"],
          ["Index de Crise Estimé",    `${summary.avg_estimated_food_crisis_index.toFixed(2)}/10`,          "text-amber-400"],
          ["Motif Dominant",           (summary.dominant_food_pattern || "none").replace(/_/g, " "),       "text-green-400"],
        ].map(([l, v, c]) => (
          <div key={String(l)} className="bg-slate-900 border border-yellow-700/30 rounded-xl p-3 text-center">
            <div className={`text-xl font-bold ${c} truncate`}>{v}</div>
            <div className="text-xs text-green-300/40 mt-0.5 leading-tight">{l}</div>
          </div>
        ))}
      </div>

      {/* Gauge Rings */}
      <div className="bg-slate-900 border border-yellow-700/30 rounded-xl p-5">
        <div className="grid grid-cols-4 gap-4">
          <GaugeRing value={summary.avg_production_score || 0} label="Score Production Moy."        color="#10b981" />
          <GaugeRing value={summary.avg_supply_score || 0}     label="Score Approvisionnement Moy." color="#f59e0b" />
          <GaugeRing value={summary.avg_access_score || 0}     label="Score Accès Moy."             color="#a855f7" />
          <GaugeRing value={summary.avg_resilience_score || 0} label="Score Résilience Moy."        color="#06b6d4" />
        </div>
      </div>

      {/* Distribution Bars */}
      <div className="bg-slate-900 border border-yellow-700/30 rounded-xl p-5 grid grid-cols-1 md:grid-cols-2 gap-5">
        {dists.map(d => <DistBar key={d.title} {...d} />)}
      </div>

      {/* Filter Pills */}
      <div className="flex flex-wrap gap-2">
        {["all", "low", "moderate", "high", "critical"].map(r => (
          <button key={r} onClick={() => setFilter(r)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${filter === r ? "bg-green-900 border-green-700 text-white" : "bg-slate-900 border-yellow-700/30 text-green-400/70 hover:text-white"}`}>
            {r}
          </button>
        ))}
        <span className="w-px h-5 self-center bg-yellow-700/30" />
        {["all", "none", "famine_cascade", "monoculture_collapse", "price_shock_explosion", "soil_death_spiral", "protein_transition_shock"].map(p => (
          <button key={p} onClick={() => setPatFilter(p)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${patFilter === p ? "bg-yellow-950 border-yellow-700 text-white" : "bg-slate-900 border-yellow-700/30 text-green-400/70 hover:text-white"}`}>
            {p.replace(/_/g, " ")}
          </button>
        ))}
      </div>

      {/* Entity Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {filtered.map(e => (
          <div key={e.id} onClick={() => setSelected(e)}
            className="bg-slate-900 border border-yellow-700/30 rounded-xl p-4 cursor-pointer hover:border-green-500 transition-colors">
            <div className="flex items-center justify-between mb-1">
              <span className="font-bold text-white">{e.id}</span>
              <span className="text-xs text-green-400/60">{e.region}</span>
            </div>
            <div className="text-xs text-slate-500 mb-2 capitalize">{e.food_system_type.replace(/_/g, " ")}</div>
            <div className="flex gap-1 mb-3 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[e.food_risk] || "bg-slate-700 text-slate-300"}`}>
                {e.food_risk}
              </span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[e.food_severity] || "bg-slate-700 text-slate-300"}`}>
                {e.food_severity.replace(/_/g, " ")}
              </span>
            </div>
            <div className="text-2xl font-black text-white mb-1">{e.food_composite.toFixed(1)}</div>
            <div className="text-xs text-green-400/60 mb-2 capitalize">{e.food_pattern.replace(/_/g, " ")}</div>
            <div className="text-xs text-green-400 font-medium mb-2">
              Prod: {e.production_score.toFixed(1)} · Appro: {e.supply_score.toFixed(1)}
            </div>
            <div className="flex gap-1 flex-wrap">
              {e.is_food_crisis && (
                <span className="px-1.5 py-0.5 rounded bg-red-950 text-red-400 text-xs">CRISE</span>
              )}
              {e.requires_food_intervention && (
                <span className="px-1.5 py-0.5 rounded bg-yellow-950 text-yellow-400 text-xs">INTERVENTION</span>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
