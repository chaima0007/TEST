"use client";

import { useState, useEffect } from "react";

// ── Types ─────────────────────────────────────────────────────────────────────

interface DealData {
  deal_id: string;
  deal_name: string;
  rep_id: string;
  stage: string;
  region: string;
  fragmentation_risk: string;
  fragmentation_pattern: string;
  deal_prognosis: string;
  recommended_action: string;
  champion_risk_score: number;
  engagement_decay_score: number;
  scope_erosion_score: number;
  timeline_drift_score: number;
  fragmentation_composite_score: number;
  estimated_deal_at_risk: number;
  recovery_probability: number;
  is_fragmenting: boolean;
  needs_immediate_intervention: boolean;
  deal_value: number;
  initial_deal_value: number;
  days_in_current_stage: number;
  close_date_pushed_times: number;
  champion_last_active_days: number;
  stage_regression_count: number;
}

interface Summary {
  total: number;
  risk_counts: Record<string, number>;
  pattern_counts: Record<string, number>;
  prognosis_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_fragmentation_composite_score: number;
  total_estimated_deal_at_risk: number;
  fragmenting_count: number;
  intervention_needed_count: number;
  avg_champion_risk_score: number;
  avg_engagement_decay_score: number;
  avg_scope_erosion_score: number;
  avg_recovery_probability: number;
}

// ── Helpers ───────────────────────────────────────────────────────────────────

const RISK_COLOR: Record<string, string> = {
  stable:       "text-emerald-400",
  early_signal: "text-amber-400",
  at_risk:      "text-orange-400",
  fragmenting:  "text-red-400",
};

const RISK_BG: Record<string, string> = {
  stable:       "bg-slate-800/60 border-slate-700/40",
  early_signal: "bg-amber-900/30 border-amber-700/40",
  at_risk:      "bg-orange-900/30 border-orange-700/40",
  fragmenting:  "bg-red-900/30 border-red-700/40",
};

const ACTION_BADGE: Record<string, string> = {
  maintain:   "bg-slate-800 text-slate-400 border-slate-700",
  re_engage:  "bg-amber-900/50 text-amber-300 border-amber-700/50",
  rescue:     "bg-orange-900/50 text-orange-300 border-orange-700/50",
  escalate:   "bg-red-900/50 text-red-300 border-red-700/50",
};

const PROGNOSIS_COLOR: Record<string, string> = {
  on_track:       "text-emerald-400",
  needs_attention: "text-amber-400",
  likely_slip:    "text-orange-400",
  at_risk_lost:   "text-red-400",
};

function fmt$(v: number) {
  return v >= 1_000_000
    ? `$${(v / 1_000_000).toFixed(1)}M`
    : v >= 1_000
    ? `$${(v / 1_000).toFixed(0)}K`
    : `$${v.toFixed(0)}`;
}

// ── FragmentationRadar (4-axis bar) ───────────────────────────────────────────

function FragmentationBars({ deal }: { deal: DealData }) {
  const bars = [
    { label: "Champion Risk", val: deal.champion_risk_score },
    { label: "Engagement Decay", val: deal.engagement_decay_score },
    { label: "Scope Erosion", val: deal.scope_erosion_score },
    { label: "Timeline Drift", val: deal.timeline_drift_score },
  ];
  return (
    <div className="space-y-2">
      {bars.map((b) => {
        const color = b.val >= 60 ? "bg-red-500" : b.val >= 40 ? "bg-orange-500" : b.val >= 20 ? "bg-amber-500" : "bg-emerald-500";
        return (
          <div key={b.label}>
            <div className="flex justify-between text-xs mb-0.5">
              <span className="text-slate-500">{b.label}</span>
              <span className={b.val >= 60 ? "text-red-400" : b.val >= 40 ? "text-orange-400" : "text-slate-400"}>
                {b.val.toFixed(0)}
              </span>
            </div>
            <div className="h-1.5 bg-slate-700 rounded-full overflow-hidden">
              <div className={`h-full rounded-full ${color} transition-all duration-500`} style={{ width: `${b.val}%` }} />
            </div>
          </div>
        );
      })}
    </div>
  );
}

// ── FragmentationGauge SVG ────────────────────────────────────────────────────

function FragmentationGauge({ score, risk }: { score: number; risk: string }) {
  const r = 28, cx = 36, cy = 42;
  const startAngle = Math.PI;
  const endAngle = 2 * Math.PI;
  const arc = endAngle - startAngle;
  const fill = arc * Math.min(1, score / 100);
  const strokeColor =
    risk === "fragmenting"  ? "#f87171" :
    risk === "at_risk"      ? "#f97316" :
    risk === "early_signal" ? "#fbbf24" : "#34d399";
  const toXY = (angle: number) => ({
    x: cx + r * Math.cos(angle),
    y: cy + r * Math.sin(angle),
  });
  const s = toXY(startAngle);
  const e = toXY(startAngle + fill);
  const large = fill > Math.PI ? 1 : 0;

  return (
    <svg width="72" height="52" viewBox="0 0 72 52">
      <path d={`M${toXY(startAngle).x},${toXY(startAngle).y} A${r},${r} 0 1 1 ${toXY(endAngle).x},${toXY(endAngle).y}`}
        fill="none" stroke="#1e293b" strokeWidth="6" strokeLinecap="round" />
      {fill > 0.01 && (
        <path d={`M${s.x},${s.y} A${r},${r} 0 ${large} 1 ${e.x},${e.y}`}
          fill="none" stroke={strokeColor} strokeWidth="6" strokeLinecap="round" />
      )}
      <text x={cx} y={cy - 8} textAnchor="middle" fill="white" fontSize="13" fontWeight="700">
        {score.toFixed(0)}
      </text>
      <text x={cx} y={cy + 4} textAnchor="middle" fill="#94a3b8" fontSize="7">
        frag score
      </text>
    </svg>
  );
}

// ── DealModal ─────────────────────────────────────────────────────────────────

function DealModal({ deal, onClose }: { deal: DealData; onClose: () => void }) {
  const [tab, setTab] = useState<"signals" | "deal" | "actions">("signals");

  useEffect(() => {
    const h = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    document.addEventListener("keydown", h);
    return () => document.removeEventListener("keydown", h);
  }, [onClose]);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4" onClick={onClose}>
      <div className="absolute inset-0 bg-black/70 backdrop-blur-sm" />
      <div
        className="relative bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-lg shadow-2xl overflow-hidden"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="p-5 border-b border-slate-800">
          <div className="flex items-start justify-between gap-3">
            <div>
              <h2 className="text-white font-bold text-lg">{deal.deal_name}</h2>
              <p className="text-slate-400 text-sm">{deal.stage} · {deal.region}</p>
            </div>
            <div className="flex items-center gap-2">
              <span className={`px-2 py-0.5 rounded-full text-xs font-semibold border ${ACTION_BADGE[deal.recommended_action]}`}>
                {deal.recommended_action.replace("_", " ")}
              </span>
              <button onClick={onClose} className="text-slate-500 hover:text-white transition-colors text-xl leading-none">×</button>
            </div>
          </div>
          <div className="flex gap-2 mt-3">
            {(["signals", "deal", "actions"] as const).map((t) => (
              <button
                key={t}
                onClick={() => setTab(t)}
                className={`px-3 py-1 rounded-lg text-xs font-medium transition-colors capitalize ${tab === t ? "bg-indigo-600 text-white" : "text-slate-400 hover:text-white hover:bg-slate-800"}`}
              >
                {t === "signals" ? "Fragmentation Signals" : t === "deal" ? "Deal Details" : "Recovery Plan"}
              </button>
            ))}
          </div>
        </div>

        <div className="p-5 overflow-y-auto max-h-[60vh]">
          {tab === "signals" && (
            <div className="space-y-4">
              <div className="flex items-center gap-4">
                <FragmentationGauge score={deal.fragmentation_composite_score} risk={deal.fragmentation_risk} />
                <div className="flex-1 space-y-1">
                  <div className="flex justify-between text-sm">
                    <span className="text-slate-400">Risk Level</span>
                    <span className={`font-semibold capitalize ${RISK_COLOR[deal.fragmentation_risk]}`}>
                      {deal.fragmentation_risk.replace("_", " ")}
                    </span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-slate-400">Pattern</span>
                    <span className="text-white font-medium capitalize">{deal.fragmentation_pattern.replace("_", " ")}</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-slate-400">Prognosis</span>
                    <span className={`font-medium capitalize ${PROGNOSIS_COLOR[deal.deal_prognosis]}`}>
                      {deal.deal_prognosis.replace("_", " ")}
                    </span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-slate-400">Recovery Prob.</span>
                    <span className={`font-bold ${deal.recovery_probability >= 60 ? "text-emerald-400" : deal.recovery_probability >= 30 ? "text-amber-400" : "text-red-400"}`}>
                      {deal.recovery_probability.toFixed(0)}%
                    </span>
                  </div>
                </div>
              </div>
              <FragmentationBars deal={deal} />
              <div className="grid grid-cols-2 gap-3">
                <div className={`rounded-lg p-3 border ${deal.is_fragmenting ? "bg-red-900/30 border-red-700/40" : "bg-slate-800/50 border-slate-700/40"}`}>
                  <p className="text-xs text-slate-500">Fragmenting</p>
                  <p className={`text-sm font-semibold mt-0.5 ${deal.is_fragmenting ? "text-red-400" : "text-emerald-400"}`}>
                    {deal.is_fragmenting ? "Yes — Alert" : "No"}
                  </p>
                </div>
                <div className={`rounded-lg p-3 border ${deal.needs_immediate_intervention ? "bg-red-900/30 border-red-700/40" : "bg-slate-800/50 border-slate-700/40"}`}>
                  <p className="text-xs text-slate-500">Intervention</p>
                  <p className={`text-sm font-semibold mt-0.5 ${deal.needs_immediate_intervention ? "text-red-400" : "text-emerald-400"}`}>
                    {deal.needs_immediate_intervention ? "Required now" : "Not needed"}
                  </p>
                </div>
              </div>
            </div>
          )}

          {tab === "deal" && (
            <div className="space-y-3">
              <div className="grid grid-cols-2 gap-3">
                <div className="bg-slate-800/50 border border-slate-700/40 rounded-lg p-3">
                  <p className="text-xs text-slate-500">Current Value</p>
                  <p className="text-lg font-bold text-white mt-1">{fmt$(deal.deal_value)}</p>
                </div>
                <div className="bg-slate-800/50 border border-slate-700/40 rounded-lg p-3">
                  <p className="text-xs text-slate-500">Initial Value</p>
                  <p className={`text-lg font-bold mt-1 ${deal.deal_value < deal.initial_deal_value ? "text-red-400" : "text-white"}`}>
                    {fmt$(deal.initial_deal_value)}
                  </p>
                </div>
                <div className="bg-slate-800/50 border border-slate-700/40 rounded-lg p-3">
                  <p className="text-xs text-slate-500">Days in Stage</p>
                  <p className="text-lg font-bold text-white mt-1">{deal.days_in_current_stage}d</p>
                </div>
                <div className="bg-slate-800/50 border border-slate-700/40 rounded-lg p-3">
                  <p className="text-xs text-slate-500">At Risk Value</p>
                  <p className="text-lg font-bold text-red-400 mt-1">{fmt$(deal.estimated_deal_at_risk)}</p>
                </div>
              </div>
              <div className="bg-slate-800/50 border border-slate-700/40 rounded-lg p-4 space-y-2">
                <div className="flex justify-between text-sm">
                  <span className="text-slate-400">Champion Last Active</span>
                  <span className={deal.champion_last_active_days >= 14 ? "text-red-400" : "text-white"}>
                    {deal.champion_last_active_days}d ago
                  </span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-slate-400">Close Date Pushed</span>
                  <span className={deal.close_date_pushed_times >= 2 ? "text-orange-400" : "text-white"}>
                    {deal.close_date_pushed_times}x
                  </span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-slate-400">Stage Regressions</span>
                  <span className={deal.stage_regression_count >= 1 ? "text-red-400" : "text-white"}>
                    {deal.stage_regression_count}
                  </span>
                </div>
              </div>
            </div>
          )}

          {tab === "actions" && (
            <div className="space-y-3">
              <div className={`rounded-lg p-4 border ${ACTION_BADGE[deal.recommended_action]}`}>
                <p className="text-xs font-semibold uppercase tracking-wider opacity-70 mb-1">Recommended Action</p>
                <p className="text-lg font-bold capitalize">{deal.recommended_action.replace("_", " ")}</p>
              </div>
              {deal.recommended_action === "escalate" && (
                <ul className="space-y-2 text-sm text-slate-300">
                  <li className="flex gap-2"><span className="text-red-400">•</span> Escalate immediately — sales manager must get involved</li>
                  <li className="flex gap-2"><span className="text-red-400">•</span> Identify new champion or executive sponsor urgently</li>
                  <li className="flex gap-2"><span className="text-red-400">•</span> Request executive-to-executive call within 48 hours</li>
                  <li className="flex gap-2"><span className="text-red-400">•</span> Reassess deal viability and consider offer restructuring</li>
                </ul>
              )}
              {deal.recommended_action === "rescue" && (
                <ul className="space-y-2 text-sm text-slate-300">
                  <li className="flex gap-2"><span className="text-orange-400">•</span> Schedule re-engagement call with all stakeholders</li>
                  <li className="flex gap-2"><span className="text-orange-400">•</span> Address scope erosion — clarify value proposition</li>
                  <li className="flex gap-2"><span className="text-orange-400">•</span> Review and refresh mutual action plan with new close date</li>
                </ul>
              )}
              {deal.recommended_action === "re_engage" && (
                <ul className="space-y-2 text-sm text-slate-300">
                  <li className="flex gap-2"><span className="text-amber-400">•</span> Send targeted outreach to silent stakeholders</li>
                  <li className="flex gap-2"><span className="text-amber-400">•</span> Provide a compelling reason to re-engage (case study, event)</li>
                  <li className="flex gap-2"><span className="text-amber-400">•</span> Validate timeline with a confirmed next step</li>
                </ul>
              )}
              {deal.recommended_action === "maintain" && (
                <ul className="space-y-2 text-sm text-slate-300">
                  <li className="flex gap-2"><span className="text-emerald-400">•</span> Deal health is good — maintain current cadence</li>
                  <li className="flex gap-2"><span className="text-emerald-400">•</span> Keep champion engaged with regular value touchpoints</li>
                  <li className="flex gap-2"><span className="text-emerald-400">•</span> Monitor for early fragmentation signals weekly</li>
                </ul>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

// ── DealCard ──────────────────────────────────────────────────────────────────

function DealCard({ deal, onClick }: { deal: DealData; onClick: () => void }) {
  return (
    <div
      onClick={onClick}
      className={`rounded-xl border p-4 cursor-pointer hover:border-slate-600 transition-all ${RISK_BG[deal.fragmentation_risk]}`}
    >
      <div className="flex items-start justify-between gap-2 mb-2">
        <div>
          <p className="text-white font-semibold text-sm">{deal.deal_name}</p>
          <p className="text-slate-500 text-xs">{deal.stage} · {deal.region}</p>
        </div>
        <div className="flex flex-col items-end gap-1">
          <span className={`text-xs font-bold uppercase ${RISK_COLOR[deal.fragmentation_risk]}`}>
            {deal.fragmentation_risk.replace("_", " ")}
          </span>
          <span className="text-slate-500 text-xs">{fmt$(deal.deal_value)}</span>
        </div>
      </div>

      <div className="flex items-center gap-3 mb-3">
        <FragmentationGauge score={deal.fragmentation_composite_score} risk={deal.fragmentation_risk} />
        <div className="flex-1">
          <FragmentationBars deal={deal} />
        </div>
      </div>

      <div className="flex items-center justify-between">
        <span className={`text-xs px-2 py-0.5 rounded-full border ${ACTION_BADGE[deal.recommended_action]}`}>
          {deal.recommended_action.replace("_", " ")}
        </span>
        <div className="flex gap-2 items-center">
          <span className={`text-xs ${PROGNOSIS_COLOR[deal.deal_prognosis]}`}>
            {deal.deal_prognosis.replace("_", " ")}
          </span>
          {deal.needs_immediate_intervention && (
            <span className="text-xs text-red-500 font-bold">⚠ Urgent</span>
          )}
        </div>
      </div>
    </div>
  );
}

// ── Page ──────────────────────────────────────────────────────────────────────

export default function DealFragmentationPage() {
  const [data, setData] = useState<{ deals: DealData[]; summary: Summary } | null>(null);
  const [loading, setLoading] = useState(true);
  const [selected, setSelected] = useState<DealData | null>(null);
  const [filterRisk, setFilterRisk]       = useState("all");
  const [filterPattern, setFilterPattern] = useState("all");
  const [filterRegion, setFilterRegion]   = useState("all");

  useEffect(() => {
    async function fetchData() {
        setLoading(true);
        try {
          const params = new URLSearchParams();
          if (filterRisk !== "all")    params.set("risk", filterRisk);
          if (filterPattern !== "all") params.set("pattern", filterPattern);
          if (filterRegion !== "all")  params.set("region", filterRegion);
          const res = await fetch(`/api/deal-fragmentation?${params}`);
          if (res.ok) setData(await res.json());
        } catch {}
        setLoading(false);
  }
    fetchData();
  }, [filterRisk, filterPattern, filterRegion]);

  const s = data?.summary;
  const riskOrder = ["fragmenting", "at_risk", "early_signal", "stable"];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
      <div className="max-w-7xl mx-auto space-y-6">

        {/* Header */}
        <div>
          <h1 className="text-2xl font-bold text-white">Deal Fragmentation Detector</h1>
          <p className="text-slate-400 text-sm mt-1">Detect deals quietly falling apart before they slip out of forecast</p>
        </div>

        {/* KPI Strip */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {[
            { label: "Deals Monitored", value: s?.total ?? "—", sub: "in pipeline" },
            { label: "Fragmenting Now", value: s?.fragmenting_count ?? "—", sub: "critical deals", danger: (s?.fragmenting_count ?? 0) > 0 },
            { label: "Need Intervention", value: s?.intervention_needed_count ?? "—", sub: "act today", danger: (s?.intervention_needed_count ?? 0) > 0 },
            { label: "Total $ At Risk", value: s ? fmt$(s.total_estimated_deal_at_risk) : "—", sub: "fragmentation risk", danger: (s?.total_estimated_deal_at_risk ?? 0) > 0 },
          ].map((k) => (
            <div key={k.label} className="bg-slate-900 border border-slate-800 rounded-xl p-4">
              <p className="text-slate-500 text-xs">{k.label}</p>
              <p className={`text-2xl font-bold mt-1 ${k.danger ? "text-red-400" : "text-white"}`}>{k.value}</p>
              <p className="text-slate-600 text-xs mt-0.5">{k.sub}</p>
            </div>
          ))}
        </div>

        {/* Score Averages */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {[
            { label: "Avg Fragmentation Score", value: s?.avg_fragmentation_composite_score.toFixed(1) ?? "—" },
            { label: "Avg Champion Risk", value: s?.avg_champion_risk_score.toFixed(1) ?? "—" },
            { label: "Avg Engagement Decay", value: s?.avg_engagement_decay_score.toFixed(1) ?? "—" },
            { label: "Avg Recovery Prob.", value: s ? `${s.avg_recovery_probability.toFixed(1)}%` : "—" },
          ].map((k) => (
            <div key={k.label} className="bg-slate-900 border border-slate-800 rounded-xl p-4">
              <p className="text-slate-500 text-xs">{k.label}</p>
              <p className="text-xl font-bold text-white mt-1">{k.value}</p>
            </div>
          ))}
        </div>

        {/* Filters */}
        <div className="flex flex-wrap gap-3">
          <div className="flex gap-1 bg-slate-900 border border-slate-800 rounded-lg p-1">
            {["all", "fragmenting", "at_risk", "early_signal", "stable"].map((v) => (
              <button
                key={v}
                onClick={() => setFilterRisk(v)}
                className={`px-3 py-1 rounded text-xs font-medium transition-colors ${filterRisk === v ? "bg-indigo-600 text-white" : "text-slate-400 hover:text-white"}`}
              >
                {v === "all" ? "All Risks" : v.replace("_", " ")}
              </button>
            ))}
          </div>
          <div className="flex gap-1 bg-slate-900 border border-slate-800 rounded-lg p-1">
            {["all", "multi_signal", "champion_loss", "engagement_drop", "scope_shrink", "timeline_slip"].map((v) => (
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

        {/* Deals grid */}
        {loading ? (
          <div className="text-center py-12 text-slate-500">Scanning pipeline for fragmentation signals...</div>
        ) : (
          <>
            {data && data.deals.filter((d) => d.needs_immediate_intervention).length > 0 && (
              <div className="bg-red-950/40 border border-red-800/50 rounded-xl p-4 flex items-center gap-3">
                <span className="text-red-400 text-xl">🚨</span>
                <p className="text-red-300 text-sm font-medium">
                  {data.deals.filter((d) => d.needs_immediate_intervention).length} deal(s) require immediate manager intervention — escalate today.
                </p>
              </div>
            )}
            <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
              {data?.deals
                .slice()
                .sort((a, b) => riskOrder.indexOf(a.fragmentation_risk) - riskOrder.indexOf(b.fragmentation_risk))
                .map((deal) => (
                  <DealCard key={deal.deal_id} deal={deal} onClick={() => setSelected(deal)} />
                ))}
            </div>
            {data?.deals.length === 0 && (
              <p className="text-center text-slate-500 py-8">No deals match current filters.</p>
            )}
          </>
        )}
      </div>

      {selected && <DealModal deal={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
