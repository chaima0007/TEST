"use client";

import { useEffect, useState } from "react";

type Stage =
  | "prospected" | "contacted" | "qualified" | "proposal"
  | "negotiation" | "verbal_close" | "closed_won";

type Scenario = "pessimistic" | "base" | "optimistic";

interface Deal {
  deal_id: string;
  company: string;
  sector: string;
  stage: Stage;
  value_eur: number;
  days_in_stage: number;
  agent_id: string;
  close_probability: number;
  sector_multiplier: number;
  weighted_value: number;
}

interface ForecastResult {
  scenario: Scenario;
  expected_revenue: number;
  deals_count: number;
  pipeline_value: number;
  weighted_pipeline: number;
  by_stage: Record<string, number>;
  by_sector: Record<string, number>;
  confidence: number;
  rationale: string;
}

interface ForecastData {
  deals: Deal[];
  scenarios: ForecastResult[];
  stage_labels: Record<Stage, string>;
  summary: {
    total_deals: number;
    pipeline_value_eur: number;
    base_forecast: number;
    pessimistic_forecast: number;
    optimistic_forecast: number;
    confidence: number;
    by_stage_count: Record<string, number>;
    stale_count: number;
  };
  top_deals: Deal[];
  stale_deals: Deal[];
}

// ─── Constants ────────────────────────────────────────────────────────────────

const STAGE_ORDER: Stage[] = [
  "prospected", "contacted", "qualified", "proposal",
  "negotiation", "verbal_close", "closed_won",
];

const STAGE_COLORS: Record<Stage, string> = {
  prospected:   "bg-slate-700",
  contacted:    "bg-blue-800",
  qualified:    "bg-blue-600",
  proposal:     "bg-indigo-600",
  negotiation:  "bg-violet-600",
  verbal_close: "bg-emerald-600",
  closed_won:   "bg-emerald-500",
};

const SCENARIO_META: Record<Scenario, { label: string; color: string; bg: string }> = {
  pessimistic: { label: "Pessimiste", color: "text-slate-400",   bg: "bg-slate-800/60"    },
  base:        { label: "De base",    color: "text-indigo-400",  bg: "bg-indigo-950/40"   },
  optimistic:  { label: "Optimiste",  color: "text-emerald-400", bg: "bg-emerald-950/40"  },
};

const SECTOR_FLAGS: Record<string, string> = {
  avocat: "⚖", comptable: "📊", notaire: "📜", médecin: "⚕",
  dentiste: "🦷", immobilier: "🏠", restaurant: "🍽", hôtel: "🏨",
  artisan: "🔧", coiffeur: "✂", pme: "🏢",
};

// ─── Sub-components ───────────────────────────────────────────────────────────

function fmt(n: number) {
  return n.toLocaleString("fr-FR", { maximumFractionDigits: 0 }) + "€";
}

function KpiCard({ label, value, sub, accent }: { label: string; value: string; sub?: string; accent?: string }) {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
      <p className="text-xs text-slate-500 uppercase tracking-wider mb-1">{label}</p>
      <p className={`text-2xl font-black ${accent ?? "text-white"}`}>{value}</p>
      {sub && <p className="text-xs text-slate-500 mt-0.5">{sub}</p>}
    </div>
  );
}

function StageBadge({ stage, label }: { stage: Stage; label: string }) {
  return (
    <span className={`inline-block px-2 py-0.5 rounded text-xs font-medium text-white ${STAGE_COLORS[stage]}`}>
      {label}
    </span>
  );
}

function ProbabilityBar({ value }: { value: number }) {
  const pct = Math.round(value * 100);
  const color = pct >= 70 ? "bg-emerald-500" : pct >= 40 ? "bg-blue-500" : pct >= 20 ? "bg-amber-500" : "bg-slate-600";
  return (
    <div className="flex items-center gap-2">
      <div className="flex-1 h-1.5 bg-slate-800 rounded-full overflow-hidden">
        <div className={`h-1.5 rounded-full ${color}`} style={{ width: `${pct}%` }} />
      </div>
      <span className="text-xs tabular-nums text-slate-400 w-8 text-right">{pct}%</span>
    </div>
  );
}

function ScenarioCard({ result }: { result: ForecastResult }) {
  const m = SCENARIO_META[result.scenario];
  const confPct = Math.round(result.confidence * 100);
  return (
    <div className={`border border-slate-700/50 rounded-xl p-5 ${m.bg}`}>
      <div className="flex items-start justify-between mb-3">
        <div>
          <p className={`text-sm font-semibold uppercase tracking-wider ${m.color}`}>{m.label}</p>
          <p className="text-3xl font-black text-white mt-1">{fmt(result.expected_revenue)}</p>
        </div>
        <div className="text-right">
          <p className="text-xs text-slate-500">Confiance</p>
          <p className={`text-lg font-bold ${m.color}`}>{confPct}%</p>
        </div>
      </div>
      <p className="text-xs text-slate-400 leading-relaxed">{result.rationale}</p>
    </div>
  );
}

function DealModal({ deal, stageLabel, onClose }: { deal: Deal; stageLabel: string; onClose: () => void }) {
  useEffect(() => {
    const h = (e: KeyboardEvent) => e.key === "Escape" && onClose();
    window.addEventListener("keydown", h);
    return () => window.removeEventListener("keydown", h);
  }, [onClose]);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm" onClick={onClose}>
      <div
        className="bg-slate-900 border border-slate-700 rounded-2xl shadow-2xl w-full max-w-lg mx-4 p-6 space-y-4"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="flex items-start justify-between">
          <div>
            <h2 className="text-white font-bold text-lg">{deal.company}</h2>
            <p className="text-slate-400 text-sm capitalize mt-0.5">{deal.sector} · Agent {deal.agent_id}</p>
          </div>
          <StageBadge stage={deal.stage} label={stageLabel} />
        </div>

        <div className="grid grid-cols-2 gap-3">
          {[
            { label: "Valeur brute", value: fmt(deal.value_eur) },
            { label: "Valeur pondérée", value: fmt(deal.weighted_value) },
            { label: "Probabilité", value: `${Math.round(deal.close_probability * 100)}%` },
            { label: "Multiplicateur secteur", value: `×${deal.sector_multiplier.toFixed(2)}` },
          ].map(({ label, value }) => (
            <div key={label} className="bg-slate-800/60 rounded-lg p-3">
              <p className="text-xs text-slate-500 mb-0.5">{label}</p>
              <p className="text-white font-bold">{value}</p>
            </div>
          ))}
        </div>

        <div>
          <p className="text-xs text-slate-500 mb-1">Probabilité de clôture</p>
          <ProbabilityBar value={deal.close_probability} />
        </div>

        {deal.days_in_stage >= 14 && (
          <div className="bg-amber-950/30 border border-amber-800/40 rounded-lg p-3">
            <p className="text-amber-400 text-xs font-semibold">
              ⚠ Affaire en attente depuis {deal.days_in_stage} jours — risque de stagnation
            </p>
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

export default function ForecastPage() {
  const [data, setData] = useState<ForecastData | null>(null);
  const [loading, setLoading] = useState(true);
  const [selectedDeal, setSelectedDeal] = useState<Deal | null>(null);
  const [stageFilter, setStageFilter] = useState<Stage | "all">("all");

  useEffect(() => {
    setLoading(true);
    fetch("/api/forecast")
      .then((r) => r.json())
      .then(setData)
      .finally(() => setLoading(false));
  }, []);

  const s = data?.summary;
  const filteredDeals = data
    ? stageFilter === "all"
      ? data.deals
      : data.deals.filter((d) => d.stage === stageFilter)
    : [];

  return (
    <div className="p-6 space-y-6 text-slate-100">
      <div>
        <h1 className="text-2xl font-bold text-white">Prévisions de Ventes</h1>
        <p className="text-slate-400 text-sm mt-1">
          Probabilité de clôture par stade · multiplicateurs sectoriels · 3 scénarios
        </p>
      </div>

      {loading ? (
        <div className="text-slate-500 text-center py-16">Chargement…</div>
      ) : data && s ? (
        <>
          {/* KPI strip */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
            <KpiCard label="Pipeline total" value={fmt(s.pipeline_value_eur)} sub={`${s.total_deals} affaires`} />
            <KpiCard label="Prévision base" value={fmt(s.base_forecast)} accent="text-indigo-400" />
            <KpiCard label="Scénario optimiste" value={fmt(s.optimistic_forecast)} accent="text-emerald-400" />
            <KpiCard
              label="Affaires stagnantes"
              value={String(s.stale_count)}
              sub="+14 jours dans le stade"
              accent={s.stale_count > 0 ? "text-amber-400" : "text-slate-400"}
            />
          </div>

          {/* Scenario cards */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {data.scenarios.map((r) => (
              <ScenarioCard key={r.scenario} result={r} />
            ))}
          </div>

          {/* Pipeline funnel — stage breakdown */}
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
            <h3 className="text-sm font-semibold text-slate-400 uppercase tracking-wider mb-4">
              Répartition par stade
            </h3>
            <div className="space-y-2">
              {STAGE_ORDER.filter((st) => s.by_stage_count[st]).map((st) => {
                const count = s.by_stage_count[st] ?? 0;
                const maxCount = Math.max(...Object.values(s.by_stage_count));
                const widthPct = maxCount > 0 ? (count / maxCount) * 100 : 0;
                const label = data.stage_labels[st];
                return (
                  <button
                    key={st}
                    onClick={() => setStageFilter(stageFilter === st ? "all" : st)}
                    className={`w-full flex items-center gap-3 rounded-lg p-2 transition-colors text-left ${stageFilter === st ? "bg-slate-800" : "hover:bg-slate-800/50"}`}
                  >
                    <div className="w-24 text-xs text-slate-400 flex-shrink-0">{label}</div>
                    <div className="flex-1 h-5 bg-slate-800 rounded overflow-hidden">
                      <div
                        className={`h-5 rounded ${STAGE_COLORS[st]} transition-all`}
                        style={{ width: `${widthPct}%` }}
                      />
                    </div>
                    <span className="text-xs text-slate-400 w-6 text-right">{count}</span>
                  </button>
                );
              })}
            </div>
          </div>

          {/* Top deals */}
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
            <h3 className="text-sm font-semibold text-slate-400 uppercase tracking-wider mb-3">
              Top 5 affaires (valeur pondérée)
            </h3>
            <div className="space-y-2">
              {data.top_deals.map((d, i) => (
                <div key={d.deal_id} className="flex items-center gap-3 bg-slate-800/40 rounded-lg p-3">
                  <span className="text-slate-600 text-xs w-5">#{i + 1}</span>
                  <div className="flex-1 min-w-0">
                    <p className="text-white font-medium text-sm truncate">{d.company}</p>
                    <p className="text-slate-500 text-xs capitalize">{d.sector}</p>
                  </div>
                  <StageBadge stage={d.stage} label={data.stage_labels[d.stage]} />
                  <div className="text-right">
                    <p className="text-indigo-400 font-bold text-sm">{fmt(d.weighted_value)}</p>
                    <p className="text-slate-500 text-xs">{fmt(d.value_eur)} brut</p>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Deals table */}
          <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden">
            <div className="px-5 py-4 border-b border-slate-800 flex items-center justify-between">
              <h3 className="text-sm font-semibold text-slate-400 uppercase tracking-wider">
                Toutes les affaires
                {stageFilter !== "all" && (
                  <span className="ml-2 text-indigo-400 normal-case">
                    · filtre: {data.stage_labels[stageFilter]}
                  </span>
                )}
              </h3>
              {stageFilter !== "all" && (
                <button
                  onClick={() => setStageFilter("all")}
                  className="text-xs text-slate-500 hover:text-white transition-colors"
                >
                  Effacer filtre ×
                </button>
              )}
            </div>
            <table className="w-full">
              <thead>
                <tr className="border-b border-slate-800">
                  <th className="text-left py-3 px-4 text-xs text-slate-500 uppercase">Entreprise</th>
                  <th className="text-left py-3 px-4 text-xs text-slate-500 uppercase hidden md:table-cell">Secteur</th>
                  <th className="text-left py-3 px-4 text-xs text-slate-500 uppercase">Stade</th>
                  <th className="text-right py-3 px-4 text-xs text-slate-500 uppercase">Valeur</th>
                  <th className="text-left py-3 px-4 text-xs text-slate-500 uppercase w-28 hidden lg:table-cell">Prob.</th>
                  <th className="text-right py-3 px-4 text-xs text-slate-500 uppercase hidden md:table-cell">Pondérée</th>
                </tr>
              </thead>
              <tbody>
                {filteredDeals.map((d) => (
                  <tr
                    key={d.deal_id}
                    onClick={() => setSelectedDeal(d)}
                    className={`border-b border-slate-800/50 hover:bg-slate-800/40 cursor-pointer transition-colors ${d.days_in_stage >= 14 ? "border-l-2 border-l-amber-600" : ""}`}
                  >
                    <td className="py-3 px-4 text-white font-medium">{d.company}</td>
                    <td className="py-3 px-4 text-slate-400 text-sm capitalize hidden md:table-cell">{d.sector}</td>
                    <td className="py-3 px-4">
                      <StageBadge stage={d.stage} label={data.stage_labels[d.stage]} />
                    </td>
                    <td className="py-3 px-4 text-right tabular-nums text-slate-300 text-sm">{fmt(d.value_eur)}</td>
                    <td className="py-3 px-4 w-28 hidden lg:table-cell">
                      <ProbabilityBar value={d.close_probability} />
                    </td>
                    <td className="py-3 px-4 text-right tabular-nums text-indigo-400 font-semibold text-sm hidden md:table-cell">
                      {fmt(d.weighted_value)}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </>
      ) : (
        <p className="text-slate-500">Erreur de chargement.</p>
      )}

      {selectedDeal && (
        <DealModal
          deal={selectedDeal}
          stageLabel={data?.stage_labels[selectedDeal.stage] ?? selectedDeal.stage}
          onClose={() => setSelectedDeal(null)}
        />
      )}
    </div>
  );
}
