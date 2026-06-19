"use client";
import { useEffect, useState } from "react";

type NPEEntity = {
  entity_id: string;
  urban_type: string;
  region: string;
  exposure_score: number;
  health_impact_score: number;
  inequality_score: number;
  governance_score: number;
  composite_score: number;
  risk_level: string;
  noise_pattern: string;
  severity: string;
  recommended_action: string;
  signal: string;
  noise_level_db: number;
  sleep_disruption: number;
};

type NPESummary = {
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
  avg_estimated_noise_health_index: number;
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
      <span className="text-xs text-yellow-500/70 text-center">{label}</span>
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
      <span className="text-xs text-yellow-500/70 font-medium">{title}</span>
      <div className="flex h-3 rounded overflow-hidden gap-px">
        {Object.entries(counts).map(([k, v]) => (
          <div
            key={k}
            style={{ width: `${(v / total) * 100}%`, background: colors[k] || "#78350f" }}
            title={`${k}: ${v}`}
          />
        ))}
      </div>
      <div className="flex flex-wrap gap-x-3 gap-y-0.5">
        {Object.entries(counts).map(([k, v]) => (
          <span key={k} className="text-xs text-yellow-500/60">
            <span style={{ color: colors[k] || "#92400e" }}>■</span> {k.replace(/_/g, " ")} {v}
          </span>
        ))}
      </div>
    </div>
  );
}

const RISK_COLORS: Record<string, string> = {
  low: "#16a34a",
  moderate: "#d97706",
  high: "#f59e0b",
  critical: "#dc2626",
};
const PATTERN_COLORS: Record<string, string> = {
  none: "#16a34a",
  chronic_cardiovascular_noise_crisis: "#dc2626",
  sleep_deprivation_pandemic: "#7c3aed",
  childhood_cognitive_impairment: "#0891b2",
  noise_poverty_inequality_trap: "#b45309",
  regulatory_enforcement_collapse: "#d97706",
};
const SEVERITY_COLORS: Record<string, string> = {
  "environnement_sonore_sous_surveillance": "#16a34a",
  "nuisance_sonore_structurelle": "#d97706",
  "crise_santé_urbaine_majeure": "#f59e0b",
  "crise_pollution_sonore_systémique": "#dc2626",
};
const ACTION_COLORS: Record<string, string> = {
  "veille_environnement_sonore_continue": "#16a34a",
  "renforcement_réglementation_acoustique_urbaine": "#d97706",
  "plan_réduction_bruit_accéléré_zones_vulnérables": "#f59e0b",
  "intervention_urgente_pollution_sonore_critique": "#dc2626",
};
const RISK_BADGE: Record<string, string> = {
  low: "bg-green-900 text-green-300",
  moderate: "bg-yellow-900 text-yellow-300",
  high: "bg-orange-900 text-orange-300",
  critical: "bg-red-950 text-red-400",
};
const SEV_BADGE: Record<string, string> = {
  "environnement_sonore_sous_surveillance": "bg-green-900 text-green-300",
  "nuisance_sonore_structurelle": "bg-yellow-900 text-yellow-300",
  "crise_santé_urbaine_majeure": "bg-orange-900 text-orange-300",
  "crise_pollution_sonore_systémique": "bg-red-950 text-red-400",
};

function DetailModal({ entity, onClose }: { entity: NPEEntity; onClose: () => void }) {
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
        className="bg-slate-950 border border-yellow-700/30 rounded-xl w-full max-w-lg p-6 shadow-2xl"
        onClick={e => e.stopPropagation()}
      >
        <div className="flex items-center justify-between mb-4">
          <div>
            <span className="text-lg font-bold text-white">{entity.entity_id}</span>
            <span className="ml-2 text-yellow-500 text-xs">{entity.region}</span>
            <span className="ml-2 text-slate-500 text-xs">
              {entity.urban_type.replace(/_/g, " ")}
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
                  ? "bg-yellow-900 text-white"
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
              ["Score Exposition",       entity.exposure_score,      "#d97706"],
              ["Score Santé",           entity.health_impact_score,  "#dc2626"],
              ["Score Inégalité",       entity.inequality_score,     "#7c3aed"],
              ["Score Gouvernance",     entity.governance_score,     "#0891b2"],
            ].map(([l, v, c]) => (
              <div
                key={String(l)}
                className="bg-slate-900 border border-yellow-700/20 rounded-lg p-3"
              >
                <div className="text-yellow-500/60 text-xs mb-1">{String(l)}</div>
                <div className="text-white font-bold text-lg">{Number(v).toFixed(1)}</div>
                <div className="h-1.5 rounded mt-1 bg-slate-800">
                  <div
                    className="h-1.5 rounded"
                    style={{ width: `${Math.min(Number(v), 100)}%`, background: String(c) }}
                  />
                </div>
              </div>
            ))}
            <div className="col-span-2 bg-slate-900 border border-yellow-700/20 rounded-lg p-3">
              <div className="text-yellow-500/60 text-xs mb-1">Score Composite Pollution Sonore</div>
              <div className="text-white font-bold text-2xl">
                {entity.composite_score.toFixed(1)}
              </div>
            </div>
          </div>
        )}

        {tab === "signal" && (
          <div className="bg-slate-900 border border-yellow-700/20 rounded-lg p-4 text-sm text-slate-200 leading-relaxed">
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
                <div className="text-yellow-500/50 text-xs mb-0.5">Niveau Sonore (dB)</div>
                <div className="text-white text-sm font-medium">
                  {Math.round(entity.noise_level_db * 100)}%
                </div>
              </div>
              <div className="bg-slate-800 rounded p-2">
                <div className="text-yellow-500/50 text-xs mb-0.5">Perturbation Sommeil</div>
                <div className="text-white text-sm font-medium">
                  {Math.round(entity.sleep_disruption * 100)}%
                </div>
              </div>
            </div>
          </div>
        )}

        {tab === "action" && (
          <div className="space-y-3 text-sm">
            <div className="bg-slate-900 border border-yellow-700/20 rounded-lg p-3">
              <div className="text-yellow-500/60 text-xs mb-1">Action Recommandée</div>
              <div className="text-white font-medium">
                {entity.recommended_action.replace(/_/g, " ")}
              </div>
            </div>
            <div className="bg-slate-900 border border-yellow-700/20 rounded-lg p-3">
              <div className="text-yellow-500/60 text-xs mb-1">Type Urbain</div>
              <div className="text-white font-medium capitalize">
                {entity.urban_type.replace(/_/g, " ")}
              </div>
            </div>
            <div className="bg-slate-900 border border-yellow-700/20 rounded-lg p-3">
              <div className="text-yellow-500/60 text-xs mb-1">Patron Détecté</div>
              <div className="text-orange-400 font-medium capitalize">
                {entity.noise_pattern.replace(/_/g, " ")}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function NoisePollutionDashboard() {
  const [data, setData] = useState<{
    entities: NPEEntity[];
    summary: NPESummary;
  } | null>(null);
  const [riskFilter, setRiskFilter] = useState<string>("all");
  const [patFilter, setPatFilter] = useState<string>("all");
  const [selected, setSelected] = useState<NPEEntity | null>(null);

  useEffect(() => {
    fetch("/api/noise-pollution-engine")
      .then(r => r.json())
      .then(setData)
      .catch(console.error);
  }, []);

  if (!data) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center">
        <div className="text-yellow-500 text-lg animate-pulse">
          Initialisation du Moteur Pollution Sonore...
        </div>
      </div>
    );
  }

  const { entities, summary } = data;
  const filtered = entities.filter(
    e =>
      (riskFilter === "all" || e.risk_level === riskFilter) &&
      (patFilter === "all" || e.noise_pattern === patFilter)
  );

  const dists = [
    { title: "Niveau de Risque",        counts: summary.risk_distribution,     colors: RISK_COLORS     },
    { title: "Patron Sonore",           counts: summary.pattern_distribution,  colors: PATTERN_COLORS  },
    { title: "Sévérité",               counts: summary.severity_distribution, colors: SEVERITY_COLORS },
    { title: "Action Déclenchée",       counts: summary.action_distribution,   colors: ACTION_COLORS   },
  ] as Array<{ title: string; counts: Record<string, number>; colors: Record<string, string> }>;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {selected && <DetailModal entity={selected} onClose={() => setSelected(null)} />}

      <div>
        <h1 className="text-2xl font-bold text-yellow-500">
          Pollution Sonore &amp; Santé Urbaine — Module 398
        </h1>
        <p className="text-orange-500/60 text-sm mt-1">
          Exposition · Santé · Inégalité · Gouvernance — Caelum Partners — Chaima Mhadbi, Fondatrice, Bruxelles
        </p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {[
          ["Total Zones Urbaines",       summary.total,                                                           "text-yellow-500"],
          ["Crise Sonore Critique",      summary.critical,                                                        "text-red-400"],
          ["Risque Élevé",               summary.high,                                                            "text-orange-400"],
          ["Composite Moyen",            `${summary.avg_composite.toFixed(1)}`,                                   "text-yellow-400"],
          ["Index Santé Sonore",         `${summary.avg_estimated_noise_health_index.toFixed(2)}/10`,             "text-yellow-500"],
          ["Zones Surveillées",          summary.low,                                                             "text-green-500"],
        ].map(([l, v, c]) => (
          <div
            key={String(l)}
            className="bg-slate-900 border border-yellow-700/30 rounded-xl p-3 text-center"
          >
            <div className={`text-xl font-bold ${c}`}>{v}</div>
            <div className="text-xs text-yellow-500/40 mt-0.5 leading-tight">{l}</div>
          </div>
        ))}
      </div>

      {/* Gauge Rings */}
      <div className="bg-slate-900 border border-yellow-700/30 rounded-xl p-5">
        <div className="grid grid-cols-4 gap-4">
          <GaugeRing
            value={entities.reduce((s, e) => s + e.exposure_score, 0) / (entities.length || 1)}
            label="Exposition Moy."
            color="#d97706"
          />
          <GaugeRing
            value={entities.reduce((s, e) => s + e.health_impact_score, 0) / (entities.length || 1)}
            label="Santé Moy."
            color="#dc2626"
          />
          <GaugeRing
            value={entities.reduce((s, e) => s + e.inequality_score, 0) / (entities.length || 1)}
            label="Inégalité Moy."
            color="#7c3aed"
          />
          <GaugeRing
            value={entities.reduce((s, e) => s + e.governance_score, 0) / (entities.length || 1)}
            label="Gouvernance Moy."
            color="#0891b2"
          />
        </div>
      </div>

      {/* Distribution Bars */}
      <div className="bg-slate-900 border border-yellow-700/30 rounded-xl p-5 grid grid-cols-1 md:grid-cols-2 gap-5">
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
                ? "bg-yellow-900 border-yellow-800 text-white"
                : "bg-slate-900 border-yellow-700/30 text-yellow-500/70 hover:text-white"
            }`}
          >
            {r}
          </button>
        ))}
        <span className="w-px h-5 self-center bg-yellow-700/30" />
        {[
          "all",
          "none",
          "chronic_cardiovascular_noise_crisis",
          "sleep_deprivation_pandemic",
          "childhood_cognitive_impairment",
          "noise_poverty_inequality_trap",
          "regulatory_enforcement_collapse",
        ].map(p => (
          <button
            key={p}
            onClick={() => setPatFilter(p)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${
              patFilter === p
                ? "bg-orange-950 border-orange-700 text-white"
                : "bg-slate-900 border-yellow-700/30 text-yellow-500/70 hover:text-white"
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
            className="bg-slate-900 border border-yellow-700/30 rounded-xl p-4 cursor-pointer hover:border-yellow-600 transition-colors"
          >
            <div className="flex items-center justify-between mb-1">
              <span className="font-bold text-white">{e.entity_id}</span>
              <span className="text-xs text-yellow-500/60">{e.region}</span>
            </div>
            <div className="text-xs text-slate-500 mb-2 capitalize">
              {e.urban_type.replace(/_/g, " ")}
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
            <div className="text-xs text-orange-500/60 mb-2 capitalize">
              {e.noise_pattern.replace(/_/g, " ")}
            </div>
            <div className="text-xs text-yellow-500/70 font-medium mb-2">
              Expo: {e.exposure_score.toFixed(1)} · Santé: {e.health_impact_score.toFixed(1)}
            </div>
            <div className="text-xs text-slate-400 truncate">{e.signal}</div>
          </div>
        ))}
      </div>
    </div>
  );
}
