"use client";

import { useEffect, useState } from "react";

interface Rep {
  rep_id: string;
  region: string;
  coaching_risk: string;
  coaching_pattern: string;
  coaching_severity: string;
  recommended_action: string;
  coaching_frequency_score: number;
  coaching_impact_score: number;
  coaching_alignment_score: number;
  manager_effectiveness_score: number;
  coaching_effectiveness_composite: number;
  is_coaching_ineffective: boolean;
  requires_coaching_redesign: boolean;
  estimated_revenue_impact_usd: number;
  coaching_signal: string;
}

interface Summary {
  total: number;
  risk_counts: Record<string, number>;
  pattern_counts: Record<string, number>;
  severity_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_coaching_effectiveness_composite: number;
  ineffective_coaching_count: number;
  coaching_redesign_count: number;
  avg_coaching_frequency_score: number;
  avg_coaching_impact_score: number;
  avg_coaching_alignment_score: number;
  avg_manager_effectiveness_score: number;
  total_estimated_revenue_impact_usd: number;
}

const riskColors: Record<string, string> = {
  low: "text-emerald-400",
  moderate: "text-yellow-400",
  high: "text-orange-400",
  critical: "text-red-400",
};
const riskBg: Record<string, string> = {
  low: "bg-emerald-900/30 border-emerald-700",
  moderate: "bg-yellow-900/30 border-yellow-700",
  high: "bg-orange-900/30 border-orange-700",
  critical: "bg-red-900/30 border-red-700",
};
const severityColors: Record<string, string> = {
  effective: "bg-emerald-700",
  developing: "bg-yellow-600",
  stalled: "bg-orange-600",
  regressing: "bg-red-600",
};
const patternLabels: Record<string, string> = {
  none: "None",
  insufficient_frequency: "Insufficient Frequency",
  no_behavioral_change: "No Behavioral Change",
  topic_misalignment: "Topic Misalignment",
  manager_ineffectiveness: "Manager Ineffectiveness",
  coaching_resistance: "Coaching Resistance",
};
const actionLabels: Record<string, string> = {
  no_action: "No Action",
  increase_coaching_frequency: "Increase Coaching Frequency",
  coaching_topic_reset: "Coaching Topic Reset",
  manager_coaching_training: "Manager Coaching Training",
  external_coach_engagement: "External Coach Engagement",
  performance_management: "Performance Management",
};

function RingGauge({ value, color }: { value: number; color: string }) {
  const r = 36;
  const circ = 2 * Math.PI * r;
  const fill = Math.min(value / 100, 1) * circ;
  return (
    <svg width={88} height={88} viewBox="0 0 88 88">
      <circle cx={44} cy={44} r={r} fill="none" stroke="#1e293b" strokeWidth={10} />
      <circle
        cx={44} cy={44} r={r} fill="none" stroke={color} strokeWidth={10}
        strokeDasharray={`${fill} ${circ}`} strokeLinecap="round"
        transform="rotate(-90 44 44)"
      />
      <text x={44} y={49} textAnchor="middle" fill="white" fontSize={14} fontWeight="bold">
        {Math.round(value)}
      </text>
    </svg>
  );
}

function ScoreBar({ label, value, color }: { label: string; value: number; color: string }) {
  return (
    <div className="space-y-1">
      <div className="flex justify-between text-xs text-slate-400">
        <span>{label}</span>
        <span className="text-slate-300 font-medium">{value.toFixed(1)}</span>
      </div>
      <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
        <div className={`h-full rounded-full ${color}`} style={{ width: `${Math.min(value, 100)}%` }} />
      </div>
    </div>
  );
}

function DistributionBar({
  title, counts, colors,
}: {
  title: string; counts: Record<string, number>; colors: Record<string, string>;
}) {
  const total = Object.values(counts).reduce((a, b) => a + b, 0);
  if (!total) return null;
  return (
    <div className="space-y-2">
      <p className="text-xs font-medium text-slate-400 uppercase tracking-wider">{title}</p>
      <div className="flex h-3 rounded-full overflow-hidden gap-0.5">
        {Object.entries(counts).map(([k, v]) => (
          <div key={k} className={`${colors[k] ?? "bg-slate-600"}`} style={{ width: `${(v / total) * 100}%` }} title={`${k}: ${v}`} />
        ))}
      </div>
      <div className="flex flex-wrap gap-2">
        {Object.entries(counts).map(([k, v]) => (
          <span key={k} className="flex items-center gap-1 text-xs text-slate-400">
            <span className={`inline-block w-2 h-2 rounded-full ${colors[k] ?? "bg-slate-600"}`} />
            {k.replace(/_/g, " ")} ({v})
          </span>
        ))}
      </div>
    </div>
  );
}

function DetailModal({ rep, onClose }: { rep: Rep; onClose: () => void }) {
  const [tab, setTab] = useState(0);
  useEffect(() => {
    const h = (e: KeyboardEvent) => e.key === "Escape" && onClose();
    window.addEventListener("keydown", h);
    return () => window.removeEventListener("keydown", h);
  }, [onClose]);
  return (
    <div className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-4" onClick={onClose}>
      <div className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-2xl shadow-2xl" onClick={(e) => e.stopPropagation()}>
        <div className="p-6 border-b border-slate-800">
          <div className="flex items-start justify-between">
            <div>
              <h2 className="text-xl font-bold text-slate-100">{rep.rep_id}</h2>
              <p className="text-sm text-slate-400 mt-0.5">{rep.region} · {patternLabels[rep.coaching_pattern] ?? rep.coaching_pattern}</p>
            </div>
            <div className="flex items-center gap-3">
              <span className={`text-sm font-semibold uppercase ${riskColors[rep.coaching_risk] ?? "text-slate-400"}`}>{rep.coaching_risk}</span>
              <button onClick={onClose} className="text-slate-500 hover:text-slate-200 text-xl leading-none">×</button>
            </div>
          </div>
          <div className="flex gap-2 mt-4">
            {["Scores", "Signals", "Action"].map((t, i) => (
              <button key={t} onClick={() => setTab(i)}
                className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-colors ${tab === i ? "bg-indigo-600 text-white" : "text-slate-400 hover:text-slate-200"}`}>
                {t}
              </button>
            ))}
          </div>
        </div>
        <div className="p-6 space-y-4">
          {tab === 0 && (
            <div className="space-y-4">
              <div className="flex justify-center">
                <div className="text-center">
                  <RingGauge value={rep.coaching_effectiveness_composite}
                    color={rep.coaching_risk === "critical" ? "#ef4444" : rep.coaching_risk === "high" ? "#f97316" : rep.coaching_risk === "moderate" ? "#eab308" : "#10b981"} />
                  <p className="text-xs text-slate-400 mt-1">Composite</p>
                </div>
              </div>
              <div className="grid grid-cols-2 gap-4">
                <ScoreBar label="Frequency Risk" value={rep.coaching_frequency_score} color="bg-blue-500" />
                <ScoreBar label="Impact Risk" value={rep.coaching_impact_score} color="bg-red-500" />
                <ScoreBar label="Alignment Risk" value={rep.coaching_alignment_score} color="bg-yellow-500" />
                <ScoreBar label="Manager Risk" value={rep.manager_effectiveness_score} color="bg-violet-500" />
              </div>
            </div>
          )}
          {tab === 1 && (
            <div className="space-y-3">
              <div className={`border rounded-xl p-4 ${riskBg[rep.coaching_risk] ?? "bg-slate-800 border-slate-700"}`}>
                <p className="text-sm text-slate-200 leading-relaxed">{rep.coaching_signal}</p>
              </div>
              <div className="grid grid-cols-2 gap-3 text-sm">
                <div className="bg-slate-800 rounded-xl p-3">
                  <p className="text-slate-400 text-xs mb-1">Severity</p>
                  <span className={`inline-block px-2 py-0.5 rounded text-white text-xs font-medium ${severityColors[rep.coaching_severity] ?? "bg-slate-600"}`}>
                    {rep.coaching_severity}
                  </span>
                </div>
                <div className="bg-slate-800 rounded-xl p-3">
                  <p className="text-slate-400 text-xs mb-1">Revenue Impact</p>
                  <p className="text-slate-100 font-semibold">${rep.estimated_revenue_impact_usd.toLocaleString()}</p>
                </div>
                <div className="bg-slate-800 rounded-xl p-3">
                  <p className="text-slate-400 text-xs mb-1">Coaching Ineffective</p>
                  <p className={rep.is_coaching_ineffective ? "text-red-400 font-medium" : "text-emerald-400 font-medium"}>
                    {rep.is_coaching_ineffective ? "Yes" : "No"}
                  </p>
                </div>
                <div className="bg-slate-800 rounded-xl p-3">
                  <p className="text-slate-400 text-xs mb-1">Redesign Needed</p>
                  <p className={rep.requires_coaching_redesign ? "text-orange-400 font-medium" : "text-emerald-400 font-medium"}>
                    {rep.requires_coaching_redesign ? "Yes" : "No"}
                  </p>
                </div>
              </div>
            </div>
          )}
          {tab === 2 && (
            <div className="space-y-4">
              <div className="bg-indigo-950 border border-indigo-800 rounded-xl p-4">
                <p className="text-xs text-indigo-400 font-medium uppercase tracking-wider mb-1">Recommended Action</p>
                <p className="text-indigo-200 font-semibold text-lg">{actionLabels[rep.recommended_action] ?? rep.recommended_action}</p>
              </div>
              <div className="bg-slate-800 rounded-xl p-4 space-y-2 text-sm">
                <div className="flex justify-between"><span className="text-slate-400">Pattern</span><span className="text-slate-200">{patternLabels[rep.coaching_pattern] ?? rep.coaching_pattern}</span></div>
                <div className="flex justify-between"><span className="text-slate-400">Risk Level</span><span className={riskColors[rep.coaching_risk] ?? "text-slate-200"}>{rep.coaching_risk}</span></div>
                <div className="flex justify-between"><span className="text-slate-400">Severity</span><span className="text-slate-200">{rep.coaching_severity}</span></div>
                <div className="flex justify-between"><span className="text-slate-400">Composite</span><span className="text-slate-200">{rep.coaching_effectiveness_composite.toFixed(1)}</span></div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default function SalesCoachingEffectivenessPage() {
  const [data, setData] = useState<{ reps: Rep[]; summary: Summary } | null>(null);
  const [riskFilter, setRiskFilter] = useState("");
  const [patternFilter, setPatternFilter] = useState("");
  const [selected, setSelected] = useState<Rep | null>(null);

  useEffect(() => {
    const params = new URLSearchParams();
    if (riskFilter)    params.set("risk", riskFilter);
    if (patternFilter) params.set("pattern", patternFilter);
    fetch(`/api/sales-coaching-effectiveness-engine?${params}`).then((r) => r.json()).then(setData);
  }, [riskFilter, patternFilter]);

  const s = data?.summary;

  const distBars = [
    { title: "Risk Distribution", counts: s?.risk_counts ?? {}, colors: { low: "bg-emerald-500", moderate: "bg-yellow-500", high: "bg-orange-500", critical: "bg-red-500" } as Record<string, string> },
    { title: "Pattern Distribution", counts: s?.pattern_counts ?? {}, colors: { none: "bg-slate-500", insufficient_frequency: "bg-blue-500", no_behavioral_change: "bg-orange-500", topic_misalignment: "bg-yellow-500", manager_ineffectiveness: "bg-violet-500", coaching_resistance: "bg-red-500" } as Record<string, string> },
    { title: "Severity Distribution", counts: s?.severity_counts ?? {}, colors: { effective: "bg-emerald-500", developing: "bg-yellow-500", stalled: "bg-orange-500", regressing: "bg-red-500" } as Record<string, string> },
  ] as Array<{ title: string; counts: Record<string, number>; colors: Record<string, string> }>;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-slate-100">Sales Coaching Effectiveness</h1>
        <p className="text-slate-400 text-sm mt-1">Measure whether coaching drives behavioral change — detect misalignment, manager ineffectiveness, and coaching resistance</p>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {[
          { label: "Total Reps", value: s?.total ?? "—", sub: "evaluated" },
          { label: "Ineffective Coaching", value: s?.ineffective_coaching_count ?? "—", sub: "reps not improving" },
          { label: "Redesign Needed", value: s?.coaching_redesign_count ?? "—", sub: "programs need reset" },
          { label: "Revenue Impact", value: s ? `$${(s.total_estimated_revenue_impact_usd / 1000).toFixed(0)}K` : "—", sub: "from coaching gaps" },
        ].map((k) => (
          <div key={k.label} className="bg-slate-900 border border-slate-800 rounded-2xl p-4">
            <p className="text-xs text-slate-400 uppercase tracking-wider">{k.label}</p>
            <p className="text-3xl font-bold text-slate-100 mt-1">{k.value}</p>
            <p className="text-xs text-slate-500 mt-0.5">{k.sub}</p>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {[
          { label: "Avg Frequency Risk", value: s?.avg_coaching_frequency_score ?? 0, color: "#3b82f6" },
          { label: "Avg Impact Risk", value: s?.avg_coaching_impact_score ?? 0, color: "#ef4444" },
          { label: "Avg Alignment Risk", value: s?.avg_coaching_alignment_score ?? 0, color: "#eab308" },
          { label: "Avg Manager Risk", value: s?.avg_manager_effectiveness_score ?? 0, color: "#8b5cf6" },
        ].map((g) => (
          <div key={g.label} className="bg-slate-900 border border-slate-800 rounded-2xl p-4 flex flex-col items-center gap-2">
            <RingGauge value={g.value} color={g.color} />
            <p className="text-xs text-slate-400 text-center">{g.label}</p>
          </div>
        ))}
      </div>

      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 space-y-5">
        {distBars.map((b) => <DistributionBar key={b.title} {...b} />)}
      </div>

      <div className="flex flex-wrap gap-3">
        <div className="space-y-1">
          <p className="text-xs text-slate-500 uppercase tracking-wider">Risk</p>
          <div className="flex gap-2">
            {["", "low", "moderate", "high", "critical"].map((v) => (
              <button key={v} onClick={() => setRiskFilter(v)}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${riskFilter === v ? "bg-indigo-600 text-white" : "bg-slate-800 text-slate-400 hover:text-slate-200"}`}>
                {v || "All"}
              </button>
            ))}
          </div>
        </div>
        <div className="space-y-1">
          <p className="text-xs text-slate-500 uppercase tracking-wider">Pattern</p>
          <div className="flex flex-wrap gap-2">
            {["", "insufficient_frequency", "no_behavioral_change", "topic_misalignment", "manager_ineffectiveness", "coaching_resistance"].map((v) => (
              <button key={v} onClick={() => setPatternFilter(v)}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${patternFilter === v ? "bg-indigo-600 text-white" : "bg-slate-800 text-slate-400 hover:text-slate-200"}`}>
                {v ? patternLabels[v] : "All"}
              </button>
            ))}
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
        {data?.reps.map((rep) => (
          <button key={rep.rep_id} onClick={() => setSelected(rep)}
            className={`text-left border rounded-2xl p-4 space-y-3 hover:border-indigo-500 transition-colors ${riskBg[rep.coaching_risk] ?? "bg-slate-900 border-slate-800"}`}>
            <div className="flex items-start justify-between">
              <div>
                <p className="font-semibold text-slate-100">{rep.rep_id}</p>
                <p className="text-xs text-slate-400">{rep.region}</p>
              </div>
              <div className="flex flex-col items-end gap-1">
                <span className={`text-xs font-bold uppercase ${riskColors[rep.coaching_risk] ?? "text-slate-400"}`}>{rep.coaching_risk}</span>
                <span className={`inline-block px-1.5 py-0.5 rounded text-white text-xs ${severityColors[rep.coaching_severity] ?? "bg-slate-600"}`}>{rep.coaching_severity}</span>
              </div>
            </div>
            <div className="space-y-1.5">
              <ScoreBar label="Frequency" value={rep.coaching_frequency_score} color="bg-blue-500" />
              <ScoreBar label="Impact" value={rep.coaching_impact_score} color="bg-red-500" />
              <ScoreBar label="Alignment" value={rep.coaching_alignment_score} color="bg-yellow-500" />
              <ScoreBar label="Manager" value={rep.manager_effectiveness_score} color="bg-violet-500" />
            </div>
            <div className="flex items-center justify-between text-xs">
              <span className="text-slate-400 truncate max-w-[70%]">{patternLabels[rep.coaching_pattern] ?? rep.coaching_pattern}</span>
              <span className="text-indigo-400 font-medium">composite {rep.coaching_effectiveness_composite.toFixed(1)}</span>
            </div>
            {rep.estimated_revenue_impact_usd > 0 && (
              <div className="text-xs text-red-400 font-medium">${rep.estimated_revenue_impact_usd.toLocaleString()} revenue impact</div>
            )}
            <p className="text-xs text-slate-500 line-clamp-2">{rep.coaching_signal}</p>
          </button>
        ))}
      </div>

      {selected && <DetailModal rep={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
