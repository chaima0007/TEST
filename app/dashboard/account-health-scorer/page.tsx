"use client";

import { useState, useEffect, useRef, useCallback } from "react";

// ─── Types ────────────────────────────────────────────────────────────────────

type HealthTier = "champion" | "healthy" | "at_risk" | "critical";
type HealthAction = "celebrate" | "maintain" | "intervene" | "escalate";
type ChurnRisk = "low" | "medium" | "high" | "imminent";
type ExpansionPotential = "strong" | "moderate" | "limited" | "none";

interface Account {
  account_id: string;
  account_name: string;
  arr_eur: number;
  segment: string;
  health_score: number;
  health_tier: HealthTier;
  health_action: HealthAction;
  churn_risk: ChurnRisk;
  expansion_potential: ExpansionPotential;
  health_drivers: string[];
  risk_signals: string[];
  recommended_plays: string[];
  renewal_probability_pct: number;
}

interface Summary {
  total: number;
  tier_counts: Record<string, number>;
  action_counts: Record<string, number>;
  churn_counts: Record<string, number>;
  avg_health_score: number;
  champion_count: number;
  critical_count: number;
  total_arr_at_risk_eur: number;
}

// ─── Helpers ──────────────────────────────────────────────────────────────────

const TIER_META: Record<HealthTier, { label: string; color: string; ring: string; bg: string; badge: string }> = {
  champion:  { label: "Champion",  color: "text-emerald-400", ring: "#34d399", bg: "bg-emerald-900/30", badge: "bg-emerald-500/20 text-emerald-300 border-emerald-700" },
  healthy:   { label: "Sain",      color: "text-sky-400",     ring: "#38bdf8", bg: "bg-sky-900/30",     badge: "bg-sky-500/20 text-sky-300 border-sky-700" },
  at_risk:   { label: "À risque",  color: "text-amber-400",   ring: "#fbbf24", bg: "bg-amber-900/30",   badge: "bg-amber-500/20 text-amber-300 border-amber-700" },
  critical:  { label: "Critique",  color: "text-red-400",     ring: "#f87171", bg: "bg-red-900/30",     badge: "bg-red-500/20 text-red-300 border-red-700" },
};

const ACTION_META: Record<HealthAction, { label: string; color: string }> = {
  celebrate: { label: "Célébrer",   color: "text-emerald-400" },
  maintain:  { label: "Maintenir",  color: "text-sky-400" },
  intervene: { label: "Intervenir", color: "text-amber-400" },
  escalate:  { label: "Escalader",  color: "text-red-400" },
};

const CHURN_META: Record<ChurnRisk, { label: string; color: string }> = {
  low:     { label: "Faible",   color: "text-emerald-400" },
  medium:  { label: "Moyen",    color: "text-amber-400" },
  high:    { label: "Élevé",    color: "text-orange-400" },
  imminent:{ label: "Imminent", color: "text-red-400" },
};

const EXPANSION_META: Record<ExpansionPotential, { label: string; color: string }> = {
  strong:   { label: "Fort",    color: "text-emerald-400" },
  moderate: { label: "Modéré",  color: "text-sky-400" },
  limited:  { label: "Limité",  color: "text-slate-400" },
  none:     { label: "Aucun",   color: "text-slate-500" },
};

function fmt(n: number): string {
  if (n >= 1_000_000) return `${(n / 1_000_000).toFixed(1)}M`;
  if (n >= 1_000) return `${(n / 1_000).toFixed(0)}k`;
  return `${n}`;
}

// ─── HealthRing SVG ───────────────────────────────────────────────────────────

function HealthRing({ score, tier }: { score: number; tier: HealthTier }) {
  const r = 38;
  const circ = 2 * Math.PI * r;
  const arc = (score / 100) * circ;
  const color = TIER_META[tier].ring;

  return (
    <svg width="96" height="96" viewBox="0 0 96 96" className="flex-shrink-0">
      <circle cx="48" cy="48" r={r} fill="none" stroke="#1e293b" strokeWidth="10" />
      <circle
        cx="48" cy="48" r={r} fill="none"
        stroke={color} strokeWidth="10"
        strokeDasharray={`${arc} ${circ - arc}`}
        strokeLinecap="round"
        transform="rotate(-90 48 48)"
      />
      <text x="48" y="44" textAnchor="middle" fill={color} fontSize="18" fontWeight="700" fontFamily="sans-serif">
        {score}
      </text>
      <text x="48" y="60" textAnchor="middle" fill="#94a3b8" fontSize="10" fontFamily="sans-serif">
        /100
      </text>
    </svg>
  );
}

// ─── AccountCard ──────────────────────────────────────────────────────────────

function AccountCard({ account, onClick }: { account: Account; onClick: () => void }) {
  const tm = TIER_META[account.health_tier];
  const am = ACTION_META[account.health_action];
  const cm = CHURN_META[account.churn_risk];

  return (
    <button
      onClick={onClick}
      className={`w-full text-left rounded-xl border border-slate-800 ${tm.bg} p-4 hover:border-slate-600 transition-colors`}
    >
      <div className="flex items-start gap-4">
        <HealthRing score={account.health_score} tier={account.health_tier} />
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 flex-wrap mb-1">
            <span className={`text-xs font-bold px-2 py-0.5 rounded border ${tm.badge}`}>{tm.label}</span>
            <span className="text-xs text-slate-400 capitalize">{account.segment.replace("_", " ")}</span>
          </div>
          <h3 className="text-white font-semibold text-sm truncate">{account.account_name}</h3>
          <p className="text-slate-400 text-xs mt-0.5">ARR: <span className="text-white font-medium">€{fmt(account.arr_eur)}</span></p>

          <div className="mt-2 grid grid-cols-3 gap-2 text-xs">
            <div>
              <span className="text-slate-500 block">Action</span>
              <span className={`font-semibold ${am.color}`}>{am.label}</span>
            </div>
            <div>
              <span className="text-slate-500 block">Churn</span>
              <span className={`font-semibold ${cm.color}`}>{cm.label}</span>
            </div>
            <div>
              <span className="text-slate-500 block">Renouvellement</span>
              <span className="text-white font-semibold">{account.renewal_probability_pct}%</span>
            </div>
          </div>

          {account.risk_signals.length > 0 && (
            <p className="mt-2 text-xs text-amber-300/80 truncate">⚠ {account.risk_signals[0]}</p>
          )}
        </div>
      </div>
    </button>
  );
}

// ─── AccountModal ─────────────────────────────────────────────────────────────

function AccountModal({ account, onClose }: { account: Account; onClose: () => void }) {
  const [tab, setTab] = useState<"signaux" | "risques" | "plays">("signaux");
  const overlayRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const fn = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", fn);
    return () => window.removeEventListener("keydown", fn);
  }, [onClose]);

  const tm = TIER_META[account.health_tier];
  const am = ACTION_META[account.health_action];
  const cm = CHURN_META[account.churn_risk];
  const em = EXPANSION_META[account.expansion_potential];

  return (
    <div
      ref={overlayRef}
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 p-4"
      onClick={(e) => { if (e.target === overlayRef.current) onClose(); }}
    >
      <div className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-2xl max-h-[90vh] overflow-y-auto shadow-2xl">
        {/* Header */}
        <div className="flex items-start justify-between p-5 border-b border-slate-800">
          <div className="flex items-center gap-4">
            <HealthRing score={account.health_score} tier={account.health_tier} />
            <div>
              <h2 className="text-white font-bold text-lg">{account.account_name}</h2>
              <p className="text-slate-400 text-sm capitalize">{account.segment.replace("_", " ")} · ARR €{fmt(account.arr_eur)}</p>
              <div className="flex gap-2 mt-1 flex-wrap">
                <span className={`text-xs font-bold px-2 py-0.5 rounded border ${tm.badge}`}>{tm.label}</span>
              </div>
            </div>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl leading-none p-1">×</button>
        </div>

        {/* KPIs */}
        <div className="grid grid-cols-4 gap-0 divide-x divide-slate-800 border-b border-slate-800">
          {[
            { label: "Action", value: am.label, color: am.color },
            { label: "Risque Churn", value: cm.label, color: cm.color },
            { label: "Expansion", value: em.label, color: em.color },
            { label: "Renouvellement", value: `${account.renewal_probability_pct}%`, color: "text-white" },
          ].map((k) => (
            <div key={k.label} className="px-4 py-3 text-center">
              <p className="text-xs text-slate-500">{k.label}</p>
              <p className={`text-sm font-bold ${k.color}`}>{k.value}</p>
            </div>
          ))}
        </div>

        {/* Tabs */}
        <div className="flex border-b border-slate-800">
          {(["signaux", "risques", "plays"] as const).map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`flex-1 py-2.5 text-xs font-semibold uppercase tracking-wide transition-colors ${
                tab === t ? "text-indigo-400 border-b-2 border-indigo-400" : "text-slate-500 hover:text-slate-300"
              }`}
            >
              {t === "signaux" ? "Points Forts" : t === "risques" ? "Signaux Risque" : "Plans d'Action"}
            </button>
          ))}
        </div>

        {/* Tab content */}
        <div className="p-5 space-y-2">
          {tab === "signaux" && (
            account.health_drivers.length > 0 ? (
              account.health_drivers.map((d, i) => (
                <div key={i} className="flex gap-2 text-sm">
                  <span className="text-emerald-400 mt-0.5 flex-shrink-0">✓</span>
                  <span className="text-slate-300">{d}</span>
                </div>
              ))
            ) : (
              <p className="text-slate-500 text-sm italic">Aucun signal positif identifié.</p>
            )
          )}
          {tab === "risques" && (
            account.risk_signals.length > 0 ? (
              account.risk_signals.map((s, i) => (
                <div key={i} className="flex gap-2 text-sm">
                  <span className="text-red-400 mt-0.5 flex-shrink-0">⚠</span>
                  <span className="text-slate-300">{s}</span>
                </div>
              ))
            ) : (
              <p className="text-slate-500 text-sm italic">Aucun signal de risque. Compte en bonne santé.</p>
            )
          )}
          {tab === "plays" && (
            account.recommended_plays.map((p, i) => (
              <div key={i} className="flex gap-2 text-sm">
                <span className="text-indigo-400 mt-0.5 flex-shrink-0">→</span>
                <span className="text-slate-300">{p}</span>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}

// ─── Page ─────────────────────────────────────────────────────────────────────

export default function AccountHealthScorerPage() {
  const [accounts, setAccounts] = useState<Account[]>([]);
  const [summary, setSummary] = useState<Summary | null>(null);
  const [loading, setLoading] = useState(true);
  const [selected, setSelected] = useState<Account | null>(null);
  const [tierFilter, setTierFilter] = useState<string>("all");
  const [actionFilter, setActionFilter] = useState<string>("all");

  const fetchData = useCallback(async () => {
    setLoading(true);
    const params = new URLSearchParams();
    if (tierFilter !== "all") params.set("tier", tierFilter);
    if (actionFilter !== "all") params.set("action", actionFilter);
    const res = await fetch(`/api/account-health-scorer?${params}`);
    const data = await res.json();
    setAccounts(data.accounts ?? []);
    setSummary(data.summary ?? null);
    setLoading(false);
  }, [tierFilter, actionFilter]);

  useEffect(() => { fetchData(); }, [fetchData]);

  const tiers: HealthTier[] = ["champion", "healthy", "at_risk", "critical"];
  const actions: HealthAction[] = ["celebrate", "maintain", "intervene", "escalate"];

  const kpis = summary
    ? [
        { label: "Comptes analysés",     value: summary.total.toString(),               sub: "portefeuille complet" },
        { label: "Champions",            value: summary.champion_count.toString(),       sub: "santé ≥ 80/100" },
        { label: "Critiques",            value: summary.critical_count.toString(),       sub: "action immédiate" },
        { label: "Score santé moyen",    value: `${summary.avg_health_score}/100`,       sub: "portfolio score" },
        { label: "ARR à risque",         value: `€${fmt(summary.total_arr_at_risk_eur)}`, sub: "at_risk + critical" },
        { label: "Taux champions",       value: `${Math.round((summary.champion_count / summary.total) * 100)}%`, sub: "du portefeuille" },
      ]
    : [];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
      {selected && <AccountModal account={selected} onClose={() => setSelected(null)} />}

      {/* Header */}
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-white">Account Health Scorer</h1>
        <p className="text-slate-400 text-sm mt-1">Score de santé client — détection précoce du churn et opportunités d'expansion</p>
      </div>

      {/* KPI strip */}
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3 mb-6">
        {kpis.map((k) => (
          <div key={k.label} className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <p className="text-xs text-slate-500 mb-1">{k.label}</p>
            <p className="text-xl font-bold text-white">{k.value}</p>
            <p className="text-xs text-slate-600 mt-0.5">{k.sub}</p>
          </div>
        ))}
      </div>

      {/* Health tier distribution */}
      {summary && (
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 mb-6">
          <p className="text-xs text-slate-500 mb-3 font-semibold uppercase tracking-wide">Distribution par tier de santé</p>
          <div className="flex h-3 rounded-full overflow-hidden gap-0.5">
            {tiers.map((t) => {
              const count = summary.tier_counts[t] ?? 0;
              const pct = summary.total > 0 ? (count / summary.total) * 100 : 0;
              const colors: Record<string, string> = {
                champion: "bg-emerald-500", healthy: "bg-sky-500",
                at_risk: "bg-amber-500", critical: "bg-red-500",
              };
              return pct > 0 ? (
                <div key={t} className={`${colors[t]} rounded-sm`} style={{ width: `${pct}%` }} title={`${TIER_META[t].label}: ${count}`} />
              ) : null;
            })}
          </div>
          <div className="flex gap-4 mt-2 flex-wrap">
            {tiers.map((t) => (
              <div key={t} className="flex items-center gap-1.5 text-xs text-slate-400">
                <span className={`w-2 h-2 rounded-full ${t === "champion" ? "bg-emerald-500" : t === "healthy" ? "bg-sky-500" : t === "at_risk" ? "bg-amber-500" : "bg-red-500"}`} />
                {TIER_META[t].label}: {summary.tier_counts[t] ?? 0}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Filters */}
      <div className="flex flex-col sm:flex-row gap-3 mb-6">
        <div className="flex gap-1 flex-wrap">
          {["all", ...tiers].map((t) => (
            <button
              key={t}
              onClick={() => setTierFilter(t)}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-colors ${
                tierFilter === t
                  ? "bg-indigo-600 text-white"
                  : "bg-slate-800 text-slate-400 hover:text-white"
              }`}
            >
              {t === "all" ? "Tous les tiers" : TIER_META[t as HealthTier].label}
            </button>
          ))}
        </div>
        <div className="flex gap-1 flex-wrap">
          {["all", ...actions].map((a) => (
            <button
              key={a}
              onClick={() => setActionFilter(a)}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-colors ${
                actionFilter === a
                  ? "bg-violet-600 text-white"
                  : "bg-slate-800 text-slate-400 hover:text-white"
              }`}
            >
              {a === "all" ? "Toutes actions" : ACTION_META[a as HealthAction].label}
            </button>
          ))}
        </div>
      </div>

      {/* Accounts grid */}
      {loading ? (
        <div className="text-center text-slate-500 py-20">Chargement…</div>
      ) : accounts.length === 0 ? (
        <div className="text-center text-slate-500 py-20">Aucun compte pour ces filtres.</div>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
          {accounts.map((a) => (
            <AccountCard key={a.account_id} account={a} onClick={() => setSelected(a)} />
          ))}
        </div>
      )}
    </div>
  );
}
