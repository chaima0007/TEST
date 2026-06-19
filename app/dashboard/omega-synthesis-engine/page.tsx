"use client";
import { useEffect, useState } from "react";

// Module 300 — OMEGA SYNTHESIS: Meta-Intelligence Convergence Engine
// Caelum Partners — Propriété exclusive de Chaima Mhadbi, Fondatrice Caelum Partners, Bruxelles.

type Entity = {
  entity_id: string; region: string; intelligence_domain: string;
  omega_risk: string; omega_pattern: string;
  omega_severity: string; recommended_action: string;
  strategic_score: number; convergence_score: number;
  resilience_score: number; sovereignty_score: number;
  omega_composite: number; is_in_omega_crisis: boolean;
  requires_omega_intervention: boolean; omega_signal: string;
};
type Summary = {
  total: number; risk_counts: Record<string,number>;
  pattern_counts: Record<string,number>; severity_counts: Record<string,number>;
  action_counts: Record<string,number>; avg_omega_composite: number;
  omega_crisis_count: number; omega_intervention_count: number;
  avg_strategic_score: number; avg_convergence_score: number;
  avg_resilience_score: number; avg_sovereignty_score: number;
  avg_estimated_omega_index: number;
};

function GaugeRing({ value, label, color }: { value: number; label: string; color: string }) {
  const r = 36; const circ = 2 * Math.PI * r;
  const fill = circ * (1 - value / 100);
  return (
    <div className="flex flex-col items-center gap-1">
      <svg width="88" height="88" viewBox="0 0 88 88">
        <circle cx="44" cy="44" r={r} fill="none" stroke="#0a0a0f" strokeWidth="8"/>
        <circle cx="44" cy="44" r={r} fill="none" stroke={color} strokeWidth="8"
          strokeDasharray={circ} strokeDashoffset={fill}
          strokeLinecap="round" transform="rotate(-90 44 44)"/>
        <text x="44" y="49" textAnchor="middle" fill="#fde047" fontSize="13" fontWeight="bold">
          {Math.round(value)}
        </text>
      </svg>
      <span className="text-xs text-yellow-300/70 text-center">{label}</span>
    </div>
  );
}

function DistBar({ title, counts, colors }: { title: string; counts: Record<string,number>; colors: Record<string,string> }) {
  const total = Object.values(counts).reduce((a,b)=>a+b,0)||1;
  return (
    <div className="flex flex-col gap-1">
      <span className="text-xs text-yellow-300/70 font-medium">{title}</span>
      <div className="flex h-3 rounded overflow-hidden gap-px">
        {Object.entries(counts).map(([k,v])=>(
          <div key={k} style={{width:`${v/total*100}%`, background:colors[k]||"#475569"}} title={`${k}: ${v}`}/>
        ))}
      </div>
      <div className="flex flex-wrap gap-x-3 gap-y-0.5">
        {Object.entries(counts).map(([k,v])=>(
          <span key={k} className="text-xs text-yellow-300/60">
            <span style={{color:colors[k]||"#94a3b8"}}>■</span> {k.replace(/_/g," ")} {v}
          </span>
        ))}
      </div>
    </div>
  );
}

const RISK_COLORS   = { low:"#10b981", moderate:"#f59e0b", high:"#f97316", critical:"#eab308" };
const PAT_COLORS    = {
  none:"#10b981",
  omega_convergence_crisis:"#7c2d12",
  technological_singularity_approach:"#a855f7",
  civilizational_inflection:"#eab308",
  sovereignty_erosion_cascade:"#ef4444",
  strategic_intelligence_gap:"#f97316",
};
const SEV_COLORS    = {
  omega_equilibrium:"#10b981",
  strategic_tension:"#f59e0b",
  high_convergence_risk:"#f97316",
  omega_emergency:"#eab308",
};
const ACT_COLORS    = {
  no_action:"#10b981",
  omega_monitoring:"#06b6d4",
  strategic_intelligence_amplification:"#f59e0b",
  convergence_war_room:"#f97316",
  omega_strategic_reset:"#eab308",
};
const RISK_BADGE: Record<string,string> = {
  low:"bg-emerald-900 text-emerald-300",
  moderate:"bg-amber-900 text-amber-300",
  high:"bg-orange-900 text-orange-300",
  critical:"bg-yellow-950 text-yellow-300 border border-yellow-500/40",
};
const SEV_BADGE: Record<string,string> = {
  omega_equilibrium:"bg-emerald-900 text-emerald-300",
  strategic_tension:"bg-amber-900 text-amber-300",
  high_convergence_risk:"bg-orange-900 text-orange-300",
  omega_emergency:"bg-yellow-950 text-yellow-300 border border-yellow-500/40",
};

function DetailModal({ entity, onClose }: { entity: Entity; onClose: () => void }) {
  const [tab, setTab] = useState<"scores"|"signal"|"action">("scores");
  useEffect(()=>{
    const h = (e: KeyboardEvent) => { if (e.key==="Escape") onClose(); };
    window.addEventListener("keydown", h);
    return ()=>window.removeEventListener("keydown",h);
  },[onClose]);
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/85" onClick={onClose}>
      <div
        className="bg-slate-950 border border-yellow-500/30 rounded-xl w-full max-w-lg p-6 shadow-2xl shadow-yellow-900/20"
        onClick={e=>e.stopPropagation()}
      >
        {/* Header */}
        <div className="flex items-center justify-between mb-4">
          <div>
            <span className="text-lg font-bold text-yellow-300">{entity.entity_id}</span>
            <span className="ml-2 text-yellow-400/60 text-xs">{entity.region}</span>
            <span className="ml-2 text-slate-500 text-xs">{entity.intelligence_domain.replace(/_/g," ")}</span>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-yellow-300 text-xl leading-none transition-colors">✕</button>
        </div>
        {/* Tabs */}
        <div className="flex gap-2 mb-4">
          {(["scores","signal","action"] as const).map(t=>(
            <button key={t} onClick={()=>setTab(t)}
              className={`px-3 py-1 rounded text-xs font-medium transition-colors ${tab===t?"bg-yellow-900/60 text-yellow-300 border border-yellow-500/40":"bg-slate-900 text-slate-400 hover:text-yellow-300"}`}>
              {t==="scores"?"Scores Omega":t==="signal"?"Signal Intelligence":"Action Stratégique"}
            </button>
          ))}
        </div>
        {/* Scores Tab */}
        {tab==="scores" && (
          <div className="grid grid-cols-2 gap-3 text-sm">
            {[
              ["Score Stratégique",    entity.strategic_score,    "#eab308"],
              ["Score Convergence",    entity.convergence_score,  "#a855f7"],
              ["Score Résilience",     entity.resilience_score,   "#f97316"],
              ["Score Souveraineté",   entity.sovereignty_score,  "#06b6d4"],
            ].map(([l,v,c])=>(
              <div key={String(l)} className="bg-slate-900 border border-yellow-500/20 rounded-lg p-3">
                <div className="text-yellow-300/60 text-xs mb-1">{String(l)}</div>
                <div className="font-bold text-lg" style={{color:String(c)}}>{Number(v).toFixed(1)}</div>
                <div className="h-1.5 rounded mt-1 bg-slate-800">
                  <div className="h-1.5 rounded transition-all" style={{width:`${Math.min(Number(v),100)}%`,background:String(c)}}/>
                </div>
              </div>
            ))}
            <div className="col-span-2 bg-slate-900 border border-yellow-500/30 rounded-lg p-3">
              <div className="text-yellow-300/60 text-xs mb-1">Composite OMEGA</div>
              <div className="text-yellow-300 font-bold text-2xl">{entity.omega_composite.toFixed(1)}</div>
              <div className="flex gap-2 mt-2">
                {entity.is_in_omega_crisis          && <span className="px-2 py-0.5 rounded bg-yellow-950 text-yellow-300 border border-yellow-500/40 text-xs font-bold">CRISE OMEGA</span>}
                {entity.requires_omega_intervention && <span className="px-2 py-0.5 rounded bg-orange-950 text-orange-300 text-xs font-medium">INTERVENTION REQ.</span>}
              </div>
            </div>
          </div>
        )}
        {/* Signal Tab */}
        {tab==="signal" && (
          <div className="bg-slate-900 border border-yellow-500/20 rounded-lg p-4 text-sm text-slate-200 leading-relaxed">
            <p className="text-yellow-100 font-medium">{entity.omega_signal}</p>
            <div className="mt-4 flex gap-2 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[entity.omega_risk]||"bg-slate-700 text-slate-300"}`}>{entity.omega_risk}</span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[entity.omega_severity]||"bg-slate-700 text-slate-300"}`}>{entity.omega_severity.replace(/_/g," ")}</span>
              <span className="px-2 py-0.5 rounded text-xs font-medium bg-slate-800 text-slate-300">{entity.omega_pattern.replace(/_/g," ")}</span>
            </div>
          </div>
        )}
        {/* Action Tab */}
        {tab==="action" && (
          <div className="space-y-3 text-sm">
            <div className="bg-slate-900 border border-yellow-500/20 rounded-lg p-3">
              <div className="text-yellow-300/60 text-xs mb-1">Action Recommandée</div>
              <div className="text-yellow-300 font-semibold capitalize">{entity.recommended_action.replace(/_/g," ")}</div>
            </div>
            <div className="bg-slate-900 border border-yellow-500/20 rounded-lg p-3">
              <div className="text-yellow-300/60 text-xs mb-1">Indice OMEGA</div>
              <div className="text-white font-bold text-xl">
                {(entity.omega_composite / 100 * 10).toFixed(2)} <span className="text-yellow-300/50 text-sm font-normal">/ 10</span>
              </div>
            </div>
            <div className="bg-slate-900 border border-yellow-500/20 rounded-lg p-3">
              <div className="text-yellow-300/60 text-xs mb-1">Domaine d'Intelligence</div>
              <div className="text-slate-200 capitalize">{entity.intelligence_domain.replace(/_/g," ")}</div>
            </div>
            <div className="flex gap-2 flex-wrap">
              {entity.is_in_omega_crisis          && <span className="px-2 py-1 rounded bg-yellow-950 border border-yellow-500/40 text-yellow-300 text-xs font-bold">CRISE OMEGA</span>}
              {entity.requires_omega_intervention && <span className="px-2 py-1 rounded bg-orange-950 text-orange-300 text-xs font-medium">INTERVENTION REQUISE</span>}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function OmegaSynthesisDashboard() {
  const [data, setData]         = useState<{ entities: Entity[]; summary: Summary }|null>(null);
  const [filter, setFilter]     = useState<string>("all");
  const [patFilter, setPat]     = useState<string>("all");
  const [selected, setSelected] = useState<Entity|null>(null);

  useEffect(()=>{
    fetch("/api/omega-synthesis-engine")
      .then(r=>r.json()).then(setData).catch(console.error);
  },[]);

  if (!data) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-yellow-400 text-lg animate-pulse tracking-widest">
        INITIALISATION OMEGA SYNTHESIS — MODULE 300 — CONVERGENCE INTELLIGENCE...
      </div>
    </div>
  );

  const { entities, summary } = data;
  const filtered = entities.filter(e=>
    (filter==="all" || e.omega_risk===filter) &&
    (patFilter==="all" || e.omega_pattern===patFilter)
  );

  const dists = [
    { title:"Niveau Risque OMEGA",        counts:summary.risk_counts,     colors:RISK_COLORS },
    { title:"Pattern de Convergence",     counts:summary.pattern_counts,  colors:PAT_COLORS  },
    { title:"Sévérité OMEGA",             counts:summary.severity_counts, colors:SEV_COLORS  },
    { title:"Action Stratégique Activée", counts:summary.action_counts,   colors:ACT_COLORS  },
  ] as Array<{title:string;counts:Record<string,number>;colors:Record<string,string>}>;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {selected && <DetailModal entity={selected} onClose={()=>setSelected(null)}/>}

      {/* Grand Title */}
      <div className="border-b border-yellow-500/20 pb-4">
        <div className="flex items-center gap-3 mb-1">
          <div className="w-2 h-8 bg-yellow-400 rounded-sm"/>
          <h1 className="text-2xl font-black text-yellow-300 tracking-wide">
            OMEGA SYNTHESIS — Intelligence Convergence Engine <span className="text-yellow-400/60 font-normal text-lg">(Module 300)</span>
          </h1>
        </div>
        <p className="text-yellow-300/40 text-sm ml-5">
          Synthèse Méta-Intelligence · Convergence Stratégique · Score Souverain Unifié · Caelum Partners
        </p>
      </div>

      {/* KPI Cards — 6 */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {[
          ["Entités Analysées",            summary.total,                                       "text-yellow-300"],
          ["Crises OMEGA Actives",         summary.omega_crisis_count,                          "text-yellow-400"],
          ["Interventions Requises",       summary.omega_intervention_count,                    "text-orange-400"],
          ["Composite OMEGA Moy.",         `${summary.avg_omega_composite.toFixed(1)}`,         "text-yellow-300"],
          ["Indice OMEGA Moy.",            `${summary.avg_estimated_omega_index.toFixed(2)}/10`,"text-amber-400"],
          ["Score Stratégique Moy.",       `${summary.avg_strategic_score.toFixed(1)}`,         "text-yellow-200"],
        ].map(([l,v,c])=>(
          <div key={String(l)} className="bg-slate-900 border border-yellow-500/30 rounded-xl p-3 text-center">
            <div className={`text-xl font-bold ${c}`}>{v}</div>
            <div className="text-xs text-yellow-300/40 mt-0.5 leading-tight">{l}</div>
          </div>
        ))}
      </div>

      {/* Gauge Rings — 4 */}
      <div className="bg-slate-900 border border-yellow-500/30 rounded-xl p-5">
        <div className="text-xs text-yellow-300/50 font-medium mb-4 uppercase tracking-widest">Scores OMEGA Moyens</div>
        <div className="grid grid-cols-4 gap-4">
          <GaugeRing value={summary.avg_strategic_score}    label="Stratégique"    color="#eab308"/>
          <GaugeRing value={summary.avg_convergence_score}  label="Convergence"    color="#a855f7"/>
          <GaugeRing value={summary.avg_resilience_score}   label="Résilience"     color="#f97316"/>
          <GaugeRing value={summary.avg_sovereignty_score}  label="Souveraineté"   color="#06b6d4"/>
        </div>
      </div>

      {/* Distribution Bars — 4 */}
      <div className="bg-slate-900 border border-yellow-500/30 rounded-xl p-5 grid grid-cols-1 md:grid-cols-2 gap-5">
        {dists.map(d=><DistBar key={d.title} {...d}/>)}
      </div>

      {/* Filter Pills — Risk */}
      <div className="flex flex-wrap gap-2 items-center">
        <span className="text-xs text-yellow-300/40 uppercase tracking-widest mr-1">Risque</span>
        {["all","low","moderate","high","critical"].map(r=>(
          <button key={r} onClick={()=>setFilter(r)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${filter===r?"bg-yellow-900/60 border-yellow-500/60 text-yellow-300":"bg-slate-900 border-yellow-500/20 text-yellow-400/60 hover:text-yellow-300"}`}>
            {r}
          </button>
        ))}
        <span className="w-px h-5 self-center bg-yellow-500/20 mx-1"/>
        <span className="text-xs text-yellow-300/40 uppercase tracking-widest mr-1">Pattern</span>
        {["all","none","omega_convergence_crisis","technological_singularity_approach","civilizational_inflection","sovereignty_erosion_cascade","strategic_intelligence_gap"].map(p=>(
          <button key={p} onClick={()=>setPat(p)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${patFilter===p?"bg-yellow-950 border-yellow-600/60 text-yellow-300":"bg-slate-900 border-yellow-500/20 text-yellow-400/60 hover:text-yellow-300"}`}>
            {p==="all"?"all":p.replace(/_/g," ")}
          </button>
        ))}
      </div>

      {/* Entity Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {filtered.map(e=>(
          <div key={e.entity_id} onClick={()=>setSelected(e)}
            className="bg-slate-900 border border-yellow-500/20 rounded-xl p-4 cursor-pointer hover:border-yellow-400/50 hover:shadow-lg hover:shadow-yellow-900/20 transition-all">
            {/* Card header */}
            <div className="flex items-center justify-between mb-1">
              <span className="font-black text-yellow-300 text-base">{e.entity_id}</span>
              <span className="text-xs text-yellow-400/50 font-medium">{e.region}</span>
            </div>
            <div className="text-xs text-slate-500 mb-2 capitalize">{e.intelligence_domain.replace(/_/g," ")}</div>
            {/* Badges */}
            <div className="flex gap-1 mb-3 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[e.omega_risk]||"bg-slate-700 text-slate-300"}`}>{e.omega_risk}</span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[e.omega_severity]||"bg-slate-700 text-slate-300"}`}>{e.omega_severity.replace(/_/g," ")}</span>
            </div>
            {/* Composite */}
            <div className="text-3xl font-black text-white mb-0.5">{e.omega_composite.toFixed(1)}</div>
            <div className="text-xs text-yellow-400/50 mb-1 capitalize">{e.omega_pattern.replace(/_/g," ")}</div>
            {/* Sub-scores mini bar */}
            <div className="grid grid-cols-4 gap-0.5 mb-2 h-1.5">
              <div className="rounded-sm" style={{background:"#eab308",opacity:e.strategic_score/100}}/>
              <div className="rounded-sm" style={{background:"#a855f7",opacity:e.convergence_score/100}}/>
              <div className="rounded-sm" style={{background:"#f97316",opacity:e.resilience_score/100}}/>
              <div className="rounded-sm" style={{background:"#06b6d4",opacity:e.sovereignty_score/100}}/>
            </div>
            {/* Omega index */}
            <div className="text-xs text-yellow-300/60 font-medium mb-2">
              Indice OMEGA: {(e.omega_composite/100*10).toFixed(2)}/10
            </div>
            {/* Alert tags */}
            <div className="flex gap-1 flex-wrap">
              {e.is_in_omega_crisis          && <span className="px-1.5 py-0.5 rounded bg-yellow-950 border border-yellow-500/40 text-yellow-300 text-xs font-bold">CRISE</span>}
              {e.requires_omega_intervention && <span className="px-1.5 py-0.5 rounded bg-orange-950 text-orange-300 text-xs">INTERVENTION</span>}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
