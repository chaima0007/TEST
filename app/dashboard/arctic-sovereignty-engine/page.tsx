"use client";
import { useEffect, useState } from "react";

// ── Types ─────────────────────────────────────────────────────────────────────
type Entity = {
  entity_id: string;
  name: string;
  country: string;
  sector: string;
  composite_score: number;
  territorial_score: number;
  military_score: number;
  resource_score: number;
  climate_score: number;
  risk_level: string;
  primary_pattern: string;
  key_signals: string[];
  estimated_arctic_index: number;
  last_updated: string;
  disputed_zones: number;
};

type SummaryData = {
  total_entities: number;
  avg_composite: number;
  risk_distribution: Record<string, number>;
  pattern_distribution: Record<string, number>;
  top_risk_entities: string[];
  critical_alerts: string[];
  last_analysis: string;
  engine_version: string;
  domain: string;
  confidence_score: number;
  data_sources: string[];
  entities: Entity[];
  avg_estimated_arctic_index: number;
};

// ── Color maps ────────────────────────────────────────────────────────────────
const RISK_COLORS: Record<string, string> = {
  faible:   "#06b6d4",
  modéré:   "#0ea5e9",
  élevé:    "#3b82f6",
  critique: "#1d4ed8",
};

const RISK_BADGE: Record<string, string> = {
  faible:   "bg-cyan-900/60 text-cyan-300 border-cyan-700/50",
  modéré:   "bg-sky-900/60 text-sky-300 border-sky-700/50",
  élevé:    "bg-blue-900/60 text-blue-300 border-blue-700/50",
  critique: "bg-indigo-950/80 text-indigo-300 border-indigo-700/50",
};

const PATTERN_COLORS: Record<string, string> = {
  stabilite_arctique:       "#06b6d4",
  tension_territoriale:     "#1d4ed8",
  militarisation_acceleree: "#3b82f6",
  ruee_ressources:          "#0ea5e9",
  crise_climatique_arctique:"#7dd3fc",
};

const RISK_LABEL: Record<string, string> = {
  faible:   "Faible",
  modéré:   "Modéré",
  élevé:    "Élevé",
  critique: "Critique",
};

// ── GaugeRing ─────────────────────────────────────────────────────────────────
function GaugeRing({ value, label, color }: { value: number; label: string; color: string }) {
  const r = 36;
  const circ = 2 * Math.PI * r;
  const fill = circ * (1 - value / 100);
  return (
    <div className="flex flex-col items-center gap-1">
      <svg width="88" height="88" viewBox="0 0 88 88">
        <circle cx="44" cy="44" r={r} fill="none" stroke="#0f172a" strokeWidth="8" />
        <circle
          cx="44" cy="44" r={r} fill="none" stroke={color} strokeWidth="8"
          strokeDasharray={circ} strokeDashoffset={fill}
          strokeLinecap="round" transform="rotate(-90 44 44)"
        />
        <text x="44" y="49" textAnchor="middle" fill="white" fontSize="13" fontWeight="bold">
          {Math.round(value)}
        </text>
      </svg>
      <span className="text-xs text-cyan-300/70 text-center leading-tight">{label}</span>
    </div>
  );
}

// ── DistBar ───────────────────────────────────────────────────────────────────
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
      <span className="text-xs text-cyan-300/70 font-medium">{title}</span>
      <div className="flex h-3 rounded overflow-hidden gap-px">
        {Object.entries(counts).map(([k, v]) => (
          <div
            key={k}
            style={{ width: `${(v / total) * 100}%`, background: colors[k] ?? "#334155" }}
            title={`${k}: ${v}`}
          />
        ))}
      </div>
      <div className="flex flex-wrap gap-x-3 gap-y-0.5">
        {Object.entries(counts).map(([k, v]) => (
          <span key={k} className="text-xs text-cyan-300/60">
            <span style={{ color: colors[k] ?? "#94a3b8" }}>■</span>{" "}
            {k.replace(/_/g, " ")} {v}
          </span>
        ))}
      </div>
    </div>
  );
}

// ── DetailModal ───────────────────────────────────────────────────────────────
function DetailModal({ entity, onClose }: { entity: Entity; onClose: () => void }) {
  const [tab, setTab] = useState<"scores" | "signaux" | "actions">("scores");

  useEffect(() => {
    const h = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
    };
    window.addEventListener("keydown", h);
    return () => window.removeEventListener("keydown", h);
  }, [onClose]);

  const ringColor = RISK_COLORS[entity.risk_level] ?? "#0ea5e9";

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm"
      onClick={onClose}
    >
      <div
        className="bg-slate-950 border border-blue-700/30 rounded-2xl w-full max-w-lg p-6 shadow-2xl"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="flex items-start justify-between mb-4">
          <div className="flex items-center gap-3">
            <GaugeRing value={entity.composite_score} label="" color={ringColor} />
            <div>
              <div className="text-lg font-bold text-white">{entity.name}</div>
              <div className="flex gap-2 mt-1 flex-wrap">
                <span className="text-cyan-400 text-xs">{entity.country}</span>
                <span className="text-slate-500 text-xs">{entity.sector}</span>
              </div>
              <div className="mt-1 flex gap-2 flex-wrap">
                <span
                  className={`px-2 py-0.5 rounded border text-xs font-medium ${RISK_BADGE[entity.risk_level] ?? "bg-slate-700 text-slate-300 border-slate-600"}`}
                >
                  {RISK_LABEL[entity.risk_level] ?? entity.risk_level}
                </span>
                <span className="px-2 py-0.5 rounded border text-xs bg-blue-950/60 text-blue-300 border-blue-700/30">
                  {entity.disputed_zones} zone{entity.disputed_zones !== 1 ? "s" : ""} disputée{entity.disputed_zones !== 1 ? "s" : ""}
                </span>
              </div>
            </div>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl leading-none">
            ✕
          </button>
        </div>

        <div className="flex gap-2 mb-4">
          {(["scores", "signaux", "actions"] as const).map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`px-3 py-1 rounded text-xs font-medium transition-colors ${
                tab === t
                  ? "bg-blue-900 text-white border border-blue-700"
                  : "bg-slate-900 text-slate-400 hover:text-white border border-slate-800"
              }`}
            >
              {t === "scores" ? "Scores" : t === "signaux" ? "Signaux" : "Actions"}
            </button>
          ))}
        </div>

        {tab === "scores" && (
          <div className="grid grid-cols-2 gap-3 text-sm">
            {(
              [
                ["Score Territorial",  entity.territorial_score, "#1d4ed8"],
                ["Score Militaire",    entity.military_score,    "#3b82f6"],
                ["Score Ressources",   entity.resource_score,    "#0ea5e9"],
                ["Score Climatique",   entity.climate_score,     "#06b6d4"],
              ] as [string, number, string][]
            ).map(([l, v, c]) => (
              <div key={l} className="bg-slate-900 border border-blue-700/20 rounded-lg p-3">
                <div className="text-cyan-300/60 text-xs mb-1">{l}</div>
                <div className="text-white font-bold text-lg">{v.toFixed(1)}</div>
                <div className="h-1.5 rounded mt-1 bg-slate-800">
                  <div
                    className="h-1.5 rounded"
                    style={{ width: `${Math.min(v, 100)}%`, background: c }}
                  />
                </div>
              </div>
            ))}
            <div className="col-span-2 bg-slate-900 border border-blue-700/20 rounded-lg p-3">
              <div className="text-cyan-300/60 text-xs mb-1">Score Composite</div>
              <div className="text-white font-bold text-2xl">
                {entity.composite_score.toFixed(1)}
              </div>
              <div className="text-cyan-400/60 text-xs mt-1">
                Index Arctique: {entity.estimated_arctic_index.toFixed(2)}/10
              </div>
            </div>
          </div>
        )}

        {tab === "signaux" && (
          <div className="space-y-3">
            <div className="text-xs text-cyan-300/60 font-medium mb-2">Signaux Géopolitiques Détectés</div>
            {entity.key_signals.map((sig, i) => (
              <div
                key={i}
                className="bg-slate-900 border border-blue-700/20 rounded-lg p-3 text-sm text-slate-200 leading-relaxed flex gap-2"
              >
                <span className="text-cyan-400 mt-0.5 shrink-0">◆</span>
                <span>{sig}</span>
              </div>
            ))}
            <div className="grid grid-cols-2 gap-2 text-xs mt-2">
              <div className="bg-slate-900 border border-blue-700/20 rounded-lg p-3">
                <div className="text-cyan-300/60 mb-1">Pattern Primaire</div>
                <div className="text-white font-bold capitalize">
                  {entity.primary_pattern.replace(/_/g, " ")}
                </div>
              </div>
              <div className="bg-slate-900 border border-blue-700/20 rounded-lg p-3">
                <div className="text-cyan-300/60 mb-1">Dernière Analyse</div>
                <div className="text-white font-bold">{entity.last_updated}</div>
              </div>
            </div>
          </div>
        )}

        {tab === "actions" && (
          <div className="space-y-3 text-sm">
            <div className="bg-blue-900/20 border border-blue-700/30 rounded-xl p-4">
              <div className="text-cyan-300/60 text-xs uppercase tracking-wide mb-2">
                Niveau de Risque Arctique
              </div>
              <div className="flex items-center gap-3">
                <span
                  className={`px-3 py-1 rounded border text-sm font-medium ${RISK_BADGE[entity.risk_level] ?? "bg-slate-700 text-slate-300 border-slate-600"}`}
                >
                  {RISK_LABEL[entity.risk_level] ?? entity.risk_level}
                </span>
                <span className="text-white font-bold text-xl">
                  {entity.composite_score.toFixed(1)}/100
                </span>
              </div>
            </div>
            <div className="bg-slate-900 border border-blue-700/20 rounded-lg p-3">
              <div className="text-cyan-300/60 text-xs mb-1">Zones Disputées</div>
              <div className="text-white font-medium text-2xl">{entity.disputed_zones}</div>
              <div className="text-cyan-400/50 text-xs">
                zone{entity.disputed_zones !== 1 ? "s" : ""} de souveraineté contestée{entity.disputed_zones !== 1 ? "s" : ""}
              </div>
            </div>
            <div className="bg-slate-900 border border-blue-700/20 rounded-lg p-3">
              <div className="text-cyan-300/60 text-xs mb-1">Index Arctique Estimé</div>
              <div className="text-white font-medium">{entity.estimated_arctic_index.toFixed(2)}/10</div>
            </div>
            <div className="bg-slate-900 border border-blue-700/20 rounded-lg p-3">
              <div className="text-cyan-300/60 text-xs mb-1">Secteur d&apos;Activité</div>
              <div className="text-white font-medium">{entity.sector}</div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

// ── EntityCard ────────────────────────────────────────────────────────────────
function EntityCard({ entity, onClick }: { entity: Entity; onClick: () => void }) {
  const ringColor = RISK_COLORS[entity.risk_level] ?? "#0ea5e9";

  return (
    <div
      onClick={onClick}
      className="bg-slate-900 border border-blue-700/30 rounded-xl p-4 cursor-pointer hover:border-cyan-500/50 hover:bg-slate-800/60 transition-all"
    >
      <div className="flex items-center gap-3 mb-3">
        <GaugeRing value={entity.composite_score} label="" color={ringColor} />
        <div className="flex-1 min-w-0">
          <div className="text-white font-bold truncate text-sm">{entity.name}</div>
          <div className="text-slate-400 text-xs">{entity.country} · {entity.sector}</div>
          <div className="mt-1 flex gap-1 flex-wrap">
            <span
              className={`px-2 py-0.5 rounded border text-xs font-medium ${RISK_BADGE[entity.risk_level] ?? "bg-slate-700 text-slate-300 border-slate-600"}`}
            >
              {RISK_LABEL[entity.risk_level] ?? entity.risk_level}
            </span>
          </div>
        </div>
      </div>
      <div className="text-xs text-cyan-300/60 mb-2 capitalize">
        {entity.primary_pattern.replace(/_/g, " ")}
      </div>
      <div className="grid grid-cols-2 gap-1 text-xs text-slate-400">
        <span>Terr: <span className="text-cyan-300">{entity.territorial_score.toFixed(0)}</span></span>
        <span>Milit: <span className="text-blue-300">{entity.military_score.toFixed(0)}</span></span>
        <span>Ress: <span className="text-sky-300">{entity.resource_score.toFixed(0)}</span></span>
        <span>Clim: <span className="text-cyan-400">{entity.climate_score.toFixed(0)}</span></span>
      </div>
      <div className="mt-2 text-xs text-slate-500 flex justify-between">
        <span>{entity.disputed_zones} zone{entity.disputed_zones !== 1 ? "s" : ""} disputée{entity.disputed_zones !== 1 ? "s" : ""}</span>
        <span>Index: {entity.estimated_arctic_index.toFixed(2)}</span>
      </div>
    </div>
  );
}

// ── Main Dashboard ────────────────────────────────────────────────────────────
export default function ArcticDashboard() {
  const [data, setData] = useState<SummaryData | null>(null);
  const [filter, setFilter] = useState("Tous");
  const [selected, setSelected] = useState<Entity | null>(null);

  useEffect(() => {
    fetch("/api/arctic-sovereignty-engine")
      .then((r) => r.json())
      .then((json) => setData(json as SummaryData))
      .catch(console.error);
  }, []);

  if (!data) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center">
        <div className="text-cyan-400 text-lg animate-pulse">
          Initialisation du Moteur Souveraineté Arctique…
        </div>
      </div>
    );
  }

  const FILTER_PILLS = ["Tous", "Critique", "Élevé", "Modéré", "Faible"];
  const FILTER_MAP: Record<string, string> = {
    Tous: "",
    Critique: "critique",
    Élevé: "élevé",
    Modéré: "modéré",
    Faible: "faible",
  };

  const filtered = data.entities.filter(
    (e) => !FILTER_MAP[filter] || e.risk_level === FILTER_MAP[filter]
  );

  const n = data.entities.length || 1;
  const avgTerritorial = data.entities.reduce((s, e) => s + e.territorial_score, 0) / n;
  const avgMilitary    = data.entities.reduce((s, e) => s + e.military_score, 0) / n;
  const avgResource    = data.entities.reduce((s, e) => s + e.resource_score, 0) / n;
  const avgClimate     = data.entities.reduce((s, e) => s + e.climate_score, 0) / n;
  const totalDisputed  = data.entities.reduce((s, e) => s + e.disputed_zones, 0);

  const kpiCards: [string, string | number, string][] = [
    ["Total Entités",      data.total_entities,                              "text-cyan-400"],
    ["Critique",           data.risk_distribution["critique"] ?? 0,          "text-indigo-400"],
    ["Élevé",              data.risk_distribution["élevé"] ?? 0,             "text-blue-400"],
    ["Composite Moyen",    data.avg_composite.toFixed(1),                    "text-sky-300"],
    ["Index Arctique",     data.avg_estimated_arctic_index.toFixed(2),       "text-cyan-300"],
    ["Zones Disputées",    totalDisputed,                                    "text-blue-300"],
  ];

  const dists: { title: string; counts: Record<string, number>; colors: Record<string, string> }[] = [
    {
      title: "Distribution du Risque",
      counts: data.risk_distribution,
      colors: RISK_COLORS,
    },
    {
      title: "Patterns Détectés",
      counts: data.pattern_distribution,
      colors: PATTERN_COLORS,
    },
    {
      title: "Entités par Pays",
      counts: data.entities.reduce<Record<string, number>>((acc, e) => {
        acc[e.country] = (acc[e.country] ?? 0) + 1;
        return acc;
      }, {}),
      colors: {
        Russie: "#1d4ed8",
        Chine: "#3b82f6",
        "États-Unis": "#0ea5e9",
        Norvège: "#06b6d4",
        Canada: "#7dd3fc",
        Finlande: "#bae6fd",
        Danemark: "#e0f2fe",
        Islande: "#f0f9ff",
      },
    },
    {
      title: "Zones Disputées par Entité",
      counts: data.entities.reduce<Record<string, number>>((acc, e) => {
        if (e.disputed_zones > 0) acc[e.name] = e.disputed_zones;
        return acc;
      }, {}),
      colors: {
        "Russia Arctic Command":    "#1d4ed8",
        "China Arctic Silk Road":   "#3b82f6",
        "US Coast Guard Arctic":    "#0ea5e9",
        "Norway Arctic Council":    "#06b6d4",
        "Canada Arctic Patrol":     "#7dd3fc",
        "Finland Arctic Strategy":  "#bae6fd",
        "Denmark Greenland Authority": "#e0f2fe",
      },
    },
  ];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {selected && (
        <DetailModal entity={selected} onClose={() => setSelected(null)} />
      )}

      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-cyan-400">
          Arctic Sovereignty Engine — Intelligence Géopolitique Polaire
        </h1>
        <p className="text-cyan-300/50 text-sm mt-1">
          Tensions Territoriales · Militarisation · Ressources · Crise Climatique Arctique
        </p>
        <div className="flex gap-4 mt-2 text-xs text-slate-500">
          <span>Domaine: <span className="text-cyan-400">{data.domain}</span></span>
          <span>Version: <span className="text-cyan-400">{data.engine_version}</span></span>
          <span>Confiance: <span className="text-cyan-400">{(data.confidence_score * 100).toFixed(0)}%</span></span>
          <span>Analyse: <span className="text-cyan-400">{data.last_analysis}</span></span>
        </div>
      </div>

      {/* KPI Cards — 6 */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {kpiCards.map(([label, value, color]) => (
          <div key={label} className="bg-slate-900 border border-blue-700/30 rounded-xl p-3 text-center">
            <div className={`text-xl font-bold ${color}`}>{value}</div>
            <div className="text-xs text-cyan-300/40 mt-0.5 leading-tight">{label}</div>
          </div>
        ))}
      </div>

      {/* Critical Alerts */}
      {data.critical_alerts.length > 0 && (
        <div className="bg-indigo-950/40 border border-indigo-700/40 rounded-xl p-4 space-y-2">
          <div className="text-xs font-semibold text-indigo-300 uppercase tracking-wide mb-2">
            Alertes Critiques
          </div>
          {data.critical_alerts.map((alert, i) => (
            <div key={i} className="flex items-start gap-2 text-sm text-indigo-200">
              <span className="text-indigo-400 shrink-0">▶</span>
              <span>{alert}</span>
            </div>
          ))}
        </div>
      )}

      {/* Gauge Rings — 4 */}
      <div className="bg-slate-900 border border-blue-700/30 rounded-xl p-5">
        <div className="text-sm font-semibold text-cyan-300/70 mb-4">
          Dimensions Souveraineté Arctique (moyennes)
        </div>
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
          <GaugeRing value={avgTerritorial} label="Territorial"  color="#1d4ed8" />
          <GaugeRing value={avgMilitary}    label="Militaire"    color="#3b82f6" />
          <GaugeRing value={avgResource}    label="Ressources"   color="#0ea5e9" />
          <GaugeRing value={avgClimate}     label="Climatique"   color="#06b6d4" />
        </div>
      </div>

      {/* Distribution Bars — 4 */}
      <div className="bg-slate-900 border border-blue-700/30 rounded-xl p-5 grid grid-cols-1 md:grid-cols-2 gap-5">
        {dists.map((d) => (
          <DistBar key={d.title} title={d.title} counts={d.counts} colors={d.colors} />
        ))}
      </div>

      {/* Data Sources */}
      <div className="flex flex-wrap gap-2">
        {data.data_sources.map((src) => (
          <span
            key={src}
            className="px-3 py-1 rounded-full text-xs bg-slate-900 border border-blue-700/30 text-cyan-400/70"
          >
            {src.replace(/_/g, " ")}
          </span>
        ))}
      </div>

      {/* Filter Pills */}
      <div className="flex flex-wrap gap-2">
        {FILTER_PILLS.map((pill) => (
          <button
            key={pill}
            onClick={() => setFilter(pill)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${
              filter === pill
                ? "bg-blue-900 border-blue-700 text-white"
                : "bg-slate-900 border-blue-700/30 text-cyan-400/70 hover:text-white"
            }`}
          >
            {pill}
          </button>
        ))}
      </div>

      {/* Entity Cards Grid — 4 cols xl */}
      {filtered.length === 0 ? (
        <div className="text-slate-500 text-center py-16">
          Aucune entité ne correspond au filtre sélectionné.
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          {filtered.map((entity) => (
            <EntityCard
              key={entity.entity_id}
              entity={entity}
              onClick={() => setSelected(entity)}
            />
          ))}
        </div>
      )}
    </div>
  );
}
