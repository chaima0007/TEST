"use client";

import { useEffect, useState, useCallback } from "react";

interface RepData {
  rep_id: string;
  rep_name: string;
  region: string;
  segment: string;
  quota_eur: number;
  current_attainment_pct: number;
  projected_attainment_pct: number;
  projected_closed_eur: number;
  gap_to_quota_eur: number;
  attainment_outcome: string;
  confidence: string;
  quota_action: string;
  run_rate_pct: number;
  pipeline_coverage_ratio: number;
  weighted_pipeline_eur: number;
  historical_avg_attainment_pct: number;
  prediction_drivers: string[];
  prediction_risks: string[];
  action_plan: string[];
}

interface Summary {
  total: number;
  outcome_counts: Record<string, number>;
  action_counts: Record<string, number>;
  confidence_counts: Record<string, number>;
  avg_projected_attainment_pct: number;
  total_projected_closed_eur: number;
  total_gap_eur: number;
  critical_miss_count: number;
  escalation_count: number;
  overachieve_count: number;
}

interface ApiResponse {
  reps: RepData[];
  summary: Summary;
}

const OUTCOME_META: Record<string, { label: string; color: string; dot: string }> = {
  overachieve:   { label: "Sur-atteinte", color: "text-emerald-400", dot: "bg-emerald-500" },
  achieve:       { label: "Atteint",      color: "text-blue-400",    dot: "bg-blue-500" },
  slight_miss:   { label: "Léger écart",  color: "text-yellow-400",  dot: "bg-yellow-500" },
  miss:          { label: "Non-atteint",  color: "text-orange-400",  dot: "bg-orange-500" },
  critical_miss: { label: "Critique",     color: "text-red-400",     dot: "bg-red-500" },
};

const ACTION_META: Record<string, { label: string; badge: string }> = {
  maintain:     { label: "Maintenir",    badge: "bg-emerald-500/20 text-emerald-300 border-emerald-500/30" },
  accelerate:   { label: "Accélérer",   badge: "bg-blue-500/20 text-blue-300 border-blue-500/30" },
  intervention: { label: "Intervention", badge: "bg-orange-500/20 text-orange-300 border-orange-500/30" },
  escalate:     { label: "Escalade",    badge: "bg-red-500/20 text-red-300 border-red-500/30" },
};

const CONFIDENCE_META: Record<string, { label: string; color: string }> = {
  high:     { label: "Haute",     color: "text-emerald-400" },
  medium:   { label: "Moyenne",   color: "text-yellow-400" },
  low:      { label: "Faible",    color: "text-orange-400" },
  very_low: { label: "Très faible", color: "text-red-400" },
};

function fmt(n: number) {
  if (n >= 1_000_000) return `${(n / 1_000_000).toFixed(1)}M€`;
  if (n >= 1_000) return `${Math.round(n / 1_000)}K€`;
  return `${n}€`;
}

function AttainmentRing({ current, projected, size = 80 }: { current: number; projected: number; size?: number }) {
  const r = size * 0.38;
  const circ = 2 * Math.PI * r;
  const rInner = size * 0.28;
  const circInner = 2 * Math.PI * rInner;
  const arcCurrent = Math.min(1, current / 100) * circ;
  const arcProjected = Math.min(1, projected / 100) * circInner;
  const cx = size / 2;
  const projColor = projected >= 110 ? "#10b981" : projected >= 90 ? "#3b82f6" : projected >= 70 ? "#f59e0b" : projected >= 50 ? "#f97316" : "#ef4444";
  return (
    <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`}>
      <circle cx={cx} cy={cx} r={r} fill="none" stroke="#1e293b" strokeWidth={size * 0.09} />
      <circle cx={cx} cy={cx} r={r} fill="none" stroke="#4b5563"
        strokeWidth={size * 0.09}
        strokeDasharray={`${arcCurrent} ${circ - arcCurrent}`}
        strokeLinecap="round"
        transform={`rotate(-90 ${cx} ${cx})`}
      />
      <circle cx={cx} cy={cx} r={rInner} fill="none" stroke="#0f172a" strokeWidth={size * 0.09} />
      <circle cx={cx} cy={cx} r={rInner} fill="none" stroke={projColor}
        strokeWidth={size * 0.09}
        strokeDasharray={`${arcProjected} ${circInner - arcProjected}`}
        strokeLinecap="round"
        transform={`rotate(-90 ${cx} ${cx})`}
      />
      <text x={cx} y={cx + size * 0.06} textAnchor="middle" fill={projColor} fontSize={size * 0.2} fontWeight="bold">
        {projected.toFixed(0)}%
      </text>
      <text x={cx} y={cx + size * 0.2} textAnchor="middle" fill="#64748b" fontSize={size * 0.1}>
        projeté
      </text>
    </svg>
  );
}

function AttainmentModal({ rep, onClose }: { rep: RepData; onClose: () => void }) {
  const [tab, setTab] = useState<"drivers" | "risks" | "plan">("drivers");
  useEffect(() => {
    const fn = (e: KeyboardEvent) => e.key === "Escape" && onClose();
    window.addEventListener("keydown", fn);
    return () => window.removeEventListener("keydown", fn);
  }, [onClose]);
  const om = OUTCOME_META[rep.attainment_outcome] ?? OUTCOME_META.slight_miss;
  const am = ACTION_META[rep.quota_action] ?? ACTION_META.accelerate;
  const cm = CONFIDENCE_META[rep.confidence] ?? CONFIDENCE_META.medium;
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4" onClick={onClose}>
      <div className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-xl shadow-2xl" onClick={(e) => e.stopPropagation()}>
        <div className="p-6 border-b border-slate-800">
          <div className="flex items-start justify-between gap-4">
            <div>
              <h2 className="text-lg font-bold text-slate-100">{rep.rep_name}</h2>
              <p className="text-sm text-slate-400">{rep.region} · {rep.segment}</p>
              <div className="flex items-center gap-2 mt-1">
                <span className={`w-1.5 h-1.5 rounded-full ${om.dot}`} />
                <span className={`text-xs font-medium ${om.color}`}>{om.label}</span>
                <span className="text-slate-600">·</span>
                <span className={`text-xs ${cm.color}`}>Confiance: {cm.label}</span>
              </div>
            </div>
            <div className="flex items-center gap-2 flex-shrink-0">
              <span className={`text-xs font-semibold px-2 py-0.5 rounded-full border ${am.badge}`}>{am.label}</span>
              <button onClick={onClose} className="text-slate-500 hover:text-slate-300 text-xl leading-none">✕</button>
            </div>
          </div>
          <div className="mt-4 grid grid-cols-4 gap-2">
            {[
              { label: "Quota", value: fmt(rep.quota_eur), color: "text-slate-300" },
              { label: "Actuel", value: `${rep.current_attainment_pct.toFixed(0)}%`, color: "text-slate-400" },
              { label: "Projeté", value: `${rep.projected_attainment_pct.toFixed(0)}%`, color: om.color },
              { label: "Gap", value: rep.gap_to_quota_eur > 0 ? fmt(rep.gap_to_quota_eur) : "✓", color: rep.gap_to_quota_eur > 0 ? "text-red-400" : "text-emerald-400" },
            ].map((k) => (
              <div key={k.label} className="bg-slate-800/50 rounded-lg p-2 text-center">
                <p className="text-xs text-slate-500 mb-0.5">{k.label}</p>
                <p className={`text-sm font-bold ${k.color}`}>{k.value}</p>
              </div>
            ))}
          </div>
          <div className="mt-3 grid grid-cols-3 gap-2">
            {[
              { label: "Run Rate", value: `${rep.run_rate_pct.toFixed(0)}%` },
              { label: "Couverture", value: `${rep.pipeline_coverage_ratio.toFixed(1)}x` },
              { label: "Hist. Moy.", value: `${rep.historical_avg_attainment_pct.toFixed(0)}%` },
            ].map((k) => (
              <div key={k.label} className="bg-slate-800/30 rounded-lg p-2 text-center">
                <p className="text-xs text-slate-600 mb-0.5">{k.label}</p>
                <p className="text-xs font-semibold text-slate-300">{k.value}</p>
              </div>
            ))}
          </div>
        </div>
        <div className="flex border-b border-slate-800">
          {(["drivers", "risks", "plan"] as const).map((t) => (
            <button key={t} onClick={() => setTab(t)}
              className={`flex-1 py-3 text-xs font-semibold transition-colors ${tab === t ? "text-indigo-400 border-b-2 border-indigo-500" : "text-slate-500 hover:text-slate-300"}`}>
              {t === "drivers" ? "Moteurs" : t === "risks" ? "Risques" : "Plan d'Action"}
            </button>
          ))}
        </div>
        <div className="p-5 max-h-64 overflow-y-auto">
          {tab === "drivers" && (
            <ul className="space-y-2">
              {rep.prediction_drivers.length === 0
                ? <li className="text-sm text-slate-500 italic">Aucun moteur fort identifié</li>
                : rep.prediction_drivers.map((d, i) => (
                    <li key={i} className="flex items-start gap-2 text-sm text-slate-300">
                      <span className="text-emerald-400 flex-shrink-0">✓</span>{d}
                    </li>
                  ))}
            </ul>
          )}
          {tab === "risks" && (
            <ul className="space-y-2">
              {rep.prediction_risks.length === 0
                ? <li className="text-sm text-slate-500 italic">Aucun risque identifié — projection fiable</li>
                : rep.prediction_risks.map((r, i) => (
                    <li key={i} className="flex items-start gap-2 text-sm text-slate-300">
                      <span className="text-red-400 flex-shrink-0">▸</span>{r}
                    </li>
                  ))}
            </ul>
          )}
          {tab === "plan" && (
            <ul className="space-y-2">
              {rep.action_plan.map((p, i) => (
                <li key={i} className="flex items-start gap-2 text-sm text-slate-300">
                  <span className="text-indigo-400 flex-shrink-0">{i + 1}.</span>{p}
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>
    </div>
  );
}

function RepCard({ rep, onClick }: { rep: RepData; onClick: () => void }) {
  const om = OUTCOME_META[rep.attainment_outcome] ?? OUTCOME_META.slight_miss;
  const am = ACTION_META[rep.quota_action] ?? ACTION_META.accelerate;
  return (
    <div onClick={onClick} className="bg-slate-800/50 border border-slate-700/50 rounded-xl p-4 cursor-pointer hover:border-indigo-500/40 hover:bg-slate-800/80 transition-all group">
      <div className="flex items-start justify-between gap-3 mb-3">
        <div className="flex items-center gap-3">
          <AttainmentRing current={rep.current_attainment_pct} projected={rep.projected_attainment_pct} size={64} />
          <div>
            <h3 className="font-semibold text-slate-100 text-sm group-hover:text-indigo-300 transition-colors">{rep.rep_name}</h3>
            <p className="text-xs text-slate-500">{rep.region} · {rep.segment}</p>
            <div className="flex items-center gap-1.5 mt-1">
              <span className={`w-1.5 h-1.5 rounded-full ${om.dot}`} />
              <span className={`text-xs font-medium ${om.color}`}>{om.label}</span>
            </div>
          </div>
        </div>
        <span className={`text-xs font-semibold px-2 py-0.5 rounded-full border flex-shrink-0 ${am.badge}`}>{am.label}</span>
      </div>
      <div className="grid grid-cols-3 gap-2 text-center">
        <div className="bg-slate-900/50 rounded-lg p-2">
          <p className="text-xs text-slate-500 mb-0.5">Actuel</p>
          <p className="text-sm font-bold text-slate-400">{rep.current_attainment_pct.toFixed(0)}%</p>
        </div>
        <div className="bg-slate-900/50 rounded-lg p-2">
          <p className="text-xs text-slate-500 mb-0.5">Projeté</p>
          <p className={`text-sm font-bold ${om.color}`}>{rep.projected_attainment_pct.toFixed(0)}%</p>
        </div>
        <div className="bg-slate-900/50 rounded-lg p-2">
          <p className="text-xs text-slate-500 mb-0.5">Gap</p>
          <p className={`text-sm font-bold ${rep.gap_to_quota_eur > 0 ? "text-red-400" : "text-emerald-400"}`}>{rep.gap_to_quota_eur > 0 ? fmt(rep.gap_to_quota_eur) : "✓"}</p>
        </div>
      </div>
      {rep.prediction_risks.length > 0 && (
        <p className="mt-2 text-xs text-slate-500 truncate">▸ {rep.prediction_risks[0]}</p>
      )}
    </div>
  );
}

export default function QuotaAttainmentPage() {
  const [data, setData] = useState<ApiResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [selected, setSelected] = useState<RepData | null>(null);
  const [outcomeFilter, setOutcomeFilter] = useState("");
  const [actionFilter, setActionFilter] = useState("");

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const params = new URLSearchParams();
      if (outcomeFilter) params.set("outcome", outcomeFilter);
      if (actionFilter) params.set("action", actionFilter);
      const res = await fetch(`/api/quota-attainment?${params}`);
      if (res.ok) setData(await res.json());
    } finally {
      setLoading(false);
    }
  }, [outcomeFilter, actionFilter]);

  useEffect(() => { load(); }, [load]);

  const sum = data?.summary;
  const reps = data?.reps ?? [];
  const outcomes = ["overachieve", "achieve", "slight_miss", "miss", "critical_miss"];
  const actions = ["maintain", "accelerate", "intervention", "escalate"];
  const outcomeTotal = sum ? Object.values(sum.outcome_counts).reduce((a, b) => a + b, 0) : 0;

  return (
    <div className="min-h-screen bg-slate-950 p-6">
      <div className="max-w-7xl mx-auto space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-slate-100">Quota Attainment Predictor</h1>
            <p className="text-sm text-slate-400 mt-0.5">Prédiction d'atteinte quota avec pipeline pondéré — Module 35</p>
          </div>
          <button onClick={load} className="flex items-center gap-2 px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg text-sm font-medium transition-colors">
            <span className={loading ? "animate-spin" : ""}>↻</span> Actualiser
          </button>
        </div>

        {/* KPI Strip */}
        {sum && (
          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
            {[
              { label: "Reps", value: sum.total, sub: "analysés", color: "text-slate-100" },
              { label: "Sur-atteinte", value: sum.overachieve_count, sub: "≥110%", color: "text-emerald-400" },
              { label: "Critique", value: sum.critical_miss_count, sub: "<50%", color: "text-red-400" },
              { label: "Escalades", value: sum.escalation_count, sub: "urgentes", color: "text-orange-400" },
              { label: "Atteinment moy.", value: `${sum.avg_projected_attainment_pct}%`, sub: "projeté", color: "text-indigo-400" },
              { label: "Gap total", value: fmt(sum.total_gap_eur), sub: "à combler", color: "text-yellow-400" },
            ].map((kpi) => (
              <div key={kpi.label} className="bg-slate-800/50 border border-slate-700/50 rounded-xl p-4">
                <p className="text-xs text-slate-500 mb-1">{kpi.label}</p>
                <p className={`text-xl font-bold ${kpi.color}`}>{kpi.value}</p>
                <p className="text-xs text-slate-600 mt-0.5">{kpi.sub}</p>
              </div>
            ))}
          </div>
        )}

        {/* Outcome Distribution Bar */}
        {sum && outcomeTotal > 0 && (
          <div className="bg-slate-800/50 border border-slate-700/50 rounded-xl p-4">
            <p className="text-xs text-slate-500 mb-3 font-medium uppercase tracking-wider">Distribution Résultat Projeté</p>
            <div className="flex h-3 rounded-full overflow-hidden gap-0.5">
              {outcomes.map((o) => {
                const cnt = sum.outcome_counts[o] ?? 0;
                if (!cnt) return null;
                const pct = (cnt / outcomeTotal) * 100;
                const colors: Record<string, string> = { overachieve: "bg-emerald-500", achieve: "bg-blue-500", slight_miss: "bg-yellow-500", miss: "bg-orange-500", critical_miss: "bg-red-500" };
                return <div key={o} className={`${colors[o]} transition-all`} style={{ width: `${pct}%` }} title={`${OUTCOME_META[o]?.label}: ${cnt}`} />;
              })}
            </div>
            <div className="flex flex-wrap gap-4 mt-3">
              {outcomes.map((o) => {
                const cnt = sum.outcome_counts[o] ?? 0;
                if (!cnt) return null;
                const om = OUTCOME_META[o];
                return (
                  <div key={o} className="flex items-center gap-1.5">
                    <span className={`w-2 h-2 rounded-full ${om.dot}`} />
                    <span className="text-xs text-slate-400">{om.label}: <span className="font-semibold text-slate-200">{cnt}</span></span>
                  </div>
                );
              })}
            </div>
          </div>
        )}

        {/* Filters */}
        <div className="flex flex-wrap gap-3">
          <div className="flex items-center gap-2 flex-wrap">
            <span className="text-xs text-slate-500 font-medium">Résultat:</span>
            {["", ...outcomes].map((o) => (
              <button key={o} onClick={() => setOutcomeFilter(o)}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium border transition-colors ${outcomeFilter === o ? "bg-indigo-600 border-indigo-500 text-white" : "bg-slate-800/50 border-slate-700 text-slate-400 hover:text-slate-200"}`}>
                {o === "" ? "Tous" : OUTCOME_META[o]?.label ?? o}
              </button>
            ))}
          </div>
          <div className="flex items-center gap-2 flex-wrap">
            <span className="text-xs text-slate-500 font-medium">Action:</span>
            {["", ...actions].map((a) => (
              <button key={a} onClick={() => setActionFilter(a)}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium border transition-colors ${actionFilter === a ? "bg-indigo-600 border-indigo-500 text-white" : "bg-slate-800/50 border-slate-700 text-slate-400 hover:text-slate-200"}`}>
                {a === "" ? "Tous" : ACTION_META[a]?.label ?? a}
              </button>
            ))}
          </div>
        </div>

        {/* Reps Grid */}
        {loading ? (
          <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
            {Array.from({ length: 6 }).map((_, i) => (
              <div key={i} className="bg-slate-800/30 border border-slate-700/30 rounded-xl h-36 animate-pulse" />
            ))}
          </div>
        ) : reps.length === 0 ? (
          <div className="text-center py-20 text-slate-500">Aucun rep correspondant aux filtres sélectionnés</div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
            {reps.map((r) => (
              <RepCard key={r.rep_id} rep={r} onClick={() => setSelected(r)} />
            ))}
          </div>
        )}
      </div>

      {selected && <AttainmentModal rep={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
