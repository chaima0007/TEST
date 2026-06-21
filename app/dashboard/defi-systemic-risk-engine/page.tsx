"use client";
import { useEffect, useState } from "react";

// ── Types ──────────────────────────────────────────────────────────────────────

type DeFiEntity = {
  id: string;
  name: string;
  country: string;
  sector: string;
  composite_score: number;
  protocol_risk_score: number;
  liquidity_risk_score: number;
  contagion_risk_score: number;
  governance_risk_score: number;
  risk_level: string;
  primary_pattern: string;
  key_signals: string[];
  estimated_defi_index: number;
  last_updated: string;
  domain: string;
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
  entities: DeFiEntity[];
  avg_estimated_defi_index: number;
  sector_distribution?: Record<string, number>;
  country_distribution?: Record<string, number>;
};

type ApiResponse = {
  entities: DeFiEntity[];
  summary: Summary;
};

// ── GaugeRing (inline SVG) ────────────────────────────────────────────────────

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

// ── DistBar (inline) ──────────────────────────────────────────────────────────

function DistBar({
  title,
  counts,
  colors,
}: {
  title: string;
  counts: Record<string, number>;
  colors: Record<string, string>;
}) {
  const total = Object.values(counts).reduce((a, b) => a + b, 0) || 1;
  return (
    <div className="flex flex-col gap-1">
      <span className="text-xs text-slate-400 font-medium">{title}</span>
      <div className="flex h-3 rounded overflow-hidden gap-px">
        {Object.entries(counts).map(([k, v]) => (
          <div
            key={k}
            style={{ width: `${(v / total) * 100}%`, background: colors[k] || "#475569" }}
            title={`${k}: ${v}`}
          />
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

// ── Color maps ────────────────────────────────────────────────────────────────

const RISK_COLORS: Record<string, string> = {
  faible:   "#10b981",
  modéré:   "#f59e0b",
  élevé:    "#f97316",
  critique: "#ef4444",
};

const PATTERN_COLORS: Record<string, string> = {
  "Exploit Protocole Critique":  "#ef4444",
  "Crise Liquidité Systémique":  "#dc2626",
  "Contagion Inter-Protocoles":  "#f97316",
  "Attaque Gouvernance DAO":     "#7c3aed",
  "Dépeg Stablecoin Partiel":    "#f59e0b",
};

const SECTOR_COLORS: Record<string, string> = {
  "DEX / AMM":                   "#3b82f6",
  "Stablecoin Algorithmique":    "#ef4444",
  "Protocole Gouvernance":       "#7c3aed",
  "Bridge Inter-Chaînes":        "#f97316",
  "Yield Farming Levieré":       "#f59e0b",
  "Lending Protocol":            "#06b6d4",
  "Lending Régulé":              "#10b981",
  "DEX Mature":                  "#22c55e",
};

const COUNTRY_COLORS: Record<string, string> = {
  "Anonyme":                     "#64748b",
  "Corée du Sud":                "#ef4444",
  "Îles Caïmans":                "#7c3aed",
  "Singapour":                   "#3b82f6",
  "Îles Vierges Britanniques":   "#f97316",
  "Suisse":                      "#f59e0b",
  "Royaume-Uni":                 "#10b981",
  "USA":                         "#22c55e",
};

const RISK_BADGE: Record<string, string> = {
  faible:   "bg-emerald-900 text-emerald-300",
  modéré:   "bg-amber-900 text-amber-300",
  élevé:    "bg-orange-900 text-orange-300",
  critique: "bg-red-900 text-red-300",
};

const PATTERN_BADGE: Record<string, string> = {
  "Exploit Protocole Critique":  "bg-red-900 text-red-300",
  "Crise Liquidité Systémique":  "bg-rose-900 text-rose-300",
  "Contagion Inter-Protocoles":  "bg-orange-900 text-orange-300",
  "Attaque Gouvernance DAO":     "bg-purple-900 text-purple-300",
  "Dépeg Stablecoin Partiel":    "bg-amber-900 text-amber-300",
};

// ── DetailModal ───────────────────────────────────────────────────────────────

function DetailModal({ entity, onClose }: { entity: DeFiEntity; onClose: () => void }) {
  const [tab, setTab] = useState<"scores" | "signals" | "actions">("scores");

  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
    };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [onClose]);

  // Look up action from pattern
  const PATTERN_ACTIONS: Record<string, string> = {
    "Exploit Protocole Critique":  "Pause protocole immédiate et activation war room sécurité",
    "Crise Liquidité Systémique":  "Injection liquidité d'urgence et coordination market makers",
    "Contagion Inter-Protocoles":  "Isolation exposition contagion et audit dépendances croisées",
    "Attaque Gouvernance DAO":     "Veto proposition et révision mécanisme gouvernance",
    "Dépeg Stablecoin Partiel":    "Surveillance maintien ancrage et réserves collatéral vérifiées",
  };

  const PATTERN_SIGNALS: Record<string, string> = {
    "Exploit Protocole Critique":  "protocol_risk_score > 80",
    "Crise Liquidité Systémique":  "liquidity_risk_score > 75",
    "Contagion Inter-Protocoles":  "contagion_risk_score > 65",
    "Attaque Gouvernance DAO":     "governance_risk_score > 60",
    "Dépeg Stablecoin Partiel":    "liquidity_risk_score between 40-75",
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70" onClick={onClose}>
      <div
        className="bg-slate-900 border border-slate-700 rounded-xl w-full max-w-lg p-6 shadow-2xl"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="flex items-start justify-between mb-4">
          <div>
            <div className="flex items-center gap-2">
              <span className="text-xs text-slate-500 font-mono">{entity.id}</span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[entity.risk_level] || "bg-slate-700 text-slate-300"}`}>
                {entity.risk_level}
              </span>
            </div>
            <div className="text-lg font-bold text-white mt-0.5">{entity.name}</div>
            <div className="text-xs text-slate-400">{entity.sector} — {entity.country}</div>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl leading-none ml-4">✕</button>
        </div>

        {/* Tabs */}
        <div className="flex gap-2 mb-4">
          {(["scores", "signals", "actions"] as const).map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`px-3 py-1 rounded text-xs font-medium transition-colors ${
                tab === t
                  ? "bg-cyan-800 text-white"
                  : "bg-slate-800 text-slate-400 hover:text-white"
              }`}
            >
              {t === "scores" ? "Scores" : t === "signals" ? "Signaux" : "Actions"}
            </button>
          ))}
        </div>

        {/* Tab: Scores */}
        {tab === "scores" && (
          <div className="space-y-3">
            <div className="grid grid-cols-2 gap-3 text-sm">
              {[
                ["Risque Protocole",   entity.protocol_risk_score,   "#ef4444"],
                ["Risque Liquidité",   entity.liquidity_risk_score,   "#f97316"],
                ["Risque Contagion",   entity.contagion_risk_score,   "#f59e0b"],
                ["Risque Gouvernance", entity.governance_risk_score,  "#7c3aed"],
              ].map(([label, val, color]) => (
                <div key={String(label)} className="bg-slate-800 rounded-lg p-3">
                  <div className="text-slate-400 text-xs mb-1">{String(label)}</div>
                  <div className="text-white font-bold text-lg">{Number(val).toFixed(1)}</div>
                  <div className="h-1.5 rounded mt-1 bg-slate-700">
                    <div
                      className="h-1.5 rounded"
                      style={{
                        width: `${Math.min(Number(val), 100)}%`,
                        background: String(color),
                      }}
                    />
                  </div>
                </div>
              ))}
            </div>
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Score Composite (pondéré 0.30/0.25/0.25/0.20)</div>
              <div className="text-white font-bold text-2xl">{entity.composite_score.toFixed(2)}</div>
              <div className="h-2 rounded mt-2 bg-slate-700">
                <div
                  className="h-2 rounded"
                  style={{
                    width: `${Math.min(entity.composite_score, 100)}%`,
                    background: RISK_COLORS[entity.risk_level] || "#94a3b8",
                  }}
                />
              </div>
            </div>
            <div className="bg-slate-800 rounded-lg p-3 flex justify-between items-center">
              <div>
                <div className="text-slate-400 text-xs">Index DeFi Estimé</div>
                <div className="text-cyan-400 font-bold text-lg">{entity.estimated_defi_index.toFixed(2)} / 10</div>
              </div>
              <div className="text-right">
                <div className="text-slate-400 text-xs">Mis à jour</div>
                <div className="text-slate-300 text-sm">{entity.last_updated}</div>
              </div>
            </div>
          </div>
        )}

        {/* Tab: Signaux */}
        {tab === "signals" && (
          <div className="space-y-3">
            <div className={`px-3 py-2 rounded text-xs font-medium inline-block ${PATTERN_BADGE[entity.primary_pattern] || "bg-slate-700 text-slate-300"}`}>
              {entity.primary_pattern}
            </div>
            <div className="text-xs text-slate-500 mb-1">
              Condition: <span className="text-cyan-400 font-mono">{PATTERN_SIGNALS[entity.primary_pattern] || "—"}</span>
            </div>
            <div className="space-y-2">
              {entity.key_signals.map((signal, i) => (
                <div key={i} className="bg-slate-800 rounded-lg p-3 flex gap-2 items-start">
                  <span className="text-cyan-400 font-bold text-sm mt-0.5">{i + 1}.</span>
                  <span className="text-slate-200 text-sm">{signal}</span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Tab: Actions */}
        {tab === "actions" && (
          <div className="space-y-3 text-sm">
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Action Recommandée</div>
              <div className="text-white font-medium leading-relaxed">
                {PATTERN_ACTIONS[entity.primary_pattern] || "Surveillance continue"}
              </div>
            </div>
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Patron Détecté</div>
              <div className={`px-2 py-1 rounded text-xs font-medium inline-block ${PATTERN_BADGE[entity.primary_pattern] || "bg-slate-700 text-slate-300"}`}>
                {entity.primary_pattern}
              </div>
            </div>
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Secteur DeFi</div>
              <div className="text-white font-medium">{entity.sector}</div>
            </div>
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Juridiction</div>
              <div className="text-white font-medium">{entity.country}</div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

// ── Main Dashboard ────────────────────────────────────────────────────────────

export default function DeFiSystemicRiskDashboard() {
  const [data, setData] = useState<ApiResponse | null>(null);
  const [riskFilter, setRiskFilter] = useState<string>("all");
  const [patternFilter, setPatternFilter] = useState<string>("all");
  const [selected, setSelected] = useState<DeFiEntity | null>(null);

  useEffect(() => {
    fetch("/api/defi-systemic-risk-engine")
      .then((r) => r.json())
      .then(setData)
      .catch(console.error);
  }, []);

  if (!data) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center">
        <div className="text-cyan-400 text-lg animate-pulse">
          Chargement DeFi Systemic Risk Intelligence...
        </div>
      </div>
    );
  }

  const { entities, summary } = data;

  const filtered = entities.filter(
    (e) =>
      (riskFilter === "all" || e.risk_level === riskFilter) &&
      (patternFilter === "all" || e.primary_pattern === patternFilter)
  );

  // Avg sub-scores for gauge rings
  const n = entities.length || 1;
  const avgProtocol    = entities.reduce((a, e) => a + e.protocol_risk_score, 0) / n;
  const avgLiquidity   = entities.reduce((a, e) => a + e.liquidity_risk_score, 0) / n;
  const avgContagion   = entities.reduce((a, e) => a + e.contagion_risk_score, 0) / n;
  const avgGovernance  = entities.reduce((a, e) => a + e.governance_risk_score, 0) / n;

  // TVL risk estimation (crude sum based on critique entities × $450M for demo)
  const critiqueCount = summary.risk_distribution["critique"] || 0;
  const tvlAtRisk = critiqueCount > 0 ? `$${(critiqueCount * 0.45 + 1.2).toFixed(1)}B` : "$0";

  const allPatterns = [
    "Exploit Protocole Critique",
    "Crise Liquidité Systémique",
    "Contagion Inter-Protocoles",
    "Attaque Gouvernance DAO",
    "Dépeg Stablecoin Partiel",
  ];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {selected && <DetailModal entity={selected} onClose={() => setSelected(null)} />}

      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-white">DeFi Systemic Risk Intelligence</h1>
        <p className="text-slate-400 text-sm mt-1">
          Surveillance des risques systémiques dans la finance décentralisée
        </p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {[
          ["Total Protocoles",      summary.total_entities,                           "text-cyan-400"],
          ["Alertes Critiques",     summary.critical_alerts,                          "text-red-500"],
          ["Score Risque Moyen",    summary.avg_composite.toFixed(1),                 "text-slate-300"],
          ["Index DeFi Moyen",      `${summary.avg_estimated_defi_index.toFixed(2)}/10`, "text-cyan-400"],
          ["TVL à Risque",          tvlAtRisk,                                        "text-rose-400"],
          ["Sources Analysées",     summary.data_sources.length,                      "text-emerald-400"],
        ].map(([label, value, color]) => (
          <div
            key={String(label)}
            className="bg-slate-900 border border-slate-800 rounded-xl p-3 text-center"
          >
            <div className={`text-xl font-bold ${color}`}>{value}</div>
            <div className="text-xs text-slate-500 mt-0.5">{label}</div>
          </div>
        ))}
      </div>

      {/* Gauge Rings */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
        <div className="text-xs text-slate-500 font-medium mb-4 uppercase tracking-wider">
          Scores Moyens par Dimension
        </div>
        <div className="grid grid-cols-4 gap-4">
          <GaugeRing value={avgProtocol}   label="Protocole"   color="#ef4444" />
          <GaugeRing value={avgLiquidity}  label="Liquidité"   color="#f97316" />
          <GaugeRing value={avgContagion}  label="Contagion"   color="#f59e0b" />
          <GaugeRing value={avgGovernance} label="Gouvernance" color="#7c3aed" />
        </div>
      </div>

      {/* Distribution Bars */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 grid grid-cols-1 md:grid-cols-2 gap-6">
        <DistBar
          title="Distribution des Risques"
          counts={summary.risk_distribution}
          colors={RISK_COLORS}
        />
        <DistBar
          title="Distribution des Patrons"
          counts={summary.pattern_distribution}
          colors={PATTERN_COLORS}
        />
        <DistBar
          title="Distribution par Secteur"
          counts={summary.sector_distribution || {}}
          colors={SECTOR_COLORS}
        />
        <DistBar
          title="Distribution par Juridiction"
          counts={summary.country_distribution || {}}
          colors={COUNTRY_COLORS}
        />
      </div>

      {/* Filter Pills */}
      <div className="flex flex-wrap gap-2">
        {["all", "faible", "modéré", "élevé", "critique"].map((r) => (
          <button
            key={r}
            onClick={() => setRiskFilter(r)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${
              riskFilter === r
                ? "bg-cyan-800 border-cyan-700 text-white"
                : "bg-slate-900 border-slate-700 text-slate-400 hover:text-white"
            }`}
          >
            {r === "all" ? "Tous" : r}
          </button>
        ))}
        <span className="w-px h-5 self-center bg-slate-700" />
        <button
          onClick={() => setPatternFilter("all")}
          className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${
            patternFilter === "all"
              ? "bg-cyan-800 border-cyan-700 text-white"
              : "bg-slate-900 border-slate-700 text-slate-400 hover:text-white"
          }`}
        >
          Tous patrons
        </button>
        {allPatterns.map((p) => (
          <button
            key={p}
            onClick={() => setPatternFilter(p)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${
              patternFilter === p
                ? "bg-cyan-800 border-cyan-700 text-white"
                : "bg-slate-900 border-slate-700 text-slate-400 hover:text-white hover:border-cyan-700"
            }`}
          >
            {p}
          </button>
        ))}
      </div>

      {/* Entity Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {filtered.map((e) => (
          <div
            key={e.id}
            onClick={() => setSelected(e)}
            className="bg-slate-900 border border-slate-800 rounded-xl p-4 cursor-pointer hover:border-cyan-700 transition-colors"
          >
            {/* Card header */}
            <div className="flex items-center justify-between mb-1">
              <span className="text-xs text-slate-500 font-mono">{e.id}</span>
              <span className="text-xs text-slate-400">{e.country}</span>
            </div>
            <div className="font-bold text-white mb-0.5 leading-tight">{e.name}</div>
            <div className="text-xs text-cyan-400 mb-2">{e.sector}</div>

            {/* Badges */}
            <div className="flex gap-1 mb-3 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[e.risk_level] || "bg-slate-700 text-slate-300"}`}>
                {e.risk_level}
              </span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${PATTERN_BADGE[e.primary_pattern] || "bg-slate-700 text-slate-300"}`}>
                {e.primary_pattern}
              </span>
            </div>

            {/* Composite score */}
            <div className="text-2xl font-black text-white mb-1">{e.composite_score.toFixed(1)}</div>
            <div className="h-1.5 rounded bg-slate-700 mb-3">
              <div
                className="h-1.5 rounded"
                style={{
                  width: `${Math.min(e.composite_score, 100)}%`,
                  background: RISK_COLORS[e.risk_level] || "#94a3b8",
                }}
              />
            </div>

            {/* Key signals */}
            <div className="space-y-1">
              {e.key_signals.map((sig, i) => (
                <div key={i} className="text-xs text-slate-400 leading-snug flex gap-1">
                  <span className="text-cyan-500 shrink-0">›</span>
                  <span>{sig}</span>
                </div>
              ))}
            </div>

            {/* Footer */}
            <div className="mt-3 pt-3 border-t border-slate-800 flex justify-between items-center">
              <span className="text-xs text-slate-500">Index DeFi</span>
              <span className="text-xs text-cyan-400 font-bold">{e.estimated_defi_index.toFixed(2)} / 10</span>
            </div>
          </div>
        ))}
      </div>

      {/* Top risk summary */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
        <div className="text-xs text-slate-500 font-medium mb-3 uppercase tracking-wider">
          Top 3 Entités à Risque
        </div>
        <div className="flex flex-wrap gap-3">
          {summary.top_risk_entities.map((name, i) => (
            <div key={name} className="flex items-center gap-2 bg-slate-800 rounded-lg px-3 py-2">
              <span className="text-red-500 font-bold text-sm">#{i + 1}</span>
              <span className="text-white text-sm font-medium">{name}</span>
            </div>
          ))}
        </div>
        <div className="mt-3 text-xs text-slate-600">
          Dernière analyse: {summary.last_analysis} — Confiance: {(summary.confidence_score * 100).toFixed(0)}% —
          Version {summary.engine_version} — {summary.data_sources.length} sources
        </div>
      </div>
    </div>
  );
}
