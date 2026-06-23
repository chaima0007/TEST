"use client";

import { useEffect, useState } from "react";

// ── Types ─────────────────────────────────────────────────────────────────────

interface CapacityTeam {
  team_id: string;
  region: string;
  segment: string;
  manager_id: string;
  capacity_status: string;
  hiring_urgency: string;
  capacity_health: string;
  capacity_action: string;
  effective_capacity_pct: number;
  headcount_gap: number;
  quota_at_risk: number;
  pipeline_per_rep: number;
  required_attainment: number;
  ramp_impact: number;
  productivity_index: number;
  is_capacity_constrained: boolean;
  needs_immediate_hire: boolean;
  current_reps: number;
  target_reps: number;
  total_team_quota: number;
  pipeline_coverage_ratio: number;
}

interface Summary {
  total: number;
  status_counts: Record<string, number>;
  urgency_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_effective_capacity: number;
  total_quota_at_risk: number;
  avg_productivity_index: number;
  constrained_count: number;
  immediate_hire_count: number;
  critical_count: number;
  total_headcount_gap: number;
}

// ── Helpers ───────────────────────────────────────────────────────────────────

const STATUS_COLORS: Record<string, string> = {
  over_capacity: "text-sky-400",
  at_capacity: "text-emerald-400",
  under_capacity: "text-amber-400",
  critical_shortage: "text-rose-400",
};

const STATUS_BG: Record<string, string> = {
  over_capacity: "bg-sky-400/10 border-sky-400/30",
  at_capacity: "bg-emerald-400/10 border-emerald-400/30",
  under_capacity: "bg-amber-400/10 border-amber-400/30",
  critical_shortage: "bg-rose-400/10 border-rose-400/30",
};

const HEALTH_COLORS: Record<string, string> = {
  healthy: "text-emerald-400",
  at_risk: "text-amber-400",
  constrained: "text-orange-400",
  critical: "text-rose-400",
};

const ACTION_STYLES: Record<string, string> = {
  hire_immediately: "bg-rose-500/20 text-rose-300",
  accelerate_ramp: "bg-violet-500/20 text-violet-300",
  redistribute_quota: "bg-amber-500/20 text-amber-300",
  focus_productivity: "bg-sky-500/20 text-sky-300",
  maintain_capacity: "bg-emerald-500/20 text-emerald-300",
  strategic_review: "bg-slate-500/20 text-slate-300",
};

const ACTION_LABELS: Record<string, string> = {
  hire_immediately: "Hire Now",
  accelerate_ramp: "Accel Ramp",
  redistribute_quota: "Redistribute",
  focus_productivity: "Focus Prod.",
  maintain_capacity: "Maintain",
  strategic_review: "Review",
};

const STATUS_LABELS: Record<string, string> = {
  over_capacity: "Over",
  at_capacity: "At Capacity",
  under_capacity: "Under",
  critical_shortage: "Critical",
};

function fmt(n: number): string {
  if (n >= 1_000_000) return `$${(n / 1_000_000).toFixed(1)}M`;
  if (n >= 1_000) return `$${(n / 1_000).toFixed(0)}K`;
  return `$${n}`;
}

function capacityColor(pct: number): string {
  if (pct >= 100) return "#38bdf8";
  if (pct >= 80)  return "#10b981";
  if (pct >= 60)  return "#f59e0b";
  return "#f43f5e";
}

function CapacityGauge({ pct, size = 72 }: { pct: number; size?: number }) {
  const cx = size / 2, cy = size / 2, r = (size - 10) / 2;
  const circ = 2 * Math.PI * r;
  const arc = (Math.min(100, pct) / 100) * circ;
  const color = capacityColor(pct);
  return (
    <svg width={size} height={size} className="flex-shrink-0">
      <circle cx={cx} cy={cy} r={r} fill="none" stroke="#1e293b" strokeWidth={8} />
      <circle
        cx={cx} cy={cy} r={r} fill="none"
        stroke={color} strokeWidth={8}
        strokeDasharray={`${arc} ${circ - arc}`}
        strokeLinecap="round"
        transform={`rotate(-90 ${cx} ${cy})`}
      />
      <text x={cx} y={cy + 1} textAnchor="middle" dominantBaseline="middle"
        fill={color} fontSize={size < 64 ? 10 : 12} fontWeight="700">
        {pct.toFixed(0)}%
      </text>
    </svg>
  );
}

function StatusDistBar({ counts }: { counts: Record<string, number> }) {
  const total = Object.values(counts).reduce((s, v) => s + v, 0) || 1;
  const statuses = ["over_capacity", "at_capacity", "under_capacity", "critical_shortage"];
  const colors = ["#38bdf8", "#10b981", "#f59e0b", "#f43f5e"];
  return (
    <div className="w-full space-y-1">
      <div className="flex h-3 rounded-full overflow-hidden gap-px bg-slate-800">
        {statuses.map((s, i) =>
          counts[s] ? (
            <div key={s}
              style={{ width: `${(counts[s] / total) * 100}%`, background: colors[i] }}
              title={`${STATUS_LABELS[s]}: ${counts[s]}`} />
          ) : null
        )}
      </div>
      <div className="flex flex-wrap gap-x-3 gap-y-1">
        {statuses.map((s, i) =>
          counts[s] ? (
            <span key={s} className="flex items-center gap-1 text-[10px] text-slate-400">
              <span className="w-2 h-2 rounded-sm" style={{ background: colors[i] }} />
              {STATUS_LABELS[s]} ({counts[s]})
            </span>
          ) : null
        )}
      </div>
    </div>
  );
}

function BarMini({ value, max = 100, color }: { value: number; max?: number; color: string }) {
  const pct = Math.min(100, (value / max) * 100);
  return (
    <div className="h-1.5 bg-slate-700 rounded-full overflow-hidden">
      <div className="h-full rounded-full transition-all" style={{ width: `${pct}%`, background: color }} />
    </div>
  );
}

// ── Team Modal ────────────────────────────────────────────────────────────────

function TeamModal({ team, onClose }: { team: CapacityTeam; onClose: () => void }) {
  const [tab, setTab] = useState<"capacity" | "pipeline" | "metrics">("capacity");

  useEffect(() => {
    const handler = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    document.addEventListener("keydown", handler);
    return () => document.removeEventListener("keydown", handler);
  }, [onClose]);

  const color = capacityColor(team.effective_capacity_pct);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4"
      onClick={(e) => { if (e.target === e.currentTarget) onClose(); }}>
      <div className="absolute inset-0 bg-black/60 backdrop-blur-sm" onClick={onClose} />
      <div className="relative w-full max-w-xl bg-slate-900 border border-slate-700 rounded-2xl shadow-2xl overflow-hidden">

        <div className="flex items-start justify-between p-5 border-b border-slate-800">
          <div className="flex items-center gap-4">
            <CapacityGauge pct={team.effective_capacity_pct} size={64} />
            <div>
              <h2 className="text-white font-bold text-lg">{team.region} · {team.segment}</h2>
              <p className="text-slate-400 text-sm">{team.manager_id} · {team.current_reps}/{team.target_reps} reps</p>
              <div className="flex gap-2 mt-1.5 flex-wrap">
                <span className={`px-2 py-0.5 text-[11px] rounded-full border ${STATUS_BG[team.capacity_status]}`}>
                  <span className={STATUS_COLORS[team.capacity_status]}>
                    {STATUS_LABELS[team.capacity_status]?.toUpperCase()}
                  </span>
                </span>
                <span className={`px-2 py-0.5 text-[11px] rounded-full font-medium ${ACTION_STYLES[team.capacity_action]}`}>
                  {ACTION_LABELS[team.capacity_action] ?? team.capacity_action}
                </span>
              </div>
            </div>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-2xl leading-none p-1">×</button>
        </div>

        <div className="flex border-b border-slate-800">
          {(["capacity", "pipeline", "metrics"] as const).map((t) => (
            <button key={t} onClick={() => setTab(t)}
              className={`flex-1 py-2.5 text-xs font-semibold capitalize transition-colors ${
                tab === t ? "text-indigo-400 border-b-2 border-indigo-400" : "text-slate-500 hover:text-slate-300"
              }`}>
              {t.charAt(0).toUpperCase() + t.slice(1)}
            </button>
          ))}
        </div>

        <div className="p-5 space-y-4 max-h-80 overflow-y-auto">
          {tab === "capacity" && (
            <>
              <div className="grid grid-cols-2 gap-3">
                <div className="bg-slate-800/50 rounded-lg p-3">
                  <p className="text-slate-500 text-xs mb-0.5">Health</p>
                  <p className={`text-sm font-bold capitalize ${HEALTH_COLORS[team.capacity_health]}`}>{team.capacity_health.replace("_", " ")}</p>
                </div>
                <div className="bg-slate-800/50 rounded-lg p-3">
                  <p className="text-slate-500 text-xs mb-0.5">Hiring Urgency</p>
                  <p className={`text-sm font-bold capitalize ${team.needs_immediate_hire ? "text-rose-400" : "text-slate-300"}`}>
                    {team.hiring_urgency.replace("_", " ")}
                  </p>
                </div>
                <div className="bg-slate-800/50 rounded-lg p-3">
                  <p className="text-slate-500 text-xs mb-0.5">Headcount Gap</p>
                  <p className={`text-sm font-bold ${team.headcount_gap > 0 ? "text-amber-400" : "text-emerald-400"}`}>
                    {team.headcount_gap > 0 ? `+${team.headcount_gap} needed` : "Fully staffed"}
                  </p>
                </div>
                <div className="bg-slate-800/50 rounded-lg p-3">
                  <p className="text-slate-500 text-xs mb-0.5">Quota at Risk</p>
                  <p className={`text-sm font-bold ${team.quota_at_risk > 0 ? "text-rose-400" : "text-emerald-400"}`}>
                    {team.quota_at_risk > 0 ? fmt(team.quota_at_risk) : "None"}
                  </p>
                </div>
              </div>
              <div>
                <div className="flex justify-between text-xs mb-1">
                  <span className="text-slate-400">Effective Capacity</span>
                  <span style={{ color }}>{team.effective_capacity_pct.toFixed(1)}%</span>
                </div>
                <BarMini value={team.effective_capacity_pct} max={150} color={color} />
              </div>
              <div>
                <div className="flex justify-between text-xs mb-1">
                  <span className="text-slate-400">Ramp Impact</span>
                  <span className="text-amber-400">{team.ramp_impact.toFixed(1)}% ramping</span>
                </div>
                <BarMini value={team.ramp_impact} color="#f59e0b" />
              </div>
            </>
          )}
          {tab === "pipeline" && (
            <>
              <div className="grid grid-cols-2 gap-3">
                <div className="bg-slate-800/50 rounded-lg p-3">
                  <p className="text-slate-500 text-xs mb-0.5">Pipeline / Rep</p>
                  <p className="text-white text-sm font-semibold">{fmt(team.pipeline_per_rep)}</p>
                </div>
                <div className="bg-slate-800/50 rounded-lg p-3">
                  <p className="text-slate-500 text-xs mb-0.5">Coverage Ratio</p>
                  <p className={`text-sm font-bold ${team.pipeline_coverage_ratio >= 3 ? "text-emerald-400" : team.pipeline_coverage_ratio >= 2 ? "text-amber-400" : "text-rose-400"}`}>
                    {team.pipeline_coverage_ratio.toFixed(1)}×
                  </p>
                </div>
                <div className="bg-slate-800/50 rounded-lg p-3">
                  <p className="text-slate-500 text-xs mb-0.5">Team Quota</p>
                  <p className="text-white text-sm font-semibold">{fmt(team.total_team_quota)}</p>
                </div>
                <div className="bg-slate-800/50 rounded-lg p-3">
                  <p className="text-slate-500 text-xs mb-0.5">Req. Attainment</p>
                  <p className={`text-sm font-bold ${team.required_attainment > 120 ? "text-rose-400" : team.required_attainment > 100 ? "text-amber-400" : "text-emerald-400"}`}>
                    {team.required_attainment.toFixed(0)}%
                  </p>
                </div>
              </div>
            </>
          )}
          {tab === "metrics" && (
            <>
              <div className="space-y-3">
                {[
                  { label: "Effective Capacity", value: team.effective_capacity_pct, max: 150, color: color },
                  { label: "Productivity Index", value: team.productivity_index, max: 100, color: "#38bdf8" },
                  { label: "Ramp Impact", value: team.ramp_impact, max: 100, color: "#f59e0b" },
                  { label: "Pipeline Coverage", value: team.pipeline_coverage_ratio * 33, max: 100, color: "#8b5cf6" },
                ].map(({ label, value, max, color: c }) => (
                  <div key={label}>
                    <div className="flex justify-between text-xs mb-1">
                      <span className="text-slate-400">{label}</span>
                      <span style={{ color: c }}>{value.toFixed(1)}</span>
                    </div>
                    <BarMini value={value} max={max} color={c} />
                  </div>
                ))}
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
}

// ── Team Card ─────────────────────────────────────────────────────────────────

function TeamCard({ team, onClick }: { team: CapacityTeam; onClick: () => void }) {
  const color = capacityColor(team.effective_capacity_pct);
  return (
    <div
      onClick={onClick}
      className="bg-slate-800/60 border border-slate-700/60 rounded-xl p-4 cursor-pointer hover:border-indigo-500/50 hover:bg-slate-800 transition-all"
    >
      <div className="flex items-start gap-3">
        <CapacityGauge pct={team.effective_capacity_pct} size={60} />
        <div className="flex-1 min-w-0">
          <div className="flex items-start justify-between gap-2">
            <div>
              <h3 className="text-white font-semibold text-sm">{team.region} · {team.segment}</h3>
              <p className="text-slate-500 text-xs">{team.manager_id} · {team.current_reps}/{team.target_reps} reps</p>
            </div>
            <span className={`px-2 py-0.5 text-[10px] rounded-full font-medium flex-shrink-0 ${ACTION_STYLES[team.capacity_action]}`}>
              {ACTION_LABELS[team.capacity_action] ?? team.capacity_action}
            </span>
          </div>
          <div className="flex gap-2 mt-1.5 flex-wrap">
            <span className={`text-[10px] font-semibold uppercase ${STATUS_COLORS[team.capacity_status]}`}>
              {STATUS_LABELS[team.capacity_status]}
            </span>
            <span className="text-slate-600 text-[10px]">·</span>
            <span className={`text-[10px] font-medium ${HEALTH_COLORS[team.capacity_health]}`}>
              {team.capacity_health.replace("_", " ")}
            </span>
            {team.needs_immediate_hire && (
              <>
                <span className="text-slate-600 text-[10px]">·</span>
                <span className="text-rose-400 text-[10px] font-bold">HIRE NOW</span>
              </>
            )}
          </div>
        </div>
      </div>

      <div className="mt-3 space-y-1.5">
        <div>
          <div className="flex justify-between text-[10px] text-slate-500 mb-0.5">
            <span>Productivity Index</span>
            <span className="text-sky-400">{team.productivity_index.toFixed(0)}</span>
          </div>
          <BarMini value={team.productivity_index} color="#38bdf8" />
        </div>
        <div>
          <div className="flex justify-between text-[10px] text-slate-500 mb-0.5">
            <span>Ramp Impact</span>
            <span className="text-amber-400">{team.ramp_impact.toFixed(0)}%</span>
          </div>
          <BarMini value={team.ramp_impact} color="#f59e0b" />
        </div>
      </div>

      <div className="mt-2 flex justify-between text-[10px] text-slate-500">
        <span>Quota risk: <span className={team.quota_at_risk > 0 ? "text-rose-400" : "text-emerald-400"}>{team.quota_at_risk > 0 ? fmt(team.quota_at_risk) : "None"}</span></span>
        <span className={team.headcount_gap > 0 ? "text-amber-400" : "text-slate-500"}>
          {team.headcount_gap > 0 ? `Gap: +${team.headcount_gap}` : "Staffed"}
        </span>
      </div>
    </div>
  );
}

// ── Main Page ─────────────────────────────────────────────────────────────────

export default function SalesCapacityPage() {
  const [data, setData] = useState<{ teams: CapacityTeam[]; summary: Summary } | null>(null);
  const [loading, setLoading] = useState(true);
  const [selected, setSelected] = useState<CapacityTeam | null>(null);
  const [filterStatus, setFilterStatus] = useState<string>("all");
  const [filterRegion, setFilterRegion] = useState<string>("all");

  useEffect(() => {
    async function load() {
        setLoading(true);
        try {
          const params = new URLSearchParams();
          if (filterStatus !== "all") params.set("status", filterStatus);
          if (filterRegion !== "all") params.set("region", filterRegion);
          const res = await fetch(`/api/sales-capacity?${params}`);
          setData(await res.json());
        } finally {
          setLoading(false);
        }
  }
    load();
  }, [filterStatus, filterRegion]);

  const s = data?.summary;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-white">Sales Capacity Intelligence</h1>
        <p className="text-slate-400 text-sm mt-1">Analyze team headcount capacity, hiring urgency, and quota coverage</p>
      </div>

      {s && (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-6">
          {[
            { label: "Avg Capacity", value: `${s.avg_effective_capacity}%`, sub: "effective", color: "text-indigo-400" },
            { label: "Quota at Risk", value: s.total_quota_at_risk >= 1_000_000 ? `$${(s.total_quota_at_risk / 1_000_000).toFixed(1)}M` : `$${(s.total_quota_at_risk / 1_000).toFixed(0)}K`, sub: "total exposed", color: "text-rose-400" },
            { label: "Immediate Hire", value: s.immediate_hire_count, sub: "teams", color: "text-amber-400" },
            { label: "HC Gap", value: `+${s.total_headcount_gap}`, sub: "headcount needed", color: "text-orange-400" },
          ].map(({ label, value, sub, color }) => (
            <div key={label} className="bg-slate-800/60 border border-slate-700/60 rounded-xl p-4">
              <p className="text-slate-500 text-xs mb-1">{label}</p>
              <p className={`text-2xl font-bold ${color}`}>{value}</p>
              <p className="text-slate-600 text-xs">{sub}</p>
            </div>
          ))}
        </div>
      )}

      {s && (
        <div className="bg-slate-800/60 border border-slate-700/60 rounded-xl p-4 mb-6">
          <p className="text-slate-400 text-xs font-semibold uppercase tracking-wider mb-3">Capacity Status Distribution</p>
          <StatusDistBar counts={s.status_counts} />
          <div className="mt-3 grid grid-cols-3 gap-2">
            {[
              { label: "Critical Teams", value: s.critical_count, color: "text-rose-400" },
              { label: "Constrained", value: s.constrained_count, color: "text-amber-400" },
              { label: "Avg Productivity", value: s.avg_productivity_index, color: "text-sky-400" },
            ].map(({ label, value, color }) => (
              <div key={label} className="text-center">
                <p className={`text-lg font-bold ${color}`}>{value}</p>
                <p className="text-slate-500 text-[10px]">{label}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      <div className="flex flex-wrap gap-3 mb-5">
        <div className="flex gap-1 flex-wrap">
          <span className="text-slate-500 text-xs self-center mr-1">Status:</span>
          {["all", "over_capacity", "at_capacity", "under_capacity", "critical_shortage"].map((s) => (
            <button key={s} onClick={() => setFilterStatus(s)}
              className={`px-3 py-1 text-xs rounded-full border transition-colors ${
                filterStatus === s
                  ? "border-indigo-500 bg-indigo-500/20 text-indigo-300"
                  : "border-slate-700 text-slate-400 hover:border-slate-500"
              }`}>
              {s === "all" ? "All" : (STATUS_LABELS[s] ?? s)}
            </button>
          ))}
        </div>
        <div className="flex gap-1 flex-wrap">
          <span className="text-slate-500 text-xs self-center mr-1">Region:</span>
          {["all", "EMEA", "NAMER", "APAC", "LATAM"].map((r) => (
            <button key={r} onClick={() => setFilterRegion(r)}
              className={`px-3 py-1 text-xs rounded-full border transition-colors ${
                filterRegion === r
                  ? "border-violet-500 bg-violet-500/20 text-violet-300"
                  : "border-slate-700 text-slate-400 hover:border-slate-500"
              }`}>
              {r === "all" ? "All" : r}
            </button>
          ))}
        </div>
      </div>

      {loading ? (
        <div className="flex justify-center py-20 text-slate-500">Loading…</div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
          {data?.teams.map((t) => (
            <TeamCard key={t.team_id} team={t} onClick={() => setSelected(t)} />
          ))}
        </div>
      )}

      {selected && <TeamModal team={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
