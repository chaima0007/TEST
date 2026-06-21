"use client";
import { useEffect, useState } from "react";

interface Entity {
  id: string;
  name: string;
  country: string;
  sector: string;
  composite_score: number;
  coordination_score: number;
  autonomy_score: number;
  latency_score: number;
  resilience_score: number;
  risk_level: string;
  primary_pattern: string;
  key_signals: string[];
  estimated_orchestration_index: number;
  last_updated: string;
  agent_count: number;
}

interface SummaryData {
  total_entities: number;
  avg_composite: number;
  risk_distribution: Record<string, number>;
  pattern_distribution: Record<string, number>;
  top_risk_entities: string[];
  critical_alerts: string[];
  last_analysis: string;
  engine_version: string;
  domain: string;
  confidence_score: number;
  data_sources: string[];
  entities: Entity[];
  avg_estimated_orchestration_index: number;
}

function GaugeRing({ value, label, color }: { value: number; label: string; color: string }) {
  const r = 36;
  const circ = 2 * Math.PI * r;
  const fill = circ * (1 - value / 100);
  return (
    <div className="flex flex-col items-center gap-1">
      <svg width="88" height="88" viewBox="0 0 88 88">
        <circle cx="44" cy="44" r={r} fill="none" stroke="#0c1a2e" strokeWidth="8" />
        <circle
          cx="44" cy="44" r={r} fill="none" stroke={color} strokeWidth="8"
          strokeDasharray={circ} strokeDashoffset={fill}
          strokeLinecap="round" transform="rotate(-90 44 44)"
        />
        <text x="44" y="49" textAnchor="middle" fill="white" fontSize="13" fontWeight="bold">
          {Math.round(value)}
        </text>
      </svg>
      <span className="text-xs text-sky-300/70 text-center">{label}</span>
    </div>
  );
}

function DistBar({ title, counts, colors }: { title: string; counts: Record<string, number>; colors: Record<string, string> }) {
  const total = Object.values(counts).reduce((a, b) => a + b, 0) || 1;
  return (
    <div className="flex flex-col gap-1">
      <span className="text-xs text-sky-300/70 font-medium">{title}</span>
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
          <span key={k} className="text-xs text-sky-300/60">
            <span style={{ color: colors[k] || "#94a3b8" }}>■</span> {k.replace(/_/g, " ")} {v}
          </span>
        ))}
      </div>
    </div>
  );
}

const RISK_COLORS: Record<string, string> = {
  faible: "#10b981",
  modéré: "#f59e0b",
  élevé: "#f97316",
  critique: "#ef4444",
};

const PAT_COLORS: Record<string, string> = {
  equilibrium_stable: "#10b981",
  autonomy_drift: "#06b6d4",
  latency_cascade: "#f59e0b",
  resilience_collapse: "#f97316",
  coordination_failure: "#ef4444",
};

const RISK_BADGE: Record<string, string> = {
  faible: "bg-emerald-900 text-emerald-300",
  modéré: "bg-amber-900 text-amber-300",
  élevé: "bg-orange-900 text-orange-300",
  critique: "bg-red-950 text-red-400",
};

function DetailModal({ entity, onClose }: { entity: Entity; onClose: () => void }) {
  const [tab, setTab] = useState<"Scores" | "Signaux" | "Actions">("Scores");
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
            <span className="text-lg font-bold text-white">{entity.id}</span>
            <span className="ml-2 text-sky-400 text-xs">{entity.name}</span>
            <span className="ml-2 text-slate-500 text-xs">{entity.country}</span>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl leading-none">✕</button>
        </div>

        <div className="flex gap-2 mb-4">
          {(["Scores", "Signaux", "Actions"] as const).map(t => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`px-3 py-1 rounded text-xs font-medium transition-colors ${
                tab === t
                  ? "bg-sky-900 text-white"
                  : "bg-slate-900 text-slate-400 hover:text-white"
              }`}
            >
              {t}
            </button>
          ))}
        </div>

        {tab === "Scores" && (
          <div className="grid grid-cols-2 gap-3 text-sm">
            {([
              ["Coordination", entity.coordination_score, "#ef4444"],
              ["Autonomie",    entity.autonomy_score,     "#06b6d4"],
              ["Latence",      entity.latency_score,      "#f59e0b"],
              ["Résilience",   entity.resilience_score,   "#a855f7"],
            ] as [string, number, string][]).map(([l, v, c]) => (
              <div key={l} className="bg-slate-900 border border-blue-700/20 rounded-lg p-3">
                <div className="text-sky-300/60 text-xs mb-1">{l}</div>
                <div className="text-white font-bold text-lg">{Number(v).toFixed(1)}</div>
                <div className="h-1.5 rounded mt-1 bg-slate-800">
                  <div className="h-1.5 rounded" style={{ width: `${Math.min(Number(v), 100)}%`, background: c }} />
                </div>
              </div>
            ))}
            <div className="col-span-2 bg-slate-900 border border-blue-700/20 rounded-lg p-3">
              <div className="text-sky-300/60 text-xs mb-1">Score Composite Orchestration</div>
              <div className="text-white font-bold text-2xl">{entity.composite_score.toFixed(1)}</div>
            </div>
          </div>
        )}

        {tab === "Signaux" && (
          <div className="bg-slate-900 border border-blue-700/20 rounded-lg p-4 text-sm text-slate-200 leading-relaxed">
            <ul className="space-y-2 mb-4">
              {entity.key_signals.map((s, i) => (
                <li key={i} className="flex items-start gap-2">
                  <span className="text-sky-400 mt-0.5">▸</span>
                  <span>{s}</span>
                </li>
              ))}
            </ul>
            <div className="mt-3 flex gap-2 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[entity.risk_level] || "bg-slate-700 text-slate-300"}`}>
                {entity.risk_level}
              </span>
              <span className="px-2 py-0.5 rounded text-xs font-medium bg-slate-700 text-slate-300">
                {entity.agent_count} agents
              </span>
            </div>
          </div>
        )}

        {tab === "Actions" && (
          <div className="space-y-3 text-sm">
            <div className="bg-slate-900 border border-blue-700/20 rounded-lg p-3">
              <div className="text-sky-300/60 text-xs mb-1">Pattern Principal</div>
              <div className="text-white font-medium capitalize">{entity.primary_pattern.replace(/_/g, " ")}</div>
            </div>
            <div className="bg-slate-900 border border-blue-700/20 rounded-lg p-3">
              <div className="text-sky-300/60 text-xs mb-1">Index Orchestration Estimé</div>
              <div className="text-white font-bold text-lg">{entity.estimated_orchestration_index.toFixed(2)}</div>
            </div>
            <div className="bg-slate-900 border border-blue-700/20 rounded-lg p-3">
              <div className="text-sky-300/60 text-xs mb-1">Dernière Mise à Jour</div>
              <div className="text-white font-medium">{entity.last_updated}</div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function OrchestrationDashboard() {
  const [data, setData]         = useState<SummaryData | null>(null);
  const [filter, setFilter]     = useState<string>("Tous");
  const [selected, setSelected] = useState<Entity | null>(null);

  useEffect(() => {
    fetch("/api/agent-orchestrator")
      .then(r => r.json())
      .then(setData)
      .catch(console.error);
  }, []);

  if (!data) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-sky-400 text-lg animate-pulse">Initialisation du Moteur Orchestration Agents...</div>
    </div>
  );

  const FILTER_MAP: Record<string, string> = {
    "Tous": "",
    "Critique": "critique",
    "Élevé": "élevé",
    "Modéré": "modéré",
    "Faible": "faible",
  };

  const filtered = data.entities.filter(e =>
    filter === "Tous" || e.risk_level === FILTER_MAP[filter]
  );

  const avgCoord    = Math.round(data.entities.reduce((s, e) => s + e.coordination_score, 0) / data.entities.length * 10) / 10;
  const avgAutonomy = Math.round(data.entities.reduce((s, e) => s + e.autonomy_score, 0) / data.entities.length * 10) / 10;
  const avgLatency  = Math.round(data.entities.reduce((s, e) => s + e.latency_score, 0) / data.entities.length * 10) / 10;
  const avgResil    = Math.round(data.entities.reduce((s, e) => s + e.resilience_score, 0) / data.entities.length * 10) / 10;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {selected && <DetailModal entity={selected} onClose={() => setSelected(null)} />}

      <div>
        <h1 className="text-2xl font-bold text-sky-400">
          Agent Orchestrator Intelligence Engine
        </h1>
        <p className="text-sky-300/50 text-sm mt-1">
          Coordination · Autonomie · Latence · Résilience — Caelum Partners
        </p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {([
          ["Total Entités",        data.total_entities,                                  "text-sky-400"],
          ["Critique",             data.risk_distribution["critique"] ?? 0,              "text-red-400"],
          ["Élevé",                data.risk_distribution["élevé"] ?? 0,                "text-orange-400"],
          ["Composite Moyen",      data.avg_composite.toFixed(1),                        "text-sky-300"],
          ["Index Orchestration",  data.avg_estimated_orchestration_index.toFixed(2),    "text-amber-400"],
          ["Confiance",            `${Math.round(data.confidence_score * 100)}%`,        "text-emerald-400"],
        ] as [string, string | number, string][]).map(([l, v, c]) => (
          <div key={String(l)} className="bg-slate-900 border border-blue-700/30 rounded-xl p-3 text-center">
            <div className={`text-xl font-bold ${c}`}>{v}</div>
            <div className="text-xs text-sky-300/40 mt-0.5 leading-tight">{l}</div>
          </div>
        ))}
      </div>

      {/* Gauge Rings */}
      <div className="bg-slate-900 border border-blue-700/30 rounded-xl p-5">
        <div className="grid grid-cols-4 gap-4">
          <GaugeRing value={avgCoord}    label="Coordination Moy."  color="#ef4444" />
          <GaugeRing value={avgAutonomy} label="Autonomie Moy."     color="#06b6d4" />
          <GaugeRing value={avgLatency}  label="Latence Moy."       color="#f59e0b" />
          <GaugeRing value={avgResil}    label="Résilience Moy."    color="#a855f7" />
        </div>
      </div>

      {/* Distribution Bars */}
      <div className="bg-slate-900 border border-blue-700/30 rounded-xl p-5 grid grid-cols-1 md:grid-cols-2 gap-5">
        <DistBar
          title="Distribution Niveaux de Risque"
          counts={data.risk_distribution}
          colors={RISK_COLORS}
        />
        <DistBar
          title="Distribution Patterns Orchestration"
          counts={data.pattern_distribution}
          colors={PAT_COLORS}
        />
        <DistBar
          title="Entités Modéré / Faible"
          counts={{
            modéré: data.risk_distribution["modéré"] ?? 0,
            faible: data.risk_distribution["faible"] ?? 0,
          }}
          colors={{ modéré: "#f59e0b", faible: "#10b981" }}
        />
        <DistBar
          title="Patterns Stables vs Dégradés"
          counts={{
            equilibrium_stable: data.pattern_distribution["equilibrium_stable"] ?? 0,
            coordination_failure: data.pattern_distribution["coordination_failure"] ?? 0,
            autonomy_drift: data.pattern_distribution["autonomy_drift"] ?? 0,
            latency_cascade: data.pattern_distribution["latency_cascade"] ?? 0,
            resilience_collapse: data.pattern_distribution["resilience_collapse"] ?? 0,
          }}
          colors={PAT_COLORS}
        />
      </div>

      {/* Filter Pills */}
      <div className="flex flex-wrap gap-2">
        {["Tous", "Critique", "Élevé", "Modéré", "Faible"].map(f => (
          <button
            key={f}
            onClick={() => setFilter(f)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${
              filter === f
                ? "bg-sky-900 border-sky-700 text-white"
                : "bg-slate-900 border-blue-700/30 text-sky-400/70 hover:text-white"
            }`}
          >
            {f}
          </button>
        ))}
      </div>

      {/* Entity Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {filtered.map(e => (
          <div
            key={e.id}
            onClick={() => setSelected(e)}
            className="bg-slate-900 border border-slate-800 rounded-xl p-4 cursor-pointer hover:border-sky-500 transition-colors"
          >
            <div className="flex items-center justify-between mb-1">
              <span className="font-bold text-white text-sm">{e.id}</span>
              <span className="text-xs text-sky-400/60">{e.country}</span>
            </div>
            <div className="text-sm font-medium text-white mb-0.5">{e.name}</div>
            <div className="text-xs text-slate-500 mb-2">{e.sector}</div>
            <div className="flex gap-1 mb-3 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[e.risk_level] || "bg-slate-700 text-slate-300"}`}>
                {e.risk_level}
              </span>
            </div>
            <div className="text-2xl font-black text-white mb-1">{e.composite_score.toFixed(1)}</div>
            <div className="text-xs text-sky-400/60 mb-2 capitalize">{e.primary_pattern.replace(/_/g, " ")}</div>
            <div className="text-xs text-slate-500">{e.agent_count} agents</div>
          </div>
        ))}
      </div>
    </div>
  );
}
