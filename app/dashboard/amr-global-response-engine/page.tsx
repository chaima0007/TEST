"use client";
import { useEffect, useState } from "react";

interface Entity {
  entity_id: string;
  name: string;
  country: string;
  sector: string;
  composite_score: number;
  detection_score: number;
  treatment_score: number;
  containment_score: number;
  cooperation_score: number;
  risk_level: string;
  primary_pattern: string;
  key_signals: string[];
  estimated_amr_index: number;
  last_updated: string;
  outbreak_count: number;
}

interface SummaryData {
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
  avg_estimated_amr_index: number;
}

function GaugeRing({ value, label, color }: { value: number; label: string; color: string }) {
  const r = 36;
  const circ = 2 * Math.PI * r;
  const fill = circ * (1 - value / 100);
  return (
    <div className="flex flex-col items-center gap-1">
      <svg width="88" height="88" viewBox="0 0 88 88">
        <circle cx="44" cy="44" r={r} fill="none" stroke="#0a1628" strokeWidth="8" />
        <circle
          cx="44" cy="44" r={r} fill="none" stroke={color} strokeWidth="8"
          strokeDasharray={circ} strokeDashoffset={fill}
          strokeLinecap="round" transform="rotate(-90 44 44)"
        />
        <text x="44" y="49" textAnchor="middle" fill="white" fontSize="13" fontWeight="bold">
          {Math.round(value)}
        </text>
      </svg>
      <span className="text-xs text-blue-300/70 text-center">{label}</span>
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
      <span className="text-xs text-blue-300/70 font-medium">{title}</span>
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
          <span key={k} className="text-xs text-blue-300/60">
            <span style={{ color: colors[k] || "#94a3b8" }}>■</span>{" "}
            {k.replace(/_/g, " ")} {v}
          </span>
        ))}
      </div>
    </div>
  );
}

const RISK_COLORS: Record<string, string> = {
  faible: "#10b981",
  "modéré": "#f59e0b",
  "élevé": "#3b82f6",
  critique: "#ef4444",
};

const PATTERN_COLORS: Record<string, string> = {
  resistance_totale: "#ef4444",
  pipeline_vide: "#f97316",
  confinement_echoue: "#a855f7",
  cooperation_absente: "#06b6d4",
  reponse_amr_coordonnee: "#10b981",
};

const RISK_BADGE: Record<string, string> = {
  faible: "bg-emerald-900 text-emerald-300",
  "modéré": "bg-amber-900 text-amber-300",
  "élevé": "bg-blue-900 text-blue-300",
  critique: "bg-red-950 text-red-400",
};

function DetailModal({ entity, onClose }: { entity: Entity; onClose: () => void }) {
  const [tab, setTab] = useState<"scores" | "signaux" | "actions">("scores");

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
        className="bg-slate-950 border border-blue-700/30 rounded-xl w-full max-w-lg p-6 shadow-2xl"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="flex items-center justify-between mb-4">
          <div>
            <span className="text-lg font-bold text-white">{entity.name}</span>
            <span className="ml-2 text-blue-400 text-xs">{entity.country}</span>
            <span className="ml-2 text-slate-500 text-xs">{entity.sector}</span>
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
                  ? "bg-blue-900 text-white"
                  : "bg-slate-900 text-slate-400 hover:text-white"
              }`}
            >
              {t.charAt(0).toUpperCase() + t.slice(1)}
            </button>
          ))}
        </div>

        {tab === "scores" && (
          <div className="grid grid-cols-2 gap-3 text-sm">
            {(
              [
                ["Détection", entity.detection_score, "#ef4444"],
                ["Traitement", entity.treatment_score, "#f97316"],
                ["Confinement", entity.containment_score, "#06b6d4"],
                ["Coopération", entity.cooperation_score, "#a855f7"],
              ] as [string, number, string][]
            ).map(([l, v, c]) => (
              <div key={l} className="bg-slate-900 border border-blue-700/20 rounded-lg p-3">
                <div className="text-blue-300/60 text-xs mb-1">{l}</div>
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
              <div className="text-blue-300/60 text-xs mb-1">Score Composite AMR</div>
              <div className="text-white font-bold text-2xl">
                {entity.composite_score.toFixed(2)}
              </div>
              <div className="text-slate-400 text-xs mt-1">
                Index AMR: {entity.estimated_amr_index.toFixed(2)}/10 · Foyers: {entity.outbreak_count}
              </div>
            </div>
          </div>
        )}

        {tab === "signaux" && (
          <div className="space-y-3">
            <div className="flex gap-2 flex-wrap mb-3">
              <span
                className={`px-2 py-0.5 rounded text-xs font-medium ${
                  RISK_BADGE[entity.risk_level] || "bg-slate-700 text-slate-300"
                }`}
              >
                {entity.risk_level}
              </span>
              <span
                className="px-2 py-0.5 rounded text-xs font-medium bg-slate-800 text-blue-300"
                style={{ borderColor: PATTERN_COLORS[entity.primary_pattern] }}
              >
                {entity.primary_pattern.replace(/_/g, " ")}
              </span>
            </div>
            {entity.key_signals.map((sig, i) => (
              <div
                key={i}
                className="bg-slate-900 border border-blue-700/20 rounded-lg p-3 text-sm text-slate-200 leading-relaxed"
              >
                {sig}
              </div>
            ))}
          </div>
        )}

        {tab === "actions" && (
          <div className="space-y-3 text-sm">
            <div className="bg-slate-900 border border-blue-700/20 rounded-lg p-3">
              <div className="text-blue-300/60 text-xs mb-1">Patron AMR Principal</div>
              <div
                className="font-medium"
                style={{ color: PATTERN_COLORS[entity.primary_pattern] || "#94a3b8" }}
              >
                {entity.primary_pattern.replace(/_/g, " ")}
              </div>
            </div>
            <div className="bg-slate-900 border border-blue-700/20 rounded-lg p-3">
              <div className="text-blue-300/60 text-xs mb-1">Secteur</div>
              <div className="text-white font-medium">{entity.sector}</div>
            </div>
            <div className="bg-slate-900 border border-blue-700/20 rounded-lg p-3">
              <div className="text-blue-300/60 text-xs mb-1">Dernière mise à jour</div>
              <div className="text-white font-medium">{entity.last_updated}</div>
            </div>
            <div className="bg-slate-900 border border-blue-700/20 rounded-lg p-3">
              <div className="text-blue-300/60 text-xs mb-1">Pays · Foyers déclarés</div>
              <div className="text-white font-medium">
                {entity.country} · {entity.outbreak_count} foyers
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function AmrDashboard() {
  const [data, setData] = useState<SummaryData | null>(null);
  const [filter, setFilter] = useState<string>("Tous");
  const [selected, setSelected] = useState<Entity | null>(null);

  useEffect(() => {
    fetch("/api/amr-global-response-engine")
      .then((r) => r.json())
      .then((json) => {
        if (json.entities) setData(json);
      })
      .catch(console.error);
  }, []);

  if (!data) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center">
        <div className="text-blue-400 text-lg animate-pulse">
          Initialisation du Moteur AMR Global Response...
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
    (e) => !FILTER_MAP[filter] || e.risk_level === FILTER_MAP[filter],
  );

  const avgDetection =
    data.entities.reduce((s, e) => s + e.detection_score, 0) / (data.entities.length || 1);
  const avgTreatment =
    data.entities.reduce((s, e) => s + e.treatment_score, 0) / (data.entities.length || 1);
  const avgContainment =
    data.entities.reduce((s, e) => s + e.containment_score, 0) / (data.entities.length || 1);
  const avgCooperation =
    data.entities.reduce((s, e) => s + e.cooperation_score, 0) / (data.entities.length || 1);

  const dist4 = [
    {
      title: "Distribution des Risques",
      counts: data.risk_distribution,
      colors: RISK_COLORS,
    },
    {
      title: "Patrons AMR",
      counts: data.pattern_distribution,
      colors: PATTERN_COLORS,
    },
    {
      title: "Sources de Données",
      counts: Object.fromEntries(data.data_sources.map((s) => [s, 1])),
      colors: { who_surveillance: "#06b6d4", clinical_trials_db: "#a855f7", resistance_monitoring: "#f59e0b" },
    },
    {
      title: "Entités à Risque Critique",
      counts: Object.fromEntries(
        data.top_risk_entities.map((name, i) => [name, 3 - i])
      ),
      colors: { [data.top_risk_entities[0]]: "#ef4444", [data.top_risk_entities[1]]: "#f97316", [data.top_risk_entities[2]]: "#f59e0b" },
    },
  ];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {selected && <DetailModal entity={selected} onClose={() => setSelected(null)} />}

      <div>
        <h1 className="text-2xl font-bold text-blue-400">
          AMR Global Response Engine — Intelligence Antimicrobienne
        </h1>
        <p className="text-blue-300/50 text-sm mt-1">
          Détection · Traitement · Confinement · Coopération Internationale AMR
        </p>
      </div>

      {/* 6 KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {(
          [
            ["Total Entités", data.total_entities, "text-blue-400"],
            [
              "Critique",
              data.risk_distribution["critique"] ?? 0,
              "text-red-400",
            ],
            [
              "Élevé",
              data.risk_distribution["élevé"] ?? 0,
              "text-orange-400",
            ],
            [
              "Composite Moyen",
              data.avg_composite.toFixed(1),
              "text-blue-300",
            ],
            [
              "Index AMR",
              `${data.avg_estimated_amr_index.toFixed(2)}/10`,
              "text-amber-400",
            ],
            [
              "Confiance",
              `${Math.round(data.confidence_score * 100)}%`,
              "text-emerald-400",
            ],
          ] as [string, string | number, string][]
        ).map(([l, v, c]) => (
          <div
            key={String(l)}
            className="bg-slate-900 border border-blue-700/30 rounded-xl p-3 text-center"
          >
            <div className={`text-xl font-bold ${c}`}>{v}</div>
            <div className="text-xs text-blue-300/40 mt-0.5 leading-tight">{l}</div>
          </div>
        ))}
      </div>

      {/* 4 GaugeRings */}
      <div className="bg-slate-900 border border-blue-700/30 rounded-xl p-5">
        <div className="grid grid-cols-4 gap-4">
          <GaugeRing value={avgDetection} label="Détection Moy." color="#ef4444" />
          <GaugeRing value={avgTreatment} label="Traitement Moy." color="#f97316" />
          <GaugeRing value={avgContainment} label="Confinement Moy." color="#06b6d4" />
          <GaugeRing value={avgCooperation} label="Coopération Moy." color="#a855f7" />
        </div>
      </div>

      {/* 4 DistBars */}
      <div className="bg-slate-900 border border-blue-700/30 rounded-xl p-5 grid grid-cols-1 md:grid-cols-2 gap-5">
        {dist4.map((d) => (
          <DistBar key={d.title} title={d.title} counts={d.counts} colors={d.colors} />
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
                : "bg-slate-900 border-blue-700/30 text-blue-400/70 hover:text-white"
            }`}
          >
            {pill}
          </button>
        ))}
      </div>

      {/* Entity Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {filtered.map((e) => (
          <div
            key={e.entity_id}
            onClick={() => setSelected(e)}
            className="bg-slate-900 border border-blue-700/30 rounded-xl p-4 cursor-pointer hover:border-blue-500 transition-colors"
          >
            <div className="flex items-center justify-between mb-1">
              <span className="font-bold text-white text-sm">{e.name}</span>
              <span className="text-xs text-blue-400/60">{e.entity_id}</span>
            </div>
            <div className="text-xs text-slate-500 mb-2">
              {e.country} · {e.sector}
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
                className="px-2 py-0.5 rounded text-xs font-medium bg-slate-800"
                style={{ color: PATTERN_COLORS[e.primary_pattern] || "#94a3b8" }}
              >
                {e.primary_pattern.replace(/_/g, " ")}
              </span>
            </div>
            <div className="text-2xl font-black text-white mb-1">
              {e.composite_score.toFixed(1)}
            </div>
            <div className="text-xs text-blue-400/60 mb-2">
              Index AMR: {e.estimated_amr_index.toFixed(2)}/10
            </div>
            <div className="text-xs text-blue-400 font-medium mb-2">
              Dét: {e.detection_score.toFixed(0)} · Trait: {e.treatment_score.toFixed(0)} ·
              Conf: {e.containment_score.toFixed(0)} · Coop: {e.cooperation_score.toFixed(0)}
            </div>
            <div className="text-xs text-slate-500">
              {e.outbreak_count} foyer{e.outbreak_count > 1 ? "s" : ""} · {e.last_updated}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
