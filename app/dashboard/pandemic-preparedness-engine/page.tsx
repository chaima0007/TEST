"use client";

import { useEffect, useState } from "react";

// ── Types ────────────────────────────────────────────────────────────────────

interface PandemicEntity {
  id: string;
  name: string;
  country: string;
  sector: string;
  composite_score: number;
  surveillance_gap_score: number;
  healthcare_capacity_gap_score: number;
  vaccine_access_deficit_score: number;
  response_coordination_gap_score: number;
  risk_level: string;
  primary_pattern: string;
  key_signals: string[];
  estimated_pandemic_index: number;
  last_updated: string;
  alert_level: string;
}

interface PandemicSummary {
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
  entities: PandemicEntity[];
  avg_estimated_pandemic_index: number;
}

interface PandemicData {
  entities: PandemicEntity[];
  total_entities?: number;
  avg_composite?: number;
  risk_distribution?: Record<string, number>;
  pattern_distribution?: Record<string, number>;
  top_risk_entities?: string[];
  critical_alerts?: number;
  last_analysis?: string;
  engine_version?: string;
  domain?: string;
  confidence_score?: number;
  data_sources?: string[];
  avg_estimated_pandemic_index?: number;
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

// ── Patterns ──────────────────────────────────────────────────────────────────

const PATTERNS_META = [
  {
    name: "Effondrement du Système de Surveillance",
    severity: "critique",
    description: "Défaillance critique des réseaux de surveillance épidémique — détection tardive des foyers.",
    action: "Déploiement d'urgence de réseaux sentinelles et renforcement OMS.",
    signal: "surveillance_gap > 85 et response_coordination_gap > 80",
    test: (e: PandemicEntity) => e.surveillance_gap_score > 85 && e.response_coordination_gap_score > 80,
  },
  {
    name: "Saturation des Capacités Hospitalières",
    severity: "critique",
    description: "Capacités hospitalières insuffisantes face à une montée en charge pandémique.",
    action: "Activation des plans de débordement et hôpitaux de campagne.",
    signal: "healthcare_capacity_gap > 80 et vaccine_access_deficit > 75",
    test: (e: PandemicEntity) => e.healthcare_capacity_gap_score > 80 && e.vaccine_access_deficit_score > 75,
  },
  {
    name: "Désert Vaccinal Critique",
    severity: "élevé",
    description: "Accès vaccinal très limité combiné à une surveillance insuffisante — vulnérabilité structurelle.",
    action: "Mécanisme COVAX renforcé et transferts de technologie vaccin.",
    signal: "vaccine_access_deficit > 70 et surveillance_gap > 65",
    test: (e: PandemicEntity) => e.vaccine_access_deficit_score > 70 && e.surveillance_gap_score > 65,
  },
  {
    name: "Déficit de Coordination Interagences",
    severity: "élevé",
    description: "Coordination insuffisante entre agences nationales et internationales de santé.",
    action: "Cellule de crise interministérielle et protocoles SIMEX.",
    signal: "response_coordination_gap > 65 et healthcare_capacity_gap > 60",
    test: (e: PandemicEntity) => e.response_coordination_gap_score > 65 && e.healthcare_capacity_gap_score > 60,
  },
  {
    name: "Fragilité Sanitaire Structurelle",
    severity: "modéré",
    description: "Infrastructure de santé primaire insuffisante — risque d'effondrement en cas de crise.",
    action: "Investissements préventifs en infrastructure de santé primaire.",
    signal: "surveillance_gap > 40 et healthcare_capacity_gap > 35",
    test: (e: PandemicEntity) => e.surveillance_gap_score > 40 && e.healthcare_capacity_gap_score > 35,
  },
];

const SEVERITY_STYLE: Record<string, string> = {
  critique: "text-red-400 bg-red-500/10 border-red-500/25",
  "élevé": "text-orange-400 bg-orange-500/10 border-orange-500/25",
  "modéré": "text-amber-400 bg-amber-500/10 border-amber-500/25",
};

// ── GaugeRing ─────────────────────────────────────────────────────────────────

function GaugeRing({
  value,
  max,
  label,
  color,
  invert = false,
}: {
  value: number;
  max: number;
  label: string;
  color: string;
  invert?: boolean;
}) {
  const pct = Math.min(100, Math.max(0, (value / max) * 100));
  const displayPct = invert ? 100 - pct : pct;
  const r = 36;
  const circ = 2 * Math.PI * r;
  const offset = circ - (displayPct / 100) * circ;

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
  entity: PandemicEntity;
  onClick: (e: PandemicEntity) => void;
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
          <p className="text-xs text-gray-400 truncate mt-0.5">{entity.country} — {entity.sector}</p>
        </div>
        <span
          className={`shrink-0 text-xs font-medium px-2.5 py-1 rounded-full border ${cfg.bg} ${cfg.border} ${cfg.color}`}
        >
          {cfg.label}
        </span>
      </div>

      <div className="grid grid-cols-3 gap-2 mb-3">
        <div className="bg-white/4 rounded-lg p-2 text-center">
          <p className="text-sm font-bold text-white">{entity.surveillance_gap_score}%</p>
          <p className="text-[10px] text-gray-500">Surveillance</p>
        </div>
        <div className="bg-white/4 rounded-lg p-2 text-center">
          <p className="text-sm font-bold text-white">{entity.healthcare_capacity_gap_score}%</p>
          <p className="text-[10px] text-gray-500">Capacité</p>
        </div>
        <div className="bg-white/4 rounded-lg p-2 text-center">
          <p className="text-sm font-bold text-white">{entity.vaccine_access_deficit_score}%</p>
          <p className="text-[10px] text-gray-500">Vaccin</p>
        </div>
      </div>

      <div className="flex items-center justify-between text-xs">
        <span className="text-gray-400">
          Score composite:{" "}
          <span className={`font-bold ${cfg.color}`}>{entity.composite_score}</span>
        </span>
        <span className={`font-medium text-[10px] px-2 py-0.5 rounded ${
          entity.alert_level === "ROUGE"
            ? "bg-red-500/20 text-red-400"
            : entity.alert_level === "ORANGE"
            ? "bg-orange-500/20 text-orange-400"
            : entity.alert_level === "JAUNE"
            ? "bg-amber-500/20 text-amber-400"
            : "bg-emerald-500/20 text-emerald-400"
        }`}>
          {entity.alert_level}
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
  entity: PandemicEntity;
  onClose: () => void;
}) {
  const [tab, setTab] = useState<"scores" | "signaux" | "actions">("scores");
  const cfg = RISK_CONFIG[entity.risk_level] ?? RISK_CONFIG.faible;
  const triggered = PATTERNS_META.filter((p) => p.test(entity));

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
              <p className="text-sm text-gray-400 mt-0.5">{entity.country} — {entity.sector}</p>
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
                  { label: "Surveillance Gap", value: `${entity.surveillance_gap_score}%` },
                  { label: "Capacité Hospitalière", value: `${entity.healthcare_capacity_gap_score}%` },
                  { label: "Déficit Vaccinal", value: `${entity.vaccine_access_deficit_score}%` },
                  { label: "Coord. Interagences", value: `${entity.response_coordination_gap_score}%` },
                  { label: "Indice Pandémique", value: `${entity.estimated_pandemic_index}/10` },
                  { label: "Niveau d'Alerte", value: entity.alert_level },
                  { label: "Pattern Primaire", value: entity.primary_pattern },
                  { label: "Dernière MAJ", value: entity.last_updated },
                ].map(({ label, value }) => (
                  <div key={label} className="bg-white/4 rounded-lg p-3">
                    <p className="text-[11px] text-gray-500 mb-0.5">{label}</p>
                    <p className="text-sm font-semibold text-white">{value}</p>
                  </div>
                ))}
              </div>

              <div className="bg-white/4 rounded-lg p-4">
                <div className="flex justify-between items-center mb-2">
                  <span className="text-sm text-gray-300">Score Composite</span>
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
                  Formule : surveillance×0.30 + capacité_santé×0.25 + vaccin_accès×0.25 + coordination×0.20
                </p>
              </div>

              <div className="bg-white/4 rounded-lg p-3">
                <p className="text-[11px] text-gray-500 mb-1.5">Signaux Clés</p>
                <div className="flex flex-wrap gap-1.5">
                  {entity.key_signals.map((sig) => (
                    <span key={sig} className="text-[10px] font-mono bg-white/8 text-gray-300 rounded px-2 py-0.5">
                      {sig}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* ── TAB: Signaux ── */}
          {tab === "signaux" && (
            <div className="space-y-3">
              {triggered.length === 0 ? (
                <div className="text-center py-8 text-gray-400 text-sm">
                  Aucun signal d&apos;alerte critique détecté — système résilient
                </div>
              ) : (
                triggered.map((p) => (
                  <div
                    key={p.name}
                    className={`rounded-xl border p-4 ${SEVERITY_STYLE[p.severity] ?? ""}`}
                  >
                    <div className="flex items-center gap-2 mb-1.5">
                      <span className="font-semibold text-sm">{p.name}</span>
                      <span className="ml-auto text-[10px] font-medium uppercase tracking-wide opacity-70">
                        {p.severity}
                      </span>
                    </div>
                    <p className="text-xs leading-relaxed opacity-80">{p.description}</p>
                    <p className="text-[10px] font-mono opacity-50 mt-1.5">Signal : {p.signal}</p>
                  </div>
                ))
              )}

              {triggered.length === 0 && (
                <div className="mt-2 bg-emerald-500/10 border border-emerald-500/25 rounded-xl p-4">
                  <p className="text-emerald-400 text-sm font-medium">Système sanitaire résilient</p>
                  <p className="text-xs text-emerald-400/70 mt-1">
                    Surveillance {entity.surveillance_gap_score}% · Capacité {entity.healthcare_capacity_gap_score}% ·
                    Vaccin {entity.vaccine_access_deficit_score}%
                  </p>
                </div>
              )}
            </div>
          )}

          {/* ── TAB: Actions ── */}
          {tab === "actions" && (
            <div className="space-y-3">
              {triggered.length === 0 ? (
                <div className="bg-white/4 border border-white/10 rounded-xl p-4">
                  <p className="text-sm text-gray-300 font-medium">Plan de maintien de résilience</p>
                  <p className="text-xs text-gray-400 mt-1.5 leading-relaxed">
                    Système en bonne santé — maintenir les investissements préventifs et renforcer
                    la coopération internationale via les protocoles OMS.
                  </p>
                </div>
              ) : (
                triggered.map((p, i) => (
                  <div key={p.name} className="bg-white/4 border border-white/10 rounded-xl p-4">
                    <div className="flex items-center gap-2 mb-2">
                      <span className="w-6 h-6 rounded-full bg-white/10 text-xs flex items-center justify-center text-gray-300 font-bold">
                        {i + 1}
                      </span>
                      <span className="text-sm font-medium text-white">{p.name}</span>
                    </div>
                    <p className="text-xs text-gray-300 leading-relaxed">{p.action}</p>
                  </div>
                ))
              )}

              <div className="bg-slate-800/60 border border-white/8 rounded-xl p-4">
                <p className="text-xs text-gray-400">
                  <span className="text-gray-300 font-medium">Indice pandémique :</span>{" "}
                  {entity.estimated_pandemic_index}/10
                </p>
                <p className="text-xs text-gray-400 mt-1">
                  <span className="text-gray-300 font-medium">Alerte :</span>{" "}
                  {entity.alert_level} — {entity.primary_pattern}
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

export default function PandemicPreparednessPage() {
  const [data, setData] = useState<PandemicData | null>(null);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState("all");
  const [selected, setSelected] = useState<PandemicEntity | null>(null);

  useEffect(() => {
    fetch("/api/pandemic-preparedness-engine")
      .then((r) => r.json())
      .then((json) => {
        // Handle sealResponse wrapper
        const payload = json?.data ?? json;
        setData(payload as PandemicData);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  const entities = data?.entities ?? [];
  const totalEntities = data?.total_entities ?? 0;
  const avgComposite = data?.avg_composite ?? 0;
  const criticalAlerts = data?.critical_alerts ?? 0;
  const confidenceScore = data?.confidence_score ?? 0;
  const avgPandemicIndex = data?.avg_estimated_pandemic_index ?? 0;
  const riskDist = data?.risk_distribution ?? { critique: 0, "élevé": 0, "modéré": 0, faible: 0 };
  const resilientSystems = (riskDist.faible ?? 0) + (riskDist["modéré"] ?? 0);

  const filtered =
    filter === "all" ? entities : entities.filter((e) => e.risk_level === filter);

  return (
    <div className="min-h-screen bg-slate-950 text-white">
      <div className="max-w-7xl mx-auto px-6 py-8 space-y-8">

        {/* ── Page header ── */}
        <div className="flex items-start justify-between gap-4">
          <div>
            <h1 className="text-2xl font-bold text-white">Préparation Pandémique & Sécurité Sanitaire</h1>
            <p className="text-sm text-gray-400 mt-1">
              Moteur d&apos;intelligence Swarm — analyse des gaps de préparation et des risques sanitaires mondiaux
            </p>
          </div>
          <span className="text-xs text-gray-500 bg-white/5 border border-white/10 rounded-lg px-3 py-1.5">
            {totalEntities} systèmes analysés
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
                label="Total Entités"
                value={totalEntities}
                sub="systèmes monitorés"
              />
              <KpiCard
                label="Score Moyen"
                value={avgComposite}
                sub="gap composite global"
                accent={avgComposite >= 60 ? "text-red-400" : avgComposite >= 40 ? "text-orange-400" : "text-emerald-400"}
              />
              <KpiCard
                label="Alertes Critiques"
                value={criticalAlerts}
                sub="intervention urgente"
                accent="text-red-400"
              />
              <KpiCard
                label="Systèmes Résilients"
                value={resilientSystems}
                sub="faible ou modéré"
                accent="text-emerald-400"
              />
              <KpiCard
                label="Indice Préparation"
                value={`${avgPandemicIndex}/10`}
                sub="index pandémique moyen"
                accent={avgPandemicIndex >= 6 ? "text-red-400" : avgPandemicIndex >= 4 ? "text-orange-400" : "text-indigo-400"}
              />
              <KpiCard
                label="Confiance Données"
                value={`${confidenceScore}%`}
                sub="OMS · GHS Index · JHU"
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
                    value={avgComposite}
                    max={100}
                    label="Score Composite"
                    color="#f87171"
                  />
                  <GaugeRing
                    value={confidenceScore}
                    max={100}
                    label="Confiance"
                    color="#818cf8"
                  />
                  <GaugeRing
                    value={(criticalAlerts / Math.max(1, totalEntities)) * 100}
                    max={100}
                    label="Taux Critique"
                    color="#fb923c"
                  />
                  <GaugeRing
                    value={avgPandemicIndex * 10}
                    max={100}
                    label="Indice × 10"
                    color="#fbbf24"
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
                    count={riskDist.critique ?? 0}
                    total={totalEntities}
                    color="#f87171"
                  />
                  <DistBar
                    label="Élevé"
                    count={riskDist["élevé"] ?? 0}
                    total={totalEntities}
                    color="#fb923c"
                  />
                  <DistBar
                    label="Modéré"
                    count={riskDist["modéré"] ?? 0}
                    total={totalEntities}
                    color="#fbbf24"
                  />
                  <DistBar
                    label="Faible"
                    count={riskDist.faible ?? 0}
                    total={totalEntities}
                    color="#34d399"
                  />
                </div>

                <div className="mt-5 pt-4 border-t border-white/8 grid grid-cols-2 gap-3">
                  <div className="bg-white/4 rounded-lg p-3">
                    <p className="text-[11px] text-gray-500">Sources de données</p>
                    <p className="text-sm font-bold text-white mt-0.5">
                      {(data.data_sources ?? []).join(" · ")}
                    </p>
                  </div>
                  <div className="bg-white/4 rounded-lg p-3">
                    <p className="text-[11px] text-gray-500">Indice Pandémique Moyen</p>
                    <p className="text-lg font-bold text-indigo-400 mt-0.5">
                      {avgPandemicIndex}/10
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
                      <span className="ml-1.5 text-xs opacity-70">{riskDist.critique ?? 0}</span>
                    )}
                    {opt.key === "élevé" && (
                      <span className="ml-1.5 text-xs opacity-70">{riskDist["élevé"] ?? 0}</span>
                    )}
                    {opt.key === "modéré" && (
                      <span className="ml-1.5 text-xs opacity-70">{riskDist["modéré"] ?? 0}</span>
                    )}
                    {opt.key === "faible" && (
                      <span className="ml-1.5 text-xs opacity-70">{riskDist.faible ?? 0}</span>
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
                  Aucune entité dans ce niveau de risque
                </div>
              )}
            </div>

            {/* ── Alert strip for critical systems ── */}
            {criticalAlerts > 0 && (
              <div className="bg-red-500/8 border border-red-500/20 rounded-xl px-5 py-4 flex items-start gap-3">
                <div className="w-2 h-2 rounded-full bg-red-500 mt-1.5 shrink-0 animate-pulse" />
                <div>
                  <p className="text-sm font-medium text-red-400">
                    {criticalAlerts} système{criticalAlerts > 1 ? "s" : ""} en situation critique — niveau ROUGE
                  </p>
                  <p className="text-xs text-red-400/70 mt-0.5">
                    Entités les plus à risque :{" "}
                    <span className="font-medium">
                      {(data.top_risk_entities ?? []).slice(0, 2).join(", ")}
                    </span>
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
