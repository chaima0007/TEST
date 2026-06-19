"use client";
import { useEffect, useState, useMemo } from "react";

type Entity = {
  entity_id: string;
  region: string;
  longevity_sector: string;
  longevity_risk: string;
  longevity_pattern: string;
  longevity_severity: string;
  recommended_action: string;
  access_score: number;
  disruption_score: number;
  governance_score: number;
  societal_score: number;
  longevity_composite: number;
  is_longevity_crisis: boolean;
  requires_longevity_intervention: boolean;
  longevity_signal: string;
};

type Summary = {
  total_entities: number;
  critical_entities: number;
  high_entities: number;
  moderate_entities: number;
  low_entities: number;
  entities_requiring_intervention: number;
  longevity_crisis_entities: number;
  avg_access_score: number;
  avg_disruption_score: number;
  avg_governance_score: number;
  avg_societal_score: number;
  avg_longevity_composite: number;
  avg_estimated_longevity_disruption_index: number;
};

function GaugeRing({ value, label, color }: { value: number; label: string; color: string }) {
  const r = 36;
  const circ = 2 * Math.PI * r;
  const fill = circ * (1 - value / 100);
  return (
    <div className="flex flex-col items-center gap-1">
      <svg width="88" height="88" viewBox="0 0 88 88">
        <circle cx="44" cy="44" r={r} fill="none" stroke="#0f172a" strokeWidth="8" />
        <circle
          cx="44" cy="44" r={r} fill="none" stroke={color} strokeWidth="8"
          strokeDasharray={circ} strokeDashoffset={fill}
          strokeLinecap="round" transform="rotate(-90 44 44)"
        />
        <text x="44" y="49" textAnchor="middle" fill="white" fontSize="13" fontWeight="bold">
          {Math.round(value)}
        </text>
      </svg>
      <span className="text-xs text-emerald-400/70 text-center">{label}</span>
    </div>
  );
}

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
    <div className="flex flex-col gap-1">
      <span className="text-xs text-emerald-400/70 font-medium">{title}</span>
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
          <span key={k} className="text-xs text-emerald-400/60">
            <span style={{ color: colors[k] || "#94a3b8" }}>■</span> {k.replace(/_/g, " ")} {v}
          </span>
        ))}
      </div>
    </div>
  );
}

const RISK_COLORS: Record<string, string> = {
  low: "#10b981",
  moderate: "#eab308",
  high: "#f97316",
  critical: "#ef4444",
};

const PAT_COLORS: Record<string, string> = {
  none: "#10b981",
  immortality_apartheid: "#dc2626",
  system_collapse_shock: "#f97316",
  biotech_monopoly: "#7c3aed",
  governance_vacuum: "#0891b2",
  intergenerational_war: "#be185d",
};

const SEV_COLORS: Record<string, string> = {
  longevity_managed: "#10b981",
  longevity_tension: "#eab308",
  high_longevity_disruption: "#f97316",
  longevity_emergency: "#7f1d1d",
};

const ACTION_COLORS: Record<string, string> = {
  no_action: "#10b981",
  longevity_monitoring: "#06b6d4",
  longevity_transition_framework: "#eab308",
  universal_longevity_access: "#f97316",
  longevity_emergency_governance: "#dc2626",
};

const RISK_BADGE: Record<string, string> = {
  low: "bg-green-500/20 text-green-400",
  moderate: "bg-yellow-500/20 text-yellow-400",
  high: "bg-orange-500/20 text-orange-400",
  critical: "bg-red-500/20 text-red-400",
};

const SEV_BADGE: Record<string, string> = {
  longevity_managed: "bg-green-500/20 text-green-400",
  longevity_tension: "bg-yellow-500/20 text-yellow-400",
  high_longevity_disruption: "bg-orange-500/20 text-orange-400",
  longevity_emergency: "bg-red-500/20 text-red-400",
};

function DetailModal({ entity, onClose }: { entity: Entity; onClose: () => void }) {
  const [tab, setTab] = useState<"overview" | "scores" | "signal">("overview");

  useEffect(() => {
    const h = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
    };
    window.addEventListener("keydown", h);
    return () => window.removeEventListener("keydown", h);
  }, [onClose]);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80" onClick={onClose}>
      <div
        className="bg-slate-950 border border-pink-700/30 rounded-xl w-full max-w-lg p-6 shadow-2xl"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="flex items-center justify-between mb-4">
          <div>
            <span className="text-lg font-bold text-white">{entity.entity_id}</span>
            <span className="ml-2 text-emerald-400 text-xs">{entity.region}</span>
            <span className="ml-2 text-slate-500 text-xs">{entity.longevity_sector.replace(/_/g, " ")}</span>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl leading-none">
            ✕
          </button>
        </div>

        <div className="flex gap-2 mb-4">
          {(["overview", "scores", "signal"] as const).map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`px-3 py-1 rounded text-xs font-medium transition-colors ${
                tab === t
                  ? "bg-emerald-900/60 text-white"
                  : "bg-slate-900 text-slate-400 hover:text-white"
              }`}
            >
              {t === "overview" ? "Vue d'ensemble" : t === "scores" ? "Scores" : "Signal"}
            </button>
          ))}
        </div>

        {tab === "overview" && (
          <div className="space-y-3 text-sm">
            <div className="bg-slate-900/50 border border-pink-700/30 rounded-lg p-3">
              <div className="text-emerald-400/60 text-xs mb-1">Action Recommandée</div>
              <div className="text-white font-medium">{entity.recommended_action.replace(/_/g, " ")}</div>
            </div>
            <div className="bg-slate-900/50 border border-pink-700/30 rounded-lg p-3">
              <div className="text-emerald-400/60 text-xs mb-1">Pattern Longévité Tech</div>
              <div className="text-white font-medium">{entity.longevity_pattern.replace(/_/g, " ")}</div>
            </div>
            <div className="bg-slate-900/50 border border-pink-700/30 rounded-lg p-3">
              <div className="text-emerald-400/60 text-xs mb-1">Composite Longévité</div>
              <div className="text-white font-bold text-2xl">{entity.longevity_composite.toFixed(1)}</div>
            </div>
            <div className="flex gap-2 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[entity.longevity_risk] || "bg-slate-700 text-slate-300"}`}>
                {entity.longevity_risk}
              </span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[entity.longevity_severity] || "bg-slate-700 text-slate-300"}`}>
                {entity.longevity_severity.replace(/_/g, " ")}
              </span>
              {entity.is_longevity_crisis && (
                <span className="px-2 py-0.5 rounded bg-red-500/20 text-red-400 text-xs font-medium">
                  CRISE LONGÉVITÉ
                </span>
              )}
              {entity.requires_longevity_intervention && (
                <span className="px-2 py-0.5 rounded bg-orange-500/20 text-orange-400 text-xs font-medium">
                  INTERVENTION REQ.
                </span>
              )}
            </div>
          </div>
        )}

        {tab === "scores" && (
          <div className="grid grid-cols-2 gap-3 text-sm">
            {[
              ["Accès", entity.access_score, "#10b981"],
              ["Disruption", entity.disruption_score, "#f97316"],
              ["Gouvernance", entity.governance_score, "#0891b2"],
              ["Sociétal", entity.societal_score, "#be185d"],
            ].map(([l, v, c]) => (
              <div key={String(l)} className="bg-slate-900/50 border border-pink-700/30 rounded-lg p-3">
                <div className="text-emerald-400/60 text-xs mb-1">{String(l)}</div>
                <div className="text-white font-bold text-lg">{Number(v).toFixed(1)}</div>
                <div className="h-1.5 rounded mt-1 bg-slate-800">
                  <div
                    className="h-1.5 rounded"
                    style={{ width: `${Math.min(Number(v), 100)}%`, background: String(c) }}
                  />
                </div>
              </div>
            ))}
            <div className="col-span-2 bg-slate-900/50 border border-pink-700/30 rounded-lg p-3">
              <div className="text-emerald-400/60 text-xs mb-1">Composite Longévité</div>
              <div className="text-white font-bold text-2xl">{entity.longevity_composite.toFixed(1)}</div>
            </div>
          </div>
        )}

        {tab === "signal" && (
          <div className="bg-slate-900/50 border border-pink-700/30 rounded-lg p-4 text-sm text-slate-200 leading-relaxed">
            {entity.longevity_signal}
            <div className="mt-3 flex gap-2 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[entity.longevity_risk] || "bg-slate-700 text-slate-300"}`}>
                {entity.longevity_risk}
              </span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[entity.longevity_severity] || "bg-slate-700 text-slate-300"}`}>
                {entity.longevity_severity.replace(/_/g, " ")}
              </span>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function LongevityTechEngineDashboard() {
  const [data, setData] = useState<{ entities: Entity[]; summary: Summary } | null>(null);
  const [riskFilter, setRiskFilter] = useState<string>("all");
  const [selected, setSelected] = useState<Entity | null>(null);

  useEffect(() => {
    fetch("/api/longevity-tech-engine")
      .then((r) => r.json())
      .then(setData)
      .catch(console.error);
  }, []);

  const filtered = useMemo(() => {
    if (!data) return [];
    return data.entities.filter(
      (e) => riskFilter === "all" || e.longevity_risk === riskFilter
    );
  }, [data, riskFilter]);

  if (!data)
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center">
        <div className="text-emerald-400 text-lg animate-pulse">
          Initialisation du Moteur Technologie Longévité...
        </div>
      </div>
    );

  const { summary } = data;

  const riskDist: Record<string, number> = {};
  const patDist: Record<string, number> = {};
  const sevDist: Record<string, number> = {};
  const actDist: Record<string, number> = {};

  for (const e of data.entities) {
    riskDist[e.longevity_risk] = (riskDist[e.longevity_risk] || 0) + 1;
    patDist[e.longevity_pattern] = (patDist[e.longevity_pattern] || 0) + 1;
    sevDist[e.longevity_severity] = (sevDist[e.longevity_severity] || 0) + 1;
    actDist[e.recommended_action] = (actDist[e.recommended_action] || 0) + 1;
  }

  const dists = [
    { title: "Niveau Risque Longévité Tech", counts: riskDist, colors: RISK_COLORS },
    { title: "Pattern Longévité", counts: patDist, colors: PAT_COLORS },
    { title: "Sévérité Longévité", counts: sevDist, colors: SEV_COLORS },
    { title: "Action Déclenchée", counts: actDist, colors: ACTION_COLORS },
  ] as Array<{ title: string; counts: Record<string, number>; colors: Record<string, string> }>;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {selected && <DetailModal entity={selected} onClose={() => setSelected(null)} />}

      <div>
        <h1 className="text-2xl font-bold text-emerald-400">
          Technologie Longévité &amp; Économie Anti-Vieillissement — Module 324
        </h1>
        <p className="text-emerald-400/50 text-sm mt-1">
          Accès Sénolytique · Disruption Systèmes · Gouvernance Bioéthique · Cohésion Sociétale
        </p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {[
          ["Entités Analysées", summary.total_entities, "text-emerald-400"],
          ["Entités Critiques", summary.critical_entities, "text-red-400"],
          ["Crises Longévité", summary.longevity_crisis_entities, "text-red-400"],
          ["Interventions Requises", summary.entities_requiring_intervention, "text-orange-400"],
          ["Composite Moy.", summary.avg_longevity_composite.toFixed(2), "text-emerald-300"],
          ["Indice Disruption Moy.", `${summary.avg_estimated_longevity_disruption_index.toFixed(2)}/10`, "text-pink-400"],
        ].map(([l, v, c]) => (
          <div key={String(l)} className="bg-slate-900/50 border border-pink-700/30 rounded-xl p-3 text-center">
            <div className={`text-xl font-bold ${c}`}>{v}</div>
            <div className="text-xs text-emerald-400/40 mt-0.5 leading-tight">{l}</div>
          </div>
        ))}
      </div>

      {/* Gauge Rings */}
      <div className="bg-slate-900/50 border border-pink-700/30 rounded-xl p-5">
        <div className="grid grid-cols-4 gap-4">
          <GaugeRing value={summary.avg_access_score} label="Accès" color="#10b981" />
          <GaugeRing value={summary.avg_disruption_score} label="Disruption" color="#f97316" />
          <GaugeRing value={summary.avg_governance_score} label="Gouvernance" color="#0891b2" />
          <GaugeRing value={summary.avg_societal_score} label="Sociétal" color="#be185d" />
        </div>
      </div>

      {/* Distribution Bars */}
      <div className="bg-slate-900/50 border border-pink-700/30 rounded-xl p-5 grid grid-cols-1 md:grid-cols-2 gap-5">
        {dists.map((d) => (
          <DistBar key={d.title} {...d} />
        ))}
      </div>

      {/* Filter Pills */}
      <div className="flex flex-wrap gap-2">
        {[
          { key: "all", label: "Tous" },
          { key: "critical", label: "Critique" },
          { key: "high", label: "Élevé" },
          { key: "moderate", label: "Modéré" },
          { key: "low", label: "Faible" },
        ].map(({ key, label }) => (
          <button
            key={key}
            onClick={() => setRiskFilter(key)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${
              riskFilter === key
                ? "bg-emerald-900/60 border-emerald-700 text-white"
                : "bg-slate-900/50 border-pink-700/30 text-emerald-400/70 hover:text-white"
            }`}
          >
            {label}
          </button>
        ))}
      </div>

      {/* Entity Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {filtered.map((e) => (
          <div
            key={e.entity_id}
            onClick={() => setSelected(e)}
            className="bg-slate-900/50 border border-pink-700/30 rounded-xl p-4 cursor-pointer hover:border-emerald-500 transition-colors"
          >
            <div className="flex items-center justify-between mb-1">
              <span className="font-bold text-white">{e.entity_id}</span>
              <span className="text-xs text-emerald-400/60">{e.region}</span>
            </div>
            <div className="text-xs text-slate-500 mb-2 capitalize">
              {e.longevity_sector.replace(/_/g, " ")}
            </div>
            <div className="flex gap-1 mb-3 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[e.longevity_risk] || "bg-slate-700 text-slate-300"}`}>
                {e.longevity_risk}
              </span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[e.longevity_severity] || "bg-slate-700 text-slate-300"}`}>
                {e.longevity_severity.replace(/_/g, " ")}
              </span>
            </div>
            <div className="text-2xl font-black text-white mb-1">{e.longevity_composite.toFixed(1)}</div>
            <div className="text-xs text-emerald-400/60 mb-2 capitalize">
              {e.longevity_pattern.replace(/_/g, " ")}
            </div>
            <div className="text-xs text-pink-400 font-medium mb-2">
              {e.recommended_action.replace(/_/g, " ")}
            </div>
            <div className="flex gap-1 flex-wrap">
              {e.is_longevity_crisis && (
                <span className="px-1.5 py-0.5 rounded bg-red-500/20 text-red-400 text-xs">CRISE</span>
              )}
              {e.requires_longevity_intervention && (
                <span className="px-1.5 py-0.5 rounded bg-orange-500/20 text-orange-400 text-xs">INTERVENTION</span>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
