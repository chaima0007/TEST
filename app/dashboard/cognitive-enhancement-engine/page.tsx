"use client";
import { useEffect, useState } from "react";

// ── Types ──────────────────────────────────────────────────────────────────────

type CognitiveEntity = {
  entity_id: string;
  name: string;
  country: string;
  sector: string;
  composite_score: number;
  neuro_risk_score: number;
  ethical_concern_score: number;
  regulatory_gap_score: number;
  social_inequality_score: number;
  risk_level: string;
  primary_pattern: string;
  key_signals: string[];
  estimated_cognitive_index: number;
  last_updated: string;
};

type Summary = {
  total_entities: number;
  avg_composite: number;
  risk_distribution: Record<string, number>;
  pattern_distribution: Record<string, number>;
  top_risk_entities: string[];
  critical_alerts: number;
  last_analysis: string;
  engine_version: string;
  domain: string;
  confidence_score: number;
  data_sources: string[];
  entities: CognitiveEntity[];
  avg_estimated_cognitive_index: number;
};

type ApiResponse = {
  entities: CognitiveEntity[];
  summary: Summary;
};

// ── GaugeRing ──────────────────────────────────────────────────────────────────

function GaugeRing({ value, label, color }: { value: number; label: string; color: string }) {
  const r = 36;
  const circ = 2 * Math.PI * r;
  const fill = circ * (1 - value / 100);
  return (
    <div className="flex flex-col items-center gap-1">
      <svg width="88" height="88" viewBox="0 0 88 88">
        <circle cx="44" cy="44" r={r} fill="none" stroke="#0f172a" strokeWidth="8" />
        <circle
          cx="44"
          cy="44"
          r={r}
          fill="none"
          stroke={color}
          strokeWidth="8"
          strokeDasharray={circ}
          strokeDashoffset={fill}
          strokeLinecap="round"
          transform="rotate(-90 44 44)"
        />
        <text x="44" y="49" textAnchor="middle" fill="white" fontSize="13" fontWeight="bold">
          {Math.round(value)}
        </text>
      </svg>
      <span className="text-xs text-slate-400 text-center">{label}</span>
    </div>
  );
}

// ── DistBar ────────────────────────────────────────────────────────────────────

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
      <span className="text-xs text-slate-400 font-medium">{title}</span>
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
          <span key={k} className="text-xs text-slate-400">
            <span style={{ color: colors[k] || "#94a3b8" }}>■</span> {k} {v}
          </span>
        ))}
      </div>
    </div>
  );
}

// ── Color maps ─────────────────────────────────────────────────────────────────

const RISK_COLORS: Record<string, string> = {
  faible: "#10b981",
  modéré: "#f59e0b",
  élevé: "#f97316",
  critique: "#ef4444",
};

const PATTERN_COLORS: Record<string, string> = {
  "Interface Neurale Non Régulée": "#ef4444",
  "Augmentation Cognitive Inégalitaire": "#f97316",
  "Vide Réglementaire Nootropique": "#a855f7",
  "Dépendance Cognitive Induite": "#f59e0b",
  "Convergence BCI-IA Incontrôlée": "#dc2626",
};

const RISK_BADGE: Record<string, string> = {
  critique: "bg-red-900/60 text-red-300 border border-red-700",
  élevé: "bg-orange-900/60 text-orange-300 border border-orange-700",
  modéré: "bg-yellow-900/60 text-yellow-300 border border-yellow-700",
  faible: "bg-emerald-900/60 text-emerald-300 border border-emerald-700",
};

// ── Pattern action lookup ──────────────────────────────────────────────────────

const PATTERN_ACTIONS: Record<string, string> = {
  "Interface Neurale Non Régulée": "Suspension immédiate et audit réglementaire d'urgence",
  "Augmentation Cognitive Inégalitaire": "Cadre d'accès équitable et financement public requis",
  "Vide Réglementaire Nootropique": "Régulation pharmaceutique accélérée des agents cognitifs",
  "Dépendance Cognitive Induite": "Protocole de sevrage et suivi neurologique",
  "Convergence BCI-IA Incontrôlée": "Comité d'éthique inter-institutionnel requis",
};

// ── DetailModal ────────────────────────────────────────────────────────────────

function DetailModal({
  entity,
  onClose,
}: {
  entity: CognitiveEntity;
  onClose: () => void;
}) {
  const [tab, setTab] = useState<"scores" | "signaux" | "actions">("scores");

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm"
      onClick={onClose}
    >
      <div
        className="bg-slate-900 border border-slate-700 rounded-xl w-full max-w-lg mx-4 overflow-hidden shadow-2xl"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="p-5 border-b border-slate-700 flex items-start justify-between gap-3">
          <div>
            <h3 className="text-white font-semibold text-lg">{entity.name}</h3>
            <p className="text-slate-400 text-sm mt-0.5">
              {entity.country} · {entity.sector}
            </p>
          </div>
          <span className={`text-xs px-2 py-1 rounded-full font-medium ${RISK_BADGE[entity.risk_level]}`}>
            {entity.risk_level}
          </span>
        </div>

        {/* Tabs */}
        <div className="flex border-b border-slate-700">
          {(["scores", "signaux", "actions"] as const).map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`flex-1 py-2.5 text-sm font-medium capitalize transition-colors ${
                tab === t
                  ? "text-violet-400 border-b-2 border-violet-400 bg-slate-800/50"
                  : "text-slate-400 hover:text-white"
              }`}
            >
              {t.charAt(0).toUpperCase() + t.slice(1)}
            </button>
          ))}
        </div>

        {/* Tab content */}
        <div className="p-5 min-h-[180px]">
          {tab === "scores" && (
            <div className="flex flex-col gap-3">
              <div className="flex items-center justify-between">
                <span className="text-slate-300 text-sm font-medium">Score Composite</span>
                <span className="text-white font-bold">{entity.composite_score}</span>
              </div>
              {[
                { label: "Risque Neurologique", value: entity.neuro_risk_score, color: "#ef4444" },
                { label: "Préoccupation Éthique", value: entity.ethical_concern_score, color: "#f97316" },
                { label: "Vide Réglementaire", value: entity.regulatory_gap_score, color: "#a855f7" },
                { label: "Inégalité Sociale", value: entity.social_inequality_score, color: "#f59e0b" },
              ].map(({ label, value, color }) => (
                <div key={label}>
                  <div className="flex justify-between text-xs text-slate-400 mb-1">
                    <span>{label}</span>
                    <span>{value}</span>
                  </div>
                  <div className="h-2 bg-slate-800 rounded-full overflow-hidden">
                    <div
                      className="h-full rounded-full"
                      style={{ width: `${value}%`, background: color }}
                    />
                  </div>
                </div>
              ))}
              <div className="mt-2 text-xs text-slate-500">
                Index Cognitif Estimé: <span className="text-violet-300 font-medium">{entity.estimated_cognitive_index}</span>
              </div>
            </div>
          )}

          {tab === "signaux" && (
            <div className="flex flex-col gap-3">
              <p className="text-slate-400 text-xs mb-1">Signaux détectés pour cette entité</p>
              {entity.key_signals.map((sig, i) => (
                <div
                  key={i}
                  className="flex items-start gap-2 bg-slate-800/60 rounded-lg px-3 py-2 border border-slate-700/50"
                >
                  <span className="text-violet-400 mt-0.5 text-xs">▶</span>
                  <span className="text-slate-200 text-sm">{sig}</span>
                </div>
              ))}
              <div className="mt-2 text-xs text-slate-500">
                Pattern primaire:{" "}
                <span className="text-white font-medium">{entity.primary_pattern}</span>
              </div>
            </div>
          )}

          {tab === "actions" && (
            <div className="flex flex-col gap-4">
              <div className="bg-slate-800/60 rounded-lg p-4 border border-slate-700/50">
                <p className="text-xs text-slate-400 mb-2 font-medium uppercase tracking-wide">
                  Action Recommandée
                </p>
                <p className="text-slate-100 text-sm leading-relaxed">
                  {PATTERN_ACTIONS[entity.primary_pattern] || "Surveillance continue requise"}
                </p>
              </div>
              <div className="bg-slate-800/60 rounded-lg p-4 border border-slate-700/50">
                <p className="text-xs text-slate-400 mb-2 font-medium uppercase tracking-wide">
                  Pattern Détecté
                </p>
                <span
                  className="text-xs px-2 py-1 rounded-full"
                  style={{
                    background: `${PATTERN_COLORS[entity.primary_pattern] || "#475569"}22`,
                    color: PATTERN_COLORS[entity.primary_pattern] || "#94a3b8",
                    border: `1px solid ${PATTERN_COLORS[entity.primary_pattern] || "#475569"}44`,
                  }}
                >
                  {entity.primary_pattern}
                </span>
              </div>
              <p className="text-xs text-slate-500">
                Dernière analyse: {entity.last_updated}
              </p>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="px-5 py-3 border-t border-slate-700 flex justify-end">
          <button
            onClick={onClose}
            className="text-sm text-slate-400 hover:text-white px-4 py-1.5 rounded-lg hover:bg-slate-700 transition-colors"
          >
            Fermer
          </button>
        </div>
      </div>
    </div>
  );
}

// ── Main page ──────────────────────────────────────────────────────────────────

export default function CognitiveEnhancementDashboard() {
  const [data, setData] = useState<ApiResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filterRisk, setFilterRisk] = useState<string>("all");
  const [selectedEntity, setSelectedEntity] = useState<CognitiveEntity | null>(null);

  useEffect(() => {
    fetch("/api/cognitive-enhancement-engine")
      .then((r) => {
        if (!r.ok) throw new Error(`HTTP ${r.status}`);
        return r.json();
      })
      .then((json) => {
        const payload = json?.data ?? json;
        setData(payload);
      })
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center">
        <div className="text-slate-400 text-sm animate-pulse">Chargement du moteur cognitif…</div>
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center">
        <div className="text-red-400 text-sm">Erreur: {error ?? "Données indisponibles"}</div>
      </div>
    );
  }

  const { entities, summary } = data;

  // Averages for gauges
  const avg = (key: keyof CognitiveEntity) => {
    const nums = entities.map((e) => e[key] as number);
    return Math.round((nums.reduce((a, b) => a + b, 0) / nums.length) * 100) / 100;
  };
  const avgNeuro = avg("neuro_risk_score");
  const avgEthical = avg("ethical_concern_score");
  const avgRegulatory = avg("regulatory_gap_score");
  const avgInequality = avg("social_inequality_score");

  // Filtered entities
  const filtered =
    filterRisk === "all" ? entities : entities.filter((e) => e.risk_level === filterRisk);

  // Sector distribution
  const sectorDist: Record<string, number> = {};
  for (const e of entities) {
    sectorDist[e.sector] = (sectorDist[e.sector] || 0) + 1;
  }
  const SECTOR_COLORS: Record<string, string> = {
    Biotechnologie: "#ef4444",
    "Intelligence Artificielle": "#f97316",
    Pharmaceutique: "#a855f7",
    Neurotechnologie: "#f59e0b",
    "Recherche Médicale": "#3b82f6",
    Neurosciences: "#10b981",
    "Éthique & Recherche": "#06b6d4",
    "Santé Publique": "#84cc16",
  };

  // Country distribution
  const countryDist: Record<string, number> = {};
  for (const e of entities) {
    countryDist[e.country] = (countryDist[e.country] || 0) + 1;
  }
  const COUNTRY_COLORS: Record<string, string> = {
    USA: "#ef4444",
    Chine: "#f97316",
    Suisse: "#a855f7",
    "Royaume-Uni": "#f59e0b",
    Allemagne: "#3b82f6",
    France: "#10b981",
    Canada: "#06b6d4",
    Suède: "#84cc16",
  };

  const FILTER_PILLS = [
    { key: "all", label: "Tous" },
    { key: "critique", label: "Critique" },
    { key: "élevé", label: "Élevé" },
    { key: "modéré", label: "Modéré" },
    { key: "faible", label: "Faible" },
  ];

  return (
    <div className="min-h-screen bg-slate-950 text-white">
      {selectedEntity && (
        <DetailModal entity={selectedEntity} onClose={() => setSelectedEntity(null)} />
      )}

      {/* Header */}
      <div className="border-b border-slate-800 bg-slate-900/50 backdrop-blur-sm sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <div>
            <h1 className="text-xl font-bold text-white">Cognitive Enhancement Intelligence</h1>
            <p className="text-slate-400 text-sm mt-0.5">
              Surveillance des technologies d&apos;augmentation cognitive
            </p>
          </div>
          <div className="flex items-center gap-2">
            <span className="text-xs text-slate-500">v{summary.engine_version}</span>
            <span className="text-xs bg-violet-900/40 text-violet-300 border border-violet-700/50 px-2 py-1 rounded-full">
              Confiance {Math.round(summary.confidence_score * 100)}%
            </span>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-6 py-8 space-y-8">
        {/* KPI Cards */}
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-4">
          {[
            {
              label: "Total Entités",
              value: summary.total_entities,
              color: "text-white",
              sub: "entités surveillées",
            },
            {
              label: "Alertes Critiques",
              value: summary.critical_alerts,
              color: "text-red-400",
              sub: "niveau critique",
            },
            {
              label: "Score Moyen",
              value: summary.avg_composite,
              color: "text-orange-400",
              sub: "composite global",
            },
            {
              label: "Index Cognitif",
              value: summary.avg_estimated_cognitive_index,
              color: "text-violet-400",
              sub: "indice estimé /10",
            },
            {
              label: "Entités Élevées",
              value: summary.risk_distribution["élevé"] ?? 0,
              color: "text-orange-300",
              sub: "risque élevé",
            },
            {
              label: "Sources Données",
              value: summary.data_sources.length,
              color: "text-cyan-400",
              sub: "flux actifs",
            },
          ].map(({ label, value, color, sub }) => (
            <div
              key={label}
              className="bg-slate-900 border border-slate-700/50 rounded-xl p-4 flex flex-col gap-1"
            >
              <span className="text-xs text-slate-400 font-medium">{label}</span>
              <span className={`text-2xl font-bold ${color}`}>{value}</span>
              <span className="text-xs text-slate-500">{sub}</span>
            </div>
          ))}
        </div>

        {/* Gauges */}
        <div className="bg-slate-900 border border-slate-700/50 rounded-xl p-6">
          <h2 className="text-sm font-semibold text-slate-300 mb-5">Scores Moyens par Dimension</h2>
          <div className="flex flex-wrap gap-8 justify-around">
            <GaugeRing value={avgNeuro} label="Risque Neurologique" color="#ef4444" />
            <GaugeRing value={avgEthical} label="Préoccupation Éthique" color="#f97316" />
            <GaugeRing value={avgRegulatory} label="Vide Réglementaire" color="#a855f7" />
            <GaugeRing value={avgInequality} label="Inégalité Sociale" color="#f59e0b" />
          </div>
        </div>

        {/* Distribution bars */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div className="bg-slate-900 border border-slate-700/50 rounded-xl p-5 space-y-5">
            <h2 className="text-sm font-semibold text-slate-300">Distributions</h2>
            <DistBar title="Niveaux de Risque" counts={summary.risk_distribution} colors={RISK_COLORS} />
            <DistBar
              title="Patterns (top 4)"
              counts={Object.fromEntries(
                Object.entries(summary.pattern_distribution)
                  .sort(([, a], [, b]) => b - a)
                  .slice(0, 4)
              )}
              colors={PATTERN_COLORS}
            />
          </div>
          <div className="bg-slate-900 border border-slate-700/50 rounded-xl p-5 space-y-5">
            <h2 className="text-sm font-semibold text-slate-300">Répartitions</h2>
            <DistBar title="Secteurs d&apos;Activité" counts={sectorDist} colors={SECTOR_COLORS} />
            <DistBar title="Pays / Régions" counts={countryDist} colors={COUNTRY_COLORS} />
          </div>
        </div>

        {/* Filter pills + entities */}
        <div>
          <div className="flex items-center gap-2 mb-4 flex-wrap">
            <span className="text-xs text-slate-400 font-medium mr-1">Filtrer:</span>
            {FILTER_PILLS.map(({ key, label }) => (
              <button
                key={key}
                onClick={() => setFilterRisk(key)}
                className={`text-xs px-3 py-1.5 rounded-full border transition-colors ${
                  filterRisk === key
                    ? "bg-violet-600 border-violet-500 text-white"
                    : "border-slate-700 text-slate-400 hover:border-slate-500 hover:text-white"
                }`}
              >
                {label}
                {key !== "all" && (
                  <span className="ml-1 opacity-60">
                    ({summary.risk_distribution[key] ?? 0})
                  </span>
                )}
              </button>
            ))}
          </div>

          {/* Entity cards grid */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {filtered.map((entity) => (
              <div
                key={entity.entity_id}
                onClick={() => setSelectedEntity(entity)}
                className="bg-slate-900 border border-slate-700/50 rounded-xl p-4 cursor-pointer hover:border-violet-500/50 hover:bg-slate-800/60 transition-all group"
              >
                <div className="flex items-start justify-between gap-2 mb-3">
                  <div>
                    <p className="text-white font-medium text-sm leading-tight group-hover:text-violet-300 transition-colors">
                      {entity.name}
                    </p>
                    <p className="text-slate-500 text-xs mt-0.5">{entity.entity_id}</p>
                  </div>
                  <span
                    className={`text-xs px-2 py-0.5 rounded-full font-medium whitespace-nowrap ${RISK_BADGE[entity.risk_level]}`}
                  >
                    {entity.risk_level}
                  </span>
                </div>

                <div className="flex items-center justify-between text-xs text-slate-400 mb-2">
                  <span>{entity.country}</span>
                  <span>{entity.sector}</span>
                </div>

                {/* Composite score bar */}
                <div className="mb-3">
                  <div className="flex justify-between text-xs text-slate-500 mb-1">
                    <span>Score composite</span>
                    <span className="font-medium text-slate-300">{entity.composite_score}</span>
                  </div>
                  <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
                    <div
                      className="h-full rounded-full transition-all"
                      style={{
                        width: `${entity.composite_score}%`,
                        background: RISK_COLORS[entity.risk_level] || "#475569",
                      }}
                    />
                  </div>
                </div>

                {/* Pattern badge */}
                <div
                  className="text-xs px-2 py-1 rounded text-center truncate"
                  style={{
                    background: `${PATTERN_COLORS[entity.primary_pattern] || "#475569"}18`,
                    color: PATTERN_COLORS[entity.primary_pattern] || "#94a3b8",
                    border: `1px solid ${PATTERN_COLORS[entity.primary_pattern] || "#475569"}30`,
                  }}
                >
                  {entity.primary_pattern}
                </div>

                {/* Index cognitif */}
                <div className="mt-2 text-right text-xs text-slate-500">
                  Index cognitif:{" "}
                  <span className="text-violet-400 font-medium">{entity.estimated_cognitive_index}</span>
                </div>
              </div>
            ))}
          </div>

          {filtered.length === 0 && (
            <div className="text-center py-12 text-slate-500 text-sm">
              Aucune entité pour ce niveau de risque.
            </div>
          )}
        </div>

        {/* Top risk + data sources */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div className="bg-slate-900 border border-slate-700/50 rounded-xl p-5">
            <h2 className="text-sm font-semibold text-slate-300 mb-3">Entités à Plus Haut Risque</h2>
            <div className="space-y-2">
              {summary.top_risk_entities.map((name, i) => (
                <div key={name} className="flex items-center gap-3">
                  <span className="text-xs text-slate-500 w-4">#{i + 1}</span>
                  <span className="text-sm text-slate-200">{name}</span>
                </div>
              ))}
            </div>
          </div>
          <div className="bg-slate-900 border border-slate-700/50 rounded-xl p-5">
            <h2 className="text-sm font-semibold text-slate-300 mb-3">Sources de Données</h2>
            <div className="space-y-1.5">
              {summary.data_sources.map((src) => (
                <div key={src} className="flex items-center gap-2">
                  <span className="w-1.5 h-1.5 rounded-full bg-cyan-400 flex-shrink-0" />
                  <span className="text-xs text-slate-400">{src}</span>
                </div>
              ))}
            </div>
            <p className="text-xs text-slate-600 mt-3">
              Dernière analyse: {summary.last_analysis}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
