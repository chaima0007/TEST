"use client";

import { useEffect, useState, useCallback } from "react";

// ── Types ─────────────────────────────────────────────────────────────────────

interface OnboardingAccount {
  account_id: string;
  account_name: string;
  csm_id: string;
  segment: string;
  current_phase: string;
  onboarding_risk: string;
  success_probability: string;
  onboarding_action: string;
  completion_score: number;
  time_to_value_score: number;
  adoption_velocity: number;
  training_completion_rate: number;
  integration_health: number;
  risk_flags_count: number;
  is_on_track: boolean;
  is_at_risk: boolean;
  contract_start_days: number;
  expected_onboarding_days: number;
  users_activated: number;
  users_licensed: number;
}

interface Summary {
  total: number;
  phase_counts: Record<string, number>;
  risk_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_completion_score: number;
  avg_time_to_value_score: number;
  avg_adoption_velocity: number;
  at_risk_count: number;
  on_track_count: number;
  critical_count: number;
  high_success_count: number;
  escalation_needed_count: number;
}

// ── Helpers ───────────────────────────────────────────────────────────────────

const PHASE_LABELS: Record<string, string> = {
  kickoff: "Kickoff",
  configuration: "Config",
  training: "Training",
  adoption: "Adoption",
  value_realization: "Value Real.",
  complete: "Complete",
};

const RISK_COLORS: Record<string, string> = {
  low: "text-emerald-400",
  medium: "text-amber-400",
  high: "text-orange-400",
  critical: "text-rose-400",
};

const RISK_BG: Record<string, string> = {
  low: "bg-emerald-400/10 border-emerald-400/30",
  medium: "bg-amber-400/10 border-amber-400/30",
  high: "bg-orange-400/10 border-orange-400/30",
  critical: "bg-rose-400/10 border-rose-400/30",
};

const PROB_COLORS: Record<string, string> = {
  high: "text-emerald-400",
  medium: "text-amber-400",
  low: "text-orange-400",
  at_risk: "text-rose-400",
};

const ACTION_COLORS: Record<string, string> = {
  celebrate: "bg-emerald-500/20 text-emerald-300",
  accelerate: "bg-sky-500/20 text-sky-300",
  standard: "bg-slate-500/20 text-slate-300",
  escalate: "bg-orange-500/20 text-orange-300",
  reassign: "bg-amber-500/20 text-amber-300",
  intervene: "bg-rose-500/20 text-rose-300",
};

const ACTION_LABELS: Record<string, string> = {
  celebrate: "Celebrate",
  accelerate: "Accelerate",
  standard: "Standard",
  escalate: "Escalate",
  reassign: "Reassign",
  intervene: "Intervene",
};

function scoreColor(score: number): string {
  if (score >= 75) return "#10b981";
  if (score >= 55) return "#f59e0b";
  if (score >= 35) return "#f97316";
  return "#f43f5e";
}

function CompletionRing({ score, size = 72 }: { score: number; size?: number }) {
  const cx = size / 2, cy = size / 2, r = (size - 10) / 2;
  const circ = 2 * Math.PI * r;
  const arc = (score / 100) * circ;
  const color = scoreColor(score);
  return (
    <svg width={size} height={size} className="flex-shrink-0">
      <circle cx={cx} cy={cy} r={r} fill="none" stroke="#1e293b" strokeWidth={8} />
      <circle
        cx={cx} cy={cy} r={r} fill="none"
        stroke={color} strokeWidth={8}
        strokeDasharray={`${arc} ${circ - arc}`}
        strokeLinecap="round"
        transform={`rotate(-90 ${cx} ${cy})`}
      />
      <text x={cx} y={cy + 1} textAnchor="middle" dominantBaseline="middle"
        fill={color} fontSize={size < 64 ? 11 : 13} fontWeight="700">
        {score.toFixed(0)}
      </text>
    </svg>
  );
}

function PhaseDistBar({ counts }: { counts: Record<string, number> }) {
  const total = Object.values(counts).reduce((s, v) => s + v, 0) || 1;
  const phases = ["kickoff", "configuration", "training", "adoption", "value_realization", "complete"];
  const colors = ["#64748b", "#8b5cf6", "#3b82f6", "#06b6d4", "#10b981", "#34d399"];
  return (
    <div className="w-full space-y-1">
      <div className="flex h-3 rounded-full overflow-hidden gap-px bg-slate-800">
        {phases.map((p, i) =>
          counts[p] ? (
            <div
              key={p}
              style={{ width: `${(counts[p] / total) * 100}%`, background: colors[i] }}
              title={`${PHASE_LABELS[p] ?? p}: ${counts[p]}`}
            />
          ) : null
        )}
      </div>
      <div className="flex flex-wrap gap-x-3 gap-y-1">
        {phases.map((p, i) =>
          counts[p] ? (
            <span key={p} className="flex items-center gap-1 text-[10px] text-slate-400">
              <span className="w-2 h-2 rounded-sm flex-shrink-0" style={{ background: colors[i] }} />
              {PHASE_LABELS[p] ?? p} ({counts[p]})
            </span>
          ) : null
        )}
      </div>
    </div>
  );
}

function BarMini({ value, max = 100, color }: { value: number; max?: number; color: string }) {
  const pct = Math.min(100, (value / max) * 100);
  return (
    <div className="h-1.5 bg-slate-700 rounded-full overflow-hidden">
      <div className="h-full rounded-full transition-all" style={{ width: `${pct}%`, background: color }} />
    </div>
  );
}

// ── Detail Modal ──────────────────────────────────────────────────────────────

function AccountModal({ account, onClose }: { account: OnboardingAccount; onClose: () => void }) {
  const [tab, setTab] = useState<"onboarding" | "health" | "metrics">("onboarding");

  useEffect(() => {
    const handler = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    document.addEventListener("keydown", handler);
    return () => document.removeEventListener("keydown", handler);
  }, [onClose]);

  const color = scoreColor(account.completion_score);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4"
      onClick={(e) => { if (e.target === e.currentTarget) onClose(); }}>
      <div className="absolute inset-0 bg-black/60 backdrop-blur-sm" onClick={onClose} />
      <div className="relative w-full max-w-xl bg-slate-900 border border-slate-700 rounded-2xl shadow-2xl overflow-hidden">

        {/* Header */}
        <div className="flex items-start justify-between p-5 border-b border-slate-800">
          <div className="flex items-center gap-4">
            <CompletionRing score={account.completion_score} size={64} />
            <div>
              <h2 className="text-white font-bold text-lg">{account.account_name}</h2>
              <p className="text-slate-400 text-sm">{account.csm_id} · {account.segment}</p>
              <div className="flex gap-2 mt-1.5 flex-wrap">
                <span className={`px-2 py-0.5 text-[11px] rounded-full border ${RISK_BG[account.onboarding_risk]}`}>
                  <span className={RISK_COLORS[account.onboarding_risk]}>
                    {account.onboarding_risk.toUpperCase()} RISK
                  </span>
                </span>
                <span className={`px-2 py-0.5 text-[11px] rounded-full font-medium ${ACTION_COLORS[account.onboarding_action]}`}>
                  {ACTION_LABELS[account.onboarding_action] ?? account.onboarding_action}
                </span>
              </div>
            </div>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-2xl leading-none p-1">×</button>
        </div>

        {/* Tabs */}
        <div className="flex border-b border-slate-800">
          {(["onboarding", "health", "metrics"] as const).map((t) => (
            <button key={t} onClick={() => setTab(t)}
              className={`flex-1 py-2.5 text-xs font-semibold capitalize transition-colors ${
                tab === t ? "text-indigo-400 border-b-2 border-indigo-400" : "text-slate-500 hover:text-slate-300"
              }`}>
              {t === "onboarding" ? "Onboarding" : t === "health" ? "Health" : "Metrics"}
            </button>
          ))}
        </div>

        {/* Body */}
        <div className="p-5 space-y-4 max-h-80 overflow-y-auto">
          {tab === "onboarding" && (
            <>
              <div className="grid grid-cols-2 gap-3">
                <div className="bg-slate-800/50 rounded-lg p-3">
                  <p className="text-slate-500 text-xs mb-0.5">Phase</p>
                  <p className="text-white text-sm font-semibold capitalize">{PHASE_LABELS[account.current_phase] ?? account.current_phase}</p>
                </div>
                <div className="bg-slate-800/50 rounded-lg p-3">
                  <p className="text-slate-500 text-xs mb-0.5">Success Probability</p>
                  <p className={`text-sm font-semibold uppercase ${PROB_COLORS[account.success_probability]}`}>
                    {account.success_probability.replace("_", " ")}
                  </p>
                </div>
                <div className="bg-slate-800/50 rounded-lg p-3">
                  <p className="text-slate-500 text-xs mb-0.5">Days Started</p>
                  <p className="text-white text-sm font-semibold">{account.contract_start_days} / {account.expected_onboarding_days}d</p>
                </div>
                <div className="bg-slate-800/50 rounded-lg p-3">
                  <p className="text-slate-500 text-xs mb-0.5">Users Activated</p>
                  <p className="text-white text-sm font-semibold">{account.users_activated} / {account.users_licensed}</p>
                </div>
              </div>
              <div>
                <div className="flex justify-between text-xs mb-1">
                  <span className="text-slate-400">Completion Score</span>
                  <span style={{ color }}>{account.completion_score.toFixed(1)}</span>
                </div>
                <BarMini value={account.completion_score} color={color} />
              </div>
              <div>
                <div className="flex justify-between text-xs mb-1">
                  <span className="text-slate-400">Time-to-Value Score</span>
                  <span className="text-sky-400">{account.time_to_value_score.toFixed(1)}</span>
                </div>
                <BarMini value={account.time_to_value_score} color="#38bdf8" />
              </div>
            </>
          )}
          {tab === "health" && (
            <>
              <div className="grid grid-cols-2 gap-3">
                <div className="bg-slate-800/50 rounded-lg p-3">
                  <p className="text-slate-500 text-xs mb-0.5">Risk Flags</p>
                  <p className={`text-sm font-bold ${account.risk_flags_count >= 3 ? "text-rose-400" : account.risk_flags_count >= 1 ? "text-amber-400" : "text-emerald-400"}`}>
                    {account.risk_flags_count}
                  </p>
                </div>
                <div className="bg-slate-800/50 rounded-lg p-3">
                  <p className="text-slate-500 text-xs mb-0.5">On Track</p>
                  <p className={`text-sm font-bold ${account.is_on_track ? "text-emerald-400" : "text-rose-400"}`}>
                    {account.is_on_track ? "Yes" : "No"}
                  </p>
                </div>
                <div className="bg-slate-800/50 rounded-lg p-3">
                  <p className="text-slate-500 text-xs mb-0.5">At Risk</p>
                  <p className={`text-sm font-bold ${account.is_at_risk ? "text-rose-400" : "text-emerald-400"}`}>
                    {account.is_at_risk ? "Yes" : "No"}
                  </p>
                </div>
                <div className="bg-slate-800/50 rounded-lg p-3">
                  <p className="text-slate-500 text-xs mb-0.5">Adoption Velocity</p>
                  <p className="text-white text-sm font-semibold">{account.adoption_velocity.toFixed(1)} users/mo</p>
                </div>
              </div>
              <div>
                <div className="flex justify-between text-xs mb-1">
                  <span className="text-slate-400">Integration Health</span>
                  <span className="text-violet-400">{account.integration_health.toFixed(0)}%</span>
                </div>
                <BarMini value={account.integration_health} color="#8b5cf6" />
              </div>
            </>
          )}
          {tab === "metrics" && (
            <>
              <div className="space-y-3">
                {[
                  { label: "Completion Score", value: account.completion_score, color: color, suffix: "" },
                  { label: "Time-to-Value Score", value: account.time_to_value_score, color: "#38bdf8", suffix: "" },
                  { label: "Training Completion", value: account.training_completion_rate, color: "#f59e0b", suffix: "%" },
                  { label: "Integration Health", value: account.integration_health, color: "#8b5cf6", suffix: "%" },
                ].map(({ label, value, color: c, suffix }) => (
                  <div key={label}>
                    <div className="flex justify-between text-xs mb-1">
                      <span className="text-slate-400">{label}</span>
                      <span style={{ color: c }}>{value.toFixed(1)}{suffix}</span>
                    </div>
                    <BarMini value={value} color={c} />
                  </div>
                ))}
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
}

// ── Account Card ──────────────────────────────────────────────────────────────

function AccountCard({ account, onClick }: { account: OnboardingAccount; onClick: () => void }) {
  const color = scoreColor(account.completion_score);
  return (
    <div
      onClick={onClick}
      className="bg-slate-800/60 border border-slate-700/60 rounded-xl p-4 cursor-pointer hover:border-indigo-500/50 hover:bg-slate-800 transition-all"
    >
      <div className="flex items-start gap-3">
        <CompletionRing score={account.completion_score} size={60} />
        <div className="flex-1 min-w-0">
          <div className="flex items-start justify-between gap-2">
            <div>
              <h3 className="text-white font-semibold text-sm truncate">{account.account_name}</h3>
              <p className="text-slate-500 text-xs">{account.csm_id} · {account.segment}</p>
            </div>
            <span className={`px-2 py-0.5 text-[10px] rounded-full font-medium flex-shrink-0 ${ACTION_COLORS[account.onboarding_action]}`}>
              {ACTION_LABELS[account.onboarding_action] ?? account.onboarding_action}
            </span>
          </div>
          <div className="flex gap-2 mt-1.5 flex-wrap">
            <span className={`text-[10px] font-semibold uppercase ${RISK_COLORS[account.onboarding_risk]}`}>
              {account.onboarding_risk} risk
            </span>
            <span className="text-slate-600 text-[10px]">·</span>
            <span className="text-slate-400 text-[10px] capitalize">
              {PHASE_LABELS[account.current_phase] ?? account.current_phase}
            </span>
            <span className="text-slate-600 text-[10px]">·</span>
            <span className={`text-[10px] font-medium ${PROB_COLORS[account.success_probability]}`}>
              {account.success_probability.replace("_", " ")} prob.
            </span>
          </div>
        </div>
      </div>

      <div className="mt-3 space-y-1.5">
        <div>
          <div className="flex justify-between text-[10px] text-slate-500 mb-0.5">
            <span>Time-to-Value</span>
            <span style={{ color: scoreColor(account.time_to_value_score) }}>{account.time_to_value_score.toFixed(0)}</span>
          </div>
          <BarMini value={account.time_to_value_score} color={scoreColor(account.time_to_value_score)} />
        </div>
        <div>
          <div className="flex justify-between text-[10px] text-slate-500 mb-0.5">
            <span>Training</span>
            <span className="text-amber-400">{account.training_completion_rate.toFixed(0)}%</span>
          </div>
          <BarMini value={account.training_completion_rate} color="#f59e0b" />
        </div>
      </div>

      <div className="mt-2 flex justify-between text-[10px] text-slate-500">
        <span>{account.users_activated}/{account.users_licensed} users</span>
        <span className={account.risk_flags_count >= 3 ? "text-rose-400" : account.risk_flags_count >= 1 ? "text-amber-400" : "text-emerald-400"}>
          {account.risk_flags_count} flag{account.risk_flags_count !== 1 ? "s" : ""}
        </span>
      </div>
    </div>
  );
}

// ── Main Page ─────────────────────────────────────────────────────────────────

export default function CustomerOnboardingPage() {
  const [data, setData] = useState<{ accounts: OnboardingAccount[]; summary: Summary } | null>(null);
  const [loading, setLoading] = useState(true);
  const [selected, setSelected] = useState<OnboardingAccount | null>(null);
  const [filterRisk, setFilterRisk] = useState<string>("all");
  const [filterPhase, setFilterPhase] = useState<string>("all");

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const params = new URLSearchParams();
      if (filterRisk !== "all")  params.set("risk", filterRisk);
      if (filterPhase !== "all") params.set("phase", filterPhase);
      const res = await fetch(`/api/customer-onboarding?${params}`);
      setData(await res.json());
    } finally {
      setLoading(false);
    }
  }, [filterRisk, filterPhase]);

  useEffect(() => { load(); }, [load]);

  const s = data?.summary;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
      {/* Header */}
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-white">Customer Onboarding Intelligence</h1>
        <p className="text-slate-400 text-sm mt-1">Track onboarding health, time-to-value, and intervention signals</p>
      </div>

      {/* KPI Strip */}
      {s && (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-6">
          {[
            { label: "Avg Completion", value: `${s.avg_completion_score}`, sub: "/ 100", color: "text-indigo-400" },
            { label: "At Risk", value: s.at_risk_count, sub: `of ${s.total}`, color: "text-rose-400" },
            { label: "On Track", value: s.on_track_count, sub: `of ${s.total}`, color: "text-emerald-400" },
            { label: "Escalation Needed", value: s.escalation_needed_count, sub: "accounts", color: "text-orange-400" },
          ].map(({ label, value, sub, color }) => (
            <div key={label} className="bg-slate-800/60 border border-slate-700/60 rounded-xl p-4">
              <p className="text-slate-500 text-xs mb-1">{label}</p>
              <p className={`text-2xl font-bold ${color}`}>{value}</p>
              <p className="text-slate-600 text-xs">{sub}</p>
            </div>
          ))}
        </div>
      )}

      {/* Phase Distribution */}
      {s && (
        <div className="bg-slate-800/60 border border-slate-700/60 rounded-xl p-4 mb-6">
          <p className="text-slate-400 text-xs font-semibold uppercase tracking-wider mb-3">Phase Distribution</p>
          <PhaseDistBar counts={s.phase_counts} />
          <div className="mt-3 grid grid-cols-3 gap-2">
            {[
              { label: "Critical", value: s.critical_count, color: "text-rose-400" },
              { label: "High Success", value: s.high_success_count, color: "text-emerald-400" },
              { label: "Avg TTV Score", value: s.avg_time_to_value_score, color: "text-sky-400" },
            ].map(({ label, value, color }) => (
              <div key={label} className="text-center">
                <p className={`text-lg font-bold ${color}`}>{value}</p>
                <p className="text-slate-500 text-[10px]">{label}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Filters */}
      <div className="flex flex-wrap gap-3 mb-5">
        <div className="flex gap-1 flex-wrap">
          <span className="text-slate-500 text-xs self-center mr-1">Risk:</span>
          {["all", "low", "medium", "high", "critical"].map((r) => (
            <button key={r} onClick={() => setFilterRisk(r)}
              className={`px-3 py-1 text-xs rounded-full border transition-colors ${
                filterRisk === r
                  ? "border-indigo-500 bg-indigo-500/20 text-indigo-300"
                  : "border-slate-700 text-slate-400 hover:border-slate-500"
              }`}>
              {r === "all" ? "All" : r.charAt(0).toUpperCase() + r.slice(1)}
            </button>
          ))}
        </div>
        <div className="flex gap-1 flex-wrap">
          <span className="text-slate-500 text-xs self-center mr-1">Phase:</span>
          {["all", "kickoff", "configuration", "training", "adoption", "value_realization", "complete"].map((p) => (
            <button key={p} onClick={() => setFilterPhase(p)}
              className={`px-3 py-1 text-xs rounded-full border transition-colors ${
                filterPhase === p
                  ? "border-violet-500 bg-violet-500/20 text-violet-300"
                  : "border-slate-700 text-slate-400 hover:border-slate-500"
              }`}>
              {p === "all" ? "All" : (PHASE_LABELS[p] ?? p)}
            </button>
          ))}
        </div>
      </div>

      {/* Account Grid */}
      {loading ? (
        <div className="flex justify-center py-20 text-slate-500">Loading…</div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
          {data?.accounts.map((a) => (
            <AccountCard key={a.account_id} account={a} onClick={() => setSelected(a)} />
          ))}
        </div>
      )}

      {/* Detail Modal */}
      {selected && <AccountModal account={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
