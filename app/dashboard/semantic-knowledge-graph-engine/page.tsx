"use client";
import { useEffect, useState } from "react";

type Entity = {
  entity_id: string;
  region: string;
  graph_domain: string;
  kg_risk: string;
  kg_pattern: string;
  kg_severity: string;
  recommended_action: string;
  coherence_score: number;
  connectivity_score: number;
  freshness_score: number;
  sovereignty_score: number;
  kg_composite: number;
  is_in_kg_crisis: boolean;
  requires_kg_intervention: boolean;
  kg_signal: string;
};

type Summary = {
  total: number;
  risk_counts: Record<string, number>;
  pattern_counts: Record<string, number>;
  severity_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_kg_composite: number;
  kg_crisis_count: number;
  kg_intervention_count: number;
  avg_coherence_score: number;
  avg_connectivity_score: number;
  avg_freshness_score: number;
  avg_sovereignty_score: number;
  avg_estimated_kg_risk_index: number;
};

function GaugeRing({ value, label, color }: { value: number; label: string; color: string }) {
  const r = 36;
  const circ = 2 * Math.PI * r;
  const fill = circ * (1 - value / 100);
  return (
    <div className="flex flex-col items-center gap-1">
      <svg width="88" height="88" viewBox="0 0 88 88">
        <circle cx="44" cy="44" r={r} fill="none" stroke="#0c1428" strokeWidth="8" />
        <circle
          cx="44" cy="44" r={r} fill="none" stroke={color} strokeWidth="8"
          strokeDasharray={circ} strokeDashoffset={fill}
          strokeLinecap="round" transform="rotate(-90 44 44)"
        />
        <text x="44" y="49" textAnchor="middle" fill="white" fontSize="13" fontWeight="bold">
          {Math.round(value)}
        </text>
      </svg>
      <span className="text-xs text-indigo-300/70 text-center">{label}</span>
    </div>
  );
}

function DistBar({ title, counts, colors }: { title: string; counts: Record<string, number>; colors: Record<string, string> }) {
  const total = Object.values(counts).reduce((a, b) => a + b, 0) || 1;
  return (
    <div className="flex flex-col gap-1">
      <span className="text-xs text-indigo-300/70 font-medium">{title}</span>
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
          <span key={k} className="text-xs text-indigo-300/60">
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
  high: "#6366f1",
  critical: "#ef4444",
};

const PAT_COLORS: Record<string, string> = {
  none: "#10b981",
  ontology_collapse: "#7c3aed",
  knowledge_fragmentation: "#6366f1",
  semantic_pollution: "#f97316",
  sovereignty_breach: "#ef4444",
  graph_staleness: "#a16207",
};

const SEV_COLORS: Record<string, string> = {
  knowledge_optimum: "#10b981",
  developing_drift: "#f59e0b",
  high_degradation: "#6366f1",
  graph_collapse: "#7f1d1d",
};

const ACTION_COLORS: Record<string, string> = {
  no_action: "#10b981",
  kg_monitoring: "#06b6d4",
  graph_restructuring: "#6366f1",
  knowledge_cleansing: "#f97316",
  kg_emergency_reconstruction: "#ef4444",
};

const RISK_BADGE: Record<string, string> = {
  low: "bg-emerald-900 text-emerald-300",
  moderate: "bg-amber-900 text-amber-300",
  high: "bg-indigo-900 text-indigo-300",
  critical: "bg-red-950 text-red-400",
};

const SEV_BADGE: Record<string, string> = {
  knowledge_optimum: "bg-emerald-900 text-emerald-300",
  developing_drift: "bg-amber-900 text-amber-300",
  high_degradation: "bg-indigo-900 text-indigo-300",
  graph_collapse: "bg-red-950 text-red-400",
};

function DetailModal({ entity, onClose }: { entity: Entity; onClose: () => void }) {
  const [tab, setTab] = useState<"scores" | "signal" | "action">("scores");

  useEffect(() => {
    const h = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", h);
    return () => window.removeEventListener("keydown", h);
  }, [onClose]);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80" onClick={onClose}>
      <div
        className="bg-slate-950 border border-emerald-600/30 rounded-xl w-full max-w-lg p-6 shadow-2xl"
        onClick={e => e.stopPropagation()}
      >
        <div className="flex items-center justify-between mb-4">
          <div>
            <span className="text-lg font-bold text-white">{entity.entity_id}</span>
            <span className="ml-2 text-indigo-400 text-xs">{entity.region}</span>
            <span className="ml-2 text-slate-500 text-xs">{entity.graph_domain.replace(/_/g, " ")}</span>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl leading-none">✕</button>
        </div>

        <div className="flex gap-2 mb-4">
          {(["scores", "signal", "action"] as const).map(t => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`px-3 py-1 rounded text-xs font-medium transition-colors ${
                tab === t
                  ? "bg-indigo-900 text-white"
                  : "bg-slate-900 text-slate-400 hover:text-white"
              }`}
            >
              {t.charAt(0).toUpperCase() + t.slice(1)}
            </button>
          ))}
        </div>

        {tab === "scores" && (
          <div className="grid grid-cols-2 gap-3 text-sm">
            {([
              ["Cohérence",     entity.coherence_score,    "#6366f1"],
              ["Connectivité",  entity.connectivity_score, "#10b981"],
              ["Fraîcheur",     entity.freshness_score,    "#f59e0b"],
              ["Souveraineté",  entity.sovereignty_score,  "#06b6d4"],
            ] as [string, number, string][]).map(([l, v, c]) => (
              <div key={l} className="bg-slate-900 border border-emerald-600/20 rounded-lg p-3">
                <div className="text-indigo-300/60 text-xs mb-1">{l}</div>
                <div className="text-white font-bold text-lg">{Number(v).toFixed(1)}</div>
                <div className="h-1.5 rounded mt-1 bg-slate-800">
                  <div className="h-1.5 rounded" style={{ width: `${Math.min(Number(v), 100)}%`, background: c }} />
                </div>
              </div>
            ))}
            <div className="col-span-2 bg-slate-900 border border-emerald-600/20 rounded-lg p-3">
              <div className="text-indigo-300/60 text-xs mb-1">Composite KG</div>
              <div className="text-white font-bold text-2xl">{entity.kg_composite.toFixed(1)}</div>
            </div>
          </div>
        )}

        {tab === "signal" && (
          <div className="bg-slate-900 border border-emerald-600/20 rounded-lg p-4 text-sm text-slate-200 leading-relaxed">
            {entity.kg_signal}
            <div className="mt-3 flex gap-2 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[entity.kg_risk] || "bg-slate-700 text-slate-300"}`}>
                {entity.kg_risk}
              </span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[entity.kg_severity] || "bg-slate-700 text-slate-300"}`}>
                {entity.kg_severity.replace(/_/g, " ")}
              </span>
            </div>
          </div>
        )}

        {tab === "action" && (
          <div className="space-y-3 text-sm">
            <div className="bg-slate-900 border border-emerald-600/20 rounded-lg p-3">
              <div className="text-indigo-300/60 text-xs mb-1">Action Recommandée</div>
              <div className="text-white font-medium">{entity.recommended_action.replace(/_/g, " ")}</div>
            </div>
            <div className="bg-slate-900 border border-emerald-600/20 rounded-lg p-3">
              <div className="text-indigo-300/60 text-xs mb-1">Patron KG</div>
              <div className="text-white font-medium">{entity.kg_pattern.replace(/_/g, " ")}</div>
            </div>
            <div className="flex gap-2 flex-wrap">
              {entity.is_in_kg_crisis && (
                <span className="px-2 py-1 rounded bg-red-950 text-red-400 text-xs font-medium">CRISE KG</span>
              )}
              {entity.requires_kg_intervention && (
                <span className="px-2 py-1 rounded bg-indigo-950 text-indigo-400 text-xs font-medium">INTERVENTION REQ.</span>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function SemanticKnowledgeGraphDashboard() {
  const [data, setData]         = useState<{ entities: Entity[]; summary: Summary } | null>(null);
  const [filter, setFilter]     = useState<string>("all");
  const [patFilter, setPatFilter] = useState<string>("all");
  const [selected, setSelected] = useState<Entity | null>(null);

  useEffect(() => {
    fetch("/api/semantic-knowledge-graph-engine")
      .then(r => r.json())
      .then(setData)
      .catch(console.error);
  }, []);

  if (!data) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-indigo-400 text-lg animate-pulse">Initialisation du Moteur Graphe de Connaissance...</div>
    </div>
  );

  const { entities, summary } = data;
  const filtered = entities.filter(e =>
    (filter === "all" || e.kg_risk === filter) &&
    (patFilter === "all" || e.kg_pattern === patFilter)
  );

  const dists = [
    { title: "Niveau Risque KG",      counts: summary.risk_counts,     colors: RISK_COLORS    },
    { title: "Patron Sémantique",      counts: summary.pattern_counts,  colors: PAT_COLORS     },
    { title: "Sévérité Graphe",        counts: summary.severity_counts, colors: SEV_COLORS     },
    { title: "Action Déclenchée",      counts: summary.action_counts,   colors: ACTION_COLORS  },
  ] as Array<{ title: string; counts: Record<string, number>; colors: Record<string, string> }>;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {selected && <DetailModal entity={selected} onClose={() => setSelected(null)} />}

      <div>
        <h1 className="text-2xl font-bold text-indigo-400">
          Semantic Web &amp; Knowledge Graph Intelligence Engine
        </h1>
        <p className="text-indigo-300/50 text-sm mt-1">
          Cohérence Ontologique · Connectivité · Fraîcheur · Souveraineté des Connaissances
        </p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {([
          ["Entités Analysées",         summary.total,                                   "text-indigo-400"],
          ["Crises KG Actives",          summary.kg_crisis_count,                         "text-red-400"],
          ["Interventions Requises",     summary.kg_intervention_count,                   "text-indigo-300"],
          ["Composite KG Moy.",          summary.avg_kg_composite.toFixed(1),             "text-amber-400"],
          ["Indice Risque KG Moy.",      summary.avg_estimated_kg_risk_index.toFixed(2),  "text-emerald-400"],
          ["Cohérence Moy.",             summary.avg_coherence_score.toFixed(1),           "text-indigo-400"],
        ] as [string, string | number, string][]).map(([l, v, c]) => (
          <div key={String(l)} className="bg-slate-900 border border-emerald-600/30 rounded-xl p-3 text-center">
            <div className={`text-xl font-bold ${c}`}>{v}</div>
            <div className="text-xs text-indigo-300/40 mt-0.5 leading-tight">{l}</div>
          </div>
        ))}
      </div>

      {/* Gauge Rings */}
      <div className="bg-slate-900 border border-emerald-600/30 rounded-xl p-5">
        <div className="grid grid-cols-4 gap-4">
          <GaugeRing value={summary.avg_coherence_score}    label="Cohérence Ontologique"  color="#6366f1" />
          <GaugeRing value={summary.avg_connectivity_score} label="Connectivité Graphe"     color="#10b981" />
          <GaugeRing value={summary.avg_freshness_score}    label="Pollution / Dérive"      color="#f59e0b" />
          <GaugeRing value={summary.avg_sovereignty_score}  label="Souveraineté Savoir"     color="#06b6d4" />
        </div>
      </div>

      {/* Distribution Bars */}
      <div className="bg-slate-900 border border-emerald-600/30 rounded-xl p-5 grid grid-cols-1 md:grid-cols-2 gap-5">
        {dists.map(d => <DistBar key={d.title} {...d} />)}
      </div>

      {/* Filter Pills */}
      <div className="flex flex-wrap gap-2">
        {["all", "low", "moderate", "high", "critical"].map(r => (
          <button
            key={r}
            onClick={() => setFilter(r)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${
              filter === r
                ? "bg-indigo-900 border-indigo-700 text-white"
                : "bg-slate-900 border-emerald-600/30 text-indigo-400/70 hover:text-white"
            }`}
          >
            {r}
          </button>
        ))}
        <span className="w-px h-5 self-center bg-emerald-600/30" />
        {["all", "none", "ontology_collapse", "knowledge_fragmentation", "semantic_pollution", "sovereignty_breach", "graph_staleness"].map(p => (
          <button
            key={p}
            onClick={() => setPatFilter(p)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${
              patFilter === p
                ? "bg-indigo-950 border-indigo-800 text-white"
                : "bg-slate-900 border-emerald-600/30 text-indigo-400/70 hover:text-white"
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
            key={e.entity_id}
            onClick={() => setSelected(e)}
            className="bg-slate-900 border border-emerald-600/30 rounded-xl p-4 cursor-pointer hover:border-indigo-500 transition-colors"
          >
            <div className="flex items-center justify-between mb-1">
              <span className="font-bold text-white">{e.entity_id}</span>
              <span className="text-xs text-indigo-400/60">{e.region}</span>
            </div>
            <div className="text-xs text-slate-500 mb-2 capitalize">{e.graph_domain.replace(/_/g, " ")}</div>
            <div className="flex gap-1 mb-3 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[e.kg_risk] || "bg-slate-700 text-slate-300"}`}>
                {e.kg_risk}
              </span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[e.kg_severity] || "bg-slate-700 text-slate-300"}`}>
                {e.kg_severity.replace(/_/g, " ")}
              </span>
            </div>
            <div className="text-2xl font-black text-white mb-1">{e.kg_composite.toFixed(1)}</div>
            <div className="text-xs text-indigo-400/60 mb-2 capitalize">{e.kg_pattern.replace(/_/g, " ")}</div>
            <div className="text-xs text-emerald-400 font-medium mb-2">
              IKG: {(e.kg_composite / 100 * 10).toFixed(2)} / 10
            </div>
            <div className="flex gap-1 flex-wrap">
              {e.is_in_kg_crisis && (
                <span className="px-1.5 py-0.5 rounded bg-red-950 text-red-400 text-xs">CRISE KG</span>
              )}
              {e.requires_kg_intervention && (
                <span className="px-1.5 py-0.5 rounded bg-indigo-950 text-indigo-400 text-xs">INTERVENTION</span>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
