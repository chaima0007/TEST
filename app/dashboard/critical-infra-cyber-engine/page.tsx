"use client";

import { useEffect, useState } from "react";

// ── Types ─────────────────────────────────────────────────────────────────────

interface CyberEntity {
  entity_id: string;
  name: string;
  country: string;
  sector: string;
  composite_score: number;
  vulnerability_score: number;
  threat_actor_score: number;
  incident_frequency_score: number;
  recovery_gap_score: number;
  risk_level: string;
  primary_pattern: string;
  key_signals: string[];
  estimated_cyber_index: number;
  last_updated: string;
}

interface CyberSummary {
  total_entities: number;
  avg_composite: number;
  risk_distribution: Record<string, number>;
  pattern_distribution: Record<string, number>;
  top_risk_entities: string[];
  critical_alerts: number;
  last_analysis: string;
  engine_version: string;
  domain: string;
  confidence_score: number;
  data_sources: string[];
  entities: CyberEntity[];
  avg_estimated_cyber_index: number;
}

interface ApiResponse {
  entities: CyberEntity[];
  summary: CyberSummary;
}

// ── Pattern action map ────────────────────────────────────────────────────────

const PATTERN_ACTIONS: Record<string, string> = {
  "Intrusion APT Étatique": "Isolation réseau immédiate et intervention CERT national",
  "Vulnérabilité Infrastructure SCADA": "Patch d'urgence systèmes OT/SCADA et segmentation réseau",
  "Ransomware Infrastructure Critique": "Plan de continuité activé et négociation cybercriminelle évitée",
  "Déficit Résilience Cyber": "Exercice Red Team et mise à jour plan de reprise d'activité",
  "Exposition Chaîne Fournisseurs": "Audit tiers fournisseurs et renforcement contrats cybersécurité",
};

// ── Colour helpers ────────────────────────────────────────────────────────────

function riskColour(level: string): string {
  switch (level) {
    case "critique": return "text-red-400";
    case "élevé":   return "text-orange-400";
    case "modéré":  return "text-yellow-400";
    default:        return "text-emerald-400";
  }
}

function riskBg(level: string): string {
  switch (level) {
    case "critique": return "bg-red-500/20 text-red-300 border border-red-500/40";
    case "élevé":   return "bg-orange-500/20 text-orange-300 border border-orange-500/40";
    case "modéré":  return "bg-yellow-500/20 text-yellow-300 border border-yellow-500/40";
    default:        return "bg-emerald-500/20 text-emerald-300 border border-emerald-500/40";
  }
}

function scoreColour(score: number): string {
  if (score >= 60) return "#f87171";
  if (score >= 40) return "#fb923c";
  if (score >= 20) return "#facc15";
  return "#34d399";
}

// ── GaugeRing (inline SVG) ────────────────────────────────────────────────────

function GaugeRing({
  label,
  value,
  max = 100,
}: {
  label: string;
  value: number;
  max?: number;
}) {
  const radius = 36;
  const circumference = 2 * Math.PI * radius;
  const pct = Math.min(value / max, 1);
  const offset = circumference * (1 - pct);
  const colour = scoreColour(value);

  return (
    <div className="flex flex-col items-center gap-2">
      <svg width="96" height="96" viewBox="0 0 96 96">
        <circle cx="48" cy="48" r={radius} fill="none" stroke="#1e293b" strokeWidth="8" />
        <circle
          cx="48"
          cy="48"
          r={radius}
          fill="none"
          stroke={colour}
          strokeWidth="8"
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          strokeLinecap="round"
          transform="rotate(-90 48 48)"
        />
        <text x="48" y="53" textAnchor="middle" fontSize="16" fontWeight="700" fill={colour}>
          {value.toFixed(0)}
        </text>
      </svg>
      <span className="text-xs text-slate-400 text-center leading-tight max-w-[96px]">{label}</span>
    </div>
  );
}

// ── DistBar (inline) ──────────────────────────────────────────────────────────

function DistBar({
  title,
  data,
}: {
  title: string;
  data: Record<string, number>;
}) {
  const total = Object.values(data).reduce((a, b) => a + b, 0);
  const colours = [
    "#f87171", "#fb923c", "#facc15", "#34d399",
    "#60a5fa", "#a78bfa", "#f472b6", "#94a3b8",
  ];

  return (
    <div className="bg-slate-900 rounded-xl p-4 border border-slate-800">
      <h3 className="text-sm font-semibold text-slate-300 mb-3">{title}</h3>
      <div className="flex h-3 rounded-full overflow-hidden mb-3">
        {Object.entries(data).map(([key, val], i) => (
          <div
            key={key}
            style={{ width: `${(val / total) * 100}%`, backgroundColor: colours[i % colours.length] }}
            title={`${key}: ${val}`}
          />
        ))}
      </div>
      <div className="space-y-1">
        {Object.entries(data).map(([key, val], i) => (
          <div key={key} className="flex items-center justify-between text-xs">
            <div className="flex items-center gap-2">
              <span
                className="inline-block w-2 h-2 rounded-full"
                style={{ backgroundColor: colours[i % colours.length] }}
              />
              <span className="text-slate-400 truncate max-w-[160px]">{key}</span>
            </div>
            <span className="text-slate-200 font-medium">{val}</span>
          </div>
        ))}
      </div>
    </div>
  );
}

// ── KPI Card ──────────────────────────────────────────────────────────────────

function KpiCard({
  label,
  value,
  sub,
  accent,
}: {
  label: string;
  value: string | number;
  sub?: string;
  accent?: string;
}) {
  return (
    <div className="bg-slate-900 rounded-xl p-4 border border-slate-800 flex flex-col gap-1">
      <span className="text-xs text-slate-500 uppercase tracking-wide">{label}</span>
      <span className={`text-2xl font-bold ${accent ?? "text-white"}`}>{value}</span>
      {sub && <span className="text-xs text-slate-500">{sub}</span>}
    </div>
  );
}

// ── Detail Modal ──────────────────────────────────────────────────────────────

function DetailModal({
  entity,
  onClose,
}: {
  entity: CyberEntity;
  onClose: () => void;
}) {
  const [tab, setTab] = useState<"scores" | "signaux" | "actions">("scores");

  const subScores = [
    { label: "Vulnérabilité (CVE / surface)", key: "vulnerability_score", weight: "30%" },
    { label: "Acteurs de menace (APT)", key: "threat_actor_score", weight: "25%" },
    { label: "Fréquence d'incidents", key: "incident_frequency_score", weight: "25%" },
    { label: "Déficit de reprise", key: "recovery_gap_score", weight: "20%" },
  ] as const;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm p-4">
      <div className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-lg max-h-[90vh] overflow-y-auto shadow-2xl">
        {/* Header */}
        <div className="flex items-start justify-between p-6 border-b border-slate-800">
          <div>
            <span className={`inline-block text-xs px-2 py-0.5 rounded-full mb-2 ${riskBg(entity.risk_level)}`}>
              {entity.risk_level.toUpperCase()}
            </span>
            <h2 className="text-lg font-bold text-white">{entity.name}</h2>
            <p className="text-sm text-slate-400">{entity.sector} — {entity.country}</p>
          </div>
          <button
            onClick={onClose}
            className="text-slate-500 hover:text-white transition-colors text-xl font-bold ml-4"
          >
            ×
          </button>
        </div>

        {/* Composite score */}
        <div className="px-6 py-4 bg-slate-950/50 flex items-center gap-4">
          <div className="flex flex-col">
            <span className="text-xs text-slate-500">Score composite</span>
            <span className={`text-3xl font-bold ${riskColour(entity.risk_level)}`}>
              {entity.composite_score.toFixed(2)}
            </span>
          </div>
          <div className="flex flex-col">
            <span className="text-xs text-slate-500">Index Cyber</span>
            <span className="text-xl font-bold text-cyan-400">{entity.estimated_cyber_index.toFixed(2)}</span>
          </div>
          <div className="ml-auto text-right">
            <span className="text-xs text-slate-500 block">Dernière MAJ</span>
            <span className="text-xs text-slate-300">{entity.last_updated}</span>
          </div>
        </div>

        {/* Tabs */}
        <div className="flex border-b border-slate-800">
          {(["scores", "signaux", "actions"] as const).map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`flex-1 py-3 text-sm font-medium capitalize transition-colors ${
                tab === t
                  ? "text-cyan-400 border-b-2 border-cyan-400"
                  : "text-slate-500 hover:text-slate-300"
              }`}
            >
              {t === "scores" ? "Scores" : t === "signaux" ? "Signaux" : "Actions"}
            </button>
          ))}
        </div>

        {/* Tab content */}
        <div className="p-6">
          {tab === "scores" && (
            <div className="space-y-4">
              {subScores.map(({ label, key, weight }) => {
                const val = entity[key] as number;
                return (
                  <div key={key}>
                    <div className="flex justify-between text-xs mb-1">
                      <span className="text-slate-400">{label}</span>
                      <span className="text-slate-300 font-medium">
                        {val.toFixed(1)} <span className="text-slate-600">({weight})</span>
                      </span>
                    </div>
                    <div className="h-2 bg-slate-800 rounded-full overflow-hidden">
                      <div
                        className="h-full rounded-full transition-all"
                        style={{
                          width: `${val}%`,
                          backgroundColor: scoreColour(val),
                        }}
                      />
                    </div>
                  </div>
                );
              })}
            </div>
          )}

          {tab === "signaux" && (
            <ul className="space-y-3">
              {entity.key_signals.map((signal, i) => (
                <li key={i} className="flex items-start gap-3">
                  <span className="mt-0.5 w-5 h-5 flex-shrink-0 rounded-full bg-cyan-500/20 text-cyan-400 text-xs flex items-center justify-center font-bold">
                    {i + 1}
                  </span>
                  <span className="text-sm text-slate-300">{signal}</span>
                </li>
              ))}
            </ul>
          )}

          {tab === "actions" && (
            <div className="space-y-4">
              <div className="bg-slate-800/60 rounded-xl p-4 border border-slate-700">
                <p className="text-xs text-slate-500 mb-1">Pattern détecté</p>
                <p className="text-sm font-semibold text-cyan-300">{entity.primary_pattern}</p>
              </div>
              <div className="bg-slate-800/60 rounded-xl p-4 border border-slate-700">
                <p className="text-xs text-slate-500 mb-2">Action recommandée</p>
                <p className="text-sm text-slate-200 leading-relaxed">
                  {PATTERN_ACTIONS[entity.primary_pattern] ?? "Consulter l'équipe CERT"}
                </p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

// ── Main Page ─────────────────────────────────────────────────────────────────

export default function CriticalInfraCyberPage() {
  const [data, setData] = useState<ApiResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filter, setFilter] = useState<string>("all");
  const [selected, setSelected] = useState<CyberEntity | null>(null);

  useEffect(() => {
    fetch("/api/critical-infra-cyber-engine")
      .then((r) => {
        if (!r.ok) throw new Error(`HTTP ${r.status}`);
        return r.json();
      })
      .then((json) => {
        setData(json);
        setLoading(false);
      })
      .catch((e: Error) => {
        setError(e.message);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center">
        <div className="text-slate-400 animate-pulse text-sm">Chargement des données cyber...</div>
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center">
        <div className="text-red-400 text-sm">Erreur: {error ?? "Données indisponibles"}</div>
      </div>
    );
  }

  const { summary } = data;
  const entities = summary.entities;

  // Filter
  const filtered =
    filter === "all" ? entities : entities.filter((e) => e.risk_level === filter);

  // Averages for gauges
  const avgVulnerability =
    Math.round(entities.reduce((a, e) => a + e.vulnerability_score, 0) / entities.length * 10) / 10;
  const avgThreatActor =
    Math.round(entities.reduce((a, e) => a + e.threat_actor_score, 0) / entities.length * 10) / 10;
  const avgIncidentFreq =
    Math.round(entities.reduce((a, e) => a + e.incident_frequency_score, 0) / entities.length * 10) / 10;
  const avgRecoveryGap =
    Math.round(entities.reduce((a, e) => a + e.recovery_gap_score, 0) / entities.length * 10) / 10;

  // Sector distribution
  const sectorDist: Record<string, number> = {};
  for (const e of entities) {
    sectorDist[e.sector] = (sectorDist[e.sector] ?? 0) + 1;
  }

  // Country distribution
  const countryDist: Record<string, number> = {};
  for (const e of entities) {
    countryDist[e.country] = (countryDist[e.country] ?? 0) + 1;
  }

  // APT count (entities where threat_actor_score > 70)
  const aptActive = entities.filter((e) => e.threat_actor_score > 70).length;

  const RISK_FILTERS = ["all", "critique", "élevé", "modéré", "faible"];

  return (
    <div className="min-h-screen bg-slate-950 text-white">
      {/* Modal */}
      {selected && (
        <DetailModal entity={selected} onClose={() => setSelected(null)} />
      )}

      <div className="max-w-7xl mx-auto px-4 py-8 space-y-8">
        {/* Header */}
        <div className="flex items-start justify-between">
          <div>
            <h1 className="text-3xl font-bold text-white tracking-tight">
              Critical Infrastructure Cyber Intelligence
            </h1>
            <p className="mt-1 text-slate-400 text-sm">
              Surveillance des cybermenaces sur infrastructures critiques
            </p>
          </div>
          <div className="text-right text-xs text-slate-600">
            <p>Analyse: {summary.last_analysis}</p>
            <p>v{summary.engine_version} · Confiance {(summary.confidence_score * 100).toFixed(0)}%</p>
          </div>
        </div>

        {/* 6 KPI Cards */}
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
          <KpiCard
            label="Total Entités"
            value={summary.total_entities}
            sub={`Domaine: ${summary.domain}`}
          />
          <KpiCard
            label="Alertes Critiques"
            value={summary.critical_alerts}
            sub="Niveau critique"
            accent="text-red-400"
          />
          <KpiCard
            label="Score Cyber Moyen"
            value={summary.avg_composite.toFixed(1)}
            sub="Sur 100"
            accent={riskColour(
              summary.avg_composite >= 60
                ? "critique"
                : summary.avg_composite >= 40
                ? "élevé"
                : summary.avg_composite >= 20
                ? "modéré"
                : "faible"
            )}
          />
          <KpiCard
            label="Index Cyber Moyen"
            value={summary.avg_estimated_cyber_index.toFixed(2)}
            sub="Sur 10"
            accent="text-cyan-400"
          />
          <KpiCard
            label="APT Actifs"
            value={aptActive}
            sub="Score menace > 70"
            accent="text-purple-400"
          />
          <KpiCard
            label="Sources Analysées"
            value={summary.data_sources.length}
            sub="Renseignements cyber"
            accent="text-blue-400"
          />
        </div>

        {/* 4 GaugeRings */}
        <div className="bg-slate-900 rounded-xl p-6 border border-slate-800">
          <h2 className="text-sm font-semibold text-slate-300 mb-6">
            Scores Moyens par Dimension
          </h2>
          <div className="flex flex-wrap justify-around gap-6">
            <GaugeRing label="Vulnérabilité (CVE)" value={avgVulnerability} />
            <GaugeRing label="Acteurs de Menace (APT)" value={avgThreatActor} />
            <GaugeRing label="Fréquence d'Incidents" value={avgIncidentFreq} />
            <GaugeRing label="Déficit de Reprise" value={avgRecoveryGap} />
          </div>
        </div>

        {/* 4 DistBars */}
        <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4">
          <DistBar title="Distribution des Risques" data={summary.risk_distribution} />
          <DistBar title="Distribution des Patterns" data={summary.pattern_distribution} />
          <DistBar title="Distribution Sectorielle" data={sectorDist} />
          <DistBar title="Distribution Géographique" data={countryDist} />
        </div>

        {/* Filter pills */}
        <div className="flex flex-wrap gap-2">
          {RISK_FILTERS.map((f) => (
            <button
              key={f}
              onClick={() => setFilter(f)}
              className={`px-4 py-1.5 rounded-full text-xs font-medium transition-colors ${
                filter === f
                  ? "bg-cyan-600 text-white"
                  : "bg-slate-800 text-slate-400 hover:bg-slate-700 hover:text-white"
              }`}
            >
              {f === "all"
                ? `Tous (${entities.length})`
                : `${f} (${entities.filter((e) => e.risk_level === f).length})`}
            </button>
          ))}
        </div>

        {/* Entity cards grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          {filtered.map((entity) => (
            <button
              key={entity.entity_id}
              onClick={() => setSelected(entity)}
              className="bg-slate-900 border border-slate-800 rounded-xl p-4 text-left hover:border-slate-600 hover:bg-slate-800/80 transition-all group"
            >
              {/* Risk badge + ID */}
              <div className="flex items-center justify-between mb-3">
                <span
                  className={`text-xs px-2 py-0.5 rounded-full font-medium ${riskBg(entity.risk_level)}`}
                >
                  {entity.risk_level}
                </span>
                <span className="text-xs text-slate-600 font-mono">{entity.entity_id}</span>
              </div>

              {/* Name */}
              <h3 className="font-semibold text-white text-sm leading-tight group-hover:text-cyan-300 transition-colors">
                {entity.name}
              </h3>
              <p className="text-xs text-slate-500 mt-0.5">
                {entity.sector} · {entity.country}
              </p>

              {/* Composite score bar */}
              <div className="mt-3">
                <div className="flex justify-between text-xs mb-1">
                  <span className="text-slate-500">Score composite</span>
                  <span className={`font-bold ${riskColour(entity.risk_level)}`}>
                    {entity.composite_score.toFixed(1)}
                  </span>
                </div>
                <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
                  <div
                    className="h-full rounded-full"
                    style={{
                      width: `${entity.composite_score}%`,
                      backgroundColor: scoreColour(entity.composite_score),
                    }}
                  />
                </div>
              </div>

              {/* Primary pattern */}
              <div className="mt-3 text-xs text-slate-400 bg-slate-800/60 rounded-lg px-2 py-1.5 leading-tight">
                {entity.primary_pattern}
              </div>

              {/* Key signals */}
              <ul className="mt-2 space-y-1">
                {entity.key_signals.map((sig, i) => (
                  <li key={i} className="flex items-start gap-1.5 text-xs text-slate-500">
                    <span className="mt-0.5 text-cyan-600 flex-shrink-0">›</span>
                    <span className="leading-tight">{sig}</span>
                  </li>
                ))}
              </ul>

              {/* Index cyber */}
              <div className="mt-3 pt-3 border-t border-slate-800 flex justify-between text-xs">
                <span className="text-slate-600">Index Cyber</span>
                <span className="text-cyan-400 font-semibold">
                  {entity.estimated_cyber_index.toFixed(2)} / 10
                </span>
              </div>
            </button>
          ))}
        </div>

        {/* Data sources footer */}
        <div className="bg-slate-900/50 rounded-xl p-4 border border-slate-800">
          <p className="text-xs text-slate-500 mb-2 font-medium uppercase tracking-wide">
            Sources de renseignement
          </p>
          <div className="flex flex-wrap gap-2">
            {summary.data_sources.map((src) => (
              <span
                key={src}
                className="text-xs bg-slate-800 text-slate-400 px-3 py-1 rounded-full"
              >
                {src}
              </span>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
