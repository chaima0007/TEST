"use client";
import { useEffect, useState } from "react";

type Entity = {
  id: string;
  name: string;
  country: string;
  sector: string;
  composite_score: number;
  risk_level: string;
  key_signals: string[];
  confidence_score: number;
  feminicide_rate_normalized_score: number;
  honor_killing_legal_tolerance_score: number;
  state_institutional_impunity_score: number;
  survivor_protection_failure_score: number;
  estimated_femicide_index: number;
  last_updated: string;
};

type ApiResponse = {
  total_entities: number;
  avg_composite: number;
  confidence_score: number;
  risk_distribution: Record<string, number>;
  top_risk_entities: string[];
  entities: Entity[];
};

const RC: Record<string, string> = {
  critique: "text-red-400",
  "élevé": "text-orange-400",
  modéré: "text-yellow-400",
  faible: "text-emerald-400",
};

const RB: Record<string, string> = {
  critique: "border-red-500/30 bg-red-500/10",
  "élevé": "border-orange-500/30 bg-orange-500/10",
  modéré: "border-yellow-500/30 bg-yellow-500/10",
  faible: "border-emerald-500/30 bg-emerald-500/10",
};

const ACCENT = "#e879f9";

function GaugeRing({ score, label }: { score: number; label: string }) {
  const circumference = 226.19;
  return (
    <div className="flex flex-col items-center gap-1">
      <svg width="88" height="88" viewBox="0 0 88 88">
        <circle cx="44" cy="44" r="36" fill="none" stroke="#0f172a" strokeWidth="8" />
        <circle
          cx="44"
          cy="44"
          r="36"
          fill="none"
          stroke={ACCENT}
          strokeWidth="8"
          strokeDasharray={`${(score / 100) * circumference} ${circumference}`}
          strokeLinecap="round"
          transform="rotate(-90 44 44)"
        />
        <text x="44" y="49" textAnchor="middle" fill="white" fontSize="13" fontWeight="bold">
          {Math.round(score)}
        </text>
      </svg>
      <span className="text-xs text-slate-400 text-center">{label}</span>
    </div>
  );
}

function DetailModal({ entity, onClose }: { entity: Entity; onClose: () => void }) {
  const [tab, setTab] = useState<"scores" | "signaux" | "actions">("scores");
  const scoreFields = [
    { label: "Taux Féminicide Normalisé", value: entity.feminicide_rate_normalized_score, color: "#e879f9" },
    { label: "Tolérance Légale Crimes d'Honneur", value: entity.honor_killing_legal_tolerance_score, color: "#ef4444" },
    { label: "Impunité Institutionnelle État", value: entity.state_institutional_impunity_score, color: "#f97316" },
    { label: "Échec Protection Survivantes", value: entity.survivor_protection_failure_score, color: "#a855f7" },
  ];
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
            <p className="text-slate-400 text-sm mt-0.5">{entity.country} · {entity.sector}</p>
          </div>
          <span className={`text-xs px-2 py-1 rounded-full border font-medium ${RB[entity.risk_level]} ${RC[entity.risk_level]}`}>
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
                  ? "border-b-2 bg-slate-800/50"
                  : "text-slate-400 hover:text-white"
              }`}
              style={tab === t ? { color: ACCENT, borderBottomColor: ACCENT } : {}}
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
              {scoreFields.map(({ label, value, color }) => (
                <div key={label}>
                  <div className="flex justify-between text-xs text-slate-400 mb-1">
                    <span>{label}</span>
                    <span>{value}</span>
                  </div>
                  <div className="h-2 bg-slate-800 rounded-full overflow-hidden">
                    <div className="h-full rounded-full" style={{ width: `${value}%`, background: color }} />
                  </div>
                </div>
              ))}
              <div className="mt-2 text-xs text-slate-500">
                Index Féminicide:{" "}
                <span className="font-medium" style={{ color: ACCENT }}>
                  {entity.estimated_femicide_index}
                </span>
              </div>
            </div>
          )}
          {tab === "signaux" && (
            <div className="flex flex-col gap-3">
              <p className="text-slate-400 text-xs mb-1">Signaux de violence de genre détectés</p>
              {entity.key_signals.slice(0, 2).map((sig, i) => (
                <div
                  key={i}
                  className="flex items-start gap-2 bg-slate-800/60 rounded-lg px-3 py-2 border border-slate-700/50"
                >
                  <span className="mt-0.5 text-xs" style={{ color: ACCENT }}>▶</span>
                  <span className="text-slate-200 text-sm">{sig}</span>
                </div>
              ))}
            </div>
          )}
          {tab === "actions" && (
            <div className="flex flex-col gap-4">
              <div className="bg-slate-800/60 rounded-lg p-4 border border-slate-700/50">
                <p className="text-xs text-slate-400 mb-2 font-medium uppercase tracking-wide">
                  Action Recommandée
                </p>
                <p className="text-slate-100 text-sm leading-relaxed">
                  {entity.key_signals[2] ?? "Renforcement législatif d'urgence et protocoles de protection des survivantes requis."}
                </p>
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

export default function FemicideDashboard() {
  const [data, setData] = useState<ApiResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filterRisk, setFilterRisk] = useState<string>("all");
  const [selectedEntity, setSelectedEntity] = useState<Entity | null>(null);

  useEffect(() => {
    fetch("/api/femicide-engine")
      .then((r) => {
        if (!r.ok) throw new Error(`HTTP ${r.status}`);
        return r.json();
      })
      .then((json) => setData(json?.data ?? json))
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center">
        <div className="text-slate-400 text-sm animate-pulse">Chargement du moteur féminicides…</div>
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

  const entities = data.entities ?? [];
  const filtered = filterRisk === "all" ? entities : entities.filter((e) => e.risk_level === filterRisk);

  const avg = (key: keyof Entity) => {
    if (!entities.length) return 0;
    const vals = entities.map((e) => (e[key] as number) || 0);
    return Math.round((vals.reduce((a, b) => a + b, 0) / vals.length) * 10) / 10;
  };

  const rd = data.risk_distribution ?? {};

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
            <h1 className="text-xl font-bold text-white">Féminicides Engine</h1>
            <p className="text-slate-400 text-sm mt-0.5">
              Crimes d'Honneur, Impunité Institutionnelle &amp; Violence Létale de Genre
            </p>
          </div>
          <span
            className="text-xs px-3 py-1.5 rounded-full border font-medium"
            style={{ borderColor: `${ACCENT}50`, color: ACCENT, background: `${ACCENT}15` }}
          >
            Confiance {Math.round(data.confidence_score ?? 0)}%
          </span>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-6 py-8 space-y-8">
        {/* KPI Cards */}
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-4">
          {[
            { label: "Total Entités", value: data.total_entities, color: "text-white", sub: "acteurs surveillés" },
            { label: "Score Moyen", value: data.avg_composite, color: "text-fuchsia-400", sub: "composite global" },
            { label: "Critique", value: rd["critique"] ?? 0, color: "text-red-400", sub: "niveau critique" },
            { label: "Élevé", value: rd["élevé"] ?? 0, color: "text-orange-400", sub: "niveau élevé" },
            { label: "Modéré", value: rd["modéré"] ?? 0, color: "text-yellow-400", sub: "niveau modéré" },
            { label: "Confiance", value: `${Math.round(data.confidence_score ?? 0)}%`, color: "text-emerald-400", sub: "fiabilité données" },
          ].map(({ label, value, color, sub }) => (
            <div key={label} className="bg-slate-900 border border-slate-700/50 rounded-xl p-4 flex flex-col gap-1">
              <span className="text-xs text-slate-400 font-medium">{label}</span>
              <span className={`text-2xl font-bold ${color}`}>{value}</span>
              <span className="text-xs text-slate-500">{sub}</span>
            </div>
          ))}
        </div>

        {/* Gauge Rings */}
        <div className="bg-slate-900 border border-slate-700/50 rounded-xl p-6">
          <h2 className="text-sm font-semibold text-slate-300 mb-5">Scores Moyens par Dimension</h2>
          <div className="flex flex-wrap gap-8 justify-around">
            <GaugeRing score={avg("feminicide_rate_normalized_score")} label="Taux Féminicide" />
            <GaugeRing score={avg("honor_killing_legal_tolerance_score")} label="Crimes d'Honneur" />
            <GaugeRing score={avg("state_institutional_impunity_score")} label="Impunité État" />
            <GaugeRing score={avg("survivor_protection_failure_score")} label="Échec Protection" />
          </div>
        </div>

        {/* Top risk entities */}
        {data.top_risk_entities && data.top_risk_entities.length > 0 && (
          <div className="bg-slate-900 border border-slate-700/50 rounded-xl p-5">
            <h2 className="text-sm font-semibold text-slate-300 mb-3">Top Entités à Risque</h2>
            <div className="flex flex-col gap-2">
              {data.top_risk_entities.map((name, i) => (
                <div key={name} className="flex items-center gap-2">
                  <span className="text-xs font-bold" style={{ color: ACCENT }}>#{i + 1}</span>
                  <span className="text-xs text-slate-300">{name}</span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Filter pills */}
        <div className="flex items-center gap-2 flex-wrap">
          <span className="text-xs text-slate-400 font-medium mr-1">Filtrer:</span>
          {FILTER_PILLS.map(({ key, label }) => (
            <button
              key={key}
              onClick={() => setFilterRisk(key)}
              className="text-xs px-3 py-1.5 rounded-full border transition-colors"
              style={
                filterRisk === key
                  ? { background: `${ACCENT}30`, borderColor: ACCENT, color: ACCENT }
                  : { borderColor: "#334155", color: "#94a3b8" }
              }
            >
              {label}
              {key !== "all" && (
                <span className="ml-1 opacity-60">({rd[key] ?? 0})</span>
              )}
            </button>
          ))}
        </div>

        {/* Entity cards grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          {filtered.map((entity) => (
            <div
              key={entity.id}
              onClick={() => setSelectedEntity(entity)}
              className="bg-slate-900 border border-slate-700/50 rounded-xl p-4 cursor-pointer transition-all group hover:bg-slate-800/60"
              onMouseEnter={(e) => (e.currentTarget.style.borderColor = `${ACCENT}80`)}
              onMouseLeave={(e) => (e.currentTarget.style.borderColor = "rgba(100,116,139,0.5)")}
            >
              <div className="flex items-start justify-between gap-2 mb-3">
                <div>
                  <p className="text-white font-medium text-sm leading-tight">{entity.name}</p>
                  <p className="text-slate-500 text-xs mt-0.5">{entity.id}</p>
                </div>
                <span className={`text-xs px-2 py-0.5 rounded-full border font-medium whitespace-nowrap ${RB[entity.risk_level]} ${RC[entity.risk_level]}`}>
                  {entity.risk_level}
                </span>
              </div>

              <div className="flex justify-between items-center mb-3">
                <div className="flex items-center gap-3">
                  <GaugeRing score={entity.composite_score} label="" />
                  <div className="text-xs text-slate-400 space-y-1">
                    <p>{entity.country}</p>
                    <p className="truncate max-w-[100px]">{entity.sector}</p>
                  </div>
                </div>
              </div>

              <div className="mb-2">
                <div className="flex justify-between text-xs text-slate-500 mb-1">
                  <span>Index Féminicide</span>
                  <span className="font-medium" style={{ color: ACCENT }}>
                    {entity.estimated_femicide_index}
                  </span>
                </div>
                <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
                  <div
                    className="h-full rounded-full"
                    style={{
                      width: `${Math.min((entity.estimated_femicide_index ?? 0) * 10, 100)}%`,
                      background: ACCENT,
                    }}
                  />
                </div>
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
    </div>
  );
}
