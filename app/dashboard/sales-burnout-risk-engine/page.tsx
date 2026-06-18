"use client";

import { useState, useEffect, useRef, useCallback } from "react";

interface RepData {
  rep_id: string;
  rep_name: string;
  region: string;
  burnout_risk: string;
  burnout_stage: string;
  primary_burnout_signal: string;
  burnout_action: string;
  activity_health_score: number;
  wellbeing_score: number;
  performance_sustainability_score: number;
  social_engagement_score: number;
  burnout_composite: number;
  is_at_burnout_risk: boolean;
  needs_immediate_support: boolean;
  estimated_productivity_impact_pct: number;
  burnout_signal: string;
}

interface Summary {
  total: number;
  risk_counts: Record<string, number>;
  stage_counts: Record<string, number>;
  signal_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_burnout_composite: number;
  at_burnout_risk_count: number;
  immediate_support_count: number;
  avg_activity_health_score: number;
  avg_wellbeing_score: number;
  avg_performance_sustainability_score: number;
  avg_social_engagement_score: number;
  total_productivity_impact_pct: number;
}

const RISK_BG: Record<string, string> = {
  none:          "bg-emerald-500/20 border-emerald-500/30 text-emerald-300",
  early_warning: "bg-sky-500/20 border-sky-500/30 text-sky-300",
  moderate:      "bg-amber-500/20 border-amber-500/30 text-amber-300",
  high:          "bg-orange-500/20 border-orange-500/30 text-orange-300",
  critical:      "bg-rose-500/20 border-rose-500/30 text-rose-300",
};
const RISK_COLOR: Record<string, string> = {
  none:          "#34d399",
  early_warning: "#38bdf8",
  moderate:      "#fbbf24",
  high:          "#f97316",
  critical:      "#f87171",
};
const RISK_LABEL: Record<string, string> = {
  none:          "Healthy",
  early_warning: "Early Warning",
  moderate:      "Moderate",
  high:          "High Risk",
  critical:      "Critical",
};
const STAGE_BG: Record<string, string> = {
  engaged:      "bg-emerald-500/15 text-emerald-300",
  coasting:     "bg-sky-500/15 text-sky-300",
  disengaging:  "bg-amber-500/15 text-amber-300",
  burned_out:   "bg-orange-500/15 text-orange-300",
  depleted:     "bg-rose-500/15 text-rose-300",
};
const STAGE_LABEL: Record<string, string> = {
  engaged:      "Engaged",
  coasting:     "Coasting",
  disengaging:  "Disengaging",
  burned_out:   "Burned Out",
  depleted:     "Depleted",
};
const ACTION_BG: Record<string, string> = {
  monitor:              "bg-emerald-500/15 text-emerald-300",
  check_in:             "bg-sky-500/15 text-sky-300",
  coaching_session:     "bg-amber-500/15 text-amber-300",
  workload_reduction:   "bg-orange-500/15 text-orange-300",
  urgent_intervention:  "bg-rose-500/15 text-rose-300",
};
const ACTION_LABEL: Record<string, string> = {
  monitor:              "Monitor",
  check_in:             "Check In",
  coaching_session:     "Coaching Session",
  workload_reduction:   "Workload Reduction",
  urgent_intervention:  "Urgent Intervention",
};

function RiskGauge({ pct, color, size = 80 }: { pct: number; color: string; size?: number }) {
  const r = size * 0.38;
  const circ = 2 * Math.PI * r;
  const fill = (pct / 100) * circ;
  return (
    <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`}>
      <circle cx={size / 2} cy={size / 2} r={r} fill="none" stroke="#1e293b" strokeWidth={size * 0.1} />
      <circle
        cx={size / 2} cy={size / 2} r={r} fill="none"
        stroke={color} strokeWidth={size * 0.1}
        strokeDasharray={`${fill} ${circ}`}
        strokeLinecap="round"
        transform={`rotate(-90 ${size / 2} ${size / 2})`}
      />
      <text x={size / 2} y={size / 2 + 5} textAnchor="middle" fill={color} fontSize={size * 0.22} fontWeight="bold">
        {pct.toFixed(0)}
      </text>
    </svg>
  );
}

function HealthBar({ score, label }: { score: number; label: string }) {
  const color = score >= 70 ? "#34d399" : score >= 50 ? "#fbbf24" : "#f87171";
  return (
    <div>
      <div className="flex justify-between mb-1">
        <span className="text-xs text-slate-400">{label}</span>
        <span className="text-xs font-medium" style={{ color }}>{score.toFixed(0)}</span>
      </div>
      <div className="h-1.5 bg-slate-700 rounded-full overflow-hidden">
        <div className="h-full rounded-full transition-all" style={{ width: `${score}%`, backgroundColor: color }} />
      </div>
    </div>
  );
}

interface ModalProps { rep: RepData; onClose: () => void }

function DetailModal({ rep, onClose }: ModalProps) {
  const [tab, setTab] = useState<"overview" | "scores" | "action">("overview");
  const backdropRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handler = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [onClose]);

  const riskColor = RISK_COLOR[rep.burnout_risk] ?? "#94a3b8";

  return (
    <div
      ref={backdropRef}
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4"
      onClick={(e) => { if (e.target === backdropRef.current) onClose(); }}
    >
      <div className="bg-slate-900 border border-slate-700 rounded-xl shadow-2xl w-full max-w-lg">
        {/* Header */}
        <div className="flex items-start justify-between p-5 border-b border-slate-800">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <span className={`text-xs px-2 py-0.5 rounded-full border font-medium ${RISK_BG[rep.burnout_risk] ?? ""}`}>
                {RISK_LABEL[rep.burnout_risk] ?? rep.burnout_risk}
              </span>
              <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${STAGE_BG[rep.burnout_stage] ?? ""}`}>
                {STAGE_LABEL[rep.burnout_stage] ?? rep.burnout_stage}
              </span>
            </div>
            <h2 className="text-white font-bold text-lg">{rep.rep_name}</h2>
            <p className="text-slate-400 text-sm">{rep.region} Region · Composite Risk: <span style={{ color: riskColor }}>{rep.burnout_composite}</span></p>
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-white p-1 transition-colors" aria-label="Close">
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        {/* Tabs */}
        <div className="flex border-b border-slate-800">
          {(["overview", "scores", "action"] as const).map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`flex-1 py-2.5 text-sm font-medium capitalize transition-colors ${
                tab === t ? "text-indigo-400 border-b-2 border-indigo-500 bg-slate-800/40" : "text-slate-400 hover:text-slate-200"
              }`}
            >
              {t === "overview" ? "Overview" : t === "scores" ? "Health Scores" : "Action Plan"}
            </button>
          ))}
        </div>

        {/* Body */}
        <div className="p-5 space-y-4">
          {tab === "overview" && (
            <>
              <div className="flex items-center justify-center py-3">
                <RiskGauge pct={rep.burnout_composite} color={riskColor} size={110} />
              </div>
              <div className="bg-slate-800/50 rounded-lg p-3">
                <p className="text-xs text-slate-400 mb-1">Primary Burnout Signal</p>
                <p className="text-sm text-white">{rep.burnout_signal}</p>
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div className="bg-slate-800/50 rounded-lg p-3">
                  <p className="text-xs text-slate-400">Productivity Impact</p>
                  <p className="text-lg font-bold text-rose-400">-{rep.estimated_productivity_impact_pct.toFixed(1)}%</p>
                </div>
                <div className="bg-slate-800/50 rounded-lg p-3">
                  <p className="text-xs text-slate-400">Immediate Support</p>
                  <p className={`text-lg font-bold ${rep.needs_immediate_support ? "text-rose-400" : "text-emerald-400"}`}>
                    {rep.needs_immediate_support ? "Required" : "Not Needed"}
                  </p>
                </div>
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div className="bg-slate-800/50 rounded-lg p-3">
                  <p className="text-xs text-slate-400">At Burnout Risk</p>
                  <p className={`text-sm font-medium ${rep.is_at_burnout_risk ? "text-orange-400" : "text-emerald-400"}`}>
                    {rep.is_at_burnout_risk ? "Yes" : "No"}
                  </p>
                </div>
                <div className="bg-slate-800/50 rounded-lg p-3">
                  <p className="text-xs text-slate-400">Region</p>
                  <p className="text-sm font-medium text-slate-200">{rep.region}</p>
                </div>
              </div>
            </>
          )}

          {tab === "scores" && (
            <div className="space-y-3">
              <HealthBar score={rep.activity_health_score} label="Activity Health" />
              <HealthBar score={rep.wellbeing_score} label="Wellbeing" />
              <HealthBar score={rep.performance_sustainability_score} label="Performance Sustainability" />
              <HealthBar score={rep.social_engagement_score} label="Social Engagement" />
              <div className="pt-2 border-t border-slate-800">
                <div className="flex justify-between items-center">
                  <span className="text-sm text-slate-400">Burnout Composite (risk)</span>
                  <span className="text-lg font-bold" style={{ color: riskColor }}>{rep.burnout_composite}</span>
                </div>
                <p className="text-xs text-slate-500 mt-1">Higher composite = greater burnout risk</p>
              </div>
            </div>
          )}

          {tab === "action" && (
            <div className="space-y-4">
              <div className="bg-slate-800/50 rounded-lg p-4">
                <p className="text-xs text-slate-400 mb-2">Recommended Action</p>
                <span className={`text-sm px-3 py-1.5 rounded-lg font-medium ${ACTION_BG[rep.burnout_action] ?? ""}`}>
                  {ACTION_LABEL[rep.burnout_action] ?? rep.burnout_action}
                </span>
              </div>
              <div className="space-y-2">
                <div className="flex justify-between p-2 rounded bg-slate-800/40">
                  <span className="text-xs text-slate-400">Primary Signal</span>
                  <span className="text-xs text-slate-200 capitalize">{rep.primary_burnout_signal.replace(/_/g, " ")}</span>
                </div>
                <div className="flex justify-between p-2 rounded bg-slate-800/40">
                  <span className="text-xs text-slate-400">Burnout Stage</span>
                  <span className="text-xs text-slate-200">{STAGE_LABEL[rep.burnout_stage] ?? rep.burnout_stage}</span>
                </div>
                <div className="flex justify-between p-2 rounded bg-slate-800/40">
                  <span className="text-xs text-slate-400">Productivity Impact</span>
                  <span className="text-xs text-rose-400 font-medium">-{rep.estimated_productivity_impact_pct.toFixed(1)}%</span>
                </div>
                <div className="flex justify-between p-2 rounded bg-slate-800/40">
                  <span className="text-xs text-slate-400">Immediate Support</span>
                  <span className={`text-xs font-medium ${rep.needs_immediate_support ? "text-rose-400" : "text-emerald-400"}`}>
                    {rep.needs_immediate_support ? "Required" : "Not Needed"}
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

function DistBar({ counts, colors }: { counts: Record<string, number>; colors: Record<string, string> }) {
  const total = Object.values(counts).reduce((a, b) => a + b, 0);
  if (!total) return null;
  return (
    <div className="flex h-2 rounded-full overflow-hidden gap-px">
      {Object.entries(counts).map(([k, v]) =>
        v > 0 ? (
          <div key={k} style={{ width: `${(v / total) * 100}%`, backgroundColor: colors[k] ?? "#94a3b8" }} title={`${k}: ${v}`} />
        ) : null
      )}
    </div>
  );
}

const RISK_FILTERS = ["all", "none", "early_warning", "moderate", "high", "critical"] as const;
type RiskFilter = typeof RISK_FILTERS[number];

export default function SalesBurnoutRiskEnginePage() {
  const [data, setData] = useState<{ reps: RepData[]; summary: Summary } | null>(null);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState<RiskFilter>("all");
  const [selected, setSelected] = useState<RepData | null>(null);

  const fetchData = useCallback(async (risk: RiskFilter) => {
    setLoading(true);
    const params = new URLSearchParams();
    if (risk !== "all") params.set("risk", risk);
    const res = await fetch(`/api/sales-burnout-risk-engine?${params}`);
    const json = await res.json();
    setData(json);
    setLoading(false);
  }, []);

  useEffect(() => { fetchData(filter); }, [filter, fetchData]);

  const s = data?.summary;
  const reps = data?.reps ?? [];

  const riskDist = s?.risk_counts ?? {};
  const riskColors: Record<string, string> = {
    none: "#34d399", early_warning: "#38bdf8", moderate: "#fbbf24", high: "#f97316", critical: "#f87171",
  };
  const stageDist = s?.stage_counts ?? {};
  const stageColors: Record<string, string> = {
    engaged: "#34d399", coasting: "#38bdf8", disengaging: "#fbbf24", burned_out: "#f97316", depleted: "#f87171",
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
      {selected && <DetailModal rep={selected} onClose={() => setSelected(null)} />}

      {/* Header */}
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-white">Sales Burnout Risk Engine</h1>
        <p className="text-slate-400 text-sm mt-1">
          Rep wellbeing intelligence — detect overwork, disengagement, and performance decay before they become attrition
        </p>
      </div>

      {/* KPI Strip */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
          <p className="text-xs text-slate-400 mb-1">Total Reps</p>
          <p className="text-2xl font-bold text-white">{s?.total ?? "—"}</p>
        </div>
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
          <p className="text-xs text-slate-400 mb-1">At Burnout Risk</p>
          <p className="text-2xl font-bold text-orange-400">{s?.at_burnout_risk_count ?? "—"}</p>
        </div>
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
          <p className="text-xs text-slate-400 mb-1">Need Immediate Support</p>
          <p className="text-2xl font-bold text-rose-400">{s?.immediate_support_count ?? "—"}</p>
        </div>
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
          <p className="text-xs text-slate-400 mb-1">Avg Burnout Composite</p>
          <p className="text-2xl font-bold text-amber-400">{s?.avg_burnout_composite ?? "—"}</p>
        </div>
      </div>

      {/* Health Scores + Distribution row */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
          <h3 className="text-sm font-semibold text-slate-300 mb-3">Avg Health Scores</h3>
          <div className="space-y-3">
            <HealthBar score={s?.avg_activity_health_score ?? 0} label="Activity Health" />
            <HealthBar score={s?.avg_wellbeing_score ?? 0} label="Wellbeing" />
            <HealthBar score={s?.avg_performance_sustainability_score ?? 0} label="Performance Sustainability" />
            <HealthBar score={s?.avg_social_engagement_score ?? 0} label="Social Engagement" />
          </div>
        </div>
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 space-y-4">
          <div>
            <div className="flex justify-between items-center mb-2">
              <h3 className="text-sm font-semibold text-slate-300">Risk Distribution</h3>
              <span className="text-xs text-slate-500">{s?.total ?? 0} reps</span>
            </div>
            <DistBar counts={riskDist} colors={riskColors} />
            <div className="flex flex-wrap gap-2 mt-2">
              {Object.entries(riskDist).map(([k, v]) => (
                <span key={k} className="text-xs text-slate-400" style={{ color: riskColors[k] }}>
                  {RISK_LABEL[k] ?? k}: {v}
                </span>
              ))}
            </div>
          </div>
          <div>
            <div className="flex justify-between items-center mb-2">
              <h3 className="text-sm font-semibold text-slate-300">Stage Distribution</h3>
            </div>
            <DistBar counts={stageDist} colors={stageColors} />
            <div className="flex flex-wrap gap-2 mt-2">
              {Object.entries(stageDist).map(([k, v]) => (
                <span key={k} className="text-xs" style={{ color: stageColors[k] }}>
                  {STAGE_LABEL[k] ?? k}: {v}
                </span>
              ))}
            </div>
          </div>
          <div className="border-t border-slate-800 pt-3">
            <div className="flex justify-between">
              <span className="text-xs text-slate-400">Total Productivity Impact</span>
              <span className="text-sm font-bold text-rose-400">-{s?.total_productivity_impact_pct?.toFixed(1) ?? "0"}%</span>
            </div>
          </div>
        </div>
      </div>

      {/* Filter tabs */}
      <div className="flex flex-wrap gap-2 mb-4">
        {RISK_FILTERS.map((f) => (
          <button
            key={f}
            onClick={() => setFilter(f)}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors border ${
              filter === f
                ? "bg-indigo-600 border-indigo-500 text-white"
                : "bg-slate-800 border-slate-700 text-slate-400 hover:text-white hover:border-slate-600"
            }`}
          >
            {f === "all" ? "All Reps" : RISK_LABEL[f] ?? f}
            {f !== "all" && s?.risk_counts?.[f] !== undefined && (
              <span className="ml-1 opacity-70">({s.risk_counts[f]})</span>
            )}
          </button>
        ))}
      </div>

      {/* Rep cards grid */}
      {loading ? (
        <div className="flex items-center justify-center h-48">
          <div className="w-8 h-8 border-2 border-indigo-500 border-t-transparent rounded-full animate-spin" />
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
          {reps.map((rep) => {
            const color = RISK_COLOR[rep.burnout_risk] ?? "#94a3b8";
            return (
              <div
                key={rep.rep_id}
                onClick={() => setSelected(rep)}
                className="bg-slate-900 border border-slate-800 rounded-xl p-4 cursor-pointer hover:border-slate-600 transition-all hover:bg-slate-800/60"
              >
                {/* Top row */}
                <div className="flex items-start justify-between mb-3">
                  <div>
                    <div className="flex items-center gap-2 mb-1">
                      <span className={`text-xs px-2 py-0.5 rounded-full border font-medium ${RISK_BG[rep.burnout_risk] ?? ""}`}>
                        {RISK_LABEL[rep.burnout_risk] ?? rep.burnout_risk}
                      </span>
                      {rep.needs_immediate_support && (
                        <span className="text-xs px-2 py-0.5 rounded-full bg-rose-500/20 border border-rose-500/30 text-rose-300 font-medium">
                          Urgent
                        </span>
                      )}
                    </div>
                    <h3 className="text-white font-semibold text-sm">{rep.rep_name}</h3>
                    <p className="text-slate-400 text-xs">{rep.region} Region</p>
                  </div>
                  <RiskGauge pct={rep.burnout_composite} color={color} size={72} />
                </div>

                {/* Score bars */}
                <div className="space-y-1.5 mb-3">
                  <HealthBar score={rep.activity_health_score} label="Activity" />
                  <HealthBar score={rep.wellbeing_score} label="Wellbeing" />
                  <HealthBar score={rep.performance_sustainability_score} label="Performance" />
                  <HealthBar score={rep.social_engagement_score} label="Social" />
                </div>

                {/* Footer */}
                <div className="border-t border-slate-800 pt-2 flex items-center justify-between">
                  <span className={`text-xs px-2 py-0.5 rounded font-medium ${ACTION_BG[rep.burnout_action] ?? ""}`}>
                    {ACTION_LABEL[rep.burnout_action] ?? rep.burnout_action}
                  </span>
                  {rep.estimated_productivity_impact_pct > 0 && (
                    <span className="text-xs text-rose-400 font-medium">-{rep.estimated_productivity_impact_pct.toFixed(1)}% prod.</span>
                  )}
                </div>

                {/* Signal text */}
                <p className="text-xs text-slate-500 mt-2 truncate">{rep.burnout_signal}</p>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
