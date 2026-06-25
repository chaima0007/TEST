"use client";

import { useEffect, useState } from "react";

interface Deal {
  deal_id: string;
  deal_name: string;
  rep_id: string;
  ghosting_risk: string;
  ghosting_pattern: string;
  buyer_momentum: string;
  ghosting_action: string;
  silence_score: number;
  engagement_decay_score: number;
  behavioral_risk_score: number;
  deal_urgency_score: number;
  ghosting_composite: number;
  predicted_ghost_days: number;
  recovery_probability: number;
  is_at_risk_of_ghosting: boolean;
  needs_escalation: boolean;
  deal_value: number;
  region: string;
}

interface Summary {
  total: number;
  risk_counts: Record<string, number>;
  pattern_counts: Record<string, number>;
  momentum_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_ghosting_composite: number;
  avg_recovery_probability: number;
  at_risk_count: number;
  escalation_count: number;
  avg_silence_score: number;
  avg_engagement_decay_score: number;
  avg_behavioral_risk_score: number;
  avg_deal_urgency_score: number;
}

const RISK_COLOR: Record<string, string> = {
  critical: "#f87171",
  high:     "#fb923c",
  moderate: "#facc15",
  low:      "#34d399",
};

const RISK_BG: Record<string, string> = {
  critical: "bg-red-500/20 border-red-500/40",
  high:     "bg-orange-500/20 border-orange-500/40",
  moderate: "bg-yellow-500/20 border-yellow-500/40",
  low:      "bg-emerald-500/20 border-emerald-500/40",
};

const PATTERN_ICONS: Record<string, string> = {
  engaged:        "✅",
  cooling_off:    "🌡️",
  slow_fade:      "🌫️",
  partial_ghost:  "👻",
  full_ghost:     "💀",
  champion_exit:  "🚨",
};

const MOMENTUM_LABELS: Record<string, string> = {
  accelerating: "Accelerating",
  stable:       "Stable",
  decelerating: "Decelerating",
  stalled:      "Stalled",
};

const ACTION_LABELS: Record<string, string> = {
  maintain:       "Maintain Cadence",
  re_engage:      "Re-Engage",
  escalate_path:  "Escalate Path",
  last_resort:    "Last Resort",
};

function GhostRing({ composite, risk }: { composite: number; risk: string }) {
  const r = 52;
  const circ = 2 * Math.PI * r;
  const fill = (composite / 100) * circ;
  const color = RISK_COLOR[risk] || "#64748b";
  return (
    <svg width="128" height="128" viewBox="0 0 128 128">
      <circle cx="64" cy="64" r={r} fill="none" stroke="#1e293b" strokeWidth="12" />
      <circle
        cx="64" cy="64" r={r} fill="none"
        stroke={color} strokeWidth="12"
        strokeDasharray={`${fill} ${circ}`}
        strokeLinecap="round"
        transform="rotate(-90 64 64)"
      />
      <text x="64" y="60" textAnchor="middle" fill={color} fontSize="22" fontWeight="bold">{composite}</text>
      <text x="64" y="78" textAnchor="middle" fill="#94a3b8" fontSize="10">Ghost Risk</text>
    </svg>
  );
}

function ScoreBar({ label, value, color }: { label: string; value: number; color: string }) {
  return (
    <div>
      <div className="flex justify-between text-xs mb-1">
        <span className="text-slate-400">{label}</span>
        <span className="text-slate-200 font-medium">{value}</span>
      </div>
      <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
        <div className="h-full rounded-full transition-all duration-700" style={{ width: `${value}%`, backgroundColor: color }} />
      </div>
    </div>
  );
}

function RiskDistBar({ counts }: { counts: Record<string, number> }) {
  const total = Object.values(counts).reduce((a, b) => a + b, 0);
  const order = ["critical", "high", "moderate", "low"];
  return (
    <div className="flex h-3 rounded-full overflow-hidden gap-0.5">
      {order.map((k) =>
        (counts[k] || 0) > 0 ? (
          <div
            key={k}
            title={`${k}: ${counts[k]}`}
            style={{ width: `${((counts[k] || 0) / total) * 100}%`, backgroundColor: RISK_COLOR[k] }}
          />
        ) : null
      )}
    </div>
  );
}

function DealModal({ deal, onClose }: { deal: Deal; onClose: () => void }) {
  const [tab, setTab] = useState<"signals" | "scores" | "actions">("signals");

  useEffect(() => {
    const handler = (e: KeyboardEvent) => e.key === "Escape" && onClose();
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [onClose]);

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm p-4"
      onClick={onClose}
    >
      <div
        className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-lg shadow-2xl"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="p-5 border-b border-slate-800">
          <div className="flex items-start justify-between gap-3">
            <div>
              <h2 className="text-slate-100 font-semibold text-lg leading-tight">
                {PATTERN_ICONS[deal.ghosting_pattern]} {deal.deal_name}
              </h2>
              <p className="text-slate-400 text-sm mt-0.5">{deal.rep_id} · {deal.region} · ${(deal.deal_value / 1000).toFixed(0)}K</p>
            </div>
            <span className={`text-xs font-bold uppercase px-2 py-1 rounded-full border ${RISK_BG[deal.ghosting_risk]}`}
              style={{ color: RISK_COLOR[deal.ghosting_risk] }}>
              {deal.ghosting_risk}
            </span>
          </div>
          <div className="flex gap-2 mt-4">
            {(["signals", "scores", "actions"] as const).map((t) => (
              <button
                key={t}
                onClick={() => setTab(t)}
                className={`px-3 py-1.5 text-xs font-medium rounded-lg transition-colors ${
                  tab === t ? "bg-indigo-600 text-white" : "text-slate-400 hover:text-slate-200"
                }`}
              >
                {t.charAt(0).toUpperCase() + t.slice(1)}
              </button>
            ))}
          </div>
        </div>

        <div className="p-5 space-y-4">
          {tab === "signals" && (
            <>
              <div className="grid grid-cols-2 gap-3">
                {[
                  ["Pattern", `${PATTERN_ICONS[deal.ghosting_pattern]} ${deal.ghosting_pattern.replace(/_/g, " ")}`],
                  ["Momentum", MOMENTUM_LABELS[deal.buyer_momentum] || deal.buyer_momentum],
                  ["Ghost in", deal.predicted_ghost_days === 0 ? "Already ghosting" : `~${deal.predicted_ghost_days}d`],
                  ["Recovery %", `${deal.recovery_probability}%`],
                ].map(([label, value]) => (
                  <div key={label} className="bg-slate-800/60 rounded-xl p-3">
                    <p className="text-xs text-slate-500">{label}</p>
                    <p className="text-sm font-semibold text-slate-100 capitalize mt-0.5">{value}</p>
                  </div>
                ))}
              </div>
              <div className="flex gap-2 flex-wrap">
                {deal.is_at_risk_of_ghosting && (
                  <span className="text-xs bg-orange-500/15 text-orange-400 border border-orange-500/30 rounded-lg px-2 py-1">
                    👻 At Risk
                  </span>
                )}
                {deal.needs_escalation && (
                  <span className="text-xs bg-red-500/15 text-red-400 border border-red-500/30 rounded-lg px-2 py-1">
                    🚨 Needs Escalation
                  </span>
                )}
              </div>
            </>
          )}
          {tab === "scores" && (
            <div className="space-y-3">
              <ScoreBar label="Silence Score" value={deal.silence_score} color="#f87171" />
              <ScoreBar label="Engagement Decay" value={deal.engagement_decay_score} color="#fb923c" />
              <ScoreBar label="Behavioral Risk" value={deal.behavioral_risk_score} color="#facc15" />
              <ScoreBar label="Deal Urgency" value={deal.deal_urgency_score} color="#818cf8" />
              <div className="pt-2 border-t border-slate-800">
                <ScoreBar label="Ghost Composite" value={deal.ghosting_composite} color={RISK_COLOR[deal.ghosting_risk]} />
              </div>
            </div>
          )}
          {tab === "actions" && (
            <div className="space-y-3">
              <div className="bg-slate-800/60 rounded-xl p-4">
                <p className="text-xs text-slate-500 mb-1">Recommended Action</p>
                <p className="text-indigo-300 font-semibold">{ACTION_LABELS[deal.ghosting_action] || deal.ghosting_action}</p>
              </div>
              {deal.ghosting_action === "last_resort" && (
                <p className="bg-red-500/10 border border-red-500/20 rounded-lg p-3 text-red-300 text-xs">
                  Executive intervention required. Send a value-reset email with a clear drop-dead date. Consider walking away if no response within 5 business days.
                </p>
              )}
              {deal.ghosting_action === "escalate_path" && (
                <p className="bg-orange-500/10 border border-orange-500/20 rounded-lg p-3 text-orange-300 text-xs">
                  Multi-thread immediately. Reach out to a second stakeholder with a new angle. Send a short breakup email to reset urgency.
                </p>
              )}
              {deal.ghosting_action === "re_engage" && (
                <p className="bg-yellow-500/10 border border-yellow-500/20 rounded-lg p-3 text-yellow-300 text-xs">
                  Change your outreach channel (call vs email). Lead with fresh value — ROI data, case study, or competitive insight. Don't reference the silence.
                </p>
              )}
              {deal.ghosting_action === "maintain" && (
                <p className="bg-emerald-500/10 border border-emerald-500/20 rounded-lg p-3 text-emerald-300 text-xs">
                  Buyer is still engaged. Continue your cadence. Reinforce next steps with a mutual timeline and recap email.
                </p>
              )}
            </div>
          )}
        </div>

        <div className="p-4 border-t border-slate-800">
          <button onClick={onClose} className="w-full py-2 text-sm text-slate-400 hover:text-slate-200 transition-colors">
            Close
          </button>
        </div>
      </div>
    </div>
  );
}

function DealCard({ deal, onClick }: { deal: Deal; onClick: () => void }) {
  return (
    <div
      onClick={onClick}
      className={`bg-slate-900 border rounded-2xl p-4 cursor-pointer hover:border-indigo-500/50 transition-all ${RISK_BG[deal.ghosting_risk]}`}
    >
      <div className="flex items-start justify-between gap-2 mb-3">
        <div className="min-w-0">
          <p className="text-slate-100 font-semibold text-sm truncate">
            {PATTERN_ICONS[deal.ghosting_pattern]} {deal.deal_name}
          </p>
          <p className="text-slate-500 text-xs mt-0.5">{deal.region} · {deal.rep_id}</p>
        </div>
        <span
          className="text-xs font-bold uppercase shrink-0"
          style={{ color: RISK_COLOR[deal.ghosting_risk] }}
        >
          {deal.ghosting_risk}
        </span>
      </div>

      <div className="flex items-center gap-3 mb-3">
        <GhostRing composite={deal.ghosting_composite} risk={deal.ghosting_risk} />
        <div className="flex-1 space-y-2 min-w-0">
          <ScoreBar label="Silence" value={deal.silence_score} color="#f87171" />
          <ScoreBar label="Decay" value={deal.engagement_decay_score} color="#fb923c" />
          <ScoreBar label="Behavior" value={deal.behavioral_risk_score} color="#facc15" />
          <ScoreBar label="Urgency" value={deal.deal_urgency_score} color="#818cf8" />
        </div>
      </div>

      <div className="flex items-center justify-between text-xs">
        <span className="text-slate-400">
          Recovery: <span className="text-emerald-400 font-medium">{deal.recovery_probability}%</span>
        </span>
        <span className="text-slate-400">
          {deal.predicted_ghost_days === 0 ? (
            <span className="text-red-400">👻 Ghosting now</span>
          ) : (
            <span>Ghost in ~{deal.predicted_ghost_days}d</span>
          )}
        </span>
      </div>
      <div className="flex gap-1 mt-2 flex-wrap">
        {deal.is_at_risk_of_ghosting && (
          <span className="text-xs bg-orange-500/15 text-orange-400 rounded px-1.5 py-0.5">At Risk</span>
        )}
        {deal.needs_escalation && (
          <span className="text-xs bg-red-500/15 text-red-400 rounded px-1.5 py-0.5">Escalate</span>
        )}
        <span className="text-xs bg-slate-700/60 text-slate-400 rounded px-1.5 py-0.5">
          ${(deal.deal_value / 1000).toFixed(0)}K
        </span>
      </div>
    </div>
  );
}

export default function GhostingPredictorPage() {
  const [data, setData] = useState<{ deals: Deal[]; summary: Summary } | null>(null);
  const [selected, setSelected] = useState<Deal | null>(null);
  const [filterRisk, setFilterRisk] = useState("all");
  const [filterPattern, setFilterPattern] = useState("all");

  useEffect(() => {
    async function load() {
        const params = new URLSearchParams();
        if (filterRisk !== "all")    params.set("risk", filterRisk);
        if (filterPattern !== "all") params.set("pattern", filterPattern);
        const res = await fetch(`/api/ghosting-predictor?${params}`);
        setData(await res.json());
  }
    load();
  }, [filterRisk, filterPattern]);

  const s = data?.summary;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
      <div className="max-w-7xl mx-auto space-y-6">

        {/* Header */}
        <div>
          <h1 className="text-2xl font-bold text-slate-100">Ghosting Predictor</h1>
          <p className="text-slate-400 text-sm mt-1">Detect deals about to go silent before they actually do — pre-ghost behavioral signals</p>
        </div>

        {/* Critical alert */}
        {s && s.escalation_count > 0 && (
          <div className="bg-red-500/10 border border-red-500/30 rounded-xl p-4 flex items-center gap-3">
            <span className="text-2xl">👻</span>
            <div>
              <p className="text-red-300 font-semibold">
                {s.escalation_count} {s.escalation_count === 1 ? "deal" : "deals"} need immediate escalation to prevent total ghosting
              </p>
              <p className="text-red-400/80 text-xs mt-0.5">
                {s.at_risk_count} total deals are at risk of buyer ghosting
              </p>
            </div>
          </div>
        )}

        {/* KPI strip */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
          {[
            { label: "Total Deals", value: s?.total ?? "—", sub: "monitored" },
            { label: "Avg Ghost Risk", value: s ? `${s.avg_ghosting_composite}` : "—", sub: "composite score" },
            { label: "At Risk", value: s?.at_risk_count ?? "—", sub: "ghost risk" },
            { label: "Avg Recovery", value: s ? `${s.avg_recovery_probability}%` : "—", sub: "re-engagement chance" },
          ].map(({ label, value, sub }) => (
            <div key={label} className="bg-slate-900 border border-slate-800 rounded-2xl p-4">
              <p className="text-xs text-slate-500">{label}</p>
              <p className="text-2xl font-bold text-slate-100 mt-1">{value}</p>
              <p className="text-xs text-slate-500 mt-0.5">{sub}</p>
            </div>
          ))}
        </div>

        {/* Risk distribution + score breakdown */}
        {s && (
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div className="bg-slate-900 border border-slate-800 rounded-2xl p-4">
              <h3 className="text-sm font-semibold text-slate-300 mb-3">Risk Distribution</h3>
              <RiskDistBar counts={s.risk_counts} />
              <div className="flex flex-wrap gap-x-4 gap-y-1 mt-3">
                {Object.entries(s.risk_counts).map(([k, v]) => (
                  <span key={k} className="text-xs" style={{ color: RISK_COLOR[k] || "#94a3b8" }}>
                    {k}: {v}
                  </span>
                ))}
              </div>
            </div>
            <div className="bg-slate-900 border border-slate-800 rounded-2xl p-4">
              <h3 className="text-sm font-semibold text-slate-300 mb-3">Avg Score Breakdown</h3>
              <div className="space-y-2">
                <ScoreBar label="Silence Score" value={s.avg_silence_score} color="#f87171" />
                <ScoreBar label="Engagement Decay" value={s.avg_engagement_decay_score} color="#fb923c" />
                <ScoreBar label="Behavioral Risk" value={s.avg_behavioral_risk_score} color="#facc15" />
                <ScoreBar label="Deal Urgency" value={s.avg_deal_urgency_score} color="#818cf8" />
              </div>
            </div>
          </div>
        )}

        {/* Filters */}
        <div className="flex flex-wrap gap-2">
          <div className="flex gap-1 flex-wrap">
            {["all", "critical", "high", "moderate", "low"].map((r) => (
              <button
                key={r}
                onClick={() => setFilterRisk(r)}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
                  filterRisk === r ? "bg-indigo-600 text-white" : "bg-slate-800 text-slate-400 hover:text-slate-200"
                }`}
              >
                {r === "all" ? "All Risks" : r.charAt(0).toUpperCase() + r.slice(1)}
              </button>
            ))}
          </div>
          <div className="flex gap-1 flex-wrap">
            {["all", "engaged", "cooling_off", "slow_fade", "partial_ghost", "full_ghost", "champion_exit"].map((p) => (
              <button
                key={p}
                onClick={() => setFilterPattern(p)}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
                  filterPattern === p ? "bg-violet-600 text-white" : "bg-slate-800 text-slate-400 hover:text-slate-200"
                }`}
              >
                {p === "all" ? "All Patterns" : `${PATTERN_ICONS[p] || ""} ${p.replace(/_/g, " ")}`}
              </button>
            ))}
          </div>
        </div>

        {/* Deal cards */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          {data?.deals.map((d) => (
            <DealCard key={d.deal_id} deal={d} onClick={() => setSelected(d)} />
          ))}
        </div>

        {data?.deals.length === 0 && (
          <div className="text-center py-16 text-slate-500">No deals match the selected filters.</div>
        )}
      </div>

      {selected && <DealModal deal={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
