"use client";
import { useEffect, useState, useCallback } from "react";

interface Rep {
  rep_id: string;
  region: string;
  negotiation_risk: string;
  negotiation_pattern: string;
  negotiation_severity: string;
  recommended_action: string;
  discount_discipline_score: number;
  concession_behavior_score: number;
  value_defense_score: number;
  close_effectiveness_score: number;
  negotiation_composite: number;
  has_pricing_risk: boolean;
  requires_negotiation_coaching: boolean;
  estimated_margin_erosion_usd: number;
  negotiation_signal: string;
}

interface Summary {
  total: number;
  risk_counts: Record<string, number>;
  pattern_counts: Record<string, number>;
  severity_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_negotiation_composite: number;
  pricing_risk_count: number;
  coaching_count: number;
  avg_discount_discipline_score: number;
  avg_concession_behavior_score: number;
  avg_value_defense_score: number;
  avg_close_effectiveness_score: number;
  total_estimated_margin_erosion_usd: number;
}

const RISK_COLORS: Record<string, string> = {
  low: "text-emerald-400",
  moderate: "text-yellow-400",
  high: "text-orange-400",
  critical: "text-red-400",
};
const RISK_BG: Record<string, string> = {
  low: "bg-emerald-900/40 border-emerald-700",
  moderate: "bg-yellow-900/40 border-yellow-700",
  high: "bg-orange-900/40 border-orange-700",
  critical: "bg-red-900/40 border-red-700",
};
const SEV_COLORS: Record<string, string> = {
  strong: "text-emerald-400",
  developing: "text-yellow-400",
  vulnerable: "text-orange-400",
  collapsing: "text-red-400",
};

function GaugeRing({ score, label, color }: { score: number; label: string; color: string }) {
  const r = 30;
  const circ = 2 * Math.PI * r;
  const pct = Math.min(score, 100) / 100;
  return (
    <div className="flex flex-col items-center gap-1">
      <svg width="80" height="80" viewBox="0 0 80 80">
        <circle cx="40" cy="40" r={r} fill="none" stroke="#1e293b" strokeWidth="8" />
        <circle
          cx="40" cy="40" r={r} fill="none"
          stroke={color} strokeWidth="8"
          strokeDasharray={`${pct * circ} ${circ}`}
          strokeLinecap="round"
          transform="rotate(-90 40 40)"
        />
        <text x="40" y="45" textAnchor="middle" fill="white" fontSize="13" fontWeight="bold">
          {score.toFixed(0)}
        </text>
      </svg>
      <span className="text-xs text-slate-400 text-center leading-tight">{label}</span>
    </div>
  );
}

function DistBar({ title, counts, colors }: { title: string; counts: Record<string, number>; colors: Record<string, string> }) {
  const total = Object.values(counts).reduce((a, b) => a + b, 0) || 1;
  return (
    <div>
      <p className="text-xs text-slate-400 mb-1">{title}</p>
      <div className="flex rounded overflow-hidden h-3">
        {Object.entries(counts).map(([k, v]) => (
          <div
            key={k}
            style={{ width: `${(v / total) * 100}%` }}
            className={`${colors[k] || "bg-slate-600"} transition-all`}
            title={`${k}: ${v}`}
          />
        ))}
      </div>
      <div className="flex flex-wrap gap-x-3 mt-1">
        {Object.entries(counts).map(([k, v]) => (
          <span key={k} className="text-xs text-slate-400">
            <span className={`inline-block w-2 h-2 rounded-full mr-1 ${colors[k] || "bg-slate-600"}`} />
            {k}: {v}
          </span>
        ))}
      </div>
    </div>
  );
}

function DetailModal({ rep, onClose }: { rep: Rep; onClose: () => void }) {
  const [tab, setTab] = useState<"scores" | "signals" | "action">("scores");
  useEffect(() => {
    const handler = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [onClose]);
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70" onClick={onClose}>
      <div className="bg-slate-900 border border-slate-700 rounded-xl p-6 w-full max-w-lg shadow-2xl" onClick={(e) => e.stopPropagation()}>
        <div className="flex items-center justify-between mb-4">
          <div>
            <h3 className="text-lg font-bold text-white">{rep.rep_id}</h3>
            <p className="text-sm text-slate-400">{rep.region}</p>
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-white text-xl">✕</button>
        </div>
        <div className="flex gap-2 mb-4">
          {(["scores", "signals", "action"] as const).map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`px-3 py-1 rounded text-xs font-medium ${tab === t ? "bg-blue-600 text-white" : "bg-slate-800 text-slate-400 hover:text-white"}`}
            >
              {t.charAt(0).toUpperCase() + t.slice(1)}
            </button>
          ))}
        </div>
        {tab === "scores" && (
          <div className="space-y-2 text-sm">
            <div className="flex justify-between"><span className="text-slate-400">Discount Discipline</span><span className="text-white">{rep.discount_discipline_score.toFixed(1)}</span></div>
            <div className="flex justify-between"><span className="text-slate-400">Concession Behavior</span><span className="text-white">{rep.concession_behavior_score.toFixed(1)}</span></div>
            <div className="flex justify-between"><span className="text-slate-400">Value Defense</span><span className="text-white">{rep.value_defense_score.toFixed(1)}</span></div>
            <div className="flex justify-between"><span className="text-slate-400">Close Effectiveness</span><span className="text-white">{rep.close_effectiveness_score.toFixed(1)}</span></div>
            <div className="flex justify-between border-t border-slate-700 pt-2 mt-2">
              <span className="text-slate-300 font-medium">Negotiation Composite</span>
              <span className="text-white font-bold">{rep.negotiation_composite.toFixed(1)}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-400">Margin Erosion Est.</span>
              <span className="text-white">${rep.estimated_margin_erosion_usd.toLocaleString()}</span>
            </div>
          </div>
        )}
        {tab === "signals" && (
          <div className="space-y-3 text-sm">
            <div className="bg-slate-800 rounded p-3">
              <p className="text-slate-400 text-xs mb-1">Signal</p>
              <p className="text-white">{rep.negotiation_signal}</p>
            </div>
            <div className="grid grid-cols-2 gap-2">
              <div className="bg-slate-800 rounded p-2">
                <p className="text-slate-400 text-xs">Risk</p>
                <p className={`font-semibold ${RISK_COLORS[rep.negotiation_risk] || "text-white"}`}>{rep.negotiation_risk}</p>
              </div>
              <div className="bg-slate-800 rounded p-2">
                <p className="text-slate-400 text-xs">Severity</p>
                <p className={`font-semibold ${SEV_COLORS[rep.negotiation_severity] || "text-white"}`}>{rep.negotiation_severity}</p>
              </div>
              <div className="bg-slate-800 rounded p-2">
                <p className="text-slate-400 text-xs">Pattern</p>
                <p className="text-white text-xs">{rep.negotiation_pattern.replace(/_/g, " ")}</p>
              </div>
              <div className="bg-slate-800 rounded p-2">
                <p className="text-slate-400 text-xs">Pricing Risk</p>
                <p className={rep.has_pricing_risk ? "text-red-400 font-semibold" : "text-emerald-400"}>{rep.has_pricing_risk ? "Yes" : "No"}</p>
              </div>
            </div>
          </div>
        )}
        {tab === "action" && (
          <div className="space-y-3 text-sm">
            <div className="bg-blue-900/30 border border-blue-700 rounded p-3">
              <p className="text-blue-300 text-xs mb-1">Recommended Action</p>
              <p className="text-white font-semibold">{rep.recommended_action.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase())}</p>
            </div>
            <div className="bg-slate-800 rounded p-2">
              <p className="text-slate-400 text-xs">Requires Negotiation Coaching</p>
              <p className={rep.requires_negotiation_coaching ? "text-orange-400 font-semibold" : "text-emerald-400"}>{rep.requires_negotiation_coaching ? "Yes" : "No"}</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function SalesNegotiationEffectivenessIntelligenceEnginePage() {
  const [reps, setReps]         = useState<Rep[]>([]);
  const [summary, setSummary]   = useState<Summary | null>(null);
  const [loading, setLoading]   = useState(true);
  const [riskFilter, setRisk]   = useState("all");
  const [patFilter, setPat]     = useState("all");
  const [selected, setSelected] = useState<Rep | null>(null);

  const load = useCallback(async () => {
    setLoading(true);
    const params = new URLSearchParams();
    if (riskFilter !== "all") params.set("risk", riskFilter);
    if (patFilter  !== "all") params.set("pattern", patFilter);
    const res = await fetch(`/api/sales-negotiation-effectiveness-intelligence-engine?${params}`);
    const data = await res.json();
    setReps(data.reps);
    setSummary(data.summary);
    setLoading(false);
  }, [riskFilter, patFilter]);

  useEffect(() => { load(); }, [load]);

  const distributions: Array<{ title: string; counts: Record<string, number>; colors: Record<string, string> }> = summary
    ? [
        {
          title: "Risk Distribution",
          counts: summary.risk_counts,
          colors: { low: "bg-emerald-500", moderate: "bg-yellow-500", high: "bg-orange-500", critical: "bg-red-500" },
        },
        {
          title: "Pattern Distribution",
          counts: summary.pattern_counts,
          colors: {
            none: "bg-emerald-600",
            excessive_discounting: "bg-red-500",
            premature_concession: "bg-orange-500",
            price_erosion: "bg-yellow-500",
            value_abandonment: "bg-purple-500",
            negotiation_avoidance: "bg-blue-500",
          },
        },
        {
          title: "Severity Distribution",
          counts: summary.severity_counts,
          colors: { strong: "bg-emerald-500", developing: "bg-yellow-500", vulnerable: "bg-orange-500", collapsing: "bg-red-500" },
        },
        {
          title: "Action Distribution",
          counts: summary.action_counts,
          colors: {
            no_action: "bg-emerald-600",
            negotiation_coaching: "bg-blue-500",
            discount_authority_review: "bg-yellow-500",
            value_selling_training: "bg-purple-500",
            pricing_integrity_program: "bg-orange-500",
            deal_desk_escalation: "bg-red-500",
          },
        },
      ]
    : [];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
      {selected && <DetailModal rep={selected} onClose={() => setSelected(null)} />}

      <div className="mb-6">
        <h1 className="text-2xl font-bold text-white">Negotiation Effectiveness Intelligence Engine</h1>
        <p className="text-slate-400 text-sm mt-1">Discount discipline, concession behavior, value defense, and pricing integrity per rep</p>
      </div>

      {/* KPI Strip */}
      {summary && (
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3 mb-6">
          {[
            { label: "Total Reps", value: summary.total },
            { label: "Avg Composite", value: summary.avg_negotiation_composite.toFixed(1) },
            { label: "Pricing Risks", value: summary.pricing_risk_count },
            { label: "Need Coaching", value: summary.coaching_count },
            { label: "Margin Erosion", value: `$${(summary.total_estimated_margin_erosion_usd / 1000).toFixed(0)}k` },
            { label: "Critical Reps", value: summary.risk_counts["critical"] ?? 0 },
          ].map(({ label, value }) => (
            <div key={label} className="bg-slate-900 border border-slate-800 rounded-lg p-3 text-center">
              <p className="text-xs text-slate-400">{label}</p>
              <p className="text-xl font-bold text-white mt-1">{value}</p>
            </div>
          ))}
        </div>
      )}

      {/* Gauges */}
      {summary && (
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 mb-6">
          <p className="text-sm text-slate-400 mb-4">Avg Sub-Scores (0–100, higher = more risk)</p>
          <div className="flex flex-wrap justify-around gap-4">
            <GaugeRing score={summary.avg_discount_discipline_score}   label="Discount Discipline"  color="#ef4444" />
            <GaugeRing score={summary.avg_concession_behavior_score}   label="Concession Behavior"  color="#f59e0b" />
            <GaugeRing score={summary.avg_value_defense_score}         label="Value Defense"         color="#a78bfa" />
            <GaugeRing score={summary.avg_close_effectiveness_score}   label="Close Effectiveness"  color="#fb923c" />
          </div>
        </div>
      )}

      {/* Distribution Bars */}
      {summary && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
          {distributions.map((d) => (
            <div key={d.title} className="bg-slate-900 border border-slate-800 rounded-xl p-4">
              <DistBar title={d.title} counts={d.counts} colors={d.colors} />
            </div>
          ))}
        </div>
      )}

      {/* Filters */}
      <div className="flex flex-wrap gap-3 mb-4">
        <div className="flex gap-1 flex-wrap">
          {["all", "low", "moderate", "high", "critical"].map((r) => (
            <button
              key={r}
              onClick={() => setRisk(r)}
              className={`px-3 py-1 rounded text-xs font-medium ${riskFilter === r ? "bg-blue-600 text-white" : "bg-slate-800 text-slate-400 hover:text-white"}`}
            >
              {r}
            </button>
          ))}
        </div>
        <div className="flex gap-1 flex-wrap">
          {["all", "none", "excessive_discounting", "premature_concession", "price_erosion", "value_abandonment", "negotiation_avoidance"].map((p) => (
            <button
              key={p}
              onClick={() => setPat(p)}
              className={`px-3 py-1 rounded text-xs font-medium ${patFilter === p ? "bg-purple-600 text-white" : "bg-slate-800 text-slate-400 hover:text-white"}`}
            >
              {p.replace(/_/g, " ")}
            </button>
          ))}
        </div>
      </div>

      {/* Rep Cards */}
      {loading ? (
        <div className="text-center text-slate-400 py-12">Loading...</div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          {reps.map((rep) => (
            <div
              key={rep.rep_id}
              onClick={() => setSelected(rep)}
              className={`border rounded-xl p-4 cursor-pointer hover:scale-[1.02] transition-transform ${RISK_BG[rep.negotiation_risk] || "bg-slate-900 border-slate-700"}`}
            >
              <div className="flex justify-between items-start mb-2">
                <div>
                  <p className="font-bold text-white">{rep.rep_id}</p>
                  <p className="text-xs text-slate-400">{rep.region}</p>
                </div>
                <div className="flex flex-col items-end gap-1">
                  <span className={`text-xs font-semibold ${RISK_COLORS[rep.negotiation_risk] || "text-white"}`}>
                    {rep.negotiation_risk.toUpperCase()}
                  </span>
                  {rep.has_pricing_risk && (
                    <span className="text-xs bg-orange-800 text-orange-200 px-1.5 py-0.5 rounded font-semibold">💸 PRICE</span>
                  )}
                </div>
              </div>
              <div className="space-y-1 text-xs">
                <div className="flex justify-between">
                  <span className="text-slate-400">Composite</span>
                  <span className="text-white font-medium">{rep.negotiation_composite.toFixed(1)}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-400">Severity</span>
                  <span className={SEV_COLORS[rep.negotiation_severity] || "text-white"}>{rep.negotiation_severity}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-400">Margin Erosion</span>
                  <span className="text-white">${rep.estimated_margin_erosion_usd.toLocaleString()}</span>
                </div>
              </div>
              <p className="text-xs text-slate-400 mt-2 line-clamp-2">{rep.negotiation_signal}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
