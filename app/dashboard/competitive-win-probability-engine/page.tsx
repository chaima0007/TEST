"use client";

import { useState, useEffect, useRef } from "react";

interface DealData {
  deal_id: string;
  deal_name: string;
  rep_id: string;
  competitor_name: string;
  win_probability_tier: string;
  win_risk: string;
  primary_win_factor: string;
  recommended_action: string;
  champion_score: number;
  competitive_position_score: number;
  relationship_momentum_score: number;
  deal_strength_score: number;
  win_probability_pct: number;
  is_at_risk: boolean;
  requires_executive_intervention: boolean;
  estimated_win_value_usd: number;
  win_signal: string;
  deal_value_usd: number;
}

interface Summary {
  total: number;
  tier_counts: Record<string, number>;
  risk_counts: Record<string, number>;
  factor_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_win_probability_pct: number;
  at_risk_count: number;
  executive_intervention_count: number;
  avg_champion_score: number;
  avg_competitive_position_score: number;
  avg_relationship_momentum_score: number;
  avg_deal_strength_score: number;
  total_weighted_pipeline_usd: number;
}

const TIER_BG: Record<string, string> = {
  very_likely:   "bg-emerald-500/20 border-emerald-500/30 text-emerald-300",
  likely:        "bg-sky-500/20 border-sky-500/30 text-sky-300",
  toss_up:       "bg-amber-500/20 border-amber-500/30 text-amber-300",
  unlikely:      "bg-orange-500/20 border-orange-500/30 text-orange-300",
  very_unlikely: "bg-rose-500/20 border-rose-500/30 text-rose-300",
};
const TIER_COLOR: Record<string, string> = {
  very_likely:   "#34d399",
  likely:        "#38bdf8",
  toss_up:       "#fbbf24",
  unlikely:      "#f97316",
  very_unlikely: "#f87171",
};
const RISK_BG: Record<string, string> = {
  low:      "bg-emerald-500/15 text-emerald-300",
  moderate: "bg-amber-500/15 text-amber-300",
  high:     "bg-orange-500/15 text-orange-300",
  critical: "bg-rose-500/15 text-rose-300",
};

function fmt(n: number) {
  return n >= 1_000_000
    ? `$${(n / 1_000_000).toFixed(1)}M`
    : n >= 1_000
    ? `$${(n / 1_000).toFixed(0)}K`
    : `$${n}`;
}

function WinRing({ pct, color, size = 80 }: { pct: number; color: string; size?: number }) {
  const r = size * 0.38;
  const circ = 2 * Math.PI * r;
  const fill = (pct / 100) * circ;
  return (
    <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`}>
      <circle cx={size / 2} cy={size / 2} r={r} fill="none" stroke="#1e293b" strokeWidth={size * 0.1} />
      <circle
        cx={size / 2} cy={size / 2} r={r} fill="none"
        stroke={color} strokeWidth={size * 0.1}
        strokeDasharray={`${fill} ${circ - fill}`}
        strokeLinecap="round"
        transform={`rotate(-90 ${size / 2} ${size / 2})`}
      />
      <text x={size / 2} y={size / 2} textAnchor="middle" fill={color} fontSize={size * 0.18} fontWeight="bold">
        {pct.toFixed(0)}%
      </text>
    </svg>
  );
}

function DetailModal({ deal, onClose }: { deal: DealData; onClose: () => void }) {
  const [tab, setTab] = useState(0);
  const backdrop = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handler = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [onClose]);

  const color = TIER_COLOR[deal.win_probability_tier] ?? "#94a3b8";

  return (
    <div
      ref={backdrop}
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm"
      onClick={(e) => { if (e.target === backdrop.current) onClose(); }}
    >
      <div className="relative w-full max-w-2xl rounded-2xl border border-slate-700 bg-slate-900 shadow-2xl mx-4">
        <button onClick={onClose} className="absolute top-4 right-4 text-slate-400 hover:text-white transition-colors text-xl font-bold">✕</button>

        <div className="p-6 border-b border-slate-800">
          <div className="flex items-center gap-4">
            <WinRing pct={deal.win_probability_pct} color={color} size={80} />
            <div>
              <h2 className="text-xl font-bold text-slate-100">{deal.deal_name}</h2>
              <p className="text-slate-400 text-sm mt-0.5">vs {deal.competitor_name} · {fmt(deal.deal_value_usd)}</p>
              <div className="flex gap-2 mt-2 flex-wrap">
                <span className={`px-2 py-0.5 rounded-full border text-xs font-semibold uppercase tracking-wide ${TIER_BG[deal.win_probability_tier]}`}>
                  {deal.win_probability_tier.replace(/_/g, " ")}
                </span>
                <span className={`px-2 py-0.5 rounded-full text-xs font-semibold ${RISK_BG[deal.win_risk]}`}>
                  {deal.win_risk} risk
                </span>
              </div>
              {(deal.is_at_risk || deal.requires_executive_intervention) && (
                <div className="flex gap-2 mt-2">
                  {deal.is_at_risk && <span className="px-2 py-0.5 rounded-full bg-rose-500/20 text-rose-300 text-xs font-semibold">AT RISK</span>}
                  {deal.requires_executive_intervention && <span className="px-2 py-0.5 rounded-full bg-violet-500/20 text-violet-300 text-xs font-semibold">EXEC NEEDED</span>}
                </div>
              )}
            </div>
          </div>
        </div>

        <div className="flex border-b border-slate-800">
          {["Win Factors", "Deal Analysis", "Action Plan"].map((t, i) => (
            <button
              key={t} onClick={() => setTab(i)}
              className={`flex-1 px-4 py-3 text-sm font-medium transition-colors ${tab === i ? "text-indigo-400 border-b-2 border-indigo-400" : "text-slate-500 hover:text-slate-300"}`}
            >{t}</button>
          ))}
        </div>

        <div className="p-6">
          {tab === 0 && (
            <div className="grid grid-cols-2 gap-4">
              {[
                { label: "Champion Strength", value: deal.champion_score, color: "#818cf8" },
                { label: "Competitive Position", value: deal.competitive_position_score, color: "#34d399" },
                { label: "Relationship Momentum", value: deal.relationship_momentum_score, color: "#38bdf8" },
                { label: "Deal Strength", value: deal.deal_strength_score, color: "#fbbf24" },
              ].map(({ label, value, color }) => (
                <div key={label} className="bg-slate-800/50 rounded-xl p-4">
                  <p className="text-slate-400 text-xs mb-2">{label}</p>
                  <div className="flex items-center gap-3">
                    <div className="flex-1 h-2 bg-slate-700 rounded-full overflow-hidden">
                      <div className="h-full rounded-full" style={{ width: `${value}%`, backgroundColor: color }} />
                    </div>
                    <span className="text-slate-200 text-sm font-bold w-10 text-right">{value.toFixed(1)}</span>
                  </div>
                </div>
              ))}
              <div className="col-span-2 bg-slate-800/30 rounded-xl p-4">
                <p className="text-slate-400 text-xs mb-1">Win Signal</p>
                <p className="text-slate-200 text-sm">{deal.win_signal}</p>
              </div>
            </div>
          )}
          {tab === 1 && (
            <div className="space-y-3">
              <div className="grid grid-cols-2 gap-3">
                <div className="bg-slate-800/50 rounded-xl p-4 text-center">
                  <p className="text-slate-400 text-xs mb-1">Deal Value</p>
                  <p className="text-slate-100 text-lg font-bold">{fmt(deal.deal_value_usd)}</p>
                </div>
                <div className="bg-slate-800/50 rounded-xl p-4 text-center">
                  <p className="text-slate-400 text-xs mb-1">Weighted Value</p>
                  <p style={{ color: TIER_COLOR[deal.win_probability_tier] }} className="text-lg font-bold">
                    {fmt(deal.estimated_win_value_usd)}
                  </p>
                </div>
              </div>
              <div className="bg-slate-800/30 rounded-xl p-4 space-y-2">
                <div className="flex justify-between text-sm">
                  <span className="text-slate-400">Competitor</span>
                  <span className="text-slate-200 font-semibold">{deal.competitor_name}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-slate-400">Primary Win Factor</span>
                  <span className="text-slate-200 font-semibold capitalize">{deal.primary_win_factor}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-slate-400">At Risk</span>
                  <span className={deal.is_at_risk ? "text-rose-400 font-semibold" : "text-slate-500"}>
                    {deal.is_at_risk ? "YES" : "No"}
                  </span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-slate-400">Exec Intervention</span>
                  <span className={deal.requires_executive_intervention ? "text-violet-400 font-semibold" : "text-slate-500"}>
                    {deal.requires_executive_intervention ? "YES" : "No"}
                  </span>
                </div>
              </div>
            </div>
          )}
          {tab === 2 && (
            <div className="space-y-4">
              <div className="bg-indigo-500/10 border border-indigo-500/20 rounded-xl p-4">
                <p className="text-indigo-400 text-xs font-semibold uppercase tracking-wide mb-2">Recommended Action</p>
                <p className="text-slate-200 font-semibold text-base">
                  {deal.recommended_action.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase())}
                </p>
              </div>
              <div className="bg-slate-800/30 rounded-xl p-4 space-y-2">
                <div className="flex justify-between text-sm">
                  <span className="text-slate-400">Win Probability</span>
                  <span className="font-bold text-lg" style={{ color: TIER_COLOR[deal.win_probability_tier] }}>
                    {deal.win_probability_pct.toFixed(1)}%
                  </span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-slate-400">Win Risk</span>
                  <span className="text-slate-200 font-semibold">{deal.win_risk.toUpperCase()}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-slate-400">Win Tier</span>
                  <span className="text-slate-200 font-semibold">{deal.win_probability_tier.replace(/_/g, " ")}</span>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default function CompetitiveWinPage() {
  const [data, setData] = useState<{ deals: DealData[]; summary: Summary } | null>(null);
  const [loading, setLoading] = useState(true);
  const [tierFilter, setTierFilter] = useState<string>("all");
  const [riskFilter, setRiskFilter] = useState<string>("all");
  const [selected, setSelected] = useState<DealData | null>(null);

  useEffect(() => {
    async function load() {
        setLoading(true);
        try {
          const params = new URLSearchParams();
          if (tierFilter !== "all") params.set("tier", tierFilter);
          if (riskFilter !== "all") params.set("risk", riskFilter);
          const res = await fetch(`/api/competitive-win-probability-engine?${params}`);
          setData(await res.json());
        } finally {
          setLoading(false);
        }
  }
    load();
  }, [tierFilter, riskFilter]);

  const s = data?.summary;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
      <div className="max-w-7xl mx-auto space-y-6">

        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-slate-100">Competitive Win Probability Engine</h1>
            <p className="text-slate-400 mt-1">Real-time win probability scoring vs specific competitors</p>
          </div>
          <button onClick={load} className="px-4 py-2 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white text-sm font-medium transition-colors">
            Refresh
          </button>
        </div>

        {s && (
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
            {[
              { label: "Avg Win Probability", value: `${s.avg_win_probability_pct.toFixed(1)}%`, sub: "across all deals", color: "text-indigo-400" },
              { label: "At Risk Deals", value: s.at_risk_count, sub: `of ${s.total} deals`, color: "text-rose-400" },
              { label: "Exec Intervention Needed", value: s.executive_intervention_count, sub: `of ${s.total} deals`, color: "text-violet-400" },
              { label: "Weighted Pipeline", value: s.total_weighted_pipeline_usd >= 1_000_000 ? `$${(s.total_weighted_pipeline_usd / 1_000_000).toFixed(1)}M` : `$${(s.total_weighted_pipeline_usd / 1000).toFixed(0)}K`, sub: "risk-adjusted", color: "text-emerald-400" },
            ].map(({ label, value, sub, color }) => (
              <div key={label} className="bg-slate-900 border border-slate-800 rounded-2xl p-4">
                <p className="text-slate-400 text-xs mb-1">{label}</p>
                <p className={`text-2xl font-bold ${color}`}>{value}</p>
                <p className="text-slate-500 text-xs mt-1">{sub}</p>
              </div>
            ))}
          </div>
        )}

        {s && (
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5">
            <h2 className="text-sm font-semibold text-slate-400 uppercase tracking-wide mb-4">Average Score Breakdown</h2>
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
              {[
                { label: "Champion Strength", value: s.avg_champion_score, color: "#818cf8" },
                { label: "Competitive Position", value: s.avg_competitive_position_score, color: "#34d399" },
                { label: "Relationship Momentum", value: s.avg_relationship_momentum_score, color: "#38bdf8" },
                { label: "Deal Strength", value: s.avg_deal_strength_score, color: "#fbbf24" },
              ].map(({ label, value, color }) => (
                <div key={label} className="flex flex-col items-center gap-2">
                  <WinRing pct={value} color={color} size={72} />
                  <p className="text-slate-400 text-xs text-center">{label}</p>
                </div>
              ))}
            </div>
          </div>
        )}

        {s && (
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5">
            <h2 className="text-sm font-semibold text-slate-400 uppercase tracking-wide mb-3">Win Probability Distribution</h2>
            <div className="flex h-5 rounded-full overflow-hidden gap-0.5">
              {(["very_likely", "likely", "toss_up", "unlikely", "very_unlikely"] as const).map((t) => {
                const pct = ((s.tier_counts[t] || 0) / s.total) * 100;
                const cols: Record<string, string> = { very_likely: "bg-emerald-500", likely: "bg-sky-500", toss_up: "bg-amber-500", unlikely: "bg-orange-500", very_unlikely: "bg-rose-500" };
                return pct > 0 ? (
                  <div key={t} style={{ width: `${pct}%` }} className={`${cols[t]} relative group`}>
                    <div className="absolute bottom-full mb-1 left-1/2 -translate-x-1/2 bg-slate-800 text-xs rounded px-2 py-1 whitespace-nowrap opacity-0 group-hover:opacity-100 transition-opacity z-10">
                      {t.replace(/_/g, " ")}: {s.tier_counts[t]}
                    </div>
                  </div>
                ) : null;
              })}
            </div>
            <div className="flex flex-wrap gap-3 mt-3">
              {(["very_likely", "likely", "toss_up", "unlikely", "very_unlikely"] as const).map((t) => {
                const dot: Record<string, string> = { very_likely: "bg-emerald-500", likely: "bg-sky-500", toss_up: "bg-amber-500", unlikely: "bg-orange-500", very_unlikely: "bg-rose-500" };
                return (
                  <div key={t} className="flex items-center gap-1.5">
                    <div className={`w-2.5 h-2.5 rounded-full ${dot[t]}`} />
                    <span className="text-slate-400 text-xs">{t.replace(/_/g, " ")} ({s.tier_counts[t] || 0})</span>
                  </div>
                );
              })}
            </div>
          </div>
        )}

        <div className="flex flex-wrap gap-3">
          <div className="flex gap-1 bg-slate-900 border border-slate-800 rounded-xl p-1 flex-wrap">
            {["all", "very_likely", "likely", "toss_up", "unlikely", "very_unlikely"].map((t) => (
              <button
                key={t} onClick={() => setTierFilter(t)}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${tierFilter === t ? "bg-indigo-600 text-white" : "text-slate-400 hover:text-slate-200"}`}
              >
                {t === "all" ? "All Tiers" : t.replace(/_/g, " ")}
              </button>
            ))}
          </div>
          <div className="flex gap-1 bg-slate-900 border border-slate-800 rounded-xl p-1">
            {["all", "low", "moderate", "high", "critical"].map((r) => (
              <button
                key={r} onClick={() => setRiskFilter(r)}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${riskFilter === r ? "bg-indigo-600 text-white" : "text-slate-400 hover:text-slate-200"}`}
              >
                {r === "all" ? "All Risk" : r}
              </button>
            ))}
          </div>
        </div>

        {loading ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {Array.from({ length: 8 }).map((_, i) => (
              <div key={i} className="bg-slate-900 border border-slate-800 rounded-2xl p-5 animate-pulse h-52" />
            ))}
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {(data?.deals ?? []).map((deal) => {
              const color = TIER_COLOR[deal.win_probability_tier] ?? "#94a3b8";
              return (
                <button
                  key={deal.deal_id}
                  onClick={() => setSelected(deal)}
                  className="bg-slate-900 border border-slate-800 rounded-2xl p-5 text-left hover:border-indigo-500/50 transition-all hover:bg-slate-800/50 group"
                >
                  <div className="flex items-center justify-between mb-3">
                    <div className="flex-1 min-w-0 mr-2">
                      <p className="text-slate-100 font-semibold text-sm truncate">{deal.deal_name}</p>
                      <p className="text-slate-400 text-xs">vs {deal.competitor_name}</p>
                    </div>
                    <WinRing pct={deal.win_probability_pct} color={color} size={56} />
                  </div>
                  <div className="flex flex-wrap gap-1.5 mb-3">
                    <span className={`px-2 py-0.5 rounded-full border text-xs font-semibold ${TIER_BG[deal.win_probability_tier]}`}>
                      {deal.win_probability_tier.replace(/_/g, " ")}
                    </span>
                    <span className={`px-2 py-0.5 rounded-full text-xs font-semibold ${RISK_BG[deal.win_risk]}`}>
                      {deal.win_risk}
                    </span>
                  </div>
                  {(deal.is_at_risk || deal.requires_executive_intervention) && (
                    <div className="flex gap-1 mb-2 flex-wrap">
                      {deal.is_at_risk && <span className="px-1.5 py-0.5 rounded bg-rose-500/20 text-rose-300 text-xs">At Risk</span>}
                      {deal.requires_executive_intervention && <span className="px-1.5 py-0.5 rounded bg-violet-500/20 text-violet-300 text-xs">Exec Needed</span>}
                    </div>
                  )}
                  <div className="flex justify-between text-xs text-slate-400 mb-1">
                    <span>{fmt(deal.deal_value_usd)}</span>
                    <span className="text-emerald-400">W: {fmt(deal.estimated_win_value_usd)}</span>
                  </div>
                  <p className="text-slate-500 text-xs line-clamp-2 group-hover:text-slate-400 transition-colors mt-1">
                    {deal.win_signal}
                  </p>
                </button>
              );
            })}
          </div>
        )}
      </div>

      {selected && <DetailModal deal={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
