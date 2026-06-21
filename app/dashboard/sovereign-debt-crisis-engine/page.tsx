"use client";
import { useEffect, useState } from "react";

type SovereignEntity = {
  id: string;
  region: string;
  sovereign_type: string;
  debt_risk: string;
  debt_pattern: string;
  debt_severity: string;
  recommended_action: string;
  solvency_score: number;
  liquidity_score: number;
  contagion_score: number;
  confidence_score: number;
  debt_composite: number;
  is_debt_crisis: boolean;
  requires_debt_intervention: boolean;
  debt_signal: string;
};

type Summary = {
  total: number;
  risk_counts: Record<string, number>;
  pattern_counts: Record<string, number>;
  severity_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_solvency_score: number;
  avg_liquidity_score: number;
  avg_contagion_score: number;
  avg_confidence_score: number;
  avg_debt_composite: number;
  debt_crisis_count: number;
  debt_intervention_count: number;
  avg_estimated_fiscal_stress_index: number;
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
            <span style={{ color: colors[k] || "#94a3b8" }}>■</span> {k} {v}
          </span>
        ))}
      </div>
    </div>
  );
}

const RISK_COLORS: Record<string, string> = { low: "#10b981", moderate: "#f59e0b", high: "#f97316", critical: "#ef4444" };
const PAT_COLORS: Record<string, string> = {
  none: "#10b981",
  debt_spiral: "#ef4444",
  liquidity_trap: "#f97316",
  contagion_cascade: "#a855f7",
  confidence_collapse: "#3b82f6",
  currency_debt_spiral: "#dc2626",
};
const SEV_COLORS: Record<string, string> = {
  fiscal_stable: "#10b981",
  fiscal_tension: "#f59e0b",
  high_fiscal_stress: "#f97316",
  fiscal_emergency: "#ef4444",
};
const ACT_COLORS: Record<string, string> = {
  no_action: "#10b981",
  fiscal_monitoring: "#f59e0b",
  fiscal_consolidation_program: "#f97316",
  contagion_firewall: "#a855f7",
  sovereign_debt_restructuring: "#ef4444",
};
const RISK_BADGE: Record<string, string> = {
  low: "bg-emerald-900 text-emerald-300",
  moderate: "bg-amber-900 text-amber-300",
  high: "bg-orange-900 text-orange-300",
  critical: "bg-red-900 text-red-300",
};
const SEV_BADGE: Record<string, string> = {
  fiscal_stable: "bg-emerald-900 text-emerald-300",
  fiscal_tension: "bg-amber-900 text-amber-300",
  high_fiscal_stress: "bg-orange-900 text-orange-300",
  fiscal_emergency: "bg-red-900 text-red-300",
};

function DetailModal({ entity, onClose }: { entity: SovereignEntity; onClose: () => void }) {
  const [tab, setTab] = useState<"scores" | "signal" | "action">("scores");
  useEffect(() => {
    const h = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", h);
    return () => window.removeEventListener("keydown", h);
  }, [onClose]);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70" onClick={onClose}>
      <div className="bg-slate-900 border border-yellow-700/30 rounded-xl w-full max-w-lg p-6 shadow-2xl" onClick={e => e.stopPropagation()}>
        <div className="flex items-center justify-between mb-4">
          <div>
            <span className="text-lg font-bold text-white">{entity.id}</span>
            <span className="ml-2 text-slate-400 text-sm">{entity.region}</span>
            <span className="ml-2 text-xs text-yellow-600">{entity.sovereign_type.replace(/_/g, " ")}</span>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl leading-none">✕</button>
        </div>
        <div className="flex gap-2 mb-4">
          {(["scores", "signal", "action"] as const).map(t => (
            <button key={t} onClick={() => setTab(t)}
              className={`px-3 py-1 rounded text-xs font-medium transition-colors ${tab === t ? "bg-red-800 text-white" : "bg-slate-800 text-slate-400 hover:text-white"}`}>
              {t === "scores" ? "Scores" : t === "signal" ? "Signal" : "Action"}
            </button>
          ))}
        </div>
        {tab === "scores" && (
          <div className="grid grid-cols-2 gap-3 text-sm">
            {[
              ["Solvabilité", entity.solvency_score, "#ef4444"],
              ["Liquidité", entity.liquidity_score, "#f97316"],
              ["Contagion", entity.contagion_score, "#a855f7"],
              ["Confiance", entity.confidence_score, "#3b82f6"],
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
              <div className="text-slate-400 text-xs mb-1">Composite Dette Souveraine</div>
              <div className="text-white font-bold text-2xl">{entity.debt_composite.toFixed(1)}</div>
            </div>
          </div>
        )}
        {tab === "signal" && (
          <div className="bg-slate-800 rounded-lg p-4 text-sm text-slate-200 leading-relaxed">
            {entity.debt_signal}
            <div className="mt-3 flex gap-2 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[entity.debt_risk] || "bg-slate-700 text-slate-300"}`}>{entity.debt_risk}</span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[entity.debt_severity] || "bg-slate-700 text-slate-300"}`}>{entity.debt_severity.replace(/_/g, " ")}</span>
            </div>
          </div>
        )}
        {tab === "action" && (
          <div className="space-y-3 text-sm">
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Action Recommandée</div>
              <div className="text-white font-medium">{entity.recommended_action.replace(/_/g, " ")}</div>
            </div>
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Modèle de Crise</div>
              <div className="text-red-400 font-medium capitalize">{entity.debt_pattern.replace(/_/g, " ")}</div>
            </div>
            <div className="flex gap-2 flex-wrap">
              {entity.is_debt_crisis && <span className="px-2 py-1 rounded bg-red-900 text-red-300 text-xs font-medium">CRISE DETTE</span>}
              {entity.requires_debt_intervention && <span className="px-2 py-1 rounded bg-yellow-900 text-yellow-300 text-xs font-medium">INTERVENTION</span>}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function SovereignDebtCrisisDashboard() {
  const [data, setData] = useState<{ entities: SovereignEntity[]; summary: Summary } | null>(null);
  const [riskFilter, setRiskFilter] = useState<string>("all");
  const [patFilter, setPatFilter] = useState<string>("all");
  const [selected, setSelected] = useState<SovereignEntity | null>(null);

  useEffect(() => {
    fetch("/api/sovereign-debt-crisis-engine")
      .then(r => r.json())
      .then(setData)
      .catch(console.error);
  }, []);

  if (!data) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-red-400 text-lg animate-pulse">Chargement de l&apos;Intelligence Dette Souveraine...</div>
    </div>
  );

  const { entities, summary } = data;
  const filtered = entities.filter(e =>
    (riskFilter === "all" || e.debt_risk === riskFilter) &&
    (patFilter === "all" || e.debt_pattern === patFilter)
  );

  const dists = [
    { title: "Risque", counts: summary.risk_counts, colors: RISK_COLORS },
    { title: "Modèle", counts: summary.pattern_counts, colors: PAT_COLORS },
    { title: "Sévérité", counts: summary.severity_counts, colors: SEV_COLORS },
    { title: "Action", counts: summary.action_counts, colors: ACT_COLORS },
  ];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {selected && <DetailModal entity={selected} onClose={() => setSelected(null)} />}

      <div>
        <h1 className="text-2xl font-bold text-red-400">Crise de Dette Souveraine &amp; Contagion Fiscale — Module 309</h1>
        <p className="text-yellow-600 text-sm mt-1">Solvabilité · Liquidité · Contagion · Confiance — Caelum Partners</p>
      </div>

      {/* 6 KPI cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {[
          ["Entités", summary.total, "text-red-400"],
          ["Composite Moyen", summary.avg_debt_composite.toFixed(1), "text-yellow-400"],
          ["Crises Actives", summary.debt_crisis_count, "text-red-400"],
          ["Interventions", summary.debt_intervention_count, "text-orange-400"],
          ["Indice Stress Fiscal", summary.avg_estimated_fiscal_stress_index.toFixed(2), "text-amber-400"],
          ["Urgences Fiscales", summary.severity_counts["fiscal_emergency"] || 0, "text-red-400"],
        ].map(([l, v, c]) => (
          <div key={String(l)} className="bg-slate-900 border border-yellow-700/30 rounded-xl p-3 text-center">
            <div className={`text-xl font-bold ${c}`}>{v}</div>
            <div className="text-xs text-slate-500 mt-0.5">{l}</div>
          </div>
        ))}
      </div>

      {/* 4 GaugeRings */}
      <div className="bg-slate-900 border border-yellow-700/30 rounded-xl p-5">
        <div className="grid grid-cols-4 gap-4">
          <GaugeRing value={summary.avg_solvency_score}   label="Solvabilité" color="#ef4444" />
          <GaugeRing value={summary.avg_liquidity_score}  label="Liquidité"   color="#f97316" />
          <GaugeRing value={summary.avg_contagion_score}  label="Contagion"   color="#a855f7" />
          <GaugeRing value={summary.avg_confidence_score} label="Confiance"   color="#3b82f6" />
        </div>
      </div>

      {/* 4 DistBars */}
      <div className="bg-slate-900 border border-yellow-700/30 rounded-xl p-5 grid grid-cols-1 md:grid-cols-2 gap-5">
        {dists.map(d => <DistBar key={d.title} {...d} />)}
      </div>

      {/* Filter pills */}
      <div className="flex flex-wrap gap-2">
        {["all", "low", "moderate", "high", "critical"].map(r => (
          <button key={r} onClick={() => setRiskFilter(r)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${riskFilter === r ? "bg-red-800 border-red-700 text-white" : "bg-slate-900 border-yellow-700/30 text-slate-400 hover:text-white"}`}>
            {r === "all" ? "Tous les risques" : r}
          </button>
        ))}
        <span className="w-px h-5 self-center bg-yellow-700/30" />
        {["all", "debt_spiral", "liquidity_trap", "contagion_cascade", "confidence_collapse", "currency_debt_spiral"].map(p => (
          <button key={p} onClick={() => setPatFilter(p)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${patFilter === p ? "bg-yellow-900 border-yellow-700 text-white" : "bg-slate-900 border-yellow-700/30 text-slate-400 hover:text-white"}`}>
            {p === "all" ? "Tous les modèles" : p.replace(/_/g, " ")}
          </button>
        ))}
      </div>

      {/* Entity cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {filtered.map(e => (
          <div key={e.id} onClick={() => setSelected(e)}
            className="bg-slate-900 border border-yellow-700/30 rounded-xl p-4 cursor-pointer hover:border-red-700 transition-colors">
            <div className="flex items-center justify-between mb-2">
              <span className="font-bold text-white">{e.id}</span>
              <span className="text-xs text-slate-400">{e.region}</span>
            </div>
            <div className="flex gap-1 mb-3 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[e.debt_risk] || "bg-slate-700 text-slate-300"}`}>{e.debt_risk}</span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[e.debt_severity] || "bg-slate-700 text-slate-300"}`}>{e.debt_severity.replace(/_/g, " ")}</span>
            </div>
            <div className="text-2xl font-black text-red-400 mb-1">{e.debt_composite.toFixed(1)}</div>
            <div className="text-xs text-slate-500 mb-2 capitalize">{e.debt_pattern.replace(/_/g, " ")}</div>
            <div className="flex gap-1 flex-wrap">
              {e.is_debt_crisis && <span className="px-1.5 py-0.5 rounded bg-red-900 text-red-300 text-xs">CRISE</span>}
              {e.requires_debt_intervention && <span className="px-1.5 py-0.5 rounded bg-yellow-900 text-yellow-300 text-xs">INTERVENTION</span>}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
