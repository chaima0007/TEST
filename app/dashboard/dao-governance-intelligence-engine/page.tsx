"use client";
import { useEffect, useState } from "react";

type Entity = {
  entity_id: string; region: string; dao_type: string;
  dao_risk: string; dao_pattern: string;
  dao_severity: string; recommended_action: string;
  participation_score: number; plutocracy_score: number;
  treasury_score: number; coordination_score: number;
  dao_composite: number; is_in_dao_crisis: boolean;
  requires_dao_intervention: boolean; dao_signal: string;
};
type Summary = {
  total: number; risk_counts: Record<string, number>;
  pattern_counts: Record<string, number>; severity_counts: Record<string, number>;
  action_counts: Record<string, number>; avg_dao_composite: number;
  dao_crisis_count: number; dao_intervention_count: number;
  avg_participation_score: number; avg_plutocracy_score: number;
  avg_treasury_score: number; avg_coordination_score: number;
  avg_estimated_dao_risk_index: number;
};

function GaugeRing({ value, label, color }: { value: number; label: string; color: string }) {
  const r = 36; const circ = 2 * Math.PI * r;
  const fill = circ * (1 - value / 100);
  return (
    <div className="flex flex-col items-center gap-1">
      <svg width="88" height="88" viewBox="0 0 88 88">
        <circle cx="44" cy="44" r={r} fill="none" stroke="#0a1a0f" strokeWidth="8"/>
        <circle cx="44" cy="44" r={r} fill="none" stroke={color} strokeWidth="8"
          strokeDasharray={circ} strokeDashoffset={fill}
          strokeLinecap="round" transform="rotate(-90 44 44)"/>
        <text x="44" y="49" textAnchor="middle" fill="white" fontSize="13" fontWeight="bold">
          {Math.round(value)}
        </text>
      </svg>
      <span className="text-xs text-emerald-300/70 text-center">{label}</span>
    </div>
  );
}

function DistBar({ title, counts, colors }: { title: string; counts: Record<string, number>; colors: Record<string, string> }) {
  const total = Object.values(counts).reduce((a, b) => a + b, 0) || 1;
  return (
    <div className="flex flex-col gap-1">
      <span className="text-xs text-emerald-300/70 font-medium">{title}</span>
      <div className="flex h-3 rounded overflow-hidden gap-px">
        {Object.entries(counts).map(([k, v]) => (
          <div key={k} style={{ width: `${v / total * 100}%`, background: colors[k] || "#475569" }} title={`${k}: ${v}`} />
        ))}
      </div>
      <div className="flex flex-wrap gap-x-3 gap-y-0.5">
        {Object.entries(counts).map(([k, v]) => (
          <span key={k} className="text-xs text-emerald-300/60">
            <span style={{ color: colors[k] || "#94a3b8" }}>■</span> {k.replace(/_/g, " ")} {v}
          </span>
        ))}
      </div>
    </div>
  );
}

const RISK_COLORS = { low: "#10b981", moderate: "#f59e0b", high: "#a855f7", critical: "#ef4444" };
const PAT_COLORS = {
  none: "#10b981",
  voter_apathy_collapse: "#6d28d9",
  plutocracy_takeover: "#ef4444",
  treasury_drain: "#f97316",
  fork_war: "#dc2626",
  sybil_governance_attack: "#7c3aed",
};
const SEV_COLORS = {
  dao_thriving: "#10b981",
  governance_stress: "#f59e0b",
  high_governance_failure: "#a855f7",
  dao_collapse: "#7f1d1d",
};
const ACT_COLORS = {
  no_action: "#10b981",
  dao_monitoring: "#06b6d4",
  governance_restructuring: "#a855f7",
  plutocracy_intervention: "#f97316",
  dao_emergency_governance: "#ef4444",
};
const RISK_BADGE = {
  low: "bg-emerald-900 text-emerald-300",
  moderate: "bg-amber-900 text-amber-300",
  high: "bg-purple-900 text-purple-300",
  critical: "bg-red-950 text-red-400",
};
const SEV_BADGE = {
  dao_thriving: "bg-emerald-900 text-emerald-300",
  governance_stress: "bg-amber-900 text-amber-300",
  high_governance_failure: "bg-purple-900 text-purple-300",
  dao_collapse: "bg-red-950 text-red-400",
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
      <div className="bg-slate-950 border border-purple-700/30 rounded-xl w-full max-w-lg p-6 shadow-2xl" onClick={e => e.stopPropagation()}>
        <div className="flex items-center justify-between mb-4">
          <div>
            <span className="text-lg font-bold text-white">{entity.entity_id}</span>
            <span className="ml-2 text-emerald-400 text-xs">{entity.region}</span>
            <span className="ml-2 text-slate-500 text-xs">{entity.dao_type.replace(/_/g, " ")}</span>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl leading-none">✕</button>
        </div>
        <div className="flex gap-2 mb-4">
          {(["scores", "signal", "action"] as const).map(t => (
            <button key={t} onClick={() => setTab(t)}
              className={`px-3 py-1 rounded text-xs font-medium transition-colors ${tab === t ? "bg-emerald-900 text-white" : "bg-slate-900 text-slate-400 hover:text-white"}`}>
              {t === "scores" ? "Scores" : t === "signal" ? "Signal" : "Action"}
            </button>
          ))}
        </div>
        {tab === "scores" && (
          <div className="grid grid-cols-2 gap-3 text-sm">
            {[
              ["Participation",   entity.participation_score,  "#6d28d9"],
              ["Plutocracie",     entity.plutocracy_score,     "#ef4444"],
              ["Trésorerie",      entity.treasury_score,       "#f97316"],
              ["Coordination",    entity.coordination_score,   "#06b6d4"],
            ].map(([l, v, c]) => (
              <div key={String(l)} className="bg-slate-900 border border-purple-700/20 rounded-lg p-3">
                <div className="text-emerald-300/60 text-xs mb-1">{String(l)}</div>
                <div className="text-white font-bold text-lg">{Number(v).toFixed(1)}</div>
                <div className="h-1.5 rounded mt-1 bg-slate-800">
                  <div className="h-1.5 rounded" style={{ width: `${Math.min(Number(v), 100)}%`, background: String(c) }} />
                </div>
              </div>
            ))}
            <div className="col-span-2 bg-slate-900 border border-purple-700/20 rounded-lg p-3">
              <div className="text-emerald-300/60 text-xs mb-1">Composite DAO</div>
              <div className="text-white font-bold text-2xl">{entity.dao_composite.toFixed(1)}</div>
            </div>
          </div>
        )}
        {tab === "signal" && (
          <div className="bg-slate-900 border border-purple-700/20 rounded-lg p-4 text-sm text-slate-200 leading-relaxed">
            {entity.dao_signal}
            <div className="mt-3 flex gap-2 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[entity.dao_risk as keyof typeof RISK_BADGE] || "bg-slate-700 text-slate-300"}`}>
                {entity.dao_risk}
              </span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[entity.dao_severity as keyof typeof SEV_BADGE] || "bg-slate-700 text-slate-300"}`}>
                {entity.dao_severity.replace(/_/g, " ")}
              </span>
            </div>
          </div>
        )}
        {tab === "action" && (
          <div className="space-y-3 text-sm">
            <div className="bg-slate-900 border border-purple-700/20 rounded-lg p-3">
              <div className="text-emerald-300/60 text-xs mb-1">Action Recommandée</div>
              <div className="text-white font-medium">{entity.recommended_action.replace(/_/g, " ")}</div>
            </div>
            <div className="bg-slate-900 border border-purple-700/20 rounded-lg p-3">
              <div className="text-emerald-300/60 text-xs mb-1">Pattern DAO</div>
              <div className="text-white font-medium">{entity.dao_pattern.replace(/_/g, " ")}</div>
            </div>
            <div className="flex gap-2 flex-wrap">
              {entity.is_in_dao_crisis && (
                <span className="px-2 py-1 rounded bg-red-950 text-red-400 text-xs font-medium">CRISE DAO</span>
              )}
              {entity.requires_dao_intervention && (
                <span className="px-2 py-1 rounded bg-purple-950 text-purple-400 text-xs font-medium">INTERVENTION REQ.</span>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function DAOGovernanceDashboard() {
  const [data, setData]         = useState<{ entities: Entity[]; summary: Summary } | null>(null);
  const [filter, setFilter]     = useState<string>("all");
  const [patFilter, setPat]     = useState<string>("all");
  const [selected, setSelected] = useState<Entity | null>(null);

  useEffect(() => {
    fetch("/api/dao-governance-intelligence-engine")
      .then(r => r.json()).then(setData).catch(console.error);
  }, []);

  if (!data) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-emerald-400 text-lg animate-pulse">Initialisation du Moteur de Gouvernance DAO...</div>
    </div>
  );

  const { entities, summary } = data;
  const filtered = entities.filter(e =>
    (filter === "all" || e.dao_risk === filter) &&
    (patFilter === "all" || e.dao_pattern === patFilter)
  );

  const dists = [
    { title: "Niveau de Risque DAO",      counts: summary.risk_counts,     colors: RISK_COLORS },
    { title: "Pattern de Gouvernance",     counts: summary.pattern_counts,  colors: PAT_COLORS  },
    { title: "Sévérité DAO",              counts: summary.severity_counts, colors: SEV_COLORS  },
    { title: "Action Recommandée",         counts: summary.action_counts,   colors: ACT_COLORS  },
  ] as Array<{ title: string; counts: Record<string, number>; colors: Record<string, string> }>;

  const criticalCount = summary.risk_counts["critical"] || 0;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {selected && <DetailModal entity={selected} onClose={() => setSelected(null)} />}

      <div>
        <h1 className="text-2xl font-bold text-emerald-400">DAO Governance Intelligence Engine</h1>
        <p className="text-emerald-300/50 text-sm mt-1">
          Participation · Plutocracy · Trésorerie · Coordination · Santé de Gouvernance
        </p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {[
          ["Entités Analysées",          summary.total,                                        "text-emerald-400"],
          ["DAO en Crise Critique",       criticalCount,                                        "text-red-400"],
          ["Composite DAO Moy.",          `${summary.avg_dao_composite.toFixed(1)}`,            "text-purple-400"],
          ["Crises DAO Actives",          summary.dao_crisis_count,                             "text-red-400"],
          ["Interventions Requises",      summary.dao_intervention_count,                       "text-purple-400"],
          ["Indice Risque DAO Moy.",      `${summary.avg_estimated_dao_risk_index.toFixed(2)}/10`, "text-emerald-400"],
        ].map(([l, v, c]) => (
          <div key={String(l)} className="bg-slate-900 border border-purple-700/30 rounded-xl p-3 text-center">
            <div className={`text-xl font-bold ${c}`}>{v}</div>
            <div className="text-xs text-emerald-300/40 mt-0.5 leading-tight">{l}</div>
          </div>
        ))}
      </div>

      {/* Gauge Rings */}
      <div className="bg-slate-900 border border-purple-700/30 rounded-xl p-5">
        <div className="grid grid-cols-4 gap-4">
          <GaugeRing value={summary.avg_participation_score} label="Apathie Participation"    color="#6d28d9"/>
          <GaugeRing value={summary.avg_plutocracy_score}    label="Risque Plutocracie"       color="#ef4444"/>
          <GaugeRing value={summary.avg_treasury_score}      label="Tension Trésorerie"       color="#f97316"/>
          <GaugeRing value={summary.avg_coordination_score}  label="Déficit Coordination"     color="#06b6d4"/>
        </div>
      </div>

      {/* Distribution Bars */}
      <div className="bg-slate-900 border border-purple-700/30 rounded-xl p-5 grid grid-cols-1 md:grid-cols-2 gap-5">
        {dists.map(d => <DistBar key={d.title} {...d} />)}
      </div>

      {/* Filter Pills */}
      <div className="flex flex-wrap gap-2">
        {["all", "low", "moderate", "high", "critical"].map(r => (
          <button key={r} onClick={() => setFilter(r)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${filter === r ? "bg-emerald-900 border-emerald-700 text-white" : "bg-slate-900 border-purple-700/30 text-emerald-400/70 hover:text-white"}`}>
            {r}
          </button>
        ))}
        <span className="w-px h-5 self-center bg-purple-700/30" />
        {["all", "none", "voter_apathy_collapse", "plutocracy_takeover", "treasury_drain", "fork_war", "sybil_governance_attack"].map(p => (
          <button key={p} onClick={() => setPat(p)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${patFilter === p ? "bg-purple-950 border-purple-700 text-white" : "bg-slate-900 border-purple-700/30 text-emerald-400/70 hover:text-white"}`}>
            {p.replace(/_/g, " ")}
          </button>
        ))}
      </div>

      {/* Entity Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {filtered.map(e => (
          <div key={e.entity_id} onClick={() => setSelected(e)}
            className="bg-slate-900 border border-purple-700/30 rounded-xl p-4 cursor-pointer hover:border-emerald-500 transition-colors">
            <div className="flex items-center justify-between mb-1">
              <span className="font-bold text-white">{e.entity_id}</span>
              <span className="text-xs text-emerald-400/60">{e.region}</span>
            </div>
            <div className="text-xs text-slate-500 mb-2 capitalize">{e.dao_type.replace(/_/g, " ")}</div>
            <div className="flex gap-1 mb-3 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[e.dao_risk as keyof typeof RISK_BADGE] || "bg-slate-700 text-slate-300"}`}>
                {e.dao_risk}
              </span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[e.dao_severity as keyof typeof SEV_BADGE] || "bg-slate-700 text-slate-300"}`}>
                {e.dao_severity.replace(/_/g, " ")}
              </span>
            </div>
            <div className="text-2xl font-black text-white mb-1">{e.dao_composite.toFixed(1)}</div>
            <div className="text-xs text-purple-400/70 mb-2 capitalize">{e.dao_pattern.replace(/_/g, " ")}</div>
            <div className="text-xs text-emerald-400 font-medium mb-2">
              {e.recommended_action.replace(/_/g, " ")}
            </div>
            <div className="flex gap-1 flex-wrap">
              {e.is_in_dao_crisis && (
                <span className="px-1.5 py-0.5 rounded bg-red-950 text-red-400 text-xs">CRISE</span>
              )}
              {e.requires_dao_intervention && (
                <span className="px-1.5 py-0.5 rounded bg-purple-950 text-purple-400 text-xs">INTERVENTION</span>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
