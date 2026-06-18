"use client";

import { useEffect, useState, useCallback } from "react";

interface Rep {
  rep_id: string; region: string; obj_risk: string; obj_pattern: string;
  obj_severity: string; recommended_action: string;
  resolution_effectiveness_score: number; objection_intelligence_score: number;
  resilience_score: number; evidence_utilization_score: number;
  obj_composite: number; has_obj_gap: boolean; requires_obj_coaching: boolean;
  estimated_deal_loss_usd: number; obj_signal: string;
}
interface Summary {
  total: number; risk_counts: Record<string,number>; pattern_counts: Record<string,number>;
  severity_counts: Record<string,number>; action_counts: Record<string,number>;
  avg_obj_composite: number; obj_gap_count: number; coaching_count: number;
  avg_resolution_effectiveness_score: number; avg_objection_intelligence_score: number;
  avg_resilience_score: number; avg_evidence_utilization_score: number;
  total_estimated_deal_loss_usd: number;
}
interface ApiResponse { reps: Rep[]; summary: Summary; }

const RC: Record<string,string> = { low:"text-emerald-400",moderate:"text-yellow-400",high:"text-orange-400",critical:"text-red-400" };
const RB: Record<string,string> = { low:"bg-emerald-400/10 border-emerald-400/30",moderate:"bg-yellow-400/10 border-yellow-400/30",high:"bg-orange-400/10 border-orange-400/30",critical:"bg-red-400/10 border-red-400/30" };

function fmt(n:number){if(n>=1e6)return`$${(n/1e6).toFixed(1)}M`;if(n>=1e3)return`$${(n/1e3).toFixed(0)}K`;return`$${n.toFixed(0)}`;}

function GaugeRing({value,label,color}:{value:number;label:string;color:string}){
  const r=36,circ=2*Math.PI*r,dash=(value/100)*circ;
  return(<div className="flex flex-col items-center gap-1"><svg width="90" height="90" viewBox="0 0 90 90"><circle cx="45" cy="45" r={r} fill="none" stroke="#1e293b" strokeWidth="8"/><circle cx="45" cy="45" r={r} fill="none" stroke={color} strokeWidth="8" strokeDasharray={`${dash} ${circ}`} strokeLinecap="round" transform="rotate(-90 45 45)"/><text x="45" y="50" textAnchor="middle" fontSize="13" fontWeight="700" fill="white">{Math.round(value)}</text></svg><span className="text-[10px] text-slate-400 text-center leading-tight">{label}</span></div>);
}

function DistBar({title,counts,colors}:{title:string;counts:Record<string,number>;colors:Record<string,string>}){
  const total=Object.values(counts).reduce((a,b)=>a+b,0)||1;
  return(<div className="space-y-2"><p className="text-xs text-slate-400 font-medium">{title}</p><div className="flex rounded overflow-hidden h-3">{Object.entries(counts).map(([k,v])=>(<div key={k} style={{width:`${(v/total)*100}%`,background:colors[k]??"#475569"}} title={`${k}: ${v}`}/>))}</div><div className="flex flex-wrap gap-x-3 gap-y-1">{Object.entries(counts).map(([k,v])=>(<span key={k} className="text-[10px] text-slate-400"><span style={{color:colors[k]??"#94a3b8"}}>■</span> {k} ({v})</span>))}</div></div>);
}

function DetailModal({rep,onClose}:{rep:Rep;onClose:()=>void}){
  const[tab,setTab]=useState<"scores"|"signal"|"action">("scores");
  useEffect(()=>{const h=(e:KeyboardEvent)=>{if(e.key==="Escape")onClose();};window.addEventListener("keydown",h);return()=>window.removeEventListener("keydown",h);},[onClose]);
  const scores=[{label:"Resolution Effectiveness",value:rep.resolution_effectiveness_score},{label:"Objection Intelligence",value:rep.objection_intelligence_score},{label:"Resilience",value:rep.resilience_score},{label:"Evidence Utilization",value:rep.evidence_utilization_score}];
  return(<div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 p-4" onClick={onClose}><div className="bg-slate-900 border border-slate-700 rounded-xl w-full max-w-lg p-6 space-y-4" onClick={e=>e.stopPropagation()}><div className="flex items-center justify-between"><div><h2 className="text-white font-bold text-lg">{rep.rep_id}</h2><p className="text-slate-400 text-sm">{rep.region}</p></div><button onClick={onClose} className="text-slate-400 hover:text-white text-xl">✕</button></div><div className="flex gap-2">{(["scores","signal","action"] as const).map(t=>(<button key={t} onClick={()=>setTab(t)} className={`px-3 py-1 rounded text-xs font-medium transition-colors ${tab===t?"bg-orange-600 text-white":"bg-slate-800 text-slate-400 hover:text-white"}`}>{t.charAt(0).toUpperCase()+t.slice(1)}</button>))}</div>{tab==="scores"&&(<div className="space-y-3">{scores.map(({label,value})=>(<div key={label}><div className="flex justify-between text-xs mb-1"><span className="text-slate-300">{label}</span><span className="text-white font-medium">{value.toFixed(1)}</span></div><div className="h-2 bg-slate-800 rounded-full overflow-hidden"><div className="h-full bg-orange-500 rounded-full transition-all" style={{width:`${value}%`}}/></div></div>))}<div className="pt-2 border-t border-slate-700 flex justify-between text-xs"><span className="text-slate-400">Composite</span><span className={`font-bold ${RC[rep.obj_risk]}`}>{rep.obj_composite.toFixed(1)}</span></div></div>)}{tab==="signal"&&(<div className="space-y-3"><p className="text-slate-300 text-sm leading-relaxed">{rep.obj_signal}</p><div className="grid grid-cols-2 gap-2 text-xs"><div className="bg-slate-800 rounded p-2"><p className="text-slate-500">Pattern</p><p className="text-white font-medium">{rep.obj_pattern.replace(/_/g," ")}</p></div><div className="bg-slate-800 rounded p-2"><p className="text-slate-500">Severity</p><p className="text-white font-medium">{rep.obj_severity}</p></div><div className="bg-slate-800 rounded p-2"><p className="text-slate-500">Deal Loss</p><p className="text-white font-medium">{fmt(rep.estimated_deal_loss_usd)}</p></div><div className="bg-slate-800 rounded p-2"><p className="text-slate-500">Risk</p><p className={`font-medium ${RC[rep.obj_risk]}`}>{rep.obj_risk}</p></div></div></div>)}{tab==="action"&&(<div className="space-y-3"><div className="bg-slate-800 rounded-lg p-3"><p className="text-slate-400 text-xs mb-1">Recommended Action</p><p className="text-white font-semibold text-sm">{rep.recommended_action.replace(/_/g," ")}</p></div><div className="flex gap-2 text-xs">{rep.has_obj_gap&&(<span className="px-2 py-1 rounded bg-orange-500/20 border border-orange-500/40 text-orange-300">🛡️ GAP</span>)}{rep.requires_obj_coaching&&(<span className="px-2 py-1 rounded bg-amber-500/20 border border-amber-500/40 text-amber-300">🎯 COACH</span>)}</div></div>)}</div></div>);
}

export default function SalesObjectionHandlingPage(){
  const[data,setData]=useState<ApiResponse|null>(null);
  const[loading,setLoading]=useState(true);
  const[riskFilter,setRiskFilter]=useState("all");
  const[patternFilter,setPatternFilter]=useState("all");
  const[selected,setSelected]=useState<Rep|null>(null);
  const load=useCallback(async()=>{setLoading(true);const p=new URLSearchParams();if(riskFilter!=="all")p.set("risk",riskFilter);if(patternFilter!=="all")p.set("pattern",patternFilter);const res=await fetch(`/api/sales-objection-handling-intelligence-engine?${p}`);setData(await res.json());setLoading(false);},[riskFilter,patternFilter]);
  useEffect(()=>{load();},[load]);
  const s=data?.summary;
  const riskColors={low:"#34d399",moderate:"#facc15",high:"#fb923c",critical:"#f87171"};
  const patternColors={none:"#64748b",price_caver:"#f87171",status_quo_deflector:"#fb923c",feature_objector:"#facc15",authority_blocker:"#a78bfa",timing_deferrer:"#38bdf8"};
  const severityColors={expert:"#34d399",competent:"#818cf8",developing:"#fb923c",struggling:"#f87171"};
  const actionColors={no_action:"#64748b",price_objection_coaching:"#f87171",reframe_coaching:"#fb923c",feature_gap_coaching:"#facc15",multi_threading_coaching:"#a78bfa",urgency_creation_coaching:"#38bdf8",objection_handling_intervention:"#f43f5e"};
  const distributions=[{title:"Risk Distribution",counts:s?.risk_counts??{},colors:riskColors},{title:"Pattern Distribution",counts:s?.pattern_counts??{},colors:patternColors},{title:"Severity Distribution",counts:s?.severity_counts??{},colors:severityColors},{title:"Action Distribution",counts:s?.action_counts??{},colors:actionColors}] as Array<{title:string;counts:Record<string,number>;colors:Record<string,string>}>;
  const RISKS=["all","low","moderate","high","critical"];
  const PATTERNS=["all","none","price_caver","status_quo_deflector","feature_objector","authority_blocker","timing_deferrer"];
  return(<div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6"><div><h1 className="text-2xl font-bold text-white">Sales Objection Handling Intelligence Engine</h1><p className="text-slate-400 text-sm mt-1">Resolution rate · Reframe quality · Resilience · Evidence use</p></div><div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">{[{label:"Total Reps",value:s?.total??"—"},{label:"Avg Composite",value:s?.avg_obj_composite?.toFixed(1)??"—"},{label:"Obj Gaps",value:s?.obj_gap_count??"—"},{label:"Need Coaching",value:s?.coaching_count??"—"},{label:"Deal Loss",value:s?fmt(s.total_estimated_deal_loss_usd):"—"},{label:"Avg Resolution",value:s?.avg_resolution_effectiveness_score?.toFixed(1)??"—"}].map(({label,value})=>(<div key={label} className="bg-slate-900 border border-slate-800 rounded-lg p-3 text-center"><p className="text-slate-400 text-xs">{label}</p><p className="text-white font-bold text-lg mt-1">{value}</p></div>))}</div><div className="bg-slate-900 border border-slate-800 rounded-xl p-5"><h2 className="text-sm font-semibold text-slate-300 mb-4">Average Sub-Scores</h2><div className="flex flex-wrap justify-around gap-6"><GaugeRing value={s?.avg_resolution_effectiveness_score??0} label="Resolution" color="#fb923c"/><GaugeRing value={s?.avg_objection_intelligence_score??0} label="Obj Intelligence" color="#a78bfa"/><GaugeRing value={s?.avg_resilience_score??0} label="Resilience" color="#38bdf8"/><GaugeRing value={s?.avg_evidence_utilization_score??0} label="Evidence Use" color="#34d399"/></div></div><div className="bg-slate-900 border border-slate-800 rounded-xl p-5 grid grid-cols-1 md:grid-cols-2 gap-5">{distributions.map(d=><DistBar key={d.title} {...d}/>)}</div><div className="space-y-3"><div className="flex flex-wrap gap-2"><span className="text-slate-400 text-xs self-center">Risk:</span>{RISKS.map(r=>(<button key={r} onClick={()=>setRiskFilter(r)} className={`px-3 py-1 rounded text-xs font-medium transition-colors ${riskFilter===r?"bg-orange-600 text-white":"bg-slate-800 text-slate-400 hover:text-white"}`}>{r}</button>))}</div><div className="flex flex-wrap gap-2"><span className="text-slate-400 text-xs self-center">Pattern:</span>{PATTERNS.map(p=>(<button key={p} onClick={()=>setPatternFilter(p)} className={`px-3 py-1 rounded text-xs font-medium transition-colors ${patternFilter===p?"bg-orange-600 text-white":"bg-slate-800 text-slate-400 hover:text-white"}`}>{p.replace(/_/g," ")}</button>))}</div></div>{loading?(<p className="text-slate-400 text-sm">Loading...</p>):(<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">{data?.reps.map(rep=>(<div key={rep.rep_id} onClick={()=>setSelected(rep)} className={`bg-slate-900 border rounded-lg p-4 cursor-pointer hover:border-orange-500 transition-colors ${RB[rep.obj_risk]}`}><div className="flex justify-between items-start mb-2"><div><p className="text-white font-semibold text-sm">{rep.rep_id}</p><p className="text-slate-400 text-xs">{rep.region}</p></div><span className={`text-xs font-bold px-2 py-0.5 rounded ${RC[rep.obj_risk]} bg-slate-800`}>{rep.obj_composite.toFixed(0)}</span></div><p className="text-slate-300 text-xs mb-2">{rep.obj_pattern.replace(/_/g," ")}</p><div className="flex gap-1 flex-wrap">{rep.has_obj_gap&&(<span className="text-[10px] px-1.5 py-0.5 rounded bg-orange-500/20 text-orange-300 border border-orange-500/30">🛡️ GAP</span>)}{rep.requires_obj_coaching&&(<span className="text-[10px] px-1.5 py-0.5 rounded bg-amber-500/20 text-amber-300 border border-amber-500/30">🎯 COACH</span>)}</div>{rep.estimated_deal_loss_usd>0&&(<p className="text-slate-500 text-[10px] mt-2">{fmt(rep.estimated_deal_loss_usd)} deal loss</p>)}</div>))}</div>)}{selected&&<DetailModal rep={selected} onClose={()=>setSelected(null)}/>}</div>);
}
