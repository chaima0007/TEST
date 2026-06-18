"use client";

import { useEffect, useState, useCallback } from "react";

// ── types ──────────────────────────────────────────────────────────────────────
interface DriftDeal {
  deal_id: string;
  deal_name: string;
  rep_id: string;
  drift_severity: string;
  drift_pattern: string;
  buyer_alignment: string;
  drift_action: string;
  level_drift_score: number;
  function_drift_score: number;
  exec_disengagement_score: number;
  committee_dilution_score: number;
  persona_drift_composite: number;
  deal_misalignment_risk: number;
  realignment_probability: number;
  is_drifted: boolean;
  needs_exec_reengagement: boolean;
  deal_value: number;
  target_persona_level: string;
  current_primary_contact_level: string;
  target_persona_function: string;
  current_primary_contact_function: string;
  region: string;
}

interface Summary {
  total: number;
  severity_counts: Record<string, number>;
  pattern_counts: Record<string, number>;
  alignment_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_persona_drift_composite: number;
  total_misalignment_risk: number;
  drifted_count: number;
  exec_reengagement_count: number;
  avg_level_drift_score: number;
  avg_function_drift_score: number;
  avg_exec_disengagement_score: number;
  avg_realignment_probability: number;
}

// ── helpers ────────────────────────────────────────────────────────────────────
const SEV_COLOR: Record<string, string> = {
  aligned:       "text-emerald-400",
  minor_drift:   "text-yellow-400",
  moderate_drift:"text-orange-400",
  severe_drift:  "text-red-400",
};
const SEV_BG: Record<string, string> = {
  aligned:       "bg-emerald-900/40 border-emerald-700",
  minor_drift:   "bg-yellow-900/40 border-yellow-700",
  moderate_drift:"bg-orange-900/40 border-orange-700",
  severe_drift:  "bg-red-900/40 border-red-700",
};
const ACTION_COLOR: Record<string, string> = {
  maintain:       "bg-emerald-900/50 text-emerald-300 border-emerald-700",
  requalify:      "bg-yellow-900/50 text-yellow-300 border-yellow-700",
  re_engage_exec: "bg-orange-900/50 text-orange-300 border-orange-700",
  realign_now:    "bg-red-900/50 text-red-300 border-red-700",
};
const PATTERN_LABEL: Record<string, string> = {
  no_drift:           "No Drift",
  level_downgrade:    "Level Downgrade",
  function_shift:     "Function Shift",
  sponsor_loss:       "Sponsor Loss",
  committee_dilution: "Committee Dilution",
  multi_drift:        "Multi-Signal Drift",
};
const SEV_LABEL: Record<string, string> = {
  aligned:        "Aligned",
  minor_drift:    "Minor Drift",
  moderate_drift: "Moderate Drift",
  severe_drift:   "Severe Drift",
};

function fmt$(n: number) {
  if (n >= 1_000_000) return `$${(n / 1_000_000).toFixed(1)}M`;
  if (n >= 1_000)     return `$${(n / 1_000).toFixed(0)}K`;
  return `$${n}`;
}

// ── DriftRing SVG ─────────────────────────────────────────────────────────────
function DriftRing({ score, size = 100 }: { score: number; size?: number }) {
  const r = (size - 16) / 2;
  const circ = 2 * Math.PI * r;
  const fill = (score / 100) * circ;
  const color = score >= 65 ? "#f87171" : score >= 45 ? "#fb923c" : score >= 25 ? "#facc15" : "#34d399";
  return (
    <svg width={size} height={size} className="rotate-[-90deg]">
      <circle cx={size / 2} cy={size / 2} r={r} fill="none" stroke="#1e293b" strokeWidth={10} />
      <circle
        cx={size / 2} cy={size / 2} r={r}
        fill="none" stroke={color} strokeWidth={10}
        strokeDasharray={`${fill} ${circ}`}
        strokeLinecap="round"
        style={{ transition: "stroke-dasharray 0.6s ease" }}
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

// ── AlignmentBar distribution ─────────────────────────────────────────────────
function AlignmentBar({ counts, total }: { counts: Record<string, number>; total: number }) {
  const order = ["strongly_aligned", "partially_aligned", "misaligned", "disconnected"];
  const colors = ["#34d399", "#facc15", "#fb923c", "#f87171"];
  const labels = ["Aligned", "Partial", "Misaligned", "Disconnected"];
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

// ── DealCard ──────────────────────────────────────────────────────────────────
function DealCard({ deal, onClick }: { deal: DriftDeal; onClick: () => void }) {
  return (
    <button
      onClick={onClick}
      className={`w-full text-left p-4 rounded-xl border transition-all hover:brightness-110 ${SEV_BG[deal.drift_severity]}`}
    >
      <div className="flex items-start justify-between gap-2 mb-2">
        <div>
          <p className="font-semibold text-slate-100 text-sm">{deal.deal_name}</p>
          <p className="text-xs text-slate-400">{deal.rep_id} · {deal.region}</p>
        </div>
        <div className="flex flex-col items-end gap-1">
          <span className={`text-xs font-bold px-2 py-0.5 rounded-full border ${ACTION_COLOR[deal.drift_action]}`}>
            {deal.drift_action.replace(/_/g, " ").toUpperCase()}
          </span>
          {deal.needs_exec_reengagement && (
            <span className="text-xs text-red-400 font-semibold">EXEC NEEDED</span>
          )}
        </div>
      </div>
      <div className="flex items-center gap-3 mt-2">
        <DriftRing score={deal.persona_drift_composite} size={52} />
        <div className="flex-1 space-y-1 text-xs text-slate-300">
          <div className="flex justify-between">
            <span>Severity</span>
            <span className={`font-semibold ${SEV_COLOR[deal.drift_severity]}`}>{SEV_LABEL[deal.drift_severity]}</span>
          </div>
          <div className="flex justify-between">
            <span>Pattern</span>
            <span className="font-semibold text-slate-200">{PATTERN_LABEL[deal.drift_pattern]}</span>
          </div>
          <div className="flex justify-between">
            <span>At Risk</span>
            <span className="font-semibold text-red-300">{fmt$(deal.deal_misalignment_risk)}</span>
          </div>
        </div>
      </div>
    </button>
  );
}

// ── DealModal ─────────────────────────────────────────────────────────────────
function DealModal({ deal, onClose }: { deal: DriftDeal; onClose: () => void }) {
  const [tab, setTab] = useState<"signals" | "personas" | "actions">("signals");

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
        <div className={`px-6 py-4 border-b border-slate-700 flex items-start justify-between ${SEV_BG[deal.drift_severity]}`}>
          <div>
            <h2 className="text-lg font-bold text-slate-100">{deal.deal_name}</h2>
            <p className="text-sm text-slate-400">{deal.rep_id} · {deal.region} · {fmt$(deal.deal_value)}</p>
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-white text-xl leading-none">✕</button>
        </div>

        {/* tabs */}
        <div className="flex border-b border-slate-700">
          {(["signals", "personas", "actions"] as const).map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`flex-1 py-2.5 text-sm font-medium capitalize transition-colors ${tab === t ? "text-violet-400 border-b-2 border-violet-400" : "text-slate-400 hover:text-slate-200"}`}
            >
              {t === "personas" ? "Persona Gap" : t.charAt(0).toUpperCase() + t.slice(1)}
            </button>
          ))}
        </div>

        {/* body */}
        <div className="p-6 space-y-4">
          {tab === "signals" && (
            <>
              <div className="flex items-center gap-6">
                <div className="relative">
                  <DriftRing score={deal.persona_drift_composite} size={100} />
                  <div className="absolute inset-0 flex flex-col items-center justify-center">
                    <span className={`text-lg font-bold ${SEV_COLOR[deal.drift_severity]}`}>{deal.persona_drift_composite.toFixed(1)}</span>
                    <span className="text-xs text-slate-400">Drift</span>
                  </div>
                </div>
                <div className="flex-1 grid grid-cols-2 gap-3 text-sm">
                  <div className="bg-slate-800 rounded-lg p-3 text-center">
                    <p className="text-xs text-slate-400">Severity</p>
                    <p className={`font-bold ${SEV_COLOR[deal.drift_severity]}`}>{SEV_LABEL[deal.drift_severity]}</p>
                  </div>
                  <div className="bg-slate-800 rounded-lg p-3 text-center">
                    <p className="text-xs text-slate-400">Pattern</p>
                    <p className="font-bold text-slate-200 text-xs">{PATTERN_LABEL[deal.drift_pattern]}</p>
                  </div>
                  <div className="bg-slate-800 rounded-lg p-3 text-center">
                    <p className="text-xs text-slate-400">At Risk</p>
                    <p className="font-bold text-red-300">{fmt$(deal.deal_misalignment_risk)}</p>
                  </div>
                  <div className="bg-slate-800 rounded-lg p-3 text-center">
                    <p className="text-xs text-slate-400">Realign Prob.</p>
                    <p className="font-bold text-emerald-300">{deal.realignment_probability.toFixed(0)}%</p>
                  </div>
                </div>
              </div>
              <div className="space-y-2">
                <ScoreBar label="Level Drift"          score={deal.level_drift_score}          color="#f87171" />
                <ScoreBar label="Function Drift"       score={deal.function_drift_score}       color="#fb923c" />
                <ScoreBar label="Exec Disengagement"   score={deal.exec_disengagement_score}   color="#facc15" />
                <ScoreBar label="Committee Dilution"   score={deal.committee_dilution_score}   color="#a78bfa" />
              </div>
              {deal.needs_exec_reengagement && (
                <div className="bg-red-950 border border-red-700 rounded-lg p-3 text-sm text-red-300">
                  ⚠ Executive re-engagement required immediately — deal at risk of collapse without sponsor alignment.
                </div>
              )}
            </>
          )}

          {tab === "personas" && (
            <div className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div className="bg-slate-800 rounded-xl p-4">
                  <p className="text-xs text-slate-400 mb-2 font-semibold uppercase tracking-wide">Target Persona</p>
                  <p className="text-slate-100 font-bold">{deal.target_persona_level}</p>
                  <p className="text-slate-300 text-sm">{deal.target_persona_function}</p>
                </div>
                <div className={`rounded-xl p-4 border ${SEV_BG[deal.drift_severity]}`}>
                  <p className="text-xs text-slate-400 mb-2 font-semibold uppercase tracking-wide">Current Contact</p>
                  <p className={`font-bold ${SEV_COLOR[deal.drift_severity]}`}>{deal.current_primary_contact_level}</p>
                  <p className="text-slate-300 text-sm">{deal.current_primary_contact_function}</p>
                </div>
              </div>
              <div className="bg-slate-800 rounded-xl p-4 space-y-3">
                <div className="flex justify-between text-sm">
                  <span className="text-slate-400">Buyer Alignment</span>
                  <span className="font-semibold text-slate-200">{deal.buyer_alignment.replace(/_/g, " ")}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-slate-400">Exec Reengagement Needed</span>
                  <span className={`font-semibold ${deal.needs_exec_reengagement ? "text-red-400" : "text-emerald-400"}`}>
                    {deal.needs_exec_reengagement ? "Yes" : "No"}
                  </span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-slate-400">Drift Status</span>
                  <span className={`font-semibold ${deal.is_drifted ? "text-red-400" : "text-emerald-400"}`}>
                    {deal.is_drifted ? "Drifted" : "On Track"}
                  </span>
                </div>
              </div>
            </div>
          )}

          {tab === "actions" && (
            <div className="space-y-3">
              <div className={`rounded-xl p-4 border ${ACTION_COLOR[deal.drift_action]} bg-opacity-10`}>
                <p className="text-xs font-semibold uppercase tracking-wide mb-1">Recommended Action</p>
                <p className="font-bold text-lg">{deal.drift_action.replace(/_/g, " ").toUpperCase()}</p>
              </div>
              {deal.drift_action === "realign_now" && (
                <ul className="text-sm text-slate-300 space-y-2 list-disc list-inside">
                  <li>Schedule immediate C-suite / exec sponsor meeting within 5 business days</li>
                  <li>Map decision authority back to the original target persona level</li>
                  <li>Engage VP+ champion or escalate to your own executive sponsor</li>
                  <li>Reconfirm budget authority and decision timeline with current contacts</li>
                </ul>
              )}
              {deal.drift_action === "re_engage_exec" && (
                <ul className="text-sm text-slate-300 space-y-2 list-disc list-inside">
                  <li>Reconnect exec sponsor via EBR or QBR within 2 weeks</li>
                  <li>Provide executive-level business case summary</li>
                  <li>Ensure champion has exec air cover before next negotiation step</li>
                </ul>
              )}
              {deal.drift_action === "requalify" && (
                <ul className="text-sm text-slate-300 space-y-2 list-disc list-inside">
                  <li>Requalify deal with updated stakeholder map</li>
                  <li>Confirm whether committee expansion changes decision timeline</li>
                  <li>Validate budget authority with newly added contacts</li>
                </ul>
              )}
              {deal.drift_action === "maintain" && (
                <ul className="text-sm text-slate-300 space-y-2 list-disc list-inside">
                  <li>Buyer persona remains well-aligned — maintain current engagement cadence</li>
                  <li>Continue tracking exec sponsor activity quarterly</li>
                  <li>Monitor for early committee expansion signals</li>
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
export default function BuyerPersonaDriftPage() {
  const [deals, setDeals]     = useState<DriftDeal[]>([]);
  const [summary, setSummary] = useState<Summary | null>(null);
  const [loading, setLoading] = useState(true);
  const [selected, setSelected] = useState<DriftDeal | null>(null);
  const [sevFilter, setSevFilter]     = useState("all");
  const [patternFilter, setPatternFilter] = useState("all");

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const params = new URLSearchParams();
      if (sevFilter !== "all")     params.set("severity", sevFilter);
      if (patternFilter !== "all") params.set("pattern", patternFilter);
      const r = await fetch(`/api/buyer-persona-drift?${params}`);
      const j = await r.json();
      setDeals(j.deals);
      setSummary(j.summary);
    } finally {
      setLoading(false);
    }
  }, [sevFilter, patternFilter]);

  useEffect(() => { load(); }, [load]);

  const severe = deals.filter((d) => d.needs_exec_reengagement);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {/* header */}
      <div>
        <h1 className="text-2xl font-bold text-slate-100">Buyer Persona Drift</h1>
        <p className="text-slate-400 text-sm mt-1">Detect when deals silently drift to the wrong buyer — before it&apos;s too late</p>
      </div>

      {/* exec re-engagement alert */}
      {severe.length > 0 && (
        <div className="bg-red-950 border border-red-700 rounded-xl p-4 flex items-start gap-3">
          <span className="text-red-400 text-xl">⚠</span>
          <div>
            <p className="text-red-300 font-semibold text-sm">{severe.length} deal{severe.length > 1 ? "s" : ""} need immediate exec re-engagement</p>
            <p className="text-red-400/80 text-xs mt-0.5">{severe.map((d) => d.deal_name).join(" · ")}</p>
          </div>
        </div>
      )}

      {/* KPI strip */}
      {summary && (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {[
            { label: "Total Deals",         value: summary.total,                      sub: "" },
            { label: "Drifted",             value: summary.drifted_count,              sub: `${Math.round((summary.drifted_count / summary.total) * 100)}% of deals` },
            { label: "Total Misalign Risk", value: fmt$(summary.total_misalignment_risk), sub: "$ at risk" },
            { label: "Avg Drift Score",     value: summary.avg_persona_drift_composite.toFixed(1), sub: "composite" },
          ].map((k) => (
            <div key={k.label} className="bg-slate-900 border border-slate-800 rounded-xl p-4">
              <p className="text-xs text-slate-400">{k.label}</p>
              <p className="text-2xl font-bold text-slate-100 mt-1">{k.value}</p>
              {k.sub && <p className="text-xs text-slate-500 mt-0.5">{k.sub}</p>}
            </div>
          ))}
        </div>
      )}

      {/* alignment distribution */}
      {summary && (
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
          <h2 className="text-sm font-semibold text-slate-300 mb-4">Buyer Alignment Distribution</h2>
          <AlignmentBar counts={summary.alignment_counts} total={summary.total} />
        </div>
      )}

      {/* filters */}
      <div className="flex flex-wrap gap-2">
        {["all", "aligned", "minor_drift", "moderate_drift", "severe_drift"].map((s) => (
          <button
            key={s}
            onClick={() => setSevFilter(s)}
            className={`px-3 py-1.5 rounded-full text-xs font-medium border transition-colors ${
              sevFilter === s ? "bg-violet-600 border-violet-500 text-white" : "bg-slate-800 border-slate-700 text-slate-300 hover:border-slate-500"
            }`}
          >
            {s === "all" ? "All Severities" : SEV_LABEL[s]}
          </button>
        ))}
        <div className="w-px bg-slate-700 mx-1" />
        {["all", "no_drift", "level_downgrade", "function_shift", "sponsor_loss", "committee_dilution", "multi_drift"].map((p) => (
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

      {/* avg sub-scores */}
      {summary && (
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-3">
          <h2 className="text-sm font-semibold text-slate-300">Average Drift Sub-Scores</h2>
          <ScoreBar label="Level Drift"          score={summary.avg_level_drift_score}        color="#f87171" />
          <ScoreBar label="Function Drift"       score={summary.avg_function_drift_score}     color="#fb923c" />
          <ScoreBar label="Exec Disengagement"   score={summary.avg_exec_disengagement_score} color="#facc15" />
          <div className="flex justify-between text-xs text-slate-400 pt-1">
            <span>Avg Realignment Probability</span>
            <span className="text-emerald-400 font-semibold">{summary.avg_realignment_probability.toFixed(1)}%</span>
          </div>
        </div>
      )}

      {/* deal grid */}
      {loading ? (
        <p className="text-slate-400 text-sm">Loading deals…</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
          {deals.map((d) => (
            <DealCard key={d.deal_id} deal={d} onClick={() => setSelected(d)} />
          ))}
        </div>
      )}

      {selected && <DealModal deal={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
