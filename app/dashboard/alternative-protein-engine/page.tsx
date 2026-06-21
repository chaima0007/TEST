"use client";
import { useEffect, useState } from "react";

type ProteinEntity = {
  id: string;
  protein_sector: string;
  region: string;
  disruption_score: number;
  monopoly_score: number;
  transition_score: number;
  safety_score: number;
  composite_score: number;
  risk_level: string;
  protein_pattern: string;
  severity: string;
  recommended_action: string;
  signal: string;
  traditional_livestock_industry_disruption_speed: number;
  biotech_monopoly_in_food_production: number;
};

type ProteinSummary = {
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
  avg_estimated_protein_disruption_index: number;
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
      <span className="text-xs text-green-300/70 text-center">{label}</span>
    </div>
  );
}

function DistBar({ title, counts, colors }: { title: string; counts: Record<string, number>; colors: Record<string, string> }) {
  const total = Object.values(counts).reduce((a, b) => a + b, 0) || 1;
  return (
    <div className="flex flex-col gap-1">
      <span className="text-xs text-green-300/70 font-medium">{title}</span>
      <div className="flex h-3 rounded overflow-hidden gap-px">
        {Object.entries(counts).map(([k, v]) => (
          <div key={k} style={{ width: `${(v / total) * 100}%`, background: colors[k] || "#475569" }} title={`${k}: ${v}`} />
        ))}
      </div>
      <div className="flex flex-wrap gap-x-3 gap-y-0.5">
        {Object.entries(counts).map(([k, v]) => (
          <span key={k} className="text-xs text-green-300/60">
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
  livestock_disruption_crisis: "#ef4444",
  biotech_food_monopoly: "#f97316",
  food_sovereignty_capture: "#a855f7",
  transition_inequality_trap: "#06b6d4",
  biosafety_novel_protein: "#1d4ed8",
};
const SEV_COLORS: Record<string, string> = {
  "transition_protéique_gérée": "#10b981",
  "restructuration_alimentaire_active": "#f59e0b",
  "transition_protéique_critique": "#3b82f6",
  "disruption_alimentaire_systémique": "#ef4444",
};
const ACTION_COLORS: Record<string, string> = {
  "veille_disruption_alimentaire_continue": "#10b981",
  "accompagnement_transition_protéique_équitable": "#f59e0b",
  "régulation_biotech_alimentaire_stricte": "#3b82f6",
  "gouvernance_urgente_disruption_alimentaire": "#ef4444",
};
const RISK_BADGE: Record<string, string> = {
  low: "bg-emerald-900 text-emerald-300",
  moderate: "bg-amber-900 text-amber-300",
  high: "bg-blue-900 text-blue-300",
  critical: "bg-red-950 text-red-400",
};
const SEV_BADGE: Record<string, string> = {
  "transition_protéique_gérée": "bg-emerald-900 text-emerald-300",
  "restructuration_alimentaire_active": "bg-amber-900 text-amber-300",
  "transition_protéique_critique": "bg-blue-900 text-blue-300",
  "disruption_alimentaire_systémique": "bg-red-950 text-red-400",
};

function DetailModal({ entity, onClose }: { entity: ProteinEntity; onClose: () => void }) {
  const [tab, setTab] = useState<"scores" | "signal" | "action">("scores");

  useEffect(() => {
    const h = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", h);
    return () => window.removeEventListener("keydown", h);
  }, [onClose]);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80" onClick={onClose}>
      <div className="bg-slate-950 border border-green-700/30 rounded-xl w-full max-w-lg p-6 shadow-2xl" onClick={e => e.stopPropagation()}>
        <div className="flex items-center justify-between mb-4">
          <div>
            <span className="text-lg font-bold text-white">{entity.id}</span>
            <span className="ml-2 text-green-400 text-xs">{entity.region}</span>
            <span className="ml-2 text-slate-500 text-xs">{entity.protein_sector.replace(/_/g, " ")}</span>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl leading-none">✕</button>
        </div>
        <div className="flex gap-2 mb-4">
          {(["scores", "signal", "action"] as const).map(t => (
            <button key={t} onClick={() => setTab(t)}
              className={`px-3 py-1 rounded text-xs font-medium transition-colors ${tab === t ? "bg-green-900 text-white" : "bg-slate-900 text-slate-400 hover:text-white"}`}>
              {t === "scores" ? "Scores" : t === "signal" ? "Signal" : "Action"}
            </button>
          ))}
        </div>

        {tab === "scores" && (
          <div className="grid grid-cols-2 gap-3 text-sm">
            {[
              ["Score Disruption",  entity.disruption_score,  "#ef4444"],
              ["Score Monopole",    entity.monopoly_score,    "#f97316"],
              ["Score Transition",  entity.transition_score,  "#06b6d4"],
              ["Score Sécurité",    entity.safety_score,      "#f59e0b"],
            ].map(([l, v, c]) => (
              <div key={String(l)} className="bg-slate-900 border border-green-700/20 rounded-lg p-3">
                <div className="text-green-300/60 text-xs mb-1">{String(l)}</div>
                <div className="text-white font-bold text-lg">{Number(v).toFixed(1)}</div>
                <div className="h-1.5 rounded mt-1 bg-slate-800">
                  <div className="h-1.5 rounded" style={{ width: `${Math.min(Number(v), 100)}%`, background: String(c) }} />
                </div>
              </div>
            ))}
            <div className="col-span-2 bg-slate-900 border border-green-700/20 rounded-lg p-3">
              <div className="text-green-300/60 text-xs mb-1">Score Composite</div>
              <div className="text-white font-bold text-2xl">{entity.composite_score.toFixed(1)}</div>
            </div>
          </div>
        )}

        {tab === "signal" && (
          <div className="bg-slate-900 border border-green-700/20 rounded-lg p-4 text-sm text-slate-200 leading-relaxed">
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
            <div className="bg-slate-900 border border-green-700/20 rounded-lg p-3">
              <div className="text-green-300/60 text-xs mb-1">Action Recommandée</div>
              <div className="text-white font-medium">{entity.recommended_action.replace(/_/g, " ")}</div>
            </div>
            <div className="bg-slate-900 border border-green-700/20 rounded-lg p-3">
              <div className="text-green-300/60 text-xs mb-1">Secteur Protéique</div>
              <div className="text-white font-medium">{entity.protein_sector.replace(/_/g, " ")}</div>
            </div>
            <div className="bg-slate-900 border border-green-700/20 rounded-lg p-3">
              <div className="text-green-300/60 text-xs mb-1">Patron Détecté</div>
              <div className="text-green-300 font-medium">{entity.protein_pattern.replace(/_/g, " ")}</div>
            </div>
            <div className="bg-slate-900 border border-green-700/20 rounded-lg p-3">
              <div className="text-green-300/60 text-xs mb-1">Vitesse Disruption Élevage</div>
              <div className="text-amber-400 font-bold">{(entity.traditional_livestock_industry_disruption_speed * 100).toFixed(0)}%</div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function AlternativeProteinDashboard() {
  const [data, setData]           = useState<{ entities: ProteinEntity[]; summary: ProteinSummary } | null>(null);
  const [filter, setFilter]       = useState<string>("all");
  const [patFilter, setPatFilter] = useState<string>("all");
  const [selected, setSelected]   = useState<ProteinEntity | null>(null);

  useEffect(() => {
    fetch("/api/alternative-protein-engine")
      .then(r => r.json())
      .then(setData)
      .catch(console.error);
  }, []);

  if (!data) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-green-400 text-lg animate-pulse">Initialisation du Moteur Protéines Alternatives...</div>
    </div>
  );

  const { entities, summary } = data;

  const filtered = entities.filter(e =>
    (filter === "all" || e.risk_level === filter) &&
    (patFilter === "all" || e.protein_pattern === patFilter)
  );

  const dists = [
    { title: "Niveau de Risque",          counts: summary.risk_distribution,     colors: RISK_COLORS   },
    { title: "Patron Alimentaire",         counts: summary.pattern_distribution,  colors: PAT_COLORS    },
    { title: "Sévérité Disruption",        counts: summary.severity_distribution, colors: SEV_COLORS    },
    { title: "Action Déclenchée",          counts: summary.action_distribution,   colors: ACTION_COLORS },
  ] as Array<{ title: string; counts: Record<string, number>; colors: Record<string, string> }>;

  const avgDisruption  = entities.length ? entities.reduce((a, e) => a + e.disruption_score,  0) / entities.length : 0;
  const avgMonopoly    = entities.length ? entities.reduce((a, e) => a + e.monopoly_score,    0) / entities.length : 0;
  const avgTransition  = entities.length ? entities.reduce((a, e) => a + e.transition_score,  0) / entities.length : 0;
  const avgSafety      = entities.length ? entities.reduce((a, e) => a + e.safety_score,      0) / entities.length : 0;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {selected && <DetailModal entity={selected} onClose={() => setSelected(null)} />}

      <div>
        <h1 className="text-2xl font-bold text-green-400">
          Protéines Alternatives &amp; Disruption FoodTech — Module 349
        </h1>
        <p className="text-green-300/50 text-sm mt-1">
          Disruption Alimentaire · Monopole Biotech · Transition Protéique · Biosécurité Novatrice
        </p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {[
          ["Total Secteurs",              summary.total_entities,                                               "text-green-400"],
          ["Disruption Systémique",       summary.critical_count,                                               "text-red-400"],
          ["Transition Critique",         summary.high_count,                                                   "text-amber-400"],
          ["Composite Moyen",             `${summary.avg_composite.toFixed(1)}`,                                "text-green-400"],
          ["Index Disruption Protéique",  `${summary.avg_estimated_protein_disruption_index.toFixed(2)}/10`,   "text-amber-400"],
          ["Disruption Moyenne",          `${summary.avg_composite.toFixed(1)}`,                                "text-green-300"],
        ].map(([l, v, c]) => (
          <div key={String(l)} className="bg-slate-900 border border-green-700/30 rounded-xl p-3 text-center">
            <div className={`text-xl font-bold ${c}`}>{v}</div>
            <div className="text-xs text-green-300/40 mt-0.5 leading-tight">{l}</div>
          </div>
        ))}
      </div>

      {/* Gauge Rings */}
      <div className="bg-slate-900 border border-green-700/30 rounded-xl p-5">
        <div className="grid grid-cols-4 gap-4">
          <GaugeRing value={avgDisruption} label="Disruption Moy."  color="#ef4444" />
          <GaugeRing value={avgMonopoly}   label="Monopole Moy."    color="#f97316" />
          <GaugeRing value={avgTransition} label="Transition Moy."  color="#06b6d4" />
          <GaugeRing value={avgSafety}     label="Sécurité Moy."    color="#f59e0b" />
        </div>
      </div>

      {/* Distribution Bars */}
      <div className="bg-slate-900 border border-green-700/30 rounded-xl p-5 grid grid-cols-1 md:grid-cols-2 gap-5">
        {dists.map(d => <DistBar key={d.title} {...d} />)}
      </div>

      {/* Filter Pills */}
      <div className="flex flex-wrap gap-2">
        {["all", "low", "moderate", "high", "critical"].map(r => (
          <button key={r} onClick={() => setFilter(r)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${filter === r ? "bg-green-900 border-green-700 text-white" : "bg-slate-900 border-green-700/30 text-green-400/70 hover:text-white"}`}>
            {r === "all" ? "Tous" : r === "low" ? "Faible" : r === "moderate" ? "Modéré" : r === "high" ? "Élevé" : "Critique"}
          </button>
        ))}
        <span className="w-px h-5 self-center bg-green-700/30" />
        {["all", "none", "livestock_disruption_crisis", "biotech_food_monopoly", "food_sovereignty_capture", "transition_inequality_trap", "biosafety_novel_protein"].map(p => (
          <button key={p} onClick={() => setPatFilter(p)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${patFilter === p ? "bg-amber-950 border-amber-700 text-white" : "bg-slate-900 border-green-700/30 text-green-400/70 hover:text-white"}`}>
            {p === "all" ? "Tous patrons" : p.replace(/_/g, " ")}
          </button>
        ))}
      </div>

      {/* Entity Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {filtered.map(e => (
          <div key={e.id} onClick={() => setSelected(e)}
            className="bg-slate-900 border border-green-700/30 rounded-xl p-4 cursor-pointer hover:border-green-500 transition-colors">
            <div className="flex items-center justify-between mb-1">
              <span className="font-bold text-white">{e.id}</span>
              <span className="text-xs text-green-400/60">{e.region}</span>
            </div>
            <div className="text-xs text-slate-500 mb-2 capitalize">{e.protein_sector.replace(/_/g, " ")}</div>
            <div className="flex gap-1 mb-3 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[e.risk_level] || "bg-slate-700 text-slate-300"}`}>
                {e.risk_level === "critical" ? "Critique" : e.risk_level === "high" ? "Élevé" : e.risk_level === "moderate" ? "Modéré" : "Faible"}
              </span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[e.severity] || "bg-slate-700 text-slate-300"}`}>
                {e.severity.replace(/_/g, " ")}
              </span>
            </div>
            <div className="text-2xl font-black text-white mb-1">{e.composite_score.toFixed(1)}</div>
            <div className="text-xs text-green-400/60 mb-2 capitalize">{e.protein_pattern.replace(/_/g, " ")}</div>
            <div className="text-xs text-amber-400 font-medium mb-2">
              Disruption: {e.disruption_score.toFixed(1)} · Monopole: {e.monopoly_score.toFixed(1)}
            </div>
            <div className="text-xs text-slate-400 leading-snug line-clamp-2">{e.signal}</div>
          </div>
        ))}
      </div>
    </div>
  );
}
