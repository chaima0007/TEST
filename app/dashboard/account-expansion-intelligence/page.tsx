"use client";

import { useState, useEffect, useCallback } from "react";

interface AccountData {
  account_id: string;
  account_name: string;
  rep_id: string;
  expansion_opportunity: string;
  expansion_priority: string;
  account_health: string;
  expansion_action: string;
  adoption_health_score: number;
  relationship_health_score: number;
  commercial_readiness_score: number;
  risk_score: number;
  expansion_composite: number;
  estimated_expansion_arr_usd: number;
  is_expansion_ready: boolean;
  needs_retention_focus: boolean;
  primary_expansion_signal: string;
  contract_value_usd: number;
  contract_renewal_days: number;
  nps_score: number;
}

interface Summary {
  total: number;
  opportunity_counts: Record<string, number>;
  priority_counts: Record<string, number>;
  health_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_expansion_composite: number;
  expansion_ready_count: number;
  retention_focus_count: number;
  avg_adoption_health_score: number;
  avg_relationship_health_score: number;
  avg_commercial_readiness_score: number;
  avg_risk_score: number;
  total_expansion_arr_potential_usd: number;
}

const OPP_COLOR: Record<string, string> = {
  upsell: "text-indigo-400",
  cross_sell: "text-violet-400",
  renewal_upgrade: "text-sky-400",
  whitespace: "text-emerald-400",
  at_risk: "text-rose-400",
};

const OPP_BG: Record<string, string> = {
  upsell: "bg-indigo-500/20 text-indigo-300 border-indigo-500/30",
  cross_sell: "bg-violet-500/20 text-violet-300 border-violet-500/30",
  renewal_upgrade: "bg-sky-500/20 text-sky-300 border-sky-500/30",
  whitespace: "bg-emerald-500/20 text-emerald-300 border-emerald-500/30",
  at_risk: "bg-rose-500/20 text-rose-300 border-rose-500/30",
};

const PRIORITY_BG: Record<string, string> = {
  critical: "bg-rose-500/20 text-rose-300 border-rose-500/30",
  high: "bg-orange-500/20 text-orange-300 border-orange-500/30",
  medium: "bg-yellow-500/20 text-yellow-300 border-yellow-500/30",
  low: "bg-slate-500/20 text-slate-300 border-slate-500/30",
};

const HEALTH_BG: Record<string, string> = {
  champion: "bg-emerald-500/20 text-emerald-300 border-emerald-500/30",
  healthy: "bg-sky-500/20 text-sky-300 border-sky-500/30",
  stable: "bg-yellow-500/20 text-yellow-300 border-yellow-500/30",
  at_risk: "bg-rose-500/20 text-rose-300 border-rose-500/30",
};

function fmtCurrency(v: number): string {
  if (v >= 1_000_000) return `$${(v / 1_000_000).toFixed(1)}M`;
  if (v >= 1_000) return `$${(v / 1_000).toFixed(0)}K`;
  return `$${v.toFixed(0)}`;
}

function fmtLabel(s: string): string {
  return s.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
}

function ExpansionRing({ score, color }: { score: number; color: string }) {
  const r = 38, cx = 44, cy = 44, stroke = 7;
  const circ = 2 * Math.PI * r;
  const fill = (score / 100) * circ;
  return (
    <svg width={88} height={88} viewBox="0 0 88 88">
      <circle cx={cx} cy={cy} r={r} fill="none" stroke="#1e293b" strokeWidth={stroke} />
      <circle cx={cx} cy={cy} r={r} fill="none" stroke={color} strokeWidth={stroke}
        strokeDasharray={`${fill} ${circ}`} strokeLinecap="round"
        transform={`rotate(-90 ${cx} ${cy})`} />
      <text x={cx} y={cy + 1} textAnchor="middle" dominantBaseline="middle"
        fill="white" fontSize={14} fontWeight={700}>{Math.round(score)}</text>
    </svg>
  );
}

function OpportunityDistBar({ counts }: { counts: Record<string, number> }) {
  const order = ["upsell", "cross_sell", "renewal_upgrade", "whitespace", "at_risk"];
  const total = Object.values(counts).reduce((s, v) => s + v, 0) || 1;
  const colors: Record<string, string> = {
    upsell: "bg-indigo-500", cross_sell: "bg-violet-500",
    renewal_upgrade: "bg-sky-500", whitespace: "bg-emerald-500", at_risk: "bg-rose-500",
  };
  return (
    <div className="space-y-2">
      <div className="flex rounded-full overflow-hidden h-3">
        {order.filter((o) => counts[o]).map((o) => (
          <div key={o} className={`${colors[o]} transition-all`}
            style={{ width: `${(counts[o] / total) * 100}%` }} />
        ))}
      </div>
      <div className="flex flex-wrap gap-3">
        {order.filter((o) => counts[o]).map((o) => (
          <span key={o} className="flex items-center gap-1 text-xs text-slate-400">
            <span className={`w-2 h-2 rounded-full ${colors[o]}`} />
            {fmtLabel(o)} ({counts[o]})
          </span>
        ))}
      </div>
    </div>
  );
}

function AccountModal({ account, onClose }: { account: AccountData; onClose: () => void }) {
  const [tab, setTab] = useState<"scores" | "details" | "actions">("scores");

  useEffect(() => {
    const handler = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [onClose]);

  const scores = [
    { label: "Adoption Health", value: account.adoption_health_score, color: "#6366f1" },
    { label: "Relationship Health", value: account.relationship_health_score, color: "#8b5cf6" },
    { label: "Commercial Readiness", value: account.commercial_readiness_score, color: "#0ea5e9" },
    { label: "Risk Score", value: account.risk_score, color: "#f43f5e" },
  ];

  return (
    <div className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-4"
      onClick={onClose}>
      <div className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-xl shadow-2xl"
        onClick={(e) => e.stopPropagation()}>
        <div className="p-6 border-b border-slate-800">
          <div className="flex items-start justify-between gap-3">
            <div>
              <h2 className="text-lg font-bold text-white">{account.account_name}</h2>
              <p className="text-sm text-slate-400 mt-0.5">
                {fmtCurrency(account.contract_value_usd)} ARR · Renewal in {account.contract_renewal_days}d · NPS {account.nps_score > 0 ? "+" : ""}{account.nps_score}
              </p>
            </div>
            <div className="flex flex-col items-end gap-1">
              <span className={`text-xs px-2 py-0.5 rounded-full border ${OPP_BG[account.expansion_opportunity]}`}>
                {fmtLabel(account.expansion_opportunity)}
              </span>
              <span className={`text-xs px-2 py-0.5 rounded-full border ${HEALTH_BG[account.account_health]}`}>
                {fmtLabel(account.account_health)}
              </span>
            </div>
          </div>
          <div className="flex gap-2 mt-4">
            {(["scores", "details", "actions"] as const).map((t) => (
              <button key={t} onClick={() => setTab(t)}
                className={`px-3 py-1 rounded-lg text-sm font-medium transition-colors ${
                  tab === t ? "bg-indigo-600 text-white" : "text-slate-400 hover:text-white"
                }`}>{t.charAt(0).toUpperCase() + t.slice(1)}</button>
            ))}
          </div>
        </div>

        <div className="p-6 space-y-4">
          {tab === "scores" && (
            <div className="grid grid-cols-2 gap-4">
              {scores.map(({ label, value, color }) => (
                <div key={label} className="bg-slate-800/50 rounded-xl p-4 flex items-center gap-3">
                  <ExpansionRing score={value} color={color} />
                  <div>
                    <p className="text-xs text-slate-400">{label}</p>
                    <p className="text-xl font-bold text-white">{value.toFixed(0)}</p>
                  </div>
                </div>
              ))}
              <div className="col-span-2 bg-slate-800/50 rounded-xl p-4 flex items-center justify-between">
                <div>
                  <p className="text-xs text-slate-400">Expansion Composite</p>
                  <p className="text-3xl font-bold text-indigo-400">{account.expansion_composite.toFixed(1)}</p>
                </div>
                <div className="text-right">
                  <p className="text-xs text-slate-400">Est. Expansion ARR</p>
                  <p className="text-2xl font-bold text-emerald-400">{fmtCurrency(account.estimated_expansion_arr_usd)}</p>
                </div>
              </div>
            </div>
          )}
          {tab === "details" && (
            <div className="space-y-3">
              <div className="bg-slate-800/50 rounded-xl p-4">
                <p className="text-xs text-slate-400 mb-1">Primary Expansion Signal</p>
                <p className="text-sm text-white font-medium">{account.primary_expansion_signal}</p>
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div className="bg-slate-800/50 rounded-xl p-3">
                  <p className="text-xs text-slate-400">Contract Value</p>
                  <p className="text-base font-bold text-white">{fmtCurrency(account.contract_value_usd)}</p>
                </div>
                <div className="bg-slate-800/50 rounded-xl p-3">
                  <p className="text-xs text-slate-400">Days to Renewal</p>
                  <p className="text-base font-bold text-white">{account.contract_renewal_days}d</p>
                </div>
                <div className="bg-slate-800/50 rounded-xl p-3">
                  <p className="text-xs text-slate-400">NPS Score</p>
                  <p className={`text-base font-bold ${account.nps_score >= 50 ? "text-emerald-400" : account.nps_score >= 0 ? "text-yellow-400" : "text-rose-400"}`}>
                    {account.nps_score > 0 ? "+" : ""}{account.nps_score}
                  </p>
                </div>
                <div className="bg-slate-800/50 rounded-xl p-3">
                  <p className="text-xs text-slate-400">Priority</p>
                  <span className={`text-xs px-2 py-0.5 rounded-full border ${PRIORITY_BG[account.expansion_priority]}`}>
                    {fmtLabel(account.expansion_priority)}
                  </span>
                </div>
              </div>
              <div className="flex gap-2">
                {account.is_expansion_ready && (
                  <span className="text-xs px-2 py-1 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
                    Expansion Ready
                  </span>
                )}
                {account.needs_retention_focus && (
                  <span className="text-xs px-2 py-1 rounded-full bg-rose-500/20 text-rose-300 border border-rose-500/30">
                    Retention Priority
                  </span>
                )}
              </div>
            </div>
          )}
          {tab === "actions" && (
            <div className="space-y-3">
              <div className="bg-indigo-600/20 border border-indigo-500/30 rounded-xl p-4">
                <p className="text-xs text-indigo-300 mb-1">Recommended Action</p>
                <p className="text-sm font-semibold text-white">{fmtLabel(account.expansion_action)}</p>
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div className="bg-slate-800/50 rounded-xl p-3">
                  <p className="text-xs text-slate-400">Opportunity Type</p>
                  <span className={`text-xs px-2 py-0.5 rounded-full border ${OPP_BG[account.expansion_opportunity]}`}>
                    {fmtLabel(account.expansion_opportunity)}
                  </span>
                </div>
                <div className="bg-slate-800/50 rounded-xl p-3">
                  <p className="text-xs text-slate-400">Account Health</p>
                  <span className={`text-xs px-2 py-0.5 rounded-full border ${HEALTH_BG[account.account_health]}`}>
                    {fmtLabel(account.account_health)}
                  </span>
                </div>
              </div>
              <div className="bg-slate-800/50 rounded-xl p-4">
                <p className="text-xs text-slate-400 mb-1">Est. Expansion ARR Potential</p>
                <p className="text-2xl font-bold text-emerald-400">{fmtCurrency(account.estimated_expansion_arr_usd)}</p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

function AccountCard({ account, onClick }: { account: AccountData; onClick: () => void }) {
  const ringColor = account.expansion_composite >= 75 ? "#6366f1"
    : account.expansion_composite >= 55 ? "#8b5cf6"
    : account.expansion_composite >= 40 ? "#f59e0b"
    : "#f43f5e";

  return (
    <div onClick={onClick}
      className="bg-slate-900 border border-slate-800 rounded-xl p-4 cursor-pointer hover:border-indigo-500/50 transition-all hover:bg-slate-800/50 group">
      <div className="flex items-start gap-3 mb-3">
        <ExpansionRing score={account.expansion_composite} color={ringColor} />
        <div className="flex-1 min-w-0">
          <p className="font-semibold text-white truncate group-hover:text-indigo-300 transition-colors">
            {account.account_name}
          </p>
          <p className="text-xs text-slate-400 mt-0.5">{fmtCurrency(account.contract_value_usd)} ARR · {account.contract_renewal_days}d renewal</p>
          <div className="flex flex-wrap gap-1 mt-1.5">
            <span className={`text-xs px-1.5 py-0.5 rounded border ${OPP_BG[account.expansion_opportunity]}`}>
              {fmtLabel(account.expansion_opportunity)}
            </span>
            <span className={`text-xs px-1.5 py-0.5 rounded border ${HEALTH_BG[account.account_health]}`}>
              {fmtLabel(account.account_health)}
            </span>
          </div>
        </div>
      </div>
      <p className="text-xs text-slate-400 line-clamp-1 mb-2">{account.primary_expansion_signal}</p>
      <div className="flex items-center justify-between text-xs">
        <span className="text-emerald-400 font-semibold">{fmtCurrency(account.estimated_expansion_arr_usd)} potential</span>
        <span className={`px-1.5 py-0.5 rounded border ${PRIORITY_BG[account.expansion_priority]}`}>
          {fmtLabel(account.expansion_priority)}
        </span>
      </div>
    </div>
  );
}

export default function AccountExpansionIntelligencePage() {
  const [data, setData] = useState<{ accounts: AccountData[]; summary: Summary } | null>(null);
  const [selected, setSelected] = useState<AccountData | null>(null);
  const [filterOpp, setFilterOpp] = useState("all");
  const [filterHealth, setFilterHealth] = useState("all");

  const load = useCallback(async () => {
    const params = new URLSearchParams();
    if (filterOpp !== "all") params.set("opportunity", filterOpp);
    if (filterHealth !== "all") params.set("health", filterHealth);
    const res = await fetch(`/api/account-expansion-intelligence?${params}`);
    if (res.ok) setData(await res.json());
  }, [filterOpp, filterHealth]);

  useEffect(() => { load(); }, [load]);

  const s = data?.summary;
  const kpis = [
    { label: "Total Accounts", value: s?.total ?? 0, sub: "tracked" },
    { label: "Expansion Ready", value: s?.expansion_ready_count ?? 0, sub: "budget confirmed", color: "text-emerald-400" },
    { label: "Retention Focus", value: s?.retention_focus_count ?? 0, sub: "at risk", color: "text-rose-400" },
    { label: "Avg Composite", value: `${s?.avg_expansion_composite ?? 0}`, sub: "/ 100" },
    { label: "ARR Potential", value: fmtCurrency(s?.total_expansion_arr_potential_usd ?? 0), sub: "expansion" },
    { label: "Avg Risk", value: `${s?.avg_risk_score ?? 0}`, sub: "/ 100", color: (s?.avg_risk_score ?? 0) > 40 ? "text-rose-400" : "text-emerald-400" },
  ];

  const oppFilters = ["all", "upsell", "cross_sell", "renewal_upgrade", "whitespace", "at_risk"];
  const healthFilters = ["all", "champion", "healthy", "stable", "at_risk"];

  return (
    <main className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white">Account Expansion Intelligence</h1>
        <p className="text-sm text-slate-400 mt-1">Upsell, cross-sell, and retention signals across your customer base</p>
      </div>

      {/* KPI strip */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {kpis.map(({ label, value, sub, color }) => (
          <div key={label} className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <p className="text-xs text-slate-400">{label}</p>
            <p className={`text-2xl font-bold mt-1 ${color ?? "text-white"}`}>{value}</p>
            <p className="text-xs text-slate-500 mt-0.5">{sub}</p>
          </div>
        ))}
      </div>

      {/* Distribution */}
      {s && (
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
          <p className="text-sm font-medium text-slate-300 mb-3">Opportunity Distribution</p>
          <OpportunityDistBar counts={s.opportunity_counts} />
        </div>
      )}

      {/* Filters */}
      <div className="flex flex-wrap gap-3">
        <div className="flex flex-wrap gap-1">
          <span className="text-xs text-slate-500 self-center mr-1">Opportunity:</span>
          {oppFilters.map((f) => (
            <button key={f} onClick={() => setFilterOpp(f)}
              className={`text-xs px-3 py-1.5 rounded-lg border transition-colors ${
                filterOpp === f
                  ? "bg-indigo-600 border-indigo-500 text-white"
                  : "border-slate-700 text-slate-400 hover:border-slate-500"
              }`}>
              {f === "all" ? "All" : fmtLabel(f)}
            </button>
          ))}
        </div>
        <div className="flex flex-wrap gap-1">
          <span className="text-xs text-slate-500 self-center mr-1">Health:</span>
          {healthFilters.map((f) => (
            <button key={f} onClick={() => setFilterHealth(f)}
              className={`text-xs px-3 py-1.5 rounded-lg border transition-colors ${
                filterHealth === f
                  ? "bg-violet-600 border-violet-500 text-white"
                  : "border-slate-700 text-slate-400 hover:border-slate-500"
              }`}>
              {f === "all" ? "All" : fmtLabel(f)}
            </button>
          ))}
        </div>
      </div>

      {/* Account grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {data?.accounts.map((a) => (
          <AccountCard key={a.account_id} account={a} onClick={() => setSelected(a)} />
        ))}
        {data?.accounts.length === 0 && (
          <div className="col-span-full text-center text-slate-500 py-12">No accounts match the selected filters.</div>
        )}
      </div>

      {selected && <AccountModal account={selected} onClose={() => setSelected(null)} />}
    </main>
  );
}
