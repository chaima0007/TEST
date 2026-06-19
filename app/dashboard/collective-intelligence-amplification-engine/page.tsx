"use client";
import { useEffect, useState } from "react";

type Entity = {
  entity_id: string;
  region: string;
  aggregation_method: string;
  ci_risk: string;
  ci_pattern: string;
  ci_severity: string;
  recommended_action: string;
  accuracy_score: number;
  diversity_score: number;
  aggregation_score: number;
  integrity_score: number;
  ci_composite: number;
  is_in_ci_crisis: boolean;
  requires_ci_intervention: boolean;
  ci_signal: string;
};

type Summary = {
  total: number;
  risk_counts: Record<string, number>;
  pattern_counts: Record<string, number>;
  severity_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_ci_composite: number;
  ci_crisis_count: number;
  ci_intervention_count: number;
  avg_accuracy_score: number;
  avg_diversity_score: number;
  avg_aggregation_score: number;
  avg_integrity_score: number;
  avg_estimated_ci_dysfunction_index: number;
};

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
      <span className="text-xs text-blue-300/70 text-center">{label}</span>
    </div>
  );
}

function DistBar({ title, counts, colors }: { title: string; counts: Record<string, number>; colors: Record<string, string> }) {
  const total = Object.values(counts).reduce((a, b) => a + b, 0) || 1;
  return (
    <div className="flex flex-col gap-1">
      <span className="text-xs text-blue-300/70 font-medium">{title}</span>
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
          <span key={k} className="text-xs text-blue-300/60">
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
  groupthink_cascade: "#7c3aed",
  wisdom_collapse: "#ef4444",
  information_cascade_failure: "#f97316",
  polarization_spiral: "#a855f7",
  manipulation_attack: "#dc2626",
};
const SEV_COLORS = {
  collective_wisdom_active: "#10b981",
  developing_distortion: "#f59e0b",
  high_dysfunction: "#f97316",
  collective_failure: "#7f1d1d",
};
const ACTION_COLORS = {
  no_action: "#10b981",
  ci_monitoring: "#06b6d4",
  diversity_amplification: "#f59e0b",
  integrity_firewall: "#f97316",
  ci_emergency_reset: "#ef4444",
};
const RISK_BADGE = {
  low: "bg-emerald-900 text-emerald-300",
  moderate: "bg-amber-900 text-amber-300",
  high: "bg-orange-900 text-orange-300",
  critical: "bg-red-950 text-red-400",
};
const SEV_BADGE = {
  collective_wisdom_active: "bg-emerald-900 text-emerald-300",
  developing_distortion: "bg-amber-900 text-amber-300",
  high_dysfunction: "bg-orange-900 text-orange-300",
  collective_failure: "bg-red-950 text-red-400",
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
        className="bg-slate-950 border border-violet-600/30 rounded-xl w-full max-w-lg p-6 shadow-2xl"
        onClick={e => e.stopPropagation()}
      >
        <div className="flex items-center justify-between mb-4">
          <div>
            <span className="text-lg font-bold text-white">{entity.entity_id}</span>
            <span className="ml-2 text-blue-400 text-xs">{entity.region}</span>
            <span className="ml-2 text-slate-500 text-xs">{entity.aggregation_method.replace(/_/g, " ")}</span>
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
                  ? "bg-violet-800 text-white"
                  : "bg-slate-900 text-slate-400 hover:text-white"
              }`}
            >
              {t.charAt(0).toUpperCase() + t.slice(1)}
            </button>
          ))}
        </div>

        {tab === "scores" && (
          <div className="grid grid-cols-2 gap-3 text-sm">
            {([
              ["Précision", entity.accuracy_score, "#60a5fa"],
              ["Diversité", entity.diversity_score, "#a78bfa"],
              ["Agrégation", entity.aggregation_score, "#818cf8"],
              ["Intégrité", entity.integrity_score, "#c084fc"],
            ] as [string, number, string][]).map(([l, v, c]) => (
              <div key={l} className="bg-slate-900 border border-violet-600/20 rounded-lg p-3">
                <div className="text-blue-300/60 text-xs mb-1">{l}</div>
                <div className="text-white font-bold text-lg">{Number(v).toFixed(1)}</div>
                <div className="h-1.5 rounded mt-1 bg-slate-800">
                  <div
                    className="h-1.5 rounded"
                    style={{ width: `${Math.min(Number(v), 100)}%`, background: c }}
                  />
                </div>
              </div>
            ))}
            <div className="col-span-2 bg-slate-900 border border-violet-600/20 rounded-lg p-3">
              <div className="text-blue-300/60 text-xs mb-1">Composite IC</div>
              <div className="text-white font-bold text-2xl">{entity.ci_composite.toFixed(1)}</div>
            </div>
          </div>
        )}

        {tab === "signal" && (
          <div className="bg-slate-900 border border-violet-600/20 rounded-lg p-4 text-sm text-slate-200 leading-relaxed">
            {entity.ci_signal}
            <div className="mt-3 flex gap-2 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[entity.ci_risk as keyof typeof RISK_BADGE] || "bg-slate-700 text-slate-300"}`}>
                {entity.ci_risk}
              </span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[entity.ci_severity as keyof typeof SEV_BADGE] || "bg-slate-700 text-slate-300"}`}>
                {entity.ci_severity.replace(/_/g, " ")}
              </span>
            </div>
          </div>
        )}

        {tab === "action" && (
          <div className="space-y-3 text-sm">
            <div className="bg-slate-900 border border-violet-600/20 rounded-lg p-3">
              <div className="text-blue-300/60 text-xs mb-1">Action Recommandée</div>
              <div className="text-white font-medium">{entity.recommended_action.replace(/_/g, " ")}</div>
            </div>
            <div className="bg-slate-900 border border-violet-600/20 rounded-lg p-3">
              <div className="text-blue-300/60 text-xs mb-1">Pattern IC</div>
              <div className="text-white font-medium">{entity.ci_pattern.replace(/_/g, " ")}</div>
            </div>
            <div className="flex gap-2">
              {entity.is_in_ci_crisis && (
                <span className="px-2 py-1 rounded bg-violet-950 text-violet-300 text-xs font-medium">
                  CRISE IC
                </span>
              )}
              {entity.requires_ci_intervention && (
                <span className="px-2 py-1 rounded bg-blue-950 text-blue-300 text-xs font-medium">
                  INTERVENTION REQ.
                </span>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function CollectiveIntelligenceDashboard() {
  const [data, setData] = useState<{ entities: Entity[]; summary: Summary } | null>(null);
  const [filter, setFilter] = useState<string>("all");
  const [patFilter, setPat] = useState<string>("all");
  const [selected, setSelected] = useState<Entity | null>(null);

  useEffect(() => {
    fetch("/api/collective-intelligence-amplification-engine")
      .then(r => r.json())
      .then(setData)
      .catch(console.error);
  }, []);

  if (!data) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-blue-400 text-lg animate-pulse">Initialisation du Moteur d&apos;Intelligence Collective...</div>
    </div>
  );

  const { entities, summary } = data;
  const filtered = entities.filter(e =>
    (filter === "all" || e.ci_risk === filter) &&
    (patFilter === "all" || e.ci_pattern === patFilter)
  );

  const dists = [
    { title: "Niveau Risque IC",        counts: summary.risk_counts,     colors: RISK_COLORS   },
    { title: "Pattern IC",              counts: summary.pattern_counts,  colors: PAT_COLORS    },
    { title: "Sévérité IC",             counts: summary.severity_counts, colors: SEV_COLORS    },
    { title: "Action Recommandée",      counts: summary.action_counts,   colors: ACTION_COLORS },
  ] as Array<{ title: string; counts: Record<string, number>; colors: Record<string, string> }>;

  const criticalCount = summary.risk_counts["critical"] || 0;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {selected && <DetailModal entity={selected} onClose={() => setSelected(null)} />}

      <div>
        <h1 className="text-2xl font-bold text-blue-400">
          Collective Intelligence Amplification &amp; Wisdom Aggregation Engine
        </h1>
        <p className="text-blue-300/50 text-sm mt-1">
          Précision Collective · Diversité · Agrégation · Intégrité Délibérative
        </p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {([
          ["Entités Analysées",             summary.total,                                    "text-blue-400"],
          ["Crises IC Critiques",           criticalCount,                                    "text-red-400"],
          ["Composite IC Moy.",             `${summary.avg_ci_composite.toFixed(1)}`,         "text-violet-400"],
          ["Indice Dysfonction IC",         `${summary.avg_estimated_ci_dysfunction_index}/10`, "text-amber-400"],
          ["Entités en Crise IC",           summary.ci_crisis_count,                          "text-red-400"],
          ["Interventions Requises",        summary.ci_intervention_count,                    "text-orange-400"],
        ] as [string, string | number, string][]).map(([l, v, c]) => (
          <div key={l} className="bg-slate-900 border border-violet-600/30 rounded-xl p-3 text-center">
            <div className={`text-xl font-bold ${c}`}>{v}</div>
            <div className="text-xs text-blue-300/40 mt-0.5 leading-tight">{l}</div>
          </div>
        ))}
      </div>

      {/* Gauge Rings */}
      <div className="bg-slate-900 border border-violet-600/30 rounded-xl p-5">
        <div className="grid grid-cols-4 gap-4">
          <GaugeRing value={summary.avg_accuracy_score}    label="Score Précision Collective" color="#60a5fa" />
          <GaugeRing value={summary.avg_diversity_score}   label="Score Diversité"            color="#a78bfa" />
          <GaugeRing value={summary.avg_aggregation_score} label="Score Agrégation"           color="#818cf8" />
          <GaugeRing value={summary.avg_integrity_score}   label="Score Intégrité"            color="#c084fc" />
        </div>
      </div>

      {/* Distribution Bars */}
      <div className="bg-slate-900 border border-violet-600/30 rounded-xl p-5 grid grid-cols-1 md:grid-cols-2 gap-5">
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
                ? "bg-violet-900 border-violet-700 text-white"
                : "bg-slate-900 border-violet-600/30 text-blue-400/70 hover:text-white"
            }`}
          >
            {r}
          </button>
        ))}
        <span className="w-px h-5 self-center bg-violet-600/30" />
        {["all", "none", "groupthink_cascade", "wisdom_collapse", "information_cascade_failure", "polarization_spiral", "manipulation_attack"].map(p => (
          <button
            key={p}
            onClick={() => setPat(p)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${
              patFilter === p
                ? "bg-violet-950 border-violet-700 text-white"
                : "bg-slate-900 border-violet-600/30 text-blue-400/70 hover:text-white"
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
            className="bg-slate-900 border border-violet-600/30 rounded-xl p-4 cursor-pointer hover:border-violet-500 transition-colors"
          >
            <div className="flex items-center justify-between mb-1">
              <span className="font-bold text-white">{e.entity_id}</span>
              <span className="text-xs text-blue-400/60">{e.region}</span>
            </div>
            <div className="text-xs text-slate-500 mb-2 capitalize">
              {e.aggregation_method.replace(/_/g, " ")}
            </div>
            <div className="flex gap-1 mb-3 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[e.ci_risk as keyof typeof RISK_BADGE] || "bg-slate-700 text-slate-300"}`}>
                {e.ci_risk}
              </span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[e.ci_severity as keyof typeof SEV_BADGE] || "bg-slate-700 text-slate-300"}`}>
                {e.ci_severity.replace(/_/g, " ")}
              </span>
            </div>
            <div className="text-2xl font-black text-white mb-1">{e.ci_composite.toFixed(1)}</div>
            <div className="text-xs text-blue-400/60 mb-2 capitalize">{e.ci_pattern.replace(/_/g, " ")}</div>
            <div className="text-xs text-violet-400 font-medium mb-2">
              Action: {e.recommended_action.replace(/_/g, " ")}
            </div>
            <div className="flex gap-1 flex-wrap">
              {e.is_in_ci_crisis && (
                <span className="px-1.5 py-0.5 rounded bg-violet-950 text-violet-300 text-xs">CRISE IC</span>
              )}
              {e.requires_ci_intervention && (
                <span className="px-1.5 py-0.5 rounded bg-blue-950 text-blue-300 text-xs">INTERVENTION</span>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
