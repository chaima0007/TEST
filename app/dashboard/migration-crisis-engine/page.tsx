"use client";
import { useEffect, useState, useRef } from "react";

// ─── Types ────────────────────────────────────────────────────────────────────

type RiskLevel       = "critical" | "high" | "moderate" | "low";
type MigrationPattern = "mass_displacement_crisis" | "asylum_system_collapse" | "climate_exodus" | "xenophobia_cascade" | "demographic_implosion" | "none";
type Severity        = "crise_migratoire_systémique" | "choc_démographique_majeur" | "pression_migratoire_structurelle" | "migration_gérée";
type Action          = "intervention_humanitaire_urgente" | "réforme_système_asile_accélérée" | "renforcement_intégration_systémique" | "veille_démographique_continue";

interface McrEntity {
  id: string;
  migration_corridor: string;
  region: string;
  displacement_score: number;
  reception_score: number;
  social_score: number;
  demographic_score: number;
  composite_score: number;
  risk_level: RiskLevel;
  migration_pattern: MigrationPattern;
  severity: Severity;
  recommended_action: Action;
  signal: string;
  forced_displacement_rate: number;
  climate_migration_acceleration: number;
}

interface McrSummary {
  module_id: number;
  module_name: string;
  total_entities: number;
  critical_count: number;
  high_count: number;
  moderate_count: number;
  low_count: number;
  avg_composite: number;
  pattern_distribution: Record<string, number>;
  risk_distribution: Record<string, number>;
  severity_distribution: Record<string, number>;
  action_distribution: Record<string, number>;
  avg_estimated_migration_crisis_index: number;
}

// ─── Meta ─────────────────────────────────────────────────────────────────────

const RISK_META: Record<RiskLevel, { label: string; color: string; ring: string; bg: string; badge: string }> = {
  critical: { label: "Critique", color: "text-red-400",    ring: "#f87171", bg: "bg-red-950/40",    badge: "bg-red-900/60 text-red-300 border-red-700" },
  high:     { label: "Élevé",    color: "text-amber-400",  ring: "#fbbf24", bg: "bg-amber-950/40",  badge: "bg-amber-900/60 text-amber-300 border-amber-700" },
  moderate: { label: "Modéré",   color: "text-blue-400",   ring: "#60a5fa", bg: "bg-blue-950/40",   badge: "bg-blue-900/60 text-blue-300 border-blue-700" },
  low:      { label: "Faible",   color: "text-slate-400",  ring: "#94a3b8", bg: "bg-slate-900/40",  badge: "bg-slate-800/60 text-slate-300 border-slate-600" },
};

const PATTERN_LABELS: Record<MigrationPattern, string> = {
  mass_displacement_crisis: "Crise Déplacement Massif",
  asylum_system_collapse:   "Effondrement Système Asile",
  climate_exodus:           "Exode Climatique",
  xenophobia_cascade:       "Cascade Xénophobe",
  demographic_implosion:    "Implosion Démographique",
  none:                     "Aucun",
};

const SEV_LABELS: Record<Severity, string> = {
  "crise_migratoire_systémique":       "Crise Migratoire Systémique",
  "choc_démographique_majeur":         "Choc Démographique Majeur",
  "pression_migratoire_structurelle":  "Pression Migratoire Structurelle",
  "migration_gérée":                   "Migration Gérée",
};

const ACTION_LABELS: Record<Action, string> = {
  "intervention_humanitaire_urgente":      "Intervention Humanitaire Urgente",
  "réforme_système_asile_accélérée":       "Réforme Système Asile Accélérée",
  "renforcement_intégration_systémique":   "Renforcement Intégration Systémique",
  "veille_démographique_continue":         "Veille Démographique Continue",
};

const RISK_COLORS: Record<string, string> = {
  critical: "#ef4444",
  high:     "#f59e0b",
  moderate: "#3b82f6",
  low:      "#64748b",
};

const PAT_COLORS: Record<string, string> = {
  mass_displacement_crisis: "#ef4444",
  asylum_system_collapse:   "#f97316",
  climate_exodus:           "#22c55e",
  xenophobia_cascade:       "#a855f7",
  demographic_implosion:    "#3b82f6",
  none:                     "#64748b",
};

const SEV_COLORS: Record<string, string> = {
  "crise_migratoire_systémique":       "#ef4444",
  "choc_démographique_majeur":         "#f59e0b",
  "pression_migratoire_structurelle":  "#3b82f6",
  "migration_gérée":                   "#64748b",
};

const ACT_COLORS: Record<string, string> = {
  "intervention_humanitaire_urgente":      "#ef4444",
  "réforme_système_asile_accélérée":       "#f59e0b",
  "renforcement_intégration_systémique":   "#3b82f6",
  "veille_démographique_continue":         "#64748b",
};

// ─── GaugeRing ────────────────────────────────────────────────────────────────

function GaugeRing({ value, label, color }: { value: number; label: string; color: string }) {
  const r = 36;
  const circ = 2 * Math.PI * r;
  const fill = circ * (1 - value / 100);
  return (
    <div className="flex flex-col items-center gap-1">
      <svg width="88" height="88" viewBox="0 0 88 88">
        <circle cx="44" cy="44" r={r} fill="none" stroke="#1e293b" strokeWidth="8" />
        <circle
          cx="44" cy="44" r={r} fill="none"
          stroke={color} strokeWidth="8"
          strokeDasharray={circ}
          strokeDashoffset={fill}
          strokeLinecap="round"
          transform="rotate(-90 44 44)"
        />
        <text x="44" y="49" textAnchor="middle" fill="white" fontSize="13" fontWeight="bold" fontFamily="sans-serif">
          {Math.round(value)}
        </text>
      </svg>
      <span className="text-xs text-slate-400 text-center">{label}</span>
    </div>
  );
}

// ─── DistBar ──────────────────────────────────────────────────────────────────

function DistBar({ title, counts, colors }: { title: string; counts: Record<string, number>; colors: Record<string, string> }) {
  const total = Object.values(counts).reduce((a, b) => a + b, 0) || 1;
  return (
    <div className="flex flex-col gap-1">
      <span className="text-xs text-slate-400 font-medium">{title}</span>
      <div className="flex h-3 rounded overflow-hidden gap-px">
        {Object.entries(counts).map(([k, v]) => (
          <div
            key={k}
            style={{ width: `${(v / total) * 100}%`, background: colors[k] || "#475569" }}
            title={`${k}: ${v}`}
          />
        ))}
      </div>
      <div className="flex flex-wrap gap-x-3 gap-y-0.5">
        {Object.entries(counts).map(([k, v]) => (
          <span key={k} className="text-xs text-slate-400">
            <span style={{ color: colors[k] || "#94a3b8" }}>■</span> {k.replace(/_/g, " ")} {v}
          </span>
        ))}
      </div>
    </div>
  );
}

// ─── DetailModal ──────────────────────────────────────────────────────────────

function DetailModal({ entity, onClose }: { entity: McrEntity; onClose: () => void }) {
  const [tab, setTab] = useState<"scores" | "signal" | "action">("scores");
  const overlayRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const fn = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", fn);
    return () => window.removeEventListener("keydown", fn);
  }, [onClose]);

  const rm = RISK_META[entity.risk_level];

  return (
    <div
      ref={overlayRef}
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 p-4"
      onClick={(e) => { if (e.target === overlayRef.current) onClose(); }}
    >
      <div className="bg-slate-900 border border-amber-700/30 rounded-2xl w-full max-w-lg shadow-2xl max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="flex items-center justify-between p-5 border-b border-slate-800">
          <div>
            <div className="flex items-center gap-2 flex-wrap">
              <span className="text-lg font-bold text-white">{entity.id}</span>
              <span className="text-amber-400 text-xs">{entity.region}</span>
              <span className={`text-xs font-bold px-2 py-0.5 rounded border ${rm.badge}`}>{rm.label}</span>
            </div>
            <p className="text-slate-400 text-sm mt-0.5">{entity.migration_corridor}</p>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl leading-none p-1">✕</button>
        </div>

        {/* Tabs */}
        <div className="flex border-b border-slate-800">
          {(["scores", "signal", "action"] as const).map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`flex-1 py-2.5 text-xs font-semibold uppercase tracking-wide transition-colors ${
                tab === t ? "text-amber-400 border-b-2 border-amber-400" : "text-slate-500 hover:text-slate-300"
              }`}
            >
              {t === "scores" ? "Scores" : t === "signal" ? "Signal" : "Action"}
            </button>
          ))}
        </div>

        {/* Tab content */}
        <div className="p-5">
          {tab === "scores" && (
            <div className="space-y-3">
              <div className="grid grid-cols-2 gap-3">
                {[
                  ["Déplacement",  entity.displacement_score,  "#f87171"],
                  ["Accueil",      entity.reception_score,     "#fbbf24"],
                  ["Social",       entity.social_score,        "#60a5fa"],
                  ["Démographique",entity.demographic_score,   "#a78bfa"],
                ].map(([l, v, c]) => (
                  <div key={String(l)} className="bg-slate-800 rounded-lg p-3">
                    <div className="text-slate-400 text-xs mb-1">{String(l)}</div>
                    <div className="text-white font-bold text-lg">{Number(v).toFixed(1)}</div>
                    <div className="h-1.5 rounded mt-1 bg-slate-700">
                      <div
                        className="h-1.5 rounded"
                        style={{ width: `${Math.min(Number(v), 100)}%`, background: String(c) }}
                      />
                    </div>
                  </div>
                ))}
              </div>
              <div className="bg-slate-800 rounded-lg p-3">
                <div className="text-slate-400 text-xs mb-1">Score Composite</div>
                <div className="text-white font-bold text-2xl">{entity.composite_score.toFixed(1)}</div>
                <div className="text-xs text-slate-500 mt-0.5">{SEV_LABELS[entity.severity]}</div>
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div className="bg-slate-800 rounded-lg p-3">
                  <div className="text-slate-400 text-xs mb-1">Taux Déplacement Forcé</div>
                  <div className="text-amber-300 font-bold">{Math.round(entity.forced_displacement_rate * 100)}%</div>
                </div>
                <div className="bg-slate-800 rounded-lg p-3">
                  <div className="text-slate-400 text-xs mb-1">Accélération Migration Climatique</div>
                  <div className="text-blue-300 font-bold">{Math.round(entity.climate_migration_acceleration * 100)}%</div>
                </div>
              </div>
            </div>
          )}

          {tab === "signal" && (
            <div className="bg-slate-800 rounded-lg p-4 text-sm text-slate-200 leading-relaxed">
              {entity.signal}
              <div className="mt-3 flex gap-2 flex-wrap">
                <span className={`px-2 py-0.5 rounded text-xs font-medium ${rm.badge}`}>{rm.label}</span>
                <span className="px-2 py-0.5 rounded text-xs font-medium bg-slate-700 text-slate-300">
                  {PATTERN_LABELS[entity.migration_pattern]}
                </span>
              </div>
            </div>
          )}

          {tab === "action" && (
            <div className="space-y-3 text-sm">
              <div className="bg-slate-800 rounded-lg p-3">
                <div className="text-slate-400 text-xs mb-1">Action Recommandée</div>
                <div className="text-amber-300 font-medium">{ACTION_LABELS[entity.recommended_action]}</div>
              </div>
              <div className="bg-slate-800 rounded-lg p-3">
                <div className="text-slate-400 text-xs mb-1">Pattern Migratoire</div>
                <div className="text-white font-medium">{PATTERN_LABELS[entity.migration_pattern]}</div>
              </div>
              <div className="bg-slate-800 rounded-lg p-3">
                <div className="text-slate-400 text-xs mb-1">Sévérité</div>
                <div className="text-white font-medium">{SEV_LABELS[entity.severity]}</div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

// ─── EntityCard ───────────────────────────────────────────────────────────────

function EntityCard({ entity, onClick }: { entity: McrEntity; onClick: () => void }) {
  const rm = RISK_META[entity.risk_level];

  return (
    <button
      onClick={onClick}
      className={`w-full text-left rounded-xl border border-slate-800 ${rm.bg} p-4 hover:border-amber-700/50 transition-colors`}
    >
      <div className="flex items-center justify-between mb-2">
        <span className="font-bold text-white">{entity.id}</span>
        <span className="text-xs text-amber-400">{entity.region}</span>
      </div>
      <div className="text-xs text-slate-400 mb-2">{entity.migration_corridor}</div>
      <div className="flex gap-1 mb-3 flex-wrap">
        <span className={`px-2 py-0.5 rounded text-xs font-bold border ${rm.badge}`}>{rm.label}</span>
      </div>
      <div className="text-2xl font-black text-white mb-1">{entity.composite_score.toFixed(1)}</div>
      <div className="text-xs text-slate-500 mb-2">{PATTERN_LABELS[entity.migration_pattern]}</div>
      <div className="text-xs text-amber-400 font-medium">{SEV_LABELS[entity.severity]}</div>
    </button>
  );
}

// ─── Page ─────────────────────────────────────────────────────────────────────

export default function MigrationCrisisDashboard() {
  const [data, setData]          = useState<{ entities: McrEntity[]; summary: McrSummary } | null>(null);
  const [riskFilter, setRisk]    = useState<string>("all");
  const [patFilter,  setPat]     = useState<string>("all");
  const [selected, setSelected]  = useState<McrEntity | null>(null);

  useEffect(() => {
    fetch("/api/migration-crisis-engine")
      .then((r) => r.json())
      .then(setData)
      .catch(console.error);
  }, []);

  if (!data) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center">
        <div className="text-amber-400 text-lg animate-pulse">Chargement Crise Migratoire…</div>
      </div>
    );
  }

  const { entities, summary } = data;

  const filtered = entities.filter(
    (e) =>
      (riskFilter === "all" || e.risk_level === riskFilter) &&
      (patFilter  === "all" || e.migration_pattern === patFilter),
  );

  const avgDisplacement = entities.length
    ? Math.round((entities.reduce((s, e) => s + e.displacement_score, 0) / entities.length) * 10) / 10
    : 0;

  const kpis = [
    { label: "Total Corridors",         value: summary.total_entities,                                          color: "text-amber-400" },
    { label: "Crise Systémique",         value: summary.critical_count,                                          color: "text-red-400" },
    { label: "Choc Majeur",              value: summary.high_count,                                              color: "text-amber-400" },
    { label: "Composite Moyen",          value: summary.avg_composite.toFixed(1),                                color: "text-blue-400" },
    { label: "Index Crise Migratoire",   value: `${summary.avg_estimated_migration_crisis_index.toFixed(2)}/10`, color: "text-amber-300" },
    { label: "Déplacement Moyen",        value: avgDisplacement.toFixed(1),                                      color: "text-red-400" },
  ];

  const avgRecep = entities.length ? entities.reduce((s, e) => s + e.reception_score, 0) / entities.length : 0;
  const avgSoc   = entities.length ? entities.reduce((s, e) => s + e.social_score, 0) / entities.length : 0;
  const avgDem   = entities.length ? entities.reduce((s, e) => s + e.demographic_score, 0) / entities.length : 0;

  const dists = [
    { title: "Risque",    counts: summary.risk_distribution,     colors: RISK_COLORS },
    { title: "Patterns",  counts: summary.pattern_distribution,  colors: PAT_COLORS  },
    { title: "Sévérité",  counts: summary.severity_distribution, colors: SEV_COLORS  },
    { title: "Actions",   counts: summary.action_distribution,   colors: ACT_COLORS  },
  ] as Array<{ title: string; counts: Record<string, number>; colors: Record<string, string> }>;

  const risks: RiskLevel[]          = ["critical", "high", "moderate", "low"];
  const patterns: MigrationPattern[] = ["mass_displacement_crisis", "asylum_system_collapse", "climate_exodus", "xenophobia_cascade", "demographic_implosion", "none"];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {selected && <DetailModal entity={selected} onClose={() => setSelected(null)} />}

      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-amber-400">Crise Migratoire & Choc Démographique — Module 338</h1>
        <p className="text-slate-400 text-sm mt-1">
          Déplacement · Accueil · Social · Démographique — surveillance des chocs migratoires et démographiques
        </p>
      </div>

      {/* KPI strip */}
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
        {kpis.map((k) => (
          <div key={k.label} className="bg-slate-900 border border-amber-700/30 rounded-xl p-4 text-center">
            <div className={`text-xl font-bold ${k.color}`}>{k.value}</div>
            <div className="text-xs text-slate-500 mt-0.5">{k.label}</div>
          </div>
        ))}
      </div>

      {/* GaugeRings */}
      <div className="bg-slate-900 border border-amber-700/30 rounded-xl p-5">
        <p className="text-xs text-slate-500 mb-4 font-semibold uppercase tracking-wide">Scores Moyens par Dimension</p>
        <div className="grid grid-cols-4 gap-4">
          <GaugeRing value={avgDisplacement} label="Déplacement"   color="#f87171" />
          <GaugeRing value={avgRecep}        label="Accueil"        color="#fbbf24" />
          <GaugeRing value={avgSoc}          label="Social"         color="#60a5fa" />
          <GaugeRing value={avgDem}          label="Démographique"  color="#a78bfa" />
        </div>
      </div>

      {/* DistBars */}
      <div className="bg-slate-900 border border-amber-700/30 rounded-xl p-5 grid grid-cols-1 md:grid-cols-2 gap-5">
        {dists.map((d) => (
          <DistBar key={d.title} {...d} />
        ))}
      </div>

      {/* Filters */}
      <div className="flex flex-col gap-2">
        <div className="flex flex-wrap gap-2">
          {["all", ...risks].map((r) => (
            <button
              key={r}
              onClick={() => setRisk(r)}
              className={`px-3 py-1.5 rounded-full text-xs font-semibold border transition-colors ${
                riskFilter === r
                  ? "bg-amber-700 border-amber-600 text-white"
                  : "bg-slate-900 border-slate-700 text-slate-400 hover:text-white hover:border-amber-600"
              }`}
            >
              {r === "all" ? "Tous risques" : RISK_META[r as RiskLevel].label}
            </button>
          ))}
        </div>
        <div className="flex flex-wrap gap-2">
          {["all", ...patterns].map((p) => (
            <button
              key={p}
              onClick={() => setPat(p)}
              className={`px-3 py-1.5 rounded-full text-xs font-semibold border transition-colors ${
                patFilter === p
                  ? "bg-blue-700 border-blue-600 text-white"
                  : "bg-slate-900 border-slate-700 text-slate-400 hover:text-white hover:border-blue-600"
              }`}
            >
              {p === "all" ? "Tous patterns" : PATTERN_LABELS[p as MigrationPattern]}
            </button>
          ))}
        </div>
      </div>

      {/* Entity grid */}
      {filtered.length === 0 ? (
        <div className="text-center text-slate-500 py-16">Aucun corridor pour ces filtres.</div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          {filtered.map((e) => (
            <EntityCard key={e.id} entity={e} onClick={() => setSelected(e)} />
          ))}
        </div>
      )}
    </div>
  );
}
