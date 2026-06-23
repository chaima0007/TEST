"use client";

import { useEffect, useState } from "react";

// ── types ─────────────────────────────────────────────────────────────────────

interface Rep {
  rep_id: string;
  rep_name: string;
  region: string;
  manager_id: string;
  burnout_risk: string;
  burnout_category: string;
  burnout_pattern: string;
  burnout_action: string;
  overwork_score: number;
  disengagement_score: number;
  performance_decline_score: number;
  wellbeing_score: number;
  burnout_composite_score: number;
  predicted_turnover_probability: number;
  intervention_urgency_score: number;
  is_at_risk: boolean;
  needs_immediate_action: boolean;
  deals_closed_this_quarter: number;
  deals_closed_last_quarter: number;
  win_rate_current: number;
  win_rate_prev_quarter: number;
}

interface Summary {
  total: number;
  risk_counts: Record<string, number>;
  category_counts: Record<string, number>;
  pattern_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_burnout_composite_score: number;
  avg_predicted_turnover_probability: number;
  at_risk_count: number;
  immediate_action_count: number;
  avg_overwork_score: number;
  avg_disengagement_score: number;
  avg_performance_decline_score: number;
  avg_wellbeing_score: number;
}

// ── helpers ───────────────────────────────────────────────────────────────────

const RISK_COLOR: Record<string, string> = {
  minimal:  "text-green-400",
  building: "text-yellow-400",
  high:     "text-orange-400",
  critical: "text-red-400",
};

const CATEGORY_BG: Record<string, string> = {
  healthy:    "bg-green-500/20 border-green-500/40",
  stressed:   "bg-yellow-500/20 border-yellow-500/40",
  overloaded: "bg-orange-500/20 border-orange-500/40",
  burned_out: "bg-red-500/20 border-red-500/40",
};

const CATEGORY_BAR: Record<string, string> = {
  healthy:    "bg-green-500",
  stressed:   "bg-yellow-500",
  overloaded: "bg-orange-500",
  burned_out: "bg-red-500",
};

const ACTION_COLOR: Record<string, string> = {
  monitor:                "bg-slate-500/20 text-slate-300 border-slate-500/30",
  workload_review:        "bg-amber-500/20 text-amber-300 border-amber-500/30",
  coaching:               "bg-sky-500/20 text-sky-300 border-sky-500/30",
  immediate_intervention: "bg-red-500/20 text-red-300 border-red-500/30",
};

const PATTERN_COLOR: Record<string, string> = {
  stable:       "text-green-400",
  overworking:  "text-amber-400",
  disengaging:  "text-orange-400",
  declining:    "text-red-400",
};

function fmt(label: string) {
  return label.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
}

// ── BurnoutMeter SVG ──────────────────────────────────────────────────────────

function BurnoutMeter({ score, label }: { score: number; label: string }) {
  const r = 28;
  const cx = 35;
  const cy = 35;
  const circ = 2 * Math.PI * r;
  const filled = (score / 100) * circ;
  const color =
    score >= 70 ? "#ef4444" :
    score >= 50 ? "#f97316" :
    score >= 30 ? "#eab308" : "#22c55e";

  return (
    <div className="flex flex-col items-center gap-1">
      <svg width="70" height="70" viewBox="0 0 70 70">
        <circle cx={cx} cy={cy} r={r} fill="none" stroke="#1e293b" strokeWidth="5" />
        <circle
          cx={cx} cy={cy} r={r}
          fill="none"
          stroke={color}
          strokeWidth="5"
          strokeDasharray={`${filled} ${circ - filled}`}
          strokeDashoffset={circ / 4}
          strokeLinecap="round"
        />
        <text x={cx} y={cy + 5} textAnchor="middle" fill="white" fontSize="12" fontWeight="bold">
          {Math.round(score)}
        </text>
      </svg>
      <span className="text-xs text-slate-400 text-center">{label}</span>
    </div>
  );
}

// ── CategoryDistBar ───────────────────────────────────────────────────────────

function CategoryDistBar({ counts, total }: { counts: Record<string, number>; total: number }) {
  const order = ["healthy", "stressed", "overloaded", "burned_out"];
  return (
    <div className="flex rounded-full overflow-hidden h-3 w-full">
      {order.map((k) => {
        const pct = total > 0 ? ((counts[k] || 0) / total) * 100 : 0;
        if (pct === 0) return null;
        return (
          <div
            key={k}
            style={{ width: `${pct}%` }}
            className={`${CATEGORY_BAR[k]} transition-all`}
            title={`${k}: ${counts[k] || 0}`}
          />
        );
      })}
    </div>
  );
}

// ── BurnoutModal ──────────────────────────────────────────────────────────────

function BurnoutModal({ rep, onClose }: { rep: Rep; onClose: () => void }) {
  const [tab, setTab] = useState<"burnout" | "performance" | "actions">("burnout");

  useEffect(() => {
    const handler = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [onClose]);

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4"
      onClick={onClose}
    >
      <div
        className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-2xl max-h-[90vh] overflow-y-auto"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="p-6 border-b border-slate-800 flex items-start justify-between gap-4">
          <div>
            <div className="flex items-center gap-3 flex-wrap">
              <h2 className="text-xl font-bold text-slate-100">{rep.rep_name}</h2>
              <span className={`text-xs font-semibold px-2.5 py-0.5 rounded-full border ${ACTION_COLOR[rep.burnout_action]}`}>
                {fmt(rep.burnout_action)}
              </span>
              {rep.needs_immediate_action && (
                <span className="text-xs font-semibold px-2.5 py-0.5 rounded-full bg-red-500/20 text-red-300 border border-red-500/30">
                  Urgent
                </span>
              )}
            </div>
            <p className="text-sm text-slate-400 mt-1">
              <span className={`font-semibold ${RISK_COLOR[rep.burnout_risk]}`}>{fmt(rep.burnout_risk)} Risk</span>
              {" · "}{fmt(rep.burnout_category)}{" · "}{rep.region}
            </p>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-slate-300 text-xl leading-none">✕</button>
        </div>

        <div className="flex gap-0 border-b border-slate-800">
          {(["burnout", "performance", "actions"] as const).map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`px-5 py-3 text-sm font-medium border-b-2 transition-colors ${
                tab === t
                  ? "border-indigo-500 text-indigo-400"
                  : "border-transparent text-slate-400 hover:text-slate-300"
              }`}
            >
              {t.charAt(0).toUpperCase() + t.slice(1)}
            </button>
          ))}
        </div>

        <div className="p-6">
          {tab === "burnout" && (
            <div className="space-y-5">
              <div className="flex justify-around">
                <BurnoutMeter score={rep.overwork_score} label="Overwork" />
                <BurnoutMeter score={rep.disengagement_score} label="Disengage" />
                <BurnoutMeter score={rep.performance_decline_score} label="Decline" />
                <BurnoutMeter score={100 - rep.wellbeing_score} label="Stress" />
              </div>
              <div className="text-center">
                <div className="text-4xl font-bold text-white">{rep.burnout_composite_score}</div>
                <div className="text-sm text-slate-400">Burnout Composite Score</div>
              </div>
              <div>
                <div className="flex justify-between text-xs text-slate-400 mb-1">
                  <span>Predicted Turnover Risk</span>
                  <span className={rep.predicted_turnover_probability >= 60 ? "text-red-400" : "text-slate-300"}>
                    {rep.predicted_turnover_probability}%
                  </span>
                </div>
                <div className="w-full bg-slate-700/50 rounded-full h-2">
                  <div
                    className={`h-2 rounded-full transition-all ${rep.predicted_turnover_probability >= 60 ? "bg-red-500" : rep.predicted_turnover_probability >= 40 ? "bg-orange-500" : "bg-green-500"}`}
                    style={{ width: `${Math.min(rep.predicted_turnover_probability, 100)}%` }}
                  />
                </div>
              </div>
              <div>
                <div className="flex justify-between text-xs text-slate-400 mb-1">
                  <span>Wellbeing Score</span>
                  <span className="text-emerald-400">{rep.wellbeing_score}</span>
                </div>
                <div className="w-full bg-slate-700/50 rounded-full h-2">
                  <div
                    className="h-2 rounded-full bg-emerald-500 transition-all"
                    style={{ width: `${Math.min(rep.wellbeing_score, 100)}%` }}
                  />
                </div>
              </div>
            </div>
          )}

          {tab === "performance" && (
            <div className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                {[
                  { label: "Deals This Quarter", value: rep.deals_closed_this_quarter },
                  { label: "Deals Last Quarter", value: rep.deals_closed_last_quarter },
                  { label: "Win Rate (Current)", value: `${rep.win_rate_current}%` },
                  { label: "Win Rate (Prev Qtr)", value: `${rep.win_rate_prev_quarter}%` },
                  { label: "Pattern", value: fmt(rep.burnout_pattern) },
                  { label: "Region", value: rep.region },
                  { label: "Intervention Urgency", value: Math.round(rep.intervention_urgency_score) },
                  { label: "At Risk", value: rep.is_at_risk ? "Yes" : "No" },
                ].map(({ label, value }) => (
                  <div key={label} className="bg-slate-800/60 rounded-xl p-3">
                    <div className="text-xs text-slate-400 mb-1">{label}</div>
                    <div className="text-base font-semibold text-slate-100">{value}</div>
                  </div>
                ))}
              </div>
              <div>
                <div className="text-xs text-slate-400 mb-2">Win Rate Trend</div>
                <div className="flex items-end gap-3">
                  <div className="flex-1">
                    <div className="text-xs text-slate-500 mb-1 text-center">Prev Qtr</div>
                    <div className="bg-slate-700/50 rounded-full h-2">
                      <div className="h-2 rounded-full bg-indigo-500" style={{ width: `${rep.win_rate_prev_quarter}%` }} />
                    </div>
                    <div className="text-xs text-center text-slate-400 mt-1">{rep.win_rate_prev_quarter}%</div>
                  </div>
                  <div className="flex-1">
                    <div className="text-xs text-slate-500 mb-1 text-center">Current</div>
                    <div className="bg-slate-700/50 rounded-full h-2">
                      <div
                        className={`h-2 rounded-full ${rep.win_rate_current >= rep.win_rate_prev_quarter ? "bg-emerald-500" : "bg-red-500"}`}
                        style={{ width: `${rep.win_rate_current}%` }}
                      />
                    </div>
                    <div className="text-xs text-center text-slate-400 mt-1">{rep.win_rate_current}%</div>
                  </div>
                </div>
              </div>
            </div>
          )}

          {tab === "actions" && (
            <div className="space-y-4">
              <div className={`p-4 rounded-xl border ${CATEGORY_BG[rep.burnout_category]}`}>
                <div className={`text-sm font-semibold ${RISK_COLOR[rep.burnout_risk]} mb-1`}>
                  {fmt(rep.burnout_category)} — {fmt(rep.burnout_pattern)} Pattern
                </div>
                <div className="text-xs text-slate-400">
                  {rep.burnout_category === "burned_out" && "Rep is showing severe burnout signals. Immediate intervention required to prevent departure."}
                  {rep.burnout_category === "overloaded" && "Rep is carrying excessive workload. Redistribute deals and enforce recovery time."}
                  {rep.burnout_category === "stressed" && "Rep is under building stress. Address root cause before it escalates to burnout."}
                  {rep.burnout_category === "healthy" && "Rep is performing well with healthy work patterns. Continue monitoring."}
                </div>
              </div>
              <div className="space-y-3">
                {[
                  rep.burnout_action === "immediate_intervention" && { label: "Crisis 1:1 with Manager", desc: "Schedule confidential 1:1 within 24 hours to assess situation" },
                  rep.burnout_action === "immediate_intervention" && { label: "Mandatory PTO Review", desc: "Enforce recovery time — block calendar and redistribute deals" },
                  rep.burnout_action === "workload_review" && { label: "Deal Load Audit", desc: "Review and cap active deal count; re-assign overdue deals" },
                  rep.burnout_action === "coaching" && { label: "Engagement Coaching Session", desc: "1:1 focused on motivation, career path, and root cause of disengagement" },
                  rep.burnout_action === "coaching" && { label: "Performance Recovery Plan", desc: "30-day plan with weekly check-ins and clear milestones" },
                  rep.burnout_action === "monitor" && { label: "Monthly Wellbeing Check-in", desc: "Informal check-in to catch early stress signals" },
                ].filter(Boolean).slice(0, 4).map((item: any) => (
                  <div key={item.label} className="flex items-start gap-3 bg-slate-800/60 rounded-xl p-3">
                    <div className="w-2 h-2 rounded-full bg-indigo-500 mt-1.5 shrink-0" />
                    <div>
                      <div className="text-sm font-medium text-slate-200">{item.label}</div>
                      <div className="text-xs text-slate-400">{item.desc}</div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

// ── RepCard ───────────────────────────────────────────────────────────────────

function RepCard({ rep, onClick }: { rep: Rep; onClick: () => void }) {
  return (
    <button
      onClick={onClick}
      className="w-full text-left bg-slate-800/60 border border-slate-700/50 rounded-2xl p-5 hover:border-indigo-500/40 hover:bg-slate-800/80 transition-all group"
    >
      <div className="flex items-start justify-between gap-3 mb-3">
        <div>
          <h3 className="font-semibold text-slate-100 group-hover:text-white transition-colors">
            {rep.rep_name}
          </h3>
          <p className="text-xs text-slate-400 mt-0.5">{rep.region}</p>
        </div>
        <div className="flex flex-col items-end gap-1.5 shrink-0">
          <span className={`text-xs font-semibold px-2 py-0.5 rounded-full border ${ACTION_COLOR[rep.burnout_action]}`}>
            {fmt(rep.burnout_action)}
          </span>
          {rep.needs_immediate_action && (
            <span className="text-xs px-2 py-0.5 rounded-full bg-red-500/20 text-red-300 border border-red-500/30">
              ⚠ Urgent
            </span>
          )}
        </div>
      </div>

      <div className="flex gap-2 mb-3 flex-wrap">
        {[
          { label: "Overwork", value: rep.overwork_score, color: "text-amber-400" },
          { label: "Disengage", value: rep.disengagement_score, color: "text-orange-400" },
          { label: "Decline", value: rep.performance_decline_score, color: "text-red-400" },
        ].map(({ label, value, color }) => (
          <div key={label} className="flex flex-col items-center bg-slate-900/60 rounded-lg px-3 py-1.5">
            <span className={`text-sm font-bold ${color}`}>{Math.round(value)}</span>
            <span className="text-xs text-slate-500">{label}</span>
          </div>
        ))}
        <div className="flex flex-col items-center bg-slate-900/60 rounded-lg px-3 py-1.5">
          <span className={`text-sm font-bold ${RISK_COLOR[rep.burnout_risk]}`}>{rep.burnout_composite_score}</span>
          <span className="text-xs text-slate-500">Composite</span>
        </div>
      </div>

      <div className="flex justify-between items-center text-xs text-slate-400">
        <span className={PATTERN_COLOR[rep.burnout_pattern]}>{fmt(rep.burnout_pattern)}</span>
        <span className={rep.predicted_turnover_probability >= 60 ? "text-red-400" : "text-slate-400"}>
          Turnover {rep.predicted_turnover_probability}%
        </span>
        <span className={`text-emerald-400`}>Wellbeing {rep.wellbeing_score}</span>
      </div>
    </button>
  );
}

// ── Page ──────────────────────────────────────────────────────────────────────

export default function SalesRepBurnoutPage() {
  const [reps, setReps] = useState<Rep[]>([]);
  const [summary, setSummary] = useState<Summary | null>(null);
  const [loading, setLoading] = useState(true);
  const [selected, setSelected] = useState<Rep | null>(null);
  const [filterRisk, setFilterRisk] = useState("all");
  const [filterCategory, setFilterCategory] = useState("all");

  useEffect(() => {
    async function load() {
        setLoading(true);
        try {
          const params = new URLSearchParams();
          if (filterRisk     !== "all") params.set("risk", filterRisk);
          if (filterCategory !== "all") params.set("category", filterCategory);
          const res = await fetch(`/api/sales-rep-burnout?${params}`);
          const data = await res.json();
          setReps(data.reps ?? []);
          setSummary(data.summary ?? null);
        } finally {
          setLoading(false);
        }
  }
    load();
  }, [filterRisk, filterCategory]);

  const risks      = ["all", "minimal", "building", "high", "critical"];
  const categories = ["all", "healthy", "stressed", "overloaded", "burned_out"];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
      {selected && (
        <BurnoutModal rep={selected} onClose={() => setSelected(null)} />
      )}

      <div className="mb-8">
        <h1 className="text-3xl font-bold text-white">Sales Rep Burnout Detector</h1>
        <p className="text-slate-400 mt-1">Predict attrition and detect burnout signals before they escalate — protect your team and revenue</p>
      </div>

      {summary && (
        <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-7 gap-4 mb-8">
          {[
            { label: "Total Reps", value: summary.total },
            { label: "At Risk", value: summary.at_risk_count, color: "text-orange-400" },
            { label: "Urgent", value: summary.immediate_action_count, color: "text-red-400" },
            { label: "Avg Burnout", value: summary.avg_burnout_composite_score },
            { label: "Avg Turnover %", value: `${summary.avg_predicted_turnover_probability}%`, color: "text-red-400" },
            { label: "Avg Wellbeing", value: summary.avg_wellbeing_score, color: "text-emerald-400" },
            { label: "Avg Disengage", value: summary.avg_disengagement_score, color: "text-orange-400" },
          ].map(({ label, value, color }) => (
            <div key={label} className="bg-slate-800/60 border border-slate-700/50 rounded-2xl p-4">
              <div className="text-xs text-slate-400 mb-1">{label}</div>
              <div className={`text-2xl font-bold ${color ?? "text-white"}`}>{value}</div>
            </div>
          ))}
        </div>
      )}

      {summary && (
        <div className="bg-slate-800/60 border border-slate-700/50 rounded-2xl p-5 mb-8">
          <div className="flex items-center justify-between mb-3">
            <h2 className="text-sm font-semibold text-slate-300">Team Health Distribution</h2>
            <div className="flex gap-3 flex-wrap">
              {["healthy", "stressed", "overloaded", "burned_out"].map((k) => (
                <div key={k} className="flex items-center gap-1.5 text-xs text-slate-400">
                  <div className={`w-2.5 h-2.5 rounded-full ${CATEGORY_BAR[k]}`} />
                  {fmt(k)} ({summary.category_counts[k] || 0})
                </div>
              ))}
            </div>
          </div>
          <CategoryDistBar counts={summary.category_counts} total={summary.total} />
          <div className="grid grid-cols-3 gap-4 mt-4 text-center">
            <div>
              <div className="text-lg font-bold text-red-400">{summary.avg_predicted_turnover_probability}%</div>
              <div className="text-xs text-slate-400">Avg Turnover Risk</div>
            </div>
            <div>
              <div className="text-lg font-bold text-slate-300">{summary.avg_performance_decline_score}</div>
              <div className="text-xs text-slate-400">Avg Perf. Decline</div>
            </div>
            <div>
              <div className="text-lg font-bold text-emerald-400">{summary.avg_wellbeing_score}</div>
              <div className="text-xs text-slate-400">Avg Wellbeing</div>
            </div>
          </div>
        </div>
      )}

      <div className="flex flex-wrap gap-3 mb-6">
        <div className="flex flex-wrap gap-2">
          {risks.map((r) => (
            <button
              key={r}
              onClick={() => setFilterRisk(r)}
              className={`px-3 py-1.5 rounded-full text-xs font-medium border transition-colors ${
                filterRisk === r
                  ? "bg-indigo-600 border-indigo-500 text-white"
                  : "bg-slate-800/60 border-slate-700 text-slate-400 hover:text-slate-300"
              }`}
            >
              {fmt(r)}
            </button>
          ))}
        </div>
        <div className="flex flex-wrap gap-2">
          {categories.map((c) => (
            <button
              key={c}
              onClick={() => setFilterCategory(c)}
              className={`px-3 py-1.5 rounded-full text-xs font-medium border transition-colors ${
                filterCategory === c
                  ? "bg-indigo-600 border-indigo-500 text-white"
                  : "bg-slate-800/60 border-slate-700 text-slate-400 hover:text-slate-300"
              }`}
            >
              {fmt(c)}
            </button>
          ))}
        </div>
      </div>

      {loading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
          {[...Array(6)].map((_, i) => (
            <div key={i} className="h-44 bg-slate-800/40 rounded-2xl animate-pulse" />
          ))}
        </div>
      ) : reps.length === 0 ? (
        <div className="text-center py-20 text-slate-500">No reps match the selected filters.</div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
          {reps.map((r) => (
            <RepCard key={r.rep_id} rep={r} onClick={() => setSelected(r)} />
          ))}
        </div>
      )}
    </div>
  );
}
