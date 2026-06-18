"use client";
import { useEffect, useState, useCallback } from "react";

// ─── types ───────────────────────────────────────────────────────────────────

interface Rep {
  rep_id: string;
  region: string;
  poc_risk: string;
  poc_pattern: string;
  poc_severity: string;
  recommended_action: string;
  poc_structure_score: number;
  poc_execution_score: number;
  poc_stakeholder_score: number;
  poc_conversion_score: number;
  poc_composite: number;
  has_poc_gap: boolean;
  requires_poc_coaching: boolean;
  estimated_pipeline_loss_usd: number;
  poc_signal: string;
}

interface Summary {
  total: number;
  risk_counts: Record<string, number>;
  pattern_counts: Record<string, number>;
  severity_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_poc_composite: number;
  poc_gap_count: number;
  coaching_count: number;
  avg_poc_structure_score: number;
  avg_poc_execution_score: number;
  avg_poc_stakeholder_score: number;
  avg_poc_conversion_score: number;
  total_estimated_pipeline_loss_usd: number;
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

function GaugeRing({
  label,
  value,
  max = 100,
  color,
}: {
  label: string;
  value: number;
  max?: number;
  color: string;
}) {
  const r = 36;
  const circ = 2 * Math.PI * r;
  const pct = Math.min(value / max, 1);
  const dash = pct * circ;
  return (
    <div className="flex flex-col items-center gap-1">
      <svg width="96" height="96" viewBox="0 0 96 96">
        <circle cx="48" cy="48" r={r} fill="none" stroke="#1e293b" strokeWidth="10" />
        <circle
          cx="48" cy="48" r={r}
          fill="none"
          stroke={color}
          strokeWidth="10"
          strokeDasharray={`${dash} ${circ}`}
          strokeLinecap="round"
          transform="rotate(-90 48 48)"
        />
        <text x="48" y="53" textAnchor="middle" fontSize="14" fontWeight="700" fill="#f1f5f9">
          {value.toFixed(1)}
        </text>
      </svg>
      <span className="text-xs text-slate-400 text-center leading-tight">{label}</span>
    </div>
  );
}

// ─── distribution bar ─────────────────────────────────────────────────────────

function DistBar({
  title,
  counts,
  colors,
}: {
  title: string;
  counts: Record<string, number>;
  colors: Record<string, string>;
}) {
  const total = Object.values(counts).reduce((a, b) => a + b, 0) || 1;
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
      <p className="text-xs font-semibold text-slate-400 mb-3 uppercase tracking-wide">{title}</p>
      <div className="flex rounded overflow-hidden h-3 mb-3">
        {Object.entries(counts).map(([k, v]) => (
          <div
            key={k}
            style={{ width: `${(v / total) * 100}%`, backgroundColor: colors[k] || "#64748b" }}
            title={`${k}: ${v}`}
          />
        ))}
      </div>
      <div className="flex flex-wrap gap-x-3 gap-y-1">
        {Object.entries(counts).map(([k, v]) => (
          <span key={k} className="flex items-center gap-1 text-xs text-slate-300">
            <span
              className="inline-block w-2 h-2 rounded-full"
              style={{ backgroundColor: colors[k] || "#64748b" }}
            />
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
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm p-4"
      onClick={onClose}
    >
      <div
        className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-lg shadow-2xl"
        onClick={(e) => e.stopPropagation()}
      >
        {/* header */}
        <div className="flex items-center justify-between p-5 border-b border-slate-800">
          <div>
            <p className="text-lg font-bold text-slate-100">{rep.rep_id}</p>
            <p className="text-xs text-slate-400">{rep.region} · {labelify(rep.poc_severity)}</p>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-slate-200 text-xl font-bold">✕</button>
        </div>

        {/* tabs */}
        <div className="flex border-b border-slate-800">
          {(["scores", "signals", "action"] as const).map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`flex-1 py-2 text-xs font-semibold uppercase tracking-wide transition-colors ${
                tab === t ? "text-violet-400 border-b-2 border-violet-400" : "text-slate-500 hover:text-slate-300"
              }`}
            >
              {t}
            </button>
          ))}
        </div>

        {/* body */}
        <div className="p-5 space-y-3">
          {tab === "scores" && (
            <>
              {[
                ["POC Composite", rep.poc_composite],
                ["Structure Score", rep.poc_structure_score],
                ["Execution Score", rep.poc_execution_score],
                ["Stakeholder Score", rep.poc_stakeholder_score],
                ["Conversion Score", rep.poc_conversion_score],
              ].map(([label, val]) => (
                <div key={label as string} className="flex items-center gap-3">
                  <span className="text-xs text-slate-400 w-36">{label as string}</span>
                  <div className="flex-1 bg-slate-800 rounded-full h-2">
                    <div
                      className="h-2 rounded-full bg-violet-500 transition-all"
                      style={{ width: `${Math.min((val as number), 100)}%` }}
                    />
                  </div>
                  <span className="text-xs text-slate-200 w-10 text-right">{(val as number).toFixed(1)}</span>
                </div>
              ))}
              <div className="mt-2 pt-2 border-t border-slate-800 flex justify-between text-xs">
                <span className="text-slate-400">Pipeline Loss</span>
                <span className="text-red-400 font-bold">{fmtUSD(rep.estimated_pipeline_loss_usd)}</span>
              </div>
            </>
          )}

          {tab === "signals" && (
            <div className="space-y-3">
              <div className="bg-slate-800 rounded-lg p-3">
                <p className="text-xs text-slate-400 mb-1">POC Signal</p>
                <p className="text-sm text-slate-100">{rep.poc_signal}</p>
              </div>
              <div className="grid grid-cols-2 gap-2 text-xs">
                {[
                  ["Risk Level", rep.poc_risk],
                  ["Pattern", rep.poc_pattern],
                  ["Severity", rep.poc_severity],
                  ["POC Gap", rep.has_poc_gap ? "Yes" : "No"],
                  ["Needs Coaching", rep.requires_poc_coaching ? "Yes" : "No"],
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
              <div className="bg-violet-900/30 border border-violet-700 rounded-lg p-4">
                <p className="text-xs text-violet-400 font-semibold uppercase tracking-wide mb-1">Recommended Action</p>
                <p className="text-base font-bold text-slate-100">{labelify(rep.recommended_action)}</p>
              </div>
              <div className="bg-slate-800 rounded-lg p-3 text-xs text-slate-300 leading-relaxed">
                {rep.recommended_action === "no_action" &&
                  "POC process is well-structured and converting. Maintain current discipline."}
                {rep.recommended_action === "poc_structure_coaching" &&
                  "Coach rep on POC setup fundamentals: define success criteria upfront, create mutual success plans, and establish timeline commitments before POC start."}
                {rep.recommended_action === "success_criteria_alignment" &&
                  "Align rep on establishing clear, measurable success criteria with customer stakeholders before any POC begins."}
                {rep.recommended_action === "scope_control_training" &&
                  "Train rep on scope management: document POC boundaries clearly, get written agreement, and escalate scope change requests through proper channels."}
                {rep.recommended_action === "technical_escalation_support" &&
                  "Provide SE and technical resources proactively. Review technical validation failures to identify gaps and prevent future losses."}
                {rep.recommended_action === "champion_engagement_during_poc" &&
                  "Coach rep to actively engage the internal champion throughout the POC — weekly check-ins, milestone reviews, and executive sponsor briefings."}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

// ─── main page ───────────────────────────────────────────────────────────────

export default function SalesPOCIntelligenceEnginePage() {
  const [data, setData] = useState<{ reps: Rep[]; summary: Summary } | null>(null);
  const [riskFilter, setRiskFilter] = useState("all");
  const [patternFilter, setPatternFilter] = useState("all");
  const [selected, setSelected] = useState<Rep | null>(null);

  const load = useCallback(() => {
    const params = new URLSearchParams();
    if (riskFilter !== "all") params.set("risk", riskFilter);
    if (patternFilter !== "all") params.set("pattern", patternFilter);
    fetch(`/api/sales-poc-intelligence-engine?${params}`)
      .then((r) => r.json())
      .then(setData);
  }, [riskFilter, patternFilter]);

  useEffect(() => { load(); }, [load]);

  if (!data) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="w-8 h-8 border-2 border-violet-500 border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  const { reps, summary } = data;

  const distributions = [
    {
      title: "POC Risk Distribution",
      counts: summary.risk_counts,
      colors: { low: "#34d399", moderate: "#fbbf24", high: "#f97316", critical: "#f87171" },
    },
    {
      title: "Pattern Distribution",
      counts: summary.pattern_counts,
      colors: {
        none: "#34d399",
        poc_stall: "#fbbf24",
        success_criteria_gap: "#f97316",
        scope_creep: "#f87171",
        technical_validation_failure: "#a78bfa",
        no_champion_during_poc: "#38bdf8",
      },
    },
    {
      title: "Severity Distribution",
      counts: summary.severity_counts,
      colors: { structured: "#34d399", developing: "#fbbf24", uncontrolled: "#f97316", failing: "#f87171" },
    },
    {
      title: "Action Distribution",
      counts: summary.action_counts,
      colors: {
        no_action: "#34d399",
        success_criteria_alignment: "#fbbf24",
        poc_structure_coaching: "#f97316",
        scope_control_training: "#a78bfa",
        technical_escalation_support: "#f87171",
        champion_engagement_during_poc: "#38bdf8",
      },
    },
  ] as Array<{ title: string; counts: Record<string, number>; colors: Record<string, string> }>;

  const riskKeys = Object.keys(summary.risk_counts);
  const patternKeys = Object.keys(summary.pattern_counts);

  return (
    <div className="p-6 space-y-6 text-slate-100 max-w-7xl mx-auto">
      {/* title */}
      <div>
        <h1 className="text-2xl font-bold text-slate-100">Sales POC Intelligence Engine</h1>
        <p className="text-sm text-slate-400 mt-1">
          Proof-of-concept execution quality — structure, conversion, and champion engagement per rep
        </p>
      </div>

      {/* KPI strip */}
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
        {[
          { label: "Total Reps", value: String(summary.total), sub: "tracked" },
          { label: "Avg Composite", value: fmtPct(summary.avg_poc_composite), sub: "poc risk score" },
          { label: "POC Gap", value: String(summary.poc_gap_count), sub: "reps with gap" },
          { label: "Needs Coaching", value: String(summary.coaching_count), sub: "reps flagged" },
          { label: "Pipeline Loss", value: fmtUSD(summary.total_estimated_pipeline_loss_usd), sub: "estimated risk" },
          { label: "Avg Conversion", value: fmtPct(summary.avg_poc_conversion_score), sub: "conversion score" },
        ].map(({ label, value, sub }) => (
          <div key={label} className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <p className="text-xs text-slate-400 uppercase tracking-wide">{label}</p>
            <p className="text-xl font-bold text-slate-100 mt-1">{value}</p>
            <p className="text-xs text-slate-500 mt-0.5">{sub}</p>
          </div>
        ))}
      </div>

      {/* gauge rings */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
        <p className="text-xs font-semibold text-slate-400 uppercase tracking-wide mb-5">Avg Sub-Scores</p>
        <div className="flex flex-wrap justify-around gap-6">
          <GaugeRing label="POC Structure" value={summary.avg_poc_structure_score} color="#a78bfa" />
          <GaugeRing label="POC Execution" value={summary.avg_poc_execution_score} color="#f97316" />
          <GaugeRing label="Stakeholder" value={summary.avg_poc_stakeholder_score} color="#38bdf8" />
          <GaugeRing label="Conversion" value={summary.avg_poc_conversion_score} color="#f87171" />
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
            <button
              key={r}
              onClick={() => setRiskFilter(r)}
              className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${
                riskFilter === r
                  ? "bg-violet-600 border-violet-500 text-white"
                  : "bg-slate-800 border-slate-700 text-slate-300 hover:border-slate-500"
              }`}
            >
              {r === "all" ? "All Risk" : labelify(r)}
            </button>
          ))}
        </div>
        <div className="flex flex-wrap gap-1">
          {["all", ...patternKeys].map((p) => (
            <button
              key={p}
              onClick={() => setPatternFilter(p)}
              className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${
                patternFilter === p
                  ? "bg-indigo-600 border-indigo-500 text-white"
                  : "bg-slate-800 border-slate-700 text-slate-300 hover:border-slate-500"
              }`}
            >
              {p === "all" ? "All Patterns" : labelify(p)}
            </button>
          ))}
        </div>
      </div>

      {/* rep cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {reps.map((rep) => (
          <button
            key={rep.rep_id}
            onClick={() => setSelected(rep)}
            className={`text-left bg-slate-900 border rounded-xl p-4 hover:border-slate-600 transition-all hover:shadow-lg ${
              RISK_BORDER[rep.poc_risk] || "border-slate-700"
            } ${RISK_BG[rep.poc_risk] || ""}`}
          >
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm font-bold text-slate-100">{rep.rep_id}</span>
              <div className="flex gap-1 flex-wrap justify-end">
                {rep.has_poc_gap && (
                  <span className="text-xs px-1.5 py-0.5 rounded bg-slate-800 text-violet-300 font-bold">🔬 GAP</span>
                )}
                {rep.requires_poc_coaching && !rep.has_poc_gap && (
                  <span className="text-xs px-1.5 py-0.5 rounded bg-slate-800 text-yellow-300 font-bold">🔬 COACH</span>
                )}
              </div>
            </div>
            <p className="text-xs text-slate-400 mb-3">{rep.region}</p>
            <div className="space-y-1.5">
              <div className="flex justify-between text-xs">
                <span className="text-slate-400">Composite</span>
                <span className={`font-bold ${RISK_COLORS[rep.poc_risk] || "text-slate-200"}`}>
                  {rep.poc_composite.toFixed(1)}
                </span>
              </div>
              <div className="flex justify-between text-xs">
                <span className="text-slate-400">Pattern</span>
                <span className="text-slate-200">{labelify(rep.poc_pattern)}</span>
              </div>
              <div className="flex justify-between text-xs">
                <span className="text-slate-400">Pipeline Loss</span>
                <span className="text-red-400 font-medium">{fmtUSD(rep.estimated_pipeline_loss_usd)}</span>
              </div>
              <div className="flex justify-between text-xs">
                <span className="text-slate-400">Action</span>
                <span className="text-slate-300 text-right max-w-[60%] truncate">{labelify(rep.recommended_action)}</span>
              </div>
            </div>
            <div className="mt-3 flex gap-1">
              {[
                { label: "Str", val: rep.poc_structure_score },
                { label: "Exc", val: rep.poc_execution_score },
                { label: "Stk", val: rep.poc_stakeholder_score },
                { label: "Cvt", val: rep.poc_conversion_score },
              ].map(({ label, val }) => (
                <div key={label} className="flex-1 text-center">
                  <div className="h-1 bg-slate-800 rounded-full overflow-hidden">
                    <div
                      className="h-full bg-violet-500 rounded-full"
                      style={{ width: `${Math.min(val, 100)}%` }}
                    />
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
