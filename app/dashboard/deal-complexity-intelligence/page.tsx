"use client";
import { useEffect, useState, useCallback } from "react";

interface ComplexDeal {
  deal_id: string; rep_id: string; deal_name: string;
  complexity_tier: string; complexity_risk: string;
  primary_complexity_dimension: string; complexity_action: string;
  people_complexity_score: number; process_complexity_score: number;
  technology_complexity_score: number; legal_complexity_score: number;
  complexity_composite: number;
  requires_deal_desk: boolean; needs_executive_sponsor: boolean;
  estimated_win_probability_impact_pct: number;
  complexity_summary: string; deal_value_usd: number;
}
interface Summary {
  total: number; tier_counts: Record<string,number>;
  risk_counts: Record<string,number>; dimension_counts: Record<string,number>;
  action_counts: Record<string,number>; avg_complexity_composite: number;
  deal_desk_required_count: number; executive_sponsor_needed_count: number;
  avg_people_score: number; avg_process_score: number;
  avg_technology_score: number; avg_legal_score: number;
  high_complexity_pipeline_usd: number;
}
interface ApiData { deals: ComplexDeal[]; summary: Summary; }

const TIER_COLORS: Record<string,string> = {
  simple: "text-emerald-400", standard: "text-sky-400",
  complex: "text-amber-400", enterprise: "text-rose-400",
};
const RISK_BG: Record<string,string> = {
  low: "bg-emerald-900/40 text-emerald-300 border-emerald-700",
  moderate: "bg-amber-900/40 text-amber-300 border-amber-700",
  high: "bg-orange-900/40 text-orange-300 border-orange-700",
  critical: "bg-rose-900/40 text-rose-300 border-rose-700",
};
const DIM_COLORS: Record<string,string> = {
  people: "#60a5fa", process: "#34d399", technology: "#a78bfa", legal: "#f59e0b",
};
const ACTION_LABELS: Record<string,string> = {
  standard_process: "Standard Process",
  assign_solution_engineer: "Assign SE",
  executive_sponsor_required: "Executive Sponsor",
  dedicated_deal_team: "Dedicated Deal Team",
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

function DetailModal({ d, onClose }: { d: ComplexDeal; onClose: ()=>void }) {
  const [tab, setTab] = useState<"overview"|"scores"|"summary">("overview");
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
              <span className={TIER_COLORS[d.complexity_tier]}>{d.complexity_tier}</span>
              <span className="text-slate-500">•</span>
              <span className="text-slate-400">{fmt(d.deal_value_usd)}</span>
              <span className="text-slate-500">•</span>
              <span className="text-slate-400">{d.deal_id}</span>
            </div>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-slate-300 text-2xl leading-none">×</button>
        </div>
        <div className="flex border-b border-slate-800">
          {(["overview","scores","summary"] as const).map(t=>(
            <button key={t} onClick={()=>setTab(t)}
              className={`px-5 py-3 text-sm font-medium capitalize transition-colors ${tab===t?"text-sky-400 border-b-2 border-sky-400":"text-slate-500 hover:text-slate-300"}`}>
              {t==="summary"?"Complexity Summary":t}
            </button>
          ))}
        </div>
        <div className="p-6">
          {tab==="overview" && (
            <div className="grid grid-cols-2 gap-4">
              {[
                ["Deal Value", fmt(d.deal_value_usd)],
                ["Win Prob Impact", `${d.estimated_win_probability_impact_pct}%`],
                ["Requires Deal Desk", d.requires_deal_desk?"Yes":"No"],
                ["Needs Exec Sponsor", d.needs_executive_sponsor?"Yes":"No"],
                ["Primary Dimension", d.primary_complexity_dimension],
                ["Recommended Action", ACTION_LABELS[d.complexity_action]??d.complexity_action],
                ["Risk Level", d.complexity_risk],
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
                ["People", d.people_complexity_score, "#60a5fa"],
                ["Process", d.process_complexity_score, "#34d399"],
                ["Technology", d.technology_complexity_score, "#a78bfa"],
                ["Legal", d.legal_complexity_score, "#f59e0b"],
              ].map(([label,val,col])=>(
                <div key={label as string} className="flex flex-col items-center gap-2">
                  <RingGauge value={val as number} size={90} color={col as string}/>
                  <span className="text-slate-400 text-sm">{label as string}</span>
                </div>
              ))}
              <div className="col-span-2 bg-slate-800/50 rounded-xl p-4 text-center">
                <p className="text-slate-500 text-xs uppercase mb-1">Complexity Composite</p>
                <p className={`text-3xl font-bold ${d.complexity_composite>=70?"text-rose-400":d.complexity_composite>=50?"text-amber-400":d.complexity_composite>=25?"text-sky-400":"text-emerald-400"}`}>
                  {d.complexity_composite.toFixed(1)}
                </p>
              </div>
            </div>
          )}
          {tab==="summary" && (
            <div className="space-y-4">
              <div className="bg-slate-800/50 rounded-xl p-4">
                <p className="text-xs text-slate-500 uppercase mb-2">Complexity Summary</p>
                <p className="text-slate-200">{d.complexity_summary}</p>
              </div>
              <div className={`rounded-xl p-4 border ${RISK_BG[d.complexity_risk]}`}>
                <p className="text-xs uppercase mb-1 opacity-70">Risk Level</p>
                <p className="font-semibold capitalize">{d.complexity_risk}</p>
              </div>
              <div className="bg-slate-800/50 rounded-xl p-4">
                <p className="text-xs text-slate-500 uppercase mb-2">Recommended Action</p>
                <p className="text-slate-200 font-medium">{ACTION_LABELS[d.complexity_action]??d.complexity_action}</p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default function DealComplexityPage() {
  const [data, setData]     = useState<ApiData|null>(null);
  const [loading, setLoading] = useState(true);
  const [tierF, setTierF]   = useState("all");
  const [riskF, setRiskF]   = useState("all");
  const [selected, setSelected] = useState<ComplexDeal|null>(null);

  const load = useCallback(async () => {
    setLoading(true);
    const p = new URLSearchParams();
    if (tierF !== "all") p.set("tier", tierF);
    if (riskF !== "all") p.set("risk", riskF);
    const res = await fetch(`/api/deal-complexity-intelligence?${p}`);
    setData(await res.json());
    setLoading(false);
  }, [tierF, riskF]);

  useEffect(() => { load(); }, [load]);

  const s = data?.summary;
  const fmt = (n:number) => n>=1e6?`$${(n/1e6).toFixed(1)}M`:n>=1e3?`$${(n/1e3).toFixed(0)}K`:`$${n}`;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-slate-100">Deal Complexity Intelligence</h1>
          <p className="text-slate-400 mt-1">4-dimension complexity scoring across people, process, technology, and legal</p>
        </div>

        {s && (
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
            {[
              ["Total Deals", s.total, "text-slate-200"],
              ["Deal Desk Required", s.deal_desk_required_count, "text-amber-400"],
              ["Exec Sponsor Needed", s.executive_sponsor_needed_count, "text-orange-400"],
              ["Avg Complexity", s.avg_complexity_composite, "text-sky-400"],
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
              ["Avg People", s.avg_people_score, "#60a5fa"],
              ["Avg Process", s.avg_process_score, "#34d399"],
              ["Avg Technology", s.avg_technology_score, "#a78bfa"],
              ["Avg Legal", s.avg_legal_score, "#f59e0b"],
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
              <span className="text-slate-400 text-sm">High Complexity Pipeline (&gt;50 composite)</span>
              <span className="text-2xl font-bold text-amber-400">{fmt(s.high_complexity_pipeline_usd)}</span>
            </div>
            {s.tier_counts && (
              <div className="flex gap-1 h-3 rounded-full overflow-hidden">
                {Object.entries(s.tier_counts).map(([k,v])=>(
                  <div key={k} style={{width:`${(v/s.total)*100}%`}}
                    className={k==="simple"?"bg-emerald-500":k==="standard"?"bg-sky-500":k==="complex"?"bg-amber-500":"bg-rose-500"}
                    title={`${k}: ${v}`}/>
                ))}
              </div>
            )}
          </div>
        )}

        <div className="flex flex-wrap gap-3 mb-6">
          <div className="flex gap-2">
            {["all","simple","standard","complex","enterprise"].map(v=>(
              <button key={v} onClick={()=>setTierF(v)}
                className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-colors ${tierF===v?"bg-sky-700 text-white":"bg-slate-800 text-slate-400 hover:text-slate-200"}`}>
                {v==="all"?"All Tiers":v}
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
                      <span className={`text-xs font-medium ${TIER_COLORS[d.complexity_tier]}`}>{d.complexity_tier}</span>
                      <span className="text-slate-600">•</span>
                      <span className="text-xs text-slate-400">{fmt(d.deal_value_usd)}</span>
                    </div>
                  </div>
                  <span className={`text-xs px-2 py-1 rounded-full border ${RISK_BG[d.complexity_risk]}`}>
                    {d.complexity_risk}
                  </span>
                </div>
                <div className="flex items-center gap-4 mb-3">
                  <RingGauge value={d.complexity_composite} size={64}
                    color={d.complexity_composite>=70?"#f43f5e":d.complexity_composite>=50?"#f59e0b":d.complexity_composite>=25?"#60a5fa":"#34d399"}/>
                  <div className="flex-1">
                    <p className="text-xs text-slate-500 mb-1">Dimensions</p>
                    <div className="space-y-1">
                      {[
                        ["Ppl", d.people_complexity_score, DIM_COLORS.people],
                        ["Pro", d.process_complexity_score, DIM_COLORS.process],
                        ["Tech", d.technology_complexity_score, DIM_COLORS.technology],
                        ["Legal", d.legal_complexity_score, DIM_COLORS.legal],
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
                <div className="text-xs text-slate-400 truncate mb-2">{d.complexity_summary}</div>
                <div className="flex items-center justify-between text-xs">
                  <span className="text-slate-500">Win impact: <span className="text-rose-400 font-medium">{d.estimated_win_probability_impact_pct}%</span></span>
                  <div className="flex gap-1">
                    {d.needs_executive_sponsor && (
                      <span className="bg-orange-900/40 text-orange-300 border border-orange-700 px-2 py-0.5 rounded-full">Exec</span>
                    )}
                    {d.requires_deal_desk && (
                      <span className="bg-amber-900/40 text-amber-300 border border-amber-700 px-2 py-0.5 rounded-full">Deal Desk</span>
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
