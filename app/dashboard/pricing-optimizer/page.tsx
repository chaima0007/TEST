"use client";

import { useState, useEffect, useRef } from "react";

interface DealResult {
  deal_id: string;
  deal_name: string;
  recommended_price_eur: number;
  recommended_strategy: string;
  discount_pct: number;
  discount_risk: string;
  deal_urgency: string;
  price_score: number;
  win_probability_boost_pct: number;
  margin_pct: number;
  value_gap_eur: number;
  pricing_signals: string[];
  negotiation_tips: string[];
  risk_flags: string[];
}

interface Summary {
  total: number;
  strategy_counts: Record<string, number>;
  urgency_counts: Record<string, number>;
  avg_price_score: number;
  avg_discount_pct: number;
  avg_margin_pct: number;
  total_pipeline_eur: number;
}

const URGENCY_TABS = [
  { key: "all", label: "Tous" },
  { key: "critical", label: "Critique" },
  { key: "high", label: "Urgent" },
  { key: "medium", label: "Moyen" },
  { key: "low", label: "Faible" },
];

const URGENCY_COLORS: Record<string, string> = {
  critical: "#ef4444",
  high: "#f97316",
  medium: "#f59e0b",
  low: "#6366f1",
};

const URGENCY_BG: Record<string, string> = {
  critical: "bg-red-500/10 text-red-400 border-red-500/30",
  high: "bg-orange-500/10 text-orange-400 border-orange-500/30",
  medium: "bg-amber-500/10 text-amber-400 border-amber-500/30",
  low: "bg-indigo-500/10 text-indigo-400 border-indigo-500/30",
};

const URGENCY_LABELS: Record<string, string> = {
  critical: "Critique",
  high: "Urgent",
  medium: "Moyen",
  low: "Faible",
};

const STRATEGY_LABELS: Record<string, string> = {
  premium: "Premium",
  competitive: "Compétitif",
  penetration: "Pénétration",
  value_based: "Value-Based",
  freemium: "Freemium",
  anchor: "Ancrage",
};

const STRATEGY_COLORS: Record<string, string> = {
  premium: "bg-purple-500/10 text-purple-400",
  competitive: "bg-blue-500/10 text-blue-400",
  penetration: "bg-amber-500/10 text-amber-400",
  value_based: "bg-green-500/10 text-green-400",
  freemium: "bg-indigo-500/10 text-indigo-400",
  anchor: "bg-orange-500/10 text-orange-400",
};

const RISK_COLORS: Record<string, string> = {
  high: "text-red-400",
  medium: "text-amber-400",
  low: "text-green-400",
  none: "text-slate-500",
};

const RISK_LABELS: Record<string, string> = {
  high: "Risque élevé",
  medium: "Risque modéré",
  low: "Risque faible",
  none: "Aucun risque",
};

function fmtEur(n: number) {
  if (n >= 1_000_000) return `${(n / 1_000_000).toFixed(1)}M€`;
  if (n >= 1_000) return `${(n / 1_000).toFixed(0)}k€`;
  return `${n}€`;
}

function PriceRing({ score, urgency }: { score: number; urgency: string }) {
  const r = 28;
  const circ = 2 * Math.PI * r;
  const fill = (score / 100) * circ;
  const color =
    score >= 75 ? "#22c55e" : score >= 55 ? "#6366f1" : score >= 35 ? "#f59e0b" : "#ef4444";

  return (
    <svg width="72" height="72" viewBox="0 0 72 72" className="shrink-0">
      <circle cx="36" cy="36" r={r} fill="none" stroke="#1e293b" strokeWidth="6" />
      <circle
        cx="36"
        cy="36"
        r={r}
        fill="none"
        stroke={color}
        strokeWidth="6"
        strokeDasharray={`${fill} ${circ - fill}`}
        strokeLinecap="round"
        transform="rotate(-90 36 36)"
      />
      <text x="36" y="40" textAnchor="middle" fontSize="13" fontWeight="700" fill={color}>
        {Math.round(score)}
      </text>
    </svg>
  );
}

function DealModal({ deal, onClose }: { deal: DealResult; onClose: () => void }) {
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handler = (e: KeyboardEvent) => e.key === "Escape" && onClose();
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [onClose]);

  useEffect(() => {
    const handler = (e: MouseEvent) => {
      if (ref.current && !ref.current.contains(e.target as Node)) onClose();
    };
    setTimeout(() => window.addEventListener("mousedown", handler), 0);
    return () => window.removeEventListener("mousedown", handler);
  }, [onClose]);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4">
      <div
        ref={ref}
        className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-2xl max-h-[90vh] overflow-y-auto"
      >
        <div className="p-6 border-b border-slate-800 flex items-start justify-between gap-4">
          <div>
            <div className="flex items-center gap-3 flex-wrap">
              <h2 className="text-xl font-bold text-slate-100">{deal.deal_name}</h2>
              <span
                className={`text-xs px-2 py-0.5 rounded-full border font-medium ${URGENCY_BG[deal.deal_urgency]}`}
              >
                {URGENCY_LABELS[deal.deal_urgency]}
              </span>
              <span
                className={`text-xs px-2 py-0.5 rounded-full font-medium ${STRATEGY_COLORS[deal.recommended_strategy]}`}
              >
                {STRATEGY_LABELS[deal.recommended_strategy]}
              </span>
            </div>
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-slate-200 text-xl shrink-0">
            ✕
          </button>
        </div>

        <div className="p-6 space-y-6">
          {/* KPIs */}
          <div className="grid grid-cols-2 gap-3 sm:grid-cols-4">
            {[
              {
                label: "Prix recommandé",
                value: fmtEur(deal.recommended_price_eur),
                color: "text-indigo-400",
              },
              {
                label: "Discount",
                value: deal.discount_pct > 0 ? `-${deal.discount_pct.toFixed(0)}%` : "Aucun",
                color: RISK_COLORS[deal.discount_risk],
              },
              {
                label: "Marge",
                value: `${deal.margin_pct.toFixed(0)}%`,
                color:
                  deal.margin_pct >= 60
                    ? "text-green-400"
                    : deal.margin_pct >= 40
                    ? "text-amber-400"
                    : "text-red-400",
              },
              {
                label: "Win boost",
                value: `+${deal.win_probability_boost_pct.toFixed(0)}%`,
                color: "text-green-400",
              },
            ].map((kpi) => (
              <div key={kpi.label} className="bg-slate-800/50 rounded-xl p-3 text-center">
                <div className={`text-xl font-bold ${kpi.color}`}>{kpi.value}</div>
                <div className="text-xs text-slate-400 mt-0.5">{kpi.label}</div>
              </div>
            ))}
          </div>

          {/* Price ring + gap */}
          <div className="flex items-center gap-6 bg-slate-800/30 rounded-xl p-4">
            <PriceRing score={deal.price_score} urgency={deal.deal_urgency} />
            <div className="flex-1">
              <div className="flex items-baseline gap-2 mb-1">
                <span
                  className={`text-2xl font-bold ${
                    deal.price_score >= 75
                      ? "text-green-400"
                      : deal.price_score >= 55
                      ? "text-indigo-400"
                      : "text-amber-400"
                  }`}
                >
                  {deal.price_score.toFixed(1)}
                </span>
                <span className="text-sm text-slate-400">/ 100 — qualité du pricing</span>
              </div>
              <div className="text-xs text-slate-400">
                Écart vs compétiteur :{" "}
                <span
                  className={deal.value_gap_eur > 0 ? "text-amber-400 font-semibold" : "text-green-400 font-semibold"}
                >
                  {deal.value_gap_eur > 0 ? `+${fmtEur(deal.value_gap_eur)} (plus cher)` : `${fmtEur(Math.abs(deal.value_gap_eur))} (moins cher)`}
                </span>
              </div>
              <div className="text-xs text-slate-400 mt-1">
                Risque discount :{" "}
                <span className={RISK_COLORS[deal.discount_risk]}>
                  {RISK_LABELS[deal.discount_risk]}
                </span>
              </div>
            </div>
          </div>

          {/* Pricing signals */}
          {deal.pricing_signals.length > 0 && (
            <div>
              <h3 className="text-sm font-semibold text-green-400 mb-2">Signaux de pricing</h3>
              <ul className="space-y-1">
                {deal.pricing_signals.map((s, i) => (
                  <li key={i} className="text-xs text-slate-300 flex gap-2">
                    <span className="text-green-400 shrink-0">✓</span>
                    <span>{s}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Negotiation tips */}
          {deal.negotiation_tips.length > 0 && (
            <div className="bg-indigo-500/5 border border-indigo-500/20 rounded-xl p-4">
              <h3 className="text-sm font-semibold text-indigo-400 mb-2">Conseils de négociation</h3>
              <ul className="space-y-1.5">
                {deal.negotiation_tips.map((tip, i) => (
                  <li key={i} className="text-xs text-slate-300 flex gap-2">
                    <span className="text-indigo-400 shrink-0">→</span>
                    <span>{tip}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Risk flags */}
          {deal.risk_flags.length > 0 && (
            <div>
              <h3 className="text-sm font-semibold text-red-400 mb-2">Points de risque</h3>
              <ul className="space-y-1">
                {deal.risk_flags.map((r, i) => (
                  <li key={i} className="text-xs text-slate-300 flex gap-2">
                    <span className="text-red-400 shrink-0">⚠</span>
                    <span>{r}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

function DealCard({ deal, onClick }: { deal: DealResult; onClick: () => void }) {
  return (
    <button
      onClick={onClick}
      className="bg-slate-900 border border-slate-800 rounded-2xl p-5 text-left hover:border-slate-600 transition-all hover:bg-slate-800/40 group"
    >
      <div className="flex items-start gap-4">
        <PriceRing score={deal.price_score} urgency={deal.deal_urgency} />
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 flex-wrap mb-1">
            <span className="font-semibold text-slate-100 truncate text-sm">{deal.deal_name}</span>
            <span
              className={`text-xs px-2 py-0.5 rounded-full border font-medium shrink-0 ${URGENCY_BG[deal.deal_urgency]}`}
            >
              {URGENCY_LABELS[deal.deal_urgency]}
            </span>
          </div>
          <p className="text-xs text-slate-400 mb-3">
            Stratégie : {STRATEGY_LABELS[deal.recommended_strategy] ?? deal.recommended_strategy}
          </p>

          <div className="flex flex-wrap gap-2 text-xs">
            <span className="bg-indigo-500/10 text-indigo-400 rounded-lg px-2 py-1 font-medium">
              {fmtEur(deal.recommended_price_eur)}
            </span>
            {deal.discount_pct > 0 && (
              <span className={`rounded-lg px-2 py-1 ${STRATEGY_COLORS[deal.recommended_strategy]}`}>
                -{deal.discount_pct.toFixed(0)}%
              </span>
            )}
            <span
              className={`rounded-lg px-2 py-1 ${
                deal.margin_pct >= 60
                  ? "bg-green-500/10 text-green-400"
                  : deal.margin_pct >= 40
                  ? "bg-amber-500/10 text-amber-400"
                  : "bg-red-500/10 text-red-400"
              }`}
            >
              Marge {deal.margin_pct.toFixed(0)}%
            </span>
          </div>
        </div>
      </div>

      {/* Win boost + risk */}
      <div className="mt-4 flex items-center justify-between text-xs text-slate-500">
        <span>
          Win boost :{" "}
          <span className="text-green-400 font-semibold">+{deal.win_probability_boost_pct.toFixed(0)}%</span>
        </span>
        <span className={RISK_COLORS[deal.discount_risk]}>
          {RISK_LABELS[deal.discount_risk]}
        </span>
      </div>

      {/* Risk flags count */}
      {deal.risk_flags.length > 0 && (
        <div className="mt-2 text-xs text-red-400">
          {deal.risk_flags.length} risque{deal.risk_flags.length > 1 ? "s" : ""} identifié{deal.risk_flags.length > 1 ? "s" : ""}
        </div>
      )}
    </button>
  );
}

export default function PricingOptimizerPage() {
  const [deals, setDeals] = useState<DealResult[]>([]);
  const [summary, setSummary] = useState<Summary | null>(null);
  const [activeUrgency, setActiveUrgency] = useState("all");
  const [selected, setSelected] = useState<DealResult | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      setLoading(true);
      try {
        const params = new URLSearchParams();
        if (activeUrgency !== "all") params.set("urgency", activeUrgency);
        const res = await fetch(`/api/pricing-optimizer?${params}`);
        const data = await res.json();
        setDeals(data.deals ?? []);
        setSummary(data.summary ?? null);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, [activeUrgency]);

  return (
    <div className="min-h-screen bg-slate-950 p-6">
      <div className="max-w-7xl mx-auto space-y-6">
        {/* Header */}
        <div>
          <h1 className="text-2xl font-bold text-slate-100">Optimiseur Pricing</h1>
          <p className="text-sm text-slate-400 mt-1">
            Recommandations de prix et stratégie de négociation par deal — marge, discount et probabilité de gain
          </p>
        </div>

        {/* KPI strip */}
        {summary && (
          <div className="grid grid-cols-2 gap-3 sm:grid-cols-4">
            {[
              {
                label: "Deals analysés",
                value: `${summary.total}`,
                sub: `${summary.urgency_counts["critical"] || 0} critiques`,
                color: "text-slate-100",
              },
              {
                label: "Pipeline total",
                value: fmtEur(summary.total_pipeline_eur),
                sub: "Somme des prix recommandés",
                color: "text-indigo-400",
              },
              {
                label: "Marge moyenne",
                value: `${summary.avg_margin_pct.toFixed(0)}%`,
                sub: `Discount moyen ${summary.avg_discount_pct.toFixed(0)}%`,
                color:
                  summary.avg_margin_pct >= 55
                    ? "text-green-400"
                    : summary.avg_margin_pct >= 40
                    ? "text-amber-400"
                    : "text-red-400",
              },
              {
                label: "Score pricing moyen",
                value: `${summary.avg_price_score}/100`,
                sub: "Qualité globale du pricing",
                color:
                  summary.avg_price_score >= 70
                    ? "text-green-400"
                    : summary.avg_price_score >= 50
                    ? "text-amber-400"
                    : "text-red-400",
              },
            ].map((kpi) => (
              <div
                key={kpi.label}
                className="bg-slate-900 border border-slate-800 rounded-2xl p-4"
              >
                <div className={`text-2xl font-bold ${kpi.color}`}>{kpi.value}</div>
                <div className="text-xs text-slate-400 mt-0.5">{kpi.label}</div>
                <div className="text-xs text-slate-500 mt-1">{kpi.sub}</div>
              </div>
            ))}
          </div>
        )}

        {/* Urgency filter tabs */}
        <div className="flex flex-wrap gap-2">
          {URGENCY_TABS.map((t) => {
            const count = t.key === "all" ? summary?.total : summary?.urgency_counts[t.key];
            return (
              <button
                key={t.key}
                onClick={() => setActiveUrgency(t.key)}
                className={`px-4 py-1.5 rounded-full text-sm font-medium border transition-all ${
                  activeUrgency === t.key
                    ? "bg-indigo-600 border-indigo-500 text-white"
                    : "bg-slate-800/50 border-slate-700 text-slate-400 hover:border-slate-500"
                }`}
              >
                {t.label}
                {count !== undefined && (
                  <span className="ml-1.5 text-xs opacity-70">({count})</span>
                )}
              </button>
            );
          })}
        </div>

        {/* Strategy breakdown */}
        {summary && activeUrgency === "all" && (
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-4">
            <p className="text-xs text-slate-400 mb-3">Répartition des stratégies recommandées</p>
            <div className="flex flex-wrap gap-2">
              {Object.entries(summary.strategy_counts).map(([strat, count]) => (
                <div
                  key={strat}
                  className={`flex items-center gap-1.5 text-xs px-3 py-1 rounded-full ${STRATEGY_COLORS[strat] ?? "bg-slate-700 text-slate-300"}`}
                >
                  <span>{STRATEGY_LABELS[strat] ?? strat}</span>
                  <span className="opacity-70">({count})</span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Deals grid */}
        {loading ? (
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {Array.from({ length: 6 }).map((_, i) => (
              <div key={i} className="h-56 bg-slate-900 border border-slate-800 rounded-2xl animate-pulse" />
            ))}
          </div>
        ) : deals.length === 0 ? (
          <div className="text-center py-20 text-slate-500">Aucun deal pour ce filtre</div>
        ) : (
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {deals.map((deal) => (
              <DealCard
                key={deal.deal_id}
                deal={deal}
                onClick={() => setSelected(deal)}
              />
            ))}
          </div>
        )}
      </div>

      {selected && <DealModal deal={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
