"use client";
import { useEffect, useState } from "react";

type Entity = {
  entity_id: string;
  region: string;
  platform_type: string;
  manipulation_risk: string;
  manipulation_pattern: string;
  manipulation_severity: string;
  recommended_action: string;
  deception_score: number;
  coercion_score: number;
  addiction_score: number;
  exploitation_score: number;
  manipulation_composite: number;
  is_manipulation_crisis: boolean;
  requires_manipulation_intervention: boolean;
  manipulation_signal: string;
};

type Summary = {
  total_entities_analyzed: number;
  critical_manipulation_count: number;
  high_manipulation_count: number;
  moderate_manipulation_count: number;
  low_manipulation_count: number;
  manipulation_crisis_count: number;
  requires_intervention_count: number;
  dominant_manipulation_pattern: string;
  avg_deception_score: number;
  avg_coercion_score: number;
  avg_addiction_score: number;
  avg_exploitation_score: number;
  avg_estimated_manipulation_index: number;
};

const RISK_COLORS: Record<string, string> = {
  low: "#10b981",
  moderate: "#f59e0b",
  high: "#f97316",
  critical: "#ef4444",
};

const PAT_COLORS: Record<string, string> = {
  none: "#10b981",
  systematic_deception: "#ef4444",
  consent_violation: "#f97316",
  addiction_engineering: "#a855f7",
  psychological_exploitation: "#ec4899",
  regulatory_evasion: "#dc2626",
};

const SEV_COLORS: Record<string, string> = {
  ethical_ux: "#10b981",
  pattern_accumulation: "#f59e0b",
  high_manipulation: "#f97316",
  manipulation_crisis: "#ef4444",
};

const ACT_COLORS: Record<string, string> = {
  no_action: "#10b981",
  pattern_monitoring: "#06b6d4",
  manipulation_audit: "#f97316",
  regulatory_intervention: "#a855f7",
  dark_pattern_shutdown: "#ef4444",
};

const RISK_BADGE: Record<string, string> = {
  low: "bg-emerald-900 text-emerald-300",
  moderate: "bg-amber-900 text-amber-300",
  high: "bg-orange-900 text-orange-300",
  critical: "bg-red-900 text-red-300",
};

const SEV_BADGE: Record<string, string> = {
  ethical_ux: "bg-emerald-900 text-emerald-300",
  pattern_accumulation: "bg-amber-900 text-amber-300",
  high_manipulation: "bg-orange-900 text-orange-300",
  manipulation_crisis: "bg-red-900 text-red-300",
};

const PATTERN_LABELS: Record<string, string> = {
  none: "Aucun",
  systematic_deception: "Déception systématique",
  consent_violation: "Violation consentement",
  addiction_engineering: "Ingénierie addiction",
  psychological_exploitation: "Exploitation psychologique",
  regulatory_evasion: "Évasion réglementaire",
};

const ACTION_LABELS: Record<string, string> = {
  no_action: "Aucune action",
  pattern_monitoring: "Surveillance pattern",
  manipulation_audit: "Audit manipulation",
  regulatory_intervention: "Intervention réglementaire",
  dark_pattern_shutdown: "Arrêt dark pattern",
};

function GaugeRing({ value, label, color }: { value: number; label: string; color: string }) {
  const r = 36;
  const circ = 2 * Math.PI * r;
  const fill = circ * (1 - value / 100);
  return (
    <div className="flex flex-col items-center gap-1">
      <svg width="88" height="88" viewBox="0 0 88 88">
        <circle cx="44" cy="44" r={r} fill="none" stroke="#1e1b4b" strokeWidth="8" />
        <circle cx="44" cy="44" r={r} fill="none" stroke={color} strokeWidth="8"
          strokeDasharray={circ} strokeDashoffset={fill}
          strokeLinecap="round" transform="rotate(-90 44 44)" />
        <text x="44" y="49" textAnchor="middle" fill="white" fontSize="13" fontWeight="bold">
          {Math.round(value)}
        </text>
      </svg>
      <span className="text-xs text-red-200/70 text-center">{label}</span>
    </div>
  );
}

function DistBar({ title, counts, colors }: { title: string; counts: Record<string, number>; colors: Record<string, string> }) {
  const total = Object.values(counts).reduce((a, b) => a + b, 0) || 1;
  return (
    <div className="flex flex-col gap-1">
      <span className="text-xs text-red-200/70 font-medium">{title}</span>
      <div className="flex h-3 rounded overflow-hidden gap-px">
        {Object.entries(counts).map(([k, v]) => (
          <div key={k} style={{ width: `${(v / total) * 100}%`, background: colors[k] || "#6b7280" }} title={`${k}: ${v}`} />
        ))}
      </div>
      <div className="flex flex-wrap gap-x-3 gap-y-0.5">
        {Object.entries(counts).map(([k, v]) => (
          <span key={k} className="text-xs text-red-200/60">
            <span style={{ color: colors[k] || "#9ca3af" }}>■</span> {k.replace(/_/g, " ")} {v}
          </span>
        ))}
      </div>
    </div>
  );
}

function DetailModal({ entity, onClose }: { entity: Entity; onClose: () => void }) {
  const [tab, setTab] = useState<"scores" | "signal" | "action">("scores");

  useEffect(() => {
    const h = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", h);
    return () => window.removeEventListener("keydown", h);
  }, [onClose]);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70" onClick={onClose}>
      <div className="bg-slate-900 border border-violet-700/30 rounded-xl w-full max-w-lg p-6 shadow-2xl" onClick={e => e.stopPropagation()}>
        <div className="flex items-center justify-between mb-4">
          <div>
            <span className="text-lg font-bold text-white">{entity.entity_id}</span>
            <span className="ml-2 text-red-400 text-xs">{entity.region}</span>
            <span className="ml-2 text-violet-400 text-xs capitalize">{entity.platform_type.replace(/_/g, " ")}</span>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl leading-none">✕</button>
        </div>

        <div className="flex gap-2 mb-4">
          {(["scores", "signal", "action"] as const).map(t => (
            <button key={t} onClick={() => setTab(t)}
              className={`px-3 py-1 rounded text-xs font-medium transition-colors ${tab === t ? "bg-violet-700 text-white" : "bg-slate-800 text-slate-400 hover:text-white"}`}>
              {t === "scores" ? "Scores" : t === "signal" ? "Signal" : "Action"}
            </button>
          ))}
        </div>

        {tab === "scores" && (
          <div className="grid grid-cols-2 gap-3 text-sm">
            {[
              ["Score Déception", entity.deception_score, "#ef4444"],
              ["Score Coercition", entity.coercion_score, "#f97316"],
              ["Score Addiction", entity.addiction_score, "#a855f7"],
              ["Score Exploitation", entity.exploitation_score, "#ec4899"],
            ].map(([l, v, c]) => (
              <div key={String(l)} className="bg-slate-800 rounded-lg p-3">
                <div className="text-red-200/60 text-xs mb-1">{String(l)}</div>
                <div className="text-white font-bold text-lg">{Number(v).toFixed(1)}</div>
                <div className="h-1.5 rounded mt-1 bg-slate-700">
                  <div className="h-1.5 rounded" style={{ width: `${Math.min(Number(v), 100)}%`, background: String(c) }} />
                </div>
              </div>
            ))}
            <div className="col-span-2 bg-slate-800 rounded-lg p-3">
              <div className="text-red-200/60 text-xs mb-1">Composite Manipulation</div>
              <div className="text-white font-bold text-2xl">{entity.manipulation_composite.toFixed(1)}</div>
            </div>
          </div>
        )}

        {tab === "signal" && (
          <div className="bg-slate-800 rounded-lg p-4 text-sm text-slate-200 leading-relaxed">
            {entity.manipulation_signal}
            <div className="mt-3 flex gap-2 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[entity.manipulation_risk] || "bg-slate-700 text-slate-300"}`}>
                {entity.manipulation_risk}
              </span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[entity.manipulation_severity] || "bg-slate-700 text-slate-300"}`}>
                {entity.manipulation_severity.replace(/_/g, " ")}
              </span>
            </div>
            <div className="mt-3 flex gap-2 flex-wrap">
              {entity.is_manipulation_crisis && (
                <span className="px-2 py-1 rounded bg-red-900 text-red-300 text-xs font-medium">CRISE MANIPULATION</span>
              )}
              {entity.requires_manipulation_intervention && (
                <span className="px-2 py-1 rounded bg-orange-900 text-orange-300 text-xs font-medium">INTERVENTION REQUISE</span>
              )}
            </div>
          </div>
        )}

        {tab === "action" && (
          <div className="space-y-3 text-sm">
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-red-200/60 text-xs mb-1">Action Recommandée</div>
              <div className="text-white font-medium capitalize">
                {ACTION_LABELS[entity.recommended_action] || entity.recommended_action.replace(/_/g, " ")}
              </div>
            </div>
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-red-200/60 text-xs mb-1">Pattern Détecté</div>
              <div className="text-white font-medium">
                {PATTERN_LABELS[entity.manipulation_pattern] || entity.manipulation_pattern.replace(/_/g, " ")}
              </div>
            </div>
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-red-200/60 text-xs mb-1">Sévérité</div>
              <div className="text-white font-medium capitalize">
                {entity.manipulation_severity.replace(/_/g, " ")}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function DarkPatternManipulationDashboard() {
  const [data, setData] = useState<{ entities: Entity[]; summary: Summary } | null>(null);
  const [riskFilter, setRiskFilter] = useState<string>("all");
  const [patFilter, setPatFilter] = useState<string>("all");
  const [selected, setSelected] = useState<Entity | null>(null);

  useEffect(() => {
    fetch("/api/dark-pattern-manipulation-engine")
      .then(r => r.json())
      .then(setData)
      .catch(console.error);
  }, []);

  if (!data) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-red-400 text-lg animate-pulse">Chargement du moteur dark patterns...</div>
    </div>
  );

  const { entities, summary } = data;
  const filtered = entities.filter(e =>
    (riskFilter === "all" || e.manipulation_risk === riskFilter) &&
    (patFilter === "all" || e.manipulation_pattern === patFilter)
  );

  const riskCounts: Record<string, number> = {
    critical: summary.critical_manipulation_count,
    high: summary.high_manipulation_count,
    moderate: summary.moderate_manipulation_count,
    low: summary.low_manipulation_count,
  };

  const patCounts: Record<string, number> = {};
  for (const e of entities) {
    patCounts[e.manipulation_pattern] = (patCounts[e.manipulation_pattern] || 0) + 1;
  }

  const sevCounts: Record<string, number> = {};
  const actCounts: Record<string, number> = {};
  for (const e of entities) {
    sevCounts[e.manipulation_severity] = (sevCounts[e.manipulation_severity] || 0) + 1;
    actCounts[e.recommended_action] = (actCounts[e.recommended_action] || 0) + 1;
  }

  const dists = [
    { title: "Risque Manipulation", counts: riskCounts, colors: RISK_COLORS },
    { title: "Pattern Détecté", counts: patCounts, colors: PAT_COLORS },
    { title: "Sévérité", counts: sevCounts, colors: SEV_COLORS },
    { title: "Action Recommandée", counts: actCounts, colors: ACT_COLORS },
  ];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {selected && <DetailModal entity={selected} onClose={() => setSelected(null)} />}

      <div>
        <h1 className="text-2xl font-bold text-red-400">Dark Patterns & Manipulation Numérique — Module 317</h1>
        <p className="text-red-200/60 text-sm mt-1">Déception · Coercition · Addiction · Exploitation — Caelum Partners</p>
      </div>

      {/* 6 KPI cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {[
          ["Total Entités", summary.total_entities_analyzed, "text-red-400"],
          ["Critiques", summary.critical_manipulation_count, "text-red-400"],
          ["Crises Manipulation", summary.manipulation_crisis_count, "text-red-300"],
          ["Intervention Requise", summary.requires_intervention_count, "text-orange-400"],
          ["Composite Moyen", `${(summary.avg_estimated_manipulation_index * 10).toFixed(1)}`, "text-violet-400"],
          ["Indice Manipulation", `${summary.avg_estimated_manipulation_index.toFixed(2)}/10`, "text-red-400"],
        ].map(([l, v, c]) => (
          <div key={String(l)} className="bg-slate-900 border border-violet-700/30 rounded-xl p-3 text-center">
            <div className={`text-xl font-bold ${c}`}>{v}</div>
            <div className="text-xs text-red-200/50 mt-0.5">{l}</div>
          </div>
        ))}
      </div>

      {/* 4 GaugeRings */}
      <div className="bg-slate-900 border border-violet-700/30 rounded-xl p-5">
        <div className="grid grid-cols-4 gap-4">
          <GaugeRing value={summary.avg_deception_score} label="Déception" color="#ef4444" />
          <GaugeRing value={summary.avg_coercion_score} label="Coercition" color="#f97316" />
          <GaugeRing value={summary.avg_addiction_score} label="Addiction" color="#a855f7" />
          <GaugeRing value={summary.avg_exploitation_score} label="Exploitation" color="#ec4899" />
        </div>
      </div>

      {/* 4 DistBars */}
      <div className="bg-slate-900 border border-violet-700/30 rounded-xl p-5 grid grid-cols-1 md:grid-cols-2 gap-5">
        {dists.map(d => <DistBar key={d.title} {...d} />)}
      </div>

      {/* Filter pills */}
      <div className="flex flex-wrap gap-2">
        {["all", "low", "moderate", "high", "critical"].map(r => (
          <button key={r} onClick={() => setRiskFilter(r)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${riskFilter === r ? "bg-red-700 border-red-600 text-white" : "bg-slate-900 border-violet-700/30 text-red-200/60 hover:text-white"}`}>
            {r === "all" ? "Tous risques" : r}
          </button>
        ))}
        <span className="w-px h-5 self-center bg-violet-700/30" />
        {["all", "none", "systematic_deception", "consent_violation", "addiction_engineering", "psychological_exploitation", "regulatory_evasion"].map(p => (
          <button key={p} onClick={() => setPatFilter(p)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${patFilter === p ? "bg-violet-900 border-violet-700 text-white" : "bg-slate-900 border-violet-700/30 text-red-200/60 hover:text-white"}`}>
            {p === "all" ? "Tous patterns" : PATTERN_LABELS[p] || p.replace(/_/g, " ")}
          </button>
        ))}
      </div>

      {/* Entity cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {filtered.map(e => (
          <div key={e.entity_id} onClick={() => setSelected(e)}
            className="bg-slate-900 border border-violet-700/30 rounded-xl p-4 cursor-pointer hover:border-red-500 transition-colors">
            <div className="flex items-center justify-between mb-1">
              <span className="font-bold text-white">{e.entity_id}</span>
              <span className="text-xs text-red-200/60">{e.region}</span>
            </div>
            <div className="text-xs text-violet-400 mb-2 capitalize">{e.platform_type.replace(/_/g, " ")}</div>
            <div className="flex gap-1 mb-3 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[e.manipulation_risk] || "bg-slate-700 text-slate-300"}`}>
                {e.manipulation_risk}
              </span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[e.manipulation_severity] || "bg-slate-700 text-slate-300"}`}>
                {e.manipulation_severity.replace(/_/g, " ")}
              </span>
            </div>
            <div className="text-2xl font-black text-red-400 mb-1">{e.manipulation_composite.toFixed(1)}</div>
            <div className="text-xs text-violet-300/70 mb-2 capitalize">{PATTERN_LABELS[e.manipulation_pattern] || e.manipulation_pattern.replace(/_/g, " ")}</div>
            <div className="text-xs text-red-400 font-medium mb-2 capitalize">{ACTION_LABELS[e.recommended_action] || e.recommended_action.replace(/_/g, " ")}</div>
            <div className="flex gap-1 flex-wrap">
              {e.is_manipulation_crisis && (
                <span className="px-1.5 py-0.5 rounded bg-red-900 text-red-300 text-xs">CRISE</span>
              )}
              {e.requires_manipulation_intervention && (
                <span className="px-1.5 py-0.5 rounded bg-orange-900 text-orange-300 text-xs">INTERVENTION</span>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
