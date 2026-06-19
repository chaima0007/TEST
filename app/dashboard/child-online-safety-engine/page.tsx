"use client";
import { useEffect, useState } from "react";

type CSEEntity = {
  entity_id: string;
  platform_type: string;
  region: string;
  predation_score: number;
  content_score: number;
  platform_score: number;
  governance_score: number;
  composite_score: number;
  risk_level: string;
  safety_pattern: string;
  severity: string;
  recommended_action: string;
  signal: string;
  predator_network_density: number;
  csam_detection_gap: number;
};

type CSESummary = {
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
  avg_estimated_child_digital_safety_index: number;
};

function GaugeRing({ value, label, color }: { value: number; label: string; color: string }) {
  const r = 36;
  const circ = 2 * Math.PI * r;
  const fill = circ * (1 - value / 100);
  return (
    <div className="flex flex-col items-center gap-1">
      <svg width="88" height="88" viewBox="0 0 88 88">
        <circle cx="44" cy="44" r={r} fill="none" stroke="#0c1521" strokeWidth="8" />
        <circle
          cx="44" cy="44" r={r} fill="none" stroke={color} strokeWidth="8"
          strokeDasharray={circ} strokeDashoffset={fill}
          strokeLinecap="round" transform="rotate(-90 44 44)"
        />
        <text x="44" y="49" textAnchor="middle" fill="white" fontSize="13" fontWeight="bold">
          {Math.round(value)}
        </text>
      </svg>
      <span className="text-xs text-rose-500/70 text-center">{label}</span>
    </div>
  );
}

function DistBar({
  title,
  counts,
  colors,
}: {
  title: string;
  counts: Record<string, number>;
  colors: Record<string, string>;
}) {
  const total = Object.values(counts).reduce((a, b) => a + b, 0) || 1;
  return (
    <div className="flex flex-col gap-1">
      <span className="text-xs text-rose-500/70 font-medium">{title}</span>
      <div className="flex h-3 rounded overflow-hidden gap-px">
        {Object.entries(counts).map(([k, v]) => (
          <div
            key={k}
            style={{ width: `${(v / total) * 100}%`, background: colors[k] || "#9f1239" }}
            title={`${k}: ${v}`}
          />
        ))}
      </div>
      <div className="flex flex-wrap gap-x-3 gap-y-0.5">
        {Object.entries(counts).map(([k, v]) => (
          <span key={k} className="text-xs text-rose-500/60">
            <span style={{ color: colors[k] || "#be123c" }}>■</span> {k.replace(/_/g, " ")} {v}
          </span>
        ))}
      </div>
    </div>
  );
}

const RISK_COLORS: Record<string, string> = {
  low: "#16a34a",
  moderate: "#d97706",
  high: "#92400e",
  critical: "#dc2626",
};
const PATTERN_COLORS: Record<string, string> = {
  none: "#16a34a",
  grooming_network_proliferation: "#dc2626",
  csam_distribution_infrastructure: "#7c3aed",
  algorithmic_radicalization_youth: "#0891b2",
  sextortion_epidemic: "#b45309",
  platform_moderation_failure: "#be123c",
};
const SEVERITY_COLORS: Record<string, string> = {
  "surveillance_sécurité_enfants_active": "#16a34a",
  "vulnérabilité_numérique_structurelle": "#d97706",
  "crise_sécurité_numérique_majeure": "#92400e",
  "crise_protection_enfants_systémique": "#dc2626",
};
const ACTION_COLORS: Record<string, string> = {
  "veille_sécurité_numérique_continue": "#16a34a",
  "amélioration_mécanismes_signalement_enfants": "#d97706",
  "renforcement_immédiat_modération_plateforme": "#92400e",
  "intervention_urgente_protection_enfants_critique": "#dc2626",
};
const RISK_BADGE: Record<string, string> = {
  low: "bg-green-900 text-green-300",
  moderate: "bg-amber-900 text-amber-300",
  high: "bg-amber-950 text-amber-500",
  critical: "bg-red-950 text-red-400",
};
const SEV_BADGE: Record<string, string> = {
  "surveillance_sécurité_enfants_active": "bg-green-900 text-green-300",
  "vulnérabilité_numérique_structurelle": "bg-amber-900 text-amber-300",
  "crise_sécurité_numérique_majeure": "bg-amber-950 text-amber-500",
  "crise_protection_enfants_systémique": "bg-red-950 text-red-400",
};

function DetailModal({ entity, onClose }: { entity: CSEEntity; onClose: () => void }) {
  const [tab, setTab] = useState<"scores" | "signal" | "action">("scores");

  useEffect(() => {
    const h = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
    };
    window.addEventListener("keydown", h);
    return () => window.removeEventListener("keydown", h);
  }, [onClose]);

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/80"
      onClick={onClose}
    >
      <div
        className="bg-slate-950 border border-rose-700/30 rounded-xl w-full max-w-lg p-6 shadow-2xl"
        onClick={e => e.stopPropagation()}
      >
        <div className="flex items-center justify-between mb-4">
          <div>
            <span className="text-lg font-bold text-white">{entity.entity_id}</span>
            <span className="ml-2 text-rose-500 text-xs">{entity.region}</span>
            <span className="ml-2 text-slate-500 text-xs">
              {entity.platform_type.replace(/_/g, " ")}
            </span>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl leading-none">
            ✕
          </button>
        </div>

        <div className="flex gap-2 mb-4">
          {(["scores", "signal", "action"] as const).map(t => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`px-3 py-1 rounded text-xs font-medium transition-colors ${
                tab === t
                  ? "bg-rose-900 text-white"
                  : "bg-slate-900 text-slate-400 hover:text-white"
              }`}
            >
              {t === "scores" ? "Scores" : t === "signal" ? "Signal" : "Action"}
            </button>
          ))}
        </div>

        {tab === "scores" && (
          <div className="grid grid-cols-2 gap-3 text-sm">
            {[
              ["Score Prédation",   entity.predation_score,  "#dc2626"],
              ["Score Contenu",     entity.content_score,    "#7c3aed"],
              ["Score Plateforme",  entity.platform_score,   "#0891b2"],
              ["Score Gouvernance", entity.governance_score, "#b45309"],
            ].map(([l, v, c]) => (
              <div
                key={String(l)}
                className="bg-slate-900 border border-rose-700/20 rounded-lg p-3"
              >
                <div className="text-rose-500/60 text-xs mb-1">{String(l)}</div>
                <div className="text-white font-bold text-lg">{Number(v).toFixed(1)}</div>
                <div className="h-1.5 rounded mt-1 bg-slate-800">
                  <div
                    className="h-1.5 rounded"
                    style={{ width: `${Math.min(Number(v), 100)}%`, background: String(c) }}
                  />
                </div>
              </div>
            ))}
            <div className="col-span-2 bg-slate-900 border border-rose-700/20 rounded-lg p-3">
              <div className="text-rose-500/60 text-xs mb-1">Score Composite Sécurité Enfants</div>
              <div className="text-white font-bold text-2xl">
                {entity.composite_score.toFixed(1)}
              </div>
            </div>
          </div>
        )}

        {tab === "signal" && (
          <div className="bg-slate-900 border border-rose-700/20 rounded-lg p-4 text-sm text-slate-200 leading-relaxed">
            {entity.signal}
            <div className="mt-3 flex gap-2 flex-wrap">
              <span
                className={`px-2 py-0.5 rounded text-xs font-medium ${
                  RISK_BADGE[entity.risk_level] || "bg-slate-700 text-slate-300"
                }`}
              >
                {entity.risk_level}
              </span>
              <span
                className={`px-2 py-0.5 rounded text-xs font-medium ${
                  SEV_BADGE[entity.severity] || "bg-slate-700 text-slate-300"
                }`}
              >
                {entity.severity.replace(/_/g, " ")}
              </span>
            </div>
            <div className="mt-3 grid grid-cols-2 gap-2">
              <div className="bg-slate-800 rounded p-2">
                <div className="text-rose-500/50 text-xs mb-0.5">Densité Réseau Prédateurs</div>
                <div className="text-white text-sm font-medium">
                  {Math.round(entity.predator_network_density * 100)}%
                </div>
              </div>
              <div className="bg-slate-800 rounded p-2">
                <div className="text-rose-500/50 text-xs mb-0.5">Gap Détection CSAM</div>
                <div className="text-white text-sm font-medium">
                  {Math.round(entity.csam_detection_gap * 100)}%
                </div>
              </div>
            </div>
          </div>
        )}

        {tab === "action" && (
          <div className="space-y-3 text-sm">
            <div className="bg-slate-900 border border-rose-700/20 rounded-lg p-3">
              <div className="text-rose-500/60 text-xs mb-1">Action Recommandée</div>
              <div className="text-white font-medium">
                {entity.recommended_action.replace(/_/g, " ")}
              </div>
            </div>
            <div className="bg-slate-900 border border-rose-700/20 rounded-lg p-3">
              <div className="text-rose-500/60 text-xs mb-1">Type de Plateforme</div>
              <div className="text-white font-medium capitalize">
                {entity.platform_type.replace(/_/g, " ")}
              </div>
            </div>
            <div className="bg-slate-900 border border-rose-700/20 rounded-lg p-3">
              <div className="text-rose-500/60 text-xs mb-1">Patron Détecté</div>
              <div className="text-red-400 font-medium capitalize">
                {entity.safety_pattern.replace(/_/g, " ")}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function ChildOnlineSafetyDashboard() {
  const [data, setData] = useState<{
    entities: CSEEntity[];
    summary: CSESummary;
    avg_predation: number;
  } | null>(null);
  const [riskFilter, setRiskFilter] = useState<string>("all");
  const [patFilter, setPatFilter] = useState<string>("all");
  const [selected, setSelected] = useState<CSEEntity | null>(null);

  useEffect(() => {
    fetch("/api/child-online-safety-engine")
      .then(r => r.json())
      .then(setData)
      .catch(console.error);
  }, []);

  if (!data) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center">
        <div className="text-rose-500 text-lg animate-pulse">
          Initialisation du Moteur Sécurité Enfants Numérique...
        </div>
      </div>
    );
  }

  const { entities, summary, avg_predation } = data;
  const filtered = entities.filter(
    e =>
      (riskFilter === "all" || e.risk_level === riskFilter) &&
      (patFilter === "all" || e.safety_pattern === patFilter)
  );

  const dists = [
    { title: "Niveau de Risque",       counts: summary.risk_distribution,     colors: RISK_COLORS     },
    { title: "Patron de Menace",       counts: summary.pattern_distribution,  colors: PATTERN_COLORS  },
    { title: "Sévérité",               counts: summary.severity_distribution, colors: SEVERITY_COLORS },
    { title: "Action Déclenchée",      counts: summary.action_distribution,   colors: ACTION_COLORS   },
  ] as Array<{ title: string; counts: Record<string, number>; colors: Record<string, string> }>;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {selected && <DetailModal entity={selected} onClose={() => setSelected(null)} />}

      <div>
        <h1 className="text-2xl font-bold text-rose-500">
          Sécurité Enfants Numérique &amp; Préjudices en Ligne — Module 436
        </h1>
        <p className="text-red-500/60 text-sm mt-1">
          Prédation · Contenu · Plateforme · Gouvernance — Caelum Partners — Chaima Mhadbi, Fondatrice, Bruxelles
        </p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {[
          ["Total Plateformes",             summary.total,                                                              "text-rose-500"],
          ["Crise Critique",                summary.critical,                                                           "text-red-400"],
          ["Risque Élevé",                  summary.high,                                                               "text-red-700"],
          ["Composite Moyen",               `${summary.avg_composite.toFixed(1)}`,                                      "text-rose-400"],
          ["Index Sécurité Enfants",        `${summary.avg_estimated_child_digital_safety_index.toFixed(2)}/10`,        "text-rose-500"],
          ["Prédation Moyenne",             `${avg_predation.toFixed(1)}`,                                              "text-red-400"],
        ].map(([l, v, c]) => (
          <div
            key={String(l)}
            className="bg-slate-900 border border-rose-700/30 rounded-xl p-3 text-center"
          >
            <div className={`text-xl font-bold ${c}`}>{v}</div>
            <div className="text-xs text-rose-500/40 mt-0.5 leading-tight">{l}</div>
          </div>
        ))}
      </div>

      {/* Gauge Rings */}
      <div className="bg-slate-900 border border-rose-700/30 rounded-xl p-5">
        <div className="grid grid-cols-4 gap-4">
          <GaugeRing
            value={entities.reduce((s, e) => s + e.predation_score, 0) / (entities.length || 1)}
            label="Prédation Moy."
            color="#dc2626"
          />
          <GaugeRing
            value={entities.reduce((s, e) => s + e.content_score, 0) / (entities.length || 1)}
            label="Contenu Moy."
            color="#7c3aed"
          />
          <GaugeRing
            value={entities.reduce((s, e) => s + e.platform_score, 0) / (entities.length || 1)}
            label="Plateforme Moy."
            color="#0891b2"
          />
          <GaugeRing
            value={entities.reduce((s, e) => s + e.governance_score, 0) / (entities.length || 1)}
            label="Gouvernance Moy."
            color="#b45309"
          />
        </div>
      </div>

      {/* Distribution Bars */}
      <div className="bg-slate-900 border border-rose-700/30 rounded-xl p-5 grid grid-cols-1 md:grid-cols-2 gap-5">
        {dists.map(d => (
          <DistBar key={d.title} {...d} />
        ))}
      </div>

      {/* Filter Pills */}
      <div className="flex flex-wrap gap-2">
        {["all", "low", "moderate", "high", "critical"].map(r => (
          <button
            key={r}
            onClick={() => setRiskFilter(r)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${
              riskFilter === r
                ? "bg-rose-900 border-rose-800 text-white"
                : "bg-slate-900 border-rose-700/30 text-rose-500/70 hover:text-white"
            }`}
          >
            {r}
          </button>
        ))}
        <span className="w-px h-5 self-center bg-rose-700/30" />
        {[
          "all",
          "none",
          "grooming_network_proliferation",
          "csam_distribution_infrastructure",
          "algorithmic_radicalization_youth",
          "sextortion_epidemic",
          "platform_moderation_failure",
        ].map(p => (
          <button
            key={p}
            onClick={() => setPatFilter(p)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${
              patFilter === p
                ? "bg-red-950 border-red-700 text-white"
                : "bg-slate-900 border-rose-700/30 text-rose-500/70 hover:text-white"
            }`}
          >
            {p.replace(/_/g, " ")}
          </button>
        ))}
      </div>

      {/* Entity Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {filtered.map(e => (
          <div
            key={e.entity_id}
            onClick={() => setSelected(e)}
            className="bg-slate-900 border border-rose-700/30 rounded-xl p-4 cursor-pointer hover:border-rose-600 transition-colors"
          >
            <div className="flex items-center justify-between mb-1">
              <span className="font-bold text-white">{e.entity_id}</span>
              <span className="text-xs text-rose-500/60">{e.region}</span>
            </div>
            <div className="text-xs text-slate-500 mb-2 capitalize">
              {e.platform_type.replace(/_/g, " ")}
            </div>
            <div className="flex gap-1 mb-3 flex-wrap">
              <span
                className={`px-2 py-0.5 rounded text-xs font-medium ${
                  RISK_BADGE[e.risk_level] || "bg-slate-700 text-slate-300"
                }`}
              >
                {e.risk_level}
              </span>
              <span
                className={`px-2 py-0.5 rounded text-xs font-medium ${
                  SEV_BADGE[e.severity] || "bg-slate-700 text-slate-300"
                }`}
              >
                {e.severity.replace(/_/g, " ")}
              </span>
            </div>
            <div className="text-2xl font-black text-white mb-1">
              {e.composite_score.toFixed(1)}
            </div>
            <div className="text-xs text-red-400/60 mb-2 capitalize">
              {e.safety_pattern.replace(/_/g, " ")}
            </div>
            <div className="text-xs text-rose-500/70 font-medium mb-2">
              Prédation: {e.predation_score.toFixed(1)} · Contenu: {e.content_score.toFixed(1)}
            </div>
            <div className="text-xs text-slate-400 truncate">{e.signal}</div>
          </div>
        ))}
      </div>
    </div>
  );
}
