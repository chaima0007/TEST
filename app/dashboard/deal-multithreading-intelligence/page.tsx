"use client";
import { useEffect, useState, useCallback } from "react";

interface Deal {
  deal_id: string; rep_id: string; deal_name: string;
  threading_status: string; threading_risk: string;
  stakeholder_coverage: string; threading_action: string;
  coverage_score: number; engagement_score: number;
  executive_access_score: number; resilience_score: number;
  threading_composite: number;
  is_single_threaded: boolean; needs_executive_access: boolean;
  estimated_risk_exposure_usd: number;
  primary_threading_gap: string;
  deal_value_usd: number; deal_stage: number;
}
interface Summary {
  total: number; threading_status_counts: Record<string,number>;
  risk_counts: Record<string,number>; coverage_counts: Record<string,number>;
  action_counts: Record<string,number>; avg_threading_composite: number;
  single_threaded_count: number; executive_access_needed_count: number;
  avg_coverage_score: number; avg_engagement_score: number;
  avg_executive_access_score: number; avg_resilience_score: number;
  total_at_risk_pipeline_usd: number;
}
interface ApiData { deals: Deal[]; summary: Summary; }

const STATUS_COLORS: Record<string,string> = {
  well_threaded: "text-emerald-400",
  adequately_threaded: "text-sky-400",
  at_risk: "text-amber-400",
  single_threaded: "text-rose-400",
};
const RISK_BG: Record<string,string> = {
  low: "bg-emerald-900/40 text-emerald-300 border-emerald-700",
  moderate: "bg-amber-900/40 text-amber-300 border-amber-700",
  high: "bg-orange-900/40 text-orange-300 border-orange-700",
  critical: "bg-rose-900/40 text-rose-300 border-rose-700",
};
const ACTION_LABELS: Record<string,string> = {
  emergency_executive_outreach: "Emergency Exec Outreach",
  expand_stakeholder_map: "Expand Stakeholder Map",
  strengthen_existing: "Strengthen Existing",
  maintain: "Maintain",
};
const STAGE_LABELS = ["Early", "Mid", "Late"];

function RingGauge({ value, size=80, color="#818cf8" }: { value:number; size?:number; color?:string }) {
  const r = (size-12)/2, circ = 2*Math.PI*r;
  const fill = (value/100)*circ;
  return (
    <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`}>
      <circle cx={size/2} cy={size/2} r={r} fill="none" stroke="#1e293b" strokeWidth={6}/>
      <circle cx={size/2} cy={size/2} r={r} fill="none" stroke={color} strokeWidth={6}
        strokeDasharray={`${fill} ${circ}`} strokeLinecap="round"
        transform={`rotate(-90 ${size/2} ${size/2})`}/>
      <text x={size/2} y={size/2+5} textAnchor="middle" fontSize={size>70?14:11}
        fill="#f1f5f9" fontWeight="bold">{Math.round(value)}</text>
    </svg>
  );
}

function DetailModal({ d, onClose }: { d: Deal; onClose: ()=>void }) {
  const [tab, setTab] = useState<"overview"|"scores"|"gap">("overview");
  useEffect(() => {
    const h = (e: KeyboardEvent) => { if (e.key==="Escape") onClose(); };
    window.addEventListener("keydown", h);
    return () => window.removeEventListener("keydown", h);
  }, [onClose]);
  const fmt = (n:number) => n>=1e6 ? `$${(n/1e6).toFixed(1)}M` : n>=1e3 ? `$${(n/1e3).toFixed(0)}K` : `$${n}`;
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4" onClick={onClose}>
      <div className="absolute inset-0 bg-black/60 backdrop-blur-sm"/>
      <div className="relative bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-2xl shadow-2xl"
           onClick={e=>e.stopPropagation()}>
        <div className="flex items-start justify-between p-6 border-b border-slate-800">
          <div>
            <h2 className="text-xl font-bold text-slate-100">{d.deal_name}</h2>
            <div className="flex gap-3 mt-1 text-sm">
              <span className={STATUS_COLORS[d.threading_status]}>{d.threading_status.replace(/_/g," ")}</span>
              <span className="text-slate-500">•</span>
              <span className="text-slate-400">Stage: {STAGE_LABELS[d.deal_stage]??d.deal_stage}</span>
              <span className="text-slate-500">•</span>
              <span className="text-slate-400">{d.deal_id}</span>
            </div>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-slate-300 text-2xl leading-none">×</button>
        </div>
        <div className="flex border-b border-slate-800">
          {(["overview","scores","gap"] as const).map(t=>(
            <button key={t} onClick={()=>setTab(t)}
              className={`px-5 py-3 text-sm font-medium capitalize transition-colors ${tab===t?"text-indigo-400 border-b-2 border-indigo-400":"text-slate-500 hover:text-slate-300"}`}>
              {t==="gap"?"Threading Gap":t}
            </button>
          ))}
        </div>
        <div className="p-6">
          {tab==="overview" && (
            <div className="grid grid-cols-2 gap-4">
              {[
                ["Deal Value", fmt(d.deal_value_usd)],
                ["Risk Exposure", fmt(d.estimated_risk_exposure_usd)],
                ["Single Threaded", d.is_single_threaded?"Yes":"No"],
                ["Needs Exec Access", d.needs_executive_access?"Yes":"No"],
                ["Coverage", d.stakeholder_coverage],
                ["Recommended Action", ACTION_LABELS[d.threading_action]??d.threading_action],
                ["Risk Level", d.threading_risk],
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
                ["Coverage", d.coverage_score, "#60a5fa"],
                ["Engagement", d.engagement_score, "#34d399"],
                ["Exec Access", d.executive_access_score, "#a78bfa"],
                ["Resilience", d.resilience_score, "#f59e0b"],
              ].map(([label,val,col])=>(
                <div key={label as string} className="flex flex-col items-center gap-2">
                  <RingGauge value={val as number} size={90} color={col as string}/>
                  <span className="text-slate-400 text-sm">{label as string}</span>
                </div>
              ))}
              <div className="col-span-2 bg-slate-800/50 rounded-xl p-4 text-center">
                <p className="text-slate-500 text-xs uppercase mb-1">Threading Composite</p>
                <p className="text-3xl font-bold text-indigo-400">{d.threading_composite.toFixed(1)}</p>
              </div>
            </div>
          )}
          {tab==="gap" && (
            <div className="space-y-4">
              <div className="bg-slate-800/50 rounded-xl p-4">
                <p className="text-xs text-slate-500 uppercase mb-2">Primary Threading Gap</p>
                <p className="text-slate-200">{d.primary_threading_gap}</p>
              </div>
              <div className={`rounded-xl p-4 border ${RISK_BG[d.threading_risk]}`}>
                <p className="text-xs uppercase mb-1 opacity-70">Risk Level</p>
                <p className="font-semibold capitalize">{d.threading_risk}</p>
              </div>
              <div className="bg-slate-800/50 rounded-xl p-4">
                <p className="text-xs text-slate-500 uppercase mb-2">Recommended Action</p>
                <p className="text-slate-200 font-medium">{ACTION_LABELS[d.threading_action]??d.threading_action}</p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default function DealMultithreadingIntelligencePage() {
  const [data, setData]       = useState<ApiData|null>(null);
  const [loading, setLoading] = useState(true);
  const [statusF, setStatusF] = useState("all");
  const [riskF, setRiskF]     = useState("all");
  const [selected, setSelected] = useState<Deal|null>(null);

  const load = useCallback(async () => {
    setLoading(true);
    const p = new URLSearchParams();
    if (statusF !== "all") p.set("status", statusF);
    if (riskF !== "all")   p.set("risk", riskF);
    const res = await fetch(`/api/deal-multithreading-intelligence?${p}`);
    setData(await res.json());
    setLoading(false);
  }, [statusF, riskF]);

  useEffect(() => { load(); }, [load]);

  const s = data?.summary;
  const fmt = (n:number) => n>=1e6 ? `$${(n/1e6).toFixed(1)}M` : n>=1e3 ? `$${(n/1e3).toFixed(0)}K` : `$${n}`;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-slate-100">Deal Multithreading Intelligence</h1>
          <p className="text-slate-400 mt-1">Stakeholder coverage, executive access, and single-threaded deal risk</p>
        </div>

        {s && (
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
            {[
              ["Total Deals", s.total, "text-slate-200"],
              ["Single Threaded", s.single_threaded_count, "text-rose-400"],
              ["Need Exec Access", s.executive_access_needed_count, "text-amber-400"],
              ["Avg Composite", s.avg_threading_composite, "text-indigo-400"],
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
              ["Avg Coverage", s.avg_coverage_score, "#60a5fa"],
              ["Avg Engagement", s.avg_engagement_score, "#34d399"],
              ["Avg Exec Access", s.avg_executive_access_score, "#a78bfa"],
              ["Avg Resilience", s.avg_resilience_score, "#f59e0b"],
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
              <span className="text-slate-400 text-sm">Total At-Risk Pipeline</span>
              <span className="text-2xl font-bold text-rose-400">{fmt(s.total_at_risk_pipeline_usd)}</span>
            </div>
            {s.threading_status_counts && (
              <div className="flex gap-1 h-3 rounded-full overflow-hidden">
                {Object.entries(s.threading_status_counts).map(([k,v])=>(
                  <div key={k} style={{width:`${(v/s.total)*100}%`}}
                    className={k==="well_threaded"?"bg-emerald-500":k==="adequately_threaded"?"bg-sky-500":k==="at_risk"?"bg-amber-500":"bg-rose-500"}
                    title={`${k}: ${v}`}/>
                ))}
              </div>
            )}
          </div>
        )}

        <div className="flex flex-wrap gap-3 mb-6">
          <div className="flex gap-2">
            {["all","well_threaded","adequately_threaded","at_risk","single_threaded"].map(v=>(
              <button key={v} onClick={()=>setStatusF(v)}
                className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-colors ${statusF===v?"bg-indigo-600 text-white":"bg-slate-800 text-slate-400 hover:text-slate-200"}`}>
                {v==="all"?"All Status":v.replace(/_/g," ")}
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
                      <span className={`text-xs font-medium ${STATUS_COLORS[d.threading_status]}`}>
                        {d.threading_status.replace(/_/g," ")}
                      </span>
                      <span className="text-slate-600">•</span>
                      <span className="text-xs text-slate-400">Stage: {STAGE_LABELS[d.deal_stage]??d.deal_stage}</span>
                    </div>
                  </div>
                  <span className={`text-xs px-2 py-1 rounded-full border ${RISK_BG[d.threading_risk]}`}>
                    {d.threading_risk}
                  </span>
                </div>
                <div className="flex items-center gap-4 mb-3">
                  <RingGauge value={d.threading_composite} size={64} color="#818cf8"/>
                  <div className="flex-1">
                    <p className="text-xs text-slate-500 mb-1">Scores</p>
                    <div className="space-y-1">
                      {[
                        ["Cov", d.coverage_score, "#60a5fa"],
                        ["Eng", d.engagement_score, "#34d399"],
                        ["Exec", d.executive_access_score, "#a78bfa"],
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
                <div className="text-xs text-slate-400 truncate mb-2">{d.primary_threading_gap}</div>
                <div className="flex items-center justify-between text-xs">
                  <span className="text-slate-500">Risk: <span className="text-rose-400 font-medium">{fmt(d.estimated_risk_exposure_usd)}</span></span>
                  <div className="flex gap-1">
                    {d.is_single_threaded && (
                      <span className="bg-rose-900/40 text-rose-300 border border-rose-700 px-2 py-0.5 rounded-full">Single</span>
                    )}
                    {d.needs_executive_access && (
                      <span className="bg-amber-900/40 text-amber-300 border border-amber-700 px-2 py-0.5 rounded-full">No Exec</span>
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
