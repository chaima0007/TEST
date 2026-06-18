"use client";

import { useEffect, useState, useCallback } from "react";

interface CompRep {
  rep_id: string;
  region: string;
  comp_risk: string;
  comp_pattern: string;
  comp_severity: string;
  recommended_action: string;
  timing_manipulation_score: number;
  discount_behavior_score: number;
  quota_gaming_score: number;
  strategic_alignment_score: number;
  comp_risk_composite: number;
  is_comp_misaligned: boolean;
  requires_immediate_review: boolean;
  estimated_margin_impact_pct: number;
  comp_signal: string;
}

interface Summary {
  total: number;
  risk_counts: Record<string, number>;
  pattern_counts: Record<string, number>;
  severity_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_comp_risk_composite: number;
  misaligned_count: number;
  immediate_review_count: number;
  avg_timing_manipulation_score: number;
  avg_discount_behavior_score: number;
  avg_quota_gaming_score: number;
  avg_strategic_alignment_score: number;
  avg_estimated_margin_impact_pct: number;
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
  aligned:    "text-emerald-400",
  watch:      "text-yellow-400",
  misaligned: "text-orange-400",
  exploiting: "text-red-400",
};
const PATTERN_LABELS: Record<string, string> = {
  none:                     "None",
  quarter_end_dumping:      "Quarter-End Dumping",
  discount_abuse:           "Discount Abuse",
  quota_ratchet_gaming:     "Quota Ratchet Gaming",
  cherry_picking:           "Cherry Picking",
  accelerator_exploitation: "Accelerator Exploitation",
};
const ACTION_LABELS: Record<string, string> = {
  no_action:            "No Action",
  comp_plan_review:     "Comp Plan Review",
  deal_desk_escalation: "Deal Desk Escalation",
  quota_recalibration:  "Quota Recalibration",
  plan_redesign:        "Plan Redesign",
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

function DetailModal({ rep, onClose }: { rep: CompRep; onClose: () => void }) {
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
              <span className={`text-xs font-semibold px-2 py-0.5 rounded-full border ${RISK_BG[rep.comp_risk]}`}>
                {rep.comp_risk.toUpperCase()}
              </span>
              {rep.is_comp_misaligned && (
                <span className="text-xs font-semibold px-2 py-0.5 rounded-full bg-red-400/10 border border-red-400/30 text-red-400">MISALIGNED</span>
              )}
            </div>
            <div className="text-sm text-slate-400">{rep.region} · {PATTERN_LABELS[rep.comp_pattern]}</div>
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
                <CompositeRing value={rep.comp_risk_composite} />
                <div>
                  <div className="text-sm text-slate-400">Comp Risk Composite</div>
                  <div className="text-2xl font-bold text-slate-100">{rep.comp_risk_composite.toFixed(1)}</div>
                  <div className={`text-sm font-medium ${SEV_COLORS[rep.comp_severity]}`}>
                    {rep.comp_severity.charAt(0).toUpperCase() + rep.comp_severity.slice(1)}
                  </div>
                </div>
              </div>
              <div className="bg-slate-800/50 rounded-xl p-4 text-sm text-slate-300 italic">
                &ldquo;{rep.comp_signal}&rdquo;
              </div>
              <div className="grid grid-cols-2 gap-3 text-sm">
                <div className="bg-slate-800/50 rounded-xl p-3">
                  <div className="text-slate-400 text-xs mb-1">Margin Impact</div>
                  <div className="text-orange-400 font-bold">{rep.estimated_margin_impact_pct.toFixed(2)}pp</div>
                </div>
                <div className="bg-slate-800/50 rounded-xl p-3">
                  <div className="text-slate-400 text-xs mb-1">Immediate Review</div>
                  <div className={rep.requires_immediate_review ? "text-red-400 font-bold" : "text-emerald-400 font-bold"}>
                    {rep.requires_immediate_review ? "Yes" : "No"}
                  </div>
                </div>
              </div>
            </div>
          )}
          {tab === "scores" && (
            <div className="space-y-3">
              <ScoreBar label="Timing Manipulation"  value={rep.timing_manipulation_score}  color="bg-yellow-400" />
              <ScoreBar label="Discount Behavior"    value={rep.discount_behavior_score}    color="bg-orange-400" />
              <ScoreBar label="Quota Gaming"         value={rep.quota_gaming_score}         color="bg-red-400" />
              <ScoreBar label="Strategic Alignment"  value={rep.strategic_alignment_score}  color="bg-purple-400" />
              <div className="border-t border-slate-800 pt-3 mt-2">
                <ScoreBar label="Composite"          value={rep.comp_risk_composite}        color="bg-indigo-400" />
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
                  <div className="text-slate-200 text-xs">{PATTERN_LABELS[rep.comp_pattern]}</div>
                </div>
                <div className="bg-slate-800/50 rounded-xl p-3">
                  <div className="text-slate-400 text-xs mb-1">Severity</div>
                  <div className={SEV_COLORS[rep.comp_severity]}>
                    {rep.comp_severity.charAt(0).toUpperCase() + rep.comp_severity.slice(1)}
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

export default function SalesIncentiveCompensationRiskEnginePage() {
  const [data,       setData]       = useState<{ reps: CompRep[]; summary: Summary } | null>(null);
  const [loading,    setLoading]    = useState(true);
  const [riskFilter, setRiskFilter] = useState("all");
  const [patFilter,  setPatFilter]  = useState("all");
  const [selected,   setSelected]   = useState<CompRep | null>(null);

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const params = new URLSearchParams();
      if (riskFilter !== "all") params.set("risk", riskFilter);
      if (patFilter  !== "all") params.set("pattern", patFilter);
      const res = await fetch(`/api/sales-incentive-compensation-risk-engine?${params}`);
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
          <h1 className="text-2xl font-bold text-slate-100">Sales Incentive Compensation Risk Engine</h1>
          <p className="text-slate-400 text-sm mt-1">
            Detect perverse incentive behavior — quarter-end dumping, discount abuse, quota ratchet gaming, cherry picking &amp; accelerator exploitation
          </p>
        </div>

        {/* KPI Strip */}
        {s && (
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {[
              { label: "Total Reps",       value: s.total,                              color: "text-slate-100" },
              { label: "Comp Misaligned",  value: s.misaligned_count,                  color: "text-red-400" },
              { label: "Immediate Review", value: s.immediate_review_count,            color: "text-orange-400" },
              { label: "Avg Composite",    value: s.avg_comp_risk_composite.toFixed(1), color: "text-indigo-400" },
            ].map(({ label, value, color }) => (
              <div key={label} className="bg-slate-900 border border-slate-800 rounded-xl p-4">
                <div className="text-xs text-slate-400 mb-1">{label}</div>
                <div className={`text-2xl font-bold ${color}`}>{value}</div>
              </div>
            ))}
          </div>
        )}

        {/* Margin Impact Banner */}
        {s && (
          <div className="bg-red-500/5 border border-red-500/20 rounded-xl p-4 flex items-center justify-between">
            <div>
              <div className="text-xs text-red-300 mb-1">Avg Estimated Margin Impact</div>
              <div className="text-2xl font-bold text-red-400">{s.avg_estimated_margin_impact_pct.toFixed(2)}pp</div>
            </div>
            <div className="text-right text-xs text-slate-400 space-y-0.5">
              <div>Avg Timing Manip. {s.avg_timing_manipulation_score.toFixed(1)}</div>
              <div>Avg Discount Behavior {s.avg_discount_behavior_score.toFixed(1)}</div>
              <div>Avg Quota Gaming {s.avg_quota_gaming_score.toFixed(1)}</div>
            </div>
          </div>
        )}

        {/* Distribution bars */}
        {s && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {(
              [
                { title: "By Risk Level", counts: s.risk_counts,    colors: { low:"bg-emerald-400", moderate:"bg-yellow-400", high:"bg-orange-400", critical:"bg-red-400" } as Record<string,string> },
                { title: "By Pattern",    counts: s.pattern_counts, colors: { none:"bg-slate-500", quarter_end_dumping:"bg-yellow-400", discount_abuse:"bg-orange-400", quota_ratchet_gaming:"bg-purple-400", cherry_picking:"bg-blue-400", accelerator_exploitation:"bg-red-500" } as Record<string,string> },
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
          {["all","quarter_end_dumping","discount_abuse","quota_ratchet_gaming","cherry_picking","accelerator_exploitation"].map((p) => (
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
                      {rep.is_comp_misaligned && (
                        <span className="text-xs bg-red-400/10 border border-red-400/30 text-red-400 px-1.5 py-0.5 rounded-full">MISALIGNED</span>
                      )}
                    </div>
                    <div className="text-xs text-slate-400">{rep.region}</div>
                  </div>
                  <CompositeRing value={rep.comp_risk_composite} />
                </div>

                <div className="flex flex-wrap gap-1.5 mb-3">
                  <span className={`text-xs px-2 py-0.5 rounded-full border font-medium ${RISK_BG[rep.comp_risk]} ${RISK_COLORS[rep.comp_risk]}`}>
                    {rep.comp_risk}
                  </span>
                  <span className={`text-xs font-medium ${SEV_COLORS[rep.comp_severity]}`}>
                    {rep.comp_severity}
                  </span>
                </div>

                <div className="text-xs text-slate-400 italic line-clamp-2 mb-3">&ldquo;{rep.comp_signal}&rdquo;</div>

                <div className="grid grid-cols-2 gap-2 text-xs">
                  <div className="bg-slate-800/50 rounded-lg p-2">
                    <div className="text-slate-500 mb-0.5">Pattern</div>
                    <div className="text-slate-300 truncate">{PATTERN_LABELS[rep.comp_pattern]}</div>
                  </div>
                  <div className="bg-slate-800/50 rounded-lg p-2">
                    <div className="text-slate-500 mb-0.5">Margin Impact</div>
                    <div className="text-orange-400 font-medium">{rep.estimated_margin_impact_pct.toFixed(2)}pp</div>
                  </div>
                </div>

                {rep.requires_immediate_review && (
                  <div className="mt-2 text-xs bg-red-500/10 border border-red-500/20 text-red-400 rounded-lg px-2 py-1 text-center">
                    Immediate Review Required
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
