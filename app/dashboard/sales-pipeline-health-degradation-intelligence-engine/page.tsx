"use client";

import { useEffect, useState, useCallback } from "react";

/* ── types ──────────────────────────────────────────────────────────────── */
interface Rep {
  rep_id: string;
  region: string;
  pipeline_risk: string;
  pipeline_pattern: string;
  pipeline_severity: string;
  recommended_action: string;
  staleness_score: number;
  progression_score: number;
  curation_score: number;
  concentration_score: number;
  pipeline_composite: number;
  has_pipeline_gap: boolean;
  requires_pipeline_coaching: boolean;
  estimated_phantom_pipeline_usd: number;
  pipeline_signal: string;
}

interface Summary {
  total: number;
  risk_counts: Record<string, number>;
  pattern_counts: Record<string, number>;
  severity_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_pipeline_composite: number;
  pipeline_gap_count: number;
  coaching_count: number;
  avg_staleness_score: number;
  avg_progression_score: number;
  avg_curation_score: number;
  avg_concentration_score: number;
  total_estimated_phantom_pipeline_usd: number;
}

/* ── helpers ─────────────────────────────────────────────────────────────── */
const fmtUSD = (v: number) =>
  v >= 1_000_000
    ? `$${(v / 1_000_000).toFixed(1)}M`
    : v >= 1_000
    ? `$${(v / 1_000).toFixed(0)}K`
    : `$${v.toFixed(0)}`;

const riskColor: Record<string, string> = {
  low:      "text-emerald-400",
  moderate: "text-yellow-400",
  high:     "text-orange-400",
  critical: "text-red-400",
};

const riskBorder: Record<string, string> = {
  low:      "border-emerald-500/40",
  moderate: "border-yellow-500/40",
  high:     "border-orange-500/40",
  critical: "border-red-500/40",
};

const severityBadge: Record<string, string> = {
  healthy:   "bg-emerald-900/50 text-emerald-300",
  declining: "bg-yellow-900/50 text-yellow-300",
  degraded:  "bg-orange-900/50 text-orange-300",
  critical:  "bg-red-900/50 text-red-300",
};

const patternLabel: Record<string, string> = {
  none:                     "None",
  zombie_deal_accumulation: "Zombie Deals",
  stage_stagnation:         "Stage Stagnation",
  pipeline_inflation:       "Pipeline Inflation",
  curation_avoidance:       "Curation Avoidance",
  late_stage_concentration: "Late-Stage Concentration",
};

const patternColor: Record<string, string> = {
  none:                     "bg-slate-700 text-slate-300",
  zombie_deal_accumulation: "bg-red-900/60 text-red-300",
  stage_stagnation:         "bg-orange-900/60 text-orange-300",
  pipeline_inflation:       "bg-amber-900/60 text-amber-300",
  curation_avoidance:       "bg-yellow-900/60 text-yellow-300",
  late_stage_concentration: "bg-emerald-900/60 text-emerald-300",
};

/* ── Gauge ───────────────────────────────────────────────────────────────── */
function Gauge({ label, value, color }: { label: string; value: number; color: string }) {
  const r = 36, circ = 2 * Math.PI * r;
  const dash = (value / 100) * circ;
  return (
    <div className="flex flex-col items-center gap-1">
      <svg width="96" height="96" viewBox="0 0 96 96">
        <circle cx="48" cy="48" r={r} fill="none" stroke="#1e293b" strokeWidth="8" />
        <circle
          cx="48" cy="48" r={r} fill="none"
          stroke={color} strokeWidth="8"
          strokeDasharray={`${dash} ${circ}`}
          strokeLinecap="round"
          transform="rotate(-90 48 48)"
          style={{ transition: "stroke-dasharray 0.6s ease" }}
        />
        <text x="48" y="53" textAnchor="middle" fontSize="15" fontWeight="700" fill="white">
          {value.toFixed(0)}
        </text>
      </svg>
      <span className="text-xs text-slate-400 text-center leading-tight">{label}</span>
    </div>
  );
}

/* ── DistBar ─────────────────────────────────────────────────────────────── */
function DistBar({
  title, counts, colors, total,
}: {
  title: string;
  counts: Record<string, number>;
  colors: Record<string, string>;
  total: number;
}) {
  return (
    <div className="space-y-1">
      <p className="text-xs text-slate-400 font-medium">{title}</p>
      {Object.entries(counts).map(([k, v]) => (
        <div key={k} className="flex items-center gap-2">
          <span className="text-xs text-slate-400 w-36 truncate capitalize">{k.replace(/_/g, " ")}</span>
          <div className="flex-1 bg-slate-800 rounded-full h-2">
            <div
              className="h-2 rounded-full transition-all duration-500"
              style={{ width: `${total ? (v / total) * 100 : 0}%`, background: colors[k] || "#64748b" }}
            />
          </div>
          <span className="text-xs text-slate-300 w-4 text-right">{v}</span>
        </div>
      ))}
    </div>
  );
}

/* ── DetailModal ─────────────────────────────────────────────────────────── */
function DetailModal({ rep, onClose }: { rep: Rep; onClose: () => void }) {
  const [tab, setTab] = useState<"scores" | "signal" | "action">("scores");

  useEffect(() => {
    const fn = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", fn);
    return () => window.removeEventListener("keydown", fn);
  }, [onClose]);

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm"
      onClick={onClose}
    >
      <div
        className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-xl mx-4 shadow-2xl"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="flex items-center justify-between p-5 border-b border-slate-800">
          <div>
            <p className="font-bold text-white">{rep.rep_id}</p>
            <p className="text-xs text-slate-400">{rep.region}</p>
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-white text-xl leading-none">✕</button>
        </div>

        <div className="flex border-b border-slate-800">
          {(["scores", "signal", "action"] as const).map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`flex-1 py-2 text-xs font-medium capitalize transition-colors ${
                tab === t ? "text-emerald-400 border-b-2 border-emerald-400" : "text-slate-400 hover:text-slate-200"
              }`}
            >
              {t}
            </button>
          ))}
        </div>

        <div className="p-5">
          {tab === "scores" && (
            <div className="grid grid-cols-2 gap-4">
              <div className="bg-slate-800/60 rounded-xl p-3">
                <p className="text-xs text-slate-400">Staleness Score</p>
                <p className="text-2xl font-bold text-emerald-400">{rep.staleness_score.toFixed(1)}</p>
              </div>
              <div className="bg-slate-800/60 rounded-xl p-3">
                <p className="text-xs text-slate-400">Progression Score</p>
                <p className="text-2xl font-bold text-teal-400">{rep.progression_score.toFixed(1)}</p>
              </div>
              <div className="bg-slate-800/60 rounded-xl p-3">
                <p className="text-xs text-slate-400">Curation Score</p>
                <p className="text-2xl font-bold text-green-400">{rep.curation_score.toFixed(1)}</p>
              </div>
              <div className="bg-slate-800/60 rounded-xl p-3">
                <p className="text-xs text-slate-400">Concentration Score</p>
                <p className="text-2xl font-bold text-lime-400">{rep.concentration_score.toFixed(1)}</p>
              </div>
              <div className="bg-slate-800/60 rounded-xl p-3 col-span-2">
                <p className="text-xs text-slate-400">Pipeline Composite</p>
                <p className="text-3xl font-bold text-white">{rep.pipeline_composite.toFixed(1)}</p>
              </div>
            </div>
          )}
          {tab === "signal" && (
            <div className="space-y-3">
              <div className="bg-slate-800/60 rounded-xl p-4">
                <p className="text-xs text-slate-400 mb-1">Pipeline Signal</p>
                <p className="text-sm text-slate-200 leading-relaxed">{rep.pipeline_signal}</p>
              </div>
              <div className="bg-slate-800/60 rounded-xl p-4">
                <p className="text-xs text-slate-400 mb-1">Phantom Pipeline Estimate</p>
                <p className="text-2xl font-bold text-red-400">{fmtUSD(rep.estimated_phantom_pipeline_usd)}</p>
              </div>
              <div className="flex gap-2">
                {rep.has_pipeline_gap && (
                  <span className="px-2 py-1 rounded-lg text-xs bg-red-900/50 text-red-300">🧹 PIPELINE GAP</span>
                )}
                {rep.requires_pipeline_coaching && (
                  <span className="px-2 py-1 rounded-lg text-xs bg-emerald-900/50 text-emerald-300">🧹 COACH</span>
                )}
              </div>
            </div>
          )}
          {tab === "action" && (
            <div className="space-y-3">
              <div className="bg-slate-800/60 rounded-xl p-4">
                <p className="text-xs text-slate-400 mb-1">Recommended Action</p>
                <p className="text-sm font-semibold text-emerald-300 capitalize">
                  {rep.recommended_action.replace(/_/g, " ")}
                </p>
              </div>
              <div className="bg-slate-800/60 rounded-xl p-4">
                <p className="text-xs text-slate-400 mb-1">Pattern</p>
                <p className="text-sm font-semibold text-white">{patternLabel[rep.pipeline_pattern] ?? rep.pipeline_pattern}</p>
              </div>
              <div className="bg-slate-800/60 rounded-xl p-4">
                <p className="text-xs text-slate-400 mb-1">Severity</p>
                <span className={`px-2 py-1 rounded-lg text-xs font-medium ${severityBadge[rep.pipeline_severity] ?? "bg-slate-700 text-slate-300"}`}>
                  {rep.pipeline_severity}
                </span>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

/* ── Main page ───────────────────────────────────────────────────────────── */
export default function SalesPipelineHealthDegradationPage() {
  const [data, setData]           = useState<{ reps: Rep[]; summary: Summary } | null>(null);
  const [loading, setLoading]     = useState(true);
  const [riskFilter, setRiskFilter]       = useState("all");
  const [patternFilter, setPatternFilter] = useState("all");
  const [selected, setSelected]   = useState<Rep | null>(null);

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const params = new URLSearchParams();
      if (riskFilter    !== "all") params.set("risk",    riskFilter);
      if (patternFilter !== "all") params.set("pattern", patternFilter);
      const res  = await fetch(`/api/sales-pipeline-health-degradation-intelligence-engine?${params}`);
      const json = await res.json();
      setData(json);
    } finally {
      setLoading(false);
    }
  }, [riskFilter, patternFilter]);

  useEffect(() => { load(); }, [load]);

  const s = data?.summary;

  const distributions = [
    {
      title: "Risk Distribution",
      counts: s?.risk_counts ?? {},
      colors: { low: "#34d399", moderate: "#facc15", high: "#f97316", critical: "#f87171" },
    },
    {
      title: "Pattern Distribution",
      counts: s?.pattern_counts ?? {},
      colors: {
        none:                     "#475569",
        zombie_deal_accumulation: "#f87171",
        stage_stagnation:         "#f97316",
        pipeline_inflation:       "#fbbf24",
        curation_avoidance:       "#facc15",
        late_stage_concentration: "#34d399",
      },
    },
    {
      title: "Severity Distribution",
      counts: s?.severity_counts ?? {},
      colors: { healthy: "#34d399", declining: "#facc15", degraded: "#f97316", critical: "#f87171" },
    },
    {
      title: "Action Distribution",
      counts: s?.action_counts ?? {},
      colors: {
        no_action:                      "#475569",
        pipeline_hygiene_coaching:      "#34d399",
        deal_progression_review:        "#facc15",
        pipeline_curation_workshop:     "#fbbf24",
        stage_exit_criteria_coaching:   "#f97316",
        pipeline_reset_intervention:    "#f87171",
      },
    },
  ] as Array<{ title: string; counts: Record<string, number>; colors: Record<string, string> }>;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {selected && <DetailModal rep={selected} onClose={() => setSelected(null)} />}

      {/* Header */}
      <div className="flex items-center gap-3">
        <div className="p-2 rounded-xl bg-emerald-500/10 border border-emerald-500/20">
          <svg className="w-6 h-6 text-emerald-400" fill="none" stroke="currentColor" strokeWidth="1.8" viewBox="0 0 24 24">
            <rect x="3" y="4" width="18" height="4" rx="1" strokeLinecap="round" strokeLinejoin="round"/>
            <rect x="5" y="10" width="14" height="4" rx="1" strokeLinecap="round" strokeLinejoin="round"/>
            <rect x="7" y="16" width="10" height="4" rx="1" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
        </div>
        <div>
          <h1 className="text-xl font-bold text-white">Sales Pipeline Health Degradation Intelligence</h1>
          <p className="text-xs text-slate-400">Per-rep pipeline quality decay — zombie deals, stage stagnation, inflation, curation avoidance &amp; phantom pipeline</p>
        </div>
        <button
          onClick={load}
          className="ml-auto px-3 py-1.5 text-xs rounded-lg bg-slate-800 hover:bg-slate-700 border border-slate-700 text-slate-300 transition-colors"
        >
          {loading ? "Loading…" : "Refresh"}
        </button>
      </div>

      {/* KPI strip */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {[
          { label: "Total Reps",       value: s?.total ?? "—" },
          { label: "Avg Composite",    value: s ? s.avg_pipeline_composite.toFixed(1) : "—" },
          { label: "Pipeline Gaps",    value: s?.pipeline_gap_count ?? "—" },
          { label: "Need Coaching",    value: s?.coaching_count ?? "—" },
          { label: "Phantom Pipeline", value: s ? fmtUSD(s.total_estimated_phantom_pipeline_usd) : "—" },
          { label: "Critical Risk",    value: s ? (s.risk_counts["critical"] ?? 0) : "—" },
        ].map(({ label, value }) => (
          <div key={label} className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <p className="text-xs text-slate-400">{label}</p>
            <p className="text-xl font-bold text-white mt-1">{value}</p>
          </div>
        ))}
      </div>

      {/* Gauges */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5">
        <p className="text-sm font-semibold text-slate-300 mb-4">Average Sub-Scores</p>
        <div className="flex flex-wrap justify-around gap-4">
          <Gauge label="Staleness"     value={s?.avg_staleness_score     ?? 0} color="#34d399" />
          <Gauge label="Progression"   value={s?.avg_progression_score   ?? 0} color="#2dd4bf" />
          <Gauge label="Curation"      value={s?.avg_curation_score      ?? 0} color="#4ade80" />
          <Gauge label="Concentration" value={s?.avg_concentration_score ?? 0} color="#a3e635" />
        </div>
      </div>

      {/* Distributions */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {distributions.map((d) => (
          <div key={d.title} className="bg-slate-900 border border-slate-800 rounded-2xl p-5">
            <DistBar title={d.title} counts={d.counts} colors={d.colors} total={s?.total ?? 0} />
          </div>
        ))}
      </div>

      {/* Filters */}
      <div className="flex flex-wrap gap-3">
        <div className="flex gap-1 flex-wrap">
          {["all", "low", "moderate", "high", "critical"].map((r) => (
            <button
              key={r}
              onClick={() => setRiskFilter(r)}
              className={`px-3 py-1 text-xs rounded-full border transition-colors capitalize ${
                riskFilter === r
                  ? "bg-emerald-500 text-slate-900 border-emerald-500 font-semibold"
                  : "bg-slate-800 text-slate-300 border-slate-700 hover:border-slate-500"
              }`}
            >
              {r}
            </button>
          ))}
        </div>
        <div className="flex gap-1 flex-wrap">
          {["all", "zombie_deal_accumulation", "stage_stagnation", "pipeline_inflation", "curation_avoidance", "late_stage_concentration"].map((p) => (
            <button
              key={p}
              onClick={() => setPatternFilter(p)}
              className={`px-3 py-1 text-xs rounded-full border transition-colors ${
                patternFilter === p
                  ? "bg-emerald-500 text-slate-900 border-emerald-500 font-semibold"
                  : "bg-slate-800 text-slate-300 border-slate-700 hover:border-slate-500"
              }`}
            >
              {patternLabel[p] ?? p}
            </button>
          ))}
        </div>
      </div>

      {/* Rep cards */}
      {loading ? (
        <div className="text-center py-16 text-slate-500">Loading…</div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {(data?.reps ?? []).map((rep) => (
            <button
              key={rep.rep_id}
              onClick={() => setSelected(rep)}
              className={`text-left bg-slate-900 border rounded-2xl p-5 hover:border-emerald-500/60 transition-colors space-y-3 ${riskBorder[rep.pipeline_risk] ?? "border-slate-800"}`}
            >
              <div className="flex items-center justify-between">
                <div>
                  <p className="font-semibold text-white">{rep.rep_id}</p>
                  <p className="text-xs text-slate-400">{rep.region}</p>
                </div>
                <span className={`text-xs font-bold uppercase ${riskColor[rep.pipeline_risk] ?? "text-slate-400"}`}>
                  {rep.pipeline_risk}
                </span>
              </div>

              <div className="flex items-center justify-between">
                <span className={`px-2 py-0.5 rounded-md text-xs font-medium ${patternColor[rep.pipeline_pattern] ?? "bg-slate-700 text-slate-300"}`}>
                  {patternLabel[rep.pipeline_pattern] ?? rep.pipeline_pattern}
                </span>
                <span className={`px-2 py-0.5 rounded-md text-xs font-medium ${severityBadge[rep.pipeline_severity] ?? "bg-slate-700 text-slate-300"}`}>
                  {rep.pipeline_severity}
                </span>
              </div>

              <div className="flex justify-between text-xs text-slate-400">
                <span>Composite <span className="text-white font-semibold">{rep.pipeline_composite.toFixed(1)}</span></span>
                <span>Phantom <span className="text-red-400 font-semibold">{fmtUSD(rep.estimated_phantom_pipeline_usd)}</span></span>
              </div>

              <div className="flex gap-1.5">
                {rep.has_pipeline_gap && (
                  <span className="px-1.5 py-0.5 rounded text-[10px] bg-red-900/50 text-red-300">🧹 GAP</span>
                )}
                {rep.requires_pipeline_coaching && (
                  <span className="px-1.5 py-0.5 rounded text-[10px] bg-emerald-900/50 text-emerald-300">🧹 COACH</span>
                )}
              </div>

              <p className="text-xs text-slate-500 line-clamp-2">{rep.pipeline_signal}</p>
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
