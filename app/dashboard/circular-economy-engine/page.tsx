"use client";
import { useEffect, useState } from "react";

type Entity = {
  id: string;
  economy_sector: string;
  region: string;
  material_score: number;
  regeneration_score: number;
  behavior_score: number;
  system_score: number;
  composite_score: number;
  risk_level: string;
  circular_pattern: string;
  severity: string;
  recommended_action: string;
  signal: string;
  product_lifecycle_extension: number;
  carbon_circularity_coupling: number;
};

type Summary = {
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
  avg_estimated_circularity_index: number;
};

function GaugeRing({ value, label, color }: { value: number; label: string; color: string }) {
  const r = 36;
  const circ = 2 * Math.PI * r;
  const fill = circ * (1 - value / 100);
  return (
    <div className="flex flex-col items-center gap-1">
      <svg width="88" height="88" viewBox="0 0 88 88">
        <circle cx="44" cy="44" r={r} fill="none" stroke="#0a1a0a" strokeWidth="8" />
        <circle cx="44" cy="44" r={r} fill="none" stroke={color} strokeWidth="8"
          strokeDasharray={circ} strokeDashoffset={fill}
          strokeLinecap="round" transform="rotate(-90 44 44)" />
        <text x="44" y="49" textAnchor="middle" fill="white" fontSize="13" fontWeight="bold">
          {Math.round(value)}
        </text>
      </svg>
      <span className="text-xs text-emerald-300/70 text-center">{label}</span>
    </div>
  );
}

function DistBar({ title, counts, colors }: { title: string; counts: Record<string, number>; colors: Record<string, string> }) {
  const total = Object.values(counts).reduce((a, b) => a + b, 0) || 1;
  return (
    <div className="flex flex-col gap-1">
      <span className="text-xs text-emerald-300/70 font-medium">{title}</span>
      <div className="flex h-3 rounded overflow-hidden gap-px">
        {Object.entries(counts).map(([k, v]) => (
          <div key={k} style={{ width: `${(v / total) * 100}%`, background: colors[k] || "#475569" }} title={`${k}: ${v}`} />
        ))}
      </div>
      <div className="flex flex-wrap gap-x-3 gap-y-0.5">
        {Object.entries(counts).map(([k, v]) => (
          <span key={k} className="text-xs text-emerald-300/60">
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
  high: "#f97316",
  critical: "#ef4444",
};
const PAT_COLORS: Record<string, string> = {
  none: "#10b981",
  linear_lock_in: "#78350f",
  waste_crisis: "#dc2626",
  regeneration_collapse: "#7c3aed",
  circular_inequality: "#0ea5e9",
  systemic_inertia: "#f97316",
};
const SEV_COLORS: Record<string, string> = {
  transition_engagée: "#10b981",
  inertie_structurelle: "#f59e0b",
  "transition_bloquée": "#f97316",
  effondrement_circulaire: "#7f1d1d",
};
const ACTION_COLORS: Record<string, string> = {
  optimisation_continue: "#10b981",
  "accélération_leviers_circulaires": "#06b6d4",
  "restructuration_modèle_économique": "#f59e0b",
  activation_protocole_transition_d_urgence: "#ef4444",
};

const RISK_BADGE: Record<string, string> = {
  low: "bg-emerald-900 text-emerald-300",
  moderate: "bg-amber-900 text-amber-300",
  high: "bg-orange-900 text-orange-300",
  critical: "bg-red-950 text-red-400",
};
const SEV_BADGE: Record<string, string> = {
  transition_engagée: "bg-emerald-900 text-emerald-300",
  inertie_structurelle: "bg-amber-900 text-amber-300",
  "transition_bloquée": "bg-orange-900 text-orange-300",
  effondrement_circulaire: "bg-red-950 text-red-400",
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
      <div className="bg-slate-950 border border-emerald-500/30 rounded-xl w-full max-w-lg p-6 shadow-2xl" onClick={e => e.stopPropagation()}>
        <div className="flex items-center justify-between mb-4">
          <div>
            <span className="text-lg font-bold text-white">{entity.id}</span>
            <span className="ml-2 text-emerald-400 text-xs">{entity.region}</span>
            <span className="ml-2 text-slate-500 text-xs">{entity.economy_sector.replace(/_/g, " ")}</span>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl leading-none">✕</button>
        </div>
        <div className="flex gap-2 mb-4">
          {(["scores", "signal", "action"] as const).map(t => (
            <button key={t} onClick={() => setTab(t)}
              className={`px-3 py-1 rounded text-xs font-medium transition-colors ${tab === t ? "bg-emerald-900 text-white" : "bg-slate-900 text-slate-400 hover:text-white"}`}>
              {t === "scores" ? "Scores" : t === "signal" ? "Signal" : "Action"}
            </button>
          ))}
        </div>

        {tab === "scores" && (
          <div className="grid grid-cols-2 gap-3 text-sm">
            {[
              ["Score Matériaux",    entity.material_score,     "#10b981"],
              ["Score Régénération", entity.regeneration_score, "#34d399"],
              ["Score Comportement", entity.behavior_score,     "#6ee7b7"],
              ["Score Système",      entity.system_score,       "#059669"],
            ].map(([l, v, c]) => (
              <div key={String(l)} className="bg-slate-900 border border-emerald-500/20 rounded-lg p-3">
                <div className="text-emerald-300/60 text-xs mb-1">{String(l)}</div>
                <div className="text-white font-bold text-lg">{Number(v).toFixed(1)}</div>
                <div className="h-1.5 rounded mt-1 bg-slate-800">
                  <div className="h-1.5 rounded" style={{ width: `${Math.min(Number(v), 100)}%`, background: String(c) }} />
                </div>
              </div>
            ))}
            <div className="col-span-2 bg-slate-900 border border-emerald-500/20 rounded-lg p-3">
              <div className="text-emerald-300/60 text-xs mb-1">Composite Circularité</div>
              <div className="text-white font-bold text-2xl">{entity.composite_score.toFixed(1)}</div>
              <div className="flex gap-4 mt-2 text-xs text-slate-400">
                <span>Extension Cycle: {(entity.product_lifecycle_extension * 100).toFixed(0)}%</span>
                <span>Couplage Carbone: {(entity.carbon_circularity_coupling * 100).toFixed(0)}%</span>
              </div>
            </div>
          </div>
        )}

        {tab === "signal" && (
          <div className="bg-slate-900 border border-emerald-500/20 rounded-lg p-4 text-sm text-slate-200 leading-relaxed">
            {entity.signal}
            <div className="mt-3 flex gap-2 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[entity.risk_level] || "bg-slate-700 text-slate-300"}`}>
                {entity.risk_level}
              </span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[entity.severity] || "bg-slate-700 text-slate-300"}`}>
                {entity.severity.replace(/_/g, " ")}
              </span>
            </div>
          </div>
        )}

        {tab === "action" && (
          <div className="space-y-3 text-sm">
            <div className="bg-slate-900 border border-emerald-500/20 rounded-lg p-3">
              <div className="text-emerald-300/60 text-xs mb-1">Action Recommandée</div>
              <div className="text-white font-medium">{entity.recommended_action.replace(/_/g, " ")}</div>
            </div>
            <div className="bg-slate-900 border border-emerald-500/20 rounded-lg p-3">
              <div className="text-emerald-300/60 text-xs mb-1">Pattern Circulaire</div>
              <div className="text-white font-medium capitalize">{entity.circular_pattern.replace(/_/g, " ")}</div>
            </div>
            <div className="bg-slate-900 border border-emerald-500/20 rounded-lg p-3">
              <div className="text-emerald-300/60 text-xs mb-1">Sévérité</div>
              <div className="text-white font-medium">{entity.severity.replace(/_/g, " ")}</div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function CircularEconomyDashboard() {
  const [data, setData] = useState<{ entities: Entity[]; summary: Summary } | null>(null);
  const [filter, setFilter] = useState<string>("all");
  const [patFilter, setPatFilter] = useState<string>("all");
  const [selected, setSelected] = useState<Entity | null>(null);

  useEffect(() => {
    fetch("/api/circular-economy-engine")
      .then(r => r.json())
      .then(setData)
      .catch(console.error);
  }, []);

  if (!data) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-emerald-400 text-lg animate-pulse">Initialisation du Moteur Économie Circulaire...</div>
    </div>
  );

  const { entities, summary } = data;
  const filtered = entities.filter(e =>
    (filter === "all" || e.risk_level === filter) &&
    (patFilter === "all" || e.circular_pattern === patFilter)
  );

  const avgMat = entities.length
    ? Math.round(entities.reduce((a, e) => a + e.material_score, 0) / entities.length * 10) / 10
    : 0;

  const dists = [
    { title: "Niveau Risque",           counts: summary.risk_distribution,     colors: RISK_COLORS  },
    { title: "Pattern Circulaire",      counts: summary.pattern_distribution,  colors: PAT_COLORS   },
    { title: "Sévérité",                counts: summary.severity_distribution, colors: SEV_COLORS   },
    { title: "Action Recommandée",      counts: summary.action_distribution,   colors: ACTION_COLORS },
  ] as Array<{ title: string; counts: Record<string, number>; colors: Record<string, string> }>;

  const avgReg = entities.length
    ? Math.round(entities.reduce((a, e) => a + e.regeneration_score, 0) / entities.length * 10) / 10
    : 0;
  const avgBeh = entities.length
    ? Math.round(entities.reduce((a, e) => a + e.behavior_score, 0) / entities.length * 10) / 10
    : 0;
  const avgSys = entities.length
    ? Math.round(entities.reduce((a, e) => a + e.system_score, 0) / entities.length * 10) / 10
    : 0;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {selected && <DetailModal entity={selected} onClose={() => setSelected(null)} />}

      <div>
        <h1 className="text-2xl font-bold text-emerald-400">Économie Circulaire &amp; Business Régénératif — Module 329</h1>
        <p className="text-emerald-300/50 text-sm mt-1">Matériaux · Régénération · Comportements · Système</p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {[
          ["Total Systèmes",     summary.total_entities,                          "text-emerald-400"],
          ["En Crise Linéaire",  summary.critical_count,                          "text-red-400"],
          ["Transition Bloquée", summary.high_count,                              "text-orange-400"],
          ["Composite Moyen",    summary.avg_composite.toFixed(1),               "text-yellow-400"],
          ["Index Circularité",  summary.avg_estimated_circularity_index.toFixed(2), "text-emerald-300"],
          ["Matériaux Moyen",    avgMat.toFixed(1),                              "text-green-400"],
        ].map(([l, v, c]) => (
          <div key={String(l)} className="bg-slate-900 border border-emerald-500/30 rounded-xl p-3 text-center">
            <div className={`text-xl font-bold ${c}`}>{v}</div>
            <div className="text-xs text-emerald-300/40 mt-0.5 leading-tight">{l}</div>
          </div>
        ))}
      </div>

      {/* Gauge Rings */}
      <div className="bg-slate-900 border border-emerald-500/30 rounded-xl p-5">
        <div className="grid grid-cols-4 gap-4">
          <GaugeRing value={avgMat}  label="Matériaux"    color="#10b981" />
          <GaugeRing value={avgReg}  label="Régénération" color="#34d399" />
          <GaugeRing value={avgBeh}  label="Comportements" color="#6ee7b7" />
          <GaugeRing value={avgSys}  label="Système"      color="#059669" />
        </div>
      </div>

      {/* Distribution Bars */}
      <div className="bg-slate-900 border border-emerald-500/30 rounded-xl p-5 grid grid-cols-1 md:grid-cols-2 gap-5">
        {dists.map(d => <DistBar key={d.title} {...d} />)}
      </div>

      {/* Filter Pills */}
      <div className="flex flex-wrap gap-2">
        {[
          { key: "all",      label: "Tous" },
          { key: "low",      label: "Faible" },
          { key: "moderate", label: "Modéré" },
          { key: "high",     label: "Élevé" },
          { key: "critical", label: "Critique" },
        ].map(({ key, label }) => (
          <button key={key} onClick={() => setFilter(key)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${filter === key ? "bg-emerald-900 border-emerald-700 text-white" : "bg-slate-900 border-emerald-500/30 text-emerald-400/70 hover:text-white"}`}>
            {label}
          </button>
        ))}
        <span className="w-px h-5 self-center bg-emerald-500/30" />
        {[
          { key: "all",                    label: "Tous patterns" },
          { key: "none",                   label: "Aucun" },
          { key: "linear_lock_in",         label: "Verrouillage Linéaire" },
          { key: "waste_crisis",           label: "Crise Déchets" },
          { key: "regeneration_collapse",  label: "Effondrement Régén." },
          { key: "circular_inequality",    label: "Inégalité Circulaire" },
          { key: "systemic_inertia",       label: "Inertie Systémique" },
        ].map(({ key, label }) => (
          <button key={key} onClick={() => setPatFilter(key)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${patFilter === key ? "bg-emerald-950 border-emerald-700 text-white" : "bg-slate-900 border-emerald-500/30 text-emerald-400/70 hover:text-white"}`}>
            {label}
          </button>
        ))}
      </div>

      {/* Entity Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {filtered.map(e => (
          <div key={e.id} onClick={() => setSelected(e)}
            className="bg-slate-900 border border-emerald-500/30 rounded-xl p-4 cursor-pointer hover:border-emerald-500 transition-colors">
            <div className="flex items-center justify-between mb-1">
              <span className="font-bold text-white">{e.id}</span>
              <span className="text-xs text-emerald-400/60">{e.region}</span>
            </div>
            <div className="text-xs text-slate-500 mb-2 capitalize">{e.economy_sector.replace(/_/g, " ")}</div>
            <div className="flex gap-1 mb-3 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[e.risk_level] || "bg-slate-700 text-slate-300"}`}>
                {e.risk_level}
              </span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[e.severity] || "bg-slate-700 text-slate-300"}`}>
                {e.severity.replace(/_/g, " ")}
              </span>
            </div>
            <div className="text-2xl font-black text-white mb-1">{e.composite_score.toFixed(1)}</div>
            <div className="text-xs text-emerald-400/60 mb-2 capitalize">{e.circular_pattern.replace(/_/g, " ")}</div>
            <div className="text-xs text-emerald-400 font-medium mb-2">
              Mat: {e.material_score.toFixed(1)} · Rég: {e.regeneration_score.toFixed(1)}
            </div>
            <div className="text-xs text-slate-400 truncate">{e.signal}</div>
          </div>
        ))}
      </div>
    </div>
  );
}
