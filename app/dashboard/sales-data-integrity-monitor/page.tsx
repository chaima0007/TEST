"use client";

import { useState, useEffect, useCallback } from "react";

interface RecordData {
  record_id: string;
  rep_id: string;
  integrity_risk: string;
  anomaly_type: string;
  data_quality: string;
  integrity_action: string;
  pipeline_accuracy_score: number;
  data_completeness_score: number;
  behavioral_consistency_score: number;
  compliance_score: number;
  integrity_composite: number;
  risk_signal_count: number;
  is_clean: boolean;
  needs_escalation: boolean;
  primary_integrity_signal: string;
}

interface Summary {
  total: number;
  risk_counts: Record<string, number>;
  anomaly_counts: Record<string, number>;
  quality_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_integrity_composite: number;
  clean_count: number;
  escalation_count: number;
  avg_pipeline_accuracy_score: number;
  avg_data_completeness_score: number;
  avg_behavioral_consistency_score: number;
  avg_compliance_score: number;
  high_risk_rep_count: number;
}

const RISK_BG: Record<string, string> = {
  clean: "bg-emerald-500/20 text-emerald-300 border-emerald-500/30",
  minor_issues: "bg-yellow-500/20 text-yellow-300 border-yellow-500/30",
  moderate_issues: "bg-orange-500/20 text-orange-300 border-orange-500/30",
  critical_breach: "bg-rose-500/20 text-rose-300 border-rose-500/30",
};

const RISK_COLOR: Record<string, string> = {
  clean: "bg-emerald-500",
  minor_issues: "bg-yellow-500",
  moderate_issues: "bg-orange-500",
  critical_breach: "bg-rose-500",
};

const QUALITY_BG: Record<string, string> = {
  excellent: "bg-emerald-500/20 text-emerald-300 border-emerald-500/30",
  good: "bg-sky-500/20 text-sky-300 border-sky-500/30",
  fair: "bg-yellow-500/20 text-yellow-300 border-yellow-500/30",
  poor: "bg-rose-500/20 text-rose-300 border-rose-500/30",
};

function fmtLabel(s: string): string {
  return s.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
}

function IntegrityRing({ score, label, color }: { score: number; label: string; color: string }) {
  const r = 30, cx = 36, cy = 36, stroke = 5;
  const circ = 2 * Math.PI * r;
  const fill = (score / 100) * circ;
  return (
    <div className="flex flex-col items-center gap-1">
      <svg width={72} height={72} viewBox="0 0 72 72">
        <circle cx={cx} cy={cy} r={r} fill="none" stroke="#1e293b" strokeWidth={stroke} />
        <circle cx={cx} cy={cy} r={r} fill="none" stroke={color} strokeWidth={stroke}
          strokeDasharray={`${fill} ${circ}`} strokeLinecap="round"
          transform={`rotate(-90 ${cx} ${cy})`} />
        <text x={cx} y={cy + 1} textAnchor="middle" dominantBaseline="middle"
          fill="white" fontSize={11} fontWeight={700}>{Math.round(score)}</text>
      </svg>
      <p className="text-xs text-slate-400 text-center leading-tight">{label}</p>
    </div>
  );
}

function RiskDistBar({ counts }: { counts: Record<string, number> }) {
  const order = ["clean", "minor_issues", "moderate_issues", "critical_breach"];
  const total = Object.values(counts).reduce((s, v) => s + v, 0) || 1;
  return (
    <div className="space-y-2">
      <div className="flex rounded-full overflow-hidden h-3">
        {order.filter((o) => counts[o]).map((o) => (
          <div key={o} className={`${RISK_COLOR[o]} transition-all`}
            style={{ width: `${(counts[o] / total) * 100}%` }} />
        ))}
      </div>
      <div className="flex flex-wrap gap-3">
        {order.filter((o) => counts[o]).map((o) => (
          <span key={o} className="flex items-center gap-1 text-xs text-slate-400">
            <span className={`w-2 h-2 rounded-full ${RISK_COLOR[o]}`} />
            {fmtLabel(o)} ({counts[o]})
          </span>
        ))}
      </div>
    </div>
  );
}

function RecordModal({ record, onClose }: { record: RecordData; onClose: () => void }) {
  const [tab, setTab] = useState<"scores" | "signals" | "actions">("scores");

  useEffect(() => {
    const handler = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [onClose]);

  const scoreColor = (v: number) => v >= 80 ? "#22c55e" : v >= 60 ? "#f59e0b" : v >= 40 ? "#f97316" : "#ef4444";

  return (
    <div className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-4"
      onClick={onClose}>
      <div className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-xl shadow-2xl"
        onClick={(e) => e.stopPropagation()}>
        <div className="p-6 border-b border-slate-800">
          <div className="flex items-start justify-between gap-3">
            <div>
              <h2 className="text-lg font-bold text-white">{record.rep_id}</h2>
              <p className="text-sm text-slate-400 mt-0.5">Record {record.record_id} · {record.risk_signal_count} risk signals detected</p>
            </div>
            <div className="flex flex-col items-end gap-1">
              <span className={`text-xs px-2 py-0.5 rounded-full border ${RISK_BG[record.integrity_risk]}`}>
                {fmtLabel(record.integrity_risk)}
              </span>
              <span className={`text-xs px-2 py-0.5 rounded-full border ${QUALITY_BG[record.data_quality]}`}>
                {fmtLabel(record.data_quality)} quality
              </span>
            </div>
          </div>
          <div className="flex gap-2 mt-4">
            {(["scores", "signals", "actions"] as const).map((t) => (
              <button key={t} onClick={() => setTab(t)}
                className={`px-3 py-1 rounded-lg text-sm font-medium transition-colors ${
                  tab === t ? "bg-violet-600 text-white" : "text-slate-400 hover:text-white"
                }`}>{t.charAt(0).toUpperCase() + t.slice(1)}</button>
            ))}
          </div>
        </div>
        <div className="p-6 space-y-4">
          {tab === "scores" && (
            <div>
              <div className="grid grid-cols-4 gap-3 mb-4">
                <IntegrityRing score={record.pipeline_accuracy_score} label="Pipeline" color={scoreColor(record.pipeline_accuracy_score)} />
                <IntegrityRing score={record.data_completeness_score} label="Completeness" color={scoreColor(record.data_completeness_score)} />
                <IntegrityRing score={record.behavioral_consistency_score} label="Behavioral" color={scoreColor(record.behavioral_consistency_score)} />
                <IntegrityRing score={record.compliance_score} label="Compliance" color={scoreColor(record.compliance_score)} />
              </div>
              <div className="bg-slate-800/50 rounded-xl p-4 flex items-center justify-between">
                <div>
                  <p className="text-xs text-slate-400">Integrity Composite</p>
                  <p className={`text-3xl font-bold ${record.integrity_composite >= 80 ? "text-emerald-400" : record.integrity_composite >= 60 ? "text-yellow-400" : "text-rose-400"}`}>
                    {record.integrity_composite.toFixed(1)}
                  </p>
                </div>
                <div className="text-right">
                  <p className="text-xs text-slate-400">Risk Signals</p>
                  <p className={`text-3xl font-bold ${record.risk_signal_count === 0 ? "text-emerald-400" : record.risk_signal_count <= 2 ? "text-yellow-400" : "text-rose-400"}`}>
                    {record.risk_signal_count}
                  </p>
                </div>
              </div>
            </div>
          )}
          {tab === "signals" && (
            <div className="space-y-3">
              <div className={`rounded-xl p-4 border ${record.needs_escalation ? "bg-rose-600/10 border-rose-500/30" : "bg-slate-800/50 border-slate-700"}`}>
                <p className={`text-xs mb-1 ${record.needs_escalation ? "text-rose-300" : "text-slate-400"}`}>
                  Primary Integrity Signal
                </p>
                <p className="text-sm text-white font-medium">{record.primary_integrity_signal}</p>
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div className="bg-slate-800/50 rounded-xl p-3">
                  <p className="text-xs text-slate-400">Anomaly Type</p>
                  <p className="text-sm font-medium text-white mt-0.5">{fmtLabel(record.anomaly_type)}</p>
                </div>
                <div className="bg-slate-800/50 rounded-xl p-3">
                  <p className="text-xs text-slate-400">Risk Level</p>
                  <span className={`text-xs px-1.5 py-0.5 rounded border ${RISK_BG[record.integrity_risk]}`}>
                    {fmtLabel(record.integrity_risk)}
                  </span>
                </div>
              </div>
              <div className="flex gap-2 flex-wrap">
                {record.is_clean && (
                  <span className="text-xs px-2 py-1 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
                    Data Clean
                  </span>
                )}
                {record.needs_escalation && (
                  <span className="text-xs px-2 py-1 rounded-full bg-rose-500/20 text-rose-300 border border-rose-500/30">
                    Needs Escalation
                  </span>
                )}
              </div>
            </div>
          )}
          {tab === "actions" && (
            <div className="space-y-3">
              <div className={`rounded-xl p-4 border ${
                record.integrity_action === "compliance_escalation"
                  ? "bg-rose-600/20 border-rose-500/30"
                  : record.integrity_action === "manager_alert"
                  ? "bg-orange-600/20 border-orange-500/30"
                  : "bg-violet-600/20 border-violet-500/30"
              }`}>
                <p className="text-xs text-slate-300 mb-1">Recommended Action</p>
                <p className="text-sm font-semibold text-white">{fmtLabel(record.integrity_action)}</p>
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div className="bg-slate-800/50 rounded-xl p-3">
                  <p className="text-xs text-slate-400">Data Quality</p>
                  <span className={`text-xs px-1.5 py-0.5 rounded border ${QUALITY_BG[record.data_quality]}`}>
                    {fmtLabel(record.data_quality)}
                  </span>
                </div>
                <div className="bg-slate-800/50 rounded-xl p-3">
                  <p className="text-xs text-slate-400">Risk Signals</p>
                  <p className={`text-base font-bold ${record.risk_signal_count === 0 ? "text-emerald-400" : "text-rose-400"}`}>
                    {record.risk_signal_count}
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

function RecordCard({ record, onClick }: { record: RecordData; onClick: () => void }) {
  const ringColor = record.integrity_composite >= 80 ? "#22c55e"
    : record.integrity_composite >= 60 ? "#f59e0b"
    : record.integrity_composite >= 40 ? "#f97316"
    : "#ef4444";
  const r = 26, cx = 30, cy = 30, stroke = 5;
  const circ = 2 * Math.PI * r;
  const fill = (record.integrity_composite / 100) * circ;

  return (
    <div onClick={onClick}
      className="bg-slate-900 border border-slate-800 rounded-xl p-4 cursor-pointer hover:border-violet-500/50 transition-all hover:bg-slate-800/50 group">
      <div className="flex items-start gap-3 mb-3">
        <svg width={60} height={60} viewBox="0 0 60 60" className="flex-shrink-0">
          <circle cx={cx} cy={cy} r={r} fill="none" stroke="#1e293b" strokeWidth={stroke} />
          <circle cx={cx} cy={cy} r={r} fill="none" stroke={ringColor} strokeWidth={stroke}
            strokeDasharray={`${fill} ${circ}`} strokeLinecap="round"
            transform={`rotate(-90 ${cx} ${cy})`} />
          <text x={cx} y={cy + 1} textAnchor="middle" dominantBaseline="middle"
            fill="white" fontSize={10} fontWeight={700}>{Math.round(record.integrity_composite)}</text>
        </svg>
        <div className="flex-1 min-w-0">
          <p className="font-semibold text-white truncate group-hover:text-violet-300 transition-colors">
            {record.rep_id}
          </p>
          <p className="text-xs text-slate-400 mt-0.5">{record.risk_signal_count} risk signals</p>
          <div className="flex flex-wrap gap-1 mt-1.5">
            <span className={`text-xs px-1.5 py-0.5 rounded border ${RISK_BG[record.integrity_risk]}`}>
              {fmtLabel(record.integrity_risk)}
            </span>
            <span className={`text-xs px-1.5 py-0.5 rounded border ${QUALITY_BG[record.data_quality]}`}>
              {fmtLabel(record.data_quality)}
            </span>
          </div>
        </div>
      </div>
      <p className="text-xs text-slate-400 line-clamp-2 mb-2">{record.primary_integrity_signal}</p>
      <div className="flex items-center justify-between text-xs">
        <span className={`font-medium ${record.is_clean ? "text-emerald-400" : "text-orange-400"}`}>
          {record.is_clean ? "Clean" : `${record.risk_signal_count} signals`}
        </span>
        {record.needs_escalation && (
          <span className="px-1.5 py-0.5 rounded bg-rose-500/20 text-rose-300 border border-rose-500/30">
            Escalate
          </span>
        )}
      </div>
    </div>
  );
}

export default function SalesDataIntegrityMonitorPage() {
  const [data, setData] = useState<{ records: RecordData[]; summary: Summary } | null>(null);
  const [selected, setSelected] = useState<RecordData | null>(null);
  const [filterRisk, setFilterRisk] = useState("all");
  const [filterQuality, setFilterQuality] = useState("all");

  const load = useCallback(async () => {
    const params = new URLSearchParams();
    if (filterRisk !== "all") params.set("risk", filterRisk);
    if (filterQuality !== "all") params.set("quality", filterQuality);
    const res = await fetch(`/api/sales-data-integrity-monitor?${params}`);
    if (res.ok) setData(await res.json());
  }, [filterRisk, filterQuality]);

  useEffect(() => { load(); }, [load]);

  const s = data?.summary;
  const kpis = [
    { label: "Total Records", value: s?.total ?? 0, sub: "monitored" },
    { label: "Clean Records", value: s?.clean_count ?? 0, sub: "no issues", color: "text-emerald-400" },
    { label: "Escalations", value: s?.escalation_count ?? 0, sub: "critical breach", color: "text-rose-400" },
    { label: "High Risk Reps", value: s?.high_risk_rep_count ?? 0, sub: "critical breach", color: "text-rose-400" },
    { label: "Avg Composite", value: `${s?.avg_integrity_composite ?? 0}`, sub: "/ 100" },
    { label: "Avg Compliance", value: `${s?.avg_compliance_score ?? 0}`, sub: "security score", color: (s?.avg_compliance_score ?? 100) < 70 ? "text-rose-400" : "text-emerald-400" },
  ];

  const riskFilters = ["all", "clean", "minor_issues", "moderate_issues", "critical_breach"];
  const qualityFilters = ["all", "excellent", "good", "fair", "poor"];

  return (
    <main className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white">Sales Data Integrity Monitor</h1>
        <p className="text-sm text-slate-400 mt-1">Detect CRM anomalies, pipeline manipulation, and data integrity breaches</p>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {kpis.map(({ label, value, sub, color }) => (
          <div key={label} className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <p className="text-xs text-slate-400">{label}</p>
            <p className={`text-2xl font-bold mt-1 ${color ?? "text-white"}`}>{value}</p>
            <p className="text-xs text-slate-500 mt-0.5">{sub}</p>
          </div>
        ))}
      </div>

      {s && (
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
          <p className="text-sm font-medium text-slate-300 mb-3">Integrity Risk Distribution</p>
          <RiskDistBar counts={s.risk_counts} />
        </div>
      )}

      <div className="flex flex-wrap gap-3">
        <div className="flex flex-wrap gap-1">
          <span className="text-xs text-slate-500 self-center mr-1">Risk:</span>
          {riskFilters.map((f) => (
            <button key={f} onClick={() => setFilterRisk(f)}
              className={`text-xs px-3 py-1.5 rounded-lg border transition-colors ${
                filterRisk === f
                  ? "bg-violet-600 border-violet-500 text-white"
                  : "border-slate-700 text-slate-400 hover:border-slate-500"
              }`}>
              {f === "all" ? "All" : fmtLabel(f)}
            </button>
          ))}
        </div>
        <div className="flex flex-wrap gap-1">
          <span className="text-xs text-slate-500 self-center mr-1">Quality:</span>
          {qualityFilters.map((f) => (
            <button key={f} onClick={() => setFilterQuality(f)}
              className={`text-xs px-3 py-1.5 rounded-lg border transition-colors ${
                filterQuality === f
                  ? "bg-indigo-600 border-indigo-500 text-white"
                  : "border-slate-700 text-slate-400 hover:border-slate-500"
              }`}>
              {f === "all" ? "All" : fmtLabel(f)}
            </button>
          ))}
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {data?.records.map((r) => (
          <RecordCard key={r.record_id} record={r} onClick={() => setSelected(r)} />
        ))}
        {data?.records.length === 0 && (
          <div className="col-span-full text-center text-slate-500 py-12">No records match the selected filters.</div>
        )}
      </div>

      {selected && <RecordModal record={selected} onClose={() => setSelected(null)} />}
    </main>
  );
}
