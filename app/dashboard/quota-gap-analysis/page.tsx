"use client";

import { useEffect, useState } from "react";

// ── Types ────────────────────────────────────────────────────────────────────

interface Rep {
  rep_id: string;
  rep_name: string;
  manager_id: string;
  region: string;
  segment: string;
  period_quota: number;
  effective_quota: number;
  closed_won_value: number;
  pipeline_value: number;
  late_stage_value: number;
  gap_to_quota: number;
  attainment_pct: number;
  attainment_tier: string;
  projected_attainment: number;
  gap_risk: string;
  pipeline_coverage: string;
  recommended_action: string;
  required_win_rate: number;
  deals_needed: number;
  quota_achievement_score: number;
  pipeline_health_score: number;
  is_at_risk: boolean;
  days_remaining: number;
  deals_in_pipeline: number;
  avg_deal_size: number;
  win_rate: number;
  is_ramping: boolean;
}

interface Summary {
  total: number;
  tier_counts: Record<string, number>;
  risk_counts: Record<string, number>;
  action_counts: Record<string, number>;
  coverage_counts: Record<string, number>;
  avg_attainment_pct: number;
  avg_projected_attainment: number;
  avg_achievement_score: number;
  avg_pipeline_health_score: number;
  total_gap: number;
  at_risk_count: number;
  overachiever_count: number;
  critical_count: number;
}

// ── Helpers ──────────────────────────────────────────────────────────────────

function tierColor(tier: string) {
  return (
    {
      overachiever: "text-emerald-400",
      on_track:     "text-blue-400",
      at_risk:      "text-amber-400",
      behind:       "text-orange-400",
      critical:     "text-red-400",
    }[tier] ?? "text-slate-400"
  );
}

function tierBg(tier: string) {
  return (
    {
      overachiever: "bg-emerald-900/30 border-emerald-700/50",
      on_track:     "bg-blue-900/30 border-blue-700/50",
      at_risk:      "bg-amber-900/30 border-amber-700/50",
      behind:       "bg-orange-900/30 border-orange-700/50",
      critical:     "bg-red-900/30 border-red-700/50",
    }[tier] ?? "bg-slate-800 border-slate-700"
  );
}

function riskBadge(risk: string) {
  const map: Record<string, string> = {
    low:      "bg-emerald-900/50 text-emerald-300 border border-emerald-700/50",
    medium:   "bg-amber-900/50 text-amber-300 border border-amber-700/50",
    high:     "bg-orange-900/50 text-orange-300 border border-orange-700/50",
    critical: "bg-red-900/50 text-red-300 border border-red-700/50",
  };
  return map[risk] ?? "bg-slate-700 text-slate-300";
}

function actionBadge(action: string) {
  const map: Record<string, string> = {
    celebrate_and_expand:   "bg-emerald-900/50 text-emerald-300 border border-emerald-700/50",
    maintain_pace:          "bg-blue-900/50 text-blue-300 border border-blue-700/50",
    accelerate_pipeline:    "bg-violet-900/50 text-violet-300 border border-violet-700/50",
    focus_late_stage:       "bg-indigo-900/50 text-indigo-300 border border-indigo-700/50",
    build_pipeline:         "bg-amber-900/50 text-amber-300 border border-amber-700/50",
    executive_intervention: "bg-red-900/50 text-red-300 border border-red-700/50",
  };
  return map[action] ?? "bg-slate-700 text-slate-300";
}

function fmtLabel(s: string) {
  return s.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
}

function fmtMoney(n: number) {
  if (n >= 1_000_000) return `${(n / 1_000_000).toFixed(1)}M€`;
  if (n >= 1_000)     return `${(n / 1_000).toFixed(0)}k€`;
  return `${n.toFixed(0)}€`;
}

// ── Attainment Ring ───────────────────────────────────────────────────────────

function AttainmentRing({ pct, size = 52 }: { pct: number; size?: number }) {
  const cx   = size / 2;
  const cy   = size / 2;
  const r    = size * 0.38;
  const circ = 2 * Math.PI * r;
  const arc  = Math.min(1, pct / 100) * circ;
  const color =
    pct >= 110 ? "#34d399" :
    pct >= 90  ? "#60a5fa" :
    pct >= 70  ? "#fbbf24" :
    pct >= 50  ? "#f97316" : "#f87171";

  return (
    <svg width={size} height={size} className="flex-shrink-0">
      <circle cx={cx} cy={cy} r={r} stroke="#1e293b" strokeWidth={size * 0.12} fill="none" />
      <circle
        cx={cx} cy={cy} r={r}
        stroke={color} strokeWidth={size * 0.12} fill="none"
        strokeDasharray={`${arc} ${circ - arc}`}
        strokeLinecap="round"
        transform={`rotate(-90 ${cx} ${cy})`}
      />
      <text x={cx} y={cy + 1} textAnchor="middle" dominantBaseline="middle"
        fill={color} fontSize={size * 0.2} fontWeight="700">
        {Math.round(pct)}%
      </text>
    </svg>
  );
}

// ── Tier Distribution Bar ─────────────────────────────────────────────────────

function TierDistBar({ counts }: { counts: Record<string, number> }) {
  const total = Object.values(counts).reduce((s, n) => s + n, 0);
  if (total === 0) return null;
  const order  = ["overachiever", "on_track", "at_risk", "behind", "critical"];
  const colors: Record<string, string> = {
    overachiever: "bg-emerald-500",
    on_track:     "bg-blue-500",
    at_risk:      "bg-amber-500",
    behind:       "bg-orange-500",
    critical:     "bg-red-500",
  };
  const entries = order.filter((k) => counts[k] != null).map((k) => [k, counts[k]] as [string, number]);

  return (
    <div className="space-y-1.5">
      <div className="flex h-2.5 rounded-full overflow-hidden gap-px">
        {entries.map(([k, v]) => (
          <div
            key={k}
            className={`${colors[k]} transition-all`}
            style={{ width: `${(v / total) * 100}%` }}
          />
        ))}
      </div>
      <div className="flex flex-wrap gap-x-3 gap-y-1">
        {entries.map(([k, v]) => (
          <span key={k} className="flex items-center gap-1 text-xs text-slate-400">
            <span className={`w-2 h-2 rounded-full ${colors[k]}`} />
            {fmtLabel(k)} <span className="text-slate-300 font-medium">{v}</span>
          </span>
        ))}
      </div>
    </div>
  );
}

// ── Rep Modal ─────────────────────────────────────────────────────────────────

function RepModal({ rep, onClose }: { rep: Rep; onClose: () => void }) {
  const [tab, setTab] = useState<"gap" | "pipeline" | "metrics">("gap");

  useEffect(() => {
    const fn = (e: KeyboardEvent) => e.key === "Escape" && onClose();
    document.addEventListener("keydown", fn);
    return () => document.removeEventListener("keydown", fn);
  }, [onClose]);

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4"
      onClick={onClose}
    >
      <div
        className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-xl max-h-[90vh] overflow-y-auto shadow-2xl"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="p-5 border-b border-slate-800">
          <div className="flex items-start justify-between gap-3">
            <div className="flex-1 min-w-0">
              <div className="flex items-center gap-2 flex-wrap">
                <h2 className="text-slate-100 font-bold text-lg">{rep.rep_name}</h2>
                {rep.is_ramping && (
                  <span className="px-1.5 py-0.5 bg-violet-900/50 text-violet-300 border border-violet-700/50 rounded text-xs font-medium">
                    Ramping
                  </span>
                )}
                {rep.is_at_risk && (
                  <span className="px-1.5 py-0.5 bg-red-900/50 text-red-300 border border-red-700/50 rounded text-xs font-medium">
                    At Risk
                  </span>
                )}
              </div>
              <p className="text-slate-400 text-sm mt-0.5">{fmtLabel(rep.region)} · {fmtLabel(rep.segment)} · {rep.days_remaining}d left</p>
            </div>
            <button onClick={onClose} className="text-slate-500 hover:text-slate-300 text-xl leading-none flex-shrink-0">✕</button>
          </div>
          <div className="flex items-center gap-2 mt-3 flex-wrap">
            <span className={`px-2 py-0.5 rounded text-xs font-medium ${riskBadge(rep.gap_risk)}`}>
              {fmtLabel(rep.gap_risk)} risk
            </span>
            <span className={`px-2 py-0.5 rounded text-xs font-medium ${actionBadge(rep.recommended_action)}`}>
              {fmtLabel(rep.recommended_action)}
            </span>
          </div>
        </div>

        {/* KPIs */}
        <div className="grid grid-cols-3 gap-px bg-slate-800 border-b border-slate-800">
          {[
            ["Attainment",  `${rep.attainment_pct}%`],
            ["Projected",   `${rep.projected_attainment}%`],
            ["Gap",         rep.gap_to_quota > 0 ? fmtMoney(rep.gap_to_quota) : "✓ Done"],
          ].map(([label, val]) => (
            <div key={label} className="bg-slate-900 px-4 py-3 text-center">
              <div className="text-slate-400 text-xs">{label}</div>
              <div className={`font-bold text-base ${label === "Gap" && rep.gap_to_quota === 0 ? "text-emerald-400" : "text-slate-100"}`}>{val}</div>
            </div>
          ))}
        </div>

        {/* Tabs */}
        <div className="flex border-b border-slate-800">
          {(["gap", "pipeline", "metrics"] as const).map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`flex-1 py-2.5 text-sm font-medium transition-colors ${
                tab === t
                  ? "text-indigo-400 border-b-2 border-indigo-500"
                  : "text-slate-500 hover:text-slate-300"
              }`}
            >
              {t === "gap" ? "Gap Analysis" : t === "pipeline" ? "Pipeline" : "Metrics"}
            </button>
          ))}
        </div>

        <div className="p-5 space-y-3">
          {tab === "gap" && (
            <div className="space-y-3">
              <div className="flex items-center gap-4 bg-slate-800/50 rounded-xl p-4">
                <AttainmentRing pct={rep.attainment_pct} size={64} />
                <div className="flex-1">
                  <div className="text-slate-300 font-semibold">{fmtLabel(rep.attainment_tier)}</div>
                  <div className="text-slate-400 text-sm mt-1">
                    {fmtMoney(rep.closed_won_value)} of {fmtMoney(rep.effective_quota)} quota
                  </div>
                  {rep.is_ramping && (
                    <div className="text-violet-400 text-xs mt-1">
                      Effective quota (ramp-adjusted): {fmtMoney(rep.effective_quota)}
                    </div>
                  )}
                </div>
              </div>
              {rep.gap_to_quota > 0 && (
                <>
                  <div className="grid grid-cols-2 gap-3">
                    <div className="bg-slate-800/50 rounded-lg p-3">
                      <div className="text-slate-500 text-xs">Gap to Quota</div>
                      <div className="text-orange-400 font-bold text-lg">{fmtMoney(rep.gap_to_quota)}</div>
                    </div>
                    <div className="bg-slate-800/50 rounded-lg p-3">
                      <div className="text-slate-500 text-xs">Deals Needed</div>
                      <div className="text-slate-100 font-bold text-lg">{rep.deals_needed} deals</div>
                    </div>
                    <div className="bg-slate-800/50 rounded-lg p-3">
                      <div className="text-slate-500 text-xs">Required Win Rate</div>
                      <div className="text-slate-100 font-bold">{(rep.required_win_rate * 100).toFixed(1)}%</div>
                    </div>
                    <div className="bg-slate-800/50 rounded-lg p-3">
                      <div className="text-slate-500 text-xs">Projected Attainment</div>
                      <div className={`font-bold ${rep.projected_attainment >= 100 ? "text-emerald-400" : "text-amber-400"}`}>
                        {rep.projected_attainment}%
                      </div>
                    </div>
                  </div>
                </>
              )}
            </div>
          )}

          {tab === "pipeline" && (
            <div className="space-y-3">
              {[
                { label: "Total Pipeline",    value: fmtMoney(rep.pipeline_value),      color: "text-indigo-300" },
                { label: "Late Stage",        value: fmtMoney(rep.late_stage_value),    color: "text-violet-300" },
                { label: "Active Deals",      value: `${rep.deals_in_pipeline} deals`,  color: "text-slate-300" },
                { label: "Win Rate",          value: `${(rep.win_rate * 100).toFixed(0)}%`, color: "text-slate-300" },
                { label: "Avg Deal Size",     value: fmtMoney(rep.avg_deal_size),       color: "text-slate-300" },
                { label: "Coverage",          value: fmtLabel(rep.pipeline_coverage),   color: "text-slate-300" },
              ].map(({ label, value, color }) => (
                <div key={label} className="flex items-center justify-between py-2 border-b border-slate-800/60 last:border-0">
                  <span className="text-slate-400 text-sm">{label}</span>
                  <span className={`font-semibold text-sm ${color}`}>{value}</span>
                </div>
              ))}
            </div>
          )}

          {tab === "metrics" && (
            <div className="grid grid-cols-2 gap-3">
              {[
                ["Achievement Score", `${rep.quota_achievement_score}/100`],
                ["Pipeline Health",   `${rep.pipeline_health_score}/100`],
                ["Region",            fmtLabel(rep.region)],
                ["Segment",           fmtLabel(rep.segment)],
                ["Days Remaining",    `${rep.days_remaining}d`],
                ["Manager",           rep.manager_id],
              ].map(([label, val]) => (
                <div key={label} className="bg-slate-800/50 rounded-lg p-3">
                  <div className="text-slate-500 text-xs mb-1">{label}</div>
                  <div className="text-slate-100 font-semibold text-sm">{val}</div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

// ── Rep Card ──────────────────────────────────────────────────────────────────

function RepCard({ rep, onClick }: { rep: Rep; onClick: () => void }) {
  const gapPct = rep.effective_quota > 0
    ? Math.min(100, (rep.closed_won_value / rep.effective_quota) * 100)
    : 100;

  return (
    <button
      onClick={onClick}
      className={`w-full text-left p-4 rounded-xl border transition-all hover:border-indigo-500/50 hover:bg-slate-800/80 ${tierBg(rep.attainment_tier)}`}
    >
      <div className="flex items-start gap-3">
        <AttainmentRing pct={rep.attainment_pct} size={52} />
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 flex-wrap mb-0.5">
            <span className="text-slate-100 font-semibold text-sm">{rep.rep_name}</span>
            {rep.is_at_risk && (
              <span className="px-1 py-0.5 bg-red-900/50 text-red-300 border border-red-700/50 rounded text-[10px] font-medium">
                AT RISK
              </span>
            )}
            {rep.is_ramping && (
              <span className="px-1 py-0.5 bg-violet-900/50 text-violet-300 border border-violet-700/50 rounded text-[10px] font-medium">
                RAMP
              </span>
            )}
          </div>
          <p className="text-slate-400 text-xs">{fmtLabel(rep.region)} · {fmtLabel(rep.segment)}</p>
          <div className="flex items-center gap-2 mt-1.5 flex-wrap">
            <span className={`text-[10px] font-medium ${tierColor(rep.attainment_tier)}`}>
              {fmtLabel(rep.attainment_tier)}
            </span>
            <span className="text-slate-600">·</span>
            <span className={`px-1.5 py-0.5 rounded text-[10px] font-medium ${actionBadge(rep.recommended_action)}`}>
              {fmtLabel(rep.recommended_action)}
            </span>
          </div>
        </div>
        <div className="text-right flex-shrink-0">
          {rep.gap_to_quota > 0 ? (
            <>
              <div className="text-orange-400 font-bold text-sm">{fmtMoney(rep.gap_to_quota)}</div>
              <div className="text-slate-500 text-[10px]">gap</div>
            </>
          ) : (
            <div className="text-emerald-400 font-bold text-sm">✓ Done</div>
          )}
        </div>
      </div>

      {/* Progress bar */}
      <div className="mt-3">
        <div className="flex items-center justify-between text-[10px] text-slate-500 mb-1">
          <span>{fmtMoney(rep.closed_won_value)} won</span>
          <span>quota {fmtMoney(rep.effective_quota)}</span>
        </div>
        <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
          <div
            className={`h-full rounded-full transition-all ${
              rep.attainment_pct >= 110 ? "bg-emerald-500" :
              rep.attainment_pct >= 90  ? "bg-blue-500" :
              rep.attainment_pct >= 70  ? "bg-amber-500" :
              rep.attainment_pct >= 50  ? "bg-orange-500" : "bg-red-500"
            }`}
            style={{ width: `${gapPct}%` }}
          />
        </div>
        <div className="text-slate-500 text-[10px] mt-1">
          Projected: <span className={rep.projected_attainment >= 100 ? "text-emerald-400" : "text-amber-400"}>
            {rep.projected_attainment}%
          </span>
          {" · "}{rep.days_remaining}d remaining
        </div>
      </div>
    </button>
  );
}

// ── Page ──────────────────────────────────────────────────────────────────────

export default function QuotaGapAnalysisPage() {
  const [data, setData]       = useState<{ reps: Rep[]; summary: Summary } | null>(null);
  const [loading, setLoading] = useState(true);
  const [tierFilter, setTierFilter]     = useState("");
  const [riskFilter, setRiskFilter]     = useState("");
  const [regionFilter, setRegionFilter] = useState("");
  const [selected, setSelected]         = useState<Rep | null>(null);

  useEffect(() => {
    async function load() {
        setLoading(true);
        try {
          const params = new URLSearchParams();
          if (tierFilter)   params.set("tier", tierFilter);
          if (riskFilter)   params.set("risk", riskFilter);
          if (regionFilter) params.set("region", regionFilter);
          const res = await fetch(`/api/quota-gap-analysis?${params}`);
          if (res.ok) setData(await res.json());
        } finally {
          setLoading(false);
        }
  }
    load();
  }, [tierFilter, riskFilter, regionFilter]);

  const s    = data?.summary;
  const reps = data?.reps ?? [];

  const tiers   = ["overachiever", "on_track", "at_risk", "behind", "critical"];
  const risks   = ["low", "medium", "high", "critical"];
  const regions = ["EMEA", "APAC", "Americas"];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {/* Header */}
      <div className="flex items-start justify-between gap-4 flex-wrap">
        <div>
          <h1 className="text-2xl font-bold text-slate-100">Quota Gap Analysis</h1>
          <p className="text-slate-400 text-sm mt-1">Rep-level attainment tracking, gap forecasting & action recommendations</p>
        </div>
        <button
          onClick={load}
          className="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg text-sm font-medium transition-colors"
        >
          Refresh
        </button>
      </div>

      {/* KPI Strip */}
      {s && (
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
          {[
            { label: "Total Gap",       value: fmtMoney(s.total_gap),                  sub: `${s.total} reps` },
            { label: "Avg Attainment",  value: `${s.avg_attainment_pct}%`,             sub: `proj. ${s.avg_projected_attainment}%` },
            { label: "At Risk",         value: String(s.at_risk_count),                sub: "reps need help" },
            { label: "Overachievers",   value: String(s.overachiever_count),           sub: `${s.critical_count} critical` },
          ].map(({ label, value, sub }) => (
            <div key={label} className="bg-slate-900 border border-slate-800 rounded-xl p-4">
              <div className="text-slate-400 text-xs">{label}</div>
              <div className="text-slate-100 font-bold text-xl mt-1">{value}</div>
              <div className="text-slate-500 text-xs mt-0.5">{sub}</div>
            </div>
          ))}
        </div>
      )}

      {/* Tier Distribution */}
      {s && (
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
          <h2 className="text-slate-300 text-sm font-semibold mb-3">Attainment Tier Distribution</h2>
          <TierDistBar counts={s.tier_counts} />
        </div>
      )}

      {/* Filters */}
      <div className="flex gap-2 flex-wrap">
        {/* Tier filter */}
        <div className="flex items-center gap-1 bg-slate-900 border border-slate-800 rounded-lg px-2 py-1">
          <span className="text-slate-500 text-xs">Tier:</span>
          <div className="flex gap-1">
            {["", ...tiers].map((t) => (
              <button
                key={t}
                onClick={() => setTierFilter(t)}
                className={`px-2 py-0.5 rounded text-xs font-medium transition-colors ${
                  tierFilter === t ? "bg-indigo-600 text-white" : "text-slate-400 hover:text-slate-200"
                }`}
              >
                {t ? fmtLabel(t) : "All"}
              </button>
            ))}
          </div>
        </div>

        {/* Risk filter */}
        <div className="flex items-center gap-1 bg-slate-900 border border-slate-800 rounded-lg px-2 py-1">
          <span className="text-slate-500 text-xs">Risk:</span>
          <div className="flex gap-1">
            {["", ...risks].map((r) => (
              <button
                key={r}
                onClick={() => setRiskFilter(r)}
                className={`px-2 py-0.5 rounded text-xs font-medium transition-colors ${
                  riskFilter === r ? "bg-indigo-600 text-white" : "text-slate-400 hover:text-slate-200"
                }`}
              >
                {r ? fmtLabel(r) : "All"}
              </button>
            ))}
          </div>
        </div>

        {/* Region filter */}
        <div className="flex items-center gap-1 bg-slate-900 border border-slate-800 rounded-lg px-2 py-1">
          <span className="text-slate-500 text-xs">Region:</span>
          <div className="flex gap-1">
            {["", ...regions].map((rg) => (
              <button
                key={rg}
                onClick={() => setRegionFilter(rg)}
                className={`px-2 py-0.5 rounded text-xs font-medium transition-colors ${
                  regionFilter === rg ? "bg-indigo-600 text-white" : "text-slate-400 hover:text-slate-200"
                }`}
              >
                {rg || "All"}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Rep Cards */}
      {loading ? (
        <div className="flex items-center justify-center py-16">
          <div className="w-8 h-8 border-2 border-indigo-500 border-t-transparent rounded-full animate-spin" />
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
          {reps.map((rep) => (
            <RepCard key={rep.rep_id} rep={rep} onClick={() => setSelected(rep)} />
          ))}
          {reps.length === 0 && (
            <div className="col-span-full text-center py-12 text-slate-500">
              No reps match the selected filters.
            </div>
          )}
        </div>
      )}

      {/* Action Summary */}
      {s && (
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
          <h2 className="text-slate-300 text-sm font-semibold mb-3">Recommended Actions</h2>
          <div className="flex flex-wrap gap-2">
            {Object.entries(s.action_counts)
              .sort((a, b) => b[1] - a[1])
              .map(([action, count]) => (
                <div key={action} className={`rounded-lg px-3 py-2 flex items-center gap-2 ${actionBadge(action)}`}>
                  <span className="text-sm font-medium">{fmtLabel(action)}</span>
                  <span className="bg-black/20 text-xs font-bold px-1.5 py-0.5 rounded">{count}</span>
                </div>
              ))}
          </div>
          <div className="grid grid-cols-3 gap-3 mt-4">
            <div className="bg-slate-800/50 rounded-lg p-3">
              <div className="text-slate-500 text-xs">Avg Achievement Score</div>
              <div className="text-slate-100 font-bold text-sm mt-1">{s.avg_achievement_score}/100</div>
            </div>
            <div className="bg-slate-800/50 rounded-lg p-3">
              <div className="text-slate-500 text-xs">Avg Pipeline Health</div>
              <div className="text-slate-100 font-bold text-sm mt-1">{s.avg_pipeline_health_score}/100</div>
            </div>
            <div className="bg-slate-800/50 rounded-lg p-3">
              <div className="text-slate-500 text-xs">Critical Reps</div>
              <div className="text-red-400 font-bold text-sm mt-1">{s.critical_count} reps</div>
            </div>
          </div>
        </div>
      )}

      {/* Modal */}
      {selected && <RepModal rep={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
