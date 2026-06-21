"use client";
import { useEffect, useState } from "react";

type DCEEntity = {
  id: string;
  tech_domain: string;
  region: string;
  dependency_score: number;
  extraction_score: number;
  sovereignty_score: number;
  exclusion_score: number;
  composite_score: number;
  risk_level: string;
  colonial_pattern: string;
  severity: string;
  recommended_action: string;
  signal: string;
  platform_dependency_ratio: number;
  data_localization_failure: number;
};

type Summary = {
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
  avg_estimated_digital_colonial_index: number;
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
      <span className="text-xs text-slate-400 text-center">{label}</span>
    </div>
  );
}

function DistBar({ title, counts, colors }: { title: string; counts: Record<string, number>; colors: Record<string, string> }) {
  const total = Object.values(counts).reduce((a, b) => a + b, 0) || 1;
  return (
    <div className="flex flex-col gap-1">
      <span className="text-xs text-slate-400 font-medium">{title}</span>
      <div className="flex h-3 rounded overflow-hidden gap-px">
        {Object.entries(counts).map(([k, v]) => (
          <div key={k} style={{ width: `${(v / total) * 100}%`, background: colors[k] || "#475569" }} title={`${k}: ${v}`} />
        ))}
      </div>
      <div className="flex flex-wrap gap-x-3 gap-y-0.5">
        {Object.entries(counts).map(([k, v]) => (
          <span key={k} className="text-xs text-slate-400">
            <span style={{ color: colors[k] || "#94a3b8" }}>■</span> {k.replace(/_/g, " ")} {v}
          </span>
        ))}
      </div>
    </div>
  );
}

const RISK_COLORS = { low: "#10b981", moderate: "#f59e0b", high: "#f97316", critical: "#ef4444" };
const PAT_COLORS: Record<string, string> = {
  none:                           "#10b981",
  platform_imperial_capture:      "#ef4444",
  data_extraction_empire:         "#f97316",
  AI_dependency_trap_system:      "#dc2626",
  surveillance_export_colonialism:"#b91c1c",
  digital_divide_structural:      "#f59e0b",
};
const SEV_COLORS: Record<string, string> = {
  "souveraineté_tech_relative":           "#10b981",
  "erosion_autonomie_numérique":          "#f59e0b",
  "crise_souveraineté_tech_majeure":      "#f97316",
  "colonialisme_numérique_systémique":    "#ef4444",
};
const ACT_COLORS: Record<string, string> = {
  "veille_souveraineté_numérique_continue":          "#10b981",
  "renforcement_industrie_numérique_locale":         "#f59e0b",
  "stratégie_souveraineté_tech_accélérée":           "#f97316",
  "intervention_décolonisation_numérique_urgente":   "#ef4444",
};
const RISK_BADGE: Record<string, string> = {
  low:      "bg-emerald-900 text-emerald-300",
  moderate: "bg-amber-900 text-amber-300",
  high:     "bg-orange-900 text-orange-300",
  critical: "bg-red-900 text-red-300",
};
const SEV_BADGE: Record<string, string> = {
  "souveraineté_tech_relative":        "bg-emerald-900 text-emerald-300",
  "erosion_autonomie_numérique":       "bg-amber-900 text-amber-300",
  "crise_souveraineté_tech_majeure":   "bg-orange-900 text-orange-300",
  "colonialisme_numérique_systémique": "bg-red-900 text-red-300",
};

function DetailModal({ entity, onClose }: { entity: DCEEntity; onClose: () => void }) {
  const [tab, setTab] = useState<"scores" | "signal" | "action">("scores");

  useEffect(() => {
    const h = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", h);
    return () => window.removeEventListener("keydown", h);
  }, [onClose]);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70" onClick={onClose}>
      <div className="bg-slate-900 border border-slate-700 rounded-xl w-full max-w-lg p-6 shadow-2xl" onClick={e => e.stopPropagation()}>
        <div className="flex items-center justify-between mb-4">
          <div>
            <span className="text-lg font-bold text-white">{entity.id}</span>
            <span className="ml-2 text-orange-400 text-xs">{entity.tech_domain.replace(/_/g, " ")}</span>
            <span className="ml-2 text-slate-400 text-xs">{entity.region}</span>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl leading-none">✕</button>
        </div>

        <div className="flex gap-2 mb-4">
          {(["scores", "signal", "action"] as const).map(t => (
            <button key={t} onClick={() => setTab(t)}
              className={`px-3 py-1 rounded text-xs font-medium transition-colors ${tab === t ? "bg-orange-700 text-white" : "bg-slate-800 text-slate-400 hover:text-white"}`}>
              {t === "scores" ? "Scores" : t === "signal" ? "Signal" : "Action"}
            </button>
          ))}
        </div>

        {tab === "scores" && (
          <div className="grid grid-cols-2 gap-3 text-sm">
            {([
              ["Dépendance",   entity.dependency_score,  "#f97316"],
              ["Extraction",   entity.extraction_score,  "#ef4444"],
              ["Souveraineté", entity.sovereignty_score, "#dc2626"],
              ["Exclusion",    entity.exclusion_score,   "#f59e0b"],
            ] as [string, number, string][]).map(([l, v, c]) => (
              <div key={l} className="bg-slate-800 rounded-lg p-3">
                <div className="text-slate-400 text-xs mb-1">{l}</div>
                <div className="text-white font-bold text-lg">{v.toFixed(1)}</div>
                <div className="h-1.5 rounded mt-1 bg-slate-700">
                  <div className="h-1.5 rounded" style={{ width: `${Math.min(v, 100)}%`, background: c }} />
                </div>
              </div>
            ))}
            <div className="col-span-2 bg-slate-800 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Score Composite Colonial</div>
              <div className="text-white font-bold text-2xl">{entity.composite_score.toFixed(1)}</div>
            </div>
            <div className="col-span-2 grid grid-cols-2 gap-2">
              <div className="bg-slate-800 rounded-lg p-2">
                <div className="text-slate-400 text-xs">Ratio Dépendance Plateforme</div>
                <div className="text-orange-300 font-bold">{(entity.platform_dependency_ratio * 100).toFixed(0)}%</div>
              </div>
              <div className="bg-slate-800 rounded-lg p-2">
                <div className="text-slate-400 text-xs">Échec Localisation Données</div>
                <div className="text-red-300 font-bold">{(entity.data_localization_failure * 100).toFixed(0)}%</div>
              </div>
            </div>
          </div>
        )}

        {tab === "signal" && (
          <div className="bg-slate-800 rounded-lg p-4 text-sm text-slate-200 leading-relaxed">
            <div className="text-base mb-3">{entity.signal}</div>
            <div className="flex gap-2 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[entity.risk_level] || "bg-slate-700 text-slate-300"}`}>
                {entity.risk_level}
              </span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[entity.severity] || "bg-slate-700 text-slate-300"}`}>
                {entity.severity.replace(/_/g, " ")}
              </span>
              <span className="px-2 py-0.5 rounded text-xs font-medium bg-slate-700 text-slate-300">
                {entity.colonial_pattern.replace(/_/g, " ")}
              </span>
            </div>
          </div>
        )}

        {tab === "action" && (
          <div className="space-y-3 text-sm">
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Action Recommandée</div>
              <div className="text-orange-300 font-medium">{entity.recommended_action.replace(/_/g, " ")}</div>
            </div>
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Sévérité</div>
              <div className="text-white font-medium">{entity.severity.replace(/_/g, " ")}</div>
            </div>
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Domaine Tech</div>
              <div className="text-orange-300 font-medium">{entity.tech_domain.replace(/_/g, " ")}</div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function DigitalColonialismDashboard() {
  const [data, setData]           = useState<{ entities: DCEEntity[]; summary: Summary } | null>(null);
  const [filter, setFilter]       = useState<string>("all");
  const [patFilter, setPatFilter] = useState<string>("all");
  const [selected, setSelected]   = useState<DCEEntity | null>(null);

  useEffect(() => {
    fetch("/api/digital-colonialism-engine")
      .then(r => r.json())
      .then(setData)
      .catch(console.error);
  }, []);

  if (!data) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-orange-400 text-lg animate-pulse">Chargement Colonialisme Numérique — Module 371…</div>
    </div>
  );

  const { entities, summary } = data;
  const filtered = entities.filter(e =>
    (filter === "all" || e.risk_level === filter) &&
    (patFilter === "all" || e.colonial_pattern === patFilter)
  );

  const avgDependency  = Math.round(entities.reduce((s, e) => s + e.dependency_score, 0) / (entities.length || 1) * 10) / 10;
  const avgExtraction  = Math.round(entities.reduce((s, e) => s + e.extraction_score, 0) / (entities.length || 1) * 10) / 10;
  const avgSovereignty = Math.round(entities.reduce((s, e) => s + e.sovereignty_score, 0) / (entities.length || 1) * 10) / 10;
  const avgExclusion   = Math.round(entities.reduce((s, e) => s + e.exclusion_score, 0) / (entities.length || 1) * 10) / 10;

  const dists = [
    { title: "Niveau de Risque",        counts: summary.risk_distribution,     colors: RISK_COLORS },
    { title: "Patron Colonial",          counts: summary.pattern_distribution,  colors: PAT_COLORS  },
    { title: "Sévérité",                 counts: summary.severity_distribution, colors: SEV_COLORS  },
    { title: "Action Recommandée",       counts: summary.action_distribution,   colors: ACT_COLORS  },
  ] as Array<{ title: string; counts: Record<string, number>; colors: Record<string, string> }>;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {selected && <DetailModal entity={selected} onClose={() => setSelected(null)} />}

      <div>
        <h1 className="text-2xl font-bold text-white">Colonialisme Numérique &amp; Souveraineté Tech — Module 371</h1>
        <p className="text-slate-400 text-sm mt-1">
          Capture impériale plateformes · Extraction données · Dépendance IA · Surveillance export · Fracture numérique
        </p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {([
          ["Total Marchés",             summary.total,                                          "text-slate-300"],
          ["Capture Impériale",         summary.critical,                                       "text-red-400"],
          ["Crise Majeure",             summary.high,                                           "text-orange-400"],
          ["Composite Moyen",           summary.avg_composite,                                  "text-indigo-300"],
          ["Index Colonial Numérique",  summary.avg_estimated_digital_colonial_index,           "text-orange-400"],
          ["Dépendance Moyenne",        avgDependency,                                          "text-amber-400"],
        ] as [string, number, string][]).map(([l, v, c]) => (
          <div key={l} className="bg-slate-900 border border-slate-800 rounded-xl p-3 text-center">
            <div className={`text-xl font-bold ${c}`}>{typeof v === "number" && !Number.isInteger(v) ? v.toFixed(1) : v}</div>
            <div className="text-xs text-slate-500 mt-0.5">{l}</div>
          </div>
        ))}
      </div>

      {/* Gauge Rings */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
        <div className="grid grid-cols-4 gap-4">
          <GaugeRing value={avgDependency}  label="Dépendance"   color="#f97316" />
          <GaugeRing value={avgExtraction}  label="Extraction"   color="#ef4444" />
          <GaugeRing value={avgSovereignty} label="Souveraineté" color="#dc2626" />
          <GaugeRing value={avgExclusion}   label="Exclusion"    color="#f59e0b" />
        </div>
      </div>

      {/* Distribution Bars */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 grid grid-cols-1 md:grid-cols-2 gap-5">
        {dists.map(d => <DistBar key={d.title} {...d} />)}
      </div>

      {/* Filter Pills */}
      <div className="flex flex-wrap gap-2">
        {["all", "low", "moderate", "high", "critical"].map(r => (
          <button key={r} onClick={() => setFilter(r)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${filter === r ? "bg-orange-700 border-orange-600 text-white" : "bg-slate-900 border-slate-700 text-slate-400 hover:text-white"}`}>
            {r}
          </button>
        ))}
        <span className="w-px h-5 self-center bg-slate-700" />
        {["all", "platform_imperial_capture", "data_extraction_empire", "AI_dependency_trap_system", "surveillance_export_colonialism", "digital_divide_structural", "none"].map(p => (
          <button key={p} onClick={() => setPatFilter(p)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${patFilter === p ? "bg-slate-700 border-slate-600 text-white" : "bg-slate-900 border-slate-700 text-slate-400 hover:text-white"}`}>
            {p.replace(/_/g, " ")}
          </button>
        ))}
      </div>

      {/* Entity Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {filtered.map(e => (
          <div key={e.id} onClick={() => setSelected(e)}
            className="bg-slate-900 border border-slate-800 rounded-xl p-4 cursor-pointer hover:border-orange-700 transition-colors">
            <div className="flex items-center justify-between mb-1">
              <span className="font-bold text-white">{e.id}</span>
              <span className="text-xs text-slate-400">{e.region}</span>
            </div>
            <div className="text-xs text-orange-400 mb-2">{e.tech_domain.replace(/_/g, " ")}</div>
            <div className="flex gap-1 mb-3 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[e.risk_level] || "bg-slate-700 text-slate-300"}`}>
                {e.risk_level}
              </span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[e.severity] || "bg-slate-700 text-slate-300"}`}>
                {e.severity.replace(/_/g, " ")}
              </span>
            </div>
            <div className="text-2xl font-black text-white mb-1">{e.composite_score.toFixed(1)}</div>
            <div className="text-xs text-slate-500 mb-2 capitalize">{e.colonial_pattern.replace(/_/g, " ")}</div>
            <div className="grid grid-cols-2 gap-1 mb-2">
              <div className="text-xs text-orange-400">Dép: {e.dependency_score.toFixed(0)}</div>
              <div className="text-xs text-red-400">Ext: {e.extraction_score.toFixed(0)}</div>
              <div className="text-xs text-rose-400">Souv: {e.sovereignty_score.toFixed(0)}</div>
              <div className="text-xs text-amber-400">Excl: {e.exclusion_score.toFixed(0)}</div>
            </div>
            <div className="text-xs text-slate-400 leading-snug line-clamp-2">{e.signal}</div>
          </div>
        ))}
      </div>
    </div>
  );
}
