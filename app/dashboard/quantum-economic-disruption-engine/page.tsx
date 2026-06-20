"use client";
import { useEffect, useState } from "react";

// ── Types ─────────────────────────────────────────────────────────────────────

type RiskLevel = "critique" | "élevé" | "modéré" | "faible";
type QuantumPattern =
  | "cryptographic_collapse"
  | "economic_disruption_cascade"
  | "quantum_readiness_gap"
  | "geopolitical_quantum_race"
  | "quantum_stable";

interface QedEntity {
  entity_id: string;
  name: string;
  country: string;
  sector: string;
  composite_score: number;
  cryptographic_vulnerability_score: number;
  economic_disruption_score: number;
  quantum_readiness_gap_score: number;
  geopolitical_exposure_score: number;
  risk_level: RiskLevel;
  primary_pattern: QuantumPattern;
  key_signals: string[];
  estimated_quantum_index: number;
  last_updated: string;
  confidence_level: number;
}

interface QedSummary {
  total_entities: number;
  avg_composite: number;
  risk_distribution: Record<string, number>;
  pattern_distribution: Record<string, number>;
  top_risk_entities: string[];
  critical_alerts: string[];
  last_analysis: string;
  engine_version: string;
  domain: string;
  confidence_score: number;
  data_sources: string[];
  entities: QedEntity[];
  avg_estimated_quantum_index: number;
}

// ── Metadata ──────────────────────────────────────────────────────────────────

const RISK_META: Record<RiskLevel, { label: string; color: string; ring: string; badge: string }> = {
  critique: { label: "Critique",      color: "text-red-400",     ring: "#ef4444", badge: "bg-red-900/60 text-red-300 border-red-700" },
  "élevé":  { label: "Élevé",         color: "text-orange-400",  ring: "#f97316", badge: "bg-orange-900/60 text-orange-300 border-orange-700" },
  "modéré": { label: "Modéré",        color: "text-amber-400",   ring: "#f59e0b", badge: "bg-amber-900/60 text-amber-300 border-amber-700" },
  faible:   { label: "Faible",        color: "text-emerald-400", ring: "#10b981", badge: "bg-emerald-900/60 text-emerald-300 border-emerald-700" },
};

const PATTERN_LABELS: Record<QuantumPattern, string> = {
  cryptographic_collapse:      "Effondrement Cryptographique",
  economic_disruption_cascade: "Cascade de Perturbation Économique",
  quantum_readiness_gap:       "Fossé de Préparation Quantique",
  geopolitical_quantum_race:   "Course Quantique Géopolitique",
  quantum_stable:              "Stabilité Quantique",
};

const PATTERN_ACTIONS: Record<QuantumPattern, string> = {
  cryptographic_collapse:      "Migration urgente vers cryptographie post-quantique",
  economic_disruption_cascade: "Plan de résilience économique quantique prioritaire",
  quantum_readiness_gap:       "Programme d'adoption quantique accéléré",
  geopolitical_quantum_race:   "Alignement stratégique sur les alliances quantiques",
  quantum_stable:              "Maintien de la veille quantique proactive",
};

const RISK_COLORS: Record<string, string> = {
  critique: "#ef4444",
  "élevé":  "#f97316",
  "modéré": "#f59e0b",
  faible:   "#10b981",
};

const PAT_COLORS: Record<string, string> = {
  cryptographic_collapse:      "#ef4444",
  economic_disruption_cascade: "#f97316",
  quantum_readiness_gap:       "#a855f7",
  geopolitical_quantum_race:   "#3b82f6",
  quantum_stable:              "#10b981",
};

// ── GaugeRing ─────────────────────────────────────────────────────────────────

function GaugeRing({ value, label, color }: { value: number; label: string; color: string }) {
  const r = 28;
  const circ = 2 * Math.PI * r;
  const dash = (value / 100) * circ;
  return (
    <div className="flex flex-col items-center gap-1">
      <svg width="72" height="72" viewBox="0 0 72 72">
        <circle cx="36" cy="36" r={r} fill="none" stroke="#1e293b" strokeWidth="7" />
        <circle
          cx="36" cy="36" r={r} fill="none"
          stroke={color} strokeWidth="7"
          strokeDasharray={`${dash} ${circ}`}
          strokeLinecap="round"
          transform="rotate(-90 36 36)"
        />
        <text x="36" y="40" textAnchor="middle" fill="white" fontSize="13" fontWeight="bold">
          {value.toFixed(0)}
        </text>
      </svg>
      <span className="text-xs text-stone-400 text-center leading-tight">{label}</span>
    </div>
  );
}

// ── DistBar ───────────────────────────────────────────────────────────────────

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
    <div>
      <p className="text-xs text-stone-500 font-medium mb-2">{title}</p>
      <div className="space-y-1.5">
        {Object.entries(counts).map(([key, count]) => (
          <div key={key} className="flex items-center gap-2 text-xs">
            <span className="w-36 text-stone-400 truncate capitalize">{key.replace(/_/g, " ")}</span>
            <div className="flex-1 h-2 bg-slate-800 rounded-full overflow-hidden">
              <div
                className="h-2 rounded-full"
                style={{
                  width: `${(count / total) * 100}%`,
                  background: colors[key] || "#6b7280",
                }}
              />
            </div>
            <span className="text-stone-300 w-4 text-right">{count}</span>
          </div>
        ))}
      </div>
    </div>
  );
}

// ── DetailModal ───────────────────────────────────────────────────────────────

function DetailModal({ entity, onClose }: { entity: QedEntity; onClose: () => void }) {
  const [tab, setTab] = useState<"scores" | "signaux" | "actions">("scores");
  const risk = RISK_META[entity.risk_level];

  return (
    <div
      className="fixed inset-0 bg-black/70 backdrop-blur-sm z-50 flex items-center justify-center p-4"
      onClick={onClose}
    >
      <div
        className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-lg shadow-2xl"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="p-5 border-b border-slate-800">
          <div className="flex items-start justify-between">
            <div>
              <div className="flex items-center gap-2 mb-1">
                <span className="text-xs text-stone-500 font-mono">{entity.entity_id}</span>
                <span
                  className={`px-2 py-0.5 rounded text-xs font-medium border ${risk?.badge || "bg-slate-700 text-stone-300"}`}
                >
                  {entity.risk_level}
                </span>
              </div>
              <h2 className="text-white font-bold text-lg leading-tight">{entity.name}</h2>
              <p className="text-stone-400 text-sm mt-0.5">
                {entity.country} · {entity.sector}
              </p>
            </div>
            <button
              onClick={onClose}
              className="text-stone-500 hover:text-white text-xl leading-none ml-4"
            >
              ×
            </button>
          </div>
          <div className="flex gap-1 mt-3">
            {(["scores", "signaux", "actions"] as const).map((t) => (
              <button
                key={t}
                onClick={() => setTab(t)}
                className={`px-3 py-1 rounded-full text-xs font-medium transition-colors capitalize ${
                  tab === t
                    ? "bg-violet-700 text-white"
                    : "bg-slate-800 text-stone-400 hover:text-white"
                }`}
              >
                {t === "scores" ? "Scores" : t === "signaux" ? "Signaux" : "Actions"}
              </button>
            ))}
          </div>
        </div>

        {/* Body */}
        <div className="p-5">
          {tab === "scores" && (
            <div className="grid grid-cols-2 gap-3">
              {(
                [
                  ["Vulnérabilité Cryptographique", entity.cryptographic_vulnerability_score, "#ef4444"],
                  ["Disruption Économique",         entity.economic_disruption_score,         "#f97316"],
                  ["Fossé Préparation Quantique",   entity.quantum_readiness_gap_score,       "#a855f7"],
                  ["Exposition Géopolitique",       entity.geopolitical_exposure_score,       "#3b82f6"],
                ] as [string, number, string][]
              ).map(([l, v, c]) => (
                <div key={l} className="bg-slate-800 border border-slate-700 rounded-lg p-3">
                  <div className="text-stone-400 text-xs mb-1 leading-tight">{l}</div>
                  <div className="text-white font-bold text-lg">{v.toFixed(1)}</div>
                  <div className="h-1.5 rounded mt-1 bg-slate-700">
                    <div
                      className="h-1.5 rounded"
                      style={{ width: `${Math.min(v, 100)}%`, background: c }}
                    />
                  </div>
                </div>
              ))}
              <div className="col-span-2 bg-slate-800 border border-slate-700 rounded-lg p-3">
                <div className="text-stone-400 text-xs mb-1">Score Composite</div>
                <div className="text-white font-bold text-2xl">{entity.composite_score.toFixed(2)}</div>
                <div className="text-stone-500 text-xs mt-0.5">
                  Index Quantique: {entity.estimated_quantum_index.toFixed(2)}/10 ·{" "}
                  Confiance: {Math.round(entity.confidence_level * 100)}%
                </div>
              </div>
            </div>
          )}

          {tab === "signaux" && (
            <div className="space-y-3">
              {entity.key_signals.map((signal, i) => (
                <div
                  key={i}
                  className="bg-slate-800 border border-violet-800/30 rounded-lg p-3 flex gap-3 items-start"
                >
                  <span className="text-violet-400 font-bold text-sm mt-0.5">{i + 1}.</span>
                  <p className="text-slate-200 text-sm leading-relaxed">{signal}</p>
                </div>
              ))}
              <div className="bg-slate-800 border border-slate-700 rounded-lg p-3 mt-2">
                <div className="text-stone-400 text-xs mb-1">Patron Principal</div>
                <div className="text-white font-medium text-sm">
                  {PATTERN_LABELS[entity.primary_pattern] || entity.primary_pattern.replace(/_/g, " ")}
                </div>
              </div>
              <div className="text-xs text-stone-600 text-right">Dernière mise à jour: {entity.last_updated}</div>
            </div>
          )}

          {tab === "actions" && (
            <div className="space-y-3 text-sm">
              <div className="bg-slate-800 border border-violet-800/30 rounded-lg p-4">
                <div className="text-stone-400 text-xs mb-2">Action Recommandée</div>
                <div className="text-white font-medium leading-relaxed">
                  {PATTERN_ACTIONS[entity.primary_pattern]}
                </div>
              </div>
              <div className="bg-slate-800 border border-slate-700 rounded-lg p-3">
                <div className="text-stone-400 text-xs mb-1">Patron de Disruption</div>
                <div className="text-violet-300 font-medium">
                  {PATTERN_LABELS[entity.primary_pattern] || entity.primary_pattern.replace(/_/g, " ")}
                </div>
              </div>
              <div className="bg-slate-800 border border-slate-700 rounded-lg p-3">
                <div className="text-stone-400 text-xs mb-1">Niveau de Confiance</div>
                <div className="flex items-center gap-2">
                  <div className="flex-1 h-2 bg-slate-700 rounded-full overflow-hidden">
                    <div
                      className="h-2 rounded-full bg-violet-500"
                      style={{ width: `${entity.confidence_level * 100}%` }}
                    />
                  </div>
                  <span className="text-white font-bold text-sm">
                    {Math.round(entity.confidence_level * 100)}%
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

// ── Dashboard ─────────────────────────────────────────────────────────────────

export default function QuantumEconomicDisruptionDashboard() {
  const [data, setData] = useState<{ entities: QedEntity[]; summary: QedSummary } | null>(null);
  const [riskFilter, setRiskFilter] = useState<string>("tous");
  const [selected, setSelected] = useState<QedEntity | null>(null);

  useEffect(() => {
    fetch("/api/quantum-economic-disruption-engine")
      .then((r) => r.json())
      .then(setData)
      .catch(console.error);
  }, []);

  if (!data) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center">
        <div className="text-violet-400 text-lg animate-pulse">
          Initialisation du Moteur Quantum Economic Disruption — Caelum Partners...
        </div>
      </div>
    );
  }

  const { entities, summary } = data;

  const filtered = entities.filter(
    (e) => riskFilter === "tous" || e.risk_level === riskFilter
  );

  return (
    <div className="min-h-screen bg-slate-950 text-stone-300 p-6 space-y-6">
      {selected && <DetailModal entity={selected} onClose={() => setSelected(null)} />}

      {/* En-tête */}
      <div>
        <h1 className="text-2xl font-bold text-violet-400">
          Quantum Economic Disruption Intelligence Engine
        </h1>
        <p className="text-stone-400 text-sm mt-1">
          Cryptographie · Disruption Économique · Préparation Quantique · Géopolitique — Caelum Partners
        </p>
        <p className="text-stone-500 text-xs mt-0.5">Chaima Mhadbi — Bruxelles</p>
      </div>

      {/* KPI Cards — 6 cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {(
          [
            ["Total Entités",          summary.total_entities,                                      "text-stone-300"],
            ["Niveau Critique",        summary.risk_distribution["critique"] ?? 0,                  "text-red-400"],
            ["Niveau Élevé",           summary.risk_distribution["élevé"] ?? 0,                     "text-orange-400"],
            ["Composite Moyen",        summary.avg_composite.toFixed(1),                            "text-violet-300"],
            ["Index Quantique Moyen",  summary.avg_estimated_quantum_index.toFixed(2) + "/10",      "text-blue-300"],
            ["Confiance Globale",      Math.round(summary.confidence_score * 100) + "%",            "text-emerald-400"],
          ] as [string, string | number, string][]
        ).map(([l, v, c]) => (
          <div key={String(l)} className="bg-slate-900 border border-violet-800/30 rounded-xl p-3 text-center">
            <div className={`text-xl font-bold ${c}`}>{v}</div>
            <div className="text-xs text-stone-500 mt-0.5 leading-tight">{l}</div>
          </div>
        ))}
      </div>

      {/* Gauge Rings */}
      <div className="bg-slate-900 border border-violet-800/30 rounded-xl p-5">
        <p className="text-xs text-stone-500 mb-4 font-medium">Scores Moyens par Dimension</p>
        <div className="grid grid-cols-4 gap-4">
          <GaugeRing
            value={
              Math.round(
                (entities.reduce((s, e) => s + e.cryptographic_vulnerability_score, 0) /
                  entities.length) *
                  10
              ) / 10
            }
            label="Vulnérabilité Crypto"
            color="#ef4444"
          />
          <GaugeRing
            value={
              Math.round(
                (entities.reduce((s, e) => s + e.economic_disruption_score, 0) / entities.length) * 10
              ) / 10
            }
            label="Disruption Économique"
            color="#f97316"
          />
          <GaugeRing
            value={
              Math.round(
                (entities.reduce((s, e) => s + e.quantum_readiness_gap_score, 0) / entities.length) * 10
              ) / 10
            }
            label="Fossé Préparation"
            color="#a855f7"
          />
          <GaugeRing
            value={
              Math.round(
                (entities.reduce((s, e) => s + e.geopolitical_exposure_score, 0) / entities.length) * 10
              ) / 10
            }
            label="Exposition Géopolitique"
            color="#3b82f6"
          />
        </div>
      </div>

      {/* Distribution Bars */}
      <div className="bg-slate-900 border border-violet-800/30 rounded-xl p-5 grid grid-cols-1 md:grid-cols-2 gap-5">
        <DistBar title="Niveau de Risque" counts={summary.risk_distribution} colors={RISK_COLORS} />
        <DistBar title="Patron de Disruption" counts={summary.pattern_distribution} colors={PAT_COLORS} />
      </div>

      {/* Alertes Critiques */}
      {summary.critical_alerts.length > 0 && (
        <div className="bg-red-950/30 border border-red-800/40 rounded-xl p-4">
          <p className="text-red-400 text-xs font-semibold mb-2 uppercase tracking-wide">
            Alertes Critiques ({summary.critical_alerts.length})
          </p>
          <div className="flex flex-wrap gap-2">
            {summary.critical_alerts.map((name) => (
              <span
                key={name}
                className="px-2 py-0.5 rounded text-xs font-medium bg-red-900/50 text-red-300 border border-red-700"
              >
                {name}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Filtres */}
      <div className="flex flex-wrap gap-2">
        {(["tous", "critique", "élevé", "modéré", "faible"] as const).map((r) => (
          <button
            key={r}
            onClick={() => setRiskFilter(r)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${
              riskFilter === r
                ? "bg-violet-800 border-violet-700 text-white"
                : "bg-slate-900 border-violet-800/30 text-stone-400 hover:text-white"
            }`}
          >
            {r === "tous" ? "Tous" : r.charAt(0).toUpperCase() + r.slice(1)}
          </button>
        ))}
      </div>

      {/* Cartes Entités */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {filtered.map((e) => {
          const risk = RISK_META[e.risk_level];
          return (
            <div
              key={e.entity_id}
              onClick={() => setSelected(e)}
              className="bg-slate-900 border border-slate-800 rounded-xl p-4 cursor-pointer hover:border-violet-700/50 transition-colors"
            >
              <div className="flex items-center justify-between mb-1">
                <span className="font-bold text-white font-mono text-sm">{e.entity_id}</span>
                <span className="text-xs text-stone-500">{e.country}</span>
              </div>
              <div className="text-sm font-semibold text-stone-200 mb-0.5 leading-tight">{e.name}</div>
              <div className="text-xs text-violet-400 mb-2">{e.sector}</div>
              <div className="flex gap-1 mb-3 flex-wrap">
                <span
                  className={`px-2 py-0.5 rounded text-xs font-medium border ${risk?.badge || "bg-slate-700 text-stone-300"}`}
                >
                  {e.risk_level}
                </span>
              </div>
              <div className="text-2xl font-black text-white mb-1">{e.composite_score.toFixed(1)}</div>
              <div className="text-xs text-stone-500 mb-2">
                {PATTERN_LABELS[e.primary_pattern] || e.primary_pattern.replace(/_/g, " ")}
              </div>
              <div className="text-xs text-violet-400 font-medium mb-3">
                {PATTERN_ACTIONS[e.primary_pattern]}
              </div>
              <div className="flex gap-3 text-xs text-stone-500">
                <span>
                  Index:{" "}
                  <span className="text-violet-300">{e.estimated_quantum_index.toFixed(2)}/10</span>
                </span>
                <span>
                  Confiance:{" "}
                  <span className="text-emerald-400">{Math.round(e.confidence_level * 100)}%</span>
                </span>
              </div>
            </div>
          );
        })}
      </div>

      {/* Footer */}
      <div className="text-xs text-stone-600 flex items-center justify-between pt-2 border-t border-slate-800">
        <span>
          Sources: {summary.data_sources.join(" · ")}
        </span>
        <span>v{summary.engine_version} · {summary.last_analysis.split("T")[0]}</span>
      </div>
    </div>
  );
}
