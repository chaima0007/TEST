"use client";
import { useEffect, useState } from "react";

type Entity = {
  id: string; region: string;
  compliance_risk: string; compliance_pattern: string;
  compliance_severity: string; recommended_action: string;
  policy_score: number; audit_score: number;
  risk_score: number; culture_score: number;
  compliance_composite: number; has_compliance_breach: boolean;
  requires_executive_action: boolean; estimated_sanction_risk_index: number;
  compliance_signal: string;
};
type Summary = {
  total: number; risk_counts: Record<string,number>;
  pattern_counts: Record<string,number>; severity_counts: Record<string,number>;
  action_counts: Record<string,number>; avg_compliance_composite: number;
  compliance_breach_count: number; executive_action_count: number;
  avg_policy_score: number; avg_audit_score: number;
  avg_risk_score: number; avg_culture_score: number;
  avg_estimated_sanction_risk_index: number;
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
const PAT_COLORS  = { none:"#10b981", regulatory_breach:"#ef4444", audit_failure:"#f97316", sanction_risk:"#dc2626", policy_gap:"#f59e0b", reporting_violation:"#a855f7" };
const SEV_COLORS  = { compliant:"#10b981", monitored:"#f59e0b", exposed:"#f97316", violated:"#ef4444" };
const ACT_COLORS  = { no_action:"#10b981", compliance_monitoring:"#06b6d4", policy_update:"#3b82f6", audit_remediation:"#f59e0b", regulatory_dialogue:"#a855f7", sanction_response:"#f97316", emergency_compliance:"#ef4444", regulatory_shutdown:"#7f1d1d" };
const RISK_BADGE  = { low:"bg-emerald-900 text-emerald-300", moderate:"bg-amber-900 text-amber-300", high:"bg-orange-900 text-orange-300", critical:"bg-red-900 text-red-300" };
const SEV_BADGE   = { compliant:"bg-emerald-900 text-emerald-300", monitored:"bg-amber-900 text-amber-300", exposed:"bg-orange-900 text-orange-300", violated:"bg-red-900 text-red-300" };

function DetailModal({ entity, onClose }: { entity: Entity; onClose: () => void }) {
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
            <span className="text-lg font-bold text-white">{entity.id}</span>
            <span className="ml-2 text-rose-400 text-xs">{entity.region}</span>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl leading-none">✕</button>
        </div>
        <div className="flex gap-2 mb-4">
          {(["scores","signal","action"] as const).map(t=>(
            <button key={t} onClick={()=>setTab(t)}
              className={`px-3 py-1 rounded text-xs font-medium transition-colors ${tab===t?"bg-rose-700 text-white":"bg-slate-800 text-slate-400 hover:text-white"}`}>
              {t.charAt(0).toUpperCase()+t.slice(1)}
            </button>
          ))}
        </div>
        {tab==="scores" && (
          <div className="grid grid-cols-2 gap-3 text-sm">
            {[
              ["Politique",   entity.policy_score,  "#fb7185"],
              ["Audit",       entity.audit_score,   "#ef4444"],
              ["Risque",      entity.risk_score,    "#dc2626"],
              ["Culture",     entity.culture_score, "#f97316"],
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
              <div className="text-slate-400 text-xs mb-1">Compliance Composite</div>
              <div className="text-white font-bold text-2xl">{entity.compliance_composite.toFixed(1)}</div>
            </div>
          </div>
        )}
        {tab==="signal" && (
          <div className="bg-slate-800 rounded-lg p-4 text-sm text-slate-200 leading-relaxed">
            {entity.compliance_signal}
            <div className="mt-3 flex gap-2 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[entity.compliance_risk as keyof typeof RISK_BADGE]||"bg-slate-700 text-slate-300"}`}>{entity.compliance_risk}</span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[entity.compliance_severity as keyof typeof SEV_BADGE]||"bg-slate-700 text-slate-300"}`}>{entity.compliance_severity}</span>
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
              <div className="text-slate-400 text-xs mb-1">Indice Risque Sanction</div>
              <div className="text-white font-bold">{entity.estimated_sanction_risk_index.toFixed(2)} / 10</div>
            </div>
            <div className="flex gap-2">
              {entity.has_compliance_breach     && <span className="px-2 py-1 rounded bg-red-900 text-red-300 text-xs font-medium">BRÈCHE</span>}
              {entity.requires_executive_action && <span className="px-2 py-1 rounded bg-orange-900 text-orange-300 text-xs font-medium">ACTION DG</span>}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function RegulatoryComplianceDashboard() {
  const [data, setData]         = useState<{ entities: Entity[]; summary: Summary }|null>(null);
  const [filter, setFilter]     = useState<string>("all");
  const [patFilter, setPat]     = useState<string>("all");
  const [selected, setSelected] = useState<Entity|null>(null);

  useEffect(()=>{
    fetch("/api/regulatory-compliance-legal-engine")
      .then(r=>r.json()).then(setData).catch(console.error);
  },[]);

  if (!data) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-slate-300 text-lg animate-pulse">Loading Compliance Engine...</div>
    </div>
  );

  const { entities, summary } = data;
  const filtered = entities.filter(e=>
    (filter==="all" || e.compliance_risk===filter) &&
    (patFilter==="all" || e.compliance_pattern===patFilter)
  );

  const dists = [
    { title:"Risk",     counts:summary.risk_counts,     colors:RISK_COLORS },
    { title:"Pattern",  counts:summary.pattern_counts,  colors:PAT_COLORS  },
    { title:"Severity", counts:summary.severity_counts, colors:SEV_COLORS  },
    { title:"Action",   counts:summary.action_counts,   colors:ACT_COLORS  },
  ] as Array<{title:string;counts:Record<string,number>;colors:Record<string,string>}>;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {selected && <DetailModal entity={selected} onClose={()=>setSelected(null)}/>}

      <div>
        <h1 className="text-2xl font-bold text-white">Conformité Réglementaire & Intelligence Juridique</h1>
        <p className="text-slate-400 text-sm mt-1">Politique · Audit · Risque Sanction · Culture Compliance — surveillance proactive et protection réglementaire</p>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {[
          ["Entités",        summary.total,                                                          "text-slate-300"],
          ["Composite",      summary.avg_compliance_composite,                                       "text-rose-400"],
          ["Brèches Conf.",  summary.compliance_breach_count,                                        "text-red-400"],
          ["Action Exec.",   summary.executive_action_count,                                         "text-orange-400"],
          ["Risque Sanction",`${summary.avg_estimated_sanction_risk_index.toFixed(1)}/10`,           "text-rose-400"],
          ["Moy Politique",  `${Math.round(summary.avg_policy_score)}`,                              "text-slate-300"],
        ].map(([l,v,c])=>(
          <div key={String(l)} className="bg-slate-900 border border-slate-800 rounded-xl p-3 text-center">
            <div className={`text-xl font-bold ${c}`}>{v}</div>
            <div className="text-xs text-slate-500 mt-0.5">{l}</div>
          </div>
        ))}
      </div>

      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
        <div className="grid grid-cols-4 gap-4">
          <Gauge value={summary.avg_policy_score}  label="Politique" color="#fb7185"/>
          <Gauge value={summary.avg_audit_score}   label="Audit"     color="#ef4444"/>
          <Gauge value={summary.avg_risk_score}    label="Risque"    color="#dc2626"/>
          <Gauge value={summary.avg_culture_score} label="Culture"   color="#f97316"/>
        </div>
      </div>

      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 grid grid-cols-1 md:grid-cols-2 gap-5">
        {dists.map(d=><DistBar key={d.title} {...d}/>)}
      </div>

      <div className="flex flex-wrap gap-2">
        {["all","low","moderate","high","critical"].map(r=>(
          <button key={r} onClick={()=>setFilter(r)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${filter===r?"bg-rose-700 border-rose-600 text-white":"bg-slate-900 border-slate-700 text-slate-400 hover:text-white"}`}>
            {r}
          </button>
        ))}
        <span className="w-px h-5 self-center bg-slate-700"/>
        {["all","none","regulatory_breach","audit_failure","sanction_risk","policy_gap","reporting_violation"].map(p=>(
          <button key={p} onClick={()=>setPat(p)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${patFilter===p?"bg-slate-700 border-slate-600 text-white":"bg-slate-900 border-slate-700 text-slate-400 hover:text-white hover:border-rose-700"}`}>
            {p.replace(/_/g," ")}
          </button>
        ))}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {filtered.map(e=>(
          <div key={e.id} onClick={()=>setSelected(e)}
            className="bg-slate-900 border border-slate-800 rounded-xl p-4 cursor-pointer hover:border-rose-700 transition-colors">
            <div className="flex items-center justify-between mb-1">
              <span className="font-bold text-white">{e.id}</span>
              <span className="text-xs text-slate-400">{e.region}</span>
            </div>
            <div className="flex gap-1 mb-3 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[e.compliance_risk as keyof typeof RISK_BADGE]||"bg-slate-700 text-slate-300"}`}>{e.compliance_risk}</span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[e.compliance_severity as keyof typeof SEV_BADGE]||"bg-slate-700 text-slate-300"}`}>{e.compliance_severity}</span>
            </div>
            <div className="text-2xl font-black text-white mb-1">{e.compliance_composite.toFixed(1)}</div>
            <div className="text-xs text-slate-500 mb-2 capitalize">{e.compliance_pattern.replace(/_/g," ")}</div>
            <div className="text-xs text-rose-400 font-medium mb-2">Sanction Idx: {e.estimated_sanction_risk_index.toFixed(2)}/10</div>
            <div className="flex gap-1 flex-wrap">
              {e.has_compliance_breach     && <span className="px-1.5 py-0.5 rounded bg-red-900 text-red-300 text-xs">BRÈCHE</span>}
              {e.requires_executive_action && <span className="px-1.5 py-0.5 rounded bg-orange-900 text-orange-300 text-xs">ACTION DG</span>}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
