"use client";

import { useState, useEffect, useRef } from "react";

// ─── Types ───────────────────────────────────────────────────────────────────

type VelocityStatus = "fast" | "on_pace" | "slow" | "stalled";
type VelocityAction = "close_now" | "rescue" | "accelerate" | "monitor";

interface Deal {
  deal_id: string;
  deal_name: string;
  account_name: string;
  segment: string;
  arr_eur: number;
  stage: string;
  velocity_status: VelocityStatus;
  velocity_action: VelocityAction;
  velocity_score: number;
  stage_pace_score: number;
  activity_score: number;
  probability_score: number;
  velocity_eur_per_day: number;
  schedule_delta_pct: number;
  days_in_current_stage: number;
  stage_benchmark_days: number;
  stage_overdue: boolean;
  win_probability_pct: number;
  last_activity_days: number;
  has_next_step_scheduled: boolean;
  champion_present: boolean;
  decision_maker_engaged: boolean;
  risk_flags: string[];
  momentum_signals: string[];
  recommended_actions: string[];
}

interface Summary {
  total: number;
  status_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_velocity_score: number;
  total_velocity_eur_per_day: number;
  total_pipeline_eur: number;
  total_weighted_pipeline_eur: number;
  stalled_count: number;
  rescue_count: number;
  close_now_count: number;
}

// ─── Helpers ─────────────────────────────────────────────────────────────────

const STATUS_META: Record<VelocityStatus, { label: string; color: string; bg: string; ring: string }> = {
  fast:     { label: "Rapide",   color: "text-emerald-400", bg: "bg-emerald-400", ring: "#34d399" },
  on_pace:  { label: "En rythme", color: "text-blue-400",   bg: "bg-blue-400",   ring: "#60a5fa" },
  slow:     { label: "Lent",     color: "text-amber-400",   bg: "bg-amber-400",   ring: "#fbbf24" },
  stalled:  { label: "Bloqué",   color: "text-red-400",     bg: "bg-red-400",     ring: "#f87171" },
};

const ACTION_META: Record<VelocityAction, { label: string; color: string; bg: string }> = {
  close_now:   { label: "Closer maintenant", color: "text-emerald-300", bg: "bg-emerald-900/40" },
  rescue:      { label: "Sauvetage urgent",  color: "text-red-300",     bg: "bg-red-900/40" },
  accelerate:  { label: "Accélérer",         color: "text-amber-300",   bg: "bg-amber-900/40" },
  monitor:     { label: "Surveiller",        color: "text-slate-300",   bg: "bg-slate-800/40" },
};

const STAGE_LABELS: Record<string, string> = {
  prospecting: "Prospection",
  qualification: "Qualification",
  demo: "Démo",
  proposal: "Proposition",
  negotiation: "Négociation",
  closing: "Closing",
};

const SEGMENT_LABELS: Record<string, string> = {
  enterprise: "Enterprise",
  mid_market: "Mid-Market",
  smb: "SMB",
};

function fmt(n: number) {
  if (n >= 1_000_000) return `${(n / 1_000_000).toFixed(1)}M`;
  if (n >= 1_000) return `${(n / 1_000).toFixed(0)}k`;
  return `${n.toFixed(0)}`;
}

function fmtEur(n: number) {
  return `€${fmt(n)}`;
}

function fmtScore(n: number) {
  return n.toFixed(1);
}

// ─── VelocityRing SVG ────────────────────────────────────────────────────────

function VelocityRing({ score, status }: { score: number; status: VelocityStatus }) {
  const r = 28;
  const circ = 2 * Math.PI * r;
  const arc = (score / 100) * circ;
  const color = STATUS_META[status].ring;
  return (
    <svg width="72" height="72" viewBox="0 0 72 72" className="flex-shrink-0">
      <circle cx="36" cy="36" r={r} fill="none" stroke="#1e293b" strokeWidth="7" />
      <circle
        cx="36" cy="36" r={r}
        fill="none"
        stroke={color}
        strokeWidth="7"
        strokeDasharray={`${arc} ${circ - arc}`}
        strokeLinecap="round"
        transform="rotate(-90 36 36)"
      />
      <text x="36" y="38" textAnchor="middle" dominantBaseline="middle" fill="white" fontSize="12" fontWeight="700">
        {fmtScore(score)}
      </text>
    </svg>
  );
}

// ─── MiniBar ─────────────────────────────────────────────────────────────────

function MiniBar({ value, label, color }: { value: number; label: string; color: string }) {
  return (
    <div className="space-y-0.5">
      <div className="flex justify-between text-[10px] text-slate-400">
        <span>{label}</span>
        <span>{value.toFixed(0)}</span>
      </div>
      <div className="h-1 bg-slate-800 rounded-full overflow-hidden">
        <div className={`h-full rounded-full ${color}`} style={{ width: `${Math.min(100, value)}%` }} />
      </div>
    </div>
  );
}

// ─── ScoreBar ────────────────────────────────────────────────────────────────

function ScoreBar({ value, label, weight, color }: { value: number; label: string; weight: string; color: string }) {
  return (
    <div className="space-y-1">
      <div className="flex items-center justify-between text-xs">
        <span className="text-slate-300">{label}</span>
        <div className="flex items-center gap-2">
          <span className="text-slate-500 text-[10px]">{weight}</span>
          <span className={`font-semibold ${color}`}>{value.toFixed(1)}</span>
        </div>
      </div>
      <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
        <div className={`h-full rounded-full ${color.replace("text-", "bg-")}`} style={{ width: `${Math.min(100, value)}%` }} />
      </div>
    </div>
  );
}

// ─── DealModal ───────────────────────────────────────────────────────────────

function DealModal({ deal, onClose }: { deal: Deal; onClose: () => void }) {
  const ref = useRef<HTMLDivElement>(null);
  const status = STATUS_META[deal.velocity_status];
  const action = ACTION_META[deal.velocity_action];

  useEffect(() => {
    const handler = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    document.addEventListener("keydown", handler);
    return () => document.removeEventListener("keydown", handler);
  }, [onClose]);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm" onClick={(e) => { if (ref.current && !ref.current.contains(e.target as Node)) onClose(); }}>
      <div ref={ref} className="w-full max-w-2xl bg-slate-900 border border-slate-700 rounded-2xl shadow-2xl max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="flex items-start justify-between p-6 border-b border-slate-800">
          <div className="space-y-1">
            <h2 className="text-white font-bold text-lg">{deal.deal_name}</h2>
            <p className="text-slate-400 text-sm">{deal.account_name} · {SEGMENT_LABELS[deal.segment] ?? deal.segment}</p>
            <div className="flex items-center gap-2 mt-2">
              <span className={`inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs font-semibold ${status.color} bg-slate-800`}>
                <span className={`w-1.5 h-1.5 rounded-full ${status.bg}`} />
                {status.label}
              </span>
              <span className={`inline-flex items-center px-2 py-0.5 rounded-full text-xs font-semibold ${action.color} ${action.bg}`}>
                {action.label}
              </span>
              <span className="text-slate-500 text-xs">{STAGE_LABELS[deal.stage] ?? deal.stage}</span>
            </div>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white transition-colors p-1 rounded ml-4">✕</button>
        </div>

        <div className="p-6 space-y-6">
          {/* KPI row */}
          <div className="grid grid-cols-3 gap-3">
            <div className="bg-slate-800/60 rounded-xl p-3 text-center">
              <p className="text-slate-400 text-xs mb-1">ARR</p>
              <p className="text-white font-bold text-lg">{fmtEur(deal.arr_eur)}</p>
            </div>
            <div className="bg-slate-800/60 rounded-xl p-3 text-center">
              <p className="text-slate-400 text-xs mb-1">Vélocité EUR/j</p>
              <p className="text-white font-bold text-lg">{fmtEur(deal.velocity_eur_per_day)}</p>
            </div>
            <div className="bg-slate-800/60 rounded-xl p-3 text-center">
              <p className="text-slate-400 text-xs mb-1">Prob. de gain</p>
              <p className="text-white font-bold text-lg">{deal.win_probability_pct}%</p>
            </div>
          </div>

          {/* Stage timing */}
          <div className="bg-slate-800/40 rounded-xl p-4">
            <div className="flex items-center justify-between mb-2">
              <span className="text-slate-300 text-sm font-medium">Stage : {STAGE_LABELS[deal.stage] ?? deal.stage}</span>
              {deal.stage_overdue ? (
                <span className="text-red-400 text-xs font-semibold">⚠ Dépassé</span>
              ) : (
                <span className="text-emerald-400 text-xs font-semibold">✓ Dans les délais</span>
              )}
            </div>
            <div className="h-2 bg-slate-700 rounded-full overflow-hidden mb-1">
              <div
                className={`h-full rounded-full transition-all ${deal.stage_overdue ? "bg-red-500" : "bg-emerald-500"}`}
                style={{ width: `${Math.min(100, (deal.days_in_current_stage / Math.max(1, deal.stage_benchmark_days)) * 100)}%` }}
              />
            </div>
            <div className="flex justify-between text-[10px] text-slate-500">
              <span>{deal.days_in_current_stage}j écoulés</span>
              <span>Benchmark : {deal.stage_benchmark_days}j</span>
            </div>
          </div>

          {/* Schedule delta */}
          <div className="flex items-center justify-between bg-slate-800/40 rounded-xl px-4 py-3">
            <span className="text-slate-300 text-sm">Avance/retard sur cycle prévu</span>
            <span className={`font-bold text-base ${deal.schedule_delta_pct >= 0 ? "text-emerald-400" : "text-red-400"}`}>
              {deal.schedule_delta_pct >= 0 ? "+" : ""}{deal.schedule_delta_pct.toFixed(1)}%
            </span>
          </div>

          {/* Score breakdown */}
          <div className="space-y-3">
            <h3 className="text-slate-300 font-semibold text-sm">Analyse de vélocité</h3>
            <ScoreBar value={deal.stage_pace_score} label="Rythme de stage" weight="40%" color="text-blue-400" />
            <ScoreBar value={deal.activity_score} label="Activité & engagement" weight="30%" color="text-violet-400" />
            <ScoreBar value={deal.probability_score} label="Probabilité de gain" weight="20%" color="text-emerald-400" />
            <div className="pt-1 border-t border-slate-800">
              <ScoreBar value={deal.velocity_score} label="Score vélocité global" weight="composite" color="text-white" />
            </div>
          </div>

          {/* Engagement signals */}
          <div className="grid grid-cols-2 gap-3">
            {[
              { label: "Champion identifié", value: deal.champion_present },
              { label: "Décideur engagé", value: deal.decision_maker_engaged },
              { label: "Prochaine étape planifiée", value: deal.has_next_step_scheduled },
              { label: "Activité < 7j", value: deal.last_activity_days <= 7 },
            ].map(({ label, value }) => (
              <div key={label} className={`flex items-center gap-2 px-3 py-2 rounded-lg ${value ? "bg-emerald-950/50 border border-emerald-800/30" : "bg-red-950/30 border border-red-900/20"}`}>
                <span className={value ? "text-emerald-400" : "text-red-400"}>{value ? "✓" : "✗"}</span>
                <span className="text-slate-300 text-xs">{label}</span>
              </div>
            ))}
          </div>

          {/* Momentum signals */}
          {deal.momentum_signals.length > 0 && (
            <div className="space-y-2">
              <h3 className="text-emerald-400 font-semibold text-sm">Signaux positifs</h3>
              <ul className="space-y-1">
                {deal.momentum_signals.map((s, i) => (
                  <li key={i} className="flex items-start gap-2 text-xs text-slate-300">
                    <span className="text-emerald-400 mt-0.5 flex-shrink-0">▲</span>
                    {s}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Risk flags */}
          {deal.risk_flags.length > 0 && (
            <div className="space-y-2">
              <h3 className="text-red-400 font-semibold text-sm">Risques détectés</h3>
              <ul className="space-y-1">
                {deal.risk_flags.map((f, i) => (
                  <li key={i} className="flex items-start gap-2 text-xs text-slate-300">
                    <span className="text-red-400 mt-0.5 flex-shrink-0">▼</span>
                    {f}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Recommended actions */}
          {deal.recommended_actions.length > 0 && (
            <div className="space-y-2">
              <h3 className="text-amber-400 font-semibold text-sm">Actions recommandées</h3>
              <ol className="space-y-1">
                {deal.recommended_actions.map((a, i) => (
                  <li key={i} className="flex items-start gap-2 text-xs text-slate-300">
                    <span className="text-amber-400 font-bold flex-shrink-0 mt-0.5">{i + 1}.</span>
                    {a}
                  </li>
                ))}
              </ol>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

// ─── DealCard ────────────────────────────────────────────────────────────────

function DealCard({ deal, onClick }: { deal: Deal; onClick: () => void }) {
  const status = STATUS_META[deal.velocity_status];
  const action = ACTION_META[deal.velocity_action];

  return (
    <div
      onClick={onClick}
      className="bg-slate-800/60 border border-slate-700/50 rounded-xl p-4 hover:border-slate-500 hover:bg-slate-800 transition-all cursor-pointer space-y-3"
    >
      {/* Header row */}
      <div className="flex items-start gap-3">
        <VelocityRing score={deal.velocity_score} status={deal.velocity_status} />
        <div className="flex-1 min-w-0 space-y-1">
          <p className="text-white font-semibold text-sm truncate leading-tight">{deal.deal_name}</p>
          <p className="text-slate-400 text-xs truncate">{deal.account_name}</p>
          <div className="flex items-center gap-1.5 flex-wrap">
            <span className={`px-1.5 py-0.5 rounded text-[10px] font-semibold ${status.color} bg-slate-700`}>
              {status.label}
            </span>
            <span className={`px-1.5 py-0.5 rounded text-[10px] font-semibold ${action.color} ${action.bg}`}>
              {action.label}
            </span>
          </div>
        </div>
      </div>

      {/* Stage + ARR row */}
      <div className="flex items-center justify-between text-xs text-slate-400 border-t border-slate-700/50 pt-2">
        <span className={`px-2 py-0.5 rounded text-[10px] font-medium ${deal.stage_overdue ? "bg-red-950/50 text-red-400" : "bg-slate-700 text-slate-300"}`}>
          {STAGE_LABELS[deal.stage] ?? deal.stage}
          {deal.stage_overdue && " ⚠"}
        </span>
        <span className="text-white font-semibold">{fmtEur(deal.arr_eur)}</span>
      </div>

      {/* Velocity EUR/day */}
      <div className="flex items-center justify-between text-xs">
        <span className="text-slate-400">Vélocité</span>
        <span className={`font-semibold ${status.color}`}>{fmtEur(deal.velocity_eur_per_day)}/j</span>
      </div>

      {/* Score bars */}
      <div className="space-y-1.5 pt-1 border-t border-slate-700/50">
        <MiniBar value={deal.stage_pace_score} label="Rythme stage" color="bg-blue-500" />
        <MiniBar value={deal.activity_score} label="Activité" color="bg-violet-500" />
        <MiniBar value={deal.probability_score} label="Probabilité" color="bg-emerald-500" />
      </div>

      {/* Schedule delta */}
      <div className="flex items-center justify-between text-[11px] border-t border-slate-700/50 pt-2">
        <span className="text-slate-500">Cycle prévu</span>
        <span className={deal.schedule_delta_pct >= 0 ? "text-emerald-400" : "text-red-400"}>
          {deal.schedule_delta_pct >= 0 ? "+" : ""}{deal.schedule_delta_pct.toFixed(1)}%
        </span>
      </div>

      {/* Flag count */}
      {deal.risk_flags.length > 0 && (
        <div className="text-[10px] text-red-400">
          ▼ {deal.risk_flags.length} risque{deal.risk_flags.length > 1 ? "s" : ""} détecté{deal.risk_flags.length > 1 ? "s" : ""}
        </div>
      )}
    </div>
  );
}

// ─── Main Page ────────────────────────────────────────────────────────────────

type StatusFilter = "all" | VelocityStatus;

export default function PipelineVelocityPage() {
  const [deals, setDeals] = useState<Deal[]>([]);
  const [summary, setSummary] = useState<Summary | null>(null);
  const [filter, setFilter] = useState<StatusFilter>("all");
  const [loading, setLoading] = useState(true);
  const [selected, setSelected] = useState<Deal | null>(null);

  useEffect(() => {
    const params = new URLSearchParams();
    if (filter !== "all") params.set("status", filter);
    fetch(`/api/pipeline-velocity?${params}`)
      .then((r) => r.json())
      .then((data) => {
        setDeals(data.deals ?? []);
        setSummary(data.summary ?? null);
        setLoading(false);
      });
  }, [filter]);

  const tabs: { key: StatusFilter; label: string; color?: string }[] = [
    { key: "all", label: "Tous" },
    { key: "fast", label: "Rapide", color: "text-emerald-400" },
    { key: "on_pace", label: "En rythme", color: "text-blue-400" },
    { key: "slow", label: "Lent", color: "text-amber-400" },
    { key: "stalled", label: "Bloqué", color: "text-red-400" },
  ];

  // Status distribution bar
  const total = summary?.total ?? 0;
  const statusBars = summary
    ? [
        { key: "fast", count: summary.status_counts.fast ?? 0, bg: "bg-emerald-500" },
        { key: "on_pace", count: summary.status_counts.on_pace ?? 0, bg: "bg-blue-500" },
        { key: "slow", count: summary.status_counts.slow ?? 0, bg: "bg-amber-500" },
        { key: "stalled", count: summary.status_counts.stalled ?? 0, bg: "bg-red-500" },
      ]
    : [];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-white">Pipeline Velocity</h1>
        <p className="text-slate-400 text-sm mt-1">Mesure du momentum des deals et du débit du pipeline commercial</p>
      </div>

      {/* KPI Strip */}
      {summary && (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {[
            { label: "Deals actifs", value: summary.total.toString(), sub: `${summary.close_now_count} à closer maintenant`, color: "text-white" },
            { label: "Vélocité totale", value: `${fmtEur(summary.total_velocity_eur_per_day)}/j`, sub: "Pipeline pondéré par jour", color: "text-blue-400" },
            { label: "Deals bloqués", value: summary.stalled_count.toString(), sub: `${summary.rescue_count} en sauvetage urgent`, color: summary.stalled_count > 0 ? "text-red-400" : "text-slate-400" },
            { label: "Pipeline total", value: fmtEur(summary.total_pipeline_eur), sub: `Pondéré : ${fmtEur(summary.total_weighted_pipeline_eur)}`, color: "text-emerald-400" },
          ].map(({ label, value, sub, color }) => (
            <div key={label} className="bg-slate-800/60 border border-slate-700/50 rounded-xl p-4">
              <p className="text-slate-400 text-xs mb-1">{label}</p>
              <p className={`text-xl font-bold ${color}`}>{value}</p>
              <p className="text-slate-500 text-xs mt-1">{sub}</p>
            </div>
          ))}
        </div>
      )}

      {/* Status distribution bar */}
      {total > 0 && (
        <div className="space-y-2">
          <div className="flex items-center justify-between text-xs text-slate-400">
            <span>Distribution de vélocité</span>
            <span>{total} deals</span>
          </div>
          <div className="flex h-2 rounded-full overflow-hidden gap-0.5">
            {statusBars.map(({ key, count, bg }) =>
              count > 0 ? (
                <div key={key} className={`${bg} transition-all`} style={{ width: `${(count / total) * 100}%` }} />
              ) : null
            )}
          </div>
          <div className="flex flex-wrap gap-3 text-xs">
            {statusBars.map(({ key, count, bg }) => (
              <span key={key} className="flex items-center gap-1 text-slate-400">
                <span className={`w-2 h-2 rounded-full ${bg}`} />
                {STATUS_META[key as VelocityStatus].label} ({count})
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Filter tabs */}
      <div className="flex flex-wrap gap-2">
        {tabs.map(({ key, label, color }) => (
          <button
            key={key}
            onClick={() => setFilter(key)}
            className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-colors ${
              filter === key
                ? "bg-indigo-600 text-white"
                : `text-slate-400 hover:text-white hover:bg-slate-800 ${color ?? ""}`
            }`}
          >
            {label}
            {key !== "all" && summary && (
              <span className="ml-1.5 text-xs opacity-70">
                ({summary.status_counts[key] ?? 0})
              </span>
            )}
          </button>
        ))}
      </div>

      {/* Deal grid */}
      {loading ? (
        <div className="flex items-center justify-center h-48 text-slate-500">Chargement…</div>
      ) : deals.length === 0 ? (
        <div className="flex items-center justify-center h-48 text-slate-500">Aucun deal trouvé</div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
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
