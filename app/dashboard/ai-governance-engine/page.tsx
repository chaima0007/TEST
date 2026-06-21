"use client";
import { useEffect, useState } from "react";

type Entity = {
  id: string;
  governance_context: string;
  region: string;
  regulatory_score: number;
  accountability_score: number;
  governance_score: number;
  systemic_score: number;
  composite_score: number;
  risk_level: string;
  ai_governance_pattern: string;
  severity: string;
  recommended_action: string;
  signal: string;
  AI_regulatory_fragmentation_index: number;
  existential_risk_regulatory_blindspot: number;
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
  avg_estimated_ai_governance_index: number;
  avg_regulatory_score: number;
};

// ── Sub-components ─────────────────────────────────────────────────────────────

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
  low: "#10b981",
  moderate: "#f59e0b",
  high: "#f97316",
  critical: "#ef4444",
};

const PATTERN_COLORS: Record<string, string> = {
  none: "#10b981",
  governance_vacuum_crisis: "#ef4444",
  accountability_collapse: "#f97316",
  AI_regulatory_capture: "#a855f7",
  existential_risk_blindspot: "#dc2626",
  geopolitical_standards_war: "#7c3aed",
};

const SEVERITY_COLORS: Record<string, string> = {
  "gouvernance_IA_relative": "#10b981",
  "fragilité_gouvernance_IA_structurelle": "#f59e0b",
  "crise_régulation_IA_majeure": "#f97316",
  "vide_gouvernance_IA_systémique": "#ef4444",
};

const ACTION_COLORS: Record<string, string> = {
  veille_gouvernance_IA_continue: "#10b981",
  "renforcement_oversight_IA_démocratique": "#06b6d4",
  "régulation_IA_internationale_accélérée": "#f59e0b",
  intervention_gouvernance_IA_urgente: "#ef4444",
};

const RISK_BADGE: Record<string, string> = {
  low: "bg-emerald-900 text-emerald-300",
  moderate: "bg-amber-900 text-amber-300",
  high: "bg-orange-900 text-orange-300",
  critical: "bg-red-900 text-red-300",
};

// ── Detail Modal ───────────────────────────────────────────────────────────────

function DetailModal({ entity, onClose }: { entity: Entity; onClose: () => void }) {
  const [tab, setTab] = useState<"scores" | "signal" | "action">("scores");

  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
    };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
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
            <span className="text-lg font-bold text-white">{entity.id}</span>
            <span className="ml-2 text-blue-400 text-xs">{entity.region}</span>
            <span className="ml-2 text-slate-500 text-xs">
              {entity.governance_context.replace(/_/g, " ")}
            </span>
          </div>
          <button
            onClick={onClose}
            className="text-slate-500 hover:text-white text-xl leading-none"
          >
            ✕
          </button>
        </div>

        <div className="flex gap-2 mb-4">
          {(["scores", "signal", "action"] as const).map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`px-3 py-1 rounded text-xs font-medium transition-colors ${
                tab === t
                  ? "bg-blue-900 text-white"
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
              ["Réglementaire", entity.regulatory_score, "#38bdf8"],
              ["Responsabilité", entity.accountability_score, "#f97316"],
              ["Gouvernance", entity.governance_score, "#a855f7"],
              ["Systémique", entity.systemic_score, "#ef4444"],
            ].map(([l, v, c]) => (
              <div
                key={String(l)}
                className="bg-slate-900 border border-blue-700/20 rounded-lg p-3"
              >
                <div className="text-blue-300/60 text-xs mb-1">{String(l)}</div>
                <div className="text-white font-bold text-lg">{Number(v).toFixed(1)}</div>
                <div className="h-1.5 rounded mt-1 bg-slate-800">
                  <div
                    className="h-1.5 rounded"
                    style={{ width: `${Math.min(Number(v), 100)}%`, background: String(c) }}
                  />
                </div>
              </div>
            ))}
            <div className="col-span-2 bg-slate-900 border border-blue-700/20 rounded-lg p-3">
              <div className="text-blue-300/60 text-xs mb-1">Score Composite Gouvernance IA</div>
              <div className="text-white font-bold text-2xl">
                {entity.composite_score.toFixed(1)}
              </div>
            </div>
          </div>
        )}

        {tab === "signal" && (
          <div className="bg-slate-900 border border-blue-700/20 rounded-lg p-4 text-sm text-slate-200 leading-relaxed">
            <div className="text-base mb-3">{entity.signal}</div>
            <div className="mt-3 flex gap-2 flex-wrap">
              <span
                className={`px-2 py-0.5 rounded text-xs font-medium ${
                  RISK_BADGE[entity.risk_level] || "bg-slate-700 text-slate-300"
                }`}
              >
                {entity.risk_level}
              </span>
              <span className="px-2 py-0.5 rounded text-xs font-medium bg-slate-700 text-slate-300">
                {entity.severity.replace(/_/g, " ")}
              </span>
            </div>
          </div>
        )}

        {tab === "action" && (
          <div className="space-y-3 text-sm">
            <div className="bg-slate-900 border border-blue-700/20 rounded-lg p-3">
              <div className="text-blue-300/60 text-xs mb-1">Action Recommandée</div>
              <div className="text-white font-medium">
                {entity.recommended_action.replace(/_/g, " ")}
              </div>
            </div>
            <div className="bg-slate-900 border border-blue-700/20 rounded-lg p-3">
              <div className="text-blue-300/60 text-xs mb-1">Patron de Gouvernance IA</div>
              <div className="text-white font-medium">
                {entity.ai_governance_pattern.replace(/_/g, " ")}
              </div>
            </div>
            <div className="bg-slate-900 border border-blue-700/20 rounded-lg p-3">
              <div className="text-blue-300/60 text-xs mb-1">Sévérité</div>
              <div className="text-white font-medium">
                {entity.severity.replace(/_/g, " ")}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

// ── Main Dashboard ─────────────────────────────────────────────────────────────

export default function AIGovernanceDashboard() {
  const [data, setData] = useState<{ entities: Entity[]; summary: Summary } | null>(null);
  const [filter, setFilter] = useState<string>("Tous");
  const [selected, setSelected] = useState<Entity | null>(null);

  useEffect(() => {
    fetch("/api/ai-governance-engine")
      .then((r) => r.json())
      .then(setData)
      .catch(console.error);
  }, []);

  if (!data) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center">
        <div className="text-blue-400 text-lg animate-pulse">
          Initialisation Moteur Gouvernance IA &amp; Intelligence Réglementaire...
        </div>
      </div>
    );
  }

  const { entities, summary } = data;

  const filterMap: Record<string, string | null> = {
    Tous: null,
    Critique: "critical",
    Élevé: "high",
    Modéré: "moderate",
    Faible: "low",
  };

  const filtered = entities.filter((e) => {
    const target = filterMap[filter];
    return target === null || e.risk_level === target;
  });

  const avgRegulatoryScore =
    entities.length > 0
      ? entities.reduce((s, e) => s + e.regulatory_score, 0) / entities.length
      : 0;

  const avgAccountabilityScore =
    entities.length > 0
      ? entities.reduce((s, e) => s + e.accountability_score, 0) / entities.length
      : 0;

  const avgGovernanceScore =
    entities.length > 0
      ? entities.reduce((s, e) => s + e.governance_score, 0) / entities.length
      : 0;

  const avgSystemicScore =
    entities.length > 0
      ? entities.reduce((s, e) => s + e.systemic_score, 0) / entities.length
      : 0;

  const distBars = [
    { title: "Distribution par Patron", counts: summary.pattern_distribution, colors: PATTERN_COLORS },
    { title: "Niveau de Risque", counts: summary.risk_distribution, colors: RISK_COLORS },
    { title: "Sévérité", counts: summary.severity_distribution, colors: SEVERITY_COLORS },
    { title: "Actions Déclenchées", counts: summary.action_distribution, colors: ACTION_COLORS },
  ] as Array<{ title: string; counts: Record<string, number>; colors: Record<string, string> }>;

  const filterPills = ["Tous", "Critique", "Élevé", "Modéré", "Faible"];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {selected && (
        <DetailModal entity={selected} onClose={() => setSelected(null)} />
      )}

      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-blue-400">
          Gouvernance IA &amp; Intelligence Réglementaire — Module 360
        </h1>
        <p className="text-slate-500 text-sm mt-1">
          Réglementaire · Responsabilité · Gouvernance · Systémique — Caelum Partners — Chaima Mhadbi,
          Fondatrice, Bruxelles
        </p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {[
          ["Total Contextes", summary.total_entities, "text-blue-400"],
          ["Vide Gouvernance", summary.critical_count, "text-red-400"],
          ["Crise Régulation", summary.high_count, "text-orange-300"],
          ["Composite Moyen", summary.avg_composite.toFixed(1), "text-blue-300"],
          ["Index Gouvernance IA", summary.avg_estimated_ai_governance_index, "text-violet-400"],
          ["Réglementaire Moyen", avgRegulatoryScore.toFixed(1), "text-sky-300"],
        ].map(([l, v, c]) => (
          <div
            key={String(l)}
            className="bg-slate-900 border border-blue-700/30 rounded-xl p-3 text-center"
          >
            <div className={`text-xl font-bold ${c}`}>{v}</div>
            <div className="text-xs text-blue-300/40 mt-0.5 leading-tight">{l}</div>
          </div>
        ))}
      </div>

      {/* Gauge Rings */}
      <div className="bg-slate-900 border border-blue-700/30 rounded-xl p-5">
        <div className="text-xs text-blue-300/60 mb-4 font-medium uppercase tracking-wide">
          Scores Moyens par Dimension
        </div>
        <div className="grid grid-cols-4 gap-4">
          <GaugeRing
            value={avgRegulatoryScore}
            label="Réglementaire"
            color="#38bdf8"
          />
          <GaugeRing
            value={avgAccountabilityScore}
            label="Responsabilité"
            color="#f97316"
          />
          <GaugeRing
            value={avgGovernanceScore}
            label="Gouvernance"
            color="#a855f7"
          />
          <GaugeRing
            value={avgSystemicScore}
            label="Systémique"
            color="#ef4444"
          />
        </div>
      </div>

      {/* Distribution Bars */}
      <div className="bg-slate-900 border border-blue-700/30 rounded-xl p-5 grid grid-cols-1 md:grid-cols-2 gap-5">
        {distBars.map((d) => (
          <DistBar key={d.title} title={d.title} counts={d.counts} colors={d.colors} />
        ))}
      </div>

      {/* Filter Pills */}
      <div className="flex flex-wrap gap-2">
        {filterPills.map((pill) => (
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

      {/* Entity Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {filtered.map((e) => (
          <div
            key={e.id}
            onClick={() => setSelected(e)}
            className="bg-slate-900 border border-blue-700/30 rounded-xl p-4 cursor-pointer hover:border-blue-500 transition-colors"
          >
            <div className="flex items-center justify-between mb-1">
              <span className="font-bold text-white">{e.id}</span>
              <span className="text-xs text-blue-400/60">{e.region}</span>
            </div>
            <div className="text-xs text-slate-500 mb-2 capitalize">
              {e.governance_context.replace(/_/g, " ")}
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
            <div className="text-xs text-blue-400/60 mb-2 capitalize">
              {e.ai_governance_pattern.replace(/_/g, " ")}
            </div>
            <div className="text-xs text-violet-400 font-medium truncate">
              {e.recommended_action.replace(/_/g, " ")}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
