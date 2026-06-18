"use client";

import { useEffect, useState, useCallback, useRef } from "react";

// ─── Types ────────────────────────────────────────────────────────────────────

type Deal = {
  deal_id: string;
  deal_name: string;
  amount_eur: number;
  stage: string;
  segment: string;
  close_date_days: number;
  base_win_probability_pct: number;
  adjusted_win_probability_pct: number;
  weighted_value_eur: number;
  conservative_value_eur: number;
  optimistic_value_eur: number;
  deal_risk: string;
  quarter_label: string;
  risk_factors: string[];
  upside_factors: string[];
};

type Summary = {
  total_pipeline_eur: number;
  conservative_forecast_eur: number;
  base_forecast_eur: number;
  optimistic_forecast_eur: number;
  current_quarter_pipeline_eur: number;
  next_quarter_pipeline_eur: number;
  beyond_pipeline_eur: number;
  avg_win_probability_pct: number;
  pipeline_health_score: number;
  deal_count: number;
  high_risk_count: number;
  segment_breakdown: Record<string, number>;
  stage_breakdown: Record<string, number>;
};

// ─── Meta helpers ─────────────────────────────────────────────────────────────

const RISK_META: Record<string, { label: string; color: string; dot: string; bg: string }> = {
  none:   { label: "Solide",   color: "text-emerald-400", dot: "bg-emerald-400", bg: "bg-emerald-900/30" },
  low:    { label: "Faible",   color: "text-blue-400",    dot: "bg-blue-400",    bg: "bg-blue-900/30"    },
  medium: { label: "Moyen",    color: "text-amber-400",   dot: "bg-amber-400",   bg: "bg-amber-900/30"   },
  high:   { label: "Élevé",   color: "text-red-400",     dot: "bg-red-400",     bg: "bg-red-900/30"     },
};

const QUARTER_META: Record<string, { label: string; color: string }> = {
  current_quarter: { label: "Ce trimestre",    color: "text-emerald-400" },
  next_quarter:    { label: "Prochain trim.",   color: "text-blue-400"    },
  beyond:          { label: "Au-delà",          color: "text-slate-400"   },
};

const STAGE_LABELS: Record<string, string> = {
  prospecting:  "Prospection",
  qualification:"Qualification",
  demo:         "Démo",
  proposal:     "Proposition",
  negotiation:  "Négociation",
  closing:      "Clôture",
};

const SEGMENT_LABELS: Record<string, string> = {
  startup:    "Startup",
  smb:        "PME",
  mid_market: "Mid-Market",
  enterprise: "Enterprise",
};

const RISK_ORDER = ["all", "none", "low", "medium", "high"];

function fmt(n: number) {
  return new Intl.NumberFormat("fr-FR", { style: "currency", currency: "EUR", maximumFractionDigits: 0 }).format(n);
}

// ─── ProbabilityBar ───────────────────────────────────────────────────────────

function ProbabilityBar({ base, adjusted }: { base: number; adjusted: number }) {
  return (
    <div className="relative h-2 bg-slate-700 rounded-full overflow-hidden">
      <div className="absolute inset-y-0 left-0 bg-slate-600 rounded-full" style={{ width: `${base}%` }} />
      <div
        className={`absolute inset-y-0 left-0 rounded-full ${adjusted >= base ? "bg-indigo-400" : "bg-orange-400"}`}
        style={{ width: `${adjusted}%` }}
      />
    </div>
  );
}

// ─── DealModal ────────────────────────────────────────────────────────────────

function DealModal({ deal, onClose }: { deal: Deal; onClose: () => void }) {
  const overlayRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleKey = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", handleKey);
    return () => window.removeEventListener("keydown", handleKey);
  }, [onClose]);

  const rm = RISK_META[deal.deal_risk] ?? RISK_META.medium;
  const qm = QUARTER_META[deal.quarter_label] ?? QUARTER_META.beyond;

  return (
    <div
      ref={overlayRef}
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm p-4"
      onClick={(e) => { if (e.target === overlayRef.current) onClose(); }}
    >
      <div className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-2xl max-h-[90vh] overflow-y-auto shadow-2xl">
        {/* Header */}
        <div className="flex items-start justify-between p-6 border-b border-slate-800">
          <div>
            <h2 className="text-white font-bold text-lg leading-tight">{deal.deal_name}</h2>
            <div className="flex flex-wrap items-center gap-2 mt-2">
              <span className={`text-xs font-semibold px-2 py-0.5 rounded-full ${rm.bg} ${rm.color}`}>
                Risque {rm.label}
              </span>
              <span className={`text-xs ${qm.color}`}>{qm.label}</span>
              <span className="text-slate-400 text-xs">{STAGE_LABELS[deal.stage] ?? deal.stage}</span>
              <span className="text-slate-400 text-xs">{SEGMENT_LABELS[deal.segment] ?? deal.segment}</span>
              {deal.close_date_days < 0 && (
                <span className="text-xs text-red-400 font-semibold">
                  En retard de {-deal.close_date_days}j
                </span>
              )}
            </div>
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-white transition-colors mt-1">
            <svg className="w-5 h-5" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
            </svg>
          </button>
        </div>

        <div className="p-6 space-y-6">
          {/* Scenario forecasts */}
          <div>
            <h3 className="text-slate-300 text-sm font-semibold mb-3">Valeur par scénario</h3>
            <div className="grid grid-cols-3 gap-3">
              {[
                { label: "Conservateur", value: deal.conservative_value_eur, color: "text-slate-300" },
                { label: "Base",         value: deal.weighted_value_eur,      color: "text-indigo-300" },
                { label: "Optimiste",    value: deal.optimistic_value_eur,    color: "text-emerald-300" },
              ].map(({ label, value, color }) => (
                <div key={label} className="bg-slate-800/60 rounded-xl p-3 text-center">
                  <p className="text-slate-500 text-xs mb-1">{label}</p>
                  <p className={`font-bold text-sm ${color}`}>{fmt(value)}</p>
                </div>
              ))}
            </div>
          </div>

          {/* Win probability */}
          <div>
            <h3 className="text-slate-300 text-sm font-semibold mb-3">Probabilité de succès</h3>
            <div className="space-y-3">
              <div>
                <div className="flex justify-between text-xs text-slate-400 mb-1.5">
                  <span>Base (étape)</span>
                  <span>{deal.base_win_probability_pct.toFixed(0)}%</span>
                </div>
                <div className="h-1.5 bg-slate-700 rounded-full overflow-hidden">
                  <div className="h-full bg-slate-500 rounded-full" style={{ width: `${deal.base_win_probability_pct}%` }} />
                </div>
              </div>
              <div>
                <div className="flex justify-between text-xs text-slate-400 mb-1.5">
                  <span>Ajustée (qualité deal)</span>
                  <span className="text-indigo-300 font-semibold">{deal.adjusted_win_probability_pct.toFixed(0)}%</span>
                </div>
                <div className="h-1.5 bg-slate-700 rounded-full overflow-hidden">
                  <div
                    className={`h-full rounded-full ${deal.adjusted_win_probability_pct >= deal.base_win_probability_pct ? "bg-indigo-500" : "bg-orange-500"}`}
                    style={{ width: `${deal.adjusted_win_probability_pct}%` }}
                  />
                </div>
              </div>
            </div>
          </div>

          {/* Upside factors */}
          {deal.upside_factors.length > 0 && (
            <div>
              <h3 className="text-slate-300 text-sm font-semibold mb-3">Facteurs positifs</h3>
              <ul className="space-y-1.5">
                {deal.upside_factors.map((u, i) => (
                  <li key={i} className="flex items-start gap-2 text-xs text-emerald-300">
                    <span className="text-emerald-400 mt-0.5 flex-shrink-0">✓</span>
                    {u}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Risk factors */}
          {deal.risk_factors.length > 0 && (
            <div>
              <h3 className="text-slate-300 text-sm font-semibold mb-3">Facteurs de risque</h3>
              <ul className="space-y-1.5">
                {deal.risk_factors.map((r, i) => (
                  <li key={i} className="flex items-start gap-2 text-xs text-orange-300">
                    <span className="text-orange-400 mt-0.5 flex-shrink-0">⚠</span>
                    {r}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Pipeline amount */}
          <div className="flex items-center justify-between p-3 bg-slate-800/60 rounded-xl">
            <div>
              <p className="text-slate-400 text-xs">Montant pipeline</p>
              <p className="text-white font-bold">{fmt(deal.amount_eur)}</p>
            </div>
            <div className="text-right">
              <p className="text-slate-400 text-xs">Valeur pondérée (base)</p>
              <p className="text-indigo-300 font-bold">{fmt(deal.weighted_value_eur)}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

// ─── DealCard ─────────────────────────────────────────────────────────────────

function DealCard({ deal, onClick }: { deal: Deal; onClick: () => void }) {
  const rm = RISK_META[deal.deal_risk] ?? RISK_META.medium;
  const qm = QUARTER_META[deal.quarter_label] ?? QUARTER_META.beyond;

  return (
    <button
      onClick={onClick}
      className="w-full text-left bg-slate-800/60 border border-slate-700/50 rounded-2xl p-5 hover:border-indigo-500/50 hover:bg-slate-800 transition-all group"
    >
      <div className="flex items-start justify-between gap-2 mb-3">
        <p className="text-white font-semibold text-sm group-hover:text-indigo-300 transition-colors leading-tight">
          {deal.deal_name}
        </p>
        <span className={`text-xs font-semibold px-2 py-0.5 rounded-full flex-shrink-0 ${rm.bg} ${rm.color}`}>
          {rm.label}
        </span>
      </div>

      <div className="flex flex-wrap items-center gap-2 text-xs text-slate-400 mb-3">
        <span className={qm.color}>{qm.label}</span>
        <span>•</span>
        <span>{STAGE_LABELS[deal.stage] ?? deal.stage}</span>
        <span>•</span>
        <span>{SEGMENT_LABELS[deal.segment] ?? deal.segment}</span>
        {deal.close_date_days < 0 && (
          <span className="text-red-400 font-semibold">Retard {-deal.close_date_days}j</span>
        )}
      </div>

      {/* Win probability bar */}
      <div className="mb-3">
        <div className="flex justify-between text-[10px] text-slate-500 mb-1">
          <span>Prob. base → ajustée</span>
          <span>
            {deal.base_win_probability_pct.toFixed(0)}% →{" "}
            <span className="text-slate-300">{deal.adjusted_win_probability_pct.toFixed(0)}%</span>
          </span>
        </div>
        <ProbabilityBar base={deal.base_win_probability_pct} adjusted={deal.adjusted_win_probability_pct} />
      </div>

      {/* Value row */}
      <div className="grid grid-cols-3 gap-2 text-center">
        <div>
          <p className="text-[10px] text-slate-500 mb-0.5">Pipeline</p>
          <p className="text-xs text-slate-300 font-medium">{fmt(deal.amount_eur)}</p>
        </div>
        <div>
          <p className="text-[10px] text-slate-500 mb-0.5">Base</p>
          <p className="text-xs text-indigo-300 font-medium">{fmt(deal.weighted_value_eur)}</p>
        </div>
        <div>
          <p className="text-[10px] text-slate-500 mb-0.5">Optimiste</p>
          <p className="text-xs text-emerald-300 font-medium">{fmt(deal.optimistic_value_eur)}</p>
        </div>
      </div>
    </button>
  );
}

// ─── Page ─────────────────────────────────────────────────────────────────────

export default function RevenueForecastPage() {
  const [deals, setDeals] = useState<Deal[]>([]);
  const [summary, setSummary] = useState<Summary | null>(null);
  const [riskFilter, setRiskFilter] = useState("all");
  const [selected, setSelected] = useState<Deal | null>(null);
  const [loading, setLoading] = useState(true);

  const fetchData = useCallback(async (risk: string) => {
    setLoading(true);
    try {
      const params = new URLSearchParams();
      if (risk !== "all") params.set("risk", risk);
      const res = await fetch(`/api/revenue-forecaster?${params}`);
      const data = await res.json();
      setDeals(data.deals ?? []);
      setSummary(data.summary ?? null);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { fetchData(riskFilter); }, [fetchData, riskFilter]);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 lg:p-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-white">Prévisions de Revenus</h1>
        <p className="text-slate-400 text-sm mt-1">
          Forecast probabiliste du pipeline — scénarios conservateur, base et optimiste
        </p>
      </div>

      {/* Scenario forecast strip */}
      {summary && (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 mb-8">
          {[
            { label: "Scénario Conservateur",   value: summary.conservative_forecast_eur, sub: "70% prob. ajustée", color: "text-slate-300",   border: "border-slate-700" },
            { label: "Scénario Base",            value: summary.base_forecast_eur,         sub: "prob. ajustée",     color: "text-indigo-300",  border: "border-indigo-700/50" },
            { label: "Scénario Optimiste",       value: summary.optimistic_forecast_eur,   sub: "130% prob. ajustée",color: "text-emerald-300", border: "border-emerald-700/50" },
          ].map(({ label, value, sub, color, border }) => (
            <div key={label} className={`bg-slate-800/60 border ${border} rounded-2xl p-6`}>
              <p className="text-slate-400 text-xs mb-1">{label}</p>
              <p className={`text-3xl font-bold ${color}`}>{fmt(value)}</p>
              <p className="text-slate-500 text-xs mt-1">{sub}</p>
            </div>
          ))}
        </div>
      )}

      {/* KPI strip */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        {[
          { label: "Pipeline total",      value: summary ? fmt(summary.total_pipeline_eur)  : "—", sub: `${summary?.deal_count ?? 0} deals` },
          { label: "Prob. moy. ajustée",  value: summary ? `${summary.avg_win_probability_pct}%` : "—", sub: "qualité pipeline" },
          { label: "Score santé pipeline",value: summary ? `${summary.pipeline_health_score}/100` : "—", sub: "indice qualité global" },
          { label: "Deals à risque élevé",value: summary?.high_risk_count ?? "—",               sub: "à surveiller" },
        ].map(({ label, value, sub }) => (
          <div key={label} className="bg-slate-800/60 border border-slate-700/50 rounded-2xl p-5">
            <p className="text-slate-400 text-xs mb-1">{label}</p>
            <p className="text-white text-2xl font-bold">{value}</p>
            <p className="text-slate-500 text-xs mt-1">{sub}</p>
          </div>
        ))}
      </div>

      {/* Quarter breakdown */}
      {summary && (
        <div className="bg-slate-800/60 border border-slate-700/50 rounded-2xl p-5 mb-8">
          <h2 className="text-slate-300 text-sm font-semibold mb-4">Forecast par trimestre (scénario base)</h2>
          <div className="grid grid-cols-3 gap-4">
            {[
              { label: "Ce trimestre",  value: summary.current_quarter_pipeline_eur, color: "text-emerald-400" },
              { label: "Prochain trim.",value: summary.next_quarter_pipeline_eur,    color: "text-blue-400"    },
              { label: "Au-delà",       value: summary.beyond_pipeline_eur,          color: "text-slate-400"   },
            ].map(({ label, value, color }) => (
              <div key={label} className="text-center p-3 bg-slate-900/40 rounded-xl">
                <p className="text-slate-500 text-xs mb-1">{label}</p>
                <p className={`font-bold text-lg ${color}`}>{fmt(value)}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Risk filter tabs */}
      <div className="flex flex-wrap gap-2 mb-6">
        {RISK_ORDER.map((r) => {
          const isAll = r === "all";
          const count = isAll
            ? (summary?.deal_count ?? 0)
            : (deals.length > 0 && riskFilter !== "all"
              ? (riskFilter === r ? deals.length : 0)
              : deals.filter((d) => d.deal_risk === r).length);
          const active = riskFilter === r;
          const meta = isAll ? null : RISK_META[r];
          return (
            <button
              key={r}
              onClick={() => setRiskFilter(r)}
              className={`px-4 py-2 rounded-full text-sm font-medium transition-all flex items-center gap-2 ${
                active
                  ? "bg-indigo-600 text-white"
                  : "bg-slate-800 text-slate-400 hover:text-white hover:bg-slate-700"
              }`}
            >
              {meta && <div className={`w-2 h-2 rounded-full ${meta.dot}`} />}
              {isAll ? "Tous" : meta?.label}
              <span className={`text-xs px-1.5 py-0.5 rounded-full ${active ? "bg-white/20" : "bg-slate-700"}`}>
                {count}
              </span>
            </button>
          );
        })}
      </div>

      {/* Deal grid */}
      {loading ? (
        <div className="flex justify-center py-20">
          <div className="w-8 h-8 border-2 border-indigo-500 border-t-transparent rounded-full animate-spin" />
        </div>
      ) : deals.length === 0 ? (
        <div className="text-center py-20 text-slate-500">Aucun deal pour ce filtre</div>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-4">
          {deals.map((deal) => (
            <DealCard key={deal.deal_id} deal={deal} onClick={() => setSelected(deal)} />
          ))}
        </div>
      )}

      {/* Modal */}
      {selected && <DealModal deal={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
