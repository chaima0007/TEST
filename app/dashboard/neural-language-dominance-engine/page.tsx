"use client";

import { useEffect, useState } from "react";

// ── types ────────────────────────────────────────────────────────────────────
interface LanguageEntity {
  id: string;
  language_domain: string;
  region: string;
  dominance_score: number;
  exclusion_score: number;
  homogenization_score: number;
  sovereignty_score: number;
  composite_score: number;
  risk_level: string;
  language_pattern: string;
  severity: string;
  recommended_action: string;
  signal: string;
  english_AI_training_bias: number;
  cognitive_sovereignty_erosion_index: number;
}

interface Summary {
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
  avg_estimated_linguistic_dominance_index: number;
  avg_dominance_score: number;
  avg_exclusion_score: number;
  avg_homogenization_score: number;
  avg_sovereignty_score: number;
}

// ── helpers ──────────────────────────────────────────────────────────────────
const RISK_COLOR: Record<string, string> = {
  critical: "text-indigo-400",
  high:     "text-teal-400",
  moderate: "text-indigo-300",
  low:      "text-slate-400",
};

const RISK_BG: Record<string, string> = {
  critical: "bg-indigo-500/20 border-indigo-500/40",
  high:     "bg-teal-500/20 border-teal-500/40",
  moderate: "bg-indigo-400/10 border-indigo-400/30",
  low:      "bg-slate-500/20 border-slate-500/40",
};

const SEVERITY_COLOR: Record<string, string> = {
  "hégémonie_linguistique_totale":    "text-indigo-400",
  "domination_linguistique_avancée":  "text-teal-400",
  "homogénéisation_active":           "text-indigo-300",
  "diversité_linguistique_relative":  "text-slate-400",
};

const PATTERN_ICON: Record<string, string> = {
  linguistic_monoculture_collapse: "🌐",
  cognitive_colonization:          "🧠",
  AI_language_hegemony:            "🤖",
  indigenous_extinction:           "🌿",
  semantic_manipulation_crisis:    "⚠️",
  none:                            "—",
};

const DOMAIN_ICON: Record<string, string> = {
  tech_platform:       "💻",
  minority_language:   "🗣️",
  social_media:        "📱",
  indigenous_community: "🌿",
  ai_foundation_model: "🤖",
  translation_service: "🌐",
  education_platform:  "📚",
  media_narrative:     "📰",
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
    <div className="bg-slate-900 border border-indigo-500/30 rounded-xl p-4">
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
function DetailModal({ entity, onClose }: { entity: LanguageEntity; onClose: () => void }) {
  const [tab, setTab] = useState<"scores" | "signal" | "action">("scores");

  useEffect(() => {
    const esc = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", esc);
    return () => window.removeEventListener("keydown", esc);
  }, [onClose]);

  const ringColor =
    entity.composite_score >= 60 ? "#6366f1"
    : entity.composite_score >= 40 ? "#14b8a6"
    : entity.composite_score >= 20 ? "#818cf8"
    : "#64748b";

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4"
      onClick={onClose}
    >
      <div
        className="bg-slate-900 border border-indigo-500/30 rounded-2xl w-full max-w-lg shadow-2xl"
        onClick={(e) => e.stopPropagation()}
      >
        {/* header */}
        <div className="flex items-center gap-4 p-5 border-b border-slate-800">
          <GaugeRing score={entity.composite_score} label="" color={ringColor} />
          <div className="flex-1 min-w-0">
            <h2 className="text-white font-bold text-lg truncate">
              {DOMAIN_ICON[entity.language_domain] || "🌐"} {entity.id}
            </h2>
            <p className="text-slate-400 text-sm">{entity.language_domain.replace(/_/g, " ")} · {entity.region}</p>
            <div className="flex gap-2 mt-1 flex-wrap">
              <span className={`text-xs px-2 py-0.5 rounded-full border ${RISK_BG[entity.risk_level]}`}>
                {entity.risk_level} risk
              </span>
              <span className={`text-xs font-medium ${SEVERITY_COLOR[entity.severity]}`}>
                {entity.severity.replace(/_/g, " ")}
              </span>
            </div>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl">✕</button>
        </div>

        {/* tabs */}
        <div className="flex border-b border-slate-800">
          {(["scores", "signal", "action"] as const).map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`flex-1 py-2.5 text-sm font-medium capitalize transition-colors ${
                tab === t ? "text-indigo-400 border-b-2 border-indigo-400" : "text-slate-500 hover:text-slate-300"
              }`}
            >
              {t === "scores" ? "Scores" : t === "signal" ? "Signal" : "Action"}
            </button>
          ))}
        </div>

        <div className="p-5 space-y-3">
          {tab === "scores" && (
            <div className="space-y-3">
              <ScoreBar label="Dominance Linguistique"    value={entity.dominance_score}      color="bg-indigo-500" />
              <ScoreBar label="Exclusion Minoritaire"     value={entity.exclusion_score}       color="bg-teal-500" />
              <ScoreBar label="Homogénéisation Cognitive" value={entity.homogenization_score}  color="bg-indigo-400" />
              <ScoreBar label="Érosion Souveraineté"      value={entity.sovereignty_score}     color="bg-teal-400" />
              <div className="grid grid-cols-2 gap-3 pt-2">
                {[
                  ["Biais IA Anglais",      (entity.english_AI_training_bias * 100).toFixed(0) + "%"],
                  ["Érosion Souveraineté",  (entity.cognitive_sovereignty_erosion_index * 100).toFixed(0) + "%"],
                  ["Pattern",               PATTERN_ICON[entity.language_pattern] + " " + entity.language_pattern.replace(/_/g, " ")],
                  ["Composite",             entity.composite_score.toFixed(1)],
                ].map(([label, value]) => (
                  <div key={label as string} className="bg-slate-800/60 rounded-lg p-3">
                    <div className="text-xs text-slate-400">{label}</div>
                    <div className="text-white font-semibold mt-0.5 text-sm">{value}</div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {tab === "signal" && (
            <div className="space-y-3">
              <div className="bg-indigo-500/10 border border-indigo-500/30 rounded-xl p-4">
                <div className="text-xs text-indigo-400 uppercase tracking-wide mb-2">Signal Linguistique</div>
                <div className="text-indigo-200 text-sm leading-relaxed">{entity.signal}</div>
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div className="bg-slate-800/60 rounded-lg p-3">
                  <div className="text-xs text-slate-400">Sévérité</div>
                  <div className={`font-semibold mt-0.5 text-sm ${SEVERITY_COLOR[entity.severity]}`}>
                    {entity.severity.replace(/_/g, " ")}
                  </div>
                </div>
                <div className="bg-slate-800/60 rounded-lg p-3">
                  <div className="text-xs text-slate-400">Niveau de Risque</div>
                  <div className={`font-semibold mt-0.5 text-sm uppercase ${RISK_COLOR[entity.risk_level]}`}>
                    {entity.risk_level}
                  </div>
                </div>
              </div>
            </div>
          )}

          {tab === "action" && (
            <div className="space-y-3">
              <div className="bg-teal-500/10 border border-teal-500/30 rounded-xl p-4">
                <div className="text-xs text-teal-400 uppercase tracking-wide mb-1">Action Recommandée</div>
                <div className="text-white font-bold text-lg">
                  {entity.recommended_action.replace(/_/g, " ")}
                </div>
              </div>
              {entity.risk_level === "critical" && (
                <div className="bg-indigo-500/10 border border-indigo-500/30 rounded-xl p-3 text-sm text-indigo-300">
                  🔴 Intervention urgente requise — hégémonie linguistique critique détectée
                </div>
              )}
              {entity.risk_level === "high" && (
                <div className="bg-teal-500/10 border border-teal-500/30 rounded-xl p-3 text-sm text-teal-300">
                  🟠 Risque élevé — décolonisation linguistique prioritaire
                </div>
              )}
              {entity.risk_level === "moderate" && (
                <div className="bg-indigo-400/10 border border-indigo-400/20 rounded-xl p-3 text-sm text-indigo-300">
                  🟡 Vigilance — renforcement du multilinguisme recommandé
                </div>
              )}
              {entity.risk_level === "low" && (
                <div className="bg-slate-800/60 rounded-xl p-3 text-sm text-slate-400">
                  🟢 Diversité préservée — veille linguistique continue recommandée
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
function EntityCard({ entity, onClick }: { entity: LanguageEntity; onClick: () => void }) {
  const ringColor =
    entity.composite_score >= 60 ? "#6366f1"
    : entity.composite_score >= 40 ? "#14b8a6"
    : entity.composite_score >= 20 ? "#818cf8"
    : "#64748b";

  return (
    <div
      onClick={onClick}
      className="bg-slate-900 border border-slate-800 rounded-xl p-4 cursor-pointer hover:border-indigo-500/30 hover:bg-slate-800/60 transition-all"
    >
      <div className="flex items-center gap-3">
        <GaugeRing score={entity.composite_score} label="" color={ringColor} />
        <div className="flex-1 min-w-0">
          <div className="text-white font-semibold truncate">
            {DOMAIN_ICON[entity.language_domain] || "🌐"} {entity.id}
          </div>
          <div className="text-slate-400 text-xs">{entity.language_domain.replace(/_/g, " ")} · {entity.region}</div>
          <div className="flex gap-2 mt-1 flex-wrap">
            <span className={`text-xs px-2 py-0.5 rounded-full border ${RISK_BG[entity.risk_level]}`}>
              {entity.risk_level}
            </span>
          </div>
        </div>
        <div className="text-right shrink-0">
          <div className={`text-sm font-bold ${SEVERITY_COLOR[entity.severity]}`}>
            {entity.severity.replace(/_/g, " ").split(" ")[0]}
          </div>
          <div className="text-xs text-slate-500 mt-1">{entity.composite_score.toFixed(1)}</div>
        </div>
      </div>
      <div className="mt-2 text-xs text-slate-400">
        {PATTERN_ICON[entity.language_pattern]} {entity.language_pattern.replace(/_/g, " ")}
      </div>
    </div>
  );
}

// ── page ──────────────────────────────────────────────────────────────────────
export default function NeuralLanguageDominancePage() {
  const [entities, setEntities]   = useState<LanguageEntity[]>([]);
  const [summary, setSummary]     = useState<Summary | null>(null);
  const [loading, setLoading]     = useState(true);
  const [selected, setSelected]   = useState<LanguageEntity | null>(null);
  const [filterRisk,    setFilterRisk]    = useState("all");
  const [filterPattern, setFilterPattern] = useState("all");

  useEffect(() => {
    setLoading(true);
    const params = new URLSearchParams();
    if (filterRisk    !== "all") params.set("risk",    filterRisk);
    if (filterPattern !== "all") params.set("pattern", filterPattern);
    fetch(`/api/neural-language-dominance-engine?${params}`)
      .then((r) => r.json())
      .then((data) => {
        let filtered = data.entities as LanguageEntity[];
        if (filterRisk    !== "all") filtered = filtered.filter((e) => e.risk_level === filterRisk);
        if (filterPattern !== "all") filtered = filtered.filter((e) => e.language_pattern === filterPattern);
        setEntities(filtered);
        setSummary(data.summary as Summary);
        setLoading(false);
      });
  }, [filterRisk, filterPattern]);

  const distributions: Array<{ title: string; counts: Record<string, number>; colors: Record<string, string> }> = [
    {
      title: "Distribution du Risque",
      counts: summary?.risk_distribution ?? {},
      colors: { critical: "bg-indigo-500", high: "bg-teal-500", moderate: "bg-indigo-300", low: "bg-slate-500" },
    },
    {
      title: "Patterns Linguistiques",
      counts: summary?.pattern_distribution ?? {},
      colors: { linguistic_monoculture_collapse: "bg-indigo-500", cognitive_colonization: "bg-teal-500", AI_language_hegemony: "bg-indigo-400", indigenous_extinction: "bg-teal-400", semantic_manipulation_crisis: "bg-indigo-300", none: "bg-slate-500" },
    },
    {
      title: "Sévérité Linguistique",
      counts: summary?.severity_distribution ?? {},
      colors: { "hégémonie_linguistique_totale": "bg-indigo-500", "domination_linguistique_avancée": "bg-teal-500", "homogénéisation_active": "bg-indigo-300", "diversité_linguistique_relative": "bg-slate-500" },
    },
    {
      title: "Actions Prescrites",
      counts: summary?.action_distribution ?? {},
      colors: { "souveraineté_linguistique_urgente": "bg-indigo-500", "décolonisation_linguistique_IA": "bg-teal-500", "renforcement_multilinguisme_IA": "bg-indigo-300", "veille_diversité_linguistique": "bg-slate-600" },
    },
  ];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
      <div className="max-w-6xl mx-auto space-y-6">

        {/* header */}
        <div>
          <h1 className="text-2xl font-bold text-white">
            Dominance Linguistique Neurale &amp; Intelligence Linguistique — Module 336
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Analyse l&apos;hégémonie linguistique induite par l&apos;IA, la colonisation cognitive et l&apos;érosion
            de la souveraineté multilingue dans les écosystèmes langagiers mondiaux.
          </p>
        </div>

        {/* KPI strip — 6 cards */}
        {summary && (
          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
            {[
              { label: "Total Systèmes",          value: summary.total_entities },
              { label: "Hégémonie Totale",         value: summary.critical_count,                              color: "text-indigo-400" },
              { label: "Domination Avancée",       value: summary.high_count,                                  color: "text-teal-400" },
              { label: "Composite Moyen",          value: summary.avg_composite.toFixed(1),                    color: "text-indigo-300" },
              { label: "Index Domination Ling.",   value: summary.avg_estimated_linguistic_dominance_index.toFixed(2), color: "text-teal-300" },
              { label: "Dominance Moyenne",        value: summary.avg_dominance_score?.toFixed(1) ?? "—",      color: "text-indigo-200" },
            ].map(({ label, value, color }) => (
              <div key={label} className="bg-slate-900 border border-indigo-500/30 rounded-xl p-4">
                <div className="text-xs text-slate-400">{label}</div>
                <div className={`text-2xl font-bold mt-1 ${color ?? "text-white"}`}>{value}</div>
              </div>
            ))}
          </div>
        )}

        {/* 4 GaugeRings */}
        {summary && (
          <div className="bg-slate-900 border border-indigo-500/30 rounded-xl p-5">
            <div className="text-sm font-semibold text-slate-300 mb-4">Dimensions de la Dominance Linguistique</div>
            <div className="flex flex-wrap gap-6 justify-around">
              <GaugeRing score={summary.avg_dominance_score}      label="Dominance"       color="#6366f1" />
              <GaugeRing score={summary.avg_exclusion_score}      label="Exclusion"       color="#14b8a6" />
              <GaugeRing score={summary.avg_homogenization_score} label="Homogénéisation" color="#818cf8" />
              <GaugeRing score={summary.avg_sovereignty_score}    label="Souveraineté"    color="#2dd4bf" />
            </div>
          </div>
        )}

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
            { label: "Tous",              val: "all" },
            { label: "🔴 Critique",       val: "critical" },
            { label: "🟠 Élevé",          val: "high" },
            { label: "🟡 Modéré",         val: "moderate" },
            { label: "🟢 Faible",         val: "low" },
          ].map(({ label, val }) => (
            <button
              key={val}
              onClick={() => setFilterRisk(val)}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
                filterRisk === val
                  ? "bg-indigo-700 text-white"
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
            <option value="all">Tous Patterns</option>
            {["linguistic_monoculture_collapse", "cognitive_colonization", "AI_language_hegemony", "indigenous_extinction", "semantic_manipulation_crisis", "none"].map((p) => (
              <option key={p} value={p}>{p.replace(/_/g, " ")}</option>
            ))}
          </select>
        </div>

        {/* entity cards grid */}
        {loading ? (
          <div className="text-slate-400 text-center py-16">Analyse de la dominance linguistique…</div>
        ) : entities.length === 0 ? (
          <div className="text-slate-500 text-center py-16">Aucune entité ne correspond aux filtres.</div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {entities.map((e) => (
              <EntityCard key={e.id} entity={e} onClick={() => setSelected(e)} />
            ))}
          </div>
        )}
      </div>

      {selected && <DetailModal entity={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
