"use client";
import { useEffect, useState, useCallback } from "react";

interface Rep {
  rep_id: string;
  region: string;
  multithread_risk: string;
  multithread_pattern: string;
  multithread_severity: string;
  recommended_action: string;
  threading_breadth_score: number;
  champion_dependency_score: number;
  decision_maker_coverage_score: number;
  relationship_map_score: number;
  multithread_composite: number;
  has_threading_gap: boolean;
  requires_multithread_coaching: boolean;
  estimated_at_risk_usd: number;
  multithread_signal: string;
}

interface Summary {
  total: number;
  risk_counts: Record<string, number>;
  pattern_counts: Record<string, number>;
  severity_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_multithread_composite: number;
  threading_gap_count: number;
  coaching_count: number;
  avg_threading_breadth_score: number;
  avg_champion_dependency_score: number;
  avg_decision_maker_coverage_score: number;
  avg_relationship_map_score: number;
  total_estimated_at_risk_usd: number;
}

const RISK_COLORS: Record<string, string> = {
  low: "text-emerald-400",
  moderate: "text-yellow-400",
  high: "text-orange-400",
  critical: "text-red-400",
};
const RISK_BG: Record<string, string> = {
  low: "bg-emerald-900/40 border-emerald-700",
  moderate: "bg-yellow-900/40 border-yellow-700",
  high: "bg-orange-900/40 border-orange-700",
  critical: "bg-red-900/40 border-red-700",
};
const SEV_COLORS: Record<string, string> = {
  networked: "text-emerald-400",
  developing: "text-yellow-400",
  exposed: "text-orange-400",
  fragile: "text-red-400",
};

function GaugeRing({ score, label, color }: { score: number; label: string; color: string }) {
  const r = 30;
  const circ = 2 * Math.PI * r;
  const pct = Math.min(score, 100) / 100;
  return (
    <div className="flex flex-col items-center gap-1">
      <svg width="80" height="80" viewBox="0 0 80 80">
        <circle cx="40" cy="40" r={r} fill="none" stroke="#1e293b" strokeWidth="8" />
        <circle
          cx="40" cy="40" r={r} fill="none"
          stroke={color} strokeWidth="8"
          strokeDasharray={`${pct * circ} ${circ}`}
          strokeLinecap="round"
          transform="rotate(-90 40 40)"
        />
        <text x="40" y="45" textAnchor="middle" fill="white" fontSize="13" fontWeight="bold">
          {score.toFixed(0)}
        </text>
      </svg>
      <span className="text-xs text-slate-400 text-center leading-tight">{label}</span>
    </div>
  );
}

function DistBar({ title, counts, colors }: { title: string; counts: Record<string, number>; colors: Record<string, string> }) {
  const total = Object.values(counts).reduce((a, b) => a + b, 0) || 1;
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
      <p className="text-xs text-slate-400 mb-2 font-medium uppercase tracking-wide">{title}</p>
      <div className="flex rounded overflow-hidden h-3 mb-2">
        {Object.entries(counts).map(([k, v]) => (
          <div key={k} style={{ width: `${(v / total) * 100}%` }} className={colors[k] || "bg-slate-600"} title={`${k}: ${v}`} />
        ))}
      </div>
      <div className="flex flex-wrap gap-x-3 gap-y-1">
        {Object.entries(counts).map(([k, v]) => (
          <span key={k} className="text-xs text-slate-400">
            <span className={`inline-block w-2 h-2 rounded-full mr-1 ${colors[k] || "bg-slate-600"}`} />
            {k.replace(/_/g, " ")}: <span className="text-slate-200">{v}</span>
          </span>
        ))}
      </div>
    </div>
  );
}

function DetailModal({ rep, onClose }: { rep: Rep; onClose: () => void }) {
  useEffect(() => {
    const handler = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [onClose]);
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm" onClick={onClose}>
      <div className="bg-slate-900 border border-slate-700 rounded-2xl p-6 w-full max-w-lg shadow-2xl" onClick={(e) => e.stopPropagation()}>
        <div className="flex justify-between items-start mb-4">
          <div>
            <h2 className="text-lg font-bold text-slate-100">{rep.rep_id}</h2>
            <p className="text-sm text-slate-400">{rep.region}</p>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-slate-300 text-xl">✕</button>
        </div>
        <div className="space-y-4">
          <div>
            <p className="text-xs text-slate-500 uppercase tracking-wide mb-2">Scores</p>
            <div className="grid grid-cols-2 gap-2 text-sm">
              {[
                ["Threading Breadth", rep.threading_breadth_score],
                ["Champion Dependency", rep.champion_dependency_score],
                ["Decision Maker Coverage", rep.decision_maker_coverage_score],
                ["Relationship Map", rep.relationship_map_score],
                ["Composite", rep.multithread_composite],
              ].map(([label, val]) => (
                <div key={label as string} className="bg-slate-800 rounded-lg p-2 flex justify-between">
                  <span className="text-slate-400">{label as string}</span>
                  <span className="text-slate-100 font-medium">{(val as number).toFixed(1)}</span>
                </div>
              ))}
            </div>
          </div>
          <div>
            <p className="text-xs text-slate-500 uppercase tracking-wide mb-2">Signal</p>
            <p className="text-sm text-slate-300 bg-slate-800 rounded-lg p-3">{rep.multithread_signal}</p>
          </div>
          <div>
            <p className="text-xs text-slate-500 uppercase tracking-wide mb-2">Action</p>
            <div className="grid grid-cols-2 gap-2 text-sm">
              <div className="bg-slate-800 rounded-lg p-2">
                <span className="text-slate-400 block text-xs">Risk</span>
                <span className={`font-medium ${RISK_COLORS[rep.multithread_risk] || "text-slate-200"}`}>
                  {rep.multithread_risk.toUpperCase()}
                </span>
              </div>
              <div className="bg-slate-800 rounded-lg p-2">
                <span className="text-slate-400 block text-xs">Severity</span>
                <span className={`font-medium ${SEV_COLORS[rep.multithread_severity] || "text-slate-200"}`}>
                  {rep.multithread_severity.toUpperCase()}
                </span>
              </div>
              <div className="bg-slate-800 rounded-lg p-2 col-span-2">
                <span className="text-slate-400 block text-xs">Recommended Action</span>
                <span className="text-slate-200 font-medium">{rep.recommended_action.replace(/_/g, " ")}</span>
              </div>
              <div className="bg-slate-800 rounded-lg p-2 col-span-2">
                <span className="text-slate-400 block text-xs">Estimated At-Risk Revenue</span>
                <span className="text-slate-200 font-medium">
                  ${rep.estimated_at_risk_usd.toLocaleString("en-US", { minimumFractionDigits: 0 })}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default function MultithreadingPage() {
  const [data, setData] = useState<{ reps: Rep[]; summary: Summary } | null>(null);
  const [loading, setLoading] = useState(true);
  const [riskFilter, setRiskFilter] = useState("");
  const [patternFilter, setPatternFilter] = useState("");
  const [selected, setSelected] = useState<Rep | null>(null);

  const load = useCallback(async () => {
    setLoading(true);
    const params = new URLSearchParams();
    if (riskFilter) params.set("risk", riskFilter);
    if (patternFilter) params.set("pattern", patternFilter);
    const res = await fetch(`/api/sales-multithreading-intelligence-engine?${params}`);
    const json = await res.json();
    setData(json);
    setLoading(false);
  }, [riskFilter, patternFilter]);

  useEffect(() => { load(); }, [load]);

  const s = data?.summary;
  const reps = data?.reps ?? [];

  const distBars = [
    {
      title: "Risk Distribution",
      counts: s?.risk_counts ?? {},
      colors: { low: "bg-emerald-500", moderate: "bg-yellow-500", high: "bg-orange-500", critical: "bg-red-500" } as Record<string, string>,
    },
    {
      title: "Pattern Distribution",
      counts: s?.pattern_counts ?? {},
      colors: { none: "bg-emerald-500", single_threading: "bg-red-500", champion_dependency: "bg-orange-500", executive_blind_spot: "bg-yellow-500", stakeholder_map_gap: "bg-blue-500", relationship_stagnation: "bg-purple-500" } as Record<string, string>,
    },
    {
      title: "Severity Distribution",
      counts: s?.severity_counts ?? {},
      colors: { networked: "bg-emerald-500", developing: "bg-yellow-500", exposed: "bg-orange-500", fragile: "bg-red-500" } as Record<string, string>,
    },
    {
      title: "Recommended Actions",
      counts: s?.action_counts ?? {},
      colors: { no_action: "bg-emerald-500", multithread_coaching: "bg-yellow-500", champion_backup_strategy: "bg-orange-500", executive_outreach_plan: "bg-blue-500", stakeholder_mapping_session: "bg-purple-500", relationship_expansion_sprint: "bg-red-500" } as Record<string, string>,
    },
  ] as Array<{ title: string; counts: Record<string, number>; colors: Record<string, string> }>;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {selected && <DetailModal rep={selected} onClose={() => setSelected(null)} />}

      <div>
        <h1 className="text-2xl font-bold text-slate-100">Multithreading Intelligence</h1>
        <p className="text-slate-400 text-sm mt-1">
          Stakeholder breadth · Champion dependency · Executive access · Relationship mapping
        </p>
      </div>

      {/* KPI Strip */}
      <div className="grid grid-cols-2 md:grid-cols-3 xl:grid-cols-6 gap-3">
        {[
          { label: "Total Reps", value: s?.total ?? 0, fmt: "int" },
          { label: "Avg Composite", value: s?.avg_multithread_composite ?? 0, fmt: "dec" },
          { label: "Threading Gaps", value: s?.threading_gap_count ?? 0, fmt: "int" },
          { label: "Need Coaching", value: s?.coaching_count ?? 0, fmt: "int" },
          { label: "Avg Champion Risk", value: s?.avg_champion_dependency_score ?? 0, fmt: "dec" },
          { label: "Revenue At Risk", value: s?.total_estimated_at_risk_usd ?? 0, fmt: "usd" },
        ].map(({ label, value, fmt }) => (
          <div key={label} className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <p className="text-xs text-slate-400 mb-1">{label}</p>
            <p className="text-xl font-bold text-slate-100">
              {fmt === "usd"
                ? `$${(value as number).toLocaleString("en-US", { maximumFractionDigits: 0 })}`
                : fmt === "dec"
                ? (value as number).toFixed(1)
                : value}
            </p>
          </div>
        ))}
      </div>

      {/* Gauge Rings */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
        <p className="text-sm font-medium text-slate-300 mb-4">Average Sub-Scores (0–100, higher = more risk)</p>
        <div className="flex flex-wrap justify-around gap-4">
          <GaugeRing score={s?.avg_threading_breadth_score ?? 0} label="Threading Breadth" color="#ef4444" />
          <GaugeRing score={s?.avg_champion_dependency_score ?? 0} label="Champion Dependency" color="#f97316" />
          <GaugeRing score={s?.avg_decision_maker_coverage_score ?? 0} label="Decision Maker Gap" color="#a855f7" />
          <GaugeRing score={s?.avg_relationship_map_score ?? 0} label="Relationship Map" color="#3b82f6" />
        </div>
      </div>

      {/* Distribution Bars */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {distBars.map((d) => (
          <DistBar key={d.title} title={d.title} counts={d.counts} colors={d.colors} />
        ))}
      </div>

      {/* Filters */}
      <div className="space-y-2">
        <div className="flex flex-wrap gap-2">
          {["", "low", "moderate", "high", "critical"].map((r) => (
            <button
              key={r}
              onClick={() => setRiskFilter(r)}
              className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${
                riskFilter === r
                  ? "bg-indigo-600 border-indigo-500 text-white"
                  : "border-slate-700 text-slate-400 hover:border-slate-500"
              }`}
            >
              {r === "" ? "All Risk" : r}
            </button>
          ))}
        </div>
        <div className="flex flex-wrap gap-2">
          {["", "none", "single_threading", "champion_dependency", "executive_blind_spot", "stakeholder_map_gap", "relationship_stagnation"].map((p) => (
            <button
              key={p}
              onClick={() => setPatternFilter(p)}
              className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${
                patternFilter === p
                  ? "bg-indigo-600 border-indigo-500 text-white"
                  : "border-slate-700 text-slate-400 hover:border-slate-500"
              }`}
            >
              {p === "" ? "All Patterns" : p.replace(/_/g, " ")}
            </button>
          ))}
        </div>
      </div>

      {/* Rep Cards */}
      {loading ? (
        <div className="text-center text-slate-500 py-12">Loading…</div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
          {reps.map((rep) => (
            <button
              key={rep.rep_id}
              onClick={() => setSelected(rep)}
              className={`text-left rounded-xl border p-4 space-y-2 transition-all hover:scale-[1.01] hover:shadow-lg ${RISK_BG[rep.multithread_risk] || "bg-slate-900 border-slate-800"}`}
            >
              <div className="flex justify-between items-start">
                <div>
                  <p className="font-semibold text-slate-100">{rep.rep_id}</p>
                  <p className="text-xs text-slate-400">{rep.region}</p>
                </div>
                <div className="flex flex-col items-end gap-1">
                  <span className={`text-xs font-bold ${RISK_COLORS[rep.multithread_risk] || "text-slate-300"}`}>
                    {rep.multithread_risk.toUpperCase()}
                  </span>
                  {rep.has_threading_gap && (
                    <span className="text-xs bg-red-900/60 border border-red-700 text-red-300 rounded px-1.5 py-0.5">🔗 GAP</span>
                  )}
                </div>
              </div>
              <div className="flex justify-between text-xs text-slate-400">
                <span>Composite: <span className="text-slate-200 font-medium">{rep.multithread_composite.toFixed(1)}</span></span>
                <span className={SEV_COLORS[rep.multithread_severity] || "text-slate-300"}>
                  {rep.multithread_severity}
                </span>
              </div>
              <p className="text-xs text-slate-400 leading-tight line-clamp-2">{rep.multithread_signal}</p>
              {rep.estimated_at_risk_usd > 0 && (
                <p className="text-xs text-orange-300 font-medium">
                  At Risk: ${rep.estimated_at_risk_usd.toLocaleString("en-US", { maximumFractionDigits: 0 })}
                </p>
              )}
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
