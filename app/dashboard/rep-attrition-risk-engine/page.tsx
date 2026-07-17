"use client";
import { useEffect, useState } from "react";

interface RepAttrition {
  rep_id: string; rep_name: string; region: string;
  attrition_risk: string; attrition_signal: string;
  compensation_health: string; retention_action: string;
  disengagement_score: number; compensation_risk_score: number;
  performance_satisfaction_score: number; social_risk_score: number;
  attrition_composite: number;
  is_flight_risk: boolean; needs_urgent_retention: boolean;
  estimated_pipeline_at_risk_usd: number;
  primary_attrition_signal: string;
  tenure_months: number; quota_attainment_pct: number;
  compensation_vs_market_pct: number;
}
interface Summary {
  total: number; risk_counts: Record<string,number>;
  signal_counts: Record<string,number>; compensation_counts: Record<string,number>;
  action_counts: Record<string,number>; avg_attrition_composite: number;
  flight_risk_count: number; urgent_retention_count: number;
  avg_disengagement_score: number; avg_compensation_risk_score: number;
  avg_performance_satisfaction_score: number; avg_social_risk_score: number;
  total_pipeline_at_risk_usd: number;
}
interface ApiData { reps: RepAttrition[]; summary: Summary; }

const RISK_COLORS: Record<string,string> = {
  low: "text-emerald-400", moderate: "text-amber-400",
  high: "text-orange-400", critical: "text-rose-400",
};
const RISK_BG: Record<string,string> = {
  low: "bg-emerald-900/40 text-emerald-300 border-emerald-700",
  moderate: "bg-amber-900/40 text-amber-300 border-amber-700",
  high: "bg-orange-900/40 text-orange-300 border-orange-700",
  critical: "bg-rose-900/40 text-rose-300 border-rose-700",
};
const SIGNAL_COLORS: Record<string,string> = {
  no_signal: "text-slate-400", early_warning: "text-amber-400",
  active_search: "text-orange-400", likely_departing: "text-rose-400",
};
const ACTION_LABELS: Record<string,string> = {
  maintain: "Maintain",
  recognition_and_development: "Recognition & Development",
  compensation_review: "Compensation Review",
  urgent_retention_meeting: "Urgent Retention Meeting",
};

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

function DetailModal({ rep, onClose }: { rep: RepAttrition; onClose: ()=>void }) {
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
            <h2 className="text-xl font-bold text-slate-100">{rep.rep_name}</h2>
            <div className="flex gap-3 mt-1 text-sm">
              <span className={RISK_COLORS[rep.attrition_risk]}>{rep.attrition_risk}</span>
              <span className="text-slate-500">•</span>
              <span className={SIGNAL_COLORS[rep.attrition_signal]}>{rep.attrition_signal.replace(/_/g," ")}</span>
              <span className="text-slate-500">•</span>
              <span className="text-slate-400">{rep.region}</span>
            </div>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-slate-300 text-2xl leading-none">×</button>
        </div>
        <div className="flex border-b border-slate-800">
          {(["overview","scores","signal"] as const).map(t=>(
            <button key={t} onClick={()=>setTab(t)}
              className={`px-5 py-3 text-sm font-medium capitalize transition-colors ${tab===t?"text-rose-400 border-b-2 border-rose-400":"text-slate-500 hover:text-slate-300"}`}>
              {t==="signal"?"Attrition Signal":t}
            </button>
          ))}
        </div>
        <div className="p-6">
          {tab==="overview" && (
            <div className="grid grid-cols-2 gap-4">
              {[
                ["Tenure", `${rep.tenure_months} months`],
                ["Quota Attainment", `${rep.quota_attainment_pct}%`],
                ["vs Market Comp", `${rep.compensation_vs_market_pct}%`],
                ["Pipeline at Risk", fmt(rep.estimated_pipeline_at_risk_usd)],
                ["Flight Risk", rep.is_flight_risk?"Yes":"No"],
                ["Urgent Retention", rep.needs_urgent_retention?"Yes":"No"],
                ["Comp Health", rep.compensation_health],
                ["Recommended Action", ACTION_LABELS[rep.retention_action]??rep.retention_action],
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
                ["Disengagement", rep.disengagement_score, "#f43f5e"],
                ["Comp Risk", rep.compensation_risk_score, "#f59e0b"],
                ["Perf Dissatisfaction", 100-rep.performance_satisfaction_score, "#fb923c"],
                ["Social Risk", rep.social_risk_score, "#a78bfa"],
              ].map(([label,val,col])=>(
                <div key={label as string} className="flex flex-col items-center gap-2">
                  <RingGauge value={val as number} size={90} color={col as string}/>
                  <span className="text-slate-400 text-sm text-center">{label as string}</span>
                </div>
              ))}
              <div className="col-span-2 bg-slate-800/50 rounded-xl p-4 text-center">
                <p className="text-slate-500 text-xs uppercase mb-1">Attrition Composite (higher = more risk)</p>
                <p className={`text-3xl font-bold ${rep.attrition_composite>=75?"text-rose-400":rep.attrition_composite>=55?"text-orange-400":rep.attrition_composite>=35?"text-amber-400":"text-emerald-400"}`}>
                  {rep.attrition_composite.toFixed(1)}
                </p>
              </div>
            </div>
          )}
          {tab==="signal" && (
            <div className="space-y-4">
              <div className="bg-slate-800/50 rounded-xl p-4">
                <p className="text-xs text-slate-500 uppercase mb-2">Primary Attrition Signal</p>
                <p className="text-slate-200">{rep.primary_attrition_signal}</p>
              </div>
              <div className={`rounded-xl p-4 border ${RISK_BG[rep.attrition_risk]}`}>
                <p className="text-xs uppercase mb-1 opacity-70">Risk Level</p>
                <p className="font-semibold capitalize">{rep.attrition_risk}</p>
              </div>
              <div className="bg-slate-800/50 rounded-xl p-4">
                <p className="text-xs text-slate-500 uppercase mb-2">Retention Action</p>
                <p className="text-slate-200 font-medium">{ACTION_LABELS[rep.retention_action]??rep.retention_action}</p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default function RepAttritionRiskPage() {
  const [data, setData]       = useState<ApiData|null>(null);
  const [loading, setLoading] = useState(true);
  const [riskF, setRiskF]     = useState("all");
  const [regionF, setRegionF] = useState("all");
  const [selected, setSelected] = useState<RepAttrition|null>(null);

  useEffect(() => {
    async function load() {
        setLoading(true);
        const p = new URLSearchParams();
        if (riskF !== "all")   p.set("risk", riskF);
        if (regionF !== "all") p.set("region", regionF);
        const res = await fetch(`/api/rep-attrition-risk-engine?${p}`);
        setData(await res.json());
        setLoading(false);
  }
    load();
  }, [riskF, regionF]);

  const s = data?.summary;
  const fmt = (n:number) => n>=1e6?`$${(n/1e6).toFixed(1)}M`:n>=1e3?`$${(n/1e3).toFixed(0)}K`:`$${n}`;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-slate-100">Rep Attrition Risk Engine</h1>
          <p className="text-slate-400 mt-1">Flight risk scoring, retention prioritization, and pipeline exposure from rep departures</p>
        </div>

        {s && (
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
            {[
              ["Total Reps", s.total, "text-slate-200"],
              ["Flight Risks", s.flight_risk_count, "text-rose-400"],
              ["Urgent Retention", s.urgent_retention_count, "text-orange-400"],
              ["Avg Risk Score", s.avg_attrition_composite, "text-amber-400"],
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
              ["Avg Disengagement", s.avg_disengagement_score, "#f43f5e"],
              ["Avg Comp Risk", s.avg_compensation_risk_score, "#f59e0b"],
              ["Avg Perf Sat", s.avg_performance_satisfaction_score, "#34d399"],
              ["Avg Social Risk", s.avg_social_risk_score, "#a78bfa"],
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
              <span className="text-slate-400 text-sm">Total Pipeline at Risk from Attrition</span>
              <span className="text-2xl font-bold text-rose-400">{fmt(s.total_pipeline_at_risk_usd)}</span>
            </div>
            {s.risk_counts && (
              <div className="flex gap-1 h-3 rounded-full overflow-hidden">
                {Object.entries(s.risk_counts).map(([k,v])=>(
                  <div key={k} style={{width:`${(v/s.total)*100}%`}}
                    className={k==="low"?"bg-emerald-500":k==="moderate"?"bg-amber-500":k==="high"?"bg-orange-500":"bg-rose-500"}
                    title={`${k}: ${v}`}/>
                ))}
              </div>
            )}
          </div>
        )}

        <div className="flex flex-wrap gap-3 mb-6">
          <div className="flex gap-2">
            {["all","low","moderate","high","critical"].map(v=>(
              <button key={v} onClick={()=>setRiskF(v)}
                className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-colors ${riskF===v?"bg-rose-700 text-white":"bg-slate-800 text-slate-400 hover:text-slate-200"}`}>
                {v==="all"?"All Risk":v}
              </button>
            ))}
          </div>
          <div className="flex gap-2">
            {["all","NAMER","EMEA","APAC","LATAM"].map(v=>(
              <button key={v} onClick={()=>setRegionF(v)}
                className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-colors ${regionF===v?"bg-indigo-600 text-white":"bg-slate-800 text-slate-400 hover:text-slate-200"}`}>
                {v==="all"?"All Regions":v}
              </button>
            ))}
          </div>
        </div>

        {loading && <div className="text-center text-slate-500 py-12">Loading...</div>}

        {!loading && data && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {data.reps.map(rep=>(
              <div key={rep.rep_id}
                className="bg-slate-900 border border-slate-800 rounded-xl p-5 cursor-pointer hover:border-slate-600 transition-all"
                onClick={()=>setSelected(rep)}>
                <div className="flex items-start justify-between mb-3">
                  <div>
                    <h3 className="font-semibold text-slate-200">{rep.rep_name}</h3>
                    <div className="flex gap-2 mt-1">
                      <span className={`text-xs font-medium ${SIGNAL_COLORS[rep.attrition_signal]}`}>
                        {rep.attrition_signal.replace(/_/g," ")}
                      </span>
                      <span className="text-slate-600">•</span>
                      <span className="text-xs text-slate-400">{rep.region}</span>
                    </div>
                  </div>
                  <span className={`text-xs px-2 py-1 rounded-full border ${RISK_BG[rep.attrition_risk]}`}>
                    {rep.attrition_risk}
                  </span>
                </div>
                <div className="flex items-center gap-4 mb-3">
                  <RingGauge value={rep.attrition_composite} size={64}
                    color={rep.attrition_composite>=75?"#f43f5e":rep.attrition_composite>=55?"#f97316":rep.attrition_composite>=35?"#f59e0b":"#34d399"}/>
                  <div className="flex-1">
                    <p className="text-xs text-slate-500 mb-1">Risk Drivers</p>
                    <div className="space-y-1">
                      {[
                        ["Dis", rep.disengagement_score, "#f43f5e"],
                        ["Comp", rep.compensation_risk_score, "#f59e0b"],
                        ["Social", rep.social_risk_score, "#a78bfa"],
                      ].map(([l,v,col])=>(
                        <div key={l as string} className="flex items-center gap-2">
                          <span className="text-xs text-slate-500 w-8">{l as string}</span>
                          <div className="flex-1 h-1.5 bg-slate-800 rounded-full">
                            <div className="h-full rounded-full" style={{width:`${v as number}%`,backgroundColor:col as string}}/>
                          </div>
                          <span className="text-xs text-slate-400 w-6">{v as number}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
                <div className="text-xs text-slate-400 truncate mb-2">{rep.primary_attrition_signal}</div>
                <div className="flex items-center justify-between text-xs">
                  <span className="text-slate-500">Pipeline risk: <span className="text-rose-400 font-medium">{fmt(rep.estimated_pipeline_at_risk_usd)}</span></span>
                  <div className="flex gap-1">
                    {rep.needs_urgent_retention && (
                      <span className="bg-rose-900/40 text-rose-300 border border-rose-700 px-2 py-0.5 rounded-full">Urgent</span>
                    )}
                    {rep.is_flight_risk && !rep.needs_urgent_retention && (
                      <span className="bg-orange-900/40 text-orange-300 border border-orange-700 px-2 py-0.5 rounded-full">At Risk</span>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
      {selected && <DetailModal rep={selected} onClose={()=>setSelected(null)}/>}
    </div>
  );
}
