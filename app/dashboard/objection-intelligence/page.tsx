"use client";

import { useState, useEffect, useRef } from "react";

// ─── Types ───────────────────────────────────────────────────────────────────

type ObjectionBurden = "clear" | "moderate" | "heavy" | "critical";
type ObjectionAction = "advance" | "address" | "escalate" | "reassess";

interface Deal {
  deal_id: string;
  deal_name: string;
  account_name: string;
  arr_eur: number;
  stage: string;
  objection_burden: ObjectionBurden;
  objection_action: ObjectionAction;
  burden_score: number;
  total_active_objections: number;
  resolution_score: number;
  primary_objection_type: string;
  deal_impact_eur: number;
  risk_factors: string[];
  mitigating_factors: string[];
  recommended_tactics: string[];
}

interface Summary {
  total: number;
  burden_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_burden_score: number;
  avg_resolution_score: number;
  total_arr_impacted_eur: number;
  total_arr_at_risk_eur: number;
  critical_count: number;
  escalation_count: number;
  advance_ready_count: number;
}

// ─── Helpers ─────────────────────────────────────────────────────────────────

const BURDEN_META: Record<ObjectionBurden, { label: string; color: string; bg: string; ring: string }> = {
  clear:    { label: "Libre",    color: "text-emerald-400", bg: "bg-emerald-400", ring: "#34d399" },
  moderate: { label: "Modéré",  color: "text-blue-400",    bg: "bg-blue-400",    ring: "#60a5fa" },
  heavy:    { label: "Lourd",   color: "text-amber-400",   bg: "bg-amber-400",   ring: "#fbbf24" },
  critical: { label: "Critique", color: "text-red-400",    bg: "bg-red-400",     ring: "#f87171" },
};

const ACTION_META: Record<ObjectionAction, { label: string; color: string; bg: string }> = {
  advance:  { label: "Avancer",          color: "text-emerald-300", bg: "bg-emerald-900/40" },
  address:  { label: "Traiter objections", color: "text-blue-300",  bg: "bg-blue-900/40" },
  escalate: { label: "Escalader",         color: "text-amber-300",  bg: "bg-amber-900/40" },
  reassess: { label: "Réévaluer",         color: "text-red-300",    bg: "bg-red-900/40" },
};

const OBJECTION_TYPE_LABELS: Record<string, string> = {
  price: "Prix",
  competitor: "Concurrent",
  authority: "Autorité",
  trust: "Confiance",
  timing: "Timing",
  implementation: "Implémentation",
  none: "Aucune",
};

const STAGE_LABELS: Record<string, string> = {
  qualification: "Qualification",
  demo: "Démo",
  proposal: "Proposition",
  negotiation: "Négociation",
  closing: "Closing",
};

function fmt(n: number) {
  if (n >= 1_000_000) return `${(n / 1_000_000).toFixed(1)}M`;
  if (n >= 1_000) return `${(n / 1_000).toFixed(0)}k`;
  return `${n.toFixed(0)}`;
}
function fmtEur(n: number) { return `€${fmt(n)}`; }

// ─── ObjectionRing ────────────────────────────────────────────────────────────

function ObjectionRing({ score, burden }: { score: number; burden: ObjectionBurden }) {
  const r = 28;
  const circ = 2 * Math.PI * r;
  const arc = (score / 100) * circ;
  const color = BURDEN_META[burden].ring;
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
        {score.toFixed(1)}
      </text>
    </svg>
  );
}

// ─── ResolutionBar ────────────────────────────────────────────────────────────

function ResolutionBar({ value }: { value: number }) {
  const color = value >= 70 ? "bg-emerald-500" : value >= 40 ? "bg-blue-500" : value >= 20 ? "bg-amber-500" : "bg-red-500";
  return (
    <div className="space-y-0.5">
      <div className="flex justify-between text-[10px] text-slate-400">
        <span>Résolution</span>
        <span>{value.toFixed(0)}%</span>
      </div>
      <div className="h-1 bg-slate-800 rounded-full overflow-hidden">
        <div className={`h-full rounded-full ${color}`} style={{ width: `${Math.min(100, value)}%` }} />
      </div>
    </div>
  );
}

// ─── ScoreBar (modal) ─────────────────────────────────────────────────────────

function ScoreBar({ value, label, color, invert = false }: { value: number; label: string; color: string; invert?: boolean }) {
  const displayVal = invert ? 100 - value : value;
  const barColor = invert
    ? (value <= 20 ? "bg-emerald-500" : value <= 45 ? "bg-blue-500" : value <= 70 ? "bg-amber-500" : "bg-red-500")
    : color.replace("text-", "bg-");
  return (
    <div className="space-y-1">
      <div className="flex items-center justify-between text-xs">
        <span className="text-slate-300">{label}</span>
        <span className={`font-semibold ${color}`}>{value.toFixed(1)}</span>
      </div>
      <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
        <div className={`h-full rounded-full ${barColor}`} style={{ width: `${Math.min(100, displayVal)}%` }} />
      </div>
    </div>
  );
}

// ─── DealModal ────────────────────────────────────────────────────────────────

function DealModal({ deal, onClose }: { deal: Deal; onClose: () => void }) {
  const ref = useRef<HTMLDivElement>(null);
  const burden = BURDEN_META[deal.objection_burden];
  const action = ACTION_META[deal.objection_action];

  useEffect(() => {
    const h = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    document.addEventListener("keydown", h);
    return () => document.removeEventListener("keydown", h);
  }, [onClose]);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm" onClick={(e) => { if (ref.current && !ref.current.contains(e.target as Node)) onClose(); }}>
      <div ref={ref} className="w-full max-w-2xl bg-slate-900 border border-slate-700 rounded-2xl shadow-2xl max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="flex items-start justify-between p-6 border-b border-slate-800">
          <div className="space-y-1">
            <h2 className="text-white font-bold text-lg">{deal.deal_name}</h2>
            <p className="text-slate-400 text-sm">{deal.account_name}</p>
            <div className="flex items-center gap-2 mt-2">
              <span className={`inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs font-semibold ${burden.color} bg-slate-800`}>
                <span className={`w-1.5 h-1.5 rounded-full ${burden.bg}`} />
                {burden.label}
              </span>
              <span className={`inline-flex px-2 py-0.5 rounded-full text-xs font-semibold ${action.color} ${action.bg}`}>
                {action.label}
              </span>
              <span className="text-slate-500 text-xs">{STAGE_LABELS[deal.stage] ?? deal.stage}</span>
            </div>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white p-1 ml-4">✕</button>
        </div>

        <div className="p-6 space-y-6">
          {/* KPI row */}
          <div className="grid grid-cols-3 gap-3">
            <div className="bg-slate-800/60 rounded-xl p-3 text-center">
              <p className="text-slate-400 text-xs mb-1">ARR</p>
              <p className="text-white font-bold text-lg">{fmtEur(deal.arr_eur)}</p>
            </div>
            <div className="bg-slate-800/60 rounded-xl p-3 text-center">
              <p className="text-slate-400 text-xs mb-1">ARR impacté</p>
              <p className={`font-bold text-lg ${burden.color}`}>{fmtEur(deal.deal_impact_eur)}</p>
            </div>
            <div className="bg-slate-800/60 rounded-xl p-3 text-center">
              <p className="text-slate-400 text-xs mb-1">Objections actives</p>
              <p className={`font-bold text-lg ${deal.total_active_objections > 0 ? "text-red-400" : "text-emerald-400"}`}>
                {deal.total_active_objections}
              </p>
            </div>
          </div>

          {/* Primary objection */}
          <div className="bg-slate-800/40 rounded-xl px-4 py-3 flex items-center justify-between">
            <span className="text-slate-400 text-sm">Objection principale</span>
            <span className={`font-semibold text-sm ${burden.color}`}>
              {OBJECTION_TYPE_LABELS[deal.primary_objection_type] ?? deal.primary_objection_type}
            </span>
          </div>

          {/* Scores */}
          <div className="space-y-3">
            <h3 className="text-slate-300 font-semibold text-sm">Scores</h3>
            <ScoreBar value={deal.burden_score} label="Score de fardeau (+ = pire)" color={burden.color} invert />
            <ScoreBar value={deal.resolution_score} label="Score de résolution" color="text-emerald-400" />
          </div>

          {/* Risk factors */}
          {deal.risk_factors.length > 0 && (
            <div className="space-y-2">
              <h3 className="text-red-400 font-semibold text-sm">Facteurs de risque ({deal.risk_factors.length})</h3>
              <ul className="space-y-1">
                {deal.risk_factors.map((f, i) => (
                  <li key={i} className="flex items-start gap-2 text-xs text-slate-300">
                    <span className="text-red-400 flex-shrink-0 mt-0.5">▼</span>{f}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Mitigating factors */}
          {deal.mitigating_factors.length > 0 && (
            <div className="space-y-2">
              <h3 className="text-emerald-400 font-semibold text-sm">Facteurs atténuants ({deal.mitigating_factors.length})</h3>
              <ul className="space-y-1">
                {deal.mitigating_factors.map((m, i) => (
                  <li key={i} className="flex items-start gap-2 text-xs text-slate-300">
                    <span className="text-emerald-400 flex-shrink-0 mt-0.5">▲</span>{m}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Recommended tactics */}
          {deal.recommended_tactics.length > 0 && (
            <div className="space-y-2">
              <h3 className="text-amber-400 font-semibold text-sm">Tactiques recommandées</h3>
              <ol className="space-y-1">
                {deal.recommended_tactics.map((t, i) => (
                  <li key={i} className="flex items-start gap-2 text-xs text-slate-300">
                    <span className="text-amber-400 font-bold flex-shrink-0 mt-0.5">{i + 1}.</span>{t}
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

// ─── DealCard ─────────────────────────────────────────────────────────────────

function DealCard({ deal, onClick }: { deal: Deal; onClick: () => void }) {
  const burden = BURDEN_META[deal.objection_burden];
  const action = ACTION_META[deal.objection_action];

  return (
    <div
      onClick={onClick}
      className="bg-slate-800/60 border border-slate-700/50 rounded-xl p-4 hover:border-slate-500 hover:bg-slate-800 transition-all cursor-pointer space-y-3"
    >
      {/* Header */}
      <div className="flex items-start gap-3">
        <ObjectionRing score={deal.burden_score} burden={deal.objection_burden} />
        <div className="flex-1 min-w-0 space-y-1">
          <p className="text-white font-semibold text-sm truncate">{deal.deal_name}</p>
          <p className="text-slate-400 text-xs truncate">{deal.account_name}</p>
          <div className="flex items-center gap-1.5 flex-wrap">
            <span className={`px-1.5 py-0.5 rounded text-[10px] font-semibold ${burden.color} bg-slate-700`}>
              {burden.label}
            </span>
            <span className={`px-1.5 py-0.5 rounded text-[10px] font-semibold ${action.color} ${action.bg}`}>
              {action.label}
            </span>
          </div>
        </div>
      </div>

      {/* ARR + Stage */}
      <div className="flex items-center justify-between text-xs border-t border-slate-700/50 pt-2">
        <span className="text-slate-400">{STAGE_LABELS[deal.stage] ?? deal.stage}</span>
        <span className="text-white font-semibold">{fmtEur(deal.arr_eur)}</span>
      </div>

      {/* Objection count + type */}
      <div className="flex items-center justify-between text-xs">
        <span className="text-slate-400">Objections actives</span>
        <span className={`font-semibold ${deal.total_active_objections > 3 ? "text-red-400" : deal.total_active_objections > 0 ? "text-amber-400" : "text-emerald-400"}`}>
          {deal.total_active_objections}
        </span>
      </div>

      {/* Primary objection type */}
      {deal.primary_objection_type !== "none" && (
        <div className="flex items-center justify-between text-[11px] border-t border-slate-700/50 pt-2">
          <span className="text-slate-500">Objection principale</span>
          <span className={`font-medium ${burden.color}`}>
            {OBJECTION_TYPE_LABELS[deal.primary_objection_type] ?? deal.primary_objection_type}
          </span>
        </div>
      )}

      {/* Resolution bar */}
      <div className="pt-1 border-t border-slate-700/50">
        <ResolutionBar value={deal.resolution_score} />
      </div>

      {/* Impact */}
      <div className="flex items-center justify-between text-[11px]">
        <span className="text-slate-500">ARR impacté</span>
        <span className={burden.color}>{fmtEur(deal.deal_impact_eur)}</span>
      </div>
    </div>
  );
}

// ─── Main Page ────────────────────────────────────────────────────────────────

type BurdenFilter = "all" | ObjectionBurden;

export default function ObjectionIntelligencePage() {
  const [deals, setDeals] = useState<Deal[]>([]);
  const [summary, setSummary] = useState<Summary | null>(null);
  const [filter, setFilter] = useState<BurdenFilter>("all");
  const [loading, setLoading] = useState(true);
  const [selected, setSelected] = useState<Deal | null>(null);

  useEffect(() => {
    const params = new URLSearchParams();
    if (filter !== "all") params.set("burden", filter);
    fetch(`/api/objection-intelligence?${params}`)
      .then((r) => r.json())
      .then((data) => {
        setDeals(data.deals ?? []);
        setSummary(data.summary ?? null);
        setLoading(false);
      });
  }, [filter]);

  const tabs: { key: BurdenFilter; label: string; color?: string }[] = [
    { key: "all", label: "Tous" },
    { key: "clear", label: "Libre", color: "text-emerald-400" },
    { key: "moderate", label: "Modéré", color: "text-blue-400" },
    { key: "heavy", label: "Lourd", color: "text-amber-400" },
    { key: "critical", label: "Critique", color: "text-red-400" },
  ];

  const total = summary?.total ?? 0;
  const burdenBars = summary
    ? [
        { key: "clear" as const, count: summary.burden_counts.clear ?? 0, bg: "bg-emerald-500" },
        { key: "moderate" as const, count: summary.burden_counts.moderate ?? 0, bg: "bg-blue-500" },
        { key: "heavy" as const, count: summary.burden_counts.heavy ?? 0, bg: "bg-amber-500" },
        { key: "critical" as const, count: summary.burden_counts.critical ?? 0, bg: "bg-red-500" },
      ]
    : [];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-white">Intelligence Objections</h1>
        <p className="text-slate-400 text-sm mt-1">Analyse des objections de vente et tactiques de réponse par deal</p>
      </div>

      {/* KPI strip */}
      {summary && (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {[
            { label: "Deals analysés", value: summary.total.toString(), sub: `${summary.advance_ready_count} prêts à avancer`, color: "text-white" },
            { label: "Fardeau moyen", value: summary.avg_burden_score.toFixed(1), sub: `Résolution moy. : ${summary.avg_resolution_score.toFixed(1)}%`, color: summary.avg_burden_score > 50 ? "text-amber-400" : "text-blue-400" },
            { label: "Escalades requises", value: summary.escalation_count.toString(), sub: `${summary.critical_count} en situation critique`, color: summary.escalation_count > 0 ? "text-red-400" : "text-slate-400" },
            { label: "ARR à risque", value: fmtEur(summary.total_arr_at_risk_eur), sub: `Impact total : ${fmtEur(summary.total_arr_impacted_eur)}`, color: "text-amber-400" },
          ].map(({ label, value, sub, color }) => (
            <div key={label} className="bg-slate-800/60 border border-slate-700/50 rounded-xl p-4">
              <p className="text-slate-400 text-xs mb-1">{label}</p>
              <p className={`text-xl font-bold ${color}`}>{value}</p>
              <p className="text-slate-500 text-xs mt-1">{sub}</p>
            </div>
          ))}
        </div>
      )}

      {/* Burden distribution bar */}
      {total > 0 && (
        <div className="space-y-2">
          <div className="flex items-center justify-between text-xs text-slate-400">
            <span>Distribution du fardeau objections</span>
            <span>{total} deals</span>
          </div>
          <div className="flex h-2 rounded-full overflow-hidden gap-0.5">
            {burdenBars.map(({ key, count, bg }) =>
              count > 0 ? (
                <div key={key} className={`${bg} transition-all`} style={{ width: `${(count / total) * 100}%` }} />
              ) : null
            )}
          </div>
          <div className="flex flex-wrap gap-3 text-xs">
            {burdenBars.map(({ key, count, bg }) => (
              <span key={key} className="flex items-center gap-1 text-slate-400">
                <span className={`w-2 h-2 rounded-full ${bg}`} />
                {BURDEN_META[key].label} ({count})
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
                ({summary.burden_counts[key] ?? 0})
              </span>
            )}
          </button>
        ))}
      </div>

      {/* Deals grid */}
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

      {selected && <DealModal deal={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
