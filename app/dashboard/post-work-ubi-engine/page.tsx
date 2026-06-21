"use client";
import { useEffect, useState } from "react";

type Entity = {
  id: string;
  economic_sector: string;
  region: string;
  automation_displacement_rate: number;
  UBI_fiscal_sustainability: number;
  retraining_program_failure: number;
  social_contract_breakdown: number;
  gig_worker_precariousness: number;
  cognitive_job_extinction: number;
  labor_market_polarization: number;
  meaning_crisis_intensity: number;
  political_instability_unemployment: number;
  welfare_state_collapse: number;
  automation_tax_resistance: number;
  UBI_inflation_risk: number;
  skills_gap_acceleration: number;
  inequality_amplification_AI: number;
  union_power_collapse: number;
  middle_class_extinction: number;
  social_cohesion_erosion: number;
  displacement_score: number;
  social_score: number;
  economic_score: number;
  political_score: number;
  composite_score: number;
  risk_level: string;
  post_work_pattern: string;
  severity: string;
  recommended_action: string;
  signal: string;
};

type Summary = {
  module_id: number;
  module_name: string;
  total: number;
  critical: number;
  high: number;
  moderate: number;
  low: number;
  avg_composite: number;
  distributions: Record<string, Record<string, number>>;
  avg_estimated_post_work_disruption_index: number;
  pattern_distribution: Record<string, number>;
  risk_distribution: Record<string, number>;
  severity_distribution: Record<string, number>;
};

function GaugeRing({ value, label, color }: { value: number; label: string; color: string }) {
  const r = 36;
  const circ = 2 * Math.PI * r;
  const fill = circ * (1 - value / 100);
  return (
    <div className="flex flex-col items-center gap-1">
      <svg width="88" height="88" viewBox="0 0 88 88">
        <circle cx="44" cy="44" r={r} fill="none" stroke="#1e293b" strokeWidth="8" />
        <circle
          cx="44" cy="44" r={r} fill="none" stroke={color} strokeWidth="8"
          strokeDasharray={circ} strokeDashoffset={fill}
          strokeLinecap="round" transform="rotate(-90 44 44)"
        />
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
          <div
            key={k}
            style={{ width: `${(v / total) * 100}%`, background: colors[k] || "#475569" }}
            title={`${k}: ${v}`}
          />
        ))}
      </div>
      <div className="flex flex-wrap gap-x-3 gap-y-0.5">
        {Object.entries(counts).map(([k, v]) => (
          <span key={k} className="text-xs text-slate-400">
            <span style={{ color: colors[k] || "#94a3b8" }}>■</span> {k} {v}
          </span>
        ))}
      </div>
    </div>
  );
}

const RISK_COLORS: Record<string, string> = {
  low:      "#10b981",
  moderate: "#f59e0b",
  high:     "#f97316",
  critical: "#ef4444",
};
const PAT_COLORS: Record<string, string> = {
  none:                          "#10b981",
  mass_automation_displacement:  "#ef4444",
  welfare_state_implosion:       "#dc2626",
  social_contract_collapse:      "#b91c1c",
  middle_class_extinction_event: "#f97316",
  political_automation_revolt:   "#7c3aed",
};
const SEV_COLORS: Record<string, string> = {
  risque_post_travail_contenu:               "#10b981",
  transition_post_travail_active:            "#f59e0b",
  disruption_emploi_revenu_majeure:          "#f97316",
  "effondrement_post_travail_systémique":    "#ef4444",
};
const ACT_COLORS: Record<string, string> = {
  "veille_disruption_marché_travail":        "#10b981",
  renforcement_filets_protection_sociale:    "#f59e0b",
  "audit_systémique_transition_emploi":      "#f97316",
  intervention_urgente_revenu_universel:     "#ef4444",
};
const RISK_BADGE: Record<string, string> = {
  low:      "bg-emerald-900 text-emerald-300",
  moderate: "bg-amber-900 text-amber-300",
  high:     "bg-orange-900 text-orange-300",
  critical: "bg-red-900 text-red-300",
};
const PAT_BADGE: Record<string, string> = {
  none:                          "bg-slate-800 text-slate-400",
  mass_automation_displacement:  "bg-red-900 text-red-300",
  welfare_state_implosion:       "bg-rose-900 text-rose-300",
  social_contract_collapse:      "bg-red-950 text-red-400",
  middle_class_extinction_event: "bg-orange-900 text-orange-300",
  political_automation_revolt:   "bg-purple-900 text-purple-300",
};

function DetailModal({ entity, onClose }: { entity: Entity; onClose: () => void }) {
  const [tab, setTab] = useState<"scores" | "signal" | "action">("scores");

  useEffect(() => {
    const h = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", h);
    return () => window.removeEventListener("keydown", h);
  }, [onClose]);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70" onClick={onClose}>
      <div
        className="bg-slate-900 border border-slate-700 rounded-xl w-full max-w-lg p-6 shadow-2xl"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="flex items-center justify-between mb-4">
          <div>
            <span className="text-lg font-bold text-white">{entity.id}</span>
            <span className="ml-2 text-slate-400 text-sm capitalize">
              {entity.economic_sector.replace(/_/g, " ")}
            </span>
            <span className="ml-2 text-amber-400 text-xs">{entity.region}</span>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl leading-none">✕</button>
        </div>

        <div className="flex gap-2 mb-4">
          {(["scores", "signal", "action"] as const).map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`px-3 py-1 rounded text-xs font-medium transition-colors ${
                tab === t ? "bg-amber-800 text-white" : "bg-slate-800 text-slate-400 hover:text-white"
              }`}
            >
              {t === "scores" ? "Scores" : t === "signal" ? "Signal" : "Action"}
            </button>
          ))}
        </div>

        {tab === "scores" && (
          <div className="grid grid-cols-2 gap-3 text-sm">
            {[
              ["Déplacement",  entity.displacement_score, "#ef4444"],
              ["Social",       entity.social_score,       "#f97316"],
              ["Économique",   entity.economic_score,     "#f59e0b"],
              ["Politique",    entity.political_score,    "#7c3aed"],
            ].map(([l, v, c]) => (
              <div key={String(l)} className="bg-slate-800 rounded-lg p-3">
                <div className="text-slate-400 text-xs mb-1">{String(l)}</div>
                <div className="text-white font-bold text-lg">{Number(v).toFixed(1)}</div>
                <div className="h-1.5 rounded mt-1 bg-slate-700">
                  <div className="h-1.5 rounded" style={{ width: `${Math.min(Number(v), 100)}%`, background: String(c) }} />
                </div>
              </div>
            ))}
            <div className="col-span-2 bg-slate-800 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Score Composite</div>
              <div className="text-white font-bold text-2xl">{entity.composite_score.toFixed(1)}</div>
            </div>
          </div>
        )}

        {tab === "signal" && (
          <div className="bg-slate-800 rounded-lg p-4 text-sm text-slate-200 leading-relaxed">
            {entity.signal}
            <div className="mt-3 flex gap-2 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[entity.risk_level] || "bg-slate-700 text-slate-300"}`}>
                {entity.risk_level}
              </span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${PAT_BADGE[entity.post_work_pattern] || "bg-slate-700 text-slate-300"}`}>
                {entity.post_work_pattern.replace(/_/g, " ")}
              </span>
            </div>
          </div>
        )}

        {tab === "action" && (
          <div className="space-y-3 text-sm">
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Action Recommandée</div>
              <div className="text-white font-medium">{entity.recommended_action.replace(/_/g, " ")}</div>
            </div>
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Sévérité</div>
              <div className="text-white font-medium">{entity.severity.replace(/_/g, " ")}</div>
            </div>
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Secteur Économique</div>
              <div className="text-white font-medium capitalize">{entity.economic_sector.replace(/_/g, " ")}</div>
            </div>
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Taux Déplacement Automation</div>
              <div className="text-white font-bold">{(entity.automation_displacement_rate * 100).toFixed(0)}%</div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function PostWorkUBIDashboard() {
  const [data, setData]         = useState<{ entities: Entity[]; summary: Summary } | null>(null);
  const [filter, setFilter]     = useState<string>("all");
  const [patFilter, setPat]     = useState<string>("all");
  const [selected, setSelected] = useState<Entity | null>(null);

  useEffect(() => {
    fetch("/api/post-work-ubi-engine")
      .then((r) => r.json())
      .then(setData)
      .catch(console.error);
  }, []);

  if (!data) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-amber-400 text-lg animate-pulse">Chargement Société Post-Travail & RUB...</div>
    </div>
  );

  const { entities, summary } = data;
  const filtered = entities.filter((e) =>
    (filter === "all" || e.risk_level === filter) &&
    (patFilter === "all" || e.post_work_pattern === patFilter)
  );

  const avgDisplacement = entities.length > 0 ? entities.reduce((a, e) => a + e.displacement_score, 0) / entities.length : 0;
  const avgSocial       = entities.length > 0 ? entities.reduce((a, e) => a + e.social_score, 0) / entities.length : 0;
  const avgEconomic     = entities.length > 0 ? entities.reduce((a, e) => a + e.economic_score, 0) / entities.length : 0;
  const avgPolitical    = entities.length > 0 ? entities.reduce((a, e) => a + e.political_score, 0) / entities.length : 0;

  const massDisplacement = entities.filter((e) => e.post_work_pattern === "mass_automation_displacement").length;
  const avgAutomation    = entities.length > 0
    ? Math.round(entities.reduce((a, e) => a + e.automation_displacement_rate, 0) / entities.length * 100)
    : 0;

  const dists = [
    { title: "Risque",    counts: summary.risk_distribution,     colors: RISK_COLORS },
    { title: "Patron",    counts: summary.pattern_distribution,  colors: PAT_COLORS  },
    { title: "Sévérité",  counts: summary.severity_distribution, colors: SEV_COLORS  },
    { title: "Action",    counts: summary.distributions?.action || {}, colors: ACT_COLORS },
  ] as Array<{ title: string; counts: Record<string, number>; colors: Record<string, string> }>;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {selected && <DetailModal entity={selected} onClose={() => setSelected(null)} />}

      <div>
        <h1 className="text-2xl font-bold text-white">
          Société Post-Travail &amp; Revenu Universel — Module 374
        </h1>
        <p className="text-slate-400 text-sm mt-1">
          Déplacement · Social · Économique · Politique — analyse systémique de la disruption post-travail et du revenu universel
        </p>
      </div>

      {/* KPI cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {[
          ["Total Secteurs",                   summary.total,                                                             "text-amber-400"],
          ["Déplacement Massif",               massDisplacement,                                                          "text-red-500"],
          ["Crise Majeure",                    summary.critical,                                                          "text-rose-400"],
          ["Composite Moyen",                  summary.avg_composite.toFixed(1),                                          "text-slate-300"],
          ["Index Disruption Post-Travail",    `${summary.avg_estimated_post_work_disruption_index.toFixed(2)}/10`,        "text-amber-400"],
          ["Déplacement Moyen",               `${avgAutomation}%`,                                                        "text-red-300"],
        ].map(([l, v, c]) => (
          <div key={String(l)} className="bg-slate-900 border border-slate-800 rounded-xl p-3 text-center">
            <div className={`text-xl font-bold ${c}`}>{v}</div>
            <div className="text-xs text-slate-500 mt-0.5">{l}</div>
          </div>
        ))}
      </div>

      {/* Gauge rings */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
        <div className="grid grid-cols-4 gap-4">
          <GaugeRing value={avgDisplacement} label="Déplacement" color="#ef4444" />
          <GaugeRing value={avgSocial}       label="Social"       color="#f97316" />
          <GaugeRing value={avgEconomic}     label="Économique"   color="#f59e0b" />
          <GaugeRing value={avgPolitical}    label="Politique"    color="#7c3aed" />
        </div>
      </div>

      {/* Distribution bars */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 grid grid-cols-1 md:grid-cols-2 gap-5">
        {dists.map((d) => <DistBar key={d.title} {...d} />)}
      </div>

      {/* Filter pills */}
      <div className="flex flex-wrap gap-2">
        {["all", "low", "moderate", "high", "critical"].map((r) => (
          <button
            key={r}
            onClick={() => setFilter(r)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${
              filter === r
                ? "bg-amber-800 border-amber-700 text-white"
                : "bg-slate-900 border-slate-700 text-slate-400 hover:text-white"
            }`}
          >
            {r === "all" ? "Tous" : r}
          </button>
        ))}
        <span className="w-px h-5 self-center bg-slate-700" />
        {["all", "none", "mass_automation_displacement", "welfare_state_implosion", "social_contract_collapse", "middle_class_extinction_event", "political_automation_revolt"].map((p) => (
          <button
            key={p}
            onClick={() => setPat(p)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${
              patFilter === p
                ? "bg-amber-800 border-amber-700 text-white"
                : "bg-slate-900 border-slate-700 text-slate-400 hover:text-white hover:border-amber-700"
            }`}
          >
            {p === "all" ? "Tous patrons" : p.replace(/_/g, " ")}
          </button>
        ))}
      </div>

      {/* Entity cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {filtered.map((e) => (
          <div
            key={e.id}
            onClick={() => setSelected(e)}
            className="bg-slate-900 border border-slate-800 rounded-xl p-4 cursor-pointer hover:border-amber-700 transition-colors"
          >
            <div className="flex items-center justify-between mb-1">
              <span className="font-bold text-white">{e.id}</span>
              <span className="text-xs text-slate-400">{e.region}</span>
            </div>
            <div className="text-xs text-amber-400 mb-2 capitalize">
              {e.economic_sector.replace(/_/g, " ")}
            </div>
            <div className="flex gap-1 mb-3 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[e.risk_level] || "bg-slate-700 text-slate-300"}`}>
                {e.risk_level}
              </span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${PAT_BADGE[e.post_work_pattern] || "bg-slate-700 text-slate-300"}`}>
                {e.post_work_pattern.replace(/_/g, " ")}
              </span>
            </div>
            <div className="text-2xl font-black text-white mb-1">{e.composite_score.toFixed(1)}</div>
            <div className="text-xs text-slate-500 mb-2 capitalize">{e.severity.replace(/_/g, " ")}</div>
            <div className="text-xs text-rose-400 font-medium mb-2">
              Automation: {(e.automation_displacement_rate * 100).toFixed(0)}%
            </div>
            <div className="text-xs text-slate-400 leading-snug line-clamp-2">{e.signal}</div>
          </div>
        ))}
      </div>
    </div>
  );
}
