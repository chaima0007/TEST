"use client";

import { useEffect, useState } from "react";

// ─── Types ───────────────────────────────────────────────────────────────────

type Tier = "A" | "B" | "C" | "D";

interface ScorecardData {
  prospect_id: string;
  company_name: string;
  sector: string;
  total_score: number;
  tier: Tier;
  bant_score: number;
  behavioral_score: number;
  temporal_score: number;
  market_fit_score: number;
  dimension_breakdown: Record<string, number>;
  notes: string;
  created_at: string;
}

interface Summary {
  total: number;
  tier_A: number;
  tier_B: number;
  tier_C: number;
  tier_D: number;
  avg_score: number;
  weakest_dimension: string;
  dimension_averages: Record<string, number>;
  sector_breakdown: Record<string, { count: number; avg_score: number }>;
}

// ─── Constants ───────────────────────────────────────────────────────────────

const TIER_META: Record<Tier, { label: string; color: string; bg: string; ring: string; description: string }> = {
  A: { label: "Tier A", color: "text-emerald-400", bg: "bg-emerald-900/40 border-emerald-700", ring: "ring-emerald-500", description: "Action immédiate" },
  B: { label: "Tier B", color: "text-blue-400", bg: "bg-blue-900/40 border-blue-700", ring: "ring-blue-500", description: "Nurture actif" },
  C: { label: "Tier C", color: "text-yellow-400", bg: "bg-yellow-900/40 border-yellow-700", ring: "ring-yellow-500", description: "Long terme" },
  D: { label: "Tier D", color: "text-slate-400", bg: "bg-slate-800 border-slate-700", ring: "ring-slate-600", description: "Déprioritiser" },
};

const DIM_META: Record<string, { label: string; max: number; color: string }> = {
  bant:        { label: "BANT",        max: 40, color: "bg-indigo-500" },
  behavioral:  { label: "Engagement",  max: 30, color: "bg-purple-500" },
  temporal:    { label: "Temporel",    max: 20, color: "bg-amber-500" },
  market_fit:  { label: "Marché",      max: 10, color: "bg-cyan-500" },
};

const DIM_LABELS: Record<string, string> = {
  bant: "BANT", behavioral: "Engagement", temporal: "Temporel", market_fit: "Marché",
};

const FILTER_TABS = [
  { key: "all", label: "Tous" },
  { key: "A", label: "Tier A" },
  { key: "B", label: "Tier B" },
  { key: "C", label: "Tier C" },
  { key: "D", label: "Tier D" },
];

// ─── Sub-components ───────────────────────────────────────────────────────────

function TierBadge({ tier }: { tier: Tier }) {
  const m = TIER_META[tier];
  return (
    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-bold border ${m.bg} ${m.color}`}>
      {m.label}
    </span>
  );
}

function ScoreRing({ score, tier }: { score: number; tier: Tier }) {
  const m = TIER_META[tier];
  const r = 18;
  const c = 2 * Math.PI * r;
  const dash = (score / 100) * c;
  const strokeColors: Record<Tier, string> = {
    A: "#10b981", B: "#3b82f6", C: "#eab308", D: "#64748b",
  };
  return (
    <div className="relative w-14 h-14 flex-shrink-0">
      <svg className="w-14 h-14 -rotate-90" viewBox="0 0 44 44">
        <circle cx="22" cy="22" r={r} fill="none" stroke="#1e293b" strokeWidth="4" />
        <circle
          cx="22" cy="22" r={r} fill="none"
          stroke={strokeColors[tier]} strokeWidth="4"
          strokeDasharray={`${dash} ${c}`}
          strokeLinecap="round"
        />
      </svg>
      <div className="absolute inset-0 flex items-center justify-center">
        <span className={`text-xs font-bold ${m.color}`}>{score}</span>
      </div>
    </div>
  );
}

function DimBar({ dim, score, max, color }: { dim: string; score: number; max: number; color: string }) {
  const pct = Math.round((score / max) * 100);
  return (
    <div className="flex items-center gap-2 text-xs">
      <span className="text-slate-500 w-20 flex-shrink-0">{DIM_LABELS[dim] ?? dim}</span>
      <div className="flex-1 bg-slate-800 rounded-full h-1.5 overflow-hidden">
        <div className={`h-1.5 rounded-full ${color}`} style={{ width: `${pct}%` }} />
      </div>
      <span className="text-slate-400 tabular-nums w-12 text-right">{score}/{max}</span>
    </div>
  );
}

function KpiCard({ label, value, sub, accent }: { label: string; value: string | number; sub?: string; accent?: string }) {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 flex flex-col gap-1">
      <p className="text-xs text-slate-500 font-medium uppercase tracking-wider">{label}</p>
      <p className={`text-2xl font-bold ${accent ?? "text-white"}`}>{value}</p>
      {sub && <p className="text-xs text-slate-500">{sub}</p>}
    </div>
  );
}

// ─── Detail Modal ─────────────────────────────────────────────────────────────

function DetailModal({ card, onClose }: { card: ScorecardData; onClose: () => void }) {
  useEffect(() => {
    const h = (e: KeyboardEvent) => e.key === "Escape" && onClose();
    window.addEventListener("keydown", h);
    return () => window.removeEventListener("keydown", h);
  }, [onClose]);

  const m = TIER_META[card.tier];

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm" onClick={onClose}>
      <div
        className={`bg-slate-900 border-2 rounded-2xl shadow-2xl w-full max-w-lg mx-4 p-6 space-y-5 ring-2 ${m.ring}`}
        onClick={(e) => e.stopPropagation()}
      >
        <div className="flex items-start gap-4">
          <ScoreRing score={card.total_score} tier={card.tier} />
          <div className="flex-1">
            <h2 className="text-white font-bold text-lg">{card.company_name}</h2>
            <p className="text-slate-400 text-sm">{card.sector} · {card.prospect_id}</p>
            <div className="mt-2">
              <TierBadge tier={card.tier} />
              <span className="ml-2 text-xs text-slate-500">{m.description}</span>
            </div>
          </div>
        </div>

        {/* Composite score */}
        <div className="bg-slate-800 rounded-xl p-4">
          <p className="text-xs text-slate-500 mb-3 uppercase tracking-wider font-semibold">Score composite</p>
          <div className="space-y-3">
            {Object.entries(DIM_META).map(([dim, meta]) => (
              <DimBar
                key={dim}
                dim={dim}
                score={card.dimension_breakdown[dim] ?? 0}
                max={meta.max}
                color={meta.color}
              />
            ))}
          </div>
        </div>

        {/* Score totals grid */}
        <div className="grid grid-cols-2 gap-3 text-sm">
          <div className="bg-slate-800/60 rounded-lg p-3">
            <p className="text-slate-500 text-xs mb-1">Score BANT</p>
            <p className="text-indigo-400 font-bold">{card.bant_score}/40</p>
          </div>
          <div className="bg-slate-800/60 rounded-lg p-3">
            <p className="text-slate-500 text-xs mb-1">Engagement</p>
            <p className="text-purple-400 font-bold">{card.behavioral_score}/30</p>
          </div>
          <div className="bg-slate-800/60 rounded-lg p-3">
            <p className="text-slate-500 text-xs mb-1">Temporel</p>
            <p className="text-amber-400 font-bold">{card.temporal_score}/20</p>
          </div>
          <div className="bg-slate-800/60 rounded-lg p-3">
            <p className="text-slate-500 text-xs mb-1">Marché</p>
            <p className="text-cyan-400 font-bold">{card.market_fit_score}/10</p>
          </div>
        </div>

        {card.notes && (
          <div className="bg-indigo-950/40 border border-indigo-900/50 rounded-lg p-3">
            <p className="text-xs text-indigo-400 font-semibold mb-1">Notes</p>
            <p className="text-slate-300 text-sm">{card.notes}</p>
          </div>
        )}

        <button
          onClick={onClose}
          className="w-full py-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 text-sm font-medium transition-colors"
        >
          Fermer
        </button>
      </div>
    </div>
  );
}

// ─── Main Page ────────────────────────────────────────────────────────────────

export default function ScorecardPage() {
  const [scorecards, setScorecards] = useState<ScorecardData[]>([]);
  const [summary, setSummary] = useState<Summary | null>(null);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState("all");
  const [selected, setSelected] = useState<ScorecardData | null>(null);

  useEffect(() => {
    setLoading(true);
    fetch("/api/scorecard")
      .then((r) => r.json())
      .then((d) => {
        setScorecards(d.scorecards ?? []);
        setSummary(d.summary ?? null);
      })
      .finally(() => setLoading(false));
  }, []);

  const filtered = filter === "all" ? scorecards : scorecards.filter((c) => c.tier === filter);

  return (
    <div className="p-6 space-y-6 text-slate-100">
      <div>
        <h1 className="text-2xl font-bold text-white">Scorecard Prospects</h1>
        <p className="text-slate-400 text-sm mt-1">
          Score composite 0–100 : BANT (40) + Engagement (30) + Temporel (20) + Marché (10)
        </p>
      </div>

      {/* KPI strip */}
      {summary && (
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
          <KpiCard label="Total" value={summary.total} />
          <KpiCard label="Tier A" value={summary.tier_A} sub="Action immédiate" accent="text-emerald-400" />
          <KpiCard label="Tier B" value={summary.tier_B} sub="Nurture actif" accent="text-blue-400" />
          <KpiCard label="Tier C" value={summary.tier_C} sub="Long terme" accent="text-yellow-400" />
          <KpiCard label="Tier D" value={summary.tier_D} sub="Déprioritiser" accent="text-slate-400" />
          <KpiCard label="Score moy." value={summary.avg_score} sub="/ 100" accent="text-indigo-400" />
        </div>
      )}

      {/* Dimension averages */}
      {summary && (
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-sm font-semibold text-slate-400 uppercase tracking-wider">
              Moyennes par dimension
            </h3>
            <span className="text-xs text-slate-500">
              Dimension faible :{" "}
              <span className="text-amber-400 font-semibold">
                {DIM_LABELS[summary.weakest_dimension] ?? summary.weakest_dimension}
              </span>
            </span>
          </div>
          <div className="space-y-3">
            {Object.entries(DIM_META).map(([dim, meta]) => {
              const avg = summary.dimension_averages[dim] ?? 0;
              const pct = Math.round((avg / meta.max) * 100);
              return (
                <div key={dim} className="flex items-center gap-3">
                  <span className="text-xs text-slate-400 w-24">{meta.label}</span>
                  <div className="flex-1 bg-slate-800 rounded-full h-2 overflow-hidden">
                    <div
                      className={`h-2 rounded-full transition-all ${meta.color}`}
                      style={{ width: `${pct}%` }}
                    />
                  </div>
                  <span className="text-xs text-slate-400 tabular-nums w-16 text-right">
                    {avg}/{meta.max} ({pct}%)
                  </span>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Filter tabs */}
      <div className="flex gap-2 flex-wrap">
        {FILTER_TABS.map((tab) => (
          <button
            key={tab.key}
            onClick={() => setFilter(tab.key)}
            className={`px-4 py-1.5 rounded-full text-sm font-medium transition-colors border ${
              filter === tab.key
                ? "bg-indigo-600 border-indigo-500 text-white"
                : "bg-slate-800 border-slate-700 text-slate-400 hover:text-white"
            }`}
          >
            {tab.label}
            {tab.key !== "all" && summary && (
              <span className="ml-1.5 opacity-70">
                {summary[`tier_${tab.key}` as keyof Summary] as number}
              </span>
            )}
            {tab.key === "all" && summary && (
              <span className="ml-1.5 opacity-70">{summary.total}</span>
            )}
          </button>
        ))}
      </div>

      {/* Cards grid */}
      {loading ? (
        <div className="text-slate-500 text-center py-16">Chargement…</div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
          {filtered.map((card) => (
            <div
              key={card.prospect_id}
              onClick={() => setSelected(card)}
              className={`bg-slate-900 border rounded-xl p-5 cursor-pointer hover:border-slate-600 transition-all space-y-4 ${
                TIER_META[card.tier].bg
              }`}
            >
              <div className="flex items-start gap-3">
                <ScoreRing score={card.total_score} tier={card.tier} />
                <div className="flex-1 min-w-0">
                  <p className="text-white font-semibold truncate">{card.company_name}</p>
                  <p className="text-slate-500 text-xs">{card.sector}</p>
                  <div className="mt-1.5">
                    <TierBadge tier={card.tier} />
                  </div>
                </div>
              </div>

              <div className="space-y-2">
                {Object.entries(DIM_META).map(([dim, meta]) => (
                  <DimBar
                    key={dim}
                    dim={dim}
                    score={card.dimension_breakdown[dim] ?? 0}
                    max={meta.max}
                    color={meta.color}
                  />
                ))}
              </div>
            </div>
          ))}
          {filtered.length === 0 && (
            <div className="col-span-full text-slate-500 text-center py-10">
              Aucun prospect dans ce tier.
            </div>
          )}
        </div>
      )}

      {/* Sector breakdown */}
      {summary && Object.keys(summary.sector_breakdown).length > 0 && (
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
          <h3 className="text-sm font-semibold text-slate-400 uppercase tracking-wider mb-4">
            Par secteur
          </h3>
          <div className="flex flex-wrap gap-3">
            {Object.entries(summary.sector_breakdown).map(([sector, data]) => (
              <div key={sector} className="bg-slate-800 border border-slate-700 rounded-lg px-4 py-3">
                <p className="text-white font-medium text-sm">{sector}</p>
                <p className="text-slate-400 text-xs">{data.count} prospect{data.count > 1 ? "s" : ""} · moy. {data.avg_score}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {selected && <DetailModal card={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
