"use client";
import { useEffect, useState } from "react";

type Asset = {
  asset_id: string; asset_category: string; region: string;
  ownership_risk: string; ownership_pattern: string;
  ownership_severity: string; recommended_action: string;
  liquidity_score: number; governance_score: number;
  trust_score: number; compliance_score: number;
  fractional_composite: number; has_freeze_signal: boolean;
  estimated_illiquidity_index: number; ownership_signal: string;
};
type Summary = {
  total: number; risk_counts: Record<string,number>;
  pattern_counts: Record<string,number>; severity_counts: Record<string,number>;
  action_counts: Record<string,number>; avg_fractional_composite: number;
  freeze_signal_count: number; avg_liquidity_score: number;
  avg_governance_score: number; avg_trust_score: number;
  avg_compliance_score: number; avg_estimated_illiquidity_index: number;
  emergency_action_count: number;
};

function GaugeRing({ value, label, color }: { value: number; label: string; color: string }) {
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

const RISK_COLORS  = { low:"#10b981", moderate:"#f59e0b", high:"#f97316", critical:"#ef4444" };
const PAT_COLORS   = { none:"#10b981", liquidity_freeze:"#ef4444", governance_capture:"#dc2626", oracle_manipulation:"#a855f7", regulatory_block:"#f97316", holder_exodus:"#eab308" };
const SEV_COLORS   = { liquid:"#10b981", maturing:"#f59e0b", illiquid:"#f97316", frozen:"#ef4444" };
const ACT_COLORS   = { no_action:"#10b981", token_monitoring:"#06b6d4", market_deepening:"#3b82f6", compliance_sprint:"#f59e0b", emergency_liquidity:"#ef4444", governance_reset:"#dc2626" };
const RISK_BADGE   = { low:"bg-emerald-900 text-emerald-300", moderate:"bg-amber-900 text-amber-300", high:"bg-orange-900 text-orange-300", critical:"bg-red-900 text-red-300" };
const SEV_BADGE    = { liquid:"bg-emerald-900 text-emerald-300", maturing:"bg-amber-900 text-amber-300", illiquid:"bg-orange-900 text-orange-300", frozen:"bg-red-900 text-red-300" };

function DetailModal({ asset, onClose }: { asset: Asset; onClose: () => void }) {
  const [tab, setTab] = useState<"scores"|"signal"|"action">("scores");
  useEffect(()=>{
    const h = (e: KeyboardEvent) => { if (e.key==="Escape") onClose(); };
    window.addEventListener("keydown", h);
    return ()=>window.removeEventListener("keydown", h);
  },[onClose]);
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70" onClick={onClose}>
      <div className="bg-slate-900 border border-yellow-600/30 rounded-xl w-full max-w-lg p-6 shadow-2xl" onClick={e=>e.stopPropagation()}>
        <div className="flex items-center justify-between mb-4">
          <div>
            <span className="text-lg font-bold text-white">{asset.asset_id}</span>
            <span className="ml-2 text-yellow-400 text-xs">{asset.asset_category.replace(/_/g," ")}</span>
            <span className="ml-2 text-yellow-500 text-xs">{asset.region}</span>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl leading-none">✕</button>
        </div>
        <div className="flex gap-2 mb-4">
          {(["scores","signal","action"] as const).map(t=>(
            <button key={t} onClick={()=>setTab(t)}
              className={`px-3 py-1 rounded text-xs font-medium transition-colors ${tab===t?"bg-yellow-600 text-white":"bg-slate-800 text-slate-400 hover:text-white"}`}>
              {t.charAt(0).toUpperCase()+t.slice(1)}
            </button>
          ))}
        </div>
        {tab==="scores" && (
          <div className="grid grid-cols-2 gap-3 text-sm">
            {[
              ["Liquidité",         asset.liquidity_score,   "#eab308"],
              ["Gouvernance",       asset.governance_score,  "#f59e0b"],
              ["Confiance",         asset.trust_score,       "#f97316"],
              ["Conformité",        asset.compliance_score,  "#ef4444"],
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
              <div className="text-slate-400 text-xs mb-1">Fractional Composite</div>
              <div className="text-white font-bold text-2xl">{asset.fractional_composite.toFixed(1)}</div>
            </div>
          </div>
        )}
        {tab==="signal" && (
          <div className="bg-slate-800 rounded-lg p-4 text-sm text-slate-200 leading-relaxed">
            {asset.ownership_signal}
            <div className="mt-3 flex gap-2 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[asset.ownership_risk as keyof typeof RISK_BADGE]||"bg-slate-700 text-slate-300"}`}>{asset.ownership_risk}</span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[asset.ownership_severity as keyof typeof SEV_BADGE]||"bg-slate-700 text-slate-300"}`}>{asset.ownership_severity}</span>
            </div>
          </div>
        )}
        {tab==="action" && (
          <div className="space-y-3 text-sm">
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Recommended Action</div>
              <div className="text-white font-medium">{asset.recommended_action.replace(/_/g," ")}</div>
            </div>
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Illiquidity Index</div>
              <div className="text-white font-bold">{asset.estimated_illiquidity_index.toFixed(2)} / 10</div>
            </div>
            <div className="flex gap-2">
              {asset.has_freeze_signal && <span className="px-2 py-1 rounded bg-yellow-900 text-yellow-300 text-xs font-medium">FREEZE ALERT</span>}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function FractionalOwnershipDashboard() {
  const [data, setData]         = useState<{ assets: Asset[]; summary: Summary }|null>(null);
  const [filter, setFilter]     = useState<string>("all");
  const [patFilter, setPat]     = useState<string>("all");
  const [selected, setSelected] = useState<Asset|null>(null);

  useEffect(()=>{
    fetch("/api/fractional-ownership-engine")
      .then(r=>r.json()).then(setData).catch(console.error);
  },[]);

  if (!data) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-yellow-400 text-lg animate-pulse">Loading Fractional Ownership Engine...</div>
    </div>
  );

  const { assets, summary } = data;
  const filtered = assets.filter(a=>
    (filter==="all" || a.ownership_risk===filter) &&
    (patFilter==="all" || a.ownership_pattern===patFilter)
  );

  const dists = [
    { title:"Risque de Propriété",   counts:summary.risk_counts,     colors:RISK_COLORS },
    { title:"Pattern Fractionnel",   counts:summary.pattern_counts,  colors:PAT_COLORS  },
    { title:"Sévérité Liquidité",    counts:summary.severity_counts, colors:SEV_COLORS  },
    { title:"Action Recommandée",    counts:summary.action_counts,   colors:ACT_COLORS  },
  ] as Array<{title:string;counts:Record<string,number>;colors:Record<string,string>}>;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {selected && <DetailModal asset={selected} onClose={()=>setSelected(null)}/>}

      <div>
        <h1 className="text-2xl font-bold text-white">Fractional Ownership &amp; Tokenized Economy Intelligence Engine</h1>
        <p className="text-slate-400 text-sm mt-1">Liquidité · Gouvernance · Confiance · Conformité — actifs fractionnés et économie tokenisée</p>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {[
          ["Total Actifs",       summary.total,                                "text-yellow-400"],
          ["Critiques",          (summary.risk_counts["critical"] || 0),       "text-red-400"],
          ["Freeze Alerts",      summary.freeze_signal_count,                  "text-yellow-300"],
          ["Avg Composite",      summary.avg_fractional_composite,             "text-yellow-400"],
          ["Avg Liquidité",      `${Math.round(summary.avg_liquidity_score)}`, "text-amber-400"],
          ["Actions Urgentes",   summary.emergency_action_count,               "text-red-400"],
        ].map(([l,v,c])=>(
          <div key={String(l)} className="bg-slate-900 border border-yellow-600/30 rounded-xl p-3 text-center">
            <div className={`text-xl font-bold ${c}`}>{v}</div>
            <div className="text-xs text-slate-500 mt-0.5">{l}</div>
          </div>
        ))}
      </div>

      <div className="bg-slate-900 border border-yellow-600/30 rounded-xl p-5">
        <div className="grid grid-cols-4 gap-4">
          <GaugeRing value={summary.avg_liquidity_score}   label="Santé Liquidité"   color="#eab308"/>
          <GaugeRing value={summary.avg_governance_score}  label="Santé Gouvernance" color="#f59e0b"/>
          <GaugeRing value={summary.avg_trust_score}       label="Confiance Contrat" color="#f97316"/>
          <GaugeRing value={summary.avg_compliance_score}  label="Conformité Réglementaire" color="#ef4444"/>
        </div>
      </div>

      <div className="bg-slate-900 border border-yellow-600/30 rounded-xl p-5 grid grid-cols-1 md:grid-cols-2 gap-5">
        {dists.map(d=><DistBar key={d.title} {...d}/>)}
      </div>

      <div className="flex flex-wrap gap-2">
        {["all","low","moderate","high","critical"].map(r=>(
          <button key={r} onClick={()=>setFilter(r)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${filter===r?"bg-yellow-600 border-yellow-500 text-white":"bg-slate-900 border-slate-700 text-slate-400 hover:text-white"}`}>
            {r}
          </button>
        ))}
        <span className="w-px h-5 self-center bg-slate-700"/>
        {["all","none","liquidity_freeze","governance_capture","oracle_manipulation","regulatory_block","holder_exodus"].map(p=>(
          <button key={p} onClick={()=>setPat(p)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${patFilter===p?"bg-yellow-700 border-yellow-600 text-white":"bg-slate-900 border-slate-700 text-slate-400 hover:text-white"}`}>
            {p.replace(/_/g," ")}
          </button>
        ))}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {filtered.map(a=>(
          <div key={a.asset_id} onClick={()=>setSelected(a)}
            className="bg-slate-900 border border-yellow-600/30 rounded-xl p-4 cursor-pointer hover:border-yellow-500 transition-colors">
            <div className="flex items-center justify-between mb-1">
              <span className="font-bold text-white">{a.asset_id}</span>
              <span className="text-xs text-slate-400">{a.region}</span>
            </div>
            <div className="text-xs text-yellow-400 mb-2">{a.asset_category.replace(/_/g," ")}</div>
            <div className="flex gap-1 mb-3 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[a.ownership_risk as keyof typeof RISK_BADGE]||"bg-slate-700 text-slate-300"}`}>{a.ownership_risk}</span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[a.ownership_severity as keyof typeof SEV_BADGE]||"bg-slate-700 text-slate-300"}`}>{a.ownership_severity}</span>
            </div>
            <div className="text-2xl font-black text-white mb-1">{a.fractional_composite.toFixed(1)}</div>
            <div className="text-xs text-slate-500 mb-2 capitalize">{a.ownership_pattern.replace(/_/g," ")}</div>
            <div className="text-xs text-yellow-400 font-medium mb-2">ILI: {a.estimated_illiquidity_index.toFixed(2)}/10</div>
            <div className="flex gap-1 flex-wrap">
              {a.has_freeze_signal && <span className="px-1.5 py-0.5 rounded bg-yellow-900 text-yellow-300 text-xs">FREEZE ALERT</span>}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
