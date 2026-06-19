"use client";

import { useEffect, useState, useCallback } from "react";

interface TicketRecord {
  ticket_id: string;
  agent_id: string;
  region: string;
  service_risk: string;
  service_pattern: string;
  service_severity: string;
  recommended_action: string;
  resolution_score: number;
  escalation_score: number;
  satisfaction_score: number;
  capacity_score: number;
  service_composite: number;
  has_service_gap: boolean;
  requires_management_action: boolean;
  estimated_churn_risk_pct: number;
  service_signal: string;
  first_contact_resolution_pct: number;
  customer_satisfaction_score: number;
  sla_breach_rate_pct: number;
  escalation_rate_pct: number;
  agent_utilization_pct: number;
}

interface Summary {
  total: number;
  risk_counts: Record<string, number>;
  pattern_counts: Record<string, number>;
  severity_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_service_composite: number;
  service_gap_count: number;
  management_action_count: number;
  avg_resolution_score: number;
  avg_escalation_score: number;
  avg_satisfaction_score: number;
  avg_capacity_score: number;
  avg_estimated_churn_risk_pct: number;
}

const RISK_ORDER = ["low", "moderate", "high", "critical"];
const PATTERN_ORDER = [
  "none",
  "resolution_failure",
  "escalation_cascade",
  "agent_burnout",
  "sla_breach",
  "satisfaction_collapse",
];

const RISK_COLORS: Record<string, string> = {
  low:      "bg-teal-900 text-teal-300",
  moderate: "bg-amber-900 text-amber-300",
  high:     "bg-orange-900 text-orange-300",
  critical: "bg-red-900 text-red-300",
};
const RISK_HEX: Record<string, string> = {
  low:      "#2dd4bf",
  moderate: "#f59e0b",
  high:     "#f97316",
  critical: "#ef4444",
};
const SEVERITY_COLORS: Record<string, string> = {
  excellent:  "bg-teal-900 text-teal-300",
  acceptable: "bg-sky-900 text-sky-300",
  degraded:   "bg-amber-900 text-amber-300",
  failing:    "bg-red-900 text-red-300",
};
const PATTERN_LABELS: Record<string, string> = {
  none:                  "None",
  resolution_failure:    "Resolution Failure",
  escalation_cascade:    "Escalation Cascade",
  agent_burnout:         "Agent Burnout",
  sla_breach:            "SLA Breach",
  satisfaction_collapse: "Satisfaction Collapse",
};
const ACTION_LABELS: Record<string, string> = {
  no_action:                 "No Action",
  quality_monitoring:        "Quality Monitoring",
  coaching_intervention:     "Coaching Intervention",
  team_rebalancing:          "Team Rebalancing",
  sla_recovery_plan:         "SLA Recovery Plan",
  escalation_process_review: "Escalation Process Review",
  agent_support_program:     "Agent Support Program",
  capacity_emergency:        "Capacity Emergency",
  executive_service_review:  "Executive Service Review",
};

function compositeColor(v: number) {
  if (v < 20) return "#2dd4bf";
  if (v < 40) return "#f59e0b";
  if (v < 60) return "#f97316";
  return "#ef4444";
}

function pct(v: number) {
  return `${(v * 100).toFixed(0)}%`;
}

function ScoreBar({ label, value, color }: { label: string; value: number; color: string }) {
  return (
    <div>
      <div className="flex justify-between text-xs text-slate-400 mb-1">
        <span>{label}</span>
        <span className="text-slate-200">{value.toFixed(0)}</span>
      </div>
      <div className="h-1.5 bg-slate-700 rounded-full overflow-hidden">
        <div
          className="h-full rounded-full"
          style={{ width: `${Math.min(value, 100)}%`, backgroundColor: color }}
        />
      </div>
    </div>
  );
}

function CompositeRing({ value, risk }: { value: number; risk: string }) {
  const r = 28;
  const circ = 2 * Math.PI * r;
  const fill = (Math.min(value, 100) / 100) * circ;
  const color = RISK_HEX[risk] ?? "#475569";
  return (
    <svg width="72" height="72" viewBox="0 0 72 72">
      <circle cx="36" cy="36" r={r} fill="none" stroke="#1e293b" strokeWidth="7" />
      <circle
        cx="36" cy="36" r={r} fill="none" stroke={color} strokeWidth="7"
        strokeDasharray={`${fill} ${circ}`} strokeLinecap="round"
        transform="rotate(-90 36 36)"
      />
      <text x="36" y="40" textAnchor="middle" fill={color} fontSize="13" fontWeight="bold">
        {value.toFixed(0)}
      </text>
    </svg>
  );
}

function DetailModal({ ticket, onClose }: { ticket: TicketRecord; onClose: () => void }) {
  const [tab, setTab] = useState(0);
  useEffect(() => {
    const fn = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", fn);
    return () => window.removeEventListener("keydown", fn);
  }, [onClose]);

  const tabs = ["Overview", "Sub-Scores", "Intervention"];
  const riskCls     = RISK_COLORS[ticket.service_risk]         ?? "bg-slate-700 text-slate-300";
  const severityCls = SEVERITY_COLORS[ticket.service_severity] ?? "bg-slate-700 text-slate-300";

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4" onClick={onClose}>
      <div className="absolute inset-0 bg-black/70 backdrop-blur-sm" />
      <div
        className="relative bg-slate-900 border border-slate-700 rounded-2xl shadow-2xl w-full max-w-lg"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="flex items-start justify-between p-6 border-b border-slate-800">
          <div>
            <h2 className="text-lg font-semibold text-slate-100">{ticket.ticket_id}</h2>
            <p className="text-sm text-slate-400">
              Agent {ticket.agent_id} &middot; {ticket.region}
            </p>
            <div className="flex gap-2 mt-2 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${riskCls}`}>
                {ticket.service_risk}
              </span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${severityCls}`}>
                {ticket.service_severity}
              </span>
              {ticket.has_service_gap && (
                <span className="px-2 py-0.5 rounded text-xs font-medium bg-amber-900 text-amber-300">
                  Service Gap
                </span>
              )}
              {ticket.requires_management_action && (
                <span className="px-2 py-0.5 rounded text-xs font-medium bg-red-900 text-red-300">
                  Mgmt Action
                </span>
              )}
            </div>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-slate-300 text-xl ml-4">
            ✕
          </button>
        </div>

        {/* Tabs */}
        <div className="flex border-b border-slate-800">
          {tabs.map((t, i) => (
            <button
              key={t}
              onClick={() => setTab(i)}
              className={`flex-1 py-3 text-sm font-medium transition-colors ${
                tab === i
                  ? "text-teal-400 border-b-2 border-teal-400"
                  : "text-slate-500 hover:text-slate-300"
              }`}
            >
              {t}
            </button>
          ))}
        </div>

        {/* Tab body */}
        <div className="p-6">
          {tab === 0 && (
            <div className="space-y-4">
              <div className="flex items-center gap-4 p-4 bg-slate-800 rounded-xl">
                <CompositeRing value={ticket.service_composite} risk={ticket.service_risk} />
                <div>
                  <p className="text-xs text-slate-400">Service Composite</p>
                  <p className="text-2xl font-bold text-slate-100">
                    {ticket.service_composite.toFixed(1)}
                  </p>
                  <p className="text-xs text-slate-400 mt-1">
                    Churn risk: {(ticket.estimated_churn_risk_pct * 100).toFixed(0)}%
                  </p>
                </div>
              </div>
              <div className="p-4 bg-slate-800 rounded-xl">
                <p className="text-xs text-slate-400 mb-1">Service Signal</p>
                <p className="text-sm text-slate-200">{ticket.service_signal}</p>
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div className="p-3 bg-slate-800 rounded-lg">
                  <p className="text-xs text-slate-400">Pattern</p>
                  <p className="text-slate-200 font-medium text-sm">
                    {PATTERN_LABELS[ticket.service_pattern] ?? ticket.service_pattern}
                  </p>
                </div>
                <div className="p-3 bg-slate-800 rounded-lg">
                  <p className="text-xs text-slate-400">FCR</p>
                  <p className="text-teal-300 font-medium">
                    {pct(ticket.first_contact_resolution_pct)}
                  </p>
                </div>
                <div className="p-3 bg-slate-800 rounded-lg">
                  <p className="text-xs text-slate-400">CSAT</p>
                  <p className="text-teal-300 font-medium">
                    {pct(ticket.customer_satisfaction_score)}
                  </p>
                </div>
                <div className="p-3 bg-slate-800 rounded-lg">
                  <p className="text-xs text-slate-400">SLA Breach</p>
                  <p className="text-orange-300 font-medium">
                    {pct(ticket.sla_breach_rate_pct)}
                  </p>
                </div>
              </div>
            </div>
          )}

          {tab === 1 && (
            <div className="space-y-4">
              <ScoreBar
                label="Resolution Risk"
                value={ticket.resolution_score}
                color={compositeColor(ticket.resolution_score)}
              />
              <ScoreBar
                label="Escalation Risk"
                value={ticket.escalation_score}
                color={compositeColor(ticket.escalation_score)}
              />
              <ScoreBar
                label="Satisfaction Risk"
                value={ticket.satisfaction_score}
                color={compositeColor(ticket.satisfaction_score)}
              />
              <ScoreBar
                label="Capacity Risk"
                value={ticket.capacity_score}
                color={compositeColor(ticket.capacity_score)}
              />
              <div className="mt-4 p-3 bg-slate-800 rounded-lg text-xs text-slate-400">
                Composite = Resolution×0.30 + Escalation×0.25 + Satisfaction×0.25 + Capacity×0.20
              </div>
            </div>
          )}

          {tab === 2 && (
            <div className="space-y-4">
              <div className="p-4 bg-slate-800 rounded-xl">
                <p className="text-xs text-slate-400 mb-1">Recommended Action</p>
                <p className="text-lg font-semibold text-teal-300">
                  {ACTION_LABELS[ticket.recommended_action] ?? ticket.recommended_action}
                </p>
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div
                  className={`p-3 rounded-lg ${
                    ticket.has_service_gap
                      ? "bg-amber-900/50 border border-amber-700"
                      : "bg-slate-800"
                  }`}
                >
                  <p className="text-xs text-slate-400">Service Gap</p>
                  <p
                    className={`font-semibold ${
                      ticket.has_service_gap ? "text-amber-300" : "text-teal-400"
                    }`}
                  >
                    {ticket.has_service_gap ? "YES" : "No"}
                  </p>
                </div>
                <div
                  className={`p-3 rounded-lg ${
                    ticket.requires_management_action
                      ? "bg-red-900/50 border border-red-700"
                      : "bg-slate-800"
                  }`}
                >
                  <p className="text-xs text-slate-400">Mgmt Action</p>
                  <p
                    className={`font-semibold ${
                      ticket.requires_management_action ? "text-red-300" : "text-teal-400"
                    }`}
                  >
                    {ticket.requires_management_action ? "REQUIRED" : "No"}
                  </p>
                </div>
                <div className="p-3 bg-slate-800 rounded-lg col-span-2">
                  <p className="text-xs text-slate-400">Agent Utilization</p>
                  <p className="text-slate-200 font-medium">
                    {pct(ticket.agent_utilization_pct)}
                  </p>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default function CustomerServiceQualityEnginePage() {
  const [data, setData] = useState<{ items: TicketRecord[]; summary: Summary } | null>(null);
  const [riskFilter, setRiskFilter] = useState("all");
  const [patternFilter, setPatternFilter] = useState("all");
  const [selected, setSelected] = useState<TicketRecord | null>(null);
  const [loading, setLoading] = useState(true);

  const load = useCallback(
    (risk: string, pattern: string) => {
      setLoading(true);
      const params = new URLSearchParams();
      if (risk !== "all")    params.set("risk",    risk);
      if (pattern !== "all") params.set("pattern", pattern);
      const qs = params.toString() ? `?${params}` : "";
      fetch(`/api/customer-service-quality-engine${qs}`, { cache: "no-store" })
        .then((r) => r.json())
        .then(setData)
        .finally(() => setLoading(false));
    },
    [],
  );

  useEffect(() => { load(riskFilter, patternFilter); }, [load, riskFilter, patternFilter]);

  const handleRisk = (v: string) => { setRiskFilter(v); };
  const handlePattern = (v: string) => { setPatternFilter(v); };

  if (!data && loading) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center">
        <div className="text-teal-400 animate-pulse">Loading customer service quality engine...</div>
      </div>
    );
  }

  const { items = [], summary } = data ?? { items: [], summary: null };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
      {selected && (
        <DetailModal ticket={selected} onClose={() => setSelected(null)} />
      )}

      {/* Header */}
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-slate-100">Customer Service Quality Engine</h1>
        <p className="text-slate-400 text-sm mt-1">
          Resolution monitoring · escalation pattern detection · agent capacity · CSAT tracking
        </p>
      </div>

      {/* KPI Strip */}
      {summary && (
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
          {[
            { label: "Total Tickets",       value: summary.total,                    sub: "monitored" },
            { label: "Service Gaps",        value: summary.service_gap_count,        sub: "detected",  alert: summary.service_gap_count > 0 },
            { label: "Mgmt Action Needed",  value: summary.management_action_count,  sub: "urgent",    alert: summary.management_action_count > 0 },
            { label: "Avg Composite",       value: summary.avg_service_composite.toFixed(1), sub: "risk score" },
          ].map(({ label, value, sub, alert }) => (
            <div
              key={label}
              className={`bg-slate-900 border rounded-xl p-4 ${
                alert ? "border-teal-700" : "border-slate-800"
              }`}
            >
              <p className="text-xs text-slate-400">{label}</p>
              <p className={`text-2xl font-bold mt-1 ${alert ? "text-teal-400" : "text-slate-100"}`}>
                {value}
              </p>
              <p className="text-xs text-slate-500 mt-1">{sub}</p>
            </div>
          ))}
        </div>
      )}

      {/* Sub-score averages + distributions */}
      {summary && (
        <div className="grid lg:grid-cols-2 gap-4 mb-6">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
            <h2 className="text-sm font-semibold text-slate-300 mb-4">Avg Sub-Scores</h2>
            <div className="space-y-3">
              {[
                { label: "Resolution Risk",   value: summary.avg_resolution_score },
                { label: "Escalation Risk",   value: summary.avg_escalation_score },
                { label: "Satisfaction Risk",  value: summary.avg_satisfaction_score },
                { label: "Capacity Risk",      value: summary.avg_capacity_score },
              ].map(({ label, value }) => (
                <div key={label}>
                  <div className="flex justify-between text-xs text-slate-400 mb-1">
                    <span>{label}</span>
                    <span className="text-slate-200">{value.toFixed(1)}</span>
                  </div>
                  <div className="h-2 bg-slate-700 rounded-full overflow-hidden">
                    <div
                      className="h-full rounded-full"
                      style={{ width: `${Math.min(value, 100)}%`, backgroundColor: compositeColor(value) }}
                    />
                  </div>
                </div>
              ))}
            </div>
            <div className="mt-4 pt-3 border-t border-slate-800 flex justify-between text-xs text-slate-500">
              <span>Avg churn risk</span>
              <span className="text-teal-400 font-medium">
                {(summary.avg_estimated_churn_risk_pct * 100).toFixed(0)}%
              </span>
            </div>
          </div>

          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-4">
            <div>
              <h2 className="text-sm font-semibold text-slate-300 mb-3">Risk Distribution</h2>
              <div className="space-y-2">
                {RISK_ORDER.map((r) => {
                  const cnt = summary.risk_counts[r] ?? 0;
                  const total = Object.values(summary.risk_counts).reduce((a, b) => a + b, 0) || 1;
                  return (
                    <div key={r} className="flex items-center gap-2 text-xs">
                      <span className="w-20 text-slate-400 capitalize">{r}</span>
                      <div className="flex-1 h-2 bg-slate-700 rounded-full overflow-hidden">
                        <div
                          className="h-full rounded-full"
                          style={{ width: `${(cnt / total) * 100}%`, backgroundColor: RISK_HEX[r] }}
                        />
                      </div>
                      <span className="w-5 text-right text-slate-300">{cnt}</span>
                    </div>
                  );
                })}
              </div>
            </div>
            <div>
              <h2 className="text-sm font-semibold text-slate-300 mb-3">Pattern Distribution</h2>
              <div className="space-y-1.5">
                {PATTERN_ORDER.filter((p) => (summary.pattern_counts[p] ?? 0) > 0).map((p) => {
                  const cnt = summary.pattern_counts[p] ?? 0;
                  const total = Object.values(summary.pattern_counts).reduce((a, b) => a + b, 0) || 1;
                  return (
                    <div key={p} className="flex items-center gap-2 text-xs">
                      <span className="w-40 text-slate-400">{PATTERN_LABELS[p] ?? p}</span>
                      <div className="flex-1 h-1.5 bg-slate-700 rounded-full overflow-hidden">
                        <div
                          className="h-full rounded-full bg-teal-500"
                          style={{ width: `${(cnt / total) * 100}%` }}
                        />
                      </div>
                      <span className="w-5 text-right text-slate-300">{cnt}</span>
                    </div>
                  );
                })}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Filter tabs — Risk */}
      <div className="mb-2">
        <p className="text-xs text-slate-500 mb-1 uppercase tracking-wide">Filter by Risk</p>
        <div className="flex flex-wrap gap-2 mb-3">
          {["all", ...RISK_ORDER].map((r) => (
            <button
              key={r}
              onClick={() => handleRisk(r)}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
                riskFilter === r
                  ? "bg-teal-700 text-white"
                  : "bg-slate-800 text-slate-400 hover:text-slate-200 hover:border-teal-700"
              }`}
            >
              {r === "all" ? "All Risks" : r.charAt(0).toUpperCase() + r.slice(1)}
              {r !== "all" && summary && (summary.risk_counts[r] ?? 0) > 0 && (
                <span className="ml-1 text-slate-400">({summary.risk_counts[r]})</span>
              )}
            </button>
          ))}
        </div>
      </div>

      {/* Filter tabs — Pattern */}
      <div className="mb-4">
        <p className="text-xs text-slate-500 mb-1 uppercase tracking-wide">Filter by Pattern</p>
        <div className="flex flex-wrap gap-2">
          {["all", ...PATTERN_ORDER].map((p) => (
            <button
              key={p}
              onClick={() => handlePattern(p)}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
                patternFilter === p
                  ? "bg-teal-700 text-white"
                  : "bg-slate-800 text-slate-400 hover:text-slate-200 hover:border-teal-700"
              }`}
            >
              {p === "all" ? "All Patterns" : PATTERN_LABELS[p] ?? p}
            </button>
          ))}
        </div>
      </div>

      {/* Ticket Cards */}
      {loading ? (
        <div className="grid sm:grid-cols-2 xl:grid-cols-3 gap-4">
          {Array.from({ length: 6 }).map((_, i) => (
            <div key={i} className="bg-slate-900 border border-slate-800 rounded-xl p-4 animate-pulse h-48" />
          ))}
        </div>
      ) : items.length === 0 ? (
        <p className="text-center text-slate-500 mt-12">No tickets match the current filters.</p>
      ) : (
        <div className="grid sm:grid-cols-2 xl:grid-cols-3 gap-4">
          {items.map((t) => {
            const riskCls     = RISK_COLORS[t.service_risk]         ?? "bg-slate-700 text-slate-300";
            const severityCls = SEVERITY_COLORS[t.service_severity] ?? "bg-slate-700 text-slate-300";
            return (
              <div
                key={t.ticket_id}
                onClick={() => setSelected(t)}
                className="bg-slate-900 border border-slate-800 rounded-xl p-4 cursor-pointer hover:border-teal-700 transition-colors"
              >
                <div className="flex items-start justify-between mb-3">
                  <div>
                    <p className="font-semibold text-slate-100">{t.ticket_id}</p>
                    <p className="text-xs text-slate-400">{t.agent_id} &middot; {t.region}</p>
                  </div>
                  <div className="flex flex-col gap-1 items-end">
                    <span className={`px-2 py-0.5 rounded text-xs font-medium ${riskCls}`}>
                      {t.service_risk}
                    </span>
                    <span className={`px-2 py-0.5 rounded text-xs font-medium ${severityCls}`}>
                      {t.service_severity}
                    </span>
                  </div>
                </div>

                <div className="flex items-center gap-3 mb-3">
                  <CompositeRing value={t.service_composite} risk={t.service_risk} />
                  <div className="flex-1 space-y-1.5">
                    <ScoreBar label="Resolution"   value={t.resolution_score}   color={compositeColor(t.resolution_score)} />
                    <ScoreBar label="Escalation"   value={t.escalation_score}   color={compositeColor(t.escalation_score)} />
                    <ScoreBar label="Satisfaction" value={t.satisfaction_score} color={compositeColor(t.satisfaction_score)} />
                    <ScoreBar label="Capacity"     value={t.capacity_score}     color={compositeColor(t.capacity_score)} />
                  </div>
                </div>

                <div className="flex gap-2 flex-wrap mb-2">
                  {t.has_service_gap && (
                    <span className="text-xs text-amber-300 bg-amber-900/40 px-2 py-0.5 rounded">
                      Service Gap
                    </span>
                  )}
                  {t.requires_management_action && (
                    <span className="text-xs text-red-300 bg-red-900/40 px-2 py-0.5 rounded">
                      Mgmt Action
                    </span>
                  )}
                  <span className="text-xs text-teal-300 bg-teal-900/30 px-2 py-0.5 rounded">
                    {(t.estimated_churn_risk_pct * 100).toFixed(0)}% churn risk
                  </span>
                </div>

                <p className="text-xs text-teal-400 font-medium mb-1">
                  {PATTERN_LABELS[t.service_pattern] ?? t.service_pattern}
                </p>
                <p className="text-xs text-slate-400 line-clamp-2">{t.service_signal}</p>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
