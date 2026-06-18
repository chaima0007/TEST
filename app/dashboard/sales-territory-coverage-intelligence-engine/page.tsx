"use client";

import { useEffect, useState, useCallback } from "react";

interface Rep {
  rep_id: string;
  region: string;
  coverage_risk: string;
  coverage_pattern: string;
  coverage_severity: string;
  recommended_action: string;
  account_breadth_score: number;
  account_prioritization_score: number;
  whitespace_exploitation_score: number;
  churn_prevention_score: number;
  territory_coverage_composite: number;
  has_coverage_gap: boolean;
  requires_territory_rebalance: boolean;
  estimated_revenue_at_risk_usd: number;
  coverage_signal: string;
}

interface Summary {
  total: number;
  risk_counts: Record<string, number>;
  pattern_counts: Record<string, number>;
  severity_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_territory_coverage_composite: number;
  coverage_gap_count: number;
  rebalance_count: number;
  avg_account_breadth_score: number;
  avg_account_prioritization_score: number;
  avg_whitespace_exploitation_score: number;
  avg_churn_prevention_score: number;
  total_estimated_revenue_at_risk_usd: number;
}

const riskColor: Record<string, string> = {
  low: "text-emerald-400", moderate: "text-amber-400",
  high: "text-orange-400", critical: "text-rose-400",
};
const riskBg: Record<string, string> = {
  low: "bg-emerald-900/40 border-emerald-700", moderate: "bg-amber-900/40 border-amber-700",
  high: "bg-orange-900/40 border-orange-700", critical: "bg-rose-900/40 border-rose-700",
};
const severityColor: Record<string, string> = {
  optimized: "text-emerald-400", gaps_detected: "text-amber-400",
  underserved: "text-orange-400", critical: "text-rose-400",
};
const scoreBarColor: Record<string, string> = {
  breadth: "bg-indigo-500", prioritization: "bg-violet-500",
  whitespace: "bg-amber-500", churn: "bg-rose-500",
};

function ScoreBar({ label, value, colorKey }: { label: string; value: number; colorKey: string }) {
  return (
    <div>
      <div className="flex justify-between text-xs text-slate-400 mb-1">
        <span>{label}</span><span>{value.toFixed(1)}</span>
      </div>
      <div className="h-1.5 bg-slate-700 rounded-full overflow-hidden">
        <div
          className={`h-full rounded-full transition-all ${scoreBarColor[colorKey] ?? "bg-slate-500"}`}
          style={{ width: `${Math.min(value, 100)}%` }}
        />
      </div>
    </div>
  );
}

function GaugeRing({ value, label, color }: { value: number; label: string; color: string }) {
  const r = 36; const circ = 2 * Math.PI * r;
  const pct = Math.min(value, 100) / 100;
  return (
    <div className="flex flex-col items-center gap-2 bg-slate-900 border border-slate-800 rounded-xl p-4">
      <svg width="96" height="96" viewBox="0 0 96 96">
        <circle cx="48" cy="48" r={r} fill="none" stroke="#1e293b" strokeWidth="8" />
        <circle cx="48" cy="48" r={r} fill="none" stroke={color} strokeWidth="8"
          strokeDasharray={circ} strokeDashoffset={circ * (1 - pct)}
          strokeLinecap="round" transform="rotate(-90 48 48)" />
        <text x="48" y="54" textAnchor="middle" fill="white" fontSize="14" fontWeight="700">
          {value.toFixed(1)}
        </text>
      </svg>
      <span className="text-xs text-slate-400 text-center leading-tight">{label}</span>
    </div>
  );
}

function DistBar({ title, counts, colors }: { title: string; counts: Record<string, number>; colors: Record<string, string> }) {
  const total = Object.values(counts).reduce((a, b) => a + b, 0);
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
      <h3 className="text-sm font-semibold text-slate-300 mb-3">{title}</h3>
      <div className="space-y-2">
        {Object.entries(counts).map(([k, v]) => (
          <div key={k}>
            <div className="flex justify-between text-xs text-slate-400 mb-1">
              <span className="capitalize">{k.replace(/_/g, " ")}</span>
              <span>{v} ({total > 0 ? Math.round((v / total) * 100) : 0}%)</span>
            </div>
            <div className="h-1.5 bg-slate-700 rounded-full overflow-hidden">
              <div className={`h-full rounded-full ${colors[k] ?? "bg-slate-500"}`}
                style={{ width: `${total > 0 ? (v / total) * 100 : 0}%` }} />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

function DetailModal({ rep, onClose }: { rep: Rep; onClose: () => void }) {
  const [tab, setTab] = useState<"scores" | "signals" | "action">("scores");
  useEffect(() => {
    const handler = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [onClose]);
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm"
      onClick={onClose}>
      <div className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-lg mx-4 shadow-2xl"
        onClick={(e) => e.stopPropagation()}>
        <div className="flex items-center justify-between p-5 border-b border-slate-800">
          <div>
            <h2 className="text-lg font-bold text-white">{rep.rep_id}</h2>
            <p className="text-sm text-slate-400">{rep.region}</p>
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-white text-xl leading-none">✕</button>
        </div>
        <div className="flex gap-1 px-5 pt-4">
          {(["scores", "signals", "action"] as const).map((t) => (
            <button key={t} onClick={() => setTab(t)}
              className={`px-3 py-1.5 text-xs rounded-lg font-medium transition-colors capitalize ${
                tab === t ? "bg-indigo-600 text-white" : "text-slate-400 hover:text-white"
              }`}>{t}</button>
          ))}
        </div>
        <div className="p-5 space-y-4">
          {tab === "scores" && (
            <>
              <div className="grid grid-cols-2 gap-3 mb-4">
                {[
                  ["Composite", rep.territory_coverage_composite.toFixed(1)],
                  ["Risk", rep.coverage_risk],
                  ["Severity", rep.coverage_severity],
                  ["Pattern", rep.coverage_pattern.replace(/_/g, " ")],
                ].map(([k, v]) => (
                  <div key={k} className="bg-slate-800 rounded-lg p-3">
                    <div className="text-xs text-slate-400">{k}</div>
                    <div className="text-sm font-semibold text-white capitalize">{v}</div>
                  </div>
                ))}
              </div>
              <div className="space-y-3">
                <ScoreBar label="Account Breadth Risk" value={rep.account_breadth_score} colorKey="breadth" />
                <ScoreBar label="Prioritization Risk" value={rep.account_prioritization_score} colorKey="prioritization" />
                <ScoreBar label="Whitespace Exploitation Risk" value={rep.whitespace_exploitation_score} colorKey="whitespace" />
                <ScoreBar label="Churn Prevention Risk" value={rep.churn_prevention_score} colorKey="churn" />
              </div>
              <div className="grid grid-cols-2 gap-2 pt-2">
                <div className="flex items-center gap-2 text-xs">
                  <span className={rep.has_coverage_gap ? "text-rose-400" : "text-emerald-400"}>●</span>
                  <span className="text-slate-400">{rep.has_coverage_gap ? "Coverage Gap" : "No Gap"}</span>
                </div>
                <div className="flex items-center gap-2 text-xs">
                  <span className={rep.requires_territory_rebalance ? "text-amber-400" : "text-emerald-400"}>●</span>
                  <span className="text-slate-400">{rep.requires_territory_rebalance ? "Rebalance Needed" : "Balanced"}</span>
                </div>
              </div>
            </>
          )}
          {tab === "signals" && (
            <div className="space-y-3">
              <div className="bg-slate-800 rounded-lg p-3">
                <div className="text-xs text-slate-400 mb-1">Signal</div>
                <div className="text-sm text-slate-200">{rep.coverage_signal}</div>
              </div>
              <div className="bg-slate-800 rounded-lg p-3">
                <div className="text-xs text-slate-400 mb-1">Est. Revenue at Risk</div>
                <div className="text-sm font-bold text-rose-400">
                  ${rep.estimated_revenue_at_risk_usd.toLocaleString()}
                </div>
              </div>
              <div className="bg-slate-800 rounded-lg p-3">
                <div className="text-xs text-slate-400 mb-1">Pattern</div>
                <div className="text-sm font-medium text-amber-300 capitalize">
                  {rep.coverage_pattern.replace(/_/g, " ")}
                </div>
              </div>
            </div>
          )}
          {tab === "action" && (
            <div className="space-y-3">
              <div className="bg-indigo-900/40 border border-indigo-700 rounded-lg p-4">
                <div className="text-xs text-indigo-300 mb-1">Recommended Action</div>
                <div className="text-sm font-bold text-white capitalize">
                  {rep.recommended_action.replace(/_/g, " ")}
                </div>
              </div>
              <div className="grid grid-cols-1 gap-2 text-sm text-slate-300">
                {rep.requires_territory_rebalance && (
                  <div className="flex items-start gap-2 bg-slate-800 rounded-lg p-3">
                    <span className="text-amber-400 mt-0.5">▲</span>
                    <span>Territory rebalance needed — review account assignment and coverage strategy</span>
                  </div>
                )}
                {rep.has_coverage_gap && (
                  <div className="flex items-start gap-2 bg-slate-800 rounded-lg p-3">
                    <span className="text-rose-400 mt-0.5">!</span>
                    <span>Active coverage gaps detected — accounts are at risk of churn or missed expansion</span>
                  </div>
                )}
                {rep.coverage_pattern === "whitespace_ignored" && (
                  <div className="flex items-start gap-2 bg-slate-800 rounded-lg p-3">
                    <span className="text-violet-400 mt-0.5">◇</span>
                    <span>Whitespace opportunities not pursued — potential expansion revenue being left on the table</span>
                  </div>
                )}
                {rep.coverage_pattern === "revenue_concentration" && (
                  <div className="flex items-start gap-2 bg-slate-800 rounded-lg p-3">
                    <span className="text-orange-400 mt-0.5">⚠</span>
                    <span>Revenue too concentrated — diversify account engagement to reduce dependency risk</span>
                  </div>
                )}
                {!rep.has_coverage_gap && !rep.requires_territory_rebalance && rep.coverage_risk === "low" && (
                  <div className="flex items-start gap-2 bg-slate-800 rounded-lg p-3">
                    <span className="text-emerald-400 mt-0.5">✓</span>
                    <span>Territory well-covered — maintain current cadence and engagement patterns</span>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default function SalesTerritoryCoverageIntelligenceEnginePage() {
  const [reps, setReps] = useState<Rep[]>([]);
  const [summary, setSummary] = useState<Summary | null>(null);
  const [loading, setLoading] = useState(true);
  const [selectedRep, setSelectedRep] = useState<Rep | null>(null);
  const [riskFilter, setRiskFilter] = useState("all");
  const [patternFilter, setPatternFilter] = useState("all");

  const fetchData = useCallback(async () => {
    setLoading(true);
    const params = new URLSearchParams();
    if (riskFilter !== "all") params.set("risk", riskFilter);
    if (patternFilter !== "all") params.set("pattern", patternFilter);
    const res = await fetch(`/api/sales-territory-coverage-intelligence-engine?${params}`);
    const data = await res.json();
    setReps(data.reps ?? []);
    setSummary(data.summary ?? null);
    setLoading(false);
  }, [riskFilter, patternFilter]);

  useEffect(() => { fetchData(); }, [fetchData]);

  const riskCounts     = summary?.risk_counts ?? {};
  const patternCounts  = summary?.pattern_counts ?? {};
  const severityCounts = summary?.severity_counts ?? {};

  const distributions: Array<{ title: string; counts: Record<string, number>; colors: Record<string, string> }> = [
    {
      title: "Risk Distribution",
      counts: riskCounts,
      colors: { low: "bg-emerald-500", moderate: "bg-amber-500", high: "bg-orange-500", critical: "bg-rose-500" } as Record<string, string>,
    },
    {
      title: "Pattern Distribution",
      counts: patternCounts,
      colors: {
        none: "bg-slate-500", account_neglect: "bg-amber-500", high_value_underserved: "bg-violet-500",
        whitespace_ignored: "bg-indigo-500", churn_risk_uncovered: "bg-rose-500", revenue_concentration: "bg-orange-500",
      } as Record<string, string>,
    },
    {
      title: "Severity Distribution",
      counts: severityCounts,
      colors: { optimized: "bg-emerald-500", gaps_detected: "bg-amber-500", underserved: "bg-orange-500", critical: "bg-rose-500" } as Record<string, string>,
    },
  ];

  return (
    <div className="space-y-6">
      {selectedRep && <DetailModal rep={selectedRep} onClose={() => setSelectedRep(null)} />}

      <div>
        <h1 className="text-2xl font-bold text-white">Territory Coverage Intelligence</h1>
        <p className="text-slate-400 mt-1 text-sm">
          Account breadth, high-value engagement, whitespace exploitation, and churn prevention by territory.
        </p>
      </div>

      {/* KPI strip */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        {[
          { label: "Total Reps", value: summary?.total ?? 0, color: "text-indigo-400" },
          { label: "Coverage Gaps", value: summary?.coverage_gap_count ?? 0, color: "text-rose-400" },
          { label: "Need Rebalance", value: summary?.rebalance_count ?? 0, color: "text-amber-400" },
          {
            label: "Revenue at Risk",
            value: `$${((summary?.total_estimated_revenue_at_risk_usd ?? 0) / 1000).toFixed(0)}k`,
            color: "text-rose-400",
          },
        ].map((kpi) => (
          <div key={kpi.label} className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-400 mb-1">{kpi.label}</div>
            <div className={`text-2xl font-bold ${kpi.color}`}>{kpi.value}</div>
          </div>
        ))}
      </div>

      {/* Gauge rings */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <GaugeRing value={summary?.avg_account_breadth_score ?? 0} label="Avg Breadth Risk" color="#6366f1" />
        <GaugeRing value={summary?.avg_account_prioritization_score ?? 0} label="Avg Prioritization Risk" color="#8b5cf6" />
        <GaugeRing value={summary?.avg_whitespace_exploitation_score ?? 0} label="Avg Whitespace Risk" color="#f59e0b" />
        <GaugeRing value={summary?.avg_churn_prevention_score ?? 0} label="Avg Churn Risk" color="#f43f5e" />
      </div>

      {/* Distribution bars */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {distributions.map((d) => (
          <DistBar key={d.title} title={d.title} counts={d.counts} colors={d.colors} />
        ))}
      </div>

      {/* Filters */}
      <div className="flex flex-wrap gap-3">
        <div className="flex gap-1 bg-slate-900 border border-slate-800 rounded-lg p-1">
          {["all", "low", "moderate", "high", "critical"].map((r) => (
            <button key={r} onClick={() => setRiskFilter(r)}
              className={`px-3 py-1 text-xs rounded-md font-medium capitalize transition-colors ${
                riskFilter === r ? "bg-indigo-600 text-white" : "text-slate-400 hover:text-white"
              }`}>{r}</button>
          ))}
        </div>
        <div className="flex flex-wrap gap-1 bg-slate-900 border border-slate-800 rounded-lg p-1">
          {["all", "none", "account_neglect", "high_value_underserved", "whitespace_ignored", "churn_risk_uncovered", "revenue_concentration"].map((p) => (
            <button key={p} onClick={() => setPatternFilter(p)}
              className={`px-3 py-1 text-xs rounded-md font-medium capitalize transition-colors ${
                patternFilter === p ? "bg-indigo-600 text-white" : "text-slate-400 hover:text-white"
              }`}>{p.replace(/_/g, " ")}</button>
          ))}
        </div>
      </div>

      {/* Rep cards */}
      {loading ? (
        <div className="text-slate-400 text-sm">Loading…</div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
          {reps.map((rep) => (
            <button key={rep.rep_id} onClick={() => setSelectedRep(rep)}
              className={`text-left border rounded-xl p-4 transition-all hover:border-indigo-500 ${riskBg[rep.coverage_risk] ?? "bg-slate-900 border-slate-800"}`}>
              <div className="flex items-start justify-between mb-3">
                <div>
                  <div className="font-semibold text-white">{rep.rep_id}</div>
                  <div className="text-xs text-slate-400">{rep.region}</div>
                </div>
                <div className="text-right">
                  <div className={`text-xs font-bold uppercase ${riskColor[rep.coverage_risk] ?? "text-slate-400"}`}>
                    {rep.coverage_risk}
                  </div>
                  <div className={`text-xs ${severityColor[rep.coverage_severity] ?? "text-slate-400"} capitalize`}>
                    {rep.coverage_severity.replace(/_/g, " ")}
                  </div>
                </div>
              </div>
              <div className="space-y-2 mb-3">
                <ScoreBar label="Account Breadth" value={rep.account_breadth_score} colorKey="breadth" />
                <ScoreBar label="Prioritization" value={rep.account_prioritization_score} colorKey="prioritization" />
                <ScoreBar label="Whitespace" value={rep.whitespace_exploitation_score} colorKey="whitespace" />
                <ScoreBar label="Churn Prevention" value={rep.churn_prevention_score} colorKey="churn" />
              </div>
              <div className="flex items-center justify-between text-xs">
                <span className="text-slate-400 capitalize">{rep.coverage_pattern.replace(/_/g, " ")}</span>
                <span className="text-slate-300 font-mono">
                  composite {rep.territory_coverage_composite.toFixed(1)}
                </span>
              </div>
              {rep.estimated_revenue_at_risk_usd > 0 && (
                <div className="mt-2 text-xs text-rose-400">
                  Revenue at risk ${rep.estimated_revenue_at_risk_usd.toLocaleString()}
                </div>
              )}
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
