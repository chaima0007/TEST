"use client";
import { useEffect, useState } from "react";

type Deal = {
  deal_id: string; region: string; pipeline_stage: string;
  velocity_risk: string; velocity_pattern: string;
  velocity_severity: string; recommended_action: string;
  stall_score: number; decision_score: number;
  stakeholder_score: number; champion_score: number;
  velocity_composite: number; has_velocity_gap: boolean;
  requires_executive_bridge: boolean; estimated_delay_days: number;
  velocity_signal: string;
};
type Summary = {
  total: number; risk_counts: Record<string,number>;
  pattern_counts: Record<string,number>; severity_counts: Record<string,number>;
  action_counts: Record<string,number>; avg_velocity_composite: number;
  velocity_gap_count: number; executive_bridge_count: number;
  avg_stall_score: number; avg_decision_score: number;
  avg_stakeholder_score: number; avg_champion_score: number;
  avg_estimated_delay_days: number;
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

const RISK_COLORS = { low:"#0ea5e9", moderate:"#f59e0b", high:"#f97316", critical:"#ef4444" };
const PAT_COLORS  = { none:"#0ea5e9", stage_stall:"#ef4444", decision_paralysis:"#f97316", stakeholder_freeze:"#a855f7", champion_disengagement:"#f59e0b", budget_drift:"#06b6d4" };
const SEV_COLORS  = { flowing:"#0ea5e9", slowing:"#f59e0b", stalled:"#f97316", frozen:"#ef4444" };
const ACT_COLORS  = { no_action:"#0ea5e9", velocity_monitoring:"#f59e0b", stage_acceleration_call:"#f97316", decision_criteria_alignment:"#06b6d4", stakeholder_mapping_refresh:"#a855f7", champion_reactivation:"#10b981", executive_sponsor_bridge:"#dc2626", mutual_action_plan_reset:"#ec4899", deal_rescue_intervention:"#7f1d1d" };
const RISK_BADGE  = { low:"bg-sky-900 text-sky-300", moderate:"bg-amber-900 text-amber-300", high:"bg-orange-900 text-orange-300", critical:"bg-red-900 text-red-300" };
const SEV_BADGE   = { flowing:"bg-sky-900 text-sky-300", slowing:"bg-amber-900 text-amber-300", stalled:"bg-orange-900 text-orange-300", frozen:"bg-red-900 text-red-300" };

function DetailModal({ deal, onClose }: { deal: Deal; onClose: () => void }) {
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
            <span className="text-lg font-bold text-white">{deal.deal_id}</span>
            <span className="ml-2 text-slate-400 text-sm">{deal.region}</span>
            <span className="ml-2 text-sky-400 text-xs capitalize">{deal.pipeline_stage.replace(/_/g," ")}</span>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl leading-none">✕</button>
        </div>
        <div className="flex gap-2 mb-4">
          {(["scores","signal","action"] as const).map(t=>(
            <button key={t} onClick={()=>setTab(t)}
              className={`px-3 py-1 rounded text-xs font-medium transition-colors ${tab===t?"bg-sky-700 text-white":"bg-slate-800 text-slate-400 hover:text-white"}`}>
              {t.charAt(0).toUpperCase()+t.slice(1)}
            </button>
          ))}
        </div>
        {tab==="scores" && (
          <div className="grid grid-cols-2 gap-3 text-sm">
            {[
              ["Stall",        deal.stall_score,       "#ef4444"],
              ["Decision",     deal.decision_score,    "#f97316"],
              ["Stakeholder",  deal.stakeholder_score, "#a855f7"],
              ["Champion",     deal.champion_score,    "#f59e0b"],
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
              <div className="text-slate-400 text-xs mb-1">Velocity Composite</div>
              <div className="text-white font-bold text-2xl">{deal.velocity_composite.toFixed(1)}</div>
            </div>
          </div>
        )}
        {tab==="signal" && (
          <div className="bg-slate-800 rounded-lg p-4 text-sm text-slate-200 leading-relaxed">
            {deal.velocity_signal}
            <div className="mt-3 flex gap-2 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[deal.velocity_risk as keyof typeof RISK_BADGE]||"bg-slate-700 text-slate-300"}`}>{deal.velocity_risk}</span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[deal.velocity_severity as keyof typeof SEV_BADGE]||"bg-slate-700 text-slate-300"}`}>{deal.velocity_severity}</span>
            </div>
          </div>
        )}
        {tab==="action" && (
          <div className="space-y-3 text-sm">
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Recommended Action</div>
              <div className="text-white font-medium">{deal.recommended_action.replace(/_/g," ")}</div>
            </div>
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Estimated Delay</div>
              <div className="text-white font-bold">{deal.estimated_delay_days} days</div>
            </div>
            <div className="flex gap-2">
              {deal.has_velocity_gap          && <span className="px-2 py-1 rounded bg-orange-900 text-orange-300 text-xs font-medium">VELOCITY GAP</span>}
              {deal.requires_executive_bridge && <span className="px-2 py-1 rounded bg-sky-900 text-sky-300 text-xs font-medium">EXEC BRIDGE</span>}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function VelocityDashboard() {
  const [data, setData]     = useState<{ deals: Deal[]; summary: Summary }|null>(null);
  const [filter, setFilter] = useState<string>("all");
  const [patFilter, setPat] = useState<string>("all");
  const [selected, setSelected] = useState<Deal|null>(null);

  useEffect(()=>{
    fetch("/api/sales-deal-velocity-acceleration-engine")
      .then(r=>r.json()).then(setData).catch(console.error);
  },[]);

  if (!data) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-sky-400 text-lg animate-pulse">Loading Velocity Intelligence...</div>
    </div>
  );

  const { deals, summary } = data;
  const filtered = deals.filter(d=>
    (filter==="all" || d.velocity_risk===filter) &&
    (patFilter==="all" || d.velocity_pattern===patFilter)
  );

  const dists = [
    { title:"Risk",     counts:summary.risk_counts,     colors:RISK_COLORS },
    { title:"Pattern",  counts:summary.pattern_counts,  colors:PAT_COLORS  },
    { title:"Severity", counts:summary.severity_counts, colors:SEV_COLORS  },
    { title:"Action",   counts:summary.action_counts,   colors:ACT_COLORS  },
  ] as Array<{title:string;counts:Record<string,number>;colors:Record<string,string>}>;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {selected && <DetailModal deal={selected} onClose={()=>setSelected(null)}/>}

      <div>
        <h1 className="text-2xl font-bold text-white">Deal Velocity Acceleration Intelligence</h1>
        <p className="text-slate-400 text-sm mt-1">Stall · Decision · Stakeholder · Champion</p>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {[
          ["Deals",          summary.total,                                         "text-sky-400"],
          ["Avg Composite",  summary.avg_velocity_composite,                        "text-blue-400"],
          ["Velocity Gaps",  summary.velocity_gap_count,                            "text-orange-400"],
          ["Exec Bridge",    summary.executive_bridge_count,                        "text-amber-400"],
          ["Avg Delay",      `${Math.round(summary.avg_estimated_delay_days)}d`,   "text-red-400"],
          ["Avg Stall",      `${Math.round(summary.avg_stall_score)}`,             "text-sky-400"],
        ].map(([l,v,c])=>(
          <div key={String(l)} className="bg-slate-900 border border-slate-800 rounded-xl p-3 text-center">
            <div className={`text-xl font-bold ${c}`}>{v}</div>
            <div className="text-xs text-slate-500 mt-0.5">{l}</div>
          </div>
        ))}
      </div>

      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
        <div className="grid grid-cols-4 gap-4">
          <Gauge value={summary.avg_stall_score}       label="Stall"       color="#ef4444"/>
          <Gauge value={summary.avg_decision_score}    label="Decision"    color="#f97316"/>
          <Gauge value={summary.avg_stakeholder_score} label="Stakeholder" color="#a855f7"/>
          <Gauge value={summary.avg_champion_score}    label="Champion"    color="#f59e0b"/>
        </div>
      </div>

      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 grid grid-cols-1 md:grid-cols-2 gap-5">
        {dists.map(d=><DistBar key={d.title} {...d}/>)}
      </div>

      <div className="flex flex-wrap gap-2">
        {["all","low","moderate","high","critical"].map(r=>(
          <button key={r} onClick={()=>setFilter(r)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${filter===r?"bg-sky-700 border-sky-600 text-white":"bg-slate-900 border-slate-700 text-slate-400 hover:text-white"}`}>
            {r}
          </button>
        ))}
        <span className="w-px h-5 self-center bg-slate-700"/>
        {["all","stage_stall","decision_paralysis","stakeholder_freeze","champion_disengagement","budget_drift"].map(p=>(
          <button key={p} onClick={()=>setPat(p)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${patFilter===p?"bg-blue-900 border-blue-800 text-white":"bg-slate-900 border-slate-700 text-slate-400 hover:text-white"}`}>
            {p.replace(/_/g," ")}
          </button>
        ))}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {filtered.map(d=>(
          <div key={d.deal_id} onClick={()=>setSelected(d)}
            className="bg-slate-900 border border-slate-800 rounded-xl p-4 cursor-pointer hover:border-sky-700 transition-colors">
            <div className="flex items-center justify-between mb-2">
              <span className="font-bold text-white">{d.deal_id}</span>
              <span className="text-xs text-slate-400">{d.region}</span>
            </div>
            <div className="text-xs text-sky-400 mb-2 capitalize">{d.pipeline_stage.replace(/_/g," ")}</div>
            <div className="flex gap-1 mb-3 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[d.velocity_risk as keyof typeof RISK_BADGE]||"bg-slate-700 text-slate-300"}`}>{d.velocity_risk}</span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[d.velocity_severity as keyof typeof SEV_BADGE]||"bg-slate-700 text-slate-300"}`}>{d.velocity_severity}</span>
            </div>
            <div className="text-2xl font-black text-white mb-1">{d.velocity_composite.toFixed(1)}</div>
            <div className="text-xs text-slate-500 mb-2 capitalize">{d.velocity_pattern.replace(/_/g," ")}</div>
            <div className="text-xs text-red-400 font-medium mb-2">{d.estimated_delay_days}d delay</div>
            <div className="flex gap-1 flex-wrap">
              {d.has_velocity_gap          && <span className="px-1.5 py-0.5 rounded bg-orange-900 text-orange-300 text-xs">GAP</span>}
              {d.requires_executive_bridge && <span className="px-1.5 py-0.5 rounded bg-sky-900 text-sky-300 text-xs">BRIDGE</span>}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
