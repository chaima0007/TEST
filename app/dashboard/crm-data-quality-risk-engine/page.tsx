"use client";

import { useEffect, useState, useCallback } from "react";

interface QualityRep {
  rep_id: string;
  region: string;
  data_quality_risk: string;
  quality_failure_mode: string;
  quality_severity: string;
  recommended_action: string;
  completeness_score: number;
  accuracy_score: number;
  timeliness_score: number;
  activity_coverage_score: number;
  quality_composite: number;
  is_data_quality_risk: boolean;
  requires_data_audit: boolean;
  estimated_pipeline_distortion_pct: number;
  quality_signal: string;
}

interface Summary {
  total: number;
  risk_counts: Record<string, number>;
  failure_mode_counts: Record<string, number>;
  severity_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_quality_composite: number;
  data_quality_risk_count: number;
  audit_required_count: number;
  avg_completeness_score: number;
  avg_accuracy_score: number;
  avg_timeliness_score: number;
  avg_activity_coverage_score: number;
  avg_estimated_pipeline_distortion_pct: number;
}

const RISK_COLORS: Record<string, string> = {
  low:      "text-emerald-400",
  moderate: "text-amber-400",
  high:     "text-orange-400",
  critical: "text-red-400",
};

const RISK_BG: Record<string, string> = {
  low:      "bg-emerald-500/20 border-emerald-500/40",
  moderate: "bg-amber-500/20 border-amber-500/40",
  high:     "bg-orange-500/20 border-orange-500/40",
  critical: "bg-red-500/20 border-red-500/40",
};

const MODE_COLORS: Record<string, string> = {
  none:               "text-slate-400",
  missing_data:       "text-amber-400",
  stale_records:      "text-orange-400",
  stage_drift:        "text-violet-400",
  activity_gap:       "text-sky-400",
  duplicate_accounts: "text-red-400",
};

const SEVERITY_BADGE: Record<string, string> = {
  clean:      "bg-emerald-500/10 text-emerald-300",
  degraded:   "bg-amber-500/10 text-amber-300",
  unreliable: "bg-orange-500/10 text-orange-300",
  corrupt:    "bg-red-500/10 text-red-300",
};

const ACTION_BADGE: Record<string, string> = {
  no_action:       "bg-slate-700 text-slate-300",
  self_remediate:  "bg-sky-500/20 text-sky-300",
  crm_coaching:    "bg-amber-500/20 text-amber-300",
  data_audit:      "bg-orange-500/20 text-orange-300",
  pipeline_freeze: "bg-red-700/40 text-red-200 border border-red-500/50",
};

function CompositeRing({ value }: { value: number }) {
  const r = 28;
  const circ = 2 * Math.PI * r;
  const fill = (value / 100) * circ;
  const color = value >= 60 ? "#ef4444" : value >= 40 ? "#f97316" : value >= 20 ? "#f59e0b" : "#10b981";
  return (
    <svg width="72" height="72" viewBox="0 0 72 72">
      <circle cx="36" cy="36" r={r} fill="none" stroke="#1e293b" strokeWidth="6" />
      <circle cx="36" cy="36" r={r} fill="none" stroke={color} strokeWidth="6"
        strokeDasharray={`${fill} ${circ}`} strokeLinecap="round"
        transform="rotate(-90 36 36)" />
      <text x="36" y="40" textAnchor="middle" fill={color} fontSize="13" fontWeight="bold">{value.toFixed(0)}</text>
    </svg>
  );
}

function ScoreBar({ label, value, color }: { label: string; value: number; color: string }) {
  return (
    <div>
      <div className="flex justify-between text-xs mb-1">
        <span className="text-slate-400">{label}</span>
        <span className={color}>{value.toFixed(1)}</span>
      </div>
      <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
        <div className={`h-full rounded-full ${color.replace("text-", "bg-")}`}
          style={{ width: `${Math.min(value, 100)}%` }} />
      </div>
    </div>
  );
}

function DetailModal({ rep, onClose }: { rep: QualityRep; onClose: () => void }) {
  const [tab, setTab] = useState<"overview" | "scores" | "action">("overview");

  useEffect(() => {
    const handler = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [onClose]);

  const tabs = [
    { id: "overview" as const, label: "Overview" },
    { id: "scores"   as const, label: "Quality Scores" },
    { id: "action"   as const, label: "Action" },
  ];

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4"
      onClick={onClose}>
      <div className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-lg shadow-2xl"
        onClick={(e) => e.stopPropagation()}>
        <div className="p-6 border-b border-slate-800">
          <div className="flex items-start justify-between gap-4">
            <div>
              <p className="text-xs text-slate-500 mb-1">{rep.rep_id} · {rep.region}</p>
              <h2 className="text-lg font-bold text-white">{rep.rep_id}</h2>
              <div className="flex items-center gap-2 mt-2 flex-wrap">
                <span className={`text-xs px-2 py-0.5 rounded-full border ${RISK_BG[rep.data_quality_risk]}`}>
                  {rep.data_quality_risk.toUpperCase()} RISK
                </span>
                <span className={`text-xs px-2 py-0.5 rounded-full ${SEVERITY_BADGE[rep.quality_severity]}`}>
                  {rep.quality_severity}
                </span>
              </div>
            </div>
            <CompositeRing value={rep.quality_composite} />
          </div>
        </div>

        <div className="flex border-b border-slate-800">
          {tabs.map((t) => (
            <button key={t.id} onClick={() => setTab(t.id)}
              className={`flex-1 py-3 text-xs font-medium transition-colors ${
                tab === t.id ? "text-indigo-400 border-b-2 border-indigo-400" : "text-slate-500 hover:text-slate-300"
              }`}>
              {t.label}
            </button>
          ))}
        </div>

        <div className="p-6">
          {tab === "overview" && (
            <div className="space-y-4">
              <div className="grid grid-cols-2 gap-3">
                <div className="bg-slate-800/60 rounded-lg p-3">
                  <p className="text-xs text-slate-500">Failure Mode</p>
                  <p className={`text-sm font-semibold mt-1 ${MODE_COLORS[rep.quality_failure_mode]}`}>
                    {rep.quality_failure_mode.replace(/_/g, " ")}
                  </p>
                </div>
                <div className="bg-slate-800/60 rounded-lg p-3">
                  <p className="text-xs text-slate-500">Pipeline Distortion</p>
                  <p className={`text-sm font-semibold mt-1 ${rep.estimated_pipeline_distortion_pct > 30 ? "text-red-400" : "text-amber-400"}`}>
                    {rep.estimated_pipeline_distortion_pct.toFixed(1)}%
                  </p>
                </div>
                <div className="bg-slate-800/60 rounded-lg p-3">
                  <p className="text-xs text-slate-500">Quality Risk</p>
                  <p className={`text-sm font-semibold mt-1 ${rep.is_data_quality_risk ? "text-red-400" : "text-emerald-400"}`}>
                    {rep.is_data_quality_risk ? "Active" : "None"}
                  </p>
                </div>
                <div className="bg-slate-800/60 rounded-lg p-3">
                  <p className="text-xs text-slate-500">Data Audit</p>
                  <p className={`text-sm font-semibold mt-1 ${rep.requires_data_audit ? "text-orange-400" : "text-emerald-400"}`}>
                    {rep.requires_data_audit ? "Required" : "Not needed"}
                  </p>
                </div>
              </div>
              <div className="bg-slate-800/40 rounded-lg p-3 border-l-2 border-sky-500">
                <p className="text-xs text-slate-400 italic">{rep.quality_signal}</p>
              </div>
            </div>
          )}

          {tab === "scores" && (
            <div className="space-y-3">
              <ScoreBar label="Completeness Score"      value={rep.completeness_score}       color="text-amber-400" />
              <ScoreBar label="Accuracy Score"          value={rep.accuracy_score}           color="text-orange-400" />
              <ScoreBar label="Timeliness Score"        value={rep.timeliness_score}         color="text-red-400" />
              <ScoreBar label="Activity Coverage Score" value={rep.activity_coverage_score}  color="text-violet-400" />
              <div className="pt-2 border-t border-slate-800">
                <div className="flex justify-between text-sm">
                  <span className="text-slate-400 font-medium">Quality Composite</span>
                  <span className="text-white font-bold">{rep.quality_composite.toFixed(1)}</span>
                </div>
                <p className="text-xs text-slate-600 mt-1">completeness×0.30 + accuracy×0.25 + timeliness×0.25 + activity×0.20</p>
              </div>
            </div>
          )}

          {tab === "action" && (
            <div className="space-y-4">
              <div className={`rounded-xl p-4 border ${RISK_BG[rep.data_quality_risk]}`}>
                <p className="text-xs text-slate-400 mb-1">Recommended Action</p>
                <p className={`text-xl font-bold ${RISK_COLORS[rep.data_quality_risk]}`}>
                  {rep.recommended_action.replace(/_/g, " ").toUpperCase()}
                </p>
              </div>
              <div className="bg-slate-800/40 rounded-lg p-3 space-y-2">
                <div className="flex justify-between text-xs">
                  <span className="text-slate-400">Severity</span>
                  <span className={SEVERITY_BADGE[rep.quality_severity].split(" ")[1]}>{rep.quality_severity}</span>
                </div>
                <div className="flex justify-between text-xs">
                  <span className="text-slate-400">Composite</span>
                  <span className="text-white">{rep.quality_composite.toFixed(1)} / 100</span>
                </div>
                <div className="flex justify-between text-xs">
                  <span className="text-slate-400">Est. Pipeline Distortion</span>
                  <span className="text-orange-400">{rep.estimated_pipeline_distortion_pct.toFixed(1)}%</span>
                </div>
              </div>
            </div>
          )}
        </div>

        <div className="px-6 pb-6">
          <button onClick={onClose}
            className="w-full py-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 text-sm transition-colors">
            Close
          </button>
        </div>
      </div>
    </div>
  );
}

export default function CRMDataQualityPage() {
  const [data, setData]       = useState<{ reps: QualityRep[]; summary: Summary } | null>(null);
  const [loading, setLoading] = useState(true);
  const [riskFilter, setRiskFilter] = useState<string>("");
  const [modeFilter, setModeFilter] = useState<string>("");
  const [selected, setSelected] = useState<QualityRep | null>(null);

  const load = useCallback(async () => {
    setLoading(true);
    const params = new URLSearchParams();
    if (riskFilter) params.set("risk", riskFilter);
    if (modeFilter) params.set("mode", modeFilter);
    const res  = await fetch(`/api/crm-data-quality-risk-engine?${params}`);
    const json = await res.json();
    setData(json);
    setLoading(false);
  }, [riskFilter, modeFilter]);

  useEffect(() => { load(); }, [load]);

  const s    = data?.summary;
  const reps = data?.reps ?? [];
  const riskLevels = ["low", "moderate", "high", "critical"];
  const failureModes = ["none", "missing_data", "stale_records", "stage_drift", "activity_gap", "duplicate_accounts"];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
      <div className="max-w-7xl mx-auto space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white">CRM Data Quality Risk Engine</h1>
          <p className="text-slate-400 text-sm mt-1">
            Detects incomplete, stale, and inconsistent CRM records that distort pipeline visibility and forecast accuracy
          </p>
        </div>

        {s && (
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {[
              { label: "Total Reps",        value: s.total,                   sub: "evaluated" },
              { label: "Quality Risk",       value: s.data_quality_risk_count, sub: "flagged" },
              { label: "Audit Required",    value: s.audit_required_count,    sub: "reps" },
              { label: "Avg Distortion",    value: `${s.avg_estimated_pipeline_distortion_pct.toFixed(1)}%`, sub: "pipeline est." },
            ].map((k) => (
              <div key={k.label} className="bg-slate-900 border border-slate-800 rounded-xl p-4">
                <p className="text-xs text-slate-500">{k.label}</p>
                <p className="text-2xl font-bold text-white mt-1">{k.value}</p>
                <p className="text-xs text-slate-600 mt-0.5">{k.sub}</p>
              </div>
            ))}
          </div>
        )}

        {s && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
              <h2 className="text-sm font-semibold text-slate-300 mb-4">Average Quality Sub-Scores</h2>
              <div className="space-y-3">
                {[
                  { label: "Completeness",      value: s.avg_completeness_score,      color: "text-amber-400" },
                  { label: "Accuracy",          value: s.avg_accuracy_score,          color: "text-orange-400" },
                  { label: "Timeliness",        value: s.avg_timeliness_score,        color: "text-red-400" },
                  { label: "Activity Coverage", value: s.avg_activity_coverage_score, color: "text-violet-400" },
                ].map((item) => (
                  <ScoreBar key={item.label} label={item.label} value={item.value} color={item.color} />
                ))}
              </div>
            </div>

            <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
              <h2 className="text-sm font-semibold text-slate-300 mb-4">Failure Mode Distribution</h2>
              <div className="space-y-2">
                {failureModes.filter((m) => s.failure_mode_counts[m]).map((m) => {
                  const count = s.failure_mode_counts[m] || 0;
                  const pct   = (count / s.total) * 100;
                  return (
                    <div key={m}>
                      <div className="flex justify-between text-xs mb-1">
                        <span className={MODE_COLORS[m]}>{m.replace(/_/g, " ")}</span>
                        <span className="text-slate-400">{count}</span>
                      </div>
                      <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
                        <div className={`h-full rounded-full ${(MODE_COLORS[m] || "text-slate-400").replace("text-", "bg-")}`}
                          style={{ width: `${pct}%` }} />
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          </div>
        )}

        <div className="flex flex-wrap gap-3">
          <div>
            <p className="text-xs text-slate-500 mb-1">Risk Level</p>
            <div className="flex flex-wrap gap-1">
              {["", ...riskLevels].map((r) => (
                <button key={r || "all"} onClick={() => setRiskFilter(r)}
                  className={`px-3 py-1 rounded-full text-xs transition-colors ${
                    riskFilter === r ? "bg-indigo-600 text-white" : "bg-slate-800 text-slate-400 hover:bg-slate-700"
                  }`}>
                  {r || "All"}
                </button>
              ))}
            </div>
          </div>
          <div>
            <p className="text-xs text-slate-500 mb-1">Failure Mode</p>
            <div className="flex flex-wrap gap-1">
              {["", ...failureModes].map((m) => (
                <button key={m || "all"} onClick={() => setModeFilter(m)}
                  className={`px-3 py-1 rounded-full text-xs transition-colors ${
                    modeFilter === m ? "bg-indigo-600 text-white" : "bg-slate-800 text-slate-400 hover:bg-slate-700"
                  }`}>
                  {m ? m.replace(/_/g, " ") : "All"}
                </button>
              ))}
            </div>
          </div>
        </div>

        {loading ? (
          <div className="flex items-center justify-center h-40">
            <div className="w-8 h-8 border-2 border-indigo-500 border-t-transparent rounded-full animate-spin" />
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
            {reps.map((rep) => (
              <button key={rep.rep_id} onClick={() => setSelected(rep)} className="text-left w-full">
                <div className={`bg-slate-900 border rounded-xl p-4 hover:border-indigo-500 transition-colors cursor-pointer ${
                  rep.is_data_quality_risk ? "border-orange-500/40" : "border-slate-800"
                }`}>
                  <div className="flex items-start justify-between gap-3 mb-3">
                    <div className="min-w-0">
                      <div className="flex items-center gap-2 flex-wrap mb-1">
                        <span className={`text-xs px-2 py-0.5 rounded-full border ${RISK_BG[rep.data_quality_risk]}`}>
                          {rep.data_quality_risk}
                        </span>
                        <span className={`text-xs ${MODE_COLORS[rep.quality_failure_mode]}`}>
                          {rep.quality_failure_mode.replace(/_/g, " ")}
                        </span>
                      </div>
                      <p className="text-sm font-semibold text-white">{rep.rep_id}</p>
                      <p className="text-xs text-slate-500">{rep.region}</p>
                    </div>
                    <CompositeRing value={rep.quality_composite} />
                  </div>

                  <div className="space-y-1.5 mb-3">
                    <ScoreBar label="Completeness" value={rep.completeness_score}      color="text-amber-400" />
                    <ScoreBar label="Accuracy"     value={rep.accuracy_score}          color="text-orange-400" />
                    <ScoreBar label="Timeliness"   value={rep.timeliness_score}        color="text-red-400" />
                    <ScoreBar label="Activity"     value={rep.activity_coverage_score} color="text-violet-400" />
                  </div>

                  <div className="flex items-center justify-between mb-2">
                    <span className={`text-xs px-2 py-0.5 rounded-full ${ACTION_BADGE[rep.recommended_action]}`}>
                      {rep.recommended_action.replace(/_/g, " ")}
                    </span>
                    <span className={`text-xs px-2 py-0.5 rounded-full ${SEVERITY_BADGE[rep.quality_severity]}`}>
                      {rep.quality_severity}
                    </span>
                  </div>

                  <p className="text-xs text-slate-500 italic line-clamp-1">{rep.quality_signal}</p>
                  {rep.estimated_pipeline_distortion_pct > 0 && (
                    <div className="text-xs text-orange-400 font-medium mt-1">
                      Pipeline distortion est.: {rep.estimated_pipeline_distortion_pct.toFixed(1)}%
                    </div>
                  )}
                </div>
              </button>
            ))}
          </div>
        )}
      </div>

      {selected && <DetailModal rep={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
