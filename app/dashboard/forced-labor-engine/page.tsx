"use client";

import { useEffect, useState } from "react";

// ── types ────────────────────────────────────────────────────────────────────
interface ForcedLaborEntity {
  entity_id: string;
  labor_sector: string;
  region: string;
  exploitation_score: number;
  detection_score: number;
  impunity_score: number;
  vulnerability_score: number;
  composite_score: number;
  risk_level: string;
  labor_pattern: string;
  severity: string;
  recommended_action: string;
  signal: string;
  forced_labor_prevalence: number;
  migrant_worker_vulnerability: number;
}

interface Summary {
  module_id: number;
  module_name: string;
  total: number;
  critical: number;
  high: number;
  moderate: number;
  low: number;
  avg_composite: number;
  pattern_distribution: Record<string, number>;
  risk_distribution: Record<string, number>;
  severity_distribution: Record<string, number>;
  action_distribution: Record<string, number>;
  avg_estimated_forced_labor_index: number;
}

// ── helpers ──────────────────────────────────────────────────────────────────
const RISK_COLOR: Record<string, string> = {
  critical: "text-red-400",
  high:     "text-red-300",
  moderate: "text-slate-300",
  low:      "text-slate-500",
};

const RISK_BG: Record<string, string> = {
  critical: "bg-red-500/20 border-red-500/40",
  high:     "bg-red-400/15 border-red-400/30",
  moderate: "bg-slate-500/20 border-slate-500/40",
  low:      "bg-slate-700/30 border-slate-600/30",
};

const SEVERITY_COLOR: Record<string, string> = {
  "crise_esclavage_moderne_systémique":       "text-red-400",
  "exploitation_grave_travail_forcé":         "text-red-300",
  "vulnérabilité_structurelle_travail_forcé": "text-slate-300",
  "surveillance_travail_forcé_active":        "text-slate-500",
};

const PATTERN_ICON: Record<string, string> = {
  supply_chain_slavery_nexus: "⛓️",
  debt_bondage_trap:          "💸",
  domestic_servitude_network: "🏠",
  sex_trafficking_economy:    "⚠️",
  prison_labor_exploitation:  "🔒",
};

const SECTOR_ICON: Record<string, string> = {
  industrie_textile:       "🧵",
  agriculture_intensive:   "🌾",
  travail_domestique:      "🏡",
  exploitation_sexuelle:   "⚠️",
  "travail_carcéral":      "🔒",
  "extraction_minière":    "⛏️",
  "manufacturing_certifié":"🏭",
  "technologie_responsable":"💻",
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
    <div className="bg-slate-900 border border-red-500/30 rounded-xl p-4">
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
function DetailModal({ entity, onClose }: { entity: ForcedLaborEntity; onClose: () => void }) {
  const [tab, setTab] = useState<"overview" | "scores" | "action">("overview");

  useEffect(() => {
    const esc = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", esc);
    return () => window.removeEventListener("keydown", esc);
  }, [onClose]);

  const ringColor =
    entity.composite_score >= 60 ? "#ef4444"
    : entity.composite_score >= 40 ? "#f87171"
    : entity.composite_score >= 20 ? "#94a3b8"
    : "#64748b";

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4"
      onClick={onClose}
    >
      <div
        className="bg-slate-900 border border-red-500/30 rounded-2xl w-full max-w-lg shadow-2xl"
        onClick={(e) => e.stopPropagation()}
      >
        {/* header */}
        <div className="flex items-center gap-4 p-5 border-b border-slate-800">
          <GaugeRing score={entity.composite_score} label="" color={ringColor} />
          <div className="flex-1 min-w-0">
            <h2 className="text-white font-bold text-lg truncate">
              {SECTOR_ICON[entity.labor_sector] || "⚙️"} {entity.entity_id}
            </h2>
            <p className="text-slate-400 text-sm">{entity.labor_sector.replace(/_/g, " ")} · {entity.region}</p>
            <div className="flex gap-2 mt-1 flex-wrap">
              <span className={`text-xs px-2 py-0.5 rounded-full border ${RISK_BG[entity.risk_level]}`}>
                {entity.risk_level} risk
              </span>
              <span className={`text-xs font-medium ${SEVERITY_COLOR[entity.severity] ?? "text-slate-400"}`}>
                {entity.severity.replace(/_/g, " ")}
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
                tab === t ? "text-red-400 border-b-2 border-red-400" : "text-slate-500 hover:text-slate-300"
              }`}
            >
              {t}
            </button>
          ))}
        </div>

        <div className="p-5 space-y-3">
          {tab === "overview" && (
            <>
              <div className="grid grid-cols-2 gap-3">
                {[
                  ["Pattern",                   (PATTERN_ICON[entity.labor_pattern] || "⛓️") + " " + entity.labor_pattern.replace(/_/g, " ")],
                  ["Prévalence Travail Forcé",  (entity.forced_labor_prevalence * 100).toFixed(1) + "%"],
                  ["Vulnérabilité Migrants",    (entity.migrant_worker_vulnerability * 100).toFixed(1) + "%"],
                  ["Score Composite",           entity.composite_score.toFixed(1) + " / 100"],
                ].map(([label, value]) => (
                  <div key={label as string} className="bg-slate-800/60 rounded-lg p-3">
                    <div className="text-xs text-slate-400">{label}</div>
                    <div className="text-white font-semibold mt-0.5 text-sm">{value}</div>
                  </div>
                ))}
              </div>
              <div className="bg-slate-800/60 rounded-lg p-3">
                <div className="text-xs text-slate-400 mb-1">Signal Travail Forcé</div>
                <div className="text-red-300 text-sm leading-relaxed">{entity.signal}</div>
              </div>
            </>
          )}

          {tab === "scores" && (
            <div className="space-y-3">
              <ScoreBar label="Score Exploitation"  value={entity.exploitation_score}  color="bg-red-500" />
              <ScoreBar label="Score Détection"     value={entity.detection_score}     color="bg-red-400" />
              <ScoreBar label="Score Impunité"      value={entity.impunity_score}      color="bg-slate-500" />
              <ScoreBar label="Score Vulnérabilité" value={entity.vulnerability_score} color="bg-red-300" />
            </div>
          )}

          {tab === "action" && (
            <div className="space-y-3">
              <div className="bg-red-500/10 border border-red-500/30 rounded-xl p-4">
                <div className="text-xs text-red-400 uppercase tracking-wide mb-1">Action Recommandée</div>
                <div className="text-white font-bold text-lg capitalize">
                  {entity.recommended_action.replace(/_/g, " ")}
                </div>
              </div>
              {entity.risk_level === "critical" && (
                <div className="bg-red-500/10 border border-red-500/30 rounded-xl p-3 text-sm text-red-300">
                  🔴 Crise esclavage moderne — déclencher le protocole d&apos;intervention d&apos;urgence immédiatement
                </div>
              )}
              {entity.risk_level === "high" && (
                <div className="bg-red-400/10 border border-red-400/30 rounded-xl p-3 text-sm text-red-200">
                  🟠 Exploitation grave détectée — renforcer la protection des victimes en priorité
                </div>
              )}
              {entity.risk_level === "moderate" && (
                <div className="bg-slate-700/40 border border-slate-600/30 rounded-xl p-3 text-sm text-slate-300">
                  🟡 Vulnérabilité structurelle — surveillance renforcée des chaînes d&apos;approvisionnement
                </div>
              )}
              {entity.risk_level === "low" && (
                <div className="bg-slate-800/60 rounded-xl p-3 text-sm text-slate-400">
                  🟢 Conformité satisfaisante — veille travail forcé continue recommandée
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
function EntityCard({ entity, onClick }: { entity: ForcedLaborEntity; onClick: () => void }) {
  const ringColor =
    entity.composite_score >= 60 ? "#ef4444"
    : entity.composite_score >= 40 ? "#f87171"
    : entity.composite_score >= 20 ? "#94a3b8"
    : "#64748b";

  return (
    <div
      onClick={onClick}
      className="bg-slate-900 border border-slate-800 rounded-xl p-4 cursor-pointer hover:border-red-500/30 hover:bg-slate-800/60 transition-all"
    >
      <div className="flex items-center gap-3">
        <GaugeRing score={entity.composite_score} label="" color={ringColor} />
        <div className="flex-1 min-w-0">
          <div className="text-white font-semibold truncate">
            {SECTOR_ICON[entity.labor_sector] || "⚙️"} {entity.entity_id}
          </div>
          <div className="text-slate-400 text-xs">{entity.labor_sector.replace(/_/g, " ")} · {entity.region}</div>
          <div className="flex gap-2 mt-1 flex-wrap">
            <span className={`text-xs px-2 py-0.5 rounded-full border ${RISK_BG[entity.risk_level]}`}>
              {entity.risk_level}
            </span>
          </div>
        </div>
        <div className="text-right shrink-0">
          <div className={`text-sm font-bold ${RISK_COLOR[entity.risk_level]}`}>
            {entity.composite_score.toFixed(1)}
          </div>
          <div className="text-xs text-slate-500 mt-0.5">composite</div>
        </div>
      </div>
      <div className="mt-2 text-xs text-slate-400">
        {PATTERN_ICON[entity.labor_pattern] || "⛓️"} {entity.labor_pattern.replace(/_/g, " ")} · prévalence: {(entity.forced_labor_prevalence * 100).toFixed(0)}%
      </div>
    </div>
  );
}

// ── page ──────────────────────────────────────────────────────────────────────
export default function ForcedLaborEnginePage() {
  const [entities, setEntities]   = useState<ForcedLaborEntity[]>([]);
  const [summary, setSummary]     = useState<Summary | null>(null);
  const [loading, setLoading]     = useState(true);
  const [selected, setSelected]   = useState<ForcedLaborEntity | null>(null);
  const [filterRisk,    setFilterRisk]    = useState("all");
  const [filterPattern, setFilterPattern] = useState("all");

  useEffect(() => {
    setLoading(true);
    const params = new URLSearchParams();
    if (filterRisk    !== "all") params.set("risk",    filterRisk);
    if (filterPattern !== "all") params.set("pattern", filterPattern);
    fetch(`/api/forced-labor-engine?${params}`)
      .then((r) => r.json())
      .then((data) => {
        setEntities(data.entities);
        setSummary(data.summary);
        setLoading(false);
      });
  }, [filterRisk, filterPattern]);

  const avgExploitation  = entities.length ? Math.round(entities.reduce((a, e) => a + e.exploitation_score, 0)  / entities.length * 10) / 10 : 0;
  const avgDetection     = entities.length ? Math.round(entities.reduce((a, e) => a + e.detection_score, 0)     / entities.length * 10) / 10 : 0;
  const avgImpunity      = entities.length ? Math.round(entities.reduce((a, e) => a + e.impunity_score, 0)      / entities.length * 10) / 10 : 0;
  const avgVulnerability = entities.length ? Math.round(entities.reduce((a, e) => a + e.vulnerability_score, 0) / entities.length * 10) / 10 : 0;

  const distributions: Array<{ title: string; counts: Record<string, number>; colors: Record<string, string> }> = [
    {
      title: "Patterns Travail Forcé",
      counts: summary?.pattern_distribution ?? {},
      colors: {
        supply_chain_slavery_nexus: "bg-red-600",
        debt_bondage_trap:          "bg-red-500",
        domestic_servitude_network: "bg-red-400",
        sex_trafficking_economy:    "bg-red-300",
        prison_labor_exploitation:  "bg-slate-500",
      },
    },
    {
      title: "Distribution du Risque",
      counts: summary?.risk_distribution ?? {},
      colors: { critical: "bg-red-500", high: "bg-red-400", moderate: "bg-slate-500", low: "bg-slate-600" },
    },
    {
      title: "Sévérité Esclavage Moderne",
      counts: summary?.severity_distribution ?? {},
      colors: {
        "crise_esclavage_moderne_systémique":       "bg-red-600",
        "exploitation_grave_travail_forcé":         "bg-red-400",
        "vulnérabilité_structurelle_travail_forcé": "bg-slate-500",
        "surveillance_travail_forcé_active":        "bg-slate-600",
      },
    },
    {
      title: "Actions Prescrites",
      counts: summary?.action_distribution ?? {},
      colors: {
        intervention_urgente_esclavage_moderne_critique:      "bg-red-600",
        renforcement_protection_victimes_travail_forcé:       "bg-red-400",
        "surveillance_renforcée_chaînes_approvisionnement":   "bg-slate-500",
        "veille_travail_forcé_continue":                      "bg-slate-600",
      },
    },
  ];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
      <div className="max-w-6xl mx-auto space-y-6">

        {/* header */}
        <div>
          <h1 className="text-2xl font-bold text-white">Travail Forcé & Esclavage Moderne — Module 418</h1>
          <p className="text-slate-400 text-sm mt-1">
            Détection et analyse de l&apos;esclavage moderne, du travail forcé et des réseaux de traite humaine —
            évaluation des chaînes d&apos;approvisionnement, de la servitude par la dette et des mécanismes
            d&apos;impunité à l&apos;échelle mondiale.
          </p>
        </div>

        {/* KPI strip — 6 cards */}
        {summary && (
          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
            {[
              { label: "Entités Analysées",    value: summary.total },
              { label: "Composite Moyen",       value: summary.avg_composite.toFixed(1),                    color: "text-red-400" },
              { label: "Critique",             value: summary.critical,                                     color: "text-red-500" },
              { label: "Élevé",                value: summary.high,                                         color: "text-red-300" },
              { label: "Indice Travail Forcé",  value: summary.avg_estimated_forced_labor_index.toFixed(2),  color: "text-red-200" },
              { label: "Modéré + Faible",       value: summary.moderate + summary.low,                      color: "text-slate-400" },
            ].map(({ label, value, color }) => (
              <div key={label} className="bg-slate-900 border border-red-500/30 rounded-xl p-4">
                <div className="text-xs text-slate-400">{label}</div>
                <div className={`text-2xl font-bold mt-1 ${color ?? "text-white"}`}>{value}</div>
              </div>
            ))}
          </div>
        )}

        {/* 4 GaugeRings */}
        {entities.length > 0 && (
          <div className="bg-slate-900 border border-red-500/30 rounded-xl p-5">
            <div className="text-sm font-semibold text-slate-300 mb-4">Dimensions de l&apos;Esclavage Moderne</div>
            <div className="flex flex-wrap gap-6 justify-around">
              <GaugeRing score={avgExploitation}  label="Exploitation"  color="#ef4444" />
              <GaugeRing score={avgDetection}     label="Détection"     color="#f87171" />
              <GaugeRing score={avgImpunity}      label="Impunité"      color="#94a3b8" />
              <GaugeRing score={avgVulnerability} label="Vulnérabilité" color="#fca5a5" />
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
            { label: "Tous",        val: "all" },
            { label: "🔴 Critique", val: "critical" },
            { label: "🟠 Élevé",    val: "high" },
            { label: "🟡 Modéré",   val: "moderate" },
            { label: "🟢 Faible",   val: "low" },
          ].map(({ label, val }) => (
            <button
              key={val}
              onClick={() => setFilterRisk(val)}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
                filterRisk === val
                  ? "bg-red-700 text-white"
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
            {[
              "supply_chain_slavery_nexus",
              "debt_bondage_trap",
              "domestic_servitude_network",
              "sex_trafficking_economy",
              "prison_labor_exploitation",
            ].map((p) => (
              <option key={p} value={p}>{p.replace(/_/g, " ")}</option>
            ))}
          </select>
        </div>

        {/* entity cards grid */}
        {loading ? (
          <div className="text-slate-400 text-center py-16">Analyse du travail forcé en cours…</div>
        ) : entities.length === 0 ? (
          <div className="text-slate-500 text-center py-16">Aucune entité ne correspond aux filtres.</div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {entities.map((entity) => (
              <EntityCard key={entity.entity_id} entity={entity} onClick={() => setSelected(entity)} />
            ))}
          </div>
        )}
      </div>

      {selected && <DetailModal entity={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
