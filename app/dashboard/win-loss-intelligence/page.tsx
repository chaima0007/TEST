"use client";

import { useEffect, useState, useCallback } from "react";

// ─── Types ──────────────────────────────────────────────────────────────────

interface WinLossDeal {
  deal_id: string;
  deal_name: string;
  account_name: string;
  segment: string;
  arr_eur: number;
  outcome: "won" | "lost" | "no_decision";
  execution_quality: "excellent" | "good" | "fair" | "poor";
  wl_action: "replicate" | "debrief" | "investigate" | "coach";
  execution_score: number;
  cycle_efficiency_pct: number;
  discount_pressure: "none" | "low" | "medium" | "high";
  win_patterns: string[];
  loss_factors: string[];
  process_gaps: string[];
  coaching_insights: string[];
}

interface Summary {
  total: number;
  outcome_counts: Record<string, number>;
  quality_counts: Record<string, number>;
  action_counts: Record<string, number>;
  win_rate: number;
  avg_execution_score: number;
  total_won_arr_eur: number;
  total_lost_arr_eur: number;
  coaching_needed_count: number;
  replicate_count: number;
}

interface ApiResponse {
  deals: WinLossDeal[];
  summary: Summary;
}

// ─── Helpers ────────────────────────────────────────────────────────────────

function fmtEur(n: number) {
  if (n >= 1_000_000) return `€${(n / 1_000_000).toFixed(1)}M`;
  if (n >= 1_000) return `€${Math.round(n / 1_000)}k`;
  return `€${n}`;
}

function outcomeColor(outcome: string) {
  if (outcome === "won") return "text-emerald-400";
  if (outcome === "lost") return "text-red-400";
  return "text-amber-400";
}

function outcomeBg(outcome: string) {
  if (outcome === "won") return "bg-emerald-500/15 text-emerald-300 border border-emerald-500/30";
  if (outcome === "lost") return "bg-red-500/15 text-red-300 border border-red-500/30";
  return "bg-amber-500/15 text-amber-300 border border-amber-500/30";
}

function qualityColor(q: string) {
  if (q === "excellent") return "text-emerald-400";
  if (q === "good") return "text-sky-400";
  if (q === "fair") return "text-amber-400";
  return "text-red-400";
}

function qualityBg(q: string) {
  if (q === "excellent") return "bg-emerald-500/15 text-emerald-300 border border-emerald-500/30";
  if (q === "good") return "bg-sky-500/15 text-sky-300 border border-sky-500/30";
  if (q === "fair") return "bg-amber-500/15 text-amber-300 border border-amber-500/30";
  return "bg-red-500/15 text-red-300 border border-red-500/30";
}

function actionBg(a: string) {
  if (a === "replicate") return "bg-emerald-500/20 text-emerald-200";
  if (a === "debrief") return "bg-sky-500/20 text-sky-200";
  if (a === "investigate") return "bg-amber-500/20 text-amber-200";
  return "bg-red-500/20 text-red-200";
}

function outcomeLabel(o: string) {
  if (o === "won") return "Gagné";
  if (o === "lost") return "Perdu";
  return "Sans décision";
}

function qualityLabel(q: string) {
  if (q === "excellent") return "Excellent";
  if (q === "good") return "Bon";
  if (q === "fair") return "Passable";
  return "Faible";
}

function actionLabel(a: string) {
  if (a === "replicate") return "Répliquer";
  if (a === "debrief") return "Débrief";
  if (a === "investigate") return "Investiguer";
  return "Coaching";
}

function discountBadge(p: string) {
  if (p === "none") return "bg-emerald-500/20 text-emerald-300";
  if (p === "low") return "bg-sky-500/20 text-sky-300";
  if (p === "medium") return "bg-amber-500/20 text-amber-300";
  return "bg-red-500/20 text-red-300";
}

function discountLabel(p: string) {
  if (p === "none") return "Sans remise";
  if (p === "low") return "Remise faible";
  if (p === "medium") return "Remise moyenne";
  return "Forte remise";
}

// ─── SVG Ring Gauge ──────────────────────────────────────────────────────────

function ExecutionRing({ score, outcome }: { score: number; outcome: string }) {
  const r = 36;
  const circ = 2 * Math.PI * r;
  const arc = (score / 100) * circ;

  let stroke = "#10b981"; // emerald — won
  if (outcome === "lost") stroke = "#ef4444"; // red
  else if (outcome === "no_decision") stroke = "#f59e0b"; // amber

  return (
    <svg viewBox="0 0 80 80" className="w-20 h-20" aria-hidden="true">
      <circle cx="40" cy="40" r={r} fill="none" stroke="#1e293b" strokeWidth="7" />
      <circle
        cx="40"
        cy="40"
        r={r}
        fill="none"
        stroke={stroke}
        strokeWidth="7"
        strokeDasharray={`${arc} ${circ - arc}`}
        strokeLinecap="round"
        transform="rotate(-90 40 40)"
      />
      <text x="40" y="44" textAnchor="middle" fontSize="15" fontWeight="700" fill="#f1f5f9">
        {score}
      </text>
    </svg>
  );
}

// ─── ScoreBar ────────────────────────────────────────────────────────────────

function ScoreBar({ label, value, color }: { label: string; value: number; color: string }) {
  return (
    <div>
      <div className="flex justify-between text-xs mb-1">
        <span className="text-slate-400">{label}</span>
        <span className="text-slate-200 font-medium">{value}</span>
      </div>
      <div className="h-1.5 bg-slate-700 rounded-full overflow-hidden">
        <div className={`h-full rounded-full ${color}`} style={{ width: `${Math.min(100, Math.max(0, value))}%` }} />
      </div>
    </div>
  );
}

// ─── Detail Modal ────────────────────────────────────────────────────────────

function WinLossModal({ deal, onClose }: { deal: WinLossDeal; onClose: () => void }) {
  useEffect(() => {
    function onKey(e: KeyboardEvent) { if (e.key === "Escape") onClose(); }
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [onClose]);

  const effSign = deal.cycle_efficiency_pct > 0 ? "+" : "";
  const effColor = deal.cycle_efficiency_pct > 0 ? "text-emerald-400" : deal.cycle_efficiency_pct < 0 ? "text-red-400" : "text-slate-400";

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4"
      onClick={onClose}
    >
      <div
        className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-2xl max-h-[90vh] overflow-y-auto shadow-2xl"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="p-6 border-b border-slate-800 flex items-start justify-between gap-4">
          <div>
            <h2 className="text-lg font-bold text-slate-100">{deal.deal_name}</h2>
            <p className="text-slate-400 text-sm mt-0.5">{deal.account_name} · {deal.segment.toUpperCase()}</p>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-slate-300 transition-colors text-xl leading-none mt-0.5">✕</button>
        </div>

        <div className="p-6 space-y-6">
          {/* Summary row */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
            <div className="bg-slate-800/60 rounded-xl p-3 text-center">
              <div className="text-xs text-slate-500 mb-1">Résultat</div>
              <span className={`text-xs font-semibold px-2 py-0.5 rounded-full ${outcomeBg(deal.outcome)}`}>
                {outcomeLabel(deal.outcome)}
              </span>
            </div>
            <div className="bg-slate-800/60 rounded-xl p-3 text-center">
              <div className="text-xs text-slate-500 mb-1">ARR</div>
              <div className="text-base font-bold text-slate-100">{fmtEur(deal.arr_eur)}</div>
            </div>
            <div className="bg-slate-800/60 rounded-xl p-3 text-center">
              <div className="text-xs text-slate-500 mb-1">Efficacité cycle</div>
              <div className={`text-base font-bold ${effColor}`}>{effSign}{deal.cycle_efficiency_pct.toFixed(0)}%</div>
            </div>
            <div className="bg-slate-800/60 rounded-xl p-3 text-center">
              <div className="text-xs text-slate-500 mb-1">Remise</div>
              <span className={`text-xs font-semibold px-2 py-0.5 rounded-full ${discountBadge(deal.discount_pressure)}`}>
                {discountLabel(deal.discount_pressure)}
              </span>
            </div>
          </div>

          {/* Execution score bar */}
          <div>
            <div className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-3">Score d'exécution</div>
            <ScoreBar
              label={`Qualité : ${qualityLabel(deal.execution_quality)}`}
              value={deal.execution_score}
              color={
                deal.execution_quality === "excellent" ? "bg-emerald-500" :
                deal.execution_quality === "good" ? "bg-sky-500" :
                deal.execution_quality === "fair" ? "bg-amber-500" : "bg-red-500"
              }
            />
          </div>

          {/* Win patterns */}
          {deal.win_patterns.length > 0 && (
            <div>
              <div className="text-xs font-semibold text-emerald-400 uppercase tracking-wider mb-3">Patterns gagnants</div>
              <ul className="space-y-2">
                {deal.win_patterns.map((p, i) => (
                  <li key={i} className="flex items-start gap-2 text-sm text-slate-300">
                    <span className="text-emerald-400 mt-0.5 shrink-0">✓</span>
                    <span>{p}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Loss factors */}
          {deal.loss_factors.length > 0 && (
            <div>
              <div className="text-xs font-semibold text-red-400 uppercase tracking-wider mb-3">Facteurs de perte</div>
              <ul className="space-y-2">
                {deal.loss_factors.map((f, i) => (
                  <li key={i} className="flex items-start gap-2 text-sm text-slate-300">
                    <span className="text-red-400 mt-0.5 shrink-0">✗</span>
                    <span>{f}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Process gaps */}
          {deal.process_gaps.length > 0 && (
            <div>
              <div className="text-xs font-semibold text-amber-400 uppercase tracking-wider mb-3">Lacunes process</div>
              <ul className="space-y-2">
                {deal.process_gaps.map((g, i) => (
                  <li key={i} className="flex items-start gap-2 text-sm text-slate-300">
                    <span className="text-amber-400 mt-0.5 shrink-0">⚠</span>
                    <span>{g}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Coaching insights */}
          {deal.coaching_insights.length > 0 && (
            <div>
              <div className="text-xs font-semibold text-indigo-400 uppercase tracking-wider mb-3">Insights coaching</div>
              <ul className="space-y-2">
                {deal.coaching_insights.map((c, i) => (
                  <li key={i} className="flex items-start gap-2 text-sm text-slate-300">
                    <span className="text-indigo-400 mt-0.5 shrink-0">→</span>
                    <span>{c}</span>
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

// ─── Deal Card ───────────────────────────────────────────────────────────────

function WinLossCard({ deal, onClick }: { deal: WinLossDeal; onClick: () => void }) {
  const effSign = deal.cycle_efficiency_pct > 0 ? "+" : "";
  const effColor = deal.cycle_efficiency_pct > 0 ? "text-emerald-400" : deal.cycle_efficiency_pct < 0 ? "text-red-400" : "text-slate-400";

  return (
    <button
      onClick={onClick}
      className="w-full text-left bg-slate-800/50 hover:bg-slate-800 border border-slate-700/50 hover:border-slate-600 rounded-2xl p-5 transition-all duration-200 group"
    >
      <div className="flex items-start gap-4">
        <ExecutionRing score={deal.execution_score} outcome={deal.outcome} />
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 flex-wrap mb-1">
            <span className={`text-[10px] font-semibold px-2 py-0.5 rounded-full ${outcomeBg(deal.outcome)}`}>
              {outcomeLabel(deal.outcome)}
            </span>
            <span className={`text-[10px] font-semibold px-2 py-0.5 rounded-full ${qualityBg(deal.execution_quality)}`}>
              {qualityLabel(deal.execution_quality)}
            </span>
            <span className={`text-[10px] font-semibold px-2 py-0.5 rounded-full ${actionBg(deal.wl_action)}`}>
              {actionLabel(deal.wl_action)}
            </span>
          </div>
          <h3 className="text-sm font-semibold text-slate-100 truncate group-hover:text-indigo-300 transition-colors">
            {deal.deal_name}
          </h3>
          <p className="text-xs text-slate-500 mt-0.5">{deal.account_name}</p>
        </div>
      </div>

      <div className="mt-4 grid grid-cols-3 gap-3 text-center">
        <div>
          <div className="text-xs text-slate-500 mb-0.5">ARR</div>
          <div className="text-sm font-bold text-slate-200">{fmtEur(deal.arr_eur)}</div>
        </div>
        <div>
          <div className="text-xs text-slate-500 mb-0.5">Cycle</div>
          <div className={`text-sm font-bold ${effColor}`}>{effSign}{deal.cycle_efficiency_pct.toFixed(0)}%</div>
        </div>
        <div>
          <div className="text-xs text-slate-500 mb-0.5">Lacunes</div>
          <div className="text-sm font-bold text-slate-200">{deal.process_gaps.length}</div>
        </div>
      </div>

      {/* Mini score bar */}
      <div className="mt-3">
        <div className="h-1 bg-slate-700 rounded-full overflow-hidden">
          <div
            className={`h-full rounded-full ${
              deal.execution_quality === "excellent" ? "bg-emerald-500" :
              deal.execution_quality === "good" ? "bg-sky-500" :
              deal.execution_quality === "fair" ? "bg-amber-500" : "bg-red-500"
            }`}
            style={{ width: `${deal.execution_score}%` }}
          />
        </div>
      </div>
    </button>
  );
}

// ─── Distribution Bar ─────────────────────────────────────────────────────────

function OutcomeBar({ summary }: { summary: Summary }) {
  const n = summary.total || 1;
  const won = summary.outcome_counts["won"] || 0;
  const lost = summary.outcome_counts["lost"] || 0;
  const nd = summary.outcome_counts["no_decision"] || 0;
  return (
    <div className="flex h-2 rounded-full overflow-hidden gap-px bg-slate-800">
      {won > 0 && <div className="bg-emerald-500 h-full transition-all" style={{ width: `${(won / n) * 100}%` }} />}
      {lost > 0 && <div className="bg-red-500 h-full transition-all" style={{ width: `${(lost / n) * 100}%` }} />}
      {nd > 0 && <div className="bg-amber-500 h-full transition-all" style={{ width: `${(nd / n) * 100}%` }} />}
    </div>
  );
}

// ─── Page ────────────────────────────────────────────────────────────────────

type OutcomeFilter = "all" | "won" | "lost" | "no_decision";
type QualityFilter = "all" | "excellent" | "good" | "fair" | "poor";

const OUTCOME_TABS: { id: OutcomeFilter; label: string }[] = [
  { id: "all", label: "Tous" },
  { id: "won", label: "Gagnés" },
  { id: "lost", label: "Perdus" },
  { id: "no_decision", label: "Sans décision" },
];

const QUALITY_TABS: { id: QualityFilter; label: string }[] = [
  { id: "all", label: "Toutes qualités" },
  { id: "excellent", label: "Excellent" },
  { id: "good", label: "Bon" },
  { id: "fair", label: "Passable" },
  { id: "poor", label: "Faible" },
];

export default function WinLossIntelligencePage() {
  const [data, setData] = useState<ApiResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [outcomeFilter, setOutcomeFilter] = useState<OutcomeFilter>("all");
  const [qualityFilter, setQualityFilter] = useState<QualityFilter>("all");
  const [selected, setSelected] = useState<WinLossDeal | null>(null);

  const fetchData = useCallback(async (outcome: OutcomeFilter, quality: QualityFilter) => {
    setLoading(true);
    try {
      const params = new URLSearchParams();
      if (outcome !== "all") params.set("outcome", outcome);
      if (quality !== "all") params.set("quality", quality);
      const res = await fetch(`/api/win-loss-intelligence${params.size ? `?${params}` : ""}`);
      if (res.ok) setData(await res.json());
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { fetchData(outcomeFilter, qualityFilter); }, [outcomeFilter, qualityFilter, fetchData]);

  const summary = data?.summary;

  return (
    <main className="min-h-screen bg-slate-950 text-slate-100 p-6 lg:p-8">
      {selected && <WinLossModal deal={selected} onClose={() => setSelected(null)} />}

      {/* Header */}
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-slate-100">Analyse Win/Loss</h1>
        <p className="text-slate-400 mt-1 text-sm">Patterns d'exécution et opportunités de coaching sur les deals clôturés</p>
      </div>

      {/* KPI Strip */}
      {summary && (
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3 mb-6">
          <div className="bg-slate-800/50 border border-slate-700/50 rounded-xl p-4 text-center">
            <div className="text-xs text-slate-500 mb-1">Taux de victoire</div>
            <div className="text-2xl font-bold text-emerald-400">{summary.win_rate}%</div>
          </div>
          <div className="bg-slate-800/50 border border-slate-700/50 rounded-xl p-4 text-center">
            <div className="text-xs text-slate-500 mb-1">Score exécution</div>
            <div className="text-2xl font-bold text-sky-400">{summary.avg_execution_score}</div>
          </div>
          <div className="bg-slate-800/50 border border-slate-700/50 rounded-xl p-4 text-center">
            <div className="text-xs text-slate-500 mb-1">ARR gagné</div>
            <div className="text-2xl font-bold text-emerald-400">{fmtEur(summary.total_won_arr_eur)}</div>
          </div>
          <div className="bg-slate-800/50 border border-slate-700/50 rounded-xl p-4 text-center">
            <div className="text-xs text-slate-500 mb-1">ARR perdu</div>
            <div className="text-2xl font-bold text-red-400">{fmtEur(summary.total_lost_arr_eur)}</div>
          </div>
          <div className="bg-slate-800/50 border border-slate-700/50 rounded-xl p-4 text-center">
            <div className="text-xs text-slate-500 mb-1">Coaching requis</div>
            <div className="text-2xl font-bold text-amber-400">{summary.coaching_needed_count}</div>
          </div>
          <div className="bg-slate-800/50 border border-slate-700/50 rounded-xl p-4 text-center">
            <div className="text-xs text-slate-500 mb-1">À répliquer</div>
            <div className="text-2xl font-bold text-indigo-400">{summary.replicate_count}</div>
          </div>
        </div>
      )}

      {/* Outcome distribution bar */}
      {summary && (
        <div className="mb-6 bg-slate-800/30 border border-slate-700/50 rounded-xl p-4">
          <div className="flex justify-between text-xs text-slate-400 mb-2">
            <span>Distribution des résultats</span>
            <span>{summary.total} deals analysés</span>
          </div>
          <OutcomeBar summary={summary} />
          <div className="flex gap-4 mt-2 text-xs">
            <span className="flex items-center gap-1.5 text-emerald-400">
              <span className="w-2 h-2 rounded-full bg-emerald-500 inline-block" />
              Gagnés {summary.outcome_counts["won"] || 0}
            </span>
            <span className="flex items-center gap-1.5 text-red-400">
              <span className="w-2 h-2 rounded-full bg-red-500 inline-block" />
              Perdus {summary.outcome_counts["lost"] || 0}
            </span>
            <span className="flex items-center gap-1.5 text-amber-400">
              <span className="w-2 h-2 rounded-full bg-amber-500 inline-block" />
              Sans décision {summary.outcome_counts["no_decision"] || 0}
            </span>
          </div>
        </div>
      )}

      {/* Outcome filter tabs */}
      <div className="flex gap-2 flex-wrap mb-3">
        {OUTCOME_TABS.map((t) => (
          <button
            key={t.id}
            onClick={() => setOutcomeFilter(t.id)}
            className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-colors ${
              outcomeFilter === t.id
                ? "bg-indigo-600 text-white"
                : "bg-slate-800 text-slate-400 hover:text-slate-200"
            }`}
          >
            {t.label}
            {summary && t.id !== "all" && (
              <span className="ml-1.5 text-xs opacity-70">{summary.outcome_counts[t.id] || 0}</span>
            )}
          </button>
        ))}
      </div>

      {/* Quality filter tabs */}
      <div className="flex gap-2 flex-wrap mb-6">
        {QUALITY_TABS.map((t) => (
          <button
            key={t.id}
            onClick={() => setQualityFilter(t.id)}
            className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-colors ${
              qualityFilter === t.id
                ? "bg-slate-600 text-white"
                : "bg-slate-800/50 text-slate-500 hover:text-slate-300"
            }`}
          >
            {t.label}
            {summary && t.id !== "all" && (
              <span className="ml-1.5 text-xs opacity-70">{summary.quality_counts[t.id] || 0}</span>
            )}
          </button>
        ))}
      </div>

      {/* Deal Grid */}
      {loading ? (
        <div className="flex items-center justify-center h-48 text-slate-500">Chargement…</div>
      ) : !data?.deals.length ? (
        <div className="flex items-center justify-center h-48 text-slate-500">Aucun deal pour ce filtre.</div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-4">
          {data.deals.map((deal) => (
            <WinLossCard key={deal.deal_id} deal={deal} onClick={() => setSelected(deal)} />
          ))}
        </div>
      )}
    </main>
  );
}
