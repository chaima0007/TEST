"use client";

import { useState, useEffect, useCallback } from "react";

// ─── Types ────────────────────────────────────────────────────────────────────

interface AccountResult {
  account_id: string;
  account_name: string;
  region: string;
  segment: string;
  arr_eur: number;
  clv_3yr_eur: number;
  clv_tier: string;
  expansion_potential: string;
  churn_risk: string;
  clv_action: string;
  health_score: number;
  churn_probability_pct: number;
  expansion_opportunity_eur: number;
  predicted_arr_yr2_eur: number;
  predicted_arr_yr3_eur: number;
  value_drivers: string[];
  risk_signals: string[];
  recommended_plays: string[];
}

interface Summary {
  total: number;
  tier_counts: Record<string, number>;
  churn_risk_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_health_score: number;
  total_clv_eur: number;
  total_arr_eur: number;
  total_expansion_opportunity_eur: number;
  at_risk_arr_eur: number;
  rescue_count: number;
}

// ─── Helpers ──────────────────────────────────────────────────────────────────

function formatEur(n: number): string {
  if (n >= 1_000_000) return `${(n / 1_000_000).toFixed(1)}M€`;
  if (n >= 1_000)     return `${Math.round(n / 1_000)}k€`;
  return `${Math.round(n)}€`;
}

function tierColor(tier: string): string {
  switch (tier) {
    case "platinum": return "#a78bfa";
    case "gold":     return "#fbbf24";
    case "silver":   return "#94a3b8";
    case "bronze":   return "#fb923c";
    case "minimal":  return "#ef4444";
    default:         return "#64748b";
  }
}

function tierBg(tier: string): string {
  switch (tier) {
    case "platinum": return "bg-violet-500/15 border-violet-500/30";
    case "gold":     return "bg-amber-500/15 border-amber-500/30";
    case "silver":   return "bg-slate-500/15 border-slate-500/30";
    case "bronze":   return "bg-orange-500/15 border-orange-500/30";
    case "minimal":  return "bg-red-500/15 border-red-500/30";
    default:         return "bg-slate-700/30 border-slate-600/30";
  }
}

function tierLabel(tier: string): string {
  switch (tier) {
    case "platinum": return "Platinum";
    case "gold":     return "Gold";
    case "silver":   return "Silver";
    case "bronze":   return "Bronze";
    case "minimal":  return "Minimal";
    default:         return tier;
  }
}

function riskColor(risk: string): string {
  switch (risk) {
    case "low":      return "text-emerald-400";
    case "medium":   return "text-amber-400";
    case "high":     return "text-orange-400";
    case "critical": return "text-red-400";
    default:         return "text-slate-400";
  }
}

function riskLabel(risk: string): string {
  switch (risk) {
    case "low":      return "Faible";
    case "medium":   return "Modéré";
    case "high":     return "Élevé";
    case "critical": return "Critique";
    default:         return risk;
  }
}

function expansionLabel(exp: string): string {
  switch (exp) {
    case "high":   return "Expansion élevée";
    case "medium": return "Expansion moyenne";
    case "low":    return "Expansion faible";
    case "none":   return "Pas d'expansion";
    default:       return exp;
  }
}

function actionLabel(action: string): string {
  switch (action) {
    case "invest":  return "Investir";
    case "grow":    return "Développer";
    case "nurture": return "Fidéliser";
    case "monitor": return "Surveiller";
    case "rescue":  return "Sauver";
    default:        return action;
  }
}

function actionBadge(action: string): string {
  switch (action) {
    case "invest":  return "bg-violet-500/20 text-violet-300 border-violet-500/30";
    case "grow":    return "bg-emerald-500/20 text-emerald-300 border-emerald-500/30";
    case "nurture": return "bg-indigo-500/20 text-indigo-300 border-indigo-500/30";
    case "monitor": return "bg-amber-500/20 text-amber-300 border-amber-500/30";
    case "rescue":  return "bg-red-500/20 text-red-300 border-red-500/30";
    default:        return "bg-slate-700/30 text-slate-300 border-slate-600/30";
  }
}

// ─── CLV Ring ─────────────────────────────────────────────────────────────────

function CLVRing({ health, tier, size = 80 }: { health: number; tier: string; size?: number }) {
  const cx = size / 2;
  const cy = size / 2;
  const r  = (size - 10) / 2;
  const circ = 2 * Math.PI * r;
  const arc  = (health / 100) * circ;
  const color = tierColor(tier);

  return (
    <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`} className="flex-shrink-0">
      <circle cx={cx} cy={cy} r={r} fill="none" stroke="#1e293b" strokeWidth="8" />
      <circle
        cx={cx} cy={cy} r={r}
        fill="none"
        stroke={color}
        strokeWidth="8"
        strokeDasharray={`${arc} ${circ - arc}`}
        strokeLinecap="round"
        transform={`rotate(-90 ${cx} ${cy})`}
      />
      <text x={cx} y={cy - 4} textAnchor="middle" fill="white" fontSize={size * 0.2} fontWeight="bold">
        {Math.round(health)}
      </text>
      <text x={cx} y={cy + size * 0.14} textAnchor="middle" fill="#94a3b8" fontSize={size * 0.12}>
        santé
      </text>
    </svg>
  );
}

// ─── Tier Distribution Bar ────────────────────────────────────────────────────

function TierDistributionBar({ counts, total }: { counts: Record<string, number>; total: number }) {
  const tiers = [
    { key: "platinum", label: "Platinum", color: "bg-violet-500" },
    { key: "gold",     label: "Gold",     color: "bg-amber-400" },
    { key: "silver",   label: "Silver",   color: "bg-slate-400" },
    { key: "bronze",   label: "Bronze",   color: "bg-orange-500" },
    { key: "minimal",  label: "Minimal",  color: "bg-red-500" },
  ];
  return (
    <div className="space-y-2">
      <div className="flex h-3 rounded-full overflow-hidden gap-0.5">
        {tiers.map(({ key, color }) => {
          const pct = total > 0 ? ((counts[key] || 0) / total) * 100 : 0;
          return pct > 0 ? (
            <div key={key} className={`${color} h-full`} style={{ width: `${pct}%` }} title={`${counts[key] || 0}`} />
          ) : null;
        })}
      </div>
      <div className="flex gap-4 flex-wrap">
        {tiers.map(({ key, label, color }) => (
          <div key={key} className="flex items-center gap-1.5">
            <div className={`w-2.5 h-2.5 rounded-full ${color}`} />
            <span className="text-xs text-slate-400">{label} <span className="text-white font-medium">{counts[key] || 0}</span></span>
          </div>
        ))}
      </div>
    </div>
  );
}

// ─── Account Modal ────────────────────────────────────────────────────────────

function AccountModal({ account, onClose }: { account: AccountResult; onClose: () => void }) {
  const [tab, setTab] = useState<"drivers" | "risks" | "plays">("plays");

  useEffect(() => {
    const h = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    document.addEventListener("keydown", h);
    return () => document.removeEventListener("keydown", h);
  }, [onClose]);

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm"
      onClick={onClose}
    >
      <div
        className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-2xl max-h-[90vh] overflow-y-auto shadow-2xl"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="p-6 border-b border-slate-800">
          <div className="flex items-start justify-between gap-4">
            <div>
              <h2 className="text-lg font-semibold text-white">{account.account_name}</h2>
              <p className="text-sm text-slate-400 mt-0.5">{account.region} · {account.segment}</p>
            </div>
            <button onClick={onClose} className="text-slate-500 hover:text-white text-xl leading-none mt-0.5">×</button>
          </div>

          {/* CLV & Projections */}
          <div className="grid grid-cols-4 gap-3 mt-4">
            <div className="bg-slate-800/60 rounded-lg p-3 text-center">
              <p className="text-lg font-bold text-white">{formatEur(account.arr_eur)}</p>
              <p className="text-xs text-slate-400 mt-0.5">ARR actuel</p>
            </div>
            <div className="bg-slate-800/60 rounded-lg p-3 text-center">
              <p className="text-lg font-bold" style={{ color: tierColor(account.clv_tier) }}>
                {formatEur(account.clv_3yr_eur)}
              </p>
              <p className="text-xs text-slate-400 mt-0.5">CLV 3 ans</p>
            </div>
            <div className="bg-slate-800/60 rounded-lg p-3 text-center">
              <p className="text-lg font-bold text-indigo-400">{formatEur(account.expansion_opportunity_eur)}</p>
              <p className="text-xs text-slate-400 mt-0.5">Potentiel expansion</p>
            </div>
            <div className="bg-slate-800/60 rounded-lg p-3 text-center">
              <p className={`text-lg font-bold ${account.churn_probability_pct >= 40 ? "text-red-400" : account.churn_probability_pct >= 20 ? "text-amber-400" : "text-emerald-400"}`}>
                {account.churn_probability_pct.toFixed(0)}%
              </p>
              <p className="text-xs text-slate-400 mt-0.5">Prob. churn</p>
            </div>
          </div>

          {/* ARR projection mini-chart */}
          <div className="mt-4 bg-slate-800/40 rounded-lg p-3">
            <p className="text-xs text-slate-500 mb-2">Projection ARR</p>
            <div className="flex items-end gap-2 h-12">
              {[
                { label: "An 1", val: account.arr_eur },
                { label: "An 2", val: account.predicted_arr_yr2_eur },
                { label: "An 3", val: account.predicted_arr_yr3_eur },
              ].map(({ label, val }) => {
                const maxVal = Math.max(account.arr_eur, account.predicted_arr_yr2_eur, account.predicted_arr_yr3_eur, 1);
                const pct = (val / maxVal) * 100;
                return (
                  <div key={label} className="flex-1 flex flex-col items-center gap-1">
                    <span className="text-[10px] text-slate-400">{formatEur(val)}</span>
                    <div className="w-full bg-indigo-500/30 rounded-t" style={{ height: `${pct}%` }} />
                    <span className="text-[10px] text-slate-500">{label}</span>
                  </div>
                );
              })}
            </div>
          </div>

          <div className="flex gap-2 mt-3 flex-wrap">
            <span className={`text-xs px-3 py-1 rounded-full border font-medium ${tierBg(account.clv_tier)}`}
              style={{ color: tierColor(account.clv_tier) }}>
              {tierLabel(account.clv_tier)}
            </span>
            <span className={`text-xs font-medium ${riskColor(account.churn_risk)}`}>
              Churn {riskLabel(account.churn_risk)}
            </span>
            <span className="text-xs text-slate-400">{expansionLabel(account.expansion_potential)}</span>
            <span className={`text-xs px-3 py-1 rounded-full border ${actionBadge(account.clv_action)}`}>
              {actionLabel(account.clv_action)}
            </span>
          </div>
        </div>

        {/* Tabs */}
        <div className="border-b border-slate-800 flex">
          {(["plays", "drivers", "risks"] as const).map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`flex-1 py-3 text-sm font-medium transition-colors ${
                tab === t ? "text-indigo-400 border-b-2 border-indigo-500" : "text-slate-500 hover:text-slate-300"
              }`}
            >
              {t === "plays" ? "Plays recommandés" : t === "drivers" ? "Moteurs de valeur" : "Signaux de risque"}
            </button>
          ))}
        </div>

        <div className="p-6 space-y-2">
          {tab === "plays" && (
            account.recommended_plays.map((p, i) => (
              <div key={i} className="flex gap-3 items-start">
                <div className="w-5 h-5 rounded-full bg-indigo-600/30 border border-indigo-500/40 flex items-center justify-center flex-shrink-0 mt-0.5">
                  <span className="text-[10px] text-indigo-300 font-bold">{i + 1}</span>
                </div>
                <p className="text-sm text-slate-300">{p}</p>
              </div>
            ))
          )}
          {tab === "drivers" && (
            account.value_drivers.length === 0 ? (
              <p className="text-sm text-slate-500">Aucun moteur de valeur identifié.</p>
            ) : (
              account.value_drivers.map((d, i) => (
                <div key={i} className="flex gap-3 items-start">
                  <div className="w-1.5 h-1.5 rounded-full bg-emerald-400 mt-2 flex-shrink-0" />
                  <p className="text-sm text-slate-300">{d}</p>
                </div>
              ))
            )
          )}
          {tab === "risks" && (
            account.risk_signals.length === 0 ? (
              <p className="text-sm text-slate-500">Aucun signal de risque détecté.</p>
            ) : (
              account.risk_signals.map((r, i) => (
                <div key={i} className="flex gap-3 items-start">
                  <div className="w-1.5 h-1.5 rounded-full bg-red-400 mt-2 flex-shrink-0" />
                  <p className="text-sm text-slate-300">{r}</p>
                </div>
              ))
            )
          )}
        </div>
      </div>
    </div>
  );
}

// ─── Account Card ─────────────────────────────────────────────────────────────

function AccountCard({ account, onClick }: { account: AccountResult; onClick: () => void }) {
  return (
    <button
      onClick={onClick}
      className={`w-full text-left p-4 rounded-xl border transition-all hover:border-indigo-500/40 hover:bg-slate-800/60 ${tierBg(account.clv_tier)}`}
    >
      <div className="flex items-start gap-4">
        <CLVRing health={account.health_score} tier={account.clv_tier} size={72} />

        <div className="flex-1 min-w-0">
          <div className="flex items-start justify-between gap-2">
            <div className="min-w-0">
              <h3 className="text-sm font-semibold text-white truncate">{account.account_name}</h3>
              <p className="text-xs text-slate-400 mt-0.5 truncate">{account.region} · {account.segment}</p>
            </div>
            <div className="text-right flex-shrink-0">
              <p className="text-sm font-bold" style={{ color: tierColor(account.clv_tier) }}>
                {formatEur(account.clv_3yr_eur)}
              </p>
              <p className="text-xs text-slate-500">CLV 3 ans</p>
            </div>
          </div>

          <div className="flex items-center gap-2 mt-2 flex-wrap">
            <span className="text-xs font-medium" style={{ color: tierColor(account.clv_tier) }}>
              {tierLabel(account.clv_tier)}
            </span>
            <span className="text-slate-600">·</span>
            <span className={`text-xs ${riskColor(account.churn_risk)}`}>
              Churn {riskLabel(account.churn_risk)} ({account.churn_probability_pct.toFixed(0)}%)
            </span>
            <span className="text-slate-600">·</span>
            <span className={`text-xs px-2 py-0.5 rounded-full border ${actionBadge(account.clv_action)}`}>
              {actionLabel(account.clv_action)}
            </span>
          </div>

          <div className="flex items-center gap-3 mt-1.5 text-xs text-slate-500">
            <span>ARR <span className="text-slate-300">{formatEur(account.arr_eur)}</span></span>
            {account.expansion_opportunity_eur > 0 && (
              <>
                <span>·</span>
                <span>Expansion <span className="text-indigo-400">+{formatEur(account.expansion_opportunity_eur)}</span></span>
              </>
            )}
            {account.risk_signals.length > 0 && (
              <>
                <span>·</span>
                <span className="text-red-400">{account.risk_signals.length} signaux risque</span>
              </>
            )}
          </div>
        </div>
      </div>
    </button>
  );
}

// ─── Page ─────────────────────────────────────────────────────────────────────

export default function CustomerLifetimeValuePage() {
  const [accounts, setAccounts] = useState<AccountResult[]>([]);
  const [summary, setSummary] = useState<Summary | null>(null);
  const [loading, setLoading] = useState(true);
  const [selected, setSelected] = useState<AccountResult | null>(null);
  const [tierFilter, setTierFilter]   = useState("all");
  const [actionFilter, setActionFilter] = useState("all");

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const params = new URLSearchParams();
      if (tierFilter !== "all")   params.set("tier", tierFilter);
      if (actionFilter !== "all") params.set("action", actionFilter);
      const res = await fetch(`/api/customer-lifetime-value?${params}`);
      const data = await res.json();
      setAccounts(data.accounts ?? []);
      setSummary(data.summary ?? null);
    } catch {}
    setLoading(false);
  }, [tierFilter, actionFilter]);

  useEffect(() => { load(); }, [load]);

  const TIER_TABS = [
    { key: "all",      label: "Tous" },
    { key: "platinum", label: "Platinum" },
    { key: "gold",     label: "Gold" },
    { key: "silver",   label: "Silver" },
    { key: "bronze",   label: "Bronze" },
    { key: "minimal",  label: "Minimal" },
  ];

  const ACTION_TABS = [
    { key: "all",     label: "Toutes" },
    { key: "invest",  label: "Investir" },
    { key: "grow",    label: "Développer" },
    { key: "nurture", label: "Fidéliser" },
    { key: "monitor", label: "Surveiller" },
    { key: "rescue",  label: "Sauver" },
  ];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">

        <div>
          <h1 className="text-2xl font-bold text-white">Valeur Client à Vie (CLV)</h1>
          <p className="text-sm text-slate-400 mt-1">
            Prédiction CLV 3 ans · Risque de churn · Potentiel d'expansion · Plays CS prioritaires
          </p>
        </div>

        {summary && (
          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-4">
            {[
              { label: "Comptes",         value: String(summary.total) },
              { label: "CLV total 3 ans", value: formatEur(summary.total_clv_eur), accent: true },
              { label: "ARR total",       value: formatEur(summary.total_arr_eur) },
              { label: "Potentiel exp.",  value: formatEur(summary.total_expansion_opportunity_eur), accent: true },
              { label: "ARR à risque",    value: formatEur(summary.at_risk_arr_eur), warn: summary.at_risk_arr_eur > 0 },
              { label: "À sauver",        value: String(summary.rescue_count), warn: summary.rescue_count > 0 },
            ].map(({ label, value, accent, warn }) => (
              <div key={label} className="bg-slate-900 border border-slate-800 rounded-xl p-4">
                <p className="text-xs text-slate-400 mb-1">{label}</p>
                <p className={`text-xl font-bold ${accent ? "text-indigo-400" : warn ? "text-orange-400" : "text-white"}`}>
                  {value}
                </p>
              </div>
            ))}
          </div>
        )}

        {summary && (
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
            <h2 className="text-sm font-semibold text-slate-300 mb-4">Distribution CLV par tier</h2>
            <TierDistributionBar counts={summary.tier_counts} total={summary.total} />
          </div>
        )}

        {/* Tier filter */}
        <div className="flex gap-2 flex-wrap">
          {TIER_TABS.map(({ key, label }) => (
            <button
              key={key}
              onClick={() => setTierFilter(key)}
              className={`px-4 py-2 rounded-lg text-sm font-medium border transition-colors ${
                tierFilter === key
                  ? "bg-indigo-600 border-indigo-500 text-white"
                  : "bg-slate-900 border-slate-700 text-slate-400 hover:text-white"
              }`}
            >
              {label}
              {summary && key !== "all" && (
                <span className="ml-1.5 text-xs opacity-70">({summary.tier_counts[key] || 0})</span>
              )}
            </button>
          ))}
        </div>

        {/* Action filter */}
        <div className="flex gap-2 flex-wrap">
          {ACTION_TABS.map(({ key, label }) => (
            <button
              key={key}
              onClick={() => setActionFilter(key)}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium border transition-colors ${
                actionFilter === key
                  ? "bg-violet-600/30 border-violet-500/50 text-violet-300"
                  : "bg-slate-900 border-slate-700 text-slate-400 hover:text-white"
              }`}
            >
              {label}
              {summary && key !== "all" && (
                <span className="ml-1 opacity-70">({summary.action_counts[key] || 0})</span>
              )}
            </button>
          ))}
        </div>

        {loading ? (
          <div className="flex items-center justify-center py-24">
            <div className="w-8 h-8 border-2 border-indigo-500 border-t-transparent rounded-full animate-spin" />
          </div>
        ) : accounts.length === 0 ? (
          <div className="text-center py-24 text-slate-500">Aucun compte ne correspond aux filtres.</div>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
            {accounts.map((a) => (
              <AccountCard key={a.account_id} account={a} onClick={() => setSelected(a)} />
            ))}
          </div>
        )}
      </div>

      {selected && <AccountModal account={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
