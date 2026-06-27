"use client";
import { useEffect, useState } from "react";

type Invoice = {
  invoice_id: string; client_id: string; region: string;
  invoice_risk: string; invoice_pattern: string;
  invoice_severity: string; recommended_action: string;
  overdue_score: number; dispute_score: number;
  exposure_score: number; behavior_score: number;
  invoice_composite: number; has_collection_signal: boolean;
  requires_escalation: boolean; estimated_bad_debt_usd: number;
  invoice_signal: string;
};
type Summary = {
  total: number; risk_counts: Record<string,number>;
  pattern_counts: Record<string,number>; severity_counts: Record<string,number>;
  action_counts: Record<string,number>; avg_invoice_composite: number;
  collection_signal_count: number; escalation_count: number;
  avg_overdue_score: number; avg_dispute_score: number;
  avg_exposure_score: number; avg_behavior_score: number;
  total_estimated_bad_debt_usd: number;
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
const PAT_COLORS  = { none:"#10b981", chronic_late_payer:"#ef4444", dispute_prone:"#f97316", partial_payment:"#a855f7", billing_anomaly:"#3b82f6", revenue_leakage:"#f59e0b" };
const SEV_COLORS  = { healthy:"#10b981", watchlist:"#f59e0b", at_risk:"#f97316", critical:"#ef4444" };
const ACT_COLORS  = { no_action:"#10b981", payment_monitoring:"#f59e0b", gentle_reminder:"#06b6d4", formal_collection_notice:"#f97316", dispute_resolution_call:"#a855f7", billing_correction:"#3b82f6", payment_plan_negotiation:"#ec4899", executive_escalation:"#dc2626", legal_review_trigger:"#7f1d1d" };
const RISK_BADGE  = { low:"bg-emerald-900 text-emerald-300", moderate:"bg-amber-900 text-amber-300", high:"bg-orange-900 text-orange-300", critical:"bg-red-900 text-red-300" };
const SEV_BADGE   = { healthy:"bg-emerald-900 text-emerald-300", watchlist:"bg-amber-900 text-amber-300", at_risk:"bg-orange-900 text-orange-300", critical:"bg-red-900 text-red-300" };

function DetailModal({ inv, onClose }: { inv: Invoice; onClose: () => void }) {
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
            <span className="text-lg font-bold text-white">{inv.invoice_id}</span>
            <span className="ml-2 text-slate-400 text-sm">{inv.client_id}</span>
            <span className="ml-2 text-yellow-400 text-xs">{inv.region}</span>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl leading-none">✕</button>
        </div>
        <div className="flex gap-2 mb-4">
          {(["scores","signal","action"] as const).map(t=>(
            <button key={t} onClick={()=>setTab(t)}
              className={`px-3 py-1 rounded text-xs font-medium transition-colors ${tab===t?"bg-yellow-700 text-white":"bg-slate-800 text-slate-400 hover:text-white"}`}>
              {t.charAt(0).toUpperCase()+t.slice(1)}
            </button>
          ))}
        </div>
        {tab==="scores" && (
          <div className="grid grid-cols-2 gap-3 text-sm">
            {[
              ["Overdue",  inv.overdue_score,  "#ef4444"],
              ["Dispute",  inv.dispute_score,  "#f97316"],
              ["Exposure", inv.exposure_score, "#a855f7"],
              ["Behavior", inv.behavior_score, "#f59e0b"],
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
              <div className="text-slate-400 text-xs mb-1">Invoice Composite</div>
              <div className="text-white font-bold text-2xl">{inv.invoice_composite.toFixed(1)}</div>
            </div>
          </div>
        )}
        {tab==="signal" && (
          <div className="bg-slate-800 rounded-lg p-4 text-sm text-slate-200 leading-relaxed">
            {inv.invoice_signal}
            <div className="mt-3 flex gap-2 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[inv.invoice_risk as keyof typeof RISK_BADGE]||"bg-slate-700 text-slate-300"}`}>{inv.invoice_risk}</span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[inv.invoice_severity as keyof typeof SEV_BADGE]||"bg-slate-700 text-slate-300"}`}>{inv.invoice_severity}</span>
            </div>
          </div>
        )}
        {tab==="action" && (
          <div className="space-y-3 text-sm">
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Recommended Action</div>
              <div className="text-white font-medium">{inv.recommended_action.replace(/_/g," ")}</div>
            </div>
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Estimated Bad Debt</div>
              <div className="text-white font-bold">${inv.estimated_bad_debt_usd.toLocaleString()}</div>
            </div>
            <div className="flex gap-2">
              {inv.has_collection_signal && <span className="px-2 py-1 rounded bg-orange-900 text-orange-300 text-xs font-medium">COLLECT</span>}
              {inv.requires_escalation   && <span className="px-2 py-1 rounded bg-red-900 text-red-300 text-xs font-medium">ESCALATE</span>}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function InvoiceDashboard() {
  const [data, setData]     = useState<{ invoices: Invoice[]; summary: Summary }|null>(null);
  const [filter, setFilter] = useState<string>("all");
  const [patFilter, setPat] = useState<string>("all");
  const [selected, setSelected] = useState<Invoice|null>(null);

  useEffect(()=>{
    fetch("/api/invoice-intelligence-engine")
      .then(r=>r.json()).then(setData).catch(console.error);
  },[]);

  if (!data) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-yellow-400 text-lg animate-pulse">Loading Invoice Intelligence...</div>
    </div>
  );

  const { invoices, summary } = data;
  const filtered = invoices.filter(inv=>
    (filter==="all" || inv.invoice_risk===filter) &&
    (patFilter==="all" || inv.invoice_pattern===patFilter)
  );

  const dists = [
    { title:"Risk",     counts:summary.risk_counts,     colors:RISK_COLORS },
    { title:"Pattern",  counts:summary.pattern_counts,  colors:PAT_COLORS  },
    { title:"Severity", counts:summary.severity_counts, colors:SEV_COLORS  },
    { title:"Action",   counts:summary.action_counts,   colors:ACT_COLORS  },
  ] as Array<{title:string;counts:Record<string,number>;colors:Record<string,string>}>;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {selected && <DetailModal inv={selected} onClose={()=>setSelected(null)}/>}

      <div>
        <h1 className="text-2xl font-bold text-white">Invoice Intelligence</h1>
        <p className="text-slate-400 text-sm mt-1">Overdue · Dispute · Exposure · Behavior</p>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {[
          ["Invoices",    summary.total,                                                                  "text-yellow-400"],
          ["Avg Risk",    summary.avg_invoice_composite,                                                  "text-amber-400"],
          ["Collection",  summary.collection_signal_count,                                                "text-orange-400"],
          ["Escalations", summary.escalation_count,                                                       "text-red-400"],
          ["Bad Debt",    `$${Math.round(summary.total_estimated_bad_debt_usd/1000)}k`,                  "text-red-400"],
          ["Avg Overdue", `${Math.round(summary.avg_overdue_score)}`,                                    "text-yellow-400"],
        ].map(([l,v,c])=>(
          <div key={String(l)} className="bg-slate-900 border border-slate-800 rounded-xl p-3 text-center">
            <div className={`text-xl font-bold ${c}`}>{v}</div>
            <div className="text-xs text-slate-500 mt-0.5">{l}</div>
          </div>
        ))}
      </div>

      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
        <div className="grid grid-cols-4 gap-4">
          <Gauge value={summary.avg_overdue_score}   label="Overdue"   color="#ef4444"/>
          <Gauge value={summary.avg_dispute_score}   label="Dispute"   color="#f97316"/>
          <Gauge value={summary.avg_exposure_score}  label="Exposure"  color="#a855f7"/>
          <Gauge value={summary.avg_behavior_score}  label="Behavior"  color="#f59e0b"/>
        </div>
      </div>

      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 grid grid-cols-1 md:grid-cols-2 gap-5">
        {dists.map(d=><DistBar key={d.title} {...d}/>)}
      </div>

      <div className="flex flex-wrap gap-2">
        {["all","low","moderate","high","critical"].map(r=>(
          <button key={r} onClick={()=>setFilter(r)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${filter===r?"bg-yellow-700 border-yellow-600 text-white":"bg-slate-900 border-slate-700 text-slate-400 hover:text-white"}`}>
            {r}
          </button>
        ))}
        <span className="w-px h-5 self-center bg-slate-700"/>
        {["all","chronic_late_payer","dispute_prone","partial_payment","billing_anomaly","revenue_leakage"].map(p=>(
          <button key={p} onClick={()=>setPat(p)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${patFilter===p?"bg-amber-900 border-amber-800 text-white":"bg-slate-900 border-slate-700 text-slate-400 hover:text-white"}`}>
            {p.replace(/_/g," ")}
          </button>
        ))}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {filtered.map(inv=>(
          <div key={inv.invoice_id} onClick={()=>setSelected(inv)}
            className="bg-slate-900 border border-slate-800 rounded-xl p-4 cursor-pointer hover:border-yellow-700 transition-colors">
            <div className="flex items-center justify-between mb-1">
              <span className="font-bold text-white">{inv.invoice_id}</span>
              <span className="text-xs text-slate-400">{inv.region}</span>
            </div>
            <div className="text-xs text-yellow-400 mb-2">{inv.client_id}</div>
            <div className="flex gap-1 mb-3 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[inv.invoice_risk as keyof typeof RISK_BADGE]||"bg-slate-700 text-slate-300"}`}>{inv.invoice_risk}</span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[inv.invoice_severity as keyof typeof SEV_BADGE]||"bg-slate-700 text-slate-300"}`}>{inv.invoice_severity}</span>
            </div>
            <div className="text-2xl font-black text-white mb-1">{inv.invoice_composite.toFixed(1)}</div>
            <div className="text-xs text-slate-500 mb-2 capitalize">{inv.invoice_pattern.replace(/_/g," ")}</div>
            <div className="text-xs text-red-400 font-medium mb-2">${inv.estimated_bad_debt_usd.toLocaleString()} bad debt</div>
            <div className="flex gap-1 flex-wrap">
              {inv.has_collection_signal && <span className="px-1.5 py-0.5 rounded bg-orange-900 text-orange-300 text-xs">COLLECT</span>}
              {inv.requires_escalation   && <span className="px-1.5 py-0.5 rounded bg-red-900 text-red-300 text-xs">ESCALATE</span>}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
