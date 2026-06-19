"use client";

import { useState, useEffect } from "react";

interface EntityData {
  entity_id: string;
  finance_domain: string;
  region: string;
  stranded_score: number;
  integrity_score: number;
  gap_score: number;
  systemic_score: number;
  composite_score: number;
  risk_level: string;
  climate_finance_pattern: string;
  severity: string;
  recommended_action: string;
  signal: string;
  stranded_asset_exposure_rate: number;
  climate_finance_gap_severity: number;
}

interface Summary {
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
  avg_estimated_climate_finance_index: number;
}

// ── Color maps ────────────────────────────────────────────────────────────────

const RISK_BG: Record<string, string> = {
  low:      "bg-emerald-500/20 border-emerald-500/30 text-emerald-300",
  moderate: "bg-amber-500/20 border-amber-500/30 text-amber-300",
  high:     "bg-orange-500/20 border-orange-500/30 text-orange-300",
  critical: "bg-rose-500/20 border-rose-500/30 text-rose-300",
};
const RISK_COLOR: Record<string, string> = {
  low:      "#34d399",
  moderate: "#fbbf24",
  high:     "#f97316",
  critical: "#f87171",
};
const RISK_LABEL: Record<string, string> = {
  low:      "Faible",
  moderate: "Modéré",
  high:     "Élevé",
  critical: "Critique",
};
const SEVERITY_BG: Record<string, string> = {
  finance_climatique_sous_surveillance:           "bg-emerald-500/15 text-emerald-300",
  "fragilité_finance_climatique_structurelle":    "bg-amber-500/15 text-amber-300",
  risque_transition_verte_majeur:                 "bg-orange-500/15 text-orange-300",
  "crise_finance_climatique_systémique":          "bg-rose-500/15 text-rose-300",
};
const SEVERITY_LABEL: Record<string, string> = {
  finance_climatique_sous_surveillance:           "Sous Surveillance",
  "fragilité_finance_climatique_structurelle":    "Fragilité Structurelle",
  risque_transition_verte_majeur:                 "Risque Majeur",
  "crise_finance_climatique_systémique":          "Crise Systémique",
};
const ACTION_BG: Record<string, string> = {
  veille_finance_climatique_continue:                   "bg-emerald-500/15 text-emerald-300",
  "renforcement_intégrité_finance_climatique":          "bg-amber-500/15 text-amber-300",
  "réforme_finance_verte_accélérée":                    "bg-orange-500/15 text-orange-300",
  intervention_finance_climatique_urgente:              "bg-rose-500/15 text-rose-300",
};
const ACTION_LABEL: Record<string, string> = {
  veille_finance_climatique_continue:                   "Veille Continue",
  "renforcement_intégrité_finance_climatique":          "Renforcement Intégrité",
  "réforme_finance_verte_accélérée":                    "Réforme Accélérée",
  intervention_finance_climatique_urgente:              "Intervention Urgente",
};
const PATTERN_LABEL: Record<string, string> = {
  none:                      "Aucun",
  stranded_asset_crisis:     "Crise Actifs Échoués",
  green_washing_epidemic:    "Épidémie Greenwashing",
  climate_finance_collapse:  "Effondrement Finance Climatique",
  sovereign_climate_default: "Défaut Souverain Climatique",
  insurance_retreat_cascade: "Cascade Retrait Assurance",
};
const PATTERN_COLOR: Record<string, string> = {
  none:                      "#64748b",
  stranded_asset_crisis:     "#f87171",
  green_washing_epidemic:    "#fb923c",
  climate_finance_collapse:  "#fbbf24",
  sovereign_climate_default: "#a78bfa",
  insurance_retreat_cascade: "#f472b6",
};
const SEVERITY_DIST_COLOR: Record<string, string> = {
  finance_climatique_sous_surveillance:           "#34d399",
  "fragilité_finance_climatique_structurelle":    "#fbbf24",
  risque_transition_verte_majeur:                 "#f97316",
  "crise_finance_climatique_systémique":          "#f87171",
};
const ACTION_DIST_COLOR: Record<string, string> = {
  veille_finance_climatique_continue:             "#34d399",
  "renforcement_intégrité_finance_climatique":    "#fbbf24",
  "réforme_finance_verte_accélérée":              "#f97316",
  intervention_finance_climatique_urgente:        "#f87171",
};

// ── Sub-components ────────────────────────────────────────────────────────────

function GaugeRing({ pct, color, label, size = 90 }: { pct: number; color: string; label: string; size?: number }) {
  const r = size * 0.38;
  const circ = 2 * Math.PI * r;
  const fill = (Math.min(pct, 100) / 100) * circ;
  return (
    <div className="flex flex-col items-center gap-1">
      <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`}>
        <circle cx={size / 2} cy={size / 2} r={r} fill="none" stroke="#1e293b" strokeWidth={size * 0.1} />
        <circle
          cx={size / 2} cy={size / 2} r={r} fill="none"
          stroke={color} strokeWidth={size * 0.1}
          strokeDasharray={`${fill} ${circ}`}
          strokeLinecap="round"
          transform={`rotate(-90 ${size / 2} ${size / 2})`}
        />
        <text x={size / 2} y={size / 2 + 5} textAnchor="middle" fill={color} fontSize={size * 0.20} fontWeight="bold">
          {pct.toFixed(0)}
        </text>
      </svg>
      <span className="text-xs text-slate-400">{label}</span>
    </div>
  );
}

function ScoreBar({ score, label }: { score: number; label: string }) {
  const color = score <= 20 ? "#34d399" : score <= 40 ? "#fbbf24" : score <= 60 ? "#f97316" : "#f87171";
  return (
    <div>
      <div className="flex justify-between mb-1">
        <span className="text-xs text-slate-400">{label}</span>
        <span className="text-xs font-medium" style={{ color }}>{score.toFixed(0)}</span>
      </div>
      <div className="h-1.5 bg-slate-700 rounded-full overflow-hidden">
        <div className="h-full rounded-full transition-all" style={{ width: `${Math.min(score, 100)}%`, backgroundColor: color }} />
      </div>
    </div>
  );
}

function DistBar({ title, counts, colors }: { title: string; counts: Record<string, number>; colors: Record<string, string> }) {
  const total = Object.values(counts).reduce((a, b) => a + b, 0);
  if (!total) return null;
  return (
    <div>
      <p className="text-xs text-slate-400 mb-1">{title}</p>
      <div className="flex h-2 rounded-full overflow-hidden gap-px">
        {Object.entries(counts).map(([k, v]) =>
          v > 0 ? (
            <div key={k} style={{ width: `${(v / total) * 100}%`, backgroundColor: colors[k] ?? "#94a3b8" }} title={`${k}: ${v}`} />
          ) : null
        )}
      </div>
      <div className="flex flex-wrap gap-2 mt-1.5">
        {Object.entries(counts).map(([k, v]) => (
          <span key={k} className="text-xs" style={{ color: colors[k] ?? "#94a3b8" }}>
            {k}: {v}
          </span>
        ))}
      </div>
    </div>
  );
}

// ── Detail Modal ──────────────────────────────────────────────────────────────

function DetailModal({ entity, onClose }: { entity: EntityData; onClose: () => void }) {
  const [tab, setTab] = useState<"scores" | "signal" | "action">("scores");
  const riskColor = RISK_COLOR[entity.risk_level] ?? "#94a3b8";

  useEffect(() => {
    const handler = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [onClose]);

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4"
      onClick={(e) => { if (e.currentTarget === e.target) onClose(); }}
    >
      <div className="bg-slate-900 border border-green-900/40 rounded-xl shadow-2xl w-full max-w-lg">
        <div className="flex items-start justify-between p-5 border-b border-slate-800">
          <div>
            <div className="flex items-center gap-2 mb-1 flex-wrap">
              <span className={`text-xs px-2 py-0.5 rounded-full border font-medium ${RISK_BG[entity.risk_level] ?? ""}`}>
                {RISK_LABEL[entity.risk_level] ?? entity.risk_level}
              </span>
              <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${SEVERITY_BG[entity.severity] ?? "bg-slate-700 text-slate-300"}`}>
                {SEVERITY_LABEL[entity.severity] ?? entity.severity}
              </span>
            </div>
            <h2 className="text-white font-bold text-lg">{entity.entity_id}</h2>
            <p className="text-slate-400 text-sm">
              {entity.finance_domain} · {entity.region} · Composite:{" "}
              <span style={{ color: riskColor }}>{entity.composite_score}</span>
            </p>
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-white p-1 transition-colors" aria-label="Fermer">
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <div className="flex border-b border-slate-800">
          {(["scores", "signal", "action"] as const).map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`flex-1 py-2.5 text-sm font-medium capitalize transition-colors ${
                tab === t
                  ? "text-green-400 border-b-2 border-green-500 bg-slate-800/40"
                  : "text-slate-400 hover:text-slate-200"
              }`}
            >
              {t === "scores" ? "Scores" : t === "signal" ? "Signal" : "Action"}
            </button>
          ))}
        </div>

        <div className="p-5 space-y-4">
          {tab === "scores" && (
            <div className="space-y-3">
              <ScoreBar score={entity.stranded_score}   label="Actifs Échoués (30%)" />
              <ScoreBar score={entity.integrity_score}  label="Intégrité (25%)" />
              <ScoreBar score={entity.gap_score}        label="Écart Financement (25%)" />
              <ScoreBar score={entity.systemic_score}   label="Systémique (20%)" />
              <div className="pt-2 border-t border-slate-800">
                <div className="flex justify-between items-center">
                  <span className="text-sm text-slate-400">Composite Finance Climatique</span>
                  <span className="text-lg font-bold" style={{ color: riskColor }}>{entity.composite_score}</span>
                </div>
                <p className="text-xs text-slate-500 mt-1">Score composite risque finance climatique (0–100)</p>
              </div>
              <div className="grid grid-cols-2 gap-3 pt-1">
                <div className="bg-slate-800/50 rounded-lg p-3">
                  <p className="text-xs text-slate-400">Exposition Actifs Échoués</p>
                  <p className="text-lg font-bold text-green-400">{(entity.stranded_asset_exposure_rate * 100).toFixed(0)}%</p>
                </div>
                <div className="bg-slate-800/50 rounded-lg p-3">
                  <p className="text-xs text-slate-400">Sévérité Écart Finance</p>
                  <p className="text-lg font-bold text-green-400">{(entity.climate_finance_gap_severity * 100).toFixed(0)}%</p>
                </div>
              </div>
            </div>
          )}

          {tab === "signal" && (
            <>
              <div className="flex items-center justify-center py-2">
                <GaugeRing pct={entity.composite_score} color={riskColor} label="Composite" size={110} />
              </div>
              <div className="bg-slate-800/50 rounded-lg p-3">
                <p className="text-xs text-slate-400 mb-1">Signal Finance Climatique</p>
                <p className="text-sm text-white">{entity.signal}</p>
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div className="bg-slate-800/50 rounded-lg p-3">
                  <p className="text-xs text-slate-400">Pattern</p>
                  <p className="text-sm font-medium" style={{ color: PATTERN_COLOR[entity.climate_finance_pattern] ?? "#94a3b8" }}>
                    {PATTERN_LABEL[entity.climate_finance_pattern] ?? entity.climate_finance_pattern}
                  </p>
                </div>
                <div className="bg-slate-800/50 rounded-lg p-3">
                  <p className="text-xs text-slate-400">Sévérité</p>
                  <p className="text-sm font-medium text-slate-200">{SEVERITY_LABEL[entity.severity] ?? entity.severity}</p>
                </div>
              </div>
            </>
          )}

          {tab === "action" && (
            <div className="space-y-4">
              <div className="bg-slate-800/50 rounded-lg p-4">
                <p className="text-xs text-slate-400 mb-2">Action Recommandée</p>
                <span className={`text-sm px-3 py-1.5 rounded-lg font-medium ${ACTION_BG[entity.recommended_action] ?? "bg-slate-700 text-slate-300"}`}>
                  {ACTION_LABEL[entity.recommended_action] ?? entity.recommended_action}
                </span>
              </div>
              <div className="space-y-2">
                <div className="flex justify-between p-2 rounded bg-slate-800/40">
                  <span className="text-xs text-slate-400">Pattern finance climatique</span>
                  <span className="text-xs text-slate-200">{PATTERN_LABEL[entity.climate_finance_pattern] ?? entity.climate_finance_pattern}</span>
                </div>
                <div className="flex justify-between p-2 rounded bg-slate-800/40">
                  <span className="text-xs text-slate-400">Sévérité</span>
                  <span className="text-xs text-slate-200">{SEVERITY_LABEL[entity.severity] ?? entity.severity}</span>
                </div>
                <div className="flex justify-between p-2 rounded bg-slate-800/40">
                  <span className="text-xs text-slate-400">Exposition actifs échoués</span>
                  <span className="text-xs text-green-400 font-medium">{(entity.stranded_asset_exposure_rate * 100).toFixed(0)}%</span>
                </div>
                <div className="flex justify-between p-2 rounded bg-slate-800/40">
                  <span className="text-xs text-slate-400">Sévérité écart financement</span>
                  <span className="text-xs text-green-400 font-medium">{(entity.climate_finance_gap_severity * 100).toFixed(0)}%</span>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

// ── Filter constants ──────────────────────────────────────────────────────────

const RISK_FILTERS = ["all", "low", "moderate", "high", "critical"] as const;
type RiskFilter = typeof RISK_FILTERS[number];

// ── Main page ─────────────────────────────────────────────────────────────────

export default function ClimateFinanceEnginePage() {
  const [data, setData] = useState<{ entities: EntityData[]; summary: Summary } | null>(null);
  const [loading, setLoading] = useState(true);
  const [riskFilter, setRiskFilter] = useState<RiskFilter>("all");
  const [selected, setSelected] = useState<EntityData | null>(null);

  useEffect(() => {
    async function fetchData() {
      setLoading(true);
      try {
        const res = await fetch("/api/climate-finance-engine");
        const json = await res.json() as { entities: EntityData[]; summary: Summary };
        setData(json);
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, []);

  const s = data?.summary;
  const allEntities = data?.entities ?? [];
  const entities = riskFilter === "all" ? allEntities : allEntities.filter((e) => e.risk_level === riskFilter);

  // Compute avg sub-scores for gauges
  const n = allEntities.length;
  const avgStranded  = n > 0 ? allEntities.reduce((acc, e) => acc + e.stranded_score,  0) / n : 0;
  const avgIntegrity = n > 0 ? allEntities.reduce((acc, e) => acc + e.integrity_score, 0) / n : 0;
  const avgGap       = n > 0 ? allEntities.reduce((acc, e) => acc + e.gap_score,        0) / n : 0;
  const avgSystemic  = n > 0 ? allEntities.reduce((acc, e) => acc + e.systemic_score,   0) / n : 0;

  const avgStrandedRate = n > 0 ? allEntities.reduce((acc, e) => acc + e.stranded_asset_exposure_rate, 0) / n : 0;

  const riskDistColors: Record<string, string> = {
    low: "#34d399", moderate: "#fbbf24", high: "#f97316", critical: "#f87171",
  };

  const distributions = [
    { title: "Distribution Risque",    counts: s?.risk_distribution     ?? {}, colors: riskDistColors },
    { title: "Distribution Pattern",   counts: s?.pattern_distribution  ?? {}, colors: PATTERN_COLOR },
    { title: "Distribution Sévérité",  counts: s?.severity_distribution ?? {}, colors: SEVERITY_DIST_COLOR },
    { title: "Distribution Action",    counts: s?.action_distribution   ?? {}, colors: ACTION_DIST_COLOR },
  ];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
      {selected && <DetailModal entity={selected} onClose={() => setSelected(null)} />}

      {/* Header */}
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-green-400">
          Finance Climatique &amp; Risques Transition Verte — Module 359
        </h1>
        <p className="text-slate-400 text-sm mt-1">
          Actifs Échoués · Intégrité · Écart Financement · Systémique — détection des risques finance climatique et transition verte
        </p>
      </div>

      {/* KPI Strip — 6 cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 xl:grid-cols-6 gap-4 mb-6">
        <div className="bg-slate-900 border border-green-900/30 rounded-xl p-4">
          <p className="text-xs text-slate-400 mb-1">Total Systèmes</p>
          <p className="text-2xl font-bold text-white">{s?.total_entities ?? "—"}</p>
        </div>
        <div className="bg-slate-900 border border-green-900/30 rounded-xl p-4">
          <p className="text-xs text-slate-400 mb-1">Crise Climatique</p>
          <p className="text-2xl font-bold text-rose-400">{s?.critical_count ?? "—"}</p>
        </div>
        <div className="bg-slate-900 border border-green-900/30 rounded-xl p-4">
          <p className="text-xs text-slate-400 mb-1">Risque Majeur</p>
          <p className="text-2xl font-bold text-orange-400">{s?.high_count ?? "—"}</p>
        </div>
        <div className="bg-slate-900 border border-green-900/30 rounded-xl p-4">
          <p className="text-xs text-slate-400 mb-1">Composite Moyen</p>
          <p className="text-2xl font-bold text-yellow-400">{s?.avg_composite ?? "—"}</p>
        </div>
        <div className="bg-slate-900 border border-green-900/30 rounded-xl p-4">
          <p className="text-xs text-slate-400 mb-1">Index Finance Climatique</p>
          <p className="text-2xl font-bold text-green-400">{s?.avg_estimated_climate_finance_index ?? "—"}</p>
        </div>
        <div className="bg-slate-900 border border-green-900/30 rounded-xl p-4">
          <p className="text-xs text-slate-400 mb-1">Actifs Échoués Moyen</p>
          <p className="text-2xl font-bold text-emerald-300">{n > 0 ? (avgStrandedRate * 100).toFixed(1) + "%" : "—"}</p>
        </div>
      </div>

      {/* Gauge Rings — 4 sub-scores */}
      <div className="bg-slate-900 border border-green-900/30 rounded-xl p-5 mb-6">
        <h3 className="text-sm font-semibold text-green-300 mb-4">Scores Moyens — Dimensions Finance Climatique</h3>
        <div className="flex flex-wrap justify-around gap-6">
          <GaugeRing pct={avgStranded}  color="#34d399" label="Actifs Échoués" />
          <GaugeRing pct={avgIntegrity} color="#a3e635" label="Intégrité" />
          <GaugeRing pct={avgGap}       color="#fbbf24" label="Écart" />
          <GaugeRing pct={avgSystemic}  color="#f97316" label="Systémique" />
        </div>
      </div>

      {/* Distribution bars */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
        {distributions.map((d) => (
          <div key={d.title} className="bg-slate-900 border border-green-900/30 rounded-xl p-4">
            <DistBar title={d.title} counts={d.counts} colors={d.colors} />
          </div>
        ))}
      </div>

      {/* Filter pills */}
      <div className="mb-4">
        <div className="flex flex-wrap gap-2 items-center">
          <span className="text-xs text-slate-500 mr-1">Risque:</span>
          {RISK_FILTERS.map((f) => (
            <button
              key={f}
              onClick={() => setRiskFilter(f)}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors border ${
                riskFilter === f
                  ? "bg-green-800 border-green-600 text-white"
                  : "bg-slate-800 border-slate-700 text-slate-400 hover:text-white hover:border-green-700"
              }`}
            >
              {f === "all" ? "Tous" : RISK_LABEL[f] ?? f}
              {f !== "all" && s?.risk_distribution?.[f] !== undefined && (
                <span className="ml-1 opacity-70">({s.risk_distribution[f]})</span>
              )}
            </button>
          ))}
        </div>
      </div>

      {/* Entity cards */}
      {loading ? (
        <div className="flex items-center justify-center h-48">
          <div className="w-8 h-8 border-2 border-green-500 border-t-transparent rounded-full animate-spin" />
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
          {entities.map((entity) => {
            const color = RISK_COLOR[entity.risk_level] ?? "#94a3b8";
            return (
              <div
                key={entity.entity_id}
                onClick={() => setSelected(entity)}
                className="bg-slate-900 border border-slate-800 rounded-xl p-4 cursor-pointer hover:border-green-700 transition-all hover:bg-slate-800/60"
              >
                <div className="flex items-start justify-between mb-3">
                  <div className="flex-1 min-w-0 pr-2">
                    <div className="flex items-center gap-2 mb-1 flex-wrap">
                      <span className={`text-xs px-2 py-0.5 rounded-full border font-medium ${RISK_BG[entity.risk_level] ?? ""}`}>
                        {RISK_LABEL[entity.risk_level] ?? entity.risk_level}
                      </span>
                      {entity.climate_finance_pattern !== "none" && (
                        <span
                          className="text-xs px-2 py-0.5 rounded-full font-medium bg-slate-800 border border-slate-700"
                          style={{ color: PATTERN_COLOR[entity.climate_finance_pattern] ?? "#94a3b8" }}
                        >
                          {PATTERN_LABEL[entity.climate_finance_pattern] ?? entity.climate_finance_pattern}
                        </span>
                      )}
                    </div>
                    <h3 className="text-white font-semibold text-sm">{entity.entity_id}</h3>
                    <p className="text-slate-400 text-xs">{entity.finance_domain} · {entity.region}</p>
                  </div>
                  <div className="flex-shrink-0">
                    <GaugeRing pct={entity.composite_score} color={color} label="" size={72} />
                  </div>
                </div>

                <div className="space-y-1.5 mb-3">
                  <ScoreBar score={entity.stranded_score}   label="Actifs Échoués" />
                  <ScoreBar score={entity.integrity_score}  label="Intégrité" />
                  <ScoreBar score={entity.gap_score}        label="Écart Financement" />
                  <ScoreBar score={entity.systemic_score}   label="Systémique" />
                </div>

                <div className="border-t border-slate-800 pt-2 flex items-center justify-between gap-2 flex-wrap">
                  <span className={`text-xs px-2 py-0.5 rounded font-medium ${ACTION_BG[entity.recommended_action] ?? "bg-slate-700 text-slate-300"}`}>
                    {ACTION_LABEL[entity.recommended_action] ?? entity.recommended_action}
                  </span>
                  <span className="text-xs text-green-400 font-medium">
                    échoués {(entity.stranded_asset_exposure_rate * 100).toFixed(0)}%
                  </span>
                </div>
                <div className="flex items-center gap-1.5 mt-2">
                  <span className={`text-xs px-1.5 py-0.5 rounded font-medium ${SEVERITY_BG[entity.severity] ?? "bg-slate-700 text-slate-300"}`}>
                    {SEVERITY_LABEL[entity.severity] ?? entity.severity}
                  </span>
                </div>
                <p className="text-xs text-slate-500 mt-1.5 truncate">{entity.signal}</p>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
