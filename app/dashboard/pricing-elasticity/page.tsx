"use client";

import { useEffect, useState } from "react";

// ── types ─────────────────────────────────────────────────────────────────────

interface Segment {
  segment_id: string;
  segment_name: string;
  industry: string;
  region: string;
  elasticity_category: string;
  pricing_risk: string;
  pricing_stance: string;
  pricing_action: string;
  price_elasticity_index: number;
  discount_leak_score: number;
  competitive_pressure_score: number;
  revenue_at_risk: number;
  expansion_opportunity: number;
  optimal_price_adjustment_pct: number;
  pricing_confidence_score: number;
  is_price_sensitive: boolean;
  needs_pricing_review: boolean;
  avg_deal_size_current: number;
  total_pipeline_value: number;
}

interface Summary {
  total: number;
  elasticity_counts: Record<string, number>;
  risk_counts: Record<string, number>;
  stance_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_price_elasticity_index: number;
  avg_discount_leak_score: number;
  total_revenue_at_risk: number;
  total_expansion_opportunity: number;
  price_sensitive_count: number;
  review_needed_count: number;
  avg_competitive_pressure_score: number;
  avg_optimal_price_adjustment_pct: number;
}

// ── helpers ───────────────────────────────────────────────────────────────────

const ELASTICITY_COLOR: Record<string, string> = {
  inelastic: "text-emerald-400",
  low:       "text-green-400",
  moderate:  "text-yellow-400",
  high:      "text-orange-400",
  extreme:   "text-red-400",
};

const ELASTICITY_BAR: Record<string, string> = {
  inelastic: "bg-emerald-500",
  low:       "bg-green-500",
  moderate:  "bg-yellow-500",
  high:      "bg-orange-500",
  extreme:   "bg-red-500",
};

const ACTION_COLOR: Record<string, string> = {
  increase:         "bg-emerald-500/20 text-emerald-300 border-emerald-500/30",
  hold:             "bg-slate-500/20 text-slate-300 border-slate-500/30",
  optimize:         "bg-indigo-500/20 text-indigo-300 border-indigo-500/30",
  discount_control: "bg-amber-500/20 text-amber-300 border-amber-500/30",
  restructure:      "bg-red-500/20 text-red-300 border-red-500/30",
};

const STANCE_COLOR: Record<string, string> = {
  premium:     "text-violet-400",
  competitive: "text-sky-400",
  neutral:     "text-slate-400",
  defensive:   "text-orange-400",
  vulnerable:  "text-red-400",
};

function fmt(label: string) {
  return label.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
}

function fmtMoney(n: number) {
  if (n >= 1_000_000) return `$${(n / 1_000_000).toFixed(1)}M`;
  if (n >= 1_000) return `$${Math.round(n / 1_000)}k`;
  return `$${n}`;
}

function fmtAdj(pct: number) {
  if (pct > 0) return `+${pct}%`;
  if (pct < 0) return `${pct}%`;
  return "Hold";
}

// ── ElasticityArc SVG ─────────────────────────────────────────────────────────

function ElasticityArc({ index }: { index: number }) {
  const angle = (index / 100) * 180 - 90;
  const rad = (angle * Math.PI) / 180;
  const r = 38;
  const cx = 50;
  const cy = 50;
  const x = cx + r * Math.cos(rad);
  const y = cy + r * Math.sin(rad);
  const color =
    index >= 75 ? "#ef4444" :
    index >= 55 ? "#f97316" :
    index >= 35 ? "#eab308" :
    index >= 15 ? "#22c55e" : "#10b981";

  return (
    <svg width="100" height="60" viewBox="0 0 100 60" className="mx-auto">
      <path d="M 12 50 A 38 38 0 0 1 88 50" fill="none" stroke="#1e293b" strokeWidth="6" strokeLinecap="round" />
      <path
        d={`M 12 50 A 38 38 0 0 1 ${x.toFixed(1)} ${y.toFixed(1)}`}
        fill="none" stroke={color} strokeWidth="6" strokeLinecap="round"
      />
      <text x="50" y="48" textAnchor="middle" fill="white" fontSize="13" fontWeight="bold">
        {Math.round(index)}
      </text>
      <text x="50" y="58" textAnchor="middle" fill="#64748b" fontSize="8">Elasticity</text>
    </svg>
  );
}

// ── ElasticityDistBar ─────────────────────────────────────────────────────────

function ElasticityDistBar({ counts, total }: { counts: Record<string, number>; total: number }) {
  const order = ["inelastic", "low", "moderate", "high", "extreme"];
  return (
    <div className="flex rounded-full overflow-hidden h-3 w-full">
      {order.map((k) => {
        const pct = total > 0 ? ((counts[k] || 0) / total) * 100 : 0;
        if (pct === 0) return null;
        return (
          <div key={k} style={{ width: `${pct}%` }} className={`${ELASTICITY_BAR[k]} transition-all`} title={`${k}: ${counts[k] || 0}`} />
        );
      })}
    </div>
  );
}

// ── SegmentModal ──────────────────────────────────────────────────────────────

function SegmentModal({ segment, onClose }: { segment: Segment; onClose: () => void }) {
  const [tab, setTab] = useState<"elasticity" | "pricing" | "actions">("elasticity");

  useEffect(() => {
    const handler = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [onClose]);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4" onClick={onClose}>
      <div className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-2xl max-h-[90vh] overflow-y-auto" onClick={(e) => e.stopPropagation()}>
        <div className="p-6 border-b border-slate-800 flex items-start justify-between gap-4">
          <div>
            <div className="flex items-center gap-3 flex-wrap">
              <h2 className="text-xl font-bold text-slate-100">{segment.segment_name}</h2>
              <span className={`text-xs font-semibold px-2.5 py-0.5 rounded-full border ${ACTION_COLOR[segment.pricing_action]}`}>
                {fmt(segment.pricing_action)}
              </span>
              {segment.needs_pricing_review && (
                <span className="text-xs font-semibold px-2.5 py-0.5 rounded-full bg-orange-500/20 text-orange-300 border border-orange-500/30">
                  Review Needed
                </span>
              )}
            </div>
            <p className="text-sm text-slate-400 mt-1">
              <span className={`font-semibold ${ELASTICITY_COLOR[segment.elasticity_category]}`}>{fmt(segment.elasticity_category)} Elasticity</span>
              {" · "}{segment.industry}{" · "}{segment.region}
            </p>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-slate-300 text-xl leading-none">✕</button>
        </div>

        <div className="flex gap-0 border-b border-slate-800">
          {(["elasticity", "pricing", "actions"] as const).map((t) => (
            <button key={t} onClick={() => setTab(t)} className={`px-5 py-3 text-sm font-medium border-b-2 transition-colors ${tab === t ? "border-indigo-500 text-indigo-400" : "border-transparent text-slate-400 hover:text-slate-300"}`}>
              {t.charAt(0).toUpperCase() + t.slice(1)}
            </button>
          ))}
        </div>

        <div className="p-6">
          {tab === "elasticity" && (
            <div className="space-y-5">
              <ElasticityArc index={segment.price_elasticity_index} />
              <div className="grid grid-cols-3 gap-4 text-center">
                {[
                  { label: "Discount Leak", value: Math.round(segment.discount_leak_score), color: "text-amber-400" },
                  { label: "Comp. Pressure", value: Math.round(segment.competitive_pressure_score), color: "text-orange-400" },
                  { label: "Confidence", value: `${segment.pricing_confidence_score}%`, color: "text-indigo-400" },
                ].map(({ label, value, color }) => (
                  <div key={label} className="bg-slate-800/60 rounded-xl p-3">
                    <div className={`text-xl font-bold ${color}`}>{value}</div>
                    <div className="text-xs text-slate-400">{label}</div>
                  </div>
                ))}
              </div>
              <div>
                <div className="flex justify-between text-xs text-slate-400 mb-1">
                  <span>Discount Leakage</span>
                  <span className="text-amber-400">{segment.discount_leak_score}</span>
                </div>
                <div className="w-full bg-slate-700/50 rounded-full h-2">
                  <div className="h-2 rounded-full bg-amber-500 transition-all" style={{ width: `${Math.min(segment.discount_leak_score, 100)}%` }} />
                </div>
              </div>
              <div>
                <div className="flex justify-between text-xs text-slate-400 mb-1">
                  <span>Competitive Pressure</span>
                  <span className="text-orange-400">{segment.competitive_pressure_score}</span>
                </div>
                <div className="w-full bg-slate-700/50 rounded-full h-2">
                  <div className="h-2 rounded-full bg-orange-500 transition-all" style={{ width: `${Math.min(segment.competitive_pressure_score, 100)}%` }} />
                </div>
              </div>
            </div>
          )}

          {tab === "pricing" && (
            <div className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                {[
                  { label: "Avg Deal Size", value: fmtMoney(segment.avg_deal_size_current) },
                  { label: "Total Pipeline", value: fmtMoney(segment.total_pipeline_value) },
                  { label: "Revenue at Risk", value: fmtMoney(segment.revenue_at_risk), color: "text-red-400" },
                  { label: "Expansion Opp.", value: fmtMoney(segment.expansion_opportunity), color: "text-emerald-400" },
                  { label: "Optimal Adjustment", value: fmtAdj(segment.optimal_price_adjustment_pct), color: segment.optimal_price_adjustment_pct > 0 ? "text-emerald-400" : segment.optimal_price_adjustment_pct < 0 ? "text-red-400" : "text-slate-300" },
                  { label: "Pricing Stance", value: fmt(segment.pricing_stance), color: STANCE_COLOR[segment.pricing_stance] },
                  { label: "Price Sensitive", value: segment.is_price_sensitive ? "Yes" : "No" },
                  { label: "Region", value: segment.region },
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
              <div className={`p-4 rounded-xl border ${segment.pricing_risk === "critical" ? "bg-red-500/10 border-red-500/30" : segment.pricing_risk === "high" ? "bg-orange-500/10 border-orange-500/30" : "bg-slate-700/30 border-slate-600/30"}`}>
                <div className={`text-sm font-semibold mb-1 ${segment.pricing_risk === "critical" ? "text-red-400" : segment.pricing_risk === "high" ? "text-orange-400" : "text-slate-300"}`}>
                  {fmt(segment.elasticity_category)} Elasticity · {fmt(segment.pricing_stance)} Stance
                </div>
                <div className="text-xs text-slate-400">
                  {segment.pricing_action === "restructure" && "Pricing model needs urgent restructure to address critical sensitivity and churn risk."}
                  {segment.pricing_action === "discount_control" && "Discount discipline required — current discount patterns are eroding margin."}
                  {segment.pricing_action === "increase" && `Segment shows inelastic demand — recommend ${fmtAdj(segment.optimal_price_adjustment_pct)} price increase.`}
                  {segment.pricing_action === "optimize" && "Optimize pricing mix — consider value-based pricing and reduce discount frequency."}
                  {segment.pricing_action === "hold" && "Current pricing is well-positioned. Monitor for competitive shifts."}
                </div>
              </div>
              <div className="space-y-3">
                {[
                  segment.pricing_action === "increase" && { label: "Price Increase Plan", desc: `Model ${fmtAdj(segment.optimal_price_adjustment_pct)} price increase phased over 2 quarters` },
                  segment.pricing_action === "discount_control" && { label: "Discount Authority Review", desc: "Cap discount authority and require manager approval above 10%" },
                  segment.pricing_action === "restructure" && { label: "Pricing Model Redesign", desc: "Align pricing to segment value drivers — move away from feature-based to outcome-based" },
                  segment.pricing_action === "optimize" && { label: "Value-Based Pricing Pilot", desc: "Run A/B test with outcome-based pricing for 3 new deals this quarter" },
                  segment.expansion_opportunity > 0 && { label: "Expansion Revenue Target", desc: `${fmtMoney(segment.expansion_opportunity)} accessible with optimised pricing strategy` },
                  segment.is_price_sensitive && { label: "Competitive Pricing Report", desc: "Quarterly competitor price benchmarking to track positioning" },
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

// ── SegmentCard ───────────────────────────────────────────────────────────────

function SegmentCard({ segment, onClick }: { segment: Segment; onClick: () => void }) {
  return (
    <button onClick={onClick} className="w-full text-left bg-slate-800/60 border border-slate-700/50 rounded-2xl p-5 hover:border-indigo-500/40 hover:bg-slate-800/80 transition-all group">
      <div className="flex items-start justify-between gap-3 mb-3">
        <div>
          <h3 className="font-semibold text-slate-100 group-hover:text-white transition-colors">{segment.segment_name}</h3>
          <p className="text-xs text-slate-400 mt-0.5">{segment.industry} · {segment.region}</p>
        </div>
        <div className="flex flex-col items-end gap-1.5 shrink-0">
          <span className={`text-xs font-semibold px-2 py-0.5 rounded-full border ${ACTION_COLOR[segment.pricing_action]}`}>
            {fmt(segment.pricing_action)}
          </span>
          <span className={`text-xs ${STANCE_COLOR[segment.pricing_stance]}`}>{fmt(segment.pricing_stance)}</span>
        </div>
      </div>

      <div className="flex gap-2 mb-3 flex-wrap">
        {[
          { label: "Elasticity", value: segment.price_elasticity_index, color: ELASTICITY_COLOR[segment.elasticity_category] },
          { label: "Discount Leak", value: segment.discount_leak_score, color: "text-amber-400" },
          { label: "Comp. Pressure", value: segment.competitive_pressure_score, color: "text-orange-400" },
        ].map(({ label, value, color }) => (
          <div key={label} className="flex flex-col items-center bg-slate-900/60 rounded-lg px-3 py-1.5">
            <span className={`text-sm font-bold ${color}`}>{Math.round(value)}</span>
            <span className="text-xs text-slate-500">{label}</span>
          </div>
        ))}
        <div className="flex flex-col items-center bg-slate-900/60 rounded-lg px-3 py-1.5">
          <span className={`text-sm font-bold ${segment.optimal_price_adjustment_pct > 0 ? "text-emerald-400" : segment.optimal_price_adjustment_pct < 0 ? "text-red-400" : "text-slate-400"}`}>
            {fmtAdj(segment.optimal_price_adjustment_pct)}
          </span>
          <span className="text-xs text-slate-500">Adj.</span>
        </div>
      </div>

      <div className="flex justify-between items-center text-xs text-slate-400">
        <span className="text-red-400">{fmtMoney(segment.revenue_at_risk)} at risk</span>
        <span className="text-emerald-400">{fmtMoney(segment.expansion_opportunity)} opp.</span>
        <span>{fmtMoney(segment.avg_deal_size_current)} avg deal</span>
      </div>
    </button>
  );
}

// ── Page ──────────────────────────────────────────────────────────────────────

export default function PricingElasticityPage() {
  const [segments, setSegments] = useState<Segment[]>([]);
  const [summary, setSummary] = useState<Summary | null>(null);
  const [loading, setLoading] = useState(true);
  const [selected, setSelected] = useState<Segment | null>(null);
  const [filterCategory, setFilterCategory] = useState("all");
  const [filterRisk, setFilterRisk] = useState("all");

  useEffect(() => {
    async function load() {
        setLoading(true);
        try {
          const params = new URLSearchParams();
          if (filterCategory !== "all") params.set("category", filterCategory);
          if (filterRisk     !== "all") params.set("risk", filterRisk);
          const res = await fetch(`/api/pricing-elasticity?${params}`);
          const data = await res.json();
          setSegments(data.segments ?? []);
          setSummary(data.summary ?? null);
        } finally {
          setLoading(false);
        }
  }
    load();
  }, [filterCategory, filterRisk]);

  const categories = ["all", "inelastic", "low", "moderate", "high", "extreme"];
  const risks = ["all", "low", "medium", "high", "critical"];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
      {selected && <SegmentModal segment={selected} onClose={() => setSelected(null)} />}

      <div className="mb-8">
        <h1 className="text-3xl font-bold text-white">Pricing Elasticity</h1>
        <p className="text-slate-400 mt-1">Quantify price sensitivity by segment — find expansion opportunities and protect revenue at risk</p>
      </div>

      {summary && (
        <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-7 gap-4 mb-8">
          {[
            { label: "Segments", value: summary.total },
            { label: "Price Sensitive", value: summary.price_sensitive_count, color: "text-orange-400" },
            { label: "Review Needed", value: summary.review_needed_count, color: "text-amber-400" },
            { label: "Revenue at Risk", value: fmtMoney(summary.total_revenue_at_risk), color: "text-red-400" },
            { label: "Expansion Opp.", value: fmtMoney(summary.total_expansion_opportunity), color: "text-emerald-400" },
            { label: "Avg Elasticity", value: summary.avg_price_elasticity_index },
            { label: "Avg Discount Leak", value: summary.avg_discount_leak_score, color: "text-amber-400" },
          ].map(({ label, value, color }) => (
            <div key={label} className="bg-slate-800/60 border border-slate-700/50 rounded-2xl p-4">
              <div className="text-xs text-slate-400 mb-1">{label}</div>
              <div className={`text-2xl font-bold ${color ?? "text-white"}`}>{value}</div>
            </div>
          ))}
        </div>
      )}

      {summary && (
        <div className="bg-slate-800/60 border border-slate-700/50 rounded-2xl p-5 mb-8">
          <div className="flex items-center justify-between mb-3">
            <h2 className="text-sm font-semibold text-slate-300">Elasticity Distribution</h2>
            <div className="flex gap-3 flex-wrap">
              {["inelastic", "low", "moderate", "high", "extreme"].map((k) => (
                <div key={k} className="flex items-center gap-1.5 text-xs text-slate-400">
                  <div className={`w-2.5 h-2.5 rounded-full ${ELASTICITY_BAR[k]}`} />
                  {fmt(k)} ({summary.elasticity_counts[k] || 0})
                </div>
              ))}
            </div>
          </div>
          <ElasticityDistBar counts={summary.elasticity_counts} total={summary.total} />
          <div className="grid grid-cols-3 gap-4 mt-4 text-center">
            <div>
              <div className="text-lg font-bold text-red-400">{fmtMoney(summary.total_revenue_at_risk)}</div>
              <div className="text-xs text-slate-400">Total Revenue at Risk</div>
            </div>
            <div>
              <div className="text-lg font-bold text-emerald-400">{fmtMoney(summary.total_expansion_opportunity)}</div>
              <div className="text-xs text-slate-400">Total Expansion Opp.</div>
            </div>
            <div>
              <div className={`text-lg font-bold ${summary.avg_optimal_price_adjustment_pct > 0 ? "text-emerald-400" : summary.avg_optimal_price_adjustment_pct < 0 ? "text-red-400" : "text-slate-300"}`}>
                {fmtAdj(summary.avg_optimal_price_adjustment_pct)}
              </div>
              <div className="text-xs text-slate-400">Avg Optimal Adj.</div>
            </div>
          </div>
        </div>
      )}

      <div className="flex flex-wrap gap-3 mb-6">
        <div className="flex flex-wrap gap-2">
          {categories.map((c) => (
            <button key={c} onClick={() => setFilterCategory(c)} className={`px-3 py-1.5 rounded-full text-xs font-medium border transition-colors ${filterCategory === c ? "bg-indigo-600 border-indigo-500 text-white" : "bg-slate-800/60 border-slate-700 text-slate-400 hover:text-slate-300"}`}>
              {fmt(c)}
            </button>
          ))}
        </div>
        <div className="flex flex-wrap gap-2">
          {risks.map((r) => (
            <button key={r} onClick={() => setFilterRisk(r)} className={`px-3 py-1.5 rounded-full text-xs font-medium border transition-colors ${filterRisk === r ? "bg-indigo-600 border-indigo-500 text-white" : "bg-slate-800/60 border-slate-700 text-slate-400 hover:text-slate-300"}`}>
              {fmt(r)}
            </button>
          ))}
        </div>
      </div>

      {loading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
          {[...Array(6)].map((_, i) => <div key={i} className="h-44 bg-slate-800/40 rounded-2xl animate-pulse" />)}
        </div>
      ) : segments.length === 0 ? (
        <div className="text-center py-20 text-slate-500">No segments match the selected filters.</div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
          {segments.map((s) => <SegmentCard key={s.segment_id} segment={s} onClick={() => setSelected(s)} />)}
        </div>
      )}
    </div>
  );
}
