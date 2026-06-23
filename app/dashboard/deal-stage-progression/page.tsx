"use client";

import { useState, useEffect } from "react";

// ─── Types ────────────────────────────────────────────────────────────────────

interface DealResult {
  deal_id: string;
  deal_name: string;
  rep_id: string;
  rep_name: string;
  account_name: string;
  current_stage: string;
  previous_stage: string | null;
  deal_size_eur: number;
  progression_risk: string;
  progression_action: string;
  close_quarter_probability: string;
  progression_score: number;
  stage_velocity_ratio: number;
  days_over_benchmark: number;
  estimated_stages_remaining: int;
  estimated_days_to_close: number;
  stall_reasons: string[];
  next_actions: string[];
  close_quarter_drivers: string[];
}

type int = number;

interface Summary {
  total: number;
  risk_counts: Record<string, number>;
  action_counts: Record<string, number>;
  probability_counts: Record<string, number>;
  avg_progression_score: number;
  total_pipeline_eur: number;
  high_prob_pipeline_eur: number;
  stuck_pipeline_eur: number;
  stuck_count: number;
  rescue_count: number;
}

// ─── Helpers ──────────────────────────────────────────────────────────────────

function formatEur(n: number): string {
  if (n >= 1_000_000) return `${(n / 1_000_000).toFixed(1)}M€`;
  if (n >= 1_000)     return `${Math.round(n / 1_000)}k€`;
  return `${Math.round(n)}€`;
}

function riskColor(risk: string): string {
  switch (risk) {
    case "on_track":  return "text-emerald-400";
    case "slowing":   return "text-amber-400";
    case "stuck":     return "text-orange-400";
    case "regressed": return "text-red-400";
    default:          return "text-slate-400";
  }
}

function riskBg(risk: string): string {
  switch (risk) {
    case "on_track":  return "bg-emerald-500/15 border-emerald-500/30";
    case "slowing":   return "bg-amber-500/15 border-amber-500/30";
    case "stuck":     return "bg-orange-500/15 border-orange-500/30";
    case "regressed": return "bg-red-500/15 border-red-500/30";
    default:          return "bg-slate-700/30 border-slate-600/30";
  }
}

function riskLabel(risk: string): string {
  switch (risk) {
    case "on_track":  return "En trajectoire";
    case "slowing":   return "Ralentit";
    case "stuck":     return "Bloqué";
    case "regressed": return "Régressé";
    default:          return risk;
  }
}

function probColor(prob: string): string {
  switch (prob) {
    case "high":     return "#10b981";
    case "medium":   return "#6366f1";
    case "low":      return "#f59e0b";
    case "very_low": return "#ef4444";
    default:         return "#64748b";
  }
}

function probLabel(prob: string): string {
  switch (prob) {
    case "high":     return "Élevée";
    case "medium":   return "Moyenne";
    case "low":      return "Faible";
    case "very_low": return "Très faible";
    default:         return prob;
  }
}

function actionLabel(action: string): string {
  switch (action) {
    case "maintain":     return "Maintenir";
    case "accelerate":   return "Accélérer";
    case "rescue":       return "Sauvetage";
    case "close_now":    return "Closer maintenant";
    case "reprioritise": return "Déprioriser";
    default:             return action;
  }
}

function actionBadgeColor(action: string): string {
  switch (action) {
    case "maintain":     return "bg-emerald-500/20 text-emerald-300 border-emerald-500/30";
    case "accelerate":   return "bg-amber-500/20 text-amber-300 border-amber-500/30";
    case "rescue":       return "bg-orange-500/20 text-orange-300 border-orange-500/30";
    case "close_now":    return "bg-indigo-500/20 text-indigo-300 border-indigo-500/30";
    case "reprioritise": return "bg-red-500/20 text-red-300 border-red-500/30";
    default:             return "bg-slate-700/30 text-slate-300 border-slate-600/30";
  }
}

function stageLabel(stage: string): string {
  switch (stage) {
    case "prospecting":   return "Prospection";
    case "qualification": return "Qualification";
    case "demo":          return "Démo";
    case "proposal":      return "Proposition";
    case "negotiation":   return "Négociation";
    case "closing":       return "Closing";
    default:              return stage;
  }
}

const STAGE_ORDER = ["prospecting", "qualification", "demo", "proposal", "negotiation", "closing"];

// ─── Score Ring SVG ───────────────────────────────────────────────────────────

function ScoreRing({
  score,
  probability,
  size = 80,
}: {
  score: number;
  probability: string;
  size?: number;
}) {
  const cx = size / 2;
  const cy = size / 2;
  const r  = (size - 10) / 2;
  const circ = 2 * Math.PI * r;
  const arc  = (score / 100) * circ;
  const color = probColor(probability);

  return (
    <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`} className="flex-shrink-0">
      {/* Track */}
      <circle
        cx={cx} cy={cy} r={r}
        fill="none"
        stroke="#1e293b"
        strokeWidth="8"
      />
      {/* Progress */}
      <circle
        cx={cx} cy={cy} r={r}
        fill="none"
        stroke={color}
        strokeWidth="8"
        strokeDasharray={`${arc} ${circ - arc}`}
        strokeLinecap="round"
        transform={`rotate(-90 ${cx} ${cy})`}
      />
      {/* Label */}
      <text x={cx} y={cy - 4} textAnchor="middle" fill="white" fontSize={size * 0.22} fontWeight="bold">
        {Math.round(score)}
      </text>
      <text x={cx} y={cy + size * 0.14} textAnchor="middle" fill="#94a3b8" fontSize={size * 0.13}>
        score
      </text>
    </svg>
  );
}

// ─── Stage Pipeline Bar ───────────────────────────────────────────────────────

function StagePipelineBar({ stage }: { stage: string }) {
  const idx = STAGE_ORDER.indexOf(stage);
  return (
    <div className="flex items-center gap-1 mt-1">
      {STAGE_ORDER.map((s, i) => (
        <div
          key={s}
          title={stageLabel(s)}
          className={`h-1.5 flex-1 rounded-full transition-all ${
            i < idx
              ? "bg-indigo-600/50"
              : i === idx
              ? "bg-indigo-400"
              : "bg-slate-700"
          }`}
        />
      ))}
    </div>
  );
}

// ─── Risk Distribution Bar ────────────────────────────────────────────────────

function RiskDistributionBar({ counts, total }: { counts: Record<string, number>; total: number }) {
  const risks = [
    { key: "on_track",  label: "En trajectoire", color: "bg-emerald-500" },
    { key: "slowing",   label: "Ralentit",        color: "bg-amber-500" },
    { key: "stuck",     label: "Bloqué",          color: "bg-orange-500" },
    { key: "regressed", label: "Régressé",        color: "bg-red-500" },
  ];

  return (
    <div className="space-y-2">
      <div className="flex h-3 rounded-full overflow-hidden gap-0.5">
        {risks.map(({ key, color }) => {
          const pct = total > 0 ? ((counts[key] || 0) / total) * 100 : 0;
          return pct > 0 ? (
            <div key={key} className={`${color} h-full`} style={{ width: `${pct}%` }} title={`${counts[key] || 0}`} />
          ) : null;
        })}
      </div>
      <div className="flex gap-4 flex-wrap">
        {risks.map(({ key, label, color }) => (
          <div key={key} className="flex items-center gap-1.5">
            <div className={`w-2.5 h-2.5 rounded-full ${color}`} />
            <span className="text-xs text-slate-400">{label} <span className="text-white font-medium">{counts[key] || 0}</span></span>
          </div>
        ))}
      </div>
    </div>
  );
}

// ─── Deal Modal ───────────────────────────────────────────────────────────────

function DealModal({ deal, onClose }: { deal: DealResult; onClose: () => void }) {
  const [tab, setTab] = useState<"stalls" | "actions" | "drivers">("actions");

  useEffect(() => {
    const handler = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    document.addEventListener("keydown", handler);
    return () => document.removeEventListener("keydown", handler);
  }, [onClose]);

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm"
      onClick={onClose}
    >
      <div
        className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-2xl max-h-[90vh] overflow-y-auto shadow-2xl"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="p-6 border-b border-slate-800">
          <div className="flex items-start justify-between gap-4">
            <div className="min-w-0">
              <h2 className="text-lg font-semibold text-white truncate">{deal.deal_name}</h2>
              <p className="text-sm text-slate-400 mt-0.5">{deal.account_name} — {deal.rep_name}</p>
            </div>
            <button onClick={onClose} className="text-slate-500 hover:text-white text-xl leading-none mt-0.5 flex-shrink-0">×</button>
          </div>

          {/* Stage progression */}
          <div className="mt-4">
            <div className="flex items-center justify-between mb-1">
              <span className="text-xs text-slate-500">Étape actuelle</span>
              <span className="text-xs font-medium text-indigo-400">{stageLabel(deal.current_stage)}</span>
            </div>
            <StagePipelineBar stage={deal.current_stage} />
          </div>

          {/* KPIs */}
          <div className="grid grid-cols-4 gap-3 mt-4">
            <div className="bg-slate-800/60 rounded-lg p-3 text-center">
              <p className="text-lg font-bold text-white">{Math.round(deal.progression_score)}</p>
              <p className="text-xs text-slate-400 mt-0.5">Score</p>
            </div>
            <div className="bg-slate-800/60 rounded-lg p-3 text-center">
              <p className={`text-lg font-bold ${deal.stage_velocity_ratio <= 1 ? "text-emerald-400" : deal.stage_velocity_ratio <= 1.5 ? "text-amber-400" : "text-red-400"}`}>
                {deal.stage_velocity_ratio.toFixed(1)}×
              </p>
              <p className="text-xs text-slate-400 mt-0.5">Vélocité</p>
            </div>
            <div className="bg-slate-800/60 rounded-lg p-3 text-center">
              <p className="text-lg font-bold text-white">{deal.estimated_days_to_close}j</p>
              <p className="text-xs text-slate-400 mt-0.5">Est. closing</p>
            </div>
            <div className="bg-slate-800/60 rounded-lg p-3 text-center">
              <p className="text-lg font-bold text-white">{formatEur(deal.deal_size_eur)}</p>
              <p className="text-xs text-slate-400 mt-0.5">Valeur</p>
            </div>
          </div>

          {/* Risk + Prob badges */}
          <div className="flex gap-2 mt-3">
            <span className={`text-xs px-3 py-1 rounded-full border font-medium ${riskBg(deal.progression_risk)} ${riskColor(deal.progression_risk)}`}>
              {riskLabel(deal.progression_risk)}
            </span>
            <span className={`text-xs px-3 py-1 rounded-full border font-medium ${actionBadgeColor(deal.progression_action)}`}>
              {actionLabel(deal.progression_action)}
            </span>
            <span className="text-xs px-3 py-1 rounded-full border border-slate-600/40 bg-slate-700/30 text-slate-300 font-medium">
              Proba. {probLabel(deal.close_quarter_probability)}
            </span>
          </div>
        </div>

        {/* Tabs */}
        <div className="border-b border-slate-800 flex">
          {(["actions", "stalls", "drivers"] as const).map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`flex-1 py-3 text-sm font-medium transition-colors ${
                tab === t ? "text-indigo-400 border-b-2 border-indigo-500" : "text-slate-500 hover:text-slate-300"
              }`}
            >
              {t === "actions" ? "Plan d'action" : t === "stalls" ? "Signaux de blocage" : "Moteurs de closing"}
            </button>
          ))}
        </div>

        {/* Tab content */}
        <div className="p-6 space-y-2">
          {tab === "actions" && (
            deal.next_actions.length === 0 ? (
              <p className="text-sm text-slate-500">Aucune action requise.</p>
            ) : (
              deal.next_actions.map((a, i) => (
                <div key={i} className="flex gap-3 items-start">
                  <div className="w-5 h-5 rounded-full bg-indigo-600/30 border border-indigo-500/40 flex items-center justify-center flex-shrink-0 mt-0.5">
                    <span className="text-[10px] text-indigo-300 font-bold">{i + 1}</span>
                  </div>
                  <p className="text-sm text-slate-300">{a}</p>
                </div>
              ))
            )
          )}
          {tab === "stalls" && (
            deal.stall_reasons.length === 0 ? (
              <p className="text-sm text-slate-500">Aucun signal de blocage détecté.</p>
            ) : (
              deal.stall_reasons.map((r, i) => (
                <div key={i} className="flex gap-3 items-start">
                  <div className="w-1.5 h-1.5 rounded-full bg-orange-400 mt-2 flex-shrink-0" />
                  <p className="text-sm text-slate-300">{r}</p>
                </div>
              ))
            )
          )}
          {tab === "drivers" && (
            deal.close_quarter_drivers.map((d, i) => (
              <div key={i} className="flex gap-3 items-start">
                <div className="w-1.5 h-1.5 rounded-full bg-emerald-400 mt-2 flex-shrink-0" />
                <p className="text-sm text-slate-300">{d}</p>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}

// ─── Deal Card ────────────────────────────────────────────────────────────────

function DealCard({ deal, onClick }: { deal: DealResult; onClick: () => void }) {
  return (
    <button
      onClick={onClick}
      className={`w-full text-left p-4 rounded-xl border transition-all hover:border-indigo-500/40 hover:bg-slate-800/60 ${riskBg(deal.progression_risk)}`}
    >
      <div className="flex items-start gap-4">
        <ScoreRing score={deal.progression_score} probability={deal.close_quarter_probability} size={72} />

        <div className="flex-1 min-w-0">
          <div className="flex items-start justify-between gap-2">
            <div className="min-w-0">
              <h3 className="text-sm font-semibold text-white truncate">{deal.deal_name}</h3>
              <p className="text-xs text-slate-400 mt-0.5 truncate">{deal.account_name} · {deal.rep_name}</p>
            </div>
            <span className="text-sm font-bold text-white flex-shrink-0">{formatEur(deal.deal_size_eur)}</span>
          </div>

          <StagePipelineBar stage={deal.current_stage} />

          <div className="flex items-center gap-2 mt-2 flex-wrap">
            <span className={`text-xs font-medium ${riskColor(deal.progression_risk)}`}>
              {riskLabel(deal.progression_risk)}
            </span>
            <span className="text-slate-600">·</span>
            <span className={`text-xs px-2 py-0.5 rounded-full border ${actionBadgeColor(deal.progression_action)}`}>
              {actionLabel(deal.progression_action)}
            </span>
            <span className="text-slate-600">·</span>
            <span className="text-xs text-slate-400">
              Proba. <span className="text-slate-200 font-medium">{probLabel(deal.close_quarter_probability)}</span>
            </span>
          </div>

          <div className="flex items-center gap-3 mt-1.5 text-xs text-slate-500">
            <span>Vélocité <span className={deal.stage_velocity_ratio <= 1 ? "text-emerald-400" : deal.stage_velocity_ratio <= 1.5 ? "text-amber-400" : "text-red-400"}>
              {deal.stage_velocity_ratio.toFixed(1)}×
            </span></span>
            <span>·</span>
            <span>Est. closing <span className="text-slate-300">{deal.estimated_days_to_close}j</span></span>
            {deal.days_over_benchmark > 0 && (
              <>
                <span>·</span>
                <span className="text-orange-400">+{deal.days_over_benchmark}j retard</span>
              </>
            )}
          </div>
        </div>
      </div>
    </button>
  );
}

// ─── Page ─────────────────────────────────────────────────────────────────────

export default function DealStageProgressionPage() {
  const [deals, setDeals] = useState<DealResult[]>([]);
  const [summary, setSummary] = useState<Summary | null>(null);
  const [loading, setLoading] = useState(true);
  const [selected, setSelected] = useState<DealResult | null>(null);
  const [riskFilter, setRiskFilter]   = useState("all");
  const [actionFilter, setActionFilter] = useState("all");

  useEffect(() => {
    async function load() {
        setLoading(true);
        try {
          const params = new URLSearchParams();
          if (riskFilter !== "all")   params.set("risk", riskFilter);
          if (actionFilter !== "all") params.set("action", actionFilter);
          const res = await fetch(`/api/deal-stage-progression?${params}`);
          const data = await res.json();
          setDeals(data.deals ?? []);
          setSummary(data.summary ?? null);
        } catch {}
        setLoading(false);
  }
    load();
  }, [riskFilter, actionFilter]);

  const RISK_TABS = [
    { key: "all",       label: "Tous" },
    { key: "on_track",  label: "En trajectoire" },
    { key: "slowing",   label: "Ralentit" },
    { key: "stuck",     label: "Bloqué" },
    { key: "regressed", label: "Régressé" },
  ];

  const ACTION_TABS = [
    { key: "all",         label: "Toutes actions" },
    { key: "close_now",   label: "Closer" },
    { key: "maintain",    label: "Maintenir" },
    { key: "accelerate",  label: "Accélérer" },
    { key: "rescue",      label: "Sauvetage" },
    { key: "reprioritise", label: "Déprioriser" },
  ];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">

        {/* Header */}
        <div>
          <h1 className="text-2xl font-bold text-white">Progression des Deals</h1>
          <p className="text-sm text-slate-400 mt-1">
            Analyse de la vélocité par étape · Détection des blocages · Probabilité de closing trimestriel
          </p>
        </div>

        {/* KPI strip */}
        {summary && (
          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-4">
            {[
              { label: "Deals suivis",    value: String(summary.total) },
              { label: "Score moy.",      value: String(summary.avg_progression_score) },
              { label: "Pipeline total",  value: formatEur(summary.total_pipeline_eur) },
              { label: "Haute proba.",    value: formatEur(summary.high_prob_pipeline_eur), accent: true },
              { label: "Deals bloqués",   value: String(summary.stuck_count), warn: true },
              { label: "Deals à sauver",  value: String(summary.rescue_count), warn: summary.rescue_count > 0 },
            ].map(({ label, value, accent, warn }) => (
              <div key={label} className="bg-slate-900 border border-slate-800 rounded-xl p-4">
                <p className="text-xs text-slate-400 mb-1">{label}</p>
                <p className={`text-xl font-bold ${accent ? "text-indigo-400" : warn ? "text-orange-400" : "text-white"}`}>
                  {value}
                </p>
              </div>
            ))}
          </div>
        )}

        {/* Risk distribution */}
        {summary && (
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
            <h2 className="text-sm font-semibold text-slate-300 mb-4">Distribution du risque de progression</h2>
            <RiskDistributionBar counts={summary.risk_counts} total={summary.total} />
          </div>
        )}

        {/* Risk filter tabs */}
        <div className="flex gap-2 flex-wrap">
          {RISK_TABS.map(({ key, label }) => (
            <button
              key={key}
              onClick={() => setRiskFilter(key)}
              className={`px-4 py-2 rounded-lg text-sm font-medium border transition-colors ${
                riskFilter === key
                  ? "bg-indigo-600 border-indigo-500 text-white"
                  : "bg-slate-900 border-slate-700 text-slate-400 hover:text-white hover:border-slate-600"
              }`}
            >
              {label}
              {summary && key !== "all" && (
                <span className="ml-1.5 text-xs opacity-70">
                  ({summary.risk_counts[key] || 0})
                </span>
              )}
            </button>
          ))}
        </div>

        {/* Action filter tabs */}
        <div className="flex gap-2 flex-wrap">
          {ACTION_TABS.map(({ key, label }) => (
            <button
              key={key}
              onClick={() => setActionFilter(key)}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium border transition-colors ${
                actionFilter === key
                  ? "bg-violet-600/30 border-violet-500/50 text-violet-300"
                  : "bg-slate-900 border-slate-700 text-slate-400 hover:text-white hover:border-slate-600"
              }`}
            >
              {label}
              {summary && key !== "all" && (
                <span className="ml-1 opacity-70">({summary.action_counts[key] || 0})</span>
              )}
            </button>
          ))}
        </div>

        {/* Deals grid */}
        {loading ? (
          <div className="flex items-center justify-center py-24">
            <div className="w-8 h-8 border-2 border-indigo-500 border-t-transparent rounded-full animate-spin" />
          </div>
        ) : deals.length === 0 ? (
          <div className="text-center py-24 text-slate-500">Aucun deal ne correspond aux filtres sélectionnés.</div>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
            {deals.map((d) => (
              <DealCard key={d.deal_id} deal={d} onClick={() => setSelected(d)} />
            ))}
          </div>
        )}
      </div>

      {selected && <DealModal deal={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
