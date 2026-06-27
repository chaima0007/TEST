"use client";

import { useState, useEffect, useRef } from "react";

interface AccountData {
  account_id: string;
  account_name: string;
  industry: string;
  contract_type: string;
  arr_eur: number;
  days_until_renewal: number;
  feature_adoption_pct: number;
  logins_last_30d: number;
  api_calls_last_30d: number;
  users_active: number;
  users_licensed: number;
  payments_on_time_pct: number;
  overdue_invoices: number;
  expansion_revenue_eur: number;
  nps_score: number;
  support_tickets_open: number;
  executive_contacts: number;
  last_qbr_days: number;
  csm_sentiment: number;
  usage_pct_of_limit: number;
}

interface AccountResult {
  account: AccountData;
  health_tier: string;
  health_score: number;
  engagement_score: number;
  adoption_score: number;
  financial_score: number;
  relationship_score: number;
  churn_risk_pct: number;
  expansion_potential_eur: number;
  primary_action: string;
  health_signals: string[];
  risk_signals: string[];
  renewal_forecast: string;
}

interface Summary {
  total: number;
  tier_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_health_score: number;
  avg_churn_risk_pct: number;
  total_arr_eur: number;
  arr_at_risk_eur: number;
  total_expansion_potential_eur: number;
}

const TIER_TABS = [
  { key: "all", label: "Tous" },
  { key: "champion", label: "Champion" },
  { key: "healthy", label: "Sain" },
  { key: "neutral", label: "Neutre" },
  { key: "at_risk", label: "À risque" },
  { key: "churning", label: "Churn" },
];

const TIER_COLORS: Record<string, string> = {
  champion: "#6366f1",
  healthy: "#22c55e",
  neutral: "#f59e0b",
  at_risk: "#f97316",
  churning: "#ef4444",
};

const TIER_BG: Record<string, string> = {
  champion: "bg-indigo-500/10 text-indigo-400 border-indigo-500/30",
  healthy: "bg-green-500/10 text-green-400 border-green-500/30",
  neutral: "bg-amber-500/10 text-amber-400 border-amber-500/30",
  at_risk: "bg-orange-500/10 text-orange-400 border-orange-500/30",
  churning: "bg-red-500/10 text-red-400 border-red-500/30",
};

const TIER_LABELS: Record<string, string> = {
  champion: "Champion",
  healthy: "Sain",
  neutral: "Neutre",
  at_risk: "À risque",
  churning: "Churn",
};

const ACTION_LABELS: Record<string, string> = {
  expand: "Expansion",
  nurture: "Nurture",
  stabilize: "Stabiliser",
  save: "Sauver",
  offboard: "Offboard",
};

const ACTION_COLORS: Record<string, string> = {
  expand: "bg-indigo-500/10 text-indigo-400",
  nurture: "bg-blue-500/10 text-blue-400",
  stabilize: "bg-amber-500/10 text-amber-400",
  save: "bg-orange-500/10 text-orange-400",
  offboard: "bg-red-500/10 text-red-400",
};

const FORECAST_LABELS: Record<string, string> = {
  confident: "Confiant",
  uncertain: "Incertain",
  at_risk: "À risque",
};

const FORECAST_COLORS: Record<string, string> = {
  confident: "text-green-400",
  uncertain: "text-amber-400",
  at_risk: "text-red-400",
};

function fmtEur(n: number) {
  if (n >= 1_000_000) return `${(n / 1_000_000).toFixed(1)}M€`;
  if (n >= 1_000) return `${(n / 1_000).toFixed(0)}k€`;
  return `${n}€`;
}

function HealthRing({ score, tier }: { score: number; tier: string }) {
  const r = 28;
  const circ = 2 * Math.PI * r;
  const fill = (score / 100) * circ;
  const color = TIER_COLORS[tier] || "#6366f1";

  return (
    <svg width="72" height="72" viewBox="0 0 72 72" className="shrink-0">
      <circle cx="36" cy="36" r={r} fill="none" stroke="#1e293b" strokeWidth="6" />
      <circle
        cx="36"
        cy="36"
        r={r}
        fill="none"
        stroke={color}
        strokeWidth="6"
        strokeDasharray={`${fill} ${circ - fill}`}
        strokeLinecap="round"
        transform="rotate(-90 36 36)"
      />
      <text x="36" y="40" textAnchor="middle" fontSize="13" fontWeight="700" fill={color}>
        {Math.round(score)}
      </text>
    </svg>
  );
}

function ScoreBar({ label, value }: { label: string; value: number }) {
  const color =
    value >= 75 ? "#22c55e" : value >= 50 ? "#6366f1" : value >= 30 ? "#f59e0b" : "#ef4444";
  return (
    <div className="flex flex-col gap-1">
      <div className="flex justify-between text-xs text-slate-400">
        <span>{label}</span>
        <span className="font-semibold" style={{ color }}>
          {Math.round(value)}
        </span>
      </div>
      <div className="h-1.5 rounded-full bg-slate-800 overflow-hidden">
        <div
          className="h-full rounded-full transition-all duration-500"
          style={{ width: `${value}%`, backgroundColor: color }}
        />
      </div>
    </div>
  );
}

function AccountModal({ acc, onClose }: { acc: AccountResult; onClose: () => void }) {
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handler = (e: KeyboardEvent) => e.key === "Escape" && onClose();
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [onClose]);

  useEffect(() => {
    const handler = (e: MouseEvent) => {
      if (ref.current && !ref.current.contains(e.target as Node)) onClose();
    };
    setTimeout(() => window.addEventListener("mousedown", handler), 0);
    return () => window.removeEventListener("mousedown", handler);
  }, [onClose]);

  const tierColor = TIER_COLORS[acc.health_tier] || "#6366f1";

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4">
      <div
        ref={ref}
        className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-2xl max-h-[90vh] overflow-y-auto"
      >
        <div className="p-6 border-b border-slate-800 flex items-start justify-between gap-4">
          <div>
            <div className="flex items-center gap-3 flex-wrap">
              <h2 className="text-xl font-bold text-slate-100">{acc.account.account_name}</h2>
              <span
                className={`text-xs px-2 py-0.5 rounded-full border font-medium ${TIER_BG[acc.health_tier]}`}
              >
                {TIER_LABELS[acc.health_tier]}
              </span>
              <span
                className={`text-xs px-2 py-0.5 rounded-full font-medium ${ACTION_COLORS[acc.primary_action]}`}
              >
                {ACTION_LABELS[acc.primary_action]}
              </span>
            </div>
            <p className="text-sm text-slate-400 mt-1">{acc.account.industry}</p>
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-slate-200 text-xl shrink-0">
            ✕
          </button>
        </div>

        <div className="p-6 space-y-6">
          {/* KPIs */}
          <div className="grid grid-cols-2 gap-3 sm:grid-cols-4">
            {[
              { label: "ARR", value: fmtEur(acc.account.arr_eur) },
              {
                label: "Renouvellement",
                value:
                  acc.account.days_until_renewal > 0
                    ? `J-${acc.account.days_until_renewal}`
                    : "Expiré",
                color:
                  acc.account.days_until_renewal <= 30
                    ? "text-red-400"
                    : acc.account.days_until_renewal <= 90
                    ? "text-amber-400"
                    : "text-slate-100",
              },
              {
                label: "Prévision",
                value: FORECAST_LABELS[acc.renewal_forecast] || acc.renewal_forecast,
                color: FORECAST_COLORS[acc.renewal_forecast] || "text-slate-100",
              },
              {
                label: "Potentiel expansion",
                value: acc.expansion_potential_eur > 0 ? fmtEur(acc.expansion_potential_eur) : "—",
                color: acc.expansion_potential_eur > 0 ? "text-indigo-400" : "text-slate-500",
              },
            ].map((kpi) => (
              <div key={kpi.label} className="bg-slate-800/50 rounded-xl p-3 text-center">
                <div className={`text-lg font-bold ${kpi.color ?? "text-slate-100"}`}>
                  {kpi.value}
                </div>
                <div className="text-xs text-slate-400 mt-0.5">{kpi.label}</div>
              </div>
            ))}
          </div>

          {/* Score ring + churn risk */}
          <div className="flex items-center gap-6 bg-slate-800/30 rounded-xl p-4">
            <HealthRing score={acc.health_score} tier={acc.health_tier} />
            <div className="flex-1 min-w-0">
              <div className="flex items-baseline gap-2 mb-1">
                <span className="text-2xl font-bold" style={{ color: tierColor }}>
                  {acc.health_score.toFixed(1)}
                </span>
                <span className="text-sm text-slate-400">/ 100 — santé compte</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-sm text-slate-400">Risque churn :</span>
                <span
                  className={`text-sm font-bold ${
                    acc.churn_risk_pct >= 70
                      ? "text-red-400"
                      : acc.churn_risk_pct >= 40
                      ? "text-orange-400"
                      : acc.churn_risk_pct >= 20
                      ? "text-amber-400"
                      : "text-green-400"
                  }`}
                >
                  {acc.churn_risk_pct.toFixed(1)}%
                </span>
              </div>
              <div className="flex gap-4 mt-2 text-xs text-slate-500">
                <span>Contrat : {acc.account.contract_type}</span>
                <span>
                  Utilisateurs : {acc.account.users_active}/{acc.account.users_licensed}
                </span>
                <span>NPS : {acc.account.nps_score > 0 ? `+${acc.account.nps_score}` : acc.account.nps_score}</span>
              </div>
            </div>
          </div>

          {/* Score dimensions */}
          <div className="space-y-3">
            <h3 className="text-sm font-semibold text-slate-300">Dimensions de santé</h3>
            <ScoreBar label="Engagement" value={acc.engagement_score} />
            <ScoreBar label="Adoption produit" value={acc.adoption_score} />
            <ScoreBar label="Santé financière" value={acc.financial_score} />
            <ScoreBar label="Relation client" value={acc.relationship_score} />
          </div>

          {/* Usage metrics */}
          <div className="grid grid-cols-3 gap-3">
            {[
              { label: "Usage/limite", value: `${acc.account.usage_pct_of_limit}%` },
              { label: "Adoption features", value: `${acc.account.feature_adoption_pct}%` },
              { label: "Paiements ok", value: `${acc.account.payments_on_time_pct}%` },
            ].map((m) => (
              <div key={m.label} className="bg-slate-800/50 rounded-xl p-3 text-center">
                <div className="text-lg font-bold text-slate-100">{m.value}</div>
                <div className="text-xs text-slate-400 mt-0.5">{m.label}</div>
              </div>
            ))}
          </div>

          {/* Signals */}
          {acc.health_signals.length > 0 && (
            <div>
              <h3 className="text-sm font-semibold text-green-400 mb-2">Signaux positifs</h3>
              <ul className="space-y-1">
                {acc.health_signals.map((s, i) => (
                  <li key={i} className="text-xs text-slate-300 flex gap-2">
                    <span className="text-green-400 shrink-0">✓</span>
                    <span>{s}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}
          {acc.risk_signals.length > 0 && (
            <div>
              <h3 className="text-sm font-semibold text-red-400 mb-2">Signaux de risque</h3>
              <ul className="space-y-1">
                {acc.risk_signals.map((s, i) => (
                  <li key={i} className="text-xs text-slate-300 flex gap-2">
                    <span className="text-red-400 shrink-0">⚠</span>
                    <span>{s}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Support & QBR */}
          <div className="grid grid-cols-2 gap-3 text-xs text-slate-400 bg-slate-800/30 rounded-xl p-4">
            <div>
              <span className="text-slate-500">Tickets ouverts : </span>
              <span
                className={
                  acc.account.support_tickets_open >= 3
                    ? "text-red-400 font-semibold"
                    : acc.account.support_tickets_open >= 1
                    ? "text-amber-400"
                    : "text-green-400"
                }
              >
                {acc.account.support_tickets_open}
              </span>
            </div>
            <div>
              <span className="text-slate-500">Dernier QBR : </span>
              <span
                className={
                  acc.account.last_qbr_days > 120
                    ? "text-red-400"
                    : acc.account.last_qbr_days > 90
                    ? "text-amber-400"
                    : "text-slate-300"
                }
              >
                J-{acc.account.last_qbr_days}
              </span>
            </div>
            <div>
              <span className="text-slate-500">Contacts exec : </span>
              <span className="text-slate-300">{acc.account.executive_contacts}</span>
            </div>
            <div>
              <span className="text-slate-500">Sentiment CSM : </span>
              <span
                className={
                  acc.account.csm_sentiment >= 70
                    ? "text-green-400"
                    : acc.account.csm_sentiment >= 45
                    ? "text-amber-400"
                    : "text-red-400"
                }
              >
                {acc.account.csm_sentiment}/100
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

function AccountCard({ acc, onClick }: { acc: AccountResult; onClick: () => void }) {
  const tierColor = TIER_COLORS[acc.health_tier] || "#6366f1";

  return (
    <button
      onClick={onClick}
      className="bg-slate-900 border border-slate-800 rounded-2xl p-5 text-left hover:border-slate-600 transition-all hover:bg-slate-800/40 group"
    >
      <div className="flex items-start gap-4">
        <HealthRing score={acc.health_score} tier={acc.health_tier} />
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 flex-wrap mb-1">
            <span className="font-semibold text-slate-100 truncate">{acc.account.account_name}</span>
            <span
              className={`text-xs px-2 py-0.5 rounded-full border font-medium shrink-0 ${TIER_BG[acc.health_tier]}`}
            >
              {TIER_LABELS[acc.health_tier]}
            </span>
          </div>
          <p className="text-xs text-slate-400 mb-3">{acc.account.industry}</p>

          <div className="flex flex-wrap gap-2 text-xs">
            <span className="bg-slate-800 rounded-lg px-2 py-1 text-slate-300">
              ARR {fmtEur(acc.account.arr_eur)}
            </span>
            <span
              className={`rounded-lg px-2 py-1 font-medium ${ACTION_COLORS[acc.primary_action]}`}
            >
              {ACTION_LABELS[acc.primary_action]}
            </span>
            {acc.expansion_potential_eur > 0 && (
              <span className="bg-indigo-500/10 text-indigo-400 rounded-lg px-2 py-1">
                +{fmtEur(acc.expansion_potential_eur)}
              </span>
            )}
          </div>
        </div>
      </div>

      {/* Mini dimension bars */}
      <div className="mt-4 space-y-2">
        {[
          { label: "Engagement", v: acc.engagement_score },
          { label: "Adoption", v: acc.adoption_score },
          { label: "Finance", v: acc.financial_score },
          { label: "Relation", v: acc.relationship_score },
        ].map((d) => {
          const c =
            d.v >= 75 ? "#22c55e" : d.v >= 50 ? "#6366f1" : d.v >= 30 ? "#f59e0b" : "#ef4444";
          return (
            <div key={d.label} className="flex items-center gap-2">
              <span className="text-xs text-slate-500 w-16 shrink-0">{d.label}</span>
              <div className="flex-1 h-1 rounded-full bg-slate-800 overflow-hidden">
                <div
                  className="h-full rounded-full"
                  style={{ width: `${d.v}%`, backgroundColor: c }}
                />
              </div>
              <span className="text-xs w-6 text-right shrink-0" style={{ color: c }}>
                {Math.round(d.v)}
              </span>
            </div>
          );
        })}
      </div>

      {/* Churn risk + renewal */}
      <div className="mt-3 flex items-center justify-between text-xs text-slate-500">
        <span>
          Churn :{" "}
          <span
            className={`font-semibold ${
              acc.churn_risk_pct >= 70
                ? "text-red-400"
                : acc.churn_risk_pct >= 40
                ? "text-orange-400"
                : acc.churn_risk_pct >= 20
                ? "text-amber-400"
                : "text-green-400"
            }`}
          >
            {acc.churn_risk_pct.toFixed(0)}%
          </span>
        </span>
        <span>
          Renouvellement :{" "}
          <span
            className={`font-semibold ${
              acc.account.days_until_renewal <= 30
                ? "text-red-400"
                : acc.account.days_until_renewal <= 90
                ? "text-amber-400"
                : "text-slate-400"
            }`}
          >
            {acc.account.days_until_renewal > 0 ? `J-${acc.account.days_until_renewal}` : "Expiré"}
          </span>
        </span>
      </div>
    </button>
  );
}

export default function AccountHealthPage() {
  const [accounts, setAccounts] = useState<AccountResult[]>([]);
  const [summary, setSummary] = useState<Summary | null>(null);
  const [activeTier, setActiveTier] = useState("all");
  const [selected, setSelected] = useState<AccountResult | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      setLoading(true);
      try {
        const params = new URLSearchParams();
        if (activeTier !== "all") params.set("tier", activeTier);
        const res = await fetch(`/api/account-health?${params}`);
        const data = await res.json();
        setAccounts(data.accounts ?? []);
        setSummary(data.summary ?? null);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, [activeTier]);

  return (
    <div className="min-h-screen bg-slate-950 p-6">
      <div className="max-w-7xl mx-auto space-y-6">
        {/* Header */}
        <div>
          <h1 className="text-2xl font-bold text-slate-100">Santé Comptes</h1>
          <p className="text-sm text-slate-400 mt-1">
            Suivi de l&apos;adoption, engagement et risque de churn — expansion opportunities
          </p>
        </div>

        {/* KPI strip */}
        {summary && (
          <div className="grid grid-cols-2 gap-3 sm:grid-cols-4">
            {[
              {
                label: "ARR Total",
                value: fmtEur(summary.total_arr_eur),
                sub: `${summary.total} comptes`,
                color: "text-slate-100",
              },
              {
                label: "ARR à risque",
                value: fmtEur(summary.arr_at_risk_eur),
                sub: `${((summary.arr_at_risk_eur / summary.total_arr_eur) * 100).toFixed(0)}% du total`,
                color: summary.arr_at_risk_eur > 0 ? "text-red-400" : "text-green-400",
              },
              {
                label: "Santé moyenne",
                value: `${summary.avg_health_score}/100`,
                sub: `Risque churn moy. ${summary.avg_churn_risk_pct}%`,
                color:
                  summary.avg_health_score >= 65
                    ? "text-green-400"
                    : summary.avg_health_score >= 45
                    ? "text-amber-400"
                    : "text-red-400",
              },
              {
                label: "Potentiel expansion",
                value: fmtEur(summary.total_expansion_potential_eur),
                sub: `${summary.action_counts["expand"] ?? 0} comptes expansibles`,
                color: "text-indigo-400",
              },
            ].map((kpi) => (
              <div
                key={kpi.label}
                className="bg-slate-900 border border-slate-800 rounded-2xl p-4"
              >
                <div className={`text-2xl font-bold ${kpi.color}`}>{kpi.value}</div>
                <div className="text-xs text-slate-400 mt-0.5">{kpi.label}</div>
                <div className="text-xs text-slate-500 mt-1">{kpi.sub}</div>
              </div>
            ))}
          </div>
        )}

        {/* Tier filter tabs */}
        <div className="flex flex-wrap gap-2">
          {TIER_TABS.map((t) => {
            const count =
              t.key === "all"
                ? summary?.total
                : summary?.tier_counts[t.key];
            return (
              <button
                key={t.key}
                onClick={() => setActiveTier(t.key)}
                className={`px-4 py-1.5 rounded-full text-sm font-medium border transition-all ${
                  activeTier === t.key
                    ? "bg-indigo-600 border-indigo-500 text-white"
                    : "bg-slate-800/50 border-slate-700 text-slate-400 hover:border-slate-500"
                }`}
              >
                {t.label}
                {count !== undefined && (
                  <span className="ml-1.5 text-xs opacity-70">({count})</span>
                )}
              </button>
            );
          })}
        </div>

        {/* Tier distribution bar */}
        {summary && activeTier === "all" && (
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-4">
            <p className="text-xs text-slate-400 mb-3">Répartition des tiers</p>
            <div className="flex h-3 rounded-full overflow-hidden gap-0.5">
              {(["champion", "healthy", "neutral", "at_risk", "churning"] as const).map((tier) => {
                const pct =
                  summary.total > 0
                    ? ((summary.tier_counts[tier] || 0) / summary.total) * 100
                    : 0;
                return pct > 0 ? (
                  <div
                    key={tier}
                    className="h-full transition-all"
                    style={{ width: `${pct}%`, backgroundColor: TIER_COLORS[tier] }}
                    title={`${TIER_LABELS[tier]}: ${summary.tier_counts[tier] || 0}`}
                  />
                ) : null;
              })}
            </div>
            <div className="flex flex-wrap gap-3 mt-2">
              {(["champion", "healthy", "neutral", "at_risk", "churning"] as const).map((tier) => (
                <div key={tier} className="flex items-center gap-1.5 text-xs text-slate-400">
                  <div
                    className="w-2 h-2 rounded-full"
                    style={{ backgroundColor: TIER_COLORS[tier] }}
                  />
                  {TIER_LABELS[tier]} ({summary.tier_counts[tier] || 0})
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Account grid */}
        {loading ? (
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {Array.from({ length: 6 }).map((_, i) => (
              <div key={i} className="h-64 bg-slate-900 border border-slate-800 rounded-2xl animate-pulse" />
            ))}
          </div>
        ) : accounts.length === 0 ? (
          <div className="text-center py-20 text-slate-500">Aucun compte pour ce filtre</div>
        ) : (
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {accounts.map((acc) => (
              <AccountCard
                key={acc.account.account_id}
                acc={acc}
                onClick={() => setSelected(acc)}
              />
            ))}
          </div>
        )}
      </div>

      {selected && <AccountModal acc={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
