"use client";
import { useEffect, useState } from "react";

type Asset = {
  asset_id: string; asset_class: string; region: string;
  economy_risk: string; economy_pattern: string;
  economy_severity: string; recommended_action: string;
  valuation_score: number; market_score: number;
  resilience_score: number; disruption_score: number;
  singularity_composite: number; has_bubble_signal: boolean;
  estimated_bubble_risk_index: number; economy_signal: string;
};
type Summary = {
  total: number; risk_counts: Record<string,number>;
  pattern_counts: Record<string,number>; severity_counts: Record<string,number>;
  action_counts: Record<string,number>; avg_singularity_composite: number;
  bubble_alert_count: number; emergency_count: number;
  avg_valuation_score: number; avg_market_score: number;
  avg_resilience_score: number; avg_disruption_score: number;
  avg_estimated_bubble_risk_index: number;
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
const PAT_COLORS  = { none:"#10b981", speculative_bubble:"#ef4444", regulatory_collapse:"#dc2626", liquidity_crisis:"#f97316", value_evaporation:"#a855f7", paradigm_displacement:"#eab308" };
const SEV_COLORS  = { stable:"#10b981", speculative:"#f59e0b", volatile:"#f97316", bubble:"#ef4444" };
const ACT_COLORS  = { no_action:"#10b981", valuation_monitoring:"#06b6d4", portfolio_rebalancing:"#3b82f6", risk_hedging:"#f59e0b", emergency_liquidation:"#ef4444", regulatory_intervention:"#dc2626" };
const RISK_BADGE  = { low:"bg-emerald-900 text-emerald-300", moderate:"bg-amber-900 text-amber-300", high:"bg-orange-900 text-orange-300", critical:"bg-red-900 text-red-300" };
const SEV_BADGE   = { stable:"bg-emerald-900 text-emerald-300", speculative:"bg-amber-900 text-amber-300", volatile:"bg-orange-900 text-orange-300", bubble:"bg-red-900 text-red-300" };

function DetailModal({ asset, onClose }: { asset: Asset; onClose: () => void }) {
  const [tab, setTab] = useState<"scores"|"signal"|"action">("scores");
  useEffect(()=>{
    const h = (e: KeyboardEvent) => { if (e.key==="Escape") onClose(); };
    window.addEventListener("keydown", h);
    return ()=>window.removeEventListener("keydown", h);
  },[onClose]);
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70" onClick={onClose}>
      <div className="bg-slate-900 border border-slate-700 rounded-xl w-full max-w-lg p-6 shadow-2xl" onClick={e=>e.stopPropagation()}>
        <div className="flex items-center justify-between mb-4">
          <div>
            <span className="text-lg font-bold text-white">{asset.asset_id}</span>
            <span className="ml-2 text-amber-400 text-xs">{asset.asset_class}</span>
            <span className="ml-2 text-yellow-500 text-xs">{asset.region}</span>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl leading-none">✕</button>
        </div>
        <div className="flex gap-2 mb-4">
          {(["scores","signal","action"] as const).map(t=>(
            <button key={t} onClick={()=>setTab(t)}
              className={`px-3 py-1 rounded text-xs font-medium transition-colors ${tab===t?"bg-amber-600 text-white":"bg-slate-800 text-slate-400 hover:text-white"}`}>
              {t.charAt(0).toUpperCase()+t.slice(1)}
            </button>
          ))}
        </div>
        {tab==="scores" && (
          <div className="grid grid-cols-2 gap-3 text-sm">
            {[
              ["Stabilité Valuation", asset.valuation_score,  "#f59e0b"],
              ["Intégrité Marché",    asset.market_score,     "#eab308"],
              ["Résilience Actif",    asset.resilience_score, "#f97316"],
              ["Disruption Paradigme",asset.disruption_score, "#ef4444"],
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
              <div className="text-slate-400 text-xs mb-1">Singularity Composite</div>
              <div className="text-white font-bold text-2xl">{asset.singularity_composite.toFixed(1)}</div>
            </div>
          </div>
        )}
        {tab==="signal" && (
          <div className="bg-slate-800 rounded-lg p-4 text-sm text-slate-200 leading-relaxed">
            {asset.economy_signal}
            <div className="mt-3 flex gap-2 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[asset.economy_risk as keyof typeof RISK_BADGE]||"bg-slate-700 text-slate-300"}`}>{asset.economy_risk}</span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[asset.economy_severity as keyof typeof SEV_BADGE]||"bg-slate-700 text-slate-300"}`}>{asset.economy_severity}</span>
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
              <div className="text-slate-400 text-xs mb-1">Bubble Risk Index</div>
              <div className="text-white font-bold">{asset.estimated_bubble_risk_index.toFixed(2)} / 10</div>
            </div>
            <div className="flex gap-2">
              {asset.has_bubble_signal && <span className="px-2 py-1 rounded bg-amber-900 text-amber-300 text-xs font-medium">BUBBLE ALERT</span>}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function SingularityEconomyDashboard() {
  const [data, setData]         = useState<{ assets: Asset[]; summary: Summary }|null>(null);
  const [filter, setFilter]     = useState<string>("all");
  const [patFilter, setPat]     = useState<string>("all");
  const [selected, setSelected] = useState<Asset|null>(null);

  useEffect(()=>{
    fetch("/api/singularity-economy-engine")
      .then(r=>r.json()).then(setData).catch(console.error);
  },[]);

  if (!data) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-amber-400 text-lg animate-pulse">Loading Singularity Economy Engine...</div>
    </div>
  );

  const { assets, summary } = data;
  const filtered = assets.filter(a=>
    (filter==="all" || a.economy_risk===filter) &&
    (patFilter==="all" || a.economy_pattern===patFilter)
  );

  const dists = [
    { title:"Risque Économique",    counts:summary.risk_counts,     colors:RISK_COLORS },
    { title:"Pattern Spéculatif",   counts:summary.pattern_counts,  colors:PAT_COLORS  },
    { title:"Sévérité Actif",       counts:summary.severity_counts, colors:SEV_COLORS  },
    { title:"Action Recommandée",   counts:summary.action_counts,   colors:ACT_COLORS  },
  ] as Array<{title:string;counts:Record<string,number>;colors:Record<string,string>}>;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {selected && <DetailModal asset={selected} onClose={()=>setSelected(null)}/>}

      <div>
        <h1 className="text-2xl font-bold text-white">Singularity Economy & Post-Rare Asset Valuation Engine</h1>
        <p className="text-slate-400 text-sm mt-1">Valorisation · Marché · Résilience · Disruption — actifs post-rares et économie singulière</p>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {[
          ["Total Actifs",     summary.total,                                                   "text-amber-400"],
          ["Critiques",        (summary.risk_counts["critical"] || 0),                          "text-red-400"],
          ["Bubble Alerts",    summary.bubble_alert_count,                                      "text-yellow-400"],
          ["Avg Composite",    summary.avg_singularity_composite,                               "text-amber-300"],
          ["Avg Valuation",    `${Math.round(summary.avg_valuation_score)}`,                    "text-yellow-400"],
          ["Avg Market",       `${Math.round(summary.avg_market_score)}`,                       "text-amber-400"],
        ].map(([l,v,c])=>(
          <div key={String(l)} className="bg-slate-900 border border-slate-800 rounded-xl p-3 text-center">
            <div className={`text-xl font-bold ${c}`}>{v}</div>
            <div className="text-xs text-slate-500 mt-0.5">{l}</div>
          </div>
        ))}
      </div>

      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
        <div className="grid grid-cols-4 gap-4">
          <Gauge value={summary.avg_valuation_score}  label="Stabilité Valuation"  color="#f59e0b"/>
          <Gauge value={summary.avg_market_score}     label="Intégrité Marché"     color="#eab308"/>
          <Gauge value={summary.avg_resilience_score} label="Résilience Actif"     color="#f97316"/>
          <Gauge value={summary.avg_disruption_score} label="Disruption Paradigme" color="#ef4444"/>
        </div>
      </div>

      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 grid grid-cols-1 md:grid-cols-2 gap-5">
        {dists.map(d=><DistBar key={d.title} {...d}/>)}
      </div>

      <div className="flex flex-wrap gap-2">
        {["all","low","moderate","high","critical"].map(r=>(
          <button key={r} onClick={()=>setFilter(r)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${filter===r?"bg-amber-600 border-amber-500 text-white":"bg-slate-900 border-slate-700 text-slate-400 hover:text-white"}`}>
            {r}
          </button>
        ))}
        <span className="w-px h-5 self-center bg-slate-700"/>
        {["all","none","speculative_bubble","regulatory_collapse","liquidity_crisis","value_evaporation","paradigm_displacement"].map(p=>(
          <button key={p} onClick={()=>setPat(p)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${patFilter===p?"bg-yellow-700 border-yellow-600 text-white":"bg-slate-900 border-slate-700 text-slate-400 hover:text-white"}`}>
            {p.replace(/_/g," ")}
          </button>
        ))}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {filtered.map(a=>(
          <div key={a.asset_id} onClick={()=>setSelected(a)}
            className="bg-slate-900 border border-slate-800 rounded-xl p-4 cursor-pointer hover:border-amber-600 transition-colors">
            <div className="flex items-center justify-between mb-1">
              <span className="font-bold text-white">{a.asset_id}</span>
              <span className="text-xs text-slate-400">{a.region}</span>
            </div>
            <div className="text-xs text-amber-400 mb-2">{a.asset_class.replace(/_/g," ")}</div>
            <div className="flex gap-1 mb-3 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[a.economy_risk as keyof typeof RISK_BADGE]||"bg-slate-700 text-slate-300"}`}>{a.economy_risk}</span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[a.economy_severity as keyof typeof SEV_BADGE]||"bg-slate-700 text-slate-300"}`}>{a.economy_severity}</span>
            </div>
            <div className="text-2xl font-black text-white mb-1">{a.singularity_composite.toFixed(1)}</div>
            <div className="text-xs text-slate-500 mb-2 capitalize">{a.economy_pattern.replace(/_/g," ")}</div>
            <div className="text-xs text-amber-400 font-medium mb-2">BRI: {a.estimated_bubble_risk_index.toFixed(2)}/10</div>
            <div className="flex gap-1 flex-wrap">
              {a.has_bubble_signal && <span className="px-1.5 py-0.5 rounded bg-amber-900 text-amber-300 text-xs">BUBBLE ALERT</span>}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
