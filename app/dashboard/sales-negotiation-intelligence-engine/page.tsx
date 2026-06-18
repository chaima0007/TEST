"use client";
import { useEffect, useState, useCallback } from "react";

// ─── types ───────────────────────────────────────────────────────────────────

interface Rep {
  rep_id: string;
  region: string;
  negotiation_risk: string;
  negotiation_pattern: string;
  negotiation_severity: string;
  recommended_action: string;
  concession_discipline_score: number;
  negotiation_process_score: number;
  negotiation_urgency_score: number;
  value_articulation_score: number;
  negotiation_composite: number;
  has_negotiation_gap: boolean;
  requires_negotiation_coaching: boolean;
  estimated_margin_erosion_usd: number;
  negotiation_signal: string;
}

interface Summary {
  total: number;
  risk_counts: Record<string, number>;
  pattern_counts: Record<string, number>;
  severity_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_negotiation_composite: number;
  negotiation_gap_count: number;
  coaching_count: number;
  avg_concession_discipline_score: number;
  avg_negotiation_process_score: number;
  avg_negotiation_urgency_score: number;
  avg_value_articulation_score: number;
  total_estimated_margin_erosion_usd: number;
}

// ─── helpers ─────────────────────────────────────────────────────────────────

const RISK_COLORS: Record<string, string> = {
  low: "text-emerald-400", moderate: "text-yellow-400",
  high: "text-orange-400", critical: "text-red-400",
};
const RISK_BORDER: Record<string, string> = {
  low: "border-emerald-700", moderate: "border-yellow-700",
  high: "border-orange-700", critical: "border-red-700",
};
const RISK_BG: Record<string, string> = {
  low: "bg-emerald-900/20", moderate: "bg-yellow-900/20",
  high: "bg-orange-900/20", critical: "bg-red-900/20",
};
const fmtUSD = (v: number) =>
  v >= 1_000_000 ? `$${(v / 1_000_000).toFixed(1)}M`
  : v >= 1_000 ? `$${(v / 1_000).toFixed(0)}K`
  : `$${v.toFixed(0)}`;
const fmtPct = (v: number) => `${v.toFixed(1)}%`;
const labelify = (s: string) =>
  s.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());

// ─── gauge ring ──────────────────────────────────────────────────────────────

function GaugeRing({ label, value, color }: { label: string; value: number; color: string }) {
  const r = 36; const circ = 2 * Math.PI * r;
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
            <p className="text-xs text-slate-400">{rep.region} · {labelify(rep.negotiation_severity)}</p>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-slate-200 text-xl font-bold">✕</button>
        </div>
        <div className="flex border-b border-slate-800">
          {(["scores", "signals", "action"] as const).map((t) => (
            <button key={t} onClick={() => setTab(t)}
              className={`flex-1 py-2 text-xs font-semibold uppercase tracking-wide transition-colors ${
                tab === t ? "text-amber-400 border-b-2 border-amber-400" : "text-slate-500 hover:text-slate-300"}`}>
              {t}
            </button>
          ))}
        </div>
        <div className="p-5 space-y-3">
          {tab === "scores" && (
            <>
              {[
                ["Negotiation Composite", rep.negotiation_composite],
                ["Concession Discipline", rep.concession_discipline_score],
                ["Negotiation Process", rep.negotiation_process_score],
                ["Urgency Score", rep.negotiation_urgency_score],
                ["Value Articulation", rep.value_articulation_score],
              ].map(([label, val]) => (
                <div key={label as string} className="flex items-center gap-3">
                  <span className="text-xs text-slate-400 w-40">{label as string}</span>
                  <div className="flex-1 bg-slate-800 rounded-full h-2">
                    <div className="h-2 rounded-full bg-amber-500 transition-all"
                      style={{ width: `${Math.min((val as number), 100)}%` }} />
                  </div>
                  <span className="text-xs text-slate-200 w-10 text-right">{(val as number).toFixed(1)}</span>
                </div>
              ))}
              <div className="mt-2 pt-2 border-t border-slate-800 flex justify-between text-xs">
                <span className="text-slate-400">Margin Erosion</span>
                <span className="text-red-400 font-bold">{fmtUSD(rep.estimated_margin_erosion_usd)}</span>
              </div>
            </>
          )}
          {tab === "signals" && (
            <div className="space-y-3">
              <div className="bg-slate-800 rounded-lg p-3">
                <p className="text-xs text-slate-400 mb-1">Negotiation Signal</p>
                <p className="text-sm text-slate-100">{rep.negotiation_signal}</p>
              </div>
              <div className="grid grid-cols-2 gap-2 text-xs">
                {[
                  ["Risk Level", rep.negotiation_risk],
                  ["Pattern", rep.negotiation_pattern],
                  ["Severity", rep.negotiation_severity],
                  ["Negotiation Gap", rep.has_negotiation_gap ? "Yes" : "No"],
                  ["Needs Coaching", rep.requires_negotiation_coaching ? "Yes" : "No"],
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
              <div className="bg-amber-900/30 border border-amber-700 rounded-lg p-4">
                <p className="text-xs text-amber-400 font-semibold uppercase tracking-wide mb-1">Recommended Action</p>
                <p className="text-base font-bold text-slate-100">{labelify(rep.recommended_action)}</p>
              </div>
              <div className="bg-slate-800 rounded-lg p-3 text-xs text-slate-300 leading-relaxed">
                {rep.recommended_action === "no_action" &&
                  "Negotiation discipline is strong. Rep holds value, creates urgency, and manages concessions effectively."}
                {rep.recommended_action === "negotiation_skills_coaching" &&
                  "Coach rep on core negotiation fundamentals: anchoring on value, timing concessions strategically, and using multi-variable trade-offs."}
                {rep.recommended_action === "value_anchoring_training" &&
                  "Rep defaults to price conversations too early. Train on value anchoring: lead with ROI, business impact, and customer outcomes before price enters the discussion."}
                {rep.recommended_action === "concession_management_review" &&
                  "Rep is giving too much too fast. Implement concession management framework: make small concessions only in exchange for something of equal or greater value."}
                {rep.recommended_action === "manager_escalation_reduction" &&
                  "Rep escalates to manager before exhausting their own negotiation options. Coach on holding the line independently and reserving manager involvement as a strategic close play."}
                {rep.recommended_action === "urgency_creation_training" &&
                  "Rep lets deals stall without creating legitimate urgency. Train on quarter-end leverage, pricing change announcements, and mutual evaluation timelines."}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

// ─── main page ───────────────────────────────────────────────────────────────

export default function SalesNegotiationIntelligenceEnginePage() {
  const [data, setData] = useState<{ reps: Rep[]; summary: Summary } | null>(null);
  const [riskFilter, setRiskFilter] = useState("all");
  const [patternFilter, setPatternFilter] = useState("all");
  const [selected, setSelected] = useState<Rep | null>(null);

  const load = useCallback(() => {
    const params = new URLSearchParams();
    if (riskFilter !== "all") params.set("risk", riskFilter);
    if (patternFilter !== "all") params.set("pattern", patternFilter);
    fetch(`/api/sales-negotiation-intelligence-engine?${params}`)
      .then((r) => r.json())
      .then(setData);
  }, [riskFilter, patternFilter]);

  useEffect(() => { load(); }, [load]);

  if (!data) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="w-8 h-8 border-2 border-amber-500 border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  const { reps, summary } = data;

  const distributions = [
    {
      title: "Negotiation Risk Distribution",
      counts: summary.risk_counts,
      colors: { low: "#34d399", moderate: "#fbbf24", high: "#f97316", critical: "#f87171" },
    },
    {
      title: "Pattern Distribution",
      counts: summary.pattern_counts,
      colors: {
        none: "#34d399",
        early_capitulation: "#f87171",
        manager_escalation_dependency: "#f97316",
        price_anchoring_failure: "#fbbf24",
        concession_cascade: "#a78bfa",
        urgency_creation_gap: "#38bdf8",
      },
    },
    {
      title: "Severity Distribution",
      counts: summary.severity_counts,
      colors: { disciplined: "#34d399", developing: "#fbbf24", reactive: "#f97316", erosive: "#f87171" },
    },
    {
      title: "Action Distribution",
      counts: summary.action_counts,
      colors: {
        no_action: "#34d399",
        negotiation_skills_coaching: "#fbbf24",
        concession_management_review: "#f97316",
        manager_escalation_reduction: "#f87171",
        value_anchoring_training: "#a78bfa",
        urgency_creation_training: "#38bdf8",
      },
    },
  ] as Array<{ title: string; counts: Record<string, number>; colors: Record<string, string> }>;

  const riskKeys = Object.keys(summary.risk_counts);
  const patternKeys = Object.keys(summary.pattern_counts);

  return (
    <div className="p-6 space-y-6 text-slate-100 max-w-7xl mx-auto">
      <div>
        <h1 className="text-2xl font-bold text-slate-100">Sales Negotiation Intelligence Engine</h1>
        <p className="text-sm text-slate-400 mt-1">
          Per-rep negotiation behavior — concession discipline, value anchoring, urgency creation, and margin erosion
        </p>
      </div>

      {/* KPI strip */}
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
        {[
          { label: "Total Reps", value: String(summary.total), sub: "tracked" },
          { label: "Avg Composite", value: fmtPct(summary.avg_negotiation_composite), sub: "negotiation risk" },
          { label: "Negotiation Gap", value: String(summary.negotiation_gap_count), sub: "reps with gap" },
          { label: "Needs Coaching", value: String(summary.coaching_count), sub: "reps flagged" },
          { label: "Margin Erosion", value: fmtUSD(summary.total_estimated_margin_erosion_usd), sub: "avoidable loss" },
          { label: "Avg Concession", value: fmtPct(summary.avg_concession_discipline_score), sub: "discipline score" },
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
          <GaugeRing label="Concession Discipline" value={summary.avg_concession_discipline_score} color="#f59e0b" />
          <GaugeRing label="Process Quality" value={summary.avg_negotiation_process_score} color="#f97316" />
          <GaugeRing label="Urgency Creation" value={summary.avg_negotiation_urgency_score} color="#38bdf8" />
          <GaugeRing label="Value Articulation" value={summary.avg_value_articulation_score} color="#a78bfa" />
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
                  ? "bg-amber-600 border-amber-500 text-white"
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
                  ? "bg-orange-600 border-orange-500 text-white"
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
              RISK_BORDER[rep.negotiation_risk] || "border-slate-700"} ${RISK_BG[rep.negotiation_risk] || ""}`}>
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm font-bold text-slate-100">{rep.rep_id}</span>
              <div className="flex gap-1 flex-wrap justify-end">
                {rep.has_negotiation_gap && (
                  <span className="text-xs px-1.5 py-0.5 rounded bg-slate-800 text-amber-300 font-bold">🤝 GAP</span>
                )}
                {rep.requires_negotiation_coaching && !rep.has_negotiation_gap && (
                  <span className="text-xs px-1.5 py-0.5 rounded bg-slate-800 text-yellow-300 font-bold">🤝 COACH</span>
                )}
              </div>
            </div>
            <p className="text-xs text-slate-400 mb-3">{rep.region}</p>
            <div className="space-y-1.5">
              <div className="flex justify-between text-xs">
                <span className="text-slate-400">Composite</span>
                <span className={`font-bold ${RISK_COLORS[rep.negotiation_risk] || "text-slate-200"}`}>
                  {rep.negotiation_composite.toFixed(1)}
                </span>
              </div>
              <div className="flex justify-between text-xs">
                <span className="text-slate-400">Pattern</span>
                <span className="text-slate-200">{labelify(rep.negotiation_pattern)}</span>
              </div>
              <div className="flex justify-between text-xs">
                <span className="text-slate-400">Margin Erosion</span>
                <span className="text-red-400 font-medium">{fmtUSD(rep.estimated_margin_erosion_usd)}</span>
              </div>
              <div className="flex justify-between text-xs">
                <span className="text-slate-400">Action</span>
                <span className="text-slate-300 text-right max-w-[60%] truncate">{labelify(rep.recommended_action)}</span>
              </div>
            </div>
            <div className="mt-3 flex gap-1">
              {[
                { label: "Con", val: rep.concession_discipline_score },
                { label: "Pro", val: rep.negotiation_process_score },
                { label: "Urg", val: rep.negotiation_urgency_score },
                { label: "Val", val: rep.value_articulation_score },
              ].map(({ label, val }) => (
                <div key={label} className="flex-1 text-center">
                  <div className="h-1 bg-slate-800 rounded-full overflow-hidden">
                    <div className="h-full bg-amber-500 rounded-full" style={{ width: `${Math.min(val, 100)}%` }} />
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
