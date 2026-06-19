"use client";
import { useEffect, useState } from "react";

type Talent = {
  talent_id: string;
  talent_segment: string;
  region: string;
  talent_risk: string;
  talent_pattern: string;
  talent_severity: string;
  recommended_action: string;
  obsolescence_score: number;
  flight_score: number;
  value_score: number;
  succession_score: number;
  talent_composite: number;
  has_obsolescence_signal: boolean;
  requires_urgent_intervention: boolean;
  estimated_talent_risk_index: number;
  talent_signal: string;
};

type Summary = {
  total: number;
  risk_counts: Record<string, number>;
  pattern_counts: Record<string, number>;
  severity_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_talent_composite: number;
  obsolescence_signal_count: number;
  urgent_intervention_count: number;
  avg_obsolescence_score: number;
  avg_flight_score: number;
  avg_succession_score: number;
  avg_value_score: number;
  avg_estimated_talent_risk_index: number;
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
          cx="44" cy="44" r={r} fill="none"
          stroke={color} strokeWidth="8"
          strokeDasharray={circ} strokeDashoffset={fill}
          strokeLinecap="round"
          transform="rotate(-90 44 44)"
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
          <div
            key={k}
            style={{ width: `${(v / total) * 100}%`, background: colors[k] || "#475569" }}
            title={`${k}: ${v}`}
          />
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

const RISK_COLORS  = { low: "#10b981", moderate: "#f59e0b", high: "#f97316", critical: "#ef4444" };
const PAT_COLORS   = {
  none: "#10b981",
  talent_obsolescence: "#ef4444",
  flight_risk_crisis: "#f97316",
  knowledge_drain: "#a855f7",
  succession_gap: "#dc2626",
  potential_stagnation: "#f59e0b",
};
const SEV_COLORS   = { thriving: "#10b981", developing: "#f59e0b", declining: "#f97316", at_risk: "#ef4444" };
const ACT_COLORS   = {
  no_action: "#10b981",
  talent_monitoring: "#06b6d4",
  succession_acceleration: "#3b82f6",
  engagement_intervention: "#f59e0b",
  reskilling_program: "#a855f7",
  talent_emergency_retention: "#ef4444",
};
const RISK_BADGE   = {
  low: "bg-emerald-900 text-emerald-300",
  moderate: "bg-amber-900 text-amber-300",
  high: "bg-orange-900 text-orange-300",
  critical: "bg-red-900 text-red-300",
};
const SEV_BADGE    = {
  thriving: "bg-emerald-900 text-emerald-300",
  developing: "bg-amber-900 text-amber-300",
  declining: "bg-orange-900 text-orange-300",
  at_risk: "bg-red-900 text-red-300",
};

function DetailModal({ talent, onClose }: { talent: Talent; onClose: () => void }) {
  const [tab, setTab] = useState<"scores" | "signal" | "action">("scores");

  useEffect(() => {
    const h = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", h);
    return () => window.removeEventListener("keydown", h);
  }, [onClose]);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70" onClick={onClose}>
      <div
        className="bg-slate-900 border border-indigo-500/30 rounded-xl w-full max-w-lg p-6 shadow-2xl"
        onClick={e => e.stopPropagation()}
      >
        <div className="flex items-center justify-between mb-4">
          <div>
            <span className="text-lg font-bold text-white">{talent.talent_id}</span>
            <span className="ml-2 text-blue-400 text-xs">{talent.region}</span>
            <span className="ml-2 text-slate-500 text-xs capitalize">{talent.talent_segment.replace(/_/g, " ")}</span>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl leading-none">✕</button>
        </div>

        <div className="flex gap-2 mb-4">
          {(["scores", "signal", "action"] as const).map(t => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`px-3 py-1 rounded text-xs font-medium transition-colors ${
                tab === t ? "bg-indigo-700 text-white" : "bg-slate-800 text-slate-400 hover:text-white"
              }`}
            >
              {t.charAt(0).toUpperCase() + t.slice(1)}
            </button>
          ))}
        </div>

        {tab === "scores" && (
          <div className="grid grid-cols-2 gap-3 text-sm">
            {([
              ["Obsolescence", talent.obsolescence_score, "#ef4444"],
              ["Flight Risk",  talent.flight_score,       "#f97316"],
              ["Value Gap",    talent.value_score,        "#a855f7"],
              ["Succession",   talent.succession_score,   "#3b82f6"],
            ] as [string, number, string][]).map(([l, v, c]) => (
              <div key={l} className="bg-slate-800 rounded-lg p-3">
                <div className="text-slate-400 text-xs mb-1">{l}</div>
                <div className="text-white font-bold text-lg">{v.toFixed(1)}</div>
                <div className="h-1.5 rounded mt-1 bg-slate-700">
                  <div className="h-1.5 rounded" style={{ width: `${Math.min(v, 100)}%`, background: c }} />
                </div>
              </div>
            ))}
            <div className="col-span-2 bg-slate-800 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Talent Composite</div>
              <div className="text-white font-bold text-2xl">{talent.talent_composite.toFixed(1)}</div>
            </div>
          </div>
        )}

        {tab === "signal" && (
          <div className="bg-slate-800 rounded-lg p-4 text-sm text-slate-200 leading-relaxed">
            {talent.talent_signal}
            <div className="mt-3 flex gap-2 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[talent.talent_risk as keyof typeof RISK_BADGE] || "bg-slate-700 text-slate-300"}`}>
                {talent.talent_risk}
              </span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[talent.talent_severity as keyof typeof SEV_BADGE] || "bg-slate-700 text-slate-300"}`}>
                {talent.talent_severity}
              </span>
            </div>
          </div>
        )}

        {tab === "action" && (
          <div className="space-y-3 text-sm">
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Recommended Action</div>
              <div className="text-white font-medium capitalize">{talent.recommended_action.replace(/_/g, " ")}</div>
            </div>
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Talent Risk Index</div>
              <div className="text-white font-bold">{talent.estimated_talent_risk_index.toFixed(2)} / 10</div>
            </div>
            <div className="flex gap-2 flex-wrap">
              {talent.has_obsolescence_signal    && <span className="px-2 py-1 rounded bg-amber-900 text-amber-300 text-xs font-medium">OBSOLESCENCE</span>}
              {talent.requires_urgent_intervention && <span className="px-2 py-1 rounded bg-red-900 text-red-300 text-xs font-medium">URGENT</span>}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function PredictiveTalentDashboard() {
  const [data, setData]         = useState<{ talents: Talent[]; summary: Summary } | null>(null);
  const [filter, setFilter]     = useState<string>("all");
  const [patFilter, setPatFilter] = useState<string>("all");
  const [selected, setSelected] = useState<Talent | null>(null);

  useEffect(() => {
    fetch("/api/predictive-talent-intelligence-engine")
      .then(r => r.json())
      .then(setData)
      .catch(console.error);
  }, []);

  if (!data) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-blue-400 text-lg animate-pulse">Loading Talent Intelligence Engine...</div>
    </div>
  );

  const { talents, summary } = data;

  const filtered = talents.filter(t =>
    (filter === "all" || t.talent_risk === filter) &&
    (patFilter === "all" || t.talent_pattern === patFilter)
  );

  const dists: Array<{ title: string; counts: Record<string, number>; colors: Record<string, string> }> = [
    { title: "Risk",     counts: summary.risk_counts,     colors: RISK_COLORS },
    { title: "Pattern",  counts: summary.pattern_counts,  colors: PAT_COLORS  },
    { title: "Severity", counts: summary.severity_counts, colors: SEV_COLORS  },
    { title: "Action",   counts: summary.action_counts,   colors: ACT_COLORS  },
  ];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {selected && <DetailModal talent={selected} onClose={() => setSelected(null)} />}

      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-white">Predictive Talent Intelligence & Human Capital Engine</h1>
        <p className="text-slate-400 text-sm mt-1">
          Trajectoires · Obsolescence · Rétention · Succession — Module 277 Caelum Partners
        </p>
      </div>

      {/* KPI Cards — 6 */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {([
          ["Talents",          summary.total,                                                      "text-blue-400"],
          ["Avg Composite",    summary.avg_talent_composite,                                       "text-indigo-400"],
          ["Obsolescence",     summary.obsolescence_signal_count,                                  "text-amber-400"],
          ["Urgent Action",    summary.urgent_intervention_count,                                  "text-red-400"],
          ["Avg Risk Index",   `${summary.avg_estimated_talent_risk_index.toFixed(1)}/10`,         "text-blue-400"],
          ["Avg Flight",       `${Math.round(summary.avg_flight_score)}`,                          "text-indigo-400"],
        ] as [string, string | number, string][]).map(([l, v, c]) => (
          <div key={l} className="bg-slate-900 border border-indigo-500/30 rounded-xl p-3 text-center">
            <div className={`text-xl font-bold ${c}`}>{v}</div>
            <div className="text-xs text-slate-500 mt-0.5">{l}</div>
          </div>
        ))}
      </div>

      {/* 4 SVG GaugeRings */}
      <div className="bg-slate-900 border border-indigo-500/30 rounded-xl p-5">
        <div className="grid grid-cols-4 gap-4">
          <GaugeRing value={summary.avg_obsolescence_score} label="Obsolescence" color="#ef4444" />
          <GaugeRing value={summary.avg_flight_score}       label="Flight Risk"  color="#f97316" />
          <GaugeRing value={summary.avg_value_score}        label="Value Gap"    color="#a855f7" />
          <GaugeRing value={summary.avg_succession_score}   label="Succession"   color="#3b82f6" />
        </div>
      </div>

      {/* 4 DistBars */}
      <div className="bg-slate-900 border border-indigo-500/30 rounded-xl p-5 grid grid-cols-1 md:grid-cols-2 gap-5">
        {dists.map(d => <DistBar key={d.title} {...d} />)}
      </div>

      {/* Filter pills */}
      <div className="flex flex-wrap gap-2">
        {["all", "low", "moderate", "high", "critical"].map(r => (
          <button
            key={r}
            onClick={() => setFilter(r)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${
              filter === r
                ? "bg-blue-700 border-blue-600 text-white"
                : "bg-slate-900 border-slate-700 text-slate-400 hover:text-white"
            }`}
          >
            {r}
          </button>
        ))}
        <span className="w-px h-5 self-center bg-slate-700" />
        {["all", "none", "talent_obsolescence", "flight_risk_crisis", "knowledge_drain", "succession_gap", "potential_stagnation"].map(p => (
          <button
            key={p}
            onClick={() => setPatFilter(p)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${
              patFilter === p
                ? "bg-indigo-900 border-indigo-700 text-white"
                : "bg-slate-900 border-slate-700 text-slate-400 hover:text-white"
            }`}
          >
            {p.replace(/_/g, " ")}
          </button>
        ))}
      </div>

      {/* Talent cards grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {filtered.map(t => (
          <div
            key={t.talent_id}
            onClick={() => setSelected(t)}
            className="bg-slate-900 border border-indigo-500/30 rounded-xl p-4 cursor-pointer hover:border-blue-500 transition-colors"
          >
            <div className="flex items-center justify-between mb-1">
              <span className="font-bold text-white">{t.talent_id}</span>
              <span className="text-xs text-slate-400">{t.region}</span>
            </div>
            <div className="text-xs text-slate-500 mb-2 capitalize">{t.talent_segment.replace(/_/g, " ")}</div>
            <div className="flex gap-1 mb-3 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[t.talent_risk as keyof typeof RISK_BADGE] || "bg-slate-700 text-slate-300"}`}>
                {t.talent_risk}
              </span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[t.talent_severity as keyof typeof SEV_BADGE] || "bg-slate-700 text-slate-300"}`}>
                {t.talent_severity}
              </span>
            </div>
            <div className="text-2xl font-black text-white mb-1">{t.talent_composite.toFixed(1)}</div>
            <div className="text-xs text-slate-500 mb-2 capitalize">{t.talent_pattern.replace(/_/g, " ")}</div>
            <div className="text-xs text-blue-400 font-medium mb-2">Risk Index: {t.estimated_talent_risk_index.toFixed(2)}/10</div>
            <div className="flex gap-1 flex-wrap">
              {t.has_obsolescence_signal      && <span className="px-1.5 py-0.5 rounded bg-amber-900 text-amber-300 text-xs">OBSOLESCENCE</span>}
              {t.requires_urgent_intervention && <span className="px-1.5 py-0.5 rounded bg-red-900 text-red-300 text-xs">URGENT</span>}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
