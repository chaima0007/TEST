"use client";

import { useEffect, useState, useCallback } from "react";

// ── types ─────────────────────────────────────────────────────────────────────

interface Account {
  account_id: string;
  account_name: string;
  industry: string;
  region: string;
  account_tier: string;
  account_health: string;
  engagement_level: string;
  account_action: string;
  health_score: number;
  engagement_score: number;
  growth_score: number;
  fit_score: number;
  churn_risk: number;
  expansion_probability: number;
  composite_score: number;
  is_at_risk: boolean;
  needs_attention: boolean;
  total_mrr: number;
  expansion_mrr: number;
  seats_used: number;
  seats_total: number;
  upsell_opportunities: number;
}

interface Summary {
  total: number;
  tier_counts: Record<string, number>;
  health_counts: Record<string, number>;
  engagement_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_health_score: number;
  avg_composite_score: number;
  at_risk_count: number;
  needs_attention_count: number;
  avg_churn_risk: number;
  avg_expansion_probability: number;
  high_value_count: number;
  avg_growth_score: number;
}

// ── helpers ───────────────────────────────────────────────────────────────────

const HEALTH_COLOR: Record<string, string> = {
  excellent: "text-emerald-400",
  good:      "text-green-400",
  fair:      "text-yellow-400",
  at_risk:   "text-orange-400",
  churning:  "text-red-400",
};

const HEALTH_BG: Record<string, string> = {
  excellent: "bg-emerald-500/20 border-emerald-500/40",
  good:      "bg-green-500/20 border-green-500/40",
  fair:      "bg-yellow-500/20 border-yellow-500/40",
  at_risk:   "bg-orange-500/20 border-orange-500/40",
  churning:  "bg-red-500/20 border-red-500/40",
};

const TIER_COLOR: Record<string, string> = {
  strategic:  "text-violet-400",
  enterprise: "text-indigo-400",
  growth:     "text-sky-400",
  smb:        "text-cyan-400",
  starter:    "text-slate-400",
};

const ACTION_COLOR: Record<string, string> = {
  expand:  "bg-emerald-500/20 text-emerald-300 border-emerald-500/30",
  retain:  "bg-indigo-500/20 text-indigo-300 border-indigo-500/30",
  nurture: "bg-sky-500/20 text-sky-300 border-sky-500/30",
  rescue:  "bg-red-500/20 text-red-300 border-red-500/30",
  monitor: "bg-slate-500/20 text-slate-300 border-slate-500/30",
};

const HEALTH_BAR: Record<string, string> = {
  excellent: "bg-emerald-500",
  good:      "bg-green-500",
  fair:      "bg-yellow-500",
  at_risk:   "bg-orange-500",
  churning:  "bg-red-500",
};

function fmt(label: string) {
  return label.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
}

function fmtMrr(n: number) {
  if (n >= 1000) return `$${(n / 1000).toFixed(1)}k`;
  return `$${n}`;
}

// ── ScoreRing SVG ─────────────────────────────────────────────────────────────

function ScoreRing({
  score,
  label,
  color,
}: {
  score: number;
  label: string;
  color: string;
}) {
  const r = 32;
  const cx = 40;
  const cy = 40;
  const circ = 2 * Math.PI * r;
  const filled = (score / 100) * circ;

  return (
    <div className="flex flex-col items-center gap-1">
      <svg width="80" height="80" viewBox="0 0 80 80">
        <circle cx={cx} cy={cy} r={r} fill="none" stroke="#1e293b" strokeWidth="7" />
        <circle
          cx={cx} cy={cy} r={r}
          fill="none"
          stroke={color}
          strokeWidth="7"
          strokeDasharray={`${filled} ${circ - filled}`}
          strokeDashoffset={circ / 4}
          strokeLinecap="round"
        />
        <text x={cx} y={cy + 5} textAnchor="middle" fill="white" fontSize="14" fontWeight="bold">
          {Math.round(score)}
        </text>
      </svg>
      <span className="text-xs text-slate-400">{label}</span>
    </div>
  );
}

// ── ChurnBar ──────────────────────────────────────────────────────────────────

function ChurnBar({ risk }: { risk: number }) {
  const color =
    risk >= 70 ? "bg-red-500" :
    risk >= 50 ? "bg-orange-500" :
    risk >= 30 ? "bg-yellow-500" : "bg-green-500";

  return (
    <div className="w-full">
      <div className="flex justify-between text-xs text-slate-400 mb-1">
        <span>Churn Risk</span>
        <span className={risk >= 50 ? "text-red-400" : "text-slate-300"}>{risk}%</span>
      </div>
      <div className="w-full bg-slate-700/50 rounded-full h-2">
        <div
          className={`h-2 rounded-full transition-all ${color}`}
          style={{ width: `${Math.min(risk, 100)}%` }}
        />
      </div>
    </div>
  );
}

// ── HealthDistBar ─────────────────────────────────────────────────────────────

function HealthDistBar({ counts, total }: { counts: Record<string, number>; total: number }) {
  const order = ["excellent", "good", "fair", "at_risk", "churning"];
  return (
    <div className="flex rounded-full overflow-hidden h-3 w-full">
      {order.map((k) => {
        const pct = total > 0 ? ((counts[k] || 0) / total) * 100 : 0;
        if (pct === 0) return null;
        return (
          <div
            key={k}
            style={{ width: `${pct}%` }}
            className={`${HEALTH_BAR[k]} transition-all`}
            title={`${k}: ${counts[k] || 0}`}
          />
        );
      })}
    </div>
  );
}

// ── AccountModal ──────────────────────────────────────────────────────────────

function AccountModal({ account, onClose }: { account: Account; onClose: () => void }) {
  const [tab, setTab] = useState<"scores" | "business" | "actions">("scores");

  useEffect(() => {
    const handler = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [onClose]);

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4"
      onClick={onClose}
    >
      <div
        className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-2xl max-h-[90vh] overflow-y-auto"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="p-6 border-b border-slate-800 flex items-start justify-between gap-4">
          <div>
            <div className="flex items-center gap-3 flex-wrap">
              <h2 className="text-xl font-bold text-slate-100">{account.account_name}</h2>
              <span className={`text-xs font-semibold px-2.5 py-0.5 rounded-full border ${ACTION_COLOR[account.account_action]}`}>
                {fmt(account.account_action)}
              </span>
              {account.is_at_risk && (
                <span className="text-xs font-semibold px-2.5 py-0.5 rounded-full bg-red-500/20 text-red-300 border border-red-500/30">
                  At Risk
                </span>
              )}
            </div>
            <p className="text-sm text-slate-400 mt-1">
              <span className={`font-semibold ${TIER_COLOR[account.account_tier]}`}>{fmt(account.account_tier)}</span>
              {" · "}{account.industry}{" · "}{account.region}
            </p>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-slate-300 text-xl leading-none">✕</button>
        </div>

        {/* Tabs */}
        <div className="flex gap-0 border-b border-slate-800">
          {(["scores", "business", "actions"] as const).map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`px-5 py-3 text-sm font-medium border-b-2 transition-colors ${
                tab === t
                  ? "border-indigo-500 text-indigo-400"
                  : "border-transparent text-slate-400 hover:text-slate-300"
              }`}
            >
              {t.charAt(0).toUpperCase() + t.slice(1)}
            </button>
          ))}
        </div>

        <div className="p-6">
          {tab === "scores" && (
            <div className="space-y-6">
              <div className="flex justify-around">
                <ScoreRing score={account.health_score} label="Health" color="#10b981" />
                <ScoreRing score={account.engagement_score} label="Engagement" color="#6366f1" />
                <ScoreRing score={account.growth_score} label="Growth" color="#0ea5e9" />
                <ScoreRing score={account.fit_score} label="Fit" color="#a78bfa" />
              </div>
              <div className="flex justify-center">
                <div className="text-center">
                  <div className="text-4xl font-bold text-white">{account.composite_score}</div>
                  <div className="text-sm text-slate-400">Composite Score</div>
                </div>
              </div>
              <ChurnBar risk={account.churn_risk} />
              <div>
                <div className="flex justify-between text-xs text-slate-400 mb-1">
                  <span>Expansion Probability</span>
                  <span className="text-emerald-400">{account.expansion_probability}%</span>
                </div>
                <div className="w-full bg-slate-700/50 rounded-full h-2">
                  <div
                    className="h-2 rounded-full bg-emerald-500 transition-all"
                    style={{ width: `${Math.min(account.expansion_probability, 100)}%` }}
                  />
                </div>
              </div>
            </div>
          )}

          {tab === "business" && (
            <div className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                {[
                  { label: "Current MRR", value: fmtMrr(account.total_mrr) },
                  { label: "Expansion MRR", value: fmtMrr(account.expansion_mrr) },
                  { label: "Seats Used", value: `${account.seats_used} / ${account.seats_total}` },
                  { label: "Seat Utilisation", value: `${Math.round((account.seats_used / Math.max(1, account.seats_total)) * 100)}%` },
                  { label: "Upsell Opportunities", value: account.upsell_opportunities },
                  { label: "Industry", value: account.industry },
                  { label: "Region", value: account.region },
                  { label: "Needs Attention", value: account.needs_attention ? "Yes" : "No" },
                ].map(({ label, value }) => (
                  <div key={label} className="bg-slate-800/60 rounded-xl p-3">
                    <div className="text-xs text-slate-400 mb-1">{label}</div>
                    <div className="text-base font-semibold text-slate-100">{value}</div>
                  </div>
                ))}
              </div>
              <div>
                <div className="text-xs text-slate-400 mb-2">Seat Utilisation</div>
                <div className="w-full bg-slate-700/50 rounded-full h-3">
                  <div
                    className="h-3 rounded-full bg-indigo-500 transition-all"
                    style={{ width: `${Math.round((account.seats_used / Math.max(1, account.seats_total)) * 100)}%` }}
                  />
                </div>
              </div>
            </div>
          )}

          {tab === "actions" && (
            <div className="space-y-4">
              <div className={`p-4 rounded-xl border ${HEALTH_BG[account.account_health]}`}>
                <div className={`text-sm font-semibold ${HEALTH_COLOR[account.account_health]} mb-1`}>
                  Account Health: {fmt(account.account_health)}
                </div>
                <div className="text-xs text-slate-400">
                  {account.account_health === "churning" && "Immediate intervention required — account showing severe churn signals."}
                  {account.account_health === "at_risk" && "Account at risk — prioritise rescue activities and executive engagement."}
                  {account.account_health === "fair" && "Account needs improvement — focus on feature adoption and engagement."}
                  {account.account_health === "good" && "Account is healthy — maintain momentum and identify expansion signals."}
                  {account.account_health === "excellent" && "Account is thriving — optimise for expansion and advocacy."}
                </div>
              </div>
              <div className="space-y-3">
                {[
                  account.account_action === "rescue" && { label: "Immediate Executive QBR", desc: "Schedule executive business review within 2 weeks" },
                  account.account_action === "rescue" && { label: "Dedicated CSM Assignment", desc: "Assign senior CSM for white-glove recovery plan" },
                  account.account_action === "expand" && { label: "Upsell Discovery Call", desc: `${account.upsell_opportunities} open upsell opportunities identified` },
                  account.account_action === "expand" && { label: "Seat Expansion Proposal", desc: `${account.seats_total - account.seats_used} seat headroom available` },
                  account.account_action === "nurture" && { label: "Engagement Campaign", desc: "Drive product adoption via targeted in-app messaging" },
                  account.account_action === "retain" && { label: "Renewal Preparation", desc: "Prepare renewal package and multi-year options" },
                  account.account_action === "monitor" && { label: "Health Check Cadence", desc: "Set bi-weekly touchpoints to track improvement" },
                  account.needs_attention && { label: "Attention Required", desc: "Account flagged for immediate CSM review" },
                ].filter(Boolean).slice(0, 4).map((item: any) => (
                  <div key={item.label} className="flex items-start gap-3 bg-slate-800/60 rounded-xl p-3">
                    <div className="w-2 h-2 rounded-full bg-indigo-500 mt-1.5 shrink-0" />
                    <div>
                      <div className="text-sm font-medium text-slate-200">{item.label}</div>
                      <div className="text-xs text-slate-400">{item.desc}</div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

// ── AccountCard ───────────────────────────────────────────────────────────────

function AccountCard({ account, onClick }: { account: Account; onClick: () => void }) {
  return (
    <button
      onClick={onClick}
      className="w-full text-left bg-slate-800/60 border border-slate-700/50 rounded-2xl p-5 hover:border-indigo-500/40 hover:bg-slate-800/80 transition-all group"
    >
      <div className="flex items-start justify-between gap-3 mb-3">
        <div>
          <h3 className="font-semibold text-slate-100 group-hover:text-white transition-colors leading-tight">
            {account.account_name}
          </h3>
          <p className="text-xs text-slate-400 mt-0.5">
            <span className={TIER_COLOR[account.account_tier]}>{fmt(account.account_tier)}</span>
            {" · "}{account.industry}
          </p>
        </div>
        <div className="flex flex-col items-end gap-1.5 shrink-0">
          <span className={`text-xs font-semibold px-2 py-0.5 rounded-full border ${ACTION_COLOR[account.account_action]}`}>
            {fmt(account.account_action)}
          </span>
          {account.is_at_risk && (
            <span className="text-xs px-2 py-0.5 rounded-full bg-red-500/20 text-red-300 border border-red-500/30">
              ⚠ At Risk
            </span>
          )}
        </div>
      </div>

      {/* Score pills */}
      <div className="flex gap-2 mb-3 flex-wrap">
        {[
          { label: "Health", value: account.health_score, color: "text-emerald-400" },
          { label: "Engagement", value: account.engagement_score, color: "text-indigo-400" },
          { label: "Growth", value: account.growth_score, color: "text-sky-400" },
        ].map(({ label, value, color }) => (
          <div key={label} className="flex flex-col items-center bg-slate-900/60 rounded-lg px-3 py-1.5">
            <span className={`text-sm font-bold ${color}`}>{Math.round(value)}</span>
            <span className="text-xs text-slate-500">{label}</span>
          </div>
        ))}
        <div className="flex flex-col items-center bg-slate-900/60 rounded-lg px-3 py-1.5">
          <span className="text-sm font-bold text-white">{account.composite_score}</span>
          <span className="text-xs text-slate-500">Total</span>
        </div>
      </div>

      <div className="flex justify-between items-center text-xs text-slate-400">
        <span>{fmtMrr(account.total_mrr)} MRR</span>
        <span className={account.churn_risk >= 50 ? "text-red-400" : "text-slate-400"}>
          Churn {account.churn_risk}%
        </span>
        <span>{account.region}</span>
      </div>
    </button>
  );
}

// ── Page ──────────────────────────────────────────────────────────────────────

export default function AccountScoringPage() {
  const [accounts, setAccounts] = useState<Account[]>([]);
  const [summary, setSummary] = useState<Summary | null>(null);
  const [loading, setLoading] = useState(true);
  const [selected, setSelected] = useState<Account | null>(null);
  const [filterTier, setFilterTier] = useState("all");
  const [filterHealth, setFilterHealth] = useState("all");

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const params = new URLSearchParams();
      if (filterTier   !== "all") params.set("tier",   filterTier);
      if (filterHealth !== "all") params.set("health", filterHealth);
      const res = await fetch(`/api/account-scoring?${params}`);
      const data = await res.json();
      setAccounts(data.accounts ?? []);
      setSummary(data.summary ?? null);
    } finally {
      setLoading(false);
    }
  }, [filterTier, filterHealth]);

  useEffect(() => { load(); }, [load]);

  const tiers   = ["all", "strategic", "enterprise", "growth", "smb", "starter"];
  const healths = ["all", "excellent", "good", "fair", "at_risk", "churning"];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
      {selected && (
        <AccountModal account={selected} onClose={() => setSelected(null)} />
      )}

      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-white">Account Scoring</h1>
        <p className="text-slate-400 mt-1">Health, engagement & growth intelligence across your customer base</p>
      </div>

      {/* KPI Strip */}
      {summary && (
        <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-7 gap-4 mb-8">
          {[
            { label: "Total Accounts", value: summary.total },
            { label: "High Value", value: summary.high_value_count, color: "text-violet-400" },
            { label: "At Risk", value: summary.at_risk_count, color: "text-red-400" },
            { label: "Need Attention", value: summary.needs_attention_count, color: "text-orange-400" },
            { label: "Avg Health", value: `${summary.avg_health_score}`, color: "text-emerald-400" },
            { label: "Avg Composite", value: `${summary.avg_composite_score}` },
            { label: "Avg Churn Risk", value: `${summary.avg_churn_risk}%`, color: "text-red-400" },
          ].map(({ label, value, color }) => (
            <div key={label} className="bg-slate-800/60 border border-slate-700/50 rounded-2xl p-4">
              <div className="text-xs text-slate-400 mb-1">{label}</div>
              <div className={`text-2xl font-bold ${color ?? "text-white"}`}>{value}</div>
            </div>
          ))}
        </div>
      )}

      {/* Health distribution */}
      {summary && (
        <div className="bg-slate-800/60 border border-slate-700/50 rounded-2xl p-5 mb-8">
          <div className="flex items-center justify-between mb-3">
            <h2 className="text-sm font-semibold text-slate-300">Health Distribution</h2>
            <div className="flex gap-3 flex-wrap">
              {["excellent", "good", "fair", "at_risk", "churning"].map((k) => (
                <div key={k} className="flex items-center gap-1.5 text-xs text-slate-400">
                  <div className={`w-2.5 h-2.5 rounded-full ${HEALTH_BAR[k]}`} />
                  {fmt(k)} ({summary.health_counts[k] || 0})
                </div>
              ))}
            </div>
          </div>
          <HealthDistBar counts={summary.health_counts} total={summary.total} />
          <div className="grid grid-cols-3 gap-4 mt-4 text-center">
            <div>
              <div className="text-lg font-bold text-emerald-400">{summary.avg_expansion_probability}%</div>
              <div className="text-xs text-slate-400">Avg Expansion Prob.</div>
            </div>
            <div>
              <div className="text-lg font-bold text-sky-400">{summary.avg_growth_score}</div>
              <div className="text-xs text-slate-400">Avg Growth Score</div>
            </div>
            <div>
              <div className="text-lg font-bold text-red-400">{summary.avg_churn_risk}%</div>
              <div className="text-xs text-slate-400">Avg Churn Risk</div>
            </div>
          </div>
        </div>
      )}

      {/* Filters */}
      <div className="flex flex-wrap gap-3 mb-6">
        <div className="flex flex-wrap gap-2">
          {tiers.map((t) => (
            <button
              key={t}
              onClick={() => setFilterTier(t)}
              className={`px-3 py-1.5 rounded-full text-xs font-medium border transition-colors ${
                filterTier === t
                  ? "bg-indigo-600 border-indigo-500 text-white"
                  : "bg-slate-800/60 border-slate-700 text-slate-400 hover:text-slate-300"
              }`}
            >
              {fmt(t)}
            </button>
          ))}
        </div>
        <div className="flex flex-wrap gap-2">
          {healths.map((h) => (
            <button
              key={h}
              onClick={() => setFilterHealth(h)}
              className={`px-3 py-1.5 rounded-full text-xs font-medium border transition-colors ${
                filterHealth === h
                  ? "bg-indigo-600 border-indigo-500 text-white"
                  : "bg-slate-800/60 border-slate-700 text-slate-400 hover:text-slate-300"
              }`}
            >
              {fmt(h)}
            </button>
          ))}
        </div>
      </div>

      {/* Account Grid */}
      {loading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
          {[...Array(6)].map((_, i) => (
            <div key={i} className="h-44 bg-slate-800/40 rounded-2xl animate-pulse" />
          ))}
        </div>
      ) : accounts.length === 0 ? (
        <div className="text-center py-20 text-slate-500">No accounts match the selected filters.</div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
          {accounts.map((a) => (
            <AccountCard key={a.account_id} account={a} onClick={() => setSelected(a)} />
          ))}
        </div>
      )}
    </div>
  );
}
