"use client";

import { useEffect, useState, useCallback } from "react";

interface AccountRecord {
  account_id: string;
  account_name: string;
  csm_id: string;
  region: string;
  decay_stage: string;
  decay_risk: string;
  primary_decay_signal: string;
  recommended_action: string;
  engagement_score: number;
  support_health_score: number;
  usage_vitality_score: number;
  relationship_score: number;
  decay_composite: number;
  is_at_risk: boolean;
  requires_escalation: boolean;
  estimated_arr_at_risk_usd: number;
  decay_signal: string;
  contract_value_usd: number;
}

interface Summary {
  total: number;
  stage_counts: Record<string, number>;
  risk_counts: Record<string, number>;
  signal_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_decay_composite: number;
  at_risk_count: number;
  escalation_count: number;
  avg_engagement_score: number;
  avg_support_health_score: number;
  avg_usage_vitality_score: number;
  avg_relationship_score: number;
  total_arr_at_risk_usd: number;
}

const STAGE_ORDER = ["stable", "early_warning", "declining", "critical", "churning"];
const STAGE_COLORS: Record<string, string> = {
  stable:        "bg-emerald-900 text-emerald-300",
  early_warning: "bg-sky-900 text-sky-300",
  declining:     "bg-amber-900 text-amber-300",
  critical:      "bg-orange-900 text-orange-300",
  churning:      "bg-red-900 text-red-300",
};
const STAGE_RING: Record<string, string> = {
  stable:        "#10b981",
  early_warning: "#38bdf8",
  declining:     "#f59e0b",
  critical:      "#f97316",
  churning:      "#ef4444",
};
const RISK_COLORS: Record<string, string> = {
  low:      "bg-emerald-900 text-emerald-300",
  moderate: "bg-amber-900 text-amber-300",
  high:     "bg-orange-900 text-orange-300",
  critical: "bg-red-900 text-red-300",
};
const SIGNAL_LABELS: Record<string, string> = {
  none:               "None",
  engagement_drop:    "Engagement Drop",
  support_escalation: "Support Escalation",
  executive_silence:  "Executive Silence",
  nps_decline:        "NPS Decline",
  usage_reduction:    "Usage Reduction",
  payment_delay:      "Payment Delay",
};
const ACTION_LABELS: Record<string, string> = {
  no_action:              "No Action",
  monitor:                "Monitor",
  proactive_outreach:     "Proactive Outreach",
  executive_escalation:   "Executive Escalation",
  emergency_intervention: "Emergency Intervention",
};

function decayColor(v: number) {
  if (v < 20) return "#10b981";
  if (v < 40) return "#f59e0b";
  if (v < 60) return "#f97316";
  return "#ef4444";
}

function fmt(n: number) {
  return n >= 1_000_000 ? `$${(n / 1_000_000).toFixed(1)}M` : n >= 1_000 ? `$${(n / 1_000).toFixed(0)}K` : `$${n.toFixed(0)}`;
}

function ScoreBar({ label, value, color }: { label: string; value: number; color: string }) {
  return (
    <div>
      <div className="flex justify-between text-xs text-slate-400 mb-1">
        <span>{label}</span><span className="text-slate-200">{value.toFixed(0)}</span>
      </div>
      <div className="h-1.5 bg-slate-700 rounded-full overflow-hidden">
        <div className="h-full rounded-full" style={{ width: `${Math.min(value, 100)}%`, backgroundColor: color }} />
      </div>
    </div>
  );
}

function CompositeRing({ value, stage }: { value: number; stage: string }) {
  const r = 28; const circ = 2 * Math.PI * r;
  const fill = (Math.min(value, 100) / 100) * circ;
  const color = STAGE_RING[stage] ?? "#475569";
  return (
    <svg width="72" height="72" viewBox="0 0 72 72">
      <circle cx="36" cy="36" r={r} fill="none" stroke="#1e293b" strokeWidth="7" />
      <circle cx="36" cy="36" r={r} fill="none" stroke={color} strokeWidth="7"
        strokeDasharray={`${fill} ${circ}`} strokeLinecap="round" transform="rotate(-90 36 36)" />
      <text x="36" y="40" textAnchor="middle" fill={color} fontSize="13" fontWeight="bold">{value.toFixed(0)}</text>
    </svg>
  );
}

function DetailModal({ account, onClose }: { account: AccountRecord; onClose: () => void }) {
  const [tab, setTab] = useState(0);
  useEffect(() => {
    const fn = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", fn); return () => window.removeEventListener("keydown", fn);
  }, [onClose]);
  const tabs = ["Overview", "Decay Scores", "Intervention"];
  const stageCls = STAGE_COLORS[account.decay_stage] ?? "bg-slate-700 text-slate-300";
  const riskCls  = RISK_COLORS[account.decay_risk]   ?? "bg-slate-700 text-slate-300";
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4" onClick={onClose}>
      <div className="absolute inset-0 bg-black/70" />
      <div className="relative bg-slate-900 border border-slate-700 rounded-2xl shadow-2xl w-full max-w-lg" onClick={(e) => e.stopPropagation()}>
        <div className="flex items-start justify-between p-6 border-b border-slate-800">
          <div>
            <h2 className="text-lg font-semibold text-slate-100">{account.account_name}</h2>
            <p className="text-sm text-slate-400">{account.csm_id} · {account.region} · {fmt(account.contract_value_usd)} ARR</p>
            <div className="flex gap-2 mt-2 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${stageCls}`}>{account.decay_stage.replace("_", " ")}</span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${riskCls}`}>{account.decay_risk}</span>
              {account.is_at_risk && <span className="px-2 py-0.5 rounded text-xs font-medium bg-red-900 text-red-300">⚠ At Risk</span>}
              {account.requires_escalation && <span className="px-2 py-0.5 rounded text-xs font-medium bg-orange-900 text-orange-300">🔥 Escalate</span>}
            </div>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-slate-300 text-xl ml-4">✕</button>
        </div>
        <div className="flex border-b border-slate-800">
          {tabs.map((t, i) => (
            <button key={t} onClick={() => setTab(i)}
              className={`flex-1 py-3 text-sm font-medium transition-colors ${tab === i ? "text-indigo-400 border-b-2 border-indigo-400" : "text-slate-500 hover:text-slate-300"}`}>
              {t}
            </button>
          ))}
        </div>
        <div className="p-6">
          {tab === 0 && (
            <div className="space-y-4">
              <div className="flex items-center gap-4 p-4 bg-slate-800 rounded-xl">
                <CompositeRing value={account.decay_composite} stage={account.decay_stage} />
                <div>
                  <p className="text-xs text-slate-400">Decay Composite</p>
                  <p className="text-2xl font-bold text-slate-100">{account.decay_composite.toFixed(1)}</p>
                  <p className="text-xs text-slate-400 mt-1">ARR at risk: {fmt(account.estimated_arr_at_risk_usd)}</p>
                </div>
              </div>
              <div className="p-4 bg-slate-800 rounded-xl">
                <p className="text-xs text-slate-400 mb-1">Decay Signal</p>
                <p className="text-sm text-slate-200">{account.decay_signal}</p>
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div className="p-3 bg-slate-800 rounded-lg">
                  <p className="text-xs text-slate-400">Primary Signal</p>
                  <p className="text-slate-200 font-medium">{SIGNAL_LABELS[account.primary_decay_signal] ?? account.primary_decay_signal}</p>
                </div>
                <div className="p-3 bg-slate-800 rounded-lg">
                  <p className="text-xs text-slate-400">ARR at Risk</p>
                  <p className="text-orange-300 font-medium">{fmt(account.estimated_arr_at_risk_usd)}</p>
                </div>
              </div>
            </div>
          )}
          {tab === 1 && (
            <div className="space-y-4">
              <ScoreBar label="Engagement Risk"      value={account.engagement_score}      color={decayColor(account.engagement_score)} />
              <ScoreBar label="Support Health Risk"  value={account.support_health_score}  color={decayColor(account.support_health_score)} />
              <ScoreBar label="Usage Vitality Risk"  value={account.usage_vitality_score}  color={decayColor(account.usage_vitality_score)} />
              <ScoreBar label="Relationship Risk"    value={account.relationship_score}    color={decayColor(account.relationship_score)} />
              <div className="mt-4 p-3 bg-slate-800 rounded-lg text-xs text-slate-400">
                Composite = Engagement×0.30 + Support×0.25 + Usage×0.25 + Relationship×0.20
              </div>
            </div>
          )}
          {tab === 2 && (
            <div className="space-y-4">
              <div className="p-4 bg-slate-800 rounded-xl">
                <p className="text-xs text-slate-400 mb-1">Recommended Action</p>
                <p className="text-lg font-semibold text-indigo-300">{ACTION_LABELS[account.recommended_action] ?? account.recommended_action}</p>
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div className={`p-3 rounded-lg ${account.is_at_risk ? "bg-red-900/50 border border-red-700" : "bg-slate-800"}`}>
                  <p className="text-xs text-slate-400">At Risk</p>
                  <p className={`font-semibold ${account.is_at_risk ? "text-red-300" : "text-emerald-400"}`}>{account.is_at_risk ? "YES" : "No"}</p>
                </div>
                <div className={`p-3 rounded-lg ${account.requires_escalation ? "bg-orange-900/50 border border-orange-700" : "bg-slate-800"}`}>
                  <p className="text-xs text-slate-400">Escalation</p>
                  <p className={`font-semibold ${account.requires_escalation ? "text-orange-300" : "text-emerald-400"}`}>{account.requires_escalation ? "REQUIRED" : "No"}</p>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default function CustomerSentimentDecayEnginePage() {
  const [data, setData]     = useState<{ accounts: AccountRecord[]; summary: Summary } | null>(null);
  const [filter, setFilter] = useState("all");
  const [selected, setSelected] = useState<AccountRecord | null>(null);

  const load = useCallback((stage?: string) => {
    const params = stage && stage !== "all" ? `?stage=${stage}` : "";
    fetch(`/api/customer-sentiment-decay-engine${params}`).then((r) => r.json()).then(setData);
  }, []);

  useEffect(() => { load(); }, [load]);
  const handleFilter = (f: string) => { setFilter(f); load(f === "all" ? undefined : f); };

  if (!data) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-slate-400 animate-pulse">Loading sentiment decay engine...</div>
    </div>
  );

  const { accounts, summary } = data;
  const stageTotal  = Object.values(summary.stage_counts).reduce((a, b) => a + b, 0) || 1;
  const signalTotal = Object.values(summary.signal_counts).reduce((a, b) => a + b, 0) || 1;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
      {selected && <DetailModal account={selected} onClose={() => setSelected(null)} />}
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-slate-100">Customer Sentiment Decay Engine</h1>
        <p className="text-slate-400 text-sm mt-1">Early churn detection · NPS erosion tracking · executive engagement monitoring</p>
      </div>

      {/* KPI Strip */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        {[
          { label: "Total Accounts", value: summary.total, sub: "monitored" },
          { label: "At Risk", value: summary.at_risk_count, sub: "flagged", alert: summary.at_risk_count > 0 },
          { label: "Escalation Needed", value: summary.escalation_count, sub: "urgent", alert: summary.escalation_count > 0 },
          { label: "ARR at Risk", value: fmt(summary.total_arr_at_risk_usd), sub: "total exposure" },
        ].map(({ label, value, sub, alert }) => (
          <div key={label} className={`bg-slate-900 border rounded-xl p-4 ${alert ? "border-red-700" : "border-slate-800"}`}>
            <p className="text-xs text-slate-400">{label}</p>
            <p className={`text-2xl font-bold mt-1 ${alert ? "text-red-400" : "text-slate-100"}`}>{value}</p>
            <p className="text-xs text-slate-500 mt-1">{sub}</p>
          </div>
        ))}
      </div>

      {/* Avg Scores + Distributions */}
      <div className="grid lg:grid-cols-2 gap-4 mb-6">
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
          <h2 className="text-sm font-semibold text-slate-300 mb-4">Avg Decay Sub-Scores</h2>
          <div className="space-y-3">
            {[
              { label: "Engagement Risk",     value: summary.avg_engagement_score },
              { label: "Support Health Risk", value: summary.avg_support_health_score },
              { label: "Usage Vitality Risk", value: summary.avg_usage_vitality_score },
              { label: "Relationship Risk",   value: summary.avg_relationship_score },
            ].map(({ label, value }) => (
              <div key={label}>
                <div className="flex justify-between text-xs text-slate-400 mb-1">
                  <span>{label}</span><span className="text-slate-200">{value.toFixed(1)}</span>
                </div>
                <div className="h-2 bg-slate-700 rounded-full overflow-hidden">
                  <div className="h-full rounded-full" style={{ width: `${Math.min(value, 100)}%`, backgroundColor: decayColor(value) }} />
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-4">
          <div>
            <h2 className="text-sm font-semibold text-slate-300 mb-3">Decay Stage Distribution</h2>
            <div className="space-y-2">
              {STAGE_ORDER.map((st) => {
                const cnt = summary.stage_counts[st] ?? 0;
                return (
                  <div key={st} className="flex items-center gap-2 text-xs">
                    <span className="w-24 text-slate-400">{st.replace("_", " ")}</span>
                    <div className="flex-1 h-2 bg-slate-700 rounded-full overflow-hidden">
                      <div className="h-full rounded-full" style={{ width: `${(cnt / stageTotal) * 100}%`, backgroundColor: STAGE_RING[st] }} />
                    </div>
                    <span className="w-5 text-right text-slate-300">{cnt}</span>
                  </div>
                );
              })}
            </div>
          </div>
          <div>
            <h2 className="text-sm font-semibold text-slate-300 mb-3">Decay Signal Distribution</h2>
            <div className="space-y-1.5">
              {Object.entries(summary.signal_counts).map(([sig, cnt]) => (
                <div key={sig} className="flex items-center gap-2 text-xs">
                  <span className="w-36 text-slate-400">{SIGNAL_LABELS[sig] ?? sig}</span>
                  <div className="flex-1 h-1.5 bg-slate-700 rounded-full overflow-hidden">
                    <div className="h-full rounded-full bg-violet-500" style={{ width: `${(cnt / signalTotal) * 100}%` }} />
                  </div>
                  <span className="w-5 text-right text-slate-300">{cnt}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Filter tabs */}
      <div className="flex flex-wrap gap-2 mb-4">
        {["all", ...STAGE_ORDER].map((st) => (
          <button key={st} onClick={() => handleFilter(st)}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
              filter === st ? "bg-indigo-600 text-white" : "bg-slate-800 text-slate-400 hover:text-slate-200"
            }`}>
            {st === "all" ? "All Accounts" : st.replace("_", " ").charAt(0).toUpperCase() + st.replace("_", " ").slice(1)}
            {st !== "all" && (summary.stage_counts[st] ?? 0) > 0 && (
              <span className="ml-1 text-slate-400">({summary.stage_counts[st]})</span>
            )}
          </button>
        ))}
      </div>

      {/* Account Cards */}
      <div className="grid sm:grid-cols-2 xl:grid-cols-3 gap-4">
        {accounts.map((a) => {
          const stageCls = STAGE_COLORS[a.decay_stage] ?? "bg-slate-700 text-slate-300";
          const riskCls  = RISK_COLORS[a.decay_risk]   ?? "bg-slate-700 text-slate-300";
          return (
            <div key={a.account_id} onClick={() => setSelected(a)}
              className="bg-slate-900 border border-slate-800 rounded-xl p-4 cursor-pointer hover:border-slate-600 transition-colors">
              <div className="flex items-start justify-between mb-3">
                <div>
                  <p className="font-semibold text-slate-100">{a.account_name}</p>
                  <p className="text-xs text-slate-400">{a.csm_id} · {a.region}</p>
                  <p className="text-xs text-slate-500 mt-0.5">{fmt(a.contract_value_usd)} ARR</p>
                </div>
                <div className="flex flex-col gap-1 items-end">
                  <span className={`px-2 py-0.5 rounded text-xs font-medium ${stageCls}`}>{a.decay_stage.replace("_", " ")}</span>
                  <span className={`px-2 py-0.5 rounded text-xs font-medium ${riskCls}`}>{a.decay_risk}</span>
                </div>
              </div>
              <div className="flex items-center gap-3 mb-3">
                <CompositeRing value={a.decay_composite} stage={a.decay_stage} />
                <div className="flex-1 space-y-1.5">
                  <ScoreBar label="Engagement"   value={a.engagement_score}      color={decayColor(a.engagement_score)} />
                  <ScoreBar label="Support"      value={a.support_health_score}  color={decayColor(a.support_health_score)} />
                  <ScoreBar label="Usage"        value={a.usage_vitality_score}  color={decayColor(a.usage_vitality_score)} />
                  <ScoreBar label="Relationship" value={a.relationship_score}    color={decayColor(a.relationship_score)} />
                </div>
              </div>
              <div className="flex gap-2 flex-wrap mb-2">
                {a.is_at_risk && <span className="text-xs text-red-400 bg-red-900/40 px-2 py-0.5 rounded">⚠ At Risk</span>}
                {a.requires_escalation && <span className="text-xs text-orange-300 bg-orange-900/40 px-2 py-0.5 rounded">🔥 Escalate</span>}
                <span className="text-xs text-amber-300 bg-amber-900/30 px-2 py-0.5 rounded">{fmt(a.estimated_arr_at_risk_usd)} at risk</span>
              </div>
              <p className="text-xs text-slate-400 line-clamp-2">{a.decay_signal}</p>
            </div>
          );
        })}
      </div>
    </div>
  );
}
