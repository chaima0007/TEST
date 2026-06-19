"use client";
import { useEffect, useState } from "react";

type SDEEntity = {
  entity_id: string;
  orbital_shell: string;
  region: string;
  cascade_score: number;
  density_score: number;
  governance_score: number;
  weaponization_score: number;
  composite_score: number;
  risk_level: string;
  debris_pattern: string;
  severity: string;
  recommended_action: string;
  signal: string;
  debris_density: number;
  collision_probability: number;
};

type SDESummary = {
  module_id: number;
  module_name: string;
  total: number;
  critical: number;
  high: number;
  moderate: number;
  low: number;
  avg_composite: number;
  pattern_distribution: Record<string, number>;
  risk_distribution: Record<string, number>;
  severity_distribution: Record<string, number>;
  action_distribution: Record<string, number>;
  avg_estimated_kessler_risk_index: number;
};

function GaugeRing({ value, label, color }: { value: number; label: string; color: string }) {
  const r = 36;
  const circ = 2 * Math.PI * r;
  const fill = circ * (1 - value / 100);
  return (
    <div className="flex flex-col items-center gap-1">
      <svg width="88" height="88" viewBox="0 0 88 88">
        <circle cx="44" cy="44" r={r} fill="none" stroke="#0a1628" strokeWidth="8" />
        <circle cx="44" cy="44" r={r} fill="none" stroke={color} strokeWidth="8"
          strokeDasharray={circ} strokeDashoffset={fill}
          strokeLinecap="round" transform="rotate(-90 44 44)" />
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
            <span style={{ color: colors[k] || "#94a3b8" }}>■</span> {k.replace(/_/g, " ")} {v}
          </span>
        ))}
      </div>
    </div>
  );
}

const RISK_COLORS = { low: "#10b981", moderate: "#f59e0b", high: "#3b82f6", critical: "#ef4444" };
const PAT_COLORS: Record<string, string> = {
  none: "#10b981",
  kessler_syndrome_onset: "#ef4444",
  mega_constellation_crisis: "#f97316",
  debris_weaponization_cascade: "#a855f7",
  governance_remediation_failure: "#06b6d4",
  orbital_commons_collapse: "#1d4ed8",
};
const SEV_COLORS: Record<string, string> = {
  "débris_sous_surveillance": "#10b981",
  "saturation_orbitale_structurelle": "#f59e0b",
  "crise_débris_spatiaux_majeure": "#3b82f6",
  "effondrement_orbital_systémique": "#ef4444",
};
const ACTION_COLORS: Record<string, string> = {
  "veille_débris_continue": "#10b981",
  "renforcement_gouvernance_orbitale": "#06b6d4",
  "retrait_débris_actifs_urgence": "#3b82f6",
  "intervention_débris_urgence_mondiale": "#ef4444",
};
const RISK_BADGE: Record<string, string> = {
  low: "bg-emerald-900 text-emerald-300",
  moderate: "bg-amber-900 text-amber-300",
  high: "bg-blue-900 text-blue-300",
  critical: "bg-red-950 text-red-400",
};
const SEV_BADGE: Record<string, string> = {
  "débris_sous_surveillance": "bg-emerald-900 text-emerald-300",
  "saturation_orbitale_structurelle": "bg-amber-900 text-amber-300",
  "crise_débris_spatiaux_majeure": "bg-blue-900 text-blue-300",
  "effondrement_orbital_systémique": "bg-red-950 text-red-400",
};

function DetailModal({ entity, onClose }: { entity: SDEEntity; onClose: () => void }) {
  const [tab, setTab] = useState<"scores" | "signal" | "action">("scores");
  useEffect(() => {
    const h = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", h);
    return () => window.removeEventListener("keydown", h);
  }, [onClose]);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80" onClick={onClose}>
      <div className="bg-slate-950 border border-red-700/30 rounded-xl w-full max-w-lg p-6 shadow-2xl" onClick={e => e.stopPropagation()}>
        <div className="flex items-center justify-between mb-4">
          <div>
            <span className="text-lg font-bold text-white">{entity.entity_id}</span>
            <span className="ml-2 text-red-400 text-xs">{entity.region}</span>
            <span className="ml-2 text-slate-500 text-xs">{entity.orbital_shell}</span>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl leading-none">✕</button>
        </div>
        <div className="flex gap-2 mb-4">
          {(["scores", "signal", "action"] as const).map(t => (
            <button key={t} onClick={() => setTab(t)}
              className={`px-3 py-1 rounded text-xs font-medium transition-colors ${tab === t ? "bg-red-900 text-white" : "bg-slate-900 text-slate-400 hover:text-white"}`}>
              {t === "scores" ? "Scores" : t === "signal" ? "Signal" : "Action"}
            </button>
          ))}
        </div>

        {tab === "scores" && (
          <div className="grid grid-cols-2 gap-3 text-sm">
            {[
              ["Score Cascade",        entity.cascade_score,       "#ef4444"],
              ["Score Densité",        entity.density_score,       "#f97316"],
              ["Score Gouvernance",    entity.governance_score,    "#06b6d4"],
              ["Score Weaponisation",  entity.weaponization_score, "#a855f7"],
            ].map(([l, v, c]) => (
              <div key={String(l)} className="bg-slate-900 border border-red-700/20 rounded-lg p-3">
                <div className="text-red-300/60 text-xs mb-1">{String(l)}</div>
                <div className="text-white font-bold text-lg">{Number(v).toFixed(1)}</div>
                <div className="h-1.5 rounded mt-1 bg-slate-800">
                  <div className="h-1.5 rounded" style={{ width: `${Math.min(Number(v), 100)}%`, background: String(c) }} />
                </div>
              </div>
            ))}
            <div className="col-span-2 bg-slate-900 border border-red-700/20 rounded-lg p-3">
              <div className="text-red-300/60 text-xs mb-1">Score Composite Débris</div>
              <div className="text-white font-bold text-2xl">{entity.composite_score.toFixed(1)}</div>
            </div>
          </div>
        )}

        {tab === "signal" && (
          <div className="bg-slate-900 border border-red-700/20 rounded-lg p-4 text-sm text-slate-200 leading-relaxed">
            {entity.signal}
            <div className="mt-3 flex gap-2 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[entity.risk_level] || "bg-slate-700 text-slate-300"}`}>
                {entity.risk_level}
              </span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[entity.severity] || "bg-slate-700 text-slate-300"}`}>
                {entity.severity.replace(/_/g, " ")}
              </span>
            </div>
            <div className="mt-3 grid grid-cols-2 gap-2">
              <div className="bg-slate-800 rounded p-2">
                <div className="text-red-300/50 text-xs mb-0.5">Densité Débris</div>
                <div className="text-white text-sm font-medium">{Math.round(entity.debris_density * 100)}%</div>
              </div>
              <div className="bg-slate-800 rounded p-2">
                <div className="text-red-300/50 text-xs mb-0.5">Probabilité Collision</div>
                <div className="text-white text-sm font-medium">{Math.round(entity.collision_probability * 100)}%</div>
              </div>
            </div>
          </div>
        )}

        {tab === "action" && (
          <div className="space-y-3 text-sm">
            <div className="bg-slate-900 border border-red-700/20 rounded-lg p-3">
              <div className="text-red-300/60 text-xs mb-1">Action Recommandée</div>
              <div className="text-white font-medium">{entity.recommended_action.replace(/_/g, " ")}</div>
            </div>
            <div className="bg-slate-900 border border-red-700/20 rounded-lg p-3">
              <div className="text-red-300/60 text-xs mb-1">Couche Orbitale</div>
              <div className="text-white font-medium">{entity.orbital_shell}</div>
            </div>
            <div className="bg-slate-900 border border-red-700/20 rounded-lg p-3">
              <div className="text-red-300/60 text-xs mb-1">Patron Débris Détecté</div>
              <div className="text-red-300 font-medium">{entity.debris_pattern.replace(/_/g, " ")}</div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function SpaceDebrisDashboard() {
  const [data, setData]               = useState<{ entities: SDEEntity[]; summary: SDESummary } | null>(null);
  const [riskFilter, setRiskFilter]   = useState<string>("all");
  const [patFilter, setPatFilter]     = useState<string>("all");
  const [selected, setSelected]       = useState<SDEEntity | null>(null);

  useEffect(() => {
    fetch("/api/space-debris-engine")
      .then(r => r.json())
      .then(setData)
      .catch(console.error);
  }, []);

  if (!data) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-red-400 text-lg animate-pulse">Initialisation du Moteur Débris Spatiaux...</div>
    </div>
  );

  const { entities, summary } = data;
  const filtered = entities.filter(e =>
    (riskFilter === "all" || e.risk_level === riskFilter) &&
    (patFilter === "all" || e.debris_pattern === patFilter)
  );

  const avgDensity = entities.reduce((s, e) => s + e.density_score, 0) / (entities.length || 1);

  const dists = [
    { title: "Niveau de Risque Orbital",    counts: summary.risk_distribution,     colors: RISK_COLORS   },
    { title: "Patron Débris Détecté",       counts: summary.pattern_distribution,  colors: PAT_COLORS   },
    { title: "Sévérité Orbitale",           counts: summary.severity_distribution, colors: SEV_COLORS   },
    { title: "Action Déclenchée",           counts: summary.action_distribution,   colors: ACTION_COLORS },
  ] as Array<{ title: string; counts: Record<string, number>; colors: Record<string, string> }>;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {selected && <DetailModal entity={selected} onClose={() => setSelected(null)} />}

      <div>
        <h1 className="text-2xl font-bold text-red-400">Débris Spatiaux &amp; Syndrome Kessler — Module 370</h1>
        <p className="text-red-300/50 text-sm mt-1">
          Cascade Orbitale · Densité Débris · Gouvernance Spatiale · Weaponisation Orbitale
        </p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {[
          ["Total Orbites",        summary.total,                                                    "text-red-400"],
          ["Kessler Imminent",     summary.critical,                                                 "text-red-500"],
          ["Crise Majeure",        summary.high,                                                     "text-orange-400"],
          ["Composite Moyen",      `${summary.avg_composite.toFixed(1)}`,                            "text-red-300"],
          ["Index Risque Kessler", `${summary.avg_estimated_kessler_risk_index.toFixed(2)}/10`,      "text-amber-400"],
          ["Densité Moyenne",      `${Math.round(avgDensity * 10) / 10}`,                            "text-slate-300"],
        ].map(([l, v, c]) => (
          <div key={String(l)} className="bg-slate-900 border border-red-700/30 rounded-xl p-3 text-center">
            <div className={`text-xl font-bold ${c}`}>{v}</div>
            <div className="text-xs text-red-300/40 mt-0.5 leading-tight">{l}</div>
          </div>
        ))}
      </div>

      {/* Gauge Rings */}
      <div className="bg-slate-900 border border-red-700/30 rounded-xl p-5">
        <div className="grid grid-cols-4 gap-4">
          <GaugeRing
            value={entities.reduce((s, e) => s + e.cascade_score, 0) / (entities.length || 1)}
            label="Cascade Moy."
            color="#ef4444"
          />
          <GaugeRing
            value={entities.reduce((s, e) => s + e.density_score, 0) / (entities.length || 1)}
            label="Densité Moy."
            color="#f97316"
          />
          <GaugeRing
            value={entities.reduce((s, e) => s + e.governance_score, 0) / (entities.length || 1)}
            label="Gouvernance Moy."
            color="#06b6d4"
          />
          <GaugeRing
            value={entities.reduce((s, e) => s + e.weaponization_score, 0) / (entities.length || 1)}
            label="Weaponisation Moy."
            color="#a855f7"
          />
        </div>
      </div>

      {/* Distribution Bars */}
      <div className="bg-slate-900 border border-red-700/30 rounded-xl p-5 grid grid-cols-1 md:grid-cols-2 gap-5">
        {dists.map(d => <DistBar key={d.title} {...d} />)}
      </div>

      {/* Filter Pills */}
      <div className="flex flex-wrap gap-2">
        {["all", "low", "moderate", "high", "critical"].map(r => (
          <button key={r} onClick={() => setRiskFilter(r)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${riskFilter === r ? "bg-red-900 border-red-700 text-white" : "bg-slate-900 border-red-700/30 text-red-400/70 hover:text-white"}`}>
            {r}
          </button>
        ))}
        <span className="w-px h-5 self-center bg-red-700/30" />
        {["all", "none", "kessler_syndrome_onset", "mega_constellation_crisis", "debris_weaponization_cascade", "governance_remediation_failure", "orbital_commons_collapse"].map(p => (
          <button key={p} onClick={() => setPatFilter(p)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${patFilter === p ? "bg-red-950 border-red-700 text-white" : "bg-slate-900 border-red-700/30 text-red-400/70 hover:text-white"}`}>
            {p.replace(/_/g, " ")}
          </button>
        ))}
      </div>

      {/* Entity Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {filtered.map(e => (
          <div key={e.entity_id} onClick={() => setSelected(e)}
            className="bg-slate-900 border border-red-700/30 rounded-xl p-4 cursor-pointer hover:border-red-500 transition-colors">
            <div className="flex items-center justify-between mb-1">
              <span className="font-bold text-white">{e.entity_id}</span>
              <span className="text-xs text-red-400/60">{e.region}</span>
            </div>
            <div className="text-xs text-slate-500 mb-2">{e.orbital_shell}</div>
            <div className="flex gap-1 mb-3 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[e.risk_level] || "bg-slate-700 text-slate-300"}`}>
                {e.risk_level}
              </span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[e.severity] || "bg-slate-700 text-slate-300"}`}>
                {e.severity.replace(/_/g, " ")}
              </span>
            </div>
            <div className="text-2xl font-black text-white mb-1">{e.composite_score.toFixed(1)}</div>
            <div className="text-xs text-red-400/60 mb-2 capitalize">{e.debris_pattern.replace(/_/g, " ")}</div>
            <div className="text-xs text-red-400 font-medium mb-2">
              Cascade: {e.cascade_score.toFixed(1)} · Densité: {e.density_score.toFixed(1)}
            </div>
            <div className="text-xs text-slate-400 truncate">{e.signal}</div>
          </div>
        ))}
      </div>
    </div>
  );
}
