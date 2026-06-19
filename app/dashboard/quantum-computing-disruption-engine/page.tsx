"use client";
import { useEffect, useState } from "react";

type Entity = {
  entity_id: string;
  region: string;
  sector: string;
  quantum_risk: string;
  quantum_pattern: string;
  quantum_severity: string;
  recommended_action: string;
  cryptographic_score: number;
  readiness_score: number;
  infrastructure_score: number;
  geopolitical_score: number;
  quantum_composite: number;
  is_quantum_crisis: boolean;
  requires_quantum_intervention: boolean;
  quantum_signal: string;
};

type Summary = {
  total: number;
  risk_counts: Record<string, number>;
  pattern_counts: Record<string, number>;
  severity_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_quantum_composite: number;
  quantum_crisis_count: number;
  quantum_intervention_count: number;
  avg_cryptographic_score: number;
  avg_readiness_score: number;
  avg_infrastructure_score: number;
  avg_geopolitical_score: number;
  avg_estimated_quantum_disruption_index: number;
};

function GaugeRing({ value, label, color }: { value: number; label: string; color: string }) {
  const r = 36;
  const circ = 2 * Math.PI * r;
  const fill = circ * (1 - value / 100);
  return (
    <div className="flex flex-col items-center gap-1">
      <svg width="88" height="88" viewBox="0 0 88 88">
        <circle cx="44" cy="44" r={r} fill="none" stroke="#0a0520" strokeWidth="8" />
        <circle cx="44" cy="44" r={r} fill="none" stroke={color} strokeWidth="8"
          strokeDasharray={circ} strokeDashoffset={fill}
          strokeLinecap="round" transform="rotate(-90 44 44)" />
        <text x="44" y="49" textAnchor="middle" fill="white" fontSize="13" fontWeight="bold">
          {Math.round(value)}
        </text>
      </svg>
      <span className="text-xs text-violet-300/70 text-center">{label}</span>
    </div>
  );
}

function DistBar({ title, counts, colors }: { title: string; counts: Record<string, number>; colors: Record<string, string> }) {
  const total = Object.values(counts).reduce((a, b) => a + b, 0) || 1;
  return (
    <div className="flex flex-col gap-1">
      <span className="text-xs text-violet-300/70 font-medium">{title}</span>
      <div className="flex h-3 rounded overflow-hidden gap-px">
        {Object.entries(counts).map(([k, v]) => (
          <div key={k} style={{ width: `${(v / total) * 100}%`, background: colors[k] || "#475569" }} title={`${k}: ${v}`} />
        ))}
      </div>
      <div className="flex flex-wrap gap-x-3 gap-y-0.5">
        {Object.entries(counts).map(([k, v]) => (
          <span key={k} className="text-xs text-violet-300/60">
            <span style={{ color: colors[k] || "#94a3b8" }}>■</span> {k.replace(/_/g, " ")} {v}
          </span>
        ))}
      </div>
    </div>
  );
}

const RISK_COLORS = { low: "#10b981", moderate: "#f59e0b", high: "#f97316", critical: "#a855f7" };
const PAT_COLORS = {
  none: "#10b981",
  cryptographic_apocalypse: "#7c3aed",
  quantum_surprise_attack: "#dc2626",
  infrastructure_quantum_shock: "#f97316",
  financial_system_collapse: "#0ea5e9",
  talent_capability_gap: "#f59e0b",
};
const SEV_COLORS = {
  quantum_secure: "#10b981",
  quantum_preparing: "#f59e0b",
  high_quantum_risk: "#f97316",
  quantum_emergency: "#7c3aed",
};
const ACTION_COLORS = {
  no_action: "#10b981",
  quantum_monitoring: "#06b6d4",
  quantum_transition_plan: "#f59e0b",
  immediate_pqc_deployment: "#f97316",
  quantum_emergency_migration: "#7c3aed",
};

const RISK_BADGE = {
  low: "bg-emerald-900 text-emerald-300",
  moderate: "bg-amber-900 text-amber-300",
  high: "bg-orange-900 text-orange-300",
  critical: "bg-violet-950 text-violet-300",
};
const SEV_BADGE = {
  quantum_secure: "bg-emerald-900 text-emerald-300",
  quantum_preparing: "bg-amber-900 text-amber-300",
  high_quantum_risk: "bg-orange-900 text-orange-300",
  quantum_emergency: "bg-violet-950 text-violet-300",
};

function DetailModal({ entity, onClose }: { entity: Entity; onClose: () => void }) {
  const [tab, setTab] = useState<"scores" | "signal" | "action">("scores");
  useEffect(() => {
    const h = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", h);
    return () => window.removeEventListener("keydown", h);
  }, [onClose]);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80" onClick={onClose}>
      <div className="bg-slate-950 border border-cyan-700/30 rounded-xl w-full max-w-lg p-6 shadow-2xl" onClick={e => e.stopPropagation()}>
        <div className="flex items-center justify-between mb-4">
          <div>
            <span className="text-lg font-bold text-white">{entity.entity_id}</span>
            <span className="ml-2 text-violet-400 text-xs">{entity.region}</span>
            <span className="ml-2 text-slate-500 text-xs">{entity.sector.replace(/_/g, " ")}</span>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl leading-none">✕</button>
        </div>
        <div className="flex gap-2 mb-4">
          {(["scores", "signal", "action"] as const).map(t => (
            <button key={t} onClick={() => setTab(t)}
              className={`px-3 py-1 rounded text-xs font-medium transition-colors ${tab === t ? "bg-violet-900 text-white" : "bg-slate-900 text-slate-400 hover:text-white"}`}>
              {t.charAt(0).toUpperCase() + t.slice(1)}
            </button>
          ))}
        </div>

        {tab === "scores" && (
          <div className="grid grid-cols-2 gap-3 text-sm">
            {[
              ["Cryptographique",  entity.cryptographic_score,  "#7c3aed"],
              ["Préparation",      entity.readiness_score,      "#06b6d4"],
              ["Infrastructure",   entity.infrastructure_score, "#f97316"],
              ["Géopolitique",     entity.geopolitical_score,   "#f59e0b"],
            ].map(([l, v, c]) => (
              <div key={String(l)} className="bg-slate-900 border border-cyan-700/20 rounded-lg p-3">
                <div className="text-violet-300/60 text-xs mb-1">{String(l)}</div>
                <div className="text-white font-bold text-lg">{Number(v).toFixed(1)}</div>
                <div className="h-1.5 rounded mt-1 bg-slate-800">
                  <div className="h-1.5 rounded" style={{ width: `${Math.min(Number(v), 100)}%`, background: String(c) }} />
                </div>
              </div>
            ))}
            <div className="col-span-2 bg-slate-900 border border-cyan-700/20 rounded-lg p-3">
              <div className="text-violet-300/60 text-xs mb-1">Composite Quantique</div>
              <div className="text-white font-bold text-2xl">{entity.quantum_composite.toFixed(1)}</div>
            </div>
          </div>
        )}

        {tab === "signal" && (
          <div className="bg-slate-900 border border-cyan-700/20 rounded-lg p-4 text-sm text-slate-200 leading-relaxed">
            {entity.quantum_signal}
            <div className="mt-3 flex gap-2 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[entity.quantum_risk as keyof typeof RISK_BADGE] || "bg-slate-700 text-slate-300"}`}>
                {entity.quantum_risk}
              </span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[entity.quantum_severity as keyof typeof SEV_BADGE] || "bg-slate-700 text-slate-300"}`}>
                {entity.quantum_severity.replace(/_/g, " ")}
              </span>
            </div>
          </div>
        )}

        {tab === "action" && (
          <div className="space-y-3 text-sm">
            <div className="bg-slate-900 border border-cyan-700/20 rounded-lg p-3">
              <div className="text-violet-300/60 text-xs mb-1">Action Recommandée</div>
              <div className="text-white font-medium">{entity.recommended_action.replace(/_/g, " ")}</div>
            </div>
            <div className="bg-slate-900 border border-cyan-700/20 rounded-lg p-3">
              <div className="text-violet-300/60 text-xs mb-1">Patron Quantique</div>
              <div className="text-white font-medium capitalize">{entity.quantum_pattern.replace(/_/g, " ")}</div>
            </div>
            <div className="flex gap-2 flex-wrap">
              {entity.is_quantum_crisis && (
                <span className="px-2 py-1 rounded bg-violet-950 text-violet-300 text-xs font-medium">CRISE QUANTIQUE</span>
              )}
              {entity.requires_quantum_intervention && (
                <span className="px-2 py-1 rounded bg-cyan-950 text-cyan-400 text-xs font-medium">INTERVENTION REQ.</span>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function QuantumComputingDisruptionDashboard() {
  const [data, setData]         = useState<{ entities: Entity[]; summary: Summary } | null>(null);
  const [filter, setFilter]     = useState<string>("all");
  const [patFilter, setPatFilter] = useState<string>("all");
  const [selected, setSelected] = useState<Entity | null>(null);

  useEffect(() => {
    fetch("/api/quantum-computing-disruption-engine")
      .then(r => r.json())
      .then(setData)
      .catch(console.error);
  }, []);

  if (!data) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-violet-400 text-lg animate-pulse">Initialisation du Moteur Disruption Quantique...</div>
    </div>
  );

  const { entities, summary } = data;
  const filtered = entities.filter(e =>
    (filter === "all" || e.quantum_risk === filter) &&
    (patFilter === "all" || e.quantum_pattern === patFilter)
  );

  const dists = [
    { title: "Niveau Risque",      counts: summary.risk_counts,     colors: RISK_COLORS   },
    { title: "Patterns Quantiques", counts: summary.pattern_counts,  colors: PAT_COLORS    },
    { title: "Sévérité",           counts: summary.severity_counts, colors: SEV_COLORS    },
    { title: "Actions",            counts: summary.action_counts,   colors: ACTION_COLORS },
  ] as Array<{ title: string; counts: Record<string, number>; colors: Record<string, string> }>;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {selected && <DetailModal entity={selected} onClose={() => setSelected(null)} />}

      <div>
        <h1 className="text-2xl font-bold text-violet-400">Disruption Quantique — Module 307</h1>
        <p className="text-violet-300/50 text-sm mt-1">Cryptographie · Préparation · Infrastructure · Géopolitique Quantique</p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {[
          ["Total Secteurs",                  summary.total,                                                  "text-violet-400"],
          ["En Crise Quantique",              summary.quantum_crisis_count,                                   "text-violet-500"],
          ["Requiert Intervention",           summary.quantum_intervention_count,                             "text-cyan-400"],
          ["Composite Moyen",                 summary.avg_quantum_composite.toFixed(1),                       "text-amber-400"],
          ["Index Disruption Quantique",      `${summary.avg_estimated_quantum_disruption_index.toFixed(2)}/10`, "text-violet-300"],
          ["Cryptographique Moyen",           summary.avg_cryptographic_score.toFixed(1),                    "text-cyan-500"],
        ].map(([l, v, c]) => (
          <div key={String(l)} className="bg-slate-900 border border-cyan-700/30 rounded-xl p-3 text-center">
            <div className={`text-xl font-bold ${c}`}>{v}</div>
            <div className="text-xs text-violet-300/40 mt-0.5 leading-tight">{l}</div>
          </div>
        ))}
      </div>

      {/* Gauge Rings */}
      <div className="bg-slate-900 border border-cyan-700/30 rounded-xl p-5">
        <div className="grid grid-cols-4 gap-4">
          <GaugeRing value={summary.avg_cryptographic_score}  label="Cryptographique"  color="#7c3aed" />
          <GaugeRing value={summary.avg_readiness_score}      label="Préparation"       color="#06b6d4" />
          <GaugeRing value={summary.avg_infrastructure_score} label="Infrastructure"    color="#f97316" />
          <GaugeRing value={summary.avg_geopolitical_score}   label="Géopolitique"      color="#f59e0b" />
        </div>
      </div>

      {/* Distribution Bars */}
      <div className="bg-slate-900 border border-cyan-700/30 rounded-xl p-5 grid grid-cols-1 md:grid-cols-2 gap-5">
        {dists.map(d => <DistBar key={d.title} {...d} />)}
      </div>

      {/* Filter Pills */}
      <div className="flex flex-wrap gap-2">
        {["all", "low", "moderate", "high", "critical"].map(r => (
          <button key={r} onClick={() => setFilter(r)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${filter === r ? "bg-violet-900 border-violet-700 text-white" : "bg-slate-900 border-cyan-700/30 text-violet-400/70 hover:text-white"}`}>
            {r}
          </button>
        ))}
        <span className="w-px h-5 self-center bg-cyan-700/30" />
        {["all", "none", "cryptographic_apocalypse", "quantum_surprise_attack", "infrastructure_quantum_shock", "financial_system_collapse", "talent_capability_gap"].map(p => (
          <button key={p} onClick={() => setPatFilter(p)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${patFilter === p ? "bg-violet-950 border-violet-800 text-white" : "bg-slate-900 border-cyan-700/30 text-violet-400/70 hover:text-white"}`}>
            {p.replace(/_/g, " ")}
          </button>
        ))}
      </div>

      {/* Entity Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {filtered.map(e => (
          <div key={e.entity_id} onClick={() => setSelected(e)}
            className="bg-slate-900 border border-cyan-700/30 rounded-xl p-4 cursor-pointer hover:border-violet-600 transition-colors">
            <div className="flex items-center justify-between mb-1">
              <span className="font-bold text-white">{e.entity_id}</span>
              <span className="text-xs text-violet-400/60">{e.region}</span>
            </div>
            <div className="text-xs text-slate-500 mb-2 capitalize">{e.sector.replace(/_/g, " ")}</div>
            <div className="flex gap-1 mb-3 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[e.quantum_risk as keyof typeof RISK_BADGE] || "bg-slate-700 text-slate-300"}`}>
                {e.quantum_risk}
              </span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[e.quantum_severity as keyof typeof SEV_BADGE] || "bg-slate-700 text-slate-300"}`}>
                {e.quantum_severity.replace(/_/g, " ")}
              </span>
            </div>
            <div className="text-2xl font-black text-white mb-1">{e.quantum_composite.toFixed(1)}</div>
            <div className="text-xs text-violet-400/60 mb-2 capitalize">{e.quantum_pattern.replace(/_/g, " ")}</div>
            <div className="text-xs text-cyan-400 font-medium mb-2">{e.recommended_action.replace(/_/g, " ")}</div>
            <div className="flex gap-1 flex-wrap">
              {e.is_quantum_crisis && (
                <span className="px-1.5 py-0.5 rounded bg-violet-950 text-violet-300 text-xs">CRISE</span>
              )}
              {e.requires_quantum_intervention && (
                <span className="px-1.5 py-0.5 rounded bg-cyan-950 text-cyan-400 text-xs">INTERVENTION</span>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
