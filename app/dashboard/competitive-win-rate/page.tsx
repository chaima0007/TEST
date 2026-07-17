"use client";

import { useEffect, useState } from "react";

interface MatchupData {
  matchup_id: string;
  our_product: string;
  competitor: string;
  segment: string;
  region: string;
  win_rate_category: string;
  competitive_risk: string;
  trend_direction: string;
  competitive_action: string;
  win_rate: number;
  win_rate_delta: number;
  deal_size_advantage: number;
  cycle_efficiency: number;
  champion_lift: number;
  competitive_score: number;
  is_at_risk: boolean;
  needs_battlecard: boolean;
  won_deals: number;
  total_deals: number;
}

interface Summary {
  total: number;
  category_counts: Record<string, number>;
  risk_counts: Record<string, number>;
  trend_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_win_rate: number;
  avg_competitive_score: number;
  avg_win_rate_delta: number;
  at_risk_count: number;
  battlecard_count: number;
  avg_deal_size_advantage: number;
  avg_cycle_efficiency: number;
  dominant_count: number;
}

const CATEGORY_COLOR: Record<string, string> = {
  dominant:    "text-emerald-400 bg-emerald-400/10 border-emerald-400/20",
  strong:      "text-sky-400 bg-sky-400/10 border-sky-400/20",
  competitive: "text-yellow-400 bg-yellow-400/10 border-yellow-400/20",
  weak:        "text-orange-400 bg-orange-400/10 border-orange-400/20",
  critical:    "text-red-400 bg-red-400/10 border-red-400/20",
};

const RISK_COLOR: Record<string, string> = {
  low:      "text-emerald-400",
  medium:   "text-yellow-400",
  high:     "text-orange-400",
  critical: "text-red-400",
};

const TREND_ICON: Record<string, string> = {
  improving: "↑",
  stable:    "→",
  declining: "↓",
  volatile:  "↕",
};

const TREND_COLOR: Record<string, string> = {
  improving: "text-emerald-400",
  stable:    "text-sky-400",
  declining: "text-red-400",
  volatile:  "text-yellow-400",
};

function WinRateArc({ rate, category }: { rate: number; category: string }) {
  const r = 38, cx = 48, cy = 48;
  const circ = 2 * Math.PI * r;
  const arc = Math.min(rate / 100, 1) * circ;
  const colorMap: Record<string, string> = {
    dominant: "#10b981", strong: "#38bdf8", competitive: "#fbbf24",
    weak: "#fb923c", critical: "#f87171",
  };
  const color = colorMap[category] || "#94a3b8";
  return (
    <svg viewBox="0 0 96 96" className="w-24 h-24">
      <circle cx={cx} cy={cy} r={r} fill="none" stroke="#1e293b" strokeWidth="8" />
      <circle cx={cx} cy={cy} r={r} fill="none" stroke={color} strokeWidth="8"
        strokeDasharray={`${arc} ${circ - arc}`} strokeLinecap="round"
        transform={`rotate(-90 ${cx} ${cy})`} />
      <text x={cx} y={cy - 4} textAnchor="middle" fill="white" fontSize="12" fontWeight="bold">
        {rate.toFixed(0)}%
      </text>
      <text x={cx} y={cy + 10} textAnchor="middle" fill="#94a3b8" fontSize="7">win rate</text>
    </svg>
  );
}

function CategoryDistBar({ counts }: { counts: Record<string, number> }) {
  const order = ["dominant", "strong", "competitive", "weak", "critical"];
  const total = Object.values(counts).reduce((a, b) => a + b, 0) || 1;
  const colors = ["#10b981", "#38bdf8", "#fbbf24", "#fb923c", "#f87171"];
  return (
    <div className="space-y-1.5">
      {order.map((k, i) => {
        const v = counts[k] || 0;
        const w = (v / total) * 100;
        return (
          <div key={k} className="flex items-center gap-2 text-xs">
            <span className="w-20 text-slate-400 capitalize text-right">{k}</span>
            <div className="flex-1 h-2 bg-slate-800 rounded-full overflow-hidden">
              <div className="h-full rounded-full" style={{ width: `${w}%`, backgroundColor: colors[i] }} />
            </div>
            <span className="w-4 text-slate-300">{v}</span>
          </div>
        );
      })}
    </div>
  );
}

function MiniBar({ value, max, color }: { value: number; max: number; color: string }) {
  return (
    <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
      <div className="h-full rounded-full" style={{ width: `${Math.min(100, Math.max(0, (value / max) * 100))}%`, backgroundColor: color }} />
    </div>
  );
}

function MatchupCard({ m, onClick }: { m: MatchupData; onClick: () => void }) {
  const cc = CATEGORY_COLOR[m.win_rate_category] || "text-slate-400 bg-slate-400/10 border-slate-400/20";
  const rc = RISK_COLOR[m.competitive_risk] || "text-slate-400";
  const tc = TREND_COLOR[m.trend_direction] || "text-slate-400";
  const ti = TREND_ICON[m.trend_direction] || "→";
  const deltaColor = m.win_rate_delta >= 0 ? "text-emerald-400" : "text-red-400";
  return (
    <button onClick={onClick}
      className="bg-slate-800/60 border border-slate-700 rounded-xl p-4 text-left hover:border-indigo-500/50 hover:bg-slate-800 transition-all w-full">
      <div className="flex items-start justify-between mb-3">
        <div>
          <div className="font-semibold text-slate-100 text-sm">{m.our_product} vs {m.competitor}</div>
          <div className="text-xs text-slate-500 mt-0.5">{m.segment} · {m.region}</div>
        </div>
        <div className="flex flex-col items-end gap-1">
          <span className={`text-xs font-medium px-2 py-0.5 rounded-full border ${cc}`}>
            {m.win_rate_category}
          </span>
          {m.needs_battlecard && (
            <span className="text-xs text-amber-400 bg-amber-400/10 px-1.5 py-0.5 rounded border border-amber-400/20">battlecard</span>
          )}
        </div>
      </div>
      <div className="flex items-center gap-4 mb-3">
        <WinRateArc rate={m.win_rate} category={m.win_rate_category} />
        <div className="flex-1 space-y-1.5">
          <div className="flex justify-between text-xs">
            <span className="text-slate-400">Delta</span>
            <span className={deltaColor}>{m.win_rate_delta >= 0 ? "+" : ""}{m.win_rate_delta.toFixed(1)}%</span>
          </div>
          <div className="flex justify-between text-xs">
            <span className="text-slate-400">Risk</span>
            <span className={rc}>{m.competitive_risk}</span>
          </div>
          <div className="flex justify-between text-xs">
            <span className="text-slate-400">Trend</span>
            <span className={tc}>{ti} {m.trend_direction}</span>
          </div>
          <div className="flex justify-between text-xs">
            <span className="text-slate-400">Deals</span>
            <span className="text-slate-200">{m.won_deals}/{m.total_deals}</span>
          </div>
        </div>
      </div>
      <div className="space-y-1">
        <div className="flex justify-between text-xs mb-0.5">
          <span className="text-slate-400">Competitive Score</span>
          <span className="text-slate-300">{m.competitive_score.toFixed(0)}</span>
        </div>
        <MiniBar value={m.competitive_score} max={100} color="#818cf8" />
        <div className="flex justify-between text-xs mb-0.5 mt-1">
          <span className="text-slate-400">Deal Size Adv.</span>
          <span className="text-slate-300">{m.deal_size_advantage.toFixed(2)}×</span>
        </div>
        <MiniBar value={m.deal_size_advantage} max={2} color="#22d3ee" />
      </div>
    </button>
  );
}

function MatchupModal({ m, onClose }: { m: MatchupData; onClose: () => void }) {
  const [tab, setTab] = useState<"win_rate" | "advantages" | "actions">("win_rate");
  useEffect(() => {
    const fn = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    document.addEventListener("keydown", fn);
    return () => document.removeEventListener("keydown", fn);
  }, [onClose]);

  const cc = CATEGORY_COLOR[m.win_rate_category] || "text-slate-400 bg-slate-400/10 border-slate-400/20";

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4"
      onClick={(e) => { if (e.target === e.currentTarget) onClose(); }}>
      <div className="absolute inset-0 bg-black/60 backdrop-blur-sm" />
      <div className="relative bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-lg shadow-2xl">
        <div className="flex items-start justify-between p-5 border-b border-slate-800">
          <div>
            <h2 className="text-lg font-bold text-white">{m.our_product} vs {m.competitor}</h2>
            <div className="flex items-center gap-2 mt-1 flex-wrap">
              <span className={`text-xs px-2 py-0.5 rounded-full border ${cc}`}>{m.win_rate_category}</span>
              <span className={`text-xs ${RISK_COLOR[m.competitive_risk]}`}>{m.competitive_risk} risk</span>
              <span className="text-xs text-slate-400">{m.segment} · {m.region}</span>
            </div>
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-white text-xl p-1">×</button>
        </div>
        <div className="flex border-b border-slate-800">
          {(["win_rate", "advantages", "actions"] as const).map((t) => (
            <button key={t} onClick={() => setTab(t)}
              className={`flex-1 py-2.5 text-xs font-medium capitalize transition-colors ${tab === t ? "text-indigo-400 border-b-2 border-indigo-400" : "text-slate-400 hover:text-slate-200"}`}>
              {t.replace("_", " ")}
            </button>
          ))}
        </div>
        <div className="p-5 max-h-96 overflow-y-auto">
          {tab === "win_rate" && (
            <div className="space-y-3">
              <div className="flex justify-center mb-4">
                <WinRateArc rate={m.win_rate} category={m.win_rate_category} />
              </div>
              {[
                ["Win Rate", `${m.win_rate.toFixed(1)}%`],
                ["Win Rate Delta", `${m.win_rate_delta >= 0 ? "+" : ""}${m.win_rate_delta.toFixed(1)}%`],
                ["Won / Total Deals", `${m.won_deals} / ${m.total_deals}`],
                ["Trend", `${TREND_ICON[m.trend_direction]} ${m.trend_direction}`],
                ["Competitive Score", `${m.competitive_score.toFixed(0)}/100`],
              ].map(([label, value]) => (
                <div key={label} className="flex justify-between text-sm border-b border-slate-800 pb-2">
                  <span className="text-slate-400">{label}</span>
                  <span className="text-slate-100 font-medium">{value}</span>
                </div>
              ))}
            </div>
          )}
          {tab === "advantages" && (
            <div className="space-y-3">
              {[
                { label: "Deal Size Advantage", value: m.deal_size_advantage, max: 2, color: "#22d3ee", fmt: `${m.deal_size_advantage.toFixed(2)}×` },
                { label: "Cycle Efficiency", value: m.cycle_efficiency, max: 2, color: "#10b981", fmt: `${m.cycle_efficiency.toFixed(2)}×` },
                { label: "Champion Lift", value: Math.max(0, m.champion_lift + 50), max: 100, color: "#818cf8", fmt: `${m.champion_lift >= 0 ? "+" : ""}${m.champion_lift.toFixed(1)}` },
              ].map((item) => (
                <div key={item.label} className="space-y-1">
                  <div className="flex justify-between text-sm">
                    <span className="text-slate-400">{item.label}</span>
                    <span className="text-slate-100 font-medium">{item.fmt}</span>
                  </div>
                  <MiniBar value={item.value} max={item.max} color={item.color} />
                </div>
              ))}
            </div>
          )}
          {tab === "actions" && (
            <div className="space-y-3">
              <div className="flex justify-between text-sm border-b border-slate-800 pb-2">
                <span className="text-slate-400">Recommended Action</span>
                <span className="text-indigo-400 font-medium capitalize">{m.competitive_action.replace(/_/g, " ")}</span>
              </div>
              <div className="flex justify-between text-sm border-b border-slate-800 pb-2">
                <span className="text-slate-400">At Risk</span>
                <span className={m.is_at_risk ? "text-red-400" : "text-emerald-400"}>{m.is_at_risk ? "Yes" : "No"}</span>
              </div>
              <div className="flex justify-between text-sm border-b border-slate-800 pb-2">
                <span className="text-slate-400">Needs Battlecard Update</span>
                <span className={m.needs_battlecard ? "text-amber-400" : "text-emerald-400"}>{m.needs_battlecard ? "Yes" : "No"}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-slate-400">Segment</span>
                <span className="text-slate-200">{m.segment} · {m.region}</span>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default function CompetitiveWinRatePage() {
  const [matchups, setMatchups] = useState<MatchupData[]>([]);
  const [summary, setSummary]   = useState<Summary | null>(null);
  const [loading, setLoading]   = useState(true);
  const [selected, setSelected] = useState<MatchupData | null>(null);
  const [filterCat, setFilterCat]   = useState("all");
  const [filterRisk, setFilterRisk] = useState("all");

  useEffect(() => {
    async function load() {
        setLoading(true);
        try {
          const params = new URLSearchParams();
          if (filterCat  !== "all") params.set("category", filterCat);
          if (filterRisk !== "all") params.set("risk", filterRisk);
          const res = await fetch(`/api/competitive-win-rate?${params}`);
          const data = await res.json();
          setMatchups(data.matchups || []);
          setSummary(data.summary || null);
        } catch {}
        setLoading(false);
  }
    load();
  }, [filterCat, filterRisk]);

  const categories = ["all", "dominant", "strong", "competitive", "weak", "critical"];
  const risks      = ["all", "low", "medium", "high", "critical"];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
      <div className="max-w-7xl mx-auto space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white">Competitive Win Rate</h1>
          <p className="text-slate-400 text-sm mt-1">Head-to-head matchup analysis, win rate trends, and competitive actions</p>
        </div>

        {summary && (
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {[
              { label: "Avg Win Rate", value: `${summary.avg_win_rate.toFixed(1)}%`, sub: `${summary.dominant_count} dominant matchups`, color: "text-sky-400" },
              { label: "Avg Score", value: summary.avg_competitive_score.toFixed(0), sub: `trend: ${summary.avg_win_rate_delta >= 0 ? "+" : ""}${summary.avg_win_rate_delta.toFixed(1)}%`, color: "text-indigo-400" },
              { label: "At Risk", value: `${summary.at_risk_count}/${summary.total}`, sub: "matchups below threshold", color: "text-red-400" },
              { label: "Battlecards", value: `${summary.battlecard_count}`, sub: "need updating", color: "text-amber-400" },
            ].map((k) => (
              <div key={k.label} className="bg-slate-800/60 border border-slate-700 rounded-xl p-4">
                <div className="text-xs text-slate-400 mb-1">{k.label}</div>
                <div className={`text-2xl font-bold ${k.color}`}>{k.value}</div>
                <div className="text-xs text-slate-500 mt-1">{k.sub}</div>
              </div>
            ))}
          </div>
        )}

        {summary && (
          <div className="bg-slate-800/60 border border-slate-700 rounded-xl p-5">
            <h2 className="text-sm font-semibold text-slate-300 mb-4">Win Rate Category Distribution</h2>
            <CategoryDistBar counts={summary.category_counts} />
          </div>
        )}

        <div className="flex flex-wrap gap-3">
          <div className="flex gap-1 bg-slate-800/60 border border-slate-700 rounded-lg p-1">
            {categories.map((c) => (
              <button key={c} onClick={() => setFilterCat(c)}
                className={`px-3 py-1.5 rounded-md text-xs font-medium transition-colors ${filterCat === c ? "bg-indigo-600 text-white" : "text-slate-400 hover:text-white"}`}>
                {c === "all" ? "All" : c}
              </button>
            ))}
          </div>
          <div className="flex gap-1 bg-slate-800/60 border border-slate-700 rounded-lg p-1">
            {risks.map((r) => (
              <button key={r} onClick={() => setFilterRisk(r)}
                className={`px-3 py-1.5 rounded-md text-xs font-medium transition-colors ${filterRisk === r ? "bg-indigo-600 text-white" : "text-slate-400 hover:text-white"}`}>
                {r === "all" ? "All Risk" : r}
              </button>
            ))}
          </div>
        </div>

        {loading ? (
          <div className="text-center text-slate-400 py-12">Loading...</div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
            {matchups.map((m) => (
              <MatchupCard key={m.matchup_id} m={m} onClick={() => setSelected(m)} />
            ))}
          </div>
        )}
      </div>
      {selected && <MatchupModal m={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
