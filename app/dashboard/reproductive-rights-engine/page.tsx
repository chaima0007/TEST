"use client";
import { useEffect, useState } from "react";

type Entity = {
  entity_id: string;
  region: string;
  rights_domain: string;
  reproductive_risk: string;
  reproductive_pattern: string;
  reproductive_severity: string;
  recommended_action: string;
  access_score: number;
  legal_score: number;
  coercion_score: number;
  disparity_score: number;
  reproductive_composite: number;
  is_in_reproductive_crisis: boolean;
  requires_reproductive_intervention: boolean;
  reproductive_signal: string;
};

type Summary = {
  total: number;
  risk_counts: Record<string, number>;
  pattern_counts: Record<string, number>;
  severity_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_reproductive_composite: number;
  reproductive_crisis_count: number;
  reproductive_intervention_count: number;
  avg_access_score: number;
  avg_legal_score: number;
  avg_coercion_score: number;
  avg_disparity_score: number;
  avg_estimated_reproductive_rights_index: number;
};

function GaugeRing({ value, label, color }: { value: number; label: string; color: string }) {
  const r = 36;
  const circ = 2 * Math.PI * r;
  const fill = circ * (1 - value / 100);
  return (
    <div className="flex flex-col items-center gap-1">
      <svg width="88" height="88" viewBox="0 0 88 88">
        <circle cx="44" cy="44" r={r} fill="none" stroke="#1e1030" strokeWidth="8" />
        <circle cx="44" cy="44" r={r} fill="none" stroke={color} strokeWidth="8"
          strokeDasharray={circ} strokeDashoffset={fill}
          strokeLinecap="round" transform="rotate(-90 44 44)" />
        <text x="44" y="49" textAnchor="middle" fill="white" fontSize="13" fontWeight="bold">
          {Math.round(value)}
        </text>
      </svg>
      <span className="text-xs text-rose-300/70 text-center">{label}</span>
    </div>
  );
}

function DistBar({ title, counts, colors }: { title: string; counts: Record<string, number>; colors: Record<string, string> }) {
  const total = Object.values(counts).reduce((a, b) => a + b, 0) || 1;
  return (
    <div className="flex flex-col gap-1">
      <span className="text-xs text-rose-300/70 font-medium">{title}</span>
      <div className="flex h-3 rounded overflow-hidden gap-px">
        {Object.entries(counts).map(([k, v]) => (
          <div key={k} style={{ width: `${(v / total) * 100}%`, background: colors[k] || "#475569" }} title={`${k}: ${v}`} />
        ))}
      </div>
      <div className="flex flex-wrap gap-x-3 gap-y-0.5">
        {Object.entries(counts).map(([k, v]) => (
          <span key={k} className="text-xs text-rose-300/60">
            <span style={{ color: colors[k] || "#94a3b8" }}>■</span> {k.replace(/_/g, " ")} {v}
          </span>
        ))}
      </div>
    </div>
  );
}

const RISK_COLORS = { low: "#10b981", moderate: "#f59e0b", high: "#f97316", critical: "#ef4444" };
const PAT_COLORS: Record<string, string> = {
  none: "#10b981",
  total_abortion_ban_crisis: "#7f1d1d",
  coercive_sterilization_pattern: "#dc2626",
  maternal_mortality_collapse: "#f97316",
  contraception_access_barrier: "#a855f7",
  reproductive_surveillance_state: "#0ea5e9",
};
const SEV_COLORS: Record<string, string> = {
  autonomie_corporelle_préservée: "#10b981",
  stress_reproductif: "#f59e0b",
  "risque_reproductif_élevé": "#f97316",
  urgence_reproductive: "#7f1d1d",
};
const ACTION_COLORS: Record<string, string> = {
  aucune_action: "#10b981",
  surveillance_reproductive: "#06b6d4",
  renforcement_droits_reproductifs: "#f59e0b",
  sauvetage_maternel_prioritaire: "#f97316",
  intervention_d_urgence_reproductive: "#ef4444",
};

const RISK_BADGE: Record<string, string> = {
  low: "bg-emerald-900 text-emerald-300",
  moderate: "bg-amber-900 text-amber-300",
  high: "bg-orange-900 text-orange-300",
  critical: "bg-red-950 text-red-400",
};
const SEV_BADGE: Record<string, string> = {
  autonomie_corporelle_préservée: "bg-emerald-900 text-emerald-300",
  stress_reproductif: "bg-amber-900 text-amber-300",
  "risque_reproductif_élevé": "bg-orange-900 text-orange-300",
  urgence_reproductive: "bg-red-950 text-red-400",
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
      <div className="bg-slate-950 border border-rose-500/30 rounded-xl w-full max-w-lg p-6 shadow-2xl" onClick={e => e.stopPropagation()}>
        <div className="flex items-center justify-between mb-4">
          <div>
            <span className="text-lg font-bold text-white">{entity.entity_id}</span>
            <span className="ml-2 text-rose-400 text-xs">{entity.region}</span>
            <span className="ml-2 text-slate-500 text-xs">{entity.rights_domain.replace(/_/g, " ")}</span>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl leading-none">✕</button>
        </div>
        <div className="flex gap-2 mb-4">
          {(["scores", "signal", "action"] as const).map(t => (
            <button key={t} onClick={() => setTab(t)}
              className={`px-3 py-1 rounded text-xs font-medium transition-colors ${tab === t ? "bg-rose-900 text-white" : "bg-slate-900 text-slate-400 hover:text-white"}`}>
              {t === "scores" ? "Scores" : t === "signal" ? "Signal" : "Action"}
            </button>
          ))}
        </div>

        {tab === "scores" && (
          <div className="grid grid-cols-2 gap-3 text-sm">
            {[
              ["Score Accès",       entity.access_score,    "#ef4444"],
              ["Score Légal",       entity.legal_score,     "#f97316"],
              ["Score Coercition",  entity.coercion_score,  "#a855f7"],
              ["Score Disparité",   entity.disparity_score, "#0ea5e9"],
            ].map(([l, v, c]) => (
              <div key={String(l)} className="bg-slate-900 border border-rose-500/20 rounded-lg p-3">
                <div className="text-rose-300/60 text-xs mb-1">{String(l)}</div>
                <div className="text-white font-bold text-lg">{Number(v).toFixed(1)}</div>
                <div className="h-1.5 rounded mt-1 bg-slate-800">
                  <div className="h-1.5 rounded" style={{ width: `${Math.min(Number(v), 100)}%`, background: String(c) }} />
                </div>
              </div>
            ))}
            <div className="col-span-2 bg-slate-900 border border-rose-500/20 rounded-lg p-3">
              <div className="text-rose-300/60 text-xs mb-1">Composite Reproductif</div>
              <div className="text-white font-bold text-2xl">{entity.reproductive_composite.toFixed(1)}</div>
            </div>
          </div>
        )}

        {tab === "signal" && (
          <div className="bg-slate-900 border border-rose-500/20 rounded-lg p-4 text-sm text-slate-200 leading-relaxed">
            {entity.reproductive_signal}
            <div className="mt-3 flex gap-2 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[entity.reproductive_risk] || "bg-slate-700 text-slate-300"}`}>
                {entity.reproductive_risk}
              </span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[entity.reproductive_severity] || "bg-slate-700 text-slate-300"}`}>
                {entity.reproductive_severity.replace(/_/g, " ")}
              </span>
            </div>
          </div>
        )}

        {tab === "action" && (
          <div className="space-y-3 text-sm">
            <div className="bg-slate-900 border border-rose-500/20 rounded-lg p-3">
              <div className="text-rose-300/60 text-xs mb-1">Action Recommandée</div>
              <div className="text-white font-medium">{entity.recommended_action.replace(/_/g, " ")}</div>
            </div>
            <div className="bg-slate-900 border border-rose-500/20 rounded-lg p-3">
              <div className="text-rose-300/60 text-xs mb-1">Pattern Reproductif</div>
              <div className="text-white font-medium capitalize">{entity.reproductive_pattern.replace(/_/g, " ")}</div>
            </div>
            <div className="flex gap-2 flex-wrap">
              {entity.is_in_reproductive_crisis && (
                <span className="px-2 py-1 rounded bg-red-950 text-red-400 text-xs font-medium">CRISE REPRODUCTIVE</span>
              )}
              {entity.requires_reproductive_intervention && (
                <span className="px-2 py-1 rounded bg-orange-950 text-orange-400 text-xs font-medium">INTERVENTION REQ.</span>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function ReproductiveRightsDashboard() {
  const [data, setData]           = useState<{ entities: Entity[]; summary: Summary } | null>(null);
  const [filter, setFilter]       = useState<string>("all");
  const [patFilter, setPatFilter] = useState<string>("all");
  const [selected, setSelected]   = useState<Entity | null>(null);

  useEffect(() => {
    fetch("/api/reproductive-rights-engine")
      .then(r => r.json())
      .then(setData)
      .catch(console.error);
  }, []);

  if (!data) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-rose-400 text-lg animate-pulse">Initialisation du Moteur Droits Reproductifs...</div>
    </div>
  );

  const { entities, summary } = data;
  const filtered = entities.filter(e =>
    (filter === "all" || e.reproductive_risk === filter) &&
    (patFilter === "all" || e.reproductive_pattern === patFilter)
  );

  const dists = [
    { title: "Niveau de Risque",         counts: summary.risk_counts,     colors: RISK_COLORS   },
    { title: "Pattern Reproductif",      counts: summary.pattern_counts,  colors: PAT_COLORS    },
    { title: "Sévérité",                 counts: summary.severity_counts, colors: SEV_COLORS    },
    { title: "Action Recommandée",       counts: summary.action_counts,   colors: ACTION_COLORS },
  ] as Array<{ title: string; counts: Record<string, number>; colors: Record<string, string> }>;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {selected && <DetailModal entity={selected} onClose={() => setSelected(null)} />}

      <div>
        <h1 className="text-2xl font-bold text-rose-400">Droits Reproductifs & Autonomie Corporelle — Module 396</h1>
        <p className="text-rose-300/50 text-sm mt-1">Accès aux Soins · Cadre Légal · Coercition · Disparités Structurelles</p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {[
          ["Entités Analysées",              summary.total,                                                  "text-rose-400"],
          ["Crises Reproductives",           summary.reproductive_crisis_count,                              "text-red-400"],
          ["Interventions Requises",         summary.reproductive_intervention_count,                        "text-orange-400"],
          ["Composite Moy.",                 summary.avg_reproductive_composite.toFixed(1),                  "text-violet-400"],
          ["Indice Droits Reproductifs",     summary.avg_estimated_reproductive_rights_index.toFixed(2),     "text-amber-400"],
          ["Score Accès Moy.",               summary.avg_access_score.toFixed(1),                            "text-rose-500"],
        ].map(([l, v, c]) => (
          <div key={String(l)} className="bg-slate-900 border border-rose-500/30 rounded-xl p-3 text-center">
            <div className={`text-xl font-bold ${c}`}>{v}</div>
            <div className="text-xs text-rose-300/40 mt-0.5 leading-tight">{l}</div>
          </div>
        ))}
      </div>

      {/* Gauge Rings */}
      <div className="bg-slate-900 border border-rose-500/30 rounded-xl p-5">
        <div className="grid grid-cols-4 gap-4">
          <GaugeRing value={summary.avg_access_score}    label="Accès aux Soins Moy."    color="#ef4444" />
          <GaugeRing value={summary.avg_legal_score}     label="Score Légal Moy."         color="#f97316" />
          <GaugeRing value={summary.avg_coercion_score}  label="Score Coercition Moy."    color="#a855f7" />
          <GaugeRing value={summary.avg_disparity_score} label="Score Disparité Moy."     color="#0ea5e9" />
        </div>
      </div>

      {/* Distribution Bars */}
      <div className="bg-slate-900 border border-rose-500/30 rounded-xl p-5 grid grid-cols-1 md:grid-cols-2 gap-5">
        {dists.map(d => <DistBar key={d.title} {...d} />)}
      </div>

      {/* Filter Pills */}
      <div className="flex flex-wrap gap-2">
        {["all", "low", "moderate", "high", "critical"].map(r => (
          <button key={r} onClick={() => setFilter(r)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${filter === r ? "bg-rose-900 border-rose-700 text-white" : "bg-slate-900 border-rose-500/30 text-rose-400/70 hover:text-white"}`}>
            {r}
          </button>
        ))}
        <span className="w-px h-5 self-center bg-rose-500/30" />
        {["all", "none", "total_abortion_ban_crisis", "coercive_sterilization_pattern", "maternal_mortality_collapse", "contraception_access_barrier", "reproductive_surveillance_state"].map(p => (
          <button key={p} onClick={() => setPatFilter(p)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${patFilter === p ? "bg-rose-950 border-rose-700 text-white" : "bg-slate-900 border-rose-500/30 text-rose-400/70 hover:text-white"}`}>
            {p.replace(/_/g, " ")}
          </button>
        ))}
      </div>

      {/* Entity Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {filtered.map(e => (
          <div key={e.entity_id} onClick={() => setSelected(e)}
            className="bg-slate-900 border border-rose-500/30 rounded-xl p-4 cursor-pointer hover:border-rose-400 transition-colors">
            <div className="flex items-center justify-between mb-1">
              <span className="font-bold text-white">{e.entity_id}</span>
              <span className="text-xs text-rose-400/60">{e.region}</span>
            </div>
            <div className="text-xs text-slate-500 mb-2 capitalize">{e.rights_domain.replace(/_/g, " ")}</div>
            <div className="flex gap-1 mb-3 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[e.reproductive_risk] || "bg-slate-700 text-slate-300"}`}>
                {e.reproductive_risk}
              </span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[e.reproductive_severity] || "bg-slate-700 text-slate-300"}`}>
                {e.reproductive_severity.replace(/_/g, " ")}
              </span>
            </div>
            <div className="text-2xl font-black text-white mb-1">{e.reproductive_composite.toFixed(1)}</div>
            <div className="text-xs text-rose-400/60 mb-2 capitalize">{e.reproductive_pattern.replace(/_/g, " ")}</div>
            <div className="text-xs text-violet-400 font-medium mb-2">
              Accès: {e.access_score.toFixed(1)} · Légal: {e.legal_score.toFixed(1)}
            </div>
            <div className="flex gap-1 flex-wrap">
              {e.is_in_reproductive_crisis && (
                <span className="px-1.5 py-0.5 rounded bg-red-950 text-red-400 text-xs">CRISE</span>
              )}
              {e.requires_reproductive_intervention && (
                <span className="px-1.5 py-0.5 rounded bg-orange-950 text-orange-400 text-xs">INTERVENTION</span>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
