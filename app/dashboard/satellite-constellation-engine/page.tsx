"use client";
import { useEffect, useState } from "react";

type SatEntity = {
  entity_id: string;
  name: string;
  country: string;
  sector: string;
  composite_score: number;
  orbital_collision_risk_score: number;
  signal_interference_score: number;
  space_debris_accumulation_score: number;
  regulatory_compliance_gap_score: number;
  risk_level: string;
  primary_pattern: string;
  key_signals: string[];
  estimated_satellite_index: number;
  last_updated: string;
  confidence_level: number;
};

type SatSummary = {
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
  entities: SatEntity[];
  avg_estimated_satellite_index: number;
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
  faible: "#16a34a",
  modéré: "#0891b2",
  "élevé": "#1d4ed8",
  critique: "#dc2626",
};

const PATTERN_COLORS: Record<string, string> = {
  constellation_stable: "#16a34a",
  kessler_syndrome_risk: "#dc2626",
  signal_warfare: "#7c3aed",
  debris_accumulation_crisis: "#b45309",
  regulatory_non_compliance: "#0891b2",
};

const RISK_BADGE: Record<string, string> = {
  faible: "bg-green-900 text-green-300",
  modéré: "bg-cyan-900 text-cyan-300",
  "élevé": "bg-blue-950 text-blue-400",
  critique: "bg-red-950 text-red-400",
};

function DetailModal({ entity, onClose }: { entity: SatEntity; onClose: () => void }) {
  const [tab, setTab] = useState<"scores" | "signaux" | "actions">("scores");

  useEffect(() => {
    const h = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
    };
    window.addEventListener("keydown", h);
    return () => window.removeEventListener("keydown", h);
  }, [onClose]);

  const patternMeta: Record<string, { severity_fr: string; action_fr: string; signal_fr: string }> = {
    kessler_syndrome_risk: {
      severity_fr: "Risque de Syndrome de Kessler",
      action_fr: "Protocole d'urgence déorbitation et surveillance renforcée",
      signal_fr: "Densité orbitale critique — risque cascade de débris",
    },
    signal_warfare: {
      severity_fr: "Guerre du Signal Orbital",
      action_fr: "Renforcement des fréquences cryptées et protection anti-brouillage",
      signal_fr: "Interférences signaux satellites détectées",
    },
    debris_accumulation_crisis: {
      severity_fr: "Crise Accumulation Débris",
      action_fr: "Mission de nettoyage orbital prioritaire",
      signal_fr: "Accumulation critique de débris spatiaux",
    },
    regulatory_non_compliance: {
      severity_fr: "Non-Conformité Réglementaire",
      action_fr: "Mise en conformité ITU et ITU-R urgente",
      signal_fr: "Violations réglementaires satellites détectées",
    },
    constellation_stable: {
      severity_fr: "Constellation Stable",
      action_fr: "Surveillance continue et optimisation orbite",
      signal_fr: "Constellation opérationnelle sous contrôle",
    },
  };

  const meta = patternMeta[entity.primary_pattern] ?? patternMeta.constellation_stable;

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
            <span className="text-lg font-bold text-white">{entity.name}</span>
            <span className="ml-2 text-cyan-500 text-xs">{entity.country}</span>
            <span className="ml-2 text-slate-500 text-xs">{entity.sector}</span>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl leading-none">
            ✕
          </button>
        </div>

        <div className="flex gap-2 mb-4">
          {(["scores", "signaux", "actions"] as const).map(t => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`px-3 py-1 rounded text-xs font-medium transition-colors ${
                tab === t
                  ? "bg-cyan-900 text-white"
                  : "bg-slate-900 text-slate-400 hover:text-white"
              }`}
            >
              {t === "scores" ? "Scores" : t === "signaux" ? "Signaux" : "Actions"}
            </button>
          ))}
        </div>

        {tab === "scores" && (
          <div className="grid grid-cols-2 gap-3 text-sm">
            {[
              ["Risque Collision Orbitale", entity.orbital_collision_risk_score, "#dc2626"],
              ["Interférence Signal",       entity.signal_interference_score,    "#7c3aed"],
              ["Accumulation Débris",       entity.space_debris_accumulation_score, "#b45309"],
              ["Écart Conformité Réglementaire", entity.regulatory_compliance_gap_score, "#0891b2"],
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
              <div className="text-cyan-500/60 text-xs mb-1">Score Composite Constellation</div>
              <div className="text-white font-bold text-2xl">
                {entity.composite_score.toFixed(2)}
              </div>
              <div className="mt-1 text-xs text-slate-400">
                Index Satellitaire Estimé: {entity.estimated_satellite_index.toFixed(2)}/10
                &nbsp;·&nbsp;Confiance: {(entity.confidence_level * 100).toFixed(0)}%
              </div>
            </div>
          </div>
        )}

        {tab === "signaux" && (
          <div className="space-y-3">
            <div className="bg-slate-900 border border-cyan-700/20 rounded-lg p-4 text-sm text-slate-200 leading-relaxed">
              <div className="text-cyan-500/60 text-xs mb-2">Signal Principal</div>
              <div className="text-slate-200">{meta.signal_fr}</div>
              <div className="mt-3 flex gap-2 flex-wrap">
                <span
                  className={`px-2 py-0.5 rounded text-xs font-medium ${
                    RISK_BADGE[entity.risk_level] || "bg-slate-700 text-slate-300"
                  }`}
                >
                  {entity.risk_level}
                </span>
                <span className="px-2 py-0.5 rounded text-xs font-medium bg-slate-800 text-slate-300">
                  {entity.primary_pattern.replace(/_/g, " ")}
                </span>
              </div>
            </div>
            <div className="bg-slate-900 border border-cyan-700/20 rounded-lg p-4">
              <div className="text-cyan-500/60 text-xs mb-2">Signaux Clés Détectés</div>
              <ul className="space-y-2">
                {entity.key_signals.map((s, i) => (
                  <li key={i} className="flex gap-2 text-xs text-slate-300">
                    <span className="text-cyan-500 mt-0.5 shrink-0">›</span>
                    <span>{s}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        )}

        {tab === "actions" && (
          <div className="space-y-3 text-sm">
            <div className="bg-slate-900 border border-cyan-700/20 rounded-lg p-3">
              <div className="text-cyan-500/60 text-xs mb-1">Sévérité du Patron</div>
              <div className="text-white font-medium">{meta.severity_fr}</div>
            </div>
            <div className="bg-slate-900 border border-cyan-700/20 rounded-lg p-3">
              <div className="text-cyan-500/60 text-xs mb-1">Action Recommandée</div>
              <div className="text-white font-medium">{meta.action_fr}</div>
            </div>
            <div className="bg-slate-900 border border-cyan-700/20 rounded-lg p-3">
              <div className="text-cyan-500/60 text-xs mb-1">Patron Orbital Détecté</div>
              <div className="text-cyan-400 font-medium capitalize">
                {entity.primary_pattern.replace(/_/g, " ")}
              </div>
            </div>
            <div className="bg-slate-900 border border-cyan-700/20 rounded-lg p-3">
              <div className="text-cyan-500/60 text-xs mb-1">Dernière Mise à Jour</div>
              <div className="text-slate-300 text-xs">{entity.last_updated}</div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function SatelliteConstellationDashboard() {
  const [data, setData] = useState<SatSummary | null>(null);
  const [riskFilter, setRiskFilter] = useState<string>("tous");
  const [selected, setSelected] = useState<SatEntity | null>(null);

  useEffect(() => {
    fetch("/api/satellite-constellation-engine")
      .then(r => r.json())
      .then(setData)
      .catch(console.error);
  }, []);

  if (!data) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center">
        <div className="text-cyan-500 text-lg animate-pulse">
          Initialisation du Moteur Constellation Satellitaire...
        </div>
      </div>
    );
  }

  const filtered = data.entities.filter(
    e => riskFilter === "tous" || e.risk_level === riskFilter
  );

  const avgOCR = data.entities.reduce((s, e) => s + e.orbital_collision_risk_score, 0) / (data.entities.length || 1);
  const avgSI  = data.entities.reduce((s, e) => s + e.signal_interference_score, 0) / (data.entities.length || 1);
  const avgSDA = data.entities.reduce((s, e) => s + e.space_debris_accumulation_score, 0) / (data.entities.length || 1);
  const avgRCG = data.entities.reduce((s, e) => s + e.regulatory_compliance_gap_score, 0) / (data.entities.length || 1);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {selected && <DetailModal entity={selected} onClose={() => setSelected(null)} />}

      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-cyan-500">
          Satellite Constellation Intelligence Engine
        </h1>
        <p className="text-blue-500/60 text-sm mt-1">
          Collision Orbitale · Signal · Débris · Conformité — Caelum Partners — Chaima Mhadbi, Fondatrice, Bruxelles
        </p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {[
          ["Total Constellations",         data.total_entities,                                                  "text-cyan-500"],
          ["Risque Critique",              data.risk_distribution["critique"] ?? 0,                             "text-red-400"],
          ["Risque Élevé",                 data.risk_distribution["élevé"] ?? 0,                                "text-blue-400"],
          ["Score Composite Moyen",        `${data.avg_composite.toFixed(1)}`,                                  "text-cyan-500"],
          ["Index Satellitaire Moyen",     `${data.avg_estimated_satellite_index.toFixed(2)}/10`,               "text-cyan-500"],
          ["Indice de Confiance",          `${(data.confidence_score * 100).toFixed(0)}%`,                      "text-blue-400"],
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
        <div className="text-xs text-cyan-500/60 mb-4 font-medium">Scores Moyens par Dimension Orbitale</div>
        <div className="grid grid-cols-4 gap-4">
          <GaugeRing value={avgOCR} label="Collision Orbitale" color="#dc2626" />
          <GaugeRing value={avgSI}  label="Interférence Signal" color="#7c3aed" />
          <GaugeRing value={avgSDA} label="Accumulation Débris" color="#b45309" />
          <GaugeRing value={avgRCG} label="Écart Conformité" color="#0891b2" />
        </div>
      </div>

      {/* Distribution Bars */}
      <div className="bg-slate-900 border border-cyan-700/30 rounded-xl p-5 grid grid-cols-1 md:grid-cols-2 gap-5">
        <DistBar
          title="Distribution des Niveaux de Risque"
          counts={data.risk_distribution}
          colors={RISK_COLORS}
        />
        <DistBar
          title="Distribution des Patrons Orbitaux"
          counts={data.pattern_distribution}
          colors={PATTERN_COLORS}
        />
      </div>

      {/* Alertes Critiques */}
      {data.critical_alerts.length > 0 && (
        <div className="bg-red-950/40 border border-red-700/40 rounded-xl p-4">
          <div className="text-red-400 text-xs font-semibold mb-2 uppercase tracking-wide">
            Alertes Critiques Constellation — Intervention Immédiate Requise
          </div>
          <div className="flex flex-wrap gap-2">
            {data.critical_alerts.map(name => (
              <span key={name} className="bg-red-900/60 text-red-300 text-xs px-2 py-0.5 rounded">
                {name}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Filter Pills */}
      <div className="flex flex-wrap gap-2">
        {["tous", "critique", "élevé", "modéré", "faible"].map(r => (
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
      </div>

      {/* Entity Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {filtered.map(e => (
          <div
            key={e.entity_id}
            onClick={() => setSelected(e)}
            className="bg-slate-900 border border-cyan-700/30 rounded-xl p-4 cursor-pointer hover:border-cyan-600 transition-colors"
          >
            <div className="flex items-center justify-between mb-1">
              <span className="font-bold text-white text-sm truncate max-w-[70%]">{e.name}</span>
              <span className="text-xs text-cyan-500/60 shrink-0">{e.country}</span>
            </div>
            <div className="text-xs text-slate-500 mb-2">{e.sector}</div>
            <div className="flex gap-1 mb-3 flex-wrap">
              <span
                className={`px-2 py-0.5 rounded text-xs font-medium ${
                  RISK_BADGE[e.risk_level] || "bg-slate-700 text-slate-300"
                }`}
              >
                {e.risk_level}
              </span>
              <span
                className="px-2 py-0.5 rounded text-xs font-medium bg-slate-800 text-slate-400"
                style={{ color: PATTERN_COLORS[e.primary_pattern] || "#94a3b8" }}
              >
                {e.primary_pattern.replace(/_/g, " ")}
              </span>
            </div>
            <div className="text-2xl font-black text-white mb-1">
              {e.composite_score.toFixed(2)}
            </div>
            <div className="text-xs text-cyan-500/60 mb-2">
              Index: {e.estimated_satellite_index.toFixed(2)}/10
            </div>
            <div className="text-xs text-blue-400/70 font-medium mb-2">
              OCR: {e.orbital_collision_risk_score.toFixed(0)} · SI: {e.signal_interference_score.toFixed(0)} · SDA: {e.space_debris_accumulation_score.toFixed(0)}
            </div>
            <div className="text-xs text-slate-400 truncate">{e.key_signals[0]}</div>
          </div>
        ))}
      </div>

      {/* Sources */}
      <div className="text-xs text-slate-600 flex flex-wrap gap-x-4 gap-y-1">
        <span className="text-slate-500 font-medium">Sources:</span>
        {data.data_sources.map(s => (
          <span key={s}>{s}</span>
        ))}
        <span className="ml-auto">v{data.engine_version} · {data.last_analysis.slice(0, 10)}</span>
      </div>
    </div>
  );
}
