"use client";

import { useEffect, useState } from "react";

interface LeakAccount {
  account_id: string;
  region: string;
  expansion_leak_risk: string;
  leak_pattern: string;
  leak_severity: string;
  recommended_action: string;
  upsell_neglect_score: number;
  cross_sell_gap_score: number;
  renewal_pricing_score: number;
  champion_leverage_score: number;
  expansion_leak_composite: number;
  is_revenue_leaking: boolean;
  requires_immediate_action: boolean;
  estimated_leaked_revenue_usd: number;
  leak_signal: string;
}

interface Summary {
  total: number;
  risk_counts: Record<string, number>;
  pattern_counts: Record<string, number>;
  severity_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_expansion_leak_composite: number;
  leaking_count: number;
  immediate_action_count: number;
  avg_upsell_neglect_score: number;
  avg_cross_sell_gap_score: number;
  avg_renewal_pricing_score: number;
  avg_champion_leverage_score: number;
  total_estimated_leaked_revenue_usd: number;
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
  captured: "text-emerald-400",
  watch:    "text-yellow-400",
  leaking:  "text-orange-400",
  critical: "text-red-400",
};
const PATTERN_LABELS: Record<string, string> = {
  none:                   "None",
  upsell_neglect:         "Upsell Neglect",
  cross_sell_gap:         "Cross-Sell Gap",
  renewal_underpricing:   "Renewal Underpricing",
  champion_not_leveraged: "Champion Not Leveraged",
  expansion_stall:        "Expansion Stall",
};
const ACTION_LABELS: Record<string, string> = {
  no_action:             "No Action",
  expansion_outreach:    "Expansion Outreach",
  qbr_scheduling:        "QBR Scheduling",
  pricing_renegotiation: "Pricing Renegotiation",
  executive_alignment:   "Executive Alignment",
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

function DetailModal({ account, onClose }: { account: LeakAccount; onClose: () => void }) {
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
              <span className="text-lg font-bold text-slate-100">{account.account_id}</span>
              <span className={`text-xs font-semibold px-2 py-0.5 rounded-full border ${RISK_BG[account.expansion_leak_risk]}`}>
                {account.expansion_leak_risk.toUpperCase()}
              </span>
              {account.is_revenue_leaking && (
                <span className="text-xs font-semibold px-2 py-0.5 rounded-full bg-red-400/10 border border-red-400/30 text-red-400">LEAKING</span>
              )}
            </div>
            <div className="text-sm text-slate-400">{account.region} · {PATTERN_LABELS[account.leak_pattern]}</div>
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
                <CompositeRing value={account.expansion_leak_composite} />
                <div>
                  <div className="text-sm text-slate-400">Expansion Leak Composite</div>
                  <div className="text-2xl font-bold text-slate-100">{account.expansion_leak_composite.toFixed(1)}</div>
                  <div className={`text-sm font-medium ${SEV_COLORS[account.leak_severity]}`}>
                    {account.leak_severity.charAt(0).toUpperCase() + account.leak_severity.slice(1)}
                  </div>
                </div>
              </div>
              <div className="bg-slate-800/50 rounded-xl p-4 text-sm text-slate-300 italic">
                &ldquo;{account.leak_signal}&rdquo;
              </div>
              <div className="grid grid-cols-2 gap-3 text-sm">
                <div className="bg-slate-800/50 rounded-xl p-3">
                  <div className="text-slate-400 text-xs mb-1">Est. Leaked Revenue</div>
                  <div className="text-orange-400 font-bold">${account.estimated_leaked_revenue_usd.toLocaleString()}</div>
                </div>
                <div className="bg-slate-800/50 rounded-xl p-3">
                  <div className="text-slate-400 text-xs mb-1">Immediate Action</div>
                  <div className={account.requires_immediate_action ? "text-red-400 font-bold" : "text-emerald-400 font-bold"}>
                    {account.requires_immediate_action ? "Yes" : "No"}
                  </div>
                </div>
              </div>
            </div>
          )}
          {tab === "scores" && (
            <div className="space-y-3">
              <ScoreBar label="Upsell Neglect"    value={account.upsell_neglect_score}    color="bg-yellow-400" />
              <ScoreBar label="Cross-Sell Gap"    value={account.cross_sell_gap_score}    color="bg-orange-400" />
              <ScoreBar label="Renewal Pricing"   value={account.renewal_pricing_score}   color="bg-purple-400" />
              <ScoreBar label="Champion Leverage" value={account.champion_leverage_score} color="bg-red-400" />
              <div className="border-t border-slate-800 pt-3 mt-2">
                <ScoreBar label="Composite"       value={account.expansion_leak_composite} color="bg-indigo-400" />
              </div>
            </div>
          )}
          {tab === "action" && (
            <div className="space-y-3">
              <div className="bg-indigo-500/10 border border-indigo-500/30 rounded-xl p-4">
                <div className="text-xs text-indigo-300 mb-1">Recommended Action</div>
                <div className="text-indigo-200 font-semibold">{ACTION_LABELS[account.recommended_action]}</div>
              </div>
              <div className="grid grid-cols-2 gap-3 text-sm">
                <div className="bg-slate-800/50 rounded-xl p-3">
                  <div className="text-slate-400 text-xs mb-1">Pattern</div>
                  <div className="text-slate-200 text-xs">{PATTERN_LABELS[account.leak_pattern]}</div>
                </div>
                <div className="bg-slate-800/50 rounded-xl p-3">
                  <div className="text-slate-400 text-xs mb-1">Severity</div>
                  <div className={SEV_COLORS[account.leak_severity]}>
                    {account.leak_severity.charAt(0).toUpperCase() + account.leak_severity.slice(1)}
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

export default function CustomerExpansionRevenueLeakDetectorPage() {
  const [data,       setData]       = useState<{ accounts: LeakAccount[]; summary: Summary } | null>(null);
  const [loading,    setLoading]    = useState(true);
  const [riskFilter, setRiskFilter] = useState("all");
  const [patFilter,  setPatFilter]  = useState("all");
  const [selected,   setSelected]   = useState<LeakAccount | null>(null);

  useEffect(() => {
    async function load() {
        setLoading(true);
        try {
          const params = new URLSearchParams();
          if (riskFilter !== "all") params.set("risk", riskFilter);
          if (patFilter  !== "all") params.set("pattern", patFilter);
          const res = await fetch(`/api/customer-expansion-revenue-leak-detector?${params}`);
          setData(await res.json());
        } finally { setLoading(false); }
  }
    load();
  }, [riskFilter, patFilter]);

  const s = data?.summary;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
      {selected && <DetailModal account={selected} onClose={() => setSelected(null)} />}

      <div className="max-w-7xl mx-auto space-y-6">
        {/* Header */}
        <div>
          <h1 className="text-2xl font-bold text-slate-100">Customer Expansion Revenue Leak Detector</h1>
          <p className="text-slate-400 text-sm mt-1">
            Detect missed expansion revenue — upsell neglect, cross-sell gaps, renewal underpricing &amp; champion leverage failures
          </p>
        </div>

        {/* KPI Strip */}
        {s && (
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {[
              { label: "Total Accounts",    value: s.total,                                 color: "text-slate-100" },
              { label: "Revenue Leaking",   value: s.leaking_count,                         color: "text-red-400" },
              { label: "Immediate Action",  value: s.immediate_action_count,                color: "text-orange-400" },
              { label: "Avg Composite",     value: s.avg_expansion_leak_composite.toFixed(1), color: "text-indigo-400" },
            ].map(({ label, value, color }) => (
              <div key={label} className="bg-slate-900 border border-slate-800 rounded-xl p-4">
                <div className="text-xs text-slate-400 mb-1">{label}</div>
                <div className={`text-2xl font-bold ${color}`}>{value}</div>
              </div>
            ))}
          </div>
        )}

        {/* Leaked Revenue Banner */}
        {s && (
          <div className="bg-orange-500/5 border border-orange-500/20 rounded-xl p-4 flex items-center justify-between">
            <div>
              <div className="text-xs text-orange-300 mb-1">Total Estimated Leaked Revenue</div>
              <div className="text-2xl font-bold text-orange-400">
                ${s.total_estimated_leaked_revenue_usd.toLocaleString(undefined, { minimumFractionDigits: 0, maximumFractionDigits: 0 })}
              </div>
            </div>
            <div className="text-right text-xs text-slate-400 space-y-0.5">
              <div>Avg Upsell Neglect {s.avg_upsell_neglect_score.toFixed(1)}</div>
              <div>Avg Cross-Sell Gap {s.avg_cross_sell_gap_score.toFixed(1)}</div>
              <div>Avg Renewal Pricing {s.avg_renewal_pricing_score.toFixed(1)}</div>
            </div>
          </div>
        )}

        {/* Distribution bars */}
        {s && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {(
              [
                { title: "By Risk Level", counts: s.risk_counts,    colors: { low:"bg-emerald-400", moderate:"bg-yellow-400", high:"bg-orange-400", critical:"bg-red-400" } as Record<string,string> },
                { title: "By Pattern",    counts: s.pattern_counts, colors: { none:"bg-slate-500", upsell_neglect:"bg-yellow-400", cross_sell_gap:"bg-orange-400", renewal_underpricing:"bg-purple-400", champion_not_leveraged:"bg-red-400", expansion_stall:"bg-red-600" } as Record<string,string> },
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
          {["all","upsell_neglect","cross_sell_gap","renewal_underpricing","champion_not_leveraged","expansion_stall"].map((p) => (
            <button key={p} onClick={() => setPatFilter(p)}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium capitalize transition-colors ${patFilter===p ? "bg-violet-600 text-white" : "bg-slate-800 text-slate-400 hover:text-slate-200"}`}>
              {p === "all" ? "All Patterns" : p.replace(/_/g," ")}
            </button>
          ))}
        </div>

        {/* Account Cards */}
        {loading ? (
          <div className="text-center text-slate-500 py-16">Loading…</div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
            {data?.accounts.map((account) => (
              <button key={account.account_id} onClick={() => setSelected(account)}
                className="bg-slate-900 border border-slate-800 rounded-xl p-4 text-left hover:border-slate-600 transition-colors group">
                <div className="flex items-start justify-between mb-3">
                  <div>
                    <div className="flex items-center gap-2 mb-0.5">
                      <span className="font-semibold text-slate-100">{account.account_id}</span>
                      {account.is_revenue_leaking && (
                        <span className="text-xs bg-red-400/10 border border-red-400/30 text-red-400 px-1.5 py-0.5 rounded-full">LEAKING</span>
                      )}
                    </div>
                    <div className="text-xs text-slate-400">{account.region}</div>
                  </div>
                  <CompositeRing value={account.expansion_leak_composite} />
                </div>

                <div className="flex flex-wrap gap-1.5 mb-3">
                  <span className={`text-xs px-2 py-0.5 rounded-full border font-medium ${RISK_BG[account.expansion_leak_risk]} ${RISK_COLORS[account.expansion_leak_risk]}`}>
                    {account.expansion_leak_risk}
                  </span>
                  <span className={`text-xs font-medium ${SEV_COLORS[account.leak_severity]}`}>
                    {account.leak_severity}
                  </span>
                </div>

                <div className="text-xs text-slate-400 italic line-clamp-2 mb-3">&ldquo;{account.leak_signal}&rdquo;</div>

                <div className="grid grid-cols-2 gap-2 text-xs">
                  <div className="bg-slate-800/50 rounded-lg p-2">
                    <div className="text-slate-500 mb-0.5">Pattern</div>
                    <div className="text-slate-300 truncate">{PATTERN_LABELS[account.leak_pattern]}</div>
                  </div>
                  <div className="bg-slate-800/50 rounded-lg p-2">
                    <div className="text-slate-500 mb-0.5">Leaked Revenue</div>
                    <div className="text-orange-400 font-medium">${account.estimated_leaked_revenue_usd.toLocaleString()}</div>
                  </div>
                </div>

                {account.requires_immediate_action && (
                  <div className="mt-2 text-xs bg-amber-500/10 border border-amber-500/20 text-amber-400 rounded-lg px-2 py-1 text-center">
                    Immediate Action Required
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
