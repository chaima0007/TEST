"use client";

import { useEffect, useState } from "react";

interface RepRamp {
  rep_id: string;
  region: string;
  ramp_risk: string;
  ramp_blocker: string;
  ramp_severity: string;
  recommended_action: string;
  pipeline_gap_score: number;
  conversion_velocity_score: number;
  knowledge_readiness_score: number;
  activity_quality_score: number;
  ramp_composite: number;
  is_under_ramping: boolean;
  requires_intervention: boolean;
  estimated_quota_attainment_pct: number;
  ramp_signal: string;
}

interface Summary {
  total: number;
  risk_counts: Record<string, number>;
  blocker_counts: Record<string, number>;
  severity_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_ramp_composite: number;
  under_ramping_count: number;
  intervention_count: number;
  avg_pipeline_gap_score: number;
  avg_conversion_velocity_score: number;
  avg_knowledge_readiness_score: number;
  avg_activity_quality_score: number;
  avg_estimated_quota_attainment_pct: number;
}

const RISK_COLORS: Record<string, string> = {
  low:      "text-emerald-400",
  moderate: "text-yellow-400",
  high:     "text-orange-400",
  critical: "text-red-400",
};

const RISK_BG: Record<string, string> = {
  low:      "bg-emerald-400/20 border-emerald-400/40",
  moderate: "bg-yellow-400/20 border-yellow-400/40",
  high:     "bg-orange-400/20 border-orange-400/40",
  critical: "bg-red-400/20 border-red-400/40",
};

const SEV_COLORS: Record<string, string> = {
  on_track: "text-emerald-400",
  behind:   "text-yellow-400",
  at_risk:  "text-orange-400",
  failing:  "text-red-400",
};

const ACTION_COLORS: Record<string, string> = {
  no_action:            "text-slate-400",
  targeted_coaching:    "text-sky-400",
  ramp_plan_adjustment: "text-yellow-400",
  pip_initiation:       "text-orange-400",
  separation_review:    "text-red-400",
};

function fmt(s: string) {
  return s.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
}

function RingGauge({ value, max = 100, color }: { value: number; max?: number; color: string }) {
  const r = 28, cx = 36, cy = 36;
  const circ = 2 * Math.PI * r;
  const pct = Math.min(value / max, 1);
  const dash = pct * circ;
  return (
    <svg width={72} height={72} className="rotate-[-90deg]">
      <circle cx={cx} cy={cy} r={r} fill="none" stroke="#1e293b" strokeWidth={8} />
      <circle cx={cx} cy={cy} r={r} fill="none" stroke={color} strokeWidth={8}
        strokeDasharray={`${dash} ${circ}`} strokeLinecap="round" />
    </svg>
  );
}

function ScoreBar({ label, value, max = 100 }: { label: string; value: number; max?: number }) {
  const pct = Math.min((value / max) * 100, 100);
  const color = value >= 60 ? "bg-red-500" : value >= 40 ? "bg-orange-500" : value >= 20 ? "bg-yellow-500" : "bg-emerald-500";
  return (
    <div className="space-y-1">
      <div className="flex justify-between text-xs text-slate-400">
        <span>{label}</span><span className="text-slate-300">{value.toFixed(1)}</span>
      </div>
      <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
        <div className={`h-full rounded-full transition-all ${color}`} style={{ width: `${pct}%` }} />
      </div>
    </div>
  );
}

function DetailModal({ rep, onClose }: { rep: RepRamp; onClose: () => void }) {
  const [tab, setTab] = useState(0);
  useEffect(() => {
    const h = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", h);
    return () => window.removeEventListener("keydown", h);
  }, [onClose]);

  const riskColor = RISK_COLORS[rep.ramp_risk] || "text-slate-400";
  const composite = rep.ramp_composite;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm"
      onClick={onClose}>
      <div className="relative w-full max-w-2xl mx-4 bg-slate-900 border border-slate-700 rounded-2xl shadow-2xl"
        onClick={(e) => e.stopPropagation()}>
        <div className="flex items-start justify-between p-6 border-b border-slate-800">
          <div>
            <h2 className="text-lg font-bold text-slate-100">{rep.rep_id}</h2>
            <p className="text-sm text-slate-400 mt-0.5">{rep.region} · {fmt(rep.ramp_blocker)}</p>
          </div>
          <div className="text-right">
            <span className={`text-sm font-semibold ${riskColor}`}>{fmt(rep.ramp_risk)} Risk</span>
            <p className={`text-xs mt-0.5 ${SEV_COLORS[rep.ramp_severity] || "text-slate-400"}`}>{fmt(rep.ramp_severity)}</p>
          </div>
        </div>

        <div className="flex border-b border-slate-800">
          {["Overview", "Scores", "Action"].map((t, i) => (
            <button key={t} onClick={() => setTab(i)}
              className={`flex-1 py-2.5 text-sm font-medium transition-colors ${tab === i ? "text-indigo-400 border-b-2 border-indigo-400" : "text-slate-500 hover:text-slate-300"}`}>
              {t}
            </button>
          ))}
        </div>

        <div className="p-6 space-y-4 max-h-[60vh] overflow-y-auto">
          {tab === 0 && (
            <>
              <div className="flex items-center gap-6">
                <div className="relative flex items-center justify-center">
                  <RingGauge value={composite} color={composite >= 60 ? "#f87171" : composite >= 40 ? "#fb923c" : composite >= 20 ? "#facc15" : "#34d399"} />
                  <span className="absolute text-sm font-bold text-slate-200">{composite.toFixed(1)}</span>
                </div>
                <div className="flex-1 space-y-2">
                  <div className="flex justify-between text-sm">
                    <span className="text-slate-400">Quota Attainment Est.</span>
                    <span className="text-slate-200 font-medium">{rep.estimated_quota_attainment_pct.toFixed(1)}%</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-slate-400">Under Ramping</span>
                    <span className={rep.is_under_ramping ? "text-red-400" : "text-emerald-400"}>{rep.is_under_ramping ? "Yes" : "No"}</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-slate-400">Needs Intervention</span>
                    <span className={rep.requires_intervention ? "text-orange-400" : "text-emerald-400"}>{rep.requires_intervention ? "Yes" : "No"}</span>
                  </div>
                </div>
              </div>
              <div className={`rounded-lg border p-3 ${RISK_BG[rep.ramp_risk] || "bg-slate-800/50 border-slate-700"}`}>
                <p className="text-xs text-slate-300">{rep.ramp_signal}</p>
              </div>
            </>
          )}
          {tab === 1 && (
            <div className="space-y-3">
              <ScoreBar label="Pipeline Gap" value={rep.pipeline_gap_score} />
              <ScoreBar label="Conversion Velocity" value={rep.conversion_velocity_score} />
              <ScoreBar label="Knowledge Readiness" value={rep.knowledge_readiness_score} />
              <ScoreBar label="Activity Quality" value={rep.activity_quality_score} />
              <div className="pt-2 border-t border-slate-800">
                <ScoreBar label="Ramp Composite" value={rep.ramp_composite} />
              </div>
            </div>
          )}
          {tab === 2 && (
            <div className="space-y-4">
              <div>
                <p className="text-xs text-slate-500 mb-1">Recommended Action</p>
                <span className={`text-sm font-semibold ${ACTION_COLORS[rep.recommended_action] || "text-slate-400"}`}>{fmt(rep.recommended_action)}</span>
              </div>
              <div>
                <p className="text-xs text-slate-500 mb-1">Primary Blocker</p>
                <span className="text-sm text-slate-200">{fmt(rep.ramp_blocker)}</span>
              </div>
              <div>
                <p className="text-xs text-slate-500 mb-1">Severity</p>
                <span className={`text-sm font-medium ${SEV_COLORS[rep.ramp_severity] || "text-slate-400"}`}>{fmt(rep.ramp_severity)}</span>
              </div>
            </div>
          )}
        </div>

        <div className="flex justify-end p-4 border-t border-slate-800">
          <button onClick={onClose}
            className="px-4 py-2 text-sm text-slate-400 hover:text-slate-200 transition-colors">Close</button>
        </div>
      </div>
    </div>
  );
}

export default function AERampVelocityPage() {
  const [data, setData] = useState<{ reps: RepRamp[]; summary: Summary } | null>(null);
  const [riskFilter, setRiskFilter] = useState("all");
  const [selected, setSelected] = useState<RepRamp | null>(null);

  useEffect(() => {
    async function load() {
        const params = new URLSearchParams();
        if (riskFilter !== "all") params.set("risk", riskFilter);
        const res = await fetch(`/api/account-executive-ramp-velocity-engine?${params}`);
        if (res.ok) setData(await res.json());
  }
    load();
  }, [riskFilter]);

  const summary = data?.summary;
  const reps = data?.reps ?? [];

  const kpis = summary ? [
    { label: "Total AEs",          value: summary.total,                              sub: "evaluated" },
    { label: "Under Ramping",       value: summary.under_ramping_count,                sub: "behind pace" },
    { label: "Need Intervention",   value: summary.intervention_count,                 sub: "escalate now" },
    { label: "Avg Composite",       value: summary.avg_ramp_composite.toFixed(1),      sub: "ramp risk score" },
    { label: "Avg Quota Est.",      value: `${summary.avg_estimated_quota_attainment_pct.toFixed(1)}%`, sub: "attainment" },
  ] : [];

  const RISKS = ["all", "low", "moderate", "high", "critical"];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-slate-100">AE Ramp Velocity Engine</h1>
        <p className="text-slate-400 mt-1 text-sm">Detect new account executives falling behind ramp targets before quota impact.</p>
      </div>

      {/* KPI strip */}
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-4">
        {kpis.map((k) => (
          <div key={k.label} className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <p className="text-xs text-slate-500">{k.label}</p>
            <p className="text-2xl font-bold text-slate-100 mt-1">{k.value}</p>
            <p className="text-xs text-slate-500 mt-0.5">{k.sub}</p>
          </div>
        ))}
      </div>

      {/* Distribution bars */}
      {summary && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {[
            { title: "Risk Level",        counts: summary.risk_counts,     colors: { low: "bg-emerald-500", moderate: "bg-yellow-500", high: "bg-orange-500", critical: "bg-red-500" } },
            { title: "Primary Blocker",   counts: summary.blocker_counts,  colors: {} },
            { title: "Severity",          counts: summary.severity_counts, colors: { on_track: "bg-emerald-500", behind: "bg-yellow-500", at_risk: "bg-orange-500", failing: "bg-red-500" } },
            { title: "Action",            counts: summary.action_counts,   colors: {} },
          ].map(({ title, counts, colors }) => (
            <div key={title} className="bg-slate-900 border border-slate-800 rounded-xl p-4 space-y-3">
              <h3 className="text-sm font-semibold text-slate-300">{title}</h3>
              {Object.entries(counts).map(([k, v]) => {
                const pct = summary.total > 0 ? (v / summary.total) * 100 : 0;
                const col = (colors as Record<string, string>)[k] ?? "bg-indigo-500";
                return (
                  <div key={k} className="space-y-1">
                    <div className="flex justify-between text-xs text-slate-400">
                      <span>{fmt(k)}</span><span>{v}</span>
                    </div>
                    <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
                      <div className={`h-full rounded-full ${col}`} style={{ width: `${pct}%` }} />
                    </div>
                  </div>
                );
              })}
            </div>
          ))}
        </div>
      )}

      {/* Sub-score averages */}
      {summary && (
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-3">
          <h3 className="text-sm font-semibold text-slate-300">Average Sub-Scores</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            <ScoreBar label="Pipeline Gap" value={summary.avg_pipeline_gap_score} />
            <ScoreBar label="Conversion Velocity" value={summary.avg_conversion_velocity_score} />
            <ScoreBar label="Knowledge Readiness" value={summary.avg_knowledge_readiness_score} />
            <ScoreBar label="Activity Quality" value={summary.avg_activity_quality_score} />
          </div>
        </div>
      )}

      {/* Filter tabs */}
      <div className="flex flex-wrap gap-2">
        {RISKS.map((r) => (
          <button key={r} onClick={() => setRiskFilter(r)}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium border transition-colors ${
              riskFilter === r
                ? "bg-indigo-600 border-indigo-500 text-white"
                : "bg-slate-900 border-slate-700 text-slate-400 hover:border-slate-500"
            }`}>
            {fmt(r)}
          </button>
        ))}
      </div>

      {/* Rep cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
        {reps.map((rep) => {
          const col = RISK_COLORS[rep.ramp_risk] || "text-slate-400";
          const bg  = RISK_BG[rep.ramp_risk]     || "bg-slate-800/50 border-slate-700";
          return (
            <button key={rep.rep_id} onClick={() => setSelected(rep)} className="text-left w-full">
              <div className={`rounded-xl border p-4 space-y-3 hover:border-indigo-500/50 transition-colors ${bg}`}>
                <div className="flex items-start justify-between">
                  <div>
                    <p className="font-semibold text-slate-100 text-sm">{rep.rep_id}</p>
                    <p className="text-xs text-slate-400">{rep.region}</p>
                  </div>
                  <div className="text-right">
                    <span className={`text-xs font-bold ${col}`}>{fmt(rep.ramp_risk).toUpperCase()}</span>
                    <p className="text-xs text-slate-500 mt-0.5">{fmt(rep.ramp_severity)}</p>
                  </div>
                </div>

                <div className="relative flex items-center gap-3">
                  <div className="relative flex-shrink-0">
                    <RingGauge value={rep.ramp_composite}
                      color={rep.ramp_composite >= 60 ? "#f87171" : rep.ramp_composite >= 40 ? "#fb923c" : rep.ramp_composite >= 20 ? "#facc15" : "#34d399"} />
                    <span className="absolute inset-0 flex items-center justify-center text-xs font-bold text-slate-200">
                      {rep.ramp_composite.toFixed(0)}
                    </span>
                  </div>
                  <div className="flex-1 space-y-1.5 min-w-0">
                    <div className="flex justify-between text-xs text-slate-400">
                      <span>Quota Est.</span>
                      <span className="text-slate-200">{rep.estimated_quota_attainment_pct.toFixed(1)}%</span>
                    </div>
                    <div className="flex justify-between text-xs text-slate-400">
                      <span>Blocker</span>
                      <span className="text-slate-300">{fmt(rep.ramp_blocker)}</span>
                    </div>
                    <div className="flex justify-between text-xs text-slate-400">
                      <span>Action</span>
                      <span className={`${ACTION_COLORS[rep.recommended_action] || "text-slate-400"}`}>{fmt(rep.recommended_action)}</span>
                    </div>
                  </div>
                </div>

                <div className="flex gap-2">
                  {rep.is_under_ramping && (
                    <span className="px-2 py-0.5 text-xs rounded-full bg-red-500/20 text-red-400 border border-red-500/30">Under Ramp</span>
                  )}
                  {rep.requires_intervention && (
                    <span className="px-2 py-0.5 text-xs rounded-full bg-orange-500/20 text-orange-400 border border-orange-500/30">Intervention</span>
                  )}
                </div>

                <p className="text-xs text-slate-500 truncate">{rep.ramp_signal}</p>
              </div>
            </button>
          );
        })}
      </div>

      {selected && <DetailModal rep={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
