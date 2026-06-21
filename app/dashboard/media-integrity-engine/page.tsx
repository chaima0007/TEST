"use client";

import { useEffect, useState, useMemo } from "react";

// ── Types ────────────────────────────────────────────────────────────────────

interface MediaIntegrityEntity {
  id: string;
  name: string;
  country: string;
  sector: string;
  disinformation_spread_score: number;
  source_credibility_gap_score: number;
  editorial_independence_score: number;
  regulatory_compliance_score: number;
  composite_score: number;
  risk_level: string;
  primary_pattern: string;
  key_signals: string[];
  estimated_media_index: number;
  last_updated: string;
  alert_level: string;
}

interface MediaIntegritySummary {
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
  entities: MediaIntegrityEntity[];
  avg_estimated_media_index: number;
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
  entity: MediaIntegrityEntity;
  onClick: (e: MediaIntegrityEntity) => void;
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
          <p className="text-sm font-bold text-white">{entity.disinformation_spread_score}%</p>
          <p className="text-[10px] text-gray-500">Désinformation</p>
        </div>
        <div className="bg-white/4 rounded-lg p-2 text-center">
          <p className="text-sm font-bold text-white">{entity.source_credibility_gap_score}%</p>
          <p className="text-[10px] text-gray-500">Crédibilité</p>
        </div>
        <div className="bg-white/4 rounded-lg p-2 text-center">
          <p className="text-sm font-bold text-white">{entity.editorial_independence_score}%</p>
          <p className="text-[10px] text-gray-500">Indépendance</p>
        </div>
      </div>

      <div className="flex items-center justify-between text-xs">
        <span className="text-gray-400">
          Score composite:{" "}
          <span className={`font-bold ${cfg.color}`}>{entity.composite_score}</span>
        </span>
        <span className={`font-mono text-[10px] font-semibold ${cfg.color}`}>{entity.alert_level}</span>
      </div>
    </button>
  );
}

// ── Detail Modal ──────────────────────────────────────────────────────────────

const MEDIA_PATTERNS = [
  {
    name: "Réseau de Désinformation Organisé",
    severity_fr: "critique",
    action_fr: "Démantèlement des réseaux coordonnés et coopération internationale immédiate.",
    signal_fr: "disinformation_spread > 85 et source_credibility_gap > 80",
    test: (e: MediaIntegrityEntity) => e.disinformation_spread_score > 85 && e.source_credibility_gap_score > 80,
  },
  {
    name: "Capture Éditoriale Systémique",
    severity_fr: "critique",
    action_fr: "Audit indépendant et rétablissement urgent de la charte éditoriale.",
    signal_fr: "editorial_independence > 80 et source_credibility_gap > 75",
    test: (e: MediaIntegrityEntity) => e.editorial_independence_score > 80 && e.source_credibility_gap_score > 75,
  },
  {
    name: "Propagande Institutionnelle",
    severity_fr: "élevé",
    action_fr: "Mécanismes de fact-checking renforcés et pluralisme médiatique.",
    signal_fr: "regulatory_compliance > 70 et editorial_independence > 65",
    test: (e: MediaIntegrityEntity) => e.regulatory_compliance_score > 70 && e.editorial_independence_score > 65,
  },
  {
    name: "Déficit de Vérification des Sources",
    severity_fr: "élevé",
    action_fr: "Formation des journalistes et partenariat avec agences de vérification.",
    signal_fr: "source_credibility_gap > 65 et disinformation_spread > 60",
    test: (e: MediaIntegrityEntity) => e.source_credibility_gap_score > 65 && e.disinformation_spread_score > 60,
  },
  {
    name: "Polarisation Médiatique Progressive",
    severity_fr: "modéré",
    action_fr: "Programmes d'éducation aux médias et promotion du pluralisme.",
    signal_fr: "disinformation_spread > 40 et editorial_independence > 35",
    test: (e: MediaIntegrityEntity) => e.disinformation_spread_score > 40 && e.editorial_independence_score > 35,
  },
];

const SEVERITY_STYLE: Record<string, string> = {
  critique: "text-red-400 bg-red-500/10 border-red-500/25",
  "élevé": "text-orange-400 bg-orange-500/10 border-orange-500/25",
  "modéré": "text-amber-400 bg-amber-500/10 border-amber-500/25",
};

function DetailModal({
  entity,
  onClose,
}: {
  entity: MediaIntegrityEntity;
  onClose: () => void;
}) {
  const [tab, setTab] = useState<"scores" | "signaux" | "actions">("scores");
  const cfg = RISK_CONFIG[entity.risk_level] ?? RISK_CONFIG.faible;
  const triggered = MEDIA_PATTERNS.filter((p) => p.test(entity));

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
                  { label: "Désinformation", value: `${entity.disinformation_spread_score}%` },
                  { label: "Crédibilité des Sources", value: `${entity.source_credibility_gap_score}%` },
                  { label: "Indépendance Éditoriale", value: `${entity.editorial_independence_score}%` },
                  { label: "Conformité Réglementaire", value: `${entity.regulatory_compliance_score}%` },
                  { label: "Indice Intégrité", value: `${entity.estimated_media_index}/10` },
                  { label: "Niveau d'Alerte", value: entity.alert_level },
                  { label: "Pays", value: entity.country },
                  { label: "Secteur", value: entity.sector },
                  { label: "Dernière mise à jour", value: entity.last_updated },
                  { label: "Patron Principal", value: entity.primary_pattern },
                ].map(({ label, value }) => (
                  <div key={label} className="bg-white/4 rounded-lg p-3">
                    <p className="text-[11px] text-gray-500 mb-0.5">{label}</p>
                    <p className="text-sm font-semibold text-white">{value}</p>
                  </div>
                ))}
              </div>
              <div className="bg-white/4 rounded-lg p-4">
                <div className="flex justify-between items-center mb-2">
                  <span className="text-sm text-gray-300">Score Composite d&apos;Intégrité</span>
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
                  Formule : désinformation×0.30 + crédibilité×0.25 + indépendance×0.25 + conformité×0.20
                </p>
              </div>
            </div>
          )}

          {/* ── TAB: Signaux ── */}
          {tab === "signaux" && (
            <div className="space-y-3">
              {triggered.length === 0 ? (
                <div className="text-center py-8 text-gray-400 text-sm">
                  Aucun signal d&apos;alerte détecté — média sain
                </div>
              ) : (
                triggered.map((p) => (
                  <div
                    key={p.name}
                    className={`rounded-xl border p-4 ${SEVERITY_STYLE[p.severity_fr] ?? ""}`}
                  >
                    <div className="flex items-center gap-2 mb-1.5">
                      <span className="font-semibold text-sm">{p.name}</span>
                      <span className="ml-auto text-[10px] font-medium uppercase tracking-wide opacity-70">
                        {p.severity_fr}
                      </span>
                    </div>
                    <p className="text-[10px] font-mono opacity-50 mt-1.5">Signal : {p.signal_fr}</p>
                  </div>
                ))
              )}

              {triggered.length === 0 && (
                <div className="mt-2 bg-emerald-500/10 border border-emerald-500/25 rounded-xl p-4">
                  <p className="text-emerald-400 text-sm font-medium">Média intègre</p>
                  <p className="text-xs text-emerald-400/70 mt-1">
                    Désinformation {entity.disinformation_spread_score}% · Crédibilité {entity.source_credibility_gap_score}% ·
                    Indépendance {entity.editorial_independence_score}%
                  </p>
                </div>
              )}

              <div className="mt-3 space-y-1.5">
                <p className="text-xs text-gray-500 font-medium mb-2">Signaux clés</p>
                {entity.key_signals.map((signal) => (
                  <div key={signal} className="bg-white/4 rounded-lg px-3 py-2">
                    <span className="text-xs font-mono text-gray-300">{signal}</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* ── TAB: Actions ── */}
          {tab === "actions" && (
            <div className="space-y-3">
              {triggered.length === 0 ? (
                <div className="bg-white/4 border border-white/10 rounded-xl p-4">
                  <p className="text-sm text-gray-300 font-medium">Plan de surveillance standard</p>
                  <p className="text-xs text-gray-400 mt-1.5 leading-relaxed">
                    Média en bonne santé — maintenir la surveillance périodique et documenter
                    les bonnes pratiques éditoriales.
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
                    <p className="text-xs text-gray-300 leading-relaxed">{p.action_fr}</p>
                  </div>
                ))
              )}

              <div className="bg-slate-800/60 border border-white/8 rounded-xl p-4">
                <p className="text-xs text-gray-400">
                  <span className="text-gray-300 font-medium">Indice d&apos;intégrité :</span>{" "}
                  {entity.estimated_media_index}/10
                </p>
                <p className="text-xs text-gray-400 mt-1">
                  <span className="text-gray-300 font-medium">Niveau d&apos;alerte :</span>{" "}
                  <span className={`font-mono font-semibold ${cfg.color}`}>{entity.alert_level}</span>
                </p>
                <p className="text-xs text-gray-400 mt-1">
                  <span className="text-gray-300 font-medium">Patron détecté :</span>{" "}
                  {entity.primary_pattern}
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

export default function MediaIntegrityEnginePage() {
  const [data, setData] = useState<MediaIntegritySummary | null>(null);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState("all");
  const [selected, setSelected] = useState<MediaIntegrityEntity | null>(null);

  useEffect(() => {
    fetch("/api/media-integrity-engine")
      .then((r) => r.json())
      .then((json) => {
        // Handle sealResponse wrapper
        const payload = json?.data ?? json;
        setData(payload as MediaIntegritySummary);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  const entities = data?.entities ?? [];

  const filtered = useMemo(
    () => (filter === "all" ? entities : entities.filter((e) => e.risk_level === filter)),
    [entities, filter]
  );

  const avgDisinfo = useMemo(
    () =>
      entities.length > 0
        ? Math.round(entities.reduce((acc, e) => acc + e.disinformation_spread_score, 0) / entities.length)
        : 0,
    [entities]
  );

  const avgCredibility = useMemo(
    () =>
      entities.length > 0
        ? Math.round(entities.reduce((acc, e) => acc + e.source_credibility_gap_score, 0) / entities.length)
        : 0,
    [entities]
  );

  const avgEditorial = useMemo(
    () =>
      entities.length > 0
        ? Math.round(entities.reduce((acc, e) => acc + e.editorial_independence_score, 0) / entities.length)
        : 0,
    [entities]
  );

  const avgCompliance = useMemo(
    () =>
      entities.length > 0
        ? Math.round(entities.reduce((acc, e) => acc + e.regulatory_compliance_score, 0) / entities.length)
        : 0,
    [entities]
  );

  const totalEntities = data?.total_entities ?? 0;
  const rd = data?.risk_distribution ?? { critique: 0, "élevé": 0, "modéré": 0, faible: 0 };
  const reliableCount = (rd["modéré"] ?? 0) + (rd["faible"] ?? 0);

  return (
    <div className="min-h-screen bg-slate-950 text-white">
      <div className="max-w-7xl mx-auto px-6 py-8 space-y-8">

        {/* ── Page header ── */}
        <div className="flex items-start justify-between gap-4">
          <div>
            <h1 className="text-2xl font-bold text-white">Intégrité Médiatique & Désinformation</h1>
            <p className="text-sm text-gray-400 mt-1">
              Moteur d&apos;intelligence Swarm — surveillance de l&apos;intégrité médiatique et détection de la désinformation
            </p>
          </div>
          <span className="text-xs text-gray-500 bg-white/5 border border-white/10 rounded-lg px-3 py-1.5">
            {totalEntities} entités analysées
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
                value={data.total_entities}
                sub="médias surveillés"
              />
              <KpiCard
                label="Score Composite Moyen"
                value={`${data.avg_composite}`}
                sub="indice d'intégrité agrégé"
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
                label="Alertes Critiques"
                value={data.critical_alerts}
                sub="intervention requise"
                accent="text-red-400"
              />
              <KpiCard
                label="Médias Fiables"
                value={reliableCount}
                sub="modéré ou faible risque"
                accent="text-emerald-400"
              />
              <KpiCard
                label="Indice Intégrité"
                value={`${data.avg_estimated_media_index}/10`}
                sub="indice médiatique moyen"
                accent="text-indigo-400"
              />
              <KpiCard
                label="Sources Données"
                value={data.data_sources.length}
                sub={data.data_sources.join(", ")}
              />
            </div>

            {/* ── Gauges + Distribution ── */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">

              {/* Gauges */}
              <div className="bg-white/4 border border-white/10 rounded-xl p-6">
                <h2 className="text-sm font-semibold text-gray-300 mb-6">Indicateurs Clés (Moyennes)</h2>
                <div className="grid grid-cols-4 gap-4">
                  <GaugeRing
                    value={avgDisinfo}
                    max={100}
                    label="Désinformation"
                    color="#f87171"
                  />
                  <GaugeRing
                    value={avgCredibility}
                    max={100}
                    label="Crédibilité"
                    color="#fb923c"
                  />
                  <GaugeRing
                    value={avgEditorial}
                    max={100}
                    label="Indépendance"
                    color="#fbbf24"
                  />
                  <GaugeRing
                    value={avgCompliance}
                    max={100}
                    label="Conformité"
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
                    count={rd["critique"] ?? 0}
                    total={data.total_entities}
                    color="#f87171"
                  />
                  <DistBar
                    label="Élevé"
                    count={rd["élevé"] ?? 0}
                    total={data.total_entities}
                    color="#fb923c"
                  />
                  <DistBar
                    label="Modéré"
                    count={rd["modéré"] ?? 0}
                    total={data.total_entities}
                    color="#fbbf24"
                  />
                  <DistBar
                    label="Faible"
                    count={rd["faible"] ?? 0}
                    total={data.total_entities}
                    color="#34d399"
                  />
                </div>

                <div className="mt-5 pt-4 border-t border-white/8 grid grid-cols-2 gap-3">
                  <div className="bg-white/4 rounded-lg p-3">
                    <p className="text-[11px] text-gray-500">Confiance du moteur</p>
                    <p className="text-lg font-bold text-white mt-0.5">{data.confidence_score}%</p>
                  </div>
                  <div className="bg-white/4 rounded-lg p-3">
                    <p className="text-[11px] text-gray-500">Indice Médiatique Moyen</p>
                    <p className="text-lg font-bold text-indigo-400 mt-0.5">
                      {data.avg_estimated_media_index}/10
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
                const count =
                  opt.key === "all"
                    ? data.total_entities
                    : rd[opt.key] ?? 0;
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
                <EntityCard key={entity.id} entity={entity} onClick={setSelected} />
              ))}
              {filtered.length === 0 && (
                <div className="col-span-full text-center py-12 text-gray-400 text-sm">
                  Aucune entité dans ce niveau de risque
                </div>
              )}
            </div>

            {/* ── Alert strip for critical entities ── */}
            {data.critical_alerts > 0 && (
              <div className="bg-red-500/8 border border-red-500/20 rounded-xl px-5 py-4 flex items-start gap-3">
                <div className="w-2 h-2 rounded-full bg-red-500 mt-1.5 shrink-0 animate-pulse" />
                <div>
                  <p className="text-sm font-medium text-red-400">
                    {data.critical_alerts} entité{data.critical_alerts > 1 ? "s" : ""} en situation critique
                  </p>
                  <p className="text-xs text-red-400/70 mt-0.5">
                    Médias les plus à risque :{" "}
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
