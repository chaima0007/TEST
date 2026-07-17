"use client";

import { useEffect, useState } from "react";

interface Deal {
  deal_id: string;
  account_name: string;
  segment: string;
  arr_eur: number;
  stage: string;
  risk_score: number;
  risk_level: string;
  deal_action: string;
  stall_reasons: string[];
  risk_factors: string[];
  positive_signals: string[];
  intervention_plan: string[];
  forecast_adjustment_pct: number;
}

interface Summary {
  total: number;
  risk_counts: Record<string, number>;
  action_counts: Record<string, number>;
  stage_counts: Record<string, number>;
  top_stall_reasons: Record<string, number>;
  avg_risk_score: number;
  critical_count: number;
  escalation_count: number;
  total_arr_at_risk_eur: number;
}

const RISK_COLOR: Record<string, string> = {
  low: "#10b981",
  moderate: "#f59e0b",
  high: "#ef4444",
  critical: "#7c3aed",
};

const RISK_BADGE: Record<string, string> = {
  low: "bg-emerald-900/60 text-emerald-300 border-emerald-700",
  moderate: "bg-amber-900/60 text-amber-300 border-amber-700",
  high: "bg-red-900/60 text-red-300 border-red-700",
  critical: "bg-violet-900/60 text-violet-300 border-violet-700",
};

const ACTION_BADGE: Record<string, string> = {
  monitor: "bg-slate-800 text-slate-400 border-slate-600",
  accelerate: "bg-sky-900/60 text-sky-300 border-sky-700",
  intervene: "bg-amber-900/60 text-amber-300 border-amber-700",
  escalate: "bg-red-900/60 text-red-300 border-red-700",
  abandon: "bg-slate-800 text-slate-500 border-slate-700",
};

const STALL_LABELS: Record<string, string> = {
  no_champion: "Pas de champion",
  single_threaded: "Mono-thread",
  budget_freeze: "Budget gelé",
  competitor_threat: "Menace concurrente",
  technical_blocker: "Bloqueur technique",
  executive_misalignment: "Misalignment exec",
  procurement_delay: "Délai procurement",
  scope_creep: "Scope creep",
};

function RiskRing({ score, risk }: { score: number; risk: string }) {
  const r = 40;
  const circ = 2 * Math.PI * r;
  const arc = (score / 100) * circ;
  const stroke = RISK_COLOR[risk] || "#64748b";
  return (
    <svg width="96" height="96" viewBox="0 0 96 96">
      <circle cx="48" cy="48" r={r} fill="none" stroke="#1e293b" strokeWidth="10" />
      <circle cx="48" cy="48" r={r} fill="none" stroke={stroke} strokeWidth="10"
        strokeDasharray={`${arc} ${circ - arc}`} strokeLinecap="round" transform="rotate(-90 48 48)" />
      <text x="48" y="53" textAnchor="middle" fill="#f1f5f9" fontSize="18" fontWeight="bold">
        {Math.round(score)}
      </text>
    </svg>
  );
}

function RiskBar({ counts, total }: { counts: Record<string, number>; total: number }) {
  if (!total) return null;
  const segs = [
    { key: "critical", label: "Critique", color: "bg-violet-600" },
    { key: "high", label: "Élevé", color: "bg-red-500" },
    { key: "moderate", label: "Modéré", color: "bg-amber-500" },
    { key: "low", label: "Faible", color: "bg-emerald-500" },
  ];
  return (
    <div className="mb-6">
      <div className="flex rounded-full overflow-hidden h-3 mb-2">
        {segs.map(({ key, color }) => {
          const pct = ((counts[key] || 0) / total) * 100;
          return pct > 0 ? <div key={key} className={`${color} h-3`} style={{ width: `${pct}%` }} /> : null;
        })}
      </div>
      <div className="flex gap-4 text-xs text-slate-400">
        {segs.map(({ key, label, color }) => (
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
  return n >= 1000000 ? `${(n / 1000000).toFixed(1)}M€` : n >= 1000 ? `${(n / 1000).toFixed(0)}k€` : `${n}€`;
}

function actionLabel(a: string) {
  return { monitor: "Surveiller", accelerate: "Accélérer", intervene: "Intervenir", escalate: "Escalader", abandon: "Abandonner" }[a] || a;
}

function stageLabel(s: string) {
  return { discovery: "Discovery", qualification: "Qualification", proposal: "Proposal", negotiation: "Négociation", closing: "Closing" }[s] || s;
}

function DealCard({ deal, onClick }: { deal: Deal; onClick: () => void }) {
  return (
    <div onClick={onClick}
      className="bg-slate-800/60 border border-slate-700 rounded-xl p-5 cursor-pointer hover:border-slate-500 hover:bg-slate-800 transition-all">
      <div className="flex items-start gap-4 mb-4">
        <RiskRing score={deal.risk_score} risk={deal.risk_level} />
        <div className="flex-1 min-w-0">
          <h3 className="font-semibold text-slate-100 text-base truncate">{deal.account_name}</h3>
          <p className="text-slate-400 text-sm">{deal.segment} · {stageLabel(deal.stage)}</p>
          <p className="text-slate-300 text-sm font-medium">{fmt(deal.arr_eur)}</p>
          <div className="flex flex-wrap gap-1 mt-2">
            <span className={`text-xs px-2 py-0.5 rounded-full border font-medium capitalize ${RISK_BADGE[deal.risk_level]}`}>
              {deal.risk_level}
            </span>
            <span className={`text-xs px-2 py-0.5 rounded-full border font-medium ${ACTION_BADGE[deal.deal_action]}`}>
              {actionLabel(deal.deal_action)}
            </span>
          </div>
        </div>
      </div>

      {deal.stall_reasons.length > 0 && (
        <div className="flex flex-wrap gap-1 mb-3">
          {deal.stall_reasons.slice(0, 3).map((s) => (
            <span key={s} className="text-xs px-2 py-0.5 bg-red-900/30 border border-red-800/50 text-red-400 rounded-full">
              {STALL_LABELS[s] || s}
            </span>
          ))}
          {deal.stall_reasons.length > 3 && (
            <span className="text-xs px-2 py-0.5 bg-slate-900/60 border border-slate-700 text-slate-500 rounded-full">
              +{deal.stall_reasons.length - 3}
            </span>
          )}
        </div>
      )}

      <div className="flex justify-between text-xs text-slate-500 mb-1">
        <span>Ajustement forecast</span>
        <span className={deal.forecast_adjustment_pct < -20 ? "text-red-400" : deal.forecast_adjustment_pct < 0 ? "text-amber-400" : "text-emerald-400"}>
          {deal.forecast_adjustment_pct > 0 ? "+" : ""}{deal.forecast_adjustment_pct}%
        </span>
      </div>

      <div className="flex justify-between text-xs text-slate-500 mb-1">
        <span>Score risque</span>
        <span>{Math.round(deal.risk_score)}/100</span>
      </div>
      <div className="h-1.5 bg-slate-700 rounded-full overflow-hidden">
        <div className="h-1.5 rounded-full" style={{ width: `${deal.risk_score}%`, backgroundColor: RISK_COLOR[deal.risk_level] || "#64748b" }} />
      </div>
    </div>
  );
}

function DealModal({ deal, onClose }: { deal: Deal; onClose: () => void }) {
  const [tab, setTab] = useState<"factors" | "signals" | "plan">("factors");

  useEffect(() => {
    const handler = (e: KeyboardEvent) => e.key === "Escape" && onClose();
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [onClose]);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm p-4" onClick={onClose}>
      <div className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-2xl max-h-[90vh] overflow-y-auto shadow-2xl"
        onClick={(e) => e.stopPropagation()}>
        <div className="p-6 border-b border-slate-800 flex items-start gap-4">
          <RiskRing score={deal.risk_score} risk={deal.risk_level} />
          <div className="flex-1">
            <h2 className="text-xl font-bold text-slate-100">{deal.account_name}</h2>
            <p className="text-slate-400 text-sm">{deal.segment} · {stageLabel(deal.stage)} · {fmt(deal.arr_eur)}</p>
            <div className="flex flex-wrap gap-2 mt-2">
              <span className={`text-xs px-2 py-0.5 rounded-full border font-medium capitalize ${RISK_BADGE[deal.risk_level]}`}>
                Risque {deal.risk_level}
              </span>
              <span className={`text-xs px-2 py-0.5 rounded-full border font-medium ${ACTION_BADGE[deal.deal_action]}`}>
                {actionLabel(deal.deal_action)}
              </span>
              <span className={`text-xs px-2 py-0.5 rounded-full border ${deal.forecast_adjustment_pct < -20 ? "bg-red-900/60 text-red-300 border-red-700" : "bg-amber-900/60 text-amber-300 border-amber-700"}`}>
                Forecast {deal.forecast_adjustment_pct}%
              </span>
            </div>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-slate-300 text-2xl leading-none">&times;</button>
        </div>

        {deal.stall_reasons.length > 0 && (
          <div className="px-6 pt-4">
            <div className="flex flex-wrap gap-2">
              {deal.stall_reasons.map((s) => (
                <span key={s} className="text-xs px-2 py-1 bg-red-900/30 border border-red-800/50 text-red-400 rounded-full">
                  {STALL_LABELS[s] || s}
                </span>
              ))}
            </div>
          </div>
        )}

        <div className="flex border-b border-slate-800 mt-4">
          {(["factors", "signals", "plan"] as const).map((t) => (
            <button key={t} onClick={() => setTab(t)}
              className={`flex-1 py-2 text-xs font-medium capitalize transition-colors ${tab === t ? "text-indigo-400 border-b-2 border-indigo-500" : "text-slate-500 hover:text-slate-300"}`}>
              {t === "factors" ? "Facteurs risque" : t === "signals" ? "Signaux positifs" : "Plan d'intervention"}
            </button>
          ))}
        </div>

        <div className="p-6 space-y-2">
          {tab === "factors" && (
            deal.risk_factors.length === 0
              ? <p className="text-slate-500 text-sm text-center">Aucun facteur de risque détecté</p>
              : deal.risk_factors.map((f, i) => (
                  <div key={i} className="text-sm text-slate-300 bg-red-900/20 border border-red-800/40 rounded-lg px-3 py-2">{f}</div>
                ))
          )}
          {tab === "signals" && (
            deal.positive_signals.length === 0
              ? <p className="text-slate-500 text-sm text-center">Aucun signal positif détecté</p>
              : deal.positive_signals.map((s, i) => (
                  <div key={i} className="text-sm text-slate-300 bg-emerald-900/20 border border-emerald-800/40 rounded-lg px-3 py-2">{s}</div>
                ))
          )}
          {tab === "plan" && (
            <ol className="space-y-2">
              {deal.intervention_plan.map((step, i) => (
                <li key={i} className="text-sm text-slate-300 bg-indigo-900/20 border border-indigo-800/40 rounded-lg px-3 py-2 flex gap-2">
                  <span className="text-indigo-400 font-bold shrink-0">{i + 1}.</span> {step}
                </li>
              ))}
            </ol>
          )}
        </div>
      </div>
    </div>
  );
}

const RISKS = ["all", "critical", "high", "moderate", "low"];
const ACTIONS = ["all", "escalate", "intervene", "accelerate", "monitor", "abandon"];

export default function DealRiskAnalyzerPage() {
  const [data, setData] = useState<{ deals: Deal[]; summary: Summary } | null>(null);
  const [loading, setLoading] = useState(true);
  const [selected, setSelected] = useState<Deal | null>(null);
  const [riskFilter, setRiskFilter] = useState("all");
  const [actionFilter, setActionFilter] = useState("all");

  useEffect(() => {
    async function load() {
      const params = new URLSearchParams();
      if (riskFilter !== "all") params.set("risk", riskFilter);
      if (actionFilter !== "all") params.set("action", actionFilter);
      const res = await fetch(`/api/deal-risk-analyzer?${params}`);
      setData(await res.json());
      setLoading(false);
    }
    load();
  }, [riskFilter, actionFilter]);

  if (loading) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-slate-400 animate-pulse">Chargement analyse deals...</div>
    </div>
  );

  const s = data!.summary;

  const kpis = [
    { label: "Score Risque Moy.", value: s.avg_risk_score.toFixed(1), sub: "/ 100" },
    { label: "Deals Critiques", value: s.critical_count, sub: "escalade requise" },
    { label: "Escalades", value: s.escalation_count, sub: "management alerté" },
    { label: "ARR à Risque", value: fmt(s.total_arr_at_risk_eur), sub: "high + critique" },
    { label: "Total Deals", value: s.total, sub: "analysés" },
    { label: "À Intervenir", value: s.action_counts["intervene"] || 0, sub: "intervention requise" },
  ];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-slate-100">Analyse Risque Deals</h1>
          <p className="text-slate-400 mt-1">Détection IA des deals en danger — stall reasons, interventions et ajustements forecast</p>
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
            <button key={v} onClick={() => setRiskFilter(v)}
              className={`text-xs px-3 py-1.5 rounded-full border transition-colors capitalize ${riskFilter === v ? "bg-indigo-600 border-indigo-500 text-white" : "bg-slate-800 border-slate-700 text-slate-400 hover:border-slate-500"}`}>
              {v === "all" ? "Tous les risques" : v}
              {v !== "all" && s.risk_counts[v] ? ` (${s.risk_counts[v]})` : ""}
            </button>
          ))}
        </div>

        <div className="flex flex-wrap gap-2 mb-8">
          {ACTIONS.map((v) => (
            <button key={v} onClick={() => setActionFilter(v)}
              className={`text-xs px-3 py-1.5 rounded-full border transition-colors ${actionFilter === v ? "bg-red-600 border-red-500 text-white" : "bg-slate-800 border-slate-700 text-slate-400 hover:border-slate-500"}`}>
              {v === "all" ? "Toutes actions" : actionLabel(v)}
              {v !== "all" && s.action_counts[v] ? ` (${s.action_counts[v]})` : ""}
            </button>
          ))}
        </div>

        {data!.deals.length === 0
          ? <div className="text-center text-slate-500 py-20">Aucun deal pour ces filtres</div>
          : (
            <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-5">
              {data!.deals.map((deal) => (
                <DealCard key={deal.deal_id} deal={deal} onClick={() => setSelected(deal)} />
              ))}
            </div>
          )}
      </div>

      {selected && <DealModal deal={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
