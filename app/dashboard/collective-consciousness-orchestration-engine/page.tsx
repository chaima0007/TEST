"use client";
import { useEffect, useState } from "react";

type SwarmNode = {
  node_id: string; node_role: string; region: string;
  swarm_risk: string; swarm_pattern: string;
  swarm_severity: string; recommended_action: string;
  coherence_score: number; intelligence_score: number;
  consensus_score: number; resilience_score: number;
  swarm_composite: number; has_fragmentation_signal: boolean;
  requires_emergency_reset: boolean; swarm_signal: string;
};
type Summary = {
  total: number; risk_counts: Record<string, number>;
  pattern_counts: Record<string, number>; severity_counts: Record<string, number>;
  action_counts: Record<string, number>; avg_swarm_composite: number;
  fragmentation_signal_count: number; emergency_reset_count: number;
  avg_coherence_score: number; avg_intelligence_score: number;
  avg_consensus_score: number; avg_resilience_score: number;
  avg_estimated_swarm_entropy_index: number;
};

function GaugeRing({ value, label, color }: { value: number; label: string; color: string }) {
  const r = 36; const circ = 2 * Math.PI * r;
  const pct = Math.round((1 - value) * 100);
  const fill = circ * value;
  return (
    <div className="flex flex-col items-center gap-1">
      <svg width="88" height="88" viewBox="0 0 88 88">
        <circle cx="44" cy="44" r={r} fill="none" stroke="#1e1b4b" strokeWidth="8"/>
        <circle cx="44" cy="44" r={r} fill="none" stroke={color} strokeWidth="8"
          strokeDasharray={circ} strokeDashoffset={fill}
          strokeLinecap="round" transform="rotate(-90 44 44)"/>
        <text x="44" y="49" textAnchor="middle" fill="white" fontSize="13" fontWeight="bold">
          {pct}
        </text>
      </svg>
      <span className="text-xs text-violet-300 text-center">{label}</span>
    </div>
  );
}

function DistBar({ title, counts, colors }: { title: string; counts: Record<string, number>; colors: Record<string, string> }) {
  const total = Object.values(counts).reduce((a, b) => a + b, 0) || 1;
  return (
    <div className="flex flex-col gap-1">
      <span className="text-xs text-violet-400 font-medium">{title}</span>
      <div className="flex h-3 rounded overflow-hidden gap-px">
        {Object.entries(counts).map(([k, v]) => (
          <div key={k} style={{ width: `${(v / total) * 100}%`, background: colors[k] || "#6d28d9" }} title={`${k}: ${v}`}/>
        ))}
      </div>
      <div className="flex flex-wrap gap-x-3 gap-y-0.5">
        {Object.entries(counts).map(([k, v]) => (
          <span key={k} className="text-xs text-slate-400">
            <span style={{ color: colors[k] || "#8b5cf6" }}>■</span> {k.replace(/_/g, " ")} {v}
          </span>
        ))}
      </div>
    </div>
  );
}

const RISK_COLORS = { low: "#10b981", moderate: "#f59e0b", high: "#f97316", critical: "#ef4444" };
const PAT_COLORS = {
  none: "#10b981", swarm_fragmentation: "#ef4444", consensus_deadlock: "#f97316",
  emergent_drift: "#a855f7", collective_amnesia: "#dc2626", orchestration_collapse: "#7f1d1d",
};
const SEV_COLORS = { unified: "#10b981", synchronizing: "#f59e0b", drifting: "#f97316", disintegrated: "#ef4444" };
const ACT_COLORS = {
  no_action: "#10b981", swarm_monitoring: "#06b6d4", diversity_rebalancing: "#3b82f6",
  consensus_protocol_refresh: "#f59e0b", orchestration_override: "#f97316",
  emergency_swarm_reset: "#ef4444",
};
const RISK_BADGE = {
  low: "bg-emerald-900 text-emerald-300", moderate: "bg-amber-900 text-amber-300",
  high: "bg-orange-900 text-orange-300", critical: "bg-red-900 text-red-300",
};
const SEV_BADGE = {
  unified: "bg-emerald-900 text-emerald-300", synchronizing: "bg-amber-900 text-amber-300",
  drifting: "bg-orange-900 text-orange-300", disintegrated: "bg-red-900 text-red-300",
};

function EntropyBar({ value }: { value: number }) {
  const pct = Math.round(value * 100);
  const color = value >= 0.60 ? "#ef4444" : value >= 0.40 ? "#f97316" : value >= 0.20 ? "#f59e0b" : "#10b981";
  return (
    <div className="mt-2">
      <div className="flex justify-between text-xs text-slate-500 mb-0.5">
        <span>Entropie essaim</span>
        <span style={{ color }}>{pct}%</span>
      </div>
      <div className="h-1.5 rounded bg-slate-800">
        <div className="h-1.5 rounded transition-all" style={{ width: `${pct}%`, background: color }}/>
      </div>
    </div>
  );
}

function DetailModal({ node, onClose }: { node: SwarmNode; onClose: () => void }) {
  const [tab, setTab] = useState<"scores" | "signal" | "action">("scores");
  useEffect(() => {
    const h = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", h);
    return () => window.removeEventListener("keydown", h);
  }, [onClose]);
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70" onClick={onClose}>
      <div className="bg-slate-900 border border-violet-500/30 rounded-xl w-full max-w-lg p-6 shadow-2xl" onClick={e => e.stopPropagation()}>
        <div className="flex items-center justify-between mb-4">
          <div>
            <span className="text-lg font-bold text-white">{node.node_id}</span>
            <span className="ml-2 text-violet-400 text-xs font-medium">{node.node_role.replace(/_/g, " ")}</span>
            <span className="ml-2 text-slate-400 text-xs">{node.region}</span>
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
              ["Cohérence", node.coherence_score, "#8b5cf6"],
              ["Intelligence", node.intelligence_score, "#a855f7"],
              ["Consensus", node.consensus_score, "#7c3aed"],
              ["Résilience", node.resilience_score, "#6d28d9"],
            ].map(([l, v, c]) => (
              <div key={String(l)} className="bg-slate-800 rounded-lg p-3">
                <div className="text-slate-400 text-xs mb-1">{String(l)}</div>
                <div className="text-white font-bold text-lg">{(Number(v) * 100).toFixed(1)}%</div>
                <div className="h-1.5 rounded mt-1 bg-slate-700">
                  <div className="h-1.5 rounded" style={{ width: `${Math.round(Number(v) * 100)}%`, background: String(c) }}/>
                </div>
              </div>
            ))}
            <div className="col-span-2 bg-slate-800 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Composite Essaim</div>
              <div className="text-white font-bold text-2xl">{(node.swarm_composite * 100).toFixed(1)}%</div>
            </div>
          </div>
        )}
        {tab === "signal" && (
          <div className="bg-slate-800 rounded-lg p-4 text-sm text-slate-200 leading-relaxed">
            {node.swarm_signal}
            <div className="mt-3 flex gap-2 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[node.swarm_risk as keyof typeof RISK_BADGE] || "bg-slate-700 text-slate-300"}`}>{node.swarm_risk}</span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[node.swarm_severity as keyof typeof SEV_BADGE] || "bg-slate-700 text-slate-300"}`}>{node.swarm_severity}</span>
              <span className="px-2 py-0.5 rounded text-xs font-medium bg-violet-900 text-violet-300">{node.swarm_pattern.replace(/_/g, " ")}</span>
            </div>
          </div>
        )}
        {tab === "action" && (
          <div className="space-y-3 text-sm">
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Action Recommandée</div>
              <div className="text-white font-medium">{node.recommended_action.replace(/_/g, " ")}</div>
            </div>
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Composite Essaim</div>
              <div className="text-white font-bold">{(node.swarm_composite * 100).toFixed(1)}% risque collectif</div>
            </div>
            <div className="flex gap-2 flex-wrap">
              {node.has_fragmentation_signal && <span className="px-2 py-1 rounded bg-violet-900 text-violet-300 text-xs font-medium">FRAGMENTATION</span>}
              {node.requires_emergency_reset && <span className="px-2 py-1 rounded bg-red-900 text-red-300 text-xs font-medium">RESET REQUIS</span>}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function CollectiveConsciousnessDashboard() {
  const [data, setData] = useState<{ nodes: SwarmNode[]; summary: Summary } | null>(null);
  const [filter, setFilter] = useState<string>("all");
  const [patFilter, setPat] = useState<string>("all");
  const [selected, setSelected] = useState<SwarmNode | null>(null);

  useEffect(() => {
    fetch("/api/collective-consciousness-orchestration-engine")
      .then(r => r.json()).then(setData).catch(console.error);
  }, []);

  if (!data) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-purple-400 text-lg animate-pulse">Synchronisation conscience collective...</div>
    </div>
  );

  const { nodes, summary } = data;
  const filtered = nodes.filter(n =>
    (filter === "all" || n.swarm_risk === filter) &&
    (patFilter === "all" || n.swarm_pattern === patFilter)
  );

  const dists: Array<{ title: string; counts: Record<string, number>; colors: Record<string, string> }> = [
    { title: "Risque Orchestration", counts: summary.risk_counts,     colors: RISK_COLORS },
    { title: "Pattern Collectif",    counts: summary.pattern_counts,  colors: PAT_COLORS  },
    { title: "Sévérité Nœud",        counts: summary.severity_counts, colors: SEV_COLORS  },
    { title: "Action Essaim",        counts: summary.action_counts,   colors: ACT_COLORS  },
  ];

  const criticalCount = (summary.risk_counts["critical"] || 0);
  const avgCoherence = Math.round((1 - summary.avg_coherence_score) * 100);
  const avgIntelligence = Math.round((1 - summary.avg_intelligence_score) * 100);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {selected && <DetailModal node={selected} onClose={() => setSelected(null)}/>}

      <div>
        <h1 className="text-2xl font-bold text-white">Conscience Collective — Orchestration Essaim</h1>
        <p className="text-violet-400 text-sm mt-1">Cohérence · Intelligence · Consensus · Résilience — méta-orchestration de l'essaim collectif</p>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {[
          ["Nœuds Actifs",         summary.total,                                                       "text-purple-400"],
          ["Fragmentation Critique", criticalCount,                                                      "text-red-400"],
          ["Cohérence Moy.",        `${avgCoherence}%`,                                                 "text-violet-400"],
          ["Intelligence Émergente", `${avgIntelligence}%`,                                             "text-purple-300"],
          ["Alertes Essaim",        summary.fragmentation_signal_count,                                 "text-amber-400"],
          ["Réinitialisations Req.", summary.emergency_reset_count,                                     "text-red-400"],
        ].map(([l, v, c]) => (
          <div key={String(l)} className="bg-slate-900 border border-violet-500/30 rounded-xl p-3 text-center">
            <div className={`text-xl font-bold ${c}`}>{v}</div>
            <div className="text-xs text-slate-500 mt-0.5">{l}</div>
          </div>
        ))}
      </div>

      <div className="bg-slate-900 border border-violet-500/30 rounded-xl p-5">
        <div className="grid grid-cols-4 gap-4">
          <GaugeRing value={summary.avg_coherence_score}     label="Cohérence Essaim"     color="#8b5cf6"/>
          <GaugeRing value={summary.avg_intelligence_score}  label="Intelligence Collective" color="#a855f7"/>
          <GaugeRing value={summary.avg_consensus_score}     label="Consensus Distribué"  color="#7c3aed"/>
          <GaugeRing value={summary.avg_resilience_score}    label="Résilience Réseau"    color="#6d28d9"/>
        </div>
      </div>

      <div className="bg-slate-900 border border-violet-500/30 rounded-xl p-5 grid grid-cols-1 md:grid-cols-2 gap-5">
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
        {["all", "none", "swarm_fragmentation", "consensus_deadlock", "emergent_drift", "collective_amnesia", "orchestration_collapse"].map(p => (
          <button key={p} onClick={() => setPat(p)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${patFilter === p ? "bg-purple-900 border-purple-800 text-white" : "bg-slate-900 border-slate-700 text-slate-400 hover:text-white"}`}>
            {p.replace(/_/g, " ")}
          </button>
        ))}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {filtered.map(n => (
          <div key={n.node_id} onClick={() => setSelected(n)}
            className="bg-slate-900 border border-violet-500/30 rounded-xl p-4 cursor-pointer hover:border-violet-500 transition-colors">
            <div className="flex items-center justify-between mb-1">
              <span className="font-bold text-white">{n.node_id}</span>
              <span className="text-xs text-slate-400">{n.region}</span>
            </div>
            <div className="text-xs text-violet-400 mb-2">{n.node_role.replace(/_/g, " ")}</div>
            <div className="flex gap-1 mb-3 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[n.swarm_risk as keyof typeof RISK_BADGE] || "bg-slate-700 text-slate-300"}`}>{n.swarm_risk}</span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[n.swarm_severity as keyof typeof SEV_BADGE] || "bg-slate-700 text-slate-300"}`}>{n.swarm_severity}</span>
            </div>
            <div className="text-2xl font-black text-white mb-1">{(n.swarm_composite * 100).toFixed(1)}%</div>
            <div className="text-xs text-slate-500 mb-2 capitalize">{n.swarm_pattern.replace(/_/g, " ")}</div>
            <EntropyBar value={n.swarm_composite}/>
            <div className="flex gap-1 flex-wrap mt-2">
              {n.has_fragmentation_signal  && <span className="px-1.5 py-0.5 rounded bg-violet-900 text-violet-300 text-xs">FRAG</span>}
              {n.requires_emergency_reset  && <span className="px-1.5 py-0.5 rounded bg-red-900 text-red-300 text-xs">RESET</span>}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
