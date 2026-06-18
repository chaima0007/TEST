"use client";

import { useState, useEffect, useRef, useCallback } from "react";

interface Rep {
  rep_id: string;
  region: string;
  meeting_risk: string;
  meeting_pattern: string;
  meeting_severity: string;
  recommended_action: string;
  meeting_preparation_score: number;
  meeting_outcome_score: number;
  stakeholder_coverage_score: number;
  meeting_discipline_score: number;
  meeting_quality_composite: number;
  has_meeting_effectiveness_gap: boolean;
  requires_coaching_intervention: boolean;
  estimated_revenue_at_risk_usd: number;
  meeting_signal: string;
}

interface Summary {
  total: number;
  risk_counts: Record<string, number>;
  pattern_counts: Record<string, number>;
  severity_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_meeting_quality_composite: number;
  effectiveness_gap_count: number;
  coaching_intervention_count: number;
  avg_meeting_preparation_score: number;
  avg_meeting_outcome_score: number;
  avg_stakeholder_coverage_score: number;
  avg_meeting_discipline_score: number;
  total_estimated_revenue_at_risk_usd: number;
}

const RISK_COLORS: Record<string, string> = {
  low:      "text-emerald-400",
  moderate: "text-amber-400",
  high:     "text-orange-400",
  critical: "text-red-400",
};

const RISK_BG: Record<string, string> = {
  low:      "bg-emerald-400",
  moderate: "bg-amber-400",
  high:     "bg-orange-400",
  critical: "bg-red-400",
};

const SEV_COLORS: Record<string, string> = {
  effective:   "text-emerald-400",
  developing:  "text-amber-400",
  ineffective: "text-orange-400",
  detrimental: "text-red-400",
};

const PATTERN_COLORS: Record<string, string> = {
  none:                 "bg-slate-600",
  poor_preparation:     "bg-yellow-500",
  no_deal_advancement:  "bg-red-500",
  wrong_stakeholders:   "bg-orange-500",
  poor_follow_through:  "bg-amber-500",
  pipeline_stall:       "bg-violet-500",
};

function fmtUsd(n: number) {
  if (n >= 1_000_000) return `$${(n / 1_000_000).toFixed(1)}M`;
  if (n >= 1_000)     return `$${(n / 1_000).toFixed(0)}K`;
  return `$${n.toFixed(0)}`;
}

function fmtLabel(s: string) {
  return s.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
}

function GaugeRing({ score, label, color }: { score: number; label: string; color: string }) {
  const r = 36;
  const circ = 2 * Math.PI * r;
  const filled = circ * (1 - score / 100);
  return (
    <div className="flex flex-col items-center gap-1">
      <svg width="96" height="96" viewBox="0 0 96 96">
        <circle cx="48" cy="48" r={r} fill="none" stroke="#1e293b" strokeWidth="10" />
        <circle cx="48" cy="48" r={r} fill="none" stroke={color} strokeWidth="10"
          strokeDasharray={circ} strokeDashoffset={filled} strokeLinecap="round"
          transform="rotate(-90 48 48)" />
        <text x="48" y="53" textAnchor="middle" fill="white" fontSize="15" fontWeight="bold">
          {score.toFixed(0)}
        </text>
      </svg>
      <span className="text-xs text-slate-400 text-center leading-tight">{label}</span>
    </div>
  );
}

function ScoreBar({ label, value, color }: { label: string; value: number; color: string }) {
  return (
    <div className="space-y-0.5">
      <div className="flex justify-between text-xs">
        <span className="text-slate-400">{label}</span>
        <span className="text-slate-300">{value.toFixed(0)}</span>
      </div>
      <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
        <div className={`h-full rounded-full ${color}`} style={{ width: `${Math.min(value, 100)}%` }} />
      </div>
    </div>
  );
}

function DistBar({ title, counts, colors }: { title: string; counts: Record<string, number>; colors: Record<string, string> }) {
  const total = Object.values(counts).reduce((a, b) => a + b, 0) || 1;
  return (
    <div className="space-y-2">
      <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider">{title}</p>
      <div className="flex h-3 rounded-full overflow-hidden gap-px">
        {Object.entries(counts).map(([k, v]) => (
          <div key={k} className={`${colors[k] || "bg-slate-600"}`} style={{ width: `${(v / total) * 100}%` }} title={`${k}: ${v}`} />
        ))}
      </div>
      <div className="flex flex-wrap gap-x-3 gap-y-1">
        {Object.entries(counts).map(([k, v]) => (
          <span key={k} className="flex items-center gap-1 text-xs text-slate-400">
            <span className={`inline-block w-2 h-2 rounded-sm ${colors[k] || "bg-slate-600"}`} />
            {fmtLabel(k)} ({v})
          </span>
        ))}
      </div>
    </div>
  );
}

function DetailModal({ rep, onClose }: { rep: Rep; onClose: () => void }) {
  const [tab, setTab] = useState<"scores" | "signals" | "action">("scores");
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handler = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [onClose]);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4"
      onClick={(e) => { if (ref.current && !ref.current.contains(e.target as Node)) onClose(); }}>
      <div ref={ref} className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-lg shadow-2xl overflow-hidden">
        <div className="flex items-center justify-between px-6 py-4 border-b border-slate-800">
          <div>
            <p className="font-bold text-slate-100 text-lg">{rep.rep_id}</p>
            <p className="text-sm text-slate-400">{rep.region} — <span className={RISK_COLORS[rep.meeting_risk]}>{fmtLabel(rep.meeting_risk)} risk</span></p>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-slate-200 text-xl font-bold">×</button>
        </div>

        <div className="flex border-b border-slate-800">
          {(["scores", "signals", "action"] as const).map((t) => (
            <button key={t} onClick={() => setTab(t)}
              className={`flex-1 py-2.5 text-sm font-medium capitalize transition-colors ${tab === t ? "text-indigo-400 border-b-2 border-indigo-400" : "text-slate-500 hover:text-slate-300"}`}>
              {t}
            </button>
          ))}
        </div>

        <div className="px-6 py-5 space-y-4 max-h-96 overflow-y-auto">
          {tab === "scores" && (
            <>
              <div className="flex justify-center">
                <GaugeRing score={rep.meeting_quality_composite} label="Composite Risk" color="#f87171" />
              </div>
              <div className="space-y-3 mt-2">
                <ScoreBar label="Preparation" value={rep.meeting_preparation_score} color="bg-indigo-500" />
                <ScoreBar label="Deal Outcome" value={rep.meeting_outcome_score} color="bg-violet-500" />
                <ScoreBar label="Stakeholder Coverage" value={rep.stakeholder_coverage_score} color="bg-amber-500" />
                <ScoreBar label="Follow-through Discipline" value={rep.meeting_discipline_score} color="bg-emerald-500" />
              </div>
              <div className="grid grid-cols-2 gap-3 pt-2 text-xs">
                <div className="bg-slate-800 rounded-lg p-3">
                  <p className="text-slate-500">Revenue at Risk</p>
                  <p className="text-lg font-bold text-red-400">{fmtUsd(rep.estimated_revenue_at_risk_usd)}</p>
                </div>
                <div className="bg-slate-800 rounded-lg p-3">
                  <p className="text-slate-500">Severity</p>
                  <p className={`text-sm font-semibold ${SEV_COLORS[rep.meeting_severity]}`}>{fmtLabel(rep.meeting_severity)}</p>
                </div>
              </div>
            </>
          )}

          {tab === "signals" && (
            <div className="space-y-3">
              <div className="bg-slate-800 rounded-lg p-4">
                <p className="text-xs text-slate-500 mb-1">Meeting Signal</p>
                <p className="text-sm text-slate-200">{rep.meeting_signal}</p>
              </div>
              <div className="bg-slate-800 rounded-lg p-4 space-y-2 text-xs">
                <div className="flex justify-between"><span className="text-slate-400">Pattern</span><span className="text-slate-200">{fmtLabel(rep.meeting_pattern)}</span></div>
                <div className="flex justify-between"><span className="text-slate-400">Effectiveness Gap</span><span className={rep.has_meeting_effectiveness_gap ? "text-red-400" : "text-emerald-400"}>{rep.has_meeting_effectiveness_gap ? "Yes" : "No"}</span></div>
                <div className="flex justify-between"><span className="text-slate-400">Coaching Needed</span><span className={rep.requires_coaching_intervention ? "text-amber-400" : "text-emerald-400"}>{rep.requires_coaching_intervention ? "Required" : "Not required"}</span></div>
              </div>
            </div>
          )}

          {tab === "action" && (
            <div className="space-y-3">
              <div className="bg-indigo-900/40 border border-indigo-700/50 rounded-lg p-4">
                <p className="text-xs text-indigo-400 mb-1 uppercase tracking-wider">Recommended Action</p>
                <p className="text-sm font-semibold text-indigo-200">{fmtLabel(rep.recommended_action)}</p>
              </div>
              <div className="bg-slate-800 rounded-lg p-4 text-xs space-y-2">
                <p className="text-slate-400">Based on <span className={RISK_COLORS[rep.meeting_risk]}>{fmtLabel(rep.meeting_risk)} risk</span> level and <span className="text-slate-200">{fmtLabel(rep.meeting_pattern)}</span> pattern.</p>
                <p className="text-slate-400">Severity: <span className={SEV_COLORS[rep.meeting_severity]}>{fmtLabel(rep.meeting_severity)}</span></p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default function MeetingQualityPage() {
  const [data, setData]             = useState<{ reps: Rep[]; summary: Summary } | null>(null);
  const [loading, setLoading]       = useState(true);
  const [riskFilter, setRisk]       = useState("");
  const [patternFilter, setPattern] = useState("");
  const [selected, setSelected]     = useState<Rep | null>(null);

  const load = useCallback(async () => {
    setLoading(true);
    const params = new URLSearchParams();
    if (riskFilter)    params.set("risk", riskFilter);
    if (patternFilter) params.set("pattern", patternFilter);
    const res = await fetch(`/api/sales-meeting-quality-intelligence-engine?${params}`);
    const json = await res.json();
    setData(json);
    setLoading(false);
  }, [riskFilter, patternFilter]);

  useEffect(() => { load(); }, [load]);

  const s = data?.summary;

  const distributions = [
    { title: "Risk Distribution", counts: s?.risk_counts ?? {}, colors: { low: "bg-emerald-500", moderate: "bg-amber-500", high: "bg-orange-500", critical: "bg-red-500" } as Record<string,string> },
    { title: "Pattern Distribution", counts: s?.pattern_counts ?? {}, colors: PATTERN_COLORS as Record<string,string> },
    { title: "Severity Distribution", counts: s?.severity_counts ?? {}, colors: { effective: "bg-emerald-500", developing: "bg-amber-500", ineffective: "bg-orange-500", detrimental: "bg-red-500" } as Record<string,string> },
  ] as Array<{ title: string; counts: Record<string,number>; colors: Record<string,string> }>;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-slate-100">Meeting Quality Intelligence</h1>
        <p className="text-slate-400 text-sm mt-1">Rep-level meeting preparation, outcome, stakeholder coverage and follow-through scoring</p>
      </div>

      {/* KPI strip */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        {[
          { label: "Total Reps", value: s?.total ?? "—", sub: "evaluated" },
          { label: "Effectiveness Gaps", value: s?.effectiveness_gap_count ?? "—", sub: "reps flagged" },
          { label: "Need Coaching", value: s?.coaching_intervention_count ?? "—", sub: "intervention required" },
          { label: "Revenue at Risk", value: s ? fmtUsd(s.total_estimated_revenue_at_risk_usd) : "—", sub: "stalled in meetings" },
        ].map((k) => (
          <div key={k.label} className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <p className="text-xs text-slate-500 uppercase tracking-wider">{k.label}</p>
            <p className="text-3xl font-bold text-slate-100 mt-1">{k.value}</p>
            <p className="text-xs text-slate-500 mt-0.5">{k.sub}</p>
          </div>
        ))}
      </div>

      {/* Gauge rings */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
        <p className="text-sm font-semibold text-slate-300 mb-4">Average Sub-Scores (Risk Level)</p>
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 justify-items-center">
          <GaugeRing score={s?.avg_meeting_preparation_score ?? 0} label="Preparation" color="#6366f1" />
          <GaugeRing score={s?.avg_meeting_outcome_score ?? 0} label="Deal Outcome" color="#8b5cf6" />
          <GaugeRing score={s?.avg_stakeholder_coverage_score ?? 0} label="Stakeholder Coverage" color="#f59e0b" />
          <GaugeRing score={s?.avg_meeting_discipline_score ?? 0} label="Follow-through" color="#10b981" />
        </div>
      </div>

      {/* Distribution bars */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {distributions.map((d) => (
          <div key={d.title} className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <DistBar {...d} />
          </div>
        ))}
      </div>

      {/* Filters */}
      <div className="flex flex-wrap gap-3 items-center">
        <span className="text-xs text-slate-500 uppercase tracking-wider">Filter:</span>
        <div className="flex gap-2 flex-wrap">
          {["", "low", "moderate", "high", "critical"].map((v) => (
            <button key={v} onClick={() => setRisk(v)}
              className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${riskFilter === v ? "bg-indigo-600 border-indigo-500 text-white" : "border-slate-700 text-slate-400 hover:text-slate-200"}`}>
              {v ? fmtLabel(v) : "All Risk"}
            </button>
          ))}
        </div>
        <div className="flex gap-2 flex-wrap">
          {["", "none", "poor_preparation", "no_deal_advancement", "wrong_stakeholders", "poor_follow_through", "pipeline_stall"].map((v) => (
            <button key={v} onClick={() => setPattern(v)}
              className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${patternFilter === v ? "bg-violet-600 border-violet-500 text-white" : "border-slate-700 text-slate-400 hover:text-slate-200"}`}>
              {v ? fmtLabel(v) : "All Patterns"}
            </button>
          ))}
        </div>
      </div>

      {/* Rep cards */}
      {loading ? (
        <div className="text-center py-16 text-slate-500">Loading...</div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
          {(data?.reps ?? []).map((rep) => (
            <div key={rep.rep_id} onClick={() => setSelected(rep)}
              className="bg-slate-900 border border-slate-800 rounded-xl p-4 cursor-pointer hover:border-indigo-600 transition-colors space-y-3">
              <div className="flex items-start justify-between">
                <div>
                  <p className="font-semibold text-slate-100">{rep.rep_id}</p>
                  <p className="text-xs text-slate-400">{rep.region}</p>
                </div>
                <div className="text-right">
                  <span className={`text-xs font-bold uppercase ${RISK_COLORS[rep.meeting_risk]}`}>{rep.meeting_risk}</span>
                  <p className="text-xs text-slate-500">{fmtLabel(rep.meeting_pattern)}</p>
                </div>
              </div>

              <div className="space-y-1.5">
                <ScoreBar label="Preparation" value={rep.meeting_preparation_score} color="bg-indigo-500" />
                <ScoreBar label="Deal Outcome" value={rep.meeting_outcome_score} color="bg-violet-500" />
                <ScoreBar label="Stakeholder Coverage" value={rep.stakeholder_coverage_score} color="bg-amber-500" />
                <ScoreBar label="Follow-through" value={rep.meeting_discipline_score} color="bg-emerald-500" />
              </div>

              <div className="flex items-center justify-between pt-1">
                <div className="flex items-center gap-2">
                  <div className={`w-2 h-2 rounded-full ${RISK_BG[rep.meeting_risk]}`} />
                  <span className="text-xs text-slate-400">Composite {rep.meeting_quality_composite.toFixed(0)}</span>
                </div>
                {rep.estimated_revenue_at_risk_usd > 0 && (
                  <span className="text-xs text-red-400 font-medium">{fmtUsd(rep.estimated_revenue_at_risk_usd)}</span>
                )}
              </div>

              <p className="text-xs text-slate-500 leading-relaxed truncate">{rep.meeting_signal}</p>
            </div>
          ))}
        </div>
      )}

      {selected && <DetailModal rep={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
