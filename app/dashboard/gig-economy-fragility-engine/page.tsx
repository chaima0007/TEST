"use client";
import { useEffect, useState } from "react";

type GigEntity = {
  id: string;
  labor_sector: string;
  region: string;
  precarity_score: number;
  rights_score: number;
  exploitation_score: number;
  systemic_score: number;
  composite_score: number;
  risk_level: string;
  gig_pattern: string;
  severity: string;
  recommended_action: string;
  signal: string;
  platform_worker_precarity_index: number;
  labor_market_dualization_index: number;
};

type Summary = {
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
  avg_estimated_precarity_index: number;
};

const RISK_COLORS: Record<string, string> = {
  low: "#10b981",
  moderate: "#f59e0b",
  high: "#f97316",
  critical: "#ef4444",
};
const PAT_COLORS: Record<string, string> = {
  none: "#10b981",
  precariat_explosion: "#ef4444",
  algorithmic_serfdom: "#dc2626",
  rights_collapse: "#f97316",
  demographic_exploitation: "#a855f7",
  systemic_dualization: "#3b82f6",
};
const SEV_COLORS: Record<string, string> = {
  tensions_gig_contenues: "#10b981",
  précarisation_structurelle: "#f59e0b",
  crise_travail_platformisé: "#f97316",
  effondrement_social_précariat: "#ef4444",
};
const ACT_COLORS: Record<string, string> = {
  veille_précarité_continue: "#10b981",
  renforcement_droits_travailleurs_gig: "#f59e0b",
  régulation_plateforme_activée: "#f97316",
  intervention_sociale_urgente: "#ef4444",
};
const RISK_BADGE: Record<string, string> = {
  low: "bg-emerald-900 text-emerald-300",
  moderate: "bg-amber-900 text-amber-300",
  high: "bg-orange-900 text-orange-300",
  critical: "bg-red-900 text-red-300",
};
const SEV_BADGE: Record<string, string> = {
  tensions_gig_contenues: "bg-emerald-900 text-emerald-300",
  précarisation_structurelle: "bg-amber-900 text-amber-300",
  crise_travail_platformisé: "bg-orange-900 text-orange-300",
  effondrement_social_précariat: "bg-red-900 text-red-300",
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

function DetailModal({ entity, onClose }: { entity: GigEntity; onClose: () => void }) {
  const [tab, setTab] = useState<"scores" | "signal" | "action">("scores");
  useEffect(() => {
    const h = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", h);
    return () => window.removeEventListener("keydown", h);
  }, [onClose]);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70" onClick={onClose}>
      <div className="bg-slate-900 border border-orange-600/30 rounded-xl w-full max-w-lg p-6 shadow-2xl" onClick={e => e.stopPropagation()}>
        <div className="flex items-center justify-between mb-4">
          <div>
            <span className="text-lg font-bold text-white">{entity.id}</span>
            <span className="ml-2 text-slate-400 text-sm">{entity.region}</span>
            <span className="ml-2 text-xs text-orange-400">{entity.labor_sector.replace(/_/g, " ")}</span>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl leading-none">✕</button>
        </div>
        <div className="flex gap-2 mb-4">
          {(["scores", "signal", "action"] as const).map(t => (
            <button key={t} onClick={() => setTab(t)}
              className={`px-3 py-1 rounded text-xs font-medium transition-colors ${tab === t ? "bg-orange-800 text-white" : "bg-slate-800 text-slate-400 hover:text-white"}`}>
              {t === "scores" ? "Scores" : t === "signal" ? "Signal" : "Action"}
            </button>
          ))}
        </div>
        {tab === "scores" && (
          <div className="grid grid-cols-2 gap-3 text-sm">
            {[
              ["Précarité", entity.precarity_score, "#ef4444"],
              ["Droits", entity.rights_score, "#f97316"],
              ["Exploitation", entity.exploitation_score, "#a855f7"],
              ["Systémique", entity.systemic_score, "#3b82f6"],
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
              <div className="text-slate-400 text-xs mb-1">Composite Gig</div>
              <div className="text-white font-bold text-2xl">{entity.composite_score.toFixed(1)}</div>
            </div>
          </div>
        )}
        {tab === "signal" && (
          <div className="bg-slate-800 rounded-lg p-4 text-sm text-slate-200 leading-relaxed">
            {entity.signal}
            <div className="mt-3 flex gap-2 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[entity.risk_level] || "bg-slate-700 text-slate-300"}`}>{entity.risk_level}</span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[entity.severity] || "bg-slate-700 text-slate-300"}`}>{entity.severity.replace(/_/g, " ")}</span>
            </div>
          </div>
        )}
        {tab === "action" && (
          <div className="space-y-3 text-sm">
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Action Recommandée</div>
              <div className="text-orange-400 font-medium">{entity.recommended_action.replace(/_/g, " ")}</div>
            </div>
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Modèle Gig</div>
              <div className="text-amber-400 font-medium capitalize">{entity.gig_pattern.replace(/_/g, " ")}</div>
            </div>
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Index Précarité Travailleur</div>
              <div className="text-slate-200 font-medium">{(entity.platform_worker_precarity_index * 100).toFixed(1)}%</div>
            </div>
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Index Dualisation Marché</div>
              <div className="text-slate-200 font-medium">{(entity.labor_market_dualization_index * 100).toFixed(1)}%</div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function GigEconomyFragilityEngineDashboard() {
  const [data, setData] = useState<{ entities: GigEntity[]; summary: Summary } | null>(null);
  const [riskFilter, setRiskFilter] = useState<string>("all");
  const [patFilter, setPatFilter] = useState<string>("all");
  const [selected, setSelected] = useState<GigEntity | null>(null);

  useEffect(() => {
    fetch("/api/gig-economy-fragility-engine")
      .then(r => r.json())
      .then(setData)
      .catch(console.error);
  }, []);

  if (!data) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-orange-400 text-lg animate-pulse">Chargement du Moteur de Fragilité Économie Gig...</div>
    </div>
  );

  const { entities, summary } = data;
  const filtered = entities.filter(e =>
    (riskFilter === "all" || e.risk_level === riskFilter) &&
    (patFilter === "all" || e.gig_pattern === patFilter)
  );

  const avgPrecarity = entities.length > 0
    ? entities.reduce((s, e) => s + e.precarity_score, 0) / entities.length
    : 0;
  const avgRights = entities.length > 0
    ? entities.reduce((s, e) => s + e.rights_score, 0) / entities.length
    : 0;
  const avgExploitation = entities.length > 0
    ? entities.reduce((s, e) => s + e.exploitation_score, 0) / entities.length
    : 0;
  const avgSystemic = entities.length > 0
    ? entities.reduce((s, e) => s + e.systemic_score, 0) / entities.length
    : 0;

  const dists = [
    { title: "Risque", counts: summary.risk_distribution, colors: RISK_COLORS },
    { title: "Modèle", counts: summary.pattern_distribution, colors: PAT_COLORS },
    { title: "Sévérité", counts: summary.severity_distribution, colors: SEV_COLORS },
    { title: "Action", counts: summary.action_distribution, colors: ACT_COLORS },
  ];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-300 p-6 space-y-6">
      {selected && <DetailModal entity={selected} onClose={() => setSelected(null)} />}

      <div>
        <h1 className="text-2xl font-bold text-orange-400">Fragilité Économie Gig &amp; Précariat — Module 334</h1>
        <p className="text-slate-400 text-sm mt-1">Précarité · Droits · Exploitation · Systémique — Caelum Partners</p>
      </div>

      {/* 6 KPI cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {[
          ["Total Systèmes", summary.total_entities, "text-orange-400"],
          ["Effondrement Social", summary.critical_count, "text-red-400"],
          ["Crise Travail", summary.high_count, "text-orange-400"],
          ["Composite Moyen", summary.avg_composite.toFixed(1), "text-orange-400"],
          ["Index Précarité", summary.avg_estimated_precarity_index.toFixed(2), "text-amber-400"],
          ["Précarité Moyenne", avgPrecarity.toFixed(1), "text-red-400"],
        ].map(([l, v, c]) => (
          <div key={String(l)} className="bg-slate-900 border border-orange-600/30 rounded-xl p-3 text-center">
            <div className={`text-xl font-bold ${c}`}>{v}</div>
            <div className="text-xs text-slate-500 mt-0.5">{l}</div>
          </div>
        ))}
      </div>

      {/* 4 GaugeRings */}
      <div className="bg-slate-900 border border-orange-600/30 rounded-xl p-5">
        <div className="grid grid-cols-4 gap-4">
          <GaugeRing value={avgPrecarity}     label="Précarité"   color="#ef4444" />
          <GaugeRing value={avgRights}        label="Droits"      color="#f97316" />
          <GaugeRing value={avgExploitation}  label="Exploitation" color="#a855f7" />
          <GaugeRing value={avgSystemic}      label="Systémique"  color="#3b82f6" />
        </div>
      </div>

      {/* 4 DistBars */}
      <div className="bg-slate-900 border border-orange-600/30 rounded-xl p-5 grid grid-cols-1 md:grid-cols-2 gap-5">
        {dists.map(d => <DistBar key={d.title} {...d} />)}
      </div>

      {/* Filter pills */}
      <div className="flex flex-wrap gap-2">
        {["all", "low", "moderate", "high", "critical"].map(r => (
          <button key={r} onClick={() => setRiskFilter(r)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${riskFilter === r ? "bg-orange-800 border-orange-700 text-white" : "bg-slate-900 border-orange-600/30 text-slate-400 hover:text-white"}`}>
            {r === "all" ? "Tous les risques" : r}
          </button>
        ))}
        <span className="w-px h-5 self-center bg-orange-600/30" />
        {["all", "precariat_explosion", "algorithmic_serfdom", "rights_collapse", "demographic_exploitation", "systemic_dualization"].map(p => (
          <button key={p} onClick={() => setPatFilter(p)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${patFilter === p ? "bg-slate-700 border-orange-600 text-white" : "bg-slate-900 border-orange-600/30 text-slate-400 hover:text-white"}`}>
            {p === "all" ? "Tous les modèles" : p.replace(/_/g, " ")}
          </button>
        ))}
      </div>

      {/* Entity cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {filtered.map(e => (
          <div key={e.id} onClick={() => setSelected(e)}
            className="bg-slate-900 border border-orange-600/30 rounded-xl p-4 cursor-pointer hover:border-orange-500 transition-colors">
            <div className="flex items-center justify-between mb-2">
              <span className="font-bold text-white">{e.id}</span>
              <span className="text-xs text-slate-400">{e.region}</span>
            </div>
            <div className="text-xs text-slate-500 mb-2 capitalize">{e.labor_sector.replace(/_/g, " ")}</div>
            <div className="flex gap-1 mb-3 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[e.risk_level] || "bg-slate-700 text-slate-300"}`}>{e.risk_level}</span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[e.severity] || "bg-slate-700 text-slate-300"}`}>{e.severity.replace(/_/g, " ")}</span>
            </div>
            <div className="text-2xl font-black text-orange-400 mb-1">{e.composite_score.toFixed(1)}</div>
            <div className="text-xs text-slate-500 mb-2 capitalize">{e.gig_pattern.replace(/_/g, " ")}</div>
            <div className="text-xs text-slate-400 truncate">{e.signal}</div>
          </div>
        ))}
      </div>
    </div>
  );
}
