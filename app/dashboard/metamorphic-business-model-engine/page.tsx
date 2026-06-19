"use client";
import { useEffect, useState } from "react";

type Entity = {
  entity_id: string;
  region: string;
  transformation_stage: string;
  transformation_risk: string;
  metamorphic_pattern: string;
  transformation_severity: string;
  recommended_action: string;
  stagnation_score: number;
  readiness_score: number;
  momentum_score: number;
  alignment_score: number;
  transformation_composite: number;
  is_in_metamorphic_crisis: boolean;
  requires_immediate_intervention: boolean;
  transformation_signal: string;
};

type Summary = {
  total: number;
  risk_counts: Record<string, number>;
  pattern_counts: Record<string, number>;
  severity_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_transformation_composite: number;
  metamorphic_crisis_count: number;
  immediate_intervention_count: number;
  avg_stagnation_score: number;
  avg_readiness_score: number;
  avg_momentum_score: number;
  avg_alignment_score: number;
  avg_estimated_transformation_risk_index: number;
};

type ApiResponse = {
  entities: Entity[];
  summary: Summary;
  digital_seal: Record<string, unknown>;
};

type DistBarItem = {
  title: string;
  counts: Record<string, number>;
  colors: Record<string, string>;
};

function GaugeRing({
  value,
  color,
  label,
  size = 120,
}: {
  value: number;
  color: string;
  label: string;
  size?: number;
}) {
  const r = 45;
  const circ = 2 * Math.PI * r;
  const offset = circ * (1 - value / 100);
  return (
    <div className="flex flex-col items-center gap-1">
      <svg width={size} height={size} viewBox="0 0 100 100">
        <circle cx="50" cy="50" r={r} fill="none" stroke="#1e293b" strokeWidth="10" />
        <circle
          cx="50"
          cy="50"
          r={r}
          fill="none"
          stroke={color}
          strokeWidth="10"
          strokeDasharray={circ}
          strokeDashoffset={offset}
          strokeLinecap="round"
          transform="rotate(-90 50 50)"
        />
        <text
          x="50"
          y="50"
          textAnchor="middle"
          dominantBaseline="middle"
          fill="white"
          fontSize="16"
          fontWeight="bold"
        >
          {Math.round(value)}
        </text>
      </svg>
      <span className="text-xs text-slate-400">{label}</span>
    </div>
  );
}

function DistBar({ item }: { item: DistBarItem }) {
  const total = Object.values(item.counts).reduce((a: number, b: number) => a + b, 0);
  return (
    <div className="mb-4">
      <p className="text-xs text-slate-400 mb-1">{item.title}</p>
      <div className="flex h-3 rounded-full overflow-hidden gap-0.5">
        {Object.entries(item.counts).map(([key, count]: [string, number]) => (
          <div
            key={key}
            style={{
              width: `${(count / total) * 100}%`,
              backgroundColor: item.colors[key] || "#64748b",
            }}
            title={`${key}: ${count}`}
          />
        ))}
      </div>
      <div className="flex flex-wrap gap-2 mt-1">
        {Object.entries(item.counts).map(([key, count]: [string, number]) => (
          <span key={key} className="text-xs text-slate-400">
            <span style={{ color: item.colors[key] }}>■</span> {key}: {count}
          </span>
        ))}
      </div>
    </div>
  );
}

function DetailModal({
  entity,
  onClose,
}: {
  entity: Entity;
  onClose: () => void;
}) {
  const [tab, setTab] = useState<"overview" | "scores" | "signal">("overview");

  const riskColor = (r: string): string => {
    const map: Record<string, string> = {
      critical: "text-red-400",
      high: "text-orange-400",
      moderate: "text-yellow-400",
      low: "text-green-400",
    };
    return map[r] ?? "text-slate-400";
  };

  return (
    <div className="fixed inset-0 bg-black/70 flex items-center justify-center z-50 p-4">
      <div className="bg-slate-900 border border-orange-500/30 rounded-xl max-w-lg w-full p-6">
        <div className="flex justify-between items-start mb-4">
          <div>
            <h3 className="text-amber-400 font-bold text-lg">{entity.entity_id}</h3>
            <p className="text-slate-400 text-sm">
              {entity.transformation_stage.replace(/_/g, " ")} · {entity.region}
            </p>
          </div>
          <button
            onClick={onClose}
            className="text-slate-400 hover:text-white text-xl leading-none"
          >
            ×
          </button>
        </div>

        <div className="flex gap-2 mb-4">
          {(["overview", "scores", "signal"] as const).map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`px-3 py-1 rounded text-xs font-medium ${
                tab === t
                  ? "bg-orange-500/20 text-amber-400 border border-orange-500/40"
                  : "text-slate-400 hover:text-white"
              }`}
            >
              {t.charAt(0).toUpperCase() + t.slice(1)}
            </button>
          ))}
        </div>

        {tab === "overview" && (
          <div className="space-y-2">
            <div className="flex justify-between">
              <span className="text-slate-400 text-sm">Risk</span>
              <span className={`text-sm font-medium ${riskColor(entity.transformation_risk)}`}>
                {entity.transformation_risk}
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-400 text-sm">Pattern</span>
              <span className="text-sm text-white">
                {entity.metamorphic_pattern.replace(/_/g, " ")}
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-400 text-sm">Severity</span>
              <span className="text-sm text-white">{entity.transformation_severity}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-400 text-sm">Action</span>
              <span className="text-sm text-amber-400">
                {entity.recommended_action.replace(/_/g, " ")}
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-400 text-sm">In Crisis</span>
              <span
                className={`text-sm ${
                  entity.is_in_metamorphic_crisis ? "text-red-400" : "text-green-400"
                }`}
              >
                {entity.is_in_metamorphic_crisis ? "Yes" : "No"}
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-400 text-sm">Needs Intervention</span>
              <span
                className={`text-sm ${
                  entity.requires_immediate_intervention ? "text-red-400" : "text-green-400"
                }`}
              >
                {entity.requires_immediate_intervention ? "Yes" : "No"}
              </span>
            </div>
          </div>
        )}

        {tab === "scores" && (
          <div className="space-y-3">
            {[
              { label: "Transformation Composite", value: entity.transformation_composite, color: "#f59e0b" },
              { label: "Stagnation Score", value: entity.stagnation_score, color: "#ef4444" },
              { label: "Readiness Score", value: entity.readiness_score, color: "#f97316" },
              { label: "Momentum Score", value: entity.momentum_score, color: "#3b82f6" },
              { label: "Alignment Score", value: entity.alignment_score, color: "#8b5cf6" },
            ].map(({ label, value, color }: { label: string; value: number; color: string }) => (
              <div key={label}>
                <div className="flex justify-between text-xs mb-1">
                  <span className="text-slate-400">{label}</span>
                  <span style={{ color }}>{Math.round(value)}</span>
                </div>
                <div className="h-2 bg-slate-800 rounded-full overflow-hidden">
                  <div
                    style={{ width: `${value}%`, backgroundColor: color }}
                    className="h-full rounded-full"
                  />
                </div>
              </div>
            ))}
          </div>
        )}

        {tab === "signal" && (
          <div className="bg-slate-800/50 rounded-lg p-3">
            <p className="text-sm text-slate-300 leading-relaxed">
              {entity.transformation_signal}
            </p>
          </div>
        )}
      </div>
    </div>
  );
}

export default function MetamorphicBusinessModelEnginePage() {
  const [data, setData] = useState<ApiResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [riskFilter, setRiskFilter] = useState<string>("all");
  const [selectedEntity, setSelectedEntity] = useState<Entity | null>(null);

  useEffect(() => {
    fetch("/api/metamorphic-business-model-engine")
      .then((r: Response) => r.json())
      .then((d: ApiResponse) => {
        setData(d);
        setLoading(false);
      })
      .catch((e: unknown) => {
        setError(String(e));
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center">
        <p className="text-amber-400">Chargement...</p>
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center">
        <p className="text-red-400">Erreur: {error}</p>
      </div>
    );
  }

  const { entities, summary } = data;

  const filteredEntities: Entity[] =
    riskFilter === "all"
      ? entities
      : entities.filter((e: Entity) => e.transformation_risk === riskFilter);

  const riskColors: Record<string, string> = {
    critical: "#ef4444",
    high: "#f97316",
    moderate: "#eab308",
    low: "#22c55e",
  };

  const patternColors: Record<string, string> = {
    metamorphic_stall: "#ef4444",
    identity_crisis: "#f97316",
    capability_gap: "#f59e0b",
    ecosystem_rejection: "#8b5cf6",
    vision_collapse: "#ec4899",
    none: "#22c55e",
  };

  const severityColors: Record<string, string> = {
    fossilized: "#ef4444",
    transitioning: "#f97316",
    morphing: "#f59e0b",
    metamorphosed: "#22c55e",
  };

  const distBars: DistBarItem[] = [
    { title: "Distribution par risque", counts: summary.risk_counts, colors: riskColors },
    { title: "Distribution par pattern", counts: summary.pattern_counts, colors: patternColors },
    { title: "Distribution par sévérité", counts: summary.severity_counts, colors: severityColors },
    {
      title: "Actions recommandées",
      counts: summary.action_counts,
      colors: {
        transformation_emergency: "#ef4444",
        identity_reconstruction: "#f97316",
        capability_sprint: "#f59e0b",
        ecosystem_rebuild: "#8b5cf6",
        transformation_monitoring: "#3b82f6",
        no_action: "#22c55e",
      },
    },
  ];

  const riskBadge = (r: string): string => {
    const cls: Record<string, string> = {
      critical: "bg-red-500/20 text-red-400 border-red-500/40",
      high: "bg-orange-500/20 text-orange-400 border-orange-500/40",
      moderate: "bg-yellow-500/20 text-yellow-400 border-yellow-500/40",
      low: "bg-green-500/20 text-green-400 border-green-500/40",
    };
    return cls[r] ?? "bg-slate-500/20 text-slate-400 border-slate-500/40";
  };

  const kpiCards: Array<{ label: string; value: string | number; color: string }> = [
    { label: "Entités analysées", value: summary.total, color: "text-amber-400" },
    { label: "En crise métamorphique", value: summary.metamorphic_crisis_count, color: "text-red-400" },
    { label: "Intervention immédiate", value: summary.immediate_intervention_count, color: "text-orange-400" },
    { label: "Composite moyen", value: `${summary.avg_transformation_composite}`, color: "text-amber-400" },
    {
      label: "Indice risque moyen",
      value: summary.avg_estimated_transformation_risk_index.toFixed(2),
      color: "text-yellow-400",
    },
    { label: "Critiques", value: summary.risk_counts["critical"] ?? 0, color: "text-red-400" },
  ];

  return (
    <div className="min-h-screen bg-slate-950 text-white p-6">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-amber-400">
          Metamorphic Business Model &amp; Organizational Transformation Engine
        </h1>
        <p className="text-slate-400 mt-1">
          Module 276 · Caelum Partners Swarm Intelligence Platform
        </p>
      </div>

      {/* 6 KPI cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4 mb-8">
        {kpiCards.map(({ label, value, color }: { label: string; value: string | number; color: string }) => (
          <div key={label} className="bg-slate-900 border border-orange-500/30 rounded-xl p-4">
            <p className="text-xs text-slate-400 mb-1">{label}</p>
            <p className={`text-2xl font-bold ${color}`}>{value}</p>
          </div>
        ))}
      </div>

      {/* 4 GaugeRings */}
      <div className="bg-slate-900 border border-orange-500/30 rounded-xl p-6 mb-8">
        <h2 className="text-amber-400 font-semibold mb-4">Scores moyens par dimension</h2>
        <div className="flex flex-wrap justify-around gap-6">
          <GaugeRing value={summary.avg_stagnation_score} color="#ef4444" label="Stagnation" />
          <GaugeRing value={summary.avg_readiness_score} color="#f97316" label="Readiness" />
          <GaugeRing value={summary.avg_momentum_score} color="#3b82f6" label="Momentum" />
          <GaugeRing value={summary.avg_alignment_score} color="#8b5cf6" label="Alignment" />
        </div>
      </div>

      {/* 4 DistBars */}
      <div className="bg-slate-900 border border-orange-500/30 rounded-xl p-6 mb-8">
        <h2 className="text-amber-400 font-semibold mb-4">Distributions</h2>
        {distBars.map((item: DistBarItem) => (
          <DistBar key={item.title} item={item} />
        ))}
      </div>

      {/* Filter pills */}
      <div className="flex flex-wrap gap-2 mb-6">
        {["all", "critical", "high", "moderate", "low"].map((f: string) => (
          <button
            key={f}
            onClick={() => setRiskFilter(f)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${
              riskFilter === f
                ? "bg-orange-500/20 text-amber-400 border-orange-500/40"
                : "text-slate-400 border-slate-700 hover:border-orange-500/40 hover:text-amber-400"
            }`}
          >
            {f === "all" ? "Tous" : f}
          </button>
        ))}
      </div>

      {/* Entity cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {filteredEntities.map((entity: Entity) => (
          <div
            key={entity.entity_id}
            className="bg-slate-900 border border-orange-500/30 rounded-xl p-4 cursor-pointer hover:border-orange-500/60 transition-colors"
            onClick={() => setSelectedEntity(entity)}
          >
            <div className="flex justify-between items-start mb-2">
              <span className="text-amber-400 font-semibold text-sm">{entity.entity_id}</span>
              <span
                className={`text-xs px-2 py-0.5 rounded-full border font-medium ${riskBadge(entity.transformation_risk)}`}
              >
                {entity.transformation_risk}
              </span>
            </div>
            <p className="text-xs text-slate-400 mb-1">
              {entity.transformation_stage.replace(/_/g, " ")}
            </p>
            <p className="text-xs text-slate-500 mb-3">{entity.region}</p>
            <div className="flex justify-between text-xs mb-2">
              <span className="text-slate-400">Pattern</span>
              <span className="text-white">{entity.metamorphic_pattern.replace(/_/g, " ")}</span>
            </div>
            <div className="flex justify-between text-xs mb-3">
              <span className="text-slate-400">Composite</span>
              <span className="text-amber-400 font-medium">
                {Math.round(entity.transformation_composite)}
              </span>
            </div>
            <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
              <div
                style={{
                  width: `${entity.transformation_composite}%`,
                  backgroundColor: riskColors[entity.transformation_risk] ?? "#f59e0b",
                }}
                className="h-full rounded-full"
              />
            </div>
            {entity.is_in_metamorphic_crisis && (
              <p className="text-xs text-red-400 mt-2">⚠ Crise métamorphique</p>
            )}
          </div>
        ))}
      </div>

      {/* DetailModal */}
      {selectedEntity && (
        <DetailModal entity={selectedEntity} onClose={() => setSelectedEntity(null)} />
      )}
    </div>
  );
}
