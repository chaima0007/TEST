"use client";
import { useEffect, useState } from "react";

type Entity = {
  entity_id: string;
  economic_zone: string;
  region: string;
  concentration_score: number;
  mobility_score: number;
  capture_score: number;
  systemic_score: number;
  composite_score: number;
  risk_level: string;
  wealth_pattern: string;
  severity: string;
  recommended_action: string;
  signal: string;
  top_1_percent_wealth_share: number;
  democratic_process_plutocratic_capture: number;
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
  avg_estimated_plutocracy_index: number;
  avg_concentration_score: number;
  avg_mobility_score: number;
  avg_capture_score: number;
  avg_systemic_score: number;
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
      <span className="text-xs text-amber-300/70 text-center">{label}</span>
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
      <span className="text-xs text-amber-300/70 font-medium">{title}</span>
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
          <span key={k} className="text-xs text-amber-300/60">
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
  plutocracy_lock_in: "#ef4444",
  wealth_singularity: "#f97316",
  social_immobility_trap: "#a855f7",
  tax_impunity_regime: "#f59e0b",
  media_plutocracy: "#06b6d4",
};

const SEVERITY_COLORS: Record<string, string> = {
  "inégalité_gérée": "#10b981",
  "inégalité_structurelle_active": "#f59e0b",
  "concentration_richesse_dangereuse": "#f97316",
  "ploutocratie_systémique_avancée": "#ef4444",
};

const ACTION_COLORS: Record<string, string> = {
  veille_concentration_richesse: "#10b981",
  renforcement_redistribution_systémique: "#06b6d4",
  "démantèlement_capture_oligarchique": "#f59e0b",
  "réforme_fiscale_urgente_ploutocratie": "#ef4444",
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
        className="bg-slate-950 border border-amber-700/30 rounded-xl w-full max-w-lg p-6 shadow-2xl"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="flex items-center justify-between mb-4">
          <div>
            <span className="text-lg font-bold text-white">{entity.entity_id}</span>
            <span className="ml-2 text-amber-400 text-xs">{entity.economic_zone}</span>
            <span className="ml-2 text-slate-500 text-xs">{entity.region}</span>
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
                  ? "bg-amber-800 text-white"
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
              ["Concentration", entity.concentration_score, "#ef4444"],
              ["Mobilité", entity.mobility_score, "#f97316"],
              ["Capture", entity.capture_score, "#a855f7"],
              ["Systémique", entity.systemic_score, "#f59e0b"],
            ].map(([l, v, c]) => (
              <div
                key={String(l)}
                className="bg-slate-900 border border-amber-700/20 rounded-lg p-3"
              >
                <div className="text-amber-300/60 text-xs mb-1">{String(l)}</div>
                <div className="text-white font-bold text-lg">{Number(v).toFixed(1)}</div>
                <div className="h-1.5 rounded mt-1 bg-slate-800">
                  <div
                    className="h-1.5 rounded"
                    style={{ width: `${Math.min(Number(v), 100)}%`, background: String(c) }}
                  />
                </div>
              </div>
            ))}
            <div className="col-span-2 bg-slate-900 border border-amber-700/20 rounded-lg p-3">
              <div className="text-amber-300/60 text-xs mb-1">Score Composite</div>
              <div className="text-white font-bold text-2xl">
                {entity.composite_score.toFixed(1)}
              </div>
            </div>
          </div>
        )}

        {tab === "signal" && (
          <div className="bg-slate-900 border border-amber-700/20 rounded-lg p-4 text-sm text-slate-200 leading-relaxed">
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
            <div className="bg-slate-900 border border-amber-700/20 rounded-lg p-3">
              <div className="text-amber-300/60 text-xs mb-1">Action Recommandée</div>
              <div className="text-white font-medium">
                {entity.recommended_action.replace(/_/g, " ")}
              </div>
            </div>
            <div className="bg-slate-900 border border-amber-700/20 rounded-lg p-3">
              <div className="text-amber-300/60 text-xs mb-1">Patron de Richesse</div>
              <div className="text-white font-medium">
                {entity.wealth_pattern.replace(/_/g, " ")}
              </div>
            </div>
            <div className="bg-slate-900 border border-amber-700/20 rounded-lg p-3">
              <div className="text-amber-300/60 text-xs mb-1">Sévérité</div>
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

export default function WealthConcentrationDashboard() {
  const [data, setData] = useState<{ entities: Entity[]; summary: Summary } | null>(null);
  const [filter, setFilter] = useState<string>("Tous");
  const [selected, setSelected] = useState<Entity | null>(null);

  useEffect(() => {
    fetch("/api/wealth-concentration-engine")
      .then((r) => r.json())
      .then(setData)
      .catch(console.error);
  }, []);

  if (!data) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center">
        <div className="text-amber-400 text-lg animate-pulse">
          Initialisation Moteur Concentration Richesses...
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

  const avgConcentration =
    entities.length > 0
      ? entities.reduce((s, e) => s + e.concentration_score, 0) / entities.length
      : 0;

  const distBars = [
    { title: "Niveau de Risque", counts: summary.risk_distribution, colors: RISK_COLORS },
    { title: "Patrons de Richesse", counts: summary.pattern_distribution, colors: PATTERN_COLORS },
    { title: "Sévérité", counts: summary.severity_distribution, colors: SEVERITY_COLORS },
    { title: "Actions", counts: summary.action_distribution, colors: ACTION_COLORS },
  ] as Array<{ title: string; counts: Record<string, number>; colors: Record<string, string> }>;

  const filterPills = ["Tous", "Critique", "Élevé", "Modéré", "Faible"];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {selected && (
        <DetailModal entity={selected} onClose={() => setSelected(null)} />
      )}

      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-amber-400">
          Concentration Extrême des Richesses &amp; Ploutocratie — Module 343
        </h1>
        <p className="text-slate-500 text-sm mt-1">
          Concentration · Mobilité · Capture · Systémique — Caelum Partners — Chaima Mhadbi,
          Fondatrice, Bruxelles
        </p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {[
          ["Total Zones", summary.total_entities, "text-amber-400"],
          ["Ploutocratie Systémique", summary.critical_count, "text-red-400"],
          ["Concentration Dangereuse", summary.high_count, "text-orange-300"],
          ["Composite Moyen", summary.avg_composite.toFixed(1), "text-amber-300"],
          ["Index Ploutocratie", summary.avg_estimated_plutocracy_index, "text-red-300"],
          ["Concentration Moyenne", avgConcentration.toFixed(1), "text-amber-200"],
        ].map(([l, v, c]) => (
          <div
            key={String(l)}
            className="bg-slate-900 border border-slate-600/30 rounded-xl p-3 text-center"
          >
            <div className={`text-xl font-bold ${c}`}>{v}</div>
            <div className="text-xs text-amber-300/40 mt-0.5 leading-tight">{l}</div>
          </div>
        ))}
      </div>

      {/* Gauge Rings */}
      <div className="bg-slate-900 border border-slate-600/30 rounded-xl p-5">
        <div className="text-xs text-amber-300/60 mb-4 font-medium uppercase tracking-wide">
          Scores Moyens par Dimension
        </div>
        <div className="grid grid-cols-4 gap-4">
          <GaugeRing
            value={summary.avg_concentration_score}
            label="Concentration"
            color="#ef4444"
          />
          <GaugeRing
            value={summary.avg_mobility_score}
            label="Mobilité"
            color="#f97316"
          />
          <GaugeRing
            value={summary.avg_capture_score}
            label="Capture"
            color="#a855f7"
          />
          <GaugeRing
            value={summary.avg_systemic_score}
            label="Systémique"
            color="#f59e0b"
          />
        </div>
      </div>

      {/* Distribution Bars */}
      <div className="bg-slate-900 border border-slate-600/30 rounded-xl p-5 grid grid-cols-1 md:grid-cols-2 gap-5">
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
                ? "bg-amber-800 border-amber-700 text-white"
                : "bg-slate-900 border-slate-600/30 text-amber-400/70 hover:text-white"
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
            key={e.entity_id}
            onClick={() => setSelected(e)}
            className="bg-slate-900 border border-slate-600/30 rounded-xl p-4 cursor-pointer hover:border-amber-600 transition-colors"
          >
            <div className="flex items-center justify-between mb-1">
              <span className="font-bold text-white">{e.entity_id}</span>
              <span className="text-xs text-amber-400/60">{e.region}</span>
            </div>
            <div className="text-xs text-slate-500 mb-2 capitalize">
              {e.economic_zone.replace(/_/g, " ")}
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
            <div className="text-xs text-amber-400/60 mb-2 capitalize">
              {e.wealth_pattern.replace(/_/g, " ")}
            </div>
            <div className="text-xs text-amber-400 font-medium truncate">
              {e.recommended_action.replace(/_/g, " ")}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
