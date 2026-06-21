"use client";
import { useEffect, useState } from "react";

// ── Types ─────────────────────────────────────────────────────────────────────

type RiskLevel      = "critical" | "high" | "moderate" | "low";
type HavenPattern   = "sovereign_wealth_capture" | "corporate_profit_shifting" | "illicit_financial_flows" | "regulatory_arbitrage_network" | "democratic_fiscal_erosion" | "none";
type Severity       = "crise_paradis_fiscal_systémique" | "opacité_financière_majeure_détectée" | "érosion_fiscale_structurelle" | "surveillance_conformité_fiscale";
type HavenAction    = "intervention_urgente_paradis_fiscal_critique" | "renforcement_échange_informations_automatique" | "audit_conformité_fiscale_approfondi" | "veille_transparence_fiscale_continue";

interface TheEntity {
  id: string;
  haven_type: string;
  region: string;
  evasion_score: number;
  opacity_score: number;
  harm_score: number;
  enforcement_score: number;
  composite_score: number;
  risk_level: RiskLevel;
  tax_haven_pattern: HavenPattern;
  severity: Severity;
  recommended_action: HavenAction;
  signal: string;
  secrecy_score: number;
  illicit_flow_volume: number;
}

interface TheSummary {
  module_id: number;
  module_name: string;
  total: number;
  critical: number;
  high: number;
  moderate: number;
  low: number;
  avg_composite: number;
  pattern_distribution: Record<string, number>;
  risk_distribution: Record<string, number>;
  severity_distribution: Record<string, number>;
  action_distribution: Record<string, number>;
  avg_estimated_tax_haven_index: number;
}

// ── Metadata ──────────────────────────────────────────────────────────────────

const RISK_META: Record<RiskLevel, { label: string; color: string; ring: string; badge: string }> = {
  critical: { label: "Crise Systémique",       color: "text-red-400",     ring: "#ef4444", badge: "bg-red-900/60 text-red-300 border-red-700" },
  high:     { label: "Opacité Majeure",         color: "text-orange-400",  ring: "#f97316", badge: "bg-orange-900/60 text-orange-300 border-orange-700" },
  moderate: { label: "Érosion Structurelle",    color: "text-amber-400",   ring: "#f59e0b", badge: "bg-amber-900/60 text-amber-300 border-amber-700" },
  low:      { label: "Sous Surveillance",       color: "text-emerald-400", ring: "#10b981", badge: "bg-emerald-900/60 text-emerald-300 border-emerald-700" },
};

const PATTERN_LABELS: Record<HavenPattern, string> = {
  sovereign_wealth_capture:    "Capture Fonds Souverains",
  corporate_profit_shifting:   "Transfert Profits Entreprises",
  illicit_financial_flows:     "Flux Financiers Illicites",
  regulatory_arbitrage_network:"Réseau Arbitrage Réglementaire",
  democratic_fiscal_erosion:   "Érosion Fiscale Démocratique",
  none:                        "Aucun",
};

const SEV_LABELS: Record<Severity, string> = {
  "crise_paradis_fiscal_systémique":      "Crise Systémique",
  "opacité_financière_majeure_détectée":  "Opacité Majeure",
  "érosion_fiscale_structurelle":         "Érosion Structurelle",
  "surveillance_conformité_fiscale":      "Sous Surveillance",
};

const ACTION_LABELS: Record<HavenAction, string> = {
  "intervention_urgente_paradis_fiscal_critique":    "Intervention Urgente",
  "renforcement_échange_informations_automatique":   "Renforcement Échange Info",
  "audit_conformité_fiscale_approfondi":             "Audit Conformité Fiscale",
  "veille_transparence_fiscale_continue":            "Veille Transparence Continue",
};

const RISK_COLORS: Record<string, string> = {
  critical: "#ef4444", high: "#f97316", moderate: "#f59e0b", low: "#10b981",
};

const PAT_COLORS: Record<string, string> = {
  sovereign_wealth_capture:    "#ef4444",
  corporate_profit_shifting:   "#f97316",
  illicit_financial_flows:     "#3b82f6",
  regulatory_arbitrage_network:"#a855f7",
  democratic_fiscal_erosion:   "#f59e0b",
  none:                        "#10b981",
};

const SEV_COLORS: Record<string, string> = {
  "crise_paradis_fiscal_systémique":      "#ef4444",
  "opacité_financière_majeure_détectée":  "#f97316",
  "érosion_fiscale_structurelle":         "#f59e0b",
  "surveillance_conformité_fiscale":      "#10b981",
};

const ACT_COLORS: Record<string, string> = {
  "intervention_urgente_paradis_fiscal_critique":    "#ef4444",
  "renforcement_échange_informations_automatique":   "#f97316",
  "audit_conformité_fiscale_approfondi":             "#f59e0b",
  "veille_transparence_fiscale_continue":            "#10b981",
};

// ── Components ────────────────────────────────────────────────────────────────

function GaugeRing({ value, label, color }: { value: number; label: string; color: string }) {
  const r = 36;
  const circ = 2 * Math.PI * r;
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
          <div key={k} style={{ width: `${v / total * 100}%`, background: colors[k] || "#64748b" }} title={`${k}: ${v}`}/>
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

function DetailModal({ entity, onClose }: { entity: TheEntity; onClose: () => void }) {
  const [tab, setTab] = useState<"scores" | "signal" | "action">("scores");
  const risk = RISK_META[entity.risk_level];

  useEffect(() => {
    const h = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", h);
    return () => window.removeEventListener("keydown", h);
  }, [onClose]);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/75" onClick={onClose}>
      <div className="bg-slate-900 border border-emerald-800/30 rounded-xl w-full max-w-lg p-6 shadow-2xl" onClick={e => e.stopPropagation()}>
        <div className="flex items-center justify-between mb-4">
          <div>
            <span className="text-lg font-bold text-white">{entity.id}</span>
            <span className="ml-2 text-emerald-400 text-xs">{entity.haven_type.replace(/_/g, " ")}</span>
            <span className="ml-2 text-slate-400 text-xs">{entity.region}</span>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl leading-none">✕</button>
        </div>

        <div className="flex gap-2 mb-4">
          {(["scores", "signal", "action"] as const).map(t => (
            <button key={t} onClick={() => setTab(t)}
              className={`px-3 py-1 rounded text-xs font-medium transition-colors ${tab === t ? "bg-emerald-800 text-white" : "bg-slate-800 text-slate-400 hover:text-white"}`}>
              {t === "scores" ? "Scores" : t === "signal" ? "Signal" : "Action"}
            </button>
          ))}
        </div>

        {tab === "scores" && (
          <div className="grid grid-cols-2 gap-3 text-sm">
            {[
              ["Évasion",      entity.evasion_score,     "#ef4444"],
              ["Opacité",      entity.opacity_score,     "#f97316"],
              ["Préjudice",    entity.harm_score,        "#3b82f6"],
              ["Coercition",   entity.enforcement_score, "#a855f7"],
            ].map(([l, v, c]) => (
              <div key={String(l)} className="bg-slate-800 border border-emerald-800/20 rounded-lg p-3">
                <div className="text-slate-400 text-xs mb-1">{String(l)}</div>
                <div className="text-white font-bold text-lg">{Number(v).toFixed(1)}</div>
                <div className="h-1.5 rounded mt-1 bg-slate-700">
                  <div className="h-1.5 rounded" style={{ width: `${Math.min(Number(v), 100)}%`, background: String(c) }}/>
                </div>
              </div>
            ))}
            <div className="col-span-2 bg-slate-800 border border-emerald-800/20 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Score Composite</div>
              <div className="text-white font-bold text-2xl">{entity.composite_score.toFixed(1)}</div>
            </div>
          </div>
        )}

        {tab === "signal" && (
          <div className="bg-slate-800 border border-emerald-800/20 rounded-lg p-4 text-sm text-slate-200 leading-relaxed">
            {entity.signal}
            <div className="mt-3 flex gap-2 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium border ${risk?.badge || "bg-slate-700 text-slate-300"}`}>
                {entity.risk_level}
              </span>
              <span className="px-2 py-0.5 rounded text-xs font-medium bg-slate-700 text-amber-300">
                {SEV_LABELS[entity.severity] || entity.severity.replace(/_/g, " ")}
              </span>
              <span className="px-2 py-0.5 rounded text-xs font-medium bg-slate-700 text-emerald-300">
                {PATTERN_LABELS[entity.tax_haven_pattern] || entity.tax_haven_pattern.replace(/_/g, " ")}
              </span>
            </div>
            <div className="mt-3 grid grid-cols-2 gap-2 text-xs text-slate-400">
              <div>Score secret: <span className="text-red-300">{Math.round(entity.secrecy_score * 100)}%</span></div>
              <div>Flux illicites: <span className="text-orange-300">{Math.round(entity.illicit_flow_volume * 100)}%</span></div>
            </div>
          </div>
        )}

        {tab === "action" && (
          <div className="space-y-3 text-sm">
            <div className="bg-slate-800 border border-emerald-800/20 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Action Recommandée</div>
              <div className="text-white font-medium">
                {ACTION_LABELS[entity.recommended_action] || entity.recommended_action.replace(/_/g, " ")}
              </div>
            </div>
            <div className="bg-slate-800 border border-emerald-800/20 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Sévérité</div>
              <div className="text-white font-medium">{SEV_LABELS[entity.severity] || entity.severity.replace(/_/g, " ")}</div>
            </div>
            <div className="bg-slate-800 border border-emerald-800/20 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Patron Détecté</div>
              <div className="text-white font-medium">{PATTERN_LABELS[entity.tax_haven_pattern] || entity.tax_haven_pattern.replace(/_/g, " ")}</div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

// ── Dashboard ─────────────────────────────────────────────────────────────────

export default function TaxHavenDashboard() {
  const [data, setData]         = useState<{ entities: TheEntity[]; summary: TheSummary } | null>(null);
  const [riskFilter, setRisk]   = useState<string>("all");
  const [regFilter, setReg]     = useState<string>("all");
  const [selected, setSelected] = useState<TheEntity | null>(null);

  useEffect(() => {
    fetch("/api/tax-haven-engine")
      .then(r => r.json())
      .then(setData)
      .catch(console.error);
  }, []);

  if (!data) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-emerald-400 text-lg animate-pulse">Initialisation Moteur Paradis Fiscaux — Module 405...</div>
    </div>
  );

  const { entities, summary } = data;

  const regions  = ["all", ...Array.from(new Set(entities.map(e => e.region)))];
  const filtered = entities.filter(e =>
    (riskFilter === "all" || e.risk_level === riskFilter) &&
    (regFilter  === "all" || e.region === regFilter)
  );

  const avgEvasion     = entities.length ? entities.reduce((s, e) => s + e.evasion_score, 0) / entities.length : 0;
  const avgOpacity     = entities.length ? entities.reduce((s, e) => s + e.opacity_score, 0) / entities.length : 0;
  const avgHarm        = entities.length ? entities.reduce((s, e) => s + e.harm_score, 0) / entities.length : 0;
  const avgEnforcement = entities.length ? entities.reduce((s, e) => s + e.enforcement_score, 0) / entities.length : 0;

  const dists = [
    { title: "Niveau de Risque",   counts: summary.risk_distribution,     colors: RISK_COLORS },
    { title: "Patron Détecté",     counts: summary.pattern_distribution,   colors: PAT_COLORS  },
    { title: "Sévérité",           counts: summary.severity_distribution,  colors: SEV_COLORS  },
    { title: "Action Recommandée", counts: summary.action_distribution,    colors: ACT_COLORS  },
  ] as Array<{ title: string; counts: Record<string, number>; colors: Record<string, string> }>;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-300 p-6 space-y-6">
      {selected && <DetailModal entity={selected} onClose={() => setSelected(null)}/>}

      {/* En-tête */}
      <div>
        <h1 className="text-2xl font-bold text-emerald-400">
          Paradis Fiscaux &amp; Centres Financiers Offshore — Module 405
        </h1>
        <p className="text-slate-400 text-sm mt-1">
          Évasion · Opacité · Préjudice · Coercition — Intelligence Fiscale Offshore — Caelum Partners
        </p>
        <p className="text-slate-500 text-xs mt-0.5">Chaima Mhadbi — Bruxelles</p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {[
          ["Total Juridictions",        summary.total,                                                    "text-slate-300"],
          ["Crise Systémique",          summary.critical,                                                 "text-red-400"],
          ["Opacité Majeure",           summary.high,                                                     "text-orange-400"],
          ["Composite Moyen",           summary.avg_composite.toFixed(1),                                 "text-emerald-300"],
          ["Index Paradis Fiscal",      summary.avg_estimated_tax_haven_index.toFixed(2) + "/10",         "text-orange-300"],
          ["Érosion Structurelle",      summary.moderate,                                                 "text-amber-400"],
        ].map(([l, v, c]) => (
          <div key={String(l)} className="bg-slate-900 border border-emerald-800/30 rounded-xl p-3 text-center">
            <div className={`text-xl font-bold ${c}`}>{v}</div>
            <div className="text-xs text-slate-500 mt-0.5 leading-tight">{l}</div>
          </div>
        ))}
      </div>

      {/* Gauge Rings */}
      <div className="bg-slate-900 border border-emerald-800/30 rounded-xl p-5">
        <p className="text-xs text-slate-500 mb-4 font-medium">Scores Moyens par Dimension</p>
        <div className="grid grid-cols-4 gap-4">
          <GaugeRing value={avgEvasion}     label="Évasion"    color="#ef4444"/>
          <GaugeRing value={avgOpacity}     label="Opacité"    color="#f97316"/>
          <GaugeRing value={avgHarm}        label="Préjudice"  color="#3b82f6"/>
          <GaugeRing value={avgEnforcement} label="Coercition" color="#a855f7"/>
        </div>
      </div>

      {/* Distribution Bars */}
      <div className="bg-slate-900 border border-emerald-800/30 rounded-xl p-5 grid grid-cols-1 md:grid-cols-2 gap-5">
        {dists.map(d => <DistBar key={d.title} {...d}/>)}
      </div>

      {/* Filtres */}
      <div className="flex flex-wrap gap-2">
        {["all", "low", "moderate", "high", "critical"].map(r => (
          <button key={r} onClick={() => setRisk(r)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${riskFilter === r ? "bg-emerald-800 border-emerald-700 text-white" : "bg-slate-900 border-emerald-800/30 text-slate-400 hover:text-white"}`}>
            {r === "all" ? "Tous risques" : r === "critical" ? "Crise systémique" : r === "high" ? "Opacité majeure" : r === "moderate" ? "Érosion structurelle" : "Sous surveillance"}
          </button>
        ))}
        <span className="w-px h-5 self-center bg-emerald-800/30"/>
        {regions.map(r => (
          <button key={r} onClick={() => setReg(r)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${regFilter === r ? "bg-slate-700 border-slate-500 text-white" : "bg-slate-900 border-emerald-800/30 text-slate-400 hover:text-white"}`}>
            {r === "all" ? "Toutes régions" : r}
          </button>
        ))}
      </div>

      {/* Cartes Entités */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {filtered.map(e => {
          const risk = RISK_META[e.risk_level];
          return (
            <div key={e.id} onClick={() => setSelected(e)}
              className="bg-slate-900 border border-slate-800 rounded-xl p-4 cursor-pointer hover:border-emerald-800/50 transition-colors">
              <div className="flex items-center justify-between mb-1">
                <span className="font-bold text-white">{e.id}</span>
                <span className="text-xs text-slate-400">{e.region}</span>
              </div>
              <div className="text-xs text-emerald-400 mb-2 capitalize">{e.haven_type.replace(/_/g, " ")}</div>
              <div className="flex gap-1 mb-3 flex-wrap">
                <span className={`px-2 py-0.5 rounded text-xs font-medium border ${risk?.badge || "bg-slate-700 text-slate-300"}`}>
                  {risk?.label || e.risk_level}
                </span>
                <span className="px-2 py-0.5 rounded text-xs font-medium bg-slate-700 text-amber-300">
                  {SEV_LABELS[e.severity] || e.severity.replace(/_/g, " ")}
                </span>
              </div>
              <div className="text-2xl font-black text-white mb-1">{e.composite_score.toFixed(1)}</div>
              <div className="text-xs text-slate-500 mb-2 capitalize">{PATTERN_LABELS[e.tax_haven_pattern] || e.tax_haven_pattern.replace(/_/g, " ")}</div>
              <div className="text-xs text-emerald-400 font-medium mb-2">
                {ACTION_LABELS[e.recommended_action] || e.recommended_action.replace(/_/g, " ")}
              </div>
              <div className="flex gap-1 flex-wrap text-xs">
                <span className="text-slate-500">Secret: <span className="text-red-300">{Math.round(e.secrecy_score * 100)}%</span></span>
                <span className="text-slate-500 ml-1">Illicites: <span className="text-orange-300">{Math.round(e.illicit_flow_volume * 100)}%</span></span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
