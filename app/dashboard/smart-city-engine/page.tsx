"use client";
import { useEffect, useState } from "react";

type City = {
  entity_id: string; city_type: string; region: string;
  surveillance_score: number; control_score: number;
  vulnerability_score: number; sovereignty_score: number;
  composite_score: number; risk_level: string;
  total_surveillance_city: boolean; authoritarian_smart_city_export: boolean;
  private_tech_city_capture_pattern: boolean; predictive_policing_dystopia: boolean;
  IoT_city_cyber_catastrophe: boolean; patterns_detected: string[];
};
type Summary = {
  module_id: number; module_name: string;
  total: number; critical: number; high: number; moderate: number; low: number;
  avg_composite: number; distributions: Record<string,number>;
  avg_estimated_smart_city_surveillance_index: number;
  avg_surveillance_score: number; avg_control_score: number; avg_vulnerability_score: number;
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

const RISK_COLORS  = { low:"#10b981", moderate:"#f59e0b", high:"#f97316", critical:"#ef4444" };
const RISK_BADGE   = { low:"bg-emerald-900 text-emerald-300", moderate:"bg-amber-900 text-amber-300", high:"bg-orange-900 text-orange-300", critical:"bg-red-900 text-red-300" };
const PAT_LABELS: Record<string,string> = {
  total_surveillance_city:           "Ville Surveillance Totale",
  authoritarian_smart_city_export:   "Export Ville Autoritaire",
  private_tech_city_capture_pattern: "Capture Tech Privée",
  predictive_policing_dystopia:      "Policing Prédictif",
  IoT_city_cyber_catastrophe:        "Catastrophe Cyber IoT",
};

function DetailModal({ city, onClose }: { city: City; onClose: () => void }) {
  const [tab, setTab] = useState<"apercu"|"scores"|"patterns">("apercu");
  useEffect(()=>{
    const h = (e: KeyboardEvent) => { if (e.key==="Escape") onClose(); };
    window.addEventListener("keydown", h);
    return ()=>window.removeEventListener("keydown",h);
  },[onClose]);
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70" onClick={onClose}>
      <div className="bg-slate-900 border border-cyan-900 rounded-xl w-full max-w-lg p-6 shadow-2xl" onClick={e=>e.stopPropagation()}>
        <div className="flex items-center justify-between mb-4">
          <div>
            <span className="text-lg font-bold text-white">{city.entity_id}</span>
            <span className="ml-2 text-cyan-400 text-xs">{city.city_type}</span>
            <span className="ml-2 text-slate-400 text-xs">{city.region}</span>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl leading-none">✕</button>
        </div>
        <div className="flex gap-2 mb-4">
          {(["apercu","scores","patterns"] as const).map(t=>(
            <button key={t} onClick={()=>setTab(t)}
              className={`px-3 py-1 rounded text-xs font-medium transition-colors ${tab===t?"bg-cyan-700 text-white":"bg-slate-800 text-slate-400 hover:text-white"}`}>
              {t==="apercu"?"Aperçu":t==="scores"?"Scores":"Patterns"}
            </button>
          ))}
        </div>
        {tab==="apercu" && (
          <div className="space-y-3 text-sm">
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Niveau de Risque</div>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[city.risk_level as keyof typeof RISK_BADGE]||"bg-slate-700 text-slate-300"}`}>{city.risk_level.toUpperCase()}</span>
            </div>
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Score Composite</div>
              <div className="text-white font-bold text-2xl">{city.composite_score.toFixed(1)}</div>
              <div className="h-1.5 rounded mt-1 bg-slate-700">
                <div className="h-1.5 rounded" style={{width:`${Math.min(city.composite_score,100)}%`,background:RISK_COLORS[city.risk_level as keyof typeof RISK_COLORS]||"#06b6d4"}}/>
              </div>
            </div>
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Patterns Détectés</div>
              <div className="text-white font-medium">{city.patterns_detected.length > 0 ? city.patterns_detected.length : "Aucun"}</div>
            </div>
          </div>
        )}
        {tab==="scores" && (
          <div className="grid grid-cols-2 gap-3 text-sm">
            {([
              ["Surveillance", city.surveillance_score,  "#06b6d4"],
              ["Contrôle",     city.control_score,       "#ef4444"],
              ["Vulnérabilité",city.vulnerability_score, "#f97316"],
              ["Souveraineté", city.sovereignty_score,   "#a855f7"],
            ] as [string,number,string][]).map(([l,v,c])=>(
              <div key={l} className="bg-slate-800 rounded-lg p-3">
                <div className="text-slate-400 text-xs mb-1">{l}</div>
                <div className="text-white font-bold text-lg">{Number(v).toFixed(1)}</div>
                <div className="h-1.5 rounded mt-1 bg-slate-700">
                  <div className="h-1.5 rounded" style={{width:`${Math.min(Number(v),100)}%`,background:c}}/>
                </div>
              </div>
            ))}
            <div className="col-span-2 bg-slate-800 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Composite Urbain</div>
              <div className="text-white font-bold text-2xl">{city.composite_score.toFixed(1)}</div>
            </div>
          </div>
        )}
        {tab==="patterns" && (
          <div className="space-y-2 text-sm">
            {Object.entries(PAT_LABELS).map(([key, label])=>{
              const active = city[key as keyof City] as boolean;
              return (
                <div key={key} className={`rounded-lg p-3 flex items-center justify-between ${active?"bg-red-950 border border-red-800":"bg-slate-800"}`}>
                  <span className={`text-xs font-medium ${active?"text-red-300":"text-slate-400"}`}>{label}</span>
                  <span className={`px-2 py-0.5 rounded text-xs font-bold ${active?"bg-red-800 text-red-200":"bg-slate-700 text-slate-500"}`}>{active?"ACTIF":"—"}</span>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}

export default function SmartCityDashboard() {
  const [data, setData]         = useState<{ cities: City[]; summary: Summary }|null>(null);
  const [filter, setFilter]     = useState<string>("all");
  const [selected, setSelected] = useState<City|null>(null);

  useEffect(()=>{
    fetch("/api/smart-city-engine")
      .then(r=>r.json()).then(setData).catch(console.error);
  },[]);

  if (!data) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-cyan-400 text-lg animate-pulse">Chargement Module 388 — Ville Intelligente...</div>
    </div>
  );

  const { cities, summary } = data;
  const filtered = cities.filter(c => filter==="all" || c.risk_level===filter);
  const totalSurveillanceCount = cities.filter(c=>c.total_surveillance_city).length;

  const dists = [
    { title:"Niveau de Risque",         counts:summary.distributions,          colors:RISK_COLORS },
    { title:"Critique vs Élevé",        counts:{ critique: summary.critical, élevé: summary.high }, colors:{ critique:"#ef4444", élevé:"#f97316" } },
    { title:"Modéré vs Faible",         counts:{ modéré: summary.moderate, faible: summary.low }, colors:{ modéré:"#f59e0b", faible:"#10b981" } },
    { title:"Distribution Complète",    counts:{ critique: summary.critical, élevé: summary.high, modéré: summary.moderate, faible: summary.low }, colors:{ critique:"#ef4444", élevé:"#f97316", modéré:"#f59e0b", faible:"#10b981" } },
  ] as Array<{title:string;counts:Record<string,number>;colors:Record<string,string>}>;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {selected && <DetailModal city={selected} onClose={()=>setSelected(null)}/>}

      <div>
        <h1 className="text-2xl font-bold text-cyan-400">Ville Intelligente &amp; Surveillance Urbaine — Module 388</h1>
        <p className="text-slate-400 text-sm mt-1">Surveillance · Contrôle · Vulnérabilité IoT · Souveraineté des Données Urbaines</p>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {([
          ["Total Villes",             summary.total,                                              "text-cyan-400"],
          ["Surveillance Totale",      totalSurveillanceCount,                                     "text-red-400"],
          ["Crise Majeure",            summary.critical,                                           "text-red-500"],
          ["Composite Moyen",          summary.avg_composite,                                      "text-amber-300"],
          ["Index Surveillance Urbaine", summary.avg_estimated_smart_city_surveillance_index,     "text-cyan-300"],
          ["Surveillance Moyenne",     summary.avg_surveillance_score,                             "text-orange-400"],
        ] as [string,number,string][]).map(([l,v,c])=>(
          <div key={l} className="bg-slate-900 border border-cyan-900 rounded-xl p-3 text-center">
            <div className={`text-xl font-bold ${c}`}>{typeof v === "number" ? (Number.isInteger(v) ? v : v.toFixed(2)) : v}</div>
            <div className="text-xs text-slate-500 mt-0.5">{l}</div>
          </div>
        ))}
      </div>

      <div className="bg-slate-900 border border-cyan-900 rounded-xl p-5">
        <div className="grid grid-cols-4 gap-4">
          <GaugeRing value={summary.avg_surveillance_score}  label="Surveillance"  color="#06b6d4"/>
          <GaugeRing value={summary.avg_control_score}       label="Contrôle"      color="#ef4444"/>
          <GaugeRing value={summary.avg_vulnerability_score} label="Vulnérabilité" color="#f97316"/>
          <GaugeRing value={summary.avg_surveillance_score}  label="Souveraineté"  color="#a855f7"/>
        </div>
      </div>

      <div className="bg-slate-900 border border-cyan-900 rounded-xl p-5 grid grid-cols-1 md:grid-cols-2 gap-5">
        {dists.map(d=><DistBar key={d.title} {...d}/>)}
      </div>

      <div className="flex flex-wrap gap-2">
        {[
          { key:"all",      label:"Tous" },
          { key:"critical", label:"Critique" },
          { key:"high",     label:"Élevé" },
          { key:"moderate", label:"Modéré" },
          { key:"low",      label:"Faible" },
        ].map(({ key, label })=>(
          <button key={key} onClick={()=>setFilter(key)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${filter===key?"bg-cyan-700 border-cyan-600 text-white":"bg-slate-900 border-slate-700 text-slate-400 hover:text-white"}`}>
            {label}
          </button>
        ))}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {filtered.map(city=>(
          <div key={city.entity_id} onClick={()=>setSelected(city)}
            className="bg-slate-900 border border-slate-800 rounded-xl p-4 cursor-pointer hover:border-cyan-700 transition-colors">
            <div className="flex items-center justify-between mb-1">
              <span className="font-bold text-white">{city.entity_id}</span>
              <span className="text-xs text-slate-400">{city.region}</span>
            </div>
            <div className="text-xs text-cyan-400 mb-2 capitalize">{city.city_type.replace(/_/g," ")}</div>
            <div className="flex gap-1 mb-3 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[city.risk_level as keyof typeof RISK_BADGE]||"bg-slate-700 text-slate-300"}`}>{city.risk_level}</span>
            </div>
            <div className="text-2xl font-black text-white mb-1">{city.composite_score.toFixed(1)}</div>
            <div className="flex flex-wrap gap-1 mt-2">
              {city.patterns_detected.map(p=>(
                <span key={p} className="px-1.5 py-0.5 rounded bg-red-900 text-red-300 text-xs">{PAT_LABELS[p]||p}</span>
              ))}
              {city.patterns_detected.length===0 && <span className="text-xs text-slate-600">Aucun pattern</span>}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
