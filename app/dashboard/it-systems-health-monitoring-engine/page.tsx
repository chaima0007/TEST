"use client";

import { useState, useEffect, useCallback } from "react";

// ── Types ─────────────────────────────────────────────────────────────────────

type SystemItem = {
  system_id: string;
  environment: string;
  region: string;
  system_risk: string;
  system_pattern: string;
  system_severity: string;
  recommended_action: string;
  performance_score: number;
  capacity_score: number;
  security_score: number;
  reliability_score: number;
  system_composite: number;
  has_system_alert: boolean;
  requires_immediate_action: boolean;
  estimated_downtime_risk_hours: number;
  system_signal: string;
  cpu_utilization_pct: number;
  memory_utilization_pct: number;
  disk_utilization_pct: number;
  network_latency_ms: number;
  error_rate_pct: number;
  uptime_pct: number;
  incident_count_30d: number;
  mean_time_to_recovery_hours: number;
  security_vulnerability_count: number;
  failed_security_scans: number;
  patch_compliance_pct: number;
  integration_failure_rate_pct: number;
  api_error_rate_pct: number;
  data_pipeline_lag_minutes: number;
  sla_compliance_pct: number;
  backup_success_rate_pct: number;
  change_failure_rate_pct: number;
  deployment_frequency_per_week: number;
  avg_response_time_ms: number;
};

type Summary = {
  total: number;
  risk_counts: Record<string, number>;
  pattern_counts: Record<string, number>;
  severity_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_system_composite: number;
  system_alert_count: number;
  immediate_action_count: number;
  avg_performance_score: number;
  avg_capacity_score: number;
  avg_security_score: number;
  avg_reliability_score: number;
  avg_estimated_downtime_risk_hours: number;
};

// ── helpers ───────────────────────────────────────────────────────────────────

function riskColor(r: string) {
  const m: Record<string, string> = {
    low:      "text-emerald-400",
    moderate: "text-amber-400",
    high:     "text-orange-400",
    critical: "text-red-400",
  };
  return m[r] ?? "text-slate-400";
}

function riskBg(r: string) {
  const m: Record<string, string> = {
    low:      "bg-emerald-500/10 border-emerald-500/30",
    moderate: "bg-amber-500/10 border-amber-500/30",
    high:     "bg-orange-500/10 border-orange-500/30",
    critical: "bg-red-500/10 border-red-500/30",
  };
  return m[r] ?? "bg-slate-700/30 border-slate-700";
}

function severityColor(s: string) {
  const m: Record<string, string> = {
    nominal:  "text-emerald-400",
    degraded: "text-amber-400",
    impaired: "text-orange-400",
    critical: "text-red-400",
  };
  return m[s] ?? "text-slate-400";
}

function patternColor(p: string) {
  const m: Record<string, string> = {
    none:                   "text-slate-400",
    performance_degradation: "text-amber-400",
    capacity_breach:        "text-orange-400",
    security_incident:      "text-red-400",
    integration_failure:    "text-violet-400",
    service_outage:         "text-rose-400",
  };
  return m[p] ?? "text-slate-400";
}

function compositeColor(v: number) {
  if (v >= 60) return "#f87171";
  if (v >= 40) return "#fb923c";
  if (v >= 20) return "#fbbf24";
  return "#34d399";
}

function scoreBarColor(v: number) {
  if (v >= 60) return "bg-red-500";
  if (v >= 40) return "bg-orange-500";
  if (v >= 20) return "bg-amber-500";
  return "bg-emerald-500";
}

function pct(v: number) {
  return `${Math.round(v * 100)}%`;
}

function fmtScore(v: number) {
  return Math.round(v);
}

// ── CompositeRing ──────────────────────────────────────────────────────────────

function CompositeRing({ value, size = 72 }: { value: number; size?: number }) {
  const cx = size / 2, cy = size / 2, r = (size - 10) / 2;
  const circ = 2 * Math.PI * r;
  const arc  = (value / 100) * circ;
  const color = compositeColor(value);
  return (
    <svg width={size} height={size} className="flex-shrink-0">
      <circle cx={cx} cy={cy} r={r} fill="none" stroke="#1e293b" strokeWidth={8} />
      <circle
        cx={cx} cy={cy} r={r}
        fill="none" stroke={color} strokeWidth={8}
        strokeDasharray={`${arc} ${circ - arc}`}
        strokeLinecap="round"
        transform={`rotate(-90 ${cx} ${cy})`}
      />
      <text x={cx} y={cy + 1} textAnchor="middle" dominantBaseline="middle"
        fill={color} fontSize={size < 60 ? 10 : 13} fontWeight="bold">
        {Math.round(value)}
      </text>
    </svg>
  );
}

// ── MiniBar ───────────────────────────────────────────────────────────────────

function MiniBar({ value, color }: { value: number; color: string }) {
  return (
    <div className="w-full bg-slate-700/50 rounded-full h-1.5 mt-1">
      <div className={`${color} h-1.5 rounded-full`} style={{ width: `${Math.min(100, value)}%` }} />
    </div>
  );
}

// ── RiskDistBar ───────────────────────────────────────────────────────────────

const RISK_ORDER  = ["critical", "high", "moderate", "low"];
const RISK_COLORS: Record<string, string> = {
  critical: "bg-red-500",
  high:     "bg-orange-500",
  moderate: "bg-amber-500",
  low:      "bg-emerald-500",
};

function RiskDistBar({ counts, total }: { counts: Record<string, number>; total: number }) {
  if (total === 0) return null;
  return (
    <div className="space-y-2">
      <div className="flex h-3 rounded-full overflow-hidden gap-0.5">
        {RISK_ORDER.map((o) => {
          const n = counts[o] ?? 0;
          if (!n) return null;
          const p = (n / total) * 100;
          return <div key={o} className={`${RISK_COLORS[o]} h-full`} style={{ width: `${p}%` }} />;
        })}
      </div>
      <div className="flex flex-wrap gap-3">
        {RISK_ORDER.map((o) => {
          const n = counts[o] ?? 0;
          if (!n) return null;
          return (
            <span key={o} className="flex items-center gap-1.5 text-xs text-slate-400">
              <span className={`w-2 h-2 rounded-full ${RISK_COLORS[o]}`} />
              {o} ({n})
            </span>
          );
        })}
      </div>
    </div>
  );
}

// ── SystemCard ────────────────────────────────────────────────────────────────

function SystemCard({ system, onClick }: { system: SystemItem; onClick: () => void }) {
  return (
    <div
      onClick={onClick}
      className={`rounded-xl border p-4 cursor-pointer hover:brightness-110 transition-all ${riskBg(system.system_risk)}`}
    >
      <div className="flex items-start gap-3">
        <CompositeRing value={system.system_composite} />
        <div className="flex-1 min-w-0">
          <div className="flex items-start justify-between gap-2">
            <div className="min-w-0">
              <p className="text-sm font-semibold text-white leading-tight truncate">
                {system.system_id}
              </p>
              <p className="text-[10px] text-slate-500 mt-0.5">{system.environment} · {system.region}</p>
            </div>
            <div className="flex items-center gap-1 flex-shrink-0">
              {system.requires_immediate_action && (
                <span className="bg-red-500/20 text-red-400 text-[9px] font-bold px-1.5 py-0.5 rounded uppercase tracking-wide">
                  Immediate
                </span>
              )}
              {system.has_system_alert && !system.requires_immediate_action && (
                <span className="bg-rose-500/20 text-rose-400 text-[9px] font-bold px-1.5 py-0.5 rounded uppercase tracking-wide">
                  Alert
                </span>
              )}
            </div>
          </div>

          <div className="flex items-center gap-2 mt-1.5 flex-wrap">
            <span className={`text-xs font-semibold ${riskColor(system.system_risk)}`}>
              {system.system_risk}
            </span>
            <span className="text-slate-600">·</span>
            <span className={`text-xs ${severityColor(system.system_severity)}`}>
              {system.system_severity}
            </span>
            <span className="text-slate-600">·</span>
            <span className={`text-xs ${patternColor(system.system_pattern)}`}>
              {system.system_pattern === "none" ? "no pattern" : system.system_pattern.replace(/_/g, " ")}
            </span>
          </div>

          <div className="grid grid-cols-2 gap-x-4 mt-2">
            <div>
              <p className="text-[10px] text-slate-500">CPU</p>
              <p className={`text-xs font-medium ${system.cpu_utilization_pct >= 0.90 ? "text-red-400" : system.cpu_utilization_pct >= 0.75 ? "text-amber-400" : "text-slate-300"}`}>
                {pct(system.cpu_utilization_pct)}
              </p>
            </div>
            <div>
              <p className="text-[10px] text-slate-500">Uptime</p>
              <p className={`text-xs font-medium ${system.uptime_pct <= 0.95 ? "text-red-400" : system.uptime_pct <= 0.98 ? "text-amber-400" : "text-emerald-400"}`}>
                {(system.uptime_pct * 100).toFixed(1)}%
              </p>
            </div>
          </div>

          <div className="mt-2 space-y-1">
            <div>
              <p className="text-[10px] text-slate-500">Performance</p>
              <MiniBar value={system.performance_score} color={scoreBarColor(system.performance_score)} />
            </div>
            <div>
              <p className="text-[10px] text-slate-500">Security</p>
              <MiniBar value={system.security_score} color={scoreBarColor(system.security_score)} />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

// ── SystemModal ───────────────────────────────────────────────────────────────

function SystemModal({ system, onClose }: { system: SystemItem; onClose: () => void }) {
  const [tab, setTab] = useState<"health" | "capacity" | "security" | "action">("health");

  useEffect(() => {
    const handler = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [onClose]);

  const tabs = [
    { id: "health"   as const, label: "Health" },
    { id: "capacity" as const, label: "Capacity" },
    { id: "security" as const, label: "Security" },
    { id: "action"   as const, label: "Action" },
  ];

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm"
      onClick={onClose}>
      <div className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-lg max-h-[90vh] overflow-y-auto shadow-2xl"
        onClick={(e) => e.stopPropagation()}>
        {/* Header */}
        <div className="flex items-start justify-between p-5 border-b border-slate-800">
          <div className="flex items-center gap-4">
            <CompositeRing value={system.system_composite} size={64} />
            <div>
              <p className="text-xs text-slate-400 mb-0.5">{system.environment} · {system.region}</p>
              <h2 className="text-base font-bold text-white leading-tight">{system.system_id}</h2>
              <div className="flex items-center gap-2 mt-1 flex-wrap">
                <span className={`text-xs font-semibold ${riskColor(system.system_risk)}`}>
                  {system.system_risk}
                </span>
                <span className="text-slate-600">·</span>
                <span className={`text-xs ${severityColor(system.system_severity)}`}>
                  {system.system_severity}
                </span>
                <span className="text-slate-600">·</span>
                <span className={`text-xs ${patternColor(system.system_pattern)}`}>
                  {system.system_pattern === "none" ? "no pattern" : system.system_pattern.replace(/_/g, " ")}
                </span>
              </div>
            </div>
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-white text-xl leading-none p-1">×</button>
        </div>

        {/* Action banner */}
        <div className="px-5 pt-4">
          <div className="flex items-center gap-2 rounded-lg bg-red-500/10 border border-red-500/25 p-3">
            <span className="text-red-400 text-xs">⚡ Recommended Action:</span>
            <span className="text-white text-xs font-semibold capitalize">
              {system.recommended_action.replace(/_/g, " ")}
            </span>
          </div>
        </div>

        {/* Signal */}
        <div className="px-5 pt-3">
          <p className="text-[10px] text-slate-500 leading-relaxed italic">{system.system_signal}</p>
        </div>

        {/* Tabs */}
        <div className="flex gap-1 px-5 mt-4">
          {tabs.map((t) => (
            <button key={t.id} onClick={() => setTab(t.id)}
              className={`text-xs font-medium px-3 py-1.5 rounded-md transition-colors ${
                tab === t.id
                  ? "bg-red-700 text-white"
                  : "text-slate-400 hover:text-white hover:bg-slate-800"
              }`}>
              {t.label}
            </button>
          ))}
        </div>

        <div className="p-5 space-y-4">
          {/* Health tab */}
          {tab === "health" && (
            <>
              <div className="grid grid-cols-2 gap-3">
                {[
                  { label: "Performance", value: fmtScore(system.performance_score) },
                  { label: "Capacity",    value: fmtScore(system.capacity_score) },
                  { label: "Security",    value: fmtScore(system.security_score) },
                  { label: "Reliability", value: fmtScore(system.reliability_score) },
                ].map(({ label, value }) => (
                  <div key={label} className="bg-slate-800/60 rounded-lg p-3">
                    <p className="text-[10px] text-slate-500 mb-0.5">{label} Score</p>
                    <p className="text-lg font-bold text-white">{value}<span className="text-xs text-slate-500">/100</span></p>
                    <MiniBar value={value} color={scoreBarColor(value)} />
                  </div>
                ))}
              </div>
              <div className="bg-slate-800/40 rounded-lg p-3 space-y-2">
                <p className="text-xs font-medium text-slate-300 mb-1">System Vitals</p>
                <div className="flex justify-between items-center">
                  <span className="text-xs text-slate-400">Response Time</span>
                  <span className={`text-xs font-medium ${system.avg_response_time_ms >= 1000 ? "text-red-400" : system.avg_response_time_ms >= 500 ? "text-amber-400" : "text-emerald-400"}`}>
                    {system.avg_response_time_ms} ms
                  </span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-xs text-slate-400">Error Rate</span>
                  <span className={`text-xs font-medium ${system.error_rate_pct >= 0.05 ? "text-red-400" : system.error_rate_pct >= 0.02 ? "text-amber-400" : "text-emerald-400"}`}>
                    {(system.error_rate_pct * 100).toFixed(1)}%
                  </span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-xs text-slate-400">Network Latency</span>
                  <span className={`text-xs font-medium ${system.network_latency_ms >= 200 ? "text-amber-400" : "text-emerald-400"}`}>
                    {system.network_latency_ms} ms
                  </span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-xs text-slate-400">Uptime (30d)</span>
                  <span className={`text-xs font-medium ${system.uptime_pct <= 0.95 ? "text-red-400" : system.uptime_pct <= 0.98 ? "text-amber-400" : "text-emerald-400"}`}>
                    {(system.uptime_pct * 100).toFixed(2)}%
                  </span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-xs text-slate-400">Incidents (30d)</span>
                  <span className={`text-xs font-medium ${system.incident_count_30d >= 5 ? "text-red-400" : system.incident_count_30d >= 2 ? "text-amber-400" : "text-emerald-400"}`}>
                    {system.incident_count_30d}
                  </span>
                </div>
              </div>
            </>
          )}

          {/* Capacity tab */}
          {tab === "capacity" && (
            <>
              <div className="grid grid-cols-2 gap-3">
                {[
                  { label: "CPU",    value: system.cpu_utilization_pct },
                  { label: "Memory", value: system.memory_utilization_pct },
                  { label: "Disk",   value: system.disk_utilization_pct },
                  { label: "SLA",    value: system.sla_compliance_pct },
                ].map(({ label, value }) => (
                  <div key={label} className="bg-slate-800/60 rounded-lg p-3">
                    <p className="text-[10px] text-slate-500 mb-0.5">{label}</p>
                    <p className={`text-base font-bold ${value >= 0.90 ? "text-red-400" : value >= 0.75 ? "text-amber-400" : "text-white"}`}>
                      {pct(value)}
                    </p>
                  </div>
                ))}
              </div>
              <div className="bg-slate-800/40 rounded-lg p-3 space-y-2">
                <p className="text-xs font-medium text-slate-300 mb-1">Pipeline & Deployment</p>
                <div className="flex justify-between items-center">
                  <span className="text-xs text-slate-400">Data Pipeline Lag</span>
                  <span className={`text-xs font-medium ${system.data_pipeline_lag_minutes >= 30 ? "text-red-400" : system.data_pipeline_lag_minutes >= 10 ? "text-amber-400" : "text-emerald-400"}`}>
                    {system.data_pipeline_lag_minutes} min
                  </span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-xs text-slate-400">Deploy Frequency</span>
                  <span className="text-xs font-medium text-slate-300">{system.deployment_frequency_per_week}/wk</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-xs text-slate-400">Change Failure Rate</span>
                  <span className={`text-xs font-medium ${system.change_failure_rate_pct >= 0.15 ? "text-red-400" : system.change_failure_rate_pct >= 0.08 ? "text-amber-400" : "text-emerald-400"}`}>
                    {(system.change_failure_rate_pct * 100).toFixed(0)}%
                  </span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-xs text-slate-400">Backup Success</span>
                  <span className={`text-xs font-medium ${system.backup_success_rate_pct <= 0.80 ? "text-red-400" : system.backup_success_rate_pct <= 0.92 ? "text-amber-400" : "text-emerald-400"}`}>
                    {pct(system.backup_success_rate_pct)}
                  </span>
                </div>
              </div>
            </>
          )}

          {/* Security tab */}
          {tab === "security" && (
            <>
              <div className="grid grid-cols-2 gap-3">
                {[
                  { label: "Vulnerabilities", value: String(system.security_vulnerability_count), warn: system.security_vulnerability_count >= 5 ? "text-red-400" : system.security_vulnerability_count >= 1 ? "text-amber-400" : "text-emerald-400" },
                  { label: "Failed Scans",    value: String(system.failed_security_scans), warn: system.failed_security_scans >= 3 ? "text-red-400" : system.failed_security_scans >= 1 ? "text-amber-400" : "text-emerald-400" },
                  { label: "Patch Compliance", value: pct(system.patch_compliance_pct), warn: system.patch_compliance_pct <= 0.60 ? "text-red-400" : system.patch_compliance_pct <= 0.80 ? "text-amber-400" : "text-emerald-400" },
                  { label: "Integration Fail",  value: pct(system.integration_failure_rate_pct), warn: system.integration_failure_rate_pct >= 0.10 ? "text-red-400" : system.integration_failure_rate_pct >= 0.05 ? "text-amber-400" : "text-emerald-400" },
                ].map(({ label, value, warn }) => (
                  <div key={label} className="bg-slate-800/60 rounded-lg p-3">
                    <p className="text-[10px] text-slate-500 mb-0.5">{label}</p>
                    <p className={`text-base font-bold ${warn}`}>{value}</p>
                  </div>
                ))}
              </div>
              <div className="bg-slate-800/40 rounded-lg p-3 space-y-2">
                <p className="text-xs font-medium text-slate-300 mb-1">API Health</p>
                <div className="flex justify-between items-center">
                  <span className="text-xs text-slate-400">API Error Rate</span>
                  <span className={`text-xs font-medium ${system.api_error_rate_pct >= 0.10 ? "text-red-400" : system.api_error_rate_pct >= 0.05 ? "text-amber-400" : "text-emerald-400"}`}>
                    {(system.api_error_rate_pct * 100).toFixed(1)}%
                  </span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-xs text-slate-400">MTTR</span>
                  <span className={`text-xs font-medium ${system.mean_time_to_recovery_hours >= 4 ? "text-red-400" : system.mean_time_to_recovery_hours >= 2 ? "text-amber-400" : "text-emerald-400"}`}>
                    {system.mean_time_to_recovery_hours} hrs
                  </span>
                </div>
              </div>
            </>
          )}

          {/* Action tab */}
          {tab === "action" && (
            <div className="space-y-3">
              <div className="grid grid-cols-2 gap-3">
                {[
                  { label: "Risk Level",       value: system.system_risk,      color: riskColor(system.system_risk) },
                  { label: "Severity",         value: system.system_severity,  color: severityColor(system.system_severity) },
                ].map(({ label, value, color }) => (
                  <div key={label} className="bg-slate-800/60 rounded-lg p-3">
                    <p className="text-[10px] text-slate-500 mb-0.5">{label}</p>
                    <p className={`text-sm font-bold capitalize ${color}`}>{value}</p>
                  </div>
                ))}
              </div>
              <div className="bg-slate-800/40 rounded-lg p-3 space-y-2">
                <p className="text-xs font-medium text-slate-300 mb-1">Risk Summary</p>
                <div className="flex justify-between items-center">
                  <span className="text-xs text-slate-400">Composite Score</span>
                  <span className={`text-xs font-bold ${riskColor(system.system_risk)}`}>
                    {system.system_composite} / 100
                  </span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-xs text-slate-400">Downtime Risk</span>
                  <span className={`text-xs font-medium ${system.estimated_downtime_risk_hours >= 2 ? "text-red-400" : system.estimated_downtime_risk_hours >= 0.5 ? "text-amber-400" : "text-emerald-400"}`}>
                    {system.estimated_downtime_risk_hours} hrs
                  </span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-xs text-slate-400">Has Alert</span>
                  <span className={`text-xs font-medium ${system.has_system_alert ? "text-red-400" : "text-emerald-400"}`}>
                    {system.has_system_alert ? "Yes" : "No"}
                  </span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-xs text-slate-400">Immediate Action</span>
                  <span className={`text-xs font-medium ${system.requires_immediate_action ? "text-red-400" : "text-emerald-400"}`}>
                    {system.requires_immediate_action ? "Required" : "Not required"}
                  </span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-xs text-slate-400">Pattern</span>
                  <span className={`text-xs font-medium capitalize ${patternColor(system.system_pattern)}`}>
                    {system.system_pattern === "none" ? "none" : system.system_pattern.replace(/_/g, " ")}
                  </span>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

// ── KPICard ───────────────────────────────────────────────────────────────────

function KPICard({ label, value, sub, accent }: {
  label: string; value: string | number; sub?: string; accent?: string;
}) {
  return (
    <div className="bg-slate-800/60 border border-slate-700/50 rounded-xl p-4">
      <p className="text-xs text-slate-400 mb-1">{label}</p>
      <p className={`text-2xl font-bold ${accent ?? "text-white"}`}>{value}</p>
      {sub && <p className="text-[11px] text-slate-500 mt-0.5">{sub}</p>}
    </div>
  );
}

// ── Filter constants ──────────────────────────────────────────────────────────

const RISK_FILTERS    = ["all", "low", "moderate", "high", "critical"];
const PATTERN_FILTERS = [
  "all", "none", "performance_degradation", "capacity_breach",
  "security_incident", "integration_failure", "service_outage",
];

// ── Page ──────────────────────────────────────────────────────────────────────

export default function ITSystemsHealthMonitoringPage() {
  const [systems, setSystems]     = useState<SystemItem[]>([]);
  const [summary, setSummary]     = useState<Summary | null>(null);
  const [loading, setLoading]     = useState(true);
  const [riskFilter, setRisk]     = useState("all");
  const [patternFilter, setPattern] = useState("all");
  const [selected, setSelected]   = useState<SystemItem | null>(null);

  const fetchData = useCallback(async () => {
    setLoading(true);
    try {
      const params = new URLSearchParams();
      if (riskFilter !== "all")    params.set("risk", riskFilter);
      if (patternFilter !== "all") params.set("pattern", patternFilter);
      const qs = params.toString();
      const res = await fetch(
        `/api/it-systems-health-monitoring-engine${qs ? `?${qs}` : ""}`,
        { cache: "no-store" },
      );
      const data = await res.json();
      setSystems(data.systems ?? []);
      setSummary(data.summary ?? null);
    } finally {
      setLoading(false);
    }
  }, [riskFilter, patternFilter]);

  useEffect(() => { fetchData(); }, [fetchData]);

  return (
    <div className="min-h-screen bg-slate-950 p-4 md:p-6 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-xl font-bold text-white">IT Systems Health Monitoring Engine</h1>
          <p className="text-sm text-slate-400 mt-0.5">
            Performance · capacity · security · reliability — composite health index
          </p>
        </div>
        <button
          onClick={fetchData}
          className="text-xs text-red-400 hover:text-red-300 border border-red-700/40 hover:border-red-600/60 px-3 py-1.5 rounded-lg transition-colors"
        >
          Refresh
        </button>
      </div>

      {/* KPI strip */}
      {summary && (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
          <KPICard label="Total Systems"     value={summary.total}                   sub="monitored" />
          <KPICard label="Avg Composite"     value={`${summary.avg_system_composite}`} sub="/100" accent="text-red-400" />
          <KPICard label="System Alerts"     value={summary.system_alert_count}       sub="need attention" accent="text-rose-400" />
          <KPICard label="Immediate Action"  value={summary.immediate_action_count}   sub="critical now" accent="text-red-400" />
        </div>
      )}

      {/* Risk distribution */}
      {summary && (
        <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-4">
          <div className="flex items-center justify-between mb-3">
            <p className="text-sm font-semibold text-slate-300">Risk Distribution</p>
            <div className="flex items-center gap-4 text-xs text-slate-500">
              <span>
                Avg downtime risk:{" "}
                <span className={`font-medium ${summary.avg_estimated_downtime_risk_hours >= 1 ? "text-red-400" : "text-white"}`}>
                  {summary.avg_estimated_downtime_risk_hours} hrs
                </span>
              </span>
              <span>
                Avg composite:{" "}
                <span className="font-medium text-white">{summary.avg_system_composite}</span>
              </span>
            </div>
          </div>
          <RiskDistBar counts={summary.risk_counts} total={summary.total} />
        </div>
      )}

      {/* Sub-score strip */}
      {summary && (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
          <KPICard label="Avg Performance" value={`${summary.avg_performance_score}`} sub="/100" accent="text-amber-400" />
          <KPICard label="Avg Capacity"    value={`${summary.avg_capacity_score}`}    sub="/100" accent="text-orange-400" />
          <KPICard label="Avg Security"    value={`${summary.avg_security_score}`}    sub="/100" accent="text-red-400" />
          <KPICard label="Avg Reliability" value={`${summary.avg_reliability_score}`} sub="/100" accent="text-rose-400" />
        </div>
      )}

      {/* Risk filter */}
      <div className="flex flex-col gap-2">
        <div className="flex flex-wrap gap-2">
          {RISK_FILTERS.map((f) => (
            <button key={f} onClick={() => setRisk(f)}
              className={`text-xs px-3 py-1.5 rounded-lg font-medium transition-colors ${
                riskFilter === f
                  ? "bg-red-700 text-white"
                  : "bg-slate-800 text-slate-400 hover:text-white hover:bg-slate-700"
              }`}>
              {f === "all" ? "All Risks" : f}
            </button>
          ))}
        </div>
        <div className="flex flex-wrap gap-2">
          {PATTERN_FILTERS.map((f) => (
            <button key={f} onClick={() => setPattern(f)}
              className={`text-xs px-3 py-1.5 rounded-lg font-medium transition-colors ${
                patternFilter === f
                  ? "bg-rose-700 text-white"
                  : "bg-slate-800 text-slate-400 hover:text-white hover:bg-slate-700"
              }`}>
              {f === "all" ? "All Patterns" : f === "none" ? "no pattern" : f.replace(/_/g, " ")}
            </button>
          ))}
        </div>
      </div>

      {/* Cards */}
      {loading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {[...Array(6)].map((_, i) => (
            <div key={i} className="rounded-xl border border-slate-800 bg-slate-800/30 h-44 animate-pulse" />
          ))}
        </div>
      ) : systems.length === 0 ? (
        <div className="text-center py-16 text-slate-500">No systems match the selected filters.</div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {systems.map((s) => (
            <SystemCard key={s.system_id} system={s} onClick={() => setSelected(s)} />
          ))}
        </div>
      )}

      {/* Modal */}
      {selected && <SystemModal system={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
