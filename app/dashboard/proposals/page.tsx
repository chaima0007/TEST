"use client";

import { useEffect, useState } from "react";

type ProposalTier = "weak" | "fair" | "good" | "strong";

interface ProposalSignals {
  proposal_id: string;
  client_name: string;
  sector: string;
  deal_value_eur: number;
  client_budget_eur: number;
  competitor_count: number;
  has_incumbent: boolean;
  meetings_held: number;
  decision_maker_reached: boolean;
  days_to_deadline: number;
  has_roi_model: boolean;
  has_case_study: boolean;
  has_personalization: boolean;
  relationship_score: number;
  previous_deals_won: number;
  proposal_page_count: number;
  our_price_vs_market: number;
}

interface ScoredProposal {
  proposal: ProposalSignals;
  win_probability: number;
  proposal_tier: ProposalTier;
  dimension_scores: Record<string, number>;
  recommendations: string[];
  strengths: string[];
}

interface Summary {
  total: number;
  tier_counts: Record<ProposalTier, number>;
  avg_win_probability: number;
  best_win_probability: number;
  total_pipeline_eur: number;
  expected_won_eur: number;
}

interface ApiData {
  proposals: ScoredProposal[];
  summary: Summary;
  last_updated: string;
}

// ─── Helpers ─────────────────────────────────────────────────────────────────

function fmt(n: number) {
  if (n >= 1_000_000) return `${(n / 1_000_000).toFixed(1)}M€`;
  if (n >= 1_000) return `${(n / 1_000).toFixed(0)}k€`;
  return `${n.toFixed(0)}€`;
}

const TIER_LABEL: Record<ProposalTier, string> = {
  strong: "Forte", good: "Bonne", fair: "Correcte", weak: "Faible",
};

const TIER_COLOR: Record<ProposalTier, string> = {
  strong: "text-emerald-400 bg-emerald-400/10 border-emerald-400/30",
  good: "text-sky-400 bg-sky-400/10 border-sky-400/30",
  fair: "text-amber-400 bg-amber-400/10 border-amber-400/30",
  weak: "text-red-400 bg-red-400/10 border-red-400/30",
};

const DIM_LABELS: Record<string, string> = {
  value_alignment: "Alignement valeur",
  competitive_position: "Position concurrentielle",
  relationship_strength: "Force relation",
  timing_fit: "Timing",
  proposal_quality: "Qualité prop.",
};

function TierBadge({ tier }: { tier: ProposalTier }) {
  return (
    <span className={`px-2 py-0.5 rounded-full text-[10px] font-semibold border ${TIER_COLOR[tier]}`}>
      {TIER_LABEL[tier]}
    </span>
  );
}

function DimBar({ label, score }: { label: string; score: number }) {
  const color = score >= 70 ? "bg-emerald-500" : score >= 50 ? "bg-amber-500" : "bg-red-500";
  return (
    <div className="flex items-center gap-2">
      <span className="text-[10px] text-slate-500 w-28 truncate">{label}</span>
      <div className="flex-1 h-1.5 bg-slate-700 rounded-full overflow-hidden">
        <div className={`h-full rounded-full ${color}`} style={{ width: `${score}%` }} />
      </div>
      <span className="text-[10px] text-slate-400 w-6 text-right">{Math.round(score)}</span>
    </div>
  );
}

// ─── Proposal Modal ───────────────────────────────────────────────────────────

function ProposalModal({ scored, onClose }: { scored: ScoredProposal; onClose: () => void }) {
  useEffect(() => {
    const handler = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    document.addEventListener("keydown", handler);
    return () => document.removeEventListener("keydown", handler);
  }, [onClose]);

  const p = scored.proposal;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4" onClick={onClose}>
      <div className="absolute inset-0 bg-black/60" />
      <div
        className="relative bg-slate-900 border border-slate-700 rounded-xl w-full max-w-xl shadow-2xl overflow-y-auto max-h-[90vh]"
        onClick={e => e.stopPropagation()}
      >
        <div className="p-5 border-b border-slate-800 flex items-start justify-between gap-3">
          <div>
            <h2 className="text-white font-semibold text-lg">{p.client_name}</h2>
            <p className="text-slate-400 text-sm">{p.sector} · {p.proposal_page_count} pages</p>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl leading-none p-1">×</button>
        </div>

        <div className="p-5 space-y-5">
          {/* Win probability */}
          <div className="bg-slate-800 rounded-xl p-4 text-center">
            <div className={`text-4xl font-bold ${scored.win_probability >= 0.65 ? "text-emerald-400" : scored.win_probability >= 0.50 ? "text-sky-400" : scored.win_probability >= 0.35 ? "text-amber-400" : "text-red-400"}`}>
              {Math.round(scored.win_probability * 100)}%
            </div>
            <div className="text-slate-400 text-sm mt-1">Probabilité de remporter</div>
            <div className="mt-2"><TierBadge tier={scored.proposal_tier} /></div>
          </div>

          {/* KPIs */}
          <div className="grid grid-cols-3 gap-3">
            <div className="bg-slate-800 rounded-lg p-3 text-center">
              <div className="text-lg font-bold text-white">{fmt(p.deal_value_eur)}</div>
              <div className="text-xs text-slate-400">Valeur offre</div>
            </div>
            <div className="bg-slate-800 rounded-lg p-3 text-center">
              <div className="text-lg font-bold text-indigo-400">{fmt(p.deal_value_eur * scored.win_probability)}</div>
              <div className="text-xs text-slate-400">Valeur attendue</div>
            </div>
            <div className="bg-slate-800 rounded-lg p-3 text-center">
              <div className="text-lg font-bold text-amber-400">{p.days_to_deadline}j</div>
              <div className="text-xs text-slate-400">Avant échéance</div>
            </div>
          </div>

          {/* Signals */}
          <div className="grid grid-cols-2 gap-3 text-xs">
            {[
              { label: "Concurrents", value: p.competitor_count },
              { label: "Réunions tenues", value: p.meetings_held },
              { label: "Deals précédents", value: p.previous_deals_won },
              { label: "Score relation", value: p.relationship_score },
              { label: "Prix vs marché", value: `×${p.our_price_vs_market.toFixed(2)}` },
              { label: "Budget client", value: p.client_budget_eur > 0 ? fmt(p.client_budget_eur) : "Inconnu" },
            ].map(({ label, value }) => (
              <div key={label} className="bg-slate-800 rounded-lg p-2.5">
                <div className="text-slate-500">{label}</div>
                <div className="text-white font-semibold mt-0.5">{value}</div>
              </div>
            ))}
          </div>

          {/* Flags */}
          <div className="flex flex-wrap gap-2 text-xs">
            {[
              { key: "decision_maker_reached", label: "Décideur atteint", ok: p.decision_maker_reached },
              { key: "has_roi_model", label: "ROI modélisé", ok: p.has_roi_model },
              { key: "has_case_study", label: "Étude de cas", ok: p.has_case_study },
              { key: "has_personalization", label: "Personnalisée", ok: p.has_personalization },
              { key: "has_incumbent", label: "Titulaire actuel", ok: !p.has_incumbent },
            ].map(({ key, label, ok }) => (
              <span key={key} className={`px-2 py-1 rounded-full font-medium ${ok ? "bg-emerald-900/40 text-emerald-400" : "bg-red-900/30 text-red-400"}`}>
                {ok ? "✓" : "✗"} {label}
              </span>
            ))}
          </div>

          {/* Dimension scores */}
          <div>
            <p className="text-xs font-semibold text-slate-400 uppercase tracking-wide mb-2">Scores par dimension</p>
            <div className="space-y-2">
              {Object.entries(scored.dimension_scores).map(([dim, score]) => (
                <DimBar key={dim} label={DIM_LABELS[dim] ?? dim} score={score} />
              ))}
            </div>
          </div>

          {/* Strengths */}
          {scored.strengths.length > 0 && (
            <div>
              <p className="text-xs font-semibold text-emerald-400 uppercase tracking-wide mb-2">Points forts</p>
              <ul className="space-y-1">
                {scored.strengths.map(s => (
                  <li key={s} className="flex items-start gap-2 text-xs text-slate-300">
                    <span className="text-emerald-400 mt-0.5">▲</span>{s}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Recommendations */}
          {scored.recommendations.length > 0 && (
            <div>
              <p className="text-xs font-semibold text-amber-400 uppercase tracking-wide mb-2">Recommandations</p>
              <ul className="space-y-1">
                {scored.recommendations.map(r => (
                  <li key={r} className="flex items-start gap-2 text-xs text-slate-300">
                    <span className="text-amber-400 mt-0.5">→</span>{r}
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

const TIER_FILTERS: { key: ProposalTier | "all"; label: string }[] = [
  { key: "all", label: "Tous" },
  { key: "strong", label: "Forte" },
  { key: "good", label: "Bonne" },
  { key: "fair", label: "Correcte" },
  { key: "weak", label: "Faible" },
];

export default function ProposalsPage() {
  const [data, setData] = useState<ApiData | null>(null);
  const [loading, setLoading] = useState(true);
  const [tierFilter, setTierFilter] = useState<ProposalTier | "all">("all");
  const [selected, setSelected] = useState<ScoredProposal | null>(null);

  useEffect(() => {
    async function load() {
        try {
          const res = await fetch("/api/proposals", { cache: "no-store" });
          if (res.ok) setData(await res.json());
        } finally {
          setLoading(false);
        }
  }
    load();
  }, []);

  const filtered = data?.proposals.filter(p => tierFilter === "all" || p.proposal_tier === tierFilter) ?? [];
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
            <h1 className="text-2xl font-bold text-white">Scoring Propositions IA</h1>
            <p className="text-slate-400 text-sm mt-1">
              Probabilité de remporter basée sur 5 dimensions — valeur, compétition, relation, timing, qualité
            </p>
          </div>
          {data && (
            <span className="text-xs text-slate-500">
              Mis à jour {new Date(data.last_updated).toLocaleTimeString("fr-FR")}
            </span>
          )}
        </div>

        {/* KPI strip */}
        {summary && (
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {[
              { label: "Propositions", value: `${summary.total}`, sub: "en cours", color: "text-white" },
              { label: "Pipeline Total", value: fmt(summary.total_pipeline_eur), sub: `Attendu: ${fmt(summary.expected_won_eur)}`, color: "text-emerald-400" },
              { label: "Prob. Moy.", value: `${Math.round(summary.avg_win_probability * 100)}%`, sub: `Meilleure: ${Math.round(summary.best_win_probability * 100)}%`, color: "text-indigo-400" },
              { label: "Tier Forte", value: `${summary.tier_counts.strong}`, sub: `Bonne: ${summary.tier_counts.good}`, color: "text-sky-400" },
            ].map(k => (
              <div key={k.label} className="bg-slate-900 border border-slate-800 rounded-xl p-4">
                <p className="text-xs text-slate-500 font-medium uppercase tracking-wide">{k.label}</p>
                <p className={`text-2xl font-bold mt-1 ${k.color}`}>{k.value}</p>
                <p className="text-xs text-slate-500 mt-0.5">{k.sub}</p>
              </div>
            ))}
          </div>
        )}

        <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
          {/* Proposal list */}
          <div className="xl:col-span-2 space-y-4">

            {/* Tier filters */}
            <div className="flex gap-1.5 flex-wrap">
              {TIER_FILTERS.map(f => (
                <button
                  key={f.key}
                  onClick={() => setTierFilter(f.key as ProposalTier | "all")}
                  className={`px-3 py-1 rounded-full text-xs font-medium transition-colors ${
                    tierFilter === f.key ? "bg-indigo-600 text-white" : "bg-slate-800 text-slate-400 hover:text-white"
                  }`}
                >
                  {f.label}
                  {f.key !== "all" && summary && (
                    <span className="ml-1 opacity-60">({summary.tier_counts[f.key]})</span>
                  )}
                </button>
              ))}
            </div>

            {/* Proposal cards */}
            <div className="space-y-3">
              {filtered.length === 0 && (
                <p className="text-slate-500 text-sm text-center py-8">Aucune proposition pour ce filtre</p>
              )}
              {filtered.map((scored, i) => (
                <div
                  key={scored.proposal.proposal_id}
                  onClick={() => setSelected(scored)}
                  className="bg-slate-900 border border-slate-800 rounded-xl p-4 cursor-pointer hover:border-slate-600 transition-colors"
                >
                  <div className="flex items-start justify-between gap-3 mb-3">
                    <div className="flex items-center gap-3">
                      <div className="w-7 h-7 rounded-full bg-indigo-900 flex items-center justify-center text-xs font-bold text-indigo-300 flex-shrink-0">
                        {i + 1}
                      </div>
                      <div>
                        <p className="text-white font-medium text-sm">{scored.proposal.client_name}</p>
                        <p className="text-slate-400 text-xs capitalize">{scored.proposal.sector}</p>
                      </div>
                    </div>
                    <div className="text-right flex-shrink-0">
                      <div className={`text-2xl font-bold ${scored.win_probability >= 0.65 ? "text-emerald-400" : scored.win_probability >= 0.50 ? "text-sky-400" : scored.win_probability >= 0.35 ? "text-amber-400" : "text-red-400"}`}>
                        {Math.round(scored.win_probability * 100)}%
                      </div>
                      <div className="text-xs text-slate-500">{fmt(scored.proposal.deal_value_eur)}</div>
                    </div>
                  </div>

                  {/* Mini dimension bars */}
                  <div className="grid grid-cols-3 gap-1 mb-3">
                    {Object.entries(scored.dimension_scores).map(([dim, score]) => (
                      <div key={dim} className="flex items-center gap-1">
                        <div className="flex-1 h-1 bg-slate-700 rounded-full overflow-hidden">
                          <div
                            className={`h-full rounded-full ${score >= 70 ? "bg-emerald-500" : score >= 50 ? "bg-amber-500" : "bg-red-500"}`}
                            style={{ width: `${score}%` }}
                          />
                        </div>
                      </div>
                    ))}
                  </div>

                  <div className="flex items-center gap-2 flex-wrap">
                    <TierBadge tier={scored.proposal_tier} />
                    <span className="text-xs text-slate-500">{scored.proposal.days_to_deadline}j · {scored.proposal.competitor_count} conc.</span>
                    {scored.recommendations.length > 0 && (
                      <span className="ml-auto text-xs text-amber-400">{scored.recommendations.length} recommandation{scored.recommendations.length > 1 ? "s" : ""}</span>
                    )}
                    {scored.strengths.length > 0 && scored.recommendations.length === 0 && (
                      <span className="ml-auto text-xs text-emerald-400">{scored.strengths.length} atout{scored.strengths.length > 1 ? "s" : ""}</span>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Sidebar */}
          <div className="space-y-4">

            {/* Tier distribution */}
            {summary && (
              <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
                <h3 className="text-sm font-semibold text-slate-300 mb-3">Distribution par tier</h3>
                <div className="space-y-2">
                  {(["strong", "good", "fair", "weak"] as ProposalTier[]).map(tier => {
                    const count = summary.tier_counts[tier];
                    const total = summary.total;
                    return (
                      <div key={tier} className="flex items-center gap-3">
                        <TierBadge tier={tier} />
                        <div className="flex-1 h-1.5 bg-slate-800 rounded-full overflow-hidden">
                          <div
                            className={`h-full rounded-full ${tier === "strong" ? "bg-emerald-500" : tier === "good" ? "bg-sky-500" : tier === "fair" ? "bg-amber-500" : "bg-red-500"}`}
                            style={{ width: total > 0 ? `${(count / total) * 100}%` : "0%" }}
                          />
                        </div>
                        <span className="text-xs text-slate-400 w-4 text-right">{count}</span>
                      </div>
                    );
                  })}
                </div>
              </div>
            )}

            {/* Top 3 propositions */}
            {data && data.proposals.slice(0, 3).length > 0 && (
              <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
                <h3 className="text-sm font-semibold text-slate-300 mb-3">Top opportunités</h3>
                <div className="space-y-3">
                  {data.proposals.slice(0, 3).map((scored, i) => (
                    <div key={scored.proposal.proposal_id} className="flex items-center gap-3">
                      <div className="w-5 h-5 rounded-full bg-indigo-900 flex items-center justify-center text-[10px] font-bold text-indigo-300 flex-shrink-0">
                        {i + 1}
                      </div>
                      <div className="flex-1 min-w-0">
                        <p className="text-xs text-white font-medium truncate">{scored.proposal.client_name}</p>
                        <p className="text-[10px] text-slate-500">{fmt(scored.proposal.deal_value_eur)}</p>
                      </div>
                      <span className={`text-sm font-bold ${scored.win_probability >= 0.65 ? "text-emerald-400" : "text-sky-400"}`}>
                        {Math.round(scored.win_probability * 100)}%
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Revenue summary */}
            {summary && (
              <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
                <h3 className="text-sm font-semibold text-slate-300 mb-3">Résumé revenus</h3>
                <div className="space-y-2">
                  {[
                    { label: "Pipeline total", value: fmt(summary.total_pipeline_eur), color: "text-white" },
                    { label: "Revenus attendus", value: fmt(summary.expected_won_eur), color: "text-emerald-400" },
                    { label: "Taux conversion moy.", value: `${Math.round(summary.avg_win_probability * 100)}%`, color: "text-indigo-400" },
                  ].map(({ label, value, color }) => (
                    <div key={label} className="flex justify-between">
                      <span className="text-xs text-slate-500">{label}</span>
                      <span className={`text-xs font-semibold ${color}`}>{value}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* At-risk count */}
            {summary && summary.tier_counts.weak > 0 && (
              <div className="bg-red-950/30 border border-red-800/40 rounded-xl p-4">
                <p className="text-red-400 text-sm font-semibold">
                  {summary.tier_counts.weak} proposition{summary.tier_counts.weak > 1 ? "s" : ""} à risque
                </p>
                <p className="text-red-300/70 text-xs mt-1">
                  Filtrer sur "Faible" pour voir les détails et recommandations
                </p>
              </div>
            )}
          </div>
        </div>
      </div>

      {selected && <ProposalModal scored={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
