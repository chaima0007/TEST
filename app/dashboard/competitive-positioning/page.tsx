"use client";

import { useState, useEffect, useCallback } from "react";

// ── Types ─────────────────────────────────────────────────────────────────────

type Deal = {
  deal_id: string;
  account_id: string;
  account_name: string;
  deal_name: string;
  deal_value: number;
  competitor_name: string;
  positioning_score: number;
  positioning_strength: string;
  competitor_threat: string;
  win_probability: string;
  recommended_action: string;
  battlecard_points: string[];
  risk_factors: string[];
  win_rate_vs_competitor: number;
  competitive_gap: number;
  is_winnable: boolean;
  urgency_score: number;
  key_differentiators: string[];
};

type Summary = {
  total: number;
  strength_counts: Record<string, number>;
  threat_counts: Record<string, number>;
  probability_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_positioning_score: number;
  avg_win_rate: number;
  avg_urgency_score: number;
  high_threat_count: number;
  winnable_count: number;
  dominant_count: number;
  escalation_count: number;
  avg_competitive_gap: number;
};

// ── Helpers ───────────────────────────────────────────────────────────────────

const STRENGTH_LABELS: Record<string, string> = {
  dominant:    "Dominant",
  strong:      "Fort",
  competitive: "Compétitif",
  weak:        "Faible",
  critical:    "Critique",
};

const THREAT_LABELS: Record<string, string> = {
  high:       "Élevée",
  medium:     "Modérée",
  low:        "Faible",
  eliminated: "Éliminé",
  unknown:    "Inconnue",
};

const WIN_PROB_LABELS: Record<string, string> = {
  very_high: "Très élevée",
  high:      "Élevée",
  medium:    "Modérée",
  low:       "Faible",
  very_low:  "Très faible",
};

const ACTION_LABELS: Record<string, string> = {
  accelerate:            "Accélérer",
  differentiate:         "Se différencier",
  defend:                "Défendre",
  executive_escalation:  "Escalade Exec.",
  competitive_response:  "Réponse compétitive",
  abandon:               "Abandonner",
};

function strengthColor(strength: string) {
  return {
    dominant:    "bg-violet-500/20 text-violet-300 border-violet-500/30",
    strong:      "bg-emerald-500/20 text-emerald-300 border-emerald-500/30",
    competitive: "bg-blue-500/20 text-blue-300 border-blue-500/30",
    weak:        "bg-amber-500/20 text-amber-300 border-amber-500/30",
    critical:    "bg-red-500/20 text-red-300 border-red-500/30",
  }[strength] ?? "bg-slate-500/20 text-slate-300 border-slate-500/30";
}

function threatColor(threat: string) {
  return {
    high:       "text-red-400",
    medium:     "text-amber-400",
    low:        "text-emerald-400",
    eliminated: "text-slate-400",
    unknown:    "text-slate-500",
  }[threat] ?? "text-slate-400";
}

function winProbColor(prob: string) {
  return {
    very_high: "text-violet-400",
    high:      "text-emerald-400",
    medium:    "text-blue-400",
    low:       "text-amber-400",
    very_low:  "text-red-400",
  }[prob] ?? "text-slate-400";
}

function actionColor(action: string) {
  return {
    accelerate:            "text-emerald-400",
    differentiate:         "text-blue-400",
    defend:                "text-amber-400",
    executive_escalation:  "text-violet-400",
    competitive_response:  "text-orange-400",
    abandon:               "text-red-400",
  }[action] ?? "text-slate-400";
}

// ── PositioningRing ───────────────────────────────────────────────────────────

function PositioningRing({ score }: { score: number }) {
  const r = 36, cx = 44, cy = 44;
  const circ = 2 * Math.PI * r;
  const arc  = (score / 100) * circ;
  const strokeColor =
    score >= 78 ? "#a78bfa"
    : score >= 62 ? "#34d399"
    : score >= 46 ? "#60a5fa"
    : score >= 30 ? "#f59e0b"
    : "#f87171";

  return (
    <svg width="88" height="88" viewBox="0 0 88 88">
      <circle cx={cx} cy={cy} r={r} fill="none" stroke="#1e293b" strokeWidth="7" />
      <circle
        cx={cx} cy={cy} r={r}
        fill="none" stroke={strokeColor} strokeWidth="7"
        strokeLinecap="round"
        strokeDasharray={`${arc} ${circ - arc}`}
        transform={`rotate(-90 ${cx} ${cy})`}
      />
      <text x={cx} y={cy - 3} textAnchor="middle" fill="white" fontSize="13" fontWeight="bold">
        {score}
      </text>
      <text x={cx} y={cy + 11} textAnchor="middle" fill="#94a3b8" fontSize="7.5">
        Position
      </text>
    </svg>
  );
}

// ── StrengthDistBar ───────────────────────────────────────────────────────────

function StrengthDistBar({ counts, total }: { counts: Record<string, number>; total: number }) {
  const palette: Record<string, string> = {
    dominant:    "#a78bfa",
    strong:      "#34d399",
    competitive: "#60a5fa",
    weak:        "#f59e0b",
    critical:    "#f87171",
  };
  const order = ["dominant", "strong", "competitive", "weak", "critical"];
  const entries = order.filter((k) => k in counts).map((k) => [k, counts[k]] as [string, number]);

  return (
    <div className="space-y-2">
      {entries.map(([s, count]) => (
        <div key={s} className="flex items-center gap-2">
          <span className="w-24 text-xs text-slate-400 truncate">{STRENGTH_LABELS[s] ?? s}</span>
          <div className="flex-1 h-2 bg-slate-800 rounded-full overflow-hidden">
            <div
              className="h-full rounded-full transition-all"
              style={{
                width: total ? `${(count / total) * 100}%` : "0%",
                backgroundColor: palette[s] ?? "#64748b",
              }}
            />
          </div>
          <span className="w-5 text-xs text-slate-400 text-right">{count}</span>
        </div>
      ))}
    </div>
  );
}

// ── DealCard ──────────────────────────────────────────────────────────────────

function DealCard({ deal, onClick }: { deal: Deal; onClick: () => void }) {
  return (
    <div
      onClick={onClick}
      className="bg-slate-800/60 border border-slate-700/50 rounded-xl p-4 cursor-pointer hover:border-indigo-500/50 hover:bg-slate-800 transition-all"
    >
      <div className="flex items-start gap-3 mb-3">
        <PositioningRing score={deal.positioning_score} />
        <div className="flex-1 min-w-0">
          <p className="text-sm font-semibold text-white truncate">{deal.deal_name}</p>
          <p className="text-xs text-slate-400 truncate">{deal.account_name}</p>
          <p className="text-xs text-slate-500 truncate">vs {deal.competitor_name}</p>
          <div className="flex flex-wrap gap-1 mt-1.5">
            <span className={`text-[10px] px-2 py-0.5 rounded-full border ${strengthColor(deal.positioning_strength)}`}>
              {STRENGTH_LABELS[deal.positioning_strength] ?? deal.positioning_strength}
            </span>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-2 mb-3 text-center">
        <div className="bg-slate-900/50 rounded-lg p-2">
          <p className="text-[10px] text-slate-400 mb-0.5">Taux de victoire</p>
          <p className="text-sm font-bold text-blue-400">{(deal.win_rate_vs_competitor * 100).toFixed(0)}%</p>
        </div>
        <div className="bg-slate-900/50 rounded-lg p-2">
          <p className="text-[10px] text-slate-400 mb-0.5">Urgence</p>
          <p className="text-sm font-bold text-amber-400">{deal.urgency_score}</p>
        </div>
      </div>

      <div className="flex items-center justify-between text-xs">
        <span className={`font-medium ${threatColor(deal.competitor_threat)}`}>
          Menace: {THREAT_LABELS[deal.competitor_threat] ?? deal.competitor_threat}
        </span>
        <span className={`font-medium ${winProbColor(deal.win_probability)}`}>
          {WIN_PROB_LABELS[deal.win_probability] ?? deal.win_probability}
        </span>
      </div>

      <div className="mt-2 text-xs">
        <span className={`font-medium ${actionColor(deal.recommended_action)}`}>
          → {ACTION_LABELS[deal.recommended_action] ?? deal.recommended_action}
        </span>
      </div>

      {!deal.is_winnable && (
        <div className="mt-2 text-[10px] text-red-400 bg-red-900/20 rounded px-2 py-1">
          ✗ Deal difficile à gagner
        </div>
      )}
    </div>
  );
}

// ── DealModal ─────────────────────────────────────────────────────────────────

function DealModal({ deal, onClose }: { deal: Deal; onClose: () => void }) {
  const [tab, setTab] = useState<"action" | "battlecard" | "risks">("action");

  useEffect(() => {
    const h = (e: KeyboardEvent) => e.key === "Escape" && onClose();
    window.addEventListener("keydown", h);
    return () => window.removeEventListener("keydown", h);
  }, [onClose]);

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70"
      onClick={onClose}
    >
      <div
        className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-lg max-h-[90vh] overflow-y-auto"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="p-5 border-b border-slate-800">
          <div className="flex items-start justify-between gap-3">
            <div className="flex items-center gap-3">
              <PositioningRing score={deal.positioning_score} />
              <div>
                <p className="text-lg font-bold text-white">{deal.deal_name}</p>
                <p className="text-sm text-slate-400">{deal.account_name}</p>
                <p className="text-xs text-slate-500">vs {deal.competitor_name}</p>
              </div>
            </div>
            <button onClick={onClose} className="text-slate-500 hover:text-white text-xl">×</button>
          </div>
          <div className="flex flex-wrap gap-2 mt-3">
            <span className={`text-xs px-2 py-0.5 rounded-full border ${strengthColor(deal.positioning_strength)}`}>
              {STRENGTH_LABELS[deal.positioning_strength] ?? deal.positioning_strength}
            </span>
            <span className={`text-xs font-medium ${threatColor(deal.competitor_threat)}`}>
              Menace {THREAT_LABELS[deal.competitor_threat] ?? deal.competitor_threat}
            </span>
            <span className={`text-xs font-medium ${winProbColor(deal.win_probability)}`}>
              Proba. {WIN_PROB_LABELS[deal.win_probability] ?? deal.win_probability}
            </span>
          </div>
        </div>

        {/* Metrics */}
        <div className="grid grid-cols-2 gap-3 p-5 border-b border-slate-800">
          <div className="bg-slate-800/60 rounded-lg p-3">
            <p className="text-xs text-slate-400 mb-1">Score position.</p>
            <p className="text-xl font-bold text-violet-400">{deal.positioning_score}</p>
          </div>
          <div className="bg-slate-800/60 rounded-lg p-3">
            <p className="text-xs text-slate-400 mb-1">Gap compétitif</p>
            <p className={`text-xl font-bold ${deal.competitive_gap >= 0 ? "text-emerald-400" : "text-red-400"}`}>
              {deal.competitive_gap > 0 ? "+" : ""}{deal.competitive_gap}
            </p>
          </div>
          <div className="bg-slate-800/60 rounded-lg p-3">
            <p className="text-xs text-slate-400 mb-1">Win rate hist.</p>
            <p className="text-xl font-bold text-blue-400">{(deal.win_rate_vs_competitor * 100).toFixed(0)}%</p>
          </div>
          <div className="bg-slate-800/60 rounded-lg p-3">
            <p className="text-xs text-slate-400 mb-1">Urgence</p>
            <p className="text-xl font-bold text-amber-400">{deal.urgency_score}</p>
          </div>
        </div>

        {/* Tabs */}
        <div className="flex border-b border-slate-800">
          {(["action", "battlecard", "risks"] as const).map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`flex-1 py-2.5 text-xs font-medium transition-colors ${
                tab === t
                  ? "text-indigo-400 border-b-2 border-indigo-400"
                  : "text-slate-500 hover:text-slate-300"
              }`}
            >
              {t === "action" ? "Action" : t === "battlecard" ? "Battlecard" : "Risques"}
            </button>
          ))}
        </div>

        <div className="p-5">
          {tab === "action" && (
            <div className="space-y-4">
              <div>
                <p className="text-xs text-slate-500 uppercase tracking-wider mb-2">Action recommandée</p>
                <p className={`text-sm font-bold ${actionColor(deal.recommended_action)}`}>
                  {ACTION_LABELS[deal.recommended_action] ?? deal.recommended_action}
                </p>
              </div>
              {deal.key_differentiators.length > 0 && (
                <div>
                  <p className="text-xs text-slate-500 uppercase tracking-wider mb-2">Différenciateurs clés</p>
                  <ul className="space-y-1">
                    {deal.key_differentiators.map((d, i) => (
                      <li key={i} className="flex items-start gap-2 text-sm text-slate-300">
                        <span className="text-emerald-400 mt-0.5">✓</span>
                        <span>{d}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          )}
          {tab === "battlecard" && (
            <div>
              {deal.battlecard_points.length === 0 ? (
                <p className="text-sm text-slate-500 italic">Aucun point battlecard disponible.</p>
              ) : (
                <ul className="space-y-2">
                  {deal.battlecard_points.map((pt, i) => (
                    <li key={i} className="flex items-start gap-2 text-sm text-slate-300 bg-slate-800/50 rounded-lg p-2">
                      <span className="text-blue-400 mt-0.5 font-bold text-xs">#{i + 1}</span>
                      <span>{pt}</span>
                    </li>
                  ))}
                </ul>
              )}
            </div>
          )}
          {tab === "risks" && (
            <div>
              {deal.risk_factors.length === 0 ? (
                <p className="text-sm text-slate-500 italic">Aucun risque compétitif identifié.</p>
              ) : (
                <ul className="space-y-2">
                  {deal.risk_factors.map((r, i) => (
                    <li key={i} className="flex items-start gap-2 text-sm text-slate-300">
                      <span className="text-red-400 mt-0.5">!</span>
                      <span>{r}</span>
                    </li>
                  ))}
                </ul>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

// ── Page ──────────────────────────────────────────────────────────────────────

export default function CompetitivePositioningPage() {
  const [data, setData]                     = useState<{ deals: Deal[]; summary: Summary } | null>(null);
  const [loading, setLoading]               = useState(true);
  const [error, setError]                   = useState<string | null>(null);
  const [strengthFilter, setStrengthFilter] = useState<string>("all");
  const [threatFilter, setThreatFilter]     = useState<string>("all");
  const [selected, setSelected]             = useState<Deal | null>(null);

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const params = new URLSearchParams();
      if (strengthFilter !== "all") params.set("strength", strengthFilter);
      if (threatFilter   !== "all") params.set("threat", threatFilter);
      const res = await fetch(`/api/competitive-positioning?${params}`);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      setData(await res.json());
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : "Erreur inconnue");
    } finally {
      setLoading(false);
    }
  }, [strengthFilter, threatFilter]);

  useEffect(() => { load(); }, [load]);

  const s = data?.summary;

  const kpis = s
    ? [
        { label: "Total Deals",        value: s.total,                color: "text-blue-400" },
        { label: "Positions Dominantes", value: s.dominant_count,      color: "text-violet-400" },
        { label: "Gagnable",           value: s.winnable_count,        color: "text-emerald-400" },
        { label: "Menaces Élevées",    value: s.high_threat_count,     color: "text-red-400" },
        { label: "Escalades",          value: s.escalation_count,      color: "text-orange-400" },
        { label: "Score Position Moy.", value: s.avg_positioning_score, color: "text-blue-400" },
      ]
    : [];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-white">Competitive Positioning Intelligence</h1>
        <p className="text-slate-400 text-sm mt-1">
          Analyse des positions compétitives par deal — battlecards, risques et probabilités de victoire
        </p>
      </div>

      {error && (
        <div className="mb-4 p-3 bg-red-900/30 border border-red-700 rounded-lg text-red-300 text-sm">
          {error}
        </div>
      )}

      {/* KPI Strip */}
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3 mb-6">
        {kpis.map((k) => (
          <div key={k.label} className="bg-slate-800/60 border border-slate-700/50 rounded-xl p-4">
            <p className="text-xs text-slate-400 mb-1">{k.label}</p>
            <p className={`text-2xl font-bold ${k.color}`}>{k.value}</p>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
        {/* Rates */}
        <div className="bg-slate-800/60 border border-slate-700/50 rounded-xl p-5">
          <p className="text-sm font-semibold text-white mb-4">Métriques Moyennes</p>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <p className="text-xs text-slate-400 mb-1">Win rate moy.</p>
              <p className="text-2xl font-bold text-emerald-400">
                {s ? `${(s.avg_win_rate * 100).toFixed(0)}%` : "—"}
              </p>
            </div>
            <div>
              <p className="text-xs text-slate-400 mb-1">Urgence moy.</p>
              <p className="text-2xl font-bold text-amber-400">{s?.avg_urgency_score ?? "—"}</p>
            </div>
          </div>
        </div>

        {/* Strength distribution */}
        <div className="lg:col-span-2 bg-slate-800/60 border border-slate-700/50 rounded-xl p-5">
          <p className="text-sm font-semibold text-white mb-4">Distribution des Forces</p>
          {s ? (
            <StrengthDistBar counts={s.strength_counts} total={s.total} />
          ) : (
            <div className="h-24 bg-slate-700/30 rounded animate-pulse" />
          )}
        </div>
      </div>

      {/* Filters */}
      <div className="flex flex-wrap gap-3 mb-5">
        <div className="flex flex-wrap gap-1">
          {["all", "dominant", "strong", "competitive", "weak", "critical"].map((v) => (
            <button
              key={v}
              onClick={() => setStrengthFilter(v)}
              className={`px-3 py-1 rounded-full text-xs font-medium transition-colors ${
                strengthFilter === v
                  ? "bg-indigo-600 text-white"
                  : "bg-slate-800 text-slate-400 hover:bg-slate-700"
              }`}
            >
              {v === "all" ? "Toutes forces" : (STRENGTH_LABELS[v] ?? v)}
            </button>
          ))}
        </div>
        <div className="flex flex-wrap gap-1">
          {["all", "high", "medium", "low", "unknown"].map((v) => (
            <button
              key={v}
              onClick={() => setThreatFilter(v)}
              className={`px-3 py-1 rounded-full text-xs font-medium transition-colors ${
                threatFilter === v
                  ? "bg-red-600 text-white"
                  : "bg-slate-800 text-slate-400 hover:bg-slate-700"
              }`}
            >
              {v === "all" ? "Toutes menaces" : (THREAT_LABELS[v] ?? v)}
            </button>
          ))}
        </div>
      </div>

      {/* Cards */}
      {loading ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          {Array.from({ length: 8 }).map((_, i) => (
            <div key={i} className="h-52 bg-slate-800/40 rounded-xl animate-pulse" />
          ))}
        </div>
      ) : (
        <>
          <p className="text-xs text-slate-500 mb-3">{data?.deals.length ?? 0} deal(s) affiché(s)</p>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {(data?.deals ?? []).map((deal) => (
              <DealCard key={deal.deal_id} deal={deal} onClick={() => setSelected(deal)} />
            ))}
          </div>
        </>
      )}

      {selected && <DealModal deal={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
