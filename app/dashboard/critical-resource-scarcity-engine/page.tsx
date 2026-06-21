"use client";
import { useEffect, useState } from "react";

type Entity = {
  id: string;
  region: string;
  resource_category: string;
  scarcity_risk: string;
  scarcity_pattern: string;
  scarcity_severity: string;
  recommended_action: string;
  supply_score: number;
  demand_score: number;
  geopolitical_score: number;
  sustainability_score: number;
  scarcity_composite: number;
  is_in_scarcity_crisis: boolean;
  requires_scarcity_intervention: boolean;
  scarcity_signal: string;
};

type Summary = {
  total: number;
  risk_counts: Record<string, number>;
  pattern_counts: Record<string, number>;
  severity_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_scarcity_composite: number;
  scarcity_crisis_count: number;
  scarcity_intervention_count: number;
  avg_supply_score: number;
  avg_demand_score: number;
  avg_geopolitical_score: number;
  avg_sustainability_score: number;
  avg_estimated_scarcity_index: number;
};

function GaugeRing({ value, label, color }: { value: number; label: string; color: string }) {
  const r = 36;
  const circ = 2 * Math.PI * r;
  const fill = circ * (1 - value / 100);
  return (
    <div className="flex flex-col items-center gap-1">
      <svg width="88" height="88" viewBox="0 0 88 88">
        <circle cx="44" cy="44" r={r} fill="none" stroke="#1a0e00" strokeWidth="8" />
        <circle
          cx="44" cy="44" r={r} fill="none" stroke={color} strokeWidth="8"
          strokeDasharray={circ} strokeDashoffset={fill}
          strokeLinecap="round" transform="rotate(-90 44 44)"
        />
        <text x="44" y="49" textAnchor="middle" fill="white" fontSize="13" fontWeight="bold">
          {Math.round(value)}
        </text>
      </svg>
      <span className="text-xs text-orange-300/70 text-center">{label}</span>
    </div>
  );
}

function DistBar({
  title,
  counts,
  colors,
}: {
  title: string;
  counts: Record<string, number>;
  colors: Record<string, string>;
}) {
  const total = Object.values(counts).reduce((a, b) => a + b, 0) || 1;
  return (
    <div className="flex flex-col gap-1">
      <span className="text-xs text-orange-300/70 font-medium">{title}</span>
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
          <span key={k} className="text-xs text-orange-300/60">
            <span style={{ color: colors[k] || "#94a3b8" }}>■</span> {k} {v}
          </span>
        ))}
      </div>
    </div>
  );
}

const RISK_COLORS: Record<string, string> = {
  low: "#10b981",
  moderate: "#f59e0b",
  high: "#f97316",
  critical: "#b45309",
};
const PATTERN_COLORS: Record<string, string> = {
  none: "#10b981",
  supply_shock: "#92400e",
  geopolitical_embargo: "#b45309",
  demand_explosion: "#f97316",
  depletion_crisis: "#dc2626",
  processing_monopoly: "#a16207",
};
const SEVERITY_COLORS: Record<string, string> = {
  resource_abundant: "#10b981",
  supply_tension: "#f59e0b",
  high_scarcity: "#f97316",
  resource_emergency: "#92400e",
};
const ACTION_COLORS: Record<string, string> = {
  no_action: "#10b981",
  resource_monitoring: "#06b6d4",
  strategic_reserve_buildup: "#f59e0b",
  supply_diversification: "#f97316",
  resource_emergency_program: "#92400e",
};
const RISK_BADGE: Record<string, string> = {
  low: "bg-emerald-900 text-emerald-300",
  moderate: "bg-amber-900 text-amber-300",
  high: "bg-orange-900 text-orange-300",
  critical: "bg-amber-950 text-amber-400",
};
const SEV_BADGE: Record<string, string> = {
  resource_abundant: "bg-emerald-900 text-emerald-300",
  supply_tension: "bg-amber-900 text-amber-300",
  high_scarcity: "bg-orange-900 text-orange-300",
  resource_emergency: "bg-amber-950 text-amber-400",
};

function DetailModal({ entity, onClose }: { entity: Entity; onClose: () => void }) {
  const [tab, setTab] = useState<"scores" | "signal" | "action">("scores");

  useEffect(() => {
    const h = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
    };
    window.addEventListener("keydown", h);
    return () => window.removeEventListener("keydown", h);
  }, [onClose]);

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/80"
      onClick={onClose}
    >
      <div
        className="bg-slate-950 border border-amber-800/30 rounded-xl w-full max-w-lg p-6 shadow-2xl"
        onClick={e => e.stopPropagation()}
      >
        <div className="flex items-center justify-between mb-4">
          <div>
            <span className="text-lg font-bold text-white">{entity.id}</span>
            <span className="ml-2 text-orange-400 text-xs">{entity.region}</span>
            <span className="ml-2 text-slate-500 text-xs">
              {entity.resource_category.replace(/_/g, " ")}
            </span>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl leading-none">
            ✕
          </button>
        </div>

        <div className="flex gap-2 mb-4">
          {(["scores", "signal", "action"] as const).map(t => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`px-3 py-1 rounded text-xs font-medium transition-colors ${
                tab === t
                  ? "bg-amber-900 text-white"
                  : "bg-slate-900 text-slate-400 hover:text-white"
              }`}
            >
              {t.charAt(0).toUpperCase() + t.slice(1)}
            </button>
          ))}
        </div>

        {tab === "scores" && (
          <div className="grid grid-cols-2 gap-3 text-sm">
            {[
              ["Approvisionnement", entity.supply_score, "#f97316"],
              ["Demande", entity.demand_score, "#f59e0b"],
              ["Géopolitique", entity.geopolitical_score, "#b45309"],
              ["Durabilité", entity.sustainability_score, "#10b981"],
            ].map(([l, v, c]) => (
              <div
                key={String(l)}
                className="bg-slate-900 border border-amber-800/20 rounded-lg p-3"
              >
                <div className="text-orange-300/60 text-xs mb-1">{String(l)}</div>
                <div className="text-white font-bold text-lg">{Number(v).toFixed(1)}</div>
                <div className="h-1.5 rounded mt-1 bg-slate-800">
                  <div
                    className="h-1.5 rounded"
                    style={{ width: `${Math.min(Number(v), 100)}%`, background: String(c) }}
                  />
                </div>
              </div>
            ))}
            <div className="col-span-2 bg-slate-900 border border-amber-800/20 rounded-lg p-3">
              <div className="text-orange-300/60 text-xs mb-1">Composite Pénurie</div>
              <div className="text-white font-bold text-2xl">
                {entity.scarcity_composite.toFixed(1)}
              </div>
            </div>
          </div>
        )}

        {tab === "signal" && (
          <div className="bg-slate-900 border border-amber-800/20 rounded-lg p-4 text-sm text-slate-200 leading-relaxed">
            {entity.scarcity_signal}
            <div className="mt-3 flex gap-2 flex-wrap">
              <span
                className={`px-2 py-0.5 rounded text-xs font-medium ${
                  RISK_BADGE[entity.scarcity_risk] || "bg-slate-700 text-slate-300"
                }`}
              >
                {entity.scarcity_risk}
              </span>
              <span
                className={`px-2 py-0.5 rounded text-xs font-medium ${
                  SEV_BADGE[entity.scarcity_severity] || "bg-slate-700 text-slate-300"
                }`}
              >
                {entity.scarcity_severity.replace(/_/g, " ")}
              </span>
            </div>
          </div>
        )}

        {tab === "action" && (
          <div className="space-y-3 text-sm">
            <div className="bg-slate-900 border border-amber-800/20 rounded-lg p-3">
              <div className="text-orange-300/60 text-xs mb-1">Action Recommandée</div>
              <div className="text-white font-medium">
                {entity.recommended_action.replace(/_/g, " ")}
              </div>
            </div>
            <div className="bg-slate-900 border border-amber-800/20 rounded-lg p-3">
              <div className="text-orange-300/60 text-xs mb-1">Pattern de Pénurie</div>
              <div className="text-white font-medium capitalize">
                {entity.scarcity_pattern.replace(/_/g, " ")}
              </div>
            </div>
            <div className="flex gap-2">
              {entity.is_in_scarcity_crisis && (
                <span className="px-2 py-1 rounded bg-amber-950 text-amber-400 text-xs font-medium">
                  CRISE PÉNURIE
                </span>
              )}
              {entity.requires_scarcity_intervention && (
                <span className="px-2 py-1 rounded bg-orange-950 text-orange-400 text-xs font-medium">
                  INTERVENTION REQ.
                </span>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function CriticalResourceScarcityDashboard() {
  const [data, setData] = useState<{ entities: Entity[]; summary: Summary } | null>(null);
  const [filter, setFilter] = useState<string>("all");
  const [patFilter, setPatFilter] = useState<string>("all");
  const [selected, setSelected] = useState<Entity | null>(null);

  useEffect(() => {
    fetch("/api/critical-resource-scarcity-engine")
      .then(r => r.json())
      .then(setData)
      .catch(console.error);
  }, []);

  if (!data) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center">
        <div className="text-orange-400 text-lg animate-pulse">
          Initialisation du Moteur de Pénurie des Ressources Critiques...
        </div>
      </div>
    );
  }

  const { entities, summary } = data;
  const filtered = entities.filter(
    e =>
      (filter === "all" || e.scarcity_risk === filter) &&
      (patFilter === "all" || e.scarcity_pattern === patFilter)
  );

  const dists = [
    { title: "Niveau Pénurie",       counts: summary.risk_counts,     colors: RISK_COLORS     },
    { title: "Pattern Pénurie",      counts: summary.pattern_counts,  colors: PATTERN_COLORS  },
    { title: "Sévérité Ressources",  counts: summary.severity_counts, colors: SEVERITY_COLORS },
    { title: "Action Déclenchée",    counts: summary.action_counts,   colors: ACTION_COLORS   },
  ] as Array<{ title: string; counts: Record<string, number>; colors: Record<string, string> }>;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {selected && <DetailModal entity={selected} onClose={() => setSelected(null)} />}

      <div>
        <h1 className="text-2xl font-bold text-orange-300">
          Material World Scarcity &amp; Critical Resource Intelligence Engine
        </h1>
        <p className="text-orange-300/50 text-sm mt-1">
          Approvisionnement · Demande · Géopolitique · Durabilité — Terres Rares, Semi-conducteurs, Eau, Alimentation
        </p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {[
          ["Entités Analysées",              summary.total,                                        "text-orange-300"],
          ["Crises de Pénurie",              summary.scarcity_crisis_count,                        "text-amber-400"],
          ["Interventions Requises",         summary.scarcity_intervention_count,                  "text-orange-400"],
          ["Composite Moyen",                summary.avg_scarcity_composite.toFixed(1),            "text-amber-300"],
          ["Indice Pénurie Moyen",           summary.avg_estimated_scarcity_index.toFixed(2)+"/10","text-orange-300"],
          ["Score Géopolitique Moyen",       summary.avg_geopolitical_score.toFixed(1),            "text-amber-400"],
        ].map(([l, v, c]) => (
          <div
            key={String(l)}
            className="bg-slate-900 border border-amber-800/30 rounded-xl p-3 text-center"
          >
            <div className={`text-xl font-bold ${c}`}>{v}</div>
            <div className="text-xs text-orange-300/40 mt-0.5 leading-tight">{l}</div>
          </div>
        ))}
      </div>

      {/* Gauge Rings */}
      <div className="bg-slate-900 border border-amber-800/30 rounded-xl p-5">
        <div className="grid grid-cols-4 gap-4">
          <GaugeRing value={summary.avg_supply_score}       label="Score Approvisionnement" color="#f97316" />
          <GaugeRing value={summary.avg_demand_score}       label="Score Demande"            color="#f59e0b" />
          <GaugeRing value={summary.avg_geopolitical_score} label="Score Géopolitique"       color="#b45309" />
          <GaugeRing value={summary.avg_sustainability_score} label="Score Durabilité"       color="#10b981" />
        </div>
      </div>

      {/* Distribution Bars */}
      <div className="bg-slate-900 border border-amber-800/30 rounded-xl p-5 grid grid-cols-1 md:grid-cols-2 gap-5">
        {dists.map(d => (
          <DistBar key={d.title} {...d} />
        ))}
      </div>

      {/* Filter Pills */}
      <div className="flex flex-wrap gap-2">
        {["all", "low", "moderate", "high", "critical"].map(r => (
          <button
            key={r}
            onClick={() => setFilter(r)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${
              filter === r
                ? "bg-amber-900 border-amber-700 text-white"
                : "bg-slate-900 border-amber-800/30 text-orange-400/70 hover:text-white"
            }`}
          >
            {r}
          </button>
        ))}
        <span className="w-px h-5 self-center bg-amber-800/30" />
        {[
          "all",
          "none",
          "supply_shock",
          "geopolitical_embargo",
          "demand_explosion",
          "depletion_crisis",
          "processing_monopoly",
        ].map(p => (
          <button
            key={p}
            onClick={() => setPatFilter(p)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${
              patFilter === p
                ? "bg-amber-950 border-amber-800 text-white"
                : "bg-slate-900 border-amber-800/30 text-orange-400/70 hover:text-white"
            }`}
          >
            {p.replace(/_/g, " ")}
          </button>
        ))}
      </div>

      {/* Entity Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {filtered.map(e => (
          <div
            key={e.id}
            onClick={() => setSelected(e)}
            className="bg-slate-900 border border-amber-800/30 rounded-xl p-4 cursor-pointer hover:border-amber-600 transition-colors"
          >
            <div className="flex items-center justify-between mb-1">
              <span className="font-bold text-white">{e.id}</span>
              <span className="text-xs text-orange-400/60">{e.region}</span>
            </div>
            <div className="text-xs text-slate-500 mb-2 capitalize">
              {e.resource_category.replace(/_/g, " ")}
            </div>
            <div className="flex gap-1 mb-3 flex-wrap">
              <span
                className={`px-2 py-0.5 rounded text-xs font-medium ${
                  RISK_BADGE[e.scarcity_risk] || "bg-slate-700 text-slate-300"
                }`}
              >
                {e.scarcity_risk}
              </span>
              <span
                className={`px-2 py-0.5 rounded text-xs font-medium ${
                  SEV_BADGE[e.scarcity_severity] || "bg-slate-700 text-slate-300"
                }`}
              >
                {e.scarcity_severity.replace(/_/g, " ")}
              </span>
            </div>
            <div className="text-2xl font-black text-white mb-1">
              {e.scarcity_composite.toFixed(1)}
            </div>
            <div className="text-xs text-orange-400/60 mb-2 capitalize">
              {e.scarcity_pattern.replace(/_/g, " ")}
            </div>
            <div className="flex gap-1 flex-wrap">
              {e.is_in_scarcity_crisis && (
                <span className="px-1.5 py-0.5 rounded bg-amber-950 text-amber-400 text-xs">
                  CRISE
                </span>
              )}
              {e.requires_scarcity_intervention && (
                <span className="px-1.5 py-0.5 rounded bg-orange-950 text-orange-400 text-xs">
                  INTERVENTION
                </span>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
