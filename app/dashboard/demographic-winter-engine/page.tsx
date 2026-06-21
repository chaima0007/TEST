"use client";
import { useEffect, useState } from "react";

type DWEntity = {
  id: string;
  name: string;
  country: string;
  sector: string;
  composite_score: number;
  fertility_decline_score: number;
  aging_index: number;
  migration_pressure: number;
  labor_shortage_score: number;
  risk_level: string;
  primary_pattern: string;
  key_signals: string[];
  estimated_demographic_index: number;
  last_updated: string;
};

type DWSummary = {
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
  entities: DWEntity[];
  avg_estimated_demographic_index: number;
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
      <span className="text-xs text-teal-300/70 text-center">{label}</span>
    </div>
  );
}

function DistBar({ title, counts, colors }: { title: string; counts: Record<string, number>; colors: Record<string, string> }) {
  const total = Object.values(counts).reduce((a, b) => a + b, 0) || 1;
  return (
    <div className="flex flex-col gap-1">
      <span className="text-xs text-teal-300/70 font-medium">{title}</span>
      <div className="flex h-3 rounded overflow-hidden gap-px">
        {Object.entries(counts).map(([k, v]) => (
          <div key={k} style={{ width: `${(v / total) * 100}%`, background: colors[k] || "#475569" }} title={`${k}: ${v}`} />
        ))}
      </div>
      <div className="flex flex-wrap gap-x-3 gap-y-0.5">
        {Object.entries(counts).map(([k, v]) => (
          <span key={k} className="text-xs text-teal-300/60">
            <span style={{ color: colors[k] || "#94a3b8" }}>■</span> {k.replace(/_/g, " ")} {v}
          </span>
        ))}
      </div>
    </div>
  );
}

const RISK_COLORS: Record<string, string> = { faible: "#10b981", "modéré": "#f59e0b", "élevé": "#3b82f6", critique: "#ef4444" };
const PAT_COLORS: Record<string, string> = {
  "Stabilité Démographique": "#10b981",
  "Déclin Démographique Structurel": "#f59e0b",
  "Pénurie Main-d'Œuvre": "#f97316",
  "Pression Migratoire Critique": "#a855f7",
  "Vieillissement Accéléré": "#06b6d4",
  "Effondrement Natalité": "#ef4444",
};
const RISK_BADGE: Record<string, string> = {
  faible: "bg-emerald-900 text-emerald-300",
  "modéré": "bg-amber-900 text-amber-300",
  "élevé": "bg-blue-900 text-blue-300",
  critique: "bg-red-950 text-red-400",
};

function DetailModal({ entity, onClose }: { entity: DWEntity; onClose: () => void }) {
  const [tab, setTab] = useState<"scores" | "signaux" | "actions">("scores");
  useEffect(() => {
    const h = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", h);
    return () => window.removeEventListener("keydown", h);
  }, [onClose]);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80" onClick={onClose}>
      <div className="bg-slate-950 border border-teal-700/30 rounded-xl w-full max-w-lg p-6 shadow-2xl" onClick={e => e.stopPropagation()}>
        <div className="flex items-center justify-between mb-4">
          <div>
            <span className="text-lg font-bold text-white">{entity.name}</span>
            <span className="ml-2 text-teal-400 text-xs">{entity.country}</span>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl leading-none">✕</button>
        </div>
        <div className="flex gap-2 mb-4">
          {(["scores", "signaux", "actions"] as const).map(t => (
            <button key={t} onClick={() => setTab(t)}
              className={`px-3 py-1 rounded text-xs font-medium transition-colors ${tab === t ? "bg-teal-900 text-white" : "bg-slate-900 text-slate-400 hover:text-white"}`}>
              {t === "scores" ? "Scores" : t === "signaux" ? "Signaux" : "Actions"}
            </button>
          ))}
        </div>

        {tab === "scores" && (
          <div className="grid grid-cols-2 gap-3 text-sm">
            {[
              ["Déclin Natalité", entity.fertility_decline_score, "#ef4444"],
              ["Index Vieillissement", entity.aging_index, "#f97316"],
              ["Pression Migratoire", entity.migration_pressure, "#a855f7"],
              ["Pénurie Travail", entity.labor_shortage_score, "#06b6d4"],
            ].map(([l, v, c]) => (
              <div key={String(l)} className="bg-slate-900 border border-teal-700/20 rounded-lg p-3">
                <div className="text-teal-300/60 text-xs mb-1">{String(l)}</div>
                <div className="text-white font-bold text-lg">{Number(v).toFixed(1)}</div>
                <div className="h-1.5 rounded mt-1 bg-slate-800">
                  <div className="h-1.5 rounded" style={{ width: `${Math.min(Number(v), 100)}%`, background: String(c) }} />
                </div>
              </div>
            ))}
            <div className="col-span-2 bg-slate-900 border border-teal-700/20 rounded-lg p-3">
              <div className="text-teal-300/60 text-xs mb-1">Score Composite Démographique</div>
              <div className="text-white font-bold text-2xl">{entity.composite_score.toFixed(1)}</div>
            </div>
          </div>
        )}

        {tab === "signaux" && (
          <div className="space-y-3">
            <div className="flex gap-2 flex-wrap mb-2">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[entity.risk_level] || "bg-slate-700 text-slate-300"}`}>{entity.risk_level}</span>
              <span className="px-2 py-0.5 rounded text-xs font-medium bg-slate-800 text-teal-300">{entity.primary_pattern}</span>
            </div>
            {entity.key_signals.map((sig, i) => (
              <div key={i} className="bg-slate-900 border border-teal-700/20 rounded-lg p-3 text-sm text-slate-200">{sig}</div>
            ))}
            <div className="bg-slate-900 border border-teal-700/20 rounded-lg p-3">
              <div className="text-teal-300/50 text-xs mb-0.5">Index Démographique Estimé</div>
              <div className="text-white text-sm font-medium">{entity.estimated_demographic_index.toFixed(2)} / 10</div>
            </div>
          </div>
        )}

        {tab === "actions" && (
          <div className="space-y-3 text-sm">
            <div className="bg-slate-900 border border-teal-700/20 rounded-lg p-3">
              <div className="text-teal-300/60 text-xs mb-1">Pattern Détecté</div>
              <div className="text-white font-medium">{entity.primary_pattern}</div>
            </div>
            <div className="bg-slate-900 border border-teal-700/20 rounded-lg p-3">
              <div className="text-teal-300/60 text-xs mb-1">Secteur</div>
              <div className="text-white font-medium">{entity.sector}</div>
            </div>
            <div className="bg-slate-900 border border-teal-700/20 rounded-lg p-3">
              <div className="text-teal-300/60 text-xs mb-1">Dernière Mise à Jour</div>
              <div className="text-teal-300 font-medium">{entity.last_updated}</div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function DemographicWinterDashboard() {
  const [data, setData] = useState<DWSummary | null>(null);
  const [riskFilter, setRiskFilter] = useState<string>("all");
  const [patFilter, setPatFilter] = useState<string>("all");
  const [selected, setSelected] = useState<DWEntity | null>(null);

  useEffect(() => {
    fetch("/api/demographic-winter-engine")
      .then(r => r.json())
      .then(setData)
      .catch(console.error);
  }, []);

  if (!data) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-teal-400 text-lg animate-pulse">Initialisation du Moteur Hiver Démographique...</div>
    </div>
  );

  const entities: DWEntity[] = data.entities || [];
  const filtered = entities.filter(e =>
    (riskFilter === "all" || e.risk_level === riskFilter) &&
    (patFilter === "all" || e.primary_pattern === patFilter)
  );

  const avgFertility = entities.reduce((s, e) => s + e.fertility_decline_score, 0) / (entities.length || 1);
  const avgAging = entities.reduce((s, e) => s + e.aging_index, 0) / (entities.length || 1);
  const avgMigration = entities.reduce((s, e) => s + e.migration_pressure, 0) / (entities.length || 1);
  const avgLabor = entities.reduce((s, e) => s + e.labor_shortage_score, 0) / (entities.length || 1);

  const patterns = [...new Set(entities.map(e => e.primary_pattern))];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {selected && <DetailModal entity={selected} onClose={() => setSelected(null)} />}

      <div>
        <h1 className="text-2xl font-bold text-teal-400">Hiver Démographique — Module Intelligence</h1>
        <p className="text-teal-300/50 text-sm mt-1">
          Déclin Natalité · Vieillissement Accéléré · Pression Migratoire · Pénurie Main-d&apos;Œuvre
        </p>
      </div>

      {/* 6 KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {[
          ["Total Entités", data.total_entities, "text-teal-400"],
          ["Alertes Critiques", data.critical_alerts, "text-red-400"],
          ["Niveau Élevé", (data.risk_distribution?.["élevé"] ?? 0), "text-blue-400"],
          ["Score Composite Moy.", `${data.avg_composite.toFixed(1)}`, "text-teal-300"],
          ["Index Démographique", `${data.avg_estimated_demographic_index.toFixed(2)}/10`, "text-amber-400"],
          ["Confiance Analyse", `${data.confidence_score}%`, "text-emerald-400"],
        ].map(([l, v, c]) => (
          <div key={String(l)} className="bg-slate-900 border border-teal-700/30 rounded-xl p-3 text-center">
            <div className={`text-xl font-bold ${c}`}>{v}</div>
            <div className="text-xs text-teal-300/40 mt-0.5 leading-tight">{l}</div>
          </div>
        ))}
      </div>

      {/* 4 Gauge Rings */}
      <div className="bg-slate-900 border border-teal-700/30 rounded-xl p-5">
        <div className="grid grid-cols-4 gap-4">
          <GaugeRing value={avgFertility} label="Déclin Natalité Moy." color="#ef4444" />
          <GaugeRing value={avgAging} label="Vieillissement Moy." color="#f97316" />
          <GaugeRing value={avgMigration} label="Pression Migratoire" color="#a855f7" />
          <GaugeRing value={avgLabor} label="Pénurie Travail Moy." color="#06b6d4" />
        </div>
      </div>

      {/* 4 Distribution Bars */}
      <div className="bg-slate-900 border border-teal-700/30 rounded-xl p-5 grid grid-cols-1 md:grid-cols-2 gap-5">
        <DistBar title="Distribution par Risque" counts={data.risk_distribution} colors={RISK_COLORS} />
        <DistBar title="Distribution par Pattern" counts={data.pattern_distribution} colors={PAT_COLORS} />
        <DistBar title="Entités Critiques vs Non-Critiques" counts={{ "critique": data.critical_alerts, "autres": data.total_entities - data.critical_alerts }} colors={{ critique: "#ef4444", autres: "#10b981" }} />
        <DistBar title="Sources de Données" counts={{ "ONU": 1, "Eurostat": 1, "OCDE": 1 }} colors={{ "ONU": "#06b6d4", "Eurostat": "#a855f7", "OCDE": "#f59e0b" }} />
      </div>

      {/* Filter Pills */}
      <div className="flex flex-wrap gap-2">
        {["all", "faible", "modéré", "élevé", "critique"].map(r => (
          <button key={r} onClick={() => setRiskFilter(r)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${riskFilter === r ? "bg-teal-900 border-teal-700 text-white" : "bg-slate-900 border-teal-700/30 text-teal-400/70 hover:text-white"}`}>
            {r}
          </button>
        ))}
        <span className="w-px h-5 self-center bg-teal-700/30" />
        {["all", ...patterns].map(p => (
          <button key={p} onClick={() => setPatFilter(p)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${patFilter === p ? "bg-amber-950 border-amber-700 text-white" : "bg-slate-900 border-teal-700/30 text-teal-400/70 hover:text-white"}`}>
            {p === "all" ? "Tous Patterns" : p}
          </button>
        ))}
      </div>

      {/* Entity Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {filtered.map(e => (
          <div key={e.id} onClick={() => setSelected(e)}
            className="bg-slate-900 border border-teal-700/30 rounded-xl p-4 cursor-pointer hover:border-teal-500 transition-colors">
            <div className="flex items-center justify-between mb-1">
              <span className="font-bold text-white text-sm">{e.id}</span>
              <span className="text-xs text-teal-400/60">{e.country}</span>
            </div>
            <div className="text-xs text-slate-400 mb-2 truncate">{e.name}</div>
            <div className="flex gap-1 mb-3 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[e.risk_level] || "bg-slate-700 text-slate-300"}`}>{e.risk_level}</span>
            </div>
            <div className="text-2xl font-black text-white mb-1">{e.composite_score.toFixed(1)}</div>
            <div className="text-xs text-teal-400/60 mb-2">{e.primary_pattern}</div>
            <div className="text-xs text-teal-400 font-medium mb-1">
              Natalité: {e.fertility_decline_score} · Âge: {e.aging_index}
            </div>
            <div className="text-xs text-slate-500 truncate">{e.key_signals[0]}</div>
          </div>
        ))}
      </div>
    </div>
  );
}
