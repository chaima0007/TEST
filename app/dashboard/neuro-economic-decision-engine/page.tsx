"use client";
import { useEffect, useState } from "react";

type Entity = {
  id: string; region: string; decision_domain: string;
  decision_risk: string; decision_pattern: string;
  decision_severity: string; recommended_action: string;
  cognitive_score: number; bias_score: number;
  fatigue_score: number; coherence_score: number;
  decision_composite: number; is_in_decision_crisis: boolean;
  requires_architecture_intervention: boolean; decision_signal: string;
};
type Summary = {
  total: number; risk_counts: Record<string,number>;
  pattern_counts: Record<string,number>; severity_counts: Record<string,number>;
  action_counts: Record<string,number>; avg_decision_composite: number;
  decision_crisis_count: number; architecture_intervention_count: number;
  avg_cognitive_score: number; avg_bias_score: number;
  avg_fatigue_score: number; avg_coherence_score: number;
  avg_estimated_decision_risk_index: number;
};

function GaugeRing({ value, label, color }: { value: number; label: string; color: string }) {
  const r = 36; const circ = 2 * Math.PI * r;
  const fill = circ * (1 - value / 100);
  return (
    <div className="flex flex-col items-center gap-1">
      <svg width="88" height="88" viewBox="0 0 88 88">
        <circle cx="44" cy="44" r={r} fill="none" stroke="#1a0e00" strokeWidth="8"/>
        <circle cx="44" cy="44" r={r} fill="none" stroke={color} strokeWidth="8"
          strokeDasharray={circ} strokeDashoffset={fill}
          strokeLinecap="round" transform="rotate(-90 44 44)"/>
        <text x="44" y="49" textAnchor="middle" fill="white" fontSize="13" fontWeight="bold">
          {Math.round(value)}
        </text>
      </svg>
      <span className="text-xs text-amber-300/70 text-center">{label}</span>
    </div>
  );
}

function DistBar({ title, counts, colors }: { title: string; counts: Record<string,number>; colors: Record<string,string> }) {
  const total = Object.values(counts).reduce((a,b)=>a+b,0)||1;
  return (
    <div className="flex flex-col gap-1">
      <span className="text-xs text-amber-300/70 font-medium">{title}</span>
      <div className="flex h-3 rounded overflow-hidden gap-px">
        {Object.entries(counts).map(([k,v])=>(
          <div key={k} style={{width:`${v/total*100}%`, background:colors[k]||"#475569"}} title={`${k}: ${v}`}/>
        ))}
      </div>
      <div className="flex flex-wrap gap-x-3 gap-y-0.5">
        {Object.entries(counts).map(([k,v])=>(
          <span key={k} className="text-xs text-amber-300/60">
            <span style={{color:colors[k]||"#94a3b8"}}>■</span> {k.replace(/_/g," ")} {v}
          </span>
        ))}
      </div>
    </div>
  );
}

const RISK_COLORS = { low:"#10b981", moderate:"#f59e0b", high:"#f97316", critical:"#ef4444" };
const PAT_COLORS  = {
  none:"#10b981", cognitive_overload:"#b45309", bias_cascade:"#f97316",
  emotional_hijack:"#dc2626", decision_paralysis:"#a855f7", herding_collapse:"#7c3aed",
};
const SEV_COLORS  = {
  rational_clarity:"#10b981", moderate_bias:"#f59e0b",
  high_distortion:"#f97316", severely_impaired:"#ef4444",
};
const ACT_COLORS  = {
  no_action:"#10b981", decision_monitoring:"#06b6d4",
  cognitive_augmentation:"#f59e0b", debiasing_protocol:"#f97316",
  decision_architecture_reset:"#ef4444",
};
const RISK_BADGE  = {
  low:"bg-emerald-900 text-emerald-300", moderate:"bg-amber-900 text-amber-300",
  high:"bg-orange-900 text-orange-300",  critical:"bg-red-950 text-red-400",
};
const SEV_BADGE   = {
  rational_clarity:"bg-emerald-900 text-emerald-300", moderate_bias:"bg-amber-900 text-amber-300",
  high_distortion:"bg-orange-900 text-orange-300",    severely_impaired:"bg-red-950 text-red-400",
};

function DetailModal({ entity, onClose }: { entity: Entity; onClose: () => void }) {
  const [tab, setTab] = useState<"scores"|"signal"|"action">("scores");
  useEffect(()=>{
    const h = (e: KeyboardEvent) => { if (e.key==="Escape") onClose(); };
    window.addEventListener("keydown", h);
    return ()=>window.removeEventListener("keydown",h);
  },[onClose]);
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80" onClick={onClose}>
      <div className="bg-slate-950 border border-orange-600/40 rounded-xl w-full max-w-lg p-6 shadow-2xl" onClick={e=>e.stopPropagation()}>
        <div className="flex items-center justify-between mb-4">
          <div>
            <span className="text-lg font-bold text-white">{entity.id}</span>
            <span className="ml-2 text-amber-400 text-xs">{entity.region}</span>
            <span className="ml-2 text-slate-500 text-xs">{entity.decision_domain.replace(/_/g," ")}</span>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl leading-none">✕</button>
        </div>
        <div className="flex gap-2 mb-4">
          {(["scores","signal","action"] as const).map(t=>(
            <button key={t} onClick={()=>setTab(t)}
              className={`px-3 py-1 rounded text-xs font-medium transition-colors ${tab===t?"bg-amber-900 text-white":"bg-slate-900 text-slate-400 hover:text-white"}`}>
              {t.charAt(0).toUpperCase()+t.slice(1)}
            </button>
          ))}
        </div>
        {tab==="scores" && (
          <div className="grid grid-cols-2 gap-3 text-sm">
            {[
              ["Charge Cognitive",  entity.cognitive_score,  "#f59e0b"],
              ["Score Biais",       entity.bias_score,       "#f97316"],
              ["Fatigue Décision.", entity.fatigue_score,    "#ef4444"],
              ["Cohérence",        entity.coherence_score,  "#a855f7"],
            ].map(([l,v,c])=>(
              <div key={String(l)} className="bg-slate-900 border border-orange-600/20 rounded-lg p-3">
                <div className="text-amber-300/60 text-xs mb-1">{String(l)}</div>
                <div className="text-white font-bold text-lg">{Number(v).toFixed(1)}</div>
                <div className="h-1.5 rounded mt-1 bg-slate-800">
                  <div className="h-1.5 rounded" style={{width:`${Math.min(Number(v),100)}%`,background:String(c)}}/>
                </div>
              </div>
            ))}
            <div className="col-span-2 bg-slate-900 border border-orange-600/20 rounded-lg p-3">
              <div className="text-amber-300/60 text-xs mb-1">Composite Décisionnel</div>
              <div className="text-white font-bold text-2xl">{entity.decision_composite.toFixed(1)}</div>
            </div>
          </div>
        )}
        {tab==="signal" && (
          <div className="bg-slate-900 border border-orange-600/20 rounded-lg p-4 text-sm text-slate-200 leading-relaxed">
            {entity.decision_signal}
            <div className="mt-3 flex gap-2 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[entity.decision_risk as keyof typeof RISK_BADGE]||"bg-slate-700 text-slate-300"}`}>{entity.decision_risk}</span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[entity.decision_severity as keyof typeof SEV_BADGE]||"bg-slate-700 text-slate-300"}`}>{entity.decision_severity.replace(/_/g," ")}</span>
            </div>
          </div>
        )}
        {tab==="action" && (
          <div className="space-y-3 text-sm">
            <div className="bg-slate-900 border border-orange-600/20 rounded-lg p-3">
              <div className="text-amber-300/60 text-xs mb-1">Action Recommandée</div>
              <div className="text-white font-medium">{entity.recommended_action.replace(/_/g," ")}</div>
            </div>
            <div className="bg-slate-900 border border-orange-600/20 rounded-lg p-3">
              <div className="text-amber-300/60 text-xs mb-1">Pattern Décisionnel</div>
              <div className="text-white font-medium">{entity.decision_pattern.replace(/_/g," ")}</div>
            </div>
            <div className="flex gap-2">
              {entity.is_in_decision_crisis              && <span className="px-2 py-1 rounded bg-red-950 text-red-400 text-xs font-medium">CRISE DÉCISIONNELLE</span>}
              {entity.requires_architecture_intervention && <span className="px-2 py-1 rounded bg-orange-950 text-orange-400 text-xs font-medium">INTERVENTION ARCH.</span>}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function NeuroEconomicDashboard() {
  const [data, setData]         = useState<{ entities: Entity[]; summary: Summary }|null>(null);
  const [filter, setFilter]     = useState<string>("all");
  const [patFilter, setPat]     = useState<string>("all");
  const [selected, setSelected] = useState<Entity|null>(null);

  useEffect(()=>{
    fetch("/api/neuro-economic-decision-engine")
      .then(r=>r.json()).then(setData).catch(console.error);
  },[]);

  if (!data) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-amber-400 text-lg animate-pulse">Initialisation du Moteur Neuro-Économique...</div>
    </div>
  );

  const { entities, summary } = data;
  const filtered = entities.filter(e=>
    (filter==="all" || e.decision_risk===filter) &&
    (patFilter==="all" || e.decision_pattern===patFilter)
  );

  const dists = [
    { title:"Niveau Risque Décisionnel", counts:summary.risk_counts,     colors:RISK_COLORS },
    { title:"Pattern Cognitif",          counts:summary.pattern_counts,  colors:PAT_COLORS  },
    { title:"Sévérité Décisionnelle",    counts:summary.severity_counts, colors:SEV_COLORS  },
    { title:"Action Recommandée",        counts:summary.action_counts,   colors:ACT_COLORS  },
  ] as Array<{title:string;counts:Record<string,number>;colors:Record<string,string>}>;

  const criticalCount = (summary.risk_counts["critical"]||0);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {selected && <DetailModal entity={selected} onClose={()=>setSelected(null)}/>}

      <div>
        <h1 className="text-2xl font-bold text-amber-400">Neuro-Economic Decision Architecture Engine</h1>
        <p className="text-amber-300/50 text-sm mt-1">Charge Cognitive · Biais Comportementaux · Fatigue Décisionnelle · Cohérence Rationnelle</p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {[
          ["Entités Analysées",              summary.total,                                        "text-amber-400"],
          ["Crises Décisionnelles Critiques", criticalCount,                                       "text-red-400"],
          ["Composite Décisionnel Moy.",      `${summary.avg_decision_composite.toFixed(1)}`,      "text-orange-400"],
          ["Indice Risque Décisionnel",       `${summary.avg_estimated_decision_risk_index.toFixed(2)}/10`, "text-amber-400"],
          ["En Crise Décisionnelle",          summary.decision_crisis_count,                       "text-red-400"],
          ["Interventions Architecture",      summary.architecture_intervention_count,             "text-orange-400"],
        ].map(([l,v,c])=>(
          <div key={String(l)} className="bg-slate-900 border border-orange-600/30 rounded-xl p-3 text-center">
            <div className={`text-xl font-bold ${c}`}>{v}</div>
            <div className="text-xs text-amber-300/40 mt-0.5 leading-tight">{l}</div>
          </div>
        ))}
      </div>

      {/* Gauge Rings */}
      <div className="bg-slate-900 border border-orange-600/30 rounded-xl p-5">
        <div className="grid grid-cols-4 gap-4">
          <GaugeRing value={summary.avg_cognitive_score} label="Charge Cognitive Moy."    color="#f59e0b"/>
          <GaugeRing value={summary.avg_bias_score}      label="Score Biais Moy."         color="#f97316"/>
          <GaugeRing value={summary.avg_fatigue_score}   label="Fatigue Décisionnelle Moy." color="#ef4444"/>
          <GaugeRing value={summary.avg_coherence_score} label="Incohérence Rationnelle"  color="#a855f7"/>
        </div>
      </div>

      {/* Distribution Bars */}
      <div className="bg-slate-900 border border-orange-600/30 rounded-xl p-5 grid grid-cols-1 md:grid-cols-2 gap-5">
        {dists.map(d=><DistBar key={d.title} {...d}/>)}
      </div>

      {/* Filter Pills */}
      <div className="flex flex-wrap gap-2">
        {["all","low","moderate","high","critical"].map(r=>(
          <button key={r} onClick={()=>setFilter(r)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${filter===r?"bg-amber-900 border-amber-700 text-white":"bg-slate-900 border-orange-600/30 text-amber-400/70 hover:text-white"}`}>
            {r}
          </button>
        ))}
        <span className="w-px h-5 self-center bg-orange-600/30"/>
        {["all","none","cognitive_overload","bias_cascade","emotional_hijack","decision_paralysis","herding_collapse"].map(p=>(
          <button key={p} onClick={()=>setPat(p)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${patFilter===p?"bg-orange-950 border-orange-700 text-white":"bg-slate-900 border-orange-600/30 text-amber-400/70 hover:text-white"}`}>
            {p.replace(/_/g," ")}
          </button>
        ))}
      </div>

      {/* Entity Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {filtered.map(e=>(
          <div key={e.id} onClick={()=>setSelected(e)}
            className="bg-slate-900 border border-orange-600/30 rounded-xl p-4 cursor-pointer hover:border-amber-500 transition-colors">
            <div className="flex items-center justify-between mb-1">
              <span className="font-bold text-white">{e.id}</span>
              <span className="text-xs text-amber-400/60">{e.region}</span>
            </div>
            <div className="text-xs text-slate-500 mb-2 capitalize">{e.decision_domain.replace(/_/g," ")}</div>
            <div className="flex gap-1 mb-3 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[e.decision_risk as keyof typeof RISK_BADGE]||"bg-slate-700 text-slate-300"}`}>{e.decision_risk}</span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[e.decision_severity as keyof typeof SEV_BADGE]||"bg-slate-700 text-slate-300"}`}>{e.decision_severity.replace(/_/g," ")}</span>
            </div>
            <div className="text-2xl font-black text-white mb-1">{e.decision_composite.toFixed(1)}</div>
            <div className="text-xs text-amber-400/60 mb-2 capitalize">{e.decision_pattern.replace(/_/g," ")}</div>
            <div className="text-xs text-amber-400 font-medium mb-2">{e.recommended_action.replace(/_/g," ")}</div>
            <div className="flex gap-1 flex-wrap">
              {e.is_in_decision_crisis              && <span className="px-1.5 py-0.5 rounded bg-red-950 text-red-400 text-xs">CRISE</span>}
              {e.requires_architecture_intervention && <span className="px-1.5 py-0.5 rounded bg-orange-950 text-orange-400 text-xs">INTERVENTION</span>}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
