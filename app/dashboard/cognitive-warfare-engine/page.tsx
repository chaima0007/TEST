"use client";
import { useEffect, useState } from "react";

type Target = {
  target_id: string; region: string; threat_domain: string;
  cognitive_warfare_risk: string; warfare_pattern: string;
  cognitive_severity: string; recommended_action: string;
  exposure_score: number; detection_score: number;
  resilience_score: number; sovereignty_score: number;
  cognitive_warfare_composite: number; has_active_threat: boolean;
  requires_immediate_response: boolean;
  estimated_cognitive_vulnerability_index: number;
  cognitive_warfare_signal: string;
};
type Summary = {
  total: number; risk_counts: Record<string,number>;
  pattern_counts: Record<string,number>; severity_counts: Record<string,number>;
  action_counts: Record<string,number>; avg_cognitive_warfare_composite: number;
  active_threat_count: number; immediate_response_count: number;
  avg_exposure_score: number; avg_detection_score: number;
  avg_resilience_score: number; avg_sovereignty_score: number;
  avg_estimated_cognitive_vulnerability_index: number;
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
const PAT_COLORS   = { none:"#10b981", narrative_capture:"#ef4444", deepfake_assault:"#dc2626", epistemic_collapse:"#7f1d1d", bot_swarm_attack:"#f97316", trust_erosion:"#a855f7" };
const SEV_COLORS   = { sovereign:"#10b981", resistant:"#f59e0b", compromised:"#f97316", captured:"#ef4444" };
const ACT_COLORS   = { no_action:"#10b981", info_monitoring:"#06b6d4", epistemic_reinforcement:"#3b82f6", bot_neutralization:"#f59e0b", narrative_counterstrike:"#f97316", cognitive_defense_protocol:"#ef4444" };
const RISK_BADGE   = { low:"bg-emerald-900 text-emerald-300", moderate:"bg-amber-900 text-amber-300", high:"bg-orange-900 text-orange-300", critical:"bg-red-900 text-red-300" };
const SEV_BADGE    = { sovereign:"bg-emerald-900 text-emerald-300", resistant:"bg-amber-900 text-amber-300", compromised:"bg-orange-900 text-orange-300", captured:"bg-red-900 text-red-300" };

function DetailModal({ target, onClose }: { target: Target; onClose: () => void }) {
  const [tab, setTab] = useState<"scores"|"signal"|"action">("scores");
  useEffect(()=>{
    const h = (e: KeyboardEvent) => { if (e.key==="Escape") onClose(); };
    window.addEventListener("keydown", h);
    return ()=>window.removeEventListener("keydown",h);
  },[onClose]);
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70" onClick={onClose}>
      <div className="bg-slate-900 border border-rose-500/30 rounded-xl w-full max-w-lg p-6 shadow-2xl" onClick={e=>e.stopPropagation()}>
        <div className="flex items-center justify-between mb-4">
          <div>
            <span className="text-lg font-bold text-white">{target.target_id}</span>
            <span className="ml-2 text-red-400 text-xs">{target.region}</span>
            <span className="ml-2 text-slate-500 text-xs capitalize">{target.threat_domain.replace(/_/g," ")}</span>
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
              ["Exposure",    target.exposure_score,    "#ef4444"],
              ["Detection",   target.detection_score,   "#f97316"],
              ["Resilience",  target.resilience_score,  "#a855f7"],
              ["Sovereignty", target.sovereignty_score, "#06b6d4"],
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
              <div className="text-slate-400 text-xs mb-1">Cognitive Warfare Composite</div>
              <div className="text-white font-bold text-2xl">{target.cognitive_warfare_composite.toFixed(1)}</div>
            </div>
          </div>
        )}
        {tab==="signal" && (
          <div className="bg-slate-800 rounded-lg p-4 text-sm text-slate-200 leading-relaxed">
            {target.cognitive_warfare_signal}
            <div className="mt-3 flex gap-2 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[target.cognitive_warfare_risk as keyof typeof RISK_BADGE]||"bg-slate-700 text-slate-300"}`}>{target.cognitive_warfare_risk}</span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[target.cognitive_severity as keyof typeof SEV_BADGE]||"bg-slate-700 text-slate-300"}`}>{target.cognitive_severity}</span>
            </div>
          </div>
        )}
        {tab==="action" && (
          <div className="space-y-3 text-sm">
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Recommended Action</div>
              <div className="text-white font-medium">{target.recommended_action.replace(/_/g," ")}</div>
            </div>
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Cognitive Vulnerability Index</div>
              <div className="text-white font-bold">{target.estimated_cognitive_vulnerability_index.toFixed(2)} / 10</div>
            </div>
            <div className="flex gap-2 flex-wrap">
              {target.has_active_threat           && <span className="px-2 py-1 rounded bg-red-900 text-red-300 text-xs font-medium">ACTIVE THREAT</span>}
              {target.requires_immediate_response && <span className="px-2 py-1 rounded bg-rose-900 text-rose-300 text-xs font-medium">IMMEDIATE RESPONSE</span>}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function CognitiveWarfareDashboard() {
  const [data, setData]         = useState<{ targets: Target[]; summary: Summary }|null>(null);
  const [filter, setFilter]     = useState<string>("all");
  const [patFilter, setPat]     = useState<string>("all");
  const [selected, setSelected] = useState<Target|null>(null);

  useEffect(()=>{
    fetch("/api/cognitive-warfare-engine")
      .then(r=>r.json()).then(setData).catch(console.error);
  },[]);

  if (!data) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-red-400 text-lg animate-pulse">Loading Cognitive Warfare Engine...</div>
    </div>
  );

  const { targets, summary } = data;
  const filtered = targets.filter(t=>
    (filter==="all" || t.cognitive_warfare_risk===filter) &&
    (patFilter==="all" || t.warfare_pattern===patFilter)
  );

  const dists: Array<{title:string;counts:Record<string,number>;colors:Record<string,string>}> = [
    { title:"Risk",     counts:summary.risk_counts,     colors:RISK_COLORS },
    { title:"Pattern",  counts:summary.pattern_counts,  colors:PAT_COLORS  },
    { title:"Severity", counts:summary.severity_counts, colors:SEV_COLORS  },
    { title:"Action",   counts:summary.action_counts,   colors:ACT_COLORS  },
  ];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {selected && <DetailModal target={selected} onClose={()=>setSelected(null)}/>}

      <div>
        <h1 className="text-2xl font-bold text-white">Cognitive Warfare & Information Integrity Engine</h1>
        <p className="text-slate-400 text-sm mt-1">Exposure · Detection · Resilience · Sovereignty — information warfare threat assessment</p>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {[
          ["Targets",        summary.total,                                                                    "text-red-400"],
          ["Avg Composite",  summary.avg_cognitive_warfare_composite,                                          "text-rose-400"],
          ["Active Threats", summary.active_threat_count,                                                      "text-red-400"],
          ["Immediate Resp", summary.immediate_response_count,                                                  "text-rose-400"],
          ["Avg Vuln Index", `${summary.avg_estimated_cognitive_vulnerability_index.toFixed(1)}/10`,           "text-red-400"],
          ["Avg Exposure",   `${Math.round(summary.avg_exposure_score)}`,                                      "text-rose-400"],
        ].map(([l,v,c])=>(
          <div key={String(l)} className="bg-slate-900 border border-rose-500/30 rounded-xl p-3 text-center">
            <div className={`text-xl font-bold ${c}`}>{v}</div>
            <div className="text-xs text-slate-500 mt-0.5">{l}</div>
          </div>
        ))}
      </div>

      <div className="bg-slate-900 border border-rose-500/30 rounded-xl p-5">
        <div className="grid grid-cols-4 gap-4">
          <GaugeRing value={summary.avg_exposure_score}    label="Exposure"    color="#ef4444"/>
          <GaugeRing value={summary.avg_detection_score}   label="Detection"   color="#f97316"/>
          <GaugeRing value={summary.avg_resilience_score}  label="Resilience"  color="#a855f7"/>
          <GaugeRing value={summary.avg_sovereignty_score} label="Sovereignty" color="#06b6d4"/>
        </div>
      </div>

      <div className="bg-slate-900 border border-rose-500/30 rounded-xl p-5 grid grid-cols-1 md:grid-cols-2 gap-5">
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
        {["all","none","narrative_capture","deepfake_assault","epistemic_collapse","bot_swarm_attack","trust_erosion"].map(p=>(
          <button key={p} onClick={()=>setPat(p)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${patFilter===p?"bg-red-900 border-red-800 text-white":"bg-slate-900 border-slate-700 text-slate-400 hover:text-white"}`}>
            {p.replace(/_/g," ")}
          </button>
        ))}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {filtered.map(t=>(
          <div key={t.target_id} onClick={()=>setSelected(t)}
            className="bg-slate-900 border border-rose-500/30 rounded-xl p-4 cursor-pointer hover:border-red-500 transition-colors">
            <div className="flex items-center justify-between mb-1">
              <span className="font-bold text-white">{t.target_id}</span>
              <span className="text-xs text-slate-400">{t.region}</span>
            </div>
            <div className="text-xs text-slate-500 mb-2 capitalize">{t.threat_domain.replace(/_/g," ")}</div>
            <div className="flex gap-1 mb-3 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[t.cognitive_warfare_risk as keyof typeof RISK_BADGE]||"bg-slate-700 text-slate-300"}`}>{t.cognitive_warfare_risk}</span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[t.cognitive_severity as keyof typeof SEV_BADGE]||"bg-slate-700 text-slate-300"}`}>{t.cognitive_severity}</span>
            </div>
            <div className="text-2xl font-black text-white mb-1">{t.cognitive_warfare_composite.toFixed(1)}</div>
            <div className="text-xs text-slate-500 mb-2 capitalize">{t.warfare_pattern.replace(/_/g," ")}</div>
            <div className="text-xs text-red-400 font-medium mb-2">Vuln: {t.estimated_cognitive_vulnerability_index.toFixed(2)}/10</div>
            <div className="flex gap-1 flex-wrap">
              {t.has_active_threat           && <span className="px-1.5 py-0.5 rounded bg-red-900 text-red-300 text-xs">THREAT</span>}
              {t.requires_immediate_response && <span className="px-1.5 py-0.5 rounded bg-rose-900 text-rose-300 text-xs">URGENT</span>}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
