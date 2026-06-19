"use client";
import { useEffect, useState } from "react";

type Entity = {
  entity_id: string;
  control_domain: string;
  region: string;
  behavioral_score_deployment_density: number;
  access_restriction_based_on_score: number;
  corporate_social_scoring_integration: number;
  gamification_compliance_mechanism: number;
  score_opacity_and_unappealability: number;
  AI_behavioral_prediction_scoring: number;
  cross_sector_score_aggregation: number;
  dissent_behavioral_penalization: number;
  score_based_opportunity_denial: number;
  social_ostracism_enforcement: number;
  private_public_score_fusion: number;
  automated_punishment_system: number;
  behavioral_norm_homogenization: number;
  opposition_score_targeting: number;
  family_collective_score_punishment: number;
  score_export_to_allied_systems: number;
  resistance_detection_scoring: number;
  control_score: number;
  opacity_score: number;
  punishment_score: number;
  homogenization_score: number;
  composite_score: number;
  risk_level: string;
  social_credit_pattern: string;
  severity: string;
  recommended_action: string;
  signal: string;
};

type Summary = {
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
  avg_estimated_social_credit_index: number;
  avg_behavioral_score_density: number;
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

const RISK_COLORS = { low: "#10b981", moderate: "#f59e0b", high: "#f97316", critical: "#ef4444" };
const PAT_COLORS: Record<string, string> = {
  none:                         "#10b981",
  total_behavioral_control:     "#ef4444",
  dissent_elimination:          "#dc2626",
  collective_punishment_system: "#b91c1c",
  behavioral_homogenization_lock: "#a21caf",
  corporate_state_score_fusion: "#7e22ce",
};
const SEV_COLORS: Record<string, string> = {
  "scoring_comportemental_limité":           "#10b981",
  "notation_comportementale_structurelle":   "#f59e0b",
  "système_crédit_social_avancé":            "#f97316",
  "contrôle_comportemental_total":           "#ef4444",
};
const ACT_COLORS: Record<string, string> = {
  veille_scoring_comportemental:        "#10b981",
  protection_droits_comportementaux:    "#f59e0b",
  interdiction_système_crédit_social:   "#f97316",
  "résistance_crédit_social_urgente":   "#ef4444",
};
const RISK_BADGE: Record<string, string> = {
  low:      "bg-emerald-900 text-emerald-300",
  moderate: "bg-amber-900 text-amber-300",
  high:     "bg-orange-900 text-orange-300",
  critical: "bg-red-900 text-red-300",
};
const PAT_BADGE: Record<string, string> = {
  none:                           "bg-slate-800 text-slate-400",
  total_behavioral_control:       "bg-red-900 text-red-300",
  dissent_elimination:            "bg-rose-900 text-rose-300",
  collective_punishment_system:   "bg-red-950 text-red-400",
  behavioral_homogenization_lock: "bg-purple-900 text-purple-300",
  corporate_state_score_fusion:   "bg-violet-900 text-violet-300",
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
            <span className="text-lg font-bold text-white">{entity.entity_id}</span>
            <span className="ml-2 text-slate-400 text-sm capitalize">
              {entity.control_domain.replace(/_/g, " ")}
            </span>
            <span className="ml-2 text-red-400 text-xs">{entity.region}</span>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl leading-none">✕</button>
        </div>

        <div className="flex gap-2 mb-4">
          {(["scores", "signal", "action"] as const).map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`px-3 py-1 rounded text-xs font-medium transition-colors ${
                tab === t ? "bg-red-800 text-white" : "bg-slate-800 text-slate-400 hover:text-white"
              }`}
            >
              {t === "scores" ? "Scores" : t === "signal" ? "Signal" : "Action"}
            </button>
          ))}
        </div>

        {tab === "scores" && (
          <div className="grid grid-cols-2 gap-3 text-sm">
            {[
              ["Contrôle",         entity.control_score,        "#ef4444"],
              ["Opacité",          entity.opacity_score,         "#dc2626"],
              ["Punition",         entity.punishment_score,      "#a21caf"],
              ["Homogénéisation",  entity.homogenization_score,  "#7e22ce"],
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
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${PAT_BADGE[entity.social_credit_pattern] || "bg-slate-700 text-slate-300"}`}>
                {entity.social_credit_pattern.replace(/_/g, " ")}
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
              <div className="text-slate-400 text-xs mb-1">Domaine de Contrôle</div>
              <div className="text-white font-medium capitalize">{entity.control_domain.replace(/_/g, " ")}</div>
            </div>
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Densité Score Comportemental</div>
              <div className="text-white font-bold">{(entity.behavioral_score_deployment_density * 100).toFixed(0)}%</div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function SocialCreditDashboard() {
  const [data, setData]     = useState<{ entities: Entity[]; summary: Summary } | null>(null);
  const [filter, setFilter] = useState<string>("all");
  const [patFilter, setPat] = useState<string>("all");
  const [selected, setSelected] = useState<Entity | null>(null);

  useEffect(() => {
    fetch("/api/social-credit-engine")
      .then((r) => r.json())
      .then(setData)
      .catch(console.error);
  }, []);

  if (!data) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-red-400 text-lg animate-pulse">Chargement Crédit Social...</div>
    </div>
  );

  const { entities, summary } = data;
  const filtered = entities.filter((e) =>
    (filter === "all" || e.risk_level === filter) &&
    (patFilter === "all" || e.social_credit_pattern === patFilter)
  );

  const avgControl        = entities.length > 0 ? entities.reduce((a, e) => a + e.control_score, 0) / entities.length : 0;
  const avgOpacity        = entities.length > 0 ? entities.reduce((a, e) => a + e.opacity_score, 0) / entities.length : 0;
  const avgPunishment     = entities.length > 0 ? entities.reduce((a, e) => a + e.punishment_score, 0) / entities.length : 0;
  const avgHomogenization = entities.length > 0 ? entities.reduce((a, e) => a + e.homogenization_score, 0) / entities.length : 0;

  const dists = [
    { title: "Risque",    counts: summary.risk_distribution,     colors: RISK_COLORS },
    { title: "Patron",    counts: summary.pattern_distribution,  colors: PAT_COLORS  },
    { title: "Sévérité",  counts: summary.severity_distribution, colors: SEV_COLORS  },
    { title: "Action",    counts: summary.action_distribution,   colors: ACT_COLORS  },
  ] as Array<{ title: string; counts: Record<string, number>; colors: Record<string, string> }>;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {selected && <DetailModal entity={selected} onClose={() => setSelected(null)} />}

      <div>
        <h1 className="text-2xl font-bold text-white">
          Crédit Social &amp; Score Comportemental — Module 348
        </h1>
        <p className="text-slate-400 text-sm mt-1">
          Contrôle · Opacité · Punition · Homogénéisation — surveillance systémique du crédit social comportemental
        </p>
      </div>

      {/* KPI cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {[
          ["Total Systèmes",      summary.total_entities,                                            "text-red-400"],
          ["Contrôle Total",      summary.critical_count,                                            "text-red-500"],
          ["Système Avancé",      summary.high_count,                                                "text-purple-400"],
          ["Composite Moyen",     summary.avg_composite.toFixed(1),                                  "text-slate-300"],
          ["Index Crédit Social", `${summary.avg_estimated_social_credit_index.toFixed(2)}/10`,      "text-red-400"],
          ["Contrôle Moyen",      `${Math.round(avgControl)}`,                                       "text-purple-300"],
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
          <GaugeRing value={avgControl}        label="Contrôle"        color="#ef4444" />
          <GaugeRing value={avgOpacity}        label="Opacité"         color="#dc2626" />
          <GaugeRing value={avgPunishment}     label="Punition"        color="#a21caf" />
          <GaugeRing value={avgHomogenization} label="Homogénéisation" color="#7e22ce" />
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
                ? "bg-red-800 border-red-700 text-white"
                : "bg-slate-900 border-slate-700 text-slate-400 hover:text-white"
            }`}
          >
            {r === "all" ? "Tous" : r}
          </button>
        ))}
        <span className="w-px h-5 self-center bg-slate-700" />
        {[
          "all",
          "none",
          "total_behavioral_control",
          "dissent_elimination",
          "collective_punishment_system",
          "behavioral_homogenization_lock",
          "corporate_state_score_fusion",
        ].map((p) => (
          <button
            key={p}
            onClick={() => setPat(p)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${
              patFilter === p
                ? "bg-red-800 border-red-700 text-white"
                : "bg-slate-900 border-slate-700 text-slate-400 hover:text-white hover:border-red-700"
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
            key={e.entity_id}
            onClick={() => setSelected(e)}
            className="bg-slate-900 border border-slate-800 rounded-xl p-4 cursor-pointer hover:border-red-700 transition-colors"
          >
            <div className="flex items-center justify-between mb-1">
              <span className="font-bold text-white">{e.entity_id}</span>
              <span className="text-xs text-slate-400">{e.region}</span>
            </div>
            <div className="text-xs text-purple-400 mb-2 capitalize">
              {e.control_domain.replace(/_/g, " ")}
            </div>
            <div className="flex gap-1 mb-3 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[e.risk_level] || "bg-slate-700 text-slate-300"}`}>
                {e.risk_level}
              </span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${PAT_BADGE[e.social_credit_pattern] || "bg-slate-700 text-slate-300"}`}>
                {e.social_credit_pattern.replace(/_/g, " ")}
              </span>
            </div>
            <div className="text-2xl font-black text-white mb-1">{e.composite_score.toFixed(1)}</div>
            <div className="text-xs text-slate-500 mb-2 capitalize">{e.severity.replace(/_/g, " ")}</div>
            <div className="text-xs text-red-400 font-medium mb-2">
              Score: {(e.behavioral_score_deployment_density * 100).toFixed(0)}%
            </div>
            <div className="text-xs text-slate-400 leading-snug line-clamp-2">{e.signal}</div>
          </div>
        ))}
      </div>
    </div>
  );
}
