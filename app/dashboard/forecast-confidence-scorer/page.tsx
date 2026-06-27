"use client";

import { useEffect, useState } from "react";

// ── types ────────────────────────────────────────────────────────────────────
interface Rep {
  rep_id: string;
  rep_name: string;
  manager_id: string;
  confidence_level: string;
  forecast_pattern: string;
  pipeline_health: string;
  forecast_action: string;
  historical_accuracy_score: number;
  pipeline_coverage_score: number;
  deal_quality_score: number;
  activity_signal_score: number;
  forecast_composite: number;
  attainment_probability: number;
  pipeline_coverage_ratio: number;
  is_forecast_reliable: boolean;
  needs_forecast_scrub: boolean;
  region: string;
}

interface Summary {
  total: number;
  confidence_counts: Record<string, number>;
  pattern_counts: Record<string, number>;
  pipeline_health_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_forecast_composite: number;
  avg_attainment_probability: number;
  reliable_count: number;
  scrub_count: number;
  avg_historical_accuracy_score: number;
  avg_pipeline_coverage_score: number;
  avg_deal_quality_score: number;
  avg_activity_signal_score: number;
}

// ── helpers ──────────────────────────────────────────────────────────────────
const CONF_COLOR: Record<string, string> = {
  committed: "text-emerald-400",
  high:      "text-sky-400",
  moderate:  "text-amber-400",
  low:       "text-rose-400",
};
const CONF_BG: Record<string, string> = {
  committed: "bg-emerald-500/20 border-emerald-500/40",
  high:      "bg-sky-500/20 border-sky-500/40",
  moderate:  "bg-amber-500/20 border-amber-500/40",
  low:       "bg-rose-500/20 border-rose-500/40",
};
const PATTERN_ICON: Record<string, string> = {
  reliable:        "✅",
  optimistic_bias: "🌈",
  sandbagging:     "🙈",
  volatile:        "🌪️",
  insufficient:    "⚠️",
};

function ConfidenceRing({ score, color }: { score: number; color: string }) {
  const r = 36, circ = 2 * Math.PI * r;
  const fill = (score / 100) * circ;
  return (
    <svg width={88} height={88} viewBox="0 0 88 88">
      <circle cx={44} cy={44} r={r} fill="none" stroke="#1e293b" strokeWidth={8} />
      <circle
        cx={44} cy={44} r={r} fill="none"
        stroke={color} strokeWidth={8}
        strokeDasharray={`${fill} ${circ}`}
        strokeLinecap="round"
        transform="rotate(-90 44 44)"
      />
      <text x={44} y={49} textAnchor="middle" fill="white" fontSize={14} fontWeight="bold">
        {Math.round(score)}
      </text>
    </svg>
  );
}

function ScoreBar({ label, value, color }: { label: string; value: number; color: string }) {
  return (
    <div>
      <div className="flex justify-between text-xs text-slate-400 mb-1">
        <span>{label}</span><span>{value.toFixed(1)}</span>
      </div>
      <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
        <div className={`h-full rounded-full ${color}`} style={{ width: `${value}%` }} />
      </div>
    </div>
  );
}

function ConfDistBar({ counts }: { counts: Record<string, number> }) {
  const order = ["committed", "high", "moderate", "low"];
  const colors = ["bg-emerald-500", "bg-sky-500", "bg-amber-500", "bg-rose-500"];
  const total = Object.values(counts).reduce((a, b) => a + b, 0) || 1;
  return (
    <div className="flex gap-1 h-3 rounded-full overflow-hidden">
      {order.map((k, i) => (
        <div
          key={k}
          className={colors[i]}
          style={{ width: `${((counts[k] || 0) / total) * 100}%` }}
          title={`${k}: ${counts[k] || 0}`}
        />
      ))}
    </div>
  );
}

// ── RepModal ─────────────────────────────────────────────────────────────────
function RepModal({ rep, onClose }: { rep: Rep; onClose: () => void }) {
  const [tab, setTab] = useState<"signals" | "scores" | "actions">("signals");

  useEffect(() => {
    const esc = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", esc);
    return () => window.removeEventListener("keydown", esc);
  }, [onClose]);

  const ringColor =
    rep.forecast_composite >= 75 ? "#10b981"
    : rep.forecast_composite >= 60 ? "#38bdf8"
    : rep.forecast_composite >= 40 ? "#f59e0b"
    : "#f43f5e";

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4"
      onClick={onClose}
    >
      <div
        className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-lg shadow-2xl"
        onClick={(e) => e.stopPropagation()}
      >
        {/* header */}
        <div className="flex items-center gap-4 p-5 border-b border-slate-800">
          <ConfidenceRing score={rep.forecast_composite} color={ringColor} />
          <div className="flex-1 min-w-0">
            <h2 className="text-white font-bold text-lg truncate">{rep.rep_name}</h2>
            <p className="text-slate-400 text-sm">{rep.rep_id} · {rep.region}</p>
            <div className="flex gap-2 mt-1 flex-wrap">
              <span className={`text-xs px-2 py-0.5 rounded-full border ${CONF_BG[rep.confidence_level]}`}>
                {rep.confidence_level}
              </span>
              <span className="text-xs text-slate-400">
                {PATTERN_ICON[rep.forecast_pattern]} {rep.forecast_pattern.replace(/_/g, " ")}
              </span>
            </div>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl">✕</button>
        </div>

        {/* tabs */}
        <div className="flex border-b border-slate-800">
          {(["signals", "scores", "actions"] as const).map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`flex-1 py-2.5 text-sm font-medium capitalize transition-colors ${
                tab === t ? "text-indigo-400 border-b-2 border-indigo-400" : "text-slate-500 hover:text-slate-300"
              }`}
            >
              {t}
            </button>
          ))}
        </div>

        <div className="p-5 space-y-3">
          {tab === "signals" && (
            <>
              <div className="grid grid-cols-2 gap-3">
                {[
                  ["Pipeline Coverage", rep.pipeline_coverage_ratio.toFixed(1) + "×"],
                  ["Pipeline Health", rep.pipeline_health.replace(/_/g, " ")],
                  ["Forecast Reliable", rep.is_forecast_reliable ? "✅ Yes" : "❌ No"],
                  ["Needs Scrub", rep.needs_forecast_scrub ? "⚠️ Yes" : "✅ No"],
                ].map(([label, value]) => (
                  <div key={label as string} className="bg-slate-800/60 rounded-lg p-3">
                    <div className="text-xs text-slate-400">{label}</div>
                    <div className="text-white font-semibold mt-0.5">{value}</div>
                  </div>
                ))}
              </div>
              <div className="bg-slate-800/60 rounded-lg p-3">
                <div className="text-xs text-slate-400 mb-1">Attainment Probability</div>
                <div className="flex items-center gap-3">
                  <span className="text-2xl font-bold text-white">{rep.attainment_probability.toFixed(1)}%</span>
                  <div className="flex-1 h-2 bg-slate-700 rounded-full">
                    <div
                      className="h-full rounded-full"
                      style={{ width: `${rep.attainment_probability}%`, backgroundColor: ringColor }}
                    />
                  </div>
                </div>
              </div>
            </>
          )}

          {tab === "scores" && (
            <div className="space-y-3">
              <ScoreBar label="Historical Accuracy" value={rep.historical_accuracy_score} color="bg-indigo-500" />
              <ScoreBar label="Pipeline Coverage"   value={rep.pipeline_coverage_score}   color="bg-violet-500" />
              <ScoreBar label="Deal Quality"        value={rep.deal_quality_score}         color="bg-sky-500" />
              <ScoreBar label="Activity Signal"     value={rep.activity_signal_score}      color="bg-amber-500" />
            </div>
          )}

          {tab === "actions" && (
            <div className="space-y-3">
              <div className="bg-indigo-500/10 border border-indigo-500/30 rounded-xl p-4">
                <div className="text-xs text-indigo-400 uppercase tracking-wide mb-1">Forecast Action</div>
                <div className="text-white font-bold text-lg capitalize">
                  {rep.forecast_action.replace(/_/g, " ")}
                </div>
              </div>
              {rep.needs_forecast_scrub && (
                <div className="bg-rose-500/10 border border-rose-500/30 rounded-xl p-3 text-sm text-rose-300">
                  🔍 Forecast scrub required — pipeline quality or slip rate needs review
                </div>
              )}
              {rep.forecast_pattern === "sandbagging" && (
                <div className="bg-amber-500/10 border border-amber-500/30 rounded-xl p-3 text-sm text-amber-300">
                  🙈 Sandbagging detected — coach rep to commit full potential
                </div>
              )}
              {rep.confidence_level === "committed" && (
                <div className="bg-emerald-500/10 border border-emerald-500/30 rounded-xl p-3 text-sm text-emerald-300">
                  🎯 High-confidence committed forecast — protect deal momentum
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

// ── RepCard ───────────────────────────────────────────────────────────────────
function RepCard({ rep, onClick }: { rep: Rep; onClick: () => void }) {
  const ringColor =
    rep.forecast_composite >= 75 ? "#10b981"
    : rep.forecast_composite >= 60 ? "#38bdf8"
    : rep.forecast_composite >= 40 ? "#f59e0b"
    : "#f43f5e";

  return (
    <div
      onClick={onClick}
      className="bg-slate-900 border border-slate-800 rounded-xl p-4 cursor-pointer hover:border-indigo-500/50 hover:bg-slate-800/60 transition-all"
    >
      <div className="flex items-center gap-3">
        <ConfidenceRing score={rep.forecast_composite} color={ringColor} />
        <div className="flex-1 min-w-0">
          <div className="text-white font-semibold truncate">{rep.rep_name}</div>
          <div className="text-slate-400 text-xs">{rep.rep_id} · {rep.region}</div>
          <div className="flex gap-2 mt-1 flex-wrap">
            <span className={`text-xs px-2 py-0.5 rounded-full border ${CONF_BG[rep.confidence_level]}`}>
              {rep.confidence_level}
            </span>
            <span className="text-xs text-slate-400">
              {PATTERN_ICON[rep.forecast_pattern]}
            </span>
          </div>
        </div>
        <div className="text-right shrink-0">
          <div className={`text-sm font-bold ${CONF_COLOR[rep.confidence_level]}`}>
            {rep.attainment_probability.toFixed(0)}%
          </div>
          <div className="text-xs text-slate-500">attain</div>
          {rep.needs_forecast_scrub && (
            <div className="text-xs text-rose-400 mt-1">🔍 scrub</div>
          )}
        </div>
      </div>
      <div className="mt-3 text-xs text-slate-400">
        Pipeline: {rep.pipeline_coverage_ratio.toFixed(1)}× · {rep.pipeline_health.replace(/_/g, " ")}
      </div>
    </div>
  );
}

// ── page ─────────────────────────────────────────────────────────────────────
export default function ForecastConfidenceScorerPage() {
  const [reps, setReps]         = useState<Rep[]>([]);
  const [summary, setSummary]   = useState<Summary | null>(null);
  const [loading, setLoading]   = useState(true);
  const [selected, setSelected] = useState<Rep | null>(null);
  const [filterConf,   setFilterConf]   = useState("all");
  const [filterRegion, setFilterRegion] = useState("all");

  useEffect(() => {
    async function load() {
        setLoading(true);
        const params = new URLSearchParams();
        if (filterConf   !== "all") params.set("confidence", filterConf);
        if (filterRegion !== "all") params.set("region", filterRegion);
        const res = await fetch(`/api/forecast-confidence-scorer?${params}`);
        const data = await res.json();
        setReps(data.reps);
        setSummary(data.summary);
        setLoading(false);
  }
    load();
  }, [filterConf, filterRegion]);

  const scrubQueue = reps.filter((r) => r.needs_forecast_scrub);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
      <div className="max-w-6xl mx-auto space-y-6">

        {/* header */}
        <div>
          <h1 className="text-2xl font-bold text-white">Forecast Confidence Scorer</h1>
          <p className="text-slate-400 text-sm mt-1">
            Scores rep forecast reliability by historical accuracy, pipeline coverage, deal quality, and activity
          </p>
        </div>

        {/* scrub alert */}
        {scrubQueue.length > 0 && (
          <div className="bg-rose-500/10 border border-rose-500/30 rounded-xl p-4 flex items-center gap-3">
            <span className="text-2xl">🔍</span>
            <div>
              <div className="text-rose-300 font-semibold">
                {scrubQueue.length} forecast{scrubQueue.length > 1 ? "s" : ""} require scrub
              </div>
              <div className="text-rose-400/70 text-xs mt-0.5">
                {scrubQueue.map((r) => r.rep_name).join(" · ")}
              </div>
            </div>
          </div>
        )}

        {/* KPI strip */}
        {summary && (
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
            {[
              { label: "Total Reps",       value: summary.total },
              { label: "Reliable",         value: summary.reliable_count,         color: "text-emerald-400" },
              { label: "Need Scrub",       value: summary.scrub_count,            color: "text-rose-400" },
              { label: "Avg Composite",    value: summary.avg_forecast_composite.toFixed(1), color: "text-indigo-400" },
            ].map(({ label, value, color }) => (
              <div key={label} className="bg-slate-900 border border-slate-800 rounded-xl p-4">
                <div className="text-xs text-slate-400">{label}</div>
                <div className={`text-2xl font-bold mt-1 ${color ?? "text-white"}`}>{value}</div>
              </div>
            ))}
          </div>
        )}

        {/* confidence dist bar */}
        {summary && (
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-400 mb-2">Confidence Level Distribution</div>
            <ConfDistBar counts={summary.confidence_counts} />
            <div className="flex gap-4 mt-2 text-xs text-slate-500">
              {["committed","high","moderate","low"].map((k) => (
                <span key={k} className={CONF_COLOR[k]}>{k}: {summary.confidence_counts[k] || 0}</span>
              ))}
            </div>
          </div>
        )}

        {/* filters */}
        <div className="flex flex-wrap gap-2">
          {[
            { label: "All Levels", val: "all" },
            { label: "Committed",  val: "committed" },
            { label: "High",       val: "high" },
            { label: "Moderate",   val: "moderate" },
            { label: "Low",        val: "low" },
          ].map(({ label, val }) => (
            <button
              key={val}
              onClick={() => setFilterConf(val)}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
                filterConf === val
                  ? "bg-indigo-600 text-white"
                  : "bg-slate-800 text-slate-400 hover:text-white"
              }`}
            >
              {label}
            </button>
          ))}
          <select
            value={filterRegion}
            onChange={(e) => setFilterRegion(e.target.value)}
            className="px-3 py-1.5 rounded-lg text-xs bg-slate-800 text-slate-300 border border-slate-700"
          >
            <option value="all">All Regions</option>
            {["NAMER","EMEA","APAC","LATAM"].map((r) => (
              <option key={r} value={r}>{r}</option>
            ))}
          </select>
        </div>

        {/* reps grid */}
        {loading ? (
          <div className="text-slate-400 text-center py-16">Loading forecasts…</div>
        ) : reps.length === 0 ? (
          <div className="text-slate-500 text-center py-16">No reps match your filters.</div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {reps.map((r) => (
              <RepCard key={r.rep_id} rep={r} onClick={() => setSelected(r)} />
            ))}
          </div>
        )}

        {/* avg score bars */}
        {summary && (
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
            <div className="text-sm font-semibold text-slate-300 mb-4">Average Score Breakdown</div>
            <div className="space-y-3">
              <ScoreBar label="Historical Accuracy" value={summary.avg_historical_accuracy_score} color="bg-indigo-500" />
              <ScoreBar label="Pipeline Coverage"   value={summary.avg_pipeline_coverage_score}   color="bg-violet-500" />
              <ScoreBar label="Deal Quality"        value={summary.avg_deal_quality_score}         color="bg-sky-500" />
              <ScoreBar label="Activity Signal"     value={summary.avg_activity_signal_score}      color="bg-amber-500" />
            </div>
          </div>
        )}
      </div>

      {selected && <RepModal rep={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
