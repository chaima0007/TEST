"use client";
import { useEffect, useState, useCallback } from "react";

interface Rep {
  rep_id: string;
  region: string;
  intent_risk: string;
  intent_pattern: string;
  intent_severity: string;
  recommended_action: string;
  engagement_decay_score: number;
  champion_health_score: number;
  buying_signal_score: number;
  competitive_threat_score: number;
  buyer_intent_composite: number;
  has_intent_gap: boolean;
  requires_re_engagement: boolean;
  estimated_pipeline_at_risk_usd: number;
  intent_signal: string;
}

interface Summary {
  total: number;
  risk_counts: Record<string, number>;
  pattern_counts: Record<string, number>;
  severity_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_buyer_intent_composite: number;
  intent_gap_count: number;
  re_engagement_count: number;
  avg_engagement_decay_score: number;
  avg_champion_health_score: number;
  avg_buying_signal_score: number;
  avg_competitive_threat_score: number;
  total_estimated_pipeline_at_risk_usd: number;
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
  engaged: "text-emerald-400",
  lukewarm: "text-yellow-400",
  cooling: "text-orange-400",
  ghosted: "text-red-400",
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
            <div className="flex justify-between"><span className="text-slate-400">Engagement Decay</span><span className="text-white">{rep.engagement_decay_score.toFixed(1)}</span></div>
            <div className="flex justify-between"><span className="text-slate-400">Champion Health</span><span className="text-white">{rep.champion_health_score.toFixed(1)}</span></div>
            <div className="flex justify-between"><span className="text-slate-400">Buying Signal</span><span className="text-white">{rep.buying_signal_score.toFixed(1)}</span></div>
            <div className="flex justify-between"><span className="text-slate-400">Competitive Threat</span><span className="text-white">{rep.competitive_threat_score.toFixed(1)}</span></div>
            <div className="flex justify-between border-t border-slate-700 pt-2 mt-2">
              <span className="text-slate-300 font-medium">Intent Composite</span>
              <span className="text-white font-bold">{rep.buyer_intent_composite.toFixed(1)}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-400">Pipeline at Risk</span>
              <span className="text-white">${rep.estimated_pipeline_at_risk_usd.toLocaleString()}</span>
            </div>
          </div>
        )}
        {tab === "signals" && (
          <div className="space-y-3 text-sm">
            <div className="bg-slate-800 rounded p-3">
              <p className="text-slate-400 text-xs mb-1">Signal</p>
              <p className="text-white">{rep.intent_signal}</p>
            </div>
            <div className="grid grid-cols-2 gap-2">
              <div className="bg-slate-800 rounded p-2">
                <p className="text-slate-400 text-xs">Risk</p>
                <p className={`font-semibold ${RISK_COLORS[rep.intent_risk] || "text-white"}`}>{rep.intent_risk}</p>
              </div>
              <div className="bg-slate-800 rounded p-2">
                <p className="text-slate-400 text-xs">Severity</p>
                <p className={`font-semibold ${SEV_COLORS[rep.intent_severity] || "text-white"}`}>{rep.intent_severity}</p>
              </div>
              <div className="bg-slate-800 rounded p-2">
                <p className="text-slate-400 text-xs">Pattern</p>
                <p className="text-white text-xs">{rep.intent_pattern.replace(/_/g, " ")}</p>
              </div>
              <div className="bg-slate-800 rounded p-2">
                <p className="text-slate-400 text-xs">Intent Gap</p>
                <p className={rep.has_intent_gap ? "text-red-400 font-semibold" : "text-emerald-400"}>{rep.has_intent_gap ? "Yes" : "No"}</p>
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
              <p className="text-slate-400 text-xs">Requires Re-Engagement</p>
              <p className={rep.requires_re_engagement ? "text-orange-400 font-semibold" : "text-emerald-400"}>{rep.requires_re_engagement ? "Yes" : "No"}</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function SalesBuyerIntentSignalIntelligenceEnginePage() {
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
    const res = await fetch(`/api/sales-buyer-intent-signal-intelligence-engine?${params}`);
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
            intent_cooling: "bg-yellow-500",
            ghost_prospect: "bg-gray-500",
            competitor_evaluation: "bg-red-500",
            timing_mismatch: "bg-blue-500",
            champion_disengagement: "bg-purple-500",
          },
        },
        {
          title: "Severity Distribution",
          counts: summary.severity_counts,
          colors: { engaged: "bg-emerald-500", lukewarm: "bg-yellow-500", cooling: "bg-orange-500", ghosted: "bg-red-500" },
        },
        {
          title: "Action Distribution",
          counts: summary.action_counts,
          colors: {
            no_action: "bg-emerald-600",
            re_engagement_sequence: "bg-blue-500",
            champion_outreach: "bg-purple-500",
            competitive_displacement: "bg-red-500",
            timing_nurture_sequence: "bg-yellow-500",
            deal_rescue_escalation: "bg-orange-500",
          },
        },
      ]
    : [];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
      {selected && <DetailModal rep={selected} onClose={() => setSelected(null)} />}

      <div className="mb-6">
        <h1 className="text-2xl font-bold text-white">Buyer Intent Signal Intelligence Engine</h1>
        <p className="text-slate-400 text-sm mt-1">Prospect engagement decay, champion health, buying signals, and competitive threat per rep</p>
      </div>

      {/* KPI Strip */}
      {summary && (
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3 mb-6">
          {[
            { label: "Total Reps", value: summary.total },
            { label: "Avg Composite", value: summary.avg_buyer_intent_composite.toFixed(1) },
            { label: "Intent Gaps", value: summary.intent_gap_count },
            { label: "Need Re-Engagement", value: summary.re_engagement_count },
            { label: "Pipeline at Risk", value: `$${(summary.total_estimated_pipeline_at_risk_usd / 1000).toFixed(0)}k` },
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
            <GaugeRing score={summary.avg_engagement_decay_score}   label="Engagement Decay"   color="#ef4444" />
            <GaugeRing score={summary.avg_champion_health_score}     label="Champion Health"    color="#a78bfa" />
            <GaugeRing score={summary.avg_buying_signal_score}       label="Buying Signal"      color="#f59e0b" />
            <GaugeRing score={summary.avg_competitive_threat_score}  label="Competitive Threat" color="#fb923c" />
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
          {["all", "none", "intent_cooling", "ghost_prospect", "competitor_evaluation", "timing_mismatch", "champion_disengagement"].map((p) => (
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
              className={`border rounded-xl p-4 cursor-pointer hover:scale-[1.02] transition-transform ${RISK_BG[rep.intent_risk] || "bg-slate-900 border-slate-700"}`}
            >
              <div className="flex justify-between items-start mb-2">
                <div>
                  <p className="font-bold text-white">{rep.rep_id}</p>
                  <p className="text-xs text-slate-400">{rep.region}</p>
                </div>
                <div className="flex flex-col items-end gap-1">
                  <span className={`text-xs font-semibold ${RISK_COLORS[rep.intent_risk] || "text-white"}`}>
                    {rep.intent_risk.toUpperCase()}
                  </span>
                  {rep.has_intent_gap && (
                    <span className="text-xs bg-red-800 text-red-200 px-1.5 py-0.5 rounded font-semibold">👻 GHOST</span>
                  )}
                </div>
              </div>
              <div className="space-y-1 text-xs">
                <div className="flex justify-between">
                  <span className="text-slate-400">Composite</span>
                  <span className="text-white font-medium">{rep.buyer_intent_composite.toFixed(1)}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-400">Severity</span>
                  <span className={SEV_COLORS[rep.intent_severity] || "text-white"}>{rep.intent_severity}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-400">Pipeline at Risk</span>
                  <span className="text-white">${rep.estimated_pipeline_at_risk_usd.toLocaleString()}</span>
                </div>
              </div>
              <p className="text-xs text-slate-400 mt-2 line-clamp-2">{rep.intent_signal}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
