"use client";
import { useEffect, useState } from "react";

type Culture = {
  microculture_id: string; cultural_cluster: string; region: string;
  cultural_risk: string; cultural_pattern: string;
  cultural_severity: string; recommended_action: string;
  cohesion_score: number; narrative_score: number;
  ritual_score: number; resilience_score: number;
  cultural_composite: number; has_fragmentation_alert: boolean;
  requires_intervention: boolean; estimated_culture_dissolution_index: number;
  cultural_signal: string;
};
type Summary = {
  total: number; risk_counts: Record<string,number>;
  pattern_counts: Record<string,number>; severity_counts: Record<string,number>;
  action_counts: Record<string,number>; avg_cultural_composite: number;
  fragmentation_alert_count: number; intervention_count: number;
  avg_cohesion_score: number; avg_narrative_score: number;
  avg_ritual_score: number; avg_resilience_score: number;
  avg_estimated_culture_dissolution_index: number;
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
const PAT_COLORS  = { none:"#10b981", tribal_fragmentation:"#ef4444", narrative_drift:"#f97316", ritual_erosion:"#f59e0b", generational_clash:"#a855f7", identity_crisis:"#ec4899" };
const SEV_COLORS  = { cohesive:"#10b981", drifting:"#f59e0b", fragmented:"#f97316", dissolved:"#ef4444" };
const ACT_COLORS  = { no_action:"#10b981", culture_pulse_monitoring:"#06b6d4", narrative_reinforcement:"#f97316", ritual_revival:"#f59e0b", generational_bridge_program:"#a855f7", tribe_mediation:"#ec4899", cultural_reset:"#dc2626", emergency_culture_intervention:"#7f1d1d" };
const RISK_BADGE  = { low:"bg-emerald-900 text-emerald-300", moderate:"bg-amber-900 text-amber-300", high:"bg-orange-900 text-orange-300", critical:"bg-red-900 text-red-300" };
const SEV_BADGE   = { cohesive:"bg-emerald-900 text-emerald-300", drifting:"bg-amber-900 text-amber-300", fragmented:"bg-orange-900 text-orange-300", dissolved:"bg-red-900 text-red-300" };

function DetailModal({ culture, onClose }: { culture: Culture; onClose: () => void }) {
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
            <span className="text-lg font-bold text-white">{culture.microculture_id}</span>
            <span className="ml-2 text-slate-400 text-sm capitalize">{culture.cultural_cluster.replace(/_/g," ")}</span>
            <span className="ml-2 text-purple-400 text-xs">{culture.region}</span>
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
              ["Cohésion",  culture.cohesion_score,  "#a855f7"],
              ["Narration", culture.narrative_score,  "#c026d3"],
              ["Rituels",   culture.ritual_score,     "#7c3aed"],
              ["Résilience",culture.resilience_score, "#9333ea"],
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
              <div className="text-slate-400 text-xs mb-1">Composite Culturel</div>
              <div className="text-white font-bold text-2xl">{culture.cultural_composite.toFixed(1)}</div>
            </div>
          </div>
        )}
        {tab==="signal" && (
          <div className="bg-slate-800 rounded-lg p-4 text-sm text-slate-200 leading-relaxed">
            {culture.cultural_signal}
            <div className="mt-3 flex gap-2 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[culture.cultural_risk as keyof typeof RISK_BADGE]||"bg-slate-700 text-slate-300"}`}>{culture.cultural_risk}</span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[culture.cultural_severity as keyof typeof SEV_BADGE]||"bg-slate-700 text-slate-300"}`}>{culture.cultural_severity}</span>
            </div>
          </div>
        )}
        {tab==="action" && (
          <div className="space-y-3 text-sm">
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Action Recommandée</div>
              <div className="text-white font-medium">{culture.recommended_action.replace(/_/g," ")}</div>
            </div>
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Indice Dissolution Culturelle</div>
              <div className="text-white font-bold">{culture.estimated_culture_dissolution_index.toFixed(2)} / 10</div>
            </div>
            <div className="flex gap-2">
              {culture.has_fragmentation_alert && <span className="px-2 py-1 rounded bg-red-900 text-red-300 text-xs font-medium">FRAGMENTATION</span>}
              {culture.requires_intervention   && <span className="px-2 py-1 rounded bg-orange-900 text-orange-300 text-xs font-medium">INTERVENTION</span>}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function CulturalChronologyDashboard() {
  const [data, setData]     = useState<{ cultures: Culture[]; summary: Summary }|null>(null);
  const [filter, setFilter] = useState<string>("all");
  const [patFilter, setPat] = useState<string>("all");
  const [selected, setSelected] = useState<Culture|null>(null);

  useEffect(()=>{
    fetch("/api/cultural-chronology-microculture-engine")
      .then(r=>r.json()).then(setData).catch(console.error);
  },[]);

  if (!data) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-purple-400 text-lg animate-pulse">Chargement Chronologie Culturelle...</div>
    </div>
  );

  const { cultures, summary } = data;
  const filtered = cultures.filter(c=>
    (filter==="all" || c.cultural_risk===filter) &&
    (patFilter==="all" || c.cultural_pattern===patFilter)
  );

  const dists = [
    { title:"Risque",   counts:summary.risk_counts,     colors:RISK_COLORS },
    { title:"Patron",   counts:summary.pattern_counts,  colors:PAT_COLORS  },
    { title:"Sévérité", counts:summary.severity_counts, colors:SEV_COLORS  },
    { title:"Action",   counts:summary.action_counts,   colors:ACT_COLORS  },
  ] as Array<{title:string;counts:Record<string,number>;colors:Record<string,string>}>;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {selected && <DetailModal culture={selected} onClose={()=>setSelected(null)}/>}

      <div>
        <h1 className="text-2xl font-bold text-white">Chronologie Culturelle &amp; Simulation Micro-Cultures</h1>
        <p className="text-slate-400 text-sm mt-1">Cohésion · Narration · Rituels · Résilience — simulation et anticipation des dynamiques culturelles organisationnelles</p>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {[
          ["Micro-Cultures",   summary.total,                                                           "text-purple-400"],
          ["Composite",        summary.avg_cultural_composite,                                          "text-fuchsia-400"],
          ["Alertes Fragm.",   summary.fragmentation_alert_count,                                       "text-red-400"],
          ["Interventions",    summary.intervention_count,                                              "text-orange-400"],
          ["Dissolution",      `${summary.avg_estimated_culture_dissolution_index.toFixed(1)}/10`,     "text-fuchsia-400"],
          ["Moy Cohésion",     `${Math.round(summary.avg_cohesion_score)}`,                            "text-purple-400"],
        ].map(([l,v,c])=>(
          <div key={String(l)} className="bg-slate-900 border border-slate-800 rounded-xl p-3 text-center">
            <div className={`text-xl font-bold ${c}`}>{v}</div>
            <div className="text-xs text-slate-500 mt-0.5">{l}</div>
          </div>
        ))}
      </div>

      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
        <div className="grid grid-cols-4 gap-4">
          <Gauge value={summary.avg_cohesion_score}   label="Cohésion"   color="#a855f7"/>
          <Gauge value={summary.avg_narrative_score}  label="Narration"  color="#c026d3"/>
          <Gauge value={summary.avg_ritual_score}     label="Rituels"    color="#7c3aed"/>
          <Gauge value={summary.avg_resilience_score} label="Résilience" color="#9333ea"/>
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
        {["all","none","tribal_fragmentation","narrative_drift","ritual_erosion","generational_clash","identity_crisis"].map(p=>(
          <button key={p} onClick={()=>setPat(p)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${patFilter===p?"bg-fuchsia-700 border-fuchsia-600 text-white":"bg-slate-900 border-slate-700 text-slate-400 hover:text-white hover:border-fuchsia-700"}`}>
            {p.replace(/_/g," ")}
          </button>
        ))}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {filtered.map(c=>(
          <div key={c.microculture_id} onClick={()=>setSelected(c)}
            className="bg-slate-900 border border-slate-800 rounded-xl p-4 cursor-pointer hover:border-fuchsia-700 transition-colors">
            <div className="flex items-center justify-between mb-1">
              <span className="font-bold text-white">{c.microculture_id}</span>
              <span className="text-xs text-slate-400">{c.region}</span>
            </div>
            <div className="text-xs text-purple-400 mb-2 capitalize">{c.cultural_cluster.replace(/_/g," ")}</div>
            <div className="flex gap-1 mb-3 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[c.cultural_risk as keyof typeof RISK_BADGE]||"bg-slate-700 text-slate-300"}`}>{c.cultural_risk}</span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[c.cultural_severity as keyof typeof SEV_BADGE]||"bg-slate-700 text-slate-300"}`}>{c.cultural_severity}</span>
            </div>
            <div className="text-2xl font-black text-white mb-1">{c.cultural_composite.toFixed(1)}</div>
            <div className="text-xs text-slate-500 mb-2 capitalize">{c.cultural_pattern.replace(/_/g," ")}</div>
            <div className="text-xs text-fuchsia-400 font-medium mb-2">Dissolution: {c.estimated_culture_dissolution_index.toFixed(2)}/10</div>
            <div className="flex gap-1 flex-wrap">
              {c.has_fragmentation_alert && <span className="px-1.5 py-0.5 rounded bg-red-900 text-red-300 text-xs">FRAGMENTATION</span>}
              {c.requires_intervention   && <span className="px-1.5 py-0.5 rounded bg-orange-900 text-orange-300 text-xs">INTERVENTION</span>}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
