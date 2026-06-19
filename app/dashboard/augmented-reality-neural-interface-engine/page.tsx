"use client";
import { useEffect, useState } from "react";

type ARInterface = {
  interface_id: string;
  interface_type: string;
  region: string;
  neural_risk_score: number;
  immersion_score: number;
  safety_score: number;
  integrity_score: number;
  neural_risk_composite: number;
  neural_risk: string;
  neural_pattern: string;
  neural_severity: string;
  recommended_action: string;
  has_critical_signal: boolean;
  requires_disconnect: boolean;
  estimated_neural_risk_index: number;
  neural_signal: string;
};

type Summary = {
  total: number;
  risk_counts: Record<string, number>;
  pattern_counts: Record<string, number>;
  severity_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_neural_risk_composite: number;
  critical_signal_count: number;
  disconnect_required_count: number;
  avg_neural_risk_score: number;
  avg_immersion_score: number;
  avg_safety_score: number;
  avg_integrity_score: number;
  avg_estimated_neural_risk_index: number;
};

// ── GaugeRing ──────────────────────────────────────────────────────────────────
function GaugeRing({ value, label, color }: { value: number; label: string; color: string }) {
  const r = 36;
  const circ = 2 * Math.PI * r;
  const fill = circ * (1 - value / 100);
  return (
    <div className="flex flex-col items-center gap-1">
      <svg width="88" height="88" viewBox="0 0 88 88">
        <circle cx="44" cy="44" r={r} fill="none" stroke="#0f172a" strokeWidth="8" />
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

// ── DistBar ────────────────────────────────────────────────────────────────────
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

// ── Color maps ─────────────────────────────────────────────────────────────────
const RISK_COLORS: Record<string, string> = {
  low: "#10b981", moderate: "#f59e0b", high: "#f97316", critical: "#ef4444",
};
const PAT_COLORS: Record<string, string> = {
  none: "#10b981",
  neural_overload: "#ef4444",
  reality_dissociation: "#f97316",
  biometric_breach: "#dc2626",
  bci_failure: "#a855f7",
  sensory_collapse: "#7c3aed",
};
const SEV_COLORS: Record<string, string> = {
  immersive: "#10b981",
  calibrating: "#f59e0b",
  unstable: "#f97316",
  critical_neural: "#ef4444",
};
const ACT_COLORS: Record<string, string> = {
  no_action: "#10b981",
  neural_monitoring: "#06b6d4",
  immersion_recalibration: "#3b82f6",
  privacy_shield: "#a855f7",
  bci_safety_lockdown: "#f97316",
  neural_emergency_disconnect: "#ef4444",
};
const RISK_BADGE: Record<string, string> = {
  low: "bg-emerald-900 text-emerald-300",
  moderate: "bg-amber-900 text-amber-300",
  high: "bg-orange-900 text-orange-300",
  critical: "bg-red-900 text-red-300",
};
const SEV_BADGE: Record<string, string> = {
  immersive: "bg-emerald-900 text-emerald-300",
  calibrating: "bg-amber-900 text-amber-300",
  unstable: "bg-orange-900 text-orange-300",
  critical_neural: "bg-red-900 text-red-300",
};

// ── DetailModal ────────────────────────────────────────────────────────────────
function DetailModal({ iface, onClose }: { iface: ARInterface; onClose: () => void }) {
  const [tab, setTab] = useState<"scores" | "signal" | "action">("scores");

  useEffect(() => {
    const h = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", h);
    return () => window.removeEventListener("keydown", h);
  }, [onClose]);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70" onClick={onClose}>
      <div
        className="bg-slate-900 border border-cyan-500/30 rounded-xl w-full max-w-lg p-6 shadow-2xl"
        onClick={e => e.stopPropagation()}
      >
        {/* Header */}
        <div className="flex items-center justify-between mb-4">
          <div>
            <span className="text-lg font-bold text-white">{iface.interface_id}</span>
            <span className="ml-2 text-teal-400 text-xs">{iface.interface_type.replace(/_/g, " ")}</span>
            <span className="ml-2 text-cyan-400 text-xs">{iface.region}</span>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl leading-none">✕</button>
        </div>

        {/* Tabs */}
        <div className="flex gap-2 mb-4">
          {(["scores", "signal", "action"] as const).map(t => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`px-3 py-1 rounded text-xs font-medium transition-colors ${
                tab === t ? "bg-teal-700 text-white" : "bg-slate-800 text-slate-400 hover:text-white"
              }`}
            >
              {t.charAt(0).toUpperCase() + t.slice(1)}
            </button>
          ))}
        </div>

        {/* Tab: Scores */}
        {tab === "scores" && (
          <div className="grid grid-cols-2 gap-3 text-sm">
            {([
              ["Risque Neural", iface.neural_risk_score, "#ef4444"],
              ["Immersion", iface.immersion_score, "#06b6d4"],
              ["Sécurité", iface.safety_score, "#f97316"],
              ["Intégrité Signal", iface.integrity_score, "#a855f7"],
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
              <div className="text-slate-400 text-xs mb-1">Composite Risque Neural</div>
              <div className="text-white font-bold text-2xl">{iface.neural_risk_composite.toFixed(1)}</div>
            </div>
          </div>
        )}

        {/* Tab: Signal */}
        {tab === "signal" && (
          <div className="bg-slate-800 rounded-lg p-4 text-sm text-slate-200 leading-relaxed">
            {iface.neural_signal}
            <div className="mt-3 flex gap-2 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[iface.neural_risk] || "bg-slate-700 text-slate-300"}`}>
                {iface.neural_risk}
              </span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[iface.neural_severity] || "bg-slate-700 text-slate-300"}`}>
                {iface.neural_severity}
              </span>
            </div>
          </div>
        )}

        {/* Tab: Action */}
        {tab === "action" && (
          <div className="space-y-3 text-sm">
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Action Recommandée</div>
              <div className="text-white font-medium">{iface.recommended_action.replace(/_/g, " ")}</div>
            </div>
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Indice Risque Neural Estimé</div>
              <div className="text-white font-bold">{iface.estimated_neural_risk_index.toFixed(2)} / 10</div>
            </div>
            <div className="bg-slate-800 rounded-lg p-3 flex gap-4">
              <div>
                <div className="text-slate-400 text-xs mb-1">Signal Critique</div>
                <div className={`text-xs font-semibold ${iface.has_critical_signal ? "text-red-400" : "text-emerald-400"}`}>
                  {iface.has_critical_signal ? "Oui" : "Non"}
                </div>
              </div>
              <div>
                <div className="text-slate-400 text-xs mb-1">Déconnexion Req.</div>
                <div className={`text-xs font-semibold ${iface.requires_disconnect ? "text-orange-400" : "text-emerald-400"}`}>
                  {iface.requires_disconnect ? "Oui" : "Non"}
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

// ── Main Dashboard ─────────────────────────────────────────────────────────────
export default function ARNeuralInterfaceDashboard() {
  const [data, setData] = useState<{ interfaces: ARInterface[]; summary: Summary } | null>(null);
  const [filter, setFilter] = useState<string>("all");
  const [patFilter, setPatFilter] = useState<string>("all");
  const [selected, setSelected] = useState<ARInterface | null>(null);

  useEffect(() => {
    fetch("/api/augmented-reality-neural-interface-engine")
      .then(r => r.json())
      .then(setData)
      .catch(console.error);
  }, []);

  if (!data) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-teal-400 text-lg animate-pulse">Loading AR Neural Interface Engine...</div>
    </div>
  );

  const { interfaces, summary } = data;

  const filtered = interfaces.filter(g =>
    (filter === "all" || g.neural_risk === filter) &&
    (patFilter === "all" || g.neural_pattern === patFilter),
  );

  const dists: Array<{ title: string; counts: Record<string, number>; colors: Record<string, string> }> = [
    { title: "Risque Interface",  counts: summary.risk_counts,     colors: RISK_COLORS },
    { title: "Pattern Neural",    counts: summary.pattern_counts,  colors: PAT_COLORS  },
    { title: "Sévérité BCI",      counts: summary.severity_counts, colors: SEV_COLORS  },
    { title: "Action Requise",    counts: summary.action_counts,   colors: ACT_COLORS  },
  ];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {selected && <DetailModal iface={selected} onClose={() => setSelected(null)} />}

      {/* Title */}
      <div>
        <h1 className="text-2xl font-bold text-white">
          Augmented Reality Engineering &amp; Neural Interface Engine
        </h1>
        <p className="text-slate-400 text-sm mt-1">
          AR/XR · Interface neuronale · Latence BCI · Sécurité biométrique · Immersion XR
        </p>
      </div>

      {/* KPI strip — 6 cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {([
          ["Interfaces Actives",         summary.total,                                              "text-teal-400"],
          ["Risques Neuronaux Critiques", summary.risk_counts["critical"] ?? 0,                      "text-red-400"],
          ["Latence Neuronale Moy.",      `${summary.avg_neural_risk_score.toFixed(1)}`,             "text-orange-400"],
          ["Score Immersion Moy.",        `${summary.avg_immersion_score.toFixed(1)}`,               "text-cyan-400"],
          ["Alertes BCI",                 summary.critical_signal_count,                             "text-amber-400"],
          ["Déconnexions Req.",           summary.disconnect_required_count,                         "text-red-300"],
        ] as [string, string | number, string][]).map(([l, v, c]) => (
          <div key={String(l)} className="bg-slate-900 border border-cyan-500/30 rounded-xl p-3 text-center">
            <div className={`text-xl font-bold ${c}`}>{v}</div>
            <div className="text-xs text-slate-500 mt-0.5">{l}</div>
          </div>
        ))}
      </div>

      {/* 4 SVG GaugeRings */}
      <div className="bg-slate-900 border border-cyan-500/30 rounded-xl p-5">
        <div className="grid grid-cols-4 gap-4">
          <GaugeRing value={summary.avg_neural_risk_score}  label="Risque Neural"       color="#ef4444" />
          <GaugeRing value={summary.avg_immersion_score}    label="Profondeur Immersion" color="#06b6d4" />
          <GaugeRing value={summary.avg_safety_score}       label="Sécurité Biométrique" color="#f97316" />
          <GaugeRing value={summary.avg_integrity_score}    label="Intégrité Signal"     color="#a855f7" />
        </div>
      </div>

      {/* 4 DistBars */}
      <div className="bg-slate-900 border border-cyan-500/30 rounded-xl p-5 grid grid-cols-1 md:grid-cols-2 gap-5">
        {dists.map(d => <DistBar key={d.title} {...d} />)}
      </div>

      {/* Filter pills — risk + pattern */}
      <div className="flex flex-wrap gap-2">
        {["all", "low", "moderate", "high", "critical"].map(r => (
          <button
            key={r}
            onClick={() => setFilter(r)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${
              filter === r
                ? "bg-teal-700 border-teal-600 text-white"
                : "bg-slate-900 border-slate-700 text-slate-400 hover:text-white"
            }`}
          >
            {r}
          </button>
        ))}
        <span className="w-px h-5 self-center bg-slate-700" />
        {["all", "neural_overload", "reality_dissociation", "biometric_breach", "bci_failure", "sensory_collapse", "none"].map(p => (
          <button
            key={p}
            onClick={() => setPatFilter(p)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${
              patFilter === p
                ? "bg-cyan-900 border-cyan-800 text-white"
                : "bg-slate-900 border-slate-700 text-slate-400 hover:text-white"
            }`}
          >
            {p.replace(/_/g, " ")}
          </button>
        ))}
      </div>

      {/* Interface cards grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {filtered.map(g => (
          <div
            key={g.interface_id}
            onClick={() => setSelected(g)}
            className="bg-slate-900 border border-slate-800 rounded-xl p-4 cursor-pointer hover:border-teal-600 transition-colors"
          >
            <div className="flex items-center justify-between mb-1">
              <span className="font-bold text-white">{g.interface_id}</span>
              <span className="text-xs text-slate-400">{g.region}</span>
            </div>
            <div className="text-xs text-teal-400 mb-2 capitalize">{g.interface_type.replace(/_/g, " ")}</div>
            <div className="flex gap-1 mb-3 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[g.neural_risk] || "bg-slate-700 text-slate-300"}`}>
                {g.neural_risk}
              </span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[g.neural_severity] || "bg-slate-700 text-slate-300"}`}>
                {g.neural_severity}
              </span>
            </div>
            {/* Neural risk indicator bar */}
            <div className="mb-2">
              <div className="flex justify-between text-xs text-slate-500 mb-1">
                <span>Risque Neural</span>
                <span className="text-teal-400 font-semibold">{g.neural_risk_composite.toFixed(1)}</span>
              </div>
              <div className="h-1.5 rounded bg-slate-800">
                <div
                  className="h-1.5 rounded"
                  style={{
                    width: `${Math.min(g.neural_risk_composite, 100)}%`,
                    background: RISK_COLORS[g.neural_risk] || "#475569",
                  }}
                />
              </div>
            </div>
            <div className="text-xs text-slate-500 mb-2 capitalize">{g.neural_pattern.replace(/_/g, " ")}</div>
            <div className="text-xs text-cyan-400 font-medium mb-2">
              Indice: {g.estimated_neural_risk_index.toFixed(2)}/10
            </div>
            <div className="text-xs text-slate-400 line-clamp-2 leading-relaxed">{g.neural_signal}</div>
          </div>
        ))}
      </div>
    </div>
  );
}
