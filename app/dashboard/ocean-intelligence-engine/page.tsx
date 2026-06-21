"use client";
import { useEffect, useState } from "react";

type Entity = {
  id: string;
  region: string;
  ocean_domain: string;
  ocean_risk: string;
  ocean_pattern: string;
  ocean_severity: string;
  recommended_action: string;
  ecological_score: number;
  economic_score: number;
  security_score: number;
  geopolitical_score: number;
  ocean_composite: number;
  is_ocean_crisis: boolean;
  requires_ocean_intervention: boolean;
  ocean_signal: string;
};

type Summary = {
  total: number;
  risk_counts: Record<string, number>;
  pattern_counts: Record<string, number>;
  severity_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_ocean_composite: number;
  ocean_crisis_count: number;
  ocean_intervention_count: number;
  avg_ecological_score: number;
  avg_economic_score: number;
  avg_security_score: number;
  avg_geopolitical_score: number;
  avg_estimated_ocean_risk_index: number;
};

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
      <span className="text-xs text-blue-300/70 text-center">{label}</span>
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
            <span style={{ color: colors[k] || "#94a3b8" }}>■</span> {k} {v}
          </span>
        ))}
      </div>
    </div>
  );
}

const RISK_COLORS: Record<string, string> = {
  low: "#10b981",
  moderate: "#06b6d4",
  high: "#3b82f6",
  critical: "#dc2626",
};
const PATTERN_COLORS: Record<string, string> = {
  none: "#10b981",
  ecological_ocean_collapse: "#dc2626",
  maritime_security_crisis: "#7c3aed",
  blue_economy_disruption: "#1d4ed8",
  ocean_sovereignty_war: "#b45309",
  plastic_collapse: "#0891b2",
};
const SEVERITY_COLORS: Record<string, string> = {
  ocean_stable: "#10b981",
  ocean_stress: "#06b6d4",
  ocean_crisis: "#3b82f6",
  ocean_emergency: "#dc2626",
};
const ACTION_COLORS: Record<string, string> = {
  no_action: "#10b981",
  ocean_monitoring: "#06b6d4",
  ocean_resilience_program: "#3b82f6",
  naval_security_deployment: "#7c3aed",
  ocean_emergency_response: "#dc2626",
};
const RISK_BADGE: Record<string, string> = {
  low: "bg-emerald-900 text-emerald-300",
  moderate: "bg-cyan-900 text-cyan-300",
  high: "bg-blue-900 text-blue-300",
  critical: "bg-red-950 text-red-400",
};
const SEV_BADGE: Record<string, string> = {
  ocean_stable: "bg-emerald-900 text-emerald-300",
  ocean_stress: "bg-cyan-900 text-cyan-300",
  ocean_crisis: "bg-blue-900 text-blue-300",
  ocean_emergency: "bg-red-950 text-red-400",
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
        className="bg-slate-950 border border-teal-700/30 rounded-xl w-full max-w-lg p-6 shadow-2xl"
        onClick={e => e.stopPropagation()}
      >
        <div className="flex items-center justify-between mb-4">
          <div>
            <span className="text-lg font-bold text-white">{entity.id}</span>
            <span className="ml-2 text-blue-300 text-xs">{entity.region}</span>
            <span className="ml-2 text-slate-500 text-xs">
              {entity.ocean_domain.replace(/_/g, " ")}
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
                  ? "bg-teal-900 text-white"
                  : "bg-slate-900 text-slate-400 hover:text-white"
              }`}
            >
              {t === "scores" ? "Scores" : t === "signal" ? "Signal" : "Action"}
            </button>
          ))}
        </div>

        {tab === "scores" && (
          <div className="grid grid-cols-2 gap-3 text-sm">
            {[
              ["Écologie", entity.ecological_score, "#10b981"],
              ["Économie", entity.economic_score, "#3b82f6"],
              ["Sécurité", entity.security_score, "#7c3aed"],
              ["Géopolitique", entity.geopolitical_score, "#f59e0b"],
            ].map(([l, v, c]) => (
              <div
                key={String(l)}
                className="bg-slate-900 border border-teal-700/20 rounded-lg p-3"
              >
                <div className="text-blue-300/60 text-xs mb-1">{String(l)}</div>
                <div className="text-white font-bold text-lg">{Number(v).toFixed(1)}</div>
                <div className="h-1.5 rounded mt-1 bg-slate-800">
                  <div
                    className="h-1.5 rounded"
                    style={{ width: `${Math.min(Number(v), 100)}%`, background: String(c) }}
                  />
                </div>
              </div>
            ))}
            <div className="col-span-2 bg-slate-900 border border-teal-700/20 rounded-lg p-3">
              <div className="text-blue-300/60 text-xs mb-1">Composite Océanique</div>
              <div className="text-white font-bold text-2xl">
                {entity.ocean_composite.toFixed(1)}
              </div>
            </div>
          </div>
        )}

        {tab === "signal" && (
          <div className="bg-slate-900 border border-teal-700/20 rounded-lg p-4 text-sm text-slate-200 leading-relaxed">
            {entity.ocean_signal}
            <div className="mt-3 flex gap-2 flex-wrap">
              <span
                className={`px-2 py-0.5 rounded text-xs font-medium ${
                  RISK_BADGE[entity.ocean_risk] || "bg-slate-700 text-slate-300"
                }`}
              >
                {entity.ocean_risk}
              </span>
              <span
                className={`px-2 py-0.5 rounded text-xs font-medium ${
                  SEV_BADGE[entity.ocean_severity] || "bg-slate-700 text-slate-300"
                }`}
              >
                {entity.ocean_severity.replace(/_/g, " ")}
              </span>
            </div>
          </div>
        )}

        {tab === "action" && (
          <div className="space-y-3 text-sm">
            <div className="bg-slate-900 border border-teal-700/20 rounded-lg p-3">
              <div className="text-blue-300/60 text-xs mb-1">Action Recommandée</div>
              <div className="text-white font-medium">
                {entity.recommended_action.replace(/_/g, " ")}
              </div>
            </div>
            <div className="bg-slate-900 border border-teal-700/20 rounded-lg p-3">
              <div className="text-blue-300/60 text-xs mb-1">Pattern Océanique</div>
              <div className="text-white font-medium capitalize">
                {entity.ocean_pattern.replace(/_/g, " ")}
              </div>
            </div>
            <div className="flex gap-2">
              {entity.is_ocean_crisis && (
                <span className="px-2 py-1 rounded bg-red-950 text-red-400 text-xs font-medium">
                  CRISE OCÉANIQUE
                </span>
              )}
              {entity.requires_ocean_intervention && (
                <span className="px-2 py-1 rounded bg-blue-950 text-blue-400 text-xs font-medium">
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

export default function OceanIntelligenceDashboard() {
  const [data, setData] = useState<{ entities: Entity[]; summary: Summary } | null>(null);
  const [filter, setFilter] = useState<string>("all");
  const [patFilter, setPatFilter] = useState<string>("all");
  const [selected, setSelected] = useState<Entity | null>(null);

  useEffect(() => {
    fetch("/api/ocean-intelligence-engine")
      .then(r => r.json())
      .then(setData)
      .catch(console.error);
  }, []);

  if (!data) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center">
        <div className="text-blue-300 text-lg animate-pulse">
          Initialisation du Moteur d&apos;Intelligence Océanique...
        </div>
      </div>
    );
  }

  const { entities, summary } = data;
  const filtered = entities.filter(
    e =>
      (filter === "all" || e.ocean_risk === filter) &&
      (patFilter === "all" || e.ocean_pattern === patFilter)
  );

  const dists = [
    { title: "Niveau Risque Océanique",  counts: summary.risk_counts,     colors: RISK_COLORS     },
    { title: "Pattern Océanique",        counts: summary.pattern_counts,  colors: PATTERN_COLORS  },
    { title: "Sévérité Océanique",       counts: summary.severity_counts, colors: SEVERITY_COLORS },
    { title: "Action Déclenchée",        counts: summary.action_counts,   colors: ACTION_COLORS   },
  ] as Array<{ title: string; counts: Record<string, number>; colors: Record<string, string> }>;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {selected && <DetailModal entity={selected} onClose={() => setSelected(null)} />}

      <div>
        <h1 className="text-2xl font-bold text-blue-300">
          Intelligence Océanique &amp; Économie Bleue — Module 327
        </h1>
        <p className="text-teal-400/60 text-sm mt-1">
          Écologie · Économie · Sécurité · Géopolitique — Caelum Partners — Chaima Mhadbi, Fondatrice, Bruxelles
        </p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {[
          ["Entités Analysées",              summary.total,                                           "text-blue-300"],
          ["Crises Océaniques",              summary.ocean_crisis_count,                              "text-red-400"],
          ["Interventions Requises",         summary.ocean_intervention_count,                        "text-blue-400"],
          ["Composite Moyen",                summary.avg_ocean_composite.toFixed(1),                  "text-blue-300"],
          ["Indice Risque Océan Moyen",      summary.avg_estimated_ocean_risk_index.toFixed(2)+"/10", "text-teal-300"],
          ["Score Géopolitique Moyen",       summary.avg_geopolitical_score.toFixed(1),               "text-blue-300"],
        ].map(([l, v, c]) => (
          <div
            key={String(l)}
            className="bg-slate-900 border border-teal-700/30 rounded-xl p-3 text-center"
          >
            <div className={`text-xl font-bold ${c}`}>{v}</div>
            <div className="text-xs text-blue-300/40 mt-0.5 leading-tight">{l}</div>
          </div>
        ))}
      </div>

      {/* Gauge Rings */}
      <div className="bg-slate-900 border border-teal-700/30 rounded-xl p-5">
        <div className="grid grid-cols-4 gap-4">
          <GaugeRing value={summary.avg_ecological_score}   label="Score Écologie"    color="#10b981" />
          <GaugeRing value={summary.avg_economic_score}     label="Score Économie"    color="#3b82f6" />
          <GaugeRing value={summary.avg_security_score}     label="Score Sécurité"    color="#7c3aed" />
          <GaugeRing value={summary.avg_geopolitical_score} label="Score Géopolitique" color="#f59e0b" />
        </div>
      </div>

      {/* Distribution Bars */}
      <div className="bg-slate-900 border border-teal-700/30 rounded-xl p-5 grid grid-cols-1 md:grid-cols-2 gap-5">
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
                ? "bg-teal-900 border-teal-700 text-white"
                : "bg-slate-900 border-teal-700/30 text-blue-300/70 hover:text-white"
            }`}
          >
            {r}
          </button>
        ))}
        <span className="w-px h-5 self-center bg-teal-700/30" />
        {[
          "all",
          "none",
          "ecological_ocean_collapse",
          "maritime_security_crisis",
          "blue_economy_disruption",
          "ocean_sovereignty_war",
          "plastic_collapse",
        ].map(p => (
          <button
            key={p}
            onClick={() => setPatFilter(p)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${
              patFilter === p
                ? "bg-blue-950 border-blue-700 text-white"
                : "bg-slate-900 border-teal-700/30 text-blue-300/70 hover:text-white"
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
            className="bg-slate-900 border border-teal-700/30 rounded-xl p-4 cursor-pointer hover:border-teal-500 transition-colors"
          >
            <div className="flex items-center justify-between mb-1">
              <span className="font-bold text-white">{e.id}</span>
              <span className="text-xs text-blue-300/60">{e.region}</span>
            </div>
            <div className="text-xs text-slate-500 mb-2 capitalize">
              {e.ocean_domain.replace(/_/g, " ")}
            </div>
            <div className="flex gap-1 mb-3 flex-wrap">
              <span
                className={`px-2 py-0.5 rounded text-xs font-medium ${
                  RISK_BADGE[e.ocean_risk] || "bg-slate-700 text-slate-300"
                }`}
              >
                {e.ocean_risk}
              </span>
              <span
                className={`px-2 py-0.5 rounded text-xs font-medium ${
                  SEV_BADGE[e.ocean_severity] || "bg-slate-700 text-slate-300"
                }`}
              >
                {e.ocean_severity.replace(/_/g, " ")}
              </span>
            </div>
            <div className="text-2xl font-black text-white mb-1">
              {e.ocean_composite.toFixed(1)}
            </div>
            <div className="text-xs text-blue-300/60 mb-2 capitalize">
              {e.ocean_pattern.replace(/_/g, " ")}
            </div>
            <div className="flex gap-1 flex-wrap">
              {e.is_ocean_crisis && (
                <span className="px-1.5 py-0.5 rounded bg-red-950 text-red-400 text-xs">
                  CRISE
                </span>
              )}
              {e.requires_ocean_intervention && (
                <span className="px-1.5 py-0.5 rounded bg-blue-950 text-blue-400 text-xs">
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
