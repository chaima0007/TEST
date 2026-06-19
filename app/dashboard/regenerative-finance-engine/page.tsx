"use client";
import { useEffect, useState } from "react";

type Fund = {
  fund_id: string; fund_type: string; region: string;
  regen_finance_risk: string; impact_pattern: string;
  impact_severity: string; recommended_action: string;
  integrity_score: number; impact_score: number;
  inclusion_score: number; verification_score: number;
  regen_finance_composite: number; has_greenwashing_signal: boolean;
  requires_impact_audit: boolean; estimated_impact_deficit_index: number;
  regen_signal: string;
};
type Summary = {
  total: number; risk_counts: Record<string,number>;
  pattern_counts: Record<string,number>; severity_counts: Record<string,number>;
  action_counts: Record<string,number>; avg_regen_finance_composite: number;
  greenwashing_signal_count: number; impact_audit_required_count: number;
  avg_integrity_score: number; avg_impact_score: number;
  avg_inclusion_score: number; avg_verification_score: number;
  avg_estimated_impact_deficit_index: number;
};

function GaugeRing({ value, label, color }: { value: number; label: string; color: string }) {
  const r = 36; const circ = 2 * Math.PI * r;
  const fill = circ * (1 - value / 100);
  return (
    <div className="flex flex-col items-center gap-1">
      <svg width="88" height="88" viewBox="0 0 88 88">
        <circle cx="44" cy="44" r={r} fill="none" stroke="#0f172a" strokeWidth="8"/>
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

const RISK_COLORS  = { low:"#10b981", moderate:"#f59e0b", high:"#f97316", critical:"#ef4444" };
const PAT_COLORS   = { none:"#10b981", greenwashing_exposure:"#ef4444", impact_dilution:"#f97316", exclusion_deficit:"#a855f7", measurement_gap:"#06b6d4", capital_misallocation:"#dc2626" };
const SEV_COLORS   = { thriving:"#10b981", regenerating:"#34d399", transitioning:"#f59e0b", extractive:"#ef4444" };
const ACT_COLORS   = { no_action:"#10b981", impact_monitoring:"#06b6d4", measurement_upgrade:"#3b82f6", stakeholder_realignment:"#a855f7", impact_audit:"#f97316", greenwashing_intervention:"#ef4444" };
const RISK_BADGE   = { low:"bg-emerald-900 text-emerald-300", moderate:"bg-amber-900 text-amber-300", high:"bg-orange-900 text-orange-300", critical:"bg-red-900 text-red-300" };
const SEV_BADGE    = { thriving:"bg-emerald-900 text-emerald-300", regenerating:"bg-teal-900 text-teal-300", transitioning:"bg-amber-900 text-amber-300", extractive:"bg-red-900 text-red-300" };

function DetailModal({ fund, onClose }: { fund: Fund; onClose: () => void }) {
  const [tab, setTab] = useState<"scores"|"signal"|"action">("scores");
  useEffect(()=>{
    const h = (e: KeyboardEvent) => { if (e.key==="Escape") onClose(); };
    window.addEventListener("keydown", h);
    return ()=>window.removeEventListener("keydown",h);
  },[onClose]);
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70" onClick={onClose}>
      <div className="bg-slate-900 border border-emerald-500/30 rounded-xl w-full max-w-lg p-6 shadow-2xl" onClick={e=>e.stopPropagation()}>
        <div className="flex items-center justify-between mb-4">
          <div>
            <span className="text-lg font-bold text-white">{fund.fund_id}</span>
            <span className="ml-2 text-green-400 text-xs">{fund.fund_type.replace(/_/g," ")}</span>
            <span className="ml-2 text-slate-400 text-xs">{fund.region}</span>
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
            {([
              ["Integrity",     fund.integrity_score,     "#10b981"],
              ["Impact",        fund.impact_score,        "#34d399"],
              ["Inclusion",     fund.inclusion_score,     "#059669"],
              ["Verification",  fund.verification_score,  "#06b6d4"],
            ] as [string, number, string][]).map(([l,v,c])=>(
              <div key={l} className="bg-slate-800 rounded-lg p-3">
                <div className="text-slate-400 text-xs mb-1">{l}</div>
                <div className="text-white font-bold text-lg">{v.toFixed(1)}</div>
                <div className="h-1.5 rounded mt-1 bg-slate-700">
                  <div className="h-1.5 rounded" style={{width:`${Math.min(v,100)}%`,background:c}}/>
                </div>
              </div>
            ))}
            <div className="col-span-2 bg-slate-800 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Regen Finance Composite</div>
              <div className="text-white font-bold text-2xl">{fund.regen_finance_composite.toFixed(1)}</div>
            </div>
          </div>
        )}
        {tab==="signal" && (
          <div className="bg-slate-800 rounded-lg p-4 text-sm text-slate-200 leading-relaxed">
            {fund.regen_signal}
            <div className="mt-3 flex gap-2 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[fund.regen_finance_risk as keyof typeof RISK_BADGE]||"bg-slate-700 text-slate-300"}`}>{fund.regen_finance_risk}</span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[fund.impact_severity as keyof typeof SEV_BADGE]||"bg-slate-700 text-slate-300"}`}>{fund.impact_severity}</span>
            </div>
          </div>
        )}
        {tab==="action" && (
          <div className="space-y-3 text-sm">
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Recommended Action</div>
              <div className="text-white font-medium">{fund.recommended_action.replace(/_/g," ")}</div>
            </div>
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Impact Deficit Index</div>
              <div className="text-white font-bold">{fund.estimated_impact_deficit_index.toFixed(2)} / 10</div>
            </div>
            <div className="flex gap-2 flex-wrap">
              {fund.has_greenwashing_signal && <span className="px-2 py-1 rounded bg-red-900 text-red-300 text-xs font-medium">GREENWASHING</span>}
              {fund.requires_impact_audit   && <span className="px-2 py-1 rounded bg-amber-900 text-amber-300 text-xs font-medium">AUDIT REQUIS</span>}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function RegenFinanceDashboard() {
  const [data, setData]         = useState<{ funds: Fund[]; summary: Summary }|null>(null);
  const [filter, setFilter]     = useState<string>("all");
  const [patFilter, setPat]     = useState<string>("all");
  const [selected, setSelected] = useState<Fund|null>(null);

  useEffect(()=>{
    fetch("/api/regenerative-finance-engine")
      .then(r=>r.json()).then(setData).catch(console.error);
  },[]);

  if (!data) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-green-400 text-lg animate-pulse">Loading Regenerative Finance Engine...</div>
    </div>
  );

  const { funds, summary } = data;
  const filtered = funds.filter(f=>
    (filter==="all" || f.regen_finance_risk===filter) &&
    (patFilter==="all" || f.impact_pattern===patFilter)
  );

  const dists: Array<{title:string;counts:Record<string,number>;colors:Record<string,string>}> = [
    { title:"Risk",     counts:summary.risk_counts,     colors:RISK_COLORS },
    { title:"Pattern",  counts:summary.pattern_counts,  colors:PAT_COLORS  },
    { title:"Severity", counts:summary.severity_counts, colors:SEV_COLORS  },
    { title:"Action",   counts:summary.action_counts,   colors:ACT_COLORS  },
  ];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {selected && <DetailModal fund={selected} onClose={()=>setSelected(null)}/>}

      <div>
        <h1 className="text-2xl font-bold text-white">Regenerative Finance &amp; Impact Measurement Engine</h1>
        <p className="text-slate-400 text-sm mt-1">Integrity · Impact · Inclusion · Verification — alignement aux limites planétaires</p>
      </div>

      {/* 6 KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {([
          ["Funds",          summary.total,                                                            "text-green-400"],
          ["Avg Composite",  summary.avg_regen_finance_composite,                                     "text-emerald-400"],
          ["Greenwashing",   summary.greenwashing_signal_count,                                       "text-red-400"],
          ["Audit Requis",   summary.impact_audit_required_count,                                     "text-amber-400"],
          ["Avg Deficit",    `${summary.avg_estimated_impact_deficit_index.toFixed(1)}/10`,           "text-green-400"],
          ["Avg Integrity",  `${Math.round(summary.avg_integrity_score)}`,                            "text-teal-400"],
        ] as [string, string|number, string][]).map(([l,v,c])=>(
          <div key={l} className="bg-slate-900 border border-emerald-500/30 rounded-xl p-3 text-center">
            <div className={`text-xl font-bold ${c}`}>{v}</div>
            <div className="text-xs text-slate-500 mt-0.5">{l}</div>
          </div>
        ))}
      </div>

      {/* 4 GaugeRings */}
      <div className="bg-slate-900 border border-emerald-500/30 rounded-xl p-5">
        <div className="grid grid-cols-4 gap-4">
          <GaugeRing value={summary.avg_integrity_score}    label="Integrity"     color="#10b981"/>
          <GaugeRing value={summary.avg_impact_score}       label="Impact"        color="#34d399"/>
          <GaugeRing value={summary.avg_inclusion_score}    label="Inclusion"     color="#059669"/>
          <GaugeRing value={summary.avg_verification_score} label="Verification"  color="#06b6d4"/>
        </div>
      </div>

      {/* 4 DistBars */}
      <div className="bg-slate-900 border border-emerald-500/30 rounded-xl p-5 grid grid-cols-1 md:grid-cols-2 gap-5">
        {dists.map(d=><DistBar key={d.title} {...d}/>)}
      </div>

      {/* Filter pills */}
      <div className="flex flex-wrap gap-2">
        {["all","low","moderate","high","critical"].map(r=>(
          <button key={r} onClick={()=>setFilter(r)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${filter===r?"bg-emerald-700 border-emerald-600 text-white":"bg-slate-900 border-slate-700 text-slate-400 hover:text-white"}`}>
            {r}
          </button>
        ))}
        <span className="w-px h-5 self-center bg-slate-700"/>
        {["all","none","greenwashing_exposure","impact_dilution","exclusion_deficit","measurement_gap","capital_misallocation"].map(p=>(
          <button key={p} onClick={()=>setPat(p)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${patFilter===p?"bg-teal-900 border-teal-800 text-white":"bg-slate-900 border-slate-700 text-slate-400 hover:text-white"}`}>
            {p.replace(/_/g," ")}
          </button>
        ))}
      </div>

      {/* Fund cards grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {filtered.map(f=>(
          <div key={f.fund_id} onClick={()=>setSelected(f)}
            className="bg-slate-900 border border-emerald-500/30 rounded-xl p-4 cursor-pointer hover:border-emerald-500 transition-colors">
            <div className="flex items-center justify-between mb-1">
              <span className="font-bold text-white">{f.fund_id}</span>
              <span className="text-xs text-slate-400">{f.region}</span>
            </div>
            <div className="text-xs text-green-400 mb-2">{f.fund_type.replace(/_/g," ")}</div>
            <div className="flex gap-1 mb-3 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[f.regen_finance_risk as keyof typeof RISK_BADGE]||"bg-slate-700 text-slate-300"}`}>{f.regen_finance_risk}</span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[f.impact_severity as keyof typeof SEV_BADGE]||"bg-slate-700 text-slate-300"}`}>{f.impact_severity}</span>
            </div>
            <div className="text-2xl font-black text-white mb-1">{f.regen_finance_composite.toFixed(1)}</div>
            <div className="text-xs text-slate-500 mb-2 capitalize">{f.impact_pattern.replace(/_/g," ")}</div>
            <div className="text-xs text-green-400 font-medium mb-2">Déficit: {f.estimated_impact_deficit_index.toFixed(2)}/10</div>
            <div className="flex gap-1 flex-wrap">
              {f.has_greenwashing_signal && <span className="px-1.5 py-0.5 rounded bg-red-900 text-red-300 text-xs">GREENWASHING</span>}
              {f.requires_impact_audit   && <span className="px-1.5 py-0.5 rounded bg-amber-900 text-amber-300 text-xs">AUDIT</span>}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
