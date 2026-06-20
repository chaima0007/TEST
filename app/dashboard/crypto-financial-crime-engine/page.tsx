"use client";
import { useEffect, useState } from "react";

type CryptoEntity = {
  entity_id: string;
  name: string;
  country: string;
  sector: string;
  composite_score: number;
  laundering_risk_score: number;
  sanctions_exposure_score: number;
  darknet_flow_score: number;
  traceability_gap_score: number;
  risk_level: string;
  primary_pattern: string;
  key_signals: string[];
  estimated_crypto_index: number;
  last_updated: string;
  watchlist_flag: boolean;
};

type Summary = {
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
  entities: CryptoEntity[];
  avg_estimated_crypto_index: number;
};

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

const RISK_COLORS: Record<string, string> = {
  faible: "#10b981",
  "modéré": "#f59e0b",
  "élevé": "#f97316",
  critique: "#ef4444",
};

const PATTERN_COLORS: Record<string, string> = {
  "Blanchiment Crypto Structuré": "#ef4444",
  "Transaction Entité Sanctionnée": "#a855f7",
  "Flux Marché Darknet": "#f97316",
  "Opacité Mixer Crypto": "#06b6d4",
  "Paiement Ransomware Détecté": "#eab308",
};

const SECTOR_COLORS: Record<string, string> = {
  "Exchange Crypto": "#ef4444",
  "OTC Crypto": "#f97316",
  "DEX Anonyme": "#a855f7",
  "Mixing Service": "#06b6d4",
  "Portefeuille Crypto": "#eab308",
  "Trading Crypto": "#f59e0b",
  "Exchange Régulé": "#10b981",
};

const COUNTRY_COLORS: Record<string, string> = {
  Russie: "#ef4444",
  "Émirats Arabes Unis": "#f97316",
  Anonyme: "#a855f7",
  "Pays-Bas": "#06b6d4",
  Ukraine: "#eab308",
  Malte: "#f59e0b",
  USA: "#10b981",
  Irlande: "#22d3ee",
};

const RISK_BADGE: Record<string, string> = {
  faible: "bg-emerald-900 text-emerald-300",
  "modéré": "bg-amber-900 text-amber-300",
  "élevé": "bg-orange-900 text-orange-300",
  critique: "bg-red-900 text-red-300",
};

const PATTERN_ACTIONS: Record<string, string> = {
  "Blanchiment Crypto Structuré": "Signalement immédiat TRACFIN et gel des avoirs crypto",
  "Transaction Entité Sanctionnée": "Blocage transaction et notification autorités OFAC/UE",
  "Flux Marché Darknet": "Analyse blockchain forensique et coopération Europol",
  "Opacité Mixer Crypto": "Due diligence renforcée et rapport AML automatisé",
  "Paiement Ransomware Détecté": "Identification portefeuille et signalement CERT/ANSSI",
};

function DetailModal({ entity, onClose }: { entity: CryptoEntity; onClose: () => void }) {
  const [tab, setTab] = useState<"scores" | "signaux" | "actions">("scores");

  useEffect(() => {
    const h = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", h);
    return () => window.removeEventListener("keydown", h);
  }, [onClose]);

  const subScores = [
    { label: "Risque Blanchiment", value: entity.laundering_risk_score, color: "#ef4444" },
    { label: "Exposition Sanctions", value: entity.sanctions_exposure_score, color: "#a855f7" },
    { label: "Flux Darknet", value: entity.darknet_flow_score, color: "#f97316" },
    { label: "Opacité Traçabilité", value: entity.traceability_gap_score, color: "#06b6d4" },
  ];

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/75" onClick={onClose}>
      <div
        className="bg-slate-900 border border-cyan-500/30 rounded-xl w-full max-w-lg p-6 shadow-2xl"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="flex items-center justify-between mb-4">
          <div>
            <span className="text-lg font-bold text-white">{entity.name}</span>
            <span className="ml-2 text-cyan-400 text-xs">{entity.entity_id}</span>
            <span className="ml-2 text-slate-400 text-xs">{entity.country}</span>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl leading-none">
            ✕
          </button>
        </div>

        <div className="flex gap-2 mb-4">
          {(["scores", "signaux", "actions"] as const).map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`px-3 py-1 rounded text-xs font-medium transition-colors ${
                tab === t
                  ? "bg-cyan-700 text-white"
                  : "bg-slate-800 text-slate-400 hover:text-white"
              }`}
            >
              {t.charAt(0).toUpperCase() + t.slice(1)}
            </button>
          ))}
        </div>

        {tab === "scores" && (
          <div className="space-y-3">
            {subScores.map(({ label, value, color }) => (
              <div key={label} className="bg-slate-800 border border-cyan-500/20 rounded-lg p-3">
                <div className="flex justify-between items-center mb-1">
                  <span className="text-slate-400 text-xs">{label}</span>
                  <span className="text-white font-bold text-sm">{value.toFixed(1)}</span>
                </div>
                <div className="h-2 rounded bg-slate-700">
                  <div
                    className="h-2 rounded"
                    style={{ width: `${Math.min(value, 100)}%`, background: color }}
                  />
                </div>
              </div>
            ))}
            <div className="bg-slate-800 border border-cyan-500/20 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Score Composite Crime Crypto</div>
              <div className="text-white font-bold text-2xl">{entity.composite_score.toFixed(2)}</div>
              <div className="text-slate-500 text-xs mt-1">
                Index Crypto: {entity.estimated_crypto_index.toFixed(2)}/10
              </div>
            </div>
          </div>
        )}

        {tab === "signaux" && (
          <div className="space-y-2">
            <div className="text-xs text-slate-500 mb-3 font-medium">Signaux Détectés</div>
            {entity.key_signals.map((signal, i) => (
              <div
                key={i}
                className="bg-slate-800 border border-cyan-500/20 rounded-lg p-3 flex items-start gap-2"
              >
                <span className="text-cyan-400 text-xs mt-0.5 shrink-0">{i + 1}.</span>
                <span className="text-slate-200 text-sm">{signal}</span>
              </div>
            ))}
            <div className="mt-3 flex gap-2 flex-wrap">
              <span
                className={`px-2 py-0.5 rounded text-xs font-medium ${
                  RISK_BADGE[entity.risk_level] || "bg-slate-700 text-slate-300"
                }`}
              >
                {entity.risk_level}
              </span>
              <span className="px-2 py-0.5 rounded text-xs font-medium bg-slate-700 text-cyan-300">
                {entity.primary_pattern}
              </span>
              <span className="px-2 py-0.5 rounded text-xs font-medium bg-slate-700 text-slate-300">
                {entity.sector}
              </span>
            </div>
          </div>
        )}

        {tab === "actions" && (
          <div className="space-y-3 text-sm">
            <div className="bg-slate-800 border border-cyan-500/20 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Action Recommandée</div>
              <div className="text-white font-medium">
                {PATTERN_ACTIONS[entity.primary_pattern] || "Surveillance continue"}
              </div>
            </div>
            <div className="bg-slate-800 border border-cyan-500/20 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Patron Crime Détecté</div>
              <div
                className="font-medium"
                style={{ color: PATTERN_COLORS[entity.primary_pattern] || "#94a3b8" }}
              >
                {entity.primary_pattern}
              </div>
            </div>
            <div className="bg-slate-800 border border-cyan-500/20 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Niveau de Risque</div>
              <span
                className={`px-2 py-0.5 rounded text-xs font-medium ${
                  RISK_BADGE[entity.risk_level] || "bg-slate-700 text-slate-300"
                }`}
              >
                {entity.risk_level}
              </span>
            </div>
            <div className="bg-slate-800 border border-cyan-500/20 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Dernière Mise à Jour</div>
              <div className="text-slate-300 text-sm">{entity.last_updated}</div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function CryptoFinancialCrimeDashboard() {
  const [data, setData] = useState<{ entities: CryptoEntity[]; summary: Summary } | null>(null);
  const [riskFilter, setRisk] = useState<string>("all");
  const [patternFilter, setPattern] = useState<string>("all");
  const [selected, setSelected] = useState<CryptoEntity | null>(null);

  useEffect(() => {
    fetch("/api/crypto-financial-crime-engine")
      .then((r) => r.json())
      .then(setData)
      .catch(console.error);
  }, []);

  if (!data) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center">
        <div className="text-cyan-400 text-lg animate-pulse">
          Initialisation du Moteur Crime Financier Crypto...
        </div>
      </div>
    );
  }

  const { entities, summary } = data;

  const patterns = ["all", ...Array.from(new Set(entities.map((e) => e.primary_pattern)))];

  const filtered = entities.filter(
    (e) =>
      (riskFilter === "all" || e.risk_level === riskFilter) &&
      (patternFilter === "all" || e.primary_pattern === patternFilter)
  );

  const avgLaundering = entities.reduce((s, e) => s + e.laundering_risk_score, 0) / (entities.length || 1);
  const avgSanctions = entities.reduce((s, e) => s + e.sanctions_exposure_score, 0) / (entities.length || 1);
  const avgDarknet = entities.reduce((s, e) => s + e.darknet_flow_score, 0) / (entities.length || 1);
  const avgTraceability = entities.reduce((s, e) => s + e.traceability_gap_score, 0) / (entities.length || 1);

  const sectorCounts: Record<string, number> = {};
  const countryCounts: Record<string, number> = {};
  for (const e of entities) {
    sectorCounts[e.sector] = (sectorCounts[e.sector] || 0) + 1;
    countryCounts[e.country] = (countryCounts[e.country] || 0) + 1;
  }

  const sanctionedCount = entities.filter((e) => e.sanctions_exposure_score > 75).length;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-300 p-6 space-y-6">
      {selected && <DetailModal entity={selected} onClose={() => setSelected(null)} />}

      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-cyan-400">
          Crypto Financial Crime Intelligence
        </h1>
        <p className="text-slate-400 text-sm mt-1">
          Surveillance des crimes financiers liés aux crypto-actifs
        </p>
        <p className="text-slate-500 text-xs mt-0.5">
          Caelum Partners — v{summary.engine_version} — Confiance: {(summary.confidence_score * 100).toFixed(0)}%
        </p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {[
          ["Total Entités", summary.total_entities, "text-slate-300"],
          ["Alertes Critiques", summary.critical_alerts, "text-red-400"],
          ["Score Crime Moyen", summary.avg_composite.toFixed(1), "text-amber-400"],
          ["Index Crypto Moyen", summary.avg_estimated_crypto_index.toFixed(2) + "/10", "text-cyan-400"],
          ["Entités Sanctionnées", sanctionedCount, "text-purple-400"],
          ["Volume Analysé", entities.length + " entités", "text-emerald-400"],
        ].map(([l, v, c]) => (
          <div key={String(l)} className="bg-slate-900 border border-cyan-500/30 rounded-xl p-3 text-center">
            <div className={`text-xl font-bold ${c}`}>{v}</div>
            <div className="text-xs text-slate-500 mt-0.5 leading-tight">{l}</div>
          </div>
        ))}
      </div>

      {/* Gauge Rings */}
      <div className="bg-slate-900 border border-cyan-500/30 rounded-xl p-5">
        <p className="text-xs text-slate-500 mb-4 font-medium">
          Scores Moyens par Dimension Crime Crypto
        </p>
        <div className="grid grid-cols-4 gap-4">
          <GaugeRing value={avgLaundering}   label="Risque Blanchiment"  color="#ef4444" />
          <GaugeRing value={avgSanctions}    label="Exposition Sanctions" color="#a855f7" />
          <GaugeRing value={avgDarknet}      label="Flux Darknet"         color="#f97316" />
          <GaugeRing value={avgTraceability} label="Opacité Traçabilité"  color="#06b6d4" />
        </div>
      </div>

      {/* Distribution Bars */}
      <div className="bg-slate-900 border border-cyan-500/30 rounded-xl p-5 grid grid-cols-1 md:grid-cols-2 gap-5">
        <DistBar title="Niveau de Risque"        counts={summary.risk_distribution}    colors={RISK_COLORS} />
        <DistBar title="Patron de Crime Détecté"  counts={summary.pattern_distribution}  colors={PATTERN_COLORS} />
        <DistBar title="Distribution Secteur"     counts={sectorCounts}                  colors={SECTOR_COLORS} />
        <DistBar title="Distribution Pays"        counts={countryCounts}                  colors={COUNTRY_COLORS} />
      </div>

      {/* Filter Pills */}
      <div className="flex flex-wrap gap-2">
        {["all", "faible", "modéré", "élevé", "critique"].map((r) => (
          <button
            key={r}
            onClick={() => setRisk(r)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${
              riskFilter === r
                ? "bg-cyan-700 border-cyan-500 text-white"
                : "bg-slate-900 border-cyan-500/30 text-slate-400 hover:text-white"
            }`}
          >
            {r === "all" ? "Tous risques" : r}
          </button>
        ))}
        <span className="w-px h-5 self-center bg-cyan-500/30" />
        {patterns.map((p) => (
          <button
            key={p}
            onClick={() => setPattern(p)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${
              patternFilter === p
                ? "bg-slate-700 border-slate-500 text-white"
                : "bg-slate-900 border-cyan-500/30 text-slate-400 hover:text-white"
            }`}
          >
            {p === "all" ? "Tous patrons" : p}
          </button>
        ))}
      </div>

      {/* Entity Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {filtered.map((e) => (
          <div
            key={e.entity_id}
            onClick={() => setSelected(e)}
            className="bg-slate-900 border border-slate-800 rounded-xl p-4 cursor-pointer hover:border-cyan-500/50 transition-colors"
          >
            <div className="flex items-center justify-between mb-1">
              <span className="font-bold text-white text-sm">{e.name}</span>
              <span className="text-xs text-slate-400">{e.entity_id}</span>
            </div>
            <div className="text-xs text-cyan-400 mb-1">{e.country} — {e.sector}</div>
            <div className="flex gap-1 mb-3 flex-wrap">
              <span
                className={`px-2 py-0.5 rounded text-xs font-medium ${
                  RISK_BADGE[e.risk_level] || "bg-slate-700 text-slate-300"
                }`}
              >
                {e.risk_level}
              </span>
            </div>
            <div className="text-2xl font-black text-white mb-1">{e.composite_score.toFixed(1)}</div>
            <div
              className="text-xs font-medium mb-2"
              style={{ color: PATTERN_COLORS[e.primary_pattern] || "#94a3b8" }}
            >
              {e.primary_pattern}
            </div>
            <div className="space-y-1">
              {e.key_signals.map((sig, i) => (
                <div key={i} className="text-xs text-slate-400 truncate">
                  <span className="text-cyan-500">›</span> {sig}
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>

      {/* Data Sources Footer */}
      <div className="bg-slate-900 border border-cyan-500/20 rounded-xl p-4">
        <p className="text-xs text-slate-500 font-medium mb-2">Sources de Données</p>
        <div className="flex flex-wrap gap-2">
          {summary.data_sources.map((src) => (
            <span key={src} className="px-2 py-0.5 rounded bg-slate-800 text-xs text-slate-400">
              {src}
            </span>
          ))}
        </div>
      </div>
    </div>
  );
}
