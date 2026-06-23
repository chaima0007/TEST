"use client";

import { useEffect, useState } from "react";

interface GhostingDeal {
  deal_id: string;
  rep_id: string;
  ghosting_risk: string;
  ghosting_pattern: string;
  ghosting_severity: string;
  recommended_action: string;
  silence_score: number;
  engagement_decay_score: number;
  stakeholder_coverage_score: number;
  deal_momentum_score: number;
  ghosting_composite: number;
  is_ghosted: boolean;
  requires_escalation: boolean;
  estimated_deal_recovery_pct: number;
  ghosting_signal: string;
}

interface Summary {
  total: number;
  risk_counts: Record<string, number>;
  pattern_counts: Record<string, number>;
  severity_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_ghosting_composite: number;
  ghosted_count: number;
  escalation_count: number;
  avg_silence_score: number;
  avg_engagement_decay_score: number;
  avg_stakeholder_coverage_score: number;
  avg_deal_momentum_score: number;
  avg_estimated_deal_recovery_pct: number;
}

const RISK_COLORS: Record<string, string> = {
  low:      "text-emerald-400",
  moderate: "text-amber-400",
  high:     "text-orange-400",
  critical: "text-red-400",
};
const RISK_BG: Record<string, string> = {
  low:      "bg-emerald-400/10 border-emerald-400/30",
  moderate: "bg-amber-400/10 border-amber-400/30",
  high:     "bg-orange-400/10 border-orange-400/30",
  critical: "bg-red-400/10 border-red-400/30",
};
const SEV_COLORS: Record<string, string> = {
  active:  "bg-emerald-500",
  cooling: "bg-amber-500",
  dark:    "bg-orange-500",
  lost:    "bg-red-500",
};
const PATTERN_LABELS: Record<string, string> = {
  none:                   "No Issues",
  silence_after_demo:     "Silence After Demo",
  proposal_drop_off:      "Proposal Drop-off",
  champion_unresponsive:  "Champion Unresponsive",
  multi_stakeholder_fade: "Multi-Stakeholder Fade",
  end_of_cycle_ghost:     "End-of-Cycle Ghost",
};
const ACTION_LABELS: Record<string, string> = {
  no_action:             "No Action",
  follow_up_sequence:    "Follow-up Sequence",
  manager_re_engage:     "Manager Re-engage",
  exec_outreach:         "Exec Outreach",
  deal_disqualification: "Deal Disqualification",
};

function ScoreBar({ label, value, color = "bg-indigo-500" }: { label: string; value: number; color?: string }) {
  return (
    <div>
      <div className="flex justify-between text-xs mb-1">
        <span className="text-slate-400">{label}</span>
        <span className="text-slate-200 font-mono">{value.toFixed(1)}</span>
      </div>
      <div className="h-1.5 rounded-full bg-slate-800">
        <div className={`h-1.5 rounded-full ${color}`} style={{ width: `${Math.min(value, 100)}%` }} />
      </div>
    </div>
  );
}

function RecoveryRing({ recoveryPct }: { recoveryPct: number }) {
  const r = 36;
  const circ = 2 * Math.PI * r;
  const fill = (recoveryPct / 100) * circ;
  const color = recoveryPct >= 70 ? "#34d399" : recoveryPct >= 50 ? "#fbbf24" : recoveryPct >= 30 ? "#fb923c" : "#f87171";
  return (
    <svg viewBox="0 0 88 88" className="w-20 h-20">
      <circle cx="44" cy="44" r={r} fill="none" stroke="#1e293b" strokeWidth="8" />
      <circle
        cx="44" cy="44" r={r} fill="none"
        stroke={color} strokeWidth="8"
        strokeDasharray={`${fill} ${circ}`}
        strokeLinecap="round"
        transform="rotate(-90 44 44)"
      />
      <text x="44" y="46" textAnchor="middle" fontSize="11" fontWeight="700" fill={color}>
        {recoveryPct.toFixed(0)}%
      </text>
    </svg>
  );
}

function DetailModal({ deal, onClose }: { deal: GhostingDeal; onClose: () => void }) {
  const [tab, setTab] = useState<"overview" | "scores" | "action">("overview");
  useEffect(() => {
    const handler = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [onClose]);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm" onClick={onClose}>
      <div className="relative bg-slate-900 border border-slate-700 rounded-2xl shadow-2xl w-full max-w-lg mx-4 overflow-hidden" onClick={(e) => e.stopPropagation()}>
        <div className="flex items-center justify-between px-6 py-4 border-b border-slate-800">
          <div>
            <p className="text-xs text-slate-500 uppercase tracking-widest">Deal Ghosting Risk</p>
            <h2 className="text-lg font-bold text-slate-100">{deal.deal_id}</h2>
            <p className="text-xs text-slate-400">{deal.rep_id} · {PATTERN_LABELS[deal.ghosting_pattern]}</p>
          </div>
          <div className="flex flex-col items-end gap-1">
            <span className={`text-xs font-semibold px-2 py-0.5 rounded-full border ${RISK_BG[deal.ghosting_risk]}`}>
              <span className={RISK_COLORS[deal.ghosting_risk]}>{deal.ghosting_risk.toUpperCase()}</span>
            </span>
            <span className={`text-xs px-2 py-0.5 rounded-full text-white ${SEV_COLORS[deal.ghosting_severity]}`}>
              {deal.ghosting_severity}
            </span>
            <button onClick={onClose} className="text-slate-500 hover:text-slate-200 text-xl leading-none mt-1">×</button>
          </div>
        </div>

        <div className="flex border-b border-slate-800">
          {(["overview", "scores", "action"] as const).map((t) => (
            <button key={t} onClick={() => setTab(t)}
              className={`flex-1 py-2 text-xs font-semibold uppercase tracking-widest transition-colors ${tab === t ? "text-indigo-400 border-b-2 border-indigo-400" : "text-slate-500 hover:text-slate-300"}`}>
              {t}
            </button>
          ))}
        </div>

        <div className="px-6 py-5 space-y-4">
          {tab === "overview" && (
            <>
              <div className="flex items-center justify-center py-2">
                <RecoveryRing recoveryPct={deal.estimated_deal_recovery_pct} />
              </div>
              <p className="text-sm text-slate-300 italic text-center">&ldquo;{deal.ghosting_signal}&rdquo;</p>
              <div className="grid grid-cols-2 gap-3 text-xs">
                <div className="bg-slate-800 rounded-lg p-3">
                  <p className="text-slate-500 mb-1">Ghosting Score</p>
                  <p className="text-slate-100 font-bold text-base">{deal.ghosting_composite.toFixed(1)}</p>
                </div>
                <div className="bg-slate-800 rounded-lg p-3">
                  <p className="text-slate-500 mb-1">Recovery Chance</p>
                  <p className="text-emerald-400 font-bold text-base">{deal.estimated_deal_recovery_pct.toFixed(1)}%</p>
                </div>
                <div className="bg-slate-800 rounded-lg p-3">
                  <p className="text-slate-500 mb-1">Ghosted</p>
                  <p className={`font-bold ${deal.is_ghosted ? "text-red-400" : "text-emerald-400"}`}>
                    {deal.is_ghosted ? "Yes" : "No"}
                  </p>
                </div>
                <div className="bg-slate-800 rounded-lg p-3">
                  <p className="text-slate-500 mb-1">Escalation</p>
                  <p className={`font-bold ${deal.requires_escalation ? "text-orange-400" : "text-emerald-400"}`}>
                    {deal.requires_escalation ? "Required" : "Not needed"}
                  </p>
                </div>
              </div>
            </>
          )}
          {tab === "scores" && (
            <div className="space-y-3">
              <ScoreBar label="Silence" value={deal.silence_score} color="bg-slate-500" />
              <ScoreBar label="Engagement Decay" value={deal.engagement_decay_score} color="bg-amber-500" />
              <ScoreBar label="Stakeholder Coverage" value={deal.stakeholder_coverage_score} color="bg-orange-500" />
              <ScoreBar label="Deal Momentum Loss" value={deal.deal_momentum_score} color="bg-red-500" />
              <div className="pt-2 border-t border-slate-800">
                <ScoreBar label="Ghosting Composite" value={deal.ghosting_composite} color="bg-indigo-500" />
              </div>
            </div>
          )}
          {tab === "action" && (
            <div className="space-y-3 text-sm">
              <div className="bg-slate-800 rounded-lg p-4">
                <p className="text-slate-500 text-xs mb-1">Recommended Action</p>
                <p className="text-indigo-300 font-semibold">{ACTION_LABELS[deal.recommended_action]}</p>
              </div>
              <div className="bg-slate-800 rounded-lg p-4">
                <p className="text-slate-500 text-xs mb-1">Ghosting Pattern</p>
                <p className="text-slate-200">{PATTERN_LABELS[deal.ghosting_pattern]}</p>
              </div>
              <div className="bg-slate-800 rounded-lg p-4">
                <p className="text-slate-500 text-xs mb-1">Severity</p>
                <p className="text-slate-200 capitalize">{deal.ghosting_severity}</p>
              </div>
              <div className="bg-slate-800 rounded-lg p-4">
                <p className="text-slate-500 text-xs mb-2">Flags</p>
                <div className="flex flex-wrap gap-2">
                  {deal.is_ghosted && <span className="text-xs px-2 py-0.5 rounded-full bg-red-400/10 border border-red-400/30 text-red-400">Ghosted</span>}
                  {deal.requires_escalation && <span className="text-xs px-2 py-0.5 rounded-full bg-orange-400/10 border border-orange-400/30 text-orange-400">Escalation Required</span>}
                  {!deal.is_ghosted && !deal.requires_escalation && <span className="text-xs text-slate-500">No critical flags</span>}
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default function DealGhostingPage() {
  const [data, setData] = useState<{ deals: GhostingDeal[]; summary: Summary } | null>(null);
  const [selected, setSelected] = useState<GhostingDeal | null>(null);
  const [riskFilter, setRiskFilter] = useState("all");

  useEffect(() => {
    async function load() {
        const params = new URLSearchParams();
        if (riskFilter !== "all") params.set("risk", riskFilter);
        const res = await fetch(`/api/deal-ghosting-risk-engine?${params}`);
        setData(await res.json());
  }
    load();
  }, [riskFilter]);

  const summary = data?.summary;
  const deals = data?.deals ?? [];

  const kpis = summary
    ? [
        { label: "Total Deals", value: summary.total, sub: "monitored" },
        { label: "Ghosted Deals", value: summary.ghosted_count, sub: "confirmed", accent: "text-red-400" },
        { label: "Need Escalation", value: summary.escalation_count, sub: "deals", accent: "text-orange-400" },
        { label: "Avg Ghost Score", value: summary.avg_ghosting_composite.toFixed(1), sub: "composite" },
        { label: "Avg Recovery", value: `${summary.avg_estimated_deal_recovery_pct.toFixed(1)}%`, sub: "chance", accent: "text-emerald-400" },
      ]
    : [];

  const patterns = summary
    ? Object.entries(summary.pattern_counts).sort((a, b) => b[1] - a[1])
    : [];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {selected && <DetailModal deal={selected} onClose={() => setSelected(null)} />}

      <div>
        <h1 className="text-2xl font-bold text-slate-100">Deal Ghosting Risk Engine</h1>
        <p className="text-sm text-slate-400 mt-1">Detects prospect silence, champion fade, and stakeholder disengagement before deals become unrecoverable</p>
      </div>

      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-4">
        {kpis.map((k) => (
          <div key={k.label} className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <p className="text-xs text-slate-500 uppercase tracking-widest mb-1">{k.label}</p>
            <p className={`text-2xl font-bold ${k.accent ?? "text-slate-100"}`}>{k.value}</p>
            <p className="text-xs text-slate-500 mt-0.5">{k.sub}</p>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {summary && (
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-3">
            <h2 className="text-sm font-semibold text-slate-300 uppercase tracking-widest mb-3">Avg Risk Scores</h2>
            <ScoreBar label="Silence" value={summary.avg_silence_score} color="bg-slate-500" />
            <ScoreBar label="Engagement Decay" value={summary.avg_engagement_decay_score} color="bg-amber-500" />
            <ScoreBar label="Stakeholder Coverage" value={summary.avg_stakeholder_coverage_score} color="bg-orange-500" />
            <ScoreBar label="Deal Momentum Loss" value={summary.avg_deal_momentum_score} color="bg-red-500" />
            <ScoreBar label="Ghosting Composite" value={summary.avg_ghosting_composite} color="bg-indigo-500" />
          </div>
        )}

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
          <h2 className="text-sm font-semibold text-slate-300 uppercase tracking-widest mb-4">Ghosting Patterns</h2>
          <div className="space-y-2">
            {patterns.map(([pat, count]) => (
              <div key={pat} className="flex items-center gap-3">
                <span className="text-xs text-slate-400 w-44 truncate">{PATTERN_LABELS[pat] ?? pat}</span>
                <div className="flex-1 h-2 bg-slate-800 rounded-full">
                  <div
                    className="h-2 rounded-full bg-indigo-500"
                    style={{ width: summary ? `${(count / summary.total) * 100}%` : "0%" }}
                  />
                </div>
                <span className="text-xs font-mono text-slate-300 w-4 text-right">{count}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="flex gap-2 flex-wrap">
        {["all", "low", "moderate", "high", "critical"].map((f) => (
          <button key={f} onClick={() => setRiskFilter(f)}
            className={`px-4 py-1.5 rounded-full text-xs font-semibold border transition-colors ${
              riskFilter === f
                ? "bg-indigo-600 border-indigo-500 text-white"
                : "bg-slate-800 border-slate-700 text-slate-400 hover:text-slate-200"
            }`}>
            {f === "all" ? "All" : f.charAt(0).toUpperCase() + f.slice(1)}
          </button>
        ))}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
        {deals.map((deal) => (
          <button key={deal.deal_id} onClick={() => setSelected(deal)}
            className={`bg-slate-900 border rounded-xl p-4 text-left transition-colors group ${
              deal.is_ghosted
                ? "border-red-500/40 hover:border-red-400/60"
                : "border-slate-800 hover:border-indigo-500/50"
            }`}>
            <div className="flex items-start justify-between mb-3">
              <div>
                <p className="font-semibold text-slate-100 group-hover:text-indigo-300 transition-colors">{deal.deal_id}</p>
                <p className="text-xs text-slate-500">{deal.rep_id}</p>
              </div>
              <div className="flex flex-col items-end gap-1">
                <span className={`text-xs font-semibold ${RISK_COLORS[deal.ghosting_risk]}`}>
                  {deal.ghosting_risk.toUpperCase()}
                </span>
                <span className={`text-xs px-1.5 py-0.5 rounded text-white ${SEV_COLORS[deal.ghosting_severity]}`}>
                  {deal.ghosting_severity}
                </span>
              </div>
            </div>
            <div className="flex items-center gap-3 mb-3">
              <RecoveryRing recoveryPct={deal.estimated_deal_recovery_pct} />
              <div className="flex-1 space-y-1.5">
                <ScoreBar label="Silence" value={deal.silence_score} color="bg-slate-500" />
                <ScoreBar label="Engagement" value={deal.engagement_decay_score} color="bg-amber-500" />
                <ScoreBar label="Stakeholders" value={deal.stakeholder_coverage_score} color="bg-orange-500" />
              </div>
            </div>
            <p className="text-xs text-slate-400 italic leading-snug line-clamp-2">{deal.ghosting_signal}</p>
            <div className="flex gap-2 mt-3 flex-wrap">
              {deal.is_ghosted && (
                <span className="text-xs px-2 py-0.5 rounded-full bg-red-400/10 border border-red-400/30 text-red-400">Ghosted</span>
              )}
              {deal.requires_escalation && (
                <span className="text-xs px-2 py-0.5 rounded-full bg-orange-400/10 border border-orange-400/30 text-orange-400">Escalate</span>
              )}
              <span className="text-xs px-2 py-0.5 rounded-full bg-slate-800 text-slate-400">
                {ACTION_LABELS[deal.recommended_action]}
              </span>
            </div>
          </button>
        ))}
      </div>
    </div>
  );
}
