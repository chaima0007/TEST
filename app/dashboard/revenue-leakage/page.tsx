"use client";

import { useEffect, useState, useCallback } from "react";

// ── types ─────────────────────────────────────────────────────────────────────

interface Rep {
  rep_id: string;
  rep_name: string;
  region: string;
  segment: string;
  leakage_category: string;
  leakage_risk: string;
  leakage_pattern: string;
  leakage_action: string;
  discount_leakage_score: number;
  process_leakage_score: number;
  champion_leakage_score: number;
  expansion_leakage_score: number;
  total_leakage_score: number;
  estimated_lost_revenue: number;
  recovery_potential: number;
  is_high_risk: boolean;
  needs_attention: boolean;
  total_deals: number;
  avg_deal_size: number;
}

interface Summary {
  total: number;
  category_counts: Record<string, number>;
  risk_counts: Record<string, number>;
  pattern_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_discount_leakage_score: number;
  avg_total_leakage_score: number;
  total_estimated_lost_revenue: number;
  high_risk_count: number;
  coaching_count: number;
  avg_recovery_potential: number;
  total_pipeline_value_at_risk: number;
  avg_process_leakage_score: number;
}

// ── helpers ───────────────────────────────────────────────────────────────────

const CATEGORY_COLOR: Record<string, string> = {
  minimal:     "text-green-400",
  moderate:    "text-yellow-400",
  significant: "text-orange-400",
  critical:    "text-red-400",
};

const CATEGORY_BG: Record<string, string> = {
  minimal:     "bg-green-500/20 border-green-500/40",
  moderate:    "bg-yellow-500/20 border-yellow-500/40",
  significant: "bg-orange-500/20 border-orange-500/40",
  critical:    "bg-red-500/20 border-red-500/40",
};

const CATEGORY_BAR: Record<string, string> = {
  minimal:     "bg-green-500",
  moderate:    "bg-yellow-500",
  significant: "bg-orange-500",
  critical:    "bg-red-500",
};

const ACTION_COLOR: Record<string, string> = {
  monitor:             "bg-slate-500/20 text-slate-300 border-slate-500/30",
  pricing_review:      "bg-amber-500/20 text-amber-300 border-amber-500/30",
  champion_coaching:   "bg-sky-500/20 text-sky-300 border-sky-500/30",
  deal_structuring:    "bg-indigo-500/20 text-indigo-300 border-indigo-500/30",
  urgent_intervention: "bg-red-500/20 text-red-300 border-red-500/30",
};

const PATTERN_COLOR: Record<string, string> = {
  discount_heavy:    "text-amber-400",
  late_stage_loss:   "text-orange-400",
  champion_deficit:  "text-sky-400",
  multiyear_miss:    "text-violet-400",
  mixed:             "text-slate-400",
};

function fmt(label: string) {
  return label.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
}

function fmtMoney(n: number) {
  if (n >= 1_000_000) return `$${(n / 1_000_000).toFixed(1)}M`;
  if (n >= 1_000) return `$${Math.round(n / 1_000)}k`;
  return `$${n}`;
}

// ── LeakageGauge SVG ──────────────────────────────────────────────────────────

function LeakageGauge({ score, label }: { score: number; label: string }) {
  const r = 30;
  const cx = 38;
  const cy = 38;
  const circ = 2 * Math.PI * r;
  const filled = (score / 100) * circ;
  const color =
    score >= 65 ? "#ef4444" :
    score >= 45 ? "#f97316" :
    score >= 25 ? "#eab308" : "#22c55e";

  return (
    <div className="flex flex-col items-center gap-1">
      <svg width="76" height="76" viewBox="0 0 76 76">
        <circle cx={cx} cy={cy} r={r} fill="none" stroke="#1e293b" strokeWidth="6" />
        <circle
          cx={cx} cy={cy} r={r}
          fill="none"
          stroke={color}
          strokeWidth="6"
          strokeDasharray={`${filled} ${circ - filled}`}
          strokeDashoffset={circ / 4}
          strokeLinecap="round"
        />
        <text x={cx} y={cy + 5} textAnchor="middle" fill="white" fontSize="13" fontWeight="bold">
          {Math.round(score)}
        </text>
      </svg>
      <span className="text-xs text-slate-400 text-center">{label}</span>
    </div>
  );
}

// ── CategoryDistBar ───────────────────────────────────────────────────────────

function CategoryDistBar({ counts, total }: { counts: Record<string, number>; total: number }) {
  const order = ["minimal", "moderate", "significant", "critical"];
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

// ── LeakageModal ──────────────────────────────────────────────────────────────

function LeakageModal({ rep, onClose }: { rep: Rep; onClose: () => void }) {
  const [tab, setTab] = useState<"leakage" | "revenue" | "actions">("leakage");

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
        {/* Header */}
        <div className="p-6 border-b border-slate-800 flex items-start justify-between gap-4">
          <div>
            <div className="flex items-center gap-3 flex-wrap">
              <h2 className="text-xl font-bold text-slate-100">{rep.rep_name}</h2>
              <span className={`text-xs font-semibold px-2.5 py-0.5 rounded-full border ${ACTION_COLOR[rep.leakage_action]}`}>
                {fmt(rep.leakage_action)}
              </span>
              {rep.is_high_risk && (
                <span className="text-xs font-semibold px-2.5 py-0.5 rounded-full bg-red-500/20 text-red-300 border border-red-500/30">
                  High Risk
                </span>
              )}
            </div>
            <p className="text-sm text-slate-400 mt-1">
              <span className={`font-semibold ${CATEGORY_COLOR[rep.leakage_category]}`}>{fmt(rep.leakage_category)} Leakage</span>
              {" · "}{rep.region}{" · "}{fmt(rep.segment)}
            </p>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-slate-300 text-xl leading-none">✕</button>
        </div>

        {/* Tabs */}
        <div className="flex gap-0 border-b border-slate-800">
          {(["leakage", "revenue", "actions"] as const).map((t) => (
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
          {tab === "leakage" && (
            <div className="space-y-5">
              <div className="flex justify-around">
                <LeakageGauge score={rep.discount_leakage_score} label="Discount" />
                <LeakageGauge score={rep.process_leakage_score} label="Process" />
                <LeakageGauge score={rep.champion_leakage_score} label="Champion" />
                <LeakageGauge score={rep.expansion_leakage_score} label="Expansion" />
              </div>
              <div className="text-center">
                <div className="text-4xl font-bold text-white">{rep.total_leakage_score}</div>
                <div className="text-sm text-slate-400">Total Leakage Score</div>
              </div>
              <div>
                <div className="flex justify-between text-xs text-slate-400 mb-1">
                  <span>Primary Pattern</span>
                  <span className={PATTERN_COLOR[rep.leakage_pattern]}>{fmt(rep.leakage_pattern)}</span>
                </div>
              </div>
              <div>
                <div className="flex justify-between text-xs text-slate-400 mb-1">
                  <span>Recovery Potential</span>
                  <span className="text-emerald-400">{rep.recovery_potential}%</span>
                </div>
                <div className="w-full bg-slate-700/50 rounded-full h-2">
                  <div
                    className="h-2 rounded-full bg-emerald-500 transition-all"
                    style={{ width: `${Math.min(rep.recovery_potential, 100)}%` }}
                  />
                </div>
              </div>
            </div>
          )}

          {tab === "revenue" && (
            <div className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                {[
                  { label: "Est. Lost Revenue", value: fmtMoney(rep.estimated_lost_revenue), color: "text-red-400" },
                  { label: "Recovery Potential", value: `${rep.recovery_potential}%`, color: "text-emerald-400" },
                  { label: "Total Deals", value: rep.total_deals },
                  { label: "Avg Deal Size", value: fmtMoney(rep.avg_deal_size) },
                  { label: "Region", value: rep.region },
                  { label: "Segment", value: fmt(rep.segment) },
                  { label: "Risk Level", value: fmt(rep.leakage_risk) },
                  { label: "Needs Attention", value: rep.needs_attention ? "Yes" : "No" },
                ].map(({ label, value, color }) => (
                  <div key={label} className="bg-slate-800/60 rounded-xl p-3">
                    <div className="text-xs text-slate-400 mb-1">{label}</div>
                    <div className={`text-base font-semibold ${color ?? "text-slate-100"}`}>{value}</div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {tab === "actions" && (
            <div className="space-y-4">
              <div className={`p-4 rounded-xl border ${CATEGORY_BG[rep.leakage_category]}`}>
                <div className={`text-sm font-semibold ${CATEGORY_COLOR[rep.leakage_category]} mb-1`}>
                  {fmt(rep.leakage_category)} Leakage — {fmt(rep.leakage_pattern)}
                </div>
                <div className="text-xs text-slate-400">
                  {rep.leakage_category === "critical" && "Critical revenue leakage detected — immediate management review required."}
                  {rep.leakage_category === "significant" && "Significant leakage pattern identified — targeted coaching recommended."}
                  {rep.leakage_category === "moderate" && "Moderate leakage — focus on top 2 dimensions for quick wins."}
                  {rep.leakage_category === "minimal" && "Leakage is well controlled — maintain current practices."}
                </div>
              </div>
              <div className="space-y-3">
                {[
                  rep.leakage_action === "urgent_intervention" && { label: "Executive Review Session", desc: "Immediate 1:1 with CRO to review deal losses and discount patterns" },
                  rep.leakage_action === "pricing_review" && { label: "Discount Authority Audit", desc: "Review and cap discount authority; introduce value-based pricing training" },
                  rep.leakage_action === "champion_coaching" && { label: "Champion Building Workshop", desc: "Coach on identifying, nurturing, and mobilising internal champions" },
                  rep.leakage_action === "deal_structuring" && { label: "Deal Structure Review", desc: "Introduce multiyear packaging and late-stage recovery playbook" },
                  rep.leakage_action === "monitor" && { label: "Quarterly Health Check", desc: "Monitor leakage trends and trigger intervention if scores rise" },
                  rep.recovery_potential >= 50 && { label: "Recovery Pipeline", desc: `${fmtMoney(Math.round(rep.estimated_lost_revenue * rep.recovery_potential / 100))} recoverable with focused intervention` },
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
          <p className="text-xs text-slate-400 mt-0.5">
            {rep.region} · {fmt(rep.segment)}
          </p>
        </div>
        <div className="flex flex-col items-end gap-1.5 shrink-0">
          <span className={`text-xs font-semibold px-2 py-0.5 rounded-full border ${ACTION_COLOR[rep.leakage_action]}`}>
            {fmt(rep.leakage_action)}
          </span>
          {rep.is_high_risk && (
            <span className="text-xs px-2 py-0.5 rounded-full bg-red-500/20 text-red-300 border border-red-500/30">
              ⚠ High Risk
            </span>
          )}
        </div>
      </div>

      {/* Leakage score pills */}
      <div className="flex gap-2 mb-3 flex-wrap">
        {[
          { label: "Discount", value: rep.discount_leakage_score, color: "text-amber-400" },
          { label: "Process", value: rep.process_leakage_score, color: "text-orange-400" },
          { label: "Champion", value: rep.champion_leakage_score, color: "text-sky-400" },
        ].map(({ label, value, color }) => (
          <div key={label} className="flex flex-col items-center bg-slate-900/60 rounded-lg px-3 py-1.5">
            <span className={`text-sm font-bold ${color}`}>{Math.round(value)}</span>
            <span className="text-xs text-slate-500">{label}</span>
          </div>
        ))}
        <div className="flex flex-col items-center bg-slate-900/60 rounded-lg px-3 py-1.5">
          <span className={`text-sm font-bold ${CATEGORY_COLOR[rep.leakage_category]}`}>{rep.total_leakage_score}</span>
          <span className="text-xs text-slate-500">Total</span>
        </div>
      </div>

      <div className="flex justify-between items-center text-xs text-slate-400">
        <span className="text-red-400">{fmtMoney(rep.estimated_lost_revenue)} lost</span>
        <span className={PATTERN_COLOR[rep.leakage_pattern]}>{fmt(rep.leakage_pattern)}</span>
        <span className="text-emerald-400">{rep.recovery_potential}% recoverable</span>
      </div>
    </button>
  );
}

// ── Page ──────────────────────────────────────────────────────────────────────

export default function RevenueLeakagePage() {
  const [reps, setReps] = useState<Rep[]>([]);
  const [summary, setSummary] = useState<Summary | null>(null);
  const [loading, setLoading] = useState(true);
  const [selected, setSelected] = useState<Rep | null>(null);
  const [filterCategory, setFilterCategory] = useState("all");
  const [filterRisk, setFilterRisk] = useState("all");

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const params = new URLSearchParams();
      if (filterCategory !== "all") params.set("category", filterCategory);
      if (filterRisk     !== "all") params.set("risk", filterRisk);
      const res = await fetch(`/api/revenue-leakage?${params}`);
      const data = await res.json();
      setReps(data.reps ?? []);
      setSummary(data.summary ?? null);
    } finally {
      setLoading(false);
    }
  }, [filterCategory, filterRisk]);

  useEffect(() => { load(); }, [load]);

  const categories = ["all", "minimal", "moderate", "significant", "critical"];
  const risks = ["all", "low", "medium", "high", "critical"];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
      {selected && (
        <LeakageModal rep={selected} onClose={() => setSelected(null)} />
      )}

      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-white">Revenue Leakage</h1>
        <p className="text-slate-400 mt-1">Detect and quantify hidden revenue loss across discounting, process gaps, and champion deficits</p>
      </div>

      {/* KPI Strip */}
      {summary && (
        <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-7 gap-4 mb-8">
          {[
            { label: "Total Reps", value: summary.total },
            { label: "High Risk", value: summary.high_risk_count, color: "text-red-400" },
            { label: "Need Coaching", value: summary.coaching_count, color: "text-orange-400" },
            { label: "Est. Lost Revenue", value: fmtMoney(summary.total_estimated_lost_revenue), color: "text-red-400" },
            { label: "Avg Leakage Score", value: summary.avg_total_leakage_score },
            { label: "Avg Discount Score", value: summary.avg_discount_leakage_score, color: "text-amber-400" },
            { label: "Avg Recovery", value: `${summary.avg_recovery_potential}%`, color: "text-emerald-400" },
          ].map(({ label, value, color }) => (
            <div key={label} className="bg-slate-800/60 border border-slate-700/50 rounded-2xl p-4">
              <div className="text-xs text-slate-400 mb-1">{label}</div>
              <div className={`text-2xl font-bold ${color ?? "text-white"}`}>{value}</div>
            </div>
          ))}
        </div>
      )}

      {/* Category distribution */}
      {summary && (
        <div className="bg-slate-800/60 border border-slate-700/50 rounded-2xl p-5 mb-8">
          <div className="flex items-center justify-between mb-3">
            <h2 className="text-sm font-semibold text-slate-300">Leakage Category Distribution</h2>
            <div className="flex gap-3 flex-wrap">
              {["minimal", "moderate", "significant", "critical"].map((k) => (
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
              <div className="text-lg font-bold text-red-400">{fmtMoney(summary.total_estimated_lost_revenue)}</div>
              <div className="text-xs text-slate-400">Total Est. Lost</div>
            </div>
            <div>
              <div className="text-lg font-bold text-slate-300">{summary.avg_process_leakage_score}</div>
              <div className="text-xs text-slate-400">Avg Process Score</div>
            </div>
            <div>
              <div className="text-lg font-bold text-emerald-400">{summary.avg_recovery_potential}%</div>
              <div className="text-xs text-slate-400">Avg Recovery</div>
            </div>
          </div>
        </div>
      )}

      {/* Filters */}
      <div className="flex flex-wrap gap-3 mb-6">
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
      </div>

      {/* Rep Grid */}
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
