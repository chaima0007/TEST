"use client";

import { useEffect, useState } from "react";

// ── Types ─────────────────────────────────────────────────────────────────────

interface Entity {
  id: string;
  name: string;
  country: string;
  sector: string;
  composite_score: number;
  deception_score: number;
  coercion_score: number;
  addiction_score: number;
  exploitation_score: number;
  risk_level: string;
  primary_pattern: string;
  key_signals: string[];
  estimated_darkpattern_index: number;
  last_updated: string;
}

interface Summary {
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
  entities: Entity[];
  avg_estimated_darkpattern_index: number;
}

interface ApiResponse {
  entities: Entity[];
  summary: Summary;
}

// ── Helpers ───────────────────────────────────────────────────────────────────

const RISK_COLORS: Record<string, string> = {
  critique: "bg-red-500/20 text-red-400 border border-red-500/30",
  élevé: "bg-orange-500/20 text-orange-400 border border-orange-500/30",
  modéré: "bg-yellow-500/20 text-yellow-400 border border-yellow-500/30",
  faible: "bg-emerald-500/20 text-emerald-400 border border-emerald-500/30",
};

const RISK_BAR_COLORS: Record<string, string> = {
  critique: "bg-red-500",
  élevé: "bg-orange-500",
  modéré: "bg-yellow-500",
  faible: "bg-emerald-500",
};

const PATTERN_ACTIONS: Record<string, string> = {
  "Déception Systématique Interface": "Injonction réglementaire immédiate et retrait du marché sous 48h.",
  "Coercition Consentement Numérique": "Audit DSA/RGPD d'urgence et suspension des flux consentement.",
  "Ingénierie Addiction Comportementale": "Désactivation fonctionnalités addictives et audit éthique indépendant.",
  "Exploitation Psychologique Ciblée": "Révision algorithme de recommandation et rapport DPC trimestriel.",
  "Nudge Opaque Décisionnel": "Transparence renforcée des algorithmes et étiquetage dark patterns.",
};

function scoreToColor(score: number): string {
  if (score >= 60) return "#ef4444";
  if (score >= 40) return "#f97316";
  if (score >= 20) return "#eab308";
  return "#10b981";
}

// ── GaugeRing ─────────────────────────────────────────────────────────────────

function GaugeRing({ label, value, max = 100 }: { label: string; value: number; max?: number }) {
  const pct = Math.min(value / max, 1);
  const r = 36;
  const cx = 44;
  const cy = 44;
  const circumference = 2 * Math.PI * r;
  const dash = pct * circumference;
  const color = scoreToColor(value);

  return (
    <div className="flex flex-col items-center gap-2 p-4 bg-slate-900 rounded-xl border border-slate-700/50">
      <svg width={88} height={88} viewBox="0 0 88 88">
        <circle cx={cx} cy={cy} r={r} fill="none" stroke="#1e293b" strokeWidth={8} />
        <circle
          cx={cx}
          cy={cy}
          r={r}
          fill="none"
          stroke={color}
          strokeWidth={8}
          strokeDasharray={`${dash} ${circumference - dash}`}
          strokeLinecap="round"
          transform={`rotate(-90 ${cx} ${cy})`}
          style={{ transition: "stroke-dasharray 0.6s ease" }}
        />
        <text x={cx} y={cy + 5} textAnchor="middle" fill={color} fontSize={14} fontWeight="bold">
          {value.toFixed(1)}
        </text>
      </svg>
      <span className="text-slate-400 text-xs text-center leading-tight">{label}</span>
    </div>
  );
}

// ── DistBar ───────────────────────────────────────────────────────────────────

function DistBar({
  title,
  data,
  colorMap,
}: {
  title: string;
  data: Record<string, number>;
  colorMap?: Record<string, string>;
}) {
  const total = Object.values(data).reduce((a, b) => a + b, 0) || 1;
  const defaultColors = ["bg-violet-500", "bg-blue-500", "bg-cyan-500", "bg-teal-500", "bg-indigo-500"];

  return (
    <div className="bg-slate-900 rounded-xl border border-slate-700/50 p-4">
      <h3 className="text-slate-300 text-sm font-semibold mb-3">{title}</h3>
      <div className="space-y-2">
        {Object.entries(data).map(([key, count], i) => {
          const pct = (count / total) * 100;
          const barColor = colorMap?.[key] ?? defaultColors[i % defaultColors.length];
          return (
            <div key={key}>
              <div className="flex justify-between text-xs mb-0.5">
                <span className="text-slate-400 truncate max-w-[160px]">{key}</span>
                <span className="text-slate-300 ml-2">{count}</span>
              </div>
              <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
                <div
                  className={`h-full rounded-full ${barColor}`}
                  style={{ width: `${pct}%`, transition: "width 0.5s ease" }}
                />
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

// ── KPI Card ─────────────────────────────────────────────────────────────────

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
    <div className="bg-slate-900 rounded-xl border border-slate-700/50 p-5 flex flex-col gap-1">
      <span className="text-slate-500 text-xs uppercase tracking-wide">{label}</span>
      <span className={`text-2xl font-bold ${accent ?? "text-white"}`}>{value}</span>
      {sub && <span className="text-slate-500 text-xs">{sub}</span>}
    </div>
  );
}

// ── Detail Modal ──────────────────────────────────────────────────────────────

function DetailModal({ entity, onClose }: { entity: Entity; onClose: () => void }) {
  const [tab, setTab] = useState<"scores" | "signaux" | "actions">("scores");

  const subScores = [
    { label: "Déception Interface", value: entity.deception_score, weight: "0.30" },
    { label: "Coercition", value: entity.coercion_score, weight: "0.25" },
    { label: "Addiction", value: entity.addiction_score, weight: "0.25" },
    { label: "Exploitation", value: entity.exploitation_score, weight: "0.20" },
  ];

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm"
      onClick={onClose}
    >
      <div
        className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-lg mx-4 overflow-hidden shadow-2xl"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="p-5 border-b border-slate-700/50">
          <div className="flex items-start justify-between gap-3">
            <div>
              <h2 className="text-white font-bold text-lg">{entity.name}</h2>
              <p className="text-slate-400 text-sm">
                {entity.country} · {entity.sector}
              </p>
            </div>
            <div className="flex items-center gap-2">
              <span
                className={`text-xs px-2 py-1 rounded-full font-medium ${RISK_COLORS[entity.risk_level] ?? "text-slate-400"}`}
              >
                {entity.risk_level}
              </span>
              <button
                onClick={onClose}
                className="text-slate-500 hover:text-white transition-colors text-xl leading-none"
              >
                &times;
              </button>
            </div>
          </div>
          <div className="mt-3 flex items-center gap-4 text-sm">
            <span className="text-slate-500">Score composite</span>
            <span className="text-white font-bold">{entity.composite_score.toFixed(2)}</span>
            <span className="text-slate-500">Index</span>
            <span className="text-violet-400 font-bold">{entity.estimated_darkpattern_index}</span>
          </div>
        </div>

        {/* Tabs */}
        <div className="flex border-b border-slate-700/50">
          {(["scores", "signaux", "actions"] as const).map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`flex-1 py-2.5 text-sm font-medium capitalize transition-colors ${
                tab === t
                  ? "text-violet-400 border-b-2 border-violet-400"
                  : "text-slate-500 hover:text-slate-300"
              }`}
            >
              {t}
            </button>
          ))}
        </div>

        {/* Tab content */}
        <div className="p-5">
          {tab === "scores" && (
            <div className="space-y-4">
              {subScores.map((s) => (
                <div key={s.label}>
                  <div className="flex justify-between text-sm mb-1">
                    <span className="text-slate-300">{s.label}</span>
                    <div className="flex items-center gap-2">
                      <span className="text-slate-500 text-xs">×{s.weight}</span>
                      <span
                        className="font-bold"
                        style={{ color: scoreToColor(s.value) }}
                      >
                        {s.value.toFixed(1)}
                      </span>
                    </div>
                  </div>
                  <div className="h-2 bg-slate-800 rounded-full overflow-hidden">
                    <div
                      className="h-full rounded-full transition-all duration-500"
                      style={{
                        width: `${s.value}%`,
                        backgroundColor: scoreToColor(s.value),
                      }}
                    />
                  </div>
                </div>
              ))}
              <div className="mt-4 pt-4 border-t border-slate-700/50">
                <div className="flex justify-between text-sm">
                  <span className="text-slate-400">Score composite final</span>
                  <span
                    className="font-bold text-base"
                    style={{ color: scoreToColor(entity.composite_score) }}
                  >
                    {entity.composite_score.toFixed(2)} / 100
                  </span>
                </div>
              </div>
            </div>
          )}

          {tab === "signaux" && (
            <div className="space-y-3">
              <p className="text-slate-500 text-xs uppercase tracking-wide mb-2">
                Signaux détectés
              </p>
              {entity.key_signals.map((signal, i) => (
                <div
                  key={i}
                  className="flex items-start gap-3 p-3 bg-slate-800 rounded-lg border border-slate-700/50"
                >
                  <span
                    className="w-5 h-5 rounded-full flex items-center justify-center text-xs font-bold shrink-0 mt-0.5"
                    style={{
                      backgroundColor: scoreToColor(entity.composite_score) + "33",
                      color: scoreToColor(entity.composite_score),
                    }}
                  >
                    {i + 1}
                  </span>
                  <span className="text-slate-300 text-sm leading-relaxed">{signal}</span>
                </div>
              ))}
              <div className="mt-3 p-3 bg-slate-800 rounded-lg border border-slate-700/30">
                <p className="text-slate-500 text-xs uppercase mb-1">Pattern principal</p>
                <p className="text-violet-300 text-sm font-medium">{entity.primary_pattern}</p>
              </div>
            </div>
          )}

          {tab === "actions" && (
            <div className="space-y-4">
              <div className="p-4 bg-slate-800 rounded-xl border border-slate-700/50">
                <p className="text-slate-500 text-xs uppercase tracking-wide mb-2">
                  Action recommandée
                </p>
                <p className="text-white text-sm leading-relaxed font-medium">
                  {PATTERN_ACTIONS[entity.primary_pattern] || "Audit UX complémentaire requis"}
                </p>
              </div>
              <div className="p-4 bg-slate-800 rounded-xl border border-slate-700/50">
                <p className="text-slate-500 text-xs uppercase tracking-wide mb-2">
                  Pattern déclencheur
                </p>
                <p className="text-violet-400 text-sm font-medium">{entity.primary_pattern}</p>
              </div>
              <div className="p-4 bg-slate-800 rounded-xl border border-slate-700/50">
                <p className="text-slate-500 text-xs uppercase tracking-wide mb-2">
                  Niveau de risque
                </p>
                <span
                  className={`text-sm px-3 py-1 rounded-full font-medium ${RISK_COLORS[entity.risk_level] ?? ""}`}
                >
                  {entity.risk_level}
                </span>
              </div>
              <div className="p-4 bg-slate-800 rounded-xl border border-slate-700/50">
                <p className="text-slate-500 text-xs uppercase tracking-wide mb-2">
                  Dernière mise à jour
                </p>
                <p className="text-slate-300 text-sm">{entity.last_updated}</p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

// ── Main Page ─────────────────────────────────────────────────────────────────

export default function DarkPatternsEnginePage() {
  const [data, setData] = useState<ApiResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filterRisk, setFilterRisk] = useState<string>("tous");
  const [selected, setSelected] = useState<Entity | null>(null);

  useEffect(() => {
    fetch("/api/dark-patterns-engine")
      .then((r) => r.json())
      .then((json) => {
        const payload = json?.data ?? json;
        setData(payload);
        setLoading(false);
      })
      .catch((err) => {
        setError(String(err));
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center">
        <div className="text-slate-400 text-sm animate-pulse">
          Chargement Dark Patterns Intelligence...
        </div>
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center">
        <div className="text-red-400 text-sm">
          Erreur de chargement : {error ?? "données indisponibles"}
        </div>
      </div>
    );
  }

  const { entities, summary } = data;

  // Compute averages for gauge rings
  const avgDeception = entities.reduce((a, e) => a + e.deception_score, 0) / entities.length;
  const avgCoercion = entities.reduce((a, e) => a + e.coercion_score, 0) / entities.length;
  const avgAddiction = entities.reduce((a, e) => a + e.addiction_score, 0) / entities.length;
  const avgExploitation = entities.reduce((a, e) => a + e.exploitation_score, 0) / entities.length;

  // Sector distribution
  const sectorDist: Record<string, number> = {};
  entities.forEach((e) => {
    sectorDist[e.sector] = (sectorDist[e.sector] ?? 0) + 1;
  });

  // Country distribution
  const countryDist: Record<string, number> = {};
  entities.forEach((e) => {
    countryDist[e.country] = (countryDist[e.country] ?? 0) + 1;
  });

  const criticalCount =
    typeof summary.critical_alerts === "number"
      ? summary.critical_alerts
      : (summary.critical_alerts as string[]).length;

  // Filter
  const riskLevels = ["tous", "critique", "élevé", "modéré", "faible"];
  const filtered =
    filterRisk === "tous" ? entities : entities.filter((e) => e.risk_level === filterRisk);

  return (
    <div className="min-h-screen bg-slate-950 text-white">
      {/* Header */}
      <div className="border-b border-slate-800 px-6 py-5">
        <div className="max-w-7xl mx-auto">
          <h1 className="text-xl font-bold text-white">Dark Patterns Intelligence</h1>
          <p className="text-slate-400 text-sm mt-1">
            Surveillance des pratiques UX déceptives et violations consentement
          </p>
          <div className="flex gap-4 mt-2 text-xs text-slate-500">
            <span>Analyse: {summary.last_analysis}</span>
            <span>·</span>
            <span>Version: {summary.engine_version}</span>
            <span>·</span>
            <span>Confiance: {(summary.confidence_score * 100).toFixed(0)}%</span>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-6 py-6 space-y-6">
        {/* KPI Cards */}
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
          <KpiCard
            label="Total Entités"
            value={summary.total_entities}
            sub="plateformes analysées"
          />
          <KpiCard
            label="Alertes Critiques"
            value={criticalCount}
            sub="niveau critique"
            accent="text-red-400"
          />
          <KpiCard
            label="Score Déception Moyen"
            value={avgDeception.toFixed(1)}
            sub="sur 100"
            accent="text-orange-400"
          />
          <KpiCard
            label="Index Dark Pattern Moyen"
            value={summary.avg_estimated_darkpattern_index}
            sub="sur 10"
            accent="text-violet-400"
          />
          <KpiCard
            label="Risque Élevé"
            value={summary.risk_distribution["élevé"] ?? 0}
            sub="entités élevées"
            accent="text-yellow-400"
          />
          <KpiCard
            label="Sources Analysées"
            value={summary.data_sources.length}
            sub="flux actifs"
            accent="text-cyan-400"
          />
        </div>

        {/* Gauge Rings */}
        <div>
          <h2 className="text-slate-300 text-sm font-semibold mb-3">
            Scores Moyens par Dimension
          </h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <GaugeRing label="Déception Interface (×0.30)" value={parseFloat(avgDeception.toFixed(1))} />
            <GaugeRing label="Coercition (×0.25)" value={parseFloat(avgCoercion.toFixed(1))} />
            <GaugeRing label="Addiction (×0.25)" value={parseFloat(avgAddiction.toFixed(1))} />
            <GaugeRing label="Exploitation (×0.20)" value={parseFloat(avgExploitation.toFixed(1))} />
          </div>
        </div>

        {/* Distribution Bars */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <DistBar
            title="Distribution par Risque"
            data={summary.risk_distribution}
            colorMap={RISK_BAR_COLORS}
          />
          <DistBar title="Distribution par Pattern" data={summary.pattern_distribution} />
          <DistBar title="Distribution par Secteur" data={sectorDist} />
          <DistBar title="Distribution par Pays" data={countryDist} />
        </div>

        {/* Filter Pills */}
        <div className="flex gap-2 flex-wrap">
          {riskLevels.map((level) => (
            <button
              key={level}
              onClick={() => setFilterRisk(level)}
              className={`px-4 py-1.5 rounded-full text-sm font-medium transition-colors ${
                filterRisk === level
                  ? "bg-violet-600 text-white"
                  : "bg-slate-800 text-slate-400 hover:text-slate-200 hover:bg-slate-700"
              }`}
            >
              {level === "tous" ? "Tous" : level}
              {level !== "tous" && summary.risk_distribution[level] !== undefined && (
                <span className="ml-1.5 text-xs opacity-70">
                  ({summary.risk_distribution[level]})
                </span>
              )}
            </button>
          ))}
        </div>

        {/* Entity Cards Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          {filtered.map((entity) => (
            <button
              key={entity.id}
              onClick={() => setSelected(entity)}
              className="bg-slate-900 border border-slate-700/50 rounded-xl p-4 text-left hover:border-slate-600 hover:bg-slate-800/50 transition-all group"
            >
              {/* Header */}
              <div className="flex items-start justify-between gap-2 mb-3">
                <div className="min-w-0">
                  <p className="text-white font-semibold text-sm truncate group-hover:text-violet-300 transition-colors">
                    {entity.name}
                  </p>
                  <p className="text-slate-500 text-xs mt-0.5 truncate">
                    {entity.country} · {entity.sector}
                  </p>
                </div>
                <span
                  className={`text-xs px-2 py-0.5 rounded-full font-medium shrink-0 ${
                    RISK_COLORS[entity.risk_level] ?? "text-slate-400"
                  }`}
                >
                  {entity.risk_level}
                </span>
              </div>

              {/* Composite Score Bar */}
              <div className="mb-3">
                <div className="flex justify-between text-xs mb-1">
                  <span className="text-slate-500">Score composite</span>
                  <span
                    className="font-bold"
                    style={{ color: scoreToColor(entity.composite_score) }}
                  >
                    {entity.composite_score.toFixed(2)}
                  </span>
                </div>
                <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
                  <div
                    className="h-full rounded-full transition-all duration-500"
                    style={{
                      width: `${entity.composite_score}%`,
                      backgroundColor: scoreToColor(entity.composite_score),
                    }}
                  />
                </div>
              </div>

              {/* Pattern */}
              <p className="text-violet-400 text-xs font-medium truncate mb-2">
                {entity.primary_pattern}
              </p>

              {/* Key Signals */}
              <div className="space-y-1">
                {entity.key_signals.map((signal, i) => (
                  <p key={i} className="text-slate-500 text-xs truncate">
                    · {signal}
                  </p>
                ))}
              </div>

              {/* Index */}
              <div className="mt-3 pt-3 border-t border-slate-700/40 flex justify-between text-xs">
                <span className="text-slate-600">Index Dark Pattern</span>
                <span className="text-violet-400 font-medium">
                  {entity.estimated_darkpattern_index} / 10
                </span>
              </div>
            </button>
          ))}
        </div>

        {filtered.length === 0 && (
          <div className="text-center text-slate-600 py-12 text-sm">
            Aucune entité pour ce niveau de risque.
          </div>
        )}

        {/* Data Sources */}
        <div className="bg-slate-900 border border-slate-700/50 rounded-xl p-4">
          <h3 className="text-slate-400 text-xs uppercase tracking-wide mb-3">
            Sources de données
          </h3>
          <div className="flex flex-wrap gap-2">
            {summary.data_sources.map((src) => (
              <span
                key={src}
                className="text-xs bg-slate-800 text-slate-400 px-3 py-1 rounded-full border border-slate-700/50"
              >
                {src}
              </span>
            ))}
          </div>
        </div>
      </div>

      {/* Detail Modal */}
      {selected && (
        <DetailModal entity={selected} onClose={() => setSelected(null)} />
      )}
    </div>
  );
}
