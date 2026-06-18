"use client";

import { useEffect, useState, useCallback } from "react";

// ─── Types ───────────────────────────────────────────────────────────────────

interface Rep {
  rep_id: string;
  region: string;
  quota_risk: string;
  quota_pattern: string;
  quota_severity: string;
  recommended_action: string;
  attainment_consistency_score: number;
  deal_quality_score: number;
  pipeline_health_score: number;
  forecast_reliability_score: number;
  quota_effectiveness_composite: number;
  is_below_quota_threshold: boolean;
  requires_performance_intervention: boolean;
  estimated_quota_gap_usd: number;
  quota_signal: string;
}

interface Summary {
  total: number;
  risk_counts: Record<string, number>;
  pattern_counts: Record<string, number>;
  severity_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_quota_effectiveness_composite: number;
  below_quota_threshold_count: number;
  performance_intervention_count: number;
  avg_attainment_consistency_score: number;
  avg_deal_quality_score: number;
  avg_pipeline_health_score: number;
  avg_forecast_reliability_score: number;
  total_estimated_quota_gap_usd: number;
}

// ─── Helpers ─────────────────────────────────────────────────────────────────

const riskColor: Record<string, string> = {
  low: "text-emerald-400", moderate: "text-yellow-400",
  high: "text-orange-400", critical: "text-red-400",
};
const riskBorder: Record<string, string> = {
  low: "border-emerald-500/30", moderate: "border-yellow-500/30",
  high: "border-orange-500/30", critical: "border-red-500/30",
};
const riskBg: Record<string, string> = {
  low: "bg-emerald-500/10", moderate: "bg-yellow-500/10",
  high: "bg-orange-500/10", critical: "bg-red-500/10",
};

function fmtUSD(v: number): string {
  if (v >= 1_000_000) return `$${(v / 1_000_000).toFixed(1)}M`;
  if (v >= 1_000)     return `$${(v / 1_000).toFixed(0)}K`;
  return `$${v.toFixed(0)}`;
}

// ─── Gauge Ring ───────────────────────────────────────────────────────────────

function GaugeRing({ label, value, max = 100 }: { label: string; value: number; max?: number }) {
  const pct = Math.min(value / max, 1);
  const r = 36, cx = 44, cy = 44;
  const circ = 2 * Math.PI * r;
  const dash = circ * pct;
  const color = pct < 0.2 ? "#34d399" : pct < 0.4 ? "#facc15" : pct < 0.6 ? "#fb923c" : "#f87171";
  return (
    <div className="flex flex-col items-center gap-1">
      <svg width={88} height={88} className="-rotate-90">
        <circle cx={cx} cy={cy} r={r} fill="none" stroke="#1e293b" strokeWidth={8} />
        <circle cx={cx} cy={cy} r={r} fill="none" stroke={color} strokeWidth={8}
          strokeDasharray={`${dash} ${circ}`} strokeLinecap="round" />
      </svg>
      <span className="text-base font-bold text-slate-100 -mt-10">{value.toFixed(1)}</span>
      <span className="text-xs text-slate-400 mt-8 text-center leading-tight">{label}</span>
    </div>
  );
}

// ─── Score Bar ────────────────────────────────────────────────────────────────

function ScoreBar({ label, value }: { label: string; value: number }) {
  const pct = Math.min(value, 100);
  const color = pct < 20 ? "bg-emerald-500" : pct < 40 ? "bg-yellow-500" : pct < 60 ? "bg-orange-500" : "bg-red-500";
  return (
    <div className="space-y-1">
      <div className="flex justify-between text-xs text-slate-400">
        <span>{label}</span><span className="font-medium text-slate-200">{value.toFixed(1)}</span>
      </div>
      <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
        <div className={`h-full rounded-full ${color}`} style={{ width: `${pct}%` }} />
      </div>
    </div>
  );
}

// ─── Distribution Bar ─────────────────────────────────────────────────────────

function DistBar({ title, counts, colors }: { title: string; counts: Record<string, number>; colors: Record<string, string> }) {
  const total = Object.values(counts).reduce((a, b) => a + b, 0) || 1;
  return (
    <div className="space-y-2">
      <p className="text-xs font-medium text-slate-400 uppercase tracking-wider">{title}</p>
      <div className="flex h-2 rounded-full overflow-hidden gap-0.5">
        {Object.entries(counts).map(([k, v]) => (
          <div key={k} className={colors[k] || "bg-slate-600"} style={{ width: `${(v / total) * 100}%` }} title={`${k}: ${v}`} />
        ))}
      </div>
      <div className="flex flex-wrap gap-x-3 gap-y-1">
        {Object.entries(counts).map(([k, v]) => (
          <span key={k} className="text-xs text-slate-400">
            <span className={`font-medium ${colors[k]?.replace("bg-", "text-") || "text-slate-300"}`}>{v}</span> {k.replace(/_/g, " ")}
          </span>
        ))}
      </div>
    </div>
  );
}

// ─── Detail Modal ─────────────────────────────────────────────────────────────

function DetailModal({ rep, onClose }: { rep: Rep; onClose: () => void }) {
  const [tab, setTab] = useState<"scores" | "signals" | "action">("scores");

  useEffect(() => {
    const handler = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [onClose]);

  const actionLabels: Record<string, string> = {
    no_action: "No Action Required",
    quota_coaching: "Quota Attainment Coaching",
    performance_plan: "Formal Performance Improvement Plan",
    sandbagging_review: "Sandbagging Pattern Review",
    deal_acceleration: "Deal Acceleration Program",
    quota_adjustment: "Quota Territory Adjustment",
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm"
      onClick={onClose}>
      <div className="relative w-full max-w-lg bg-slate-900 border border-slate-700 rounded-2xl shadow-2xl p-6"
        onClick={(e) => e.stopPropagation()}>
        <button onClick={onClose} className="absolute top-4 right-4 text-slate-500 hover:text-slate-200 text-lg">✕</button>
        <div className="mb-4">
          <h3 className="text-lg font-bold text-slate-100">{rep.rep_id}</h3>
          <p className="text-sm text-slate-400">{rep.region} · <span className={riskColor[rep.quota_risk] || "text-slate-300"}>{rep.quota_risk.toUpperCase()}</span></p>
        </div>
        <div className="flex gap-2 mb-4">
          {(["scores", "signals", "action"] as const).map((t) => (
            <button key={t} onClick={() => setTab(t)}
              className={`px-3 py-1 rounded-lg text-xs font-medium transition-colors ${tab === t ? "bg-indigo-600 text-white" : "bg-slate-800 text-slate-400 hover:text-slate-200"}`}>
              {t.charAt(0).toUpperCase() + t.slice(1)}
            </button>
          ))}
        </div>
        {tab === "scores" && (
          <div className="space-y-3">
            <ScoreBar label="Attainment Consistency Score" value={rep.attainment_consistency_score} />
            <ScoreBar label="Deal Quality Score" value={rep.deal_quality_score} />
            <ScoreBar label="Pipeline Health Score" value={rep.pipeline_health_score} />
            <ScoreBar label="Forecast Reliability Score" value={rep.forecast_reliability_score} />
            <div className="pt-2 border-t border-slate-800">
              <ScoreBar label="Composite" value={rep.quota_effectiveness_composite} />
            </div>
          </div>
        )}
        {tab === "signals" && (
          <div className="space-y-3 text-sm">
            <p className="text-slate-300 leading-relaxed">{rep.quota_signal}</p>
            <div className="grid grid-cols-2 gap-2 pt-2">
              <div className="bg-slate-800/60 rounded-lg p-3">
                <p className="text-xs text-slate-500 mb-1">Severity</p>
                <p className="font-medium text-slate-200 capitalize">{rep.quota_severity.replace(/_/g, " ")}</p>
              </div>
              <div className="bg-slate-800/60 rounded-lg p-3">
                <p className="text-xs text-slate-500 mb-1">Pattern</p>
                <p className="font-medium text-slate-200 capitalize">{rep.quota_pattern.replace(/_/g, " ")}</p>
              </div>
              <div className="bg-slate-800/60 rounded-lg p-3">
                <p className="text-xs text-slate-500 mb-1">Below Threshold</p>
                <p className={`font-medium ${rep.is_below_quota_threshold ? "text-red-400" : "text-emerald-400"}`}>
                  {rep.is_below_quota_threshold ? "Yes" : "No"}
                </p>
              </div>
              <div className="bg-slate-800/60 rounded-lg p-3">
                <p className="text-xs text-slate-500 mb-1">Quota Gap</p>
                <p className="font-medium text-orange-400">{fmtUSD(rep.estimated_quota_gap_usd)}</p>
              </div>
            </div>
          </div>
        )}
        {tab === "action" && (
          <div className="space-y-3">
            <div className="bg-indigo-500/10 border border-indigo-500/30 rounded-xl p-4">
              <p className="text-xs text-indigo-400 mb-1 font-medium uppercase tracking-wider">Recommended Action</p>
              <p className="text-slate-100 font-semibold">{actionLabels[rep.recommended_action] || rep.recommended_action}</p>
            </div>
            <div className="flex gap-2">
              <span className={`px-2 py-1 rounded text-xs font-medium ${riskBg[rep.quota_risk]} ${riskColor[rep.quota_risk]}`}>
                {rep.quota_risk} risk
              </span>
              {rep.requires_performance_intervention && (
                <span className="px-2 py-1 rounded text-xs font-medium bg-red-500/10 text-red-400">Intervention Needed</span>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

// ─── Main Page ────────────────────────────────────────────────────────────────

export default function SalesQuotaAttainmentPage() {
  const [data, setData] = useState<{ reps: Rep[]; summary: Summary } | null>(null);
  const [riskFilter, setRiskFilter]       = useState("");
  const [patternFilter, setPatternFilter] = useState("");
  const [selectedRep, setSelectedRep]     = useState<Rep | null>(null);

  const load = useCallback(async () => {
    const params = new URLSearchParams();
    if (riskFilter)    params.set("risk", riskFilter);
    if (patternFilter) params.set("pattern", patternFilter);
    const res = await fetch(`/api/sales-quota-attainment-intelligence-engine?${params}`);
    if (res.ok) setData(await res.json());
  }, [riskFilter, patternFilter]);

  useEffect(() => { load(); }, [load]);

  if (!data) return (
    <div className="flex items-center justify-center h-64">
      <div className="w-8 h-8 border-2 border-indigo-500 border-t-transparent rounded-full animate-spin" />
    </div>
  );

  const { reps, summary } = data;

  const riskColors     = { low: "bg-emerald-500", moderate: "bg-yellow-500", high: "bg-orange-500", critical: "bg-red-500" } as Record<string, string>;
  const patternColors  = { none: "bg-slate-500", consistent_underperformance: "bg-red-500", sandbagging: "bg-violet-500", late_quarter_surge: "bg-orange-500", early_drop_off: "bg-yellow-500", quota_avoidance: "bg-pink-500" } as Record<string, string>;
  const severityColors = { on_track: "bg-emerald-500", developing: "bg-yellow-500", at_risk: "bg-orange-500", critical: "bg-red-500" } as Record<string, string>;

  const distributions: Array<{ title: string; counts: Record<string, number>; colors: Record<string, string> }> = [
    { title: "Risk Distribution", counts: summary.risk_counts, colors: riskColors },
    { title: "Pattern Distribution", counts: summary.pattern_counts, colors: patternColors },
    { title: "Severity Distribution", counts: summary.severity_counts, colors: severityColors },
  ];

  const RISKS    = ["low", "moderate", "high", "critical"];
  const PATTERNS = ["none", "consistent_underperformance", "sandbagging", "late_quarter_surge", "early_drop_off", "quota_avoidance"];

  return (
    <div className="space-y-6 p-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-slate-100">Quota Attainment Intelligence</h1>
        <p className="text-slate-400 text-sm mt-1">Track quota consistency, deal quality patterns, pipeline health, and forecast reliability across your team</p>
      </div>

      {/* KPI Strip */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        {[
          { label: "Total Reps", value: summary.total, sub: "monitored" },
          { label: "Below Threshold", value: summary.below_quota_threshold_count, sub: "reps", color: "text-red-400" },
          { label: "Need Intervention", value: summary.performance_intervention_count, sub: "reps", color: "text-orange-400" },
          { label: "Total Quota Gap", value: fmtUSD(summary.total_estimated_quota_gap_usd), sub: "estimated exposure", color: "text-violet-400" },
        ].map(({ label, value, sub, color }) => (
          <div key={label} className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <p className="text-xs text-slate-500 uppercase tracking-wider mb-1">{label}</p>
            <p className={`text-2xl font-bold ${color || "text-slate-100"}`}>{value}</p>
            <p className="text-xs text-slate-500 mt-1">{sub}</p>
          </div>
        ))}
      </div>

      {/* Gauge Rings */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
        <h2 className="text-sm font-semibold text-slate-300 uppercase tracking-wider mb-6">Avg Score Components</h2>
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-6 justify-items-center">
          <GaugeRing label="Attainment Consist." value={summary.avg_attainment_consistency_score} />
          <GaugeRing label="Deal Quality" value={summary.avg_deal_quality_score} />
          <GaugeRing label="Pipeline Health" value={summary.avg_pipeline_health_score} />
          <GaugeRing label="Forecast Reliability" value={summary.avg_forecast_reliability_score} />
        </div>
      </div>

      {/* Distributions */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-5">
        <h2 className="text-sm font-semibold text-slate-300 uppercase tracking-wider">Distributions</h2>
        {distributions.map((d) => <DistBar key={d.title} {...d} />)}
      </div>

      {/* Filters */}
      <div className="flex flex-wrap gap-3">
        <div className="flex gap-1 flex-wrap">
          <span className="text-xs text-slate-500 self-center mr-1">Risk:</span>
          {["", ...RISKS].map((r) => (
            <button key={r} onClick={() => setRiskFilter(r)}
              className={`px-3 py-1 rounded-lg text-xs font-medium transition-colors ${riskFilter === r ? "bg-indigo-600 text-white" : "bg-slate-800 text-slate-400 hover:text-slate-200"}`}>
              {r || "All"}
            </button>
          ))}
        </div>
        <div className="flex gap-1 flex-wrap">
          <span className="text-xs text-slate-500 self-center mr-1">Pattern:</span>
          {["", ...PATTERNS].map((p) => (
            <button key={p} onClick={() => setPatternFilter(p)}
              className={`px-3 py-1 rounded-lg text-xs font-medium transition-colors ${patternFilter === p ? "bg-violet-600 text-white" : "bg-slate-800 text-slate-400 hover:text-slate-200"}`}>
              {p ? p.replace(/_/g, " ") : "All"}
            </button>
          ))}
        </div>
      </div>

      {/* Rep Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
        {reps.map((rep) => (
          <button key={rep.rep_id} onClick={() => setSelectedRep(rep)} className="text-left w-full">
            <div className={`bg-slate-900 border rounded-xl p-4 hover:border-slate-600 transition-colors ${riskBorder[rep.quota_risk] || "border-slate-800"}`}>
              <div className="flex justify-between items-start mb-3">
                <div>
                  <p className="font-semibold text-slate-100">{rep.rep_id}</p>
                  <p className="text-xs text-slate-400">{rep.region}</p>
                </div>
                <div className="text-right">
                  <span className={`text-xs font-bold px-2 py-0.5 rounded ${riskBg[rep.quota_risk]} ${riskColor[rep.quota_risk]}`}>
                    {rep.quota_risk.toUpperCase()}
                  </span>
                  <p className="text-xs text-slate-500 mt-1">composite {rep.quota_effectiveness_composite.toFixed(1)}</p>
                </div>
              </div>
              <div className="space-y-2 mb-3">
                <ScoreBar label="Attainment Consistency" value={rep.attainment_consistency_score} />
                <ScoreBar label="Deal Quality" value={rep.deal_quality_score} />
                <ScoreBar label="Pipeline Health" value={rep.pipeline_health_score} />
                <ScoreBar label="Forecast Reliability" value={rep.forecast_reliability_score} />
              </div>
              <div className="flex justify-between items-center text-xs text-slate-500">
                <span className="capitalize">{rep.quota_pattern.replace(/_/g, " ")}</span>
                <span className="text-orange-400 font-medium">{fmtUSD(rep.estimated_quota_gap_usd)}</span>
              </div>
              {(rep.is_below_quota_threshold || rep.requires_performance_intervention) && (
                <div className="flex gap-1 mt-2">
                  {rep.is_below_quota_threshold && <span className="text-xs bg-red-500/10 text-red-400 px-2 py-0.5 rounded">Below Threshold</span>}
                  {rep.requires_performance_intervention && <span className="text-xs bg-orange-500/10 text-orange-400 px-2 py-0.5 rounded">Intervention</span>}
                </div>
              )}
            </div>
          </button>
        ))}
      </div>

      {selectedRep && <DetailModal rep={selectedRep} onClose={() => setSelectedRep(null)} />}
    </div>
  );
}
