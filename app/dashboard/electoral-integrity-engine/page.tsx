"use client";
import { useEffect, useState } from "react";

type ElectoralEntity = {
  id: string;
  name: string;
  country: string;
  sector: string;
  composite_score: number;
  voter_suppression_score: number;
  electoral_fraud_score: number;
  media_manipulation_score: number;
  institutional_capture_score: number;
  risk_level: string;
  primary_pattern: string;
  key_signals: string[];
  estimated_electoral_index: number;
  last_updated: string;
};

type Summary = {
  total_entities: number;
  avg_composite: number;
  risk_distribution: Record<string, number>;
  pattern_distribution: Record<string, number>;
  top_risk_entities: string[];
  critical_alerts: string[] | number;
  last_analysis: string;
  engine_version: string;
  domain: string;
  confidence_score: number;
  data_sources: string[];
  entities: ElectoralEntity[];
  avg_estimated_electoral_index: number;
};

type ApiResponse = {
  entities: ElectoralEntity[];
  summary: Summary;
};

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

const RISK_COLORS: Record<string, string> = {
  faible: "#10b981",
  modéré: "#f59e0b",
  élevé: "#f97316",
  critique: "#ef4444",
};

const PATTERN_COLORS: Record<string, string> = {
  "Suppression Électorale": "#ef4444",
  "Fraude Systémique": "#dc2626",
  "Manipulation Médiatique": "#f97316",
  "Capture Institutionnelle": "#a855f7",
  "Désinformation Virale": "#f59e0b",
  "Aucun": "#10b981",
};

const RISK_BADGE: Record<string, string> = {
  critique: "bg-red-900/60 text-red-300 border border-red-700",
  élevé: "bg-orange-900/60 text-orange-300 border border-orange-700",
  modéré: "bg-yellow-900/60 text-yellow-300 border border-yellow-700",
  faible: "bg-emerald-900/60 text-emerald-300 border border-emerald-700",
};

const PATTERN_ACTIONS: Record<string, string> = {
  "Suppression Électorale": "Déploiement d'observateurs indépendants et saisine immédiate des instances internationales.",
  "Fraude Systémique": "Audit des procès-verbaux par commission multipartite et recomptage indépendant requis.",
  "Manipulation Médiatique": "Obligation d'accès équitable aux médias et surveillance des plateformes numériques.",
  "Capture Institutionnelle": "Réforme structurelle de la commission électorale avec membres indépendants.",
  "Désinformation Virale": "Fact-checking renforcé et partenariat avec les régulateurs des réseaux sociaux.",
  "Aucun": "Maintien des standards de transparence électorale actuels.",
};

function DetailModal({ entity, onClose }: { entity: ElectoralEntity; onClose: () => void }) {
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

        <div className="flex border-b border-slate-700">
          {(["scores", "signaux", "actions"] as const).map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`flex-1 py-2.5 text-sm font-medium capitalize transition-colors ${
                tab === t
                  ? "text-amber-400 border-b-2 border-amber-400 bg-slate-800/50"
                  : "text-slate-400 hover:text-white"
              }`}
            >
              {t.charAt(0).toUpperCase() + t.slice(1)}
            </button>
          ))}
        </div>

        <div className="p-5 min-h-[180px]">
          {tab === "scores" && (
            <div className="flex flex-col gap-3">
              <div className="flex items-center justify-between">
                <span className="text-slate-300 text-sm font-medium">Score Composite</span>
                <span className="text-white font-bold">{entity.composite_score}</span>
              </div>
              {[
                { label: "Suppression Électorale", value: entity.voter_suppression_score, color: "#ef4444" },
                { label: "Fraude Électorale", value: entity.electoral_fraud_score, color: "#f97316" },
                { label: "Manipulation Médias", value: entity.media_manipulation_score, color: "#dc2626" },
                { label: "Capture Institutionnelle", value: entity.institutional_capture_score, color: "#a855f7" },
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
                Index Intégrité Électorale:{" "}
                <span className="text-amber-300 font-medium">{entity.estimated_electoral_index}</span>
              </div>
            </div>
          )}

          {tab === "signaux" && (
            <div className="flex flex-col gap-3">
              <p className="text-slate-400 text-xs mb-1">Signaux d'atteinte à l'intégrité détectés</p>
              {entity.key_signals.map((sig, i) => (
                <div
                  key={i}
                  className="flex items-start gap-2 bg-slate-800/60 rounded-lg px-3 py-2 border border-slate-700/50"
                >
                  <span className="text-amber-400 mt-0.5 text-xs">▶</span>
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
                  Pattern Électoral
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
              <p className="text-xs text-slate-500">Dernière analyse: {entity.last_updated}</p>
            </div>
          )}
        </div>

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

export default function ElectoralIntegrityDashboard() {
  const [data, setData] = useState<ApiResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filterRisk, setFilterRisk] = useState<string>("all");
  const [selectedEntity, setSelectedEntity] = useState<ElectoralEntity | null>(null);

  useEffect(() => {
    fetch("/api/electoral-integrity-engine")
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
        <div className="text-slate-400 text-sm animate-pulse">
          Chargement du moteur intégrité électorale…
        </div>
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

  const avg = (key: keyof ElectoralEntity) => {
    if (entities.length === 0) return 0;
    const nums = entities.map((e) => e[key] as number);
    return Math.round((nums.reduce((a, b) => a + b, 0) / nums.length) * 100) / 100;
  };
  const avgSuppression = avg("voter_suppression_score");
  const avgFraud = avg("electoral_fraud_score");
  const avgMedia = avg("media_manipulation_score");
  const avgCapture = avg("institutional_capture_score");

  const filtered =
    filterRisk === "all" ? entities : entities.filter((e) => e.risk_level === filterRisk);

  const countryDist: Record<string, number> = {};
  for (const e of entities) countryDist[e.country] = (countryDist[e.country] || 0) + 1;
  const COUNTRY_COLORS: Record<string, string> = {
    Myanmar: "#ef4444",
    Venezuela: "#dc2626",
    Belarus: "#f97316",
    Bangladesh: "#f59e0b",
    Niger: "#a855f7",
    Tunisie: "#3b82f6",
    Allemagne: "#10b981",
    "Nouvelle-Zélande": "#06b6d4",
  };

  const FILTER_PILLS = [
    { key: "all", label: "Tous" },
    { key: "critique", label: "Critique" },
    { key: "élevé", label: "Élevé" },
    { key: "modéré", label: "Modéré" },
    { key: "faible", label: "Faible" },
  ];

  const criticalAlertsArr = Array.isArray(summary.critical_alerts)
    ? summary.critical_alerts as string[]
    : [];

  return (
    <div className="min-h-screen bg-slate-950 text-white">
      {selectedEntity && (
        <DetailModal entity={selectedEntity} onClose={() => setSelectedEntity(null)} />
      )}

      <div className="border-b border-slate-800 bg-slate-900/50 backdrop-blur-sm sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <div>
            <h1 className="text-xl font-bold text-white">Electoral Integrity Intelligence Engine</h1>
            <p className="text-slate-400 text-sm mt-0.5">
              Suppression, fraude, manipulation médiatique — surveillance intégrité démocratique
            </p>
          </div>
          <div className="flex items-center gap-2">
            <span className="text-xs text-slate-500">v{summary.engine_version}</span>
            <span className="text-xs bg-amber-900/40 text-amber-300 border border-amber-700/50 px-2 py-1 rounded-full">
              Confiance {Math.round(summary.confidence_score)}%
            </span>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-6 py-8 space-y-8">
        {/* KPI Cards */}
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-4">
          {[
            { label: "Total Entités", value: summary.total_entities, color: "text-white", sub: "acteurs surveillés" },
            { label: "Alertes Critiques", value: criticalAlertsArr.length || (summary.risk_distribution["critique"] ?? 0), color: "text-red-400", sub: "niveau critique" },
            { label: "Score Moyen", value: summary.avg_composite, color: "text-orange-400", sub: "composite global" },
            { label: "Index Électoral", value: summary.avg_estimated_electoral_index, color: "text-amber-400", sub: "indice atteinte /10" },
            { label: "Risque Élevé", value: summary.risk_distribution["élevé"] ?? 0, color: "text-orange-300", sub: "entités élevées" },
            { label: "Sources Renseignement", value: summary.data_sources.length, color: "text-green-400", sub: "flux actifs" },
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
            <GaugeRing value={avgSuppression} label="Suppression Électorale" color="#ef4444" />
            <GaugeRing value={avgFraud} label="Fraude Électorale" color="#f97316" />
            <GaugeRing value={avgMedia} label="Manipulation Médias" color="#dc2626" />
            <GaugeRing value={avgCapture} label="Capture Institutionnelle" color="#a855f7" />
          </div>
        </div>

        {/* Distribution bars */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div className="bg-slate-900 border border-slate-700/50 rounded-xl p-5 space-y-5">
            <h2 className="text-sm font-semibold text-slate-300">Distributions</h2>
            <DistBar title="Niveaux de Risque" counts={summary.risk_distribution} colors={RISK_COLORS} />
            <DistBar title="Patterns Électoraux" counts={summary.pattern_distribution} colors={PATTERN_COLORS} />
          </div>
          <div className="bg-slate-900 border border-slate-700/50 rounded-xl p-5 space-y-5">
            <h2 className="text-sm font-semibold text-slate-300">Géographie</h2>
            <DistBar title="Pays des Acteurs" counts={countryDist} colors={COUNTRY_COLORS} />
            <div className="bg-slate-800/40 rounded-lg p-3 mt-2">
              <p className="text-xs text-slate-400 font-medium mb-2">Top 3 Risques</p>
              {summary.top_risk_entities.map((name, i) => (
                <div key={name} className="flex items-center gap-2 mb-1">
                  <span className="text-xs text-red-400 font-bold">#{i + 1}</span>
                  <span className="text-xs text-slate-300">{name}</span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Filter pills */}
        <div className="flex items-center gap-2 flex-wrap">
          <span className="text-xs text-slate-400 font-medium mr-1">Filtrer:</span>
          {FILTER_PILLS.map(({ key, label }) => (
            <button
              key={key}
              onClick={() => setFilterRisk(key)}
              className={`text-xs px-3 py-1.5 rounded-full border transition-colors ${
                filterRisk === key
                  ? "bg-amber-700 border-amber-600 text-white"
                  : "border-slate-700 text-slate-400 hover:border-slate-500 hover:text-white"
              }`}
            >
              {label}
              {key !== "all" && (
                <span className="ml-1 opacity-60">({summary.risk_distribution[key] ?? 0})</span>
              )}
            </button>
          ))}
        </div>

        {/* Entity grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          {filtered.map((entity) => (
            <div
              key={entity.id}
              onClick={() => setSelectedEntity(entity)}
              className="bg-slate-900 border border-slate-700/50 rounded-xl p-4 cursor-pointer hover:border-amber-500/50 hover:bg-slate-800/60 transition-all group"
            >
              <div className="flex items-start justify-between gap-2 mb-3">
                <div>
                  <p className="text-white font-medium text-sm leading-tight group-hover:text-amber-300 transition-colors">
                    {entity.name}
                  </p>
                  <p className="text-slate-500 text-xs mt-0.5">{entity.id}</p>
                </div>
                <span className={`text-xs px-2 py-0.5 rounded-full font-medium whitespace-nowrap ${RISK_BADGE[entity.risk_level]}`}>
                  {entity.risk_level}
                </span>
              </div>

              <div className="flex items-center justify-between text-xs text-slate-400 mb-2">
                <span>{entity.country}</span>
                <span className="truncate ml-2">{entity.sector}</span>
              </div>

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

              <div className="mt-2 text-right text-xs text-slate-500">
                Index électoral:{" "}
                <span className="text-amber-400 font-medium">{entity.estimated_electoral_index}</span>
              </div>
            </div>
          ))}
        </div>

        {filtered.length === 0 && (
          <div className="text-center py-12 text-slate-500 text-sm">
            Aucune entité pour ce niveau de risque.
          </div>
        )}

        {/* Critical alerts */}
        {criticalAlertsArr.length > 0 && (
          <div className="bg-red-950/30 border border-red-800/50 rounded-xl p-5">
            <h2 className="text-sm font-semibold text-red-300 mb-3">Alertes Intégrité Électorale Critiques</h2>
            <div className="space-y-2">
              {criticalAlertsArr.map((alert, i) => (
                <div key={i} className="flex items-start gap-2">
                  <span className="text-red-400 text-xs mt-0.5">⚠</span>
                  <span className="text-xs text-red-200">{alert}</span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
