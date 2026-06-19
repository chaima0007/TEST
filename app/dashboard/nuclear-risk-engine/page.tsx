"use client";
import { useEffect, useState } from "react";

type Entity = {
  entity_id: string; region: string; nuclear_domain: string;
  nuclear_risk: string; nuclear_pattern: string;
  nuclear_severity: string; recommended_action: string;
  proliferation_score: number; stability_score: number;
  security_score: number; doctrine_score: number;
  nuclear_composite: number; is_nuclear_crisis: boolean;
  requires_nuclear_intervention: boolean; nuclear_signal: string;
};
type Summary = {
  total_entities: number;
  critical_entities: number; high_entities: number;
  moderate_entities: number; low_entities: number;
  crisis_entities: number; intervention_required: number;
  avg_proliferation_score: number; avg_stability_score: number;
  avg_security_score: number; avg_doctrine_score: number;
  avg_nuclear_composite: number;
  avg_estimated_nuclear_threat_index: number;
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
      <span className="text-xs text-orange-300/70 text-center">{label}</span>
    </div>
  );
}

function DistBar({ title, counts, colors }: { title: string; counts: Record<string,number>; colors: Record<string,string> }) {
  const total = Object.values(counts).reduce((a,b)=>a+b,0)||1;
  return (
    <div className="flex flex-col gap-1">
      <span className="text-xs text-orange-300/70 font-medium">{title}</span>
      <div className="flex h-3 rounded overflow-hidden gap-px">
        {Object.entries(counts).map(([k,v])=>(
          <div key={k} style={{width:`${v/total*100}%`, background:colors[k]||"#475569"}} title={`${k}: ${v}`}/>
        ))}
      </div>
      <div className="flex flex-wrap gap-x-3 gap-y-0.5">
        {Object.entries(counts).map(([k,v])=>(
          <span key={k} className="text-xs text-orange-300/60">
            <span style={{color:colors[k]||"#94a3b8"}}>■</span> {k.replace(/_/g," ")} {v}
          </span>
        ))}
      </div>
    </div>
  );
}

const RISK_COLORS   = { low:"#10b981", moderate:"#f59e0b", high:"#f97316", critical:"#ef4444" };
const PAT_COLORS    = {
  none:"#10b981",
  proliferation_cascade:"#ef4444",
  deterrence_breakdown:"#f97316",
  nuclear_terrorism_event:"#a855f7",
  doctrine_escalation:"#f59e0b",
  arms_control_collapse:"#06b6d4",
};
const SEV_COLORS    = {
  nuclear_stable:"#10b981",
  nuclear_tension:"#f59e0b",
  high_nuclear_risk:"#f97316",
  existential_threat:"#ef4444",
};
const ACTION_COLORS = {
  no_action:"#10b981",
  nuclear_monitoring:"#06b6d4",
  nonproliferation_activation:"#f59e0b",
  nuclear_security_emergency:"#a855f7",
  existential_risk_protocol:"#ef4444",
};

const RISK_BADGE: Record<string,string> = {
  low:"bg-emerald-900 text-emerald-300",
  moderate:"bg-amber-900 text-amber-300",
  high:"bg-orange-900 text-orange-300",
  critical:"bg-red-900 text-red-300",
};
const SEV_BADGE: Record<string,string> = {
  nuclear_stable:"bg-emerald-900 text-emerald-300",
  nuclear_tension:"bg-amber-900 text-amber-300",
  high_nuclear_risk:"bg-orange-900 text-orange-300",
  existential_threat:"bg-red-900 text-red-300",
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
      <div className="bg-slate-950 border border-orange-700/30 rounded-xl w-full max-w-lg p-6 shadow-2xl" onClick={e=>e.stopPropagation()}>
        <div className="flex items-center justify-between mb-4">
          <div>
            <span className="text-lg font-bold text-white">{entity.entity_id}</span>
            <span className="ml-2 text-orange-400 text-xs">{entity.region}</span>
            <span className="ml-2 text-slate-500 text-xs">{entity.nuclear_domain.replace(/_/g," ")}</span>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl leading-none">✕</button>
        </div>
        <div className="flex gap-2 mb-4">
          {(["scores","signal","action"] as const).map(t=>(
            <button key={t} onClick={()=>setTab(t)}
              className={`px-3 py-1 rounded text-xs font-medium transition-colors ${tab===t?"bg-orange-800 text-white":"bg-slate-900 text-slate-400 hover:text-white"}`}>
              {t.charAt(0).toUpperCase()+t.slice(1)}
            </button>
          ))}
        </div>
        {tab==="scores" && (
          <div className="grid grid-cols-2 gap-3 text-sm">
            {[
              ["Prolifération",  entity.proliferation_score, "#ef4444"],
              ["Stabilité",      entity.stability_score,     "#f97316"],
              ["Sécurité",       entity.security_score,      "#a855f7"],
              ["Doctrine",       entity.doctrine_score,      "#f59e0b"],
            ].map(([l,v,c])=>(
              <div key={String(l)} className="bg-slate-900 border border-orange-700/20 rounded-lg p-3">
                <div className="text-orange-300/60 text-xs mb-1">{String(l)}</div>
                <div className="text-white font-bold text-lg">{Number(v).toFixed(1)}</div>
                <div className="h-1.5 rounded mt-1 bg-slate-800">
                  <div className="h-1.5 rounded" style={{width:`${Math.min(Number(v),100)}%`,background:String(c)}}/>
                </div>
              </div>
            ))}
            <div className="col-span-2 bg-slate-900 border border-orange-700/20 rounded-lg p-3">
              <div className="text-orange-300/60 text-xs mb-1">Composite Nucléaire</div>
              <div className="text-white font-bold text-2xl">{entity.nuclear_composite.toFixed(1)}</div>
            </div>
          </div>
        )}
        {tab==="signal" && (
          <div className="bg-slate-900 border border-orange-700/20 rounded-lg p-4 text-sm text-slate-200 leading-relaxed">
            {entity.nuclear_signal}
            <div className="mt-3 flex gap-2 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[entity.nuclear_risk]||"bg-slate-700 text-slate-300"}`}>{entity.nuclear_risk}</span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[entity.nuclear_severity]||"bg-slate-700 text-slate-300"}`}>{entity.nuclear_severity.replace(/_/g," ")}</span>
            </div>
          </div>
        )}
        {tab==="action" && (
          <div className="space-y-3 text-sm">
            <div className="bg-slate-900 border border-orange-700/20 rounded-lg p-3">
              <div className="text-orange-300/60 text-xs mb-1">Action Recommandée</div>
              <div className="text-white font-medium">{entity.recommended_action.replace(/_/g," ")}</div>
            </div>
            <div className="bg-slate-900 border border-orange-700/20 rounded-lg p-3">
              <div className="text-orange-300/60 text-xs mb-1">Pattern Nucléaire</div>
              <div className="text-white font-medium">{entity.nuclear_pattern.replace(/_/g," ")}</div>
            </div>
            <div className="flex gap-2 flex-wrap">
              {entity.is_nuclear_crisis && (
                <span className="px-2 py-1 rounded bg-red-950 text-red-300 text-xs font-medium">CRISE NUCLÉAIRE</span>
              )}
              {entity.requires_nuclear_intervention && (
                <span className="px-2 py-1 rounded bg-orange-950 text-orange-400 text-xs font-medium">INTERVENTION</span>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function NuclearRiskDashboard() {
  const [data, setData]         = useState<{ entities: Entity[]; summary: Summary }|null>(null);
  const [filter, setFilter]     = useState<string>("all");
  const [patFilter, setPat]     = useState<string>("all");
  const [selected, setSelected] = useState<Entity|null>(null);

  useEffect(()=>{
    fetch("/api/nuclear-risk-engine")
      .then(r=>r.json()).then(setData).catch(console.error);
  },[]);

  if (!data) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-orange-400 text-lg animate-pulse">Initialisation Moteur Risque Nucléaire...</div>
    </div>
  );

  const { entities, summary } = data;
  const filtered = entities.filter(e=>
    (filter==="all" || e.nuclear_risk===filter) &&
    (patFilter==="all" || e.nuclear_pattern===patFilter)
  );

  const dists = [
    { title:"Niveau Risque",         counts:summary.risk_counts,     colors:RISK_COLORS   },
    { title:"Patterns Nucléaires",   counts:summary.pattern_counts,  colors:PAT_COLORS    },
    { title:"Sévérité",              counts:summary.severity_counts, colors:SEV_COLORS    },
    { title:"Actions",               counts:summary.action_counts,   colors:ACTION_COLORS },
  ] as Array<{title:string;counts:Record<string,number>;colors:Record<string,string>}>;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {selected && <DetailModal entity={selected} onClose={()=>setSelected(null)}/>}

      <div>
        <h1 className="text-2xl font-bold text-orange-400">Risque Nucléaire &amp; Prolifération — Module 326</h1>
        <p className="text-slate-500 text-sm mt-1">Prolifération · Stabilité · Sécurité · Doctrine — Caelum Partners — Chaima Mhadbi, Fondatrice, Bruxelles</p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {[
          ["Total Entités",              summary.total_entities,                                        "text-orange-400"],
          ["Critiques",                  summary.critical_entities,                                     "text-red-400"],
          ["Élevés",                     summary.high_entities,                                         "text-orange-300"],
          ["Modérés / Faibles",          `${summary.moderate_entities}/${summary.low_entities}`,        "text-amber-300"],
          ["Crises Nucléaires",          summary.crisis_entities,                                       "text-red-500"],
          ["Intervention Requise",       summary.intervention_required,                                 "text-orange-500"],
        ].map(([l,v,c])=>(
          <div key={String(l)} className="bg-slate-900 border border-slate-600/30 rounded-xl p-3 text-center">
            <div className={`text-xl font-bold ${c}`}>{v}</div>
            <div className="text-xs text-orange-300/40 mt-0.5 leading-tight">{l}</div>
          </div>
        ))}
      </div>

      {/* Gauge Rings */}
      <div className="bg-slate-900 border border-slate-600/30 rounded-xl p-5">
        <div className="grid grid-cols-4 gap-4">
          <GaugeRing value={summary.avg_proliferation_score} label="Prolifération" color="#ef4444"/>
          <GaugeRing value={summary.avg_stability_score}     label="Stabilité"     color="#f97316"/>
          <GaugeRing value={summary.avg_security_score}      label="Sécurité"      color="#a855f7"/>
          <GaugeRing value={summary.avg_doctrine_score}      label="Doctrine"      color="#f59e0b"/>
        </div>
      </div>

      {/* Distribution Bars */}
      <div className="bg-slate-900 border border-slate-600/30 rounded-xl p-5 grid grid-cols-1 md:grid-cols-2 gap-5">
        {dists.map(d=><DistBar key={d.title} {...d}/>)}
      </div>

      {/* Filter Pills */}
      <div className="flex flex-wrap gap-2">
        {["all","low","moderate","high","critical"].map(r=>(
          <button key={r} onClick={()=>setFilter(r)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${filter===r?"bg-orange-800 border-orange-700 text-white":"bg-slate-900 border-slate-600/30 text-orange-400/70 hover:text-white"}`}>
            {r}
          </button>
        ))}
        <span className="w-px h-5 self-center bg-slate-600/30"/>
        {["all","none","proliferation_cascade","deterrence_breakdown","nuclear_terrorism_event","doctrine_escalation","arms_control_collapse"].map(p=>(
          <button key={p} onClick={()=>setPat(p)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${patFilter===p?"bg-red-900 border-red-800 text-white":"bg-slate-900 border-slate-600/30 text-orange-400/70 hover:text-white"}`}>
            {p.replace(/_/g," ")}
          </button>
        ))}
      </div>

      {/* Entity Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {filtered.map(e=>(
          <div key={e.entity_id} onClick={()=>setSelected(e)}
            className="bg-slate-900 border border-slate-600/30 rounded-xl p-4 cursor-pointer hover:border-orange-600 transition-colors">
            <div className="flex items-center justify-between mb-1">
              <span className="font-bold text-white">{e.entity_id}</span>
              <span className="text-xs text-orange-400/60">{e.region}</span>
            </div>
            <div className="text-xs text-slate-500 mb-2 capitalize">{e.nuclear_domain.replace(/_/g," ")}</div>
            <div className="flex gap-1 mb-3 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[e.nuclear_risk]||"bg-slate-700 text-slate-300"}`}>{e.nuclear_risk}</span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[e.nuclear_severity]||"bg-slate-700 text-slate-300"}`}>{e.nuclear_severity.replace(/_/g," ")}</span>
            </div>
            <div className="text-2xl font-black text-white mb-1">{e.nuclear_composite.toFixed(1)}</div>
            <div className="text-xs text-orange-400/60 mb-2 capitalize">{e.nuclear_pattern.replace(/_/g," ")}</div>
            <div className="text-xs text-orange-400 font-medium mb-2">{e.recommended_action.replace(/_/g," ")}</div>
            <div className="flex gap-1 flex-wrap">
              {e.is_nuclear_crisis && (
                <span className="px-1.5 py-0.5 rounded bg-red-950 text-red-300 text-xs">CRISE NUCLÉAIRE</span>
              )}
              {e.requires_nuclear_intervention && (
                <span className="px-1.5 py-0.5 rounded bg-orange-950 text-orange-400 text-xs">INTERVENTION</span>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
