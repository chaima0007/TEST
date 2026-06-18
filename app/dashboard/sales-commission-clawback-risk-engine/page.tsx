"use client";

import { useEffect, useState, useCallback } from "react";

interface DealRecord {
  deal_id: string;
  rep_id: string;
  rep_name: string;
  region: string;
  deal_value_usd: number;
  commission_paid_usd: number;
  clawback_risk: string;
  clawback_likelihood: string;
  primary_clawback_reason: string;
  recommended_action: string;
  payment_risk_score: number;
  customer_stability_score: number;
  deal_integrity_score: number;
  rep_risk_score: number;
  clawback_composite: number;
  is_clawback_likely: boolean;
  requires_commission_hold: boolean;
  estimated_clawback_usd: number;
  clawback_signal: string;
}

interface Summary {
  total: number;
  risk_counts: Record<string, number>;
  likelihood_counts: Record<string, number>;
  reason_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_clawback_composite: number;
  clawback_likely_count: number;
  commission_hold_count: number;
  avg_payment_risk_score: number;
  avg_customer_stability_score: number;
  avg_deal_integrity_score: number;
  avg_rep_risk_score: number;
  total_estimated_clawback_usd: number;
}

const RISK_ORDER = ["low", "moderate", "high", "critical"];
const RISK_COLORS: Record<string, string> = {
  low:      "bg-emerald-900 text-emerald-300",
  moderate: "bg-amber-900 text-amber-300",
  high:     "bg-orange-900 text-orange-300",
  critical: "bg-red-900 text-red-300",
};
const RISK_RING: Record<string, string> = {
  low:      "#10b981",
  moderate: "#f59e0b",
  high:     "#f97316",
  critical: "#ef4444",
};
const LIKELIHOOD_COLORS: Record<string, string> = {
  unlikely: "bg-slate-700 text-slate-300",
  possible: "bg-amber-900 text-amber-300",
  probable: "bg-orange-900 text-orange-300",
  imminent: "bg-red-900 text-red-300",
};
const REASON_LABELS: Record<string, string> = {
  none:               "None",
  early_cancellation: "Early Cancellation",
  payment_failure:    "Payment Failure",
  contract_dispute:   "Contract Dispute",
  deal_revision:      "Deal Revision",
  customer_bankruptcy:"Customer Bankruptcy",
};
const ACTION_LABELS: Record<string, string> = {
  no_action:        "No Action",
  flag_for_review:  "Flag for Review",
  hold_commission:  "Hold Commission",
  partial_clawback: "Partial Clawback",
  full_clawback:    "Full Clawback",
};

function riskColor(v: number) {
  if (v < 20) return "#10b981";
  if (v < 45) return "#f59e0b";
  if (v < 65) return "#f97316";
  return "#ef4444";
}

function fmt(n: number) {
  return n >= 1_000_000
    ? `$${(n / 1_000_000).toFixed(1)}M`
    : n >= 1_000
    ? `$${(n / 1_000).toFixed(0)}K`
    : `$${n.toFixed(0)}`;
}

function ScoreBar({ label, value, color }: { label: string; value: number; color: string }) {
  return (
    <div>
      <div className="flex justify-between text-xs text-slate-400 mb-1">
        <span>{label}</span><span className="text-slate-200">{value.toFixed(0)}</span>
      </div>
      <div className="h-1.5 bg-slate-700 rounded-full overflow-hidden">
        <div className="h-full rounded-full" style={{ width: `${Math.min(value, 100)}%`, backgroundColor: color }} />
      </div>
    </div>
  );
}

function CompositeRing({ value, risk }: { value: number; risk: string }) {
  const r = 28; const circ = 2 * Math.PI * r;
  const fill = (Math.min(value, 100) / 100) * circ;
  const color = RISK_RING[risk] ?? "#475569";
  return (
    <svg width="72" height="72" viewBox="0 0 72 72">
      <circle cx="36" cy="36" r={r} fill="none" stroke="#1e293b" strokeWidth="7" />
      <circle cx="36" cy="36" r={r} fill="none" stroke={color} strokeWidth="7"
        strokeDasharray={`${fill} ${circ}`} strokeLinecap="round" transform="rotate(-90 36 36)" />
      <text x="36" y="40" textAnchor="middle" fill={color} fontSize="13" fontWeight="bold">{value.toFixed(0)}</text>
    </svg>
  );
}

function DetailModal({ deal, onClose }: { deal: DealRecord; onClose: () => void }) {
  const [tab, setTab] = useState(0);
  useEffect(() => {
    const fn = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", fn); return () => window.removeEventListener("keydown", fn);
  }, [onClose]);
  const tabs = ["Overview", "Risk Scores", "Commission Action"];
  const riskCls       = RISK_COLORS[deal.clawback_risk] ?? "bg-slate-700 text-slate-300";
  const likelihoodCls = LIKELIHOOD_COLORS[deal.clawback_likelihood] ?? "bg-slate-700 text-slate-300";
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4" onClick={onClose}>
      <div className="absolute inset-0 bg-black/70" />
      <div className="relative bg-slate-900 border border-slate-700 rounded-2xl shadow-2xl w-full max-w-lg" onClick={(e) => e.stopPropagation()}>
        <div className="flex items-start justify-between p-6 border-b border-slate-800">
          <div>
            <h2 className="text-lg font-semibold text-slate-100">{deal.deal_id}</h2>
            <p className="text-sm text-slate-400">{deal.rep_name} · {deal.region}</p>
            <div className="flex gap-2 mt-2 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${riskCls}`}>{deal.clawback_risk}</span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${likelihoodCls}`}>{deal.clawback_likelihood}</span>
              {deal.is_clawback_likely && <span className="px-2 py-0.5 rounded text-xs font-medium bg-red-900 text-red-300">⚠ Clawback Likely</span>}
              {deal.requires_commission_hold && <span className="px-2 py-0.5 rounded text-xs font-medium bg-amber-900 text-amber-300">🔒 Hold Commission</span>}
            </div>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-slate-300 text-xl ml-4">✕</button>
        </div>
        <div className="flex border-b border-slate-800">
          {tabs.map((t, i) => (
            <button key={t} onClick={() => setTab(i)}
              className={`flex-1 py-3 text-sm font-medium transition-colors ${tab === i ? "text-indigo-400 border-b-2 border-indigo-400" : "text-slate-500 hover:text-slate-300"}`}>
              {t}
            </button>
          ))}
        </div>
        <div className="p-6">
          {tab === 0 && (
            <div className="space-y-4">
              <div className="flex items-center gap-4 p-4 bg-slate-800 rounded-xl">
                <CompositeRing value={deal.clawback_composite} risk={deal.clawback_risk} />
                <div>
                  <p className="text-xs text-slate-400">Clawback Composite</p>
                  <p className="text-2xl font-bold text-slate-100">{deal.clawback_composite.toFixed(1)}</p>
                  <p className="text-xs text-slate-400 mt-1">Est. clawback: {fmt(deal.estimated_clawback_usd)}</p>
                </div>
              </div>
              <div className="p-4 bg-slate-800 rounded-xl">
                <p className="text-xs text-slate-400 mb-1">Signal</p>
                <p className="text-sm text-slate-200">{deal.clawback_signal}</p>
              </div>
              <div className="grid grid-cols-2 gap-3 text-sm">
                <div className="p-3 bg-slate-800 rounded-lg">
                  <p className="text-xs text-slate-400">Reason</p>
                  <p className="text-slate-200 font-medium">{REASON_LABELS[deal.primary_clawback_reason] ?? deal.primary_clawback_reason}</p>
                </div>
                <div className="p-3 bg-slate-800 rounded-lg">
                  <p className="text-xs text-slate-400">Deal Value</p>
                  <p className="text-slate-200 font-medium">{fmt(deal.deal_value_usd)}</p>
                </div>
                <div className="p-3 bg-slate-800 rounded-lg">
                  <p className="text-xs text-slate-400">Commission Paid</p>
                  <p className="text-slate-200 font-medium">{fmt(deal.commission_paid_usd)}</p>
                </div>
                <div className="p-3 bg-slate-800 rounded-lg">
                  <p className="text-xs text-slate-400">Est. Clawback</p>
                  <p className="text-orange-300 font-medium">{fmt(deal.estimated_clawback_usd)}</p>
                </div>
              </div>
            </div>
          )}
          {tab === 1 && (
            <div className="space-y-4">
              <ScoreBar label="Payment Risk"        value={deal.payment_risk_score}        color={riskColor(deal.payment_risk_score)} />
              <ScoreBar label="Customer Instability" value={deal.customer_stability_score}  color={riskColor(deal.customer_stability_score)} />
              <ScoreBar label="Deal Integrity"       value={deal.deal_integrity_score}      color={riskColor(deal.deal_integrity_score)} />
              <ScoreBar label="Rep Risk History"     value={deal.rep_risk_score}            color={riskColor(deal.rep_risk_score)} />
              <div className="mt-4 p-3 bg-slate-800 rounded-lg text-xs text-slate-400">
                Composite = Payment×0.35 + Customer×0.30 + Integrity×0.25 + Rep×0.10
              </div>
            </div>
          )}
          {tab === 2 && (
            <div className="space-y-4">
              <div className="p-4 bg-slate-800 rounded-xl">
                <p className="text-xs text-slate-400 mb-1">Recommended Action</p>
                <p className="text-lg font-semibold text-indigo-300">{ACTION_LABELS[deal.recommended_action] ?? deal.recommended_action}</p>
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div className={`p-3 rounded-lg ${deal.is_clawback_likely ? "bg-red-900/50 border border-red-700" : "bg-slate-800"}`}>
                  <p className="text-xs text-slate-400">Clawback Likely</p>
                  <p className={`font-semibold ${deal.is_clawback_likely ? "text-red-300" : "text-emerald-400"}`}>{deal.is_clawback_likely ? "YES" : "No"}</p>
                </div>
                <div className={`p-3 rounded-lg ${deal.requires_commission_hold ? "bg-amber-900/50 border border-amber-700" : "bg-slate-800"}`}>
                  <p className="text-xs text-slate-400">Commission Hold</p>
                  <p className={`font-semibold ${deal.requires_commission_hold ? "text-amber-300" : "text-emerald-400"}`}>{deal.requires_commission_hold ? "REQUIRED" : "No"}</p>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default function SalesCommissionClawbackRiskEnginePage() {
  const [data, setData]     = useState<{ deals: DealRecord[]; summary: Summary } | null>(null);
  const [filter, setFilter] = useState("all");
  const [selected, setSelected] = useState<DealRecord | null>(null);

  const load = useCallback((risk?: string) => {
    const params = risk && risk !== "all" ? `?risk=${risk}` : "";
    fetch(`/api/sales-commission-clawback-risk-engine${params}`).then((r) => r.json()).then(setData);
  }, []);

  useEffect(() => { load(); }, [load]);
  const handleFilter = (f: string) => { setFilter(f); load(f === "all" ? undefined : f); };

  if (!data) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-slate-400 animate-pulse">Loading commission clawback engine...</div>
    </div>
  );

  const { deals, summary } = data;
  const riskTotal = Object.values(summary.risk_counts).reduce((a, b) => a + b, 0) || 1;
  const reasonTotal = Object.values(summary.reason_counts).reduce((a, b) => a + b, 0) || 1;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
      {selected && <DetailModal deal={selected} onClose={() => setSelected(null)} />}
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-slate-100">Commission Clawback Risk Engine</h1>
        <p className="text-slate-400 text-sm mt-1">Closed deal integrity · payment risk · commission liability forecasting</p>
      </div>

      {/* KPI Strip */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        {[
          { label: "Total Deals", value: summary.total, sub: "monitored" },
          { label: "Clawback Likely", value: summary.clawback_likely_count, sub: "at risk", alert: summary.clawback_likely_count > 0 },
          { label: "Commission Hold", value: summary.commission_hold_count, sub: "pending", alert: summary.commission_hold_count > 0 },
          { label: "Est. Clawback", value: fmt(summary.total_estimated_clawback_usd), sub: "total at risk" },
        ].map(({ label, value, sub, alert }) => (
          <div key={label} className={`bg-slate-900 border rounded-xl p-4 ${alert ? "border-red-700" : "border-slate-800"}`}>
            <p className="text-xs text-slate-400">{label}</p>
            <p className={`text-2xl font-bold mt-1 ${alert ? "text-red-400" : "text-slate-100"}`}>{value}</p>
            <p className="text-xs text-slate-500 mt-1">{sub}</p>
          </div>
        ))}
      </div>

      {/* Avg Scores + Distributions */}
      <div className="grid lg:grid-cols-2 gap-4 mb-6">
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
          <h2 className="text-sm font-semibold text-slate-300 mb-4">Avg Risk Sub-Scores</h2>
          <div className="space-y-3">
            {[
              { label: "Payment Risk",         value: summary.avg_payment_risk_score },
              { label: "Customer Instability", value: summary.avg_customer_stability_score },
              { label: "Deal Integrity",        value: summary.avg_deal_integrity_score },
              { label: "Rep Risk History",      value: summary.avg_rep_risk_score },
            ].map(({ label, value }) => (
              <div key={label}>
                <div className="flex justify-between text-xs text-slate-400 mb-1">
                  <span>{label}</span><span className="text-slate-200">{value.toFixed(1)}</span>
                </div>
                <div className="h-2 bg-slate-700 rounded-full overflow-hidden">
                  <div className="h-full rounded-full" style={{ width: `${Math.min(value, 100)}%`, backgroundColor: riskColor(value) }} />
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-4">
          <div>
            <h2 className="text-sm font-semibold text-slate-300 mb-3">Clawback Risk Distribution</h2>
            <div className="space-y-2">
              {RISK_ORDER.map((lv) => {
                const cnt = summary.risk_counts[lv] ?? 0;
                return (
                  <div key={lv} className="flex items-center gap-2 text-xs">
                    <span className="w-20 text-slate-400 capitalize">{lv}</span>
                    <div className="flex-1 h-2 bg-slate-700 rounded-full overflow-hidden">
                      <div className="h-full rounded-full" style={{ width: `${(cnt / riskTotal) * 100}%`, backgroundColor: RISK_RING[lv] }} />
                    </div>
                    <span className="w-5 text-right text-slate-300">{cnt}</span>
                  </div>
                );
              })}
            </div>
          </div>
          <div>
            <h2 className="text-sm font-semibold text-slate-300 mb-3">Clawback Reason Distribution</h2>
            <div className="space-y-1.5">
              {Object.entries(summary.reason_counts).map(([reason, cnt]) => (
                <div key={reason} className="flex items-center gap-2 text-xs">
                  <span className="w-36 text-slate-400">{REASON_LABELS[reason] ?? reason}</span>
                  <div className="flex-1 h-1.5 bg-slate-700 rounded-full overflow-hidden">
                    <div className="h-full rounded-full bg-indigo-500" style={{ width: `${(cnt / reasonTotal) * 100}%` }} />
                  </div>
                  <span className="w-5 text-right text-slate-300">{cnt}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Filter tabs */}
      <div className="flex flex-wrap gap-2 mb-4">
        {["all", ...RISK_ORDER].map((lv) => (
          <button key={lv} onClick={() => handleFilter(lv)}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
              filter === lv ? "bg-indigo-600 text-white" : "bg-slate-800 text-slate-400 hover:text-slate-200"
            }`}>
            {lv === "all" ? "All Deals" : lv.charAt(0).toUpperCase() + lv.slice(1)}
            {lv !== "all" && (summary.risk_counts[lv] ?? 0) > 0 && (
              <span className="ml-1 text-slate-400">({summary.risk_counts[lv]})</span>
            )}
          </button>
        ))}
      </div>

      {/* Deal Cards */}
      <div className="grid sm:grid-cols-2 xl:grid-cols-3 gap-4">
        {deals.map((d) => {
          const riskCls       = RISK_COLORS[d.clawback_risk] ?? "bg-slate-700 text-slate-300";
          const likelihoodCls = LIKELIHOOD_COLORS[d.clawback_likelihood] ?? "bg-slate-700 text-slate-300";
          return (
            <div key={d.deal_id} onClick={() => setSelected(d)}
              className="bg-slate-900 border border-slate-800 rounded-xl p-4 cursor-pointer hover:border-slate-600 transition-colors">
              <div className="flex items-start justify-between mb-3">
                <div>
                  <p className="font-semibold text-slate-100">{d.deal_id}</p>
                  <p className="text-xs text-slate-400">{d.rep_name} · {d.region}</p>
                  <p className="text-xs text-slate-500 mt-0.5">{fmt(d.deal_value_usd)} deal · {fmt(d.commission_paid_usd)} commission</p>
                </div>
                <div className="flex flex-col gap-1 items-end">
                  <span className={`px-2 py-0.5 rounded text-xs font-medium ${riskCls}`}>{d.clawback_risk}</span>
                  <span className={`px-2 py-0.5 rounded text-xs font-medium ${likelihoodCls}`}>{d.clawback_likelihood}</span>
                </div>
              </div>
              <div className="flex items-center gap-3 mb-3">
                <CompositeRing value={d.clawback_composite} risk={d.clawback_risk} />
                <div className="flex-1 space-y-1.5">
                  <ScoreBar label="Payment Risk"    value={d.payment_risk_score}       color={riskColor(d.payment_risk_score)} />
                  <ScoreBar label="Customer"        value={d.customer_stability_score} color={riskColor(d.customer_stability_score)} />
                  <ScoreBar label="Deal Integrity"  value={d.deal_integrity_score}     color={riskColor(d.deal_integrity_score)} />
                  <ScoreBar label="Rep History"     value={d.rep_risk_score}           color={riskColor(d.rep_risk_score)} />
                </div>
              </div>
              <div className="flex gap-2 flex-wrap mb-2">
                {d.is_clawback_likely && <span className="text-xs text-red-400 bg-red-900/40 px-2 py-0.5 rounded">⚠ Clawback</span>}
                {d.requires_commission_hold && <span className="text-xs text-amber-300 bg-amber-900/40 px-2 py-0.5 rounded">🔒 Hold</span>}
                <span className="text-xs text-orange-300 bg-orange-900/30 px-2 py-0.5 rounded">{fmt(d.estimated_clawback_usd)} est.</span>
              </div>
              <p className="text-xs text-slate-400 line-clamp-2">{d.clawback_signal}</p>
            </div>
          );
        })}
      </div>
    </div>
  );
}
