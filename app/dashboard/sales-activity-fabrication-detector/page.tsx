"use client";

import { useEffect, useState } from "react";

interface RepRecord {
  rep_id: string;
  rep_name: string;
  region: string;
  manager_id: string;
  fabrication_risk: string;
  fabrication_severity: string;
  primary_fabrication_pattern: string;
  recommended_action: string;
  call_authenticity_score: number;
  meeting_authenticity_score: number;
  timing_anomaly_score: number;
  corroboration_score: number;
  fabrication_composite: number;
  is_likely_fabricating: boolean;
  requires_audit: boolean;
  estimated_fake_activity_pct: number;
  fabrication_signal: string;
}

interface Summary {
  total: number;
  risk_counts: Record<string, number>;
  severity_counts: Record<string, number>;
  pattern_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_fabrication_composite: number;
  likely_fabricating_count: number;
  audit_required_count: number;
  avg_call_authenticity_score: number;
  avg_meeting_authenticity_score: number;
  avg_timing_anomaly_score: number;
  avg_corroboration_score: number;
  avg_estimated_fake_activity_pct: number;
}

const RISK_ORDER = ["none", "low", "moderate", "high", "critical"];
const RISK_COLORS: Record<string, string> = {
  none:     "bg-slate-700 text-slate-300",
  low:      "bg-emerald-900 text-emerald-300",
  moderate: "bg-amber-900 text-amber-300",
  high:     "bg-orange-900 text-orange-300",
  critical: "bg-red-900 text-red-300",
};
const RISK_RING: Record<string, string> = {
  none:     "#475569",
  low:      "#10b981",
  moderate: "#f59e0b",
  high:     "#f97316",
  critical: "#ef4444",
};
const SEVERITY_COLORS: Record<string, string> = {
  clean:            "bg-emerald-900 text-emerald-300",
  suspicious:       "bg-amber-900 text-amber-300",
  likely_fabricated:"bg-orange-900 text-orange-300",
  confirmed_fraud:  "bg-red-900 text-red-300",
};
const PATTERN_LABELS: Record<string, string> = {
  none:                 "None",
  phantom_calls:        "Phantom Calls",
  fake_meetings:        "Fake Meetings",
  bulk_logging:         "Bulk Logging",
  no_follow_up:         "No Follow-Up",
  note_absence:         "Note Absence",
  timestamp_clustering: "Timestamp Clustering",
};
const ACTION_LABELS: Record<string, string> = {
  no_action:      "No Action",
  monitor:        "Monitor",
  audit_request:  "Audit Request",
  manager_review: "Manager Review",
  hr_escalation:  "HR Escalation",
};

function anomalyColor(v: number) {
  if (v < 20) return "#10b981";
  if (v < 40) return "#f59e0b";
  if (v < 60) return "#f97316";
  return "#ef4444";
}

function ScoreBar({ label, value, color }: { label: string; value: number; color: string }) {
  return (
    <div>
      <div className="flex justify-between text-xs text-slate-400 mb-1">
        <span>{label}</span><span className="text-slate-200">{value.toFixed(0)}</span>
      </div>
      <div className="h-1.5 bg-slate-700 rounded-full overflow-hidden">
        <div className="h-full rounded-full transition-all" style={{ width: `${Math.min(value, 100)}%`, backgroundColor: color }} />
      </div>
    </div>
  );
}

function CompositeRing({ value, risk }: { value: number; risk: string }) {
  const r = 28; const circ = 2 * Math.PI * r;
  const fill = (Math.min(value, 100) / 100) * circ;
  const color = RISK_RING[risk] ?? "#475569";
  return (
    <svg width="72" height="72" viewBox="0 0 72 72">
      <circle cx="36" cy="36" r={r} fill="none" stroke="#1e293b" strokeWidth="7" />
      <circle cx="36" cy="36" r={r} fill="none" stroke={color} strokeWidth="7"
        strokeDasharray={`${fill} ${circ}`} strokeLinecap="round" transform="rotate(-90 36 36)" />
      <text x="36" y="40" textAnchor="middle" fill={color} fontSize="13" fontWeight="bold">{value.toFixed(0)}</text>
    </svg>
  );
}

function DetailModal({ rep, onClose }: { rep: RepRecord; onClose: () => void }) {
  const [tab, setTab] = useState(0);
  useEffect(() => {
    const fn = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", fn); return () => window.removeEventListener("keydown", fn);
  }, [onClose]);
  const tabs = ["Overview", "Authenticity Scores", "Investigation"];
  const riskCls = RISK_COLORS[rep.fabrication_risk] ?? "bg-slate-700 text-slate-300";
  const sevCls  = SEVERITY_COLORS[rep.fabrication_severity] ?? "bg-slate-700 text-slate-300";
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4" onClick={onClose}>
      <div className="absolute inset-0 bg-black/70" />
      <div className="relative bg-slate-900 border border-slate-700 rounded-2xl shadow-2xl w-full max-w-lg" onClick={(e) => e.stopPropagation()}>
        <div className="flex items-start justify-between p-6 border-b border-slate-800">
          <div>
            <h2 className="text-lg font-semibold text-slate-100">{rep.rep_name}</h2>
            <p className="text-sm text-slate-400">{rep.region} · Manager: {rep.manager_id}</p>
            <div className="flex gap-2 mt-2 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${riskCls}`}>{rep.fabrication_risk}</span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${sevCls}`}>{rep.fabrication_severity.replace("_", " ")}</span>
              {rep.is_likely_fabricating && <span className="px-2 py-0.5 rounded text-xs font-medium bg-red-900 text-red-300">⚠ Likely Fabricating</span>}
              {rep.requires_audit && <span className="px-2 py-0.5 rounded text-xs font-medium bg-amber-900 text-amber-300">🔍 Audit Required</span>}
            </div>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-slate-300 text-xl ml-4">✕</button>
        </div>
        <div className="flex border-b border-slate-800">
          {tabs.map((t, i) => (
            <button key={t} onClick={() => setTab(i)}
              className={`flex-1 py-3 text-sm font-medium transition-colors ${tab === i ? "text-indigo-400 border-b-2 border-indigo-400" : "text-slate-500 hover:text-slate-300"}`}>
              {t}
            </button>
          ))}
        </div>
        <div className="p-6">
          {tab === 0 && (
            <div className="space-y-4">
              <div className="flex items-center gap-4 p-4 bg-slate-800 rounded-xl">
                <CompositeRing value={rep.fabrication_composite} risk={rep.fabrication_risk} />
                <div>
                  <p className="text-xs text-slate-400">Fabrication Composite</p>
                  <p className="text-2xl font-bold text-slate-100">{rep.fabrication_composite.toFixed(1)}</p>
                  <p className="text-xs text-slate-400 mt-1">~{rep.estimated_fake_activity_pct.toFixed(0)}% est. fake activity</p>
                </div>
              </div>
              <div className="p-4 bg-slate-800 rounded-xl">
                <p className="text-xs text-slate-400 mb-1">Fabrication Signal</p>
                <p className="text-sm text-slate-200">{rep.fabrication_signal}</p>
              </div>
              <div className="grid grid-cols-2 gap-3 text-sm">
                <div className="p-3 bg-slate-800 rounded-lg">
                  <p className="text-xs text-slate-400">Pattern</p>
                  <p className="text-slate-200 font-medium">{PATTERN_LABELS[rep.primary_fabrication_pattern] ?? rep.primary_fabrication_pattern}</p>
                </div>
                <div className="p-3 bg-slate-800 rounded-lg">
                  <p className="text-xs text-slate-400">Est. Fake %</p>
                  <p className="text-slate-200 font-medium">{rep.estimated_fake_activity_pct.toFixed(1)}%</p>
                </div>
              </div>
            </div>
          )}
          {tab === 1 && (
            <div className="space-y-4">
              <ScoreBar label="Call Authenticity Risk"    value={rep.call_authenticity_score}    color={anomalyColor(rep.call_authenticity_score)} />
              <ScoreBar label="Meeting Authenticity Risk" value={rep.meeting_authenticity_score} color={anomalyColor(rep.meeting_authenticity_score)} />
              <ScoreBar label="Timing Anomaly"            value={rep.timing_anomaly_score}        color={anomalyColor(rep.timing_anomaly_score)} />
              <ScoreBar label="Corroboration Gap"         value={rep.corroboration_score}         color={anomalyColor(rep.corroboration_score)} />
              <div className="mt-4 p-3 bg-slate-800 rounded-lg text-xs text-slate-400">
                Composite = Call×0.30 + Meeting×0.25 + Timing×0.25 + Corroboration×0.20
              </div>
            </div>
          )}
          {tab === 2 && (
            <div className="space-y-4">
              <div className="p-4 bg-slate-800 rounded-xl">
                <p className="text-xs text-slate-400 mb-1">Recommended Action</p>
                <p className="text-lg font-semibold text-indigo-300">{ACTION_LABELS[rep.recommended_action] ?? rep.recommended_action}</p>
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div className={`p-3 rounded-lg ${rep.is_likely_fabricating ? "bg-red-900/50 border border-red-700" : "bg-slate-800"}`}>
                  <p className="text-xs text-slate-400">Likely Fabricating</p>
                  <p className={`font-semibold ${rep.is_likely_fabricating ? "text-red-300" : "text-emerald-400"}`}>{rep.is_likely_fabricating ? "YES" : "No"}</p>
                </div>
                <div className={`p-3 rounded-lg ${rep.requires_audit ? "bg-amber-900/50 border border-amber-700" : "bg-slate-800"}`}>
                  <p className="text-xs text-slate-400">Audit Required</p>
                  <p className={`font-semibold ${rep.requires_audit ? "text-amber-300" : "text-emerald-400"}`}>{rep.requires_audit ? "YES" : "No"}</p>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default function SalesActivityFabricationDetectorPage() {
  const [data, setData]     = useState<{ reps: RepRecord[]; summary: Summary } | null>(null);
  const [filter, setFilter] = useState("all");
  const [selected, setSelected] = useState<RepRecord | null>(null);

  const load = (risk?: string) => {
    const params = risk && risk !== "all" ? `?risk=${risk}` : "";
    fetch(`/api/sales-activity-fabrication-detector${params}`).then((r) => r.json()).then(setData);
  };

  useEffect(() => { load(); }, [load]);
  const handleFilter = (f: string) => { setFilter(f); load(f === "all" ? undefined : f); };

  if (!data) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-slate-400 animate-pulse">Loading activity fabrication detector...</div>
    </div>
  );

  const { reps, summary } = data;
  const riskTotal = Object.values(summary.risk_counts).reduce((a, b) => a + b, 0) || 1;
  const patTotal  = Object.values(summary.pattern_counts).reduce((a, b) => a + b, 0) || 1;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
      {selected && <DetailModal rep={selected} onClose={() => setSelected(null)} />}
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-slate-100">Sales Activity Fabrication Detector</h1>
        <p className="text-slate-400 text-sm mt-1">Phantom call detection · fake meeting analysis · CRM log integrity monitoring</p>
      </div>

      {/* KPI Strip */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        {[
          { label: "Total Reps", value: summary.total, sub: "monitored" },
          { label: "Likely Fabricating", value: summary.likely_fabricating_count, sub: "flagged", alert: summary.likely_fabricating_count > 0 },
          { label: "Audit Required", value: summary.audit_required_count, sub: "need review", alert: summary.audit_required_count > 0 },
          { label: "Avg Fake Activity", value: `${summary.avg_estimated_fake_activity_pct.toFixed(1)}%`, sub: "estimated" },
        ].map(({ label, value, sub, alert }) => (
          <div key={label} className={`bg-slate-900 border rounded-xl p-4 ${alert ? "border-red-700" : "border-slate-800"}`}>
            <p className="text-xs text-slate-400">{label}</p>
            <p className={`text-2xl font-bold mt-1 ${alert ? "text-red-400" : "text-slate-100"}`}>{value}</p>
            <p className="text-xs text-slate-500 mt-1">{sub}</p>
          </div>
        ))}
      </div>

      {/* Avg Scores + Distributions */}
      <div className="grid lg:grid-cols-2 gap-4 mb-6">
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
          <h2 className="text-sm font-semibold text-slate-300 mb-4">Avg Anomaly Sub-Scores</h2>
          <div className="space-y-3">
            {[
              { label: "Call Authenticity Risk",    value: summary.avg_call_authenticity_score },
              { label: "Meeting Authenticity Risk", value: summary.avg_meeting_authenticity_score },
              { label: "Timing Anomaly",            value: summary.avg_timing_anomaly_score },
              { label: "Corroboration Gap",         value: summary.avg_corroboration_score },
            ].map(({ label, value }) => (
              <div key={label}>
                <div className="flex justify-between text-xs text-slate-400 mb-1">
                  <span>{label}</span><span className="text-slate-200">{value.toFixed(1)}</span>
                </div>
                <div className="h-2 bg-slate-700 rounded-full overflow-hidden">
                  <div className="h-full rounded-full" style={{ width: `${Math.min(value, 100)}%`, backgroundColor: anomalyColor(value) }} />
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-4">
          <div>
            <h2 className="text-sm font-semibold text-slate-300 mb-3">Risk Level Distribution</h2>
            <div className="space-y-2">
              {RISK_ORDER.map((lv) => {
                const cnt = summary.risk_counts[lv] ?? 0;
                return (
                  <div key={lv} className="flex items-center gap-2 text-xs">
                    <span className="w-20 text-slate-400 capitalize">{lv}</span>
                    <div className="flex-1 h-2 bg-slate-700 rounded-full overflow-hidden">
                      <div className="h-full rounded-full" style={{ width: `${(cnt / riskTotal) * 100}%`, backgroundColor: RISK_RING[lv] }} />
                    </div>
                    <span className="w-5 text-right text-slate-300">{cnt}</span>
                  </div>
                );
              })}
            </div>
          </div>
          <div>
            <h2 className="text-sm font-semibold text-slate-300 mb-3">Fabrication Pattern Distribution</h2>
            <div className="space-y-1.5">
              {Object.entries(summary.pattern_counts).map(([pat, cnt]) => (
                <div key={pat} className="flex items-center gap-2 text-xs">
                  <span className="w-36 text-slate-400">{PATTERN_LABELS[pat] ?? pat}</span>
                  <div className="flex-1 h-1.5 bg-slate-700 rounded-full overflow-hidden">
                    <div className="h-full rounded-full bg-violet-500" style={{ width: `${(cnt / patTotal) * 100}%` }} />
                  </div>
                  <span className="w-5 text-right text-slate-300">{cnt}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Filter tabs */}
      <div className="flex flex-wrap gap-2 mb-4">
        {["all", ...RISK_ORDER].map((lv) => (
          <button key={lv} onClick={() => handleFilter(lv)}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
              filter === lv ? "bg-indigo-600 text-white" : "bg-slate-800 text-slate-400 hover:text-slate-200"
            }`}>
            {lv === "all" ? "All Reps" : lv.charAt(0).toUpperCase() + lv.slice(1)}
            {lv !== "all" && (summary.risk_counts[lv] ?? 0) > 0 && (
              <span className="ml-1 text-slate-400">({summary.risk_counts[lv]})</span>
            )}
          </button>
        ))}
      </div>

      {/* Rep Cards */}
      <div className="grid sm:grid-cols-2 xl:grid-cols-3 gap-4">
        {reps.map((r) => {
          const riskCls = RISK_COLORS[r.fabrication_risk] ?? "bg-slate-700 text-slate-300";
          const sevCls  = SEVERITY_COLORS[r.fabrication_severity] ?? "bg-slate-700 text-slate-300";
          return (
            <div key={r.rep_id} onClick={() => setSelected(r)}
              className="bg-slate-900 border border-slate-800 rounded-xl p-4 cursor-pointer hover:border-slate-600 transition-colors">
              <div className="flex items-start justify-between mb-3">
                <div>
                  <p className="font-semibold text-slate-100">{r.rep_name}</p>
                  <p className="text-xs text-slate-400">{r.region} · {r.manager_id}</p>
                </div>
                <div className="flex flex-col gap-1 items-end">
                  <span className={`px-2 py-0.5 rounded text-xs font-medium ${riskCls}`}>{r.fabrication_risk}</span>
                  <span className={`px-2 py-0.5 rounded text-xs font-medium ${sevCls}`}>{r.fabrication_severity.replace("_", " ")}</span>
                </div>
              </div>
              <div className="flex items-center gap-3 mb-3">
                <CompositeRing value={r.fabrication_composite} risk={r.fabrication_risk} />
                <div className="flex-1 space-y-1.5">
                  <ScoreBar label="Call Auth."  value={r.call_authenticity_score}    color={anomalyColor(r.call_authenticity_score)} />
                  <ScoreBar label="Meeting"     value={r.meeting_authenticity_score} color={anomalyColor(r.meeting_authenticity_score)} />
                  <ScoreBar label="Timing"      value={r.timing_anomaly_score}        color={anomalyColor(r.timing_anomaly_score)} />
                  <ScoreBar label="Corroborate" value={r.corroboration_score}         color={anomalyColor(r.corroboration_score)} />
                </div>
              </div>
              <div className="flex gap-2 flex-wrap mb-2">
                {r.is_likely_fabricating && <span className="text-xs text-red-400 bg-red-900/40 px-2 py-0.5 rounded">⚠ Fabricating</span>}
                {r.requires_audit && <span className="text-xs text-amber-300 bg-amber-900/40 px-2 py-0.5 rounded">🔍 Audit</span>}
                <span className="text-xs text-slate-400 bg-slate-800 px-2 py-0.5 rounded">{ACTION_LABELS[r.recommended_action]}</span>
              </div>
              <p className="text-xs text-slate-400 line-clamp-2">{r.fabrication_signal}</p>
            </div>
          );
        })}
      </div>
    </div>
  );
}
