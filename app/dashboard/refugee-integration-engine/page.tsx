"use client";

import { useEffect, useState } from "react";

// ── Types ────────────────────────────────────────────────────────────────────

interface EntityRecord {
  entity_id: string;
  name: string;
  country: string;
  sector: string;
  composite_score: number;
  social_integration_barrier_score: number;
  economic_exclusion_score: number;
  legal_vulnerability_score: number;
  mental_health_crisis_score: number;
  risk_level: string;
  primary_pattern: string;
  key_signals: string[];
  estimated_refugee_index: number;
  last_updated: string;
  confidence_level: number;
}

interface RefugeeSummary {
  total_entities: number;
  avg_composite: number;
  risk_distribution: { critique: number; "élevé": number; "modéré": number; faible: number };
  pattern_distribution: Record<string, number>;
  top_risk_entities: string[];
  critical_alerts: string[];
  last_analysis: string;
  engine_version: string;
  domain: string;
  confidence_score: number;
  data_sources: string[];
  entities: EntityRecord[];
  avg_estimated_refugee_index: number;
}

interface RefugeeData {
  total_entities: number;
  avg_composite: number;
  risk_distribution: { critique: number; "élevé": number; "modéré": number; faible: number };
  pattern_distribution: Record<string, number>;
  top_risk_entities: string[];
  critical_alerts: string[];
  last_analysis: string;
  engine_version: string;
  domain: string;
  confidence_score: number;
  data_sources: string[];
  entities: EntityRecord[];
  avg_estimated_refugee_index: number;
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
  { key: "tous", label: "Tous" },
  { key: "critique", label: "Critique" },
  { key: "élevé", label: "Élevé" },
  { key: "modéré", label: "Modéré" },
  { key: "faible", label: "Faible" },
];

const PATTERN_LABELS: Record<string, string> = {
  integration_failure: "Échec d'Intégration",
  economic_exclusion: "Exclusion Économique",
  legal_precarity: "Précarité Juridique",
  mental_health_crisis: "Crise de Santé Mentale",
  successful_integration: "Intégration Réussie",
};

const PATTERN_ACTIONS: Record<string, string> = {
  integration_failure: "Programme d'intégration d'urgence multidimensionnel",
  economic_exclusion: "Insertion professionnelle prioritaire et formation linguistique",
  legal_precarity: "Assistance juridique d'urgence et accompagnement administratif",
  mental_health_crisis: "Soutien psychologique immédiat et réseaux communautaires",
  successful_integration: "Renforcement des programmes de réussite et partage des meilleures pratiques",
};

const SEVERITY_STYLE: Record<string, string> = {
  integration_failure: "text-red-400 bg-red-500/10 border-red-500/25",
  economic_exclusion: "text-orange-400 bg-orange-500/10 border-orange-500/25",
  legal_precarity: "text-purple-400 bg-purple-500/10 border-purple-500/25",
  mental_health_crisis: "text-pink-400 bg-pink-500/10 border-pink-500/25",
  successful_integration: "text-emerald-400 bg-emerald-500/10 border-emerald-500/25",
};

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
  entity: EntityRecord;
  onClick: (e: EntityRecord) => void;
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
          <p className="text-xs text-gray-400 truncate mt-0.5">
            {entity.country} · {entity.sector}
          </p>
        </div>
        <span
          className={`shrink-0 text-xs font-medium px-2.5 py-1 rounded-full border ${cfg.bg} ${cfg.border} ${cfg.color}`}
        >
          {cfg.label}
        </span>
      </div>

      <div className="grid grid-cols-2 gap-2 mb-3">
        <div className="bg-white/4 rounded-lg p-2 text-center">
          <p className="text-sm font-bold text-white">{entity.composite_score}</p>
          <p className="text-[10px] text-gray-500">Score Composite</p>
        </div>
        <div className="bg-white/4 rounded-lg p-2 text-center">
          <p className="text-sm font-bold text-white">{entity.estimated_refugee_index}/10</p>
          <p className="text-[10px] text-gray-500">Indice Réfugié</p>
        </div>
      </div>

      <div className="flex items-center justify-between text-xs">
        <span className="text-gray-400 truncate">
          {PATTERN_LABELS[entity.primary_pattern] ?? entity.primary_pattern}
        </span>
        <span className="text-gray-500 shrink-0 ml-2">
          Confiance {Math.round(entity.confidence_level * 100)}%
        </span>
      </div>
    </button>
  );
}

// ── DetailModal ───────────────────────────────────────────────────────────────

function DetailModal({
  entity,
  onClose,
}: {
  entity: EntityRecord;
  onClose: () => void;
}) {
  const [tab, setTab] = useState<"scores" | "signaux" | "actions">("scores");
  const cfg = RISK_CONFIG[entity.risk_level] ?? RISK_CONFIG.faible;

  const TABS = [
    { key: "scores", label: "Scores" },
    { key: "signaux", label: "Signaux" },
    { key: "actions", label: "Actions" },
  ] as const;

  const scoreColor =
    entity.risk_level === "critique"
      ? "#f87171"
      : entity.risk_level === "élevé"
      ? "#fb923c"
      : entity.risk_level === "modéré"
      ? "#fbbf24"
      : "#34d399";

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
              <p className="text-sm text-gray-400 mt-0.5">
                {entity.country} · {entity.sector}
              </p>
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
                  { label: "Barrières d'Intégration Sociale", value: `${entity.social_integration_barrier_score}/100` },
                  { label: "Exclusion Économique", value: `${entity.economic_exclusion_score}/100` },
                  { label: "Vulnérabilité Juridique", value: `${entity.legal_vulnerability_score}/100` },
                  { label: "Crise de Santé Mentale", value: `${entity.mental_health_crisis_score}/100` },
                  { label: "Indice Réfugié Estimé", value: `${entity.estimated_refugee_index}/10` },
                  { label: "Niveau de Confiance", value: `${Math.round(entity.confidence_level * 100)}%` },
                  { label: "Pays d'Origine", value: entity.country },
                  { label: "Pays d'Accueil", value: entity.sector },
                  { label: "Identifiant", value: entity.entity_id },
                  { label: "Dernière Mise à Jour", value: entity.last_updated },
                ].map(({ label, value }) => (
                  <div key={label} className="bg-white/4 rounded-lg p-3">
                    <p className="text-[11px] text-gray-500 mb-0.5">{label}</p>
                    <p className="text-sm font-semibold text-white">{value}</p>
                  </div>
                ))}
              </div>
              <div className="bg-white/4 rounded-lg p-4">
                <div className="flex justify-between items-center mb-2">
                  <span className="text-sm text-gray-300">Score Composite de Vulnérabilité</span>
                  <span className={`text-xl font-bold ${cfg.color}`}>
                    {entity.composite_score}
                  </span>
                </div>
                <div className="h-2 bg-white/5 rounded-full overflow-hidden">
                  <div
                    className="h-full rounded-full transition-all duration-700"
                    style={{
                      width: `${Math.min(100, entity.composite_score)}%`,
                      backgroundColor: scoreColor,
                    }}
                  />
                </div>
                <p className="text-[11px] text-gray-500 mt-1.5">
                  Formule : intégration sociale×0.30 + exclusion économique×0.25 + vulnérabilité juridique×0.25 + santé mentale×0.20
                </p>
              </div>
            </div>
          )}

          {/* ── TAB: Signaux ── */}
          {tab === "signaux" && (
            <div className="space-y-3">
              <div
                className={`rounded-xl border p-4 ${SEVERITY_STYLE[entity.primary_pattern] ?? ""}`}
              >
                <div className="flex items-center gap-2 mb-2">
                  <span className="font-semibold text-sm">
                    {PATTERN_LABELS[entity.primary_pattern] ?? entity.primary_pattern}
                  </span>
                  <span className="ml-auto text-[10px] font-medium uppercase tracking-wide opacity-70">
                    {entity.risk_level}
                  </span>
                </div>
                <div className="space-y-2 mt-3">
                  {entity.key_signals.map((signal, i) => (
                    <div key={i} className="flex items-start gap-2">
                      <span className="w-1.5 h-1.5 rounded-full bg-current mt-1.5 shrink-0 opacity-70" />
                      <p className="text-xs leading-relaxed opacity-80">{signal}</p>
                    </div>
                  ))}
                </div>
              </div>

              <div className="bg-white/4 border border-white/10 rounded-xl p-4 space-y-3">
                <p className="text-xs font-medium text-gray-300">Scores de vulnérabilité détaillés</p>
                {[
                  { label: "Barrières d'Intégration Sociale", value: entity.social_integration_barrier_score, color: "#f87171" },
                  { label: "Exclusion Économique", value: entity.economic_exclusion_score, color: "#fb923c" },
                  { label: "Vulnérabilité Juridique", value: entity.legal_vulnerability_score, color: "#c084fc" },
                  { label: "Crise de Santé Mentale", value: entity.mental_health_crisis_score, color: "#f472b6" },
                ].map(({ label, value, color }) => (
                  <div key={label} className="space-y-1">
                    <div className="flex justify-between text-xs">
                      <span className="text-gray-400">{label}</span>
                      <span className="text-gray-300 font-medium">{value}/100</span>
                    </div>
                    <div className="h-1.5 bg-white/5 rounded-full overflow-hidden">
                      <div
                        className="h-full rounded-full"
                        style={{ width: `${value}%`, backgroundColor: color }}
                      />
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* ── TAB: Actions ── */}
          {tab === "actions" && (
            <div className="space-y-3">
              <div className="bg-white/4 border border-white/10 rounded-xl p-4">
                <div className="flex items-center gap-2 mb-2">
                  <span className="w-6 h-6 rounded-full bg-white/10 text-xs flex items-center justify-center text-gray-300 font-bold">
                    1
                  </span>
                  <span className="text-sm font-medium text-white">
                    {PATTERN_LABELS[entity.primary_pattern] ?? entity.primary_pattern}
                  </span>
                </div>
                <p className="text-xs text-gray-300 leading-relaxed">
                  {PATTERN_ACTIONS[entity.primary_pattern] ?? "Suivi personnalisé recommandé"}
                </p>
              </div>

              <div className="bg-slate-800/60 border border-white/8 rounded-xl p-4 space-y-2">
                <p className="text-xs text-gray-400">
                  <span className="text-gray-300 font-medium">Pays d&apos;origine :</span>{" "}
                  {entity.country}
                </p>
                <p className="text-xs text-gray-400">
                  <span className="text-gray-300 font-medium">Pays d&apos;accueil :</span>{" "}
                  {entity.sector}
                </p>
                <p className="text-xs text-gray-400">
                  <span className="text-gray-300 font-medium">Indice réfugié estimé :</span>{" "}
                  {entity.estimated_refugee_index}/10
                </p>
                <p className="text-xs text-gray-400">
                  <span className="text-gray-300 font-medium">Niveau de confiance :</span>{" "}
                  {Math.round(entity.confidence_level * 100)}%
                </p>
              </div>

              {entity.risk_level === "critique" && (
                <div className="bg-red-500/8 border border-red-500/20 rounded-xl p-4">
                  <p className="text-sm font-medium text-red-400">Intervention d&apos;urgence requise</p>
                  <p className="text-xs text-red-400/70 mt-1 leading-relaxed">
                    Ce programme présente un niveau de vulnérabilité critique. Une action coordonnée
                    entre les services sociaux, juridiques et de santé mentale doit être déclenchée
                    immédiatement.
                  </p>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

// ── Page ──────────────────────────────────────────────────────────────────────

export default function RefugeeIntegrationEnginePage() {
  const [data, setData] = useState<RefugeeData | null>(null);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState("tous");
  const [selected, setSelected] = useState<EntityRecord | null>(null);

  useEffect(() => {
    fetch("/api/refugee-integration-engine")
      .then((r) => r.json())
      .then((json) => {
        const payload = json?.data ?? json;
        setData(payload as RefugeeData);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  const entities = data?.entities ?? [];
  const rd = data?.risk_distribution;

  const filtered =
    filter === "tous" ? entities : entities.filter((e) => e.risk_level === filter);

  const totalEntities = data?.total_entities ?? 0;

  return (
    <div className="min-h-screen bg-slate-950 text-white">
      <div className="max-w-7xl mx-auto px-6 py-8 space-y-8">

        {/* ── Page header ── */}
        <div className="flex items-start justify-between gap-4">
          <div>
            <h1 className="text-2xl font-bold text-white">Moteur d&apos;Intelligence — Intégration des Réfugiés</h1>
            <p className="text-sm text-gray-400 mt-1">
              Analyse multidimensionnelle des vulnérabilités et des trajectoires d&apos;intégration
            </p>
          </div>
          <span className="text-xs text-gray-500 bg-white/5 border border-white/10 rounded-lg px-3 py-1.5">
            {totalEntities} programmes analysés
          </span>
        </div>

        {/* ── Loading ── */}
        {loading && (
          <div className="flex items-center justify-center py-24">
            <div className="w-8 h-8 border-2 border-indigo-500 border-t-transparent rounded-full animate-spin" />
          </div>
        )}

        {!loading && data && (
          <>
            {/* ── KPI Cards ── */}
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
              <KpiCard
                label="Programmes Analysés"
                value={data.total_entities}
                sub="couverts par le moteur"
              />
              <KpiCard
                label="Score Composite Moyen"
                value={data.avg_composite}
                sub="vulnérabilité agrégée"
                accent={
                  data.avg_composite >= 60
                    ? "text-red-400"
                    : data.avg_composite >= 40
                    ? "text-orange-400"
                    : data.avg_composite >= 20
                    ? "text-amber-400"
                    : "text-emerald-400"
                }
              />
              <KpiCard
                label="Programmes Critiques"
                value={rd?.critique ?? 0}
                sub="intervention urgente"
                accent="text-red-400"
              />
              <KpiCard
                label="Niveau Élevé"
                value={rd?.["élevé"] ?? 0}
                sub="surveillance renforcée"
                accent="text-orange-400"
              />
              <KpiCard
                label="Score de Confiance"
                value={`${Math.round((data.confidence_score ?? 0) * 100)}%`}
                sub="fiabilité des données"
                accent="text-indigo-400"
              />
              <KpiCard
                label="Indice Réfugié Moyen"
                value={`${data.avg_estimated_refugee_index}/10`}
                sub="trajectoire d'intégration"
                accent={data.avg_estimated_refugee_index >= 6 ? "text-red-400" : data.avg_estimated_refugee_index >= 4 ? "text-amber-400" : "text-emerald-400"}
              />
            </div>

            {/* ── Gauges + Distribution ── */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">

              {/* Gauges */}
              <div className="bg-white/4 border border-white/10 rounded-xl p-6">
                <h2 className="text-sm font-semibold text-gray-300 mb-6">Indicateurs de Vulnérabilité</h2>
                <div className="grid grid-cols-4 gap-4">
                  <GaugeRing
                    value={
                      entities.length > 0
                        ? Math.round(entities.reduce((s, e) => s + e.social_integration_barrier_score, 0) / entities.length)
                        : 0
                    }
                    max={100}
                    label="Barrières Sociales"
                    color="#f87171"
                  />
                  <GaugeRing
                    value={
                      entities.length > 0
                        ? Math.round(entities.reduce((s, e) => s + e.economic_exclusion_score, 0) / entities.length)
                        : 0
                    }
                    max={100}
                    label="Exclusion Économique"
                    color="#fb923c"
                  />
                  <GaugeRing
                    value={
                      entities.length > 0
                        ? Math.round(entities.reduce((s, e) => s + e.legal_vulnerability_score, 0) / entities.length)
                        : 0
                    }
                    max={100}
                    label="Vulnérabilité Juridique"
                    color="#c084fc"
                  />
                  <GaugeRing
                    value={
                      entities.length > 0
                        ? Math.round(entities.reduce((s, e) => s + e.mental_health_crisis_score, 0) / entities.length)
                        : 0
                    }
                    max={100}
                    label="Santé Mentale"
                    color="#f472b6"
                  />
                </div>
              </div>

              {/* Distribution bars */}
              <div className="bg-white/4 border border-white/10 rounded-xl p-6">
                <h2 className="text-sm font-semibold text-gray-300 mb-6">
                  Distribution par Niveau de Vulnérabilité
                </h2>
                <div className="space-y-4">
                  <DistBar
                    label="Critique"
                    count={rd?.critique ?? 0}
                    total={data.total_entities}
                    color="#f87171"
                  />
                  <DistBar
                    label="Élevé"
                    count={rd?.["élevé"] ?? 0}
                    total={data.total_entities}
                    color="#fb923c"
                  />
                  <DistBar
                    label="Modéré"
                    count={rd?.["modéré"] ?? 0}
                    total={data.total_entities}
                    color="#fbbf24"
                  />
                  <DistBar
                    label="Faible"
                    count={rd?.faible ?? 0}
                    total={data.total_entities}
                    color="#34d399"
                  />
                </div>

                <div className="mt-5 pt-4 border-t border-white/8 grid grid-cols-2 gap-3">
                  <div className="bg-white/4 rounded-lg p-3">
                    <p className="text-[11px] text-gray-500">Alertes critiques actives</p>
                    <p className="text-lg font-bold text-red-400 mt-0.5">
                      {data.critical_alerts?.length ?? 0}
                    </p>
                  </div>
                  <div className="bg-white/4 rounded-lg p-3">
                    <p className="text-[11px] text-gray-500">Indice Réfugié Moyen</p>
                    <p className="text-lg font-bold text-indigo-400 mt-0.5">
                      {data.avg_estimated_refugee_index}/10
                    </p>
                  </div>
                </div>
              </div>
            </div>

            {/* ── Filter pills ── */}
            <div className="flex flex-wrap gap-2">
              {FILTER_OPTIONS.map((opt) => {
                const isActive = filter === opt.key;
                const cfg = opt.key !== "tous" ? RISK_CONFIG[opt.key] : null;
                const count =
                  opt.key === "tous"
                    ? data.total_entities
                    : opt.key === "critique"
                    ? (rd?.critique ?? 0)
                    : opt.key === "élevé"
                    ? (rd?.["élevé"] ?? 0)
                    : opt.key === "modéré"
                    ? (rd?.["modéré"] ?? 0)
                    : (rd?.faible ?? 0);
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
                    <span className="ml-1.5 text-xs opacity-70">{count}</span>
                  </button>
                );
              })}
            </div>

            {/* ── Entity cards grid ── */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
              {filtered.map((entity) => (
                <EntityCard key={entity.entity_id} entity={entity} onClick={setSelected} />
              ))}
              {filtered.length === 0 && (
                <div className="col-span-full text-center py-12 text-gray-400 text-sm">
                  Aucun programme dans ce niveau de vulnérabilité
                </div>
              )}
            </div>

            {/* ── Critical alerts strip ── */}
            {(rd?.critique ?? 0) > 0 && (
              <div className="bg-red-500/8 border border-red-500/20 rounded-xl px-5 py-4 flex items-start gap-3">
                <div className="w-2 h-2 rounded-full bg-red-500 mt-1.5 shrink-0 animate-pulse" />
                <div>
                  <p className="text-sm font-medium text-red-400">
                    {rd?.critique} programme{(rd?.critique ?? 0) > 1 ? "s" : ""} en situation critique — intervention humanitaire urgente requise
                  </p>
                  <p className="text-xs text-red-400/70 mt-0.5">
                    Programmes les plus vulnérables :{" "}
                    <span className="font-medium">
                      {data.top_risk_entities?.slice(0, 2).join(", ")}
                    </span>
                  </p>
                </div>
              </div>
            )}

            {/* ── Data sources footer ── */}
            <div className="bg-white/2 border border-white/8 rounded-xl px-5 py-4">
              <p className="text-xs text-gray-500 mb-2 font-medium">Sources de données</p>
              <div className="flex flex-wrap gap-2">
                {data.data_sources?.map((src) => (
                  <span
                    key={src}
                    className="text-xs text-gray-400 bg-white/5 border border-white/10 rounded-lg px-3 py-1"
                  >
                    {src}
                  </span>
                ))}
              </div>
            </div>
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
