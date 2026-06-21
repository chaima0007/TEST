"use client";
import { useEffect, useState } from "react";

type DNEEntity = {
  id: string;
  destination_type: string;
  region: string;
  gentrification_score: number;
  tax_evasion_score: number;
  inequality_score: number;
  governance_score: number;
  composite_score: number;
  risk_level: string;
  nomad_pattern: string;
  severity: string;
  recommended_action: string;
  signal: string;
  housing_price_spike: number;
  local_displacement_rate: number;
};

type DNESummary = {
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
  avg_estimated_nomad_impact_index: number;
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
      <span className="text-xs text-violet-400/70 text-center">{label}</span>
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
      <span className="text-xs text-violet-400/70 font-medium">{title}</span>
      <div className="flex h-3 rounded overflow-hidden gap-px">
        {Object.entries(counts).map(([k, v]) => (
          <div
            key={k}
            style={{ width: `${(v / total) * 100}%`, background: colors[k] || "#4c1d95" }}
            title={`${k}: ${v}`}
          />
        ))}
      </div>
      <div className="flex flex-wrap gap-x-3 gap-y-0.5">
        {Object.entries(counts).map(([k, v]) => (
          <span key={k} className="text-xs text-violet-400/60">
            <span style={{ color: colors[k] || "#5b21b6" }}>■</span> {k.replace(/_/g, " ")} {v}
          </span>
        ))}
      </div>
    </div>
  );
}

const RISK_COLORS: Record<string, string> = {
  low: "#16a34a",
  moderate: "#d97706",
  high: "#7c3aed",
  critical: "#dc2626",
};
const PATTERN_COLORS: Record<string, string> = {
  none: "#16a34a",
  housing_gentrification_explosion: "#dc2626",
  tax_base_erosion_crisis: "#d97706",
  cultural_displacement_trap: "#7c3aed",
  two_tier_economy_formation: "#2563eb",
  regulatory_arbitrage_race: "#0891b2",
};
const SEVERITY_COLORS: Record<string, string> = {
  impact_nomade_sous_surveillance: "#16a34a",
  inégalité_économique_structurelle: "#d97706",
  crise_impact_local_majeure: "#7c3aed",
  crise_gentrification_nomade_systémique: "#dc2626",
};
const ACTION_COLORS: Record<string, string> = {
  veille_impact_nomade_continue: "#16a34a",
  renforcement_politiques_intégration_économique: "#d97706",
  régulation_accélérée_marché_immobilier_nomade: "#7c3aed",
  intervention_urgente_protection_résidents_locaux: "#dc2626",
};

const RISK_BADGE: Record<string, string> = {
  low: "bg-green-900/60 text-green-300",
  moderate: "bg-amber-900/60 text-amber-300",
  high: "bg-violet-900/60 text-violet-300",
  critical: "bg-red-900/60 text-red-300",
};
const SEV_BADGE: Record<string, string> = {
  impact_nomade_sous_surveillance: "bg-green-900/40 text-green-400",
  inégalité_économique_structurelle: "bg-amber-900/40 text-amber-400",
  crise_impact_local_majeure: "bg-violet-900/40 text-violet-400",
  crise_gentrification_nomade_systémique: "bg-red-900/40 text-red-400",
};

function DetailModal({ entity, onClose }: { entity: DNEEntity; onClose: () => void }) {
  const [tab, setTab] = useState<"scores" | "signal" | "action">("scores");

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm"
      onClick={onClose}
    >
      <div
        className="bg-slate-900 border border-violet-700/40 rounded-2xl p-6 max-w-md w-full mx-4 shadow-2xl"
        onClick={e => e.stopPropagation()}
      >
        <div className="flex items-center justify-between mb-4">
          <div>
            <span className="font-bold text-white text-lg">{entity.id}</span>
            <span className="ml-2 text-violet-400/60 text-sm">{entity.region}</span>
          </div>
          <button
            onClick={onClose}
            className="text-slate-400 hover:text-white transition-colors text-xl leading-none"
          >
            ×
          </button>
        </div>

        <div className="flex gap-1 mb-4">
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

        <div className="flex gap-2 mb-4">
          {(["scores", "signal", "action"] as const).map(t => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`px-3 py-1 rounded text-xs font-medium transition-colors ${
                tab === t
                  ? "bg-violet-900 text-white"
                  : "bg-slate-800 text-slate-400 hover:text-white"
              }`}
            >
              {t === "scores" ? "Scores" : t === "signal" ? "Signal" : "Action"}
            </button>
          ))}
        </div>

        {tab === "scores" && (
          <div className="grid grid-cols-2 gap-3 text-sm">
            {[
              ["Score Gentrification",  entity.gentrification_score, "#dc2626"],
              ["Score Évasion Fiscale", entity.tax_evasion_score,    "#d97706"],
              ["Score Inégalité",       entity.inequality_score,     "#7c3aed"],
              ["Score Gouvernance",     entity.governance_score,     "#2563eb"],
            ].map(([l, v, c]) => (
              <div
                key={String(l)}
                className="bg-slate-800 border border-violet-700/20 rounded-lg p-3"
              >
                <div className="text-violet-400/60 text-xs mb-1">{String(l)}</div>
                <div className="text-white font-bold text-lg">{Number(v).toFixed(1)}</div>
                <div className="h-1.5 rounded mt-1 bg-slate-700">
                  <div
                    className="h-1.5 rounded"
                    style={{ width: `${Math.min(Number(v), 100)}%`, background: String(c) }}
                  />
                </div>
              </div>
            ))}
            <div className="col-span-2 bg-slate-800 border border-violet-700/20 rounded-lg p-3">
              <div className="text-violet-400/60 text-xs mb-1">Score Composite Impact Nomade</div>
              <div className="text-white font-bold text-2xl">
                {entity.composite_score.toFixed(1)}
              </div>
            </div>
          </div>
        )}

        {tab === "signal" && (
          <div className="bg-slate-800 border border-violet-700/20 rounded-lg p-4 text-sm text-slate-200 leading-relaxed">
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
              <div className="bg-slate-700 rounded p-2">
                <div className="text-violet-400/50 text-xs mb-0.5">Hausse Prix Logement</div>
                <div className="text-white text-sm font-medium">
                  {Math.round(entity.housing_price_spike * 100)}%
                </div>
              </div>
              <div className="bg-slate-700 rounded p-2">
                <div className="text-violet-400/50 text-xs mb-0.5">Taux Déplacement Local</div>
                <div className="text-white text-sm font-medium">
                  {Math.round(entity.local_displacement_rate * 100)}%
                </div>
              </div>
            </div>
          </div>
        )}

        {tab === "action" && (
          <div className="space-y-3 text-sm">
            <div className="bg-slate-800 border border-violet-700/20 rounded-lg p-3">
              <div className="text-violet-400/60 text-xs mb-1">Action Recommandée</div>
              <div className="text-white font-medium">
                {entity.recommended_action.replace(/_/g, " ")}
              </div>
            </div>
            <div className="bg-slate-800 border border-violet-700/20 rounded-lg p-3">
              <div className="text-violet-400/60 text-xs mb-1">Type de Destination</div>
              <div className="text-white font-medium capitalize">
                {entity.destination_type.replace(/_/g, " ")}
              </div>
            </div>
            <div className="bg-slate-800 border border-violet-700/20 rounded-lg p-3">
              <div className="text-violet-400/60 text-xs mb-1">Patron Détecté</div>
              <div className="text-violet-400 font-medium capitalize">
                {entity.nomad_pattern.replace(/_/g, " ")}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function DigitalNomadDashboard() {
  const [data, setData] = useState<{
    entities: DNEEntity[];
    summary: DNESummary;
    avg_gentrification: number;
  } | null>(null);
  const [riskFilter, setRiskFilter] = useState<string>("all");
  const [patFilter, setPatFilter] = useState<string>("all");
  const [selected, setSelected] = useState<DNEEntity | null>(null);

  useEffect(() => {
    fetch("/api/digital-nomad-engine")
      .then(r => r.json())
      .then(setData)
      .catch(console.error);
  }, []);

  if (!data) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center">
        <div className="text-violet-400 text-lg animate-pulse">
          Initialisation du Moteur Nomades Numériques...
        </div>
      </div>
    );
  }

  const { entities, summary, avg_gentrification } = data;
  const filtered = entities.filter(
    e =>
      (riskFilter === "all" || e.risk_level === riskFilter) &&
      (patFilter === "all" || e.nomad_pattern === patFilter)
  );

  const dists = [
    { title: "Niveau de Risque",     counts: summary.risk_distribution,     colors: RISK_COLORS     },
    { title: "Patron Nomade",        counts: summary.pattern_distribution,  colors: PATTERN_COLORS  },
    { title: "Sévérité",             counts: summary.severity_distribution, colors: SEVERITY_COLORS },
    { title: "Action Déclenchée",    counts: summary.action_distribution,   colors: ACTION_COLORS   },
  ] as Array<{ title: string; counts: Record<string, number>; colors: Record<string, string> }>;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {selected && <DetailModal entity={selected} onClose={() => setSelected(null)} />}

      <div>
        <h1 className="text-2xl font-bold text-violet-400">
          Économie Nomades Numériques &amp; Impact Local — Module 430
        </h1>
        <p className="text-amber-500/60 text-sm mt-1">
          Gentrification · Évasion Fiscale · Inégalité · Gouvernance — Caelum Partners — Chaima Mhadbi, Fondatrice, Bruxelles
        </p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {[
          ["Total Destinations",        summary.total,                                                             "text-violet-400"],
          ["Crise Gentrification",       summary.critical,                                                         "text-red-400"],
          ["Impact Majeur",              summary.high,                                                             "text-violet-500"],
          ["Composite Moyen",            `${summary.avg_composite.toFixed(1)}`,                                    "text-amber-500"],
          ["Index Impact Nomade",        `${summary.avg_estimated_nomad_impact_index.toFixed(2)}/10`,              "text-violet-400"],
          ["Gentrification Moy.",        `${avg_gentrification.toFixed(1)}`,                                       "text-amber-500"],
        ].map(([l, v, c]) => (
          <div
            key={String(l)}
            className="bg-slate-900 border border-violet-700/30 rounded-xl p-3 text-center"
          >
            <div className={`text-xl font-bold ${c}`}>{v}</div>
            <div className="text-xs text-violet-400/40 mt-0.5 leading-tight">{l}</div>
          </div>
        ))}
      </div>

      {/* Gauge Rings */}
      <div className="bg-slate-900 border border-violet-700/30 rounded-xl p-5">
        <div className="grid grid-cols-4 gap-4">
          <GaugeRing
            value={entities.reduce((s, e) => s + e.gentrification_score, 0) / (entities.length || 1)}
            label="Gentrification Moy."
            color="#dc2626"
          />
          <GaugeRing
            value={entities.reduce((s, e) => s + e.tax_evasion_score, 0) / (entities.length || 1)}
            label="Évasion Fiscale Moy."
            color="#d97706"
          />
          <GaugeRing
            value={entities.reduce((s, e) => s + e.inequality_score, 0) / (entities.length || 1)}
            label="Inégalité Moy."
            color="#7c3aed"
          />
          <GaugeRing
            value={entities.reduce((s, e) => s + e.governance_score, 0) / (entities.length || 1)}
            label="Gouvernance Moy."
            color="#2563eb"
          />
        </div>
      </div>

      {/* Distribution Bars */}
      <div className="bg-slate-900 border border-violet-700/30 rounded-xl p-5 grid grid-cols-1 md:grid-cols-2 gap-5">
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
                ? "bg-violet-900 border-violet-800 text-white"
                : "bg-slate-900 border-violet-700/30 text-violet-400/70 hover:text-white"
            }`}
          >
            {r}
          </button>
        ))}
        <span className="w-px h-5 self-center bg-violet-700/30" />
        {[
          "all",
          "none",
          "housing_gentrification_explosion",
          "tax_base_erosion_crisis",
          "cultural_displacement_trap",
          "two_tier_economy_formation",
          "regulatory_arbitrage_race",
        ].map(p => (
          <button
            key={p}
            onClick={() => setPatFilter(p)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${
              patFilter === p
                ? "bg-amber-950 border-amber-700 text-white"
                : "bg-slate-900 border-violet-700/30 text-violet-400/70 hover:text-white"
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
            className="bg-slate-900 border border-violet-700/30 rounded-xl p-4 cursor-pointer hover:border-violet-500 transition-colors"
          >
            <div className="flex items-center justify-between mb-1">
              <span className="font-bold text-white">{e.id}</span>
              <span className="text-xs text-violet-400/60">{e.region}</span>
            </div>
            <div className="text-xs text-slate-500 mb-2 capitalize">
              {e.destination_type.replace(/_/g, " ")}
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
            <div className="text-xs text-violet-400/60 mb-2 capitalize">
              {e.nomad_pattern.replace(/_/g, " ")}
            </div>
            <div className="text-xs text-amber-500/70 font-medium mb-2">
              Gentrif.: {e.gentrification_score.toFixed(1)} · Fiscal: {e.tax_evasion_score.toFixed(1)}
            </div>
            <div className="text-xs text-slate-400 truncate">{e.signal}</div>
          </div>
        ))}
      </div>
    </div>
  );
}
