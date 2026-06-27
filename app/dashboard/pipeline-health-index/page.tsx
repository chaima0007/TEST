"use client";

import { useEffect, useState } from "react";

// ── Types ──────────────────────────────────────────────────────────────────────
interface Pipeline {
  pipeline_id: string;
  rep_id: string;
  rep_name: string;
  region: string;
  health_grade: string;
  pipeline_risk: string;
  health_action: string;
  phi_score: number;
  velocity_score: number;
  quality_score: number;
  coverage_score: number;
  activity_score: number;
  coverage_ratio: number;
  stale_deal_pct: number;
  remediation_plays: string[];
  risk_signals: string[];
  manager_alerts: string[];
}

interface Summary {
  total: number;
  grade_counts: Record<string, number>;
  risk_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_phi_score: number;
  avg_velocity_score: number;
  avg_quality_score: number;
  avg_coverage_score: number;
  avg_activity_score: number;
  critical_count: number;
  severe_risk_count: number;
}

// ── Colour helpers ─────────────────────────────────────────────────────────────
function gradeColor(g: string) {
  return g === "excellent" ? "#22c55e"
       : g === "good"      ? "#6366f1"
       : g === "fair"      ? "#f59e0b"
       : g === "poor"      ? "#f97316"
       :                     "#ef4444"; // critical
}

function riskColor(r: string) {
  return r === "low"      ? "#22c55e"
       : r === "moderate" ? "#f59e0b"
       : r === "high"     ? "#f97316"
       :                    "#ef4444"; // severe
}

function gradeBadge(g: string) {
  const base = "text-xs px-2 py-0.5 rounded-full font-semibold";
  return g === "excellent" ? `${base} bg-emerald-500/20 text-emerald-300`
       : g === "good"      ? `${base} bg-indigo-500/20 text-indigo-300`
       : g === "fair"      ? `${base} bg-amber-500/20 text-amber-300`
       : g === "poor"      ? `${base} bg-orange-500/20 text-orange-300`
       :                     `${base} bg-red-500/20 text-red-300`;
}

function riskBadge(r: string) {
  const base = "text-xs px-2 py-0.5 rounded-full font-semibold";
  return r === "low"      ? `${base} bg-emerald-500/20 text-emerald-300`
       : r === "moderate" ? `${base} bg-amber-500/20 text-amber-300`
       : r === "high"     ? `${base} bg-orange-500/20 text-orange-300`
       :                    `${base} bg-red-500/20 text-red-300`;
}

function gradeLabel(g: string) {
  const map: Record<string, string> = {
    excellent: "Excellent", good: "Bon", fair: "Correct", poor: "Faible", critical: "Critique",
  };
  return map[g] ?? g;
}

function riskLabel(r: string) {
  const map: Record<string, string> = {
    low: "Faible", moderate: "Modéré", high: "Élevé", severe: "Sévère",
  };
  return map[r] ?? r;
}

function actionLabel(a: string) {
  const map: Record<string, string> = {
    accelerate: "Accélérer", add_pipeline: "Générer Pipeline",
    improve_qual: "Améliorer Qualification", rebalance: "Rééquilibrer",
    boost_activity: "Booster Activité", maintain: "Maintenir",
  };
  return map[a] ?? a;
}

// ── PHI Gauge SVG ──────────────────────────────────────────────────────────────
function PhiGauge({ phi, grade }: { phi: number; grade: string }) {
  const r = 30, cx = 38, cy = 38;
  const circ = 2 * Math.PI * r;
  const arc  = (phi / 100) * circ;
  const color = gradeColor(grade);
  return (
    <svg width="76" height="76" viewBox="0 0 76 76">
      <circle cx={cx} cy={cy} r={r} fill="none" stroke="#1e293b" strokeWidth="7" />
      <circle
        cx={cx} cy={cy} r={r} fill="none"
        stroke={color} strokeWidth="7"
        strokeLinecap="round"
        strokeDasharray={`${arc} ${circ - arc}`}
        transform={`rotate(-90 ${cx} ${cy})`}
      />
      <text x={cx} y={cy - 3} textAnchor="middle" fill={color} fontSize="12" fontWeight="700">
        {Math.round(phi)}
      </text>
      <text x={cx} y={cy + 10} textAnchor="middle" fill="#94a3b8" fontSize="7">
        PHI
      </text>
    </svg>
  );
}

// ── DimensionBar ───────────────────────────────────────────────────────────────
function DimensionBar({ label, score, color }: { label: string; score: number; color: string }) {
  return (
    <div className="flex items-center gap-2">
      <span className="text-xs text-slate-500 w-16">{label}</span>
      <div className="flex-1 bg-slate-700 rounded-full h-1.5 overflow-hidden">
        <div className="h-full rounded-full transition-all" style={{ width: `${score}%`, backgroundColor: color }} />
      </div>
      <span className="text-xs text-slate-400 w-6 text-right">{Math.round(score)}</span>
    </div>
  );
}

// ── GradeDistBar ───────────────────────────────────────────────────────────────
function GradeDistBar({ counts }: { counts: Record<string, number> }) {
  const total = Object.values(counts).reduce((a, b) => a + b, 0);
  if (total === 0) return null;
  const order = ["excellent", "good", "fair", "poor", "critical"];
  return (
    <div className="flex h-2.5 rounded-full overflow-hidden gap-0.5">
      {order.map((g) => {
        const pct = ((counts[g] ?? 0) / total) * 100;
        return pct > 0 ? (
          <div key={g} style={{ width: `${pct}%`, backgroundColor: gradeColor(g) }} title={`${gradeLabel(g)}: ${counts[g]}`} />
        ) : null;
      })}
    </div>
  );
}

// ── PipelineModal ──────────────────────────────────────────────────────────────
function PipelineModal({ p, onClose }: { p: Pipeline; onClose: () => void }) {
  const [tab, setTab] = useState<"plays" | "risks" | "alerts">("plays");

  useEffect(() => {
    const handler = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [onClose]);

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm"
      onClick={onClose}
    >
      <div
        className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-2xl max-h-[88vh] overflow-y-auto mx-4 shadow-2xl"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="p-6 border-b border-slate-800">
          <div className="flex items-start justify-between gap-4">
            <div>
              <h2 className="text-xl font-bold text-white">{p.rep_name}</h2>
              <p className="text-slate-400 text-sm mt-0.5">{p.region} · Pipeline Health Index</p>
            </div>
            <button onClick={onClose} className="text-slate-400 hover:text-white text-xl leading-none">✕</button>
          </div>
          <div className="flex flex-wrap gap-2 mt-4">
            <span className={gradeBadge(p.health_grade)}>{gradeLabel(p.health_grade)}</span>
            <span className={riskBadge(p.pipeline_risk)}>Risque {riskLabel(p.pipeline_risk)}</span>
            <span className="text-xs px-2 py-0.5 rounded-full bg-indigo-500/20 text-indigo-300">{actionLabel(p.health_action)}</span>
          </div>
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mt-4">
            {[
              { label: "PHI",           value: Math.round(p.phi_score),        color: "text-white" },
              { label: "Couverture",    value: `${p.coverage_ratio.toFixed(1)}×`, color: "text-emerald-400" },
              { label: "Stale %",       value: `${Math.round(p.stale_deal_pct)}%`, color: p.stale_deal_pct > 25 ? "text-red-400" : "text-slate-300" },
              { label: "Action",        value: actionLabel(p.health_action),   color: "text-indigo-400" },
            ].map((kpi) => (
              <div key={kpi.label} className="bg-slate-800/60 rounded-xl p-3 text-center">
                <p className={`text-base font-bold ${kpi.color} truncate`}>{kpi.value}</p>
                <p className="text-xs text-slate-400 mt-0.5">{kpi.label}</p>
              </div>
            ))}
          </div>
          {/* Dimension bars */}
          <div className="mt-4 space-y-2">
            <DimensionBar label="Vélocité" score={p.velocity_score} color="#6366f1" />
            <DimensionBar label="Qualité" score={p.quality_score} color="#22c55e" />
            <DimensionBar label="Couverture" score={p.coverage_score} color="#f59e0b" />
            <DimensionBar label="Activité" score={p.activity_score} color="#a78bfa" />
          </div>
        </div>

        {/* Tabs */}
        <div className="flex border-b border-slate-800">
          {(["plays", "risks", "alerts"] as const).map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`flex-1 py-3 text-sm font-medium transition-colors ${
                tab === t ? "text-indigo-400 border-b-2 border-indigo-400" : "text-slate-400 hover:text-slate-200"
              }`}
            >
              {t === "plays" ? "Plans de remédiation" : t === "risks" ? "Signaux de risque" : "Alertes manager"}
            </button>
          ))}
        </div>

        <div className="p-6 space-y-3">
          {tab === "plays" && (
            p.remediation_plays.map((play, i) => (
              <div key={i} className="flex items-start gap-3 bg-slate-800/50 rounded-xl p-3">
                <span className="text-indigo-400 text-sm font-bold mt-0.5">{i + 1}</span>
                <p className="text-slate-200 text-sm">{play}</p>
              </div>
            ))
          )}
          {tab === "risks" && (
            p.risk_signals.length > 0 ? (
              p.risk_signals.map((r, i) => (
                <div key={i} className="flex items-start gap-2 bg-amber-900/20 border border-amber-800/30 rounded-xl p-3">
                  <span className="text-amber-400 text-sm mt-0.5">!</span>
                  <p className="text-slate-200 text-sm">{r}</p>
                </div>
              ))
            ) : (
              <div className="bg-emerald-900/20 border border-emerald-800/30 rounded-xl p-4 text-center">
                <p className="text-emerald-400 text-sm font-medium">Aucun signal de risque</p>
                <p className="text-slate-400 text-xs mt-1">Pipeline en bonne santé</p>
              </div>
            )
          )}
          {tab === "alerts" && (
            p.manager_alerts.length > 0 ? (
              p.manager_alerts.map((a, i) => (
                <div key={i} className="flex items-start gap-2 bg-red-900/20 border border-red-800/40 rounded-xl p-3">
                  <span className="text-red-400 text-sm mt-0.5">⚠</span>
                  <p className="text-slate-200 text-sm">{a}</p>
                </div>
              ))
            ) : (
              <div className="bg-emerald-900/20 border border-emerald-800/30 rounded-xl p-4 text-center">
                <p className="text-emerald-400 text-sm font-medium">Aucune alerte manager</p>
                <p className="text-slate-400 text-xs mt-1">Pipeline bien géré</p>
              </div>
            )
          )}
        </div>
      </div>
    </div>
  );
}

// ── PipelineCard ───────────────────────────────────────────────────────────────
function PipelineCard({ p, onClick }: { p: Pipeline; onClick: () => void }) {
  return (
    <div
      onClick={onClick}
      className="bg-slate-800/50 border border-slate-700/50 rounded-2xl p-4 cursor-pointer hover:border-slate-500 hover:bg-slate-800 transition-all"
    >
      <div className="flex items-start gap-4">
        <PhiGauge phi={p.phi_score} grade={p.health_grade} />
        <div className="flex-1 min-w-0">
          <div className="flex items-start justify-between gap-2">
            <div>
              <h3 className="text-white font-semibold text-sm">{p.rep_name}</h3>
              <p className="text-slate-400 text-xs mt-0.5">{p.region}</p>
            </div>
            <span className={riskBadge(p.pipeline_risk)}>{riskLabel(p.pipeline_risk)}</span>
          </div>

          <div className="flex gap-2 mt-2">
            <span className={gradeBadge(p.health_grade)}>{gradeLabel(p.health_grade)}</span>
          </div>

          {/* 4 dimension mini-bars */}
          <div className="mt-3 space-y-1">
            <DimensionBar label="Vélocité" score={p.velocity_score} color="#6366f1" />
            <DimensionBar label="Qualité" score={p.quality_score} color="#22c55e" />
            <DimensionBar label="Couverture" score={p.coverage_score} color="#f59e0b" />
            <DimensionBar label="Activité" score={p.activity_score} color="#a78bfa" />
          </div>

          {/* Coverage ratio + stale */}
          <div className="flex gap-3 mt-2">
            <span className="text-xs text-slate-400">
              Couverture: <span className={p.coverage_ratio >= 2 ? "text-emerald-400" : "text-amber-400"}>
                {p.coverage_ratio.toFixed(1)}×
              </span>
            </span>
            <span className="text-xs text-slate-400">
              Stale: <span className={p.stale_deal_pct > 25 ? "text-red-400" : "text-slate-300"}>
                {Math.round(p.stale_deal_pct)}%
              </span>
            </span>
          </div>

          {/* Manager alerts */}
          {p.manager_alerts.length > 0 && (
            <div className="mt-2 flex items-center gap-1.5 bg-red-900/20 border border-red-800/30 rounded-lg px-2.5 py-1.5">
              <span className="text-red-400 text-xs">⚠</span>
              <p className="text-red-300 text-xs line-clamp-1">{p.manager_alerts[0]}</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

// ── Page ───────────────────────────────────────────────────────────────────────
export default function PipelineHealthIndexPage() {
  const [data, setData] = useState<{ pipelines: Pipeline[]; summary: Summary } | null>(null);
  const [selected, setSelected] = useState<Pipeline | null>(null);
  const [gradeFilter, setGradeFilter] = useState<string>("all");
  const [riskFilter, setRiskFilter] = useState<string>("all");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchData() {
        setLoading(true);
        try {
          const params = new URLSearchParams();
          if (gradeFilter !== "all") params.set("grade", gradeFilter);
          if (riskFilter !== "all")  params.set("risk", riskFilter);
          const res = await fetch(`/api/pipeline-health-index?${params.toString()}`);
          if (res.ok) setData(await res.json());
        } finally {
          setLoading(false);
        }
  }
    fetchData();
  }, [gradeFilter, riskFilter]);

  const s = data?.summary;

  const gradeOptions = ["all", "excellent", "good", "fair", "poor", "critical"];
  const riskOptions  = ["all", "low", "moderate", "high", "severe"];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">

        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-white">Pipeline Health Index</h1>
          <p className="text-slate-400 mt-1">Indice composite de santé pipeline · vélocité · qualité · couverture · activité</p>
        </div>

        {/* KPI strip */}
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3 mb-8">
          {[
            { label: "Pipelines analysés",  value: s?.total ?? "—",               accent: "text-white" },
            { label: "PHI moyen",            value: s ? `${s.avg_phi_score}` : "—", accent: "text-indigo-400" },
            { label: "Vélocité moy.",        value: s ? `${s.avg_velocity_score}` : "—", accent: "text-violet-400" },
            { label: "Qualité moy.",         value: s ? `${s.avg_quality_score}` : "—", accent: "text-emerald-400" },
            { label: "Pipelines critiques",  value: s?.critical_count ?? "—",      accent: "text-red-400" },
            { label: "Risque sévère",        value: s?.severe_risk_count ?? "—",   accent: "text-orange-400" },
          ].map((kpi) => (
            <div key={kpi.label} className="bg-slate-800/50 border border-slate-700/50 rounded-xl p-4">
              <p className={`text-2xl font-bold ${kpi.accent}`}>{kpi.value}</p>
              <p className="text-slate-400 text-xs mt-1">{kpi.label}</p>
            </div>
          ))}
        </div>

        {/* Grade distribution */}
        {s && (
          <div className="bg-slate-800/40 border border-slate-700/50 rounded-2xl p-5 mb-8">
            <h2 className="text-sm font-semibold text-slate-300 mb-3 uppercase tracking-wider">
              Distribution des grades de santé pipeline
            </h2>
            <GradeDistBar counts={s.grade_counts} />
            <div className="flex flex-wrap gap-3 mt-3">
              {["excellent", "good", "fair", "poor", "critical"].map((g) => (
                (s.grade_counts[g] ?? 0) > 0 && (
                  <div key={g} className="flex items-center gap-1.5">
                    <div className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: gradeColor(g) }} />
                    <span className="text-xs text-slate-400">{gradeLabel(g)} ({s.grade_counts[g]})</span>
                  </div>
                )
              ))}
            </div>
          </div>
        )}

        {/* Dimension averages */}
        {s && (
          <div className="bg-slate-800/40 border border-slate-700/50 rounded-2xl p-5 mb-8">
            <h2 className="text-sm font-semibold text-slate-300 mb-4 uppercase tracking-wider">
              Scores moyens par dimension
            </h2>
            <div className="space-y-3">
              <DimensionBar label="Vélocité" score={s.avg_velocity_score} color="#6366f1" />
              <DimensionBar label="Qualité" score={s.avg_quality_score} color="#22c55e" />
              <DimensionBar label="Couverture" score={s.avg_coverage_score} color="#f59e0b" />
              <DimensionBar label="Activité" score={s.avg_activity_score} color="#a78bfa" />
            </div>
          </div>
        )}

        {/* Filters */}
        <div className="space-y-3 mb-6">
          <div className="flex flex-wrap gap-2">
            <span className="text-xs text-slate-500 self-center mr-1">Grade :</span>
            {gradeOptions.map((g) => (
              <button
                key={g}
                onClick={() => setGradeFilter(g)}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
                  gradeFilter === g
                    ? "bg-indigo-600 text-white"
                    : "bg-slate-800 text-slate-400 hover:text-slate-200"
                }`}
              >
                {g === "all" ? "Tous" : gradeLabel(g)}
              </button>
            ))}
          </div>
          <div className="flex flex-wrap gap-2">
            <span className="text-xs text-slate-500 self-center mr-1">Risque :</span>
            {riskOptions.map((r) => (
              <button
                key={r}
                onClick={() => setRiskFilter(r)}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
                  riskFilter === r
                    ? "bg-red-600 text-white"
                    : "bg-slate-800 text-slate-400 hover:text-slate-200"
                }`}
              >
                {r === "all" ? "Tous" : riskLabel(r)}
              </button>
            ))}
          </div>
        </div>

        {/* Pipeline grid */}
        {loading ? (
          <div className="flex items-center justify-center py-20">
            <div className="w-8 h-8 border-2 border-indigo-500 border-t-transparent rounded-full animate-spin" />
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-4">
            {data?.pipelines.map((p) => (
              <PipelineCard key={p.pipeline_id} p={p} onClick={() => setSelected(p)} />
            ))}
          </div>
        )}

        {data?.pipelines.length === 0 && !loading && (
          <div className="text-center py-16 text-slate-500">
            <p className="text-lg">Aucun pipeline trouvé pour ces filtres.</p>
          </div>
        )}
      </div>

      {selected && <PipelineModal p={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
