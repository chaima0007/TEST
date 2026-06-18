"use client";

import { useState, useEffect, useCallback } from "react";

type Team = {
  team_id: string;
  region: string;
  segment: string;
  manager_id: string;
  coverage_status: string;
  gap_severity: string;
  pipeline_quality: string;
  coverage_action: string;
  coverage_ratio: number;
  weighted_coverage_ratio: number;
  gap_to_quota: number;
  pipeline_velocity: number;
  quality_score: number;
  stage_mix_score: number;
  coverage_trend: number;
  is_at_risk: boolean;
  needs_intervention: boolean;
  quota_remaining: number;
  current_pipeline: number;
  weighted_pipeline: number;
  avg_deal_health: number;
  stalled_deal_count: number;
  competitive_deal_pct: number;
};

type Summary = {
  total: number;
  status_counts: Record<string, number>;
  gap_severity_counts: Record<string, number>;
  quality_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_coverage_ratio: number;
  avg_weighted_coverage: number;
  total_gap_to_quota: number;
  at_risk_count: number;
  intervention_count: number;
  avg_quality_score: number;
  avg_stage_mix_score: number;
  healthy_team_count: number;
};

// ── helpers ───────────────────────────────────────────────────────────────────

function fmtCurrency(n: number) {
  if (n >= 1_000_000) return `$${(n / 1_000_000).toFixed(1)}M`;
  if (n >= 1_000)     return `$${(n / 1_000).toFixed(0)}K`;
  return `$${n}`;
}

function statusColor(s: string) {
  const m: Record<string, string> = {
    over_covered:  "text-emerald-400",
    adequate:      "text-blue-400",
    under_covered: "text-amber-400",
    critical_gap:  "text-red-400",
  };
  return m[s] ?? "text-slate-400";
}

function statusBg(s: string) {
  const m: Record<string, string> = {
    over_covered:  "bg-emerald-500/10 border-emerald-500/30",
    adequate:      "bg-blue-500/10 border-blue-500/30",
    under_covered: "bg-amber-500/10 border-amber-500/30",
    critical_gap:  "bg-red-500/10 border-red-500/30",
  };
  return m[s] ?? "bg-slate-700/30 border-slate-700";
}

function gapColor(g: string) {
  const m: Record<string, string> = {
    none:     "text-emerald-400",
    low:      "text-blue-400",
    medium:   "text-amber-400",
    high:     "text-orange-400",
    critical: "text-red-400",
  };
  return m[g] ?? "text-slate-400";
}

function qualityColor(q: string) {
  const m: Record<string, string> = {
    excellent: "text-emerald-400",
    good:      "text-blue-400",
    fair:      "text-amber-400",
    poor:      "text-red-400",
  };
  return m[q] ?? "text-slate-400";
}

function coverageBarColor(ratio: number) {
  if (ratio >= 3.5) return "bg-emerald-500";
  if (ratio >= 2.0) return "bg-blue-500";
  if (ratio >= 1.0) return "bg-amber-500";
  return "bg-red-500";
}

// ── CoverageGauge ─────────────────────────────────────────────────────────────

function CoverageGauge({ ratio, size = 72 }: { ratio: number; size?: number }) {
  const cx = size / 2, cy = size / 2, r = (size - 10) / 2;
  const maxRatio = 5.0;
  const pct = Math.min(100, (ratio / maxRatio) * 100);
  const circ = 2 * Math.PI * r;
  const arc  = (pct / 100) * circ;
  const color = ratio >= 3.5 ? "#34d399" : ratio >= 2.0 ? "#60a5fa" : ratio >= 1.0 ? "#fb923c" : "#f87171";

  return (
    <svg width={size} height={size} className="flex-shrink-0">
      <circle cx={cx} cy={cy} r={r} fill="none" stroke="#1e293b" strokeWidth={8} />
      <circle cx={cx} cy={cy} r={r} fill="none" stroke={color} strokeWidth={8}
        strokeDasharray={`${arc} ${circ - arc}`} strokeLinecap="round"
        transform={`rotate(-90 ${cx} ${cy})`} />
      <text x={cx} y={cy - 5} textAnchor="middle" dominantBaseline="middle"
        fill={color} fontSize={size < 60 ? 9 : 11} fontWeight="bold">
        {ratio.toFixed(1)}x
      </text>
      <text x={cx} y={cy + 8} textAnchor="middle" dominantBaseline="middle"
        fill="#64748b" fontSize={size < 60 ? 7 : 8}>
        cover
      </text>
    </svg>
  );
}

// ── StatusDistBar ─────────────────────────────────────────────────────────────

const STATUS_ORDER = ["over_covered", "adequate", "under_covered", "critical_gap"];
const STATUS_COLORS: Record<string, string> = {
  over_covered:  "bg-emerald-500",
  adequate:      "bg-blue-500",
  under_covered: "bg-amber-500",
  critical_gap:  "bg-red-500",
};

function StatusDistBar({ counts, total }: { counts: Record<string, number>; total: number }) {
  if (total === 0) return null;
  return (
    <div className="space-y-2">
      <div className="flex h-3 rounded-full overflow-hidden gap-0.5">
        {STATUS_ORDER.map((s) => {
          const n = counts[s] ?? 0;
          if (!n) return null;
          return (
            <div key={s} className={`${STATUS_COLORS[s]} h-full`}
              style={{ width: `${(n / total) * 100}%` }} />
          );
        })}
      </div>
      <div className="flex flex-wrap gap-3">
        {STATUS_ORDER.map((s) => {
          const n = counts[s] ?? 0;
          if (!n) return null;
          return (
            <span key={s} className="flex items-center gap-1.5 text-xs text-slate-400">
              <span className={`w-2 h-2 rounded-full ${STATUS_COLORS[s]}`} />
              {s.replace(/_/g, " ")} ({n})
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
    <div className="w-full bg-slate-700/50 rounded-full h-1.5 mt-0.5">
      <div className={`${color} h-1.5 rounded-full`} style={{ width: `${Math.min(100, value)}%` }} />
    </div>
  );
}

// ── TeamCard ──────────────────────────────────────────────────────────────────

function TeamCard({ team, onClick }: { team: Team; onClick: () => void }) {
  return (
    <div onClick={onClick}
      className={`rounded-xl border p-4 cursor-pointer hover:brightness-110 transition-all ${statusBg(team.coverage_status)}`}>
      <div className="flex items-start gap-3">
        <CoverageGauge ratio={team.coverage_ratio} />
        <div className="flex-1 min-w-0">
          <div className="flex items-start justify-between gap-2">
            <div>
              <p className="text-sm font-semibold text-white">
                {team.region} · {team.segment}
              </p>
              <p className="text-[10px] text-slate-500">{team.team_id} · {team.manager_id}</p>
            </div>
            <div className="flex flex-col items-end gap-1">
              {team.needs_intervention && (
                <span className="bg-red-500/20 text-red-400 text-[9px] font-bold px-1.5 py-0.5 rounded uppercase">
                  Intervene
                </span>
              )}
              {team.is_at_risk && !team.needs_intervention && (
                <span className="bg-amber-500/20 text-amber-400 text-[9px] font-bold px-1.5 py-0.5 rounded uppercase">
                  At Risk
                </span>
              )}
            </div>
          </div>

          <div className="flex items-center gap-2 mt-1 flex-wrap">
            <span className={`text-xs font-semibold ${statusColor(team.coverage_status)}`}>
              {team.coverage_status.replace(/_/g, " ")}
            </span>
            <span className="text-slate-600">·</span>
            <span className={`text-xs ${gapColor(team.gap_severity)}`}>
              gap: {team.gap_severity}
            </span>
            <span className="text-slate-600">·</span>
            <span className={`text-xs ${qualityColor(team.pipeline_quality)}`}>
              {team.pipeline_quality}
            </span>
          </div>

          <div className="grid grid-cols-2 gap-x-4 mt-2">
            <div>
              <p className="text-[10px] text-slate-500">Remaining Quota</p>
              <p className="text-xs text-white font-medium">{fmtCurrency(team.quota_remaining)}</p>
            </div>
            <div>
              <p className="text-[10px] text-slate-500">Gap to Quota</p>
              <p className={`text-xs font-medium ${team.gap_to_quota > 0 ? "text-red-400" : "text-emerald-400"}`}>
                {team.gap_to_quota > 0 ? fmtCurrency(team.gap_to_quota) : "Covered"}
              </p>
            </div>
          </div>

          <div className="mt-2 space-y-1">
            <div>
              <p className="text-[10px] text-slate-500">Pipeline Quality</p>
              <MiniBar value={team.quality_score}
                color={team.quality_score >= 65 ? "bg-emerald-500" : team.quality_score >= 45 ? "bg-blue-500" : "bg-amber-500"} />
            </div>
            <div>
              <p className="text-[10px] text-slate-500">Stage Mix</p>
              <MiniBar value={team.stage_mix_score}
                color={team.stage_mix_score >= 55 ? "bg-violet-500" : "bg-amber-500"} />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

// ── TeamModal ─────────────────────────────────────────────────────────────────

function TeamModal({ team, onClose }: { team: Team; onClose: () => void }) {
  const [tab, setTab] = useState<"coverage" | "pipeline" | "metrics">("coverage");

  useEffect(() => {
    const h = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", h);
    return () => window.removeEventListener("keydown", h);
  }, [onClose]);

  const tabs = [
    { id: "coverage" as const, label: "Coverage" },
    { id: "pipeline" as const, label: "Pipeline" },
    { id: "metrics"  as const, label: "Metrics" },
  ];

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm"
      onClick={onClose}>
      <div className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-lg max-h-[90vh] overflow-y-auto shadow-2xl"
        onClick={(e) => e.stopPropagation()}>
        {/* Header */}
        <div className="flex items-start justify-between p-5 border-b border-slate-800">
          <div className="flex items-center gap-4">
            <CoverageGauge ratio={team.coverage_ratio} size={64} />
            <div>
              <p className="text-xs text-slate-400 mb-0.5">{team.team_id} · {team.manager_id}</p>
              <h2 className="text-base font-bold text-white">{team.region} — {team.segment}</h2>
              <div className="flex items-center gap-2 mt-1">
                <span className={`text-xs font-semibold ${statusColor(team.coverage_status)}`}>
                  {team.coverage_status.replace(/_/g, " ")}
                </span>
                <span className="text-slate-600">·</span>
                <span className={`text-xs ${gapColor(team.gap_severity)}`}>
                  gap {team.gap_severity}
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
              {team.coverage_action.replace(/_/g, " ")}
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
          {tab === "coverage" && (
            <>
              <div className="grid grid-cols-2 gap-3">
                {[
                  { label: "Coverage Ratio",    value: `${team.coverage_ratio}×` },
                  { label: "Weighted Coverage", value: `${team.weighted_coverage_ratio}×` },
                  { label: "Gap to Quota",      value: team.gap_to_quota > 0 ? fmtCurrency(team.gap_to_quota) : "Covered" },
                  { label: "Coverage Trend",    value: `${team.coverage_trend > 0 ? "+" : ""}${team.coverage_trend}%` },
                ].map(({ label, value }) => (
                  <div key={label} className="bg-slate-800/60 rounded-lg p-3">
                    <p className="text-[10px] text-slate-500 mb-0.5">{label}</p>
                    <p className="text-base font-bold text-white">{value}</p>
                  </div>
                ))}
              </div>
              <div className="bg-slate-800/40 rounded-lg p-3">
                <p className="text-xs font-medium text-slate-300 mb-2">Coverage Bar</p>
                <div className="w-full bg-slate-700 rounded-full h-3">
                  <div className={`${coverageBarColor(team.coverage_ratio)} h-3 rounded-full transition-all`}
                    style={{ width: `${Math.min(100, (team.coverage_ratio / 5) * 100)}%` }} />
                </div>
                <div className="flex justify-between text-[9px] text-slate-500 mt-1">
                  <span>0×</span><span>1× (min)</span><span>2× (ok)</span><span>3.5×</span><span>5×</span>
                </div>
              </div>
            </>
          )}

          {tab === "pipeline" && (
            <>
              <div className="grid grid-cols-2 gap-3">
                {[
                  { label: "Total Pipeline",   value: fmtCurrency(team.current_pipeline) },
                  { label: "Weighted Pipeline",value: fmtCurrency(team.weighted_pipeline) },
                  { label: "Remaining Quota",  value: fmtCurrency(team.quota_remaining) },
                  { label: "Velocity/Day",     value: fmtCurrency(team.pipeline_velocity) },
                ].map(({ label, value }) => (
                  <div key={label} className="bg-slate-800/60 rounded-lg p-3">
                    <p className="text-[10px] text-slate-500 mb-0.5">{label}</p>
                    <p className="text-sm font-bold text-white">{value}</p>
                  </div>
                ))}
              </div>
              <div className="bg-slate-800/40 rounded-lg p-3 space-y-2">
                <p className="text-xs font-medium text-slate-300 mb-1">Stage Mix Score</p>
                <MiniBar value={team.stage_mix_score}
                  color={team.stage_mix_score >= 50 ? "bg-violet-500" : "bg-amber-500"} />
                <p className="text-[10px] text-slate-500 mt-1">{team.stage_mix_score}/100 — higher = more late-stage pipeline</p>
              </div>
            </>
          )}

          {tab === "metrics" && (
            <>
              <div className="grid grid-cols-2 gap-3">
                {[
                  { label: "Quality Score",   value: `${team.quality_score}/100`, color: qualityColor(team.pipeline_quality) },
                  { label: "Pipeline Quality",value: team.pipeline_quality,       color: qualityColor(team.pipeline_quality) },
                  { label: "Avg Deal Health", value: `${team.avg_deal_health}/100` },
                  { label: "Stalled Deals",   value: `${team.stalled_deal_count}` },
                ].map(({ label, value, color }) => (
                  <div key={label} className="bg-slate-800/60 rounded-lg p-3">
                    <p className="text-[10px] text-slate-500 mb-0.5">{label}</p>
                    <p className={`text-sm font-bold capitalize ${color ?? "text-white"}`}>{value}</p>
                  </div>
                ))}
              </div>
              <div className="bg-slate-800/40 rounded-lg p-3">
                <p className="text-xs font-medium text-slate-300 mb-2">Risk Factors</p>
                <div className="flex flex-wrap gap-1.5">
                  <Chip active={team.is_at_risk}           label="At Risk"           negative />
                  <Chip active={team.needs_intervention}   label="Needs Intervention" negative />
                  <Chip active={team.competitive_deal_pct > 40} label={`${team.competitive_deal_pct}% Competitive`} negative />
                  <Chip active={!team.is_at_risk}          label="Healthy Coverage"  />
                </div>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
}

function Chip({ active, label, negative = false }: { active: boolean; label: string; negative?: boolean }) {
  if (!active) return null;
  const cls = negative
    ? "bg-red-500/15 text-red-400 border-red-500/25"
    : "bg-emerald-500/15 text-emerald-400 border-emerald-500/25";
  return (
    <span className={`text-[10px] font-medium px-2 py-0.5 rounded border ${cls}`}>{label}</span>
  );
}

// ── KPI Card ──────────────────────────────────────────────────────────────────

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

const STATUS_FILTERS = ["all", "over_covered", "adequate", "under_covered", "critical_gap"];
const GAP_FILTERS    = ["all", "none", "low", "medium", "high", "critical"];

export default function PipelineCoveragePage() {
  const [teams, setTeams]           = useState<Team[]>([]);
  const [summary, setSummary]       = useState<Summary | null>(null);
  const [loading, setLoading]       = useState(true);
  const [statusFilter, setStatus]   = useState("all");
  const [gapFilter, setGap]         = useState("all");
  const [selected, setSelected]     = useState<Team | null>(null);

  const fetchData = useCallback(async () => {
    setLoading(true);
    try {
      const params = new URLSearchParams();
      if (statusFilter !== "all") params.set("status", statusFilter);
      if (gapFilter !== "all")    params.set("gap", gapFilter);
      const qs = params.toString();
      const res = await fetch(`/api/pipeline-coverage${qs ? `?${qs}` : ""}`, { cache: "no-store" });
      const data = await res.json();
      setTeams(data.teams ?? []);
      setSummary(data.summary ?? null);
    } finally {
      setLoading(false);
    }
  }, [statusFilter, gapFilter]);

  useEffect(() => { fetchData(); }, [fetchData]);

  return (
    <div className="min-h-screen bg-slate-950 p-4 md:p-6 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-xl font-bold text-white">Pipeline Coverage Engine</h1>
          <p className="text-sm text-slate-400 mt-0.5">Coverage ratios · gap analysis · stage mix quality</p>
        </div>
        <button onClick={fetchData}
          className="text-xs text-indigo-400 hover:text-indigo-300 border border-indigo-500/30 hover:border-indigo-400/50 px-3 py-1.5 rounded-lg transition-colors">
          Refresh
        </button>
      </div>

      {/* KPI Strip */}
      {summary && (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
          <KPICard label="Teams"            value={summary.total}              sub="in pipeline" />
          <KPICard label="Avg Coverage"     value={`${summary.avg_coverage_ratio}×`} accent="text-blue-400" />
          <KPICard label="At Risk"          value={summary.at_risk_count}      sub="teams" accent="text-amber-400" />
          <KPICard label="Total Gap"        value={fmtCurrency(summary.total_gap_to_quota)} sub="to cover" accent={summary.total_gap_to_quota > 0 ? "text-red-400" : "text-emerald-400"} />
        </div>
      )}

      {/* Coverage distribution */}
      {summary && (
        <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-4">
          <div className="flex items-center justify-between mb-3">
            <p className="text-sm font-semibold text-slate-300">Coverage Status Distribution</p>
            <div className="flex items-center gap-3 text-xs text-slate-500">
              <span>Wtd coverage: <span className="text-white font-medium">{summary.avg_weighted_coverage}×</span></span>
              <span>Healthy: <span className="text-emerald-400 font-medium">{summary.healthy_team_count}</span></span>
            </div>
          </div>
          <StatusDistBar counts={summary.status_counts} total={summary.total} />
        </div>
      )}

      {/* Filters */}
      <div className="flex flex-col gap-2">
        <div className="flex flex-wrap gap-2">
          {STATUS_FILTERS.map((f) => (
            <button key={f} onClick={() => setStatus(f)}
              className={`text-xs px-3 py-1.5 rounded-lg font-medium transition-colors ${
                statusFilter === f
                  ? "bg-indigo-600 text-white"
                  : "bg-slate-800 text-slate-400 hover:text-white hover:bg-slate-700"
              }`}>
              {f === "all" ? "All Statuses" : f.replace(/_/g, " ")}
            </button>
          ))}
        </div>
        <div className="flex flex-wrap gap-2">
          {GAP_FILTERS.map((f) => (
            <button key={f} onClick={() => setGap(f)}
              className={`text-xs px-3 py-1.5 rounded-lg font-medium transition-colors ${
                gapFilter === f
                  ? "bg-violet-600 text-white"
                  : "bg-slate-800 text-slate-400 hover:text-white hover:bg-slate-700"
              }`}>
              {f === "all" ? "All Gaps" : `gap: ${f}`}
            </button>
          ))}
        </div>
      </div>

      {/* Cards */}
      {loading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {[...Array(6)].map((_, i) => (
            <div key={i} className="rounded-xl border border-slate-800 bg-slate-800/30 h-44 animate-pulse" />
          ))}
        </div>
      ) : teams.length === 0 ? (
        <div className="text-center py-16 text-slate-500">No teams match the selected filters.</div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {teams.map((t) => (
            <TeamCard key={t.team_id} team={t} onClick={() => setSelected(t)} />
          ))}
        </div>
      )}

      {/* Summary stats */}
      {summary && (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
          <KPICard label="Avg Quality Score" value={`${summary.avg_quality_score}`} sub="/100" accent="text-violet-400" />
          <KPICard label="Avg Stage Mix"     value={`${summary.avg_stage_mix_score}`} sub="/100" accent="text-blue-400" />
          <KPICard label="Need Intervention" value={summary.intervention_count} sub="critical" accent="text-red-400" />
          <KPICard label="Healthy Teams"     value={summary.healthy_team_count} sub="covered" accent="text-emerald-400" />
        </div>
      )}

      {selected && <TeamModal team={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
