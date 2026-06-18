"use client";

import { useEffect, useState, useCallback } from "react";

interface Rep {
  rep_id: string;
  region: string;
  proposal_risk: string;
  proposal_pattern: string;
  proposal_severity: string;
  recommended_action: string;
  proposal_win_rate_score: number;
  proposal_velocity_score: number;
  value_alignment_score: number;
  competitive_exposure_score: number;
  proposal_effectiveness_composite: number;
  is_win_rate_declining: boolean;
  requires_proposal_redesign: boolean;
  estimated_lost_revenue_usd: number;
  proposal_signal: string;
}

interface Summary {
  total: number;
  risk_counts: Record<string, number>;
  pattern_counts: Record<string, number>;
  severity_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_proposal_effectiveness_composite: number;
  declining_win_rate_count: number;
  proposal_redesign_count: number;
  avg_proposal_win_rate_score: number;
  avg_proposal_velocity_score: number;
  avg_value_alignment_score: number;
  avg_competitive_exposure_score: number;
  total_estimated_lost_revenue_usd: number;
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
  healthy: "text-emerald-400", declining: "text-amber-400",
  stalled: "text-orange-400", critical: "text-rose-400",
};
const scoreBarColor: Record<string, string> = {
  win_rate: "bg-indigo-500", velocity: "bg-violet-500",
  value: "bg-amber-500", competitive: "bg-rose-500",
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
                  ["Composite", rep.proposal_effectiveness_composite.toFixed(1)],
                  ["Risk", rep.proposal_risk],
                  ["Severity", rep.proposal_severity],
                  ["Pattern", rep.proposal_pattern.replace(/_/g, " ")],
                ].map(([k, v]) => (
                  <div key={k} className="bg-slate-800 rounded-lg p-3">
                    <div className="text-xs text-slate-400">{k}</div>
                    <div className="text-sm font-semibold text-white capitalize">{v}</div>
                  </div>
                ))}
              </div>
              <div className="space-y-3">
                <ScoreBar label="Win Rate Risk" value={rep.proposal_win_rate_score} colorKey="win_rate" />
                <ScoreBar label="Velocity Risk" value={rep.proposal_velocity_score} colorKey="velocity" />
                <ScoreBar label="Value Alignment Risk" value={rep.value_alignment_score} colorKey="value" />
                <ScoreBar label="Competitive Exposure" value={rep.competitive_exposure_score} colorKey="competitive" />
              </div>
              <div className="grid grid-cols-2 gap-2 pt-2">
                <div className="flex items-center gap-2 text-xs">
                  <span className={rep.is_win_rate_declining ? "text-rose-400" : "text-emerald-400"}>●</span>
                  <span className="text-slate-400">Win Rate {rep.is_win_rate_declining ? "Declining" : "Stable"}</span>
                </div>
                <div className="flex items-center gap-2 text-xs">
                  <span className={rep.requires_proposal_redesign ? "text-amber-400" : "text-emerald-400"}>●</span>
                  <span className="text-slate-400">{rep.requires_proposal_redesign ? "Redesign Needed" : "No Redesign"}</span>
                </div>
              </div>
            </>
          )}
          {tab === "signals" && (
            <div className="space-y-3">
              <div className="bg-slate-800 rounded-lg p-3">
                <div className="text-xs text-slate-400 mb-1">Signal</div>
                <div className="text-sm text-slate-200">{rep.proposal_signal}</div>
              </div>
              <div className="bg-slate-800 rounded-lg p-3">
                <div className="text-xs text-slate-400 mb-1">Est. Lost Revenue</div>
                <div className="text-sm font-bold text-rose-400">
                  ${rep.estimated_lost_revenue_usd.toLocaleString()}
                </div>
              </div>
              <div className="bg-slate-800 rounded-lg p-3">
                <div className="text-xs text-slate-400 mb-1">Pattern</div>
                <div className="text-sm font-medium text-amber-300 capitalize">
                  {rep.proposal_pattern.replace(/_/g, " ")}
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
                {rep.requires_proposal_redesign && (
                  <div className="flex items-start gap-2 bg-slate-800 rounded-lg p-3">
                    <span className="text-amber-400 mt-0.5">▲</span>
                    <span>Proposal redesign required — value messaging or structure needs overhaul</span>
                  </div>
                )}
                {rep.is_win_rate_declining && (
                  <div className="flex items-start gap-2 bg-slate-800 rounded-lg p-3">
                    <span className="text-rose-400 mt-0.5">↓</span>
                    <span>Win rate is declining — review deal qualification and proposal quality</span>
                  </div>
                )}
                {rep.proposal_pattern === "competitive_loss" && (
                  <div className="flex items-start gap-2 bg-slate-800 rounded-lg p-3">
                    <span className="text-orange-400 mt-0.5">⚔</span>
                    <span>Competitive losses detected — refresh battlecards and positioning</span>
                  </div>
                )}
                {rep.proposal_pattern === "budget_friction" && (
                  <div className="flex items-start gap-2 bg-slate-800 rounded-lg p-3">
                    <span className="text-violet-400 mt-0.5">$</span>
                    <span>Budget friction evident — consider pricing strategy and package options</span>
                  </div>
                )}
                {!rep.requires_proposal_redesign && !rep.is_win_rate_declining && rep.proposal_risk === "low" && (
                  <div className="flex items-start gap-2 bg-slate-800 rounded-lg p-3">
                    <span className="text-emerald-400 mt-0.5">✓</span>
                    <span>Proposal quality is healthy — maintain current approach</span>
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

export default function SalesProposalConversionIntelligenceEnginePage() {
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
    const res = await fetch(`/api/sales-proposal-conversion-intelligence-engine?${params}`);
    const data = await res.json();
    setReps(data.reps ?? []);
    setSummary(data.summary ?? null);
    setLoading(false);
  }, [riskFilter, patternFilter]);

  useEffect(() => { fetchData(); }, [fetchData]);

  const riskCounts = summary?.risk_counts ?? {};
  const patternCounts = summary?.pattern_counts ?? {};
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
        none: "bg-slate-500", poor_win_rate: "bg-amber-500", proposal_staleness: "bg-violet-500",
        value_misalignment: "bg-orange-500", competitive_loss: "bg-rose-500", budget_friction: "bg-indigo-500",
      } as Record<string, string>,
    },
    {
      title: "Severity Distribution",
      counts: severityCounts,
      colors: { healthy: "bg-emerald-500", declining: "bg-amber-500", stalled: "bg-orange-500", critical: "bg-rose-500" } as Record<string, string>,
    },
  ];

  return (
    <div className="space-y-6">
      {selectedRep && <DetailModal rep={selectedRep} onClose={() => setSelectedRep(null)} />}

      <div>
        <h1 className="text-2xl font-bold text-white">Proposal Conversion Intelligence</h1>
        <p className="text-slate-400 mt-1 text-sm">
          Win rate trends, proposal velocity, value alignment, and competitive exposure by rep.
        </p>
      </div>

      {/* KPI strip */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        {[
          { label: "Total Reps", value: summary?.total ?? 0, color: "text-indigo-400" },
          { label: "Declining Win Rate", value: summary?.declining_win_rate_count ?? 0, color: "text-rose-400" },
          { label: "Need Redesign", value: summary?.proposal_redesign_count ?? 0, color: "text-amber-400" },
          {
            label: "Est. Lost Revenue",
            value: `$${((summary?.total_estimated_lost_revenue_usd ?? 0) / 1000).toFixed(0)}k`,
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
        <GaugeRing value={summary?.avg_proposal_win_rate_score ?? 0} label="Avg Win Rate Risk" color="#6366f1" />
        <GaugeRing value={summary?.avg_proposal_velocity_score ?? 0} label="Avg Velocity Risk" color="#8b5cf6" />
        <GaugeRing value={summary?.avg_value_alignment_score ?? 0} label="Avg Value Alignment Risk" color="#f59e0b" />
        <GaugeRing value={summary?.avg_competitive_exposure_score ?? 0} label="Avg Competitive Exposure" color="#f43f5e" />
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
          {["all", "none", "poor_win_rate", "proposal_staleness", "value_misalignment", "competitive_loss", "budget_friction"].map((p) => (
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
              className={`text-left border rounded-xl p-4 transition-all hover:border-indigo-500 ${riskBg[rep.proposal_risk] ?? "bg-slate-900 border-slate-800"}`}>
              <div className="flex items-start justify-between mb-3">
                <div>
                  <div className="font-semibold text-white">{rep.rep_id}</div>
                  <div className="text-xs text-slate-400">{rep.region}</div>
                </div>
                <div className="text-right">
                  <div className={`text-xs font-bold uppercase ${riskColor[rep.proposal_risk] ?? "text-slate-400"}`}>
                    {rep.proposal_risk}
                  </div>
                  <div className={`text-xs ${severityColor[rep.proposal_severity] ?? "text-slate-400"} capitalize`}>
                    {rep.proposal_severity}
                  </div>
                </div>
              </div>
              <div className="space-y-2 mb-3">
                <ScoreBar label="Win Rate Risk" value={rep.proposal_win_rate_score} colorKey="win_rate" />
                <ScoreBar label="Velocity Risk" value={rep.proposal_velocity_score} colorKey="velocity" />
                <ScoreBar label="Value Alignment Risk" value={rep.value_alignment_score} colorKey="value" />
                <ScoreBar label="Competitive Exposure" value={rep.competitive_exposure_score} colorKey="competitive" />
              </div>
              <div className="flex items-center justify-between text-xs">
                <span className="text-slate-400 capitalize">{rep.proposal_pattern.replace(/_/g, " ")}</span>
                <span className="text-slate-300 font-mono">
                  composite {rep.proposal_effectiveness_composite.toFixed(1)}
                </span>
              </div>
              {rep.estimated_lost_revenue_usd > 0 && (
                <div className="mt-2 text-xs text-rose-400">
                  Est. lost ${rep.estimated_lost_revenue_usd.toLocaleString()}
                </div>
              )}
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
