"use client";
import { useEffect, useState } from "react";

type Horizon = {
  horizon_id: string; temporal_domain: string; region: string;
  temporal_risk: string; temporal_pattern: string; temporal_severity: string;
  recommended_action: string;
  divergence_score: number; anticipation_score: number;
  synchronization_score: number; resilience_score: number;
  temporal_composite: number;
  has_bifurcation_signal: boolean; requires_realignment: boolean;
  estimated_temporal_risk_index: number; temporal_signal: string;
};
type Summary = {
  total: number; risk_counts: Record<string,number>; pattern_counts: Record<string,number>;
  severity_counts: Record<string,number>; action_counts: Record<string,number>;
  avg_temporal_composite: number; bifurcation_signal_count: number;
  realignment_required_count: number; avg_divergence_score: number;
  avg_anticipation_score: number; avg_synchronization_score: number;
  avg_resilience_score: number; avg_estimated_temporal_risk_index: number;
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

const RISK_COLORS    = { low:"#10b981", moderate:"#f59e0b", high:"#f97316", critical:"#ef4444" };
const PAT_COLORS     = {
  none:"#10b981", timeline_bifurcation:"#ef4444", temporal_blind_spot:"#dc2626",
  chronological_desync:"#a855f7", causal_loop_trap:"#f97316", future_optionality_collapse:"#f59e0b",
};
const SEV_COLORS     = {
  temporally_mastered:"#10b981", anticipating:"#f59e0b",
  desynchronized:"#f97316", temporally_lost:"#ef4444",
};
const ACT_COLORS     = {
  no_action:"#10b981", temporal_monitoring:"#06b6d4",
  chronological_resync:"#3b82f6", anticipation_upgrade:"#f59e0b",
  temporal_emergency_realignment:"#ef4444", timeline_convergence_protocol:"#dc2626",
};
const RISK_BADGE: Record<string,string> = {
  low:"bg-emerald-900 text-emerald-300", moderate:"bg-amber-900 text-amber-300",
  high:"bg-orange-900 text-orange-300", critical:"bg-red-900 text-red-300",
};
const SEV_BADGE: Record<string,string> = {
  temporally_mastered:"bg-emerald-900 text-emerald-300", anticipating:"bg-amber-900 text-amber-300",
  desynchronized:"bg-orange-900 text-orange-300", temporally_lost:"bg-red-900 text-red-300",
};

function DetailModal({ horizon, onClose }: { horizon: Horizon; onClose: () => void }) {
  const [tab, setTab] = useState<"scores"|"signal"|"action">("scores");
  useEffect(()=>{
    const h = (e: KeyboardEvent) => { if (e.key==="Escape") onClose(); };
    window.addEventListener("keydown", h);
    return ()=>window.removeEventListener("keydown", h);
  },[onClose]);
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70" onClick={onClose}>
      <div className="bg-slate-900 border border-yellow-500/30 rounded-xl w-full max-w-lg p-6 shadow-2xl" onClick={e=>e.stopPropagation()}>
        <div className="flex items-center justify-between mb-4">
          <div>
            <span className="text-lg font-bold text-white">{horizon.horizon_id}</span>
            <span className="ml-2 text-indigo-400 text-xs">{horizon.temporal_domain.replace(/_/g," ")}</span>
            <span className="ml-2 text-yellow-400 text-xs">{horizon.region}</span>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl leading-none">✕</button>
        </div>
        <div className="flex gap-2 mb-4">
          {(["scores","signal","action"] as const).map(t=>(
            <button key={t} onClick={()=>setTab(t)}
              className={`px-3 py-1 rounded text-xs font-medium transition-colors ${tab===t?"bg-indigo-700 text-white":"bg-slate-800 text-slate-400 hover:text-white"}`}>
              {t.charAt(0).toUpperCase()+t.slice(1)}
            </button>
          ))}
        </div>
        {tab==="scores" && (
          <div className="grid grid-cols-2 gap-3 text-sm">
            {[
              ["Divergence",       horizon.divergence_score,      "#ef4444"],
              ["Anticipation",     horizon.anticipation_score,    "#f97316"],
              ["Synchronisation",  horizon.synchronization_score, "#a855f7"],
              ["Résilience",       horizon.resilience_score,      "#6366f1"],
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
              <div className="text-slate-400 text-xs mb-1">Composite Temporel</div>
              <div className="text-white font-bold text-2xl">{horizon.temporal_composite.toFixed(1)}</div>
            </div>
          </div>
        )}
        {tab==="signal" && (
          <div className="bg-slate-800 rounded-lg p-4 text-sm text-slate-200 leading-relaxed">
            {horizon.temporal_signal}
            <div className="mt-3 flex gap-2 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[horizon.temporal_risk]||"bg-slate-700 text-slate-300"}`}>{horizon.temporal_risk}</span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[horizon.temporal_severity]||"bg-slate-700 text-slate-300"}`}>{horizon.temporal_severity}</span>
            </div>
          </div>
        )}
        {tab==="action" && (
          <div className="space-y-3 text-sm">
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Action Recommandée</div>
              <div className="text-white font-medium">{horizon.recommended_action.replace(/_/g," ")}</div>
            </div>
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Temporal Risk Index</div>
              <div className="text-white font-bold">{horizon.estimated_temporal_risk_index.toFixed(2)} / 10</div>
            </div>
            <div className="flex gap-2">
              {horizon.has_bifurcation_signal  && <span className="px-2 py-1 rounded bg-red-900 text-red-300 text-xs font-medium">BIFURCATION</span>}
              {horizon.requires_realignment     && <span className="px-2 py-1 rounded bg-amber-900 text-amber-300 text-xs font-medium">RÉALIGNEMENT</span>}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function TemporalEngineeringDashboard() {
  const [data, setData]         = useState<{ horizons: Horizon[]; summary: Summary }|null>(null);
  const [filter, setFilter]     = useState<string>("all");
  const [patFilter, setPat]     = useState<string>("all");
  const [selected, setSelected] = useState<Horizon|null>(null);

  useEffect(()=>{
    fetch("/api/temporal-engineering-engine")
      .then(r=>r.json()).then(setData).catch(console.error);
  },[]);

  if (!data) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-indigo-400 text-lg animate-pulse">Loading Temporal Engineering Engine...</div>
    </div>
  );

  const { horizons, summary } = data;
  const filtered = horizons.filter(h=>
    (filter==="all" || h.temporal_risk===filter) &&
    (patFilter==="all" || h.temporal_pattern===patFilter)
  );

  const dists: Array<{title:string;counts:Record<string,number>;colors:Record<string,string>}> = [
    { title:"Risque Temporel",        counts:summary.risk_counts,     colors:RISK_COLORS },
    { title:"Pattern Chronologique",  counts:summary.pattern_counts,  colors:PAT_COLORS  },
    { title:"Sévérité Horizon",       counts:summary.severity_counts, colors:SEV_COLORS  },
    { title:"Action Temporelle",      counts:summary.action_counts,   colors:ACT_COLORS  },
  ];

  const criticalCount  = summary.risk_counts["critical"] ?? 0;
  const avgCoherence   = summary.avg_synchronization_score;
  const avgAnticipation = summary.avg_anticipation_score;
  const alertCount     = summary.bifurcation_signal_count;
  const realignCount   = summary.realignment_required_count;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {selected && <DetailModal horizon={selected} onClose={()=>setSelected(null)}/>}

      <div>
        <h1 className="text-2xl font-bold text-white">Temporal Engineering & Multi-Chronological Anticipation Engine</h1>
        <p className="text-slate-400 text-sm mt-1">
          Horizons temporels · Bifurcations chronologiques · Anticipation multi-échelle · Fenêtres d&apos;intervention
        </p>
      </div>

      {/* 6 KPI cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {[
          ["Horizons Temporels",           summary.total,                           "text-indigo-400"],
          ["Bifurcations Critiques",        criticalCount,                           "text-red-400"],
          ["Cohérence Chronologique Moy.",  `${Math.round(avgCoherence)}`,           "text-yellow-400"],
          ["Profondeur Anticipation Moy.",  `${Math.round(avgAnticipation)}`,        "text-indigo-300"],
          ["Alertes Temporelles",           alertCount,                              "text-amber-400"],
          ["Réalignements Req.",            realignCount,                            "text-orange-400"],
        ].map(([l,v,c])=>(
          <div key={String(l)} className="bg-slate-900 border border-yellow-500/30 rounded-xl p-3 text-center">
            <div className={`text-xl font-bold ${c}`}>{v}</div>
            <div className="text-xs text-slate-500 mt-0.5">{l}</div>
          </div>
        ))}
      </div>

      {/* 4 GaugeRings */}
      <div className="bg-slate-900 border border-yellow-500/30 rounded-xl p-5">
        <div className="grid grid-cols-4 gap-4">
          <GaugeRing value={summary.avg_divergence_score}       label="Divergence Timeline"       color="#ef4444"/>
          <GaugeRing value={summary.avg_anticipation_score}     label="Précision Anticipation"    color="#f97316"/>
          <GaugeRing value={summary.avg_synchronization_score}  label="Synchronisation Multi-Échelle" color="#a855f7"/>
          <GaugeRing value={summary.avg_resilience_score}       label="Résilience Temporelle"     color="#6366f1"/>
        </div>
      </div>

      {/* 4 DistBars */}
      <div className="bg-slate-900 border border-yellow-500/30 rounded-xl p-5 grid grid-cols-1 md:grid-cols-2 gap-5">
        {dists.map(d=><DistBar key={d.title} {...d}/>)}
      </div>

      {/* Filter pills */}
      <div className="flex flex-wrap gap-2">
        {["all","low","moderate","high","critical"].map(r=>(
          <button key={r} onClick={()=>setFilter(r)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${filter===r?"bg-indigo-700 border-indigo-600 text-white":"bg-slate-900 border-slate-700 text-slate-400 hover:text-white"}`}>
            {r}
          </button>
        ))}
        <span className="w-px h-5 self-center bg-slate-700"/>
        {["all","timeline_bifurcation","temporal_blind_spot","chronological_desync","causal_loop_trap","future_optionality_collapse","none"].map(p=>(
          <button key={p} onClick={()=>setPat(p)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${patFilter===p?"bg-yellow-900 border-yellow-700 text-white":"bg-slate-900 border-slate-700 text-slate-400 hover:text-white"}`}>
            {p.replace(/_/g," ")}
          </button>
        ))}
      </div>

      {/* Horizon cards grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {filtered.map(h=>{
          const gaugeColor = h.temporal_risk==="critical"?"#ef4444":h.temporal_risk==="high"?"#f97316":h.temporal_risk==="moderate"?"#f59e0b":"#10b981";
          const r = 16; const circ = 2*Math.PI*r;
          const fill = circ*(1 - h.temporal_composite/100);
          return (
            <div key={h.horizon_id} onClick={()=>setSelected(h)}
              className="bg-slate-900 border border-yellow-500/30 rounded-xl p-4 cursor-pointer hover:border-indigo-500 transition-colors">
              <div className="flex items-center justify-between mb-1">
                <span className="font-bold text-white">{h.horizon_id}</span>
                <span className="text-xs text-slate-400">{h.region}</span>
              </div>
              <div className="text-xs text-indigo-400 mb-2 capitalize">{h.temporal_domain.replace(/_/g," ")}</div>
              <div className="flex gap-1 mb-3 flex-wrap">
                <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[h.temporal_risk]||"bg-slate-700 text-slate-300"}`}>{h.temporal_risk}</span>
                <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[h.temporal_severity]||"bg-slate-700 text-slate-300"}`}>{h.temporal_severity}</span>
              </div>
              {/* Temporal risk gauge */}
              <div className="flex items-center gap-3 mb-2">
                <svg width="44" height="44" viewBox="0 0 44 44">
                  <circle cx="22" cy="22" r={r} fill="none" stroke="#1e293b" strokeWidth="5"/>
                  <circle cx="22" cy="22" r={r} fill="none" stroke={gaugeColor} strokeWidth="5"
                    strokeDasharray={circ} strokeDashoffset={fill}
                    strokeLinecap="round" transform="rotate(-90 22 22)"/>
                  <text x="22" y="26" textAnchor="middle" fill="white" fontSize="8" fontWeight="bold">
                    {Math.round(h.temporal_composite)}
                  </text>
                </svg>
                <div>
                  <div className="text-xs text-slate-500 mb-0.5">Composite Temporel</div>
                  <div className="text-lg font-black text-white">{h.temporal_composite.toFixed(1)}</div>
                </div>
              </div>
              <div className="text-xs text-slate-500 mb-2 capitalize">{h.temporal_pattern.replace(/_/g," ")}</div>
              <div className="text-xs text-yellow-400 font-medium mb-2">Risk Index: {h.estimated_temporal_risk_index.toFixed(2)}/10</div>
              <div className="flex gap-1 flex-wrap">
                {h.has_bifurcation_signal && <span className="px-1.5 py-0.5 rounded bg-red-900 text-red-300 text-xs">BIFURCATION</span>}
                {h.requires_realignment   && <span className="px-1.5 py-0.5 rounded bg-amber-900 text-amber-300 text-xs">RÉALIGN.</span>}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
