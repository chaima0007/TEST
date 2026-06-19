"use client";
import { useEffect, useState } from "react";

type HydroEntity = {
  entity_id: string; region: string; basin_type: string;
  hydro_risk: string; hydro_pattern: string;
  hydro_severity: string; recommended_action: string;
  stress_score: number; conflict_score: number;
  demand_score: number; infrastructure_score: number;
  hydro_composite: number; is_hydro_crisis: boolean;
  requires_hydro_intervention: boolean; hydro_signal: string;
};

type Summary = {
  module: string; module_id: number;
  total_entities: number;
  critical_count: number; high_count: number;
  moderate_count: number; low_count: number;
  hydro_crisis_count: number; requires_intervention_count: number;
  avg_composite: number; avg_estimated_hydro_conflict_index: number;
  avg_stress_score: number; avg_conflict_score: number;
  avg_demand_score: number; avg_infrastructure_score: number;
  risk_counts: Record<string, number>;
  pattern_counts: Record<string, number>;
  severity_counts: Record<string, number>;
  action_counts: Record<string, number>;
};

function GaugeRing({ value, label, color }: { value: number; label: string; color: string }) {
  const r = 36; const circ = 2 * Math.PI * r;
  const fill = circ * (1 - value / 100);
  return (
    <div className="flex flex-col items-center gap-1">
      <svg width="88" height="88" viewBox="0 0 88 88">
        <circle cx="44" cy="44" r={r} fill="none" stroke="#0f172a" strokeWidth="8"/>
        <circle cx="44" cy="44" r={r} fill="none" stroke={color} strokeWidth="8"
          strokeDasharray={circ} strokeDashoffset={fill}
          strokeLinecap="round" transform="rotate(-90 44 44)"/>
        <text x="44" y="49" textAnchor="middle" fill="white" fontSize="13" fontWeight="bold">
          {Math.round(value)}
        </text>
      </svg>
      <span className="text-xs text-slate-400 text-center">{label}</span>
    </div>
  );
}

function DistBar({ title, counts, colors }: { title: string; counts: Record<string, number>; colors: Record<string, string> }) {
  const total = Object.values(counts).reduce((a, b) => a + b, 0) || 1;
  return (
    <div className="flex flex-col gap-1">
      <span className="text-xs text-slate-400 font-medium">{title}</span>
      <div className="flex h-3 rounded overflow-hidden gap-px">
        {Object.entries(counts).map(([k, v]) => (
          <div key={k} style={{ width: `${v / total * 100}%`, background: colors[k] || "#475569" }} title={`${k}: ${v}`}/>
        ))}
      </div>
      <div className="flex flex-wrap gap-x-3 gap-y-0.5">
        {Object.entries(counts).map(([k, v]) => (
          <span key={k} className="text-xs text-slate-400">
            <span style={{ color: colors[k] || "#94a3b8" }}>■</span> {k.replace(/_/g, " ")} {v}
          </span>
        ))}
      </div>
    </div>
  );
}

const RISK_COLORS = { low: "#10b981", moderate: "#f59e0b", high: "#f97316", critical: "#ef4444" };
const PAT_COLORS = {
  none: "#10b981", water_war_imminent: "#ef4444", aquifer_collapse: "#f97316",
  upstream_dam_coercion: "#a855f7", urban_water_crisis: "#f59e0b", glacial_catastrophe: "#06b6d4",
};
const SEV_COLORS = {
  water_secure: "#10b981", water_tension: "#f59e0b",
  hydro_crisis: "#f97316", water_emergency: "#ef4444",
};
const ACT_COLORS = {
  no_action: "#10b981", hydro_monitoring: "#06b6d4",
  water_resilience_program: "#f97316", diplomatic_water_intervention: "#a855f7",
  water_emergency_protocol: "#ef4444",
};

const RISK_BADGE: Record<string, string> = {
  low: "bg-emerald-900 text-emerald-300",
  moderate: "bg-amber-900 text-amber-300",
  high: "bg-orange-900 text-orange-300",
  critical: "bg-red-900 text-red-300",
};
const SEV_BADGE: Record<string, string> = {
  water_secure: "bg-emerald-900 text-emerald-300",
  water_tension: "bg-amber-900 text-amber-300",
  hydro_crisis: "bg-orange-900 text-orange-300",
  water_emergency: "bg-red-900 text-red-300",
};

function DetailModal({ entity, onClose }: { entity: HydroEntity; onClose: () => void }) {
  const [tab, setTab] = useState<"scores" | "analyse" | "actions">("scores");

  useEffect(() => {
    const h = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", h);
    return () => window.removeEventListener("keydown", h);
  }, [onClose]);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/75" onClick={onClose}>
      <div className="bg-slate-900 border border-cyan-700/30 rounded-xl w-full max-w-lg p-6 shadow-2xl" onClick={e => e.stopPropagation()}>
        <div className="flex items-center justify-between mb-4">
          <div>
            <span className="text-lg font-bold text-white">{entity.entity_id}</span>
            <span className="ml-2 text-cyan-400 text-xs">{entity.basin_type.replace(/_/g, " ")}</span>
            <span className="ml-2 text-slate-400 text-xs">{entity.region}</span>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl leading-none">✕</button>
        </div>
        <div className="flex gap-2 mb-4">
          {(["scores", "analyse", "actions"] as const).map(t => (
            <button key={t} onClick={() => setTab(t)}
              className={`px-3 py-1 rounded text-xs font-medium transition-colors ${tab === t ? "bg-cyan-700 text-white" : "bg-slate-800 text-slate-400 hover:text-white"}`}>
              {t.charAt(0).toUpperCase() + t.slice(1)}
            </button>
          ))}
        </div>

        {tab === "scores" && (
          <div className="grid grid-cols-2 gap-3 text-sm">
            {[
              ["Stress Hydrique", entity.stress_score, "#06b6d4"],
              ["Conflits",        entity.conflict_score, "#ef4444"],
              ["Demande",         entity.demand_score, "#f97316"],
              ["Infrastructure",  entity.infrastructure_score, "#a855f7"],
            ].map(([l, v, c]) => (
              <div key={String(l)} className="bg-slate-800 border border-cyan-700/20 rounded-lg p-3">
                <div className="text-slate-400 text-xs mb-1">{String(l)}</div>
                <div className="text-white font-bold text-lg">{Number(v).toFixed(1)}</div>
                <div className="h-1.5 rounded mt-1 bg-slate-700">
                  <div className="h-1.5 rounded" style={{ width: `${Math.min(Number(v), 100)}%`, background: String(c) }}/>
                </div>
              </div>
            ))}
            <div className="col-span-2 bg-slate-800 border border-cyan-700/20 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Composite Hydro</div>
              <div className="text-white font-bold text-2xl">{entity.hydro_composite.toFixed(1)}</div>
            </div>
          </div>
        )}

        {tab === "analyse" && (
          <div className="bg-slate-800 border border-cyan-700/20 rounded-lg p-4 text-sm text-slate-200 leading-relaxed">
            {entity.hydro_signal}
            <div className="mt-3 flex gap-2 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[entity.hydro_risk] || "bg-slate-700 text-slate-300"}`}>
                {entity.hydro_risk}
              </span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[entity.hydro_severity] || "bg-slate-700 text-slate-300"}`}>
                {entity.hydro_severity.replace(/_/g, " ")}
              </span>
              <span className="px-2 py-0.5 rounded text-xs font-medium bg-slate-700 text-cyan-300">
                {entity.hydro_pattern.replace(/_/g, " ")}
              </span>
            </div>
          </div>
        )}

        {tab === "actions" && (
          <div className="space-y-3 text-sm">
            <div className="bg-slate-800 border border-cyan-700/20 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Action Recommandée</div>
              <div className="text-white font-medium">{entity.recommended_action.replace(/_/g, " ")}</div>
            </div>
            <div className="bg-slate-800 border border-cyan-700/20 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Sévérité Hydrique</div>
              <div className="text-white font-medium">{entity.hydro_severity.replace(/_/g, " ")}</div>
            </div>
            <div className="flex gap-2 flex-wrap">
              {entity.is_hydro_crisis && (
                <span className="px-2 py-1 rounded bg-red-900 text-red-300 text-xs font-medium">CRISE HYDRIQUE</span>
              )}
              {entity.requires_hydro_intervention && (
                <span className="px-2 py-1 rounded bg-orange-900 text-orange-300 text-xs font-medium">INTERVENTION REQ.</span>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function WaterGeopoliticsDashboard() {
  const [data, setData]          = useState<{ entities: HydroEntity[]; summary: Summary } | null>(null);
  const [riskFilter, setRisk]    = useState<string>("all");
  const [regFilter, setReg]      = useState<string>("all");
  const [selected, setSelected]  = useState<HydroEntity | null>(null);

  useEffect(() => {
    fetch("/api/water-geopolitics-engine")
      .then(r => r.json())
      .then(setData)
      .catch(console.error);
  }, []);

  if (!data) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-cyan-400 text-lg animate-pulse">Initialisation du Moteur Géopolitique de l'Eau...</div>
    </div>
  );

  const { entities, summary } = data;

  const regions  = ["all", ...Array.from(new Set(entities.map(e => e.region)))];
  const filtered = entities.filter(e =>
    (riskFilter === "all" || e.hydro_risk === riskFilter) &&
    (regFilter  === "all" || e.region === regFilter)
  );

  const dists = [
    { title: "Risque Hydrique",        counts: summary.risk_counts,     colors: RISK_COLORS },
    { title: "Patron Hydro-Conflictuel", counts: summary.pattern_counts,  colors: PAT_COLORS  },
    { title: "Sévérité Hydrique",      counts: summary.severity_counts, colors: SEV_COLORS  },
    { title: "Action Recommandée",     counts: summary.action_counts,   colors: ACT_COLORS  },
  ] as Array<{ title: string; counts: Record<string, number>; colors: Record<string, string> }>;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-300 p-6 space-y-6">
      {selected && <DetailModal entity={selected} onClose={() => setSelected(null)}/>}

      {/* En-tête */}
      <div>
        <h1 className="text-2xl font-bold text-cyan-400">
          Géopolitique de l'Eau & Conflits Hydriques — Module 318
        </h1>
        <p className="text-slate-400 text-sm mt-1">
          Stress Hydrique · Conflits · Demande · Infrastructure — Intelligence Hydro-Géopolitique — Caelum Partners
        </p>
        <p className="text-slate-500 text-xs mt-0.5">Chaima Mhadbi — Bruxelles</p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {[
          ["Entités Analysées",      summary.total_entities,                                  "text-slate-300"],
          ["Crises Critiques",       summary.critical_count,                                  "text-red-400"],
          ["Risque Élevé",           summary.high_count,                                      "text-orange-400"],
          ["Crises Hydriques",       summary.hydro_crisis_count,                              "text-red-400"],
          ["Composite Moyen",        summary.avg_composite.toFixed(1),                        "text-cyan-400"],
          ["Indice Conflit Hydro",   summary.avg_estimated_hydro_conflict_index.toFixed(2) + "/10", "text-blue-400"],
        ].map(([l, v, c]) => (
          <div key={String(l)} className="bg-slate-900 border border-cyan-700/30 rounded-xl p-3 text-center">
            <div className={`text-xl font-bold ${c}`}>{v}</div>
            <div className="text-xs text-slate-500 mt-0.5 leading-tight">{l}</div>
          </div>
        ))}
      </div>

      {/* Gauge Rings */}
      <div className="bg-slate-900 border border-cyan-700/30 rounded-xl p-5">
        <p className="text-xs text-slate-500 mb-4 font-medium">Scores Moyens par Dimension</p>
        <div className="grid grid-cols-4 gap-4">
          <GaugeRing value={summary.avg_stress_score}        label="Stress Hydrique" color="#06b6d4"/>
          <GaugeRing value={summary.avg_conflict_score}      label="Conflits"        color="#ef4444"/>
          <GaugeRing value={summary.avg_demand_score}        label="Demande"         color="#f97316"/>
          <GaugeRing value={summary.avg_infrastructure_score} label="Infrastructure" color="#a855f7"/>
        </div>
      </div>

      {/* Distribution Bars */}
      <div className="bg-slate-900 border border-cyan-700/30 rounded-xl p-5 grid grid-cols-1 md:grid-cols-2 gap-5">
        {dists.map(d => <DistBar key={d.title} {...d}/>)}
      </div>

      {/* Filtres */}
      <div className="flex flex-wrap gap-2">
        {["all", "low", "moderate", "high", "critical"].map(r => (
          <button key={r} onClick={() => setRisk(r)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${riskFilter === r ? "bg-cyan-700 border-cyan-600 text-white" : "bg-slate-900 border-cyan-700/30 text-slate-400 hover:text-white"}`}>
            {r === "all" ? "Tous risques" : r}
          </button>
        ))}
        <span className="w-px h-5 self-center bg-cyan-700/30"/>
        {regions.map(r => (
          <button key={r} onClick={() => setReg(r)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${regFilter === r ? "bg-slate-700 border-slate-500 text-white" : "bg-slate-900 border-cyan-700/30 text-slate-400 hover:text-white"}`}>
            {r === "all" ? "Toutes régions" : r}
          </button>
        ))}
      </div>

      {/* Cartes Entités */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {filtered.map(e => (
          <div key={e.entity_id} onClick={() => setSelected(e)}
            className="bg-slate-900 border border-slate-800 rounded-xl p-4 cursor-pointer hover:border-cyan-700/50 transition-colors">
            <div className="flex items-center justify-between mb-1">
              <span className="font-bold text-white">{e.entity_id}</span>
              <span className="text-xs text-slate-400">{e.region}</span>
            </div>
            <div className="text-xs text-cyan-400 mb-2 capitalize">{e.basin_type.replace(/_/g, " ")}</div>
            <div className="flex gap-1 mb-3 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[e.hydro_risk] || "bg-slate-700 text-slate-300"}`}>
                {e.hydro_risk}
              </span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[e.hydro_severity] || "bg-slate-700 text-slate-300"}`}>
                {e.hydro_severity.replace(/_/g, " ")}
              </span>
            </div>
            <div className="text-2xl font-black text-white mb-1">{e.hydro_composite.toFixed(1)}</div>
            <div className="text-xs text-slate-500 mb-2 capitalize">{e.hydro_pattern.replace(/_/g, " ")}</div>
            <div className="text-xs text-cyan-400 font-medium mb-2">{e.recommended_action.replace(/_/g, " ")}</div>
            <div className="flex gap-1 flex-wrap">
              {e.is_hydro_crisis && (
                <span className="px-1.5 py-0.5 rounded bg-red-900 text-red-300 text-xs">CRISE</span>
              )}
              {e.requires_hydro_intervention && (
                <span className="px-1.5 py-0.5 rounded bg-orange-900 text-orange-300 text-xs">INTERVENTION</span>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
