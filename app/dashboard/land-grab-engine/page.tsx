"use client";
import { useEffect, useState, useRef } from "react";

// ─── Types ────────────────────────────────────────────────────────────────────

type RiskLevel   = "critical" | "high" | "moderate" | "low";
type LandPattern =
  | "foreign_sovereign_land_capture"
  | "corporate_agribusiness_displacement"
  | "climate_migration_land_conflict"
  | "indigenous_territory_seizure"
  | "green_colonialism_trap"
  | "none";
type Severity =
  | "crise_accaparement_terres_systémique"
  | "crise_souveraineté_alimentaire_majeure"
  | "dépossession_foncière_structurelle"
  | "pression_foncière_sous_surveillance";
type Action =
  | "intervention_urgente_protection_terres_critiques"
  | "réforme_foncière_accélérée_communautés_vulnérables"
  | "renforcement_droits_fonciers_souveraineté_alimentaire"
  | "veille_accaparement_terres_continue";

interface LgeEntity {
  entity_id: string;
  land_type: string;
  region: string;
  dispossession_score: number;
  food_sovereignty_score: number;
  violence_score: number;
  governance_score: number;
  composite_score: number;
  risk_level: RiskLevel;
  land_pattern: LandPattern;
  severity: Severity;
  recommended_action: Action;
  signal: string;
  land_concentration: number;
  smallholder_displacement: number;
}

interface LgeSummary {
  module_id: number;
  module_name: string;
  total: number;
  critical: number;
  high: number;
  moderate: number;
  low: number;
  avg_composite: number;
  pattern_distribution: Record<string, number>;
  risk_distribution: Record<string, number>;
  severity_distribution: Record<string, number>;
  action_distribution: Record<string, number>;
  avg_estimated_land_grab_index: number;
  avg_dispossession_score: number;
  avg_food_sovereignty_score: number;
  avg_violence_score: number;
  avg_governance_score: number;
}

// ─── Meta ─────────────────────────────────────────────────────────────────────

const RISK_META: Record<RiskLevel, { label: string; color: string; ring: string; bg: string; badge: string }> = {
  critical: { label: "Critique", color: "text-red-400",    ring: "#f87171", bg: "bg-red-950/40",    badge: "bg-red-900/60 text-red-300 border-red-700"       },
  high:     { label: "Élevé",    color: "text-amber-400",  ring: "#fbbf24", bg: "bg-amber-950/40",  badge: "bg-amber-900/60 text-amber-300 border-amber-700"  },
  moderate: { label: "Modéré",   color: "text-yellow-400", ring: "#facc15", bg: "bg-yellow-950/40", badge: "bg-yellow-900/60 text-yellow-300 border-yellow-700"},
  low:      { label: "Faible",   color: "text-green-400",  ring: "#4ade80", bg: "bg-green-950/40",  badge: "bg-green-900/60 text-green-300 border-green-700"  },
};

const PATTERN_LABELS: Record<LandPattern, string> = {
  foreign_sovereign_land_capture:      "Captation Foncière Souveraine Étrangère",
  corporate_agribusiness_displacement: "Déplacement Agro-Industrie Corporative",
  climate_migration_land_conflict:     "Conflit Foncier Migration Climatique",
  indigenous_territory_seizure:        "Saisie Territoire Autochtone",
  green_colonialism_trap:              "Piège Colonialisme Vert",
  none:                                "Aucun",
};

const SEV_LABELS: Record<Severity, string> = {
  "crise_accaparement_terres_systémique":   "Crise Accaparement Terres Systémique",
  "crise_souveraineté_alimentaire_majeure": "Crise Souveraineté Alimentaire Majeure",
  "dépossession_foncière_structurelle":     "Dépossession Foncière Structurelle",
  "pression_foncière_sous_surveillance":    "Pression Foncière sous Surveillance",
};

const ACTION_LABELS: Record<Action, string> = {
  "intervention_urgente_protection_terres_critiques":      "Intervention Urgente — Protection Terres Critiques",
  "réforme_foncière_accélérée_communautés_vulnérables":   "Réforme Foncière Accélérée",
  "renforcement_droits_fonciers_souveraineté_alimentaire": "Renforcement Droits Fonciers",
  "veille_accaparement_terres_continue":                  "Veille Accaparement Terres Continue",
};

const RISK_COLORS: Record<string, string> = {
  critical: "#ef4444",
  high:     "#f59e0b",
  moderate: "#facc15",
  low:      "#4ade80",
};

const PAT_COLORS: Record<string, string> = {
  foreign_sovereign_land_capture:      "#ef4444",
  corporate_agribusiness_displacement: "#f59e0b",
  climate_migration_land_conflict:     "#3b82f6",
  indigenous_territory_seizure:        "#a855f7",
  green_colonialism_trap:              "#22c55e",
  none:                                "#64748b",
};

const SEV_COLORS: Record<string, string> = {
  "crise_accaparement_terres_systémique":   "#ef4444",
  "crise_souveraineté_alimentaire_majeure": "#f59e0b",
  "dépossession_foncière_structurelle":     "#facc15",
  "pression_foncière_sous_surveillance":    "#4ade80",
};

const ACT_COLORS: Record<string, string> = {
  "intervention_urgente_protection_terres_critiques":      "#ef4444",
  "réforme_foncière_accélérée_communautés_vulnérables":   "#f59e0b",
  "renforcement_droits_fonciers_souveraineté_alimentaire": "#facc15",
  "veille_accaparement_terres_continue":                  "#4ade80",
};

// ─── GaugeRing ────────────────────────────────────────────────────────────────

function GaugeRing({ value, label, color }: { value: number; label: string; color: string }) {
  const r    = 36;
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
            <span style={{ color: colors[k] || "#94a3b8" }}>■</span>{" "}
            {k.replace(/_/g, " ")} {v}
          </span>
        ))}
      </div>
    </div>
  );
}

// ─── DetailModal ──────────────────────────────────────────────────────────────

function DetailModal({ entity, onClose }: { entity: LgeEntity; onClose: () => void }) {
  const [tab, setTab] = useState<"scores" | "signal" | "action">("scores");
  const overlayRef    = useRef<HTMLDivElement>(null);

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
              <span className="text-lg font-bold text-white">{entity.entity_id}</span>
              <span className="text-amber-400 text-xs">{entity.region}</span>
              <span className={`text-xs font-bold px-2 py-0.5 rounded border ${rm.badge}`}>{rm.label}</span>
            </div>
            <p className="text-slate-400 text-sm capitalize mt-0.5">{entity.land_type.replace(/_/g, " ")}</p>
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
                tab === t
                  ? "text-amber-400 border-b-2 border-amber-400"
                  : "text-slate-500 hover:text-slate-300"
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
                {([
                  ["Dépossession",       entity.dispossession_score,    "#ef4444"],
                  ["Souveraineté Alim.", entity.food_sovereignty_score, "#f59e0b"],
                  ["Violence",           entity.violence_score,         "#f87171"],
                  ["Gouvernance",        entity.governance_score,       "#fbbf24"],
                ] as [string, number, string][]).map(([l, v, c]) => (
                  <div key={l} className="bg-slate-800 rounded-lg p-3">
                    <div className="text-slate-400 text-xs mb-1">{l}</div>
                    <div className="text-white font-bold text-lg">{v.toFixed(1)}</div>
                    <div className="h-1.5 rounded mt-1 bg-slate-700">
                      <div
                        className="h-1.5 rounded"
                        style={{ width: `${Math.min(v, 100)}%`, background: c }}
                      />
                    </div>
                  </div>
                ))}
              </div>
              <div className="bg-slate-800 rounded-lg p-3">
                <div className="text-slate-400 text-xs mb-1">Score Composite Accaparement</div>
                <div className="text-white font-bold text-2xl">{entity.composite_score.toFixed(1)}</div>
                <div className="text-xs text-slate-500 mt-0.5">{SEV_LABELS[entity.severity]}</div>
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div className="bg-slate-800 rounded-lg p-3">
                  <div className="text-slate-400 text-xs mb-1">Concentration Terres</div>
                  <div className="text-amber-300 font-bold">{(entity.land_concentration * 100).toFixed(0)}%</div>
                </div>
                <div className="bg-slate-800 rounded-lg p-3">
                  <div className="text-slate-400 text-xs mb-1">Déplacement Petits Exploitants</div>
                  <div className="text-red-300 font-bold">{(entity.smallholder_displacement * 100).toFixed(0)}%</div>
                </div>
              </div>
            </div>
          )}

          {tab === "signal" && (
            <div className="bg-slate-800 rounded-lg p-4 text-sm text-slate-200 leading-relaxed">
              {entity.signal}
              <div className="mt-3 flex gap-2 flex-wrap">
                <span className={`px-2 py-0.5 rounded text-xs font-medium border ${rm.badge}`}>{rm.label}</span>
                <span className="px-2 py-0.5 rounded text-xs font-medium bg-slate-700 text-slate-300">
                  {PATTERN_LABELS[entity.land_pattern]}
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
                <div className="text-slate-400 text-xs mb-1">Pattern Foncier</div>
                <div className="text-white font-medium">{PATTERN_LABELS[entity.land_pattern]}</div>
              </div>
              <div className="bg-slate-800 rounded-lg p-3">
                <div className="text-slate-400 text-xs mb-1">Sévérité</div>
                <div className="text-white font-medium">{SEV_LABELS[entity.severity]}</div>
              </div>
              {entity.risk_level === "critical" && (
                <span className="inline-block px-2 py-1 rounded bg-red-900/60 text-red-300 text-xs font-bold border border-red-700">
                  ACCAPAREMENT CRITIQUE
                </span>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

// ─── EntityCard ───────────────────────────────────────────────────────────────

function EntityCard({ entity, onClick }: { entity: LgeEntity; onClick: () => void }) {
  const rm = RISK_META[entity.risk_level];

  return (
    <button
      onClick={onClick}
      className={`w-full text-left rounded-xl border border-slate-800 ${rm.bg} p-4 hover:border-amber-700/50 transition-colors`}
    >
      <div className="flex items-center justify-between mb-2">
        <span className="font-bold text-white">{entity.entity_id}</span>
        <span className="text-xs text-amber-400">{entity.region}</span>
      </div>
      <div className="text-xs text-slate-400 mb-2 capitalize">{entity.land_type.replace(/_/g, " ")}</div>
      <div className="flex gap-1 mb-3 flex-wrap">
        <span className={`px-2 py-0.5 rounded text-xs font-bold border ${rm.badge}`}>{rm.label}</span>
      </div>
      <div className="text-2xl font-black text-white mb-1">{entity.composite_score.toFixed(1)}</div>
      <div className="text-xs text-slate-500 mb-2">{PATTERN_LABELS[entity.land_pattern]}</div>
      <div className="text-xs text-amber-400 font-medium mb-2">{SEV_LABELS[entity.severity]}</div>
      <div className="text-xs text-slate-400 leading-snug line-clamp-2">{entity.signal}</div>
    </button>
  );
}

// ─── Page ─────────────────────────────────────────────────────────────────────

export default function LandGrabEngineDashboard() {
  const [data, setData]              = useState<{ entities: LgeEntity[]; summary: LgeSummary } | null>(null);
  const [riskFilter, setRiskFilter]  = useState<string>("all");
  const [patFilter,  setPatFilter]   = useState<string>("all");
  const [selected,   setSelected]    = useState<LgeEntity | null>(null);

  useEffect(() => {
    fetch("/api/land-grab-engine")
      .then((r) => r.json())
      .then(setData)
      .catch(console.error);
  }, []);

  if (!data) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center">
        <div className="text-amber-400 text-lg animate-pulse">Chargement Accaparement Terres…</div>
      </div>
    );
  }

  const { entities, summary } = data;

  const filtered = entities.filter(
    (e) =>
      (riskFilter === "all" || e.risk_level  === riskFilter) &&
      (patFilter  === "all" || e.land_pattern === patFilter),
  );

  const kpis = [
    { label: "Total Entités",         value: String(summary.total),                                                    color: "text-amber-400"  },
    { label: "Accaparement Critique", value: String(summary.critical),                                                 color: "text-red-400"    },
    { label: "Risque Élevé",          value: String(summary.high),                                                     color: "text-amber-400"  },
    { label: "Composite Moyen",       value: summary.avg_composite.toFixed(1),                                         color: "text-yellow-400" },
    { label: "Index Accaparement",    value: `${summary.avg_estimated_land_grab_index.toFixed(2)}/10`,                 color: "text-red-400"    },
    { label: "Dépossession Moy.",     value: Math.round(summary.avg_dispossession_score ?? 0).toString(),              color: "text-amber-400"  },
  ];

  const dists = [
    { title: "Risque",    counts: summary.risk_distribution,     colors: RISK_COLORS },
    { title: "Patterns",  counts: summary.pattern_distribution,  colors: PAT_COLORS  },
    { title: "Sévérité",  counts: summary.severity_distribution, colors: SEV_COLORS  },
    { title: "Actions",   counts: summary.action_distribution,   colors: ACT_COLORS  },
  ] as Array<{ title: string; counts: Record<string, number>; colors: Record<string, string> }>;

  const risks:    RiskLevel[]   = ["critical", "high", "moderate", "low"];
  const patterns: LandPattern[] = [
    "foreign_sovereign_land_capture",
    "corporate_agribusiness_displacement",
    "climate_migration_land_conflict",
    "indigenous_territory_seizure",
    "green_colonialism_trap",
    "none",
  ];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {selected && <DetailModal entity={selected} onClose={() => setSelected(null)} />}

      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-amber-400">
          Accaparement Terres &amp; Déplacement Agricole — Module 403
        </h1>
        <p className="text-slate-400 text-sm mt-1">
          Dépossession · Souveraineté Alimentaire · Violence · Gouvernance — surveillance de l&apos;accaparement foncier mondial
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
        <p className="text-xs text-slate-500 mb-4 font-semibold uppercase tracking-wide">
          Scores Moyens par Dimension
        </p>
        <div className="grid grid-cols-4 gap-4">
          <GaugeRing value={summary.avg_dispossession_score    ?? 0} label="Dépossession"   color="#ef4444" />
          <GaugeRing value={summary.avg_food_sovereignty_score ?? 0} label="Souveraineté"   color="#f59e0b" />
          <GaugeRing value={summary.avg_violence_score         ?? 0} label="Violence"        color="#f87171" />
          <GaugeRing value={summary.avg_governance_score       ?? 0} label="Gouvernance"     color="#fbbf24" />
        </div>
      </div>

      {/* DistBars */}
      <div className="bg-slate-900 border border-amber-700/30 rounded-xl p-5 grid grid-cols-1 md:grid-cols-2 gap-5">
        {dists.map((d) => (
          <DistBar key={d.title} {...d} />
        ))}
      </div>

      {/* Risk filters */}
      <div className="flex flex-col gap-2">
        <div className="flex flex-wrap gap-2">
          {["all", ...risks].map((r) => (
            <button
              key={r}
              onClick={() => setRiskFilter(r)}
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
        {/* Pattern filters */}
        <div className="flex flex-wrap gap-2">
          {["all", ...patterns].map((p) => (
            <button
              key={p}
              onClick={() => setPatFilter(p)}
              className={`px-3 py-1.5 rounded-full text-xs font-semibold border transition-colors ${
                patFilter === p
                  ? "bg-red-800 border-red-700 text-white"
                  : "bg-slate-900 border-slate-700 text-slate-400 hover:text-white hover:border-red-700"
              }`}
            >
              {p === "all" ? "Tous patterns" : PATTERN_LABELS[p as LandPattern]}
            </button>
          ))}
        </div>
      </div>

      {/* Entity grid */}
      {filtered.length === 0 ? (
        <div className="text-center text-slate-500 py-16">Aucune entité pour ces filtres.</div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          {filtered.map((e) => (
            <EntityCard key={e.entity_id} entity={e} onClick={() => setSelected(e)} />
          ))}
        </div>
      )}
    </div>
  );
}
