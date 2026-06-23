"use client";

import { useEffect, useState } from "react";

// ── types ────────────────────────────────────────────────────────────────────
interface InnovationSignal {
  signal_id: string;
  domain: string;
  region: string;
  innovation_risk: string;
  innovation_pattern: string;
  innovation_severity: string;
  recommended_action: string;
  opportunity_score: number;
  market_score: number;
  capability_score: number;
  timing_score: number;
  innovation_composite: number;
  has_opportunity_signal: boolean;
  requires_executive_attention: boolean;
  estimated_opportunity_value_index: number;
  innovation_signal: string;
}

interface Summary {
  total: number;
  risk_counts: Record<string, number>;
  pattern_counts: Record<string, number>;
  severity_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_innovation_composite: number;
  opportunity_signal_count: number;
  executive_attention_count: number;
  avg_opportunity_score: number;
  avg_market_score: number;
  avg_capability_score: number;
  avg_timing_score: number;
  avg_estimated_opportunity_value_index: number;
}

// ── helpers ──────────────────────────────────────────────────────────────────
const RISK_COLOR: Record<string, string> = {
  critical: "text-rose-400",
  high:     "text-amber-400",
  moderate: "text-cyan-400",
  low:      "text-teal-400",
};

const RISK_BG: Record<string, string> = {
  critical: "bg-rose-500/20 border-rose-500/40",
  high:     "bg-amber-500/20 border-amber-500/40",
  moderate: "bg-cyan-500/20 border-cyan-500/40",
  low:      "bg-teal-500/20 border-teal-500/40",
};

const SEVERITY_COLOR: Record<string, string> = {
  critical_gap: "text-rose-400",
  lagging:      "text-amber-400",
  monitoring:   "text-cyan-400",
  ahead:        "text-teal-400",
};

const PATTERN_ICON: Record<string, string> = {
  emerging_technology:    "🔬",
  competitive_disruption: "⚔️",
  market_whitespace:      "🗺️",
  talent_shift:           "👥",
  regulatory_opportunity: "📋",
  none:                   "—",
};

function CompositeRing({ score, color }: { score: number; color: string }) {
  const r = 36, circ = 2 * Math.PI * r;
  const fill = (Math.min(score, 100) / 100) * circ;
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

function RiskDistBar({ counts }: { counts: Record<string, number> }) {
  const order  = ["critical", "high", "moderate", "low"];
  const colors = ["bg-rose-500", "bg-amber-500", "bg-cyan-500", "bg-teal-500"];
  const total  = Object.values(counts).reduce((a, b) => a + b, 0) || 1;
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

// ── SignalModal ───────────────────────────────────────────────────────────────
function SignalModal({ signal, onClose }: { signal: InnovationSignal; onClose: () => void }) {
  const [tab, setTab] = useState<"overview" | "scores" | "action">("overview");

  useEffect(() => {
    const esc = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", esc);
    return () => window.removeEventListener("keydown", esc);
  }, [onClose]);

  const ringColor =
    signal.innovation_composite >= 60 ? "#f43f5e"
    : signal.innovation_composite >= 40 ? "#f59e0b"
    : signal.innovation_composite >= 20 ? "#22d3ee"
    : "#2dd4bf";

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
          <CompositeRing score={signal.innovation_composite} color={ringColor} />
          <div className="flex-1 min-w-0">
            <h2 className="text-white font-bold text-lg truncate">{signal.domain}</h2>
            <p className="text-slate-400 text-sm">{signal.signal_id} · {signal.region}</p>
            <div className="flex gap-2 mt-1 flex-wrap">
              <span className={`text-xs px-2 py-0.5 rounded-full border ${RISK_BG[signal.innovation_risk]}`}>
                {signal.innovation_risk} risk
              </span>
              <span className={`text-xs font-medium ${SEVERITY_COLOR[signal.innovation_severity]}`}>
                {signal.innovation_severity.replace(/_/g, " ")}
              </span>
            </div>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl">✕</button>
        </div>

        {/* tabs */}
        <div className="flex border-b border-slate-800">
          {(["overview", "scores", "action"] as const).map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`flex-1 py-2.5 text-sm font-medium capitalize transition-colors ${
                tab === t ? "text-teal-400 border-b-2 border-teal-400" : "text-slate-500 hover:text-slate-300"
              }`}
            >
              {t}
            </button>
          ))}
        </div>

        <div className="p-5 space-y-3">
          {tab === "overview" && (
            <>
              <div className="grid grid-cols-2 gap-3">
                {[
                  ["Pattern",         PATTERN_ICON[signal.innovation_pattern] + " " + signal.innovation_pattern.replace(/_/g, " ")],
                  ["Opp Value Index",  signal.estimated_opportunity_value_index.toFixed(2) + " / 10"],
                  ["Opp Signal",      signal.has_opportunity_signal ? "✅ Yes" : "No"],
                  ["Exec Attention",  signal.requires_executive_attention ? "⚡ Yes" : "No"],
                ].map(([label, value]) => (
                  <div key={label as string} className="bg-slate-800/60 rounded-lg p-3">
                    <div className="text-xs text-slate-400">{label}</div>
                    <div className="text-white font-semibold mt-0.5 text-sm">{value}</div>
                  </div>
                ))}
              </div>
              <div className="bg-slate-800/60 rounded-lg p-3">
                <div className="text-xs text-slate-400 mb-1">Innovation Signal</div>
                <div className="text-teal-300 text-sm leading-relaxed">{signal.innovation_signal}</div>
              </div>
            </>
          )}

          {tab === "scores" && (
            <div className="space-y-3">
              <ScoreBar label="Opportunity"  value={signal.opportunity_score}  color="bg-teal-500" />
              <ScoreBar label="Market"       value={signal.market_score}        color="bg-cyan-500" />
              <ScoreBar label="Capability"   value={signal.capability_score}    color="bg-sky-500" />
              <ScoreBar label="Timing"       value={signal.timing_score}        color="bg-indigo-500" />
            </div>
          )}

          {tab === "action" && (
            <div className="space-y-3">
              <div className="bg-teal-500/10 border border-teal-500/30 rounded-xl p-4">
                <div className="text-xs text-teal-400 uppercase tracking-wide mb-1">Recommended Action</div>
                <div className="text-white font-bold text-lg capitalize">
                  {signal.recommended_action.replace(/_/g, " ")}
                </div>
              </div>
              {signal.requires_executive_attention && (
                <div className="bg-amber-500/10 border border-amber-500/30 rounded-xl p-3 text-sm text-amber-300">
                  ⚡ Executive attention required — brief leadership on opportunity window
                </div>
              )}
              {signal.has_opportunity_signal && (
                <div className="bg-cyan-500/10 border border-cyan-500/30 rounded-xl p-3 text-sm text-cyan-300">
                  🎯 Active opportunity signal — prioritise assessment this quarter
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

// ── SignalCard ────────────────────────────────────────────────────────────────
function SignalCard({ signal, onClick }: { signal: InnovationSignal; onClick: () => void }) {
  const ringColor =
    signal.innovation_composite >= 60 ? "#f43f5e"
    : signal.innovation_composite >= 40 ? "#f59e0b"
    : signal.innovation_composite >= 20 ? "#22d3ee"
    : "#2dd4bf";

  return (
    <div
      onClick={onClick}
      className="bg-slate-900 border border-slate-800 rounded-xl p-4 cursor-pointer hover:border-teal-500/50 hover:bg-slate-800/60 transition-all"
    >
      <div className="flex items-center gap-3">
        <CompositeRing score={signal.innovation_composite} color={ringColor} />
        <div className="flex-1 min-w-0">
          <div className="text-white font-semibold truncate">{signal.domain}</div>
          <div className="text-slate-400 text-xs">{signal.signal_id} · {signal.region}</div>
          <div className="flex gap-2 mt-1 flex-wrap">
            <span className={`text-xs px-2 py-0.5 rounded-full border ${RISK_BG[signal.innovation_risk]}`}>
              {signal.innovation_risk}
            </span>
          </div>
        </div>
        <div className="text-right shrink-0">
          {signal.requires_executive_attention && <div className="text-xs text-amber-400">⚡ Exec</div>}
          <div className={`text-sm font-bold mt-1 ${SEVERITY_COLOR[signal.innovation_severity]}`}>
            {signal.innovation_severity.replace(/_/g, " ")}
          </div>
          {signal.has_opportunity_signal && (
            <div className="text-xs text-teal-400 mt-1">🎯</div>
          )}
        </div>
      </div>
      <div className="mt-2 text-xs text-slate-400">
        {PATTERN_ICON[signal.innovation_pattern]} {signal.innovation_pattern.replace(/_/g, " ")} · val: {signal.estimated_opportunity_value_index.toFixed(2)}
      </div>
    </div>
  );
}

// ── page ─────────────────────────────────────────────────────────────────────
export default function InnovationScoutEnginePage() {
  const [signals, setSignals]   = useState<InnovationSignal[]>([]);
  const [summary, setSummary]   = useState<Summary | null>(null);
  const [loading, setLoading]   = useState(true);
  const [selected, setSelected] = useState<InnovationSignal | null>(null);
  const [filterRisk,   setFilterRisk]   = useState("all");
  const [filterRegion, setFilterRegion] = useState("all");

  useEffect(() => {
    async function load() {
        setLoading(true);
        const params = new URLSearchParams();
        if (filterRisk   !== "all") params.set("risk",   filterRisk);
        if (filterRegion !== "all") params.set("region", filterRegion);
        const res  = await fetch(`/api/innovation-scout-engine?${params}`);
        const data = await res.json();
        setSignals(data.signals);
        setSummary(data.summary);
        setLoading(false);
  }
    load();
  }, [filterRisk, filterRegion]);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
      <div className="max-w-6xl mx-auto space-y-6">

        {/* header */}
        <div>
          <h1 className="text-2xl font-bold text-white">Innovation Scout Engine</h1>
          <p className="text-slate-400 text-sm mt-1">
            Detects missed-opportunity risk across domains — technology lags, competitive disruption,
            market whitespace, talent shifts and regulatory tailwinds
          </p>
        </div>

        {/* KPI strip */}
        {summary && (
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
            {[
              { label: "Signals Tracked",     value: summary.total },
              { label: "Avg Composite",        value: summary.avg_innovation_composite.toFixed(1), color: "text-teal-400" },
              { label: "Opp Signals",          value: summary.opportunity_signal_count,             color: "text-cyan-400" },
              { label: "Exec Attention",       value: summary.executive_attention_count,            color: "text-amber-400" },
            ].map(({ label, value, color }) => (
              <div key={label} className="bg-slate-900 border border-slate-800 rounded-xl p-4">
                <div className="text-xs text-slate-400">{label}</div>
                <div className={`text-2xl font-bold mt-1 ${color ?? "text-white"}`}>{value}</div>
              </div>
            ))}
          </div>
        )}

        {/* risk distribution bar */}
        {summary && (
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-400 mb-2">Risk Distribution (missed-opportunity)</div>
            <RiskDistBar counts={summary.risk_counts} />
            <div className="flex gap-4 mt-2 text-xs text-slate-500">
              {["critical", "high", "moderate", "low"].map((k) => (
                <span key={k} className={RISK_COLOR[k]}>{k}: {summary.risk_counts[k] || 0}</span>
              ))}
            </div>
          </div>
        )}

        {/* filters */}
        <div className="flex flex-wrap gap-2">
          {[
            { label: "All Risks",  val: "all" },
            { label: "🔴 Critical", val: "critical" },
            { label: "🟠 High",    val: "high" },
            { label: "🔵 Moderate", val: "moderate" },
            { label: "🟢 Low",     val: "low" },
          ].map(({ label, val }) => (
            <button
              key={val}
              onClick={() => setFilterRisk(val)}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
                filterRisk === val
                  ? "bg-teal-600 text-white"
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
            {["NAMER", "EMEA", "APAC", "LATAM"].map((r) => (
              <option key={r} value={r}>{r}</option>
            ))}
          </select>
        </div>

        {/* signals grid */}
        {loading ? (
          <div className="text-slate-400 text-center py-16">Scanning innovation landscape…</div>
        ) : signals.length === 0 ? (
          <div className="text-slate-500 text-center py-16">No signals match your filters.</div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {signals.map((s) => (
              <SignalCard key={s.signal_id} signal={s} onClick={() => setSelected(s)} />
            ))}
          </div>
        )}

        {/* avg score bars */}
        {summary && (
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
            <div className="text-sm font-semibold text-slate-300 mb-4">Average Score Breakdown</div>
            <div className="space-y-3">
              <ScoreBar label="Opportunity"  value={summary.avg_opportunity_score}  color="bg-teal-500" />
              <ScoreBar label="Market"       value={summary.avg_market_score}        color="bg-cyan-500" />
              <ScoreBar label="Capability"   value={summary.avg_capability_score}    color="bg-sky-500" />
              <ScoreBar label="Timing"       value={summary.avg_timing_score}        color="bg-indigo-500" />
            </div>
          </div>
        )}
      </div>

      {selected && <SignalModal signal={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
