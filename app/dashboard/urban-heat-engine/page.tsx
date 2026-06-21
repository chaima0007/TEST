"use client";
import { useEffect, useState } from "react";

// ── Types ─────────────────────────────────────────────────────────────────────

type RiskLevel   = "critical" | "high" | "moderate" | "low";
type HeatPattern = "lethal_heat_dome" | "cooling_infrastructure_collapse" | "green_desert_city" | "heat_poverty_trap" | "compound_climate_crisis" | "none";
type Severity    = "urgence_chaleur_urbaine_létale" | "crise_chaleur_urbaine_majeure" | "stress_thermique_structurel" | "chaleur_urbaine_gérée";
type HeatAction  = "plan_urgence_chaleur_urbaine" | "infrastructure_refroidissement_urgente" | "verdissement_urbain_accéléré" | "veille_chaleur_urbaine_continue";

interface UheEntity {
  id: string;
  city_type: string;
  region: string;
  thermal_score: number;
  mortality_score: number;
  adaptation_score: number;
  equity_score: number;
  composite_score: number;
  risk_level: RiskLevel;
  heat_pattern: HeatPattern;
  severity: Severity;
  recommended_action: HeatAction;
  signal: string;
  heat_island_intensity_index: number;
  extreme_heat_mortality_rate: number;
}

interface UheSummary {
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
  avg_estimated_urban_heat_index: number;
  avg_thermal_score: number;
  avg_mortality_score: number;
  avg_adaptation_score: number;
  avg_equity_score: number;
}

// ── Metadata ──────────────────────────────────────────────────────────────────

const RISK_META: Record<RiskLevel, { label: string; color: string; ring: string; badge: string }> = {
  critical: { label: "Urgence Létale",  color: "text-red-400",    ring: "#ef4444", badge: "bg-red-900/60 text-red-300 border-red-700" },
  high:     { label: "Crise Majeure",   color: "text-orange-400", ring: "#f97316", badge: "bg-orange-900/60 text-orange-300 border-orange-700" },
  moderate: { label: "Stress Thermique", color: "text-amber-400", ring: "#f59e0b", badge: "bg-amber-900/60 text-amber-300 border-amber-700" },
  low:      { label: "Sous Contrôle",   color: "text-emerald-400", ring: "#10b981", badge: "bg-emerald-900/60 text-emerald-300 border-emerald-700" },
};

const PATTERN_LABELS: Record<HeatPattern, string> = {
  lethal_heat_dome:                "Dôme de Chaleur Létale",
  cooling_infrastructure_collapse: "Effondrement Infra. Refroidissement",
  green_desert_city:               "Ville Désert Vert",
  heat_poverty_trap:               "Trappe Chaleur & Pauvreté",
  compound_climate_crisis:         "Crise Climatique Composée",
  none:                            "Aucun",
};

const SEV_LABELS: Record<Severity, string> = {
  urgence_chaleur_urbaine_létale: "Urgence Létale",
  crise_chaleur_urbaine_majeure:  "Crise Majeure",
  stress_thermique_structurel:    "Stress Structurel",
  chaleur_urbaine_gérée:          "Gérée",
};

const ACTION_LABELS: Record<HeatAction, string> = {
  plan_urgence_chaleur_urbaine:              "Plan Urgence Chaleur Urbaine",
  infrastructure_refroidissement_urgente:    "Infrastructure Refroidissement Urgente",
  "verdissement_urbain_accéléré":            "Verdissement Urbain Accéléré",
  veille_chaleur_urbaine_continue:           "Veille Chaleur Urbaine Continue",
};

const RISK_COLORS: Record<string, string> = {
  critical: "#ef4444", high: "#f97316", moderate: "#f59e0b", low: "#10b981",
};

const PAT_COLORS: Record<string, string> = {
  lethal_heat_dome:                "#ef4444",
  cooling_infrastructure_collapse: "#f97316",
  green_desert_city:               "#22c55e",
  heat_poverty_trap:               "#a855f7",
  compound_climate_crisis:         "#f59e0b",
  none:                            "#10b981",
};

const SEV_COLORS: Record<string, string> = {
  urgence_chaleur_urbaine_létale: "#ef4444",
  crise_chaleur_urbaine_majeure:  "#f97316",
  stress_thermique_structurel:    "#f59e0b",
  chaleur_urbaine_gérée:          "#10b981",
};

const ACT_COLORS: Record<string, string> = {
  plan_urgence_chaleur_urbaine:           "#ef4444",
  infrastructure_refroidissement_urgente: "#f97316",
  "verdissement_urbain_accéléré":         "#22c55e",
  veille_chaleur_urbaine_continue:        "#10b981",
};

// ── Components ────────────────────────────────────────────────────────────────

function GaugeRing({ value, label, color }: { value: number; label: string; color: string }) {
  const r = 36;
  const circ = 2 * Math.PI * r;
  const fill = circ * (1 - value / 100);
  return (
    <div className="flex flex-col items-center gap-1">
      <svg width="88" height="88" viewBox="0 0 88 88">
        <circle cx="44" cy="44" r={r} fill="none" stroke="#0f172a" strokeWidth="8"/>
        <circle cx="44" cy="44" r={r} fill="none" stroke={color} strokeWidth="8"
          strokeDasharray={circ} strokeDashoffset={fill}
          strokeLinecap="round" transform="rotate(-90 44 44)"/>
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
          <div key={k} style={{ width: `${v / total * 100}%`, background: colors[k] || "#475569" }} title={`${k}: ${v}`}/>
        ))}
      </div>
      <div className="flex flex-wrap gap-x-3 gap-y-0.5">
        {Object.entries(counts).map(([k, v]) => (
          <span key={k} className="text-xs text-slate-400">
            <span style={{ color: colors[k] || "#94a3b8" }}>■</span> {k.replace(/_/g, " ")} {v}
          </span>
        ))}
      </div>
    </div>
  );
}

function DetailModal({ entity, onClose }: { entity: UheEntity; onClose: () => void }) {
  const [tab, setTab] = useState<"scores" | "analyse" | "actions">("scores");
  const risk = RISK_META[entity.risk_level];

  useEffect(() => {
    const h = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", h);
    return () => window.removeEventListener("keydown", h);
  }, [onClose]);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/75" onClick={onClose}>
      <div className="bg-slate-900 border border-orange-700/30 rounded-xl w-full max-w-lg p-6 shadow-2xl" onClick={e => e.stopPropagation()}>
        <div className="flex items-center justify-between mb-4">
          <div>
            <span className="text-lg font-bold text-white">{entity.id}</span>
            <span className="ml-2 text-orange-400 text-xs">{entity.city_type.replace(/_/g, " ")}</span>
            <span className="ml-2 text-slate-400 text-xs">{entity.region}</span>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl leading-none">✕</button>
        </div>

        <div className="flex gap-2 mb-4">
          {(["scores", "analyse", "actions"] as const).map(t => (
            <button key={t} onClick={() => setTab(t)}
              className={`px-3 py-1 rounded text-xs font-medium transition-colors ${tab === t ? "bg-orange-700 text-white" : "bg-slate-800 text-slate-400 hover:text-white"}`}>
              {t === "scores" ? "Scores" : t === "analyse" ? "Analyse" : "Actions"}
            </button>
          ))}
        </div>

        {tab === "scores" && (
          <div className="grid grid-cols-2 gap-3 text-sm">
            {[
              ["Thermique",  entity.thermal_score,    "#ef4444"],
              ["Mortalité",  entity.mortality_score,  "#f97316"],
              ["Adaptation", entity.adaptation_score, "#f59e0b"],
              ["Équité",     entity.equity_score,     "#a855f7"],
            ].map(([l, v, c]) => (
              <div key={String(l)} className="bg-slate-800 border border-orange-700/20 rounded-lg p-3">
                <div className="text-slate-400 text-xs mb-1">{String(l)}</div>
                <div className="text-white font-bold text-lg">{Number(v).toFixed(1)}</div>
                <div className="h-1.5 rounded mt-1 bg-slate-700">
                  <div className="h-1.5 rounded" style={{ width: `${Math.min(Number(v), 100)}%`, background: String(c) }}/>
                </div>
              </div>
            ))}
            <div className="col-span-2 bg-slate-800 border border-orange-700/20 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Score Composite</div>
              <div className="text-white font-bold text-2xl">{entity.composite_score.toFixed(1)}</div>
            </div>
          </div>
        )}

        {tab === "analyse" && (
          <div className="bg-slate-800 border border-orange-700/20 rounded-lg p-4 text-sm text-slate-200 leading-relaxed">
            {entity.signal}
            <div className="mt-3 flex gap-2 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium border ${risk?.badge || "bg-slate-700 text-slate-300"}`}>
                {entity.risk_level}
              </span>
              <span className="px-2 py-0.5 rounded text-xs font-medium bg-slate-700 text-amber-300">
                {SEV_LABELS[entity.severity] || entity.severity.replace(/_/g, " ")}
              </span>
              <span className="px-2 py-0.5 rounded text-xs font-medium bg-slate-700 text-orange-300">
                {PATTERN_LABELS[entity.heat_pattern] || entity.heat_pattern.replace(/_/g, " ")}
              </span>
            </div>
            <div className="mt-3 grid grid-cols-2 gap-2 text-xs text-slate-400">
              <div>Intensité ilot chaleur: <span className="text-orange-300">{Math.round(entity.heat_island_intensity_index * 100)}%</span></div>
              <div>Mortalité chaleur: <span className="text-red-300">{Math.round(entity.extreme_heat_mortality_rate * 100)}%</span></div>
            </div>
          </div>
        )}

        {tab === "actions" && (
          <div className="space-y-3 text-sm">
            <div className="bg-slate-800 border border-orange-700/20 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Action Recommandée</div>
              <div className="text-white font-medium">
                {ACTION_LABELS[entity.recommended_action] || entity.recommended_action.replace(/_/g, " ")}
              </div>
            </div>
            <div className="bg-slate-800 border border-orange-700/20 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Sévérité</div>
              <div className="text-white font-medium">{SEV_LABELS[entity.severity] || entity.severity.replace(/_/g, " ")}</div>
            </div>
            <div className="bg-slate-800 border border-orange-700/20 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Patron de Chaleur</div>
              <div className="text-white font-medium">{PATTERN_LABELS[entity.heat_pattern] || entity.heat_pattern.replace(/_/g, " ")}</div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

// ── Dashboard ─────────────────────────────────────────────────────────────────

export default function UrbanHeatDashboard() {
  const [data, setData]         = useState<{ entities: UheEntity[]; summary: UheSummary } | null>(null);
  const [riskFilter, setRisk]   = useState<string>("all");
  const [regFilter, setReg]     = useState<string>("all");
  const [selected, setSelected] = useState<UheEntity | null>(null);

  useEffect(() => {
    fetch("/api/urban-heat-engine")
      .then(r => r.json())
      .then(setData)
      .catch(console.error);
  }, []);

  if (!data) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-orange-400 text-lg animate-pulse">Initialisation du Moteur Chaleur Urbaine — Module 354...</div>
    </div>
  );

  const { entities, summary } = data;

  const regions  = ["all", ...Array.from(new Set(entities.map(e => e.region)))];
  const filtered = entities.filter(e =>
    (riskFilter === "all" || e.risk_level === riskFilter) &&
    (regFilter  === "all" || e.region === regFilter)
  );

  const dists = [
    { title: "Niveau de Risque",        counts: summary.risk_distribution,     colors: RISK_COLORS },
    { title: "Patron de Chaleur",        counts: summary.pattern_distribution,  colors: PAT_COLORS  },
    { title: "Sévérité",                 counts: summary.severity_distribution, colors: SEV_COLORS  },
    { title: "Action Recommandée",       counts: summary.action_distribution,   colors: ACT_COLORS  },
  ] as Array<{ title: string; counts: Record<string, number>; colors: Record<string, string> }>;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-300 p-6 space-y-6">
      {selected && <DetailModal entity={selected} onClose={() => setSelected(null)}/>}

      {/* En-tête */}
      <div>
        <h1 className="text-2xl font-bold text-orange-400">
          Chaleur Urbaine &amp; Urgence Climatique Ville — Module 354
        </h1>
        <p className="text-slate-400 text-sm mt-1">
          Thermique · Mortalité · Adaptation · Équité — Intelligence Chaleur Urbaine — Caelum Partners
        </p>
        <p className="text-slate-500 text-xs mt-0.5">Chaima Mhadbi — Bruxelles</p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {[
          ["Total Villes",          summary.total_entities,                                       "text-slate-300"],
          ["Urgence Létale",        summary.critical_count,                                       "text-red-400"],
          ["Crise Majeure",         summary.high_count,                                           "text-orange-400"],
          ["Composite Moyen",       summary.avg_composite.toFixed(1),                             "text-orange-300"],
          ["Index Chaleur Urbaine", summary.avg_estimated_urban_heat_index.toFixed(2) + "/10",    "text-red-300"],
          ["Thermique Moyen",       summary.avg_thermal_score != null ? summary.avg_thermal_score.toFixed(1) : "—", "text-amber-400"],
        ].map(([l, v, c]) => (
          <div key={String(l)} className="bg-slate-900 border border-orange-700/30 rounded-xl p-3 text-center">
            <div className={`text-xl font-bold ${c}`}>{v}</div>
            <div className="text-xs text-slate-500 mt-0.5 leading-tight">{l}</div>
          </div>
        ))}
      </div>

      {/* Gauge Rings */}
      <div className="bg-slate-900 border border-orange-700/30 rounded-xl p-5">
        <p className="text-xs text-slate-500 mb-4 font-medium">Scores Moyens par Dimension</p>
        <div className="grid grid-cols-4 gap-4">
          <GaugeRing value={summary.avg_thermal_score    ?? 0} label="Thermique"  color="#ef4444"/>
          <GaugeRing value={summary.avg_mortality_score  ?? 0} label="Mortalité"  color="#f97316"/>
          <GaugeRing value={summary.avg_adaptation_score ?? 0} label="Adaptation" color="#f59e0b"/>
          <GaugeRing value={summary.avg_equity_score     ?? 0} label="Équité"     color="#a855f7"/>
        </div>
      </div>

      {/* Distribution Bars */}
      <div className="bg-slate-900 border border-orange-700/30 rounded-xl p-5 grid grid-cols-1 md:grid-cols-2 gap-5">
        {dists.map(d => <DistBar key={d.title} {...d}/>)}
      </div>

      {/* Filtres Risque */}
      <div className="flex flex-wrap gap-2">
        {["all", "low", "moderate", "high", "critical"].map(r => (
          <button key={r} onClick={() => setRisk(r)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${riskFilter === r ? "bg-orange-700 border-orange-600 text-white" : "bg-slate-900 border-orange-700/30 text-slate-400 hover:text-white"}`}>
            {r === "all" ? "Tous risques" : r === "critical" ? "Urgence létale" : r === "high" ? "Crise majeure" : r === "moderate" ? "Stress thermique" : "Sous contrôle"}
          </button>
        ))}
        <span className="w-px h-5 self-center bg-orange-700/30"/>
        {regions.map(r => (
          <button key={r} onClick={() => setReg(r)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${regFilter === r ? "bg-slate-700 border-slate-500 text-white" : "bg-slate-900 border-orange-700/30 text-slate-400 hover:text-white"}`}>
            {r === "all" ? "Toutes régions" : r}
          </button>
        ))}
      </div>

      {/* Cartes Entités */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {filtered.map(e => {
          const risk = RISK_META[e.risk_level];
          return (
            <div key={e.id} onClick={() => setSelected(e)}
              className="bg-slate-900 border border-slate-800 rounded-xl p-4 cursor-pointer hover:border-orange-700/50 transition-colors">
              <div className="flex items-center justify-between mb-1">
                <span className="font-bold text-white">{e.id}</span>
                <span className="text-xs text-slate-400">{e.region}</span>
              </div>
              <div className="text-xs text-orange-400 mb-2 capitalize">{e.city_type.replace(/_/g, " ")}</div>
              <div className="flex gap-1 mb-3 flex-wrap">
                <span className={`px-2 py-0.5 rounded text-xs font-medium border ${risk?.badge || "bg-slate-700 text-slate-300"}`}>
                  {risk?.label || e.risk_level}
                </span>
                <span className="px-2 py-0.5 rounded text-xs font-medium bg-slate-700 text-amber-300">
                  {SEV_LABELS[e.severity] || e.severity.replace(/_/g, " ")}
                </span>
              </div>
              <div className="text-2xl font-black text-white mb-1">{e.composite_score.toFixed(1)}</div>
              <div className="text-xs text-slate-500 mb-2 capitalize">{PATTERN_LABELS[e.heat_pattern] || e.heat_pattern.replace(/_/g, " ")}</div>
              <div className="text-xs text-orange-400 font-medium mb-2">
                {ACTION_LABELS[e.recommended_action] || e.recommended_action.replace(/_/g, " ")}
              </div>
              <div className="flex gap-1 flex-wrap text-xs">
                <span className="text-slate-500">Ilot chaleur: <span className="text-orange-300">{Math.round(e.heat_island_intensity_index * 100)}%</span></span>
                <span className="text-slate-500 ml-1">Mortalité: <span className="text-red-300">{Math.round(e.extreme_heat_mortality_rate * 100)}%</span></span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
