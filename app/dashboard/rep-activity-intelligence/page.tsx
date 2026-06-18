"use client";

import { useState, useEffect, useCallback } from "react";

// ─── Types ────────────────────────────────────────────────────────────────────

interface RepResult {
  rep_id: string;
  rep_name: string;
  region: string;
  segment: string;
  activity_tier: string;
  activity_trend: string;
  coaching_focus: string;
  activity_action: string;
  activity_score: number;
  call_index: number;
  email_index: number;
  meeting_index: number;
  proposal_index: number;
  connect_rate_pct: number;
  email_reply_rate_pct: number;
  meeting_show_rate_pct: number;
  deals_created_30d: number;
  pipeline_generated_eur: number;
  coaching_insights: string[];
  action_items: string[];
}

interface Summary {
  total: number;
  tier_counts: Record<string, number>;
  trend_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_activity_score: number;
  total_pipeline_generated_eur: number;
  elite_count: number;
  inactive_count: number;
  intervention_count: number;
  declining_count: number;
}

// ─── Helpers ──────────────────────────────────────────────────────────────────

function formatEur(n: number): string {
  if (n >= 1_000_000) return `${(n / 1_000_000).toFixed(1)}M€`;
  if (n >= 1_000)     return `${Math.round(n / 1_000)}k€`;
  return `${Math.round(n)}€`;
}

function tierColor(tier: string): string {
  switch (tier) {
    case "elite":    return "#6366f1";
    case "high":     return "#10b981";
    case "average":  return "#f59e0b";
    case "low":      return "#f97316";
    case "inactive": return "#ef4444";
    default:         return "#64748b";
  }
}

function tierBg(tier: string): string {
  switch (tier) {
    case "elite":    return "bg-indigo-500/15 border-indigo-500/30";
    case "high":     return "bg-emerald-500/15 border-emerald-500/30";
    case "average":  return "bg-amber-500/15 border-amber-500/30";
    case "low":      return "bg-orange-500/15 border-orange-500/30";
    case "inactive": return "bg-red-500/15 border-red-500/30";
    default:         return "bg-slate-700/30 border-slate-600/30";
  }
}

function tierLabel(tier: string): string {
  switch (tier) {
    case "elite":    return "Élite";
    case "high":     return "Élevé";
    case "average":  return "Moyen";
    case "low":      return "Faible";
    case "inactive": return "Inactif";
    default:         return tier;
  }
}

function trendLabel(trend: string): string {
  switch (trend) {
    case "accelerating": return "↑ Accélère";
    case "stable":       return "→ Stable";
    case "declining":    return "↓ Décline";
    case "stalled":      return "⚠ Stoppé";
    default:             return trend;
  }
}

function trendColor(trend: string): string {
  switch (trend) {
    case "accelerating": return "text-emerald-400";
    case "stable":       return "text-slate-300";
    case "declining":    return "text-amber-400";
    case "stalled":      return "text-red-400";
    default:             return "text-slate-400";
  }
}

function actionLabel(action: string): string {
  switch (action) {
    case "celebrate":  return "Célébrer";
    case "maintain":   return "Maintenir";
    case "nudge":      return "Ajuster";
    case "coach":      return "Coacher";
    case "intervene":  return "Intervenir";
    default:           return action;
  }
}

function actionBadge(action: string): string {
  switch (action) {
    case "celebrate":  return "bg-indigo-500/20 text-indigo-300 border-indigo-500/30";
    case "maintain":   return "bg-emerald-500/20 text-emerald-300 border-emerald-500/30";
    case "nudge":      return "bg-amber-500/20 text-amber-300 border-amber-500/30";
    case "coach":      return "bg-orange-500/20 text-orange-300 border-orange-500/30";
    case "intervene":  return "bg-red-500/20 text-red-300 border-red-500/30";
    default:           return "bg-slate-700/30 text-slate-300 border-slate-600/30";
  }
}

function focusLabel(focus: string): string {
  switch (focus) {
    case "calls":       return "Appels";
    case "emails":      return "Emails";
    case "meetings":    return "Réunions";
    case "prospecting": return "Prospection";
    case "follow_up":   return "Relances";
    case "quality":     return "Qualité";
    case "on_track":    return "Sur cible";
    default:            return focus;
  }
}

function indexColor(idx: number): string {
  if (idx >= 1.2) return "text-emerald-400";
  if (idx >= 0.8) return "text-slate-300";
  if (idx >= 0.5) return "text-amber-400";
  return "text-red-400";
}

// ─── Activity Score Ring ──────────────────────────────────────────────────────

function ActivityRing({ score, tier, size = 80 }: { score: number; tier: string; size?: number }) {
  const cx = size / 2;
  const cy = size / 2;
  const r  = (size - 10) / 2;
  const circ = 2 * Math.PI * r;
  const arc  = (score / 100) * circ;
  const color = tierColor(tier);

  return (
    <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`} className="flex-shrink-0">
      <circle cx={cx} cy={cy} r={r} fill="none" stroke="#1e293b" strokeWidth="8" />
      <circle
        cx={cx} cy={cy} r={r}
        fill="none"
        stroke={color}
        strokeWidth="8"
        strokeDasharray={`${arc} ${circ - arc}`}
        strokeLinecap="round"
        transform={`rotate(-90 ${cx} ${cy})`}
      />
      <text x={cx} y={cy - 4} textAnchor="middle" fill="white" fontSize={size * 0.22} fontWeight="bold">
        {Math.round(score)}
      </text>
      <text x={cx} y={cy + size * 0.14} textAnchor="middle" fill="#94a3b8" fontSize={size * 0.13}>
        score
      </text>
    </svg>
  );
}

// ─── Index Bar Row ────────────────────────────────────────────────────────────

function IndexBar({ label, index }: { label: string; index: number }) {
  const pct = Math.min(100, index * 100);
  return (
    <div>
      <div className="flex justify-between text-xs text-slate-400 mb-1">
        <span>{label}</span>
        <span className={indexColor(index)}>{index.toFixed(2)}×</span>
      </div>
      <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
        <div
          className={`h-full rounded-full ${index >= 1.0 ? "bg-emerald-500" : index >= 0.7 ? "bg-amber-500" : "bg-red-500"}`}
          style={{ width: `${pct}%` }}
        />
      </div>
    </div>
  );
}

// ─── Tier Distribution Bar ────────────────────────────────────────────────────

function TierDistributionBar({ counts, total }: { counts: Record<string, number>; total: number }) {
  const tiers = [
    { key: "elite",    label: "Élite",    color: "bg-indigo-500" },
    { key: "high",     label: "Élevé",    color: "bg-emerald-500" },
    { key: "average",  label: "Moyen",    color: "bg-amber-500" },
    { key: "low",      label: "Faible",   color: "bg-orange-500" },
    { key: "inactive", label: "Inactif",  color: "bg-red-500" },
  ];
  return (
    <div className="space-y-2">
      <div className="flex h-3 rounded-full overflow-hidden gap-0.5">
        {tiers.map(({ key, color }) => {
          const pct = total > 0 ? ((counts[key] || 0) / total) * 100 : 0;
          return pct > 0 ? (
            <div key={key} className={`${color} h-full`} style={{ width: `${pct}%` }} title={`${counts[key] || 0}`} />
          ) : null;
        })}
      </div>
      <div className="flex gap-4 flex-wrap">
        {tiers.map(({ key, label, color }) => (
          <div key={key} className="flex items-center gap-1.5">
            <div className={`w-2.5 h-2.5 rounded-full ${color}`} />
            <span className="text-xs text-slate-400">{label} <span className="text-white font-medium">{counts[key] || 0}</span></span>
          </div>
        ))}
      </div>
    </div>
  );
}

// ─── Rep Modal ────────────────────────────────────────────────────────────────

function RepModal({ rep, onClose }: { rep: RepResult; onClose: () => void }) {
  const [tab, setTab] = useState<"insights" | "actions" | "indices">("insights");

  useEffect(() => {
    const h = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    document.addEventListener("keydown", h);
    return () => document.removeEventListener("keydown", h);
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
            <div>
              <h2 className="text-lg font-semibold text-white">{rep.rep_name}</h2>
              <p className="text-sm text-slate-400 mt-0.5">{rep.region} · {rep.segment}</p>
            </div>
            <button onClick={onClose} className="text-slate-500 hover:text-white text-xl leading-none mt-0.5">×</button>
          </div>

          <div className="grid grid-cols-4 gap-3 mt-4">
            {[
              { label: "Score", value: String(Math.round(rep.activity_score)) },
              { label: "Deals créés", value: String(rep.deals_created_30d) },
              { label: "Pipeline 30j", value: formatEur(rep.pipeline_generated_eur) },
              { label: "Taux connexion", value: `${rep.connect_rate_pct.toFixed(0)}%` },
            ].map(({ label, value }) => (
              <div key={label} className="bg-slate-800/60 rounded-lg p-3 text-center">
                <p className="text-lg font-bold text-white">{value}</p>
                <p className="text-xs text-slate-400 mt-0.5">{label}</p>
              </div>
            ))}
          </div>

          <div className="flex gap-2 mt-3 flex-wrap">
            <span className={`text-xs px-3 py-1 rounded-full border font-medium ${tierBg(rep.activity_tier)}`}
              style={{ color: tierColor(rep.activity_tier) }}>
              {tierLabel(rep.activity_tier)}
            </span>
            <span className={`text-xs font-medium ${trendColor(rep.activity_trend)}`}>{trendLabel(rep.activity_trend)}</span>
            <span className={`text-xs px-3 py-1 rounded-full border ${actionBadge(rep.activity_action)}`}>
              {actionLabel(rep.activity_action)}
            </span>
            <span className="text-xs text-slate-400">Focus : <span className="text-slate-200">{focusLabel(rep.coaching_focus)}</span></span>
          </div>
        </div>

        {/* Tabs */}
        <div className="border-b border-slate-800 flex">
          {(["insights", "actions", "indices"] as const).map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`flex-1 py-3 text-sm font-medium transition-colors ${
                tab === t ? "text-indigo-400 border-b-2 border-indigo-500" : "text-slate-500 hover:text-slate-300"
              }`}
            >
              {t === "insights" ? "Insights coaching" : t === "actions" ? "Plan d'action" : "Indices activité"}
            </button>
          ))}
        </div>

        <div className="p-6 space-y-3">
          {tab === "insights" && rep.coaching_insights.map((ins, i) => (
            <div key={i} className="flex gap-3 items-start">
              <div className="w-1.5 h-1.5 rounded-full bg-indigo-400 mt-2 flex-shrink-0" />
              <p className="text-sm text-slate-300">{ins}</p>
            </div>
          ))}
          {tab === "actions" && rep.action_items.map((a, i) => (
            <div key={i} className="flex gap-3 items-start">
              <div className="w-5 h-5 rounded-full bg-indigo-600/30 border border-indigo-500/40 flex items-center justify-center flex-shrink-0 mt-0.5">
                <span className="text-[10px] text-indigo-300 font-bold">{i + 1}</span>
              </div>
              <p className="text-sm text-slate-300">{a}</p>
            </div>
          ))}
          {tab === "indices" && (
            <div className="space-y-4">
              <IndexBar label="Appels" index={rep.call_index} />
              <IndexBar label="Emails" index={rep.email_index} />
              <IndexBar label="Réunions" index={rep.meeting_index} />
              <IndexBar label="Propositions" index={rep.proposal_index} />
              <div className="pt-2 border-t border-slate-800 grid grid-cols-3 gap-3">
                {[
                  { label: "Taux connexion", value: `${rep.connect_rate_pct.toFixed(1)}%`, good: rep.connect_rate_pct >= 20 },
                  { label: "Réponse email",  value: `${rep.email_reply_rate_pct.toFixed(1)}%`, good: rep.email_reply_rate_pct >= 15 },
                  { label: "Taux présence",  value: `${rep.meeting_show_rate_pct.toFixed(1)}%`, good: rep.meeting_show_rate_pct >= 75 },
                ].map(({ label, value, good }) => (
                  <div key={label} className="bg-slate-800/60 rounded-lg p-3 text-center">
                    <p className={`text-lg font-bold ${good ? "text-emerald-400" : "text-amber-400"}`}>{value}</p>
                    <p className="text-xs text-slate-400 mt-0.5">{label}</p>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

// ─── Rep Card ─────────────────────────────────────────────────────────────────

function RepCard({ rep, onClick }: { rep: RepResult; onClick: () => void }) {
  return (
    <button
      onClick={onClick}
      className={`w-full text-left p-4 rounded-xl border transition-all hover:border-indigo-500/40 hover:bg-slate-800/60 ${tierBg(rep.activity_tier)}`}
    >
      <div className="flex items-start gap-4">
        <ActivityRing score={rep.activity_score} tier={rep.activity_tier} size={72} />

        <div className="flex-1 min-w-0">
          <div className="flex items-start justify-between gap-2">
            <div className="min-w-0">
              <h3 className="text-sm font-semibold text-white truncate">{rep.rep_name}</h3>
              <p className="text-xs text-slate-400 mt-0.5">{rep.region} · {rep.segment}</p>
            </div>
            <span className="text-xs font-medium text-slate-300 flex-shrink-0">{formatEur(rep.pipeline_generated_eur)}</span>
          </div>

          <div className="flex items-center gap-2 mt-2 flex-wrap">
            <span className="text-xs font-medium" style={{ color: tierColor(rep.activity_tier) }}>
              {tierLabel(rep.activity_tier)}
            </span>
            <span className="text-slate-600">·</span>
            <span className={`text-xs ${trendColor(rep.activity_trend)}`}>{trendLabel(rep.activity_trend)}</span>
            <span className="text-slate-600">·</span>
            <span className={`text-xs px-2 py-0.5 rounded-full border ${actionBadge(rep.activity_action)}`}>
              {actionLabel(rep.activity_action)}
            </span>
          </div>

          {/* Micro index bars */}
          <div className="grid grid-cols-4 gap-2 mt-2.5">
            {[
              { label: "Appels", idx: rep.call_index },
              { label: "Emails", idx: rep.email_index },
              { label: "RDV",    idx: rep.meeting_index },
              { label: "Props",  idx: rep.proposal_index },
            ].map(({ label, idx }) => (
              <div key={label}>
                <div className="flex justify-between text-[10px] text-slate-500 mb-0.5">
                  <span>{label}</span>
                  <span className={indexColor(idx)}>{idx.toFixed(1)}×</span>
                </div>
                <div className="h-1 bg-slate-800 rounded-full overflow-hidden">
                  <div
                    className={`h-full rounded-full ${idx >= 1.0 ? "bg-emerald-500" : idx >= 0.7 ? "bg-amber-500" : "bg-red-500"}`}
                    style={{ width: `${Math.min(100, idx * 100)}%` }}
                  />
                </div>
              </div>
            ))}
          </div>

          <div className="mt-2 text-xs text-slate-500">
            Focus coaching : <span className="text-slate-300">{focusLabel(rep.coaching_focus)}</span>
            {rep.deals_created_30d > 0 && (
              <> · <span className="text-slate-300">{rep.deals_created_30d} deal{rep.deals_created_30d > 1 ? "s" : ""} créés</span></>
            )}
          </div>
        </div>
      </div>
    </button>
  );
}

// ─── Page ─────────────────────────────────────────────────────────────────────

export default function RepActivityIntelligencePage() {
  const [reps, setReps] = useState<RepResult[]>([]);
  const [summary, setSummary] = useState<Summary | null>(null);
  const [loading, setLoading] = useState(true);
  const [selected, setSelected] = useState<RepResult | null>(null);
  const [tierFilter, setTierFilter]     = useState("all");
  const [actionFilter, setActionFilter] = useState("all");

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const params = new URLSearchParams();
      if (tierFilter !== "all")   params.set("tier", tierFilter);
      if (actionFilter !== "all") params.set("action", actionFilter);
      const res = await fetch(`/api/rep-activity-intelligence?${params}`);
      const data = await res.json();
      setReps(data.reps ?? []);
      setSummary(data.summary ?? null);
    } catch {}
    setLoading(false);
  }, [tierFilter, actionFilter]);

  useEffect(() => { load(); }, [load]);

  const TIER_TABS = [
    { key: "all",      label: "Tous" },
    { key: "elite",    label: "Élite" },
    { key: "high",     label: "Élevé" },
    { key: "average",  label: "Moyen" },
    { key: "low",      label: "Faible" },
    { key: "inactive", label: "Inactif" },
  ];

  const ACTION_TABS = [
    { key: "all",        label: "Toutes" },
    { key: "celebrate",  label: "Célébrer" },
    { key: "maintain",   label: "Maintenir" },
    { key: "nudge",      label: "Ajuster" },
    { key: "coach",      label: "Coacher" },
    { key: "intervene",  label: "Intervenir" },
  ];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">

        <div>
          <h1 className="text-2xl font-bold text-white">Intelligence Activité Commerciale</h1>
          <p className="text-sm text-slate-400 mt-1">
            Benchmarking volume · Détection de décrochage · Coaching ciblé par levier
          </p>
        </div>

        {summary && (
          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-4">
            {[
              { label: "Reps suivis",     value: String(summary.total) },
              { label: "Score moy.",      value: String(summary.avg_activity_score) },
              { label: "Pipeline 30j",    value: formatEur(summary.total_pipeline_generated_eur) },
              { label: "Reps Élite",      value: String(summary.elite_count), accent: true },
              { label: "Inactifs",        value: String(summary.inactive_count), warn: summary.inactive_count > 0 },
              { label: "Nécessitent aide",value: String(summary.intervention_count), warn: summary.intervention_count > 0 },
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

        {summary && (
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
            <h2 className="text-sm font-semibold text-slate-300 mb-4">Distribution des niveaux d'activité</h2>
            <TierDistributionBar counts={summary.tier_counts} total={summary.total} />
          </div>
        )}

        {/* Tier filter */}
        <div className="flex gap-2 flex-wrap">
          {TIER_TABS.map(({ key, label }) => (
            <button
              key={key}
              onClick={() => setTierFilter(key)}
              className={`px-4 py-2 rounded-lg text-sm font-medium border transition-colors ${
                tierFilter === key
                  ? "bg-indigo-600 border-indigo-500 text-white"
                  : "bg-slate-900 border-slate-700 text-slate-400 hover:text-white"
              }`}
            >
              {label}
              {summary && key !== "all" && (
                <span className="ml-1.5 text-xs opacity-70">({summary.tier_counts[key] || 0})</span>
              )}
            </button>
          ))}
        </div>

        {/* Action filter */}
        <div className="flex gap-2 flex-wrap">
          {ACTION_TABS.map(({ key, label }) => (
            <button
              key={key}
              onClick={() => setActionFilter(key)}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium border transition-colors ${
                actionFilter === key
                  ? "bg-violet-600/30 border-violet-500/50 text-violet-300"
                  : "bg-slate-900 border-slate-700 text-slate-400 hover:text-white"
              }`}
            >
              {label}
              {summary && key !== "all" && (
                <span className="ml-1 opacity-70">({summary.action_counts[key] || 0})</span>
              )}
            </button>
          ))}
        </div>

        {loading ? (
          <div className="flex items-center justify-center py-24">
            <div className="w-8 h-8 border-2 border-indigo-500 border-t-transparent rounded-full animate-spin" />
          </div>
        ) : reps.length === 0 ? (
          <div className="text-center py-24 text-slate-500">Aucun rep ne correspond aux filtres.</div>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
            {reps.map((r) => (
              <RepCard key={r.rep_id} rep={r} onClick={() => setSelected(r)} />
            ))}
          </div>
        )}
      </div>

      {selected && <RepModal rep={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
