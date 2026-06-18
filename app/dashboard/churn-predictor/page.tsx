"use client";

import { useEffect, useState, useCallback, useRef } from "react";

// ─── Types ────────────────────────────────────────────────────────────────────

type Account = {
  account_id: string;
  account_name: string;
  arr_eur: number;
  churn_probability_pct: number;
  churn_risk: string;
  retention_action: string;
  churn_drivers: string[];
  retention_signals: string[];
  risk_flags: string[];
  recommended_actions: string[];
  arr_at_risk_eur: number;
  days_to_act: number;
  usage_risk_score: number;
  support_risk_score: number;
  financial_risk_score: number;
  relationship_risk_score: number;
  competitive_risk_score: number;
};

type Summary = {
  total: number;
  risk_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_churn_probability: number;
  total_arr_at_risk_eur: number;
  critical_count: number;
  emergency_count: number;
};

// ─── Meta helpers ─────────────────────────────────────────────────────────────

const RISK_META: Record<string, { label: string; color: string; ring: string; bg: string }> = {
  critical: { label: "Critique",  color: "text-red-400",     ring: "#f87171", bg: "bg-red-900/30"     },
  high:     { label: "Élevé",     color: "text-orange-400",  ring: "#fb923c", bg: "bg-orange-900/30"  },
  medium:   { label: "Moyen",     color: "text-amber-400",   ring: "#fbbf24", bg: "bg-amber-900/30"   },
  low:      { label: "Faible",    color: "text-blue-400",    ring: "#60a5fa", bg: "bg-blue-900/30"    },
  safe:     { label: "Sécurisé",  color: "text-emerald-400", ring: "#34d399", bg: "bg-emerald-900/30" },
};

const ACTION_META: Record<string, { label: string; color: string; dot: string }> = {
  emergency:  { label: "Urgence",    color: "text-red-400",     dot: "bg-red-400"     },
  rescue:     { label: "Sauvetage",  color: "text-orange-400",  dot: "bg-orange-400"  },
  proactive:  { label: "Proactif",   color: "text-amber-400",   dot: "bg-amber-400"   },
  nurture:    { label: "Nurture",    color: "text-blue-400",    dot: "bg-blue-400"    },
  expand:     { label: "Expansion",  color: "text-emerald-400", dot: "bg-emerald-400" },
};

const RISK_ORDER = ["all", "critical", "high", "medium", "low", "safe"];

function fmt(n: number) {
  return new Intl.NumberFormat("fr-FR", { style: "currency", currency: "EUR", maximumFractionDigits: 0 }).format(n);
}

// ─── ChurnRing ────────────────────────────────────────────────────────────────

function ChurnRing({ prob, risk }: { prob: number; risk: string }) {
  const r = 28;
  const circ = 2 * Math.PI * r;
  const fill = (prob / 100) * circ;
  const ringColor = RISK_META[risk]?.ring ?? "#6366f1";
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
      <text x="36" y="40" textAnchor="middle" fill="white" fontSize="12" fontWeight="700">
        {prob.toFixed(0)}%
      </text>
    </svg>
  );
}

// ─── ScoreBar ─────────────────────────────────────────────────────────────────

function ScoreBar({ label, value, color = "bg-red-500" }: { label: string; value: number; color?: string }) {
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

  const rm = RISK_META[account.churn_risk] ?? RISK_META.safe;
  const am = ACTION_META[account.retention_action] ?? ACTION_META.nurture;

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
            <ChurnRing prob={account.churn_probability_pct} risk={account.churn_risk} />
            <div>
              <h2 className="text-white font-bold text-lg leading-tight">{account.account_name}</h2>
              <div className="flex flex-wrap items-center gap-2 mt-1">
                <span className={`text-xs font-semibold px-2 py-0.5 rounded-full ${rm.bg} ${rm.color}`}>
                  {rm.label}
                </span>
                <span className="text-slate-400 text-xs">ARR {fmt(account.arr_eur)}</span>
                <span className="text-xs text-slate-400">
                  Agir dans <span className={account.days_to_act <= 7 ? "text-red-400 font-bold" : "text-amber-400"}>
                    {account.days_to_act}j
                  </span>
                </span>
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
          {/* ARR at risk + action */}
          <div className="grid grid-cols-2 gap-4">
            <div className="bg-slate-800/60 rounded-xl p-4">
              <p className="text-slate-400 text-xs mb-1">ARR à risque</p>
              <p className="text-red-400 font-bold text-xl">{fmt(account.arr_at_risk_eur)}</p>
            </div>
            <div className="flex items-center gap-3 bg-slate-800/60 rounded-xl p-4">
              <div className={`w-2.5 h-2.5 rounded-full flex-shrink-0 ${am.dot}`} />
              <div>
                <p className="text-slate-400 text-xs">Action requise</p>
                <p className={`font-semibold text-sm ${am.color}`}>{am.label}</p>
              </div>
            </div>
          </div>

          {/* Risk component scores */}
          <div>
            <h3 className="text-slate-300 text-sm font-semibold mb-3">Scores de risque par dimension</h3>
            <div className="space-y-3">
              <ScoreBar label="Usage" value={account.usage_risk_score} color="bg-red-500" />
              <ScoreBar label="Support" value={account.support_risk_score} color="bg-orange-500" />
              <ScoreBar label="Financier" value={account.financial_risk_score} color="bg-amber-500" />
              <ScoreBar label="Relation" value={account.relationship_risk_score} color="bg-violet-500" />
              <ScoreBar label="Compétitif" value={account.competitive_risk_score} color="bg-indigo-500" />
            </div>
          </div>

          {/* Churn drivers */}
          {account.churn_drivers.length > 0 && (
            <div>
              <h3 className="text-slate-300 text-sm font-semibold mb-3">
                Facteurs de churn ({account.churn_drivers.length})
              </h3>
              <ul className="space-y-1.5">
                {account.churn_drivers.map((d, i) => (
                  <li key={i} className="flex items-start gap-2 text-xs text-orange-300">
                    <span className="text-orange-400 mt-0.5 flex-shrink-0">▲</span>
                    {d}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Retention signals */}
          {account.retention_signals.length > 0 && (
            <div>
              <h3 className="text-slate-300 text-sm font-semibold mb-3">Signaux de rétention</h3>
              <ul className="space-y-1.5">
                {account.retention_signals.map((s, i) => (
                  <li key={i} className="flex items-start gap-2 text-xs text-emerald-300">
                    <span className="text-emerald-400 mt-0.5 flex-shrink-0">✓</span>
                    {s}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Risk flags */}
          {account.risk_flags.length > 0 && (
            <div>
              <h3 className="text-slate-300 text-sm font-semibold mb-3">Alertes critiques</h3>
              <ul className="space-y-1.5">
                {account.risk_flags.map((f, i) => (
                  <li key={i} className="flex items-start gap-2 text-xs text-red-300">
                    <span className="text-red-400 mt-0.5 flex-shrink-0">⚠</span>
                    {f}
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
  const rm = RISK_META[account.churn_risk] ?? RISK_META.safe;
  const am = ACTION_META[account.retention_action] ?? ACTION_META.nurture;
  return (
    <button
      onClick={onClick}
      className="w-full text-left bg-slate-800/60 border border-slate-700/50 rounded-2xl p-5 hover:border-indigo-500/50 hover:bg-slate-800 transition-all group"
    >
      <div className="flex items-start gap-4">
        <ChurnRing prob={account.churn_probability_pct} risk={account.churn_risk} />
        <div className="flex-1 min-w-0">
          <div className="flex items-start justify-between gap-2">
            <p className="text-white font-semibold text-sm group-hover:text-indigo-300 transition-colors truncate">
              {account.account_name}
            </p>
            <span className={`text-xs font-semibold px-2 py-0.5 rounded-full flex-shrink-0 ${rm.bg} ${rm.color}`}>
              {rm.label}
            </span>
          </div>

          <div className="mt-1 flex flex-wrap items-center gap-3 text-xs text-slate-400">
            <span>{fmt(account.arr_eur)} ARR</span>
            <span className="text-red-400">{fmt(account.arr_at_risk_eur)} à risque</span>
          </div>

          <div className="mt-2 flex flex-wrap items-center gap-2">
            <div className="flex items-center gap-1.5">
              <div className={`w-1.5 h-1.5 rounded-full ${am.dot}`} />
              <span className={`text-xs ${am.color}`}>{am.label}</span>
            </div>
            <span className={`text-xs ${account.days_to_act <= 7 ? "text-red-400 font-semibold" : "text-slate-400"}`}>
              Agir dans {account.days_to_act}j
            </span>
          </div>

          {/* Risk component mini bars */}
          <div className="mt-3 grid grid-cols-2 gap-x-4 gap-y-1.5">
            {[
              { label: "Usage",     val: account.usage_risk_score,        color: "bg-red-500"     },
              { label: "Support",   val: account.support_risk_score,      color: "bg-orange-500"  },
              { label: "Financier", val: account.financial_risk_score,    color: "bg-amber-500"   },
              { label: "Relation",  val: account.relationship_risk_score, color: "bg-violet-500"  },
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
        </div>
      </div>
    </button>
  );
}

// ─── Page ─────────────────────────────────────────────────────────────────────

export default function ChurnPredictorPage() {
  const [accounts, setAccounts] = useState<Account[]>([]);
  const [summary, setSummary] = useState<Summary | null>(null);
  const [riskFilter, setRiskFilter] = useState("all");
  const [selected, setSelected] = useState<Account | null>(null);
  const [loading, setLoading] = useState(true);

  const fetchData = useCallback(async (risk: string) => {
    setLoading(true);
    try {
      const params = new URLSearchParams();
      if (risk !== "all") params.set("risk", risk);
      const res = await fetch(`/api/churn-predictor?${params}`);
      const data = await res.json();
      setAccounts(data.accounts ?? []);
      setSummary(data.summary ?? null);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { fetchData(riskFilter); }, [fetchData, riskFilter]);

  const rc = summary?.risk_counts ?? {};

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 lg:p-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-white">Prédicteur de Churn</h1>
        <p className="text-slate-400 text-sm mt-1">
          Probabilité de churn par compte, ARR à risque et plan d'action de rétention
        </p>
      </div>

      {/* KPI strip */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        {[
          { label: "Comptes analysés",      value: summary?.total ?? "—",                                        sub: "total" },
          { label: "Prob. churn moyenne",   value: summary ? `${summary.avg_churn_probability}%` : "—",          sub: "portefeuille" },
          { label: "ARR total à risque",    value: summary ? fmt(summary.total_arr_at_risk_eur) : "—",           sub: "exposition" },
          { label: "Actions d'urgence",     value: summary?.emergency_count ?? "—",                              sub: "intervention immédiate" },
        ].map(({ label, value, sub }) => (
          <div key={label} className="bg-slate-800/60 border border-slate-700/50 rounded-2xl p-5">
            <p className="text-slate-400 text-xs mb-1">{label}</p>
            <p className="text-white text-2xl font-bold">{value}</p>
            <p className="text-slate-500 text-xs mt-1">{sub}</p>
          </div>
        ))}
      </div>

      {/* Churn risk distribution */}
      {summary && Object.keys(rc).length > 0 && (
        <div className="bg-slate-800/60 border border-slate-700/50 rounded-2xl p-5 mb-8">
          <h2 className="text-slate-300 text-sm font-semibold mb-4">Répartition des risques de churn</h2>
          <div className="flex gap-1 h-5 rounded-full overflow-hidden mb-3">
            {(["critical","high","medium","low","safe"] as const).map((r) => {
              const count = rc[r] ?? 0;
              const pct = summary.total > 0 ? (count / summary.total) * 100 : 0;
              if (pct === 0) return null;
              return (
                <div
                  key={r}
                  style={{ width: `${pct}%`, backgroundColor: RISK_META[r].ring }}
                  className="h-full"
                  title={`${RISK_META[r].label}: ${count}`}
                />
              );
            })}
          </div>
          <div className="flex flex-wrap gap-3">
            {(["critical","high","medium","low","safe"] as const).map((r) => {
              const count = rc[r] ?? 0;
              if (!count) return null;
              const m = RISK_META[r];
              return (
                <div key={r} className="flex items-center gap-1.5 text-xs">
                  <div className="w-2 h-2 rounded-full" style={{ backgroundColor: m.ring }} />
                  <span className={m.color}>{m.label}</span>
                  <span className="text-slate-500">({count})</span>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Risk filter tabs */}
      <div className="flex flex-wrap gap-2 mb-6">
        {RISK_ORDER.map((r) => {
          const isAll = r === "all";
          const count = isAll ? (summary?.total ?? 0) : (rc[r] ?? 0);
          const active = riskFilter === r;
          const meta = isAll ? null : RISK_META[r];
          return (
            <button
              key={r}
              onClick={() => setRiskFilter(r)}
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
        <div className="text-center py-20 text-slate-500">Aucun compte pour ce filtre</div>
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
