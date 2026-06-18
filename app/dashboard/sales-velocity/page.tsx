"use client";

import { useEffect, useState, useCallback } from "react";

interface RepData {
  rep_id: string;
  rep_name: string;
  region: string;
  segment: string;
  velocity_eur_per_day: number;
  velocity_tier: string;
  velocity_action: string;
  primary_driver: string;
  velocity_score: number;
  opportunity_index: number;
  win_rate_index: number;
  deal_size_index: number;
  cycle_time_index: number;
  quota_attainment_pct: number;
  projected_arr_eur: number;
  velocity_gaps: string[];
  velocity_levers: string[];
  benchmark_velocity_eur_per_day: number;
}

interface Summary {
  total: number;
  tier_counts: Record<string, number>;
  action_counts: Record<string, number>;
  driver_counts: Record<string, number>;
  avg_velocity_eur_per_day: number;
  avg_velocity_score: number;
  elite_count: number;
  stalled_count: number;
  total_projected_arr_eur: number;
}

interface ApiResponse {
  reps: RepData[];
  summary: Summary;
}

const TIER_META: Record<string, { label: string; color: string; dot: string }> = {
  elite:   { label: "Elite",    color: "text-emerald-400", dot: "bg-emerald-500" },
  high:    { label: "Élevée",   color: "text-blue-400",    dot: "bg-blue-500" },
  average: { label: "Moyenne",  color: "text-yellow-400",  dot: "bg-yellow-500" },
  low:     { label: "Faible",   color: "text-orange-400",  dot: "bg-orange-500" },
  stalled: { label: "Bloquée",  color: "text-red-400",     dot: "bg-red-500" },
};

const ACTION_META: Record<string, { label: string; badge: string }> = {
  celebrate:   { label: "Célébrer",   badge: "bg-emerald-500/20 text-emerald-300 border-emerald-500/30" },
  accelerate:  { label: "Accélérer",  badge: "bg-blue-500/20 text-blue-300 border-blue-500/30" },
  optimize:    { label: "Optimiser",  badge: "bg-yellow-500/20 text-yellow-300 border-yellow-500/30" },
  rescue:      { label: "Sauvetage",  badge: "bg-orange-500/20 text-orange-300 border-orange-500/30" },
  reset:       { label: "Reset",      badge: "bg-red-500/20 text-red-300 border-red-500/30" },
};

const DRIVER_META: Record<string, { label: string; icon: string }> = {
  opportunities: { label: "Volume Opps",  icon: "📊" },
  win_rate:      { label: "Taux Closing", icon: "🎯" },
  deal_size:     { label: "Taille Deal",  icon: "💰" },
  cycle_time:    { label: "Cycle Vente",  icon: "⏱" },
  balanced:      { label: "Équilibré",    icon: "⚖️" },
};

function fmt(n: number) {
  if (n >= 1_000_000) return `${(n / 1_000_000).toFixed(1)}M€`;
  if (n >= 1_000) return `${Math.round(n / 1_000)}K€`;
  return `${n}€`;
}

function fmtV(v: number) {
  return `${Math.round(v).toLocaleString("fr-FR")}€/j`;
}

function VelocityRing({ score, size = 96 }: { score: number; size?: number }) {
  const r = size * 0.42;
  const circ = 2 * Math.PI * r;
  const arc = Math.min(1, score / 100) * circ;
  const cx = size / 2;
  const color =
    score >= 85 ? "#10b981" : score >= 65 ? "#3b82f6" : score >= 45 ? "#f59e0b" : score >= 25 ? "#f97316" : "#ef4444";
  return (
    <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`}>
      <circle cx={cx} cy={cx} r={r} fill="none" stroke="#1e293b" strokeWidth={size * 0.1} />
      <circle
        cx={cx} cy={cx} r={r} fill="none" stroke={color}
        strokeWidth={size * 0.1}
        strokeDasharray={`${arc} ${circ - arc}`}
        strokeLinecap="round"
        transform={`rotate(-90 ${cx} ${cx})`}
      />
      <text x={cx} y={cx + size * 0.07} textAnchor="middle" fill={color} fontSize={size * 0.22} fontWeight="bold">
        {score.toFixed(0)}
      </text>
      <text x={cx} y={cx + size * 0.22} textAnchor="middle" fill="#64748b" fontSize={size * 0.11}>
        /100
      </text>
    </svg>
  );
}

function IndexBar({ label, value, max = 2 }: { label: string; value: number; max?: number }) {
  const pct = Math.min(100, (value / max) * 100);
  const color = value >= 1 ? "bg-emerald-500" : value >= 0.7 ? "bg-yellow-500" : "bg-red-500";
  return (
    <div>
      <div className="flex justify-between mb-1">
        <span className="text-xs text-slate-500">{label}</span>
        <span className={`text-xs font-semibold ${value >= 1 ? "text-emerald-400" : value >= 0.7 ? "text-yellow-400" : "text-red-400"}`}>{value.toFixed(2)}x</span>
      </div>
      <div className="h-1.5 bg-slate-700 rounded-full overflow-hidden">
        <div className={`h-full ${color} rounded-full transition-all`} style={{ width: `${pct}%` }} />
      </div>
    </div>
  );
}

function VelocityModal({ rep, onClose }: { rep: RepData; onClose: () => void }) {
  const [tab, setTab] = useState<"indices" | "gaps" | "levers">("indices");
  useEffect(() => {
    const fn = (e: KeyboardEvent) => e.key === "Escape" && onClose();
    window.addEventListener("keydown", fn);
    return () => window.removeEventListener("keydown", fn);
  }, [onClose]);
  const tm = TIER_META[rep.velocity_tier] ?? TIER_META.average;
  const am = ACTION_META[rep.velocity_action] ?? ACTION_META.optimize;
  const dm = DRIVER_META[rep.primary_driver] ?? DRIVER_META.balanced;
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4" onClick={onClose}>
      <div className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-xl shadow-2xl" onClick={(e) => e.stopPropagation()}>
        <div className="p-6 border-b border-slate-800">
          <div className="flex items-start justify-between gap-4">
            <div>
              <h2 className="text-lg font-bold text-slate-100">{rep.rep_name}</h2>
              <p className="text-sm text-slate-400">{rep.region} · {rep.segment}</p>
            </div>
            <div className="flex items-center gap-2 flex-shrink-0">
              <span className={`text-xs font-semibold px-2 py-0.5 rounded-full border ${am.badge}`}>{am.label}</span>
              <button onClick={onClose} className="text-slate-500 hover:text-slate-300 text-xl leading-none">✕</button>
            </div>
          </div>
          <div className="mt-4 grid grid-cols-3 gap-3">
            <div className="bg-slate-800/50 rounded-lg p-3 text-center">
              <p className="text-xs text-slate-500 mb-1">Vélocité</p>
              <p className={`text-base font-bold ${tm.color}`}>{fmtV(rep.velocity_eur_per_day)}</p>
            </div>
            <div className="bg-slate-800/50 rounded-lg p-3 text-center">
              <p className="text-xs text-slate-500 mb-1">ARR projeté</p>
              <p className="text-base font-bold text-indigo-400">{fmt(rep.projected_arr_eur)}</p>
            </div>
            <div className="bg-slate-800/50 rounded-lg p-3 text-center">
              <p className="text-xs text-slate-500 mb-1">Contrainte</p>
              <p className="text-base font-bold text-slate-200">{dm.icon} {dm.label}</p>
            </div>
          </div>
        </div>
        <div className="flex border-b border-slate-800">
          {(["indices", "gaps", "levers"] as const).map((t) => (
            <button key={t} onClick={() => setTab(t)}
              className={`flex-1 py-3 text-xs font-semibold transition-colors ${tab === t ? "text-indigo-400 border-b-2 border-indigo-500" : "text-slate-500 hover:text-slate-300"}`}>
              {t === "indices" ? "Indices (4 Leviers)" : t === "gaps" ? "Points Faibles" : "Plan d'Action"}
            </button>
          ))}
        </div>
        <div className="p-5 max-h-72 overflow-y-auto">
          {tab === "indices" && (
            <div className="space-y-4">
              <IndexBar label="Volume Opportunités" value={rep.opportunity_index} />
              <IndexBar label="Taux de Closing" value={rep.win_rate_index} />
              <IndexBar label="Taille Moyenne Deal" value={rep.deal_size_index} />
              <IndexBar label="Rapidité Cycle" value={rep.cycle_time_index} />
              <div className="pt-2 border-t border-slate-800">
                <div className="flex justify-between text-xs">
                  <span className="text-slate-500">Vélocité benchmark</span>
                  <span className="text-slate-300">{fmtV(rep.benchmark_velocity_eur_per_day)}</span>
                </div>
                <div className="flex justify-between text-xs mt-1">
                  <span className="text-slate-500">Atteinment quota</span>
                  <span className="text-indigo-400 font-semibold">{rep.quota_attainment_pct.toFixed(1)}%</span>
                </div>
              </div>
            </div>
          )}
          {tab === "gaps" && (
            <ul className="space-y-2">
              {rep.velocity_gaps.length === 0
                ? <li className="text-sm text-slate-500 italic">Aucun gap identifié — vélocité au-dessus du benchmark</li>
                : rep.velocity_gaps.map((g, i) => (
                    <li key={i} className="flex items-start gap-2 text-sm text-slate-300">
                      <span className="text-red-400 mt-0.5 flex-shrink-0">▸</span>{g}
                    </li>
                  ))}
            </ul>
          )}
          {tab === "levers" && (
            <ul className="space-y-2">
              {rep.velocity_levers.map((l, i) => (
                <li key={i} className="flex items-start gap-2 text-sm text-slate-300">
                  <span className="text-indigo-400 mt-0.5 flex-shrink-0">✓</span>{l}
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
  const tm = TIER_META[rep.velocity_tier] ?? TIER_META.average;
  const am = ACTION_META[rep.velocity_action] ?? ACTION_META.optimize;
  const dm = DRIVER_META[rep.primary_driver] ?? DRIVER_META.balanced;
  const vsRatio = rep.benchmark_velocity_eur_per_day > 0
    ? rep.velocity_eur_per_day / rep.benchmark_velocity_eur_per_day
    : 0;
  return (
    <div onClick={onClick} className="bg-slate-800/50 border border-slate-700/50 rounded-xl p-4 cursor-pointer hover:border-indigo-500/40 hover:bg-slate-800/80 transition-all group">
      <div className="flex items-start justify-between gap-3 mb-3">
        <div className="flex items-center gap-3">
          <VelocityRing score={rep.velocity_score} size={56} />
          <div>
            <h3 className="font-semibold text-slate-100 text-sm group-hover:text-indigo-300 transition-colors">{rep.rep_name}</h3>
            <p className="text-xs text-slate-500">{rep.region} · {rep.segment}</p>
            <div className="flex items-center gap-1.5 mt-1">
              <span className={`w-1.5 h-1.5 rounded-full ${tm.dot}`} />
              <span className={`text-xs font-medium ${tm.color}`}>{tm.label}</span>
            </div>
          </div>
        </div>
        <span className={`text-xs font-semibold px-2 py-0.5 rounded-full border flex-shrink-0 ${am.badge}`}>{am.label}</span>
      </div>
      <div className="grid grid-cols-3 gap-2 text-center">
        <div className="bg-slate-900/50 rounded-lg p-2">
          <p className="text-xs text-slate-500 mb-0.5">€/jour</p>
          <p className={`text-sm font-bold ${tm.color}`}>{Math.round(rep.velocity_eur_per_day).toLocaleString("fr-FR")}</p>
        </div>
        <div className="bg-slate-900/50 rounded-lg p-2">
          <p className="text-xs text-slate-500 mb-0.5">vs Bench.</p>
          <p className={`text-sm font-bold ${vsRatio >= 1 ? "text-emerald-400" : "text-red-400"}`}>{vsRatio.toFixed(1)}x</p>
        </div>
        <div className="bg-slate-900/50 rounded-lg p-2">
          <p className="text-xs text-slate-500 mb-0.5">ARR projeté</p>
          <p className="text-sm font-bold text-indigo-400">{fmt(rep.projected_arr_eur)}</p>
        </div>
      </div>
      <div className="mt-2 flex items-center gap-1.5">
        <span className="text-xs">{dm.icon}</span>
        <span className="text-xs text-slate-500">Contrainte: <span className="text-slate-400">{dm.label}</span></span>
      </div>
    </div>
  );
}

export default function SalesVelocityPage() {
  const [data, setData] = useState<ApiResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [selected, setSelected] = useState<RepData | null>(null);
  const [tierFilter, setTierFilter] = useState("");
  const [actionFilter, setActionFilter] = useState("");

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const params = new URLSearchParams();
      if (tierFilter) params.set("tier", tierFilter);
      if (actionFilter) params.set("action", actionFilter);
      const res = await fetch(`/api/sales-velocity?${params}`);
      if (res.ok) setData(await res.json());
    } finally {
      setLoading(false);
    }
  }, [tierFilter, actionFilter]);

  useEffect(() => { load(); }, [load]);

  const sum = data?.summary;
  const reps = data?.reps ?? [];
  const tiers = ["elite", "high", "average", "low", "stalled"];
  const actions = ["celebrate", "accelerate", "optimize", "rescue", "reset"];
  const tierTotal = sum ? Object.values(sum.tier_counts).reduce((a, b) => a + b, 0) : 0;

  return (
    <div className="min-h-screen bg-slate-950 p-6">
      <div className="max-w-7xl mx-auto space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-slate-100">Sales Velocity Engine</h1>
            <p className="text-sm text-slate-400 mt-0.5">Mesure et optimisation de la vélocité commerciale — Module 33</p>
          </div>
          <button onClick={load} className="flex items-center gap-2 px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg text-sm font-medium transition-colors">
            <span className={loading ? "animate-spin" : ""}>↻</span> Actualiser
          </button>
        </div>

        {/* KPI Strip */}
        {sum && (
          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
            {[
              { label: "Reps analysés", value: sum.total, sub: "total", color: "text-slate-100" },
              { label: "Elite", value: sum.elite_count, sub: "reps", color: "text-emerald-400" },
              { label: "Bloqués", value: sum.stalled_count, sub: "reps", color: "text-red-400" },
              { label: "ARR projeté", value: fmt(sum.total_projected_arr_eur), sub: "team total", color: "text-indigo-400" },
              { label: "Vélocité moy.", value: fmtV(sum.avg_velocity_eur_per_day), sub: "équipe", color: "text-blue-400" },
              { label: "Score moyen", value: `${sum.avg_velocity_score}/100`, sub: "vélocité", color: "text-violet-400" },
            ].map((kpi) => (
              <div key={kpi.label} className="bg-slate-800/50 border border-slate-700/50 rounded-xl p-4">
                <p className="text-xs text-slate-500 mb-1">{kpi.label}</p>
                <p className={`text-xl font-bold ${kpi.color}`}>{kpi.value}</p>
                <p className="text-xs text-slate-600 mt-0.5">{kpi.sub}</p>
              </div>
            ))}
          </div>
        )}

        {/* Tier Distribution Bar */}
        {sum && tierTotal > 0 && (
          <div className="bg-slate-800/50 border border-slate-700/50 rounded-xl p-4">
            <p className="text-xs text-slate-500 mb-3 font-medium uppercase tracking-wider">Distribution Tier Vélocité</p>
            <div className="flex h-3 rounded-full overflow-hidden gap-0.5">
              {tiers.map((t) => {
                const cnt = sum.tier_counts[t] ?? 0;
                if (!cnt) return null;
                const pct = (cnt / tierTotal) * 100;
                const colors: Record<string, string> = { elite: "bg-emerald-500", high: "bg-blue-500", average: "bg-yellow-500", low: "bg-orange-500", stalled: "bg-red-500" };
                return <div key={t} className={`${colors[t]} transition-all`} style={{ width: `${pct}%` }} title={`${TIER_META[t]?.label}: ${cnt}`} />;
              })}
            </div>
            <div className="flex flex-wrap gap-4 mt-3">
              {tiers.map((t) => {
                const cnt = sum.tier_counts[t] ?? 0;
                if (!cnt) return null;
                const tm = TIER_META[t];
                return (
                  <div key={t} className="flex items-center gap-1.5">
                    <span className={`w-2 h-2 rounded-full ${tm.dot}`} />
                    <span className="text-xs text-slate-400">{tm.label}: <span className="font-semibold text-slate-200">{cnt}</span></span>
                  </div>
                );
              })}
            </div>
          </div>
        )}

        {/* Filters */}
        <div className="flex flex-wrap gap-3">
          <div className="flex items-center gap-2 flex-wrap">
            <span className="text-xs text-slate-500 font-medium">Tier:</span>
            {["", ...tiers].map((t) => (
              <button key={t} onClick={() => setTierFilter(t)}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium border transition-colors ${tierFilter === t ? "bg-indigo-600 border-indigo-500 text-white" : "bg-slate-800/50 border-slate-700 text-slate-400 hover:text-slate-200"}`}>
                {t === "" ? "Tous" : TIER_META[t]?.label ?? t}
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

      {selected && <VelocityModal rep={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
