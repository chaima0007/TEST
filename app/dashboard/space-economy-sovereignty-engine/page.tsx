"use client";
import { useEffect, useState } from "react";

type SecEntity = {
  entity_id: string;
  space_sector: string;
  region: string;
  congestion_score: number;
  militarization_score: number;
  monopoly_score: number;
  sovereignty_score: number;
  composite_score: number;
  risk_level: string;
  space_pattern: string;
  severity: string;
  recommended_action: string;
  signal: string;
  orbital_congestion_index: number;
  space_weaponization_level: number;
};

type SecSummary = {
  module_id: number;
  module_name: string;
  total_entities: number;
  critical_count: number;
  high_count: number;
  moderate_count: number;
  low_count: number;
  avg_composite: number;
  pattern_distribution: Record<string, number>;
  risk_distribution: Record<string, number>;
  severity_distribution: Record<string, number>;
  action_distribution: Record<string, number>;
  avg_estimated_orbital_risk_index: number;
  avg_congestion_score: number;
};

function GaugeRing({ value, label, color }: { value: number; label: string; color: string }) {
  const r = 36;
  const circ = 2 * Math.PI * r;
  const fill = circ * (1 - value / 100);
  return (
    <div className="flex flex-col items-center gap-1">
      <svg width="88" height="88" viewBox="0 0 88 88">
        <circle cx="44" cy="44" r={r} fill="none" stroke="#0f172a" strokeWidth="8" />
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

const RISK_COLORS: Record<string, string> = {
  low: "#10b981",
  moderate: "#f59e0b",
  high: "#8b5cf6",
  critical: "#ef4444",
};
const PAT_COLORS: Record<string, string> = {
  none: "#10b981",
  orbital_warfare: "#ef4444",
  kessler_syndrome: "#f97316",
  commercial_colonization: "#8b5cf6",
  space_resource_war: "#06b6d4",
  regulatory_vacuum_crisis: "#ec4899",
};
const SEV_COLORS: Record<string, string> = {
  espace_stable: "#10b981",
  tension_orbitale: "#f59e0b",
  escalade_spatiale_majeure: "#8b5cf6",
  "crise_orbitale_systémique": "#ef4444",
};
const ACTION_COLORS: Record<string, string> = {
  monitoring_continu: "#10b981",
  "surveillance_orbital_renforcée": "#06b6d4",
  "diplomatie_spatiale_activée": "#8b5cf6",
  "intervention_souveraineté_spatiale_urgente": "#ef4444",
};
const RISK_BADGE: Record<string, string> = {
  low: "bg-emerald-900 text-emerald-300",
  moderate: "bg-amber-900 text-amber-300",
  high: "bg-violet-900 text-violet-300",
  critical: "bg-red-950 text-red-400",
};
const SEV_BADGE: Record<string, string> = {
  espace_stable: "bg-emerald-900 text-emerald-300",
  tension_orbitale: "bg-amber-900 text-amber-300",
  escalade_spatiale_majeure: "bg-violet-900 text-violet-300",
  "crise_orbitale_systémique": "bg-red-950 text-red-400",
};

function DetailModal({ entity, onClose }: { entity: SecEntity; onClose: () => void }) {
  const [tab, setTab] = useState<"scores" | "signal" | "action">("scores");
  useEffect(() => {
    const h = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", h);
    return () => window.removeEventListener("keydown", h);
  }, [onClose]);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80" onClick={onClose}>
      <div className="bg-slate-950 border border-violet-700/30 rounded-xl w-full max-w-lg p-6 shadow-2xl" onClick={e => e.stopPropagation()}>
        <div className="flex items-center justify-between mb-4">
          <div>
            <span className="text-lg font-bold text-white">{entity.entity_id}</span>
            <span className="ml-2 text-cyan-400 text-xs">{entity.region}</span>
            <span className="ml-2 text-slate-500 text-xs">{entity.space_sector.replace(/_/g, " ")}</span>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl leading-none">✕</button>
        </div>
        <div className="flex gap-2 mb-4">
          {(["scores", "signal", "action"] as const).map(t => (
            <button key={t} onClick={() => setTab(t)}
              className={`px-3 py-1 rounded text-xs font-medium transition-colors ${tab === t ? "bg-violet-900 text-white" : "bg-slate-900 text-slate-400 hover:text-white"}`}>
              {t === "scores" ? "Scores" : t === "signal" ? "Signal" : "Action"}
            </button>
          ))}
        </div>

        {tab === "scores" && (
          <div className="grid grid-cols-2 gap-3 text-sm">
            {[
              ["Congestion Orbitale", entity.congestion_score, "#8b5cf6"],
              ["Militarisation", entity.militarization_score, "#ef4444"],
              ["Monopole Commercial", entity.monopoly_score, "#06b6d4"],
              ["Érosion Souveraineté", entity.sovereignty_score, "#f59e0b"],
            ].map(([l, v, c]) => (
              <div key={String(l)} className="bg-slate-900 border border-violet-700/20 rounded-lg p-3">
                <div className="text-violet-300/60 text-xs mb-1">{String(l)}</div>
                <div className="text-white font-bold text-lg">{Number(v).toFixed(1)}</div>
                <div className="h-1.5 rounded mt-1 bg-slate-800">
                  <div className="h-1.5 rounded" style={{ width: `${Math.min(Number(v), 100)}%`, background: String(c) }} />
                </div>
              </div>
            ))}
            <div className="col-span-2 bg-slate-900 border border-violet-700/20 rounded-lg p-3">
              <div className="text-violet-300/60 text-xs mb-1">Score Composite</div>
              <div className="text-white font-bold text-2xl">{entity.composite_score.toFixed(1)}</div>
            </div>
          </div>
        )}

        {tab === "signal" && (
          <div className="bg-slate-900 border border-violet-700/20 rounded-lg p-4 text-sm text-slate-200 leading-relaxed">
            {entity.signal}
            <div className="mt-3 flex gap-2 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[entity.risk_level] || "bg-slate-700 text-slate-300"}`}>
                {entity.risk_level}
              </span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[entity.severity] || "bg-slate-700 text-slate-300"}`}>
                {entity.severity.replace(/_/g, " ")}
              </span>
            </div>
            <div className="mt-3 grid grid-cols-2 gap-2 text-xs">
              <div className="bg-slate-800 rounded p-2">
                <div className="text-violet-300/60">Congestion Orbitale</div>
                <div className="text-white font-medium">{(entity.orbital_congestion_index * 100).toFixed(0)}%</div>
              </div>
              <div className="bg-slate-800 rounded p-2">
                <div className="text-violet-300/60">Armement Spatial</div>
                <div className="text-white font-medium">{(entity.space_weaponization_level * 100).toFixed(0)}%</div>
              </div>
            </div>
          </div>
        )}

        {tab === "action" && (
          <div className="space-y-3 text-sm">
            <div className="bg-slate-900 border border-violet-700/20 rounded-lg p-3">
              <div className="text-violet-300/60 text-xs mb-1">Action Recommandée</div>
              <div className="text-white font-medium">{entity.recommended_action.replace(/_/g, " ")}</div>
            </div>
            <div className="bg-slate-900 border border-violet-700/20 rounded-lg p-3">
              <div className="text-violet-300/60 text-xs mb-1">Secteur Spatial</div>
              <div className="text-white font-medium">{entity.space_sector.replace(/_/g, " ")}</div>
            </div>
            <div className="bg-slate-900 border border-violet-700/20 rounded-lg p-3">
              <div className="text-violet-300/60 text-xs mb-1">Patron Détecté</div>
              <div className="text-cyan-300 font-medium">{entity.space_pattern.replace(/_/g, " ")}</div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function SpaceEconomySovereigntyDashboard() {
  const [data, setData] = useState<{ entities: SecEntity[]; summary: SecSummary } | null>(null);
  const [filter, setFilter] = useState<string>("all");
  const [patFilter, setPatFilter] = useState<string>("all");
  const [selected, setSelected] = useState<SecEntity | null>(null);

  useEffect(() => {
    fetch("/api/space-economy-sovereignty-engine")
      .then(r => r.json())
      .then(setData)
      .catch(console.error);
  }, []);

  if (!data) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-violet-400 text-lg animate-pulse">Initialisation — Économie Spatiale & Souveraineté Orbitale...</div>
    </div>
  );

  const { entities, summary } = data;
  const filtered = entities.filter(e =>
    (filter === "all" || e.risk_level === filter) &&
    (patFilter === "all" || e.space_pattern === patFilter)
  );

  const dists: Array<{ title: string; counts: Record<string, number>; colors: Record<string, string> }> = [
    { title: "Niveau de Risque", counts: summary.risk_distribution, colors: RISK_COLORS },
    { title: "Patron Orbital", counts: summary.pattern_distribution, colors: PAT_COLORS },
    { title: "Sévérité", counts: summary.severity_distribution, colors: SEV_COLORS },
    { title: "Action Déclenchée", counts: summary.action_distribution, colors: ACTION_COLORS },
  ];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {selected && <DetailModal entity={selected} onClose={() => setSelected(null)} />}

      <div>
        <h1 className="text-2xl font-bold text-violet-400">
          Économie Spatiale &amp; Souveraineté Orbitale — Module 331
        </h1>
        <p className="text-cyan-300/50 text-sm mt-1">
          Congestion Orbitale · Militarisation Spatiale · Monopole Commercial · Souveraineté Orbitale
        </p>
      </div>

      {/* KPI Cards — 6 cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {[
          ["Total Systèmes",       summary.total_entities,                                          "text-cyan-400"],
          ["Crise Orbitale",       summary.critical_count,                                          "text-red-400"],
          ["Escalade Spatiale",    summary.high_count,                                              "text-violet-400"],
          ["Composite Moyen",      summary.avg_composite.toFixed(1),                               "text-amber-400"],
          ["Index Risque Orbital", `${summary.avg_estimated_orbital_risk_index.toFixed(2)}/10`,    "text-violet-300"],
          ["Congestion Moyenne",   summary.avg_congestion_score.toFixed(1),                        "text-cyan-300"],
        ].map(([l, v, c]) => (
          <div key={String(l)} className="bg-slate-900 border border-violet-700/30 rounded-xl p-3 text-center">
            <div className={`text-xl font-bold ${c}`}>{v}</div>
            <div className="text-xs text-violet-300/40 mt-0.5 leading-tight">{l}</div>
          </div>
        ))}
      </div>

      {/* 4 Gauge Rings */}
      <div className="bg-slate-900 border border-violet-700/30 rounded-xl p-5">
        <div className="grid grid-cols-4 gap-4">
          {(() => {
            const n = entities.length || 1;
            const avgCg = entities.reduce((s, e) => s + e.congestion_score, 0) / n;
            const avgMl = entities.reduce((s, e) => s + e.militarization_score, 0) / n;
            const avgMo = entities.reduce((s, e) => s + e.monopoly_score, 0) / n;
            const avgSv = entities.reduce((s, e) => s + e.sovereignty_score, 0) / n;
            return (
              <>
                <GaugeRing value={avgCg} label="Congestion" color="#8b5cf6" />
                <GaugeRing value={avgMl} label="Militarisation" color="#ef4444" />
                <GaugeRing value={avgMo} label="Monopole" color="#06b6d4" />
                <GaugeRing value={avgSv} label="Souveraineté" color="#f59e0b" />
              </>
            );
          })()}
        </div>
      </div>

      {/* 4 Distribution Bars */}
      <div className="bg-slate-900 border border-violet-700/30 rounded-xl p-5 grid grid-cols-1 md:grid-cols-2 gap-5">
        {dists.map(d => <DistBar key={d.title} {...d} />)}
      </div>

      {/* Filter Pills */}
      <div className="flex flex-wrap gap-2">
        {["all", "low", "moderate", "high", "critical"].map(r => (
          <button key={r} onClick={() => setFilter(r)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${filter === r ? "bg-violet-900 border-violet-700 text-white" : "bg-slate-900 border-violet-700/30 text-violet-400/70 hover:text-white"}`}>
            {r}
          </button>
        ))}
        <span className="w-px h-5 self-center bg-violet-700/30" />
        {["all", "none", "orbital_warfare", "kessler_syndrome", "commercial_colonization", "space_resource_war", "regulatory_vacuum_crisis"].map(p => (
          <button key={p} onClick={() => setPatFilter(p)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${patFilter === p ? "bg-cyan-950 border-cyan-700 text-white" : "bg-slate-900 border-violet-700/30 text-violet-400/70 hover:text-white"}`}>
            {p.replace(/_/g, " ")}
          </button>
        ))}
      </div>

      {/* Entity Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {filtered.map(e => (
          <div key={e.entity_id} onClick={() => setSelected(e)}
            className="bg-slate-900 border border-violet-700/30 rounded-xl p-4 cursor-pointer hover:border-violet-500 transition-colors">
            <div className="flex items-center justify-between mb-1">
              <span className="font-bold text-white">{e.entity_id}</span>
              <span className="text-xs text-cyan-400/60">{e.region}</span>
            </div>
            <div className="text-xs text-slate-500 mb-2 capitalize">{e.space_sector.replace(/_/g, " ")}</div>
            <div className="flex gap-1 mb-3 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[e.risk_level] || "bg-slate-700 text-slate-300"}`}>
                {e.risk_level}
              </span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[e.severity] || "bg-slate-700 text-slate-300"}`}>
                {e.severity.replace(/_/g, " ")}
              </span>
            </div>
            <div className="text-2xl font-black text-white mb-1">{e.composite_score.toFixed(1)}</div>
            <div className="text-xs text-violet-400/60 mb-2 capitalize">{e.space_pattern.replace(/_/g, " ")}</div>
            <div className="text-xs text-cyan-400 font-medium mb-2">
              Cong: {e.congestion_score.toFixed(1)} · Mil: {e.militarization_score.toFixed(1)} · Sov: {e.sovereignty_score.toFixed(1)}
            </div>
            <div className="text-xs text-slate-400 truncate">{e.signal}</div>
          </div>
        ))}
      </div>
    </div>
  );
}
