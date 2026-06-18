"use client";
import { useEffect, useState, useCallback } from "react";

interface AgingDeal {
  deal_id: string; rep_id: string; deal_name: string;
  decay_status: string; decay_risk: string;
  stage_velocity: string; recovery_action: string;
  activity_decay_score: number; engagement_decay_score: number;
  velocity_decay_score: number; stage_health_score: number;
  decay_composite: number;
  is_stale: boolean; needs_immediate_action: boolean;
  recovery_probability_pct: number;
  primary_decay_signal: string;
  deal_value_usd: number; deal_stage: number;
}
interface Summary {
  total: number; decay_status_counts: Record<string,number>;
  risk_counts: Record<string,number>; velocity_counts: Record<string,number>;
  action_counts: Record<string,number>; avg_decay_composite: number;
  stale_deal_count: number; immediate_action_count: number;
  avg_activity_decay_score: number; avg_engagement_decay_score: number;
  avg_velocity_decay_score: number; avg_stage_health_score: number;
  total_stale_pipeline_usd: number;
}
interface ApiData { deals: AgingDeal[]; summary: Summary; }

const STATUS_COLORS: Record<string,string> = {
  fresh: "text-emerald-400", aging: "text-amber-400",
  stale: "text-orange-400", dead: "text-rose-400",
};
const RISK_BG: Record<string,string> = {
  low: "bg-emerald-900/40 text-emerald-300 border-emerald-700",
  moderate: "bg-amber-900/40 text-amber-300 border-amber-700",
  high: "bg-orange-900/40 text-orange-300 border-orange-700",
  critical: "bg-rose-900/40 text-rose-300 border-rose-700",
};
const ACTION_LABELS: Record<string,string> = {
  maintain: "Maintain",
  re_engage_champion: "Re-Engage Champion",
  executive_escalation: "Executive Escalation",
  kill_or_recycle: "Kill or Recycle",
};
const STAGE_LABELS = ["Prospect","Qualified","Discovery","Proposal","Negotiation","Closing"];

function RingGauge({ value, size=80, color="#818cf8", invert=false }:
  { value:number; size?:number; color?:string; invert?:boolean }) {
  const display = invert ? 100 - value : value;
  const r = (size-12)/2, circ = 2*Math.PI*r;
  const fill = (display/100)*circ;
  return (
    <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`}>
      <circle cx={size/2} cy={size/2} r={r} fill="none" stroke="#1e293b" strokeWidth={6}/>
      <circle cx={size/2} cy={size/2} r={r} fill="none" stroke={color} strokeWidth={6}
        strokeDasharray={`${fill} ${circ}`} strokeLinecap="round"
        transform={`rotate(-90 ${size/2} ${size/2})`}/>
      <text x={size/2} y={size/2+5} textAnchor="middle" fontSize={size>70?14:11}
        fill="#f1f5f9" fontWeight="bold">{Math.round(display)}</text>
    </svg>
  );
}

function DetailModal({ d, onClose }: { d: AgingDeal; onClose: ()=>void }) {
  const [tab, setTab] = useState<"overview"|"scores"|"signal">("overview");
  useEffect(() => {
    const h = (e: KeyboardEvent) => { if (e.key==="Escape") onClose(); };
    window.addEventListener("keydown", h);
    return () => window.removeEventListener("keydown", h);
  }, [onClose]);
  const fmt = (n:number) => n>=1e6?`$${(n/1e6).toFixed(1)}M`:n>=1e3?`$${(n/1e3).toFixed(0)}K`:`$${n}`;
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4" onClick={onClose}>
      <div className="absolute inset-0 bg-black/60 backdrop-blur-sm"/>
      <div className="relative bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-2xl shadow-2xl"
           onClick={e=>e.stopPropagation()}>
        <div className="flex items-start justify-between p-6 border-b border-slate-800">
          <div>
            <h2 className="text-xl font-bold text-slate-100">{d.deal_name}</h2>
            <div className="flex gap-3 mt-1 text-sm">
              <span className={STATUS_COLORS[d.decay_status]}>{d.decay_status}</span>
              <span className="text-slate-500">•</span>
              <span className="text-slate-400">{STAGE_LABELS[d.deal_stage]??`Stage ${d.deal_stage}`}</span>
              <span className="text-slate-500">•</span>
              <span className="text-slate-400">{fmt(d.deal_value_usd)}</span>
            </div>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-slate-300 text-2xl leading-none">×</button>
        </div>
        <div className="flex border-b border-slate-800">
          {(["overview","scores","signal"] as const).map(t=>(
            <button key={t} onClick={()=>setTab(t)}
              className={`px-5 py-3 text-sm font-medium capitalize transition-colors ${tab===t?"text-amber-400 border-b-2 border-amber-400":"text-slate-500 hover:text-slate-300"}`}>
              {t==="signal"?"Decay Signal":t}
            </button>
          ))}
        </div>
        <div className="p-6">
          {tab==="overview" && (
            <div className="grid grid-cols-2 gap-4">
              {[
                ["Deal Value", fmt(d.deal_value_usd)],
                ["Recovery Probability", `${d.recovery_probability_pct.toFixed(1)}%`],
                ["Stage Velocity", d.stage_velocity],
                ["Is Stale", d.is_stale?"Yes":"No"],
                ["Immediate Action Needed", d.needs_immediate_action?"Yes":"No"],
                ["Recommended Action", ACTION_LABELS[d.recovery_action]??d.recovery_action],
                ["Risk Level", d.decay_risk],
                ["Rep ID", d.rep_id],
              ].map(([k,v])=>(
                <div key={k} className="bg-slate-800/50 rounded-lg p-3">
                  <p className="text-xs text-slate-500 uppercase tracking-wide">{k}</p>
                  <p className="text-slate-200 font-semibold mt-1">{v}</p>
                </div>
              ))}
            </div>
          )}
          {tab==="scores" && (
            <div className="grid grid-cols-2 gap-6">
              {[
                ["Activity Decay", d.activity_decay_score, "#f43f5e", false],
                ["Engagement Decay", d.engagement_decay_score, "#f97316", false],
                ["Velocity Decay", d.velocity_decay_score, "#f59e0b", false],
                ["Stage Health", d.stage_health_score, "#34d399", false],
              ].map(([label,val,col,inv])=>(
                <div key={label as string} className="flex flex-col items-center gap-2">
                  <RingGauge value={val as number} size={90} color={col as string} invert={inv as boolean}/>
                  <span className="text-slate-400 text-sm">{label as string}</span>
                </div>
              ))}
              <div className="col-span-2 bg-slate-800/50 rounded-xl p-4 text-center">
                <p className="text-slate-500 text-xs uppercase mb-1">Decay Composite (higher = worse)</p>
                <p className={`text-3xl font-bold ${d.decay_composite>=70?"text-rose-400":d.decay_composite>=50?"text-orange-400":d.decay_composite>=30?"text-amber-400":"text-emerald-400"}`}>
                  {d.decay_composite.toFixed(1)}
                </p>
              </div>
            </div>
          )}
          {tab==="signal" && (
            <div className="space-y-4">
              <div className="bg-slate-800/50 rounded-xl p-4">
                <p className="text-xs text-slate-500 uppercase mb-2">Primary Decay Signal</p>
                <p className="text-slate-200">{d.primary_decay_signal}</p>
              </div>
              <div className={`rounded-xl p-4 border ${RISK_BG[d.decay_risk]}`}>
                <p className="text-xs uppercase mb-1 opacity-70">Risk Level</p>
                <p className="font-semibold capitalize">{d.decay_risk}</p>
              </div>
              <div className="bg-slate-800/50 rounded-xl p-4">
                <p className="text-xs text-slate-500 uppercase mb-2">Recovery Action</p>
                <p className="text-slate-200 font-medium">{ACTION_LABELS[d.recovery_action]??d.recovery_action}</p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default function PipelineAgingPage() {
  const [data, setData]       = useState<ApiData|null>(null);
  const [loading, setLoading] = useState(true);
  const [statusF, setStatusF] = useState("all");
  const [riskF, setRiskF]     = useState("all");
  const [selected, setSelected] = useState<AgingDeal|null>(null);

  const load = useCallback(async () => {
    setLoading(true);
    const p = new URLSearchParams();
    if (statusF !== "all") p.set("status", statusF);
    if (riskF !== "all")   p.set("risk", riskF);
    const res = await fetch(`/api/pipeline-aging-intelligence?${p}`);
    setData(await res.json());
    setLoading(false);
  }, [statusF, riskF]);

  useEffect(() => { load(); }, [load]);

  const s = data?.summary;
  const fmt = (n:number) => n>=1e6?`$${(n/1e6).toFixed(1)}M`:n>=1e3?`$${(n/1e3).toFixed(0)}K`:`$${n}`;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-slate-100">Pipeline Aging & Decay Intelligence</h1>
          <p className="text-slate-400 mt-1">Deal freshness scoring, stale pipeline detection, and recovery prioritization</p>
        </div>

        {s && (
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
            {[
              ["Total Deals", s.total, "text-slate-200"],
              ["Stale Deals", s.stale_deal_count, "text-orange-400"],
              ["Immediate Action", s.immediate_action_count, "text-rose-400"],
              ["Avg Decay Score", s.avg_decay_composite, "text-amber-400"],
            ].map(([label,val,cls])=>(
              <div key={label as string} className="bg-slate-900 border border-slate-800 rounded-xl p-5">
                <p className="text-slate-500 text-xs uppercase tracking-wide">{label as string}</p>
                <p className={`text-3xl font-bold mt-1 ${cls as string}`}>{val as number}</p>
              </div>
            ))}
          </div>
        )}

        {s && (
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
            {[
              ["Avg Activity Decay", s.avg_activity_decay_score, "#f43f5e"],
              ["Avg Engagement Decay", s.avg_engagement_decay_score, "#f97316"],
              ["Avg Velocity Decay", s.avg_velocity_decay_score, "#f59e0b"],
              ["Avg Stage Health", s.avg_stage_health_score, "#34d399"],
            ].map(([label,val,col])=>(
              <div key={label as string} className="bg-slate-900 border border-slate-800 rounded-xl p-4 flex items-center gap-4">
                <RingGauge value={val as number} size={70} color={col as string}/>
                <div>
                  <p className="text-xs text-slate-500">{label as string}</p>
                  <p className="text-lg font-bold text-slate-200">{(val as number).toFixed(1)}</p>
                </div>
              </div>
            ))}
          </div>
        )}

        {s && (
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 mb-8">
            <div className="flex items-center justify-between mb-3">
              <span className="text-slate-400 text-sm">Stale Pipeline Value</span>
              <span className="text-2xl font-bold text-orange-400">{fmt(s.total_stale_pipeline_usd)}</span>
            </div>
            {s.decay_status_counts && (
              <div className="flex gap-1 h-3 rounded-full overflow-hidden">
                {Object.entries(s.decay_status_counts).map(([k,v])=>(
                  <div key={k} style={{width:`${(v/s.total)*100}%`}}
                    className={k==="fresh"?"bg-emerald-500":k==="aging"?"bg-amber-500":k==="stale"?"bg-orange-500":"bg-rose-500"}
                    title={`${k}: ${v}`}/>
                ))}
              </div>
            )}
          </div>
        )}

        <div className="flex flex-wrap gap-3 mb-6">
          <div className="flex gap-2">
            {["all","fresh","aging","stale","dead"].map(v=>(
              <button key={v} onClick={()=>setStatusF(v)}
                className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-colors ${statusF===v?"bg-amber-700 text-white":"bg-slate-800 text-slate-400 hover:text-slate-200"}`}>
                {v==="all"?"All Status":v}
              </button>
            ))}
          </div>
          <div className="flex gap-2">
            {["all","critical","high","moderate","low"].map(v=>(
              <button key={v} onClick={()=>setRiskF(v)}
                className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-colors ${riskF===v?"bg-rose-700 text-white":"bg-slate-800 text-slate-400 hover:text-slate-200"}`}>
                {v==="all"?"All Risk":v}
              </button>
            ))}
          </div>
        </div>

        {loading && <div className="text-center text-slate-500 py-12">Loading...</div>}

        {!loading && data && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {data.deals.map(d=>(
              <div key={d.deal_id}
                className="bg-slate-900 border border-slate-800 rounded-xl p-5 cursor-pointer hover:border-slate-600 transition-all"
                onClick={()=>setSelected(d)}>
                <div className="flex items-start justify-between mb-3">
                  <div>
                    <h3 className="font-semibold text-slate-200">{d.deal_name}</h3>
                    <div className="flex gap-2 mt-1">
                      <span className={`text-xs font-medium ${STATUS_COLORS[d.decay_status]}`}>{d.decay_status}</span>
                      <span className="text-slate-600">•</span>
                      <span className="text-xs text-slate-400">{STAGE_LABELS[d.deal_stage]??`Stage ${d.deal_stage}`}</span>
                    </div>
                  </div>
                  <span className={`text-xs px-2 py-1 rounded-full border ${RISK_BG[d.decay_risk]}`}>
                    {d.decay_risk}
                  </span>
                </div>
                <div className="flex items-center gap-4 mb-3">
                  <RingGauge value={d.decay_composite} size={64}
                    color={d.decay_composite>=70?"#f43f5e":d.decay_composite>=50?"#f97316":d.decay_composite>=30?"#f59e0b":"#34d399"}/>
                  <div className="flex-1">
                    <p className="text-xs text-slate-500 mb-1">Decay Drivers</p>
                    <div className="space-y-1">
                      {[
                        ["Act", d.activity_decay_score, "#f43f5e"],
                        ["Eng", d.engagement_decay_score, "#f97316"],
                        ["Vel", d.velocity_decay_score, "#f59e0b"],
                      ].map(([l,v,col])=>(
                        <div key={l as string} className="flex items-center gap-2">
                          <span className="text-xs text-slate-500 w-7">{l as string}</span>
                          <div className="flex-1 h-1.5 bg-slate-800 rounded-full">
                            <div className="h-full rounded-full" style={{width:`${v as number}%`,backgroundColor:col as string}}/>
                          </div>
                          <span className="text-xs text-slate-400 w-6">{v as number}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
                <div className="text-xs text-slate-400 truncate mb-2">{d.primary_decay_signal}</div>
                <div className="flex items-center justify-between text-xs">
                  <span className="text-slate-500">Recovery: <span className="text-emerald-400 font-medium">{d.recovery_probability_pct.toFixed(0)}%</span></span>
                  <div className="flex gap-1">
                    {d.needs_immediate_action && (
                      <span className="bg-rose-900/40 text-rose-300 border border-rose-700 px-2 py-0.5 rounded-full">Action!</span>
                    )}
                    {d.is_stale && !d.needs_immediate_action && (
                      <span className="bg-orange-900/40 text-orange-300 border border-orange-700 px-2 py-0.5 rounded-full">Stale</span>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
      {selected && <DetailModal d={selected} onClose={()=>setSelected(null)}/>}
    </div>
  );
}
