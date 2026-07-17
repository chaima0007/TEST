"use client";

import { useEffect, useState } from "react";

interface ComplianceAgent {
  agent_id: string;
  region: string;
  agent_type: string;
  compliance_risk: string;
  compliance_pattern: string;
  compliance_severity: string;
  recommended_action: string;
  bias_score: number;
  privacy_score: number;
  ethics_score: number;
  regulatory_score: number;
  compliance_composite: number;
  has_compliance_flag: boolean;
  requires_immediate_review: boolean;
  estimated_liability_index: number;
  compliance_signal: string;
}

interface Summary {
  total: number;
  risk_counts: Record<string, number>;
  pattern_counts: Record<string, number>;
  severity_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_compliance_composite: number;
  compliance_flag_count: number;
  immediate_review_count: number;
  avg_bias_score: number;
  avg_privacy_score: number;
  avg_ethics_score: number;
  avg_regulatory_score: number;
  avg_estimated_liability_index: number;
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

const PATTERN_COLORS: Record<string, string> = {
  none:                 "text-slate-400",
  bias_detection:       "text-red-400",
  gdpr_violation:       "text-orange-400",
  ethical_breach:       "text-amber-400",
  regulatory_gap:       "text-purple-400",
  transparency_failure: "text-violet-400",
};

const SEVERITY_BADGE: Record<string, string> = {
  compliant:     "bg-emerald-500/10 text-emerald-300",
  watchlist:     "bg-amber-500/10 text-amber-300",
  non_compliant: "bg-orange-500/10 text-orange-300",
  breach:        "bg-red-500/10 text-red-300",
};

const ACTION_BADGE: Record<string, string> = {
  no_action:                "bg-slate-700 text-slate-300",
  compliance_monitoring:    "bg-purple-500/20 text-purple-300",
  bias_review:              "bg-red-500/20 text-red-300",
  gdpr_remediation:         "bg-orange-500/20 text-orange-300",
  ethical_committee_review: "bg-amber-500/20 text-amber-300",
  regulatory_audit:         "bg-violet-500/20 text-violet-300",
  transparency_report:      "bg-sky-500/20 text-sky-300",
  immediate_suspension:     "bg-red-700/40 text-red-200 border border-red-500/50",
  legal_escalation:         "bg-red-900/60 text-red-100 border border-red-400/60",
};

function CompositeRing({ value }: { value: number }) {
  const r = 28;
  const circ = 2 * Math.PI * r;
  const fill = (value / 100) * circ;
  const color = value >= 60 ? "#ef4444" : value >= 40 ? "#f97316" : value >= 20 ? "#f59e0b" : "#a855f7";
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

function DetailModal({ agent, onClose }: { agent: ComplianceAgent; onClose: () => void }) {
  const [tab, setTab] = useState<"overview" | "scores" | "action">("overview");

  useEffect(() => {
    const handler = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [onClose]);

  const tabs = [
    { id: "overview" as const, label: "Overview" },
    { id: "scores"   as const, label: "Sub-Scores" },
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
              <p className="text-xs text-slate-500 mb-1">{agent.agent_id} · {agent.region}</p>
              <h2 className="text-lg font-bold text-white">{agent.agent_id}</h2>
              <p className="text-xs text-purple-400 mt-0.5">{agent.agent_type.replace(/_/g, " ")}</p>
              <div className="flex items-center gap-2 mt-2 flex-wrap">
                <span className={`text-xs px-2 py-0.5 rounded-full border ${RISK_BG[agent.compliance_risk]}`}>
                  {agent.compliance_risk.toUpperCase()} RISK
                </span>
                <span className={`text-xs px-2 py-0.5 rounded-full ${SEVERITY_BADGE[agent.compliance_severity]}`}>
                  {agent.compliance_severity.replace(/_/g, " ")}
                </span>
              </div>
            </div>
            <CompositeRing value={agent.compliance_composite} />
          </div>
        </div>

        <div className="flex border-b border-slate-800">
          {tabs.map((t) => (
            <button key={t.id} onClick={() => setTab(t.id)}
              className={`flex-1 py-3 text-xs font-medium transition-colors ${
                tab === t.id ? "text-purple-400 border-b-2 border-purple-400" : "text-slate-500 hover:text-slate-300"
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
                  <p className="text-xs text-slate-500">Pattern</p>
                  <p className={`text-sm font-semibold mt-1 ${PATTERN_COLORS[agent.compliance_pattern]}`}>
                    {agent.compliance_pattern.replace(/_/g, " ")}
                  </p>
                </div>
                <div className="bg-slate-800/60 rounded-lg p-3">
                  <p className="text-xs text-slate-500">Liability Index</p>
                  <p className={`text-sm font-semibold mt-1 ${agent.estimated_liability_index > 5 ? "text-red-400" : agent.estimated_liability_index > 2 ? "text-orange-400" : "text-purple-400"}`}>
                    {agent.estimated_liability_index.toFixed(2)} / 10
                  </p>
                </div>
                <div className="bg-slate-800/60 rounded-lg p-3">
                  <p className="text-xs text-slate-500">Compliance Flag</p>
                  <p className={`text-sm font-semibold mt-1 ${agent.has_compliance_flag ? "text-red-400" : "text-emerald-400"}`}>
                    {agent.has_compliance_flag ? "Active" : "Clear"}
                  </p>
                </div>
                <div className="bg-slate-800/60 rounded-lg p-3">
                  <p className="text-xs text-slate-500">Immediate Review</p>
                  <p className={`text-sm font-semibold mt-1 ${agent.requires_immediate_review ? "text-orange-400" : "text-emerald-400"}`}>
                    {agent.requires_immediate_review ? "Required" : "Not needed"}
                  </p>
                </div>
              </div>
              <div className="bg-slate-800/40 rounded-lg p-3 border-l-2 border-purple-500">
                <p className="text-xs text-slate-400 italic">{agent.compliance_signal}</p>
              </div>
            </div>
          )}

          {tab === "scores" && (
            <div className="space-y-3">
              <ScoreBar label="Bias Score"       value={agent.bias_score}       color="text-red-400" />
              <ScoreBar label="Privacy Score"    value={agent.privacy_score}    color="text-orange-400" />
              <ScoreBar label="Ethics Score"     value={agent.ethics_score}     color="text-amber-400" />
              <ScoreBar label="Regulatory Score" value={agent.regulatory_score} color="text-violet-400" />
              <div className="pt-2 border-t border-slate-800">
                <div className="flex justify-between text-sm">
                  <span className="text-slate-400 font-medium">Compliance Composite</span>
                  <span className="text-white font-bold">{agent.compliance_composite.toFixed(1)}</span>
                </div>
                <p className="text-xs text-slate-600 mt-1">bias×0.30 + privacy×0.25 + ethics×0.25 + regulatory×0.20</p>
              </div>
            </div>
          )}

          {tab === "action" && (
            <div className="space-y-4">
              <div className={`rounded-xl p-4 border ${RISK_BG[agent.compliance_risk]}`}>
                <p className="text-xs text-slate-400 mb-1">Recommended Action</p>
                <p className={`text-xl font-bold ${RISK_COLORS[agent.compliance_risk]}`}>
                  {agent.recommended_action.replace(/_/g, " ").toUpperCase()}
                </p>
              </div>
              <div className="bg-slate-800/40 rounded-lg p-3 space-y-2">
                <div className="flex justify-between text-xs">
                  <span className="text-slate-400">Severity</span>
                  <span className={SEVERITY_BADGE[agent.compliance_severity]?.split(" ")[1]}>{agent.compliance_severity.replace(/_/g, " ")}</span>
                </div>
                <div className="flex justify-between text-xs">
                  <span className="text-slate-400">Composite</span>
                  <span className="text-white">{agent.compliance_composite.toFixed(1)} / 100</span>
                </div>
                <div className="flex justify-between text-xs">
                  <span className="text-slate-400">Est. Liability Index</span>
                  <span className="text-purple-400">{agent.estimated_liability_index.toFixed(2)} / 10</span>
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

export default function EthicsComplianceSentinelPage() {
  const [data, setData]           = useState<{ agents: ComplianceAgent[]; summary: Summary } | null>(null);
  const [loading, setLoading]     = useState(true);
  const [riskFilter, setRiskFilter]       = useState<string>("");
  const [patternFilter, setPatternFilter] = useState<string>("");
  const [selected, setSelected]   = useState<ComplianceAgent | null>(null);

  useEffect(() => {
    async function load() {
        setLoading(true);
        const params = new URLSearchParams();
        if (riskFilter)    params.set("risk",    riskFilter);
        if (patternFilter) params.set("pattern", patternFilter);
        const res  = await fetch(`/api/ethics-compliance-sentinel-engine?${params}`);
        const json = await res.json();
        setData(json);
        setLoading(false);
  }
    load();
  }, [riskFilter, patternFilter]);

  const s      = data?.summary;
  const agents = data?.agents ?? [];
  const riskLevels = ["low", "moderate", "high", "critical"];
  const patterns   = ["none", "bias_detection", "gdpr_violation", "ethical_breach", "regulatory_gap", "transparency_failure"];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
      <div className="max-w-7xl mx-auto space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white">Ethics &amp; Compliance Sentinel Engine</h1>
          <p className="text-slate-400 text-sm mt-1">
            Monitors AI agents for bias, privacy, ethics, and regulatory compliance risks across the Caelum Swarm
          </p>
        </div>

        {s && (
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {[
              { label: "Total Agents",       value: s.total,                        sub: "monitored" },
              { label: "Compliance Flags",   value: s.compliance_flag_count,        sub: "active" },
              { label: "Immediate Review",   value: s.immediate_review_count,       sub: "required" },
              { label: "Avg Liability",      value: s.avg_estimated_liability_index.toFixed(2), sub: "/ 10 index" },
            ].map((k) => (
              <div key={k.label} className="bg-slate-900 border border-purple-900/40 rounded-xl p-4">
                <p className="text-xs text-slate-500">{k.label}</p>
                <p className="text-2xl font-bold text-purple-400 mt-1">{k.value}</p>
                <p className="text-xs text-slate-600 mt-0.5">{k.sub}</p>
              </div>
            ))}
          </div>
        )}

        {s && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
              <h2 className="text-sm font-semibold text-slate-300 mb-4">Average Compliance Sub-Scores</h2>
              <div className="space-y-3">
                {[
                  { label: "Bias Score",       value: s.avg_bias_score,       color: "text-red-400" },
                  { label: "Privacy Score",    value: s.avg_privacy_score,    color: "text-orange-400" },
                  { label: "Ethics Score",     value: s.avg_ethics_score,     color: "text-amber-400" },
                  { label: "Regulatory Score", value: s.avg_regulatory_score, color: "text-violet-400" },
                ].map((item) => (
                  <ScoreBar key={item.label} label={item.label} value={item.value} color={item.color} />
                ))}
              </div>
            </div>

            <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
              <h2 className="text-sm font-semibold text-slate-300 mb-4">Pattern Distribution</h2>
              <div className="space-y-2">
                {patterns.filter((p) => s.pattern_counts[p]).map((p) => {
                  const count = s.pattern_counts[p] || 0;
                  const pct   = (count / s.total) * 100;
                  return (
                    <div key={p}>
                      <div className="flex justify-between text-xs mb-1">
                        <span className={PATTERN_COLORS[p]}>{p.replace(/_/g, " ")}</span>
                        <span className="text-slate-400">{count}</span>
                      </div>
                      <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
                        <div className={`h-full rounded-full ${(PATTERN_COLORS[p] || "text-slate-400").replace("text-", "bg-")}`}
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
                    riskFilter === r ? "bg-purple-600 text-white" : "bg-slate-800 text-slate-400 hover:border-purple-700 hover:bg-slate-700"
                  }`}>
                  {r || "All"}
                </button>
              ))}
            </div>
          </div>
          <div>
            <p className="text-xs text-slate-500 mb-1">Pattern</p>
            <div className="flex flex-wrap gap-1">
              {["", ...patterns].map((p) => (
                <button key={p || "all"} onClick={() => setPatternFilter(p)}
                  className={`px-3 py-1 rounded-full text-xs transition-colors ${
                    patternFilter === p ? "bg-purple-600 text-white" : "bg-slate-800 text-slate-400 hover:border-purple-700 hover:bg-slate-700"
                  }`}>
                  {p ? p.replace(/_/g, " ") : "All"}
                </button>
              ))}
            </div>
          </div>
        </div>

        {loading ? (
          <div className="flex items-center justify-center h-40">
            <div className="w-8 h-8 border-2 border-purple-500 border-t-transparent rounded-full animate-spin" />
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
            {agents.map((agent) => (
              <button key={agent.agent_id} onClick={() => setSelected(agent)} className="text-left w-full">
                <div className={`bg-slate-900 border rounded-xl p-4 hover:border-purple-700 transition-colors cursor-pointer ${
                  agent.has_compliance_flag ? "border-purple-500/40" : "border-slate-800"
                }`}>
                  <div className="flex items-start justify-between gap-3 mb-3">
                    <div className="min-w-0">
                      <div className="flex items-center gap-2 flex-wrap mb-1">
                        <span className={`text-xs px-2 py-0.5 rounded-full border ${RISK_BG[agent.compliance_risk]}`}>
                          {agent.compliance_risk}
                        </span>
                        <span className={`text-xs ${PATTERN_COLORS[agent.compliance_pattern]}`}>
                          {agent.compliance_pattern.replace(/_/g, " ")}
                        </span>
                      </div>
                      <p className="text-sm font-semibold text-white">{agent.agent_id}</p>
                      <p className="text-xs text-purple-400">{agent.agent_type.replace(/_/g, " ")}</p>
                      <p className="text-xs text-slate-500">{agent.region}</p>
                    </div>
                    <CompositeRing value={agent.compliance_composite} />
                  </div>

                  <div className="space-y-1.5 mb-3">
                    <ScoreBar label="Bias"       value={agent.bias_score}       color="text-red-400" />
                    <ScoreBar label="Privacy"    value={agent.privacy_score}    color="text-orange-400" />
                    <ScoreBar label="Ethics"     value={agent.ethics_score}     color="text-amber-400" />
                    <ScoreBar label="Regulatory" value={agent.regulatory_score} color="text-violet-400" />
                  </div>

                  <div className="flex items-center justify-between mb-2">
                    <span className={`text-xs px-2 py-0.5 rounded-full ${ACTION_BADGE[agent.recommended_action]}`}>
                      {agent.recommended_action.replace(/_/g, " ")}
                    </span>
                    <span className={`text-xs px-2 py-0.5 rounded-full ${SEVERITY_BADGE[agent.compliance_severity]}`}>
                      {agent.compliance_severity.replace(/_/g, " ")}
                    </span>
                  </div>

                  <p className="text-xs text-slate-500 italic line-clamp-1">{agent.compliance_signal}</p>
                  <div className="text-xs text-purple-400 font-medium mt-1">
                    Liability index: {agent.estimated_liability_index.toFixed(2)} / 10
                  </div>
                </div>
              </button>
            ))}
          </div>
        )}
      </div>

      {selected && <DetailModal agent={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
