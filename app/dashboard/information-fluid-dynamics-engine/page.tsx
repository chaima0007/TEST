"use client";

import { useState, useEffect, useRef } from "react";

// ─── Types ────────────────────────────────────────────────────────────────────

interface SystemData {
  system_id: string;
  system_type: string;
  region: string;
  chaos_risk: string;
  chaos_pattern: string;
  flow_severity: string;
  recommended_action: string;
  turbulence_score: number;
  entropy_score: number;
  flow_score: number;
  resilience_score: number;
  chaos_composite: number;
  has_chaos_signal: boolean;
  requires_restructuring: boolean;
  estimated_chaos_index: number;
  chaos_signal: string;
}

interface Summary {
  total: number;
  risk_counts: Record<string, number>;
  pattern_counts: Record<string, number>;
  severity_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_estimated_chaos_index: number;
  chaos_signal_count: number;
  restructuring_required_count: number;
  avg_turbulence_score: number;
  avg_entropy_score: number;
  avg_flow_score: number;
  avg_resilience_score: number;
  avg_chaos_composite: number;
}

// ─── Meta helpers ─────────────────────────────────────────────────────────────

const RISK_BG: Record<string, string> = {
  low:      "bg-emerald-500/20 border-emerald-500/30 text-emerald-300",
  moderate: "bg-amber-500/20 border-amber-500/30 text-amber-300",
  high:     "bg-orange-500/20 border-orange-500/30 text-orange-300",
  critical: "bg-rose-500/20 border-rose-500/30 text-rose-300",
};
const RISK_COLOR: Record<string, string> = {
  low:      "#34d399",
  moderate: "#fbbf24",
  high:     "#f97316",
  critical: "#f87171",
};
const RISK_LABEL: Record<string, string> = {
  low:      "Faible",
  moderate: "Modéré",
  high:     "Élevé",
  critical: "Critique",
};

const SEVERITY_BG: Record<string, string> = {
  laminar:      "bg-emerald-500/15 text-emerald-300",
  transitional: "bg-amber-500/15 text-amber-300",
  turbulent:    "bg-orange-500/15 text-orange-300",
  chaotic:      "bg-rose-500/15 text-rose-300",
};
const SEVERITY_LABEL: Record<string, string> = {
  laminar:      "Laminaire",
  transitional: "Transitoire",
  turbulent:    "Turbulent",
  chaotic:      "Chaotique",
};

const ACTION_BG: Record<string, string> = {
  no_action:               "bg-emerald-500/15 text-emerald-300",
  flow_monitoring:         "bg-cyan-500/15 text-cyan-300",
  entropy_reduction:       "bg-amber-500/15 text-amber-300",
  attractor_stabilization: "bg-orange-500/15 text-orange-300",
  chaos_containment:       "bg-rose-500/15 text-rose-300",
  flow_restructuring:      "bg-red-600/15 text-red-300",
};
const ACTION_LABEL: Record<string, string> = {
  no_action:               "Aucune Action",
  flow_monitoring:         "Surveillance Flux",
  entropy_reduction:       "Réduction Entropie",
  attractor_stabilization: "Stabilisation Attracteur",
  chaos_containment:       "Confinement Chaos",
  flow_restructuring:      "Restructuration Flux",
};

const PATTERN_LABEL: Record<string, string> = {
  none:                   "Aucun",
  turbulent_cascade:      "Cascade Turbulente",
  entropy_collapse:        "Effondrement Entropique",
  bifurcation_crisis:      "Crise Bifurcation",
  vortex_lock:             "Verrouillage Vortex",
  strange_attractor_trap:  "Piège Attracteur Étrange",
};

const RISK_FILTERS    = ["all", "critical", "high", "moderate", "low"] as const;
const PATTERN_FILTERS = [
  "all",
  "turbulent_cascade",
  "entropy_collapse",
  "bifurcation_crisis",
  "vortex_lock",
  "strange_attractor_trap",
  "none",
] as const;

type RiskFilter    = typeof RISK_FILTERS[number];
type PatternFilter = typeof PATTERN_FILTERS[number];

// ─── GaugeRing ────────────────────────────────────────────────────────────────

function GaugeRing({
  pct,
  color,
  label,
  size = 90,
}: {
  pct: number;
  color: string;
  label: string;
  size?: number;
}) {
  const r    = size * 0.38;
  const circ = 2 * Math.PI * r;
  const fill = (Math.min(pct, 100) / 100) * circ;
  return (
    <div className="flex flex-col items-center gap-1">
      <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`}>
        <circle
          cx={size / 2} cy={size / 2} r={r}
          fill="none" stroke="#1e293b" strokeWidth={size * 0.1}
        />
        <circle
          cx={size / 2} cy={size / 2} r={r}
          fill="none" stroke={color} strokeWidth={size * 0.1}
          strokeDasharray={`${fill} ${circ}`}
          strokeLinecap="round"
          transform={`rotate(-90 ${size / 2} ${size / 2})`}
        />
        <text
          x={size / 2} y={size / 2 + 5}
          textAnchor="middle" fill={color}
          fontSize={size * 0.2} fontWeight="bold"
        >
          {pct.toFixed(0)}
        </text>
      </svg>
      <span className="text-xs text-slate-400 text-center">{label}</span>
    </div>
  );
}

// ─── ScoreBar ─────────────────────────────────────────────────────────────────

function ScoreBar({ score, label }: { score: number; label: string }) {
  const color =
    score <= 20
      ? "#34d399"
      : score <= 40
      ? "#fbbf24"
      : score <= 60
      ? "#f97316"
      : "#f87171";
  return (
    <div>
      <div className="flex justify-between mb-1">
        <span className="text-xs text-slate-400">{label}</span>
        <span className="text-xs font-medium" style={{ color }}>
          {score.toFixed(0)}
        </span>
      </div>
      <div className="h-1.5 bg-slate-700 rounded-full overflow-hidden">
        <div
          className="h-full rounded-full transition-all"
          style={{ width: `${Math.min(score, 100)}%`, backgroundColor: color }}
        />
      </div>
    </div>
  );
}

// ─── DistBar ──────────────────────────────────────────────────────────────────

type DistBarItem = { title: string; counts: Record<string, number>; colors: Record<string, string> };

function DistBar({ title, counts, colors }: DistBarItem) {
  const total = Object.values(counts).reduce((a, b) => a + b, 0);
  if (!total) return null;
  return (
    <div>
      <p className="text-xs text-slate-400 mb-1">{title}</p>
      <div className="flex h-2 rounded-full overflow-hidden gap-px">
        {Object.entries(counts).map(([k, v]) =>
          v > 0 ? (
            <div
              key={k}
              style={{ width: `${(v / total) * 100}%`, backgroundColor: colors[k] ?? "#94a3b8" }}
              title={`${k}: ${v}`}
            />
          ) : null,
        )}
      </div>
      <div className="flex flex-wrap gap-2 mt-1.5">
        {Object.entries(counts).map(([k, v]) => (
          <span key={k} className="text-xs" style={{ color: colors[k] ?? "#94a3b8" }}>
            {RISK_LABEL[k] ?? SEVERITY_LABEL[k] ?? PATTERN_LABEL[k] ?? ACTION_LABEL[k] ?? k}: {v}
          </span>
        ))}
      </div>
    </div>
  );
}

// ─── DetailModal ──────────────────────────────────────────────────────────────

function DetailModal({ system, onClose }: { system: SystemData; onClose: () => void }) {
  const [tab, setTab] = useState<"scores" | "signal" | "action">("scores");
  const overlayRef    = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handler = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [onClose]);

  const riskColor = RISK_COLOR[system.chaos_risk] ?? "#22d3ee";

  return (
    <div
      ref={overlayRef}
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4"
      onClick={(e) => { if (e.target === overlayRef.current) onClose(); }}
    >
      <div className="bg-slate-900 border border-cyan-700/30 rounded-xl shadow-2xl w-full max-w-lg">
        {/* Header */}
        <div className="flex items-start justify-between p-5 border-b border-slate-800">
          <div>
            <div className="flex items-center gap-2 mb-1 flex-wrap">
              <span
                className={`text-xs px-2 py-0.5 rounded-full border font-medium ${RISK_BG[system.chaos_risk] ?? ""}`}
              >
                {RISK_LABEL[system.chaos_risk] ?? system.chaos_risk}
              </span>
              <span
                className={`text-xs px-2 py-0.5 rounded-full font-medium ${SEVERITY_BG[system.flow_severity] ?? ""}`}
              >
                {SEVERITY_LABEL[system.flow_severity] ?? system.flow_severity}
              </span>
            </div>
            <h2 className="text-white font-bold text-lg">{system.system_id}</h2>
            <p className="text-slate-400 text-sm">
              {system.system_type} · {system.region} · Composite:{" "}
              <span style={{ color: riskColor }}>{system.chaos_composite}</span>
            </p>
          </div>
          <button
            onClick={onClose}
            className="text-slate-400 hover:text-white p-1 transition-colors"
            aria-label="Fermer"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        {/* Tabs */}
        <div className="flex border-b border-slate-800">
          {(["scores", "signal", "action"] as const).map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`flex-1 py-2.5 text-sm font-medium transition-colors ${
                tab === t
                  ? "text-cyan-400 border-b-2 border-cyan-500 bg-slate-800/40"
                  : "text-slate-400 hover:text-slate-200"
              }`}
            >
              {t === "scores" ? "Scores" : t === "signal" ? "Signal" : "Action"}
            </button>
          ))}
        </div>

        {/* Tab content */}
        <div className="p-5 space-y-4">
          {tab === "scores" && (
            <div className="space-y-3">
              <ScoreBar score={system.turbulence_score} label="Turbulence (30%)" />
              <ScoreBar score={system.entropy_score}    label="Entropie (25%)" />
              <ScoreBar score={system.flow_score}       label="Flux Info. (25%)" />
              <ScoreBar score={system.resilience_score} label="Résilience Bassin (20%)" />
              <div className="pt-2 border-t border-slate-800">
                <div className="flex justify-between items-center">
                  <span className="text-sm text-slate-400">Composite Chaos</span>
                  <span className="text-lg font-bold" style={{ color: riskColor }}>
                    {system.chaos_composite}
                  </span>
                </div>
                <p className="text-xs text-slate-500 mt-1">
                  Score composite indice de chaos informationnel (0–100)
                </p>
              </div>
            </div>
          )}

          {tab === "signal" && (
            <>
              <div className="flex items-center justify-center py-2">
                <GaugeRing
                  pct={system.chaos_composite}
                  color={riskColor}
                  label="Composite"
                  size={110}
                />
              </div>
              <div className="bg-slate-800/50 rounded-lg p-3">
                <p className="text-xs text-slate-400 mb-1">Signal Chaos</p>
                <p className="text-sm text-white">{system.chaos_signal}</p>
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div className="bg-slate-800/50 rounded-lg p-3">
                  <p className="text-xs text-slate-400">Indice Chaos</p>
                  <p className="text-lg font-bold text-cyan-400">
                    {system.estimated_chaos_index.toFixed(2)}
                  </p>
                </div>
                <div className="bg-slate-800/50 rounded-lg p-3">
                  <p className="text-xs text-slate-400">Signal Chaos</p>
                  <p className={`text-lg font-bold ${system.has_chaos_signal ? "text-rose-400" : "text-emerald-400"}`}>
                    {system.has_chaos_signal ? "Oui" : "Non"}
                  </p>
                </div>
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div className="bg-slate-800/50 rounded-lg p-3">
                  <p className="text-xs text-slate-400">Restructuration Requise</p>
                  <p className={`text-sm font-medium ${system.requires_restructuring ? "text-orange-400" : "text-emerald-400"}`}>
                    {system.requires_restructuring ? "Requise" : "Non requise"}
                  </p>
                </div>
                <div className="bg-slate-800/50 rounded-lg p-3">
                  <p className="text-xs text-slate-400">Pattern</p>
                  <p className="text-sm font-medium text-slate-200">
                    {PATTERN_LABEL[system.chaos_pattern] ?? system.chaos_pattern}
                  </p>
                </div>
              </div>
            </>
          )}

          {tab === "action" && (
            <div className="space-y-4">
              <div className="bg-slate-800/50 rounded-lg p-4">
                <p className="text-xs text-slate-400 mb-2">Action Recommandée</p>
                <span className={`text-sm px-3 py-1.5 rounded-lg font-medium ${ACTION_BG[system.recommended_action] ?? ""}`}>
                  {ACTION_LABEL[system.recommended_action] ?? system.recommended_action}
                </span>
              </div>
              <div className="space-y-2">
                <div className="flex justify-between p-2 rounded bg-slate-800/40">
                  <span className="text-xs text-slate-400">Sévérité Flux</span>
                  <span className="text-xs text-slate-200">
                    {SEVERITY_LABEL[system.flow_severity] ?? system.flow_severity}
                  </span>
                </div>
                <div className="flex justify-between p-2 rounded bg-slate-800/40">
                  <span className="text-xs text-slate-400">Pattern Dynamique</span>
                  <span className="text-xs text-slate-200">
                    {PATTERN_LABEL[system.chaos_pattern] ?? system.chaos_pattern}
                  </span>
                </div>
                <div className="flex justify-between p-2 rounded bg-slate-800/40">
                  <span className="text-xs text-slate-400">Indice Chaos</span>
                  <span className="text-xs text-cyan-400 font-medium">
                    {system.estimated_chaos_index.toFixed(2)}
                  </span>
                </div>
                <div className="flex justify-between p-2 rounded bg-slate-800/40">
                  <span className="text-xs text-slate-400">Signal Chaos</span>
                  <span className={`text-xs font-medium ${system.has_chaos_signal ? "text-rose-400" : "text-emerald-400"}`}>
                    {system.has_chaos_signal ? "Oui" : "Non"}
                  </span>
                </div>
                <div className="flex justify-between p-2 rounded bg-slate-800/40">
                  <span className="text-xs text-slate-400">Restructuration Requise</span>
                  <span className={`text-xs font-medium ${system.requires_restructuring ? "text-orange-400" : "text-emerald-400"}`}>
                    {system.requires_restructuring ? "Requise" : "Non requise"}
                  </span>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

// ─── SystemCard ───────────────────────────────────────────────────────────────

function SystemCard({ system, onClick }: { system: SystemData; onClick: () => void }) {
  const riskColor = RISK_COLOR[system.chaos_risk] ?? "#22d3ee";

  return (
    <div
      onClick={onClick}
      className="bg-slate-900 border border-slate-800 rounded-xl p-4 cursor-pointer hover:border-cyan-700 transition-all hover:bg-slate-800/60"
    >
      <div className="flex items-start justify-between mb-3">
        <div className="flex-1 min-w-0 pr-2">
          <div className="flex items-center gap-2 mb-1 flex-wrap">
            <span className={`text-xs px-2 py-0.5 rounded-full border font-medium ${RISK_BG[system.chaos_risk] ?? ""}`}>
              {RISK_LABEL[system.chaos_risk] ?? system.chaos_risk}
            </span>
            {system.has_chaos_signal && (
              <span className="text-xs px-2 py-0.5 rounded-full bg-rose-500/20 border border-rose-500/30 text-rose-300 font-medium">
                SIGNAL CHAOS
              </span>
            )}
          </div>
          <h3 className="text-white font-semibold text-sm">{system.system_id}</h3>
          <p className="text-slate-400 text-xs">{system.system_type} · {system.region}</p>
        </div>
        <div className="flex-shrink-0">
          <GaugeRing pct={system.chaos_composite} color={riskColor} label="" size={72} />
        </div>
      </div>

      <div className="space-y-1.5 mb-3">
        <ScoreBar score={system.turbulence_score} label="Turbulence" />
        <ScoreBar score={system.entropy_score}    label="Entropie" />
        <ScoreBar score={system.flow_score}       label="Flux Info." />
        <ScoreBar score={system.resilience_score} label="Résilience" />
      </div>

      <div className="border-t border-slate-800 pt-2 flex items-center justify-between">
        <span className={`text-xs px-2 py-0.5 rounded font-medium ${ACTION_BG[system.recommended_action] ?? ""}`}>
          {ACTION_LABEL[system.recommended_action] ?? system.recommended_action}
        </span>
        <span className="text-xs text-cyan-400 font-medium">
          idx {system.estimated_chaos_index.toFixed(2)}
        </span>
      </div>
      <div className="flex items-center gap-1.5 mt-2">
        <span className={`text-xs px-1.5 py-0.5 rounded font-medium ${SEVERITY_BG[system.flow_severity] ?? ""}`}>
          {SEVERITY_LABEL[system.flow_severity] ?? system.flow_severity}
        </span>
        <span className="text-xs text-slate-500 truncate">
          {PATTERN_LABEL[system.chaos_pattern] ?? system.chaos_pattern}
        </span>
      </div>
      <p className="text-xs text-slate-500 mt-1.5 truncate">{system.chaos_signal}</p>
    </div>
  );
}

// ─── Page ─────────────────────────────────────────────────────────────────────

export default function InformationFluidDynamicsEnginePage() {
  const [data, setData]           = useState<{ systems: SystemData[]; summary: Summary } | null>(null);
  const [loading, setLoading]     = useState(true);
  const [riskFilter, setRiskFilter]       = useState<RiskFilter>("all");
  const [patternFilter, setPatternFilter] = useState<PatternFilter>("all");
  const [selected, setSelected]   = useState<SystemData | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      const params = new URLSearchParams();
      if (riskFilter    !== "all") params.set("risk",    riskFilter);
      if (patternFilter !== "all") params.set("pattern", patternFilter);
      const res  = await fetch(`/api/information-fluid-dynamics-engine?${params}`);
      const json = await res.json();
      setData(json);
      setLoading(false);
    };
    fetchData();
  }, [riskFilter, patternFilter]);

  const s       = data?.summary;
  const systems = data?.systems ?? [];

  // ── distribution color maps ───────────────────────────────────────────────

  const riskColors: Record<string, string> = {
    low:      "#34d399",
    moderate: "#fbbf24",
    high:     "#f97316",
    critical: "#f87171",
  };
  const patternColors: Record<string, string> = {
    none:                   "#64748b",
    turbulent_cascade:      "#f87171",
    entropy_collapse:        "#f97316",
    bifurcation_crisis:      "#ef4444",
    vortex_lock:             "#a78bfa",
    strange_attractor_trap:  "#ec4899",
  };
  const severityColors: Record<string, string> = {
    laminar:      "#34d399",
    transitional: "#fbbf24",
    turbulent:    "#f97316",
    chaotic:      "#f87171",
  };
  const actionColors: Record<string, string> = {
    no_action:               "#34d399",
    flow_monitoring:         "#22d3ee",
    entropy_reduction:       "#fbbf24",
    attractor_stabilization: "#f97316",
    chaos_containment:       "#f87171",
    flow_restructuring:      "#ef4444",
  };

  const distributions: Array<DistBarItem> = [
    { title: "Risque Chaos",        counts: s?.risk_counts     ?? {}, colors: riskColors     },
    { title: "Pattern Dynamique",   counts: s?.pattern_counts  ?? {}, colors: patternColors  },
    { title: "Sévérité Flux",       counts: s?.severity_counts ?? {}, colors: severityColors },
    { title: "Action Recommandée",  counts: s?.action_counts   ?? {}, colors: actionColors   },
  ];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
      {selected && <DetailModal system={selected} onClose={() => setSelected(null)} />}

      {/* Header */}
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-cyan-400">
          Dynamique Fluide Informationnelle & Moteur Théorie du Chaos
        </h1>
        <p className="text-slate-400 text-sm mt-1">
          Turbulence · Entropie · Flux · Résilience — bifurcations, attracteurs étranges et cascades chaotiques
        </p>
      </div>

      {/* KPI strip — 6 cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 xl:grid-cols-6 gap-4 mb-6">
        <div className="bg-slate-900 border border-cyan-700/30 rounded-xl p-4">
          <p className="text-xs text-slate-400 mb-1">Systèmes Analysés</p>
          <p className="text-2xl font-bold text-white">{s?.total ?? "—"}</p>
        </div>
        <div className="bg-slate-900 border border-cyan-700/30 rounded-xl p-4">
          <p className="text-xs text-slate-400 mb-1">Cascades Critiques</p>
          <p className="text-2xl font-bold text-rose-400">{s?.risk_counts?.["critical"] ?? "—"}</p>
        </div>
        <div className="bg-slate-900 border border-cyan-700/30 rounded-xl p-4">
          <p className="text-xs text-slate-400 mb-1">Turbulence Moy.</p>
          <p className="text-2xl font-bold text-orange-400">{s?.avg_turbulence_score ?? "—"}</p>
        </div>
        <div className="bg-slate-900 border border-cyan-700/30 rounded-xl p-4">
          <p className="text-xs text-slate-400 mb-1">Entropie Moy.</p>
          <p className="text-2xl font-bold text-amber-400">{s?.avg_entropy_score ?? "—"}</p>
        </div>
        <div className="bg-slate-900 border border-cyan-700/30 rounded-xl p-4">
          <p className="text-xs text-slate-400 mb-1">Alertes Chaos</p>
          <p className="text-2xl font-bold text-cyan-400">{s?.chaos_signal_count ?? "—"}</p>
        </div>
        <div className="bg-slate-900 border border-cyan-700/30 rounded-xl p-4">
          <p className="text-xs text-slate-400 mb-1">Restructurations Requises</p>
          <p className="text-2xl font-bold text-red-400">{s?.restructuring_required_count ?? "—"}</p>
        </div>
      </div>

      {/* Gauge rings — 4 sub-scores */}
      <div className="bg-slate-900 border border-cyan-700/30 rounded-xl p-5 mb-6">
        <h3 className="text-sm font-semibold text-slate-300 mb-4">
          Scores Moyens de Dynamique Fluide
        </h3>
        <div className="flex flex-wrap justify-around gap-6">
          <GaugeRing pct={s?.avg_turbulence_score  ?? 0} color="#f87171" label="Turbulence"        />
          <GaugeRing pct={s?.avg_entropy_score     ?? 0} color="#f97316" label="Entropie Système"  />
          <GaugeRing pct={s?.avg_flow_score        ?? 0} color="#22d3ee" label="Fluidité Info."    />
          <GaugeRing pct={s?.avg_resilience_score  ?? 0} color="#a78bfa" label="Résilience Bassin" />
        </div>
      </div>

      {/* Distribution bars — 4 */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
        {distributions.map((d) => (
          <div key={d.title} className="bg-slate-900 border border-cyan-700/30 rounded-xl p-4">
            <DistBar title={d.title} counts={d.counts} colors={d.colors} />
          </div>
        ))}
      </div>

      {/* Filters */}
      <div className="mb-4 space-y-3">
        <div className="flex flex-wrap gap-2 items-center">
          <span className="text-xs text-slate-500 mr-1">Risque:</span>
          {RISK_FILTERS.map((f) => (
            <button
              key={f}
              onClick={() => setRiskFilter(f)}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors border ${
                riskFilter === f
                  ? "bg-cyan-700 border-cyan-500 text-white"
                  : "bg-slate-800 border-slate-700 text-slate-400 hover:text-white hover:border-cyan-700"
              }`}
            >
              {f === "all" ? "Tous" : RISK_LABEL[f] ?? f}
              {f !== "all" && s?.risk_counts?.[f] !== undefined && (
                <span className="ml-1 opacity-70">({s.risk_counts[f]})</span>
              )}
            </button>
          ))}
        </div>
        <div className="flex flex-wrap gap-2 items-center">
          <span className="text-xs text-slate-500 mr-1">Pattern:</span>
          {PATTERN_FILTERS.map((f) => (
            <button
              key={f}
              onClick={() => setPatternFilter(f)}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors border ${
                patternFilter === f
                  ? "bg-cyan-700 border-cyan-500 text-white"
                  : "bg-slate-800 border-slate-700 text-slate-400 hover:text-white hover:border-cyan-700"
              }`}
            >
              {f === "all" ? "Tous" : PATTERN_LABEL[f] ?? f}
            </button>
          ))}
        </div>
      </div>

      {/* System cards */}
      {loading ? (
        <div className="flex items-center justify-center h-48">
          <div className="w-8 h-8 border-2 border-cyan-500 border-t-transparent rounded-full animate-spin" />
        </div>
      ) : systems.length === 0 ? (
        <div className="text-center py-20 text-slate-500">
          Aucun système pour ce filtre
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
          {systems.map((system) => (
            <SystemCard key={system.system_id} system={system} onClick={() => setSelected(system)} />
          ))}
        </div>
      )}
    </div>
  );
}
