"use client";

import { useEffect, useState } from "react";

interface Deal {
  deal_id: string;
  account_name: string;
  segment: string;
  list_price_eur: number;
  proposed_price_eur: number;
  optimized_price_eur: number;
  recommended_discount_pct: number;
  max_acceptable_discount_pct: number;
  pricing_strategy: string;
  discount_risk: string;
  pricing_action: string;
  revenue_impact: string;
  price_optimization_score: number;
  pricing_rationale: string[];
  negotiation_guardrails: string[];
  value_anchors: string[];
  bundle_options: string[];
}

interface Summary {
  total: number;
  risk_counts: Record<string, number>;
  action_counts: Record<string, number>;
  strategy_counts: Record<string, number>;
  revenue_impact_counts: Record<string, number>;
  avg_optimization_score: number;
  excessive_discount_count: number;
  restructure_count: number;
  total_revenue_at_risk_eur: number;
}

const RISK_COLOR: Record<string, string> = {
  low: "#10b981",
  medium: "#f59e0b",
  high: "#ef4444",
  excessive: "#7c3aed",
};

const RISK_BADGE: Record<string, string> = {
  low: "bg-emerald-900/60 text-emerald-300 border-emerald-700",
  medium: "bg-amber-900/60 text-amber-300 border-amber-700",
  high: "bg-red-900/60 text-red-300 border-red-700",
  excessive: "bg-violet-900/60 text-violet-300 border-violet-700",
};

const ACTION_BADGE: Record<string, string> = {
  hold: "bg-slate-800 text-slate-400 border-slate-600",
  increase: "bg-emerald-900/60 text-emerald-300 border-emerald-700",
  bundle: "bg-sky-900/60 text-sky-300 border-sky-700",
  discount: "bg-amber-900/60 text-amber-300 border-amber-700",
  restructure: "bg-red-900/60 text-red-300 border-red-700",
};

const STRATEGY_BADGE: Record<string, string> = {
  premium: "bg-indigo-900/60 text-indigo-300 border-indigo-700",
  competitive: "bg-sky-900/60 text-sky-300 border-sky-700",
  penetration: "bg-amber-900/60 text-amber-300 border-amber-700",
  value_based: "bg-emerald-900/60 text-emerald-300 border-emerald-700",
};

const IMPACT_BADGE: Record<string, string> = {
  positive: "bg-emerald-900/60 text-emerald-300 border-emerald-700",
  neutral: "bg-slate-800 text-slate-400 border-slate-600",
  negative: "bg-red-900/60 text-red-300 border-red-700",
};

function ScoreRing({ score, risk }: { score: number; risk: string }) {
  const r = 40;
  const circ = 2 * Math.PI * r;
  const arc = (score / 100) * circ;
  const stroke = RISK_COLOR[risk] || "#64748b";
  return (
    <svg width="96" height="96" viewBox="0 0 96 96">
      <circle cx="48" cy="48" r={r} fill="none" stroke="#1e293b" strokeWidth="10" />
      <circle
        cx="48"
        cy="48"
        r={r}
        fill="none"
        stroke={stroke}
        strokeWidth="10"
        strokeDasharray={`${arc} ${circ - arc}`}
        strokeLinecap="round"
        transform="rotate(-90 48 48)"
      />
      <text x="48" y="53" textAnchor="middle" fill="#f1f5f9" fontSize="18" fontWeight="bold">
        {Math.round(score)}
      </text>
    </svg>
  );
}

function RiskBar({ counts, total }: { counts: Record<string, number>; total: number }) {
  if (!total) return null;
  const segments = [
    { key: "low", label: "Faible", color: "bg-emerald-500" },
    { key: "medium", label: "Moyen", color: "bg-amber-500" },
    { key: "high", label: "Élevé", color: "bg-red-500" },
    { key: "excessive", label: "Excessif", color: "bg-violet-600" },
  ];
  return (
    <div className="mb-6">
      <div className="flex rounded-full overflow-hidden h-3 mb-2">
        {segments.map(({ key, color }) => {
          const pct = ((counts[key] || 0) / total) * 100;
          return pct > 0 ? (
            <div key={key} className={`${color} h-3`} style={{ width: `${pct}%` }} />
          ) : null;
        })}
      </div>
      <div className="flex gap-4 text-xs text-slate-400">
        {segments.map(({ key, label, color }) => (
          <span key={key} className="flex items-center gap-1">
            <span className={`inline-block w-2 h-2 rounded-full ${color}`} />
            {label} ({counts[key] || 0})
          </span>
        ))}
      </div>
    </div>
  );
}

function fmt(n: number) {
  return n >= 1000000
    ? `${(n / 1000000).toFixed(1)}M€`
    : n >= 1000
    ? `${(n / 1000).toFixed(0)}k€`
    : `${n}€`;
}

function actionLabel(a: string) {
  const m: Record<string, string> = {
    hold: "Maintenir",
    increase: "Augmenter",
    bundle: "Bundler",
    discount: "Réduire",
    restructure: "Restructurer",
  };
  return m[a] || a;
}

function strategyLabel(s: string) {
  const m: Record<string, string> = {
    premium: "Premium",
    competitive: "Compétitif",
    penetration: "Pénétration",
    value_based: "Valeur",
  };
  return m[s] || s;
}

function DealCard({ deal, onClick }: { deal: Deal; onClick: () => void }) {
  const discount = ((deal.list_price_eur - deal.proposed_price_eur) / deal.list_price_eur * 100).toFixed(1);
  return (
    <div
      onClick={onClick}
      className="bg-slate-800/60 border border-slate-700 rounded-xl p-5 cursor-pointer hover:border-slate-500 hover:bg-slate-800 transition-all"
    >
      <div className="flex items-start gap-4 mb-4">
        <ScoreRing score={deal.price_optimization_score} risk={deal.discount_risk} />
        <div className="flex-1 min-w-0">
          <h3 className="font-semibold text-slate-100 text-base truncate">{deal.account_name}</h3>
          <p className="text-slate-400 text-sm capitalize">{deal.segment}</p>
          <div className="flex flex-wrap gap-1 mt-2">
            <span className={`text-xs px-2 py-0.5 rounded-full border font-medium capitalize ${RISK_BADGE[deal.discount_risk]}`}>
              Risque {deal.discount_risk}
            </span>
            <span className={`text-xs px-2 py-0.5 rounded-full border font-medium ${ACTION_BADGE[deal.pricing_action]}`}>
              {actionLabel(deal.pricing_action)}
            </span>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-3 gap-2 mb-4 text-center">
        <div className="bg-slate-900/50 rounded-lg p-2">
          <div className="text-slate-100 font-bold text-sm">{fmt(deal.list_price_eur)}</div>
          <div className="text-slate-500 text-xs">Liste</div>
        </div>
        <div className="bg-slate-900/50 rounded-lg p-2">
          <div className="text-slate-100 font-bold text-sm">{fmt(deal.optimized_price_eur)}</div>
          <div className="text-slate-500 text-xs">Optimisé</div>
        </div>
        <div className="bg-slate-900/50 rounded-lg p-2">
          <div className={`font-bold text-sm ${parseFloat(discount) > 15 ? "text-red-400" : "text-slate-100"}`}>
            -{discount}%
          </div>
          <div className="text-slate-500 text-xs">Remise act.</div>
        </div>
      </div>

      <div className="flex gap-2 mb-3">
        <span className={`text-xs px-2 py-0.5 rounded-full border ${STRATEGY_BADGE[deal.pricing_strategy]}`}>
          {strategyLabel(deal.pricing_strategy)}
        </span>
        <span className={`text-xs px-2 py-0.5 rounded-full border ${IMPACT_BADGE[deal.revenue_impact]}`}>
          {deal.revenue_impact === "positive" ? "Impact +" : deal.revenue_impact === "negative" ? "Impact -" : "Neutre"}
        </span>
      </div>

      <div className="mt-1">
        <div className="flex justify-between text-xs text-slate-500 mb-1">
          <span>Score pricing</span>
          <span>{Math.round(deal.price_optimization_score)}/100</span>
        </div>
        <div className="h-1.5 bg-slate-700 rounded-full overflow-hidden">
          <div
            className="h-1.5 rounded-full"
            style={{
              width: `${deal.price_optimization_score}%`,
              backgroundColor: RISK_COLOR[deal.discount_risk] || "#64748b",
            }}
          />
        </div>
      </div>
    </div>
  );
}

function DealModal({ deal, onClose }: { deal: Deal; onClose: () => void }) {
  const [tab, setTab] = useState<"rationale" | "guardrails" | "anchors" | "bundles">("rationale");

  useEffect(() => {
    const handler = (e: KeyboardEvent) => e.key === "Escape" && onClose();
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [onClose]);

  const discount = ((deal.list_price_eur - deal.proposed_price_eur) / deal.list_price_eur * 100).toFixed(1);

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm p-4"
      onClick={onClose}
    >
      <div
        className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-2xl max-h-[90vh] overflow-y-auto shadow-2xl"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="p-6 border-b border-slate-800 flex items-start gap-4">
          <ScoreRing score={deal.price_optimization_score} risk={deal.discount_risk} />
          <div className="flex-1">
            <h2 className="text-xl font-bold text-slate-100">{deal.account_name}</h2>
            <p className="text-slate-400 text-sm capitalize">{deal.segment}</p>
            <div className="flex flex-wrap gap-2 mt-2">
              <span className={`text-xs px-2 py-0.5 rounded-full border font-medium capitalize ${RISK_BADGE[deal.discount_risk]}`}>
                Risque {deal.discount_risk}
              </span>
              <span className={`text-xs px-2 py-0.5 rounded-full border font-medium ${ACTION_BADGE[deal.pricing_action]}`}>
                {actionLabel(deal.pricing_action)}
              </span>
              <span className={`text-xs px-2 py-0.5 rounded-full border ${STRATEGY_BADGE[deal.pricing_strategy]}`}>
                {strategyLabel(deal.pricing_strategy)}
              </span>
            </div>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-slate-300 text-2xl leading-none">&times;</button>
        </div>

        <div className="p-4 border-b border-slate-800">
          <div className="grid grid-cols-4 gap-3 text-center">
            <div className="bg-slate-800 rounded-xl p-3">
              <div className="text-base font-bold text-slate-100">{fmt(deal.list_price_eur)}</div>
              <div className="text-xs text-slate-400">Prix liste</div>
            </div>
            <div className="bg-slate-800 rounded-xl p-3">
              <div className="text-base font-bold text-amber-400">{fmt(deal.proposed_price_eur)}</div>
              <div className="text-xs text-slate-400">Proposé</div>
            </div>
            <div className="bg-slate-800 rounded-xl p-3">
              <div className="text-base font-bold text-emerald-400">{fmt(deal.optimized_price_eur)}</div>
              <div className="text-xs text-slate-400">Optimisé</div>
            </div>
            <div className="bg-slate-800 rounded-xl p-3">
              <div className={`text-base font-bold ${parseFloat(discount) > 15 ? "text-red-400" : "text-slate-100"}`}>
                -{discount}%
              </div>
              <div className="text-xs text-slate-400">Remise act.</div>
            </div>
          </div>
          <div className="mt-3 grid grid-cols-2 gap-3 text-center text-sm">
            <div className="text-slate-400">
              Remise recommandée : <span className="text-indigo-300 font-bold">{deal.recommended_discount_pct}%</span>
            </div>
            <div className="text-slate-400">
              Max acceptable : <span className="text-red-300 font-bold">{deal.max_acceptable_discount_pct}%</span>
            </div>
          </div>
        </div>

        {/* Tabs */}
        <div className="flex border-b border-slate-800">
          {(["rationale", "guardrails", "anchors", "bundles"] as const).map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`flex-1 py-2 text-xs font-medium capitalize transition-colors ${
                tab === t
                  ? "text-indigo-400 border-b-2 border-indigo-500"
                  : "text-slate-500 hover:text-slate-300"
              }`}
            >
              {t === "rationale" ? "Rationale" : t === "guardrails" ? "Guardrails" : t === "anchors" ? "Ancres valeur" : "Bundles"}
            </button>
          ))}
        </div>

        <div className="p-6 space-y-3">
          {tab === "rationale" && deal.pricing_rationale.map((r, i) => (
            <div key={i} className="text-sm text-slate-300 bg-indigo-900/20 border border-indigo-800/40 rounded-lg px-3 py-2">
              {r}
            </div>
          ))}

          {tab === "guardrails" && deal.negotiation_guardrails.map((g, i) => (
            <div key={i} className="text-sm text-slate-300 bg-amber-900/20 border border-amber-800/40 rounded-lg px-3 py-2 flex gap-2">
              <span className="text-amber-400 shrink-0">⚠</span> {g}
            </div>
          ))}

          {tab === "anchors" && deal.value_anchors.map((a, i) => (
            <div key={i} className="text-sm text-slate-300 bg-emerald-900/20 border border-emerald-800/40 rounded-lg px-3 py-2">
              {a}
            </div>
          ))}

          {tab === "bundles" && deal.bundle_options.map((b, i) => (
            <div key={i} className="text-sm text-slate-300 bg-sky-900/20 border border-sky-800/40 rounded-lg px-3 py-2">
              {b}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

const RISKS = ["all", "low", "medium", "high", "excessive"];
const ACTIONS = ["all", "hold", "increase", "bundle", "discount", "restructure"];

export default function PriceOptimizationPage() {
  const [data, setData] = useState<{ deals: Deal[]; summary: Summary } | null>(null);
  const [loading, setLoading] = useState(true);
  const [selectedDeal, setSelectedDeal] = useState<Deal | null>(null);
  const [riskFilter, setRiskFilter] = useState("all");
  const [actionFilter, setActionFilter] = useState("all");

  useEffect(() => {
    async function load() {
      const params = new URLSearchParams();
      if (riskFilter !== "all") params.set("risk", riskFilter);
      if (actionFilter !== "all") params.set("action", actionFilter);
      const res = await fetch(`/api/price-optimization?${params}`);
      const json = await res.json();
      setData(json);
      setLoading(false);
    }
    load();
  }, [riskFilter, actionFilter]);

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center">
        <div className="text-slate-400 animate-pulse">Chargement pricing...</div>
      </div>
    );
  }

  const s = data!.summary;

  const kpis = [
    { label: "Score Moyen", value: s.avg_optimization_score.toFixed(1), sub: "/ 100" },
    { label: "Deals Excessifs", value: s.excessive_discount_count, sub: "remise hors guardrail" },
    { label: "À Restructurer", value: s.restructure_count, sub: "urgence pricing" },
    { label: "Revenue à Risque", value: fmt(s.total_revenue_at_risk_eur), sub: "high + excessif" },
    { label: "Total Deals", value: s.total, sub: "analysés" },
    { label: "Impact Positif", value: s.revenue_impact_counts["positive"] || 0, sub: "revenue optimisé" },
  ];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-slate-100">Optimisation Pricing</h1>
          <p className="text-slate-400 mt-1">IA de pricing — remises optimales, guardrails de négociation et bundles intelligents</p>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4 mb-8">
          {kpis.map(({ label, value, sub }) => (
            <div key={label} className="bg-slate-800/60 border border-slate-700 rounded-xl p-4">
              <div className="text-2xl font-bold text-slate-100">{value}</div>
              <div className="text-xs text-slate-400 mt-0.5">{label}</div>
              <div className="text-xs text-slate-600 mt-0.5">{sub}</div>
            </div>
          ))}
        </div>

        <RiskBar counts={s.risk_counts} total={s.total} />

        <div className="flex flex-wrap gap-2 mb-3">
          {RISKS.map((v) => (
            <button
              key={v}
              onClick={() => setRiskFilter(v)}
              className={`text-xs px-3 py-1.5 rounded-full border transition-colors capitalize ${
                riskFilter === v
                  ? "bg-indigo-600 border-indigo-500 text-white"
                  : "bg-slate-800 border-slate-700 text-slate-400 hover:border-slate-500"
              }`}
            >
              {v === "all" ? "Tous les risques" : v}
              {v !== "all" && s.risk_counts[v] ? ` (${s.risk_counts[v]})` : ""}
            </button>
          ))}
        </div>

        <div className="flex flex-wrap gap-2 mb-8">
          {ACTIONS.map((v) => (
            <button
              key={v}
              onClick={() => setActionFilter(v)}
              className={`text-xs px-3 py-1.5 rounded-full border transition-colors ${
                actionFilter === v
                  ? "bg-violet-600 border-violet-500 text-white"
                  : "bg-slate-800 border-slate-700 text-slate-400 hover:border-slate-500"
              }`}
            >
              {v === "all" ? "Toutes actions" : actionLabel(v)}
              {v !== "all" && s.action_counts[v] ? ` (${s.action_counts[v]})` : ""}
            </button>
          ))}
        </div>

        {data!.deals.length === 0 ? (
          <div className="text-center text-slate-500 py-20">Aucun deal pour ces filtres</div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-5">
            {data!.deals.map((deal) => (
              <DealCard key={deal.deal_id} deal={deal} onClick={() => setSelectedDeal(deal)} />
            ))}
          </div>
        )}
      </div>

      {selectedDeal && <DealModal deal={selectedDeal} onClose={() => setSelectedDeal(null)} />}
    </div>
  );
}
