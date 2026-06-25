"use client";

import { useState, useEffect, useRef } from "react";

interface RepData {
  rep_id: string;
  rep_name: string;
  region: string;
  quarter: string;
  calibration_rating: string;
  calibration_risk: string;
  bias_type: string;
  calibration_action: string;
  accuracy_score: number;
  bias_score: number;
  consistency_score: number;
  data_quality_score: number;
  calibration_composite: number;
  is_sandbagging: boolean;
  is_over_optimistic: boolean;
  estimated_forecast_error_usd: number;
  calibration_signal: string;
  forecasted_amount_usd: number;
}

interface Summary {
  total: number;
  calibration_counts: Record<string, number>;
  risk_counts: Record<string, number>;
  bias_type_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_calibration_composite: number;
  sandbagging_count: number;
  over_optimistic_count: number;
  avg_accuracy_score: number;
  avg_bias_score: number;
  avg_consistency_score: number;
  avg_data_quality_score: number;
  total_forecast_error_exposure_usd: number;
}

const RATING_BG: Record<string, string> = {
  excellent: "bg-emerald-500/20 border-emerald-500/30 text-emerald-300",
  good:      "bg-sky-500/20 border-sky-500/30 text-sky-300",
  fair:      "bg-amber-500/20 border-amber-500/30 text-amber-300",
  poor:      "bg-rose-500/20 border-rose-500/30 text-rose-300",
};
const RATING_COLOR: Record<string, string> = {
  excellent: "#34d399",
  good:      "#38bdf8",
  fair:      "#fbbf24",
  poor:      "#f87171",
};
const RISK_BG: Record<string, string> = {
  low:      "bg-emerald-500/15 text-emerald-300",
  moderate: "bg-amber-500/15 text-amber-300",
  high:     "bg-orange-500/15 text-orange-300",
  critical: "bg-rose-500/15 text-rose-300",
};
const BIAS_BG: Record<string, string> = {
  accurate:       "bg-emerald-500/15 text-emerald-300",
  sandbagging:    "bg-violet-500/15 text-violet-300",
  over_optimistic:"bg-rose-500/15 text-rose-300",
  inconsistent:   "bg-amber-500/15 text-amber-300",
};

function fmt(n: number) {
  return n >= 1_000_000
    ? `$${(n / 1_000_000).toFixed(1)}M`
    : n >= 1_000
    ? `$${(n / 1_000).toFixed(0)}K`
    : `$${n}`;
}

function Ring({ value, color, size = 80, inverted = false }: { value: number; color: string; size?: number; inverted?: boolean }) {
  const displayValue = inverted ? 100 - value : value;
  const r = size * 0.38;
  const circ = 2 * Math.PI * r;
  const fill = (displayValue / 100) * circ;
  return (
    <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`}>
      <circle cx={size / 2} cy={size / 2} r={r} fill="none" stroke="#1e293b" strokeWidth={size * 0.1} />
      <circle
        cx={size / 2} cy={size / 2} r={r} fill="none"
        stroke={color} strokeWidth={size * 0.1}
        strokeDasharray={`${fill} ${circ - fill}`}
        strokeLinecap="round"
        transform={`rotate(-90 ${size / 2} ${size / 2})`}
      />
      <text x={size / 2} y={size / 2 + 5} textAnchor="middle" fill={color} fontSize={size * 0.2} fontWeight="bold">
        {value.toFixed(0)}
      </text>
    </svg>
  );
}

function DetailModal({ rep, onClose }: { rep: RepData; onClose: () => void }) {
  const [tab, setTab] = useState(0);
  const backdrop = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handler = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [onClose]);

  const color = RATING_COLOR[rep.calibration_rating] ?? "#94a3b8";

  return (
    <div
      ref={backdrop}
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm"
      onClick={(e) => { if (e.target === backdrop.current) onClose(); }}
    >
      <div className="relative w-full max-w-2xl rounded-2xl border border-slate-700 bg-slate-900 shadow-2xl mx-4">
        <button onClick={onClose} className="absolute top-4 right-4 text-slate-400 hover:text-white transition-colors text-xl font-bold">✕</button>

        <div className="p-6 border-b border-slate-800">
          <div className="flex items-center gap-4">
            <Ring value={rep.calibration_composite} color={color} size={72} />
            <div>
              <h2 className="text-xl font-bold text-slate-100">{rep.rep_name}</h2>
              <p className="text-slate-400 text-sm mt-0.5">{rep.region} · {rep.quarter}</p>
              <div className="flex gap-2 mt-2 flex-wrap">
                <span className={`px-2 py-0.5 rounded-full border text-xs font-semibold uppercase tracking-wide ${RATING_BG[rep.calibration_rating]}`}>
                  {rep.calibration_rating}
                </span>
                <span className={`px-2 py-0.5 rounded-full text-xs font-semibold ${BIAS_BG[rep.bias_type]}`}>
                  {rep.bias_type.replace("_", " ")}
                </span>
                {rep.is_sandbagging && (
                  <span className="px-2 py-0.5 rounded-full bg-violet-500/20 text-violet-300 text-xs font-semibold">SANDBAGGING</span>
                )}
                {rep.is_over_optimistic && (
                  <span className="px-2 py-0.5 rounded-full bg-rose-500/20 text-rose-300 text-xs font-semibold">OVER-OPTIMISTIC</span>
                )}
              </div>
            </div>
          </div>
        </div>

        <div className="flex border-b border-slate-800">
          {["Scores", "Forecast Analysis", "Action"].map((t, i) => (
            <button
              key={t} onClick={() => setTab(i)}
              className={`flex-1 px-4 py-3 text-sm font-medium transition-colors ${tab === i ? "text-indigo-400 border-b-2 border-indigo-400" : "text-slate-500 hover:text-slate-300"}`}
            >{t}</button>
          ))}
        </div>

        <div className="p-6">
          {tab === 0 && (
            <div className="grid grid-cols-2 gap-4">
              {[
                { label: "Accuracy", value: rep.accuracy_score, color: "#34d399" },
                { label: "Consistency", value: rep.consistency_score, color: "#818cf8" },
                { label: "Data Quality", value: rep.data_quality_score, color: "#38bdf8" },
                { label: "Bias (lower=better)", value: rep.bias_score, color: "#f87171" },
              ].map(({ label, value, color }) => (
                <div key={label} className="bg-slate-800/50 rounded-xl p-4">
                  <p className="text-slate-400 text-xs mb-2">{label}</p>
                  <div className="flex items-center gap-3">
                    <div className="flex-1 h-2 bg-slate-700 rounded-full overflow-hidden">
                      <div className="h-full rounded-full" style={{ width: `${value}%`, backgroundColor: color }} />
                    </div>
                    <span className="text-slate-200 text-sm font-bold w-10 text-right">{value.toFixed(1)}</span>
                  </div>
                </div>
              ))}
              <div className="col-span-2 bg-slate-800/30 rounded-xl p-4">
                <p className="text-slate-400 text-xs mb-1">Calibration Signal</p>
                <p className="text-slate-200 text-sm">{rep.calibration_signal}</p>
              </div>
            </div>
          )}
          {tab === 1 && (
            <div className="space-y-3">
              <div className="grid grid-cols-2 gap-3">
                <div className="bg-slate-800/50 rounded-xl p-4">
                  <p className="text-slate-400 text-xs mb-1">Forecasted Amount</p>
                  <p className="text-slate-100 text-lg font-bold">{fmt(rep.forecasted_amount_usd)}</p>
                </div>
                <div className="bg-slate-800/50 rounded-xl p-4">
                  <p className="text-slate-400 text-xs mb-1">Forecast Error Exposure</p>
                  <p className="text-rose-400 text-lg font-bold">{fmt(rep.estimated_forecast_error_usd)}</p>
                </div>
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div className={`rounded-xl p-3 text-center ${RISK_BG[rep.calibration_risk]}`}>
                  <p className="text-xs opacity-70 mb-1">Risk Level</p>
                  <p className="text-sm font-bold uppercase">{rep.calibration_risk}</p>
                </div>
                <div className={`rounded-xl p-3 text-center ${BIAS_BG[rep.bias_type]}`}>
                  <p className="text-xs opacity-70 mb-1">Bias Type</p>
                  <p className="text-sm font-bold">{rep.bias_type.replace("_", " ")}</p>
                </div>
              </div>
            </div>
          )}
          {tab === 2 && (
            <div className="space-y-4">
              <div className="bg-indigo-500/10 border border-indigo-500/20 rounded-xl p-4">
                <p className="text-indigo-400 text-xs font-semibold uppercase tracking-wide mb-2">Recommended Action</p>
                <p className="text-slate-200 font-semibold text-base">
                  {rep.calibration_action.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase())}
                </p>
              </div>
              <div className="bg-slate-800/30 rounded-xl p-4 space-y-2">
                <div className="flex justify-between text-sm">
                  <span className="text-slate-400">Calibration Rating</span>
                  <span className="font-semibold" style={{ color: RATING_COLOR[rep.calibration_rating] }}>
                    {rep.calibration_rating.toUpperCase()}
                  </span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-slate-400">Sandbagging Flag</span>
                  <span className={rep.is_sandbagging ? "text-violet-400 font-semibold" : "text-slate-500"}>
                    {rep.is_sandbagging ? "YES" : "No"}
                  </span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-slate-400">Over-Optimistic Flag</span>
                  <span className={rep.is_over_optimistic ? "text-rose-400 font-semibold" : "text-slate-500"}>
                    {rep.is_over_optimistic ? "YES" : "No"}
                  </span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-slate-400">Composite Score</span>
                  <span className="text-slate-200 font-semibold">{rep.calibration_composite.toFixed(1)}</span>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default function ForecastCalibrationPage() {
  const [data, setData] = useState<{ reps: RepData[]; summary: Summary } | null>(null);
  const [loading, setLoading] = useState(true);
  const [ratingFilter, setRatingFilter] = useState<string>("all");
  const [biasFilter, setBiasFilter] = useState<string>("all");
  const [selected, setSelected] = useState<RepData | null>(null);

  async function load() {
      setLoading(true);
      try {
        const params = new URLSearchParams();
        if (ratingFilter !== "all") params.set("rating", ratingFilter);
        if (biasFilter !== "all") params.set("bias", biasFilter);
        const res = await fetch(`/api/forecast-calibration-engine?${params}`);
        setData(await res.json());
      } finally {
        setLoading(false);
      }
  }

  useEffect(() => {
    load();
  }, [ratingFilter, biasFilter]);

  const s = data?.summary;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
      <div className="max-w-7xl mx-auto space-y-6">

        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-slate-100">Forecast Calibration Engine</h1>
            <p className="text-slate-400 mt-1">Detect sandbagging, over-optimism, and CRM data quality issues</p>
          </div>
          <button onClick={load} className="px-4 py-2 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white text-sm font-medium transition-colors">
            Refresh
          </button>
        </div>

        {s && (
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
            {[
              { label: "Avg Calibration Score", value: s.avg_calibration_composite.toFixed(1), sub: "composite", color: "text-indigo-400" },
              { label: "Sandbagging Reps", value: s.sandbagging_count, sub: `of ${s.total} total`, color: "text-violet-400" },
              { label: "Over-Optimistic Reps", value: s.over_optimistic_count, sub: `of ${s.total} total`, color: "text-rose-400" },
              { label: "Total Error Exposure", value: fmt(s.total_forecast_error_exposure_usd), sub: "this quarter", color: "text-amber-400" },
            ].map(({ label, value, sub, color }) => (
              <div key={label} className="bg-slate-900 border border-slate-800 rounded-2xl p-4">
                <p className="text-slate-400 text-xs mb-1">{label}</p>
                <p className={`text-2xl font-bold ${color}`}>{value}</p>
                <p className="text-slate-500 text-xs mt-1">{sub}</p>
              </div>
            ))}
          </div>
        )}

        {s && (
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5">
            <h2 className="text-sm font-semibold text-slate-400 uppercase tracking-wide mb-4">Average Score Breakdown</h2>
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
              {[
                { label: "Accuracy", value: s.avg_accuracy_score, color: "#34d399" },
                { label: "Consistency", value: s.avg_consistency_score, color: "#818cf8" },
                { label: "Data Quality", value: s.avg_data_quality_score, color: "#38bdf8" },
                { label: "Bias (lower=better)", value: s.avg_bias_score, color: "#f87171" },
              ].map(({ label, value, color }) => (
                <div key={label} className="flex flex-col items-center gap-2">
                  <Ring value={value} color={color} size={80} />
                  <p className="text-slate-400 text-xs text-center">{label}</p>
                </div>
              ))}
            </div>
          </div>
        )}

        {s && (
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5">
            <h2 className="text-sm font-semibold text-slate-400 uppercase tracking-wide mb-3">Calibration Distribution</h2>
            <div className="flex h-5 rounded-full overflow-hidden gap-0.5">
              {(["excellent", "good", "fair", "poor"] as const).map((r) => {
                const pct = ((s.calibration_counts[r] || 0) / s.total) * 100;
                const cols: Record<string, string> = { excellent: "bg-emerald-500", good: "bg-sky-500", fair: "bg-amber-500", poor: "bg-rose-500" };
                return pct > 0 ? (
                  <div key={r} style={{ width: `${pct}%` }} className={`${cols[r]} relative group`}>
                    <div className="absolute bottom-full mb-1 left-1/2 -translate-x-1/2 bg-slate-800 text-xs rounded px-2 py-1 whitespace-nowrap opacity-0 group-hover:opacity-100 transition-opacity z-10">
                      {r}: {s.calibration_counts[r]}
                    </div>
                  </div>
                ) : null;
              })}
            </div>
            <div className="flex flex-wrap gap-3 mt-3">
              {(["excellent", "good", "fair", "poor"] as const).map((r) => {
                const dot: Record<string, string> = { excellent: "bg-emerald-500", good: "bg-sky-500", fair: "bg-amber-500", poor: "bg-rose-500" };
                return (
                  <div key={r} className="flex items-center gap-1.5">
                    <div className={`w-2.5 h-2.5 rounded-full ${dot[r]}`} />
                    <span className="text-slate-400 text-xs">{r} ({s.calibration_counts[r] || 0})</span>
                  </div>
                );
              })}
            </div>
          </div>
        )}

        <div className="flex flex-wrap gap-3">
          <div className="flex gap-1 bg-slate-900 border border-slate-800 rounded-xl p-1">
            {["all", "excellent", "good", "fair", "poor"].map((r) => (
              <button
                key={r} onClick={() => setRatingFilter(r)}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${ratingFilter === r ? "bg-indigo-600 text-white" : "text-slate-400 hover:text-slate-200"}`}
              >
                {r === "all" ? "All Ratings" : r}
              </button>
            ))}
          </div>
          <div className="flex gap-1 bg-slate-900 border border-slate-800 rounded-xl p-1">
            {["all", "accurate", "sandbagging", "over_optimistic", "inconsistent"].map((b) => (
              <button
                key={b} onClick={() => setBiasFilter(b)}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${biasFilter === b ? "bg-indigo-600 text-white" : "text-slate-400 hover:text-slate-200"}`}
              >
                {b === "all" ? "All Bias" : b.replace("_", " ")}
              </button>
            ))}
          </div>
        </div>

        {loading ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {Array.from({ length: 8 }).map((_, i) => (
              <div key={i} className="bg-slate-900 border border-slate-800 rounded-2xl p-5 animate-pulse h-52" />
            ))}
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {(data?.reps ?? []).map((rep) => {
              const color = RATING_COLOR[rep.calibration_rating] ?? "#94a3b8";
              return (
                <button
                  key={rep.rep_id}
                  onClick={() => setSelected(rep)}
                  className="bg-slate-900 border border-slate-800 rounded-2xl p-5 text-left hover:border-indigo-500/50 transition-all hover:bg-slate-800/50 group"
                >
                  <div className="flex items-center justify-between mb-3">
                    <div>
                      <p className="text-slate-100 font-semibold text-sm">{rep.rep_name}</p>
                      <p className="text-slate-400 text-xs">{rep.region}</p>
                    </div>
                    <Ring value={rep.calibration_composite} color={color} size={52} />
                  </div>
                  <div className="flex flex-wrap gap-1.5 mb-3">
                    <span className={`px-2 py-0.5 rounded-full border text-xs font-semibold ${RATING_BG[rep.calibration_rating]}`}>
                      {rep.calibration_rating}
                    </span>
                    <span className={`px-2 py-0.5 rounded-full text-xs font-semibold ${BIAS_BG[rep.bias_type]}`}>
                      {rep.bias_type.replace("_", " ")}
                    </span>
                  </div>
                  {(rep.is_sandbagging || rep.is_over_optimistic) && (
                    <div className={`text-xs font-semibold px-2 py-1 rounded-lg mb-2 ${rep.is_sandbagging ? "bg-violet-500/15 text-violet-300" : "bg-rose-500/15 text-rose-300"}`}>
                      {rep.is_sandbagging ? "Sandbagging detected" : "Over-optimistic forecast"}
                    </div>
                  )}
                  <div className="flex justify-between text-xs text-slate-400 mb-1">
                    <span>Forecast: {fmt(rep.forecasted_amount_usd)}</span>
                    <span className="text-rose-400">Error: {fmt(rep.estimated_forecast_error_usd)}</span>
                  </div>
                  <p className="text-slate-500 text-xs mt-1 line-clamp-2 group-hover:text-slate-400 transition-colors">
                    {rep.calibration_signal}
                  </p>
                </button>
              );
            })}
          </div>
        )}
      </div>

      {selected && <DetailModal rep={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
