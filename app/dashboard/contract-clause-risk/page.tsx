"use client";

import { useEffect, useState, useCallback } from "react";

// ── types ──────────────────────────────────────────────────────────────────────
interface Contract {
  contract_id: string;
  deal_name: string;
  rep_id: string;
  clause_risk_level: string;
  risky_clause_pattern: string;
  negotiation_stance: string;
  contract_action: string;
  liability_risk_score: number;
  ip_risk_score: number;
  renewal_trap_score: number;
  termination_risk_score: number;
  clause_risk_composite: number;
  estimated_financial_exposure: number;
  clause_negotiability_score: number;
  is_high_risk_contract: boolean;
  needs_legal_escalation: boolean;
  contract_value: number;
  contract_term_months: number;
  region: string;
}

interface Summary {
  total: number;
  risk_counts: Record<string, number>;
  pattern_counts: Record<string, number>;
  stance_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_clause_risk_composite: number;
  total_financial_exposure: number;
  high_risk_count: number;
  legal_escalation_count: number;
  avg_liability_risk_score: number;
  avg_ip_risk_score: number;
  avg_renewal_trap_score: number;
  avg_negotiability_score: number;
}

// ── helpers ────────────────────────────────────────────────────────────────────
const RISK_COLOR: Record<string, string> = {
  low:      "text-emerald-400",
  moderate: "text-yellow-400",
  high:     "text-orange-400",
  critical: "text-red-400",
};
const RISK_BG: Record<string, string> = {
  low:      "bg-emerald-900/30 border-emerald-700",
  moderate: "bg-yellow-900/30 border-yellow-700",
  high:     "bg-orange-900/30 border-orange-700",
  critical: "bg-red-900/30 border-red-700",
};
const ACTION_BADGE: Record<string, string> = {
  proceed:        "bg-emerald-900/50 text-emerald-300 border-emerald-700",
  flag_for_review:"bg-yellow-900/50 text-yellow-300 border-yellow-700",
  redline:        "bg-orange-900/50 text-orange-300 border-orange-700",
  block_signing:  "bg-red-900/50 text-red-300 border-red-700",
};
const PATTERN_LABEL: Record<string, string> = {
  clean:             "Clean",
  liability_exposure:"Liability Exposure",
  ip_conflict:       "IP Conflict",
  renewal_trap:      "Renewal Trap",
  termination_risk:  "Termination Risk",
  multi_clause_risk: "Multi-Clause Risk",
};
const RISK_LABEL: Record<string, string> = {
  low: "Low", moderate: "Moderate", high: "High", critical: "Critical",
};

function fmt$(n: number) {
  if (n >= 1_000_000) return `$${(n / 1_000_000).toFixed(1)}M`;
  if (n >= 1_000)     return `$${(n / 1_000).toFixed(0)}K`;
  return `$${n}`;
}

// ── ClauseGauge ───────────────────────────────────────────────────────────────
function ClauseGauge({ score, size = 90 }: { score: number; size?: number }) {
  const r = (size - 14) / 2;
  const circ = 2 * Math.PI * r;
  const fill = (score / 100) * circ;
  const color = score >= 65 ? "#f87171" : score >= 45 ? "#fb923c" : score >= 25 ? "#facc15" : "#34d399";
  return (
    <svg width={size} height={size} className="rotate-[-90deg]">
      <circle cx={size / 2} cy={size / 2} r={r} fill="none" stroke="#1e293b" strokeWidth={9} />
      <circle
        cx={size / 2} cy={size / 2} r={r}
        fill="none" stroke={color} strokeWidth={9}
        strokeDasharray={`${fill} ${circ}`}
        strokeLinecap="round"
      />
    </svg>
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
        <div className="h-full rounded-full transition-all duration-500" style={{ width: `${score}%`, backgroundColor: color }} />
      </div>
    </div>
  );
}

// ── RiskDistBar ───────────────────────────────────────────────────────────────
function RiskDistBar({ counts, total }: { counts: Record<string, number>; total: number }) {
  const order  = ["low", "moderate", "high", "critical"];
  const colors = ["#34d399", "#facc15", "#fb923c", "#f87171"];
  const labels = ["Low", "Moderate", "High", "Critical"];
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

// ── ContractCard ──────────────────────────────────────────────────────────────
function ContractCard({ contract, onClick }: { contract: Contract; onClick: () => void }) {
  return (
    <button
      onClick={onClick}
      className={`w-full text-left p-4 rounded-xl border transition-all hover:brightness-110 ${RISK_BG[contract.clause_risk_level]}`}
    >
      <div className="flex items-start justify-between gap-2 mb-2">
        <div>
          <p className="font-semibold text-slate-100 text-sm">{contract.deal_name}</p>
          <p className="text-xs text-slate-400">{contract.rep_id} · {contract.region} · {contract.contract_term_months}mo</p>
        </div>
        <div className="flex flex-col items-end gap-1">
          <span className={`text-xs font-bold px-2 py-0.5 rounded-full border ${ACTION_BADGE[contract.contract_action]}`}>
            {contract.contract_action.replace(/_/g, " ").toUpperCase()}
          </span>
          {contract.needs_legal_escalation && (
            <span className="text-xs text-red-400 font-semibold">⚖ LEGAL ESCALATION</span>
          )}
        </div>
      </div>
      <div className="flex items-center gap-3 mt-2">
        <div className="relative w-[52px] h-[52px] flex-shrink-0">
          <ClauseGauge score={contract.clause_risk_composite} size={52} />
          <div className="absolute inset-0 flex items-center justify-center">
            <span className={`text-xs font-bold ${RISK_COLOR[contract.clause_risk_level]}`}>
              {contract.clause_risk_composite.toFixed(0)}
            </span>
          </div>
        </div>
        <div className="flex-1 space-y-1 text-xs text-slate-300">
          <div className="flex justify-between">
            <span>Risk Level</span>
            <span className={`font-semibold ${RISK_COLOR[contract.clause_risk_level]}`}>{RISK_LABEL[contract.clause_risk_level]}</span>
          </div>
          <div className="flex justify-between">
            <span>Pattern</span>
            <span className="font-semibold text-slate-200 text-right max-w-[120px] truncate">{PATTERN_LABEL[contract.risky_clause_pattern]}</span>
          </div>
          <div className="flex justify-between">
            <span>Exposure</span>
            <span className="font-semibold text-red-300">{fmt$(contract.estimated_financial_exposure)}</span>
          </div>
        </div>
      </div>
    </button>
  );
}

// ── ContractModal ─────────────────────────────────────────────────────────────
function ContractModal({ contract, onClose }: { contract: Contract; onClose: () => void }) {
  const [tab, setTab] = useState<"clauses" | "scores" | "actions">("clauses");

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
        <div className={`px-6 py-4 border-b border-slate-700 flex items-start justify-between ${RISK_BG[contract.clause_risk_level]}`}>
          <div>
            <h2 className="text-lg font-bold text-slate-100">{contract.deal_name}</h2>
            <p className="text-sm text-slate-400">{contract.rep_id} · {contract.region} · {fmt$(contract.contract_value)} · {contract.contract_term_months}mo</p>
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-white text-xl leading-none">✕</button>
        </div>

        {/* tabs */}
        <div className="flex border-b border-slate-700">
          {(["clauses", "scores", "actions"] as const).map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`flex-1 py-2.5 text-sm font-medium capitalize transition-colors ${tab === t ? "text-violet-400 border-b-2 border-violet-400" : "text-slate-400 hover:text-slate-200"}`}
            >
              {t === "clauses" ? "Risk Signals" : t.charAt(0).toUpperCase() + t.slice(1)}
            </button>
          ))}
        </div>

        {/* body */}
        <div className="p-6 space-y-4">
          {tab === "clauses" && (
            <>
              <div className="flex items-center gap-6">
                <div className="relative">
                  <ClauseGauge score={contract.clause_risk_composite} size={100} />
                  <div className="absolute inset-0 flex flex-col items-center justify-center">
                    <span className={`text-lg font-bold ${RISK_COLOR[contract.clause_risk_level]}`}>{contract.clause_risk_composite.toFixed(1)}</span>
                    <span className="text-xs text-slate-400">Risk</span>
                  </div>
                </div>
                <div className="flex-1 grid grid-cols-2 gap-3 text-sm">
                  <div className="bg-slate-800 rounded-lg p-3 text-center">
                    <p className="text-xs text-slate-400">Risk Level</p>
                    <p className={`font-bold ${RISK_COLOR[contract.clause_risk_level]}`}>{RISK_LABEL[contract.clause_risk_level]}</p>
                  </div>
                  <div className="bg-slate-800 rounded-lg p-3 text-center">
                    <p className="text-xs text-slate-400">Pattern</p>
                    <p className="font-bold text-slate-200 text-xs">{PATTERN_LABEL[contract.risky_clause_pattern]}</p>
                  </div>
                  <div className="bg-slate-800 rounded-lg p-3 text-center">
                    <p className="text-xs text-slate-400">Exposure</p>
                    <p className="font-bold text-red-300">{fmt$(contract.estimated_financial_exposure)}</p>
                  </div>
                  <div className="bg-slate-800 rounded-lg p-3 text-center">
                    <p className="text-xs text-slate-400">Negotiability</p>
                    <p className="font-bold text-emerald-300">{contract.clause_negotiability_score.toFixed(0)}/100</p>
                  </div>
                </div>
              </div>
              {contract.needs_legal_escalation && (
                <div className="bg-red-950 border border-red-700 rounded-lg p-3 text-sm text-red-300">
                  ⚖ Legal escalation required — this contract contains clauses that cannot be accepted without counsel review.
                </div>
              )}
            </>
          )}

          {tab === "scores" && (
            <div className="space-y-3">
              <ScoreBar label="Liability Risk"     score={contract.liability_risk_score}     color="#f87171" />
              <ScoreBar label="IP Risk"            score={contract.ip_risk_score}            color="#c084fc" />
              <ScoreBar label="Renewal Trap"       score={contract.renewal_trap_score}       color="#fb923c" />
              <ScoreBar label="Termination Risk"   score={contract.termination_risk_score}   color="#facc15" />
              <div className="pt-2 border-t border-slate-700 grid grid-cols-2 gap-4 text-sm">
                <div>
                  <p className="text-xs text-slate-400">Stance</p>
                  <p className="font-semibold text-slate-200">{contract.negotiation_stance.replace(/_/g, " ")}</p>
                </div>
                <div>
                  <p className="text-xs text-slate-400">Is High Risk</p>
                  <p className={`font-semibold ${contract.is_high_risk_contract ? "text-red-400" : "text-emerald-400"}`}>
                    {contract.is_high_risk_contract ? "Yes" : "No"}
                  </p>
                </div>
              </div>
            </div>
          )}

          {tab === "actions" && (
            <div className="space-y-3">
              <div className={`rounded-xl p-4 border ${ACTION_BADGE[contract.contract_action]}`}>
                <p className="text-xs font-semibold uppercase tracking-wide mb-1">Recommended Action</p>
                <p className="font-bold text-lg">{contract.contract_action.replace(/_/g, " ").toUpperCase()}</p>
              </div>
              {contract.contract_action === "block_signing" && (
                <ul className="text-sm text-slate-300 space-y-2 list-disc list-inside">
                  <li>Do NOT proceed to signature — escalate to legal and deal desk immediately</li>
                  <li>Identify which clauses are non-negotiable vs. fallback positions</li>
                  <li>Request vendor&apos;s redline version with explicit clause changes</li>
                  <li>Assess whether deal can survive with modified terms or should be abandoned</li>
                </ul>
              )}
              {contract.contract_action === "redline" && (
                <ul className="text-sm text-slate-300 space-y-2 list-disc list-inside">
                  <li>Issue redline on liability cap, indemnification scope, and IP clauses</li>
                  <li>Negotiate specific caps: liability limited to fees paid in prior 12 months</li>
                  <li>Request mutual indemnification rather than one-sided clauses</li>
                  <li>Include clear data portability obligations before signing</li>
                </ul>
              )}
              {contract.contract_action === "flag_for_review" && (
                <ul className="text-sm text-slate-300 space-y-2 list-disc list-inside">
                  <li>Flag renewal notice window and price increase clause for negotiation</li>
                  <li>Request 90-day cancellation notice in writing before auto-renewal</li>
                  <li>Confirm termination fees are reasonable relative to remaining term</li>
                </ul>
              )}
              {contract.contract_action === "proceed" && (
                <ul className="text-sm text-slate-300 space-y-2 list-disc list-inside">
                  <li>Contract terms are acceptable — proceed to signature</li>
                  <li>Archive all negotiated terms for renewal reference</li>
                  <li>Set calendar reminder 90 days before renewal date</li>
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
export default function ContractClauseRiskPage() {
  const [contracts, setContracts] = useState<Contract[]>([]);
  const [summary, setSummary]     = useState<Summary | null>(null);
  const [loading, setLoading]     = useState(true);
  const [selected, setSelected]   = useState<Contract | null>(null);
  const [riskFilter, setRiskFilter]       = useState("all");
  const [patternFilter, setPatternFilter] = useState("all");

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const params = new URLSearchParams();
      if (riskFilter !== "all")    params.set("risk", riskFilter);
      if (patternFilter !== "all") params.set("pattern", patternFilter);
      const r = await fetch(`/api/contract-clause-risk?${params}`);
      const j = await r.json();
      setContracts(j.contracts);
      setSummary(j.summary);
    } finally {
      setLoading(false);
    }
  }, [riskFilter, patternFilter]);

  useEffect(() => { load(); }, [load]);

  const blocked = contracts.filter((c) => c.needs_legal_escalation);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {/* header */}
      <div>
        <h1 className="text-2xl font-bold text-slate-100">Contract Clause Risk Radar</h1>
        <p className="text-slate-400 text-sm mt-1">Detect liability traps, IP conflicts, renewal snares, and termination risk in contracts before signing</p>
      </div>

      {/* legal escalation alert */}
      {blocked.length > 0 && (
        <div className="bg-red-950 border border-red-700 rounded-xl p-4 flex items-start gap-3">
          <span className="text-red-400 text-xl">⚖</span>
          <div>
            <p className="text-red-300 font-semibold text-sm">{blocked.length} contract{blocked.length > 1 ? "s" : ""} require legal escalation before signing</p>
            <p className="text-red-400/80 text-xs mt-0.5">{blocked.map((c) => c.deal_name).join(" · ")}</p>
          </div>
        </div>
      )}

      {/* KPI strip */}
      {summary && (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {[
            { label: "Total Contracts",      value: summary.total },
            { label: "High Risk / Critical", value: summary.high_risk_count },
            { label: "Total Exposure",       value: fmt$(summary.total_financial_exposure) },
            { label: "Avg Risk Score",       value: summary.avg_clause_risk_composite.toFixed(1) },
          ].map((k) => (
            <div key={k.label} className="bg-slate-900 border border-slate-800 rounded-xl p-4">
              <p className="text-xs text-slate-400">{k.label}</p>
              <p className="text-2xl font-bold text-slate-100 mt-1">{k.value}</p>
            </div>
          ))}
        </div>
      )}

      {/* risk distribution */}
      {summary && (
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
          <h2 className="text-sm font-semibold text-slate-300 mb-4">Clause Risk Distribution</h2>
          <RiskDistBar counts={summary.risk_counts} total={summary.total} />
        </div>
      )}

      {/* filters */}
      <div className="flex flex-wrap gap-2">
        {["all", "low", "moderate", "high", "critical"].map((r) => (
          <button
            key={r}
            onClick={() => setRiskFilter(r)}
            className={`px-3 py-1.5 rounded-full text-xs font-medium border transition-colors ${
              riskFilter === r ? "bg-violet-600 border-violet-500 text-white" : "bg-slate-800 border-slate-700 text-slate-300 hover:border-slate-500"
            }`}
          >
            {r === "all" ? "All Risks" : RISK_LABEL[r]}
          </button>
        ))}
        <div className="w-px bg-slate-700 mx-1" />
        {["all", "clean", "liability_exposure", "ip_conflict", "renewal_trap", "termination_risk", "multi_clause_risk"].map((p) => (
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
          <h2 className="text-sm font-semibold text-slate-300">Average Clause Risk Sub-Scores</h2>
          <ScoreBar label="Liability Risk"   score={summary.avg_liability_risk_score}  color="#f87171" />
          <ScoreBar label="IP Risk"          score={summary.avg_ip_risk_score}          color="#c084fc" />
          <ScoreBar label="Renewal Trap"     score={summary.avg_renewal_trap_score}     color="#fb923c" />
          <div className="flex justify-between text-xs text-slate-400 pt-1">
            <span>Avg Clause Negotiability</span>
            <span className="text-emerald-400 font-semibold">{summary.avg_negotiability_score.toFixed(1)}/100</span>
          </div>
        </div>
      )}

      {/* contract grid */}
      {loading ? (
        <p className="text-slate-400 text-sm">Loading contracts…</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
          {contracts.map((c) => (
            <ContractCard key={c.contract_id} contract={c} onClick={() => setSelected(c)} />
          ))}
        </div>
      )}

      {selected && <ContractModal contract={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
