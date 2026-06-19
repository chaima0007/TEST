"use client";
import { useEffect, useState } from "react";

// Module 315 — Economic Singularity Simulation Intelligence Engine
// Caelum Partners — Chaima Mhadbi, Fondatrice, Bruxelles

type Entity = {
  entity_id: string;
  region: string;
  economy_type: string;
  singularity_risk: string;
  singularity_pattern: string;
  singularity_severity: string;
  recommended_action: string;
  displacement_score: number;
  transition_score: number;
  concentration_score: number;
  disruption_score: number;
  singularity_composite: number;
  is_singularity_crisis: boolean;
  requires_singularity_intervention: boolean;
  singularity_signal: string;
};

type Summary = {
  total: number;
  risk_counts: Record<string, number>;
  pattern_counts: Record<string, number>;
  severity_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_singularity_composite: number;
  singularity_crisis_count: number;
  singularity_intervention_count: number;
  avg_displacement_score: number;
  avg_transition_score: number;
  avg_concentration_score: number;
  avg_disruption_score: number;
  avg_estimated_singularity_proximity_index: number;
};

function GaugeRing({ value, label, color }: { value: number; label: string; color: string }) {
  const r = 36;
  const circ = 2 * Math.PI * r;
  const fill = circ * (1 - value / 100);
  return (
    <div className="flex flex-col items-center gap-1">
      <svg width="88" height="88" viewBox="0 0 88 88">
        <circle cx="44" cy="44" r={r} fill="none" stroke="#1a1200" strokeWidth="8" />
        <circle
          cx="44" cy="44" r={r} fill="none" stroke={color} strokeWidth="8"
          strokeDasharray={circ} strokeDashoffset={fill}
          strokeLinecap="round" transform="rotate(-90 44 44)"
        />
        <text x="44" y="49" textAnchor="middle" fill="white" fontSize="13" fontWeight="bold">
          {Math.round(value)}
        </text>
      </svg>
      <span className="text-xs text-yellow-300/60 text-center">{label}</span>
    </div>
  );
}

function DistBar({ title, counts, colors }: { title: string; counts: Record<string, number>; colors: Record<string, string> }) {
  const total = Object.values(counts).reduce((a, b) => a + b, 0) || 1;
  return (
    <div className="flex flex-col gap-1">
      <span className="text-xs text-yellow-300/60 font-medium">{title}</span>
      <div className="flex h-3 rounded overflow-hidden gap-px">
        {Object.entries(counts).map(([k, v]) => (
          <div
            key={k}
            style={{ width: `${(v / total) * 100}%`, background: colors[k] || "#475569" }}
            title={`${k}: ${v}`}
          />
        ))}
      </div>
      <div className="flex flex-wrap gap-x-3 gap-y-0.5">
        {Object.entries(counts).map(([k, v]) => (
          <span key={k} className="text-xs text-yellow-300/50">
            <span style={{ color: colors[k] || "#94a3b8" }}>■</span> {k.replace(/_/g, " ")} {v}
          </span>
        ))}
      </div>
    </div>
  );
}

const RISK_COLORS = { low: "#10b981", moderate: "#f59e0b", high: "#f97316", critical: "#ef4444" };
const PAT_COLORS = {
  none: "#10b981",
  singularity_threshold_breach: "#dc2626",
  labor_extinction_event: "#7c3aed",
  capital_hypercentralization: "#f59e0b",
  institutional_collapse: "#f97316",
  social_contract_rupture: "#a855f7",
};
const SEV_COLORS = {
  pre_acceleration: "#10b981",
  singularity_approaching: "#f59e0b",
  phase_transition_critical: "#f97316",
  singularity_imminent: "#ef4444",
};
const ACT_COLORS = {
  no_action: "#10b981",
  economic_monitoring: "#eab308",
  singularity_transition_program: "#3b82f6",
  universal_income_emergency: "#f97316",
  emergency_economic_redesign: "#ef4444",
};
const RISK_BADGE: Record<string, string> = {
  low: "bg-emerald-950 text-emerald-400",
  moderate: "bg-yellow-950 text-yellow-300",
  high: "bg-orange-950 text-orange-400",
  critical: "bg-red-950 text-red-400",
};
const SEV_BADGE: Record<string, string> = {
  pre_acceleration: "bg-emerald-950 text-emerald-400",
  singularity_approaching: "bg-yellow-950 text-yellow-300",
  phase_transition_critical: "bg-orange-950 text-orange-400",
  singularity_imminent: "bg-red-950 text-red-400",
};

function DetailModal({ entity, onClose }: { entity: Entity; onClose: () => void }) {
  const [tab, setTab] = useState<"scores" | "signal" | "action">("scores");

  useEffect(() => {
    const h = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", h);
    return () => window.removeEventListener("keydown", h);
  }, [onClose]);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/75" onClick={onClose}>
      <div
        className="bg-slate-950 border border-yellow-600/30 rounded-xl w-full max-w-lg p-6 shadow-2xl"
        onClick={e => e.stopPropagation()}
      >
        <div className="flex items-center justify-between mb-4">
          <div>
            <span className="text-lg font-bold text-yellow-300">{entity.entity_id}</span>
            <span className="ml-2 text-yellow-300/60 text-xs">{entity.economy_type.replace(/_/g, " ")}</span>
            <span className="ml-2 text-yellow-300/40 text-xs">{entity.region}</span>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-yellow-300 text-xl leading-none">✕</button>
        </div>

        <div className="flex gap-2 mb-4">
          {(["scores", "signal", "action"] as const).map(t => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`px-3 py-1 rounded text-xs font-medium transition-colors ${
                tab === t
                  ? "bg-yellow-700 text-white"
                  : "bg-slate-900 text-yellow-300/50 hover:text-yellow-300"
              }`}
            >
              {t === "scores" ? "Scores" : t === "signal" ? "Signal" : "Action"}
            </button>
          ))}
        </div>

        {tab === "scores" && (
          <div className="grid grid-cols-2 gap-3 text-sm">
            {([
              ["Déplacement IA",   entity.displacement_score,  "#f97316"],
              ["Transition Phase", entity.transition_score,    "#eab308"],
              ["Concentration",    entity.concentration_score, "#f59e0b"],
              ["Disruption",       entity.disruption_score,    "#ef4444"],
            ] as [string, number, string][]).map(([l, v, c]) => (
              <div key={l} className="bg-slate-900 border border-yellow-600/20 rounded-lg p-3">
                <div className="text-yellow-300/50 text-xs mb-1">{l}</div>
                <div className="text-white font-bold text-lg">{v.toFixed(1)}</div>
                <div className="h-1.5 rounded mt-1 bg-slate-800">
                  <div className="h-1.5 rounded" style={{ width: `${Math.min(v, 100)}%`, background: c }} />
                </div>
              </div>
            ))}
            <div className="col-span-2 bg-slate-900 border border-yellow-600/30 rounded-lg p-3">
              <div className="text-yellow-300/50 text-xs mb-1">Composite Singularité</div>
              <div className="text-yellow-300 font-bold text-2xl">{entity.singularity_composite.toFixed(1)}</div>
            </div>
          </div>
        )}

        {tab === "signal" && (
          <div className="bg-slate-900 border border-yellow-600/20 rounded-lg p-4 text-sm text-slate-200 leading-relaxed">
            {entity.singularity_signal}
            <div className="mt-3 flex gap-2 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[entity.singularity_risk] || "bg-slate-700 text-slate-300"}`}>
                {entity.singularity_risk}
              </span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[entity.singularity_severity] || "bg-slate-700 text-slate-300"}`}>
                {entity.singularity_severity.replace(/_/g, " ")}
              </span>
            </div>
          </div>
        )}

        {tab === "action" && (
          <div className="space-y-3 text-sm">
            <div className="bg-slate-900 border border-yellow-600/20 rounded-lg p-3">
              <div className="text-yellow-300/50 text-xs mb-1">Action Recommandée</div>
              <div className="text-white font-medium capitalize">{entity.recommended_action.replace(/_/g, " ")}</div>
            </div>
            <div className="bg-slate-900 border border-yellow-600/20 rounded-lg p-3">
              <div className="text-yellow-300/50 text-xs mb-1">Pattern Détecté</div>
              <div className="text-white font-medium capitalize">{entity.singularity_pattern.replace(/_/g, " ")}</div>
            </div>
            <div className="flex gap-2 flex-wrap">
              {entity.is_singularity_crisis && (
                <span className="px-2 py-1 rounded bg-red-950 text-red-400 text-xs font-medium">SINGULARITÉ IMMINENTE</span>
              )}
              {entity.requires_singularity_intervention && (
                <span className="px-2 py-1 rounded bg-yellow-950 text-yellow-400 text-xs font-medium">INTERVENTION</span>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function EconomicSingularityDashboard() {
  const [data, setData]     = useState<{ entities: Entity[]; summary: Summary } | null>(null);
  const [filter, setFilter] = useState<string>("all");
  const [patFilter, setPat] = useState<string>("all");
  const [selected, setSelected] = useState<Entity | null>(null);

  useEffect(() => {
    fetch("/api/economic-singularity-engine")
      .then(r => r.json())
      .then(setData)
      .catch(console.error);
  }, []);

  if (!data) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-yellow-300 text-lg animate-pulse">
        Chargement du Simulateur de Singularité Économique...
      </div>
    </div>
  );

  const { entities, summary } = data;
  const filtered = entities.filter(e =>
    (filter === "all" || e.singularity_risk === filter) &&
    (patFilter === "all" || e.singularity_pattern === patFilter)
  );

  const dists = [
    { title: "Risque Singularité",     counts: summary.risk_counts,     colors: RISK_COLORS },
    { title: "Patterns Détectés",      counts: summary.pattern_counts,  colors: PAT_COLORS  },
    { title: "Sévérité",               counts: summary.severity_counts, colors: SEV_COLORS  },
    { title: "Actions Déclenchées",    counts: summary.action_counts,   colors: ACT_COLORS  },
  ] as Array<{ title: string; counts: Record<string, number>; colors: Record<string, string> }>;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {selected && <DetailModal entity={selected} onClose={() => setSelected(null)} />}

      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-yellow-300">
          Simulateur de Singularité Économique — Module 315
        </h1>
        <p className="text-yellow-300/40 text-sm mt-1">
          Déplacement IA · Transition de Phase · Concentration · Disruption — Caelum Partners
        </p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {([
          ["Total Économies",              summary.total,                                                    "text-yellow-300"],
          ["En Crise Singularité",         summary.singularity_crisis_count,                                 "text-red-400"],
          ["Requiert Intervention",        summary.singularity_intervention_count,                           "text-orange-400"],
          ["Composite Moyen",              summary.avg_singularity_composite.toFixed(1),                     "text-yellow-300"],
          ["Index Proximité Singularité",  summary.avg_estimated_singularity_proximity_index.toFixed(2),     "text-yellow-400"],
          ["Déplacement Moyen",            summary.avg_displacement_score.toFixed(1),                        "text-amber-400"],
        ] as [string, string | number, string][]).map(([l, v, c]) => (
          <div key={String(l)} className="bg-slate-950 border border-yellow-600/30 rounded-xl p-3 text-center">
            <div className={`text-xl font-bold ${c}`}>{v}</div>
            <div className="text-xs text-yellow-300/30 mt-0.5 leading-tight">{l}</div>
          </div>
        ))}
      </div>

      {/* Gauge Rings */}
      <div className="bg-slate-950 border border-yellow-600/30 rounded-xl p-5">
        <div className="grid grid-cols-4 gap-4">
          <GaugeRing value={summary.avg_displacement_score}   label="Déplacement IA"   color="#f97316" />
          <GaugeRing value={summary.avg_transition_score}     label="Transition"        color="#eab308" />
          <GaugeRing value={summary.avg_concentration_score}  label="Concentration"     color="#f59e0b" />
          <GaugeRing value={summary.avg_disruption_score}     label="Disruption"        color="#ef4444" />
        </div>
      </div>

      {/* Distribution Bars */}
      <div className="bg-slate-950 border border-yellow-600/30 rounded-xl p-5 grid grid-cols-1 md:grid-cols-2 gap-5">
        {dists.map(d => <DistBar key={d.title} {...d} />)}
      </div>

      {/* Filter Pills */}
      <div className="flex flex-wrap gap-2">
        {["all", "low", "moderate", "high", "critical"].map(r => (
          <button
            key={r}
            onClick={() => setFilter(r)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${
              filter === r
                ? "bg-yellow-700 border-yellow-600 text-white"
                : "bg-slate-950 border-yellow-600/30 text-yellow-300/60 hover:text-yellow-300"
            }`}
          >
            {r}
          </button>
        ))}
        <span className="w-px h-5 self-center bg-yellow-600/30" />
        {["all", "none", "singularity_threshold_breach", "labor_extinction_event", "capital_hypercentralization", "institutional_collapse", "social_contract_rupture"].map(p => (
          <button
            key={p}
            onClick={() => setPat(p)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${
              patFilter === p
                ? "bg-amber-900 border-amber-700 text-white"
                : "bg-slate-950 border-yellow-600/30 text-yellow-300/60 hover:text-yellow-300"
            }`}
          >
            {p.replace(/_/g, " ")}
          </button>
        ))}
      </div>

      {/* Entity Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {filtered.map(e => (
          <div
            key={e.entity_id}
            onClick={() => setSelected(e)}
            className="bg-slate-950 border border-yellow-600/30 rounded-xl p-4 cursor-pointer hover:border-yellow-400 transition-colors"
          >
            <div className="flex items-center justify-between mb-1">
              <span className="font-bold text-yellow-300">{e.entity_id}</span>
              <span className="text-xs text-yellow-300/40">{e.region}</span>
            </div>
            <div className="text-xs text-yellow-300/50 mb-2 capitalize">{e.economy_type.replace(/_/g, " ")}</div>
            <div className="flex gap-1 mb-3 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[e.singularity_risk] || "bg-slate-700 text-slate-300"}`}>
                {e.singularity_risk}
              </span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[e.singularity_severity] || "bg-slate-700 text-slate-300"}`}>
                {e.singularity_severity.replace(/_/g, " ")}
              </span>
            </div>
            <div className="text-2xl font-black text-yellow-300 mb-1">{e.singularity_composite.toFixed(1)}</div>
            <div className="text-xs text-yellow-300/40 mb-2 capitalize">{e.singularity_pattern.replace(/_/g, " ")}</div>
            <div className="text-xs text-amber-400 font-medium mb-2">
              Déplacement: {e.displacement_score.toFixed(1)}
            </div>
            <div className="flex gap-1 flex-wrap">
              {e.is_singularity_crisis && (
                <span className="px-1.5 py-0.5 rounded bg-red-950 text-red-400 text-xs font-medium">
                  SINGULARITÉ IMMINENTE
                </span>
              )}
              {e.requires_singularity_intervention && !e.is_singularity_crisis && (
                <span className="px-1.5 py-0.5 rounded bg-yellow-950 text-yellow-400 text-xs font-medium">
                  INTERVENTION
                </span>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
