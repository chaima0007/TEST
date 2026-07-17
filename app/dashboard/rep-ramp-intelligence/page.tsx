"use client";

import { useEffect, useState } from "react";

// ─── Types ───────────────────────────────────────────────────────────────────

type RampStatus  = "ahead" | "on_track" | "at_risk" | "behind";
type RampPhase   = "learning" | "ramping" | "approaching_quota" | "at_quota";
type RampRisk    = "low" | "moderate" | "high" | "critical";
type RampAction  = "maintain" | "accelerate_coaching" | "territory_adjustment" | "performance_improvement_plan";

interface Rep {
  rep_id: string;
  rep_name: string;
  region: string;
  ramp_status: RampStatus;
  ramp_phase: RampPhase;
  ramp_risk: RampRisk;
  ramp_action: RampAction;
  activity_score: number;
  readiness_score: number;
  pipeline_health_score: number;
  attainment_score: number;
  ramp_composite: number;
  projected_full_ramp_days: number;
  is_on_track: boolean;
  needs_intervention: boolean;
  key_risk_factor: string;
  hire_date_days_ago: number;
  expected_ramp_days: number;
  revenue_attainment_pct: number;
}

interface Summary {
  total: number;
  ramp_status_counts: Record<string, number>;
  ramp_phase_counts: Record<string, number>;
  ramp_risk_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_ramp_composite: number;
  on_track_count: number;
  intervention_count: number;
  avg_activity_score: number;
  avg_readiness_score: number;
  avg_pipeline_health_score: number;
  avg_attainment_score: number;
  avg_projected_full_ramp_days: number;
}

// ─── Helpers ─────────────────────────────────────────────────────────────────

const STATUS_COLOR: Record<RampStatus, string> = {
  ahead:    "text-emerald-400",
  on_track: "text-indigo-400",
  at_risk:  "text-amber-400",
  behind:   "text-red-400",
};

const RISK_COLOR: Record<RampRisk, string> = {
  low:      "bg-emerald-500/20 text-emerald-300",
  moderate: "bg-amber-500/20  text-amber-300",
  high:     "bg-orange-500/20 text-orange-300",
  critical: "bg-red-500/20    text-red-300",
};

const PHASE_COLOR: Record<RampPhase, string> = {
  learning:           "bg-slate-500/20  text-slate-300",
  ramping:            "bg-indigo-500/20 text-indigo-300",
  approaching_quota:  "bg-violet-500/20 text-violet-300",
  at_quota:           "bg-emerald-500/20 text-emerald-300",
};

function fmtStatus(s: RampStatus): string {
  return s.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
}

function fmtPhase(p: RampPhase): string {
  return p.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
}

function fmtAction(a: RampAction): string {
  return a.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
}

function compositeColor(v: number): string {
  if (v >= 75) return "#34d399";
  if (v >= 55) return "#818cf8";
  if (v >= 40) return "#fbbf24";
  return "#f87171";
}

// ─── SVG Ramp Ring ────────────────────────────────────────────────────────────

function RampRing({ value, label }: { value: number; label: string }) {
  const r = 40;
  const circ = 2 * Math.PI * r;
  const fill = (value / 100) * circ;
  const color = compositeColor(value);
  return (
    <div className="flex flex-col items-center gap-1">
      <svg width="100" height="100" viewBox="0 0 100 100">
        <circle cx="50" cy="50" r={r} fill="none" stroke="#1e293b" strokeWidth="10" />
        <circle
          cx="50" cy="50" r={r} fill="none"
          stroke={color} strokeWidth="10"
          strokeDasharray={`${fill} ${circ}`}
          strokeLinecap="round"
          transform="rotate(-90 50 50)"
        />
        <text x="50" y="46" textAnchor="middle" fill={color} fontSize="16" fontWeight="bold">{value}</text>
        <text x="50" y="60" textAnchor="middle" fill="#94a3b8" fontSize="8">/ 100</text>
      </svg>
      <span className="text-xs text-slate-400">{label}</span>
    </div>
  );
}

// ─── Status Distribution Bar ─────────────────────────────────────────────────

function StatusDistBar({ counts, total }: { counts: Record<string, number>; total: number }) {
  const order: RampStatus[] = ["ahead", "on_track", "at_risk", "behind"];
  const colors: Record<string, string> = {
    ahead: "bg-emerald-500", on_track: "bg-indigo-500", at_risk: "bg-amber-500", behind: "bg-red-500",
  };
  return (
    <div className="space-y-2">
      <div className="flex h-3 rounded-full overflow-hidden gap-0.5">
        {order.map((s) => {
          const pct = total > 0 ? ((counts[s] || 0) / total) * 100 : 0;
          return pct > 0 ? (
            <div key={s} className={`${colors[s]} transition-all`} style={{ width: `${pct}%` }} title={`${s}: ${counts[s] || 0}`} />
          ) : null;
        })}
      </div>
      <div className="flex flex-wrap gap-3">
        {order.map((s) => (
          <div key={s} className="flex items-center gap-1.5">
            <div className={`w-2 h-2 rounded-full ${colors[s]}`} />
            <span className="text-xs text-slate-400">{fmtStatus(s)}: {counts[s] || 0}</span>
          </div>
        ))}
      </div>
    </div>
  );
}

// ─── Rep Card ────────────────────────────────────────────────────────────────

function RepCard({ rep, onClick }: { rep: Rep; onClick: () => void }) {
  const progressPct = rep.expected_ramp_days > 0
    ? Math.min(100, Math.round((rep.hire_date_days_ago / rep.expected_ramp_days) * 100))
    : 0;

  return (
    <button
      onClick={onClick}
      className="w-full text-left bg-slate-900 border border-slate-800 rounded-xl p-4 hover:border-indigo-500/50 transition-all"
    >
      <div className="flex items-start justify-between mb-3">
        <div>
          <p className="font-semibold text-slate-100">{rep.rep_name}</p>
          <p className="text-xs text-slate-500">{rep.rep_id} · {rep.region}</p>
        </div>
        <div className="flex flex-col items-end gap-1">
          <span className={`text-xs font-medium ${STATUS_COLOR[rep.ramp_status]}`}>
            {fmtStatus(rep.ramp_status)}
          </span>
          <span className={`text-xs px-2 py-0.5 rounded-full ${RISK_COLOR[rep.ramp_risk]}`}>
            {rep.ramp_risk} risk
          </span>
        </div>
      </div>

      <div className="flex items-center gap-3 mb-3">
        <div className="flex-1">
          <div className="flex justify-between text-xs text-slate-500 mb-1">
            <span>Ramp progress</span>
            <span>{progressPct}% of {rep.expected_ramp_days}d</span>
          </div>
          <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
            <div
              className="h-full bg-indigo-500 rounded-full"
              style={{ width: `${progressPct}%` }}
            />
          </div>
        </div>
        <div className="text-right">
          <p className="text-lg font-bold" style={{ color: compositeColor(rep.ramp_composite) }}>
            {rep.ramp_composite}
          </p>
          <p className="text-xs text-slate-500">composite</p>
        </div>
      </div>

      <div className="flex items-center justify-between">
        <span className={`text-xs px-2 py-0.5 rounded-full ${PHASE_COLOR[rep.ramp_phase]}`}>
          {fmtPhase(rep.ramp_phase)}
        </span>
        <span className="text-xs text-slate-400">
          {rep.revenue_attainment_pct}% attainment
        </span>
        {rep.needs_intervention && (
          <span className="text-xs bg-red-500/20 text-red-300 px-2 py-0.5 rounded-full">Intervention</span>
        )}
        {rep.is_on_track && !rep.needs_intervention && (
          <span className="text-xs bg-emerald-500/20 text-emerald-300 px-2 py-0.5 rounded-full">On Track</span>
        )}
      </div>
    </button>
  );
}

// ─── Rep Modal ────────────────────────────────────────────────────────────────

function RepModal({ rep, onClose }: { rep: Rep; onClose: () => void }) {
  const [tab, setTab] = useState<"scores" | "ramp" | "actions">("scores");

  useEffect(() => {
    const handler = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [onClose]);

  const scores = [
    { label: "Activity",        value: rep.activity_score },
    { label: "Readiness",       value: rep.readiness_score },
    { label: "Pipeline Health", value: rep.pipeline_health_score },
    { label: "Attainment",      value: rep.attainment_score },
  ];

  return (
    <div
      className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-4"
      onClick={onClose}
    >
      <div
        className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-lg max-h-[90vh] overflow-y-auto"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="p-5 border-b border-slate-800">
          <div className="flex items-start justify-between">
            <div>
              <h2 className="text-lg font-bold text-slate-100">{rep.rep_name}</h2>
              <p className="text-sm text-slate-400">{rep.rep_id} · {rep.region}</p>
              <div className="flex gap-2 mt-2">
                <span className={`text-xs px-2 py-0.5 rounded-full ${PHASE_COLOR[rep.ramp_phase]}`}>
                  {fmtPhase(rep.ramp_phase)}
                </span>
                <span className={`text-xs px-2 py-0.5 rounded-full ${RISK_COLOR[rep.ramp_risk]}`}>
                  {rep.ramp_risk} risk
                </span>
              </div>
            </div>
            <button onClick={onClose} className="text-slate-500 hover:text-slate-300 text-xl leading-none">×</button>
          </div>
        </div>

        {/* Tabs */}
        <div className="flex border-b border-slate-800">
          {(["scores", "ramp", "actions"] as const).map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`flex-1 py-2.5 text-sm capitalize transition-colors ${
                tab === t ? "border-b-2 border-indigo-500 text-indigo-400" : "text-slate-500 hover:text-slate-300"
              }`}
            >
              {t}
            </button>
          ))}
        </div>

        <div className="p-5">
          {tab === "scores" && (
            <div className="space-y-4">
              <div className="grid grid-cols-2 gap-3">
                {scores.map((s) => (
                  <div key={s.label} className="bg-slate-800/50 rounded-lg p-3">
                    <p className="text-xs text-slate-400 mb-1">{s.label}</p>
                    <p className="text-xl font-bold" style={{ color: compositeColor(s.value) }}>{s.value}</p>
                    <div className="mt-1 h-1 bg-slate-700 rounded-full overflow-hidden">
                      <div className="h-full rounded-full" style={{ width: `${s.value}%`, backgroundColor: compositeColor(s.value) }} />
                    </div>
                  </div>
                ))}
              </div>
              <div className="bg-slate-800/50 rounded-lg p-3 flex justify-between items-center">
                <span className="text-sm text-slate-300">Ramp Composite</span>
                <span className="text-2xl font-bold" style={{ color: compositeColor(rep.ramp_composite) }}>
                  {rep.ramp_composite}
                </span>
              </div>
              <div className="bg-slate-800/50 rounded-lg p-3">
                <p className="text-xs text-slate-500 mb-1">Key Risk Factor</p>
                <p className="text-sm text-amber-300">{rep.key_risk_factor}</p>
              </div>
            </div>
          )}

          {tab === "ramp" && (
            <div className="space-y-3">
              {[
                { label: "Days Since Hire", value: `${rep.hire_date_days_ago}d` },
                { label: "Expected Ramp Period", value: `${rep.expected_ramp_days}d` },
                { label: "Projected Full Ramp", value: `${rep.projected_full_ramp_days}d` },
                { label: "Revenue Attainment", value: `${rep.revenue_attainment_pct}%` },
                { label: "Ramp Status", value: fmtStatus(rep.ramp_status) },
                { label: "Is On Track", value: rep.is_on_track ? "Yes" : "No" },
                { label: "Needs Intervention", value: rep.needs_intervention ? "Yes" : "No" },
              ].map(({ label, value }) => (
                <div key={label} className="flex justify-between items-center py-2 border-b border-slate-800">
                  <span className="text-sm text-slate-400">{label}</span>
                  <span className="text-sm font-medium text-slate-200">{value}</span>
                </div>
              ))}
            </div>
          )}

          {tab === "actions" && (
            <div className="space-y-4">
              <div className="bg-indigo-500/10 border border-indigo-500/30 rounded-lg p-4">
                <p className="text-xs text-indigo-400 mb-1">Recommended Action</p>
                <p className="font-semibold text-indigo-300">{fmtAction(rep.ramp_action)}</p>
              </div>
              <div className="space-y-2 text-sm text-slate-300">
                {rep.ramp_action === "maintain" && (
                  <p>Rep is performing well. Continue current coaching cadence and monitor pipeline growth.</p>
                )}
                {rep.ramp_action === "accelerate_coaching" && (
                  <p>Increase manager touchpoints to at least 3 per week. Focus on deal qualification and activity metrics.</p>
                )}
                {rep.ramp_action === "territory_adjustment" && (
                  <p>Evaluate territory quality and prospect density. Consider reassigning high-value accounts to boost pipeline velocity.</p>
                )}
                {rep.ramp_action === "performance_improvement_plan" && (
                  <p>Initiate a formal PIP with clear 30/60/90 day milestones. Address root causes: {rep.key_risk_factor}.</p>
                )}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

// ─── Page ─────────────────────────────────────────────────────────────────────

export default function RepRampIntelligencePage() {
  const [data, setData] = useState<{ reps: Rep[]; summary: Summary } | null>(null);
  const [status, setStatus] = useState("");
  const [phase, setPhase]   = useState("");
  const [region, setRegion] = useState("");
  const [selected, setSelected] = useState<Rep | null>(null);

  useEffect(() => {
    const params = new URLSearchParams();
    if (status) params.set("status", status);
    if (phase)  params.set("phase", phase);
    if (region) params.set("region", region);
    fetch(`/api/rep-ramp-intelligence?${params}`)
      .then((r) => r.json())
      .then(setData);
  }, [status, phase, region]);

  if (!data) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-slate-400">Loading…</div>
    </div>
  );

  const { reps, summary } = data;

  const kpis = [
    { label: "Total Reps",       value: summary.total },
    { label: "On Track",         value: summary.on_track_count,     sub: `${Math.round((summary.on_track_count / summary.total) * 100)}%` },
    { label: "Interventions",    value: summary.intervention_count, sub: "need action" },
    { label: "Avg Composite",    value: summary.avg_ramp_composite },
    { label: "Avg Proj. Ramp",   value: `${summary.avg_projected_full_ramp_days}d` },
    { label: "Avg Attainment",   value: `${summary.avg_attainment_score}` },
  ];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
      <div className="max-w-7xl mx-auto space-y-6">

        {/* Header */}
        <div>
          <h1 className="text-2xl font-bold text-slate-100">Rep Ramp Intelligence</h1>
          <p className="text-slate-400 text-sm mt-1">New rep onboarding performance and full-quota timeline prediction</p>
        </div>

        {/* KPI Strip */}
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
          {kpis.map((k) => (
            <div key={k.label} className="bg-slate-900 border border-slate-800 rounded-xl p-4">
              <p className="text-xs text-slate-500 mb-1">{k.label}</p>
              <p className="text-2xl font-bold text-slate-100">{k.value}</p>
              {k.sub && <p className="text-xs text-slate-500 mt-0.5">{k.sub}</p>}
            </div>
          ))}
        </div>

        {/* Summary Panel */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
          {/* Status Distribution */}
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
            <h2 className="text-sm font-semibold text-slate-300 mb-4">Ramp Status Distribution</h2>
            <StatusDistBar counts={summary.ramp_status_counts} total={summary.total} />
          </div>

          {/* Score Rings */}
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
            <h2 className="text-sm font-semibold text-slate-300 mb-4">Average Scores</h2>
            <div className="flex justify-around">
              <RampRing value={summary.avg_activity_score}          label="Activity" />
              <RampRing value={summary.avg_readiness_score}         label="Readiness" />
              <RampRing value={summary.avg_pipeline_health_score}   label="Pipeline" />
              <RampRing value={summary.avg_attainment_score}        label="Attainment" />
            </div>
          </div>
        </div>

        {/* Filters */}
        <div className="flex flex-wrap gap-3">
          <select
            value={status}
            onChange={(e) => setStatus(e.target.value)}
            className="bg-slate-900 border border-slate-700 text-slate-300 rounded-lg px-3 py-2 text-sm"
          >
            <option value="">All Statuses</option>
            {["ahead", "on_track", "at_risk", "behind"].map((s) => (
              <option key={s} value={s}>{fmtStatus(s as RampStatus)}</option>
            ))}
          </select>
          <select
            value={phase}
            onChange={(e) => setPhase(e.target.value)}
            className="bg-slate-900 border border-slate-700 text-slate-300 rounded-lg px-3 py-2 text-sm"
          >
            <option value="">All Phases</option>
            {["learning", "ramping", "approaching_quota", "at_quota"].map((p) => (
              <option key={p} value={p}>{fmtPhase(p as RampPhase)}</option>
            ))}
          </select>
          <select
            value={region}
            onChange={(e) => setRegion(e.target.value)}
            className="bg-slate-900 border border-slate-700 text-slate-300 rounded-lg px-3 py-2 text-sm"
          >
            <option value="">All Regions</option>
            {["NAMER", "EMEA", "APAC", "LATAM"].map((r) => (
              <option key={r} value={r}>{r}</option>
            ))}
          </select>
        </div>

        {/* Rep Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
          {reps.map((rep) => (
            <RepCard key={rep.rep_id} rep={rep} onClick={() => setSelected(rep)} />
          ))}
        </div>
      </div>

      {selected && <RepModal rep={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
