"use client";

import { useEffect, useState } from "react";

// ── types ────────────────────────────────────────────────────────────────────
interface BatteryEntity {
  id: string;
  battery_type: string;
  region: string;
  recovery_score: number;
  toxicity_score: number;
  supply_score: number;
  governance_score: number;
  composite_score: number;
  risk_level: string;
  battery_pattern: string;
  severity: string;
  recommended_action: string;
  signal: string;
  recycling_facility_capacity: number;
  circular_economy_score: number;
}

interface Summary {
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
  avg_estimated_battery_circular_index: number;
}

// ── helpers ──────────────────────────────────────────────────────────────────
const RISK_COLOR: Record<string, string> = {
  critical: "text-red-400",
  high:     "text-orange-400",
  moderate: "text-yellow-400",
  low:      "text-slate-400",
};

const RISK_BG: Record<string, string> = {
  critical: "bg-red-500/20 border-red-500/40",
  high:     "bg-orange-500/20 border-orange-500/40",
  moderate: "bg-yellow-500/10 border-yellow-500/30",
  low:      "bg-slate-500/20 border-slate-500/40",
};

const SEVERITY_COLOR: Record<string, string> = {
  "crise_recyclage_lithium_systémique":       "text-red-400",
  "crise_chaîne_valeur_batteries_majeure":    "text-orange-400",
  "déficit_infrastructure_recyclage_structurel": "text-yellow-400",
  "recyclage_batteries_sous_surveillance":    "text-slate-300",
};

const PATTERN_ICON: Record<string, string> = {
  toxic_battery_dumping_crisis:              "☠️",
  lithium_cobalt_scarcity_trap:              "⛏️",
  recycling_infrastructure_gap:              "🏗️",
  second_life_market_failure:                "🔋",
  extended_producer_responsibility_collapse: "📋",
  none:                                      "—",
};

const BATTERY_ICON: Record<string, string> = {
  NMC_lithium_ion: "🔋",
  LFP_lithium:     "⚡",
  NCA_lithium:     "🌿",
  LCO_lithium:     "🔵",
};

// ── GaugeRing ────────────────────────────────────────────────────────────────
function GaugeRing({ score, label, color }: { score: number; label: string; color: string }) {
  const r = 36, circ = 2 * Math.PI * r;
  const fill = (Math.min(score, 100) / 100) * circ;
  return (
    <div className="flex flex-col items-center gap-2">
      <svg width={88} height={88} viewBox="0 0 88 88">
        <circle cx={44} cy={44} r={r} fill="none" stroke="#1e293b" strokeWidth={8} />
        <circle
          cx={44} cy={44} r={r} fill="none"
          stroke={color} strokeWidth={8}
          strokeDasharray={`${fill} ${circ}`}
          strokeLinecap="round"
          transform="rotate(-90 44 44)"
        />
        <text x={44} y={49} textAnchor="middle" fill="white" fontSize={14} fontWeight="bold">
          {Math.round(score)}
        </text>
      </svg>
      <span className="text-xs text-slate-400 text-center leading-tight">{label}</span>
    </div>
  );
}

// ── ScoreBar ─────────────────────────────────────────────────────────────────
function ScoreBar({ label, value, color }: { label: string; value: number; color: string }) {
  return (
    <div>
      <div className="flex justify-between text-xs text-slate-400 mb-1">
        <span>{label}</span><span>{value.toFixed(1)}</span>
      </div>
      <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
        <div className={`h-full rounded-full ${color}`} style={{ width: `${value}%` }} />
      </div>
    </div>
  );
}

// ── DistBar ───────────────────────────────────────────────────────────────────
function DistBar({ title, counts, colors }: { title: string; counts: Record<string, number>; colors: Record<string, string> }) {
  const total = Object.values(counts).reduce((a, b) => a + b, 0) || 1;
  return (
    <div className="bg-slate-900 border border-teal-500/30 rounded-xl p-4">
      <div className="text-xs text-slate-400 mb-2">{title}</div>
      <div className="flex gap-1 h-3 rounded-full overflow-hidden">
        {Object.entries(counts).map(([k, v]) => (
          <div
            key={k}
            className={colors[k] ?? "bg-slate-600"}
            style={{ width: `${(v / total) * 100}%` }}
            title={`${k}: ${v}`}
          />
        ))}
      </div>
      <div className="flex flex-wrap gap-2 mt-2 text-xs text-slate-500">
        {Object.entries(counts).map(([k, v]) => (
          <span key={k}>{k.replace(/_/g, " ")}: {v}</span>
        ))}
      </div>
    </div>
  );
}

// ── DetailModal ───────────────────────────────────────────────────────────────
function DetailModal({ entity, onClose }: { entity: BatteryEntity; onClose: () => void }) {
  const [tab, setTab] = useState<"overview" | "scores" | "action">("overview");

  useEffect(() => {
    const esc = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", esc);
    return () => window.removeEventListener("keydown", esc);
  }, [onClose]);

  const ringColor =
    entity.composite_score >= 60 ? "#ef4444"
    : entity.composite_score >= 40 ? "#f97316"
    : entity.composite_score >= 20 ? "#eab308"
    : "#14b8a6";

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4"
      onClick={onClose}
    >
      <div
        className="bg-slate-900 border border-teal-500/30 rounded-2xl w-full max-w-lg shadow-2xl"
        onClick={(e) => e.stopPropagation()}
      >
        {/* header */}
        <div className="flex items-center gap-4 p-5 border-b border-slate-800">
          <GaugeRing score={entity.composite_score} label="" color={ringColor} />
          <div className="flex-1 min-w-0">
            <h2 className="text-white font-bold text-lg truncate">
              {BATTERY_ICON[entity.battery_type] || "🔋"} {entity.id}
            </h2>
            <p className="text-slate-400 text-sm">{entity.battery_type.replace(/_/g, " ")} · {entity.region.replace(/_/g, " ")}</p>
            <div className="flex gap-2 mt-1 flex-wrap">
              <span className={`text-xs px-2 py-0.5 rounded-full border ${RISK_BG[entity.risk_level]}`}>
                {entity.risk_level} risk
              </span>
              <span className={`text-xs font-medium ${SEVERITY_COLOR[entity.severity]}`}>
                {entity.severity.replace(/_/g, " ")}
              </span>
            </div>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl">✕</button>
        </div>

        {/* tabs */}
        <div className="flex border-b border-slate-800">
          {(["overview", "scores", "action"] as const).map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`flex-1 py-2.5 text-sm font-medium capitalize transition-colors ${
                tab === t ? "text-teal-400 border-b-2 border-teal-400" : "text-slate-500 hover:text-slate-300"
              }`}
            >
              {t}
            </button>
          ))}
        </div>

        <div className="p-5 space-y-3">
          {tab === "overview" && (
            <>
              <div className="grid grid-cols-2 gap-3">
                {[
                  ["Pattern",                PATTERN_ICON[entity.battery_pattern] + " " + entity.battery_pattern.replace(/_/g, " ")],
                  ["Capacité Installation",  (entity.recycling_facility_capacity * 100).toFixed(0) + "%"],
                  ["Économie Circulaire",    (entity.circular_economy_score * 100).toFixed(0) + "%"],
                  ["Score Composite",        entity.composite_score.toFixed(1) + " / 100"],
                ].map(([label, value]) => (
                  <div key={label as string} className="bg-slate-800/60 rounded-lg p-3">
                    <div className="text-xs text-slate-400">{label}</div>
                    <div className="text-white font-semibold mt-0.5 text-sm">{value}</div>
                  </div>
                ))}
              </div>
              <div className="bg-slate-800/60 rounded-lg p-3">
                <div className="text-xs text-slate-400 mb-1">Signal de Recyclage</div>
                <div className="text-teal-300 text-sm leading-relaxed">{entity.signal}</div>
              </div>
            </>
          )}

          {tab === "scores" && (
            <div className="space-y-3">
              <ScoreBar label="Score de Récupération"   value={entity.recovery_score}   color="bg-green-500" />
              <ScoreBar label="Score de Toxicité"       value={entity.toxicity_score}   color="bg-red-500" />
              <ScoreBar label="Score d'Approvisionnement" value={entity.supply_score}   color="bg-teal-500" />
              <ScoreBar label="Score de Gouvernance"    value={entity.governance_score} color="bg-emerald-500" />
            </div>
          )}

          {tab === "action" && (
            <div className="space-y-3">
              <div className="bg-teal-500/10 border border-teal-500/30 rounded-xl p-4">
                <div className="text-xs text-teal-400 uppercase tracking-wide mb-1">Action Recommandée</div>
                <div className="text-white font-bold text-base capitalize">
                  {entity.recommended_action.replace(/_/g, " ")}
                </div>
              </div>
              {entity.risk_level === "critical" && (
                <div className="bg-red-500/10 border border-red-500/30 rounded-xl p-3 text-sm text-red-300">
                  ☠️ Risque critique — intervention immédiate requise pour décontamination et recyclage
                </div>
              )}
              {entity.risk_level === "high" && (
                <div className="bg-orange-500/10 border border-orange-500/30 rounded-xl p-3 text-sm text-orange-300">
                  ⚠️ Risque élevé — renforcement urgent de la filière recyclage
                </div>
              )}
              {entity.risk_level === "moderate" && (
                <div className="bg-yellow-500/10 border border-yellow-500/30 rounded-xl p-3 text-sm text-yellow-300">
                  🟡 Risque modéré — optimisation de l&apos;infrastructure recommandée
                </div>
              )}
              {entity.risk_level === "low" && (
                <div className="bg-slate-800/60 rounded-xl p-3 text-sm text-slate-400">
                  ✅ Filière de recyclage performante — veille économie circulaire continue
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

// ── EntityCard ────────────────────────────────────────────────────────────────
function EntityCard({ entity, onClick }: { entity: BatteryEntity; onClick: () => void }) {
  const ringColor =
    entity.composite_score >= 60 ? "#ef4444"
    : entity.composite_score >= 40 ? "#f97316"
    : entity.composite_score >= 20 ? "#eab308"
    : "#14b8a6";

  return (
    <div
      onClick={onClick}
      className="bg-slate-900 border border-slate-800 rounded-xl p-4 cursor-pointer hover:border-teal-500/30 hover:bg-slate-800/60 transition-all"
    >
      <div className="flex items-center gap-3">
        <GaugeRing score={entity.composite_score} label="" color={ringColor} />
        <div className="flex-1 min-w-0">
          <div className="text-white font-semibold truncate">
            {BATTERY_ICON[entity.battery_type] || "🔋"} {entity.id}
          </div>
          <div className="text-slate-400 text-xs">{entity.battery_type.replace(/_/g, " ")} · {entity.region.replace(/_/g, " ")}</div>
          <div className="flex gap-2 mt-1 flex-wrap">
            <span className={`text-xs px-2 py-0.5 rounded-full border ${RISK_BG[entity.risk_level]}`}>
              {entity.risk_level}
            </span>
          </div>
        </div>
        <div className="text-right shrink-0">
          <div className={`text-sm font-bold mt-1 ${SEVERITY_COLOR[entity.severity]}`}>
            {entity.severity.replace(/_/g, " ").split(" ")[0]}
          </div>
          <div className="text-xs text-slate-400 mt-1">
            circ. {(entity.circular_economy_score * 100).toFixed(0)}%
          </div>
        </div>
      </div>
      <div className="mt-2 text-xs text-slate-400">
        {PATTERN_ICON[entity.battery_pattern]} {entity.battery_pattern.replace(/_/g, " ")}
      </div>
    </div>
  );
}

// ── page ──────────────────────────────────────────────────────────────────────
export default function LithiumBatteryRecyclingEnginePage() {
  const [entities, setEntities]  = useState<BatteryEntity[]>([]);
  const [summary, setSummary]    = useState<Summary | null>(null);
  const [loading, setLoading]    = useState(true);
  const [selected, setSelected]  = useState<BatteryEntity | null>(null);
  const [filterRisk,    setFilterRisk]    = useState("all");
  const [filterPattern, setFilterPattern] = useState("all");

  useEffect(() => {
    setLoading(true);
    const params = new URLSearchParams();
    if (filterRisk    !== "all") params.set("risk",    filterRisk);
    if (filterPattern !== "all") params.set("pattern", filterPattern);
    fetch(`/api/lithium-battery-recycling-engine?${params}`)
      .then((r) => r.json())
      .then((data) => {
        setEntities(data.entities);
        setSummary(data.summary);
        setLoading(false);
      });
  }, [filterRisk, filterPattern]);

  const distributions: Array<{ title: string; counts: Record<string, number>; colors: Record<string, string> }> = [
    {
      title: "Patterns Batteries",
      counts: summary?.pattern_distribution ?? {},
      colors: {
        toxic_battery_dumping_crisis:              "bg-red-600",
        lithium_cobalt_scarcity_trap:              "bg-orange-500",
        recycling_infrastructure_gap:              "bg-yellow-500",
        second_life_market_failure:                "bg-teal-500",
        extended_producer_responsibility_collapse: "bg-emerald-500",
        none:                                      "bg-slate-500",
      },
    },
    {
      title: "Sévérité Recyclage",
      counts: summary?.severity_distribution ?? {},
      colors: {
        "crise_recyclage_lithium_systémique":       "bg-red-600",
        "crise_chaîne_valeur_batteries_majeure":    "bg-orange-500",
        "déficit_infrastructure_recyclage_structurel": "bg-yellow-500",
        "recyclage_batteries_sous_surveillance":    "bg-teal-400",
      },
    },
    {
      title: "Distribution du Risque",
      counts: summary?.risk_distribution ?? {},
      colors: { critical: "bg-red-600", high: "bg-orange-500", moderate: "bg-yellow-500", low: "bg-teal-400" },
    },
    {
      title: "Actions Prescrites",
      counts: summary?.action_distribution ?? {},
      colors: {
        intervention_urgente_décontamination_et_recyclage_critique: "bg-red-600",
        renforcement_filière_recyclage_lithium_accéléré:            "bg-orange-500",
        optimisation_infrastructure_collecte_et_traitement:         "bg-yellow-500",
        veille_économie_circulaire_batteries_continue:              "bg-teal-400",
      },
    },
  ];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
      <div className="max-w-6xl mx-auto space-y-6">

        {/* header */}
        <div>
          <h1 className="text-2xl font-bold text-white">
            Recyclage Batteries Lithium &amp; Économie Circulaire — Module 425
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Intelligence en temps réel sur la filière de recyclage des batteries lithium — détection des crises
            de contamination toxique, des pénuries de matières critiques et des défaillances d&apos;infrastructure,
            avec prescription d&apos;actions pour une économie circulaire des batteries durable.
          </p>
        </div>

        {/* KPI strip — 6 cards */}
        {summary && (
          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
            {[
              { label: "Entités",                  value: summary.total },
              { label: "Composite Moy.",            value: summary.avg_composite.toFixed(1),                          color: "text-teal-400" },
              { label: "Critique",                  value: summary.critical,                                           color: "text-red-400" },
              { label: "Élevé",                     value: summary.high,                                               color: "text-orange-400" },
              { label: "Modéré",                    value: summary.moderate,                                           color: "text-yellow-400" },
              { label: "Indice Circulaire Moy.",    value: summary.avg_estimated_battery_circular_index.toFixed(2),   color: "text-green-400" },
            ].map(({ label, value, color }) => (
              <div key={label} className="bg-slate-900 border border-teal-500/30 rounded-xl p-4">
                <div className="text-xs text-slate-400">{label}</div>
                <div className={`text-2xl font-bold mt-1 ${color ?? "text-white"}`}>{value}</div>
              </div>
            ))}
          </div>
        )}

        {/* 4 GaugeRings */}
        {summary && entities.length > 0 && (
          <div className="bg-slate-900 border border-teal-500/30 rounded-xl p-5">
            <div className="text-sm font-semibold text-slate-300 mb-4">Dimensions de Performance Recyclage</div>
            <div className="flex flex-wrap gap-6 justify-around">
              <GaugeRing
                score={Math.round(entities.reduce((a, e) => a + e.recovery_score, 0) / entities.length * 10) / 10}
                label="Récupération"
                color="#10b981"
              />
              <GaugeRing
                score={Math.round(entities.reduce((a, e) => a + e.toxicity_score, 0) / entities.length * 10) / 10}
                label="Toxicité"
                color="#ef4444"
              />
              <GaugeRing
                score={Math.round(entities.reduce((a, e) => a + e.supply_score, 0) / entities.length * 10) / 10}
                label="Approvisionnement"
                color="#14b8a6"
              />
              <GaugeRing
                score={Math.round(entities.reduce((a, e) => a + e.governance_score, 0) / entities.length * 10) / 10}
                label="Gouvernance"
                color="#22c55e"
              />
            </div>
          </div>
        )}

        {/* 4 DistBars */}
        {summary && (
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {distributions.map((d) => (
              <DistBar key={d.title} title={d.title} counts={d.counts} colors={d.colors} />
            ))}
          </div>
        )}

        {/* filter pills */}
        <div className="flex flex-wrap gap-2">
          {[
            { label: "Tous",          val: "all" },
            { label: "🔴 Critical",   val: "critical" },
            { label: "🟠 High",       val: "high" },
            { label: "🟡 Moderate",   val: "moderate" },
            { label: "🟢 Low",        val: "low" },
          ].map(({ label, val }) => (
            <button
              key={val}
              onClick={() => setFilterRisk(val)}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
                filterRisk === val
                  ? "bg-teal-700 text-white"
                  : "bg-slate-800 text-slate-400 hover:text-white"
              }`}
            >
              {label}
            </button>
          ))}
          <select
            value={filterPattern}
            onChange={(e) => setFilterPattern(e.target.value)}
            className="px-3 py-1.5 rounded-lg text-xs bg-slate-800 text-slate-300 border border-slate-700"
          >
            <option value="all">Tous Patterns</option>
            {[
              "toxic_battery_dumping_crisis",
              "lithium_cobalt_scarcity_trap",
              "recycling_infrastructure_gap",
              "second_life_market_failure",
              "extended_producer_responsibility_collapse",
              "none",
            ].map((p) => (
              <option key={p} value={p}>{p.replace(/_/g, " ")}</option>
            ))}
          </select>
        </div>

        {/* entity cards grid */}
        {loading ? (
          <div className="text-slate-400 text-center py-16">Analyse recyclage batteries lithium…</div>
        ) : entities.length === 0 ? (
          <div className="text-slate-500 text-center py-16">Aucune entité ne correspond aux filtres.</div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {entities.map((e) => (
              <EntityCard key={e.id} entity={e} onClick={() => setSelected(e)} />
            ))}
          </div>
        )}
      </div>

      {selected && <DetailModal entity={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
