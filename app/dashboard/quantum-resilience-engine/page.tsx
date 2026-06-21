"use client";
import { useEffect, useState } from "react";

type Entity = {
  id: string; region: string; defense_layer: string;
  resilience_risk: string; resilience_pattern: string;
  resilience_severity: string; recommended_action: string;
  coherence_score: number; adaptation_score: number;
  neutralization_score: number; synchrony_score: number;
  resilience_composite: number; is_in_resilience_crisis: boolean;
  requires_immediate_reinforcement: boolean; resilience_signal: string;
};
type Summary = {
  total: number; risk_counts: Record<string,number>;
  pattern_counts: Record<string,number>; severity_counts: Record<string,number>;
  action_counts: Record<string,number>; avg_resilience_composite: number;
  resilience_crisis_count: number; immediate_reinforcement_count: number;
  avg_coherence_score: number; avg_adaptation_score: number;
  avg_neutralization_score: number; avg_synchrony_score: number;
  avg_estimated_resilience_index: number;
};

function GaugeRing({ value, label, color }: { value: number; label: string; color: string }) {
  const r = 36; const circ = 2 * Math.PI * r;
  const fill = circ * (1 - value / 100);
  return (
    <div className="flex flex-col items-center gap-1">
      <svg width="88" height="88" viewBox="0 0 88 88">
        <circle cx="44" cy="44" r={r} fill="none" stroke="#0a0520" strokeWidth="8"/>
        <circle cx="44" cy="44" r={r} fill="none" stroke={color} strokeWidth="8"
          strokeDasharray={circ} strokeDashoffset={fill}
          strokeLinecap="round" transform="rotate(-90 44 44)"/>
        <text x="44" y="49" textAnchor="middle" fill="white" fontSize="13" fontWeight="bold">
          {Math.round(value)}
        </text>
      </svg>
      <span className="text-xs text-purple-300/70 text-center">{label}</span>
    </div>
  );
}

function DistBar({ title, counts, colors }: { title: string; counts: Record<string,number>; colors: Record<string,string> }) {
  const total = Object.values(counts).reduce((a,b)=>a+b,0)||1;
  return (
    <div className="flex flex-col gap-1">
      <span className="text-xs text-purple-300/70 font-medium">{title}</span>
      <div className="flex h-3 rounded overflow-hidden gap-px">
        {Object.entries(counts).map(([k,v])=>(
          <div key={k} style={{width:`${v/total*100}%`, background:colors[k]||"#475569"}} title={`${k}: ${v}`}/>
        ))}
      </div>
      <div className="flex flex-wrap gap-x-3 gap-y-0.5">
        {Object.entries(counts).map(([k,v])=>(
          <span key={k} className="text-xs text-purple-300/60">
            <span style={{color:colors[k]||"#94a3b8"}}>■</span> {k.replace(/_/g," ")} {v}
          </span>
        ))}
      </div>
    </div>
  );
}

const RISK_COLORS    = { low:"#10b981", moderate:"#f59e0b", high:"#f97316", critical:"#a855f7" };
const PAT_COLORS     = {
  none:"#10b981", quantum_decoherence:"#7c3aed", adaptive_failure:"#f97316",
  cascade_collapse:"#dc2626", vulnerability_breach:"#f59e0b", immune_breakdown:"#06b6d4",
};
const SEV_COLORS     = { resilient:"#10b981", degrading:"#f59e0b", critical_stress:"#f97316", collapsed:"#7c3aed" };
const ACTION_COLORS  = {
  no_action:"#10b981", resilience_monitoring:"#06b6d4",
  decoherence_correction:"#f59e0b", adaptive_defense_protocol:"#f97316",
  quantum_reinforcement_emergency:"#7c3aed",
};

const RISK_BADGE  = {
  low:"bg-emerald-900 text-emerald-300", moderate:"bg-amber-900 text-amber-300",
  high:"bg-orange-900 text-orange-300",  critical:"bg-purple-950 text-purple-300",
};
const SEV_BADGE   = {
  resilient:"bg-emerald-900 text-emerald-300", degrading:"bg-amber-900 text-amber-300",
  critical_stress:"bg-orange-900 text-orange-300", collapsed:"bg-purple-950 text-purple-300",
};

function DetailModal({ entity, onClose }: { entity: Entity; onClose: () => void }) {
  const [tab, setTab] = useState<"scores"|"signal"|"action">("scores");
  useEffect(()=>{
    const h = (e: KeyboardEvent) => { if (e.key==="Escape") onClose(); };
    window.addEventListener("keydown", h);
    return ()=>window.removeEventListener("keydown", h);
  },[onClose]);
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80" onClick={onClose}>
      <div className="bg-slate-950 border border-cyan-600/30 rounded-xl w-full max-w-lg p-6 shadow-2xl" onClick={e=>e.stopPropagation()}>
        <div className="flex items-center justify-between mb-4">
          <div>
            <span className="text-lg font-bold text-white">{entity.id}</span>
            <span className="ml-2 text-purple-400 text-xs">{entity.region}</span>
            <span className="ml-2 text-slate-500 text-xs">{entity.defense_layer.replace(/_/g," ")}</span>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl leading-none">✕</button>
        </div>
        <div className="flex gap-2 mb-4">
          {(["scores","signal","action"] as const).map(t=>(
            <button key={t} onClick={()=>setTab(t)}
              className={`px-3 py-1 rounded text-xs font-medium transition-colors ${tab===t?"bg-purple-900 text-white":"bg-slate-900 text-slate-400 hover:text-white"}`}>
              {t.charAt(0).toUpperCase()+t.slice(1)}
            </button>
          ))}
        </div>
        {tab==="scores" && (
          <div className="grid grid-cols-2 gap-3 text-sm">
            {[
              ["Cohérence",      entity.coherence_score,      "#7c3aed"],
              ["Adaptation",     entity.adaptation_score,     "#f97316"],
              ["Neutralisation", entity.neutralization_score, "#f59e0b"],
              ["Synchronie",     entity.synchrony_score,      "#06b6d4"],
            ].map(([l,v,c])=>(
              <div key={String(l)} className="bg-slate-900 border border-cyan-600/20 rounded-lg p-3">
                <div className="text-purple-300/60 text-xs mb-1">{String(l)}</div>
                <div className="text-white font-bold text-lg">{Number(v).toFixed(1)}</div>
                <div className="h-1.5 rounded mt-1 bg-slate-800">
                  <div className="h-1.5 rounded" style={{width:`${Math.min(Number(v),100)}%`,background:String(c)}}/>
                </div>
              </div>
            ))}
            <div className="col-span-2 bg-slate-900 border border-cyan-600/20 rounded-lg p-3">
              <div className="text-purple-300/60 text-xs mb-1">Composite Résilience</div>
              <div className="text-white font-bold text-2xl">{entity.resilience_composite.toFixed(1)}</div>
            </div>
          </div>
        )}
        {tab==="signal" && (
          <div className="bg-slate-900 border border-cyan-600/20 rounded-lg p-4 text-sm text-slate-200 leading-relaxed">
            {entity.resilience_signal}
            <div className="mt-3 flex gap-2 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[entity.resilience_risk as keyof typeof RISK_BADGE]||"bg-slate-700 text-slate-300"}`}>{entity.resilience_risk}</span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[entity.resilience_severity as keyof typeof SEV_BADGE]||"bg-slate-700 text-slate-300"}`}>{entity.resilience_severity.replace(/_/g," ")}</span>
            </div>
          </div>
        )}
        {tab==="action" && (
          <div className="space-y-3 text-sm">
            <div className="bg-slate-900 border border-cyan-600/20 rounded-lg p-3">
              <div className="text-purple-300/60 text-xs mb-1">Action Recommandée</div>
              <div className="text-white font-medium">{entity.recommended_action.replace(/_/g," ")}</div>
            </div>
            <div className="bg-slate-900 border border-cyan-600/20 rounded-lg p-3">
              <div className="text-purple-300/60 text-xs mb-1">Patron de Résilience</div>
              <div className="text-white font-medium">{entity.resilience_pattern.replace(/_/g," ")}</div>
            </div>
            <div className="flex gap-2 flex-wrap">
              {entity.is_in_resilience_crisis && (
                <span className="px-2 py-1 rounded bg-purple-950 text-purple-300 text-xs font-medium">CRISE RÉSILIENCE</span>
              )}
              {entity.requires_immediate_reinforcement && (
                <span className="px-2 py-1 rounded bg-cyan-950 text-cyan-400 text-xs font-medium">RENFORCEMENT REQ.</span>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function QuantumResilienceDashboard() {
  const [data, setData]         = useState<{ entities: Entity[]; summary: Summary }|null>(null);
  const [filter, setFilter]     = useState<string>("all");
  const [patFilter, setPat]     = useState<string>("all");
  const [selected, setSelected] = useState<Entity|null>(null);

  useEffect(()=>{
    fetch("/api/quantum-resilience-engine")
      .then(r=>r.json()).then(setData).catch(console.error);
  },[]);

  if (!data) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-purple-400 text-lg animate-pulse">Initialisation du Moteur Résilience Quantique...</div>
    </div>
  );

  const { entities, summary } = data;
  const filtered = entities.filter(e=>
    (filter==="all" || e.resilience_risk===filter) &&
    (patFilter==="all" || e.resilience_pattern===patFilter)
  );

  const dists = [
    { title:"Niveau Risque",         counts:summary.risk_counts,     colors:RISK_COLORS   },
    { title:"Patron Résilience",     counts:summary.pattern_counts,  colors:PAT_COLORS    },
    { title:"Sévérité Défensive",    counts:summary.severity_counts, colors:SEV_COLORS    },
    { title:"Action Déclenchée",     counts:summary.action_counts,   colors:ACTION_COLORS },
  ] as Array<{title:string;counts:Record<string,number>;colors:Record<string,string>}>;

  const criticalCount = summary.risk_counts["critical"] || 0;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {selected && <DetailModal entity={selected} onClose={()=>setSelected(null)}/>}

      <div>
        <h1 className="text-2xl font-bold text-purple-400">Quantum Resilience & Adaptive Defense Engine</h1>
        <p className="text-purple-300/50 text-sm mt-1">Cohérence · Adaptation · Neutralisation · Synchronie Inter-Couches</p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {[
          ["Entités Analysées",                summary.total,                                 "text-purple-400"],
          ["Crises Critiques",                 criticalCount,                                 "text-purple-500"],
          ["Composite Résilience Moy.",        `${summary.avg_resilience_composite.toFixed(1)}`, "text-cyan-400"],
          ["Indice Résilience Estimé",         `${summary.avg_estimated_resilience_index.toFixed(2)}/10`, "text-amber-400"],
          ["En Crise de Résilience",           summary.resilience_crisis_count,               "text-purple-400"],
          ["Renforcement Immédiat Req.",        summary.immediate_reinforcement_count,          "text-cyan-500"],
        ].map(([l,v,c])=>(
          <div key={String(l)} className="bg-slate-900 border border-cyan-600/30 rounded-xl p-3 text-center">
            <div className={`text-xl font-bold ${c}`}>{v}</div>
            <div className="text-xs text-purple-300/40 mt-0.5 leading-tight">{l}</div>
          </div>
        ))}
      </div>

      {/* Gauge Rings */}
      <div className="bg-slate-900 border border-cyan-600/30 rounded-xl p-5">
        <div className="grid grid-cols-4 gap-4">
          <GaugeRing value={summary.avg_coherence_score}      label="Cohérence Quantique"     color="#7c3aed"/>
          <GaugeRing value={summary.avg_adaptation_score}     label="Capacité Adaptative"     color="#f97316"/>
          <GaugeRing value={summary.avg_neutralization_score} label="Neutralisation Menaces"  color="#f59e0b"/>
          <GaugeRing value={summary.avg_synchrony_score}      label="Synchronie Inter-Couches" color="#06b6d4"/>
        </div>
      </div>

      {/* Distribution Bars */}
      <div className="bg-slate-900 border border-cyan-600/30 rounded-xl p-5 grid grid-cols-1 md:grid-cols-2 gap-5">
        {dists.map(d=><DistBar key={d.title} {...d}/>)}
      </div>

      {/* Filter Pills */}
      <div className="flex flex-wrap gap-2">
        {["all","low","moderate","high","critical"].map(r=>(
          <button key={r} onClick={()=>setFilter(r)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${filter===r?"bg-purple-900 border-purple-700 text-white":"bg-slate-900 border-cyan-600/30 text-purple-400/70 hover:text-white"}`}>
            {r}
          </button>
        ))}
        <span className="w-px h-5 self-center bg-cyan-600/30"/>
        {["all","none","quantum_decoherence","adaptive_failure","cascade_collapse","vulnerability_breach","immune_breakdown"].map(p=>(
          <button key={p} onClick={()=>setPat(p)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${patFilter===p?"bg-purple-950 border-purple-800 text-white":"bg-slate-900 border-cyan-600/30 text-purple-400/70 hover:text-white"}`}>
            {p.replace(/_/g," ")}
          </button>
        ))}
      </div>

      {/* Entity Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {filtered.map(e=>(
          <div key={e.id} onClick={()=>setSelected(e)}
            className="bg-slate-900 border border-cyan-600/30 rounded-xl p-4 cursor-pointer hover:border-purple-600 transition-colors">
            <div className="flex items-center justify-between mb-1">
              <span className="font-bold text-white">{e.id}</span>
              <span className="text-xs text-purple-400/60">{e.region}</span>
            </div>
            <div className="text-xs text-slate-500 mb-2 capitalize">{e.defense_layer.replace(/_/g," ")}</div>
            <div className="flex gap-1 mb-3 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[e.resilience_risk as keyof typeof RISK_BADGE]||"bg-slate-700 text-slate-300"}`}>{e.resilience_risk}</span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[e.resilience_severity as keyof typeof SEV_BADGE]||"bg-slate-700 text-slate-300"}`}>{e.resilience_severity.replace(/_/g," ")}</span>
            </div>
            <div className="text-2xl font-black text-white mb-1">{e.resilience_composite.toFixed(1)}</div>
            <div className="text-xs text-purple-400/60 mb-2 capitalize">{e.resilience_pattern.replace(/_/g," ")}</div>
            <div className="text-xs text-cyan-400 font-medium mb-2">{e.recommended_action.replace(/_/g," ")}</div>
            <div className="flex gap-1 flex-wrap">
              {e.is_in_resilience_crisis && (
                <span className="px-1.5 py-0.5 rounded bg-purple-950 text-purple-300 text-xs">CRISE</span>
              )}
              {e.requires_immediate_reinforcement && (
                <span className="px-1.5 py-0.5 rounded bg-cyan-950 text-cyan-400 text-xs">RENFORCEMENT</span>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
