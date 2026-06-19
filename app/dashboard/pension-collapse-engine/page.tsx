"use client";
import { useEffect, useState } from "react";

type PensionEntity = {
  entity_id: string;
  region: string;
  pension_system_type: string;
  pension_risk: string;
  pension_pattern: string;
  pension_severity: string;
  recommended_action: string;
  demographic_score: number;
  funding_score: number;
  social_score: number;
  structural_score: number;
  pension_composite: number;
  is_pension_crisis: boolean;
  requires_pension_intervention: boolean;
  pension_signal: string;
};

type Summary = {
  module: string;
  total: number;
  risk_counts: Record<string, number>;
  pattern_counts: Record<string, number>;
  severity_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_demographic_score: number;
  avg_funding_score: number;
  avg_social_score: number;
  avg_structural_score: number;
  avg_pension_composite: number;
  crisis_count: number;
  intervention_count: number;
  avg_estimated_pension_crisis_index: number;
};

const RISK_COLORS: Record<string, string> = {
  low: "#10b981",
  moderate: "#f59e0b",
  high: "#f97316",
  critical: "#ef4444",
};
const PAT_COLORS: Record<string, string> = {
  none: "#10b981",
  demographic_collapse: "#ef4444",
  pension_insolvency: "#dc2626",
  generational_war: "#f97316",
  reform_paralysis: "#a855f7",
  automation_displacement: "#3b82f6",
};
const SEV_COLORS: Record<string, string> = {
  pension_sustainable: "#10b981",
  pension_stress: "#f59e0b",
  pension_crisis: "#f97316",
  pension_emergency: "#ef4444",
};
const ACT_COLORS: Record<string, string> = {
  no_action: "#10b981",
  pension_monitoring: "#f59e0b",
  pension_reform_program: "#f97316",
  sovereign_pension_bailout: "#a855f7",
  pension_emergency_restructuring: "#ef4444",
};
const RISK_BADGE: Record<string, string> = {
  low: "bg-emerald-900 text-emerald-300",
  moderate: "bg-amber-900 text-amber-300",
  high: "bg-orange-900 text-orange-300",
  critical: "bg-red-900 text-red-300",
};
const SEV_BADGE: Record<string, string> = {
  pension_sustainable: "bg-emerald-900 text-emerald-300",
  pension_stress: "bg-amber-900 text-amber-300",
  pension_crisis: "bg-orange-900 text-orange-300",
  pension_emergency: "bg-red-900 text-red-300",
};

function GaugeRing({ value, label, color }: { value: number; label: string; color: string }) {
  const r = 36;
  const circ = 2 * Math.PI * r;
  const fill = circ * (1 - value / 100);
  return (
    <div className="flex flex-col items-center gap-1">
      <svg width="88" height="88" viewBox="0 0 88 88">
        <circle cx="44" cy="44" r={r} fill="none" stroke="#1e293b" strokeWidth="8" />
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

function DistBar({ title, counts, colors }: { title: string; counts: Record<string, number>; colors: Record<string, string> }) {
  const total = Object.values(counts).reduce((a, b) => a + b, 0) || 1;
  return (
    <div className="flex flex-col gap-1">
      <span className="text-xs text-slate-400 font-medium">{title}</span>
      <div className="flex h-3 rounded overflow-hidden gap-px">
        {Object.entries(counts).map(([k, v]) => (
          <div key={k} style={{ width: `${(v / total) * 100}%`, background: colors[k] || "#475569" }} title={`${k}: ${v}`} />
        ))}
      </div>
      <div className="flex flex-wrap gap-x-3 gap-y-0.5">
        {Object.entries(counts).map(([k, v]) => (
          <span key={k} className="text-xs text-slate-400">
            <span style={{ color: colors[k] || "#94a3b8" }}>■</span> {k.replace(/_/g, " ")} {v}
          </span>
        ))}
      </div>
    </div>
  );
}

function DetailModal({ entity, onClose }: { entity: PensionEntity; onClose: () => void }) {
  const [tab, setTab] = useState<"scores" | "signal" | "action">("scores");
  useEffect(() => {
    const h = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", h);
    return () => window.removeEventListener("keydown", h);
  }, [onClose]);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70" onClick={onClose}>
      <div className="bg-slate-900 border border-yellow-600/30 rounded-xl w-full max-w-lg p-6 shadow-2xl" onClick={e => e.stopPropagation()}>
        <div className="flex items-center justify-between mb-4">
          <div>
            <span className="text-lg font-bold text-white">{entity.entity_id}</span>
            <span className="ml-2 text-slate-400 text-sm">{entity.region}</span>
            <span className="ml-2 text-xs text-yellow-400">{entity.pension_system_type.replace(/_/g, " ")}</span>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl leading-none">✕</button>
        </div>
        <div className="flex gap-2 mb-4">
          {(["scores", "signal", "action"] as const).map(t => (
            <button key={t} onClick={() => setTab(t)}
              className={`px-3 py-1 rounded text-xs font-medium transition-colors ${tab === t ? "bg-yellow-800 text-white" : "bg-slate-800 text-slate-400 hover:text-white"}`}>
              {t === "scores" ? "Scores" : t === "signal" ? "Signal" : "Action"}
            </button>
          ))}
        </div>
        {tab === "scores" && (
          <div className="grid grid-cols-2 gap-3 text-sm">
            {[
              ["Démographie", entity.demographic_score, "#ef4444"],
              ["Financement", entity.funding_score, "#f97316"],
              ["Social", entity.social_score, "#a855f7"],
              ["Structurel", entity.structural_score, "#3b82f6"],
            ].map(([l, v, c]) => (
              <div key={String(l)} className="bg-slate-800 rounded-lg p-3">
                <div className="text-slate-400 text-xs mb-1">{String(l)}</div>
                <div className="text-white font-bold text-lg">{Number(v).toFixed(1)}</div>
                <div className="h-1.5 rounded mt-1 bg-slate-700">
                  <div className="h-1.5 rounded" style={{ width: `${Math.min(Number(v), 100)}%`, background: String(c) }} />
                </div>
              </div>
            ))}
            <div className="col-span-2 bg-slate-800 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Composite Retraite</div>
              <div className="text-white font-bold text-2xl">{entity.pension_composite.toFixed(1)}</div>
            </div>
          </div>
        )}
        {tab === "signal" && (
          <div className="bg-slate-800 rounded-lg p-4 text-sm text-slate-200 leading-relaxed">
            {entity.pension_signal}
            <div className="mt-3 flex gap-2 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[entity.pension_risk] || "bg-slate-700 text-slate-300"}`}>{entity.pension_risk}</span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[entity.pension_severity] || "bg-slate-700 text-slate-300"}`}>{entity.pension_severity.replace(/_/g, " ")}</span>
            </div>
          </div>
        )}
        {tab === "action" && (
          <div className="space-y-3 text-sm">
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Action Recommandée</div>
              <div className="text-yellow-400 font-medium">{entity.recommended_action.replace(/_/g, " ")}</div>
            </div>
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Modèle de Crise</div>
              <div className="text-orange-400 font-medium capitalize">{entity.pension_pattern.replace(/_/g, " ")}</div>
            </div>
            <div className="flex gap-2 flex-wrap">
              {entity.is_pension_crisis && <span className="px-2 py-1 rounded bg-red-900 text-red-300 text-xs font-medium">CRISE RETRAITE</span>}
              {entity.requires_pension_intervention && <span className="px-2 py-1 rounded bg-yellow-900 text-yellow-300 text-xs font-medium">INTERVENTION</span>}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function PensionCollapseEngineDashboard() {
  const [data, setData] = useState<{ entities: PensionEntity[]; summary: Summary } | null>(null);
  const [riskFilter, setRiskFilter] = useState<string>("all");
  const [patFilter, setPatFilter] = useState<string>("all");
  const [selected, setSelected] = useState<PensionEntity | null>(null);

  useEffect(() => {
    fetch("/api/pension-collapse-engine")
      .then(r => r.json())
      .then(setData)
      .catch(console.error);
  }, []);

  if (!data) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-yellow-400 text-lg animate-pulse">Chargement du Moteur d&apos;Effondrement des Retraites...</div>
    </div>
  );

  const { entities, summary } = data;
  const filtered = entities.filter(e =>
    (riskFilter === "all" || e.pension_risk === riskFilter) &&
    (patFilter === "all" || e.pension_pattern === patFilter)
  );

  const dists = [
    { title: "Risque", counts: summary.risk_counts, colors: RISK_COLORS },
    { title: "Modèle", counts: summary.pattern_counts, colors: PAT_COLORS },
    { title: "Sévérité", counts: summary.severity_counts, colors: SEV_COLORS },
    { title: "Action", counts: summary.action_counts, colors: ACT_COLORS },
  ];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-300 p-6 space-y-6">
      {selected && <DetailModal entity={selected} onClose={() => setSelected(null)} />}

      <div>
        <h1 className="text-2xl font-bold text-yellow-400">Effondrement Retraites &amp; Protection Sociale — Module 320</h1>
        <p className="text-slate-400 text-sm mt-1">Démographie · Financement · Cohésion Sociale · Structurel — Caelum Partners</p>
      </div>

      {/* 6 KPI cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {[
          ["Entités", summary.total, "text-yellow-400"],
          ["Composite Moyen", summary.avg_pension_composite.toFixed(1), "text-yellow-400"],
          ["Crises Actives", summary.crisis_count, "text-red-400"],
          ["Interventions", summary.intervention_count, "text-orange-400"],
          ["Indice Crise Retraite", summary.avg_estimated_pension_crisis_index.toFixed(2), "text-amber-400"],
          ["Urgences Retraite", summary.severity_counts["pension_emergency"] || 0, "text-red-400"],
        ].map(([l, v, c]) => (
          <div key={String(l)} className="bg-slate-900 border border-yellow-600/30 rounded-xl p-3 text-center">
            <div className={`text-xl font-bold ${c}`}>{v}</div>
            <div className="text-xs text-slate-500 mt-0.5">{l}</div>
          </div>
        ))}
      </div>

      {/* 4 GaugeRings */}
      <div className="bg-slate-900 border border-yellow-600/30 rounded-xl p-5">
        <div className="grid grid-cols-4 gap-4">
          <GaugeRing value={summary.avg_demographic_score}  label="Démographie" color="#ef4444" />
          <GaugeRing value={summary.avg_funding_score}      label="Financement"  color="#f97316" />
          <GaugeRing value={summary.avg_social_score}       label="Social"       color="#a855f7" />
          <GaugeRing value={summary.avg_structural_score}   label="Structurel"   color="#3b82f6" />
        </div>
      </div>

      {/* 4 DistBars */}
      <div className="bg-slate-900 border border-yellow-600/30 rounded-xl p-5 grid grid-cols-1 md:grid-cols-2 gap-5">
        {dists.map(d => <DistBar key={d.title} {...d} />)}
      </div>

      {/* Filter pills */}
      <div className="flex flex-wrap gap-2">
        {["all", "low", "moderate", "high", "critical"].map(r => (
          <button key={r} onClick={() => setRiskFilter(r)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${riskFilter === r ? "bg-yellow-800 border-yellow-700 text-white" : "bg-slate-900 border-yellow-600/30 text-slate-400 hover:text-white"}`}>
            {r === "all" ? "Tous les risques" : r}
          </button>
        ))}
        <span className="w-px h-5 self-center bg-yellow-600/30" />
        {["all", "demographic_collapse", "pension_insolvency", "generational_war", "reform_paralysis", "automation_displacement"].map(p => (
          <button key={p} onClick={() => setPatFilter(p)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${patFilter === p ? "bg-slate-700 border-yellow-600 text-white" : "bg-slate-900 border-yellow-600/30 text-slate-400 hover:text-white"}`}>
            {p === "all" ? "Tous les modèles" : p.replace(/_/g, " ")}
          </button>
        ))}
      </div>

      {/* Entity cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {filtered.map(e => (
          <div key={e.entity_id} onClick={() => setSelected(e)}
            className="bg-slate-900 border border-yellow-600/30 rounded-xl p-4 cursor-pointer hover:border-yellow-500 transition-colors">
            <div className="flex items-center justify-between mb-2">
              <span className="font-bold text-white">{e.entity_id}</span>
              <span className="text-xs text-slate-400">{e.region}</span>
            </div>
            <div className="flex gap-1 mb-3 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[e.pension_risk] || "bg-slate-700 text-slate-300"}`}>{e.pension_risk}</span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[e.pension_severity] || "bg-slate-700 text-slate-300"}`}>{e.pension_severity.replace(/_/g, " ")}</span>
            </div>
            <div className="text-2xl font-black text-yellow-400 mb-1">{e.pension_composite.toFixed(1)}</div>
            <div className="text-xs text-slate-500 mb-2 capitalize">{e.pension_pattern.replace(/_/g, " ")}</div>
            <div className="flex gap-1 flex-wrap">
              {e.is_pension_crisis && <span className="px-1.5 py-0.5 rounded bg-red-900 text-red-300 text-xs">CRISE</span>}
              {e.requires_pension_intervention && <span className="px-1.5 py-0.5 rounded bg-yellow-900 text-yellow-300 text-xs">INTERVENTION</span>}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
