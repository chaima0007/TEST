"use client";

import { useState, useEffect, useRef } from "react";

interface CertData {
  cert_id: string;
  region: string;
  cert_risk: string;
  cert_pattern: string;
  cert_severity: string;
  recommended_action: string;
  expiry_score: number;
  gap_score: number;
  audit_score: number;
  compliance_score: number;
  cert_composite: number;
  has_cert_risk: boolean;
  requires_immediate_action: boolean;
  estimated_compliance_gap_index: number;
  cert_signal: string;
}

interface Summary {
  total: number;
  risk_counts: Record<string, number>;
  pattern_counts: Record<string, number>;
  severity_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_cert_composite: number;
  cert_risk_count: number;
  immediate_action_count: number;
  avg_expiry_score: number;
  avg_gap_score: number;
  avg_audit_score: number;
  avg_compliance_score: number;
  avg_estimated_compliance_gap_index: number;
}

const RISK_BG: Record<string, string> = {
  low:      "bg-emerald-500/20 border-emerald-500/30 text-emerald-300",
  moderate: "bg-amber-500/20 border-amber-500/30 text-amber-300",
  high:     "bg-orange-500/20 border-orange-500/30 text-orange-300",
  critical: "bg-rose-500/20 border-rose-500/30 text-rose-300",
};
const RISK_COLOR: Record<string, string> = {
  low:      "#34d399",
  moderate: "#fbbf24",
  high:     "#f97316",
  critical: "#f87171",
};
const RISK_LABEL: Record<string, string> = {
  low:      "Low Risk",
  moderate: "Moderate",
  high:     "High Risk",
  critical: "Critical",
};
const SEVERITY_BG: Record<string, string> = {
  current:  "bg-emerald-500/15 text-emerald-300",
  due_soon: "bg-amber-500/15 text-amber-300",
  overdue:  "bg-orange-500/15 text-orange-300",
  expired:  "bg-rose-500/15 text-rose-300",
};
const SEVERITY_LABEL: Record<string, string> = {
  current:  "Current",
  due_soon: "Due Soon",
  overdue:  "Overdue",
  expired:  "Expired",
};
const ACTION_BG: Record<string, string> = {
  no_action:                "bg-emerald-500/15 text-emerald-300",
  cert_monitoring:          "bg-sky-500/15 text-sky-300",
  renewal_scheduling:       "bg-amber-500/15 text-amber-300",
  standard_update:          "bg-yellow-500/15 text-yellow-300",
  gap_remediation:          "bg-orange-500/15 text-orange-300",
  audit_preparation:        "bg-orange-600/15 text-orange-300",
  emergency_recertification: "bg-rose-500/15 text-rose-300",
  regulatory_submission:    "bg-violet-500/15 text-violet-300",
  board_compliance_review:  "bg-red-500/15 text-red-300",
};
const ACTION_LABEL: Record<string, string> = {
  no_action:                "No Action",
  cert_monitoring:          "Cert Monitoring",
  renewal_scheduling:       "Renewal Scheduling",
  standard_update:          "Standard Update",
  gap_remediation:          "Gap Remediation",
  audit_preparation:        "Audit Preparation",
  emergency_recertification: "Emergency Recertification",
  regulatory_submission:    "Regulatory Submission",
  board_compliance_review:  "Board Compliance Review",
};
const PATTERN_LABEL: Record<string, string> = {
  none:                  "None",
  certification_expiry:  "Certification Expiry",
  standard_obsolescence: "Standard Obsolescence",
  compliance_gap:        "Compliance Gap",
  audit_failure:         "Audit Failure",
  new_requirement:       "New Requirement",
};

function RiskGauge({ pct, color, size = 80 }: { pct: number; color: string; size?: number }) {
  const r = size * 0.38;
  const circ = 2 * Math.PI * r;
  const fill = (pct / 100) * circ;
  return (
    <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`}>
      <circle cx={size / 2} cy={size / 2} r={r} fill="none" stroke="#1e293b" strokeWidth={size * 0.1} />
      <circle
        cx={size / 2} cy={size / 2} r={r} fill="none"
        stroke={color} strokeWidth={size * 0.1}
        strokeDasharray={`${fill} ${circ}`}
        strokeLinecap="round"
        transform={`rotate(-90 ${size / 2} ${size / 2})`}
      />
      <text x={size / 2} y={size / 2 + 5} textAnchor="middle" fill={color} fontSize={size * 0.22} fontWeight="bold">
        {pct.toFixed(0)}
      </text>
    </svg>
  );
}

function ScoreBar({ score, label }: { score: number; label: string }) {
  const color = score <= 20 ? "#34d399" : score <= 40 ? "#fbbf24" : score <= 60 ? "#f97316" : "#f87171";
  return (
    <div>
      <div className="flex justify-between mb-1">
        <span className="text-xs text-slate-400">{label}</span>
        <span className="text-xs font-medium" style={{ color }}>{score.toFixed(0)}</span>
      </div>
      <div className="h-1.5 bg-slate-700 rounded-full overflow-hidden">
        <div className="h-full rounded-full transition-all" style={{ width: `${Math.min(score, 100)}%`, backgroundColor: color }} />
      </div>
    </div>
  );
}

interface ModalProps { cert: CertData; onClose: () => void }

function DetailModal({ cert, onClose }: ModalProps) {
  const [tab, setTab] = useState<"overview" | "scores" | "action">("overview");
  const backdropRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handler = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [onClose]);

  const riskColor = RISK_COLOR[cert.cert_risk] ?? "#94a3b8";

  return (
    <div
      ref={backdropRef}
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4"
      onClick={(e) => { if (e.target === backdropRef.current) onClose(); }}
    >
      <div className="bg-slate-900 border border-slate-700 rounded-xl shadow-2xl w-full max-w-lg">
        <div className="flex items-start justify-between p-5 border-b border-slate-800">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <span className={`text-xs px-2 py-0.5 rounded-full border font-medium ${RISK_BG[cert.cert_risk] ?? ""}`}>
                {RISK_LABEL[cert.cert_risk] ?? cert.cert_risk}
              </span>
              <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${SEVERITY_BG[cert.cert_severity] ?? ""}`}>
                {SEVERITY_LABEL[cert.cert_severity] ?? cert.cert_severity}
              </span>
            </div>
            <h2 className="text-white font-bold text-lg">{cert.cert_id}</h2>
            <p className="text-slate-400 text-sm">{cert.region} · Composite: <span style={{ color: riskColor }}>{cert.cert_composite}</span></p>
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-white p-1 transition-colors" aria-label="Close">
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <div className="flex border-b border-slate-800">
          {(["overview", "scores", "action"] as const).map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`flex-1 py-2.5 text-sm font-medium capitalize transition-colors ${
                tab === t ? "text-amber-400 border-b-2 border-amber-500 bg-slate-800/40" : "text-slate-400 hover:text-slate-200"
              }`}
            >
              {t === "overview" ? "Overview" : t === "scores" ? "Sub-Scores" : "Action Plan"}
            </button>
          ))}
        </div>

        <div className="p-5 space-y-4">
          {tab === "overview" && (
            <>
              <div className="flex items-center justify-center py-3">
                <RiskGauge pct={cert.cert_composite} color={riskColor} size={110} />
              </div>
              <div className="bg-slate-800/50 rounded-lg p-3">
                <p className="text-xs text-slate-400 mb-1">Cert Signal</p>
                <p className="text-sm text-white">{cert.cert_signal}</p>
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div className="bg-slate-800/50 rounded-lg p-3">
                  <p className="text-xs text-slate-400">Compliance Gap Index</p>
                  <p className="text-lg font-bold text-orange-400">{cert.estimated_compliance_gap_index.toFixed(2)}</p>
                </div>
                <div className="bg-slate-800/50 rounded-lg p-3">
                  <p className="text-xs text-slate-400">Immediate Action</p>
                  <p className={`text-lg font-bold ${cert.requires_immediate_action ? "text-rose-400" : "text-emerald-400"}`}>
                    {cert.requires_immediate_action ? "Required" : "Not Needed"}
                  </p>
                </div>
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div className="bg-slate-800/50 rounded-lg p-3">
                  <p className="text-xs text-slate-400">Cert Risk</p>
                  <p className={`text-sm font-medium ${cert.has_cert_risk ? "text-orange-400" : "text-emerald-400"}`}>
                    {cert.has_cert_risk ? "At Risk" : "Clear"}
                  </p>
                </div>
                <div className="bg-slate-800/50 rounded-lg p-3">
                  <p className="text-xs text-slate-400">Pattern</p>
                  <p className="text-sm font-medium text-slate-200">{PATTERN_LABEL[cert.cert_pattern] ?? cert.cert_pattern}</p>
                </div>
              </div>
            </>
          )}

          {tab === "scores" && (
            <div className="space-y-3">
              <ScoreBar score={cert.expiry_score} label="Expiry (30%)" />
              <ScoreBar score={cert.gap_score} label="Gap (25%)" />
              <ScoreBar score={cert.audit_score} label="Audit (25%)" />
              <ScoreBar score={cert.compliance_score} label="Compliance (20%)" />
              <div className="pt-2 border-t border-slate-800">
                <div className="flex justify-between items-center">
                  <span className="text-sm text-slate-400">Cert Composite (risk)</span>
                  <span className="text-lg font-bold" style={{ color: riskColor }}>{cert.cert_composite}</span>
                </div>
                <p className="text-xs text-slate-500 mt-1">Higher composite = greater compliance risk</p>
              </div>
            </div>
          )}

          {tab === "action" && (
            <div className="space-y-4">
              <div className="bg-slate-800/50 rounded-lg p-4">
                <p className="text-xs text-slate-400 mb-2">Recommended Action</p>
                <span className={`text-sm px-3 py-1.5 rounded-lg font-medium ${ACTION_BG[cert.recommended_action] ?? ""}`}>
                  {ACTION_LABEL[cert.recommended_action] ?? cert.recommended_action}
                </span>
              </div>
              <div className="space-y-2">
                <div className="flex justify-between p-2 rounded bg-slate-800/40">
                  <span className="text-xs text-slate-400">Pattern</span>
                  <span className="text-xs text-slate-200">{PATTERN_LABEL[cert.cert_pattern] ?? cert.cert_pattern}</span>
                </div>
                <div className="flex justify-between p-2 rounded bg-slate-800/40">
                  <span className="text-xs text-slate-400">Severity</span>
                  <span className="text-xs text-slate-200">{SEVERITY_LABEL[cert.cert_severity] ?? cert.cert_severity}</span>
                </div>
                <div className="flex justify-between p-2 rounded bg-slate-800/40">
                  <span className="text-xs text-slate-400">Compliance Gap Index</span>
                  <span className="text-xs text-orange-400 font-medium">{cert.estimated_compliance_gap_index.toFixed(2)}</span>
                </div>
                <div className="flex justify-between p-2 rounded bg-slate-800/40">
                  <span className="text-xs text-slate-400">Immediate Action</span>
                  <span className={`text-xs font-medium ${cert.requires_immediate_action ? "text-rose-400" : "text-emerald-400"}`}>
                    {cert.requires_immediate_action ? "Required" : "Not Needed"}
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

function DistBar({ counts, colors }: { counts: Record<string, number>; colors: Record<string, string> }) {
  const total = Object.values(counts).reduce((a, b) => a + b, 0);
  if (!total) return null;
  return (
    <div className="flex h-2 rounded-full overflow-hidden gap-px">
      {Object.entries(counts).map(([k, v]) =>
        v > 0 ? (
          <div key={k} style={{ width: `${(v / total) * 100}%`, backgroundColor: colors[k] ?? "#94a3b8" }} title={`${k}: ${v}`} />
        ) : null
      )}
    </div>
  );
}

const RISK_FILTERS = ["all", "low", "moderate", "high", "critical"] as const;
type RiskFilter = typeof RISK_FILTERS[number];

export default function CertificationStandardsTrackerEnginePage() {
  const [data, setData] = useState<{ certs: CertData[]; summary: Summary } | null>(null);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState<RiskFilter>("all");
  const [selected, setSelected] = useState<CertData | null>(null);

  const fetchData = async (risk: RiskFilter) => {
    setLoading(true);
    const params = new URLSearchParams();
    if (risk !== "all") params.set("risk", risk);
    const res = await fetch(`/api/certification-standards-tracker-engine?${params}`);
    const json = await res.json();
    setData(json);
    setLoading(false);
  };

  useEffect(() => { fetchData(filter); }, [filter, fetchData]);

  const s = data?.summary;
  const certs = data?.certs ?? [];

  const riskColors: Record<string, string> = {
    low: "#34d399", moderate: "#fbbf24", high: "#f97316", critical: "#f87171",
  };
  const severityColors: Record<string, string> = {
    current: "#34d399", due_soon: "#fbbf24", overdue: "#f97316", expired: "#f87171",
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
      {selected && <DetailModal cert={selected} onClose={() => setSelected(null)} />}

      <div className="mb-6">
        <h1 className="text-2xl font-bold text-white">Certification & Industry Standards Tracker Engine</h1>
        <p className="text-slate-400 text-sm mt-1">
          Monitor certification expiry, compliance gaps, and audit readiness — prevent regulatory failures before they occur
        </p>
      </div>

      {/* KPI Strip */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
          <p className="text-xs text-slate-400 mb-1">Total Certs</p>
          <p className="text-2xl font-bold text-white">{s?.total ?? "—"}</p>
        </div>
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
          <p className="text-xs text-slate-400 mb-1">At Cert Risk</p>
          <p className="text-2xl font-bold text-orange-400">{s?.cert_risk_count ?? "—"}</p>
        </div>
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
          <p className="text-xs text-slate-400 mb-1">Immediate Action</p>
          <p className="text-2xl font-bold text-rose-400">{s?.immediate_action_count ?? "—"}</p>
        </div>
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
          <p className="text-xs text-slate-400 mb-1">Avg Cert Composite</p>
          <p className="text-2xl font-bold text-amber-400">{s?.avg_cert_composite ?? "—"}</p>
        </div>
      </div>

      {/* Score panel + Distribution */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
          <h3 className="text-sm font-semibold text-slate-300 mb-3">Avg Sub-Scores (compliance risk)</h3>
          <div className="space-y-3">
            <ScoreBar score={s?.avg_expiry_score ?? 0} label="Expiry (30%)" />
            <ScoreBar score={s?.avg_gap_score ?? 0} label="Gap (25%)" />
            <ScoreBar score={s?.avg_audit_score ?? 0} label="Audit (25%)" />
            <ScoreBar score={s?.avg_compliance_score ?? 0} label="Compliance (20%)" />
          </div>
        </div>
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 space-y-4">
          <div>
            <div className="flex justify-between items-center mb-2">
              <h3 className="text-sm font-semibold text-slate-300">Risk Distribution</h3>
              <span className="text-xs text-slate-500">{s?.total ?? 0} certs</span>
            </div>
            <DistBar counts={s?.risk_counts ?? {}} colors={riskColors} />
            <div className="flex flex-wrap gap-2 mt-2">
              {Object.entries(s?.risk_counts ?? {}).map(([k, v]) => (
                <span key={k} className="text-xs" style={{ color: riskColors[k] ?? "#94a3b8" }}>
                  {RISK_LABEL[k] ?? k}: {v}
                </span>
              ))}
            </div>
          </div>
          <div>
            <div className="flex justify-between items-center mb-2">
              <h3 className="text-sm font-semibold text-slate-300">Severity Distribution</h3>
            </div>
            <DistBar counts={s?.severity_counts ?? {}} colors={severityColors} />
            <div className="flex flex-wrap gap-2 mt-2">
              {Object.entries(s?.severity_counts ?? {}).map(([k, v]) => (
                <span key={k} className="text-xs" style={{ color: severityColors[k] ?? "#94a3b8" }}>
                  {SEVERITY_LABEL[k] ?? k}: {v}
                </span>
              ))}
            </div>
          </div>
          <div className="border-t border-slate-800 pt-3">
            <div className="flex justify-between">
              <span className="text-xs text-slate-400">Avg Compliance Gap Index</span>
              <span className="text-sm font-bold text-orange-400">{s?.avg_estimated_compliance_gap_index?.toFixed(2) ?? "—"}</span>
            </div>
          </div>
        </div>
      </div>

      {/* Filter tabs */}
      <div className="flex flex-wrap gap-2 mb-4">
        {RISK_FILTERS.map((f) => (
          <button
            key={f}
            onClick={() => setFilter(f)}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors border ${
              filter === f
                ? "bg-amber-600 border-amber-500 text-white"
                : "bg-slate-800 border-slate-700 text-slate-400 hover:text-white hover:border-slate-600"
            }`}
          >
            {f === "all" ? "All Certs" : RISK_LABEL[f] ?? f}
            {f !== "all" && s?.risk_counts?.[f] !== undefined && (
              <span className="ml-1 opacity-70">({s.risk_counts[f]})</span>
            )}
          </button>
        ))}
      </div>

      {/* Cert cards */}
      {loading ? (
        <div className="flex items-center justify-center h-48">
          <div className="w-8 h-8 border-2 border-amber-500 border-t-transparent rounded-full animate-spin" />
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
          {certs.map((cert) => {
            const color = RISK_COLOR[cert.cert_risk] ?? "#94a3b8";
            return (
              <div
                key={cert.cert_id}
                onClick={() => setSelected(cert)}
                className="bg-slate-900 border border-slate-800 rounded-xl p-4 cursor-pointer hover:border-slate-600 transition-all hover:bg-slate-800/60"
              >
                <div className="flex items-start justify-between mb-3">
                  <div>
                    <div className="flex items-center gap-2 mb-1">
                      <span className={`text-xs px-2 py-0.5 rounded-full border font-medium ${RISK_BG[cert.cert_risk] ?? ""}`}>
                        {RISK_LABEL[cert.cert_risk] ?? cert.cert_risk}
                      </span>
                      {cert.requires_immediate_action && (
                        <span className="text-xs px-2 py-0.5 rounded-full bg-rose-500/20 border border-rose-500/30 text-rose-300 font-medium">
                          Urgent
                        </span>
                      )}
                    </div>
                    <h3 className="text-white font-semibold text-sm">{cert.cert_id}</h3>
                    <p className="text-slate-400 text-xs">{cert.region}</p>
                  </div>
                  <RiskGauge pct={cert.cert_composite} color={color} size={72} />
                </div>

                <div className="space-y-1.5 mb-3">
                  <ScoreBar score={cert.expiry_score} label="Expiry" />
                  <ScoreBar score={cert.gap_score} label="Gap" />
                  <ScoreBar score={cert.audit_score} label="Audit" />
                  <ScoreBar score={cert.compliance_score} label="Compliance" />
                </div>

                <div className="border-t border-slate-800 pt-2 flex items-center justify-between">
                  <span className={`text-xs px-2 py-0.5 rounded font-medium ${ACTION_BG[cert.recommended_action] ?? ""}`}>
                    {ACTION_LABEL[cert.recommended_action] ?? cert.recommended_action}
                  </span>
                  {cert.estimated_compliance_gap_index > 0 && (
                    <span className="text-xs text-orange-400 font-medium">
                      gap idx {cert.estimated_compliance_gap_index.toFixed(2)}
                    </span>
                  )}
                </div>
                <p className="text-xs text-slate-500 mt-2 truncate">{cert.cert_signal}</p>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
