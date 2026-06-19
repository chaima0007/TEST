"use client";

import { useState, useEffect, useRef, useCallback } from "react";

interface EmployeeData {
  employee_id: string;
  region: string;
  skill_risk: string;
  skill_pattern: string;
  skill_severity: string;
  recommended_action: string;
  competency_score: number;
  market_alignment_score: number;
  leadership_score: number;
  digital_score: number;
  skill_composite: number;
  has_skill_gap: boolean;
  requires_intervention: boolean;
  estimated_performance_impact: number;
  skill_signal: string;
}

interface Summary {
  total: number;
  risk_counts: Record<string, number>;
  pattern_counts: Record<string, number>;
  severity_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_skill_composite: number;
  skill_gap_count: number;
  intervention_count: number;
  avg_competency_score: number;
  avg_market_alignment_score: number;
  avg_leadership_score: number;
  avg_digital_score: number;
  avg_estimated_performance_impact: number;
}

const RISK_BG: Record<string, string> = {
  low:      "bg-emerald-500/20 border-emerald-500/30 text-emerald-300",
  moderate: "bg-blue-500/20 border-blue-500/30 text-blue-300",
  high:     "bg-indigo-500/20 border-indigo-500/30 text-indigo-300",
  critical: "bg-rose-500/20 border-rose-500/30 text-rose-300",
};
const RISK_COLOR: Record<string, string> = {
  low:      "#34d399",
  moderate: "#60a5fa",
  high:     "#818cf8",
  critical: "#f87171",
};
const RISK_LABEL: Record<string, string> = {
  low:      "Low Risk",
  moderate: "Moderate",
  high:     "High Risk",
  critical: "Critical",
};
const SEVERITY_BG: Record<string, string> = {
  proficient: "bg-emerald-500/15 text-emerald-300",
  developing: "bg-blue-500/15 text-blue-300",
  gap:        "bg-indigo-500/15 text-indigo-300",
  critical:   "bg-rose-500/15 text-rose-300",
};
const SEVERITY_LABEL: Record<string, string> = {
  proficient: "Proficient",
  developing: "Developing",
  gap:        "Gap",
  critical:   "Critical",
};
const ACTION_BG: Record<string, string> = {
  no_action:                  "bg-emerald-500/15 text-emerald-300",
  skill_monitoring:           "bg-sky-500/15 text-sky-300",
  targeted_training:          "bg-blue-500/15 text-blue-300",
  mentoring_program:          "bg-indigo-500/15 text-indigo-300",
  external_hiring:            "bg-violet-500/15 text-violet-300",
  reskilling_initiative:      "bg-amber-500/15 text-amber-300",
  leadership_development:     "bg-purple-500/15 text-purple-300",
  digital_upskilling:         "bg-cyan-500/15 text-cyan-300",
  emergency_capability_build: "bg-rose-500/15 text-rose-300",
};
const ACTION_LABEL: Record<string, string> = {
  no_action:                  "No Action",
  skill_monitoring:           "Skill Monitoring",
  targeted_training:          "Targeted Training",
  mentoring_program:          "Mentoring Program",
  external_hiring:            "External Hiring",
  reskilling_initiative:      "Reskilling Initiative",
  leadership_development:     "Leadership Development",
  digital_upskilling:         "Digital Upskilling",
  emergency_capability_build: "Emergency Capability Build",
};
const PATTERN_LABEL: Record<string, string> = {
  none:                "None",
  critical_skill_gap:  "Critical Skill Gap",
  market_mismatch:     "Market Mismatch",
  obsolescence_risk:   "Obsolescence Risk",
  leadership_void:     "Leadership Void",
  digital_literacy_gap: "Digital Literacy Gap",
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
  const color = score <= 20 ? "#34d399" : score <= 40 ? "#60a5fa" : score <= 60 ? "#818cf8" : "#f87171";
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

interface ModalProps { emp: EmployeeData; onClose: () => void }

function DetailModal({ emp, onClose }: ModalProps) {
  const [tab, setTab] = useState<"overview" | "scores" | "action">("overview");
  const backdropRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handler = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [onClose]);

  const riskColor = RISK_COLOR[emp.skill_risk] ?? "#94a3b8";

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
              <span className={`text-xs px-2 py-0.5 rounded-full border font-medium ${RISK_BG[emp.skill_risk] ?? ""}`}>
                {RISK_LABEL[emp.skill_risk] ?? emp.skill_risk}
              </span>
              <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${SEVERITY_BG[emp.skill_severity] ?? ""}`}>
                {SEVERITY_LABEL[emp.skill_severity] ?? emp.skill_severity}
              </span>
            </div>
            <h2 className="text-white font-bold text-lg">{emp.employee_id}</h2>
            <p className="text-slate-400 text-sm">{emp.region} · Composite: <span style={{ color: riskColor }}>{emp.skill_composite}</span></p>
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
                tab === t ? "text-blue-400 border-b-2 border-blue-500 bg-slate-800/40" : "text-slate-400 hover:text-slate-200"
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
                <RiskGauge pct={emp.skill_composite} color={riskColor} size={110} />
              </div>
              <div className="bg-slate-800/50 rounded-lg p-3">
                <p className="text-xs text-slate-400 mb-1">Skill Signal</p>
                <p className="text-sm text-white">{emp.skill_signal}</p>
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div className="bg-slate-800/50 rounded-lg p-3">
                  <p className="text-xs text-slate-400">Perf. Impact</p>
                  <p className="text-lg font-bold text-indigo-400">{emp.estimated_performance_impact.toFixed(2)}</p>
                </div>
                <div className="bg-slate-800/50 rounded-lg p-3">
                  <p className="text-xs text-slate-400">Intervention</p>
                  <p className={`text-lg font-bold ${emp.requires_intervention ? "text-rose-400" : "text-emerald-400"}`}>
                    {emp.requires_intervention ? "Required" : "Not Needed"}
                  </p>
                </div>
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div className="bg-slate-800/50 rounded-lg p-3">
                  <p className="text-xs text-slate-400">Skill Gap</p>
                  <p className={`text-sm font-medium ${emp.has_skill_gap ? "text-orange-400" : "text-emerald-400"}`}>
                    {emp.has_skill_gap ? "Identified" : "None"}
                  </p>
                </div>
                <div className="bg-slate-800/50 rounded-lg p-3">
                  <p className="text-xs text-slate-400">Pattern</p>
                  <p className="text-sm font-medium text-slate-200">{PATTERN_LABEL[emp.skill_pattern] ?? emp.skill_pattern}</p>
                </div>
              </div>
            </>
          )}

          {tab === "scores" && (
            <div className="space-y-3">
              <ScoreBar score={emp.competency_score} label="Competency (30%)" />
              <ScoreBar score={emp.market_alignment_score} label="Market Alignment (25%)" />
              <ScoreBar score={emp.leadership_score} label="Leadership (25%)" />
              <ScoreBar score={emp.digital_score} label="Digital (20%)" />
              <div className="pt-2 border-t border-slate-800">
                <div className="flex justify-between items-center">
                  <span className="text-sm text-slate-400">Skill Composite (risk)</span>
                  <span className="text-lg font-bold" style={{ color: riskColor }}>{emp.skill_composite}</span>
                </div>
                <p className="text-xs text-slate-500 mt-1">Higher composite = greater skill gap risk</p>
              </div>
            </div>
          )}

          {tab === "action" && (
            <div className="space-y-4">
              <div className="bg-slate-800/50 rounded-lg p-4">
                <p className="text-xs text-slate-400 mb-2">Recommended Action</p>
                <span className={`text-sm px-3 py-1.5 rounded-lg font-medium ${ACTION_BG[emp.recommended_action] ?? ""}`}>
                  {ACTION_LABEL[emp.recommended_action] ?? emp.recommended_action}
                </span>
              </div>
              <div className="space-y-2">
                <div className="flex justify-between p-2 rounded bg-slate-800/40">
                  <span className="text-xs text-slate-400">Pattern</span>
                  <span className="text-xs text-slate-200">{PATTERN_LABEL[emp.skill_pattern] ?? emp.skill_pattern}</span>
                </div>
                <div className="flex justify-between p-2 rounded bg-slate-800/40">
                  <span className="text-xs text-slate-400">Severity</span>
                  <span className="text-xs text-slate-200">{SEVERITY_LABEL[emp.skill_severity] ?? emp.skill_severity}</span>
                </div>
                <div className="flex justify-between p-2 rounded bg-slate-800/40">
                  <span className="text-xs text-slate-400">Perf. Impact</span>
                  <span className="text-xs text-indigo-400 font-medium">{emp.estimated_performance_impact.toFixed(2)}</span>
                </div>
                <div className="flex justify-between p-2 rounded bg-slate-800/40">
                  <span className="text-xs text-slate-400">Requires Intervention</span>
                  <span className={`text-xs font-medium ${emp.requires_intervention ? "text-rose-400" : "text-emerald-400"}`}>
                    {emp.requires_intervention ? "Yes" : "No"}
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

export default function KnowledgeGapSkillsAnalysisEnginePage() {
  const [data, setData] = useState<{ employees: EmployeeData[]; summary: Summary } | null>(null);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState<RiskFilter>("all");
  const [selected, setSelected] = useState<EmployeeData | null>(null);

  const fetchData = useCallback(async (risk: RiskFilter) => {
    setLoading(true);
    const params = new URLSearchParams();
    if (risk !== "all") params.set("risk", risk);
    const res = await fetch(`/api/knowledge-gap-skills-analysis-engine?${params}`);
    const json = await res.json();
    setData(json);
    setLoading(false);
  }, []);

  useEffect(() => { fetchData(filter); }, [filter, fetchData]);

  const s = data?.summary;
  const employees = data?.employees ?? [];

  const riskColors: Record<string, string> = {
    low: "#34d399", moderate: "#60a5fa", high: "#818cf8", critical: "#f87171",
  };
  const severityColors: Record<string, string> = {
    proficient: "#34d399", developing: "#60a5fa", gap: "#818cf8", critical: "#f87171",
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
      {selected && <DetailModal emp={selected} onClose={() => setSelected(null)} />}

      <div className="mb-6">
        <h1 className="text-2xl font-bold text-white">Knowledge Gap & Skills Analysis Engine</h1>
        <p className="text-slate-400 text-sm mt-1">
          Identify skill gaps, market misalignments, and leadership voids — drive targeted development before performance decays
        </p>
      </div>

      {/* KPI Strip */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
          <p className="text-xs text-slate-400 mb-1">Total Employees</p>
          <p className="text-2xl font-bold text-white">{s?.total ?? "—"}</p>
        </div>
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
          <p className="text-xs text-slate-400 mb-1">Skill Gap Identified</p>
          <p className="text-2xl font-bold text-indigo-400">{s?.skill_gap_count ?? "—"}</p>
        </div>
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
          <p className="text-xs text-slate-400 mb-1">Need Intervention</p>
          <p className="text-2xl font-bold text-rose-400">{s?.intervention_count ?? "—"}</p>
        </div>
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
          <p className="text-xs text-slate-400 mb-1">Avg Skill Composite</p>
          <p className="text-2xl font-bold text-blue-400">{s?.avg_skill_composite ?? "—"}</p>
        </div>
      </div>

      {/* Score panel + Distribution */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
          <h3 className="text-sm font-semibold text-slate-300 mb-3">Avg Sub-Scores (gap risk)</h3>
          <div className="space-y-3">
            <ScoreBar score={s?.avg_competency_score ?? 0} label="Competency (30%)" />
            <ScoreBar score={s?.avg_market_alignment_score ?? 0} label="Market Alignment (25%)" />
            <ScoreBar score={s?.avg_leadership_score ?? 0} label="Leadership (25%)" />
            <ScoreBar score={s?.avg_digital_score ?? 0} label="Digital (20%)" />
          </div>
        </div>
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 space-y-4">
          <div>
            <div className="flex justify-between items-center mb-2">
              <h3 className="text-sm font-semibold text-slate-300">Risk Distribution</h3>
              <span className="text-xs text-slate-500">{s?.total ?? 0} employees</span>
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
              <span className="text-xs text-slate-400">Avg Performance Impact</span>
              <span className="text-sm font-bold text-indigo-400">{s?.avg_estimated_performance_impact?.toFixed(2) ?? "—"}</span>
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
                ? "bg-blue-600 border-blue-500 text-white"
                : "bg-slate-800 border-slate-700 text-slate-400 hover:text-white hover:border-slate-600"
            }`}
          >
            {f === "all" ? "All Employees" : RISK_LABEL[f] ?? f}
            {f !== "all" && s?.risk_counts?.[f] !== undefined && (
              <span className="ml-1 opacity-70">({s.risk_counts[f]})</span>
            )}
          </button>
        ))}
      </div>

      {/* Employee cards */}
      {loading ? (
        <div className="flex items-center justify-center h-48">
          <div className="w-8 h-8 border-2 border-blue-500 border-t-transparent rounded-full animate-spin" />
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
          {employees.map((emp) => {
            const color = RISK_COLOR[emp.skill_risk] ?? "#94a3b8";
            return (
              <div
                key={emp.employee_id}
                onClick={() => setSelected(emp)}
                className="bg-slate-900 border border-slate-800 rounded-xl p-4 cursor-pointer hover:border-slate-600 transition-all hover:bg-slate-800/60"
              >
                <div className="flex items-start justify-between mb-3">
                  <div>
                    <div className="flex items-center gap-2 mb-1">
                      <span className={`text-xs px-2 py-0.5 rounded-full border font-medium ${RISK_BG[emp.skill_risk] ?? ""}`}>
                        {RISK_LABEL[emp.skill_risk] ?? emp.skill_risk}
                      </span>
                      {emp.requires_intervention && (
                        <span className="text-xs px-2 py-0.5 rounded-full bg-rose-500/20 border border-rose-500/30 text-rose-300 font-medium">
                          Intervene
                        </span>
                      )}
                    </div>
                    <h3 className="text-white font-semibold text-sm">{emp.employee_id}</h3>
                    <p className="text-slate-400 text-xs">{emp.region}</p>
                  </div>
                  <RiskGauge pct={emp.skill_composite} color={color} size={72} />
                </div>

                <div className="space-y-1.5 mb-3">
                  <ScoreBar score={emp.competency_score} label="Competency" />
                  <ScoreBar score={emp.market_alignment_score} label="Market Alignment" />
                  <ScoreBar score={emp.leadership_score} label="Leadership" />
                  <ScoreBar score={emp.digital_score} label="Digital" />
                </div>

                <div className="border-t border-slate-800 pt-2 flex items-center justify-between">
                  <span className={`text-xs px-2 py-0.5 rounded font-medium ${ACTION_BG[emp.recommended_action] ?? ""}`}>
                    {ACTION_LABEL[emp.recommended_action] ?? emp.recommended_action}
                  </span>
                  {emp.estimated_performance_impact > 0 && (
                    <span className="text-xs text-indigo-400 font-medium">
                      impact {emp.estimated_performance_impact.toFixed(2)}
                    </span>
                  )}
                </div>
                <p className="text-xs text-slate-500 mt-2 truncate">{emp.skill_signal}</p>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
