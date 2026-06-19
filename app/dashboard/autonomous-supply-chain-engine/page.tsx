"use client";

import { useState, useEffect } from "react";

interface NodeData {
  node_id: string;
  node_type: string;
  region: string;
  disruption_risk: string;
  disruption_pattern: string;
  disruption_severity: string;
  recommended_action: string;
  concentration_score: number;
  disruption_score: number;
  resilience_score: number;
  intelligence_score: number;
  supply_chain_composite: number;
  has_critical_exposure: boolean;
  requires_immediate_intervention: boolean;
  estimated_disruption_impact_index: number;
  disruption_signal: string;
}

interface Summary {
  total: number;
  risk_counts: Record<string, number>;
  pattern_counts: Record<string, number>;
  severity_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_supply_chain_composite: number;
  critical_exposure_count: number;
  intervention_required_count: number;
  avg_concentration_score: number;
  avg_disruption_score: number;
  avg_resilience_score: number;
  avg_intelligence_score: number;
  avg_estimated_disruption_impact_index: number;
}

const RISK_BG: Record<string, string> = {
  low:      "bg-emerald-500/20 border-emerald-500/30 text-emerald-300",
  moderate: "bg-yellow-500/20 border-yellow-500/30 text-yellow-300",
  high:     "bg-amber-500/20 border-amber-500/30 text-amber-300",
  critical: "bg-rose-500/20 border-rose-500/30 text-rose-300",
};
const RISK_COLOR: Record<string, string> = {
  low:      "#34d399",
  moderate: "#facc15",
  high:     "#f59e0b",
  critical: "#f87171",
};
const RISK_LABEL: Record<string, string> = {
  low:      "Low",
  moderate: "Moderate",
  high:     "High",
  critical: "Critical",
};
const SEVERITY_BG: Record<string, string> = {
  autonomous: "bg-emerald-500/15 text-emerald-300",
  adaptive:   "bg-yellow-500/15 text-yellow-300",
  stressed:   "bg-amber-500/15 text-amber-300",
  fractured:  "bg-rose-500/15 text-rose-300",
};
const SEVERITY_LABEL: Record<string, string> = {
  autonomous: "Autonome",
  adaptive:   "Adaptatif",
  stressed:   "Sous Stress",
  fractured:  "Fracturé",
};
const ACTION_BG: Record<string, string> = {
  no_action:               "bg-emerald-500/15 text-emerald-300",
  resilience_monitoring:   "bg-sky-500/15 text-sky-300",
  buffer_stockpiling:      "bg-yellow-500/15 text-yellow-300",
  nearshoring_acceleration:"bg-amber-500/15 text-amber-300",
  supply_diversification:  "bg-orange-500/15 text-orange-300",
  emergency_sourcing:      "bg-rose-500/15 text-rose-300",
};
const ACTION_LABEL: Record<string, string> = {
  no_action:               "Aucune Action",
  resilience_monitoring:   "Surveillance Résilience",
  buffer_stockpiling:      "Constitution Stocks Tampon",
  nearshoring_acceleration:"Accélération Nearshoring",
  supply_diversification:  "Diversification Supply",
  emergency_sourcing:      "Approvisionnement Urgence",
};
const PATTERN_LABEL: Record<string, string> = {
  none:                "Aucun",
  supplier_collapse:   "Effondrement Fournisseur",
  demand_shock:        "Choc Demande",
  logistics_breakdown: "Rupture Logistique",
  digital_blindspot:   "Angle Mort Digital",
  climate_disruption:  "Disruption Climatique",
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
  const color = score <= 20 ? "#34d399" : score <= 40 ? "#facc15" : score <= 60 ? "#f59e0b" : "#f87171";
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

interface ModalProps { node: NodeData; onClose: () => void }

function DetailModal({ node, onClose }: ModalProps) {
  const [tab, setTab] = useState<"scores" | "signal" | "action">("scores");

  useEffect(() => {
    const handler = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [onClose]);

  const riskColor = RISK_COLOR[node.disruption_risk] ?? "#94a3b8";

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4"
      onClick={(e) => { if (e.currentTarget === e.target) onClose(); }}
    >
      <div className="bg-slate-900 border border-amber-500/30 rounded-xl shadow-2xl w-full max-w-lg">
        <div className="flex items-start justify-between p-5 border-b border-slate-800">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <span className={`text-xs px-2 py-0.5 rounded-full border font-medium ${RISK_BG[node.disruption_risk] ?? ""}`}>
                {RISK_LABEL[node.disruption_risk] ?? node.disruption_risk}
              </span>
              <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${SEVERITY_BG[node.disruption_severity] ?? ""}`}>
                {SEVERITY_LABEL[node.disruption_severity] ?? node.disruption_severity}
              </span>
            </div>
            <h2 className="text-white font-bold text-lg">{node.node_id}</h2>
            <p className="text-slate-400 text-sm">
              {node.region} · {node.node_type} · Composite:{" "}
              <span style={{ color: riskColor }}>{node.supply_chain_composite}</span>
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
                  ? "text-yellow-400 border-b-2 border-amber-500 bg-slate-800/40"
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
              <ScoreBar score={node.concentration_score} label="Concentration (30%)" />
              <ScoreBar score={node.disruption_score}    label="Disruption (25%)" />
              <ScoreBar score={node.resilience_score}    label="Résilience (25%)" />
              <ScoreBar score={node.intelligence_score}  label="Intelligence (20%)" />
              <div className="pt-2 border-t border-slate-800">
                <div className="flex justify-between items-center">
                  <span className="text-sm text-slate-400">Composite Supply Chain</span>
                  <span className="text-lg font-bold" style={{ color: riskColor }}>{node.supply_chain_composite}</span>
                </div>
                <p className="text-xs text-slate-500 mt-1">Score composite risque disruption (0–100)</p>
              </div>
            </div>
          )}

          {tab === "signal" && (
            <>
              <div className="flex items-center justify-center py-2">
                <GaugeRing pct={node.supply_chain_composite} color={riskColor} label="Composite" size={110} />
              </div>
              <div className="bg-slate-800/50 rounded-lg p-3">
                <p className="text-xs text-slate-400 mb-1">Signal Disruption</p>
                <p className="text-sm text-white">{node.disruption_signal}</p>
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div className="bg-slate-800/50 rounded-lg p-3">
                  <p className="text-xs text-slate-400">Disruption Impact Index</p>
                  <p className="text-lg font-bold text-yellow-400">{node.estimated_disruption_impact_index.toFixed(2)}</p>
                </div>
                <div className="bg-slate-800/50 rounded-lg p-3">
                  <p className="text-xs text-slate-400">Exposition Critique</p>
                  <p className={`text-lg font-bold ${node.has_critical_exposure ? "text-rose-400" : "text-emerald-400"}`}>
                    {node.has_critical_exposure ? "Active" : "Inactive"}
                  </p>
                </div>
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div className="bg-slate-800/50 rounded-lg p-3">
                  <p className="text-xs text-slate-400">Intervention Immédiate</p>
                  <p className={`text-sm font-medium ${node.requires_immediate_intervention ? "text-amber-400" : "text-emerald-400"}`}>
                    {node.requires_immediate_intervention ? "Requise" : "Non requise"}
                  </p>
                </div>
                <div className="bg-slate-800/50 rounded-lg p-3">
                  <p className="text-xs text-slate-400">Pattern</p>
                  <p className="text-sm font-medium text-slate-200">{PATTERN_LABEL[node.disruption_pattern] ?? node.disruption_pattern}</p>
                </div>
              </div>
            </>
          )}

          {tab === "action" && (
            <div className="space-y-4">
              <div className="bg-slate-800/50 rounded-lg p-4">
                <p className="text-xs text-slate-400 mb-2">Action Recommandée</p>
                <span className={`text-sm px-3 py-1.5 rounded-lg font-medium ${ACTION_BG[node.recommended_action] ?? ""}`}>
                  {ACTION_LABEL[node.recommended_action] ?? node.recommended_action}
                </span>
              </div>
              <div className="space-y-2">
                <div className="flex justify-between p-2 rounded bg-slate-800/40">
                  <span className="text-xs text-slate-400">Pattern</span>
                  <span className="text-xs text-slate-200">{PATTERN_LABEL[node.disruption_pattern] ?? node.disruption_pattern}</span>
                </div>
                <div className="flex justify-between p-2 rounded bg-slate-800/40">
                  <span className="text-xs text-slate-400">Sévérité</span>
                  <span className="text-xs text-slate-200">{SEVERITY_LABEL[node.disruption_severity] ?? node.disruption_severity}</span>
                </div>
                <div className="flex justify-between p-2 rounded bg-slate-800/40">
                  <span className="text-xs text-slate-400">Disruption Impact Index</span>
                  <span className="text-xs text-yellow-400 font-medium">{node.estimated_disruption_impact_index.toFixed(2)}</span>
                </div>
                <div className="flex justify-between p-2 rounded bg-slate-800/40">
                  <span className="text-xs text-slate-400">Intervention Immédiate</span>
                  <span className={`text-xs font-medium ${node.requires_immediate_intervention ? "text-amber-400" : "text-emerald-400"}`}>
                    {node.requires_immediate_intervention ? "Requise" : "Non requise"}
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
const PATTERN_FILTERS = ["all", "none", "supplier_collapse", "demand_shock", "logistics_breakdown", "digital_blindspot", "climate_disruption"] as const;
type PatternFilter = typeof PATTERN_FILTERS[number];

export default function AutonomousSupplyChainEnginePage() {
  const [data, setData] = useState<{ nodes: NodeData[]; summary: Summary } | null>(null);
  const [loading, setLoading] = useState(true);
  const [riskFilter, setRiskFilter] = useState<RiskFilter>("all");
  const [patternFilter, setPatternFilter] = useState<PatternFilter>("all");
  const [selected, setSelected] = useState<NodeData | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      const params = new URLSearchParams();
      if (riskFilter !== "all")    params.set("risk",    riskFilter);
      if (patternFilter !== "all") params.set("pattern", patternFilter);
      const res  = await fetch(`/api/autonomous-supply-chain-engine?${params}`);
      const json = await res.json();
      setData(json);
      setLoading(false);
    };
    fetchData();
  }, [riskFilter, patternFilter]);

  const s     = data?.summary;
  const nodes = data?.nodes ?? [];

  const riskColors: Record<string, string> = {
    low: "#34d399", moderate: "#facc15", high: "#f59e0b", critical: "#f87171",
  };
  const severityColors: Record<string, string> = {
    autonomous: "#34d399", adaptive: "#facc15", stressed: "#f59e0b", fractured: "#f87171",
  };
  const patternColors: Record<string, string> = {
    none: "#64748b", supplier_collapse: "#f87171", demand_shock: "#f59e0b",
    logistics_breakdown: "#fbbf24", digital_blindspot: "#a78bfa", climate_disruption: "#22d3ee",
  };

  const distributions: Array<{ title: string; counts: Record<string, number>; colors: Record<string, string> }> = [
    { title: "Risque",    counts: s?.risk_counts     ?? {}, colors: riskColors },
    { title: "Sévérité",  counts: s?.severity_counts ?? {}, colors: severityColors },
    { title: "Pattern",   counts: s?.pattern_counts  ?? {}, colors: patternColors },
    { title: "Action",    counts: s?.action_counts   ?? {}, colors: {} },
  ];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
      {selected && <DetailModal node={selected} onClose={() => setSelected(null)} />}

      <div className="mb-6">
        <h1 className="text-2xl font-bold text-yellow-400">
          Résilience Supply Chain Autonome & Intelligence Disruption
        </h1>
        <p className="text-slate-400 text-sm mt-1">
          Concentration · Disruption · Résilience · Intelligence — détection autonome des ruptures supply chain
        </p>
      </div>

      {/* KPI Strip — 6 cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 xl:grid-cols-6 gap-4 mb-6">
        <div className="bg-slate-900 border border-amber-500/30 rounded-xl p-4">
          <p className="text-xs text-slate-400 mb-1">Noeuds</p>
          <p className="text-2xl font-bold text-white">{s?.total ?? "—"}</p>
        </div>
        <div className="bg-slate-900 border border-amber-500/30 rounded-xl p-4">
          <p className="text-xs text-slate-400 mb-1">Composite</p>
          <p className="text-2xl font-bold text-yellow-400">{s?.avg_supply_chain_composite ?? "—"}</p>
        </div>
        <div className="bg-slate-900 border border-amber-500/30 rounded-xl p-4">
          <p className="text-xs text-slate-400 mb-1">Exposition Critique</p>
          <p className="text-2xl font-bold text-rose-400">{s?.critical_exposure_count ?? "—"}</p>
        </div>
        <div className="bg-slate-900 border border-amber-500/30 rounded-xl p-4">
          <p className="text-xs text-slate-400 mb-1">Intervention Req.</p>
          <p className="text-2xl font-bold text-amber-400">{s?.intervention_required_count ?? "—"}</p>
        </div>
        <div className="bg-slate-900 border border-amber-500/30 rounded-xl p-4">
          <p className="text-xs text-slate-400 mb-1">Impact Index</p>
          <p className="text-2xl font-bold text-yellow-300">{s?.avg_estimated_disruption_impact_index ?? "—"}</p>
        </div>
        <div className="bg-slate-900 border border-amber-500/30 rounded-xl p-4">
          <p className="text-xs text-slate-400 mb-1">Moy Concentration</p>
          <p className="text-2xl font-bold text-amber-300">{s?.avg_concentration_score ?? "—"}</p>
        </div>
      </div>

      {/* Gauge Rings — 4 sub-scores */}
      <div className="bg-slate-900 border border-amber-500/30 rounded-xl p-5 mb-6">
        <h3 className="text-sm font-semibold text-slate-300 mb-4">Scores Moyens (risque disruption supply chain)</h3>
        <div className="flex flex-wrap justify-around gap-6">
          <GaugeRing pct={s?.avg_concentration_score ?? 0} color="#f59e0b" label="Concentration" />
          <GaugeRing pct={s?.avg_disruption_score    ?? 0} color="#f87171" label="Disruption" />
          <GaugeRing pct={s?.avg_resilience_score    ?? 0} color="#facc15" label="Résilience" />
          <GaugeRing pct={s?.avg_intelligence_score  ?? 0} color="#34d399" label="Intelligence" />
        </div>
      </div>

      {/* Distribution bars — 4 */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
        {distributions.map((d) => (
          <div key={d.title} className="bg-slate-900 border border-amber-500/30 rounded-xl p-4">
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
                  ? "bg-amber-700 border-amber-500 text-white"
                  : "bg-slate-800 border-slate-700 text-slate-400 hover:text-white hover:border-amber-600"
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
                  ? "bg-amber-700 border-amber-500 text-white"
                  : "bg-slate-800 border-slate-700 text-slate-400 hover:text-white hover:border-amber-600"
              }`}
            >
              {f === "all" ? "Tous" : PATTERN_LABEL[f] ?? f}
            </button>
          ))}
        </div>
      </div>

      {/* Node cards */}
      {loading ? (
        <div className="flex items-center justify-center h-48">
          <div className="w-8 h-8 border-2 border-amber-500 border-t-transparent rounded-full animate-spin" />
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
          {nodes.map((node) => {
            const color = RISK_COLOR[node.disruption_risk] ?? "#94a3b8";
            return (
              <div
                key={node.node_id}
                onClick={() => setSelected(node)}
                className="bg-slate-900 border border-slate-800 rounded-xl p-4 cursor-pointer hover:border-amber-500/50 transition-all hover:bg-slate-800/60"
              >
                <div className="flex items-start justify-between mb-3">
                  <div className="flex-1 min-w-0 pr-2">
                    <div className="flex items-center gap-2 mb-1 flex-wrap">
                      <span className={`text-xs px-2 py-0.5 rounded-full border font-medium ${RISK_BG[node.disruption_risk] ?? ""}`}>
                        {RISK_LABEL[node.disruption_risk] ?? node.disruption_risk}
                      </span>
                      {node.has_critical_exposure && (
                        <span className="text-xs px-2 py-0.5 rounded-full bg-rose-500/20 border border-rose-500/30 text-rose-300 font-medium">
                          EXPOSITION CRITIQUE
                        </span>
                      )}
                      {node.requires_immediate_intervention && (
                        <span className="text-xs px-2 py-0.5 rounded-full bg-amber-500/20 border border-amber-500/30 text-amber-300 font-medium">
                          INTERVENTION REQ.
                        </span>
                      )}
                    </div>
                    <h3 className="text-white font-semibold text-sm">{node.node_id}</h3>
                    <p className="text-slate-400 text-xs">{node.region} · {node.node_type}</p>
                  </div>
                  <div className="flex-shrink-0">
                    <GaugeRing pct={node.supply_chain_composite} color={color} label="" size={72} />
                  </div>
                </div>

                <div className="space-y-1.5 mb-3">
                  <ScoreBar score={node.concentration_score} label="Concentration" />
                  <ScoreBar score={node.disruption_score}    label="Disruption" />
                  <ScoreBar score={node.resilience_score}    label="Résilience" />
                  <ScoreBar score={node.intelligence_score}  label="Intelligence" />
                </div>

                <div className="border-t border-slate-800 pt-2 flex items-center justify-between">
                  <span className={`text-xs px-2 py-0.5 rounded font-medium ${ACTION_BG[node.recommended_action] ?? ""}`}>
                    {ACTION_LABEL[node.recommended_action] ?? node.recommended_action}
                  </span>
                  <span className="text-xs text-yellow-400 font-medium">
                    impact {node.estimated_disruption_impact_index.toFixed(2)}
                  </span>
                </div>
                <div className="flex items-center gap-1.5 mt-2">
                  <span className={`text-xs px-1.5 py-0.5 rounded font-medium ${SEVERITY_BG[node.disruption_severity] ?? ""}`}>
                    {SEVERITY_LABEL[node.disruption_severity] ?? node.disruption_severity}
                  </span>
                  <span className="text-xs text-slate-500 truncate">{PATTERN_LABEL[node.disruption_pattern] ?? node.disruption_pattern}</span>
                </div>
                <p className="text-xs text-slate-500 mt-1.5 truncate">{node.disruption_signal}</p>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
