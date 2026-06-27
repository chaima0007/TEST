"use client";
import { useEffect, useState } from "react";

type Account = {
  account_id: string; region: string; expansion_risk: string; expansion_pattern: string;
  expansion_severity: string; recommended_action: string;
  usage_ceiling_score: number; product_gap_score: number;
  engagement_score: number; relationship_score: number;
  expansion_composite: number; has_expansion_signal: boolean;
  requires_executive_engagement: boolean; estimated_expansion_arr_usd: number;
  expansion_signal: string;
};
type Summary = {
  total: number; risk_counts: Record<string,number>;
  pattern_counts: Record<string,number>; severity_counts: Record<string,number>;
  action_counts: Record<string,number>; avg_expansion_composite: number;
  expansion_signal_count: number; executive_engagement_count: number;
  avg_usage_ceiling_score: number; avg_product_gap_score: number;
  avg_engagement_score: number; avg_relationship_score: number;
  total_estimated_expansion_arr_usd: number;
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

const RISK_COLORS = { low:"#6366f1", moderate:"#8b5cf6", high:"#a855f7", critical:"#d946ef" };
const PAT_COLORS  = { none:"#475569", usage_ceiling_breach:"#d946ef", product_gap_signal:"#8b5cf6", engagement_elevation:"#06b6d4", executive_pull_through:"#f59e0b", contract_white_space:"#10b981" };
const SEV_COLORS  = { dormant:"#475569", emerging:"#8b5cf6", active:"#a855f7", urgent:"#d946ef" };
const ACT_COLORS  = { no_action:"#475569", expansion_monitoring:"#6366f1", cross_sell_campaign:"#8b5cf6", qbr_expansion_pitch:"#06b6d4", product_gap_discovery_call:"#a855f7", executive_expansion_briefing:"#f59e0b", usage_ceiling_upsell:"#d946ef", white_space_mapping_session:"#10b981", expansion_fast_track:"#ec4899" };
const RISK_BADGE  = { low:"bg-indigo-900 text-indigo-300", moderate:"bg-violet-900 text-violet-300", high:"bg-purple-900 text-purple-300", critical:"bg-fuchsia-900 text-fuchsia-300" };
const SEV_BADGE   = { dormant:"bg-slate-800 text-slate-400", emerging:"bg-violet-900 text-violet-300", active:"bg-purple-900 text-purple-300", urgent:"bg-fuchsia-900 text-fuchsia-300" };

function DetailModal({ account, onClose }: { account: Account; onClose: () => void }) {
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
            <span className="text-lg font-bold text-white">{account.account_id}</span>
            <span className="ml-2 text-slate-400 text-sm">{account.region}</span>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl leading-none">✕</button>
        </div>
        <div className="flex gap-2 mb-4">
          {(["scores","signal","action"] as const).map(t=>(
            <button key={t} onClick={()=>setTab(t)}
              className={`px-3 py-1 rounded text-xs font-medium transition-colors ${tab===t?"bg-fuchsia-700 text-white":"bg-slate-800 text-slate-400 hover:text-white"}`}>
              {t.charAt(0).toUpperCase()+t.slice(1)}
            </button>
          ))}
        </div>
        {tab==="scores" && (
          <div className="grid grid-cols-2 gap-3 text-sm">
            {[
              ["Usage Ceiling", account.usage_ceiling_score, "#d946ef"],
              ["Product Gap",   account.product_gap_score,   "#8b5cf6"],
              ["Engagement",    account.engagement_score,    "#06b6d4"],
              ["Relationship",  account.relationship_score,  "#f59e0b"],
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
              <div className="text-slate-400 text-xs mb-1">Expansion Composite</div>
              <div className="text-white font-bold text-2xl">{account.expansion_composite.toFixed(1)}</div>
            </div>
          </div>
        )}
        {tab==="signal" && (
          <div className="bg-slate-800 rounded-lg p-4 text-sm text-slate-200 leading-relaxed">
            {account.expansion_signal}
            <div className="mt-3 flex gap-2 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[account.expansion_risk as keyof typeof RISK_BADGE]||"bg-slate-700 text-slate-300"}`}>{account.expansion_risk}</span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[account.expansion_severity as keyof typeof SEV_BADGE]||"bg-slate-700 text-slate-300"}`}>{account.expansion_severity}</span>
            </div>
          </div>
        )}
        {tab==="action" && (
          <div className="space-y-3 text-sm">
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Recommended Action</div>
              <div className="text-white font-medium">{account.recommended_action.replace(/_/g," ")}</div>
            </div>
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Estimated Expansion ARR</div>
              <div className="text-white font-bold">${account.estimated_expansion_arr_usd.toLocaleString()}</div>
            </div>
            <div className="flex gap-2">
              {account.has_expansion_signal          && <span className="px-2 py-1 rounded bg-fuchsia-900 text-fuchsia-300 text-xs font-medium">SIGNAL</span>}
              {account.requires_executive_engagement && <span className="px-2 py-1 rounded bg-violet-900 text-violet-300 text-xs font-medium">EXEC ENGAGE</span>}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function ExpansionDashboard() {
  const [data, setData]     = useState<{ accounts: Account[]; summary: Summary }|null>(null);
  const [filter, setFilter] = useState<string>("all");
  const [patFilter, setPat] = useState<string>("all");
  const [selected, setSelected] = useState<Account|null>(null);

  useEffect(()=>{
    fetch("/api/sales-expansion-revenue-signal-engine")
      .then(r=>r.json()).then(setData).catch(console.error);
  },[]);

  if (!data) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-fuchsia-400 text-lg animate-pulse">Loading Expansion Intelligence...</div>
    </div>
  );

  const { accounts, summary } = data;
  const filtered = accounts.filter(a=>
    (filter==="all" || a.expansion_risk===filter) &&
    (patFilter==="all" || a.expansion_pattern===patFilter)
  );

  const dists = [
    { title:"Risk",     counts:summary.risk_counts,     colors:RISK_COLORS },
    { title:"Pattern",  counts:summary.pattern_counts,  colors:PAT_COLORS  },
    { title:"Severity", counts:summary.severity_counts, colors:SEV_COLORS  },
    { title:"Action",   counts:summary.action_counts,   colors:ACT_COLORS  },
  ] as Array<{title:string;counts:Record<string,number>;colors:Record<string,string>}>;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {selected && <DetailModal account={selected} onClose={()=>setSelected(null)}/>}

      <div>
        <h1 className="text-2xl font-bold text-white">Expansion Revenue Signal Intelligence</h1>
        <p className="text-slate-400 text-sm mt-1">Usage Ceiling · Product Gap · Engagement · Relationship</p>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {[
          ["Accounts",       summary.total,                                                                         "text-fuchsia-400"],
          ["Avg Composite",  summary.avg_expansion_composite,                                                       "text-purple-400"],
          ["Exp Signals",    summary.expansion_signal_count,                                                        "text-violet-400"],
          ["Exec Engage",    summary.executive_engagement_count,                                                     "text-amber-400"],
          ["Exp ARR",        `$${Math.round(summary.total_estimated_expansion_arr_usd/1000)}k`,                    "text-fuchsia-400"],
          ["Avg Usage",      `${Math.round(summary.avg_usage_ceiling_score)}`,                                      "text-purple-400"],
        ].map(([l,v,c])=>(
          <div key={String(l)} className="bg-slate-900 border border-slate-800 rounded-xl p-3 text-center">
            <div className={`text-xl font-bold ${c}`}>{v}</div>
            <div className="text-xs text-slate-500 mt-0.5">{l}</div>
          </div>
        ))}
      </div>

      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
        <div className="grid grid-cols-4 gap-4">
          <Gauge value={summary.avg_usage_ceiling_score} label="Usage Ceiling" color="#d946ef"/>
          <Gauge value={summary.avg_product_gap_score}   label="Product Gap"   color="#8b5cf6"/>
          <Gauge value={summary.avg_engagement_score}    label="Engagement"    color="#06b6d4"/>
          <Gauge value={summary.avg_relationship_score}  label="Relationship"  color="#f59e0b"/>
        </div>
      </div>

      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 grid grid-cols-1 md:grid-cols-2 gap-5">
        {dists.map(d=><DistBar key={d.title} {...d}/>)}
      </div>

      <div className="flex flex-wrap gap-2">
        {["all","low","moderate","high","critical"].map(r=>(
          <button key={r} onClick={()=>setFilter(r)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${filter===r?"bg-fuchsia-700 border-fuchsia-600 text-white":"bg-slate-900 border-slate-700 text-slate-400 hover:text-white"}`}>
            {r}
          </button>
        ))}
        <span className="w-px h-5 self-center bg-slate-700"/>
        {["all","usage_ceiling_breach","product_gap_signal","engagement_elevation","executive_pull_through","contract_white_space"].map(p=>(
          <button key={p} onClick={()=>setPat(p)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${patFilter===p?"bg-purple-900 border-purple-800 text-white":"bg-slate-900 border-slate-700 text-slate-400 hover:text-white"}`}>
            {p.replace(/_/g," ")}
          </button>
        ))}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {filtered.map(a=>(
          <div key={a.account_id} onClick={()=>setSelected(a)}
            className="bg-slate-900 border border-slate-800 rounded-xl p-4 cursor-pointer hover:border-fuchsia-700 transition-colors">
            <div className="flex items-center justify-between mb-2">
              <span className="font-bold text-white">{a.account_id}</span>
              <span className="text-xs text-slate-400">{a.region}</span>
            </div>
            <div className="flex gap-1 mb-3 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[a.expansion_risk as keyof typeof RISK_BADGE]||"bg-slate-700 text-slate-300"}`}>{a.expansion_risk}</span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[a.expansion_severity as keyof typeof SEV_BADGE]||"bg-slate-700 text-slate-300"}`}>{a.expansion_severity}</span>
            </div>
            <div className="text-2xl font-black text-white mb-1">{a.expansion_composite.toFixed(1)}</div>
            <div className="text-xs text-slate-500 mb-2 capitalize">{a.expansion_pattern.replace(/_/g," ")}</div>
            <div className="text-xs text-fuchsia-400 font-medium mb-2">${a.estimated_expansion_arr_usd.toLocaleString()} expansion</div>
            <div className="flex gap-1 flex-wrap">
              {a.has_expansion_signal          && <span className="px-1.5 py-0.5 rounded bg-fuchsia-900 text-fuchsia-300 text-xs">SIGNAL</span>}
              {a.requires_executive_engagement && <span className="px-1.5 py-0.5 rounded bg-violet-900 text-violet-300 text-xs">EXEC</span>}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
