"use client";
import { useEffect, useState, useCallback } from "react";

interface Rep {
  rep_id: string;
  region: string;
  pipeline_risk: string;
  pipeline_pattern: string;
  pipeline_severity: string;
  recommended_action: string;
  generation_rate_score: number;
  pipeline_volume_score: number;
  prospecting_quality_score: number;
  consistency_score: number;
  pipeline_composite: number;
  has_pipeline_gap: boolean;
  requires_pipeline_coaching: boolean;
  estimated_pipeline_shortfall_usd: number;
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
  avg_generation_rate_score: number;
  avg_pipeline_volume_score: number;
  avg_prospecting_quality_score: number;
  avg_consistency_score: number;
  total_estimated_pipeline_shortfall_usd: number;
}

const RISK_COLORS: Record<string, string> = {
  low: "text-emerald-400", moderate: "text-yellow-400",
  high: "text-orange-400", critical: "text-rose-400",
};
const RISK_BG: Record<string, string> = {
  low: "bg-emerald-400/10 border-emerald-400/30",
  moderate: "bg-yellow-400/10 border-yellow-400/30",
  high: "bg-orange-400/10 border-orange-400/30",
  critical: "bg-rose-400/10 border-rose-400/30",
};
const SEV_COLORS: Record<string, string> = {
  generating: "text-emerald-400", adequate: "text-yellow-400",
  sluggish: "text-orange-400", stalled: "text-rose-400",
};
const PATTERN_LABELS: Record<string, string> = {
  none: "None", burst_and_fade: "Burst & Fade",
  reactive_only: "Reactive Only", slow_starter: "Slow Starter",
  territory_exhaustion: "Territory Exhaustion", channel_dependency: "Channel Dependency",
};

function GaugeRing({ value, label, color }: { value: number; label: string; color: string }) {
  const r = 36, circ = 2 * Math.PI * r;
  const arc = circ * (1 - value / 100);
  return (
    <div className="flex flex-col items-center gap-1">
      <svg width="88" height="88" viewBox="0 0 88 88">
        <circle cx="44" cy="44" r={r} fill="none" stroke="#1e293b" strokeWidth="8" />
        <circle cx="44" cy="44" r={r} fill="none" stroke={color} strokeWidth="8"
          strokeDasharray={circ} strokeDashoffset={arc}
          strokeLinecap="round" transform="rotate(-90 44 44)" />
        <text x="44" y="49" textAnchor="middle" fontSize="13" fontWeight="700" fill="white">
          {value.toFixed(0)}
        </text>
      </svg>
      <span className="text-xs text-slate-400 text-center leading-tight">{label}</span>
    </div>
  );
}

function DistBar({ title, counts, colors }: { title: string; counts: Record<string, number>; colors: Record<string, string> }) {
  const total = Object.values(counts).reduce((a, b) => a + b, 0) || 1;
  return (
    <div>
      <p className="text-xs text-slate-400 mb-1">{title}</p>
      <div className="flex rounded overflow-hidden h-3">
        {Object.entries(counts).map(([k, v]) => (
          <div key={k} style={{ width: `${(v / total) * 100}%` }}
            className={`${colors[k] ?? "bg-slate-600"} transition-all`} title={`${k}: ${v}`} />
        ))}
      </div>
      <div className="flex flex-wrap gap-x-3 mt-1">
        {Object.entries(counts).map(([k, v]) => (
          <span key={k} className="text-xs text-slate-400">
            <span className={`inline-block w-2 h-2 rounded-sm mr-1 ${colors[k] ?? "bg-slate-600"}`} />
            {k} ({v})
          </span>
        ))}
      </div>
    </div>
  );
}

function DetailModal({ rep, onClose }: { rep: Rep; onClose: () => void }) {
  useEffect(() => {
    const h = (e: KeyboardEvent) => e.key === "Escape" && onClose();
    window.addEventListener("keydown", h);
    return () => window.removeEventListener("keydown", h);
  }, [onClose]);
  const [tab, setTab] = useState<"scores" | "signal" | "action">("scores");
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70"
      onClick={onClose}>
      <div className="bg-slate-900 border border-slate-700 rounded-xl p-6 max-w-lg w-full mx-4 shadow-2xl"
        onClick={(e) => e.stopPropagation()}>
        <div className="flex items-start justify-between mb-4">
          <div>
            <h2 className="text-lg font-bold text-white">{rep.rep_id}</h2>
            <p className="text-sm text-slate-400">{rep.region}</p>
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-white text-xl leading-none">✕</button>
        </div>
        <div className="flex gap-2 mb-4">
          {(["scores", "signal", "action"] as const).map((t) => (
            <button key={t} onClick={() => setTab(t)}
              className={`px-3 py-1 rounded text-xs font-medium transition-colors ${
                tab === t ? "bg-cyan-500 text-white" : "bg-slate-800 text-slate-400 hover:text-white"}`}>
              {t.charAt(0).toUpperCase() + t.slice(1)}
            </button>
          ))}
        </div>
        {tab === "scores" && (
          <div className="space-y-2">
            {[
              ["Generation Rate", rep.generation_rate_score],
              ["Pipeline Volume", rep.pipeline_volume_score],
              ["Prospecting Quality", rep.prospecting_quality_score],
              ["Consistency", rep.consistency_score],
              ["Pipeline Composite", rep.pipeline_composite],
            ].map(([label, val]) => (
              <div key={label as string} className="flex justify-between items-center">
                <span className="text-sm text-slate-300">{label as string}</span>
                <div className="flex items-center gap-2">
                  <div className="w-24 bg-slate-800 rounded-full h-1.5">
                    <div className="bg-cyan-500 h-1.5 rounded-full"
                      style={{ width: `${Math.min(val as number, 100)}%` }} />
                  </div>
                  <span className="text-sm font-mono text-white w-10 text-right">
                    {(val as number).toFixed(1)}
                  </span>
                </div>
              </div>
            ))}
            <div className="mt-3 pt-3 border-t border-slate-800">
              <div className="flex justify-between text-sm">
                <span className="text-slate-400">Pipeline Shortfall</span>
                <span className="font-semibold text-cyan-400">
                  ${rep.estimated_pipeline_shortfall_usd.toLocaleString()}
                </span>
              </div>
            </div>
          </div>
        )}
        {tab === "signal" && (
          <div className="space-y-3">
            <div className="bg-slate-800 rounded-lg p-3">
              <p className="text-xs text-slate-400 mb-1">Pipeline Signal</p>
              <p className="text-sm text-white leading-relaxed">{rep.pipeline_signal}</p>
            </div>
            <div className="grid grid-cols-2 gap-2 text-sm">
              <div className="bg-slate-800 rounded p-2">
                <p className="text-slate-400 text-xs">Pattern</p>
                <p className="text-white">{PATTERN_LABELS[rep.pipeline_pattern] ?? rep.pipeline_pattern}</p>
              </div>
              <div className="bg-slate-800 rounded p-2">
                <p className="text-slate-400 text-xs">Severity</p>
                <p className={SEV_COLORS[rep.pipeline_severity] ?? "text-white"}>
                  {rep.pipeline_severity.charAt(0).toUpperCase() + rep.pipeline_severity.slice(1)}
                </p>
              </div>
            </div>
          </div>
        )}
        {tab === "action" && (
          <div className="space-y-3">
            <div className="bg-cyan-500/10 border border-cyan-500/30 rounded-lg p-3">
              <p className="text-xs text-cyan-400 mb-1">Recommended Action</p>
              <p className="text-sm text-white">
                {rep.recommended_action.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase())}
              </p>
            </div>
            <div className="grid grid-cols-2 gap-2 text-sm">
              <div className="bg-slate-800 rounded p-2">
                <p className="text-slate-400 text-xs">Gap Detected</p>
                <p className={rep.has_pipeline_gap ? "text-rose-400" : "text-emerald-400"}>
                  {rep.has_pipeline_gap ? "✗ Yes" : "✓ No"}
                </p>
              </div>
              <div className="bg-slate-800 rounded p-2">
                <p className="text-slate-400 text-xs">Coaching Required</p>
                <p className={rep.requires_pipeline_coaching ? "text-orange-400" : "text-emerald-400"}>
                  {rep.requires_pipeline_coaching ? "✗ Yes" : "✓ No"}
                </p>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function SalesPipelineGenerationVelocityPage() {
  const [reps, setReps] = useState<Rep[]>([]);
  const [summary, setSummary] = useState<Summary | null>(null);
  const [loading, setLoading] = useState(true);
  const [riskFilter, setRiskFilter] = useState("");
  const [patternFilter, setPatternFilter] = useState("");
  const [selected, setSelected] = useState<Rep | null>(null);

  const load = useCallback(async () => {
    setLoading(true);
    const params = new URLSearchParams();
    if (riskFilter) params.set("risk", riskFilter);
    if (patternFilter) params.set("pattern", patternFilter);
    const res = await fetch(`/api/sales-pipeline-generation-velocity-intelligence-engine?${params}`);
    const data = await res.json();
    setReps(data.reps ?? []);
    setSummary(data.summary ?? null);
    setLoading(false);
  }, [riskFilter, patternFilter]);

  useEffect(() => { load(); }, [load]);

  const fmt = (n: number) =>
    n >= 1_000_000 ? `$${(n / 1_000_000).toFixed(1)}M`
    : n >= 1_000 ? `$${(n / 1_000).toFixed(0)}K`
    : `$${n.toFixed(0)}`;

  const distributions = [
    {
      title: "Risk Distribution",
      counts: summary?.risk_counts ?? {},
      colors: { low: "bg-emerald-400", moderate: "bg-yellow-400", high: "bg-orange-400", critical: "bg-rose-400" },
    },
    {
      title: "Pattern Distribution",
      counts: summary?.pattern_counts ?? {},
      colors: {
        none: "bg-slate-500", burst_and_fade: "bg-rose-400",
        reactive_only: "bg-orange-400", slow_starter: "bg-yellow-400",
        territory_exhaustion: "bg-purple-400", channel_dependency: "bg-cyan-400",
      },
    },
    {
      title: "Severity Distribution",
      counts: summary?.severity_counts ?? {},
      colors: { generating: "bg-emerald-400", adequate: "bg-yellow-400", sluggish: "bg-orange-400", stalled: "bg-rose-400" },
    },
    {
      title: "Action Distribution",
      counts: summary?.action_counts ?? {},
      colors: {
        no_action: "bg-slate-500",
        prospecting_cadence_coaching: "bg-yellow-400",
        icp_targeting_coaching: "bg-purple-400",
        channel_diversification_coaching: "bg-cyan-400",
        pipeline_generation_coaching: "bg-orange-400",
        pipeline_generation_intervention: "bg-rose-400",
        pipeline_reset_intervention: "bg-red-600",
      },
    },
  ] as Array<{ title: string; counts: Record<string, number>; colors: Record<string, string> }>;

  const RISKS = ["", "low", "moderate", "high", "critical"];
  const PATTERNS = ["", "none", "burst_and_fade", "reactive_only", "slow_starter",
    "territory_exhaustion", "channel_dependency"];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
      {selected && <DetailModal rep={selected} onClose={() => setSelected(null)} />}

      <div className="max-w-7xl mx-auto">
        <div className="mb-6">
          <h1 className="text-2xl font-bold text-white">
            🚀 Sales Pipeline Generation Velocity Intelligence Engine
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Per-rep pipeline creation speed — outreach conversion, volume generation, prospecting quality, and consistency
          </p>
        </div>

        {/* KPI strip */}
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3 mb-6">
          {[
            { label: "Total Reps", value: summary?.total ?? 0, suffix: "" },
            { label: "Avg Composite", value: summary?.avg_pipeline_composite ?? 0, suffix: "/100" },
            { label: "Gap Detected", value: summary?.pipeline_gap_count ?? 0, suffix: " reps" },
            { label: "Coaching Needed", value: summary?.coaching_count ?? 0, suffix: " reps" },
            { label: "Pipeline Shortfall", value: summary ? fmt(summary.total_estimated_pipeline_shortfall_usd) : "$0", suffix: "" },
            { label: "Avg Gen Rate", value: summary?.avg_generation_rate_score ?? 0, suffix: "/100" },
          ].map(({ label, value, suffix }) => (
            <div key={label} className="bg-slate-900 border border-slate-800 rounded-xl p-4">
              <p className="text-xs text-slate-400 mb-1">{label}</p>
              <p className="text-xl font-bold text-white">
                {typeof value === "number" ? value.toLocaleString() : value}{suffix}
              </p>
            </div>
          ))}
        </div>

        {/* Gauges */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 mb-6">
          <h2 className="text-sm font-semibold text-slate-300 mb-4">Average Sub-Scores</h2>
          <div className="flex flex-wrap justify-around gap-4">
            <GaugeRing value={summary?.avg_generation_rate_score ?? 0} label="Generation Rate" color="#06b6d4" />
            <GaugeRing value={summary?.avg_pipeline_volume_score ?? 0} label="Pipeline Volume" color="#0891b2" />
            <GaugeRing value={summary?.avg_prospecting_quality_score ?? 0} label="Prospecting Quality" color="#0e7490" />
            <GaugeRing value={summary?.avg_consistency_score ?? 0} label="Consistency" color="#22d3ee" />
          </div>
        </div>

        {/* Distributions */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 mb-6">
          <h2 className="text-sm font-semibold text-slate-300 mb-4">Distributions</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-5">
            {distributions.map((d) => (
              <DistBar key={d.title} title={d.title} counts={d.counts} colors={d.colors} />
            ))}
          </div>
        </div>

        {/* Filters */}
        <div className="flex flex-wrap gap-2 mb-4">
          <div className="flex gap-1 flex-wrap">
            {RISKS.map((r) => (
              <button key={r} onClick={() => setRiskFilter(r)}
                className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${
                  riskFilter === r
                    ? "bg-cyan-500 border-cyan-500 text-white"
                    : "border-slate-700 text-slate-400 hover:text-white"}`}>
                {r || "All Risks"}
              </button>
            ))}
          </div>
          <div className="flex gap-1 flex-wrap">
            {PATTERNS.map((p) => (
              <button key={p} onClick={() => setPatternFilter(p)}
                className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${
                  patternFilter === p
                    ? "bg-cyan-500 border-cyan-500 text-white"
                    : "border-slate-700 text-slate-400 hover:text-white"}`}>
                {p ? PATTERN_LABELS[p] ?? p : "All Patterns"}
              </button>
            ))}
          </div>
        </div>

        {/* Rep grid */}
        {loading ? (
          <div className="text-center py-12 text-slate-400">Loading...</div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {reps.map((rep) => (
              <button key={rep.rep_id} onClick={() => setSelected(rep)}
                className="text-left bg-slate-900 border border-slate-800 rounded-xl p-4 hover:border-cyan-500/50 transition-colors">
                <div className="flex items-start justify-between mb-2">
                  <div>
                    <p className="font-semibold text-white text-sm">{rep.rep_id}</p>
                    <p className="text-xs text-slate-400">{rep.region}</p>
                  </div>
                  <span className={`text-xs font-semibold px-2 py-0.5 rounded-full border ${RISK_BG[rep.pipeline_risk] ?? ""}`}>
                    <span className={RISK_COLORS[rep.pipeline_risk] ?? ""}>{rep.pipeline_risk}</span>
                  </span>
                </div>

                <div className="mb-3">
                  <div className="flex justify-between text-xs mb-0.5">
                    <span className="text-slate-400">Composite</span>
                    <span className="text-white font-mono">{rep.pipeline_composite.toFixed(1)}</span>
                  </div>
                  <div className="w-full bg-slate-800 rounded-full h-1.5">
                    <div className="bg-cyan-500 h-1.5 rounded-full"
                      style={{ width: `${rep.pipeline_composite}%` }} />
                  </div>
                </div>

                <div className="text-xs text-slate-400 mb-2">
                  {PATTERN_LABELS[rep.pipeline_pattern] ?? rep.pipeline_pattern}
                </div>

                <div className="flex gap-1.5 flex-wrap">
                  {rep.has_pipeline_gap && (
                    <span className="text-xs bg-cyan-500/10 text-cyan-400 border border-cyan-500/30 rounded px-1.5 py-0.5">
                      🚀 GAP
                    </span>
                  )}
                  {rep.requires_pipeline_coaching && (
                    <span className="text-xs bg-orange-500/10 text-orange-400 border border-orange-500/30 rounded px-1.5 py-0.5">
                      🎯 COACH
                    </span>
                  )}
                </div>

                {rep.estimated_pipeline_shortfall_usd > 0 && (
                  <p className="text-xs text-cyan-400 font-semibold mt-2">
                    {fmt(rep.estimated_pipeline_shortfall_usd)} shortfall
                  </p>
                )}
              </button>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
