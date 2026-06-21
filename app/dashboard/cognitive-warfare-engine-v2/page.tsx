"use client";

import { useEffect, useState } from "react";

// ── types ────────────────────────────────────────────────────────────────────
interface CognitiveWarfareEntity {
  id: string;
  region: string;
  operation_type: string;
  warfare_risk: string;
  warfare_pattern: string;
  warfare_severity: string;
  recommended_action: string;
  disinformation_score: number;
  influence_score: number;
  erosion_score: number;
  vulnerability_score: number;
  warfare_composite: number;
  is_warfare_crisis: boolean;
  requires_warfare_intervention: boolean;
  warfare_signal: string;
}

interface Summary {
  module: string;
  analyst: string;
  total_entities: number;
  warfare_crises: number;
  requires_intervention: number;
  avg_estimated_cognitive_warfare_index: number;
  avg_warfare_composite: number;
  risk_distribution: Record<string, number>;
  pattern_distribution: Record<string, number>;
  critical_entities: string[];
  crisis_entities: string[];
  top_threat: string;
  entities: CognitiveWarfareEntity[];
}

// ── helpers ──────────────────────────────────────────────────────────────────
const RISK_COLOR: Record<string, string> = {
  critical: "text-rose-400",
  high:     "text-rose-300",
  moderate: "text-slate-300",
  low:      "text-slate-400",
};

const RISK_BG: Record<string, string> = {
  critical: "bg-rose-500/20 border-rose-500/40",
  high:     "bg-rose-400/15 border-rose-400/35",
  moderate: "bg-slate-500/15 border-slate-500/35",
  low:      "bg-slate-700/20 border-slate-600/30",
};

const SEVERITY_COLOR: Record<string, string> = {
  info_war_emergency:         "text-rose-400",
  high_cognitive_threat:      "text-rose-300",
  cognitive_attack_developing: "text-slate-300",
  cognitive_resilient:        "text-slate-400",
};

const PATTERN_ICON: Record<string, string> = {
  deepfake_information_war:   "🎭",
  epistemic_collapse:         "🧠",
  influence_network_dominance: "🕸️",
  narrative_siege:            "📢",
  cognitive_immune_failure:   "🛡️",
  none:                       "—",
};

const OP_ICON: Record<string, string> = {
  state_sponsored_operation: "🏛️",
  defensive_operation:       "🛡️",
  election_interference:     "🗳️",
  local_disinfo:             "📰",
  hybrid_warfare:            "⚔️",
  commercial_influence:      "💼",
  social_manipulation:       "👥",
  ai_generated_psyop:        "🤖",
};

// ── GaugeRing ────────────────────────────────────────────────────────────────
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

// ── ScoreBar ─────────────────────────────────────────────────────────────────
function ScoreBar({ label, value, color }: { label: string; value: number; color: string }) {
  return (
    <div>
      <div className="flex justify-between text-xs text-slate-400 mb-1">
        <span>{label}</span><span>{value.toFixed(1)}</span>
      </div>
      <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
        <div className={`h-full rounded-full ${color}`} style={{ width: `${value}%` }} />
      </div>
    </div>
  );
}

// ── DistBar ───────────────────────────────────────────────────────────────────
function DistBar({ title, counts, colors }: { title: string; counts: Record<string, number>; colors: Record<string, string> }) {
  const total = Object.values(counts).reduce((a, b) => a + b, 0) || 1;
  return (
    <div className="bg-slate-900 border border-slate-500/30 rounded-xl p-4">
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

// ── DetailModal ───────────────────────────────────────────────────────────────
function DetailModal({ entity, onClose }: { entity: CognitiveWarfareEntity; onClose: () => void }) {
  const [tab, setTab] = useState<"overview" | "scores" | "action">("overview");

  useEffect(() => {
    const esc = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", esc);
    return () => window.removeEventListener("keydown", esc);
  }, [onClose]);

  const ringColor =
    entity.warfare_composite >= 60 ? "#f43f5e"
    : entity.warfare_composite >= 40 ? "#fb7185"
    : entity.warfare_composite >= 20 ? "#94a3b8"
    : "#64748b";

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4"
      onClick={onClose}
    >
      <div
        className="bg-slate-900 border border-slate-500/30 rounded-2xl w-full max-w-lg shadow-2xl"
        onClick={(e) => e.stopPropagation()}
      >
        {/* header */}
        <div className="flex items-center gap-4 p-5 border-b border-slate-800">
          <GaugeRing score={entity.warfare_composite} label="" color={ringColor} />
          <div className="flex-1 min-w-0">
            <h2 className="text-white font-bold text-lg truncate">
              {OP_ICON[entity.operation_type] || "🎯"} {entity.id}
            </h2>
            <p className="text-slate-400 text-sm">{entity.operation_type.replace(/_/g, " ")} · {entity.region}</p>
            <div className="flex gap-2 mt-1 flex-wrap">
              <span className={`text-xs px-2 py-0.5 rounded-full border ${RISK_BG[entity.warfare_risk]}`}>
                {entity.warfare_risk} risk
              </span>
              <span className={`text-xs font-medium ${SEVERITY_COLOR[entity.warfare_severity]}`}>
                {entity.warfare_severity.replace(/_/g, " ")}
              </span>
            </div>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl">✕</button>
        </div>

        {/* tabs */}
        <div className="flex border-b border-slate-800">
          {(["overview", "scores", "action"] as const).map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`flex-1 py-2.5 text-sm font-medium capitalize transition-colors ${
                tab === t ? "text-rose-400 border-b-2 border-rose-400" : "text-slate-500 hover:text-slate-300"
              }`}
            >
              {t === "overview" ? "Vue d'ensemble" : t === "scores" ? "Scores" : "Action"}
            </button>
          ))}
        </div>

        <div className="p-5 space-y-3">
          {tab === "overview" && (
            <>
              <div className="grid grid-cols-2 gap-3">
                {[
                  ["Patron",               PATTERN_ICON[entity.warfare_pattern] + " " + entity.warfare_pattern.replace(/_/g, " ")],
                  ["Composite Guerre",     entity.warfare_composite.toFixed(2) + " / 100"],
                  ["Crise Active",         entity.is_warfare_crisis ? "🚨 Oui" : "Non"],
                  ["Intervention Requise", entity.requires_warfare_intervention ? "⚡ Oui" : "Non"],
                ].map(([label, value]) => (
                  <div key={label as string} className="bg-slate-800/60 rounded-lg p-3">
                    <div className="text-xs text-slate-400">{label}</div>
                    <div className="text-white font-semibold mt-0.5 text-sm">{value}</div>
                  </div>
                ))}
              </div>
              <div className="bg-slate-800/60 rounded-lg p-3">
                <div className="text-xs text-slate-400 mb-1">Signal de Guerre Cognitive</div>
                <div className="text-rose-300 text-sm leading-relaxed">{entity.warfare_signal}</div>
              </div>
            </>
          )}

          {tab === "scores" && (
            <div className="space-y-3">
              <ScoreBar label="Désinformation"  value={entity.disinformation_score} color="bg-rose-500" />
              <ScoreBar label="Influence"        value={entity.influence_score}      color="bg-rose-400" />
              <ScoreBar label="Érosion"          value={entity.erosion_score}        color="bg-slate-500" />
              <ScoreBar label="Vulnérabilité"    value={entity.vulnerability_score}  color="bg-rose-300" />
            </div>
          )}

          {tab === "action" && (
            <div className="space-y-3">
              <div className="bg-rose-500/10 border border-rose-500/30 rounded-xl p-4">
                <div className="text-xs text-rose-400 uppercase tracking-wide mb-1">Action Recommandée</div>
                <div className="text-white font-bold text-lg capitalize">
                  {entity.recommended_action.replace(/_/g, " ")}
                </div>
              </div>
              {entity.is_warfare_crisis && (
                <div className="bg-rose-500/10 border border-rose-500/30 rounded-xl p-3 text-sm text-rose-300">
                  🚨 Crise de guerre cognitive — déclencher le protocole d&apos;urgence immédiatement
                </div>
              )}
              {entity.requires_warfare_intervention && !entity.is_warfare_crisis && (
                <div className="bg-rose-400/10 border border-rose-400/30 rounded-xl p-3 text-sm text-rose-200">
                  ⚡ Intervention requise — opération d&apos;influence active détectée
                </div>
              )}
              {!entity.requires_warfare_intervention && (
                <div className="bg-slate-800/60 rounded-xl p-3 text-sm text-slate-400">
                  ✅ Environnement cognitif stable — surveillance continue recommandée
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
function EntityCard({ entity, onClick }: { entity: CognitiveWarfareEntity; onClick: () => void }) {
  const ringColor =
    entity.warfare_composite >= 60 ? "#f43f5e"
    : entity.warfare_composite >= 40 ? "#fb7185"
    : entity.warfare_composite >= 20 ? "#94a3b8"
    : "#64748b";

  return (
    <div
      onClick={onClick}
      className="bg-slate-900 border border-slate-800 rounded-xl p-4 cursor-pointer hover:border-slate-500/30 hover:bg-slate-800/60 transition-all"
    >
      <div className="flex items-center gap-3">
        <GaugeRing score={entity.warfare_composite} label="" color={ringColor} />
        <div className="flex-1 min-w-0">
          <div className="text-white font-semibold truncate">
            {OP_ICON[entity.operation_type] || "🎯"} {entity.id}
          </div>
          <div className="text-slate-400 text-xs">{entity.operation_type.replace(/_/g, " ")} · {entity.region}</div>
          <div className="flex gap-2 mt-1 flex-wrap">
            <span className={`text-xs px-2 py-0.5 rounded-full border ${RISK_BG[entity.warfare_risk]}`}>
              {entity.warfare_risk}
            </span>
          </div>
        </div>
        <div className="text-right shrink-0">
          {entity.is_warfare_crisis && <div className="text-xs text-rose-400">🚨 Crise</div>}
          <div className={`text-sm font-bold mt-1 ${SEVERITY_COLOR[entity.warfare_severity]}`}>
            {entity.warfare_severity.replace(/_/g, " ")}
          </div>
          {entity.requires_warfare_intervention && !entity.is_warfare_crisis && (
            <div className="text-xs text-rose-300 mt-1">⚡ Intervention</div>
          )}
        </div>
      </div>
      <div className="mt-2 text-xs text-slate-400">
        {PATTERN_ICON[entity.warfare_pattern]} {entity.warfare_pattern.replace(/_/g, " ")} · composite: {entity.warfare_composite.toFixed(2)}
      </div>
    </div>
  );
}

// ── page ──────────────────────────────────────────────────────────────────────
export default function CognitiveWarfareEnginePage() {
  const [summary, setSummary]   = useState<Summary | null>(null);
  const [loading, setLoading]   = useState(true);
  const [selected, setSelected] = useState<CognitiveWarfareEntity | null>(null);
  const [filterRisk,    setFilterRisk]    = useState("all");
  const [filterPattern, setFilterPattern] = useState("all");

  useEffect(() => {
    setLoading(true);
    fetch("/api/cognitive-warfare-engine-v2")
      .then((r) => r.json())
      .then((data) => {
        setSummary(data);
        setLoading(false);
      });
  }, []);

  const entities = summary?.entities ?? [];
  const filtered = entities.filter((e) => {
    if (filterRisk    !== "all" && e.warfare_risk    !== filterRisk)    return false;
    if (filterPattern !== "all" && e.warfare_pattern !== filterPattern) return false;
    return true;
  });

  const distributions: Array<{ title: string; counts: Record<string, number>; colors: Record<string, string> }> = [
    {
      title: "Distribution du Risque",
      counts: summary?.risk_distribution ?? {},
      colors: { critical: "bg-rose-500", high: "bg-rose-400", moderate: "bg-slate-500", low: "bg-slate-600" },
    },
    {
      title: "Patrons de Guerre Cognitive",
      counts: summary?.pattern_distribution ?? {},
      colors: {
        deepfake_information_war: "bg-rose-500",
        epistemic_collapse: "bg-rose-400",
        influence_network_dominance: "bg-rose-300",
        narrative_siege: "bg-slate-400",
        cognitive_immune_failure: "bg-slate-500",
        none: "bg-slate-600",
      },
    },
    {
      title: "Entités en Crise",
      counts: summary ? {
        "en crise": summary.warfare_crises,
        "intervention requise": summary.requires_intervention - summary.warfare_crises,
        "stable": (summary.total_entities - summary.requires_intervention),
      } : {},
      colors: { "en crise": "bg-rose-500", "intervention requise": "bg-rose-300", "stable": "bg-slate-600" },
    },
    {
      title: "Entités Critiques",
      counts: summary ? {
        "critiques": summary.critical_entities.length,
        "autres": summary.total_entities - summary.critical_entities.length,
      } : {},
      colors: { "critiques": "bg-rose-500", "autres": "bg-slate-600" },
    },
  ];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
      <div className="max-w-6xl mx-auto space-y-6">

        {/* header */}
        <div>
          <h1 className="text-2xl font-bold text-white">
            Guerre Cognitive &amp; Opérations d&apos;Information — Module 323
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Détecte et analyse les opérations de guerre cognitive, campagnes de désinformation, réseaux
            d&apos;influence et attaques épistémiques — prescription d&apos;interventions avant l&apos;effondrement
            institutionnel.
          </p>
          {summary && (
            <p className="text-slate-500 text-xs mt-1">{summary.analyst} · {summary.module}</p>
          )}
        </div>

        {/* KPI strip — 6 cards */}
        {summary && (
          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
            {[
              { label: "Entités",              value: summary.total_entities },
              { label: "Composite Moy.",       value: summary.avg_warfare_composite.toFixed(1),                  color: "text-rose-400" },
              { label: "Crises Actives",       value: summary.warfare_crises,                                    color: "text-rose-500" },
              { label: "Interventions",        value: summary.requires_intervention,                             color: "text-rose-300" },
              { label: "Indice Guerre Moy.",   value: summary.avg_estimated_cognitive_warfare_index.toFixed(2),  color: "text-rose-200" },
              { label: "Entités Critiques",    value: summary.critical_entities.length,                         color: "text-slate-300" },
            ].map(({ label, value, color }) => (
              <div key={label} className="bg-slate-900 border border-slate-500/30 rounded-xl p-4">
                <div className="text-xs text-slate-400">{label}</div>
                <div className={`text-2xl font-bold mt-1 ${color ?? "text-white"}`}>{value}</div>
              </div>
            ))}
          </div>
        )}

        {/* 4 GaugeRings */}
        {summary && (() => {
          const entities = summary.entities;
          const n = entities.length || 1;
          const avgDis  = entities.reduce((s, e) => s + e.disinformation_score, 0) / n;
          const avgInf  = entities.reduce((s, e) => s + e.influence_score, 0) / n;
          const avgEro  = entities.reduce((s, e) => s + e.erosion_score, 0) / n;
          const avgVul  = entities.reduce((s, e) => s + e.vulnerability_score, 0) / n;
          return (
            <div className="bg-slate-900 border border-slate-500/30 rounded-xl p-5">
              <div className="text-sm font-semibold text-slate-300 mb-4">Dimensions de la Guerre Cognitive</div>
              <div className="flex flex-wrap gap-6 justify-around">
                <GaugeRing score={avgDis}  label="Désinformation"  color="#f43f5e" />
                <GaugeRing score={avgInf}  label="Influence"        color="#fb7185" />
                <GaugeRing score={avgEro}  label="Érosion"          color="#94a3b8" />
                <GaugeRing score={avgVul}  label="Vulnérabilité"    color="#e2e8f0" />
              </div>
            </div>
          );
        })()}

        {/* 4 DistBars */}
        {summary && (
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {distributions.map((d) => (
              <DistBar key={d.title} title={d.title} counts={d.counts} colors={d.colors} />
            ))}
          </div>
        )}

        {/* filter pills */}
        <div className="flex flex-wrap gap-2">
          {[
            { label: "Tous",        val: "all" },
            { label: "🔴 Critical", val: "critical" },
            { label: "🟠 High",     val: "high" },
            { label: "🟡 Moderate", val: "moderate" },
            { label: "🟢 Low",      val: "low" },
          ].map(({ label, val }) => (
            <button
              key={val}
              onClick={() => setFilterRisk(val)}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
                filterRisk === val
                  ? "bg-rose-700 text-white"
                  : "bg-slate-800 text-slate-400 hover:text-white"
              }`}
            >
              {label}
            </button>
          ))}
          <select
            value={filterPattern}
            onChange={(e) => setFilterPattern(e.target.value)}
            className="px-3 py-1.5 rounded-lg text-xs bg-slate-800 text-slate-300 border border-slate-700"
          >
            <option value="all">Tous Patrons</option>
            {["deepfake_information_war", "epistemic_collapse", "influence_network_dominance", "narrative_siege", "cognitive_immune_failure", "none"].map((p) => (
              <option key={p} value={p}>{p.replace(/_/g, " ")}</option>
            ))}
          </select>
        </div>

        {/* entity cards grid */}
        {loading ? (
          <div className="text-slate-400 text-center py-16">Analyse de la guerre cognitive en cours…</div>
        ) : filtered.length === 0 ? (
          <div className="text-slate-500 text-center py-16">Aucune entité ne correspond aux filtres.</div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {filtered.map((e) => (
              <EntityCard key={e.id} entity={e} onClick={() => setSelected(e)} />
            ))}
          </div>
        )}
      </div>

      {selected && <DetailModal entity={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
