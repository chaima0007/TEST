"use client";
import { useEffect, useState } from "react";

type Swarm = {
  swarm_id: string; region: string;
  orchestration_risk: string; conflict_pattern: string;
  orchestration_severity: string; recommended_action: string;
  conflict_score: number; coordination_score: number;
  efficiency_score: number; resilience_score: number;
  orchestration_composite: number; has_orchestration_alert: boolean;
  requires_human_intervention: boolean; estimated_swarm_health_index: number;
  orchestration_signal: string;
};
type Summary = {
  total: number; risk_counts: Record<string,number>;
  pattern_counts: Record<string,number>; severity_counts: Record<string,number>;
  action_counts: Record<string,number>; avg_orchestration_composite: number;
  orchestration_alert_count: number; human_intervention_count: number;
  avg_conflict_score: number; avg_coordination_score: number;
  avg_efficiency_score: number; avg_resilience_score: number;
  avg_estimated_swarm_health_index: number;
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

const RISK_COLORS   = { low:"#10b981", moderate:"#f59e0b", high:"#f97316", critical:"#ef4444" };
const PAT_COLORS    = { none:"#10b981", resource_contention:"#f97316", goal_misalignment:"#a855f7", communication_breakdown:"#f59e0b", cascade_failure:"#dc2626", deadlock:"#ef4444" };
const SEV_COLORS    = { harmonized:"#10b981", balanced:"#f59e0b", degraded:"#f97316", critical:"#ef4444" };
const ACT_COLORS    = { no_action:"#10b981", coordination_monitoring:"#06b6d4", task_redistribution:"#f59e0b", goal_realignment:"#a855f7", communication_protocol_update:"#3b82f6", cascade_isolation:"#f97316", deadlock_resolution:"#dc2626", emergency_reorchestration:"#ef4444", swarm_reset:"#7f1d1d" };
const RISK_BADGE    = { low:"bg-emerald-900 text-emerald-300", moderate:"bg-amber-900 text-amber-300", high:"bg-orange-900 text-orange-300", critical:"bg-red-900 text-red-300" };
const SEV_BADGE     = { harmonized:"bg-emerald-900 text-emerald-300", balanced:"bg-amber-900 text-amber-300", degraded:"bg-orange-900 text-orange-300", critical:"bg-red-900 text-red-300" };

function DetailModal({ swarm, onClose }: { swarm: Swarm; onClose: () => void }) {
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
            <span className="text-lg font-bold text-white">{swarm.swarm_id}</span>
            <span className="ml-2 text-cyan-400 text-xs">{swarm.region}</span>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl leading-none">✕</button>
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
              ["Conflict",     swarm.conflict_score,     "#ef4444"],
              ["Coordination", swarm.coordination_score, "#f59e0b"],
              ["Efficiency",   swarm.efficiency_score,   "#f97316"],
              ["Resilience",   swarm.resilience_score,   "#06b6d4"],
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
              <div className="text-slate-400 text-xs mb-1">Orchestration Composite</div>
              <div className="text-white font-bold text-2xl">{swarm.orchestration_composite.toFixed(1)}</div>
            </div>
          </div>
        )}
        {tab==="signal" && (
          <div className="bg-slate-800 rounded-lg p-4 text-sm text-slate-200 leading-relaxed">
            {swarm.orchestration_signal}
            <div className="mt-3 flex gap-2 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[swarm.orchestration_risk as keyof typeof RISK_BADGE]||"bg-slate-700 text-slate-300"}`}>{swarm.orchestration_risk}</span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[swarm.orchestration_severity as keyof typeof SEV_BADGE]||"bg-slate-700 text-slate-300"}`}>{swarm.orchestration_severity}</span>
            </div>
          </div>
        )}
        {tab==="action" && (
          <div className="space-y-3 text-sm">
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Recommended Action</div>
              <div className="text-white font-medium">{swarm.recommended_action.replace(/_/g," ")}</div>
            </div>
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Swarm Health Index</div>
              <div className="text-white font-bold">{swarm.estimated_swarm_health_index.toFixed(2)} / 10</div>
            </div>
            <div className="flex gap-2">
              {swarm.has_orchestration_alert        && <span className="px-2 py-1 rounded bg-cyan-900 text-cyan-300 text-xs font-medium">ALERT</span>}
              {swarm.requires_human_intervention    && <span className="px-2 py-1 rounded bg-orange-900 text-orange-300 text-xs font-medium">HUMAN NEEDED</span>}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function OrchestrationDashboard() {
  const [data, setData]       = useState<{ swarms: Swarm[]; summary: Summary }|null>(null);
  const [filter, setFilter]   = useState<string>("all");
  const [patFilter, setPat]   = useState<string>("all");
  const [selected, setSelected] = useState<Swarm|null>(null);

  useEffect(()=>{
    fetch("/api/swarm-orchestration-conflict-engine")
      .then(r=>r.json()).then(setData).catch(console.error);
  },[]);

  if (!data) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-cyan-400 text-lg animate-pulse">Loading Orchestration Engine...</div>
    </div>
  );

  const { swarms, summary } = data;
  const filtered = swarms.filter(s=>
    (filter==="all" || s.orchestration_risk===filter) &&
    (patFilter==="all" || s.conflict_pattern===patFilter)
  );

  const dists = [
    { title:"Risk",     counts:summary.risk_counts,     colors:RISK_COLORS },
    { title:"Pattern",  counts:summary.pattern_counts,  colors:PAT_COLORS  },
    { title:"Severity", counts:summary.severity_counts, colors:SEV_COLORS  },
    { title:"Action",   counts:summary.action_counts,   colors:ACT_COLORS  },
  ] as Array<{title:string;counts:Record<string,number>;colors:Record<string,string>}>;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {selected && <DetailModal swarm={selected} onClose={()=>setSelected(null)}/>}

      <div>
        <h1 className="text-2xl font-bold text-white">Swarm Orchestration & Conflict Resolution</h1>
        <p className="text-slate-400 text-sm mt-1">Conflict · Coordination · Efficiency · Resilience — keeping swarms in harmony</p>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {[
          ["Swarms",       summary.total,                                              "text-cyan-400"],
          ["Avg Composite",summary.avg_orchestration_composite,                        "text-sky-400"],
          ["Alerts",       summary.orchestration_alert_count,                          "text-amber-400"],
          ["Human Needed", summary.human_intervention_count,                           "text-orange-400"],
          ["Avg Health",   `${summary.avg_estimated_swarm_health_index.toFixed(1)}/10`,"text-cyan-400"],
          ["Avg Conflict", `${Math.round(summary.avg_conflict_score)}`,                "text-sky-400"],
        ].map(([l,v,c])=>(
          <div key={String(l)} className="bg-slate-900 border border-slate-800 rounded-xl p-3 text-center">
            <div className={`text-xl font-bold ${c}`}>{v}</div>
            <div className="text-xs text-slate-500 mt-0.5">{l}</div>
          </div>
        ))}
      </div>

      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
        <div className="grid grid-cols-4 gap-4">
          <Gauge value={summary.avg_conflict_score}      label="Conflict"     color="#ef4444"/>
          <Gauge value={summary.avg_coordination_score}  label="Coordination" color="#f59e0b"/>
          <Gauge value={summary.avg_efficiency_score}    label="Efficiency"   color="#f97316"/>
          <Gauge value={summary.avg_resilience_score}    label="Resilience"   color="#06b6d4"/>
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
        {["all","none","resource_contention","goal_misalignment","communication_breakdown","cascade_failure","deadlock"].map(p=>(
          <button key={p} onClick={()=>setPat(p)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${patFilter===p?"bg-sky-900 border-sky-800 text-white":"bg-slate-900 border-slate-700 text-slate-400 hover:text-white"}`}>
            {p.replace(/_/g," ")}
          </button>
        ))}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {filtered.map(s=>(
          <div key={s.swarm_id} onClick={()=>setSelected(s)}
            className="bg-slate-900 border border-slate-800 rounded-xl p-4 cursor-pointer hover:border-cyan-700 transition-colors">
            <div className="flex items-center justify-between mb-1">
              <span className="font-bold text-white">{s.swarm_id}</span>
              <span className="text-xs text-slate-400">{s.region}</span>
            </div>
            <div className="flex gap-1 mb-3 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[s.orchestration_risk as keyof typeof RISK_BADGE]||"bg-slate-700 text-slate-300"}`}>{s.orchestration_risk}</span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[s.orchestration_severity as keyof typeof SEV_BADGE]||"bg-slate-700 text-slate-300"}`}>{s.orchestration_severity}</span>
            </div>
            <div className="text-2xl font-black text-white mb-1">{s.orchestration_composite.toFixed(1)}</div>
            <div className="text-xs text-slate-500 mb-2 capitalize">{s.conflict_pattern.replace(/_/g," ")}</div>
            <div className="text-xs text-cyan-400 font-medium mb-2">Health: {s.estimated_swarm_health_index.toFixed(2)}/10</div>
            <div className="flex gap-1 flex-wrap">
              {s.has_orchestration_alert     && <span className="px-1.5 py-0.5 rounded bg-cyan-900 text-cyan-300 text-xs">ALERT</span>}
              {s.requires_human_intervention && <span className="px-1.5 py-0.5 rounded bg-orange-900 text-orange-300 text-xs">HUMAN</span>}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
