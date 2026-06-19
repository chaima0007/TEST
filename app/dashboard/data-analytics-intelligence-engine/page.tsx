"use client";

import { useEffect, useState, useCallback } from "react";

interface DataPipeline {
  pipeline_id: string;
  region: string;
  data_domain: string;
  data_risk: string;
  data_pattern: string;
  data_severity: string;
  recommended_action: string;
  pipeline_score: number;
  quality_score: number;
  analytics_score: number;
  governance_score: number;
  data_composite: number;
  has_data_alert: boolean;
  requires_data_governance: boolean;
  estimated_insight_delay_hours: number;
  data_signal: string;
}

interface Summary {
  total: number;
  risk_counts: Record<string, number>;
  pattern_counts: Record<string, number>;
  severity_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_data_composite: number;
  data_alert_count: number;
  governance_count: number;
  avg_pipeline_score: number;
  avg_quality_score: number;
  avg_analytics_score: number;
  avg_governance_score: number;
  avg_estimated_insight_delay_hours: number;
}

const RISK_COLORS: Record<string, string> = {
  low:      "text-emerald-400",
  moderate: "text-amber-400",
  high:     "text-orange-400",
  critical: "text-red-400",
};
const RISK_BG: Record<string, string> = {
  low:      "bg-emerald-400/10 border-emerald-400/30",
  moderate: "bg-amber-400/10 border-amber-400/30",
  high:     "bg-orange-400/10 border-orange-400/30",
  critical: "bg-red-400/10 border-red-400/30",
};
const SEV_COLORS: Record<string, string> = {
  reliable:   "bg-emerald-500",
  degraded:   "bg-amber-500",
  unreliable: "bg-orange-500",
  blind:      "bg-red-500",
};
const PATTERN_LABELS: Record<string, string> = {
  none:                "No Issues",
  pipeline_failure:    "Pipeline Failure",
  data_drift:          "Data Drift",
  quality_degradation: "Quality Degradation",
  model_staleness:     "Model Staleness",
  insight_gap:         "Insight Gap",
};
const ACTION_LABELS: Record<string, string> = {
  no_action:                    "No Action",
  data_monitoring:              "Data Monitoring",
  pipeline_repair:              "Pipeline Repair",
  data_quality_remediation:     "Quality Remediation",
  drift_investigation:          "Drift Investigation",
  model_retraining:             "Model Retraining",
  schema_validation:            "Schema Validation",
  data_governance_review:       "Governance Review",
  analytics_emergency:          "Analytics Emergency",
};
const ACTION_COLORS: Record<string, string> = {
  no_action:                    "text-slate-400",
  data_monitoring:              "text-indigo-400",
  pipeline_repair:              "text-amber-400",
  data_quality_remediation:     "text-orange-400",
  drift_investigation:          "text-violet-400",
  model_retraining:             "text-sky-400",
  schema_validation:            "text-amber-400",
  data_governance_review:       "text-red-400",
  analytics_emergency:          "text-red-500",
};
const DOMAIN_LABELS: Record<string, string> = {
  sales:            "Sales",
  finance:          "Finance",
  operations:       "Operations",
  marketing:        "Marketing",
  customer_success: "Customer Success",
  supply_chain:     "Supply Chain",
  product:          "Product",
  risk_management:  "Risk Mgmt",
};

function ScoreBar({ label, value, color = "bg-indigo-500" }: { label: string; value: number; color?: string }) {
  return (
    <div>
      <div className="flex justify-between text-xs mb-1">
        <span className="text-slate-400">{label}</span>
        <span className="text-slate-200 font-mono">{value.toFixed(1)}</span>
      </div>
      <div className="h-1.5 rounded-full bg-slate-800">
        <div className={`h-1.5 rounded-full ${color}`} style={{ width: `${Math.min(value, 100)}%` }} />
      </div>
    </div>
  );
}

function CompositeRing({ composite }: { composite: number }) {
  const r = 36;
  const circ = 2 * Math.PI * r;
  const fill = (composite / 100) * circ;
  const color = composite >= 60 ? "#f87171" : composite >= 40 ? "#fb923c" : composite >= 20 ? "#fbbf24" : "#34d399";
  return (
    <svg viewBox="0 0 88 88" className="w-20 h-20">
      <circle cx="44" cy="44" r={r} fill="none" stroke="#1e293b" strokeWidth="8" />
      <circle
        cx="44" cy="44" r={r} fill="none"
        stroke={color} strokeWidth="8"
        strokeDasharray={`${fill} ${circ}`}
        strokeLinecap="round"
        transform="rotate(-90 44 44)"
      />
      <text x="44" y="49" textAnchor="middle" fontSize="14" fontWeight="700" fill={color}>
        {composite.toFixed(0)}
      </text>
    </svg>
  );
}

function DetailModal({ pipeline, onClose }: { pipeline: DataPipeline; onClose: () => void }) {
  const [tab, setTab] = useState<"overview" | "scores" | "action">("overview");
  useEffect(() => {
    const handler = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [onClose]);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm" onClick={onClose}>
      <div className="relative bg-slate-900 border border-slate-700 rounded-2xl shadow-2xl w-full max-w-lg mx-4 overflow-hidden" onClick={(e) => e.stopPropagation()}>
        <div className="flex items-center justify-between px-6 py-4 border-b border-slate-800">
          <div>
            <p className="text-xs text-slate-500 uppercase tracking-widest">Data Analytics Intelligence</p>
            <h2 className="text-lg font-bold text-slate-100">{pipeline.pipeline_id}</h2>
            <p className="text-xs text-slate-400">
              {pipeline.region} · {DOMAIN_LABELS[pipeline.data_domain] ?? pipeline.data_domain} · {PATTERN_LABELS[pipeline.data_pattern]}
            </p>
          </div>
          <div className="flex flex-col items-end gap-1">
            <span className={`text-xs font-semibold px-2 py-0.5 rounded-full border ${RISK_BG[pipeline.data_risk]}`}>
              <span className={RISK_COLORS[pipeline.data_risk]}>{pipeline.data_risk.toUpperCase()}</span>
            </span>
            <span className={`text-xs px-2 py-0.5 rounded-full text-white ${SEV_COLORS[pipeline.data_severity]}`}>
              {pipeline.data_severity}
            </span>
            <button onClick={onClose} className="text-slate-500 hover:text-slate-200 text-xl leading-none mt-1">×</button>
          </div>
        </div>

        <div className="flex border-b border-slate-800">
          {(["overview", "scores", "action"] as const).map((t) => (
            <button key={t} onClick={() => setTab(t)}
              className={`flex-1 py-2 text-xs font-semibold uppercase tracking-widest transition-colors ${tab === t ? "text-indigo-400 border-b-2 border-indigo-400" : "text-slate-500 hover:text-slate-300"}`}>
              {t}
            </button>
          ))}
        </div>

        <div className="px-6 py-5 space-y-4">
          {tab === "overview" && (
            <>
              <div className="flex items-center justify-center py-2">
                <CompositeRing composite={pipeline.data_composite} />
              </div>
              <p className="text-sm text-slate-300 italic text-center">&ldquo;{pipeline.data_signal}&rdquo;</p>
              <div className="grid grid-cols-2 gap-3 text-xs">
                <div className="bg-slate-800 rounded-lg p-3">
                  <p className="text-slate-500 mb-1">Composite Score</p>
                  <p className="text-slate-100 font-bold text-base">{pipeline.data_composite.toFixed(1)}</p>
                </div>
                <div className="bg-slate-800 rounded-lg p-3">
                  <p className="text-slate-500 mb-1">Insight Delay</p>
                  <p className="text-indigo-400 font-bold text-base">{pipeline.estimated_insight_delay_hours.toFixed(2)}h</p>
                </div>
                <div className="bg-slate-800 rounded-lg p-3">
                  <p className="text-slate-500 mb-1">Data Alert</p>
                  <p className={`font-bold ${pipeline.has_data_alert ? "text-orange-400" : "text-emerald-400"}`}>
                    {pipeline.has_data_alert ? "Active" : "Clear"}
                  </p>
                </div>
                <div className="bg-slate-800 rounded-lg p-3">
                  <p className="text-slate-500 mb-1">Governance</p>
                  <p className={`font-bold ${pipeline.requires_data_governance ? "text-violet-400" : "text-emerald-400"}`}>
                    {pipeline.requires_data_governance ? "Required" : "Not needed"}
                  </p>
                </div>
              </div>
            </>
          )}
          {tab === "scores" && (
            <div className="space-y-3">
              <ScoreBar label="Pipeline Health" value={pipeline.pipeline_score} color="bg-indigo-500" />
              <ScoreBar label="Data Quality" value={pipeline.quality_score} color="bg-violet-500" />
              <ScoreBar label="Analytics" value={pipeline.analytics_score} color="bg-sky-500" />
              <ScoreBar label="Governance" value={pipeline.governance_score} color="bg-amber-500" />
              <div className="pt-2 border-t border-slate-800">
                <ScoreBar label="Data Composite" value={pipeline.data_composite} color="bg-indigo-600" />
              </div>
            </div>
          )}
          {tab === "action" && (
            <div className="space-y-3 text-sm">
              <div className="bg-slate-800 rounded-lg p-4">
                <p className="text-slate-500 text-xs mb-1">Recommended Action</p>
                <p className={`font-semibold ${ACTION_COLORS[pipeline.recommended_action]}`}>{ACTION_LABELS[pipeline.recommended_action]}</p>
              </div>
              <div className="bg-slate-800 rounded-lg p-4">
                <p className="text-slate-500 text-xs mb-1">Data Pattern</p>
                <p className="text-slate-200">{PATTERN_LABELS[pipeline.data_pattern]}</p>
              </div>
              <div className="bg-slate-800 rounded-lg p-4">
                <p className="text-slate-500 text-xs mb-1">Domain</p>
                <p className="text-slate-200">{DOMAIN_LABELS[pipeline.data_domain] ?? pipeline.data_domain}</p>
              </div>
              <div className="bg-slate-800 rounded-lg p-4">
                <p className="text-slate-500 text-xs mb-2">Status Flags</p>
                <div className="flex flex-wrap gap-2">
                  {pipeline.has_data_alert && (
                    <span className="text-xs px-2 py-0.5 rounded-full bg-orange-400/10 border border-orange-400/30 text-orange-400">Data Alert</span>
                  )}
                  {pipeline.requires_data_governance && (
                    <span className="text-xs px-2 py-0.5 rounded-full bg-violet-400/10 border border-violet-400/30 text-violet-400">Governance Review</span>
                  )}
                  {!pipeline.has_data_alert && !pipeline.requires_data_governance && (
                    <span className="text-xs text-slate-500">No critical flags</span>
                  )}
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default function DataAnalyticsIntelligenceEnginePage() {
  const [data, setData] = useState<{ pipelines: DataPipeline[]; summary: Summary } | null>(null);
  const [selected, setSelected] = useState<DataPipeline | null>(null);
  const [riskFilter, setRiskFilter] = useState("all");
  const [patternFilter, setPatternFilter] = useState("all");

  const load = useCallback(async () => {
    const params = new URLSearchParams();
    if (riskFilter !== "all")    params.set("risk", riskFilter);
    if (patternFilter !== "all") params.set("pattern", patternFilter);
    const res = await fetch(`/api/data-analytics-intelligence-engine?${params}`);
    setData(await res.json());
  }, [riskFilter, patternFilter]);

  useEffect(() => { load(); }, [load]);

  const summary = data?.summary;
  const pipelines = data?.pipelines ?? [];

  const kpis = summary
    ? [
        { label: "Total Pipelines", value: summary.total, sub: "monitored" },
        { label: "Data Alerts", value: summary.data_alert_count, sub: "active alerts", accent: "text-orange-400" },
        { label: "Governance Reviews", value: summary.governance_count, sub: "required", accent: "text-violet-400" },
        { label: "Avg Composite", value: summary.avg_data_composite.toFixed(1), sub: "risk score" },
        { label: "Avg Insight Delay", value: `${summary.avg_estimated_insight_delay_hours.toFixed(2)}h`, sub: "pipeline lag impact", accent: "text-indigo-400" },
      ]
    : [];

  const patterns = summary
    ? Object.entries(summary.pattern_counts).sort((a, b) => b[1] - a[1])
    : [];

  const allPatterns = ["none", "pipeline_failure", "data_drift", "quality_degradation", "model_staleness", "insight_gap"];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {selected && <DetailModal pipeline={selected} onClose={() => setSelected(null)} />}

      <div>
        <h1 className="text-2xl font-bold text-slate-100">Data Analytics Intelligence Engine</h1>
        <p className="text-sm text-slate-400 mt-1">
          Monitors pipeline health, data quality, analytics performance, and governance across all data domains
        </p>
      </div>

      {/* KPI Strip */}
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-4">
        {kpis.map((k) => (
          <div key={k.label} className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <p className="text-xs text-slate-500 uppercase tracking-widest mb-1">{k.label}</p>
            <p className={`text-2xl font-bold ${k.accent ?? "text-slate-100"}`}>{k.value}</p>
            <p className="text-xs text-slate-500 mt-0.5">{k.sub}</p>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Sub-score averages */}
        {summary && (
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-3">
            <h2 className="text-sm font-semibold text-slate-300 uppercase tracking-widest mb-3">Avg Risk Scores</h2>
            <ScoreBar label="Pipeline Health" value={summary.avg_pipeline_score} color="bg-indigo-500" />
            <ScoreBar label="Data Quality" value={summary.avg_quality_score} color="bg-violet-500" />
            <ScoreBar label="Analytics" value={summary.avg_analytics_score} color="bg-sky-500" />
            <ScoreBar label="Governance" value={summary.avg_governance_score} color="bg-amber-500" />
            <ScoreBar label="Data Composite" value={summary.avg_data_composite} color="bg-indigo-600" />
          </div>
        )}

        {/* Pattern distribution */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
          <h2 className="text-sm font-semibold text-slate-300 uppercase tracking-widest mb-4">Data Patterns</h2>
          <div className="space-y-2">
            {patterns.map(([pat, count]) => (
              <div key={pat} className="flex items-center gap-3">
                <span className="text-xs text-slate-400 w-44 truncate">{PATTERN_LABELS[pat] ?? pat}</span>
                <div className="flex-1 h-2 bg-slate-800 rounded-full">
                  <div
                    className="h-2 rounded-full bg-indigo-500"
                    style={{ width: summary ? `${(count / summary.total) * 100}%` : "0%" }}
                  />
                </div>
                <span className="text-xs font-mono text-slate-300 w-4 text-right">{count}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Filters */}
      <div className="space-y-3">
        <div className="flex gap-2 flex-wrap">
          <span className="text-xs text-slate-500 self-center mr-1">Risk:</span>
          {["all", "low", "moderate", "high", "critical"].map((f) => (
            <button key={f} onClick={() => setRiskFilter(f)}
              className={`px-4 py-1.5 rounded-full text-xs font-semibold border transition-colors ${
                riskFilter === f
                  ? "bg-indigo-700 border-indigo-600 text-white"
                  : "bg-slate-800 border-slate-700 text-slate-400 hover:text-slate-200"
              }`}>
              {f === "all" ? "All" : f.charAt(0).toUpperCase() + f.slice(1)}
            </button>
          ))}
        </div>
        <div className="flex gap-2 flex-wrap">
          <span className="text-xs text-slate-500 self-center mr-1">Pattern:</span>
          {["all", ...allPatterns].map((f) => (
            <button key={f} onClick={() => setPatternFilter(f)}
              className={`px-4 py-1.5 rounded-full text-xs font-semibold border transition-colors ${
                patternFilter === f
                  ? "bg-violet-700 border-violet-600 text-white"
                  : "bg-slate-800 border-slate-700 text-slate-400 hover:text-slate-200"
              }`}>
              {f === "all" ? "All" : (PATTERN_LABELS[f] ?? f)}
            </button>
          ))}
        </div>
      </div>

      {/* Pipeline Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
        {pipelines.map((pipeline) => (
          <button key={pipeline.pipeline_id} onClick={() => setSelected(pipeline)}
            className={`bg-slate-900 border rounded-xl p-4 text-left transition-colors group ${
              pipeline.data_risk === "critical"
                ? "border-red-500/40 hover:border-red-400/60"
                : "border-slate-800 hover:border-indigo-700"
            }`}>
            <div className="flex items-start justify-between mb-3">
              <div>
                <p className="font-semibold text-slate-100 group-hover:text-indigo-300 transition-colors">{pipeline.pipeline_id}</p>
                <p className="text-xs text-slate-500">{pipeline.region} · <span className="text-indigo-400">{DOMAIN_LABELS[pipeline.data_domain] ?? pipeline.data_domain}</span></p>
              </div>
              <div className="flex flex-col items-end gap-1">
                <span className={`text-xs font-semibold ${RISK_COLORS[pipeline.data_risk]}`}>
                  {pipeline.data_risk.toUpperCase()}
                </span>
                <span className={`text-xs px-1.5 py-0.5 rounded text-white ${SEV_COLORS[pipeline.data_severity]}`}>
                  {pipeline.data_severity}
                </span>
              </div>
            </div>
            <div className="flex items-center gap-3 mb-3">
              <CompositeRing composite={pipeline.data_composite} />
              <div className="flex-1 space-y-1.5">
                <ScoreBar label="Pipeline" value={pipeline.pipeline_score} color="bg-indigo-500" />
                <ScoreBar label="Quality" value={pipeline.quality_score} color="bg-violet-500" />
                <ScoreBar label="Analytics" value={pipeline.analytics_score} color="bg-sky-500" />
              </div>
            </div>
            <p className="text-xs text-slate-400 italic leading-snug line-clamp-2">{pipeline.data_signal}</p>
            <div className="flex items-center justify-between mt-3">
              <div className="flex gap-2 flex-wrap">
                {pipeline.has_data_alert && (
                  <span className="text-xs px-2 py-0.5 rounded-full bg-orange-400/10 border border-orange-400/30 text-orange-400">Alert</span>
                )}
                {pipeline.requires_data_governance && (
                  <span className="text-xs px-2 py-0.5 rounded-full bg-violet-400/10 border border-violet-400/30 text-violet-400">Governance</span>
                )}
                <span className={`text-xs px-2 py-0.5 rounded-full bg-slate-800 ${ACTION_COLORS[pipeline.recommended_action]}`}>
                  {ACTION_LABELS[pipeline.recommended_action]}
                </span>
              </div>
              <span className="text-xs text-slate-500 font-mono">{pipeline.estimated_insight_delay_hours.toFixed(2)}h</span>
            </div>
          </button>
        ))}
      </div>
    </div>
  );
}
