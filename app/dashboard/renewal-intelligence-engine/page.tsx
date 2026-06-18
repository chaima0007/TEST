"use client";

import { useState, useEffect, useRef, useCallback } from "react";

// ─── Types ────────────────────────────────────────────────────────────────────

type RenewalRisk = "low" | "moderate" | "high" | "critical";
type RenewalAction = "close" | "nurture" | "intervene" | "escalate";
type RenewalOutcome = "renew" | "expand" | "downgrade" | "churn";
type EngagementTrend = "growing" | "stable" | "declining" | "dormant";

interface Renewal {
  customer_id: string;
  customer_name: string;
  arr_eur: number;
  segment: string;
  days_to_renewal: number;
  renewal_risk: RenewalRisk;
  renewal_action: RenewalAction;
  predicted_outcome: RenewalOutcome;
  engagement_trend: EngagementTrend;
  renewal_probability_pct: number;
  expected_arr_change_pct: number;
  risk_signals: string[];
  positive_signals: string[];
  renewal_plays: string[];
  urgency_score: number;
}

interface Summary {
  total: number;
  risk_counts: Record<string, number>;
  action_counts: Record<string, number>;
  outcome_counts: Record<string, number>;
  avg_renewal_probability_pct: number;
  critical_count: number;
  escalation_count: number;
  total_arr_at_risk_eur: number;
  expected_arr_delta_eur: number;
}

// ─── Helpers ──────────────────────────────────────────────────────────────────

const RISK_META: Record<RenewalRisk, { label: string; ring: string; bg: string; badge: string }> = {
  low:      { label: "Faible",   ring: "#34d399", bg: "bg-emerald-900/30", badge: "bg-emerald-500/20 text-emerald-300 border-emerald-700" },
  moderate: { label: "Modéré",   ring: "#38bdf8", bg: "bg-sky-900/30",     badge: "bg-sky-500/20 text-sky-300 border-sky-700" },
  high:     { label: "Élevé",    ring: "#fbbf24", bg: "bg-amber-900/30",   badge: "bg-amber-500/20 text-amber-300 border-amber-700" },
  critical: { label: "Critique", ring: "#f87171", bg: "bg-red-900/30",     badge: "bg-red-500/20 text-red-300 border-red-700" },
};

const ACTION_META: Record<RenewalAction, { label: string; color: string }> = {
  close:     { label: "Closer",     color: "text-emerald-400" },
  nurture:   { label: "Nurturer",   color: "text-sky-400" },
  intervene: { label: "Intervenir", color: "text-amber-400" },
  escalate:  { label: "Escalader",  color: "text-red-400" },
};

const OUTCOME_META: Record<RenewalOutcome, { label: string; color: string; icon: string }> = {
  renew:     { label: "Renouvellement", color: "text-sky-400",     icon: "↺" },
  expand:    { label: "Expansion",      color: "text-emerald-400", icon: "↑" },
  downgrade: { label: "Downgrade",      color: "text-amber-400",   icon: "↓" },
  churn:     { label: "Churn",          color: "text-red-400",     icon: "✗" },
};

const TREND_META: Record<EngagementTrend, { label: string; color: string }> = {
  growing:  { label: "Croissant",  color: "text-emerald-400" },
  stable:   { label: "Stable",     color: "text-sky-400" },
  declining: { label: "Déclinant", color: "text-amber-400" },
  dormant:  { label: "Dormant",    color: "text-red-400" },
};

function fmt(n: number): string {
  const abs = Math.abs(n);
  const prefix = n < 0 ? "-€" : "€";
  if (abs >= 1_000_000) return `${prefix}${(abs / 1_000_000).toFixed(1)}M`;
  if (abs >= 1_000) return `${prefix}${(abs / 1_000).toFixed(0)}k`;
  return `${prefix}${abs}`;
}

function fmtChange(pct: number): string {
  if (pct === -100) return "Churn total";
  if (pct > 0) return `+${pct}%`;
  return `${pct}%`;
}

// ─── UrgencyRing ──────────────────────────────────────────────────────────────

function UrgencyRing({ score, risk }: { score: number; risk: RenewalRisk }) {
  const r = 38;
  const circ = 2 * Math.PI * r;
  const arc = (score / 100) * circ;
  const color = RISK_META[risk].ring;

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
        urgence
      </text>
    </svg>
  );
}

// ─── RenewalCard ──────────────────────────────────────────────────────────────

function RenewalCard({ renewal, onClick }: { renewal: Renewal; onClick: () => void }) {
  const rm = RISK_META[renewal.renewal_risk];
  const am = ACTION_META[renewal.renewal_action];
  const om = OUTCOME_META[renewal.predicted_outcome];
  const tm = TREND_META[renewal.engagement_trend];

  return (
    <button
      onClick={onClick}
      className={`w-full text-left rounded-xl border border-slate-800 ${rm.bg} p-4 hover:border-slate-600 transition-colors`}
    >
      <div className="flex items-start gap-4">
        <UrgencyRing score={renewal.urgency_score} risk={renewal.renewal_risk} />
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 flex-wrap mb-1">
            <span className={`text-xs font-bold px-2 py-0.5 rounded border ${rm.badge}`}>{rm.label}</span>
            <span className="text-xs text-slate-400 capitalize">{renewal.segment.replace("_", " ")}</span>
            <span className={`text-xs font-semibold ${renewal.days_to_renewal <= 30 ? "text-red-400" : "text-slate-400"}`}>
              {renewal.days_to_renewal <= 0 ? `Expiré ${Math.abs(renewal.days_to_renewal)}j` : `J-${renewal.days_to_renewal}`}
            </span>
          </div>
          <h3 className="text-white font-semibold text-sm truncate">{renewal.customer_name}</h3>
          <p className="text-slate-400 text-xs mt-0.5">ARR: <span className="text-white font-medium">{fmt(renewal.arr_eur)}</span></p>

          <div className="mt-2 grid grid-cols-4 gap-1 text-xs">
            <div>
              <span className="text-slate-500 block">Probabilité</span>
              <span className={`font-semibold ${renewal.renewal_probability_pct >= 70 ? "text-emerald-400" : renewal.renewal_probability_pct >= 50 ? "text-amber-400" : "text-red-400"}`}>
                {renewal.renewal_probability_pct}%
              </span>
            </div>
            <div>
              <span className="text-slate-500 block">Résultat</span>
              <span className={`font-semibold ${om.color}`}>{om.icon} {om.label}</span>
            </div>
            <div>
              <span className="text-slate-500 block">ARR Δ</span>
              <span className={`font-semibold ${renewal.expected_arr_change_pct > 0 ? "text-emerald-400" : renewal.expected_arr_change_pct < 0 ? "text-red-400" : "text-slate-300"}`}>
                {fmtChange(renewal.expected_arr_change_pct)}
              </span>
            </div>
            <div>
              <span className="text-slate-500 block">Action</span>
              <span className={`font-semibold ${am.color}`}>{am.label}</span>
            </div>
          </div>

          {renewal.risk_signals.length > 0 && (
            <p className="mt-2 text-xs text-amber-300/80 truncate">⚠ {renewal.risk_signals[0]}</p>
          )}
        </div>
      </div>
    </button>
  );
}

// ─── RenewalModal ─────────────────────────────────────────────────────────────

function RenewalModal({ renewal, onClose }: { renewal: Renewal; onClose: () => void }) {
  const [tab, setTab] = useState<"risques" | "positifs" | "plays">("risques");
  const overlayRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const fn = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", fn);
    return () => window.removeEventListener("keydown", fn);
  }, [onClose]);

  const rm = RISK_META[renewal.renewal_risk];
  const am = ACTION_META[renewal.renewal_action];
  const om = OUTCOME_META[renewal.predicted_outcome];
  const tm = TREND_META[renewal.engagement_trend];

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
            <UrgencyRing score={renewal.urgency_score} risk={renewal.renewal_risk} />
            <div>
              <h2 className="text-white font-bold text-lg">{renewal.customer_name}</h2>
              <p className="text-slate-400 text-sm capitalize">
                {renewal.segment.replace("_", " ")} · ARR {fmt(renewal.arr_eur)}
              </p>
              <div className="flex gap-2 mt-1 flex-wrap">
                <span className={`text-xs font-bold px-2 py-0.5 rounded border ${rm.badge}`}>{rm.label}</span>
                <span className={`text-xs font-semibold ${renewal.days_to_renewal <= 30 ? "text-red-400" : "text-slate-400"}`}>
                  {renewal.days_to_renewal <= 0 ? `Expiré ${Math.abs(renewal.days_to_renewal)}j` : `J-${renewal.days_to_renewal}`}
                </span>
                <span className={`text-xs font-semibold ${tm.color}`}>{tm.label}</span>
              </div>
            </div>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl leading-none p-1">×</button>
        </div>

        {/* KPIs */}
        <div className="grid grid-cols-4 gap-0 divide-x divide-slate-800 border-b border-slate-800">
          {[
            { label: "Probabilité",   value: `${renewal.renewal_probability_pct}%`, color: renewal.renewal_probability_pct >= 70 ? "text-emerald-400" : renewal.renewal_probability_pct >= 50 ? "text-amber-400" : "text-red-400" },
            { label: "Résultat",      value: `${om.icon} ${om.label}`, color: om.color },
            { label: "ARR Delta",     value: fmtChange(renewal.expected_arr_change_pct), color: renewal.expected_arr_change_pct > 0 ? "text-emerald-400" : renewal.expected_arr_change_pct < 0 ? "text-red-400" : "text-slate-300" },
            { label: "Action",        value: am.label, color: am.color },
          ].map((k) => (
            <div key={k.label} className="px-4 py-3 text-center">
              <p className="text-xs text-slate-500">{k.label}</p>
              <p className={`text-sm font-bold ${k.color}`}>{k.value}</p>
            </div>
          ))}
        </div>

        {/* Tabs */}
        <div className="flex border-b border-slate-800">
          {(["risques", "positifs", "plays"] as const).map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`flex-1 py-2.5 text-xs font-semibold uppercase tracking-wide transition-colors ${
                tab === t ? "text-indigo-400 border-b-2 border-indigo-400" : "text-slate-500 hover:text-slate-300"
              }`}
            >
              {t === "risques" ? "Signaux Risque" : t === "positifs" ? "Signaux Positifs" : "Renewal Plays"}
            </button>
          ))}
        </div>

        {/* Tab content */}
        <div className="p-5 space-y-2">
          {tab === "risques" && (
            renewal.risk_signals.length > 0 ? (
              renewal.risk_signals.map((s, i) => (
                <div key={i} className="flex gap-2 text-sm">
                  <span className="text-red-400 mt-0.5 flex-shrink-0">⚠</span>
                  <span className="text-slate-300">{s}</span>
                </div>
              ))
            ) : (
              <p className="text-slate-500 text-sm italic">Aucun signal de risque. Renouvellement sécurisé.</p>
            )
          )}
          {tab === "positifs" && (
            renewal.positive_signals.length > 0 ? (
              renewal.positive_signals.map((s, i) => (
                <div key={i} className="flex gap-2 text-sm">
                  <span className="text-emerald-400 mt-0.5 flex-shrink-0">✓</span>
                  <span className="text-slate-300">{s}</span>
                </div>
              ))
            ) : (
              <p className="text-slate-500 text-sm italic">Aucun signal positif identifié.</p>
            )
          )}
          {tab === "plays" && (
            renewal.renewal_plays.map((p, i) => (
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

export default function RenewalIntelligenceEnginePage() {
  const [renewals, setRenewals] = useState<Renewal[]>([]);
  const [summary, setSummary] = useState<Summary | null>(null);
  const [loading, setLoading] = useState(true);
  const [selected, setSelected] = useState<Renewal | null>(null);
  const [riskFilter, setRiskFilter] = useState<string>("all");
  const [actionFilter, setActionFilter] = useState<string>("all");

  const fetchData = useCallback(async () => {
    setLoading(true);
    const params = new URLSearchParams();
    if (riskFilter !== "all") params.set("risk", riskFilter);
    if (actionFilter !== "all") params.set("action", actionFilter);
    const res = await fetch(`/api/renewal-intelligence-engine?${params}`);
    const data = await res.json();
    setRenewals(data.renewals ?? []);
    setSummary(data.summary ?? null);
    setLoading(false);
  }, [riskFilter, actionFilter]);

  useEffect(() => { fetchData(); }, [fetchData]);

  const riskLevels: RenewalRisk[] = ["low", "moderate", "high", "critical"];
  const actions: RenewalAction[] = ["close", "nurture", "intervene", "escalate"];

  const kpis = summary
    ? [
        { label: "Renouvellements",    value: summary.total.toString(),                          sub: "pipeline renouvellement" },
        { label: "Critiques",          value: summary.critical_count.toString(),                  sub: "action urgente" },
        { label: "Escalades",          value: summary.escalation_count.toString(),                sub: "C-level requis" },
        { label: "Prob. moyenne",      value: `${summary.avg_renewal_probability_pct}%`,          sub: "probabilité renouvellement" },
        { label: "ARR à risque",       value: fmt(summary.total_arr_at_risk_eur),                 sub: "high + critical" },
        { label: "ARR net attendu",    value: `${summary.expected_arr_delta_eur >= 0 ? "+" : ""}${fmt(summary.expected_arr_delta_eur)}`, sub: "delta expansion/churn" },
      ]
    : [];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
      {selected && <RenewalModal renewal={selected} onClose={() => setSelected(null)} />}

      {/* Header */}
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-white">Renewal Intelligence Engine</h1>
        <p className="text-slate-400 text-sm mt-1">Intelligence de renouvellement — scoring d'urgence, prédiction d'outcome et plays de rétention</p>
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
          <p className="text-xs text-slate-500 mb-3 font-semibold uppercase tracking-wide">Distribution par risque de renouvellement</p>
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
              {l === "all" ? "Tous les risques" : RISK_META[l as RenewalRisk].label}
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
              {a === "all" ? "Toutes actions" : ACTION_META[a as RenewalAction].label}
            </button>
          ))}
        </div>
      </div>

      {/* Renewals grid */}
      {loading ? (
        <div className="text-center text-slate-500 py-20">Chargement…</div>
      ) : renewals.length === 0 ? (
        <div className="text-center text-slate-500 py-20">Aucun renouvellement pour ces filtres.</div>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
          {renewals.map((r) => (
            <RenewalCard key={r.customer_id} renewal={r} onClick={() => setSelected(r)} />
          ))}
        </div>
      )}
    </div>
  );
}
