"use client";

import { useEffect, useState, useCallback } from "react";

interface VelocityRep {
  rep_id: string;
  region: string;
  velocity_risk: string;
  velocity_pattern: string;
  velocity_severity: string;
  recommended_action: string;
  cycle_length_score: number;
  stage_stall_score: number;
  buyer_engagement_score: number;
  late_stage_drag_score: number;
  velocity_composite: number;
  is_velocity_degraded: boolean;
  requires_intervention: boolean;
  estimated_at_risk_deals: number;
  velocity_signal: string;
}

interface Summary {
  total: number;
  risk_counts: Record<string, number>;
  pattern_counts: Record<string, number>;
  severity_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_velocity_composite: number;
  degraded_count: number;
  intervention_count: number;
  avg_cycle_length_score: number;
  avg_stage_stall_score: number;
  avg_buyer_engagement_score: number;
  avg_late_stage_drag_score: number;
  total_estimated_at_risk_deals: number;
}

const RISK_COLORS: Record<string, string> = {
  low:      "text-emerald-400",
  moderate: "text-yellow-400",
  high:     "text-orange-400",
  critical: "text-red-400",
};
const RISK_BG: Record<string, string> = {
  low:      "bg-emerald-400/10 border-emerald-400/30",
  moderate: "bg-yellow-400/10 border-yellow-400/30",
  high:     "bg-orange-400/10 border-orange-400/30",
  critical: "bg-red-400/10 border-red-400/30",
};
const SEV_COLORS: Record<string, string> = {
  healthy:  "text-emerald-400",
  slowing:  "text-yellow-400",
  degraded: "text-orange-400",
  stalled:  "text-red-400",
};
const PATTERN_LABELS: Record<string, string> = {
  none:                    "None",
  stage_progression_stall: "Stage Progression Stall",
  buyer_inactivity:        "Buyer Inactivity",
  approval_bottleneck:     "Approval Bottleneck",
  late_stage_drag:         "Late Stage Drag",
  deal_aging:              "Deal Aging",
};
const ACTION_LABELS: Record<string, string> = {
  no_action:                "No Action",
  cycle_review:             "Cycle Review",
  buyer_re_engagement:      "Buyer Re-Engagement",
  deal_qualification_reset: "Deal Qualification Reset",
  executive_acceleration:   "Executive Acceleration",
};

function CompositeRing({ value }: { value: number }) {
  const r    = 28;
  const circ = 2 * Math.PI * r;
  const fill = Math.min(value / 100, 1) * circ;
  const color = value >= 60 ? "#f87171" : value >= 40 ? "#fb923c" : value >= 20 ? "#facc15" : "#34d399";
  return (
    <svg width="72" height="72" viewBox="0 0 72 72">
      <circle cx="36" cy="36" r={r} fill="none" stroke="#1e293b" strokeWidth="8" />
      <circle cx="36" cy="36" r={r} fill="none" stroke={color} strokeWidth="8"
        strokeDasharray={`${fill} ${circ}`} strokeLinecap="round"
        transform="rotate(-90 36 36)" />
      <text x="36" y="40" textAnchor="middle" fontSize="13" fontWeight="bold" fill={color}>
        {value.toFixed(0)}
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
        <div className={`h-full rounded-full ${color}`} style={{ width: `${Math.min(value, 100)}%` }} />
      </div>
    </div>
  );
}

function DetailModal({ rep, onClose }: { rep: VelocityRep; onClose: () => void }) {
  const [tab, setTab] = useState<"overview" | "scores" | "action">("overview");
  useEffect(() => {
    const handler = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [onClose]);
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm"
      onClick={onClose}>
      <div className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-lg mx-4 shadow-2xl"
        onClick={(e) => e.stopPropagation()}>
        <div className="flex items-start justify-between p-6 border-b border-slate-800">
          <div>
            <div className="flex items-center gap-3 mb-1">
              <span className="text-lg font-bold text-slate-100">{rep.rep_id}</span>
              <span className={`text-xs font-semibold px-2 py-0.5 rounded-full border ${RISK_BG[rep.velocity_risk]}`}>
                {rep.velocity_risk.toUpperCase()}
              </span>
              {rep.is_velocity_degraded && (
                <span className="text-xs font-semibold px-2 py-0.5 rounded-full bg-red-400/10 border border-red-400/30 text-red-400">DEGRADED</span>
              )}
            </div>
            <div className="text-sm text-slate-400">{rep.region} · {PATTERN_LABELS[rep.velocity_pattern]}</div>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-slate-300 text-xl leading-none">✕</button>
        </div>
        <div className="flex border-b border-slate-800">
          {(["overview","scores","action"] as const).map((t) => (
            <button key={t} onClick={() => setTab(t)}
              className={`flex-1 py-2.5 text-sm font-medium capitalize transition-colors ${tab===t ? "text-indigo-400 border-b-2 border-indigo-400" : "text-slate-500 hover:text-slate-300"}`}>
              {t}
            </button>
          ))}
        </div>
        <div className="p-6">
          {tab === "overview" && (
            <div className="space-y-4">
              <div className="flex items-center gap-4">
                <CompositeRing value={rep.velocity_composite} />
                <div>
                  <div className="text-sm text-slate-400">Velocity Composite</div>
                  <div className="text-2xl font-bold text-slate-100">{rep.velocity_composite.toFixed(1)}</div>
                  <div className={`text-sm font-medium ${SEV_COLORS[rep.velocity_severity]}`}>
                    {rep.velocity_severity.charAt(0).toUpperCase() + rep.velocity_severity.slice(1)}
                  </div>
                </div>
              </div>
              <div className="bg-slate-800/50 rounded-xl p-4 text-sm text-slate-300 italic">
                &ldquo;{rep.velocity_signal}&rdquo;
              </div>
              <div className="grid grid-cols-2 gap-3 text-sm">
                <div className="bg-slate-800/50 rounded-xl p-3">
                  <div className="text-slate-400 text-xs mb-1">At-Risk Deals</div>
                  <div className="text-orange-400 font-bold">{rep.estimated_at_risk_deals}</div>
                </div>
                <div className="bg-slate-800/50 rounded-xl p-3">
                  <div className="text-slate-400 text-xs mb-1">Intervention Required</div>
                  <div className={rep.requires_intervention ? "text-red-400 font-bold" : "text-emerald-400 font-bold"}>
                    {rep.requires_intervention ? "Yes" : "No"}
                  </div>
                </div>
              </div>
            </div>
          )}
          {tab === "scores" && (
            <div className="space-y-3">
              <ScoreBar label="Cycle Length"       value={rep.cycle_length_score}      color="bg-yellow-400" />
              <ScoreBar label="Stage Stall"        value={rep.stage_stall_score}       color="bg-orange-400" />
              <ScoreBar label="Buyer Engagement"   value={rep.buyer_engagement_score}  color="bg-purple-400" />
              <ScoreBar label="Late Stage Drag"    value={rep.late_stage_drag_score}   color="bg-red-400" />
              <div className="border-t border-slate-800 pt-3 mt-2">
                <ScoreBar label="Composite"        value={rep.velocity_composite}      color="bg-indigo-400" />
              </div>
            </div>
          )}
          {tab === "action" && (
            <div className="space-y-3">
              <div className="bg-indigo-500/10 border border-indigo-500/30 rounded-xl p-4">
                <div className="text-xs text-indigo-300 mb-1">Recommended Action</div>
                <div className="text-indigo-200 font-semibold">{ACTION_LABELS[rep.recommended_action]}</div>
              </div>
              <div className="grid grid-cols-2 gap-3 text-sm">
                <div className="bg-slate-800/50 rounded-xl p-3">
                  <div className="text-slate-400 text-xs mb-1">Pattern</div>
                  <div className="text-slate-200 text-xs">{PATTERN_LABELS[rep.velocity_pattern]}</div>
                </div>
                <div className="bg-slate-800/50 rounded-xl p-3">
                  <div className="text-slate-400 text-xs mb-1">Severity</div>
                  <div className={SEV_COLORS[rep.velocity_severity]}>
                    {rep.velocity_severity.charAt(0).toUpperCase() + rep.velocity_severity.slice(1)}
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default function SalesCycleVelocityDegradationEnginePage() {
  const [data,       setData]       = useState<{ reps: VelocityRep[]; summary: Summary } | null>(null);
  const [loading,    setLoading]    = useState(true);
  const [riskFilter, setRiskFilter] = useState("all");
  const [patFilter,  setPatFilter]  = useState("all");
  const [selected,   setSelected]   = useState<VelocityRep | null>(null);

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const params = new URLSearchParams();
      if (riskFilter !== "all") params.set("risk", riskFilter);
      if (patFilter  !== "all") params.set("pattern", patFilter);
      const res = await fetch(`/api/sales-cycle-velocity-degradation-engine?${params}`);
      setData(await res.json());
    } finally { setLoading(false); }
  }, [riskFilter, patFilter]);

  useEffect(() => { load(); }, [load]);

  const s = data?.summary;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
      {selected && <DetailModal rep={selected} onClose={() => setSelected(null)} />}

      <div className="max-w-7xl mx-auto space-y-6">
        {/* Header */}
        <div>
          <h1 className="text-2xl font-bold text-slate-100">Sales Cycle Velocity Degradation Engine</h1>
          <p className="text-slate-400 text-sm mt-1">
            Detect lengthening sales cycles before they kill your quarter — stage stalls, buyer inactivity, approval bottlenecks &amp; late-stage drag patterns
          </p>
        </div>

        {/* KPI Strip */}
        {s && (
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {[
              { label: "Total Reps",        value: s.total,                              color: "text-slate-100" },
              { label: "Velocity Degraded", value: s.degraded_count,                    color: "text-red-400" },
              { label: "Need Intervention", value: s.intervention_count,                color: "text-orange-400" },
              { label: "Avg Composite",     value: s.avg_velocity_composite.toFixed(1), color: "text-indigo-400" },
            ].map(({ label, value, color }) => (
              <div key={label} className="bg-slate-900 border border-slate-800 rounded-xl p-4">
                <div className="text-xs text-slate-400 mb-1">{label}</div>
                <div className={`text-2xl font-bold ${color}`}>{value}</div>
              </div>
            ))}
          </div>
        )}

        {/* At-Risk Deals Banner */}
        {s && (
          <div className="bg-red-500/5 border border-red-500/20 rounded-xl p-4 flex items-center justify-between">
            <div>
              <div className="text-xs text-red-300 mb-1">Total At-Risk Deals (Stalled)</div>
              <div className="text-2xl font-bold text-red-400">{s.total_estimated_at_risk_deals} deals</div>
            </div>
            <div className="text-right text-xs text-slate-400 space-y-0.5">
              <div>Avg Cycle Length {s.avg_cycle_length_score.toFixed(1)}</div>
              <div>Avg Stage Stall {s.avg_stage_stall_score.toFixed(1)}</div>
              <div>Avg Buyer Engagement {s.avg_buyer_engagement_score.toFixed(1)}</div>
            </div>
          </div>
        )}

        {/* Distribution bars */}
        {s && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {(
              [
                { title: "By Risk Level", counts: s.risk_counts,    colors: { low:"bg-emerald-400", moderate:"bg-yellow-400", high:"bg-orange-400", critical:"bg-red-400" } as Record<string,string> },
                { title: "By Pattern",    counts: s.pattern_counts, colors: { none:"bg-slate-500", stage_progression_stall:"bg-yellow-400", buyer_inactivity:"bg-blue-400", approval_bottleneck:"bg-purple-400", late_stage_drag:"bg-orange-400", deal_aging:"bg-red-500" } as Record<string,string> },
              ] as Array<{ title: string; counts: Record<string,number>; colors: Record<string,string> }>
            ).map(({ title, counts, colors }) => (
              <div key={title} className="bg-slate-900 border border-slate-800 rounded-xl p-4">
                <div className="text-sm font-semibold text-slate-300 mb-3">{title}</div>
                <div className="space-y-2">
                  {Object.entries(counts).map(([k, v]) => (
                    <div key={k}>
                      <div className="flex justify-between text-xs text-slate-400 mb-1">
                        <span className="capitalize">{k.replace(/_/g," ")}</span><span>{v}</span>
                      </div>
                      <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
                        <div className={`h-full rounded-full ${colors[k] ?? "bg-indigo-400"}`}
                          style={{ width: `${(v / (s?.total || 1)) * 100}%` }} />
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Filters */}
        <div className="flex flex-wrap gap-2">
          {["all","low","moderate","high","critical"].map((r) => (
            <button key={r} onClick={() => setRiskFilter(r)}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium capitalize transition-colors ${riskFilter===r ? "bg-indigo-600 text-white" : "bg-slate-800 text-slate-400 hover:text-slate-200"}`}>
              {r === "all" ? "All Risks" : r}
            </button>
          ))}
          <span className="w-px bg-slate-700" />
          {["all","stage_progression_stall","buyer_inactivity","approval_bottleneck","late_stage_drag","deal_aging"].map((p) => (
            <button key={p} onClick={() => setPatFilter(p)}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium capitalize transition-colors ${patFilter===p ? "bg-violet-600 text-white" : "bg-slate-800 text-slate-400 hover:text-slate-200"}`}>
              {p === "all" ? "All Patterns" : p.replace(/_/g," ")}
            </button>
          ))}
        </div>

        {/* Rep Cards */}
        {loading ? (
          <div className="text-center text-slate-500 py-16">Loading…</div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
            {data?.reps.map((rep) => (
              <button key={rep.rep_id} onClick={() => setSelected(rep)}
                className="bg-slate-900 border border-slate-800 rounded-xl p-4 text-left hover:border-slate-600 transition-colors group">
                <div className="flex items-start justify-between mb-3">
                  <div>
                    <div className="flex items-center gap-2 mb-0.5">
                      <span className="font-semibold text-slate-100">{rep.rep_id}</span>
                      {rep.is_velocity_degraded && (
                        <span className="text-xs bg-red-400/10 border border-red-400/30 text-red-400 px-1.5 py-0.5 rounded-full">DEGRADED</span>
                      )}
                    </div>
                    <div className="text-xs text-slate-400">{rep.region}</div>
                  </div>
                  <CompositeRing value={rep.velocity_composite} />
                </div>

                <div className="flex flex-wrap gap-1.5 mb-3">
                  <span className={`text-xs px-2 py-0.5 rounded-full border font-medium ${RISK_BG[rep.velocity_risk]} ${RISK_COLORS[rep.velocity_risk]}`}>
                    {rep.velocity_risk}
                  </span>
                  <span className={`text-xs font-medium ${SEV_COLORS[rep.velocity_severity]}`}>
                    {rep.velocity_severity}
                  </span>
                </div>

                <div className="text-xs text-slate-400 italic line-clamp-2 mb-3">&ldquo;{rep.velocity_signal}&rdquo;</div>

                <div className="grid grid-cols-2 gap-2 text-xs">
                  <div className="bg-slate-800/50 rounded-lg p-2">
                    <div className="text-slate-500 mb-0.5">Pattern</div>
                    <div className="text-slate-300 truncate">{PATTERN_LABELS[rep.velocity_pattern]}</div>
                  </div>
                  <div className="bg-slate-800/50 rounded-lg p-2">
                    <div className="text-slate-500 mb-0.5">At-Risk Deals</div>
                    <div className="text-orange-400 font-medium">{rep.estimated_at_risk_deals}</div>
                  </div>
                </div>

                {rep.requires_intervention && (
                  <div className="mt-2 text-xs bg-amber-500/10 border border-amber-500/20 text-amber-400 rounded-lg px-2 py-1 text-center">
                    Intervention Required
                  </div>
                )}
              </button>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
