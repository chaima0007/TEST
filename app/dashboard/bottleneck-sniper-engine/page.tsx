"use client";

import { useEffect, useState } from "react";

// ── types ─────────────────────────────────────────────────────────────────────

interface ConstraintEntity {
  entity_id: string;
  region: string;
  system_type: string;
  constraint_risk: string;
  constraint_pattern: string;
  constraint_severity: string;
  recommended_action: string;
  flow_score: number;
  constraint_score: number;
  system_score: number;
  resilience_score: number;
  constraint_composite: number;
  is_constraint_crisis: boolean;
  requires_constraint_intervention: boolean;
  constraint_signal: string;
}

interface Summary {
  total_entities: number;
  critical_count: number;
  high_count: number;
  moderate_count: number;
  low_count: number;
  crisis_entities: number;
  intervention_required: number;
  dominant_pattern: string;
  risk_counts: Record<string, number>;
  pattern_counts: Record<string, number>;
  severity_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_flow_score: number;
  avg_constraint_score: number;
  avg_system_score: number;
  avg_resilience_score: number;
  avg_constraint_composite: number;
  avg_estimated_constraint_index: number;
}

// ── color maps ────────────────────────────────────────────────────────────────

const RISK_COLOR: Record<string, string> = {
  critical: "text-red-400",
  high:     "text-orange-400",
  moderate: "text-yellow-400",
  low:      "text-slate-400",
};

const RISK_BG: Record<string, string> = {
  critical: "bg-red-500/20 border-red-500/40",
  high:     "bg-orange-500/20 border-orange-500/40",
  moderate: "bg-yellow-500/20 border-yellow-500/40",
  low:      "bg-slate-500/20 border-slate-500/40",
};

const RISK_BAR: Record<string, string> = {
  critical: "bg-red-500",
  high:     "bg-orange-500",
  moderate: "bg-yellow-500",
  low:      "bg-slate-500",
};

const SEVERITY_COLOR: Record<string, string> = {
  system_halt:         "text-red-400",
  critical_constraint: "text-orange-400",
  constraint_building: "text-yellow-400",
  flow_optimal:        "text-slate-400",
};

const PATTERN_BAR: Record<string, string> = {
  critical_path_failure:       "bg-red-600",
  policy_constraint_dominance: "bg-orange-600",
  market_constraint_crisis:    "bg-rose-500",
  wip_catastrophe:             "bg-orange-500",
  cascade_starvation:          "bg-red-500",
  none:                        "bg-slate-600",
};

const SEV_BAR: Record<string, string> = {
  system_halt:         "bg-red-600",
  critical_constraint: "bg-orange-500",
  constraint_building: "bg-yellow-500",
  flow_optimal:        "bg-slate-500",
};

const ACTION_BAR: Record<string, string> = {
  emergency_constraint_bypass:   "bg-red-500",
  policy_redesign:               "bg-orange-600",
  constraint_exploitation_program: "bg-orange-400",
  bottleneck_monitoring:         "bg-yellow-500",
  no_action:                     "bg-slate-600",
};

function fmt(s: string) {
  return s.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
}

function ringColor(comp: number): string {
  if (comp >= 60) return "#f87171";
  if (comp >= 40) return "#fb923c";
  if (comp >= 20) return "#facc15";
  return "#64748b";
}

// ── GaugeRing ─────────────────────────────────────────────────────────────────

function GaugeRing({ score, label, color }: { score: number; label: string; color: string }) {
  const r = 36, circ = 2 * Math.PI * r;
  const fill = (Math.min(score, 100) / 100) * circ;
  return (
    <div className="flex flex-col items-center gap-2">
      <svg width={88} height={88} viewBox="0 0 88 88">
        <circle cx={44} cy={44} r={r} fill="none" stroke="#1e293b" strokeWidth={8} />
        <circle
          cx={44} cy={44} r={r} fill="none"
          stroke={color} strokeWidth={8}
          strokeDasharray={`${fill} ${circ}`}
          strokeLinecap="round"
          transform="rotate(-90 44 44)"
        />
        <text x={44} y={49} textAnchor="middle" fill="white" fontSize={14} fontWeight="bold">
          {Math.round(score)}
        </text>
      </svg>
      <span className="text-xs text-slate-400 text-center leading-tight">{label}</span>
    </div>
  );
}

// ── DistBar ───────────────────────────────────────────────────────────────────

function DistBar({ title, counts, colors }: { title: string; counts: Record<string, number>; colors: Record<string, string> }) {
  const total = Object.values(counts).reduce((a, b) => a + b, 0) || 1;
  return (
    <div className="bg-slate-900 border border-orange-700/30 rounded-xl p-4">
      <div className="text-xs text-slate-400 mb-2">{title}</div>
      <div className="flex gap-1 h-3 rounded-full overflow-hidden">
        {Object.entries(counts).map(([k, v]) => (
          <div
            key={k}
            className={colors[k] ?? "bg-slate-600"}
            style={{ width: `${(v / total) * 100}%` }}
            title={`${k}: ${v}`}
          />
        ))}
      </div>
      <div className="flex flex-wrap gap-2 mt-2 text-xs text-slate-500">
        {Object.entries(counts).map(([k, v]) => (
          <span key={k}>{k.replace(/_/g, " ")}: {v}</span>
        ))}
      </div>
    </div>
  );
}

// ── ScoreBar ──────────────────────────────────────────────────────────────────

function ScoreBar({ label, value, color }: { label: string; value: number; color: string }) {
  return (
    <div>
      <div className="flex justify-between text-xs text-slate-400 mb-1">
        <span>{label}</span><span>{value.toFixed(2)}</span>
      </div>
      <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
        <div className={`h-full rounded-full ${color}`} style={{ width: `${value}%` }} />
      </div>
    </div>
  );
}

// ── DetailModal ───────────────────────────────────────────────────────────────

function DetailModal({ entity, onClose }: { entity: ConstraintEntity; onClose: () => void }) {
  const [tab, setTab] = useState<0 | 1 | 2>(0);

  useEffect(() => {
    const esc = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", esc);
    return () => window.removeEventListener("keydown", esc);
  }, [onClose]);

  const comp = entity.constraint_composite;
  const rc   = ringColor(comp);

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4"
      onClick={onClose}
    >
      <div
        className="bg-slate-900 border border-orange-700/30 rounded-2xl w-full max-w-lg shadow-2xl"
        onClick={(e) => e.stopPropagation()}
      >
        {/* header */}
        <div className="flex items-center gap-4 p-5 border-b border-slate-800">
          <div className="relative flex-shrink-0">
            <GaugeRing score={comp} label="" color={rc} />
            <span className="absolute inset-0 flex items-center justify-center text-sm font-bold text-slate-200 pointer-events-none">
              {comp.toFixed(0)}
            </span>
          </div>
          <div className="flex-1 min-w-0">
            <h2 className="text-white font-bold text-lg truncate">{entity.entity_id}</h2>
            <p className="text-slate-400 text-sm">{entity.system_type.replace(/_/g, " ")} · {entity.region}</p>
            <div className="flex gap-2 mt-1 flex-wrap">
              <span className={`text-xs px-2 py-0.5 rounded-full border ${RISK_BG[entity.constraint_risk]}`}>
                {entity.constraint_risk}
              </span>
              <span className={`text-xs font-medium ${SEVERITY_COLOR[entity.constraint_severity] ?? "text-slate-400"}`}>
                {entity.constraint_severity.replace(/_/g, " ")}
              </span>
            </div>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl shrink-0">✕</button>
        </div>

        {/* tabs */}
        <div className="flex border-b border-slate-800">
          {(["Scores", "Patterns & Signaux", "Actions"] as const).map((t, i) => (
            <button
              key={t}
              onClick={() => setTab(i as 0 | 1 | 2)}
              className={`flex-1 py-2.5 text-xs font-medium transition-colors ${
                tab === i ? "text-red-400 border-b-2 border-red-400" : "text-slate-500 hover:text-slate-300"
              }`}
            >
              {t}
            </button>
          ))}
        </div>

        <div className="p-5 space-y-3 max-h-[60vh] overflow-y-auto">
          {/* Tab 0 — Scores */}
          {tab === 0 && (
            <div className="space-y-3">
              <ScoreBar label="Score Flux"        value={entity.flow_score}        color="bg-red-500" />
              <ScoreBar label="Score Contrainte"  value={entity.constraint_score}  color="bg-orange-500" />
              <ScoreBar label="Score Système"     value={entity.system_score}      color="bg-red-400" />
              <ScoreBar label="Score Résilience"  value={entity.resilience_score}  color="bg-orange-400" />
              <div className="pt-2 border-t border-slate-800">
                <ScoreBar label="Composite Contrainte" value={entity.constraint_composite} color="bg-rose-600" />
              </div>
            </div>
          )}

          {/* Tab 1 — Patterns & Signals */}
          {tab === 1 && (
            <>
              <div className="grid grid-cols-2 gap-3">
                {[
                  ["Région",           entity.region],
                  ["Système",          entity.system_type.replace(/_/g, " ")],
                  ["Pattern",          entity.constraint_pattern.replace(/_/g, " ")],
                  ["Sévérité",         entity.constraint_severity.replace(/_/g, " ")],
                  ["En Crise",         entity.is_constraint_crisis ? "Oui" : "Non"],
                  ["Intervention",     entity.requires_constraint_intervention ? "Oui" : "Non"],
                ].map(([label, value]) => (
                  <div key={label} className="bg-slate-800/60 rounded-lg p-3">
                    <div className="text-xs text-slate-400">{label}</div>
                    <div className="text-white font-semibold mt-0.5 text-sm">{value}</div>
                  </div>
                ))}
              </div>
              <div className="bg-slate-800/60 rounded-lg p-3">
                <div className="text-xs text-slate-400 mb-1">Signal de Contrainte</div>
                <div className="text-orange-300 text-sm leading-relaxed">{entity.constraint_signal}</div>
              </div>
            </>
          )}

          {/* Tab 2 — Actions */}
          {tab === 2 && (
            <div className="space-y-3">
              <div className="bg-red-500/10 border border-red-500/30 rounded-xl p-4">
                <div className="text-xs text-red-400 uppercase tracking-wide mb-1">Action Recommandée</div>
                <div className="text-white font-bold text-lg">
                  {entity.recommended_action.replace(/_/g, " ")}
                </div>
              </div>
              {entity.is_constraint_crisis && (
                <div className="bg-red-500/10 border border-red-500/30 rounded-xl p-3 text-sm text-red-300">
                  Crise de contrainte active — déclencher le protocole d&apos;urgence immédiatement
                </div>
              )}
              {entity.requires_constraint_intervention && !entity.is_constraint_crisis && (
                <div className="bg-orange-500/10 border border-orange-500/30 rounded-xl p-3 text-sm text-orange-300">
                  Intervention contrainte requise — planifier l&apos;action dans les 48h
                </div>
              )}
              {!entity.requires_constraint_intervention && (
                <div className="bg-slate-800/60 rounded-xl p-3 text-sm text-slate-400">
                  Aucune intervention immédiate — surveillance continue recommandée
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

// ── EntityCard ────────────────────────────────────────────────────────────────

function EntityCard({ entity, onClick }: { entity: ConstraintEntity; onClick: () => void }) {
  const comp = entity.constraint_composite;
  const rc   = ringColor(comp);

  return (
    <div
      onClick={onClick}
      className="bg-slate-900 border border-slate-800 rounded-xl p-4 cursor-pointer hover:border-orange-700/40 hover:bg-slate-800/60 transition-all"
    >
      <div className="flex items-center gap-3">
        <div className="relative flex-shrink-0">
          <GaugeRing score={comp} label="" color={rc} />
          <span className="absolute inset-0 flex items-center justify-center text-xs font-bold text-slate-200 pointer-events-none">
            {comp.toFixed(0)}
          </span>
        </div>
        <div className="flex-1 min-w-0">
          <div className="text-white font-semibold truncate">{entity.entity_id}</div>
          <div className="text-slate-400 text-xs">{entity.system_type.replace(/_/g, " ")} · {entity.region}</div>
          <div className="flex gap-2 mt-1 flex-wrap">
            <span className={`text-xs px-2 py-0.5 rounded-full border ${RISK_BG[entity.constraint_risk]}`}>
              {entity.constraint_risk}
            </span>
          </div>
        </div>
        <div className="text-right shrink-0">
          <div className={`text-sm font-bold ${SEVERITY_COLOR[entity.constraint_severity] ?? "text-slate-400"}`}>
            {entity.constraint_severity.replace(/_/g, " ")}
          </div>
        </div>
      </div>

      {/* badges */}
      <div className="flex gap-2 mt-3">
        {entity.is_constraint_crisis && (
          <span className="px-2 py-0.5 text-xs rounded-full bg-red-500/20 text-red-400 border border-red-500/30">CRISE</span>
        )}
        {entity.requires_constraint_intervention && (
          <span className="px-2 py-0.5 text-xs rounded-full bg-orange-500/20 text-orange-400 border border-orange-500/30">INTERVENTION</span>
        )}
      </div>

      <div className="mt-2 text-xs text-slate-500 truncate">
        {entity.constraint_pattern.replace(/_/g, " ")} · {entity.recommended_action.replace(/_/g, " ")}
      </div>
    </div>
  );
}

// ── page ──────────────────────────────────────────────────────────────────────

export default function BottleneckSniperEnginePage() {
  const [entities, setEntities]   = useState<ConstraintEntity[]>([]);
  const [summary, setSummary]     = useState<Summary | null>(null);
  const [loading, setLoading]     = useState(true);
  const [selected, setSelected]   = useState<ConstraintEntity | null>(null);
  const [filterRisk, setFilterRisk] = useState("all");

  useEffect(() => {
    setLoading(true);
    fetch("/api/bottleneck-sniper-engine")
      .then((r) => r.json())
      .then((data) => {
        setEntities(data.entities ?? []);
        setSummary(data.summary ?? null);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  const filtered = filterRisk === "all"
    ? entities
    : entities.filter((e) => e.constraint_risk === filterRisk);

  const RISKS = ["all", "critical", "high", "moderate", "low"];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
      <div className="max-w-6xl mx-auto space-y-6">

        {/* header */}
        <div>
          <h1 className="text-2xl font-bold text-red-400">
            Détecteur de Goulot — Bottleneck Sniper — Module 314
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Identifie et priorise les contraintes systèmes critiques en temps réel —
            Caelum Partners · Chaima Mhadbi, Fondatrice, Bruxelles
          </p>
        </div>

        {/* 6 KPI cards */}
        {summary && (
          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
            {[
              { label: "Total Systèmes",        value: summary.total_entities,                               color: "text-white" },
              { label: "En Crise Contrainte",   value: summary.crisis_entities,                              color: "text-red-400" },
              { label: "Requiert Intervention", value: summary.intervention_required,                        color: "text-orange-400" },
              { label: "Composite Moyen",       value: summary.avg_constraint_composite.toFixed(2),          color: "text-red-300" },
              { label: "Index Contrainte",      value: summary.avg_estimated_constraint_index.toFixed(2),    color: "text-orange-300" },
              { label: "Flux Moyen",            value: summary.avg_flow_score.toFixed(2),                    color: "text-yellow-400" },
            ].map(({ label, value, color }) => (
              <div key={label} className="bg-slate-900 border border-orange-700/30 rounded-xl p-4">
                <div className="text-xs text-slate-400">{label}</div>
                <div className={`text-2xl font-bold mt-1 ${color}`}>{value}</div>
              </div>
            ))}
          </div>
        )}

        {/* 4 GaugeRings */}
        {summary && (
          <div className="bg-slate-900 border border-orange-700/30 rounded-xl p-5">
            <div className="text-sm font-semibold text-slate-300 mb-4">Dimensions de la Contrainte</div>
            <div className="flex flex-wrap gap-6 justify-around">
              <GaugeRing score={summary.avg_flow_score}        label="Flux"        color="#f87171" />
              <GaugeRing score={summary.avg_constraint_score}  label="Contrainte"  color="#fb923c" />
              <GaugeRing score={summary.avg_system_score}      label="Système"     color="#fca5a5" />
              <GaugeRing score={summary.avg_resilience_score}  label="Résilience"  color="#fdba74" />
            </div>
          </div>
        )}

        {/* 4 DistBars */}
        {summary && (
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <DistBar title="Risque"    counts={summary.risk_counts}     colors={RISK_BAR} />
            <DistBar title="Patterns"  counts={summary.pattern_counts}   colors={PATTERN_BAR} />
            <DistBar title="Sévérité"  counts={summary.severity_counts}  colors={SEV_BAR} />
            <DistBar title="Actions"   counts={summary.action_counts}    colors={ACTION_BAR} />
          </div>
        )}

        {/* filter pills */}
        <div className="flex flex-wrap gap-2">
          {RISKS.map((r) => (
            <button
              key={r}
              onClick={() => setFilterRisk(r)}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium border transition-colors ${
                filterRisk === r
                  ? "bg-red-700 border-red-600 text-white"
                  : "bg-slate-900 border-slate-700 text-slate-400 hover:border-orange-700/50 hover:text-slate-200"
              }`}
            >
              {fmt(r)}
            </button>
          ))}
        </div>

        {/* entity cards */}
        {loading ? (
          <div className="text-slate-400 text-center py-16">Analyse des contraintes système en cours…</div>
        ) : filtered.length === 0 ? (
          <div className="text-slate-500 text-center py-16">Aucune entité ne correspond aux filtres.</div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {filtered.map((e) => (
              <EntityCard key={e.entity_id} entity={e} onClick={() => setSelected(e)} />
            ))}
          </div>
        )}
      </div>

      {selected && <DetailModal entity={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
