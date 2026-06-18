"use client";

import { useEffect, useState, useCallback } from "react";

interface UserRecord {
  user_id: string;
  user_name: string;
  role: string;
  region: string;
  anomaly_level: string;
  anomaly_risk: string;
  primary_anomaly_type: string;
  recommended_action: string;
  access_volume_score: number;
  behavioral_deviation_score: number;
  data_sensitivity_score: number;
  authentication_risk_score: number;
  anomaly_composite: number;
  is_active_threat: boolean;
  requires_immediate_action: boolean;
  estimated_data_exposure_mb: number;
  anomaly_signal: string;
  download_volume_mb: number;
}

interface Summary {
  total: number;
  level_counts: Record<string, number>;
  risk_counts: Record<string, number>;
  type_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_anomaly_composite: number;
  active_threat_count: number;
  immediate_action_count: number;
  avg_access_volume_score: number;
  avg_behavioral_deviation_score: number;
  avg_data_sensitivity_score: number;
  avg_authentication_risk_score: number;
  total_data_exposure_mb: number;
}

const LEVEL_ORDER = ["none", "low", "elevated", "high", "critical"];
const LEVEL_COLORS: Record<string, string> = {
  none:     "bg-slate-600 text-slate-200",
  low:      "bg-emerald-900 text-emerald-300",
  elevated: "bg-amber-900 text-amber-300",
  high:     "bg-orange-900 text-orange-300",
  critical: "bg-red-900 text-red-300",
};
const LEVEL_RING: Record<string, string> = {
  none:     "#475569",
  low:      "#10b981",
  elevated: "#f59e0b",
  high:     "#f97316",
  critical: "#ef4444",
};
const RISK_COLORS: Record<string, string> = {
  low:      "bg-emerald-900 text-emerald-300",
  moderate: "bg-amber-900 text-amber-300",
  high:     "bg-orange-900 text-orange-300",
  critical: "bg-red-900 text-red-300",
};
const TYPE_LABELS: Record<string, string> = {
  none:               "None",
  bulk_export:        "Bulk Export",
  off_hours:          "Off-Hours",
  credential_sharing: "Credential Sharing",
  data_exfiltration:  "Data Exfiltration",
  privilege_abuse:    "Privilege Abuse",
};
const ACTION_LABELS: Record<string, string> = {
  no_action:          "No Action",
  log_alert:          "Log & Alert",
  security_review:    "Security Review",
  account_suspend:    "Suspend Account",
  immediate_lockdown: "Immediate Lockdown",
};

function compositeColor(v: number) {
  if (v < 20) return "#10b981";
  if (v < 40) return "#f59e0b";
  if (v < 60) return "#f97316";
  return "#ef4444";
}

function ScoreBar({ label, value, color }: { label: string; value: number; color: string }) {
  return (
    <div>
      <div className="flex justify-between text-xs text-slate-400 mb-1">
        <span>{label}</span>
        <span className="text-slate-200">{value.toFixed(0)}</span>
      </div>
      <div className="h-1.5 bg-slate-700 rounded-full overflow-hidden">
        <div className="h-full rounded-full transition-all" style={{ width: `${Math.min(value, 100)}%`, backgroundColor: color }} />
      </div>
    </div>
  );
}

function CompositeRing({ value, level }: { value: number; level: string }) {
  const r = 28; const circ = 2 * Math.PI * r;
  const fill = (Math.min(value, 100) / 100) * circ;
  const color = LEVEL_RING[level] ?? "#475569";
  return (
    <svg width="72" height="72" viewBox="0 0 72 72">
      <circle cx="36" cy="36" r={r} fill="none" stroke="#1e293b" strokeWidth="7" />
      <circle cx="36" cy="36" r={r} fill="none" stroke={color} strokeWidth="7"
        strokeDasharray={`${fill} ${circ}`} strokeLinecap="round"
        transform="rotate(-90 36 36)" />
      <text x="36" y="40" textAnchor="middle" fill={color} fontSize="13" fontWeight="bold">{value.toFixed(0)}</text>
    </svg>
  );
}

function DetailModal({ user, onClose }: { user: UserRecord; onClose: () => void }) {
  const [tab, setTab] = useState(0);

  useEffect(() => {
    const fn = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", fn);
    return () => window.removeEventListener("keydown", fn);
  }, [onClose]);

  const tabs = ["Overview", "Risk Scores", "Security Action"];
  const levelColor = LEVEL_COLORS[user.anomaly_level] ?? "bg-slate-700 text-slate-300";
  const riskColor  = RISK_COLORS[user.anomaly_risk]   ?? "bg-slate-700 text-slate-300";

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4" onClick={onClose}>
      <div className="absolute inset-0 bg-black/70" />
      <div className="relative bg-slate-900 border border-slate-700 rounded-2xl shadow-2xl w-full max-w-lg" onClick={(e) => e.stopPropagation()}>
        <div className="flex items-start justify-between p-6 border-b border-slate-800">
          <div>
            <h2 className="text-lg font-semibold text-slate-100">{user.user_name}</h2>
            <p className="text-sm text-slate-400">{user.role} · {user.region}</p>
            <div className="flex gap-2 mt-2 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${levelColor}`}>{user.anomaly_level}</span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${riskColor}`}>{user.anomaly_risk} risk</span>
              {user.is_active_threat && (
                <span className="px-2 py-0.5 rounded text-xs font-medium bg-red-900 text-red-300">⚠ Active Threat</span>
              )}
              {user.requires_immediate_action && (
                <span className="px-2 py-0.5 rounded text-xs font-medium bg-red-800 text-red-200">🔒 Lockdown Required</span>
              )}
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
                <CompositeRing value={user.anomaly_composite} level={user.anomaly_level} />
                <div>
                  <p className="text-xs text-slate-400">Anomaly Composite</p>
                  <p className="text-2xl font-bold text-slate-100">{user.anomaly_composite.toFixed(1)}</p>
                  <p className="text-xs text-slate-400 mt-1">{user.estimated_data_exposure_mb.toFixed(1)} MB exposure est.</p>
                </div>
              </div>
              <div className="p-4 bg-slate-800 rounded-xl">
                <p className="text-xs text-slate-400 mb-1">Anomaly Signal</p>
                <p className="text-sm text-slate-200">{user.anomaly_signal}</p>
              </div>
              <div className="grid grid-cols-2 gap-3 text-sm">
                <div className="p-3 bg-slate-800 rounded-lg">
                  <p className="text-xs text-slate-400">Type</p>
                  <p className="text-slate-200 font-medium">{TYPE_LABELS[user.primary_anomaly_type] ?? user.primary_anomaly_type}</p>
                </div>
                <div className="p-3 bg-slate-800 rounded-lg">
                  <p className="text-xs text-slate-400">Download Vol.</p>
                  <p className="text-slate-200 font-medium">{user.download_volume_mb.toFixed(1)} MB</p>
                </div>
              </div>
            </div>
          )}

          {tab === 1 && (
            <div className="space-y-4">
              <ScoreBar label="Access Volume" value={user.access_volume_score} color={compositeColor(user.access_volume_score)} />
              <ScoreBar label="Behavioral Deviation" value={user.behavioral_deviation_score} color={compositeColor(user.behavioral_deviation_score)} />
              <ScoreBar label="Data Sensitivity" value={user.data_sensitivity_score} color={compositeColor(user.data_sensitivity_score)} />
              <ScoreBar label="Authentication Risk" value={user.authentication_risk_score} color={compositeColor(user.authentication_risk_score)} />
              <div className="mt-4 p-3 bg-slate-800 rounded-lg text-xs text-slate-400">
                Composite = Access×0.30 + Behavioral×0.25 + Sensitivity×0.25 + Auth×0.20
              </div>
            </div>
          )}

          {tab === 2 && (
            <div className="space-y-4">
              <div className="p-4 bg-slate-800 rounded-xl">
                <p className="text-xs text-slate-400 mb-1">Recommended Action</p>
                <p className="text-lg font-semibold text-indigo-300">{ACTION_LABELS[user.recommended_action] ?? user.recommended_action}</p>
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div className={`p-3 rounded-lg ${user.is_active_threat ? "bg-red-900/50 border border-red-700" : "bg-slate-800"}`}>
                  <p className="text-xs text-slate-400">Active Threat</p>
                  <p className={`font-semibold ${user.is_active_threat ? "text-red-300" : "text-emerald-400"}`}>
                    {user.is_active_threat ? "YES" : "No"}
                  </p>
                </div>
                <div className={`p-3 rounded-lg ${user.requires_immediate_action ? "bg-red-900/50 border border-red-700" : "bg-slate-800"}`}>
                  <p className="text-xs text-slate-400">Immediate Action</p>
                  <p className={`font-semibold ${user.requires_immediate_action ? "text-red-300" : "text-emerald-400"}`}>
                    {user.requires_immediate_action ? "REQUIRED" : "No"}
                  </p>
                </div>
              </div>
              <div className="p-3 bg-slate-800 rounded-lg">
                <p className="text-xs text-slate-400">Estimated Data Exposure</p>
                <p className="text-slate-200 font-medium">{user.estimated_data_exposure_mb.toFixed(1)} MB</p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default function SalesDataAccessAnomalyEnginePage() {
  const [data, setData]       = useState<{ users: UserRecord[]; summary: Summary } | null>(null);
  const [filter, setFilter]   = useState("all");
  const [selected, setSelected] = useState<UserRecord | null>(null);

  const load = useCallback((level?: string) => {
    const params = level && level !== "all" ? `?level=${level}` : "";
    fetch(`/api/sales-data-access-anomaly-engine${params}`)
      .then((r) => r.json())
      .then(setData);
  }, []);

  useEffect(() => { load(); }, [load]);

  const handleFilter = (f: string) => {
    setFilter(f);
    load(f === "all" ? undefined : f);
  };

  if (!data) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-slate-400 animate-pulse">Loading data access anomaly engine...</div>
    </div>
  );

  const { users, summary } = data;
  const levelTotal = Object.values(summary.level_counts).reduce((a, b) => a + b, 0) || 1;
  const typeTotal  = Object.values(summary.type_counts).reduce((a, b) => a + b, 0) || 1;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
      {selected && <DetailModal user={selected} onClose={() => setSelected(null)} />}

      <div className="mb-6">
        <h1 className="text-2xl font-bold text-slate-100">Sales Data Access Anomaly Engine</h1>
        <p className="text-slate-400 text-sm mt-1">CRM access pattern analysis · insider threat detection · data exfiltration prevention</p>
      </div>

      {/* KPI Strip */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        {[
          { label: "Total Users", value: summary.total, sub: "monitored" },
          { label: "Active Threats", value: summary.active_threat_count, sub: "flagged now", alert: summary.active_threat_count > 0 },
          { label: "Immediate Action", value: summary.immediate_action_count, sub: "require lockdown", alert: summary.immediate_action_count > 0 },
          { label: "Data Exposure", value: `${(summary.total_data_exposure_mb / 1024).toFixed(1)} GB`, sub: "estimated at risk" },
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
          <h2 className="text-sm font-semibold text-slate-300 mb-4">Avg Risk Scores</h2>
          <div className="space-y-3">
            {[
              { label: "Access Volume",        value: summary.avg_access_volume_score },
              { label: "Behavioral Deviation", value: summary.avg_behavioral_deviation_score },
              { label: "Data Sensitivity",     value: summary.avg_data_sensitivity_score },
              { label: "Authentication Risk",  value: summary.avg_authentication_risk_score },
            ].map(({ label, value }) => (
              <div key={label}>
                <div className="flex justify-between text-xs text-slate-400 mb-1">
                  <span>{label}</span>
                  <span className="text-slate-200">{value.toFixed(1)}</span>
                </div>
                <div className="h-2 bg-slate-700 rounded-full overflow-hidden">
                  <div className="h-full rounded-full" style={{ width: `${Math.min(value, 100)}%`, backgroundColor: compositeColor(value) }} />
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-4">
          <div>
            <h2 className="text-sm font-semibold text-slate-300 mb-3">Anomaly Level Distribution</h2>
            <div className="space-y-2">
              {LEVEL_ORDER.map((lv) => {
                const cnt = summary.level_counts[lv] ?? 0;
                const pct = (cnt / levelTotal) * 100;
                return (
                  <div key={lv} className="flex items-center gap-2 text-xs">
                    <span className="w-20 text-slate-400 capitalize">{lv}</span>
                    <div className="flex-1 h-2 bg-slate-700 rounded-full overflow-hidden">
                      <div className="h-full rounded-full" style={{ width: `${pct}%`, backgroundColor: LEVEL_RING[lv] }} />
                    </div>
                    <span className="w-5 text-right text-slate-300">{cnt}</span>
                  </div>
                );
              })}
            </div>
          </div>
          <div>
            <h2 className="text-sm font-semibold text-slate-300 mb-3">Anomaly Type Distribution</h2>
            <div className="space-y-1.5">
              {Object.entries(summary.type_counts).map(([type, cnt]) => (
                <div key={type} className="flex items-center gap-2 text-xs">
                  <span className="w-32 text-slate-400">{TYPE_LABELS[type] ?? type}</span>
                  <div className="flex-1 h-1.5 bg-slate-700 rounded-full overflow-hidden">
                    <div className="h-full rounded-full bg-indigo-500" style={{ width: `${(cnt / typeTotal) * 100}%` }} />
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
        {["all", ...LEVEL_ORDER].map((lv) => (
          <button key={lv} onClick={() => handleFilter(lv)}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
              filter === lv ? "bg-indigo-600 text-white" : "bg-slate-800 text-slate-400 hover:text-slate-200"
            }`}>
            {lv === "all" ? "All Users" : lv.charAt(0).toUpperCase() + lv.slice(1)}
            {lv !== "all" && (summary.level_counts[lv] ?? 0) > 0 && (
              <span className="ml-1 text-slate-400">({summary.level_counts[lv]})</span>
            )}
          </button>
        ))}
      </div>

      {/* User Cards */}
      <div className="grid sm:grid-cols-2 xl:grid-cols-3 gap-4">
        {users.map((u) => {
          const levelCls = LEVEL_COLORS[u.anomaly_level] ?? "bg-slate-700 text-slate-300";
          const riskCls  = RISK_COLORS[u.anomaly_risk]   ?? "bg-slate-700 text-slate-300";
          return (
            <div key={u.user_id} onClick={() => setSelected(u)}
              className="bg-slate-900 border border-slate-800 rounded-xl p-4 cursor-pointer hover:border-slate-600 transition-colors">
              <div className="flex items-start justify-between mb-3">
                <div>
                  <p className="font-semibold text-slate-100">{u.user_name}</p>
                  <p className="text-xs text-slate-400">{u.role} · {u.region}</p>
                </div>
                <div className="flex flex-col gap-1 items-end">
                  <span className={`px-2 py-0.5 rounded text-xs font-medium ${levelCls}`}>{u.anomaly_level}</span>
                  <span className={`px-2 py-0.5 rounded text-xs font-medium ${riskCls}`}>{u.anomaly_risk}</span>
                </div>
              </div>

              <div className="flex items-center gap-3 mb-3">
                <CompositeRing value={u.anomaly_composite} level={u.anomaly_level} />
                <div className="flex-1 space-y-1.5">
                  <ScoreBar label="Access Vol." value={u.access_volume_score} color={compositeColor(u.access_volume_score)} />
                  <ScoreBar label="Behavioral"  value={u.behavioral_deviation_score} color={compositeColor(u.behavioral_deviation_score)} />
                  <ScoreBar label="Sensitivity" value={u.data_sensitivity_score} color={compositeColor(u.data_sensitivity_score)} />
                  <ScoreBar label="Auth Risk"   value={u.authentication_risk_score} color={compositeColor(u.authentication_risk_score)} />
                </div>
              </div>

              <div className="flex gap-2 flex-wrap mb-2">
                {u.is_active_threat && (
                  <span className="text-xs text-red-400 bg-red-900/40 px-2 py-0.5 rounded">⚠ Threat</span>
                )}
                {u.requires_immediate_action && (
                  <span className="text-xs text-red-300 bg-red-900/60 px-2 py-0.5 rounded">🔒 Action</span>
                )}
                <span className="text-xs text-slate-400 bg-slate-800 px-2 py-0.5 rounded">
                  {ACTION_LABELS[u.recommended_action] ?? u.recommended_action}
                </span>
              </div>

              <p className="text-xs text-slate-400 line-clamp-2">{u.anomaly_signal}</p>
            </div>
          );
        })}
      </div>
    </div>
  );
}
