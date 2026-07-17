"use client";

import { useState, useEffect, useRef } from "react";

interface RepData {
  rep_id: string;
  rep_name: string;
  region: string;
  fairness_rating: string;
  fairness_risk: string;
  bias_direction: string;
  quota_action: string;
  market_alignment_score: number;
  experience_alignment_score: number;
  peer_equity_score: number;
  attainment_sustainability_score: number;
  fairness_composite: number;
  is_over_quoted: boolean;
  is_under_quoted: boolean;
  estimated_fair_quota_usd: number;
  fairness_signal: string;
  annual_quota_usd: number;
}

interface Summary {
  total: number;
  fairness_counts: Record<string, number>;
  risk_counts: Record<string, number>;
  bias_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_fairness_composite: number;
  over_quoted_count: number;
  under_quoted_count: number;
  avg_market_alignment_score: number;
  avg_experience_alignment_score: number;
  avg_peer_equity_score: number;
  avg_attainment_sustainability_score: number;
  total_quota_adjustment_opportunity_usd: number;
}

const RATING_COLOR: Record<string, string> = {
  very_fair:    "text-emerald-400",
  fair:         "text-sky-400",
  questionable: "text-amber-400",
  unfair:       "text-rose-400",
};
const RATING_BG: Record<string, string> = {
  very_fair:    "bg-emerald-500/20 border-emerald-500/30 text-emerald-300",
  fair:         "bg-sky-500/20 border-sky-500/30 text-sky-300",
  questionable: "bg-amber-500/20 border-amber-500/30 text-amber-300",
  unfair:       "bg-rose-500/20 border-rose-500/30 text-rose-300",
};
const RISK_BG: Record<string, string> = {
  low:      "bg-emerald-500/15 text-emerald-300",
  moderate: "bg-amber-500/15 text-amber-300",
  high:     "bg-orange-500/15 text-orange-300",
  critical: "bg-rose-500/15 text-rose-300",
};
const BIAS_BG: Record<string, string> = {
  balanced:     "bg-slate-700/50 text-slate-300",
  over_quoted:  "bg-rose-500/15 text-rose-300",
  under_quoted: "bg-violet-500/15 text-violet-300",
};
const GAUGE_COLOR: Record<string, string> = {
  very_fair:    "#34d399",
  fair:         "#38bdf8",
  questionable: "#fbbf24",
  unfair:       "#f87171",
};

function fmt(n: number) {
  return n >= 1_000_000
    ? `$${(n / 1_000_000).toFixed(1)}M`
    : n >= 1_000
    ? `$${(n / 1_000).toFixed(0)}K`
    : `$${n}`;
}

function Ring({ value, color, size = 80 }: { value: number; color: string; size?: number }) {
  const r = size * 0.38;
  const circ = 2 * Math.PI * r;
  const fill = (value / 100) * circ;
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
      <text x={size / 2} y={size / 2 + 5} textAnchor="middle" fill={color} fontSize={size * 0.2} fontWeight="bold">
        {value.toFixed(0)}
      </text>
    </svg>
  );
}

function DetailModal({ rep, onClose }: { rep: RepData; onClose: () => void }) {
  const [tab, setTab] = useState(0);
  const backdrop = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handler = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [onClose]);

  const color = GAUGE_COLOR[rep.fairness_rating] ?? "#94a3b8";

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
            <Ring value={rep.fairness_composite} color={color} size={72} />
            <div>
              <h2 className="text-xl font-bold text-slate-100">{rep.rep_name}</h2>
              <p className="text-slate-400 text-sm mt-0.5">{rep.region}</p>
              <div className="flex gap-2 mt-2 flex-wrap">
                <span className={`px-2 py-0.5 rounded-full border text-xs font-semibold uppercase tracking-wide ${RATING_BG[rep.fairness_rating]}`}>
                  {rep.fairness_rating.replace("_", " ")}
                </span>
                <span className={`px-2 py-0.5 rounded-full text-xs font-semibold uppercase tracking-wide ${BIAS_BG[rep.bias_direction]}`}>
                  {rep.bias_direction.replace("_", " ")}
                </span>
                {rep.is_over_quoted && (
                  <span className="px-2 py-0.5 rounded-full bg-rose-500/20 text-rose-300 text-xs font-semibold">OVER-QUOTED</span>
                )}
                {rep.is_under_quoted && (
                  <span className="px-2 py-0.5 rounded-full bg-violet-500/20 text-violet-300 text-xs font-semibold">UNDER-QUOTED</span>
                )}
              </div>
            </div>
          </div>
        </div>

        <div className="flex border-b border-slate-800">
          {["Scores", "Quota Analysis", "Action"].map((t, i) => (
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
                { label: "Market Alignment", value: rep.market_alignment_score },
                { label: "Experience Alignment", value: rep.experience_alignment_score },
                { label: "Peer Equity", value: rep.peer_equity_score },
                { label: "Attainment Sustainability", value: rep.attainment_sustainability_score },
              ].map(({ label, value }) => (
                <div key={label} className="bg-slate-800/50 rounded-xl p-4">
                  <p className="text-slate-400 text-xs mb-2">{label}</p>
                  <div className="flex items-center gap-3">
                    <div className="flex-1 h-2 bg-slate-700 rounded-full overflow-hidden">
                      <div className="h-full rounded-full bg-indigo-500" style={{ width: `${value}%` }} />
                    </div>
                    <span className="text-slate-200 text-sm font-bold w-10 text-right">{value.toFixed(1)}</span>
                  </div>
                </div>
              ))}
              <div className="col-span-2 bg-slate-800/30 rounded-xl p-4">
                <p className="text-slate-400 text-xs mb-1">Fairness Signal</p>
                <p className="text-slate-200 text-sm">{rep.fairness_signal}</p>
              </div>
            </div>
          )}
          {tab === 1 && (
            <div className="space-y-3">
              <div className="grid grid-cols-2 gap-3">
                <div className="bg-slate-800/50 rounded-xl p-4">
                  <p className="text-slate-400 text-xs mb-1">Current Quota</p>
                  <p className="text-slate-100 text-lg font-bold">{fmt(rep.annual_quota_usd)}</p>
                </div>
                <div className="bg-slate-800/50 rounded-xl p-4">
                  <p className="text-slate-400 text-xs mb-1">Estimated Fair Quota</p>
                  <p className="text-emerald-400 text-lg font-bold">{fmt(rep.estimated_fair_quota_usd)}</p>
                </div>
              </div>
              <div className="bg-slate-800/50 rounded-xl p-4">
                <p className="text-slate-400 text-xs mb-2">Quota Gap</p>
                <p className={`text-base font-bold ${rep.annual_quota_usd > rep.estimated_fair_quota_usd ? "text-rose-400" : "text-violet-400"}`}>
                  {rep.annual_quota_usd > rep.estimated_fair_quota_usd ? "+" : ""}
                  {fmt(rep.annual_quota_usd - rep.estimated_fair_quota_usd)} vs fair estimate
                </p>
              </div>
              <div className="grid grid-cols-3 gap-3">
                <div className={`rounded-xl p-3 text-center ${RISK_BG[rep.fairness_risk]}`}>
                  <p className="text-xs opacity-70 mb-1">Risk</p>
                  <p className="text-sm font-bold uppercase">{rep.fairness_risk}</p>
                </div>
                <div className={`rounded-xl p-3 text-center ${BIAS_BG[rep.bias_direction]}`}>
                  <p className="text-xs opacity-70 mb-1">Bias</p>
                  <p className="text-sm font-bold">{rep.bias_direction.replace("_", " ")}</p>
                </div>
                <div className="rounded-xl p-3 text-center bg-slate-800/50">
                  <p className="text-xs text-slate-400 mb-1">Composite</p>
                  <p className="text-sm font-bold text-slate-100">{rep.fairness_composite.toFixed(1)}</p>
                </div>
              </div>
            </div>
          )}
          {tab === 2 && (
            <div className="space-y-4">
              <div className="bg-indigo-500/10 border border-indigo-500/20 rounded-xl p-4">
                <p className="text-indigo-400 text-xs font-semibold uppercase tracking-wide mb-2">Recommended Action</p>
                <p className="text-slate-200 font-semibold text-base">
                  {rep.quota_action.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase())}
                </p>
              </div>
              <div className="bg-slate-800/30 rounded-xl p-4 space-y-2">
                <div className="flex justify-between text-sm">
                  <span className="text-slate-400">Fairness Rating</span>
                  <span className={`font-semibold ${RATING_COLOR[rep.fairness_rating]}`}>{rep.fairness_rating.replace("_", " ").toUpperCase()}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-slate-400">Risk Level</span>
                  <span className="text-slate-200 font-semibold">{rep.fairness_risk.toUpperCase()}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-slate-400">Over-Quoted Flag</span>
                  <span className={rep.is_over_quoted ? "text-rose-400 font-semibold" : "text-slate-500"}>
                    {rep.is_over_quoted ? "YES" : "No"}
                  </span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-slate-400">Under-Quoted Flag</span>
                  <span className={rep.is_under_quoted ? "text-violet-400 font-semibold" : "text-slate-500"}>
                    {rep.is_under_quoted ? "YES" : "No"}
                  </span>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default function QuotaFairnessPage() {
  const [data, setData] = useState<{ reps: RepData[]; summary: Summary } | null>(null);
  const [loading, setLoading] = useState(true);
  const [ratingFilter, setRatingFilter] = useState<string>("all");
  const [biasFilter, setBiasFilter] = useState<string>("all");
  const [selected, setSelected] = useState<RepData | null>(null);

  async function load() {
      setLoading(true);
      try {
        const params = new URLSearchParams();
        if (ratingFilter !== "all") params.set("rating", ratingFilter);
        if (biasFilter !== "all") params.set("bias", biasFilter);
        const res = await fetch(`/api/quota-fairness-engine?${params}`);
        setData(await res.json());
      } finally {
        setLoading(false);
      }
  }

  useEffect(() => {
    load();
  }, [ratingFilter, biasFilter]);

  const s = data?.summary;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
      <div className="max-w-7xl mx-auto space-y-6">

        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-slate-100">Quota Fairness Engine</h1>
            <p className="text-slate-400 mt-1">Equity analysis across territory, experience, and peer benchmarks</p>
          </div>
          <button onClick={load} className="px-4 py-2 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white text-sm font-medium transition-colors">
            Refresh
          </button>
        </div>

        {/* KPI Strip */}
        {s && (
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
            {[
              { label: "Avg Fairness Score", value: s.avg_fairness_composite.toFixed(1), sub: "composite", color: "text-indigo-400" },
              { label: "Over-Quoted Reps", value: s.over_quoted_count, sub: `of ${s.total} reps`, color: "text-rose-400" },
              { label: "Under-Quoted Reps", value: s.under_quoted_count, sub: `of ${s.total} reps`, color: "text-violet-400" },
              { label: "Quota Adj. Opportunity", value: fmt(s.total_quota_adjustment_opportunity_usd), sub: "total gap", color: "text-amber-400" },
            ].map(({ label, value, sub, color }) => (
              <div key={label} className="bg-slate-900 border border-slate-800 rounded-2xl p-4">
                <p className="text-slate-400 text-xs mb-1">{label}</p>
                <p className={`text-2xl font-bold ${color}`}>{value}</p>
                <p className="text-slate-500 text-xs mt-1">{sub}</p>
              </div>
            ))}
          </div>
        )}

        {/* Score Averages */}
        {s && (
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5">
            <h2 className="text-sm font-semibold text-slate-400 uppercase tracking-wide mb-4">Average Score Breakdown</h2>
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
              {[
                { label: "Market Alignment", value: s.avg_market_alignment_score, color: "#818cf8" },
                { label: "Experience Alignment", value: s.avg_experience_alignment_score, color: "#34d399" },
                { label: "Peer Equity", value: s.avg_peer_equity_score, color: "#fbbf24" },
                { label: "Attainment Sustainability", value: s.avg_attainment_sustainability_score, color: "#f472b6" },
              ].map(({ label, value, color }) => (
                <div key={label} className="flex flex-col items-center gap-2">
                  <Ring value={value} color={color} size={80} />
                  <p className="text-slate-400 text-xs text-center">{label}</p>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Distribution */}
        {s && (
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5">
            <h2 className="text-sm font-semibold text-slate-400 uppercase tracking-wide mb-3">Fairness Distribution</h2>
            <div className="flex h-5 rounded-full overflow-hidden gap-0.5">
              {(["very_fair", "fair", "questionable", "unfair"] as const).map((r) => {
                const pct = ((s.fairness_counts[r] || 0) / s.total) * 100;
                const colors: Record<string, string> = { very_fair: "bg-emerald-500", fair: "bg-sky-500", questionable: "bg-amber-500", unfair: "bg-rose-500" };
                return pct > 0 ? (
                  <div key={r} style={{ width: `${pct}%` }} className={`${colors[r]} relative group`}>
                    <div className="absolute bottom-full mb-1 left-1/2 -translate-x-1/2 bg-slate-800 text-xs rounded px-2 py-1 whitespace-nowrap opacity-0 group-hover:opacity-100 transition-opacity z-10">
                      {r.replace("_", " ")}: {s.fairness_counts[r]}
                    </div>
                  </div>
                ) : null;
              })}
            </div>
            <div className="flex flex-wrap gap-3 mt-3">
              {(["very_fair", "fair", "questionable", "unfair"] as const).map((r) => {
                const dot: Record<string, string> = { very_fair: "bg-emerald-500", fair: "bg-sky-500", questionable: "bg-amber-500", unfair: "bg-rose-500" };
                return (
                  <div key={r} className="flex items-center gap-1.5">
                    <div className={`w-2.5 h-2.5 rounded-full ${dot[r]}`} />
                    <span className="text-slate-400 text-xs">{r.replace("_", " ")} ({s.fairness_counts[r] || 0})</span>
                  </div>
                );
              })}
            </div>
          </div>
        )}

        {/* Filters */}
        <div className="flex flex-wrap gap-3">
          <div className="flex gap-1 bg-slate-900 border border-slate-800 rounded-xl p-1">
            {["all", "very_fair", "fair", "questionable", "unfair"].map((r) => (
              <button
                key={r}
                onClick={() => setRatingFilter(r)}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${ratingFilter === r ? "bg-indigo-600 text-white" : "text-slate-400 hover:text-slate-200"}`}
              >
                {r === "all" ? "All Ratings" : r.replace("_", " ")}
              </button>
            ))}
          </div>
          <div className="flex gap-1 bg-slate-900 border border-slate-800 rounded-xl p-1">
            {["all", "balanced", "over_quoted", "under_quoted"].map((b) => (
              <button
                key={b}
                onClick={() => setBiasFilter(b)}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${biasFilter === b ? "bg-indigo-600 text-white" : "text-slate-400 hover:text-slate-200"}`}
              >
                {b === "all" ? "All Bias" : b.replace("_", " ")}
              </button>
            ))}
          </div>
        </div>

        {/* Rep Cards */}
        {loading ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {Array.from({ length: 8 }).map((_, i) => (
              <div key={i} className="bg-slate-900 border border-slate-800 rounded-2xl p-5 animate-pulse h-52" />
            ))}
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {(data?.reps ?? []).map((rep) => {
              const color = GAUGE_COLOR[rep.fairness_rating] ?? "#94a3b8";
              return (
                <button
                  key={rep.rep_id}
                  onClick={() => setSelected(rep)}
                  className="bg-slate-900 border border-slate-800 rounded-2xl p-5 text-left hover:border-indigo-500/50 transition-all hover:bg-slate-800/50 group"
                >
                  <div className="flex items-center justify-between mb-3">
                    <div>
                      <p className="text-slate-100 font-semibold text-sm">{rep.rep_name}</p>
                      <p className="text-slate-400 text-xs">{rep.region}</p>
                    </div>
                    <Ring value={rep.fairness_composite} color={color} size={52} />
                  </div>
                  <div className="flex flex-wrap gap-1.5 mb-3">
                    <span className={`px-2 py-0.5 rounded-full border text-xs font-semibold ${RATING_BG[rep.fairness_rating]}`}>
                      {rep.fairness_rating.replace("_", " ")}
                    </span>
                    <span className={`px-2 py-0.5 rounded-full text-xs font-semibold ${BIAS_BG[rep.bias_direction]}`}>
                      {rep.bias_direction.replace("_", " ")}
                    </span>
                  </div>
                  {(rep.is_over_quoted || rep.is_under_quoted) && (
                    <div className={`text-xs font-semibold px-2 py-1 rounded-lg mb-2 ${rep.is_over_quoted ? "bg-rose-500/15 text-rose-300" : "bg-violet-500/15 text-violet-300"}`}>
                      {rep.is_over_quoted ? "Over-quoted — reduce quota" : "Under-quoted — increase quota"}
                    </div>
                  )}
                  <div className="flex justify-between text-xs text-slate-400">
                    <span>Quota: {fmt(rep.annual_quota_usd)}</span>
                    <span>Fair: {fmt(rep.estimated_fair_quota_usd)}</span>
                  </div>
                  <p className="text-slate-500 text-xs mt-2 line-clamp-2 group-hover:text-slate-400 transition-colors">
                    {rep.fairness_signal}
                  </p>
                </button>
              );
            })}
          </div>
        )}
      </div>

      {selected && <DetailModal rep={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
