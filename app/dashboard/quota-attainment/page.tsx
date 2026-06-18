"use client";

import { useEffect, useState, useCallback } from "react";

interface RepData {
  rep_id: string;
  rep_name: string;
  manager_id: string;
  attainment_likelihood: string;
  attainment_risk: string;
  performance_trend: string;
  attainment_action: string;
  attainment_pct: number;
  projected_attainment: number;
  gap_to_quota: number;
  coverage_ratio: number;
  confidence_score: number;
  momentum_score: number;
  pace_score: number;
  is_at_risk: boolean;
  needs_coaching: boolean;
  closed_won_ytd: number;
  quota_ytd: number;
}

interface Summary {
  total: number;
  likelihood_counts: Record<string, number>;
  risk_counts: Record<string, number>;
  trend_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_attainment_pct: number;
  avg_projected_attainment: number;
  total_gap_to_quota: number;
  at_risk_count: number;
  coaching_count: number;
  avg_confidence_score: number;
  avg_momentum_score: number;
  likely_attainer_count: number;
}

const LIKELIHOOD_COLOR: Record<string, string> = {
  very_likely:  "text-emerald-400 bg-emerald-400/10 border-emerald-400/20",
  likely:       "text-green-400 bg-green-400/10 border-green-400/20",
  possible:     "text-yellow-400 bg-yellow-400/10 border-yellow-400/20",
  unlikely:     "text-orange-400 bg-orange-400/10 border-orange-400/20",
  very_unlikely:"text-red-400 bg-red-400/10 border-red-400/20",
};

const RISK_COLOR: Record<string, string> = {
  low:      "text-emerald-400",
  medium:   "text-yellow-400",
  high:     "text-orange-400",
  critical: "text-red-400",
};

const TREND_COLOR: Record<string, string> = {
  accelerating: "text-emerald-400",
  on_track:     "text-sky-400",
  slowing:      "text-yellow-400",
  declining:    "text-red-400",
};

const TREND_ICON: Record<string, string> = {
  accelerating: "↑↑",
  on_track:     "→",
  slowing:      "↘",
  declining:    "↓↓",
};

function fmt(n: number) {
  if (n >= 1_000_000) return `$${(n / 1_000_000).toFixed(1)}M`;
  if (n >= 1_000)     return `$${(n / 1_000).toFixed(0)}K`;
  return `$${n}`;
}

function AttainmentRing({ pct, projected }: { pct: number; projected: number }) {
  const r = 38, cx = 48, cy = 48;
  const circ = 2 * Math.PI * r;
  const current_arc = Math.min(pct / 100, 1.5) * circ;
  const proj_arc    = Math.min(projected / 100, 1.5) * circ;
  const color = projected >= 100 ? "#10b981" : projected >= 80 ? "#38bdf8" : projected >= 60 ? "#fbbf24" : "#f87171";
  return (
    <svg viewBox="0 0 96 96" className="w-24 h-24">
      <circle cx={cx} cy={cy} r={r} fill="none" stroke="#1e293b" strokeWidth="8" />
      <circle cx={cx} cy={cy} r={r} fill="none" stroke="#334155" strokeWidth="8"
        strokeDasharray={`${proj_arc} ${circ - proj_arc}`}
        strokeLinecap="round"
        transform={`rotate(-90 ${cx} ${cy})`} opacity="0.4" />
      <circle cx={cx} cy={cy} r={r} fill="none" stroke={color} strokeWidth="8"
        strokeDasharray={`${current_arc} ${circ - current_arc}`}
        strokeLinecap="round"
        transform={`rotate(-90 ${cx} ${cy})`} />
      <text x={cx} y={cy - 4} textAnchor="middle" fill="white" fontSize="11" fontWeight="bold">
        {pct.toFixed(0)}%
      </text>
      <text x={cx} y={cy + 10} textAnchor="middle" fill="#94a3b8" fontSize="7">
        →{projected.toFixed(0)}%
      </text>
    </svg>
  );
}

function LikelihoodDistBar({ counts }: { counts: Record<string, number> }) {
  const order = ["very_likely", "likely", "possible", "unlikely", "very_unlikely"];
  const total = Object.values(counts).reduce((a, b) => a + b, 0) || 1;
  const colors = ["#10b981", "#22c55e", "#fbbf24", "#fb923c", "#f87171"];
  const labels = ["V.Likely", "Likely", "Possible", "Unlikely", "V.Unlikely"];
  return (
    <div className="space-y-1.5">
      {order.map((k, i) => {
        const v = counts[k] || 0;
        const w = (v / total) * 100;
        return (
          <div key={k} className="flex items-center gap-2 text-xs">
            <span className="w-16 text-slate-400 text-right">{labels[i]}</span>
            <div className="flex-1 h-2 bg-slate-800 rounded-full overflow-hidden">
              <div className="h-full rounded-full transition-all" style={{ width: `${w}%`, backgroundColor: colors[i] }} />
            </div>
            <span className="w-4 text-slate-300">{v}</span>
          </div>
        );
      })}
    </div>
  );
}

function MiniBar({ value, max, color }: { value: number; max: number; color: string }) {
  return (
    <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
      <div className="h-full rounded-full" style={{ width: `${Math.min(100, (value / max) * 100)}%`, backgroundColor: color }} />
    </div>
  );
}

function RepCard({ rep, onClick }: { rep: RepData; onClick: () => void }) {
  const lc = LIKELIHOOD_COLOR[rep.attainment_likelihood] || "text-slate-400 bg-slate-400/10 border-slate-400/20";
  const rc = RISK_COLOR[rep.attainment_risk] || "text-slate-400";
  const tc = TREND_COLOR[rep.performance_trend] || "text-slate-400";
  const ti = TREND_ICON[rep.performance_trend] || "→";
  return (
    <button onClick={onClick}
      className="bg-slate-800/60 border border-slate-700 rounded-xl p-4 text-left hover:border-indigo-500/50 hover:bg-slate-800 transition-all w-full">
      <div className="flex items-start justify-between mb-3">
        <div>
          <div className="font-semibold text-slate-100 text-sm">{rep.rep_name}</div>
          <div className="text-xs text-slate-500 mt-0.5">{rep.rep_id} · {rep.manager_id}</div>
        </div>
        <div className="flex flex-col items-end gap-1">
          <span className={`text-xs font-medium px-2 py-0.5 rounded-full border ${lc}`}>
            {rep.attainment_likelihood.replace("_", " ")}
          </span>
          {rep.is_at_risk && (
            <span className="text-xs text-red-400 bg-red-400/10 px-1.5 py-0.5 rounded border border-red-400/20">at risk</span>
          )}
        </div>
      </div>
      <div className="flex items-center gap-4 mb-3">
        <AttainmentRing pct={rep.attainment_pct} projected={rep.projected_attainment} />
        <div className="flex-1 space-y-1.5">
          <div className="flex justify-between text-xs">
            <span className="text-slate-400">Gap to Quota</span>
            <span className="text-slate-200">{fmt(rep.gap_to_quota)}</span>
          </div>
          <div className="flex justify-between text-xs">
            <span className="text-slate-400">Coverage</span>
            <span className="text-slate-200">{rep.coverage_ratio.toFixed(2)}×</span>
          </div>
          <div className="flex justify-between text-xs">
            <span className="text-slate-400">Risk</span>
            <span className={rc}>{rep.attainment_risk}</span>
          </div>
          <div className="flex justify-between text-xs">
            <span className="text-slate-400">Trend</span>
            <span className={tc}>{ti} {rep.performance_trend.replace("_", " ")}</span>
          </div>
        </div>
      </div>
      <div className="space-y-1">
        <div className="flex justify-between text-xs mb-0.5">
          <span className="text-slate-400">Confidence</span>
          <span className="text-slate-300">{rep.confidence_score.toFixed(0)}</span>
        </div>
        <MiniBar value={rep.confidence_score} max={100} color="#818cf8" />
        <div className="flex justify-between text-xs mb-0.5 mt-1">
          <span className="text-slate-400">Momentum</span>
          <span className="text-slate-300">{rep.momentum_score.toFixed(0)}</span>
        </div>
        <MiniBar value={rep.momentum_score} max={100} color="#22d3ee" />
      </div>
    </button>
  );
}

function RepModal({ rep, onClose }: { rep: RepData; onClose: () => void }) {
  const [tab, setTab] = useState<"attainment" | "pipeline" | "coaching">("attainment");
  useEffect(() => {
    const fn = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    document.addEventListener("keydown", fn);
    return () => document.removeEventListener("keydown", fn);
  }, [onClose]);

  const lc = LIKELIHOOD_COLOR[rep.attainment_likelihood] || "text-slate-400 bg-slate-400/10 border-slate-400/20";

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4"
      onClick={(e) => { if (e.target === e.currentTarget) onClose(); }}>
      <div className="absolute inset-0 bg-black/60 backdrop-blur-sm" />
      <div className="relative bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-lg shadow-2xl">
        <div className="flex items-start justify-between p-5 border-b border-slate-800">
          <div>
            <h2 className="text-lg font-bold text-white">{rep.rep_name}</h2>
            <div className="flex items-center gap-2 mt-1 flex-wrap">
              <span className={`text-xs px-2 py-0.5 rounded-full border ${lc}`}>
                {rep.attainment_likelihood.replace("_", " ")}
              </span>
              <span className={`text-xs font-medium ${RISK_COLOR[rep.attainment_risk]}`}>
                {rep.attainment_risk} risk
              </span>
              {rep.needs_coaching && (
                <span className="text-xs text-violet-400 bg-violet-400/10 px-1.5 py-0.5 rounded border border-violet-400/20">needs coaching</span>
              )}
            </div>
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-white text-xl p-1">×</button>
        </div>
        <div className="flex border-b border-slate-800">
          {(["attainment", "pipeline", "coaching"] as const).map((t) => (
            <button key={t} onClick={() => setTab(t)}
              className={`flex-1 py-2.5 text-xs font-medium capitalize transition-colors ${tab === t ? "text-indigo-400 border-b-2 border-indigo-400" : "text-slate-400 hover:text-slate-200"}`}>
              {t}
            </button>
          ))}
        </div>
        <div className="p-5 max-h-96 overflow-y-auto">
          {tab === "attainment" && (
            <div className="space-y-3">
              <div className="flex items-center justify-center mb-4">
                <AttainmentRing pct={rep.attainment_pct} projected={rep.projected_attainment} />
              </div>
              {[
                ["Attainment %", `${rep.attainment_pct.toFixed(1)}%`],
                ["Projected %", `${rep.projected_attainment.toFixed(1)}%`],
                ["Closed Won YTD", fmt(rep.closed_won_ytd)],
                ["Quota YTD", fmt(rep.quota_ytd)],
                ["Gap to Quota", fmt(rep.gap_to_quota)],
                ["Action", rep.attainment_action.replace(/_/g, " ")],
              ].map(([label, value]) => (
                <div key={label} className="flex justify-between text-sm border-b border-slate-800 pb-2">
                  <span className="text-slate-400">{label}</span>
                  <span className="text-slate-100 font-medium">{value}</span>
                </div>
              ))}
            </div>
          )}
          {tab === "pipeline" && (
            <div className="space-y-3">
              {[
                ["Coverage Ratio", `${rep.coverage_ratio.toFixed(2)}×`],
                ["Confidence Score", `${rep.confidence_score.toFixed(0)}/100`],
                ["Momentum Score", `${rep.momentum_score.toFixed(0)}/100`],
                ["Pace Score", `${rep.pace_score.toFixed(0)}/100`],
              ].map(([label, value]) => (
                <div key={label} className="space-y-1">
                  <div className="flex justify-between text-sm">
                    <span className="text-slate-400">{label}</span>
                    <span className="text-slate-100 font-medium">{value}</span>
                  </div>
                  <MiniBar
                    value={parseFloat(String(value).replace(/[^0-9.]/g, ""))}
                    max={label === "Coverage Ratio" ? 2 : 100}
                    color={label === "Coverage Ratio" ? "#10b981" : label === "Confidence Score" ? "#818cf8" : label === "Momentum Score" ? "#22d3ee" : "#fbbf24"}
                  />
                </div>
              ))}
              <div className="pt-2 border-t border-slate-800">
                <div className="flex justify-between text-sm">
                  <span className="text-slate-400">Performance Trend</span>
                  <span className={`${TREND_COLOR[rep.performance_trend]} font-medium`}>
                    {TREND_ICON[rep.performance_trend]} {rep.performance_trend.replace("_", " ")}
                  </span>
                </div>
              </div>
            </div>
          )}
          {tab === "coaching" && (
            <div className="space-y-3">
              <div className="flex justify-between text-sm border-b border-slate-800 pb-2">
                <span className="text-slate-400">Needs Coaching</span>
                <span className={rep.needs_coaching ? "text-violet-400" : "text-emerald-400"}>
                  {rep.needs_coaching ? "Yes" : "No"}
                </span>
              </div>
              <div className="flex justify-between text-sm border-b border-slate-800 pb-2">
                <span className="text-slate-400">At Risk</span>
                <span className={rep.is_at_risk ? "text-red-400" : "text-emerald-400"}>
                  {rep.is_at_risk ? "Yes" : "No"}
                </span>
              </div>
              <div className="flex justify-between text-sm border-b border-slate-800 pb-2">
                <span className="text-slate-400">Recommended Action</span>
                <span className="text-indigo-400 font-medium capitalize">{rep.attainment_action.replace(/_/g, " ")}</span>
              </div>
              <div className="flex justify-between text-sm border-b border-slate-800 pb-2">
                <span className="text-slate-400">Risk Level</span>
                <span className={`${RISK_COLOR[rep.attainment_risk]} font-medium capitalize`}>{rep.attainment_risk}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-slate-400">Manager</span>
                <span className="text-slate-200">{rep.manager_id}</span>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default function QuotaAttainmentPage() {
  const [reps, setReps]       = useState<RepData[]>([]);
  const [summary, setSummary] = useState<Summary | null>(null);
  const [loading, setLoading] = useState(true);
  const [selected, setSelected] = useState<RepData | null>(null);
  const [filterLikelihood, setFilterLikelihood] = useState("all");
  const [filterRisk, setFilterRisk]             = useState("all");

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const params = new URLSearchParams();
      if (filterLikelihood !== "all") params.set("likelihood", filterLikelihood);
      if (filterRisk !== "all")       params.set("risk", filterRisk);
      const res = await fetch(`/api/quota-attainment?${params}`);
      const data = await res.json();
      setReps(data.reps || []);
      setSummary(data.summary || null);
    } catch {}
    setLoading(false);
  }, [filterLikelihood, filterRisk]);

  useEffect(() => { load(); }, [load]);

  const likelihoods = ["all", "very_likely", "likely", "possible", "unlikely", "very_unlikely"];
  const risks       = ["all", "low", "medium", "high", "critical"];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
      <div className="max-w-7xl mx-auto space-y-6">
        {/* Header */}
        <div>
          <h1 className="text-2xl font-bold text-white">Quota Attainment Predictor</h1>
          <p className="text-slate-400 text-sm mt-1">Rep-level quota attainment likelihood, risk, and recommended actions</p>
        </div>

        {/* KPIs */}
        {summary && (
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {[
              { label: "Avg Attainment", value: `${summary.avg_attainment_pct.toFixed(1)}%`, sub: "current period", color: "text-sky-400" },
              { label: "Avg Projected", value: `${summary.avg_projected_attainment.toFixed(1)}%`, sub: "end-of-period", color: "text-emerald-400" },
              { label: "Total Gap", value: fmt(summary.total_gap_to_quota), sub: `${summary.at_risk_count} at risk`, color: "text-red-400" },
              { label: "Likely Attainers", value: `${summary.likely_attainer_count}/${summary.total}`, sub: `${summary.coaching_count} need coaching`, color: "text-violet-400" },
            ].map((k) => (
              <div key={k.label} className="bg-slate-800/60 border border-slate-700 rounded-xl p-4">
                <div className="text-xs text-slate-400 mb-1">{k.label}</div>
                <div className={`text-2xl font-bold ${k.color}`}>{k.value}</div>
                <div className="text-xs text-slate-500 mt-1">{k.sub}</div>
              </div>
            ))}
          </div>
        )}

        {/* Likelihood Distribution */}
        {summary && (
          <div className="bg-slate-800/60 border border-slate-700 rounded-xl p-5">
            <h2 className="text-sm font-semibold text-slate-300 mb-4">Attainment Likelihood Distribution</h2>
            <LikelihoodDistBar counts={summary.likelihood_counts} />
          </div>
        )}

        {/* Filters */}
        <div className="flex flex-wrap gap-3">
          <div className="flex gap-1 bg-slate-800/60 border border-slate-700 rounded-lg p-1">
            {likelihoods.map((l) => (
              <button key={l} onClick={() => setFilterLikelihood(l)}
                className={`px-3 py-1.5 rounded-md text-xs font-medium transition-colors ${filterLikelihood === l ? "bg-indigo-600 text-white" : "text-slate-400 hover:text-white"}`}>
                {l === "all" ? "All" : l.replace("_", " ")}
              </button>
            ))}
          </div>
          <div className="flex gap-1 bg-slate-800/60 border border-slate-700 rounded-lg p-1">
            {risks.map((r) => (
              <button key={r} onClick={() => setFilterRisk(r)}
                className={`px-3 py-1.5 rounded-md text-xs font-medium transition-colors ${filterRisk === r ? "bg-indigo-600 text-white" : "text-slate-400 hover:text-white"}`}>
                {r === "all" ? "All Risk" : r}
              </button>
            ))}
          </div>
        </div>

        {/* Rep Cards */}
        {loading ? (
          <div className="text-center text-slate-400 py-12">Loading...</div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
            {reps.map((rep) => (
              <RepCard key={rep.rep_id} rep={rep} onClick={() => setSelected(rep)} />
            ))}
          </div>
        )}
      </div>
      {selected && <RepModal rep={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
