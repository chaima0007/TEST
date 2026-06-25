"use client";
import { useEffect, useState } from "react";

type Account = {
  account_id: string; region: string; churn_risk: string; churn_pattern: string;
  churn_severity: string; recommended_action: string;
  usage_score: number; relationship_score: number;
  support_score: number; value_score: number;
  churn_composite: number; has_churn_signal: boolean;
  requires_executive_action: boolean; estimated_arr_at_risk_usd: number;
  churn_signal: string;
};
type Summary = {
  total: number; risk_counts: Record<string,number>;
  pattern_counts: Record<string,number>; severity_counts: Record<string,number>;
  action_counts: Record<string,number>; avg_churn_composite: number;
  churn_signal_count: number; executive_action_count: number;
  avg_usage_score: number; avg_relationship_score: number;
  avg_support_score: number; avg_value_score: number;
  total_estimated_arr_at_risk_usd: number;
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
const PAT_COLORS  = { none:"#10b981", usage_collapse:"#ef4444", sponsor_exodus:"#f97316", support_spiral:"#a855f7", competitive_switch:"#3b82f6", value_gap_crisis:"#f59e0b" };
const SEV_COLORS  = { healthy:"#10b981", watching:"#f59e0b", at_risk:"#f97316", churning:"#ef4444" };
const ACT_COLORS  = { no_action:"#10b981", health_monitoring:"#f59e0b", executive_business_review:"#06b6d4", success_plan_reset:"#f97316", competitive_defense_playbook:"#3b82f6", sponsor_re_engagement:"#a855f7", support_escalation_resolution:"#ec4899", renewal_risk_intervention:"#dc2626", executive_save_call:"#7f1d1d" };
const RISK_BADGE  = { low:"bg-emerald-900 text-emerald-300", moderate:"bg-amber-900 text-amber-300", high:"bg-orange-900 text-orange-300", critical:"bg-red-900 text-red-300" };
const SEV_BADGE   = { healthy:"bg-emerald-900 text-emerald-300", watching:"bg-amber-900 text-amber-300", at_risk:"bg-orange-900 text-orange-300", churning:"bg-red-900 text-red-300" };

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
              className={`px-3 py-1 rounded text-xs font-medium transition-colors ${tab===t?"bg-emerald-700 text-white":"bg-slate-800 text-slate-400 hover:text-white"}`}>
              {t.charAt(0).toUpperCase()+t.slice(1)}
            </button>
          ))}
        </div>
        {tab==="scores" && (
          <div className="grid grid-cols-2 gap-3 text-sm">
            {[
              ["Usage",        account.usage_score,        "#10b981"],
              ["Relationship", account.relationship_score, "#06b6d4"],
              ["Support",      account.support_score,      "#f97316"],
              ["Value",        account.value_score,        "#a855f7"],
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
              <div className="text-slate-400 text-xs mb-1">Churn Composite</div>
              <div className="text-white font-bold text-2xl">{account.churn_composite.toFixed(1)}</div>
            </div>
          </div>
        )}
        {tab==="signal" && (
          <div className="bg-slate-800 rounded-lg p-4 text-sm text-slate-200 leading-relaxed">
            {account.churn_signal}
            <div className="mt-3 flex gap-2 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[account.churn_risk as keyof typeof RISK_BADGE]||"bg-slate-700 text-slate-300"}`}>{account.churn_risk}</span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[account.churn_severity as keyof typeof SEV_BADGE]||"bg-slate-700 text-slate-300"}`}>{account.churn_severity}</span>
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
              <div className="text-slate-400 text-xs mb-1">ARR at Risk</div>
              <div className="text-white font-bold">${account.estimated_arr_at_risk_usd.toLocaleString()}</div>
            </div>
            <div className="flex gap-2">
              {account.has_churn_signal        && <span className="px-2 py-1 rounded bg-orange-900 text-orange-300 text-xs font-medium">CHURN SIGNAL</span>}
              {account.requires_executive_action && <span className="px-2 py-1 rounded bg-emerald-900 text-emerald-300 text-xs font-medium">EXEC ACTION</span>}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function ChurnDashboard() {
  const [data, setData]     = useState<{ accounts: Account[]; summary: Summary }|null>(null);
  const [filter, setFilter] = useState<string>("all");
  const [patFilter, setPat] = useState<string>("all");
  const [selected, setSelected] = useState<Account|null>(null);

  useEffect(()=>{
    fetch("/api/sales-account-churn-early-warning-engine")
      .then(r=>r.json()).then(setData).catch(console.error);
  },[]);

  if (!data) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-emerald-400 text-lg animate-pulse">Loading Churn Intelligence...</div>
    </div>
  );

  const { accounts, summary } = data;
  const filtered = accounts.filter(a=>
    (filter==="all" || a.churn_risk===filter) &&
    (patFilter==="all" || a.churn_pattern===patFilter)
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
        <h1 className="text-2xl font-bold text-white">Account Churn Early Warning</h1>
        <p className="text-slate-400 text-sm mt-1">Usage · Relationship · Support · Value</p>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {[
          ["Accounts",       summary.total,                                                                      "text-emerald-400"],
          ["Avg Composite",  summary.avg_churn_composite,                                                        "text-green-400"],
          ["Churn Signals",  summary.churn_signal_count,                                                         "text-orange-400"],
          ["Exec Action",    summary.executive_action_count,                                                      "text-amber-400"],
          ["ARR at Risk",    `$${Math.round(summary.total_estimated_arr_at_risk_usd/1000)}k`,                    "text-red-400"],
          ["Avg Usage",      `${Math.round(summary.avg_usage_score)}`,                                           "text-emerald-400"],
        ].map(([l,v,c])=>(
          <div key={String(l)} className="bg-slate-900 border border-slate-800 rounded-xl p-3 text-center">
            <div className={`text-xl font-bold ${c}`}>{v}</div>
            <div className="text-xs text-slate-500 mt-0.5">{l}</div>
          </div>
        ))}
      </div>

      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
        <div className="grid grid-cols-4 gap-4">
          <Gauge value={summary.avg_usage_score}        label="Usage"        color="#10b981"/>
          <Gauge value={summary.avg_relationship_score} label="Relationship" color="#06b6d4"/>
          <Gauge value={summary.avg_support_score}      label="Support"      color="#f97316"/>
          <Gauge value={summary.avg_value_score}        label="Value"        color="#a855f7"/>
        </div>
      </div>

      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 grid grid-cols-1 md:grid-cols-2 gap-5">
        {dists.map(d=><DistBar key={d.title} {...d}/>)}
      </div>

      <div className="flex flex-wrap gap-2">
        {["all","low","moderate","high","critical"].map(r=>(
          <button key={r} onClick={()=>setFilter(r)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${filter===r?"bg-emerald-700 border-emerald-600 text-white":"bg-slate-900 border-slate-700 text-slate-400 hover:text-white"}`}>
            {r}
          </button>
        ))}
        <span className="w-px h-5 self-center bg-slate-700"/>
        {["all","usage_collapse","sponsor_exodus","support_spiral","competitive_switch","value_gap_crisis"].map(p=>(
          <button key={p} onClick={()=>setPat(p)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${patFilter===p?"bg-green-900 border-green-800 text-white":"bg-slate-900 border-slate-700 text-slate-400 hover:text-white"}`}>
            {p.replace(/_/g," ")}
          </button>
        ))}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {filtered.map(a=>(
          <div key={a.account_id} onClick={()=>setSelected(a)}
            className="bg-slate-900 border border-slate-800 rounded-xl p-4 cursor-pointer hover:border-emerald-700 transition-colors">
            <div className="flex items-center justify-between mb-2">
              <span className="font-bold text-white">{a.account_id}</span>
              <span className="text-xs text-slate-400">{a.region}</span>
            </div>
            <div className="flex gap-1 mb-3 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[a.churn_risk as keyof typeof RISK_BADGE]||"bg-slate-700 text-slate-300"}`}>{a.churn_risk}</span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[a.churn_severity as keyof typeof SEV_BADGE]||"bg-slate-700 text-slate-300"}`}>{a.churn_severity}</span>
            </div>
            <div className="text-2xl font-black text-white mb-1">{a.churn_composite.toFixed(1)}</div>
            <div className="text-xs text-slate-500 mb-2 capitalize">{a.churn_pattern.replace(/_/g," ")}</div>
            <div className="text-xs text-emerald-400 font-medium mb-2">${a.estimated_arr_at_risk_usd.toLocaleString()} ARR</div>
            <div className="flex gap-1 flex-wrap">
              {a.has_churn_signal          && <span className="px-1.5 py-0.5 rounded bg-orange-900 text-orange-300 text-xs">SIGNAL</span>}
              {a.requires_executive_action && <span className="px-1.5 py-0.5 rounded bg-emerald-900 text-emerald-300 text-xs">EXEC</span>}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
