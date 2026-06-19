"use client";

import { useState, useEffect, useRef } from "react";

// ─── Types ────────────────────────────────────────────────────────────────────

interface EntityData {
  entity_id: string;
  decision_system_type: string;
  region: string;
  bias_risk: string;
  bias_pattern: string;
  bias_severity: string;
  recommended_action: string;
  reasoning_score: number;
  heuristic_score: number;
  group_score: number;
  meta_score: number;
  bias_composite: number;
  is_bias_crisis: boolean;
  requires_bias_intervention: boolean;
  bias_signal: string;
}

interface Summary {
  total: number;
  risk_counts: Record<string, number>;
  pattern_counts: Record<string, number>;
  severity_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_bias_composite: number;
  bias_crisis_count: number;
  bias_intervention_count: number;
  avg_reasoning_score: number;
  avg_heuristic_score: number;
  avg_group_score: number;
  avg_meta_score: number;
  avg_estimated_cognitive_vulnerability_index: number;
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
  cognitive_clarity:  "bg-emerald-500/15 text-emerald-300",
  bias_accumulation:  "bg-amber-500/15 text-amber-300",
  high_bias_risk:     "bg-orange-500/15 text-orange-300",
  cognitive_emergency:"bg-rose-500/15 text-rose-300",
};
const SEVERITY_LABEL: Record<string, string> = {
  cognitive_clarity:  "Clarté Cognitive",
  bias_accumulation:  "Accumulation Biais",
  high_bias_risk:     "Risque Biais Élevé",
  cognitive_emergency:"Urgence Cognitive",
};

const ACTION_BG: Record<string, string> = {
  no_action:                     "bg-emerald-500/15 text-emerald-300",
  bias_monitoring:               "bg-sky-500/15 text-sky-300",
  systematic_debiasing:          "bg-amber-500/15 text-amber-300",
  red_team_intervention:         "bg-orange-500/15 text-orange-300",
  cognitive_emergency_debiasing: "bg-rose-500/15 text-rose-300",
};
const ACTION_LABEL: Record<string, string> = {
  no_action:                     "Aucune Action",
  bias_monitoring:               "Surveillance Biais",
  systematic_debiasing:          "Débiaisage Systématique",
  red_team_intervention:         "Intervention Red Team",
  cognitive_emergency_debiasing: "Débiaisage d'Urgence",
};

const PATTERN_LABEL: Record<string, string> = {
  none:                  "Aucun",
  dunning_kruger_crisis: "Crise Dunning-Kruger",
  groupthink_capture:    "Capture Groupthink",
  black_swan_blindness:  "Cécité Cygne Noir",
  narrative_trap:        "Piège Narratif",
  metacognitive_collapse:"Effondrement Métacognitif",
};

const RISK_FILTERS    = ["all", "critical", "high", "moderate", "low"] as const;
const PATTERN_FILTERS = [
  "all",
  "dunning_kruger_crisis",
  "groupthink_capture",
  "black_swan_blindness",
  "narrative_trap",
  "metacognitive_collapse",
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

function DetailModal({ entity, onClose }: { entity: EntityData; onClose: () => void }) {
  const [tab, setTab] = useState<"scores" | "signal" | "action">("scores");
  const overlayRef    = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handler = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [onClose]);

  const riskColor = RISK_COLOR[entity.bias_risk] ?? "#fbbf24";

  return (
    <div
      ref={overlayRef}
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4"
      onClick={(e) => { if (e.target === overlayRef.current) onClose(); }}
    >
      <div className="bg-slate-900 border border-indigo-700/30 rounded-xl shadow-2xl w-full max-w-lg">
        {/* Header */}
        <div className="flex items-start justify-between p-5 border-b border-slate-800">
          <div>
            <div className="flex items-center gap-2 mb-1 flex-wrap">
              <span
                className={`text-xs px-2 py-0.5 rounded-full border font-medium ${RISK_BG[entity.bias_risk] ?? ""}`}
              >
                {RISK_LABEL[entity.bias_risk] ?? entity.bias_risk}
              </span>
              <span
                className={`text-xs px-2 py-0.5 rounded-full font-medium ${SEVERITY_BG[entity.bias_severity] ?? ""}`}
              >
                {SEVERITY_LABEL[entity.bias_severity] ?? entity.bias_severity}
              </span>
            </div>
            <h2 className="text-white font-bold text-lg">{entity.entity_id}</h2>
            <p className="text-slate-400 text-sm">
              {entity.decision_system_type} · {entity.region} · Composite:{" "}
              <span style={{ color: riskColor }}>{entity.bias_composite}</span>
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
                  ? "text-amber-400 border-b-2 border-amber-500 bg-slate-800/40"
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
              <ScoreBar score={entity.reasoning_score}  label="Raisonnement & Biais (30%)" />
              <ScoreBar score={entity.heuristic_score}  label="Heuristiques Cognitives (25%)" />
              <ScoreBar score={entity.group_score}      label="Dynamiques de Groupe (25%)" />
              <ScoreBar score={entity.meta_score}       label="Métacognition (20%)" />
              <div className="pt-2 border-t border-slate-800">
                <div className="flex justify-between items-center">
                  <span className="text-sm text-slate-400">Composite Biais</span>
                  <span className="text-lg font-bold" style={{ color: riskColor }}>
                    {entity.bias_composite}
                  </span>
                </div>
                <p className="text-xs text-slate-500 mt-1">
                  Score composite vulnérabilité cognitive (0–100)
                </p>
              </div>
            </div>
          )}

          {tab === "signal" && (
            <>
              <div className="flex items-center justify-center py-2">
                <GaugeRing
                  pct={entity.bias_composite}
                  color={riskColor}
                  label="Composite"
                  size={110}
                />
              </div>
              <div className="bg-slate-800/50 rounded-lg p-3">
                <p className="text-xs text-slate-400 mb-1">Signal Cognitif</p>
                <p className="text-sm text-white">{entity.bias_signal}</p>
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div className="bg-slate-800/50 rounded-lg p-3">
                  <p className="text-xs text-slate-400">Crise Cognitive</p>
                  <p className={`text-lg font-bold ${entity.is_bias_crisis ? "text-rose-400" : "text-emerald-400"}`}>
                    {entity.is_bias_crisis ? "Oui" : "Non"}
                  </p>
                </div>
                <div className="bg-slate-800/50 rounded-lg p-3">
                  <p className="text-xs text-slate-400">Intervention Requise</p>
                  <p className={`text-lg font-bold ${entity.requires_bias_intervention ? "text-orange-400" : "text-emerald-400"}`}>
                    {entity.requires_bias_intervention ? "Oui" : "Non"}
                  </p>
                </div>
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div className="bg-slate-800/50 rounded-lg p-3">
                  <p className="text-xs text-slate-400">Patron Cognitif</p>
                  <p className="text-sm font-medium text-slate-200">
                    {PATTERN_LABEL[entity.bias_pattern] ?? entity.bias_pattern}
                  </p>
                </div>
                <div className="bg-slate-800/50 rounded-lg p-3">
                  <p className="text-xs text-slate-400">Sévérité</p>
                  <p className="text-sm font-medium text-slate-200">
                    {SEVERITY_LABEL[entity.bias_severity] ?? entity.bias_severity}
                  </p>
                </div>
              </div>
            </>
          )}

          {tab === "action" && (
            <div className="space-y-4">
              <div className="bg-slate-800/50 rounded-lg p-4">
                <p className="text-xs text-slate-400 mb-2">Action Recommandée</p>
                <span
                  className={`text-sm px-3 py-1.5 rounded-lg font-medium ${ACTION_BG[entity.recommended_action] ?? ""}`}
                >
                  {ACTION_LABEL[entity.recommended_action] ?? entity.recommended_action}
                </span>
              </div>
              <div className="space-y-2">
                <div className="flex justify-between p-2 rounded bg-slate-800/40">
                  <span className="text-xs text-slate-400">Sévérité</span>
                  <span className="text-xs text-slate-200">
                    {SEVERITY_LABEL[entity.bias_severity] ?? entity.bias_severity}
                  </span>
                </div>
                <div className="flex justify-between p-2 rounded bg-slate-800/40">
                  <span className="text-xs text-slate-400">Patron Cognitif</span>
                  <span className="text-xs text-slate-200">
                    {PATTERN_LABEL[entity.bias_pattern] ?? entity.bias_pattern}
                  </span>
                </div>
                <div className="flex justify-between p-2 rounded bg-slate-800/40">
                  <span className="text-xs text-slate-400">Crise Cognitive</span>
                  <span className={`text-xs font-medium ${entity.is_bias_crisis ? "text-rose-400" : "text-emerald-400"}`}>
                    {entity.is_bias_crisis ? "Oui" : "Non"}
                  </span>
                </div>
                <div className="flex justify-between p-2 rounded bg-slate-800/40">
                  <span className="text-xs text-slate-400">Intervention Requise</span>
                  <span className={`text-xs font-medium ${entity.requires_bias_intervention ? "text-orange-400" : "text-emerald-400"}`}>
                    {entity.requires_bias_intervention ? "Requise" : "Non requise"}
                  </span>
                </div>
                <div className="flex justify-between p-2 rounded bg-slate-800/40">
                  <span className="text-xs text-slate-400">Raisonnement</span>
                  <span className="text-xs text-amber-400 font-medium">
                    {entity.reasoning_score.toFixed(1)}
                  </span>
                </div>
                <div className="flex justify-between p-2 rounded bg-slate-800/40">
                  <span className="text-xs text-slate-400">Métacognition</span>
                  <span className="text-xs text-indigo-400 font-medium">
                    {entity.meta_score.toFixed(1)}
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

// ─── EntityCard ───────────────────────────────────────────────────────────────

function EntityCard({ entity, onClick }: { entity: EntityData; onClick: () => void }) {
  const riskColor = RISK_COLOR[entity.bias_risk] ?? "#fbbf24";

  return (
    <div
      onClick={onClick}
      className="bg-slate-900 border border-slate-800 rounded-xl p-4 cursor-pointer hover:border-indigo-700/30 transition-all hover:bg-slate-800/60"
    >
      <div className="flex items-start justify-between mb-3">
        <div className="flex-1 min-w-0 pr-2">
          <div className="flex items-center gap-2 mb-1 flex-wrap">
            <span
              className={`text-xs px-2 py-0.5 rounded-full border font-medium ${RISK_BG[entity.bias_risk] ?? ""}`}
            >
              {RISK_LABEL[entity.bias_risk] ?? entity.bias_risk}
            </span>
            {entity.is_bias_crisis && (
              <span className="text-xs px-2 py-0.5 rounded-full bg-rose-500/20 border border-rose-500/30 text-rose-300 font-medium">
                CRISE
              </span>
            )}
          </div>
          <h3 className="text-white font-semibold text-sm">{entity.entity_id}</h3>
          <p className="text-slate-400 text-xs">{entity.decision_system_type} · {entity.region}</p>
        </div>
        <div className="flex-shrink-0">
          <GaugeRing pct={entity.bias_composite} color={riskColor} label="" size={72} />
        </div>
      </div>

      <div className="space-y-1.5 mb-3">
        <ScoreBar score={entity.reasoning_score}  label="Raisonnement" />
        <ScoreBar score={entity.heuristic_score}  label="Heuristiques" />
        <ScoreBar score={entity.group_score}      label="Groupe" />
        <ScoreBar score={entity.meta_score}       label="Métacognition" />
      </div>

      <div className="border-t border-slate-800 pt-2 flex items-center justify-between">
        <span className={`text-xs px-2 py-0.5 rounded font-medium ${ACTION_BG[entity.recommended_action] ?? ""}`}>
          {ACTION_LABEL[entity.recommended_action] ?? entity.recommended_action}
        </span>
        <span className="text-xs text-amber-400 font-medium">
          {entity.bias_composite.toFixed(1)}
        </span>
      </div>
      <div className="flex items-center gap-1.5 mt-2">
        <span
          className={`text-xs px-1.5 py-0.5 rounded font-medium ${SEVERITY_BG[entity.bias_severity] ?? ""}`}
        >
          {SEVERITY_LABEL[entity.bias_severity] ?? entity.bias_severity}
        </span>
        <span className="text-xs text-slate-500 truncate">
          {PATTERN_LABEL[entity.bias_pattern] ?? entity.bias_pattern}
        </span>
      </div>
      <p className="text-xs text-slate-500 mt-1.5 truncate">{entity.bias_signal}</p>
    </div>
  );
}

// ─── Page ─────────────────────────────────────────────────────────────────────

export default function MetacognitiveBiasEnginePage() {
  const [data, setData]                   = useState<{ entities: EntityData[]; summary: Summary } | null>(null);
  const [loading, setLoading]             = useState(true);
  const [riskFilter, setRiskFilter]       = useState<RiskFilter>("all");
  const [patternFilter, setPatternFilter] = useState<PatternFilter>("all");
  const [selected, setSelected]           = useState<EntityData | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      const params = new URLSearchParams();
      if (riskFilter    !== "all") params.set("risk",    riskFilter);
      if (patternFilter !== "all") params.set("pattern", patternFilter);
      const res  = await fetch(`/api/metacognitive-bias-engine?${params}`);
      const json = await res.json();
      setData(json);
      setLoading(false);
    };
    fetchData();
  }, [riskFilter, patternFilter]);

  const s        = data?.summary;
  const entities = data?.entities ?? [];

  // ── distribution color maps ──────────────────────────────────────────────

  const riskColors: Record<string, string> = {
    low:      "#34d399",
    moderate: "#fbbf24",
    high:     "#f97316",
    critical: "#f87171",
  };
  const patternColors: Record<string, string> = {
    none:                  "#64748b",
    dunning_kruger_crisis: "#f87171",
    groupthink_capture:    "#a78bfa",
    black_swan_blindness:  "#f97316",
    narrative_trap:        "#ec4899",
    metacognitive_collapse:"#ef4444",
  };
  const severityColors: Record<string, string> = {
    cognitive_clarity:  "#34d399",
    bias_accumulation:  "#fbbf24",
    high_bias_risk:     "#f97316",
    cognitive_emergency:"#f87171",
  };
  const actionColors: Record<string, string> = {
    no_action:                     "#34d399",
    bias_monitoring:               "#38bdf8",
    systematic_debiasing:          "#fbbf24",
    red_team_intervention:         "#f97316",
    cognitive_emergency_debiasing: "#f87171",
  };

  const distributions: Array<{ title: string; counts: Record<string, number>; colors: Record<string, string> }> = [
    { title: "Risque Cognitif",        counts: s?.risk_counts     ?? {}, colors: riskColors     },
    { title: "Patron de Biais",        counts: s?.pattern_counts  ?? {}, colors: patternColors  },
    { title: "Sévérité Métacognitive", counts: s?.severity_counts ?? {}, colors: severityColors },
    { title: "Action Recommandée",     counts: s?.action_counts   ?? {}, colors: actionColors   },
  ];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
      {selected && <DetailModal entity={selected} onClose={() => setSelected(null)} />}

      {/* Header */}
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-amber-400">
          Biais Métacognitifs &amp; Vulnérabilité Cognitive — Module 321
        </h1>
        <p className="text-slate-400 text-sm mt-1">
          Raisonnement · Heuristiques · Groupe · Métacognition — détection et quantification des angles morts cognitifs
        </p>
      </div>

      {/* KPI strip — 6 cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 xl:grid-cols-6 gap-4 mb-6">
        <div className="bg-slate-900 border border-indigo-700/30 rounded-xl p-4">
          <p className="text-xs text-slate-400 mb-1">Total Systèmes</p>
          <p className="text-2xl font-bold text-white">{s?.total ?? "—"}</p>
        </div>
        <div className="bg-slate-900 border border-indigo-700/30 rounded-xl p-4">
          <p className="text-xs text-slate-400 mb-1">En Crise Cognitive</p>
          <p className="text-2xl font-bold text-rose-400">{s?.bias_crisis_count ?? "—"}</p>
        </div>
        <div className="bg-slate-900 border border-indigo-700/30 rounded-xl p-4">
          <p className="text-xs text-slate-400 mb-1">Requiert Intervention</p>
          <p className="text-2xl font-bold text-orange-400">{s?.bias_intervention_count ?? "—"}</p>
        </div>
        <div className="bg-slate-900 border border-indigo-700/30 rounded-xl p-4">
          <p className="text-xs text-slate-400 mb-1">Composite Moyen</p>
          <p className="text-2xl font-bold text-amber-400">{s?.avg_bias_composite ?? "—"}</p>
        </div>
        <div className="bg-slate-900 border border-indigo-700/30 rounded-xl p-4">
          <p className="text-xs text-slate-400 mb-1">Index Vulnérabilité</p>
          <p className="text-2xl font-bold text-indigo-400">
            {s?.avg_estimated_cognitive_vulnerability_index ?? "—"}
          </p>
        </div>
        <div className="bg-slate-900 border border-indigo-700/30 rounded-xl p-4">
          <p className="text-xs text-slate-400 mb-1">Raisonnement Moyen</p>
          <p className="text-2xl font-bold text-amber-300">{s?.avg_reasoning_score ?? "—"}</p>
        </div>
      </div>

      {/* Gauge rings — 4 sub-scores */}
      <div className="bg-slate-900 border border-indigo-700/30 rounded-xl p-5 mb-6">
        <h3 className="text-sm font-semibold text-slate-300 mb-4">
          Scores Moyens de Vulnérabilité Cognitive
        </h3>
        <div className="flex flex-wrap justify-around gap-6">
          <GaugeRing pct={s?.avg_reasoning_score  ?? 0} color="#fbbf24" label="Raisonnement"  />
          <GaugeRing pct={s?.avg_heuristic_score  ?? 0} color="#818cf8" label="Heuristiques"  />
          <GaugeRing pct={s?.avg_group_score      ?? 0} color="#a78bfa" label="Groupe"         />
          <GaugeRing pct={s?.avg_meta_score       ?? 0} color="#f87171" label="Métacognition"  />
        </div>
      </div>

      {/* Distribution bars — 4 */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
        {distributions.map((d) => (
          <div key={d.title} className="bg-slate-900 border border-indigo-700/30 rounded-xl p-4">
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
                  ? "bg-amber-700 border-amber-500 text-white"
                  : "bg-slate-800 border-slate-700 text-slate-400 hover:text-white hover:border-amber-700"
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
          <span className="text-xs text-slate-500 mr-1">Patron:</span>
          {PATTERN_FILTERS.map((f) => (
            <button
              key={f}
              onClick={() => setPatternFilter(f)}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors border ${
                patternFilter === f
                  ? "bg-indigo-700 border-indigo-500 text-white"
                  : "bg-slate-800 border-slate-700 text-slate-400 hover:text-white hover:border-indigo-700"
              }`}
            >
              {f === "all" ? "Tous" : PATTERN_LABEL[f] ?? f}
            </button>
          ))}
        </div>
      </div>

      {/* Entity cards */}
      {loading ? (
        <div className="flex items-center justify-center h-48">
          <div className="w-8 h-8 border-2 border-amber-500 border-t-transparent rounded-full animate-spin" />
        </div>
      ) : entities.length === 0 ? (
        <div className="text-center py-20 text-slate-500">
          Aucun système pour ce filtre
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
          {entities.map((entity) => (
            <EntityCard key={entity.entity_id} entity={entity} onClick={() => setSelected(entity)} />
          ))}
        </div>
      )}
    </div>
  );
}
