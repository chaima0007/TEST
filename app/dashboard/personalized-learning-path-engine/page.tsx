"use client";

import { useState, useEffect, useRef, useCallback } from "react";

interface LearnerData {
  learner_id: string;
  region: string;
  learning_risk: string;
  learning_pattern: string;
  learning_severity: string;
  recommended_action: string;
  engagement_score_calc: number;
  retention_score: number;
  application_score: number;
  alignment_score: number;
  learning_composite: number;
  has_learning_gap: boolean;
  requires_path_adjustment: boolean;
  estimated_learning_velocity_index: number;
  learning_signal: string;
}

interface Summary {
  total: number;
  risk_counts: Record<string, number>;
  pattern_counts: Record<string, number>;
  severity_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_learning_composite: number;
  learning_gap_count: number;
  path_adjustment_count: number;
  avg_engagement_score_calc: number;
  avg_retention_score: number;
  avg_application_score: number;
  avg_alignment_score: number;
  avg_estimated_learning_velocity_index: number;
}

const RISK_BG: Record<string, string> = {
  low:      "bg-emerald-500/20 border-emerald-500/30 text-emerald-300",
  moderate: "bg-teal-500/20 border-teal-500/30 text-teal-300",
  high:     "bg-green-600/20 border-green-600/30 text-green-300",
  critical: "bg-rose-500/20 border-rose-500/30 text-rose-300",
};
const RISK_COLOR: Record<string, string> = {
  low:      "#34d399",
  moderate: "#2dd4bf",
  high:     "#4ade80",
  critical: "#f87171",
};
const RISK_LABEL: Record<string, string> = {
  low:      "Low Risk",
  moderate: "Moderate",
  high:     "High Risk",
  critical: "Critical",
};
const SEVERITY_BG: Record<string, string> = {
  thriving:   "bg-emerald-500/15 text-emerald-300",
  progressing: "bg-teal-500/15 text-teal-300",
  stalling:   "bg-yellow-500/15 text-yellow-300",
  regressing: "bg-rose-500/15 text-rose-300",
};
const SEVERITY_LABEL: Record<string, string> = {
  thriving:   "Thriving",
  progressing: "Progressing",
  stalling:   "Stalling",
  regressing: "Regressing",
};
const ACTION_BG: Record<string, string> = {
  no_action:           "bg-emerald-500/15 text-emerald-300",
  path_monitoring:     "bg-teal-500/15 text-teal-300",
  content_refresh:     "bg-cyan-500/15 text-cyan-300",
  coaching_session:    "bg-sky-500/15 text-sky-300",
  challenge_assignment: "bg-blue-500/15 text-blue-300",
  peer_learning_group: "bg-green-500/15 text-green-300",
  mentorship_match:    "bg-lime-500/15 text-lime-300",
  intensive_bootcamp:  "bg-amber-500/15 text-amber-300",
  career_path_redesign: "bg-rose-500/15 text-rose-300",
};
const ACTION_LABEL: Record<string, string> = {
  no_action:           "No Action",
  path_monitoring:     "Path Monitoring",
  content_refresh:     "Content Refresh",
  coaching_session:    "Coaching Session",
  challenge_assignment: "Challenge Assignment",
  peer_learning_group: "Peer Learning Group",
  mentorship_match:    "Mentorship Match",
  intensive_bootcamp:  "Intensive Bootcamp",
  career_path_redesign: "Career Path Redesign",
};
const PATTERN_LABEL: Record<string, string> = {
  none:                   "None",
  plateau_risk:           "Plateau Risk",
  disengaged_learner:     "Disengaged Learner",
  high_potential_redirect: "High Potential Redirect",
  knowledge_hoarding:     "Knowledge Hoarding",
  learning_style_conflict: "Learning Style Conflict",
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

function ScoreBar({ score, label }: { score: number; label: string }) {
  const color = score <= 20 ? "#34d399" : score <= 40 ? "#2dd4bf" : score <= 60 ? "#4ade80" : "#f87171";
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

interface ModalProps { learner: LearnerData; onClose: () => void }

function DetailModal({ learner, onClose }: ModalProps) {
  const [tab, setTab] = useState<"overview" | "scores" | "action">("overview");
  const backdropRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handler = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [onClose]);

  const riskColor = RISK_COLOR[learner.learning_risk] ?? "#94a3b8";

  return (
    <div
      ref={backdropRef}
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4"
      onClick={(e) => { if (e.target === backdropRef.current) onClose(); }}
    >
      <div className="bg-slate-900 border border-slate-700 rounded-xl shadow-2xl w-full max-w-lg">
        <div className="flex items-start justify-between p-5 border-b border-slate-800">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <span className={`text-xs px-2 py-0.5 rounded-full border font-medium ${RISK_BG[learner.learning_risk] ?? ""}`}>
                {RISK_LABEL[learner.learning_risk] ?? learner.learning_risk}
              </span>
              <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${SEVERITY_BG[learner.learning_severity] ?? ""}`}>
                {SEVERITY_LABEL[learner.learning_severity] ?? learner.learning_severity}
              </span>
            </div>
            <h2 className="text-white font-bold text-lg">{learner.learner_id}</h2>
            <p className="text-slate-400 text-sm">{learner.region} · Composite: <span style={{ color: riskColor }}>{learner.learning_composite}</span></p>
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-white p-1 transition-colors" aria-label="Close">
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <div className="flex border-b border-slate-800">
          {(["overview", "scores", "action"] as const).map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`flex-1 py-2.5 text-sm font-medium capitalize transition-colors ${
                tab === t ? "text-teal-400 border-b-2 border-teal-500 bg-slate-800/40" : "text-slate-400 hover:text-slate-200"
              }`}
            >
              {t === "overview" ? "Overview" : t === "scores" ? "Sub-Scores" : "Action Plan"}
            </button>
          ))}
        </div>

        <div className="p-5 space-y-4">
          {tab === "overview" && (
            <>
              <div className="flex items-center justify-center py-3">
                <RiskGauge pct={learner.learning_composite} color={riskColor} size={110} />
              </div>
              <div className="bg-slate-800/50 rounded-lg p-3">
                <p className="text-xs text-slate-400 mb-1">Learning Signal</p>
                <p className="text-sm text-white">{learner.learning_signal}</p>
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div className="bg-slate-800/50 rounded-lg p-3">
                  <p className="text-xs text-slate-400">Velocity Index</p>
                  <p className="text-lg font-bold text-teal-400">{learner.estimated_learning_velocity_index.toFixed(2)}</p>
                </div>
                <div className="bg-slate-800/50 rounded-lg p-3">
                  <p className="text-xs text-slate-400">Path Adjustment</p>
                  <p className={`text-lg font-bold ${learner.requires_path_adjustment ? "text-rose-400" : "text-emerald-400"}`}>
                    {learner.requires_path_adjustment ? "Needed" : "On Track"}
                  </p>
                </div>
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div className="bg-slate-800/50 rounded-lg p-3">
                  <p className="text-xs text-slate-400">Learning Gap</p>
                  <p className={`text-sm font-medium ${learner.has_learning_gap ? "text-orange-400" : "text-emerald-400"}`}>
                    {learner.has_learning_gap ? "Identified" : "None"}
                  </p>
                </div>
                <div className="bg-slate-800/50 rounded-lg p-3">
                  <p className="text-xs text-slate-400">Pattern</p>
                  <p className="text-sm font-medium text-slate-200">{PATTERN_LABEL[learner.learning_pattern] ?? learner.learning_pattern}</p>
                </div>
              </div>
            </>
          )}

          {tab === "scores" && (
            <div className="space-y-3">
              <ScoreBar score={learner.engagement_score_calc} label="Engagement (30%)" />
              <ScoreBar score={learner.retention_score} label="Retention (25%)" />
              <ScoreBar score={learner.application_score} label="Application (25%)" />
              <ScoreBar score={learner.alignment_score} label="Alignment (20%)" />
              <div className="pt-2 border-t border-slate-800">
                <div className="flex justify-between items-center">
                  <span className="text-sm text-slate-400">Learning Composite (risk)</span>
                  <span className="text-lg font-bold" style={{ color: riskColor }}>{learner.learning_composite}</span>
                </div>
                <p className="text-xs text-slate-500 mt-1">Higher composite = greater missed-learning risk</p>
              </div>
            </div>
          )}

          {tab === "action" && (
            <div className="space-y-4">
              <div className="bg-slate-800/50 rounded-lg p-4">
                <p className="text-xs text-slate-400 mb-2">Recommended Action</p>
                <span className={`text-sm px-3 py-1.5 rounded-lg font-medium ${ACTION_BG[learner.recommended_action] ?? ""}`}>
                  {ACTION_LABEL[learner.recommended_action] ?? learner.recommended_action}
                </span>
              </div>
              <div className="space-y-2">
                <div className="flex justify-between p-2 rounded bg-slate-800/40">
                  <span className="text-xs text-slate-400">Pattern</span>
                  <span className="text-xs text-slate-200">{PATTERN_LABEL[learner.learning_pattern] ?? learner.learning_pattern}</span>
                </div>
                <div className="flex justify-between p-2 rounded bg-slate-800/40">
                  <span className="text-xs text-slate-400">Severity</span>
                  <span className="text-xs text-slate-200">{SEVERITY_LABEL[learner.learning_severity] ?? learner.learning_severity}</span>
                </div>
                <div className="flex justify-between p-2 rounded bg-slate-800/40">
                  <span className="text-xs text-slate-400">Velocity Index</span>
                  <span className="text-xs text-teal-400 font-medium">{learner.estimated_learning_velocity_index.toFixed(2)}</span>
                </div>
                <div className="flex justify-between p-2 rounded bg-slate-800/40">
                  <span className="text-xs text-slate-400">Path Adjustment</span>
                  <span className={`text-xs font-medium ${learner.requires_path_adjustment ? "text-rose-400" : "text-emerald-400"}`}>
                    {learner.requires_path_adjustment ? "Needed" : "On Track"}
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

const RISK_FILTERS = ["all", "low", "moderate", "high", "critical"] as const;
type RiskFilter = typeof RISK_FILTERS[number];

export default function PersonalizedLearningPathEnginePage() {
  const [data, setData] = useState<{ learners: LearnerData[]; summary: Summary } | null>(null);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState<RiskFilter>("all");
  const [selected, setSelected] = useState<LearnerData | null>(null);

  const fetchData = useCallback(async (risk: RiskFilter) => {
    setLoading(true);
    const params = new URLSearchParams();
    if (risk !== "all") params.set("risk", risk);
    const res = await fetch(`/api/personalized-learning-path-engine?${params}`);
    const json = await res.json();
    setData(json);
    setLoading(false);
  }, []);

  useEffect(() => { fetchData(filter); }, [filter, fetchData]);

  const s = data?.summary;
  const learners = data?.learners ?? [];

  const riskColors: Record<string, string> = {
    low: "#34d399", moderate: "#2dd4bf", high: "#4ade80", critical: "#f87171",
  };
  const severityColors: Record<string, string> = {
    thriving: "#34d399", progressing: "#2dd4bf", stalling: "#fbbf24", regressing: "#f87171",
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
      {selected && <DetailModal learner={selected} onClose={() => setSelected(null)} />}

      <div className="mb-6">
        <h1 className="text-2xl font-bold text-white">Personalized Learning Path Engine</h1>
        <p className="text-slate-400 text-sm mt-1">
          Detect missed-learning risk and tailor development paths — surface disengagement, plateaus, and misaligned ambitions early
        </p>
      </div>

      {/* KPI Strip */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
          <p className="text-xs text-slate-400 mb-1">Total Learners</p>
          <p className="text-2xl font-bold text-white">{s?.total ?? "—"}</p>
        </div>
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
          <p className="text-xs text-slate-400 mb-1">Learning Gap</p>
          <p className="text-2xl font-bold text-teal-400">{s?.learning_gap_count ?? "—"}</p>
        </div>
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
          <p className="text-xs text-slate-400 mb-1">Path Adjustments</p>
          <p className="text-2xl font-bold text-rose-400">{s?.path_adjustment_count ?? "—"}</p>
        </div>
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
          <p className="text-xs text-slate-400 mb-1">Avg Learning Composite</p>
          <p className="text-2xl font-bold text-emerald-400">{s?.avg_learning_composite ?? "—"}</p>
        </div>
      </div>

      {/* Score panel + Distribution */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
          <h3 className="text-sm font-semibold text-slate-300 mb-3">Avg Sub-Scores (missed-learning risk)</h3>
          <div className="space-y-3">
            <ScoreBar score={s?.avg_engagement_score_calc ?? 0} label="Engagement (30%)" />
            <ScoreBar score={s?.avg_retention_score ?? 0} label="Retention (25%)" />
            <ScoreBar score={s?.avg_application_score ?? 0} label="Application (25%)" />
            <ScoreBar score={s?.avg_alignment_score ?? 0} label="Alignment (20%)" />
          </div>
        </div>
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 space-y-4">
          <div>
            <div className="flex justify-between items-center mb-2">
              <h3 className="text-sm font-semibold text-slate-300">Risk Distribution</h3>
              <span className="text-xs text-slate-500">{s?.total ?? 0} learners</span>
            </div>
            <DistBar counts={s?.risk_counts ?? {}} colors={riskColors} />
            <div className="flex flex-wrap gap-2 mt-2">
              {Object.entries(s?.risk_counts ?? {}).map(([k, v]) => (
                <span key={k} className="text-xs" style={{ color: riskColors[k] ?? "#94a3b8" }}>
                  {RISK_LABEL[k] ?? k}: {v}
                </span>
              ))}
            </div>
          </div>
          <div>
            <div className="flex justify-between items-center mb-2">
              <h3 className="text-sm font-semibold text-slate-300">Severity Distribution</h3>
            </div>
            <DistBar counts={s?.severity_counts ?? {}} colors={severityColors} />
            <div className="flex flex-wrap gap-2 mt-2">
              {Object.entries(s?.severity_counts ?? {}).map(([k, v]) => (
                <span key={k} className="text-xs" style={{ color: severityColors[k] ?? "#94a3b8" }}>
                  {SEVERITY_LABEL[k] ?? k}: {v}
                </span>
              ))}
            </div>
          </div>
          <div className="border-t border-slate-800 pt-3">
            <div className="flex justify-between">
              <span className="text-xs text-slate-400">Avg Velocity Index</span>
              <span className="text-sm font-bold text-teal-400">{s?.avg_estimated_learning_velocity_index?.toFixed(2) ?? "—"}</span>
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
                ? "bg-teal-600 border-teal-500 text-white"
                : "bg-slate-800 border-slate-700 text-slate-400 hover:text-white hover:border-slate-600"
            }`}
          >
            {f === "all" ? "All Learners" : RISK_LABEL[f] ?? f}
            {f !== "all" && s?.risk_counts?.[f] !== undefined && (
              <span className="ml-1 opacity-70">({s.risk_counts[f]})</span>
            )}
          </button>
        ))}
      </div>

      {/* Learner cards */}
      {loading ? (
        <div className="flex items-center justify-center h-48">
          <div className="w-8 h-8 border-2 border-teal-500 border-t-transparent rounded-full animate-spin" />
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
          {learners.map((learner) => {
            const color = RISK_COLOR[learner.learning_risk] ?? "#94a3b8";
            return (
              <div
                key={learner.learner_id}
                onClick={() => setSelected(learner)}
                className="bg-slate-900 border border-slate-800 rounded-xl p-4 cursor-pointer hover:border-slate-600 transition-all hover:bg-slate-800/60"
              >
                <div className="flex items-start justify-between mb-3">
                  <div>
                    <div className="flex items-center gap-2 mb-1">
                      <span className={`text-xs px-2 py-0.5 rounded-full border font-medium ${RISK_BG[learner.learning_risk] ?? ""}`}>
                        {RISK_LABEL[learner.learning_risk] ?? learner.learning_risk}
                      </span>
                      {learner.requires_path_adjustment && (
                        <span className="text-xs px-2 py-0.5 rounded-full bg-amber-500/20 border border-amber-500/30 text-amber-300 font-medium">
                          Adjust Path
                        </span>
                      )}
                    </div>
                    <h3 className="text-white font-semibold text-sm">{learner.learner_id}</h3>
                    <p className="text-slate-400 text-xs">{learner.region}</p>
                  </div>
                  <RiskGauge pct={learner.learning_composite} color={color} size={72} />
                </div>

                <div className="space-y-1.5 mb-3">
                  <ScoreBar score={learner.engagement_score_calc} label="Engagement" />
                  <ScoreBar score={learner.retention_score} label="Retention" />
                  <ScoreBar score={learner.application_score} label="Application" />
                  <ScoreBar score={learner.alignment_score} label="Alignment" />
                </div>

                <div className="border-t border-slate-800 pt-2 flex items-center justify-between">
                  <span className={`text-xs px-2 py-0.5 rounded font-medium ${ACTION_BG[learner.recommended_action] ?? ""}`}>
                    {ACTION_LABEL[learner.recommended_action] ?? learner.recommended_action}
                  </span>
                  {learner.estimated_learning_velocity_index > 0 && (
                    <span className="text-xs text-teal-400 font-medium">
                      vel. {learner.estimated_learning_velocity_index.toFixed(2)}
                    </span>
                  )}
                </div>
                <p className="text-xs text-slate-500 mt-2 truncate">{learner.learning_signal}</p>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
