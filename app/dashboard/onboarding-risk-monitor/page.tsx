"use client";

import { useState, useEffect, useRef } from "react";

// ─── Types ────────────────────────────────────────────────────────────────────

type OnboardingRisk = "low" | "moderate" | "high" | "critical";
type OnboardingAction = "monitor" | "accelerate" | "rescue" | "escalate";
type OnboardingPhase = "kickoff" | "setup" | "training" | "adoption" | "value_realization";
type ChurnSignal = "none" | "early" | "moderate" | "strong";

interface Customer {
  customer_id: string;
  customer_name: string;
  arr_eur: number;
  segment: string;
  phase: OnboardingPhase;
  risk_score: number;
  risk_level: OnboardingRisk;
  risk_action: OnboardingAction;
  churn_signal: ChurnSignal;
  go_live_delay_days: number;
  risk_factors: string[];
  positive_signals: string[];
  intervention_plan: string[];
  time_to_value_score: number;
}

interface Summary {
  total: number;
  risk_counts: Record<string, number>;
  action_counts: Record<string, number>;
  phase_counts: Record<string, number>;
  avg_risk_score: number;
  avg_time_to_value: number;
  critical_count: number;
  behind_schedule_count: number;
  total_arr_at_risk_eur: number;
}

// ─── Helpers ──────────────────────────────────────────────────────────────────

const RISK_META: Record<OnboardingRisk, { label: string; ring: string; bg: string; badge: string }> = {
  low:      { label: "Faible",   ring: "#34d399", bg: "bg-emerald-900/30", badge: "bg-emerald-500/20 text-emerald-300 border-emerald-700" },
  moderate: { label: "Modéré",   ring: "#38bdf8", bg: "bg-sky-900/30",     badge: "bg-sky-500/20 text-sky-300 border-sky-700" },
  high:     { label: "Élevé",    ring: "#fbbf24", bg: "bg-amber-900/30",   badge: "bg-amber-500/20 text-amber-300 border-amber-700" },
  critical: { label: "Critique", ring: "#f87171", bg: "bg-red-900/30",     badge: "bg-red-500/20 text-red-300 border-red-700" },
};

const ACTION_META: Record<OnboardingAction, { label: string; color: string }> = {
  monitor:    { label: "Surveiller", color: "text-emerald-400" },
  accelerate: { label: "Accélérer",  color: "text-sky-400" },
  rescue:     { label: "Rescue",     color: "text-amber-400" },
  escalate:   { label: "Escalader",  color: "text-red-400" },
};

const PHASE_META: Record<OnboardingPhase, { label: string; step: number }> = {
  kickoff:          { label: "Kickoff",          step: 1 },
  setup:            { label: "Setup",            step: 2 },
  training:         { label: "Formation",        step: 3 },
  adoption:         { label: "Adoption",         step: 4 },
  value_realization: { label: "Valeur",          step: 5 },
};

const CHURN_META: Record<ChurnSignal, { label: string; color: string }> = {
  none:     { label: "Aucun",   color: "text-emerald-400" },
  early:    { label: "Léger",   color: "text-sky-400" },
  moderate: { label: "Modéré",  color: "text-amber-400" },
  strong:   { label: "Fort",    color: "text-red-400" },
};

function fmt(n: number): string {
  if (n >= 1_000_000) return `€${(n / 1_000_000).toFixed(1)}M`;
  if (n >= 1_000) return `€${(n / 1_000).toFixed(0)}k`;
  return `€${n}`;
}

// ─── Phase Progress Bar ───────────────────────────────────────────────────────

function PhaseBar({ phase }: { phase: OnboardingPhase }) {
  const phases: OnboardingPhase[] = ["kickoff", "setup", "training", "adoption", "value_realization"];
  const current = PHASE_META[phase].step;
  return (
    <div className="flex gap-0.5 mt-2">
      {phases.map((p, i) => (
        <div
          key={p}
          className={`h-1.5 flex-1 rounded-full transition-colors ${
            i + 1 <= current
              ? "bg-indigo-500"
              : "bg-slate-700"
          }`}
          title={PHASE_META[p].label}
        />
      ))}
    </div>
  );
}

// ─── RiskRing ─────────────────────────────────────────────────────────────────

function RiskRing({ score, level }: { score: number; level: OnboardingRisk }) {
  const r = 38;
  const circ = 2 * Math.PI * r;
  const arc = (score / 100) * circ;
  const color = RISK_META[level].ring;

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
        risque
      </text>
    </svg>
  );
}

// ─── CustomerCard ─────────────────────────────────────────────────────────────

function CustomerCard({ customer, onClick }: { customer: Customer; onClick: () => void }) {
  const rm = RISK_META[customer.risk_level];
  const am = ACTION_META[customer.risk_action];
  const cm = CHURN_META[customer.churn_signal];
  const pm = PHASE_META[customer.phase];

  return (
    <button
      onClick={onClick}
      className={`w-full text-left rounded-xl border border-slate-800 ${rm.bg} p-4 hover:border-slate-600 transition-colors`}
    >
      <div className="flex items-start gap-4">
        <RiskRing score={customer.risk_score} level={customer.risk_level} />
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 flex-wrap mb-1">
            <span className={`text-xs font-bold px-2 py-0.5 rounded border ${rm.badge}`}>{rm.label}</span>
            <span className="text-xs text-slate-400">{pm.label}</span>
            {customer.go_live_delay_days > 0 && (
              <span className="text-xs text-red-400">+{customer.go_live_delay_days}j retard</span>
            )}
          </div>
          <h3 className="text-white font-semibold text-sm truncate">{customer.customer_name}</h3>
          <p className="text-slate-400 text-xs mt-0.5 capitalize">{customer.segment.replace("_", " ")} · ARR {fmt(customer.arr_eur)}</p>

          <PhaseBar phase={customer.phase} />

          <div className="mt-2 grid grid-cols-3 gap-2 text-xs">
            <div>
              <span className="text-slate-500 block">Action</span>
              <span className={`font-semibold ${am.color}`}>{am.label}</span>
            </div>
            <div>
              <span className="text-slate-500 block">Signal Churn</span>
              <span className={`font-semibold ${cm.color}`}>{cm.label}</span>
            </div>
            <div>
              <span className="text-slate-500 block">Time-to-Value</span>
              <span className="text-white font-semibold">{customer.time_to_value_score}/100</span>
            </div>
          </div>

          {customer.risk_factors.length > 0 && (
            <p className="mt-2 text-xs text-amber-300/80 truncate">⚠ {customer.risk_factors[0]}</p>
          )}
        </div>
      </div>
    </button>
  );
}

// ─── CustomerModal ────────────────────────────────────────────────────────────

function CustomerModal({ customer, onClose }: { customer: Customer; onClose: () => void }) {
  const [tab, setTab] = useState<"risques" | "positifs" | "plan">("risques");
  const overlayRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const fn = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", fn);
    return () => window.removeEventListener("keydown", fn);
  }, [onClose]);

  const rm = RISK_META[customer.risk_level];
  const am = ACTION_META[customer.risk_action];
  const cm = CHURN_META[customer.churn_signal];

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
            <RiskRing score={customer.risk_score} level={customer.risk_level} />
            <div>
              <h2 className="text-white font-bold text-lg">{customer.customer_name}</h2>
              <p className="text-slate-400 text-sm capitalize">
                {customer.segment.replace("_", " ")} · ARR {fmt(customer.arr_eur)}
              </p>
              <div className="flex gap-2 mt-1 flex-wrap">
                <span className={`text-xs font-bold px-2 py-0.5 rounded border ${rm.badge}`}>{rm.label}</span>
                <span className="text-xs text-slate-400">{PHASE_META[customer.phase].label}</span>
                {customer.go_live_delay_days > 0 && (
                  <span className="text-xs text-red-400 font-semibold">+{customer.go_live_delay_days}j retard</span>
                )}
              </div>
              <PhaseBar phase={customer.phase} />
            </div>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl leading-none p-1">×</button>
        </div>

        {/* KPIs */}
        <div className="grid grid-cols-4 gap-0 divide-x divide-slate-800 border-b border-slate-800">
          {[
            { label: "Action",       value: am.label, color: am.color },
            { label: "Signal Churn", value: cm.label, color: cm.color },
            { label: "Time-to-Value", value: `${customer.time_to_value_score}/100`, color: "text-white" },
            { label: "Facteurs risque", value: customer.risk_factors.length.toString(), color: customer.risk_factors.length > 0 ? "text-red-400" : "text-emerald-400" },
          ].map((k) => (
            <div key={k.label} className="px-4 py-3 text-center">
              <p className="text-xs text-slate-500">{k.label}</p>
              <p className={`text-sm font-bold ${k.color}`}>{k.value}</p>
            </div>
          ))}
        </div>

        {/* Tabs */}
        <div className="flex border-b border-slate-800">
          {(["risques", "positifs", "plan"] as const).map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`flex-1 py-2.5 text-xs font-semibold uppercase tracking-wide transition-colors ${
                tab === t ? "text-indigo-400 border-b-2 border-indigo-400" : "text-slate-500 hover:text-slate-300"
              }`}
            >
              {t === "risques" ? "Facteurs Risque" : t === "positifs" ? "Signaux Positifs" : "Plan d'Intervention"}
            </button>
          ))}
        </div>

        {/* Tab content */}
        <div className="p-5 space-y-2">
          {tab === "risques" && (
            customer.risk_factors.length > 0 ? (
              customer.risk_factors.map((f, i) => (
                <div key={i} className="flex gap-2 text-sm">
                  <span className="text-red-400 mt-0.5 flex-shrink-0">⚠</span>
                  <span className="text-slate-300">{f}</span>
                </div>
              ))
            ) : (
              <p className="text-slate-500 text-sm italic">Aucun facteur de risque. Onboarding en bonne santé.</p>
            )
          )}
          {tab === "positifs" && (
            customer.positive_signals.length > 0 ? (
              customer.positive_signals.map((s, i) => (
                <div key={i} className="flex gap-2 text-sm">
                  <span className="text-emerald-400 mt-0.5 flex-shrink-0">✓</span>
                  <span className="text-slate-300">{s}</span>
                </div>
              ))
            ) : (
              <p className="text-slate-500 text-sm italic">Aucun signal positif identifié.</p>
            )
          )}
          {tab === "plan" && (
            customer.intervention_plan.map((p, i) => (
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

export default function OnboardingRiskMonitorPage() {
  const [customers, setCustomers] = useState<Customer[]>([]);
  const [summary, setSummary] = useState<Summary | null>(null);
  const [loading, setLoading] = useState(true);
  const [selected, setSelected] = useState<Customer | null>(null);
  const [riskFilter, setRiskFilter] = useState<string>("all");
  const [actionFilter, setActionFilter] = useState<string>("all");

  useEffect(() => {
    async function fetchData() {
        setLoading(true);
        const params = new URLSearchParams();
        if (riskFilter !== "all") params.set("risk", riskFilter);
        if (actionFilter !== "all") params.set("action", actionFilter);
        const res = await fetch(`/api/onboarding-risk-monitor?${params}`);
        const data = await res.json();
        setCustomers(data.customers ?? []);
        setSummary(data.summary ?? null);
        setLoading(false);
  }
    fetchData();
  }, [riskFilter, actionFilter]);

  const riskLevels: OnboardingRisk[] = ["low", "moderate", "high", "critical"];
  const actions: OnboardingAction[] = ["monitor", "accelerate", "rescue", "escalate"];

  function fmtCur(n: number) {
    if (n >= 1_000_000) return `€${(n / 1_000_000).toFixed(1)}M`;
    if (n >= 1_000) return `€${(n / 1_000).toFixed(0)}k`;
    return `€${n}`;
  }

  const kpis = summary
    ? [
        { label: "Clients en onboarding",  value: summary.total.toString(),                       sub: "portefeuille actif" },
        { label: "Critiques",              value: summary.critical_count.toString(),               sub: "action urgente" },
        { label: "En retard",              value: summary.behind_schedule_count.toString(),        sub: "go-live dépassé" },
        { label: "Score risque moyen",     value: `${summary.avg_risk_score}/100`,                 sub: "portfolio onboarding" },
        { label: "Time-to-Value moyen",    value: `${summary.avg_time_to_value}/100`,              sub: "adoption produit" },
        { label: "ARR à risque",           value: fmtCur(summary.total_arr_at_risk_eur),          sub: "high + critical" },
      ]
    : [];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
      {selected && <CustomerModal customer={selected} onClose={() => setSelected(null)} />}

      {/* Header */}
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-white">Onboarding Risk Monitor</h1>
        <p className="text-slate-400 text-sm mt-1">Surveillance des risques d'onboarding — détection précoce des dérives et protection du Time-to-Value</p>
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

      {/* Risk distribution */}
      {summary && (
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 mb-6">
          <p className="text-xs text-slate-500 mb-3 font-semibold uppercase tracking-wide">Distribution par niveau de risque onboarding</p>
          <div className="flex h-3 rounded-full overflow-hidden gap-0.5">
            {riskLevels.map((l) => {
              const count = summary.risk_counts[l] ?? 0;
              const pct = summary.total > 0 ? (count / summary.total) * 100 : 0;
              const colors: Record<string, string> = {
                low: "bg-emerald-500", moderate: "bg-sky-500",
                high: "bg-amber-500", critical: "bg-red-500",
              };
              return pct > 0 ? (
                <div key={l} className={`${colors[l]} rounded-sm`} style={{ width: `${pct}%` }} title={`${RISK_META[l].label}: ${count}`} />
              ) : null;
            })}
          </div>
          <div className="flex gap-4 mt-2 flex-wrap">
            {riskLevels.map((l) => (
              <div key={l} className="flex items-center gap-1.5 text-xs text-slate-400">
                <span className={`w-2 h-2 rounded-full ${l === "low" ? "bg-emerald-500" : l === "moderate" ? "bg-sky-500" : l === "high" ? "bg-amber-500" : "bg-red-500"}`} />
                {RISK_META[l].label}: {summary.risk_counts[l] ?? 0}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Filters */}
      <div className="flex flex-col sm:flex-row gap-3 mb-6">
        <div className="flex gap-1 flex-wrap">
          {["all", ...riskLevels].map((l) => (
            <button
              key={l}
              onClick={() => setRiskFilter(l)}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-colors ${
                riskFilter === l
                  ? "bg-indigo-600 text-white"
                  : "bg-slate-800 text-slate-400 hover:text-white"
              }`}
            >
              {l === "all" ? "Tous les risques" : RISK_META[l as OnboardingRisk].label}
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
              {a === "all" ? "Toutes actions" : ACTION_META[a as OnboardingAction].label}
            </button>
          ))}
        </div>
      </div>

      {/* Customer grid */}
      {loading ? (
        <div className="text-center text-slate-500 py-20">Chargement…</div>
      ) : customers.length === 0 ? (
        <div className="text-center text-slate-500 py-20">Aucun client pour ces filtres.</div>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
          {customers.map((c) => (
            <CustomerCard key={c.customer_id} customer={c} onClick={() => setSelected(c)} />
          ))}
        </div>
      )}
    </div>
  );
}
