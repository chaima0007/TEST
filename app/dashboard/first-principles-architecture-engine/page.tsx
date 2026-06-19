"use client";
import { useEffect, useState } from "react";

type EntityResult = {
  entity_id: string;
  domain_type: string;
  region: string;
  principles_risk: string;
  principles_pattern: string;
  principles_severity: string;
  recommended_action: string;
  assumption_score: number;
  rigidity_score: number;
  blindspot_score: number;
  innovation_score: number;
  principles_composite: number;
  is_principles_crisis: boolean;
  requires_principles_intervention: boolean;
  principles_signal: string;
};

type ApiData = {
  entity_results: EntityResult[];
  total_entities_analyzed: number;
  critical_principles_risk: number;
  high_principles_risk: number;
  moderate_principles_risk: number;
  low_principles_risk: number;
  principles_crises_detected: number;
  requires_intervention_count: number;
  avg_assumption_score: number;
  avg_rigidity_score: number;
  avg_blindspot_score: number;
  avg_innovation_score: number;
  avg_estimated_principles_weakness_index: number;
};

function GaugeRing({ value, label, color }: { value: number; label: string; color: string }) {
  const r = 36; const circ = 2 * Math.PI * r;
  const fill = circ * (1 - value / 100);
  return (
    <div className="flex flex-col items-center gap-1">
      <svg width="88" height="88" viewBox="0 0 88 88">
        <circle cx="44" cy="44" r={r} fill="none" stroke="#1e293b" strokeWidth="8"/>
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
  const total = Object.values(counts).reduce((a,b)=>a+b,0)||1;
  return (
    <div className="flex flex-col gap-1">
      <span className="text-xs text-slate-400 font-medium">{title}</span>
      <div className="flex h-3 rounded overflow-hidden gap-px">
        {Object.entries(counts).map(([k,v])=>(
          <div key={k} style={{width:`${v/total*100}%`, background:colors[k]||"#475569"}} title={`${k}: ${v}`}/>
        ))}
      </div>
      <div className="flex flex-wrap gap-x-3 gap-y-0.5">
        {Object.entries(counts).map(([k,v])=>(
          <span key={k} className="text-xs text-slate-400">
            <span style={{color:colors[k]||"#94a3b8"}}>■</span> {k} {v}
          </span>
        ))}
      </div>
    </div>
  );
}

const RISK_COLORS    = { low:"#10b981", moderate:"#14b8a6", high:"#f97316", critical:"#ef4444" };
const PAT_COLORS     = { none:"#10b981", assumption_collapse:"#ef4444", epistemic_lock:"#dc2626", complexity_blindness:"#f97316", innovation_atrophy:"#6b7280", benchmark_trap:"#0d9488" };
const SEV_COLORS     = { first_principles_sound:"#10b981", assumption_accumulation:"#14b8a6", high_assumption_risk:"#f97316", systemic_blindness_crisis:"#ef4444" };
const ACT_COLORS     = { no_action:"#10b981", assumption_mapping:"#06b6d4", first_principles_review:"#14b8a6", mindset_reconstruction:"#f97316", full_assumption_audit:"#ef4444" };
const RISK_BADGE     = { low:"bg-emerald-900 text-emerald-300", moderate:"bg-teal-900 text-teal-300", high:"bg-orange-900 text-orange-300", critical:"bg-red-900 text-red-300" };
const SEV_BADGE      = { first_principles_sound:"bg-emerald-900 text-emerald-300", assumption_accumulation:"bg-teal-900 text-teal-300", high_assumption_risk:"bg-orange-900 text-orange-300", systemic_blindness_crisis:"bg-red-900 text-red-300" };

function DetailModal({ entity, onClose }: { entity: EntityResult; onClose: () => void }) {
  const [tab, setTab] = useState<"scores"|"patterns"|"signal">("scores");
  useEffect(() => {
    const h = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", h);
    return () => window.removeEventListener("keydown", h);
  }, [onClose]);
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70" onClick={onClose}>
      <div className="bg-slate-900 border border-amber-700/30 rounded-xl w-full max-w-lg p-6 shadow-2xl" onClick={e=>e.stopPropagation()}>
        <div className="flex items-center justify-between mb-4">
          <div>
            <span className="text-lg font-bold text-white">{entity.entity_id}</span>
            <span className="ml-2 text-slate-400 text-sm capitalize">{entity.domain_type.replace(/_/g," ")}</span>
            <span className="ml-2 text-indigo-400 text-xs">{entity.region}</span>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl leading-none">✕</button>
        </div>
        <div className="flex gap-2 mb-4">
          {(["scores","patterns","signal"] as const).map(t=>(
            <button key={t} onClick={()=>setTab(t)}
              className={`px-3 py-1 rounded text-xs font-medium transition-colors ${tab===t?"bg-indigo-700 text-white":"bg-slate-800 text-slate-400 hover:text-white"}`}>
              {t.charAt(0).toUpperCase()+t.slice(1)}
            </button>
          ))}
        </div>
        {tab==="scores" && (
          <div className="grid grid-cols-2 gap-3 text-sm">
            {[
              ["Hypothèses",  entity.assumption_score,  "#6366f1"],
              ["Rigidité",    entity.rigidity_score,    "#f59e0b"],
              ["Angles Morts",entity.blindspot_score,   "#f97316"],
              ["Innovation",  entity.innovation_score,  "#10b981"],
            ].map(([l,v,c])=>(
              <div key={String(l)} className="bg-slate-800 rounded-lg p-3">
                <div className="text-slate-400 text-xs mb-1">{String(l)}</div>
                <div className="text-white font-bold text-lg">{Number(v).toFixed(1)}</div>
                <div className="h-1.5 rounded mt-1 bg-slate-700">
                  <div className="h-1.5 rounded" style={{width:`${Math.min(Number(v),100)}%`,background:String(c)}}/>
                </div>
              </div>
            ))}
            <div className="col-span-2 bg-slate-800 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Composite Premiers Principes</div>
              <div className="text-white font-bold text-2xl">{entity.principles_composite.toFixed(1)}</div>
            </div>
          </div>
        )}
        {tab==="patterns" && (
          <div className="space-y-3 text-sm">
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Patron Détecté</div>
              <div className="text-white font-medium capitalize">{entity.principles_pattern.replace(/_/g," ")}</div>
            </div>
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Sévérité</div>
              <div className="text-white font-medium capitalize">{entity.principles_severity.replace(/_/g," ")}</div>
            </div>
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Action Recommandée</div>
              <div className="text-white font-medium capitalize">{entity.recommended_action.replace(/_/g," ")}</div>
            </div>
            <div className="flex gap-2 flex-wrap">
              {entity.is_principles_crisis              && <span className="px-2 py-1 rounded bg-red-900 text-red-300 text-xs font-medium">CRISE PRINCIPES</span>}
              {entity.requires_principles_intervention  && <span className="px-2 py-1 rounded bg-orange-900 text-orange-300 text-xs font-medium">INTERVENTION REQUISE</span>}
            </div>
          </div>
        )}
        {tab==="signal" && (
          <div className="bg-slate-800 rounded-lg p-4 text-sm text-slate-200 leading-relaxed">
            {entity.principles_signal}
            <div className="mt-3 flex gap-2 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[entity.principles_risk as keyof typeof RISK_BADGE]||"bg-slate-700 text-slate-300"}`}>{entity.principles_risk}</span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[entity.principles_severity as keyof typeof SEV_BADGE]||"bg-slate-700 text-slate-300"}`}>{entity.principles_severity.replace(/_/g," ")}</span>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function FirstPrinciplesArchitectureDashboard() {
  const [data, setData]       = useState<ApiData|null>(null);
  const [domainFilter, setDomainFilter] = useState<string>("all");
  const [selected, setSelected]         = useState<EntityResult|null>(null);

  useEffect(() => {
    fetch("/api/first-principles-architecture-engine")
      .then(r => r.json())
      .then(setData)
      .catch(console.error);
  }, []);

  if (!data) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-indigo-400 text-lg animate-pulse">Chargement Architecture Premiers Principes...</div>
    </div>
  );

  const { entity_results } = data;

  const allDomains = Array.from(new Set(entity_results.map(e => e.domain_type)));
  const filtered   = entity_results.filter(e => domainFilter === "all" || e.domain_type === domainFilter);

  const avgComposite = entity_results.reduce((s,e)=>s+e.principles_composite,0) / (entity_results.length||1);

  const riskCounts     = entity_results.reduce((acc,e)=>{ acc[e.principles_risk]=(acc[e.principles_risk]||0)+1; return acc; },{} as Record<string,number>);
  const patternCounts  = entity_results.reduce((acc,e)=>{ acc[e.principles_pattern]=(acc[e.principles_pattern]||0)+1; return acc; },{} as Record<string,number>);
  const severityCounts = entity_results.reduce((acc,e)=>{ acc[e.principles_severity]=(acc[e.principles_severity]||0)+1; return acc; },{} as Record<string,number>);
  const actionCounts   = entity_results.reduce((acc,e)=>{ acc[e.recommended_action]=(acc[e.recommended_action]||0)+1; return acc; },{} as Record<string,number>);

  const dists = [
    { title:"Risque",    counts:riskCounts,     colors:RISK_COLORS },
    { title:"Patterns",  counts:patternCounts,  colors:PAT_COLORS  },
    { title:"Sévérité",  counts:severityCounts, colors:SEV_COLORS  },
    { title:"Actions",   counts:actionCounts,   colors:ACT_COLORS  },
  ] as Array<{title:string;counts:Record<string,number>;colors:Record<string,string>}>;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {selected && <DetailModal entity={selected} onClose={()=>setSelected(null)}/>}

      <div>
        <h1 className="text-2xl font-bold text-white">Architecture Premiers Principes — Module 313</h1>
        <p className="text-slate-400 text-sm mt-1">Caelum Partners · Chaima Mhadbi, Fondatrice · Bruxelles</p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {[
          ["Total Domaines",          data.total_entities_analyzed,                                         "text-indigo-400"],
          ["En Crise Épistémique",    data.principles_crises_detected,                                      "text-red-400"],
          ["Requiert Intervention",   data.requires_intervention_count,                                     "text-orange-400"],
          ["Composite Moyen",         avgComposite.toFixed(1),                                              "text-amber-400"],
          ["Index Faiblesse Principes", data.avg_estimated_principles_weakness_index.toFixed(2),            "text-indigo-400"],
          ["Hypothèses Moyen",        data.avg_assumption_score.toFixed(1),                                 "text-teal-400"],
        ].map(([l,v,c])=>(
          <div key={String(l)} className="bg-slate-900 border border-amber-700/30 rounded-xl p-3 text-center">
            <div className={`text-xl font-bold ${c}`}>{v}</div>
            <div className="text-xs text-slate-500 mt-0.5">{l}</div>
          </div>
        ))}
      </div>

      {/* Gauge Rings */}
      <div className="bg-slate-900 border border-amber-700/30 rounded-xl p-5">
        <div className="grid grid-cols-4 gap-4">
          <GaugeRing value={data.avg_assumption_score}  label="Hypothèses"   color="#6366f1"/>
          <GaugeRing value={data.avg_rigidity_score}    label="Rigidité"     color="#f59e0b"/>
          <GaugeRing value={data.avg_blindspot_score}   label="Angles Morts" color="#f97316"/>
          <GaugeRing value={data.avg_innovation_score}  label="Innovation"   color="#10b981"/>
        </div>
      </div>

      {/* Distribution Bars */}
      <div className="bg-slate-900 border border-amber-700/30 rounded-xl p-5 grid grid-cols-1 md:grid-cols-2 gap-5">
        {dists.map(d=><DistBar key={d.title} {...d}/>)}
      </div>

      {/* Filter pills for domain_type */}
      <div className="flex flex-wrap gap-2">
        <button onClick={()=>setDomainFilter("all")}
          className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${domainFilter==="all"?"bg-indigo-700 border-indigo-600 text-white":"bg-slate-900 border-slate-700 text-slate-400 hover:text-white"}`}>
          Tous les domaines
        </button>
        {allDomains.map(d=>(
          <button key={d} onClick={()=>setDomainFilter(d)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors capitalize ${domainFilter===d?"bg-indigo-700 border-indigo-600 text-white":"bg-slate-900 border-slate-700 text-slate-400 hover:text-white hover:border-indigo-600"}`}>
            {d.replace(/_/g," ")}
          </button>
        ))}
      </div>

      {/* Entity Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {filtered.map(e=>(
          <div key={e.entity_id} onClick={()=>setSelected(e)}
            className="bg-slate-900 border border-amber-700/30 rounded-xl p-4 cursor-pointer hover:border-indigo-500 transition-colors">
            <div className="flex items-center justify-between mb-1">
              <span className="font-bold text-white">{e.entity_id}</span>
              <span className="text-xs text-slate-400">{e.region}</span>
            </div>
            <div className="text-xs text-indigo-400 mb-2 capitalize">{e.domain_type.replace(/_/g," ")}</div>
            <div className="flex gap-1 mb-3 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[e.principles_risk as keyof typeof RISK_BADGE]||"bg-slate-700 text-slate-300"}`}>{e.principles_risk}</span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[e.principles_severity as keyof typeof SEV_BADGE]||"bg-slate-700 text-slate-300"}`}>{e.principles_severity.replace(/_/g," ")}</span>
            </div>
            <div className="text-2xl font-black text-white mb-1">{e.principles_composite.toFixed(1)}</div>
            <div className="text-xs text-slate-500 mb-2 capitalize">{e.principles_pattern.replace(/_/g," ")}</div>
            <div className="text-xs text-amber-400 font-medium mb-2 capitalize">{e.recommended_action.replace(/_/g," ")}</div>
            <div className="flex gap-1 flex-wrap">
              {e.is_principles_crisis             && <span className="px-1.5 py-0.5 rounded bg-red-900 text-red-300 text-xs">CRISE</span>}
              {e.requires_principles_intervention && <span className="px-1.5 py-0.5 rounded bg-orange-900 text-orange-300 text-xs">INTERVENTION</span>}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
