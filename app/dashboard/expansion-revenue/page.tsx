"use client";

import { useState, useEffect, useRef } from "react";

// ─── Types ───────────────────────────────────────────────────────────────────

type ExpansionTier = "hot" | "warm" | "cool" | "cold";
type ExpansionAction = "close" | "nurture" | "qualify" | "watch";

interface Account {
  account_id: string;
  account_name: string;
  current_arr_eur: number;
  product_tier: string;
  expansion_tier: ExpansionTier;
  expansion_action: ExpansionAction;
  expansion_score: number;
  utilization_score: number;
  relationship_score: number;
  growth_score: number;
  timing_score: number;
  opportunity_types: string[];
  estimated_expansion_eur: number;
  seat_utilization_pct: number;
  modules_utilization_pct: number;
  positive_signals: string[];
  risk_factors: string[];
  recommended_actions: string[];
}

interface Summary {
  total: number;
  tier_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_expansion_score: number;
  total_estimated_expansion_eur: number;
  total_current_arr_eur: number;
  hot_count: number;
  close_ready_count: number;
}

// ─── Helpers ─────────────────────────────────────────────────────────────────

const TIER_META: Record<ExpansionTier, { label: string; color: string; bg: string; ring: string }> = {
  hot:  { label: "Chaud",   color: "text-red-400",     bg: "bg-red-400",     ring: "#f87171" },
  warm: { label: "Tiède",   color: "text-amber-400",   bg: "bg-amber-400",   ring: "#fbbf24" },
  cool: { label: "Modéré",  color: "text-blue-400",    bg: "bg-blue-400",    ring: "#60a5fa" },
  cold: { label: "Faible",  color: "text-slate-400",   bg: "bg-slate-400",   ring: "#94a3b8" },
};

const ACTION_META: Record<ExpansionAction, { label: string; color: string; bg: string }> = {
  close:   { label: "Closer maintenant", color: "text-red-300",     bg: "bg-red-900/40" },
  nurture: { label: "Nurturer",          color: "text-amber-300",   bg: "bg-amber-900/40" },
  qualify: { label: "Qualifier",         color: "text-blue-300",    bg: "bg-blue-900/40" },
  watch:   { label: "Observer",          color: "text-slate-300",   bg: "bg-slate-800/40" },
};

const OPP_TYPE_LABELS: Record<string, string> = {
  SEAT_EXPANSION: "Licences",
  UPSELL: "Montée en gamme",
  CROSS_SELL: "Vente croisée",
  RENEWAL_UPLIFT: "Revalorisation",
  NEW_MODULE: "Activation module",
};

const TIER_LABELS: Record<string, string> = {
  starter: "Starter",
  professional: "Pro",
  enterprise: "Enterprise",
};

function fmt(n: number) {
  if (n >= 1_000_000) return `${(n / 1_000_000).toFixed(1)}M`;
  if (n >= 1_000) return `${(n / 1_000).toFixed(0)}k`;
  return `${n.toFixed(0)}`;
}
function fmtEur(n: number) { return `€${fmt(n)}`; }

// ─── ExpansionRing ────────────────────────────────────────────────────────────

function ExpansionRing({ score, tier }: { score: number; tier: ExpansionTier }) {
  const r = 28;
  const circ = 2 * Math.PI * r;
  const arc = (score / 100) * circ;
  const color = TIER_META[tier].ring;
  return (
    <svg width="72" height="72" viewBox="0 0 72 72" className="flex-shrink-0">
      <circle cx="36" cy="36" r={r} fill="none" stroke="#1e293b" strokeWidth="7" />
      <circle
        cx="36" cy="36" r={r}
        fill="none"
        stroke={color}
        strokeWidth="7"
        strokeDasharray={`${arc} ${circ - arc}`}
        strokeLinecap="round"
        transform="rotate(-90 36 36)"
      />
      <text x="36" y="38" textAnchor="middle" dominantBaseline="middle" fill="white" fontSize="12" fontWeight="700">
        {score.toFixed(1)}
      </text>
    </svg>
  );
}

// ─── MiniBar ─────────────────────────────────────────────────────────────────

function MiniBar({ value, label, color }: { value: number; label: string; color: string }) {
  return (
    <div className="space-y-0.5">
      <div className="flex justify-between text-[10px] text-slate-400">
        <span>{label}</span>
        <span>{value.toFixed(0)}</span>
      </div>
      <div className="h-1 bg-slate-800 rounded-full overflow-hidden">
        <div className={`h-full rounded-full ${color}`} style={{ width: `${Math.min(100, value)}%` }} />
      </div>
    </div>
  );
}

// ─── ScoreBar (modal) ─────────────────────────────────────────────────────────

function ScoreBar({ value, label, weight, color }: { value: number; label: string; weight: string; color: string }) {
  return (
    <div className="space-y-1">
      <div className="flex items-center justify-between text-xs">
        <span className="text-slate-300">{label}</span>
        <div className="flex items-center gap-2">
          <span className="text-slate-500 text-[10px]">{weight}</span>
          <span className={`font-semibold ${color}`}>{value.toFixed(1)}</span>
        </div>
      </div>
      <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
        <div className={`h-full rounded-full ${color.replace("text-", "bg-")}`} style={{ width: `${Math.min(100, value)}%` }} />
      </div>
    </div>
  );
}

// ─── AccountModal ─────────────────────────────────────────────────────────────

function AccountModal({ account, onClose }: { account: Account; onClose: () => void }) {
  const ref = useRef<HTMLDivElement>(null);
  const tier = TIER_META[account.expansion_tier];
  const action = ACTION_META[account.expansion_action];

  useEffect(() => {
    const h = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    document.addEventListener("keydown", h);
    return () => document.removeEventListener("keydown", h);
  }, [onClose]);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm" onClick={(e) => { if (ref.current && !ref.current.contains(e.target as Node)) onClose(); }}>
      <div ref={ref} className="w-full max-w-2xl bg-slate-900 border border-slate-700 rounded-2xl shadow-2xl max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="flex items-start justify-between p-6 border-b border-slate-800">
          <div className="space-y-1">
            <h2 className="text-white font-bold text-lg">{account.account_name}</h2>
            <p className="text-slate-400 text-sm">{TIER_LABELS[account.product_tier] ?? account.product_tier} · ARR actuel : {fmtEur(account.current_arr_eur)}</p>
            <div className="flex items-center gap-2 mt-2">
              <span className={`inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs font-semibold ${tier.color} bg-slate-800`}>
                <span className={`w-1.5 h-1.5 rounded-full ${tier.bg}`} />
                {tier.label}
              </span>
              <span className={`inline-flex px-2 py-0.5 rounded-full text-xs font-semibold ${action.color} ${action.bg}`}>
                {action.label}
              </span>
            </div>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white p-1 ml-4">✕</button>
        </div>

        <div className="p-6 space-y-6">
          {/* KPI row */}
          <div className="grid grid-cols-3 gap-3">
            <div className="bg-slate-800/60 rounded-xl p-3 text-center">
              <p className="text-slate-400 text-xs mb-1">ARR actuel</p>
              <p className="text-white font-bold text-lg">{fmtEur(account.current_arr_eur)}</p>
            </div>
            <div className="bg-slate-800/60 rounded-xl p-3 text-center">
              <p className="text-slate-400 text-xs mb-1">Expansion estimée</p>
              <p className={`font-bold text-lg ${tier.color}`}>{fmtEur(account.estimated_expansion_eur)}</p>
            </div>
            <div className="bg-slate-800/60 rounded-xl p-3 text-center">
              <p className="text-slate-400 text-xs mb-1">Croissance potentielle</p>
              <p className="text-emerald-400 font-bold text-lg">
                +{account.current_arr_eur > 0 ? ((account.estimated_expansion_eur / account.current_arr_eur) * 100).toFixed(0) : 0}%
              </p>
            </div>
          </div>

          {/* Opportunity types */}
          {account.opportunity_types.length > 0 && (
            <div className="space-y-2">
              <h3 className="text-slate-300 font-semibold text-sm">Types d'opportunités</h3>
              <div className="flex flex-wrap gap-2">
                {account.opportunity_types.map((t) => (
                  <span key={t} className={`px-2.5 py-1 rounded-lg text-xs font-medium ${tier.color} bg-slate-800`}>
                    {OPP_TYPE_LABELS[t] ?? t}
                  </span>
                ))}
              </div>
            </div>
          )}

          {/* Usage metrics */}
          <div className="grid grid-cols-2 gap-3">
            <div className="bg-slate-800/40 rounded-xl p-3 space-y-1">
              <p className="text-slate-400 text-xs">Utilisation licences</p>
              <p className="text-white font-bold text-lg">{account.seat_utilization_pct.toFixed(0)}%</p>
              <div className="h-1.5 bg-slate-700 rounded-full overflow-hidden">
                <div
                  className={`h-full rounded-full ${account.seat_utilization_pct > 80 ? "bg-red-500" : account.seat_utilization_pct > 60 ? "bg-amber-500" : "bg-blue-500"}`}
                  style={{ width: `${Math.min(100, account.seat_utilization_pct)}%` }}
                />
              </div>
            </div>
            <div className="bg-slate-800/40 rounded-xl p-3 space-y-1">
              <p className="text-slate-400 text-xs">Adoption modules</p>
              <p className="text-white font-bold text-lg">{account.modules_utilization_pct.toFixed(0)}%</p>
              <div className="h-1.5 bg-slate-700 rounded-full overflow-hidden">
                <div
                  className={`h-full rounded-full ${account.modules_utilization_pct > 80 ? "bg-emerald-500" : account.modules_utilization_pct > 50 ? "bg-blue-500" : "bg-amber-500"}`}
                  style={{ width: `${Math.min(100, account.modules_utilization_pct)}%` }}
                />
              </div>
            </div>
          </div>

          {/* Score breakdown */}
          <div className="space-y-3">
            <h3 className="text-slate-300 font-semibold text-sm">Analyse d'expansion</h3>
            <ScoreBar value={account.utilization_score} label="Signal d'utilisation" weight="30%" color="text-blue-400" />
            <ScoreBar value={account.relationship_score} label="Signal relationnel" weight="25%" color="text-violet-400" />
            <ScoreBar value={account.growth_score} label="Signal de croissance" weight="25%" color="text-emerald-400" />
            <ScoreBar value={account.timing_score} label="Signal de timing" weight="20%" color="text-amber-400" />
            <div className="pt-1 border-t border-slate-800">
              <ScoreBar value={account.expansion_score} label="Score expansion global" weight="composite" color={tier.color} />
            </div>
          </div>

          {/* Positive signals */}
          {account.positive_signals.length > 0 && (
            <div className="space-y-2">
              <h3 className="text-emerald-400 font-semibold text-sm">Signaux positifs</h3>
              <ul className="space-y-1">
                {account.positive_signals.map((s, i) => (
                  <li key={i} className="flex items-start gap-2 text-xs text-slate-300">
                    <span className="text-emerald-400 flex-shrink-0 mt-0.5">▲</span>{s}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Risk factors */}
          {account.risk_factors.length > 0 && (
            <div className="space-y-2">
              <h3 className="text-red-400 font-semibold text-sm">Risques</h3>
              <ul className="space-y-1">
                {account.risk_factors.map((r, i) => (
                  <li key={i} className="flex items-start gap-2 text-xs text-slate-300">
                    <span className="text-red-400 flex-shrink-0 mt-0.5">▼</span>{r}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Recommended actions */}
          {account.recommended_actions.length > 0 && (
            <div className="space-y-2">
              <h3 className="text-amber-400 font-semibold text-sm">Actions recommandées</h3>
              <ol className="space-y-1">
                {account.recommended_actions.map((a, i) => (
                  <li key={i} className="flex items-start gap-2 text-xs text-slate-300">
                    <span className="text-amber-400 font-bold flex-shrink-0 mt-0.5">{i + 1}.</span>{a}
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
  const tier = TIER_META[account.expansion_tier];
  const action = ACTION_META[account.expansion_action];

  return (
    <div
      onClick={onClick}
      className="bg-slate-800/60 border border-slate-700/50 rounded-xl p-4 hover:border-slate-500 hover:bg-slate-800 transition-all cursor-pointer space-y-3"
    >
      {/* Header */}
      <div className="flex items-start gap-3">
        <ExpansionRing score={account.expansion_score} tier={account.expansion_tier} />
        <div className="flex-1 min-w-0 space-y-1">
          <p className="text-white font-semibold text-sm truncate">{account.account_name}</p>
          <p className="text-slate-400 text-xs">{TIER_LABELS[account.product_tier] ?? account.product_tier}</p>
          <div className="flex items-center gap-1.5 flex-wrap">
            <span className={`px-1.5 py-0.5 rounded text-[10px] font-semibold ${tier.color} bg-slate-700`}>
              {tier.label}
            </span>
            <span className={`px-1.5 py-0.5 rounded text-[10px] font-semibold ${action.color} ${action.bg}`}>
              {action.label}
            </span>
          </div>
        </div>
      </div>

      {/* ARR rows */}
      <div className="flex items-center justify-between text-xs border-t border-slate-700/50 pt-2">
        <span className="text-slate-400">ARR actuel</span>
        <span className="text-white font-semibold">{fmtEur(account.current_arr_eur)}</span>
      </div>
      <div className="flex items-center justify-between text-xs">
        <span className="text-slate-400">Expansion estimée</span>
        <span className={`font-semibold ${tier.color}`}>{fmtEur(account.estimated_expansion_eur)}</span>
      </div>

      {/* Opportunity types */}
      {account.opportunity_types.length > 0 && (
        <div className="flex flex-wrap gap-1 border-t border-slate-700/50 pt-2">
          {account.opportunity_types.slice(0, 3).map((t) => (
            <span key={t} className="px-1.5 py-0.5 rounded text-[9px] font-medium text-slate-400 bg-slate-700/60">
              {OPP_TYPE_LABELS[t] ?? t}
            </span>
          ))}
          {account.opportunity_types.length > 3 && (
            <span className="px-1.5 py-0.5 rounded text-[9px] text-slate-500">+{account.opportunity_types.length - 3}</span>
          )}
        </div>
      )}

      {/* Score bars */}
      <div className="space-y-1.5 border-t border-slate-700/50 pt-2">
        <MiniBar value={account.utilization_score} label="Utilisation" color="bg-blue-500" />
        <MiniBar value={account.relationship_score} label="Relation" color="bg-violet-500" />
        <MiniBar value={account.growth_score} label="Croissance" color="bg-emerald-500" />
      </div>

      {/* Risk count */}
      {account.risk_factors.length > 0 && (
        <div className="text-[10px] text-red-400">
          ▼ {account.risk_factors.length} risque{account.risk_factors.length > 1 ? "s" : ""} détecté{account.risk_factors.length > 1 ? "s" : ""}
        </div>
      )}
    </div>
  );
}

// ─── Main Page ────────────────────────────────────────────────────────────────

type TierFilter = "all" | ExpansionTier;

export default function ExpansionRevenuePage() {
  const [accounts, setAccounts] = useState<Account[]>([]);
  const [summary, setSummary] = useState<Summary | null>(null);
  const [filter, setFilter] = useState<TierFilter>("all");
  const [loading, setLoading] = useState(true);
  const [selected, setSelected] = useState<Account | null>(null);

  useEffect(() => {
    const params = new URLSearchParams();
    if (filter !== "all") params.set("tier", filter);
    fetch(`/api/expansion-revenue?${params}`)
      .then((r) => r.json())
      .then((data) => {
        setAccounts(data.accounts ?? []);
        setSummary(data.summary ?? null);
        setLoading(false);
      });
  }, [filter]);

  const tabs: { key: TierFilter; label: string; color?: string }[] = [
    { key: "all", label: "Tous" },
    { key: "hot", label: "Chaud", color: "text-red-400" },
    { key: "warm", label: "Tiède", color: "text-amber-400" },
    { key: "cool", label: "Modéré", color: "text-blue-400" },
    { key: "cold", label: "Faible", color: "text-slate-400" },
  ];

  const total = summary?.total ?? 0;
  const tierBars = summary
    ? [
        { key: "hot" as const, count: summary.tier_counts.hot ?? 0, bg: "bg-red-500" },
        { key: "warm" as const, count: summary.tier_counts.warm ?? 0, bg: "bg-amber-500" },
        { key: "cool" as const, count: summary.tier_counts.cool ?? 0, bg: "bg-blue-500" },
        { key: "cold" as const, count: summary.tier_counts.cold ?? 0, bg: "bg-slate-500" },
      ]
    : [];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-white">Détection Revenus d'Expansion</h1>
        <p className="text-slate-400 text-sm mt-1">Identification des opportunités d'upsell et cross-sell sur les comptes existants</p>
      </div>

      {/* KPI strip */}
      {summary && (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {[
            { label: "Comptes analysés", value: summary.total.toString(), sub: `${summary.close_ready_count} à closer maintenant`, color: "text-white" },
            { label: "Expansion estimée", value: fmtEur(summary.total_estimated_expansion_eur), sub: `ARR total : ${fmtEur(summary.total_current_arr_eur)}`, color: "text-emerald-400" },
            { label: "Opportunités chaudes", value: summary.hot_count.toString(), sub: `Score moyen : ${summary.avg_expansion_score.toFixed(1)}`, color: summary.hot_count > 0 ? "text-red-400" : "text-slate-400" },
            { label: "Croissance potentielle", value: `+${summary.total_current_arr_eur > 0 ? ((summary.total_estimated_expansion_eur / summary.total_current_arr_eur) * 100).toFixed(0) : 0}%`, sub: "Sur l'ARR existant", color: "text-amber-400" },
          ].map(({ label, value, sub, color }) => (
            <div key={label} className="bg-slate-800/60 border border-slate-700/50 rounded-xl p-4">
              <p className="text-slate-400 text-xs mb-1">{label}</p>
              <p className={`text-xl font-bold ${color}`}>{value}</p>
              <p className="text-slate-500 text-xs mt-1">{sub}</p>
            </div>
          ))}
        </div>
      )}

      {/* Tier distribution bar */}
      {total > 0 && (
        <div className="space-y-2">
          <div className="flex items-center justify-between text-xs text-slate-400">
            <span>Distribution des opportunités d'expansion</span>
            <span>{total} comptes</span>
          </div>
          <div className="flex h-2 rounded-full overflow-hidden gap-0.5">
            {tierBars.map(({ key, count, bg }) =>
              count > 0 ? (
                <div key={key} className={`${bg} transition-all`} style={{ width: `${(count / total) * 100}%` }} />
              ) : null
            )}
          </div>
          <div className="flex flex-wrap gap-3 text-xs">
            {tierBars.map(({ key, count, bg }) => (
              <span key={key} className="flex items-center gap-1 text-slate-400">
                <span className={`w-2 h-2 rounded-full ${bg}`} />
                {TIER_META[key].label} ({count})
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Filter tabs */}
      <div className="flex flex-wrap gap-2">
        {tabs.map(({ key, label, color }) => (
          <button
            key={key}
            onClick={() => setFilter(key)}
            className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-colors ${
              filter === key
                ? "bg-indigo-600 text-white"
                : `text-slate-400 hover:text-white hover:bg-slate-800 ${color ?? ""}`
            }`}
          >
            {label}
            {key !== "all" && summary && (
              <span className="ml-1.5 text-xs opacity-70">
                ({summary.tier_counts[key] ?? 0})
              </span>
            )}
          </button>
        ))}
      </div>

      {/* Account grid */}
      {loading ? (
        <div className="flex items-center justify-center h-48 text-slate-500">Chargement…</div>
      ) : accounts.length === 0 ? (
        <div className="flex items-center justify-center h-48 text-slate-500">Aucun compte trouvé</div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          {accounts.map((account) => (
            <AccountCard key={account.account_id} account={account} onClick={() => setSelected(account)} />
          ))}
        </div>
      )}

      {selected && <AccountModal account={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
