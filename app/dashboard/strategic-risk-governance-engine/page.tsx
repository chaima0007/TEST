"use client";
import { useEffect, useState } from "react";

type Entity = {
  id: string; region: string;
  governance_risk: string; risk_pattern: string;
  governance_severity: string; recommended_action: string;
  strategic_score: number; governance_score: number;
  financial_risk_score: number; resilience_score: number;
  governance_composite: number; has_governance_alert: boolean;
  requires_board_action: boolean; estimated_strategic_risk_index: number;
  governance_signal: string;
};
type Summary = {
  total: number; risk_counts: Record<string,number>;
  pattern_counts: Record<string,number>; severity_counts: Record<string,number>;
  action_counts: Record<string,number>; avg_governance_composite: number;
  governance_alert_count: number; board_action_count: number;
  avg_strategic_score: number; avg_governance_score: number;
  avg_financial_risk_score: number; avg_resilience_score: number;
  avg_estimated_strategic_risk_index: number;
};

function Gauge({ value, label, color }: { value: number; label: string; color: string }) {
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

const RISK_COLORS = { low:"#10b981", moderate:"#f59e0b", high:"#f97316", critical:"#ef4444" };
const PAT_COLORS  = { none:"#10b981", market_disruption:"#f97316", governance_failure:"#ef4444", reputational_crisis:"#ec4899", financial_exposure:"#dc2626", strategic_drift:"#a855f7" };
const SEV_COLORS  = { sound:"#10b981", monitored:"#f59e0b", exposed:"#f97316", crisis:"#ef4444" };
const ACT_COLORS  = { no_action:"#10b981", risk_monitoring:"#06b6d4", governance_review:"#3b82f6", board_alert:"#f59e0b", financial_restructuring:"#dc2626", strategic_pivot:"#a855f7", reputational_intervention:"#ec4899", emergency_governance:"#ef4444", strategic_transformation:"#7f1d1d" };
const RISK_BADGE  = { low:"bg-emerald-900 text-emerald-300", moderate:"bg-amber-900 text-amber-300", high:"bg-orange-900 text-orange-300", critical:"bg-red-900 text-red-300" };
const SEV_BADGE   = { sound:"bg-emerald-900 text-emerald-300", monitored:"bg-amber-900 text-amber-300", exposed:"bg-orange-900 text-orange-300", crisis:"bg-red-900 text-red-300" };

function DetailModal({ entity, onClose }: { entity: Entity; onClose: () => void }) {
  const [tab, setTab] = useState<"scores"|"signal"|"action">("scores");
  useEffect(()=>{
    const h = (e: KeyboardEvent) => { if (e.key==="Escape") onClose(); };
    window.addEventListener("keydown", h);
    return ()=>window.removeEventListener("keydown",h);
  },[onClose]);
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70" onClick={onClose}>
      <div className="bg-slate-900 border border-slate-700 rounded-xl w-full max-w-lg p-6 shadow-2xl" onClick={e=>e.stopPropagation()}>
        <div className="flex items-center justify-between mb-4">
          <div>
            <span className="text-lg font-bold text-white">{entity.id}</span>
            <span className="ml-2 text-purple-400 text-xs">{entity.region}</span>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl leading-none">✕</button>
        </div>
        <div className="flex gap-2 mb-4">
          {(["scores","signal","action"] as const).map(t=>(
            <button key={t} onClick={()=>setTab(t)}
              className={`px-3 py-1 rounded text-xs font-medium transition-colors ${tab===t?"bg-purple-700 text-white":"bg-slate-800 text-slate-400 hover:text-white"}`}>
              {t.charAt(0).toUpperCase()+t.slice(1)}
            </button>
          ))}
        </div>
        {tab==="scores" && (
          <div className="grid grid-cols-2 gap-3 text-sm">
            {[
              ["Strategic",      entity.strategic_score,      "#a855f7"],
              ["Governance",     entity.governance_score,     "#ef4444"],
              ["Financial Risk", entity.financial_risk_score, "#dc2626"],
              ["Resilience",     entity.resilience_score,     "#06b6d4"],
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
              <div className="text-slate-400 text-xs mb-1">Governance Composite</div>
              <div className="text-white font-bold text-2xl">{entity.governance_composite.toFixed(1)}</div>
            </div>
          </div>
        )}
        {tab==="signal" && (
          <div className="bg-slate-800 rounded-lg p-4 text-sm text-slate-200 leading-relaxed">
            {entity.governance_signal}
            <div className="mt-3 flex gap-2 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[entity.governance_risk as keyof typeof RISK_BADGE]||"bg-slate-700 text-slate-300"}`}>{entity.governance_risk}</span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[entity.governance_severity as keyof typeof SEV_BADGE]||"bg-slate-700 text-slate-300"}`}>{entity.governance_severity}</span>
            </div>
          </div>
        )}
        {tab==="action" && (
          <div className="space-y-3 text-sm">
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Recommended Action</div>
              <div className="text-white font-medium">{entity.recommended_action.replace(/_/g," ")}</div>
            </div>
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Strategic Risk Index</div>
              <div className="text-white font-bold">{entity.estimated_strategic_risk_index.toFixed(2)} / 10</div>
            </div>
            <div className="flex gap-2">
              {entity.has_governance_alert  && <span className="px-2 py-1 rounded bg-purple-900 text-purple-300 text-xs font-medium">GOV ALERT</span>}
              {entity.requires_board_action && <span className="px-2 py-1 rounded bg-red-900 text-red-300 text-xs font-medium">BOARD ACTION</span>}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function GovernanceDashboard() {
  const [data, setData]         = useState<{ entities: Entity[]; summary: Summary }|null>(null);
  const [filter, setFilter]     = useState<string>("all");
  const [patFilter, setPat]     = useState<string>("all");
  const [selected, setSelected] = useState<Entity|null>(null);

  useEffect(()=>{
    fetch("/api/strategic-risk-governance-engine")
      .then(r=>r.json()).then(setData).catch(console.error);
  },[]);

  if (!data) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-slate-300 text-lg animate-pulse">Loading Governance Engine...</div>
    </div>
  );

  const { entities, summary } = data;
  const filtered = entities.filter(e=>
    (filter==="all" || e.governance_risk===filter) &&
    (patFilter==="all" || e.risk_pattern===patFilter)
  );

  const dists = [
    { title:"Risk",     counts:summary.risk_counts,     colors:RISK_COLORS },
    { title:"Pattern",  counts:summary.pattern_counts,  colors:PAT_COLORS  },
    { title:"Severity", counts:summary.severity_counts, colors:SEV_COLORS  },
    { title:"Action",   counts:summary.action_counts,   colors:ACT_COLORS  },
  ] as Array<{title:string;counts:Record<string,number>;colors:Record<string,string>}>;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {selected && <DetailModal entity={selected} onClose={()=>setSelected(null)}/>}

      <div>
        <h1 className="text-2xl font-bold text-white">Strategic Risk & Governance</h1>
        <p className="text-slate-400 text-sm mt-1">Strategic · Governance · Financial · Resilience — board-level intelligence</p>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {[
          ["Entities",      summary.total,                                                  "text-slate-300"],
          ["Avg Composite", summary.avg_governance_composite,                               "text-purple-400"],
          ["Gov Alerts",    summary.governance_alert_count,                                 "text-amber-400"],
          ["Board Actions", summary.board_action_count,                                     "text-red-400"],
          ["Avg Risk Idx",  `${summary.avg_estimated_strategic_risk_index.toFixed(1)}/10`,  "text-purple-400"],
          ["Avg Strategic", `${Math.round(summary.avg_strategic_score)}`,                   "text-slate-300"],
        ].map(([l,v,c])=>(
          <div key={String(l)} className="bg-slate-900 border border-slate-800 rounded-xl p-3 text-center">
            <div className={`text-xl font-bold ${c}`}>{v}</div>
            <div className="text-xs text-slate-500 mt-0.5">{l}</div>
          </div>
        ))}
      </div>

      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
        <div className="grid grid-cols-4 gap-4">
          <Gauge value={summary.avg_strategic_score}      label="Strategic"      color="#a855f7"/>
          <Gauge value={summary.avg_governance_score}     label="Governance"     color="#ef4444"/>
          <Gauge value={summary.avg_financial_risk_score} label="Financial Risk" color="#dc2626"/>
          <Gauge value={summary.avg_resilience_score}     label="Resilience"     color="#06b6d4"/>
        </div>
      </div>

      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 grid grid-cols-1 md:grid-cols-2 gap-5">
        {dists.map(d=><DistBar key={d.title} {...d}/>)}
      </div>

      <div className="flex flex-wrap gap-2">
        {["all","low","moderate","high","critical"].map(r=>(
          <button key={r} onClick={()=>setFilter(r)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${filter===r?"bg-purple-700 border-purple-600 text-white":"bg-slate-900 border-slate-700 text-slate-400 hover:text-white"}`}>
            {r}
          </button>
        ))}
        <span className="w-px h-5 self-center bg-slate-700"/>
        {["all","none","market_disruption","governance_failure","reputational_crisis","financial_exposure","strategic_drift"].map(p=>(
          <button key={p} onClick={()=>setPat(p)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${patFilter===p?"bg-slate-700 border-slate-600 text-white":"bg-slate-900 border-slate-700 text-slate-400 hover:text-white"}`}>
            {p.replace(/_/g," ")}
          </button>
        ))}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {filtered.map(e=>(
          <div key={e.id} onClick={()=>setSelected(e)}
            className="bg-slate-900 border border-slate-800 rounded-xl p-4 cursor-pointer hover:border-purple-700 transition-colors">
            <div className="flex items-center justify-between mb-1">
              <span className="font-bold text-white">{e.id}</span>
              <span className="text-xs text-slate-400">{e.region}</span>
            </div>
            <div className="flex gap-1 mb-3 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[e.governance_risk as keyof typeof RISK_BADGE]||"bg-slate-700 text-slate-300"}`}>{e.governance_risk}</span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[e.governance_severity as keyof typeof SEV_BADGE]||"bg-slate-700 text-slate-300"}`}>{e.governance_severity}</span>
            </div>
            <div className="text-2xl font-black text-white mb-1">{e.governance_composite.toFixed(1)}</div>
            <div className="text-xs text-slate-500 mb-2 capitalize">{e.risk_pattern.replace(/_/g," ")}</div>
            <div className="text-xs text-purple-400 font-medium mb-2">Risk Idx: {e.estimated_strategic_risk_index.toFixed(2)}/10</div>
            <div className="flex gap-1 flex-wrap">
              {e.has_governance_alert  && <span className="px-1.5 py-0.5 rounded bg-purple-900 text-purple-300 text-xs">ALERT</span>}
              {e.requires_board_action && <span className="px-1.5 py-0.5 rounded bg-red-900 text-red-300 text-xs">BOARD</span>}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
