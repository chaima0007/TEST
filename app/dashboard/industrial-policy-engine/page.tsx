"use client";
import { useEffect, useState } from "react";

type Entity = {
  entity_id: string;
  industrial_sector: string;
  region: string;
  dependency_score: number;
  policy_score: number;
  resilience_score: number;
  geopolitical_score: number;
  composite_score: number;
  risk_level: string;
  industrial_pattern: string;
  severity: string;
  recommended_action: string;
  signal: string;
  strategic_dependency_exposure: number;
  semiconductor_dependency: number;
};

type Summary = {
  module_id: number;
  module_name: string;
  total: number;
  critical: number;
  high: number;
  moderate: number;
  low: number;
  avg_composite: number;
  risk_distribution: Record<string, number>;
  pattern_distribution: Record<string, number>;
  severity_distribution: Record<string, number>;
  action_distribution: Record<string, number>;
  avg_estimated_reshoring_index: number;
};

function GaugeRing({ value, label, color }: { value: number; label: string; color: string }) {
  const r = 36;
  const circ = 2 * Math.PI * r;
  const fill = circ * (1 - value / 100);
  return (
    <div className="flex flex-col items-center gap-1">
      <svg width="88" height="88" viewBox="0 0 88 88">
        <circle cx="44" cy="44" r={r} fill="none" stroke="#0c0a1a" strokeWidth="8" />
        <circle
          cx="44" cy="44" r={r} fill="none" stroke={color} strokeWidth="8"
          strokeDasharray={circ} strokeDashoffset={fill}
          strokeLinecap="round" transform="rotate(-90 44 44)"
        />
        <text x="44" y="49" textAnchor="middle" fill="white" fontSize="13" fontWeight="bold">
          {Math.round(value)}
        </text>
      </svg>
      <span className="text-xs text-blue-300/70 text-center">{label}</span>
    </div>
  );
}

function DistBar({ title, counts, colors }: { title: string; counts: Record<string, number>; colors: Record<string, string> }) {
  const total = Object.values(counts).reduce((a, b) => a + b, 0) || 1;
  return (
    <div className="flex flex-col gap-1">
      <span className="text-xs text-blue-300/70 font-medium">{title}</span>
      <div className="flex h-3 rounded overflow-hidden gap-px">
        {Object.entries(counts).map(([k, v]) => (
          <div
            key={k}
            style={{ width: `${(v / total) * 100}%`, background: colors[k] || "#475569" }}
            title={`${k}: ${v}`}
          />
        ))}
      </div>
      <div className="flex flex-wrap gap-x-3 gap-y-0.5">
        {Object.entries(counts).map(([k, v]) => (
          <span key={k} className="text-xs text-blue-300/60">
            <span style={{ color: colors[k] || "#94a3b8" }}>■</span> {k.replace(/_/g, " ")} {v}
          </span>
        ))}
      </div>
    </div>
  );
}

const RISK_COLORS: Record<string, string> = { low: "#10b981", moderate: "#f59e0b", high: "#d97706", critical: "#ef4444" };
const PAT_COLORS: Record<string, string> = {
  none: "#10b981",
  strategic_dependency_crisis: "#ef4444",
  subsidy_trade_war_escalation: "#d97706",
  reshoring_policy_failure: "#7c3aed",
  pharmaceutical_supply_collapse: "#1d4ed8",
  green_manufacturing_gap_crisis: "#059669",
};
const SEV_COLORS: Record<string, string> = {
  "politique_industrielle_gérée": "#10b981",
  "restructuration_industrielle_active": "#f59e0b",
  "disruption_industrielle_majeure": "#d97706",
  "crise_politique_industrielle_systémique": "#ef4444",
};
const ACT_COLORS: Record<string, string> = {
  "veille_politique_industrielle_continue": "#10b981",
  "surveillance_dépendances_industrielles": "#f59e0b",
  "renforcement_stratégie_relocalisation": "#d97706",
  "intervention_urgente_politique_industrielle": "#ef4444",
};
const RISK_BADGE: Record<string, string> = {
  low: "bg-emerald-900 text-emerald-300",
  moderate: "bg-amber-900 text-amber-300",
  high: "bg-orange-900 text-orange-300",
  critical: "bg-red-950 text-red-300",
};
const SEV_BADGE: Record<string, string> = {
  "politique_industrielle_gérée": "bg-emerald-900 text-emerald-300",
  "restructuration_industrielle_active": "bg-amber-900 text-amber-300",
  "disruption_industrielle_majeure": "bg-orange-900 text-orange-300",
  "crise_politique_industrielle_systémique": "bg-red-950 text-red-300",
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
      <div
        className="bg-slate-950 border border-blue-700/30 rounded-xl w-full max-w-lg p-6 shadow-2xl"
        onClick={e => e.stopPropagation()}
      >
        <div className="flex items-center justify-between mb-4">
          <div>
            <span className="text-lg font-bold text-white">{entity.entity_id}</span>
            <span className="ml-2 text-blue-400 text-xs">{entity.region}</span>
            <span className="ml-2 text-slate-500 text-xs">{entity.industrial_sector.replace(/_/g, " ")}</span>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl leading-none">✕</button>
        </div>

        <div className="flex gap-2 mb-4">
          {(["scores", "signal", "action"] as const).map(t => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`px-3 py-1 rounded text-xs font-medium transition-colors ${
                tab === t
                  ? "bg-blue-900 text-white"
                  : "bg-slate-900 text-slate-400 hover:text-white"
              }`}
            >
              {t === "scores" ? "Scores" : t === "signal" ? "Signal" : "Action"}
            </button>
          ))}
        </div>

        {tab === "scores" && (
          <div className="grid grid-cols-2 gap-3 text-sm">
            {([
              ["Dépendance",   entity.dependency_score,   "#ef4444"],
              ["Politique",    entity.policy_score,        "#f59e0b"],
              ["Résilience",   entity.resilience_score,    "#3b82f6"],
              ["Géopolitique", entity.geopolitical_score,  "#8b5cf6"],
            ] as [string, number, string][]).map(([l, v, c]) => (
              <div key={l} className="bg-slate-900 border border-blue-700/20 rounded-lg p-3">
                <div className="text-blue-300/60 text-xs mb-1">{l}</div>
                <div className="text-white font-bold text-lg">{Number(v).toFixed(1)}</div>
                <div className="h-1.5 rounded mt-1 bg-slate-800">
                  <div className="h-1.5 rounded" style={{ width: `${Math.min(Number(v), 100)}%`, background: c }} />
                </div>
              </div>
            ))}
            <div className="col-span-2 bg-slate-900 border border-blue-700/20 rounded-lg p-3">
              <div className="text-blue-300/60 text-xs mb-1">Composite Politique Industrielle</div>
              <div className="text-white font-bold text-2xl">{entity.composite_score.toFixed(1)}</div>
            </div>
          </div>
        )}

        {tab === "signal" && (
          <div className="bg-slate-900 border border-blue-700/20 rounded-lg p-4 text-sm text-slate-200 leading-relaxed">
            {entity.signal}
            <div className="mt-3 flex gap-2 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[entity.risk_level] || "bg-slate-700 text-slate-300"}`}>
                {entity.risk_level}
              </span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[entity.severity] || "bg-slate-700 text-slate-300"}`}>
                {entity.severity.replace(/_/g, " ")}
              </span>
            </div>
            <div className="mt-3 grid grid-cols-2 gap-2 text-xs">
              <div className="bg-slate-800 rounded p-2">
                <div className="text-blue-300/50 mb-0.5">Exposition Dépendance Stratégique</div>
                <div className="text-white font-bold">{Math.round(entity.strategic_dependency_exposure * 100)}%</div>
              </div>
              <div className="bg-slate-800 rounded p-2">
                <div className="text-blue-300/50 mb-0.5">Dépendance Semiconducteurs</div>
                <div className="text-white font-bold">{Math.round(entity.semiconductor_dependency * 100)}%</div>
              </div>
            </div>
          </div>
        )}

        {tab === "action" && (
          <div className="space-y-3 text-sm">
            <div className="bg-slate-900 border border-blue-700/20 rounded-lg p-3">
              <div className="text-blue-300/60 text-xs mb-1">Action Recommandée</div>
              <div className="text-white font-medium">{entity.recommended_action.replace(/_/g, " ")}</div>
            </div>
            <div className="bg-slate-900 border border-blue-700/20 rounded-lg p-3">
              <div className="text-blue-300/60 text-xs mb-1">Schéma Industriel Détecté</div>
              <div className="text-white font-medium capitalize">{entity.industrial_pattern.replace(/_/g, " ")}</div>
            </div>
            <div className="bg-slate-900 border border-blue-700/20 rounded-lg p-3">
              <div className="text-blue-300/60 text-xs mb-1">Sévérité</div>
              <div className="text-white font-medium">{entity.severity.replace(/_/g, " ")}</div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function IndustrialPolicyEngineDashboard() {
  const [data, setData]         = useState<{ entities: Entity[]; summary: Summary } | null>(null);
  const [filter, setFilter]     = useState<string>("all");
  const [patFilter, setPat]     = useState<string>("all");
  const [selected, setSelected] = useState<Entity | null>(null);

  useEffect(() => {
    fetch("/api/industrial-policy-engine")
      .then(r => r.json())
      .then(setData)
      .catch(console.error);
  }, []);

  if (!data) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-blue-400 text-lg animate-pulse">Initialisation du Moteur Politique Industrielle &amp; Relocalisation...</div>
    </div>
  );

  const { entities, summary } = data;
  const filtered = entities.filter(e =>
    (filter === "all" || e.risk_level === filter) &&
    (patFilter === "all" || e.industrial_pattern === patFilter)
  );

  const avgDependency = entities.reduce((s, e) => s + e.dependency_score, 0) / (entities.length || 1);

  const dists: Array<{ title: string; counts: Record<string, number>; colors: Record<string, string> }> = [
    { title: "Niveau Risque Industriel",         counts: summary.risk_distribution,     colors: RISK_COLORS },
    { title: "Schéma Politique Industrielle",    counts: summary.pattern_distribution,  colors: PAT_COLORS  },
    { title: "Sévérité Crise Industrielle",      counts: summary.severity_distribution, colors: SEV_COLORS  },
    { title: "Action Déclenchée",                counts: summary.action_distribution,   colors: ACT_COLORS  },
  ];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {selected && <DetailModal entity={selected} onClose={() => setSelected(null)} />}

      <div>
        <h1 className="text-2xl font-bold text-blue-400">
          Politique Industrielle &amp; Relocalisation — Module 383
        </h1>
        <p className="text-blue-300/50 text-sm mt-1">
          Dépendance · Politique · Résilience · Géopolitique Industrielle
        </p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {([
          ["Total Secteurs",          summary.total,                                           "text-blue-400"],
          ["Dépendance Stratégique",  summary.critical,                                        "text-red-400"],
          ["Crise Majeure",           summary.high,                                            "text-amber-400"],
          ["Composite Moyen",         summary.avg_composite.toFixed(1),                        "text-blue-300"],
          ["Index Relocalisation",    summary.avg_estimated_reshoring_index.toFixed(2),        "text-emerald-400"],
          ["Dépendance Moyenne",      avgDependency.toFixed(1),                                "text-slate-300"],
        ] as [string, string | number, string][]).map(([l, v, c]) => (
          <div key={String(l)} className="bg-slate-900 border border-blue-700/30 rounded-xl p-3 text-center">
            <div className={`text-xl font-bold ${c}`}>{v}</div>
            <div className="text-xs text-blue-300/40 mt-0.5 leading-tight">{l}</div>
          </div>
        ))}
      </div>

      {/* Gauge Rings */}
      <div className="bg-slate-900 border border-blue-700/30 rounded-xl p-5">
        <div className="grid grid-cols-4 gap-4">
          <GaugeRing value={entities.reduce((s, e) => s + e.dependency_score, 0)   / (entities.length || 1)} label="Dépendance"   color="#ef4444" />
          <GaugeRing value={entities.reduce((s, e) => s + e.policy_score, 0)       / (entities.length || 1)} label="Politique"    color="#f59e0b" />
          <GaugeRing value={entities.reduce((s, e) => s + e.resilience_score, 0)   / (entities.length || 1)} label="Résilience"   color="#3b82f6" />
          <GaugeRing value={entities.reduce((s, e) => s + e.geopolitical_score, 0) / (entities.length || 1)} label="Géopolitique" color="#8b5cf6" />
        </div>
      </div>

      {/* Distribution Bars */}
      <div className="bg-slate-900 border border-blue-700/30 rounded-xl p-5 grid grid-cols-1 md:grid-cols-2 gap-5">
        {dists.map(d => <DistBar key={d.title} {...d} />)}
      </div>

      {/* Filter Pills */}
      <div className="flex flex-wrap gap-2">
        {["all", "low", "moderate", "high", "critical"].map(r => (
          <button
            key={r}
            onClick={() => setFilter(r)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${
              filter === r
                ? "bg-blue-900 border-blue-700 text-white"
                : "bg-slate-900 border-blue-700/30 text-blue-400/70 hover:text-white"
            }`}
          >
            {r}
          </button>
        ))}
        <span className="w-px h-5 self-center bg-blue-700/30" />
        {["all", "none", "strategic_dependency_crisis", "subsidy_trade_war_escalation", "reshoring_policy_failure", "pharmaceutical_supply_collapse", "green_manufacturing_gap_crisis"].map(p => (
          <button
            key={p}
            onClick={() => setPat(p)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${
              patFilter === p
                ? "bg-slate-700 border-slate-500 text-white"
                : "bg-slate-900 border-blue-700/30 text-blue-400/70 hover:text-white"
            }`}
          >
            {p.replace(/_/g, " ")}
          </button>
        ))}
      </div>

      {/* Entity Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {filtered.map(e => (
          <div
            key={e.entity_id}
            onClick={() => setSelected(e)}
            className="bg-slate-900 border border-blue-700/30 rounded-xl p-4 cursor-pointer hover:border-blue-500 transition-colors"
          >
            <div className="flex items-center justify-between mb-1">
              <span className="font-bold text-white">{e.entity_id}</span>
              <span className="text-xs text-blue-400/60">{e.region}</span>
            </div>
            <div className="text-xs text-slate-500 mb-2 capitalize">{e.industrial_sector.replace(/_/g, " ")}</div>
            <div className="flex gap-1 mb-3 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[e.risk_level] || "bg-slate-700 text-slate-300"}`}>
                {e.risk_level}
              </span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[e.severity] || "bg-slate-700 text-slate-300"}`}>
                {e.severity.replace(/_/g, " ")}
              </span>
            </div>
            <div className="text-2xl font-black text-white mb-1">{e.composite_score.toFixed(1)}</div>
            <div className="text-xs text-blue-400/60 mb-2 capitalize">{e.industrial_pattern.replace(/_/g, " ")}</div>
            <div className="text-xs text-red-400 font-medium mb-2">
              Dépendance: {e.dependency_score.toFixed(1)}
            </div>
            <div className="text-xs text-slate-400 truncate">{e.signal}</div>
          </div>
        ))}
      </div>
    </div>
  );
}
