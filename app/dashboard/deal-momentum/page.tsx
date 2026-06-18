"use client";

import { useEffect, useState, useCallback } from "react";

// ── Types ────────────────────────────────────────────────────────────────────

interface DealData {
  deal_id: string;
  rep_id: string;
  rep_name: string;
  account_name: string;
  momentum_score: number;
  velocity_score: number;
  engagement_score: number;
  risk_score: number;
  momentum_level: string;
  stall_reason: string;
  momentum_trend: string;
  momentum_action: string;
  momentum_indicators: string[];
  risk_signals: string[];
  recommended_actions: string[];
}

interface Summary {
  total: number;
  level_counts: Record<string, number>;
  action_counts: Record<string, number>;
  trend_counts: Record<string, number>;
  avg_momentum_score: number;
  avg_velocity_score: number;
  avg_engagement_score: number;
  avg_risk_score: number;
  at_risk_count: number;
  stalled_count: number;
}

// ── Helpers ──────────────────────────────────────────────────────────────────

function levelColor(level: string) {
  switch (level) {
    case "accelerating": return { ring: "#10b981", text: "text-emerald-400", bg: "bg-emerald-500/20", border: "border-emerald-500/30" };
    case "positive":     return { ring: "#6366f1", text: "text-indigo-400",  bg: "bg-indigo-500/20",  border: "border-indigo-500/30" };
    case "neutral":      return { ring: "#64748b", text: "text-slate-400",   bg: "bg-slate-500/20",   border: "border-slate-500/30" };
    case "stalling":     return { ring: "#f59e0b", text: "text-amber-400",   bg: "bg-amber-500/20",   border: "border-amber-500/30" };
    case "declining":    return { ring: "#f97316", text: "text-orange-400",  bg: "bg-orange-500/20",  border: "border-orange-500/30" };
    case "stalled":      return { ring: "#ef4444", text: "text-red-400",     bg: "bg-red-500/20",     border: "border-red-500/30" };
    default:             return { ring: "#64748b", text: "text-slate-400",   bg: "bg-slate-500/20",   border: "border-slate-500/30" };
  }
}

function levelLabel(level: string) {
  const map: Record<string, string> = {
    accelerating: "Accélérant",
    positive:     "Positif",
    neutral:      "Neutre",
    stalling:     "Ralentissement",
    declining:    "En déclin",
    stalled:      "Bloqué",
  };
  return map[level] ?? level;
}

function trendLabel(trend: string) {
  const map: Record<string, string> = {
    improving:    "Progression",
    stable:       "Stable",
    deteriorating:"Dégradation",
    critical:     "Critique",
  };
  return map[trend] ?? trend;
}

function trendColor(trend: string) {
  switch (trend) {
    case "improving":     return "text-emerald-400";
    case "stable":        return "text-slate-400";
    case "deteriorating": return "text-amber-400";
    case "critical":      return "text-red-400";
    default:              return "text-slate-400";
  }
}

function actionLabel(action: string) {
  const map: Record<string, string> = {
    maintain:              "Maintenir",
    accelerate:            "Accélérer",
    re_engage:             "Relancer",
    executive_escalation:  "Escalade Exec",
    competitive_defense:   "Défense Concurr.",
    champion_recovery:     "Récupérer Champion",
    technical_resolution:  "Résolution Tech.",
    close_or_abandon:      "Clore / Abandonner",
  };
  return map[action] ?? action;
}

function stall_label(reason: string) {
  const map: Record<string, string> = {
    no_stall:              "Aucun blocage",
    decision_delayed:      "Décision retardée",
    budget_frozen:         "Budget gelé",
    stakeholder_change:    "Changement parties",
    competitive_threat:    "Menace concurrente",
    champion_left:         "Champion parti",
    technical_blocker:     "Blocage technique",
    internal_misalignment: "Désalignement interne",
  };
  return map[reason] ?? reason;
}

// ── SVG Momentum Ring ────────────────────────────────────────────────────────

function MomentumRing({
  score,
  level,
  size = 80,
}: {
  score: number;
  level: string;
  size?: number;
}) {
  const { ring } = levelColor(level);
  const cx = size / 2;
  const cy = size / 2;
  const r = size * 0.38;
  const circ = 2 * Math.PI * r;
  const arc = (score / 100) * circ;
  const strokeW = size * 0.09;

  return (
    <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`} aria-hidden="true">
      <circle cx={cx} cy={cy} r={r} fill="none" stroke="#1e293b" strokeWidth={strokeW} />
      <circle
        cx={cx} cy={cy} r={r}
        fill="none"
        stroke={ring}
        strokeWidth={strokeW}
        strokeDasharray={`${arc} ${circ - arc}`}
        strokeLinecap="round"
        transform={`rotate(-90 ${cx} ${cy})`}
      />
      <text x={cx} y={cy + 5} textAnchor="middle" fill="white" fontSize={size * 0.18} fontWeight="700">
        {Math.round(score)}
      </text>
    </svg>
  );
}

// ── Level Distribution Bar ────────────────────────────────────────────────────

function LevelDistBar({ counts, total }: { counts: Record<string, number>; total: number }) {
  const levels = [
    { key: "accelerating", color: "#10b981" },
    { key: "positive",     color: "#6366f1" },
    { key: "neutral",      color: "#64748b" },
    { key: "stalling",     color: "#f59e0b" },
    { key: "declining",    color: "#f97316" },
    { key: "stalled",      color: "#ef4444" },
  ];
  return (
    <div className="flex h-2.5 rounded-full overflow-hidden gap-px bg-slate-800">
      {levels.map(({ key, color }) => {
        const pct = total > 0 ? ((counts[key] ?? 0) / total) * 100 : 0;
        return pct > 0 ? (
          <div key={key} style={{ width: `${pct}%`, background: color }} title={`${levelLabel(key)}: ${counts[key]}`} />
        ) : null;
      })}
    </div>
  );
}

// ── Mini score bar ────────────────────────────────────────────────────────────

function ScoreBar({ value, color, label }: { value: number; color: string; label: string }) {
  return (
    <div>
      <div className="flex justify-between text-[10px] text-slate-500 mb-0.5">
        <span>{label}</span>
        <span className="text-slate-400">{Math.round(value)}</span>
      </div>
      <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
        <div className="h-full rounded-full" style={{ width: `${value}%`, background: color }} />
      </div>
    </div>
  );
}

// ── Deal Card ────────────────────────────────────────────────────────────────

function DealCard({ deal, onClick }: { deal: DealData; onClick: () => void }) {
  const col = levelColor(deal.momentum_level);
  return (
    <button
      onClick={onClick}
      className={`w-full text-left rounded-xl border p-4 transition-all hover:brightness-110 ${col.bg} ${col.border}`}
    >
      <div className="flex items-start gap-4">
        <MomentumRing score={deal.momentum_score} level={deal.momentum_level} size={72} />
        <div className="flex-1 min-w-0">
          <div className="flex items-center justify-between gap-2 mb-1">
            <span className="text-white font-semibold text-sm truncate">{deal.account_name}</span>
            <span className={`text-xs font-medium px-2 py-0.5 rounded-full ${col.bg} ${col.text} border ${col.border}`}>
              {levelLabel(deal.momentum_level)}
            </span>
          </div>
          <p className="text-xs text-slate-500 mb-2">{deal.rep_name}</p>
          <div className="grid grid-cols-3 gap-2 mb-2">
            <ScoreBar value={deal.velocity_score}   color="#6366f1" label="Vélocité" />
            <ScoreBar value={deal.engagement_score} color="#10b981" label="Engagement" />
            <ScoreBar value={deal.risk_score}       color="#ef4444" label="Risque" />
          </div>
          <div className="flex items-center justify-between text-[10px]">
            <span className={`font-medium ${trendColor(deal.momentum_trend)}`}>
              ↗ {trendLabel(deal.momentum_trend)}
            </span>
            <span className="text-slate-500 truncate ml-2">
              {actionLabel(deal.momentum_action)}
            </span>
          </div>
          {deal.stall_reason !== "no_stall" && (
            <div className="mt-1 text-[10px] text-amber-400 truncate">
              ⚠ {stall_label(deal.stall_reason)}
            </div>
          )}
        </div>
      </div>
    </button>
  );
}

// ── Deal Modal ───────────────────────────────────────────────────────────────

function DealModal({ deal, onClose }: { deal: DealData; onClose: () => void }) {
  const col = levelColor(deal.momentum_level);
  const [tab, setTab] = useState<"actions" | "indicators" | "risks">("actions");

  useEffect(() => {
    const handler = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    document.addEventListener("keydown", handler);
    return () => document.removeEventListener("keydown", handler);
  }, [onClose]);

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 p-4"
      onClick={onClose}
    >
      <div
        className="w-full max-w-2xl bg-slate-900 border border-slate-700 rounded-2xl shadow-2xl max-h-[90vh] overflow-y-auto"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className={`flex items-center justify-between p-5 border-b border-slate-800`}>
          <div className="flex items-center gap-4">
            <MomentumRing score={deal.momentum_score} level={deal.momentum_level} size={64} />
            <div>
              <h2 className="text-white font-bold text-lg">{deal.account_name}</h2>
              <p className="text-slate-400 text-sm">{deal.rep_name}</p>
              <div className="flex items-center gap-2 mt-1">
                <span className={`text-xs font-medium px-2 py-0.5 rounded-full ${col.bg} ${col.text} border ${col.border}`}>
                  {levelLabel(deal.momentum_level)}
                </span>
                <span className={`text-xs ${trendColor(deal.momentum_trend)}`}>
                  {trendLabel(deal.momentum_trend)}
                </span>
                {deal.stall_reason !== "no_stall" && (
                  <span className="text-xs text-amber-400">⚠ {stall_label(deal.stall_reason)}</span>
                )}
              </div>
            </div>
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-white text-2xl leading-none">×</button>
        </div>

        {/* Score breakdown */}
        <div className="grid grid-cols-3 gap-3 p-5 border-b border-slate-800">
          {[
            { label: "Vélocité", value: deal.velocity_score, color: "#6366f1" },
            { label: "Engagement", value: deal.engagement_score, color: "#10b981" },
            { label: "Risque", value: deal.risk_score, color: "#ef4444" },
          ].map(({ label, value, color }) => (
            <div key={label} className="bg-slate-800/50 rounded-lg p-3 text-center">
              <div className="text-2xl font-bold" style={{ color }}>{Math.round(value)}</div>
              <div className="text-xs text-slate-400">{label}</div>
            </div>
          ))}
        </div>

        {/* Tabs */}
        <div className="flex border-b border-slate-800 px-5">
          {(["actions", "indicators", "risks"] as const).map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`px-4 py-3 text-sm font-medium border-b-2 transition-colors ${
                tab === t ? "border-indigo-500 text-indigo-400" : "border-transparent text-slate-500 hover:text-slate-300"
              }`}
            >
              {t === "actions" ? "Actions recommandées" : t === "indicators" ? "Indicateurs momentum" : "Signaux de risque"}
            </button>
          ))}
        </div>

        {/* Tab content */}
        <div className="p-5 space-y-3">
          {tab === "actions" && (
            <>
              <div className={`text-sm font-medium px-3 py-2 rounded-lg ${col.bg} ${col.text} border ${col.border}`}>
                Stratégie : {actionLabel(deal.momentum_action)}
              </div>
              {deal.recommended_actions.map((a, i) => (
                <div key={i} className="flex gap-2 text-sm text-slate-300 bg-slate-800/50 rounded-lg p-3">
                  <span className="text-indigo-400 flex-shrink-0">→</span>
                  <span>{a}</span>
                </div>
              ))}
              {deal.recommended_actions.length === 0 && (
                <p className="text-slate-500 text-sm">Aucune action recommandée.</p>
              )}
            </>
          )}

          {tab === "indicators" && (
            <>
              {deal.momentum_indicators.length > 0 ? (
                deal.momentum_indicators.map((ind, i) => (
                  <div key={i} className="flex gap-2 text-sm text-slate-300 bg-slate-800/50 rounded-lg p-3">
                    <span className="text-emerald-400 flex-shrink-0">✓</span>
                    <span>{ind}</span>
                  </div>
                ))
              ) : (
                <p className="text-slate-500 text-sm">Aucun indicateur de momentum positif détecté.</p>
              )}
            </>
          )}

          {tab === "risks" && (
            <>
              {deal.risk_signals.length > 0 ? (
                deal.risk_signals.map((sig, i) => (
                  <div key={i} className="flex gap-2 text-sm text-slate-300 bg-red-500/10 border border-red-500/20 rounded-lg p-3">
                    <span className="text-red-400 flex-shrink-0">⚠</span>
                    <span>{sig}</span>
                  </div>
                ))
              ) : (
                <p className="text-slate-500 text-sm">Aucun signal de risque détecté.</p>
              )}
            </>
          )}
        </div>
      </div>
    </div>
  );
}

// ── Main Page ────────────────────────────────────────────────────────────────

export default function DealMomentumPage() {
  const [deals, setDeals]       = useState<DealData[]>([]);
  const [summary, setSummary]   = useState<Summary | null>(null);
  const [loading, setLoading]   = useState(true);
  const [error, setError]       = useState<string | null>(null);
  const [levelFilter, setLevel] = useState("all");
  const [trendFilter, setTrend] = useState("all");
  const [selected, setSelected] = useState<DealData | null>(null);

  const fetchData = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const params = new URLSearchParams();
      if (levelFilter !== "all") params.set("level", levelFilter);
      if (trendFilter !== "all") params.set("trend", trendFilter);
      const res = await fetch(`/api/deal-momentum?${params}`);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      setDeals(data.deals ?? []);
      setSummary(data.summary ?? null);
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : "Erreur inconnue");
    } finally {
      setLoading(false);
    }
  }, [levelFilter, trendFilter]);

  useEffect(() => { fetchData(); }, [fetchData]);

  const levels  = ["all", "accelerating", "positive", "neutral", "stalling", "declining", "stalled"];
  const trends  = ["all", "improving", "stable", "deteriorating", "critical"];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
      <div className="max-w-7xl mx-auto space-y-6">

        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-white">Deal Momentum Intelligence</h1>
            <p className="text-slate-400 text-sm mt-1">Suivi de la dynamique des deals en temps réel</p>
          </div>
          <button
            onClick={fetchData}
            className="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white text-sm font-medium rounded-lg transition-colors"
          >
            Actualiser
          </button>
        </div>

        {/* KPI strip */}
        {summary && (
          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
            {[
              { label: "Deals total",    value: summary.total,                    color: "text-white" },
              { label: "Score moyen",    value: summary.avg_momentum_score,       color: "text-indigo-400" },
              { label: "Vélocité moy.",  value: summary.avg_velocity_score,       color: "text-violet-400" },
              { label: "Engagement moy.",value: summary.avg_engagement_score,     color: "text-emerald-400" },
              { label: "Risque moyen",   value: summary.avg_risk_score,           color: "text-red-400" },
              { label: "Deals à risque", value: summary.at_risk_count,            color: "text-orange-400" },
            ].map(({ label, value, color }) => (
              <div key={label} className="bg-slate-900 border border-slate-800 rounded-xl p-4 text-center">
                <div className={`text-2xl font-bold ${color}`}>{value}</div>
                <div className="text-xs text-slate-500 mt-1">{label}</div>
              </div>
            ))}
          </div>
        )}

        {/* Distribution bar */}
        {summary && (
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="flex items-center justify-between mb-3">
              <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Distribution par niveau</span>
              <div className="flex gap-3 text-xs">
                {["accelerating", "positive", "neutral", "stalling", "declining", "stalled"].map((lvl) => (
                  (summary.level_counts[lvl] ?? 0) > 0 && (
                    <span key={lvl} className={`${levelColor(lvl).text}`}>
                      {levelLabel(lvl)}: {summary.level_counts[lvl]}
                    </span>
                  )
                ))}
              </div>
            </div>
            <LevelDistBar counts={summary.level_counts} total={summary.total} />
          </div>
        )}

        {/* Filters */}
        <div className="space-y-2">
          <div className="flex flex-wrap gap-2">
            {levels.map((l) => (
              <button
                key={l}
                onClick={() => setLevel(l)}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
                  levelFilter === l
                    ? "bg-indigo-600 text-white"
                    : "bg-slate-800 text-slate-400 hover:text-white"
                }`}
              >
                {l === "all" ? "Tous les niveaux" : levelLabel(l)}
              </button>
            ))}
          </div>
          <div className="flex flex-wrap gap-2">
            {trends.map((t) => (
              <button
                key={t}
                onClick={() => setTrend(t)}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
                  trendFilter === t
                    ? "bg-violet-600 text-white"
                    : "bg-slate-800 text-slate-400 hover:text-white"
                }`}
              >
                {t === "all" ? "Toutes les tendances" : trendLabel(t)}
              </button>
            ))}
          </div>
        </div>

        {/* Content */}
        {loading && (
          <div className="text-center py-20 text-slate-400">Chargement...</div>
        )}
        {error && (
          <div className="text-center py-20 text-red-400">Erreur : {error}</div>
        )}
        {!loading && !error && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
            {deals.map((deal) => (
              <DealCard key={deal.deal_id} deal={deal} onClick={() => setSelected(deal)} />
            ))}
            {deals.length === 0 && (
              <div className="col-span-2 text-center py-20 text-slate-500">
                Aucun deal trouvé pour les filtres sélectionnés.
              </div>
            )}
          </div>
        )}
      </div>

      {selected && <DealModal deal={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
