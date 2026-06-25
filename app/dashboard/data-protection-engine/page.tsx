"use client";
import { useEffect, useState } from "react";

type Dossier = {
  dossier_id: string; entity_type: string; region: string;
  protection_risk: string; violation_pattern: string;
  protection_severity: string; recommended_action: string;
  rgpd_score: number; rights_score: number;
  breach_score: number; transfer_score: number;
  protection_composite: number; has_active_violation: boolean;
  requires_dpa_notification: boolean;
  estimated_fine_risk_index: number;
  protection_signal: string;
};
type Summary = {
  total: number; risk_counts: Record<string,number>;
  pattern_counts: Record<string,number>; severity_counts: Record<string,number>;
  action_counts: Record<string,number>; avg_protection_composite: number;
  active_violation_count: number; dpa_notification_count: number;
  avg_rgpd_score: number; avg_rights_score: number;
  avg_breach_score: number; avg_transfer_score: number;
  avg_estimated_fine_risk_index: number;
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
const PAT_COLORS  = { none:"#10b981", consent_violation:"#f59e0b", data_breach:"#ef4444", rights_denial:"#f97316", cross_border_exposure:"#a855f7", retention_breach:"#3b82f6" };
const SEV_COLORS  = { compliant:"#10b981", monitoring:"#f59e0b", at_risk:"#f97316", breached:"#ef4444" };
const ACT_COLORS  = { no_action:"#10b981", compliance_monitoring:"#f59e0b", consent_remediation:"#06b6d4", rights_processing:"#3b82f6", dpia_required:"#a855f7", breach_notification:"#f97316", transfer_suspension:"#dc2626", regulatory_filing:"#ec4899", emergency_data_lockdown:"#7f1d1d" };
const RISK_BADGE  = { low:"bg-emerald-900 text-emerald-300", moderate:"bg-amber-900 text-amber-300", high:"bg-orange-900 text-orange-300", critical:"bg-red-900 text-red-300" };
const SEV_BADGE   = { compliant:"bg-emerald-900 text-emerald-300", monitoring:"bg-amber-900 text-amber-300", at_risk:"bg-orange-900 text-orange-300", breached:"bg-red-900 text-red-300" };

function DetailModal({ dos, onClose }: { dos: Dossier; onClose: () => void }) {
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
            <span className="text-lg font-bold text-white">{dos.dossier_id}</span>
            <span className="ml-2 text-slate-400 text-sm capitalize">{dos.entity_type}</span>
            <span className="ml-2 text-violet-400 text-xs">{dos.region}</span>
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
              ["RGPD",      dos.rgpd_score,     "#a855f7"],
              ["Droits",    dos.rights_score,   "#06b6d4"],
              ["Violation", dos.breach_score,   "#ef4444"],
              ["Transfert", dos.transfer_score, "#f97316"],
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
              <div className="text-slate-400 text-xs mb-1">Protection Composite</div>
              <div className="text-white font-bold text-2xl">{dos.protection_composite.toFixed(1)}</div>
            </div>
          </div>
        )}
        {tab==="signal" && (
          <div className="bg-slate-800 rounded-lg p-4 text-sm text-slate-200 leading-relaxed">
            {dos.protection_signal}
            <div className="mt-3 flex gap-2 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[dos.protection_risk as keyof typeof RISK_BADGE]||"bg-slate-700 text-slate-300"}`}>{dos.protection_risk}</span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[dos.protection_severity as keyof typeof SEV_BADGE]||"bg-slate-700 text-slate-300"}`}>{dos.protection_severity.replace(/_/g," ")}</span>
            </div>
          </div>
        )}
        {tab==="action" && (
          <div className="space-y-3 text-sm">
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Action Recommandée</div>
              <div className="text-white font-medium">{dos.recommended_action.replace(/_/g," ")}</div>
            </div>
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Risque Amende</div>
              <div className="text-white font-bold">{dos.estimated_fine_risk_index.toFixed(2)} / 10</div>
            </div>
            <div className="flex gap-2">
              {dos.has_active_violation       && <span className="px-2 py-1 rounded bg-red-900 text-red-300 text-xs font-medium">VIOLATION</span>}
              {dos.requires_dpa_notification  && <span className="px-2 py-1 rounded bg-orange-900 text-orange-300 text-xs font-medium">NOTIF CNIL</span>}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function DataProtectionDashboard() {
  const [data, setData]     = useState<{ dossiers: Dossier[]; summary: Summary }|null>(null);
  const [filter, setFilter] = useState<string>("all");
  const [patFilter, setPat] = useState<string>("all");
  const [selected, setSelected] = useState<Dossier|null>(null);

  useEffect(()=>{
    fetch("/api/data-protection-engine")
      .then(r=>r.json()).then(setData).catch(console.error);
  },[]);

  if (!data) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-violet-400 text-lg animate-pulse">Chargement Protection des Données...</div>
    </div>
  );

  const { dossiers, summary } = data;
  const filtered = dossiers.filter(d=>
    (filter==="all" || d.protection_risk===filter) &&
    (patFilter==="all" || d.violation_pattern===patFilter)
  );

  const dists = [
    { title:"Risque",   counts:summary.risk_counts,     colors:RISK_COLORS },
    { title:"Pattern",  counts:summary.pattern_counts,  colors:PAT_COLORS  },
    { title:"Sévérité", counts:summary.severity_counts, colors:SEV_COLORS  },
    { title:"Action",   counts:summary.action_counts,   colors:ACT_COLORS  },
  ] as Array<{title:string;counts:Record<string,number>;colors:Record<string,string>}>;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {selected && <DetailModal dos={selected} onClose={()=>setSelected(null)}/>}

      <div>
        <h1 className="text-2xl font-bold text-white">Protection des Données</h1>
        <p className="text-slate-400 text-sm mt-1">RGPD · Droits · Violations · Transferts — conformité et protection proactive</p>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {[
          ["Dossiers",     summary.total,                                                         "text-violet-400"],
          ["Composite",    summary.avg_protection_composite,                                      "text-purple-400"],
          ["Violations",   summary.active_violation_count,                                        "text-red-400"],
          ["Notif CNIL",   summary.dpa_notification_count,                                        "text-orange-400"],
          ["Risque Amende",`${summary.avg_estimated_fine_risk_index.toFixed(1)}/10`,              "text-violet-400"],
          ["Moy RGPD",     `${Math.round(summary.avg_rgpd_score)}`,                              "text-purple-400"],
        ].map(([l,v,c])=>(
          <div key={String(l)} className="bg-slate-900 border border-slate-800 rounded-xl p-3 text-center">
            <div className={`text-xl font-bold ${c}`}>{v}</div>
            <div className="text-xs text-slate-500 mt-0.5">{l}</div>
          </div>
        ))}
      </div>

      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
        <div className="grid grid-cols-4 gap-4">
          <Gauge value={summary.avg_rgpd_score}     label="RGPD"      color="#a855f7"/>
          <Gauge value={summary.avg_rights_score}   label="Droits"    color="#06b6d4"/>
          <Gauge value={summary.avg_breach_score}   label="Violation" color="#ef4444"/>
          <Gauge value={summary.avg_transfer_score} label="Transfert" color="#f97316"/>
        </div>
      </div>

      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 grid grid-cols-1 md:grid-cols-2 gap-5">
        {dists.map(d=><DistBar key={d.title} {...d}/>)}
      </div>

      <div className="flex flex-wrap gap-2">
        {["all","low","moderate","high","critical"].map(r=>(
          <button key={r} onClick={()=>setFilter(r)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${filter===r?"bg-violet-700 border-violet-600 text-white":"bg-slate-900 border-slate-700 text-slate-400 hover:text-white"}`}>
            {r}
          </button>
        ))}
        <span className="w-px h-5 self-center bg-slate-700"/>
        {["all","consent_violation","data_breach","rights_denial","cross_border_exposure","retention_breach"].map(p=>(
          <button key={p} onClick={()=>setPat(p)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${patFilter===p?"bg-purple-900 border-purple-800 text-white":"bg-slate-900 border-slate-700 text-slate-400 hover:text-white"}`}>
            {p.replace(/_/g," ")}
          </button>
        ))}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {filtered.map(d=>(
          <div key={d.dossier_id} onClick={()=>setSelected(d)}
            className="bg-slate-900 border border-slate-800 rounded-xl p-4 cursor-pointer hover:border-violet-700 transition-colors">
            <div className="flex items-center justify-between mb-1">
              <span className="font-bold text-white">{d.dossier_id}</span>
              <span className="text-xs text-slate-400">{d.region}</span>
            </div>
            <div className="text-xs text-violet-400 mb-2 capitalize">{d.entity_type}</div>
            <div className="flex gap-1 mb-3 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[d.protection_risk as keyof typeof RISK_BADGE]||"bg-slate-700 text-slate-300"}`}>{d.protection_risk}</span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[d.protection_severity as keyof typeof SEV_BADGE]||"bg-slate-700 text-slate-300"}`}>{d.protection_severity.replace(/_/g," ")}</span>
            </div>
            <div className="text-2xl font-black text-white mb-1">{d.protection_composite.toFixed(1)}</div>
            <div className="text-xs text-slate-500 mb-2 capitalize">{d.violation_pattern.replace(/_/g," ")}</div>
            <div className="text-xs text-violet-400 font-medium mb-2">Amende: {d.estimated_fine_risk_index.toFixed(2)}/10</div>
            <div className="flex gap-1 flex-wrap">
              {d.has_active_violation      && <span className="px-1.5 py-0.5 rounded bg-red-900 text-red-300 text-xs">VIOLATION</span>}
              {d.requires_dpa_notification && <span className="px-1.5 py-0.5 rounded bg-orange-900 text-orange-300 text-xs">CNIL</span>}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
