"use client";

import { useEffect, useState, useCallback } from "react";

// ── types ──────────────────────────────────────────────────────────────────────
interface MAPRecord {
  deal_id: string;
  deal_name: string;
  rep_id: string;
  map_health: string;
  adherence_pattern: string;
  commitment_signal: string;
  map_action: string;
  rep_adherence_score: number;
  buyer_adherence_score: number;
  milestone_progress_score: number;
  map_quality_score: number;
  map_adherence_composite: number;
  estimated_close_confidence: number;
  days_to_close_risk: number;
  is_healthy_map: boolean;
  needs_map_reset: boolean;
  deal_value: number;
  region: string;
}

interface Summary {
  total: number;
  health_counts: Record<string, number>;
  pattern_counts: Record<string, number>;
  signal_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_map_adherence_composite: number;
  avg_close_confidence: number;
  healthy_map_count: number;
  reset_needed_count: number;
  avg_rep_adherence_score: number;
  avg_buyer_adherence_score: number;
  avg_milestone_progress_score: number;
  avg_map_quality_score: number;
}

// ── helpers ────────────────────────────────────────────────────────────────────
const HEALTH_COLOR: Record<string, string> = {
  on_track: "text-emerald-400",
  slipping: "text-yellow-400",
  at_risk:  "text-orange-400",
  broken:   "text-red-400",
};
const HEALTH_BG: Record<string, string> = {
  on_track: "bg-emerald-900/30 border-emerald-700",
  slipping: "bg-yellow-900/30 border-yellow-700",
  at_risk:  "bg-orange-900/30 border-orange-700",
  broken:   "bg-red-900/30 border-red-700",
};
const ACTION_BADGE: Record<string, string> = {
  accelerate: "bg-emerald-900/50 text-emerald-300 border-emerald-700",
  reaffirm:   "bg-yellow-900/50 text-yellow-300 border-yellow-700",
  reset_map:  "bg-orange-900/50 text-orange-300 border-orange-700",
  escalate:   "bg-red-900/50 text-red-300 border-red-700",
};
const SIGNAL_COLOR: Record<string, string> = {
  strong:   "text-emerald-400",
  moderate: "text-blue-400",
  weak:     "text-yellow-400",
  absent:   "text-red-400",
};
const PATTERN_LABEL: Record<string, string> = {
  both_committed:     "Both Committed",
  rep_only:           "Rep Only",
  buyer_leading:      "Buyer Leading",
  buyer_ghosting:     "Buyer Ghosting",
  mutual_drift:       "Mutual Drift",
  complete_breakdown: "Complete Breakdown",
};
const HEALTH_LABEL: Record<string, string> = {
  on_track: "On Track", slipping: "Slipping", at_risk: "At Risk", broken: "Broken",
};

function fmt$(n: number) {
  if (n >= 1_000_000) return `$${(n / 1_000_000).toFixed(1)}M`;
  if (n >= 1_000)     return `$${(n / 1_000).toFixed(0)}K`;
  return `$${n}`;
}

// ── MAPGauge ──────────────────────────────────────────────────────────────────
function MAPGauge({ score, health, size = 80 }: { score: number; health: string; size?: number }) {
  const r = (size - 12) / 2;
  const circ = 2 * Math.PI * r;
  const fill = (score / 100) * circ;
  const colorMap: Record<string, string> = {
    on_track: "#34d399", slipping: "#facc15", at_risk: "#fb923c", broken: "#f87171",
  };
  const color = colorMap[health] || "#64748b";
  return (
    <svg width={size} height={size} className="rotate-[-90deg]">
      <circle cx={size / 2} cy={size / 2} r={r} fill="none" stroke="#1e293b" strokeWidth={8} />
      <circle
        cx={size / 2} cy={size / 2} r={r}
        fill="none" stroke={color} strokeWidth={8}
        strokeDasharray={`${fill} ${circ}`}
        strokeLinecap="round"
      />
    </svg>
  );
}

// ── DualBar: rep vs buyer adherence ──────────────────────────────────────────
function DualBar({ repScore, buyerScore }: { repScore: number; buyerScore: number }) {
  return (
    <div className="space-y-1">
      <div className="flex items-center gap-2 text-xs">
        <span className="text-slate-400 w-10">Rep</span>
        <div className="flex-1 h-2 bg-slate-800 rounded-full overflow-hidden">
          <div className="h-full bg-blue-500 rounded-full" style={{ width: `${repScore}%` }} />
        </div>
        <span className="text-blue-300 font-semibold w-8 text-right">{repScore.toFixed(0)}</span>
      </div>
      <div className="flex items-center gap-2 text-xs">
        <span className="text-slate-400 w-10">Buyer</span>
        <div className="flex-1 h-2 bg-slate-800 rounded-full overflow-hidden">
          <div className="h-full bg-violet-500 rounded-full" style={{ width: `${buyerScore}%` }} />
        </div>
        <span className="text-violet-300 font-semibold w-8 text-right">{buyerScore.toFixed(0)}</span>
      </div>
    </div>
  );
}

// ── HealthDistBar ─────────────────────────────────────────────────────────────
function HealthDistBar({ counts, total }: { counts: Record<string, number>; total: number }) {
  const order  = ["on_track", "slipping", "at_risk", "broken"];
  const colors = ["#34d399", "#facc15", "#fb923c", "#f87171"];
  const labels = ["On Track", "Slipping", "At Risk", "Broken"];
  return (
    <div>
      <div className="flex h-4 rounded-full overflow-hidden mb-2 gap-0.5">
        {order.map((k, i) => {
          const pct = total > 0 ? ((counts[k] || 0) / total) * 100 : 0;
          return pct > 0 ? (
            <div key={k} style={{ width: `${pct}%`, backgroundColor: colors[i] }} title={labels[i]} />
          ) : null;
        })}
      </div>
      <div className="flex gap-4 flex-wrap">
        {order.map((k, i) => (
          <div key={k} className="flex items-center gap-1.5 text-xs text-slate-400">
            <span className="w-2 h-2 rounded-full inline-block" style={{ backgroundColor: colors[i] }} />
            {labels[i]}: {counts[k] || 0}
          </div>
        ))}
      </div>
    </div>
  );
}

// ── ScoreBar ──────────────────────────────────────────────────────────────────
function ScoreBar({ label, score, color }: { label: string; score: number; color: string }) {
  return (
    <div>
      <div className="flex justify-between text-xs mb-1">
        <span className="text-slate-400">{label}</span>
        <span className="font-semibold" style={{ color }}>{score.toFixed(1)}</span>
      </div>
      <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
        <div className="h-full rounded-full" style={{ width: `${score}%`, backgroundColor: color }} />
      </div>
    </div>
  );
}

// ── MAPCard ───────────────────────────────────────────────────────────────────
function MAPCard({ map, onClick }: { map: MAPRecord; onClick: () => void }) {
  return (
    <button
      onClick={onClick}
      className={`w-full text-left p-4 rounded-xl border transition-all hover:brightness-110 ${HEALTH_BG[map.map_health]}`}
    >
      <div className="flex items-start justify-between gap-2 mb-2">
        <div>
          <p className="font-semibold text-slate-100 text-sm">{map.deal_name}</p>
          <p className="text-xs text-slate-400">{map.rep_id} · {map.region} · {fmt$(map.deal_value)}</p>
        </div>
        <div className="flex flex-col items-end gap-1">
          <span className={`text-xs font-bold px-2 py-0.5 rounded-full border ${ACTION_BADGE[map.map_action]}`}>
            {map.map_action.replace(/_/g, " ").toUpperCase()}
          </span>
          {map.needs_map_reset && (
            <span className="text-xs text-red-400 font-semibold">🔄 MAP RESET</span>
          )}
        </div>
      </div>
      <div className="flex items-center gap-3 mt-2">
        <div className="relative flex-shrink-0">
          <MAPGauge score={map.map_adherence_composite} health={map.map_health} size={52} />
          <div className="absolute inset-0 flex items-center justify-center">
            <span className={`text-xs font-bold ${HEALTH_COLOR[map.map_health]}`}>
              {map.map_adherence_composite.toFixed(0)}
            </span>
          </div>
        </div>
        <div className="flex-1 space-y-1.5">
          <div className="flex justify-between text-xs">
            <span className="text-slate-400">Health</span>
            <span className={`font-semibold ${HEALTH_COLOR[map.map_health]}`}>{HEALTH_LABEL[map.map_health]}</span>
          </div>
          <DualBar repScore={map.rep_adherence_score} buyerScore={map.buyer_adherence_score} />
        </div>
      </div>
    </button>
  );
}

// ── MAPModal ──────────────────────────────────────────────────────────────────
function MAPModal({ map, onClose }: { map: MAPRecord; onClose: () => void }) {
  const [tab, setTab] = useState<"adherence" | "milestones" | "actions">("adherence");

  useEffect(() => {
    const fn = (e: KeyboardEvent) => e.key === "Escape" && onClose();
    window.addEventListener("keydown", fn);
    return () => window.removeEventListener("keydown", fn);
  }, [onClose]);

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm p-4"
      onClick={(e) => e.target === e.currentTarget && onClose()}
    >
      <div className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-2xl shadow-2xl overflow-hidden">
        {/* header */}
        <div className={`px-6 py-4 border-b border-slate-700 flex items-start justify-between ${HEALTH_BG[map.map_health]}`}>
          <div>
            <h2 className="text-lg font-bold text-slate-100">{map.deal_name}</h2>
            <p className="text-sm text-slate-400">{map.rep_id} · {map.region} · {fmt$(map.deal_value)}</p>
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-white text-xl leading-none">✕</button>
        </div>

        {/* tabs */}
        <div className="flex border-b border-slate-700">
          {(["adherence", "milestones", "actions"] as const).map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`flex-1 py-2.5 text-sm font-medium capitalize transition-colors ${tab === t ? "text-violet-400 border-b-2 border-violet-400" : "text-slate-400 hover:text-slate-200"}`}
            >
              {t === "adherence" ? "MAP Health" : t.charAt(0).toUpperCase() + t.slice(1)}
            </button>
          ))}
        </div>

        {/* body */}
        <div className="p-6 space-y-4">
          {tab === "adherence" && (
            <>
              <div className="flex items-center gap-6">
                <div className="relative">
                  <MAPGauge score={map.map_adherence_composite} health={map.map_health} size={100} />
                  <div className="absolute inset-0 flex flex-col items-center justify-center">
                    <span className={`text-lg font-bold ${HEALTH_COLOR[map.map_health]}`}>{map.map_adherence_composite.toFixed(1)}</span>
                    <span className="text-xs text-slate-400">MAP</span>
                  </div>
                </div>
                <div className="flex-1 grid grid-cols-2 gap-3 text-sm">
                  <div className="bg-slate-800 rounded-lg p-3 text-center">
                    <p className="text-xs text-slate-400">Health</p>
                    <p className={`font-bold ${HEALTH_COLOR[map.map_health]}`}>{HEALTH_LABEL[map.map_health]}</p>
                  </div>
                  <div className="bg-slate-800 rounded-lg p-3 text-center">
                    <p className="text-xs text-slate-400">Pattern</p>
                    <p className="font-bold text-slate-200 text-xs">{PATTERN_LABEL[map.adherence_pattern]}</p>
                  </div>
                  <div className="bg-slate-800 rounded-lg p-3 text-center">
                    <p className="text-xs text-slate-400">Commitment</p>
                    <p className={`font-bold capitalize ${SIGNAL_COLOR[map.commitment_signal]}`}>{map.commitment_signal}</p>
                  </div>
                  <div className="bg-slate-800 rounded-lg p-3 text-center">
                    <p className="text-xs text-slate-400">Close Confidence</p>
                    <p className={`font-bold ${map.estimated_close_confidence >= 60 ? "text-emerald-400" : "text-red-400"}`}>
                      {map.estimated_close_confidence.toFixed(0)}%
                    </p>
                  </div>
                </div>
              </div>
              <div className="space-y-2">
                <DualBar repScore={map.rep_adherence_score} buyerScore={map.buyer_adherence_score} />
              </div>
              {map.days_to_close_risk > 0 && (
                <div className="bg-orange-950 border border-orange-700 rounded-lg p-3 text-sm text-orange-300">
                  ⚠ Current MAP drift may push close date by ~{map.days_to_close_risk} days if not addressed.
                </div>
              )}
              {map.needs_map_reset && (
                <div className="bg-red-950 border border-red-700 rounded-lg p-3 text-sm text-red-300">
                  🔄 MAP requires full reset — current commitments are not being honored by buyer.
                </div>
              )}
            </>
          )}

          {tab === "milestones" && (
            <div className="space-y-3">
              <ScoreBar label="Milestone Progress" score={map.milestone_progress_score} color="#a78bfa" />
              <ScoreBar label="MAP Quality"        score={map.map_quality_score}        color="#60a5fa" />
              <div className="grid grid-cols-2 gap-3 pt-2">
                <div className="bg-slate-800 rounded-lg p-3 text-sm">
                  <p className="text-xs text-slate-400">Rep Adherence</p>
                  <p className="text-blue-300 font-bold">{map.rep_adherence_score.toFixed(1)}/100</p>
                </div>
                <div className="bg-slate-800 rounded-lg p-3 text-sm">
                  <p className="text-xs text-slate-400">Buyer Adherence</p>
                  <p className="text-violet-300 font-bold">{map.buyer_adherence_score.toFixed(1)}/100</p>
                </div>
                <div className="bg-slate-800 rounded-lg p-3 text-sm">
                  <p className="text-xs text-slate-400">Close Risk</p>
                  <p className={`font-bold ${map.days_to_close_risk === 0 ? "text-emerald-400" : "text-orange-400"}`}>
                    {map.days_to_close_risk === 0 ? "None" : `+${map.days_to_close_risk}d`}
                  </p>
                </div>
                <div className="bg-slate-800 rounded-lg p-3 text-sm">
                  <p className="text-xs text-slate-400">Map Reset</p>
                  <p className={`font-bold ${map.needs_map_reset ? "text-red-400" : "text-emerald-400"}`}>
                    {map.needs_map_reset ? "Required" : "Not Needed"}
                  </p>
                </div>
              </div>
            </div>
          )}

          {tab === "actions" && (
            <div className="space-y-3">
              <div className={`rounded-xl p-4 border ${ACTION_BADGE[map.map_action]}`}>
                <p className="text-xs font-semibold uppercase tracking-wide mb-1">Recommended Action</p>
                <p className="font-bold text-lg">{map.map_action.replace(/_/g, " ").toUpperCase()}</p>
              </div>
              {map.map_action === "escalate" && (
                <ul className="text-sm text-slate-300 space-y-2 list-disc list-inside">
                  <li>Escalate to manager — MAP has completely broken down</li>
                  <li>Request executive-to-executive call to requalify deal viability</li>
                  <li>Determine if deal should continue or be disqualified from pipeline</li>
                  <li>If continuing, build a brand new MAP with clear consequences for non-completion</li>
                </ul>
              )}
              {map.map_action === "reset_map" && (
                <ul className="text-sm text-slate-300 space-y-2 list-disc list-inside">
                  <li>Schedule MAP reset meeting with buyer champion and manager</li>
                  <li>Revisit and re-agree every milestone with updated dates</li>
                  <li>Get explicit sign-off from economic buyer on reset commitments</li>
                  <li>Add consequence language — what happens if milestones slip again</li>
                </ul>
              )}
              {map.map_action === "reaffirm" && (
                <ul className="text-sm text-slate-300 space-y-2 list-disc list-inside">
                  <li>Schedule MAP review call within 5 business days</li>
                  <li>Reaffirm specific milestone ownership and dates with buyer</li>
                  <li>Ask buyer to share updated MAP with their internal stakeholders</li>
                  <li>Track daily progress on slipping milestones</li>
                </ul>
              )}
              {map.map_action === "accelerate" && (
                <ul className="text-sm text-slate-300 space-y-2 list-disc list-inside">
                  <li>MAP is healthy — look for opportunities to compress timeline</li>
                  <li>Ask buyer if any milestones can be completed ahead of schedule</li>
                  <li>Introduce any remaining stakeholders that need to be briefed</li>
                  <li>Begin preparing contract and commercial terms in parallel</li>
                </ul>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

// ── Page ──────────────────────────────────────────────────────────────────────
export default function MutualActionPlanPage() {
  const [maps, setMaps]         = useState<MAPRecord[]>([]);
  const [summary, setSummary]   = useState<Summary | null>(null);
  const [loading, setLoading]   = useState(true);
  const [selected, setSelected] = useState<MAPRecord | null>(null);
  const [healthFilter, setHealthFilter]   = useState("all");
  const [patternFilter, setPatternFilter] = useState("all");

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const params = new URLSearchParams();
      if (healthFilter !== "all")  params.set("health", healthFilter);
      if (patternFilter !== "all") params.set("pattern", patternFilter);
      const r = await fetch(`/api/mutual-action-plan?${params}`);
      const j = await r.json();
      setMaps(j.maps);
      setSummary(j.summary);
    } finally {
      setLoading(false);
    }
  }, [healthFilter, patternFilter]);

  useEffect(() => { load(); }, [load]);

  const broken = maps.filter((m) => m.needs_map_reset);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {/* header */}
      <div>
        <h1 className="text-2xl font-bold text-slate-100">Mutual Action Plan Tracker</h1>
        <p className="text-slate-400 text-sm mt-1">Track MAP adherence from both rep and buyer — the strongest predictor of deal close</p>
      </div>

      {/* reset alert */}
      {broken.length > 0 && (
        <div className="bg-red-950 border border-red-700 rounded-xl p-4 flex items-start gap-3">
          <span className="text-red-400 text-xl">🔄</span>
          <div>
            <p className="text-red-300 font-semibold text-sm">{broken.length} MAP{broken.length > 1 ? "s" : ""} require immediate reset or escalation</p>
            <p className="text-red-400/80 text-xs mt-0.5">{broken.map((m) => m.deal_name).join(" · ")}</p>
          </div>
        </div>
      )}

      {/* KPI strip */}
      {summary && (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {[
            { label: "Total MAPs",       value: summary.total },
            { label: "Healthy",          value: `${summary.healthy_map_count} / ${summary.total}` },
            { label: "Reset Needed",     value: summary.reset_needed_count },
            { label: "Avg Adherence",    value: summary.avg_map_adherence_composite.toFixed(1) },
          ].map((k) => (
            <div key={k.label} className="bg-slate-900 border border-slate-800 rounded-xl p-4">
              <p className="text-xs text-slate-400">{k.label}</p>
              <p className="text-2xl font-bold text-slate-100 mt-1">{k.value}</p>
            </div>
          ))}
        </div>
      )}

      {/* health distribution */}
      {summary && (
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
          <h2 className="text-sm font-semibold text-slate-300 mb-4">MAP Health Distribution</h2>
          <HealthDistBar counts={summary.health_counts} total={summary.total} />
        </div>
      )}

      {/* filters */}
      <div className="flex flex-wrap gap-2">
        {["all", "on_track", "slipping", "at_risk", "broken"].map((h) => (
          <button
            key={h}
            onClick={() => setHealthFilter(h)}
            className={`px-3 py-1.5 rounded-full text-xs font-medium border transition-colors ${
              healthFilter === h ? "bg-violet-600 border-violet-500 text-white" : "bg-slate-800 border-slate-700 text-slate-300 hover:border-slate-500"
            }`}
          >
            {h === "all" ? "All Health" : HEALTH_LABEL[h]}
          </button>
        ))}
        <div className="w-px bg-slate-700 mx-1" />
        {["all", "both_committed", "rep_only", "buyer_leading", "buyer_ghosting", "mutual_drift", "complete_breakdown"].map((p) => (
          <button
            key={p}
            onClick={() => setPatternFilter(p)}
            className={`px-3 py-1.5 rounded-full text-xs font-medium border transition-colors ${
              patternFilter === p ? "bg-indigo-600 border-indigo-500 text-white" : "bg-slate-800 border-slate-700 text-slate-300 hover:border-slate-500"
            }`}
          >
            {p === "all" ? "All Patterns" : PATTERN_LABEL[p]}
          </button>
        ))}
      </div>

      {/* avg scores */}
      {summary && (
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-3">
          <h2 className="text-sm font-semibold text-slate-300">Average MAP Scores</h2>
          <ScoreBar label="Rep Adherence"      score={summary.avg_rep_adherence_score}      color="#60a5fa" />
          <ScoreBar label="Buyer Adherence"    score={summary.avg_buyer_adherence_score}    color="#a78bfa" />
          <ScoreBar label="Milestone Progress" score={summary.avg_milestone_progress_score} color="#34d399" />
          <div className="flex justify-between text-xs text-slate-400 pt-1">
            <span>Avg Close Confidence</span>
            <span className="text-emerald-400 font-semibold">{summary.avg_close_confidence.toFixed(1)}%</span>
          </div>
        </div>
      )}

      {/* MAP grid */}
      {loading ? (
        <p className="text-slate-400 text-sm">Loading MAPs…</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
          {maps.map((m) => (
            <MAPCard key={m.deal_id} map={m} onClick={() => setSelected(m)} />
          ))}
        </div>
      )}

      {selected && <MAPModal map={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
