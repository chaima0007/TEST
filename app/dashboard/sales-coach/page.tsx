"use client";

import { useEffect, useState, useRef } from "react";

type CoachingPriority = "urgent" | "high" | "medium" | "low";
type CoachingFocus =
  | "prospecting"
  | "qualification"
  | "presentation"
  | "negotiation"
  | "closing"
  | "retention";

interface RepPerformance {
  rep_id: string;
  rep_name: string;
  manager_id: string;
  territory: string;
  open_deals: number;
  pipeline_value_eur: number;
  quota_eur: number;
  pipeline_coverage_ratio: number;
  calls_last_30d: number;
  emails_last_30d: number;
  meetings_last_30d: number;
  demos_last_30d: number;
  win_rate_last_90d: number;
  win_rate_prev_90d: number;
  avg_deal_size_eur: number;
  avg_sales_cycle_days: number;
  deals_won_last_90d: number;
  deals_lost_last_90d: number;
  deals_stalled_last_30d: number;
  discovery_score: number;
  objection_score: number;
  demo_score: number;
  pricing_score: number;
  follow_up_score: number;
  relationship_score: number;
  time_mgmt_score: number;
}

interface CoachingPlan {
  rep: RepPerformance;
  coaching_priority: CoachingPriority;
  primary_focus: CoachingFocus;
  coaching_score: number;
  pipeline_health_score: number;
  activity_score: number;
  skill_gap_score: number;
  win_rate_trend_score: number;
  top_recommendations: string[];
  skill_development: string[];
  kpis_to_watch: string[];
  estimated_quota_attainment_pct: number;
}

interface Summary {
  total_reps: number;
  priority_counts: Record<string, number>;
  focus_counts: Record<string, number>;
  avg_coaching_score: number;
  avg_quota_attainment_pct: number;
  urgent_count: number;
}

const PRIORITY_META: Record<CoachingPriority, { label: string; color: string; bg: string; dot: string }> = {
  urgent: { label: "URGENT", color: "text-red-400", bg: "bg-red-500/10 border-red-500/30", dot: "bg-red-400" },
  high: { label: "ÉLEVÉ", color: "text-orange-400", bg: "bg-orange-500/10 border-orange-500/30", dot: "bg-orange-400" },
  medium: { label: "MOYEN", color: "text-yellow-400", bg: "bg-yellow-500/10 border-yellow-500/30", dot: "bg-yellow-400" },
  low: { label: "FAIBLE", color: "text-emerald-400", bg: "bg-emerald-500/10 border-emerald-500/30", dot: "bg-emerald-400" },
};

const FOCUS_META: Record<CoachingFocus, { label: string; icon: string }> = {
  prospecting: { label: "Prospection", icon: "🎯" },
  qualification: { label: "Qualification", icon: "🔍" },
  presentation: { label: "Présentation", icon: "📊" },
  negotiation: { label: "Négociation", icon: "🤝" },
  closing: { label: "Closing", icon: "✍️" },
  retention: { label: "Rétention", icon: "🔒" },
};

const PRIORITY_TABS: { id: CoachingPriority | "all"; label: string }[] = [
  { id: "all", label: "Tous" },
  { id: "urgent", label: "Urgent" },
  { id: "high", label: "Élevé" },
  { id: "medium", label: "Moyen" },
  { id: "low", label: "Faible" },
];

function fmt(n: number, decimals = 0) {
  return n.toLocaleString("fr-FR", { maximumFractionDigits: decimals });
}

function fmtEur(n: number) {
  if (n >= 1_000_000) return `${(n / 1_000_000).toFixed(1)}M€`;
  if (n >= 1_000) return `${(n / 1_000).toFixed(0)}k€`;
  return `${n}€`;
}

function ScoreBar({ value, color = "bg-indigo-500" }: { value: number; color?: string }) {
  return (
    <div className="h-1.5 w-full rounded-full bg-slate-700">
      <div
        className={`h-1.5 rounded-full transition-all ${color}`}
        style={{ width: `${Math.min(100, value)}%` }}
      />
    </div>
  );
}

function AttainmentRing({ pct }: { pct: number }) {
  const clamped = Math.min(200, Math.max(0, pct));
  const display = Math.min(100, clamped);
  const r = 28;
  const circ = 2 * Math.PI * r;
  const offset = circ - (display / 100) * circ;
  const color = pct >= 80 ? "#10b981" : pct >= 50 ? "#f59e0b" : "#ef4444";
  return (
    <div className="relative flex items-center justify-center w-16 h-16">
      <svg viewBox="0 0 72 72" className="w-16 h-16 -rotate-90">
        <circle cx="36" cy="36" r={r} fill="none" stroke="#334155" strokeWidth="6" />
        <circle
          cx="36" cy="36" r={r} fill="none"
          stroke={color} strokeWidth="6"
          strokeDasharray={circ}
          strokeDashoffset={offset}
          strokeLinecap="round"
          className="transition-all duration-700"
        />
      </svg>
      <span className="absolute text-xs font-bold" style={{ color }}>{Math.round(pct)}%</span>
    </div>
  );
}

function CoachingModal({ plan, onClose }: { plan: CoachingPlan; onClose: () => void }) {
  const modalRef = useRef<HTMLDivElement>(null);
  const meta = PRIORITY_META[plan.coaching_priority];
  const focus = FOCUS_META[plan.primary_focus];

  useEffect(() => {
    const handler = (e: KeyboardEvent) => e.key === "Escape" && onClose();
    const clickOut = (e: MouseEvent) => {
      if (modalRef.current && !modalRef.current.contains(e.target as Node)) onClose();
    };
    window.addEventListener("keydown", handler);
    document.addEventListener("mousedown", clickOut);
    return () => {
      window.removeEventListener("keydown", handler);
      document.removeEventListener("mousedown", clickOut);
    };
  }, [onClose]);

  const skills = [
    { label: "Découverte", val: plan.rep.discovery_score },
    { label: "Objections", val: plan.rep.objection_score },
    { label: "Demo", val: plan.rep.demo_score },
    { label: "Pricing", val: plan.rep.pricing_score },
    { label: "Follow-up", val: plan.rep.follow_up_score },
    { label: "Relation", val: plan.rep.relationship_score },
    { label: "Temps", val: plan.rep.time_mgmt_score },
  ];

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4">
      <div ref={modalRef} className="relative w-full max-w-2xl max-h-[90vh] overflow-y-auto rounded-2xl bg-slate-900 border border-slate-700 shadow-2xl">
        <div className="sticky top-0 z-10 flex items-start justify-between gap-4 p-6 bg-slate-900 border-b border-slate-800">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <span className={`text-xs font-bold px-2 py-0.5 rounded-full border ${meta.bg} ${meta.color}`}>
                {meta.label}
              </span>
              <span className="text-xs text-slate-400">{focus.icon} {focus.label}</span>
            </div>
            <h2 className="text-xl font-bold text-slate-100">{plan.rep.rep_name}</h2>
            <p className="text-sm text-slate-400">{plan.rep.territory}</p>
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-slate-200 text-xl leading-none mt-1">✕</button>
        </div>

        <div className="p-6 space-y-6">
          {/* KPI strip */}
          <div className="grid grid-cols-2 gap-3 sm:grid-cols-4">
            {[
              { label: "Attainment", value: `${Math.round(plan.estimated_quota_attainment_pct)}%` },
              { label: "Win Rate 90j", value: `${plan.rep.win_rate_last_90d}%` },
              { label: "Pipeline", value: fmtEur(plan.rep.pipeline_value_eur) },
              { label: "Deals ouverts", value: plan.rep.open_deals },
            ].map((kpi) => (
              <div key={kpi.label} className="rounded-lg bg-slate-800 border border-slate-700 p-3 text-center">
                <div className="text-lg font-bold text-slate-100">{kpi.value}</div>
                <div className="text-xs text-slate-400">{kpi.label}</div>
              </div>
            ))}
          </div>

          {/* Dimension scores */}
          <div>
            <h3 className="text-sm font-semibold text-slate-300 mb-3">Dimensions coaching</h3>
            <div className="space-y-2">
              {[
                { label: "Santé pipeline", val: plan.pipeline_health_score, color: "bg-blue-500" },
                { label: "Activité", val: plan.activity_score, color: "bg-purple-500" },
                { label: "Taux de victoire", val: plan.win_rate_trend_score, color: "bg-emerald-500" },
                { label: "Compétences (inv. gaps)", val: 100 - plan.skill_gap_score, color: "bg-indigo-500" },
              ].map((d) => (
                <div key={d.label} className="flex items-center gap-3">
                  <span className="text-xs text-slate-400 w-36 shrink-0">{d.label}</span>
                  <div className="flex-1">
                    <ScoreBar value={d.val} color={d.color} />
                  </div>
                  <span className="text-xs text-slate-300 w-8 text-right">{Math.round(d.val)}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Skill radar */}
          <div>
            <h3 className="text-sm font-semibold text-slate-300 mb-3">Compétences individuelles</h3>
            <div className="space-y-2">
              {skills.map((s) => (
                <div key={s.label} className="flex items-center gap-3">
                  <span className="text-xs text-slate-400 w-20 shrink-0">{s.label}</span>
                  <div className="flex-1">
                    <ScoreBar
                      value={s.val}
                      color={s.val >= 70 ? "bg-emerald-500" : s.val >= 50 ? "bg-yellow-500" : "bg-red-500"}
                    />
                  </div>
                  <span className="text-xs text-slate-300 w-8 text-right">{Math.round(s.val)}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Recommendations */}
          {plan.top_recommendations.length > 0 && (
            <div>
              <h3 className="text-sm font-semibold text-slate-300 mb-3">Recommandations actions</h3>
              <ul className="space-y-2">
                {plan.top_recommendations.map((r, i) => (
                  <li key={i} className="flex items-start gap-2 text-sm text-slate-300">
                    <span className="text-indigo-400 mt-0.5 shrink-0">→</span>
                    {r}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Skill development */}
          {plan.skill_development.length > 0 && (
            <div>
              <h3 className="text-sm font-semibold text-slate-300 mb-3">Développement compétences</h3>
              <ul className="space-y-2">
                {plan.skill_development.map((s, i) => (
                  <li key={i} className="flex items-start gap-2 text-sm text-slate-300">
                    <span className="text-purple-400 mt-0.5 shrink-0">◆</span>
                    {s}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* KPIs */}
          <div>
            <h3 className="text-sm font-semibold text-slate-300 mb-3">KPIs à suivre</h3>
            <div className="flex flex-wrap gap-2">
              {plan.kpis_to_watch.map((k, i) => (
                <span key={i} className="text-xs bg-slate-800 border border-slate-700 text-slate-300 px-2 py-1 rounded-full">
                  {k}
                </span>
              ))}
            </div>
          </div>

          {/* Activity breakdown */}
          <div>
            <h3 className="text-sm font-semibold text-slate-300 mb-3">Activité 30 derniers jours</h3>
            <div className="grid grid-cols-2 gap-3 sm:grid-cols-4">
              {[
                { label: "Appels", val: plan.rep.calls_last_30d, bench: 60 },
                { label: "Emails", val: plan.rep.emails_last_30d, bench: 120 },
                { label: "RDV", val: plan.rep.meetings_last_30d, bench: 15 },
                { label: "Demos", val: plan.rep.demos_last_30d, bench: 8 },
              ].map((a) => (
                <div key={a.label} className="rounded-lg bg-slate-800 border border-slate-700 p-3 text-center">
                  <div className={`text-lg font-bold ${a.val >= a.bench ? "text-emerald-400" : "text-orange-400"}`}>{a.val}</div>
                  <div className="text-xs text-slate-400">{a.label}</div>
                  <div className="text-xs text-slate-500">/ {a.bench} cible</div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

function RepCard({ plan, onClick }: { plan: CoachingPlan; onClick: () => void }) {
  const meta = PRIORITY_META[plan.coaching_priority];
  const focus = FOCUS_META[plan.primary_focus];
  const winTrend = plan.rep.win_rate_last_90d - plan.rep.win_rate_prev_90d;

  return (
    <div
      onClick={onClick}
      className={`cursor-pointer rounded-xl border p-5 transition-all hover:border-slate-600 hover:bg-slate-800/80 ${meta.bg}`}
    >
      <div className="flex items-start justify-between gap-3 mb-4">
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 mb-1">
            <span className={`inline-flex items-center gap-1 text-xs font-semibold px-2 py-0.5 rounded-full border ${meta.bg} ${meta.color}`}>
              <span className={`w-1.5 h-1.5 rounded-full ${meta.dot}`} />
              {meta.label}
            </span>
          </div>
          <h3 className="font-semibold text-slate-100 truncate">{plan.rep.rep_name}</h3>
          <p className="text-xs text-slate-400 truncate">{plan.rep.territory}</p>
        </div>
        <AttainmentRing pct={plan.estimated_quota_attainment_pct} />
      </div>

      {/* Focus badge */}
      <div className="flex items-center gap-2 mb-4">
        <span className="text-xs bg-slate-800 border border-slate-700 text-slate-300 px-2 py-0.5 rounded-full">
          {focus.icon} Focus: {focus.label}
        </span>
        <span className={`text-xs font-medium ${winTrend >= 0 ? "text-emerald-400" : "text-red-400"}`}>
          {winTrend >= 0 ? "▲" : "▼"} {Math.abs(winTrend)}% win rate
        </span>
      </div>

      {/* Bars */}
      <div className="space-y-2 mb-4">
        <div className="flex items-center gap-2">
          <span className="text-xs text-slate-500 w-14 shrink-0">Pipeline</span>
          <div className="flex-1"><ScoreBar value={plan.pipeline_health_score} color="bg-blue-500" /></div>
          <span className="text-xs text-slate-400 w-6 text-right">{Math.round(plan.pipeline_health_score)}</span>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-xs text-slate-500 w-14 shrink-0">Activité</span>
          <div className="flex-1"><ScoreBar value={plan.activity_score} color="bg-purple-500" /></div>
          <span className="text-xs text-slate-400 w-6 text-right">{Math.round(plan.activity_score)}</span>
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-3 gap-2 text-center">
        <div>
          <div className="text-sm font-bold text-slate-200">{fmtEur(plan.rep.pipeline_value_eur)}</div>
          <div className="text-xs text-slate-500">Pipeline</div>
        </div>
        <div>
          <div className="text-sm font-bold text-slate-200">{plan.rep.win_rate_last_90d}%</div>
          <div className="text-xs text-slate-500">Win Rate</div>
        </div>
        <div>
          <div className="text-sm font-bold text-slate-200">{plan.rep.open_deals}</div>
          <div className="text-xs text-slate-500">Deals</div>
        </div>
      </div>
    </div>
  );
}

export default function SalesCoachPage() {
  const [reps, setReps] = useState<CoachingPlan[]>([]);
  const [summary, setSummary] = useState<Summary | null>(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<CoachingPriority | "all">("all");
  const [selected, setSelected] = useState<CoachingPlan | null>(null);

  useEffect(() => {
    fetch("/api/sales-coach")
      .then((r) => r.json())
      .then((data) => {
        setReps(data.reps ?? []);
        setSummary(data.summary ?? null);
      })
      .finally(() => setLoading(false));
  }, []);

  const filtered = activeTab === "all" ? reps : reps.filter((r) => r.coaching_priority === activeTab);

  return (
    <div className="min-h-screen bg-slate-950 p-6">
      <div className="max-w-7xl mx-auto space-y-6">

        {/* Header */}
        <div className="flex items-start justify-between gap-4">
          <div>
            <h1 className="text-2xl font-bold text-slate-100">Sales Coach IA</h1>
            <p className="text-sm text-slate-400 mt-1">
              Recommandations personnalisées pour chaque commercial — pipeline, activité, compétences
            </p>
          </div>
          {summary && summary.urgent_count > 0 && (
            <div className="flex items-center gap-2 bg-red-500/10 border border-red-500/30 rounded-xl px-4 py-2">
              <span className="w-2 h-2 bg-red-400 rounded-full animate-pulse" />
              <span className="text-sm font-semibold text-red-400">
                {summary.urgent_count} commercial{summary.urgent_count > 1 ? "x" : ""} en urgence
              </span>
            </div>
          )}
        </div>

        {/* KPI strip */}
        {summary && (
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
            {[
              { label: "Commerciaux suivis", value: summary.total_reps, color: "text-slate-100" },
              { label: "Score coaching moyen", value: `${summary.avg_coaching_score}/100`, color: "text-orange-400" },
              { label: "Attainment moyen", value: `${summary.avg_quota_attainment_pct}%`, color: summary.avg_quota_attainment_pct >= 80 ? "text-emerald-400" : "text-yellow-400" },
              { label: "Urgences", value: summary.urgent_count, color: "text-red-400" },
            ].map((kpi) => (
              <div key={kpi.label} className="rounded-xl bg-slate-900 border border-slate-800 p-4">
                <div className={`text-2xl font-bold ${kpi.color}`}>{kpi.value}</div>
                <div className="text-xs text-slate-400 mt-1">{kpi.label}</div>
              </div>
            ))}
          </div>
        )}

        {/* Focus distribution */}
        {summary && (
          <div className="rounded-xl bg-slate-900 border border-slate-800 p-4">
            <h2 className="text-sm font-semibold text-slate-400 mb-3">Répartition par focus coaching</h2>
            <div className="flex flex-wrap gap-2">
              {Object.entries(summary.focus_counts).map(([focus, count]) => {
                const f = FOCUS_META[focus as CoachingFocus];
                if (!f || count === 0) return null;
                return (
                  <span key={focus} className="text-xs bg-slate-800 border border-slate-700 text-slate-300 px-3 py-1.5 rounded-full">
                    {f.icon} {f.label}: <span className="font-bold text-slate-100">{count}</span>
                  </span>
                );
              })}
            </div>
          </div>
        )}

        {/* Priority tabs */}
        <div className="flex gap-1 bg-slate-900 border border-slate-800 rounded-xl p-1 w-fit">
          {PRIORITY_TABS.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-all ${
                activeTab === tab.id
                  ? "bg-indigo-600 text-white"
                  : "text-slate-400 hover:text-slate-200"
              }`}
            >
              {tab.label}
              {summary && tab.id !== "all" && (
                <span className="ml-1.5 text-xs opacity-70">
                  ({summary.priority_counts[tab.id] ?? 0})
                </span>
              )}
            </button>
          ))}
        </div>

        {/* Rep grid */}
        {loading ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {Array.from({ length: 8 }).map((_, i) => (
              <div key={i} className="rounded-xl bg-slate-900 border border-slate-800 p-5 animate-pulse h-52" />
            ))}
          </div>
        ) : filtered.length === 0 ? (
          <div className="text-center text-slate-500 py-16">Aucun commercial dans cette catégorie</div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {filtered.map((plan) => (
              <RepCard key={plan.rep.rep_id} plan={plan} onClick={() => setSelected(plan)} />
            ))}
          </div>
        )}
      </div>

      {selected && <CoachingModal plan={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
