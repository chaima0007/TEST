"use client";
import { useEffect, useState } from "react";

type EntityResult = {
  entity_id: string;
  political_domain: string;
  region: string;
  manipulation_score: number;
  identity_score: number;
  trauma_score: number;
  structural_score: number;
  composite_score: number;
  risk_level: string;
  psycho_pattern: string;
  severity: string;
  recommended_action: string;
  signal: string;
  mass_anxiety_political_exploitation: number;
  democratic_disillusionment_weaponization: number;
};

type ApiData = {
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
  avg_estimated_psychopolitics_index: number;
  avg_manipulation_score: number;
  avg_identity_score: number;
  avg_trauma_score: number;
  avg_structural_score: number;
  results: EntityResult[];
};

function GaugeRing({ value, label, color }: { value: number; label: string; color: string }) {
  const r = 36;
  const circ = 2 * Math.PI * r;
  const fill = circ * (1 - value / 100);
  return (
    <div className="flex flex-col items-center gap-1">
      <svg width="88" height="88" viewBox="0 0 88 88">
        <circle cx="44" cy="44" r={r} fill="none" stroke="#0f172a" strokeWidth="8" />
        <circle cx="44" cy="44" r={r} fill="none" stroke={color} strokeWidth="8"
          strokeDasharray={circ} strokeDashoffset={fill}
          strokeLinecap="round" transform="rotate(-90 44 44)" />
        <text x="44" y="49" textAnchor="middle" fill="white" fontSize="13" fontWeight="bold">
          {Math.round(value)}
        </text>
      </svg>
      <span className="text-xs text-violet-300/70 text-center">{label}</span>
    </div>
  );
}

function DistBar({ title, counts, colors }: { title: string; counts: Record<string, number>; colors: Record<string, string> }) {
  const total = Object.values(counts).reduce((a, b) => a + b, 0) || 1;
  return (
    <div className="flex flex-col gap-1">
      <span className="text-xs text-violet-300/70 font-medium">{title}</span>
      <div className="flex h-3 rounded overflow-hidden gap-px">
        {Object.entries(counts).map(([k, v]) => (
          <div key={k} style={{ width: `${(v / total) * 100}%`, background: colors[k] || "#475569" }} title={`${k}: ${v}`} />
        ))}
      </div>
      <div className="flex flex-wrap gap-x-3 gap-y-0.5">
        {Object.entries(counts).map(([k, v]) => (
          <span key={k} className="text-xs text-violet-300/60">
            <span style={{ color: colors[k] || "#94a3b8" }}>■</span> {k.replace(/_/g, " ")} {v}
          </span>
        ))}
      </div>
    </div>
  );
}

const RISK_COLORS: Record<string, string> = {
  low:      "#10b981",
  moderate: "#f59e0b",
  high:     "#f97316",
  critical: "#ef4444",
};

const PATTERN_COLORS: Record<string, string> = {
  none:                            "#10b981",
  mass_psychosis_politics:         "#7c3aed",
  tribal_warfare_activation:       "#dc2626",
  trauma_based_control:            "#9333ea",
  authoritarian_personality_cult:  "#c026d3",
  democratic_psychological_collapse: "#be123c",
};

const SEVERITY_COLORS: Record<string, string> = {
  politique_psychologie_contenue:        "#10b981",
  exploitation_psychologique_structurelle: "#f59e0b",
  manipulation_masse_majeure:            "#f97316",
  "psychopolitique_systémique_avancée":  "#ef4444",
};

const ACTION_COLORS: Record<string, string> = {
  veille_psychopolitique_continue:              "#10b981",
  "renforcement_pensée_critique_citoyenne":      "#06b6d4",
  "contre-mesures_manipulation_psychopolitique": "#f97316",
  "résilience_psychologique_collective_urgente": "#ef4444",
};

const RISK_BADGE: Record<string, string> = {
  low:      "bg-emerald-900 text-emerald-300",
  moderate: "bg-amber-900 text-amber-300",
  high:     "bg-orange-900 text-orange-300",
  critical: "bg-red-950 text-red-400",
};

const PATTERN_BADGE: Record<string, string> = {
  none:                            "bg-slate-800 text-slate-400",
  mass_psychosis_politics:         "bg-violet-950 text-violet-300",
  tribal_warfare_activation:       "bg-red-950 text-red-400",
  trauma_based_control:            "bg-purple-950 text-purple-300",
  authoritarian_personality_cult:  "bg-fuchsia-950 text-fuchsia-300",
  democratic_psychological_collapse: "bg-rose-950 text-rose-400",
};

function DetailModal({ entity, onClose }: { entity: EntityResult; onClose: () => void }) {
  const [tab, setTab] = useState<"scores" | "signal" | "action">("scores");

  useEffect(() => {
    const h = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", h);
    return () => window.removeEventListener("keydown", h);
  }, [onClose]);

  const riskColor = RISK_COLORS[entity.risk_level] ?? "#94a3b8";

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80" onClick={onClose}>
      <div className="bg-slate-950 border border-violet-700/30 rounded-xl w-full max-w-lg p-6 shadow-2xl" onClick={e => e.stopPropagation()}>
        <div className="flex items-center justify-between mb-4">
          <div>
            <span className="text-lg font-bold text-white">{entity.entity_id}</span>
            <span className="ml-2 text-violet-400 text-xs">{entity.region}</span>
            <span className="ml-2 text-slate-500 text-xs">{entity.political_domain.replace(/_/g, " ")}</span>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl leading-none">✕</button>
        </div>

        <div className="flex gap-2 mb-4">
          {(["scores", "signal", "action"] as const).map(t => (
            <button key={t} onClick={() => setTab(t)}
              className={`px-3 py-1 rounded text-xs font-medium transition-colors ${tab === t ? "bg-violet-900 text-white" : "bg-slate-900 text-slate-400 hover:text-white"}`}>
              {t === "scores" ? "Scores" : t === "signal" ? "Signal" : "Action"}
            </button>
          ))}
        </div>

        {tab === "scores" && (
          <div className="grid grid-cols-2 gap-3 text-sm">
            {([
              ["Manipulation",  entity.manipulation_score,  "#ef4444"],
              ["Identité",      entity.identity_score,      "#a855f7"],
              ["Trauma",        entity.trauma_score,        "#f97316"],
              ["Structurel",    entity.structural_score,    "#06b6d4"],
            ] as [string, number, string][]).map(([l, v, c]) => (
              <div key={l} className="bg-slate-900 border border-violet-700/20 rounded-lg p-3">
                <div className="text-violet-300/60 text-xs mb-1">{l}</div>
                <div className="text-white font-bold text-lg">{v.toFixed(1)}</div>
                <div className="h-1.5 rounded mt-1 bg-slate-800">
                  <div className="h-1.5 rounded" style={{ width: `${Math.min(v, 100)}%`, background: c }} />
                </div>
              </div>
            ))}
            <div className="col-span-2 bg-slate-900 border border-violet-700/20 rounded-lg p-3">
              <div className="text-violet-300/60 text-xs mb-1">Score Composite Psychopolitique</div>
              <div className="font-bold text-2xl" style={{ color: riskColor }}>{entity.composite_score.toFixed(1)}</div>
            </div>
          </div>
        )}

        {tab === "signal" && (
          <div className="bg-slate-900 border border-violet-700/20 rounded-lg p-4 text-sm text-slate-200 leading-relaxed">
            {entity.signal}
            <div className="mt-3 flex gap-2 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[entity.risk_level] || "bg-slate-700 text-slate-300"}`}>
                {entity.risk_level}
              </span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${PATTERN_BADGE[entity.psycho_pattern] || "bg-slate-800 text-slate-400"}`}>
                {entity.psycho_pattern.replace(/_/g, " ")}
              </span>
            </div>
            <div className="mt-3 text-xs text-slate-500">
              <span>Anxiété masse: {Math.round(entity.mass_anxiety_political_exploitation * 100)}%</span>
              <span className="mx-2">·</span>
              <span>Désillusion démocratie: {Math.round(entity.democratic_disillusionment_weaponization * 100)}%</span>
            </div>
          </div>
        )}

        {tab === "action" && (
          <div className="space-y-3 text-sm">
            <div className="bg-slate-900 border border-violet-700/20 rounded-lg p-3">
              <div className="text-violet-300/60 text-xs mb-1">Action Recommandée</div>
              <div className="text-white font-medium">{entity.recommended_action.replace(/_/g, " ")}</div>
            </div>
            <div className="bg-slate-900 border border-violet-700/20 rounded-lg p-3">
              <div className="text-violet-300/60 text-xs mb-1">Sévérité Psychopolitique</div>
              <div className="text-white font-medium">{entity.severity.replace(/_/g, " ")}</div>
            </div>
            <div className="bg-slate-900 border border-violet-700/20 rounded-lg p-3">
              <div className="text-violet-300/60 text-xs mb-1">Schéma Psychologique</div>
              <div className="text-white font-medium">{entity.psycho_pattern.replace(/_/g, " ")}</div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function PsychopoliticsDashboard() {
  const [data, setData]           = useState<ApiData | null>(null);
  const [filter, setFilter]       = useState<string>("all");
  const [patFilter, setPatFilter] = useState<string>("all");
  const [selected, setSelected]   = useState<EntityResult | null>(null);

  useEffect(() => {
    fetch("/api/psychopolitics-engine")
      .then(r => r.json())
      .then(setData)
      .catch(console.error);
  }, []);

  if (!data) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-violet-400 text-lg animate-pulse">Initialisation du Moteur Psychopolitique — Module 344...</div>
    </div>
  );

  const filtered = (data.results || []).filter(e =>
    (filter === "all" || e.risk_level === filter) &&
    (patFilter === "all" || e.psycho_pattern === patFilter)
  );

  const dists = [
    { title: "Niveau Risque Psychopolitique",  counts: data.risk_distribution,     colors: RISK_COLORS     },
    { title: "Schéma Psychologique",           counts: data.pattern_distribution,  colors: PATTERN_COLORS  },
    { title: "Sévérité Psychopolitique",       counts: data.severity_distribution, colors: SEVERITY_COLORS },
    { title: "Action Déclenchée",              counts: data.action_distribution,   colors: ACTION_COLORS   },
  ];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {selected && <DetailModal entity={selected} onClose={() => setSelected(null)} />}

      <div>
        <h1 className="text-2xl font-bold text-violet-400">Psychopolitique &amp; Psychologie des Masses — Module 344</h1>
        <p className="text-violet-300/50 text-sm mt-1">Manipulation · Identité · Trauma · Structurel</p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {([
          ["Total Systèmes",           data.total_entities,                                             "text-violet-400"],
          ["Psychopolitique Critique", data.critical_count,                                             "text-red-400"],
          ["Manipulation Majeure",     data.high_count,                                                 "text-orange-400"],
          ["Composite Moyen",          `${data.avg_composite?.toFixed(1) ?? "—"}`,                     "text-amber-400"],
          ["Index Psychopolitique",    `${data.avg_estimated_psychopolitics_index?.toFixed(2) ?? "—"}/10`, "text-crimson-400 text-rose-400"],
          ["Manipulation Moyenne",     `${data.avg_manipulation_score?.toFixed(1) ?? "—"}`,             "text-fuchsia-400"],
        ] as [string, string | number, string][]).map(([l, v, c]) => (
          <div key={l} className="bg-slate-900 border border-violet-700/30 rounded-xl p-3 text-center">
            <div className={`text-xl font-bold ${c}`}>{v}</div>
            <div className="text-xs text-violet-300/40 mt-0.5 leading-tight">{l}</div>
          </div>
        ))}
      </div>

      {/* Gauge Rings */}
      <div className="bg-slate-900 border border-violet-700/30 rounded-xl p-5">
        <div className="grid grid-cols-4 gap-4">
          <GaugeRing value={data.avg_manipulation_score ?? 0} label="Manipulation"  color="#ef4444" />
          <GaugeRing value={data.avg_identity_score    ?? 0} label="Identité"       color="#a855f7" />
          <GaugeRing value={data.avg_trauma_score      ?? 0} label="Trauma"         color="#f97316" />
          <GaugeRing value={data.avg_structural_score  ?? 0} label="Structurel"     color="#06b6d4" />
        </div>
      </div>

      {/* Distribution Bars */}
      <div className="bg-slate-900 border border-violet-700/30 rounded-xl p-5 grid grid-cols-1 md:grid-cols-2 gap-5">
        {dists.map(d => <DistBar key={d.title} {...d} />)}
      </div>

      {/* Filter Pills */}
      <div className="flex flex-wrap gap-2">
        {["all", "low", "moderate", "high", "critical"].map(r => (
          <button key={r} onClick={() => setFilter(r)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${filter === r ? "bg-violet-900 border-violet-700 text-white" : "bg-slate-900 border-violet-700/30 text-violet-400/70 hover:text-white"}`}>
            {r}
          </button>
        ))}
        <span className="w-px h-5 self-center bg-violet-700/30" />
        {["all", "none", "mass_psychosis_politics", "tribal_warfare_activation", "trauma_based_control", "authoritarian_personality_cult", "democratic_psychological_collapse"].map(p => (
          <button key={p} onClick={() => setPatFilter(p)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${patFilter === p ? "bg-violet-950 border-violet-800 text-white" : "bg-slate-900 border-violet-700/30 text-violet-400/70 hover:text-white"}`}>
            {p.replace(/_/g, " ")}
          </button>
        ))}
      </div>

      {/* Entity Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {filtered.map(e => (
          <div key={e.entity_id} onClick={() => setSelected(e)}
            className="bg-slate-900 border border-violet-700/30 rounded-xl p-4 cursor-pointer hover:border-violet-500 transition-colors">
            <div className="flex items-center justify-between mb-1">
              <span className="font-bold text-white">{e.entity_id}</span>
              <span className="text-xs text-violet-400/70">{e.region}</span>
            </div>
            <div className="text-xs text-slate-500 mb-2 capitalize">{e.political_domain.replace(/_/g, " ")}</div>
            <div className="flex gap-1 mb-3 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[e.risk_level] || "bg-slate-700 text-slate-300"}`}>
                {e.risk_level}
              </span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${PATTERN_BADGE[e.psycho_pattern] || "bg-slate-800 text-slate-400"}`}>
                {e.psycho_pattern.replace(/_/g, " ")}
              </span>
            </div>
            <div className="text-2xl font-black text-white mb-1" style={{ color: RISK_COLORS[e.risk_level] ?? "#fff" }}>
              {e.composite_score.toFixed(1)}
            </div>
            <div className="text-xs text-violet-400/60 mb-2 capitalize">{e.severity.replace(/_/g, " ")}</div>
            <div className="text-xs text-rose-400 font-medium mb-2">{e.recommended_action.replace(/_/g, " ")}</div>
            <div className="text-xs text-slate-500 italic line-clamp-2">{e.signal}</div>
          </div>
        ))}
      </div>
    </div>
  );
}
