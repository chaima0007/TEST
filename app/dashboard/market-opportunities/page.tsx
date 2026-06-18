"use client";

import { useEffect, useState, useCallback } from "react";

type OpportunityPhase = "emerging" | "growing" | "mature" | "declining";
type RiskLevel = "low" | "medium" | "high" | "critical";

interface MarketSignals {
  opportunity_id: string;
  market_name: string;
  sector: string;
  sub_sector: string;
  total_addressable_market_eur: number;
  annual_growth_rate_pct: number;
  competitor_count: number;
  our_market_share_pct: number;
  avg_deal_size_eur: number;
  avg_sales_cycle_days: number;
  demand_trend: number;
  regulatory_complexity: number;
  tech_disruption_risk: number;
  our_expertise_score: number;
}

interface ScoredOpportunity {
  market: MarketSignals;
  opportunity_score: number;
  opportunity_phase: OpportunityPhase;
  risk_level: RiskLevel;
  market_attractiveness: number;
  penetrability: number;
  strategic_fit: number;
  projected_revenue_2y_eur: number;
  key_advantages: string[];
  key_risks: string[];
  recommended_actions: string[];
}

interface Summary {
  total: number;
  phase_counts: Record<OpportunityPhase, number>;
  risk_counts: Record<RiskLevel, number>;
  avg_opportunity_score: number;
  total_projected_revenue_2y_eur: number;
  top_sector: string | null;
}

interface ApiData {
  opportunities: ScoredOpportunity[];
  summary: Summary;
  last_updated: string;
}

// ─── Helpers ─────────────────────────────────────────────────────────────────

function fmt(n: number) {
  if (n >= 1_000_000_000) return `${(n / 1_000_000_000).toFixed(1)}Md€`;
  if (n >= 1_000_000) return `${(n / 1_000_000).toFixed(1)}M€`;
  if (n >= 1_000) return `${(n / 1_000).toFixed(0)}k€`;
  return `${n.toFixed(0)}€`;
}

const PHASE_LABEL: Record<OpportunityPhase, string> = {
  emerging: "Émergent", growing: "En croissance", mature: "Mature", declining: "Déclin",
};

const PHASE_COLOR: Record<OpportunityPhase, string> = {
  emerging: "text-emerald-400 bg-emerald-400/10 border-emerald-400/30",
  growing: "text-sky-400 bg-sky-400/10 border-sky-400/30",
  mature: "text-slate-300 bg-slate-700/40 border-slate-600/30",
  declining: "text-red-400 bg-red-400/10 border-red-400/30",
};

const RISK_LABEL: Record<RiskLevel, string> = {
  low: "Faible", medium: "Moyen", high: "Élevé", critical: "Critique",
};

const RISK_COLOR: Record<RiskLevel, string> = {
  low: "text-emerald-400", medium: "text-amber-400", high: "text-orange-400", critical: "text-red-400",
};

function PhaseBadge({ phase }: { phase: OpportunityPhase }) {
  return (
    <span className={`px-2 py-0.5 rounded-full text-[10px] font-semibold border ${PHASE_COLOR[phase]}`}>
      {PHASE_LABEL[phase]}
    </span>
  );
}

function ScoreRing({ score, size = 56 }: { score: number; size?: number }) {
  const radius = (size - 8) / 2;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (score / 100) * circumference;
  const color = score >= 70 ? "#10b981" : score >= 55 ? "#38bdf8" : score >= 40 ? "#f59e0b" : "#f87171";

  return (
    <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`} className="flex-shrink-0">
      <circle cx={size / 2} cy={size / 2} r={radius} fill="none" stroke="#1e293b" strokeWidth="6" />
      <circle
        cx={size / 2} cy={size / 2} r={radius}
        fill="none" stroke={color} strokeWidth="6"
        strokeDasharray={circumference}
        strokeDashoffset={offset}
        strokeLinecap="round"
        transform={`rotate(-90 ${size / 2} ${size / 2})`}
      />
      <text x={size / 2} y={size / 2 + 4} textAnchor="middle" fontSize="11" fontWeight="bold" fill={color}>
        {Math.round(score)}
      </text>
    </svg>
  );
}

function DimBar({ label, score }: { label: string; score: number }) {
  const color = score >= 70 ? "bg-emerald-500" : score >= 50 ? "bg-amber-500" : "bg-red-500";
  return (
    <div className="flex items-center gap-2">
      <span className="text-[10px] text-slate-500 w-24 truncate">{label}</span>
      <div className="flex-1 h-1.5 bg-slate-700 rounded-full overflow-hidden">
        <div className={`h-full rounded-full ${color}`} style={{ width: `${score}%` }} />
      </div>
      <span className="text-[10px] text-slate-400 w-6 text-right">{Math.round(score)}</span>
    </div>
  );
}

// ─── Opportunity Modal ────────────────────────────────────────────────────────

function OpportunityModal({ opp, onClose }: { opp: ScoredOpportunity; onClose: () => void }) {
  useEffect(() => {
    const handler = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    document.addEventListener("keydown", handler);
    return () => document.removeEventListener("keydown", handler);
  }, [onClose]);

  const m = opp.market;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4" onClick={onClose}>
      <div className="absolute inset-0 bg-black/60" />
      <div
        className="relative bg-slate-900 border border-slate-700 rounded-xl w-full max-w-xl shadow-2xl overflow-y-auto max-h-[90vh]"
        onClick={e => e.stopPropagation()}
      >
        <div className="p-5 border-b border-slate-800 flex items-start justify-between gap-3">
          <div>
            <h2 className="text-white font-semibold text-lg">{m.market_name}</h2>
            <p className="text-slate-400 text-sm">{m.sector} / {m.sub_sector}</p>
          </div>
          <div className="flex items-center gap-2">
            <PhaseBadge phase={opp.opportunity_phase} />
            <button onClick={onClose} className="text-slate-500 hover:text-white text-xl leading-none p-1">×</button>
          </div>
        </div>

        <div className="p-5 space-y-5">
          {/* Score + projection */}
          <div className="flex items-center gap-4 bg-slate-800 rounded-xl p-4">
            <ScoreRing score={opp.opportunity_score} size={72} />
            <div>
              <div className="text-xs text-slate-500">Score d'opportunité</div>
              <div className="text-3xl font-bold text-white">{Math.round(opp.opportunity_score)}/100</div>
              <div className="text-xs text-emerald-400 mt-1">Revenue projeté 2 ans: {fmt(opp.projected_revenue_2y_eur)}</div>
            </div>
          </div>

          {/* Market stats */}
          <div className="grid grid-cols-2 gap-3 text-xs">
            {[
              { label: "TAM", value: fmt(m.total_addressable_market_eur) },
              { label: "Croissance/an", value: `${(m.annual_growth_rate_pct * 100).toFixed(0)}%` },
              { label: "Concurrents", value: m.competitor_count },
              { label: "Deal moyen", value: fmt(m.avg_deal_size_eur) },
              { label: "Cycle de vente", value: `${m.avg_sales_cycle_days}j` },
              { label: "Notre part", value: `${m.our_market_share_pct}%` },
              { label: "Risque", value: RISK_LABEL[opp.risk_level], className: RISK_COLOR[opp.risk_level] },
              { label: "Expertise", value: `${m.our_expertise_score}/100` },
            ].map(({ label, value, className }) => (
              <div key={label} className="bg-slate-800 rounded-lg p-2.5">
                <div className="text-slate-500">{label}</div>
                <div className={`font-semibold mt-0.5 ${className ?? "text-white"}`}>{value}</div>
              </div>
            ))}
          </div>

          {/* Dimensions */}
          <div>
            <p className="text-xs font-semibold text-slate-400 uppercase tracking-wide mb-2">Dimensions</p>
            <div className="space-y-2">
              <DimBar label="Attractivité marché" score={opp.market_attractiveness} />
              <DimBar label="Pénétrabilité" score={opp.penetrability} />
              <DimBar label="Fit stratégique" score={opp.strategic_fit} />
            </div>
          </div>

          {/* Advantages */}
          {opp.key_advantages.length > 0 && (
            <div>
              <p className="text-xs font-semibold text-emerald-400 uppercase tracking-wide mb-2">Avantages clés</p>
              <ul className="space-y-1">
                {opp.key_advantages.map(a => (
                  <li key={a} className="flex items-start gap-2 text-xs text-slate-300">
                    <span className="text-emerald-400 mt-0.5">▲</span>{a}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Risks */}
          {opp.key_risks.length > 0 && (
            <div>
              <p className="text-xs font-semibold text-red-400 uppercase tracking-wide mb-2">Risques identifiés</p>
              <ul className="space-y-1">
                {opp.key_risks.map(r => (
                  <li key={r} className="flex items-start gap-2 text-xs text-slate-300">
                    <span className="text-red-400 mt-0.5">▼</span>{r}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Actions */}
          {opp.recommended_actions.length > 0 && (
            <div>
              <p className="text-xs font-semibold text-sky-400 uppercase tracking-wide mb-2">Actions recommandées</p>
              <ul className="space-y-2">
                {opp.recommended_actions.map((a, i) => (
                  <li key={i} className="flex items-start gap-2 text-xs text-slate-300 bg-slate-800 rounded-lg p-2.5">
                    <span className="text-sky-400 mt-0.5 flex-shrink-0">→</span>{a}
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

// ─── Main page ────────────────────────────────────────────────────────────────

const PHASE_FILTERS: { key: OpportunityPhase | "all"; label: string }[] = [
  { key: "all", label: "Tous" },
  { key: "emerging", label: "Émergents" },
  { key: "growing", label: "En croissance" },
  { key: "mature", label: "Matures" },
  { key: "declining", label: "Déclin" },
];

export default function MarketOpportunitiesPage() {
  const [data, setData] = useState<ApiData | null>(null);
  const [loading, setLoading] = useState(true);
  const [phaseFilter, setPhaseFilter] = useState<OpportunityPhase | "all">("all");
  const [selected, setSelected] = useState<ScoredOpportunity | null>(null);

  const load = useCallback(async () => {
    try {
      const res = await fetch("/api/market-opportunities", { cache: "no-store" });
      if (res.ok) setData(await res.json());
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { load(); }, [load]);

  const filtered = data?.opportunities.filter(o => phaseFilter === "all" || o.opportunity_phase === phaseFilter) ?? [];
  const summary = data?.summary;

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center">
        <div className="w-6 h-6 border-2 border-indigo-500 border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      <div className="max-w-7xl mx-auto px-4 py-8 space-y-6">

        {/* Header */}
        <div className="flex items-start justify-between gap-4">
          <div>
            <h1 className="text-2xl font-bold text-white">Scanner Opportunités Marché</h1>
            <p className="text-slate-400 text-sm mt-1">
              Score composite: attractivité(40%) + pénétrabilité(35%) + fit stratégique(25%)
            </p>
          </div>
          {data && (
            <span className="text-xs text-slate-500">
              Mis à jour {new Date(data.last_updated).toLocaleTimeString("fr-FR")}
            </span>
          )}
        </div>

        {/* KPIs */}
        {summary && (
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {[
              { label: "Marchés analysés", value: `${summary.total}`, sub: `Score moy. ${summary.avg_opportunity_score.toFixed(0)}/100`, color: "text-white" },
              { label: "Revenus projetés 2 ans", value: fmt(summary.total_projected_revenue_2y_eur), sub: summary.top_sector ? `Secteur leader: ${summary.top_sector}` : "—", color: "text-emerald-400" },
              { label: "Marchés émergents", value: `${summary.phase_counts.emerging}`, sub: `En croissance: ${summary.phase_counts.growing}`, color: "text-sky-400" },
              { label: "Risque critique", value: `${summary.risk_counts.critical}`, sub: `Risque élevé: ${summary.risk_counts.high}`, color: "text-red-400" },
            ].map(k => (
              <div key={k.label} className="bg-slate-900 border border-slate-800 rounded-xl p-4">
                <p className="text-xs text-slate-500 font-medium uppercase tracking-wide">{k.label}</p>
                <p className={`text-2xl font-bold mt-1 ${k.color}`}>{k.value}</p>
                <p className="text-xs text-slate-500 mt-0.5">{k.sub}</p>
              </div>
            ))}
          </div>
        )}

        {/* Phase filters */}
        <div className="flex gap-1.5 flex-wrap">
          {PHASE_FILTERS.map(f => (
            <button
              key={f.key}
              onClick={() => setPhaseFilter(f.key as OpportunityPhase | "all")}
              className={`px-3 py-1 rounded-full text-xs font-medium transition-colors ${
                phaseFilter === f.key ? "bg-indigo-600 text-white" : "bg-slate-800 text-slate-400 hover:text-white"
              }`}
            >
              {f.label}
              {f.key !== "all" && summary && (
                <span className="ml-1 opacity-60">({summary.phase_counts[f.key]})</span>
              )}
            </button>
          ))}
        </div>

        {/* Opportunity grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
          {filtered.length === 0 && (
            <p className="text-slate-500 text-sm text-center py-8 col-span-3">Aucune opportunité pour ce filtre</p>
          )}
          {filtered.map((opp, i) => (
            <div
              key={opp.market.opportunity_id}
              onClick={() => setSelected(opp)}
              className="bg-slate-900 border border-slate-800 rounded-xl p-4 cursor-pointer hover:border-slate-600 transition-colors"
            >
              <div className="flex items-start gap-3 mb-3">
                <ScoreRing score={opp.opportunity_score} size={52} />
                <div className="flex-1 min-w-0">
                  <div className="flex items-start justify-between gap-2">
                    <p className="text-white font-medium text-sm truncate">{opp.market.market_name}</p>
                    <span className="text-[10px] font-semibold text-slate-500 flex-shrink-0">#{i + 1}</span>
                  </div>
                  <p className="text-slate-400 text-xs capitalize mt-0.5">{opp.market.sector}</p>
                  <div className="flex items-center gap-2 mt-1.5">
                    <PhaseBadge phase={opp.opportunity_phase} />
                    <span className={`text-[10px] font-medium ${RISK_COLOR[opp.risk_level]}`}>
                      Risque {RISK_LABEL[opp.risk_level]}
                    </span>
                  </div>
                </div>
              </div>

              {/* Mini dim bars */}
              <div className="space-y-1 mb-3">
                {[
                  { label: "Attractivité", score: opp.market_attractiveness },
                  { label: "Pénétrabilité", score: opp.penetrability },
                  { label: "Fit stratégique", score: opp.strategic_fit },
                ].map(({ label, score }) => (
                  <div key={label} className="flex items-center gap-2">
                    <span className="text-[9px] text-slate-600 w-16">{label}</span>
                    <div className="flex-1 h-1 bg-slate-700 rounded-full overflow-hidden">
                      <div
                        className={`h-full rounded-full ${score >= 70 ? "bg-emerald-500" : score >= 50 ? "bg-amber-500" : "bg-red-500"}`}
                        style={{ width: `${score}%` }}
                      />
                    </div>
                  </div>
                ))}
              </div>

              <div className="flex items-center justify-between text-xs">
                <span className="text-slate-500">TAM: {fmt(opp.market.total_addressable_market_eur)}</span>
                <span className="text-emerald-400 font-medium">{fmt(opp.projected_revenue_2y_eur)} proj.</span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {selected && <OpportunityModal opp={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
