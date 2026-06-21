"use client";
import { useEffect, useState } from "react";

type Entity = {
  id: string;
  region: string;
  contagion_type: string;
  contagion_risk: string;
  contagion_pattern: string;
  contagion_severity: string;
  recommended_action: string;
  spread_score: number;
  amplification_score: number;
  resilience_score: number;
  polarization_score: number;
  contagion_composite: number;
  is_in_contagion_crisis: boolean;
  requires_contagion_intervention: boolean;
  contagion_signal: string;
};

type Summary = {
  total: number;
  risk_counts: Record<string, number>;
  pattern_counts: Record<string, number>;
  severity_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_contagion_composite: number;
  contagion_crisis_count: number;
  contagion_intervention_count: number;
  avg_spread_score: number;
  avg_amplification_score: number;
  avg_resilience_score: number;
  avg_polarization_score: number;
  avg_estimated_contagion_index: number;
};

function GaugeRing({ value, label, color }: { value: number; label: string; color: string }) {
  const r = 36;
  const circ = 2 * Math.PI * r;
  const fill = circ * (1 - value / 100);
  return (
    <div className="flex flex-col items-center gap-1">
      <svg width="88" height="88" viewBox="0 0 88 88">
        <circle cx="44" cy="44" r={r} fill="none" stroke="#1a0505" strokeWidth="8" />
        <circle
          cx="44" cy="44" r={r} fill="none" stroke={color} strokeWidth="8"
          strokeDasharray={circ} strokeDashoffset={fill}
          strokeLinecap="round" transform="rotate(-90 44 44)"
        />
        <text x="44" y="49" textAnchor="middle" fill="white" fontSize="13" fontWeight="bold">
          {Math.round(value)}
        </text>
      </svg>
      <span className="text-xs text-red-300/70 text-center">{label}</span>
    </div>
  );
}

function DistBar({ title, counts, colors }: { title: string; counts: Record<string, number>; colors: Record<string, string> }) {
  const total = Object.values(counts).reduce((a, b) => a + b, 0) || 1;
  return (
    <div className="flex flex-col gap-1">
      <span className="text-xs text-red-300/70 font-medium">{title}</span>
      <div className="flex h-3 rounded overflow-hidden gap-px">
        {Object.entries(counts).map(([k, v]) => (
          <div key={k} style={{ width: `${(v / total) * 100}%`, background: colors[k] || "#475569" }} title={`${k}: ${v}`} />
        ))}
      </div>
      <div className="flex flex-wrap gap-x-3 gap-y-0.5">
        {Object.entries(counts).map(([k, v]) => (
          <span key={k} className="text-xs text-red-300/60">
            <span style={{ color: colors[k] || "#94a3b8" }}>■</span> {k} {v}
          </span>
        ))}
      </div>
    </div>
  );
}

const RISK_COLORS = { low: "#10b981", moderate: "#f59e0b", high: "#f97316", critical: "#ef4444" };
const PAT_COLORS: Record<string, string> = {
  none: "#10b981",
  panic_epidemic: "#7f1d1d",
  euphoria_mania: "#a855f7",
  rage_wildfire: "#ef4444",
  anxiety_tsunami: "#f97316",
  polarization_spiral: "#dc2626",
};
const SEV_COLORS: Record<string, string> = {
  emotional_equilibrium: "#10b981",
  contagion_developing: "#f59e0b",
  high_contagion: "#f97316",
  contagion_emergency: "#7f1d1d",
};
const ACTION_COLORS: Record<string, string> = {
  no_action: "#10b981",
  contagion_monitoring: "#06b6d4",
  rage_de_escalation: "#f59e0b",
  emotional_containment: "#f97316",
  contagion_circuit_breaker: "#7f1d1d",
};
const RISK_BADGE: Record<string, string> = {
  low: "bg-emerald-900 text-emerald-300",
  moderate: "bg-amber-900 text-amber-300",
  high: "bg-orange-900 text-orange-300",
  critical: "bg-red-950 text-red-400",
};
const SEV_BADGE: Record<string, string> = {
  emotional_equilibrium: "bg-emerald-900 text-emerald-300",
  contagion_developing: "bg-amber-900 text-amber-300",
  high_contagion: "bg-orange-900 text-orange-300",
  contagion_emergency: "bg-red-950 text-red-400",
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
      <div
        className="bg-slate-950 border border-amber-600/30 rounded-xl w-full max-w-lg p-6 shadow-2xl"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="flex items-center justify-between mb-4">
          <div>
            <span className="text-lg font-bold text-white">{entity.id}</span>
            <span className="ml-2 text-red-400 text-xs">{entity.region}</span>
            <span className="ml-2 text-slate-500 text-xs">{entity.contagion_type.replace(/_/g, " ")}</span>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl leading-none">✕</button>
        </div>

        <div className="flex gap-2 mb-4">
          {(["scores", "signal", "action"] as const).map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`px-3 py-1 rounded text-xs font-medium transition-colors ${
                tab === t ? "bg-red-900 text-white" : "bg-slate-900 text-slate-400 hover:text-white"
              }`}
            >
              {t.charAt(0).toUpperCase() + t.slice(1)}
            </button>
          ))}
        </div>

        {tab === "scores" && (
          <div className="grid grid-cols-2 gap-3 text-sm">
            {[
              ["Propagation",    entity.spread_score,        "#ef4444"],
              ["Amplification",  entity.amplification_score, "#a855f7"],
              ["Résilience",     entity.resilience_score,    "#f97316"],
              ["Polarisation",   entity.polarization_score,  "#06b6d4"],
            ].map(([l, v, c]) => (
              <div key={String(l)} className="bg-slate-900 border border-amber-600/20 rounded-lg p-3">
                <div className="text-red-300/60 text-xs mb-1">{String(l)}</div>
                <div className="text-white font-bold text-lg">{Number(v).toFixed(1)}</div>
                <div className="h-1.5 rounded mt-1 bg-slate-800">
                  <div className="h-1.5 rounded" style={{ width: `${Math.min(Number(v), 100)}%`, background: String(c) }} />
                </div>
              </div>
            ))}
            <div className="col-span-2 bg-slate-900 border border-amber-600/20 rounded-lg p-3">
              <div className="text-red-300/60 text-xs mb-1">Composite Contagion</div>
              <div className="text-white font-bold text-2xl">{entity.contagion_composite.toFixed(1)}</div>
            </div>
          </div>
        )}

        {tab === "signal" && (
          <div className="bg-slate-900 border border-amber-600/20 rounded-lg p-4 text-sm text-slate-200 leading-relaxed">
            {entity.contagion_signal}
            <div className="mt-3 flex gap-2 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[entity.contagion_risk] || "bg-slate-700 text-slate-300"}`}>
                {entity.contagion_risk}
              </span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[entity.contagion_severity] || "bg-slate-700 text-slate-300"}`}>
                {entity.contagion_severity.replace(/_/g, " ")}
              </span>
            </div>
          </div>
        )}

        {tab === "action" && (
          <div className="space-y-3 text-sm">
            <div className="bg-slate-900 border border-amber-600/20 rounded-lg p-3">
              <div className="text-red-300/60 text-xs mb-1">Action Recommandée</div>
              <div className="text-white font-medium">{entity.recommended_action.replace(/_/g, " ")}</div>
            </div>
            <div className="bg-slate-900 border border-amber-600/20 rounded-lg p-3">
              <div className="text-red-300/60 text-xs mb-1">Pattern Contagion</div>
              <div className="text-white font-medium">{entity.contagion_pattern.replace(/_/g, " ")}</div>
            </div>
            <div className="flex gap-2 flex-wrap">
              {entity.is_in_contagion_crisis && (
                <span className="px-2 py-1 rounded bg-red-950 text-red-400 text-xs font-medium">CRISE CONTAGION</span>
              )}
              {entity.requires_contagion_intervention && (
                <span className="px-2 py-1 rounded bg-orange-950 text-orange-400 text-xs font-medium">INTERVENTION REQ.</span>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function EmotionalContagionDashboard() {
  const [data, setData]         = useState<{ entities: Entity[]; summary: Summary } | null>(null);
  const [filter, setFilter]     = useState<string>("all");
  const [patFilter, setPatFilter] = useState<string>("all");
  const [selected, setSelected] = useState<Entity | null>(null);

  useEffect(() => {
    fetch("/api/emotional-contagion-engine")
      .then((r) => r.json())
      .then(setData)
      .catch(console.error);
  }, []);

  if (!data) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-red-400 text-lg animate-pulse">Initialisation du Moteur de Contagion Émotionnelle...</div>
    </div>
  );

  const { entities, summary } = data;
  const filtered = entities.filter((e) =>
    (filter === "all" || e.contagion_risk === filter) &&
    (patFilter === "all" || e.contagion_pattern === patFilter)
  );

  const dists = [
    { title: "Niveau de Risque",       counts: summary.risk_counts,     colors: RISK_COLORS  },
    { title: "Pattern Contagion",      counts: summary.pattern_counts,  colors: PAT_COLORS   },
    { title: "Sévérité Épidémique",    counts: summary.severity_counts, colors: SEV_COLORS   },
    { title: "Action Déclenchée",      counts: summary.action_counts,   colors: ACTION_COLORS },
  ] as Array<{ title: string; counts: Record<string, number>; colors: Record<string, string> }>;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {selected && <DetailModal entity={selected} onClose={() => setSelected(null)} />}

      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-red-400">
          Emotional Contagion &amp; Social Epidemic Intelligence Engine
        </h1>
        <p className="text-red-300/50 text-sm mt-1">
          Propagation · Amplification Médiatique · Résilience Émotionnelle · Dynamiques de Contagion Collectives
        </p>
      </div>

      {/* KPI Cards — 6 cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {[
          ["Entités Analysées",              summary.total,                                     "text-red-400"],
          ["Crises Contagion",               summary.contagion_crisis_count,                    "text-red-500"],
          ["Interventions Requises",         summary.contagion_intervention_count,              "text-amber-400"],
          ["Composite Moyen",                `${summary.avg_contagion_composite.toFixed(1)}`,   "text-orange-400"],
          ["Indice Contagion Moy.",          `${summary.avg_estimated_contagion_index.toFixed(2)}/10`, "text-red-400"],
          ["Score Propagation Moy.",         `${summary.avg_spread_score.toFixed(1)}`,          "text-red-500"],
        ].map(([l, v, c]) => (
          <div key={String(l)} className="bg-slate-900 border border-amber-600/30 rounded-xl p-3 text-center">
            <div className={`text-xl font-bold ${c}`}>{v}</div>
            <div className="text-xs text-red-300/40 mt-0.5 leading-tight">{l}</div>
          </div>
        ))}
      </div>

      {/* Gauge Rings — 4 */}
      <div className="bg-slate-900 border border-amber-600/30 rounded-xl p-5">
        <div className="grid grid-cols-4 gap-4">
          <GaugeRing value={summary.avg_spread_score}        label="Propagation Émotionnelle"    color="#ef4444" />
          <GaugeRing value={summary.avg_amplification_score} label="Amplification Médiatique"    color="#a855f7" />
          <GaugeRing value={summary.avg_resilience_score}    label="Vulnérabilité Résilience"    color="#f97316" />
          <GaugeRing value={summary.avg_polarization_score}  label="Polarisation Collective"     color="#f59e0b" />
        </div>
      </div>

      {/* Distribution Bars — 4 */}
      <div className="bg-slate-900 border border-amber-600/30 rounded-xl p-5 grid grid-cols-1 md:grid-cols-2 gap-5">
        {dists.map((d) => <DistBar key={d.title} {...d} />)}
      </div>

      {/* Filter Pills */}
      <div className="flex flex-wrap gap-2">
        {["all", "low", "moderate", "high", "critical"].map((r) => (
          <button
            key={r}
            onClick={() => setFilter(r)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${
              filter === r
                ? "bg-red-900 border-red-700 text-white"
                : "bg-slate-900 border-amber-600/30 text-red-400/70 hover:text-white"
            }`}
          >
            {r}
          </button>
        ))}
        <span className="w-px h-5 self-center bg-amber-600/30" />
        {["all", "none", "panic_epidemic", "euphoria_mania", "rage_wildfire", "anxiety_tsunami", "polarization_spiral"].map((p) => (
          <button
            key={p}
            onClick={() => setPatFilter(p)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${
              patFilter === p
                ? "bg-red-950 border-red-800 text-white"
                : "bg-slate-900 border-amber-600/30 text-red-400/70 hover:text-white"
            }`}
          >
            {p.replace(/_/g, " ")}
          </button>
        ))}
      </div>

      {/* Entity Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {filtered.map((e) => (
          <div
            key={e.id}
            onClick={() => setSelected(e)}
            className="bg-slate-900 border border-amber-600/30 rounded-xl p-4 cursor-pointer hover:border-red-600 transition-colors"
          >
            <div className="flex items-center justify-between mb-1">
              <span className="font-bold text-white">{e.id}</span>
              <span className="text-xs text-red-400/60">{e.region}</span>
            </div>
            <div className="text-xs text-slate-500 mb-2 capitalize">{e.contagion_type.replace(/_/g, " ")}</div>
            <div className="flex gap-1 mb-3 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[e.contagion_risk] || "bg-slate-700 text-slate-300"}`}>
                {e.contagion_risk}
              </span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[e.contagion_severity] || "bg-slate-700 text-slate-300"}`}>
                {e.contagion_severity.replace(/_/g, " ")}
              </span>
            </div>
            <div className="text-2xl font-black text-white mb-1">{e.contagion_composite.toFixed(1)}</div>
            <div className="text-xs text-red-400/60 mb-2 capitalize">{e.contagion_pattern.replace(/_/g, " ")}</div>
            <div className="text-xs text-amber-400 font-medium mb-2">{e.recommended_action.replace(/_/g, " ")}</div>
            <div className="flex gap-1 flex-wrap">
              {e.is_in_contagion_crisis && (
                <span className="px-1.5 py-0.5 rounded bg-red-950 text-red-400 text-xs">CRISE</span>
              )}
              {e.requires_contagion_intervention && (
                <span className="px-1.5 py-0.5 rounded bg-orange-950 text-orange-400 text-xs">INTERVENTION</span>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
