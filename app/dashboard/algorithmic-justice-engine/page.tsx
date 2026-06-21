"use client";
import { useEffect, useState } from "react";

type Entity = {
  id: string;
  justice_domain: string;
  region: string;
  recidivism_AI_racial_bias_index: number;
  pretrial_detention_algorithmic_amplification: number;
  sentencing_AI_disparity_rate: number;
  parole_AI_discrimination_index: number;
  predictive_policing_racial_profiling: number;
  facial_recognition_justice_error_rate: number;
  algorithmic_opacity_in_courts: number;
  AI_due_process_violation_rate: number;
  criminal_justice_AI_accountability_gap: number;
  poverty_AI_bias_amplification: number;
  immigration_AI_detention_bias: number;
  data_quality_justice_impact: number;
  AI_legal_representation_inequality: number;
  wrongful_conviction_AI_contribution: number;
  justice_outcome_wealth_AI_correlation: number;
  AI_rehabilitation_assessment_bias: number;
  systemic_racism_AI_reproduction: number;
  bias_score: number;
  opacity_score: number;
  discrimination_score: number;
  systemic_score: number;
  composite_score: number;
  risk_level: string;
  justice_pattern: string;
  severity: string;
  recommended_action: string;
  signal: string;
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
  avg_estimated_justice_bias_index: number;
  avg_recidivism_AI_racial_bias: number;
};

function GaugeRing({ value, label, color }: { value: number; label: string; color: string }) {
  const r = 36;
  const circ = 2 * Math.PI * r;
  const fill = circ * (1 - value / 100);
  return (
    <div className="flex flex-col items-center gap-1">
      <svg width="88" height="88" viewBox="0 0 88 88">
        <circle cx="44" cy="44" r={r} fill="none" stroke="#1e293b" strokeWidth="8" />
        <circle
          cx="44" cy="44" r={r} fill="none" stroke={color} strokeWidth="8"
          strokeDasharray={circ} strokeDashoffset={fill}
          strokeLinecap="round" transform="rotate(-90 44 44)"
        />
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
          <div
            key={k}
            style={{ width: `${(v / total) * 100}%`, background: colors[k] || "#475569" }}
            title={`${k}: ${v}`}
          />
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

const RISK_COLORS: Record<string, string> = {
  low:      "#10b981",
  moderate: "#f59e0b",
  high:     "#f97316",
  critical: "#ef4444",
};
const PAT_COLORS: Record<string, string> = {
  none:                         "#10b981",
  racial_algorithm_bias:        "#ef4444",
  justice_opacity_crisis:       "#dc2626",
  poverty_discrimination_cascade: "#b91c1c",
  wrongful_AI_conviction:       "#6d28d9",
  predictive_persecution:       "#7c3aed",
};
const SEV_COLORS: Record<string, string> = {
  biais_algorithmique_contenu:          "#10b981",
  discrimination_algorithmique_active:  "#f59e0b",
  "biais_judiciaire_IA_majeur":         "#f97316",
  "injustice_algorithmique_systémique": "#ef4444",
};
const ACT_COLORS: Record<string, string> = {
  veille_biais_judiciaire_IA:             "#10b981",
  "renforcement_équité_algorithmique":    "#f59e0b",
  "audit_systémique_IA_judiciaire":       "#f97316",
  "réforme_urgente_justice_algorithmique": "#ef4444",
};
const RISK_BADGE: Record<string, string> = {
  low:      "bg-emerald-900 text-emerald-300",
  moderate: "bg-amber-900 text-amber-300",
  high:     "bg-orange-900 text-orange-300",
  critical: "bg-red-900 text-red-300",
};
const PAT_BADGE: Record<string, string> = {
  none:                         "bg-slate-800 text-slate-400",
  racial_algorithm_bias:        "bg-red-900 text-red-300",
  justice_opacity_crisis:       "bg-rose-900 text-rose-300",
  poverty_discrimination_cascade: "bg-red-950 text-red-400",
  wrongful_AI_conviction:       "bg-violet-900 text-violet-300",
  predictive_persecution:       "bg-purple-900 text-purple-300",
};

function DetailModal({ entity, onClose }: { entity: Entity; onClose: () => void }) {
  const [tab, setTab] = useState<"scores" | "signal" | "action">("scores");

  useEffect(() => {
    const h = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", h);
    return () => window.removeEventListener("keydown", h);
  }, [onClose]);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70" onClick={onClose}>
      <div
        className="bg-slate-900 border border-slate-700 rounded-xl w-full max-w-lg p-6 shadow-2xl"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="flex items-center justify-between mb-4">
          <div>
            <span className="text-lg font-bold text-white">{entity.id}</span>
            <span className="ml-2 text-slate-400 text-sm capitalize">
              {entity.justice_domain.replace(/_/g, " ")}
            </span>
            <span className="ml-2 text-indigo-400 text-xs">{entity.region}</span>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl leading-none">✕</button>
        </div>

        <div className="flex gap-2 mb-4">
          {(["scores", "signal", "action"] as const).map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`px-3 py-1 rounded text-xs font-medium transition-colors ${
                tab === t ? "bg-indigo-800 text-white" : "bg-slate-800 text-slate-400 hover:text-white"
              }`}
            >
              {t === "scores" ? "Scores" : t === "signal" ? "Signal" : "Action"}
            </button>
          ))}
        </div>

        {tab === "scores" && (
          <div className="grid grid-cols-2 gap-3 text-sm">
            {[
              ["Biais",           entity.bias_score,           "#ef4444"],
              ["Opacité",         entity.opacity_score,        "#dc2626"],
              ["Discrimination",  entity.discrimination_score, "#6d28d9"],
              ["Systémique",      entity.systemic_score,       "#b91c1c"],
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
              <div className="text-slate-400 text-xs mb-1">Score Composite</div>
              <div className="text-white font-bold text-2xl">{entity.composite_score.toFixed(1)}</div>
            </div>
          </div>
        )}

        {tab === "signal" && (
          <div className="bg-slate-800 rounded-lg p-4 text-sm text-slate-200 leading-relaxed">
            {entity.signal}
            <div className="mt-3 flex gap-2 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[entity.risk_level] || "bg-slate-700 text-slate-300"}`}>
                {entity.risk_level}
              </span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${PAT_BADGE[entity.justice_pattern] || "bg-slate-700 text-slate-300"}`}>
                {entity.justice_pattern.replace(/_/g, " ")}
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
              <div className="text-slate-400 text-xs mb-1">Sévérité</div>
              <div className="text-white font-medium">{entity.severity.replace(/_/g, " ")}</div>
            </div>
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Domaine Justice</div>
              <div className="text-white font-medium capitalize">{entity.justice_domain.replace(/_/g, " ")}</div>
            </div>
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Index Biais Récidivisme IA</div>
              <div className="text-white font-bold">{(entity.recidivism_AI_racial_bias_index * 100).toFixed(0)}%</div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function AlgorithmicJusticeDashboard() {
  const [data, setData]         = useState<{ entities: Entity[]; summary: Summary } | null>(null);
  const [filter, setFilter]     = useState<string>("all");
  const [patFilter, setPat]     = useState<string>("all");
  const [selected, setSelected] = useState<Entity | null>(null);

  useEffect(() => {
    fetch("/api/algorithmic-justice-engine")
      .then((r) => r.json())
      .then(setData)
      .catch(console.error);
  }, []);

  if (!data) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-indigo-400 text-lg animate-pulse">Chargement Justice Algorithmique...</div>
    </div>
  );

  const { entities, summary } = data;
  const filtered = entities.filter((e) =>
    (filter === "all" || e.risk_level === filter) &&
    (patFilter === "all" || e.justice_pattern === patFilter)
  );

  const avgBias           = entities.length > 0 ? entities.reduce((a, e) => a + e.bias_score, 0) / entities.length : 0;
  const avgOpacity        = entities.length > 0 ? entities.reduce((a, e) => a + e.opacity_score, 0) / entities.length : 0;
  const avgDiscrimination = entities.length > 0 ? entities.reduce((a, e) => a + e.discrimination_score, 0) / entities.length : 0;
  const avgSystemic       = entities.length > 0 ? entities.reduce((a, e) => a + e.systemic_score, 0) / entities.length : 0;

  const dists = [
    { title: "Risque",         counts: summary.risk_distribution,     colors: RISK_COLORS },
    { title: "Patron",         counts: summary.pattern_distribution,  colors: PAT_COLORS  },
    { title: "Sévérité",       counts: summary.severity_distribution, colors: SEV_COLORS  },
    { title: "Action",         counts: summary.action_distribution,   colors: ACT_COLORS  },
  ] as Array<{ title: string; counts: Record<string, number>; colors: Record<string, string> }>;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {selected && <DetailModal entity={selected} onClose={() => setSelected(null)} />}

      <div>
        <h1 className="text-2xl font-bold text-white">
          Justice Algorithmique &amp; Biais IA Judiciaire — Module 346
        </h1>
        <p className="text-slate-400 text-sm mt-1">
          Biais · Opacité · Discrimination · Systémique — analyse systémique du biais algorithmique judiciaire
        </p>
      </div>

      {/* KPI cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {[
          ["Total Systèmes",          summary.total_entities,                                              "text-indigo-400"],
          ["Injustice Systémique",    summary.critical_count,                                              "text-red-500"],
          ["Biais Majeur",            summary.high_count,                                                  "text-orange-400"],
          ["Composite Moyen",         summary.avg_composite.toFixed(1),                                    "text-slate-300"],
          ["Index Biais Judiciaire",  `${summary.avg_estimated_justice_bias_index.toFixed(2)}/10`,         "text-indigo-400"],
          ["Biais Moyen",             `${Math.round(avgBias)}`,                                            "text-red-300"],
        ].map(([l, v, c]) => (
          <div key={String(l)} className="bg-slate-900 border border-slate-800 rounded-xl p-3 text-center">
            <div className={`text-xl font-bold ${c}`}>{v}</div>
            <div className="text-xs text-slate-500 mt-0.5">{l}</div>
          </div>
        ))}
      </div>

      {/* Gauge rings */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
        <div className="grid grid-cols-4 gap-4">
          <GaugeRing value={avgBias}           label="Biais"           color="#ef4444" />
          <GaugeRing value={avgOpacity}        label="Opacité"         color="#6d28d9" />
          <GaugeRing value={avgDiscrimination} label="Discrimination"  color="#dc2626" />
          <GaugeRing value={avgSystemic}       label="Systémique"      color="#b91c1c" />
        </div>
      </div>

      {/* Distribution bars */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 grid grid-cols-1 md:grid-cols-2 gap-5">
        {dists.map((d) => <DistBar key={d.title} {...d} />)}
      </div>

      {/* Filter pills */}
      <div className="flex flex-wrap gap-2">
        {["all", "low", "moderate", "high", "critical"].map((r) => (
          <button
            key={r}
            onClick={() => setFilter(r)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${
              filter === r
                ? "bg-indigo-800 border-indigo-700 text-white"
                : "bg-slate-900 border-slate-700 text-slate-400 hover:text-white"
            }`}
          >
            {r === "all" ? "Tous" : r}
          </button>
        ))}
        <span className="w-px h-5 self-center bg-slate-700" />
        {["all", "none", "racial_algorithm_bias", "justice_opacity_crisis", "poverty_discrimination_cascade", "wrongful_AI_conviction", "predictive_persecution"].map((p) => (
          <button
            key={p}
            onClick={() => setPat(p)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${
              patFilter === p
                ? "bg-indigo-800 border-indigo-700 text-white"
                : "bg-slate-900 border-slate-700 text-slate-400 hover:text-white hover:border-indigo-700"
            }`}
          >
            {p === "all" ? "Tous patrons" : p.replace(/_/g, " ")}
          </button>
        ))}
      </div>

      {/* Entity cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {filtered.map((e) => (
          <div
            key={e.id}
            onClick={() => setSelected(e)}
            className="bg-slate-900 border border-slate-800 rounded-xl p-4 cursor-pointer hover:border-indigo-700 transition-colors"
          >
            <div className="flex items-center justify-between mb-1">
              <span className="font-bold text-white">{e.id}</span>
              <span className="text-xs text-slate-400">{e.region}</span>
            </div>
            <div className="text-xs text-indigo-400 mb-2 capitalize">
              {e.justice_domain.replace(/_/g, " ")}
            </div>
            <div className="flex gap-1 mb-3 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[e.risk_level] || "bg-slate-700 text-slate-300"}`}>
                {e.risk_level}
              </span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${PAT_BADGE[e.justice_pattern] || "bg-slate-700 text-slate-300"}`}>
                {e.justice_pattern.replace(/_/g, " ")}
              </span>
            </div>
            <div className="text-2xl font-black text-white mb-1">{e.composite_score.toFixed(1)}</div>
            <div className="text-xs text-slate-500 mb-2 capitalize">{e.severity.replace(/_/g, " ")}</div>
            <div className="text-xs text-red-400 font-medium mb-2">
              Récidivisme IA: {(e.recidivism_AI_racial_bias_index * 100).toFixed(0)}%
            </div>
            <div className="text-xs text-slate-400 leading-snug line-clamp-2">{e.signal}</div>
          </div>
        ))}
      </div>
    </div>
  );
}
