"use client";

import { useEffect, useState } from "react";

// ─── Types ────────────────────────────────────────────────────────────────────

interface FarmingEntity {
  entity_id: string;
  name: string;
  country: string;
  sector: string;
  domain: string;
  composite_score: number;
  yield_score: number;
  energy_score: number;
  sustainability_score: number;
  scalability_score: number;
  risk_level: string;
  primary_pattern: string;
  key_signals: string[];
  estimated_farming_index: number;
  last_updated: string;
}

interface SummaryData {
  total_entities: number;
  avg_composite: number;
  risk_distribution: Record<string, number>;
  pattern_distribution: Record<string, number>;
  top_risk_entities: FarmingEntity[];
  critical_alerts: string[];
  last_analysis: string;
  engine_version: string;
  domain: string;
  confidence_score: number;
  data_sources: string[];
  entities: FarmingEntity[];
  avg_estimated_farming_index: number;
}

interface ApiResponse {
  digital_seal?: unknown;
  total_entities: number;
  avg_composite: number;
  risk_distribution: Record<string, number>;
  pattern_distribution: Record<string, number>;
  top_risk_entities: FarmingEntity[];
  critical_alerts: string[];
  last_analysis: string;
  engine_version: string;
  domain: string;
  confidence_score: number;
  data_sources: string[];
  entities: FarmingEntity[];
  avg_estimated_farming_index: number;
}

// ─── Constants ────────────────────────────────────────────────────────────────

const RISK_COLORS: Record<string, string> = {
  critique: "#ef4444",
  "élevé": "#f97316",
  "modéré": "#eab308",
  faible: "#22c55e",
};

const RISK_BG: Record<string, string> = {
  critique: "bg-red-500/10 text-red-400 border-red-500/30",
  "élevé": "bg-orange-500/10 text-orange-400 border-orange-500/30",
  "modéré": "bg-yellow-500/10 text-yellow-400 border-yellow-500/30",
  faible: "bg-emerald-500/10 text-emerald-400 border-emerald-500/30",
};

const RISK_LABELS: Record<string, string> = {
  all: "Tous",
  critique: "Critique",
  "élevé": "Élevé",
  "modéré": "Modéré",
  faible: "Faible",
};

const COUNTRY_FLAGS: Record<string, string> = {
  USA: "🇺🇸",
  Bangladesh: "🇧🇩",
  Nigeria: "🇳🇬",
  "United Kingdom": "🇬🇧",
  Germany: "🇩🇪",
  France: "🇫🇷",
  Norway: "🇳🇴",
  Netherlands: "🇳🇱",
};

// ─── GaugeRing ────────────────────────────────────────────────────────────────

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
      <span className="text-xs text-stone-400 text-center">{label}</span>
    </div>
  );
}

// ─── DistBar ──────────────────────────────────────────────────────────────────

function DistBar({
  label,
  distribution,
  total,
  colorMap,
}: {
  label: string;
  distribution: Record<string, number>;
  total: number;
  colorMap: Record<string, string>;
}) {
  const entries = Object.entries(distribution).filter(([, v]) => v > 0);
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-4">
      <p className="text-xs text-slate-400 mb-3 font-medium">{label}</p>
      <div className="flex h-2.5 rounded-full overflow-hidden gap-0.5 mb-3">
        {entries.map(([key, count]) => {
          const pct = total > 0 ? (count / total) * 100 : 0;
          const color = colorMap[key] || "#6b7280";
          return pct > 0 ? (
            <div
              key={key}
              className="h-full transition-all"
              style={{ width: `${pct}%`, backgroundColor: color }}
              title={`${key}: ${count}`}
            />
          ) : null;
        })}
      </div>
      <div className="flex flex-wrap gap-2">
        {entries.map(([key, count]) => {
          const color = colorMap[key] || "#6b7280";
          return (
            <div key={key} className="flex items-center gap-1.5 text-xs text-slate-400">
              <div className="w-2 h-2 rounded-full shrink-0" style={{ backgroundColor: color }} />
              <span className="truncate max-w-[120px]" title={key}>
                {key}
              </span>
              <span className="text-slate-500">({count})</span>
            </div>
          );
        })}
      </div>
    </div>
  );
}

// ─── DetailModal ──────────────────────────────────────────────────────────────

const PATTERN_ACTIONS: Record<string, string> = {
  "Rendement Insuffisant Critique":
    "Revoir immédiatement le protocole de culture — ajuster densité de plantation, cycle lumineux et nutrition hydroponique pour restaurer les rendements au seuil de viabilité économique.",
  "Consommation Énergie Excessive":
    "Auditer immédiatement le système d'éclairage LED et HVAC — migrer vers des solutions basse consommation et optimiser les plages horaires d'éclairage pour réduire le coût énergétique par kg produit.",
  "Échec Scalabilité":
    "Revoir l'architecture modulaire des tours de culture et la logistique interne — identifier les goulots d'étranglement humains et technologiques avant toute tentative d'expansion de superficie.",
  "Impact Carbone Élevé":
    "Planifier la transition vers des sources d'énergie renouvelable (PPA solaire/éolien) et optimiser la chaîne logistique de distribution pour réduire l'empreinte carbone globale de l'opération.",
  "Risque Rentabilité":
    "Diversifier le portefeuille de cultures vers des variétés à haute valeur ajoutée (microgreens, herbes aromatiques premium) et explorer les partenariats avec la grande distribution pour sécuriser les débouchés commerciaux.",
};

function DetailModal({ entity, onClose }: { entity: FarmingEntity; onClose: () => void }) {
  const [tab, setTab] = useState<"scores" | "signaux" | "actions">("scores");

  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
    };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [onClose]);

  const riskColor = RISK_COLORS[entity.risk_level] || "#6b7280";
  const flag = COUNTRY_FLAGS[entity.country] || "🌍";
  const actionText = PATTERN_ACTIONS[entity.primary_pattern] || "Analyser la situation et définir un plan d'action adapté.";

  const subScores = [
    { label: "Rendement", value: entity.yield_score, color: "#10b981" },
    { label: "Énergie", value: entity.energy_score, color: "#3b82f6" },
    { label: "Durabilité", value: entity.sustainability_score, color: "#8b5cf6" },
    { label: "Scalabilité", value: entity.scalability_score, color: "#f59e0b" },
  ];

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm p-4"
      onClick={onClose}
    >
      <div
        className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-lg max-h-[90vh] overflow-y-auto"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="p-6 border-b border-slate-800 flex items-start justify-between gap-4">
          <div>
            <div className="flex items-center gap-2 flex-wrap mb-1">
              <span className="text-lg">{flag}</span>
              <h2 className="text-lg font-bold text-slate-100">{entity.name}</h2>
              <span
                className={`text-xs px-2 py-0.5 rounded-full border font-medium ${RISK_BG[entity.risk_level]}`}
              >
                {entity.risk_level}
              </span>
            </div>
            <p className="text-xs text-slate-400">
              {entity.country} · {entity.sector} · {entity.entity_id}
            </p>
          </div>
          <button
            onClick={onClose}
            className="text-slate-400 hover:text-slate-200 text-xl shrink-0 leading-none"
          >
            ✕
          </button>
        </div>

        {/* Scores strip */}
        <div className="px-6 pt-5 pb-4 flex items-center gap-4 bg-slate-800/30">
          <div className="text-center">
            <div className="text-3xl font-bold" style={{ color: riskColor }}>
              {entity.composite_score.toFixed(1)}
            </div>
            <div className="text-xs text-slate-400">Score composite</div>
          </div>
          <div className="w-px h-10 bg-slate-700" />
          <div className="text-center">
            <div className="text-2xl font-bold text-emerald-400">
              {entity.estimated_farming_index.toFixed(2)}
            </div>
            <div className="text-xs text-slate-400">Index /10</div>
          </div>
          <div className="flex-1 text-right">
            <div className="text-xs text-slate-500 truncate max-w-[160px] ml-auto" title={entity.primary_pattern}>
              {entity.primary_pattern}
            </div>
          </div>
        </div>

        {/* Tabs */}
        <div className="flex border-b border-slate-800 px-6">
          {(["scores", "signaux", "actions"] as const).map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`px-4 py-3 text-sm font-medium capitalize border-b-2 transition-colors ${
                tab === t
                  ? "border-emerald-500 text-emerald-400"
                  : "border-transparent text-slate-400 hover:text-slate-300"
              }`}
            >
              {t === "scores" ? "Scores" : t === "signaux" ? "Signaux" : "Actions"}
            </button>
          ))}
        </div>

        {/* Tab content */}
        <div className="p-6">
          {tab === "scores" && (
            <div className="space-y-4">
              {subScores.map(({ label, value, color }) => (
                <div key={label} className="flex flex-col gap-1.5">
                  <div className="flex justify-between text-sm">
                    <span className="text-slate-300 font-medium">{label}</span>
                    <span className="font-bold" style={{ color }}>
                      {value.toFixed(1)} / 100
                    </span>
                  </div>
                  <div className="h-2 rounded-full bg-slate-800 overflow-hidden">
                    <div
                      className="h-full rounded-full transition-all duration-500"
                      style={{ width: `${value}%`, backgroundColor: color }}
                    />
                  </div>
                </div>
              ))}
              <div className="mt-4 pt-4 border-t border-slate-800 text-xs text-slate-500">
                <span className="text-slate-400 font-medium">Formule : </span>
                Rendement×30% + Énergie×25% + Durabilité×25% + Scalabilité×20% ={" "}
                <span className="text-emerald-400 font-bold">{entity.composite_score.toFixed(2)}</span>
              </div>
            </div>
          )}

          {tab === "signaux" && (
            <ul className="space-y-3">
              {entity.key_signals.map((signal, i) => (
                <li key={i} className="flex gap-3 text-sm">
                  <span className="text-emerald-400 font-bold shrink-0 mt-0.5">{i + 1}.</span>
                  <span className="text-slate-300 leading-relaxed">{signal}</span>
                </li>
              ))}
            </ul>
          )}

          {tab === "actions" && (
            <div className="space-y-4">
              <div
                className={`rounded-xl border p-4 ${RISK_BG[entity.risk_level]}`}
              >
                <div className="text-xs font-semibold mb-1 uppercase tracking-wide opacity-70">
                  Niveau de risque
                </div>
                <div className="font-bold capitalize">{entity.risk_level}</div>
              </div>
              <div>
                <div className="text-xs font-semibold text-slate-400 mb-2 uppercase tracking-wide">
                  Pattern détecté
                </div>
                <div className="text-sm text-emerald-300 font-medium mb-3">{entity.primary_pattern}</div>
                <div className="text-sm text-slate-300 leading-relaxed bg-slate-800/50 rounded-xl p-4">
                  {actionText}
                </div>
              </div>
            </div>
          )}
        </div>

        <div className="px-6 pb-5 text-xs text-slate-600">
          Dernière mise à jour : {entity.last_updated}
        </div>
      </div>
    </div>
  );
}

// ─── EntityCard ───────────────────────────────────────────────────────────────

function EntityCard({ entity, onClick }: { entity: FarmingEntity; onClick: () => void }) {
  const riskColor = RISK_COLORS[entity.risk_level] || "#6b7280";
  const flag = COUNTRY_FLAGS[entity.country] || "🌍";

  const subScores = [
    { label: "Rendement", value: entity.yield_score, color: "#10b981" },
    { label: "Énergie", value: entity.energy_score, color: "#3b82f6" },
    { label: "Durabilité", value: entity.sustainability_score, color: "#8b5cf6" },
    { label: "Scalabilité", value: entity.scalability_score, color: "#f59e0b" },
  ];

  return (
    <button
      onClick={onClick}
      className="bg-slate-900 border border-slate-800 rounded-2xl p-5 text-left hover:border-emerald-700/50 hover:bg-slate-800/40 transition-all w-full"
    >
      {/* Header */}
      <div className="flex items-start justify-between gap-3 mb-4">
        <div className="min-w-0">
          <div className="flex items-center gap-1.5 mb-0.5">
            <span>{flag}</span>
            <span className="font-semibold text-slate-100 truncate">{entity.name}</span>
          </div>
          <p className="text-xs text-slate-500">
            {entity.country} · {entity.sector}
          </p>
        </div>
        <div className="text-right shrink-0">
          <div className="text-xl font-bold" style={{ color: riskColor }}>
            {entity.composite_score.toFixed(1)}
          </div>
          <div className="text-xs text-slate-500">/ 100</div>
        </div>
      </div>

      {/* Risk badge */}
      <div className="flex items-center gap-2 mb-4">
        <span
          className={`text-xs px-2 py-0.5 rounded-full border font-medium ${RISK_BG[entity.risk_level]}`}
        >
          {entity.risk_level}
        </span>
        <span className="text-xs text-slate-500 bg-slate-800 rounded-lg px-2 py-0.5">
          Index {entity.estimated_farming_index.toFixed(2)}/10
        </span>
      </div>

      {/* Sub-score bars */}
      <div className="space-y-2 mb-4">
        {subScores.map(({ label, value, color }) => (
          <div key={label} className="flex items-center gap-2">
            <span className="text-xs text-slate-500 w-16 shrink-0">{label}</span>
            <div className="flex-1 h-1.5 rounded-full bg-slate-800 overflow-hidden">
              <div
                className="h-full rounded-full"
                style={{ width: `${value}%`, backgroundColor: color }}
              />
            </div>
            <span className="text-xs w-7 text-right shrink-0 text-slate-400">
              {Math.round(value)}
            </span>
          </div>
        ))}
      </div>

      {/* Pattern */}
      <div className="text-xs text-slate-500 truncate border-t border-slate-800 pt-3">
        <span className="text-slate-400">Pattern : </span>
        {entity.primary_pattern}
      </div>
    </button>
  );
}

// ─── Page ─────────────────────────────────────────────────────────────────────

export default function VerticalFarmingEnginePage() {
  const [data, setData] = useState<SummaryData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedRisk, setSelectedRisk] = useState("all");
  const [selectedCountry, setSelectedCountry] = useState("all");
  const [selectedEntity, setSelectedEntity] = useState<FarmingEntity | null>(null);

  useEffect(() => {
    async function load() {
      setLoading(true);
      setError(null);
      try {
        const res = await fetch("/api/vertical-farming-engine");
        if (!res.ok) throw new Error(`Erreur ${res.status}`);
        const json: ApiResponse = await res.json();
        setData({
          total_entities: json.total_entities,
          avg_composite: json.avg_composite,
          risk_distribution: json.risk_distribution,
          pattern_distribution: json.pattern_distribution,
          top_risk_entities: json.top_risk_entities,
          critical_alerts: json.critical_alerts,
          last_analysis: json.last_analysis,
          engine_version: json.engine_version,
          domain: json.domain,
          confidence_score: json.confidence_score,
          data_sources: json.data_sources,
          entities: json.entities,
          avg_estimated_farming_index: json.avg_estimated_farming_index,
        });
      } catch (err) {
        setError(err instanceof Error ? err.message : "Erreur inconnue");
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center">
        <div className="text-emerald-400 text-lg animate-pulse">
          Analyse agriculture verticale en cours…
        </div>
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center">
        <div className="text-red-400">{error || "Données indisponibles"}</div>
      </div>
    );
  }

  const allEntities = data.entities;

  // Filter
  const filtered = allEntities.filter((e) => {
    const riskOk = selectedRisk === "all" || e.risk_level === selectedRisk;
    const countryOk = selectedCountry === "all" || e.country === selectedCountry;
    return riskOk && countryOk;
  });

  // Aggregate KPIs
  const critiqueCount = allEntities.filter((e) => e.risk_level === "critique").length;
  const eleveCount = allEntities.filter((e) => e.risk_level === "élevé").length;
  const avgYield = allEntities.length > 0
    ? Math.round(allEntities.reduce((s, e) => s + e.yield_score, 0) / allEntities.length)
    : 0;

  // Countries
  const countries = Array.from(new Set(allEntities.map((e) => e.country))).sort();

  // Gauge averages
  const avgEnergy = allEntities.length > 0
    ? allEntities.reduce((s, e) => s + e.energy_score, 0) / allEntities.length
    : 0;
  const avgSustainability = allEntities.length > 0
    ? allEntities.reduce((s, e) => s + e.sustainability_score, 0) / allEntities.length
    : 0;
  const avgScalability = allEntities.length > 0
    ? allEntities.reduce((s, e) => s + e.scalability_score, 0) / allEntities.length
    : 0;

  const patternColors: Record<string, string> = {
    "Rendement Insuffisant Critique": "#ef4444",
    "Consommation Énergie Excessive": "#f97316",
    "Échec Scalabilité": "#eab308",
    "Impact Carbone Élevé": "#8b5cf6",
    "Risque Rentabilité": "#22c55e",
  };

  return (
    <div className="min-h-screen bg-slate-950 p-6">
      <div className="max-w-7xl mx-auto space-y-6">

        {/* Header */}
        <div className="flex items-start justify-between gap-4 flex-wrap">
          <div>
            <h1 className="text-2xl font-bold text-slate-100">Vertical Farming Engine</h1>
            <p className="text-sm text-slate-400 mt-1">
              Intelligence agricole — rendement, énergie, durabilité, scalabilité · Caelum Partners
            </p>
          </div>
          <div className="flex items-center gap-2 text-xs text-slate-500">
            <div className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
            <span>v{data.engine_version} · {data.confidence_score}% confiance</span>
          </div>
        </div>

        {/* 6 KPI Cards */}
        <div className="grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-6">
          {[
            {
              label: "Total Entités",
              value: data.total_entities,
              color: "text-slate-100",
              sub: data.domain,
            },
            {
              label: "Critique",
              value: critiqueCount,
              color: "text-red-400",
              sub: `${Math.round((critiqueCount / data.total_entities) * 100)}% du total`,
            },
            {
              label: "Élevé",
              value: eleveCount,
              color: "text-orange-400",
              sub: `${Math.round((eleveCount / data.total_entities) * 100)}% du total`,
            },
            {
              label: "Composite Moyen",
              value: `${data.avg_composite.toFixed(1)}`,
              color:
                data.avg_composite >= 60
                  ? "text-red-400"
                  : data.avg_composite >= 40
                  ? "text-orange-400"
                  : data.avg_composite >= 20
                  ? "text-yellow-400"
                  : "text-emerald-400",
              sub: "/ 100",
            },
            {
              label: "Index Agriculture",
              value: `${data.avg_estimated_farming_index.toFixed(2)}`,
              color: "text-emerald-400",
              sub: "/ 10",
            },
            {
              label: "Rendement Moyen",
              value: avgYield,
              color: "#10b981",
              sub: "score moyen",
            },
          ].map((kpi) => (
            <div
              key={kpi.label}
              className="bg-slate-900 border border-slate-800 rounded-2xl p-4"
            >
              <div
                className={`text-2xl font-bold ${typeof kpi.color === "string" && kpi.color.startsWith("text-") ? kpi.color : ""}`}
                style={typeof kpi.color === "string" && !kpi.color.startsWith("text-") ? { color: kpi.color } : undefined}
              >
                {kpi.value}
              </div>
              <div className="text-xs text-slate-400 mt-0.5">{kpi.label}</div>
              <div className="text-xs text-slate-600 mt-1">{kpi.sub}</div>
            </div>
          ))}
        </div>

        {/* 4 GaugeRings */}
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6">
          <h2 className="text-sm font-semibold text-slate-300 mb-5">
            Scores moyens — dimensions d&apos;analyse
          </h2>
          <div className="grid grid-cols-2 gap-6 sm:grid-cols-4 justify-items-center">
            <GaugeRing value={avgYield} label="Rendement" color="#10b981" />
            <GaugeRing value={avgEnergy} label="Énergie" color="#3b82f6" />
            <GaugeRing value={avgSustainability} label="Durabilité" color="#8b5cf6" />
            <GaugeRing value={avgScalability} label="Scalabilité" color="#f59e0b" />
          </div>
        </div>

        {/* 4 DistBars */}
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
          <DistBar
            label="Distribution par niveau de risque"
            distribution={data.risk_distribution}
            total={data.total_entities}
            colorMap={RISK_COLORS}
          />
          <DistBar
            label="Distribution par pattern"
            distribution={data.pattern_distribution}
            total={data.total_entities}
            colorMap={patternColors}
          />
          <DistBar
            label="Entités filtrées — risque actif"
            distribution={
              selectedRisk === "all"
                ? data.risk_distribution
                : { [selectedRisk]: (data.risk_distribution[selectedRisk] || 0) }
            }
            total={filtered.length || data.total_entities}
            colorMap={RISK_COLORS}
          />
          <DistBar
            label="Patterns — sélection active"
            distribution={
              filtered.reduce((acc, e) => {
                acc[e.primary_pattern] = (acc[e.primary_pattern] || 0) + 1;
                return acc;
              }, {} as Record<string, number>)
            }
            total={filtered.length}
            colorMap={patternColors}
          />
        </div>

        {/* Critical Alerts */}
        {data.critical_alerts.length > 0 && (
          <div className="bg-red-950/30 border border-red-800/40 rounded-2xl p-4">
            <h2 className="text-sm font-semibold text-red-400 mb-3 flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-red-500 animate-pulse" />
              Alertes critiques ({data.critical_alerts.length})
            </h2>
            <ul className="space-y-1.5">
              {data.critical_alerts.map((alert, i) => (
                <li key={i} className="text-xs text-red-300 flex gap-2">
                  <span className="text-red-500 shrink-0">⚠</span>
                  {alert}
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Filters */}
        <div className="flex flex-wrap gap-3 items-center">
          {/* Risk pills */}
          <div className="flex flex-wrap gap-2">
            {Object.keys(RISK_LABELS).map((rk) => {
              const count =
                rk === "all"
                  ? data.total_entities
                  : (data.risk_distribution[rk] || 0);
              return (
                <button
                  key={rk}
                  onClick={() => setSelectedRisk(rk)}
                  className={`px-3 py-1.5 rounded-full text-xs font-medium border transition-all ${
                    selectedRisk === rk
                      ? "bg-emerald-600 border-emerald-500 text-white"
                      : "bg-slate-800/50 border-slate-700 text-slate-400 hover:border-slate-500"
                  }`}
                >
                  {RISK_LABELS[rk]}
                  <span className="ml-1 opacity-70">({count})</span>
                </button>
              );
            })}
          </div>

          <div className="w-px h-5 bg-slate-700" />

          {/* Country pills */}
          <div className="flex flex-wrap gap-2">
            <button
              onClick={() => setSelectedCountry("all")}
              className={`px-3 py-1.5 rounded-full text-xs font-medium border transition-all ${
                selectedCountry === "all"
                  ? "bg-emerald-600 border-emerald-500 text-white"
                  : "bg-slate-800/50 border-slate-700 text-slate-400 hover:border-slate-500"
              }`}
            >
              Tous pays
            </button>
            {countries.map((c) => (
              <button
                key={c}
                onClick={() => setSelectedCountry(c)}
                className={`px-3 py-1.5 rounded-full text-xs font-medium border transition-all ${
                  selectedCountry === c
                    ? "bg-emerald-600 border-emerald-500 text-white"
                    : "bg-slate-800/50 border-slate-700 text-slate-400 hover:border-slate-500"
                }`}
              >
                {COUNTRY_FLAGS[c] || "🌍"} {c}
              </button>
            ))}
          </div>
        </div>

        {/* Entity count */}
        <div className="text-xs text-slate-500">
          {filtered.length} entité{filtered.length !== 1 ? "s" : ""} affichée{filtered.length !== 1 ? "s" : ""}
          {(selectedRisk !== "all" || selectedCountry !== "all") && (
            <button
              onClick={() => { setSelectedRisk("all"); setSelectedCountry("all"); }}
              className="ml-2 text-emerald-400 hover:text-emerald-300 underline"
            >
              Réinitialiser les filtres
            </button>
          )}
        </div>

        {/* Entity Grid */}
        {filtered.length === 0 ? (
          <div className="text-center py-20 text-slate-500">
            Aucune entité pour cette combinaison de filtres.
          </div>
        ) : (
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
            {filtered.map((entity) => (
              <EntityCard
                key={entity.entity_id}
                entity={entity}
                onClick={() => setSelectedEntity(entity)}
              />
            ))}
          </div>
        )}

        {/* Footer */}
        <div className="pt-4 border-t border-slate-800 flex items-center justify-between flex-wrap gap-2 text-xs text-slate-600">
          <span>
            Sources : {data.data_sources.join(" · ")}
          </span>
          <span>Dernière analyse : {data.last_analysis}</span>
        </div>
      </div>

      {/* Detail Modal */}
      {selectedEntity && (
        <DetailModal entity={selectedEntity} onClose={() => setSelectedEntity(null)} />
      )}
    </div>
  );
}
