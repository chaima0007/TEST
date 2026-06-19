"use client";
import { useEffect, useState } from "react";

type NBCEntity = {
  entity_id: string;
  region: string;
  technology_type: string;
  neural_risk: string;
  neural_pattern: string;
  neural_severity: string;
  recommended_action: string;
  privacy_score: number;
  security_score: number;
  rights_score: number;
  societal_score: number;
  neural_composite: number;
  is_neural_crisis: boolean;
  requires_neural_intervention: boolean;
  neural_signal: string;
};

type Summary = {
  total: number;
  risk_counts: Record<string, number>;
  pattern_counts: Record<string, number>;
  severity_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_neural_composite: number;
  neural_crisis_count: number;
  neural_intervention_count: number;
  avg_privacy_score: number;
  avg_security_score: number;
  avg_rights_score: number;
  avg_societal_score: number;
  avg_estimated_neural_risk_index: number;
};

// ── GaugeRing ──────────────────────────────────────────────────────────────────
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
      <span className="text-xs text-slate-400 text-center">{label}</span>
    </div>
  );
}

// ── DistBar ────────────────────────────────────────────────────────────────────
function DistBar({ title, counts, colors }: { title: string; counts: Record<string, number>; colors: Record<string, string> }) {
  const total = Object.values(counts).reduce((a, b) => a + b, 0) || 1;
  return (
    <div className="flex flex-col gap-1">
      <span className="text-xs text-slate-400 font-medium">{title}</span>
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
          <span key={k} className="text-xs text-slate-400">
            <span style={{ color: colors[k] || "#94a3b8" }}>■</span> {k} {v}
          </span>
        ))}
      </div>
    </div>
  );
}

// ── Color maps ─────────────────────────────────────────────────────────────────
const RISK_COLORS: Record<string, string> = {
  low: "#10b981", moderate: "#f59e0b", high: "#f97316", critical: "#ef4444",
};
const PAT_COLORS: Record<string, string> = {
  none:                        "#10b981",
  neural_sovereignty_breach:   "#ec4899",
  brain_hacking_attack:        "#ef4444",
  neurorights_violation:       "#f97316",
  cognitive_inequality_crisis: "#a855f7",
  military_neuroweapon:        "#7c3aed",
};
const SEV_COLORS: Record<string, string> = {
  neural_safe:      "#10b981",
  neural_concern:   "#f59e0b",
  high_neural_risk: "#f97316",
  neural_emergency: "#ef4444",
};
const ACT_COLORS: Record<string, string> = {
  no_action:                      "#10b981",
  neural_monitoring:              "#06b6d4",
  neurorights_protection_program: "#a855f7",
  neural_security_lockdown:       "#f97316",
  neural_emergency_shutdown:      "#ef4444",
};
const RISK_BADGE: Record<string, string> = {
  low:      "bg-emerald-900 text-emerald-300",
  moderate: "bg-amber-900 text-amber-300",
  high:     "bg-orange-900 text-orange-300",
  critical: "bg-red-900 text-red-300",
};
const SEV_BADGE: Record<string, string> = {
  neural_safe:      "bg-emerald-900 text-emerald-300",
  neural_concern:   "bg-amber-900 text-amber-300",
  high_neural_risk: "bg-orange-900 text-orange-300",
  neural_emergency: "bg-red-900 text-red-300",
};

// ── DetailModal ────────────────────────────────────────────────────────────────
function DetailModal({ entity, onClose }: { entity: NBCEntity; onClose: () => void }) {
  const [tab, setTab] = useState<"scores" | "signal" | "action">("scores");

  useEffect(() => {
    const h = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", h);
    return () => window.removeEventListener("keydown", h);
  }, [onClose]);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70" onClick={onClose}>
      <div
        className="bg-slate-900 border border-violet-700/30 rounded-xl w-full max-w-lg p-6 shadow-2xl"
        onClick={e => e.stopPropagation()}
      >
        {/* Header */}
        <div className="flex items-center justify-between mb-4">
          <div>
            <span className="text-lg font-bold text-white">{entity.entity_id}</span>
            <span className="ml-2 text-pink-400 text-xs">{entity.technology_type.replace(/_/g, " ")}</span>
            <span className="ml-2 text-violet-400 text-xs">{entity.region}</span>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl leading-none">✕</button>
        </div>

        {/* Tabs */}
        <div className="flex gap-2 mb-4">
          {(["scores", "signal", "action"] as const).map(t => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`px-3 py-1 rounded text-xs font-medium transition-colors ${
                tab === t
                  ? "bg-pink-700 text-white"
                  : "bg-slate-800 text-slate-400 hover:text-white"
              }`}
            >
              {t === "scores" ? "Scores" : t === "signal" ? "Signal" : "Action"}
            </button>
          ))}
        </div>

        {/* Tab: Scores */}
        {tab === "scores" && (
          <div className="grid grid-cols-2 gap-3 text-sm">
            {([
              ["Vie Privée", entity.privacy_score,   "#ec4899"],
              ["Sécurité",   entity.security_score,  "#f97316"],
              ["Droits Neuraux", entity.rights_score, "#a855f7"],
              ["Sociétal",   entity.societal_score,  "#06b6d4"],
            ] as [string, number, string][]).map(([l, v, c]) => (
              <div key={l} className="bg-slate-800 rounded-lg p-3">
                <div className="text-slate-400 text-xs mb-1">{l}</div>
                <div className="text-white font-bold text-lg">{Number(v).toFixed(1)}</div>
                <div className="h-1.5 rounded mt-1 bg-slate-700">
                  <div className="h-1.5 rounded" style={{ width: `${Math.min(Number(v), 100)}%`, background: c }} />
                </div>
              </div>
            ))}
            <div className="col-span-2 bg-slate-800 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Composite Risque Neural</div>
              <div className="text-white font-bold text-2xl">{entity.neural_composite.toFixed(1)}</div>
            </div>
          </div>
        )}

        {/* Tab: Signal */}
        {tab === "signal" && (
          <div className="bg-slate-800 rounded-lg p-4 text-sm text-slate-200 leading-relaxed">
            {entity.neural_signal}
            <div className="mt-3 flex gap-2 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[entity.neural_risk] || "bg-slate-700 text-slate-300"}`}>
                {entity.neural_risk}
              </span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[entity.neural_severity] || "bg-slate-700 text-slate-300"}`}>
                {entity.neural_severity}
              </span>
            </div>
          </div>
        )}

        {/* Tab: Action */}
        {tab === "action" && (
          <div className="space-y-3 text-sm">
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Action Recommandée</div>
              <div className="text-white font-medium">{entity.recommended_action.replace(/_/g, " ")}</div>
            </div>
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Patron Neuromorphique</div>
              <div className="text-pink-400 font-medium">{entity.neural_pattern.replace(/_/g, " ")}</div>
            </div>
            <div className="bg-slate-800 rounded-lg p-3 flex gap-4">
              <div>
                <div className="text-slate-400 text-xs mb-1">Crise Neurale</div>
                <div className={`text-xs font-semibold ${entity.is_neural_crisis ? "text-red-400" : "text-emerald-400"}`}>
                  {entity.is_neural_crisis ? "Oui" : "Non"}
                </div>
              </div>
              <div>
                <div className="text-slate-400 text-xs mb-1">Intervention Req.</div>
                <div className={`text-xs font-semibold ${entity.requires_neural_intervention ? "text-orange-400" : "text-emerald-400"}`}>
                  {entity.requires_neural_intervention ? "Oui" : "Non"}
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

// ── Main Dashboard ─────────────────────────────────────────────────────────────
export default function NeuromorphicBCIDashboard() {
  const [data, setData] = useState<{ entities: NBCEntity[]; summary: Summary } | null>(null);
  const [filter, setFilter] = useState<string>("all");
  const [patFilter, setPatFilter] = useState<string>("all");
  const [selected, setSelected] = useState<NBCEntity | null>(null);

  useEffect(() => {
    fetch("/api/neuromorphic-bci-engine")
      .then(r => r.json())
      .then(setData)
      .catch(console.error);
  }, []);

  if (!data) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-pink-400 text-lg animate-pulse">Chargement Module 310 — BCI Neuromorphique...</div>
    </div>
  );

  const { entities, summary } = data;

  const filtered = entities.filter(e =>
    (filter === "all" || e.neural_risk === filter) &&
    (patFilter === "all" || e.neural_pattern === patFilter),
  );

  const dists: Array<{ title: string; counts: Record<string, number>; colors: Record<string, string> }> = [
    { title: "Niveau de Risque Neural",  counts: summary.risk_counts,     colors: RISK_COLORS },
    { title: "Patron Neuromorphique",    counts: summary.pattern_counts,  colors: PAT_COLORS  },
    { title: "Sévérité BCI",             counts: summary.severity_counts, colors: SEV_COLORS  },
    { title: "Action Requise",           counts: summary.action_counts,   colors: ACT_COLORS  },
  ];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {selected && <DetailModal entity={selected} onClose={() => setSelected(null)} />}

      {/* Title */}
      <div>
        <h1 className="text-2xl font-bold text-white">
          Informatique Neuromorphique &amp; Interface Cerveau-Machine — Module 310
        </h1>
        <p className="text-slate-400 text-sm mt-1">
          BCI · Neurodroits · Vie privée neurale · Sécurité cérébrale · Inégalité cognitive · Caelum Partners
        </p>
      </div>

      {/* KPI strip — 6 cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {([
          ["Entités Analysées",        summary.total,                                    "text-pink-400"],
          ["Crises Neurales",          summary.neural_crisis_count,                      "text-red-400"],
          ["Interventions Req.",        summary.neural_intervention_count,               "text-orange-400"],
          ["Composite Moyen",          `${summary.avg_neural_composite.toFixed(1)}`,     "text-violet-400"],
          ["Indice Risque Neural",     `${summary.avg_estimated_neural_risk_index.toFixed(2)}/10`, "text-pink-300"],
          ["Droits Neuraux Moy.",      `${summary.avg_rights_score.toFixed(1)}`,         "text-amber-400"],
        ] as [string, string | number, string][]).map(([l, v, c]) => (
          <div key={String(l)} className="bg-slate-900 border border-violet-700/30 rounded-xl p-3 text-center">
            <div className={`text-xl font-bold ${c}`}>{v}</div>
            <div className="text-xs text-slate-500 mt-0.5">{l}</div>
          </div>
        ))}
      </div>

      {/* 4 GaugeRings */}
      <div className="bg-slate-900 border border-violet-700/30 rounded-xl p-5">
        <div className="grid grid-cols-4 gap-4">
          <GaugeRing value={summary.avg_privacy_score}   label="Vie Privée"     color="#ec4899" />
          <GaugeRing value={summary.avg_security_score}  label="Sécurité"       color="#f97316" />
          <GaugeRing value={summary.avg_rights_score}    label="Droits Neuraux" color="#a855f7" />
          <GaugeRing value={summary.avg_societal_score}  label="Sociétal"       color="#06b6d4" />
        </div>
      </div>

      {/* 4 DistBars */}
      <div className="bg-slate-900 border border-violet-700/30 rounded-xl p-5 grid grid-cols-1 md:grid-cols-2 gap-5">
        {dists.map(d => <DistBar key={d.title} {...d} />)}
      </div>

      {/* Filter pills — risk + pattern */}
      <div className="flex flex-wrap gap-2">
        {["all", "low", "moderate", "high", "critical"].map(r => (
          <button
            key={r}
            onClick={() => setFilter(r)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${
              filter === r
                ? "bg-pink-700 border-pink-600 text-white"
                : "bg-slate-900 border-slate-700 text-slate-400 hover:text-white"
            }`}
          >
            {r}
          </button>
        ))}
        <span className="w-px h-5 self-center bg-slate-700" />
        {[
          "all",
          "neural_sovereignty_breach",
          "brain_hacking_attack",
          "neurorights_violation",
          "cognitive_inequality_crisis",
          "military_neuroweapon",
          "none",
        ].map(p => (
          <button
            key={p}
            onClick={() => setPatFilter(p)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${
              patFilter === p
                ? "bg-violet-900 border-violet-800 text-white"
                : "bg-slate-900 border-slate-700 text-slate-400 hover:text-white"
            }`}
          >
            {p.replace(/_/g, " ")}
          </button>
        ))}
      </div>

      {/* Entity cards grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {filtered.map(e => (
          <div
            key={e.entity_id}
            onClick={() => setSelected(e)}
            className="bg-slate-900 border border-slate-800 rounded-xl p-4 cursor-pointer hover:border-pink-600 transition-colors"
          >
            <div className="flex items-center justify-between mb-1">
              <span className="font-bold text-white">{e.entity_id}</span>
              <span className="text-xs text-slate-400">{e.region}</span>
            </div>
            <div className="text-xs text-pink-400 mb-2 capitalize">{e.technology_type.replace(/_/g, " ")}</div>
            <div className="flex gap-1 mb-3 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[e.neural_risk] || "bg-slate-700 text-slate-300"}`}>
                {e.neural_risk}
              </span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[e.neural_severity] || "bg-slate-700 text-slate-300"}`}>
                {e.neural_severity}
              </span>
            </div>
            {/* Composite risk bar */}
            <div className="mb-2">
              <div className="flex justify-between text-xs text-slate-500 mb-1">
                <span>Risque Composite</span>
                <span className="text-pink-400 font-semibold">{e.neural_composite.toFixed(1)}</span>
              </div>
              <div className="h-1.5 rounded bg-slate-800">
                <div
                  className="h-1.5 rounded"
                  style={{
                    width: `${Math.min(e.neural_composite, 100)}%`,
                    background: RISK_COLORS[e.neural_risk] || "#475569",
                  }}
                />
              </div>
            </div>
            <div className="text-xs text-slate-500 mb-2 capitalize">{e.neural_pattern.replace(/_/g, " ")}</div>
            <div className="text-xs text-slate-400 line-clamp-2 leading-relaxed">{e.neural_signal}</div>
          </div>
        ))}
      </div>
    </div>
  );
}
