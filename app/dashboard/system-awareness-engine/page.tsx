"use client";
import { useEffect, useState } from "react";

type Entity = {
  entity_id: string; region: string; system_category: string;
  awareness_risk: string; awareness_pattern: string;
  awareness_severity: string; recommended_action: string;
  loop_score: number; delay_score: number;
  emergence_score: number; blindspot_score: number;
  awareness_composite: number; is_system_crisis: boolean;
  requires_system_intervention: boolean; system_signal: string;
};
type Summary = {
  total_entities_analyzed: number;
  critical_count: number; high_count: number;
  moderate_count: number; low_count: number;
  crisis_count: number; intervention_required_count: number;
  avg_loop_score: number; avg_delay_score: number;
  avg_emergence_score: number; avg_blindspot_score: number;
  avg_awareness_composite: number;
  avg_estimated_system_risk_index: number;
  risk_counts: Record<string,number>;
  pattern_counts: Record<string,number>;
  severity_counts: Record<string,number>;
  action_counts: Record<string,number>;
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
      <span className="text-xs text-teal-300/70 text-center">{label}</span>
    </div>
  );
}

function DistBar({ title, counts, colors }: { title: string; counts: Record<string,number>; colors: Record<string,string> }) {
  const total = Object.values(counts).reduce((a,b)=>a+b,0)||1;
  return (
    <div className="flex flex-col gap-1">
      <span className="text-xs text-teal-300/70 font-medium">{title}</span>
      <div className="flex h-3 rounded overflow-hidden gap-px">
        {Object.entries(counts).map(([k,v])=>(
          <div key={k} style={{width:`${v/total*100}%`, background:colors[k]||"#475569"}} title={`${k}: ${v}`}/>
        ))}
      </div>
      <div className="flex flex-wrap gap-x-3 gap-y-0.5">
        {Object.entries(counts).map(([k,v])=>(
          <span key={k} className="text-xs text-teal-300/60">
            <span style={{color:colors[k]||"#94a3b8"}}>■</span> {k.replace(/_/g," ")} {v}
          </span>
        ))}
      </div>
    </div>
  );
}

const RISK_COLORS    = { low:"#10b981", moderate:"#f59e0b", high:"#f97316", critical:"#ef4444" };
const PAT_COLORS     = {
  none:"#10b981",
  runaway_reinforcing_loop:"#ef4444",
  delay_catastrophe:"#f97316",
  tipping_point_cascade:"#a855f7",
  archetype_trap:"#f59e0b",
  oscillation_death_spiral:"#06b6d4",
};
const SEV_COLORS     = {
  system_balanced:"#10b981",
  systemic_instability:"#f59e0b",
  high_systemic_risk:"#f97316",
  system_chaos:"#ef4444",
};
const ACTION_COLORS  = {
  no_action:"#10b981",
  system_monitoring:"#06b6d4",
  loop_dampening:"#f59e0b",
  leverage_point_intervention:"#f97316",
  systemic_emergency_redesign:"#ef4444",
};

const RISK_BADGE: Record<string,string> = {
  low:"bg-emerald-900 text-emerald-300",
  moderate:"bg-amber-900 text-amber-300",
  high:"bg-orange-900 text-orange-300",
  critical:"bg-red-900 text-red-300",
};
const SEV_BADGE: Record<string,string> = {
  system_balanced:"bg-emerald-900 text-emerald-300",
  systemic_instability:"bg-amber-900 text-amber-300",
  high_systemic_risk:"bg-orange-900 text-orange-300",
  system_chaos:"bg-red-900 text-red-300",
};

function DetailModal({ entity, onClose }: { entity: Entity; onClose: () => void }) {
  const [tab, setTab] = useState<"scores"|"signal"|"action">("scores");
  useEffect(()=>{
    const h = (e: KeyboardEvent) => { if (e.key==="Escape") onClose(); };
    window.addEventListener("keydown", h);
    return ()=>window.removeEventListener("keydown", h);
  },[onClose]);
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80" onClick={onClose}>
      <div className="bg-slate-950 border border-purple-700/30 rounded-xl w-full max-w-lg p-6 shadow-2xl" onClick={e=>e.stopPropagation()}>
        <div className="flex items-center justify-between mb-4">
          <div>
            <span className="text-lg font-bold text-white">{entity.entity_id}</span>
            <span className="ml-2 text-teal-400 text-xs">{entity.region}</span>
            <span className="ml-2 text-slate-500 text-xs">{entity.system_category.replace(/_/g," ")}</span>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl leading-none">✕</button>
        </div>
        <div className="flex gap-2 mb-4">
          {(["scores","signal","action"] as const).map(t=>(
            <button key={t} onClick={()=>setTab(t)}
              className={`px-3 py-1 rounded text-xs font-medium transition-colors ${tab===t?"bg-teal-800 text-white":"bg-slate-900 text-slate-400 hover:text-white"}`}>
              {t.charAt(0).toUpperCase()+t.slice(1)}
            </button>
          ))}
        </div>
        {tab==="scores" && (
          <div className="grid grid-cols-2 gap-3 text-sm">
            {[
              ["Boucles Feedback", entity.loop_score,      "#14b8a6"],
              ["Délais Système",   entity.delay_score,     "#f97316"],
              ["Émergence",        entity.emergence_score, "#a855f7"],
              ["Angles Morts",     entity.blindspot_score, "#f59e0b"],
            ].map(([l,v,c])=>(
              <div key={String(l)} className="bg-slate-900 border border-purple-700/20 rounded-lg p-3">
                <div className="text-teal-300/60 text-xs mb-1">{String(l)}</div>
                <div className="text-white font-bold text-lg">{Number(v).toFixed(1)}</div>
                <div className="h-1.5 rounded mt-1 bg-slate-800">
                  <div className="h-1.5 rounded" style={{width:`${Math.min(Number(v),100)}%`,background:String(c)}}/>
                </div>
              </div>
            ))}
            <div className="col-span-2 bg-slate-900 border border-purple-700/20 rounded-lg p-3">
              <div className="text-teal-300/60 text-xs mb-1">Composite Systémique</div>
              <div className="text-white font-bold text-2xl">{entity.awareness_composite.toFixed(1)}</div>
            </div>
          </div>
        )}
        {tab==="signal" && (
          <div className="bg-slate-900 border border-purple-700/20 rounded-lg p-4 text-sm text-slate-200 leading-relaxed">
            {entity.system_signal}
            <div className="mt-3 flex gap-2 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[entity.awareness_risk]||"bg-slate-700 text-slate-300"}`}>{entity.awareness_risk}</span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[entity.awareness_severity]||"bg-slate-700 text-slate-300"}`}>{entity.awareness_severity.replace(/_/g," ")}</span>
            </div>
          </div>
        )}
        {tab==="action" && (
          <div className="space-y-3 text-sm">
            <div className="bg-slate-900 border border-purple-700/20 rounded-lg p-3">
              <div className="text-teal-300/60 text-xs mb-1">Action Recommandée</div>
              <div className="text-white font-medium">{entity.recommended_action.replace(/_/g," ")}</div>
            </div>
            <div className="bg-slate-900 border border-purple-700/20 rounded-lg p-3">
              <div className="text-teal-300/60 text-xs mb-1">Pattern Systémique</div>
              <div className="text-white font-medium">{entity.awareness_pattern.replace(/_/g," ")}</div>
            </div>
            <div className="flex gap-2 flex-wrap">
              {entity.is_system_crisis && (
                <span className="px-2 py-1 rounded bg-red-950 text-red-300 text-xs font-medium">CHAOS SYSTÈME</span>
              )}
              {entity.requires_system_intervention && (
                <span className="px-2 py-1 rounded bg-teal-950 text-teal-400 text-xs font-medium">INTERVENTION</span>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function SystemAwarenessDashboard() {
  const [data, setData]         = useState<{ entities: Entity[]; summary: Summary }|null>(null);
  const [filter, setFilter]     = useState<string>("all");
  const [patFilter, setPat]     = useState<string>("all");
  const [selected, setSelected] = useState<Entity|null>(null);

  useEffect(()=>{
    fetch("/api/system-awareness-engine")
      .then(r=>r.json()).then(setData).catch(console.error);
  },[]);

  if (!data) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-teal-400 text-lg animate-pulse">Initialisation Moteur Conscience Systémique...</div>
    </div>
  );

  const { entities, summary } = data;
  const filtered = entities.filter(e=>
    (filter==="all" || e.awareness_risk===filter) &&
    (patFilter==="all" || e.awareness_pattern===patFilter)
  );

  const dists = [
    { title:"Niveau Risque",       counts:summary.risk_counts,     colors:RISK_COLORS    },
    { title:"Patterns Systémiques",counts:summary.pattern_counts,  colors:PAT_COLORS     },
    { title:"Sévérité",            counts:summary.severity_counts, colors:SEV_COLORS     },
    { title:"Actions",             counts:summary.action_counts,   colors:ACTION_COLORS  },
  ] as Array<{title:string;counts:Record<string,number>;colors:Record<string,string>}>;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {selected && <DetailModal entity={selected} onClose={()=>setSelected(null)}/>}

      <div>
        <h1 className="text-2xl font-bold text-teal-400">Conscience Systémique &amp; Boucles de Rétroaction — Module 316</h1>
        <p className="text-purple-400/60 text-sm mt-1">Boucles · Délais · Émergence · Angles Morts — Caelum Partners — Chaima Mhadbi, Fondatrice, Bruxelles</p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {[
          ["Total Systèmes",          summary.total_entities_analyzed,                                  "text-teal-400"],
          ["En Crise Systémique",     summary.crisis_count,                                             "text-red-400"],
          ["Requiert Intervention",   summary.intervention_required_count,                              "text-orange-400"],
          ["Composite Moyen",         summary.avg_awareness_composite.toFixed(1),                      "text-amber-300"],
          ["Index Risque Systémique", `${summary.avg_estimated_system_risk_index.toFixed(2)}/10`,       "text-purple-400"],
          ["Boucles Moyen",           `${summary.avg_loop_score.toFixed(1)}`,                          "text-teal-300"],
        ].map(([l,v,c])=>(
          <div key={String(l)} className="bg-slate-900 border border-purple-700/30 rounded-xl p-3 text-center">
            <div className={`text-xl font-bold ${c}`}>{v}</div>
            <div className="text-xs text-teal-300/40 mt-0.5 leading-tight">{l}</div>
          </div>
        ))}
      </div>

      {/* Gauge Rings */}
      <div className="bg-slate-900 border border-purple-700/30 rounded-xl p-5">
        <div className="grid grid-cols-4 gap-4">
          <GaugeRing value={summary.avg_loop_score}      label="Boucles Feedback"   color="#14b8a6"/>
          <GaugeRing value={summary.avg_delay_score}     label="Délais"             color="#f97316"/>
          <GaugeRing value={summary.avg_emergence_score} label="Émergence"          color="#a855f7"/>
          <GaugeRing value={summary.avg_blindspot_score} label="Angles Morts"       color="#f59e0b"/>
        </div>
      </div>

      {/* Distribution Bars */}
      <div className="bg-slate-900 border border-purple-700/30 rounded-xl p-5 grid grid-cols-1 md:grid-cols-2 gap-5">
        {dists.map(d=><DistBar key={d.title} {...d}/>)}
      </div>

      {/* Filter Pills */}
      <div className="flex flex-wrap gap-2">
        {["all","low","moderate","high","critical"].map(r=>(
          <button key={r} onClick={()=>setFilter(r)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${filter===r?"bg-teal-800 border-teal-700 text-white":"bg-slate-900 border-purple-700/30 text-teal-400/70 hover:text-white"}`}>
            {r}
          </button>
        ))}
        <span className="w-px h-5 self-center bg-purple-700/30"/>
        {["all","none","runaway_reinforcing_loop","delay_catastrophe","tipping_point_cascade","archetype_trap","oscillation_death_spiral"].map(p=>(
          <button key={p} onClick={()=>setPat(p)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${patFilter===p?"bg-purple-900 border-purple-800 text-white":"bg-slate-900 border-purple-700/30 text-teal-400/70 hover:text-white"}`}>
            {p.replace(/_/g," ")}
          </button>
        ))}
      </div>

      {/* Entity Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {filtered.map(e=>(
          <div key={e.entity_id} onClick={()=>setSelected(e)}
            className="bg-slate-900 border border-purple-700/30 rounded-xl p-4 cursor-pointer hover:border-teal-600 transition-colors">
            <div className="flex items-center justify-between mb-1">
              <span className="font-bold text-white">{e.entity_id}</span>
              <span className="text-xs text-teal-400/60">{e.region}</span>
            </div>
            <div className="text-xs text-slate-500 mb-2 capitalize">{e.system_category.replace(/_/g," ")}</div>
            <div className="flex gap-1 mb-3 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[e.awareness_risk]||"bg-slate-700 text-slate-300"}`}>{e.awareness_risk}</span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[e.awareness_severity]||"bg-slate-700 text-slate-300"}`}>{e.awareness_severity.replace(/_/g," ")}</span>
            </div>
            <div className="text-2xl font-black text-white mb-1">{e.awareness_composite.toFixed(1)}</div>
            <div className="text-xs text-purple-400/60 mb-2 capitalize">{e.awareness_pattern.replace(/_/g," ")}</div>
            <div className="text-xs text-teal-400 font-medium mb-2">{e.recommended_action.replace(/_/g," ")}</div>
            <div className="flex gap-1 flex-wrap">
              {e.is_system_crisis && (
                <span className="px-1.5 py-0.5 rounded bg-red-950 text-red-300 text-xs">CHAOS SYSTÈME</span>
              )}
              {e.requires_system_intervention && (
                <span className="px-1.5 py-0.5 rounded bg-teal-950 text-teal-400 text-xs">INTERVENTION</span>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
