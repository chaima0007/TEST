"use client";
import { useEffect, useState } from "react";

type EntityResult = {
  entity_id: string;
  region: string;
  pathogen_category: string;
  pandemic_risk: string;
  pandemic_pattern: string;
  pandemic_severity: string;
  recommended_action: string;
  transmission_score: number;
  severity_score: number;
  preparedness_score: number;
  systemic_score: number;
  pandemic_composite: number;
  is_pandemic_crisis: boolean;
  requires_pandemic_intervention: boolean;
  pandemic_signal: string;
};

type ApiData = {
  total_entities_analyzed: number;
  critical_pandemic_risks: number;
  high_pandemic_risks: number;
  moderate_pandemic_risks: number;
  low_pandemic_risks: number;
  pandemic_crises_detected: number;
  pandemic_interventions_required: number;
  dominant_pandemic_pattern: string;
  avg_estimated_pandemic_threat_index: number;
  highest_risk_entity: string;
  results: EntityResult[];
  analysis_timestamp: string;
  engine_version: string;
  risk_counts: Record<string, number>;
  pattern_counts: Record<string, number>;
  severity_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_transmission_score: number;
  avg_severity_score: number;
  avg_preparedness_score: number;
  avg_systemic_score: number;
  avg_pandemic_composite: number;
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
      <span className="text-xs text-green-300/70 text-center">{label}</span>
    </div>
  );
}

function DistBar({ title, counts, colors }: { title: string; counts: Record<string, number>; colors: Record<string, string> }) {
  const total = Object.values(counts).reduce((a, b) => a + b, 0) || 1;
  return (
    <div className="flex flex-col gap-1">
      <span className="text-xs text-green-300/70 font-medium">{title}</span>
      <div className="flex h-3 rounded overflow-hidden gap-px">
        {Object.entries(counts).map(([k, v]) => (
          <div key={k} style={{ width: `${(v / total) * 100}%`, background: colors[k] || "#475569" }} title={`${k}: ${v}`} />
        ))}
      </div>
      <div className="flex flex-wrap gap-x-3 gap-y-0.5">
        {Object.entries(counts).map(([k, v]) => (
          <span key={k} className="text-xs text-green-300/60">
            <span style={{ color: colors[k] || "#94a3b8" }}>■</span> {k.replace(/_/g, " ")} {v}
          </span>
        ))}
      </div>
    </div>
  );
}

const RISK_COLORS = { low: "#10b981", moderate: "#f59e0b", high: "#f97316", critical: "#ef4444" };
const PAT_COLORS: Record<string, string> = {
  none:                      "#10b981",
  pandemic_emergence:        "#7f1d1d",
  variant_escape_cascade:    "#a855f7",
  healthcare_system_collapse:"#ef4444",
  amr_catastrophe:           "#dc2626",
  zoonotic_explosion:        "#f97316",
};
const SEV_COLORS: Record<string, string> = {
  containment_adequate: "#10b981",
  outbreak_developing:  "#f59e0b",
  epidemic_crisis:      "#f97316",
  pandemic_emergency:   "#7f1d1d",
};
const ACTION_COLORS: Record<string, string> = {
  no_action:                    "#10b981",
  outbreak_monitoring:          "#06b6d4",
  enhanced_surveillance:        "#f59e0b",
  surge_capacity_activation:    "#f97316",
  pandemic_emergency_response:  "#7f1d1d",
};

const RISK_BADGE: Record<string, string> = {
  low:      "bg-emerald-900 text-emerald-300",
  moderate: "bg-amber-900 text-amber-300",
  high:     "bg-orange-900 text-orange-300",
  critical: "bg-red-950 text-red-400",
};
const SEV_BADGE: Record<string, string> = {
  containment_adequate: "bg-emerald-900 text-emerald-300",
  outbreak_developing:  "bg-amber-900 text-amber-300",
  epidemic_crisis:      "bg-orange-900 text-orange-300",
  pandemic_emergency:   "bg-red-950 text-red-400",
};

function DetailModal({ entity, onClose }: { entity: EntityResult; onClose: () => void }) {
  const [tab, setTab] = useState<"scores" | "signal" | "action">("scores");

  useEffect(() => {
    const h = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", h);
    return () => window.removeEventListener("keydown", h);
  }, [onClose]);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80" onClick={onClose}>
      <div className="bg-slate-950 border border-green-700/30 rounded-xl w-full max-w-lg p-6 shadow-2xl" onClick={e => e.stopPropagation()}>
        <div className="flex items-center justify-between mb-4">
          <div>
            <span className="text-lg font-bold text-white">{entity.entity_id}</span>
            <span className="ml-2 text-red-400 text-xs">{entity.region}</span>
            <span className="ml-2 text-slate-500 text-xs">{entity.pathogen_category.replace(/_/g, " ")}</span>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl leading-none">✕</button>
        </div>

        <div className="flex gap-2 mb-4">
          {(["scores", "signal", "action"] as const).map(t => (
            <button key={t} onClick={() => setTab(t)}
              className={`px-3 py-1 rounded text-xs font-medium transition-colors ${tab === t ? "bg-green-900 text-white" : "bg-slate-900 text-slate-400 hover:text-white"}`}>
              {t === "scores" ? "Scores" : t === "signal" ? "Signal" : "Action"}
            </button>
          ))}
        </div>

        {tab === "scores" && (
          <div className="grid grid-cols-2 gap-3 text-sm">
            {([
              ["Transmission",  entity.transmission_score,  "#ef4444"],
              ["Sévérité",      entity.severity_score,      "#a855f7"],
              ["Préparation",   entity.preparedness_score,  "#f97316"],
              ["Systémique",    entity.systemic_score,      "#06b6d4"],
            ] as [string, number, string][]).map(([l, v, c]) => (
              <div key={l} className="bg-slate-900 border border-green-700/20 rounded-lg p-3">
                <div className="text-green-300/60 text-xs mb-1">{l}</div>
                <div className="text-white font-bold text-lg">{v.toFixed(1)}</div>
                <div className="h-1.5 rounded mt-1 bg-slate-800">
                  <div className="h-1.5 rounded" style={{ width: `${Math.min(v, 100)}%`, background: c }} />
                </div>
              </div>
            ))}
            <div className="col-span-2 bg-slate-900 border border-green-700/20 rounded-lg p-3">
              <div className="text-green-300/60 text-xs mb-1">Composite Pandémique</div>
              <div className="text-white font-bold text-2xl">{entity.pandemic_composite.toFixed(1)}</div>
            </div>
          </div>
        )}

        {tab === "signal" && (
          <div className="bg-slate-900 border border-green-700/20 rounded-lg p-4 text-sm text-slate-200 leading-relaxed">
            {entity.pandemic_signal}
            <div className="mt-3 flex gap-2 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[entity.pandemic_risk] || "bg-slate-700 text-slate-300"}`}>
                {entity.pandemic_risk}
              </span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[entity.pandemic_severity] || "bg-slate-700 text-slate-300"}`}>
                {entity.pandemic_severity.replace(/_/g, " ")}
              </span>
            </div>
          </div>
        )}

        {tab === "action" && (
          <div className="space-y-3 text-sm">
            <div className="bg-slate-900 border border-green-700/20 rounded-lg p-3">
              <div className="text-green-300/60 text-xs mb-1">Action Recommandée</div>
              <div className="text-white font-medium">{entity.recommended_action.replace(/_/g, " ")}</div>
            </div>
            <div className="bg-slate-900 border border-green-700/20 rounded-lg p-3">
              <div className="text-green-300/60 text-xs mb-1">Schéma Pandémique</div>
              <div className="text-white font-medium">{entity.pandemic_pattern.replace(/_/g, " ")}</div>
            </div>
            <div className="flex gap-2">
              {entity.is_pandemic_crisis && (
                <span className="px-2 py-1 rounded bg-red-950 text-red-400 text-xs font-medium">CRISE PANDÉMIQUE</span>
              )}
              {entity.requires_pandemic_intervention && (
                <span className="px-2 py-1 rounded bg-orange-950 text-orange-400 text-xs font-medium">INTERVENTION REQ.</span>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function PandemicIntelligenceDashboard() {
  const [data, setData]             = useState<ApiData | null>(null);
  const [filter, setFilter]         = useState<string>("all");
  const [patFilter, setPatFilter]   = useState<string>("all");
  const [selected, setSelected]     = useState<EntityResult | null>(null);

  useEffect(() => {
    fetch("/api/pandemic-intelligence-engine")
      .then(r => r.json())
      .then(setData)
      .catch(console.error);
  }, []);

  if (!data) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-red-400 text-lg animate-pulse">Initialisation du Moteur Intelligence Pandémique...</div>
    </div>
  );

  const filtered = (data.results || []).filter(e =>
    (filter === "all" || e.pandemic_risk === filter) &&
    (patFilter === "all" || e.pandemic_pattern === patFilter)
  );

  const dists = [
    { title: "Niveau Risque Pandémique",   counts: data.risk_counts,     colors: RISK_COLORS   },
    { title: "Schéma Pandémique",          counts: data.pattern_counts,  colors: PAT_COLORS    },
    { title: "Sévérité Épidémique",        counts: data.severity_counts, colors: SEV_COLORS    },
    { title: "Action Déclenchée",          counts: data.action_counts,   colors: ACTION_COLORS },
  ];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {selected && <DetailModal entity={selected} onClose={() => setSelected(null)} />}

      <div>
        <h1 className="text-2xl font-bold text-red-400">Intelligence Pandémique &amp; Biosurveillance Mondiale — Module 325</h1>
        <p className="text-green-300/50 text-sm mt-1">Transmission · Sévérité · Préparation · Systémique</p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {([
          ["Entités Analysées",         data.total_entities_analyzed,                         "text-green-400"],
          ["Risques Critiques",         data.critical_pandemic_risks,                          "text-red-400"],
          ["Composite Pandémique Moy.", `${data.avg_pandemic_composite?.toFixed(1) ?? "—"}`,  "text-orange-400"],
          ["Indice Menace Moy.",        `${data.avg_estimated_pandemic_threat_index?.toFixed(2) ?? "—"}/10`, "text-amber-400"],
          ["Crises Pandémiques",        data.pandemic_crises_detected,                        "text-red-500"],
          ["Interventions Requises",    data.pandemic_interventions_required,                  "text-red-400"],
        ] as [string, string | number, string][]).map(([l, v, c]) => (
          <div key={l} className="bg-slate-900 border border-green-700/30 rounded-xl p-3 text-center">
            <div className={`text-xl font-bold ${c}`}>{v}</div>
            <div className="text-xs text-green-300/40 mt-0.5 leading-tight">{l}</div>
          </div>
        ))}
      </div>

      {/* Gauge Rings */}
      <div className="bg-slate-900 border border-green-700/30 rounded-xl p-5">
        <div className="grid grid-cols-4 gap-4">
          <GaugeRing value={data.avg_transmission_score ?? 0}  label="Score Transmission"  color="#ef4444" />
          <GaugeRing value={data.avg_severity_score ?? 0}      label="Score Sévérité"       color="#a855f7" />
          <GaugeRing value={data.avg_preparedness_score ?? 0}  label="Score Préparation"    color="#f97316" />
          <GaugeRing value={data.avg_systemic_score ?? 0}      label="Score Systémique"     color="#06b6d4" />
        </div>
      </div>

      {/* Distribution Bars */}
      <div className="bg-slate-900 border border-green-700/30 rounded-xl p-5 grid grid-cols-1 md:grid-cols-2 gap-5">
        {dists.map(d => <DistBar key={d.title} {...d} />)}
      </div>

      {/* Filter Pills */}
      <div className="flex flex-wrap gap-2">
        {["all", "low", "moderate", "high", "critical"].map(r => (
          <button key={r} onClick={() => setFilter(r)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${filter === r ? "bg-red-900 border-red-700 text-white" : "bg-slate-900 border-green-700/30 text-green-400/70 hover:text-white"}`}>
            {r}
          </button>
        ))}
        <span className="w-px h-5 self-center bg-green-700/30" />
        {["all", "none", "pandemic_emergence", "variant_escape_cascade", "healthcare_system_collapse", "amr_catastrophe", "zoonotic_explosion"].map(p => (
          <button key={p} onClick={() => setPatFilter(p)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${patFilter === p ? "bg-red-950 border-red-800 text-white" : "bg-slate-900 border-green-700/30 text-green-400/70 hover:text-white"}`}>
            {p.replace(/_/g, " ")}
          </button>
        ))}
      </div>

      {/* Entity Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {filtered.map(e => (
          <div key={e.entity_id} onClick={() => setSelected(e)}
            className="bg-slate-900 border border-green-700/30 rounded-xl p-4 cursor-pointer hover:border-red-500 transition-colors">
            <div className="flex items-center justify-between mb-1">
              <span className="font-bold text-white">{e.entity_id}</span>
              <span className="text-xs text-red-400/70">{e.region}</span>
            </div>
            <div className="text-xs text-slate-500 mb-2 capitalize">{e.pathogen_category.replace(/_/g, " ")}</div>
            <div className="flex gap-1 mb-3 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[e.pandemic_risk] || "bg-slate-700 text-slate-300"}`}>
                {e.pandemic_risk}
              </span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[e.pandemic_severity] || "bg-slate-700 text-slate-300"}`}>
                {e.pandemic_severity.replace(/_/g, " ")}
              </span>
            </div>
            <div className="text-2xl font-black text-white mb-1">{e.pandemic_composite.toFixed(1)}</div>
            <div className="text-xs text-green-400/60 mb-2 capitalize">{e.pandemic_pattern.replace(/_/g, " ")}</div>
            <div className="text-xs text-red-400 font-medium mb-2">{e.recommended_action.replace(/_/g, " ")}</div>
            <div className="flex gap-1 flex-wrap">
              {e.is_pandemic_crisis && (
                <span className="px-1.5 py-0.5 rounded bg-red-950 text-red-400 text-xs">CRISE PANDÉMIQUE</span>
              )}
              {e.requires_pandemic_intervention && (
                <span className="px-1.5 py-0.5 rounded bg-orange-950 text-orange-400 text-xs">INTERVENTION</span>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
