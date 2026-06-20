"use client";
import { useEffect, useState } from "react";

// ── Types ─────────────────────────────────────────────────────────────────────

type RiskLevel = "critique" | "élevé" | "modéré" | "faible";
type PatternName =
  | "Opacité Fournisseur Critique"
  | "Non-Conformité Réglementaire"
  | "Traçabilité Défaillante"
  | "Divulgation Insuffisante"
  | "Risque Fournisseur Émergent";
type ActionName =
  | "plan_urgence_transparence_chaîne_approvisionnement"
  | "audit_conformité_fournisseurs_prioritaire"
  | "programme_amélioration_divulgation_continue"
  | "veille_transparence_fournisseurs_active";

interface SctEntity {
  entity_id: string;
  name: string;
  country: string;
  sector: string;
  composite_score: number;
  traceability_score: number;
  compliance_score: number;
  disclosure_score: number;
  risk_mitigation_score: number;
  risk_level: RiskLevel;
  primary_pattern: PatternName;
  key_signals: string[];
  estimated_transparency_index: number;
  last_updated: string;
  recommended_action: ActionName;
}

interface SctSummary {
  total_entities: number;
  avg_composite: number;
  risk_distribution: Record<string, number>;
  pattern_distribution: Record<string, number>;
  top_risk_entities: string[];
  critical_alerts: string[];
  last_analysis: string;
  engine_version: string;
  domain: string;
  confidence_score: number;
  data_sources: string[];
  entities: SctEntity[];
  avg_estimated_transparency_index: number;
}

// ── Metadata ──────────────────────────────────────────────────────────────────

const RISK_META: Record<RiskLevel, { label: string; color: string; ring: string; badge: string }> = {
  critique: { label: "Opacité Critique",      color: "text-red-400",    ring: "#ef4444", badge: "bg-red-900/60 text-red-300 border-red-700" },
  "élevé":  { label: "Risque Élevé",          color: "text-orange-400", ring: "#f97316", badge: "bg-orange-900/60 text-orange-300 border-orange-700" },
  "modéré": { label: "Divulgation Partielle",  color: "text-amber-400",  ring: "#f59e0b", badge: "bg-amber-900/60 text-amber-300 border-amber-700" },
  faible:   { label: "Transparent",           color: "text-teal-400",   ring: "#14b8a6", badge: "bg-teal-900/60 text-teal-300 border-teal-700" },
};

const PATTERN_LABELS: Record<PatternName, string> = {
  "Opacité Fournisseur Critique":  "Opacité Fournisseur Critique",
  "Non-Conformité Réglementaire":  "Non-Conformité Réglementaire",
  "Traçabilité Défaillante":       "Traçabilité Défaillante",
  "Divulgation Insuffisante":      "Divulgation Insuffisante",
  "Risque Fournisseur Émergent":   "Risque Fournisseur Émergent",
};

const ACTION_LABELS: Record<ActionName, string> = {
  "plan_urgence_transparence_chaîne_approvisionnement": "Plan Urgence Transparence Chaîne",
  "audit_conformité_fournisseurs_prioritaire":          "Audit Conformité Fournisseurs",
  "programme_amélioration_divulgation_continue":        "Programme Amélioration Divulgation",
  "veille_transparence_fournisseurs_active":            "Veille Transparence Active",
};

const RISK_COLORS: Record<string, string> = {
  critique: "#ef4444",
  "élevé":  "#f97316",
  "modéré": "#f59e0b",
  faible:   "#14b8a6",
};

const PAT_COLORS: Record<string, string> = {
  "Opacité Fournisseur Critique": "#ef4444",
  "Non-Conformité Réglementaire": "#f97316",
  "Traçabilité Défaillante":      "#f59e0b",
  "Divulgation Insuffisante":     "#06b6d4",
  "Risque Fournisseur Émergent":  "#14b8a6",
};

const ACT_COLORS: Record<string, string> = {
  "plan_urgence_transparence_chaîne_approvisionnement": "#ef4444",
  "audit_conformité_fournisseurs_prioritaire":          "#f97316",
  "programme_amélioration_divulgation_continue":        "#f59e0b",
  "veille_transparence_fournisseurs_active":            "#14b8a6",
};

// ── GaugeRing ─────────────────────────────────────────────────────────────────

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
      <span className="text-xs text-stone-400 text-center">{label}</span>
    </div>
  );
}

// ── DistBar ───────────────────────────────────────────────────────────────────

function DistBar({ title, counts, colors }: { title: string; counts: Record<string, number>; colors: Record<string, string> }) {
  const total = Object.values(counts).reduce((a, b) => a + b, 0) || 1;
  return (
    <div className="flex flex-col gap-1">
      <span className="text-xs text-stone-400 font-medium">{title}</span>
      <div className="flex h-3 rounded overflow-hidden gap-px">
        {Object.entries(counts).map(([k, v]) => (
          <div key={k} style={{ width: `${v / total * 100}%`, background: colors[k] || "#78716c" }} title={`${k}: ${v}`}/>
        ))}
      </div>
      <div className="flex flex-wrap gap-x-3 gap-y-0.5">
        {Object.entries(counts).map(([k, v]) => (
          <span key={k} className="text-xs text-stone-400">
            <span style={{ color: colors[k] || "#a8a29e" }}>■</span> {k} {v}
          </span>
        ))}
      </div>
    </div>
  );
}

// ── DetailModal ───────────────────────────────────────────────────────────────

function DetailModal({ entity, onClose }: { entity: SctEntity; onClose: () => void }) {
  const [tab, setTab] = useState<"scores" | "signaux" | "actions">("scores");
  const risk = RISK_META[entity.risk_level];

  useEffect(() => {
    const h = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", h);
    return () => window.removeEventListener("keydown", h);
  }, [onClose]);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/75" onClick={onClose}>
      <div className="bg-slate-900 border border-teal-800/30 rounded-xl w-full max-w-lg p-6 shadow-2xl" onClick={e => e.stopPropagation()}>
        <div className="flex items-center justify-between mb-4">
          <div>
            <span className="text-lg font-bold text-white">{entity.name}</span>
            <span className="ml-2 text-teal-400 text-xs">{entity.entity_id}</span>
            <span className="ml-2 text-stone-400 text-xs">{entity.country} · {entity.sector}</span>
          </div>
          <button onClick={onClose} className="text-stone-500 hover:text-white text-xl leading-none">✕</button>
        </div>

        <div className="flex gap-2 mb-4">
          {(["scores", "signaux", "actions"] as const).map(t => (
            <button key={t} onClick={() => setTab(t)}
              className={`px-3 py-1 rounded text-xs font-medium transition-colors ${tab === t ? "bg-teal-800 text-white" : "bg-slate-800 text-stone-400 hover:text-white"}`}>
              {t === "scores" ? "Scores" : t === "signaux" ? "Signaux" : "Actions"}
            </button>
          ))}
        </div>

        {tab === "scores" && (
          <div className="grid grid-cols-2 gap-3 text-sm">
            {[
              ["Traçabilité",     entity.traceability_score,    "#14b8a6"],
              ["Conformité",      entity.compliance_score,       "#f97316"],
              ["Divulgation",     entity.disclosure_score,       "#06b6d4"],
              ["Maîtrise Risque", entity.risk_mitigation_score,  "#a855f7"],
            ].map(([l, v, c]) => (
              <div key={String(l)} className="bg-slate-800 border border-teal-800/20 rounded-lg p-3">
                <div className="text-stone-400 text-xs mb-1">{String(l)}</div>
                <div className="text-white font-bold text-lg">{Number(v).toFixed(1)}</div>
                <div className="h-1.5 rounded mt-1 bg-slate-700">
                  <div className="h-1.5 rounded" style={{ width: `${Math.min(Number(v), 100)}%`, background: String(c) }}/>
                </div>
              </div>
            ))}
            <div className="col-span-2 bg-slate-800 border border-teal-800/20 rounded-lg p-3">
              <div className="text-stone-400 text-xs mb-1">Score Composite</div>
              <div className="text-white font-bold text-2xl">{entity.composite_score.toFixed(1)}</div>
              <div className="text-teal-400 text-xs mt-1">Index Transparence: {entity.estimated_transparency_index.toFixed(2)}/10</div>
            </div>
          </div>
        )}

        {tab === "signaux" && (
          <div className="bg-slate-800 border border-teal-800/20 rounded-lg p-4 text-sm text-slate-200 leading-relaxed">
            <div className="mb-3 flex gap-2 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium border ${risk?.badge || "bg-slate-700 text-stone-300"}`}>
                {entity.risk_level}
              </span>
              <span className="px-2 py-0.5 rounded text-xs font-medium bg-slate-700 text-cyan-300">
                {PATTERN_LABELS[entity.primary_pattern] || entity.primary_pattern}
              </span>
            </div>
            <ul className="space-y-2">
              {entity.key_signals.map((sig, i) => (
                <li key={i} className="flex items-start gap-2">
                  <span className="text-teal-400 mt-0.5">▸</span>
                  <span className="text-stone-300 text-xs">{sig}</span>
                </li>
              ))}
            </ul>
            <div className="mt-3 text-xs text-stone-500">
              Dernière mise à jour: {new Date(entity.last_updated).toLocaleString("fr-FR")}
            </div>
          </div>
        )}

        {tab === "actions" && (
          <div className="space-y-3 text-sm">
            <div className="bg-slate-800 border border-teal-800/20 rounded-lg p-3">
              <div className="text-stone-400 text-xs mb-1">Action Recommandée</div>
              <div className="text-white font-medium">
                {ACTION_LABELS[entity.recommended_action] || entity.recommended_action.replace(/_/g, " ")}
              </div>
            </div>
            <div className="bg-slate-800 border border-teal-800/20 rounded-lg p-3">
              <div className="text-stone-400 text-xs mb-1">Patron Principal</div>
              <div className="text-white font-medium">{PATTERN_LABELS[entity.primary_pattern] || entity.primary_pattern}</div>
            </div>
            <div className="bg-slate-800 border border-teal-800/20 rounded-lg p-3">
              <div className="text-stone-400 text-xs mb-1">Niveau de Risque</div>
              <div className={`font-bold text-base ${risk?.color || "text-stone-300"}`}>
                {risk?.label || entity.risk_level}
              </div>
            </div>
            <div className="bg-slate-800 border border-teal-800/20 rounded-lg p-3">
              <div className="text-stone-400 text-xs mb-1">Index de Transparence</div>
              <div className="text-teal-400 font-bold text-xl">{entity.estimated_transparency_index.toFixed(2)}<span className="text-stone-400 text-sm font-normal">/10</span></div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

// ── Dashboard ─────────────────────────────────────────────────────────────────

export default function SupplyChainTransparencyDashboard() {
  const [data, setData]           = useState<{ entities: SctEntity[]; summary: SctSummary } | null>(null);
  const [riskFilter, setRisk]     = useState<string>("all");
  const [countryFilter, setCountry] = useState<string>("all");
  const [selected, setSelected]   = useState<SctEntity | null>(null);

  useEffect(() => {
    fetch("/api/supply-chain-transparency-engine")
      .then(r => r.json())
      .then(setData)
      .catch(console.error);
  }, []);

  if (!data) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-teal-400 text-lg animate-pulse">Initialisation du Moteur Transparence Chaîne d&apos;Approvisionnement...</div>
    </div>
  );

  const { entities, summary } = data;

  // Derive avg sub-scores from entities
  const n = entities.length || 1;
  const avgTraceability  = Math.round(entities.reduce((s, e) => s + e.traceability_score, 0) / n * 10) / 10;
  const avgCompliance    = Math.round(entities.reduce((s, e) => s + e.compliance_score, 0) / n * 10) / 10;
  const avgDisclosure    = Math.round(entities.reduce((s, e) => s + e.disclosure_score, 0) / n * 10) / 10;
  const avgRiskMitigation = Math.round(entities.reduce((s, e) => s + e.risk_mitigation_score, 0) / n * 10) / 10;

  const countries = ["all", ...Array.from(new Set(entities.map(e => e.country)))];
  const filtered  = entities.filter(e =>
    (riskFilter    === "all" || e.risk_level  === riskFilter) &&
    (countryFilter === "all" || e.country     === countryFilter)
  );

  const critiqueCount = summary.risk_distribution["critique"] || 0;
  const eleveCount    = summary.risk_distribution["élevé"]   || 0;

  const dists = [
    { title: "Niveau de Risque",    counts: summary.risk_distribution,    colors: RISK_COLORS },
    { title: "Patron Détecté",      counts: summary.pattern_distribution,  colors: PAT_COLORS  },
    { title: "Action Recommandée",  counts: Object.fromEntries(
        entities.reduce((m, e) => {
          m.set(e.recommended_action, (m.get(e.recommended_action) || 0) + 1);
          return m;
        }, new Map<string, number>())
      ),                                                                    colors: ACT_COLORS  },
    { title: "Pays",                counts: Object.fromEntries(
        entities.reduce((m, e) => {
          m.set(e.country, (m.get(e.country) || 0) + 1);
          return m;
        }, new Map<string, number>())
      ),                                                                    colors: {} },
  ] as Array<{ title: string; counts: Record<string, number>; colors: Record<string, string> }>;

  return (
    <div className="min-h-screen bg-slate-950 text-stone-300 p-6 space-y-6">
      {selected && <DetailModal entity={selected} onClose={() => setSelected(null)}/>}

      {/* En-tête */}
      <div>
        <h1 className="text-2xl font-bold text-teal-400">
          Transparence Chaîne d&apos;Approvisionnement
        </h1>
        <p className="text-stone-400 text-sm mt-1">
          Traçabilité · Conformité · Divulgation · Maîtrise Risque — Intelligence Transparence Supply Chain — Caelum Partners
        </p>
        <p className="text-stone-500 text-xs mt-0.5">Chaima Mhadbi — Bruxelles</p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {[
          ["Total Entités",          summary.total_entities,                                                "text-stone-300"],
          ["Opacité Critique",       critiqueCount,                                                         "text-red-400"],
          ["Risque Élevé",           eleveCount,                                                            "text-orange-400"],
          ["Composite Moyen",        summary.avg_composite.toFixed(1),                                      "text-teal-300"],
          ["Index Transparence",     summary.avg_estimated_transparency_index.toFixed(2) + "/10",           "text-cyan-400"],
          ["Conformité Moyenne",     avgCompliance.toFixed(1),                                              "text-amber-400"],
        ].map(([l, v, c]) => (
          <div key={String(l)} className="bg-slate-900 border border-teal-800/30 rounded-xl p-3 text-center">
            <div className={`text-xl font-bold ${c}`}>{v}</div>
            <div className="text-xs text-stone-500 mt-0.5 leading-tight">{l}</div>
          </div>
        ))}
      </div>

      {/* Gauge Rings */}
      <div className="bg-slate-900 border border-teal-800/30 rounded-xl p-5">
        <p className="text-xs text-stone-500 mb-4 font-medium">Scores Moyens par Dimension</p>
        <div className="grid grid-cols-4 gap-4">
          <GaugeRing value={avgTraceability}   label="Traçabilité"     color="#14b8a6"/>
          <GaugeRing value={avgCompliance}     label="Conformité"      color="#f97316"/>
          <GaugeRing value={avgDisclosure}     label="Divulgation"     color="#06b6d4"/>
          <GaugeRing value={avgRiskMitigation} label="Maîtrise Risque" color="#a855f7"/>
        </div>
      </div>

      {/* Distribution Bars */}
      <div className="bg-slate-900 border border-teal-800/30 rounded-xl p-5 grid grid-cols-1 md:grid-cols-2 gap-5">
        {dists.map(d => <DistBar key={d.title} {...d}/>)}
      </div>

      {/* Alertes Critiques */}
      {summary.critical_alerts.length > 0 && (
        <div className="bg-red-950/30 border border-red-800/40 rounded-xl p-4">
          <p className="text-xs text-red-400 font-semibold mb-2">Alertes Critiques — Opacité Détectée</p>
          <ul className="space-y-1">
            {summary.critical_alerts.map((alert, i) => (
              <li key={i} className="text-xs text-red-300 flex items-start gap-2">
                <span className="text-red-500 mt-0.5">▸</span>
                <span>{alert}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Filtres */}
      <div className="flex flex-wrap gap-2">
        {["all", "faible", "modéré", "élevé", "critique"].map(r => (
          <button key={r} onClick={() => setRisk(r)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${riskFilter === r ? "bg-teal-800 border-teal-700 text-white" : "bg-slate-900 border-teal-800/30 text-stone-400 hover:text-white"}`}>
            {r === "all" ? "Tous risques" : r === "critique" ? "Opacité Critique" : r === "élevé" ? "Risque Élevé" : r === "modéré" ? "Divulgation Partielle" : "Transparent"}
          </button>
        ))}
        <span className="w-px h-5 self-center bg-teal-800/30"/>
        {countries.map(c => (
          <button key={c} onClick={() => setCountry(c)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${countryFilter === c ? "bg-slate-700 border-slate-500 text-white" : "bg-slate-900 border-teal-800/30 text-stone-400 hover:text-white"}`}>
            {c === "all" ? "Tous pays" : c}
          </button>
        ))}
      </div>

      {/* Cartes Entités */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {filtered.map(e => {
          const risk = RISK_META[e.risk_level];
          return (
            <div key={e.entity_id} onClick={() => setSelected(e)}
              className="bg-slate-900 border border-slate-800 rounded-xl p-4 cursor-pointer hover:border-teal-700/50 transition-colors">
              <div className="flex items-center justify-between mb-1">
                <span className="font-bold text-white text-sm">{e.name}</span>
                <span className="text-xs text-stone-400">{e.country}</span>
              </div>
              <div className="text-xs text-teal-400 mb-2">{e.sector}</div>
              <div className="flex gap-1 mb-3 flex-wrap">
                <span className={`px-2 py-0.5 rounded text-xs font-medium border ${risk?.badge || "bg-slate-700 text-stone-300"}`}>
                  {risk?.label || e.risk_level}
                </span>
              </div>
              <div className="text-2xl font-black text-white mb-0.5">{e.composite_score.toFixed(1)}</div>
              <div className="text-teal-400 text-xs mb-2">Index: {e.estimated_transparency_index.toFixed(2)}/10</div>
              <div className="text-xs text-stone-500 mb-2 italic">{PATTERN_LABELS[e.primary_pattern] || e.primary_pattern}</div>
              <div className="text-xs text-cyan-400 font-medium mb-2">
                {ACTION_LABELS[e.recommended_action] || e.recommended_action.replace(/_/g, " ")}
              </div>
              <div className="space-y-0.5">
                {e.key_signals.slice(0, 2).map((sig, i) => (
                  <div key={i} className="text-xs text-stone-500 truncate">
                    <span className="text-teal-500">▸</span> {sig}
                  </div>
                ))}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
