"use client";
import { useEffect, useState } from "react";

type DarkWebEntity = {
  entity_id: string; market_type: string; region: string;
  risk_level: string; crime_pattern: string;
  severity: string; recommended_action: string;
  crime_scale_score: number; ecosystem_score: number;
  enforcement_gap_score: number; spillover_score: number;
  composite_score: number; signal: string;
  ransomware_ecosystem_scale: number;
  crypto_laundering_volume: number;
};

type Summary = {
  module_id: number; module_name: string;
  total: number;
  critical: number; high: number;
  moderate: number; low: number;
  avg_composite: number;
  pattern_distribution: Record<string, number>;
  risk_distribution: Record<string, number>;
  severity_distribution: Record<string, number>;
  action_distribution: Record<string, number>;
  avg_estimated_darkweb_risk_index: number;
};

function GaugeRing({ value, label, color }: { value: number; label: string; color: string }) {
  const r = 36; const circ = 2 * Math.PI * r;
  const fill = circ * (1 - value / 100);
  return (
    <div className="flex flex-col items-center gap-1">
      <svg width="88" height="88" viewBox="0 0 88 88">
        <circle cx="44" cy="44" r={r} fill="none" stroke="#0f172a" strokeWidth="8"/>
        <circle cx="44" cy="44" r={r} fill="none" stroke={color} strokeWidth="8"
          strokeDasharray={circ} strokeDashoffset={fill}
          strokeLinecap="round" transform="rotate(-90 44 44)"/>
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
          <div key={k} style={{ width: `${v / total * 100}%`, background: colors[k] || "#475569" }} title={`${k}: ${v}`}/>
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

const RISK_COLORS = { low: "#10b981", moderate: "#f59e0b", high: "#f97316", critical: "#ef4444" };
const PAT_COLORS  = {
  none:                              "#10b981",
  ransomware_industrial_complex:     "#ef4444",
  nation_state_crime_market:         "#f97316",
  criminal_marketplace_empire:       "#a855f7",
  AI_crime_automation_crisis:        "#06b6d4",
  human_trafficking_digital_network: "#eab308",
};
const SEV_COLORS  = {
  "risque_darkweb_contenu":              "#10b981",
  "vulnérabilité_darkweb_structurelle":  "#f59e0b",
  "marché_souterrain_majeur":            "#f97316",
  "économie_criminelle_systémique":      "#ef4444",
};
const ACT_COLORS  = {
  veille_darkweb_continue:                   "#10b981",
  "surveillance_renforcée_marchés_illicites": "#f59e0b",
  neutralisation_réseau_souterrain:           "#f97316",
  "démantèlement_urgence_darkweb":            "#ef4444",
};

const RISK_BADGE: Record<string, string> = {
  low:      "bg-emerald-900 text-emerald-300",
  moderate: "bg-amber-900 text-amber-300",
  high:     "bg-orange-900 text-orange-300",
  critical: "bg-red-900 text-red-300",
};
const SEV_BADGE: Record<string, string> = {
  "risque_darkweb_contenu":             "bg-emerald-900 text-emerald-300",
  "vulnérabilité_darkweb_structurelle": "bg-amber-900 text-amber-300",
  "marché_souterrain_majeur":           "bg-orange-900 text-orange-300",
  "économie_criminelle_systémique":     "bg-red-900 text-red-300",
};

function DetailModal({ entity, onClose }: { entity: DarkWebEntity; onClose: () => void }) {
  const [tab, setTab] = useState<"scores" | "analyse" | "actions">("scores");

  useEffect(() => {
    const h = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", h);
    return () => window.removeEventListener("keydown", h);
  }, [onClose]);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/75" onClick={onClose}>
      <div className="bg-slate-900 border border-purple-700/30 rounded-xl w-full max-w-lg p-6 shadow-2xl" onClick={e => e.stopPropagation()}>
        <div className="flex items-center justify-between mb-4">
          <div>
            <span className="text-lg font-bold text-white">{entity.entity_id}</span>
            <span className="ml-2 text-purple-400 text-xs">{entity.market_type.replace(/_/g, " ")}</span>
            <span className="ml-2 text-slate-400 text-xs">{entity.region}</span>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl leading-none">✕</button>
        </div>
        <div className="flex gap-2 mb-4">
          {(["scores", "analyse", "actions"] as const).map(t => (
            <button key={t} onClick={() => setTab(t)}
              className={`px-3 py-1 rounded text-xs font-medium transition-colors ${tab === t ? "bg-purple-700 text-white" : "bg-slate-800 text-slate-400 hover:text-white"}`}>
              {t.charAt(0).toUpperCase() + t.slice(1)}
            </button>
          ))}
        </div>

        {tab === "scores" && (
          <div className="grid grid-cols-2 gap-3 text-sm">
            {[
              ["Échelle Crime",      entity.crime_scale_score,      "#ef4444"],
              ["Écosystème",         entity.ecosystem_score,        "#a855f7"],
              ["Lacune Répression",  entity.enforcement_gap_score,  "#f97316"],
              ["Contamination",      entity.spillover_score,        "#06b6d4"],
            ].map(([l, v, c]) => (
              <div key={String(l)} className="bg-slate-800 border border-purple-700/20 rounded-lg p-3">
                <div className="text-slate-400 text-xs mb-1">{String(l)}</div>
                <div className="text-white font-bold text-lg">{Number(v).toFixed(1)}</div>
                <div className="h-1.5 rounded mt-1 bg-slate-700">
                  <div className="h-1.5 rounded" style={{ width: `${Math.min(Number(v), 100)}%`, background: String(c) }}/>
                </div>
              </div>
            ))}
            <div className="col-span-2 bg-slate-800 border border-purple-700/20 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Score Composite Dark Web</div>
              <div className="text-white font-bold text-2xl">{entity.composite_score.toFixed(1)}</div>
            </div>
          </div>
        )}

        {tab === "analyse" && (
          <div className="bg-slate-800 border border-purple-700/20 rounded-lg p-4 text-sm text-slate-200 leading-relaxed">
            {entity.signal}
            <div className="mt-3 flex gap-2 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[entity.risk_level] || "bg-slate-700 text-slate-300"}`}>
                {entity.risk_level}
              </span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[entity.severity] || "bg-slate-700 text-slate-300"}`}>
                {entity.severity.replace(/_/g, " ")}
              </span>
              <span className="px-2 py-0.5 rounded text-xs font-medium bg-slate-700 text-purple-300">
                {entity.crime_pattern.replace(/_/g, " ")}
              </span>
            </div>
            <div className="mt-3 grid grid-cols-2 gap-2 text-xs text-slate-400">
              <div>Ransomware Scale: <span className="text-red-400 font-medium">{entity.ransomware_ecosystem_scale.toFixed(2)}</span></div>
              <div>Crypto Laundering: <span className="text-purple-400 font-medium">{entity.crypto_laundering_volume.toFixed(2)}</span></div>
            </div>
          </div>
        )}

        {tab === "actions" && (
          <div className="space-y-3 text-sm">
            <div className="bg-slate-800 border border-purple-700/20 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Action Recommandée</div>
              <div className="text-white font-medium">{entity.recommended_action.replace(/_/g, " ")}</div>
            </div>
            <div className="bg-slate-800 border border-purple-700/20 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Sévérité Marché Souterrain</div>
              <div className="text-white font-medium">{entity.severity.replace(/_/g, " ")}</div>
            </div>
            <div className="bg-slate-800 border border-purple-700/20 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Patron Criminel Détecté</div>
              <div className="text-amber-400 font-medium">{entity.crime_pattern.replace(/_/g, " ")}</div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function DarkWebEconomyDashboard() {
  const [data, setData]         = useState<{ entities: DarkWebEntity[]; summary: Summary } | null>(null);
  const [riskFilter, setRisk]   = useState<string>("all");
  const [regFilter, setReg]     = useState<string>("all");
  const [selected, setSelected] = useState<DarkWebEntity | null>(null);

  useEffect(() => {
    fetch("/api/dark-web-economy-engine")
      .then(r => r.json())
      .then(setData)
      .catch(console.error);
  }, []);

  if (!data) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-purple-400 text-lg animate-pulse">Initialisation du Moteur Économie Dark Web...</div>
    </div>
  );

  const { entities, summary } = data;

  const regions  = ["all", ...Array.from(new Set(entities.map(e => e.region)))];
  const filtered = entities.filter(e =>
    (riskFilter === "all" || e.risk_level === riskFilter) &&
    (regFilter  === "all" || e.region === regFilter)
  );

  const avgCrimeScale     = entities.reduce((s, e) => s + e.crime_scale_score,      0) / (entities.length || 1);
  const avgEcosystem      = entities.reduce((s, e) => s + e.ecosystem_score,         0) / (entities.length || 1);
  const avgEnforcementGap = entities.reduce((s, e) => s + e.enforcement_gap_score,   0) / (entities.length || 1);
  const avgSpillover      = entities.reduce((s, e) => s + e.spillover_score,         0) / (entities.length || 1);

  const dists = [
    { title: "Niveau de Risque Dark Web",     counts: summary.risk_distribution,     colors: RISK_COLORS },
    { title: "Patron Criminel Souterrain",    counts: summary.pattern_distribution,  colors: PAT_COLORS  },
    { title: "Sévérité Marché",              counts: summary.severity_distribution, colors: SEV_COLORS  },
    { title: "Action Recommandée",           counts: summary.action_distribution,   colors: ACT_COLORS  },
  ] as Array<{ title: string; counts: Record<string, number>; colors: Record<string, string> }>;

  const criticalCount = summary.critical;
  const highCount     = summary.high;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-300 p-6 space-y-6">
      {selected && <DetailModal entity={selected} onClose={() => setSelected(null)}/>}

      {/* En-tête */}
      <div>
        <h1 className="text-2xl font-bold text-purple-400">
          Économie Dark Web &amp; Marchés Souterrains — Module 384
        </h1>
        <p className="text-slate-400 text-sm mt-1">
          Ransomware · Trafic · Cybercrime · IA Criminelle · Contamination — Intelligence Darknet — Caelum Partners
        </p>
        <p className="text-slate-500 text-xs mt-0.5">Chaima Mhadbi — Bruxelles</p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {[
          ["Total Marchés",        summary.total,                                              "text-slate-300"],
          ["Empire Ransomware",    criticalCount,                                              "text-red-400"],
          ["Crise Majeure",        highCount,                                                  "text-orange-400"],
          ["Composite Moyen",      summary.avg_composite.toFixed(1),                           "text-amber-400"],
          ["Index Risque Dark Web", summary.avg_estimated_darkweb_risk_index.toFixed(2) + "/10", "text-purple-400"],
          ["Crime Moyen",          avgCrimeScale.toFixed(1),                                   "text-rose-400"],
        ].map(([l, v, c]) => (
          <div key={String(l)} className="bg-slate-900 border border-purple-700/30 rounded-xl p-3 text-center">
            <div className={`text-xl font-bold ${c}`}>{v}</div>
            <div className="text-xs text-slate-500 mt-0.5 leading-tight">{l}</div>
          </div>
        ))}
      </div>

      {/* Gauge Rings */}
      <div className="bg-slate-900 border border-purple-700/30 rounded-xl p-5">
        <p className="text-xs text-slate-500 mb-4 font-medium">Scores Moyens par Dimension Dark Web</p>
        <div className="grid grid-cols-4 gap-4">
          <GaugeRing value={avgCrimeScale}     label="Échelle Crime"     color="#ef4444"/>
          <GaugeRing value={avgEcosystem}      label="Écosystème"        color="#a855f7"/>
          <GaugeRing value={avgEnforcementGap} label="Lacune Répression" color="#f97316"/>
          <GaugeRing value={avgSpillover}      label="Contamination"     color="#06b6d4"/>
        </div>
      </div>

      {/* Distribution Bars */}
      <div className="bg-slate-900 border border-purple-700/30 rounded-xl p-5 grid grid-cols-1 md:grid-cols-2 gap-5">
        {dists.map(d => <DistBar key={d.title} {...d}/>)}
      </div>

      {/* Filtres */}
      <div className="flex flex-wrap gap-2">
        {["all", "low", "moderate", "high", "critical"].map(r => (
          <button key={r} onClick={() => setRisk(r)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${riskFilter === r ? "bg-purple-700 border-purple-600 text-white" : "bg-slate-900 border-purple-700/30 text-slate-400 hover:text-white"}`}>
            {r === "all" ? "Tous risques" : r}
          </button>
        ))}
        <span className="w-px h-5 self-center bg-purple-700/30"/>
        {regions.map(r => (
          <button key={r} onClick={() => setReg(r)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${regFilter === r ? "bg-slate-700 border-slate-500 text-white" : "bg-slate-900 border-purple-700/30 text-slate-400 hover:text-white"}`}>
            {r === "all" ? "Toutes régions" : r}
          </button>
        ))}
      </div>

      {/* Cartes Entités */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {filtered.map(e => (
          <div key={e.entity_id} onClick={() => setSelected(e)}
            className="bg-slate-900 border border-slate-800 rounded-xl p-4 cursor-pointer hover:border-purple-700/50 transition-colors">
            <div className="flex items-center justify-between mb-1">
              <span className="font-bold text-white">{e.entity_id}</span>
              <span className="text-xs text-slate-400">{e.region}</span>
            </div>
            <div className="text-xs text-purple-400 mb-2 capitalize">{e.market_type.replace(/_/g, " ")}</div>
            <div className="flex gap-1 mb-3 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[e.risk_level] || "bg-slate-700 text-slate-300"}`}>
                {e.risk_level}
              </span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[e.severity] || "bg-slate-700 text-slate-300"}`}>
                {e.severity.replace(/_/g, " ")}
              </span>
            </div>
            <div className="text-2xl font-black text-white mb-1">{e.composite_score.toFixed(1)}</div>
            <div className="text-xs text-slate-500 mb-2 capitalize">{e.crime_pattern.replace(/_/g, " ")}</div>
            <div className="text-xs text-amber-400 font-medium mb-2">{e.recommended_action.replace(/_/g, " ")}</div>
            <div className="text-xs text-slate-400 truncate">{e.signal}</div>
          </div>
        ))}
      </div>
    </div>
  );
}
