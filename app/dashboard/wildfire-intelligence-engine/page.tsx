"use client";
import { useEffect, useState } from "react";

// ── Wildfire Intelligence Engine Dashboard
// Caelum Partners — Chaima Mhadbi, Fondatrice, Bruxelles
// Domain: wildfire | Theme: orange/red (fire danger)

// ── Types ──────────────────────────────────────────────────────────────────────

type RiskLevel = "critique" | "élevé" | "modéré" | "faible";

interface WildfireEntity {
  entity_id: string;
  name: string;
  country: string;
  sector: string;
  composite_score: number;
  spread_score: number;
  prevention_score: number;
  response_score: number;
  impact_score: number;
  risk_level: RiskLevel;
  primary_pattern: string;
  key_signals: string[];
  estimated_wildfire_index: number;
  action_fr: string;
  last_updated: string;
}

interface WildfireSummary {
  total_entities: number;
  avg_composite: number;
  risk_distribution: Record<string, number>;
  pattern_distribution: Record<string, number>;
  top_risk_entities: WildfireEntity[];
  critical_alerts: Array<{
    entity_id: string;
    name: string;
    composite_score: number;
    primary_pattern: string;
    alert: string;
  }>;
  last_analysis: string;
  engine_version: string;
  domain: string;
  confidence_score: number;
  data_sources: string[];
  entities: WildfireEntity[];
  avg_estimated_wildfire_index: number;
}

interface ApiResponse extends WildfireSummary {
  digital_seal?: unknown;
}

// ── Risk metadata ─────────────────────────────────────────────────────────────

const RISK_META: Record<RiskLevel, { label: string; color: string; ring: string; badge: string }> = {
  critique: {
    label: "Critique",
    color: "text-red-400",
    ring: "#ef4444",
    badge: "bg-red-900/50 text-red-300 border border-red-700/60",
  },
  élevé: {
    label: "Élevé",
    color: "text-orange-400",
    ring: "#f97316",
    badge: "bg-orange-900/50 text-orange-300 border border-orange-700/60",
  },
  modéré: {
    label: "Modéré",
    color: "text-amber-400",
    ring: "#f59e0b",
    badge: "bg-amber-900/50 text-amber-300 border border-amber-700/60",
  },
  faible: {
    label: "Faible",
    color: "text-emerald-400",
    ring: "#10b981",
    badge: "bg-emerald-900/50 text-emerald-300 border border-emerald-700/60",
  },
};

// ── Sub-components ─────────────────────────────────────────────────────────────

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

function DistBar({
  label,
  value,
  max,
  color,
}: {
  label: string;
  value: number;
  max: number;
  color: string;
}) {
  return (
    <div className="flex items-center gap-2">
      <span className="text-xs text-stone-400 w-32 truncate">{label}</span>
      <div className="flex-1 bg-slate-800 rounded-full h-2">
        <div
          className="h-2 rounded-full transition-all"
          style={{ width: `${max > 0 ? (value / max) * 100 : 0}%`, backgroundColor: color }}
        />
      </div>
      <span className="text-xs text-stone-300 w-6 text-right">{value}</span>
    </div>
  );
}

function KpiCard({
  label,
  value,
  sub,
  color,
}: {
  label: string;
  value: string | number;
  sub?: string;
  color?: string;
}) {
  return (
    <div className="bg-slate-900 border border-orange-500/20 rounded-xl p-4 flex flex-col gap-1">
      <span className="text-xs text-stone-500 uppercase tracking-wider">{label}</span>
      <span className={`text-2xl font-bold ${color ?? "text-orange-400"}`}>{value}</span>
      {sub && <span className="text-xs text-stone-500">{sub}</span>}
    </div>
  );
}

function ScoreBar({ label, value, color }: { label: string; value: number; color: string }) {
  return (
    <div className="flex flex-col gap-1">
      <div className="flex justify-between text-xs">
        <span className="text-stone-400">{label}</span>
        <span className="text-stone-300 font-medium">{value}</span>
      </div>
      <div className="bg-slate-800 rounded-full h-2">
        <div
          className="h-2 rounded-full transition-all"
          style={{ width: `${value}%`, backgroundColor: color }}
        />
      </div>
    </div>
  );
}

// ── Detail Modal ───────────────────────────────────────────────────────────────

function DetailModal({
  entity,
  onClose,
}: {
  entity: WildfireEntity;
  onClose: () => void;
}) {
  const [tab, setTab] = useState<"scores" | "signaux" | "actions">("scores");
  const meta = RISK_META[entity.risk_level];

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm p-4"
      onClick={onClose}
    >
      <div
        className="bg-slate-900 border border-orange-500/30 rounded-2xl w-full max-w-lg shadow-2xl shadow-orange-900/20"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="p-5 border-b border-slate-800 flex items-start justify-between gap-3">
          <div className="flex flex-col gap-1">
            <div className="flex items-center gap-2">
              <span className="text-xs text-orange-500 font-mono">{entity.entity_id}</span>
              <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${meta.badge}`}>
                {meta.label}
              </span>
            </div>
            <h2 className="text-white font-semibold text-lg leading-tight">{entity.name}</h2>
            <p className="text-stone-400 text-sm">
              {entity.country} — {entity.sector}
            </p>
          </div>
          <button
            onClick={onClose}
            className="text-stone-500 hover:text-stone-300 transition-colors text-xl leading-none mt-0.5"
            aria-label="Fermer"
          >
            ✕
          </button>
        </div>

        {/* Tabs */}
        <div className="flex border-b border-slate-800">
          {(["scores", "signaux", "actions"] as const).map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`flex-1 py-2.5 text-xs font-medium capitalize transition-colors ${
                tab === t
                  ? "text-orange-400 border-b-2 border-orange-500"
                  : "text-stone-500 hover:text-stone-300"
              }`}
            >
              {t === "scores" ? "Scores" : t === "signaux" ? "Signaux" : "Actions"}
            </button>
          ))}
        </div>

        {/* Tab content */}
        <div className="p-5 flex flex-col gap-4">
          {tab === "scores" && (
            <>
              <div className="flex items-center justify-between mb-1">
                <span className="text-xs text-stone-500 uppercase tracking-wider">Score composite</span>
                <span className="text-orange-400 font-bold text-lg">
                  {entity.composite_score}
                </span>
              </div>
              <ScoreBar label="Propagation" value={entity.spread_score} color="#f97316" />
              <ScoreBar label="Prévention" value={entity.prevention_score} color="#ef4444" />
              <ScoreBar label="Réponse" value={entity.response_score} color="#fb923c" />
              <ScoreBar label="Impact" value={entity.impact_score} color="#fbbf24" />
              <div className="flex items-center justify-between pt-2 border-t border-slate-800">
                <span className="text-xs text-stone-500">Index Incendie</span>
                <span className="text-amber-400 font-bold">
                  {entity.estimated_wildfire_index} / 10
                </span>
              </div>
            </>
          )}

          {tab === "signaux" && (
            <ul className="flex flex-col gap-3">
              {entity.key_signals.map((signal, i) => (
                <li
                  key={i}
                  className="flex gap-3 items-start bg-orange-500/5 border border-orange-500/20 rounded-lg p-3"
                >
                  <span className="text-orange-500 text-sm mt-0.5 shrink-0">⚠</span>
                  <p className="text-stone-300 text-sm leading-relaxed">{signal}</p>
                </li>
              ))}
            </ul>
          )}

          {tab === "actions" && (
            <div className="flex flex-col gap-4">
              <div className="bg-red-500/5 border border-red-500/20 rounded-lg p-4">
                <div className="flex items-center gap-2 mb-2">
                  <span className="text-red-400 text-sm">🔥</span>
                  <span className="text-xs text-red-400 font-medium uppercase tracking-wider">
                    Schéma détecté
                  </span>
                </div>
                <p className="text-orange-300 font-semibold text-sm">{entity.primary_pattern}</p>
              </div>
              <div className="bg-amber-500/5 border border-amber-500/20 rounded-lg p-4">
                <div className="flex items-center gap-2 mb-2">
                  <span className="text-amber-400 text-sm">⚡</span>
                  <span className="text-xs text-amber-400 font-medium uppercase tracking-wider">
                    Action recommandée
                  </span>
                </div>
                <p className="text-stone-300 text-sm leading-relaxed">{entity.action_fr}</p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

// ── Main Dashboard ─────────────────────────────────────────────────────────────

export default function WildfireIntelligenceDashboard() {
  const [data, setData] = useState<ApiResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedRisk, setSelectedRisk] = useState<RiskLevel | "all">("all");
  const [selectedCountry, setSelectedCountry] = useState<string>("all");
  const [selectedEntity, setSelectedEntity] = useState<WildfireEntity | null>(null);

  useEffect(() => {
    fetch("/api/wildfire-intelligence-engine")
      .then((r) => {
        if (!r.ok) throw new Error(`HTTP ${r.status}`);
        return r.json();
      })
      .then((d: ApiResponse) => {
        setData(d);
        setLoading(false);
      })
      .catch((e: unknown) => {
        setError(e instanceof Error ? e.message : "Erreur inconnue");
        setLoading(false);
      });
  }, []);

  // ── Loading ──────────────────────────────────────────────────────────────────

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center">
        <div className="flex flex-col items-center gap-4">
          <div className="w-12 h-12 border-4 border-orange-500/30 border-t-orange-500 rounded-full animate-spin" />
          <p className="text-stone-400 text-sm">Analyse des risques d'incendie en cours…</p>
        </div>
      </div>
    );
  }

  // ── Error ────────────────────────────────────────────────────────────────────

  if (error || !data) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center p-6">
        <div className="bg-red-900/20 border border-red-500/40 rounded-xl p-6 max-w-sm text-center">
          <p className="text-red-400 font-semibold mb-1">Erreur de chargement</p>
          <p className="text-stone-400 text-sm">{error ?? "Données indisponibles"}</p>
        </div>
      </div>
    );
  }

  // ── Computed values ──────────────────────────────────────────────────────────

  const entities = data.entities ?? [];

  const avgSpread =
    entities.length > 0
      ? Math.round(entities.reduce((s, e) => s + e.spread_score, 0) / entities.length)
      : 0;
  const avgPrevention =
    entities.length > 0
      ? Math.round(entities.reduce((s, e) => s + e.prevention_score, 0) / entities.length)
      : 0;
  const avgResponse =
    entities.length > 0
      ? Math.round(entities.reduce((s, e) => s + e.response_score, 0) / entities.length)
      : 0;
  const avgImpact =
    entities.length > 0
      ? Math.round(entities.reduce((s, e) => s + e.impact_score, 0) / entities.length)
      : 0;

  const countries = Array.from(new Set(entities.map((e) => e.country))).sort();

  const filtered = entities.filter((e) => {
    if (selectedRisk !== "all" && e.risk_level !== selectedRisk) return false;
    if (selectedCountry !== "all" && e.country !== selectedCountry) return false;
    return true;
  });

  const riskDist = data.risk_distribution ?? {};
  const patternDist = data.pattern_distribution ?? {};
  const maxRisk = Math.max(...Object.values(riskDist), 1);
  const maxPattern = Math.max(...Object.values(patternDist), 1);

  const RISK_COLORS: Record<string, string> = {
    critique: "#ef4444",
    élevé: "#f97316",
    modéré: "#f59e0b",
    faible: "#10b981",
  };

  const PATTERN_COLORS: Record<string, string> = {
    "Propagation Catastrophique": "#ef4444",
    "Déficit Prévention Critique": "#dc2626",
    "Effondrement Réponse d'Urgence": "#f97316",
    "Impact Écosystème Majeur": "#f59e0b",
    "Risque Saisonnier Émergent": "#10b981",
  };

  // ── Render ───────────────────────────────────────────────────────────────────

  return (
    <div className="min-h-screen bg-slate-950 text-white">
      {/* Header */}
      <div className="border-b border-orange-500/20 bg-slate-950/80 sticky top-0 z-10 backdrop-blur-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 py-4 flex items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-lg bg-orange-500/20 border border-orange-500/40 flex items-center justify-center text-lg">
              🔥
            </div>
            <div>
              <h1 className="text-white font-bold text-lg leading-tight">
                Wildfire Intelligence Engine
              </h1>
              <p className="text-stone-500 text-xs">
                Caelum Partners — {data.total_entities} entités surveillées
              </p>
            </div>
          </div>
          <div className="flex items-center gap-3 shrink-0">
            <span className="hidden sm:block text-xs text-stone-500">
              Confiance:{" "}
              <span className="text-orange-400 font-medium">
                {Math.round((data.confidence_score ?? 0) * 100)}%
              </span>
            </span>
            <span className="text-xs text-stone-600 font-mono">v{data.engine_version}</span>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 py-6 flex flex-col gap-6">

        {/* KPI Cards */}
        <section className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
          <KpiCard label="Total Entités" value={data.total_entities} sub="zones surveillées" />
          <KpiCard
            label="Critique"
            value={riskDist["critique"] ?? 0}
            sub="zones en alerte"
            color="text-red-400"
          />
          <KpiCard
            label="Élevé"
            value={riskDist["élevé"] ?? 0}
            sub="risque élevé"
            color="text-orange-400"
          />
          <KpiCard
            label="Composite Moyen"
            value={data.avg_composite.toFixed(1)}
            sub="score /100"
            color="text-amber-400"
          />
          <KpiCard
            label="Index Incendie"
            value={`${data.avg_estimated_wildfire_index} /10`}
            sub="indice global"
            color="text-orange-400"
          />
          <KpiCard
            label="Propagation Moy."
            value={avgSpread}
            sub="spread /100"
            color="text-red-400"
          />
        </section>

        {/* Gauges */}
        <section className="bg-slate-900 border border-orange-500/20 rounded-xl p-5">
          <h2 className="text-sm font-semibold text-stone-300 mb-4 uppercase tracking-wider">
            Scores Moyens par Dimension
          </h2>
          <div className="flex flex-wrap justify-around gap-4">
            <GaugeRing value={avgSpread} label="Propagation" color="#ef4444" />
            <GaugeRing value={avgPrevention} label="Prévention" color="#f97316" />
            <GaugeRing value={avgResponse} label="Réponse" color="#fb923c" />
            <GaugeRing value={avgImpact} label="Impact" color="#fbbf24" />
          </div>
        </section>

        {/* Distributions */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {/* Risk distribution */}
          <section className="bg-slate-900 border border-orange-500/20 rounded-xl p-5">
            <h2 className="text-sm font-semibold text-stone-300 mb-4 uppercase tracking-wider">
              Distribution des Risques
            </h2>
            <div className="flex flex-col gap-3">
              {Object.entries(riskDist).map(([label, value]) => (
                <DistBar
                  key={label}
                  label={label.charAt(0).toUpperCase() + label.slice(1)}
                  value={value}
                  max={maxRisk}
                  color={RISK_COLORS[label] ?? "#6b7280"}
                />
              ))}
            </div>
          </section>

          {/* Pattern distribution */}
          <section className="bg-slate-900 border border-orange-500/20 rounded-xl p-5">
            <h2 className="text-sm font-semibold text-stone-300 mb-4 uppercase tracking-wider">
              Distribution des Schémas
            </h2>
            <div className="flex flex-col gap-3">
              {Object.entries(patternDist).map(([label, value]) => (
                <DistBar
                  key={label}
                  label={label}
                  value={value}
                  max={maxPattern}
                  color={PATTERN_COLORS[label] ?? "#f97316"}
                />
              ))}
            </div>
          </section>
        </div>

        {/* Filters */}
        <section className="flex flex-wrap gap-2 items-center">
          <span className="text-xs text-stone-500 mr-1">Risque:</span>
          {(["all", "critique", "élevé", "modéré", "faible"] as const).map((r) => (
            <button
              key={r}
              onClick={() => setSelectedRisk(r)}
              className={`px-3 py-1 rounded-full text-xs font-medium transition-colors border ${
                selectedRisk === r
                  ? "bg-orange-500/20 border-orange-500/60 text-orange-300"
                  : "bg-slate-800 border-slate-700 text-stone-400 hover:text-stone-300 hover:border-slate-600"
              }`}
            >
              {r === "all" ? "Tous" : r.charAt(0).toUpperCase() + r.slice(1)}
            </button>
          ))}

          <span className="text-xs text-stone-500 ml-3 mr-1">Pays:</span>
          <button
            onClick={() => setSelectedCountry("all")}
            className={`px-3 py-1 rounded-full text-xs font-medium transition-colors border ${
              selectedCountry === "all"
                ? "bg-orange-500/20 border-orange-500/60 text-orange-300"
                : "bg-slate-800 border-slate-700 text-stone-400 hover:text-stone-300"
            }`}
          >
            Tous
          </button>
          {countries.map((c) => (
            <button
              key={c}
              onClick={() => setSelectedCountry(c)}
              className={`px-3 py-1 rounded-full text-xs font-medium transition-colors border ${
                selectedCountry === c
                  ? "bg-orange-500/20 border-orange-500/60 text-orange-300"
                  : "bg-slate-800 border-slate-700 text-stone-400 hover:text-stone-300"
              }`}
            >
              {c}
            </button>
          ))}
        </section>

        {/* Entity Grid */}
        <section>
          <div className="flex items-center justify-between mb-3">
            <h2 className="text-sm font-semibold text-stone-300 uppercase tracking-wider">
              Entités — {filtered.length} résultat{filtered.length !== 1 ? "s" : ""}
            </h2>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {filtered.map((entity) => {
              const meta = RISK_META[entity.risk_level];
              return (
                <button
                  key={entity.entity_id}
                  onClick={() => setSelectedEntity(entity)}
                  className="bg-slate-900 border border-orange-500/20 rounded-xl p-4 text-left hover:border-orange-500/50 hover:bg-slate-800/80 transition-all group flex flex-col gap-3"
                >
                  {/* Top row */}
                  <div className="flex items-start justify-between gap-2">
                    <span className="text-xs text-orange-500/70 font-mono">{entity.entity_id}</span>
                    <span className={`text-xs px-2 py-0.5 rounded-full font-medium shrink-0 ${meta.badge}`}>
                      {meta.label}
                    </span>
                  </div>

                  {/* Name */}
                  <div>
                    <p className="text-sm font-semibold text-white leading-snug group-hover:text-orange-200 transition-colors">
                      {entity.name}
                    </p>
                    <p className="text-xs text-stone-500 mt-0.5">
                      {entity.country} · {entity.sector}
                    </p>
                  </div>

                  {/* Scores */}
                  <div className="flex flex-col gap-1.5">
                    <div className="flex justify-between text-xs">
                      <span className="text-stone-500">Composite</span>
                      <span className={`font-bold ${meta.color}`}>{entity.composite_score}</span>
                    </div>
                    <div className="bg-slate-800 rounded-full h-1.5">
                      <div
                        className="h-1.5 rounded-full"
                        style={{
                          width: `${entity.composite_score}%`,
                          backgroundColor: meta.ring,
                        }}
                      />
                    </div>
                  </div>

                  {/* Pattern & Index */}
                  <div className="flex items-center justify-between pt-1 border-t border-slate-800">
                    <span className="text-xs text-stone-500 truncate mr-2 flex-1">
                      {entity.primary_pattern}
                    </span>
                    <span className="text-xs font-medium text-amber-400 shrink-0">
                      {entity.estimated_wildfire_index}/10
                    </span>
                  </div>
                </button>
              );
            })}

            {filtered.length === 0 && (
              <div className="col-span-full text-center py-10 text-stone-500 text-sm">
                Aucune entité ne correspond aux filtres sélectionnés.
              </div>
            )}
          </div>
        </section>

        {/* Data sources footer */}
        <footer className="border-t border-slate-800 pt-4 flex flex-wrap gap-2 items-center">
          <span className="text-xs text-stone-600">Sources:</span>
          {(data.data_sources ?? []).map((src) => (
            <span
              key={src}
              className="text-xs text-stone-600 bg-slate-900 border border-slate-800 rounded px-2 py-0.5"
            >
              {src}
            </span>
          ))}
        </footer>
      </div>

      {/* Detail Modal */}
      {selectedEntity && (
        <DetailModal entity={selectedEntity} onClose={() => setSelectedEntity(null)} />
      )}
    </div>
  );
}
