"use client";

import { useEffect, useState } from "react";

interface RepData {
  rep_id: string;
  rep_name: string;
  region: string;
  segment: string;
  quota_eur: number;
  territory_health: string;
  territory_action: string;
  coverage_gap: string;
  workload_balance: string;
  territory_score: number;
  coverage_pct: number;
  icp_penetration_pct: number;
  whitespace_opportunity_eur: number;
  workload_ratio: number;
  market_penetration_pct: number;
  territory_drivers: string[];
  territory_plays: string[];
  optimization_score: number;
}

interface Summary {
  total: number;
  health_counts: Record<string, number>;
  action_counts: Record<string, number>;
  gap_counts: Record<string, number>;
  avg_territory_score: number;
  avg_coverage_pct: number;
  avg_optimization_score: number;
  poor_count: number;
  restructure_count: number;
  total_whitespace_eur: number;
}

interface ApiResponse {
  reps: RepData[];
  summary: Summary;
}

const HEALTH_META: Record<string, { label: string; color: string; dot: string }> = {
  excellent: { label: "Excellent",    color: "text-emerald-400", dot: "bg-emerald-500" },
  good:      { label: "Bon",          color: "text-blue-400",    dot: "bg-blue-500" },
  fair:      { label: "Correct",      color: "text-yellow-400",  dot: "bg-yellow-500" },
  poor:      { label: "Insuffisant",  color: "text-red-400",     dot: "bg-red-500" },
};

const ACTION_META: Record<string, { label: string; badge: string }> = {
  optimize:    { label: "Optimiser",    badge: "bg-emerald-500/20 text-emerald-300 border-emerald-500/30" },
  expand:      { label: "Étendre",      badge: "bg-blue-500/20 text-blue-300 border-blue-500/30" },
  rebalance:   { label: "Rééquilibrer", badge: "bg-yellow-500/20 text-yellow-300 border-yellow-500/30" },
  restructure: { label: "Restructurer", badge: "bg-red-500/20 text-red-300 border-red-500/30" },
};

const GAP_META: Record<string, { label: string; color: string }> = {
  none:        { label: "Aucun",        color: "text-emerald-400" },
  minor:       { label: "Mineur",       color: "text-blue-400" },
  significant: { label: "Significatif", color: "text-yellow-400" },
  critical:    { label: "Critique",     color: "text-red-400" },
};

const BALANCE_META: Record<string, { label: string; color: string }> = {
  balanced:    { label: "Équilibré",     color: "text-emerald-400" },
  overloaded:  { label: "Surchargé",     color: "text-orange-400" },
  underloaded: { label: "Sous-chargé",   color: "text-blue-400" },
  skewed:      { label: "Asymétrique",   color: "text-yellow-400" },
};

function fmt(n: number) {
  if (n >= 1_000_000) return `${(n / 1_000_000).toFixed(1)}M€`;
  if (n >= 1_000) return `${Math.round(n / 1_000)}K€`;
  return `${n}€`;
}

function TerritoryRing({ score, size = 96 }: { score: number; size?: number }) {
  const r = size * 0.42;
  const circ = 2 * Math.PI * r;
  const arc = Math.min(1, score / 100) * circ;
  const cx = size / 2;
  const color =
    score >= 75 ? "#10b981" : score >= 55 ? "#3b82f6" : score >= 35 ? "#f59e0b" : "#ef4444";
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

function TerritoryModal({ rep, onClose }: { rep: RepData; onClose: () => void }) {
  const [tab, setTab] = useState<"drivers" | "plays" | "metrics">("drivers");
  useEffect(() => {
    const fn = (e: KeyboardEvent) => e.key === "Escape" && onClose();
    window.addEventListener("keydown", fn);
    return () => window.removeEventListener("keydown", fn);
  }, [onClose]);
  const hm = HEALTH_META[rep.territory_health] ?? HEALTH_META.poor;
  const am = ACTION_META[rep.territory_action] ?? ACTION_META.optimize;
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
              <p className="text-xs text-slate-500 mb-1">Score</p>
              <p className={`text-lg font-bold ${hm.color}`}>{rep.territory_score.toFixed(1)}/100</p>
            </div>
            <div className="bg-slate-800/50 rounded-lg p-3 text-center">
              <p className="text-xs text-slate-500 mb-1">Couverture</p>
              <p className="text-lg font-bold text-indigo-400">{rep.coverage_pct.toFixed(0)}%</p>
            </div>
            <div className="bg-slate-800/50 rounded-lg p-3 text-center">
              <p className="text-xs text-slate-500 mb-1">Whitespace</p>
              <p className="text-lg font-bold text-violet-400">{fmt(rep.whitespace_opportunity_eur)}</p>
            </div>
          </div>
        </div>
        <div className="flex border-b border-slate-800">
          {(["drivers", "plays", "metrics"] as const).map((t) => (
            <button key={t} onClick={() => setTab(t)}
              className={`flex-1 py-3 text-xs font-semibold transition-colors ${tab === t ? "text-indigo-400 border-b-2 border-indigo-500" : "text-slate-500 hover:text-slate-300"}`}>
              {t === "drivers" ? "Problèmes" : t === "plays" ? "Plan d'Action" : "Métriques"}
            </button>
          ))}
        </div>
        <div className="p-5 max-h-72 overflow-y-auto">
          {tab === "drivers" && (
            <ul className="space-y-2">
              {rep.territory_drivers.length === 0
                ? <li className="text-sm text-slate-500 italic">Aucun problème — territoire en excellente forme</li>
                : rep.territory_drivers.map((d, i) => (
                    <li key={i} className="flex items-start gap-2 text-sm text-slate-300">
                      <span className="text-orange-400 mt-0.5 flex-shrink-0">▸</span>{d}
                    </li>
                  ))}
            </ul>
          )}
          {tab === "plays" && (
            <ul className="space-y-2">
              {rep.territory_plays.map((p, i) => (
                <li key={i} className="flex items-start gap-2 text-sm text-slate-300">
                  <span className="text-indigo-400 mt-0.5 flex-shrink-0">✓</span>{p}
                </li>
              ))}
            </ul>
          )}
          {tab === "metrics" && (
            <div className="grid grid-cols-2 gap-3">
              {[
                ["Quota", fmt(rep.quota_eur)],
                ["ICP Pénétration", `${rep.icp_penetration_pct.toFixed(0)}%`],
                ["Charge (ratio)", `${rep.workload_ratio.toFixed(2)}x`],
                ["Pénétration Marché", `${rep.market_penetration_pct.toFixed(0)}%`],
                ["Score Optim.", `${rep.optimization_score.toFixed(1)}/100`],
                ["Balance Charge", BALANCE_META[rep.workload_balance]?.label ?? rep.workload_balance],
                ["Gap Couverture", GAP_META[rep.coverage_gap]?.label ?? rep.coverage_gap],
                ["Santé Territoire", HEALTH_META[rep.territory_health]?.label ?? rep.territory_health],
              ].map(([k, v]) => (
                <div key={k} className="bg-slate-800/50 rounded-lg p-2.5">
                  <p className="text-xs text-slate-500">{k}</p>
                  <p className="text-sm font-semibold text-slate-200">{v}</p>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

function RepCard({ rep, onClick }: { rep: RepData; onClick: () => void }) {
  const hm = HEALTH_META[rep.territory_health] ?? HEALTH_META.poor;
  const am = ACTION_META[rep.territory_action] ?? ACTION_META.optimize;
  return (
    <div onClick={onClick} className="bg-slate-800/50 border border-slate-700/50 rounded-xl p-4 cursor-pointer hover:border-indigo-500/40 hover:bg-slate-800/80 transition-all group">
      <div className="flex items-start justify-between gap-3 mb-3">
        <div className="flex items-center gap-3">
          <TerritoryRing score={rep.territory_score} size={56} />
          <div>
            <h3 className="font-semibold text-slate-100 text-sm group-hover:text-indigo-300 transition-colors">{rep.rep_name}</h3>
            <p className="text-xs text-slate-500">{rep.region} · {rep.segment}</p>
            <div className="flex items-center gap-1.5 mt-1">
              <span className={`w-1.5 h-1.5 rounded-full ${hm.dot}`} />
              <span className={`text-xs font-medium ${hm.color}`}>{hm.label}</span>
            </div>
          </div>
        </div>
        <span className={`text-xs font-semibold px-2 py-0.5 rounded-full border flex-shrink-0 ${am.badge}`}>{am.label}</span>
      </div>
      <div className="grid grid-cols-3 gap-2 text-center">
        <div className="bg-slate-900/50 rounded-lg p-2">
          <p className="text-xs text-slate-500 mb-0.5">Couverture</p>
          <p className="text-sm font-bold text-indigo-400">{rep.coverage_pct.toFixed(0)}%</p>
        </div>
        <div className="bg-slate-900/50 rounded-lg p-2">
          <p className="text-xs text-slate-500 mb-0.5">ICP</p>
          <p className="text-sm font-bold text-blue-400">{rep.icp_penetration_pct.toFixed(0)}%</p>
        </div>
        <div className="bg-slate-900/50 rounded-lg p-2">
          <p className="text-xs text-slate-500 mb-0.5">Whitespace</p>
          <p className="text-sm font-bold text-violet-400">{fmt(rep.whitespace_opportunity_eur)}</p>
        </div>
      </div>
      {rep.territory_drivers.length > 0 && (
        <p className="mt-2 text-xs text-slate-500 truncate">
          ▸ {rep.territory_drivers[0]}
        </p>
      )}
    </div>
  );
}

export default function TerritoryOptimizerPage() {
  const [data, setData] = useState<ApiResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [selected, setSelected] = useState<RepData | null>(null);
  const [healthFilter, setHealthFilter] = useState("");
  const [actionFilter, setActionFilter] = useState("");

  useEffect(() => {
    async function load() {
        setLoading(true);
        try {
          const params = new URLSearchParams();
          if (healthFilter) params.set("health", healthFilter);
          if (actionFilter) params.set("action", actionFilter);
          const res = await fetch(`/api/territory-optimizer?${params}`);
          if (res.ok) setData(await res.json());
        } finally {
          setLoading(false);
        }
  }
    load();
  }, [healthFilter, actionFilter]);

  const sum = data?.summary;
  const reps = data?.reps ?? [];
  const healths = ["excellent", "good", "fair", "poor"];
  const actions = ["optimize", "expand", "rebalance", "restructure"];
  const healthTotal = sum ? Object.values(sum.health_counts).reduce((a, b) => a + b, 0) : 0;

  return (
    <div className="min-h-screen bg-slate-950 p-6">
      <div className="max-w-7xl mx-auto space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-slate-100">Territory Optimizer</h1>
            <p className="text-sm text-slate-400 mt-0.5">Optimisation & équilibrage des territoires commerciaux — Module 32</p>
          </div>
          <button onClick={load} className="flex items-center gap-2 px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg text-sm font-medium transition-colors">
            <span className={loading ? "animate-spin" : ""}>↻</span> Actualiser
          </button>
        </div>

        {/* KPI Strip */}
        {sum && (
          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
            {[
              { label: "Territoires", value: sum.total, sub: "analysés", color: "text-slate-100" },
              { label: "Insuffisants", value: sum.poor_count, sub: "reps", color: "text-red-400" },
              { label: "À restructurer", value: sum.restructure_count, sub: "reps", color: "text-orange-400" },
              { label: "Whitespace total", value: fmt(sum.total_whitespace_eur), sub: "opportunité", color: "text-violet-400" },
              { label: "Score moyen", value: `${sum.avg_territory_score}/100`, sub: "territoire", color: "text-indigo-400" },
              { label: "Couverture moy.", value: `${sum.avg_coverage_pct}%`, sub: "comptes actifs", color: "text-blue-400" },
            ].map((kpi) => (
              <div key={kpi.label} className="bg-slate-800/50 border border-slate-700/50 rounded-xl p-4">
                <p className="text-xs text-slate-500 mb-1">{kpi.label}</p>
                <p className={`text-xl font-bold ${kpi.color}`}>{kpi.value}</p>
                <p className="text-xs text-slate-600 mt-0.5">{kpi.sub}</p>
              </div>
            ))}
          </div>
        )}

        {/* Health Distribution Bar */}
        {sum && healthTotal > 0 && (
          <div className="bg-slate-800/50 border border-slate-700/50 rounded-xl p-4">
            <p className="text-xs text-slate-500 mb-3 font-medium uppercase tracking-wider">Distribution Santé Territoire</p>
            <div className="flex h-3 rounded-full overflow-hidden gap-0.5">
              {healths.map((h) => {
                const cnt = sum.health_counts[h] ?? 0;
                if (!cnt) return null;
                const pct = (cnt / healthTotal) * 100;
                const colors: Record<string, string> = { excellent: "bg-emerald-500", good: "bg-blue-500", fair: "bg-yellow-500", poor: "bg-red-500" };
                return <div key={h} className={`${colors[h]} transition-all`} style={{ width: `${pct}%` }} title={`${HEALTH_META[h]?.label}: ${cnt}`} />;
              })}
            </div>
            <div className="flex flex-wrap gap-4 mt-3">
              {healths.map((h) => {
                const cnt = sum.health_counts[h] ?? 0;
                if (!cnt) return null;
                const hm = HEALTH_META[h];
                return (
                  <div key={h} className="flex items-center gap-1.5">
                    <span className={`w-2 h-2 rounded-full ${hm.dot}`} />
                    <span className="text-xs text-slate-400">{hm.label}: <span className="font-semibold text-slate-200">{cnt}</span></span>
                  </div>
                );
              })}
            </div>
          </div>
        )}

        {/* Filters */}
        <div className="flex flex-wrap gap-3">
          <div className="flex items-center gap-2 flex-wrap">
            <span className="text-xs text-slate-500 font-medium">Santé:</span>
            {["", ...healths].map((h) => (
              <button key={h} onClick={() => setHealthFilter(h)}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium border transition-colors ${healthFilter === h ? "bg-indigo-600 border-indigo-500 text-white" : "bg-slate-800/50 border-slate-700 text-slate-400 hover:text-slate-200"}`}>
                {h === "" ? "Tous" : HEALTH_META[h]?.label ?? h}
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
          <div className="text-center py-20 text-slate-500">Aucun territoire correspondant aux filtres sélectionnés</div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
            {reps.map((r) => (
              <RepCard key={r.rep_id} rep={r} onClick={() => setSelected(r)} />
            ))}
          </div>
        )}
      </div>

      {selected && <TerritoryModal rep={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
