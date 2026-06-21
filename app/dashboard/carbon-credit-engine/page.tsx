"use client";

import { useState, useEffect } from "react";

interface EntityData {
  id: string;
  market_type: string;
  region: string;
  fraud_score: number;
  greenwash_score: number;
  systemic_score: number;
  manipulation_score: number;
  composite_score: number;
  risk_level: string;
  carbon_credit_pattern: string;
  severity: string;
  recommended_action: string;
  signal: string;
  fraud_prevalence: number;
  greenwashing_integration: number;
}

interface Summary {
  module_id: number;
  module_name: string;
  total: number;
  critical: number;
  high: number;
  moderate: number;
  low: number;
  avg_composite: number;
  distributions: Record<string, number>;
  avg_estimated_carbon_fraud_index: number;
  risk_distribution: Record<string, number>;
  severity_distribution: Record<string, number>;
  action_distribution: Record<string, number>;
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
  "marché_carbone_sous_surveillance":                    "bg-emerald-500/15 text-emerald-300",
  "fragilité_intégrité_crédit_carbone_structurelle":     "bg-amber-500/15 text-amber-300",
  "risque_manipulation_marché_carbone_majeur":           "bg-orange-500/15 text-orange-300",
  "crise_fraude_carbone_systémique":                     "bg-rose-500/15 text-rose-300",
};
const SEVERITY_LABEL: Record<string, string> = {
  "marché_carbone_sous_surveillance":                    "Sous Surveillance",
  "fragilité_intégrité_crédit_carbone_structurelle":     "Fragilité Structurelle",
  "risque_manipulation_marché_carbone_majeur":           "Risque Majeur",
  "crise_fraude_carbone_systémique":                     "Crise Systémique",
};
const ACTION_BG: Record<string, string> = {
  "veille_marché_carbone_continue":            "bg-emerald-500/15 text-emerald-300",
  "renforcement_vérification_crédit_carbone":  "bg-amber-500/15 text-amber-300",
  "audit_marché_carbone_accéléré":             "bg-orange-500/15 text-orange-300",
  "intervention_fraude_carbone_urgente":       "bg-rose-500/15 text-rose-300",
};
const ACTION_LABEL: Record<string, string> = {
  "veille_marché_carbone_continue":            "Veille Continue",
  "renforcement_vérification_crédit_carbone":  "Renforcement Vérification",
  "audit_marché_carbone_accéléré":             "Audit Accéléré",
  "intervention_fraude_carbone_urgente":       "Intervention Urgente",
};
const PATTERN_LABEL: Record<string, string> = {
  none:                          "Aucun",
  systematic_carbon_fraud:       "Fraude Carbone Systématique",
  REDD_ecosystem_collapse:       "Effondrement REDD+",
  corporate_greenwashing_empire: "Empire Greenwashing Corporatif",
  market_manipulation_capture:   "Capture Manipulation Marché",
  standard_regulatory_capture:   "Capture Réglementaire Standard",
};
const PATTERN_COLOR: Record<string, string> = {
  none:                          "#64748b",
  systematic_carbon_fraud:       "#f87171",
  REDD_ecosystem_collapse:       "#fb923c",
  corporate_greenwashing_empire: "#fbbf24",
  market_manipulation_capture:   "#a78bfa",
  standard_regulatory_capture:   "#f472b6",
};
const SEVERITY_DIST_COLOR: Record<string, string> = {
  "marché_carbone_sous_surveillance":                    "#34d399",
  "fragilité_intégrité_crédit_carbone_structurelle":     "#fbbf24",
  "risque_manipulation_marché_carbone_majeur":           "#f97316",
  "crise_fraude_carbone_systémique":                     "#f87171",
};
const ACTION_DIST_COLOR: Record<string, string> = {
  "veille_marché_carbone_continue":            "#34d399",
  "renforcement_vérification_crédit_carbone":  "#fbbf24",
  "audit_marché_carbone_accéléré":             "#f97316",
  "intervention_fraude_carbone_urgente":       "#f87171",
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
            <h2 className="text-white font-bold text-lg">{entity.id}</h2>
            <p className="text-slate-400 text-sm">
              {entity.market_type} · {entity.region} · Composite:{" "}
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
              <ScoreBar score={entity.fraud_score}        label="Fraude (30%)" />
              <ScoreBar score={entity.greenwash_score}    label="Greenwashing (25%)" />
              <ScoreBar score={entity.systemic_score}     label="Systémique (25%)" />
              <ScoreBar score={entity.manipulation_score} label="Manipulation (20%)" />
              <div className="pt-2 border-t border-slate-800">
                <div className="flex justify-between items-center">
                  <span className="text-sm text-slate-400">Composite Fraude Carbone</span>
                  <span className="text-lg font-bold" style={{ color: riskColor }}>{entity.composite_score}</span>
                </div>
                <p className="text-xs text-slate-500 mt-1">Score composite fraude marché carbone (0–100)</p>
              </div>
              <div className="grid grid-cols-2 gap-3 pt-1">
                <div className="bg-slate-800/50 rounded-lg p-3">
                  <p className="text-xs text-slate-400">Prévalence Fraude</p>
                  <p className="text-lg font-bold text-green-400">{(entity.fraud_prevalence * 100).toFixed(0)}%</p>
                </div>
                <div className="bg-slate-800/50 rounded-lg p-3">
                  <p className="text-xs text-slate-400">Intégration Greenwashing</p>
                  <p className="text-lg font-bold text-green-400">{(entity.greenwashing_integration * 100).toFixed(0)}%</p>
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
                <p className="text-xs text-slate-400 mb-1">Signal Fraude Carbone</p>
                <p className="text-sm text-white">{entity.signal}</p>
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div className="bg-slate-800/50 rounded-lg p-3">
                  <p className="text-xs text-slate-400">Pattern</p>
                  <p className="text-sm font-medium" style={{ color: PATTERN_COLOR[entity.carbon_credit_pattern] ?? "#94a3b8" }}>
                    {PATTERN_LABEL[entity.carbon_credit_pattern] ?? entity.carbon_credit_pattern}
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
                  <span className="text-xs text-slate-400">Pattern fraude carbone</span>
                  <span className="text-xs text-slate-200">{PATTERN_LABEL[entity.carbon_credit_pattern] ?? entity.carbon_credit_pattern}</span>
                </div>
                <div className="flex justify-between p-2 rounded bg-slate-800/40">
                  <span className="text-xs text-slate-400">Sévérité</span>
                  <span className="text-xs text-slate-200">{SEVERITY_LABEL[entity.severity] ?? entity.severity}</span>
                </div>
                <div className="flex justify-between p-2 rounded bg-slate-800/40">
                  <span className="text-xs text-slate-400">Prévalence fraude</span>
                  <span className="text-xs text-green-400 font-medium">{(entity.fraud_prevalence * 100).toFixed(0)}%</span>
                </div>
                <div className="flex justify-between p-2 rounded bg-slate-800/40">
                  <span className="text-xs text-slate-400">Intégration greenwashing</span>
                  <span className="text-xs text-green-400 font-medium">{(entity.greenwashing_integration * 100).toFixed(0)}%</span>
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

export default function CarbonCreditEnginePage() {
  const [data, setData] = useState<{ entities: EntityData[]; summary: Summary } | null>(null);
  const [loading, setLoading] = useState(true);
  const [riskFilter, setRiskFilter] = useState<RiskFilter>("all");
  const [selected, setSelected] = useState<EntityData | null>(null);

  useEffect(() => {
    async function fetchData() {
      setLoading(true);
      try {
        const res = await fetch("/api/carbon-credit-engine");
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
  const avgFraud        = n > 0 ? allEntities.reduce((acc, e) => acc + e.fraud_score,        0) / n : 0;
  const avgGreenwash    = n > 0 ? allEntities.reduce((acc, e) => acc + e.greenwash_score,    0) / n : 0;
  const avgSystemic     = n > 0 ? allEntities.reduce((acc, e) => acc + e.systemic_score,     0) / n : 0;
  const avgManipulation = n > 0 ? allEntities.reduce((acc, e) => acc + e.manipulation_score, 0) / n : 0;

  const avgFraudPrev = n > 0 ? allEntities.reduce((acc, e) => acc + e.fraud_prevalence, 0) / n : 0;

  const riskDistColors: Record<string, string> = {
    low: "#34d399", moderate: "#fbbf24", high: "#f97316", critical: "#f87171",
  };

  const distributions = [
    { title: "Distribution Risque",    counts: s?.risk_distribution     ?? {}, colors: riskDistColors },
    { title: "Distribution Pattern",   counts: s?.distributions         ?? {}, colors: PATTERN_COLOR },
    { title: "Distribution Sévérité",  counts: s?.severity_distribution ?? {}, colors: SEVERITY_DIST_COLOR },
    { title: "Distribution Action",    counts: s?.action_distribution   ?? {}, colors: ACTION_DIST_COLOR },
  ];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
      {selected && <DetailModal entity={selected} onClose={() => setSelected(null)} />}

      {/* Header */}
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-green-400">
          Marchés Carbone &amp; Fraude Climatique — Module 369
        </h1>
        <p className="text-slate-400 text-sm mt-1">
          Fraude · Greenwashing · Systémique · Manipulation — détection des fraudes marchés carbone et finance climatique
        </p>
      </div>

      {/* KPI Strip — 6 cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 xl:grid-cols-6 gap-4 mb-6">
        <div className="bg-slate-900 border border-green-900/30 rounded-xl p-4">
          <p className="text-xs text-slate-400 mb-1">Total Marchés</p>
          <p className="text-2xl font-bold text-white">{s?.total ?? "—"}</p>
        </div>
        <div className="bg-slate-900 border border-green-900/30 rounded-xl p-4">
          <p className="text-xs text-slate-400 mb-1">Fraude Systémique</p>
          <p className="text-2xl font-bold text-rose-400">{s?.critical ?? "—"}</p>
        </div>
        <div className="bg-slate-900 border border-green-900/30 rounded-xl p-4">
          <p className="text-xs text-slate-400 mb-1">Manipulation Majeure</p>
          <p className="text-2xl font-bold text-orange-400">{s?.high ?? "—"}</p>
        </div>
        <div className="bg-slate-900 border border-green-900/30 rounded-xl p-4">
          <p className="text-xs text-slate-400 mb-1">Composite Moyen</p>
          <p className="text-2xl font-bold text-yellow-400">{s?.avg_composite ?? "—"}</p>
        </div>
        <div className="bg-slate-900 border border-green-900/30 rounded-xl p-4">
          <p className="text-xs text-slate-400 mb-1">Index Fraude Carbone</p>
          <p className="text-2xl font-bold text-green-400">{s?.avg_estimated_carbon_fraud_index ?? "—"}</p>
        </div>
        <div className="bg-slate-900 border border-green-900/30 rounded-xl p-4">
          <p className="text-xs text-slate-400 mb-1">Fraude Moyenne</p>
          <p className="text-2xl font-bold text-emerald-300">{n > 0 ? (avgFraudPrev * 100).toFixed(1) + "%" : "—"}</p>
        </div>
      </div>

      {/* Gauge Rings — 4 sub-scores */}
      <div className="bg-slate-900 border border-green-900/30 rounded-xl p-5 mb-6">
        <h3 className="text-sm font-semibold text-green-300 mb-4">Scores Moyens — Dimensions Fraude Carbone</h3>
        <div className="flex flex-wrap justify-around gap-6">
          <GaugeRing pct={avgFraud}        color="#f87171" label="Fraude" />
          <GaugeRing pct={avgGreenwash}    color="#fbbf24" label="Greenwashing" />
          <GaugeRing pct={avgSystemic}     color="#f97316" label="Systémique" />
          <GaugeRing pct={avgManipulation} color="#a78bfa" label="Manipulation" />
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
                key={entity.id}
                onClick={() => setSelected(entity)}
                className="bg-slate-900 border border-slate-800 rounded-xl p-4 cursor-pointer hover:border-green-700 transition-all hover:bg-slate-800/60"
              >
                <div className="flex items-start justify-between mb-3">
                  <div className="flex-1 min-w-0 pr-2">
                    <div className="flex items-center gap-2 mb-1 flex-wrap">
                      <span className={`text-xs px-2 py-0.5 rounded-full border font-medium ${RISK_BG[entity.risk_level] ?? ""}`}>
                        {RISK_LABEL[entity.risk_level] ?? entity.risk_level}
                      </span>
                      {entity.carbon_credit_pattern !== "none" && (
                        <span
                          className="text-xs px-2 py-0.5 rounded-full font-medium bg-slate-800 border border-slate-700"
                          style={{ color: PATTERN_COLOR[entity.carbon_credit_pattern] ?? "#94a3b8" }}
                        >
                          {PATTERN_LABEL[entity.carbon_credit_pattern] ?? entity.carbon_credit_pattern}
                        </span>
                      )}
                    </div>
                    <h3 className="text-white font-semibold text-sm">{entity.id}</h3>
                    <p className="text-slate-400 text-xs">{entity.market_type} · {entity.region}</p>
                  </div>
                  <div className="flex-shrink-0">
                    <GaugeRing pct={entity.composite_score} color={color} label="" size={72} />
                  </div>
                </div>

                <div className="space-y-1.5 mb-3">
                  <ScoreBar score={entity.fraud_score}        label="Fraude" />
                  <ScoreBar score={entity.greenwash_score}    label="Greenwashing" />
                  <ScoreBar score={entity.systemic_score}     label="Systémique" />
                  <ScoreBar score={entity.manipulation_score} label="Manipulation" />
                </div>

                <div className="border-t border-slate-800 pt-2 flex items-center justify-between gap-2 flex-wrap">
                  <span className={`text-xs px-2 py-0.5 rounded font-medium ${ACTION_BG[entity.recommended_action] ?? "bg-slate-700 text-slate-300"}`}>
                    {ACTION_LABEL[entity.recommended_action] ?? entity.recommended_action}
                  </span>
                  <span className="text-xs text-green-400 font-medium">
                    fraude {(entity.fraud_prevalence * 100).toFixed(0)}%
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
