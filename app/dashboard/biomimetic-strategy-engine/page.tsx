"use client";
import { useEffect, useState } from "react";

type Organism = {
  organism_id: string; strategy_archetype: string; region: string;
  biomimetic_risk: string; evolutionary_pattern: string;
  biomimetic_severity: string; recommended_action: string;
  fitness_score: number; adaptation_score: number;
  resilience_score: number; synergy_score: number;
  biomimetic_composite: number; has_extinction_signal: boolean;
  requires_evolutionary_intervention: boolean; estimated_extinction_risk_index: number;
  biomimetic_signal: string;
};
type Summary = {
  total: number; risk_counts: Record<string,number>;
  pattern_counts: Record<string,number>; severity_counts: Record<string,number>;
  action_counts: Record<string,number>; avg_biomimetic_composite: number;
  extinction_signal_count: number; evolutionary_intervention_count: number;
  avg_fitness_score: number; avg_adaptation_score: number;
  avg_resilience_score: number; avg_synergy_score: number;
  avg_estimated_extinction_risk_index: number;
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

const RISK_COLORS  = { low:"#10b981", moderate:"#14b8a6", high:"#f97316", critical:"#ef4444" };
const PAT_COLORS   = { none:"#10b981", extinction_spiral:"#ef4444", niche_collapse:"#dc2626", symbiosis_breakdown:"#f97316", evolutionary_stagnation:"#6b7280", territorial_loss:"#0d9488" };
const SEV_COLORS   = { thriving:"#10b981", adapting:"#14b8a6", endangered:"#f97316", extinct_risk:"#ef4444" };
const ACT_COLORS   = { no_action:"#10b981", evolution_monitoring:"#06b6d4", symbiosis_forge:"#2dd4bf", adaptation_acceleration:"#f97316", evolutionary_pivot:"#ef4444", niche_reconstruction:"#dc2626" };
const RISK_BADGE   = { low:"bg-emerald-900 text-emerald-300", moderate:"bg-teal-900 text-teal-300", high:"bg-orange-900 text-orange-300", critical:"bg-red-900 text-red-300" };
const SEV_BADGE    = { thriving:"bg-emerald-900 text-emerald-300", adapting:"bg-teal-900 text-teal-300", endangered:"bg-orange-900 text-orange-300", extinct_risk:"bg-red-900 text-red-300" };

function DetailModal({ organism, onClose }: { organism: Organism; onClose: () => void }) {
  const [tab, setTab] = useState<"scores"|"signal"|"action">("scores");
  useEffect(()=>{
    const h = (e: KeyboardEvent) => { if (e.key==="Escape") onClose(); };
    window.addEventListener("keydown", h);
    return ()=>window.removeEventListener("keydown",h);
  },[onClose]);
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70" onClick={onClose}>
      <div className="bg-slate-900 border border-teal-600/30 rounded-xl w-full max-w-lg p-6 shadow-2xl" onClick={e=>e.stopPropagation()}>
        <div className="flex items-center justify-between mb-4">
          <div>
            <span className="text-lg font-bold text-white">{organism.organism_id}</span>
            <span className="ml-2 text-slate-400 text-sm capitalize">{organism.strategy_archetype.replace(/_/g," ")}</span>
            <span className="ml-2 text-green-400 text-xs">{organism.region}</span>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl leading-none">✕</button>
        </div>
        <div className="flex gap-2 mb-4">
          {(["scores","signal","action"] as const).map(t=>(
            <button key={t} onClick={()=>setTab(t)}
              className={`px-3 py-1 rounded text-xs font-medium transition-colors ${tab===t?"bg-teal-700 text-white":"bg-slate-800 text-slate-400 hover:text-white"}`}>
              {t.charAt(0).toUpperCase()+t.slice(1)}
            </button>
          ))}
        </div>
        {tab==="scores" && (
          <div className="grid grid-cols-2 gap-3 text-sm">
            {[
              ["Fitness",     organism.fitness_score,     "#22c55e"],
              ["Adaptation",  organism.adaptation_score,  "#14b8a6"],
              ["Résilience",  organism.resilience_score,  "#0d9488"],
              ["Synergie",    organism.synergy_score,     "#10b981"],
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
              <div className="text-slate-400 text-xs mb-1">Composite Biomimétique</div>
              <div className="text-white font-bold text-2xl">{organism.biomimetic_composite.toFixed(1)}</div>
            </div>
          </div>
        )}
        {tab==="signal" && (
          <div className="bg-slate-800 rounded-lg p-4 text-sm text-slate-200 leading-relaxed">
            {organism.biomimetic_signal}
            <div className="mt-3 flex gap-2 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[organism.biomimetic_risk as keyof typeof RISK_BADGE]||"bg-slate-700 text-slate-300"}`}>{organism.biomimetic_risk}</span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[organism.biomimetic_severity as keyof typeof SEV_BADGE]||"bg-slate-700 text-slate-300"}`}>{organism.biomimetic_severity}</span>
            </div>
          </div>
        )}
        {tab==="action" && (
          <div className="space-y-3 text-sm">
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Action Recommandée</div>
              <div className="text-white font-medium">{organism.recommended_action.replace(/_/g," ")}</div>
            </div>
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Indice Risque Extinction</div>
              <div className="text-white font-bold">{organism.estimated_extinction_risk_index.toFixed(2)} / 10</div>
            </div>
            <div className="flex gap-2">
              {organism.has_extinction_signal              && <span className="px-2 py-1 rounded bg-red-900 text-red-300 text-xs font-medium">SIGNAL EXTINCTION</span>}
              {organism.requires_evolutionary_intervention && <span className="px-2 py-1 rounded bg-orange-900 text-orange-300 text-xs font-medium">INTERVENTION ÉVOL.</span>}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function BiomimeticStrategyDashboard() {
  const [data, setData]     = useState<{ organisms: Organism[]; summary: Summary }|null>(null);
  const [filter, setFilter] = useState<string>("all");
  const [patFilter, setPat] = useState<string>("all");
  const [selected, setSelected] = useState<Organism|null>(null);

  useEffect(()=>{
    fetch("/api/biomimetic-strategy-engine")
      .then(r=>r.json()).then(setData).catch(console.error);
  },[]);

  if (!data) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-green-400 text-lg animate-pulse">Chargement Moteur Stratégie Biomimétique...</div>
    </div>
  );

  const { organisms, summary } = data;
  const filtered = organisms.filter(o=>
    (filter==="all" || o.biomimetic_risk===filter) &&
    (patFilter==="all" || o.evolutionary_pattern===patFilter)
  );

  const dists = [
    { title:"Risque",   counts:summary.risk_counts,     colors:RISK_COLORS },
    { title:"Patron",   counts:summary.pattern_counts,  colors:PAT_COLORS  },
    { title:"Sévérité", counts:summary.severity_counts, colors:SEV_COLORS  },
    { title:"Action",   counts:summary.action_counts,   colors:ACT_COLORS  },
  ] as Array<{title:string;counts:Record<string,number>;colors:Record<string,string>}>;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {selected && <DetailModal organism={selected} onClose={()=>setSelected(null)}/>}

      <div>
        <h1 className="text-2xl font-bold text-white">Biomimétique &amp; Moteur d'Adaptation Évolutive</h1>
        <p className="text-slate-400 text-sm mt-1">Fitness · Adaptation · Résilience · Synergie — surveillance et optimisation de la stratégie biomimétique organisationnelle</p>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {[
          ["Organismes",       summary.total,                                                                    "text-green-400"],
          ["Composite",        summary.avg_biomimetic_composite,                                                 "text-teal-400"],
          ["Signaux Extinct.", summary.extinction_signal_count,                                                  "text-red-400"],
          ["Interventions",    summary.evolutionary_intervention_count,                                          "text-orange-400"],
          ["Risque Extinct.",  `${summary.avg_estimated_extinction_risk_index.toFixed(1)}/10`,                  "text-teal-400"],
          ["Moy Fitness",      `${Math.round(summary.avg_fitness_score)}`,                                      "text-green-400"],
        ].map(([l,v,c])=>(
          <div key={String(l)} className="bg-slate-900 border border-teal-600/30 rounded-xl p-3 text-center">
            <div className={`text-xl font-bold ${c}`}>{v}</div>
            <div className="text-xs text-slate-500 mt-0.5">{l}</div>
          </div>
        ))}
      </div>

      <div className="bg-slate-900 border border-teal-600/30 rounded-xl p-5">
        <div className="grid grid-cols-4 gap-4">
          <GaugeRing value={summary.avg_fitness_score}     label="Fitness"     color="#22c55e"/>
          <GaugeRing value={summary.avg_adaptation_score}  label="Adaptation"  color="#14b8a6"/>
          <GaugeRing value={summary.avg_resilience_score}  label="Résilience"  color="#0d9488"/>
          <GaugeRing value={summary.avg_synergy_score}     label="Synergie"    color="#10b981"/>
        </div>
      </div>

      <div className="bg-slate-900 border border-teal-600/30 rounded-xl p-5 grid grid-cols-1 md:grid-cols-2 gap-5">
        {dists.map(d=><DistBar key={d.title} {...d}/>)}
      </div>

      <div className="flex flex-wrap gap-2">
        {["all","low","moderate","high","critical"].map(r=>(
          <button key={r} onClick={()=>setFilter(r)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${filter===r?"bg-teal-700 border-teal-600 text-white":"bg-slate-900 border-slate-700 text-slate-400 hover:text-white"}`}>
            {r}
          </button>
        ))}
        <span className="w-px h-5 self-center bg-slate-700"/>
        {["all","none","extinction_spiral","niche_collapse","symbiosis_breakdown","evolutionary_stagnation","territorial_loss"].map(p=>(
          <button key={p} onClick={()=>setPat(p)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${patFilter===p?"bg-teal-700 border-teal-600 text-white":"bg-slate-900 border-slate-700 text-slate-400 hover:text-white hover:border-teal-600"}`}>
            {p.replace(/_/g," ")}
          </button>
        ))}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {filtered.map(o=>(
          <div key={o.organism_id} onClick={()=>setSelected(o)}
            className="bg-slate-900 border border-teal-600/30 rounded-xl p-4 cursor-pointer hover:border-teal-500 transition-colors">
            <div className="flex items-center justify-between mb-1">
              <span className="font-bold text-white">{o.organism_id}</span>
              <span className="text-xs text-slate-400">{o.region}</span>
            </div>
            <div className="text-xs text-green-400 mb-2 capitalize">{o.strategy_archetype.replace(/_/g," ")}</div>
            <div className="flex gap-1 mb-3 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[o.biomimetic_risk as keyof typeof RISK_BADGE]||"bg-slate-700 text-slate-300"}`}>{o.biomimetic_risk}</span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[o.biomimetic_severity as keyof typeof SEV_BADGE]||"bg-slate-700 text-slate-300"}`}>{o.biomimetic_severity}</span>
            </div>
            <div className="text-2xl font-black text-white mb-1">{o.biomimetic_composite.toFixed(1)}</div>
            <div className="text-xs text-slate-500 mb-2 capitalize">{o.evolutionary_pattern.replace(/_/g," ")}</div>
            <div className="text-xs text-teal-400 font-medium mb-2">Risque Extinct.: {o.estimated_extinction_risk_index.toFixed(2)}/10</div>
            <div className="flex gap-1 flex-wrap">
              {o.has_extinction_signal              && <span className="px-1.5 py-0.5 rounded bg-red-900 text-red-300 text-xs">SIGNAL EXTINCT.</span>}
              {o.requires_evolutionary_intervention && <span className="px-1.5 py-0.5 rounded bg-orange-900 text-orange-300 text-xs">INTERVENTION</span>}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
