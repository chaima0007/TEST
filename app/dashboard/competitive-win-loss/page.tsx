"use client";

import { useEffect, useState, useCallback } from "react";

interface CompetitorData {
  competitor: string;
  total_deals: number;
  wins: number;
  losses: number;
  no_decisions: number;
  win_rate_pct: number;
  avg_deal_size_eur: number;
  avg_cycle_days: number;
  position: string;
  action: string;
  top_loss_reasons: string[];
  win_patterns: string[];
  loss_patterns: string[];
  battlecard_priorities: string[];
  arr_won_eur: number;
  arr_lost_eur: number;
  net_arr_eur: number;
}

interface Summary {
  total_competitors: number;
  total_deals: number;
  overall_win_rate_pct: number;
  total_arr_won_eur: number;
  total_arr_lost_eur: number;
  net_arr_eur: number;
  position_counts: Record<string, number>;
  action_counts: Record<string, number>;
  needs_battlecard_count: number;
  most_common_loss_reason: string;
}

interface ApiResponse {
  competitors: CompetitorData[];
  summary: Summary;
}

const POSITION_META: Record<string, { label: string; color: string; dot: string }> = {
  dominant:    { label: "Dominant",     color: "text-emerald-400", dot: "bg-emerald-500" },
  strong:      { label: "Fort",         color: "text-blue-400",    dot: "bg-blue-500" },
  competitive: { label: "Compétitif",   color: "text-yellow-400",  dot: "bg-yellow-500" },
  weak:        { label: "Faible",       color: "text-red-400",     dot: "bg-red-500" },
  unknown:     { label: "Inconnu",      color: "text-slate-400",   dot: "bg-slate-500" },
};

const ACTION_META: Record<string, { label: string; badge: string }> = {
  replicate:      { label: "Répliquer",     badge: "bg-emerald-500/20 text-emerald-300 border-emerald-500/30" },
  defend:         { label: "Défendre",      badge: "bg-blue-500/20 text-blue-300 border-blue-500/30" },
  differentiate:  { label: "Différencier",  badge: "bg-yellow-500/20 text-yellow-300 border-yellow-500/30" },
  battlecard:     { label: "Battlecard",    badge: "bg-red-500/20 text-red-300 border-red-500/30" },
};

function fmt(n: number) {
  if (Math.abs(n) >= 1_000_000) return `${(n / 1_000_000).toFixed(1)}M€`;
  if (Math.abs(n) >= 1_000) return `${Math.round(n / 1_000)}K€`;
  return `${n}€`;
}

function WinRateRing({ rate, size = 80 }: { rate: number; size?: number }) {
  const r = size * 0.42;
  const circ = 2 * Math.PI * r;
  const arc = Math.min(1, rate / 100) * circ;
  const cx = size / 2;
  const color = rate >= 70 ? "#10b981" : rate >= 50 ? "#3b82f6" : rate >= 30 ? "#f59e0b" : "#ef4444";
  return (
    <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`}>
      <circle cx={cx} cy={cx} r={r} fill="none" stroke="#1e293b" strokeWidth={size * 0.1} />
      <circle cx={cx} cy={cx} r={r} fill="none" stroke={color}
        strokeWidth={size * 0.1}
        strokeDasharray={`${arc} ${circ - arc}`}
        strokeLinecap="round"
        transform={`rotate(-90 ${cx} ${cx})`}
      />
      <text x={cx} y={cx + size * 0.07} textAnchor="middle" fill={color} fontSize={size * 0.24} fontWeight="bold">
        {rate.toFixed(0)}%
      </text>
      <text x={cx} y={cx + size * 0.24} textAnchor="middle" fill="#64748b" fontSize={size * 0.12}>
        win rate
      </text>
    </svg>
  );
}

function CompetitorModal({ comp, onClose }: { comp: CompetitorData; onClose: () => void }) {
  const [tab, setTab] = useState<"wins" | "losses" | "battlecard">("wins");
  useEffect(() => {
    const fn = (e: KeyboardEvent) => e.key === "Escape" && onClose();
    window.addEventListener("keydown", fn);
    return () => window.removeEventListener("keydown", fn);
  }, [onClose]);
  const pm = POSITION_META[comp.position] ?? POSITION_META.unknown;
  const am = ACTION_META[comp.action] ?? ACTION_META.differentiate;
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4" onClick={onClose}>
      <div className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-xl shadow-2xl" onClick={(e) => e.stopPropagation()}>
        <div className="p-6 border-b border-slate-800">
          <div className="flex items-start justify-between gap-4">
            <div>
              <h2 className="text-xl font-bold text-slate-100">{comp.competitor}</h2>
              <div className="flex items-center gap-2 mt-1">
                <span className={`w-2 h-2 rounded-full ${pm.dot}`} />
                <span className={`text-sm font-medium ${pm.color}`}>{pm.label}</span>
                <span className="text-slate-600">·</span>
                <span className="text-sm text-slate-400">{comp.total_deals} deals analysés</span>
              </div>
            </div>
            <div className="flex items-center gap-2 flex-shrink-0">
              <span className={`text-xs font-semibold px-2 py-0.5 rounded-full border ${am.badge}`}>{am.label}</span>
              <button onClick={onClose} className="text-slate-500 hover:text-slate-300 text-xl leading-none">✕</button>
            </div>
          </div>
          <div className="mt-4 grid grid-cols-4 gap-2">
            {[
              { label: "Gagnés", value: comp.wins, color: "text-emerald-400" },
              { label: "Perdus", value: comp.losses, color: "text-red-400" },
              { label: "ARR gagné", value: fmt(comp.arr_won_eur), color: "text-emerald-400" },
              { label: "ARR perdu", value: fmt(comp.arr_lost_eur), color: "text-red-400" },
            ].map((k) => (
              <div key={k.label} className="bg-slate-800/50 rounded-lg p-2 text-center">
                <p className="text-xs text-slate-500 mb-0.5">{k.label}</p>
                <p className={`text-sm font-bold ${k.color}`}>{k.value}</p>
              </div>
            ))}
          </div>
        </div>
        <div className="flex border-b border-slate-800">
          {(["wins", "losses", "battlecard"] as const).map((t) => (
            <button key={t} onClick={() => setTab(t)}
              className={`flex-1 py-3 text-xs font-semibold transition-colors ${tab === t ? "text-indigo-400 border-b-2 border-indigo-500" : "text-slate-500 hover:text-slate-300"}`}>
              {t === "wins" ? "Patterns Victoire" : t === "losses" ? "Patterns Défaite" : "Battlecard"}
            </button>
          ))}
        </div>
        <div className="p-5 max-h-72 overflow-y-auto">
          {tab === "wins" && (
            <div className="space-y-4">
              {comp.win_patterns.length > 0 && (
                <div>
                  <p className="text-xs text-slate-500 font-medium mb-2">Patterns des deals gagnés</p>
                  <ul className="space-y-1.5">
                    {comp.win_patterns.map((p, i) => (
                      <li key={i} className="flex items-start gap-2 text-sm text-slate-300">
                        <span className="text-emerald-400 flex-shrink-0">✓</span>{p}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
              <div>
                <p className="text-xs text-slate-500 font-medium mb-2">Métriques moyennes</p>
                <div className="grid grid-cols-2 gap-2">
                  <div className="bg-slate-800/50 rounded-lg p-2.5">
                    <p className="text-xs text-slate-500">Deal size moyen</p>
                    <p className="text-sm font-semibold text-slate-200">{fmt(comp.avg_deal_size_eur)}</p>
                  </div>
                  <div className="bg-slate-800/50 rounded-lg p-2.5">
                    <p className="text-xs text-slate-500">Cycle moyen</p>
                    <p className="text-sm font-semibold text-slate-200">{comp.avg_cycle_days.toFixed(0)}j</p>
                  </div>
                </div>
              </div>
            </div>
          )}
          {tab === "losses" && (
            <div className="space-y-4">
              {comp.top_loss_reasons.length > 0 && (
                <div>
                  <p className="text-xs text-slate-500 font-medium mb-2">Principales raisons de défaite</p>
                  <ul className="space-y-1.5">
                    {comp.top_loss_reasons.map((r, i) => (
                      <li key={i} className="flex items-start gap-2 text-sm text-slate-300">
                        <span className="text-red-400 flex-shrink-0">▸</span>{r}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
              {comp.loss_patterns.length > 0 && (
                <div>
                  <p className="text-xs text-slate-500 font-medium mb-2">Patterns des défaites</p>
                  <ul className="space-y-1.5">
                    {comp.loss_patterns.map((p, i) => (
                      <li key={i} className="flex items-start gap-2 text-sm text-slate-300">
                        <span className="text-orange-400 flex-shrink-0">!</span>{p}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          )}
          {tab === "battlecard" && (
            <ul className="space-y-2">
              {comp.battlecard_priorities.map((b, i) => (
                <li key={i} className="flex items-start gap-2 text-sm text-slate-300">
                  <span className="text-indigo-400 font-bold flex-shrink-0">{i + 1}.</span>{b}
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>
    </div>
  );
}

function CompetitorCard({ comp, onClick }: { comp: CompetitorData; onClick: () => void }) {
  const pm = POSITION_META[comp.position] ?? POSITION_META.unknown;
  const am = ACTION_META[comp.action] ?? ACTION_META.differentiate;
  return (
    <div onClick={onClick} className="bg-slate-800/50 border border-slate-700/50 rounded-xl p-4 cursor-pointer hover:border-indigo-500/40 hover:bg-slate-800/80 transition-all group">
      <div className="flex items-center justify-between gap-3 mb-3">
        <div className="flex items-center gap-3">
          <WinRateRing rate={comp.win_rate_pct} size={64} />
          <div>
            <h3 className="font-bold text-slate-100 text-base group-hover:text-indigo-300 transition-colors">{comp.competitor}</h3>
            <div className="flex items-center gap-1.5 mt-0.5">
              <span className={`w-1.5 h-1.5 rounded-full ${pm.dot}`} />
              <span className={`text-xs font-medium ${pm.color}`}>{pm.label}</span>
            </div>
            <p className="text-xs text-slate-500 mt-0.5">{comp.total_deals} deals · {comp.avg_cycle_days.toFixed(0)}j cycle</p>
          </div>
        </div>
        <span className={`text-xs font-semibold px-2 py-0.5 rounded-full border flex-shrink-0 ${am.badge}`}>{am.label}</span>
      </div>
      <div className="grid grid-cols-3 gap-2 text-center">
        <div className="bg-slate-900/50 rounded-lg p-2">
          <p className="text-xs text-slate-500 mb-0.5">Gagnés</p>
          <p className="text-sm font-bold text-emerald-400">{comp.wins}</p>
        </div>
        <div className="bg-slate-900/50 rounded-lg p-2">
          <p className="text-xs text-slate-500 mb-0.5">Perdus</p>
          <p className="text-sm font-bold text-red-400">{comp.losses}</p>
        </div>
        <div className="bg-slate-900/50 rounded-lg p-2">
          <p className="text-xs text-slate-500 mb-0.5">Net ARR</p>
          <p className={`text-sm font-bold ${comp.net_arr_eur >= 0 ? "text-emerald-400" : "text-red-400"}`}>{fmt(comp.net_arr_eur)}</p>
        </div>
      </div>
      {comp.top_loss_reasons.length > 0 && (
        <p className="mt-2 text-xs text-slate-500 truncate">▸ {comp.top_loss_reasons[0]}</p>
      )}
    </div>
  );
}

export default function CompetitiveWinLossPage() {
  const [data, setData] = useState<ApiResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [selected, setSelected] = useState<CompetitorData | null>(null);
  const [positionFilter, setPositionFilter] = useState("");
  const [actionFilter, setActionFilter] = useState("");

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const params = new URLSearchParams();
      if (positionFilter) params.set("position", positionFilter);
      if (actionFilter) params.set("action", actionFilter);
      const res = await fetch(`/api/competitive-win-loss?${params}`);
      if (res.ok) setData(await res.json());
    } finally {
      setLoading(false);
    }
  }, [positionFilter, actionFilter]);

  useEffect(() => { load(); }, [load]);

  const sum = data?.summary;
  const competitors = data?.competitors ?? [];
  const positions = ["dominant", "strong", "competitive", "weak"];
  const actions = ["replicate", "defend", "differentiate", "battlecard"];
  const posTotal = sum ? Object.values(sum.position_counts).reduce((a, b) => a + b, 0) : 0;

  return (
    <div className="min-h-screen bg-slate-950 p-6">
      <div className="max-w-7xl mx-auto space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-slate-100">Competitive Win-Loss</h1>
            <p className="text-sm text-slate-400 mt-0.5">Analyse gagnée/perdue par concurrent — Module 34</p>
          </div>
          <button onClick={load} className="flex items-center gap-2 px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg text-sm font-medium transition-colors">
            <span className={loading ? "animate-spin" : ""}>↻</span> Actualiser
          </button>
        </div>

        {/* KPI Strip */}
        {sum && (
          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
            {[
              { label: "Concurrents", value: sum.total_competitors, sub: "analysés", color: "text-slate-100" },
              { label: "Win rate global", value: `${sum.overall_win_rate_pct.toFixed(1)}%`, sub: `${sum.total_deals} deals`, color: "text-indigo-400" },
              { label: "ARR gagné", value: fmt(sum.total_arr_won_eur), sub: "total", color: "text-emerald-400" },
              { label: "ARR perdu", value: fmt(sum.total_arr_lost_eur), sub: "total", color: "text-red-400" },
              { label: "Net ARR", value: fmt(sum.net_arr_eur), sub: "gagné−perdu", color: sum.net_arr_eur >= 0 ? "text-emerald-400" : "text-red-400" },
              { label: "Battlecard", value: sum.needs_battlecard_count, sub: "urgents", color: "text-orange-400" },
            ].map((kpi) => (
              <div key={kpi.label} className="bg-slate-800/50 border border-slate-700/50 rounded-xl p-4">
                <p className="text-xs text-slate-500 mb-1">{kpi.label}</p>
                <p className={`text-xl font-bold ${kpi.color}`}>{kpi.value}</p>
                <p className="text-xs text-slate-600 mt-0.5">{kpi.sub}</p>
              </div>
            ))}
          </div>
        )}

        {/* Position Distribution Bar */}
        {sum && posTotal > 0 && (
          <div className="bg-slate-800/50 border border-slate-700/50 rounded-xl p-4">
            <p className="text-xs text-slate-500 mb-3 font-medium uppercase tracking-wider">Distribution Position Concurrentielle</p>
            <div className="flex h-3 rounded-full overflow-hidden gap-0.5">
              {positions.map((p) => {
                const cnt = sum.position_counts[p] ?? 0;
                if (!cnt) return null;
                const pct = (cnt / posTotal) * 100;
                const colors: Record<string, string> = { dominant: "bg-emerald-500", strong: "bg-blue-500", competitive: "bg-yellow-500", weak: "bg-red-500" };
                return <div key={p} className={`${colors[p]} transition-all`} style={{ width: `${pct}%` }} title={`${POSITION_META[p]?.label}: ${cnt}`} />;
              })}
            </div>
            <div className="flex flex-wrap gap-4 mt-3">
              {positions.map((p) => {
                const cnt = sum.position_counts[p] ?? 0;
                if (!cnt) return null;
                const pm = POSITION_META[p];
                return (
                  <div key={p} className="flex items-center gap-1.5">
                    <span className={`w-2 h-2 rounded-full ${pm.dot}`} />
                    <span className="text-xs text-slate-400">{pm.label}: <span className="font-semibold text-slate-200">{cnt}</span></span>
                  </div>
                );
              })}
            </div>
          </div>
        )}

        {/* Filters */}
        <div className="flex flex-wrap gap-3">
          <div className="flex items-center gap-2 flex-wrap">
            <span className="text-xs text-slate-500 font-medium">Position:</span>
            {["", ...positions].map((p) => (
              <button key={p} onClick={() => setPositionFilter(p)}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium border transition-colors ${positionFilter === p ? "bg-indigo-600 border-indigo-500 text-white" : "bg-slate-800/50 border-slate-700 text-slate-400 hover:text-slate-200"}`}>
                {p === "" ? "Tous" : POSITION_META[p]?.label ?? p}
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

        {/* Competitors Grid */}
        {loading ? (
          <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
            {Array.from({ length: 6 }).map((_, i) => (
              <div key={i} className="bg-slate-800/30 border border-slate-700/30 rounded-xl h-36 animate-pulse" />
            ))}
          </div>
        ) : competitors.length === 0 ? (
          <div className="text-center py-20 text-slate-500">Aucun concurrent correspondant aux filtres sélectionnés</div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
            {competitors.map((c) => (
              <CompetitorCard key={c.competitor} comp={c} onClick={() => setSelected(c)} />
            ))}
          </div>
        )}
      </div>

      {selected && <CompetitorModal comp={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
