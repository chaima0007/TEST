"use client";

import { useEffect, useState, useCallback } from "react";

interface Rep {
  rep_id: string; region: string;
  penetration_risk: string; penetration_pattern: string;
  penetration_severity: string; recommended_action: string;
  account_coverage_score: number; account_depth_score: number;
  strategic_focus_score: number; expansion_momentum_score: number;
  account_penetration_composite: number;
  has_penetration_gap: boolean; requires_account_coaching: boolean;
  estimated_untapped_revenue_usd: number; penetration_signal: string;
}
interface Summary {
  total: number; risk_counts: Record<string, number>;
  pattern_counts: Record<string, number>; severity_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_account_penetration_composite: number; penetration_gap_count: number;
  account_coaching_count: number; avg_account_coverage_score: number;
  avg_account_depth_score: number; avg_strategic_focus_score: number;
  avg_expansion_momentum_score: number; total_estimated_untapped_revenue_usd: number;
}

const riskColor: Record<string,string> = { low:"text-emerald-400", moderate:"text-yellow-400", high:"text-orange-400", critical:"text-red-400" };
const riskBorder: Record<string,string> = { low:"border-emerald-500/30", moderate:"border-yellow-500/30", high:"border-orange-500/30", critical:"border-red-500/30" };
const riskBg: Record<string,string> = { low:"bg-emerald-500/10", moderate:"bg-yellow-500/10", high:"bg-orange-500/10", critical:"bg-red-500/10" };

function fmtUSD(v:number){ if(v>=1_000_000) return `$${(v/1_000_000).toFixed(1)}M`; if(v>=1_000) return `$${(v/1_000).toFixed(0)}K`; return `$${v.toFixed(0)}`; }

function GaugeRing({label,value}:{label:string;value:number}) {
  const pct=Math.min(value/100,1),r=36,cx=44,cy=44,circ=2*Math.PI*r,dash=circ*pct;
  const color=pct<0.2?"#34d399":pct<0.4?"#facc15":pct<0.6?"#fb923c":"#f87171";
  return (
    <div className="flex flex-col items-center gap-1">
      <svg width={88} height={88} className="-rotate-90">
        <circle cx={cx} cy={cy} r={r} fill="none" stroke="#1e293b" strokeWidth={8}/>
        <circle cx={cx} cy={cy} r={r} fill="none" stroke={color} strokeWidth={8} strokeDasharray={`${dash} ${circ}`} strokeLinecap="round"/>
      </svg>
      <span className="text-base font-bold text-slate-100 -mt-10">{value.toFixed(1)}</span>
      <span className="text-xs text-slate-400 mt-8 text-center leading-tight">{label}</span>
    </div>
  );
}

function ScoreBar({label,value}:{label:string;value:number}) {
  const pct=Math.min(value,100);
  const color=pct<20?"bg-emerald-500":pct<40?"bg-yellow-500":pct<60?"bg-orange-500":"bg-red-500";
  return (
    <div className="space-y-1">
      <div className="flex justify-between text-xs text-slate-400"><span>{label}</span><span className="font-medium text-slate-200">{value.toFixed(1)}</span></div>
      <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden"><div className={`h-full rounded-full ${color}`} style={{width:`${pct}%`}}/></div>
    </div>
  );
}

function DistBar({title,counts,colors}:{title:string;counts:Record<string,number>;colors:Record<string,string>}) {
  const total=Object.values(counts).reduce((a,b)=>a+b,0)||1;
  return (
    <div className="space-y-2">
      <p className="text-xs font-medium text-slate-400 uppercase tracking-wider">{title}</p>
      <div className="flex h-2 rounded-full overflow-hidden gap-0.5">
        {Object.entries(counts).map(([k,v])=><div key={k} className={colors[k]||"bg-slate-600"} style={{width:`${(v/total)*100}%`}} title={`${k}: ${v}`}/>)}
      </div>
      <div className="flex flex-wrap gap-x-3 gap-y-1">
        {Object.entries(counts).map(([k,v])=>(
          <span key={k} className="text-xs text-slate-400">
            <span className={`font-medium ${colors[k]?.replace("bg-","text-")||"text-slate-300"}`}>{v}</span> {k.replace(/_/g," ")}
          </span>
        ))}
      </div>
    </div>
  );
}

function DetailModal({rep,onClose}:{rep:Rep;onClose:()=>void}) {
  const [tab,setTab]=useState<"scores"|"signals"|"action">("scores");
  useEffect(()=>{ const h=(e:KeyboardEvent)=>{if(e.key==="Escape")onClose();}; window.addEventListener("keydown",h); return ()=>window.removeEventListener("keydown",h); },[onClose]);
  const actionLabels:Record<string,string>={
    no_action:"No Action Required",
    territory_coverage_coaching:"Territory Coverage Coaching",
    account_prioritization_review:"Account Prioritization Review",
    strategic_account_planning:"Strategic Account Planning",
    expansion_pipeline_build:"Expansion Pipeline Build",
    executive_engagement_program:"Executive Engagement Program",
  };
  const severityColors:Record<string,string>={ optimal:"text-emerald-400", developing:"text-yellow-400", shallow:"text-orange-400", stagnant:"text-red-400" };
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm" onClick={onClose}>
      <div className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-lg mx-4 shadow-2xl" onClick={e=>e.stopPropagation()}>
        <div className="flex items-center justify-between p-5 border-b border-slate-800">
          <div>
            <h3 className="font-semibold text-slate-100">{rep.rep_id}</h3>
            <p className="text-xs text-slate-400">{rep.region} · {rep.penetration_pattern.replace(/_/g," ")}</p>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-slate-300 text-xl leading-none">×</button>
        </div>
        <div className="flex border-b border-slate-800">
          {(["scores","signals","action"] as const).map(t=>(
            <button key={t} onClick={()=>setTab(t)} className={`flex-1 py-2.5 text-xs font-medium capitalize transition-colors ${tab===t?"text-indigo-400 border-b-2 border-indigo-400":"text-slate-500 hover:text-slate-300"}`}>{t}</button>
          ))}
        </div>
        <div className="p-5 space-y-4">
          {tab==="scores" && (
            <>
              <div className="flex justify-between items-center">
                <span className="text-sm text-slate-400">Composite</span>
                <span className={`text-xl font-bold ${riskColor[rep.penetration_risk]||"text-slate-100"}`}>{rep.account_penetration_composite.toFixed(1)}</span>
              </div>
              <ScoreBar label="Account Coverage" value={rep.account_coverage_score}/>
              <ScoreBar label="Account Depth" value={rep.account_depth_score}/>
              <ScoreBar label="Strategic Focus" value={rep.strategic_focus_score}/>
              <ScoreBar label="Expansion Momentum" value={rep.expansion_momentum_score}/>
              <div className="pt-2 flex gap-4 text-xs text-slate-500">
                <span>Gap: <span className={rep.has_penetration_gap?"text-red-400":"text-emerald-400"}>{rep.has_penetration_gap?"Yes":"No"}</span></span>
                <span>Coaching: <span className={rep.requires_account_coaching?"text-orange-400":"text-emerald-400"}>{rep.requires_account_coaching?"Yes":"No"}</span></span>
                <span>Severity: <span className={severityColors[rep.penetration_severity]||"text-slate-300"}>{rep.penetration_severity}</span></span>
              </div>
            </>
          )}
          {tab==="signals" && (
            <div className="space-y-3">
              <p className="text-sm text-slate-300 leading-relaxed">{rep.penetration_signal}</p>
              <div className="bg-slate-800/50 rounded-lg p-3 space-y-1.5 text-xs text-slate-400">
                <div className="flex justify-between"><span>Risk Level</span><span className={`font-medium ${riskColor[rep.penetration_risk]}`}>{rep.penetration_risk}</span></div>
                <div className="flex justify-between"><span>Pattern</span><span className="font-medium text-slate-200">{rep.penetration_pattern.replace(/_/g," ")}</span></div>
                <div className="flex justify-between"><span>Severity</span><span className={`font-medium ${severityColors[rep.penetration_severity]||"text-slate-200"}`}>{rep.penetration_severity}</span></div>
                <div className="flex justify-between"><span>Untapped Revenue</span><span className="font-medium text-violet-400">{fmtUSD(rep.estimated_untapped_revenue_usd)}</span></div>
              </div>
            </div>
          )}
          {tab==="action" && (
            <div className="space-y-3">
              <div className={`rounded-lg p-3 border ${riskBorder[rep.penetration_risk]} ${riskBg[rep.penetration_risk]}`}>
                <p className="text-xs text-slate-400 mb-1">Recommended Action</p>
                <p className={`font-semibold ${riskColor[rep.penetration_risk]}`}>{actionLabels[rep.recommended_action]||rep.recommended_action}</p>
              </div>
              <p className="text-xs text-slate-500 leading-relaxed">
                Focus on expanding territory coverage, deepening account engagement through multi-threading, and ensuring strategic accounts receive appropriate executive attention.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default function SalesAccountPenetrationPage() {
  const [data, setData]       = useState<{reps:Rep[];summary:Summary}|null>(null);
  const [filter, setFilter]   = useState("all");
  const [patFilter, setPat]   = useState("all");
  const [selected, setSelected] = useState<Rep|null>(null);

  const load = useCallback(async () => {
    const params = new URLSearchParams();
    if (filter !== "all") params.set("risk", filter);
    if (patFilter !== "all") params.set("pattern", patFilter);
    const res = await fetch(`/api/sales-account-penetration-intelligence-engine?${params}`, { cache: "no-store" });
    if (res.ok) setData(await res.json());
  }, [filter, patFilter]);

  useEffect(() => { load(); }, [load]);

  const s = data?.summary;
  const reps = data?.reps ?? [];

  const riskColors:Record<string,string> = { low:"bg-emerald-500", moderate:"bg-yellow-500", high:"bg-orange-500", critical:"bg-red-500" };
  const patColors:Record<string,string>  = { none:"bg-slate-500", whitespace_neglect:"bg-red-500", shallow_coverage:"bg-orange-500", cherry_picking:"bg-yellow-500", churn_risk_blindness:"bg-violet-500", expansion_stagnation:"bg-blue-500" };
  const sevColors:Record<string,string>  = { optimal:"bg-emerald-500", developing:"bg-yellow-500", shallow:"bg-orange-500", stagnant:"bg-red-500" };
  const actColors:Record<string,string>  = { no_action:"bg-slate-500", territory_coverage_coaching:"bg-sky-500", account_prioritization_review:"bg-yellow-500", strategic_account_planning:"bg-orange-500", expansion_pipeline_build:"bg-violet-500", executive_engagement_program:"bg-red-500" };

  const distributions = [
    { title:"Risk Distribution",     counts:s?.risk_counts     ??{}, colors:riskColors },
    { title:"Pattern Distribution",  counts:s?.pattern_counts  ??{}, colors:patColors },
    { title:"Severity Distribution", counts:s?.severity_counts ??{}, colors:sevColors },
    { title:"Action Distribution",   counts:s?.action_counts   ??{}, colors:actColors },
  ] as Array<{title:string;counts:Record<string,number>;colors:Record<string,string>}>;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-slate-100">Account Penetration Intelligence</h1>
        <p className="text-sm text-slate-400 mt-1">Territory coverage depth · whitespace mapping · strategic account engagement</p>
      </div>

      {/* KPI strip */}
      <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-6 gap-3">
        {[
          { label:"Total Reps",          value: s?.total ?? 0,                     fmt:(v:number)=>v.toString() },
          { label:"Avg Composite",        value: s?.avg_account_penetration_composite??0, fmt:(v:number)=>v.toFixed(1) },
          { label:"Penetration Gaps",     value: s?.penetration_gap_count  ??0,       fmt:(v:number)=>v.toString() },
          { label:"Need Coaching",        value: s?.account_coaching_count ??0,        fmt:(v:number)=>v.toString() },
          { label:"Untapped Revenue",     value: s?.total_estimated_untapped_revenue_usd??0, fmt:fmtUSD },
          { label:"Avg Coverage Score",   value: s?.avg_account_coverage_score ??0,  fmt:(v:number)=>v.toFixed(1) },
        ].map(({label,value,fmt})=>(
          <div key={label} className="bg-slate-900 border border-slate-800 rounded-xl p-3 space-y-1">
            <p className="text-xs text-slate-400">{label}</p>
            <p className="text-xl font-bold text-slate-100">{fmt(value)}</p>
          </div>
        ))}
      </div>

      {/* Gauge rings */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5">
        <p className="text-sm font-medium text-slate-300 mb-4">Average Sub-Scores</p>
        <div className="flex flex-wrap justify-around gap-6">
          <GaugeRing label="Coverage" value={s?.avg_account_coverage_score??0}/>
          <GaugeRing label="Depth" value={s?.avg_account_depth_score??0}/>
          <GaugeRing label="Strategic Focus" value={s?.avg_strategic_focus_score??0}/>
          <GaugeRing label="Expansion" value={s?.avg_expansion_momentum_score??0}/>
        </div>
      </div>

      {/* Distributions */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        {distributions.map(d=>(
          <div key={d.title} className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <DistBar {...d}/>
          </div>
        ))}
      </div>

      {/* Filters */}
      <div className="flex flex-wrap gap-2">
        <span className="text-xs text-slate-500 self-center">Risk:</span>
        {["all","low","moderate","high","critical"].map(f=>(
          <button key={f} onClick={()=>setFilter(f)} className={`px-3 py-1 rounded-full text-xs font-medium transition-colors ${filter===f?"bg-indigo-600 text-white":"bg-slate-800 text-slate-400 hover:text-slate-200"}`}>{f}</button>
        ))}
        <span className="text-xs text-slate-500 self-center ml-2">Pattern:</span>
        {["all","whitespace_neglect","shallow_coverage","cherry_picking","churn_risk_blindness","expansion_stagnation","none"].map(f=>(
          <button key={f} onClick={()=>setPat(f)} className={`px-3 py-1 rounded-full text-xs font-medium transition-colors ${patFilter===f?"bg-violet-600 text-white":"bg-slate-800 text-slate-400 hover:text-slate-200"}`}>{f.replace(/_/g," ")}</button>
        ))}
      </div>

      {/* Rep cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {reps.map(rep=>(
          <button key={rep.rep_id} onClick={()=>setSelected(rep)} className={`bg-slate-900 border rounded-xl p-4 text-left space-y-3 hover:border-slate-600 transition-colors cursor-pointer ${riskBorder[rep.penetration_risk]}`}>
            <div className="flex items-center justify-between">
              <span className="font-semibold text-slate-100">{rep.rep_id}</span>
              <span className={`text-xs font-bold px-2 py-0.5 rounded-full ${riskBg[rep.penetration_risk]} ${riskColor[rep.penetration_risk]}`}>{rep.penetration_risk}</span>
            </div>
            <p className="text-xs text-slate-400">{rep.region}</p>
            <div className="space-y-1.5">
              <ScoreBar label="Coverage" value={rep.account_coverage_score}/>
              <ScoreBar label="Depth" value={rep.account_depth_score}/>
              <ScoreBar label="Strategic Focus" value={rep.strategic_focus_score}/>
            </div>
            <div className="flex justify-between items-center pt-1">
              <span className="text-xs text-slate-500">{rep.penetration_pattern.replace(/_/g," ")}</span>
              <span className="text-xs font-semibold text-violet-400">{fmtUSD(rep.estimated_untapped_revenue_usd)}</span>
            </div>
            <p className="text-xs text-slate-500 leading-relaxed line-clamp-2">{rep.penetration_signal}</p>
          </button>
        ))}
      </div>

      {selected && <DetailModal rep={selected} onClose={()=>setSelected(null)}/>}
    </div>
  );
}
