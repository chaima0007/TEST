"use client";

import { useState, useEffect, useRef, useCallback } from "react";

interface RepData {
  rep_id: string;
  rep_name: string;
  region: string;
  misalignment_rating: string;
  misalignment_risk: string;
  primary_misalignment_type: string;
  incentive_action: string;
  behavior_alignment_score: number;
  strategic_alignment_score: number;
  discount_discipline_score: number;
  revenue_quality_score: number;
  misalignment_composite: number;
  is_gaming_quota: boolean;
  requires_plan_review: boolean;
  estimated_revenue_risk_usd: number;
  misalignment_signal: string;
  quota_usd: number;
  closed_won_usd: number;
}

interface Summary {
  total: number;
  rating_counts: Record<string, number>;
  risk_counts: Record<string, number>;
  type_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_misalignment_composite: number;
  gaming_quota_count: number;
  plan_review_count: number;
  avg_behavior_alignment_score: number;
  avg_strategic_alignment_score: number;
  avg_discount_discipline_score: number;
  avg_revenue_quality_score: number;
  total_revenue_risk_usd: number;
}

const RATING_BG: Record<string, string> = {
  aligned:  "bg-emerald-500/20 border-emerald-500/30 text-emerald-300",
  minor:    "bg-sky-500/20 border-sky-500/30 text-sky-300",
  moderate: "bg-amber-500/20 border-amber-500/30 text-amber-300",
  severe:   "bg-orange-500/20 border-orange-500/30 text-orange-300",
  critical: "bg-rose-500/20 border-rose-500/30 text-rose-300",
};
const RATING_COLOR: Record<string, string> = {
  aligned: "#34d399", minor: "#38bdf8", moderate: "#fbbf24", severe: "#f97316", critical: "#f87171",
};
const RATING_LABEL: Record<string, string> = {
  aligned: "Aligned", minor: "Minor", moderate: "Moderate", severe: "Severe", critical: "Critical",
};
const RISK_BG: Record<string, string> = {
  low:      "bg-emerald-500/15 text-emerald-300",
  moderate: "bg-amber-500/15 text-amber-300",
  high:     "bg-orange-500/15 text-orange-300",
  critical: "bg-rose-500/15 text-rose-300",
};
const ACTION_BG: Record<string, string> = {
  no_action:          "bg-emerald-500/15 text-emerald-300",
  monitor:            "bg-sky-500/15 text-sky-300",
  plan_review:        "bg-amber-500/15 text-amber-300",
  manager_coaching:   "bg-orange-500/15 text-orange-300",
  comp_restructure:   "bg-rose-500/15 text-rose-300",
};
const ACTION_LABEL: Record<string, string> = {
  no_action: "No Action", monitor: "Monitor", plan_review: "Plan Review",
  manager_coaching: "Manager Coaching", comp_restructure: "Comp Restructure",
};
const TYPE_LABEL: Record<string, string> = {
  none: "None", sandbagging: "Sandbagging", cherry_picking: "Cherry Picking",
  discount_abuse: "Discount Abuse", account_neglect: "Account Neglect", quota_gaming: "Quota Gaming",
};

function fmt(n: number) {
  return n >= 1_000_000 ? `$${(n / 1_000_000).toFixed(1)}M` : n >= 1_000 ? `$${(n / 1_000).toFixed(0)}K` : `$${n}`;
}

function MisalignmentRing({ pct, color, size = 80 }: { pct: number; color: string; size?: number }) {
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

function AlignmentBar({ score, label }: { score: number; label: string }) {
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

interface ModalProps { rep: RepData; onClose: () => void }

function DetailModal({ rep, onClose }: ModalProps) {
  const [tab, setTab] = useState<"overview" | "scores" | "action">("overview");
  const backdropRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handler = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [onClose]);

  const color = RATING_COLOR[rep.misalignment_rating] ?? "#94a3b8";
  const attain = rep.quota_usd > 0 ? (rep.closed_won_usd / rep.quota_usd) * 100 : 0;

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
              <span className={`text-xs px-2 py-0.5 rounded-full border font-medium ${RATING_BG[rep.misalignment_rating] ?? ""}`}>
                {RATING_LABEL[rep.misalignment_rating] ?? rep.misalignment_rating}
              </span>
              {rep.is_gaming_quota && (
                <span className="text-xs px-2 py-0.5 rounded-full bg-rose-500/20 border border-rose-500/30 text-rose-300">Gaming</span>
              )}
            </div>
            <h2 className="text-white font-bold text-lg">{rep.rep_name}</h2>
            <p className="text-slate-400 text-sm">{rep.region} · Misalignment: <span style={{ color }}>{rep.misalignment_composite}</span></p>
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-white p-1" aria-label="Close">
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <div className="flex border-b border-slate-800">
          {(["overview", "scores", "action"] as const).map((t) => (
            <button key={t} onClick={() => setTab(t)}
              className={`flex-1 py-2.5 text-sm font-medium capitalize transition-colors ${
                tab === t ? "text-indigo-400 border-b-2 border-indigo-500 bg-slate-800/40" : "text-slate-400 hover:text-slate-200"
              }`}>
              {t === "overview" ? "Overview" : t === "scores" ? "Alignment Scores" : "Action Plan"}
            </button>
          ))}
        </div>

        <div className="p-5 space-y-4">
          {tab === "overview" && (
            <>
              <div className="flex items-center justify-center py-2">
                <MisalignmentRing pct={rep.misalignment_composite} color={color} size={110} />
              </div>
              <div className="bg-slate-800/50 rounded-lg p-3">
                <p className="text-xs text-slate-400 mb-1">Misalignment Signal</p>
                <p className="text-sm text-white">{rep.misalignment_signal}</p>
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div className="bg-slate-800/50 rounded-lg p-3">
                  <p className="text-xs text-slate-400">Revenue Risk</p>
                  <p className="text-lg font-bold text-rose-400">{fmt(rep.estimated_revenue_risk_usd)}</p>
                </div>
                <div className="bg-slate-800/50 rounded-lg p-3">
                  <p className="text-xs text-slate-400">Quota Attainment</p>
                  <p className="text-lg font-bold text-indigo-400">{attain.toFixed(0)}%</p>
                </div>
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div className="bg-slate-800/50 rounded-lg p-3">
                  <p className="text-xs text-slate-400">Misalignment Type</p>
                  <p className="text-sm font-medium text-slate-200">{TYPE_LABEL[rep.primary_misalignment_type] ?? rep.primary_misalignment_type}</p>
                </div>
                <div className="bg-slate-800/50 rounded-lg p-3">
                  <p className="text-xs text-slate-400">Plan Review</p>
                  <p className={`text-sm font-medium ${rep.requires_plan_review ? "text-amber-400" : "text-emerald-400"}`}>
                    {rep.requires_plan_review ? "Required" : "Not Needed"}
                  </p>
                </div>
              </div>
            </>
          )}

          {tab === "scores" && (
            <div className="space-y-3">
              <AlignmentBar score={rep.behavior_alignment_score} label="Behavior Alignment" />
              <AlignmentBar score={rep.strategic_alignment_score} label="Strategic Alignment" />
              <AlignmentBar score={rep.discount_discipline_score} label="Discount Discipline" />
              <AlignmentBar score={rep.revenue_quality_score} label="Revenue Quality" />
              <div className="pt-2 border-t border-slate-800">
                <div className="flex justify-between items-center">
                  <span className="text-sm text-slate-400">Misalignment Composite</span>
                  <span className="text-lg font-bold" style={{ color }}>{rep.misalignment_composite}</span>
                </div>
                <p className="text-xs text-slate-500 mt-1">Higher composite = greater incentive misalignment</p>
              </div>
            </div>
          )}

          {tab === "action" && (
            <div className="space-y-4">
              <div className="bg-slate-800/50 rounded-lg p-4">
                <p className="text-xs text-slate-400 mb-2">Recommended Action</p>
                <span className={`text-sm px-3 py-1.5 rounded-lg font-medium ${ACTION_BG[rep.incentive_action] ?? ""}`}>
                  {ACTION_LABEL[rep.incentive_action] ?? rep.incentive_action}
                </span>
              </div>
              <div className="space-y-2">
                <div className="flex justify-between p-2 rounded bg-slate-800/40">
                  <span className="text-xs text-slate-400">Misalignment Type</span>
                  <span className="text-xs text-slate-200">{TYPE_LABEL[rep.primary_misalignment_type] ?? rep.primary_misalignment_type}</span>
                </div>
                <div className="flex justify-between p-2 rounded bg-slate-800/40">
                  <span className="text-xs text-slate-400">Risk Level</span>
                  <span className={`text-xs font-medium ${RISK_BG[rep.misalignment_risk] ?? ""}`}>{rep.misalignment_risk.toUpperCase()}</span>
                </div>
                <div className="flex justify-between p-2 rounded bg-slate-800/40">
                  <span className="text-xs text-slate-400">Revenue Risk</span>
                  <span className="text-xs text-rose-400 font-medium">{fmt(rep.estimated_revenue_risk_usd)}</span>
                </div>
                <div className="flex justify-between p-2 rounded bg-slate-800/40">
                  <span className="text-xs text-slate-400">Quota Gaming</span>
                  <span className={`text-xs font-medium ${rep.is_gaming_quota ? "text-rose-400" : "text-emerald-400"}`}>
                    {rep.is_gaming_quota ? "Detected" : "Not Detected"}
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

const RATING_FILTERS = ["all", "aligned", "minor", "moderate", "severe", "critical"] as const;
type RatingFilter = typeof RATING_FILTERS[number];

const RATING_COLORS: Record<string, string> = {
  aligned: "#34d399", minor: "#38bdf8", moderate: "#fbbf24", severe: "#f97316", critical: "#f87171",
};
const TYPE_COLORS: Record<string, string> = {
  none: "#34d399", sandbagging: "#f87171", cherry_picking: "#fbbf24",
  discount_abuse: "#f97316", account_neglect: "#818cf8", quota_gaming: "#e879f9",
};

export default function RepIncentiveMisalignmentEnginePage() {
  const [data, setData] = useState<{ reps: RepData[]; summary: Summary } | null>(null);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState<RatingFilter>("all");
  const [selected, setSelected] = useState<RepData | null>(null);

  const fetchData = useCallback(async (rating: RatingFilter) => {
    setLoading(true);
    const params = new URLSearchParams();
    if (rating !== "all") params.set("rating", rating);
    const res = await fetch(`/api/rep-incentive-misalignment-engine?${params}`);
    const json = await res.json();
    setData(json);
    setLoading(false);
  }, []);

  useEffect(() => { fetchData(filter); }, [filter, fetchData]);

  const s = data?.summary;
  const reps = data?.reps ?? [];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
      {selected && <DetailModal rep={selected} onClose={() => setSelected(null)} />}

      <div className="mb-6">
        <h1 className="text-2xl font-bold text-white">Rep Incentive Misalignment Engine</h1>
        <p className="text-slate-400 text-sm mt-1">
          Detect when comp plans drive wrong behaviors — sandbagging, cherry-picking, discount abuse, quota gaming
        </p>
      </div>

      {/* KPI Strip */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
          <p className="text-xs text-slate-400 mb-1">Total Reps</p>
          <p className="text-2xl font-bold text-white">{s?.total ?? "—"}</p>
        </div>
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
          <p className="text-xs text-slate-400 mb-1">Gaming Quota</p>
          <p className="text-2xl font-bold text-rose-400">{s?.gaming_quota_count ?? "—"}</p>
        </div>
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
          <p className="text-xs text-slate-400 mb-1">Plan Review Needed</p>
          <p className="text-2xl font-bold text-amber-400">{s?.plan_review_count ?? "—"}</p>
        </div>
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
          <p className="text-xs text-slate-400 mb-1">Revenue at Risk</p>
          <p className="text-2xl font-bold text-orange-400">{s ? fmt(s.total_revenue_risk_usd) : "—"}</p>
        </div>
      </div>

      {/* Alignment Scores + Distributions */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
          <h3 className="text-sm font-semibold text-slate-300 mb-3">Avg Alignment Scores</h3>
          <div className="space-y-3">
            <AlignmentBar score={s?.avg_behavior_alignment_score ?? 0} label="Behavior Alignment" />
            <AlignmentBar score={s?.avg_strategic_alignment_score ?? 0} label="Strategic Alignment" />
            <AlignmentBar score={s?.avg_discount_discipline_score ?? 0} label="Discount Discipline" />
            <AlignmentBar score={s?.avg_revenue_quality_score ?? 0} label="Revenue Quality" />
          </div>
        </div>
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 space-y-4">
          <div>
            <div className="flex justify-between items-center mb-2">
              <h3 className="text-sm font-semibold text-slate-300">Rating Distribution</h3>
            </div>
            <DistBar counts={s?.rating_counts ?? {}} colors={RATING_COLORS} />
            <div className="flex flex-wrap gap-2 mt-2">
              {Object.entries(s?.rating_counts ?? {}).map(([k, v]) => (
                <span key={k} className="text-xs" style={{ color: RATING_COLORS[k] ?? "#94a3b8" }}>
                  {RATING_LABEL[k] ?? k}: {v}
                </span>
              ))}
            </div>
          </div>
          <div>
            <div className="flex justify-between items-center mb-2">
              <h3 className="text-sm font-semibold text-slate-300">Misalignment Types</h3>
            </div>
            <DistBar counts={s?.type_counts ?? {}} colors={TYPE_COLORS} />
            <div className="flex flex-wrap gap-2 mt-2">
              {Object.entries(s?.type_counts ?? {}).map(([k, v]) => (
                <span key={k} className="text-xs" style={{ color: TYPE_COLORS[k] ?? "#94a3b8" }}>
                  {TYPE_LABEL[k] ?? k}: {v}
                </span>
              ))}
            </div>
          </div>
          <div className="border-t border-slate-800 pt-3">
            <div className="flex justify-between">
              <span className="text-xs text-slate-400">Avg Misalignment Composite</span>
              <span className="text-sm font-bold text-amber-400">{s?.avg_misalignment_composite ?? "—"}</span>
            </div>
          </div>
        </div>
      </div>

      {/* Filter tabs */}
      <div className="flex flex-wrap gap-2 mb-4">
        {RATING_FILTERS.map((f) => (
          <button key={f} onClick={() => setFilter(f)}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors border ${
              filter === f
                ? "bg-indigo-600 border-indigo-500 text-white"
                : "bg-slate-800 border-slate-700 text-slate-400 hover:text-white hover:border-slate-600"
            }`}>
            {f === "all" ? "All Reps" : RATING_LABEL[f] ?? f}
            {f !== "all" && s?.rating_counts?.[f] !== undefined && (
              <span className="ml-1 opacity-70">({s.rating_counts[f]})</span>
            )}
          </button>
        ))}
      </div>

      {/* Rep cards */}
      {loading ? (
        <div className="flex items-center justify-center h-48">
          <div className="w-8 h-8 border-2 border-indigo-500 border-t-transparent rounded-full animate-spin" />
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
          {reps.map((rep) => {
            const color = RATING_COLOR[rep.misalignment_rating] ?? "#94a3b8";
            return (
              <div key={rep.rep_id} onClick={() => setSelected(rep)}
                className="bg-slate-900 border border-slate-800 rounded-xl p-4 cursor-pointer hover:border-slate-600 transition-all hover:bg-slate-800/60">
                <div className="flex items-start justify-between mb-3">
                  <div>
                    <div className="flex items-center gap-2 mb-1">
                      <span className={`text-xs px-2 py-0.5 rounded-full border font-medium ${RATING_BG[rep.misalignment_rating] ?? ""}`}>
                        {RATING_LABEL[rep.misalignment_rating] ?? rep.misalignment_rating}
                      </span>
                      {rep.is_gaming_quota && (
                        <span className="text-xs px-1.5 py-0.5 rounded bg-rose-500/20 text-rose-300 font-medium">Gaming</span>
                      )}
                    </div>
                    <h3 className="text-white font-semibold text-sm">{rep.rep_name}</h3>
                    <p className="text-slate-400 text-xs">{rep.region}</p>
                  </div>
                  <MisalignmentRing pct={rep.misalignment_composite} color={color} size={72} />
                </div>

                <div className="space-y-1.5 mb-3">
                  <AlignmentBar score={rep.behavior_alignment_score} label="Behavior" />
                  <AlignmentBar score={rep.strategic_alignment_score} label="Strategic" />
                  <AlignmentBar score={rep.discount_discipline_score} label="Discount" />
                  <AlignmentBar score={rep.revenue_quality_score} label="Rev. Quality" />
                </div>

                <div className="border-t border-slate-800 pt-2 flex items-center justify-between">
                  <span className={`text-xs px-2 py-0.5 rounded font-medium ${ACTION_BG[rep.incentive_action] ?? ""}`}>
                    {ACTION_LABEL[rep.incentive_action] ?? rep.incentive_action}
                  </span>
                  {rep.estimated_revenue_risk_usd > 0 && (
                    <span className="text-xs text-rose-400 font-medium">{fmt(rep.estimated_revenue_risk_usd)} risk</span>
                  )}
                </div>
                <p className="text-xs text-slate-500 mt-2 truncate">{rep.misalignment_signal}</p>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
