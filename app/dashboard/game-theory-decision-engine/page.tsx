"use client";
import { useEffect, useState } from "react";

type Game = {
  game_id: string;
  game_type: string;
  region: string;
  stability_score: number;
  strategy_score: number;
  cooperation_score: number;
  information_score: number;
  game_composite: number;
  game_risk: string;
  game_pattern: string;
  game_severity: string;
  recommended_action: string;
  recommended_action_secondary: string;
  game_signal: string;
  estimated_game_loss_index: number;
};

type Summary = {
  total: number;
  risk_counts: Record<string,number>;
  pattern_counts: Record<string,number>;
  severity_counts: Record<string,number>;
  action_counts: Record<string,number>;
  avg_game_composite: number;
  destructive_count: number;
  mediation_required_count: number;
  avg_stability_score: number;
  avg_strategy_score: number;
  avg_cooperation_score: number;
  avg_information_score: number;
  avg_estimated_game_loss_index: number;
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
const PAT_COLORS    = { none:"#10b981", prisoners_dilemma_trap:"#ef4444", nash_deadlock:"#dc2626", defection_cascade:"#f97316", information_warfare:"#a855f7", zero_sum_destruction:"#7f1d1d" };
const SEV_COLORS    = { optimal:"#10b981", negotiating:"#f59e0b", unstable:"#f97316", destructive:"#ef4444" };
const ACT_COLORS    = { no_action:"#10b981", strategy_monitoring:"#06b6d4", commitment_device:"#3b82f6", coalition_building:"#a855f7", emergency_mediation:"#ef4444", game_reset:"#7f1d1d" };
const RISK_BADGE    = { low:"bg-emerald-900 text-emerald-300", moderate:"bg-amber-900 text-amber-300", high:"bg-orange-900 text-orange-300", critical:"bg-red-900 text-red-300" };
const SEV_BADGE     = { optimal:"bg-emerald-900 text-emerald-300", negotiating:"bg-amber-900 text-amber-300", unstable:"bg-orange-900 text-orange-300", destructive:"bg-red-900 text-red-300" };

function DetailModal({ game, onClose }: { game: Game; onClose: () => void }) {
  const [tab, setTab] = useState<"scores"|"signal"|"action">("scores");
  useEffect(() => {
    const h = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", h);
    return () => window.removeEventListener("keydown", h);
  }, [onClose]);
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70" onClick={onClose}>
      <div className="bg-slate-900 border border-slate-700 rounded-xl w-full max-w-lg p-6 shadow-2xl" onClick={e=>e.stopPropagation()}>
        <div className="flex items-center justify-between mb-4">
          <div>
            <span className="text-lg font-bold text-white">{game.game_id}</span>
            <span className="ml-2 text-emerald-400 text-xs">{game.game_type.replace(/_/g," ")}</span>
            <span className="ml-2 text-teal-400 text-xs">{game.region}</span>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl leading-none">✕</button>
        </div>
        <div className="flex gap-2 mb-4">
          {(["scores","signal","action"] as const).map(t=>(
            <button key={t} onClick={()=>setTab(t)}
              className={`px-3 py-1 rounded text-xs font-medium transition-colors ${tab===t?"bg-emerald-700 text-white":"bg-slate-800 text-slate-400 hover:text-white"}`}>
              {t.charAt(0).toUpperCase()+t.slice(1)}
            </button>
          ))}
        </div>
        {tab==="scores" && (
          <div className="grid grid-cols-2 gap-3 text-sm">
            {[
              ["Stabilité",    game.stability_score,    "#10b981"],
              ["Stratégie",    game.strategy_score,     "#f97316"],
              ["Coopération",  game.cooperation_score,  "#06b6d4"],
              ["Information",  game.information_score,  "#a855f7"],
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
              <div className="text-slate-400 text-xs mb-1">Composite Jeu</div>
              <div className="text-white font-bold text-2xl">{game.game_composite.toFixed(1)}</div>
            </div>
          </div>
        )}
        {tab==="signal" && (
          <div className="bg-slate-800 rounded-lg p-4 text-sm text-slate-200 leading-relaxed">
            {game.game_signal}
            <div className="mt-3 flex gap-2 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[game.game_risk as keyof typeof RISK_BADGE]||"bg-slate-700 text-slate-300"}`}>{game.game_risk}</span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[game.game_severity as keyof typeof SEV_BADGE]||"bg-slate-700 text-slate-300"}`}>{game.game_severity}</span>
            </div>
          </div>
        )}
        {tab==="action" && (
          <div className="space-y-3 text-sm">
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Action Principale</div>
              <div className="text-white font-medium">{game.recommended_action.replace(/_/g," ")}</div>
            </div>
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Action Secondaire</div>
              <div className="text-white font-medium">{game.recommended_action_secondary.replace(/_/g," ")}</div>
            </div>
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Indice de Perte Estimée</div>
              <div className="text-white font-bold">{game.estimated_game_loss_index.toFixed(2)} / 10</div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function GameTheoryDashboard() {
  const [data, setData]         = useState<{ games: Game[]; summary: Summary }|null>(null);
  const [filter, setFilter]     = useState<string>("all");
  const [patFilter, setPat]     = useState<string>("all");
  const [selected, setSelected] = useState<Game|null>(null);

  useEffect(()=>{
    fetch("/api/game-theory-decision-engine")
      .then(r=>r.json()).then(setData).catch(console.error);
  },[]);

  if (!data) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-emerald-400 text-lg animate-pulse">Loading Game Theory Engine...</div>
    </div>
  );

  const { games, summary } = data;
  const filtered = games.filter(g=>
    (filter==="all" || g.game_risk===filter) &&
    (patFilter==="all" || g.game_pattern===patFilter)
  );

  const dists = [
    { title:"Risque Décision",        counts:summary.risk_counts,     colors:RISK_COLORS },
    { title:"Pattern Jeu",            counts:summary.pattern_counts,  colors:PAT_COLORS  },
    { title:"Sévérité Équilibre",     counts:summary.severity_counts, colors:SEV_COLORS  },
    { title:"Action Recommandée",     counts:summary.action_counts,   colors:ACT_COLORS  },
  ] as Array<{title:string;counts:Record<string,number>;colors:Record<string,string>}>;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {selected && <DetailModal game={selected} onClose={()=>setSelected(null)}/>}

      <div>
        <h1 className="text-2xl font-bold text-white">Dynamic Game Theory &amp; Decision Engineering</h1>
        <p className="text-slate-400 text-sm mt-1">Nash Equilibrium · Stratégie Dominante · Coopération · Information — optimisation des décisions multi-agents</p>
      </div>

      {/* KPI strip — 6 cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {[
          ["Total Jeux",          summary.total,                                              "text-emerald-400"],
          ["Destructifs",         summary.destructive_count,                                  "text-red-400"],
          ["Médiations Req.",     summary.mediation_required_count,                           "text-orange-400"],
          ["Composite Moyen",     summary.avg_game_composite,                                 "text-teal-400"],
          ["Stabilité Nash",      `${Math.round(summary.avg_stability_score)}`,               "text-emerald-400"],
          ["Coopération Moy.",    `${Math.round(summary.avg_cooperation_score)}`,             "text-teal-400"],
        ].map(([l,v,c])=>(
          <div key={String(l)} className="bg-slate-900 border border-slate-800 rounded-xl p-3 text-center">
            <div className={`text-xl font-bold ${c}`}>{v}</div>
            <div className="text-xs text-slate-500 mt-0.5">{l}</div>
          </div>
        ))}
      </div>

      {/* 4 SVG gauge rings */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
        <div className="grid grid-cols-4 gap-4">
          <Gauge value={summary.avg_stability_score}   label="Stabilité Nash"       color="#10b981"/>
          <Gauge value={summary.avg_strategy_score}    label="Clarté Stratégie"     color="#f97316"/>
          <Gauge value={summary.avg_cooperation_score} label="Potentiel Coopération" color="#06b6d4"/>
          <Gauge value={summary.avg_information_score} label="Qualité Information"   color="#a855f7"/>
        </div>
      </div>

      {/* 4 DistBar distributions */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 grid grid-cols-1 md:grid-cols-2 gap-5">
        {dists.map(d=><DistBar key={d.title} {...d}/>)}
      </div>

      {/* Filter pills — risk + pattern */}
      <div className="flex flex-wrap gap-2">
        {["all","low","moderate","high","critical"].map(r=>(
          <button key={r} onClick={()=>setFilter(r)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${filter===r?"bg-emerald-700 border-emerald-600 text-white":"bg-slate-900 border-slate-700 text-slate-400 hover:text-white"}`}>
            {r}
          </button>
        ))}
        <span className="w-px h-5 self-center bg-slate-700"/>
        {["all","prisoners_dilemma_trap","nash_deadlock","defection_cascade","information_warfare","zero_sum_destruction","none"].map(p=>(
          <button key={p} onClick={()=>setPat(p)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${patFilter===p?"bg-teal-900 border-teal-800 text-white":"bg-slate-900 border-slate-700 text-slate-400 hover:text-white"}`}>
            {p.replace(/_/g," ")}
          </button>
        ))}
      </div>

      {/* Entity cards grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {filtered.map(g=>(
          <div key={g.game_id} onClick={()=>setSelected(g)}
            className="bg-slate-900 border border-slate-800 rounded-xl p-4 cursor-pointer hover:border-emerald-700 transition-colors">
            <div className="flex items-center justify-between mb-1">
              <span className="font-bold text-white">{g.game_id}</span>
              <span className="text-xs text-slate-400">{g.region}</span>
            </div>
            <div className="text-xs text-teal-400 mb-2 capitalize">{g.game_type.replace(/_/g," ")}</div>
            <div className="flex gap-1 mb-3 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[g.game_risk as keyof typeof RISK_BADGE]||"bg-slate-700 text-slate-300"}`}>{g.game_risk}</span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[g.game_severity as keyof typeof SEV_BADGE]||"bg-slate-700 text-slate-300"}`}>{g.game_severity}</span>
            </div>
            <div className="text-2xl font-black text-white mb-1">{g.game_composite.toFixed(1)}</div>
            <div className="text-xs text-slate-500 mb-2 capitalize">{g.game_pattern.replace(/_/g," ")}</div>
            <div className="text-xs text-emerald-400 font-medium mb-2">Perte: {g.estimated_game_loss_index.toFixed(2)}/10</div>
            <div className="text-xs text-slate-400 line-clamp-2 leading-relaxed">{g.game_signal}</div>
          </div>
        ))}
      </div>
    </div>
  );
}
