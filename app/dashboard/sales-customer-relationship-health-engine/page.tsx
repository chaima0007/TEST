"use client";

import { useEffect, useState, useCallback } from "react";

interface Rep {
  rep_id: string;
  region: string;
  relationship_risk: string;
  relationship_pattern: string;
  relationship_severity: string;
  recommended_action: string;
  engagement_frequency_score: number;
  relationship_quality_score: number;
  account_health_score: number;
  strategic_depth_score: number;
  relationship_health_composite: number;
  is_relationship_at_risk: boolean;
  requires_csa_intervention: boolean;
  estimated_revenue_at_risk_usd: number;
  relationship_signal: string;
}

interface Summary {
  total: number;
  risk_counts: Record<string, number>;
  pattern_counts: Record<string, number>;
  severity_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_relationship_health_composite: number;
  relationship_at_risk_count: number;
  csa_intervention_count: number;
  avg_engagement_frequency_score: number;
  avg_relationship_quality_score: number;
  avg_account_health_score: number;
  avg_strategic_depth_score: number;
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
  healthy: "text-emerald-400", at_risk: "text-amber-400",
  degrading: "text-orange-400", critical: "text-rose-400",
};
const scoreBarColor: Record<string, string> = {
  frequency: "bg-indigo-500", quality: "bg-violet-500",
  health: "bg-amber-500", strategic: "bg-rose-500",
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
                  ["Composite", rep.relationship_health_composite.toFixed(1)],
                  ["Risk", rep.relationship_risk],
                  ["Severity", rep.relationship_severity],
                  ["Pattern", rep.relationship_pattern.replace(/_/g, " ")],
                ].map(([k, v]) => (
                  <div key={k} className="bg-slate-800 rounded-lg p-3">
                    <div className="text-xs text-slate-400">{k}</div>
                    <div className="text-sm font-semibold text-white capitalize">{v}</div>
                  </div>
                ))}
              </div>
              <div className="space-y-3">
                <ScoreBar label="Engagement Frequency Risk" value={rep.engagement_frequency_score} colorKey="frequency" />
                <ScoreBar label="Relationship Quality Risk" value={rep.relationship_quality_score} colorKey="quality" />
                <ScoreBar label="Account Health Risk" value={rep.account_health_score} colorKey="health" />
                <ScoreBar label="Strategic Depth Risk" value={rep.strategic_depth_score} colorKey="strategic" />
              </div>
              <div className="grid grid-cols-2 gap-2 pt-2">
                <div className="flex items-center gap-2 text-xs">
                  <span className={rep.is_relationship_at_risk ? "text-rose-400" : "text-emerald-400"}>●</span>
                  <span className="text-slate-400">{rep.is_relationship_at_risk ? "At Risk" : "Not at Risk"}</span>
                </div>
                <div className="flex items-center gap-2 text-xs">
                  <span className={rep.requires_csa_intervention ? "text-amber-400" : "text-emerald-400"}>●</span>
                  <span className="text-slate-400">{rep.requires_csa_intervention ? "CSA Needed" : "No CSA"}</span>
                </div>
              </div>
            </>
          )}
          {tab === "signals" && (
            <div className="space-y-3">
              <div className="bg-slate-800 rounded-lg p-3">
                <div className="text-xs text-slate-400 mb-1">Signal</div>
                <div className="text-sm text-slate-200">{rep.relationship_signal}</div>
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
                  {rep.relationship_pattern.replace(/_/g, " ")}
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
                {rep.requires_csa_intervention && (
                  <div className="flex items-start gap-2 bg-slate-800 rounded-lg p-3">
                    <span className="text-amber-400 mt-0.5">▲</span>
                    <span>CSA intervention required — escalate customer success involvement immediately</span>
                  </div>
                )}
                {rep.is_relationship_at_risk && (
                  <div className="flex items-start gap-2 bg-slate-800 rounded-lg p-3">
                    <span className="text-rose-400 mt-0.5">!</span>
                    <span>Relationship at risk — revenue impact likely without immediate corrective action</span>
                  </div>
                )}
                {rep.relationship_pattern === "relationship_decay" && (
                  <div className="flex items-start gap-2 bg-slate-800 rounded-lg p-3">
                    <span className="text-orange-400 mt-0.5">↓</span>
                    <span>NPS declining — initiate executive-level relationship recovery conversation</span>
                  </div>
                )}
                {rep.relationship_pattern === "executive_neglect" && (
                  <div className="flex items-start gap-2 bg-slate-800 rounded-lg p-3">
                    <span className="text-violet-400 mt-0.5">◆</span>
                    <span>Executive contacts not being engaged — schedule QBRs and sponsor briefings</span>
                  </div>
                )}
                {!rep.is_relationship_at_risk && !rep.requires_csa_intervention && rep.relationship_risk === "low" && (
                  <div className="flex items-start gap-2 bg-slate-800 rounded-lg p-3">
                    <span className="text-emerald-400 mt-0.5">✓</span>
                    <span>Relationships healthy — maintain engagement cadence and expand whitespace</span>
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

export default function SalesCustomerRelationshipHealthEnginePage() {
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
    const res = await fetch(`/api/sales-customer-relationship-health-engine?${params}`);
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
        none: "bg-slate-500", relationship_decay: "bg-rose-500", executive_neglect: "bg-violet-500",
        account_health_crisis: "bg-red-600", expansion_neglect: "bg-amber-500", qbr_backlog: "bg-orange-500",
      } as Record<string, string>,
    },
    {
      title: "Severity Distribution",
      counts: severityCounts,
      colors: { healthy: "bg-emerald-500", at_risk: "bg-amber-500", degrading: "bg-orange-500", critical: "bg-rose-500" } as Record<string, string>,
    },
  ];

  return (
    <div className="space-y-6">
      {selectedRep && <DetailModal rep={selectedRep} onClose={() => setSelectedRep(null)} />}

      <div>
        <h1 className="text-2xl font-bold text-white">Customer Relationship Health</h1>
        <p className="text-slate-400 mt-1 text-sm">
          Engagement frequency, relationship quality, account health, and strategic depth by rep.
        </p>
      </div>

      {/* KPI strip */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        {[
          { label: "Total Reps", value: summary?.total ?? 0, color: "text-indigo-400" },
          { label: "Relationships at Risk", value: summary?.relationship_at_risk_count ?? 0, color: "text-rose-400" },
          { label: "CSA Intervention Needed", value: summary?.csa_intervention_count ?? 0, color: "text-amber-400" },
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
        <GaugeRing value={summary?.avg_engagement_frequency_score ?? 0} label="Avg Frequency Risk" color="#6366f1" />
        <GaugeRing value={summary?.avg_relationship_quality_score ?? 0} label="Avg Quality Risk" color="#8b5cf6" />
        <GaugeRing value={summary?.avg_account_health_score ?? 0} label="Avg Account Health Risk" color="#f59e0b" />
        <GaugeRing value={summary?.avg_strategic_depth_score ?? 0} label="Avg Strategic Depth Risk" color="#f43f5e" />
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
          {["all", "none", "relationship_decay", "executive_neglect", "account_health_crisis", "expansion_neglect", "qbr_backlog"].map((p) => (
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
              className={`text-left border rounded-xl p-4 transition-all hover:border-indigo-500 ${riskBg[rep.relationship_risk] ?? "bg-slate-900 border-slate-800"}`}>
              <div className="flex items-start justify-between mb-3">
                <div>
                  <div className="font-semibold text-white">{rep.rep_id}</div>
                  <div className="text-xs text-slate-400">{rep.region}</div>
                </div>
                <div className="text-right">
                  <div className={`text-xs font-bold uppercase ${riskColor[rep.relationship_risk] ?? "text-slate-400"}`}>
                    {rep.relationship_risk}
                  </div>
                  <div className={`text-xs ${severityColor[rep.relationship_severity] ?? "text-slate-400"} capitalize`}>
                    {rep.relationship_severity.replace(/_/g, " ")}
                  </div>
                </div>
              </div>
              <div className="space-y-2 mb-3">
                <ScoreBar label="Engagement Frequency" value={rep.engagement_frequency_score} colorKey="frequency" />
                <ScoreBar label="Relationship Quality" value={rep.relationship_quality_score} colorKey="quality" />
                <ScoreBar label="Account Health" value={rep.account_health_score} colorKey="health" />
                <ScoreBar label="Strategic Depth" value={rep.strategic_depth_score} colorKey="strategic" />
              </div>
              <div className="flex items-center justify-between text-xs">
                <span className="text-slate-400 capitalize">{rep.relationship_pattern.replace(/_/g, " ")}</span>
                <span className="text-slate-300 font-mono">
                  composite {rep.relationship_health_composite.toFixed(1)}
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
