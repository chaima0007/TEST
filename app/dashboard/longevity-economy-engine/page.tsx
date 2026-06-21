"use client";
import { useEffect, useState } from "react";

type Entity = {
  id: string;
  region: string;
  longevity_segment: string;
  longevity_risk: string;
  longevity_pattern: string;
  longevity_severity: string;
  recommended_action: string;
  aging_score: number;
  financial_score: number;
  health_score: number;
  inclusion_score: number;
  longevity_composite: number;
  is_in_longevity_crisis: boolean;
  requires_longevity_intervention: boolean;
  longevity_signal: string;
};

type Summary = {
  total: number;
  risk_counts: Record<string, number>;
  pattern_counts: Record<string, number>;
  severity_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_longevity_composite: number;
  longevity_crisis_count: number;
  longevity_intervention_count: number;
  avg_aging_score: number;
  avg_financial_score: number;
  avg_health_score: number;
  avg_inclusion_score: number;
  avg_estimated_longevity_risk_index: number;
};

function GaugeRing({ value, label, color }: { value: number; label: string; color: string }) {
  const r = 36;
  const circ = 2 * Math.PI * r;
  const fill = circ * (1 - value / 100);
  return (
    <div className="flex flex-col items-center gap-1">
      <svg width="88" height="88" viewBox="0 0 88 88">
        <circle cx="44" cy="44" r={r} fill="none" stroke="#0f1a1a" strokeWidth="8" />
        <circle
          cx="44" cy="44" r={r} fill="none" stroke={color} strokeWidth="8"
          strokeDasharray={circ} strokeDashoffset={fill}
          strokeLinecap="round" transform="rotate(-90 44 44)"
        />
        <text x="44" y="49" textAnchor="middle" fill="white" fontSize="13" fontWeight="bold">
          {Math.round(value)}
        </text>
      </svg>
      <span className="text-xs text-teal-300/70 text-center">{label}</span>
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
      <span className="text-xs text-teal-300/70 font-medium">{title}</span>
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
          <span key={k} className="text-xs text-teal-300/60">
            <span style={{ color: colors[k] || "#94a3b8" }}>■</span> {k.replace(/_/g, " ")} {v}
          </span>
        ))}
      </div>
    </div>
  );
}

const RISK_COLORS: Record<string, string> = {
  low: "#10b981",
  moderate: "#f59e0b",
  high: "#f97316",
  critical: "#ef4444",
};
const PAT_COLORS: Record<string, string> = {
  none: "#10b981",
  pension_collapse: "#7c3aed",
  healthcare_cost_spiral: "#ef4444",
  silver_exclusion: "#f97316",
  intergenerational_wealth_lock: "#dc2626",
  longevity_insurance_gap: "#a855f7",
};
const SEV_COLORS: Record<string, string> = {
  longevity_thriving: "#10b981",
  silver_stress: "#f59e0b",
  high_longevity_risk: "#f97316",
  longevity_emergency: "#7f1d1d",
};
const ACTION_COLORS: Record<string, string> = {
  no_action: "#10b981",
  longevity_monitoring: "#06b6d4",
  silver_economy_stimulus: "#f59e0b",
  pension_rescue: "#f97316",
  longevity_emergency_program: "#dc2626",
};
const RISK_BADGE: Record<string, string> = {
  low: "bg-emerald-900 text-emerald-300",
  moderate: "bg-amber-900 text-amber-300",
  high: "bg-orange-900 text-orange-300",
  critical: "bg-red-950 text-red-400",
};
const SEV_BADGE: Record<string, string> = {
  longevity_thriving: "bg-emerald-900 text-emerald-300",
  silver_stress: "bg-amber-900 text-amber-300",
  high_longevity_risk: "bg-orange-900 text-orange-300",
  longevity_emergency: "bg-red-950 text-red-400",
};

function DetailModal({ entity, onClose }: { entity: Entity; onClose: () => void }) {
  const [tab, setTab] = useState<"scores" | "signal" | "action">("scores");

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
        className="bg-slate-950 border border-teal-500/30 rounded-xl w-full max-w-lg p-6 shadow-2xl"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="flex items-center justify-between mb-4">
          <div>
            <span className="text-lg font-bold text-white">{entity.id}</span>
            <span className="ml-2 text-amber-400 text-xs">{entity.region}</span>
            <span className="ml-2 text-slate-500 text-xs">{entity.longevity_segment.replace(/_/g, " ")}</span>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl leading-none">
            ✕
          </button>
        </div>
        <div className="flex gap-2 mb-4">
          {(["scores", "signal", "action"] as const).map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`px-3 py-1 rounded text-xs font-medium transition-colors ${
                tab === t ? "bg-teal-900 text-white" : "bg-slate-900 text-slate-400 hover:text-white"
              }`}
            >
              {t.charAt(0).toUpperCase() + t.slice(1)}
            </button>
          ))}
        </div>

        {tab === "scores" && (
          <div className="grid grid-cols-2 gap-3 text-sm">
            {[
              ["Vieillissement", entity.aging_score, "#f59e0b"],
              ["Financier", entity.financial_score, "#14b8a6"],
              ["Santé", entity.health_score, "#ef4444"],
              ["Inclusion", entity.inclusion_score, "#a855f7"],
            ].map(([l, v, c]) => (
              <div key={String(l)} className="bg-slate-900 border border-teal-500/20 rounded-lg p-3">
                <div className="text-teal-300/60 text-xs mb-1">{String(l)}</div>
                <div className="text-white font-bold text-lg">{Number(v).toFixed(1)}</div>
                <div className="h-1.5 rounded mt-1 bg-slate-800">
                  <div
                    className="h-1.5 rounded"
                    style={{ width: `${Math.min(Number(v), 100)}%`, background: String(c) }}
                  />
                </div>
              </div>
            ))}
            <div className="col-span-2 bg-slate-900 border border-teal-500/20 rounded-lg p-3">
              <div className="text-teal-300/60 text-xs mb-1">Composite Longévité</div>
              <div className="text-white font-bold text-2xl">{entity.longevity_composite.toFixed(1)}</div>
            </div>
          </div>
        )}

        {tab === "signal" && (
          <div className="bg-slate-900 border border-teal-500/20 rounded-lg p-4 text-sm text-slate-200 leading-relaxed">
            {entity.longevity_signal}
            <div className="mt-3 flex gap-2 flex-wrap">
              <span
                className={`px-2 py-0.5 rounded text-xs font-medium ${
                  RISK_BADGE[entity.longevity_risk] || "bg-slate-700 text-slate-300"
                }`}
              >
                {entity.longevity_risk}
              </span>
              <span
                className={`px-2 py-0.5 rounded text-xs font-medium ${
                  SEV_BADGE[entity.longevity_severity] || "bg-slate-700 text-slate-300"
                }`}
              >
                {entity.longevity_severity.replace(/_/g, " ")}
              </span>
            </div>
          </div>
        )}

        {tab === "action" && (
          <div className="space-y-3 text-sm">
            <div className="bg-slate-900 border border-teal-500/20 rounded-lg p-3">
              <div className="text-teal-300/60 text-xs mb-1">Action Recommandée</div>
              <div className="text-white font-medium">{entity.recommended_action.replace(/_/g, " ")}</div>
            </div>
            <div className="bg-slate-900 border border-teal-500/20 rounded-lg p-3">
              <div className="text-teal-300/60 text-xs mb-1">Pattern Longévité</div>
              <div className="text-white font-medium">{entity.longevity_pattern.replace(/_/g, " ")}</div>
            </div>
            <div className="flex gap-2 flex-wrap">
              {entity.is_in_longevity_crisis && (
                <span className="px-2 py-1 rounded bg-red-950 text-red-400 text-xs font-medium">
                  CRISE LONGÉVITÉ
                </span>
              )}
              {entity.requires_longevity_intervention && (
                <span className="px-2 py-1 rounded bg-amber-950 text-amber-400 text-xs font-medium">
                  INTERVENTION REQ.
                </span>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function LongevityEconomyDashboard() {
  const [data, setData] = useState<{ entities: Entity[]; summary: Summary } | null>(null);
  const [riskFilter, setRiskFilter] = useState<string>("all");
  const [patFilter, setPatFilter] = useState<string>("all");
  const [selected, setSelected] = useState<Entity | null>(null);

  useEffect(() => {
    fetch("/api/longevity-economy-engine")
      .then((r) => r.json())
      .then(setData)
      .catch(console.error);
  }, []);

  if (!data)
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center">
        <div className="text-amber-400 text-lg animate-pulse">Initialisation du Moteur Économie Longévité...</div>
      </div>
    );

  const { entities, summary } = data;

  const filtered = entities.filter(
    (e) =>
      (riskFilter === "all" || e.longevity_risk === riskFilter) &&
      (patFilter === "all" || e.longevity_pattern === patFilter)
  );

  const dists = [
    { title: "Niveau Risque Longévité", counts: summary.risk_counts, colors: RISK_COLORS },
    { title: "Pattern Longévité", counts: summary.pattern_counts, colors: PAT_COLORS },
    { title: "Sévérité Silver", counts: summary.severity_counts, colors: SEV_COLORS },
    { title: "Action Déclenchée", counts: summary.action_counts, colors: ACTION_COLORS },
  ] as Array<{ title: string; counts: Record<string, number>; colors: Record<string, string> }>;

  const criticalCount = summary.risk_counts["critical"] || 0;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {selected && <DetailModal entity={selected} onClose={() => setSelected(null)} />}

      <div>
        <h1 className="text-2xl font-bold text-amber-400">
          Longevity Economy &amp; Silver Intelligence Engine
        </h1>
        <p className="text-teal-300/50 text-sm mt-1">
          Vieillissement · Finances Silver · Santé Longévité · Inclusion Intergénérationnelle
        </p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {[
          ["Entités Analysées", summary.total, "text-amber-400"],
          ["Crises Longévité Critiques", criticalCount, "text-red-400"],
          ["Composite Longévité Moy.", `${summary.avg_longevity_composite.toFixed(1)}`, "text-amber-300"],
          ["Indice Risque Moy.", `${summary.avg_estimated_longevity_risk_index.toFixed(2)}/10`, "text-teal-400"],
          ["Entités en Crise", summary.longevity_crisis_count, "text-red-400"],
          ["Interventions Requises", summary.longevity_intervention_count, "text-orange-400"],
        ].map(([l, v, c]) => (
          <div key={String(l)} className="bg-slate-900 border border-teal-500/30 rounded-xl p-3 text-center">
            <div className={`text-xl font-bold ${c}`}>{v}</div>
            <div className="text-xs text-teal-300/40 mt-0.5 leading-tight">{l}</div>
          </div>
        ))}
      </div>

      {/* Gauge Rings */}
      <div className="bg-slate-900 border border-teal-500/30 rounded-xl p-5">
        <div className="grid grid-cols-4 gap-4">
          <GaugeRing value={summary.avg_aging_score} label="Score Vieillissement" color="#f59e0b" />
          <GaugeRing value={summary.avg_financial_score} label="Score Financier Silver" color="#14b8a6" />
          <GaugeRing value={summary.avg_health_score} label="Score Santé Longévité" color="#ef4444" />
          <GaugeRing value={summary.avg_inclusion_score} label="Score Inclusion Silver" color="#a855f7" />
        </div>
      </div>

      {/* Distribution Bars */}
      <div className="bg-slate-900 border border-teal-500/30 rounded-xl p-5 grid grid-cols-1 md:grid-cols-2 gap-5">
        {dists.map((d) => (
          <DistBar key={d.title} {...d} />
        ))}
      </div>

      {/* Filter Pills */}
      <div className="flex flex-wrap gap-2">
        {["all", "low", "moderate", "high", "critical"].map((r) => (
          <button
            key={r}
            onClick={() => setRiskFilter(r)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${
              riskFilter === r
                ? "bg-amber-900 border-amber-700 text-white"
                : "bg-slate-900 border-teal-500/30 text-teal-400/70 hover:text-white"
            }`}
          >
            {r}
          </button>
        ))}
        <span className="w-px h-5 self-center bg-teal-500/30" />
        {[
          "all",
          "none",
          "pension_collapse",
          "healthcare_cost_spiral",
          "silver_exclusion",
          "intergenerational_wealth_lock",
          "longevity_insurance_gap",
        ].map((p) => (
          <button
            key={p}
            onClick={() => setPatFilter(p)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${
              patFilter === p
                ? "bg-teal-900 border-teal-700 text-white"
                : "bg-slate-900 border-teal-500/30 text-teal-400/70 hover:text-white"
            }`}
          >
            {p.replace(/_/g, " ")}
          </button>
        ))}
      </div>

      {/* Entity Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {filtered.map((e) => (
          <div
            key={e.id}
            onClick={() => setSelected(e)}
            className="bg-slate-900 border border-teal-500/30 rounded-xl p-4 cursor-pointer hover:border-amber-500 transition-colors"
          >
            <div className="flex items-center justify-between mb-1">
              <span className="font-bold text-white">{e.id}</span>
              <span className="text-xs text-amber-400/60">{e.region}</span>
            </div>
            <div className="text-xs text-slate-500 mb-2 capitalize">
              {e.longevity_segment.replace(/_/g, " ")}
            </div>
            <div className="flex gap-1 mb-3 flex-wrap">
              <span
                className={`px-2 py-0.5 rounded text-xs font-medium ${
                  RISK_BADGE[e.longevity_risk] || "bg-slate-700 text-slate-300"
                }`}
              >
                {e.longevity_risk}
              </span>
              <span
                className={`px-2 py-0.5 rounded text-xs font-medium ${
                  SEV_BADGE[e.longevity_severity] || "bg-slate-700 text-slate-300"
                }`}
              >
                {e.longevity_severity.replace(/_/g, " ")}
              </span>
            </div>
            <div className="text-2xl font-black text-white mb-1">{e.longevity_composite.toFixed(1)}</div>
            <div className="text-xs text-teal-400/60 mb-2 capitalize">
              {e.longevity_pattern.replace(/_/g, " ")}
            </div>
            <div className="text-xs text-amber-400 font-medium mb-2">
              {e.recommended_action.replace(/_/g, " ")}
            </div>
            <div className="flex gap-1 flex-wrap">
              {e.is_in_longevity_crisis && (
                <span className="px-1.5 py-0.5 rounded bg-red-950 text-red-400 text-xs">CRISE</span>
              )}
              {e.requires_longevity_intervention && (
                <span className="px-1.5 py-0.5 rounded bg-amber-950 text-amber-400 text-xs">INTERVENTION</span>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
