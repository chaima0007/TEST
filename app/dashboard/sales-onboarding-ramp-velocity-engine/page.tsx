"use client";
import { useEffect, useState } from "react";

type Rep = {
  rep_id: string; region: string; ramp_risk: string; ramp_pattern: string;
  ramp_severity: string; recommended_action: string;
  velocity_score: number; readiness_score: number;
  activity_score: number; engagement_score: number;
  ramp_composite: number; has_ramp_gap: boolean;
  requires_intervention: boolean; estimated_ramp_delay_weeks: number;
  ramp_signal: string;
};
type Summary = {
  total: number; risk_counts: Record<string,number>;
  pattern_counts: Record<string,number>; severity_counts: Record<string,number>;
  action_counts: Record<string,number>; avg_ramp_composite: number;
  ramp_gap_count: number; intervention_count: number;
  avg_velocity_score: number; avg_readiness_score: number;
  avg_activity_score: number; avg_engagement_score: number;
  avg_estimated_ramp_delay_weeks: number;
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
const PAT_COLORS  = { none:"#10b981", stalled_ramp:"#ef4444", plateau_trap:"#f97316", knowledge_gap:"#a855f7", activity_laggard:"#f59e0b", pipeline_void:"#3b82f6" };
const SEV_COLORS  = { on_track:"#10b981", at_risk:"#f59e0b", stalled:"#f97316", failed:"#ef4444" };
const ACT_COLORS  = { no_action:"#10b981", ramp_monitoring:"#f59e0b", enablement_acceleration:"#f97316", pipeline_building_support:"#3b82f6", skills_gap_coaching:"#a855f7", manager_ramp_intervention:"#06b6d4", territory_assignment_review:"#ec4899", ramp_plan_reset:"#dc2626", early_exit_assessment:"#7f1d1d" };
const RISK_BADGE  = { low:"bg-emerald-900 text-emerald-300", moderate:"bg-amber-900 text-amber-300", high:"bg-orange-900 text-orange-300", critical:"bg-red-900 text-red-300" };
const SEV_BADGE   = { on_track:"bg-emerald-900 text-emerald-300", at_risk:"bg-amber-900 text-amber-300", stalled:"bg-orange-900 text-orange-300", failed:"bg-red-900 text-red-300" };

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
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl leading-none">✕</button>
        </div>
        <div className="flex gap-2 mb-4">
          {(["scores","signal","action"] as const).map(t=>(
            <button key={t} onClick={()=>setTab(t)}
              className={`px-3 py-1 rounded text-xs font-medium transition-colors ${tab===t?"bg-violet-700 text-white":"bg-slate-800 text-slate-400 hover:text-white"}`}>
              {t.charAt(0).toUpperCase()+t.slice(1)}
            </button>
          ))}
        </div>
        {tab==="scores" && (
          <div className="grid grid-cols-2 gap-3 text-sm">
            {[
              ["Velocity",    rep.velocity_score,    "#8b5cf6"],
              ["Readiness",   rep.readiness_score,   "#06b6d4"],
              ["Activity",    rep.activity_score,    "#f97316"],
              ["Engagement",  rep.engagement_score,  "#10b981"],
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
              <div className="text-slate-400 text-xs mb-1">Ramp Composite</div>
              <div className="text-white font-bold text-2xl">{rep.ramp_composite.toFixed(1)}</div>
            </div>
          </div>
        )}
        {tab==="signal" && (
          <div className="bg-slate-800 rounded-lg p-4 text-sm text-slate-200 leading-relaxed">
            {rep.ramp_signal}
            <div className="mt-3 flex gap-2 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[rep.ramp_risk as keyof typeof RISK_BADGE]||"bg-slate-700 text-slate-300"}`}>{rep.ramp_risk}</span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[rep.ramp_severity as keyof typeof SEV_BADGE]||"bg-slate-700 text-slate-300"}`}>{rep.ramp_severity}</span>
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
              <div className="text-slate-400 text-xs mb-1">Estimated Ramp Delay</div>
              <div className="text-white font-bold">{rep.estimated_ramp_delay_weeks.toFixed(1)} weeks</div>
            </div>
            <div className="flex gap-2">
              {rep.has_ramp_gap        && <span className="px-2 py-1 rounded bg-orange-900 text-orange-300 text-xs font-medium">RAMP GAP</span>}
              {rep.requires_intervention && <span className="px-2 py-1 rounded bg-violet-900 text-violet-300 text-xs font-medium">INTERVENE</span>}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function RampDashboard() {
  const [data, setData]     = useState<{ reps: Rep[]; summary: Summary }|null>(null);
  const [filter, setFilter] = useState<string>("all");
  const [patFilter, setPat] = useState<string>("all");
  const [selected, setSelected] = useState<Rep|null>(null);

  useEffect(()=>{
    fetch("/api/sales-onboarding-ramp-velocity-engine")
      .then(r=>r.json()).then(setData).catch(console.error);
  },[]);

  if (!data) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-violet-400 text-lg animate-pulse">Loading Ramp Intelligence...</div>
    </div>
  );

  const { reps, summary } = data;
  const filtered = reps.filter(r=>
    (filter==="all" || r.ramp_risk===filter) &&
    (patFilter==="all" || r.ramp_pattern===patFilter)
  );

  const dists = [
    { title:"Risk",     counts:summary.risk_counts,     colors:RISK_COLORS },
    { title:"Pattern",  counts:summary.pattern_counts,  colors:PAT_COLORS  },
    { title:"Severity", counts:summary.severity_counts, colors:SEV_COLORS  },
    { title:"Action",   counts:summary.action_counts,   colors:ACT_COLORS  },
  ] as Array<{title:string;counts:Record<string,number>;colors:Record<string,string>}>;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {selected && <DetailModal rep={selected} onClose={()=>setSelected(null)}/>}

      <div>
        <h1 className="text-2xl font-bold text-white">Onboarding Ramp Velocity Intelligence</h1>
        <p className="text-slate-400 text-sm mt-1">Velocity · Readiness · Activity · Engagement</p>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {[
          ["New Reps",       summary.total,                                                              "text-violet-400"],
          ["Avg Composite",  summary.avg_ramp_composite,                                                "text-purple-400"],
          ["Ramp Gaps",      summary.ramp_gap_count,                                                    "text-orange-400"],
          ["Need Action",    summary.intervention_count,                                                 "text-amber-400"],
          ["Avg Delay",      `${summary.avg_estimated_ramp_delay_weeks.toFixed(1)}w`,                  "text-red-400"],
          ["Avg Velocity",   `${Math.round(100 - summary.avg_velocity_score)}%`,                       "text-violet-400"],
        ].map(([l,v,c])=>(
          <div key={String(l)} className="bg-slate-900 border border-slate-800 rounded-xl p-3 text-center">
            <div className={`text-xl font-bold ${c}`}>{v}</div>
            <div className="text-xs text-slate-500 mt-0.5">{l}</div>
          </div>
        ))}
      </div>

      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
        <div className="grid grid-cols-4 gap-4">
          <Gauge value={summary.avg_velocity_score}   label="Velocity"   color="#8b5cf6"/>
          <Gauge value={summary.avg_readiness_score}  label="Readiness"  color="#06b6d4"/>
          <Gauge value={summary.avg_activity_score}   label="Activity"   color="#f97316"/>
          <Gauge value={summary.avg_engagement_score} label="Engagement" color="#10b981"/>
        </div>
      </div>

      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 grid grid-cols-1 md:grid-cols-2 gap-5">
        {dists.map(d=><DistBar key={d.title} {...d}/>)}
      </div>

      <div className="flex flex-wrap gap-2">
        {["all","low","moderate","high","critical"].map(r=>(
          <button key={r} onClick={()=>setFilter(r)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${filter===r?"bg-violet-700 border-violet-600 text-white":"bg-slate-900 border-slate-700 text-slate-400 hover:text-white"}`}>
            {r}
          </button>
        ))}
        <span className="w-px h-5 self-center bg-slate-700"/>
        {["all","stalled_ramp","plateau_trap","knowledge_gap","activity_laggard","pipeline_void"].map(p=>(
          <button key={p} onClick={()=>setPat(p)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${patFilter===p?"bg-purple-900 border-purple-800 text-white":"bg-slate-900 border-slate-700 text-slate-400 hover:text-white"}`}>
            {p.replace(/_/g," ")}
          </button>
        ))}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {filtered.map(r=>(
          <div key={r.rep_id} onClick={()=>setSelected(r)}
            className="bg-slate-900 border border-slate-800 rounded-xl p-4 cursor-pointer hover:border-violet-700 transition-colors">
            <div className="flex items-center justify-between mb-2">
              <span className="font-bold text-white">{r.rep_id}</span>
              <span className="text-xs text-slate-400">{r.region}</span>
            </div>
            <div className="flex gap-1 mb-3 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[r.ramp_risk as keyof typeof RISK_BADGE]||"bg-slate-700 text-slate-300"}`}>{r.ramp_risk}</span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[r.ramp_severity as keyof typeof SEV_BADGE]||"bg-slate-700 text-slate-300"}`}>{r.ramp_severity}</span>
            </div>
            <div className="text-2xl font-black text-white mb-1">{r.ramp_composite.toFixed(1)}</div>
            <div className="text-xs text-slate-500 mb-2 capitalize">{r.ramp_pattern.replace(/_/g," ")}</div>
            <div className="flex gap-1 flex-wrap">
              {r.has_ramp_gap        && <span className="px-1.5 py-0.5 rounded bg-orange-900 text-orange-300 text-xs">RAMP GAP</span>}
              {r.requires_intervention && <span className="px-1.5 py-0.5 rounded bg-violet-900 text-violet-300 text-xs">ACT</span>}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
