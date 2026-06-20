"use client";
import { useEffect, useState } from "react";

type MNHEntity = {
  entity_id: string;
  name: string;
  country: string;
  sector: string;
  composite_score: number;
  algorithmic_harm_amplification_score: number;
  youth_vulnerability_exposure_score: number;
  mental_disorder_correlation_score: number;
  platform_accountability_deficit_score: number;
  risk_level: string;
  primary_pattern: string;
  key_signals: string[];
  estimated_mentalhealth_index: number;
  last_updated: string;
  confidence_level: number;
};

type MNHSummary = {
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
  entities: MNHEntity[];
  avg_estimated_mentalhealth_index: number;
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
            style={{ width: `${(v / total) * 100}%`, background: colors[k] || "#7c3aed" }}
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
  faible: "#16a34a",
  "modéré": "#d97706",
  "élevé": "#92400e",
  critique: "#dc2626",
};

const PATTERN_COLORS: Record<string, string> = {
  platform_responsible: "#16a34a",
  depression_anxiety_nexus: "#0891b2",
  youth_mental_crisis: "#7c3aed",
  algorithmic_radicalization: "#b45309",
  platform_negligence: "#dc2626",
};

const RISK_BADGE: Record<string, string> = {
  faible: "bg-green-900 text-green-300",
  "modéré": "bg-amber-900 text-amber-300",
  "élevé": "bg-orange-950 text-orange-400",
  critique: "bg-red-950 text-red-400",
};

type TabType = "Scores" | "Signaux" | "Actions";

function DetailModal({ entity, onClose }: { entity: MNHEntity; onClose: () => void }) {
  const [tab, setTab] = useState<TabType>("Scores");

  useEffect(() => {
    const h = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
    };
    window.addEventListener("keydown", h);
    return () => window.removeEventListener("keydown", h);
  }, [onClose]);

  const PATTERN_LABELS: Record<string, { severity_fr: string; action_fr: string; signal_fr: string }> = {
    algorithmic_radicalization: {
      severity_fr: "Radicalisation Algorithmique",
      action_fr: "Audit algorithmique indépendant et refonte des systèmes de recommandation",
      signal_fr: "Amplification algorithmique de contenus nocifs détectée",
    },
    youth_mental_crisis: {
      severity_fr: "Crise Santé Mentale Jeunes",
      action_fr: "Restrictions d'accès mineurs et protocoles de protection renforcés",
      signal_fr: "Exposition massive des jeunes à des contenus préjudiciables",
    },
    depression_anxiety_nexus: {
      severity_fr: "Nexus Dépression-Anxiété",
      action_fr: "Partenariat clinique et intégration d'outils de bien-être numérique",
      signal_fr: "Corrélation forte entre usage plateforme et troubles mentaux",
    },
    platform_negligence: {
      severity_fr: "Négligence Plateforme",
      action_fr: "Cadre de responsabilité réglementaire et sanctions plateformes",
      signal_fr: "Déficit critique de responsabilité plateforme",
    },
    platform_responsible: {
      severity_fr: "Plateforme Responsable",
      action_fr: "Maintien et amplification des bonnes pratiques bien-être numérique",
      signal_fr: "Pratiques de protection de la santé mentale conformes",
    },
  };

  const patternInfo = PATTERN_LABELS[entity.primary_pattern] ?? {
    severity_fr: entity.primary_pattern,
    action_fr: "Action non définie",
    signal_fr: "Signal non défini",
  };

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
            <span className="text-lg font-bold text-white">{entity.name}</span>
            <span className="ml-2 text-violet-400 text-xs">{entity.country}</span>
            <span className="ml-2 text-slate-500 text-xs">{entity.sector}</span>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl leading-none">
            ✕
          </button>
        </div>

        <div className="flex gap-2 mb-4">
          {(["Scores", "Signaux", "Actions"] as TabType[]).map(t => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`px-3 py-1 rounded text-xs font-medium transition-colors ${
                tab === t
                  ? "bg-violet-900 text-white"
                  : "bg-slate-900 text-slate-400 hover:text-white"
              }`}
            >
              {t}
            </button>
          ))}
        </div>

        {tab === "Scores" && (
          <div className="grid grid-cols-2 gap-3 text-sm">
            {[
              ["Amplification Nocive Algorithmique", entity.algorithmic_harm_amplification_score, "#b45309"],
              ["Exposition Vulnérabilité Jeunes",    entity.youth_vulnerability_exposure_score,    "#7c3aed"],
              ["Corrélation Troubles Mentaux",       entity.mental_disorder_correlation_score,      "#0891b2"],
              ["Déficit Responsabilité Plateforme",  entity.platform_accountability_deficit_score,  "#dc2626"],
            ].map(([l, v, c]) => (
              <div
                key={String(l)}
                className="bg-slate-900 border border-violet-700/20 rounded-lg p-3"
              >
                <div className="text-violet-400/60 text-xs mb-1 leading-tight">{String(l)}</div>
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
              <div className="text-violet-400/60 text-xs mb-1">Score Composite Santé Mentale</div>
              <div className="text-white font-bold text-2xl">{entity.composite_score.toFixed(2)}</div>
              <div className="text-violet-400/50 text-xs mt-1">
                Index Bien-être Numérique: {entity.estimated_mentalhealth_index.toFixed(2)}/10
              </div>
            </div>
            <div className="col-span-2 bg-slate-900 border border-violet-700/20 rounded-lg p-3 flex items-center justify-between">
              <div>
                <div className="text-violet-400/60 text-xs mb-1">Niveau de Risque</div>
                <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[entity.risk_level] || "bg-slate-700 text-slate-300"}`}>
                  {entity.risk_level}
                </span>
              </div>
              <div className="text-right">
                <div className="text-violet-400/60 text-xs mb-1">Confiance Analyse</div>
                <div className="text-white font-bold">{Math.round(entity.confidence_level * 100)}%</div>
              </div>
            </div>
          </div>
        )}

        {tab === "Signaux" && (
          <div className="space-y-3">
            <div className="bg-slate-900 border border-violet-700/20 rounded-lg p-3">
              <div className="text-violet-400/60 text-xs mb-2">Signal Principal — {patternInfo.severity_fr}</div>
              <div className="text-slate-300 text-sm">{patternInfo.signal_fr}</div>
            </div>
            <div className="space-y-2">
              <div className="text-violet-400/60 text-xs font-medium">Signaux Détaillés</div>
              {entity.key_signals.map((signal, i) => (
                <div key={i} className="bg-slate-900 border border-violet-700/10 rounded-lg p-3 text-sm text-slate-200 leading-relaxed">
                  <span className="text-violet-500 font-bold mr-2">{i + 1}.</span>
                  {signal}
                </div>
              ))}
            </div>
            <div className="flex gap-2 flex-wrap mt-2">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[entity.risk_level] || "bg-slate-700 text-slate-300"}`}>
                {entity.risk_level}
              </span>
              <span className="px-2 py-0.5 rounded text-xs font-medium bg-violet-950 text-violet-300">
                {entity.primary_pattern.replace(/_/g, " ")}
              </span>
            </div>
          </div>
        )}

        {tab === "Actions" && (
          <div className="space-y-3 text-sm">
            <div className="bg-slate-900 border border-violet-700/20 rounded-lg p-3">
              <div className="text-violet-400/60 text-xs mb-1">Patron Détecté</div>
              <div className="text-violet-300 font-medium">{patternInfo.severity_fr}</div>
            </div>
            <div className="bg-slate-900 border border-violet-700/20 rounded-lg p-3">
              <div className="text-violet-400/60 text-xs mb-1">Action Recommandée</div>
              <div className="text-white font-medium leading-relaxed">{patternInfo.action_fr}</div>
            </div>
            <div className="bg-slate-900 border border-violet-700/20 rounded-lg p-3">
              <div className="text-violet-400/60 text-xs mb-1">Plateforme</div>
              <div className="text-white font-medium">{entity.name}</div>
              <div className="text-slate-500 text-xs mt-0.5">{entity.country} — {entity.sector}</div>
            </div>
            <div className="bg-slate-900 border border-violet-700/20 rounded-lg p-3">
              <div className="text-violet-400/60 text-xs mb-1">Dernière Mise à Jour</div>
              <div className="text-white font-medium">{entity.last_updated}</div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function SocialMediaMentalHealthDashboard() {
  const [data, setData] = useState<MNHSummary | null>(null);
  const [riskFilter, setRiskFilter] = useState<string>("tous");
  const [selected, setSelected] = useState<MNHEntity | null>(null);

  useEffect(() => {
    fetch("/api/social-media-mental-health-engine")
      .then(r => r.json())
      .then(setData)
      .catch(console.error);
  }, []);

  if (!data) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center">
        <div className="text-violet-400 text-lg animate-pulse">
          Initialisation du Moteur Santé Mentale Réseaux Sociaux...
        </div>
      </div>
    );
  }

  const { entities, risk_distribution, pattern_distribution } = data;

  const filtered = entities.filter(e =>
    riskFilter === "tous" || e.risk_level === riskFilter
  );

  const avgAHA = entities.reduce((s, e) => s + e.algorithmic_harm_amplification_score, 0) / (entities.length || 1);
  const avgYVE = entities.reduce((s, e) => s + e.youth_vulnerability_exposure_score, 0) / (entities.length || 1);
  const avgMDC = entities.reduce((s, e) => s + e.mental_disorder_correlation_score, 0) / (entities.length || 1);
  const avgPAD = entities.reduce((s, e) => s + e.platform_accountability_deficit_score, 0) / (entities.length || 1);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {selected && <DetailModal entity={selected} onClose={() => setSelected(null)} />}

      <div>
        <h1 className="text-2xl font-bold text-violet-400">
          Santé Mentale &amp; Réseaux Sociaux — Moteur d&apos;Intelligence
        </h1>
        <p className="text-violet-400/60 text-sm mt-1">
          Algorithmes · Jeunesse · Troubles Mentaux · Responsabilité — Caelum Partners — Chaima Mhadbi, Fondatrice, Bruxelles
        </p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {[
          ["Total Plateformes",          data.total_entities,                                      "text-violet-400"],
          ["Risque Critique",            risk_distribution["critique"] ?? 0,                       "text-red-400"],
          ["Risque Élevé",               risk_distribution["élevé"] ?? 0,                          "text-orange-400"],
          ["Score Composite Moyen",      data.avg_composite.toFixed(1),                            "text-violet-300"],
          ["Index Bien-être Numérique",  `${data.avg_estimated_mentalhealth_index.toFixed(2)}/10`, "text-violet-400"],
          ["Score Confiance Analyse",    `${Math.round(data.confidence_score * 100)}%`,            "text-violet-500"],
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
        <div className="text-xs text-violet-400/60 font-medium mb-4">Dimensions d&apos;Impact Moyen</div>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <GaugeRing value={avgAHA} label="Amplification Nocive" color="#b45309" />
          <GaugeRing value={avgYVE} label="Vulnérabilité Jeunes" color="#7c3aed" />
          <GaugeRing value={avgMDC} label="Corrélation Troubles" color="#0891b2" />
          <GaugeRing value={avgPAD} label="Déficit Responsabilité" color="#dc2626" />
        </div>
      </div>

      {/* Distribution Bars */}
      <div className="bg-slate-900 border border-violet-700/30 rounded-xl p-5 grid grid-cols-1 md:grid-cols-2 gap-5">
        <DistBar
          title="Distribution par Niveau de Risque"
          counts={risk_distribution}
          colors={RISK_COLORS}
        />
        <DistBar
          title="Distribution par Patron Détecté"
          counts={pattern_distribution}
          colors={PATTERN_COLORS}
        />
      </div>

      {/* Alertes Critiques */}
      {data.critical_alerts.length > 0 && (
        <div className="bg-red-950/40 border border-red-700/40 rounded-xl p-4">
          <div className="text-xs text-red-400/70 font-medium mb-2">Alertes Critiques Santé Mentale</div>
          <div className="flex flex-wrap gap-2">
            {data.critical_alerts.map(name => (
              <span key={name} className="px-2 py-0.5 rounded bg-red-900/60 text-red-300 text-xs font-medium">
                {name}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Filter Pills */}
      <div className="flex flex-wrap gap-2">
        {["tous", "critique", "élevé", "modéré", "faible"].map(r => (
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
      </div>

      {/* Entity Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {filtered.map(e => (
          <div
            key={e.entity_id}
            onClick={() => setSelected(e)}
            className="bg-slate-900 border border-violet-700/30 rounded-xl p-4 cursor-pointer hover:border-violet-500 transition-colors"
          >
            <div className="flex items-center justify-between mb-1">
              <span className="font-bold text-white text-sm">{e.entity_id}</span>
              <span className="text-xs text-violet-400/60">{e.country}</span>
            </div>
            <div className="text-sm text-white font-medium mb-1 leading-tight">{e.name}</div>
            <div className="text-xs text-slate-500 mb-2">{e.sector}</div>
            <div className="flex gap-1 mb-3 flex-wrap">
              <span
                className={`px-2 py-0.5 rounded text-xs font-medium ${
                  RISK_BADGE[e.risk_level] || "bg-slate-700 text-slate-300"
                }`}
              >
                {e.risk_level}
              </span>
              <span
                className="px-2 py-0.5 rounded text-xs font-medium bg-violet-950 text-violet-300"
                style={{ background: PATTERN_COLORS[e.primary_pattern] ? `${PATTERN_COLORS[e.primary_pattern]}22` : undefined }}
              >
                <span style={{ color: PATTERN_COLORS[e.primary_pattern] || "#7c3aed" }}>■</span>{" "}
                {e.primary_pattern.replace(/_/g, " ")}
              </span>
            </div>
            <div className="text-2xl font-black text-white mb-1">{e.composite_score.toFixed(1)}</div>
            <div className="text-xs text-violet-400/50 mb-2">
              Index bien-être: {e.estimated_mentalhealth_index.toFixed(2)}/10
            </div>
            <div className="space-y-1">
              <div className="flex justify-between text-xs">
                <span className="text-slate-500">Amplif. Nocive</span>
                <span className="text-amber-400">{e.algorithmic_harm_amplification_score.toFixed(0)}</span>
              </div>
              <div className="flex justify-between text-xs">
                <span className="text-slate-500">Vuln. Jeunes</span>
                <span className="text-violet-400">{e.youth_vulnerability_exposure_score.toFixed(0)}</span>
              </div>
              <div className="flex justify-between text-xs">
                <span className="text-slate-500">Corr. Troubles</span>
                <span className="text-cyan-400">{e.mental_disorder_correlation_score.toFixed(0)}</span>
              </div>
            </div>
            <div className="text-xs text-slate-500 mt-2 truncate" title={e.key_signals[0]}>
              {e.key_signals[0]}
            </div>
          </div>
        ))}
      </div>

      {/* Sources */}
      <div className="bg-slate-900 border border-violet-700/20 rounded-xl p-4">
        <div className="text-xs text-violet-400/60 font-medium mb-2">Sources de Données</div>
        <div className="flex flex-wrap gap-2">
          {data.data_sources.map(src => (
            <span key={src} className="px-2 py-0.5 rounded bg-slate-800 text-slate-400 text-xs">
              {src}
            </span>
          ))}
        </div>
        <div className="text-xs text-slate-600 mt-2">
          Dernière analyse: {data.last_analysis} · Version: {data.engine_version}
        </div>
      </div>
    </div>
  );
}
