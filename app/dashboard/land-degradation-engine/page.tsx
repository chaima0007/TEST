"use client";

import { useEffect, useState } from "react";

// ── Types ────────────────────────────────────────────────────────────────────

interface LandDegradationEntity {
  id: string;
  name: string;
  country: string;
  sector: string;
  composite_score: number;
  soil_erosion_score: number;
  desertification_score: number;
  deforestation_score: number;
  land_use_pressure_score: number;
  risk_level: string;
  primary_pattern: string;
  key_signals: string[];
  estimated_land_index: number;
  last_updated: string;
  alert_level: string;
}

interface LandDegradationSummary {
  total_entities: number;
  avg_composite: number;
  risk_distribution: { critique: number; "élevé": number; "modéré": number; faible: number };
  pattern_distribution: Record<string, number>;
  top_risk_entities: string[];
  critical_alerts: number;
  last_analysis: string;
  engine_version: string;
  domain: string;
  confidence_score: number;
  data_sources: string[];
  entities: LandDegradationEntity[];
  avg_estimated_land_index: number;
}

// ── Risk level helpers ────────────────────────────────────────────────────────

const RISK_CONFIG: Record<string, { label: string; color: string; bg: string; border: string; dot: string }> = {
  critique: {
    label: "Critique",
    color: "text-red-400",
    bg: "bg-red-500/10",
    border: "border-red-500/25",
    dot: "bg-red-500",
  },
  "élevé": {
    label: "Élevé",
    color: "text-orange-400",
    bg: "bg-orange-500/10",
    border: "border-orange-500/25",
    dot: "bg-orange-500",
  },
  "modéré": {
    label: "Modéré",
    color: "text-amber-400",
    bg: "bg-amber-500/10",
    border: "border-amber-500/25",
    dot: "bg-amber-500",
  },
  faible: {
    label: "Faible",
    color: "text-emerald-400",
    bg: "bg-emerald-500/10",
    border: "border-emerald-500/25",
    dot: "bg-emerald-500",
  },
};

const FILTER_OPTIONS = [
  { key: "all", label: "Tous" },
  { key: "critique", label: "Critique" },
  { key: "élevé", label: "Élevé" },
  { key: "modéré", label: "Modéré" },
  { key: "faible", label: "Faible" },
];

// ── GaugeRing (inline SVG, no lib) ───────────────────────────────────────────

function GaugeRing({
  value,
  max,
  label,
  color,
}: {
  value: number;
  max: number;
  label: string;
  color: string;
}) {
  const pct = Math.min(100, Math.max(0, (value / max) * 100));
  const r = 36;
  const circ = 2 * Math.PI * r;
  const offset = circ - (pct / 100) * circ;

  return (
    <div className="flex flex-col items-center gap-2">
      <svg width="96" height="96" viewBox="0 0 96 96">
        <circle cx="48" cy="48" r={r} fill="none" stroke="rgba(255,255,255,0.07)" strokeWidth="8" />
        <circle
          cx="48"
          cy="48"
          r={r}
          fill="none"
          stroke={color}
          strokeWidth="8"
          strokeLinecap="round"
          strokeDasharray={circ}
          strokeDashoffset={offset}
          transform="rotate(-90 48 48)"
          style={{ transition: "stroke-dashoffset 0.7s ease" }}
        />
        <text
          x="48"
          y="52"
          textAnchor="middle"
          fontSize="14"
          fontWeight="700"
          fill="white"
        >
          {Math.round(value)}
        </text>
      </svg>
      <span className="text-xs text-gray-400 text-center leading-tight">{label}</span>
    </div>
  );
}

// ── DistBar ───────────────────────────────────────────────────────────────────

function DistBar({
  label,
  count,
  total,
  color,
}: {
  label: string;
  count: number;
  total: number;
  color: string;
}) {
  const pct = total > 0 ? Math.round((count / total) * 100) : 0;
  return (
    <div className="space-y-1">
      <div className="flex justify-between text-xs">
        <span className="text-gray-300">{label}</span>
        <span className="text-gray-400">
          {count} <span className="text-gray-600">({pct}%)</span>
        </span>
      </div>
      <div className="h-2 bg-white/5 rounded-full overflow-hidden">
        <div
          className="h-full rounded-full transition-all duration-700"
          style={{ width: `${pct}%`, backgroundColor: color }}
        />
      </div>
    </div>
  );
}

// ── KPI Card ──────────────────────────────────────────────────────────────────

function KpiCard({
  label,
  value,
  sub,
  accent,
}: {
  label: string;
  value: string | number;
  sub?: string;
  accent?: string;
}) {
  return (
    <div className="bg-white/4 border border-white/10 rounded-xl px-5 py-4 hover:bg-white/6 transition-colors">
      <p className="text-xs text-gray-400 mb-1">{label}</p>
      <p className={`text-2xl font-bold ${accent ?? "text-white"}`}>{value}</p>
      {sub && <p className="text-xs text-gray-500 mt-0.5">{sub}</p>}
    </div>
  );
}

// ── Entity Card ───────────────────────────────────────────────────────────────

function EntityCard({
  entity,
  onClick,
}: {
  entity: LandDegradationEntity;
  onClick: (e: LandDegradationEntity) => void;
}) {
  const cfg = RISK_CONFIG[entity.risk_level] ?? RISK_CONFIG.faible;

  return (
    <button
      onClick={() => onClick(entity)}
      className={`w-full text-left bg-white/4 border ${cfg.border} rounded-xl p-4 hover:bg-white/7 transition-all`}
    >
      <div className="flex items-start justify-between gap-3 mb-3">
        <div className="min-w-0">
          <p className="font-semibold text-white truncate">{entity.name}</p>
          <p className="text-xs text-gray-400 truncate mt-0.5">{entity.country} · {entity.sector}</p>
        </div>
        <span
          className={`shrink-0 text-xs font-medium px-2.5 py-1 rounded-full border ${cfg.bg} ${cfg.border} ${cfg.color}`}
        >
          {cfg.label}
        </span>
      </div>

      <div className="grid grid-cols-3 gap-2 mb-3">
        <div className="bg-white/4 rounded-lg p-2 text-center">
          <p className="text-sm font-bold text-white">{entity.soil_erosion_score}%</p>
          <p className="text-[10px] text-gray-500">Érosion</p>
        </div>
        <div className="bg-white/4 rounded-lg p-2 text-center">
          <p className="text-sm font-bold text-white">{entity.desertification_score}%</p>
          <p className="text-[10px] text-gray-500">Désertif.</p>
        </div>
        <div className="bg-white/4 rounded-lg p-2 text-center">
          <p className="text-sm font-bold text-white">{entity.deforestation_score}%</p>
          <p className="text-[10px] text-gray-500">Déforest.</p>
        </div>
      </div>

      <div className="flex items-center justify-between text-xs">
        <span className="text-gray-400">
          Score composite :{" "}
          <span className={`font-bold ${cfg.color}`}>{entity.composite_score}</span>
        </span>
        <span className={`font-mono text-[10px] font-semibold ${cfg.color}`}>{entity.alert_level}</span>
      </div>
    </button>
  );
}

// ── Patterns (for Actions tab) ────────────────────────────────────────────────

const LAND_PATTERNS = [
  {
    name: "Érosion Catastrophique des Sols",
    severity_fr: "critique",
    action_fr: "Programme d'urgence de restauration des sols et terrasses agricoles.",
    signal_fr: "soil_erosion > 85 et desertification > 80",
  },
  {
    name: "Désertification Accélérée",
    severity_fr: "critique",
    action_fr: "Déploiement immédiat de barrières vertes et reforestation massive.",
    signal_fr: "desertification > 80 et deforestation > 75",
  },
  {
    name: "Pression Agricole Intensive",
    severity_fr: "élevé",
    action_fr: "Transition vers l'agriculture régénérative et rotation des cultures.",
    signal_fr: "land_use_pressure > 70 et soil_erosion > 65",
  },
  {
    name: "Déforestation Critique",
    severity_fr: "élevé",
    action_fr: "Moratoire sur les coupes forestières et corridors de biodiversité.",
    signal_fr: "deforestation > 70 et land_use_pressure > 60",
  },
  {
    name: "Dégradation Progressive",
    severity_fr: "modéré",
    action_fr: "Renforcement des pratiques durables et suivi satellitaire.",
    signal_fr: "soil_erosion > 40 et desertification > 35",
  },
  {
    name: "Surveillance Standard",
    severity_fr: "faible",
    action_fr: "Maintenir le suivi périodique et les pratiques actuelles de conservation.",
    signal_fr: "Aucun seuil critique atteint",
  },
];

const SEVERITY_STYLE: Record<string, string> = {
  critique: "text-red-400 bg-red-500/10 border-red-500/25",
  "élevé": "text-orange-400 bg-orange-500/10 border-orange-500/25",
  "modéré": "text-amber-400 bg-amber-500/10 border-amber-500/25",
  faible: "text-emerald-400 bg-emerald-500/10 border-emerald-500/25",
};

// ── Detail Modal ──────────────────────────────────────────────────────────────

function DetailModal({
  entity,
  onClose,
}: {
  entity: LandDegradationEntity;
  onClose: () => void;
}) {
  const [tab, setTab] = useState<"scores" | "signaux" | "actions">("scores");
  const cfg = RISK_CONFIG[entity.risk_level] ?? RISK_CONFIG.faible;
  const patternInfo = LAND_PATTERNS.find((p) => p.name === entity.primary_pattern);

  const TABS = [
    { key: "scores", label: "Scores" },
    { key: "signaux", label: "Signaux" },
    { key: "actions", label: "Actions" },
  ] as const;

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm"
      onClick={onClose}
    >
      <div
        className="w-full max-w-xl bg-slate-900 border border-white/12 rounded-2xl shadow-2xl overflow-hidden"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="px-6 pt-6 pb-4 border-b border-white/8">
          <div className="flex items-start justify-between gap-4">
            <div>
              <h2 className="text-lg font-bold text-white">{entity.name}</h2>
              <p className="text-sm text-gray-400 mt-0.5">{entity.country} · {entity.sector}</p>
            </div>
            <div className="flex items-center gap-2">
              <span
                className={`text-xs font-medium px-2.5 py-1 rounded-full border ${cfg.bg} ${cfg.border} ${cfg.color}`}
              >
                {cfg.label}
              </span>
              <button
                onClick={onClose}
                className="text-gray-400 hover:text-white transition-colors ml-1"
              >
                <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                  <path d="M5 5l10 10M15 5L5 15" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
                </svg>
              </button>
            </div>
          </div>

          {/* Tab bar */}
          <div className="flex gap-1 mt-4">
            {TABS.map((t) => (
              <button
                key={t.key}
                onClick={() => setTab(t.key)}
                className={`px-4 py-1.5 rounded-lg text-sm font-medium transition-colors ${
                  tab === t.key
                    ? "bg-white/10 text-white"
                    : "text-gray-400 hover:text-white"
                }`}
              >
                {t.label}
              </button>
            ))}
          </div>
        </div>

        {/* Body */}
        <div className="px-6 py-5 space-y-4 max-h-[60vh] overflow-y-auto">

          {/* ── TAB: Scores ── */}
          {tab === "scores" && (
            <div className="space-y-4">
              <div className="grid grid-cols-2 gap-3">
                {[
                  { label: "Érosion des Sols", value: `${entity.soil_erosion_score}%` },
                  { label: "Désertification", value: `${entity.desertification_score}%` },
                  { label: "Déforestation", value: `${entity.deforestation_score}%` },
                  { label: "Pression Foncière", value: `${entity.land_use_pressure_score}%` },
                  { label: "Indice Foncier", value: `${entity.estimated_land_index}/10` },
                  { label: "Dernière mise à jour", value: entity.last_updated },
                ].map(({ label, value }) => (
                  <div key={label} className="bg-white/4 rounded-lg p-3">
                    <p className="text-[11px] text-gray-500 mb-0.5">{label}</p>
                    <p className="text-sm font-semibold text-white">{value}</p>
                  </div>
                ))}
              </div>
              <div className="bg-white/4 rounded-lg p-4">
                <div className="flex justify-between items-center mb-2">
                  <span className="text-sm text-gray-300">Score Composite de Dégradation</span>
                  <span className={`text-xl font-bold ${cfg.color}`}>
                    {entity.composite_score}
                  </span>
                </div>
                <div className="h-2 bg-white/5 rounded-full overflow-hidden">
                  <div
                    className="h-full rounded-full transition-all duration-700"
                    style={{
                      width: `${Math.min(100, entity.composite_score)}%`,
                      backgroundColor:
                        entity.risk_level === "critique"
                          ? "#f87171"
                          : entity.risk_level === "élevé"
                          ? "#fb923c"
                          : entity.risk_level === "modéré"
                          ? "#fbbf24"
                          : "#34d399",
                    }}
                  />
                </div>
                <p className="text-[11px] text-gray-500 mt-1.5">
                  Formule : érosion×0.30 + désertification×0.25 + déforestation×0.25 + pression×0.20
                </p>
              </div>
            </div>
          )}

          {/* ── TAB: Signaux ── */}
          {tab === "signaux" && (
            <div className="space-y-3">
              {/* Alert level badge */}
              <div className={`rounded-xl border p-4 ${SEVERITY_STYLE[entity.risk_level] ?? ""}`}>
                <div className="flex items-center gap-2 mb-1.5">
                  <span className="font-mono text-xs font-semibold">{entity.alert_level}</span>
                  <span className="font-semibold text-sm">{entity.primary_pattern}</span>
                </div>
                {patternInfo && (
                  <p className="text-[10px] font-mono opacity-50 mt-1">
                    Signal : {patternInfo.signal_fr}
                  </p>
                )}
              </div>

              {/* Key signals */}
              <div className="bg-white/4 border border-white/10 rounded-xl p-4">
                <p className="text-xs font-medium text-gray-300 mb-3">Signaux clés détectés</p>
                <div className="space-y-2">
                  {entity.key_signals.map((sig) => (
                    <div key={sig} className="flex items-center gap-2">
                      <div className={`w-1.5 h-1.5 rounded-full shrink-0 ${cfg.dot}`} />
                      <span className="text-xs font-mono text-gray-300">{sig}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* ── TAB: Actions ── */}
          {tab === "actions" && (
            <div className="space-y-3">
              {patternInfo ? (
                <div className="bg-white/4 border border-white/10 rounded-xl p-4">
                  <div className="flex items-center gap-2 mb-2">
                    <span className="w-6 h-6 rounded-full bg-white/10 text-xs flex items-center justify-center text-gray-300 font-bold">
                      1
                    </span>
                    <span className="text-sm font-medium text-white">{patternInfo.name}</span>
                  </div>
                  <p className="text-xs text-gray-300 leading-relaxed">{patternInfo.action_fr}</p>
                </div>
              ) : (
                <div className="bg-white/4 border border-white/10 rounded-xl p-4">
                  <p className="text-sm text-gray-300 font-medium">Surveillance continue</p>
                  <p className="text-xs text-gray-400 mt-1.5 leading-relaxed">
                    Zone stable — maintenir le suivi périodique et les pratiques actuelles de conservation.
                  </p>
                </div>
              )}

              <div className="bg-slate-800/60 border border-white/8 rounded-xl p-4">
                <p className="text-xs text-gray-400">
                  <span className="text-gray-300 font-medium">Sources de données :</span>{" "}
                  FAO · UNCCD · Global Land Watch
                </p>
                <p className="text-xs text-gray-400 mt-1">
                  <span className="text-gray-300 font-medium">Dernière analyse :</span>{" "}
                  {entity.last_updated}
                </p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

// ── Page ──────────────────────────────────────────────────────────────────────

export default function LandDegradationEnginePage() {
  const [data, setData] = useState<LandDegradationSummary | null>(null);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState("all");
  const [selected, setSelected] = useState<LandDegradationEntity | null>(null);

  useEffect(() => {
    fetch("/api/land-degradation-engine")
      .then((r) => r.json())
      .then((json) => {
        // Handle sealResponse wrapper
        const payload = json?.data ?? json;
        setData(payload as LandDegradationSummary);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  const entities = data?.entities ?? [];

  const filtered =
    filter === "all" ? entities : entities.filter((e) => e.risk_level === filter);

  const totalEntities = data?.total_entities ?? 0;

  // Compute avg soil scores from entities
  const avgSoilErosion =
    entities.length > 0
      ? Math.round(entities.reduce((sum, e) => sum + e.soil_erosion_score, 0) / entities.length)
      : 0;
  const avgDesertification =
    entities.length > 0
      ? Math.round(entities.reduce((sum, e) => sum + e.desertification_score, 0) / entities.length)
      : 0;

  const critiquePct =
    totalEntities > 0
      ? Math.round(((data?.risk_distribution?.critique ?? 0) / totalEntities) * 100)
      : 0;

  const rd = data?.risk_distribution;

  return (
    <div className="min-h-screen bg-slate-950 text-white">
      <div className="max-w-7xl mx-auto px-6 py-8 space-y-8">

        {/* ── Page header ── */}
        <div className="flex items-start justify-between gap-4">
          <div>
            <h1 className="text-2xl font-bold text-white">Dégradation des Terres &amp; Érosion des Sols</h1>
            <p className="text-sm text-gray-400 mt-1">
              Moteur d&apos;intelligence Swarm — surveillance des écosystèmes terrestres et alertes environnementales
            </p>
          </div>
          <span className="text-xs text-gray-500 bg-white/5 border border-white/10 rounded-lg px-3 py-1.5">
            {totalEntities} zones analysées
          </span>
        </div>

        {/* ── Loading ── */}
        {loading && (
          <div className="flex items-center justify-center py-24">
            <div className="w-8 h-8 border-2 border-emerald-500 border-t-transparent rounded-full animate-spin" />
          </div>
        )}

        {!loading && data && (
          <>
            {/* ── KPI Cards ── */}
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
              <KpiCard
                label="Total Zones"
                value={data.total_entities}
                sub="zones surveillées"
              />
              <KpiCard
                label="Score Moyen"
                value={data.avg_composite}
                sub="dégradation composite"
                accent={data.avg_composite >= 60 ? "text-red-400" : data.avg_composite >= 40 ? "text-orange-400" : "text-emerald-400"}
              />
              <KpiCard
                label="Zones Critiques"
                value={data.critical_alerts}
                sub="intervention urgente"
                accent="text-red-400"
              />
              <KpiCard
                label="Zones Stables"
                value={(rd?.faible ?? 0) + (rd?.["modéré"] ?? 0)}
                sub="faible à modéré"
                accent="text-emerald-400"
              />
              <KpiCard
                label="Indice Dégradation"
                value={`${data.avg_estimated_land_index}/10`}
                sub="indice foncier moyen"
                accent={data.avg_estimated_land_index >= 6 ? "text-red-400" : data.avg_estimated_land_index >= 4 ? "text-orange-400" : "text-emerald-400"}
              />
              <KpiCard
                label="Confiance Analyse"
                value={`${data.confidence_score}%`}
                sub={data.data_sources.join(" · ")}
                accent="text-indigo-400"
              />
            </div>

            {/* ── Gauges + Distribution ── */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">

              {/* Gauges */}
              <div className="bg-white/4 border border-white/10 rounded-xl p-6">
                <h2 className="text-sm font-semibold text-gray-300 mb-6">Indicateurs Clés</h2>
                <div className="grid grid-cols-4 gap-4">
                  <GaugeRing
                    value={data.avg_composite}
                    max={100}
                    label="Score Composite"
                    color="#fb923c"
                  />
                  <GaugeRing
                    value={avgSoilErosion}
                    max={100}
                    label="Érosion Moy."
                    color="#f87171"
                  />
                  <GaugeRing
                    value={critiquePct}
                    max={100}
                    label="% Critique"
                    color="#ef4444"
                  />
                  <GaugeRing
                    value={data.avg_estimated_land_index * 10}
                    max={100}
                    label="Indice Foncier"
                    color="#818cf8"
                  />
                </div>
              </div>

              {/* Distribution bars */}
              <div className="bg-white/4 border border-white/10 rounded-xl p-6">
                <h2 className="text-sm font-semibold text-gray-300 mb-6">
                  Distribution par Niveau de Risque
                </h2>
                <div className="space-y-4">
                  <DistBar
                    label="Critique"
                    count={rd?.critique ?? 0}
                    total={totalEntities}
                    color="#f87171"
                  />
                  <DistBar
                    label="Élevé"
                    count={rd?.["élevé"] ?? 0}
                    total={totalEntities}
                    color="#fb923c"
                  />
                  <DistBar
                    label="Modéré"
                    count={rd?.["modéré"] ?? 0}
                    total={totalEntities}
                    color="#fbbf24"
                  />
                  <DistBar
                    label="Faible"
                    count={rd?.faible ?? 0}
                    total={totalEntities}
                    color="#34d399"
                  />
                </div>

                <div className="mt-5 pt-4 border-t border-white/8 grid grid-cols-2 gap-3">
                  <div className="bg-white/4 rounded-lg p-3">
                    <p className="text-[11px] text-gray-500">Version moteur</p>
                    <p className="text-lg font-bold text-white mt-0.5">{data.engine_version}</p>
                  </div>
                  <div className="bg-white/4 rounded-lg p-3">
                    <p className="text-[11px] text-gray-500">Désertif. Moyenne</p>
                    <p className="text-lg font-bold text-amber-400 mt-0.5">
                      {avgDesertification}%
                    </p>
                  </div>
                </div>
              </div>
            </div>

            {/* ── Filter pills ── */}
            <div className="flex flex-wrap gap-2">
              {FILTER_OPTIONS.map((opt) => {
                const isActive = filter === opt.key;
                const cfg = opt.key !== "all" ? RISK_CONFIG[opt.key] : null;
                return (
                  <button
                    key={opt.key}
                    onClick={() => setFilter(opt.key)}
                    className={`px-4 py-1.5 rounded-full text-sm font-medium border transition-all ${
                      isActive
                        ? cfg
                          ? `${cfg.bg} ${cfg.border} ${cfg.color}`
                          : "bg-white/10 border-white/20 text-white"
                        : "bg-transparent border-white/10 text-gray-400 hover:text-white hover:border-white/20"
                    }`}
                  >
                    {opt.label}
                    {opt.key === "critique" && (
                      <span className="ml-1.5 text-xs opacity-70">{rd?.critique ?? 0}</span>
                    )}
                    {opt.key === "élevé" && (
                      <span className="ml-1.5 text-xs opacity-70">{rd?.["élevé"] ?? 0}</span>
                    )}
                    {opt.key === "modéré" && (
                      <span className="ml-1.5 text-xs opacity-70">{rd?.["modéré"] ?? 0}</span>
                    )}
                    {opt.key === "faible" && (
                      <span className="ml-1.5 text-xs opacity-70">{rd?.faible ?? 0}</span>
                    )}
                    {opt.key === "all" && (
                      <span className="ml-1.5 text-xs opacity-70">{totalEntities}</span>
                    )}
                  </button>
                );
              })}
            </div>

            {/* ── Entity cards grid ── */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
              {filtered.map((entity) => (
                <EntityCard key={entity.id} entity={entity} onClick={setSelected} />
              ))}
              {filtered.length === 0 && (
                <div className="col-span-full text-center py-12 text-gray-400 text-sm">
                  Aucune zone dans ce niveau de risque
                </div>
              )}
            </div>

            {/* ── Alert strip for critical zones ── */}
            {(data.critical_alerts ?? 0) > 0 && (
              <div className="bg-red-500/8 border border-red-500/20 rounded-xl px-5 py-4 flex items-start gap-3">
                <div className="w-2 h-2 rounded-full bg-red-500 mt-1.5 shrink-0 animate-pulse" />
                <div>
                  <p className="text-sm font-medium text-red-400">
                    {data.critical_alerts} zone{data.critical_alerts > 1 ? "s" : ""} en dégradation critique — alerte ROUGE
                  </p>
                  <p className="text-xs text-red-400/70 mt-0.5">
                    Zones prioritaires :{" "}
                    <span className="font-medium">{data.top_risk_entities.join(", ")}</span>
                  </p>
                </div>
              </div>
            )}
          </>
        )}
      </div>

      {/* ── Detail Modal ── */}
      {selected && (
        <DetailModal entity={selected} onClose={() => setSelected(null)} />
      )}
    </div>
  );
}
