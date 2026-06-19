"use client";
import { useEffect, useState } from "react";

type Initiative = {
  initiative_id: string; region: string;
  improvement_risk: string; improvement_pattern: string;
  improvement_severity: string; recommended_action: string;
  process_score: number; innovation_score: number;
  execution_score: number; maturity_score: number;
  improvement_composite: number; has_stagnation_signal: boolean;
  requires_transformation: boolean; estimated_improvement_gap_index: number;
  improvement_signal: string;
};
type Summary = {
  total: number; risk_counts: Record<string,number>;
  pattern_counts: Record<string,number>; severity_counts: Record<string,number>;
  action_counts: Record<string,number>; avg_improvement_composite: number;
  stagnation_signal_count: number; transformation_required_count: number;
  avg_process_score: number; avg_innovation_score: number;
  avg_execution_score: number; avg_maturity_score: number;
  avg_estimated_improvement_gap_index: number;
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
const PAT_COLORS  = { none:"#10b981", process_stagnation:"#ef4444", waste_accumulation:"#f97316", innovation_deficit:"#a855f7", kpi_degradation:"#dc2626", change_fatigue:"#f59e0b" };
const SEV_COLORS  = { excellent:"#10b981", progressing:"#f59e0b", stagnating:"#f97316", declining:"#ef4444" };
const ACT_COLORS  = { no_action:"#10b981", improvement_monitoring:"#06b6d4", kaizen_initiative:"#3b82f6", lean_review:"#f59e0b", kpi_reset:"#a855f7", innovation_sprint:"#ec4899", change_management:"#f97316", process_reengineering:"#dc2626", transformation_program:"#7f1d1d" };
const RISK_BADGE  = { low:"bg-emerald-900 text-emerald-300", moderate:"bg-amber-900 text-amber-300", high:"bg-orange-900 text-orange-300", critical:"bg-red-900 text-red-300" };
const SEV_BADGE   = { excellent:"bg-emerald-900 text-emerald-300", progressing:"bg-amber-900 text-amber-300", stagnating:"bg-orange-900 text-orange-300", declining:"bg-red-900 text-red-300" };

function DetailModal({ initiative, onClose }: { initiative: Initiative; onClose: () => void }) {
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
            <span className="text-lg font-bold text-white">{initiative.initiative_id}</span>
            <span className="ml-2 text-green-400 text-xs">{initiative.region}</span>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl leading-none">✕</button>
        </div>
        <div className="flex gap-2 mb-4">
          {(["scores","signal","action"] as const).map(t=>(
            <button key={t} onClick={()=>setTab(t)}
              className={`px-3 py-1 rounded text-xs font-medium transition-colors ${tab===t?"bg-green-700 text-white":"bg-slate-800 text-slate-400 hover:text-white"}`}>
              {t.charAt(0).toUpperCase()+t.slice(1)}
            </button>
          ))}
        </div>
        {tab==="scores" && (
          <div className="grid grid-cols-2 gap-3 text-sm">
            {[
              ["Process",    initiative.process_score,    "#ef4444"],
              ["Innovation", initiative.innovation_score, "#a855f7"],
              ["Execution",  initiative.execution_score,  "#f97316"],
              ["Maturity",   initiative.maturity_score,   "#10b981"],
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
              <div className="text-slate-400 text-xs mb-1">Improvement Composite</div>
              <div className="text-white font-bold text-2xl">{initiative.improvement_composite.toFixed(1)}</div>
            </div>
          </div>
        )}
        {tab==="signal" && (
          <div className="bg-slate-800 rounded-lg p-4 text-sm text-slate-200 leading-relaxed">
            {initiative.improvement_signal}
            <div className="mt-3 flex gap-2 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[initiative.improvement_risk as keyof typeof RISK_BADGE]||"bg-slate-700 text-slate-300"}`}>{initiative.improvement_risk}</span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[initiative.improvement_severity as keyof typeof SEV_BADGE]||"bg-slate-700 text-slate-300"}`}>{initiative.improvement_severity}</span>
            </div>
          </div>
        )}
        {tab==="action" && (
          <div className="space-y-3 text-sm">
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Recommended Action</div>
              <div className="text-white font-medium">{initiative.recommended_action.replace(/_/g," ")}</div>
            </div>
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Improvement Gap Index</div>
              <div className="text-white font-bold">{initiative.estimated_improvement_gap_index.toFixed(2)} / 10</div>
            </div>
            <div className="flex gap-2">
              {initiative.has_stagnation_signal    && <span className="px-2 py-1 rounded bg-amber-900 text-amber-300 text-xs font-medium">STAGNATION</span>}
              {initiative.requires_transformation  && <span className="px-2 py-1 rounded bg-red-900 text-red-300 text-xs font-medium">TRANSFORM</span>}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function ImprovementDashboard() {
  const [data, setData]         = useState<{ initiatives: Initiative[]; summary: Summary }|null>(null);
  const [filter, setFilter]     = useState<string>("all");
  const [patFilter, setPat]     = useState<string>("all");
  const [selected, setSelected] = useState<Initiative|null>(null);

  useEffect(()=>{
    fetch("/api/continuous-improvement-excellence-engine")
      .then(r=>r.json()).then(setData).catch(console.error);
  },[]);

  if (!data) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-green-400 text-lg animate-pulse">Loading Improvement Engine...</div>
    </div>
  );

  const { initiatives, summary } = data;
  const filtered = initiatives.filter(i=>
    (filter==="all" || i.improvement_risk===filter) &&
    (patFilter==="all" || i.improvement_pattern===patFilter)
  );

  const dists = [
    { title:"Risk",     counts:summary.risk_counts,     colors:RISK_COLORS },
    { title:"Pattern",  counts:summary.pattern_counts,  colors:PAT_COLORS  },
    { title:"Severity", counts:summary.severity_counts, colors:SEV_COLORS  },
    { title:"Action",   counts:summary.action_counts,   colors:ACT_COLORS  },
  ] as Array<{title:string;counts:Record<string,number>;colors:Record<string,string>}>;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {selected && <DetailModal initiative={selected} onClose={()=>setSelected(null)}/>}

      <div>
        <h1 className="text-2xl font-bold text-white">Continuous Improvement & Operational Excellence</h1>
        <p className="text-slate-400 text-sm mt-1">Process · Innovation · Execution · Maturity — driving operational excellence</p>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {[
          ["Initiatives",   summary.total,                                                    "text-green-400"],
          ["Avg Composite", summary.avg_improvement_composite,                                "text-teal-400"],
          ["Stagnating",    summary.stagnation_signal_count,                                  "text-amber-400"],
          ["Transform Req", summary.transformation_required_count,                            "text-red-400"],
          ["Avg Gap Index", `${summary.avg_estimated_improvement_gap_index.toFixed(1)}/10`,   "text-green-400"],
          ["Avg Process",   `${Math.round(summary.avg_process_score)}`,                       "text-teal-400"],
        ].map(([l,v,c])=>(
          <div key={String(l)} className="bg-slate-900 border border-slate-800 rounded-xl p-3 text-center">
            <div className={`text-xl font-bold ${c}`}>{v}</div>
            <div className="text-xs text-slate-500 mt-0.5">{l}</div>
          </div>
        ))}
      </div>

      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
        <div className="grid grid-cols-4 gap-4">
          <Gauge value={summary.avg_process_score}    label="Process"    color="#ef4444"/>
          <Gauge value={summary.avg_innovation_score} label="Innovation" color="#a855f7"/>
          <Gauge value={summary.avg_execution_score}  label="Execution"  color="#f97316"/>
          <Gauge value={summary.avg_maturity_score}   label="Maturity"   color="#10b981"/>
        </div>
      </div>

      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 grid grid-cols-1 md:grid-cols-2 gap-5">
        {dists.map(d=><DistBar key={d.title} {...d}/>)}
      </div>

      <div className="flex flex-wrap gap-2">
        {["all","low","moderate","high","critical"].map(r=>(
          <button key={r} onClick={()=>setFilter(r)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${filter===r?"bg-green-700 border-green-600 text-white":"bg-slate-900 border-slate-700 text-slate-400 hover:text-white"}`}>
            {r}
          </button>
        ))}
        <span className="w-px h-5 self-center bg-slate-700"/>
        {["all","none","process_stagnation","waste_accumulation","innovation_deficit","kpi_degradation","change_fatigue"].map(p=>(
          <button key={p} onClick={()=>setPat(p)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${patFilter===p?"bg-teal-900 border-teal-800 text-white":"bg-slate-900 border-slate-700 text-slate-400 hover:text-white"}`}>
            {p.replace(/_/g," ")}
          </button>
        ))}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {filtered.map(i=>(
          <div key={i.initiative_id} onClick={()=>setSelected(i)}
            className="bg-slate-900 border border-slate-800 rounded-xl p-4 cursor-pointer hover:border-green-700 transition-colors">
            <div className="flex items-center justify-between mb-1">
              <span className="font-bold text-white">{i.initiative_id}</span>
              <span className="text-xs text-slate-400">{i.region}</span>
            </div>
            <div className="flex gap-1 mb-3 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[i.improvement_risk as keyof typeof RISK_BADGE]||"bg-slate-700 text-slate-300"}`}>{i.improvement_risk}</span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[i.improvement_severity as keyof typeof SEV_BADGE]||"bg-slate-700 text-slate-300"}`}>{i.improvement_severity}</span>
            </div>
            <div className="text-2xl font-black text-white mb-1">{i.improvement_composite.toFixed(1)}</div>
            <div className="text-xs text-slate-500 mb-2 capitalize">{i.improvement_pattern.replace(/_/g," ")}</div>
            <div className="text-xs text-green-400 font-medium mb-2">Gap: {i.estimated_improvement_gap_index.toFixed(2)}/10</div>
            <div className="flex gap-1 flex-wrap">
              {i.has_stagnation_signal    && <span className="px-1.5 py-0.5 rounded bg-amber-900 text-amber-300 text-xs">STAGNATION</span>}
              {i.requires_transformation  && <span className="px-1.5 py-0.5 rounded bg-red-900 text-red-300 text-xs">TRANSFORM</span>}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
