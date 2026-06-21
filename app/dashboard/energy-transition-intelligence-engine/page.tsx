"use client";
import { useEffect, useState } from "react";

type Entity = {
  id: string;
  region: string;
  energy_sector: string;
  transition_risk: string;
  transition_pattern: string;
  transition_severity: string;
  recommended_action: string;
  fossil_score: number;
  stability_score: number;
  stranded_score: number;
  sovereignty_score: number;
  transition_composite: number;
  is_in_transition_crisis: boolean;
  requires_transition_intervention: boolean;
  transition_signal: string;
};

type Summary = {
  total: number;
  risk_counts: Record<string, number>;
  pattern_counts: Record<string, number>;
  severity_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_transition_composite: number;
  transition_crisis_count: number;
  transition_intervention_count: number;
  avg_fossil_score: number;
  avg_stability_score: number;
  avg_stranded_score: number;
  avg_sovereignty_score: number;
  avg_estimated_transition_risk_index: number;
};

function GaugeRing({ value, label, color }: { value: number; label: string; color: string }) {
  const r = 36;
  const circ = 2 * Math.PI * r;
  const fill = circ * (1 - value / 100);
  return (
    <div className="flex flex-col items-center gap-1">
      <svg width="88" height="88" viewBox="0 0 88 88">
        <circle cx="44" cy="44" r={r} fill="none" stroke="#0a1a0a" strokeWidth="8" />
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
            <span style={{ color: colors[k] || "#94a3b8" }}>■</span> {k} {v}
          </span>
        ))}
      </div>
    </div>
  );
}

const RISK_COLORS = { low: "#10b981", moderate: "#f59e0b", high: "#f97316", critical: "#ef4444" };
const PAT_COLORS = {
  none: "#10b981",
  fossil_lock_in: "#78350f",
  stranded_asset_crisis: "#dc2626",
  grid_instability: "#f97316",
  energy_poverty_trap: "#a855f7",
  mineral_sovereignty_loss: "#0ea5e9",
};
const SEV_COLORS = {
  transition_optimum: "#10b981",
  transition_stress: "#f59e0b",
  high_transition_risk: "#f97316",
  transition_emergency: "#7f1d1d",
};
const ACTION_COLORS = {
  no_action: "#10b981",
  transition_monitoring: "#06b6d4",
  transition_acceleration: "#f59e0b",
  stranded_asset_rescue: "#f97316",
  decarbonization_emergency: "#ef4444",
};

const RISK_BADGE = {
  low: "bg-emerald-900 text-emerald-300",
  moderate: "bg-amber-900 text-amber-300",
  high: "bg-orange-900 text-orange-300",
  critical: "bg-red-950 text-red-400",
};
const SEV_BADGE = {
  transition_optimum: "bg-emerald-900 text-emerald-300",
  transition_stress: "bg-amber-900 text-amber-300",
  high_transition_risk: "bg-orange-900 text-orange-300",
  transition_emergency: "bg-red-950 text-red-400",
};

function DetailModal({ entity, onClose }: { entity: Entity; onClose: () => void }) {
  const [tab, setTab] = useState<"scores" | "signal" | "action">("scores");
  useEffect(() => {
    const h = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", h);
    return () => window.removeEventListener("keydown", h);
  }, [onClose]);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80" onClick={onClose}>
      <div className="bg-slate-950 border border-yellow-500/30 rounded-xl w-full max-w-lg p-6 shadow-2xl" onClick={e => e.stopPropagation()}>
        <div className="flex items-center justify-between mb-4">
          <div>
            <span className="text-lg font-bold text-white">{entity.id}</span>
            <span className="ml-2 text-green-400 text-xs">{entity.region}</span>
            <span className="ml-2 text-slate-500 text-xs">{entity.energy_sector.replace(/_/g, " ")}</span>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl leading-none">✕</button>
        </div>
        <div className="flex gap-2 mb-4">
          {(["scores", "signal", "action"] as const).map(t => (
            <button key={t} onClick={() => setTab(t)}
              className={`px-3 py-1 rounded text-xs font-medium transition-colors ${tab === t ? "bg-green-900 text-white" : "bg-slate-900 text-slate-400 hover:text-white"}`}>
              {t.charAt(0).toUpperCase() + t.slice(1)}
            </button>
          ))}
        </div>

        {tab === "scores" && (
          <div className="grid grid-cols-2 gap-3 text-sm">
            {[
              ["Score Fossile",       entity.fossil_score,      "#ef4444"],
              ["Score Stabilité",     entity.stability_score,   "#f97316"],
              ["Score Actifs Échoués",entity.stranded_score,    "#a855f7"],
              ["Score Souveraineté",  entity.sovereignty_score, "#0ea5e9"],
            ].map(([l, v, c]) => (
              <div key={String(l)} className="bg-slate-900 border border-yellow-500/20 rounded-lg p-3">
                <div className="text-green-300/60 text-xs mb-1">{String(l)}</div>
                <div className="text-white font-bold text-lg">{Number(v).toFixed(1)}</div>
                <div className="h-1.5 rounded mt-1 bg-slate-800">
                  <div className="h-1.5 rounded" style={{ width: `${Math.min(Number(v), 100)}%`, background: String(c) }} />
                </div>
              </div>
            ))}
            <div className="col-span-2 bg-slate-900 border border-yellow-500/20 rounded-lg p-3">
              <div className="text-green-300/60 text-xs mb-1">Composite Transition</div>
              <div className="text-white font-bold text-2xl">{entity.transition_composite.toFixed(1)}</div>
            </div>
          </div>
        )}

        {tab === "signal" && (
          <div className="bg-slate-900 border border-yellow-500/20 rounded-lg p-4 text-sm text-slate-200 leading-relaxed">
            {entity.transition_signal}
            <div className="mt-3 flex gap-2 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[entity.transition_risk as keyof typeof RISK_BADGE] || "bg-slate-700 text-slate-300"}`}>
                {entity.transition_risk}
              </span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[entity.transition_severity as keyof typeof SEV_BADGE] || "bg-slate-700 text-slate-300"}`}>
                {entity.transition_severity.replace(/_/g, " ")}
              </span>
            </div>
          </div>
        )}

        {tab === "action" && (
          <div className="space-y-3 text-sm">
            <div className="bg-slate-900 border border-yellow-500/20 rounded-lg p-3">
              <div className="text-green-300/60 text-xs mb-1">Action Recommandée</div>
              <div className="text-white font-medium">{entity.recommended_action.replace(/_/g, " ")}</div>
            </div>
            <div className="bg-slate-900 border border-yellow-500/20 rounded-lg p-3">
              <div className="text-green-300/60 text-xs mb-1">Pattern de Transition</div>
              <div className="text-white font-medium capitalize">{entity.transition_pattern.replace(/_/g, " ")}</div>
            </div>
            <div className="flex gap-2 flex-wrap">
              {entity.is_in_transition_crisis && (
                <span className="px-2 py-1 rounded bg-red-950 text-red-400 text-xs font-medium">CRISE TRANSITION</span>
              )}
              {entity.requires_transition_intervention && (
                <span className="px-2 py-1 rounded bg-orange-950 text-orange-400 text-xs font-medium">INTERVENTION REQ.</span>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function EnergyTransitionDashboard() {
  const [data, setData]         = useState<{ entities: Entity[]; summary: Summary } | null>(null);
  const [filter, setFilter]     = useState<string>("all");
  const [patFilter, setPatFilter] = useState<string>("all");
  const [selected, setSelected] = useState<Entity | null>(null);

  useEffect(() => {
    fetch("/api/energy-transition-intelligence-engine")
      .then(r => r.json())
      .then(setData)
      .catch(console.error);
  }, []);

  if (!data) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-green-400 text-lg animate-pulse">Initialisation du Moteur de Transition Énergétique...</div>
    </div>
  );

  const { entities, summary } = data;
  const filtered = entities.filter(e =>
    (filter === "all" || e.transition_risk === filter) &&
    (patFilter === "all" || e.transition_pattern === patFilter)
  );

  const dists = [
    { title: "Niveau Risque",          counts: summary.risk_counts,     colors: RISK_COLORS   },
    { title: "Pattern Transition",     counts: summary.pattern_counts,  colors: PAT_COLORS    },
    { title: "Sévérité Transition",    counts: summary.severity_counts, colors: SEV_COLORS    },
    { title: "Action Recommandée",     counts: summary.action_counts,   colors: ACTION_COLORS },
  ] as Array<{ title: string; counts: Record<string, number>; colors: Record<string, string> }>;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {selected && <DetailModal entity={selected} onClose={() => setSelected(null)} />}

      <div>
        <h1 className="text-2xl font-bold text-green-400">Energy Transition Intelligence & Decarbonization Engine</h1>
        <p className="text-green-300/50 text-sm mt-1">Dépendance Fossile · Stabilité Réseau · Actifs Échoués · Souveraineté Énergétique</p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {[
          ["Entités Analysées",             summary.total,                                          "text-green-400"],
          ["Crises de Transition",          summary.transition_crisis_count,                        "text-red-400"],
          ["Interventions Requises",        summary.transition_intervention_count,                  "text-orange-400"],
          ["Composite Moy.",                summary.avg_transition_composite.toFixed(1),            "text-yellow-400"],
          ["Indice Risque Transition",      summary.avg_estimated_transition_risk_index.toFixed(2), "text-amber-400"],
          ["Score Fossile Moy.",            summary.avg_fossil_score.toFixed(1),                    "text-red-500"],
        ].map(([l, v, c]) => (
          <div key={String(l)} className="bg-slate-900 border border-yellow-500/30 rounded-xl p-3 text-center">
            <div className={`text-xl font-bold ${c}`}>{v}</div>
            <div className="text-xs text-green-300/40 mt-0.5 leading-tight">{l}</div>
          </div>
        ))}
      </div>

      {/* Gauge Rings */}
      <div className="bg-slate-900 border border-yellow-500/30 rounded-xl p-5">
        <div className="grid grid-cols-4 gap-4">
          <GaugeRing value={summary.avg_fossil_score}      label="Score Fossile Moy."       color="#ef4444" />
          <GaugeRing value={summary.avg_stability_score}   label="Score Stabilité Moy."     color="#f97316" />
          <GaugeRing value={summary.avg_stranded_score}    label="Score Actifs Échoués Moy." color="#a855f7" />
          <GaugeRing value={summary.avg_sovereignty_score} label="Score Souveraineté Moy."  color="#0ea5e9" />
        </div>
      </div>

      {/* Distribution Bars */}
      <div className="bg-slate-900 border border-yellow-500/30 rounded-xl p-5 grid grid-cols-1 md:grid-cols-2 gap-5">
        {dists.map(d => <DistBar key={d.title} {...d} />)}
      </div>

      {/* Filter Pills */}
      <div className="flex flex-wrap gap-2">
        {["all", "low", "moderate", "high", "critical"].map(r => (
          <button key={r} onClick={() => setFilter(r)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${filter === r ? "bg-green-900 border-green-700 text-white" : "bg-slate-900 border-yellow-500/30 text-green-400/70 hover:text-white"}`}>
            {r}
          </button>
        ))}
        <span className="w-px h-5 self-center bg-yellow-500/30" />
        {["all", "none", "fossil_lock_in", "stranded_asset_crisis", "grid_instability", "energy_poverty_trap", "mineral_sovereignty_loss"].map(p => (
          <button key={p} onClick={() => setPatFilter(p)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${patFilter === p ? "bg-green-950 border-green-700 text-white" : "bg-slate-900 border-yellow-500/30 text-green-400/70 hover:text-white"}`}>
            {p.replace(/_/g, " ")}
          </button>
        ))}
      </div>

      {/* Entity Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {filtered.map(e => (
          <div key={e.id} onClick={() => setSelected(e)}
            className="bg-slate-900 border border-yellow-500/30 rounded-xl p-4 cursor-pointer hover:border-green-500 transition-colors">
            <div className="flex items-center justify-between mb-1">
              <span className="font-bold text-white">{e.id}</span>
              <span className="text-xs text-green-400/60">{e.region}</span>
            </div>
            <div className="text-xs text-slate-500 mb-2 capitalize">{e.energy_sector.replace(/_/g, " ")}</div>
            <div className="flex gap-1 mb-3 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[e.transition_risk as keyof typeof RISK_BADGE] || "bg-slate-700 text-slate-300"}`}>
                {e.transition_risk}
              </span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[e.transition_severity as keyof typeof SEV_BADGE] || "bg-slate-700 text-slate-300"}`}>
                {e.transition_severity.replace(/_/g, " ")}
              </span>
            </div>
            <div className="text-2xl font-black text-white mb-1">{e.transition_composite.toFixed(1)}</div>
            <div className="text-xs text-green-400/60 mb-2 capitalize">{e.transition_pattern.replace(/_/g, " ")}</div>
            <div className="text-xs text-yellow-400 font-medium mb-2">
              Fossile: {e.fossil_score.toFixed(1)} · Stabilité: {e.stability_score.toFixed(1)}
            </div>
            <div className="flex gap-1 flex-wrap">
              {e.is_in_transition_crisis && (
                <span className="px-1.5 py-0.5 rounded bg-red-950 text-red-400 text-xs">CRISE</span>
              )}
              {e.requires_transition_intervention && (
                <span className="px-1.5 py-0.5 rounded bg-orange-950 text-orange-400 text-xs">INTERVENTION</span>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
