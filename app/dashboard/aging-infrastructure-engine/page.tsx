"use client";
import { useEffect, useState } from "react";

// ── Types ─────────────────────────────────────────────────────────────────────

type RiskLevel    = "critical" | "high" | "moderate" | "low";
type AgingPattern = "critical_infrastructure_imminent_failure" | "investment_deficit_crisis" | "water_power_grid_collapse" | "bridge_dam_catastrophe_risk" | "failure_cascade_systemic" | "none";
type Severity     = "urgence_effondrement_infrastructure_physique" | "crise_vieillissement_infrastructure_majeure" | "dégradation_structurelle_chronique" | "vieillissement_infrastructure_géré";
type AgingAction  = "plan_urgence_réhabilitation_infrastructure" | "réparation_urgente_infrastructure_critique" | "programme_maintenance_préventive_accéléré" | "veille_vieillissement_infrastructure_continue";

interface AieEntity {
  id: string;
  infrastructure_type: string;
  region: string;
  deterioration_score: number;
  safety_score: number;
  investment_score: number;
  cascade_score: number;
  composite_score: number;
  risk_level: RiskLevel;
  aging_pattern: AgingPattern;
  severity: Severity;
  recommended_action: AgingAction;
  signal: string;
  structural_deterioration_rate: number;
  critical_failure_imminent: number;
}

interface AieSummary {
  module_id: number;
  module_name: string;
  total: number;
  critical: number;
  high: number;
  moderate: number;
  low: number;
  avg_composite: number;
  distributions: {
    risk: Record<string, number>;
    pattern: Record<string, number>;
    severity: Record<string, number>;
    action: Record<string, number>;
  };
  avg_estimated_infrastructure_aging_index: number;
  avg_deterioration_score: number;
  avg_safety_score: number;
  avg_investment_score: number;
  avg_cascade_score: number;
}

// ── Metadata ──────────────────────────────────────────────────────────────────

const RISK_META: Record<RiskLevel, { label: string; color: string; ring: string; badge: string }> = {
  critical: { label: "Défaillance Imminente", color: "text-red-400",    ring: "#ef4444", badge: "bg-red-900/60 text-red-300 border-red-700" },
  high:     { label: "Crise Majeure",         color: "text-orange-400", ring: "#f97316", badge: "bg-orange-900/60 text-orange-300 border-orange-700" },
  moderate: { label: "Dégradation Chronique", color: "text-amber-400",  ring: "#f59e0b", badge: "bg-amber-900/60 text-amber-300 border-amber-700" },
  low:      { label: "Sous Contrôle",         color: "text-emerald-400", ring: "#10b981", badge: "bg-emerald-900/60 text-emerald-300 border-emerald-700" },
};

const PATTERN_LABELS: Record<AgingPattern, string> = {
  critical_infrastructure_imminent_failure: "Défaillance Infrastructure Imminente",
  investment_deficit_crisis:                "Crise Déficit Investissement",
  water_power_grid_collapse:                "Effondrement Eau & Réseau Électrique",
  bridge_dam_catastrophe_risk:              "Risque Catastrophe Pont/Barrage",
  failure_cascade_systemic:                 "Cascade Défaillance Systémique",
  none:                                     "Aucun",
};

const SEV_LABELS: Record<Severity, string> = {
  urgence_effondrement_infrastructure_physique: "Urgence Effondrement",
  crise_vieillissement_infrastructure_majeure:  "Crise Vieillissement",
  "dégradation_structurelle_chronique":         "Dégradation Chronique",
  "vieillissement_infrastructure_géré":         "Géré",
};

const ACTION_LABELS: Record<AgingAction, string> = {
  "plan_urgence_réhabilitation_infrastructure":   "Plan Urgence Réhabilitation",
  "réparation_urgente_infrastructure_critique":   "Réparation Urgente Infrastructure",
  "programme_maintenance_préventive_accéléré":    "Programme Maintenance Préventive",
  veille_vieillissement_infrastructure_continue:  "Veille Vieillissement Continue",
};

const RISK_COLORS: Record<string, string> = {
  critical: "#ef4444", high: "#f97316", moderate: "#f59e0b", low: "#10b981",
};

const PAT_COLORS: Record<string, string> = {
  critical_infrastructure_imminent_failure: "#ef4444",
  investment_deficit_crisis:                "#f97316",
  water_power_grid_collapse:                "#3b82f6",
  bridge_dam_catastrophe_risk:              "#a855f7",
  failure_cascade_systemic:                 "#f59e0b",
  none:                                     "#10b981",
};

const SEV_COLORS: Record<string, string> = {
  urgence_effondrement_infrastructure_physique: "#ef4444",
  crise_vieillissement_infrastructure_majeure:  "#f97316",
  "dégradation_structurelle_chronique":         "#f59e0b",
  "vieillissement_infrastructure_géré":         "#10b981",
};

const ACT_COLORS: Record<string, string> = {
  "plan_urgence_réhabilitation_infrastructure":  "#ef4444",
  "réparation_urgente_infrastructure_critique":  "#f97316",
  "programme_maintenance_préventive_accéléré":   "#f59e0b",
  veille_vieillissement_infrastructure_continue: "#10b981",
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
      <span className="text-xs text-stone-400 text-center">{label}</span>
    </div>
  );
}

function DistBar({ title, counts, colors }: { title: string; counts: Record<string, number>; colors: Record<string, string> }) {
  const total = Object.values(counts).reduce((a, b) => a + b, 0) || 1;
  return (
    <div className="flex flex-col gap-1">
      <span className="text-xs text-stone-400 font-medium">{title}</span>
      <div className="flex h-3 rounded overflow-hidden gap-px">
        {Object.entries(counts).map(([k, v]) => (
          <div key={k} style={{ width: `${v / total * 100}%`, background: colors[k] || "#78716c" }} title={`${k}: ${v}`}/>
        ))}
      </div>
      <div className="flex flex-wrap gap-x-3 gap-y-0.5">
        {Object.entries(counts).map(([k, v]) => (
          <span key={k} className="text-xs text-stone-400">
            <span style={{ color: colors[k] || "#a8a29e" }}>■</span> {k.replace(/_/g, " ")} {v}
          </span>
        ))}
      </div>
    </div>
  );
}

function DetailModal({ entity, onClose }: { entity: AieEntity; onClose: () => void }) {
  const [tab, setTab] = useState<"scores" | "analyse" | "actions">("scores");
  const risk = RISK_META[entity.risk_level];

  useEffect(() => {
    const h = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", h);
    return () => window.removeEventListener("keydown", h);
  }, [onClose]);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/75" onClick={onClose}>
      <div className="bg-slate-900 border border-red-800/30 rounded-xl w-full max-w-lg p-6 shadow-2xl" onClick={e => e.stopPropagation()}>
        <div className="flex items-center justify-between mb-4">
          <div>
            <span className="text-lg font-bold text-white">{entity.id}</span>
            <span className="ml-2 text-red-400 text-xs">{entity.infrastructure_type.replace(/_/g, " ")}</span>
            <span className="ml-2 text-stone-400 text-xs">{entity.region}</span>
          </div>
          <button onClick={onClose} className="text-stone-500 hover:text-white text-xl leading-none">✕</button>
        </div>

        <div className="flex gap-2 mb-4">
          {(["scores", "analyse", "actions"] as const).map(t => (
            <button key={t} onClick={() => setTab(t)}
              className={`px-3 py-1 rounded text-xs font-medium transition-colors ${tab === t ? "bg-red-800 text-white" : "bg-slate-800 text-stone-400 hover:text-white"}`}>
              {t === "scores" ? "Scores" : t === "analyse" ? "Analyse" : "Actions"}
            </button>
          ))}
        </div>

        {tab === "scores" && (
          <div className="grid grid-cols-2 gap-3 text-sm">
            {[
              ["Détérioration", entity.deterioration_score, "#ef4444"],
              ["Sécurité",      entity.safety_score,        "#f97316"],
              ["Investissement", entity.investment_score,   "#f59e0b"],
              ["Cascade",       entity.cascade_score,       "#a855f7"],
            ].map(([l, v, c]) => (
              <div key={String(l)} className="bg-slate-800 border border-red-800/20 rounded-lg p-3">
                <div className="text-stone-400 text-xs mb-1">{String(l)}</div>
                <div className="text-white font-bold text-lg">{Number(v).toFixed(1)}</div>
                <div className="h-1.5 rounded mt-1 bg-slate-700">
                  <div className="h-1.5 rounded" style={{ width: `${Math.min(Number(v), 100)}%`, background: String(c) }}/>
                </div>
              </div>
            ))}
            <div className="col-span-2 bg-slate-800 border border-red-800/20 rounded-lg p-3">
              <div className="text-stone-400 text-xs mb-1">Score Composite</div>
              <div className="text-white font-bold text-2xl">{entity.composite_score.toFixed(1)}</div>
            </div>
          </div>
        )}

        {tab === "analyse" && (
          <div className="bg-slate-800 border border-red-800/20 rounded-lg p-4 text-sm text-slate-200 leading-relaxed">
            {entity.signal}
            <div className="mt-3 flex gap-2 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium border ${risk?.badge || "bg-slate-700 text-stone-300"}`}>
                {entity.risk_level}
              </span>
              <span className="px-2 py-0.5 rounded text-xs font-medium bg-slate-700 text-amber-300">
                {SEV_LABELS[entity.severity] || entity.severity.replace(/_/g, " ")}
              </span>
              <span className="px-2 py-0.5 rounded text-xs font-medium bg-slate-700 text-red-300">
                {PATTERN_LABELS[entity.aging_pattern] || entity.aging_pattern.replace(/_/g, " ")}
              </span>
            </div>
            <div className="mt-3 grid grid-cols-2 gap-2 text-xs text-stone-400">
              <div>Détérioration structurelle: <span className="text-red-300">{Math.round(entity.structural_deterioration_rate * 100)}%</span></div>
              <div>Défaillance imminente: <span className="text-orange-300">{Math.round(entity.critical_failure_imminent * 100)}%</span></div>
            </div>
          </div>
        )}

        {tab === "actions" && (
          <div className="space-y-3 text-sm">
            <div className="bg-slate-800 border border-red-800/20 rounded-lg p-3">
              <div className="text-stone-400 text-xs mb-1">Action Recommandée</div>
              <div className="text-white font-medium">
                {ACTION_LABELS[entity.recommended_action] || entity.recommended_action.replace(/_/g, " ")}
              </div>
            </div>
            <div className="bg-slate-800 border border-red-800/20 rounded-lg p-3">
              <div className="text-stone-400 text-xs mb-1">Sévérité</div>
              <div className="text-white font-medium">{SEV_LABELS[entity.severity] || entity.severity.replace(/_/g, " ")}</div>
            </div>
            <div className="bg-slate-800 border border-red-800/20 rounded-lg p-3">
              <div className="text-stone-400 text-xs mb-1">Patron de Vieillissement</div>
              <div className="text-white font-medium">{PATTERN_LABELS[entity.aging_pattern] || entity.aging_pattern.replace(/_/g, " ")}</div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

// ── Dashboard ─────────────────────────────────────────────────────────────────

export default function AgingInfrastructureDashboard() {
  const [data, setData]         = useState<{ entities: AieEntity[]; summary: AieSummary } | null>(null);
  const [riskFilter, setRisk]   = useState<string>("all");
  const [regFilter, setReg]     = useState<string>("all");
  const [selected, setSelected] = useState<AieEntity | null>(null);

  useEffect(() => {
    fetch("/api/aging-infrastructure-engine")
      .then(r => r.json())
      .then(setData)
      .catch(console.error);
  }, []);

  if (!data) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-red-400 text-lg animate-pulse">Initialisation du Moteur Infrastructure Vieillissante — Module 392...</div>
    </div>
  );

  const { entities, summary } = data;

  const regions  = ["all", ...Array.from(new Set(entities.map(e => e.region)))];
  const filtered = entities.filter(e =>
    (riskFilter === "all" || e.risk_level === riskFilter) &&
    (regFilter  === "all" || e.region === regFilter)
  );

  const dists = [
    { title: "Niveau de Risque",        counts: summary.distributions.risk,     colors: RISK_COLORS },
    { title: "Patron de Vieillissement", counts: summary.distributions.pattern,  colors: PAT_COLORS  },
    { title: "Sévérité",                 counts: summary.distributions.severity, colors: SEV_COLORS  },
    { title: "Action Recommandée",       counts: summary.distributions.action,   colors: ACT_COLORS  },
  ] as Array<{ title: string; counts: Record<string, number>; colors: Record<string, string> }>;

  return (
    <div className="min-h-screen bg-slate-950 text-stone-300 p-6 space-y-6">
      {selected && <DetailModal entity={selected} onClose={() => setSelected(null)}/>}

      {/* En-tête */}
      <div>
        <h1 className="text-2xl font-bold text-red-400">
          Infrastructure Vieillissante &amp; Effondrement Systèmes — Module 392
        </h1>
        <p className="text-stone-400 text-sm mt-1">
          Détérioration · Sécurité · Investissement · Cascade — Intelligence Infrastructure Physique — Caelum Partners
        </p>
        <p className="text-stone-500 text-xs mt-0.5">Chaima Mhadbi — Bruxelles</p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {[
          ["Total Infrastructures",       summary.total,                                                          "text-stone-300"],
          ["Défaillance Imminente",        summary.critical,                                                      "text-red-400"],
          ["Crise Majeure",                summary.high,                                                          "text-orange-400"],
          ["Composite Moyen",              summary.avg_composite.toFixed(1),                                      "text-red-300"],
          ["Index Vieillissement Infra.",  summary.avg_estimated_infrastructure_aging_index.toFixed(2) + "/10",   "text-orange-300"],
          ["Détérioration Moyenne",        summary.avg_deterioration_score != null ? summary.avg_deterioration_score.toFixed(1) : "—", "text-amber-400"],
        ].map(([l, v, c]) => (
          <div key={String(l)} className="bg-slate-900 border border-red-800/30 rounded-xl p-3 text-center">
            <div className={`text-xl font-bold ${c}`}>{v}</div>
            <div className="text-xs text-stone-500 mt-0.5 leading-tight">{l}</div>
          </div>
        ))}
      </div>

      {/* Gauge Rings */}
      <div className="bg-slate-900 border border-red-800/30 rounded-xl p-5">
        <p className="text-xs text-stone-500 mb-4 font-medium">Scores Moyens par Dimension</p>
        <div className="grid grid-cols-4 gap-4">
          <GaugeRing value={summary.avg_deterioration_score ?? 0} label="Détérioration" color="#ef4444"/>
          <GaugeRing value={summary.avg_safety_score        ?? 0} label="Sécurité"      color="#f97316"/>
          <GaugeRing value={summary.avg_investment_score    ?? 0} label="Investissement" color="#f59e0b"/>
          <GaugeRing value={summary.avg_cascade_score       ?? 0} label="Cascade"        color="#a855f7"/>
        </div>
      </div>

      {/* Distribution Bars */}
      <div className="bg-slate-900 border border-red-800/30 rounded-xl p-5 grid grid-cols-1 md:grid-cols-2 gap-5">
        {dists.map(d => <DistBar key={d.title} {...d}/>)}
      </div>

      {/* Filtres Risque */}
      <div className="flex flex-wrap gap-2">
        {["all", "low", "moderate", "high", "critical"].map(r => (
          <button key={r} onClick={() => setRisk(r)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${riskFilter === r ? "bg-red-800 border-red-700 text-white" : "bg-slate-900 border-red-800/30 text-stone-400 hover:text-white"}`}>
            {r === "all" ? "Tous risques" : r === "critical" ? "Défaillance imminente" : r === "high" ? "Crise majeure" : r === "moderate" ? "Dégradation chronique" : "Sous contrôle"}
          </button>
        ))}
        <span className="w-px h-5 self-center bg-red-800/30"/>
        {regions.map(r => (
          <button key={r} onClick={() => setReg(r)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${regFilter === r ? "bg-slate-700 border-slate-500 text-white" : "bg-slate-900 border-red-800/30 text-stone-400 hover:text-white"}`}>
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
              className="bg-slate-900 border border-slate-800 rounded-xl p-4 cursor-pointer hover:border-red-800/50 transition-colors">
              <div className="flex items-center justify-between mb-1">
                <span className="font-bold text-white">{e.id}</span>
                <span className="text-xs text-stone-400">{e.region}</span>
              </div>
              <div className="text-xs text-red-400 mb-2 capitalize">{e.infrastructure_type.replace(/_/g, " ")}</div>
              <div className="flex gap-1 mb-3 flex-wrap">
                <span className={`px-2 py-0.5 rounded text-xs font-medium border ${risk?.badge || "bg-slate-700 text-stone-300"}`}>
                  {risk?.label || e.risk_level}
                </span>
                <span className="px-2 py-0.5 rounded text-xs font-medium bg-slate-700 text-amber-300">
                  {SEV_LABELS[e.severity] || e.severity.replace(/_/g, " ")}
                </span>
              </div>
              <div className="text-2xl font-black text-white mb-1">{e.composite_score.toFixed(1)}</div>
              <div className="text-xs text-stone-500 mb-2 capitalize">{PATTERN_LABELS[e.aging_pattern] || e.aging_pattern.replace(/_/g, " ")}</div>
              <div className="text-xs text-red-400 font-medium mb-2">
                {ACTION_LABELS[e.recommended_action] || e.recommended_action.replace(/_/g, " ")}
              </div>
              <div className="flex gap-1 flex-wrap text-xs">
                <span className="text-stone-500">Détérioration: <span className="text-red-300">{Math.round(e.structural_deterioration_rate * 100)}%</span></span>
                <span className="text-stone-500 ml-1">Défaillance: <span className="text-orange-300">{Math.round(e.critical_failure_imminent * 100)}%</span></span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
