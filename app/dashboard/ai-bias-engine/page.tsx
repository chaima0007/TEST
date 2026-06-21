"use client";

import { useEffect, useState } from "react";

interface Entity {
  id: string;
  name: string;
  country: string;
  sector: string;
  composite_score: number;
  algorithmic_score: number;
  data_score: number;
  impact_score: number;
  transparency_score: number;
  risk_level: string;
  primary_pattern: string;
  key_signals: string[];
  estimated_bias_index: number;
  last_updated: string;
  model_count: number;
}

interface SummaryData {
  total_entities: number;
  avg_composite: number;
  risk_distribution: { critique: number; élevé: number; modéré: number; faible: number };
  pattern_distribution: Record<string, number>;
  top_risk_entities: string[];
  critical_alerts: string[];
  last_analysis: string;
  engine_version: string;
  domain: string;
  confidence_score: number;
  data_sources: string[];
  entities: Entity[];
  avg_estimated_bias_index: number;
}

// ── GaugeRing ──────────────────────────────────────────────────────────────
function GaugeRing({ value, label, color }: { value: number; label: string; color: string }) {
  const r = 36;
  const circumference = 2 * Math.PI * r;
  const progress = Math.min(Math.max(value / 100, 0), 1);
  const dashOffset = circumference * (1 - progress);

  return (
    <div className="flex flex-col items-center gap-1">
      <svg width="96" height="96" viewBox="0 0 96 96">
        <circle cx="48" cy="48" r={r} fill="none" stroke="#1e293b" strokeWidth="8" />
        <circle
          cx="48"
          cy="48"
          r={r}
          fill="none"
          stroke={color}
          strokeWidth="8"
          strokeDasharray={circumference}
          strokeDashoffset={dashOffset}
          strokeLinecap="round"
          transform="rotate(-90 48 48)"
        />
        <text x="48" y="48" textAnchor="middle" dominantBaseline="middle" fill="white" fontSize="14" fontWeight="bold">
          {Math.round(value)}
        </text>
      </svg>
      <span className="text-xs text-slate-400 text-center">{label}</span>
    </div>
  );
}

// ── DistBar ────────────────────────────────────────────────────────────────
function DistBar({ label, value, max, color }: { label: string; value: number; max: number; color: string }) {
  const pct = max > 0 ? (value / max) * 100 : 0;
  return (
    <div className="flex items-center gap-3 w-full">
      <span className="text-xs text-slate-400 w-32 shrink-0">{label}</span>
      <div className="flex-1 bg-slate-800 rounded-full h-2">
        <div className="h-2 rounded-full transition-all duration-500" style={{ width: `${pct}%`, backgroundColor: color }} />
      </div>
      <span className="text-xs text-slate-300 w-6 text-right">{value}</span>
    </div>
  );
}

// ── Risk colour helpers ────────────────────────────────────────────────────
function riskColor(level: string): string {
  switch (level) {
    case "critique": return "#ef4444";
    case "élevé":    return "#f97316";
    case "modéré":   return "#eab308";
    case "faible":   return "#22c55e";
    default:         return "#94a3b8";
  }
}

function riskBadgeClass(level: string): string {
  switch (level) {
    case "critique": return "bg-red-900/60 text-red-300 border border-red-700/40";
    case "élevé":    return "bg-orange-900/60 text-orange-300 border border-orange-700/40";
    case "modéré":   return "bg-yellow-900/60 text-yellow-300 border border-yellow-700/40";
    case "faible":   return "bg-green-900/60 text-green-300 border border-green-700/40";
    default:         return "bg-slate-700/60 text-slate-300";
  }
}

// ── DetailModal ────────────────────────────────────────────────────────────
function DetailModal({ entity, onClose }: { entity: Entity; onClose: () => void }) {
  const [tab, setTab] = useState<"Scores" | "Signaux" | "Actions">("Scores");
  const tabs: Array<"Scores" | "Signaux" | "Actions"> = ["Scores", "Signaux", "Actions"];

  const actionsByPattern: Record<string, string> = {
    biais_algorithmique: "Audit immédiat des algorithmes de décision automatisée",
    biais_données: "Révision des jeux de données d'entraînement et de validation",
    impact_discriminatoire: "Évaluation d'impact sur les groupes protégés requise",
    opacite_systematique: "Mise en place d'un cadre d'explicabilité (XAI)",
    equilibre_biais: "Surveillance continue et rapports périodiques",
  };

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/70"
      onClick={onClose}
    >
      <div
        className="bg-slate-900 border border-blue-700/30 rounded-xl w-full max-w-lg mx-4 shadow-2xl"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="flex items-start justify-between p-5 border-b border-slate-800">
          <div>
            <h2 className="text-lg font-bold text-white">{entity.name}</h2>
            <p className="text-sm text-slate-400">{entity.sector} · {entity.country}</p>
          </div>
          <span className={`px-2 py-1 rounded text-xs font-semibold ${riskBadgeClass(entity.risk_level)}`}>
            {entity.risk_level.toUpperCase()}
          </span>
        </div>

        {/* Tabs */}
        <div className="flex border-b border-slate-800">
          {tabs.map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`flex-1 py-2.5 text-sm font-medium transition-colors ${
                tab === t
                  ? "text-blue-400 border-b-2 border-blue-400"
                  : "text-slate-400 hover:text-white"
              }`}
            >
              {t}
            </button>
          ))}
        </div>

        {/* Tab content */}
        <div className="p-5 min-h-[200px]">
          {tab === "Scores" && (
            <div className="space-y-3">
              {[
                { label: "Composite", value: entity.composite_score },
                { label: "Algorithmique (×0.30)", value: entity.algorithmic_score },
                { label: "Données (×0.25)", value: entity.data_score },
                { label: "Impact (×0.25)", value: entity.impact_score },
                { label: "Transparence (×0.20)", value: entity.transparency_score },
              ].map((item) => (
                <div key={item.label} className="flex justify-between items-center">
                  <span className="text-sm text-slate-400">{item.label}</span>
                  <div className="flex items-center gap-3">
                    <div className="w-32 bg-slate-800 rounded-full h-1.5">
                      <div
                        className="h-1.5 rounded-full"
                        style={{ width: `${item.value}%`, backgroundColor: riskColor(entity.risk_level) }}
                      />
                    </div>
                    <span className="text-sm font-semibold text-white w-10 text-right">
                      {item.value.toFixed(1)}
                    </span>
                  </div>
                </div>
              ))}
              <div className="mt-4 pt-4 border-t border-slate-800 flex justify-between text-sm">
                <span className="text-slate-400">Index de biais estimé</span>
                <span className="font-bold text-blue-400">{entity.estimated_bias_index} / 10</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-slate-400">Modèles analysés</span>
                <span className="font-bold text-white">{entity.model_count}</span>
              </div>
            </div>
          )}

          {tab === "Signaux" && (
            <ul className="space-y-3">
              {entity.key_signals.map((signal, i) => (
                <li key={i} className="flex gap-3 text-sm text-slate-300">
                  <span className="text-blue-400 font-bold shrink-0">{i + 1}.</span>
                  <span>{signal}</span>
                </li>
              ))}
            </ul>
          )}

          {tab === "Actions" && (
            <div className="space-y-4">
              <div className="bg-slate-800/50 rounded-lg p-4">
                <p className="text-xs text-slate-500 mb-1">Pattern détecté</p>
                <p className="text-sm font-mono text-blue-300">{entity.primary_pattern}</p>
              </div>
              <div className="bg-slate-800/50 rounded-lg p-4">
                <p className="text-xs text-slate-500 mb-2">Action recommandée</p>
                <p className="text-sm text-slate-200">{actionsByPattern[entity.primary_pattern] ?? "Analyse approfondie requise"}</p>
              </div>
              <div className="bg-slate-800/50 rounded-lg p-4">
                <p className="text-xs text-slate-500 mb-1">Dernière mise à jour</p>
                <p className="text-sm text-slate-300">{entity.last_updated}</p>
              </div>
            </div>
          )}
        </div>

        <div className="px-5 pb-5">
          <button
            onClick={onClose}
            className="w-full py-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 text-sm transition-colors"
          >
            Fermer
          </button>
        </div>
      </div>
    </div>
  );
}

// ── Main Dashboard ─────────────────────────────────────────────────────────
export default function BiasDashboard() {
  const [data, setData] = useState<SummaryData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filter, setFilter] = useState<string>("Tous");
  const [selectedEntity, setSelectedEntity] = useState<Entity | null>(null);

  useEffect(() => {
    fetch("/api/ai-bias-engine")
      .then((r) => r.json())
      .then((json) => {
        setData(json);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message ?? "Erreur de chargement");
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center">
        <div className="text-slate-400 text-sm animate-pulse">Chargement du moteur de biais IA...</div>
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center">
        <div className="text-red-400 text-sm">{error ?? "Données indisponibles"}</div>
      </div>
    );
  }

  const filterMap: Record<string, string> = {
    Tous: "",
    Critique: "critique",
    Élevé: "élevé",
    Modéré: "modéré",
    Faible: "faible",
  };

  const filterPills = ["Tous", "Critique", "Élevé", "Modéré", "Faible"];

  const filteredEntities =
    filter === "Tous"
      ? data.entities
      : data.entities.filter((e) => e.risk_level === filterMap[filter]);

  // Average sub-scores across all entities
  const avgAlgo = data.entities.reduce((s, e) => s + e.algorithmic_score, 0) / data.entities.length;
  const avgData = data.entities.reduce((s, e) => s + e.data_score, 0) / data.entities.length;
  const avgImpact = data.entities.reduce((s, e) => s + e.impact_score, 0) / data.entities.length;
  const avgTransparency = data.entities.reduce((s, e) => s + e.transparency_score, 0) / data.entities.length;

  const maxPattern = Math.max(...Object.values(data.pattern_distribution));

  const patternLabels: Record<string, string> = {
    biais_algorithmique: "Biais algorithmique",
    biais_données: "Biais données",
    impact_discriminatoire: "Impact discriminatoire",
    opacite_systematique: "Opacité systématique",
    equilibre_biais: "Équilibre biais",
  };

  const patternColors: Record<string, string> = {
    biais_algorithmique: "#ef4444",
    biais_données: "#f97316",
    impact_discriminatoire: "#a855f7",
    opacite_systematique: "#eab308",
    equilibre_biais: "#22c55e",
  };

  return (
    <div className="min-h-screen bg-slate-950 text-white p-6">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-1">
          <div className="w-2 h-2 rounded-full bg-blue-400 animate-pulse" />
          <h1 className="text-2xl font-bold text-white">AI Bias Intelligence Engine</h1>
        </div>
        <p className="text-slate-400 text-sm ml-5">
          Caelum Partners · Détection & analyse des biais algorithmiques · {data.last_analysis}
        </p>
      </div>

      {/* Critical Alerts */}
      {data.critical_alerts.length > 0 && (
        <div className="mb-6 space-y-2">
          {data.critical_alerts.map((alert, i) => (
            <div key={i} className="bg-red-950/40 border border-red-700/40 rounded-lg px-4 py-2.5 text-xs text-red-300">
              {alert}
            </div>
          ))}
        </div>
      )}

      {/* KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4 mb-8">
        {[
          { label: "Total Entités", value: data.total_entities, sub: `v${data.engine_version}`, color: "text-blue-400" },
          { label: "Critique", value: data.risk_distribution.critique, sub: "entités", color: "text-red-400" },
          { label: "Élevé", value: data.risk_distribution["élevé"], sub: "entités", color: "text-orange-400" },
          { label: "Composite Moyen", value: data.avg_composite.toFixed(1), sub: "/ 100", color: "text-yellow-400" },
          { label: "Index Biais", value: data.avg_estimated_bias_index.toFixed(2), sub: "/ 10", color: "text-purple-400" },
          { label: "Confiance", value: `${(data.confidence_score * 100).toFixed(0)}%`, sub: data.domain, color: "text-green-400" },
        ].map((kpi) => (
          <div key={kpi.label} className="bg-slate-900 border border-blue-700/30 rounded-xl p-4">
            <p className="text-xs text-slate-500 mb-1">{kpi.label}</p>
            <p className={`text-2xl font-bold ${kpi.color}`}>{kpi.value}</p>
            <p className="text-xs text-slate-600 mt-0.5">{kpi.sub}</p>
          </div>
        ))}
      </div>

      {/* Gauge Rings + Distribution Bars */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        {/* Gauge rings */}
        <div className="bg-slate-900 border border-blue-700/30 rounded-xl p-6">
          <h2 className="text-sm font-semibold text-slate-300 mb-5">Scores Moyens par Dimension</h2>
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 justify-items-center">
            <GaugeRing value={avgAlgo} label="Algorithmique" color="#ef4444" />
            <GaugeRing value={avgData} label="Données" color="#f97316" />
            <GaugeRing value={avgImpact} label="Impact" color="#a855f7" />
            <GaugeRing value={avgTransparency} label="Transparence" color="#3b82f6" />
          </div>
        </div>

        {/* Distribution Bars */}
        <div className="bg-slate-900 border border-blue-700/30 rounded-xl p-6">
          <h2 className="text-sm font-semibold text-slate-300 mb-5">Distribution des Patterns</h2>
          <div className="space-y-3">
            {Object.entries(data.pattern_distribution).map(([pattern, count]) => (
              <DistBar
                key={pattern}
                label={patternLabels[pattern] ?? pattern}
                value={count}
                max={maxPattern || 1}
                color={patternColors[pattern] ?? "#64748b"}
              />
            ))}
          </div>
        </div>
      </div>

      {/* Risk Distribution Bars */}
      <div className="bg-slate-900 border border-blue-700/30 rounded-xl p-6 mb-8">
        <h2 className="text-sm font-semibold text-slate-300 mb-5">Distribution des Niveaux de Risque</h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {(["critique", "élevé", "modéré", "faible"] as const).map((level) => (
            <div key={level} className="space-y-2">
              <DistBar
                label={level.charAt(0).toUpperCase() + level.slice(1)}
                value={data.risk_distribution[level]}
                max={data.total_entities}
                color={riskColor(level)}
              />
            </div>
          ))}
        </div>
      </div>

      {/* Filter Pills */}
      <div className="flex gap-2 mb-5 flex-wrap">
        {filterPills.map((pill) => (
          <button
            key={pill}
            onClick={() => setFilter(pill)}
            className={`px-4 py-1.5 rounded-full text-xs font-medium transition-colors ${
              filter === pill
                ? "bg-blue-600 text-white"
                : "bg-slate-800 text-slate-400 hover:bg-slate-700 hover:text-white"
            }`}
          >
            {pill}
          </button>
        ))}
        <span className="ml-auto text-xs text-slate-500 self-center">
          {filteredEntities.length} entité{filteredEntities.length !== 1 ? "s" : ""}
        </span>
      </div>

      {/* Entity Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4 mb-8">
        {filteredEntities.map((entity) => (
          <button
            key={entity.id}
            onClick={() => setSelectedEntity(entity)}
            className="bg-slate-900 border border-blue-700/30 rounded-xl p-5 text-left hover:border-blue-500/60 transition-all hover:bg-slate-800/60 group"
          >
            <div className="flex items-start justify-between mb-3">
              <div>
                <p className="font-semibold text-white group-hover:text-blue-300 transition-colors">
                  {entity.name}
                </p>
                <p className="text-xs text-slate-500">{entity.id} · {entity.country}</p>
              </div>
              <span className={`px-2 py-1 rounded text-xs font-semibold shrink-0 ${riskBadgeClass(entity.risk_level)}`}>
                {entity.risk_level.toUpperCase()}
              </span>
            </div>

            <p className="text-xs text-slate-400 mb-3">{entity.sector}</p>

            <div className="flex items-center gap-3 mb-3">
              <div className="flex-1 bg-slate-800 rounded-full h-1.5">
                <div
                  className="h-1.5 rounded-full"
                  style={{ width: `${entity.composite_score}%`, backgroundColor: riskColor(entity.risk_level) }}
                />
              </div>
              <span className="text-sm font-bold" style={{ color: riskColor(entity.risk_level) }}>
                {entity.composite_score.toFixed(1)}
              </span>
            </div>

            <div className="grid grid-cols-3 gap-2 text-xs text-slate-500">
              <div>
                <span className="block text-slate-300 font-medium">{entity.model_count}</span>
                modèles
              </div>
              <div>
                <span className="block text-slate-300 font-medium">{entity.estimated_bias_index}</span>
                indice
              </div>
              <div>
                <span className="block text-slate-300 font-medium font-mono text-xs leading-tight">{entity.primary_pattern.replace(/_/g, " ")}</span>
                pattern
              </div>
            </div>
          </button>
        ))}
      </div>

      {/* Data Sources Footer */}
      <div className="bg-slate-900 border border-blue-700/30 rounded-xl p-4">
        <p className="text-xs text-slate-500">
          Sources de données :{" "}
          {data.data_sources.map((src) => (
            <span key={src} className="inline-block bg-slate-800 text-slate-300 px-2 py-0.5 rounded text-xs mr-2 mb-1">
              {src}
            </span>
          ))}
          · Analyse {data.last_analysis} · Confiance {(data.confidence_score * 100).toFixed(0)}%
        </p>
      </div>

      {/* Detail Modal */}
      {selectedEntity && (
        <DetailModal entity={selectedEntity} onClose={() => setSelectedEntity(null)} />
      )}
    </div>
  );
}
