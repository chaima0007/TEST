"use client";
import { useEffect, useState } from "react";

type PEEEntity = {
  id: string;
  platform_sector: string;
  region: string;
  exploitation_score: number;
  precarity_score: number;
  monopoly_score: number;
  misclassification_score: number;
  composite_score: number;
  risk_level: string;
  dominant_pattern: string;
  patterns_detected: string[];
  severity: string;
  action: string;
  signal: string;
  surveillance_score: number;
};

type PEESummary = {
  total_entities: number;
  critical_count: number;
  high_count: number;
  moderate_count: number;
  low_count: number;
  avg_exploitation: number;
  avg_precarity: number;
  avg_monopoly: number;
  avg_misclassification: number;
  avg_composite: number;
  top_pattern: string;
  entities_at_risk: number;
  avg_estimated_gig_rights_index: number;
};

function GaugeRing({ value, label, color }: { value: number; label: string; color: string }) {
  const r = 36;
  const circ = 2 * Math.PI * r;
  const fill = circ * (1 - value / 100);
  return (
    <div className="flex flex-col items-center gap-1">
      <svg width="88" height="88" viewBox="0 0 88 88">
        <circle cx="44" cy="44" r={r} fill="none" stroke="#0c1521" strokeWidth="8" />
        <circle
          cx="44" cy="44" r={r} fill="none" stroke={color} strokeWidth="8"
          strokeDasharray={circ} strokeDashoffset={fill}
          strokeLinecap="round" transform="rotate(-90 44 44)"
        />
        <text x="44" y="49" textAnchor="middle" fill="white" fontSize="13" fontWeight="bold">
          {Math.round(value)}
        </text>
      </svg>
      <span className="text-xs text-violet-400/70 text-center">{label}</span>
    </div>
  );
}

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
      <span className="text-xs text-violet-400/70 font-medium">{title}</span>
      <div className="flex h-3 rounded overflow-hidden gap-px">
        {Object.entries(counts).map(([k, v]) => (
          <div
            key={k}
            style={{ width: `${(v / total) * 100}%`, background: colors[k] || "#6d28d9" }}
            title={`${k}: ${v}`}
          />
        ))}
      </div>
      <div className="flex flex-wrap gap-x-3 gap-y-0.5">
        {Object.entries(counts).map(([k, v]) => (
          <span key={k} className="text-xs text-violet-400/60">
            <span style={{ color: colors[k] || "#7c3aed" }}>■</span> {k.replace(/_/g, " ")} {v}
          </span>
        ))}
      </div>
    </div>
  );
}

const RISK_COLORS: Record<string, string> = {
  low: "#16a34a",
  moderate: "#d97706",
  high: "#ea580c",
  critical: "#dc2626",
};
const PATTERN_COLORS: Record<string, string> = {
  algorithmic_wage_theft: "#dc2626",
  benefits_denial_systematic: "#ea580c",
  platform_monopoly_capture: "#7c3aed",
  misclassification_fraud: "#b45309",
  surveillance_control_dystopia: "#0891b2",
};
const SEV_COLORS: Record<string, string> = {
  faible: "#16a34a",
  modérée: "#d97706",
  élevée: "#ea580c",
  critique: "#dc2626",
};
const ACTION_COLORS: Record<string, string> = {
  veille_économie_plateformes_continue: "#16a34a",
  "audit_conditions_travail_plateforme_et_reclassification": "#d97706",
  "renforcement_protection_sociale_gig_economy_accéléré": "#ea580c",
  "intervention_urgente_droits_travailleurs_plateformes_critiques": "#dc2626",
};
const RISK_BADGE: Record<string, string> = {
  low: "bg-green-900 text-green-300",
  moderate: "bg-amber-900 text-amber-300",
  high: "bg-orange-950 text-orange-400",
  critical: "bg-red-950 text-red-400",
};
const SEV_BADGE: Record<string, string> = {
  faible: "bg-green-900 text-green-300",
  modérée: "bg-amber-900 text-amber-300",
  élevée: "bg-orange-950 text-orange-400",
  critique: "bg-red-950 text-red-400",
};

function DetailModal({ entity, onClose }: { entity: PEEEntity; onClose: () => void }) {
  const [tab, setTab] = useState<"scores" | "signal" | "action">("scores");

  useEffect(() => {
    const h = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
    };
    window.addEventListener("keydown", h);
    return () => window.removeEventListener("keydown", h);
  }, [onClose]);

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/80"
      onClick={onClose}
    >
      <div
        className="bg-slate-950 border border-violet-700/30 rounded-xl w-full max-w-lg p-6 shadow-2xl"
        onClick={e => e.stopPropagation()}
      >
        <div className="flex items-center justify-between mb-4">
          <div>
            <span className="text-lg font-bold text-white">{entity.id}</span>
            <span className="ml-2 text-violet-400 text-xs">{entity.region}</span>
            <span className="ml-2 text-slate-500 text-xs">
              {entity.platform_sector.replace(/_/g, " ")}
            </span>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl leading-none">
            ✕
          </button>
        </div>

        <div className="flex gap-2 mb-4">
          {(["scores", "signal", "action"] as const).map(t => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`px-3 py-1 rounded text-xs font-medium transition-colors ${
                tab === t
                  ? "bg-violet-900 text-white"
                  : "bg-slate-900 text-slate-400 hover:text-white"
              }`}
            >
              {t === "scores" ? "Scores" : t === "signal" ? "Signal" : "Action"}
            </button>
          ))}
        </div>

        {tab === "scores" && (
          <div className="grid grid-cols-2 gap-3 text-sm">
            {[
              ["Score Exploitation",       entity.exploitation_score,      "#dc2626"],
              ["Score Précarité",          entity.precarity_score,         "#ea580c"],
              ["Score Monopole",           entity.monopoly_score,          "#7c3aed"],
              ["Score Misclassification",  entity.misclassification_score, "#b45309"],
            ].map(([l, v, c]) => (
              <div
                key={String(l)}
                className="bg-slate-900 border border-violet-700/20 rounded-lg p-3"
              >
                <div className="text-violet-400/60 text-xs mb-1">{String(l)}</div>
                <div className="text-white font-bold text-lg">{Number(v).toFixed(1)}</div>
                <div className="h-1.5 rounded mt-1 bg-slate-800">
                  <div
                    className="h-1.5 rounded"
                    style={{ width: `${Math.min(Number(v), 100)}%`, background: String(c) }}
                  />
                </div>
              </div>
            ))}
            <div className="col-span-2 bg-slate-900 border border-violet-700/20 rounded-lg p-3">
              <div className="text-violet-400/60 text-xs mb-1">Score Composite Économie Plateforme</div>
              <div className="text-white font-bold text-2xl">
                {entity.composite_score.toFixed(1)}
              </div>
            </div>
            <div className="col-span-2 bg-slate-900 border border-violet-700/20 rounded-lg p-3">
              <div className="text-violet-400/60 text-xs mb-1">Patterns Détectés</div>
              <div className="flex flex-wrap gap-1 mt-1">
                {entity.patterns_detected.length > 0
                  ? entity.patterns_detected.map(p => (
                      <span
                        key={p}
                        className="px-2 py-0.5 rounded text-xs font-medium bg-slate-800 text-orange-400"
                        style={{ color: PATTERN_COLORS[p] || "#a78bfa" }}
                      >
                        {p.replace(/_/g, " ")}
                      </span>
                    ))
                  : <span className="text-slate-500 text-xs">Aucun pattern détecté</span>
                }
              </div>
            </div>
          </div>
        )}

        {tab === "signal" && (
          <div className="bg-slate-900 border border-violet-700/20 rounded-lg p-4 text-sm text-slate-200 leading-relaxed">
            {entity.signal}
            <div className="mt-3 flex gap-2 flex-wrap">
              <span
                className={`px-2 py-0.5 rounded text-xs font-medium ${
                  RISK_BADGE[entity.risk_level] || "bg-slate-700 text-slate-300"
                }`}
              >
                {entity.risk_level}
              </span>
              <span
                className={`px-2 py-0.5 rounded text-xs font-medium ${
                  SEV_BADGE[entity.severity] || "bg-slate-700 text-slate-300"
                }`}
              >
                {entity.severity}
              </span>
            </div>
            <div className="mt-3 grid grid-cols-2 gap-2">
              <div className="bg-slate-800 rounded p-2">
                <div className="text-violet-400/50 text-xs mb-0.5">Score Surveillance</div>
                <div className="text-white text-sm font-medium">
                  {Math.round(entity.surveillance_score * 100)}%
                </div>
              </div>
              <div className="bg-slate-800 rounded p-2">
                <div className="text-violet-400/50 text-xs mb-0.5">Pattern Dominant</div>
                <div className="text-orange-400 text-xs font-medium capitalize">
                  {entity.dominant_pattern.replace(/_/g, " ")}
                </div>
              </div>
            </div>
          </div>
        )}

        {tab === "action" && (
          <div className="space-y-3 text-sm">
            <div className="bg-slate-900 border border-violet-700/20 rounded-lg p-3">
              <div className="text-violet-400/60 text-xs mb-1">Action Recommandée</div>
              <div className="text-white font-medium">
                {entity.action.replace(/_/g, " ")}
              </div>
            </div>
            <div className="bg-slate-900 border border-violet-700/20 rounded-lg p-3">
              <div className="text-violet-400/60 text-xs mb-1">Secteur Plateforme</div>
              <div className="text-white font-medium capitalize">
                {entity.platform_sector.replace(/_/g, " ")}
              </div>
            </div>
            <div className="bg-slate-900 border border-violet-700/20 rounded-lg p-3">
              <div className="text-violet-400/60 text-xs mb-1">Pattern Dominant</div>
              <div className="font-medium capitalize" style={{ color: PATTERN_COLORS[entity.dominant_pattern] || "#a78bfa" }}>
                {entity.dominant_pattern.replace(/_/g, " ")}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function PlatformEconomyDashboard() {
  const [data, setData] = useState<{
    entities: PEEEntity[];
    summary: PEESummary;
  } | null>(null);
  const [riskFilter, setRiskFilter] = useState<string>("all");
  const [patFilter, setPatFilter] = useState<string>("all");
  const [selected, setSelected] = useState<PEEEntity | null>(null);

  useEffect(() => {
    fetch("/api/platform-economy-engine")
      .then(r => r.json())
      .then(setData)
      .catch(console.error);
  }, []);

  if (!data) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center">
        <div className="text-violet-400 text-lg animate-pulse">
          Initialisation du Moteur Économie de Plateforme...
        </div>
      </div>
    );
  }

  const { entities, summary } = data;

  const filtered = entities.filter(
    e =>
      (riskFilter === "all" || e.risk_level === riskFilter) &&
      (patFilter === "all" || e.dominant_pattern === patFilter)
  );

  // Build distribution counts
  const riskDist: Record<string, number> = {};
  const patDist: Record<string, number> = {};
  const sevDist: Record<string, number> = {};
  const actDist: Record<string, number> = {};
  for (const e of entities) {
    riskDist[e.risk_level] = (riskDist[e.risk_level] || 0) + 1;
    patDist[e.dominant_pattern] = (patDist[e.dominant_pattern] || 0) + 1;
    sevDist[e.severity] = (sevDist[e.severity] || 0) + 1;
    actDist[e.action] = (actDist[e.action] || 0) + 1;
  }

  const dists = [
    { title: "Niveau de Risque",        counts: riskDist, colors: RISK_COLORS    },
    { title: "Pattern Dominant",        counts: patDist,  colors: PATTERN_COLORS  },
    { title: "Sévérité",                counts: sevDist,  colors: SEV_COLORS      },
    { title: "Action Déclenchée",       counts: actDist,  colors: ACTION_COLORS   },
  ] as Array<{ title: string; counts: Record<string, number>; colors: Record<string, string> }>;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {selected && <DetailModal entity={selected} onClose={() => setSelected(null)} />}

      <div>
        <h1 className="text-2xl font-bold text-violet-400">
          Économie de Plateforme &amp; Droits Travailleurs Gig — Module 408
        </h1>
        <p className="text-orange-400/60 text-sm mt-1">
          Exploitation · Précarité · Monopole · Misclassification — Caelum Partners — Chaima Mhadbi, Fondatrice, Bruxelles
        </p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {[
          ["Total Entités",                 summary.total_entities,                                         "text-violet-400"],
          ["Crise Critique",                summary.critical_count,                                         "text-red-400"],
          ["Risque Élevé",                  summary.high_count,                                             "text-orange-400"],
          ["Composite Moyen",               `${summary.avg_composite.toFixed(1)}`,                          "text-violet-300"],
          ["Index Droits Gig",              `${summary.avg_estimated_gig_rights_index.toFixed(2)}/10`,      "text-orange-400"],
          ["Entités à Risque",              summary.entities_at_risk,                                       "text-red-400"],
        ].map(([l, v, c]) => (
          <div
            key={String(l)}
            className="bg-slate-900 border border-violet-700/30 rounded-xl p-3 text-center"
          >
            <div className={`text-xl font-bold ${c}`}>{v}</div>
            <div className="text-xs text-violet-400/40 mt-0.5 leading-tight">{l}</div>
          </div>
        ))}
      </div>

      {/* Gauge Rings */}
      <div className="bg-slate-900 border border-violet-700/30 rounded-xl p-5">
        <div className="grid grid-cols-4 gap-4">
          <GaugeRing
            value={entities.reduce((s, e) => s + e.exploitation_score, 0) / (entities.length || 1)}
            label="Exploitation Moy."
            color="#dc2626"
          />
          <GaugeRing
            value={entities.reduce((s, e) => s + e.precarity_score, 0) / (entities.length || 1)}
            label="Précarité Moy."
            color="#ea580c"
          />
          <GaugeRing
            value={entities.reduce((s, e) => s + e.monopoly_score, 0) / (entities.length || 1)}
            label="Monopole Moy."
            color="#7c3aed"
          />
          <GaugeRing
            value={entities.reduce((s, e) => s + e.misclassification_score, 0) / (entities.length || 1)}
            label="Misclassif. Moy."
            color="#b45309"
          />
        </div>
      </div>

      {/* Distribution Bars */}
      <div className="bg-slate-900 border border-violet-700/30 rounded-xl p-5 grid grid-cols-1 md:grid-cols-2 gap-5">
        {dists.map(d => (
          <DistBar key={d.title} {...d} />
        ))}
      </div>

      {/* Filter Pills */}
      <div className="flex flex-wrap gap-2">
        {["all", "low", "moderate", "high", "critical"].map(r => (
          <button
            key={r}
            onClick={() => setRiskFilter(r)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${
              riskFilter === r
                ? "bg-violet-900 border-violet-700 text-white"
                : "bg-slate-900 border-violet-700/30 text-violet-400/70 hover:text-white"
            }`}
          >
            {r}
          </button>
        ))}
        <span className="w-px h-5 self-center bg-violet-700/30" />
        {[
          "all",
          "algorithmic_wage_theft",
          "benefits_denial_systematic",
          "platform_monopoly_capture",
          "misclassification_fraud",
          "surveillance_control_dystopia",
        ].map(p => (
          <button
            key={p}
            onClick={() => setPatFilter(p)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${
              patFilter === p
                ? "bg-orange-950 border-orange-700 text-white"
                : "bg-slate-900 border-violet-700/30 text-violet-400/70 hover:text-white"
            }`}
          >
            {p.replace(/_/g, " ")}
          </button>
        ))}
      </div>

      {/* Entity Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {filtered.map(e => (
          <div
            key={e.id}
            onClick={() => setSelected(e)}
            className="bg-slate-900 border border-violet-700/30 rounded-xl p-4 cursor-pointer hover:border-violet-500 transition-colors"
          >
            <div className="flex items-center justify-between mb-1">
              <span className="font-bold text-white">{e.id}</span>
              <span className="text-xs text-violet-400/60">{e.region}</span>
            </div>
            <div className="text-xs text-slate-500 mb-2 capitalize">
              {e.platform_sector.replace(/_/g, " ")}
            </div>
            <div className="flex gap-1 mb-3 flex-wrap">
              <span
                className={`px-2 py-0.5 rounded text-xs font-medium ${
                  RISK_BADGE[e.risk_level] || "bg-slate-700 text-slate-300"
                }`}
              >
                {e.risk_level}
              </span>
              <span
                className={`px-2 py-0.5 rounded text-xs font-medium ${
                  SEV_BADGE[e.severity] || "bg-slate-700 text-slate-300"
                }`}
              >
                {e.severity}
              </span>
            </div>
            <div className="text-2xl font-black text-white mb-1">
              {e.composite_score.toFixed(1)}
            </div>
            <div className="text-xs mb-2 capitalize font-medium" style={{ color: PATTERN_COLORS[e.dominant_pattern] || "#a78bfa" }}>
              {e.dominant_pattern.replace(/_/g, " ")}
            </div>
            <div className="text-xs text-violet-400/70 font-medium mb-2">
              Exploit: {e.exploitation_score.toFixed(1)} · Précarité: {e.precarity_score.toFixed(1)}
            </div>
            <div className="text-xs text-slate-400 truncate">{e.signal}</div>
          </div>
        ))}
      </div>
    </div>
  );
}
