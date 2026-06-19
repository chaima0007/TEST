"use client";

import { useState, useEffect } from "react";

interface ScenarioData {
  scenario_id: string;
  region: string;
  foresight_risk: string;
  scenario_pattern: string;
  foresight_severity: string;
  recommended_action: string;
  signal_score: number;
  readiness_score: number;
  simulation_score: number;
  exposure_score: number;
  foresight_composite: number;
  has_blind_spot_risk: boolean;
  requires_immediate_simulation: boolean;
  estimated_scenario_risk_index: number;
  foresight_signal: string;
}

interface Summary {
  total: number;
  risk_counts: Record<string, number>;
  pattern_counts: Record<string, number>;
  severity_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_foresight_composite: number;
  blind_spot_risk_count: number;
  immediate_simulation_count: number;
  avg_signal_score: number;
  avg_readiness_score: number;
  avg_simulation_score: number;
  avg_exposure_score: number;
  avg_estimated_scenario_risk_index: number;
}

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
  low:      "Low",
  moderate: "Moderate",
  high:     "High",
  critical: "Critical",
};
const SEVERITY_BG: Record<string, string> = {
  prepared:   "bg-emerald-500/15 text-emerald-300",
  monitoring: "bg-amber-500/15 text-amber-300",
  vulnerable: "bg-orange-500/15 text-orange-300",
  blind_spot: "bg-rose-500/15 text-rose-300",
};
const SEVERITY_LABEL: Record<string, string> = {
  prepared:   "Préparé",
  monitoring: "Surveillance",
  vulnerable: "Vulnérable",
  blind_spot: "Angle Mort",
};
const ACTION_BG: Record<string, string> = {
  no_action:               "bg-emerald-500/15 text-emerald-300",
  scenario_monitoring:     "bg-sky-500/15 text-sky-300",
  signal_amplification:    "bg-blue-500/15 text-blue-300",
  strategic_hedge:         "bg-amber-500/15 text-amber-300",
  contingency_activation:  "bg-yellow-500/15 text-yellow-300",
  crisis_simulation:       "bg-orange-500/15 text-orange-300",
  scenario_replan:         "bg-orange-600/15 text-orange-300",
  strategic_pivot:         "bg-rose-500/15 text-rose-300",
  emergency_replan:        "bg-red-500/15 text-red-300",
};
const ACTION_LABEL: Record<string, string> = {
  no_action:               "Aucune Action",
  scenario_monitoring:     "Surveillance Scénario",
  signal_amplification:    "Amplification Signal",
  strategic_hedge:         "Couverture Stratégique",
  contingency_activation:  "Activation Contingence",
  crisis_simulation:       "Simulation Crise",
  scenario_replan:         "Replanification",
  strategic_pivot:         "Pivot Stratégique",
  emergency_replan:        "Replanification Urgente",
};
const PATTERN_LABEL: Record<string, string> = {
  none:                  "Aucun",
  black_swan:            "Cygne Noir",
  disruption_wave:       "Vague Disruptive",
  competitive_collapse:  "Effondrement Concurrentiel",
  regulatory_shock:      "Choc Réglementaire",
  geopolitical_shift:    "Choc Géopolitique",
};

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

type DistBarItem = { title: string; counts: Record<string, number>; colors: Record<string, string> };

function DistBar({ title, counts, colors }: DistBarItem) {
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

interface ModalProps { scenario: ScenarioData; onClose: () => void }

function DetailModal({ scenario, onClose }: ModalProps) {
  const [tab, setTab] = useState<"scores" | "signal" | "action">("scores");

  useEffect(() => {
    const handler = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [onClose]);

  const riskColor = RISK_COLOR[scenario.foresight_risk] ?? "#94a3b8";

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4"
      onClick={(e) => { if (e.currentTarget === e.target) onClose(); }}
    >
      <div className="bg-slate-900 border border-slate-700 rounded-xl shadow-2xl w-full max-w-lg">
        <div className="flex items-start justify-between p-5 border-b border-slate-800">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <span className={`text-xs px-2 py-0.5 rounded-full border font-medium ${RISK_BG[scenario.foresight_risk] ?? ""}`}>
                {RISK_LABEL[scenario.foresight_risk] ?? scenario.foresight_risk}
              </span>
              <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${SEVERITY_BG[scenario.foresight_severity] ?? ""}`}>
                {SEVERITY_LABEL[scenario.foresight_severity] ?? scenario.foresight_severity}
              </span>
            </div>
            <h2 className="text-white font-bold text-lg">{scenario.scenario_id}</h2>
            <p className="text-slate-400 text-sm">
              {scenario.region} · Composite: <span style={{ color: riskColor }}>{scenario.foresight_composite}</span>
            </p>
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-white p-1 transition-colors" aria-label="Close">
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
                tab === t ? "text-indigo-400 border-b-2 border-indigo-500 bg-slate-800/40" : "text-slate-400 hover:text-slate-200"
              }`}
            >
              {t === "scores" ? "Scores" : t === "signal" ? "Signal" : "Action"}
            </button>
          ))}
        </div>

        <div className="p-5 space-y-4">
          {tab === "scores" && (
            <div className="space-y-3">
              <ScoreBar score={scenario.signal_score} label="Signal (30%)" />
              <ScoreBar score={scenario.readiness_score} label="Préparation (25%)" />
              <ScoreBar score={scenario.simulation_score} label="Simulation (25%)" />
              <ScoreBar score={scenario.exposure_score} label="Exposition (20%)" />
              <div className="pt-2 border-t border-slate-800">
                <div className="flex justify-between items-center">
                  <span className="text-sm text-slate-400">Composite Foresight</span>
                  <span className="text-lg font-bold" style={{ color: riskColor }}>{scenario.foresight_composite}</span>
                </div>
                <p className="text-xs text-slate-500 mt-1">Score composite risque foresight (0–100)</p>
              </div>
            </div>
          )}

          {tab === "signal" && (
            <>
              <div className="flex items-center justify-center py-2">
                <GaugeRing pct={scenario.foresight_composite} color={riskColor} label="Composite" size={110} />
              </div>
              <div className="bg-slate-800/50 rounded-lg p-3">
                <p className="text-xs text-slate-400 mb-1">Signal Foresight</p>
                <p className="text-sm text-white">{scenario.foresight_signal}</p>
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div className="bg-slate-800/50 rounded-lg p-3">
                  <p className="text-xs text-slate-400">Risque Scénario Index</p>
                  <p className="text-lg font-bold text-indigo-400">{scenario.estimated_scenario_risk_index.toFixed(2)}</p>
                </div>
                <div className="bg-slate-800/50 rounded-lg p-3">
                  <p className="text-xs text-slate-400">Angle Mort</p>
                  <p className={`text-lg font-bold ${scenario.has_blind_spot_risk ? "text-rose-400" : "text-emerald-400"}`}>
                    {scenario.has_blind_spot_risk ? "Détecté" : "Absent"}
                  </p>
                </div>
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div className="bg-slate-800/50 rounded-lg p-3">
                  <p className="text-xs text-slate-400">Simul. Urgente</p>
                  <p className={`text-sm font-medium ${scenario.requires_immediate_simulation ? "text-orange-400" : "text-emerald-400"}`}>
                    {scenario.requires_immediate_simulation ? "Requise" : "Non requise"}
                  </p>
                </div>
                <div className="bg-slate-800/50 rounded-lg p-3">
                  <p className="text-xs text-slate-400">Pattern</p>
                  <p className="text-sm font-medium text-slate-200">{PATTERN_LABEL[scenario.scenario_pattern] ?? scenario.scenario_pattern}</p>
                </div>
              </div>
            </>
          )}

          {tab === "action" && (
            <div className="space-y-4">
              <div className="bg-slate-800/50 rounded-lg p-4">
                <p className="text-xs text-slate-400 mb-2">Action Recommandée</p>
                <span className={`text-sm px-3 py-1.5 rounded-lg font-medium ${ACTION_BG[scenario.recommended_action] ?? ""}`}>
                  {ACTION_LABEL[scenario.recommended_action] ?? scenario.recommended_action}
                </span>
              </div>
              <div className="space-y-2">
                <div className="flex justify-between p-2 rounded bg-slate-800/40">
                  <span className="text-xs text-slate-400">Pattern</span>
                  <span className="text-xs text-slate-200">{PATTERN_LABEL[scenario.scenario_pattern] ?? scenario.scenario_pattern}</span>
                </div>
                <div className="flex justify-between p-2 rounded bg-slate-800/40">
                  <span className="text-xs text-slate-400">Sévérité</span>
                  <span className="text-xs text-slate-200">{SEVERITY_LABEL[scenario.foresight_severity] ?? scenario.foresight_severity}</span>
                </div>
                <div className="flex justify-between p-2 rounded bg-slate-800/40">
                  <span className="text-xs text-slate-400">Risque Scénario Index</span>
                  <span className="text-xs text-indigo-400 font-medium">{scenario.estimated_scenario_risk_index.toFixed(2)}</span>
                </div>
                <div className="flex justify-between p-2 rounded bg-slate-800/40">
                  <span className="text-xs text-slate-400">Simulation Urgente</span>
                  <span className={`text-xs font-medium ${scenario.requires_immediate_simulation ? "text-orange-400" : "text-emerald-400"}`}>
                    {scenario.requires_immediate_simulation ? "Requise" : "Non requise"}
                  </span>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

const RISK_FILTERS = ["all", "low", "moderate", "high", "critical"] as const;
type RiskFilter = typeof RISK_FILTERS[number];
const PATTERN_FILTERS = ["all", "none", "black_swan", "disruption_wave", "competitive_collapse", "regulatory_shock", "geopolitical_shift"] as const;
type PatternFilter = typeof PATTERN_FILTERS[number];

export default function StrategicForesightSimulationEnginePage() {
  const [data, setData] = useState<{ scenarios: ScenarioData[]; summary: Summary } | null>(null);
  const [loading, setLoading] = useState(true);
  const [riskFilter, setRiskFilter] = useState<RiskFilter>("all");
  const [patternFilter, setPatternFilter] = useState<PatternFilter>("all");
  const [selected, setSelected] = useState<ScenarioData | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      const params = new URLSearchParams();
      if (riskFilter !== "all")    params.set("risk",    riskFilter);
      if (patternFilter !== "all") params.set("pattern", patternFilter);
      const res = await fetch(`/api/strategic-foresight-simulation-engine?${params}`);
      const json = await res.json();
      setData(json);
      setLoading(false);
    };
    fetchData();
  }, [riskFilter, patternFilter]);

  const s = data?.summary;
  const scenarios = data?.scenarios ?? [];

  const riskColors: Record<string, string> = {
    low: "#34d399", moderate: "#fbbf24", high: "#f97316", critical: "#f87171",
  };
  const severityColors: Record<string, string> = {
    prepared: "#34d399", monitoring: "#fbbf24", vulnerable: "#f97316", blind_spot: "#f87171",
  };
  const patternColors: Record<string, string> = {
    none: "#64748b", black_swan: "#f87171", disruption_wave: "#f97316",
    competitive_collapse: "#fbbf24", regulatory_shock: "#a78bfa", geopolitical_shift: "#60a5fa",
  };

  const distributions: Array<{ title: string; counts: Record<string, number>; colors: Record<string, string> }> = [
    { title: "Risque", counts: s?.risk_counts ?? {}, colors: riskColors },
    { title: "Sévérité", counts: s?.severity_counts ?? {}, colors: severityColors },
    { title: "Pattern", counts: s?.pattern_counts ?? {}, colors: patternColors },
    { title: "Action", counts: s?.action_counts ?? {}, colors: {} },
  ];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
      {selected && <DetailModal scenario={selected} onClose={() => setSelected(null)} />}

      <div className="mb-6">
        <h1 className="text-2xl font-bold text-white">Anticipation Stratégique & Simulation Avancée</h1>
        <p className="text-slate-400 text-sm mt-1">
          Signal · Préparation · Simulation · Exposition — anticipation et résilience face aux chocs futurs
        </p>
      </div>

      {/* KPI Strip — 6 cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 xl:grid-cols-6 gap-4 mb-6">
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
          <p className="text-xs text-slate-400 mb-1">Scénarios</p>
          <p className="text-2xl font-bold text-white">{s?.total ?? "—"}</p>
        </div>
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
          <p className="text-xs text-slate-400 mb-1">Composite</p>
          <p className="text-2xl font-bold text-indigo-400">{s?.avg_foresight_composite ?? "—"}</p>
        </div>
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
          <p className="text-xs text-slate-400 mb-1">Angle Mort</p>
          <p className="text-2xl font-bold text-rose-400">{s?.blind_spot_risk_count ?? "—"}</p>
        </div>
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
          <p className="text-xs text-slate-400 mb-1">Simulation Urgente</p>
          <p className="text-2xl font-bold text-orange-400">{s?.immediate_simulation_count ?? "—"}</p>
        </div>
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
          <p className="text-xs text-slate-400 mb-1">Risque Scénario</p>
          <p className="text-2xl font-bold text-blue-400">{s?.avg_estimated_scenario_risk_index ?? "—"}</p>
        </div>
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
          <p className="text-xs text-slate-400 mb-1">Moy Signal</p>
          <p className="text-2xl font-bold text-sky-400">{s?.avg_signal_score ?? "—"}</p>
        </div>
      </div>

      {/* Gauge Rings — 4 sub-scores */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 mb-6">
        <h3 className="text-sm font-semibold text-slate-300 mb-4">Scores Moyens (risque foresight)</h3>
        <div className="flex flex-wrap justify-around gap-6">
          <GaugeRing pct={s?.avg_signal_score ?? 0} color="#818cf8" label="Signal" />
          <GaugeRing pct={s?.avg_readiness_score ?? 0} color="#60a5fa" label="Préparation" />
          <GaugeRing pct={s?.avg_simulation_score ?? 0} color="#a78bfa" label="Simulation" />
          <GaugeRing pct={s?.avg_exposure_score ?? 0} color="#f87171" label="Exposition" />
        </div>
      </div>

      {/* Distribution bars — 4 */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
        {distributions.map((d) => (
          <div key={d.title} className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <DistBar title={d.title} counts={d.counts} colors={d.colors} />
          </div>
        ))}
      </div>

      {/* Filters */}
      <div className="mb-4 space-y-3">
        <div className="flex flex-wrap gap-2 items-center">
          <span className="text-xs text-slate-500 mr-1">Risque:</span>
          {RISK_FILTERS.map((f) => (
            <button
              key={f}
              onClick={() => setRiskFilter(f)}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors border ${
                riskFilter === f
                  ? "bg-indigo-700 border-indigo-500 text-white"
                  : "bg-slate-800 border-slate-700 text-slate-400 hover:text-white hover:border-indigo-700"
              }`}
            >
              {f === "all" ? "Tous" : RISK_LABEL[f] ?? f}
              {f !== "all" && s?.risk_counts?.[f] !== undefined && (
                <span className="ml-1 opacity-70">({s.risk_counts[f]})</span>
              )}
            </button>
          ))}
        </div>
        <div className="flex flex-wrap gap-2 items-center">
          <span className="text-xs text-slate-500 mr-1">Pattern:</span>
          {PATTERN_FILTERS.map((f) => (
            <button
              key={f}
              onClick={() => setPatternFilter(f)}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors border ${
                patternFilter === f
                  ? "bg-indigo-700 border-indigo-500 text-white"
                  : "bg-slate-800 border-slate-700 text-slate-400 hover:text-white hover:border-indigo-700"
              }`}
            >
              {f === "all" ? "Tous" : PATTERN_LABEL[f] ?? f}
            </button>
          ))}
        </div>
      </div>

      {/* Scenario cards */}
      {loading ? (
        <div className="flex items-center justify-center h-48">
          <div className="w-8 h-8 border-2 border-indigo-500 border-t-transparent rounded-full animate-spin" />
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
          {scenarios.map((scenario) => {
            const color = RISK_COLOR[scenario.foresight_risk] ?? "#94a3b8";
            return (
              <div
                key={scenario.scenario_id}
                onClick={() => setSelected(scenario)}
                className="bg-slate-900 border border-slate-800 rounded-xl p-4 cursor-pointer hover:border-indigo-700 transition-all hover:bg-slate-800/60"
              >
                <div className="flex items-start justify-between mb-3">
                  <div className="flex-1 min-w-0 pr-2">
                    <div className="flex items-center gap-2 mb-1 flex-wrap">
                      <span className={`text-xs px-2 py-0.5 rounded-full border font-medium ${RISK_BG[scenario.foresight_risk] ?? ""}`}>
                        {RISK_LABEL[scenario.foresight_risk] ?? scenario.foresight_risk}
                      </span>
                      {scenario.has_blind_spot_risk && (
                        <span className="text-xs px-2 py-0.5 rounded-full bg-rose-500/20 border border-rose-500/30 text-rose-300 font-medium">
                          ANGLE MORT
                        </span>
                      )}
                      {scenario.requires_immediate_simulation && (
                        <span className="text-xs px-2 py-0.5 rounded-full bg-orange-500/20 border border-orange-500/30 text-orange-300 font-medium">
                          SIMUL. URG.
                        </span>
                      )}
                    </div>
                    <h3 className="text-white font-semibold text-sm">{scenario.scenario_id}</h3>
                    <p className="text-slate-400 text-xs">{scenario.region}</p>
                  </div>
                  <div className="flex-shrink-0">
                    <GaugeRing pct={scenario.foresight_composite} color={color} label="" size={72} />
                  </div>
                </div>

                <div className="space-y-1.5 mb-3">
                  <ScoreBar score={scenario.signal_score} label="Signal" />
                  <ScoreBar score={scenario.readiness_score} label="Préparation" />
                  <ScoreBar score={scenario.simulation_score} label="Simulation" />
                  <ScoreBar score={scenario.exposure_score} label="Exposition" />
                </div>

                <div className="border-t border-slate-800 pt-2 flex items-center justify-between">
                  <span className={`text-xs px-2 py-0.5 rounded font-medium ${ACTION_BG[scenario.recommended_action] ?? ""}`}>
                    {ACTION_LABEL[scenario.recommended_action] ?? scenario.recommended_action}
                  </span>
                  <span className="text-xs text-indigo-400 font-medium">
                    idx {scenario.estimated_scenario_risk_index.toFixed(2)}
                  </span>
                </div>
                <div className="flex items-center gap-1.5 mt-2">
                  <span className={`text-xs px-1.5 py-0.5 rounded font-medium ${SEVERITY_BG[scenario.foresight_severity] ?? ""}`}>
                    {SEVERITY_LABEL[scenario.foresight_severity] ?? scenario.foresight_severity}
                  </span>
                  <span className="text-xs text-slate-500 truncate">{PATTERN_LABEL[scenario.scenario_pattern] ?? scenario.scenario_pattern}</span>
                </div>
                <p className="text-xs text-slate-500 mt-1.5 truncate">{scenario.foresight_signal}</p>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
