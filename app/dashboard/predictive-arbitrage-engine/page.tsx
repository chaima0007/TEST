"use client";
import { useEffect, useState } from "react";

type ArbitrageSignal = {
  signal_id: string;
  signal_type: string;
  region: string;
  signal_quality_score: number;
  alpha_capture_score: number;
  execution_score: number;
  resilience_score: number;
  arbitrage_composite: number;
  arbitrage_risk: string;
  arbitrage_pattern: string;
  arbitrage_severity: string;
  recommended_action: string;
  arbitrage_signal: string;
  avg_estimated_alpha_decay_index: number;
  has_active_alert: boolean;
};

type Summary = {
  total: number;
  risk_counts: Record<string,number>;
  pattern_counts: Record<string,number>;
  severity_counts: Record<string,number>;
  action_counts: Record<string,number>;
  avg_arbitrage_composite: number;
  alert_count: number;
  transformation_required_count: number;
  avg_signal_quality_score: number;
  avg_alpha_capture_score: number;
  avg_execution_score: number;
  avg_resilience_score: number;
  avg_estimated_alpha_decay_index: number;
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

const RISK_COLORS   = { low:"#10b981", moderate:"#f59e0b", high:"#f97316", critical:"#ef4444" };
const PAT_COLORS    = { none:"#10b981", signal_degradation:"#ef4444", alpha_erosion:"#dc2626", execution_failure:"#f97316", model_overfit:"#a855f7", regime_blindness:"#0891b2" };
const SEV_COLORS    = { optimal:"#10b981", stable:"#06b6d4", degrading:"#f97316", collapsing:"#ef4444" };
const ACT_COLORS    = { no_action:"#10b981", performance_monitoring:"#06b6d4", signal_recalibration:"#3b82f6", ensemble_retrain:"#a855f7", risk_deleverage:"#f97316", model_rebuild:"#ef4444", execution_overhaul:"#dc2626", alpha_crisis:"#7f1d1d" };
const RISK_BADGE    = { low:"bg-emerald-900 text-emerald-300", moderate:"bg-amber-900 text-amber-300", high:"bg-orange-900 text-orange-300", critical:"bg-red-900 text-red-300" };
const SEV_BADGE     = { optimal:"bg-emerald-900 text-emerald-300", stable:"bg-cyan-900 text-cyan-300", degrading:"bg-orange-900 text-orange-300", collapsing:"bg-red-900 text-red-300" };

function DetailModal({ signal, onClose }: { signal: ArbitrageSignal; onClose: () => void }) {
  const [tab, setTab] = useState<"scores"|"signal"|"action">("scores");
  useEffect(() => {
    const h = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", h);
    return () => window.removeEventListener("keydown", h);
  }, [onClose]);
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70" onClick={onClose}>
      <div className="bg-slate-900 border border-teal-500/30 rounded-xl w-full max-w-lg p-6 shadow-2xl" onClick={e=>e.stopPropagation()}>
        <div className="flex items-center justify-between mb-4">
          <div>
            <span className="text-lg font-bold text-white">{signal.signal_id}</span>
            <span className="ml-2 text-cyan-400 text-xs">{signal.signal_type.replace(/_/g," ")}</span>
            <span className="ml-2 text-teal-400 text-xs">{signal.region}</span>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl leading-none">✕</button>
        </div>
        <div className="flex gap-2 mb-4">
          {(["scores","signal","action"] as const).map(t=>(
            <button key={t} onClick={()=>setTab(t)}
              className={`px-3 py-1 rounded text-xs font-medium transition-colors ${tab===t?"bg-cyan-700 text-white":"bg-slate-800 text-slate-400 hover:text-white"}`}>
              {t.charAt(0).toUpperCase()+t.slice(1)}
            </button>
          ))}
        </div>
        {tab==="scores" && (
          <div className="grid grid-cols-2 gap-3 text-sm">
            {[
              ["Qualité Signal",  signal.signal_quality_score, "#06b6d4"],
              ["Capture Alpha",   signal.alpha_capture_score,  "#f97316"],
              ["Exécution",       signal.execution_score,      "#a855f7"],
              ["Résilience",      signal.resilience_score,     "#10b981"],
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
              <div className="text-slate-400 text-xs mb-1">Composite Arbitrage</div>
              <div className="text-white font-bold text-2xl">{signal.arbitrage_composite.toFixed(1)}</div>
            </div>
          </div>
        )}
        {tab==="signal" && (
          <div className="bg-slate-800 rounded-lg p-4 text-sm text-slate-200 leading-relaxed">
            {signal.arbitrage_signal}
            <div className="mt-3 flex gap-2 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[signal.arbitrage_risk as keyof typeof RISK_BADGE]||"bg-slate-700 text-slate-300"}`}>{signal.arbitrage_risk}</span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[signal.arbitrage_severity as keyof typeof SEV_BADGE]||"bg-slate-700 text-slate-300"}`}>{signal.arbitrage_severity}</span>
              {signal.has_active_alert && (
                <span className="px-2 py-0.5 rounded text-xs font-medium bg-red-900 text-red-300">Alerte Active</span>
              )}
            </div>
          </div>
        )}
        {tab==="action" && (
          <div className="space-y-3 text-sm">
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Action Recommandée</div>
              <div className="text-white font-medium">{signal.recommended_action.replace(/_/g," ")}</div>
            </div>
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Pattern Détecté</div>
              <div className="text-white font-medium">{signal.arbitrage_pattern.replace(/_/g," ")}</div>
            </div>
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Indice Décroissance Alpha</div>
              <div className="text-white font-bold">{signal.avg_estimated_alpha_decay_index.toFixed(2)} / 10</div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function PredictiveArbitrageDashboard() {
  const [data, setData]         = useState<{ signals: ArbitrageSignal[]; summary: Summary }|null>(null);
  const [filter, setFilter]     = useState<string>("all");
  const [patFilter, setPat]     = useState<string>("all");
  const [selected, setSelected] = useState<ArbitrageSignal|null>(null);

  useEffect(()=>{
    fetch("/api/predictive-arbitrage-engine")
      .then(r=>r.json()).then(setData).catch(console.error);
  },[]);

  if (!data) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-cyan-400 text-lg animate-pulse">Loading Predictive Arbitrage Engine...</div>
    </div>
  );

  const { signals, summary } = data;
  const filtered = signals.filter(s=>
    (filter==="all" || s.arbitrage_risk===filter) &&
    (patFilter==="all" || s.arbitrage_pattern===patFilter)
  );

  const dists: Array<{title:string;counts:Record<string,number>;colors:Record<string,string>}> = [
    { title:"Risque Arbitrage",        counts:summary.risk_counts,     colors:RISK_COLORS },
    { title:"Pattern Signal",          counts:summary.pattern_counts,  colors:PAT_COLORS  },
    { title:"Sévérité Modèle",         counts:summary.severity_counts, colors:SEV_COLORS  },
    { title:"Action Recommandée",      counts:summary.action_counts,   colors:ACT_COLORS  },
  ];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {selected && <DetailModal signal={selected} onClose={()=>setSelected(null)}/>}

      <div>
        <h1 className="text-2xl font-bold text-white">Predictive Analytics &amp; Algorithmic Arbitrage Engine</h1>
        <p className="text-slate-400 text-sm mt-1">Qualité Signal · Capture Alpha · Exécution · Résilience — surveillance des opportunités d&apos;arbitrage algorithmique</p>
      </div>

      {/* KPI strip — 6 cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {[
          ["Total Signaux",          summary.total,                                   "text-cyan-400"],
          ["Signaux Critiques",      summary.risk_counts["critical"] ?? 0,            "text-red-400"],
          ["Score Signal Moy.",      summary.avg_signal_quality_score,                "text-teal-400"],
          ["Score Alpha Moy.",       summary.avg_alpha_capture_score,                 "text-orange-400"],
          ["Alertes Actives",        summary.alert_count,                             "text-amber-400"],
          ["Transformations Req.",   summary.transformation_required_count,           "text-cyan-400"],
        ].map(([l,v,c])=>(
          <div key={String(l)} className="bg-slate-900 border border-teal-500/30 rounded-xl p-3 text-center">
            <div className={`text-xl font-bold ${c}`}>{v}</div>
            <div className="text-xs text-slate-500 mt-0.5">{l}</div>
          </div>
        ))}
      </div>

      {/* 4 SVG GaugeRing */}
      <div className="bg-slate-900 border border-teal-500/30 rounded-xl p-5">
        <div className="grid grid-cols-4 gap-4">
          <GaugeRing value={summary.avg_signal_quality_score} label="Qualité Signal"  color="#06b6d4"/>
          <GaugeRing value={summary.avg_alpha_capture_score}  label="Capture Alpha"   color="#f97316"/>
          <GaugeRing value={summary.avg_execution_score}      label="Exécution"        color="#a855f7"/>
          <GaugeRing value={summary.avg_resilience_score}     label="Résilience"       color="#10b981"/>
        </div>
      </div>

      {/* 4 DistBar distributions */}
      <div className="bg-slate-900 border border-teal-500/30 rounded-xl p-5 grid grid-cols-1 md:grid-cols-2 gap-5">
        {dists.map(d=><DistBar key={d.title} {...d}/>)}
      </div>

      {/* Filter pills — risk + pattern */}
      <div className="flex flex-wrap gap-2">
        {["all","low","moderate","high","critical"].map(r=>(
          <button key={r} onClick={()=>setFilter(r)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${filter===r?"bg-cyan-700 border-cyan-600 text-white":"bg-slate-900 border-slate-700 text-slate-400 hover:text-white"}`}>
            {r}
          </button>
        ))}
        <span className="w-px h-5 self-center bg-slate-700"/>
        {["all","signal_degradation","alpha_erosion","execution_failure","model_overfit","regime_blindness","none"].map(p=>(
          <button key={p} onClick={()=>setPat(p)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${patFilter===p?"bg-teal-900 border-teal-800 text-white":"bg-slate-900 border-slate-700 text-slate-400 hover:text-white"}`}>
            {p.replace(/_/g," ")}
          </button>
        ))}
      </div>

      {/* Signal cards grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {filtered.map(s=>(
          <div key={s.signal_id} onClick={()=>setSelected(s)}
            className="bg-slate-900 border border-teal-500/30 rounded-xl p-4 cursor-pointer hover:border-cyan-500 transition-colors">
            <div className="flex items-center justify-between mb-1">
              <span className="font-bold text-white">{s.signal_id}</span>
              <span className="text-xs text-slate-400">{s.region}</span>
            </div>
            <div className="text-xs text-cyan-400 mb-2 capitalize">{s.signal_type.replace(/_/g," ")}</div>
            <div className="flex gap-1 mb-3 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[s.arbitrage_risk as keyof typeof RISK_BADGE]||"bg-slate-700 text-slate-300"}`}>{s.arbitrage_risk}</span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[s.arbitrage_severity as keyof typeof SEV_BADGE]||"bg-slate-700 text-slate-300"}`}>{s.arbitrage_severity}</span>
            </div>
            {/* Composite gauge value */}
            <div className="text-2xl font-black text-white mb-1">{s.arbitrage_composite.toFixed(1)}</div>
            <div className="text-xs text-slate-500 mb-2 capitalize">{s.arbitrage_pattern.replace(/_/g," ")}</div>
            {/* 4 score bars */}
            <div className="space-y-1 mb-2">
              {[
                ["Qualité Signal", s.signal_quality_score,  "#06b6d4"],
                ["Capture Alpha",  s.alpha_capture_score,   "#f97316"],
                ["Exécution",      s.execution_score,       "#a855f7"],
                ["Résilience",     s.resilience_score,      "#10b981"],
              ].map(([l,v,c])=>(
                <div key={String(l)} className="flex items-center gap-2">
                  <span className="text-xs text-slate-500 w-20 shrink-0">{String(l)}</span>
                  <div className="flex-1 h-1.5 bg-slate-800 rounded">
                    <div className="h-1.5 rounded" style={{width:`${Math.min(Number(v),100)}%`,background:String(c)}}/>
                  </div>
                  <span className="text-xs text-slate-400 w-8 text-right">{Number(v).toFixed(0)}</span>
                </div>
              ))}
            </div>
            <div className="text-xs text-cyan-400 font-medium">Décroissance: {s.avg_estimated_alpha_decay_index.toFixed(2)}/10</div>
            {s.has_active_alert && (
              <div className="mt-1 text-xs text-red-400 font-medium">⚠ Alerte Active</div>
            )}
            <div className="text-xs text-slate-400 line-clamp-2 leading-relaxed mt-1">{s.arbitrage_signal}</div>
          </div>
        ))}
      </div>
    </div>
  );
}
