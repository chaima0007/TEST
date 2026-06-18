"use client";
import { useEffect, useState, useCallback } from "react";

// ─── types ───────────────────────────────────────────────────────────────────

interface Rep {
  rep_id: string;
  region: string;
  reference_risk: string;
  reference_pattern: string;
  reference_severity: string;
  recommended_action: string;
  reference_utilization_score: number;
  evidence_diversity_score: number;
  reference_timing_score: number;
  evidence_depth_score: number;
  reference_composite: number;
  has_reference_gap: boolean;
  requires_reference_coaching: boolean;
  estimated_win_rate_impact_usd: number;
  reference_signal: string;
}

interface Summary {
  total: number;
  risk_counts: Record<string, number>;
  pattern_counts: Record<string, number>;
  severity_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_reference_composite: number;
  reference_gap_count: number;
  coaching_count: number;
  avg_reference_utilization_score: number;
  avg_evidence_diversity_score: number;
  avg_reference_timing_score: number;
  avg_evidence_depth_score: number;
  total_estimated_win_rate_impact_usd: number;
}

// ─── helpers ─────────────────────────────────────────────────────────────────

const RISK_COLORS: Record<string, string> = {
  low: "text-emerald-400",
  moderate: "text-yellow-400",
  high: "text-orange-400",
  critical: "text-red-400",
};
const RISK_BORDER: Record<string, string> = {
  low: "border-emerald-700",
  moderate: "border-yellow-700",
  high: "border-orange-700",
  critical: "border-red-700",
};
const RISK_BG: Record<string, string> = {
  low: "bg-emerald-900/20",
  moderate: "bg-yellow-900/20",
  high: "bg-orange-900/20",
  critical: "bg-red-900/20",
};

const fmtUSD = (v: number) =>
  v >= 1_000_000
    ? `$${(v / 1_000_000).toFixed(1)}M`
    : v >= 1_000
    ? `$${(v / 1_000).toFixed(0)}K`
    : `$${v.toFixed(0)}`;

const fmtPct = (v: number) => `${v.toFixed(1)}%`;

const labelify = (s: string) =>
  s.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());

// ─── gauge ring ──────────────────────────────────────────────────────────────

function GaugeRing({ label, value, color }: { label: string; value: number; color: string }) {
  const r = 36;
  const circ = 2 * Math.PI * r;
  const dash = Math.min(value / 100, 1) * circ;
  return (
    <div className="flex flex-col items-center gap-1">
      <svg width="96" height="96" viewBox="0 0 96 96">
        <circle cx="48" cy="48" r={r} fill="none" stroke="#1e293b" strokeWidth="10" />
        <circle cx="48" cy="48" r={r} fill="none" stroke={color} strokeWidth="10"
          strokeDasharray={`${dash} ${circ}`} strokeLinecap="round" transform="rotate(-90 48 48)" />
        <text x="48" y="53" textAnchor="middle" fontSize="14" fontWeight="700" fill="#f1f5f9">
          {value.toFixed(1)}
        </text>
      </svg>
      <span className="text-xs text-slate-400 text-center leading-tight">{label}</span>
    </div>
  );
}

// ─── distribution bar ────────────────────────────────────────────────────────

function DistBar({ title, counts, colors }: {
  title: string; counts: Record<string, number>; colors: Record<string, string>;
}) {
  const total = Object.values(counts).reduce((a, b) => a + b, 0) || 1;
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
      <p className="text-xs font-semibold text-slate-400 mb-3 uppercase tracking-wide">{title}</p>
      <div className="flex rounded overflow-hidden h-3 mb-3">
        {Object.entries(counts).map(([k, v]) => (
          <div key={k} style={{ width: `${(v / total) * 100}%`, backgroundColor: colors[k] || "#64748b" }}
            title={`${k}: ${v}`} />
        ))}
      </div>
      <div className="flex flex-wrap gap-x-3 gap-y-1">
        {Object.entries(counts).map(([k, v]) => (
          <span key={k} className="flex items-center gap-1 text-xs text-slate-300">
            <span className="inline-block w-2 h-2 rounded-full" style={{ backgroundColor: colors[k] || "#64748b" }} />
            {labelify(k)} <span className="text-slate-500">({v})</span>
          </span>
        ))}
      </div>
    </div>
  );
}

// ─── detail modal ────────────────────────────────────────────────────────────

function DetailModal({ rep, onClose }: { rep: Rep; onClose: () => void }) {
  const [tab, setTab] = useState<"scores" | "signals" | "action">("scores");
  useEffect(() => {
    const h = (e: KeyboardEvent) => e.key === "Escape" && onClose();
    window.addEventListener("keydown", h);
    return () => window.removeEventListener("keydown", h);
  }, [onClose]);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm p-4"
      onClick={onClose}>
      <div className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-lg shadow-2xl"
        onClick={(e) => e.stopPropagation()}>
        <div className="flex items-center justify-between p-5 border-b border-slate-800">
          <div>
            <p className="text-lg font-bold text-slate-100">{rep.rep_id}</p>
            <p className="text-xs text-slate-400">{rep.region} · {labelify(rep.reference_severity)}</p>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-slate-200 text-xl font-bold">✕</button>
        </div>
        <div className="flex border-b border-slate-800">
          {(["scores", "signals", "action"] as const).map((t) => (
            <button key={t} onClick={() => setTab(t)}
              className={`flex-1 py-2 text-xs font-semibold uppercase tracking-wide transition-colors ${
                tab === t ? "text-teal-400 border-b-2 border-teal-400" : "text-slate-500 hover:text-slate-300"}`}>
              {t}
            </button>
          ))}
        </div>
        <div className="p-5 space-y-3">
          {tab === "scores" && (
            <>
              {[
                ["Reference Composite", rep.reference_composite],
                ["Utilization Score", rep.reference_utilization_score],
                ["Diversity Score", rep.evidence_diversity_score],
                ["Timing Score", rep.reference_timing_score],
                ["Depth Score", rep.evidence_depth_score],
              ].map(([label, val]) => (
                <div key={label as string} className="flex items-center gap-3">
                  <span className="text-xs text-slate-400 w-36">{label as string}</span>
                  <div className="flex-1 bg-slate-800 rounded-full h-2">
                    <div className="h-2 rounded-full bg-teal-500 transition-all"
                      style={{ width: `${Math.min((val as number), 100)}%` }} />
                  </div>
                  <span className="text-xs text-slate-200 w-10 text-right">{(val as number).toFixed(1)}</span>
                </div>
              ))}
              <div className="mt-2 pt-2 border-t border-slate-800 flex justify-between text-xs">
                <span className="text-slate-400">Win Rate Impact</span>
                <span className="text-amber-400 font-bold">{fmtUSD(rep.estimated_win_rate_impact_usd)}</span>
              </div>
            </>
          )}
          {tab === "signals" && (
            <div className="space-y-3">
              <div className="bg-slate-800 rounded-lg p-3">
                <p className="text-xs text-slate-400 mb-1">Reference Signal</p>
                <p className="text-sm text-slate-100">{rep.reference_signal}</p>
              </div>
              <div className="grid grid-cols-2 gap-2 text-xs">
                {[
                  ["Risk Level", rep.reference_risk],
                  ["Pattern", rep.reference_pattern],
                  ["Severity", rep.reference_severity],
                  ["Evidence Gap", rep.has_reference_gap ? "Yes" : "No"],
                  ["Needs Coaching", rep.requires_reference_coaching ? "Yes" : "No"],
                ].map(([k, v]) => (
                  <div key={k as string} className="bg-slate-800 rounded-lg p-2">
                    <p className="text-slate-500">{k as string}</p>
                    <p className="text-slate-100 font-medium mt-0.5">{labelify(v as string)}</p>
                  </div>
                ))}
              </div>
            </div>
          )}
          {tab === "action" && (
            <div className="space-y-3">
              <div className="bg-teal-900/30 border border-teal-700 rounded-lg p-4">
                <p className="text-xs text-teal-400 font-semibold uppercase tracking-wide mb-1">Recommended Action</p>
                <p className="text-base font-bold text-slate-100">{labelify(rep.recommended_action)}</p>
              </div>
              <div className="bg-slate-800 rounded-lg p-3 text-xs text-slate-300 leading-relaxed">
                {rep.recommended_action === "no_action" &&
                  "Customer evidence usage is strong. References, case studies, and ROI assets are deployed strategically."}
                {rep.recommended_action === "reference_program_onboarding" &&
                  "Enroll rep in reference program immediately. Map available customer references by industry and use-case and establish deployment protocols."}
                {rep.recommended_action === "evidence_library_training" &&
                  "Train rep on using the evidence library: how to select, customize, and deploy case studies and ROI documents at the right deal stage."}
                {rep.recommended_action === "reference_rotation_coaching" &&
                  "Coach rep to diversify reference usage. Overusing the same reference burns customer relationships. Build a rotation plan across verticals."}
                {rep.recommended_action === "case_study_deployment_plan" &&
                  "Build a systematic case study deployment plan: identify relevant case studies per deal type and establish a workflow to share them consistently."}
                {rep.recommended_action === "late_stage_evidence_sprint" &&
                  "References must enter deals at discovery, not near close. Coach rep to introduce social proof early and track evidence timing per deal."}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

// ─── main page ───────────────────────────────────────────────────────────────

export default function SalesReferenceIntelligenceEnginePage() {
  const [data, setData] = useState<{ reps: Rep[]; summary: Summary } | null>(null);
  const [riskFilter, setRiskFilter] = useState("all");
  const [patternFilter, setPatternFilter] = useState("all");
  const [selected, setSelected] = useState<Rep | null>(null);

  const load = useCallback(() => {
    const params = new URLSearchParams();
    if (riskFilter !== "all") params.set("risk", riskFilter);
    if (patternFilter !== "all") params.set("pattern", patternFilter);
    fetch(`/api/sales-reference-intelligence-engine?${params}`)
      .then((r) => r.json())
      .then(setData);
  }, [riskFilter, patternFilter]);

  useEffect(() => { load(); }, [load]);

  if (!data) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="w-8 h-8 border-2 border-teal-500 border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  const { reps, summary } = data;

  const distributions = [
    {
      title: "Reference Risk Distribution",
      counts: summary.risk_counts,
      colors: { low: "#34d399", moderate: "#fbbf24", high: "#f97316", critical: "#f87171" },
    },
    {
      title: "Pattern Distribution",
      counts: summary.pattern_counts,
      colors: {
        none: "#34d399",
        reference_avoidance: "#f87171",
        reference_fatigue: "#f97316",
        single_reference_overuse: "#fbbf24",
        no_case_study_usage: "#a78bfa",
        late_stage_evidence_gap: "#38bdf8",
      },
    },
    {
      title: "Severity Distribution",
      counts: summary.severity_counts,
      colors: { evidence_led: "#34d399", developing: "#fbbf24", anecdotal: "#f97316", blind: "#f87171" },
    },
    {
      title: "Action Distribution",
      counts: summary.action_counts,
      colors: {
        no_action: "#34d399",
        evidence_library_training: "#fbbf24",
        reference_rotation_coaching: "#f97316",
        reference_program_onboarding: "#f87171",
        case_study_deployment_plan: "#a78bfa",
        late_stage_evidence_sprint: "#38bdf8",
      },
    },
  ] as Array<{ title: string; counts: Record<string, number>; colors: Record<string, string> }>;

  const riskKeys = Object.keys(summary.risk_counts);
  const patternKeys = Object.keys(summary.pattern_counts);

  return (
    <div className="p-6 space-y-6 text-slate-100 max-w-7xl mx-auto">
      <div>
        <h1 className="text-2xl font-bold text-slate-100">Sales Reference Intelligence Engine</h1>
        <p className="text-sm text-slate-400 mt-1">
          Customer evidence deployment — references, case studies, ROI assets, and social proof per rep
        </p>
      </div>

      {/* KPI strip */}
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
        {[
          { label: "Total Reps", value: String(summary.total), sub: "tracked" },
          { label: "Avg Composite", value: fmtPct(summary.avg_reference_composite), sub: "evidence risk score" },
          { label: "Evidence Gap", value: String(summary.reference_gap_count), sub: "reps with gap" },
          { label: "Needs Coaching", value: String(summary.coaching_count), sub: "reps flagged" },
          { label: "Win Rate Impact", value: fmtUSD(summary.total_estimated_win_rate_impact_usd), sub: "pipeline at risk" },
          { label: "Avg Depth", value: fmtPct(summary.avg_evidence_depth_score), sub: "depth score" },
        ].map(({ label, value, sub }) => (
          <div key={label} className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <p className="text-xs text-slate-400 uppercase tracking-wide">{label}</p>
            <p className="text-xl font-bold text-slate-100 mt-1">{value}</p>
            <p className="text-xs text-slate-500 mt-0.5">{sub}</p>
          </div>
        ))}
      </div>

      {/* gauges */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
        <p className="text-xs font-semibold text-slate-400 uppercase tracking-wide mb-5">Avg Sub-Scores</p>
        <div className="flex flex-wrap justify-around gap-6">
          <GaugeRing label="Utilization" value={summary.avg_reference_utilization_score} color="#2dd4bf" />
          <GaugeRing label="Diversity" value={summary.avg_evidence_diversity_score} color="#f97316" />
          <GaugeRing label="Timing" value={summary.avg_reference_timing_score} color="#38bdf8" />
          <GaugeRing label="Depth" value={summary.avg_evidence_depth_score} color="#a78bfa" />
        </div>
      </div>

      {/* distributions */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        {distributions.map((d) => (
          <DistBar key={d.title} title={d.title} counts={d.counts} colors={d.colors} />
        ))}
      </div>

      {/* filters */}
      <div className="flex flex-wrap gap-3">
        <div className="flex flex-wrap gap-1">
          {["all", ...riskKeys].map((r) => (
            <button key={r} onClick={() => setRiskFilter(r)}
              className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${
                riskFilter === r
                  ? "bg-teal-600 border-teal-500 text-white"
                  : "bg-slate-800 border-slate-700 text-slate-300 hover:border-slate-500"}`}>
              {r === "all" ? "All Risk" : labelify(r)}
            </button>
          ))}
        </div>
        <div className="flex flex-wrap gap-1">
          {["all", ...patternKeys].map((p) => (
            <button key={p} onClick={() => setPatternFilter(p)}
              className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${
                patternFilter === p
                  ? "bg-cyan-600 border-cyan-500 text-white"
                  : "bg-slate-800 border-slate-700 text-slate-300 hover:border-slate-500"}`}>
              {p === "all" ? "All Patterns" : labelify(p)}
            </button>
          ))}
        </div>
      </div>

      {/* rep cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {reps.map((rep) => (
          <button key={rep.rep_id} onClick={() => setSelected(rep)}
            className={`text-left bg-slate-900 border rounded-xl p-4 hover:border-slate-600 transition-all hover:shadow-lg ${
              RISK_BORDER[rep.reference_risk] || "border-slate-700"} ${RISK_BG[rep.reference_risk] || ""}`}>
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm font-bold text-slate-100">{rep.rep_id}</span>
              <div className="flex gap-1 flex-wrap justify-end">
                {rep.has_reference_gap && (
                  <span className="text-xs px-1.5 py-0.5 rounded bg-slate-800 text-teal-300 font-bold">📋 GAP</span>
                )}
                {rep.requires_reference_coaching && !rep.has_reference_gap && (
                  <span className="text-xs px-1.5 py-0.5 rounded bg-slate-800 text-yellow-300 font-bold">📋 COACH</span>
                )}
              </div>
            </div>
            <p className="text-xs text-slate-400 mb-3">{rep.region}</p>
            <div className="space-y-1.5">
              <div className="flex justify-between text-xs">
                <span className="text-slate-400">Composite</span>
                <span className={`font-bold ${RISK_COLORS[rep.reference_risk] || "text-slate-200"}`}>
                  {rep.reference_composite.toFixed(1)}
                </span>
              </div>
              <div className="flex justify-between text-xs">
                <span className="text-slate-400">Pattern</span>
                <span className="text-slate-200">{labelify(rep.reference_pattern)}</span>
              </div>
              <div className="flex justify-between text-xs">
                <span className="text-slate-400">Win Rate Impact</span>
                <span className="text-amber-400 font-medium">{fmtUSD(rep.estimated_win_rate_impact_usd)}</span>
              </div>
              <div className="flex justify-between text-xs">
                <span className="text-slate-400">Action</span>
                <span className="text-slate-300 text-right max-w-[60%] truncate">{labelify(rep.recommended_action)}</span>
              </div>
            </div>
            <div className="mt-3 flex gap-1">
              {[
                { label: "Uti", val: rep.reference_utilization_score },
                { label: "Div", val: rep.evidence_diversity_score },
                { label: "Tim", val: rep.reference_timing_score },
                { label: "Dep", val: rep.evidence_depth_score },
              ].map(({ label, val }) => (
                <div key={label} className="flex-1 text-center">
                  <div className="h-1 bg-slate-800 rounded-full overflow-hidden">
                    <div className="h-full bg-teal-500 rounded-full" style={{ width: `${Math.min(val, 100)}%` }} />
                  </div>
                  <p className="text-[10px] text-slate-500 mt-0.5">{label}</p>
                </div>
              ))}
            </div>
          </button>
        ))}
      </div>

      {reps.length === 0 && (
        <div className="text-center py-12 text-slate-500">No reps match the selected filters.</div>
      )}

      {selected && <DetailModal rep={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
