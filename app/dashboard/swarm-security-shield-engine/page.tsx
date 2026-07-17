"use client";
import { useEffect, useState } from "react";

type Agent = {
  agent_id: string; agent_type: string; region: string;
  security_risk: string; threat_pattern: string;
  security_severity: string; recommended_action: string;
  credential_score: number; access_score: number;
  injection_score: number; compliance_score: number;
  security_composite: number; has_active_threat: boolean;
  requires_immediate_response: boolean; estimated_exposure_severity: number;
  security_signal: string;
};
type Summary = {
  total: number; risk_counts: Record<string,number>;
  pattern_counts: Record<string,number>; severity_counts: Record<string,number>;
  action_counts: Record<string,number>; avg_security_composite: number;
  active_threat_count: number; immediate_response_count: number;
  avg_credential_score: number; avg_access_score: number;
  avg_injection_score: number; avg_compliance_score: number;
  avg_estimated_exposure_severity: number;
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
const PAT_COLORS  = { none:"#10b981", credential_exposure:"#ef4444", injection_attempt:"#dc2626", data_exfiltration:"#f97316", access_anomaly:"#f59e0b", compliance_violation:"#a855f7" };
const SEV_COLORS  = { secure:"#10b981", monitoring:"#f59e0b", threatened:"#f97316", breached:"#ef4444" };
const ACT_COLORS  = { no_action:"#10b981", security_monitoring:"#f59e0b", access_review:"#06b6d4", credential_rotation:"#f97316", injection_block:"#dc2626", data_quarantine:"#a855f7", compliance_audit:"#3b82f6", incident_containment:"#ec4899", emergency_lockdown:"#7f1d1d" };
const RISK_BADGE  = { low:"bg-emerald-900 text-emerald-300", moderate:"bg-amber-900 text-amber-300", high:"bg-orange-900 text-orange-300", critical:"bg-red-900 text-red-300" };
const SEV_BADGE   = { secure:"bg-emerald-900 text-emerald-300", monitoring:"bg-amber-900 text-amber-300", threatened:"bg-orange-900 text-orange-300", breached:"bg-red-900 text-red-300" };

function DetailModal({ agent, onClose }: { agent: Agent; onClose: () => void }) {
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
            <span className="text-lg font-bold text-white">{agent.agent_id}</span>
            <span className="ml-2 text-slate-400 text-sm capitalize">{agent.agent_type.replace(/_/g," ")}</span>
            <span className="ml-2 text-red-400 text-xs">{agent.region}</span>
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
              ["Credential", agent.credential_score, "#ef4444"],
              ["Access",     agent.access_score,     "#f97316"],
              ["Injection",  agent.injection_score,  "#dc2626"],
              ["Compliance", agent.compliance_score, "#a855f7"],
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
              <div className="text-slate-400 text-xs mb-1">Security Composite</div>
              <div className="text-white font-bold text-2xl">{agent.security_composite.toFixed(1)}</div>
            </div>
          </div>
        )}
        {tab==="signal" && (
          <div className="bg-slate-800 rounded-lg p-4 text-sm text-slate-200 leading-relaxed">
            {agent.security_signal}
            <div className="mt-3 flex gap-2 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[agent.security_risk as keyof typeof RISK_BADGE]||"bg-slate-700 text-slate-300"}`}>{agent.security_risk}</span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[agent.security_severity as keyof typeof SEV_BADGE]||"bg-slate-700 text-slate-300"}`}>{agent.security_severity}</span>
            </div>
          </div>
        )}
        {tab==="action" && (
          <div className="space-y-3 text-sm">
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Recommended Action</div>
              <div className="text-white font-medium">{agent.recommended_action.replace(/_/g," ")}</div>
            </div>
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Exposure Severity</div>
              <div className="text-white font-bold">{agent.estimated_exposure_severity.toFixed(2)} / 10</div>
            </div>
            <div className="flex gap-2">
              {agent.has_active_threat           && <span className="px-2 py-1 rounded bg-red-900 text-red-300 text-xs font-medium">THREAT</span>}
              {agent.requires_immediate_response && <span className="px-2 py-1 rounded bg-orange-900 text-orange-300 text-xs font-medium">RESPOND NOW</span>}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function SecurityDashboard() {
  const [data, setData]     = useState<{ agents: Agent[]; summary: Summary }|null>(null);
  const [filter, setFilter] = useState<string>("all");
  const [patFilter, setPat] = useState<string>("all");
  const [selected, setSelected] = useState<Agent|null>(null);

  useEffect(()=>{
    fetch("/api/swarm-security-shield-engine")
      .then(r=>r.json()).then(setData).catch(console.error);
  },[]);

  if (!data) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-red-400 text-lg animate-pulse">Loading Security Shield...</div>
    </div>
  );

  const { agents, summary } = data;
  const filtered = agents.filter(a=>
    (filter==="all" || a.security_risk===filter) &&
    (patFilter==="all" || a.threat_pattern===patFilter)
  );

  const dists = [
    { title:"Risk",     counts:summary.risk_counts,     colors:RISK_COLORS },
    { title:"Threat",   counts:summary.pattern_counts,  colors:PAT_COLORS  },
    { title:"Severity", counts:summary.severity_counts, colors:SEV_COLORS  },
    { title:"Action",   counts:summary.action_counts,   colors:ACT_COLORS  },
  ] as Array<{title:string;counts:Record<string,number>;colors:Record<string,string>}>;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {selected && <DetailModal agent={selected} onClose={()=>setSelected(null)}/>}

      <div>
        <h1 className="text-2xl font-bold text-white">Swarm Security Shield</h1>
        <p className="text-slate-400 text-sm mt-1">Credential · Access · Injection · Compliance — protecting all agents silently</p>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {[
          ["Agents",      summary.total,                                       "text-red-400"],
          ["Avg Risk",    summary.avg_security_composite,                      "text-rose-400"],
          ["Threats",     summary.active_threat_count,                         "text-orange-400"],
          ["Respond Now", summary.immediate_response_count,                    "text-red-400"],
          ["Avg Exposure",`${summary.avg_estimated_exposure_severity.toFixed(1)}/10`, "text-rose-400"],
          ["Avg Cred",    `${Math.round(summary.avg_credential_score)}`,       "text-red-400"],
        ].map(([l,v,c])=>(
          <div key={String(l)} className="bg-slate-900 border border-slate-800 rounded-xl p-3 text-center">
            <div className={`text-xl font-bold ${c}`}>{v}</div>
            <div className="text-xs text-slate-500 mt-0.5">{l}</div>
          </div>
        ))}
      </div>

      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
        <div className="grid grid-cols-4 gap-4">
          <Gauge value={summary.avg_credential_score}  label="Credential"  color="#ef4444"/>
          <Gauge value={summary.avg_access_score}      label="Access"      color="#f97316"/>
          <Gauge value={summary.avg_injection_score}   label="Injection"   color="#dc2626"/>
          <Gauge value={summary.avg_compliance_score}  label="Compliance"  color="#a855f7"/>
        </div>
      </div>

      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 grid grid-cols-1 md:grid-cols-2 gap-5">
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
        {["all","credential_exposure","injection_attempt","data_exfiltration","access_anomaly","compliance_violation"].map(p=>(
          <button key={p} onClick={()=>setPat(p)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${patFilter===p?"bg-rose-900 border-rose-800 text-white":"bg-slate-900 border-slate-700 text-slate-400 hover:text-white"}`}>
            {p.replace(/_/g," ")}
          </button>
        ))}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {filtered.map(a=>(
          <div key={a.agent_id} onClick={()=>setSelected(a)}
            className="bg-slate-900 border border-slate-800 rounded-xl p-4 cursor-pointer hover:border-red-700 transition-colors">
            <div className="flex items-center justify-between mb-1">
              <span className="font-bold text-white">{a.agent_id}</span>
              <span className="text-xs text-slate-400">{a.region}</span>
            </div>
            <div className="text-xs text-red-400 mb-2 capitalize">{a.agent_type.replace(/_/g," ")}</div>
            <div className="flex gap-1 mb-3 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[a.security_risk as keyof typeof RISK_BADGE]||"bg-slate-700 text-slate-300"}`}>{a.security_risk}</span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[a.security_severity as keyof typeof SEV_BADGE]||"bg-slate-700 text-slate-300"}`}>{a.security_severity}</span>
            </div>
            <div className="text-2xl font-black text-white mb-1">{a.security_composite.toFixed(1)}</div>
            <div className="text-xs text-slate-500 mb-2 capitalize">{a.threat_pattern.replace(/_/g," ")}</div>
            <div className="text-xs text-rose-400 font-medium mb-2">Exposure: {a.estimated_exposure_severity.toFixed(2)}/10</div>
            <div className="flex gap-1 flex-wrap">
              {a.has_active_threat           && <span className="px-1.5 py-0.5 rounded bg-red-900 text-red-300 text-xs">THREAT</span>}
              {a.requires_immediate_response && <span className="px-1.5 py-0.5 rounded bg-orange-900 text-orange-300 text-xs">RESPOND</span>}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
