"use client";

import { useEffect, useState } from "react";

type RevenuePeriod = "monthly" | "quarterly" | "annual";
type ConfidenceLevel = "low" | "medium" | "high" | "very_high";

interface DealSignals {
  deal_id: string;
  name: string;
  company: string;
  sector: string;
  stage: string;
  deal_value_eur: number;
  probability: number;
  expected_close_days: number;
  lead_score: number;
  churn_risk_score: number;
  months_in_pipeline: number;
}

interface RevenuePrediction {
  deal: DealSignals;
  adjusted_probability: number;
  weighted_value_eur: number;
  confidence: ConfidenceLevel;
  expected_close_date_offset_days: number;
  risk_factors: string[];
  upside_factors: string[];
}

interface PeriodForecast {
  period: RevenuePeriod;
  predictions: RevenuePrediction[];
  total_pipeline_eur: number;
  expected_revenue_eur: number;
  conservative_eur: number;
  optimistic_eur: number;
  by_stage: Record<string, { count: number; pipeline_eur: number; weighted_eur: number }>;
  by_sector: Record<string, number>;
  confidence_distribution: Record<ConfidenceLevel, number>;
}

interface Summary {
  total_deals: number;
  total_pipeline_eur: number;
  expected_revenue_eur: number;
  conservative_eur: number;
  optimistic_eur: number;
  avg_adjusted_probability: number;
  at_risk_count: number;
  confidence_distribution: Record<ConfidenceLevel, number>;
}

interface ApiData {
  predictions: RevenuePrediction[];
  summary: Summary;
  quarterly: PeriodForecast;
  monthly: PeriodForecast;
  annual: PeriodForecast;
  last_updated: string;
}

// ─── Helpers ─────────────────────────────────────────────────────────────────

function fmt(n: number) {
  if (n >= 1_000_000) return `${(n / 1_000_000).toFixed(1)}M€`;
  if (n >= 1_000) return `${(n / 1_000).toFixed(0)}k€`;
  return `${n.toFixed(0)}€`;
}

function pct(n: number) {
  return `${(n * 100).toFixed(0)}%`;
}

const CONF_LABEL: Record<ConfidenceLevel, string> = {
  very_high: "Très haute",
  high: "Haute",
  medium: "Moyenne",
  low: "Faible",
};

const CONF_COLOR: Record<ConfidenceLevel, string> = {
  very_high: "text-emerald-400 bg-emerald-400/10 border-emerald-400/30",
  high: "text-sky-400 bg-sky-400/10 border-sky-400/30",
  medium: "text-amber-400 bg-amber-400/10 border-amber-400/30",
  low: "text-red-400 bg-red-400/10 border-red-400/30",
};

const STAGE_LABEL: Record<string, string> = {
  prospecting: "Prospection",
  qualified: "Qualifié",
  proposal: "Proposition",
  negotiation: "Négociation",
  closing: "Clôture",
};

const STAGE_COLOR: Record<string, string> = {
  prospecting: "bg-slate-500",
  qualified: "bg-blue-500",
  proposal: "bg-amber-500",
  negotiation: "bg-violet-500",
  closing: "bg-emerald-500",
};

function ConfBadge({ conf }: { conf: ConfidenceLevel }) {
  return (
    <span className={`px-2 py-0.5 rounded-full text-[10px] font-semibold border ${CONF_COLOR[conf]}`}>
      {CONF_LABEL[conf]}
    </span>
  );
}

function StageBadge({ stage }: { stage: string }) {
  const color = STAGE_COLOR[stage] ?? "bg-slate-600";
  return (
    <span className={`px-2 py-0.5 rounded-full text-[10px] font-semibold text-white ${color}`}>
      {STAGE_LABEL[stage] ?? stage}
    </span>
  );
}

function ProbBar({ prob, label }: { prob: number; label: string }) {
  const pctVal = Math.round(prob * 100);
  const color = pctVal >= 65 ? "bg-emerald-500" : pctVal >= 45 ? "bg-amber-500" : "bg-red-500";
  return (
    <div className="flex items-center gap-2">
      <div className="flex-1 h-1.5 bg-slate-700 rounded-full overflow-hidden">
        <div className={`h-full rounded-full transition-all ${color}`} style={{ width: `${pctVal}%` }} />
      </div>
      <span className="text-xs text-slate-400 w-8 text-right">{pctVal}%</span>
      <span className="text-xs text-slate-500 w-14 truncate">{label}</span>
    </div>
  );
}

function ScoreBar({ value, max = 100, color }: { value: number; max?: number; color: string }) {
  return (
    <div className="h-1 bg-slate-700 rounded-full overflow-hidden flex-1">
      <div className={`h-full rounded-full ${color}`} style={{ width: `${(value / max) * 100}%` }} />
    </div>
  );
}

// ─── Deal Modal ───────────────────────────────────────────────────────────────

function DealModal({ pred, onClose }: { pred: RevenuePrediction; onClose: () => void }) {
  useEffect(() => {
    const handler = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    document.addEventListener("keydown", handler);
    return () => document.removeEventListener("keydown", handler);
  }, [onClose]);

  const d = pred.deal;
  const adjPct = Math.round(pred.adjusted_probability * 100);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4" onClick={onClose}>
      <div className="absolute inset-0 bg-black/60" />
      <div
        className="relative bg-slate-900 border border-slate-700 rounded-xl w-full max-w-xl shadow-2xl overflow-y-auto max-h-[90vh]"
        onClick={e => e.stopPropagation()}
      >
        <div className="p-5 border-b border-slate-800 flex items-start justify-between gap-3">
          <div>
            <h2 className="text-white font-semibold text-lg">{d.name}</h2>
            <p className="text-slate-400 text-sm">{d.company} · {d.sector}</p>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl leading-none p-1">×</button>
        </div>

        <div className="p-5 space-y-5">
          {/* KPIs */}
          <div className="grid grid-cols-3 gap-3">
            <div className="bg-slate-800 rounded-lg p-3 text-center">
              <div className="text-xl font-bold text-white">{fmt(d.deal_value_eur)}</div>
              <div className="text-xs text-slate-400 mt-0.5">Valeur brute</div>
            </div>
            <div className="bg-slate-800 rounded-lg p-3 text-center">
              <div className="text-xl font-bold text-emerald-400">{fmt(pred.weighted_value_eur)}</div>
              <div className="text-xs text-slate-400 mt-0.5">Valeur ajustée</div>
            </div>
            <div className="bg-slate-800 rounded-lg p-3 text-center">
              <div className="text-xl font-bold text-indigo-400">{adjPct}%</div>
              <div className="text-xs text-slate-400 mt-0.5">Prob. ajustée</div>
            </div>
          </div>

          {/* Stage + Confidence */}
          <div className="flex items-center gap-3">
            <StageBadge stage={d.stage} />
            <ConfBadge conf={pred.confidence} />
            <span className="text-xs text-slate-400 ml-auto">
              Clôture dans {pred.expected_close_date_offset_days}j · {d.months_in_pipeline} mois pipeline
            </span>
          </div>

          {/* Dimension scores */}
          <div>
            <p className="text-xs font-semibold text-slate-400 uppercase tracking-wide mb-2">Signaux</p>
            <div className="space-y-2">
              <div className="flex items-center gap-2">
                <span className="text-xs text-slate-500 w-28">Probabilité base</span>
                <ScoreBar value={d.probability * 100} color="bg-indigo-500" />
                <span className="text-xs text-slate-400 w-8 text-right">{pct(d.probability)}</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-xs text-slate-500 w-28">Score lead</span>
                <ScoreBar value={d.lead_score} color="bg-emerald-500" />
                <span className="text-xs text-slate-400 w-8 text-right">{d.lead_score}</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-xs text-slate-500 w-28">Risque churn</span>
                <ScoreBar value={d.churn_risk_score} color="bg-red-500" />
                <span className="text-xs text-slate-400 w-8 text-right">{d.churn_risk_score}</span>
              </div>
            </div>
          </div>

          {/* Risk factors */}
          {pred.risk_factors.length > 0 && (
            <div>
              <p className="text-xs font-semibold text-red-400 uppercase tracking-wide mb-2">Facteurs de risque</p>
              <ul className="space-y-1">
                {pred.risk_factors.map(r => (
                  <li key={r} className="flex items-start gap-2 text-xs text-slate-300">
                    <span className="text-red-400 mt-0.5">▲</span>{r}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Upside factors */}
          {pred.upside_factors.length > 0 && (
            <div>
              <p className="text-xs font-semibold text-emerald-400 uppercase tracking-wide mb-2">Facteurs positifs</p>
              <ul className="space-y-1">
                {pred.upside_factors.map(u => (
                  <li key={u} className="flex items-start gap-2 text-xs text-slate-300">
                    <span className="text-emerald-400 mt-0.5">▲</span>{u}
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

const PERIOD_LABELS: Record<RevenuePeriod, string> = {
  monthly: "Ce mois",
  quarterly: "Ce trimestre",
  annual: "Cette année",
};

const CONF_FILTERS: { key: ConfidenceLevel | "all"; label: string }[] = [
  { key: "all", label: "Tous" },
  { key: "very_high", label: "Très haute" },
  { key: "high", label: "Haute" },
  { key: "medium", label: "Moyenne" },
  { key: "low", label: "Faible" },
];

export default function RevenuePage() {
  const [data, setData] = useState<ApiData | null>(null);
  const [loading, setLoading] = useState(true);
  const [period, setPeriod] = useState<RevenuePeriod>("quarterly");
  const [confFilter, setConfFilter] = useState<ConfidenceLevel | "all">("all");
  const [selected, setSelected] = useState<RevenuePrediction | null>(null);

  useEffect(() => {
    async function load() {
        try {
          const res = await fetch("/api/revenue", { cache: "no-store" });
          if (res.ok) setData(await res.json());
        } finally {
          setLoading(false);
        }
  }
    load();
  }, []);

  const forecast: PeriodForecast | null = data ? data[period] : null;
  const summary = data?.summary;

  const filtered = forecast
    ? (confFilter === "all" ? forecast.predictions : forecast.predictions.filter(p => p.confidence === confFilter))
    : [];

  const stageOrder = ["closing", "negotiation", "proposal", "qualified", "prospecting"];
  const maxSectorVal = forecast ? Math.max(...Object.values(forecast.by_sector), 1) : 1;

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
            <h1 className="text-2xl font-bold text-white">Prévisions Revenus IA</h1>
            <p className="text-slate-400 text-sm mt-1">
              Probabilités ajustées par score lead, risque churn et stade pipeline
            </p>
          </div>
          {data && (
            <span className="text-xs text-slate-500">
              Mis à jour {new Date(data.last_updated).toLocaleTimeString("fr-FR")}
            </span>
          )}
        </div>

        {/* Global KPIs */}
        {summary && (
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {[
              { label: "Pipeline Total", value: fmt(summary.total_pipeline_eur), sub: `${summary.total_deals} deals`, color: "text-white" },
              { label: "Revenus Attendus", value: fmt(summary.expected_revenue_eur), sub: `${Math.round(summary.avg_adjusted_probability * 100)}% prob. moy.`, color: "text-emerald-400" },
              { label: "Scénario Conservateur", value: fmt(summary.conservative_eur), sub: "×0.75", color: "text-amber-400" },
              { label: "Scénario Optimiste", value: fmt(summary.optimistic_eur), sub: "×1.25", color: "text-sky-400" },
            ].map(k => (
              <div key={k.label} className="bg-slate-900 border border-slate-800 rounded-xl p-4">
                <p className="text-xs text-slate-500 font-medium uppercase tracking-wide">{k.label}</p>
                <p className={`text-2xl font-bold mt-1 ${k.color}`}>{k.value}</p>
                <p className="text-xs text-slate-500 mt-0.5">{k.sub}</p>
              </div>
            ))}
          </div>
        )}

        {/* Period selector */}
        <div className="flex gap-2 flex-wrap">
          {(["monthly", "quarterly", "annual"] as RevenuePeriod[]).map(p => (
            <button
              key={p}
              onClick={() => setPeriod(p)}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                period === p ? "bg-indigo-600 text-white" : "bg-slate-800 text-slate-400 hover:text-white"
              }`}
            >
              {PERIOD_LABELS[p]}
            </button>
          ))}
        </div>

        <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
          {/* Left: deals list */}
          <div className="xl:col-span-2 space-y-4">

            {/* Period KPIs */}
            {forecast && (
              <div className="grid grid-cols-3 gap-3">
                {[
                  { label: "Pipeline période", value: fmt(forecast.total_pipeline_eur), color: "text-white" },
                  { label: "Revenus attendus", value: fmt(forecast.expected_revenue_eur), color: "text-emerald-400" },
                  { label: "Deals en période", value: `${forecast.predictions.length}`, color: "text-indigo-400" },
                ].map(k => (
                  <div key={k.label} className="bg-slate-900 border border-slate-800 rounded-lg p-3">
                    <p className="text-[10px] text-slate-500 uppercase tracking-wide">{k.label}</p>
                    <p className={`text-xl font-bold mt-0.5 ${k.color}`}>{k.value}</p>
                  </div>
                ))}
              </div>
            )}

            {/* Confidence filter tabs */}
            <div className="flex gap-1.5 flex-wrap">
              {CONF_FILTERS.map(f => (
                <button
                  key={f.key}
                  onClick={() => setConfFilter(f.key as ConfidenceLevel | "all")}
                  className={`px-3 py-1 rounded-full text-xs font-medium transition-colors ${
                    confFilter === f.key
                      ? "bg-indigo-600 text-white"
                      : "bg-slate-800 text-slate-400 hover:text-white"
                  }`}
                >
                  {f.label}
                  {f.key !== "all" && forecast && (
                    <span className="ml-1 opacity-60">({forecast.confidence_distribution[f.key]})</span>
                  )}
                </button>
              ))}
            </div>

            {/* Deal rows */}
            <div className="space-y-2">
              {filtered.length === 0 && (
                <p className="text-slate-500 text-sm text-center py-8">Aucun deal pour cette période / filtre</p>
              )}
              {filtered.map((pred, i) => (
                <div
                  key={pred.deal.deal_id}
                  onClick={() => setSelected(pred)}
                  className="bg-slate-900 border border-slate-800 rounded-xl p-4 cursor-pointer hover:border-slate-600 transition-colors"
                >
                  <div className="flex items-start justify-between gap-3 mb-3">
                    <div className="flex items-center gap-3">
                      <div className="w-7 h-7 rounded-full bg-indigo-900 flex items-center justify-center text-xs font-bold text-indigo-300 flex-shrink-0">
                        {i + 1}
                      </div>
                      <div>
                        <p className="text-white font-medium text-sm">{pred.deal.name}</p>
                        <p className="text-slate-400 text-xs">{pred.deal.company} · {pred.deal.sector}</p>
                      </div>
                    </div>
                    <div className="text-right flex-shrink-0">
                      <p className="text-white font-bold">{fmt(pred.weighted_value_eur)}</p>
                      <p className="text-slate-500 text-xs line-through">{fmt(pred.deal.deal_value_eur)}</p>
                    </div>
                  </div>

                  <div className="grid grid-cols-3 gap-2 mb-3">
                    <div className="text-center">
                      <div className="text-xs text-slate-500">Prob. ajustée</div>
                      <div className="text-sm font-bold text-indigo-400">{pct(pred.adjusted_probability)}</div>
                    </div>
                    <div className="text-center">
                      <div className="text-xs text-slate-500">Clôture</div>
                      <div className="text-sm font-bold text-slate-300">{pred.expected_close_date_offset_days}j</div>
                    </div>
                    <div className="text-center">
                      <div className="text-xs text-slate-500">Pipeline</div>
                      <div className="text-sm font-bold text-slate-300">{pred.deal.months_in_pipeline}m</div>
                    </div>
                  </div>

                  <div className="space-y-1">
                    <ProbBar prob={pred.adjusted_probability} label="prob. adj." />
                    <ProbBar prob={pred.deal.lead_score / 100} label="lead score" />
                  </div>

                  <div className="flex items-center gap-2 mt-3">
                    <StageBadge stage={pred.deal.stage} />
                    <ConfBadge conf={pred.confidence} />
                    {pred.risk_factors.length > 0 && (
                      <span className="ml-auto text-xs text-red-400">{pred.risk_factors.length} risque{pred.risk_factors.length > 1 ? "s" : ""}</span>
                    )}
                    {pred.upside_factors.length > 0 && pred.risk_factors.length === 0 && (
                      <span className="ml-auto text-xs text-emerald-400">{pred.upside_factors.length} atout{pred.upside_factors.length > 1 ? "s" : ""}</span>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Right sidebar: breakdowns */}
          <div className="space-y-4">

            {/* By stage */}
            {forecast && Object.keys(forecast.by_stage).length > 0 && (
              <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
                <h3 className="text-sm font-semibold text-slate-300 mb-3">Par stade</h3>
                <div className="space-y-3">
                  {stageOrder.filter(s => forecast.by_stage[s]).map(stage => {
                    const d = forecast.by_stage[stage];
                    const barPct = forecast.total_pipeline_eur > 0
                      ? (d.pipeline_eur / forecast.total_pipeline_eur) * 100
                      : 0;
                    return (
                      <div key={stage}>
                        <div className="flex items-center justify-between mb-1">
                          <span className="text-xs text-slate-400">{STAGE_LABEL[stage] ?? stage}</span>
                          <span className="text-xs text-slate-300 font-medium">{fmt(d.weighted_eur)}</span>
                        </div>
                        <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
                          <div
                            className={`h-full rounded-full ${STAGE_COLOR[stage] ?? "bg-slate-500"}`}
                            style={{ width: `${barPct}%` }}
                          />
                        </div>
                        <div className="text-[10px] text-slate-500 mt-0.5">{d.count} deal{d.count > 1 ? "s" : ""} · {fmt(d.pipeline_eur)} pipeline</div>
                      </div>
                    );
                  })}
                </div>
              </div>
            )}

            {/* By sector */}
            {forecast && Object.keys(forecast.by_sector).length > 0 && (
              <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
                <h3 className="text-sm font-semibold text-slate-300 mb-3">Par secteur</h3>
                <div className="space-y-2">
                  {Object.entries(forecast.by_sector)
                    .sort(([, a], [, b]) => b - a)
                    .map(([sector, val]) => (
                      <div key={sector}>
                        <div className="flex items-center justify-between mb-1">
                          <span className="text-xs text-slate-400 capitalize">{sector}</span>
                          <span className="text-xs text-slate-300 font-medium">{fmt(val)}</span>
                        </div>
                        <div className="h-1 bg-slate-800 rounded-full overflow-hidden">
                          <div
                            className="h-full bg-indigo-500 rounded-full"
                            style={{ width: `${(val / maxSectorVal) * 100}%` }}
                          />
                        </div>
                      </div>
                    ))}
                </div>
              </div>
            )}

            {/* Confidence distribution */}
            {forecast && (
              <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
                <h3 className="text-sm font-semibold text-slate-300 mb-3">Niveau de confiance</h3>
                <div className="space-y-2">
                  {(["very_high", "high", "medium", "low"] as ConfidenceLevel[]).map(c => {
                    const count = forecast.confidence_distribution[c];
                    const total = forecast.predictions.length;
                    return (
                      <div key={c} className="flex items-center gap-3">
                        <ConfBadge conf={c} />
                        <div className="flex-1 h-1.5 bg-slate-800 rounded-full overflow-hidden">
                          <div
                            className={`h-full rounded-full ${
                              c === "very_high" ? "bg-emerald-500" :
                              c === "high" ? "bg-sky-500" :
                              c === "medium" ? "bg-amber-500" : "bg-red-500"
                            }`}
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

            {/* At-risk alert */}
            {summary && summary.at_risk_count > 0 && (
              <div className="bg-red-950/30 border border-red-800/40 rounded-xl p-4">
                <p className="text-red-400 text-sm font-semibold">
                  {summary.at_risk_count} deal{summary.at_risk_count > 1 ? "s" : ""} à risque
                </p>
                <p className="text-red-300/70 text-xs mt-1">
                  Cliquer sur un deal pour voir les facteurs de risque détaillés
                </p>
              </div>
            )}
          </div>
        </div>
      </div>

      {selected && <DealModal pred={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
