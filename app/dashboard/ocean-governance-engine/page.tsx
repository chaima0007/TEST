"use client";
import { useEffect, useState } from "react";

type OGEEntity = {
  id: string;
  ocean_zone: string;
  region: string;
  jurisdiction_score: number;
  conservation_score: number;
  enforcement_score: number;
  equity_score: number;
  composite_score: number;
  risk_level: string;
  ocean_pattern: string;
  severity: string;
  recommended_action: string;
  signal: string;
  jurisdictional_gap: number;
  illegal_fishing_intensity: number;
};

type OGESummary = {
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
  avg_estimated_ocean_governance_index: number;
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
      <span className="text-xs text-cyan-500/70 text-center">{label}</span>
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
      <span className="text-xs text-cyan-500/70 font-medium">{title}</span>
      <div className="flex h-3 rounded overflow-hidden gap-px">
        {Object.entries(counts).map(([k, v]) => (
          <div
            key={k}
            style={{ width: `${(v / total) * 100}%`, background: colors[k] || "#164e63" }}
            title={`${k}: ${v}`}
          />
        ))}
      </div>
      <div className="flex flex-wrap gap-x-3 gap-y-0.5">
        {Object.entries(counts).map(([k, v]) => (
          <span key={k} className="text-xs text-cyan-500/60">
            <span style={{ color: colors[k] || "#0e7490" }}>■</span> {k.replace(/_/g, " ")} {v}
          </span>
        ))}
      </div>
    </div>
  );
}

const RISK_COLORS: Record<string, string> = {
  low: "#16a34a",
  moderate: "#0891b2",
  high: "#1d4ed8",
  critical: "#dc2626",
};
const PATTERN_COLORS: Record<string, string> = {
  none: "#16a34a",
  high_seas_jurisdiction_vacuum: "#dc2626",
  illeagal_fishing_impunity: "#7c3aed",
  biodiversity_treaty_collapse: "#059669",
  deep_sea_resource_capture: "#b45309",
  marine_protected_area_failure: "#0891b2",
};
const SEVERITY_COLORS: Record<string, string> = {
  "gouvernance_océanique_sous_surveillance": "#16a34a",
  "déficit_gouvernance_maritime_structurel": "#0891b2",
  "crise_haute_mer_majeure": "#1d4ed8",
  "crise_gouvernance_océanique_systémique": "#dc2626",
};
const ACTION_COLORS: Record<string, string> = {
  "veille_gouvernance_océanique_continue": "#16a34a",
  "consolidation_politiques_conservation_marine": "#0891b2",
  "renforcement_accéléré_juridiction_maritime": "#1d4ed8",
  "intervention_urgente_traité_haute_mer_critique": "#dc2626",
};
const RISK_BADGE: Record<string, string> = {
  low: "bg-green-900 text-green-300",
  moderate: "bg-cyan-900 text-cyan-300",
  high: "bg-blue-950 text-blue-400",
  critical: "bg-red-950 text-red-400",
};
const SEV_BADGE: Record<string, string> = {
  "gouvernance_océanique_sous_surveillance": "bg-green-900 text-green-300",
  "déficit_gouvernance_maritime_structurel": "bg-cyan-900 text-cyan-300",
  "crise_haute_mer_majeure": "bg-blue-950 text-blue-400",
  "crise_gouvernance_océanique_systémique": "bg-red-950 text-red-400",
};

function DetailModal({ entity, onClose }: { entity: OGEEntity; onClose: () => void }) {
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
        className="bg-slate-950 border border-cyan-700/30 rounded-xl w-full max-w-lg p-6 shadow-2xl"
        onClick={e => e.stopPropagation()}
      >
        <div className="flex items-center justify-between mb-4">
          <div>
            <span className="text-lg font-bold text-white">{entity.id}</span>
            <span className="ml-2 text-cyan-500 text-xs">{entity.region}</span>
            <span className="ml-2 text-slate-500 text-xs">
              {entity.ocean_zone.replace(/_/g, " ")}
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
                  ? "bg-cyan-900 text-white"
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
              ["Score Juridiction",   entity.jurisdiction_score,  "#0891b2"],
              ["Score Conservation", entity.conservation_score,   "#16a34a"],
              ["Score Répression",   entity.enforcement_score,    "#1d4ed8"],
              ["Score Équité",       entity.equity_score,         "#7c3aed"],
            ].map(([l, v, c]) => (
              <div
                key={String(l)}
                className="bg-slate-900 border border-cyan-700/20 rounded-lg p-3"
              >
                <div className="text-cyan-500/60 text-xs mb-1">{String(l)}</div>
                <div className="text-white font-bold text-lg">{Number(v).toFixed(1)}</div>
                <div className="h-1.5 rounded mt-1 bg-slate-800">
                  <div
                    className="h-1.5 rounded"
                    style={{ width: `${Math.min(Number(v), 100)}%`, background: String(c) }}
                  />
                </div>
              </div>
            ))}
            <div className="col-span-2 bg-slate-900 border border-cyan-700/20 rounded-lg p-3">
              <div className="text-cyan-500/60 text-xs mb-1">Score Composite Gouvernance Océanique</div>
              <div className="text-white font-bold text-2xl">
                {entity.composite_score.toFixed(1)}
              </div>
            </div>
          </div>
        )}

        {tab === "signal" && (
          <div className="bg-slate-900 border border-cyan-700/20 rounded-lg p-4 text-sm text-slate-200 leading-relaxed">
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
                <div className="text-cyan-500/50 text-xs mb-0.5">Gap Juridictionnel</div>
                <div className="text-white text-sm font-medium">
                  {Math.round(entity.jurisdictional_gap * 100)}%
                </div>
              </div>
              <div className="bg-slate-800 rounded p-2">
                <div className="text-cyan-500/50 text-xs mb-0.5">Intensité Pêche Illégale</div>
                <div className="text-white text-sm font-medium">
                  {Math.round(entity.illegal_fishing_intensity * 100)}%
                </div>
              </div>
            </div>
          </div>
        )}

        {tab === "action" && (
          <div className="space-y-3 text-sm">
            <div className="bg-slate-900 border border-cyan-700/20 rounded-lg p-3">
              <div className="text-cyan-500/60 text-xs mb-1">Action Recommandée</div>
              <div className="text-white font-medium">
                {entity.recommended_action.replace(/_/g, " ")}
              </div>
            </div>
            <div className="bg-slate-900 border border-cyan-700/20 rounded-lg p-3">
              <div className="text-cyan-500/60 text-xs mb-1">Zone Océanique</div>
              <div className="text-white font-medium capitalize">
                {entity.ocean_zone.replace(/_/g, " ")}
              </div>
            </div>
            <div className="bg-slate-900 border border-cyan-700/20 rounded-lg p-3">
              <div className="text-cyan-500/60 text-xs mb-1">Patron Détecté</div>
              <div className="text-cyan-400 font-medium capitalize">
                {entity.ocean_pattern.replace(/_/g, " ")}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function OceanGovernanceDashboard() {
  const [data, setData] = useState<{
    entities: OGEEntity[];
    summary: OGESummary;
    avg_jurisdiction: number;
  } | null>(null);
  const [riskFilter, setRiskFilter] = useState<string>("all");
  const [patFilter, setPatFilter] = useState<string>("all");
  const [selected, setSelected] = useState<OGEEntity | null>(null);

  useEffect(() => {
    fetch("/api/ocean-governance-engine")
      .then(r => r.json())
      .then(setData)
      .catch(console.error);
  }, []);

  if (!data) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center">
        <div className="text-cyan-500 text-lg animate-pulse">
          Initialisation du Moteur Gouvernance Océanique...
        </div>
      </div>
    );
  }

  const { entities, summary, avg_jurisdiction } = data;
  const filtered = entities.filter(
    e =>
      (riskFilter === "all" || e.risk_level === riskFilter) &&
      (patFilter === "all" || e.ocean_pattern === patFilter)
  );

  const dists = [
    { title: "Niveau de Risque",          counts: summary.risk_distribution,     colors: RISK_COLORS     },
    { title: "Patron Océanique",          counts: summary.pattern_distribution,  colors: PATTERN_COLORS  },
    { title: "Sévérité",                  counts: summary.severity_distribution, colors: SEVERITY_COLORS },
    { title: "Action Déclenchée",         counts: summary.action_distribution,   colors: ACTION_COLORS   },
  ] as Array<{ title: string; counts: Record<string, number>; colors: Record<string, string> }>;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {selected && <DetailModal entity={selected} onClose={() => setSelected(null)} />}

      <div>
        <h1 className="text-2xl font-bold text-cyan-400">
          Gouvernance Océans &amp; Traité Haute Mer — Module 420
        </h1>
        <p className="text-blue-500/60 text-sm mt-1">
          Juridiction · Conservation · Répression · Équité — Caelum Partners — Chaima Mhadbi, Fondatrice, Bruxelles
        </p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {[
          ["Total Zones Marines",          summary.total,                                                              "text-cyan-400"],
          ["Crise Gouvernance",            summary.critical,                                                           "text-red-400"],
          ["Crise Haute Mer",             summary.high,                                                               "text-blue-400"],
          ["Composite Moyen",             `${summary.avg_composite.toFixed(1)}`,                                      "text-cyan-500"],
          ["Index Gouvernance Océanique", `${summary.avg_estimated_ocean_governance_index.toFixed(2)}/10`,            "text-cyan-400"],
          ["Juridiction Moy.",           `${avg_jurisdiction.toFixed(1)}`,                                            "text-blue-400"],
        ].map(([l, v, c]) => (
          <div
            key={String(l)}
            className="bg-slate-900 border border-cyan-700/30 rounded-xl p-3 text-center"
          >
            <div className={`text-xl font-bold ${c}`}>{v}</div>
            <div className="text-xs text-cyan-500/40 mt-0.5 leading-tight">{l}</div>
          </div>
        ))}
      </div>

      {/* Gauge Rings */}
      <div className="bg-slate-900 border border-cyan-700/30 rounded-xl p-5">
        <div className="grid grid-cols-4 gap-4">
          <GaugeRing
            value={entities.reduce((s, e) => s + e.jurisdiction_score, 0) / (entities.length || 1)}
            label="Juridiction Moy."
            color="#0891b2"
          />
          <GaugeRing
            value={entities.reduce((s, e) => s + e.conservation_score, 0) / (entities.length || 1)}
            label="Conservation Moy."
            color="#16a34a"
          />
          <GaugeRing
            value={entities.reduce((s, e) => s + e.enforcement_score, 0) / (entities.length || 1)}
            label="Répression Moy."
            color="#1d4ed8"
          />
          <GaugeRing
            value={entities.reduce((s, e) => s + e.equity_score, 0) / (entities.length || 1)}
            label="Équité Moy."
            color="#7c3aed"
          />
        </div>
      </div>

      {/* Distribution Bars */}
      <div className="bg-slate-900 border border-cyan-700/30 rounded-xl p-5 grid grid-cols-1 md:grid-cols-2 gap-5">
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
                ? "bg-cyan-900 border-cyan-800 text-white"
                : "bg-slate-900 border-cyan-700/30 text-cyan-500/70 hover:text-white"
            }`}
          >
            {r}
          </button>
        ))}
        <span className="w-px h-5 self-center bg-cyan-700/30" />
        {[
          "all",
          "none",
          "high_seas_jurisdiction_vacuum",
          "illeagal_fishing_impunity",
          "biodiversity_treaty_collapse",
          "deep_sea_resource_capture",
          "marine_protected_area_failure",
        ].map(p => (
          <button
            key={p}
            onClick={() => setPatFilter(p)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${
              patFilter === p
                ? "bg-blue-950 border-blue-700 text-white"
                : "bg-slate-900 border-cyan-700/30 text-cyan-500/70 hover:text-white"
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
            key={e.id}
            onClick={() => setSelected(e)}
            className="bg-slate-900 border border-cyan-700/30 rounded-xl p-4 cursor-pointer hover:border-cyan-600 transition-colors"
          >
            <div className="flex items-center justify-between mb-1">
              <span className="font-bold text-white">{e.id}</span>
              <span className="text-xs text-cyan-500/60">{e.region}</span>
            </div>
            <div className="text-xs text-slate-500 mb-2 capitalize">
              {e.ocean_zone.replace(/_/g, " ")}
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
            <div className="text-xs text-cyan-500/60 mb-2 capitalize">
              {e.ocean_pattern.replace(/_/g, " ")}
            </div>
            <div className="text-xs text-blue-400/70 font-medium mb-2">
              Jur: {e.jurisdiction_score.toFixed(1)} · Con: {e.conservation_score.toFixed(1)}
            </div>
            <div className="text-xs text-slate-400 truncate">{e.signal}</div>
          </div>
        ))}
      </div>
    </div>
  );
}
