"use client";
import { useEffect, useState } from "react";

type DemocracyEntity = {
  id: string;
  governance_domain: string;
  region: string;
  risk_level: string;
  democracy_pattern: string;
  severity: string;
  recommended_action: string;
  exclusion_score: number;
  manipulation_score: number;
  accountability_score: number;
  sovereignty_score: number;
  composite_score: number;
  signal: string;
  e_voting_integrity_risk: number;
  open_data_governance_level: number;
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
  avg_estimated_democracy_risk_index: number;
  avg_exclusion_score: number;
};

function GaugeRing({ value, label, color }: { value: number; label: string; color: string }) {
  const r = 36;
  const circ = 2 * Math.PI * r;
  const fill = circ * (1 - value / 100);
  return (
    <div className="flex flex-col items-center gap-1">
      <svg width="88" height="88" viewBox="0 0 88 88">
        <circle cx="44" cy="44" r={r} fill="none" stroke="#1e293b" strokeWidth="8" />
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
  algorithmic_autocracy: "#ef4444",
  digital_disenfranchisement: "#a855f7",
  electoral_subversion: "#dc2626",
  surveillance_democracy: "#f97316",
  platform_sovereignty_capture: "#3b82f6",
};
const SEV_COLORS = {
  gouvernance_stable: "#10b981",
  "fragilité_gouvernance": "#f59e0b",
  "risque_démocratique_élevé": "#f97316",
  "démocratie_numérique_compromise": "#ef4444",
};
const ACT_COLORS = {
  surveillance_continue: "#10b981",
  "renforcement_oversight_numérique": "#06b6d4",
  "réforme_gouvernance_algorithmique": "#f97316",
  "intervention_démocratique_urgente": "#ef4444",
};
const RISK_BADGE = {
  low: "bg-emerald-900 text-emerald-300",
  moderate: "bg-amber-900 text-amber-300",
  high: "bg-orange-900 text-orange-300",
  critical: "bg-red-900 text-red-300",
};
const SEV_BADGE = {
  gouvernance_stable: "bg-emerald-900 text-emerald-300",
  "fragilité_gouvernance": "bg-amber-900 text-amber-300",
  "risque_démocratique_élevé": "bg-orange-900 text-orange-300",
  "démocratie_numérique_compromise": "bg-red-900 text-red-300",
};

function DetailModal({ entity, onClose }: { entity: DemocracyEntity; onClose: () => void }) {
  const [tab, setTab] = useState<"scores" | "signal" | "action">("scores");
  useEffect(() => {
    const h = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", h);
    return () => window.removeEventListener("keydown", h);
  }, [onClose]);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70" onClick={onClose}>
      <div className="bg-slate-900 border border-blue-800/40 rounded-xl w-full max-w-lg p-6 shadow-2xl" onClick={e => e.stopPropagation()}>
        <div className="flex items-center justify-between mb-4">
          <div>
            <span className="text-lg font-bold text-white">{entity.id}</span>
            <span className="ml-2 text-blue-400 text-xs">{entity.governance_domain.replace(/_/g, " ")}</span>
            <span className="ml-2 text-slate-400 text-xs">{entity.region}</span>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl leading-none">✕</button>
        </div>
        <div className="flex gap-2 mb-4">
          {(["scores", "signal", "action"] as const).map(t => (
            <button key={t} onClick={() => setTab(t)}
              className={`px-3 py-1 rounded text-xs font-medium transition-colors ${tab === t ? "bg-blue-700 text-white" : "bg-slate-800 text-slate-400 hover:text-white"}`}>
              {t === "scores" ? "Scores" : t === "signal" ? "Signal" : "Action"}
            </button>
          ))}
        </div>

        {tab === "scores" && (
          <div className="grid grid-cols-2 gap-3 text-sm">
            {[
              ["Score Exclusion",       entity.exclusion_score,       "#a855f7"],
              ["Score Manipulation",    entity.manipulation_score,    "#ef4444"],
              ["Score Responsabilité",  entity.accountability_score,  "#f97316"],
              ["Score Souveraineté",    entity.sovereignty_score,     "#3b82f6"],
            ].map(([l, v, c]) => (
              <div key={String(l)} className="bg-slate-800 rounded-lg p-3">
                <div className="text-slate-400 text-xs mb-1">{String(l)}</div>
                <div className="text-white font-bold text-lg">{Number(v).toFixed(1)}</div>
                <div className="h-1.5 rounded mt-1 bg-slate-700">
                  <div className="h-1.5 rounded" style={{ width: `${Math.min(Number(v), 100)}%`, background: String(c) }} />
                </div>
              </div>
            ))}
            <div className="col-span-2 bg-slate-800 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Score Composite Démocratie</div>
              <div className="text-white font-bold text-2xl">{entity.composite_score.toFixed(1)}</div>
            </div>
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Risque Vote Électronique</div>
              <div className="text-white font-bold">{(entity.e_voting_integrity_risk * 100).toFixed(0)}%</div>
            </div>
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Gouvernance Open Data</div>
              <div className="text-white font-bold">{(entity.open_data_governance_level * 100).toFixed(0)}%</div>
            </div>
          </div>
        )}

        {tab === "signal" && (
          <div className="bg-slate-800 rounded-lg p-4 text-sm text-slate-200 leading-relaxed">
            {entity.signal}
            <div className="mt-3 flex gap-2 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[entity.risk_level as keyof typeof RISK_BADGE] || "bg-slate-700 text-slate-300"}`}>
                {entity.risk_level}
              </span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[entity.severity as keyof typeof SEV_BADGE] || "bg-slate-700 text-slate-300"}`}>
                {entity.severity.replace(/_/g, " ")}
              </span>
              <span className="px-2 py-0.5 rounded text-xs font-medium bg-indigo-900 text-indigo-300">
                {entity.democracy_pattern.replace(/_/g, " ")}
              </span>
            </div>
          </div>
        )}

        {tab === "action" && (
          <div className="space-y-3 text-sm">
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Action Recommandée</div>
              <div className="text-white font-medium">{entity.recommended_action.replace(/_/g, " ")}</div>
            </div>
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Patron Démocratique Détecté</div>
              <div className="text-indigo-300 font-medium capitalize">{entity.democracy_pattern.replace(/_/g, " ")}</div>
            </div>
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Sévérité</div>
              <div className="text-white font-medium">{entity.severity.replace(/_/g, " ")}</div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function DigitalDemocracyDashboard() {
  const [data, setData]         = useState<{ entities: DemocracyEntity[]; summary: Summary } | null>(null);
  const [filter, setFilter]     = useState<string>("all");
  const [patFilter, setPatFilter] = useState<string>("all");
  const [selected, setSelected] = useState<DemocracyEntity | null>(null);

  useEffect(() => {
    fetch("/api/digital-democracy-engine")
      .then(r => r.json())
      .then(setData)
      .catch(console.error);
  }, []);

  if (!data) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-blue-400 text-lg animate-pulse">Initialisation du Moteur Démocratie Numérique...</div>
    </div>
  );

  const { entities, summary } = data;
  const n = entities.length || 1;
  const avgManipulation    = entities.reduce((s, e) => s + e.manipulation_score, 0) / n;
  const avgAccountability  = entities.reduce((s, e) => s + e.accountability_score, 0) / n;
  const avgSovereignty     = entities.reduce((s, e) => s + e.sovereignty_score, 0) / n;

  const filtered = entities.filter(e =>
    (filter === "all" || e.risk_level === filter) &&
    (patFilter === "all" || e.democracy_pattern === patFilter)
  );

  const dists = [
    { title: "Niveau de Risque",          counts: summary.risk_distribution,     colors: RISK_COLORS },
    { title: "Patron Démocratique",       counts: summary.pattern_distribution,  colors: PAT_COLORS  },
    { title: "Sévérité Gouvernance",      counts: summary.severity_distribution, colors: SEV_COLORS  },
    { title: "Action Recommandée",        counts: summary.action_distribution,   colors: ACT_COLORS  },
  ] as Array<{ title: string; counts: Record<string, number>; colors: Record<string, string> }>;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {selected && <DetailModal entity={selected} onClose={() => setSelected(null)} />}

      <div>
        <h1 className="text-2xl font-bold text-blue-400">Démocratie Numérique &amp; Gouvernance Algorithmique — Module 330</h1>
        <p className="text-slate-400 text-sm mt-1">Exclusion Numérique · Manipulation Électorale · Responsabilité Algorithmique · Souveraineté Numérique</p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {[
          ["Total Systèmes",          summary.total_entities,                                          "text-slate-300"],
          ["Démocratie Compromise",   summary.critical_count,                                          "text-red-400"],
          ["Risque Élevé",            summary.high_count,                                              "text-orange-400"],
          ["Composite Moyen",         summary.avg_composite.toFixed(1),                                "text-blue-400"],
          ["Index Risque Démocratie", summary.avg_estimated_democracy_risk_index.toFixed(2),           "text-indigo-400"],
          ["Exclusion Moyenne",       summary.avg_exclusion_score?.toFixed(1) ?? "—",                  "text-purple-400"],
        ].map(([l, v, c]) => (
          <div key={String(l)} className="bg-slate-900 border border-blue-900/40 rounded-xl p-3 text-center">
            <div className={`text-xl font-bold ${c}`}>{v}</div>
            <div className="text-xs text-slate-500 mt-0.5 leading-tight">{l}</div>
          </div>
        ))}
      </div>

      {/* Gauge Rings */}
      <div className="bg-slate-900 border border-blue-900/40 rounded-xl p-5">
        <div className="grid grid-cols-4 gap-4">
          <GaugeRing value={summary.avg_exclusion_score ?? 0} label="Exclusion"        color="#a855f7" />
          <GaugeRing value={avgManipulation}                  label="Manipulation"     color="#ef4444" />
          <GaugeRing value={avgAccountability}                label="Responsabilité"   color="#f97316" />
          <GaugeRing value={avgSovereignty}                   label="Souveraineté"     color="#3b82f6" />
        </div>
      </div>

      {/* Distribution Bars */}
      <div className="bg-slate-900 border border-blue-900/40 rounded-xl p-5 grid grid-cols-1 md:grid-cols-2 gap-5">
        {dists.map(d => <DistBar key={d.title} {...d} />)}
      </div>

      {/* Filter Pills */}
      <div className="flex flex-wrap gap-2">
        {["all", "low", "moderate", "high", "critical"].map(r => (
          <button key={r} onClick={() => setFilter(r)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${filter === r ? "bg-blue-700 border-blue-600 text-white" : "bg-slate-900 border-blue-900/40 text-slate-400 hover:text-white"}`}>
            {r}
          </button>
        ))}
        <span className="w-px h-5 self-center bg-blue-900/40" />
        {["all", "none", "algorithmic_autocracy", "digital_disenfranchisement", "electoral_subversion", "surveillance_democracy", "platform_sovereignty_capture"].map(p => (
          <button key={p} onClick={() => setPatFilter(p)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${patFilter === p ? "bg-indigo-800 border-indigo-700 text-white" : "bg-slate-900 border-blue-900/40 text-slate-400 hover:text-white"}`}>
            {p.replace(/_/g, " ")}
          </button>
        ))}
      </div>

      {/* Entity Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {filtered.map(e => (
          <div key={e.id} onClick={() => setSelected(e)}
            className="bg-slate-900 border border-blue-900/40 rounded-xl p-4 cursor-pointer hover:border-blue-500 transition-colors">
            <div className="flex items-center justify-between mb-1">
              <span className="font-bold text-white">{e.id}</span>
              <span className="text-xs text-slate-400">{e.region}</span>
            </div>
            <div className="text-xs text-blue-400 mb-2 capitalize">{e.governance_domain.replace(/_/g, " ")}</div>
            <div className="flex gap-1 mb-3 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[e.risk_level as keyof typeof RISK_BADGE] || "bg-slate-700 text-slate-300"}`}>
                {e.risk_level}
              </span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[e.severity as keyof typeof SEV_BADGE] || "bg-slate-700 text-slate-300"}`}>
                {e.severity.replace(/_/g, " ")}
              </span>
            </div>
            <div className="text-2xl font-black text-white mb-1">{e.composite_score.toFixed(1)}</div>
            <div className="text-xs text-indigo-400 mb-2 capitalize">{e.democracy_pattern.replace(/_/g, " ")}</div>
            <div className="text-xs text-slate-400 leading-snug line-clamp-2">{e.signal}</div>
            <div className="mt-2 grid grid-cols-2 gap-1 text-xs text-slate-500">
              <span>Excl: {e.exclusion_score.toFixed(1)}</span>
              <span>Manip: {e.manipulation_score.toFixed(1)}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
