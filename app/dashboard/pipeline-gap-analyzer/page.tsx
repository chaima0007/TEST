"use client";

import { useEffect, useState } from "react";

interface RepData {
  rep_id: string;
  rep_name: string;
  region: string;
  segment: string;
  quota_eur: number;
  gap_eur: number;
  gap_severity: string;
  pipeline_action: string;
  quota_risk: string;
  coverage_health: string;
  coverage_ratio: number;
  expected_close_eur: number;
  quota_remaining_eur: number;
  attainment_pct: number;
  run_rate_pct: number;
  gap_drivers: string[];
  gap_closers: string[];
  pipeline_score: number;
}

interface Summary {
  total: number;
  severity_counts: Record<string, number>;
  action_counts: Record<string, number>;
  risk_counts: Record<string, number>;
  avg_pipeline_score: number;
  avg_coverage_ratio: number;
  critical_count: number;
  emergency_count: number;
  total_gap_eur: number;
}

interface ApiResponse {
  reps: RepData[];
  summary: Summary;
}

const SEVERITY_META: Record<string, { label: string; color: string; dot: string }> = {
  critical: { label: "Critique", color: "text-red-400", dot: "bg-red-500" },
  severe:   { label: "Sévère",   color: "text-orange-400", dot: "bg-orange-500" },
  moderate: { label: "Modéré",   color: "text-yellow-400", dot: "bg-yellow-500" },
  minor:    { label: "Mineur",   color: "text-blue-400",  dot: "bg-blue-500" },
  none:     { label: "Aucun",    color: "text-emerald-400", dot: "bg-emerald-500" },
};

const ACTION_META: Record<string, { label: string; badge: string }> = {
  emergency: { label: "Urgence",    badge: "bg-red-500/20 text-red-300 border-red-500/30" },
  build:     { label: "Construire", badge: "bg-orange-500/20 text-orange-300 border-orange-500/30" },
  accelerate:{ label: "Accélérer", badge: "bg-yellow-500/20 text-yellow-300 border-yellow-500/30" },
  maintain:  { label: "Maintenir", badge: "bg-emerald-500/20 text-emerald-300 border-emerald-500/30" },
};

const RISK_META: Record<string, { label: string; color: string }> = {
  critical: { label: "Critique",  color: "text-red-400" },
  behind:   { label: "En retard", color: "text-orange-400" },
  at_risk:  { label: "À risque",  color: "text-yellow-400" },
  on_track: { label: "En route",  color: "text-emerald-400" },
};

const HEALTH_META: Record<string, { label: string; color: string }> = {
  healthy:      { label: "Saine (≥4x)",     color: "text-emerald-400" },
  adequate:     { label: "Adéquate (≥3x)", color: "text-blue-400" },
  thin:         { label: "Mince (≥2x)",     color: "text-yellow-400" },
  insufficient: { label: "Insuffisante",   color: "text-red-400" },
};

function fmt(n: number) {
  if (n >= 1_000_000) return `${(n / 1_000_000).toFixed(1)}M€`;
  if (n >= 1_000) return `${Math.round(n / 1_000)}K€`;
  return `${n}€`;
}

function CoverageRing({ score, size = 96 }: { score: number; size?: number }) {
  const r = size * 0.42;
  const circ = 2 * Math.PI * r;
  const arc = Math.min(1, score / 100) * circ;
  const cx = size / 2;
  const color =
    score >= 70 ? "#10b981" : score >= 50 ? "#f59e0b" : score >= 30 ? "#f97316" : "#ef4444";
  return (
    <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`}>
      <circle cx={cx} cy={cx} r={r} fill="none" stroke="#1e293b" strokeWidth={size * 0.1} />
      <circle
        cx={cx} cy={cx} r={r} fill="none" stroke={color}
        strokeWidth={size * 0.1}
        strokeDasharray={`${arc} ${circ - arc}`}
        strokeLinecap="round"
        transform={`rotate(-90 ${cx} ${cx})`}
      />
      <text x={cx} y={cx + size * 0.07} textAnchor="middle" fill={color} fontSize={size * 0.22} fontWeight="bold">
        {score.toFixed(0)}
      </text>
      <text x={cx} y={cx + size * 0.22} textAnchor="middle" fill="#64748b" fontSize={size * 0.11}>
        /100
      </text>
    </svg>
  );
}

function GapModal({ rep, onClose }: { rep: RepData; onClose: () => void }) {
  const [tab, setTab] = useState<"drivers" | "closers" | "metrics">("drivers");
  useEffect(() => {
    const fn = (e: KeyboardEvent) => e.key === "Escape" && onClose();
    window.addEventListener("keydown", fn);
    return () => window.removeEventListener("keydown", fn);
  }, [onClose]);
  const sm = SEVERITY_META[rep.gap_severity] ?? SEVERITY_META.none;
  const am = ACTION_META[rep.pipeline_action] ?? ACTION_META.maintain;
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4" onClick={onClose}>
      <div className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-xl shadow-2xl" onClick={(e) => e.stopPropagation()}>
        <div className="p-6 border-b border-slate-800">
          <div className="flex items-start justify-between gap-4">
            <div>
              <h2 className="text-lg font-bold text-slate-100">{rep.rep_name}</h2>
              <p className="text-sm text-slate-400">{rep.region} · {rep.segment}</p>
            </div>
            <div className="flex items-center gap-2 flex-shrink-0">
              <span className={`text-xs font-semibold px-2 py-0.5 rounded-full border ${am.badge}`}>{am.label}</span>
              <button onClick={onClose} className="text-slate-500 hover:text-slate-300 text-xl leading-none">✕</button>
            </div>
          </div>
          <div className="mt-4 grid grid-cols-3 gap-3">
            <div className="bg-slate-800/50 rounded-lg p-3 text-center">
              <p className="text-xs text-slate-500 mb-1">Gap</p>
              <p className="text-lg font-bold text-red-400">{fmt(rep.gap_eur)}</p>
            </div>
            <div className="bg-slate-800/50 rounded-lg p-3 text-center">
              <p className="text-xs text-slate-500 mb-1">Couverture</p>
              <p className={`text-lg font-bold ${HEALTH_META[rep.coverage_health]?.color ?? "text-slate-300"}`}>{rep.coverage_ratio.toFixed(1)}x</p>
            </div>
            <div className="bg-slate-800/50 rounded-lg p-3 text-center">
              <p className="text-xs text-slate-500 mb-1">Atteinment</p>
              <p className="text-lg font-bold text-indigo-400">{rep.attainment_pct.toFixed(1)}%</p>
            </div>
          </div>
        </div>
        <div className="flex border-b border-slate-800">
          {(["drivers", "closers", "metrics"] as const).map((t) => (
            <button key={t} onClick={() => setTab(t)}
              className={`flex-1 py-3 text-xs font-semibold transition-colors ${tab === t ? "text-indigo-400 border-b-2 border-indigo-500" : "text-slate-500 hover:text-slate-300"}`}>
              {t === "drivers" ? "Causes du Gap" : t === "closers" ? "Plan d'Action" : "Métriques"}
            </button>
          ))}
        </div>
        <div className="p-5 max-h-72 overflow-y-auto">
          {tab === "drivers" && (
            <ul className="space-y-2">
              {rep.gap_drivers.length === 0
                ? <li className="text-sm text-slate-500 italic">Aucun driver identifié — pipeline en bonne santé</li>
                : rep.gap_drivers.map((d, i) => (
                    <li key={i} className="flex items-start gap-2 text-sm text-slate-300">
                      <span className="text-red-400 mt-0.5 flex-shrink-0">▸</span>{d}
                    </li>
                  ))}
            </ul>
          )}
          {tab === "closers" && (
            <ul className="space-y-2">
              {rep.gap_closers.map((c, i) => (
                <li key={i} className="flex items-start gap-2 text-sm text-slate-300">
                  <span className="text-emerald-400 mt-0.5 flex-shrink-0">✓</span>{c}
                </li>
              ))}
            </ul>
          )}
          {tab === "metrics" && (
            <div className="grid grid-cols-2 gap-3">
              {[
                ["Quota", fmt(rep.quota_eur)],
                ["Closé", fmt(rep.quota_eur - rep.quota_remaining_eur)],
                ["Remaining", fmt(rep.quota_remaining_eur)],
                ["Expected Close", fmt(rep.expected_close_eur)],
                ["Run Rate", `${rep.run_rate_pct.toFixed(1)}%`],
                ["Score Pipeline", `${rep.pipeline_score.toFixed(1)}/100`],
                ["Risque Quota", RISK_META[rep.quota_risk]?.label ?? rep.quota_risk],
                ["Santé Pipeline", HEALTH_META[rep.coverage_health]?.label ?? rep.coverage_health],
              ].map(([k, v]) => (
                <div key={k} className="bg-slate-800/50 rounded-lg p-2.5">
                  <p className="text-xs text-slate-500">{k}</p>
                  <p className="text-sm font-semibold text-slate-200">{v}</p>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

function RepCard({ rep, onClick }: { rep: RepData; onClick: () => void }) {
  const sm = SEVERITY_META[rep.gap_severity] ?? SEVERITY_META.none;
  const am = ACTION_META[rep.pipeline_action] ?? ACTION_META.maintain;
  return (
    <div onClick={onClick} className="bg-slate-800/50 border border-slate-700/50 rounded-xl p-4 cursor-pointer hover:border-indigo-500/40 hover:bg-slate-800/80 transition-all group">
      <div className="flex items-start justify-between gap-3 mb-3">
        <div className="flex items-center gap-3">
          <CoverageRing score={rep.pipeline_score} size={56} />
          <div>
            <h3 className="font-semibold text-slate-100 text-sm group-hover:text-indigo-300 transition-colors">{rep.rep_name}</h3>
            <p className="text-xs text-slate-500">{rep.region} · {rep.segment}</p>
            <div className="flex items-center gap-1.5 mt-1">
              <span className={`w-1.5 h-1.5 rounded-full ${sm.dot}`} />
              <span className={`text-xs font-medium ${sm.color}`}>{sm.label}</span>
            </div>
          </div>
        </div>
        <span className={`text-xs font-semibold px-2 py-0.5 rounded-full border flex-shrink-0 ${am.badge}`}>{am.label}</span>
      </div>
      <div className="grid grid-cols-3 gap-2 text-center">
        <div className="bg-slate-900/50 rounded-lg p-2">
          <p className="text-xs text-slate-500 mb-0.5">Gap</p>
          <p className={`text-sm font-bold ${rep.gap_eur > 0 ? "text-red-400" : "text-emerald-400"}`}>{rep.gap_eur > 0 ? fmt(rep.gap_eur) : "✓"}</p>
        </div>
        <div className="bg-slate-900/50 rounded-lg p-2">
          <p className="text-xs text-slate-500 mb-0.5">Couverture</p>
          <p className={`text-sm font-bold ${HEALTH_META[rep.coverage_health]?.color ?? "text-slate-300"}`}>{rep.coverage_ratio.toFixed(1)}x</p>
        </div>
        <div className="bg-slate-900/50 rounded-lg p-2">
          <p className="text-xs text-slate-500 mb-0.5">Atteinment</p>
          <p className="text-sm font-bold text-indigo-400">{rep.attainment_pct.toFixed(1)}%</p>
        </div>
      </div>
      {rep.gap_drivers.length > 0 && (
        <p className="mt-2 text-xs text-slate-500 truncate">
          ▸ {rep.gap_drivers[0]}
        </p>
      )}
    </div>
  );
}

export default function PipelineGapAnalyzerPage() {
  const [data, setData] = useState<ApiResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [selected, setSelected] = useState<RepData | null>(null);
  const [severityFilter, setSeverityFilter] = useState("");
  const [actionFilter, setActionFilter] = useState("");

  async function load() {
      setLoading(true);
      try {
        const params = new URLSearchParams();
        if (severityFilter) params.set("severity", severityFilter);
        if (actionFilter) params.set("action", actionFilter);
        const res = await fetch(`/api/pipeline-gap-analyzer?${params}`);
        if (res.ok) setData(await res.json());
      } finally {
        setLoading(false);
      }
  }

  useEffect(() => {
    load();
  }, [severityFilter, actionFilter]);

  const sum = data?.summary;
  const reps = data?.reps ?? [];

  const severities = ["critical", "severe", "moderate", "minor", "none"];
  const actions = ["emergency", "build", "accelerate", "maintain"];
  const severityTotal = sum ? Object.values(sum.severity_counts).reduce((a, b) => a + b, 0) : 0;

  return (
    <div className="min-h-screen bg-slate-950 p-6">
      <div className="max-w-7xl mx-auto space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-slate-100">Pipeline Gap Analyzer</h1>
            <p className="text-sm text-slate-400 mt-0.5">Analyse des écarts pipeline vs. quota — Module 31</p>
          </div>
          <button onClick={load} className="flex items-center gap-2 px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg text-sm font-medium transition-colors">
            <span className={loading ? "animate-spin" : ""}>↻</span> Actualiser
          </button>
        </div>

        {/* KPI Strip */}
        {sum && (
          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
            {[
              { label: "Reps analysés", value: sum.total, sub: "total", color: "text-slate-100" },
              { label: "Gap critique", value: sum.critical_count, sub: "reps", color: "text-red-400" },
              { label: "Action urgence", value: sum.emergency_count, sub: "reps", color: "text-orange-400" },
              { label: "Gap total", value: fmt(sum.total_gap_eur), sub: "à combler", color: "text-yellow-400" },
              { label: "Score moyen", value: `${sum.avg_pipeline_score}/100`, sub: "pipeline", color: "text-indigo-400" },
              { label: "Couverture moy.", value: `${sum.avg_coverage_ratio}x`, sub: "ratio pipeline", color: "text-violet-400" },
            ].map((kpi) => (
              <div key={kpi.label} className="bg-slate-800/50 border border-slate-700/50 rounded-xl p-4">
                <p className="text-xs text-slate-500 mb-1">{kpi.label}</p>
                <p className={`text-xl font-bold ${kpi.color}`}>{kpi.value}</p>
                <p className="text-xs text-slate-600 mt-0.5">{kpi.sub}</p>
              </div>
            ))}
          </div>
        )}

        {/* Severity Distribution Bar */}
        {sum && severityTotal > 0 && (
          <div className="bg-slate-800/50 border border-slate-700/50 rounded-xl p-4">
            <p className="text-xs text-slate-500 mb-3 font-medium uppercase tracking-wider">Distribution Sévérité Gap</p>
            <div className="flex h-3 rounded-full overflow-hidden gap-0.5">
              {severities.map((s) => {
                const cnt = sum.severity_counts[s] ?? 0;
                if (!cnt) return null;
                const pct = (cnt / severityTotal) * 100;
                const colors: Record<string, string> = { critical: "bg-red-500", severe: "bg-orange-500", moderate: "bg-yellow-500", minor: "bg-blue-500", none: "bg-emerald-500" };
                return <div key={s} className={`${colors[s]} transition-all`} style={{ width: `${pct}%` }} title={`${SEVERITY_META[s]?.label}: ${cnt}`} />;
              })}
            </div>
            <div className="flex flex-wrap gap-4 mt-3">
              {severities.map((s) => {
                const cnt = sum.severity_counts[s] ?? 0;
                if (!cnt) return null;
                const sm = SEVERITY_META[s];
                return (
                  <div key={s} className="flex items-center gap-1.5">
                    <span className={`w-2 h-2 rounded-full ${sm.dot}`} />
                    <span className="text-xs text-slate-400">{sm.label}: <span className="font-semibold text-slate-200">{cnt}</span></span>
                  </div>
                );
              })}
            </div>
          </div>
        )}

        {/* Filters */}
        <div className="flex flex-wrap gap-3">
          <div className="flex items-center gap-2 flex-wrap">
            <span className="text-xs text-slate-500 font-medium">Sévérité:</span>
            {["", ...severities].map((s) => (
              <button key={s} onClick={() => setSeverityFilter(s)}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium border transition-colors ${severityFilter === s ? "bg-indigo-600 border-indigo-500 text-white" : "bg-slate-800/50 border-slate-700 text-slate-400 hover:text-slate-200"}`}>
                {s === "" ? "Tous" : SEVERITY_META[s]?.label ?? s}
              </button>
            ))}
          </div>
          <div className="flex items-center gap-2 flex-wrap">
            <span className="text-xs text-slate-500 font-medium">Action:</span>
            {["", ...actions].map((a) => (
              <button key={a} onClick={() => setActionFilter(a)}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium border transition-colors ${actionFilter === a ? "bg-indigo-600 border-indigo-500 text-white" : "bg-slate-800/50 border-slate-700 text-slate-400 hover:text-slate-200"}`}>
                {a === "" ? "Tous" : ACTION_META[a]?.label ?? a}
              </button>
            ))}
          </div>
        </div>

        {/* Reps Grid */}
        {loading ? (
          <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
            {Array.from({ length: 6 }).map((_, i) => (
              <div key={i} className="bg-slate-800/30 border border-slate-700/30 rounded-xl h-36 animate-pulse" />
            ))}
          </div>
        ) : reps.length === 0 ? (
          <div className="text-center py-20 text-slate-500">Aucun rep correspondant aux filtres sélectionnés</div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
            {reps.map((r) => (
              <RepCard key={r.rep_id} rep={r} onClick={() => setSelected(r)} />
            ))}
          </div>
        )}
      </div>

      {selected && <GapModal rep={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
