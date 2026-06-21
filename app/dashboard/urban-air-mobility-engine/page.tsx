"use client";
import { useEffect, useState } from "react";

type UAMEntity = {
  id: string;
  vehicle_type: string;
  region: string;
  composite_score: number;
  risk_level: string;
  safety_score: number;
  infrastructure_score: number;
  regulatory_score: number;
  equity_score: number;
  patterns: string[];
  collision_avoidance_gap: number;
  noise_impact_residential: number;
  equity_access_gap: number;
  regulatory_certification_delay: number;
  battery_energy_density_risk: number;
};

type UAMSummary = {
  total: number;
  critique: number;
  eleve: number;
  modere: number;
  faible: number;
  avg_composite: number;
  avg_safety: number;
  avg_infrastructure: number;
  avg_regulatory: number;
  avg_equity: number;
  top_patterns: string[];
  dominant_region: string;
  avg_estimated_uam_readiness_index: number;
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
      <span className="text-xs text-sky-500/70 text-center">{label}</span>
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
      <span className="text-xs text-sky-500/70 font-medium">{title}</span>
      <div className="flex h-3 rounded overflow-hidden gap-px">
        {Object.entries(counts).map(([k, v]) => (
          <div
            key={k}
            style={{ width: `${(v / total) * 100}%`, background: colors[k] || "#0369a1" }}
            title={`${k}: ${v}`}
          />
        ))}
      </div>
      <div className="flex flex-wrap gap-x-3 gap-y-0.5">
        {Object.entries(counts).map(([k, v]) => (
          <span key={k} className="text-xs text-sky-500/60">
            <span style={{ color: colors[k] || "#0284c7" }}>■</span> {k.replace(/_/g, " ")} {v}
          </span>
        ))}
      </div>
    </div>
  );
}

const RISK_COLORS: Record<string, string> = {
  faible: "#0284c7",
  modéré: "#0ea5e9",
  élevé: "#0369a1",
  critique: "#dc2626",
};
const PATTERN_COLORS: Record<string, string> = {
  airspace_collision_risk: "#dc2626",
  noise_pollution_community_conflict: "#7c3aed",
  elite_mobility_gentrification: "#b45309",
  battery_fire_safety_gap: "#ea580c",
  regulatory_certification_bottleneck: "#0891b2",
};
const RISK_BADGE: Record<string, string> = {
  faible: "bg-sky-900 text-sky-300",
  modéré: "bg-blue-900 text-blue-300",
  élevé: "bg-sky-950 text-sky-400",
  critique: "bg-red-950 text-red-400",
};

function DetailModal({ entity, onClose }: { entity: UAMEntity; onClose: () => void }) {
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
        className="bg-slate-950 border border-sky-700/30 rounded-xl w-full max-w-lg p-6 shadow-2xl"
        onClick={e => e.stopPropagation()}
      >
        <div className="flex items-center justify-between mb-4">
          <div>
            <span className="text-lg font-bold text-white">{entity.id}</span>
            <span className="ml-2 text-sky-500 text-xs">{entity.region}</span>
            <span className="ml-2 text-slate-500 text-xs">
              {entity.vehicle_type.replace(/_/g, " ")}
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
                  ? "bg-sky-900 text-white"
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
              ["Score Sécurité",        entity.safety_score,         "#dc2626"],
              ["Score Infrastructure",  entity.infrastructure_score, "#0891b2"],
              ["Score Réglementation",  entity.regulatory_score,     "#7c3aed"],
              ["Score Équité",          entity.equity_score,         "#059669"],
            ].map(([l, v, c]) => (
              <div
                key={String(l)}
                className="bg-slate-900 border border-sky-700/20 rounded-lg p-3"
              >
                <div className="text-sky-500/60 text-xs mb-1">{String(l)}</div>
                <div className="text-white font-bold text-lg">{Number(v).toFixed(1)}</div>
                <div className="h-1.5 rounded mt-1 bg-slate-800">
                  <div
                    className="h-1.5 rounded"
                    style={{ width: `${Math.min(Number(v), 100)}%`, background: String(c) }}
                  />
                </div>
              </div>
            ))}
            <div className="col-span-2 bg-slate-900 border border-sky-700/20 rounded-lg p-3">
              <div className="text-sky-500/60 text-xs mb-1">Score Composite UAM</div>
              <div className="text-white font-bold text-2xl">
                {entity.composite_score.toFixed(1)}
              </div>
            </div>
          </div>
        )}

        {tab === "signal" && (
          <div className="bg-slate-900 border border-sky-700/20 rounded-lg p-4 text-sm text-slate-200 leading-relaxed">
            <div className="mb-3 flex gap-2 flex-wrap">
              <span
                className={`px-2 py-0.5 rounded text-xs font-medium ${
                  RISK_BADGE[entity.risk_level] || "bg-slate-700 text-slate-300"
                }`}
              >
                {entity.risk_level}
              </span>
            </div>
            <div className="mt-3 grid grid-cols-2 gap-2">
              <div className="bg-slate-800 rounded p-2">
                <div className="text-sky-500/50 text-xs mb-0.5">Évitement Collision</div>
                <div className="text-white text-sm font-medium">
                  {Math.round(entity.collision_avoidance_gap * 100)}%
                </div>
              </div>
              <div className="bg-slate-800 rounded p-2">
                <div className="text-sky-500/50 text-xs mb-0.5">Risque Batterie</div>
                <div className="text-white text-sm font-medium">
                  {Math.round(entity.battery_energy_density_risk * 100)}%
                </div>
              </div>
              <div className="bg-slate-800 rounded p-2">
                <div className="text-sky-500/50 text-xs mb-0.5">Impact Sonore</div>
                <div className="text-white text-sm font-medium">
                  {Math.round(entity.noise_impact_residential * 100)}%
                </div>
              </div>
              <div className="bg-slate-800 rounded p-2">
                <div className="text-sky-500/50 text-xs mb-0.5">Délai Certification</div>
                <div className="text-white text-sm font-medium">
                  {Math.round(entity.regulatory_certification_delay * 100)}%
                </div>
              </div>
            </div>
            {entity.patterns.length > 0 && (
              <div className="mt-3">
                <div className="text-sky-500/50 text-xs mb-1">Patterns Détectés</div>
                <div className="flex flex-wrap gap-1">
                  {entity.patterns.map(p => (
                    <span key={p} className="px-2 py-0.5 rounded text-xs bg-red-950 text-red-300">
                      {p.replace(/_/g, " ")}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {tab === "action" && (
          <div className="space-y-3 text-sm">
            <div className="bg-slate-900 border border-sky-700/20 rounded-lg p-3">
              <div className="text-sky-500/60 text-xs mb-1">Type de Véhicule</div>
              <div className="text-white font-medium capitalize">
                {entity.vehicle_type.replace(/_/g, " ")}
              </div>
            </div>
            <div className="bg-slate-900 border border-sky-700/20 rounded-lg p-3">
              <div className="text-sky-500/60 text-xs mb-1">Écart Équité d&apos;Accès</div>
              <div className="text-white font-medium">
                {Math.round(entity.equity_access_gap * 100)}%
              </div>
            </div>
            <div className="bg-slate-900 border border-sky-700/20 rounded-lg p-3">
              <div className="text-sky-500/60 text-xs mb-1">Patterns de Risque</div>
              <div className="flex flex-wrap gap-1 mt-1">
                {entity.patterns.length > 0 ? (
                  entity.patterns.map(p => (
                    <span key={p} className="text-sky-400 font-medium capitalize text-xs">
                      {p.replace(/_/g, " ")}
                    </span>
                  ))
                ) : (
                  <span className="text-green-400 text-xs">Aucun pattern critique détecté</span>
                )}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function UrbanAirMobilityDashboard() {
  const [data, setData] = useState<{
    entities: UAMEntity[];
    summary: UAMSummary;
    module_id: number;
    module_name: string;
  } | null>(null);
  const [riskFilter, setRiskFilter] = useState<string>("all");
  const [patFilter, setPatFilter] = useState<string>("all");
  const [selected, setSelected] = useState<UAMEntity | null>(null);

  useEffect(() => {
    fetch("/api/urban-air-mobility-engine")
      .then(r => r.json())
      .then(setData)
      .catch(console.error);
  }, []);

  if (!data) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center">
        <div className="text-sky-500 text-lg animate-pulse">
          Initialisation du Moteur Mobilité Aérienne Urbaine...
        </div>
      </div>
    );
  }

  const { entities, summary } = data;
  const filtered = entities.filter(
    e =>
      (riskFilter === "all" || e.risk_level === riskFilter) &&
      (patFilter === "all" || e.patterns.includes(patFilter))
  );

  const riskDist: Record<string, number> = {};
  for (const e of entities) {
    riskDist[e.risk_level] = (riskDist[e.risk_level] || 0) + 1;
  }
  const patDist: Record<string, number> = {};
  for (const e of entities) {
    for (const p of e.patterns) {
      patDist[p] = (patDist[p] || 0) + 1;
    }
  }

  const dists = [
    { title: "Niveau de Risque",        counts: riskDist,  colors: RISK_COLORS    },
    { title: "Patterns de Risque UAM",  counts: patDist,   colors: PATTERN_COLORS },
  ] as Array<{ title: string; counts: Record<string, number>; colors: Record<string, string> }>;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {selected && <DetailModal entity={selected} onClose={() => setSelected(null)} />}

      <div>
        <h1 className="text-2xl font-bold text-sky-500">
          Mobilité Aérienne Urbaine &amp; Véhicules Volants — Module 439
        </h1>
        <p className="text-blue-500/60 text-sm mt-1">
          Sécurité · Infrastructure · Réglementation · Équité — Caelum Partners — Chaima Mhadbi, Fondatrice, Bruxelles
        </p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {[
          ["Total Véhicules",              summary.total,                                                             "text-sky-500"],
          ["Risque Critique",              summary.critique,                                                          "text-red-400"],
          ["Risque Élevé",                 summary.eleve,                                                             "text-sky-700"],
          ["Risque Modéré",                summary.modere,                                                            "text-blue-400"],
          ["Risque Faible",                summary.faible,                                                            "text-sky-300"],
          ["Index Readiness UAM",          `${summary.avg_estimated_uam_readiness_index.toFixed(2)}/10`,              "text-sky-500"],
        ].map(([l, v, c]) => (
          <div
            key={String(l)}
            className="bg-slate-900 border border-sky-700/30 rounded-xl p-3 text-center"
          >
            <div className={`text-xl font-bold ${c}`}>{v}</div>
            <div className="text-xs text-sky-500/40 mt-0.5 leading-tight">{l}</div>
          </div>
        ))}
      </div>

      {/* Gauge Rings */}
      <div className="bg-slate-900 border border-sky-700/30 rounded-xl p-5">
        <div className="grid grid-cols-4 gap-4">
          <GaugeRing
            value={summary.avg_safety}
            label="Sécurité Moy."
            color="#dc2626"
          />
          <GaugeRing
            value={summary.avg_infrastructure}
            label="Infrastructure Moy."
            color="#0891b2"
          />
          <GaugeRing
            value={summary.avg_regulatory}
            label="Réglementation Moy."
            color="#7c3aed"
          />
          <GaugeRing
            value={summary.avg_equity}
            label="Équité Moy."
            color="#059669"
          />
        </div>
      </div>

      {/* Distribution Bars */}
      <div className="bg-slate-900 border border-sky-700/30 rounded-xl p-5 grid grid-cols-1 md:grid-cols-2 gap-5">
        {dists.map(d => (
          <DistBar key={d.title} {...d} />
        ))}
      </div>

      {/* Filter Pills */}
      <div className="flex flex-wrap gap-2">
        {["all", "faible", "modéré", "élevé", "critique"].map(r => (
          <button
            key={r}
            onClick={() => setRiskFilter(r)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${
              riskFilter === r
                ? "bg-sky-900 border-sky-800 text-white"
                : "bg-slate-900 border-sky-700/30 text-sky-500/70 hover:text-white"
            }`}
          >
            {r}
          </button>
        ))}
        <span className="w-px h-5 self-center bg-sky-700/30" />
        {[
          "all",
          "airspace_collision_risk",
          "noise_pollution_community_conflict",
          "elite_mobility_gentrification",
          "battery_fire_safety_gap",
          "regulatory_certification_bottleneck",
        ].map(p => (
          <button
            key={p}
            onClick={() => setPatFilter(p)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${
              patFilter === p
                ? "bg-blue-950 border-blue-700 text-white"
                : "bg-slate-900 border-sky-700/30 text-sky-500/70 hover:text-white"
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
            className="bg-slate-900 border border-sky-700/30 rounded-xl p-4 cursor-pointer hover:border-sky-600 transition-colors"
          >
            <div className="flex items-center justify-between mb-1">
              <span className="font-bold text-white">{e.id}</span>
              <span className="text-xs text-sky-500/60">{e.region}</span>
            </div>
            <div className="text-xs text-slate-500 mb-2 capitalize">
              {e.vehicle_type.replace(/_/g, " ")}
            </div>
            <div className="flex gap-1 mb-3 flex-wrap">
              <span
                className={`px-2 py-0.5 rounded text-xs font-medium ${
                  RISK_BADGE[e.risk_level] || "bg-slate-700 text-slate-300"
                }`}
              >
                {e.risk_level}
              </span>
            </div>
            <div className="text-2xl font-black text-white mb-1">
              {e.composite_score.toFixed(1)}
            </div>
            <div className="flex flex-wrap gap-1 mb-2">
              {e.patterns.map(p => (
                <span key={p} className="text-xs text-red-400/70 capitalize">
                  {p.replace(/_/g, " ")}
                </span>
              ))}
              {e.patterns.length === 0 && (
                <span className="text-xs text-green-500/60">Aucun pattern critique</span>
              )}
            </div>
            <div className="text-xs text-sky-500/70 font-medium mb-2">
              Séc.: {e.safety_score.toFixed(1)} · Infra.: {e.infrastructure_score.toFixed(1)}
            </div>
            <div className="text-xs text-slate-400">
              Rég.: {e.regulatory_score.toFixed(1)} · Éq.: {e.equity_score.toFixed(1)}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
