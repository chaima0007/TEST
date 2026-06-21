"use client";
import { useEffect, useState, useRef } from "react";

// ─── Types ────────────────────────────────────────────────────────────────────

type TippingRisk     = "critical" | "high" | "moderate" | "low";
type TippingPattern  = "thermal_runaway" | "permafrost_collapse" | "ocean_system_failure" | "biosphere_cascade" | "arctic_tipping" | "none";
type TippingSeverity = "planetary_emergency" | "critical_tipping" | "tipping_developing" | "ecosystem_stable";
type TippingAction   = "planetary_emergency_protocol" | "carbon_emergency_brake" | "ecosystem_crisis_response" | "tipping_monitoring" | "no_action";

interface CtpEntity {
  id: string;
  region: string;
  ecosystem_type: string;
  tipping_risk: TippingRisk;
  tipping_pattern: TippingPattern;
  tipping_severity: TippingSeverity;
  recommended_action: TippingAction;
  thermal_score: number;
  ecosystem_score: number;
  feedback_score: number;
  vulnerability_score: number;
  tipping_composite: number;
  is_tipping_crisis: boolean;
  requires_tipping_intervention: boolean;
  tipping_signal: string;
}

interface CtpSummary {
  total: number;
  risk_counts: Record<string, number>;
  pattern_counts: Record<string, number>;
  severity_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_tipping_composite: number;
  tipping_crisis_count: number;
  tipping_intervention_count: number;
  avg_thermal_score: number;
  avg_ecosystem_score: number;
  avg_feedback_score: number;
  avg_vulnerability_score: number;
  avg_estimated_tipping_index: number;
}

// ─── Meta ─────────────────────────────────────────────────────────────────────

const RISK_META: Record<TippingRisk, { label: string; color: string; ring: string; bg: string; badge: string }> = {
  critical: { label: "Critique",  color: "text-red-400",     ring: "#f87171", bg: "bg-red-950/40",     badge: "bg-red-900/60 text-red-300 border-red-700" },
  high:     { label: "Élevé",     color: "text-orange-400",  ring: "#fb923c", bg: "bg-orange-950/40",  badge: "bg-orange-900/60 text-orange-300 border-orange-700" },
  moderate: { label: "Modéré",    color: "text-amber-400",   ring: "#fbbf24", bg: "bg-amber-950/40",   badge: "bg-amber-900/60 text-amber-300 border-amber-700" },
  low:      { label: "Faible",    color: "text-teal-400",    ring: "#2dd4bf", bg: "bg-teal-950/40",    badge: "bg-teal-900/60 text-teal-300 border-teal-700" },
};

const PATTERN_LABELS: Record<TippingPattern, string> = {
  thermal_runaway:      "Emballement Thermique",
  permafrost_collapse:  "Effondrement Pergélisol",
  ocean_system_failure: "Défaillance Système Océanique",
  biosphere_cascade:    "Cascade Biosphère",
  arctic_tipping:       "Basculement Arctique",
  none:                 "Aucun",
};

const SEV_LABELS: Record<TippingSeverity, string> = {
  planetary_emergency: "Urgence Planétaire",
  critical_tipping:    "Basculement Critique",
  tipping_developing:  "Basculement Émergent",
  ecosystem_stable:    "Écosystème Stable",
};

const ACTION_LABELS: Record<TippingAction, string> = {
  planetary_emergency_protocol: "Protocole Urgence Planétaire",
  carbon_emergency_brake:       "Frein d'Urgence Carbone",
  ecosystem_crisis_response:    "Réponse Crise Écosystème",
  tipping_monitoring:           "Surveillance Basculement",
  no_action:                    "Aucune Action",
};

const RISK_COLORS: Record<string, string> = {
  critical: "#ef4444",
  high:     "#f97316",
  moderate: "#f59e0b",
  low:      "#14b8a6",
};

const PAT_COLORS: Record<string, string> = {
  thermal_runaway:      "#ef4444",
  permafrost_collapse:  "#f97316",
  ocean_system_failure: "#3b82f6",
  biosphere_cascade:    "#22c55e",
  arctic_tipping:       "#a855f7",
  none:                 "#14b8a6",
};

const SEV_COLORS: Record<string, string> = {
  planetary_emergency: "#ef4444",
  critical_tipping:    "#f97316",
  tipping_developing:  "#f59e0b",
  ecosystem_stable:    "#14b8a6",
};

const ACT_COLORS: Record<string, string> = {
  planetary_emergency_protocol: "#ef4444",
  carbon_emergency_brake:       "#f97316",
  ecosystem_crisis_response:    "#f59e0b",
  tipping_monitoring:           "#06b6d4",
  no_action:                    "#14b8a6",
};

// ─── GaugeRing ────────────────────────────────────────────────────────────────

function GaugeRing({ value, label, color }: { value: number; label: string; color: string }) {
  const r = 36;
  const circ = 2 * Math.PI * r;
  const fill = circ * (1 - value / 100);
  return (
    <div className="flex flex-col items-center gap-1">
      <svg width="88" height="88" viewBox="0 0 88 88">
        <circle cx="44" cy="44" r={r} fill="none" stroke="#1e293b" strokeWidth="8" />
        <circle
          cx="44" cy="44" r={r} fill="none"
          stroke={color} strokeWidth="8"
          strokeDasharray={circ}
          strokeDashoffset={fill}
          strokeLinecap="round"
          transform="rotate(-90 44 44)"
        />
        <text x="44" y="49" textAnchor="middle" fill="white" fontSize="13" fontWeight="bold" fontFamily="sans-serif">
          {Math.round(value)}
        </text>
      </svg>
      <span className="text-xs text-slate-400 text-center">{label}</span>
    </div>
  );
}

// ─── DistBar ──────────────────────────────────────────────────────────────────

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
            <span style={{ color: colors[k] || "#94a3b8" }}>■</span> {k.replace(/_/g, " ")} {v}
          </span>
        ))}
      </div>
    </div>
  );
}

// ─── DetailModal ──────────────────────────────────────────────────────────────

function DetailModal({ entity, onClose }: { entity: CtpEntity; onClose: () => void }) {
  const [tab, setTab] = useState<"scores" | "signal" | "action">("scores");
  const overlayRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const fn = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", fn);
    return () => window.removeEventListener("keydown", fn);
  }, [onClose]);

  const rm = RISK_META[entity.tipping_risk];

  return (
    <div
      ref={overlayRef}
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 p-4"
      onClick={(e) => { if (e.target === overlayRef.current) onClose(); }}
    >
      <div className="bg-slate-900 border border-emerald-700/30 rounded-2xl w-full max-w-lg shadow-2xl max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="flex items-center justify-between p-5 border-b border-slate-800">
          <div>
            <div className="flex items-center gap-2 flex-wrap">
              <span className="text-lg font-bold text-white">{entity.id}</span>
              <span className="text-teal-400 text-xs">{entity.region}</span>
              <span className={`text-xs font-bold px-2 py-0.5 rounded border ${rm.badge}`}>{rm.label}</span>
            </div>
            <p className="text-slate-400 text-sm capitalize mt-0.5">{entity.ecosystem_type.replace(/_/g, " ")}</p>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl leading-none p-1">✕</button>
        </div>

        {/* Tabs */}
        <div className="flex border-b border-slate-800">
          {(["scores", "signal", "action"] as const).map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`flex-1 py-2.5 text-xs font-semibold uppercase tracking-wide transition-colors ${
                tab === t ? "text-teal-400 border-b-2 border-teal-400" : "text-slate-500 hover:text-slate-300"
              }`}
            >
              {t === "scores" ? "Scores" : t === "signal" ? "Signal" : "Action"}
            </button>
          ))}
        </div>

        {/* Tab content */}
        <div className="p-5">
          {tab === "scores" && (
            <div className="space-y-3">
              <div className="grid grid-cols-2 gap-3">
                {[
                  ["Thermique",     entity.thermal_score,       "#f87171"],
                  ["Écosystème",    entity.ecosystem_score,     "#34d399"],
                  ["Rétroaction",   entity.feedback_score,      "#60a5fa"],
                  ["Vulnérabilité", entity.vulnerability_score, "#fb923c"],
                ].map(([l, v, c]) => (
                  <div key={String(l)} className="bg-slate-800 rounded-lg p-3">
                    <div className="text-slate-400 text-xs mb-1">{String(l)}</div>
                    <div className="text-white font-bold text-lg">{Number(v).toFixed(1)}</div>
                    <div className="h-1.5 rounded mt-1 bg-slate-700">
                      <div
                        className="h-1.5 rounded"
                        style={{ width: `${Math.min(Number(v), 100)}%`, background: String(c) }}
                      />
                    </div>
                  </div>
                ))}
              </div>
              <div className="bg-slate-800 rounded-lg p-3">
                <div className="text-slate-400 text-xs mb-1">Composite Basculement</div>
                <div className="text-white font-bold text-2xl">{entity.tipping_composite.toFixed(1)}</div>
                <div className="text-xs text-slate-500 mt-0.5">{SEV_LABELS[entity.tipping_severity]}</div>
              </div>
            </div>
          )}

          {tab === "signal" && (
            <div className="bg-slate-800 rounded-lg p-4 text-sm text-slate-200 leading-relaxed">
              {entity.tipping_signal}
              <div className="mt-3 flex gap-2 flex-wrap">
                <span className={`px-2 py-0.5 rounded text-xs font-medium ${rm.badge}`}>{rm.label}</span>
                <span className="px-2 py-0.5 rounded text-xs font-medium bg-slate-700 text-slate-300">
                  {PATTERN_LABELS[entity.tipping_pattern]}
                </span>
              </div>
            </div>
          )}

          {tab === "action" && (
            <div className="space-y-3 text-sm">
              <div className="bg-slate-800 rounded-lg p-3">
                <div className="text-slate-400 text-xs mb-1">Action Recommandée</div>
                <div className="text-teal-300 font-medium">{ACTION_LABELS[entity.recommended_action]}</div>
              </div>
              <div className="bg-slate-800 rounded-lg p-3">
                <div className="text-slate-400 text-xs mb-1">Pattern Climatique</div>
                <div className="text-white font-medium">{PATTERN_LABELS[entity.tipping_pattern]}</div>
              </div>
              <div className="bg-slate-800 rounded-lg p-3">
                <div className="text-slate-400 text-xs mb-1">Sévérité</div>
                <div className="text-white font-medium">{SEV_LABELS[entity.tipping_severity]}</div>
              </div>
              <div className="flex gap-2 flex-wrap">
                {entity.is_tipping_crisis && (
                  <span className="px-2 py-1 rounded bg-red-900/60 text-red-300 text-xs font-bold border border-red-700">
                    CRISE
                  </span>
                )}
                {entity.requires_tipping_intervention && (
                  <span className="px-2 py-1 rounded bg-orange-900/60 text-orange-300 text-xs font-bold border border-orange-700">
                    INTERVENTION
                  </span>
                )}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

// ─── EntityCard ───────────────────────────────────────────────────────────────

function EntityCard({ entity, onClick }: { entity: CtpEntity; onClick: () => void }) {
  const rm = RISK_META[entity.tipping_risk];

  return (
    <button
      onClick={onClick}
      className={`w-full text-left rounded-xl border border-slate-800 ${rm.bg} p-4 hover:border-emerald-700/50 transition-colors`}
    >
      <div className="flex items-center justify-between mb-2">
        <span className="font-bold text-white">{entity.id}</span>
        <span className="text-xs text-teal-400">{entity.region}</span>
      </div>
      <div className="text-xs text-slate-400 mb-2 capitalize">{entity.ecosystem_type.replace(/_/g, " ")}</div>
      <div className="flex gap-1 mb-3 flex-wrap">
        <span className={`px-2 py-0.5 rounded text-xs font-bold border ${rm.badge}`}>{rm.label}</span>
      </div>
      <div className="text-2xl font-black text-white mb-1">{entity.tipping_composite.toFixed(1)}</div>
      <div className="text-xs text-slate-500 mb-2 capitalize">{PATTERN_LABELS[entity.tipping_pattern]}</div>
      <div className="text-xs text-teal-400 font-medium mb-2">{SEV_LABELS[entity.tipping_severity]}</div>
      <div className="flex gap-1 flex-wrap">
        {entity.is_tipping_crisis && (
          <span className="px-1.5 py-0.5 rounded bg-red-900/60 text-red-300 text-xs font-bold border border-red-800">
            CRISE
          </span>
        )}
        {entity.requires_tipping_intervention && !entity.is_tipping_crisis && (
          <span className="px-1.5 py-0.5 rounded bg-orange-900/60 text-orange-300 text-xs font-bold border border-orange-800">
            INTERVENTION
          </span>
        )}
      </div>
    </button>
  );
}

// ─── Page ─────────────────────────────────────────────────────────────────────

export default function ClimateTippingPointsDashboard() {
  const [data, setData]         = useState<{ entities: CtpEntity[]; summary: CtpSummary } | null>(null);
  const [riskFilter, setRisk]   = useState<string>("all");
  const [patFilter,  setPat]    = useState<string>("all");
  const [selected, setSelected] = useState<CtpEntity | null>(null);

  useEffect(() => {
    fetch("/api/climate-tipping-points-engine")
      .then((r) => r.json())
      .then(setData)
      .catch(console.error);
  }, []);

  if (!data) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center">
        <div className="text-teal-400 text-lg animate-pulse">Chargement Points de Basculement Climatique…</div>
      </div>
    );
  }

  const { entities, summary } = data;

  const filtered = entities.filter(
    (e) =>
      (riskFilter === "all" || e.tipping_risk === riskFilter) &&
      (patFilter === "all" || e.tipping_pattern === patFilter),
  );

  const kpis = [
    { label: "Total Écosystèmes",    value: summary.total,                                          color: "text-teal-400" },
    { label: "En Crise Climatique",  value: summary.tipping_crisis_count,                           color: "text-red-400" },
    { label: "Requiert Intervention",value: summary.tipping_intervention_count,                     color: "text-orange-400" },
    { label: "Composite Moyen",      value: summary.avg_tipping_composite.toFixed(1),               color: "text-teal-400" },
    { label: "Index Basculement",    value: `${summary.avg_estimated_tipping_index.toFixed(2)}/10`, color: "text-emerald-400" },
    { label: "Thermique Moyen",      value: Math.round(summary.avg_thermal_score).toString(),       color: "text-orange-400" },
  ];

  const dists = [
    { title: "Risque",    counts: summary.risk_counts,     colors: RISK_COLORS },
    { title: "Patterns",  counts: summary.pattern_counts,  colors: PAT_COLORS  },
    { title: "Sévérité",  counts: summary.severity_counts, colors: SEV_COLORS  },
    { title: "Actions",   counts: summary.action_counts,   colors: ACT_COLORS  },
  ] as Array<{ title: string; counts: Record<string, number>; colors: Record<string, string> }>;

  const risks: TippingRisk[]    = ["critical", "high", "moderate", "low"];
  const patterns: TippingPattern[] = ["thermal_runaway", "permafrost_collapse", "ocean_system_failure", "biosphere_cascade", "arctic_tipping", "none"];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {selected && <DetailModal entity={selected} onClose={() => setSelected(null)} />}

      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-teal-400">Points de Basculement Climatique — Module 305</h1>
        <p className="text-slate-400 text-sm mt-1">
          Thermique · Écosystème · Rétroaction · Vulnérabilité — surveillance des seuils de basculement planétaires
        </p>
      </div>

      {/* KPI strip */}
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
        {kpis.map((k) => (
          <div key={k.label} className="bg-slate-900 border border-emerald-700/30 rounded-xl p-4 text-center">
            <div className={`text-xl font-bold ${k.color}`}>{k.value}</div>
            <div className="text-xs text-slate-500 mt-0.5">{k.label}</div>
          </div>
        ))}
      </div>

      {/* GaugeRings */}
      <div className="bg-slate-900 border border-emerald-700/30 rounded-xl p-5">
        <p className="text-xs text-slate-500 mb-4 font-semibold uppercase tracking-wide">Scores Moyens par Dimension</p>
        <div className="grid grid-cols-4 gap-4">
          <GaugeRing value={summary.avg_thermal_score}       label="Thermique"   color="#f87171" />
          <GaugeRing value={summary.avg_ecosystem_score}     label="Écosystème"  color="#34d399" />
          <GaugeRing value={summary.avg_feedback_score}      label="Rétroaction" color="#60a5fa" />
          <GaugeRing value={summary.avg_vulnerability_score} label="Vulnérabilité" color="#fb923c" />
        </div>
      </div>

      {/* DistBars */}
      <div className="bg-slate-900 border border-emerald-700/30 rounded-xl p-5 grid grid-cols-1 md:grid-cols-2 gap-5">
        {dists.map((d) => (
          <DistBar key={d.title} {...d} />
        ))}
      </div>

      {/* Filters */}
      <div className="flex flex-col gap-2">
        <div className="flex flex-wrap gap-2">
          {["all", ...risks].map((r) => (
            <button
              key={r}
              onClick={() => setRisk(r)}
              className={`px-3 py-1.5 rounded-full text-xs font-semibold border transition-colors ${
                riskFilter === r
                  ? "bg-teal-700 border-teal-600 text-white"
                  : "bg-slate-900 border-slate-700 text-slate-400 hover:text-white hover:border-teal-600"
              }`}
            >
              {r === "all" ? "Tous risques" : RISK_META[r as TippingRisk].label}
            </button>
          ))}
        </div>
        <div className="flex flex-wrap gap-2">
          {["all", ...patterns].map((p) => (
            <button
              key={p}
              onClick={() => setPat(p)}
              className={`px-3 py-1.5 rounded-full text-xs font-semibold border transition-colors ${
                patFilter === p
                  ? "bg-emerald-700 border-emerald-600 text-white"
                  : "bg-slate-900 border-slate-700 text-slate-400 hover:text-white hover:border-emerald-600"
              }`}
            >
              {p === "all" ? "Tous patterns" : PATTERN_LABELS[p as TippingPattern]}
            </button>
          ))}
        </div>
      </div>

      {/* Entity grid */}
      {filtered.length === 0 ? (
        <div className="text-center text-slate-500 py-16">Aucun écosystème pour ces filtres.</div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          {filtered.map((e) => (
            <EntityCard key={e.id} entity={e} onClick={() => setSelected(e)} />
          ))}
        </div>
      )}
    </div>
  );
}
