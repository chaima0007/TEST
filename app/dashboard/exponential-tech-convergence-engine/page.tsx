"use client";
import { useEffect, useState } from "react";

type Entity = {
  id: string; region: string; tech_cluster: string;
  disruption_risk: string; disruption_pattern: string;
  disruption_severity: string; recommended_action: string;
  acceleration_score: number; displacement_score: number;
  concentration_score: number; sovereignty_score: number;
  disruption_composite: number; is_in_disruption_crisis: boolean;
  requires_disruption_intervention: boolean; disruption_signal: string;
};
type Summary = {
  total: number; risk_counts: Record<string,number>;
  pattern_counts: Record<string,number>; severity_counts: Record<string,number>;
  action_counts: Record<string,number>; avg_disruption_composite: number;
  disruption_crisis_count: number; disruption_intervention_count: number;
  avg_acceleration_score: number; avg_displacement_score: number;
  avg_concentration_score: number; avg_sovereignty_score: number;
  avg_estimated_disruption_index: number;
};

function GaugeRing({ value, label, color }: { value: number; label: string; color: string }) {
  const r = 36; const circ = 2 * Math.PI * r;
  const fill = circ * (1 - value / 100);
  return (
    <div className="flex flex-col items-center gap-1">
      <svg width="88" height="88" viewBox="0 0 88 88">
        <circle cx="44" cy="44" r={r} fill="none" stroke="#0c0a1a" strokeWidth="8"/>
        <circle cx="44" cy="44" r={r} fill="none" stroke={color} strokeWidth="8"
          strokeDasharray={circ} strokeDashoffset={fill}
          strokeLinecap="round" transform="rotate(-90 44 44)"/>
        <text x="44" y="49" textAnchor="middle" fill="white" fontSize="13" fontWeight="bold">
          {Math.round(value)}
        </text>
      </svg>
      <span className="text-xs text-fuchsia-300/70 text-center">{label}</span>
    </div>
  );
}

function DistBar({ title, counts, colors }: { title: string; counts: Record<string,number>; colors: Record<string,string> }) {
  const total = Object.values(counts).reduce((a, b) => a + b, 0) || 1;
  return (
    <div className="flex flex-col gap-1">
      <span className="text-xs text-fuchsia-300/70 font-medium">{title}</span>
      <div className="flex h-3 rounded overflow-hidden gap-px">
        {Object.entries(counts).map(([k, v]) => (
          <div key={k} style={{ width: `${(v / total) * 100}%`, background: colors[k] || "#475569" }} title={`${k}: ${v}`}/>
        ))}
      </div>
      <div className="flex flex-wrap gap-x-3 gap-y-0.5">
        {Object.entries(counts).map(([k, v]) => (
          <span key={k} className="text-xs text-fuchsia-300/60">
            <span style={{ color: colors[k] || "#94a3b8" }}>■</span> {k} {v}
          </span>
        ))}
      </div>
    </div>
  );
}

const RISK_COLORS = { low: "#10b981", moderate: "#f59e0b", high: "#38bdf8", critical: "#e879f9" };
const PAT_COLORS  = {
  none: "#10b981",
  convergence_singularity: "#e879f9",
  incumbent_collapse: "#38bdf8",
  platform_monopolization: "#a78bfa",
  sovereignty_vacuum: "#f59e0b",
  innovation_inequality_spiral: "#fb923c",
};
const SEV_COLORS  = {
  controlled_innovation: "#10b981",
  disruption_developing: "#f59e0b",
  high_disruption: "#38bdf8",
  exponential_rupture: "#e879f9",
};
const ACT_COLORS  = {
  no_action: "#10b981",
  tech_monitoring: "#06b6d4",
  disruption_hedging: "#f59e0b",
  singularity_preparedness: "#38bdf8",
  disruption_emergency_response: "#e879f9",
};
const RISK_BADGE  = {
  low: "bg-emerald-900 text-emerald-300",
  moderate: "bg-amber-900 text-amber-300",
  high: "bg-sky-900 text-sky-300",
  critical: "bg-fuchsia-950 text-fuchsia-300",
};
const SEV_BADGE   = {
  controlled_innovation: "bg-emerald-900 text-emerald-300",
  disruption_developing: "bg-amber-900 text-amber-300",
  high_disruption: "bg-sky-900 text-sky-300",
  exponential_rupture: "bg-fuchsia-950 text-fuchsia-300",
};

function DetailModal({ entity, onClose }: { entity: Entity; onClose: () => void }) {
  const [tab, setTab] = useState<"scores" | "signal" | "action">("scores");
  useEffect(() => {
    const h = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", h);
    return () => window.removeEventListener("keydown", h);
  }, [onClose]);
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80" onClick={onClose}>
      <div className="bg-slate-950 border border-sky-600/30 rounded-xl w-full max-w-lg p-6 shadow-2xl" onClick={e => e.stopPropagation()}>
        <div className="flex items-center justify-between mb-4">
          <div>
            <span className="text-lg font-bold text-white">{entity.id}</span>
            <span className="ml-2 text-fuchsia-400 text-xs">{entity.region}</span>
            <span className="ml-2 text-slate-500 text-xs">{entity.tech_cluster.replace(/_/g, " ")}</span>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl leading-none">✕</button>
        </div>
        <div className="flex gap-2 mb-4">
          {(["scores", "signal", "action"] as const).map(t => (
            <button key={t} onClick={() => setTab(t)}
              className={`px-3 py-1 rounded text-xs font-medium transition-colors ${tab === t ? "bg-fuchsia-900 text-white" : "bg-slate-900 text-slate-400 hover:text-white"}`}>
              {t.charAt(0).toUpperCase() + t.slice(1)}
            </button>
          ))}
        </div>
        {tab === "scores" && (
          <div className="grid grid-cols-2 gap-3 text-sm">
            {([
              ["Accélération",   entity.acceleration_score,  "#e879f9"],
              ["Déplacement",    entity.displacement_score,  "#38bdf8"],
              ["Concentration",  entity.concentration_score, "#a78bfa"],
              ["Souveraineté",   entity.sovereignty_score,   "#fb923c"],
            ] as [string, number, string][]).map(([l, v, c]) => (
              <div key={l} className="bg-slate-900 border border-sky-600/20 rounded-lg p-3">
                <div className="text-fuchsia-300/60 text-xs mb-1">{l}</div>
                <div className="text-white font-bold text-lg">{Number(v).toFixed(1)}</div>
                <div className="h-1.5 rounded mt-1 bg-slate-800">
                  <div className="h-1.5 rounded" style={{ width: `${Math.min(Number(v), 100)}%`, background: c }}/>
                </div>
              </div>
            ))}
            <div className="col-span-2 bg-slate-900 border border-sky-600/20 rounded-lg p-3">
              <div className="text-fuchsia-300/60 text-xs mb-1">Composite Disruption</div>
              <div className="text-white font-bold text-2xl">{entity.disruption_composite.toFixed(1)}</div>
            </div>
          </div>
        )}
        {tab === "signal" && (
          <div className="bg-slate-900 border border-sky-600/20 rounded-lg p-4 text-sm text-slate-200 leading-relaxed">
            {entity.disruption_signal}
            <div className="mt-3 flex gap-2 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[entity.disruption_risk as keyof typeof RISK_BADGE] || "bg-slate-700 text-slate-300"}`}>
                {entity.disruption_risk}
              </span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[entity.disruption_severity as keyof typeof SEV_BADGE] || "bg-slate-700 text-slate-300"}`}>
                {entity.disruption_severity.replace(/_/g, " ")}
              </span>
            </div>
          </div>
        )}
        {tab === "action" && (
          <div className="space-y-3 text-sm">
            <div className="bg-slate-900 border border-sky-600/20 rounded-lg p-3">
              <div className="text-fuchsia-300/60 text-xs mb-1">Action Recommandée</div>
              <div className="text-white font-medium">{entity.recommended_action.replace(/_/g, " ")}</div>
            </div>
            <div className="bg-slate-900 border border-sky-600/20 rounded-lg p-3">
              <div className="text-fuchsia-300/60 text-xs mb-1">Pattern Disruption</div>
              <div className="text-white font-medium">{entity.disruption_pattern.replace(/_/g, " ")}</div>
            </div>
            <div className="flex gap-2 flex-wrap">
              {entity.is_in_disruption_crisis && (
                <span className="px-2 py-1 rounded bg-fuchsia-950 text-fuchsia-300 text-xs font-medium">CRISE DISRUPTION</span>
              )}
              {entity.requires_disruption_intervention && (
                <span className="px-2 py-1 rounded bg-sky-950 text-sky-300 text-xs font-medium">INTERVENTION REQ.</span>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function ExponentialTechConvergenceDashboard() {
  const [data, setData]         = useState<{ entities: Entity[]; summary: Summary } | null>(null);
  const [filter, setFilter]     = useState<string>("all");
  const [patFilter, setPat]     = useState<string>("all");
  const [selected, setSelected] = useState<Entity | null>(null);

  useEffect(() => {
    fetch("/api/exponential-tech-convergence-engine")
      .then(r => r.json()).then(setData).catch(console.error);
  }, []);

  if (!data) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-fuchsia-400 text-lg animate-pulse">Initialisation du Moteur de Convergence Exponentielle...</div>
    </div>
  );

  const { entities, summary } = data;
  const filtered = entities.filter(e =>
    (filter === "all" || e.disruption_risk === filter) &&
    (patFilter === "all" || e.disruption_pattern === patFilter)
  );

  const dists = [
    { title: "Niveau Risque Disruption", counts: summary.risk_counts,    colors: RISK_COLORS },
    { title: "Pattern Convergence",      counts: summary.pattern_counts,  colors: PAT_COLORS  },
    { title: "Sévérité Disruption",      counts: summary.severity_counts, colors: SEV_COLORS  },
    { title: "Action Activée",           counts: summary.action_counts,   colors: ACT_COLORS  },
  ] as Array<{ title: string; counts: Record<string,number>; colors: Record<string,string> }>;

  const criticalCount = summary.risk_counts["critical"] || 0;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {selected && <DetailModal entity={selected} onClose={() => setSelected(null)}/>}

      <div>
        <h1 className="text-2xl font-bold text-fuchsia-400">Exponential Technology Convergence & Disruption Anticipation Engine</h1>
        <p className="text-fuchsia-300/50 text-sm mt-1">Accélération · Déplacement · Concentration · Souveraineté Technologique</p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {([
          ["Entités Analysées",             summary.total,                           "text-fuchsia-400"],
          ["Crises Disruption Critiques",   criticalCount,                           "text-fuchsia-500"],
          ["Composite Disruption Moy.",     `${summary.avg_disruption_composite.toFixed(1)}`, "text-sky-400"],
          ["Indice Disruption Moy.",        `${summary.avg_estimated_disruption_index.toFixed(2)}/10`, "text-violet-400"],
          ["En Crise Disruption",           summary.disruption_crisis_count,         "text-fuchsia-400"],
          ["Interventions Requises",        summary.disruption_intervention_count,   "text-sky-400"],
        ] as [string, string | number, string][]).map(([l, v, c]) => (
          <div key={l} className="bg-slate-900 border border-sky-600/30 rounded-xl p-3 text-center">
            <div className={`text-xl font-bold ${c}`}>{v}</div>
            <div className="text-xs text-fuchsia-300/40 mt-0.5 leading-tight">{l}</div>
          </div>
        ))}
      </div>

      {/* Gauge Rings */}
      <div className="bg-slate-900 border border-sky-600/30 rounded-xl p-5">
        <div className="grid grid-cols-4 gap-4">
          <GaugeRing value={summary.avg_acceleration_score}  label="Accélération Exponentielle"   color="#e879f9"/>
          <GaugeRing value={summary.avg_displacement_score}  label="Déplacement Incumbents"       color="#38bdf8"/>
          <GaugeRing value={summary.avg_concentration_score} label="Concentration Talents/Plates"  color="#a78bfa"/>
          <GaugeRing value={summary.avg_sovereignty_score}   label="Lacune Souveraineté Tech"     color="#fb923c"/>
        </div>
      </div>

      {/* Distribution Bars */}
      <div className="bg-slate-900 border border-sky-600/30 rounded-xl p-5 grid grid-cols-1 md:grid-cols-2 gap-5">
        {dists.map(d => <DistBar key={d.title} {...d}/>)}
      </div>

      {/* Filter Pills — risk */}
      <div className="flex flex-wrap gap-2">
        {["all", "low", "moderate", "high", "critical"].map(r => (
          <button key={r} onClick={() => setFilter(r)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${filter === r ? "bg-fuchsia-900 border-fuchsia-700 text-white" : "bg-slate-900 border-sky-600/30 text-fuchsia-400/70 hover:text-white"}`}>
            {r}
          </button>
        ))}
        <span className="w-px h-5 self-center bg-sky-600/30"/>
        {["all", "none", "convergence_singularity", "incumbent_collapse", "platform_monopolization", "sovereignty_vacuum", "innovation_inequality_spiral"].map(p => (
          <button key={p} onClick={() => setPat(p)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${patFilter === p ? "bg-sky-950 border-sky-700 text-white" : "bg-slate-900 border-sky-600/30 text-sky-400/70 hover:text-white"}`}>
            {p.replace(/_/g, " ")}
          </button>
        ))}
      </div>

      {/* Entity Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {filtered.map(e => (
          <div key={e.id} onClick={() => setSelected(e)}
            className="bg-slate-900 border border-sky-600/30 rounded-xl p-4 cursor-pointer hover:border-fuchsia-500 transition-colors">
            <div className="flex items-center justify-between mb-1">
              <span className="font-bold text-white">{e.id}</span>
              <span className="text-xs text-fuchsia-400/60">{e.region}</span>
            </div>
            <div className="text-xs text-slate-500 mb-2 capitalize">{e.tech_cluster.replace(/_/g, " ")}</div>
            <div className="flex gap-1 mb-3 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[e.disruption_risk as keyof typeof RISK_BADGE] || "bg-slate-700 text-slate-300"}`}>
                {e.disruption_risk}
              </span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[e.disruption_severity as keyof typeof SEV_BADGE] || "bg-slate-700 text-slate-300"}`}>
                {e.disruption_severity.replace(/_/g, " ")}
              </span>
            </div>
            <div className="text-2xl font-black text-white mb-1">{e.disruption_composite.toFixed(1)}</div>
            <div className="text-xs text-fuchsia-400/60 mb-2 capitalize">{e.disruption_pattern.replace(/_/g, " ")}</div>
            <div className="text-xs text-sky-400 font-medium mb-2">
              Acc: {e.acceleration_score.toFixed(1)} · Dép: {e.displacement_score.toFixed(1)}
            </div>
            <div className="flex gap-1 flex-wrap">
              {e.is_in_disruption_crisis && (
                <span className="px-1.5 py-0.5 rounded bg-fuchsia-950 text-fuchsia-400 text-xs">CRISE</span>
              )}
              {e.requires_disruption_intervention && (
                <span className="px-1.5 py-0.5 rounded bg-sky-950 text-sky-400 text-xs">INTERVENTION</span>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
