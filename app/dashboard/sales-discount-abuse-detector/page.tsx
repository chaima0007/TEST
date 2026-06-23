"use client";

import { useEffect, useState } from "react";

interface DiscountRep {
  rep_id: string;
  region: string;
  discount_risk: string;
  discount_pattern: string;
  discount_severity: string;
  recommended_action: string;
  policy_violation_score: number;
  revenue_impact_score: number;
  behavioral_pattern_score: number;
  dependency_score: number;
  discount_composite: number;
  is_abusing_discounts: boolean;
  requires_manager_review: boolean;
  estimated_margin_loss_usd: number;
  discount_signal: string;
}

interface Summary {
  total: number;
  risk_counts: Record<string, number>;
  pattern_counts: Record<string, number>;
  severity_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_discount_composite: number;
  abusing_count: number;
  review_required_count: number;
  avg_policy_violation_score: number;
  avg_revenue_impact_score: number;
  avg_behavioral_pattern_score: number;
  avg_dependency_score: number;
  total_estimated_margin_loss_usd: number;
}

const RISK_COLORS: Record<string, string> = {
  low:      "text-emerald-400",
  moderate: "text-amber-400",
  high:     "text-orange-400",
  critical: "text-red-400",
};

const RISK_BG: Record<string, string> = {
  low:      "bg-emerald-500/20 border-emerald-500/40",
  moderate: "bg-amber-500/20 border-amber-500/40",
  high:     "bg-orange-500/20 border-orange-500/40",
  critical: "bg-red-500/20 border-red-500/40",
};

const PATTERN_COLORS: Record<string, string> = {
  none:                 "text-slate-400",
  policy_breach:        "text-amber-400",
  habitual_discounting: "text-orange-400",
  dependency_pattern:   "text-red-400",
  unauthorized:         "text-red-500",
  margin_destruction:   "text-rose-400",
};

const SEVERITY_BADGE: Record<string, string> = {
  clean:      "bg-emerald-500/10 text-emerald-300",
  watch:      "bg-amber-500/10 text-amber-300",
  concerning: "bg-orange-500/10 text-orange-300",
  abusive:    "bg-red-500/10 text-red-300",
};

const ACTION_BADGE: Record<string, string> = {
  no_action:           "bg-slate-700 text-slate-300",
  flag_for_review:     "bg-sky-500/20 text-sky-300",
  manager_approval:    "bg-amber-500/20 text-amber-300",
  discount_freeze:     "bg-orange-500/20 text-orange-300",
  compensation_review: "bg-red-700/40 text-red-200 border border-red-500/50",
};

function CompositeRing({ value }: { value: number }) {
  const r = 28;
  const circ = 2 * Math.PI * r;
  const fill = (value / 100) * circ;
  const color = value >= 60 ? "#ef4444" : value >= 40 ? "#f97316" : value >= 20 ? "#f59e0b" : "#10b981";
  return (
    <svg width="72" height="72" viewBox="0 0 72 72">
      <circle cx="36" cy="36" r={r} fill="none" stroke="#1e293b" strokeWidth="6" />
      <circle cx="36" cy="36" r={r} fill="none" stroke={color} strokeWidth="6"
        strokeDasharray={`${fill} ${circ}`} strokeLinecap="round"
        transform="rotate(-90 36 36)" />
      <text x="36" y="40" textAnchor="middle" fill={color} fontSize="13" fontWeight="bold">{value.toFixed(0)}</text>
    </svg>
  );
}

function ScoreBar({ label, value, color }: { label: string; value: number; color: string }) {
  return (
    <div>
      <div className="flex justify-between text-xs mb-1">
        <span className="text-slate-400">{label}</span>
        <span className={color}>{value.toFixed(1)}</span>
      </div>
      <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
        <div className={`h-full rounded-full ${color.replace("text-", "bg-")}`}
          style={{ width: `${Math.min(value, 100)}%` }} />
      </div>
    </div>
  );
}

function fmt(n: number) {
  return n >= 1_000_000 ? `$${(n / 1_000_000).toFixed(1)}M`
       : n >= 1_000     ? `$${(n / 1_000).toFixed(0)}K`
       : `$${n.toFixed(0)}`;
}

function DetailModal({ rep, onClose }: { rep: DiscountRep; onClose: () => void }) {
  const [tab, setTab] = useState<"overview" | "scores" | "action">("overview");

  useEffect(() => {
    const handler = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [onClose]);

  const tabs = [
    { id: "overview" as const, label: "Overview" },
    { id: "scores"   as const, label: "Risk Scores" },
    { id: "action"   as const, label: "Action" },
  ];

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4"
      onClick={onClose}>
      <div className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-lg shadow-2xl"
        onClick={(e) => e.stopPropagation()}>
        <div className="p-6 border-b border-slate-800">
          <div className="flex items-start justify-between gap-4">
            <div>
              <p className="text-xs text-slate-500 mb-1">{rep.rep_id} · {rep.region}</p>
              <h2 className="text-lg font-bold text-white">{rep.rep_id}</h2>
              <div className="flex items-center gap-2 mt-2 flex-wrap">
                <span className={`text-xs px-2 py-0.5 rounded-full border ${RISK_BG[rep.discount_risk]}`}>
                  {rep.discount_risk.toUpperCase()} RISK
                </span>
                <span className={`text-xs px-2 py-0.5 rounded-full ${SEVERITY_BADGE[rep.discount_severity]}`}>
                  {rep.discount_severity}
                </span>
              </div>
            </div>
            <CompositeRing value={rep.discount_composite} />
          </div>
        </div>

        <div className="flex border-b border-slate-800">
          {tabs.map((t) => (
            <button key={t.id} onClick={() => setTab(t.id)}
              className={`flex-1 py-3 text-xs font-medium transition-colors ${
                tab === t.id ? "text-indigo-400 border-b-2 border-indigo-400" : "text-slate-500 hover:text-slate-300"
              }`}>
              {t.label}
            </button>
          ))}
        </div>

        <div className="p-6">
          {tab === "overview" && (
            <div className="space-y-4">
              <div className="grid grid-cols-2 gap-3">
                <div className="bg-slate-800/60 rounded-lg p-3">
                  <p className="text-xs text-slate-500">Pattern</p>
                  <p className={`text-sm font-semibold mt-1 ${PATTERN_COLORS[rep.discount_pattern]}`}>
                    {rep.discount_pattern.replace(/_/g, " ")}
                  </p>
                </div>
                <div className="bg-slate-800/60 rounded-lg p-3">
                  <p className="text-xs text-slate-500">Est. Margin Loss</p>
                  <p className="text-sm font-semibold mt-1 text-red-400">
                    {fmt(rep.estimated_margin_loss_usd)}
                  </p>
                </div>
                <div className="bg-slate-800/60 rounded-lg p-3">
                  <p className="text-xs text-slate-500">Abusing</p>
                  <p className={`text-sm font-semibold mt-1 ${rep.is_abusing_discounts ? "text-red-400" : "text-emerald-400"}`}>
                    {rep.is_abusing_discounts ? "Yes" : "No"}
                  </p>
                </div>
                <div className="bg-slate-800/60 rounded-lg p-3">
                  <p className="text-xs text-slate-500">Manager Review</p>
                  <p className={`text-sm font-semibold mt-1 ${rep.requires_manager_review ? "text-orange-400" : "text-emerald-400"}`}>
                    {rep.requires_manager_review ? "Required" : "Not needed"}
                  </p>
                </div>
              </div>
              <div className="bg-slate-800/40 rounded-lg p-3 border-l-2 border-amber-500">
                <p className="text-xs text-slate-400 italic">{rep.discount_signal}</p>
              </div>
            </div>
          )}

          {tab === "scores" && (
            <div className="space-y-3">
              <ScoreBar label="Policy Violation"   value={rep.policy_violation_score}   color="text-red-400" />
              <ScoreBar label="Revenue Impact"     value={rep.revenue_impact_score}     color="text-orange-400" />
              <ScoreBar label="Behavioral Pattern" value={rep.behavioral_pattern_score} color="text-amber-400" />
              <ScoreBar label="Dependency"         value={rep.dependency_score}         color="text-violet-400" />
              <div className="pt-2 border-t border-slate-800">
                <div className="flex justify-between text-sm">
                  <span className="text-slate-400 font-medium">Discount Composite</span>
                  <span className="text-white font-bold">{rep.discount_composite.toFixed(1)}</span>
                </div>
                <p className="text-xs text-slate-600 mt-1">policy×0.35 + revenue×0.30 + behavioral×0.20 + dependency×0.15</p>
              </div>
            </div>
          )}

          {tab === "action" && (
            <div className="space-y-4">
              <div className={`rounded-xl p-4 border ${RISK_BG[rep.discount_risk]}`}>
                <p className="text-xs text-slate-400 mb-1">Recommended Action</p>
                <p className={`text-xl font-bold ${RISK_COLORS[rep.discount_risk]}`}>
                  {rep.recommended_action.replace(/_/g, " ").toUpperCase()}
                </p>
              </div>
              <div className="bg-slate-800/40 rounded-lg p-3 space-y-2">
                <div className="flex justify-between text-xs">
                  <span className="text-slate-400">Severity</span>
                  <span className={SEVERITY_BADGE[rep.discount_severity].split(" ")[1]}>{rep.discount_severity}</span>
                </div>
                <div className="flex justify-between text-xs">
                  <span className="text-slate-400">Composite</span>
                  <span className="text-white">{rep.discount_composite.toFixed(1)} / 100</span>
                </div>
                <div className="flex justify-between text-xs">
                  <span className="text-slate-400">Est. Margin Loss</span>
                  <span className="text-red-400">{fmt(rep.estimated_margin_loss_usd)}</span>
                </div>
              </div>
            </div>
          )}
        </div>

        <div className="px-6 pb-6">
          <button onClick={onClose}
            className="w-full py-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 text-sm transition-colors">
            Close
          </button>
        </div>
      </div>
    </div>
  );
}

export default function SalesDiscountAbusePage() {
  const [data, setData]       = useState<{ reps: DiscountRep[]; summary: Summary } | null>(null);
  const [loading, setLoading] = useState(true);
  const [riskFilter, setRiskFilter]       = useState<string>("");
  const [patternFilter, setPatternFilter] = useState<string>("");
  const [selected, setSelected] = useState<DiscountRep | null>(null);

  useEffect(() => {
    async function load() {
        setLoading(true);
        const params = new URLSearchParams();
        if (riskFilter)    params.set("risk",    riskFilter);
        if (patternFilter) params.set("pattern", patternFilter);
        const res  = await fetch(`/api/sales-discount-abuse-detector?${params}`);
        const json = await res.json();
        setData(json);
        setLoading(false);
  }
    load();
  }, [riskFilter, patternFilter]);

  const s    = data?.summary;
  const reps = data?.reps ?? [];
  const riskLevels   = ["low", "moderate", "high", "critical"];
  const patternTypes = ["none", "policy_breach", "habitual_discounting", "dependency_pattern", "unauthorized", "margin_destruction"];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
      <div className="max-w-7xl mx-auto space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white">Sales Discount Abuse Detector</h1>
          <p className="text-slate-400 text-sm mt-1">
            Identifies reps who systematically over-discount to close deals at the expense of margin and revenue quality
          </p>
        </div>

        {s && (
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {[
              { label: "Total Reps",        value: s.total,                 sub: "analyzed" },
              { label: "Abusing",           value: s.abusing_count,        sub: "confirmed" },
              { label: "Manager Review",    value: s.review_required_count,sub: "required" },
              { label: "Est. Margin Loss",  value: fmt(s.total_estimated_margin_loss_usd), sub: "at risk" },
            ].map((k) => (
              <div key={k.label} className="bg-slate-900 border border-slate-800 rounded-xl p-4">
                <p className="text-xs text-slate-500">{k.label}</p>
                <p className="text-2xl font-bold text-white mt-1">{k.value}</p>
                <p className="text-xs text-slate-600 mt-0.5">{k.sub}</p>
              </div>
            ))}
          </div>
        )}

        {s && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
              <h2 className="text-sm font-semibold text-slate-300 mb-4">Average Risk Sub-Scores</h2>
              <div className="space-y-3">
                {[
                  { label: "Policy Violation",   value: s.avg_policy_violation_score,   color: "text-red-400" },
                  { label: "Revenue Impact",     value: s.avg_revenue_impact_score,     color: "text-orange-400" },
                  { label: "Behavioral Pattern", value: s.avg_behavioral_pattern_score, color: "text-amber-400" },
                  { label: "Dependency",         value: s.avg_dependency_score,         color: "text-violet-400" },
                ].map((item) => (
                  <ScoreBar key={item.label} label={item.label} value={item.value} color={item.color} />
                ))}
              </div>
            </div>

            <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
              <h2 className="text-sm font-semibold text-slate-300 mb-4">Pattern Distribution</h2>
              <div className="space-y-2">
                {patternTypes.filter((p) => s.pattern_counts[p]).map((p) => {
                  const count = s.pattern_counts[p] || 0;
                  const pct   = (count / s.total) * 100;
                  return (
                    <div key={p}>
                      <div className="flex justify-between text-xs mb-1">
                        <span className={PATTERN_COLORS[p]}>{p.replace(/_/g, " ")}</span>
                        <span className="text-slate-400">{count}</span>
                      </div>
                      <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
                        <div className={`h-full rounded-full ${(PATTERN_COLORS[p] || "text-slate-400").replace("text-", "bg-")}`}
                          style={{ width: `${pct}%` }} />
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          </div>
        )}

        <div className="flex flex-wrap gap-3">
          <div>
            <p className="text-xs text-slate-500 mb-1">Risk Level</p>
            <div className="flex flex-wrap gap-1">
              {["", ...riskLevels].map((r) => (
                <button key={r || "all"} onClick={() => setRiskFilter(r)}
                  className={`px-3 py-1 rounded-full text-xs transition-colors ${
                    riskFilter === r ? "bg-indigo-600 text-white" : "bg-slate-800 text-slate-400 hover:bg-slate-700"
                  }`}>
                  {r || "All"}
                </button>
              ))}
            </div>
          </div>
          <div>
            <p className="text-xs text-slate-500 mb-1">Pattern</p>
            <div className="flex flex-wrap gap-1">
              {["", ...patternTypes].map((p) => (
                <button key={p || "all"} onClick={() => setPatternFilter(p)}
                  className={`px-3 py-1 rounded-full text-xs transition-colors ${
                    patternFilter === p ? "bg-indigo-600 text-white" : "bg-slate-800 text-slate-400 hover:bg-slate-700"
                  }`}>
                  {p ? p.replace(/_/g, " ") : "All"}
                </button>
              ))}
            </div>
          </div>
        </div>

        {loading ? (
          <div className="flex items-center justify-center h-40">
            <div className="w-8 h-8 border-2 border-indigo-500 border-t-transparent rounded-full animate-spin" />
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
            {reps.map((rep) => (
              <button key={rep.rep_id} onClick={() => setSelected(rep)} className="text-left w-full">
                <div className={`bg-slate-900 border rounded-xl p-4 hover:border-indigo-500 transition-colors cursor-pointer ${
                  rep.is_abusing_discounts ? "border-orange-500/40" : "border-slate-800"
                }`}>
                  <div className="flex items-start justify-between gap-3 mb-3">
                    <div className="min-w-0">
                      <div className="flex items-center gap-2 flex-wrap mb-1">
                        <span className={`text-xs px-2 py-0.5 rounded-full border ${RISK_BG[rep.discount_risk]}`}>
                          {rep.discount_risk}
                        </span>
                        <span className={`text-xs ${PATTERN_COLORS[rep.discount_pattern]}`}>
                          {rep.discount_pattern.replace(/_/g, " ")}
                        </span>
                      </div>
                      <p className="text-sm font-semibold text-white">{rep.rep_id}</p>
                      <p className="text-xs text-slate-500">{rep.region}</p>
                    </div>
                    <CompositeRing value={rep.discount_composite} />
                  </div>

                  <div className="space-y-1.5 mb-3">
                    <ScoreBar label="Policy"     value={rep.policy_violation_score}   color="text-red-400" />
                    <ScoreBar label="Revenue"    value={rep.revenue_impact_score}     color="text-orange-400" />
                    <ScoreBar label="Behavioral" value={rep.behavioral_pattern_score} color="text-amber-400" />
                    <ScoreBar label="Dependency" value={rep.dependency_score}         color="text-violet-400" />
                  </div>

                  <div className="flex items-center justify-between mb-2">
                    <span className={`text-xs px-2 py-0.5 rounded-full ${ACTION_BADGE[rep.recommended_action]}`}>
                      {rep.recommended_action.replace(/_/g, " ")}
                    </span>
                    <span className={`text-xs px-2 py-0.5 rounded-full ${SEVERITY_BADGE[rep.discount_severity]}`}>
                      {rep.discount_severity}
                    </span>
                  </div>

                  {rep.estimated_margin_loss_usd > 0 && (
                    <div className="text-xs text-red-400 font-medium">
                      Est. margin loss: {fmt(rep.estimated_margin_loss_usd)}
                    </div>
                  )}
                </div>
              </button>
            ))}
          </div>
        )}
      </div>

      {selected && <DetailModal rep={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
