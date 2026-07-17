"use client";
import { useEffect, useState } from "react";

type Decision = {
  decision_id: string; decision_type: string; region: string;
  temporal_risk: string; timing_pattern: string; timing_severity: string;
  recommended_action: string; opportunity_score: number; readiness_score: number;
  alignment_score: number; risk_score: number; temporal_composite: number;
  missed_window: boolean; acceleration_required: boolean;
  estimated_timing_loss_index: number; timing_signal: string;
};
type Summary = {
  total: number; risk_counts: Record<string,number>; pattern_counts: Record<string,number>;
  severity_counts: Record<string,number>; action_counts: Record<string,number>;
  avg_temporal_composite: number; missed_window_count: number;
  acceleration_required_count: number; avg_opportunity_score: number;
  avg_readiness_score: number; avg_alignment_score: number; avg_risk_score: number;
  avg_estimated_timing_loss_index: number;
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

const RISK_COLORS  = { low:"#10b981", moderate:"#f59e0b", high:"#f97316", critical:"#ef4444" };
const PAT_COLORS   = { none:"#10b981", timing_miss:"#ef4444", window_collapse:"#dc2626", premature_action:"#a855f7", delayed_response:"#f97316", timing_conflict:"#f59e0b" };
const SEV_COLORS   = { optimal:"#10b981", watch:"#f59e0b", closing:"#f97316", missed:"#ef4444" };
const ACT_COLORS   = { no_action:"#10b981", timing_monitoring:"#06b6d4", timing_recalibration:"#3b82f6", window_capture:"#f59e0b", emergency_acceleration:"#ef4444", strategic_pause:"#dc2626" };
const RISK_BADGE   = { low:"bg-emerald-900 text-emerald-300", moderate:"bg-amber-900 text-amber-300", high:"bg-orange-900 text-orange-300", critical:"bg-red-900 text-red-300" };
const SEV_BADGE    = { optimal:"bg-emerald-900 text-emerald-300", watch:"bg-amber-900 text-amber-300", closing:"bg-orange-900 text-orange-300", missed:"bg-red-900 text-red-300" };

function DetailModal({ decision, onClose }: { decision: Decision; onClose: () => void }) {
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
            <span className="text-lg font-bold text-white">{decision.decision_id}</span>
            <span className="ml-2 text-cyan-400 text-xs">{decision.decision_type.replace(/_/g," ")}</span>
            <span className="ml-2 text-sky-400 text-xs">{decision.region}</span>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl leading-none">✕</button>
        </div>
        <div className="flex gap-2 mb-4">
          {(["scores","signal","action"] as const).map(t=>(
            <button key={t} onClick={()=>setTab(t)}
              className={`px-3 py-1 rounded text-xs font-medium transition-colors ${tab===t?"bg-sky-700 text-white":"bg-slate-800 text-slate-400 hover:text-white"}`}>
              {t.charAt(0).toUpperCase()+t.slice(1)}
            </button>
          ))}
        </div>
        {tab==="scores" && (
          <div className="grid grid-cols-2 gap-3 text-sm">
            {[
              ["Opportunité",  decision.opportunity_score, "#06b6d4"],
              ["Préparation",  decision.readiness_score,   "#3b82f6"],
              ["Alignement",   decision.alignment_score,   "#8b5cf6"],
              ["Risque Timing",decision.risk_score,        "#ef4444"],
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
              <div className="text-white font-bold text-2xl">{decision.temporal_composite.toFixed(1)}</div>
            </div>
          </div>
        )}
        {tab==="signal" && (
          <div className="bg-slate-800 rounded-lg p-4 text-sm text-slate-200 leading-relaxed">
            {decision.timing_signal}
            <div className="mt-3 flex gap-2 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[decision.temporal_risk as keyof typeof RISK_BADGE]||"bg-slate-700 text-slate-300"}`}>{decision.temporal_risk}</span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[decision.timing_severity as keyof typeof SEV_BADGE]||"bg-slate-700 text-slate-300"}`}>{decision.timing_severity}</span>
            </div>
          </div>
        )}
        {tab==="action" && (
          <div className="space-y-3 text-sm">
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Action Recommandée</div>
              <div className="text-white font-medium">{decision.recommended_action.replace(/_/g," ")}</div>
            </div>
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Timing Loss Index</div>
              <div className="text-white font-bold">{decision.estimated_timing_loss_index.toFixed(2)} / 10</div>
            </div>
            <div className="flex gap-2">
              {decision.missed_window        && <span className="px-2 py-1 rounded bg-red-900 text-red-300 text-xs font-medium">FENÊTRE MANQUÉE</span>}
              {decision.acceleration_required && <span className="px-2 py-1 rounded bg-amber-900 text-amber-300 text-xs font-medium">ACCÉLÉRATION</span>}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function TemporalIntelligenceDashboard() {
  const [data, setData]         = useState<{ decisions: Decision[]; summary: Summary }|null>(null);
  const [filter, setFilter]     = useState<string>("all");
  const [patFilter, setPat]     = useState<string>("all");
  const [selected, setSelected] = useState<Decision|null>(null);

  useEffect(()=>{
    fetch("/api/temporal-intelligence-engine")
      .then(r=>r.json()).then(setData).catch(console.error);
  },[]);

  if (!data) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-cyan-400 text-lg animate-pulse">Loading Temporal Intelligence Engine...</div>
    </div>
  );

  const { decisions, summary } = data;
  const filtered = decisions.filter(d=>
    (filter==="all" || d.temporal_risk===filter) &&
    (patFilter==="all" || d.timing_pattern===patFilter)
  );

  const dists = [
    { title:"Risque Temporel",     counts:summary.risk_counts,     colors:RISK_COLORS },
    { title:"Pattern Timing",      counts:summary.pattern_counts,  colors:PAT_COLORS  },
    { title:"Sévérité Décision",   counts:summary.severity_counts, colors:SEV_COLORS  },
    { title:"Action Recommandée",  counts:summary.action_counts,   colors:ACT_COLORS  },
  ] as Array<{title:string;counts:Record<string,number>;colors:Record<string,string>}>;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {selected && <DetailModal decision={selected} onClose={()=>setSelected(null)}/>}

      <div>
        <h1 className="text-2xl font-bold text-white">Temporal Intelligence & Strategic Timing Optimization</h1>
        <p className="text-slate-400 text-sm mt-1">Fenêtres temporelles · Cycles marché · Timing réglementaire · Alignement géopolitique</p>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {[
          ["Total Décisions",        summary.total,                                                       "text-cyan-400"],
          ["Fenêtres Manquées",      summary.missed_window_count,                                         "text-red-400"],
          ["Accélérations Req.",     summary.acceleration_required_count,                                 "text-amber-400"],
          ["Composite Moyen",        summary.avg_temporal_composite,                                      "text-sky-400"],
          ["Opportunité Moyenne",    `${Math.round(summary.avg_opportunity_score)}`,                      "text-cyan-400"],
          ["Préparation",            `${Math.round(summary.avg_readiness_score)}`,                        "text-blue-400"],
        ].map(([l,v,c])=>(
          <div key={String(l)} className="bg-slate-900 border border-slate-800 rounded-xl p-3 text-center">
            <div className={`text-xl font-bold ${c}`}>{v}</div>
            <div className="text-xs text-slate-500 mt-0.5">{l}</div>
          </div>
        ))}
      </div>

      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
        <div className="grid grid-cols-4 gap-4">
          <Gauge value={summary.avg_opportunity_score} label="Opportunité Temporelle" color="#06b6d4"/>
          <Gauge value={summary.avg_readiness_score}   label="Préparation Exécution"  color="#3b82f6"/>
          <Gauge value={summary.avg_alignment_score}   label="Alignement Macro"       color="#8b5cf6"/>
          <Gauge value={summary.avg_risk_score}        label="Risque Timing"          color="#ef4444"/>
        </div>
      </div>

      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 grid grid-cols-1 md:grid-cols-2 gap-5">
        {dists.map(d=><DistBar key={d.title} {...d}/>)}
      </div>

      <div className="flex flex-wrap gap-2">
        {["all","low","moderate","high","critical"].map(r=>(
          <button key={r} onClick={()=>setFilter(r)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${filter===r?"bg-sky-700 border-sky-600 text-white":"bg-slate-900 border-slate-700 text-slate-400 hover:text-white"}`}>
            {r}
          </button>
        ))}
        <span className="w-px h-5 self-center bg-slate-700"/>
        {["all","timing_miss","window_collapse","premature_action","delayed_response","timing_conflict","none"].map(p=>(
          <button key={p} onClick={()=>setPat(p)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${patFilter===p?"bg-cyan-900 border-cyan-800 text-white":"bg-slate-900 border-slate-700 text-slate-400 hover:text-white"}`}>
            {p.replace(/_/g," ")}
          </button>
        ))}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {filtered.map(d=>(
          <div key={d.decision_id} onClick={()=>setSelected(d)}
            className="bg-slate-900 border border-slate-800 rounded-xl p-4 cursor-pointer hover:border-sky-700 transition-colors">
            <div className="flex items-center justify-between mb-1">
              <span className="font-bold text-white">{d.decision_id}</span>
              <span className="text-xs text-slate-400">{d.region}</span>
            </div>
            <div className="text-xs text-cyan-400 mb-2 capitalize">{d.decision_type.replace(/_/g," ")}</div>
            <div className="flex gap-1 mb-3 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[d.temporal_risk as keyof typeof RISK_BADGE]||"bg-slate-700 text-slate-300"}`}>{d.temporal_risk}</span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[d.timing_severity as keyof typeof SEV_BADGE]||"bg-slate-700 text-slate-300"}`}>{d.timing_severity}</span>
            </div>
            <div className="text-2xl font-black text-white mb-1">{d.temporal_composite.toFixed(1)}</div>
            <div className="text-xs text-slate-500 mb-2 capitalize">{d.timing_pattern.replace(/_/g," ")}</div>
            <div className="text-xs text-cyan-400 font-medium mb-2">Loss: {d.estimated_timing_loss_index.toFixed(2)}/10</div>
            <div className="flex gap-1 flex-wrap">
              {d.missed_window        && <span className="px-1.5 py-0.5 rounded bg-red-900 text-red-300 text-xs">MANQUÉE</span>}
              {d.acceleration_required && <span className="px-1.5 py-0.5 rounded bg-amber-900 text-amber-300 text-xs">ACCÉLER</span>}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
