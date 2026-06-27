"use client";
import { useEffect, useState } from "react";

type CryptoSystem = {
  system_id: string; system_type: string; region: string;
  crypto_risk: string; crypto_pattern: string;
  crypto_severity: string; recommended_action: string;
  vulnerability_score: number; temporal_score: number;
  resilience_score: number; readiness_score: number;
  crypto_composite: number; is_quantum_vulnerable: boolean;
  estimated_quantum_breach_index: number; crypto_signal: string;
};
type Summary = {
  total: number; risk_counts: Record<string,number>;
  pattern_counts: Record<string,number>; severity_counts: Record<string,number>;
  action_counts: Record<string,number>; avg_crypto_composite: number;
  compromised_count: number; quantum_vulnerable_count: number;
  avg_vulnerability_score: number; avg_temporal_score: number;
  avg_resilience_score: number; avg_readiness_score: number;
  avg_estimated_quantum_breach_index: number;
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
const PAT_COLORS  = { none:"#10b981", quantum_exposure:"#ef4444", temporal_attack_surface:"#f97316", key_compromise_risk:"#dc2626", certificate_collapse:"#f59e0b", crypto_agility_deficit:"#a855f7" };
const SEV_COLORS  = { quantum_safe:"#10b981", hardening:"#f59e0b", exposed:"#f97316", compromised:"#ef4444" };
const ACT_COLORS  = { no_action:"#10b981", crypto_audit:"#06b6d4", pqc_migration:"#3b82f6", temporal_hardening:"#f59e0b", emergency_rekeying:"#dc2626", quantum_isolation:"#ef4444" };
const RISK_BADGE  = { low:"bg-emerald-900 text-emerald-300", moderate:"bg-amber-900 text-amber-300", high:"bg-orange-900 text-orange-300", critical:"bg-red-900 text-red-300" };
const SEV_BADGE   = { quantum_safe:"bg-emerald-900 text-emerald-300", hardening:"bg-amber-900 text-amber-300", exposed:"bg-orange-900 text-orange-300", compromised:"bg-red-900 text-red-300" };

function DetailModal({ entity, onClose }: { entity: CryptoSystem; onClose: () => void }) {
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
            <span className="text-lg font-bold text-white">{entity.system_id}</span>
            <span className="ml-2 text-cyan-400 text-xs">{entity.system_type}</span>
            <span className="ml-2 text-slate-400 text-xs">{entity.region}</span>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl leading-none">✕</button>
        </div>
        <div className="flex gap-2 mb-4">
          {(["scores","signal","action"] as const).map(t=>(
            <button key={t} onClick={()=>setTab(t)}
              className={`px-3 py-1 rounded text-xs font-medium transition-colors ${tab===t?"bg-cyan-700 text-white":"bg-slate-800 text-slate-400 hover:text-white"}`}>
              {t.charAt(0).toUpperCase()+t.slice(1)}
            </button>
          ))}
        </div>
        {tab==="scores" && (
          <div className="grid grid-cols-2 gap-3 text-sm">
            {[
              ["Exposition Quantique", entity.vulnerability_score, "#ef4444"],
              ["Intégrité Temporelle", entity.temporal_score,      "#f97316"],
              ["Résilience Crypto",    entity.resilience_score,    "#06b6d4"],
              ["Préparation PQC",      entity.readiness_score,     "#a855f7"],
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
              <div className="text-slate-400 text-xs mb-1">Crypto Composite</div>
              <div className="text-white font-bold text-2xl">{entity.crypto_composite.toFixed(1)}</div>
            </div>
          </div>
        )}
        {tab==="signal" && (
          <div className="bg-slate-800 rounded-lg p-4 text-sm text-slate-200 leading-relaxed">
            {entity.crypto_signal}
            <div className="mt-3 flex gap-2 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[entity.crypto_risk as keyof typeof RISK_BADGE]||"bg-slate-700 text-slate-300"}`}>{entity.crypto_risk}</span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[entity.crypto_severity as keyof typeof SEV_BADGE]||"bg-slate-700 text-slate-300"}`}>{entity.crypto_severity}</span>
            </div>
          </div>
        )}
        {tab==="action" && (
          <div className="space-y-3 text-sm">
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Action Recommandée</div>
              <div className="text-white font-medium">{entity.recommended_action.replace(/_/g," ")}</div>
            </div>
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Quantum Breach Index</div>
              <div className="text-white font-bold">{entity.estimated_quantum_breach_index.toFixed(2)} / 10</div>
            </div>
            <div className="flex gap-2">
              {entity.is_quantum_vulnerable && <span className="px-2 py-1 rounded bg-cyan-900 text-cyan-300 text-xs font-medium">QUANTUM VULNÉRABLE</span>}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function PostQuantumCryptographyDashboard() {
  const [data, setData]         = useState<{ systems: CryptoSystem[]; summary: Summary }|null>(null);
  const [filter, setFilter]     = useState<string>("all");
  const [patFilter, setPat]     = useState<string>("all");
  const [selected, setSelected] = useState<CryptoSystem|null>(null);

  useEffect(()=>{
    fetch("/api/post-quantum-cryptography-engine")
      .then(r=>r.json()).then(setData).catch(console.error);
  },[]);

  if (!data) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-slate-300 text-lg animate-pulse">Loading Cryptography Engine...</div>
    </div>
  );

  const { systems, summary } = data;
  const filtered = systems.filter(s=>
    (filter==="all" || s.crypto_risk===filter) &&
    (patFilter==="all" || s.crypto_pattern===patFilter)
  );

  const dists = [
    { title:"Risque Cryptographique", counts:summary.risk_counts,     colors:RISK_COLORS },
    { title:"Pattern Attaque",        counts:summary.pattern_counts,  colors:PAT_COLORS  },
    { title:"Sévérité Système",       counts:summary.severity_counts, colors:SEV_COLORS  },
    { title:"Action Recommandée",     counts:summary.action_counts,   colors:ACT_COLORS  },
  ] as Array<{title:string;counts:Record<string,number>;colors:Record<string,string>}>;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {selected && <DetailModal entity={selected} onClose={()=>setSelected(null)}/>}

      <div>
        <h1 className="text-2xl font-bold text-white">Post-Quantum Cryptography & Temporal Integrity</h1>
        <p className="text-slate-400 text-sm mt-1">Exposition quantique · Intégrité temporelle · Résilience crypto · Préparation PQC</p>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {([
          ["Total Systèmes",      summary.total,                                                    "text-slate-300"],
          ["Critiques",           summary.risk_counts["critical"]??0,                               "text-red-400"],
          ["Vulnérables Quantum", summary.quantum_vulnerable_count,                                 "text-cyan-400"],
          ["Composite Moyen",     summary.avg_crypto_composite,                                     "text-teal-400"],
          ["Score Temporel Moy.", `${Math.round(summary.avg_temporal_score)}`,                      "text-amber-400"],
          ["Score Résilience",    `${Math.round(summary.avg_resilience_score)}`,                    "text-slate-300"],
        ] as const).map(([l,v,c])=>(
          <div key={String(l)} className="bg-slate-900 border border-slate-800 rounded-xl p-3 text-center">
            <div className={`text-xl font-bold ${c}`}>{v}</div>
            <div className="text-xs text-slate-500 mt-0.5">{l}</div>
          </div>
        ))}
      </div>

      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
        <div className="grid grid-cols-4 gap-4">
          <Gauge value={summary.avg_vulnerability_score} label="Exposition Quantique"  color="#ef4444"/>
          <Gauge value={summary.avg_temporal_score}      label="Intégrité Temporelle"  color="#f97316"/>
          <Gauge value={summary.avg_resilience_score}    label="Résilience Crypto"     color="#06b6d4"/>
          <Gauge value={summary.avg_readiness_score}     label="Préparation PQC"       color="#a855f7"/>
        </div>
      </div>

      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 grid grid-cols-1 md:grid-cols-2 gap-5">
        {dists.map(d=><DistBar key={d.title} {...d}/>)}
      </div>

      <div className="flex flex-wrap gap-2">
        {["all","low","moderate","high","critical"].map(r=>(
          <button key={r} onClick={()=>setFilter(r)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${filter===r?"bg-cyan-700 border-cyan-600 text-white":"bg-slate-900 border-slate-700 text-slate-400 hover:text-white"}`}>
            {r}
          </button>
        ))}
        <span className="w-px h-5 self-center bg-slate-700"/>
        {["all","quantum_exposure","temporal_attack_surface","key_compromise_risk","certificate_collapse","crypto_agility_deficit","none"].map(p=>(
          <button key={p} onClick={()=>setPat(p)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${patFilter===p?"bg-slate-700 border-slate-600 text-white":"bg-slate-900 border-slate-700 text-slate-400 hover:text-white"}`}>
            {p.replace(/_/g," ")}
          </button>
        ))}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {filtered.map(s=>(
          <div key={s.system_id} onClick={()=>setSelected(s)}
            className="bg-slate-900 border border-slate-800 rounded-xl p-4 cursor-pointer hover:border-cyan-700 transition-colors">
            <div className="flex items-center justify-between mb-1">
              <span className="font-bold text-white">{s.system_id}</span>
              <span className="text-xs text-slate-400">{s.region}</span>
            </div>
            <div className="text-xs text-teal-400 mb-2">{s.system_type.replace(/_/g," ")}</div>
            <div className="flex gap-1 mb-3 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[s.crypto_risk as keyof typeof RISK_BADGE]||"bg-slate-700 text-slate-300"}`}>{s.crypto_risk}</span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[s.crypto_severity as keyof typeof SEV_BADGE]||"bg-slate-700 text-slate-300"}`}>{s.crypto_severity}</span>
            </div>
            <div className="text-2xl font-black text-white mb-1">{s.crypto_composite.toFixed(1)}</div>
            <div className="text-xs text-slate-500 mb-2 capitalize">{s.crypto_pattern.replace(/_/g," ")}</div>
            <div className="text-xs text-cyan-400 font-medium mb-2">QBI: {s.estimated_quantum_breach_index.toFixed(2)}/10</div>
            <div className="text-xs text-slate-400 leading-snug line-clamp-2">{s.crypto_signal}</div>
            <div className="mt-2 flex gap-1 flex-wrap">
              {s.is_quantum_vulnerable && <span className="px-1.5 py-0.5 rounded bg-cyan-900 text-cyan-300 text-xs">QUANTUM</span>}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
