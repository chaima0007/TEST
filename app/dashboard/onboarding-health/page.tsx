"use client";

import { useEffect, useState, useCallback, useRef } from "react";

// ─── Types ────────────────────────────────────────────────────────────────────

type Account = {
  account_id: string;
  account_name: string;
  arr_eur: number;
  onboarding_status: string;
  onboarding_action: string;
  overall_score: number;
  milestone_score: number;
  engagement_score: number;
  health_score: number;
  completion_pct: number;
  days_remaining: number;
  schedule_delta_pct: number;
  go_live_done: boolean;
  blockers: string[];
  achievements: string[];
  recommended_actions: string[];
};

type Summary = {
  total: number;
  status_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_completion_pct: number;
  avg_overall_score: number;
  critical_count: number;
  overdue_count: number;
  completed_count: number;
  total_arr_at_risk_eur: number;
};

// ─── Meta helpers ─────────────────────────────────────────────────────────────

const STATUS_META: Record<string, { label: string; color: string; ring: string; bg: string }> = {
  on_track: { label: "Sur les rails", color: "text-emerald-400", ring: "#34d399", bg: "bg-emerald-900/30" },
  at_risk:  { label: "À risque",      color: "text-amber-400",   ring: "#fbbf24", bg: "bg-amber-900/30"   },
  delayed:  { label: "En retard",     color: "text-orange-400",  ring: "#fb923c", bg: "bg-orange-900/30"  },
  critical: { label: "Critique",      color: "text-red-400",     ring: "#f87171", bg: "bg-red-900/30"     },
};

const ACTION_META: Record<string, { label: string; color: string; dot: string }> = {
  celebrate:   { label: "Go-live!",    color: "text-emerald-400", dot: "bg-emerald-400" },
  monitor:     { label: "Surveiller",  color: "text-blue-400",    dot: "bg-blue-400"    },
  accelerate:  { label: "Accélérer",   color: "text-amber-400",   dot: "bg-amber-400"   },
  rescue:      { label: "Sauvetage",   color: "text-red-400",     dot: "bg-red-400"     },
};

const STATUS_ORDER = ["all", "on_track", "at_risk", "delayed", "critical"];

function fmt(n: number) {
  return new Intl.NumberFormat("fr-FR", { style: "currency", currency: "EUR", maximumFractionDigits: 0 }).format(n);
}

// ─── OnboardingRing ───────────────────────────────────────────────────────────

function OnboardingRing({ score, status }: { score: number; status: string }) {
  const r = 28;
  const circ = 2 * Math.PI * r;
  const fill = (score / 100) * circ;
  const ringColor = STATUS_META[status]?.ring ?? "#6366f1";
  return (
    <svg width="72" height="72" viewBox="0 0 72 72">
      <circle cx="36" cy="36" r={r} fill="none" stroke="#1e293b" strokeWidth="7" />
      <circle
        cx="36" cy="36" r={r}
        fill="none"
        stroke={ringColor}
        strokeWidth="7"
        strokeDasharray={`${fill} ${circ}`}
        strokeLinecap="round"
        transform="rotate(-90 36 36)"
      />
      <text x="36" y="40" textAnchor="middle" fill="white" fontSize="13" fontWeight="700">
        {score.toFixed(0)}
      </text>
    </svg>
  );
}

// ─── ScoreBar ─────────────────────────────────────────────────────────────────

function ScoreBar({ label, value, color = "bg-indigo-500" }: { label: string; value: number; color?: string }) {
  return (
    <div>
      <div className="flex justify-between text-xs text-slate-400 mb-1">
        <span>{label}</span>
        <span className="text-slate-200">{value.toFixed(0)}</span>
      </div>
      <div className="h-1.5 bg-slate-700 rounded-full overflow-hidden">
        <div className={`h-full rounded-full ${color}`} style={{ width: `${Math.min(100, value)}%` }} />
      </div>
    </div>
  );
}

// ─── AccountModal ─────────────────────────────────────────────────────────────

function AccountModal({ account, onClose }: { account: Account; onClose: () => void }) {
  const overlayRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleKey = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", handleKey);
    return () => window.removeEventListener("keydown", handleKey);
  }, [onClose]);

  const sm = STATUS_META[account.onboarding_status] ?? STATUS_META.at_risk;
  const am = ACTION_META[account.onboarding_action] ?? ACTION_META.monitor;

  return (
    <div
      ref={overlayRef}
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm p-4"
      onClick={(e) => { if (e.target === overlayRef.current) onClose(); }}
    >
      <div className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-2xl max-h-[90vh] overflow-y-auto shadow-2xl">
        {/* Header */}
        <div className="flex items-start justify-between p-6 border-b border-slate-800">
          <div className="flex items-center gap-4">
            <OnboardingRing score={account.overall_score} status={account.onboarding_status} />
            <div>
              <h2 className="text-white font-bold text-lg leading-tight">{account.account_name}</h2>
              <div className="flex flex-wrap items-center gap-2 mt-1">
                <span className={`text-xs font-semibold px-2 py-0.5 rounded-full ${sm.bg} ${sm.color}`}>
                  {sm.label}
                </span>
                <span className="text-slate-400 text-xs">{fmt(account.arr_eur)}</span>
                {account.days_remaining < 0 && !account.go_live_done ? (
                  <span className="text-xs text-red-400 font-semibold">
                    En retard de {-account.days_remaining}j
                  </span>
                ) : account.go_live_done ? (
                  <span className="text-xs text-emerald-400 font-semibold">Go-live complété</span>
                ) : (
                  <span className="text-xs text-slate-400">Go-live dans {account.days_remaining}j</span>
                )}
              </div>
            </div>
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-white transition-colors mt-1">
            <svg className="w-5 h-5" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
            </svg>
          </button>
        </div>

        <div className="p-6 space-y-6">
          {/* Schedule delta + action */}
          <div className="grid grid-cols-2 gap-4">
            <div className="bg-slate-800/60 rounded-xl p-4">
              <p className="text-slate-400 text-xs mb-1">Avance / Retard planning</p>
              <p className={`font-bold text-xl ${account.schedule_delta_pct >= 0 ? "text-emerald-400" : "text-orange-400"}`}>
                {account.schedule_delta_pct >= 0 ? "+" : ""}{account.schedule_delta_pct.toFixed(0)}%
              </p>
            </div>
            <div className="flex items-center gap-3 bg-slate-800/60 rounded-xl p-4">
              <div className={`w-2.5 h-2.5 rounded-full flex-shrink-0 ${am.dot}`} />
              <div>
                <p className="text-slate-400 text-xs">Action</p>
                <p className={`font-semibold text-sm ${am.color}`}>{am.label}</p>
              </div>
            </div>
          </div>

          {/* Score breakdown */}
          <div>
            <h3 className="text-slate-300 text-sm font-semibold mb-3">Scores par dimension</h3>
            <div className="space-y-3">
              <ScoreBar label="Progression jalons (55%)" value={account.milestone_score} color="bg-indigo-500" />
              <ScoreBar label="Engagement équipes (25%)" value={account.engagement_score} color="bg-violet-500" />
              <ScoreBar label="Santé opérationnelle (20%)" value={account.health_score} color="bg-emerald-500" />
            </div>
          </div>

          {/* Completion bar */}
          <div>
            <div className="flex justify-between text-xs text-slate-400 mb-2">
              <span>Complétion globale jalons</span>
              <span className="text-white font-semibold">{account.completion_pct.toFixed(0)}%</span>
            </div>
            <div className="h-3 bg-slate-700 rounded-full overflow-hidden">
              <div
                className={`h-full rounded-full ${
                  account.completion_pct >= 75 ? "bg-emerald-500" :
                  account.completion_pct >= 50 ? "bg-amber-500" : "bg-red-500"
                }`}
                style={{ width: `${Math.min(100, account.completion_pct)}%` }}
              />
            </div>
          </div>

          {/* Blockers */}
          {account.blockers.length > 0 && (
            <div>
              <h3 className="text-slate-300 text-sm font-semibold mb-3">
                Blocages ({account.blockers.length})
              </h3>
              <ul className="space-y-1.5">
                {account.blockers.map((b, i) => (
                  <li key={i} className="flex items-start gap-2 text-xs text-orange-300">
                    <span className="text-orange-400 mt-0.5 flex-shrink-0">⚠</span>
                    {b}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Achievements */}
          {account.achievements.length > 0 && (
            <div>
              <h3 className="text-slate-300 text-sm font-semibold mb-3">Réalisations</h3>
              <ul className="space-y-1.5">
                {account.achievements.map((a, i) => (
                  <li key={i} className="flex items-start gap-2 text-xs text-emerald-300">
                    <span className="text-emerald-400 mt-0.5 flex-shrink-0">✓</span>
                    {a}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Recommended actions */}
          {account.recommended_actions.length > 0 && (
            <div>
              <h3 className="text-slate-300 text-sm font-semibold mb-3">Actions recommandées</h3>
              <ol className="space-y-2">
                {account.recommended_actions.map((a, i) => (
                  <li key={i} className="flex items-start gap-2.5 text-xs text-indigo-300">
                    <span className="text-indigo-500 font-bold mt-0.5 flex-shrink-0">{i + 1}.</span>
                    {a}
                  </li>
                ))}
              </ol>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

// ─── AccountCard ──────────────────────────────────────────────────────────────

function AccountCard({ account, onClick }: { account: Account; onClick: () => void }) {
  const sm = STATUS_META[account.onboarding_status] ?? STATUS_META.at_risk;
  const am = ACTION_META[account.onboarding_action] ?? ACTION_META.monitor;

  return (
    <button
      onClick={onClick}
      className="w-full text-left bg-slate-800/60 border border-slate-700/50 rounded-2xl p-5 hover:border-indigo-500/50 hover:bg-slate-800 transition-all group"
    >
      <div className="flex items-start gap-4">
        <OnboardingRing score={account.overall_score} status={account.onboarding_status} />
        <div className="flex-1 min-w-0">
          <div className="flex items-start justify-between gap-2">
            <p className="text-white font-semibold text-sm group-hover:text-indigo-300 transition-colors truncate">
              {account.account_name}
            </p>
            <span className={`text-xs font-semibold px-2 py-0.5 rounded-full flex-shrink-0 ${sm.bg} ${sm.color}`}>
              {sm.label}
            </span>
          </div>

          <div className="mt-1 flex flex-wrap items-center gap-2 text-xs text-slate-400">
            <span>{fmt(account.arr_eur)}</span>
            {account.go_live_done ? (
              <span className="text-emerald-400">● Go-live complété</span>
            ) : account.days_remaining < 0 ? (
              <span className="text-red-400 font-semibold">● Retard {-account.days_remaining}j</span>
            ) : (
              <span>Go-live dans {account.days_remaining}j</span>
            )}
          </div>

          <div className="mt-2 flex items-center gap-2">
            <div className={`w-1.5 h-1.5 rounded-full ${am.dot}`} />
            <span className={`text-xs ${am.color}`}>{am.label}</span>
            <span className={`text-xs ml-1 ${account.schedule_delta_pct >= 0 ? "text-emerald-400" : "text-orange-400"}`}>
              {account.schedule_delta_pct >= 0 ? "+" : ""}{account.schedule_delta_pct.toFixed(0)}% planning
            </span>
          </div>

          {/* Dimension mini bars */}
          <div className="mt-3 space-y-1.5">
            {[
              { label: "Jalons",     val: account.milestone_score,  color: "bg-indigo-500" },
              { label: "Équipes",    val: account.engagement_score, color: "bg-violet-500" },
              { label: "Santé",      val: account.health_score,     color: "bg-emerald-500" },
            ].map(({ label, val, color }) => (
              <div key={label}>
                <div className="flex justify-between text-[10px] text-slate-500 mb-0.5">
                  <span>{label}</span>
                  <span>{val.toFixed(0)}</span>
                </div>
                <div className="h-1 bg-slate-700 rounded-full overflow-hidden">
                  <div className={`h-full rounded-full ${color}`} style={{ width: `${Math.min(100, val)}%` }} />
                </div>
              </div>
            ))}
          </div>

          {account.blockers.length > 0 && (
            <p className="text-xs text-orange-400 mt-2">
              {account.blockers.length} blocage{account.blockers.length > 1 ? "s" : ""}
            </p>
          )}
        </div>
      </div>
    </button>
  );
}

// ─── Page ─────────────────────────────────────────────────────────────────────

export default function OnboardingHealthPage() {
  const [accounts, setAccounts] = useState<Account[]>([]);
  const [summary, setSummary] = useState<Summary | null>(null);
  const [statusFilter, setStatusFilter] = useState("all");
  const [selected, setSelected] = useState<Account | null>(null);
  const [loading, setLoading] = useState(true);

  const fetchData = useCallback(async (status: string) => {
    setLoading(true);
    try {
      const params = new URLSearchParams();
      if (status !== "all") params.set("status", status);
      const res = await fetch(`/api/onboarding-health?${params}`);
      const data = await res.json();
      setAccounts(data.accounts ?? []);
      setSummary(data.summary ?? null);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { fetchData(statusFilter); }, [fetchData, statusFilter]);

  const sc = summary?.status_counts ?? {};

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 lg:p-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-white">Santé Onboarding</h1>
        <p className="text-slate-400 text-sm mt-1">
          Suivi des jalons d'onboarding, blocages et risques d'échec pour les nouveaux clients
        </p>
      </div>

      {/* KPI strip */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        {[
          { label: "Onboardings suivis",    value: summary?.total ?? "—",                                         sub: "total" },
          { label: "Complétion moyenne",    value: summary ? `${summary.avg_completion_pct}%` : "—",              sub: "jalons" },
          { label: "ARR à risque",          value: summary ? fmt(summary.total_arr_at_risk_eur) : "—",            sub: "critique + à risque" },
          { label: "Go-lives complétés",    value: summary?.completed_count ?? "—",                               sub: `${summary?.overdue_count ?? 0} en retard` },
        ].map(({ label, value, sub }) => (
          <div key={label} className="bg-slate-800/60 border border-slate-700/50 rounded-2xl p-5">
            <p className="text-slate-400 text-xs mb-1">{label}</p>
            <p className="text-white text-2xl font-bold">{value}</p>
            <p className="text-slate-500 text-xs mt-1">{sub}</p>
          </div>
        ))}
      </div>

      {/* Status distribution */}
      {summary && Object.keys(sc).length > 0 && (
        <div className="bg-slate-800/60 border border-slate-700/50 rounded-2xl p-5 mb-8">
          <h2 className="text-slate-300 text-sm font-semibold mb-4">Répartition des statuts d'onboarding</h2>
          <div className="flex gap-1 h-5 rounded-full overflow-hidden mb-3">
            {(["on_track","at_risk","delayed","critical"] as const).map((s) => {
              const count = sc[s] ?? 0;
              const pct = summary.total > 0 ? (count / summary.total) * 100 : 0;
              if (pct === 0) return null;
              return (
                <div
                  key={s}
                  style={{ width: `${pct}%`, backgroundColor: STATUS_META[s].ring }}
                  className="h-full"
                  title={`${STATUS_META[s].label}: ${count}`}
                />
              );
            })}
          </div>
          <div className="flex flex-wrap gap-3">
            {(["on_track","at_risk","delayed","critical"] as const).map((s) => {
              const count = sc[s] ?? 0;
              if (!count) return null;
              const m = STATUS_META[s];
              return (
                <div key={s} className="flex items-center gap-1.5 text-xs">
                  <div className="w-2 h-2 rounded-full" style={{ backgroundColor: m.ring }} />
                  <span className={m.color}>{m.label}</span>
                  <span className="text-slate-500">({count})</span>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Status filter tabs */}
      <div className="flex flex-wrap gap-2 mb-6">
        {STATUS_ORDER.map((s) => {
          const isAll = s === "all";
          const count = isAll ? (summary?.total ?? 0) : (sc[s] ?? 0);
          const active = statusFilter === s;
          const meta = isAll ? null : STATUS_META[s];
          return (
            <button
              key={s}
              onClick={() => setStatusFilter(s)}
              className={`px-4 py-2 rounded-full text-sm font-medium transition-all flex items-center gap-2 ${
                active
                  ? "bg-indigo-600 text-white"
                  : "bg-slate-800 text-slate-400 hover:text-white hover:bg-slate-700"
              }`}
            >
              {meta && <div className="w-2 h-2 rounded-full" style={{ backgroundColor: meta.ring }} />}
              {isAll ? "Tous" : meta?.label}
              <span className={`text-xs px-1.5 py-0.5 rounded-full ${active ? "bg-white/20" : "bg-slate-700"}`}>
                {count}
              </span>
            </button>
          );
        })}
      </div>

      {/* Account grid */}
      {loading ? (
        <div className="flex justify-center py-20">
          <div className="w-8 h-8 border-2 border-indigo-500 border-t-transparent rounded-full animate-spin" />
        </div>
      ) : accounts.length === 0 ? (
        <div className="text-center py-20 text-slate-500">Aucun onboarding pour ce filtre</div>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-4">
          {accounts.map((acc) => (
            <AccountCard key={acc.account_id} account={acc} onClick={() => setSelected(acc)} />
          ))}
        </div>
      )}

      {/* Modal */}
      {selected && <AccountModal account={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
