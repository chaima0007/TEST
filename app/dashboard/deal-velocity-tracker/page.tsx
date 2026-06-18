"use client";

import { useEffect, useState, useCallback } from "react";

// ── types ────────────────────────────────────────────────────────────────────
interface Deal {
  deal_id: string;
  deal_name: string;
  rep_id: string;
  velocity_status: string;
  slip_risk: string;
  deal_momentum: string;
  velocity_action: string;
  stage_progress_score: number;
  activity_velocity_score: number;
  stakeholder_momentum_score: number;
  urgency_alignment_score: number;
  velocity_composite: number;
  days_in_current_stage: number;
  close_date_push_count: number;
  is_on_track: boolean;
  needs_velocity_boost: boolean;
  region: string;
}

interface Summary {
  total: number;
  status_counts: Record<string, number>;
  slip_counts: Record<string, number>;
  momentum_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_velocity_composite: number;
  on_track_count: number;
  boost_needed_count: number;
  avg_stage_progress_score: number;
  avg_activity_velocity_score: number;
  avg_stakeholder_momentum_score: number;
  avg_urgency_alignment_score: number;
}

// ── helpers ──────────────────────────────────────────────────────────────────
const STATUS_COLOR: Record<string, string> = {
  accelerating: "text-emerald-400",
  on_pace:      "text-sky-400",
  decelerating: "text-amber-400",
  stalled:      "text-rose-400",
};
const STATUS_BG: Record<string, string> = {
  accelerating: "bg-emerald-500/20 border-emerald-500/40",
  on_pace:      "bg-sky-500/20 border-sky-500/40",
  decelerating: "bg-amber-500/20 border-amber-500/40",
  stalled:      "bg-rose-500/20 border-rose-500/40",
};
const SLIP_COLOR: Record<string, string> = {
  low:      "text-emerald-400",
  moderate: "text-amber-400",
  high:     "text-orange-400",
  critical: "text-rose-400",
};
const MOMENTUM_ICON: Record<string, string> = {
  strong:   "⚡",
  building: "📈",
  fading:   "📉",
  lost:     "💀",
};

function VelocityRing({ score, color }: { score: number; color: string }) {
  const r = 36, circ = 2 * Math.PI * r;
  const fill = (score / 100) * circ;
  return (
    <svg width={88} height={88} viewBox="0 0 88 88">
      <circle cx={44} cy={44} r={r} fill="none" stroke="#1e293b" strokeWidth={8} />
      <circle
        cx={44} cy={44} r={r} fill="none"
        stroke={color} strokeWidth={8}
        strokeDasharray={`${fill} ${circ}`}
        strokeLinecap="round"
        transform="rotate(-90 44 44)"
      />
      <text x={44} y={49} textAnchor="middle" fill="white" fontSize={14} fontWeight="bold">
        {Math.round(score)}
      </text>
    </svg>
  );
}

function ScoreBar({ label, value, color }: { label: string; value: number; color: string }) {
  return (
    <div>
      <div className="flex justify-between text-xs text-slate-400 mb-1">
        <span>{label}</span><span>{value.toFixed(1)}</span>
      </div>
      <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
        <div className={`h-full rounded-full ${color}`} style={{ width: `${value}%` }} />
      </div>
    </div>
  );
}

function SlipDistBar({ counts }: { counts: Record<string, number> }) {
  const order = ["low", "moderate", "high", "critical"];
  const colors = ["bg-emerald-500", "bg-amber-500", "bg-orange-500", "bg-rose-500"];
  const total = Object.values(counts).reduce((a, b) => a + b, 0) || 1;
  return (
    <div className="flex gap-1 h-3 rounded-full overflow-hidden">
      {order.map((k, i) => (
        <div
          key={k}
          className={colors[i]}
          style={{ width: `${((counts[k] || 0) / total) * 100}%` }}
          title={`${k}: ${counts[k] || 0}`}
        />
      ))}
    </div>
  );
}

// ── DealModal ────────────────────────────────────────────────────────────────
function DealModal({ deal, onClose }: { deal: Deal; onClose: () => void }) {
  const [tab, setTab] = useState<"signals" | "scores" | "actions">("signals");

  useEffect(() => {
    const esc = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", esc);
    return () => window.removeEventListener("keydown", esc);
  }, [onClose]);

  const ringColor =
    deal.velocity_composite >= 70 ? "#10b981"
    : deal.velocity_composite >= 50 ? "#38bdf8"
    : deal.velocity_composite >= 35 ? "#f59e0b"
    : "#f43f5e";

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4"
      onClick={onClose}
    >
      <div
        className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-lg shadow-2xl"
        onClick={(e) => e.stopPropagation()}
      >
        {/* header */}
        <div className="flex items-center gap-4 p-5 border-b border-slate-800">
          <VelocityRing score={deal.velocity_composite} color={ringColor} />
          <div className="flex-1 min-w-0">
            <h2 className="text-white font-bold text-lg truncate">{deal.deal_name}</h2>
            <p className="text-slate-400 text-sm">{deal.rep_id} · {deal.region}</p>
            <div className="flex gap-2 mt-1 flex-wrap">
              <span className={`text-xs px-2 py-0.5 rounded-full border ${STATUS_BG[deal.velocity_status]}`}>
                {deal.velocity_status.replace("_", " ")}
              </span>
              <span className={`text-xs font-semibold ${SLIP_COLOR[deal.slip_risk]}`}>
                {deal.slip_risk.toUpperCase()} RISK
              </span>
              <span className="text-xs text-slate-400">{MOMENTUM_ICON[deal.deal_momentum]} {deal.deal_momentum}</span>
            </div>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl">✕</button>
        </div>

        {/* tabs */}
        <div className="flex border-b border-slate-800">
          {(["signals", "scores", "actions"] as const).map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`flex-1 py-2.5 text-sm font-medium capitalize transition-colors ${
                tab === t ? "text-indigo-400 border-b-2 border-indigo-400" : "text-slate-500 hover:text-slate-300"
              }`}
            >
              {t}
            </button>
          ))}
        </div>

        <div className="p-5 space-y-3">
          {tab === "signals" && (
            <>
              <div className="grid grid-cols-2 gap-3">
                {[
                  ["Days in Stage", deal.days_in_current_stage + "d"],
                  ["Close Date Pushes", deal.close_date_push_count],
                  ["On Track", deal.is_on_track ? "✅ Yes" : "❌ No"],
                  ["Needs Boost", deal.needs_velocity_boost ? "⚠️ Yes" : "✅ No"],
                ].map(([label, value]) => (
                  <div key={label as string} className="bg-slate-800/60 rounded-lg p-3">
                    <div className="text-xs text-slate-400">{label}</div>
                    <div className="text-white font-semibold mt-0.5">{value}</div>
                  </div>
                ))}
              </div>
              <div className="bg-slate-800/60 rounded-lg p-3">
                <div className="text-xs text-slate-400 mb-1">Velocity Composite</div>
                <div className="flex items-center gap-3">
                  <span className="text-2xl font-bold text-white">{deal.velocity_composite.toFixed(1)}</span>
                  <div className="flex-1 h-2 bg-slate-700 rounded-full">
                    <div
                      className="h-full rounded-full"
                      style={{ width: `${deal.velocity_composite}%`, backgroundColor: ringColor }}
                    />
                  </div>
                </div>
              </div>
            </>
          )}

          {tab === "scores" && (
            <div className="space-y-3">
              <ScoreBar label="Stage Progress" value={deal.stage_progress_score} color="bg-indigo-500" />
              <ScoreBar label="Activity Velocity" value={deal.activity_velocity_score} color="bg-violet-500" />
              <ScoreBar label="Stakeholder Momentum" value={deal.stakeholder_momentum_score} color="bg-sky-500" />
              <ScoreBar label="Urgency Alignment" value={deal.urgency_alignment_score} color="bg-amber-500" />
            </div>
          )}

          {tab === "actions" && (
            <div className="space-y-3">
              <div className="bg-indigo-500/10 border border-indigo-500/30 rounded-xl p-4">
                <div className="text-xs text-indigo-400 uppercase tracking-wide mb-1">Recommended Action</div>
                <div className="text-white font-bold text-lg capitalize">
                  {deal.velocity_action.replace(/_/g, " ")}
                </div>
              </div>
              {deal.needs_velocity_boost && (
                <div className="bg-rose-500/10 border border-rose-500/30 rounded-xl p-3 text-sm text-rose-300">
                  ⚡ Velocity boost required — deal momentum at risk
                </div>
              )}
              {deal.close_date_push_count >= 2 && (
                <div className="bg-amber-500/10 border border-amber-500/30 rounded-xl p-3 text-sm text-amber-300">
                  📅 Close date pushed {deal.close_date_push_count}× — review timeline with champion
                </div>
              )}
              {deal.velocity_composite >= 75 && (
                <div className="bg-emerald-500/10 border border-emerald-500/30 rounded-xl p-3 text-sm text-emerald-300">
                  🚀 High velocity deal — protect momentum and accelerate to close
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

// ── DealCard ─────────────────────────────────────────────────────────────────
function DealCard({ deal, onClick }: { deal: Deal; onClick: () => void }) {
  const ringColor =
    deal.velocity_composite >= 70 ? "#10b981"
    : deal.velocity_composite >= 50 ? "#38bdf8"
    : deal.velocity_composite >= 35 ? "#f59e0b"
    : "#f43f5e";

  return (
    <div
      onClick={onClick}
      className="bg-slate-900 border border-slate-800 rounded-xl p-4 cursor-pointer hover:border-indigo-500/50 hover:bg-slate-800/60 transition-all"
    >
      <div className="flex items-center gap-3">
        <VelocityRing score={deal.velocity_composite} color={ringColor} />
        <div className="flex-1 min-w-0">
          <div className="text-white font-semibold truncate">{deal.deal_name}</div>
          <div className="text-slate-400 text-xs">{deal.rep_id} · {deal.region}</div>
          <div className="flex gap-2 mt-1 flex-wrap">
            <span className={`text-xs px-2 py-0.5 rounded-full border ${STATUS_BG[deal.velocity_status]}`}>
              {deal.velocity_status.replace("_", " ")}
            </span>
            <span className={`text-xs font-medium ${SLIP_COLOR[deal.slip_risk]}`}>
              {deal.slip_risk} risk
            </span>
          </div>
        </div>
        <div className="text-right shrink-0">
          <div className="text-xl">{MOMENTUM_ICON[deal.deal_momentum]}</div>
          {deal.needs_velocity_boost && (
            <div className="text-xs text-rose-400 mt-1">⚡ boost</div>
          )}
        </div>
      </div>
      <div className="mt-3 grid grid-cols-2 gap-1 text-xs text-slate-400">
        <span>Stage: {deal.days_in_current_stage}d</span>
        <span>Pushes: {deal.close_date_push_count}</span>
      </div>
    </div>
  );
}

// ── page ─────────────────────────────────────────────────────────────────────
export default function DealVelocityTrackerPage() {
  const [deals, setDeals]       = useState<Deal[]>([]);
  const [summary, setSummary]   = useState<Summary | null>(null);
  const [loading, setLoading]   = useState(true);
  const [selected, setSelected] = useState<Deal | null>(null);
  const [filterStatus, setFilterStatus] = useState("all");
  const [filterSlip,   setFilterSlip]   = useState("all");
  const [filterRegion, setFilterRegion] = useState("all");

  const load = useCallback(async () => {
    setLoading(true);
    const params = new URLSearchParams();
    if (filterStatus !== "all") params.set("status", filterStatus);
    if (filterSlip   !== "all") params.set("slip",   filterSlip);
    if (filterRegion !== "all") params.set("region", filterRegion);
    const res = await fetch(`/api/deal-velocity-tracker?${params}`);
    const data = await res.json();
    setDeals(data.deals);
    setSummary(data.summary);
    setLoading(false);
  }, [filterStatus, filterSlip, filterRegion]);

  useEffect(() => { load(); }, [load]);

  const boostNeeded = deals.filter((d) => d.needs_velocity_boost);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
      <div className="max-w-6xl mx-auto space-y-6">

        {/* header */}
        <div>
          <h1 className="text-2xl font-bold text-white">Deal Velocity Tracker</h1>
          <p className="text-slate-400 text-sm mt-1">
            Measures deal velocity by stage transition speed, activity frequency, and stakeholder momentum
          </p>
        </div>

        {/* rescue alert */}
        {boostNeeded.length > 0 && (
          <div className="bg-rose-500/10 border border-rose-500/30 rounded-xl p-4 flex items-center gap-3">
            <span className="text-2xl">⚡</span>
            <div>
              <div className="text-rose-300 font-semibold">
                {boostNeeded.length} deal{boostNeeded.length > 1 ? "s" : ""} need velocity boost
              </div>
              <div className="text-rose-400/70 text-xs mt-0.5">
                {boostNeeded.map((d) => d.deal_name).join(" · ")}
              </div>
            </div>
          </div>
        )}

        {/* KPI strip */}
        {summary && (
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
            {[
              { label: "Total Deals",       value: summary.total },
              { label: "On Track",          value: summary.on_track_count,     color: "text-emerald-400" },
              { label: "Need Boost",        value: summary.boost_needed_count, color: "text-rose-400" },
              { label: "Avg Composite",     value: summary.avg_velocity_composite.toFixed(1), color: "text-indigo-400" },
            ].map(({ label, value, color }) => (
              <div key={label} className="bg-slate-900 border border-slate-800 rounded-xl p-4">
                <div className="text-xs text-slate-400">{label}</div>
                <div className={`text-2xl font-bold mt-1 ${color ?? "text-white"}`}>{value}</div>
              </div>
            ))}
          </div>
        )}

        {/* slip dist bar */}
        {summary && (
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-400 mb-2">Slip Risk Distribution</div>
            <SlipDistBar counts={summary.slip_counts} />
            <div className="flex gap-4 mt-2 text-xs text-slate-500">
              {["low","moderate","high","critical"].map((k) => (
                <span key={k} className={SLIP_COLOR[k]}>{k}: {summary.slip_counts[k] || 0}</span>
              ))}
            </div>
          </div>
        )}

        {/* filters */}
        <div className="flex flex-wrap gap-2">
          {[
            { label: "All Statuses", val: "all", setter: setFilterStatus, current: filterStatus },
            { label: "Accelerating", val: "accelerating", setter: setFilterStatus, current: filterStatus },
            { label: "On Pace",      val: "on_pace",      setter: setFilterStatus, current: filterStatus },
            { label: "Decelerating", val: "decelerating", setter: setFilterStatus, current: filterStatus },
            { label: "Stalled",      val: "stalled",      setter: setFilterStatus, current: filterStatus },
          ].map(({ label, val, setter, current }) => (
            <button
              key={val}
              onClick={() => setter(val)}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
                current === val
                  ? "bg-indigo-600 text-white"
                  : "bg-slate-800 text-slate-400 hover:text-white"
              }`}
            >
              {label}
            </button>
          ))}
          <select
            value={filterRegion}
            onChange={(e) => setFilterRegion(e.target.value)}
            className="px-3 py-1.5 rounded-lg text-xs bg-slate-800 text-slate-300 border border-slate-700"
          >
            <option value="all">All Regions</option>
            {["NAMER","EMEA","APAC","LATAM"].map((r) => (
              <option key={r} value={r}>{r}</option>
            ))}
          </select>
        </div>

        {/* deals grid */}
        {loading ? (
          <div className="text-slate-400 text-center py-16">Loading deals…</div>
        ) : deals.length === 0 ? (
          <div className="text-slate-500 text-center py-16">No deals match your filters.</div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {deals.map((d) => (
              <DealCard key={d.deal_id} deal={d} onClick={() => setSelected(d)} />
            ))}
          </div>
        )}

        {/* avg score bars */}
        {summary && (
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
            <div className="text-sm font-semibold text-slate-300 mb-4">Average Score Breakdown</div>
            <div className="space-y-3">
              <ScoreBar label="Stage Progress"       value={summary.avg_stage_progress_score}       color="bg-indigo-500" />
              <ScoreBar label="Activity Velocity"    value={summary.avg_activity_velocity_score}    color="bg-violet-500" />
              <ScoreBar label="Stakeholder Momentum" value={summary.avg_stakeholder_momentum_score} color="bg-sky-500" />
              <ScoreBar label="Urgency Alignment"    value={summary.avg_urgency_alignment_score}    color="bg-amber-500" />
            </div>
          </div>
        )}
      </div>

      {selected && <DealModal deal={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
