"use client";

import { useEffect, useState } from "react";

interface VelocityDeal {
  deal_id: string;
  rep_id: string;
  velocity_anomaly: string;
  velocity_risk: string;
  velocity_alert: string;
  velocity_severity: string;
  stage_completion_score: number;
  timeline_deviation_score: number;
  forecast_integrity_score: number;
  pattern_risk_score: number;
  velocity_composite: number;
  is_anomalous: boolean;
  requires_review: boolean;
  pipeline_days_deviation: number;
  velocity_signal: string;
}

interface Summary {
  total: number;
  anomaly_counts: Record<string, number>;
  risk_counts: Record<string, number>;
  alert_counts: Record<string, number>;
  severity_counts: Record<string, number>;
  avg_velocity_composite: number;
  anomalous_count: number;
  review_required_count: number;
  avg_stage_completion_score: number;
  avg_timeline_deviation_score: number;
  avg_forecast_integrity_score: number;
  avg_pattern_risk_score: number;
  avg_pipeline_days_deviation: number;
}

const ANOMALY_COLORS: Record<string, string> = {
  normal:         "text-emerald-400",
  suspicious_fast:"text-amber-400",
  stage_skipping: "text-orange-400",
  stalled:        "text-sky-400",
  recycled:       "text-violet-400",
  forced_close:   "text-red-400",
};

const RISK_COLORS: Record<string, string> = {
  low:      "text-emerald-400",
  moderate: "text-amber-400",
  high:     "text-orange-400",
  critical: "text-red-400",
};

const RISK_BG: Record<string, string> = {
  low:      "bg-emerald-500/20 border-emerald-500/40",
  moderate: "bg-amber-500/20 border-amber-500/40",
  high:     "bg-orange-500/20 border-orange-500/40",
  critical: "bg-red-500/20 border-red-500/40",
};

const SEVERITY_BG: Record<string, string> = {
  clean:       "bg-emerald-500/10 text-emerald-300",
  watch:       "bg-amber-500/10 text-amber-300",
  anomalous:   "bg-orange-500/10 text-orange-300",
  fraud_risk:  "bg-red-500/10 text-red-300",
};

const ALERT_BADGE: Record<string, string> = {
  none:     "bg-slate-700 text-slate-300",
  flag:     "bg-amber-500/20 text-amber-300",
  review:   "bg-orange-500/20 text-orange-300",
  escalate: "bg-red-500/20 text-red-300",
  audit:    "bg-red-700/40 text-red-200 border border-red-500/50",
};

function CompositeRing({ value }: { value: number }) {
  const r = 28;
  const circ = 2 * Math.PI * r;
  const fill = (value / 100) * circ;
  const color = value >= 65 ? "#ef4444" : value >= 40 ? "#f97316" : value >= 20 ? "#f59e0b" : "#10b981";
  return (
    <svg width="72" height="72" viewBox="0 0 72 72">
      <circle cx="36" cy="36" r={r} fill="none" stroke="#1e293b" strokeWidth="6" />
      <circle cx="36" cy="36" r={r} fill="none" stroke={color} strokeWidth="6"
        strokeDasharray={`${fill} ${circ}`} strokeLinecap="round"
        transform="rotate(-90 36 36)" />
      <text x="36" y="40" textAnchor="middle" fill={color} fontSize="13" fontWeight="bold">{value.toFixed(0)}</text>
    </svg>
  );
}

function ScoreBar({ label, value, color }: { label: string; value: number; color: string }) {
  return (
    <div>
      <div className="flex justify-between text-xs mb-1">
        <span className="text-slate-400">{label}</span>
        <span className={color}>{value.toFixed(1)}</span>
      </div>
      <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
        <div className={`h-full rounded-full ${color.replace("text-", "bg-")}`}
          style={{ width: `${Math.min(value, 100)}%` }} />
      </div>
    </div>
  );
}

function DetailModal({ deal, onClose }: { deal: VelocityDeal; onClose: () => void }) {
  const [tab, setTab] = useState<"overview" | "scores" | "action">("overview");

  useEffect(() => {
    const handler = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [onClose]);

  const tabs = [
    { id: "overview" as const, label: "Overview" },
    { id: "scores"   as const, label: "Velocity Scores" },
    { id: "action"   as const, label: "Action" },
  ];

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4"
      onClick={onClose}>
      <div className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-lg shadow-2xl"
        onClick={(e) => e.stopPropagation()}>
        {/* Header */}
        <div className="p-6 border-b border-slate-800">
          <div className="flex items-start justify-between gap-4">
            <div>
              <p className="text-xs text-slate-500 mb-1">Deal ID · {deal.deal_id}</p>
              <h2 className="text-lg font-bold text-white">{deal.rep_id}</h2>
              <div className="flex items-center gap-2 mt-2 flex-wrap">
                <span className={`text-xs px-2 py-0.5 rounded-full border ${RISK_BG[deal.velocity_risk]}`}>
                  {deal.velocity_risk.toUpperCase()} RISK
                </span>
                <span className={`text-xs px-2 py-0.5 rounded-full ${SEVERITY_BG[deal.velocity_severity]}`}>
                  {deal.velocity_severity.replace("_", " ")}
                </span>
                <span className={`text-xs px-2 py-0.5 rounded-full ${ALERT_BADGE[deal.velocity_alert]}`}>
                  {deal.velocity_alert.toUpperCase()}
                </span>
              </div>
            </div>
            <CompositeRing value={deal.velocity_composite} />
          </div>
        </div>

        {/* Tabs */}
        <div className="flex border-b border-slate-800">
          {tabs.map((t) => (
            <button key={t.id} onClick={() => setTab(t.id)}
              className={`flex-1 py-3 text-xs font-medium transition-colors ${
                tab === t.id ? "text-indigo-400 border-b-2 border-indigo-400" : "text-slate-500 hover:text-slate-300"
              }`}>
              {t.label}
            </button>
          ))}
        </div>

        {/* Content */}
        <div className="p-6">
          {tab === "overview" && (
            <div className="space-y-4">
              <div className="grid grid-cols-2 gap-3">
                <div className="bg-slate-800/60 rounded-lg p-3">
                  <p className="text-xs text-slate-500">Anomaly Type</p>
                  <p className={`text-sm font-semibold mt-1 ${ANOMALY_COLORS[deal.velocity_anomaly]}`}>
                    {deal.velocity_anomaly.replace(/_/g, " ")}
                  </p>
                </div>
                <div className="bg-slate-800/60 rounded-lg p-3">
                  <p className="text-xs text-slate-500">Pipeline Deviation</p>
                  <p className={`text-sm font-semibold mt-1 ${deal.pipeline_days_deviation < 0 ? "text-amber-400" : "text-sky-400"}`}>
                    {deal.pipeline_days_deviation > 0 ? "+" : ""}{deal.pipeline_days_deviation.toFixed(0)} days
                  </p>
                </div>
                <div className="bg-slate-800/60 rounded-lg p-3">
                  <p className="text-xs text-slate-500">Is Anomalous</p>
                  <p className={`text-sm font-semibold mt-1 ${deal.is_anomalous ? "text-red-400" : "text-emerald-400"}`}>
                    {deal.is_anomalous ? "Yes" : "No"}
                  </p>
                </div>
                <div className="bg-slate-800/60 rounded-lg p-3">
                  <p className="text-xs text-slate-500">Requires Review</p>
                  <p className={`text-sm font-semibold mt-1 ${deal.requires_review ? "text-orange-400" : "text-emerald-400"}`}>
                    {deal.requires_review ? "Yes" : "No"}
                  </p>
                </div>
              </div>
              <div className="bg-slate-800/40 rounded-lg p-3 border-l-2 border-indigo-500">
                <p className="text-xs text-slate-400 italic">{deal.velocity_signal}</p>
              </div>
            </div>
          )}

          {tab === "scores" && (
            <div className="space-y-3">
              <ScoreBar label="Stage Completion Score" value={deal.stage_completion_score} color="text-violet-400" />
              <ScoreBar label="Timeline Deviation Score" value={deal.timeline_deviation_score} color="text-amber-400" />
              <ScoreBar label="Forecast Integrity Score" value={deal.forecast_integrity_score} color="text-orange-400" />
              <ScoreBar label="Pattern Risk Score" value={deal.pattern_risk_score} color="text-red-400" />
              <div className="pt-2 border-t border-slate-800">
                <div className="flex justify-between text-sm">
                  <span className="text-slate-400 font-medium">Velocity Composite</span>
                  <span className="text-white font-bold">{deal.velocity_composite.toFixed(1)}</span>
                </div>
                <p className="text-xs text-slate-600 mt-1">stage×0.25 + timeline×0.35 + forecast×0.25 + pattern×0.15</p>
              </div>
            </div>
          )}

          {tab === "action" && (
            <div className="space-y-4">
              <div className={`rounded-xl p-4 border ${RISK_BG[deal.velocity_risk]}`}>
                <p className="text-xs text-slate-400 mb-1">Recommended Alert</p>
                <p className={`text-xl font-bold ${RISK_COLORS[deal.velocity_risk]}`}>
                  {deal.velocity_alert.toUpperCase()}
                </p>
              </div>
              <div className="bg-slate-800/40 rounded-lg p-3 space-y-2">
                <div className="flex justify-between text-xs">
                  <span className="text-slate-400">Velocity Severity</span>
                  <span className={SEVERITY_BG[deal.velocity_severity].split(" ")[1]}>
                    {deal.velocity_severity.replace("_", " ")}
                  </span>
                </div>
                <div className="flex justify-between text-xs">
                  <span className="text-slate-400">Composite Score</span>
                  <span className="text-white">{deal.velocity_composite.toFixed(1)} / 100</span>
                </div>
              </div>
            </div>
          )}
        </div>

        <div className="px-6 pb-6">
          <button onClick={onClose}
            className="w-full py-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 text-sm transition-colors">
            Close
          </button>
        </div>
      </div>
    </div>
  );
}

export default function SalesProcessVelocityAnomalyPage() {
  const [data, setData] = useState<{ deals: VelocityDeal[]; summary: Summary } | null>(null);
  const [loading, setLoading] = useState(true);
  const [anomalyFilter, setAnomalyFilter] = useState<string>("");
  const [riskFilter, setRiskFilter]       = useState<string>("");
  const [selected, setSelected] = useState<VelocityDeal | null>(null);

  useEffect(() => {
    async function load() {
        setLoading(true);
        const params = new URLSearchParams();
        if (anomalyFilter) params.set("anomaly", anomalyFilter);
        if (riskFilter)    params.set("risk",    riskFilter);
        const res  = await fetch(`/api/sales-process-velocity-anomaly-engine?${params}`);
        const json = await res.json();
        setData(json);
        setLoading(false);
  }
    load();
  }, [anomalyFilter, riskFilter]);

  const s = data?.summary;
  const deals = data?.deals ?? [];

  const anomalyTypes = ["normal", "suspicious_fast", "stage_skipping", "stalled", "recycled", "forced_close"];
  const riskLevels   = ["low", "moderate", "high", "critical"];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
      <div className="max-w-7xl mx-auto space-y-6">

        {/* Header */}
        <div>
          <h1 className="text-2xl font-bold text-white">Sales Process Velocity Anomaly Engine</h1>
          <p className="text-slate-400 text-sm mt-1">
            Detects abnormally fast or slow deal progression signaling gaming, misclassification, or forecast manipulation
          </p>
        </div>

        {/* KPI Strip */}
        {s && (
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {[
              { label: "Total Deals",        value: s.total,                  sub: "analyzed" },
              { label: "Anomalous",          value: s.anomalous_count,        sub: "detected" },
              { label: "Review Required",    value: s.review_required_count,  sub: "flagged" },
              { label: "Avg Composite",      value: s.avg_velocity_composite, sub: "velocity score" },
            ].map((k) => (
              <div key={k.label} className="bg-slate-900 border border-slate-800 rounded-xl p-4">
                <p className="text-xs text-slate-500">{k.label}</p>
                <p className="text-2xl font-bold text-white mt-1">{k.value}</p>
                <p className="text-xs text-slate-600 mt-0.5">{k.sub}</p>
              </div>
            ))}
          </div>
        )}

        {/* Avg Sub-score Bars + Distributions */}
        {s && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* Avg sub-scores */}
            <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
              <h2 className="text-sm font-semibold text-slate-300 mb-4">Average Sub-Scores</h2>
              <div className="space-y-3">
                {[
                  { label: "Stage Completion",    value: s.avg_stage_completion_score,    color: "text-violet-400" },
                  { label: "Timeline Deviation",  value: s.avg_timeline_deviation_score,  color: "text-amber-400" },
                  { label: "Forecast Integrity",  value: s.avg_forecast_integrity_score,  color: "text-orange-400" },
                  { label: "Pattern Risk",        value: s.avg_pattern_risk_score,        color: "text-red-400" },
                ].map((item) => (
                  <ScoreBar key={item.label} label={item.label} value={item.value} color={item.color} />
                ))}
              </div>
            </div>

            {/* Anomaly distribution */}
            <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
              <h2 className="text-sm font-semibold text-slate-300 mb-4">Anomaly Distribution</h2>
              <div className="space-y-2">
                {anomalyTypes.filter((a) => s.anomaly_counts[a]).map((a) => {
                  const count = s.anomaly_counts[a] || 0;
                  const pct   = (count / s.total) * 100;
                  return (
                    <div key={a}>
                      <div className="flex justify-between text-xs mb-1">
                        <span className={ANOMALY_COLORS[a]}>{a.replace(/_/g, " ")}</span>
                        <span className="text-slate-400">{count}</span>
                      </div>
                      <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
                        <div className={`h-full rounded-full ${(ANOMALY_COLORS[a] || "text-slate-400").replace("text-", "bg-")}`}
                          style={{ width: `${pct}%` }} />
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          </div>
        )}

        {/* Filters */}
        <div className="flex flex-wrap gap-3">
          <div>
            <p className="text-xs text-slate-500 mb-1">Anomaly Type</p>
            <div className="flex flex-wrap gap-1">
              {["", ...anomalyTypes].map((a) => (
                <button key={a || "all"} onClick={() => setAnomalyFilter(a)}
                  className={`px-3 py-1 rounded-full text-xs transition-colors ${
                    anomalyFilter === a
                      ? "bg-indigo-600 text-white"
                      : "bg-slate-800 text-slate-400 hover:bg-slate-700"
                  }`}>
                  {a ? a.replace(/_/g, " ") : "All"}
                </button>
              ))}
            </div>
          </div>
          <div>
            <p className="text-xs text-slate-500 mb-1">Risk Level</p>
            <div className="flex flex-wrap gap-1">
              {["", ...riskLevels].map((r) => (
                <button key={r || "all"} onClick={() => setRiskFilter(r)}
                  className={`px-3 py-1 rounded-full text-xs transition-colors ${
                    riskFilter === r
                      ? "bg-indigo-600 text-white"
                      : "bg-slate-800 text-slate-400 hover:bg-slate-700"
                  }`}>
                  {r || "All"}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Deal Cards */}
        {loading ? (
          <div className="flex items-center justify-center h-40">
            <div className="w-8 h-8 border-2 border-indigo-500 border-t-transparent rounded-full animate-spin" />
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
            {deals.map((deal) => (
              <button key={deal.deal_id} onClick={() => setSelected(deal)} className="text-left w-full">
                <div className={`bg-slate-900 border rounded-xl p-4 hover:border-indigo-500 transition-colors cursor-pointer ${
                  deal.is_anomalous ? "border-orange-500/40" : "border-slate-800"
                }`}>
                  <div className="flex items-start justify-between gap-3 mb-3">
                    <div className="min-w-0">
                      <div className="flex items-center gap-2 flex-wrap mb-1">
                        <span className={`text-xs px-2 py-0.5 rounded-full border ${RISK_BG[deal.velocity_risk]}`}>
                          {deal.velocity_risk}
                        </span>
                        <span className={`text-xs ${ANOMALY_COLORS[deal.velocity_anomaly]}`}>
                          {deal.velocity_anomaly.replace(/_/g, " ")}
                        </span>
                      </div>
                      <p className="text-sm font-semibold text-white truncate">{deal.deal_id}</p>
                      <p className="text-xs text-slate-500">{deal.rep_id}</p>
                    </div>
                    <CompositeRing value={deal.velocity_composite} />
                  </div>

                  {/* Sub-score bars */}
                  <div className="space-y-1.5 mb-3">
                    <ScoreBar label="Stage"    value={deal.stage_completion_score}    color="text-violet-400" />
                    <ScoreBar label="Timeline" value={deal.timeline_deviation_score}  color="text-amber-400" />
                    <ScoreBar label="Forecast" value={deal.forecast_integrity_score}  color="text-orange-400" />
                    <ScoreBar label="Pattern"  value={deal.pattern_risk_score}        color="text-red-400" />
                  </div>

                  <div className="flex items-center justify-between">
                    <span className={`text-xs px-2 py-0.5 rounded-full ${ALERT_BADGE[deal.velocity_alert]}`}>
                      {deal.velocity_alert}
                    </span>
                    <span className={`text-xs px-2 py-0.5 rounded-full ${SEVERITY_BG[deal.velocity_severity]}`}>
                      {deal.velocity_severity.replace("_", " ")}
                    </span>
                  </div>

                  <p className="text-xs text-slate-500 mt-2 line-clamp-2 italic">{deal.velocity_signal}</p>
                </div>
              </button>
            ))}
          </div>
        )}
      </div>

      {selected && <DetailModal deal={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
