"use client";
import { useEffect, useState } from "react";

type DHSEntity = {
  id: string;
  name: string;
  country: string;
  sector: string;
  composite_score: number;
  data_sovereignty_gap: number;
  cyber_resilience_gap: number;
  platform_dependency: number;
  interoperability_gap: number;
  risk_level: string;
  primary_pattern: string;
  key_signals: string[];
  estimated_health_index: number;
  last_updated: string;
};

type DHSSummary = {
  total_entities: number;
  avg_composite: number;
  risk_distribution: Record<string, number>;
  pattern_distribution: Record<string, number>;
  top_risk_entities: string[];
  critical_alerts: number;
  last_analysis: string;
  engine_version: string;
  domain: string;
  confidence_score: number;
  data_sources: string[];
  entities: DHSEntity[];
  avg_estimated_health_index: number;
};

function GaugeRing({ value, label, color }: { value: number; label: string; color: string }) {
  const r = 36;
  const circ = 2 * Math.PI * r;
  const fill = circ * (1 - value / 100);
  return (
    <div className="flex flex-col items-center gap-1">
      <svg width="88" height="88" viewBox="0 0 88 88">
        <circle cx="44" cy="44" r={r} fill="none" stroke="#0a1628" strokeWidth="8" />
        <circle cx="44" cy="44" r={r} fill="none" stroke={color} strokeWidth="8"
          strokeDasharray={circ} strokeDashoffset={fill}
          strokeLinecap="round" transform="rotate(-90 44 44)" />
        <text x="44" y="49" textAnchor="middle" fill="white" fontSize="13" fontWeight="bold">
          {Math.round(value)}
        </text>
      </svg>
      <span className="text-xs text-emerald-300/70 text-center">{label}</span>
    </div>
  );
}

function DistBar({ title, counts, colors }: { title: string; counts: Record<string, number>; colors: Record<string, string> }) {
  const total = Object.values(counts).reduce((a, b) => a + b, 0) || 1;
  return (
    <div className="flex flex-col gap-1">
      <span className="text-xs text-emerald-300/70 font-medium">{title}</span>
      <div className="flex h-3 rounded overflow-hidden gap-px">
        {Object.entries(counts).map(([k, v]) => (
          <div key={k} style={{ width: `${(v / total) * 100}%`, background: colors[k] || "#475569" }} title={`${k}: ${v}`} />
        ))}
      </div>
      <div className="flex flex-wrap gap-x-3 gap-y-0.5">
        {Object.entries(counts).map(([k, v]) => (
          <span key={k} className="text-xs text-emerald-300/60">
            <span style={{ color: colors[k] || "#94a3b8" }}>■</span> {k.replace(/_/g, " ")} {v}
          </span>
        ))}
      </div>
    </div>
  );
}

const RISK_COLORS: Record<string, string> = { faible: "#10b981", "modéré": "#f59e0b", "élevé": "#3b82f6", critique: "#ef4444" };
const PAT_COLORS: Record<string, string> = {
  "Souveraineté Santé Numérique Maîtrisée": "#10b981",
  "Risque Souveraineté Santé Numérique": "#f59e0b",
  "Fragmentation Interopérabilité": "#a855f7",
  "Dépendance Plateformes Étrangères": "#f97316",
  "Vulnérabilité Cybersécurité Hospitalière": "#06b6d4",
  "Fuite Données Médicales": "#ef4444",
};
const RISK_BADGE: Record<string, string> = {
  faible: "bg-emerald-900 text-emerald-300",
  "modéré": "bg-amber-900 text-amber-300",
  "élevé": "bg-blue-900 text-blue-300",
  critique: "bg-red-950 text-red-400",
};

function DetailModal({ entity, onClose }: { entity: DHSEntity; onClose: () => void }) {
  const [tab, setTab] = useState<"scores" | "signaux" | "actions">("scores");
  useEffect(() => {
    const h = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", h);
    return () => window.removeEventListener("keydown", h);
  }, [onClose]);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80" onClick={onClose}>
      <div className="bg-slate-950 border border-emerald-700/30 rounded-xl w-full max-w-lg p-6 shadow-2xl" onClick={e => e.stopPropagation()}>
        <div className="flex items-center justify-between mb-4">
          <div>
            <span className="text-lg font-bold text-white">{entity.name}</span>
            <span className="ml-2 text-emerald-400 text-xs">{entity.country}</span>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl leading-none">✕</button>
        </div>
        <div className="flex gap-2 mb-4">
          {(["scores", "signaux", "actions"] as const).map(t => (
            <button key={t} onClick={() => setTab(t)}
              className={`px-3 py-1 rounded text-xs font-medium transition-colors ${tab === t ? "bg-emerald-900 text-white" : "bg-slate-900 text-slate-400 hover:text-white"}`}>
              {t === "scores" ? "Scores" : t === "signaux" ? "Signaux" : "Actions"}
            </button>
          ))}
        </div>

        {tab === "scores" && (
          <div className="grid grid-cols-2 gap-3 text-sm">
            {[
              ["Souveraineté Données", entity.data_sovereignty_gap, "#ef4444"],
              ["Cyber-Résilience", entity.cyber_resilience_gap, "#f97316"],
              ["Dépendance Plateformes", entity.platform_dependency, "#a855f7"],
              ["Interopérabilité", entity.interoperability_gap, "#06b6d4"],
            ].map(([l, v, c]) => (
              <div key={String(l)} className="bg-slate-900 border border-emerald-700/20 rounded-lg p-3">
                <div className="text-emerald-300/60 text-xs mb-1">{String(l)}</div>
                <div className="text-white font-bold text-lg">{Number(v).toFixed(1)}</div>
                <div className="h-1.5 rounded mt-1 bg-slate-800">
                  <div className="h-1.5 rounded" style={{ width: `${Math.min(Number(v), 100)}%`, background: String(c) }} />
                </div>
              </div>
            ))}
            <div className="col-span-2 bg-slate-900 border border-emerald-700/20 rounded-lg p-3">
              <div className="text-emerald-300/60 text-xs mb-1">Score Composite Souveraineté Santé</div>
              <div className="text-white font-bold text-2xl">{entity.composite_score.toFixed(1)}</div>
            </div>
          </div>
        )}

        {tab === "signaux" && (
          <div className="space-y-3">
            <div className="flex gap-2 flex-wrap mb-2">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[entity.risk_level] || "bg-slate-700 text-slate-300"}`}>{entity.risk_level}</span>
              <span className="px-2 py-0.5 rounded text-xs font-medium bg-slate-800 text-emerald-300">{entity.primary_pattern}</span>
            </div>
            {entity.key_signals.map((sig, i) => (
              <div key={i} className="bg-slate-900 border border-emerald-700/20 rounded-lg p-3 text-sm text-slate-200">{sig}</div>
            ))}
            <div className="bg-slate-900 border border-emerald-700/20 rounded-lg p-3">
              <div className="text-emerald-300/50 text-xs mb-0.5">Index Souveraineté Santé Estimé</div>
              <div className="text-white text-sm font-medium">{entity.estimated_health_index.toFixed(2)} / 10</div>
            </div>
          </div>
        )}

        {tab === "actions" && (
          <div className="space-y-3 text-sm">
            <div className="bg-slate-900 border border-emerald-700/20 rounded-lg p-3">
              <div className="text-emerald-300/60 text-xs mb-1">Pattern Détecté</div>
              <div className="text-white font-medium">{entity.primary_pattern}</div>
            </div>
            <div className="bg-slate-900 border border-emerald-700/20 rounded-lg p-3">
              <div className="text-emerald-300/60 text-xs mb-1">Secteur</div>
              <div className="text-white font-medium">{entity.sector}</div>
            </div>
            <div className="bg-slate-900 border border-emerald-700/20 rounded-lg p-3">
              <div className="text-emerald-300/60 text-xs mb-1">Dernière Analyse</div>
              <div className="text-emerald-300 font-medium">{entity.last_updated}</div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function DigitalHealthSovereigntyDashboard() {
  const [data, setData] = useState<DHSSummary | null>(null);
  const [riskFilter, setRiskFilter] = useState<string>("all");
  const [patFilter, setPatFilter] = useState<string>("all");
  const [selected, setSelected] = useState<DHSEntity | null>(null);

  useEffect(() => {
    fetch("/api/digital-health-sovereignty-engine")
      .then(r => r.json())
      .then(setData)
      .catch(console.error);
  }, []);

  if (!data) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-emerald-400 text-lg animate-pulse">Initialisation du Moteur Souveraineté Santé Numérique...</div>
    </div>
  );

  const entities: DHSEntity[] = data.entities || [];
  const filtered = entities.filter(e =>
    (riskFilter === "all" || e.risk_level === riskFilter) &&
    (patFilter === "all" || e.primary_pattern === patFilter)
  );

  const avgData = entities.reduce((s, e) => s + e.data_sovereignty_gap, 0) / (entities.length || 1);
  const avgCyber = entities.reduce((s, e) => s + e.cyber_resilience_gap, 0) / (entities.length || 1);
  const avgPlatform = entities.reduce((s, e) => s + e.platform_dependency, 0) / (entities.length || 1);
  const avgInterop = entities.reduce((s, e) => s + e.interoperability_gap, 0) / (entities.length || 1);

  const patterns = [...new Set(entities.map(e => e.primary_pattern))];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {selected && <DetailModal entity={selected} onClose={() => setSelected(null)} />}

      <div>
        <h1 className="text-2xl font-bold text-emerald-400">Souveraineté Santé Numérique — Module Intelligence</h1>
        <p className="text-emerald-300/50 text-sm mt-1">
          Données Médicales · Cybersécurité Hospitalière · Dépendance Plateformes · Interopérabilité
        </p>
      </div>

      {/* 6 KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {[
          ["Total Entités", data.total_entities, "text-emerald-400"],
          ["Alertes Critiques", data.critical_alerts, "text-red-400"],
          ["Niveau Élevé", (data.risk_distribution?.["élevé"] ?? 0), "text-blue-400"],
          ["Score Composite Moy.", `${data.avg_composite.toFixed(1)}`, "text-emerald-300"],
          ["Index Santé Numérique", `${data.avg_estimated_health_index.toFixed(2)}/10`, "text-amber-400"],
          ["Confiance Analyse", `${data.confidence_score}%`, "text-teal-400"],
        ].map(([l, v, c]) => (
          <div key={String(l)} className="bg-slate-900 border border-emerald-700/30 rounded-xl p-3 text-center">
            <div className={`text-xl font-bold ${c}`}>{v}</div>
            <div className="text-xs text-emerald-300/40 mt-0.5 leading-tight">{l}</div>
          </div>
        ))}
      </div>

      {/* 4 Gauge Rings */}
      <div className="bg-slate-900 border border-emerald-700/30 rounded-xl p-5">
        <div className="grid grid-cols-4 gap-4">
          <GaugeRing value={avgData} label="Souveraineté Données" color="#ef4444" />
          <GaugeRing value={avgCyber} label="Lacune Cyber-Résilience" color="#f97316" />
          <GaugeRing value={avgPlatform} label="Dépendance Plateformes" color="#a855f7" />
          <GaugeRing value={avgInterop} label="Fragmentation Interop." color="#06b6d4" />
        </div>
      </div>

      {/* 4 Distribution Bars */}
      <div className="bg-slate-900 border border-emerald-700/30 rounded-xl p-5 grid grid-cols-1 md:grid-cols-2 gap-5">
        <DistBar title="Distribution par Risque" counts={data.risk_distribution} colors={RISK_COLORS} />
        <DistBar title="Distribution par Pattern" counts={data.pattern_distribution} colors={PAT_COLORS} />
        <DistBar title="Critique vs Autres" counts={{ "critique": data.critical_alerts, "autres": data.total_entities - data.critical_alerts }} colors={{ critique: "#ef4444", autres: "#10b981" }} />
        <DistBar title="Sources Données" counts={{ "OMS": 1, "ENISA": 1, "ITU": 1 }} colors={{ "OMS": "#06b6d4", "ENISA": "#a855f7", "ITU": "#f59e0b" }} />
      </div>

      {/* Filter Pills */}
      <div className="flex flex-wrap gap-2">
        {["all", "faible", "modéré", "élevé", "critique"].map(r => (
          <button key={r} onClick={() => setRiskFilter(r)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${riskFilter === r ? "bg-emerald-900 border-emerald-700 text-white" : "bg-slate-900 border-emerald-700/30 text-emerald-400/70 hover:text-white"}`}>
            {r}
          </button>
        ))}
        <span className="w-px h-5 self-center bg-emerald-700/30" />
        {["all", ...patterns].map(p => (
          <button key={p} onClick={() => setPatFilter(p)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${patFilter === p ? "bg-amber-950 border-amber-700 text-white" : "bg-slate-900 border-emerald-700/30 text-emerald-400/70 hover:text-white"}`}>
            {p === "all" ? "Tous Patterns" : p}
          </button>
        ))}
      </div>

      {/* Entity Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {filtered.map(e => (
          <div key={e.id} onClick={() => setSelected(e)}
            className="bg-slate-900 border border-emerald-700/30 rounded-xl p-4 cursor-pointer hover:border-emerald-500 transition-colors">
            <div className="flex items-center justify-between mb-1">
              <span className="font-bold text-white text-sm">{e.id}</span>
              <span className="text-xs text-emerald-400/60">{e.country}</span>
            </div>
            <div className="text-xs text-slate-400 mb-2 truncate">{e.name}</div>
            <div className="flex gap-1 mb-3">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[e.risk_level] || "bg-slate-700 text-slate-300"}`}>{e.risk_level}</span>
            </div>
            <div className="text-2xl font-black text-white mb-1">{e.composite_score.toFixed(1)}</div>
            <div className="text-xs text-emerald-400/60 mb-2">{e.primary_pattern}</div>
            <div className="text-xs text-emerald-400 font-medium mb-1">
              Data: {e.data_sovereignty_gap} · Cyber: {e.cyber_resilience_gap}
            </div>
            <div className="text-xs text-slate-500 truncate">{e.key_signals[0]}</div>
          </div>
        ))}
      </div>
    </div>
  );
}
