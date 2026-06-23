"use client";

import { useState, useEffect } from "react";

type Deal = {
  deal_id: string;
  deal_name: string;
  rep_id: string;
  account_id: string;
  stage_number: number;
  deal_value: number;
  velocity_trend: string;
  stage_health: string;
  deal_outcome: string;
  velocity_action: string;
  velocity_score: number;
  stage_progression_rate: number;
  close_date_risk: number;
  engagement_score: number;
  momentum_score: number;
  deal_health_index: number;
  is_at_risk: boolean;
  needs_escalation: boolean;
  probability_pct: number;
  expected_close_days: number;
  last_activity_days_ago: number;
  competitor_present: boolean;
  decision_maker_engaged: boolean;
  champion_identified: boolean;
  nrr_expansion_potential: number;
};

type Summary = {
  total: number;
  trend_counts: Record<string, number>;
  health_counts: Record<string, number>;
  outcome_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_velocity_score: number;
  avg_deal_health_index: number;
  avg_close_date_risk: number;
  at_risk_count: number;
  escalation_count: number;
  avg_engagement_score: number;
  avg_momentum_score: number;
  healthy_deal_count: number;
};

// ── helpers ───────────────────────────────────────────────────────────────────

function fmtCurrency(n: number) {
  if (n >= 1_000_000) return `$${(n / 1_000_000).toFixed(1)}M`;
  if (n >= 1_000) return `$${(n / 1_000).toFixed(0)}K`;
  return `$${n}`;
}

function outcomeColor(o: string) {
  const m: Record<string, string> = {
    likely_close: "text-emerald-400",
    on_track:     "text-blue-400",
    at_risk:      "text-amber-400",
    likely_slip:  "text-orange-400",
    likely_lose:  "text-red-400",
  };
  return m[o] ?? "text-slate-400";
}

function outcomeBg(o: string) {
  const m: Record<string, string> = {
    likely_close: "bg-emerald-500/10 border-emerald-500/30",
    on_track:     "bg-blue-500/10 border-blue-500/30",
    at_risk:      "bg-amber-500/10 border-amber-500/30",
    likely_slip:  "bg-orange-500/10 border-orange-500/30",
    likely_lose:  "bg-red-500/10 border-red-500/30",
  };
  return m[o] ?? "bg-slate-700/30 border-slate-700";
}

function healthColor(h: string) {
  const m: Record<string, string> = {
    healthy:  "text-emerald-400",
    slow:     "text-amber-400",
    stuck:    "text-orange-400",
    critical: "text-red-400",
  };
  return m[h] ?? "text-slate-400";
}

function trendIcon(t: string) {
  const m: Record<string, string> = {
    accelerating: "▲",
    stable:       "→",
    decelerating: "▼",
    stalled:      "⏸",
  };
  return m[t] ?? "–";
}

function trendColor(t: string) {
  const m: Record<string, string> = {
    accelerating: "text-emerald-400",
    stable:       "text-blue-400",
    decelerating: "text-amber-400",
    stalled:      "text-red-400",
  };
  return m[t] ?? "text-slate-400";
}

function healthIndexColor(v: number) {
  if (v >= 70) return "#34d399";
  if (v >= 50) return "#60a5fa";
  if (v >= 35) return "#fb923c";
  return "#f87171";
}

function scoreArc(value: number, cx: number, cy: number, r: number) {
  const circ = 2 * Math.PI * r;
  const arc  = (value / 100) * circ;
  return { arc, circ };
}

// ── VelocityRing ──────────────────────────────────────────────────────────────

function VelocityRing({ value, size = 72 }: { value: number; size?: number }) {
  const cx = size / 2, cy = size / 2, r = (size - 10) / 2;
  const { arc, circ } = scoreArc(value, cx, cy, r);
  const color = healthIndexColor(value);
  return (
    <svg width={size} height={size} className="flex-shrink-0">
      <circle cx={cx} cy={cy} r={r} fill="none" stroke="#1e293b" strokeWidth={8} />
      <circle
        cx={cx} cy={cy} r={r}
        fill="none" stroke={color} strokeWidth={8}
        strokeDasharray={`${arc} ${circ - arc}`}
        strokeLinecap="round"
        transform={`rotate(-90 ${cx} ${cy})`}
      />
      <text x={cx} y={cy + 1} textAnchor="middle" dominantBaseline="middle"
        fill={color} fontSize={size < 60 ? 10 : 13} fontWeight="bold">
        {Math.round(value)}
      </text>
    </svg>
  );
}

// ── OutcomeDistBar ────────────────────────────────────────────────────────────

const OUTCOME_ORDER = ["likely_close", "on_track", "at_risk", "likely_slip", "likely_lose"];
const OUTCOME_COLORS: Record<string, string> = {
  likely_close: "bg-emerald-500",
  on_track:     "bg-blue-500",
  at_risk:      "bg-amber-500",
  likely_slip:  "bg-orange-500",
  likely_lose:  "bg-red-500",
};

function OutcomeDistBar({ counts, total }: { counts: Record<string, number>; total: number }) {
  if (total === 0) return null;
  return (
    <div className="space-y-2">
      <div className="flex h-3 rounded-full overflow-hidden gap-0.5">
        {OUTCOME_ORDER.map((o) => {
          const n = counts[o] ?? 0;
          if (!n) return null;
          const pct = (n / total) * 100;
          return (
            <div key={o} className={`${OUTCOME_COLORS[o]} h-full`} style={{ width: `${pct}%` }} />
          );
        })}
      </div>
      <div className="flex flex-wrap gap-3">
        {OUTCOME_ORDER.map((o) => {
          const n = counts[o] ?? 0;
          if (!n) return null;
          return (
            <span key={o} className="flex items-center gap-1.5 text-xs text-slate-400">
              <span className={`w-2 h-2 rounded-full ${OUTCOME_COLORS[o]}`} />
              {o.replace("_", " ")} ({n})
            </span>
          );
        })}
      </div>
    </div>
  );
}

// ── MiniBar ───────────────────────────────────────────────────────────────────

function MiniBar({ value, color }: { value: number; color: string }) {
  return (
    <div className="w-full bg-slate-700/50 rounded-full h-1.5 mt-1">
      <div className={`${color} h-1.5 rounded-full`} style={{ width: `${Math.min(100, value)}%` }} />
    </div>
  );
}

// ── DealCard ─────────────────────────────────────────────────────────────────

function DealCard({ deal, onClick }: { deal: Deal; onClick: () => void }) {
  return (
    <div
      onClick={onClick}
      className={`rounded-xl border p-4 cursor-pointer hover:brightness-110 transition-all ${outcomeBg(deal.deal_outcome)}`}
    >
      <div className="flex items-start gap-3">
        <VelocityRing value={deal.deal_health_index} />
        <div className="flex-1 min-w-0">
          <div className="flex items-start justify-between gap-2">
            <p className="text-sm font-semibold text-white leading-tight truncate">
              {deal.deal_name}
            </p>
            <div className="flex items-center gap-1 flex-shrink-0">
              {deal.needs_escalation && (
                <span className="bg-red-500/20 text-red-400 text-[9px] font-bold px-1.5 py-0.5 rounded uppercase tracking-wide">
                  Escalate
                </span>
              )}
              {deal.is_at_risk && !deal.needs_escalation && (
                <span className="bg-amber-500/20 text-amber-400 text-[9px] font-bold px-1.5 py-0.5 rounded uppercase tracking-wide">
                  At Risk
                </span>
              )}
            </div>
          </div>

          <div className="flex items-center gap-2 mt-0.5 flex-wrap">
            <span className={`text-xs font-semibold ${outcomeColor(deal.deal_outcome)}`}>
              {deal.deal_outcome.replace(/_/g, " ")}
            </span>
            <span className="text-slate-600">·</span>
            <span className={`text-xs ${trendColor(deal.velocity_trend)}`}>
              {trendIcon(deal.velocity_trend)} {deal.velocity_trend}
            </span>
            <span className="text-slate-600">·</span>
            <span className={`text-xs ${healthColor(deal.stage_health)}`}>
              {deal.stage_health}
            </span>
          </div>

          <div className="grid grid-cols-2 gap-x-4 mt-2">
            <div>
              <p className="text-[10px] text-slate-500">Deal Value</p>
              <p className="text-xs text-white font-medium">{fmtCurrency(deal.deal_value)}</p>
            </div>
            <div>
              <p className="text-[10px] text-slate-500">Close in</p>
              <p className={`text-xs font-medium ${deal.expected_close_days < 7 ? "text-amber-400" : "text-slate-300"}`}>
                {deal.expected_close_days}d
              </p>
            </div>
          </div>

          <div className="mt-2 space-y-1">
            <div>
              <p className="text-[10px] text-slate-500">Engagement</p>
              <MiniBar value={deal.engagement_score}
                color={deal.engagement_score >= 70 ? "bg-emerald-500" : deal.engagement_score >= 50 ? "bg-blue-500" : "bg-amber-500"} />
            </div>
            <div>
              <p className="text-[10px] text-slate-500">Momentum</p>
              <MiniBar value={deal.momentum_score}
                color={deal.momentum_score >= 60 ? "bg-violet-500" : deal.momentum_score >= 40 ? "bg-amber-500" : "bg-red-500"} />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

// ── DealModal ─────────────────────────────────────────────────────────────────

function DealModal({ deal, onClose }: { deal: Deal; onClose: () => void }) {
  const [tab, setTab] = useState<"velocity" | "pipeline" | "signals">("velocity");

  useEffect(() => {
    const handler = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [onClose]);

  const tabs = [
    { id: "velocity" as const, label: "Velocity" },
    { id: "pipeline" as const, label: "Pipeline" },
    { id: "signals"  as const, label: "Signals" },
  ];

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm"
      onClick={onClose}>
      <div className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-lg max-h-[90vh] overflow-y-auto shadow-2xl"
        onClick={(e) => e.stopPropagation()}>
        {/* Header */}
        <div className="flex items-start justify-between p-5 border-b border-slate-800">
          <div className="flex items-center gap-4">
            <VelocityRing value={deal.deal_health_index} size={64} />
            <div>
              <p className="text-xs text-slate-400 mb-0.5">{deal.rep_id} · Stage {deal.stage_number}</p>
              <h2 className="text-base font-bold text-white leading-tight">{deal.deal_name}</h2>
              <div className="flex items-center gap-2 mt-1">
                <span className={`text-xs font-semibold ${outcomeColor(deal.deal_outcome)}`}>
                  {deal.deal_outcome.replace(/_/g, " ")}
                </span>
                <span className="text-slate-600">·</span>
                <span className={`text-xs ${trendColor(deal.velocity_trend)}`}>
                  {trendIcon(deal.velocity_trend)} {deal.velocity_trend}
                </span>
              </div>
            </div>
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-white text-xl leading-none p-1">×</button>
        </div>

        {/* Action banner */}
        <div className="px-5 pt-4">
          <div className="flex items-center gap-2 rounded-lg bg-indigo-500/10 border border-indigo-500/25 p-3">
            <span className="text-indigo-400 text-xs">⚡ Recommended Action:</span>
            <span className="text-white text-xs font-semibold capitalize">
              {deal.velocity_action.replace(/_/g, " ")}
            </span>
          </div>
        </div>

        {/* Tabs */}
        <div className="flex gap-1 px-5 mt-4">
          {tabs.map((t) => (
            <button key={t.id} onClick={() => setTab(t.id)}
              className={`text-xs font-medium px-3 py-1.5 rounded-md transition-colors ${
                tab === t.id ? "bg-indigo-600 text-white" : "text-slate-400 hover:text-white hover:bg-slate-800"
              }`}>
              {t.label}
            </button>
          ))}
        </div>

        <div className="p-5 space-y-4">
          {tab === "velocity" && (
            <>
              <div className="grid grid-cols-2 gap-3">
                {[
                  { label: "Velocity Score", value: `${deal.velocity_score}`, unit: "/100" },
                  { label: "Health Index",   value: `${deal.deal_health_index}`, unit: "/100" },
                  { label: "Momentum",       value: `${deal.momentum_score}`, unit: "/100" },
                  { label: "Close Risk",     value: `${deal.close_date_risk}`, unit: "/100" },
                ].map(({ label, value, unit }) => (
                  <div key={label} className="bg-slate-800/60 rounded-lg p-3">
                    <p className="text-[10px] text-slate-500 mb-0.5">{label}</p>
                    <p className="text-lg font-bold text-white">{value}<span className="text-xs text-slate-500">{unit}</span></p>
                  </div>
                ))}
              </div>
              <div className="bg-slate-800/40 rounded-lg p-3 space-y-2">
                <p className="text-xs font-medium text-slate-300 mb-1">Progression Rate</p>
                <div className="flex items-center justify-between">
                  <span className="text-xs text-slate-400">Stage vs Avg</span>
                  <span className={`text-xs font-bold ${deal.stage_progression_rate >= 1.2 ? "text-emerald-400" : deal.stage_progression_rate >= 0.8 ? "text-blue-400" : "text-red-400"}`}>
                    {deal.stage_progression_rate}×
                  </span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-xs text-slate-400">Last Activity</span>
                  <span className={`text-xs font-medium ${deal.last_activity_days_ago <= 3 ? "text-emerald-400" : deal.last_activity_days_ago <= 7 ? "text-amber-400" : "text-red-400"}`}>
                    {deal.last_activity_days_ago}d ago
                  </span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-xs text-slate-400">Expected Close</span>
                  <span className={`text-xs font-medium ${deal.expected_close_days <= 7 ? "text-amber-400" : "text-slate-300"}`}>
                    {deal.expected_close_days > 0 ? `${deal.expected_close_days}d` : "Overdue"}
                  </span>
                </div>
              </div>
            </>
          )}

          {tab === "pipeline" && (
            <>
              <div className="grid grid-cols-2 gap-3">
                {[
                  { label: "Deal Value",      value: fmtCurrency(deal.deal_value) },
                  { label: "NRR Potential",   value: fmtCurrency(deal.nrr_expansion_potential) },
                  { label: "Probability",     value: `${deal.probability_pct}%` },
                  { label: "Stage",           value: `${deal.stage_number}/5` },
                ].map(({ label, value }) => (
                  <div key={label} className="bg-slate-800/60 rounded-lg p-3">
                    <p className="text-[10px] text-slate-500 mb-0.5">{label}</p>
                    <p className="text-base font-bold text-white">{value}</p>
                  </div>
                ))}
              </div>
              <div className="bg-slate-800/40 rounded-lg p-3">
                <p className="text-xs font-medium text-slate-300 mb-2">Engagement Breakdown</p>
                <div className="space-y-1.5">
                  <div className="flex justify-between items-center">
                    <span className="text-xs text-slate-400">Engagement Score</span>
                    <span className="text-xs font-medium text-white">{deal.engagement_score}/100</span>
                  </div>
                  <MiniBar value={deal.engagement_score}
                    color={deal.engagement_score >= 70 ? "bg-emerald-500" : "bg-amber-500"} />
                  <div className="flex gap-4 mt-1 flex-wrap">
                    <Pill active={deal.decision_maker_engaged} label="DM Engaged" />
                    <Pill active={deal.champion_identified} label="Champion" />
                    <Pill active={deal.competitor_present} label="Competitor" negative />
                  </div>
                </div>
              </div>
            </>
          )}

          {tab === "signals" && (
            <div className="space-y-3">
              <div className="grid grid-cols-2 gap-2">
                {[
                  { label: "Stage Health",   value: deal.stage_health,    color: healthColor(deal.stage_health) },
                  { label: "Velocity Trend", value: deal.velocity_trend,  color: trendColor(deal.velocity_trend) },
                ].map(({ label, value, color }) => (
                  <div key={label} className="bg-slate-800/60 rounded-lg p-3">
                    <p className="text-[10px] text-slate-500 mb-0.5">{label}</p>
                    <p className={`text-sm font-bold capitalize ${color}`}>{value.replace(/_/g, " ")}</p>
                  </div>
                ))}
              </div>
              <div className="bg-slate-800/40 rounded-lg p-3 space-y-2">
                <p className="text-xs font-medium text-slate-300 mb-1">Deal Signals</p>
                <Pill active={!deal.competitor_present} label="No Competitor" />
                <Pill active={deal.decision_maker_engaged} label="DM Engaged" />
                <Pill active={deal.champion_identified} label="Champion Identified" />
                <Pill active={deal.is_at_risk} label="At Risk" negative />
                <Pill active={deal.needs_escalation} label="Needs Escalation" negative />
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

function Pill({ active, label, negative = false }: { active: boolean; label: string; negative?: boolean }) {
  if (!active) return null;
  const cls = negative
    ? "bg-red-500/15 text-red-400 border-red-500/25"
    : "bg-emerald-500/15 text-emerald-400 border-emerald-500/25";
  return (
    <span className={`inline-block text-[10px] font-medium px-2 py-0.5 rounded border mr-1 mb-1 ${cls}`}>
      {label}
    </span>
  );
}

// ── KPI Strip ─────────────────────────────────────────────────────────────────

function KPICard({ label, value, sub, accent }: {
  label: string; value: string | number; sub?: string; accent?: string;
}) {
  return (
    <div className="bg-slate-800/60 border border-slate-700/50 rounded-xl p-4">
      <p className="text-xs text-slate-400 mb-1">{label}</p>
      <p className={`text-2xl font-bold ${accent ?? "text-white"}`}>{value}</p>
      {sub && <p className="text-[11px] text-slate-500 mt-0.5">{sub}</p>}
    </div>
  );
}

// ── Page ──────────────────────────────────────────────────────────────────────

const TREND_FILTERS = ["all", "accelerating", "stable", "decelerating", "stalled"];
const OUTCOME_FILTERS = ["all", "likely_close", "on_track", "at_risk", "likely_slip", "likely_lose"];

export default function DealVelocityPage() {
  const [deals, setDeals]         = useState<Deal[]>([]);
  const [summary, setSummary]     = useState<Summary | null>(null);
  const [loading, setLoading]     = useState(true);
  const [trendFilter, setTrend]   = useState("all");
  const [outcomeFilter, setOutcome] = useState("all");
  const [selected, setSelected]   = useState<Deal | null>(null);

  useEffect(() => {
    async function fetchData() {
        setLoading(true);
        try {
          const params = new URLSearchParams();
          if (trendFilter !== "all")   params.set("trend", trendFilter);
          if (outcomeFilter !== "all") params.set("outcome", outcomeFilter);
          const qs = params.toString();
          const res = await fetch(`/api/deal-velocity${qs ? `?${qs}` : ""}`, { cache: "no-store" });
          const data = await res.json();
          setDeals(data.deals ?? []);
          setSummary(data.summary ?? null);
        } finally {
          setLoading(false);
        }
  }
    fetchData();
  }, [trendFilter, outcomeFilter]);

  const totalValue = deals.reduce((s, d) => s + d.deal_value, 0);

  return (
    <div className="min-h-screen bg-slate-950 p-4 md:p-6 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-xl font-bold text-white">Deal Velocity Engine</h1>
          <p className="text-sm text-slate-400 mt-0.5">Stage progression · health index · close-date risk</p>
        </div>
        <button onClick={fetchData}
          className="text-xs text-indigo-400 hover:text-indigo-300 border border-indigo-500/30 hover:border-indigo-400/50 px-3 py-1.5 rounded-lg transition-colors">
          Refresh
        </button>
      </div>

      {/* KPI strip */}
      {summary && (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
          <KPICard label="Total Deals"       value={summary.total}              sub="in pipeline" />
          <KPICard label="Avg Health Index"  value={`${summary.avg_deal_health_index}`} sub="/100" accent="text-blue-400" />
          <KPICard label="At Risk"           value={summary.at_risk_count}      sub="need attention" accent="text-amber-400" />
          <KPICard label="Need Escalation"   value={summary.escalation_count}   sub="critical deals" accent="text-red-400" />
        </div>
      )}

      {/* Outcome distribution */}
      {summary && (
        <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-4">
          <div className="flex items-center justify-between mb-3">
            <p className="text-sm font-semibold text-slate-300">Outcome Distribution</p>
            <div className="flex items-center gap-3 text-xs text-slate-500">
              <span>Avg velocity: <span className="text-white font-medium">{summary.avg_velocity_score}</span></span>
              <span>Avg close risk: <span className={`font-medium ${summary.avg_close_date_risk > 40 ? "text-amber-400" : "text-white"}`}>{summary.avg_close_date_risk}</span></span>
            </div>
          </div>
          <OutcomeDistBar counts={summary.outcome_counts} total={summary.total} />
        </div>
      )}

      {/* Trend filter */}
      <div className="flex flex-col gap-2">
        <div className="flex flex-wrap gap-2">
          {TREND_FILTERS.map((f) => (
            <button key={f} onClick={() => setTrend(f)}
              className={`text-xs px-3 py-1.5 rounded-lg font-medium transition-colors ${
                trendFilter === f
                  ? "bg-indigo-600 text-white"
                  : "bg-slate-800 text-slate-400 hover:text-white hover:bg-slate-700"
              }`}>
              {f === "all" ? "All Trends" : `${trendIcon(f)} ${f}`}
            </button>
          ))}
        </div>
        <div className="flex flex-wrap gap-2">
          {OUTCOME_FILTERS.map((f) => (
            <button key={f} onClick={() => setOutcome(f)}
              className={`text-xs px-3 py-1.5 rounded-lg font-medium transition-colors ${
                outcomeFilter === f
                  ? "bg-violet-600 text-white"
                  : "bg-slate-800 text-slate-400 hover:text-white hover:bg-slate-700"
              }`}>
              {f === "all" ? "All Outcomes" : f.replace(/_/g, " ")}
            </button>
          ))}
        </div>
      </div>

      {/* Pipeline value banner */}
      {deals.length > 0 && (
        <div className="bg-slate-800/40 border border-slate-700/40 rounded-xl px-4 py-2.5 flex items-center justify-between">
          <span className="text-xs text-slate-400">Filtered pipeline value</span>
          <span className="text-sm font-bold text-white">{fmtCurrency(totalValue)}</span>
        </div>
      )}

      {/* Cards */}
      {loading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {[...Array(6)].map((_, i) => (
            <div key={i} className="rounded-xl border border-slate-800 bg-slate-800/30 h-44 animate-pulse" />
          ))}
        </div>
      ) : deals.length === 0 ? (
        <div className="text-center py-16 text-slate-500">No deals match the selected filters.</div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {deals.map((d) => (
            <DealCard key={d.deal_id} deal={d} onClick={() => setSelected(d)} />
          ))}
        </div>
      )}

      {/* Aggregate stats */}
      {summary && (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
          <KPICard label="Avg Engagement"  value={`${summary.avg_engagement_score}`} sub="/100" accent="text-violet-400" />
          <KPICard label="Avg Momentum"    value={`${summary.avg_momentum_score}`} sub="/100" accent="text-blue-400" />
          <KPICard label="Healthy Deals"   value={summary.healthy_deal_count} sub="health ≥ 65" accent="text-emerald-400" />
          <KPICard label="Avg Close Risk"  value={`${summary.avg_close_date_risk}`} sub="/100"
            accent={summary.avg_close_date_risk > 40 ? "text-amber-400" : "text-slate-300"} />
        </div>
      )}

      {/* Modal */}
      {selected && <DealModal deal={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
