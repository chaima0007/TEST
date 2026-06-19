"use client";
import { useEffect, useState, useRef } from "react";

// ─── Types ────────────────────────────────────────────────────────────────────

type RiskLevel      = "critical" | "high" | "moderate" | "low";
type MethanePattern = "permafrost_methane_bomb" | "clathrate_destabilization" | "agricultural_methane_crisis" | "arctic_feedback_cascade" | "tundra_methane_inferno" | "none";
type Severity       = "bombe_méthane_imminente" | "crise_méthane_accélérée" | "accumulation_méthane_critique" | "émissions_méthane_surveillées";
type Action         = "intervention_méthane_urgence_planétaire" | "réduction_méthane_accélérée" | "surveillance_méthane_renforcée" | "monitoring_méthane_continu";

interface MceEntity {
  entity_id: string;
  methane_source: string;
  region: string;
  arctic_score: number;
  emission_score: number;
  feedback_score: number;
  response_score: number;
  composite_score: number;
  risk_level: RiskLevel;
  methane_pattern: MethanePattern;
  severity: Severity;
  recommended_action: Action;
  signal: string;
  arctic_permafrost_methane_release_rate: number;
  methane_warming_feedback_loop_intensity: number;
}

interface MceSummary {
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
  avg_estimated_methane_risk_index: number;
  avg_arctic_score: number;
  avg_emission_score: number;
  avg_feedback_score: number;
  avg_response_score: number;
}

// ─── Meta ─────────────────────────────────────────────────────────────────────

const RISK_META: Record<RiskLevel, { label: string; color: string; ring: string; bg: string; badge: string }> = {
  critical: { label: "Critique",  color: "text-red-400",    ring: "#f87171", bg: "bg-red-950/40",    badge: "bg-red-900/60 text-red-300 border-red-700"    },
  high:     { label: "Élevé",     color: "text-orange-400", ring: "#fb923c", bg: "bg-orange-950/40", badge: "bg-orange-900/60 text-orange-300 border-orange-700" },
  moderate: { label: "Modéré",    color: "text-amber-400",  ring: "#fbbf24", bg: "bg-amber-950/40",  badge: "bg-amber-900/60 text-amber-300 border-amber-700"  },
  low:      { label: "Faible",    color: "text-cyan-400",   ring: "#22d3ee", bg: "bg-cyan-950/40",   badge: "bg-cyan-900/60 text-cyan-300 border-cyan-700"     },
};

const PATTERN_LABELS: Record<MethanePattern, string> = {
  permafrost_methane_bomb:   "Bombe Méthane Pergélisol",
  clathrate_destabilization: "Déstabilisation Clathrate",
  agricultural_methane_crisis: "Crise Méthane Agricole",
  arctic_feedback_cascade:   "Cascade Rétroaction Arctique",
  tundra_methane_inferno:    "Enfer Méthane Toundra",
  none:                      "Aucun",
};

const SEV_LABELS: Record<Severity, string> = {
  "bombe_méthane_imminente":       "Bombe Méthane Imminente",
  "crise_méthane_accélérée":       "Crise Méthane Accélérée",
  "accumulation_méthane_critique": "Accumulation Méthane Critique",
  "émissions_méthane_surveillées": "Émissions Méthane Surveillées",
};

const ACTION_LABELS: Record<Action, string> = {
  "intervention_méthane_urgence_planétaire": "Intervention Urgence Planétaire",
  "réduction_méthane_accélérée":             "Réduction Méthane Accélérée",
  "surveillance_méthane_renforcée":          "Surveillance Méthane Renforcée",
  "monitoring_méthane_continu":              "Monitoring Méthane Continu",
};

const RISK_COLORS: Record<string, string> = {
  critical: "#ef4444",
  high:     "#f97316",
  moderate: "#f59e0b",
  low:      "#22d3ee",
};

const PAT_COLORS: Record<string, string> = {
  permafrost_methane_bomb:     "#ef4444",
  clathrate_destabilization:   "#3b82f6",
  agricultural_methane_crisis: "#22c55e",
  arctic_feedback_cascade:     "#a855f7",
  tundra_methane_inferno:      "#f97316",
  none:                        "#22d3ee",
};

const SEV_COLORS: Record<string, string> = {
  "bombe_méthane_imminente":       "#ef4444",
  "crise_méthane_accélérée":       "#f97316",
  "accumulation_méthane_critique": "#f59e0b",
  "émissions_méthane_surveillées": "#22d3ee",
};

const ACT_COLORS: Record<string, string> = {
  "intervention_méthane_urgence_planétaire": "#ef4444",
  "réduction_méthane_accélérée":             "#f97316",
  "surveillance_méthane_renforcée":          "#f59e0b",
  "monitoring_méthane_continu":              "#22d3ee",
};

// ─── GaugeRing ────────────────────────────────────────────────────────────────

function GaugeRing({ value, label, color }: { value: number; label: string; color: string }) {
  const r    = 36;
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
            <span style={{ color: colors[k] || "#94a3b8" }}>■</span>{" "}
            {k.replace(/_/g, " ")} {v}
          </span>
        ))}
      </div>
    </div>
  );
}

// ─── DetailModal ──────────────────────────────────────────────────────────────

function DetailModal({ entity, onClose }: { entity: MceEntity; onClose: () => void }) {
  const [tab, setTab] = useState<"scores" | "signal" | "action">("scores");
  const overlayRef    = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const fn = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", fn);
    return () => window.removeEventListener("keydown", fn);
  }, [onClose]);

  const rm = RISK_META[entity.risk_level];

  return (
    <div
      ref={overlayRef}
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 p-4"
      onClick={(e) => { if (e.target === overlayRef.current) onClose(); }}
    >
      <div className="bg-slate-900 border border-cyan-700/30 rounded-2xl w-full max-w-lg shadow-2xl max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="flex items-center justify-between p-5 border-b border-slate-800">
          <div>
            <div className="flex items-center gap-2 flex-wrap">
              <span className="text-lg font-bold text-white">{entity.entity_id}</span>
              <span className="text-cyan-400 text-xs">{entity.region}</span>
              <span className={`text-xs font-bold px-2 py-0.5 rounded border ${rm.badge}`}>{rm.label}</span>
            </div>
            <p className="text-slate-400 text-sm capitalize mt-0.5">{entity.methane_source.replace(/_/g, " ")}</p>
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
                tab === t
                  ? "text-cyan-400 border-b-2 border-cyan-400"
                  : "text-slate-500 hover:text-slate-300"
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
                {([
                  ["Arctique",    entity.arctic_score,    "#22d3ee"],
                  ["Émissions",   entity.emission_score,  "#f87171"],
                  ["Rétroaction", entity.feedback_score,  "#fb923c"],
                  ["Réponse",     entity.response_score,  "#f59e0b"],
                ] as [string, number, string][]).map(([l, v, c]) => (
                  <div key={l} className="bg-slate-800 rounded-lg p-3">
                    <div className="text-slate-400 text-xs mb-1">{l}</div>
                    <div className="text-white font-bold text-lg">{v.toFixed(1)}</div>
                    <div className="h-1.5 rounded mt-1 bg-slate-700">
                      <div
                        className="h-1.5 rounded"
                        style={{ width: `${Math.min(v, 100)}%`, background: c }}
                      />
                    </div>
                  </div>
                ))}
              </div>
              <div className="bg-slate-800 rounded-lg p-3">
                <div className="text-slate-400 text-xs mb-1">Score Composite Méthane</div>
                <div className="text-white font-bold text-2xl">{entity.composite_score.toFixed(1)}</div>
                <div className="text-xs text-slate-500 mt-0.5">{SEV_LABELS[entity.severity]}</div>
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div className="bg-slate-800 rounded-lg p-3">
                  <div className="text-slate-400 text-xs mb-1">Relâchement Pergélisol</div>
                  <div className="text-cyan-300 font-bold">{(entity.arctic_permafrost_methane_release_rate * 100).toFixed(0)}%</div>
                </div>
                <div className="bg-slate-800 rounded-lg p-3">
                  <div className="text-slate-400 text-xs mb-1">Intensité Rétroaction</div>
                  <div className="text-orange-300 font-bold">{(entity.methane_warming_feedback_loop_intensity * 100).toFixed(0)}%</div>
                </div>
              </div>
            </div>
          )}

          {tab === "signal" && (
            <div className="bg-slate-800 rounded-lg p-4 text-sm text-slate-200 leading-relaxed">
              {entity.signal}
              <div className="mt-3 flex gap-2 flex-wrap">
                <span className={`px-2 py-0.5 rounded text-xs font-medium border ${rm.badge}`}>{rm.label}</span>
                <span className="px-2 py-0.5 rounded text-xs font-medium bg-slate-700 text-slate-300">
                  {PATTERN_LABELS[entity.methane_pattern]}
                </span>
              </div>
            </div>
          )}

          {tab === "action" && (
            <div className="space-y-3 text-sm">
              <div className="bg-slate-800 rounded-lg p-3">
                <div className="text-slate-400 text-xs mb-1">Action Recommandée</div>
                <div className="text-cyan-300 font-medium">{ACTION_LABELS[entity.recommended_action]}</div>
              </div>
              <div className="bg-slate-800 rounded-lg p-3">
                <div className="text-slate-400 text-xs mb-1">Pattern Méthane</div>
                <div className="text-white font-medium">{PATTERN_LABELS[entity.methane_pattern]}</div>
              </div>
              <div className="bg-slate-800 rounded-lg p-3">
                <div className="text-slate-400 text-xs mb-1">Sévérité</div>
                <div className="text-white font-medium">{SEV_LABELS[entity.severity]}</div>
              </div>
              {entity.risk_level === "critical" && (
                <span className="inline-block px-2 py-1 rounded bg-red-900/60 text-red-300 text-xs font-bold border border-red-700">
                  BOMBE MÉTHANE
                </span>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

// ─── EntityCard ───────────────────────────────────────────────────────────────

function EntityCard({ entity, onClick }: { entity: MceEntity; onClick: () => void }) {
  const rm = RISK_META[entity.risk_level];

  return (
    <button
      onClick={onClick}
      className={`w-full text-left rounded-xl border border-slate-800 ${rm.bg} p-4 hover:border-cyan-700/50 transition-colors`}
    >
      <div className="flex items-center justify-between mb-2">
        <span className="font-bold text-white">{entity.entity_id}</span>
        <span className="text-xs text-cyan-400">{entity.region}</span>
      </div>
      <div className="text-xs text-slate-400 mb-2 capitalize">{entity.methane_source.replace(/_/g, " ")}</div>
      <div className="flex gap-1 mb-3 flex-wrap">
        <span className={`px-2 py-0.5 rounded text-xs font-bold border ${rm.badge}`}>{rm.label}</span>
      </div>
      <div className="text-2xl font-black text-white mb-1">{entity.composite_score.toFixed(1)}</div>
      <div className="text-xs text-slate-500 mb-2">{PATTERN_LABELS[entity.methane_pattern]}</div>
      <div className="text-xs text-cyan-400 font-medium mb-2">{SEV_LABELS[entity.severity]}</div>
      <div className="text-xs text-slate-400 leading-snug line-clamp-2">{entity.signal}</div>
    </button>
  );
}

// ─── Page ─────────────────────────────────────────────────────────────────────

export default function MethaneCrisisDashboard() {
  const [data, setData]            = useState<{ entities: MceEntity[]; summary: MceSummary } | null>(null);
  const [riskFilter, setRiskFilter]   = useState<string>("all");
  const [patFilter,  setPatFilter]    = useState<string>("all");
  const [selected,   setSelected]     = useState<MceEntity | null>(null);

  useEffect(() => {
    fetch("/api/methane-crisis-engine")
      .then((r) => r.json())
      .then(setData)
      .catch(console.error);
  }, []);

  if (!data) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center">
        <div className="text-cyan-400 text-lg animate-pulse">Chargement Crise Méthane…</div>
      </div>
    );
  }

  const { entities, summary } = data;

  const filtered = entities.filter(
    (e) =>
      (riskFilter === "all" || e.risk_level      === riskFilter) &&
      (patFilter  === "all" || e.methane_pattern === patFilter),
  );

  const kpis = [
    { label: "Total Sources",     value: String(summary.total_entities),                           color: "text-cyan-400"   },
    { label: "Bombe Méthane",     value: String(summary.critical_count),                           color: "text-red-400"    },
    { label: "Crise Accélérée",   value: String(summary.high_count),                               color: "text-orange-400" },
    { label: "Composite Moyen",   value: summary.avg_composite.toFixed(1),                         color: "text-cyan-400"   },
    { label: "Index Risque Méthane", value: `${summary.avg_estimated_methane_risk_index.toFixed(2)}/10`, color: "text-teal-400" },
    { label: "Arctique Moyen",    value: Math.round(summary.avg_arctic_score ?? 0).toString(),     color: "text-orange-400" },
  ];

  const dists = [
    { title: "Risque",    counts: summary.risk_distribution,    colors: RISK_COLORS },
    { title: "Patterns",  counts: summary.pattern_distribution, colors: PAT_COLORS  },
    { title: "Sévérité",  counts: summary.severity_distribution, colors: SEV_COLORS },
    { title: "Actions",   counts: summary.action_distribution,  colors: ACT_COLORS  },
  ] as Array<{ title: string; counts: Record<string, number>; colors: Record<string, string> }>;

  const risks:    RiskLevel[]      = ["critical", "high", "moderate", "low"];
  const patterns: MethanePattern[] = ["permafrost_methane_bomb", "clathrate_destabilization", "agricultural_methane_crisis", "arctic_feedback_cascade", "tundra_methane_inferno", "none"];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {selected && <DetailModal entity={selected} onClose={() => setSelected(null)} />}

      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-cyan-400">
          Crise Méthane &amp; Bombe Méthane Arctique — Module 345
        </h1>
        <p className="text-slate-400 text-sm mt-1">
          Arctique · Émissions · Rétroaction · Réponse — surveillance des bombes méthane planétaires
        </p>
      </div>

      {/* KPI strip */}
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
        {kpis.map((k) => (
          <div key={k.label} className="bg-slate-900 border border-cyan-700/30 rounded-xl p-4 text-center">
            <div className={`text-xl font-bold ${k.color}`}>{k.value}</div>
            <div className="text-xs text-slate-500 mt-0.5">{k.label}</div>
          </div>
        ))}
      </div>

      {/* GaugeRings */}
      <div className="bg-slate-900 border border-cyan-700/30 rounded-xl p-5">
        <p className="text-xs text-slate-500 mb-4 font-semibold uppercase tracking-wide">
          Scores Moyens par Dimension
        </p>
        <div className="grid grid-cols-4 gap-4">
          <GaugeRing value={summary.avg_arctic_score   ?? 0} label="Arctique"    color="#22d3ee" />
          <GaugeRing value={summary.avg_emission_score ?? 0} label="Émissions"   color="#f87171" />
          <GaugeRing value={summary.avg_feedback_score ?? 0} label="Rétroaction" color="#fb923c" />
          <GaugeRing value={summary.avg_response_score ?? 0} label="Réponse"     color="#f59e0b" />
        </div>
      </div>

      {/* DistBars */}
      <div className="bg-slate-900 border border-cyan-700/30 rounded-xl p-5 grid grid-cols-1 md:grid-cols-2 gap-5">
        {dists.map((d) => (
          <DistBar key={d.title} {...d} />
        ))}
      </div>

      {/* Risk filters */}
      <div className="flex flex-col gap-2">
        <div className="flex flex-wrap gap-2">
          {["all", ...risks].map((r) => (
            <button
              key={r}
              onClick={() => setRiskFilter(r)}
              className={`px-3 py-1.5 rounded-full text-xs font-semibold border transition-colors ${
                riskFilter === r
                  ? "bg-cyan-700 border-cyan-600 text-white"
                  : "bg-slate-900 border-slate-700 text-slate-400 hover:text-white hover:border-cyan-600"
              }`}
            >
              {r === "all" ? "Tous risques" : RISK_META[r as RiskLevel].label}
            </button>
          ))}
        </div>
        {/* Pattern filters */}
        <div className="flex flex-wrap gap-2">
          {["all", ...patterns].map((p) => (
            <button
              key={p}
              onClick={() => setPatFilter(p)}
              className={`px-3 py-1.5 rounded-full text-xs font-semibold border transition-colors ${
                patFilter === p
                  ? "bg-teal-700 border-teal-600 text-white"
                  : "bg-slate-900 border-slate-700 text-slate-400 hover:text-white hover:border-teal-600"
              }`}
            >
              {p === "all" ? "Tous patterns" : PATTERN_LABELS[p as MethanePattern]}
            </button>
          ))}
        </div>
      </div>

      {/* Entity grid */}
      {filtered.length === 0 ? (
        <div className="text-center text-slate-500 py-16">Aucune source pour ces filtres.</div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          {filtered.map((e) => (
            <EntityCard key={e.entity_id} entity={e} onClick={() => setSelected(e)} />
          ))}
        </div>
      )}
    </div>
  );
}
