"use client";
import { useEffect, useState } from "react";

type Entity = {
  entity_id: string;
  creative_sector: string;
  region: string;
  displacement_score: number;
  control_score: number;
  culture_score: number;
  integrity_score: number;
  composite_score: number;
  risk_level: string;
  genai_pattern: string;
  severity: string;
  recommended_action: string;
  signal: string;
  AI_creative_displacement_rate: number;
  generative_model_monopoly_concentration: number;
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
  avg_estimated_creative_disruption_index: number;
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
      <span className="text-xs text-yellow-300/70 text-center">{label}</span>
    </div>
  );
}

function DistBar({ title, counts, colors }: { title: string; counts: Record<string, number>; colors: Record<string, string> }) {
  const total = Object.values(counts).reduce((a, b) => a + b, 0) || 1;
  return (
    <div className="flex flex-col gap-1">
      <span className="text-xs text-yellow-300/70 font-medium">{title}</span>
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
          <span key={k} className="text-xs text-yellow-300/60">
            <span style={{ color: colors[k] || "#94a3b8" }}>■</span> {k.replace(/_/g, " ")} {v}
          </span>
        ))}
      </div>
    </div>
  );
}

const RISK_COLORS: Record<string, string> = { low: "#10b981", moderate: "#f59e0b", high: "#d97706", critical: "#7c3aed" };
const PAT_COLORS: Record<string, string> = {
  none: "#10b981",
  creative_class_extinction: "#7c3aed",
  generative_monopoly_capture: "#ef4444",
  cultural_homogenization_crisis: "#d97706",
  IP_extraction_empire: "#1d4ed8",
  synthetic_content_saturation: "#b45309",
};
const SEV_COLORS: Record<string, string> = {
  "disruption_créative_gérée": "#10b981",
  "restructuration_créative_active": "#f59e0b",
  "disruption_créative_majeure": "#d97706",
  "effondrement_économie_créative": "#7c3aed",
};
const ACT_COLORS: Record<string, string> = {
  "veille_disruption_créative_continue": "#10b981",
  "renforcement_droits_créateurs_IA": "#f59e0b",
  "régulation_IA_générative_stricte": "#d97706",
  "protection_urgente_économie_créative": "#7c3aed",
};
const RISK_BADGE: Record<string, string> = {
  low: "bg-emerald-900 text-emerald-300",
  moderate: "bg-amber-900 text-amber-300",
  high: "bg-orange-900 text-orange-300",
  critical: "bg-violet-950 text-violet-300",
};
const SEV_BADGE: Record<string, string> = {
  "disruption_créative_gérée": "bg-emerald-900 text-emerald-300",
  "restructuration_créative_active": "bg-amber-900 text-amber-300",
  "disruption_créative_majeure": "bg-orange-900 text-orange-300",
  "effondrement_économie_créative": "bg-violet-950 text-violet-300",
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
            <span className="ml-2 text-yellow-400 text-xs">{entity.region}</span>
            <span className="ml-2 text-slate-500 text-xs">{entity.creative_sector.replace(/_/g, " ")}</span>
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
                  ? "bg-violet-900 text-white"
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
              ["Déplacement",  entity.displacement_score, "#7c3aed"],
              ["Contrôle",     entity.control_score,      "#ef4444"],
              ["Culture",      entity.culture_score,      "#d97706"],
              ["Intégrité",    entity.integrity_score,    "#1d4ed8"],
            ] as [string, number, string][]).map(([l, v, c]) => (
              <div key={l} className="bg-slate-900 border border-yellow-700/20 rounded-lg p-3">
                <div className="text-yellow-300/60 text-xs mb-1">{l}</div>
                <div className="text-white font-bold text-lg">{Number(v).toFixed(1)}</div>
                <div className="h-1.5 rounded mt-1 bg-slate-800">
                  <div className="h-1.5 rounded" style={{ width: `${Math.min(Number(v), 100)}%`, background: c }} />
                </div>
              </div>
            ))}
            <div className="col-span-2 bg-slate-900 border border-yellow-700/20 rounded-lg p-3">
              <div className="text-yellow-300/60 text-xs mb-1">Composite Disruption Créative</div>
              <div className="text-white font-bold text-2xl">{entity.composite_score.toFixed(1)}</div>
            </div>
          </div>
        )}

        {tab === "signal" && (
          <div className="bg-slate-900 border border-yellow-700/20 rounded-lg p-4 text-sm text-slate-200 leading-relaxed">
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
                <div className="text-yellow-300/50 mb-0.5">Taux Déplacement Créatif IA</div>
                <div className="text-white font-bold">{Math.round(entity.AI_creative_displacement_rate * 100)}%</div>
              </div>
              <div className="bg-slate-800 rounded p-2">
                <div className="text-yellow-300/50 mb-0.5">Concentration Monopole Génératif</div>
                <div className="text-white font-bold">{Math.round(entity.generative_model_monopoly_concentration * 100)}%</div>
              </div>
            </div>
          </div>
        )}

        {tab === "action" && (
          <div className="space-y-3 text-sm">
            <div className="bg-slate-900 border border-yellow-700/20 rounded-lg p-3">
              <div className="text-yellow-300/60 text-xs mb-1">Action Recommandée</div>
              <div className="text-white font-medium">{entity.recommended_action.replace(/_/g, " ")}</div>
            </div>
            <div className="bg-slate-900 border border-yellow-700/20 rounded-lg p-3">
              <div className="text-yellow-300/60 text-xs mb-1">Pattern IA Générative Détecté</div>
              <div className="text-white font-medium capitalize">{entity.genai_pattern.replace(/_/g, " ")}</div>
            </div>
            <div className="bg-slate-900 border border-yellow-700/20 rounded-lg p-3">
              <div className="text-yellow-300/60 text-xs mb-1">Sévérité</div>
              <div className="text-white font-medium">{entity.severity.replace(/_/g, " ")}</div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function GenerativeAIEconomyEngineDashboard() {
  const [data, setData]         = useState<{ entities: Entity[]; summary: Summary } | null>(null);
  const [filter, setFilter]     = useState<string>("all");
  const [patFilter, setPat]     = useState<string>("all");
  const [selected, setSelected] = useState<Entity | null>(null);

  useEffect(() => {
    fetch("/api/generative-ai-economy-engine")
      .then(r => r.json())
      .then(setData)
      .catch(console.error);
  }, []);

  if (!data) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-violet-400 text-lg animate-pulse">Initialisation du Moteur IA Générative &amp; Économie Créative...</div>
    </div>
  );

  const { entities, summary } = data;
  const filtered = entities.filter(e =>
    (filter === "all" || e.risk_level === filter) &&
    (patFilter === "all" || e.genai_pattern === patFilter)
  );

  const avgDisplacement = entities.reduce((s, e) => s + e.displacement_score, 0) / (entities.length || 1);

  const dists: Array<{ title: string; counts: Record<string, number>; colors: Record<string, string> }> = [
    { title: "Niveau Risque Disruption",       counts: summary.risk_distribution,     colors: RISK_COLORS },
    { title: "Pattern IA Générative",          counts: summary.pattern_distribution,  colors: PAT_COLORS  },
    { title: "Sévérité Disruption Créative",   counts: summary.severity_distribution, colors: SEV_COLORS  },
    { title: "Action Déclenchée",              counts: summary.action_distribution,   colors: ACT_COLORS  },
  ];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {selected && <DetailModal entity={selected} onClose={() => setSelected(null)} />}

      <div>
        <h1 className="text-2xl font-bold text-yellow-400">
          IA Générative &amp; Disruption Économie Créative — Module 350
        </h1>
        <p className="text-yellow-300/50 text-sm mt-1">
          Déplacement · Contrôle · Culture · Intégrité Créative
        </p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {([
          ["Total Secteurs",              summary.total_entities,                                   "text-yellow-400"],
          ["Effondrement Créatif",        summary.critical_count,                                   "text-violet-400"],
          ["Disruption Majeure",          summary.high_count,                                       "text-orange-400"],
          ["Composite Moyen",             summary.avg_composite.toFixed(1),                         "text-yellow-300"],
          ["Index Disruption Créative",   summary.avg_estimated_creative_disruption_index.toFixed(2), "text-violet-400"],
          ["Déplacement Moyen",           avgDisplacement.toFixed(1),                               "text-slate-300"],
        ] as [string, string | number, string][]).map(([l, v, c]) => (
          <div key={String(l)} className="bg-slate-900 border border-yellow-700/30 rounded-xl p-3 text-center">
            <div className={`text-xl font-bold ${c}`}>{v}</div>
            <div className="text-xs text-yellow-300/40 mt-0.5 leading-tight">{l}</div>
          </div>
        ))}
      </div>

      {/* Gauge Rings */}
      <div className="bg-slate-900 border border-yellow-700/30 rounded-xl p-5">
        <div className="grid grid-cols-4 gap-4">
          <GaugeRing value={entities.reduce((s, e) => s + e.displacement_score, 0) / (entities.length || 1)} label="Déplacement" color="#7c3aed" />
          <GaugeRing value={entities.reduce((s, e) => s + e.control_score, 0)     / (entities.length || 1)} label="Contrôle"     color="#ef4444" />
          <GaugeRing value={entities.reduce((s, e) => s + e.culture_score, 0)     / (entities.length || 1)} label="Culture"      color="#d97706" />
          <GaugeRing value={entities.reduce((s, e) => s + e.integrity_score, 0)   / (entities.length || 1)} label="Intégrité"    color="#1d4ed8" />
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
                ? "bg-violet-900 border-violet-700 text-white"
                : "bg-slate-900 border-yellow-700/30 text-yellow-400/70 hover:text-white"
            }`}
          >
            {r}
          </button>
        ))}
        <span className="w-px h-5 self-center bg-yellow-700/30" />
        {["all", "none", "creative_class_extinction", "generative_monopoly_capture", "cultural_homogenization_crisis", "IP_extraction_empire", "synthetic_content_saturation"].map(p => (
          <button
            key={p}
            onClick={() => setPat(p)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${
              patFilter === p
                ? "bg-slate-700 border-slate-500 text-white"
                : "bg-slate-900 border-yellow-700/30 text-yellow-400/70 hover:text-white"
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
            className="bg-slate-900 border border-yellow-700/30 rounded-xl p-4 cursor-pointer hover:border-violet-500 transition-colors"
          >
            <div className="flex items-center justify-between mb-1">
              <span className="font-bold text-white">{e.entity_id}</span>
              <span className="text-xs text-yellow-400/60">{e.region}</span>
            </div>
            <div className="text-xs text-slate-500 mb-2 capitalize">{e.creative_sector.replace(/_/g, " ")}</div>
            <div className="flex gap-1 mb-3 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[e.risk_level] || "bg-slate-700 text-slate-300"}`}>
                {e.risk_level}
              </span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[e.severity] || "bg-slate-700 text-slate-300"}`}>
                {e.severity.replace(/_/g, " ")}
              </span>
            </div>
            <div className="text-2xl font-black text-white mb-1">{e.composite_score.toFixed(1)}</div>
            <div className="text-xs text-yellow-400/60 mb-2 capitalize">{e.genai_pattern.replace(/_/g, " ")}</div>
            <div className="text-xs text-violet-400 font-medium mb-2">
              Déplacement: {e.displacement_score.toFixed(1)}
            </div>
            <div className="text-xs text-slate-400 truncate">{e.signal}</div>
          </div>
        ))}
      </div>
    </div>
  );
}
