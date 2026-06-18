"use client";
import { useEffect, useState, useCallback } from "react";

interface Rep {
  rep_id: string;
  region: string;
  time_risk: string;
  time_pattern: string;
  time_severity: string;
  recommended_action: string;
  priority_allocation_score: number;
  balance_score: number;
  pipeline_focus_score: number;
  selling_effectiveness_score: number;
  time_composite: number;
  has_time_gap: boolean;
  requires_time_coaching: boolean;
  estimated_quota_risk_usd: number;
  time_signal: string;
}

interface Summary {
  total: number;
  risk_counts: Record<string, number>;
  pattern_counts: Record<string, number>;
  severity_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_time_composite: number;
  time_gap_count: number;
  coaching_count: number;
  avg_priority_allocation_score: number;
  avg_balance_score: number;
  avg_pipeline_focus_score: number;
  avg_selling_effectiveness_score: number;
  total_estimated_quota_risk_usd: number;
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
  optimized: "text-emerald-400", balanced: "text-yellow-400",
  misaligned: "text-orange-400", scattered: "text-rose-400",
};
const PATTERN_LABELS: Record<string, string> = {
  none: "None", high_priority_neglect: "Priority Neglect",
  admin_overload: "Admin Overload", reactive_time_sink: "Reactive Trap",
  wrong_size_focus: "Wrong Size Focus", renewal_hover: "Renewal Hover",
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
                tab === t ? "bg-lime-500 text-white" : "bg-slate-800 text-slate-400 hover:text-white"}`}>
              {t.charAt(0).toUpperCase() + t.slice(1)}
            </button>
          ))}
        </div>
        {tab === "scores" && (
          <div className="space-y-2">
            {[
              ["Priority Allocation", rep.priority_allocation_score],
              ["Time Balance", rep.balance_score],
              ["Pipeline Focus", rep.pipeline_focus_score],
              ["Selling Effectiveness", rep.selling_effectiveness_score],
              ["Time Composite", rep.time_composite],
            ].map(([label, val]) => (
              <div key={label as string} className="flex justify-between items-center">
                <span className="text-sm text-slate-300">{label as string}</span>
                <div className="flex items-center gap-2">
                  <div className="w-24 bg-slate-800 rounded-full h-1.5">
                    <div className="bg-lime-500 h-1.5 rounded-full"
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
                <span className="text-slate-400">Quota Risk</span>
                <span className="font-semibold text-lime-400">
                  ${rep.estimated_quota_risk_usd.toLocaleString()}
                </span>
              </div>
            </div>
          </div>
        )}
        {tab === "signal" && (
          <div className="space-y-3">
            <div className="bg-slate-800 rounded-lg p-3">
              <p className="text-xs text-slate-400 mb-1">Time Signal</p>
              <p className="text-sm text-white leading-relaxed">{rep.time_signal}</p>
            </div>
            <div className="grid grid-cols-2 gap-2 text-sm">
              <div className="bg-slate-800 rounded p-2">
                <p className="text-slate-400 text-xs">Pattern</p>
                <p className="text-white">{PATTERN_LABELS[rep.time_pattern] ?? rep.time_pattern}</p>
              </div>
              <div className="bg-slate-800 rounded p-2">
                <p className="text-slate-400 text-xs">Severity</p>
                <p className={SEV_COLORS[rep.time_severity] ?? "text-white"}>
                  {rep.time_severity.charAt(0).toUpperCase() + rep.time_severity.slice(1)}
                </p>
              </div>
            </div>
          </div>
        )}
        {tab === "action" && (
          <div className="space-y-3">
            <div className="bg-lime-500/10 border border-lime-500/30 rounded-lg p-3">
              <p className="text-xs text-lime-400 mb-1">Recommended Action</p>
              <p className="text-sm text-white">
                {rep.recommended_action.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase())}
              </p>
            </div>
            <div className="grid grid-cols-2 gap-2 text-sm">
              <div className="bg-slate-800 rounded p-2">
                <p className="text-slate-400 text-xs">Gap Detected</p>
                <p className={rep.has_time_gap ? "text-rose-400" : "text-emerald-400"}>
                  {rep.has_time_gap ? "✗ Yes" : "✓ No"}
                </p>
              </div>
              <div className="bg-slate-800 rounded p-2">
                <p className="text-slate-400 text-xs">Coaching Required</p>
                <p className={rep.requires_time_coaching ? "text-orange-400" : "text-emerald-400"}>
                  {rep.requires_time_coaching ? "✗ Yes" : "✓ No"}
                </p>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function SalesTimeAllocationPage() {
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
    const res = await fetch(`/api/sales-time-allocation-intelligence-engine?${params}`);
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
        none: "bg-slate-500", high_priority_neglect: "bg-rose-400",
        admin_overload: "bg-orange-400", reactive_time_sink: "bg-amber-400",
        wrong_size_focus: "bg-yellow-400", renewal_hover: "bg-lime-400",
      },
    },
    {
      title: "Severity Distribution",
      counts: summary?.severity_counts ?? {},
      colors: { optimized: "bg-emerald-400", balanced: "bg-yellow-400", misaligned: "bg-orange-400", scattered: "bg-rose-400" },
    },
    {
      title: "Action Distribution",
      counts: summary?.action_counts ?? {},
      colors: {
        no_action: "bg-slate-500",
        account_prioritization_coaching: "bg-lime-400",
        admin_reduction_coaching: "bg-orange-400",
        pipeline_focus_coaching: "bg-yellow-400",
        time_reallocation_coaching: "bg-amber-400",
        time_reallocation_intervention: "bg-rose-400",
        time_strategy_reset: "bg-red-600",
      },
    },
  ] as Array<{ title: string; counts: Record<string, number>; colors: Record<string, string> }>;

  const RISKS = ["", "low", "moderate", "high", "critical"];
  const PATTERNS = ["", "none", "high_priority_neglect", "admin_overload",
    "reactive_time_sink", "wrong_size_focus", "renewal_hover"];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
      {selected && <DetailModal rep={selected} onClose={() => setSelected(null)} />}

      <div className="max-w-7xl mx-auto">
        <div className="mb-6">
          <h1 className="text-2xl font-bold text-white">
            ⏱️ Sales Time Allocation Intelligence Engine
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Per-rep time misalignment analysis — priority account focus, admin burden, pipeline building, and selling effectiveness
          </p>
        </div>

        {/* KPI strip */}
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3 mb-6">
          {[
            { label: "Total Reps", value: summary?.total ?? 0, suffix: "" },
            { label: "Avg Composite", value: summary?.avg_time_composite ?? 0, suffix: "/100" },
            { label: "Gap Detected", value: summary?.time_gap_count ?? 0, suffix: " reps" },
            { label: "Coaching Needed", value: summary?.coaching_count ?? 0, suffix: " reps" },
            { label: "Quota at Risk", value: summary ? fmt(summary.total_estimated_quota_risk_usd) : "$0", suffix: "" },
            { label: "Avg Priority Score", value: summary?.avg_priority_allocation_score ?? 0, suffix: "/100" },
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
            <GaugeRing value={summary?.avg_priority_allocation_score ?? 0} label="Priority Allocation" color="#84cc16" />
            <GaugeRing value={summary?.avg_balance_score ?? 0} label="Time Balance" color="#65a30d" />
            <GaugeRing value={summary?.avg_pipeline_focus_score ?? 0} label="Pipeline Focus" color="#4d7c0f" />
            <GaugeRing value={summary?.avg_selling_effectiveness_score ?? 0} label="Selling Effectiveness" color="#a3e635" />
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
                    ? "bg-lime-500 border-lime-500 text-white"
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
                    ? "bg-lime-500 border-lime-500 text-white"
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
                className="text-left bg-slate-900 border border-slate-800 rounded-xl p-4 hover:border-lime-500/50 transition-colors">
                <div className="flex items-start justify-between mb-2">
                  <div>
                    <p className="font-semibold text-white text-sm">{rep.rep_id}</p>
                    <p className="text-xs text-slate-400">{rep.region}</p>
                  </div>
                  <span className={`text-xs font-semibold px-2 py-0.5 rounded-full border ${RISK_BG[rep.time_risk] ?? ""}`}>
                    <span className={RISK_COLORS[rep.time_risk] ?? ""}>{rep.time_risk}</span>
                  </span>
                </div>

                <div className="mb-3">
                  <div className="flex justify-between text-xs mb-0.5">
                    <span className="text-slate-400">Composite</span>
                    <span className="text-white font-mono">{rep.time_composite.toFixed(1)}</span>
                  </div>
                  <div className="w-full bg-slate-800 rounded-full h-1.5">
                    <div className="bg-lime-500 h-1.5 rounded-full"
                      style={{ width: `${rep.time_composite}%` }} />
                  </div>
                </div>

                <div className="text-xs text-slate-400 mb-2">
                  {PATTERN_LABELS[rep.time_pattern] ?? rep.time_pattern}
                </div>

                <div className="flex gap-1.5 flex-wrap">
                  {rep.has_time_gap && (
                    <span className="text-xs bg-lime-500/10 text-lime-400 border border-lime-500/30 rounded px-1.5 py-0.5">
                      ⏱️ GAP
                    </span>
                  )}
                  {rep.requires_time_coaching && (
                    <span className="text-xs bg-orange-500/10 text-orange-400 border border-orange-500/30 rounded px-1.5 py-0.5">
                      🎯 COACH
                    </span>
                  )}
                </div>

                {rep.estimated_quota_risk_usd > 0 && (
                  <p className="text-xs text-lime-400 font-semibold mt-2">
                    {fmt(rep.estimated_quota_risk_usd)} quota risk
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
