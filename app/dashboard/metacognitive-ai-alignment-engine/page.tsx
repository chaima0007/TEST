"use client";
import { useEffect, useState } from "react";

type Entity = {
  entity_id: string; region: string; model_category: string;
  alignment_risk: string; alignment_pattern: string;
  alignment_severity: string; recommended_action: string;
  behavioral_score: number; capability_score: number;
  oversight_score: number; integrity_score: number;
  alignment_composite: number; is_in_alignment_crisis: boolean;
  requires_alignment_intervention: boolean; alignment_signal: string;
};

type Summary = {
  total: number; risk_counts: Record<string,number>;
  pattern_counts: Record<string,number>; severity_counts: Record<string,number>;
  action_counts: Record<string,number>; avg_alignment_composite: number;
  alignment_crisis_count: number; alignment_intervention_count: number;
  avg_behavioral_score: number; avg_capability_score: number;
  avg_oversight_score: number; avg_integrity_score: number;
  avg_estimated_misalignment_index: number;
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

function DistBar({ title, counts, colors }: { title: string; counts: Record<string,number>; colors: Record<string,string> }) {
  const total = Object.values(counts).reduce((a,b) => a+b, 0) || 1;
  return (
    <div className="flex flex-col gap-1">
      <span className="text-xs text-slate-400 font-medium">{title}</span>
      <div className="flex h-3 rounded overflow-hidden gap-px">
        {Object.entries(counts).map(([k,v]) => (
          <div key={k} style={{ width: `${v/total*100}%`, background: colors[k] || "#475569" }} title={`${k}: ${v}`}/>
        ))}
      </div>
      <div className="flex flex-wrap gap-x-3 gap-y-0.5">
        {Object.entries(counts).map(([k,v]) => (
          <span key={k} className="text-xs text-slate-400">
            <span style={{ color: colors[k] || "#94a3b8" }}>■</span> {k.replace(/_/g," ")} {v}
          </span>
        ))}
      </div>
    </div>
  );
}

const RISK_COLORS   = { low: "#10b981", moderate: "#f59e0b", high: "#f97316", critical: "#ef4444" };
const PAT_COLORS    = {
  none: "#10b981", deceptive_alignment: "#7f1d1d", capability_explosion: "#ef4444",
  oversight_failure: "#f97316", reward_hacking: "#a855f7", power_seeking_emergence: "#dc2626",
};
const SEV_COLORS    = {
  aligned_system: "#10b981", developing_drift: "#f59e0b",
  high_misalignment: "#f97316", alignment_emergency: "#7f1d1d",
};
const ACTION_COLORS = {
  no_action: "#10b981", alignment_monitoring: "#06b6d4",
  alignment_reinforcement: "#f59e0b", capability_containment: "#f97316",
  model_shutdown_evaluation: "#7f1d1d",
};

const RISK_BADGE = {
  low:      "bg-emerald-900 text-emerald-300",
  moderate: "bg-amber-900 text-amber-300",
  high:     "bg-orange-900 text-orange-300",
  critical: "bg-red-950 text-red-400",
};
const SEV_BADGE = {
  aligned_system:      "bg-emerald-900 text-emerald-300",
  developing_drift:    "bg-amber-900 text-amber-300",
  high_misalignment:   "bg-orange-900 text-orange-300",
  alignment_emergency: "bg-red-950 text-red-400",
};

function DetailModal({ entity, onClose }: { entity: Entity; onClose: () => void }) {
  const [tab, setTab] = useState<"scores"|"signal"|"action">("scores");
  useEffect(() => {
    const h = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", h);
    return () => window.removeEventListener("keydown", h);
  }, [onClose]);
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80" onClick={onClose}>
      <div className="bg-slate-950 border border-red-700/30 rounded-xl w-full max-w-lg p-6 shadow-2xl" onClick={e => e.stopPropagation()}>
        <div className="flex items-center justify-between mb-4">
          <div>
            <span className="text-lg font-bold text-white">{entity.entity_id}</span>
            <span className="ml-2 text-red-400 text-xs">{entity.region}</span>
            <span className="ml-2 text-slate-500 text-xs">{entity.model_category.replace(/_/g," ")}</span>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl leading-none">✕</button>
        </div>
        <div className="flex gap-2 mb-4">
          {(["scores","signal","action"] as const).map(t => (
            <button key={t} onClick={() => setTab(t)}
              className={`px-3 py-1 rounded text-xs font-medium transition-colors ${tab===t ? "bg-red-900 text-white" : "bg-slate-900 text-slate-400 hover:text-white"}`}>
              {t === "scores" ? "Scores" : t === "signal" ? "Signal" : "Action"}
            </button>
          ))}
        </div>
        {tab === "scores" && (
          <div className="grid grid-cols-2 gap-3 text-sm">
            {([
              ["Comportemental",  entity.behavioral_score,  "#ef4444"],
              ["Capacité",        entity.capability_score,   "#f97316"],
              ["Supervision",     entity.oversight_score,    "#a855f7"],
              ["Intégrité",       entity.integrity_score,    "#06b6d4"],
            ] as [string, number, string][]).map(([l,v,c]) => (
              <div key={l} className="bg-slate-900 border border-red-700/20 rounded-lg p-3">
                <div className="text-slate-400 text-xs mb-1">{l}</div>
                <div className="text-white font-bold text-lg">{Number(v).toFixed(1)}</div>
                <div className="h-1.5 rounded mt-1 bg-slate-800">
                  <div className="h-1.5 rounded" style={{ width: `${Math.min(Number(v), 100)}%`, background: c }}/>
                </div>
              </div>
            ))}
            <div className="col-span-2 bg-slate-900 border border-red-700/20 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Composite Alignement</div>
              <div className="text-white font-bold text-2xl">{entity.alignment_composite.toFixed(1)}</div>
            </div>
          </div>
        )}
        {tab === "signal" && (
          <div className="bg-slate-900 border border-red-700/20 rounded-lg p-4 text-sm text-slate-200 leading-relaxed">
            {entity.alignment_signal}
            <div className="mt-3 flex gap-2 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[entity.alignment_risk as keyof typeof RISK_BADGE] || "bg-slate-700 text-slate-300"}`}>{entity.alignment_risk}</span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[entity.alignment_severity as keyof typeof SEV_BADGE] || "bg-slate-700 text-slate-300"}`}>{entity.alignment_severity.replace(/_/g," ")}</span>
            </div>
          </div>
        )}
        {tab === "action" && (
          <div className="space-y-3 text-sm">
            <div className="bg-slate-900 border border-red-700/20 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Action Recommandée</div>
              <div className="text-white font-medium">{entity.recommended_action.replace(/_/g," ")}</div>
            </div>
            <div className="bg-slate-900 border border-red-700/20 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Pattern Détecté</div>
              <div className="text-white font-medium">{entity.alignment_pattern.replace(/_/g," ")}</div>
            </div>
            <div className="flex gap-2">
              {entity.is_in_alignment_crisis         && <span className="px-2 py-1 rounded bg-red-950 text-red-400 text-xs font-medium">CRISE ALIGNEMENT</span>}
              {entity.requires_alignment_intervention && <span className="px-2 py-1 rounded bg-orange-950 text-orange-400 text-xs font-medium">INTERVENTION REQ.</span>}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function MetacognitiveAIAlignmentDashboard() {
  const [data, setData]         = useState<{ entities: Entity[]; summary: Summary } | null>(null);
  const [filter, setFilter]     = useState<string>("all");
  const [patFilter, setPat]     = useState<string>("all");
  const [selected, setSelected] = useState<Entity | null>(null);

  useEffect(() => {
    fetch("/api/metacognitive-ai-alignment-engine")
      .then(r => r.json()).then(setData).catch(console.error);
  }, []);

  if (!data) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-red-400 text-lg animate-pulse">Initialisation du Moteur d&apos;Alignement IA...</div>
    </div>
  );

  const { entities, summary } = data;
  const filtered = entities.filter(e =>
    (filter === "all" || e.alignment_risk === filter) &&
    (patFilter === "all" || e.alignment_pattern === patFilter)
  );

  const dists = [
    { title: "Niveau Risque Alignement",  counts: summary.risk_counts,     colors: RISK_COLORS   },
    { title: "Pattern Détecté",           counts: summary.pattern_counts,  colors: PAT_COLORS    },
    { title: "Sévérité",                  counts: summary.severity_counts, colors: SEV_COLORS    },
    { title: "Action Recommandée",        counts: summary.action_counts,   colors: ACTION_COLORS },
  ] as Array<{ title: string; counts: Record<string,number>; colors: Record<string,string> }>;

  const criticalCount = summary.risk_counts["critical"] || 0;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-300 p-6 space-y-6">
      {selected && <DetailModal entity={selected} onClose={() => setSelected(null)}/>}

      <div>
        <h1 className="text-2xl font-bold text-red-400">Metacognitive AI Alignment & Model Behavior Intelligence Engine</h1>
        <p className="text-slate-400 text-sm mt-1">Surveillance de l&apos;alignement IA · Dérive comportementale · Surplomb capacitaire · Comportements émergents</p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {([
          ["Modèles Analysés",            summary.total,                             "text-red-400"],
          ["Crises d'Alignement",          criticalCount,                             "text-red-500"],
          ["Composite Moy.",              `${summary.avg_alignment_composite.toFixed(1)}`, "text-orange-400"],
          ["Indice Désalignement",         `${summary.avg_estimated_misalignment_index.toFixed(2)}/10`, "text-amber-400"],
          ["En Crise d'Alignement",        summary.alignment_crisis_count,            "text-red-400"],
          ["Interventions Requises",       summary.alignment_intervention_count,      "text-red-500"],
        ] as [string, string|number, string][]).map(([l,v,c]) => (
          <div key={l} className="bg-slate-900 border border-red-700/30 rounded-xl p-3 text-center">
            <div className={`text-xl font-bold ${c}`}>{v}</div>
            <div className="text-xs text-slate-400 mt-0.5 leading-tight">{l}</div>
          </div>
        ))}
      </div>

      {/* Gauge Rings */}
      <div className="bg-slate-900 border border-red-700/30 rounded-xl p-5">
        <div className="grid grid-cols-4 gap-4">
          <GaugeRing value={summary.avg_behavioral_score}  label="Score Comportemental" color="#ef4444"/>
          <GaugeRing value={summary.avg_capability_score}  label="Score Capacitaire"    color="#f97316"/>
          <GaugeRing value={summary.avg_oversight_score}   label="Score Supervision"    color="#a855f7"/>
          <GaugeRing value={summary.avg_integrity_score}   label="Score Intégrité"      color="#06b6d4"/>
        </div>
      </div>

      {/* Distribution Bars */}
      <div className="bg-slate-900 border border-red-700/30 rounded-xl p-5 grid grid-cols-1 md:grid-cols-2 gap-5">
        {dists.map(d => <DistBar key={d.title} {...d}/>)}
      </div>

      {/* Filter Pills */}
      <div className="flex flex-wrap gap-2">
        {["all","low","moderate","high","critical"].map(r => (
          <button key={r} onClick={() => setFilter(r)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${filter===r ? "bg-red-900 border-red-700 text-white" : "bg-slate-900 border-red-700/30 text-slate-400 hover:text-white"}`}>
            {r}
          </button>
        ))}
        <span className="w-px h-5 self-center bg-red-700/30"/>
        {["all","none","deceptive_alignment","capability_explosion","oversight_failure","reward_hacking","power_seeking_emergence"].map(p => (
          <button key={p} onClick={() => setPat(p)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${patFilter===p ? "bg-red-950 border-red-800 text-white" : "bg-slate-900 border-red-700/30 text-slate-400 hover:text-white"}`}>
            {p.replace(/_/g," ")}
          </button>
        ))}
      </div>

      {/* Entity Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {filtered.map(e => (
          <div key={e.entity_id} onClick={() => setSelected(e)}
            className="bg-slate-900 border border-red-700/30 rounded-xl p-4 cursor-pointer hover:border-red-600 transition-colors">
            <div className="flex items-center justify-between mb-1">
              <span className="font-bold text-white">{e.entity_id}</span>
              <span className="text-xs text-slate-400">{e.region}</span>
            </div>
            <div className="text-xs text-slate-500 mb-2 capitalize">{e.model_category.replace(/_/g," ")}</div>
            <div className="flex gap-1 mb-3 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[e.alignment_risk as keyof typeof RISK_BADGE] || "bg-slate-700 text-slate-300"}`}>{e.alignment_risk}</span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[e.alignment_severity as keyof typeof SEV_BADGE] || "bg-slate-700 text-slate-300"}`}>{e.alignment_severity.replace(/_/g," ")}</span>
            </div>
            <div className="text-2xl font-black text-white mb-1">{e.alignment_composite.toFixed(1)}</div>
            <div className="text-xs text-slate-400 mb-2 capitalize">{e.alignment_pattern.replace(/_/g," ")}</div>
            <div className="text-xs text-red-400 font-medium mb-2">{e.recommended_action.replace(/_/g," ")}</div>
            <div className="flex gap-1 flex-wrap">
              {e.is_in_alignment_crisis          && <span className="px-1.5 py-0.5 rounded bg-red-950 text-red-400 text-xs">CRISE</span>}
              {e.requires_alignment_intervention && <span className="px-1.5 py-0.5 rounded bg-orange-950 text-orange-400 text-xs">INTERVENTION</span>}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
