"use client";

import { useEffect, useState } from "react";

interface GamingRep {
  rep_id: string;
  region: string;
  quota_gaming_risk: string;
  gaming_pattern: string;
  gaming_severity: string;
  recommended_action: string;
  timing_manipulation_score: number;
  pipeline_integrity_score: number;
  compensation_gaming_score: number;
  reporting_distortion_score: number;
  gaming_composite: number;
  is_gaming_quota: boolean;
  requires_comp_audit: boolean;
  estimated_inflated_pipeline_usd: number;
  gaming_signal: string;
}

interface Summary {
  total: number;
  risk_counts: Record<string, number>;
  pattern_counts: Record<string, number>;
  severity_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_gaming_composite: number;
  gaming_count: number;
  comp_audit_count: number;
  avg_timing_manipulation_score: number;
  avg_pipeline_integrity_score: number;
  avg_compensation_gaming_score: number;
  avg_reporting_distortion_score: number;
  total_estimated_inflated_pipeline_usd: number;
}

const RISK_COLORS: Record<string, string> = {
  low:      "text-emerald-400",
  moderate: "text-amber-400",
  high:     "text-orange-400",
  critical: "text-red-400",
};
const RISK_BG: Record<string, string> = {
  low:      "bg-emerald-400/10 border-emerald-400/30",
  moderate: "bg-amber-400/10 border-amber-400/30",
  high:     "bg-orange-400/10 border-orange-400/30",
  critical: "bg-red-400/10 border-red-400/30",
};
const SEV_COLORS: Record<string, string> = {
  clean:     "bg-emerald-500",
  watch:     "bg-amber-500",
  suspicious: "bg-orange-500",
  confirmed: "bg-red-500",
};
const PATTERN_LABELS: Record<string, string> = {
  none:                     "No Issues",
  pull_forward_abuse:       "Pull Forward Abuse",
  pipeline_inflation:       "Pipeline Inflation",
  close_date_manipulation:  "Close Date Manipulation",
  quota_anchor_gaming:      "Quota Anchor Gaming",
  comp_period_stuffing:     "Comp Period Stuffing",
};
const ACTION_LABELS: Record<string, string> = {
  no_action:             "No Action",
  manager_review:        "Manager Review",
  comp_plan_audit:       "Comp Plan Audit",
  quota_recalibration:   "Quota Recalibration",
  compensation_clawback: "Compensation Clawback",
};

function ScoreBar({ label, value, color = "bg-indigo-500" }: { label: string; value: number; color?: string }) {
  return (
    <div>
      <div className="flex justify-between text-xs mb-1">
        <span className="text-slate-400">{label}</span>
        <span className="text-slate-200 font-mono">{value.toFixed(1)}</span>
      </div>
      <div className="h-1.5 rounded-full bg-slate-800">
        <div className={`h-1.5 rounded-full ${color}`} style={{ width: `${Math.min(value, 100)}%` }} />
      </div>
    </div>
  );
}

function GamingRing({ composite }: { composite: number }) {
  const r = 36;
  const circ = 2 * Math.PI * r;
  const fill = (composite / 100) * circ;
  const color = composite >= 60 ? "#f87171" : composite >= 40 ? "#fb923c" : composite >= 20 ? "#fbbf24" : "#34d399";
  return (
    <svg viewBox="0 0 88 88" className="w-20 h-20">
      <circle cx="44" cy="44" r={r} fill="none" stroke="#1e293b" strokeWidth="8" />
      <circle
        cx="44" cy="44" r={r} fill="none"
        stroke={color} strokeWidth="8"
        strokeDasharray={`${fill} ${circ}`}
        strokeLinecap="round"
        transform="rotate(-90 44 44)"
      />
      <text x="44" y="49" textAnchor="middle" fontSize="14" fontWeight="700" fill={color}>
        {composite.toFixed(0)}
      </text>
    </svg>
  );
}

function fmt(n: number): string {
  if (n >= 1_000_000) return `$${(n / 1_000_000).toFixed(1)}M`;
  if (n >= 1_000) return `$${(n / 1_000).toFixed(0)}K`;
  return `$${n.toFixed(0)}`;
}

function DetailModal({ rep, onClose }: { rep: GamingRep; onClose: () => void }) {
  const [tab, setTab] = useState<"overview" | "scores" | "action">("overview");
  useEffect(() => {
    const handler = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [onClose]);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm" onClick={onClose}>
      <div className="relative bg-slate-900 border border-slate-700 rounded-2xl shadow-2xl w-full max-w-lg mx-4 overflow-hidden" onClick={(e) => e.stopPropagation()}>
        <div className="flex items-center justify-between px-6 py-4 border-b border-slate-800">
          <div>
            <p className="text-xs text-slate-500 uppercase tracking-widest">Quota Gaming</p>
            <h2 className="text-lg font-bold text-slate-100">{rep.rep_id}</h2>
            <p className="text-xs text-slate-400">{rep.region} · {PATTERN_LABELS[rep.gaming_pattern]}</p>
          </div>
          <div className="flex flex-col items-end gap-1">
            <span className={`text-xs font-semibold px-2 py-0.5 rounded-full border ${RISK_BG[rep.quota_gaming_risk]}`}>
              <span className={RISK_COLORS[rep.quota_gaming_risk]}>{rep.quota_gaming_risk.toUpperCase()}</span>
            </span>
            <span className={`text-xs px-2 py-0.5 rounded-full text-white ${SEV_COLORS[rep.gaming_severity]}`}>
              {rep.gaming_severity}
            </span>
            <button onClick={onClose} className="text-slate-500 hover:text-slate-200 text-xl leading-none mt-1">×</button>
          </div>
        </div>

        <div className="flex border-b border-slate-800">
          {(["overview", "scores", "action"] as const).map((t) => (
            <button key={t} onClick={() => setTab(t)}
              className={`flex-1 py-2 text-xs font-semibold uppercase tracking-widest transition-colors ${tab === t ? "text-indigo-400 border-b-2 border-indigo-400" : "text-slate-500 hover:text-slate-300"}`}>
              {t}
            </button>
          ))}
        </div>

        <div className="px-6 py-5 space-y-4">
          {tab === "overview" && (
            <>
              <div className="flex items-center justify-center py-2">
                <GamingRing composite={rep.gaming_composite} />
              </div>
              <p className="text-sm text-slate-300 italic text-center">&ldquo;{rep.gaming_signal}&rdquo;</p>
              <div className="grid grid-cols-2 gap-3 text-xs">
                <div className="bg-slate-800 rounded-lg p-3">
                  <p className="text-slate-500 mb-1">Composite</p>
                  <p className="text-slate-100 font-bold text-base">{rep.gaming_composite.toFixed(1)}</p>
                </div>
                <div className="bg-slate-800 rounded-lg p-3">
                  <p className="text-slate-500 mb-1">Inflated Pipeline</p>
                  <p className="text-red-400 font-bold text-base">{fmt(rep.estimated_inflated_pipeline_usd)}</p>
                </div>
                <div className="bg-slate-800 rounded-lg p-3">
                  <p className="text-slate-500 mb-1">Gaming Confirmed</p>
                  <p className={`font-bold ${rep.is_gaming_quota ? "text-red-400" : "text-emerald-400"}`}>
                    {rep.is_gaming_quota ? "Yes" : "No"}
                  </p>
                </div>
                <div className="bg-slate-800 rounded-lg p-3">
                  <p className="text-slate-500 mb-1">Comp Audit</p>
                  <p className={`font-bold ${rep.requires_comp_audit ? "text-orange-400" : "text-emerald-400"}`}>
                    {rep.requires_comp_audit ? "Required" : "Not needed"}
                  </p>
                </div>
              </div>
            </>
          )}
          {tab === "scores" && (
            <div className="space-y-3">
              <ScoreBar label="Timing Manipulation" value={rep.timing_manipulation_score} color="bg-violet-500" />
              <ScoreBar label="Pipeline Integrity" value={rep.pipeline_integrity_score} color="bg-amber-500" />
              <ScoreBar label="Compensation Gaming" value={rep.compensation_gaming_score} color="bg-orange-500" />
              <ScoreBar label="Reporting Distortion" value={rep.reporting_distortion_score} color="bg-red-500" />
              <div className="pt-2 border-t border-slate-800">
                <ScoreBar label="Gaming Composite" value={rep.gaming_composite} color="bg-indigo-500" />
              </div>
            </div>
          )}
          {tab === "action" && (
            <div className="space-y-3 text-sm">
              <div className="bg-slate-800 rounded-lg p-4">
                <p className="text-slate-500 text-xs mb-1">Recommended Action</p>
                <p className="text-indigo-300 font-semibold">{ACTION_LABELS[rep.recommended_action]}</p>
              </div>
              <div className="bg-slate-800 rounded-lg p-4">
                <p className="text-slate-500 text-xs mb-1">Gaming Pattern</p>
                <p className="text-slate-200">{PATTERN_LABELS[rep.gaming_pattern]}</p>
              </div>
              <div className="bg-slate-800 rounded-lg p-4">
                <p className="text-slate-500 text-xs mb-1">Severity</p>
                <p className="text-slate-200 capitalize">{rep.gaming_severity}</p>
              </div>
              <div className="bg-slate-800 rounded-lg p-4">
                <p className="text-slate-500 text-xs mb-2">Flags</p>
                <div className="flex flex-wrap gap-2">
                  {rep.is_gaming_quota && <span className="text-xs px-2 py-0.5 rounded-full bg-red-400/10 border border-red-400/30 text-red-400">Gaming Confirmed</span>}
                  {rep.requires_comp_audit && <span className="text-xs px-2 py-0.5 rounded-full bg-orange-400/10 border border-orange-400/30 text-orange-400">Comp Audit Required</span>}
                  {!rep.is_gaming_quota && !rep.requires_comp_audit && <span className="text-xs text-slate-500">No critical flags</span>}
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default function QuotaGamingPage() {
  const [data, setData] = useState<{ reps: GamingRep[]; summary: Summary } | null>(null);
  const [selected, setSelected] = useState<GamingRep | null>(null);
  const [riskFilter, setRiskFilter] = useState("all");

  useEffect(() => {
    async function load() {
        const params = new URLSearchParams();
        if (riskFilter !== "all") params.set("risk", riskFilter);
        const res = await fetch(`/api/sales-quota-gaming-detection-engine?${params}`);
        setData(await res.json());
  }
    load();
  }, [riskFilter]);

  const summary = data?.summary;
  const reps = data?.reps ?? [];

  const kpis = summary
    ? [
        { label: "Total Reps", value: summary.total, sub: "evaluated" },
        { label: "Gaming Confirmed", value: summary.gaming_count, sub: "cases", accent: "text-red-400" },
        { label: "Comp Audits", value: summary.comp_audit_count, sub: "required", accent: "text-orange-400" },
        { label: "Avg Composite", value: summary.avg_gaming_composite.toFixed(1), sub: "gaming score" },
        { label: "Inflated Pipeline", value: fmt(summary.total_estimated_inflated_pipeline_usd), sub: "estimated total", accent: "text-amber-400" },
      ]
    : [];

  const patterns = summary
    ? Object.entries(summary.pattern_counts).sort((a, b) => b[1] - a[1])
    : [];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {selected && <DetailModal rep={selected} onClose={() => setSelected(null)} />}

      <div>
        <h1 className="text-2xl font-bold text-slate-100">Sales Quota Gaming Detection Engine</h1>
        <p className="text-sm text-slate-400 mt-1">Detects deal timing manipulation, pipeline inflation, and comp plan abuse distorting quota attainment metrics</p>
      </div>

      {/* KPI Strip */}
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-4">
        {kpis.map((k) => (
          <div key={k.label} className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <p className="text-xs text-slate-500 uppercase tracking-widest mb-1">{k.label}</p>
            <p className={`text-2xl font-bold ${k.accent ?? "text-slate-100"}`}>{k.value}</p>
            <p className="text-xs text-slate-500 mt-0.5">{k.sub}</p>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {summary && (
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-3">
            <h2 className="text-sm font-semibold text-slate-300 uppercase tracking-widest mb-3">Avg Risk Scores</h2>
            <ScoreBar label="Timing Manipulation" value={summary.avg_timing_manipulation_score} color="bg-violet-500" />
            <ScoreBar label="Pipeline Integrity" value={summary.avg_pipeline_integrity_score} color="bg-amber-500" />
            <ScoreBar label="Compensation Gaming" value={summary.avg_compensation_gaming_score} color="bg-orange-500" />
            <ScoreBar label="Reporting Distortion" value={summary.avg_reporting_distortion_score} color="bg-red-500" />
            <ScoreBar label="Gaming Composite" value={summary.avg_gaming_composite} color="bg-indigo-500" />
          </div>
        )}

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
          <h2 className="text-sm font-semibold text-slate-300 uppercase tracking-widest mb-4">Gaming Patterns</h2>
          <div className="space-y-2">
            {patterns.map(([pat, count]) => (
              <div key={pat} className="flex items-center gap-3">
                <span className="text-xs text-slate-400 w-44 truncate">{PATTERN_LABELS[pat] ?? pat}</span>
                <div className="flex-1 h-2 bg-slate-800 rounded-full">
                  <div
                    className="h-2 rounded-full bg-indigo-500"
                    style={{ width: summary ? `${(count / summary.total) * 100}%` : "0%" }}
                  />
                </div>
                <span className="text-xs font-mono text-slate-300 w-4 text-right">{count}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="flex gap-2 flex-wrap">
        {["all", "low", "moderate", "high", "critical"].map((f) => (
          <button key={f} onClick={() => setRiskFilter(f)}
            className={`px-4 py-1.5 rounded-full text-xs font-semibold border transition-colors ${
              riskFilter === f
                ? "bg-indigo-600 border-indigo-500 text-white"
                : "bg-slate-800 border-slate-700 text-slate-400 hover:text-slate-200"
            }`}>
            {f === "all" ? "All" : f.charAt(0).toUpperCase() + f.slice(1)}
          </button>
        ))}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
        {reps.map((rep) => (
          <button key={rep.rep_id} onClick={() => setSelected(rep)}
            className="bg-slate-900 border border-slate-800 rounded-xl p-4 text-left hover:border-indigo-500/50 transition-colors group">
            <div className="flex items-start justify-between mb-3">
              <div>
                <p className="font-semibold text-slate-100 group-hover:text-indigo-300 transition-colors">{rep.rep_id}</p>
                <p className="text-xs text-slate-500">{rep.region}</p>
              </div>
              <div className="flex flex-col items-end gap-1">
                <span className={`text-xs font-semibold ${RISK_COLORS[rep.quota_gaming_risk]}`}>
                  {rep.quota_gaming_risk.toUpperCase()}
                </span>
                <span className={`text-xs px-1.5 py-0.5 rounded text-white ${SEV_COLORS[rep.gaming_severity]}`}>
                  {rep.gaming_severity}
                </span>
              </div>
            </div>
            <div className="flex items-center gap-3 mb-3">
              <GamingRing composite={rep.gaming_composite} />
              <div className="flex-1 space-y-1.5">
                <ScoreBar label="Timing" value={rep.timing_manipulation_score} color="bg-violet-500" />
                <ScoreBar label="Pipeline" value={rep.pipeline_integrity_score} color="bg-amber-500" />
                <ScoreBar label="Comp" value={rep.compensation_gaming_score} color="bg-orange-500" />
              </div>
            </div>
            <p className="text-xs text-slate-400 italic leading-snug line-clamp-2">{rep.gaming_signal}</p>
            <div className="flex gap-2 mt-3 flex-wrap">
              {rep.is_gaming_quota && (
                <span className="text-xs px-2 py-0.5 rounded-full bg-red-400/10 border border-red-400/30 text-red-400">Gaming</span>
              )}
              {rep.requires_comp_audit && (
                <span className="text-xs px-2 py-0.5 rounded-full bg-orange-400/10 border border-orange-400/30 text-orange-400">Comp Audit</span>
              )}
              <span className="text-xs px-2 py-0.5 rounded-full bg-slate-800 text-slate-400">
                {fmt(rep.estimated_inflated_pipeline_usd)}
              </span>
            </div>
          </button>
        ))}
      </div>
    </div>
  );
}
