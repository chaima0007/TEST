"use client";
import { useEffect, useState } from "react";

type Territory = {
  territory_id: string; territory_type: string; region: string;
  terraforming_risk: string; eco_pattern: string;
  terraforming_severity: string; recommended_action: string;
  ecosystem_score: number; climate_score: number;
  resource_score: number; resilience_score: number;
  terraforming_composite: number; has_ecological_alert: boolean;
  requires_emergency_action: boolean; estimated_ecological_risk_index: number;
  terraforming_signal: string;
};
type Summary = {
  total: number; risk_counts: Record<string,number>;
  pattern_counts: Record<string,number>; severity_counts: Record<string,number>;
  action_counts: Record<string,number>; avg_terraforming_composite: number;
  ecological_alert_count: number; emergency_action_count: number;
  avg_ecosystem_score: number; avg_climate_score: number;
  avg_resource_score: number; avg_resilience_score: number;
  avg_estimated_ecological_risk_index: number;
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
const PAT_COLORS  = { none:"#10b981", urban_heat_surge:"#ef4444", biodiversity_collapse:"#dc2626", soil_degradation:"#92400e", water_stress:"#3b82f6", carbon_debt:"#6b7280" };
const SEV_COLORS  = { regenerating:"#10b981", stable:"#f59e0b", degraded:"#f97316", critical:"#ef4444" };
const ACT_COLORS  = { no_action:"#10b981", eco_monitoring:"#06b6d4", green_corridor_activation:"#84cc16", soil_remediation:"#92400e", water_cycle_restoration:"#3b82f6", urban_cooling_deployment:"#f97316", biodiversity_reintroduction:"#a855f7", emergency_terraforming:"#dc2626", territory_quarantine:"#7f1d1d" };
const RISK_BADGE  = { low:"bg-emerald-900 text-emerald-300", moderate:"bg-amber-900 text-amber-300", high:"bg-orange-900 text-orange-300", critical:"bg-red-900 text-red-300" };
const SEV_BADGE   = { regenerating:"bg-emerald-900 text-emerald-300", stable:"bg-amber-900 text-amber-300", degraded:"bg-orange-900 text-orange-300", critical:"bg-red-900 text-red-300" };

function DetailModal({ territory, onClose }: { territory: Territory; onClose: () => void }) {
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
            <span className="text-lg font-bold text-white">{territory.territory_id}</span>
            <span className="ml-2 text-slate-400 text-sm capitalize">{territory.territory_type.replace(/_/g," ")}</span>
            <span className="ml-2 text-green-400 text-xs">{territory.region}</span>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl leading-none">✕</button>
        </div>
        <div className="flex gap-2 mb-4">
          {(["scores","signal","action"] as const).map(t=>(
            <button key={t} onClick={()=>setTab(t)}
              className={`px-3 py-1 rounded text-xs font-medium transition-colors ${tab===t?"bg-lime-700 text-white":"bg-slate-800 text-slate-400 hover:text-white"}`}>
              {t.charAt(0).toUpperCase()+t.slice(1)}
            </button>
          ))}
        </div>
        {tab==="scores" && (
          <div className="grid grid-cols-2 gap-3 text-sm">
            {[
              ["Écosystème", territory.ecosystem_score, "#22c55e"],
              ["Climat",     territory.climate_score,   "#84cc16"],
              ["Ressources", territory.resource_score,  "#65a30d"],
              ["Résilience", territory.resilience_score,"#16a34a"],
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
              <div className="text-slate-400 text-xs mb-1">Composite Terraformage</div>
              <div className="text-white font-bold text-2xl">{territory.terraforming_composite.toFixed(1)}</div>
            </div>
          </div>
        )}
        {tab==="signal" && (
          <div className="bg-slate-800 rounded-lg p-4 text-sm text-slate-200 leading-relaxed">
            {territory.terraforming_signal}
            <div className="mt-3 flex gap-2 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[territory.terraforming_risk as keyof typeof RISK_BADGE]||"bg-slate-700 text-slate-300"}`}>{territory.terraforming_risk}</span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[territory.terraforming_severity as keyof typeof SEV_BADGE]||"bg-slate-700 text-slate-300"}`}>{territory.terraforming_severity}</span>
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
              <div className="text-slate-400 text-xs mb-1">Indice Risque Écologique</div>
              <div className="text-white font-bold">{territory.estimated_ecological_risk_index.toFixed(2)} / 10</div>
            </div>
            <div className="flex gap-2">
              {territory.has_ecological_alert      && <span className="px-2 py-1 rounded bg-red-900 text-red-300 text-xs font-medium">ALERTE ÉCOL.</span>}
              {territory.requires_emergency_action && <span className="px-2 py-1 rounded bg-orange-900 text-orange-300 text-xs font-medium">URGENCE</span>}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function AnthropoceneDashboard() {
  const [data, setData]     = useState<{ territories: Territory[]; summary: Summary }|null>(null);
  const [filter, setFilter] = useState<string>("all");
  const [patFilter, setPat] = useState<string>("all");
  const [selected, setSelected] = useState<Territory|null>(null);

  useEffect(()=>{
    fetch("/api/anthropocene-terraforming-engine")
      .then(r=>r.json()).then(setData).catch(console.error);
  },[]);

  if (!data) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-green-400 text-lg animate-pulse">Chargement Terraformage Anthropocène...</div>
    </div>
  );

  const { territories, summary } = data;
  const filtered = territories.filter(t=>
    (filter==="all" || t.terraforming_risk===filter) &&
    (patFilter==="all" || t.eco_pattern===patFilter)
  );

  const dists = [
    { title:"Risque",   counts:summary.risk_counts,     colors:RISK_COLORS },
    { title:"Patron",   counts:summary.pattern_counts,  colors:PAT_COLORS  },
    { title:"Sévérité", counts:summary.severity_counts, colors:SEV_COLORS  },
    { title:"Action",   counts:summary.action_counts,   colors:ACT_COLORS  },
  ] as Array<{title:string;counts:Record<string,number>;colors:Record<string,string>}>;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {selected && <DetailModal territory={selected} onClose={()=>setSelected(null)}/>}

      <div>
        <h1 className="text-2xl font-bold text-white">Anthropocène &amp; Optimisation Terraformage Local</h1>
        <p className="text-slate-400 text-sm mt-1">Écosystème · Climat · Ressources · Résilience — surveillance et optimisation de l'empreinte territoriale anthropocène</p>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {[
          ["Territoires",      summary.total,                                                          "text-green-400"],
          ["Composite",        summary.avg_terraforming_composite,                                     "text-lime-400"],
          ["Alertes Écol.",    summary.ecological_alert_count,                                         "text-red-400"],
          ["Actions Urgentes", summary.emergency_action_count,                                         "text-orange-400"],
          ["Risque Écol.",     `${summary.avg_estimated_ecological_risk_index.toFixed(1)}/10`,        "text-lime-400"],
          ["Moy Écosystème",   `${Math.round(summary.avg_ecosystem_score)}`,                          "text-green-400"],
        ].map(([l,v,c])=>(
          <div key={String(l)} className="bg-slate-900 border border-slate-800 rounded-xl p-3 text-center">
            <div className={`text-xl font-bold ${c}`}>{v}</div>
            <div className="text-xs text-slate-500 mt-0.5">{l}</div>
          </div>
        ))}
      </div>

      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
        <div className="grid grid-cols-4 gap-4">
          <Gauge value={summary.avg_ecosystem_score} label="Écosystème" color="#22c55e"/>
          <Gauge value={summary.avg_climate_score}   label="Climat"     color="#84cc16"/>
          <Gauge value={summary.avg_resource_score}  label="Ressources" color="#65a30d"/>
          <Gauge value={summary.avg_resilience_score}label="Résilience" color="#16a34a"/>
        </div>
      </div>

      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 grid grid-cols-1 md:grid-cols-2 gap-5">
        {dists.map(d=><DistBar key={d.title} {...d}/>)}
      </div>

      <div className="flex flex-wrap gap-2">
        {["all","low","moderate","high","critical"].map(r=>(
          <button key={r} onClick={()=>setFilter(r)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${filter===r?"bg-lime-700 border-lime-600 text-white":"bg-slate-900 border-slate-700 text-slate-400 hover:text-white"}`}>
            {r}
          </button>
        ))}
        <span className="w-px h-5 self-center bg-slate-700"/>
        {["all","none","urban_heat_surge","biodiversity_collapse","soil_degradation","water_stress","carbon_debt"].map(p=>(
          <button key={p} onClick={()=>setPat(p)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${patFilter===p?"bg-lime-700 border-lime-600 text-white":"bg-slate-900 border-slate-700 text-slate-400 hover:text-white hover:border-lime-600"}`}>
            {p.replace(/_/g," ")}
          </button>
        ))}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {filtered.map(t=>(
          <div key={t.territory_id} onClick={()=>setSelected(t)}
            className="bg-slate-900 border border-slate-800 rounded-xl p-4 cursor-pointer hover:border-lime-600 transition-colors">
            <div className="flex items-center justify-between mb-1">
              <span className="font-bold text-white">{t.territory_id}</span>
              <span className="text-xs text-slate-400">{t.region}</span>
            </div>
            <div className="text-xs text-green-400 mb-2 capitalize">{t.territory_type.replace(/_/g," ")}</div>
            <div className="flex gap-1 mb-3 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[t.terraforming_risk as keyof typeof RISK_BADGE]||"bg-slate-700 text-slate-300"}`}>{t.terraforming_risk}</span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[t.terraforming_severity as keyof typeof SEV_BADGE]||"bg-slate-700 text-slate-300"}`}>{t.terraforming_severity}</span>
            </div>
            <div className="text-2xl font-black text-white mb-1">{t.terraforming_composite.toFixed(1)}</div>
            <div className="text-xs text-slate-500 mb-2 capitalize">{t.eco_pattern.replace(/_/g," ")}</div>
            <div className="text-xs text-lime-400 font-medium mb-2">Risque Écol.: {t.estimated_ecological_risk_index.toFixed(2)}/10</div>
            <div className="flex gap-1 flex-wrap">
              {t.has_ecological_alert      && <span className="px-1.5 py-0.5 rounded bg-red-900 text-red-300 text-xs">ALERTE ÉCOL.</span>}
              {t.requires_emergency_action && <span className="px-1.5 py-0.5 rounded bg-orange-900 text-orange-300 text-xs">URGENCE</span>}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
