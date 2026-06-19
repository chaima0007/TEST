"use client";
import { useEffect, useState } from "react";

type DataAsset = {
  asset_id: string; data_domain: string; region: string;
  dark_data_risk: string; dark_data_pattern: string;
  dark_data_severity: string; recommended_action: string;
  governance_score: number; discovery_score: number;
  quality_score: number; value_score: number;
  dark_data_composite: number;
  has_hidden_value_signal: boolean;
  requires_immediate_governance: boolean;
  estimated_hidden_value_index: number;
  dark_data_signal: string;
};
type Summary = {
  total: number; risk_counts: Record<string,number>;
  pattern_counts: Record<string,number>; severity_counts: Record<string,number>;
  action_counts: Record<string,number>; avg_dark_data_composite: number;
  hidden_value_signal_count: number; immediate_governance_count: number;
  avg_governance_score: number; avg_discovery_score: number;
  avg_quality_score: number; avg_value_score: number;
  avg_estimated_hidden_value_index: number;
};

function GaugeRing({ value, label, color }: { value: number; label: string; color: string }) {
  const r = 36; const circ = 2 * Math.PI * r;
  const fill = circ * (1 - value / 100);
  return (
    <div className="flex flex-col items-center gap-1">
      <svg width="88" height="88" viewBox="0 0 88 88">
        <circle cx="44" cy="44" r={r} fill="none" stroke="#1e1b4b" strokeWidth="8"/>
        <circle cx="44" cy="44" r={r} fill="none" stroke={color} strokeWidth="8"
          strokeDasharray={circ} strokeDashoffset={fill}
          strokeLinecap="round" transform="rotate(-90 44 44)"/>
        <text x="44" y="49" textAnchor="middle" fill="white" fontSize="13" fontWeight="bold">
          {Math.round(value)}
        </text>
      </svg>
      <span className="text-xs text-violet-200/70 text-center">{label}</span>
    </div>
  );
}

function DistBar({ title, counts, colors }: { title: string; counts: Record<string,number>; colors: Record<string,string> }) {
  const total = Object.values(counts).reduce((a,b)=>a+b,0)||1;
  return (
    <div className="flex flex-col gap-1">
      <span className="text-xs text-violet-200/70 font-medium">{title}</span>
      <div className="flex h-3 rounded overflow-hidden gap-px">
        {Object.entries(counts).map(([k,v])=>(
          <div key={k} style={{width:`${v/total*100}%`, background:colors[k]||"#6b7280"}} title={`${k}: ${v}`}/>
        ))}
      </div>
      <div className="flex flex-wrap gap-x-3 gap-y-0.5">
        {Object.entries(counts).map(([k,v])=>(
          <span key={k} className="text-xs text-violet-200/60">
            <span style={{color:colors[k]||"#9ca3af"}}>■</span> {k} {v}
          </span>
        ))}
      </div>
    </div>
  );
}

const RISK_COLORS    = { low:"#10b981", moderate:"#f59e0b", high:"#f97316", critical:"#ef4444" };
const PAT_COLORS     = { none:"#10b981", governance_blindspot:"#ef4444", value_burial:"#a855f7", silo_fragmentation:"#f97316", compliance_exposure:"#dc2626", data_rot:"#ec4899" };
const SEV_COLORS     = { illuminated:"#10b981", emerging:"#f59e0b", obscured:"#f97316", critical_exposure:"#ef4444" };
const ACT_COLORS     = { no_action:"#10b981", data_monitoring:"#06b6d4", dark_data_excavation:"#a855f7", silo_bridge:"#f59e0b", privacy_audit:"#f97316", data_governance_emergency:"#ef4444" };
const RISK_BADGE     = { low:"bg-emerald-900 text-emerald-300", moderate:"bg-amber-900 text-amber-300", high:"bg-orange-900 text-orange-300", critical:"bg-red-900 text-red-300" };
const SEV_BADGE      = { illuminated:"bg-emerald-900 text-emerald-300", emerging:"bg-amber-900 text-amber-300", obscured:"bg-orange-900 text-orange-300", critical_exposure:"bg-red-900 text-red-300" };

function DetailModal({ asset, onClose }: { asset: DataAsset; onClose: () => void }) {
  const [tab, setTab] = useState<"scores"|"signal"|"action">("scores");
  useEffect(()=>{
    const h = (e: KeyboardEvent) => { if (e.key==="Escape") onClose(); };
    window.addEventListener("keydown", h);
    return ()=>window.removeEventListener("keydown",h);
  },[onClose]);
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70" onClick={onClose}>
      <div className="bg-slate-900 border border-purple-600/30 rounded-xl w-full max-w-lg p-6 shadow-2xl" onClick={e=>e.stopPropagation()}>
        <div className="flex items-center justify-between mb-4">
          <div>
            <span className="text-lg font-bold text-white">{asset.asset_id}</span>
            <span className="ml-2 text-violet-400 text-xs">{asset.region}</span>
            <span className="ml-2 text-purple-400 text-xs capitalize">{asset.data_domain.replace(/_/g," ")}</span>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl leading-none">✕</button>
        </div>
        <div className="flex gap-2 mb-4">
          {(["scores","signal","action"] as const).map(t=>(
            <button key={t} onClick={()=>setTab(t)}
              className={`px-3 py-1 rounded text-xs font-medium transition-colors ${tab===t?"bg-violet-700 text-white":"bg-slate-800 text-slate-400 hover:text-white"}`}>
              {t.charAt(0).toUpperCase()+t.slice(1)}
            </button>
          ))}
        </div>
        {tab==="scores" && (
          <div className="grid grid-cols-2 gap-3 text-sm">
            {[
              ["Score Gouvernance",  asset.governance_score,  "#a855f7"],
              ["Score Découverte",   asset.discovery_score,   "#f97316"],
              ["Score Qualité",      asset.quality_score,     "#f59e0b"],
              ["Score Valeur",       asset.value_score,       "#ec4899"],
            ].map(([l,v,c])=>(
              <div key={String(l)} className="bg-slate-800 rounded-lg p-3">
                <div className="text-violet-200/60 text-xs mb-1">{String(l)}</div>
                <div className="text-white font-bold text-lg">{Number(v).toFixed(1)}</div>
                <div className="h-1.5 rounded mt-1 bg-slate-700">
                  <div className="h-1.5 rounded" style={{width:`${Math.min(Number(v),100)}%`,background:String(c)}}/>
                </div>
              </div>
            ))}
            <div className="col-span-2 bg-slate-800 rounded-lg p-3">
              <div className="text-violet-200/60 text-xs mb-1">Composite Données Sombres</div>
              <div className="text-white font-bold text-2xl">{asset.dark_data_composite.toFixed(1)}</div>
            </div>
          </div>
        )}
        {tab==="signal" && (
          <div className="bg-slate-800 rounded-lg p-4 text-sm text-slate-200 leading-relaxed">
            {asset.dark_data_signal}
            <div className="mt-3 flex gap-2 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[asset.dark_data_risk as keyof typeof RISK_BADGE]||"bg-slate-700 text-slate-300"}`}>{asset.dark_data_risk}</span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[asset.dark_data_severity as keyof typeof SEV_BADGE]||"bg-slate-700 text-slate-300"}`}>{asset.dark_data_severity}</span>
            </div>
          </div>
        )}
        {tab==="action" && (
          <div className="space-y-3 text-sm">
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-violet-200/60 text-xs mb-1">Action Recommandée</div>
              <div className="text-white font-medium capitalize">{asset.recommended_action.replace(/_/g," ")}</div>
            </div>
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-violet-200/60 text-xs mb-1">Indice de Valeur Cachée</div>
              <div className="text-white font-bold">{asset.estimated_hidden_value_index.toFixed(2)} / 10</div>
            </div>
            <div className="flex gap-2 flex-wrap">
              {asset.has_hidden_value_signal && <span className="px-2 py-1 rounded bg-purple-900 text-purple-300 text-xs font-medium">VALEUR CACHÉE</span>}
              {asset.requires_immediate_governance && <span className="px-2 py-1 rounded bg-red-900 text-red-300 text-xs font-medium">GOUVERNANCE URGENTE</span>}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function DarkDataIntelligenceDashboard() {
  const [data, setData]         = useState<{ assets: DataAsset[]; summary: Summary }|null>(null);
  const [filter, setFilter]     = useState<string>("all");
  const [patFilter, setPat]     = useState<string>("all");
  const [selected, setSelected] = useState<DataAsset|null>(null);

  useEffect(()=>{
    fetch("/api/dark-data-intelligence-engine")
      .then(r=>r.json()).then(setData).catch(console.error);
  },[]);

  if (!data) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-violet-400 text-lg animate-pulse">Chargement du moteur de données sombres...</div>
    </div>
  );

  const { assets, summary } = data;
  const filtered = assets.filter(a=>
    (filter==="all" || a.dark_data_risk===filter) &&
    (patFilter==="all" || a.dark_data_pattern===patFilter)
  );

  const dists = [
    { title:"Risque Données Sombres", counts:summary.risk_counts,     colors:RISK_COLORS },
    { title:"Pattern Détecté",        counts:summary.pattern_counts,   colors:PAT_COLORS  },
    { title:"Sévérité Actif",         counts:summary.severity_counts,  colors:SEV_COLORS  },
    { title:"Action Recommandée",     counts:summary.action_counts,    colors:ACT_COLORS  },
  ] as Array<{title:string;counts:Record<string,number>;colors:Record<string,string>}>;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {selected && <DetailModal asset={selected} onClose={()=>setSelected(null)}/>}

      <div>
        <h1 className="text-2xl font-bold text-violet-400">Intelligence Données Sombres & Découverte d&apos;Actifs Cachés</h1>
        <p className="text-violet-200/60 text-sm mt-1">Gouvernance · Découverte · Qualité · Valeur — Caelum Partners</p>
      </div>

      {/* 6 KPI cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {[
          ["Total Actifs",          summary.total,                                            "text-violet-400"],
          ["Signaux Valeur Cachée", summary.hidden_value_signal_count,                        "text-purple-400"],
          ["Gouvernance Urgente",   summary.immediate_governance_count,                       "text-red-400"],
          ["Composite Moyen",       summary.avg_dark_data_composite,                          "text-violet-300"],
          ["Indice Valeur Cachée",  summary.avg_estimated_hidden_value_index.toFixed(2),      "text-violet-400"],
          ["Score Gouvernance Moy", `${Math.round(summary.avg_governance_score)}`,            "text-purple-400"],
        ].map(([l,v,c])=>(
          <div key={String(l)} className="bg-slate-900 border border-purple-600/30 rounded-xl p-3 text-center">
            <div className={`text-xl font-bold ${c}`}>{v}</div>
            <div className="text-xs text-violet-200/50 mt-0.5">{l}</div>
          </div>
        ))}
      </div>

      {/* 4 GaugeRings */}
      <div className="bg-slate-900 border border-purple-600/30 rounded-xl p-5">
        <div className="grid grid-cols-4 gap-4">
          <GaugeRing value={summary.avg_governance_score} label="Risque Gouvernance"  color="#a855f7"/>
          <GaugeRing value={summary.avg_discovery_score}  label="Opacité Découverte"  color="#f97316"/>
          <GaugeRing value={summary.avg_quality_score}    label="Dégradation Qualité" color="#f59e0b"/>
          <GaugeRing value={summary.avg_value_score}      label="Enfouissement Valeur" color="#ec4899"/>
        </div>
      </div>

      {/* 4 DistBars */}
      <div className="bg-slate-900 border border-purple-600/30 rounded-xl p-5 grid grid-cols-1 md:grid-cols-2 gap-5">
        {dists.map(d=><DistBar key={d.title} {...d}/>)}
      </div>

      {/* Filter pills */}
      <div className="flex flex-wrap gap-2">
        {["all","low","moderate","high","critical"].map(r=>(
          <button key={r} onClick={()=>setFilter(r)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${filter===r?"bg-violet-700 border-violet-600 text-white":"bg-slate-900 border-purple-600/30 text-violet-200/60 hover:text-white"}`}>
            {r}
          </button>
        ))}
        <span className="w-px h-5 self-center bg-purple-600/30"/>
        {["all","governance_blindspot","value_burial","silo_fragmentation","compliance_exposure","data_rot","none"].map(p=>(
          <button key={p} onClick={()=>setPat(p)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${patFilter===p?"bg-purple-900 border-purple-700 text-white":"bg-slate-900 border-purple-600/30 text-violet-200/60 hover:text-white"}`}>
            {p.replace(/_/g," ")}
          </button>
        ))}
      </div>

      {/* Entity cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {filtered.map(a=>(
          <div key={a.asset_id} onClick={()=>setSelected(a)}
            className="bg-slate-900 border border-purple-600/30 rounded-xl p-4 cursor-pointer hover:border-violet-500 transition-colors">
            <div className="flex items-center justify-between mb-1">
              <span className="font-bold text-white">{a.asset_id}</span>
              <span className="text-xs text-violet-200/60">{a.region}</span>
            </div>
            <div className="text-xs text-purple-400 mb-2 capitalize">{a.data_domain.replace(/_/g," ")}</div>
            <div className="flex gap-1 mb-3 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[a.dark_data_risk as keyof typeof RISK_BADGE]||"bg-slate-700 text-slate-300"}`}>{a.dark_data_risk}</span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[a.dark_data_severity as keyof typeof SEV_BADGE]||"bg-slate-700 text-slate-300"}`}>{a.dark_data_severity.replace(/_/g," ")}</span>
            </div>
            <div className="text-2xl font-black text-violet-400 mb-1">{a.dark_data_composite.toFixed(1)}</div>
            <div className="text-xs text-violet-200/50 mb-2 capitalize">{a.dark_data_pattern.replace(/_/g," ")}</div>
            <div className="text-xs text-purple-400 font-medium mb-2">Valeur cachée: {a.estimated_hidden_value_index.toFixed(2)}/10</div>
            <div className="flex gap-1 flex-wrap">
              {a.has_hidden_value_signal && <span className="px-1.5 py-0.5 rounded bg-purple-900 text-purple-300 text-xs">VALEUR CACHÉE</span>}
              {a.requires_immediate_governance && <span className="px-1.5 py-0.5 rounded bg-red-900 text-red-300 text-xs">GOUVERNANCE URGENTE</span>}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
