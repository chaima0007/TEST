"use client";

import { useEffect, useState } from "react";

interface SyntheticPortfolio {
  portfolio_id: string;
  asset_class: string;
  region: string;
  liquidation_risk: string;
  liquidation_pattern: string;
  liquidation_severity: string;
  recommended_action: string;
  collateral_score: number;
  protocol_score: number;
  liquidity_score: number;
  systemic_score: number;
  liquidation_composite: number;
  is_liquidation_imminent: boolean;
  requires_collateral_top_up: boolean;
  estimated_liquidation_risk_index: number;
  liquidation_signal: string;
}

interface Summary {
  total: number;
  risk_counts: Record<string, number>;
  pattern_counts: Record<string, number>;
  severity_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_liquidation_composite: number;
  liquidation_imminent_count: number;
  collateral_top_up_count: number;
  avg_collateral_score: number;
  avg_protocol_score: number;
  avg_liquidity_score: number;
  avg_systemic_score: number;
  avg_estimated_liquidation_risk_index: number;
}

const RISK_COLORS: Record<string, string> = {
  low:      "text-emerald-400",
  moderate: "text-amber-400",
  high:     "text-orange-400",
  critical: "text-red-400",
};
const RISK_BG: Record<string, string> = {
  low:      "bg-emerald-400/10 border-emerald-400/30",
  moderate: "bg-amber-400/10 border-amber-400/30",
  high:     "bg-orange-400/10 border-orange-400/30",
  critical: "bg-red-400/10 border-red-400/30",
};
const SEV_COLORS: Record<string, string> = {
  secured:    "bg-emerald-500",
  monitored:  "bg-amber-500",
  at_risk:    "bg-orange-500",
  liquidating: "bg-red-500",
};
const PATTERN_LABELS: Record<string, string> = {
  none:                "Aucun",
  collateral_cascade:  "Cascade Collatéral",
  oracle_attack:       "Attaque Oracle",
  liquidity_crunch:    "Crise Liquidité",
  protocol_exploit:    "Exploit Protocole",
  peg_destabilization: "Déstabilisation Peg",
};
const ACTION_LABELS: Record<string, string> = {
  no_action:               "Aucune Action",
  defi_monitoring:         "Surveillance DeFi",
  risk_rebalancing:        "Rééquilibrage Risque",
  oracle_diversification:  "Diversification Oracle",
  liquidity_reinforcement: "Renforcement Liquidité",
  emergency_deleveraging:  "Désendettement d'Urgence",
  collateral_injection:    "Injection Collatéral",
  protocol_pause:          "Pause Protocole",
};
const ASSET_LABELS: Record<string, string> = {
  synthetic_equity:           "Equity Synthétique",
  tokenized_debt:             "Dette Tokenisée",
  collateralized_derivative:  "Dérivé Collatéralisé",
  liquidity_pool:             "Pool de Liquidité",
  structured_product:         "Produit Structuré",
  algorithmic_stablecoin:     "Stablecoin Algorithmique",
  yield_vault:                "Vault de Rendement",
  cross_chain_bridge:         "Bridge Cross-Chain",
};

function ScoreBar({ label, value, color = "bg-orange-500" }: { label: string; value: number; color?: string }) {
  return (
    <div>
      <div className="flex justify-between text-xs mb-1">
        <span className="text-slate-400">{label}</span>
        <span className="text-slate-200 font-mono">{value.toFixed(1)}</span>
      </div>
      <div className="h-1.5 rounded-full bg-slate-800">
        <div className={`h-1.5 rounded-full ${color}`} style={{ width: `${Math.min(value, 100)}%` }} />
      </div>
    </div>
  );
}

function GaugeRing({ label, value, color }: { label: string; value: number; color: string }) {
  const r = 36;
  const circ = 2 * Math.PI * r;
  const fill = (value / 100) * circ;
  return (
    <div className="flex flex-col items-center gap-2">
      <svg viewBox="0 0 88 88" className="w-20 h-20">
        <circle cx="44" cy="44" r={r} fill="none" stroke="#1e293b" strokeWidth="8" />
        <circle
          cx="44" cy="44" r={r} fill="none"
          stroke={color} strokeWidth="8"
          strokeDasharray={`${fill} ${circ}`}
          strokeLinecap="round"
          transform="rotate(-90 44 44)"
        />
        <text x="44" y="49" textAnchor="middle" fontSize="14" fontWeight="700" fill={color}>
          {value.toFixed(0)}
        </text>
      </svg>
      <span className="text-xs text-slate-400 text-center leading-tight">{label}</span>
    </div>
  );
}

function PortfolioRing({ composite }: { composite: number }) {
  const r = 36;
  const circ = 2 * Math.PI * r;
  const fill = (composite / 100) * circ;
  const color = composite >= 60 ? "#f87171" : composite >= 40 ? "#fb923c" : composite >= 20 ? "#fbbf24" : "#34d399";
  return (
    <svg viewBox="0 0 88 88" className="w-20 h-20">
      <circle cx="44" cy="44" r={r} fill="none" stroke="#1e293b" strokeWidth="8" />
      <circle
        cx="44" cy="44" r={r} fill="none"
        stroke={color} strokeWidth="8"
        strokeDasharray={`${fill} ${circ}`}
        strokeLinecap="round"
        transform="rotate(-90 44 44)"
      />
      <text x="44" y="49" textAnchor="middle" fontSize="14" fontWeight="700" fill={color}>
        {composite.toFixed(0)}
      </text>
    </svg>
  );
}

function DistBar({ title, counts, colors, total }: { title: string; counts: Record<string,number>; colors: Record<string,string>; total: number }) {
  return (
    <div className="bg-slate-900 border border-red-500/30 rounded-xl p-5">
      <h2 className="text-sm font-semibold text-slate-300 uppercase tracking-widest mb-4">{title}</h2>
      <div className="space-y-2">
        {Object.entries(counts).sort((a, b) => b[1] - a[1]).map(([key, count]) => (
          <div key={key} className="flex items-center gap-3">
            <span className="text-xs text-slate-400 w-36 truncate">{colors[key] ?? key}</span>
            <div className="flex-1 h-2 bg-slate-800 rounded-full">
              <div
                className="h-2 rounded-full bg-orange-500"
                style={{ width: total > 0 ? `${(count / total) * 100}%` : "0%" }}
              />
            </div>
            <span className="text-xs font-mono text-slate-300 w-4 text-right">{count}</span>
          </div>
        ))}
      </div>
    </div>
  );
}

function DetailModal({ port, onClose }: { port: SyntheticPortfolio; onClose: () => void }) {
  const [tab, setTab] = useState<"scores" | "signal" | "action">("scores");
  useEffect(() => {
    const handler = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [onClose]);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm" onClick={onClose}>
      <div className="relative bg-slate-900 border border-red-500/30 rounded-2xl shadow-2xl w-full max-w-lg mx-4 overflow-hidden" onClick={(e) => e.stopPropagation()}>
        <div className="flex items-center justify-between px-6 py-4 border-b border-slate-800">
          <div>
            <p className="text-xs text-slate-500 uppercase tracking-widest">Portefeuille Synthétique</p>
            <h2 className="text-lg font-bold text-slate-100">{port.portfolio_id}</h2>
            <p className="text-xs text-slate-400">{port.region} · {ASSET_LABELS[port.asset_class] ?? port.asset_class}</p>
          </div>
          <div className="flex flex-col items-end gap-1">
            <span className={`text-xs font-semibold px-2 py-0.5 rounded-full border ${RISK_BG[port.liquidation_risk]}`}>
              <span className={RISK_COLORS[port.liquidation_risk]}>{port.liquidation_risk.toUpperCase()}</span>
            </span>
            <span className={`text-xs px-2 py-0.5 rounded-full text-white ${SEV_COLORS[port.liquidation_severity]}`}>
              {port.liquidation_severity}
            </span>
            <button onClick={onClose} className="text-slate-500 hover:text-slate-200 text-xl leading-none mt-1">×</button>
          </div>
        </div>

        <div className="flex border-b border-slate-800">
          {(["scores", "signal", "action"] as const).map((t) => (
            <button key={t} onClick={() => setTab(t)}
              className={`flex-1 py-2 text-xs font-semibold uppercase tracking-widest transition-colors ${tab === t ? "text-orange-400 border-b-2 border-orange-400" : "text-slate-500 hover:text-slate-300"}`}>
              {t === "scores" ? "Scores" : t === "signal" ? "Signal" : "Action"}
            </button>
          ))}
        </div>

        <div className="px-6 py-5 space-y-4">
          {tab === "scores" && (
            <div className="space-y-3">
              <ScoreBar label="Santé Collatéral" value={port.collateral_score} color="bg-red-500" />
              <ScoreBar label="Sécurité Protocole" value={port.protocol_score} color="bg-orange-500" />
              <ScoreBar label="Liquidité DeFi" value={port.liquidity_score} color="bg-amber-500" />
              <ScoreBar label="Risque Systémique" value={port.systemic_score} color="bg-rose-500" />
              <div className="pt-2 border-t border-slate-800">
                <ScoreBar label="Composite Liquidation" value={port.liquidation_composite} color="bg-orange-400" />
              </div>
              <div className="grid grid-cols-2 gap-3 pt-1">
                <div className="bg-slate-800 rounded-lg p-3">
                  <p className="text-slate-500 text-xs mb-1">Risque Index</p>
                  <p className="text-orange-400 font-bold">{port.estimated_liquidation_risk_index.toFixed(2)}/10</p>
                </div>
                <div className="bg-slate-800 rounded-lg p-3">
                  <p className="text-slate-500 text-xs mb-1">Top-up Requis</p>
                  <p className={`font-bold ${port.requires_collateral_top_up ? "text-red-400" : "text-emerald-400"}`}>
                    {port.requires_collateral_top_up ? "Oui" : "Non"}
                  </p>
                </div>
              </div>
            </div>
          )}
          {tab === "signal" && (
            <div className="space-y-4">
              <div className="flex items-center justify-center py-2">
                <PortfolioRing composite={port.liquidation_composite} />
              </div>
              <p className="text-sm text-slate-300 italic text-center">&ldquo;{port.liquidation_signal}&rdquo;</p>
              <div className="grid grid-cols-2 gap-3 text-xs">
                <div className="bg-slate-800 rounded-lg p-3">
                  <p className="text-slate-500 mb-1">Patron détecté</p>
                  <p className="text-orange-300 font-semibold">{PATTERN_LABELS[port.liquidation_pattern] ?? port.liquidation_pattern}</p>
                </div>
                <div className="bg-slate-800 rounded-lg p-3">
                  <p className="text-slate-500 mb-1">Sévérité</p>
                  <p className="text-slate-100 font-semibold capitalize">{port.liquidation_severity}</p>
                </div>
                <div className="bg-slate-800 rounded-lg p-3">
                  <p className="text-slate-500 mb-1">Liquidation imminente</p>
                  <p className={`font-bold ${port.is_liquidation_imminent ? "text-red-400" : "text-emerald-400"}`}>
                    {port.is_liquidation_imminent ? "Oui" : "Non"}
                  </p>
                </div>
                <div className="bg-slate-800 rounded-lg p-3">
                  <p className="text-slate-500 mb-1">Composite</p>
                  <p className="text-slate-100 font-bold text-base">{port.liquidation_composite.toFixed(1)}</p>
                </div>
              </div>
            </div>
          )}
          {tab === "action" && (
            <div className="space-y-3 text-sm">
              <div className="bg-slate-800 rounded-lg p-4">
                <p className="text-slate-500 text-xs mb-1">Action Recommandée</p>
                <p className="text-orange-300 font-semibold">{ACTION_LABELS[port.recommended_action] ?? port.recommended_action}</p>
              </div>
              <div className="bg-slate-800 rounded-lg p-4">
                <p className="text-slate-500 text-xs mb-1">Patron de Liquidation</p>
                <p className="text-slate-200">{PATTERN_LABELS[port.liquidation_pattern] ?? port.liquidation_pattern}</p>
              </div>
              <div className="bg-slate-800 rounded-lg p-4">
                <p className="text-slate-500 text-xs mb-1">Classe d&apos;Actif</p>
                <p className="text-slate-200">{ASSET_LABELS[port.asset_class] ?? port.asset_class}</p>
              </div>
              <div className="bg-slate-800 rounded-lg p-4">
                <p className="text-slate-500 text-xs mb-2">Alertes</p>
                <div className="flex flex-wrap gap-2">
                  {port.is_liquidation_imminent && (
                    <span className="text-xs px-2 py-0.5 rounded-full bg-red-400/10 border border-red-400/30 text-red-400">Liquidation Imminente</span>
                  )}
                  {port.requires_collateral_top_up && (
                    <span className="text-xs px-2 py-0.5 rounded-full bg-orange-400/10 border border-orange-400/30 text-orange-400">Top-up Collatéral</span>
                  )}
                  {!port.is_liquidation_imminent && !port.requires_collateral_top_up && (
                    <span className="text-xs text-slate-500">Aucune alerte critique</span>
                  )}
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default function SyntheticAssetLiquidationPage() {
  const [data, setData] = useState<{ portfolios: SyntheticPortfolio[]; summary: Summary } | null>(null);
  const [selected, setSelected] = useState<SyntheticPortfolio | null>(null);
  const [riskFilter, setRiskFilter] = useState("all");
  const [patternFilter, setPatternFilter] = useState("all");

  useEffect(() => {
    const params = new URLSearchParams();
    if (riskFilter !== "all") params.set("risk", riskFilter);
    if (patternFilter !== "all") params.set("pattern", patternFilter);
    fetch(`/api/synthetic-asset-liquidation-engine?${params}`)
      .then((r) => r.json())
      .then(setData);
  }, [riskFilter, patternFilter]);

  const summary = data?.summary;
  const portfolios = (data?.portfolios ?? []).filter((p) => {
    if (riskFilter !== "all" && p.liquidation_risk !== riskFilter) return false;
    if (patternFilter !== "all" && p.liquidation_pattern !== patternFilter) return false;
    return true;
  });

  const kpis = summary
    ? [
        { label: "Total Portefeuilles", value: summary.total, sub: "évalués" },
        { label: "Liquidation Imminente", value: summary.liquidation_imminent_count, sub: "portefeuilles", accent: "text-red-400" },
        { label: "Top-up Collatéral", value: summary.collateral_top_up_count, sub: "requis", accent: "text-orange-400" },
        { label: "Composite Moyen", value: summary.avg_liquidation_composite.toFixed(1), sub: "score liquidation" },
        { label: "Index Risque Moyen", value: summary.avg_estimated_liquidation_risk_index.toFixed(2), sub: "sur 10", accent: "text-amber-400" },
        { label: "Critiques", value: summary.risk_counts["critical"] ?? 0, sub: "portefeuilles critiques", accent: "text-red-400" },
      ]
    : [];

  const distributions: Array<{ title: string; counts: Record<string, number>; colors: Record<string, string> }> = summary
    ? [
        {
          title: "Risque de Liquidation",
          counts: summary.risk_counts,
          colors: { low: "Faible", moderate: "Modéré", high: "Élevé", critical: "Critique" },
        },
        {
          title: "Patrons de Liquidation",
          counts: summary.pattern_counts,
          colors: PATTERN_LABELS,
        },
        {
          title: "Sévérité",
          counts: summary.severity_counts,
          colors: { secured: "Sécurisé", monitored: "Surveillé", at_risk: "À Risque", liquidating: "En Liquidation" },
        },
        {
          title: "Actions Recommandées",
          counts: summary.action_counts,
          colors: ACTION_LABELS,
        },
      ]
    : [];

  const patterns = ["all", "collateral_cascade", "oracle_attack", "liquidity_crunch", "protocol_exploit", "peg_destabilization", "none"];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {selected && <DetailModal port={selected} onClose={() => setSelected(null)} />}

      <div>
        <h1 className="text-2xl font-bold text-orange-400">Synthetic Asset Portfolio &amp; Liquidation Engine</h1>
        <p className="text-sm text-slate-400 mt-1">
          Surveille les portefeuilles d&apos;actifs synthétiques, les risques de liquidation DeFi, la santé des collatéraux et l&apos;exposition aux protocoles décentralisés
        </p>
      </div>

      {/* KPI Strip */}
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-4">
        {kpis.map((k) => (
          <div key={k.label} className="bg-slate-900 border border-red-500/30 rounded-xl p-4">
            <p className="text-xs text-slate-500 uppercase tracking-widest mb-1">{k.label}</p>
            <p className={`text-2xl font-bold ${k.accent ?? "text-slate-100"}`}>{k.value}</p>
            <p className="text-xs text-slate-500 mt-0.5">{k.sub}</p>
          </div>
        ))}
      </div>

      {/* Gauge Rings */}
      {summary && (
        <div className="bg-slate-900 border border-red-500/30 rounded-xl p-6">
          <h2 className="text-sm font-semibold text-slate-300 uppercase tracking-widest mb-6">Scores Moyens du Portefeuille</h2>
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-6 justify-items-center">
            <GaugeRing label="Santé Collatéral" value={summary.avg_collateral_score} color="#f87171" />
            <GaugeRing label="Sécurité Protocole" value={summary.avg_protocol_score} color="#fb923c" />
            <GaugeRing label="Liquidité DeFi" value={summary.avg_liquidity_score} color="#fbbf24" />
            <GaugeRing label="Risque Systémique" value={summary.avg_systemic_score} color="#f43f5e" />
          </div>
        </div>
      )}

      {/* Distribution Bars */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {distributions.map((d) => (
          <DistBar
            key={d.title}
            title={d.title}
            counts={d.counts}
            colors={d.colors}
            total={summary?.total ?? 1}
          />
        ))}
      </div>

      {/* Filters */}
      <div className="space-y-3">
        <div className="flex gap-2 flex-wrap">
          <span className="text-xs text-slate-500 self-center mr-1">Risque:</span>
          {["all", "low", "moderate", "high", "critical"].map((f) => (
            <button key={f} onClick={() => setRiskFilter(f)}
              className={`px-4 py-1.5 rounded-full text-xs font-semibold border transition-colors ${
                riskFilter === f
                  ? "bg-orange-600 border-orange-500 text-white"
                  : "bg-slate-800 border-slate-700 text-slate-400 hover:text-slate-200"
              }`}>
              {f === "all" ? "Tous" : f.charAt(0).toUpperCase() + f.slice(1)}
            </button>
          ))}
        </div>
        <div className="flex gap-2 flex-wrap">
          <span className="text-xs text-slate-500 self-center mr-1">Patron:</span>
          {patterns.map((f) => (
            <button key={f} onClick={() => setPatternFilter(f)}
              className={`px-4 py-1.5 rounded-full text-xs font-semibold border transition-colors ${
                patternFilter === f
                  ? "bg-red-700 border-red-600 text-white"
                  : "bg-slate-800 border-slate-700 text-slate-400 hover:text-slate-200"
              }`}>
              {f === "all" ? "Tous" : (PATTERN_LABELS[f] ?? f)}
            </button>
          ))}
        </div>
      </div>

      {/* Portfolio Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
        {portfolios.map((port) => (
          <button key={port.portfolio_id} onClick={() => setSelected(port)}
            className="bg-slate-900 border border-red-500/30 rounded-xl p-4 text-left hover:border-orange-500/50 transition-colors group">
            <div className="flex items-start justify-between mb-3">
              <div>
                <p className="font-semibold text-slate-100 group-hover:text-orange-300 transition-colors">{port.portfolio_id}</p>
                <p className="text-xs text-slate-500">{port.region} · {ASSET_LABELS[port.asset_class] ?? port.asset_class}</p>
              </div>
              <div className="flex flex-col items-end gap-1">
                <span className={`text-xs font-semibold ${RISK_COLORS[port.liquidation_risk]}`}>
                  {port.liquidation_risk.toUpperCase()}
                </span>
                <span className={`text-xs px-1.5 py-0.5 rounded text-white ${SEV_COLORS[port.liquidation_severity]}`}>
                  {port.liquidation_severity}
                </span>
              </div>
            </div>
            <div className="flex items-center gap-3 mb-3">
              <PortfolioRing composite={port.liquidation_composite} />
              <div className="flex-1 space-y-1.5">
                <ScoreBar label="Collatéral" value={port.collateral_score} color="bg-red-500" />
                <ScoreBar label="Protocole" value={port.protocol_score} color="bg-orange-500" />
                <ScoreBar label="Liquidité" value={port.liquidity_score} color="bg-amber-500" />
                <ScoreBar label="Systémique" value={port.systemic_score} color="bg-rose-500" />
              </div>
            </div>
            <p className="text-xs text-slate-400 italic leading-snug line-clamp-2">{port.liquidation_signal}</p>
            <div className="flex gap-2 mt-3 flex-wrap">
              {port.is_liquidation_imminent && (
                <span className="text-xs px-2 py-0.5 rounded-full bg-red-400/10 border border-red-400/30 text-red-400">Imminente</span>
              )}
              {port.requires_collateral_top_up && (
                <span className="text-xs px-2 py-0.5 rounded-full bg-orange-400/10 border border-orange-400/30 text-orange-400">Top-up</span>
              )}
              <span className="text-xs px-2 py-0.5 rounded-full bg-slate-800 text-slate-400">
                {PATTERN_LABELS[port.liquidation_pattern] ?? port.liquidation_pattern}
              </span>
            </div>
          </button>
        ))}
      </div>
    </div>
  );
}
