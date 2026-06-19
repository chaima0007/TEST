"use client";
import { useEffect, useState } from "react";

type Meme = {
  meme_id: string; meme_type: string; region: string;
  memetic_risk: string; memetic_pattern: string;
  memetic_severity: string; recommended_action: string;
  virality_score: number; resonance_score: number;
  persistence_score: number; reach_score: number;
  memetic_composite: number; is_epidemic_threat: boolean;
  requires_active_intervention: boolean;
  estimated_viral_disruption_index: number;
  memetic_signal: string;
};
type Summary = {
  total: number; risk_counts: Record<string,number>;
  pattern_counts: Record<string,number>; severity_counts: Record<string,number>;
  action_counts: Record<string,number>; avg_memetic_composite: number;
  epidemic_count: number; active_intervention_count: number;
  avg_virality_score: number; avg_resonance_score: number;
  avg_persistence_score: number; avg_reach_score: number;
  avg_estimated_viral_disruption_index: number;
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
const PAT_COLORS   = { none:"#10b981", viral_cascade:"#ef4444", echo_chamber_lock:"#dc2626", narrative_hijack:"#f97316", counter_meme_collapse:"#a855f7", belief_crystallization:"#ec4899" };
const SEV_COLORS   = { contained:"#10b981", seeding:"#f59e0b", spreading:"#f97316", epidemic:"#ef4444" };
const ACT_COLORS   = { no_action:"#10b981", meme_monitoring:"#06b6d4", narrative_steering:"#3b82f6", influence_mapping:"#f59e0b", crisis_narrative_reset:"#dc2626", counter_meme_injection:"#7f1d1d" };
const RISK_BADGE   = { low:"bg-emerald-900 text-emerald-300", moderate:"bg-amber-900 text-amber-300", high:"bg-orange-900 text-orange-300", critical:"bg-red-900 text-red-300" };
const SEV_BADGE    = { contained:"bg-emerald-900 text-emerald-300", seeding:"bg-amber-900 text-amber-300", spreading:"bg-orange-900 text-orange-300", epidemic:"bg-red-900 text-red-300" };

function DetailModal({ meme, onClose }: { meme: Meme; onClose: () => void }) {
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
            <span className="text-lg font-bold text-white">{meme.meme_id}</span>
            <span className="ml-2 text-orange-400 text-xs">{meme.meme_type}</span>
            <span className="ml-2 text-pink-400 text-xs">{meme.region}</span>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl leading-none">✕</button>
        </div>
        <div className="flex gap-2 mb-4">
          {(["scores","signal","action"] as const).map(t=>(
            <button key={t} onClick={()=>setTab(t)}
              className={`px-3 py-1 rounded text-xs font-medium transition-colors ${tab===t?"bg-orange-600 text-white":"bg-slate-800 text-slate-400 hover:text-white"}`}>
              {t.charAt(0).toUpperCase()+t.slice(1)}
            </button>
          ))}
        </div>
        {tab==="scores" && (
          <div className="grid grid-cols-2 gap-3 text-sm">
            {[
              ["Viralité",    meme.virality_score,     "#ef4444"],
              ["Résonance",   meme.resonance_score,    "#ec4899"],
              ["Persistance", meme.persistence_score,  "#f97316"],
              ["Portée",      meme.reach_score,        "#f59e0b"],
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
              <div className="text-slate-400 text-xs mb-1">Composite Mémetique</div>
              <div className="text-white font-bold text-2xl">{meme.memetic_composite.toFixed(1)}</div>
            </div>
          </div>
        )}
        {tab==="signal" && (
          <div className="bg-slate-800 rounded-lg p-4 text-sm text-slate-200 leading-relaxed">
            {meme.memetic_signal}
            <div className="mt-3 flex gap-2 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[meme.memetic_risk as keyof typeof RISK_BADGE]||"bg-slate-700 text-slate-300"}`}>{meme.memetic_risk}</span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[meme.memetic_severity as keyof typeof SEV_BADGE]||"bg-slate-700 text-slate-300"}`}>{meme.memetic_severity}</span>
            </div>
          </div>
        )}
        {tab==="action" && (
          <div className="space-y-3 text-sm">
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Action Recommandée</div>
              <div className="text-white font-medium">{meme.recommended_action.replace(/_/g," ")}</div>
            </div>
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Indice de Disruption Virale</div>
              <div className="text-white font-bold">{meme.estimated_viral_disruption_index.toFixed(2)} / 10</div>
            </div>
            <div className="flex gap-2">
              {meme.is_epidemic_threat           && <span className="px-2 py-1 rounded bg-red-900 text-red-300 text-xs font-medium">ÉPIDÉMIQUE</span>}
              {meme.requires_active_intervention && <span className="px-2 py-1 rounded bg-orange-900 text-orange-300 text-xs font-medium">INTERVENTION</span>}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function MemeticResonanceDashboard() {
  const [data, setData]         = useState<{ memes: Meme[]; summary: Summary }|null>(null);
  const [filter, setFilter]     = useState<string>("all");
  const [patFilter, setPat]     = useState<string>("all");
  const [selected, setSelected] = useState<Meme|null>(null);

  useEffect(()=>{
    fetch("/api/memetic-resonance-engine")
      .then(r=>r.json()).then(setData).catch(console.error);
  },[]);

  if (!data) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-orange-400 text-lg animate-pulse">Loading Memetic Resonance Engine...</div>
    </div>
  );

  const { memes, summary } = data;
  const filtered = memes.filter(m=>
    (filter==="all" || m.memetic_risk===filter) &&
    (patFilter==="all" || m.memetic_pattern===patFilter)
  );

  const dists = [
    { title:"Risque Propagation",  counts:summary.risk_counts,     colors:RISK_COLORS },
    { title:"Pattern Mémetique",   counts:summary.pattern_counts,  colors:PAT_COLORS  },
    { title:"Sévérité Narrative",  counts:summary.severity_counts, colors:SEV_COLORS  },
    { title:"Action Recommandée",  counts:summary.action_counts,   colors:ACT_COLORS  },
  ] as Array<{title:string;counts:Record<string,number>;colors:Record<string,string>}>;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {selected && <DetailModal meme={selected} onClose={()=>setSelected(null)}/>}

      <div>
        <h1 className="text-2xl font-bold text-white">Memetic Resonance & Viral Idea Propagation Engine</h1>
        <p className="text-slate-400 text-sm mt-1">Viralité · Résonance · Persistance · Portée — dynamiques de propagation des idées</p>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {[
          ["Total Mèmes",        summary.total,                                                          "text-orange-400"],
          ["Épidémiques",        summary.epidemic_count,                                                 "text-red-400"],
          ["Interventions Act.", summary.active_intervention_count,                                      "text-pink-400"],
          ["Composite Moyen",    summary.avg_memetic_composite,                                          "text-amber-400"],
          ["Viralité Moy.",      `${Math.round(summary.avg_virality_score)}`,                            "text-orange-300"],
          ["Résonance Moy.",     `${Math.round(summary.avg_resonance_score)}`,                           "text-pink-300"],
        ].map(([l,v,c])=>(
          <div key={String(l)} className="bg-slate-900 border border-slate-800 rounded-xl p-3 text-center">
            <div className={`text-xl font-bold ${c}`}>{v}</div>
            <div className="text-xs text-slate-500 mt-0.5">{l}</div>
          </div>
        ))}
      </div>

      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
        <div className="grid grid-cols-4 gap-4">
          <Gauge value={summary.avg_virality_score}     label="Vélocité Virale"     color="#ef4444"/>
          <Gauge value={summary.avg_resonance_score}    label="Résonance Mémetique" color="#ec4899"/>
          <Gauge value={summary.avg_persistence_score}  label="Persistance Narrative" color="#f97316"/>
          <Gauge value={summary.avg_reach_score}        label="Portée Réseau"       color="#f59e0b"/>
        </div>
      </div>

      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 grid grid-cols-1 md:grid-cols-2 gap-5">
        {dists.map(d=><DistBar key={d.title} {...d}/>)}
      </div>

      <div className="flex flex-wrap gap-2">
        {["all","low","moderate","high","critical"].map(r=>(
          <button key={r} onClick={()=>setFilter(r)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${filter===r?"bg-orange-600 border-orange-500 text-white":"bg-slate-900 border-slate-700 text-slate-400 hover:text-white"}`}>
            {r}
          </button>
        ))}
        <span className="w-px h-5 self-center bg-slate-700"/>
        {["all","viral_cascade","echo_chamber_lock","narrative_hijack","counter_meme_collapse","belief_crystallization","none"].map(p=>(
          <button key={p} onClick={()=>setPat(p)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${patFilter===p?"bg-pink-700 border-pink-600 text-white":"bg-slate-900 border-slate-700 text-slate-400 hover:text-white"}`}>
            {p.replace(/_/g," ")}
          </button>
        ))}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {filtered.map(m=>(
          <div key={m.meme_id} onClick={()=>setSelected(m)}
            className="bg-slate-900 border border-slate-800 rounded-xl p-4 cursor-pointer hover:border-orange-600 transition-colors">
            <div className="flex items-center justify-between mb-1">
              <span className="font-bold text-white">{m.meme_id}</span>
              <span className="text-xs text-slate-400">{m.region}</span>
            </div>
            <div className="text-xs text-pink-400 mb-2 truncate">{m.meme_type}</div>
            <div className="flex gap-1 mb-3 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[m.memetic_risk as keyof typeof RISK_BADGE]||"bg-slate-700 text-slate-300"}`}>{m.memetic_risk}</span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[m.memetic_severity as keyof typeof SEV_BADGE]||"bg-slate-700 text-slate-300"}`}>{m.memetic_severity}</span>
            </div>
            <div className="text-2xl font-black text-white mb-1">{m.memetic_composite.toFixed(1)}</div>
            <div className="text-xs text-slate-500 mb-2 capitalize">{m.memetic_pattern.replace(/_/g," ")}</div>
            <div className="text-xs text-orange-400 font-medium mb-2">Disruption: {m.estimated_viral_disruption_index.toFixed(2)}/10</div>
            <div className="flex gap-1 flex-wrap">
              {m.is_epidemic_threat           && <span className="px-1.5 py-0.5 rounded bg-red-900 text-red-300 text-xs">ÉPIDÉMIQUE</span>}
              {m.requires_active_intervention && <span className="px-1.5 py-0.5 rounded bg-orange-900 text-orange-300 text-xs">INTERVENTION</span>}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
