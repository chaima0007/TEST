"use client";
import { useEffect, useState } from "react";

type Territory = {
  territory_id: string; territory_type: string; region: string;
  geopolitical_risk: string; geopolitical_pattern: string;
  geopolitical_severity: string; recommended_action: string;
  stability_score: number; exposure_score: number;
  governance_score: number; sovereignty_score: number;
  geopolitical_composite: number; is_hostile_territory: boolean;
  requires_exit_plan: boolean; estimated_geopolitical_risk_index: number;
  geopolitical_signal: string;
};
type Summary = {
  total: number; risk_counts: Record<string,number>;
  pattern_counts: Record<string,number>; severity_counts: Record<string,number>;
  action_counts: Record<string,number>; avg_geopolitical_composite: number;
  hostile_count: number; exit_plan_count: number;
  avg_stability_score: number; avg_exposure_score: number;
  avg_governance_score: number; avg_sovereignty_score: number;
  avg_estimated_geopolitical_risk_index: number;
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

const RISK_COLORS   = { low:"#10b981", moderate:"#f59e0b", high:"#f97316", critical:"#ef4444" };
const PAT_COLORS    = { none:"#10b981", sanctions_cascade:"#ef4444", diplomatic_rupture:"#f97316", regulatory_decoupling:"#a855f7", conflict_spillover:"#dc2626", sovereignty_erosion:"#f59e0b" };
const SEV_COLORS    = { stable:"#10b981", cautious:"#f59e0b", tense:"#f97316", hostile:"#ef4444" };
const ACT_COLORS    = { no_action:"#10b981", geopolitical_monitoring:"#06b6d4", exposure_reduction:"#f97316", diplomatic_engagement:"#3b82f6", market_exit_plan:"#dc2626", emergency_hedging:"#7f1d1d" };
const RISK_BADGE    = { low:"bg-emerald-900 text-emerald-300", moderate:"bg-amber-900 text-amber-300", high:"bg-orange-900 text-orange-300", critical:"bg-red-900 text-red-300" };
const SEV_BADGE     = { stable:"bg-emerald-900 text-emerald-300", cautious:"bg-amber-900 text-amber-300", tense:"bg-orange-900 text-orange-300", hostile:"bg-red-900 text-red-300" };

function DetailModal({ territory, onClose }: { territory: Territory; onClose: () => void }) {
  const [tab, setTab] = useState<"scores"|"signal"|"action">("scores");
  useEffect(()=>{
    const h = (e: KeyboardEvent) => { if (e.key==="Escape") onClose(); };
    window.addEventListener("keydown", h);
    return ()=>window.removeEventListener("keydown",h);
  },[onClose]);
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70" onClick={onClose}>
      <div className="bg-slate-900 border border-red-900 rounded-xl w-full max-w-lg p-6 shadow-2xl" onClick={e=>e.stopPropagation()}>
        <div className="flex items-center justify-between mb-4">
          <div>
            <span className="text-lg font-bold text-white">{territory.territory_id}</span>
            <span className="ml-2 text-orange-400 text-xs">{territory.territory_type}</span>
            <span className="ml-2 text-amber-300 text-xs">{territory.region}</span>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl leading-none">✕</button>
        </div>
        <div className="flex gap-2 mb-4">
          {(["scores","signal","action"] as const).map(t=>(
            <button key={t} onClick={()=>setTab(t)}
              className={`px-3 py-1 rounded text-xs font-medium transition-colors ${tab===t?"bg-red-700 text-white":"bg-slate-800 text-slate-400 hover:text-white"}`}>
              {t.charAt(0).toUpperCase()+t.slice(1)}
            </button>
          ))}
        </div>
        {tab==="scores" && (
          <div className="grid grid-cols-2 gap-3 text-sm">
            {[
              ["Stabilité",    territory.stability_score,   "#ef4444"],
              ["Exposition",   territory.exposure_score,    "#f97316"],
              ["Gouvernance",  territory.governance_score,  "#a855f7"],
              ["Souveraineté", territory.sovereignty_score, "#f59e0b"],
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
              <div className="text-slate-400 text-xs mb-1">Composite Géopolitique</div>
              <div className="text-white font-bold text-2xl">{territory.geopolitical_composite.toFixed(1)}</div>
            </div>
          </div>
        )}
        {tab==="signal" && (
          <div className="bg-slate-800 rounded-lg p-4 text-sm text-slate-200 leading-relaxed">
            {territory.geopolitical_signal}
            <div className="mt-3 flex gap-2 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[territory.geopolitical_risk as keyof typeof RISK_BADGE]||"bg-slate-700 text-slate-300"}`}>{territory.geopolitical_risk}</span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[territory.geopolitical_severity as keyof typeof SEV_BADGE]||"bg-slate-700 text-slate-300"}`}>{territory.geopolitical_severity}</span>
            </div>
          </div>
        )}
        {tab==="action" && (
          <div className="space-y-3 text-sm">
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Action Recommandée</div>
              <div className="text-white font-medium">{territory.recommended_action.replace(/_/g," ")}</div>
            </div>
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Indice Risque Géopolitique</div>
              <div className="text-white font-bold">{territory.estimated_geopolitical_risk_index.toFixed(2)} / 10</div>
            </div>
            <div className="flex gap-2">
              {territory.is_hostile_territory && <span className="px-2 py-1 rounded bg-red-900 text-red-300 text-xs font-medium">HOSTILE</span>}
              {territory.requires_exit_plan    && <span className="px-2 py-1 rounded bg-orange-900 text-orange-300 text-xs font-medium">PLAN DE SORTIE</span>}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function GeopoliticalDashboard() {
  const [data, setData]         = useState<{ territories: Territory[]; summary: Summary }|null>(null);
  const [filter, setFilter]     = useState<string>("all");
  const [patFilter, setPat]     = useState<string>("all");
  const [selected, setSelected] = useState<Territory|null>(null);

  useEffect(()=>{
    fetch("/api/geopolitical-resilience-engine")
      .then(r=>r.json()).then(setData).catch(console.error);
  },[]);

  if (!data) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-orange-400 text-lg animate-pulse">Loading Geopolitical Engine...</div>
    </div>
  );

  const { territories, summary } = data;
  const filtered = territories.filter(t=>
    (filter==="all" || t.geopolitical_risk===filter) &&
    (patFilter==="all" || t.geopolitical_pattern===patFilter)
  );

  const dists = [
    { title:"Risque Géopolitique",   counts:summary.risk_counts,     colors:RISK_COLORS },
    { title:"Pattern Crise",         counts:summary.pattern_counts,  colors:PAT_COLORS  },
    { title:"Sévérité Territoire",   counts:summary.severity_counts, colors:SEV_COLORS  },
    { title:"Action Recommandée",    counts:summary.action_counts,   colors:ACT_COLORS  },
  ] as Array<{title:string;counts:Record<string,number>;colors:Record<string,string>}>;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {selected && <DetailModal territory={selected} onClose={()=>setSelected(null)}/>}

      <div>
        <h1 className="text-2xl font-bold text-red-700">Geopolitical Resilience & Diplomatic Risk</h1>
        <p className="text-orange-400 text-sm mt-1">Sanctions · Diplomatie · Gouvernance · Souveraineté — exposition géopolitique opérationnelle</p>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {[
          ["Total Territoires",      summary.total,                                                          "text-orange-400"],
          ["Hostiles",               summary.hostile_count,                                                  "text-red-400"],
          ["Plans de Sortie Actifs", summary.exit_plan_count,                                                "text-red-500"],
          ["Composite Moyen",        summary.avg_geopolitical_composite,                                     "text-amber-300"],
          ["Stabilité Politique",    `${Math.round(summary.avg_stability_score)}`,                           "text-orange-400"],
          ["Gouvernance",            `${Math.round(summary.avg_governance_score)}`,                          "text-amber-300"],
        ].map(([l,v,c])=>(
          <div key={String(l)} className="bg-slate-900 border border-red-900 rounded-xl p-3 text-center">
            <div className={`text-xl font-bold ${c}`}>{v}</div>
            <div className="text-xs text-slate-500 mt-0.5">{l}</div>
          </div>
        ))}
      </div>

      <div className="bg-slate-900 border border-red-900 rounded-xl p-5">
        <div className="grid grid-cols-4 gap-4">
          <Gauge value={summary.avg_stability_score}   label="Stabilité Politique"          color="#ef4444"/>
          <Gauge value={summary.avg_exposure_score}    label="Exposition Sanctions"          color="#f97316"/>
          <Gauge value={summary.avg_governance_score}  label="Gouvernance Institutionnelle"  color="#a855f7"/>
          <Gauge value={summary.avg_sovereignty_score} label="Souveraineté Stratégique"      color="#f59e0b"/>
        </div>
      </div>

      <div className="bg-slate-900 border border-red-900 rounded-xl p-5 grid grid-cols-1 md:grid-cols-2 gap-5">
        {dists.map(d=><DistBar key={d.title} {...d}/>)}
      </div>

      <div className="flex flex-wrap gap-2">
        {["all","low","moderate","high","critical"].map(r=>(
          <button key={r} onClick={()=>setFilter(r)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${filter===r?"bg-red-700 border-red-600 text-white":"bg-slate-900 border-slate-700 text-slate-400 hover:text-white"}`}>
            {r}
          </button>
        ))}
        <span className="w-px h-5 self-center bg-slate-700"/>
        {["all","sanctions_cascade","diplomatic_rupture","regulatory_decoupling","conflict_spillover","sovereignty_erosion","none"].map(p=>(
          <button key={p} onClick={()=>setPat(p)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${patFilter===p?"bg-orange-900 border-orange-800 text-white":"bg-slate-900 border-slate-700 text-slate-400 hover:text-white"}`}>
            {p.replace(/_/g," ")}
          </button>
        ))}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {filtered.map(t=>(
          <div key={t.territory_id} onClick={()=>setSelected(t)}
            className="bg-slate-900 border border-slate-800 rounded-xl p-4 cursor-pointer hover:border-red-700 transition-colors">
            <div className="flex items-center justify-between mb-1">
              <span className="font-bold text-white">{t.territory_id}</span>
              <span className="text-xs text-amber-300">{t.region}</span>
            </div>
            <div className="text-xs text-orange-400 mb-2 capitalize">{t.territory_type.replace(/_/g," ")}</div>
            <div className="flex gap-1 mb-3 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[t.geopolitical_risk as keyof typeof RISK_BADGE]||"bg-slate-700 text-slate-300"}`}>{t.geopolitical_risk}</span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[t.geopolitical_severity as keyof typeof SEV_BADGE]||"bg-slate-700 text-slate-300"}`}>{t.geopolitical_severity}</span>
            </div>
            <div className="text-2xl font-black text-white mb-1">{t.geopolitical_composite.toFixed(1)}</div>
            <div className="text-xs text-slate-500 mb-2 capitalize">{t.geopolitical_pattern.replace(/_/g," ")}</div>
            <div className="text-xs text-amber-300 font-medium mb-2">Risque: {t.estimated_geopolitical_risk_index.toFixed(2)}/10</div>
            <div className="flex gap-1 flex-wrap">
              {t.is_hostile_territory && <span className="px-1.5 py-0.5 rounded bg-red-900 text-red-300 text-xs">HOSTILE</span>}
              {t.requires_exit_plan   && <span className="px-1.5 py-0.5 rounded bg-orange-900 text-orange-300 text-xs">SORTIE</span>}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
