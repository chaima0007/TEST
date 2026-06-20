"use client";

import { useState, useEffect } from "react";

// ── Types ─────────────────────────────────────────────────────────────────────

interface EntityData {
  entity_id: string;
  name: string;
  country: string;
  sector: string;
  composite_score: number;
  impact_measurement_deficit_score: number;
  greenwashing_risk_score: number;
  investor_trust_erosion_score: number;
  regulatory_compliance_gap_score: number;
  risk_level: string;
  primary_pattern: string;
  key_signals: string[];
  estimated_bond_index: number;
  last_updated: string;
  confidence_level: number;
}

interface SummaryData {
  total_entities: number;
  avg_composite: number;
  risk_distribution: Record<string, number>;
  pattern_distribution: Record<string, number>;
  top_risk_entities: string[];
  critical_alerts: string[];
  last_analysis: string;
  engine_version: string;
  domain: string;
  confidence_score: number;
  data_sources: string[];
  entities: EntityData[];
  avg_estimated_bond_index: number;
}

// ── Color maps ────────────────────────────────────────────────────────────────

const RISK_BG: Record<string, string> = {
  faible:   "bg-emerald-500/20 border-emerald-500/30 text-emerald-300",
  "modéré": "bg-amber-500/20 border-amber-500/30 text-amber-300",
  "élevé":  "bg-orange-500/20 border-orange-500/30 text-orange-300",
  critique: "bg-rose-500/20 border-rose-500/30 text-rose-300",
};

const RISK_COLOR: Record<string, string> = {
  faible:   "#34d399",
  "modéré": "#fbbf24",
  "élevé":  "#f97316",
  critique: "#f87171",
};

const RISK_LABEL: Record<string, string> = {
  faible:   "Faible",
  "modéré": "Modéré",
  "élevé":  "Élevé",
  critique: "Critique",
};

const PATTERN_LABEL: Record<string, string> = {
  impact_fraud:                 "Fraude à l'Impact Social",
  social_washing:               "Social Washing Systémique",
  investor_confidence_collapse: "Effondrement Confiance Investisseurs",
  regulatory_breach:            "Violation Réglementaire ESG",
  bond_performing:              "Obligation Sociale Performante",
};

const PATTERN_COLOR: Record<string, string> = {
  impact_fraud:                 "#f87171",
  social_washing:               "#fb923c",
  investor_confidence_collapse: "#fbbf24",
  regulatory_breach:            "#a78bfa",
  bond_performing:              "#34d399",
};

// ── GaugeRing ─────────────────────────────────────────────────────────────────

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
      {label && <span className="text-xs text-slate-400">{label}</span>}
    </div>
  );
}

// ── DistBar ───────────────────────────────────────────────────────────────────

function DistBar({ label, value, total, color }: { label: string; value: number; total: number; color: string }) {
  const pct = total > 0 ? (value / total) * 100 : 0;
  return (
    <div className="flex items-center gap-2">
      <span className="text-xs text-slate-400 w-24 shrink-0 truncate">{label}</span>
      <div className="flex-1 h-2 bg-slate-800 rounded-full overflow-hidden">
        <div
          className="h-full rounded-full transition-all"
          style={{ width: `${pct}%`, backgroundColor: color }}
        />
      </div>
      <span className="text-xs font-medium shrink-0" style={{ color }}>{value}</span>
    </div>
  );
}

// ── ScoreBar ──────────────────────────────────────────────────────────────────

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

// ── DetailModal ───────────────────────────────────────────────────────────────

function DetailModal({ entity, onClose }: { entity: EntityData; onClose: () => void }) {
  const [tab, setTab] = useState<"scores" | "signaux" | "actions">("scores");
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
      <div className="bg-slate-900 border border-blue-900/40 rounded-xl shadow-2xl w-full max-w-lg">
        {/* Header */}
        <div className="flex items-start justify-between p-5 border-b border-slate-800">
          <div>
            <div className="flex items-center gap-2 mb-1 flex-wrap">
              <span className={`text-xs px-2 py-0.5 rounded-full border font-medium ${RISK_BG[entity.risk_level] ?? ""}`}>
                {RISK_LABEL[entity.risk_level] ?? entity.risk_level}
              </span>
              <span
                className="text-xs px-2 py-0.5 rounded-full font-medium bg-slate-800 border border-slate-700"
                style={{ color: PATTERN_COLOR[entity.primary_pattern] ?? "#94a3b8" }}
              >
                {PATTERN_LABEL[entity.primary_pattern] ?? entity.primary_pattern}
              </span>
            </div>
            <h2 className="text-white font-bold text-lg">{entity.entity_id}</h2>
            <p className="text-slate-300 text-sm font-medium">{entity.name}</p>
            <p className="text-slate-400 text-xs mt-0.5">
              {entity.country} · {entity.sector} · Composite:{" "}
              <span style={{ color: riskColor }}>{entity.composite_score}</span>
            </p>
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-white p-1 transition-colors" aria-label="Fermer">
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        {/* Tabs */}
        <div className="flex border-b border-slate-800">
          {(["scores", "signaux", "actions"] as const).map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`flex-1 py-2.5 text-sm font-medium capitalize transition-colors ${
                tab === t
                  ? "text-blue-400 border-b-2 border-blue-500 bg-slate-800/40"
                  : "text-slate-400 hover:text-slate-200"
              }`}
            >
              {t.charAt(0).toUpperCase() + t.slice(1)}
            </button>
          ))}
        </div>

        {/* Tab content */}
        <div className="p-5 space-y-4">
          {tab === "scores" && (
            <div className="space-y-3">
              <ScoreBar score={entity.impact_measurement_deficit_score} label="Déficit Mesure Impact (30%)" />
              <ScoreBar score={entity.greenwashing_risk_score}          label="Risque Greenwashing (25%)" />
              <ScoreBar score={entity.investor_trust_erosion_score}     label="Érosion Confiance Investisseurs (25%)" />
              <ScoreBar score={entity.regulatory_compliance_gap_score}  label="Écart Conformité Réglementaire (20%)" />
              <div className="pt-2 border-t border-slate-800">
                <div className="flex justify-between items-center">
                  <span className="text-sm text-slate-400">Score Composite Obligation Sociale</span>
                  <span className="text-lg font-bold" style={{ color: riskColor }}>{entity.composite_score}</span>
                </div>
                <p className="text-xs text-slate-500 mt-1">Indice de risque obligation sociale (0–100)</p>
              </div>
              <div className="grid grid-cols-2 gap-3 pt-1">
                <div className="bg-slate-800/50 rounded-lg p-3">
                  <p className="text-xs text-slate-400">Index Obligataire</p>
                  <p className="text-lg font-bold text-blue-400">{entity.estimated_bond_index}</p>
                </div>
                <div className="bg-slate-800/50 rounded-lg p-3">
                  <p className="text-xs text-slate-400">Niveau de Confiance</p>
                  <p className="text-lg font-bold text-blue-400">{(entity.confidence_level * 100).toFixed(0)}%</p>
                </div>
              </div>
            </div>
          )}

          {tab === "signaux" && (
            <>
              <div className="flex items-center justify-center py-2">
                <GaugeRing pct={entity.composite_score} color={riskColor} label="Composite" size={110} />
              </div>
              <div className="space-y-2">
                {entity.key_signals.map((signal, i) => (
                  <div key={i} className="bg-slate-800/50 rounded-lg p-3">
                    <p className="text-xs text-slate-400 mb-0.5">Signal {i + 1}</p>
                    <p className="text-sm text-white">{signal}</p>
                  </div>
                ))}
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div className="bg-slate-800/50 rounded-lg p-3">
                  <p className="text-xs text-slate-400">Pattern</p>
                  <p className="text-sm font-medium" style={{ color: PATTERN_COLOR[entity.primary_pattern] ?? "#94a3b8" }}>
                    {PATTERN_LABEL[entity.primary_pattern] ?? entity.primary_pattern}
                  </p>
                </div>
                <div className="bg-slate-800/50 rounded-lg p-3">
                  <p className="text-xs text-slate-400">Dernière Analyse</p>
                  <p className="text-sm font-medium text-slate-200">{entity.last_updated}</p>
                </div>
              </div>
            </>
          )}

          {tab === "actions" && (
            <div className="space-y-4">
              <div className="bg-slate-800/50 rounded-lg p-4">
                <p className="text-xs text-slate-400 mb-2">Pattern Détecté</p>
                <span
                  className="text-sm px-3 py-1.5 rounded-lg font-medium bg-slate-700"
                  style={{ color: PATTERN_COLOR[entity.primary_pattern] ?? "#94a3b8" }}
                >
                  {PATTERN_LABEL[entity.primary_pattern] ?? entity.primary_pattern}
                </span>
              </div>
              <div className="space-y-2">
                <div className="flex justify-between p-2 rounded bg-slate-800/40">
                  <span className="text-xs text-slate-400">Pays émetteur</span>
                  <span className="text-xs text-slate-200">{entity.country}</span>
                </div>
                <div className="flex justify-between p-2 rounded bg-slate-800/40">
                  <span className="text-xs text-slate-400">Secteur</span>
                  <span className="text-xs text-slate-200">{entity.sector}</span>
                </div>
                <div className="flex justify-between p-2 rounded bg-slate-800/40">
                  <span className="text-xs text-slate-400">Niveau de risque</span>
                  <span className="text-xs font-medium" style={{ color: riskColor }}>
                    {RISK_LABEL[entity.risk_level] ?? entity.risk_level}
                  </span>
                </div>
                <div className="flex justify-between p-2 rounded bg-slate-800/40">
                  <span className="text-xs text-slate-400">Index obligataire estimé</span>
                  <span className="text-xs text-blue-400 font-medium">{entity.estimated_bond_index}/10</span>
                </div>
                <div className="flex justify-between p-2 rounded bg-slate-800/40">
                  <span className="text-xs text-slate-400">Fiabilité modèle</span>
                  <span className="text-xs text-blue-400 font-medium">{(entity.confidence_level * 100).toFixed(0)}%</span>
                </div>
              </div>
              {/* Action from key signal[2] */}
              <div className="bg-blue-900/20 border border-blue-800/30 rounded-lg p-3">
                <p className="text-xs text-blue-300 mb-1 font-medium">Action Recommandée</p>
                <p className="text-sm text-slate-200">{entity.key_signals[2]}</p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

// ── Filter constants ──────────────────────────────────────────────────────────

const RISK_FILTERS = ["tous", "critique", "élevé", "modéré", "faible"] as const;
type RiskFilter = typeof RISK_FILTERS[number];

// ── Main page ─────────────────────────────────────────────────────────────────

export default function SocialBondEnginePage() {
  const [data, setData] = useState<SummaryData | null>(null);
  const [loading, setLoading] = useState(true);
  const [riskFilter, setRiskFilter] = useState<RiskFilter>("tous");
  const [selected, setSelected] = useState<EntityData | null>(null);

  useEffect(() => {
    async function fetchData() {
      setLoading(true);
      try {
        const res = await fetch("/api/social-bond-engine");
        const json = await res.json() as SummaryData;
        setData(json);
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, []);

  const allEntities: EntityData[] = data?.entities ?? [];
  const entities = riskFilter === "tous" ? allEntities : allEntities.filter((e) => e.risk_level === riskFilter);

  const n = allEntities.length;
  const avgImd  = n > 0 ? allEntities.reduce((acc, e) => acc + e.impact_measurement_deficit_score, 0) / n : 0;
  const avgGr   = n > 0 ? allEntities.reduce((acc, e) => acc + e.greenwashing_risk_score,          0) / n : 0;
  const avgIte  = n > 0 ? allEntities.reduce((acc, e) => acc + e.investor_trust_erosion_score,     0) / n : 0;
  const avgRcg  = n > 0 ? allEntities.reduce((acc, e) => acc + e.regulatory_compliance_gap_score,  0) / n : 0;

  const patternTotal = Object.values(data?.pattern_distribution ?? {}).reduce((a, b) => a + b, 0);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
      {selected && <DetailModal entity={selected} onClose={() => setSelected(null)} />}

      {/* Header */}
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-blue-400">
          Social Bond Intelligence Engine
        </h1>
        <p className="text-slate-400 text-sm mt-1">
          Impact · Greenwashing · Confiance Investisseurs · Conformité Réglementaire ESG — Caelum Partners
        </p>
      </div>

      {/* KPI Strip — 6 cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4 mb-6">
        <div className="bg-slate-900 border border-blue-900/30 rounded-xl p-4">
          <p className="text-xs text-slate-400 mb-1">Total Obligations</p>
          <p className="text-2xl font-bold text-white">{data?.total_entities ?? "—"}</p>
        </div>
        <div className="bg-slate-900 border border-blue-900/30 rounded-xl p-4">
          <p className="text-xs text-slate-400 mb-1">Risque Critique</p>
          <p className="text-2xl font-bold text-rose-400">{data?.risk_distribution?.["critique"] ?? "—"}</p>
        </div>
        <div className="bg-slate-900 border border-blue-900/30 rounded-xl p-4">
          <p className="text-xs text-slate-400 mb-1">Risque Élevé</p>
          <p className="text-2xl font-bold text-orange-400">{data?.risk_distribution?.["élevé"] ?? "—"}</p>
        </div>
        <div className="bg-slate-900 border border-blue-900/30 rounded-xl p-4">
          <p className="text-xs text-slate-400 mb-1">Score Composite Moyen</p>
          <p className="text-2xl font-bold text-yellow-400">{data?.avg_composite ?? "—"}</p>
        </div>
        <div className="bg-slate-900 border border-blue-900/30 rounded-xl p-4">
          <p className="text-xs text-slate-400 mb-1">Index Obligataire Moyen</p>
          <p className="text-2xl font-bold text-blue-400">{data?.avg_estimated_bond_index ?? "—"}</p>
        </div>
        <div className="bg-slate-900 border border-blue-900/30 rounded-xl p-4">
          <p className="text-xs text-slate-400 mb-1">Fiabilité Modèle</p>
          <p className="text-2xl font-bold text-emerald-300">
            {data?.confidence_score != null ? `${(data.confidence_score * 100).toFixed(0)}%` : "—"}
          </p>
        </div>
      </div>

      {/* Gauge Rings — 4 sub-scores */}
      <div className="bg-slate-900 border border-blue-900/30 rounded-xl p-5 mb-6">
        <h3 className="text-sm font-semibold text-blue-300 mb-4">Scores Moyens — Dimensions Risque Obligataire Social</h3>
        <div className="flex flex-wrap justify-around gap-6">
          <GaugeRing pct={avgImd}  color="#f87171" label="Déficit Impact" />
          <GaugeRing pct={avgGr}   color="#fb923c" label="Greenwashing" />
          <GaugeRing pct={avgIte}  color="#fbbf24" label="Confiance Invest." />
          <GaugeRing pct={avgRcg}  color="#a78bfa" label="Conformité Régl." />
        </div>
      </div>

      {/* Pattern distribution */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
        <div className="bg-slate-900 border border-blue-900/30 rounded-xl p-4">
          <h3 className="text-sm font-semibold text-blue-300 mb-3">Distribution des Patterns ESG</h3>
          <div className="space-y-2">
            {Object.entries(data?.pattern_distribution ?? {}).map(([pat, count]) => (
              <DistBar
                key={pat}
                label={PATTERN_LABEL[pat] ?? pat}
                value={count}
                total={patternTotal}
                color={PATTERN_COLOR[pat] ?? "#94a3b8"}
              />
            ))}
          </div>
        </div>
        <div className="bg-slate-900 border border-blue-900/30 rounded-xl p-4">
          <h3 className="text-sm font-semibold text-blue-300 mb-3">Distribution des Niveaux de Risque</h3>
          <div className="space-y-2">
            {(["critique", "élevé", "modéré", "faible"] as const).map((level) => (
              <DistBar
                key={level}
                label={RISK_LABEL[level]}
                value={data?.risk_distribution?.[level] ?? 0}
                total={n}
                color={RISK_COLOR[level]}
              />
            ))}
          </div>
          {data?.critical_alerts && data.critical_alerts.length > 0 && (
            <div className="mt-4 p-3 bg-rose-950/30 border border-rose-800/30 rounded-lg">
              <p className="text-xs text-rose-300 font-medium mb-1">Alertes Critiques</p>
              {data.critical_alerts.map((name) => (
                <p key={name} className="text-xs text-slate-300">{name}</p>
              ))}
            </div>
          )}
        </div>
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
                  ? "bg-blue-800 border-blue-600 text-white"
                  : "bg-slate-800 border-slate-700 text-slate-400 hover:text-white hover:border-blue-700"
              }`}
            >
              {f === "tous" ? "Tous" : RISK_LABEL[f] ?? f}
              {f !== "tous" && data?.risk_distribution?.[f] !== undefined && (
                <span className="ml-1 opacity-70">({data.risk_distribution[f]})</span>
              )}
            </button>
          ))}
        </div>
      </div>

      {/* Entity cards */}
      {loading ? (
        <div className="flex items-center justify-center h-48">
          <div className="w-8 h-8 border-2 border-blue-500 border-t-transparent rounded-full animate-spin" />
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
          {entities.map((entity) => {
            const color = RISK_COLOR[entity.risk_level] ?? "#94a3b8";
            return (
              <div
                key={entity.entity_id}
                onClick={() => setSelected(entity)}
                className="bg-slate-900 border border-slate-800 rounded-xl p-4 cursor-pointer hover:border-blue-700 transition-all hover:bg-slate-800/60"
              >
                <div className="flex items-start justify-between mb-3">
                  <div className="flex-1 min-w-0 pr-2">
                    <div className="flex items-center gap-2 mb-1 flex-wrap">
                      <span className={`text-xs px-2 py-0.5 rounded-full border font-medium ${RISK_BG[entity.risk_level] ?? ""}`}>
                        {RISK_LABEL[entity.risk_level] ?? entity.risk_level}
                      </span>
                    </div>
                    <h3 className="text-white font-semibold text-sm leading-snug">{entity.name}</h3>
                    <p className="text-slate-400 text-xs mt-0.5">{entity.entity_id} · {entity.country} · {entity.sector}</p>
                  </div>
                  <div className="flex-shrink-0">
                    <GaugeRing pct={entity.composite_score} color={color} label="" size={72} />
                  </div>
                </div>

                <div className="space-y-1.5 mb-3">
                  <ScoreBar score={entity.impact_measurement_deficit_score} label="Déficit Impact" />
                  <ScoreBar score={entity.greenwashing_risk_score}          label="Greenwashing" />
                  <ScoreBar score={entity.investor_trust_erosion_score}     label="Confiance Invest." />
                  <ScoreBar score={entity.regulatory_compliance_gap_score}  label="Conformité Régl." />
                </div>

                <div className="border-t border-slate-800 pt-2 flex items-center justify-between gap-2 flex-wrap">
                  <span
                    className="text-xs px-2 py-0.5 rounded font-medium bg-slate-800"
                    style={{ color: PATTERN_COLOR[entity.primary_pattern] ?? "#94a3b8" }}
                  >
                    {PATTERN_LABEL[entity.primary_pattern] ?? entity.primary_pattern}
                  </span>
                  <span className="text-xs text-blue-400 font-medium">
                    Index {entity.estimated_bond_index}/10
                  </span>
                </div>
                <p className="text-xs text-slate-500 mt-1.5 truncate">{entity.key_signals[0]}</p>
              </div>
            );
          })}
        </div>
      )}

      {/* Footer */}
      <div className="mt-8 pt-4 border-t border-slate-800 flex flex-wrap gap-4 items-center justify-between">
        <div className="text-xs text-slate-500">
          Sources: {(data?.data_sources ?? []).join(" · ")}
        </div>
        <div className="text-xs text-slate-500">
          Version {data?.engine_version ?? "—"} · Analyse: {data?.last_analysis?.slice(0, 10) ?? "—"}
        </div>
      </div>
    </div>
  );
}
