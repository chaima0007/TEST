"use client";

import { useEffect, useState } from "react";

// ── types ────────────────────────────────────────────────────────────────────
interface Deal {
  deal_id: string;
  deal_name: string;
  rep_id: string;
  deal_outcome: string;
  loss_reason: string;
  rep_behavior_pattern: string;
  win_loss_action: string;
  process_quality_score: number;
  execution_score: number;
  relationship_score: number;
  deal_health_score: number;
  win_loss_composite: number;
  win_probability_index: number;
  replication_value: number;
  is_best_practice: boolean;
  needs_coaching: boolean;
  region: string;
}

interface Summary {
  total: number;
  outcome_counts: Record<string, number>;
  loss_reason_counts: Record<string, number>;
  behavior_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_win_loss_composite: number;
  win_rate: number;
  best_practice_count: number;
  coaching_count: number;
  avg_process_quality_score: number;
  avg_execution_score: number;
  avg_relationship_score: number;
  avg_replication_value: number;
}

// ── helpers ──────────────────────────────────────────────────────────────────
const OUTCOME_COLOR: Record<string, string> = {
  closed_won:  "text-emerald-400",
  closed_lost: "text-rose-400",
  no_decision: "text-amber-400",
  churned:     "text-orange-400",
};
const OUTCOME_BG: Record<string, string> = {
  closed_won:  "bg-emerald-500/20 border-emerald-500/40",
  closed_lost: "bg-rose-500/20 border-rose-500/40",
  no_decision: "bg-amber-500/20 border-amber-500/40",
  churned:     "bg-orange-500/20 border-orange-500/40",
};
const OUTCOME_ICON: Record<string, string> = {
  closed_won:  "🏆",
  closed_lost: "❌",
  no_decision: "⏸️",
  churned:     "🔄",
};
const BEHAVIOR_COLOR: Record<string, string> = {
  exemplary:  "text-emerald-400",
  solid:      "text-sky-400",
  improvable: "text-amber-400",
  high_risk:  "text-rose-400",
};
const LOSS_ICON: Record<string, string> = {
  price:         "💰",
  timing:        "⏰",
  competitor:    "⚔️",
  champion_loss: "🚪",
  poor_process:  "⚙️",
  no_loss:       "✅",
};

function WinLossRing({ score, color }: { score: number; color: string }) {
  const r = 36, circ = 2 * Math.PI * r;
  const fill = (score / 100) * circ;
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

function OutcomeDistBar({ counts }: { counts: Record<string, number> }) {
  const order = ["closed_won", "closed_lost", "no_decision", "churned"];
  const colors = ["bg-emerald-500", "bg-rose-500", "bg-amber-500", "bg-orange-500"];
  const total = Object.values(counts).reduce((a, b) => a + b, 0) || 1;
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

// ── DealModal ────────────────────────────────────────────────────────────────
function DealModal({ deal, onClose }: { deal: Deal; onClose: () => void }) {
  const [tab, setTab] = useState<"signals" | "scores" | "coaching">("signals");

  useEffect(() => {
    const esc = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", esc);
    return () => window.removeEventListener("keydown", esc);
  }, [onClose]);

  const ringColor =
    deal.win_loss_composite >= 75 ? "#10b981"
    : deal.win_loss_composite >= 55 ? "#38bdf8"
    : deal.win_loss_composite >= 35 ? "#f59e0b"
    : "#f43f5e";

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
          <WinLossRing score={deal.win_loss_composite} color={ringColor} />
          <div className="flex-1 min-w-0">
            <h2 className="text-white font-bold text-lg truncate">{deal.deal_name}</h2>
            <p className="text-slate-400 text-sm">{deal.rep_id} · {deal.region}</p>
            <div className="flex gap-2 mt-1 flex-wrap">
              <span className={`text-xs px-2 py-0.5 rounded-full border ${OUTCOME_BG[deal.deal_outcome]}`}>
                {OUTCOME_ICON[deal.deal_outcome]} {deal.deal_outcome.replace(/_/g, " ")}
              </span>
              <span className={`text-xs font-medium ${BEHAVIOR_COLOR[deal.rep_behavior_pattern]}`}>
                {deal.rep_behavior_pattern}
              </span>
            </div>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl">✕</button>
        </div>

        {/* tabs */}
        <div className="flex border-b border-slate-800">
          {(["signals", "scores", "coaching"] as const).map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`flex-1 py-2.5 text-sm font-medium capitalize transition-colors ${
                tab === t ? "text-indigo-400 border-b-2 border-indigo-400" : "text-slate-500 hover:text-slate-300"
              }`}
            >
              {t}
            </button>
          ))}
        </div>

        <div className="p-5 space-y-3">
          {tab === "signals" && (
            <>
              <div className="grid grid-cols-2 gap-3">
                {[
                  ["Loss Reason",      LOSS_ICON[deal.loss_reason] + " " + deal.loss_reason.replace(/_/g, " ")],
                  ["Win Probability",  deal.win_probability_index.toFixed(0) + "%"],
                  ["Best Practice",    deal.is_best_practice ? "⭐ Yes" : "No"],
                  ["Needs Coaching",   deal.needs_coaching ? "🎓 Yes" : "✅ No"],
                ].map(([label, value]) => (
                  <div key={label as string} className="bg-slate-800/60 rounded-lg p-3">
                    <div className="text-xs text-slate-400">{label}</div>
                    <div className="text-white font-semibold mt-0.5 text-sm">{value}</div>
                  </div>
                ))}
              </div>
              <div className="bg-slate-800/60 rounded-lg p-3">
                <div className="text-xs text-slate-400 mb-1">Replication Value</div>
                <div className="flex items-center gap-3">
                  <span className="text-2xl font-bold text-white">{deal.replication_value.toFixed(0)}</span>
                  <div className="flex-1 h-2 bg-slate-700 rounded-full">
                    <div
                      className="h-full rounded-full bg-indigo-500"
                      style={{ width: `${deal.replication_value}%` }}
                    />
                  </div>
                </div>
              </div>
            </>
          )}

          {tab === "scores" && (
            <div className="space-y-3">
              <ScoreBar label="Process Quality"  value={deal.process_quality_score} color="bg-indigo-500" />
              <ScoreBar label="Execution"        value={deal.execution_score}        color="bg-violet-500" />
              <ScoreBar label="Relationship"     value={deal.relationship_score}     color="bg-sky-500" />
              <ScoreBar label="Deal Health"      value={deal.deal_health_score}      color="bg-emerald-500" />
            </div>
          )}

          {tab === "coaching" && (
            <div className="space-y-3">
              <div className="bg-indigo-500/10 border border-indigo-500/30 rounded-xl p-4">
                <div className="text-xs text-indigo-400 uppercase tracking-wide mb-1">Recommended Action</div>
                <div className="text-white font-bold text-lg capitalize">
                  {deal.win_loss_action.replace(/_/g, " ")}
                </div>
              </div>
              {deal.is_best_practice && (
                <div className="bg-emerald-500/10 border border-emerald-500/30 rounded-xl p-3 text-sm text-emerald-300">
                  ⭐ Best practice deal — share playbook with the team
                </div>
              )}
              {deal.needs_coaching && (
                <div className="bg-amber-500/10 border border-amber-500/30 rounded-xl p-3 text-sm text-amber-300">
                  🎓 Coaching required — review discovery, MAP usage, and objection handling
                </div>
              )}
              {deal.deal_outcome === "closed_lost" && deal.loss_reason !== "no_loss" && (
                <div className="bg-rose-500/10 border border-rose-500/30 rounded-xl p-3 text-sm text-rose-300">
                  {LOSS_ICON[deal.loss_reason]} Loss reason: {deal.loss_reason.replace(/_/g, " ")} — address in next similar deal
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

// ── DealCard ─────────────────────────────────────────────────────────────────
function DealCard({ deal, onClick }: { deal: Deal; onClick: () => void }) {
  const ringColor =
    deal.win_loss_composite >= 75 ? "#10b981"
    : deal.win_loss_composite >= 55 ? "#38bdf8"
    : deal.win_loss_composite >= 35 ? "#f59e0b"
    : "#f43f5e";

  return (
    <div
      onClick={onClick}
      className="bg-slate-900 border border-slate-800 rounded-xl p-4 cursor-pointer hover:border-indigo-500/50 hover:bg-slate-800/60 transition-all"
    >
      <div className="flex items-center gap-3">
        <WinLossRing score={deal.win_loss_composite} color={ringColor} />
        <div className="flex-1 min-w-0">
          <div className="text-white font-semibold truncate">{deal.deal_name}</div>
          <div className="text-slate-400 text-xs">{deal.rep_id} · {deal.region}</div>
          <div className="flex gap-2 mt-1 flex-wrap">
            <span className={`text-xs px-2 py-0.5 rounded-full border ${OUTCOME_BG[deal.deal_outcome]}`}>
              {OUTCOME_ICON[deal.deal_outcome]} {deal.deal_outcome.replace(/_/g, " ")}
            </span>
          </div>
        </div>
        <div className="text-right shrink-0">
          {deal.is_best_practice && <div className="text-xs text-emerald-400">⭐ BP</div>}
          <div className={`text-sm font-bold mt-1 ${BEHAVIOR_COLOR[deal.rep_behavior_pattern]}`}>
            {deal.rep_behavior_pattern}
          </div>
          {deal.needs_coaching && (
            <div className="text-xs text-amber-400 mt-1">🎓</div>
          )}
        </div>
      </div>
      <div className="mt-2 text-xs text-slate-400">
        {LOSS_ICON[deal.loss_reason]} {deal.loss_reason.replace(/_/g, " ")} · repl: {deal.replication_value.toFixed(0)}
      </div>
    </div>
  );
}

// ── page ─────────────────────────────────────────────────────────────────────
export default function WinLossPatternEnginePage() {
  const [deals, setDeals]       = useState<Deal[]>([]);
  const [summary, setSummary]   = useState<Summary | null>(null);
  const [loading, setLoading]   = useState(true);
  const [selected, setSelected] = useState<Deal | null>(null);
  const [filterOutcome, setFilterOutcome] = useState("all");
  const [filterRegion,  setFilterRegion]  = useState("all");

  useEffect(() => {
    async function load() {
        setLoading(true);
        const params = new URLSearchParams();
        if (filterOutcome !== "all") params.set("outcome", filterOutcome);
        if (filterRegion  !== "all") params.set("region",  filterRegion);
        const res = await fetch(`/api/win-loss-pattern-engine?${params}`);
        const data = await res.json();
        setDeals(data.deals);
        setSummary(data.summary);
        setLoading(false);
  }
    load();
  }, [filterOutcome, filterRegion]);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
      <div className="max-w-6xl mx-auto space-y-6">

        {/* header */}
        <div>
          <h1 className="text-2xl font-bold text-white">Win/Loss Pattern Engine</h1>
          <p className="text-slate-400 text-sm mt-1">
            Extracts rep behavior patterns from closed deals to identify best practices and coaching opportunities
          </p>
        </div>

        {/* KPI strip */}
        {summary && (
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
            {[
              { label: "Total Deals",    value: summary.total },
              { label: "Win Rate",       value: summary.win_rate.toFixed(1) + "%",     color: "text-emerald-400" },
              { label: "Best Practices", value: summary.best_practice_count,           color: "text-indigo-400" },
              { label: "Need Coaching",  value: summary.coaching_count,                color: "text-amber-400" },
            ].map(({ label, value, color }) => (
              <div key={label} className="bg-slate-900 border border-slate-800 rounded-xl p-4">
                <div className="text-xs text-slate-400">{label}</div>
                <div className={`text-2xl font-bold mt-1 ${color ?? "text-white"}`}>{value}</div>
              </div>
            ))}
          </div>
        )}

        {/* outcome dist bar */}
        {summary && (
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-400 mb-2">Outcome Distribution</div>
            <OutcomeDistBar counts={summary.outcome_counts} />
            <div className="flex gap-4 mt-2 text-xs text-slate-500">
              {["closed_won","closed_lost","no_decision","churned"].map((k) => (
                <span key={k} className={OUTCOME_COLOR[k]}>{k.replace(/_/g," ")}: {summary.outcome_counts[k] || 0}</span>
              ))}
            </div>
          </div>
        )}

        {/* filters */}
        <div className="flex flex-wrap gap-2">
          {[
            { label: "All Outcomes",  val: "all" },
            { label: "🏆 Won",        val: "closed_won" },
            { label: "❌ Lost",        val: "closed_lost" },
            { label: "⏸️ No Decision",  val: "no_decision" },
          ].map(({ label, val }) => (
            <button
              key={val}
              onClick={() => setFilterOutcome(val)}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
                filterOutcome === val
                  ? "bg-indigo-600 text-white"
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
            {["NAMER","EMEA","APAC","LATAM"].map((r) => (
              <option key={r} value={r}>{r}</option>
            ))}
          </select>
        </div>

        {/* deals grid */}
        {loading ? (
          <div className="text-slate-400 text-center py-16">Loading deal patterns…</div>
        ) : deals.length === 0 ? (
          <div className="text-slate-500 text-center py-16">No deals match your filters.</div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {deals.map((d) => (
              <DealCard key={d.deal_id} deal={d} onClick={() => setSelected(d)} />
            ))}
          </div>
        )}

        {/* avg score bars */}
        {summary && (
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
            <div className="text-sm font-semibold text-slate-300 mb-4">Average Score Breakdown</div>
            <div className="space-y-3">
              <ScoreBar label="Process Quality"  value={summary.avg_process_quality_score}  color="bg-indigo-500" />
              <ScoreBar label="Execution"        value={summary.avg_execution_score}         color="bg-violet-500" />
              <ScoreBar label="Relationship"     value={summary.avg_relationship_score}      color="bg-sky-500" />
              <ScoreBar label="Replication Value" value={summary.avg_replication_value}      color="bg-emerald-500" />
            </div>
          </div>
        )}
      </div>

      {selected && <DealModal deal={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
