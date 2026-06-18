"use client";

import { useEffect, useState, useCallback } from "react";

// ─── Types ───────────────────────────────────────────────────────────────────

interface Rep {
  rep_id: string;
  region: string;
  ramp_risk: string;
  ramp_pattern: string;
  ramp_severity: string;
  recommended_action: string;
  pipeline_score: number;
  activity_score: number;
  coaching_score: number;
  progression_score: number;
  ramp_composite: number;
  has_ramp_gap: boolean;
  requires_ramp_intervention: boolean;
  estimated_ramp_revenue_loss_usd: number;
  ramp_signal: string;
}

interface Summary {
  total: number;
  risk_counts: Record<string, number>;
  pattern_counts: Record<string, number>;
  severity_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_ramp_composite: number;
  ramp_gap_count: number;
  intervention_count: number;
  avg_pipeline_score: number;
  avg_activity_score: number;
  avg_coaching_score: number;
  avg_progression_score: number;
  total_estimated_ramp_revenue_loss_usd: number;
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
  accelerating: "text-emerald-400", on_track: "text-sky-400",
  lagging: "text-orange-400", derailing: "text-red-400",
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
        <p className="text-slate-400 text-sm mb-4">{rep.region} · {fmtLabel(rep.ramp_risk)} risk · {fmtLabel(rep.ramp_severity)}</p>
        <div className="flex gap-2 mb-4">
          {(["scores", "signal", "action"] as const).map((t) => (
            <button key={t} onClick={() => setTab(t)}
              className={`px-3 py-1 rounded text-xs font-medium transition-colors ${tab === t ? "bg-sky-500/20 text-sky-300 border border-sky-500/40" : "text-slate-400 border border-slate-700 hover:text-white"}`}>
              {t.charAt(0).toUpperCase() + t.slice(1)}
            </button>
          ))}
        </div>
        {tab === "scores" && (
          <div className="space-y-2">
            {[
              { label: "Pipeline Build", value: rep.pipeline_score },
              { label: "Activity Adoption", value: rep.activity_score },
              { label: "Coaching", value: rep.coaching_score },
              { label: "Progression", value: rep.progression_score },
              { label: "Composite", value: rep.ramp_composite },
            ].map(({ label, value }) => (
              <div key={label} className="flex items-center gap-3">
                <span className="text-slate-400 text-xs w-36">{label}</span>
                <div className="flex-1 bg-slate-800 rounded-full h-2">
                  <div className="h-2 rounded-full bg-sky-400" style={{ width: `${Math.min(value, 100)}%` }} />
                </div>
                <span className="text-white text-xs w-10 text-right">{value.toFixed(1)}</span>
              </div>
            ))}
            <div className="pt-2 border-t border-slate-800 text-xs text-slate-400 flex justify-between">
              <span>Revenue Loss Risk</span>
              <span className="text-sky-300 font-semibold">{fmtUSD(rep.estimated_ramp_revenue_loss_usd)}</span>
            </div>
          </div>
        )}
        {tab === "signal" && (
          <div className="bg-slate-800 rounded-lg p-4">
            <p className="text-slate-200 text-sm leading-relaxed">{rep.ramp_signal}</p>
            <div className="mt-3 flex gap-3 flex-wrap text-xs">
              <span className={`px-2 py-0.5 rounded border ${RISK_BG[rep.ramp_risk]} ${RISK_COLORS[rep.ramp_risk]}`}>{fmtLabel(rep.ramp_risk)} risk</span>
              <span className="text-slate-400">{fmtLabel(rep.ramp_pattern)}</span>
            </div>
          </div>
        )}
        {tab === "action" && (
          <div className="space-y-3">
            <div className="bg-sky-500/10 border border-sky-500/30 rounded-lg p-4">
              <p className="text-sky-300 text-sm font-semibold">{fmtLabel(rep.recommended_action)}</p>
            </div>
            <div className="flex gap-4 text-xs text-slate-400">
              <span>Gap: <span className={rep.has_ramp_gap ? "text-red-400" : "text-emerald-400"}>{rep.has_ramp_gap ? "Yes" : "No"}</span></span>
              <span>Intervention: <span className={rep.requires_ramp_intervention ? "text-orange-400" : "text-emerald-400"}>{rep.requires_ramp_intervention ? "Required" : "Not required"}</span></span>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

// ─── Page ─────────────────────────────────────────────────────────────────────

export default function SalesRepOnboardingRampIntelligencePage() {
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
    const res = await fetch(`/api/sales-rep-onboarding-ramp-intelligence-engine?${params}`);
    const data = await res.json();
    setReps(data.reps ?? []);
    setSummary(data.summary ?? null);
    setLoading(false);
  }, [riskFilter, patFilter]);

  useEffect(() => { load(); }, [load]);

  const RISK_TABS = ["all", "low", "moderate", "high", "critical"];
  const PAT_TABS  = ["all", "none", "slow_pipeline_build", "activity_adoption_lag", "first_deal_stall", "coaching_resistance", "early_exit_risk"];

  const gaugeColor = (v: number) => v >= 60 ? "#f87171" : v >= 40 ? "#fb923c" : v >= 20 ? "#38bdf8" : "#34d399";

  const dists = [
    { title: "Risk Distribution", counts: summary?.risk_counts ?? {}, colors: { low: "#34d399", moderate: "#fbbf24", high: "#fb923c", critical: "#f87171" } },
    { title: "Pattern Distribution", counts: summary?.pattern_counts ?? {}, colors: { none: "#64748b", slow_pipeline_build: "#38bdf8", activity_adoption_lag: "#fbbf24", first_deal_stall: "#fb923c", coaching_resistance: "#a78bfa", early_exit_risk: "#f87171" } },
    { title: "Severity Distribution", counts: summary?.severity_counts ?? {}, colors: { accelerating: "#34d399", on_track: "#38bdf8", lagging: "#fb923c", derailing: "#f87171" } },
    { title: "Action Distribution", counts: summary?.action_counts ?? {}, colors: { no_action: "#64748b", pipeline_build_coaching: "#38bdf8", activity_habits_coaching: "#fbbf24", deal_progression_coaching: "#fb923c", manager_led_intervention: "#a78bfa", ramp_extension_review: "#f87171" } },
  ] as Array<{ title: string; counts: Record<string, number>; colors: Record<string, string> }>;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
      {selected && <DetailModal rep={selected} onClose={() => setSelected(null)} />}

      {/* Header */}
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-white">Rep Onboarding Ramp Intelligence</h1>
        <p className="text-slate-400 text-sm mt-1">How reps ramp — not just when — pipeline build pace, activity adoption, coaching responsiveness, peer progression</p>
      </div>

      {/* KPI Strip */}
      {summary && (
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3 mb-6">
          {[
            { label: "Total Reps", value: summary.total.toString() },
            { label: "Avg Composite", value: summary.avg_ramp_composite.toFixed(1) },
            { label: "Ramp Gap", value: summary.ramp_gap_count.toString() },
            { label: "Need Intervention", value: summary.intervention_count.toString() },
            { label: "Revenue at Risk", value: fmtUSD(summary.total_estimated_ramp_revenue_loss_usd) },
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
            <GaugeRing value={summary.avg_pipeline_score}    label="Pipeline Build"  color={gaugeColor(summary.avg_pipeline_score)} />
            <GaugeRing value={summary.avg_activity_score}    label="Activity Adopt"  color={gaugeColor(summary.avg_activity_score)} />
            <GaugeRing value={summary.avg_coaching_score}    label="Coaching"        color={gaugeColor(summary.avg_coaching_score)} />
            <GaugeRing value={summary.avg_progression_score} label="Progression"     color={gaugeColor(summary.avg_progression_score)} />
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
              className={`px-3 py-1 rounded text-xs font-medium border transition-colors ${riskFilter === r ? "bg-sky-500/20 text-sky-300 border-sky-500/40" : "text-slate-400 border-slate-700 hover:text-white"}`}>
              {fmtLabel(r)}
            </button>
          ))}
        </div>
        <div className="flex flex-wrap gap-2">
          {PAT_TABS.map((p) => (
            <button key={p} onClick={() => setPat(p)}
              className={`px-3 py-1 rounded text-xs font-medium border transition-colors ${patFilter === p ? "bg-sky-500/20 text-sky-300 border-sky-500/40" : "text-slate-400 border-slate-700 hover:text-white"}`}>
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
              className="bg-slate-900 border border-slate-800 rounded-xl p-4 text-left hover:border-sky-500/40 transition-colors">
              <div className="flex items-center justify-between mb-2">
                <span className="text-white font-semibold text-sm">{rep.rep_id}</span>
                <span className={`text-xs font-medium ${RISK_COLORS[rep.ramp_risk] ?? "text-slate-400"}`}>
                  {fmtLabel(rep.ramp_risk)}
                </span>
              </div>
              <p className="text-slate-400 text-xs mb-2">{rep.region}</p>
              <div className="flex items-center gap-2 mb-2">
                <div className="flex-1 bg-slate-800 rounded-full h-1.5">
                  <div className="h-1.5 rounded-full bg-sky-400" style={{ width: `${Math.min(rep.ramp_composite, 100)}%` }} />
                </div>
                <span className="text-xs text-slate-300">{rep.ramp_composite.toFixed(0)}</span>
              </div>
              <p className={`text-xs mb-2 ${SEV_COLORS[rep.ramp_severity] ?? "text-slate-400"}`}>{fmtLabel(rep.ramp_severity)}</p>
              <p className="text-slate-500 text-xs truncate mb-2">{fmtLabel(rep.ramp_pattern)}</p>
              <div className="flex gap-2 flex-wrap">
                {rep.has_ramp_gap && (
                  <span className="text-xs bg-red-400/10 text-red-400 border border-red-400/30 px-1.5 py-0.5 rounded">🚀 GAP</span>
                )}
                {rep.requires_ramp_intervention && (
                  <span className="text-xs bg-orange-400/10 text-orange-400 border border-orange-400/30 px-1.5 py-0.5 rounded">🚀 INTERVENE</span>
                )}
              </div>
              {rep.estimated_ramp_revenue_loss_usd > 0 && (
                <p className="text-xs text-sky-300 mt-2">{fmtUSD(rep.estimated_ramp_revenue_loss_usd)} at risk</p>
              )}
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
