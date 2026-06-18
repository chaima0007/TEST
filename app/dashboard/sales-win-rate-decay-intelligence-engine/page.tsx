"use client";

import { useEffect, useState, useCallback } from "react";

// ─── Types ───────────────────────────────────────────────────────────────────

interface Rep {
  rep_id: string;
  region: string;
  decay_risk: string;
  decay_pattern: string;
  decay_severity: string;
  recommended_action: string;
  trajectory_score: number;
  competitive_score: number;
  deal_quality_score: number;
  late_stage_score: number;
  decay_composite: number;
  has_decay_gap: boolean;
  requires_decay_coaching: boolean;
  estimated_revenue_decay_usd: number;
  decay_signal: string;
}

interface Summary {
  total: number;
  risk_counts: Record<string, number>;
  pattern_counts: Record<string, number>;
  severity_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_decay_composite: number;
  decay_gap_count: number;
  coaching_count: number;
  avg_trajectory_score: number;
  avg_competitive_score: number;
  avg_deal_quality_score: number;
  avg_late_stage_score: number;
  total_estimated_revenue_decay_usd: number;
}

// ─── Helpers ─────────────────────────────────────────────────────────────────

const RISK_COLORS: Record<string, string> = {
  low: "text-emerald-400", moderate: "text-amber-400",
  high: "text-orange-400", critical: "text-red-400",
};
const RISK_BG: Record<string, string> = {
  low: "bg-emerald-400/10 border-emerald-400/30",
  moderate: "bg-amber-400/10 border-amber-400/30",
  high: "bg-orange-400/10 border-orange-400/30",
  critical: "bg-red-400/10 border-red-400/30",
};
const SEV_COLORS: Record<string, string> = {
  improving: "text-emerald-400", stable: "text-sky-400",
  declining: "text-orange-400", collapsing: "text-red-400",
};

function fmtUSD(v: number): string {
  if (v >= 1_000_000) return `$${(v / 1_000_000).toFixed(1)}M`;
  if (v >= 1_000) return `$${(v / 1_000).toFixed(0)}K`;
  return `$${v.toFixed(0)}`;
}
function fmtLabel(s: string): string {
  return s.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
}

// ─── Gauge Ring ──────────────────────────────────────────────────────────────

function GaugeRing({ value, label, color }: { value: number; label: string; color: string }) {
  const r = 36, cx = 44, cy = 44;
  const circ = 2 * Math.PI * r;
  const pct = Math.min(value / 100, 1);
  const dash = pct * circ;
  return (
    <div className="flex flex-col items-center gap-1">
      <svg width="88" height="88" viewBox="0 0 88 88">
        <circle cx={cx} cy={cy} r={r} fill="none" stroke="#1e293b" strokeWidth="8" />
        <circle cx={cx} cy={cy} r={r} fill="none" stroke={color} strokeWidth="8"
          strokeDasharray={`${dash} ${circ - dash}`} strokeLinecap="round"
          transform={`rotate(-90 ${cx} ${cy})`} />
        <text x={cx} y={cy + 5} textAnchor="middle" fontSize="14" fontWeight="bold" fill="white">
          {value.toFixed(0)}
        </text>
      </svg>
      <span className="text-xs text-slate-400 text-center">{label}</span>
    </div>
  );
}

// ─── DistBar ─────────────────────────────────────────────────────────────────

function DistBar({ title, counts, colors }: { title: string; counts: Record<string, number>; colors: Record<string, string> }) {
  const total = Object.values(counts).reduce((a, b) => a + b, 0) || 1;
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-lg p-4">
      <p className="text-xs text-slate-400 mb-2">{title}</p>
      <div className="flex rounded overflow-hidden h-3 mb-2">
        {Object.entries(counts).map(([k, v]) => (
          <div key={k} style={{ width: `${(v / total) * 100}%`, background: colors[k] || "#64748b" }} title={`${k}: ${v}`} />
        ))}
      </div>
      <div className="flex flex-wrap gap-x-3 gap-y-1">
        {Object.entries(counts).map(([k, v]) => (
          <span key={k} className="text-xs" style={{ color: colors[k] || "#94a3b8" }}>
            {fmtLabel(k)}: {v}
          </span>
        ))}
      </div>
    </div>
  );
}

// ─── Detail Modal ─────────────────────────────────────────────────────────────

function DetailModal({ rep, onClose }: { rep: Rep; onClose: () => void }) {
  const [tab, setTab] = useState<"scores" | "signal" | "action">("scores");
  useEffect(() => {
    const handler = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [onClose]);
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60" onClick={onClose}>
      <div className="bg-slate-900 border border-slate-700 rounded-xl w-full max-w-lg p-6 relative" onClick={(e) => e.stopPropagation()}>
        <button onClick={onClose} className="absolute top-4 right-4 text-slate-400 hover:text-white text-lg">✕</button>
        <h3 className="text-white font-bold text-lg mb-1">{rep.rep_id}</h3>
        <p className="text-slate-400 text-sm mb-4">{rep.region} · {fmtLabel(rep.decay_risk)} risk · {fmtLabel(rep.decay_severity)}</p>
        <div className="flex gap-2 mb-4">
          {(["scores", "signal", "action"] as const).map((t) => (
            <button key={t} onClick={() => setTab(t)}
              className={`px-3 py-1 rounded text-xs font-medium transition-colors ${tab === t ? "bg-violet-500/20 text-violet-300 border border-violet-500/40" : "text-slate-400 border border-slate-700 hover:text-white"}`}>
              {t.charAt(0).toUpperCase() + t.slice(1)}
            </button>
          ))}
        </div>
        {tab === "scores" && (
          <div className="space-y-2">
            {[
              { label: "Trajectory", value: rep.trajectory_score },
              { label: "Competitive", value: rep.competitive_score },
              { label: "Deal Quality", value: rep.deal_quality_score },
              { label: "Late Stage", value: rep.late_stage_score },
              { label: "Composite", value: rep.decay_composite },
            ].map(({ label, value }) => (
              <div key={label} className="flex items-center gap-3">
                <span className="text-slate-400 text-xs w-32">{label}</span>
                <div className="flex-1 bg-slate-800 rounded-full h-2">
                  <div className="h-2 rounded-full bg-violet-400" style={{ width: `${Math.min(value, 100)}%` }} />
                </div>
                <span className="text-white text-xs w-10 text-right">{value.toFixed(1)}</span>
              </div>
            ))}
            <div className="pt-2 border-t border-slate-800 text-xs text-slate-400 flex justify-between">
              <span>Revenue Decay</span>
              <span className="text-violet-300 font-semibold">{fmtUSD(rep.estimated_revenue_decay_usd)}</span>
            </div>
          </div>
        )}
        {tab === "signal" && (
          <div className="bg-slate-800 rounded-lg p-4">
            <p className="text-slate-200 text-sm leading-relaxed">{rep.decay_signal}</p>
            <div className="mt-3 flex gap-3 flex-wrap text-xs">
              <span className={`px-2 py-0.5 rounded border ${RISK_BG[rep.decay_risk]} ${RISK_COLORS[rep.decay_risk]}`}>{fmtLabel(rep.decay_risk)} risk</span>
              <span className="text-slate-400">{fmtLabel(rep.decay_pattern)}</span>
            </div>
          </div>
        )}
        {tab === "action" && (
          <div className="space-y-3">
            <div className="bg-violet-500/10 border border-violet-500/30 rounded-lg p-4">
              <p className="text-violet-300 text-sm font-semibold">{fmtLabel(rep.recommended_action)}</p>
            </div>
            <div className="flex gap-4 text-xs text-slate-400">
              <span>Gap: <span className={rep.has_decay_gap ? "text-red-400" : "text-emerald-400"}>{rep.has_decay_gap ? "Yes" : "No"}</span></span>
              <span>Coaching: <span className={rep.requires_decay_coaching ? "text-orange-400" : "text-emerald-400"}>{rep.requires_decay_coaching ? "Required" : "Not required"}</span></span>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

// ─── Page ─────────────────────────────────────────────────────────────────────

export default function SalesWinRateDecayIntelligencePage() {
  const [reps, setReps]         = useState<Rep[]>([]);
  const [summary, setSummary]   = useState<Summary | null>(null);
  const [loading, setLoading]   = useState(true);
  const [riskFilter, setRisk]   = useState("all");
  const [patFilter, setPat]     = useState("all");
  const [selected, setSelected] = useState<Rep | null>(null);

  const load = useCallback(async () => {
    setLoading(true);
    const params = new URLSearchParams();
    if (riskFilter !== "all") params.set("risk", riskFilter);
    if (patFilter  !== "all") params.set("pattern", patFilter);
    const res = await fetch(`/api/sales-win-rate-decay-intelligence-engine?${params}`);
    const data = await res.json();
    setReps(data.reps ?? []);
    setSummary(data.summary ?? null);
    setLoading(false);
  }, [riskFilter, patFilter]);

  useEffect(() => { load(); }, [load]);

  const RISK_TABS = ["all", "low", "moderate", "high", "critical"];
  const PAT_TABS  = ["all", "none", "gradual_erosion", "sharp_cliff_drop", "competitive_displacement", "late_stage_collapse", "deal_size_inflation_trap"];

  const gaugeColor = (v: number) => v >= 60 ? "#f87171" : v >= 40 ? "#fb923c" : v >= 20 ? "#c084fc" : "#34d399";

  const dists = [
    { title: "Risk Distribution", counts: summary?.risk_counts ?? {}, colors: { low: "#34d399", moderate: "#fbbf24", high: "#fb923c", critical: "#f87171" } },
    { title: "Pattern Distribution", counts: summary?.pattern_counts ?? {}, colors: { none: "#64748b", gradual_erosion: "#fbbf24", sharp_cliff_drop: "#fb923c", competitive_displacement: "#c084fc", late_stage_collapse: "#f472b6", deal_size_inflation_trap: "#f87171" } },
    { title: "Severity Distribution", counts: summary?.severity_counts ?? {}, colors: { improving: "#34d399", stable: "#38bdf8", declining: "#fb923c", collapsing: "#f87171" } },
    { title: "Action Distribution", counts: summary?.action_counts ?? {}, colors: { no_action: "#64748b", win_loss_debrief_coaching: "#fbbf24", competitive_positioning_review: "#c084fc", deal_quality_audit: "#fb923c", late_stage_process_coaching: "#f472b6", urgent_pipeline_intervention: "#f87171" } },
  ] as Array<{ title: string; counts: Record<string, number>; colors: Record<string, string> }>;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
      {selected && <DetailModal rep={selected} onClose={() => setSelected(null)} />}

      {/* Header */}
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-white">Win Rate Decay Intelligence</h1>
        <p className="text-slate-400 text-sm mt-1">Win-rate trajectory per rep — velocity of decline, competitive displacement, deal-size inflation traps, late-stage collapse patterns</p>
      </div>

      {/* KPI Strip */}
      {summary && (
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3 mb-6">
          {[
            { label: "Total Reps", value: summary.total.toString() },
            { label: "Avg Composite", value: summary.avg_decay_composite.toFixed(1) },
            { label: "Decay Gap", value: summary.decay_gap_count.toString() },
            { label: "Need Coaching", value: summary.coaching_count.toString() },
            { label: "Revenue Decay", value: fmtUSD(summary.total_estimated_revenue_decay_usd) },
            { label: "Critical Reps", value: (summary.risk_counts["critical"] ?? 0).toString() },
          ].map(({ label, value }) => (
            <div key={label} className="bg-slate-900 border border-slate-800 rounded-lg p-4">
              <p className="text-slate-400 text-xs">{label}</p>
              <p className="text-white text-xl font-bold mt-1">{value}</p>
            </div>
          ))}
        </div>
      )}

      {/* Gauge Rings */}
      {summary && (
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 mb-6">
          <p className="text-slate-400 text-xs mb-4">Average Sub-Scores (0–100, higher = more risk)</p>
          <div className="flex flex-wrap gap-8 justify-center">
            <GaugeRing value={summary.avg_trajectory_score}   label="Trajectory"    color={gaugeColor(summary.avg_trajectory_score)} />
            <GaugeRing value={summary.avg_competitive_score}  label="Competitive"   color={gaugeColor(summary.avg_competitive_score)} />
            <GaugeRing value={summary.avg_deal_quality_score} label="Deal Quality"  color={gaugeColor(summary.avg_deal_quality_score)} />
            <GaugeRing value={summary.avg_late_stage_score}   label="Late Stage"    color={gaugeColor(summary.avg_late_stage_score)} />
          </div>
        </div>
      )}

      {/* Distribution bars */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-3 mb-6">
        {dists.map((d) => <DistBar key={d.title} {...d} />)}
      </div>

      {/* Filters */}
      <div className="space-y-2 mb-6">
        <div className="flex flex-wrap gap-2">
          {RISK_TABS.map((r) => (
            <button key={r} onClick={() => setRisk(r)}
              className={`px-3 py-1 rounded text-xs font-medium border transition-colors ${riskFilter === r ? "bg-violet-500/20 text-violet-300 border-violet-500/40" : "text-slate-400 border-slate-700 hover:text-white"}`}>
              {fmtLabel(r)}
            </button>
          ))}
        </div>
        <div className="flex flex-wrap gap-2">
          {PAT_TABS.map((p) => (
            <button key={p} onClick={() => setPat(p)}
              className={`px-3 py-1 rounded text-xs font-medium border transition-colors ${patFilter === p ? "bg-violet-500/20 text-violet-300 border-violet-500/40" : "text-slate-400 border-slate-700 hover:text-white"}`}>
              {fmtLabel(p)}
            </button>
          ))}
        </div>
      </div>

      {/* Rep Cards */}
      {loading ? (
        <div className="text-slate-400 text-center py-12">Loading...</div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          {reps.map((rep) => (
            <button key={rep.rep_id} onClick={() => setSelected(rep)}
              className="bg-slate-900 border border-slate-800 rounded-xl p-4 text-left hover:border-violet-500/40 transition-colors">
              <div className="flex items-center justify-between mb-2">
                <span className="text-white font-semibold text-sm">{rep.rep_id}</span>
                <span className={`text-xs font-medium ${RISK_COLORS[rep.decay_risk] ?? "text-slate-400"}`}>
                  {fmtLabel(rep.decay_risk)}
                </span>
              </div>
              <p className="text-slate-400 text-xs mb-2">{rep.region}</p>
              <div className="flex items-center gap-2 mb-2">
                <div className="flex-1 bg-slate-800 rounded-full h-1.5">
                  <div className="h-1.5 rounded-full bg-violet-400" style={{ width: `${Math.min(rep.decay_composite, 100)}%` }} />
                </div>
                <span className="text-xs text-slate-300">{rep.decay_composite.toFixed(0)}</span>
              </div>
              <p className={`text-xs mb-2 ${SEV_COLORS[rep.decay_severity] ?? "text-slate-400"}`}>{fmtLabel(rep.decay_severity)}</p>
              <p className="text-slate-500 text-xs truncate mb-2">{fmtLabel(rep.decay_pattern)}</p>
              <div className="flex gap-2 flex-wrap">
                {rep.has_decay_gap && (
                  <span className="text-xs bg-red-400/10 text-red-400 border border-red-400/30 px-1.5 py-0.5 rounded">📉 GAP</span>
                )}
                {rep.requires_decay_coaching && (
                  <span className="text-xs bg-orange-400/10 text-orange-400 border border-orange-400/30 px-1.5 py-0.5 rounded">📉 COACH</span>
                )}
              </div>
              {rep.estimated_revenue_decay_usd > 0 && (
                <p className="text-xs text-violet-300 mt-2">{fmtUSD(rep.estimated_revenue_decay_usd)} decay</p>
              )}
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
