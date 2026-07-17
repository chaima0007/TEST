"use client";
import { useEffect, useState } from "react";

type Network = {
  network_id: string;
  network_type: string;
  region: string;
  network_risk: string;
  network_pattern: string;
  network_severity: string;
  recommended_action: string;
  topology_score: number;
  dynamics_score: number;
  resilience_score: number;
  emergence_score: number;
  network_composite: number;
  cascade_vulnerability_score: number;
  network_signal: string;
  estimated_cascade_risk_index: number;
};

type Summary = {
  total: number;
  risk_counts: Record<string, number>;
  pattern_counts: Record<string, number>;
  severity_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_network_composite: number;
  cascading_count: number;
  critical_intervention_count: number;
  avg_topology_score: number;
  avg_dynamics_score: number;
  avg_resilience_score: number;
  avg_emergence_score: number;
  avg_estimated_cascade_risk_index: number;
};

function Gauge({ value, label, color }: { value: number; label: string; color: string }) {
  const r = 36; const circ = 2 * Math.PI * r;
  const fill = circ * (1 - value / 100);
  return (
    <div className="flex flex-col items-center gap-1">
      <svg width="88" height="88" viewBox="0 0 88 88">
        <circle cx="44" cy="44" r={r} fill="none" stroke="#1e293b" strokeWidth="8"/>
        <circle cx="44" cy="44" r={r} fill="none" stroke={color} strokeWidth="8"
          strokeDasharray={circ} strokeDashoffset={fill}
          strokeLinecap="round" transform="rotate(-90 44 44)"/>
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
          <div key={k} style={{ width: `${v / total * 100}%`, background: colors[k] || "#475569" }} title={`${k}: ${v}`}/>
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
  cascade_failure: "#ef4444",
  phase_transition_collapse: "#dc2626",
  hub_fragility: "#f97316",
  attractor_instability: "#a855f7",
  complexity_overload: "#ec4899",
};
const SEV_COLORS = {
  stable_complex: "#10b981",
  fluctuating: "#f59e0b",
  critical_point: "#f97316",
  cascading: "#ef4444",
};
const ACT_COLORS = {
  no_action: "#10b981",
  topology_monitoring: "#06b6d4",
  hub_bypass: "#3b82f6",
  redundancy_injection: "#f59e0b",
  emergency_decoupling: "#ef4444",
  network_partitioning: "#dc2626",
};
const RISK_BADGE = {
  low: "bg-emerald-900 text-emerald-300",
  moderate: "bg-amber-900 text-amber-300",
  high: "bg-orange-900 text-orange-300",
  critical: "bg-red-900 text-red-300",
};
const SEV_BADGE = {
  stable_complex: "bg-emerald-900 text-emerald-300",
  fluctuating: "bg-amber-900 text-amber-300",
  critical_point: "bg-orange-900 text-orange-300",
  cascading: "bg-red-900 text-red-300",
};

function DetailModal({ network, onClose }: { network: Network; onClose: () => void }) {
  const [tab, setTab] = useState<"scores" | "signal" | "action">("scores");
  useEffect(() => {
    const h = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", h);
    return () => window.removeEventListener("keydown", h);
  }, [onClose]);
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70" onClick={onClose}>
      <div className="bg-slate-900 border border-slate-700 rounded-xl w-full max-w-lg p-6 shadow-2xl" onClick={e => e.stopPropagation()}>
        <div className="flex items-center justify-between mb-4">
          <div>
            <span className="text-lg font-bold text-white">{network.network_id}</span>
            <span className="ml-2 text-indigo-400 text-xs">{network.region}</span>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl leading-none">✕</button>
        </div>
        <div className="flex gap-2 mb-4">
          {(["scores", "signal", "action"] as const).map(t => (
            <button key={t} onClick={() => setTab(t)}
              className={`px-3 py-1 rounded text-xs font-medium transition-colors ${tab === t ? "bg-violet-700 text-white" : "bg-slate-800 text-slate-400 hover:text-white"}`}>
              {t.charAt(0).toUpperCase() + t.slice(1)}
            </button>
          ))}
        </div>
        {tab === "scores" && (
          <div className="grid grid-cols-2 gap-3 text-sm">
            {[
              ["Topologie",  network.topology_score,  "#7c3aed"],
              ["Dynamiques", network.dynamics_score,  "#ef4444"],
              ["Résilience", network.resilience_score, "#06b6d4"],
              ["Émergence",  network.emergence_score,  "#a855f7"],
            ].map(([l, v, c]) => (
              <div key={String(l)} className="bg-slate-800 rounded-lg p-3">
                <div className="text-slate-400 text-xs mb-1">{String(l)}</div>
                <div className="text-white font-bold text-lg">{Number(v).toFixed(1)}</div>
                <div className="h-1.5 rounded mt-1 bg-slate-700">
                  <div className="h-1.5 rounded" style={{ width: `${Math.min(Number(v), 100)}%`, background: String(c) }}/>
                </div>
              </div>
            ))}
            <div className="col-span-2 bg-slate-800 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Composite Réseau</div>
              <div className="text-white font-bold text-2xl">{network.network_composite.toFixed(1)}</div>
            </div>
          </div>
        )}
        {tab === "signal" && (
          <div className="bg-slate-800 rounded-lg p-4 text-sm text-slate-200 leading-relaxed">
            {network.network_signal}
            <div className="mt-3 flex gap-2 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[network.network_risk as keyof typeof RISK_BADGE] || "bg-slate-700 text-slate-300"}`}>{network.network_risk}</span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[network.network_severity as keyof typeof SEV_BADGE] || "bg-slate-700 text-slate-300"}`}>{network.network_severity}</span>
            </div>
          </div>
        )}
        {tab === "action" && (
          <div className="space-y-3 text-sm">
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Action Recommandée</div>
              <div className="text-white font-medium">{network.recommended_action.replace(/_/g, " ")}</div>
            </div>
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Indice Risque Cascade</div>
              <div className="text-white font-bold">{network.estimated_cascade_risk_index.toFixed(2)} / 10</div>
            </div>
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Type de Réseau</div>
              <div className="text-purple-300 font-medium capitalize">{network.network_type.replace(/_/g, " ")}</div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function ComplexNetworkPhysicsDashboard() {
  const [data, setData]         = useState<{ networks: Network[]; summary: Summary } | null>(null);
  const [filter, setFilter]     = useState<string>("all");
  const [patFilter, setPat]     = useState<string>("all");
  const [selected, setSelected] = useState<Network | null>(null);

  useEffect(() => {
    fetch("/api/complex-network-physics-engine")
      .then(r => r.json()).then(setData).catch(console.error);
  }, []);

  if (!data) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-slate-300 text-lg animate-pulse">Chargement du moteur de physique réseau...</div>
    </div>
  );

  const { networks, summary } = data;
  const filtered = networks.filter(n =>
    (filter === "all" || n.network_risk === filter) &&
    (patFilter === "all" || n.network_pattern === patFilter)
  );

  const dists = [
    { title: "Risque Réseau",        counts: summary.risk_counts,     colors: RISK_COLORS },
    { title: "Pattern Effondrement", counts: summary.pattern_counts,  colors: PAT_COLORS  },
    { title: "Sévérité Système",     counts: summary.severity_counts, colors: SEV_COLORS  },
    { title: "Action Recommandée",   counts: summary.action_counts,   colors: ACT_COLORS  },
  ] as Array<{ title: string; counts: Record<string, number>; colors: Record<string, string> }>;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {selected && <DetailModal network={selected} onClose={() => setSelected(null)}/>}

      <div>
        <h1 className="text-2xl font-bold text-white">Complex Network Physics &amp; Emergent Dynamics</h1>
        <p className="text-slate-400 text-sm mt-1">Topologie · Dynamiques · Résilience · Émergence — analyse des systèmes adaptatifs complexes</p>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {[
          ["Total Réseaux",       summary.total,                                                      "text-slate-300"],
          ["Cascades Critiques",  summary.cascading_count,                                            "text-red-400"],
          ["Interventions",       summary.critical_intervention_count,                                "text-orange-400"],
          ["Composite Moyen",     summary.avg_network_composite,                                      "text-violet-400"],
          ["Topologie Moy.",      `${Math.round(summary.avg_topology_score)}`,                        "text-indigo-400"],
          ["Résilience Moy.",     `${Math.round(summary.avg_resilience_score)}`,                      "text-purple-300"],
        ].map(([l, v, c]) => (
          <div key={String(l)} className="bg-slate-900 border border-slate-800 rounded-xl p-3 text-center">
            <div className={`text-xl font-bold ${c}`}>{v}</div>
            <div className="text-xs text-slate-500 mt-0.5">{l}</div>
          </div>
        ))}
      </div>

      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
        <div className="grid grid-cols-4 gap-4">
          <Gauge value={summary.avg_topology_score}  label="Robustesse Topologie" color="#7c3aed"/>
          <Gauge value={summary.avg_dynamics_score}  label="Dynamiques Réseau"    color="#ef4444"/>
          <Gauge value={summary.avg_resilience_score} label="Résilience Système"  color="#06b6d4"/>
          <Gauge value={summary.avg_emergence_score} label="Émergence Prédictible" color="#a855f7"/>
        </div>
      </div>

      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 grid grid-cols-1 md:grid-cols-2 gap-5">
        {dists.map(d => <DistBar key={d.title} {...d}/>)}
      </div>

      <div className="flex flex-wrap gap-2">
        {["all", "low", "moderate", "high", "critical"].map(r => (
          <button key={r} onClick={() => setFilter(r)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${filter === r ? "bg-violet-700 border-violet-600 text-white" : "bg-slate-900 border-slate-700 text-slate-400 hover:text-white"}`}>
            {r}
          </button>
        ))}
        <span className="w-px h-5 self-center bg-slate-700"/>
        {["all", "cascade_failure", "phase_transition_collapse", "hub_fragility", "attractor_instability", "complexity_overload", "none"].map(p => (
          <button key={p} onClick={() => setPat(p)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${patFilter === p ? "bg-slate-700 border-slate-600 text-white" : "bg-slate-900 border-slate-700 text-slate-400 hover:text-white"}`}>
            {p.replace(/_/g, " ")}
          </button>
        ))}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {filtered.map(n => (
          <div key={n.network_id} onClick={() => setSelected(n)}
            className="bg-slate-900 border border-slate-800 rounded-xl p-4 cursor-pointer hover:border-violet-700 transition-colors">
            <div className="flex items-center justify-between mb-1">
              <span className="font-bold text-white">{n.network_id}</span>
              <span className="text-xs text-slate-400">{n.region}</span>
            </div>
            <div className="text-xs text-indigo-400 mb-2 capitalize">{n.network_type.replace(/_/g, " ")}</div>
            <div className="flex gap-1 mb-3 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[n.network_risk as keyof typeof RISK_BADGE] || "bg-slate-700 text-slate-300"}`}>{n.network_risk}</span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[n.network_severity as keyof typeof SEV_BADGE] || "bg-slate-700 text-slate-300"}`}>{n.network_severity}</span>
            </div>
            <div className="text-2xl font-black text-white mb-1">{n.network_composite.toFixed(1)}</div>
            <div className="text-xs text-slate-500 mb-2 capitalize">{n.network_pattern.replace(/_/g, " ")}</div>
            <div className="text-xs text-purple-300 font-medium">Cascade idx: {n.estimated_cascade_risk_index.toFixed(2)}/10</div>
          </div>
        ))}
      </div>
    </div>
  );
}
