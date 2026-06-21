"use client";
import { useEffect, useState } from "react";

// ── Types ──────────────────────────────────────────────────────────────────────

interface EntityDict {
  id: string;
  name: string;
  country: string;
  sector: string;
  composite_score: number;
  enhancement_score: number;
  consent_score: number;
  equity_score: number;
  governance_score: number;
  risk_level: string;
  primary_pattern: string;
  key_signals: string[];
  estimated_transhumanist_index: number;
  pattern_severity: string;
  last_updated: string;
}

interface TopRiskEntity {
  id: string;
  name: string;
  composite_score: number;
  risk_level: string;
  primary_pattern: string;
}

interface CriticalAlert {
  id: string;
  name: string;
  composite_score: number;
  primary_pattern: string;
  alert: string;
}

interface SummaryData {
  total_entities: number;
  avg_composite: number;
  risk_distribution: Record<string, number>;
  pattern_distribution: Record<string, number>;
  top_risk_entities: TopRiskEntity[];
  critical_alerts: CriticalAlert[];
  last_analysis: string;
  engine_version: string;
  domain: string;
  confidence_score: number;
  data_sources: string[];
  entities: EntityDict[];
  avg_estimated_transhumanist_index: number;
}

interface ApiResponse {
  digital_seal?: unknown;
  [key: string]: unknown;
}

// ── Color maps ─────────────────────────────────────────────────────────────────

const RISK_COLOR: Record<string, string> = {
  critique: "#ef4444",
  élevé: "#f97316",
  modéré: "#eab308",
  faible: "#22c55e",
};

const RISK_BADGE_CLASS: Record<string, string> = {
  critique: "bg-red-950 text-red-400 border border-red-800",
  élevé: "bg-orange-950 text-orange-400 border border-orange-800",
  modéré: "bg-yellow-950 text-yellow-400 border border-yellow-800",
  faible: "bg-green-950 text-green-400 border border-green-800",
};

const PATTERN_COLOR: Record<string, string> = {
  "Augmentation Non Consentie": "#ef4444",
  "Inégalité d'Accès Transhumaniste": "#f97316",
  "Dérive Eugéniste": "#a855f7",
  "Vide Réglementaire Critique": "#8b5cf6",
  "Risque Éthique Émergent": "#6366f1",
};

// ── GaugeRing ─────────────────────────────────────────────────────────────────

function GaugeRing({ value, label, color }: { value: number; label: string; color: string }) {
  const r = 36;
  const circ = 2 * Math.PI * r;
  const fill = circ * (1 - value / 100);
  return (
    <div className="flex flex-col items-center gap-1">
      <svg width="88" height="88" viewBox="0 0 88 88">
        <circle cx="44" cy="44" r={r} fill="none" stroke="#0f172a" strokeWidth="8"/>
        <circle cx="44" cy="44" r={r} fill="none" stroke={color} strokeWidth="8"
          strokeDasharray={circ} strokeDashoffset={fill}
          strokeLinecap="round" transform="rotate(-90 44 44)"/>
        <text x="44" y="49" textAnchor="middle" fill="white" fontSize="13" fontWeight="bold">
          {Math.round(value)}
        </text>
      </svg>
      <span className="text-xs text-stone-400 text-center">{label}</span>
    </div>
  );
}

// ── DistBar ───────────────────────────────────────────────────────────────────

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
    <div className="flex flex-col gap-1.5">
      <span className="text-xs text-purple-400/70 font-medium uppercase tracking-wide">{title}</span>
      <div className="flex h-3 rounded overflow-hidden gap-px">
        {Object.entries(counts).map(([k, v]) => (
          <div
            key={k}
            style={{ width: `${(v / total) * 100}%`, background: colors[k] || "#6d28d9" }}
            title={`${k}: ${v}`}
          />
        ))}
      </div>
      <div className="flex flex-wrap gap-x-3 gap-y-0.5">
        {Object.entries(counts).map(([k, v]) => (
          <span key={k} className="text-xs text-purple-300/60">
            <span style={{ color: colors[k] || "#7c3aed" }}>■</span>{" "}
            {k} {v}
          </span>
        ))}
      </div>
    </div>
  );
}

// ── DetailModal ───────────────────────────────────────────────────────────────

const PATTERN_ACTIONS: Record<string, string> = {
  "Augmentation Non Consentie":
    "Suspension immédiate des programmes d'augmentation non consentis et audit indépendant obligatoire par un comité éthique accrédité.",
  "Inégalité d'Accès Transhumaniste":
    "Mise en place d'un cadre d'accès équitable aux technologies d'augmentation — programmes publics subventionnés requis.",
  "Dérive Eugéniste":
    "Interdiction immédiate des programmes à visée sélective. Saisine des autorités éthiques nationales et internationales.",
  "Vide Réglementaire Critique":
    "Engagement urgent des régulateurs pour combler le vide juridique sur l'augmentation humaine. Moratoire temporaire recommandé.",
  "Risque Éthique Émergent":
    "Mise en veille éthique renforcée. Consultation des comités d'éthique spécialisés et renforcement de la documentation de consentement.",
};

function DetailModal({ entity, onClose }: { entity: EntityDict; onClose: () => void }) {
  const [tab, setTab] = useState<"scores" | "signaux" | "actions">("scores");

  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
    };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [onClose]);

  const riskAction =
    entity.risk_level === "critique"
      ? "Intervention urgente requise — risque éthique transhumaniste systémique. Mobilisation des autorités de régulation et des comités d'éthique indépendants."
      : entity.risk_level === "élevé"
      ? "Surveillance renforcée et mise en conformité accélérée avec les standards éthiques internationaux de l'augmentation humaine."
      : entity.risk_level === "modéré"
      ? "Veille éthique active. Renforcement des protocoles de consentement et d'équité d'accès recommandé."
      : "Maintien des bonnes pratiques éthiques. Contribution aux initiatives de normalisation transhumaniste internationale.";

  const patternAction = PATTERN_ACTIONS[entity.primary_pattern] ?? riskAction;

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm"
      onClick={onClose}
    >
      <div
        className="bg-slate-950 border border-purple-700/40 rounded-2xl w-full max-w-lg p-6 shadow-2xl shadow-purple-900/20"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="flex items-start justify-between mb-5">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <span className="text-lg font-bold text-white">{entity.name}</span>
              <span
                className={`text-xs px-2 py-0.5 rounded-full font-medium ${
                  RISK_BADGE_CLASS[entity.risk_level] ?? "bg-slate-800 text-slate-300"
                }`}
              >
                {entity.risk_level}
              </span>
            </div>
            <div className="flex items-center gap-2 text-xs text-slate-400">
              <span>{entity.id}</span>
              <span>·</span>
              <span>{entity.country}</span>
              <span>·</span>
              <span>{entity.sector}</span>
            </div>
            <div className="mt-1 text-xs text-purple-400/70">{entity.primary_pattern}</div>
          </div>
          <button
            onClick={onClose}
            className="text-slate-500 hover:text-white text-xl leading-none ml-4 flex-shrink-0"
          >
            ✕
          </button>
        </div>

        {/* Composite score summary */}
        <div className="flex items-center gap-3 mb-5 p-3 rounded-xl bg-slate-900 border border-purple-800/20">
          <div className="text-3xl font-bold text-purple-300">{entity.composite_score.toFixed(2)}</div>
          <div>
            <div className="text-xs text-slate-500">Score composite</div>
            <div className="text-xs text-violet-400">
              Index éthique:{" "}
              <span className="font-bold text-violet-300">{entity.estimated_transhumanist_index.toFixed(2)}/10</span>
            </div>
          </div>
        </div>

        {/* Tabs */}
        <div className="flex gap-2 mb-4">
          {(["scores", "signaux", "actions"] as const).map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
                tab === t
                  ? "bg-purple-900 text-white border border-purple-700"
                  : "bg-slate-900 text-slate-400 hover:text-white border border-transparent"
              }`}
            >
              {t === "scores" ? "Scores" : t === "signaux" ? "Signaux" : "Actions"}
            </button>
          ))}
        </div>

        {/* Tab: Scores */}
        {tab === "scores" && (
          <div className="flex flex-col gap-3">
            {[
              ["Augmentation", entity.enhancement_score, "#a855f7"],
              ["Consentement", entity.consent_score, "#7c3aed"],
              ["Équité", entity.equity_score, "#6366f1"],
              ["Gouvernance", entity.governance_score, "#4f46e5"],
            ].map(([label, value, color]) => (
              <div key={String(label)} className="bg-slate-900 border border-purple-800/20 rounded-xl p-3">
                <div className="flex justify-between items-center mb-2">
                  <span className="text-xs text-slate-400">{String(label)}</span>
                  <span className="text-sm font-bold text-white">{Number(value).toFixed(1)}</span>
                </div>
                <div className="h-1.5 rounded-full bg-slate-800">
                  <div
                    className="h-1.5 rounded-full transition-all"
                    style={{
                      width: `${Math.min(Number(value), 100)}%`,
                      background: String(color),
                    }}
                  />
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Tab: Signaux */}
        {tab === "signaux" && (
          <div className="flex flex-col gap-2">
            {entity.key_signals.map((signal, i) => (
              <div
                key={i}
                className="flex items-start gap-2 bg-slate-900 border border-purple-800/20 rounded-xl p-3"
              >
                <span
                  className="mt-0.5 flex-shrink-0 w-4 h-4 rounded-full flex items-center justify-center text-xs font-bold"
                  style={{
                    background: RISK_COLOR[entity.risk_level] ?? "#6d28d9",
                    color: "#fff",
                  }}
                >
                  {i + 1}
                </span>
                <span className="text-sm text-slate-300 leading-snug">{signal}</span>
              </div>
            ))}
          </div>
        )}

        {/* Tab: Actions */}
        {tab === "actions" && (
          <div className="flex flex-col gap-3">
            <div className="bg-slate-900 border border-purple-800/20 rounded-xl p-4">
              <div className="text-xs text-purple-400/70 uppercase tracking-wide mb-2 font-medium">
                Action recommandée — Niveau {entity.risk_level}
              </div>
              <p className="text-sm text-slate-300 leading-relaxed">{riskAction}</p>
            </div>
            <div className="bg-slate-900 border border-violet-800/20 rounded-xl p-4">
              <div className="text-xs text-violet-400/70 uppercase tracking-wide mb-2 font-medium">
                Action spécifique — {entity.primary_pattern}
              </div>
              <p className="text-sm text-slate-300 leading-relaxed">{patternAction}</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

// ── Main page ─────────────────────────────────────────────────────────────────

export default function TranshumanistEthicsEnginePage() {
  const [data, setData] = useState<SummaryData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [riskFilter, setRiskFilter] = useState<string>("tous");
  const [countryFilter, setCountryFilter] = useState<string>("tous");
  const [selectedEntity, setSelectedEntity] = useState<EntityDict | null>(null);

  useEffect(() => {
    fetch("/api/transhumanist-ethics-engine")
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.json() as Promise<ApiResponse & SummaryData>;
      })
      .then((json) => {
        // Strip the digital_seal wrapper key if present, use the rest as SummaryData
        const { digital_seal: _seal, ...rest } = json;
        void _seal;
        setData(rest as unknown as SummaryData);
        setLoading(false);
      })
      .catch((err: unknown) => {
        setError(err instanceof Error ? err.message : "Erreur inconnue");
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center">
        <div className="text-purple-400 text-sm animate-pulse">
          Chargement du moteur éthique transhumaniste…
        </div>
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center">
        <div className="text-red-400 text-sm">
          Erreur : {error ?? "Données indisponibles"}
        </div>
      </div>
    );
  }

  const entities: EntityDict[] = data.entities ?? [];

  // ── Derived stats ─────────────────────────────────────────────────────────
  const avgEnhancement =
    entities.length > 0
      ? entities.reduce((s, e) => s + e.enhancement_score, 0) / entities.length
      : 0;
  const avgConsent =
    entities.length > 0
      ? entities.reduce((s, e) => s + e.consent_score, 0) / entities.length
      : 0;
  const avgEquity =
    entities.length > 0
      ? entities.reduce((s, e) => s + e.equity_score, 0) / entities.length
      : 0;
  const avgGovernance =
    entities.length > 0
      ? entities.reduce((s, e) => s + e.governance_score, 0) / entities.length
      : 0;

  const riskDist = data.risk_distribution ?? {};
  const critiqueCount = riskDist["critique"] ?? 0;
  const eleveCount = riskDist["élevé"] ?? 0;

  // ── Countries ─────────────────────────────────────────────────────────────
  const countries = Array.from(new Set(entities.map((e) => e.country))).sort();

  // ── Country / sector distributions ───────────────────────────────────────
  const countryDist: Record<string, number> = {};
  const sectorDist: Record<string, number> = {};
  for (const e of entities) {
    countryDist[e.country] = (countryDist[e.country] ?? 0) + 1;
    sectorDist[e.sector] = (sectorDist[e.sector] ?? 0) + 1;
  }

  const countryColors: Record<string, string> = {
    USA: "#a855f7",
    Chine: "#ef4444",
    "Émirats Arabes Unis": "#f97316",
    Japon: "#eab308",
    Russie: "#6366f1",
    Allemagne: "#22c55e",
    Norvège: "#0ea5e9",
    Suisse: "#14b8a6",
  };
  const sectorColors: Record<string, string> = {
    Neurotechnology: "#a855f7",
    Biotechnology: "#f97316",
    Cybernetics: "#8b5cf6",
    Pharmaceuticals: "#6366f1",
    Research: "#22c55e",
    "Ethics Research": "#14b8a6",
  };

  // ── Filtered entities ─────────────────────────────────────────────────────
  const filtered = entities.filter((e) => {
    const riskOk = riskFilter === "tous" || e.risk_level === riskFilter;
    const countryOk = countryFilter === "tous" || e.country === countryFilter;
    return riskOk && countryOk;
  });

  return (
    <div className="min-h-screen bg-slate-950 text-white px-4 py-8 font-sans">
      {/* Modal */}
      {selectedEntity && (
        <DetailModal
          entity={selectedEntity}
          onClose={() => setSelectedEntity(null)}
        />
      )}

      {/* Header */}
      <div className="max-w-7xl mx-auto mb-8">
        <div className="flex items-start justify-between gap-4 flex-wrap">
          <div>
            <h1 className="text-2xl font-bold text-white tracking-tight">
              Transhumanist Ethics Engine
            </h1>
            <p className="text-slate-400 text-sm mt-1">
              Surveillance éthique des technologies d'augmentation humaine — Caelum Partners
            </p>
          </div>
          <div className="flex items-center gap-3 text-xs text-slate-500">
            <span className="bg-purple-950 text-purple-400 border border-purple-800 px-2 py-1 rounded-full">
              v{data.engine_version}
            </span>
            <span>Confiance: {(data.confidence_score * 100).toFixed(0)}%</span>
            <span>
              {new Date(data.last_analysis).toLocaleDateString("fr-FR", {
                day: "2-digit",
                month: "short",
                year: "numeric",
              })}
            </span>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto space-y-6">
        {/* ── KPI Cards ─────────────────────────────────────────────────── */}
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
          {/* Total Entités */}
          <div className="bg-slate-900 border border-purple-800/20 rounded-2xl p-4 flex flex-col gap-1">
            <span className="text-xs text-slate-500 uppercase tracking-wide">Total Entités</span>
            <span className="text-3xl font-bold text-white">{data.total_entities}</span>
            <span className="text-xs text-purple-400/60">domaine {data.domain}</span>
          </div>

          {/* Critique */}
          <div className="bg-slate-900 border border-red-800/30 rounded-2xl p-4 flex flex-col gap-1">
            <span className="text-xs text-slate-500 uppercase tracking-wide">Critique</span>
            <span className="text-3xl font-bold text-red-400">{critiqueCount}</span>
            <span className="text-xs text-red-500/60">risque ≥ 60</span>
          </div>

          {/* Élevé */}
          <div className="bg-slate-900 border border-orange-800/30 rounded-2xl p-4 flex flex-col gap-1">
            <span className="text-xs text-slate-500 uppercase tracking-wide">Élevé</span>
            <span className="text-3xl font-bold text-orange-400">{eleveCount}</span>
            <span className="text-xs text-orange-500/60">risque 40–59</span>
          </div>

          {/* Composite moyen */}
          <div className="bg-slate-900 border border-purple-700/30 rounded-2xl p-4 flex flex-col gap-1">
            <span className="text-xs text-slate-500 uppercase tracking-wide">Composite Moyen</span>
            <span className="text-3xl font-bold text-purple-400">
              {data.avg_composite.toFixed(1)}
            </span>
            <span className="text-xs text-purple-500/60">sur 100</span>
          </div>

          {/* Index Éthique */}
          <div className="bg-slate-900 border border-violet-700/30 rounded-2xl p-4 flex flex-col gap-1">
            <span className="text-xs text-slate-500 uppercase tracking-wide">Index Éthique</span>
            <span className="text-3xl font-bold text-violet-400">
              {data.avg_estimated_transhumanist_index.toFixed(2)}
            </span>
            <span className="text-xs text-violet-500/60">sur /10</span>
          </div>

          {/* Score Consentement Moyen */}
          <div className="bg-slate-900 border border-blue-800/30 rounded-2xl p-4 flex flex-col gap-1">
            <span className="text-xs text-slate-500 uppercase tracking-wide">Consentement Moy.</span>
            <span className="text-3xl font-bold text-blue-400">
              {avgConsent.toFixed(1)}
            </span>
            <span className="text-xs text-blue-500/60">sur 100</span>
          </div>
        </div>

        {/* ── Gauge Rings ───────────────────────────────────────────────── */}
        <div className="bg-slate-900 border border-purple-800/20 rounded-2xl p-6">
          <h2 className="text-sm font-semibold text-purple-300 uppercase tracking-wide mb-5">
            Scores Moyens par Dimension
          </h2>
          <div className="flex flex-wrap gap-8 justify-center sm:justify-start">
            <GaugeRing value={avgEnhancement} label="Augmentation" color="#a855f7" />
            <GaugeRing value={avgConsent} label="Consentement" color="#7c3aed" />
            <GaugeRing value={avgEquity} label="Équité" color="#6366f1" />
            <GaugeRing value={avgGovernance} label="Gouvernance" color="#4f46e5" />
          </div>
        </div>

        {/* ── Distributions ─────────────────────────────────────────────── */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div className="bg-slate-900 border border-purple-800/20 rounded-2xl p-5 flex flex-col gap-5">
            <DistBar
              title="Distribution des niveaux de risque"
              counts={riskDist}
              colors={RISK_COLOR}
            />
            <DistBar
              title="Distribution des patterns éthiques"
              counts={data.pattern_distribution ?? {}}
              colors={PATTERN_COLOR}
            />
          </div>
          <div className="bg-slate-900 border border-purple-800/20 rounded-2xl p-5 flex flex-col gap-5">
            <DistBar
              title="Distribution par pays"
              counts={countryDist}
              colors={countryColors}
            />
            <DistBar
              title="Distribution par secteur"
              counts={sectorDist}
              colors={sectorColors}
            />
          </div>
        </div>

        {/* ── Critical alerts ───────────────────────────────────────────── */}
        {data.critical_alerts && data.critical_alerts.length > 0 && (
          <div className="bg-slate-900 border border-red-800/30 rounded-2xl p-5">
            <h2 className="text-sm font-semibold text-red-400 uppercase tracking-wide mb-4">
              Alertes Critiques ({data.critical_alerts.length})
            </h2>
            <div className="flex flex-col gap-3">
              {data.critical_alerts.map((alert) => (
                <div
                  key={alert.id}
                  className="flex items-start gap-3 bg-red-950/20 border border-red-800/20 rounded-xl p-3"
                >
                  <span className="flex-shrink-0 mt-0.5 w-2 h-2 rounded-full bg-red-500 animate-pulse" />
                  <div>
                    <div className="flex items-center gap-2 mb-0.5">
                      <span className="text-sm font-semibold text-white">{alert.name}</span>
                      <span className="text-xs text-slate-500">{alert.id}</span>
                      <span className="text-xs text-red-400 font-bold">
                        {alert.composite_score.toFixed(2)}
                      </span>
                    </div>
                    <div className="text-xs text-slate-400">{alert.alert}</div>
                    <div className="text-xs text-red-400/70 mt-0.5">{alert.primary_pattern}</div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* ── Top Risk entities ─────────────────────────────────────────── */}
        <div className="bg-slate-900 border border-purple-800/20 rounded-2xl p-5">
          <h2 className="text-sm font-semibold text-purple-300 uppercase tracking-wide mb-4">
            Top 3 Entités à Risque
          </h2>
          <div className="flex flex-col gap-3">
            {(data.top_risk_entities ?? []).map((e, i) => (
              <div
                key={e.id}
                className="flex items-center gap-4 bg-slate-950 border border-purple-800/20 rounded-xl p-3"
              >
                <span className="text-2xl font-black text-purple-700/40 w-6 text-center leading-none">
                  {i + 1}
                </span>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 flex-wrap">
                    <span className="font-semibold text-white text-sm">{e.name}</span>
                    <span
                      className={`text-xs px-2 py-0.5 rounded-full font-medium ${
                        RISK_BADGE_CLASS[e.risk_level] ?? "bg-slate-800 text-slate-300"
                      }`}
                    >
                      {e.risk_level}
                    </span>
                  </div>
                  <div className="text-xs text-slate-500 mt-0.5">{e.primary_pattern}</div>
                </div>
                <div className="text-right flex-shrink-0">
                  <div className="text-lg font-bold text-purple-300">
                    {e.composite_score.toFixed(2)}
                  </div>
                  <div className="text-xs text-slate-600">composite</div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* ── Filters ───────────────────────────────────────────────────── */}
        <div className="flex flex-wrap gap-3 items-center">
          {/* Risk level pills */}
          <div className="flex flex-wrap gap-2">
            {["tous", "critique", "élevé", "modéré", "faible"].map((level) => (
              <button
                key={level}
                onClick={() => setRiskFilter(level)}
                className={`px-3 py-1 rounded-full text-xs font-medium transition-colors ${
                  riskFilter === level
                    ? level === "tous"
                      ? "bg-purple-800 text-white"
                      : `text-white`
                    : "bg-slate-800 text-slate-400 hover:text-white"
                }`}
                style={
                  riskFilter === level && level !== "tous"
                    ? { background: RISK_COLOR[level], color: "#fff" }
                    : undefined
                }
              >
                {level}
              </button>
            ))}
          </div>

          {/* Country pills */}
          <div className="flex flex-wrap gap-2">
            <button
              onClick={() => setCountryFilter("tous")}
              className={`px-3 py-1 rounded-full text-xs font-medium transition-colors ${
                countryFilter === "tous"
                  ? "bg-violet-800 text-white"
                  : "bg-slate-800 text-slate-400 hover:text-white"
              }`}
            >
              tous pays
            </button>
            {countries.map((country) => (
              <button
                key={country}
                onClick={() => setCountryFilter(country)}
                className={`px-3 py-1 rounded-full text-xs font-medium transition-colors ${
                  countryFilter === country
                    ? "bg-violet-700 text-white"
                    : "bg-slate-800 text-slate-400 hover:text-white"
                }`}
              >
                {country}
              </button>
            ))}
          </div>

          <span className="text-xs text-slate-600 ml-auto">
            {filtered.length} entité{filtered.length !== 1 ? "s" : ""} affichée
            {filtered.length !== 1 ? "s" : ""}
          </span>
        </div>

        {/* ── Entity cards grid ─────────────────────────────────────────── */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          {filtered.map((entity) => (
            <button
              key={entity.id}
              onClick={() => setSelectedEntity(entity)}
              className="text-left bg-slate-900 border border-purple-800/20 rounded-2xl p-4 hover:border-purple-600/50 hover:bg-slate-900/80 transition-all group focus:outline-none focus:ring-2 focus:ring-purple-700"
            >
              {/* Card header */}
              <div className="flex items-start justify-between mb-3 gap-2">
                <div className="flex-1 min-w-0">
                  <div className="font-semibold text-white text-sm leading-tight truncate group-hover:text-purple-200 transition-colors">
                    {entity.name}
                  </div>
                  <div className="text-xs text-slate-500 mt-0.5">
                    {entity.id} · {entity.country}
                  </div>
                </div>
                <span
                  className={`flex-shrink-0 text-xs px-2 py-0.5 rounded-full font-medium ${
                    RISK_BADGE_CLASS[entity.risk_level] ?? "bg-slate-800 text-slate-300"
                  }`}
                >
                  {entity.risk_level}
                </span>
              </div>

              {/* Sector */}
              <div className="text-xs text-purple-400/60 mb-3">{entity.sector}</div>

              {/* Composite score bar */}
              <div className="mb-3">
                <div className="flex justify-between text-xs mb-1">
                  <span className="text-slate-500">Score composite</span>
                  <span className="font-bold text-white">{entity.composite_score.toFixed(2)}</span>
                </div>
                <div className="h-1.5 rounded-full bg-slate-800">
                  <div
                    className="h-1.5 rounded-full transition-all"
                    style={{
                      width: `${Math.min(entity.composite_score, 100)}%`,
                      background: RISK_COLOR[entity.risk_level] ?? "#6d28d9",
                    }}
                  />
                </div>
              </div>

              {/* Primary pattern */}
              <div
                className="text-xs px-2 py-1 rounded-lg font-medium truncate"
                style={{
                  background: `${PATTERN_COLOR[entity.primary_pattern] ?? "#6d28d9"}18`,
                  color: PATTERN_COLOR[entity.primary_pattern] ?? "#a78bfa",
                  border: `1px solid ${PATTERN_COLOR[entity.primary_pattern] ?? "#6d28d9"}30`,
                }}
              >
                {entity.primary_pattern}
              </div>

              {/* Index */}
              <div className="mt-3 text-xs text-slate-600 flex justify-between">
                <span>Index éthique</span>
                <span className="text-violet-400 font-semibold">
                  {entity.estimated_transhumanist_index.toFixed(2)}/10
                </span>
              </div>
            </button>
          ))}

          {filtered.length === 0 && (
            <div className="col-span-full text-center text-slate-600 text-sm py-12">
              Aucune entité pour les filtres sélectionnés.
            </div>
          )}
        </div>

        {/* ── Data sources ──────────────────────────────────────────────── */}
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5">
          <h2 className="text-xs font-semibold text-slate-500 uppercase tracking-wide mb-3">
            Sources de données ({(data.data_sources ?? []).length})
          </h2>
          <div className="flex flex-wrap gap-2">
            {(data.data_sources ?? []).map((source) => (
              <span
                key={source}
                className="text-xs bg-slate-800 text-slate-400 px-2 py-1 rounded-lg border border-slate-700"
              >
                {source}
              </span>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
