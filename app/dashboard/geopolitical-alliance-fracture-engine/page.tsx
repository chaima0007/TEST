"use client";
import { useEffect, useState } from "react";

type AllianceEntity = {
  id: string; region: string; alliance_type: string;
  fracture_risk: string; fracture_pattern: string;
  fracture_severity: string; recommended_action: string;
  cohesion_score: number; defection_score: number;
  trust_score: number; legitimacy_score: number;
  fracture_composite: number; is_fracture_crisis: boolean;
  requires_fracture_intervention: boolean; fracture_signal: string;
};

type Summary = {
  module: string; engine: string; analyst: string; location: string;
  total_entities_analyzed: number;
  critical_fractures: number; high_fractures: number;
  moderate_fractures: number; stable_alliances: number;
  avg_estimated_fracture_index: number;
  fracture_crisis_entities: string[];
  dominant_fracture_pattern: string;
  risk_counts: Record<string, number>;
  pattern_counts: Record<string, number>;
  severity_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_cohesion_score: number; avg_defection_score: number;
  avg_trust_score: number; avg_legitimacy_score: number;
  avg_fracture_composite: number;
  fracture_crisis_count: number; requires_intervention_count: number;
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

const RISK_COLORS    = { low: "#10b981", moderate: "#f59e0b", high: "#f97316", critical: "#ef4444" };
const PAT_COLORS     = {
  none: "#10b981", alliance_dissolution: "#ef4444", strategic_pivot: "#f97316",
  trust_collapse: "#a855f7", populist_defection: "#f59e0b", economic_fracture: "#06b6d4",
};
const SEV_COLORS     = {
  alliance_stable: "#10b981", fracture_developing: "#f59e0b",
  high_fracture_risk: "#f97316", alliance_emergency: "#ef4444",
};
const ACT_COLORS     = {
  no_action: "#10b981", alliance_monitoring: "#06b6d4",
  cohesion_reinforcement: "#f97316", realignment_containment: "#a855f7",
  alliance_emergency_summit: "#ef4444",
};

const RISK_BADGE = {
  low: "bg-emerald-900 text-emerald-300",
  moderate: "bg-amber-900 text-amber-300",
  high: "bg-orange-900 text-orange-300",
  critical: "bg-red-900 text-red-300",
};
const SEV_BADGE = {
  alliance_stable: "bg-emerald-900 text-emerald-300",
  fracture_developing: "bg-amber-900 text-amber-300",
  high_fracture_risk: "bg-orange-900 text-orange-300",
  alliance_emergency: "bg-red-900 text-red-300",
};

function DetailModal({ entity, onClose }: { entity: AllianceEntity; onClose: () => void }) {
  const [tab, setTab] = useState<"scores" | "analyse" | "actions">("scores");

  useEffect(() => {
    const h = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", h);
    return () => window.removeEventListener("keydown", h);
  }, [onClose]);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/75" onClick={onClose}>
      <div className="bg-slate-900 border border-red-700/30 rounded-xl w-full max-w-lg p-6 shadow-2xl" onClick={e => e.stopPropagation()}>
        <div className="flex items-center justify-between mb-4">
          <div>
            <span className="text-lg font-bold text-white">{entity.id}</span>
            <span className="ml-2 text-red-400 text-xs">{entity.alliance_type.replace(/_/g, " ")}</span>
            <span className="ml-2 text-slate-400 text-xs">{entity.region}</span>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl leading-none">✕</button>
        </div>
        <div className="flex gap-2 mb-4">
          {(["scores", "analyse", "actions"] as const).map(t => (
            <button key={t} onClick={() => setTab(t)}
              className={`px-3 py-1 rounded text-xs font-medium transition-colors ${tab === t ? "bg-red-700 text-white" : "bg-slate-800 text-slate-400 hover:text-white"}`}>
              {t.charAt(0).toUpperCase() + t.slice(1)}
            </button>
          ))}
        </div>

        {tab === "scores" && (
          <div className="grid grid-cols-2 gap-3 text-sm">
            {[
              ["Cohésion",   entity.cohesion_score,   "#ef4444"],
              ["Défection",  entity.defection_score,  "#f97316"],
              ["Confiance",  entity.trust_score,      "#a855f7"],
              ["Légitimité", entity.legitimacy_score, "#f59e0b"],
            ].map(([l, v, c]) => (
              <div key={String(l)} className="bg-slate-800 border border-red-700/20 rounded-lg p-3">
                <div className="text-slate-400 text-xs mb-1">{String(l)}</div>
                <div className="text-white font-bold text-lg">{Number(v).toFixed(1)}</div>
                <div className="h-1.5 rounded mt-1 bg-slate-700">
                  <div className="h-1.5 rounded" style={{ width: `${Math.min(Number(v), 100)}%`, background: String(c) }}/>
                </div>
              </div>
            ))}
            <div className="col-span-2 bg-slate-800 border border-red-700/20 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Composite Fracture</div>
              <div className="text-white font-bold text-2xl">{entity.fracture_composite.toFixed(1)}</div>
            </div>
          </div>
        )}

        {tab === "analyse" && (
          <div className="bg-slate-800 border border-red-700/20 rounded-lg p-4 text-sm text-slate-200 leading-relaxed">
            {entity.fracture_signal}
            <div className="mt-3 flex gap-2 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[entity.fracture_risk as keyof typeof RISK_BADGE] || "bg-slate-700 text-slate-300"}`}>
                {entity.fracture_risk}
              </span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[entity.fracture_severity as keyof typeof SEV_BADGE] || "bg-slate-700 text-slate-300"}`}>
                {entity.fracture_severity.replace(/_/g, " ")}
              </span>
              <span className="px-2 py-0.5 rounded text-xs font-medium bg-slate-700 text-red-300">
                {entity.fracture_pattern.replace(/_/g, " ")}
              </span>
            </div>
          </div>
        )}

        {tab === "actions" && (
          <div className="space-y-3 text-sm">
            <div className="bg-slate-800 border border-red-700/20 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Action Recommandée</div>
              <div className="text-white font-medium">{entity.recommended_action.replace(/_/g, " ")}</div>
            </div>
            <div className="bg-slate-800 border border-red-700/20 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Sévérité Fracture</div>
              <div className="text-white font-medium">{entity.fracture_severity.replace(/_/g, " ")}</div>
            </div>
            <div className="flex gap-2 flex-wrap">
              {entity.is_fracture_crisis && (
                <span className="px-2 py-1 rounded bg-red-900 text-red-300 text-xs font-medium">CRISE FRACTURE</span>
              )}
              {entity.requires_fracture_intervention && (
                <span className="px-2 py-1 rounded bg-orange-900 text-orange-300 text-xs font-medium">INTERVENTION REQ.</span>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function GeopoliticalAllianceFractureDashboard() {
  const [data, setData]         = useState<{ entities: AllianceEntity[]; summary: Summary } | null>(null);
  const [riskFilter, setRisk]   = useState<string>("all");
  const [regFilter, setReg]     = useState<string>("all");
  const [selected, setSelected] = useState<AllianceEntity | null>(null);

  useEffect(() => {
    fetch("/api/geopolitical-alliance-fracture-engine")
      .then(r => r.json())
      .then(setData)
      .catch(console.error);
  }, []);

  if (!data) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-red-400 text-lg animate-pulse">Initialisation du Moteur Fracture Alliance Géopolitique...</div>
    </div>
  );

  const { entities, summary } = data;

  const regions  = ["all", ...Array.from(new Set(entities.map(e => e.region)))];
  const filtered = entities.filter(e =>
    (riskFilter === "all" || e.fracture_risk === riskFilter) &&
    (regFilter  === "all" || e.region === regFilter)
  );

  const dists = [
    { title: "Risque de Fracture",        counts: summary.risk_counts,     colors: RISK_COLORS },
    { title: "Patron de Fracture",        counts: summary.pattern_counts,  colors: PAT_COLORS  },
    { title: "Sévérité d'Alliance",       counts: summary.severity_counts, colors: SEV_COLORS  },
    { title: "Action Recommandée",        counts: summary.action_counts,   colors: ACT_COLORS  },
  ] as Array<{ title: string; counts: Record<string, number>; colors: Record<string, string> }>;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-300 p-6 space-y-6">
      {selected && <DetailModal entity={selected} onClose={() => setSelected(null)}/>}

      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-red-400">
          Fractures d'Alliances Géopolitiques — Module 312
        </h1>
        <p className="text-slate-400 text-sm mt-1">
          Cohésion · Défection · Confiance · Légitimité — Réalignement Multipolaire — Caelum Partners
        </p>
        <p className="text-slate-500 text-xs mt-0.5">{summary.analyst} — {summary.location}</p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {[
          ["Entités Analysées",     summary.total_entities_analyzed,             "text-slate-300"],
          ["Fractures Critiques",   summary.critical_fractures,                  "text-red-400"],
          ["Risque Élevé",          summary.high_fractures,                      "text-orange-400"],
          ["Risque Modéré",         summary.moderate_fractures,                  "text-amber-400"],
          ["Alliances Stables",     summary.stable_alliances,                    "text-emerald-400"],
          ["Indice Fracture Moy.",  summary.avg_estimated_fracture_index.toFixed(2) + "/10", "text-red-400"],
        ].map(([l, v, c]) => (
          <div key={String(l)} className="bg-slate-900 border border-red-700/30 rounded-xl p-3 text-center">
            <div className={`text-xl font-bold ${c}`}>{v}</div>
            <div className="text-xs text-slate-500 mt-0.5 leading-tight">{l}</div>
          </div>
        ))}
      </div>

      {/* Gauge Rings */}
      <div className="bg-slate-900 border border-red-700/30 rounded-xl p-5">
        <p className="text-xs text-slate-500 mb-4 font-medium">Scores Moyens par Dimension</p>
        <div className="grid grid-cols-4 gap-4">
          <GaugeRing value={summary.avg_cohesion_score}   label="Cohésion"   color="#ef4444"/>
          <GaugeRing value={summary.avg_defection_score}  label="Défection"  color="#f97316"/>
          <GaugeRing value={summary.avg_trust_score}      label="Confiance"  color="#a855f7"/>
          <GaugeRing value={summary.avg_legitimacy_score} label="Légitimité" color="#f59e0b"/>
        </div>
      </div>

      {/* Distribution Bars */}
      <div className="bg-slate-900 border border-red-700/30 rounded-xl p-5 grid grid-cols-1 md:grid-cols-2 gap-5">
        {dists.map(d => <DistBar key={d.title} {...d}/>)}
      </div>

      {/* Filter Pills */}
      <div className="flex flex-wrap gap-2">
        {["all", "low", "moderate", "high", "critical"].map(r => (
          <button key={r} onClick={() => setRisk(r)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${riskFilter === r ? "bg-red-700 border-red-600 text-white" : "bg-slate-900 border-red-700/30 text-slate-400 hover:text-white"}`}>
            {r === "all" ? "Tous risques" : r}
          </button>
        ))}
        <span className="w-px h-5 self-center bg-red-700/30"/>
        {regions.map(r => (
          <button key={r} onClick={() => setReg(r)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${regFilter === r ? "bg-slate-700 border-slate-500 text-white" : "bg-slate-900 border-red-700/30 text-slate-400 hover:text-white"}`}>
            {r === "all" ? "Toutes régions" : r}
          </button>
        ))}
      </div>

      {/* Entity Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {filtered.map(e => (
          <div key={e.id} onClick={() => setSelected(e)}
            className="bg-slate-900 border border-slate-800 rounded-xl p-4 cursor-pointer hover:border-red-700/50 transition-colors">
            <div className="flex items-center justify-between mb-1">
              <span className="font-bold text-white">{e.id}</span>
              <span className="text-xs text-slate-400">{e.region}</span>
            </div>
            <div className="text-xs text-red-400 mb-2 capitalize">{e.alliance_type.replace(/_/g, " ")}</div>
            <div className="flex gap-1 mb-3 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[e.fracture_risk as keyof typeof RISK_BADGE] || "bg-slate-700 text-slate-300"}`}>
                {e.fracture_risk}
              </span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[e.fracture_severity as keyof typeof SEV_BADGE] || "bg-slate-700 text-slate-300"}`}>
                {e.fracture_severity.replace(/_/g, " ")}
              </span>
            </div>
            <div className="text-2xl font-black text-white mb-1">{e.fracture_composite.toFixed(1)}</div>
            <div className="text-xs text-slate-500 mb-2 capitalize">{e.fracture_pattern.replace(/_/g, " ")}</div>
            <div className="text-xs text-red-400 font-medium mb-2">{e.recommended_action.replace(/_/g, " ")}</div>
            <div className="flex gap-1 flex-wrap">
              {e.is_fracture_crisis && (
                <span className="px-1.5 py-0.5 rounded bg-red-900 text-red-300 text-xs">CRISE</span>
              )}
              {e.requires_fracture_intervention && (
                <span className="px-1.5 py-0.5 rounded bg-orange-900 text-orange-300 text-xs">INTERVENTION</span>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
