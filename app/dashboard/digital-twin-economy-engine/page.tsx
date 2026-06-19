"use client";
import { useEffect, useState } from "react";

type Entity = {
  entity_id: string;
  region: string;
  twin_category: string;
  twin_risk: string;
  twin_pattern: string;
  twin_severity: string;
  recommended_action: string;
  fidelity_score: number;
  sync_score: number;
  security_score: number;
  governance_score: number;
  twin_composite: number;
  is_twin_crisis: boolean;
  requires_twin_intervention: boolean;
  twin_signal: string;
};

type Summary = {
  total: number;
  risk_counts: Record<string, number>;
  pattern_counts: Record<string, number>;
  severity_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_twin_composite: number;
  twin_crisis_count: number;
  twin_intervention_count: number;
  avg_fidelity_score: number;
  avg_sync_score: number;
  avg_security_score: number;
  avg_governance_score: number;
  avg_estimated_twin_risk_index: number;
};

function GaugeRing({ value, label, color }: { value: number; label: string; color: string }) {
  const r = 36;
  const circ = 2 * Math.PI * r;
  const fill = circ * (1 - value / 100);
  return (
    <div className="flex flex-col items-center gap-1">
      <svg width="88" height="88" viewBox="0 0 88 88">
        <circle cx="44" cy="44" r={r} fill="none" stroke="#0c1a2e" strokeWidth="8" />
        <circle
          cx="44" cy="44" r={r} fill="none" stroke={color} strokeWidth="8"
          strokeDasharray={circ} strokeDashoffset={fill}
          strokeLinecap="round" transform="rotate(-90 44 44)"
        />
        <text x="44" y="49" textAnchor="middle" fill="white" fontSize="13" fontWeight="bold">
          {Math.round(value)}
        </text>
      </svg>
      <span className="text-xs text-cyan-300/70 text-center">{label}</span>
    </div>
  );
}

function DistBar({ title, counts, colors }: { title: string; counts: Record<string, number>; colors: Record<string, string> }) {
  const total = Object.values(counts).reduce((a, b) => a + b, 0) || 1;
  return (
    <div className="flex flex-col gap-1">
      <span className="text-xs text-cyan-300/70 font-medium">{title}</span>
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
          <span key={k} className="text-xs text-cyan-300/60">
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
  twin_divergence_crisis: "#7f1d1d",
  digital_sovereignty_breach: "#7c3aed",
  adversarial_twin_attack: "#dc2626",
  predictive_failure_cascade: "#f97316",
  lock_in_monopoly: "#a855f7",
};
const SEV_COLORS: Record<string, string> = {
  twin_stable: "#10b981",
  twin_instability: "#f59e0b",
  critical_divergence: "#f97316",
  twin_emergency: "#ef4444",
};
const ACT_COLORS: Record<string, string> = {
  no_action: "#10b981",
  sync_monitoring: "#06b6d4",
  twin_recalibration: "#f59e0b",
  security_lockdown: "#f97316",
  twin_emergency_shutdown: "#ef4444",
};
const RISK_BADGE: Record<string, string> = {
  low: "bg-emerald-900 text-emerald-300",
  moderate: "bg-amber-900 text-amber-300",
  high: "bg-orange-900 text-orange-300",
  critical: "bg-red-950 text-red-400",
};
const SEV_BADGE: Record<string, string> = {
  twin_stable: "bg-emerald-900 text-emerald-300",
  twin_instability: "bg-amber-900 text-amber-300",
  critical_divergence: "bg-orange-900 text-orange-300",
  twin_emergency: "bg-red-950 text-red-400",
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
        className="bg-slate-950 border border-violet-700/30 rounded-xl w-full max-w-lg p-6 shadow-2xl"
        onClick={e => e.stopPropagation()}
      >
        <div className="flex items-center justify-between mb-4">
          <div>
            <span className="text-lg font-bold text-white">{entity.entity_id}</span>
            <span className="ml-2 text-cyan-400 text-xs">{entity.region}</span>
            <span className="ml-2 text-slate-500 text-xs">{entity.twin_category.replace(/_/g, " ")}</span>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl leading-none">✕</button>
        </div>

        <div className="flex gap-2 mb-4">
          {(["scores", "signal", "action"] as const).map(t => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`px-3 py-1 rounded text-xs font-medium transition-colors ${
                tab === t
                  ? "bg-cyan-900 text-white"
                  : "bg-slate-900 text-slate-400 hover:text-white"
              }`}
            >
              {t === "scores" ? "Scores" : t === "signal" ? "Signal" : "Action"}
            </button>
          ))}
        </div>

        {tab === "scores" && (
          <div className="grid grid-cols-2 gap-3 text-sm">
            {([
              ["Fidélité",        entity.fidelity_score,   "#06b6d4"],
              ["Synchronisation", entity.sync_score,        "#a855f7"],
              ["Sécurité",        entity.security_score,   "#ef4444"],
              ["Gouvernance",     entity.governance_score, "#f59e0b"],
            ] as [string, number, string][]).map(([l, v, c]) => (
              <div key={l} className="bg-slate-900 border border-violet-700/20 rounded-lg p-3">
                <div className="text-cyan-300/60 text-xs mb-1">{l}</div>
                <div className="text-white font-bold text-lg">{Number(v).toFixed(1)}</div>
                <div className="h-1.5 rounded mt-1 bg-slate-800">
                  <div className="h-1.5 rounded" style={{ width: `${Math.min(Number(v), 100)}%`, background: c }} />
                </div>
              </div>
            ))}
            <div className="col-span-2 bg-slate-900 border border-violet-700/20 rounded-lg p-3">
              <div className="text-cyan-300/60 text-xs mb-1">Composite Jumeau Numérique</div>
              <div className="text-white font-bold text-2xl">{entity.twin_composite.toFixed(1)}</div>
            </div>
          </div>
        )}

        {tab === "signal" && (
          <div className="bg-slate-900 border border-violet-700/20 rounded-lg p-4 text-sm text-slate-200 leading-relaxed">
            {entity.twin_signal}
            <div className="mt-3 flex gap-2 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[entity.twin_risk] || "bg-slate-700 text-slate-300"}`}>
                {entity.twin_risk}
              </span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[entity.twin_severity] || "bg-slate-700 text-slate-300"}`}>
                {entity.twin_severity.replace(/_/g, " ")}
              </span>
            </div>
          </div>
        )}

        {tab === "action" && (
          <div className="space-y-3 text-sm">
            <div className="bg-slate-900 border border-violet-700/20 rounded-lg p-3">
              <div className="text-cyan-300/60 text-xs mb-1">Action Recommandée</div>
              <div className="text-white font-medium">{entity.recommended_action.replace(/_/g, " ")}</div>
            </div>
            <div className="bg-slate-900 border border-violet-700/20 rounded-lg p-3">
              <div className="text-cyan-300/60 text-xs mb-1">Pattern Détecté</div>
              <div className="text-white font-medium capitalize">{entity.twin_pattern.replace(/_/g, " ")}</div>
            </div>
            <div className="flex gap-2">
              {entity.is_twin_crisis && (
                <span className="px-2 py-1 rounded bg-red-950 text-red-400 text-xs font-medium">CRISE JUMEAU</span>
              )}
              {entity.requires_twin_intervention && (
                <span className="px-2 py-1 rounded bg-violet-950 text-violet-400 text-xs font-medium">INTERVENTION REQ.</span>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function DigitalTwinEconomyDashboard() {
  const [data, setData]         = useState<{ entities: Entity[]; summary: Summary } | null>(null);
  const [filter, setFilter]     = useState<string>("all");
  const [patFilter, setPat]     = useState<string>("all");
  const [selected, setSelected] = useState<Entity | null>(null);

  useEffect(() => {
    fetch("/api/digital-twin-economy-engine")
      .then(r => r.json())
      .then(setData)
      .catch(console.error);
  }, []);

  if (!data) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-cyan-400 text-lg animate-pulse">Initialisation du Moteur Économie Jumeaux Numériques...</div>
    </div>
  );

  const { entities, summary } = data;
  const filtered = entities.filter(e =>
    (filter === "all" || e.twin_risk === filter) &&
    (patFilter === "all" || e.twin_pattern === patFilter)
  );

  const dists = [
    { title: "Niveau Risque Jumeau",    counts: summary.risk_counts,     colors: RISK_COLORS },
    { title: "Pattern Détecté",         counts: summary.pattern_counts,  colors: PAT_COLORS  },
    { title: "Sévérité Divergence",     counts: summary.severity_counts, colors: SEV_COLORS  },
    { title: "Action Déclenchée",       counts: summary.action_counts,   colors: ACT_COLORS  },
  ] as Array<{ title: string; counts: Record<string, number>; colors: Record<string, string> }>;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {selected && <DetailModal entity={selected} onClose={() => setSelected(null)} />}

      <div>
        <h1 className="text-2xl font-bold text-cyan-400">
          Économie des Jumeaux Numériques — Module 306
        </h1>
        <p className="text-cyan-300/50 text-sm mt-1">
          Fidélité · Synchronisation · Sécurité · Gouvernance
        </p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {([
          ["Total Jumeaux",          summary.total,                                            "text-cyan-400"],
          ["En Crise Jumeau",        summary.twin_crisis_count,                                "text-red-400"],
          ["Requiert Intervention",  summary.twin_intervention_count,                          "text-violet-400"],
          ["Composite Moyen",        summary.avg_twin_composite.toFixed(1),                    "text-cyan-300"],
          ["Index Risque Jumeau",    summary.avg_estimated_twin_risk_index.toFixed(2),         "text-amber-400"],
          ["Fidélité Moyenne",       summary.avg_fidelity_score.toFixed(1),                    "text-orange-400"],
        ] as [string, string | number, string][]).map(([l, v, c]) => (
          <div key={String(l)} className="bg-slate-900 border border-violet-700/30 rounded-xl p-3 text-center">
            <div className={`text-xl font-bold ${c}`}>{v}</div>
            <div className="text-xs text-cyan-300/40 mt-0.5 leading-tight">{l}</div>
          </div>
        ))}
      </div>

      {/* Gauge Rings */}
      <div className="bg-slate-900 border border-violet-700/30 rounded-xl p-5">
        <div className="grid grid-cols-4 gap-4">
          <GaugeRing value={summary.avg_fidelity_score}    label="Fidélité"        color="#06b6d4" />
          <GaugeRing value={summary.avg_sync_score}        label="Synchronisation" color="#a855f7" />
          <GaugeRing value={summary.avg_security_score}    label="Sécurité"        color="#ef4444" />
          <GaugeRing value={summary.avg_governance_score}  label="Gouvernance"     color="#f59e0b" />
        </div>
      </div>

      {/* Distribution Bars */}
      <div className="bg-slate-900 border border-violet-700/30 rounded-xl p-5 grid grid-cols-1 md:grid-cols-2 gap-5">
        {dists.map(d => <DistBar key={d.title} {...d} />)}
      </div>

      {/* Filter Pills */}
      <div className="flex flex-wrap gap-2">
        {["all", "low", "moderate", "high", "critical"].map(r => (
          <button
            key={r}
            onClick={() => setFilter(r)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${
              filter === r
                ? "bg-cyan-900 border-cyan-700 text-white"
                : "bg-slate-900 border-violet-700/30 text-cyan-400/70 hover:text-white"
            }`}
          >
            {r}
          </button>
        ))}
        <span className="w-px h-5 self-center bg-violet-700/30" />
        {["all", "none", "twin_divergence_crisis", "digital_sovereignty_breach", "adversarial_twin_attack", "predictive_failure_cascade", "lock_in_monopoly"].map(p => (
          <button
            key={p}
            onClick={() => setPat(p)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${
              patFilter === p
                ? "bg-violet-950 border-violet-700 text-white"
                : "bg-slate-900 border-violet-700/30 text-cyan-400/70 hover:text-white"
            }`}
          >
            {p.replace(/_/g, " ")}
          </button>
        ))}
      </div>

      {/* Entity Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {filtered.map(e => (
          <div
            key={e.entity_id}
            onClick={() => setSelected(e)}
            className="bg-slate-900 border border-violet-700/30 rounded-xl p-4 cursor-pointer hover:border-cyan-500 transition-colors"
          >
            <div className="flex items-center justify-between mb-1">
              <span className="font-bold text-white">{e.entity_id}</span>
              <span className="text-xs text-cyan-400/60">{e.region}</span>
            </div>
            <div className="text-xs text-slate-500 mb-2 capitalize">{e.twin_category.replace(/_/g, " ")}</div>
            <div className="flex gap-1 mb-3 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[e.twin_risk] || "bg-slate-700 text-slate-300"}`}>
                {e.twin_risk}
              </span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[e.twin_severity] || "bg-slate-700 text-slate-300"}`}>
                {e.twin_severity.replace(/_/g, " ")}
              </span>
            </div>
            <div className="text-2xl font-black text-white mb-1">{e.twin_composite.toFixed(1)}</div>
            <div className="text-xs text-cyan-400/60 mb-2 capitalize">{e.twin_pattern.replace(/_/g, " ")}</div>
            <div className="text-xs text-violet-400 font-medium mb-2">
              Fidélité: {e.fidelity_score.toFixed(1)}
            </div>
            <div className="flex gap-1 flex-wrap">
              {e.is_twin_crisis && (
                <span className="px-1.5 py-0.5 rounded bg-red-950 text-red-400 text-xs">CRISE</span>
              )}
              {e.requires_twin_intervention && (
                <span className="px-1.5 py-0.5 rounded bg-violet-950 text-violet-400 text-xs">INTERVENTION</span>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
