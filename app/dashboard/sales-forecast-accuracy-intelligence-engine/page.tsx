"use client";
import { useEffect, useState } from "react";

type Rep = {
  rep_id: string; region: string; forecast_risk: string; forecast_pattern: string;
  forecast_severity: string; recommended_action: string;
  accuracy_score: number; consistency_score: number;
  pipeline_quality_score: number; calibration_score: number;
  forecast_composite: number; has_forecast_gap: boolean;
  requires_forecast_coaching: boolean; estimated_forecast_error_usd: number;
  forecast_signal: string;
};
type Summary = {
  total: number; risk_counts: Record<string,number>;
  pattern_counts: Record<string,number>; severity_counts: Record<string,number>;
  action_counts: Record<string,number>; avg_forecast_composite: number;
  forecast_gap_count: number; coaching_count: number;
  avg_accuracy_score: number; avg_consistency_score: number;
  avg_pipeline_quality_score: number; avg_calibration_score: number;
  total_estimated_forecast_error_usd: number;
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

const RISK_COLORS = { low:"#06b6d4", moderate:"#f59e0b", high:"#f97316", critical:"#ef4444" };
const PAT_COLORS  = { none:"#06b6d4", chronic_overcommit:"#ef4444", sandbagger:"#3b82f6", volatile_caller:"#f97316", stage_inflate:"#a855f7", late_quarter_crash:"#f59e0b" };
const SEV_COLORS  = { precise:"#06b6d4", acceptable:"#f59e0b", unreliable:"#f97316", deceptive:"#ef4444" };
const ACT_COLORS  = { no_action:"#06b6d4", forecast_calibration_coaching:"#f59e0b", pipeline_qualification_coaching:"#f97316", forecast_discipline_coaching:"#a855f7", forecast_review_escalation:"#ef4444", manager_override_required:"#dc2626", forecast_audit:"#991b1b" };
const RISK_BADGE  = { low:"bg-cyan-900 text-cyan-300", moderate:"bg-amber-900 text-amber-300", high:"bg-orange-900 text-orange-300", critical:"bg-red-900 text-red-300" };
const SEV_BADGE   = { precise:"bg-cyan-900 text-cyan-300", acceptable:"bg-amber-900 text-amber-300", unreliable:"bg-orange-900 text-orange-300", deceptive:"bg-red-900 text-red-300" };

function DetailModal({ rep, onClose }: { rep: Rep; onClose: () => void }) {
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
            <span className="text-lg font-bold text-white">{rep.rep_id}</span>
            <span className="ml-2 text-slate-400 text-sm">{rep.region}</span>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl leading-none">x</button>
        </div>
        <div className="flex gap-2 mb-4">
          {(["scores","signal","action"] as const).map(t=>(
            <button key={t} onClick={()=>setTab(t)}
              className={`px-3 py-1 rounded text-xs font-medium transition-colors ${tab===t?"bg-cyan-700 text-white":"bg-slate-800 text-slate-400 hover:text-white"}`}>
              {t.charAt(0).toUpperCase()+t.slice(1)}
            </button>
          ))}
        </div>
        {tab==="scores" && (
          <div className="grid grid-cols-2 gap-3 text-sm">
            {[
              ["Accuracy",         rep.accuracy_score,         "#06b6d4"],
              ["Consistency",      rep.consistency_score,      "#f97316"],
              ["Pipeline Quality", rep.pipeline_quality_score, "#f59e0b"],
              ["Calibration",      rep.calibration_score,      "#a855f7"],
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
              <div className="text-slate-400 text-xs mb-1">Forecast Composite</div>
              <div className="text-white font-bold text-2xl">{rep.forecast_composite.toFixed(1)}</div>
            </div>
          </div>
        )}
        {tab==="signal" && (
          <div className="bg-slate-800 rounded-lg p-4 text-sm text-slate-200 leading-relaxed">
            {rep.forecast_signal}
            <div className="mt-3 flex gap-2 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[rep.forecast_risk as keyof typeof RISK_BADGE]||"bg-slate-700 text-slate-300"}`}>{rep.forecast_risk}</span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[rep.forecast_severity as keyof typeof SEV_BADGE]||"bg-slate-700 text-slate-300"}`}>{rep.forecast_severity}</span>
            </div>
          </div>
        )}
        {tab==="action" && (
          <div className="space-y-3 text-sm">
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Recommended Action</div>
              <div className="text-white font-medium">{rep.recommended_action.replace(/_/g," ")}</div>
            </div>
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Forecast Error</div>
              <div className="text-white font-bold">${rep.estimated_forecast_error_usd.toLocaleString()}</div>
            </div>
            <div className="flex gap-2">
              {rep.has_forecast_gap           && <span className="px-2 py-1 rounded bg-red-900 text-red-300 text-xs font-medium">GAP</span>}
              {rep.requires_forecast_coaching && <span className="px-2 py-1 rounded bg-cyan-900 text-cyan-300 text-xs font-medium">COACH</span>}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function ForecastAccuracyDashboard() {
  const [data, setData]     = useState<{ reps: Rep[]; summary: Summary }|null>(null);
  const [filter, setFilter] = useState<string>("all");
  const [patFilter, setPat] = useState<string>("all");
  const [selected, setSelected] = useState<Rep|null>(null);

  useEffect(()=>{
    fetch("/api/sales-forecast-accuracy-intelligence-engine")
      .then(r=>r.json()).then(setData).catch(console.error);
  },[]);

  if (!data) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-cyan-400 text-lg animate-pulse">Loading Forecast Accuracy Intelligence...</div>
    </div>
  );

  const { reps, summary } = data;
  const filtered = reps.filter(r=>
    (filter==="all" || r.forecast_risk===filter) &&
    (patFilter==="all" || r.forecast_pattern===patFilter)
  );

  const dists = [
    { title:"Risk",     counts:summary.risk_counts,     colors:RISK_COLORS } as {title:string;counts:Record<string,number>;colors:Record<string,string>},
    { title:"Pattern",  counts:summary.pattern_counts,  colors:PAT_COLORS  } as {title:string;counts:Record<string,number>;colors:Record<string,string>},
    { title:"Severity", counts:summary.severity_counts, colors:SEV_COLORS  } as {title:string;counts:Record<string,number>;colors:Record<string,string>},
    { title:"Action",   counts:summary.action_counts,   colors:ACT_COLORS  } as {title:string;counts:Record<string,number>;colors:Record<string,string>},
  ] as Array<{title:string;counts:Record<string,number>;colors:Record<string,string>}>;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {selected && <DetailModal rep={selected} onClose={()=>setSelected(null)}/>}

      <div>
        <h1 className="text-2xl font-bold text-white">Forecast Accuracy Intelligence</h1>
        <p className="text-slate-400 text-sm mt-1">Accuracy - Consistency - Pipeline quality - Calibration</p>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {[
          ["Reps",           summary.total,                                                          "text-cyan-400"],
          ["Avg Composite",  summary.avg_forecast_composite,                                        "text-red-400"],
          ["Forecast Gaps",  summary.forecast_gap_count,                                            "text-orange-400"],
          ["Need Coaching",  summary.coaching_count,                                                "text-amber-400"],
          ["Total Error",    "$"+(summary.total_estimated_forecast_error_usd/1000).toFixed(0)+"K", "text-red-400"],
          ["Avg Accuracy",   summary.avg_accuracy_score,                                            "text-cyan-400"],
        ].map(([l,v,c])=>(
          <div key={String(l)} className="bg-slate-900 border border-slate-800 rounded-xl p-3 text-center">
            <div className={`text-xl font-bold ${c}`}>{v}</div>
            <div className="text-xs text-slate-500 mt-0.5">{l}</div>
          </div>
        ))}
      </div>

      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
        <div className="grid grid-cols-4 gap-4">
          <Gauge value={summary.avg_accuracy_score}          label="Accuracy"         color="#06b6d4"/>
          <Gauge value={summary.avg_consistency_score}       label="Consistency"      color="#f97316"/>
          <Gauge value={summary.avg_pipeline_quality_score}  label="Pipeline Quality" color="#f59e0b"/>
          <Gauge value={summary.avg_calibration_score}       label="Calibration"      color="#a855f7"/>
        </div>
      </div>

      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 grid grid-cols-1 md:grid-cols-2 gap-5">
        {dists.map(d=><DistBar key={d.title} {...d}/>)}
      </div>

      <div className="flex flex-wrap gap-2">
        {["all","low","moderate","high","critical"].map(r=>(
          <button key={r} onClick={()=>setFilter(r)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${filter===r?"bg-cyan-700 border-cyan-600 text-white":"bg-slate-900 border-slate-700 text-slate-400 hover:text-white"}`}>
            {r}
          </button>
        ))}
        <span className="w-px h-5 self-center bg-slate-700"/>
        {["all","chronic_overcommit","sandbagger","volatile_caller","stage_inflate","late_quarter_crash"].map(p=>(
          <button key={p} onClick={()=>setPat(p)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${patFilter===p?"bg-sky-700 border-sky-600 text-white":"bg-slate-900 border-slate-700 text-slate-400 hover:text-white"}`}>
            {p.replace(/_/g," ")}
          </button>
        ))}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {filtered.map(r=>(
          <div key={r.rep_id} onClick={()=>setSelected(r)}
            className="bg-slate-900 border border-slate-800 rounded-xl p-4 cursor-pointer hover:border-cyan-700 transition-colors">
            <div className="flex items-center justify-between mb-2">
              <span className="font-bold text-white">{r.rep_id}</span>
              <span className="text-xs text-slate-400">{r.region}</span>
            </div>
            <div className="flex gap-1 mb-3 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[r.forecast_risk as keyof typeof RISK_BADGE]||"bg-slate-700 text-slate-300"}`}>{r.forecast_risk}</span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[r.forecast_severity as keyof typeof SEV_BADGE]||"bg-slate-700 text-slate-300"}`}>{r.forecast_severity}</span>
            </div>
            <div className="text-2xl font-black text-white mb-1">{r.forecast_composite.toFixed(1)}</div>
            <div className="text-xs text-slate-500 mb-2 capitalize">{r.forecast_pattern.replace(/_/g," ")}</div>
            <div className="flex gap-1">
              {r.has_forecast_gap           && <span className="px-1.5 py-0.5 rounded bg-red-900 text-red-300 text-xs">GAP</span>}
              {r.requires_forecast_coaching && <span className="px-1.5 py-0.5 rounded bg-cyan-900 text-cyan-300 text-xs">COACH</span>}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
