"use client";
import { useEffect, useState } from "react";

interface CustomerRep {
  customer_id: string; customer_name: string; rep_id: string;
  referral_velocity: string; advocacy_level: string;
  referral_risk: string; referral_action: string;
  advocacy_score: number; relationship_depth_score: number;
  referral_propensity_score: number; advocacy_impact_score: number;
  referral_composite: number; estimated_referral_pipeline_usd: number;
  is_active_referrer: boolean; needs_advocacy_activation: boolean;
  primary_advocacy_signal: string;
  contract_value_usd: number; nps_score: number;
}
interface Summary {
  total: number; velocity_counts: Record<string,number>;
  advocacy_counts: Record<string,number>; risk_counts: Record<string,number>;
  action_counts: Record<string,number>; avg_referral_composite: number;
  active_referrer_count: number; activation_needed_count: number;
  avg_advocacy_score: number; avg_relationship_depth_score: number;
  avg_referral_propensity_score: number; avg_advocacy_impact_score: number;
  total_estimated_referral_pipeline_usd: number;
}
interface ApiData { customers: CustomerRep[]; summary: Summary; }

const VELOCITY_COLORS: Record<string,string> = {
  accelerating: "text-emerald-400", steady: "text-sky-400",
  declining: "text-amber-400", inactive: "text-slate-400",
};
const ADVOCACY_COLORS: Record<string,string> = {
  champion: "text-violet-400", promoter: "text-indigo-400",
  passive: "text-slate-400", detractor: "text-rose-400",
};
const RISK_BG: Record<string,string> = {
  low: "bg-emerald-900/40 text-emerald-300 border-emerald-700",
  moderate: "bg-amber-900/40 text-amber-300 border-amber-700",
  high: "bg-orange-900/40 text-orange-300 border-orange-700",
  critical: "bg-rose-900/40 text-rose-300 border-rose-700",
};
const ACTION_LABELS: Record<string,string> = {
  activate_referral: "Activate Referral", nurture_advocate: "Nurture Advocate",
  re_engage: "Re-Engage", convert_detractor: "Convert Detractor",
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

function DetailModal({ c, onClose }: { c: CustomerRep; onClose: ()=>void }) {
  const [tab, setTab] = useState<"overview"|"scores"|"signals">("overview");
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
            <h2 className="text-xl font-bold text-slate-100">{c.customer_name}</h2>
            <div className="flex gap-3 mt-1 text-sm">
              <span className={VELOCITY_COLORS[c.referral_velocity]}>{c.referral_velocity}</span>
              <span className="text-slate-500">•</span>
              <span className={ADVOCACY_COLORS[c.advocacy_level]}>{c.advocacy_level}</span>
              <span className="text-slate-500">•</span>
              <span className="text-slate-400">{c.customer_id}</span>
            </div>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-slate-300 text-2xl leading-none">×</button>
        </div>
        <div className="flex border-b border-slate-800">
          {(["overview","scores","signals"] as const).map(t=>(
            <button key={t} onClick={()=>setTab(t)}
              className={`px-5 py-3 text-sm font-medium capitalize transition-colors ${tab===t?"text-violet-400 border-b-2 border-violet-400":"text-slate-500 hover:text-slate-300"}`}>
              {t}
            </button>
          ))}
        </div>
        <div className="p-6">
          {tab==="overview" && (
            <div className="grid grid-cols-2 gap-4">
              {[
                ["Contract Value", fmt(c.contract_value_usd)],
                ["NPS Score", c.nps_score >= 0 ? `+${c.nps_score}` : `${c.nps_score}`],
                ["Est. Referral Pipeline", fmt(c.estimated_referral_pipeline_usd)],
                ["Active Referrer", c.is_active_referrer ? "Yes" : "No"],
                ["Needs Activation", c.needs_advocacy_activation ? "Yes" : "No"],
                ["Recommended Action", ACTION_LABELS[c.referral_action]??c.referral_action],
                ["Referral Risk", c.referral_risk],
                ["Rep ID", c.rep_id],
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
                ["Advocacy", c.advocacy_score, "#a78bfa"],
                ["Relationship", c.relationship_depth_score, "#60a5fa"],
                ["Propensity", c.referral_propensity_score, "#34d399"],
                ["Impact", c.advocacy_impact_score, "#f59e0b"],
              ].map(([label,val,col])=>(
                <div key={label as string} className="flex flex-col items-center gap-2">
                  <RingGauge value={val as number} size={90} color={col as string}/>
                  <span className="text-slate-400 text-sm">{label as string}</span>
                </div>
              ))}
              <div className="col-span-2 bg-slate-800/50 rounded-xl p-4 text-center">
                <p className="text-slate-500 text-xs uppercase mb-1">Referral Composite</p>
                <p className="text-3xl font-bold text-violet-400">{c.referral_composite.toFixed(1)}</p>
              </div>
            </div>
          )}
          {tab==="signals" && (
            <div className="space-y-4">
              <div className="bg-slate-800/50 rounded-xl p-4">
                <p className="text-xs text-slate-500 uppercase mb-2">Primary Advocacy Signal</p>
                <p className="text-slate-200">{c.primary_advocacy_signal}</p>
              </div>
              <div className={`rounded-xl p-4 border ${RISK_BG[c.referral_risk]}`}>
                <p className="text-xs uppercase mb-1 opacity-70">Risk Level</p>
                <p className="font-semibold capitalize">{c.referral_risk}</p>
              </div>
              <div className="bg-slate-800/50 rounded-xl p-4">
                <p className="text-xs text-slate-500 uppercase mb-2">Action</p>
                <p className="text-slate-200 font-medium">{ACTION_LABELS[c.referral_action]??c.referral_action}</p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default function CustomerReferralIntelligencePage() {
  const [data, setData]         = useState<ApiData|null>(null);
  const [loading, setLoading]   = useState(true);
  const [velocityF, setVelocityF] = useState("all");
  const [levelF, setLevelF]     = useState("all");
  const [selected, setSelected] = useState<CustomerRep|null>(null);

  useEffect(() => {
    async function load() {
        setLoading(true);
        const p = new URLSearchParams();
        if (velocityF !== "all") p.set("velocity", velocityF);
        if (levelF !== "all")    p.set("level", levelF);
        const res = await fetch(`/api/customer-referral-intelligence?${p}`);
        setData(await res.json());
        setLoading(false);
  }
    load();
  }, [velocityF, levelF]);

  const s = data?.summary;
  const fmt = (n:number) => n>=1e6 ? `$${(n/1e6).toFixed(1)}M` : n>=1e3 ? `$${(n/1e3).toFixed(0)}K` : `$${n}`;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-slate-100">Customer Referral Intelligence</h1>
          <p className="text-slate-400 mt-1">Advocacy scoring, referral velocity, and activation prioritization</p>
        </div>

        {s && (
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
            {[
              ["Total Customers", s.total, "text-slate-200"],
              ["Active Referrers", s.active_referrer_count, "text-emerald-400"],
              ["Need Activation", s.activation_needed_count, "text-violet-400"],
              ["Avg Composite", s.avg_referral_composite, "text-indigo-400"],
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
              ["Avg Advocacy", s.avg_advocacy_score, "#a78bfa"],
              ["Avg Relationship", s.avg_relationship_depth_score, "#60a5fa"],
              ["Avg Propensity", s.avg_referral_propensity_score, "#34d399"],
              ["Avg Impact", s.avg_advocacy_impact_score, "#f59e0b"],
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
              <span className="text-slate-400 text-sm">Total Est. Referral Pipeline</span>
              <span className="text-2xl font-bold text-emerald-400">{fmt(s.total_estimated_referral_pipeline_usd)}</span>
            </div>
            {s.advocacy_counts && (
              <div className="flex gap-1 h-3 rounded-full overflow-hidden">
                {Object.entries(s.advocacy_counts).map(([k,v])=>(
                  <div key={k} style={{width:`${(v/s.total)*100}%`}}
                    className={k==="champion"?"bg-violet-500":k==="promoter"?"bg-indigo-500":k==="passive"?"bg-slate-600":"bg-rose-500"}
                    title={`${k}: ${v}`}/>
                ))}
              </div>
            )}
          </div>
        )}

        <div className="flex flex-wrap gap-3 mb-6">
          <div className="flex gap-2">
            {["all","accelerating","steady","declining","inactive"].map(v=>(
              <button key={v} onClick={()=>setVelocityF(v)}
                className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-colors ${velocityF===v?"bg-indigo-600 text-white":"bg-slate-800 text-slate-400 hover:text-slate-200"}`}>
                {v==="all"?"All Velocity":v}
              </button>
            ))}
          </div>
          <div className="flex gap-2">
            {["all","champion","promoter","passive","detractor"].map(v=>(
              <button key={v} onClick={()=>setLevelF(v)}
                className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-colors ${levelF===v?"bg-violet-600 text-white":"bg-slate-800 text-slate-400 hover:text-slate-200"}`}>
                {v==="all"?"All Levels":v}
              </button>
            ))}
          </div>
        </div>

        {loading && <div className="text-center text-slate-500 py-12">Loading...</div>}

        {!loading && data && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {data.customers.map(c=>(
              <div key={c.customer_id}
                className="bg-slate-900 border border-slate-800 rounded-xl p-5 cursor-pointer hover:border-slate-600 transition-all"
                onClick={()=>setSelected(c)}>
                <div className="flex items-start justify-between mb-3">
                  <div>
                    <h3 className="font-semibold text-slate-200">{c.customer_name}</h3>
                    <div className="flex gap-2 mt-1">
                      <span className={`text-xs font-medium ${VELOCITY_COLORS[c.referral_velocity]}`}>{c.referral_velocity}</span>
                      <span className="text-slate-600">•</span>
                      <span className={`text-xs font-medium ${ADVOCACY_COLORS[c.advocacy_level]}`}>{c.advocacy_level}</span>
                    </div>
                  </div>
                  <span className={`text-xs px-2 py-1 rounded-full border ${RISK_BG[c.referral_risk]}`}>
                    {c.referral_risk}
                  </span>
                </div>
                <div className="flex items-center gap-4 mb-3">
                  <RingGauge value={c.referral_composite} size={64} color="#818cf8"/>
                  <div className="flex-1">
                    <p className="text-xs text-slate-500 mb-1">Scores</p>
                    <div className="space-y-1">
                      {[
                        ["Adv", c.advocacy_score, "#a78bfa"],
                        ["Rel", c.relationship_depth_score, "#60a5fa"],
                        ["Prop", c.referral_propensity_score, "#34d399"],
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
                <div className="text-xs text-slate-400 truncate mb-2">{c.primary_advocacy_signal}</div>
                <div className="flex items-center justify-between text-xs">
                  <span className="text-slate-500">Pipeline: <span className="text-emerald-400 font-medium">{fmt(c.estimated_referral_pipeline_usd)}</span></span>
                  {c.needs_advocacy_activation && (
                    <span className="bg-violet-900/40 text-violet-300 border border-violet-700 px-2 py-0.5 rounded-full">Activate</span>
                  )}
                  {c.is_active_referrer && (
                    <span className="bg-emerald-900/40 text-emerald-300 border border-emerald-700 px-2 py-0.5 rounded-full">Active</span>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
      {selected && <DetailModal c={selected} onClose={()=>setSelected(null)}/>}
    </div>
  );
}
