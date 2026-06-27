"use client";

import { useState, useEffect } from "react";

// ── Types ─────────────────────────────────────────────────────────────────────

interface RepData {
  rep_id: string;
  rep_name: string;
  region: string;
  comp_risk_level: string;
  gaming_pattern: string;
  incentive_alignment: string;
  comp_action: string;
  sandbagging_score: number;
  spiff_dependency_score: number;
  discount_behavior_score: number;
  attainment_consistency_score: number;
  compensation_efficiency_score: number;
  estimated_overcompensation: number;
  quota_accuracy_score: number;
  is_gaming_comp: boolean;
  needs_comp_review: boolean;
  base_salary: number;
  ote_salary: number;
  quota: number;
  revenue_closed_qtd: number;
  avg_discount_pct: number;
  quota_attainment_q1: number;
  quota_attainment_q2: number;
  quota_attainment_q3: number;
}

interface Summary {
  total: number;
  risk_counts: Record<string, number>;
  pattern_counts: Record<string, number>;
  alignment_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_compensation_efficiency_score: number;
  avg_sandbagging_score: number;
  total_estimated_overcompensation: number;
  gaming_count: number;
  review_needed_count: number;
  avg_spiff_dependency_score: number;
  avg_discount_behavior_score: number;
  avg_quota_accuracy_score: number;
}

// ── Helpers ───────────────────────────────────────────────────────────────────

const RISK_COLOR: Record<string, string> = {
  low:      "text-emerald-400",
  moderate: "text-amber-400",
  high:     "text-orange-400",
  critical: "text-red-400",
};

const RISK_BG: Record<string, string> = {
  low:      "bg-emerald-900/40 border-emerald-700/40",
  moderate: "bg-amber-900/40 border-amber-700/40",
  high:     "bg-orange-900/40 border-orange-700/40",
  critical: "bg-red-900/40 border-red-700/40",
};

const PATTERN_COLOR: Record<string, string> = {
  clean:          "text-emerald-400",
  sandbagging:    "text-yellow-400",
  spiff_chasing:  "text-orange-400",
  discount_heavy: "text-rose-400",
  mixed:          "text-red-400",
};

const ACTION_COLOR: Record<string, string> = {
  maintain:         "bg-emerald-900/50 text-emerald-300 border-emerald-700/50",
  monitor:          "bg-amber-900/50 text-amber-300 border-amber-700/50",
  restructure:      "bg-orange-900/50 text-orange-300 border-orange-700/50",
  immediate_review: "bg-red-900/50 text-red-300 border-red-700/50",
};

function fmt$(v: number) {
  return v >= 1_000_000
    ? `$${(v / 1_000_000).toFixed(1)}M`
    : v >= 1_000
    ? `$${(v / 1_000).toFixed(0)}K`
    : `$${v.toFixed(0)}`;
}

// ── CompEfficiencyMeter SVG ───────────────────────────────────────────────────

function CompEfficiencyMeter({ score, risk }: { score: number; risk: string }) {
  const r = 36, cx = 48, cy = 52;
  const circ = 2 * Math.PI * r;
  const arc  = circ * 0.75;
  const fill = arc * Math.min(1, score / 100);
  const strokeColor =
    score >= 70 ? "#34d399" :
    score >= 50 ? "#fbbf24" :
    score >= 30 ? "#f97316" : "#f87171";

  return (
    <svg width="96" height="80" viewBox="0 0 96 80">
      <path
        d={`M${cx - r * Math.cos(Math.PI * 0.75)},${cy - r * Math.sin(Math.PI * 0.75)}
           A${r},${r} 0 1 1 ${cx + r * Math.cos(Math.PI * 0.75)},${cy - r * Math.sin(Math.PI * 0.75)}`}
        fill="none" stroke="#1e293b" strokeWidth="8"
        strokeLinecap="round"
      />
      <path
        d={`M${cx - r * Math.cos(Math.PI * 0.75)},${cy - r * Math.sin(Math.PI * 0.75)}
           A${r},${r} 0 1 1 ${cx + r * Math.cos(Math.PI * 0.75)},${cy - r * Math.sin(Math.PI * 0.75)}`}
        fill="none" stroke={strokeColor} strokeWidth="8"
        strokeLinecap="round"
        strokeDasharray={`${fill} ${arc}`}
        style={{ transition: "stroke-dasharray .6s ease" }}
      />
      <text x={cx} y={cy - 4} textAnchor="middle" fill="white" fontSize="16" fontWeight="700">
        {score.toFixed(0)}
      </text>
      <text x={cx} y={cy + 12} textAnchor="middle" fill="#94a3b8" fontSize="8">
        Efficiency
      </text>
    </svg>
  );
}

// ── GamingPatternBar ──────────────────────────────────────────────────────────

function GamingPatternBar({ counts }: { counts: Record<string, number> }) {
  const order = ["clean", "sandbagging", "spiff_chasing", "discount_heavy", "mixed"];
  const colors = ["#34d399", "#fbbf24", "#f97316", "#f87171", "#dc2626"];
  const total = Object.values(counts).reduce((s, v) => s + v, 0) || 1;
  return (
    <div className="space-y-2">
      <div className="flex h-3 rounded-full overflow-hidden">
        {order.map((k, i) => {
          const w = ((counts[k] || 0) / total) * 100;
          return w > 0 ? (
            <div key={k} style={{ width: `${w}%`, background: colors[i] }} title={`${k}: ${counts[k]}`} />
          ) : null;
        })}
      </div>
      <div className="flex flex-wrap gap-x-4 gap-y-1">
        {order.map((k, i) =>
          (counts[k] || 0) > 0 ? (
            <span key={k} className="flex items-center gap-1 text-xs text-slate-400">
              <span className="w-2 h-2 rounded-full inline-block" style={{ background: colors[i] }} />
              {k.replace("_", " ")} ({counts[k]})
            </span>
          ) : null
        )}
      </div>
    </div>
  );
}

// ── RepModal ──────────────────────────────────────────────────────────────────

function RepModal({ rep, onClose }: { rep: RepData; onClose: () => void }) {
  const [tab, setTab] = useState<"comp" | "attainment" | "actions">("comp");

  useEffect(() => {
    const h = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    document.addEventListener("keydown", h);
    return () => document.removeEventListener("keydown", h);
  }, [onClose]);

  const scoreBar = (label: string, val: number, invert = false) => {
    const effective = invert ? 100 - val : val;
    const color = effective >= 70 ? "bg-emerald-500" : effective >= 45 ? "bg-amber-500" : "bg-red-500";
    return (
      <div>
        <div className="flex justify-between text-xs mb-1">
          <span className="text-slate-400">{label}</span>
          <span className="text-white font-medium">{val.toFixed(1)}</span>
        </div>
        <div className="h-1.5 bg-slate-700 rounded-full overflow-hidden">
          <div className={`h-full rounded-full ${color} transition-all duration-500`} style={{ width: `${val}%` }} />
        </div>
      </div>
    );
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4" onClick={onClose}>
      <div className="absolute inset-0 bg-black/70 backdrop-blur-sm" />
      <div
        className="relative bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-lg shadow-2xl overflow-hidden"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="p-5 border-b border-slate-800">
          <div className="flex items-start justify-between gap-3">
            <div>
              <h2 className="text-white font-bold text-lg">{rep.rep_name}</h2>
              <p className="text-slate-400 text-sm">{rep.region}</p>
            </div>
            <div className="flex items-center gap-2">
              <span className={`px-2 py-0.5 rounded-full text-xs font-semibold border ${ACTION_COLOR[rep.comp_action]}`}>
                {rep.comp_action.replace("_", " ")}
              </span>
              <button onClick={onClose} className="text-slate-500 hover:text-white transition-colors text-xl leading-none">×</button>
            </div>
          </div>
          <div className="flex gap-2 mt-3">
            {(["comp", "attainment", "actions"] as const).map((t) => (
              <button
                key={t}
                onClick={() => setTab(t)}
                className={`px-3 py-1 rounded-lg text-xs font-medium transition-colors ${tab === t ? "bg-indigo-600 text-white" : "text-slate-400 hover:text-white hover:bg-slate-800"}`}
              >
                {t === "comp" ? "Comp Analysis" : t === "attainment" ? "Attainment" : "Actions"}
              </button>
            ))}
          </div>
        </div>

        <div className="p-5 overflow-y-auto max-h-[60vh]">
          {tab === "comp" && (
            <div className="space-y-4">
              <div className="flex items-center gap-4">
                <CompEfficiencyMeter score={rep.compensation_efficiency_score} risk={rep.comp_risk_level} />
                <div className="space-y-1 flex-1">
                  <div className="flex justify-between text-sm">
                    <span className="text-slate-400">OTE</span>
                    <span className="text-white font-medium">{fmt$(rep.ote_salary)}</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-slate-400">Quota</span>
                    <span className="text-white font-medium">{fmt$(rep.quota)}</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-slate-400">Revenue QTD</span>
                    <span className="text-white font-medium">{fmt$(rep.revenue_closed_qtd)}</span>
                  </div>
                  {rep.estimated_overcompensation > 0 && (
                    <div className="flex justify-between text-sm">
                      <span className="text-red-400">Est. Overpay</span>
                      <span className="text-red-400 font-bold">{fmt$(rep.estimated_overcompensation)}</span>
                    </div>
                  )}
                </div>
              </div>
              <div className="space-y-3">
                {scoreBar("Compensation Efficiency", rep.compensation_efficiency_score)}
                {scoreBar("Quota Accuracy Score", rep.quota_accuracy_score)}
                {scoreBar("Attainment Consistency", rep.attainment_consistency_score)}
              </div>
              <div className="grid grid-cols-2 gap-3 pt-2">
                <div className={`rounded-lg p-3 border ${rep.is_gaming_comp ? "bg-red-900/30 border-red-700/40" : "bg-slate-800/50 border-slate-700/40"}`}>
                  <p className="text-xs text-slate-500">Gaming Comp</p>
                  <p className={`text-sm font-semibold mt-0.5 ${rep.is_gaming_comp ? "text-red-400" : "text-emerald-400"}`}>
                    {rep.is_gaming_comp ? "Yes — Flagged" : "No"}
                  </p>
                </div>
                <div className={`rounded-lg p-3 border ${rep.needs_comp_review ? "bg-amber-900/30 border-amber-700/40" : "bg-slate-800/50 border-slate-700/40"}`}>
                  <p className="text-xs text-slate-500">Comp Review</p>
                  <p className={`text-sm font-semibold mt-0.5 ${rep.needs_comp_review ? "text-amber-400" : "text-emerald-400"}`}>
                    {rep.needs_comp_review ? "Required" : "Not needed"}
                  </p>
                </div>
              </div>
            </div>
          )}

          {tab === "attainment" && (
            <div className="space-y-4">
              <div className="grid grid-cols-3 gap-3">
                {[rep.quota_attainment_q1, rep.quota_attainment_q2, rep.quota_attainment_q3].map((v, i) => (
                  <div key={i} className={`rounded-lg p-3 border text-center ${
                    v >= 100 ? "bg-emerald-900/30 border-emerald-700/40" :
                    v >= 80  ? "bg-amber-900/30 border-amber-700/40" :
                    "bg-red-900/30 border-red-700/40"
                  }`}>
                    <p className="text-xs text-slate-500">Q{i + 1}</p>
                    <p className={`text-xl font-bold mt-1 ${v >= 100 ? "text-emerald-400" : v >= 80 ? "text-amber-400" : "text-red-400"}`}>
                      {v.toFixed(0)}%
                    </p>
                  </div>
                ))}
              </div>
              <div className="space-y-3">
                {scoreBar("Sandbagging Score (higher = worse)", rep.sandbagging_score, true)}
                {scoreBar("Spiff Dependency Score (higher = worse)", rep.spiff_dependency_score, true)}
                {scoreBar("Discount Behavior Score (higher = worse)", rep.discount_behavior_score, true)}
              </div>
              <div className="bg-slate-800/50 rounded-lg p-3 border border-slate-700/40 space-y-2">
                <div className="flex justify-between text-sm">
                  <span className="text-slate-400">Gaming Pattern</span>
                  <span className={`font-semibold capitalize ${PATTERN_COLOR[rep.gaming_pattern]}`}>{rep.gaming_pattern.replace("_", " ")}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-slate-400">Incentive Alignment</span>
                  <span className="text-white font-medium capitalize">{rep.incentive_alignment.replace("_", " ")}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-slate-400">Avg Discount Given</span>
                  <span className="text-white font-medium">{rep.avg_discount_pct.toFixed(1)}%</span>
                </div>
              </div>
            </div>
          )}

          {tab === "actions" && (
            <div className="space-y-3">
              <div className={`rounded-lg p-4 border ${ACTION_COLOR[rep.comp_action]}`}>
                <p className="text-xs font-semibold uppercase tracking-wider opacity-70 mb-1">Recommended Action</p>
                <p className="text-lg font-bold capitalize">{rep.comp_action.replace("_", " ")}</p>
              </div>
              {rep.comp_action === "immediate_review" && (
                <ul className="space-y-2 text-sm text-slate-300">
                  <li className="flex gap-2"><span className="text-red-400">•</span> Schedule comp review meeting with manager and HR immediately</li>
                  <li className="flex gap-2"><span className="text-red-400">•</span> Audit deal timing and spiff-driven close patterns</li>
                  <li className="flex gap-2"><span className="text-red-400">•</span> Review quota accuracy for next planning cycle</li>
                  <li className="flex gap-2"><span className="text-red-400">•</span> Evaluate pipeline sandbag disclosures</li>
                </ul>
              )}
              {rep.comp_action === "restructure" && (
                <ul className="space-y-2 text-sm text-slate-300">
                  <li className="flex gap-2"><span className="text-orange-400">•</span> Redesign comp plan to remove gaming incentives</li>
                  <li className="flex gap-2"><span className="text-orange-400">•</span> Add discount approval gates to control margin erosion</li>
                  <li className="flex gap-2"><span className="text-orange-400">•</span> Introduce balanced KPIs beyond pure revenue</li>
                </ul>
              )}
              {rep.comp_action === "monitor" && (
                <ul className="space-y-2 text-sm text-slate-300">
                  <li className="flex gap-2"><span className="text-amber-400">•</span> Monitor deal timing and close patterns weekly</li>
                  <li className="flex gap-2"><span className="text-amber-400">•</span> Review spiff participation rates next quarter</li>
                  <li className="flex gap-2"><span className="text-amber-400">•</span> Validate pipeline values against historical accuracy</li>
                </ul>
              )}
              {rep.comp_action === "maintain" && (
                <ul className="space-y-2 text-sm text-slate-300">
                  <li className="flex gap-2"><span className="text-emerald-400">•</span> Current comp structure is working well — maintain</li>
                  <li className="flex gap-2"><span className="text-emerald-400">•</span> Use this rep as a benchmark for comp plan design</li>
                  <li className="flex gap-2"><span className="text-emerald-400">•</span> Consider retention incentives to lock in top performer</li>
                </ul>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

// ── RepCard ───────────────────────────────────────────────────────────────────

function RepCard({ rep, onClick }: { rep: RepData; onClick: () => void }) {
  return (
    <div
      onClick={onClick}
      className={`rounded-xl border p-4 cursor-pointer hover:border-slate-600 transition-all ${RISK_BG[rep.comp_risk_level]}`}
    >
      <div className="flex items-start justify-between gap-2 mb-3">
        <div>
          <p className="text-white font-semibold text-sm">{rep.rep_name}</p>
          <p className="text-slate-500 text-xs">{rep.region}</p>
        </div>
        <div className="flex flex-col items-end gap-1">
          <span className={`text-xs font-bold uppercase ${RISK_COLOR[rep.comp_risk_level]}`}>
            {rep.comp_risk_level}
          </span>
          <span className={`text-xs capitalize ${PATTERN_COLOR[rep.gaming_pattern]}`}>
            {rep.gaming_pattern.replace("_", " ")}
          </span>
        </div>
      </div>

      <div className="flex items-center justify-between mb-3">
        <CompEfficiencyMeter score={rep.compensation_efficiency_score} risk={rep.comp_risk_level} />
        <div className="space-y-1 flex-1 ml-3">
          <div className="flex justify-between text-xs">
            <span className="text-slate-500">Sandbagging</span>
            <span className={rep.sandbagging_score >= 55 ? "text-red-400" : "text-slate-400"}>
              {rep.sandbagging_score.toFixed(0)}
            </span>
          </div>
          <div className="flex justify-between text-xs">
            <span className="text-slate-500">Spiff Dep.</span>
            <span className={rep.spiff_dependency_score >= 65 ? "text-orange-400" : "text-slate-400"}>
              {rep.spiff_dependency_score.toFixed(0)}
            </span>
          </div>
          <div className="flex justify-between text-xs">
            <span className="text-slate-500">Discount</span>
            <span className={rep.discount_behavior_score >= 60 ? "text-rose-400" : "text-slate-400"}>
              {rep.discount_behavior_score.toFixed(0)}
            </span>
          </div>
        </div>
      </div>

      <div className="flex items-center justify-between">
        <span className={`text-xs px-2 py-0.5 rounded-full border ${ACTION_COLOR[rep.comp_action]}`}>
          {rep.comp_action.replace("_", " ")}
        </span>
        {rep.estimated_overcompensation > 0 && (
          <span className="text-xs text-red-400 font-medium">
            Overpay {fmt$(rep.estimated_overcompensation)}
          </span>
        )}
        {rep.is_gaming_comp && (
          <span className="text-xs text-red-500 font-bold">⚠ Gaming</span>
        )}
      </div>
    </div>
  );
}

// ── Page ──────────────────────────────────────────────────────────────────────

export default function SalesCompIntelPage() {
  const [data, setData] = useState<{ reps: RepData[]; summary: Summary } | null>(null);
  const [loading, setLoading] = useState(true);
  const [selectedRep, setSelectedRep] = useState<RepData | null>(null);
  const [filterRisk, setFilterRisk] = useState("all");
  const [filterPattern, setFilterPattern] = useState("all");
  const [filterRegion, setFilterRegion] = useState("all");

  useEffect(() => {
    async function fetchData() {
        setLoading(true);
        try {
          const params = new URLSearchParams();
          if (filterRisk !== "all")    params.set("risk", filterRisk);
          if (filterPattern !== "all") params.set("pattern", filterPattern);
          if (filterRegion !== "all")  params.set("region", filterRegion);
          const res = await fetch(`/api/sales-compensation-intelligence?${params}`);
          if (res.ok) setData(await res.json());
        } catch {}
        setLoading(false);
  }
    fetchData();
  }, [filterRisk, filterPattern, filterRegion]);

  const s = data?.summary;
  const riskOrder = ["critical", "high", "moderate", "low"];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
      <div className="max-w-7xl mx-auto space-y-6">

        {/* Header */}
        <div>
          <h1 className="text-2xl font-bold text-white">Sales Compensation Intelligence</h1>
          <p className="text-slate-400 text-sm mt-1">Detect comp gaming, sandbagging, and incentive misalignment across your sales team</p>
        </div>

        {/* KPI Strip */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {[
            { label: "Total Reps Analyzed", value: s?.total ?? "—", sub: "in scope" },
            { label: "Gaming Comp", value: s?.gaming_count ?? "—", sub: "flagged reps", danger: (s?.gaming_count ?? 0) > 0 },
            { label: "Reviews Required", value: s?.review_needed_count ?? "—", sub: "immediate action", warn: (s?.review_needed_count ?? 0) > 0 },
            { label: "Est. Overcompensation", value: s ? fmt$(s.total_estimated_overcompensation) : "—", sub: "recoverable", danger: (s?.total_estimated_overcompensation ?? 0) > 0 },
          ].map((k) => (
            <div key={k.label} className="bg-slate-900 border border-slate-800 rounded-xl p-4">
              <p className="text-slate-500 text-xs">{k.label}</p>
              <p className={`text-2xl font-bold mt-1 ${k.danger ? "text-red-400" : k.warn ? "text-amber-400" : "text-white"}`}>
                {k.value}
              </p>
              <p className="text-slate-600 text-xs mt-0.5">{k.sub}</p>
            </div>
          ))}
        </div>

        {/* Averages row */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {[
            { label: "Avg Comp Efficiency", value: s?.avg_compensation_efficiency_score.toFixed(1) ?? "—", suffix: "" },
            { label: "Avg Sandbagging Score", value: s?.avg_sandbagging_score.toFixed(1) ?? "—", suffix: "" },
            { label: "Avg Spiff Dependency", value: s?.avg_spiff_dependency_score.toFixed(1) ?? "—", suffix: "" },
            { label: "Avg Quota Accuracy", value: s?.avg_quota_accuracy_score.toFixed(1) ?? "—", suffix: "" },
          ].map((k) => (
            <div key={k.label} className="bg-slate-900 border border-slate-800 rounded-xl p-4">
              <p className="text-slate-500 text-xs">{k.label}</p>
              <p className="text-xl font-bold text-white mt-1">{k.value}{k.suffix}</p>
            </div>
          ))}
        </div>

        {/* Pattern Distribution */}
        {s && (
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
            <h2 className="text-sm font-semibold text-slate-300 mb-3">Gaming Pattern Distribution</h2>
            <GamingPatternBar counts={s.pattern_counts} />
          </div>
        )}

        {/* Filters */}
        <div className="flex flex-wrap gap-3">
          <div className="flex gap-1 bg-slate-900 border border-slate-800 rounded-lg p-1">
            {["all", "low", "moderate", "high", "critical"].map((v) => (
              <button
                key={v}
                onClick={() => setFilterRisk(v)}
                className={`px-3 py-1 rounded text-xs font-medium transition-colors capitalize ${filterRisk === v ? "bg-indigo-600 text-white" : "text-slate-400 hover:text-white"}`}
              >
                {v === "all" ? "All Risks" : v}
              </button>
            ))}
          </div>
          <div className="flex gap-1 bg-slate-900 border border-slate-800 rounded-lg p-1">
            {["all", "clean", "sandbagging", "spiff_chasing", "discount_heavy", "mixed"].map((v) => (
              <button
                key={v}
                onClick={() => setFilterPattern(v)}
                className={`px-3 py-1 rounded text-xs font-medium transition-colors ${filterPattern === v ? "bg-indigo-600 text-white" : "text-slate-400 hover:text-white"}`}
              >
                {v === "all" ? "All Patterns" : v.replace("_", " ")}
              </button>
            ))}
          </div>
          <div className="flex gap-1 bg-slate-900 border border-slate-800 rounded-lg p-1">
            {["all", "NAMER", "EMEA", "APAC", "LATAM"].map((v) => (
              <button
                key={v}
                onClick={() => setFilterRegion(v)}
                className={`px-3 py-1 rounded text-xs font-medium transition-colors ${filterRegion === v ? "bg-indigo-600 text-white" : "text-slate-400 hover:text-white"}`}
              >
                {v === "all" ? "All Regions" : v}
              </button>
            ))}
          </div>
        </div>

        {/* Rep grid */}
        {loading ? (
          <div className="text-center py-12 text-slate-500">Loading compensation intelligence...</div>
        ) : (
          <>
            {/* Critical + High banner */}
            {data && data.reps.filter((r) => r.comp_risk_level === "critical" || r.comp_risk_level === "high").length > 0 && (
              <div className="bg-red-950/40 border border-red-800/50 rounded-xl p-4 flex items-center gap-3">
                <span className="text-red-400 text-xl">⚠</span>
                <p className="text-red-300 text-sm font-medium">
                  {data.reps.filter((r) => r.comp_risk_level === "critical" || r.comp_risk_level === "high").length} rep(s) show high/critical comp risk — immediate review recommended.
                </p>
              </div>
            )}
            {/* Cards sorted by risk */}
            <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
              {data?.reps
                .slice()
                .sort((a, b) => riskOrder.indexOf(a.comp_risk_level) - riskOrder.indexOf(b.comp_risk_level))
                .map((rep) => (
                  <RepCard key={rep.rep_id} rep={rep} onClick={() => setSelectedRep(rep)} />
                ))}
            </div>
            {data?.reps.length === 0 && (
              <p className="text-center text-slate-500 py-8">No reps match current filters.</p>
            )}
          </>
        )}
      </div>

      {selectedRep && <RepModal rep={selectedRep} onClose={() => setSelectedRep(null)} />}
    </div>
  );
}
