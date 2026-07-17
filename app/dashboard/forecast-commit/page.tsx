"use client";

import { useEffect, useState } from "react";

// ── Types ────────────────────────────────────────────────────────────────────

interface CommitDeal {
  deal_id: string;
  rep_id: string;
  rep_name: string;
  account_name: string;
  commit_score: number;
  sandbag_score: number;
  risk_score: number;
  calibrated_probability: number;
  commit_category: string;
  forecast_confidence: string;
  bias_type: string;
  commit_action: string;
  confidence_factors: string[];
  risk_factors: string[];
  recommended_actions: string[];
}

interface Summary {
  total: number;
  cat_counts: Record<string, number>;
  conf_counts: Record<string, number>;
  bias_counts: Record<string, number>;
  act_counts: Record<string, number>;
  avg_commit_score: number;
  avg_sandbag_score: number;
  avg_risk_score: number;
  avg_calibrated_probability: number;
  solid_commit_count: number;
  at_risk_count: number;
  escalation_count: number;
  sandbag_count: number;
}

// ── Helpers ──────────────────────────────────────────────────────────────────

function categoryColor(cat: string) {
  switch (cat) {
    case "commit":   return { ring: "#10b981", text: "text-emerald-400", bg: "bg-emerald-500/20", border: "border-emerald-500/30" };
    case "upside":   return { ring: "#6366f1", text: "text-indigo-400",  bg: "bg-indigo-500/20",  border: "border-indigo-500/30" };
    case "pipeline": return { ring: "#64748b", text: "text-slate-400",   bg: "bg-slate-500/20",   border: "border-slate-500/30" };
    case "at_risk":  return { ring: "#ef4444", text: "text-red-400",     bg: "bg-red-500/20",     border: "border-red-500/30" };
    case "omitted":  return { ring: "#6b7280", text: "text-gray-400",    bg: "bg-gray-500/20",    border: "border-gray-500/30" };
    default:         return { ring: "#64748b", text: "text-slate-400",   bg: "bg-slate-500/20",   border: "border-slate-500/30" };
  }
}

function categoryLabel(cat: string) {
  const map: Record<string, string> = {
    commit:   "Commit",
    upside:   "Upside",
    pipeline: "Pipeline",
    at_risk:  "À risque",
    omitted:  "Exclu",
  };
  return map[cat] ?? cat;
}

function confidenceLabel(conf: string) {
  const map: Record<string, string> = {
    high:     "Élevée",
    medium:   "Moyenne",
    low:      "Faible",
    very_low: "Très faible",
  };
  return map[conf] ?? conf;
}

function confidenceColor(conf: string) {
  switch (conf) {
    case "high":     return "text-emerald-400";
    case "medium":   return "text-indigo-400";
    case "low":      return "text-amber-400";
    case "very_low": return "text-red-400";
    default:         return "text-slate-400";
  }
}

function biasLabel(bias: string) {
  const map: Record<string, string> = {
    accurate:             "Précis",
    sandbagger:           "Sandbagger",
    optimistic:           "Optimiste",
    sandbagging_risk:     "Risque sandbag",
    overforecasting_risk: "Risque surforecast",
  };
  return map[bias] ?? bias;
}

function biasColor(bias: string) {
  switch (bias) {
    case "accurate":             return "text-emerald-400";
    case "sandbagger":           return "text-violet-400";
    case "sandbagging_risk":     return "text-purple-400";
    case "optimistic":           return "text-amber-400";
    case "overforecasting_risk": return "text-orange-400";
    default:                     return "text-slate-400";
  }
}

function actionLabel(action: string) {
  const map: Record<string, string> = {
    confirm:              "Confirmer",
    challenge:            "Challenger",
    pull_in:              "Accélérer",
    push_out:             "Reporter",
    escalate:             "Escalader",
    monitor:              "Surveiller",
  };
  return map[action] ?? action;
}

// ── Commit Gauge ─────────────────────────────────────────────────────────────

function CommitGauge({ score, category, size = 80 }: { score: number; category: string; size?: number }) {
  const { ring } = categoryColor(category);
  const cx = size / 2, cy = size / 2;
  const r = size * 0.38;
  const circ = 2 * Math.PI * r;
  const arc = (score / 100) * circ;
  const sw = size * 0.09;
  return (
    <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`} aria-hidden="true">
      <circle cx={cx} cy={cy} r={r} fill="none" stroke="#1e293b" strokeWidth={sw} />
      <circle cx={cx} cy={cy} r={r} fill="none" stroke={ring} strokeWidth={sw}
        strokeDasharray={`${arc} ${circ - arc}`} strokeLinecap="round"
        transform={`rotate(-90 ${cx} ${cy})`}
      />
      <text x={cx} y={cy + 4} textAnchor="middle" fill="white" fontSize={size * 0.18} fontWeight="700">
        {Math.round(score)}
      </text>
    </svg>
  );
}

// ── Category Dist Bar ─────────────────────────────────────────────────────────

function CatDistBar({ counts, total }: { counts: Record<string, number>; total: number }) {
  const cats = [
    { key: "commit",   color: "#10b981" },
    { key: "upside",   color: "#6366f1" },
    { key: "pipeline", color: "#64748b" },
    { key: "at_risk",  color: "#ef4444" },
    { key: "omitted",  color: "#6b7280" },
  ];
  return (
    <div className="flex h-2.5 rounded-full overflow-hidden gap-px bg-slate-800">
      {cats.map(({ key, color }) => {
        const pct = total > 0 ? ((counts[key] ?? 0) / total) * 100 : 0;
        return pct > 0 ? (
          <div key={key} style={{ width: `${pct}%`, background: color }} title={`${categoryLabel(key)}: ${counts[key]}`} />
        ) : null;
      })}
    </div>
  );
}

// ── Mini bar ──────────────────────────────────────────────────────────────────

function MiniBar({ value, color, label }: { value: number; color: string; label: string }) {
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

// ── Deal Card ─────────────────────────────────────────────────────────────────

function CommitCard({ deal, onClick }: { deal: CommitDeal; onClick: () => void }) {
  const col = categoryColor(deal.commit_category);
  return (
    <button
      onClick={onClick}
      className={`w-full text-left rounded-xl border p-4 transition-all hover:brightness-110 ${col.bg} ${col.border}`}
    >
      <div className="flex items-start gap-4">
        <CommitGauge score={deal.commit_score} category={deal.commit_category} size={72} />
        <div className="flex-1 min-w-0">
          <div className="flex items-center justify-between gap-2 mb-1">
            <span className="text-white font-semibold text-sm truncate">{deal.account_name}</span>
            <span className={`text-xs font-medium px-2 py-0.5 rounded-full ${col.bg} ${col.text} border ${col.border}`}>
              {categoryLabel(deal.commit_category)}
            </span>
          </div>
          <p className="text-xs text-slate-500 mb-2">{deal.rep_name}</p>
          <div className="grid grid-cols-3 gap-2 mb-2">
            <MiniBar value={deal.commit_score}  color="#10b981" label="Commit" />
            <MiniBar value={deal.sandbag_score} color="#8b5cf6" label="Sandbag" />
            <MiniBar value={deal.risk_score}    color="#ef4444" label="Risque" />
          </div>
          <div className="flex items-center justify-between text-[10px]">
            <span className={`font-medium ${confidenceColor(deal.forecast_confidence)}`}>
              {confidenceLabel(deal.forecast_confidence)} — {Math.round(deal.calibrated_probability * 100)}%
            </span>
            <span className={`ml-2 ${biasColor(deal.bias_type)}`}>
              {biasLabel(deal.bias_type)}
            </span>
          </div>
          <div className="mt-1 text-[10px] text-slate-400">
            Action : {actionLabel(deal.commit_action)}
          </div>
        </div>
      </div>
    </button>
  );
}

// ── Deal Modal ────────────────────────────────────────────────────────────────

function CommitModal({ deal, onClose }: { deal: CommitDeal; onClose: () => void }) {
  const col = categoryColor(deal.commit_category);
  const [tab, setTab] = useState<"actions" | "confidence" | "risk">("actions");

  useEffect(() => {
    const handler = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    document.addEventListener("keydown", handler);
    return () => document.removeEventListener("keydown", handler);
  }, [onClose]);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 p-4" onClick={onClose}>
      <div
        className="w-full max-w-2xl bg-slate-900 border border-slate-700 rounded-2xl shadow-2xl max-h-[90vh] overflow-y-auto"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="flex items-center justify-between p-5 border-b border-slate-800">
          <div className="flex items-center gap-4">
            <CommitGauge score={deal.commit_score} category={deal.commit_category} size={64} />
            <div>
              <h2 className="text-white font-bold text-lg">{deal.account_name}</h2>
              <p className="text-slate-400 text-sm">{deal.rep_name}</p>
              <div className="flex items-center gap-2 mt-1 flex-wrap">
                <span className={`text-xs font-medium px-2 py-0.5 rounded-full ${col.bg} ${col.text} border ${col.border}`}>
                  {categoryLabel(deal.commit_category)}
                </span>
                <span className={`text-xs ${confidenceColor(deal.forecast_confidence)}`}>
                  Conf. {confidenceLabel(deal.forecast_confidence)}
                </span>
                <span className={`text-xs ${biasColor(deal.bias_type)}`}>
                  {biasLabel(deal.bias_type)}
                </span>
              </div>
            </div>
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-white text-2xl leading-none">×</button>
        </div>

        {/* Score strip */}
        <div className="grid grid-cols-4 gap-3 p-5 border-b border-slate-800">
          {[
            { label: "Commit",   value: Math.round(deal.commit_score),  color: "#10b981", suffix: "" },
            { label: "Sandbag",  value: Math.round(deal.sandbag_score), color: "#8b5cf6", suffix: "" },
            { label: "Risque",   value: Math.round(deal.risk_score),    color: "#ef4444", suffix: "" },
            { label: "Prob. calib.", value: Math.round(deal.calibrated_probability * 100), color: "#6366f1", suffix: "%" },
          ].map(({ label, value, color, suffix }) => (
            <div key={label} className="bg-slate-800/50 rounded-lg p-3 text-center">
              <div className="text-2xl font-bold" style={{ color }}>{value}{suffix}</div>
              <div className="text-xs text-slate-400">{label}</div>
            </div>
          ))}
        </div>

        {/* Tabs */}
        <div className="flex border-b border-slate-800 px-5">
          {(["actions", "confidence", "risk"] as const).map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`px-4 py-3 text-sm font-medium border-b-2 transition-colors ${
                tab === t ? "border-indigo-500 text-indigo-400" : "border-transparent text-slate-500 hover:text-slate-300"
              }`}
            >
              {t === "actions" ? "Actions" : t === "confidence" ? "Facteurs de confiance" : "Facteurs de risque"}
            </button>
          ))}
        </div>

        <div className="p-5 space-y-3">
          {tab === "actions" && (
            <>
              <div className={`text-sm font-medium px-3 py-2 rounded-lg ${col.bg} ${col.text} border ${col.border}`}>
                Action : {actionLabel(deal.commit_action)}
              </div>
              {deal.recommended_actions.map((a, i) => (
                <div key={i} className="flex gap-2 text-sm text-slate-300 bg-slate-800/50 rounded-lg p-3">
                  <span className="text-indigo-400 flex-shrink-0">→</span>
                  <span>{a}</span>
                </div>
              ))}
            </>
          )}

          {tab === "confidence" && (
            <>
              {deal.confidence_factors.length > 0 ? (
                deal.confidence_factors.map((f, i) => (
                  <div key={i} className="flex gap-2 text-sm text-slate-300 bg-emerald-500/10 border border-emerald-500/20 rounded-lg p-3">
                    <span className="text-emerald-400 flex-shrink-0">✓</span>
                    <span>{f}</span>
                  </div>
                ))
              ) : (
                <p className="text-slate-500 text-sm">Aucun facteur de confiance détecté.</p>
              )}
            </>
          )}

          {tab === "risk" && (
            <>
              {deal.risk_factors.length > 0 ? (
                deal.risk_factors.map((f, i) => (
                  <div key={i} className="flex gap-2 text-sm text-slate-300 bg-red-500/10 border border-red-500/20 rounded-lg p-3">
                    <span className="text-red-400 flex-shrink-0">⚠</span>
                    <span>{f}</span>
                  </div>
                ))
              ) : (
                <p className="text-slate-500 text-sm">Aucun facteur de risque détecté.</p>
              )}
            </>
          )}
        </div>
      </div>
    </div>
  );
}

// ── Main Page ─────────────────────────────────────────────────────────────────

export default function ForecastCommitPage() {
  const [deals, setDeals]       = useState<CommitDeal[]>([]);
  const [summary, setSummary]   = useState<Summary | null>(null);
  const [loading, setLoading]   = useState(true);
  const [error, setError]       = useState<string | null>(null);
  const [catFilter, setCat]     = useState("all");
  const [confFilter, setConf]   = useState("all");
  const [selected, setSelected] = useState<CommitDeal | null>(null);

  async function fetchData() {
      setLoading(true);
      setError(null);
      try {
        const params = new URLSearchParams();
        if (catFilter !== "all")  params.set("category",   catFilter);
        if (confFilter !== "all") params.set("confidence", confFilter);
        const res = await fetch(`/api/forecast-commit?${params}`);
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();
        setDeals(data.deals ?? []);
        setSummary(data.summary ?? null);
      } catch (e: unknown) {
        setError(e instanceof Error ? e.message : "Erreur inconnue");
      } finally {
        setLoading(false);
      }
  }

  useEffect(() => {
    fetchData();
  }, [catFilter, confFilter]);

  const categories  = ["all", "commit", "upside", "pipeline", "at_risk", "omitted"];
  const confidences = ["all", "high", "medium", "low", "very_low"];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
      <div className="max-w-7xl mx-auto space-y-6">

        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-white">Forecast Commit Intelligence</h1>
            <p className="text-slate-400 text-sm mt-1">Validation et calibration des commits commerciaux</p>
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
          <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-8 gap-3">
            {[
              { label: "Total",          value: summary.total,                                       color: "text-white" },
              { label: "Commits solides",value: summary.solid_commit_count,                          color: "text-emerald-400" },
              { label: "À risque",       value: summary.at_risk_count,                               color: "text-red-400" },
              { label: "Escalades",      value: summary.escalation_count,                            color: "text-orange-400" },
              { label: "Sandbaggeurs",   value: summary.sandbag_count,                               color: "text-violet-400" },
              { label: "Score commit",   value: summary.avg_commit_score,                            color: "text-indigo-400" },
              { label: "Score risque",   value: summary.avg_risk_score,                              color: "text-red-400" },
              { label: "Prob. moyenne",  value: `${Math.round(summary.avg_calibrated_probability * 100)}%`, color: "text-cyan-400" },
            ].map(({ label, value, color }) => (
              <div key={label} className="bg-slate-900 border border-slate-800 rounded-xl p-3 text-center">
                <div className={`text-xl font-bold ${color}`}>{value}</div>
                <div className="text-[10px] text-slate-500 mt-1">{label}</div>
              </div>
            ))}
          </div>
        )}

        {/* Distribution bar */}
        {summary && (
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="flex items-center justify-between mb-3">
              <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Distribution par catégorie</span>
              <div className="flex gap-3 text-xs">
                {["commit", "upside", "pipeline", "at_risk", "omitted"].map((cat) => (
                  (summary.cat_counts[cat] ?? 0) > 0 && (
                    <span key={cat} className={categoryColor(cat).text}>
                      {categoryLabel(cat)}: {summary.cat_counts[cat]}
                    </span>
                  )
                ))}
              </div>
            </div>
            <CatDistBar counts={summary.cat_counts} total={summary.total} />
          </div>
        )}

        {/* Filters */}
        <div className="space-y-2">
          <div className="flex flex-wrap gap-2">
            {categories.map((c) => (
              <button
                key={c}
                onClick={() => setCat(c)}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
                  catFilter === c ? "bg-indigo-600 text-white" : "bg-slate-800 text-slate-400 hover:text-white"
                }`}
              >
                {c === "all" ? "Toutes catégories" : categoryLabel(c)}
              </button>
            ))}
          </div>
          <div className="flex flex-wrap gap-2">
            {confidences.map((cf) => (
              <button
                key={cf}
                onClick={() => setConf(cf)}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
                  confFilter === cf ? "bg-emerald-600 text-white" : "bg-slate-800 text-slate-400 hover:text-white"
                }`}
              >
                {cf === "all" ? "Toutes confiances" : confidenceLabel(cf)}
              </button>
            ))}
          </div>
        </div>

        {/* Content */}
        {loading && <div className="text-center py-20 text-slate-400">Chargement...</div>}
        {error && <div className="text-center py-20 text-red-400">Erreur : {error}</div>}
        {!loading && !error && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
            {deals.map((deal) => (
              <CommitCard key={deal.deal_id} deal={deal} onClick={() => setSelected(deal)} />
            ))}
            {deals.length === 0 && (
              <div className="col-span-2 text-center py-20 text-slate-500">
                Aucun deal trouvé pour les filtres sélectionnés.
              </div>
            )}
          </div>
        )}
      </div>

      {selected && <CommitModal deal={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
