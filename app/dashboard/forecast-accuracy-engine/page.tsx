"use client";

import { useState, useEffect, useRef, useCallback } from "react";

// ─── Types ────────────────────────────────────────────────────────────────────

type ForecastAccuracy = "excellent" | "good" | "fair" | "poor";
type ForecastBias = "optimistic" | "neutral" | "pessimistic";
type ForecastAction = "celebrate" | "calibrate" | "improve" | "overhaul";
type RepTier = "top" | "solid" | "developing" | "struggling";

interface Rep {
  rep_id: string;
  rep_name: string;
  region: string;
  segment: string;
  accuracy_pct: number;
  accuracy_tier: ForecastAccuracy;
  bias: ForecastBias;
  forecast_action: ForecastAction;
  rep_tier: RepTier;
  attainment_pct: number;
  variance_eur: number;
  accuracy_drivers: string[];
  accuracy_gaps: string[];
  coaching_recommendations: string[];
  reliability_score: number;
}

interface Summary {
  total: number;
  accuracy_counts: Record<string, number>;
  action_counts: Record<string, number>;
  bias_counts: Record<string, number>;
  avg_accuracy_pct: number;
  avg_attainment_pct: number;
  excellent_count: number;
  overhaul_count: number;
  total_variance_eur: number;
}

// ─── Helpers ──────────────────────────────────────────────────────────────────

const ACCURACY_META: Record<ForecastAccuracy, { label: string; ring: string; bg: string; badge: string }> = {
  excellent: { label: "Excellent",   ring: "#34d399", bg: "bg-emerald-900/30", badge: "bg-emerald-500/20 text-emerald-300 border-emerald-700" },
  good:      { label: "Bon",         ring: "#38bdf8", bg: "bg-sky-900/30",     badge: "bg-sky-500/20 text-sky-300 border-sky-700" },
  fair:      { label: "Passable",    ring: "#fbbf24", bg: "bg-amber-900/30",   badge: "bg-amber-500/20 text-amber-300 border-amber-700" },
  poor:      { label: "Insuffisant", ring: "#f87171", bg: "bg-red-900/30",     badge: "bg-red-500/20 text-red-300 border-red-700" },
};

const ACTION_META: Record<ForecastAction, { label: string; color: string }> = {
  celebrate: { label: "Célébrer",   color: "text-emerald-400" },
  calibrate: { label: "Calibrer",   color: "text-sky-400" },
  improve:   { label: "Améliorer",  color: "text-amber-400" },
  overhaul:  { label: "Révision",   color: "text-red-400" },
};

const BIAS_META: Record<ForecastBias, { label: string; color: string; icon: string }> = {
  optimistic:  { label: "Optimiste",  color: "text-orange-400", icon: "↑" },
  neutral:     { label: "Neutre",     color: "text-slate-300",  icon: "→" },
  pessimistic: { label: "Pessimiste", color: "text-violet-400", icon: "↓" },
};

const REP_TIER_META: Record<RepTier, { label: string; color: string }> = {
  top:        { label: "Top",         color: "text-emerald-400" },
  solid:      { label: "Solide",      color: "text-sky-400" },
  developing: { label: "En progrès",  color: "text-amber-400" },
  struggling: { label: "En difficulté", color: "text-red-400" },
};

function fmtEur(n: number): string {
  const abs = Math.abs(n);
  const prefix = n < 0 ? "-" : "+";
  if (abs >= 1_000_000) return `${prefix}€${(abs / 1_000_000).toFixed(1)}M`;
  if (abs >= 1_000) return `${prefix}€${(abs / 1_000).toFixed(0)}k`;
  return `${prefix}€${abs}`;
}

// ─── AccuracyRing ─────────────────────────────────────────────────────────────

function AccuracyRing({ score, tier }: { score: number; tier: ForecastAccuracy }) {
  const r = 38;
  const circ = 2 * Math.PI * r;
  const arc = (score / 100) * circ;
  const color = ACCURACY_META[tier].ring;

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
      <text x="48" y="44" textAnchor="middle" fill={color} fontSize="16" fontWeight="700" fontFamily="sans-serif">
        {score}%
      </text>
      <text x="48" y="60" textAnchor="middle" fill="#94a3b8" fontSize="9" fontFamily="sans-serif">
        précision
      </text>
    </svg>
  );
}

// ─── RepCard ──────────────────────────────────────────────────────────────────

function RepCard({ rep, onClick }: { rep: Rep; onClick: () => void }) {
  const am = ACCURACY_META[rep.accuracy_tier];
  const acm = ACTION_META[rep.forecast_action];
  const bm = BIAS_META[rep.bias];
  const rtm = REP_TIER_META[rep.rep_tier];

  return (
    <button
      onClick={onClick}
      className={`w-full text-left rounded-xl border border-slate-800 ${am.bg} p-4 hover:border-slate-600 transition-colors`}
    >
      <div className="flex items-start gap-4">
        <AccuracyRing score={rep.accuracy_pct} tier={rep.accuracy_tier} />
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 flex-wrap mb-1">
            <span className={`text-xs font-bold px-2 py-0.5 rounded border ${am.badge}`}>{am.label}</span>
            <span className="text-xs text-slate-400">{rep.region}</span>
          </div>
          <h3 className="text-white font-semibold text-sm">{rep.rep_name}</h3>
          <p className="text-slate-400 text-xs mt-0.5 capitalize">{rep.segment.replace("_", " ")}</p>

          <div className="mt-2 grid grid-cols-4 gap-2 text-xs">
            <div>
              <span className="text-slate-500 block">Attainment</span>
              <span className={`font-semibold ${rep.attainment_pct >= 100 ? "text-emerald-400" : rep.attainment_pct >= 75 ? "text-sky-400" : "text-red-400"}`}>
                {rep.attainment_pct}%
              </span>
            </div>
            <div>
              <span className="text-slate-500 block">Variance</span>
              <span className={`font-semibold ${rep.variance_eur >= 0 ? "text-emerald-400" : "text-red-400"}`}>
                {fmtEur(rep.variance_eur)}
              </span>
            </div>
            <div>
              <span className="text-slate-500 block">Biais</span>
              <span className={`font-semibold ${bm.color}`}>{bm.icon} {bm.label}</span>
            </div>
            <div>
              <span className="text-slate-500 block">Action</span>
              <span className={`font-semibold ${acm.color}`}>{acm.label}</span>
            </div>
          </div>

          {rep.accuracy_gaps.length > 0 && (
            <p className="mt-2 text-xs text-amber-300/80 truncate">⚠ {rep.accuracy_gaps[0]}</p>
          )}
        </div>
      </div>
    </button>
  );
}

// ─── RepModal ─────────────────────────────────────────────────────────────────

function RepModal({ rep, onClose }: { rep: Rep; onClose: () => void }) {
  const [tab, setTab] = useState<"drivers" | "gaps" | "coaching">("drivers");
  const overlayRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const fn = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", fn);
    return () => window.removeEventListener("keydown", fn);
  }, [onClose]);

  const am = ACCURACY_META[rep.accuracy_tier];
  const bm = BIAS_META[rep.bias];
  const acm = ACTION_META[rep.forecast_action];
  const rtm = REP_TIER_META[rep.rep_tier];

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
            <AccuracyRing score={rep.accuracy_pct} tier={rep.accuracy_tier} />
            <div>
              <h2 className="text-white font-bold text-lg">{rep.rep_name}</h2>
              <p className="text-slate-400 text-sm">{rep.region} · {rep.segment.replace("_", " ")}</p>
              <div className="flex gap-2 mt-1 flex-wrap">
                <span className={`text-xs font-bold px-2 py-0.5 rounded border ${am.badge}`}>{am.label}</span>
                <span className={`text-xs font-semibold ${rtm.color}`}>{rtm.label}</span>
              </div>
            </div>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl leading-none p-1">×</button>
        </div>

        {/* KPIs */}
        <div className="grid grid-cols-4 gap-0 divide-x divide-slate-800 border-b border-slate-800">
          {[
            { label: "Attainment",   value: `${rep.attainment_pct}%`, color: rep.attainment_pct >= 100 ? "text-emerald-400" : "text-amber-400" },
            { label: "Variance",     value: fmtEur(rep.variance_eur), color: rep.variance_eur >= 0 ? "text-emerald-400" : "text-red-400" },
            { label: "Biais",        value: `${bm.icon} ${bm.label}`, color: bm.color },
            { label: "Fiabilité",    value: `${rep.reliability_score}/100`, color: "text-white" },
          ].map((k) => (
            <div key={k.label} className="px-4 py-3 text-center">
              <p className="text-xs text-slate-500">{k.label}</p>
              <p className={`text-sm font-bold ${k.color}`}>{k.value}</p>
            </div>
          ))}
        </div>

        {/* Tabs */}
        <div className="flex border-b border-slate-800">
          {(["drivers", "gaps", "coaching"] as const).map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`flex-1 py-2.5 text-xs font-semibold uppercase tracking-wide transition-colors ${
                tab === t ? "text-indigo-400 border-b-2 border-indigo-400" : "text-slate-500 hover:text-slate-300"
              }`}
            >
              {t === "drivers" ? "Points Forts" : t === "gaps" ? "Lacunes" : "Coaching"}
            </button>
          ))}
        </div>

        {/* Tab content */}
        <div className="p-5 space-y-2">
          {tab === "drivers" && (
            rep.accuracy_drivers.length > 0 ? (
              rep.accuracy_drivers.map((d, i) => (
                <div key={i} className="flex gap-2 text-sm">
                  <span className="text-emerald-400 mt-0.5 flex-shrink-0">✓</span>
                  <span className="text-slate-300">{d}</span>
                </div>
              ))
            ) : (
              <p className="text-slate-500 text-sm italic">Aucun signal positif identifié.</p>
            )
          )}
          {tab === "gaps" && (
            rep.accuracy_gaps.length > 0 ? (
              rep.accuracy_gaps.map((g, i) => (
                <div key={i} className="flex gap-2 text-sm">
                  <span className="text-red-400 mt-0.5 flex-shrink-0">✗</span>
                  <span className="text-slate-300">{g}</span>
                </div>
              ))
            ) : (
              <p className="text-slate-500 text-sm italic">Aucune lacune identifiée — forecast propre.</p>
            )
          )}
          {tab === "coaching" && (
            rep.coaching_recommendations.map((r, i) => (
              <div key={i} className="flex gap-2 text-sm">
                <span className="text-indigo-400 mt-0.5 flex-shrink-0">→</span>
                <span className="text-slate-300">{r}</span>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}

// ─── Page ─────────────────────────────────────────────────────────────────────

export default function ForecastAccuracyEnginePage() {
  const [reps, setReps] = useState<Rep[]>([]);
  const [summary, setSummary] = useState<Summary | null>(null);
  const [loading, setLoading] = useState(true);
  const [selected, setSelected] = useState<Rep | null>(null);
  const [accuracyFilter, setAccuracyFilter] = useState<string>("all");
  const [actionFilter, setActionFilter] = useState<string>("all");

  const fetchData = useCallback(async () => {
    setLoading(true);
    const params = new URLSearchParams();
    if (accuracyFilter !== "all") params.set("accuracy", accuracyFilter);
    if (actionFilter !== "all") params.set("action", actionFilter);
    const res = await fetch(`/api/forecast-accuracy-engine?${params}`);
    const data = await res.json();
    setReps(data.reps ?? []);
    setSummary(data.summary ?? null);
    setLoading(false);
  }, [accuracyFilter, actionFilter]);

  useEffect(() => { fetchData(); }, [fetchData]);

  const accuracyTiers: ForecastAccuracy[] = ["excellent", "good", "fair", "poor"];
  const actions: ForecastAction[] = ["celebrate", "calibrate", "improve", "overhaul"];

  const kpis = summary
    ? [
        { label: "Reps analysés",        value: summary.total.toString(),              sub: "équipe complète" },
        { label: "Forecasters excellents", value: summary.excellent_count.toString(),   sub: "précision ≥ 90%" },
        { label: "Nécessitent révision",  value: summary.overhaul_count.toString(),     sub: "action urgente" },
        { label: "Précision moyenne",     value: `${summary.avg_accuracy_pct}%`,        sub: "team forecast" },
        { label: "Attainment moyen",      value: `${summary.avg_attainment_pct}%`,      sub: "quota réalisé" },
        { label: "Variance totale",       value: `${fmtEur(summary.total_variance_eur)}`, sub: "actual vs. committed" },
      ]
    : [];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
      {selected && <RepModal rep={selected} onClose={() => setSelected(null)} />}

      {/* Header */}
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-white">Forecast Accuracy Engine</h1>
        <p className="text-slate-400 text-sm mt-1">Analyse de précision des prévisions commerciales — détection des biais et coaching ciblé</p>
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

      {/* Accuracy distribution bar */}
      {summary && (
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 mb-6">
          <p className="text-xs text-slate-500 mb-3 font-semibold uppercase tracking-wide">Distribution de précision forecast</p>
          <div className="flex h-3 rounded-full overflow-hidden gap-0.5">
            {accuracyTiers.map((t) => {
              const count = summary.accuracy_counts[t] ?? 0;
              const pct = summary.total > 0 ? (count / summary.total) * 100 : 0;
              const colors: Record<string, string> = {
                excellent: "bg-emerald-500", good: "bg-sky-500",
                fair: "bg-amber-500", poor: "bg-red-500",
              };
              return pct > 0 ? (
                <div key={t} className={`${colors[t]} rounded-sm`} style={{ width: `${pct}%` }} title={`${ACCURACY_META[t].label}: ${count}`} />
              ) : null;
            })}
          </div>
          <div className="flex gap-4 mt-2 flex-wrap">
            {accuracyTiers.map((t) => (
              <div key={t} className="flex items-center gap-1.5 text-xs text-slate-400">
                <span className={`w-2 h-2 rounded-full ${t === "excellent" ? "bg-emerald-500" : t === "good" ? "bg-sky-500" : t === "fair" ? "bg-amber-500" : "bg-red-500"}`} />
                {ACCURACY_META[t].label}: {summary.accuracy_counts[t] ?? 0}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Filters */}
      <div className="flex flex-col sm:flex-row gap-3 mb-6">
        <div className="flex gap-1 flex-wrap">
          {["all", ...accuracyTiers].map((t) => (
            <button
              key={t}
              onClick={() => setAccuracyFilter(t)}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-colors ${
                accuracyFilter === t
                  ? "bg-indigo-600 text-white"
                  : "bg-slate-800 text-slate-400 hover:text-white"
              }`}
            >
              {t === "all" ? "Toutes précisions" : ACCURACY_META[t as ForecastAccuracy].label}
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
              {a === "all" ? "Toutes actions" : ACTION_META[a as ForecastAction].label}
            </button>
          ))}
        </div>
      </div>

      {/* Reps grid */}
      {loading ? (
        <div className="text-center text-slate-500 py-20">Chargement…</div>
      ) : reps.length === 0 ? (
        <div className="text-center text-slate-500 py-20">Aucun rep pour ces filtres.</div>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
          {reps.map((r) => (
            <RepCard key={r.rep_id} rep={r} onClick={() => setSelected(r)} />
          ))}
        </div>
      )}
    </div>
  );
}
