"use client";

import { useEffect, useState, useCallback } from "react";

// ── Types ─────────────────────────────────────────────────────────────────────

interface ForecastRep {
  rep_id: string;
  rep_name: string;
  manager_id: string;
  region: string;
  forecast_band: string;
  forecast_accuracy: string;
  call_reliability: string;
  forecast_action: string;
  adjusted_forecast: number;
  coverage_ratio: number;
  sandbagging_score: number;
  pipeline_health: number;
  commit_vs_quota_pct: number;
  upside_potential: number;
  is_at_risk: boolean;
  is_sandbagging: boolean;
  quota: number;
  submitted_commit: number;
  submitted_best_case: number;
  closed_won_qtd: number;
  late_stage_pipeline: number;
}

interface Summary {
  total: number;
  band_counts: Record<string, number>;
  accuracy_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_coverage_ratio: number;
  avg_pipeline_health: number;
  total_adjusted_forecast: number;
  at_risk_count: number;
  sandbagging_count: number;
  high_reliability_count: number;
  total_upside_potential: number;
  avg_sandbagging_score: number;
}

// ── Helpers ───────────────────────────────────────────────────────────────────

const BAND_COLORS: Record<string, string> = {
  best_case: "text-sky-400",
  upside: "text-emerald-400",
  commit: "text-indigo-400",
  likely: "text-amber-400",
};

const BAND_BG: Record<string, string> = {
  best_case: "bg-sky-400/10 border-sky-400/30",
  upside: "bg-emerald-400/10 border-emerald-400/30",
  commit: "bg-indigo-400/10 border-indigo-400/30",
  likely: "bg-amber-400/10 border-amber-400/30",
};

const ACCURACY_COLORS: Record<string, string> = {
  excellent: "text-emerald-400",
  good: "text-sky-400",
  fair: "text-amber-400",
  poor: "text-rose-400",
};

const RELIABILITY_COLORS: Record<string, string> = {
  high: "text-emerald-400",
  medium: "text-amber-400",
  low: "text-orange-400",
  unreliable: "text-rose-400",
};

const ACTION_STYLES: Record<string, string> = {
  commit_as_is: "bg-emerald-500/20 text-emerald-300",
  adjust_up: "bg-sky-500/20 text-sky-300",
  adjust_down: "bg-amber-500/20 text-amber-300",
  investigate: "bg-orange-500/20 text-orange-300",
  escalate: "bg-rose-500/20 text-rose-300",
};

const ACTION_LABELS: Record<string, string> = {
  commit_as_is: "Commit",
  adjust_up: "Adj. Up",
  adjust_down: "Adj. Down",
  investigate: "Investigate",
  escalate: "Escalate",
};

const BAND_LABELS: Record<string, string> = {
  best_case: "Best Case",
  upside: "Upside",
  commit: "Commit",
  likely: "Likely",
};

function fmt(n: number): string {
  if (n >= 1_000_000) return `$${(n / 1_000_000).toFixed(1)}M`;
  if (n >= 1_000) return `$${(n / 1_000).toFixed(0)}K`;
  return `$${n}`;
}

function healthColor(score: number): string {
  if (score >= 75) return "#10b981";
  if (score >= 55) return "#f59e0b";
  if (score >= 35) return "#f97316";
  return "#f43f5e";
}

function ForecastRing({ pct, size = 72 }: { pct: number; size?: number }) {
  const cx = size / 2, cy = size / 2, r = (size - 10) / 2;
  const circ = 2 * Math.PI * r;
  const arc = (Math.min(100, pct) / 100) * circ;
  const color = pct >= 100 ? "#10b981" : pct >= 80 ? "#6366f1" : pct >= 60 ? "#f59e0b" : "#f43f5e";
  return (
    <svg width={size} height={size} className="flex-shrink-0">
      <circle cx={cx} cy={cy} r={r} fill="none" stroke="#1e293b" strokeWidth={8} />
      <circle
        cx={cx} cy={cy} r={r} fill="none"
        stroke={color} strokeWidth={8}
        strokeDasharray={`${arc} ${circ - arc}`}
        strokeLinecap="round"
        transform={`rotate(-90 ${cx} ${cy})`}
      />
      <text x={cx} y={cy + 1} textAnchor="middle" dominantBaseline="middle"
        fill={color} fontSize={size < 64 ? 10 : 12} fontWeight="700">
        {pct.toFixed(0)}%
      </text>
    </svg>
  );
}

function BandDistBar({ counts }: { counts: Record<string, number> }) {
  const total = Object.values(counts).reduce((s, v) => s + v, 0) || 1;
  const bands = ["best_case", "upside", "commit", "likely"];
  const colors = ["#38bdf8", "#10b981", "#6366f1", "#f59e0b"];
  return (
    <div className="space-y-1">
      <div className="flex h-3 rounded-full overflow-hidden gap-px bg-slate-800">
        {bands.map((b, i) =>
          counts[b] ? (
            <div key={b}
              style={{ width: `${(counts[b] / total) * 100}%`, background: colors[i] }}
              title={`${BAND_LABELS[b]}: ${counts[b]}`} />
          ) : null
        )}
      </div>
      <div className="flex flex-wrap gap-x-3 gap-y-1">
        {bands.map((b, i) =>
          counts[b] ? (
            <span key={b} className="flex items-center gap-1 text-[10px] text-slate-400">
              <span className="w-2 h-2 rounded-sm" style={{ background: colors[i] }} />
              {BAND_LABELS[b]} ({counts[b]})
            </span>
          ) : null
        )}
      </div>
    </div>
  );
}

function BarMini({ value, max = 100, color }: { value: number; max?: number; color: string }) {
  const pct = Math.min(100, (value / max) * 100);
  return (
    <div className="h-1.5 bg-slate-700 rounded-full overflow-hidden">
      <div className="h-full rounded-full transition-all" style={{ width: `${pct}%`, background: color }} />
    </div>
  );
}

// ── Rep Modal ─────────────────────────────────────────────────────────────────

function RepModal({ rep, onClose }: { rep: ForecastRep; onClose: () => void }) {
  const [tab, setTab] = useState<"forecast" | "pipeline" | "reliability">("forecast");

  useEffect(() => {
    const handler = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    document.addEventListener("keydown", handler);
    return () => document.removeEventListener("keydown", handler);
  }, [onClose]);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4"
      onClick={(e) => { if (e.target === e.currentTarget) onClose(); }}>
      <div className="absolute inset-0 bg-black/60 backdrop-blur-sm" onClick={onClose} />
      <div className="relative w-full max-w-xl bg-slate-900 border border-slate-700 rounded-2xl shadow-2xl overflow-hidden">

        <div className="flex items-start justify-between p-5 border-b border-slate-800">
          <div className="flex items-center gap-4">
            <ForecastRing pct={rep.commit_vs_quota_pct} size={64} />
            <div>
              <h2 className="text-white font-bold text-lg">{rep.rep_name}</h2>
              <p className="text-slate-400 text-sm">{rep.manager_id} · {rep.region}</p>
              <div className="flex gap-2 mt-1.5 flex-wrap">
                <span className={`px-2 py-0.5 text-[11px] rounded-full border ${BAND_BG[rep.forecast_band]}`}>
                  <span className={BAND_COLORS[rep.forecast_band]}>{BAND_LABELS[rep.forecast_band]?.toUpperCase()}</span>
                </span>
                <span className={`px-2 py-0.5 text-[11px] rounded-full font-medium ${ACTION_STYLES[rep.forecast_action]}`}>
                  {ACTION_LABELS[rep.forecast_action] ?? rep.forecast_action}
                </span>
                {rep.is_sandbagging && (
                  <span className="px-2 py-0.5 text-[11px] rounded-full bg-violet-500/20 text-violet-300">Sandbagging</span>
                )}
              </div>
            </div>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-2xl leading-none p-1">×</button>
        </div>

        <div className="flex border-b border-slate-800">
          {(["forecast", "pipeline", "reliability"] as const).map((t) => (
            <button key={t} onClick={() => setTab(t)}
              className={`flex-1 py-2.5 text-xs font-semibold capitalize transition-colors ${
                tab === t ? "text-indigo-400 border-b-2 border-indigo-400" : "text-slate-500 hover:text-slate-300"
              }`}>
              {t.charAt(0).toUpperCase() + t.slice(1)}
            </button>
          ))}
        </div>

        <div className="p-5 space-y-4 max-h-80 overflow-y-auto">
          {tab === "forecast" && (
            <>
              <div className="grid grid-cols-2 gap-3">
                {[
                  { label: "Quota", value: fmt(rep.quota), color: "text-white" },
                  { label: "Submitted Commit", value: fmt(rep.submitted_commit), color: "text-indigo-400" },
                  { label: "Best Case", value: fmt(rep.submitted_best_case), color: "text-sky-400" },
                  { label: "Adjusted Forecast", value: fmt(rep.adjusted_forecast), color: "#10b981" },
                ].map(({ label, value, color }) => (
                  <div key={label} className="bg-slate-800/50 rounded-lg p-3">
                    <p className="text-slate-500 text-xs mb-0.5">{label}</p>
                    <p className="text-sm font-bold" style={{ color }}>{value}</p>
                  </div>
                ))}
              </div>
              <div>
                <div className="flex justify-between text-xs mb-1">
                  <span className="text-slate-400">Commit vs Quota</span>
                  <span className={rep.commit_vs_quota_pct >= 100 ? "text-emerald-400" : rep.commit_vs_quota_pct >= 80 ? "text-indigo-400" : "text-amber-400"}>
                    {rep.commit_vs_quota_pct.toFixed(0)}%
                  </span>
                </div>
                <BarMini value={rep.commit_vs_quota_pct} color={rep.commit_vs_quota_pct >= 100 ? "#10b981" : "#6366f1"} />
              </div>
              <div className="flex justify-between text-xs text-slate-400">
                <span>Upside potential: <span className="text-emerald-400">{fmt(rep.upside_potential)}</span></span>
                <span>Closed QTD: <span className="text-white">{fmt(rep.closed_won_qtd)}</span></span>
              </div>
            </>
          )}
          {tab === "pipeline" && (
            <>
              <div className="grid grid-cols-2 gap-3">
                {[
                  { label: "Coverage Ratio", value: `${rep.coverage_ratio.toFixed(1)}×`, color: rep.coverage_ratio >= 3 ? "text-emerald-400" : rep.coverage_ratio >= 1.5 ? "text-amber-400" : "text-rose-400" },
                  { label: "Late Stage", value: fmt(rep.late_stage_pipeline), color: "text-sky-400" },
                  { label: "Pipeline Health", value: rep.pipeline_health.toFixed(0), color: healthColor(rep.pipeline_health) },
                  { label: "At Risk", value: rep.is_at_risk ? "Yes" : "No", color: rep.is_at_risk ? "text-rose-400" : "text-emerald-400" },
                ].map(({ label, value, color }) => (
                  <div key={label} className="bg-slate-800/50 rounded-lg p-3">
                    <p className="text-slate-500 text-xs mb-0.5">{label}</p>
                    <p className={`text-sm font-bold ${color}`}>{value}</p>
                  </div>
                ))}
              </div>
              <div>
                <div className="flex justify-between text-xs mb-1">
                  <span className="text-slate-400">Pipeline Health</span>
                  <span style={{ color: healthColor(rep.pipeline_health) }}>{rep.pipeline_health.toFixed(0)}</span>
                </div>
                <BarMini value={rep.pipeline_health} color={healthColor(rep.pipeline_health)} />
              </div>
            </>
          )}
          {tab === "reliability" && (
            <>
              <div className="grid grid-cols-2 gap-3">
                {[
                  { label: "Accuracy Tier", value: rep.forecast_accuracy, color: ACCURACY_COLORS[rep.forecast_accuracy] },
                  { label: "Call Reliability", value: rep.call_reliability, color: RELIABILITY_COLORS[rep.call_reliability] },
                  { label: "Sandbagging Score", value: rep.sandbagging_score.toFixed(0), color: rep.sandbagging_score >= 50 ? "text-violet-400" : "text-slate-300" },
                  { label: "Sandbagging", value: rep.is_sandbagging ? "Detected" : "None", color: rep.is_sandbagging ? "text-violet-400" : "text-emerald-400" },
                ].map(({ label, value, color }) => (
                  <div key={label} className="bg-slate-800/50 rounded-lg p-3">
                    <p className="text-slate-500 text-xs mb-0.5">{label}</p>
                    <p className={`text-sm font-bold capitalize ${color}`}>{value}</p>
                  </div>
                ))}
              </div>
              <div>
                <div className="flex justify-between text-xs mb-1">
                  <span className="text-slate-400">Sandbagging Score</span>
                  <span className={rep.sandbagging_score >= 50 ? "text-violet-400" : "text-slate-400"}>{rep.sandbagging_score.toFixed(0)}/100</span>
                </div>
                <BarMini value={rep.sandbagging_score} color="#8b5cf6" />
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
}

// ── Rep Card ──────────────────────────────────────────────────────────────────

function RepCard({ rep, onClick }: { rep: ForecastRep; onClick: () => void }) {
  return (
    <div
      onClick={onClick}
      className="bg-slate-800/60 border border-slate-700/60 rounded-xl p-4 cursor-pointer hover:border-indigo-500/50 hover:bg-slate-800 transition-all"
    >
      <div className="flex items-start gap-3">
        <ForecastRing pct={rep.commit_vs_quota_pct} size={60} />
        <div className="flex-1 min-w-0">
          <div className="flex items-start justify-between gap-2">
            <div>
              <h3 className="text-white font-semibold text-sm truncate">{rep.rep_name}</h3>
              <p className="text-slate-500 text-xs">{rep.manager_id} · {rep.region}</p>
            </div>
            <span className={`px-2 py-0.5 text-[10px] rounded-full font-medium flex-shrink-0 ${ACTION_STYLES[rep.forecast_action]}`}>
              {ACTION_LABELS[rep.forecast_action] ?? rep.forecast_action}
            </span>
          </div>
          <div className="flex gap-2 mt-1.5 flex-wrap">
            <span className={`text-[10px] font-semibold ${BAND_COLORS[rep.forecast_band]}`}>
              {BAND_LABELS[rep.forecast_band]}
            </span>
            <span className="text-slate-600 text-[10px]">·</span>
            <span className={`text-[10px] ${ACCURACY_COLORS[rep.forecast_accuracy]}`}>
              {rep.forecast_accuracy} acc.
            </span>
            {rep.is_sandbagging && (
              <>
                <span className="text-slate-600 text-[10px]">·</span>
                <span className="text-violet-400 text-[10px] font-bold">SAND</span>
              </>
            )}
            {rep.is_at_risk && (
              <>
                <span className="text-slate-600 text-[10px]">·</span>
                <span className="text-rose-400 text-[10px] font-bold">AT RISK</span>
              </>
            )}
          </div>
        </div>
      </div>

      <div className="mt-3 space-y-1.5">
        <div>
          <div className="flex justify-between text-[10px] text-slate-500 mb-0.5">
            <span>Pipeline Health</span>
            <span style={{ color: healthColor(rep.pipeline_health) }}>{rep.pipeline_health.toFixed(0)}</span>
          </div>
          <BarMini value={rep.pipeline_health} color={healthColor(rep.pipeline_health)} />
        </div>
        <div>
          <div className="flex justify-between text-[10px] text-slate-500 mb-0.5">
            <span>Sandbagging Score</span>
            <span className="text-violet-400">{rep.sandbagging_score.toFixed(0)}</span>
          </div>
          <BarMini value={rep.sandbagging_score} color="#8b5cf6" />
        </div>
      </div>

      <div className="mt-2 flex justify-between text-[10px] text-slate-500">
        <span>Adj: <span className="text-white">{fmt(rep.adjusted_forecast)}</span></span>
        <span>Cov: <span className={rep.coverage_ratio >= 3 ? "text-emerald-400" : rep.coverage_ratio >= 1.5 ? "text-amber-400" : "text-rose-400"}>{rep.coverage_ratio.toFixed(1)}×</span></span>
      </div>
    </div>
  );
}

// ── Main Page ─────────────────────────────────────────────────────────────────

export default function SalesForecastPage() {
  const [data, setData] = useState<{ reps: ForecastRep[]; summary: Summary } | null>(null);
  const [loading, setLoading] = useState(true);
  const [selected, setSelected] = useState<ForecastRep | null>(null);
  const [filterBand, setFilterBand] = useState<string>("all");
  const [filterRegion, setFilterRegion] = useState<string>("all");

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const params = new URLSearchParams();
      if (filterBand !== "all")   params.set("band", filterBand);
      if (filterRegion !== "all") params.set("region", filterRegion);
      const res = await fetch(`/api/sales-forecast?${params}`);
      setData(await res.json());
    } finally {
      setLoading(false);
    }
  }, [filterBand, filterRegion]);

  useEffect(() => { load(); }, [load]);

  const s = data?.summary;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-white">Sales Forecast Intelligence</h1>
        <p className="text-slate-400 text-sm mt-1">Analyze forecast confidence, sandbagging signals, and pipeline health by rep</p>
      </div>

      {s && (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-6">
          {[
            { label: "Total Adj. Forecast", value: s.total_adjusted_forecast >= 1e6 ? `$${(s.total_adjusted_forecast / 1e6).toFixed(1)}M` : `$${(s.total_adjusted_forecast / 1000).toFixed(0)}K`, sub: "engine estimate", color: "text-indigo-400" },
            { label: "Total Upside", value: s.total_upside_potential >= 1e6 ? `$${(s.total_upside_potential / 1e6).toFixed(1)}M` : `$${(s.total_upside_potential / 1000).toFixed(0)}K`, sub: "potential", color: "text-emerald-400" },
            { label: "At Risk", value: s.at_risk_count, sub: `of ${s.total} reps`, color: "text-rose-400" },
            { label: "Sandbagging", value: s.sandbagging_count, sub: "detected", color: "text-violet-400" },
          ].map(({ label, value, sub, color }) => (
            <div key={label} className="bg-slate-800/60 border border-slate-700/60 rounded-xl p-4">
              <p className="text-slate-500 text-xs mb-1">{label}</p>
              <p className={`text-2xl font-bold ${color}`}>{value}</p>
              <p className="text-slate-600 text-xs">{sub}</p>
            </div>
          ))}
        </div>
      )}

      {s && (
        <div className="bg-slate-800/60 border border-slate-700/60 rounded-xl p-4 mb-6">
          <p className="text-slate-400 text-xs font-semibold uppercase tracking-wider mb-3">Forecast Band Distribution</p>
          <BandDistBar counts={s.band_counts} />
          <div className="mt-3 grid grid-cols-3 gap-2">
            {[
              { label: "Avg Coverage", value: `${s.avg_coverage_ratio}×`, color: "text-sky-400" },
              { label: "Avg Health", value: s.avg_pipeline_health, color: "text-amber-400" },
              { label: "High Reliability", value: s.high_reliability_count, color: "text-emerald-400" },
            ].map(({ label, value, color }) => (
              <div key={label} className="text-center">
                <p className={`text-lg font-bold ${color}`}>{value}</p>
                <p className="text-slate-500 text-[10px]">{label}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      <div className="flex flex-wrap gap-3 mb-5">
        <div className="flex gap-1 flex-wrap">
          <span className="text-slate-500 text-xs self-center mr-1">Band:</span>
          {["all", "best_case", "upside", "commit", "likely"].map((b) => (
            <button key={b} onClick={() => setFilterBand(b)}
              className={`px-3 py-1 text-xs rounded-full border transition-colors ${
                filterBand === b
                  ? "border-indigo-500 bg-indigo-500/20 text-indigo-300"
                  : "border-slate-700 text-slate-400 hover:border-slate-500"
              }`}>
              {b === "all" ? "All" : (BAND_LABELS[b] ?? b)}
            </button>
          ))}
        </div>
        <div className="flex gap-1 flex-wrap">
          <span className="text-slate-500 text-xs self-center mr-1">Region:</span>
          {["all", "EMEA", "NAMER", "APAC", "LATAM"].map((r) => (
            <button key={r} onClick={() => setFilterRegion(r)}
              className={`px-3 py-1 text-xs rounded-full border transition-colors ${
                filterRegion === r
                  ? "border-violet-500 bg-violet-500/20 text-violet-300"
                  : "border-slate-700 text-slate-400 hover:border-slate-500"
              }`}>
              {r === "all" ? "All" : r}
            </button>
          ))}
        </div>
      </div>

      {loading ? (
        <div className="flex justify-center py-20 text-slate-500">Loading…</div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
          {data?.reps.map((r) => (
            <RepCard key={r.rep_id} rep={r} onClick={() => setSelected(r)} />
          ))}
        </div>
      )}

      {selected && <RepModal rep={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
