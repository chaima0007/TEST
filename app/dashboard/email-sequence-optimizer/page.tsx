"use client";

import { useState, useEffect, useRef } from "react";

interface StepOptimization {
  step_number: number;
  step_type: string;
  current_day_offset: number;
  recommended_day_offset: number;
  timing_score: number;
  performance_score: number;
  issues: string[];
  recommendations: string[];
}

interface SequenceResult {
  sequence_id: string;
  sequence_name: string;
  strategy: string;
  overall_score: number;
  status: string;
  avg_open_rate_pct: number;
  avg_reply_rate_pct: number;
  conversion_rate_pct: number;
  bounce_rate_pct: number;
  estimated_pipeline_eur: number;
  recommended_strategy: string;
  sequence_signals: string[];
  risk_signals: string[];
  step_optimizations: StepOptimization[];
}

interface Summary {
  total: number;
  status_counts: Record<string, number>;
  strategy_counts: Record<string, number>;
  avg_score: number;
  avg_conversion_rate_pct: number;
  total_pipeline_eur: number;
}

const STATUS_TABS = [
  { key: "all", label: "Toutes" },
  { key: "excellent", label: "Excellent" },
  { key: "good", label: "Bon" },
  { key: "average", label: "Moyen" },
  { key: "poor", label: "Faible" },
  { key: "critical", label: "Critique" },
];

const STATUS_COLORS: Record<string, string> = {
  excellent: "#6366f1",
  good: "#22c55e",
  average: "#f59e0b",
  poor: "#f97316",
  critical: "#ef4444",
};

const STATUS_BG: Record<string, string> = {
  excellent: "bg-indigo-500/10 text-indigo-400 border-indigo-500/30",
  good: "bg-green-500/10 text-green-400 border-green-500/30",
  average: "bg-amber-500/10 text-amber-400 border-amber-500/30",
  poor: "bg-orange-500/10 text-orange-400 border-orange-500/30",
  critical: "bg-red-500/10 text-red-400 border-red-500/30",
};

const STATUS_LABELS: Record<string, string> = {
  excellent: "Excellent",
  good: "Bon",
  average: "Moyen",
  poor: "Faible",
  critical: "Critique",
};

const STRATEGY_LABELS: Record<string, string> = {
  aggressive: "Agressif",
  balanced: "Équilibré",
  nurture: "Nurture",
  reactivation: "Réactivation",
};

const STEP_TYPE_ICONS: Record<string, string> = {
  email: "📧",
  linkedin: "💼",
  phone: "📞",
  video: "🎥",
  direct_mail: "📬",
};

function fmtEur(n: number) {
  if (n >= 1_000_000) return `${(n / 1_000_000).toFixed(1)}M€`;
  if (n >= 1_000) return `${(n / 1_000).toFixed(0)}k€`;
  return `${n}€`;
}

function ScoreRing({ score, status }: { score: number; status: string }) {
  const r = 28;
  const circ = 2 * Math.PI * r;
  const fill = (score / 100) * circ;
  const color = STATUS_COLORS[status] || "#6366f1";

  return (
    <svg width="72" height="72" viewBox="0 0 72 72" className="shrink-0">
      <circle cx="36" cy="36" r={r} fill="none" stroke="#1e293b" strokeWidth="6" />
      <circle
        cx="36"
        cy="36"
        r={r}
        fill="none"
        stroke={color}
        strokeWidth="6"
        strokeDasharray={`${fill} ${circ - fill}`}
        strokeLinecap="round"
        transform="rotate(-90 36 36)"
      />
      <text x="36" y="40" textAnchor="middle" fontSize="13" fontWeight="700" fill={color}>
        {Math.round(score)}
      </text>
    </svg>
  );
}

function MiniBar({ label, value, max = 100 }: { label: string; value: number; max?: number }) {
  const pct = Math.min(100, (value / max) * 100);
  const color =
    pct >= 75 ? "#22c55e" : pct >= 50 ? "#6366f1" : pct >= 30 ? "#f59e0b" : "#ef4444";
  return (
    <div className="flex flex-col gap-1">
      <div className="flex justify-between text-xs text-slate-400">
        <span>{label}</span>
        <span className="font-semibold" style={{ color }}>
          {value.toFixed(1)}%
        </span>
      </div>
      <div className="h-1.5 rounded-full bg-slate-800 overflow-hidden">
        <div
          className="h-full rounded-full transition-all duration-500"
          style={{ width: `${pct}%`, backgroundColor: color }}
        />
      </div>
    </div>
  );
}

function SequenceModal({ seq, onClose }: { seq: SequenceResult; onClose: () => void }) {
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handler = (e: KeyboardEvent) => e.key === "Escape" && onClose();
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [onClose]);

  useEffect(() => {
    const handler = (e: MouseEvent) => {
      if (ref.current && !ref.current.contains(e.target as Node)) onClose();
    };
    setTimeout(() => window.addEventListener("mousedown", handler), 0);
    return () => window.removeEventListener("mousedown", handler);
  }, [onClose]);

  const statusColor = STATUS_COLORS[seq.status] || "#6366f1";

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4">
      <div
        ref={ref}
        className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-2xl max-h-[90vh] overflow-y-auto"
      >
        <div className="p-6 border-b border-slate-800 flex items-start justify-between gap-4">
          <div>
            <div className="flex items-center gap-3 flex-wrap">
              <h2 className="text-xl font-bold text-slate-100">{seq.sequence_name}</h2>
              <span
                className={`text-xs px-2 py-0.5 rounded-full border font-medium ${STATUS_BG[seq.status]}`}
              >
                {STATUS_LABELS[seq.status]}
              </span>
              <span className="text-xs px-2 py-0.5 rounded-full bg-slate-800 text-slate-300 font-medium">
                {STRATEGY_LABELS[seq.strategy] ?? seq.strategy}
              </span>
            </div>
            <p className="text-sm text-slate-400 mt-1">
              Recommandé : {STRATEGY_LABELS[seq.recommended_strategy] ?? seq.recommended_strategy}
            </p>
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-slate-200 text-xl shrink-0">
            ✕
          </button>
        </div>

        <div className="p-6 space-y-6">
          {/* KPIs */}
          <div className="grid grid-cols-2 gap-3 sm:grid-cols-4">
            {[
              { label: "Taux d'ouverture", value: `${seq.avg_open_rate_pct.toFixed(1)}%` },
              { label: "Taux de réponse", value: `${seq.avg_reply_rate_pct.toFixed(1)}%` },
              { label: "Conversion", value: `${seq.conversion_rate_pct.toFixed(1)}%` },
              {
                label: "Pipeline estimé",
                value: fmtEur(seq.estimated_pipeline_eur),
                color: "text-indigo-400",
              },
            ].map((kpi) => (
              <div key={kpi.label} className="bg-slate-800/50 rounded-xl p-3 text-center">
                <div className={`text-lg font-bold ${kpi.color ?? "text-slate-100"}`}>
                  {kpi.value}
                </div>
                <div className="text-xs text-slate-400 mt-0.5">{kpi.label}</div>
              </div>
            ))}
          </div>

          {/* Score ring */}
          <div className="flex items-center gap-6 bg-slate-800/30 rounded-xl p-4">
            <ScoreRing score={seq.overall_score} status={seq.status} />
            <div>
              <div className="flex items-baseline gap-2 mb-1">
                <span className="text-2xl font-bold" style={{ color: statusColor }}>
                  {seq.overall_score.toFixed(1)}
                </span>
                <span className="text-sm text-slate-400">/ 100 — score séquence</span>
              </div>
              <div className="text-xs text-slate-400">
                Bounce :{" "}
                <span
                  className={
                    seq.bounce_rate_pct >= 5
                      ? "text-red-400 font-semibold"
                      : seq.bounce_rate_pct >= 2
                      ? "text-amber-400"
                      : "text-green-400"
                  }
                >
                  {seq.bounce_rate_pct.toFixed(1)}%
                </span>
              </div>
            </div>
          </div>

          {/* Step-by-step */}
          <div>
            <h3 className="text-sm font-semibold text-slate-300 mb-3">
              Analyse pas-à-pas ({seq.step_optimizations.length} étapes)
            </h3>
            <div className="space-y-3">
              {seq.step_optimizations.map((step) => (
                <div
                  key={step.step_number}
                  className="bg-slate-800/40 rounded-xl p-4 border border-slate-700/50"
                >
                  <div className="flex items-center justify-between mb-2">
                    <div className="flex items-center gap-2">
                      <span className="text-lg">
                        {STEP_TYPE_ICONS[step.step_type] ?? "📨"}
                      </span>
                      <span className="text-sm font-semibold text-slate-200">
                        Étape {step.step_number} — {step.step_type}
                      </span>
                    </div>
                    <div className="flex gap-3 text-xs text-slate-400">
                      <span>
                        Timing{" "}
                        <span
                          className={`font-bold ${
                            step.timing_score >= 80
                              ? "text-green-400"
                              : step.timing_score >= 50
                              ? "text-amber-400"
                              : "text-red-400"
                          }`}
                        >
                          {Math.round(step.timing_score)}
                        </span>
                      </span>
                      <span>
                        Perf{" "}
                        <span
                          className={`font-bold ${
                            step.performance_score >= 70
                              ? "text-green-400"
                              : step.performance_score >= 50
                              ? "text-amber-400"
                              : "text-red-400"
                          }`}
                        >
                          {Math.round(step.performance_score)}
                        </span>
                      </span>
                    </div>
                  </div>
                  <div className="text-xs text-slate-500 mb-2">
                    Jour actuel : J+{step.current_day_offset}
                    {step.current_day_offset !== step.recommended_day_offset && (
                      <span className="text-amber-400 ml-2">
                        → Recommandé : J+{step.recommended_day_offset}
                      </span>
                    )}
                  </div>
                  {step.issues.length > 0 && (
                    <ul className="space-y-1 mt-2">
                      {step.issues.map((issue, i) => (
                        <li key={i} className="text-xs text-red-400 flex gap-1.5">
                          <span>⚠</span>
                          <span>{issue}</span>
                        </li>
                      ))}
                    </ul>
                  )}
                  {step.recommendations.length > 0 && (
                    <ul className="space-y-1 mt-2">
                      {step.recommendations.map((rec, i) => (
                        <li key={i} className="text-xs text-indigo-400 flex gap-1.5">
                          <span>→</span>
                          <span>{rec}</span>
                        </li>
                      ))}
                    </ul>
                  )}
                </div>
              ))}
            </div>
          </div>

          {/* Signals */}
          {seq.sequence_signals.length > 0 && (
            <div>
              <h3 className="text-sm font-semibold text-green-400 mb-2">Signaux positifs</h3>
              <ul className="space-y-1">
                {seq.sequence_signals.map((s, i) => (
                  <li key={i} className="text-xs text-slate-300 flex gap-2">
                    <span className="text-green-400 shrink-0">✓</span>
                    <span>{s}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}
          {seq.risk_signals.length > 0 && (
            <div>
              <h3 className="text-sm font-semibold text-red-400 mb-2">Points d&apos;attention</h3>
              <ul className="space-y-1">
                {seq.risk_signals.map((s, i) => (
                  <li key={i} className="text-xs text-slate-300 flex gap-2">
                    <span className="text-red-400 shrink-0">⚠</span>
                    <span>{s}</span>
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

function SequenceCard({ seq, onClick }: { seq: SequenceResult; onClick: () => void }) {
  return (
    <button
      onClick={onClick}
      className="bg-slate-900 border border-slate-800 rounded-2xl p-5 text-left hover:border-slate-600 transition-all hover:bg-slate-800/40 group"
    >
      <div className="flex items-start gap-4">
        <ScoreRing score={seq.overall_score} status={seq.status} />
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 flex-wrap mb-1">
            <span className="font-semibold text-slate-100 truncate text-sm">{seq.sequence_name}</span>
            <span
              className={`text-xs px-2 py-0.5 rounded-full border font-medium shrink-0 ${STATUS_BG[seq.status]}`}
            >
              {STATUS_LABELS[seq.status]}
            </span>
          </div>
          <p className="text-xs text-slate-400 mb-3">
            Stratégie : {STRATEGY_LABELS[seq.strategy] ?? seq.strategy} ·{" "}
            {seq.step_optimizations.length} étapes
          </p>

          <div className="flex flex-wrap gap-2 text-xs">
            <span className="bg-slate-800 rounded-lg px-2 py-1 text-slate-300">
              {seq.avg_open_rate_pct.toFixed(0)}% ouverture
            </span>
            <span className="bg-slate-800 rounded-lg px-2 py-1 text-slate-300">
              {seq.avg_reply_rate_pct.toFixed(0)}% réponse
            </span>
            {seq.estimated_pipeline_eur > 0 && (
              <span className="bg-indigo-500/10 text-indigo-400 rounded-lg px-2 py-1">
                {fmtEur(seq.estimated_pipeline_eur)}
              </span>
            )}
          </div>
        </div>
      </div>

      {/* Mini perf bars */}
      <div className="mt-4 space-y-2">
        <MiniBar label="Taux ouverture" value={seq.avg_open_rate_pct} max={50} />
        <MiniBar label="Taux réponse" value={seq.avg_reply_rate_pct} max={25} />
        <MiniBar label="Conversion" value={seq.conversion_rate_pct} max={15} />
      </div>

      {/* Issues count */}
      {(() => {
        const issues = seq.step_optimizations.reduce((n, s) => n + s.issues.length, 0);
        return issues > 0 ? (
          <div className="mt-3 text-xs text-amber-400">
            {issues} problème{issues > 1 ? "s" : ""} détecté{issues > 1 ? "s" : ""}
          </div>
        ) : (
          <div className="mt-3 text-xs text-green-500">Aucun problème détecté</div>
        );
      })()}
    </button>
  );
}

export default function EmailSequenceOptimizerPage() {
  const [sequences, setSequences] = useState<SequenceResult[]>([]);
  const [summary, setSummary] = useState<Summary | null>(null);
  const [activeStatus, setActiveStatus] = useState("all");
  const [selected, setSelected] = useState<SequenceResult | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      setLoading(true);
      try {
        const params = new URLSearchParams();
        if (activeStatus !== "all") params.set("status", activeStatus);
        const res = await fetch(`/api/email-sequence-optimizer?${params}`);
        const data = await res.json();
        setSequences(data.sequences ?? []);
        setSummary(data.summary ?? null);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, [activeStatus]);

  return (
    <div className="min-h-screen bg-slate-950 p-6">
      <div className="max-w-7xl mx-auto space-y-6">
        {/* Header */}
        <div>
          <h1 className="text-2xl font-bold text-slate-100">Optimiseur Séquences Email</h1>
          <p className="text-sm text-slate-400 mt-1">
            Analyse et optimisation des séquences outreach — timing, performance et conversion
          </p>
        </div>

        {/* KPI strip */}
        {summary && (
          <div className="grid grid-cols-2 gap-3 sm:grid-cols-4">
            {[
              {
                label: "Séquences analysées",
                value: `${summary.total}`,
                sub: `${summary.status_counts["excellent"] || 0} excellentes`,
                color: "text-slate-100",
              },
              {
                label: "Score moyen",
                value: `${summary.avg_score}/100`,
                sub: `${summary.status_counts["critical"] || 0} critiques`,
                color:
                  summary.avg_score >= 70
                    ? "text-green-400"
                    : summary.avg_score >= 50
                    ? "text-amber-400"
                    : "text-red-400",
              },
              {
                label: "Taux conv. moyen",
                value: `${summary.avg_conversion_rate_pct.toFixed(1)}%`,
                sub: "Tous canaux confondus",
                color:
                  summary.avg_conversion_rate_pct >= 5
                    ? "text-green-400"
                    : summary.avg_conversion_rate_pct >= 2
                    ? "text-amber-400"
                    : "text-red-400",
              },
              {
                label: "Pipeline total",
                value: fmtEur(summary.total_pipeline_eur),
                sub: "Deals estimés actifs",
                color: "text-indigo-400",
              },
            ].map((kpi) => (
              <div
                key={kpi.label}
                className="bg-slate-900 border border-slate-800 rounded-2xl p-4"
              >
                <div className={`text-2xl font-bold ${kpi.color}`}>{kpi.value}</div>
                <div className="text-xs text-slate-400 mt-0.5">{kpi.label}</div>
                <div className="text-xs text-slate-500 mt-1">{kpi.sub}</div>
              </div>
            ))}
          </div>
        )}

        {/* Status filter tabs */}
        <div className="flex flex-wrap gap-2">
          {STATUS_TABS.map((t) => {
            const count =
              t.key === "all" ? summary?.total : summary?.status_counts[t.key];
            return (
              <button
                key={t.key}
                onClick={() => setActiveStatus(t.key)}
                className={`px-4 py-1.5 rounded-full text-sm font-medium border transition-all ${
                  activeStatus === t.key
                    ? "bg-indigo-600 border-indigo-500 text-white"
                    : "bg-slate-800/50 border-slate-700 text-slate-400 hover:border-slate-500"
                }`}
              >
                {t.label}
                {count !== undefined && (
                  <span className="ml-1.5 text-xs opacity-70">({count})</span>
                )}
              </button>
            );
          })}
        </div>

        {/* Sequences grid */}
        {loading ? (
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {Array.from({ length: 6 }).map((_, i) => (
              <div key={i} className="h-64 bg-slate-900 border border-slate-800 rounded-2xl animate-pulse" />
            ))}
          </div>
        ) : sequences.length === 0 ? (
          <div className="text-center py-20 text-slate-500">Aucune séquence pour ce filtre</div>
        ) : (
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {sequences.map((seq) => (
              <SequenceCard
                key={seq.sequence_id}
                seq={seq}
                onClick={() => setSelected(seq)}
              />
            ))}
          </div>
        )}
      </div>

      {selected && <SequenceModal seq={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
