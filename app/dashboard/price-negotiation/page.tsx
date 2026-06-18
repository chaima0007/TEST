"use client";

import { useEffect, useState, useCallback } from "react";

// ── Types ────────────────────────────────────────────────────────────────────

interface Deal {
  deal_id: string;
  account_id: string;
  rep_id: string;
  deal_name: string;
  account_name: string;
  segment: string;
  list_price: number;
  proposed_price: number;
  discount_risk: string;
  negotiation_stage: string;
  pricing_strategy: string;
  margin_health: string;
  gross_margin_pct: number;
  effective_discount_pct: number;
  price_to_value_score: number;
  negotiation_leverage: number;
  walkaway_risk: number;
  recommended_concession: number;
  is_margin_positive: boolean;
  is_strategic: boolean;
  days_to_close: number;
  multi_year_deal: boolean;
  professional_services: number;
}

interface Summary {
  total: number;
  risk_counts: Record<string, number>;
  stage_counts: Record<string, number>;
  strategy_counts: Record<string, number>;
  margin_health_counts: Record<string, number>;
  avg_gross_margin_pct: number;
  avg_effective_discount: number;
  avg_negotiation_leverage: number;
  avg_walkaway_risk: number;
  high_risk_count: number;
  strategic_count: number;
  walk_away_count: number;
  avg_price_to_value_score: number;
}

// ── Helpers ──────────────────────────────────────────────────────────────────

function riskColor(r: string) {
  return ({ minimal: "text-emerald-400", moderate: "text-amber-400", high: "text-orange-400", critical: "text-red-400" }[r] ?? "text-slate-400");
}

function riskBg(r: string) {
  return ({
    minimal:  "bg-emerald-900/30 border-emerald-700/50",
    moderate: "bg-amber-900/30 border-amber-700/50",
    high:     "bg-orange-900/30 border-orange-700/50",
    critical: "bg-red-900/30 border-red-700/50",
  }[r] ?? "bg-slate-800 border-slate-700");
}

function marginBadge(m: string) {
  return ({
    strong:   "bg-emerald-900/50 text-emerald-300 border border-emerald-700/50",
    healthy:  "bg-blue-900/50 text-blue-300 border border-blue-700/50",
    thin:     "bg-amber-900/50 text-amber-300 border border-amber-700/50",
    critical: "bg-red-900/50 text-red-300 border border-red-700/50",
  }[m] ?? "bg-slate-700 text-slate-300");
}

function strategyBadge(s: string) {
  return ({
    hold_price:        "bg-blue-900/50 text-blue-300 border border-blue-700/50",
    offer_value_add:   "bg-violet-900/50 text-violet-300 border border-violet-700/50",
    concede_strategic: "bg-indigo-900/50 text-indigo-300 border border-indigo-700/50",
    escalate_to_exec:  "bg-orange-900/50 text-orange-300 border border-orange-700/50",
    walk_away:         "bg-red-900/50 text-red-300 border border-red-700/50",
    accept_and_close:  "bg-emerald-900/50 text-emerald-300 border border-emerald-700/50",
  }[s] ?? "bg-slate-700 text-slate-300");
}

function fmtLabel(s: string) {
  return s.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
}

function fmtMoney(n: number) {
  if (n >= 1_000_000) return `${(n / 1_000_000).toFixed(1)}M€`;
  if (n >= 1_000)     return `${(n / 1_000).toFixed(0)}k€`;
  return `${n.toFixed(0)}€`;
}

// ── Margin Ring ───────────────────────────────────────────────────────────────

function MarginRing({ pct, size = 52 }: { pct: number; size?: number }) {
  const cx = size / 2, cy = size / 2;
  const r = size * 0.38;
  const circ = 2 * Math.PI * r;
  const arc = Math.max(0, (pct / 100)) * circ;
  const color = pct >= 60 ? "#34d399" : pct >= 45 ? "#60a5fa" : pct >= 30 ? "#fbbf24" : "#f87171";

  return (
    <svg width={size} height={size} className="flex-shrink-0">
      <circle cx={cx} cy={cy} r={r} stroke="#1e293b" strokeWidth={size * 0.12} fill="none" />
      <circle cx={cx} cy={cy} r={r} stroke={color} strokeWidth={size * 0.12} fill="none"
        strokeDasharray={`${arc} ${circ - arc}`} strokeLinecap="round"
        transform={`rotate(-90 ${cx} ${cy})`} />
      <text x={cx} y={cy + 1} textAnchor="middle" dominantBaseline="middle"
        fill={color} fontSize={size * 0.2} fontWeight="700">{Math.round(pct)}%</text>
    </svg>
  );
}

// ── Risk Distribution Bar ─────────────────────────────────────────────────────

function RiskDistBar({ counts }: { counts: Record<string, number> }) {
  const total = Object.values(counts).reduce((s, n) => s + n, 0);
  if (total === 0) return null;
  const order  = ["minimal", "moderate", "high", "critical"];
  const colors: Record<string, string> = { minimal: "bg-emerald-500", moderate: "bg-amber-500", high: "bg-orange-500", critical: "bg-red-500" };
  const entries = order.filter((k) => counts[k] != null).map((k) => [k, counts[k]] as [string, number]);
  return (
    <div className="space-y-1.5">
      <div className="flex h-2.5 rounded-full overflow-hidden gap-px">
        {entries.map(([k, v]) => (
          <div key={k} className={`${colors[k]} transition-all`} style={{ width: `${(v / total) * 100}%` }} />
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

// ── Deal Modal ────────────────────────────────────────────────────────────────

function DealModal({ deal, onClose }: { deal: Deal; onClose: () => void }) {
  const [tab, setTab] = useState<"pricing" | "leverage" | "details">("pricing");

  useEffect(() => {
    const fn = (e: KeyboardEvent) => e.key === "Escape" && onClose();
    document.addEventListener("keydown", fn);
    return () => document.removeEventListener("keydown", fn);
  }, [onClose]);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4" onClick={onClose}>
      <div className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-xl max-h-[90vh] overflow-y-auto shadow-2xl" onClick={(e) => e.stopPropagation()}>
        {/* Header */}
        <div className="p-5 border-b border-slate-800">
          <div className="flex items-start justify-between gap-3">
            <div className="flex-1 min-w-0">
              <div className="flex items-center gap-2 flex-wrap">
                <h2 className="text-slate-100 font-bold text-lg">{deal.deal_name}</h2>
                {deal.is_strategic && (
                  <span className="px-1.5 py-0.5 bg-indigo-900/50 text-indigo-300 border border-indigo-700/50 rounded text-xs font-medium">Strategic</span>
                )}
                {deal.multi_year_deal && (
                  <span className="px-1.5 py-0.5 bg-violet-900/50 text-violet-300 border border-violet-700/50 rounded text-xs font-medium">Multi-Year</span>
                )}
              </div>
              <p className="text-slate-400 text-sm mt-0.5">{deal.account_name} · {fmtLabel(deal.segment)} · {deal.days_to_close}d to close</p>
            </div>
            <button onClick={onClose} className="text-slate-500 hover:text-slate-300 text-xl leading-none flex-shrink-0">✕</button>
          </div>
          <div className="flex items-center gap-2 mt-3 flex-wrap">
            <span className={`px-2 py-0.5 rounded text-xs font-medium ${riskColor(deal.discount_risk)} bg-slate-800`}>
              {fmtLabel(deal.discount_risk)} risk
            </span>
            <span className={`px-2 py-0.5 rounded text-xs font-medium ${strategyBadge(deal.pricing_strategy)}`}>
              {fmtLabel(deal.pricing_strategy)}
            </span>
            <span className={`px-2 py-0.5 rounded text-xs font-medium ${marginBadge(deal.margin_health)}`}>
              {fmtLabel(deal.margin_health)} margin
            </span>
          </div>
        </div>

        {/* KPIs */}
        <div className="grid grid-cols-3 gap-px bg-slate-800 border-b border-slate-800">
          {[
            ["Gross Margin",  `${deal.gross_margin_pct}%`],
            ["Discount",      `${deal.effective_discount_pct}%`],
            ["Concession",    fmtMoney(deal.recommended_concession)],
          ].map(([label, val]) => (
            <div key={label} className="bg-slate-900 px-4 py-3 text-center">
              <div className="text-slate-400 text-xs">{label}</div>
              <div className="text-slate-100 font-bold text-base">{val}</div>
            </div>
          ))}
        </div>

        {/* Tabs */}
        <div className="flex border-b border-slate-800">
          {(["pricing", "leverage", "details"] as const).map((t) => (
            <button key={t} onClick={() => setTab(t)}
              className={`flex-1 py-2.5 text-sm font-medium transition-colors ${tab === t ? "text-indigo-400 border-b-2 border-indigo-500" : "text-slate-500 hover:text-slate-300"}`}>
              {t === "pricing" ? "Pricing" : t === "leverage" ? "Leverage" : "Details"}
            </button>
          ))}
        </div>

        <div className="p-5 space-y-3">
          {tab === "pricing" && (
            <div className="space-y-3">
              {[
                { label: "List Price",      value: fmtMoney(deal.list_price),        bar: 100,                                color: "bg-slate-500" },
                { label: "Proposed Price",  value: fmtMoney(deal.proposed_price),    bar: (deal.proposed_price / deal.list_price) * 100, color: "bg-indigo-500" },
                { label: "Price-to-Value",  value: `${deal.price_to_value_score}/100`, bar: deal.price_to_value_score,       color: "bg-violet-500" },
                { label: "Walkaway Risk",   value: `${deal.walkaway_risk}%`,          bar: deal.walkaway_risk,               color: deal.walkaway_risk >= 60 ? "bg-red-500" : "bg-amber-500" },
              ].map(({ label, value, bar, color }) => (
                <div key={label} className="space-y-1">
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-slate-300">{label}</span>
                    <span className="text-slate-100 font-semibold">{value}</span>
                  </div>
                  <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
                    <div className={`h-full ${color} rounded-full`} style={{ width: `${Math.min(100, bar)}%` }} />
                  </div>
                </div>
              ))}
              {deal.professional_services > 0 && (
                <div className="bg-slate-800/50 rounded-lg p-3 mt-2">
                  <div className="text-slate-500 text-xs">Professional Services Attached</div>
                  <div className="text-emerald-400 font-bold">{fmtMoney(deal.professional_services)}</div>
                </div>
              )}
            </div>
          )}

          {tab === "leverage" && (
            <div className="space-y-3">
              <div className="flex items-center gap-4 bg-slate-800/50 rounded-xl p-4">
                <MarginRing pct={deal.negotiation_leverage} size={64} />
                <div className="flex-1">
                  <div className="text-slate-300 font-semibold">Negotiation Leverage</div>
                  <div className="text-slate-400 text-sm mt-1">
                    {deal.negotiation_leverage >= 70 ? "Strong position" :
                     deal.negotiation_leverage >= 50 ? "Balanced position" : "Weak position"}
                  </div>
                </div>
              </div>
              <div className="text-slate-400 text-xs">Stage: <span className="text-slate-200 font-medium">{fmtLabel(deal.negotiation_stage)}</span></div>
            </div>
          )}

          {tab === "details" && (
            <div className="grid grid-cols-2 gap-3">
              {[
                ["Segment",       fmtLabel(deal.segment)],
                ["Days to Close", `${deal.days_to_close}d`],
                ["Multi-Year",    deal.multi_year_deal ? "Yes" : "No"],
                ["Strategic",     deal.is_strategic ? "Yes" : "No"],
                ["P→V Score",     `${deal.price_to_value_score}/100`],
                ["Walkaway",      `${deal.walkaway_risk}%`],
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

// ── Deal Card ─────────────────────────────────────────────────────────────────

function DealCard({ deal, onClick }: { deal: Deal; onClick: () => void }) {
  return (
    <button onClick={onClick}
      className={`w-full text-left p-4 rounded-xl border transition-all hover:border-indigo-500/50 hover:bg-slate-800/80 ${riskBg(deal.discount_risk)}`}>
      <div className="flex items-start gap-3">
        <MarginRing pct={deal.gross_margin_pct} size={52} />
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 flex-wrap mb-0.5">
            <span className="text-slate-100 font-semibold text-sm truncate">{deal.deal_name}</span>
            {deal.is_strategic && (
              <span className="px-1 py-0.5 bg-indigo-900/50 text-indigo-300 border border-indigo-700/50 rounded text-[10px] font-medium">STRATEGIC</span>
            )}
          </div>
          <p className="text-slate-400 text-xs truncate">{deal.account_name} · {fmtLabel(deal.segment)}</p>
          <div className="flex items-center gap-2 mt-1.5 flex-wrap">
            <span className={`px-1.5 py-0.5 rounded text-[10px] font-medium ${marginBadge(deal.margin_health)}`}>
              {fmtLabel(deal.margin_health)}
            </span>
            <span className={`px-1.5 py-0.5 rounded text-[10px] font-medium ${strategyBadge(deal.pricing_strategy)}`}>
              {fmtLabel(deal.pricing_strategy)}
            </span>
          </div>
        </div>
        <div className="text-right flex-shrink-0">
          <div className="text-indigo-300 font-bold text-sm">{fmtMoney(deal.proposed_price)}</div>
          <div className={`text-xs mt-0.5 ${riskColor(deal.discount_risk)}`}>-{deal.effective_discount_pct}%</div>
        </div>
      </div>

      {/* Leverage vs Walkaway */}
      <div className="mt-3 space-y-1">
        <div className="flex items-center gap-2">
          <span className="text-slate-600 text-[10px] w-14">Leverage</span>
          <div className="flex-1 h-1 bg-slate-800 rounded-full overflow-hidden">
            <div className="h-full bg-indigo-500 rounded-full" style={{ width: `${deal.negotiation_leverage}%` }} />
          </div>
          <span className="text-slate-500 text-[10px] w-6 text-right">{Math.round(deal.negotiation_leverage)}</span>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-slate-600 text-[10px] w-14">Walkaway</span>
          <div className="flex-1 h-1 bg-slate-800 rounded-full overflow-hidden">
            <div className={`h-full rounded-full ${deal.walkaway_risk >= 60 ? "bg-red-500" : "bg-amber-500"}`}
              style={{ width: `${deal.walkaway_risk}%` }} />
          </div>
          <span className="text-slate-500 text-[10px] w-6 text-right">{Math.round(deal.walkaway_risk)}</span>
        </div>
      </div>
    </button>
  );
}

// ── Page ──────────────────────────────────────────────────────────────────────

export default function PriceNegotiationPage() {
  const [data, setData]       = useState<{ deals: Deal[]; summary: Summary } | null>(null);
  const [loading, setLoading] = useState(true);
  const [riskFilter, setRiskFilter]         = useState("");
  const [strategyFilter, setStrategyFilter] = useState("");
  const [selected, setSelected]             = useState<Deal | null>(null);

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const params = new URLSearchParams();
      if (riskFilter)     params.set("risk", riskFilter);
      if (strategyFilter) params.set("strategy", strategyFilter);
      const res = await fetch(`/api/price-negotiation?${params}`);
      if (res.ok) setData(await res.json());
    } finally {
      setLoading(false);
    }
  }, [riskFilter, strategyFilter]);

  useEffect(() => { load(); }, [load]);

  const s     = data?.summary;
  const deals = data?.deals ?? [];

  const risks      = ["minimal", "moderate", "high", "critical"];
  const strategies = ["hold_price", "offer_value_add", "concede_strategic", "escalate_to_exec", "walk_away", "accept_and_close"];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {/* Header */}
      <div className="flex items-start justify-between gap-4 flex-wrap">
        <div>
          <h1 className="text-2xl font-bold text-slate-100">Price Negotiation</h1>
          <p className="text-slate-400 text-sm mt-1">Discount risk, margin health & negotiation strategy intelligence</p>
        </div>
        <button onClick={load} className="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg text-sm font-medium transition-colors">
          Refresh
        </button>
      </div>

      {/* KPI Strip */}
      {s && (
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
          {[
            { label: "Avg Margin",    value: `${s.avg_gross_margin_pct}%`,     sub: `avg discount ${s.avg_effective_discount}%` },
            { label: "Avg Leverage",  value: `${s.avg_negotiation_leverage}/100`, sub: `walkaway ${s.avg_walkaway_risk}%` },
            { label: "High Risk",     value: String(s.high_risk_count),         sub: `${s.walk_away_count} walk-away` },
            { label: "Strategic",     value: String(s.strategic_count),         sub: `${s.total} total deals` },
          ].map(({ label, value, sub }) => (
            <div key={label} className="bg-slate-900 border border-slate-800 rounded-xl p-4">
              <div className="text-slate-400 text-xs">{label}</div>
              <div className="text-slate-100 font-bold text-xl mt-1">{value}</div>
              <div className="text-slate-500 text-xs mt-0.5">{sub}</div>
            </div>
          ))}
        </div>
      )}

      {/* Risk Distribution */}
      {s && (
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
          <h2 className="text-slate-300 text-sm font-semibold mb-3">Discount Risk Distribution</h2>
          <RiskDistBar counts={s.risk_counts} />
        </div>
      )}

      {/* Filters */}
      <div className="flex gap-2 flex-wrap">
        <div className="flex items-center gap-1 bg-slate-900 border border-slate-800 rounded-lg px-2 py-1">
          <span className="text-slate-500 text-xs">Risk:</span>
          <div className="flex gap-1">
            {["", ...risks].map((r) => (
              <button key={r} onClick={() => setRiskFilter(r)}
                className={`px-2 py-0.5 rounded text-xs font-medium transition-colors ${riskFilter === r ? "bg-indigo-600 text-white" : "text-slate-400 hover:text-slate-200"}`}>
                {r ? fmtLabel(r) : "All"}
              </button>
            ))}
          </div>
        </div>
        <div className="flex items-center gap-1 bg-slate-900 border border-slate-800 rounded-lg px-2 py-1">
          <span className="text-slate-500 text-xs">Strategy:</span>
          <div className="flex gap-1">
            {["", ...strategies].map((s) => (
              <button key={s} onClick={() => setStrategyFilter(s)}
                className={`px-2 py-0.5 rounded text-xs font-medium transition-colors ${strategyFilter === s ? "bg-indigo-600 text-white" : "text-slate-400 hover:text-slate-200"}`}>
                {s ? fmtLabel(s) : "All"}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Deal Cards */}
      {loading ? (
        <div className="flex items-center justify-center py-16">
          <div className="w-8 h-8 border-2 border-indigo-500 border-t-transparent rounded-full animate-spin" />
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
          {deals.map((d) => (
            <DealCard key={d.deal_id} deal={d} onClick={() => setSelected(d)} />
          ))}
          {deals.length === 0 && (
            <div className="col-span-full text-center py-12 text-slate-500">No deals match the selected filters.</div>
          )}
        </div>
      )}

      {/* Strategy Summary */}
      {s && (
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
          <h2 className="text-slate-300 text-sm font-semibold mb-3">Pricing Strategy Distribution</h2>
          <div className="flex flex-wrap gap-2">
            {Object.entries(s.strategy_counts).sort((a, b) => b[1] - a[1]).map(([strat, count]) => (
              <div key={strat} className={`rounded-lg px-3 py-2 flex items-center gap-2 ${strategyBadge(strat)}`}>
                <span className="text-sm font-medium">{fmtLabel(strat)}</span>
                <span className="bg-black/20 text-xs font-bold px-1.5 py-0.5 rounded">{count}</span>
              </div>
            ))}
          </div>
          <div className="grid grid-cols-3 gap-3 mt-4">
            <div className="bg-slate-800/50 rounded-lg p-3">
              <div className="text-slate-500 text-xs">Avg P→V Score</div>
              <div className="text-slate-100 font-bold text-sm mt-1">{s.avg_price_to_value_score}/100</div>
            </div>
            {Object.entries(s.margin_health_counts).map(([m, c]) => (
              <div key={m} className="bg-slate-800/50 rounded-lg p-3">
                <div className="text-slate-500 text-xs">{fmtLabel(m)} Margin</div>
                <div className="text-slate-100 font-bold text-sm mt-1">{c} deals</div>
              </div>
            )).slice(0, 2)}
          </div>
        </div>
      )}

      {selected && <DealModal deal={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
