"use client";
import { useEffect, useState } from "react";

type Entity = {
  entity_id: string;
  region: string;
  platform_domain: string;
  feudal_risk: string;
  feudal_pattern: string;
  feudal_severity: string;
  recommended_action: string;
  capture_score: number;
  rent_score: number;
  dependency_score: number;
  sovereignty_score: number;
  feudal_composite: number;
  is_feudal_crisis: boolean;
  requires_feudal_intervention: boolean;
  feudal_signal: string;
};

type Summary = {
  total: number;
  risk_counts: Record<string, number>;
  pattern_counts: Record<string, number>;
  severity_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_feudal_composite: number;
  feudal_crisis_count: number;
  feudal_intervention_count: number;
  avg_capture_score: number;
  avg_rent_score: number;
  avg_dependency_score: number;
  avg_sovereignty_score: number;
  avg_estimated_feudalization_index: number;
};

function GaugeRing({ value, label, color }: { value: number; label: string; color: string }) {
  const r = 36;
  const circ = 2 * Math.PI * r;
  const fill = circ * (1 - value / 100);
  return (
    <div className="flex flex-col items-center gap-1">
      <svg width="88" height="88" viewBox="0 0 88 88">
        <circle cx="44" cy="44" r={r} fill="none" stroke="#0c0a1a" strokeWidth="8" />
        <circle
          cx="44" cy="44" r={r} fill="none" stroke={color} strokeWidth="8"
          strokeDasharray={circ} strokeDashoffset={fill}
          strokeLinecap="round" transform="rotate(-90 44 44)"
        />
        <text x="44" y="49" textAnchor="middle" fill="white" fontSize="13" fontWeight="bold">
          {Math.round(value)}
        </text>
      </svg>
      <span className="text-xs text-purple-300/70 text-center">{label}</span>
    </div>
  );
}

function DistBar({ title, counts, colors }: { title: string; counts: Record<string, number>; colors: Record<string, string> }) {
  const total = Object.values(counts).reduce((a, b) => a + b, 0) || 1;
  return (
    <div className="flex flex-col gap-1">
      <span className="text-xs text-purple-300/70 font-medium">{title}</span>
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
          <span key={k} className="text-xs text-purple-300/60">
            <span style={{ color: colors[k] || "#94a3b8" }}>■</span> {k.replace(/_/g, " ")} {v}
          </span>
        ))}
      </div>
    </div>
  );
}

const RISK_COLORS = { low: "#10b981", moderate: "#f59e0b", high: "#a855f7", critical: "#ef4444" };
const PAT_COLORS: Record<string, string> = {
  none: "#10b981",
  monopoly_feudalism: "#7c3aed",
  data_serfdom: "#9333ea",
  cloud_colonialism: "#06b6d4",
  digital_enclosure: "#f97316",
  worker_feudalization: "#eab308",
};
const SEV_COLORS: Record<string, string> = {
  digital_commons_healthy: "#10b981",
  feudal_dynamics_emerging: "#f59e0b",
  high_feudalization: "#a855f7",
  feudal_emergency: "#ef4444",
};
const ACT_COLORS: Record<string, string> = {
  no_action: "#10b981",
  market_monitoring: "#06b6d4",
  platform_regulation: "#a855f7",
  sovereign_cloud_program: "#f59e0b",
  antitrust_emergency_action: "#ef4444",
};
const RISK_BADGE: Record<string, string> = {
  low: "bg-emerald-900 text-emerald-300",
  moderate: "bg-amber-900 text-amber-300",
  high: "bg-purple-900 text-purple-300",
  critical: "bg-red-950 text-red-400",
};
const SEV_BADGE: Record<string, string> = {
  digital_commons_healthy: "bg-emerald-900 text-emerald-300",
  feudal_dynamics_emerging: "bg-amber-900 text-amber-300",
  high_feudalization: "bg-purple-900 text-purple-300",
  feudal_emergency: "bg-red-950 text-red-400",
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
        className="bg-slate-950 border border-yellow-700/30 rounded-xl w-full max-w-lg p-6 shadow-2xl"
        onClick={e => e.stopPropagation()}
      >
        <div className="flex items-center justify-between mb-4">
          <div>
            <span className="text-lg font-bold text-white">{entity.entity_id}</span>
            <span className="ml-2 text-purple-400 text-xs">{entity.region}</span>
            <span className="ml-2 text-slate-500 text-xs">{entity.platform_domain.replace(/_/g, " ")}</span>
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
                  ? "bg-purple-900 text-white"
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
              ["Capture",      entity.capture_score,     "#7c3aed"],
              ["Rente",        entity.rent_score,        "#eab308"],
              ["Dépendance",   entity.dependency_score,  "#a855f7"],
              ["Souveraineté", entity.sovereignty_score, "#06b6d4"],
            ] as [string, number, string][]).map(([l, v, c]) => (
              <div key={l} className="bg-slate-900 border border-yellow-700/20 rounded-lg p-3">
                <div className="text-purple-300/60 text-xs mb-1">{l}</div>
                <div className="text-white font-bold text-lg">{Number(v).toFixed(1)}</div>
                <div className="h-1.5 rounded mt-1 bg-slate-800">
                  <div className="h-1.5 rounded" style={{ width: `${Math.min(Number(v), 100)}%`, background: c }} />
                </div>
              </div>
            ))}
            <div className="col-span-2 bg-slate-900 border border-yellow-700/20 rounded-lg p-3">
              <div className="text-purple-300/60 text-xs mb-1">Composite Féodalisme Numérique</div>
              <div className="text-white font-bold text-2xl">{entity.feudal_composite.toFixed(1)}</div>
            </div>
          </div>
        )}

        {tab === "signal" && (
          <div className="bg-slate-900 border border-yellow-700/20 rounded-lg p-4 text-sm text-slate-200 leading-relaxed">
            {entity.feudal_signal}
            <div className="mt-3 flex gap-2 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[entity.feudal_risk] || "bg-slate-700 text-slate-300"}`}>
                {entity.feudal_risk}
              </span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[entity.feudal_severity] || "bg-slate-700 text-slate-300"}`}>
                {entity.feudal_severity.replace(/_/g, " ")}
              </span>
            </div>
          </div>
        )}

        {tab === "action" && (
          <div className="space-y-3 text-sm">
            <div className="bg-slate-900 border border-yellow-700/20 rounded-lg p-3">
              <div className="text-purple-300/60 text-xs mb-1">Action Recommandée</div>
              <div className="text-white font-medium">{entity.recommended_action.replace(/_/g, " ")}</div>
            </div>
            <div className="bg-slate-900 border border-yellow-700/20 rounded-lg p-3">
              <div className="text-purple-300/60 text-xs mb-1">Pattern Féodal Détecté</div>
              <div className="text-white font-medium capitalize">{entity.feudal_pattern.replace(/_/g, " ")}</div>
            </div>
            <div className="flex gap-2 flex-wrap">
              {entity.is_feudal_crisis && (
                <span className="px-2 py-1 rounded bg-red-950 text-red-400 text-xs font-medium">CRISE FÉODALE</span>
              )}
              {entity.requires_feudal_intervention && (
                <span className="px-2 py-1 rounded bg-purple-950 text-purple-400 text-xs font-medium">INTERVENTION REQ.</span>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function TechnoFeudalismDashboard() {
  const [data, setData]         = useState<{ entities: Entity[]; summary: Summary } | null>(null);
  const [filter, setFilter]     = useState<string>("all");
  const [patFilter, setPat]     = useState<string>("all");
  const [selected, setSelected] = useState<Entity | null>(null);

  useEffect(() => {
    fetch("/api/techno-feudalism-engine")
      .then(r => r.json())
      .then(setData)
      .catch(console.error);
  }, []);

  if (!data) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-purple-400 text-lg animate-pulse">Initialisation du Moteur Techno-Féodalisme...</div>
    </div>
  );

  const { entities, summary } = data;
  const filtered = entities.filter(e =>
    (filter === "all" || e.feudal_risk === filter) &&
    (patFilter === "all" || e.feudal_pattern === patFilter)
  );

  const dists: Array<{ title: string; counts: Record<string, number>; colors: Record<string, string> }> = [
    { title: "Niveau Risque Féodal",        counts: summary.risk_counts,     colors: RISK_COLORS },
    { title: "Pattern Féodal",              counts: summary.pattern_counts,  colors: PAT_COLORS  },
    { title: "Sévérité Féodalisation",      counts: summary.severity_counts, colors: SEV_COLORS  },
    { title: "Action Déclenchée",           counts: summary.action_counts,   colors: ACT_COLORS  },
  ];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {selected && <DetailModal entity={selected} onClose={() => setSelected(null)} />}

      <div>
        <h1 className="text-2xl font-bold text-purple-400">
          Techno-Féodalisme &amp; Concentration Pouvoir Plateformes — Module 322
        </h1>
        <p className="text-purple-300/50 text-sm mt-1">
          Capture · Rente · Dépendance · Souveraineté Numérique
        </p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {([
          ["Entités Analysées",           summary.total,                                                "text-purple-400"],
          ["Crises Féodales",             summary.feudal_crisis_count,                                  "text-red-400"],
          ["Interventions Requises",      summary.feudal_intervention_count,                            "text-yellow-400"],
          ["Composite Moy.",              summary.avg_feudal_composite.toFixed(1),                      "text-purple-300"],
          ["Indice Féodalisation Moy.",   summary.avg_estimated_feudalization_index.toFixed(2),         "text-yellow-400"],
          ["Capture Moy.",                summary.avg_capture_score.toFixed(1),                         "text-purple-400"],
        ] as [string, string | number, string][]).map(([l, v, c]) => (
          <div key={String(l)} className="bg-slate-900 border border-yellow-700/30 rounded-xl p-3 text-center">
            <div className={`text-xl font-bold ${c}`}>{v}</div>
            <div className="text-xs text-purple-300/40 mt-0.5 leading-tight">{l}</div>
          </div>
        ))}
      </div>

      {/* Gauge Rings */}
      <div className="bg-slate-900 border border-yellow-700/30 rounded-xl p-5">
        <div className="grid grid-cols-4 gap-4">
          <GaugeRing value={summary.avg_capture_score}     label="Score Capture"      color="#7c3aed" />
          <GaugeRing value={summary.avg_rent_score}        label="Score Rente"        color="#eab308" />
          <GaugeRing value={summary.avg_dependency_score}  label="Score Dépendance"   color="#a855f7" />
          <GaugeRing value={summary.avg_sovereignty_score} label="Score Souveraineté" color="#06b6d4" />
        </div>
      </div>

      {/* Distribution Bars */}
      <div className="bg-slate-900 border border-yellow-700/30 rounded-xl p-5 grid grid-cols-1 md:grid-cols-2 gap-5">
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
                ? "bg-purple-900 border-purple-700 text-white"
                : "bg-slate-900 border-yellow-700/30 text-purple-400/70 hover:text-white"
            }`}
          >
            {r}
          </button>
        ))}
        <span className="w-px h-5 self-center bg-yellow-700/30" />
        {["all", "none", "monopoly_feudalism", "data_serfdom", "cloud_colonialism", "digital_enclosure", "worker_feudalization"].map(p => (
          <button
            key={p}
            onClick={() => setPat(p)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${
              patFilter === p
                ? "bg-yellow-900 border-yellow-700 text-white"
                : "bg-slate-900 border-yellow-700/30 text-purple-400/70 hover:text-white"
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
            className="bg-slate-900 border border-yellow-700/30 rounded-xl p-4 cursor-pointer hover:border-purple-500 transition-colors"
          >
            <div className="flex items-center justify-between mb-1">
              <span className="font-bold text-white">{e.entity_id}</span>
              <span className="text-xs text-purple-400/60">{e.region}</span>
            </div>
            <div className="text-xs text-slate-500 mb-2 capitalize">{e.platform_domain.replace(/_/g, " ")}</div>
            <div className="flex gap-1 mb-3 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[e.feudal_risk] || "bg-slate-700 text-slate-300"}`}>
                {e.feudal_risk}
              </span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[e.feudal_severity] || "bg-slate-700 text-slate-300"}`}>
                {e.feudal_severity.replace(/_/g, " ")}
              </span>
            </div>
            <div className="text-2xl font-black text-white mb-1">{e.feudal_composite.toFixed(1)}</div>
            <div className="text-xs text-purple-400/60 mb-2 capitalize">{e.feudal_pattern.replace(/_/g, " ")}</div>
            <div className="text-xs text-yellow-400 font-medium mb-2">
              Capture: {e.capture_score.toFixed(1)}
            </div>
            <div className="flex gap-1 flex-wrap">
              {e.is_feudal_crisis && (
                <span className="px-1.5 py-0.5 rounded bg-red-950 text-red-400 text-xs">CRISE</span>
              )}
              {e.requires_feudal_intervention && (
                <span className="px-1.5 py-0.5 rounded bg-purple-950 text-purple-400 text-xs">INTERVENTION</span>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
