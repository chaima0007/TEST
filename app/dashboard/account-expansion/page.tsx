"use client";

import { useEffect, useState } from "react";

// ── Types ────────────────────────────────────────────────────────────────────

interface Account {
  account_id: string;
  account_name: string;
  csm_id: string;
  segment: string;
  current_arr: number;
  contract_end_days: number;
  expansion_type: string;
  expansion_readiness: string;
  churn_signal: string;
  expansion_action: string;
  expansion_score: number;
  health_score: number;
  churn_risk_score: number;
  adoption_rate: number;
  feature_utilization: number;
  expansion_potential: number;
  nrr_forecast: number;
  is_at_risk: boolean;
  is_ready_to_expand: boolean;
  active_users: number;
  licensed_users: number;
  nps_score: number;
  whitespace_products: number;
  growth_since_start_pct: number;
}

interface Summary {
  total: number;
  readiness_counts: Record<string, number>;
  churn_signal_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_health_score: number;
  avg_expansion_score: number;
  avg_churn_risk_score: number;
  avg_nrr_forecast: number;
  total_expansion_potential: number;
  at_risk_count: number;
  ready_to_expand_count: number;
  high_value_count: number;
}

// ── Helpers ──────────────────────────────────────────────────────────────────

function churnColor(c: string) {
  return ({ none: "text-emerald-400", low: "text-blue-400", medium: "text-amber-400", high: "text-orange-400", critical: "text-red-400" }[c] ?? "text-slate-400");
}

function readinessBg(r: string) {
  return ({
    ready_now:       "bg-emerald-900/30 border-emerald-700/50",
    upcoming:        "bg-blue-900/30 border-blue-700/50",
    needs_nurturing: "bg-amber-900/30 border-amber-700/50",
    not_ready:       "bg-red-900/30 border-red-700/50",
  }[r] ?? "bg-slate-800 border-slate-700");
}

function actionBadge(a: string) {
  return ({
    pitch_now:          "bg-emerald-900/50 text-emerald-300 border border-emerald-700/50",
    schedule_qbr:       "bg-blue-900/50 text-blue-300 border border-blue-700/50",
    nurture_adoption:   "bg-violet-900/50 text-violet-300 border border-violet-700/50",
    risk_intervention:  "bg-red-900/50 text-red-300 border border-red-700/50",
    reactivate:         "bg-orange-900/50 text-orange-300 border border-orange-700/50",
    maintain_health:    "bg-slate-700/50 text-slate-300 border border-slate-600/50",
  }[a] ?? "bg-slate-700 text-slate-300");
}

function fmtLabel(s: string) {
  return s.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
}

function fmtMoney(n: number) {
  if (n >= 1_000_000) return `${(n / 1_000_000).toFixed(1)}M€`;
  if (n >= 1_000)     return `${(n / 1_000).toFixed(0)}k€`;
  return `${n.toFixed(0)}€`;
}

// ── Health Ring ───────────────────────────────────────────────────────────────

function HealthRing({ score, size = 52 }: { score: number; size?: number }) {
  const cx = size / 2, cy = size / 2;
  const r = size * 0.38;
  const circ = 2 * Math.PI * r;
  const arc = (score / 100) * circ;
  const color = score >= 70 ? "#34d399" : score >= 50 ? "#60a5fa" : score >= 30 ? "#fbbf24" : "#f87171";

  return (
    <svg width={size} height={size} className="flex-shrink-0">
      <circle cx={cx} cy={cy} r={r} stroke="#1e293b" strokeWidth={size * 0.12} fill="none" />
      <circle cx={cx} cy={cy} r={r} stroke={color} strokeWidth={size * 0.12} fill="none"
        strokeDasharray={`${arc} ${circ - arc}`} strokeLinecap="round"
        transform={`rotate(-90 ${cx} ${cy})`} />
      <text x={cx} y={cy + 1} textAnchor="middle" dominantBaseline="middle"
        fill={color} fontSize={size * 0.22} fontWeight="700">{Math.round(score)}</text>
    </svg>
  );
}

// ── Readiness Distribution Bar ────────────────────────────────────────────────

function ReadinessDistBar({ counts }: { counts: Record<string, number> }) {
  const total = Object.values(counts).reduce((s, n) => s + n, 0);
  if (total === 0) return null;
  const order  = ["ready_now", "upcoming", "needs_nurturing", "not_ready"];
  const colors: Record<string, string> = { ready_now: "bg-emerald-500", upcoming: "bg-blue-500", needs_nurturing: "bg-amber-500", not_ready: "bg-red-500" };
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

// ── Account Modal ─────────────────────────────────────────────────────────────

function AccountModal({ account, onClose }: { account: Account; onClose: () => void }) {
  const [tab, setTab] = useState<"expansion" | "health" | "metrics">("expansion");

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
                <h2 className="text-slate-100 font-bold text-lg">{account.account_name}</h2>
                {account.is_at_risk && (
                  <span className="px-1.5 py-0.5 bg-red-900/50 text-red-300 border border-red-700/50 rounded text-xs font-medium">At Risk</span>
                )}
                {account.is_ready_to_expand && (
                  <span className="px-1.5 py-0.5 bg-emerald-900/50 text-emerald-300 border border-emerald-700/50 rounded text-xs font-medium">Ready</span>
                )}
              </div>
              <p className="text-slate-400 text-sm mt-0.5">
                {fmtLabel(account.segment)} · {account.contract_end_days}d to renewal · ARR {fmtMoney(account.current_arr)}
              </p>
            </div>
            <button onClick={onClose} className="text-slate-500 hover:text-slate-300 text-xl leading-none flex-shrink-0">✕</button>
          </div>
          <div className="flex items-center gap-2 mt-3 flex-wrap">
            <span className={`px-2 py-0.5 rounded text-xs font-medium ${actionBadge(account.expansion_action)}`}>
              {fmtLabel(account.expansion_action)}
            </span>
            <span className={`text-xs font-medium ${churnColor(account.churn_signal)}`}>
              Churn: {fmtLabel(account.churn_signal)}
            </span>
          </div>
        </div>

        {/* KPIs */}
        <div className="grid grid-cols-3 gap-px bg-slate-800 border-b border-slate-800">
          {[
            ["Health",     `${account.health_score}/100`],
            ["NRR",        `${account.nrr_forecast}%`],
            ["Potential",  fmtMoney(account.expansion_potential)],
          ].map(([label, val]) => (
            <div key={label} className="bg-slate-900 px-4 py-3 text-center">
              <div className="text-slate-400 text-xs">{label}</div>
              <div className="text-slate-100 font-bold text-base">{val}</div>
            </div>
          ))}
        </div>

        {/* Tabs */}
        <div className="flex border-b border-slate-800">
          {(["expansion", "health", "metrics"] as const).map((t) => (
            <button key={t} onClick={() => setTab(t)}
              className={`flex-1 py-2.5 text-sm font-medium transition-colors ${tab === t ? "text-indigo-400 border-b-2 border-indigo-500" : "text-slate-500 hover:text-slate-300"}`}>
              {t === "expansion" ? "Expansion" : t === "health" ? "Health" : "Details"}
            </button>
          ))}
        </div>

        <div className="p-5 space-y-3">
          {tab === "expansion" && (
            <div className="space-y-3">
              {[
                { label: "Expansion Score",    value: `${account.expansion_score}/100`,   bar: account.expansion_score,    color: "bg-indigo-500" },
                { label: "Expansion Potential", value: fmtMoney(account.expansion_potential), bar: Math.min(100, (account.expansion_potential / 120000) * 100), color: "bg-emerald-500" },
                { label: "Whitespace Products", value: `${account.whitespace_products} products`, bar: Math.min(100, account.whitespace_products * 20), color: "bg-violet-500" },
                { label: "Growth",             value: `${account.growth_since_start_pct}%`, bar: Math.min(100, Math.max(0, account.growth_since_start_pct + 20)), color: account.growth_since_start_pct >= 0 ? "bg-blue-500" : "bg-red-500" },
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
              <div className="text-slate-400 text-xs mt-2">
                Type: <span className="text-slate-200 font-medium">{fmtLabel(account.expansion_type)}</span>
                {" · "}Readiness: <span className="text-slate-200 font-medium">{fmtLabel(account.expansion_readiness)}</span>
              </div>
            </div>
          )}

          {tab === "health" && (
            <div className="space-y-3">
              <div className="flex items-center gap-4 bg-slate-800/50 rounded-xl p-4">
                <HealthRing score={account.health_score} size={64} />
                <div className="flex-1">
                  <div className="text-slate-300 font-semibold">Account Health</div>
                  <div className="text-slate-400 text-sm mt-1">NPS: <span className={account.nps_score >= 30 ? "text-emerald-400" : account.nps_score >= 0 ? "text-amber-400" : "text-red-400"}>
                    {account.nps_score > 0 ? "+" : ""}{account.nps_score}
                  </span></div>
                  <div className="text-slate-400 text-sm">
                    Adoption: <span className="text-slate-200 font-medium">{account.adoption_rate}%</span>
                    {" · "}Features: <span className="text-slate-200 font-medium">{account.feature_utilization}%</span>
                  </div>
                </div>
              </div>
              <div className="flex items-center justify-between py-2 border-b border-slate-800/60">
                <span className="text-slate-400 text-sm">Churn Risk</span>
                <span className={`font-bold text-sm ${churnColor(account.churn_signal)}`}>
                  {account.churn_risk_score}% · {fmtLabel(account.churn_signal)}
                </span>
              </div>
              <div className="flex items-center justify-between py-2">
                <span className="text-slate-400 text-sm">Users</span>
                <span className="text-slate-200 font-medium text-sm">{account.active_users}/{account.licensed_users} active</span>
              </div>
            </div>
          )}

          {tab === "metrics" && (
            <div className="grid grid-cols-2 gap-3">
              {[
                ["Current ARR",       fmtMoney(account.current_arr)],
                ["Renewal In",        `${account.contract_end_days}d`],
                ["Segment",           fmtLabel(account.segment)],
                ["CSM",               account.csm_id],
                ["NRR Forecast",      `${account.nrr_forecast}%`],
                ["Expansion Score",   `${account.expansion_score}/100`],
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

// ── Account Card ──────────────────────────────────────────────────────────────

function AccountCard({ account, onClick }: { account: Account; onClick: () => void }) {
  return (
    <button onClick={onClick}
      className={`w-full text-left p-4 rounded-xl border transition-all hover:border-indigo-500/50 hover:bg-slate-800/80 ${readinessBg(account.expansion_readiness)}`}>
      <div className="flex items-start gap-3">
        <HealthRing score={account.health_score} size={52} />
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 flex-wrap mb-0.5">
            <span className="text-slate-100 font-semibold text-sm truncate">{account.account_name}</span>
            {account.is_at_risk && (
              <span className="px-1 py-0.5 bg-red-900/50 text-red-300 border border-red-700/50 rounded text-[10px] font-medium">AT RISK</span>
            )}
          </div>
          <p className="text-slate-400 text-xs">{fmtLabel(account.segment)} · {account.contract_end_days}d renewal</p>
          <div className="flex items-center gap-2 mt-1.5 flex-wrap">
            <span className={`px-1.5 py-0.5 rounded text-[10px] font-medium ${actionBadge(account.expansion_action)}`}>
              {fmtLabel(account.expansion_action)}
            </span>
            <span className={`text-[10px] font-medium ${churnColor(account.churn_signal)}`}>
              {fmtLabel(account.churn_signal)} churn
            </span>
          </div>
        </div>
        <div className="text-right flex-shrink-0">
          <div className="text-emerald-400 font-bold text-sm">{fmtMoney(account.expansion_potential)}</div>
          <div className="text-slate-500 text-[10px]">NRR {account.nrr_forecast}%</div>
        </div>
      </div>

      {/* Adoption + Expansion bars */}
      <div className="mt-3 space-y-1.5">
        <div className="flex items-center gap-2">
          <span className="text-slate-600 text-[10px] w-14">Adoption</span>
          <div className="flex-1 h-1 bg-slate-800 rounded-full overflow-hidden">
            <div className="h-full bg-blue-500 rounded-full" style={{ width: `${account.adoption_rate}%` }} />
          </div>
          <span className="text-slate-500 text-[10px] w-8 text-right">{Math.round(account.adoption_rate)}%</span>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-slate-600 text-[10px] w-14">Expansion</span>
          <div className="flex-1 h-1 bg-slate-800 rounded-full overflow-hidden">
            <div className="h-full bg-indigo-500 rounded-full" style={{ width: `${account.expansion_score}%` }} />
          </div>
          <span className="text-slate-500 text-[10px] w-8 text-right">{Math.round(account.expansion_score)}</span>
        </div>
      </div>
    </button>
  );
}

// ── Page ──────────────────────────────────────────────────────────────────────

export default function AccountExpansionPage() {
  const [data, setData]       = useState<{ accounts: Account[]; summary: Summary } | null>(null);
  const [loading, setLoading] = useState(true);
  const [readinessFilter, setReadinessFilter] = useState("");
  const [churnFilter, setChurnFilter]         = useState("");
  const [selected, setSelected]               = useState<Account | null>(null);

  useEffect(() => {
    async function load() {
        setLoading(true);
        try {
          const params = new URLSearchParams();
          if (readinessFilter) params.set("readiness", readinessFilter);
          if (churnFilter)     params.set("churn", churnFilter);
          const res = await fetch(`/api/account-expansion?${params}`);
          if (res.ok) setData(await res.json());
        } finally {
          setLoading(false);
        }
  }
    load();
  }, [readinessFilter, churnFilter]);

  const s        = data?.summary;
  const accounts = data?.accounts ?? [];

  const readinesses = ["ready_now", "upcoming", "needs_nurturing", "not_ready"];
  const churns      = ["none", "low", "medium", "high", "critical"];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {/* Header */}
      <div className="flex items-start justify-between gap-4 flex-wrap">
        <div>
          <h1 className="text-2xl font-bold text-slate-100">Account Expansion</h1>
          <p className="text-slate-400 text-sm mt-1">Upsell/cross-sell intelligence, NRR forecasting & churn prevention</p>
        </div>
        <button onClick={load} className="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg text-sm font-medium transition-colors">Refresh</button>
      </div>

      {/* KPI Strip */}
      {s && (
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
          {[
            { label: "Total Potential",   value: fmtMoney(s.total_expansion_potential),  sub: `${s.ready_to_expand_count} ready now` },
            { label: "Avg NRR Forecast",  value: `${s.avg_nrr_forecast}%`,               sub: `avg health ${s.avg_health_score}/100` },
            { label: "High Value",        value: String(s.high_value_count),              sub: "≥50k potential" },
            { label: "At Risk",           value: String(s.at_risk_count),                sub: `${s.total} total accounts` },
          ].map(({ label, value, sub }) => (
            <div key={label} className="bg-slate-900 border border-slate-800 rounded-xl p-4">
              <div className="text-slate-400 text-xs">{label}</div>
              <div className="text-slate-100 font-bold text-xl mt-1">{value}</div>
              <div className="text-slate-500 text-xs mt-0.5">{sub}</div>
            </div>
          ))}
        </div>
      )}

      {/* Readiness Distribution */}
      {s && (
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
          <h2 className="text-slate-300 text-sm font-semibold mb-3">Expansion Readiness Distribution</h2>
          <ReadinessDistBar counts={s.readiness_counts} />
        </div>
      )}

      {/* Filters */}
      <div className="flex gap-2 flex-wrap">
        <div className="flex items-center gap-1 bg-slate-900 border border-slate-800 rounded-lg px-2 py-1">
          <span className="text-slate-500 text-xs">Readiness:</span>
          <div className="flex gap-1">
            {["", ...readinesses].map((r) => (
              <button key={r} onClick={() => setReadinessFilter(r)}
                className={`px-2 py-0.5 rounded text-xs font-medium transition-colors ${readinessFilter === r ? "bg-indigo-600 text-white" : "text-slate-400 hover:text-slate-200"}`}>
                {r ? fmtLabel(r) : "All"}
              </button>
            ))}
          </div>
        </div>
        <div className="flex items-center gap-1 bg-slate-900 border border-slate-800 rounded-lg px-2 py-1">
          <span className="text-slate-500 text-xs">Churn:</span>
          <div className="flex gap-1">
            {["", ...churns].map((c) => (
              <button key={c} onClick={() => setChurnFilter(c)}
                className={`px-2 py-0.5 rounded text-xs font-medium transition-colors ${churnFilter === c ? "bg-indigo-600 text-white" : "text-slate-400 hover:text-slate-200"}`}>
                {c ? fmtLabel(c) : "All"}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Account Cards */}
      {loading ? (
        <div className="flex items-center justify-center py-16">
          <div className="w-8 h-8 border-2 border-indigo-500 border-t-transparent rounded-full animate-spin" />
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
          {accounts.map((a) => (
            <AccountCard key={a.account_id} account={a} onClick={() => setSelected(a)} />
          ))}
          {accounts.length === 0 && (
            <div className="col-span-full text-center py-12 text-slate-500">No accounts match the selected filters.</div>
          )}
        </div>
      )}

      {/* Action Summary */}
      {s && (
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
          <h2 className="text-slate-300 text-sm font-semibold mb-3">Recommended Actions</h2>
          <div className="flex flex-wrap gap-2">
            {Object.entries(s.action_counts).sort((a, b) => b[1] - a[1]).map(([action, count]) => (
              <div key={action} className={`rounded-lg px-3 py-2 flex items-center gap-2 ${actionBadge(action)}`}>
                <span className="text-sm font-medium">{fmtLabel(action)}</span>
                <span className="bg-black/20 text-xs font-bold px-1.5 py-0.5 rounded">{count}</span>
              </div>
            ))}
          </div>
          <div className="grid grid-cols-3 gap-3 mt-4">
            <div className="bg-slate-800/50 rounded-lg p-3">
              <div className="text-slate-500 text-xs">Avg Churn Risk</div>
              <div className="text-slate-100 font-bold text-sm mt-1">{s.avg_churn_risk_score}%</div>
            </div>
            <div className="bg-slate-800/50 rounded-lg p-3">
              <div className="text-slate-500 text-xs">Avg Exp. Score</div>
              <div className="text-slate-100 font-bold text-sm mt-1">{s.avg_expansion_score}/100</div>
            </div>
            <div className="bg-slate-800/50 rounded-lg p-3">
              <div className="text-slate-500 text-xs">High Value Opps</div>
              <div className="text-indigo-400 font-bold text-sm mt-1">{s.high_value_count} accounts</div>
            </div>
          </div>
        </div>
      )}

      {selected && <AccountModal account={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
