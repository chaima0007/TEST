"use client";
import { useEffect, useState } from "react";

type AlgaeEntity = {
  entity_id: string;
  name: string;
  country: string;
  sector: string;
  composite_score: number;
  productivity_score: number;
  sustainability_score: number;
  scalability_score: number;
  efficiency_score: number;
  risk_level: string;
  primary_pattern: string;
  key_signals: string[];
  estimated_algae_index: number;
  last_updated: string;
  facility_count: number;
};

type AlgaeSummary = {
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
  entities: AlgaeEntity[];
  avg_estimated_algae_index: number;
};

const RISK_COLORS: Record<string, string> = {
  faible: "#10b981",
  modéré: "#f59e0b",
  élevé: "#3b82f6",
  critique: "#ef4444",
};

const RISK_BADGE: Record<string, string> = {
  faible: "bg-emerald-900 text-emerald-300",
  modéré: "bg-amber-900 text-amber-300",
  élevé: "bg-blue-900 text-blue-300",
  critique: "bg-red-950 text-red-400",
};

const PATTERN_COLORS: Record<string, string> = {
  rendement_critique: "#ef4444",
  durabilite_compromise: "#f97316",
  echelle_bloquee: "#a855f7",
  efficience_degradee: "#06b6d4",
  systeme_algal_stable: "#10b981",
};

const GAUGE_COLORS = ["#22c55e", "#06b6d4", "#a855f7", "#f59e0b"];

function GaugeRing({ value, label, color }: { value: number; label: string; color: string }) {
  const r = 36;
  const circ = 2 * Math.PI * r;
  const fill = circ * (1 - value / 100);
  return (
    <div className="flex flex-col items-center gap-1">
      <svg width="88" height="88" viewBox="0 0 88 88">
        <circle cx="44" cy="44" r={r} fill="none" stroke="#0a1628" strokeWidth="8" />
        <circle
          cx="44" cy="44" r={r} fill="none"
          stroke={color} strokeWidth="8"
          strokeDasharray={circ} strokeDashoffset={fill}
          strokeLinecap="round" transform="rotate(-90 44 44)"
        />
        <text x="44" y="49" textAnchor="middle" fill="white" fontSize="13" fontWeight="bold">
          {Math.round(value)}
        </text>
      </svg>
      <span className="text-xs text-blue-300/70 text-center leading-tight">{label}</span>
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
            <span style={{ color: colors[k] || "#94a3b8" }}>■</span>{" "}
            {k.replace(/_/g, " ")} {v}
          </span>
        ))}
      </div>
    </div>
  );
}

function DetailModal({ entity, onClose }: { entity: AlgaeEntity; onClose: () => void }) {
  const [tab, setTab] = useState<"scores" | "signaux" | "actions">("scores");

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
        className="bg-slate-950 border border-blue-700/30 rounded-xl w-full max-w-lg p-6 shadow-2xl"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="flex items-center justify-between mb-4">
          <div>
            <span className="text-lg font-bold text-white">{entity.name}</span>
            <span className="ml-2 text-blue-400 text-xs">{entity.country}</span>
            <span className="ml-2 text-slate-500 text-xs">{entity.sector}</span>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl leading-none">
            ✕
          </button>
        </div>

        <div className="flex gap-2 mb-4">
          {(["scores", "signaux", "actions"] as const).map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`px-3 py-1 rounded text-xs font-medium transition-colors ${
                tab === t
                  ? "bg-blue-900 text-white"
                  : "bg-slate-900 text-slate-400 hover:text-white"
              }`}
            >
              {t === "scores" ? "Scores" : t === "signaux" ? "Signaux" : "Actions"}
            </button>
          ))}
        </div>

        {tab === "scores" && (
          <div className="grid grid-cols-2 gap-3 text-sm">
            {[
              ["Productivité", entity.productivity_score, GAUGE_COLORS[0]],
              ["Durabilité", entity.sustainability_score, GAUGE_COLORS[1]],
              ["Scalabilité", entity.scalability_score, GAUGE_COLORS[2]],
              ["Efficience", entity.efficiency_score, GAUGE_COLORS[3]],
            ].map(([l, v, c]) => (
              <div
                key={String(l)}
                className="bg-slate-900 border border-blue-700/20 rounded-lg p-3"
              >
                <div className="text-blue-300/60 text-xs mb-1">{String(l)}</div>
                <div className="text-white font-bold text-lg">{Number(v).toFixed(1)}</div>
                <div className="h-1.5 rounded mt-1 bg-slate-800">
                  <div
                    className="h-1.5 rounded"
                    style={{
                      width: `${Math.min(Number(v), 100)}%`,
                      background: String(c),
                    }}
                  />
                </div>
              </div>
            ))}
            <div className="col-span-2 bg-slate-900 border border-blue-700/20 rounded-lg p-3">
              <div className="text-blue-300/60 text-xs mb-1">Score Composite</div>
              <div className="text-white font-bold text-2xl">
                {entity.composite_score.toFixed(2)}
              </div>
            </div>
            <div className="col-span-2 bg-slate-900 border border-blue-700/20 rounded-lg p-3">
              <div className="text-blue-300/60 text-xs mb-1">Index Algues Estimé</div>
              <div className="text-teal-400 font-bold text-xl">
                {entity.estimated_algae_index.toFixed(2)}
              </div>
            </div>
          </div>
        )}

        {tab === "signaux" && (
          <div className="space-y-3">
            <div className="flex gap-2 flex-wrap mb-3">
              <span
                className={`px-2 py-0.5 rounded text-xs font-medium ${
                  RISK_BADGE[entity.risk_level] || "bg-slate-700 text-slate-300"
                }`}
              >
                {entity.risk_level}
              </span>
              <span className="px-2 py-0.5 rounded text-xs font-medium bg-slate-800 text-slate-300">
                {entity.primary_pattern.replace(/_/g, " ")}
              </span>
            </div>
            {entity.key_signals.map((sig, i) => (
              <div
                key={i}
                className="bg-slate-900 border border-blue-700/20 rounded-lg p-3 text-sm text-slate-200 leading-relaxed"
              >
                {sig}
              </div>
            ))}
          </div>
        )}

        {tab === "actions" && (
          <div className="space-y-3 text-sm">
            <div className="bg-slate-900 border border-blue-700/20 rounded-lg p-3">
              <div className="text-blue-300/60 text-xs mb-1">Secteur</div>
              <div className="text-white font-medium">{entity.sector}</div>
            </div>
            <div className="bg-slate-900 border border-blue-700/20 rounded-lg p-3">
              <div className="text-blue-300/60 text-xs mb-1">Patron Détecté</div>
              <div className="text-blue-300 font-medium">
                {entity.primary_pattern.replace(/_/g, " ")}
              </div>
            </div>
            <div className="bg-slate-900 border border-blue-700/20 rounded-lg p-3">
              <div className="text-blue-300/60 text-xs mb-1">Installations</div>
              <div className="text-amber-400 font-bold">{entity.facility_count}</div>
            </div>
            <div className="bg-slate-900 border border-blue-700/20 rounded-lg p-3">
              <div className="text-blue-300/60 text-xs mb-1">Dernière Mise à Jour</div>
              <div className="text-slate-300">{entity.last_updated}</div>
            </div>
            <div className="bg-slate-900 border border-blue-700/20 rounded-lg p-3">
              <div className="text-blue-300/60 text-xs mb-1">Index Algues</div>
              <div className="text-teal-400 font-bold">{entity.estimated_algae_index.toFixed(2)} / 10</div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

const FILTER_OPTIONS = ["Tous", "Critique", "Élevé", "Modéré", "Faible"];

const FILTER_MAP: Record<string, string> = {
  Tous: "",
  Critique: "critique",
  Élevé: "élevé",
  Modéré: "modéré",
  Faible: "faible",
};

export default function AlgaeDashboard() {
  const [data, setData] = useState<AlgaeSummary | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filter, setFilter] = useState("Tous");
  const [selected, setSelected] = useState<AlgaeEntity | null>(null);

  useEffect(() => {
    fetch("/api/algae-energy-engine")
      .then((r) => r.json())
      .then((d) => {
        setData(d);
        setLoading(false);
      })
      .catch(() => {
        setError("Erreur de chargement des données.");
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center text-white">
        Chargement...
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center text-red-400">
        {error || "Données indisponibles"}
      </div>
    );
  }

  const entities = data.entities ?? [];
  const filtered = filter === "Tous"
    ? entities
    : entities.filter((e) => e.risk_level === FILTER_MAP[filter]);

  const avgProductivity =
    entities.reduce((s, e) => s + e.productivity_score, 0) / (entities.length || 1);
  const avgSustainability =
    entities.reduce((s, e) => s + e.sustainability_score, 0) / (entities.length || 1);
  const avgScalability =
    entities.reduce((s, e) => s + e.scalability_score, 0) / (entities.length || 1);
  const avgEfficiency =
    entities.reduce((s, e) => s + e.efficiency_score, 0) / (entities.length || 1);

  const rd = data.risk_distribution ?? {};
  const pd = data.pattern_distribution ?? {};

  return (
    <div className="min-h-screen bg-slate-950 text-white p-4 md:p-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-2xl md:text-3xl font-bold text-white mb-1">
          Algae Energy Intelligence Engine
        </h1>
        <p className="text-blue-300/60 text-sm">
          Caelum Partners — Analyse bioénergie algale • v{data.engine_version} •{" "}
          {data.last_analysis}
        </p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 xl:grid-cols-6 gap-3 mb-8">
        {[
          { label: "Total Entités", value: data.total_entities, color: "text-white" },
          {
            label: "Critique",
            value: rd["critique"] ?? 0,
            color: "text-red-400",
          },
          {
            label: "Élevé",
            value: rd["élevé"] ?? 0,
            color: "text-blue-400",
          },
          {
            label: "Composite Moyen",
            value: data.avg_composite.toFixed(1),
            color: "text-amber-400",
          },
          {
            label: "Index Algues",
            value: data.avg_estimated_algae_index.toFixed(2),
            color: "text-teal-400",
          },
          {
            label: "Confiance",
            value: `${(data.confidence_score * 100).toFixed(0)}%`,
            color: "text-emerald-400",
          },
        ].map(({ label, value, color }) => (
          <div
            key={label}
            className="bg-slate-900 border border-blue-700/30 rounded-xl p-4 flex flex-col gap-1"
          >
            <span className="text-blue-300/60 text-xs">{label}</span>
            <span className={`text-2xl font-bold ${color}`}>{value}</span>
          </div>
        ))}
      </div>

      {/* Gauges */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8">
        <div className="bg-slate-900 border border-blue-700/30 rounded-xl p-5">
          <h2 className="text-sm font-semibold text-blue-300/70 mb-4 uppercase tracking-wide">
            Scores Moyens
          </h2>
          <div className="grid grid-cols-4 gap-2">
            <GaugeRing value={avgProductivity} label="Productivité" color={GAUGE_COLORS[0]} />
            <GaugeRing value={avgSustainability} label="Durabilité" color={GAUGE_COLORS[1]} />
            <GaugeRing value={avgScalability} label="Scalabilité" color={GAUGE_COLORS[2]} />
            <GaugeRing value={avgEfficiency} label="Efficience" color={GAUGE_COLORS[3]} />
          </div>
        </div>

        <div className="bg-slate-900 border border-blue-700/30 rounded-xl p-5 flex flex-col gap-4">
          <h2 className="text-sm font-semibold text-blue-300/70 uppercase tracking-wide">
            Distributions
          </h2>
          <DistBar title="Risque" counts={rd} colors={RISK_COLORS} />
          <DistBar title="Patron" counts={pd} colors={PATTERN_COLORS} />
        </div>
      </div>

      {/* Alerts */}
      {data.critical_alerts.length > 0 && (
        <div className="bg-red-950/40 border border-red-700/30 rounded-xl p-4 mb-8">
          <h2 className="text-red-400 text-sm font-semibold mb-2 uppercase tracking-wide">
            Alertes Critiques
          </h2>
          <ul className="space-y-1">
            {data.critical_alerts.map((alert, i) => (
              <li key={i} className="text-red-300 text-sm">
                • {alert}
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Filter Pills */}
      <div className="flex flex-wrap gap-2 mb-5">
        {FILTER_OPTIONS.map((opt) => (
          <button
            key={opt}
            onClick={() => setFilter(opt)}
            className={`px-3 py-1 rounded-full text-xs font-medium transition-colors border ${
              filter === opt
                ? "bg-blue-700 border-blue-500 text-white"
                : "bg-slate-900 border-blue-700/30 text-slate-400 hover:text-white"
            }`}
          >
            {opt}
          </button>
        ))}
        <span className="text-xs text-blue-300/40 self-center ml-1">
          {filtered.length} entité{filtered.length !== 1 ? "s" : ""}
        </span>
      </div>

      {/* Entity Cards Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 mb-8">
        {filtered.map((entity) => (
          <div
            key={entity.entity_id}
            onClick={() => setSelected(entity)}
            className="bg-slate-900 border border-blue-700/30 rounded-xl p-4 cursor-pointer hover:border-blue-500/60 transition-colors"
          >
            <div className="flex items-start justify-between mb-2">
              <div>
                <div className="text-white font-semibold text-sm leading-tight">
                  {entity.name}
                </div>
                <div className="text-blue-300/50 text-xs mt-0.5">{entity.entity_id}</div>
              </div>
              <span
                className={`px-2 py-0.5 rounded text-xs font-medium shrink-0 ml-2 ${
                  RISK_BADGE[entity.risk_level] || "bg-slate-700 text-slate-300"
                }`}
              >
                {entity.risk_level}
              </span>
            </div>

            <div className="text-slate-400 text-xs mb-1">{entity.country} — {entity.sector}</div>

            <div className="flex items-center justify-between mb-3">
              <span className="text-xs text-blue-300/50">Composite</span>
              <span
                className="text-lg font-bold"
                style={{ color: RISK_COLORS[entity.risk_level] || "#fff" }}
              >
                {entity.composite_score.toFixed(1)}
              </span>
            </div>

            <div className="h-1.5 rounded bg-slate-800 mb-3">
              <div
                className="h-1.5 rounded transition-all"
                style={{
                  width: `${Math.min(entity.composite_score, 100)}%`,
                  background: RISK_COLORS[entity.risk_level] || "#475569",
                }}
              />
            </div>

            <div className="grid grid-cols-2 gap-1 text-xs mb-3">
              <span className="text-slate-500">Productivité</span>
              <span className="text-right text-green-400">{entity.productivity_score.toFixed(0)}</span>
              <span className="text-slate-500">Durabilité</span>
              <span className="text-right text-cyan-400">{entity.sustainability_score.toFixed(0)}</span>
              <span className="text-slate-500">Scalabilité</span>
              <span className="text-right text-purple-400">{entity.scalability_score.toFixed(0)}</span>
              <span className="text-slate-500">Efficience</span>
              <span className="text-right text-amber-400">{entity.efficiency_score.toFixed(0)}</span>
            </div>

            <div className="flex items-center justify-between">
              <span
                className="text-xs px-2 py-0.5 rounded"
                style={{
                  background: `${PATTERN_COLORS[entity.primary_pattern] || "#475569"}22`,
                  color: PATTERN_COLORS[entity.primary_pattern] || "#94a3b8",
                }}
              >
                {entity.primary_pattern.replace(/_/g, " ")}
              </span>
              <span className="text-xs text-teal-400">
                {entity.facility_count} site{entity.facility_count !== 1 ? "s" : ""}
              </span>
            </div>
          </div>
        ))}
      </div>

      {/* Data Sources */}
      <div className="bg-slate-900 border border-blue-700/30 rounded-xl p-4">
        <h2 className="text-xs font-semibold text-blue-300/60 uppercase tracking-wide mb-2">
          Sources de Données
        </h2>
        <div className="flex flex-wrap gap-2">
          {data.data_sources.map((src) => (
            <span
              key={src}
              className="px-2 py-0.5 bg-slate-800 border border-blue-700/20 rounded text-xs text-blue-300/60"
            >
              {src.replace(/_/g, " ")}
            </span>
          ))}
        </div>
      </div>

      {/* Detail Modal */}
      {selected && (
        <DetailModal entity={selected} onClose={() => setSelected(null)} />
      )}
    </div>
  );
}
