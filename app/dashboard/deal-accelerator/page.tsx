"use client";

import { useEffect, useState, useRef } from "react";

type DealHealth = "active" | "at_risk" | "stalled" | "critical" | "lost";
type AccelerationStrategy =
  | "executive_sponsor" | "requalify" | "competitive_play" | "value_proof"
  | "urgency_create" | "champion_build" | "budget_reshape" | "direct_close";
type SalesStage = "prospecting" | "discovery" | "demo" | "proposal" | "negotiation" | "closing";

interface DealContext {
  deal_id: string;
  deal_name: string;
  company: string;
  contact_name: string;
  stage: SalesStage;
  deal_value_eur: number;
  days_in_stage: number;
  days_since_last_activity: number;
  close_date_in_days: number;
  contacts_count: number;
  decision_maker_identified: boolean;
  champion_identified: boolean;
  executive_sponsor: boolean;
  last_email_response_days: number;
  meetings_last_30d: number;
  prospect_initiated_last_30d: number;
  has_competitor: boolean;
  competitor_name: string | null;
  competitor_strength: number;
  budget_confirmed: boolean;
  price_objection: boolean;
  technical_hold: boolean;
  rep_notes_concern: boolean;
  next_step_defined: boolean;
}

interface AccelerationPlan {
  deal: DealContext;
  deal_health: DealHealth;
  stall_score: number;
  inactivity_risk: number;
  stakeholder_gap: number;
  competitive_risk: number;
  budget_risk: number;
  primary_strategy: AccelerationStrategy;
  secondary_strategies: AccelerationStrategy[];
  active_blockers: string[];
  action_plan: string[];
  days_to_act: number;
  win_probability_adj: number;
  deal_momentum: number;
}

interface Summary {
  total: number;
  health_counts: Record<string, number>;
  strategy_counts: Record<string, number>;
  avg_stall_score: number;
  avg_win_probability: number;
  pipeline_at_risk_eur: number;
  critical_count: number;
}

const HEALTH_META: Record<DealHealth, { label: string; color: string; bg: string; dot: string }> = {
  active: { label: "ACTIF", color: "text-emerald-400", bg: "bg-emerald-500/10 border-emerald-500/30", dot: "bg-emerald-400" },
  at_risk: { label: "À RISQUE", color: "text-yellow-400", bg: "bg-yellow-500/10 border-yellow-500/30", dot: "bg-yellow-400" },
  stalled: { label: "BLOQUÉ", color: "text-orange-400", bg: "bg-orange-500/10 border-orange-500/30", dot: "bg-orange-400" },
  critical: { label: "CRITIQUE", color: "text-red-400", bg: "bg-red-500/10 border-red-500/30", dot: "bg-red-400" },
  lost: { label: "PERDU", color: "text-slate-400", bg: "bg-slate-500/10 border-slate-500/30", dot: "bg-slate-400" },
};

const STRATEGY_META: Record<AccelerationStrategy, { label: string; icon: string }> = {
  executive_sponsor: { label: "Executive Sponsor", icon: "👔" },
  requalify: { label: "Requalifier", icon: "🔍" },
  competitive_play: { label: "Différenciation Concurrentielle", icon: "⚔️" },
  value_proof: { label: "Preuve de Valeur", icon: "📊" },
  urgency_create: { label: "Créer l'Urgence", icon: "⏰" },
  champion_build: { label: "Construire un Champion", icon: "🏆" },
  budget_reshape: { label: "Rework Financier", icon: "💰" },
  direct_close: { label: "Closing Direct", icon: "✍️" },
};

const STAGE_LABELS: Record<SalesStage, string> = {
  prospecting: "Prospection",
  discovery: "Découverte",
  demo: "Démo",
  proposal: "Proposition",
  negotiation: "Négociation",
  closing: "Closing",
};

const HEALTH_TABS: { id: DealHealth | "all"; label: string }[] = [
  { id: "all", label: "Tous" },
  { id: "critical", label: "Critique" },
  { id: "stalled", label: "Bloqué" },
  { id: "at_risk", label: "À risque" },
  { id: "active", label: "Actif" },
];

function fmtEur(n: number) {
  if (n >= 1_000_000) return `${(n / 1_000_000).toFixed(1)}M€`;
  if (n >= 1_000) return `${(n / 1_000).toFixed(0)}k€`;
  return `${n}€`;
}

function ScoreBar({ value, color = "bg-indigo-500", invert = false }: { value: number; color?: string; invert?: boolean }) {
  const display = invert ? 100 - value : value;
  return (
    <div className="h-1.5 w-full rounded-full bg-slate-700">
      <div className={`h-1.5 rounded-full transition-all ${color}`} style={{ width: `${Math.min(100, Math.max(0, display))}%` }} />
    </div>
  );
}

function MomentumRing({ momentum, win }: { momentum: number; win: number }) {
  const r = 26;
  const circ = 2 * Math.PI * r;
  const offset = circ - (Math.min(100, momentum) / 100) * circ;
  const color = momentum >= 70 ? "#10b981" : momentum >= 40 ? "#f59e0b" : "#ef4444";
  return (
    <div className="relative flex flex-col items-center">
      <div className="relative flex items-center justify-center w-14 h-14">
        <svg viewBox="0 0 68 68" className="w-14 h-14 -rotate-90">
          <circle cx="34" cy="34" r={r} fill="none" stroke="#334155" strokeWidth="5" />
          <circle cx="34" cy="34" r={r} fill="none" stroke={color} strokeWidth="5"
            strokeDasharray={circ} strokeDashoffset={offset} strokeLinecap="round" />
        </svg>
        <span className="absolute text-xs font-bold" style={{ color }}>{Math.round(momentum)}</span>
      </div>
      <span className="text-xs text-slate-400 mt-0.5">Win {Math.round(win)}%</span>
    </div>
  );
}

function DealModal({ plan, onClose }: { plan: AccelerationPlan; onClose: () => void }) {
  const modalRef = useRef<HTMLDivElement>(null);
  const meta = HEALTH_META[plan.deal_health];
  const strategy = STRATEGY_META[plan.primary_strategy];

  useEffect(() => {
    const handler = (e: KeyboardEvent) => e.key === "Escape" && onClose();
    const click = (e: MouseEvent) => {
      if (modalRef.current && !modalRef.current.contains(e.target as Node)) onClose();
    };
    window.addEventListener("keydown", handler);
    document.addEventListener("mousedown", click);
    return () => { window.removeEventListener("keydown", handler); document.removeEventListener("mousedown", click); };
  }, [onClose]);

  const overdue = plan.deal.close_date_in_days < 0;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4">
      <div ref={modalRef} className="relative w-full max-w-2xl max-h-[90vh] overflow-y-auto rounded-2xl bg-slate-900 border border-slate-700 shadow-2xl">
        <div className="sticky top-0 z-10 flex items-start justify-between gap-4 p-6 bg-slate-900 border-b border-slate-800">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <span className={`text-xs font-bold px-2 py-0.5 rounded-full border ${meta.bg} ${meta.color} flex items-center gap-1`}>
                <span className={`w-1.5 h-1.5 rounded-full ${meta.dot} ${plan.deal_health === "critical" ? "animate-pulse" : ""}`} />
                {meta.label}
              </span>
              <span className="text-xs text-slate-400">{STAGE_LABELS[plan.deal.stage]}</span>
              {overdue && (
                <span className="text-xs bg-red-500/20 border border-red-500/40 text-red-400 px-2 py-0.5 rounded-full">
                  OVERDUE {Math.abs(plan.deal.close_date_in_days)}j
                </span>
              )}
            </div>
            <h2 className="text-xl font-bold text-slate-100">{plan.deal.deal_name}</h2>
            <p className="text-sm text-slate-400">{plan.deal.contact_name} · {plan.deal.company}</p>
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-slate-200 text-xl leading-none mt-1">✕</button>
        </div>

        <div className="p-6 space-y-6">
          {/* Deal KPIs */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
            {[
              { label: "Valeur deal", value: fmtEur(plan.deal.deal_value_eur), color: "text-slate-100" },
              { label: "Win prob.", value: `${Math.round(plan.win_probability_adj)}%`, color: plan.win_probability_adj >= 50 ? "text-emerald-400" : "text-red-400" },
              { label: "Momentum", value: `${Math.round(plan.deal_momentum)}/100`, color: plan.deal_momentum >= 60 ? "text-emerald-400" : "text-orange-400" },
              { label: "Agir dans", value: plan.days_to_act === 0 ? "Maintenant" : `${plan.days_to_act}j`, color: plan.days_to_act === 0 ? "text-red-400" : "text-yellow-400" },
            ].map((kpi) => (
              <div key={kpi.label} className="rounded-lg bg-slate-800 border border-slate-700 p-3 text-center">
                <div className={`text-lg font-bold ${kpi.color}`}>{kpi.value}</div>
                <div className="text-xs text-slate-400">{kpi.label}</div>
              </div>
            ))}
          </div>

          {/* Risk dimensions */}
          <div>
            <h3 className="text-sm font-semibold text-slate-300 mb-3">Dimensions de risque</h3>
            <div className="space-y-2">
              {[
                { label: "Inactivité", val: plan.inactivity_risk, color: "bg-red-500" },
                { label: "Stakeholders", val: plan.stakeholder_gap, color: "bg-orange-500" },
                { label: "Concurrentiel", val: plan.competitive_risk, color: "bg-yellow-500" },
                { label: "Budget", val: plan.budget_risk, color: "bg-purple-500" },
              ].map((d) => (
                <div key={d.label} className="flex items-center gap-3">
                  <span className="text-xs text-slate-400 w-24 shrink-0">{d.label}</span>
                  <div className="flex-1"><ScoreBar value={d.val} color={d.color} /></div>
                  <span className="text-xs text-slate-300 w-8 text-right">{Math.round(d.val)}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Primary strategy */}
          <div>
            <h3 className="text-sm font-semibold text-slate-300 mb-2">Stratégie principale</h3>
            <div className="bg-indigo-500/10 border border-indigo-500/30 rounded-lg p-4">
              <div className="flex items-center gap-2 mb-1">
                <span className="text-lg">{strategy.icon}</span>
                <span className="text-sm font-semibold text-indigo-300">{strategy.label}</span>
              </div>
              {plan.secondary_strategies.length > 0 && (
                <div className="flex flex-wrap gap-1 mt-2">
                  {plan.secondary_strategies.map((s) => (
                    <span key={s} className="text-xs bg-slate-800 border border-slate-700 text-slate-300 px-2 py-0.5 rounded-full">
                      {STRATEGY_META[s]?.icon} {STRATEGY_META[s]?.label}
                    </span>
                  ))}
                </div>
              )}
            </div>
          </div>

          {/* Action plan */}
          <div>
            <h3 className="text-sm font-semibold text-slate-300 mb-3">Plan d'action</h3>
            <ol className="space-y-2">
              {plan.action_plan.map((a, i) => (
                <li key={i} className="flex items-start gap-3 text-sm text-slate-300">
                  <span className="w-5 h-5 rounded-full bg-indigo-600 text-white text-xs flex items-center justify-center shrink-0 mt-0.5">{i + 1}</span>
                  {a}
                </li>
              ))}
            </ol>
          </div>

          {/* Blockers */}
          {plan.active_blockers.length > 0 && (
            <div>
              <h3 className="text-sm font-semibold text-slate-300 mb-3">Blocages identifiés ({plan.active_blockers.length})</h3>
              <ul className="space-y-1.5">
                {plan.active_blockers.map((b, i) => (
                  <li key={i} className="flex items-start gap-2 text-sm text-slate-400">
                    <span className="text-red-400 mt-0.5 shrink-0">⚠</span>{b}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Deal data */}
          <div>
            <h3 className="text-sm font-semibold text-slate-300 mb-3">Données du deal</h3>
            <div className="grid grid-cols-2 sm:grid-cols-3 gap-2 text-center">
              {[
                { label: "Jours en étape", val: plan.deal.days_in_stage },
                { label: "Inactivité", val: `${plan.deal.days_since_last_activity}j` },
                { label: "Contacts", val: plan.deal.contacts_count },
                { label: "RDV 30j", val: plan.deal.meetings_last_30d },
                { label: "Initié par prospect", val: plan.deal.prospect_initiated_last_30d },
                { label: plan.deal.close_date_in_days < 0 ? "Retard" : "Clôture dans", val: `${Math.abs(plan.deal.close_date_in_days)}j` },
              ].map((d) => (
                <div key={d.label} className="rounded-lg bg-slate-800 border border-slate-700 p-2">
                  <div className="text-sm font-bold text-slate-100">{d.val}</div>
                  <div className="text-xs text-slate-400">{d.label}</div>
                </div>
              ))}
            </div>
          </div>

          {/* Status flags */}
          <div>
            <h3 className="text-sm font-semibold text-slate-300 mb-3">État des éléments clés</h3>
            <div className="flex flex-wrap gap-2">
              {[
                { label: "Décideur identifié", ok: plan.deal.decision_maker_identified },
                { label: "Champion identifié", ok: plan.deal.champion_identified },
                { label: "Sponsor exécutif", ok: plan.deal.executive_sponsor },
                { label: "Budget confirmé", ok: plan.deal.budget_confirmed },
                { label: "Prochaine étape", ok: plan.deal.next_step_defined },
                { label: "Pas de concurrent", ok: !plan.deal.has_competitor },
                { label: "Pas d'objection prix", ok: !plan.deal.price_objection },
                { label: "Pas de blocage tech.", ok: !plan.deal.technical_hold },
              ].map((f) => (
                <span key={f.label} className={`text-xs px-3 py-1 rounded-full border ${f.ok ? "bg-emerald-500/10 border-emerald-500/30 text-emerald-300" : "bg-red-500/10 border-red-500/30 text-red-300"}`}>
                  {f.ok ? "✓" : "✗"} {f.label}
                </span>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

function DealCard({ plan, onClick }: { plan: AccelerationPlan; onClick: () => void }) {
  const meta = HEALTH_META[plan.deal_health];
  const strategy = STRATEGY_META[plan.primary_strategy];
  const isCritical = plan.deal_health === "critical";
  const overdue = plan.deal.close_date_in_days < 0;

  return (
    <div
      onClick={onClick}
      className={`cursor-pointer rounded-xl border p-5 transition-all hover:border-slate-600 hover:bg-slate-800/80 ${meta.bg}`}
    >
      <div className="flex items-start justify-between gap-3 mb-4">
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 mb-1 flex-wrap">
            <span className={`text-xs font-bold px-2 py-0.5 rounded-full border ${meta.bg} ${meta.color} flex items-center gap-1`}>
              <span className={`w-1.5 h-1.5 rounded-full ${meta.dot} ${isCritical ? "animate-pulse" : ""}`} />
              {meta.label}
            </span>
            {overdue && <span className="text-xs text-red-400 font-bold">OVERDUE</span>}
          </div>
          <h3 className="font-semibold text-slate-100 text-sm leading-tight truncate">{plan.deal.deal_name}</h3>
          <p className="text-xs text-slate-400 truncate">{plan.deal.company}</p>
        </div>
        <MomentumRing momentum={plan.deal_momentum} win={plan.win_probability_adj} />
      </div>

      {/* Strategy badge */}
      <div className="flex items-center gap-2 mb-3">
        <span className="text-xs bg-indigo-500/10 border border-indigo-500/30 text-indigo-300 px-2 py-0.5 rounded-full truncate max-w-full">
          {strategy.icon} {strategy.label}
        </span>
      </div>

      {/* Risk bars */}
      <div className="space-y-1.5 mb-4">
        <div className="flex items-center gap-2">
          <span className="text-xs text-slate-500 w-16 shrink-0">Inactivité</span>
          <div className="flex-1"><ScoreBar value={plan.inactivity_risk} color="bg-red-500" /></div>
          <span className="text-xs text-slate-400 w-6 text-right">{Math.round(plan.inactivity_risk)}</span>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-xs text-slate-500 w-16 shrink-0">Stakeholder</span>
          <div className="flex-1"><ScoreBar value={plan.stakeholder_gap} color="bg-orange-500" /></div>
          <span className="text-xs text-slate-400 w-6 text-right">{Math.round(plan.stakeholder_gap)}</span>
        </div>
      </div>

      {/* Bottom stats */}
      <div className="grid grid-cols-3 gap-2 text-center border-t border-slate-700 pt-3">
        <div>
          <div className="text-sm font-bold text-slate-200">{fmtEur(plan.deal.deal_value_eur)}</div>
          <div className="text-xs text-slate-500">Valeur</div>
        </div>
        <div>
          <div className={`text-sm font-bold ${plan.days_to_act === 0 ? "text-red-400" : "text-yellow-400"}`}>
            {plan.days_to_act === 0 ? "Maintenant" : `${plan.days_to_act}j`}
          </div>
          <div className="text-xs text-slate-500">Agir</div>
        </div>
        <div>
          <div className="text-sm font-bold text-slate-200">{plan.active_blockers.length}</div>
          <div className="text-xs text-slate-500">Blocages</div>
        </div>
      </div>
    </div>
  );
}

export default function DealAcceleratorPage() {
  const [deals, setDeals] = useState<AccelerationPlan[]>([]);
  const [summary, setSummary] = useState<Summary | null>(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<DealHealth | "all">("all");
  const [selected, setSelected] = useState<AccelerationPlan | null>(null);

  useEffect(() => {
    fetch("/api/deal-accelerator")
      .then((r) => r.json())
      .then((data) => {
        setDeals(data.deals ?? []);
        setSummary(data.summary ?? null);
      })
      .finally(() => setLoading(false));
  }, []);

  const filtered = activeTab === "all" ? deals : deals.filter((d) => d.deal_health === activeTab);

  return (
    <div className="min-h-screen bg-slate-950 p-6">
      <div className="max-w-7xl mx-auto space-y-6">

        {/* Header */}
        <div className="flex items-start justify-between gap-4">
          <div>
            <h1 className="text-2xl font-bold text-slate-100">Deal Accelerator IA</h1>
            <p className="text-sm text-slate-400 mt-1">
              Diagnostic des deals bloqués — stratégies de déblocage, plan d'action, probabilité de victoire ajustée
            </p>
          </div>
          {summary && summary.critical_count > 0 && (
            <div className="flex items-center gap-2 bg-red-500/10 border border-red-500/30 rounded-xl px-4 py-2">
              <span className="w-2 h-2 bg-red-400 rounded-full animate-pulse" />
              <span className="text-sm font-semibold text-red-400">
                {summary.critical_count} deal{summary.critical_count > 1 ? "s" : ""} critique{summary.critical_count > 1 ? "s" : ""}
              </span>
            </div>
          )}
        </div>

        {/* KPI strip */}
        {summary && (
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
            {[
              { label: "Deals analysés", value: summary.total, color: "text-slate-100" },
              { label: "Pipeline à risque", value: fmtEur(summary.pipeline_at_risk_eur), color: "text-red-400" },
              { label: "Win prob. moyen", value: `${Math.round(summary.avg_win_probability)}%`, color: summary.avg_win_probability >= 50 ? "text-emerald-400" : "text-orange-400" },
              { label: "Score stall moyen", value: `${summary.avg_stall_score}/100`, color: "text-orange-400" },
            ].map((kpi) => (
              <div key={kpi.label} className="rounded-xl bg-slate-900 border border-slate-800 p-4">
                <div className={`text-2xl font-bold ${kpi.color}`}>{kpi.value}</div>
                <div className="text-xs text-slate-400 mt-1">{kpi.label}</div>
              </div>
            ))}
          </div>
        )}

        {/* Strategy distribution */}
        {summary && (
          <div className="rounded-xl bg-slate-900 border border-slate-800 p-4">
            <h2 className="text-sm font-semibold text-slate-400 mb-3">Stratégies de déblocage</h2>
            <div className="flex flex-wrap gap-2">
              {Object.entries(summary.strategy_counts).map(([s, count]) => {
                const meta = STRATEGY_META[s as AccelerationStrategy];
                if (!meta || count === 0) return null;
                return (
                  <span key={s} className="text-xs bg-slate-800 border border-slate-700 text-slate-300 px-3 py-1.5 rounded-full">
                    {meta.icon} {meta.label}: <span className="font-bold text-slate-100">{count}</span>
                  </span>
                );
              })}
            </div>
          </div>
        )}

        {/* Health tabs */}
        <div className="flex gap-1 bg-slate-900 border border-slate-800 rounded-xl p-1 w-fit flex-wrap">
          {HEALTH_TABS.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-all ${
                activeTab === tab.id ? "bg-indigo-600 text-white" : "text-slate-400 hover:text-slate-200"
              }`}
            >
              {tab.label}
              {summary && tab.id !== "all" && (
                <span className="ml-1.5 text-xs opacity-70">({summary.health_counts[tab.id] ?? 0})</span>
              )}
            </button>
          ))}
        </div>

        {/* Deal grid */}
        {loading ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {Array.from({ length: 8 }).map((_, i) => (
              <div key={i} className="rounded-xl bg-slate-900 border border-slate-800 p-5 animate-pulse h-52" />
            ))}
          </div>
        ) : filtered.length === 0 ? (
          <div className="text-center text-slate-500 py-16">Aucun deal dans cette catégorie</div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {filtered.map((plan) => (
              <DealCard key={plan.deal.deal_id} plan={plan} onClick={() => setSelected(plan)} />
            ))}
          </div>
        )}
      </div>

      {selected && <DealModal plan={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
