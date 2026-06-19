"use client";
import { useEffect, useState } from "react";

type UXInterface = {
  interface_id: string;
  ux_domain: string;
  region: string;
  cognitive_score: number;
  engagement_score: number;
  adaptation_score: number;
  accessibility_score: number;
  ux_composite: number;
  ux_risk: string;
  ux_pattern: string;
  ux_severity: string;
  recommended_action: string;
  has_load_signal: boolean;
  requires_intervention: boolean;
  estimated_cognitive_friction_index: number;
  ux_signal: string;
};

type Summary = {
  total: number;
  risk_counts: Record<string, number>;
  pattern_counts: Record<string, number>;
  severity_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_ux_composite: number;
  load_signal_count: number;
  intervention_required_count: number;
  avg_cognitive_score: number;
  avg_engagement_score: number;
  avg_adaptation_score: number;
  avg_accessibility_score: number;
  avg_estimated_cognitive_friction_index: number;
};

function GaugeRing({ value, label, color }: { value: number; label: string; color: string }) {
  const r = 36;
  const circ = 2 * Math.PI * r;
  const fill = circ * (1 - value / 100);
  return (
    <div className="flex flex-col items-center gap-1">
      <svg width="88" height="88" viewBox="0 0 88 88">
        <circle cx="44" cy="44" r={r} fill="none" stroke="#1e293b" strokeWidth="8" />
        <circle
          cx="44" cy="44" r={r} fill="none" stroke={color} strokeWidth="8"
          strokeDasharray={circ} strokeDashoffset={fill}
          strokeLinecap="round" transform="rotate(-90 44 44)"
        />
        <text x="44" y="49" textAnchor="middle" fill="white" fontSize="13" fontWeight="bold">
          {Math.round(value)}
        </text>
      </svg>
      <span className="text-xs text-slate-400 text-center">{label}</span>
    </div>
  );
}

function DistBar({ title, counts, colors }: { title: string; counts: Record<string, number>; colors: Record<string, string> }) {
  const total = Object.values(counts).reduce((a, b) => a + b, 0) || 1;
  return (
    <div className="flex flex-col gap-1">
      <span className="text-xs text-slate-400 font-medium">{title}</span>
      <div className="flex h-3 rounded overflow-hidden gap-px">
        {Object.entries(counts).map(([k, v]) => (
          <div key={k} style={{ width: `${(v / total) * 100}%`, background: colors[k] || "#475569" }} title={`${k}: ${v}`} />
        ))}
      </div>
      <div className="flex flex-wrap gap-x-3 gap-y-0.5">
        {Object.entries(counts).map(([k, v]) => (
          <span key={k} className="text-xs text-slate-400">
            <span style={{ color: colors[k] || "#94a3b8" }}>■</span> {k} {v}
          </span>
        ))}
      </div>
    </div>
  );
}

const RISK_COLORS = { low: "#10b981", moderate: "#f59e0b", high: "#f97316", critical: "#ef4444" };
const PAT_COLORS = {
  none: "#10b981",
  cognitive_overload: "#ef4444",
  attention_fragmentation: "#f97316",
  adaptation_failure: "#dc2626",
  engagement_collapse: "#a855f7",
  accessibility_gap: "#7c3aed",
};
const SEV_COLORS = { neuroptimal: "#10b981", optimizing: "#f59e0b", strained: "#f97316", critical_load: "#ef4444" };
const ACT_COLORS = {
  no_action: "#10b981",
  ux_monitoring: "#06b6d4",
  adaptation_sprint: "#3b82f6",
  accessibility_audit: "#a855f7",
  ux_redesign: "#ef4444",
  load_shedding: "#7f1d1d",
};
const RISK_BADGE: Record<string, string> = {
  low: "bg-emerald-900 text-emerald-300",
  moderate: "bg-amber-900 text-amber-300",
  high: "bg-orange-900 text-orange-300",
  critical: "bg-red-900 text-red-300",
};
const SEV_BADGE: Record<string, string> = {
  neuroptimal: "bg-emerald-900 text-emerald-300",
  optimizing: "bg-lime-900 text-lime-300",
  strained: "bg-orange-900 text-orange-300",
  critical_load: "bg-red-900 text-red-300",
};

function DetailModal({ iface, onClose }: { iface: UXInterface; onClose: () => void }) {
  const [tab, setTab] = useState<"scores" | "signal" | "action">("scores");
  useEffect(() => {
    const h = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", h);
    return () => window.removeEventListener("keydown", h);
  }, [onClose]);
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70" onClick={onClose}>
      <div
        className="bg-slate-900 border border-lime-500/30 rounded-xl w-full max-w-lg p-6 shadow-2xl"
        onClick={e => e.stopPropagation()}
      >
        <div className="flex items-center justify-between mb-4">
          <div>
            <span className="text-lg font-bold text-white">{iface.interface_id}</span>
            <span className="ml-2 text-emerald-400 text-xs">{iface.ux_domain.replace(/_/g, " ")}</span>
            <span className="ml-2 text-lime-400 text-xs">{iface.region}</span>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl leading-none">✕</button>
        </div>
        <div className="flex gap-2 mb-4">
          {(["scores", "signal", "action"] as const).map(t => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`px-3 py-1 rounded text-xs font-medium transition-colors ${tab === t ? "bg-emerald-700 text-white" : "bg-slate-800 text-slate-400 hover:text-white"}`}
            >
              {t.charAt(0).toUpperCase() + t.slice(1)}
            </button>
          ))}
        </div>
        {tab === "scores" && (
          <div className="grid grid-cols-2 gap-3 text-sm">
            {([
              ["Cognition", iface.cognitive_score, "#ef4444"],
              ["Engagement", iface.engagement_score, "#10b981"],
              ["Adaptation", iface.adaptation_score, "#06b6d4"],
              ["Accessibilité", iface.accessibility_score, "#a855f7"],
            ] as [string, number, string][]).map(([l, v, c]) => (
              <div key={l} className="bg-slate-800 rounded-lg p-3">
                <div className="text-slate-400 text-xs mb-1">{l}</div>
                <div className="text-white font-bold text-lg">{Number(v).toFixed(1)}</div>
                <div className="h-1.5 rounded mt-1 bg-slate-700">
                  <div className="h-1.5 rounded" style={{ width: `${Math.min(Number(v), 100)}%`, background: c }} />
                </div>
              </div>
            ))}
            <div className="col-span-2 bg-slate-800 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Composite UX</div>
              <div className="text-white font-bold text-2xl">{iface.ux_composite.toFixed(1)}</div>
            </div>
          </div>
        )}
        {tab === "signal" && (
          <div className="bg-slate-800 rounded-lg p-4 text-sm text-slate-200 leading-relaxed">
            {iface.ux_signal}
            <div className="mt-3 flex gap-2 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[iface.ux_risk] || "bg-slate-700 text-slate-300"}`}>{iface.ux_risk}</span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[iface.ux_severity] || "bg-slate-700 text-slate-300"}`}>{iface.ux_severity}</span>
            </div>
          </div>
        )}
        {tab === "action" && (
          <div className="space-y-3 text-sm">
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Action Recommandée</div>
              <div className="text-white font-medium">{iface.recommended_action.replace(/_/g, " ")}</div>
            </div>
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Friction Cognitive Estimée</div>
              <div className="text-white font-bold">{iface.estimated_cognitive_friction_index.toFixed(2)} / 10</div>
            </div>
            <div className="bg-slate-800 rounded-lg p-3 flex gap-4">
              <div>
                <div className="text-slate-400 text-xs mb-1">Signal Charge</div>
                <div className={`text-xs font-semibold ${iface.has_load_signal ? "text-red-400" : "text-emerald-400"}`}>
                  {iface.has_load_signal ? "Oui" : "Non"}
                </div>
              </div>
              <div>
                <div className="text-slate-400 text-xs mb-1">Intervention Req.</div>
                <div className={`text-xs font-semibold ${iface.requires_intervention ? "text-orange-400" : "text-emerald-400"}`}>
                  {iface.requires_intervention ? "Oui" : "Non"}
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function NeuroadaptiveUXDashboard() {
  const [data, setData] = useState<{ interfaces: UXInterface[]; summary: Summary } | null>(null);
  const [filter, setFilter] = useState<string>("all");
  const [patFilter, setPatFilter] = useState<string>("all");
  const [selected, setSelected] = useState<UXInterface | null>(null);

  useEffect(() => {
    fetch("/api/neuroadaptive-ux-engine")
      .then(r => r.json())
      .then(setData)
      .catch(console.error);
  }, []);

  if (!data) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-emerald-400 text-lg animate-pulse">Loading Neuroadaptive UX Engine...</div>
    </div>
  );

  const { interfaces, summary } = data;
  const filtered = interfaces.filter(g =>
    (filter === "all" || g.ux_risk === filter) &&
    (patFilter === "all" || g.ux_pattern === patFilter)
  );

  const dists: Array<{ title: string; counts: Record<string, number>; colors: Record<string, string> }> = [
    { title: "Risque UX",            counts: summary.risk_counts,     colors: RISK_COLORS },
    { title: "Pattern Neuroadaptif", counts: summary.pattern_counts,  colors: PAT_COLORS  },
    { title: "Sévérité Charge",      counts: summary.severity_counts, colors: SEV_COLORS  },
    { title: "Action Recommandée",   counts: summary.action_counts,   colors: ACT_COLORS  },
  ];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {selected && <DetailModal iface={selected} onClose={() => setSelected(null)} />}

      <div>
        <h1 className="text-2xl font-bold text-white">Neuroadaptive UX &amp; Cognitive Load Optimization Engine</h1>
        <p className="text-slate-400 text-sm mt-1">Charge cognitive · Adaptation · Engagement · Accessibilité — optimisation neuroadaptive des interfaces</p>
      </div>

      {/* KPI strip — 6 cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {([
          ["Total Interfaces",    summary.total,                                        "text-emerald-400"],
          ["Signaux Charge",      summary.load_signal_count,                            "text-red-400"],
          ["Interventions Req.",  summary.intervention_required_count,                  "text-orange-400"],
          ["Composite Moyen",     summary.avg_ux_composite,                             "text-lime-400"],
          ["Friction Cognitive",  summary.avg_estimated_cognitive_friction_index,       "text-emerald-400"],
          ["Score Adaptation",    `${Math.round(summary.avg_adaptation_score)}`,        "text-teal-400"],
        ] as [string, string | number, string][]).map(([l, v, c]) => (
          <div key={String(l)} className="bg-slate-900 border border-lime-500/30 rounded-xl p-3 text-center">
            <div className={`text-xl font-bold ${c}`}>{v}</div>
            <div className="text-xs text-slate-500 mt-0.5">{l}</div>
          </div>
        ))}
      </div>

      {/* 4 SVG GaugeRings */}
      <div className="bg-slate-900 border border-lime-500/30 rounded-xl p-5">
        <div className="grid grid-cols-4 gap-4">
          <GaugeRing value={summary.avg_cognitive_score}     label="Score Cognition"   color="#ef4444" />
          <GaugeRing value={summary.avg_engagement_score}    label="Engagement"         color="#10b981" />
          <GaugeRing value={summary.avg_adaptation_score}    label="Adaptation Neuro"   color="#06b6d4" />
          <GaugeRing value={summary.avg_accessibility_score} label="Accessibilité"      color="#a855f7" />
        </div>
      </div>

      {/* 4 DistBars */}
      <div className="bg-slate-900 border border-lime-500/30 rounded-xl p-5 grid grid-cols-1 md:grid-cols-2 gap-5">
        {dists.map(d => <DistBar key={d.title} {...d} />)}
      </div>

      {/* Filter pills — risk + pattern */}
      <div className="flex flex-wrap gap-2">
        {["all", "low", "moderate", "high", "critical"].map(r => (
          <button
            key={r}
            onClick={() => setFilter(r)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${filter === r ? "bg-emerald-700 border-emerald-600 text-white" : "bg-slate-900 border-slate-700 text-slate-400 hover:text-white"}`}
          >
            {r}
          </button>
        ))}
        <span className="w-px h-5 self-center bg-slate-700" />
        {["all", "cognitive_overload", "attention_fragmentation", "adaptation_failure", "engagement_collapse", "accessibility_gap", "none"].map(p => (
          <button
            key={p}
            onClick={() => setPatFilter(p)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${patFilter === p ? "bg-lime-900 border-lime-800 text-white" : "bg-slate-900 border-slate-700 text-slate-400 hover:text-white"}`}
          >
            {p.replace(/_/g, " ")}
          </button>
        ))}
      </div>

      {/* Entity cards grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {filtered.map(g => (
          <div
            key={g.interface_id}
            onClick={() => setSelected(g)}
            className="bg-slate-900 border border-slate-800 rounded-xl p-4 cursor-pointer hover:border-emerald-700 transition-colors"
          >
            <div className="flex items-center justify-between mb-1">
              <span className="font-bold text-white">{g.interface_id}</span>
              <span className="text-xs text-slate-400">{g.region}</span>
            </div>
            <div className="text-xs text-lime-400 mb-2 capitalize">{g.ux_domain.replace(/_/g, " ")}</div>
            <div className="flex gap-1 mb-3 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[g.ux_risk] || "bg-slate-700 text-slate-300"}`}>{g.ux_risk}</span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[g.ux_severity] || "bg-slate-700 text-slate-300"}`}>{g.ux_severity}</span>
            </div>
            <div className="text-2xl font-black text-white mb-1">{g.ux_composite.toFixed(1)}</div>
            <div className="text-xs text-slate-500 mb-2 capitalize">{g.ux_pattern.replace(/_/g, " ")}</div>
            <div className="text-xs text-emerald-400 font-medium mb-2">Friction: {g.estimated_cognitive_friction_index.toFixed(2)}/10</div>
            <div className="text-xs text-slate-400 line-clamp-2 leading-relaxed">{g.ux_signal}</div>
          </div>
        ))}
      </div>
    </div>
  );
}
