"use client";
import { useEffect, useState } from "react";

type Entity = {
  id: string;
  region: string;
  augmentation_domain: string;
  augmentation_risk: string;
  augmentation_pattern: string;
  augmentation_severity: string;
  recommended_action: string;
  adoption_score: number;
  equity_score: number;
  integrity_score: number;
  transition_score: number;
  augmentation_composite: number;
  is_in_augmentation_crisis: boolean;
  requires_augmentation_intervention: boolean;
  augmentation_signal: string;
};

type Summary = {
  total: number;
  risk_counts: Record<string, number>;
  pattern_counts: Record<string, number>;
  severity_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_augmentation_composite: number;
  augmentation_crisis_count: number;
  augmentation_intervention_count: number;
  avg_adoption_score: number;
  avg_equity_score: number;
  avg_integrity_score: number;
  avg_transition_score: number;
  avg_estimated_augmentation_disruption_index: number;
};

function GaugeRing({ value, label, color }: { value: number; label: string; color: string }) {
  const r = 36;
  const circ = 2 * Math.PI * r;
  const fill = circ * (1 - value / 100);
  return (
    <div className="flex flex-col items-center gap-1">
      <svg width="88" height="88" viewBox="0 0 88 88">
        <circle cx="44" cy="44" r={r} fill="none" stroke="#020617" strokeWidth="8" />
        <circle cx="44" cy="44" r={r} fill="none" stroke={color} strokeWidth="8"
          strokeDasharray={circ} strokeDashoffset={fill}
          strokeLinecap="round" transform="rotate(-90 44 44)" />
        <text x="44" y="49" textAnchor="middle" fill="white" fontSize="13" fontWeight="bold">
          {Math.round(value)}
        </text>
      </svg>
      <span className="text-xs text-cyan-300/70 text-center">{label}</span>
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
      <span className="text-xs text-cyan-300/70 font-medium">{title}</span>
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
          <span key={k} className="text-xs text-cyan-300/60">
            <span style={{ color: colors[k] || "#94a3b8" }}>■</span> {k} {v}
          </span>
        ))}
      </div>
    </div>
  );
}

const RISK_COLORS = {
  low: "#10b981",
  moderate: "#f59e0b",
  high: "#f97316",
  critical: "#ec4899",
};
const PAT_COLORS = {
  none: "#10b981",
  cognitive_arms_race: "#06b6d4",
  identity_collapse: "#a855f7",
  augmentation_divide: "#ec4899",
  regulatory_vacuum: "#f97316",
  biological_sovereignty_loss: "#dc2626",
};
const SEV_COLORS = {
  controlled_augmentation: "#10b981",
  early_disruption: "#f59e0b",
  high_transition_risk: "#f97316",
  post_human_rupture: "#ec4899",
};
const ACTION_COLORS = {
  no_action: "#10b981",
  augmentation_monitoring: "#06b6d4",
  transition_management: "#f59e0b",
  identity_preservation_protocol: "#a855f7",
  augmentation_governance_emergency: "#ec4899",
};

const RISK_BADGE = {
  low: "bg-emerald-900 text-emerald-300",
  moderate: "bg-amber-900 text-amber-300",
  high: "bg-orange-900 text-orange-300",
  critical: "bg-pink-950 text-pink-400",
};
const SEV_BADGE = {
  controlled_augmentation: "bg-emerald-900 text-emerald-300",
  early_disruption: "bg-amber-900 text-amber-300",
  high_transition_risk: "bg-orange-900 text-orange-300",
  post_human_rupture: "bg-pink-950 text-pink-400",
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
        className="bg-slate-950 border border-pink-600/30 rounded-xl w-full max-w-lg p-6 shadow-2xl"
        onClick={e => e.stopPropagation()}
      >
        <div className="flex items-center justify-between mb-4">
          <div>
            <span className="text-lg font-bold text-white">{entity.id}</span>
            <span className="ml-2 text-cyan-400 text-xs">{entity.region}</span>
            <span className="ml-2 text-slate-500 text-xs">{entity.augmentation_domain.replace(/_/g, " ")}</span>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl leading-none">
            ✕
          </button>
        </div>

        <div className="flex gap-2 mb-4">
          {(["scores", "signal", "action"] as const).map(t => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`px-3 py-1 rounded text-xs font-medium transition-colors ${
                tab === t
                  ? "bg-pink-900 text-white"
                  : "bg-slate-900 text-slate-400 hover:text-white"
              }`}
            >
              {t.charAt(0).toUpperCase() + t.slice(1)}
            </button>
          ))}
        </div>

        {tab === "scores" && (
          <div className="grid grid-cols-2 gap-3 text-sm">
            {(
              [
                ["Adoption",    entity.adoption_score,    "#06b6d4"],
                ["Équité",      entity.equity_score,      "#ec4899"],
                ["Intégrité",   entity.integrity_score,   "#a855f7"],
                ["Transition",  entity.transition_score,  "#f97316"],
              ] as [string, number, string][]
            ).map(([l, v, c]) => (
              <div key={l} className="bg-slate-900 border border-pink-600/20 rounded-lg p-3">
                <div className="text-cyan-300/60 text-xs mb-1">{l}</div>
                <div className="text-white font-bold text-lg">{Number(v).toFixed(1)}</div>
                <div className="h-1.5 rounded mt-1 bg-slate-800">
                  <div
                    className="h-1.5 rounded"
                    style={{ width: `${Math.min(Number(v), 100)}%`, background: c }}
                  />
                </div>
              </div>
            ))}
            <div className="col-span-2 bg-slate-900 border border-pink-600/20 rounded-lg p-3">
              <div className="text-cyan-300/60 text-xs mb-1">Composite Augmentation</div>
              <div className="text-white font-bold text-2xl">{entity.augmentation_composite.toFixed(1)}</div>
            </div>
          </div>
        )}

        {tab === "signal" && (
          <div className="bg-slate-900 border border-pink-600/20 rounded-lg p-4 text-sm text-slate-200 leading-relaxed">
            {entity.augmentation_signal}
            <div className="mt-3 flex gap-2 flex-wrap">
              <span
                className={`px-2 py-0.5 rounded text-xs font-medium ${
                  RISK_BADGE[entity.augmentation_risk as keyof typeof RISK_BADGE] ||
                  "bg-slate-700 text-slate-300"
                }`}
              >
                {entity.augmentation_risk}
              </span>
              <span
                className={`px-2 py-0.5 rounded text-xs font-medium ${
                  SEV_BADGE[entity.augmentation_severity as keyof typeof SEV_BADGE] ||
                  "bg-slate-700 text-slate-300"
                }`}
              >
                {entity.augmentation_severity.replace(/_/g, " ")}
              </span>
            </div>
          </div>
        )}

        {tab === "action" && (
          <div className="space-y-3 text-sm">
            <div className="bg-slate-900 border border-pink-600/20 rounded-lg p-3">
              <div className="text-cyan-300/60 text-xs mb-1">Action Recommandée</div>
              <div className="text-white font-medium">{entity.recommended_action.replace(/_/g, " ")}</div>
            </div>
            <div className="bg-slate-900 border border-pink-600/20 rounded-lg p-3">
              <div className="text-cyan-300/60 text-xs mb-1">Patron Augmentation</div>
              <div className="text-white font-medium">{entity.augmentation_pattern.replace(/_/g, " ")}</div>
            </div>
            <div className="flex gap-2 flex-wrap">
              {entity.is_in_augmentation_crisis && (
                <span className="px-2 py-1 rounded bg-pink-950 text-pink-400 text-xs font-medium">
                  CRISE AUGMENTATION
                </span>
              )}
              {entity.requires_augmentation_intervention && (
                <span className="px-2 py-1 rounded bg-cyan-950 text-cyan-400 text-xs font-medium">
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

export default function PostHumanAugmentationDashboard() {
  const [data, setData] = useState<{ entities: Entity[]; summary: Summary } | null>(null);
  const [riskFilter, setRiskFilter] = useState<string>("all");
  const [patFilter, setPatFilter] = useState<string>("all");
  const [selected, setSelected] = useState<Entity | null>(null);

  useEffect(() => {
    fetch("/api/post-human-augmentation-engine")
      .then(r => r.json())
      .then(setData)
      .catch(console.error);
  }, []);

  if (!data) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center">
        <div className="text-cyan-400 text-lg animate-pulse">
          Initialisation du Moteur Post-Humain...
        </div>
      </div>
    );
  }

  const { entities, summary } = data;
  const filtered = entities.filter(
    e =>
      (riskFilter === "all" || e.augmentation_risk === riskFilter) &&
      (patFilter === "all" || e.augmentation_pattern === patFilter)
  );

  const dists = [
    { title: "Niveau Risque",          counts: summary.risk_counts,     colors: RISK_COLORS    },
    { title: "Patron Augmentation",    counts: summary.pattern_counts,  colors: PAT_COLORS     },
    { title: "Sévérité Transition",    counts: summary.severity_counts, colors: SEV_COLORS     },
    { title: "Action Activée",         counts: summary.action_counts,   colors: ACTION_COLORS  },
  ] as Array<{ title: string; counts: Record<string, number>; colors: Record<string, string> }>;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {selected && <DetailModal entity={selected} onClose={() => setSelected(null)} />}

      <div>
        <h1 className="text-2xl font-bold text-cyan-400">
          Post-Human Augmentation & Transhumanist Strategy Engine
        </h1>
        <p className="text-cyan-300/50 text-sm mt-1">
          Adoption · Équité · Intégrité Biologique · Transition Post-Humaine
        </p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {(
          [
            ["Entités Analysées",              summary.total,                                          "text-cyan-400"],
            ["Crises Augmentation",            summary.augmentation_crisis_count,                      "text-pink-500"],
            ["Interventions Requises",         summary.augmentation_intervention_count,                "text-pink-400"],
            ["Composite Moy.",                 summary.avg_augmentation_composite.toFixed(1),          "text-cyan-300"],
            ["Indice Disruption Moy.",         summary.avg_estimated_augmentation_disruption_index.toFixed(2) + "/10", "text-pink-400"],
            ["Score Adoption Moy.",            summary.avg_adoption_score.toFixed(1),                  "text-cyan-400"],
          ] as [string, string | number, string][]
        ).map(([l, v, c]) => (
          <div
            key={String(l)}
            className="bg-slate-900 border border-pink-600/30 rounded-xl p-3 text-center"
          >
            <div className={`text-xl font-bold ${c}`}>{v}</div>
            <div className="text-xs text-cyan-300/40 mt-0.5 leading-tight">{l}</div>
          </div>
        ))}
      </div>

      {/* Gauge Rings */}
      <div className="bg-slate-900 border border-pink-600/30 rounded-xl p-5">
        <div className="grid grid-cols-4 gap-4">
          <GaugeRing value={summary.avg_adoption_score}    label="Score Adoption"            color="#06b6d4" />
          <GaugeRing value={summary.avg_equity_score}      label="Fracture Équité"           color="#ec4899" />
          <GaugeRing value={summary.avg_integrity_score}   label="Risque Intégrité Bio."     color="#a855f7" />
          <GaugeRing value={summary.avg_transition_score}  label="Lag Transition"            color="#f97316" />
        </div>
      </div>

      {/* Distribution Bars */}
      <div className="bg-slate-900 border border-pink-600/30 rounded-xl p-5 grid grid-cols-1 md:grid-cols-2 gap-5">
        {dists.map(d => (
          <DistBar key={d.title} {...d} />
        ))}
      </div>

      {/* Filter Pills */}
      <div className="flex flex-wrap gap-2">
        {["all", "low", "moderate", "high", "critical"].map(r => (
          <button
            key={r}
            onClick={() => setRiskFilter(r)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${
              riskFilter === r
                ? "bg-pink-900 border-pink-700 text-white"
                : "bg-slate-900 border-pink-600/30 text-cyan-400/70 hover:text-white"
            }`}
          >
            {r}
          </button>
        ))}
        <span className="w-px h-5 self-center bg-pink-600/30" />
        {[
          "all",
          "none",
          "cognitive_arms_race",
          "identity_collapse",
          "augmentation_divide",
          "regulatory_vacuum",
          "biological_sovereignty_loss",
        ].map(p => (
          <button
            key={p}
            onClick={() => setPatFilter(p)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${
              patFilter === p
                ? "bg-cyan-950 border-cyan-700 text-white"
                : "bg-slate-900 border-pink-600/30 text-cyan-400/70 hover:text-white"
            }`}
          >
            {p.replace(/_/g, " ")}
          </button>
        ))}
      </div>

      {/* Entity Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {filtered.map(e => (
          <div
            key={e.id}
            onClick={() => setSelected(e)}
            className="bg-slate-900 border border-pink-600/30 rounded-xl p-4 cursor-pointer hover:border-cyan-500 transition-colors"
          >
            <div className="flex items-center justify-between mb-1">
              <span className="font-bold text-white">{e.id}</span>
              <span className="text-xs text-cyan-400/60">{e.region}</span>
            </div>
            <div className="text-xs text-slate-500 mb-2 capitalize">
              {e.augmentation_domain.replace(/_/g, " ")}
            </div>
            <div className="flex gap-1 mb-3 flex-wrap">
              <span
                className={`px-2 py-0.5 rounded text-xs font-medium ${
                  RISK_BADGE[e.augmentation_risk as keyof typeof RISK_BADGE] ||
                  "bg-slate-700 text-slate-300"
                }`}
              >
                {e.augmentation_risk}
              </span>
              <span
                className={`px-2 py-0.5 rounded text-xs font-medium ${
                  SEV_BADGE[e.augmentation_severity as keyof typeof SEV_BADGE] ||
                  "bg-slate-700 text-slate-300"
                }`}
              >
                {e.augmentation_severity.replace(/_/g, " ")}
              </span>
            </div>
            <div className="text-2xl font-black text-white mb-1">
              {e.augmentation_composite.toFixed(1)}
            </div>
            <div className="text-xs text-pink-400/60 mb-2 capitalize">
              {e.augmentation_pattern.replace(/_/g, " ")}
            </div>
            <div className="text-xs text-cyan-400 font-medium mb-2">
              {e.recommended_action.replace(/_/g, " ")}
            </div>
            <div className="flex gap-1 flex-wrap">
              {e.is_in_augmentation_crisis && (
                <span className="px-1.5 py-0.5 rounded bg-pink-950 text-pink-400 text-xs">
                  CRISE
                </span>
              )}
              {e.requires_augmentation_intervention && (
                <span className="px-1.5 py-0.5 rounded bg-cyan-950 text-cyan-400 text-xs">
                  INTERVENTION
                </span>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
