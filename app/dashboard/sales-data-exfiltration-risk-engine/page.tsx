"use client";

import { useEffect, useState, useCallback } from "react";

interface ExfiltrationRep {
  rep_id: string;
  region: string;
  exfiltration_risk: string;
  exfiltration_pattern: string;
  exfiltration_severity: string;
  recommended_action: string;
  export_anomaly_score: number;
  access_pattern_score: number;
  boundary_violation_score: number;
  behavioral_risk_score: number;
  exfiltration_composite: number;
  is_exfiltration_risk: boolean;
  requires_immediate_review: boolean;
  estimated_records_at_risk: number;
  exfiltration_signal: string;
}

interface Summary {
  total: number;
  risk_counts: Record<string, number>;
  pattern_counts: Record<string, number>;
  severity_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_exfiltration_composite: number;
  exfiltration_risk_count: number;
  immediate_review_count: number;
  avg_export_anomaly_score: number;
  avg_access_pattern_score: number;
  avg_boundary_violation_score: number;
  avg_behavioral_risk_score: number;
  total_estimated_records_at_risk: number;
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
  normal:    "bg-emerald-500",
  suspicious: "bg-amber-500",
  concerning: "bg-orange-500",
  threat:    "bg-red-500",
};
const PATTERN_LABELS: Record<string, string> = {
  none:                     "No Issues",
  bulk_export:              "Bulk Export",
  territory_boundary_breach: "Territory Breach",
  unusual_access_hours:     "Unusual Hours",
  account_scraping:         "Account Scraping",
  pre_departure_download:   "Pre-Departure Download",
};
const ACTION_LABELS: Record<string, string> = {
  no_action:              "No Action",
  audit_trail_review:     "Audit Trail Review",
  access_restriction:     "Access Restriction",
  security_investigation: "Security Investigation",
  immediate_lockdown:     "Immediate Lockdown",
};
const ACTION_COLORS: Record<string, string> = {
  no_action:              "text-slate-400",
  audit_trail_review:     "text-amber-400",
  access_restriction:     "text-orange-400",
  security_investigation: "text-red-400",
  immediate_lockdown:     "text-red-500",
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

function ThreatRing({ composite }: { composite: number }) {
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

function fmtRec(n: number): string {
  if (n >= 1_000_000) return `${(n / 1_000_000).toFixed(1)}M`;
  if (n >= 1_000) return `${(n / 1_000).toFixed(0)}K`;
  return String(n);
}

function DetailModal({ rep, onClose }: { rep: ExfiltrationRep; onClose: () => void }) {
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
            <p className="text-xs text-slate-500 uppercase tracking-widest">Data Exfiltration Risk</p>
            <h2 className="text-lg font-bold text-slate-100">{rep.rep_id}</h2>
            <p className="text-xs text-slate-400">{rep.region} · {PATTERN_LABELS[rep.exfiltration_pattern]}</p>
          </div>
          <div className="flex flex-col items-end gap-1">
            <span className={`text-xs font-semibold px-2 py-0.5 rounded-full border ${RISK_BG[rep.exfiltration_risk]}`}>
              <span className={RISK_COLORS[rep.exfiltration_risk]}>{rep.exfiltration_risk.toUpperCase()}</span>
            </span>
            <span className={`text-xs px-2 py-0.5 rounded-full text-white ${SEV_COLORS[rep.exfiltration_severity]}`}>
              {rep.exfiltration_severity}
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
                <ThreatRing composite={rep.exfiltration_composite} />
              </div>
              <p className="text-sm text-slate-300 italic text-center">&ldquo;{rep.exfiltration_signal}&rdquo;</p>
              <div className="grid grid-cols-2 gap-3 text-xs">
                <div className="bg-slate-800 rounded-lg p-3">
                  <p className="text-slate-500 mb-1">Composite</p>
                  <p className="text-slate-100 font-bold text-base">{rep.exfiltration_composite.toFixed(1)}</p>
                </div>
                <div className="bg-slate-800 rounded-lg p-3">
                  <p className="text-slate-500 mb-1">Records at Risk</p>
                  <p className="text-red-400 font-bold text-base">{fmtRec(rep.estimated_records_at_risk)}</p>
                </div>
                <div className="bg-slate-800 rounded-lg p-3">
                  <p className="text-slate-500 mb-1">Exfiltration Risk</p>
                  <p className={`font-bold ${rep.is_exfiltration_risk ? "text-red-400" : "text-emerald-400"}`}>
                    {rep.is_exfiltration_risk ? "Confirmed" : "Not flagged"}
                  </p>
                </div>
                <div className="bg-slate-800 rounded-lg p-3">
                  <p className="text-slate-500 mb-1">Immediate Review</p>
                  <p className={`font-bold ${rep.requires_immediate_review ? "text-orange-400" : "text-emerald-400"}`}>
                    {rep.requires_immediate_review ? "Required" : "Not needed"}
                  </p>
                </div>
              </div>
            </>
          )}
          {tab === "scores" && (
            <div className="space-y-3">
              <ScoreBar label="Export Anomaly" value={rep.export_anomaly_score} color="bg-red-500" />
              <ScoreBar label="Access Pattern" value={rep.access_pattern_score} color="bg-orange-500" />
              <ScoreBar label="Boundary Violation" value={rep.boundary_violation_score} color="bg-amber-500" />
              <ScoreBar label="Behavioral Risk" value={rep.behavioral_risk_score} color="bg-violet-500" />
              <div className="pt-2 border-t border-slate-800">
                <ScoreBar label="Exfiltration Composite" value={rep.exfiltration_composite} color="bg-indigo-500" />
              </div>
            </div>
          )}
          {tab === "action" && (
            <div className="space-y-3 text-sm">
              <div className="bg-slate-800 rounded-lg p-4">
                <p className="text-slate-500 text-xs mb-1">Recommended Action</p>
                <p className={`font-semibold ${ACTION_COLORS[rep.recommended_action]}`}>{ACTION_LABELS[rep.recommended_action]}</p>
              </div>
              <div className="bg-slate-800 rounded-lg p-4">
                <p className="text-slate-500 text-xs mb-1">Threat Pattern</p>
                <p className="text-slate-200">{PATTERN_LABELS[rep.exfiltration_pattern]}</p>
              </div>
              <div className="bg-slate-800 rounded-lg p-4">
                <p className="text-slate-500 text-xs mb-1">Severity</p>
                <p className="text-slate-200 capitalize">{rep.exfiltration_severity}</p>
              </div>
              <div className="bg-slate-800 rounded-lg p-4">
                <p className="text-slate-500 text-xs mb-2">Security Flags</p>
                <div className="flex flex-wrap gap-2">
                  {rep.is_exfiltration_risk && <span className="text-xs px-2 py-0.5 rounded-full bg-red-400/10 border border-red-400/30 text-red-400">Exfiltration Confirmed</span>}
                  {rep.requires_immediate_review && <span className="text-xs px-2 py-0.5 rounded-full bg-orange-400/10 border border-orange-400/30 text-orange-400">Immediate Review</span>}
                  {!rep.is_exfiltration_risk && !rep.requires_immediate_review && <span className="text-xs text-slate-500">No critical flags</span>}
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default function SalesDataExfiltrationPage() {
  const [data, setData] = useState<{ reps: ExfiltrationRep[]; summary: Summary } | null>(null);
  const [selected, setSelected] = useState<ExfiltrationRep | null>(null);
  const [riskFilter, setRiskFilter] = useState("all");

  const load = useCallback(async () => {
    const params = new URLSearchParams();
    if (riskFilter !== "all") params.set("risk", riskFilter);
    const res = await fetch(`/api/sales-data-exfiltration-risk-engine?${params}`);
    setData(await res.json());
  }, [riskFilter]);

  useEffect(() => { load(); }, [load]);

  const summary = data?.summary;
  const reps = data?.reps ?? [];

  const kpis = summary
    ? [
        { label: "Total Reps", value: summary.total, sub: "monitored" },
        { label: "Exfiltration Risk", value: summary.exfiltration_risk_count, sub: "confirmed threats", accent: "text-red-400" },
        { label: "Immediate Reviews", value: summary.immediate_review_count, sub: "required", accent: "text-orange-400" },
        { label: "Avg Composite", value: summary.avg_exfiltration_composite.toFixed(1), sub: "threat score" },
        { label: "Records at Risk", value: fmtRec(summary.total_estimated_records_at_risk), sub: "estimated total", accent: "text-amber-400" },
      ]
    : [];

  const patterns = summary
    ? Object.entries(summary.pattern_counts).sort((a, b) => b[1] - a[1])
    : [];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {selected && <DetailModal rep={selected} onClose={() => setSelected(null)} />}

      <div>
        <h1 className="text-2xl font-bold text-slate-100">Sales Data Exfiltration Risk Engine</h1>
        <p className="text-sm text-slate-400 mt-1">Detects bulk CRM exports, boundary breaches, and pre-departure download surges protecting customer data from theft</p>
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
        {/* Sub-score averages */}
        {summary && (
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-3">
            <h2 className="text-sm font-semibold text-slate-300 uppercase tracking-widest mb-3">Avg Threat Scores</h2>
            <ScoreBar label="Export Anomaly" value={summary.avg_export_anomaly_score} color="bg-red-500" />
            <ScoreBar label="Access Pattern" value={summary.avg_access_pattern_score} color="bg-orange-500" />
            <ScoreBar label="Boundary Violation" value={summary.avg_boundary_violation_score} color="bg-amber-500" />
            <ScoreBar label="Behavioral Risk" value={summary.avg_behavioral_risk_score} color="bg-violet-500" />
            <ScoreBar label="Exfiltration Composite" value={summary.avg_exfiltration_composite} color="bg-indigo-500" />
          </div>
        )}

        {/* Pattern distribution */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
          <h2 className="text-sm font-semibold text-slate-300 uppercase tracking-widest mb-4">Threat Patterns</h2>
          <div className="space-y-2">
            {patterns.map(([pat, count]) => (
              <div key={pat} className="flex items-center gap-3">
                <span className="text-xs text-slate-400 w-44 truncate">{PATTERN_LABELS[pat] ?? pat}</span>
                <div className="flex-1 h-2 bg-slate-800 rounded-full">
                  <div
                    className="h-2 rounded-full bg-red-500"
                    style={{ width: summary ? `${(count / summary.total) * 100}%` : "0%" }}
                  />
                </div>
                <span className="text-xs font-mono text-slate-300 w-4 text-right">{count}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Risk Filter */}
      <div className="flex gap-2 flex-wrap">
        {["all", "low", "moderate", "high", "critical"].map((f) => (
          <button key={f} onClick={() => setRiskFilter(f)}
            className={`px-4 py-1.5 rounded-full text-xs font-semibold border transition-colors ${
              riskFilter === f
                ? "bg-red-700 border-red-600 text-white"
                : "bg-slate-800 border-slate-700 text-slate-400 hover:text-slate-200"
            }`}>
            {f === "all" ? "All" : f.charAt(0).toUpperCase() + f.slice(1)}
          </button>
        ))}
      </div>

      {/* Rep Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
        {reps.map((rep) => (
          <button key={rep.rep_id} onClick={() => setSelected(rep)}
            className={`bg-slate-900 border rounded-xl p-4 text-left transition-colors group ${
              rep.is_exfiltration_risk
                ? "border-red-500/40 hover:border-red-400/60"
                : "border-slate-800 hover:border-indigo-500/50"
            }`}>
            <div className="flex items-start justify-between mb-3">
              <div>
                <p className="font-semibold text-slate-100 group-hover:text-indigo-300 transition-colors">{rep.rep_id}</p>
                <p className="text-xs text-slate-500">{rep.region}</p>
              </div>
              <div className="flex flex-col items-end gap-1">
                <span className={`text-xs font-semibold ${RISK_COLORS[rep.exfiltration_risk]}`}>
                  {rep.exfiltration_risk.toUpperCase()}
                </span>
                <span className={`text-xs px-1.5 py-0.5 rounded text-white ${SEV_COLORS[rep.exfiltration_severity]}`}>
                  {rep.exfiltration_severity}
                </span>
              </div>
            </div>
            <div className="flex items-center gap-3 mb-3">
              <ThreatRing composite={rep.exfiltration_composite} />
              <div className="flex-1 space-y-1.5">
                <ScoreBar label="Export" value={rep.export_anomaly_score} color="bg-red-500" />
                <ScoreBar label="Access" value={rep.access_pattern_score} color="bg-orange-500" />
                <ScoreBar label="Boundary" value={rep.boundary_violation_score} color="bg-amber-500" />
              </div>
            </div>
            <p className="text-xs text-slate-400 italic leading-snug line-clamp-2">{rep.exfiltration_signal}</p>
            <div className="flex gap-2 mt-3 flex-wrap">
              {rep.is_exfiltration_risk && (
                <span className="text-xs px-2 py-0.5 rounded-full bg-red-400/10 border border-red-400/30 text-red-400">Threat</span>
              )}
              {rep.requires_immediate_review && (
                <span className="text-xs px-2 py-0.5 rounded-full bg-orange-400/10 border border-orange-400/30 text-orange-400">Immediate</span>
              )}
              <span className={`text-xs px-2 py-0.5 rounded-full bg-slate-800 ${ACTION_COLORS[rep.recommended_action]}`}>
                {ACTION_LABELS[rep.recommended_action]}
              </span>
            </div>
          </button>
        ))}
      </div>
    </div>
  );
}
