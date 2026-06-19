"use client";

import { useEffect, useState, useCallback } from "react";

// ── types ────────────────────────────────────────────────────────────────────
interface ProcessRecord {
  process_id: string;
  process_type: string;
  region: string;
  quality_risk: string;
  quality_pattern: string;
  quality_severity: string;
  recommended_action: string;
  defect_score: number;
  process_score: number;
  compliance_score: number;
  supplier_score: number;
  quality_composite: number;
  has_quality_alert: boolean;
  requires_immediate_action: boolean;
  estimated_quality_risk_index: number;
  quality_signal: string;
}

interface Summary {
  total: number;
  risk_counts: Record<string, number>;
  pattern_counts: Record<string, number>;
  severity_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_quality_composite: number;
  quality_alert_count: number;
  immediate_action_count: number;
  avg_defect_score: number;
  avg_process_score: number;
  avg_compliance_score: number;
  avg_supplier_score: number;
  avg_estimated_quality_risk_index: number;
}

// ── helpers ──────────────────────────────────────────────────────────────────
const RISK_COLOR: Record<string, string> = {
  critical: "text-rose-400",
  high:     "text-orange-400",
  moderate: "text-yellow-400",
  low:      "text-slate-400",
};

const RISK_BG: Record<string, string> = {
  critical: "bg-rose-500/20 border-rose-500/40",
  high:     "bg-orange-500/20 border-orange-500/40",
  moderate: "bg-yellow-500/20 border-yellow-500/40",
  low:      "bg-slate-500/20 border-slate-500/40",
};

const SEVERITY_COLOR: Record<string, string> = {
  critical:   "text-rose-400",
  degraded:   "text-orange-400",
  acceptable: "text-yellow-400",
  excellent:  "text-lime-400",
};

const PATTERN_ICON: Record<string, string> = {
  defect_surge:             "🔴",
  process_deviation:        "🔀",
  sla_breach:               "⏱️",
  audit_failure:            "📋",
  supplier_quality_failure: "🏭",
  none:                     "—",
};

const PROCESS_TYPE_ICON: Record<string, string> = {
  manufacturing: "🏭",
  software:      "💻",
  service:       "🎯",
  procurement:   "📦",
  delivery:      "🚚",
};

function CompositeRing({ score, color }: { score: number; color: string }) {
  const r = 36, circ = 2 * Math.PI * r;
  const fill = (Math.min(score, 100) / 100) * circ;
  return (
    <svg width={88} height={88} viewBox="0 0 88 88">
      <circle cx={44} cy={44} r={r} fill="none" stroke="#1e293b" strokeWidth={8} />
      <circle
        cx={44} cy={44} r={r} fill="none"
        stroke={color} strokeWidth={8}
        strokeDasharray={`${fill} ${circ}`}
        strokeLinecap="round"
        transform="rotate(-90 44 44)"
      />
      <text x={44} y={49} textAnchor="middle" fill="white" fontSize={14} fontWeight="bold">
        {Math.round(score)}
      </text>
    </svg>
  );
}

function ScoreBar({ label, value, color }: { label: string; value: number; color: string }) {
  return (
    <div>
      <div className="flex justify-between text-xs text-slate-400 mb-1">
        <span>{label}</span><span>{value.toFixed(1)}</span>
      </div>
      <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
        <div className={`h-full rounded-full ${color}`} style={{ width: `${value}%` }} />
      </div>
    </div>
  );
}

function RiskDistBar({ counts }: { counts: Record<string, number> }) {
  const order  = ["critical", "high", "moderate", "low"];
  const colors = ["bg-rose-500", "bg-orange-500", "bg-yellow-500", "bg-slate-500"];
  const total  = Object.values(counts).reduce((a, b) => a + b, 0) || 1;
  return (
    <div className="flex gap-1 h-3 rounded-full overflow-hidden">
      {order.map((k, i) => (
        <div
          key={k}
          className={colors[i]}
          style={{ width: `${((counts[k] || 0) / total) * 100}%` }}
          title={`${k}: ${counts[k] || 0}`}
        />
      ))}
    </div>
  );
}

// ── distributions panel ───────────────────────────────────────────────────────
function DistributionPanel({ title, counts, colors }: {
  title: string;
  counts: Record<string, number>;
  colors: Record<string, string>;
}) {
  const total = Object.values(counts).reduce((a, b) => a + b, 0) || 1;
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
      <div className="text-xs text-slate-400 font-medium mb-3">{title}</div>
      <div className="space-y-2">
        {Object.entries(counts).map(([k, v]) => (
          <div key={k}>
            <div className="flex justify-between text-xs mb-1">
              <span className={colors[k] ?? "text-slate-400"}>{k.replace(/_/g, " ")}</span>
              <span className="text-slate-500">{v}</span>
            </div>
            <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
              <div
                className={`h-full rounded-full ${
                  colors[k]?.replace("text-", "bg-").replace("-400", "-500") ?? "bg-slate-500"
                }`}
                style={{ width: `${(v / total) * 100}%` }}
              />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

// ── ProcessModal ──────────────────────────────────────────────────────────────
function ProcessModal({ proc, onClose }: { proc: ProcessRecord; onClose: () => void }) {
  const [tab, setTab] = useState<"overview" | "scores" | "action">("overview");

  useEffect(() => {
    const esc = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", esc);
    return () => window.removeEventListener("keydown", esc);
  }, [onClose]);

  const ringColor =
    proc.quality_composite >= 60 ? "#f43f5e"
    : proc.quality_composite >= 40 ? "#f97316"
    : proc.quality_composite >= 20 ? "#eab308"
    : "#64748b";

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4"
      onClick={onClose}
    >
      <div
        className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-lg shadow-2xl"
        onClick={(e) => e.stopPropagation()}
      >
        {/* header */}
        <div className="flex items-center gap-4 p-5 border-b border-slate-800">
          <CompositeRing score={proc.quality_composite} color={ringColor} />
          <div className="flex-1 min-w-0">
            <h2 className="text-white font-bold text-lg truncate">
              {PROCESS_TYPE_ICON[proc.process_type] ?? "🔧"} {proc.process_type}
            </h2>
            <p className="text-slate-400 text-sm">{proc.process_id} · {proc.region}</p>
            <div className="flex gap-2 mt-1 flex-wrap">
              <span className={`text-xs px-2 py-0.5 rounded-full border ${RISK_BG[proc.quality_risk]}`}>
                {proc.quality_risk} risk
              </span>
              <span className={`text-xs font-medium ${SEVERITY_COLOR[proc.quality_severity]}`}>
                {proc.quality_severity}
              </span>
            </div>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl">✕</button>
        </div>

        {/* tabs */}
        <div className="flex border-b border-slate-800">
          {(["overview", "scores", "action"] as const).map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`flex-1 py-2.5 text-sm font-medium capitalize transition-colors ${
                tab === t
                  ? "text-yellow-400 border-b-2 border-yellow-400"
                  : "text-slate-500 hover:text-slate-300"
              }`}
            >
              {t}
            </button>
          ))}
        </div>

        <div className="p-5 space-y-3">
          {tab === "overview" && (
            <>
              <div className="grid grid-cols-2 gap-3">
                {[
                  ["Pattern",           PATTERN_ICON[proc.quality_pattern] + " " + proc.quality_pattern.replace(/_/g, " ")],
                  ["Risk Index",        proc.estimated_quality_risk_index.toFixed(2) + " / 10"],
                  ["Quality Alert",     proc.has_quality_alert ? "🚨 Yes" : "No"],
                  ["Immediate Action",  proc.requires_immediate_action ? "⚡ Yes" : "No"],
                ].map(([label, value]) => (
                  <div key={label as string} className="bg-slate-800/60 rounded-lg p-3">
                    <div className="text-xs text-slate-400">{label}</div>
                    <div className="text-white font-semibold mt-0.5 text-sm">{value}</div>
                  </div>
                ))}
              </div>
              <div className="bg-slate-800/60 rounded-lg p-3">
                <div className="text-xs text-slate-400 mb-1">Quality Signal</div>
                <div className="text-yellow-300 text-sm leading-relaxed">{proc.quality_signal}</div>
              </div>
            </>
          )}

          {tab === "scores" && (
            <div className="space-y-3">
              <ScoreBar label="Defect"      value={proc.defect_score}     color="bg-rose-500" />
              <ScoreBar label="Process"     value={proc.process_score}    color="bg-orange-500" />
              <ScoreBar label="Compliance"  value={proc.compliance_score} color="bg-yellow-500" />
              <ScoreBar label="Supplier"    value={proc.supplier_score}   color="bg-lime-500" />
            </div>
          )}

          {tab === "action" && (
            <div className="space-y-3">
              <div className="bg-yellow-500/10 border border-yellow-500/30 rounded-xl p-4">
                <div className="text-xs text-yellow-400 uppercase tracking-wide mb-1">Recommended Action</div>
                <div className="text-white font-bold text-lg capitalize">
                  {proc.recommended_action.replace(/_/g, " ")}
                </div>
              </div>
              {proc.requires_immediate_action && (
                <div className="bg-amber-500/10 border border-amber-500/30 rounded-xl p-3 text-sm text-amber-300">
                  ⚡ Immediate action required — escalate to quality team now
                </div>
              )}
              {proc.has_quality_alert && (
                <div className="bg-rose-500/10 border border-rose-500/30 rounded-xl p-3 text-sm text-rose-300">
                  🚨 Quality alert active — initiate corrective action protocol
                </div>
              )}
              {!proc.has_quality_alert && (
                <div className="bg-slate-800/60 rounded-xl p-3 text-sm text-slate-400">
                  ✅ No quality alert — continue routine quality monitoring
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

// ── ProcessCard ───────────────────────────────────────────────────────────────
function ProcessCard({ proc, onClick }: { proc: ProcessRecord; onClick: () => void }) {
  const ringColor =
    proc.quality_composite >= 60 ? "#f43f5e"
    : proc.quality_composite >= 40 ? "#f97316"
    : proc.quality_composite >= 20 ? "#eab308"
    : "#64748b";

  return (
    <div
      onClick={onClick}
      className="bg-slate-900 border border-slate-800 rounded-xl p-4 cursor-pointer hover:border-yellow-700 hover:bg-slate-800/60 transition-all"
    >
      <div className="flex items-center gap-3">
        <CompositeRing score={proc.quality_composite} color={ringColor} />
        <div className="flex-1 min-w-0">
          <div className="text-white font-semibold truncate">
            {PROCESS_TYPE_ICON[proc.process_type] ?? "🔧"} {proc.process_type}
          </div>
          <div className="text-slate-400 text-xs">{proc.process_id} · {proc.region}</div>
          <div className="flex gap-2 mt-1 flex-wrap">
            <span className={`text-xs px-2 py-0.5 rounded-full border ${RISK_BG[proc.quality_risk]}`}>
              {proc.quality_risk}
            </span>
          </div>
        </div>
        <div className="text-right shrink-0">
          {proc.requires_immediate_action && <div className="text-xs text-amber-400">⚡ Action</div>}
          <div className={`text-sm font-bold mt-1 ${SEVERITY_COLOR[proc.quality_severity]}`}>
            {proc.quality_severity}
          </div>
          {proc.has_quality_alert && (
            <div className="text-xs text-rose-400 mt-1">🚨</div>
          )}
        </div>
      </div>
      <div className="mt-2 text-xs text-slate-400">
        {PATTERN_ICON[proc.quality_pattern]} {proc.quality_pattern.replace(/_/g, " ")} · risk idx: {proc.estimated_quality_risk_index.toFixed(2)}
      </div>
    </div>
  );
}

// ── page ─────────────────────────────────────────────────────────────────────
export default function QualityAssuranceProcessEnginePage() {
  const [processes, setProcesses] = useState<ProcessRecord[]>([]);
  const [summary, setSummary]     = useState<Summary | null>(null);
  const [loading, setLoading]     = useState(true);
  const [selected, setSelected]   = useState<ProcessRecord | null>(null);
  const [filterRisk,   setFilterRisk]   = useState("all");
  const [filterRegion, setFilterRegion] = useState("all");

  const load = useCallback(async () => {
    setLoading(true);
    const params = new URLSearchParams();
    if (filterRisk   !== "all") params.set("risk",   filterRisk);
    if (filterRegion !== "all") params.set("region", filterRegion);
    const res  = await fetch(`/api/quality-assurance-process-engine?${params}`);
    const data = await res.json();
    setProcesses(data.processes);
    setSummary(data.summary);
    setLoading(false);
  }, [filterRisk, filterRegion]);

  useEffect(() => { load(); }, [load]);

  const distributions = [
    {
      title: "Risk Distribution",
      counts: summary?.risk_counts ?? {},
      colors: { critical: "text-rose-400", high: "text-orange-400", moderate: "text-yellow-400", low: "text-slate-400" },
    },
    {
      title: "Pattern Distribution",
      counts: summary?.pattern_counts ?? {},
      colors: {
        defect_surge: "text-rose-400", process_deviation: "text-orange-400",
        sla_breach: "text-yellow-400", audit_failure: "text-amber-400",
        supplier_quality_failure: "text-lime-400", none: "text-slate-400",
      },
    },
    {
      title: "Severity Distribution",
      counts: summary?.severity_counts ?? {},
      colors: { critical: "text-rose-400", degraded: "text-orange-400", acceptable: "text-yellow-400", excellent: "text-lime-400" },
    },
  ] as Array<{ title: string; counts: Record<string, number>; colors: Record<string, string> }>;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
      <div className="max-w-6xl mx-auto space-y-6">

        {/* header */}
        <div>
          <h1 className="text-2xl font-bold text-white">Quality Assurance & Process Optimization Engine</h1>
          <p className="text-slate-400 text-sm mt-1">
            Monitors defect rates, process adherence, SLA compliance, audit scores, and supplier quality —
            prescribing the right corrective action before quality degradation becomes customer-impacting
          </p>
        </div>

        {/* KPI strip */}
        {summary && (
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
            {[
              { label: "Processes Tracked",  value: summary.total },
              { label: "Avg QA Composite",   value: summary.avg_quality_composite.toFixed(1), color: "text-yellow-400" },
              { label: "Quality Alerts",     value: summary.quality_alert_count,              color: "text-rose-400" },
              { label: "Immediate Actions",  value: summary.immediate_action_count,           color: "text-amber-400" },
            ].map(({ label, value, color }) => (
              <div key={label} className="bg-slate-900 border border-slate-800 rounded-xl p-4">
                <div className="text-xs text-slate-400">{label}</div>
                <div className={`text-2xl font-bold mt-1 ${color ?? "text-white"}`}>{value}</div>
              </div>
            ))}
          </div>
        )}

        {/* risk distribution bar */}
        {summary && (
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-400 mb-2">Quality Risk Distribution</div>
            <RiskDistBar counts={summary.risk_counts} />
            <div className="flex gap-4 mt-2 text-xs text-slate-500">
              {["critical", "high", "moderate", "low"].map((k) => (
                <span key={k} className={RISK_COLOR[k]}>{k}: {summary.risk_counts[k] || 0}</span>
              ))}
            </div>
          </div>
        )}

        {/* filters */}
        <div className="flex flex-wrap gap-2">
          {[
            { label: "All Risks",   val: "all" },
            { label: "🔴 Critical", val: "critical" },
            { label: "🟠 High",    val: "high" },
            { label: "🟡 Moderate", val: "moderate" },
            { label: "⚫ Low",     val: "low" },
          ].map(({ label, val }) => (
            <button
              key={val}
              onClick={() => setFilterRisk(val)}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
                filterRisk === val
                  ? "bg-yellow-600 text-white"
                  : "bg-slate-800 text-slate-400 hover:text-white"
              }`}
            >
              {label}
            </button>
          ))}
          <select
            value={filterRegion}
            onChange={(e) => setFilterRegion(e.target.value)}
            className="px-3 py-1.5 rounded-lg text-xs bg-slate-800 text-slate-300 border border-slate-700"
          >
            <option value="all">All Regions</option>
            {["NAMER", "EMEA", "APAC", "LATAM", "MEA"].map((r) => (
              <option key={r} value={r}>{r}</option>
            ))}
          </select>
        </div>

        {/* processes grid */}
        {loading ? (
          <div className="text-slate-400 text-center py-16">Scanning quality & process landscape…</div>
        ) : processes.length === 0 ? (
          <div className="text-slate-500 text-center py-16">No processes match your filters.</div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {processes.map((p) => (
              <ProcessCard key={p.process_id} proc={p} onClick={() => setSelected(p)} />
            ))}
          </div>
        )}

        {/* distributions */}
        {summary && (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {distributions.map((d) => (
              <DistributionPanel key={d.title} title={d.title} counts={d.counts} colors={d.colors} />
            ))}
          </div>
        )}

        {/* avg score bars */}
        {summary && (
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
            <div className="text-sm font-semibold text-slate-300 mb-4">Average Sub-Score Breakdown</div>
            <div className="space-y-3">
              <ScoreBar label="Defect"     value={summary.avg_defect_score}     color="bg-rose-500" />
              <ScoreBar label="Process"    value={summary.avg_process_score}    color="bg-orange-500" />
              <ScoreBar label="Compliance" value={summary.avg_compliance_score} color="bg-yellow-500" />
              <ScoreBar label="Supplier"   value={summary.avg_supplier_score}   color="bg-lime-500" />
            </div>
          </div>
        )}
      </div>

      {selected && <ProcessModal proc={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
