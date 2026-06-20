"use client";
import { useEffect, useState } from "react";

// ── types ────────────────────────────────────────────────────────────────────

type Entity = {
  entity_id:                  string;
  name:                       string;
  country:                    string;
  sector:                     string;
  composite_score:            number;
  evasion_score:              number;
  avoidance_score:            number;
  offshore_score:             number;
  inequality_score:           number;
  risk_level:                 string;
  primary_pattern:            string;
  key_signals:                string[];
  estimated_taxjustice_index: number;
  last_updated:               string;
  alerts:                     string[];
};

type ApiData = {
  total_entities:                number;
  avg_composite:                 number;
  risk_distribution:             Record<string, number>;
  pattern_distribution:          Record<string, number>;
  top_risk_entities:             Array<{ entity_id: string; name: string; composite_score: number; risk_level: string }>;
  critical_alerts:               string[];
  last_analysis:                 string;
  engine_version:                string;
  domain:                        string;
  confidence_score:              number;
  data_sources:                  string[];
  entities:                      Entity[];
  avg_estimated_taxjustice_index: number;
};

// ── colour maps ──────────────────────────────────────────────────────────────

const RISK_COLOR: Record<string, string> = {
  faible:   "#10b981",
  modéré:   "#f59e0b",
  élevé:    "#f97316",
  critique: "#ef4444",
};
const PAT_COLOR: Record<string, string> = {
  "Évasion Fiscale Systémique":     "#ef4444",
  "Optimisation Abusive Offshore":  "#dc2626",
  "Contournement Réglementaire":    "#f97316",
  "Inégalité Fiscale Structurelle": "#f59e0b",
  "Risque Réputation Fiscale":      "#10b981",
};
const RISK_BADGE: Record<string, string> = {
  faible:   "bg-emerald-900 text-emerald-300",
  modéré:   "bg-amber-900 text-amber-300",
  élevé:    "bg-orange-900 text-orange-300",
  critique: "bg-red-900 text-red-300",
};
const PAT_BADGE: Record<string, string> = {
  "Évasion Fiscale Systémique":     "bg-red-900 text-red-300",
  "Optimisation Abusive Offshore":  "bg-rose-900 text-rose-300",
  "Contournement Réglementaire":    "bg-orange-900 text-orange-300",
  "Inégalité Fiscale Structurelle": "bg-amber-900 text-amber-300",
  "Risque Réputation Fiscale":      "bg-emerald-900 text-emerald-300",
};

const PATTERN_ACTIONS: Record<string, string> = {
  "Évasion Fiscale Systémique":     "Signalement immédiat aux autorités fiscales compétentes. Gel des actifs suspects et ouverture d'une enquête judiciaire. Coopération internationale via CRS/FATCA.",
  "Optimisation Abusive Offshore":  "Audit d'urgence des structures offshore. Restructuration fiscale obligatoire sous 90 jours. Déclaration aux autorités via échange automatique d'informations.",
  "Contournement Réglementaire":    "Audit de conformité fiscale renforcé. Révision des prix de transfert intra-groupe. Mise en conformité avec les règles BEPS de l'OCDE.",
  "Inégalité Fiscale Structurelle": "Révision de la politique fiscale interne. Alignement du taux effectif d'imposition sur le taux légal. Rapport de transparence fiscale publié annuellement.",
  "Risque Réputation Fiscale":      "Veille réputation fiscale standard. Maintien de la conformité CbCR OCDE. Communication proactive sur la contribution fiscale totale.",
};

// ── sub-components ───────────────────────────────────────────────────────────

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
      <span className="text-xs text-red-300 font-medium">{title}</span>
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
          <span key={k} className="text-xs text-stone-400">
            <span style={{ color: colors[k] || "#94a3b8" }}>■</span> {k} {v}
          </span>
        ))}
      </div>
    </div>
  );
}

function DetailModal({
  entity,
  onClose,
}: {
  entity: Entity;
  onClose: () => void;
}) {
  const [activeTab, setActiveTab] = useState<"scores" | "signals" | "actions">("scores");

  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
    };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [onClose]);

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/75"
      onClick={onClose}
    >
      <div
        className="bg-slate-900 border border-red-900/40 rounded-xl w-full max-w-lg p-6 shadow-2xl"
        onClick={(e) => e.stopPropagation()}
      >
        {/* header */}
        <div className="flex items-start justify-between mb-4">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <span className="text-lg font-bold text-white">{entity.entity_id}</span>
              <span
                className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[entity.risk_level] || "bg-slate-700 text-slate-300"}`}
              >
                {entity.risk_level}
              </span>
            </div>
            <div className="text-sm text-red-300 font-medium">{entity.name}</div>
            <div className="text-xs text-stone-400 mt-0.5">
              {entity.country} · {entity.sector}
            </div>
          </div>
          <button
            onClick={onClose}
            className="text-stone-500 hover:text-white text-xl leading-none"
          >
            ✕
          </button>
        </div>

        {/* tabs */}
        <div className="flex gap-2 mb-4">
          {(["scores", "signals", "actions"] as const).map((t) => (
            <button
              key={t}
              onClick={() => setActiveTab(t)}
              className={`px-3 py-1 rounded text-xs font-medium transition-colors ${
                activeTab === t
                  ? "bg-red-900 text-white border border-red-700"
                  : "bg-slate-800 text-stone-400 hover:text-white border border-transparent"
              }`}
            >
              {t === "scores" ? "Scores" : t === "signals" ? "Signaux" : "Actions"}
            </button>
          ))}
        </div>

        {/* Scores tab */}
        {activeTab === "scores" && (
          <div className="space-y-3">
            <div className="grid grid-cols-2 gap-3 text-sm">
              {[
                ["Évasion",   entity.evasion_score,   "#ef4444"],
                ["Évitement", entity.avoidance_score,  "#dc2626"],
                ["Offshore",  entity.offshore_score,   "#b91c1c"],
                ["Inégalité", entity.inequality_score, "#f97316"],
              ].map(([label, val, color]) => (
                <div key={String(label)} className="bg-slate-800 rounded-lg p-3">
                  <div className="text-stone-400 text-xs mb-1">{String(label)}</div>
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
              <div className="text-stone-400 text-xs mb-1">Score Composite</div>
              <div className="text-white font-bold text-2xl">{entity.composite_score.toFixed(2)}</div>
              <div className="text-stone-400 text-xs mt-1">
                Index Justice Fiscale: {entity.estimated_taxjustice_index.toFixed(2)}/10
              </div>
            </div>
          </div>
        )}

        {/* Signaux tab */}
        {activeTab === "signals" && (
          <div className="space-y-2">
            <div className="text-xs text-stone-400 mb-3 font-medium uppercase tracking-wide">
              Signaux clés identifiés
            </div>
            {entity.key_signals.map((sig, i) => (
              <div key={i} className="bg-slate-800 rounded-lg p-3 flex gap-3 items-start">
                <span className="text-red-500 font-bold text-sm mt-0.5">⚠</span>
                <span className="text-stone-200 text-sm leading-snug">{sig}</span>
              </div>
            ))}
            {entity.alerts.length > 0 && (
              <div className="mt-3 space-y-1">
                <div className="text-xs text-red-400 font-medium uppercase tracking-wide">
                  Alertes actives
                </div>
                {entity.alerts.map((alert, i) => (
                  <div key={i} className="bg-red-950/50 border border-red-800 rounded-lg p-2 text-xs text-red-300">
                    {alert}
                  </div>
                ))}
              </div>
            )}
            <div className="mt-2">
              <span
                className={`px-2 py-0.5 rounded text-xs font-medium ${PAT_BADGE[entity.primary_pattern] || "bg-slate-700 text-slate-300"}`}
              >
                {entity.primary_pattern}
              </span>
            </div>
          </div>
        )}

        {/* Actions tab */}
        {activeTab === "actions" && (
          <div className="space-y-3 text-sm">
            <div className="bg-red-950/40 border border-red-800/50 rounded-lg p-4">
              <div className="text-red-400 text-xs font-medium uppercase tracking-wide mb-2">
                Actions Recommandées
              </div>
              <div className="text-stone-200 leading-relaxed">
                {PATTERN_ACTIONS[entity.primary_pattern] || "Surveillance standard recommandée."}
              </div>
            </div>
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-stone-400 text-xs mb-1">Patron Principal</div>
              <div className="text-white font-medium">{entity.primary_pattern}</div>
            </div>
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-stone-400 text-xs mb-1">Niveau de Risque</div>
              <div
                className="font-bold text-lg"
                style={{ color: RISK_COLOR[entity.risk_level] || "#94a3b8" }}
              >
                {entity.risk_level.toUpperCase()}
              </div>
            </div>
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-stone-400 text-xs mb-1">Dernière Mise à Jour</div>
              <div className="text-white font-medium">{entity.last_updated}</div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

// ── main page ────────────────────────────────────────────────────────────────

export default function TaxJusticeEngineDashboard() {
  const [data, setData]                   = useState<ApiData | null>(null);
  const [loading, setLoading]             = useState(true);
  const [error, setError]                 = useState<string | null>(null);
  const [selectedRisk, setSelectedRisk]   = useState<string>("all");
  const [selectedCountry, setSelectedCountry] = useState<string>("all");
  const [selectedEntity, setSelectedEntity]   = useState<Entity | null>(null);

  useEffect(() => {
    fetch("/api/tax-justice-engine")
      .then((r) => {
        if (!r.ok) throw new Error(`HTTP ${r.status}`);
        return r.json();
      })
      .then((d: ApiData) => {
        setData(d);
        setLoading(false);
      })
      .catch((e: unknown) => {
        setError(e instanceof Error ? e.message : "Erreur inconnue");
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center">
        <div className="text-red-400 text-lg animate-pulse">
          Chargement Tax Justice Engine...
        </div>
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center">
        <div className="bg-red-950/50 border border-red-700 rounded-xl p-6 text-center max-w-md">
          <div className="text-red-400 text-lg font-bold mb-2">Erreur de chargement</div>
          <div className="text-stone-400 text-sm">{error ?? "Données non disponibles"}</div>
        </div>
      </div>
    );
  }

  // ── derived values ──────────────────────────────────────────────────────────

  const entities = data.entities ?? [];

  const allCountries = Array.from(new Set(entities.map((e) => e.country))).sort();

  const filtered = entities.filter(
    (e) =>
      (selectedRisk === "all" || e.risk_level === selectedRisk) &&
      (selectedCountry === "all" || e.country === selectedCountry),
  );

  const avgEvasion    = entities.length > 0 ? entities.reduce((a, e) => a + e.evasion_score, 0)    / entities.length : 0;
  const avgAvoidance  = entities.length > 0 ? entities.reduce((a, e) => a + e.avoidance_score, 0)  / entities.length : 0;
  const avgOffshore   = entities.length > 0 ? entities.reduce((a, e) => a + e.offshore_score, 0)   / entities.length : 0;
  const avgInequality = entities.length > 0 ? entities.reduce((a, e) => a + e.inequality_score, 0) / entities.length : 0;

  const critiqueCount = entities.filter((e) => e.risk_level === "critique").length;
  const eleveCount    = entities.filter((e) => e.risk_level === "élevé").length;
  const avgEvasionDisplay = Math.round(avgEvasion);

  const riskPills    = ["all", "critique", "élevé", "modéré", "faible"] as const;
  const countryPills = ["all", ...allCountries];

  return (
    <div className="min-h-screen bg-slate-950 text-stone-100 p-6 space-y-6">
      {selectedEntity && (
        <DetailModal entity={selectedEntity} onClose={() => setSelectedEntity(null)} />
      )}

      {/* header */}
      <div>
        <h1 className="text-2xl font-bold text-white">
          Tax Justice Engine — Intelligence Fiscale
        </h1>
        <p className="text-stone-400 text-sm mt-1">
          Évasion · Évitement · Offshore · Inégalité — analyse systémique de la justice fiscale
        </p>
        <div className="flex gap-3 mt-2 flex-wrap">
          <span className="text-xs text-stone-500">
            Version: <span className="text-red-400">{data.engine_version}</span>
          </span>
          <span className="text-xs text-stone-500">
            Dernière analyse: <span className="text-stone-300">{data.last_analysis}</span>
          </span>
          <span className="text-xs text-stone-500">
            Confiance: <span className="text-amber-400">{data.confidence_score}%</span>
          </span>
        </div>
      </div>

      {/* critical alerts banner */}
      {data.critical_alerts && data.critical_alerts.length > 0 && (
        <div className="bg-red-950/60 border border-red-700 rounded-xl p-4 space-y-1">
          <div className="text-red-400 font-semibold text-sm mb-2">
            Alertes Critiques ({data.critical_alerts.length})
          </div>
          {data.critical_alerts.map((alert, i) => (
            <div key={i} className="text-xs text-red-300 flex gap-2">
              <span>▸</span>
              <span>{alert}</span>
            </div>
          ))}
        </div>
      )}

      {/* KPI cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {[
          { label: "Total Entités",              value: data.total_entities,                              color: "text-red-400"   },
          { label: "Critique",                   value: critiqueCount,                                    color: "text-red-500"   },
          { label: "Élevé",                      value: eleveCount,                                       color: "text-orange-400" },
          { label: "Composite Moyen",            value: data.avg_composite.toFixed(1),                   color: "text-stone-300"  },
          { label: "Index Justice Fiscale (/10)", value: `${data.avg_estimated_taxjustice_index.toFixed(2)}/10`, color: "text-amber-400" },
          { label: "Score Évasion Moyen",        value: avgEvasionDisplay,                               color: "text-red-400"   },
        ].map(({ label, value, color }) => (
          <div
            key={label}
            className="bg-slate-900 border border-red-900/30 rounded-xl p-3 text-center"
          >
            <div className={`text-xl font-bold ${color}`}>{value}</div>
            <div className="text-xs text-stone-500 mt-0.5">{label}</div>
          </div>
        ))}
      </div>

      {/* gauge rings */}
      <div className="bg-slate-900 border border-red-900/30 rounded-xl p-5">
        <div className="text-xs text-stone-400 font-medium mb-4 uppercase tracking-wide">
          Scores Moyens par Dimension
        </div>
        <div className="grid grid-cols-4 gap-4">
          <GaugeRing value={avgEvasion}    label="Évasion"   color="#ef4444" />
          <GaugeRing value={avgAvoidance}  label="Évitement" color="#dc2626" />
          <GaugeRing value={avgOffshore}   label="Offshore"  color="#b91c1c" />
          <GaugeRing value={avgInequality} label="Inégalité" color="#f97316" />
        </div>
      </div>

      {/* distribution bars */}
      <div className="bg-slate-900 border border-red-900/30 rounded-xl p-5 grid grid-cols-1 md:grid-cols-2 gap-5">
        <DistBar
          title="Distribution des Risques"
          counts={data.risk_distribution}
          colors={RISK_COLOR}
        />
        <DistBar
          title="Distribution des Patrons"
          counts={data.pattern_distribution}
          colors={PAT_COLOR}
        />
        <DistBar
          title="Risque par Pays (échantillon)"
          counts={Object.fromEntries(
            entities.reduce((acc, e) => {
              acc.set(e.country, (acc.get(e.country) || 0) + e.composite_score / entities.length);
              return acc;
            }, new Map<string, number>()),
          )}
          colors={{}}
        />
        <DistBar
          title="Entités par Secteur"
          counts={entities.reduce(
            (acc, e) => ({ ...acc, [e.sector]: (acc[e.sector] || 0) + 1 }),
            {} as Record<string, number>,
          )}
          colors={{}}
        />
      </div>

      {/* filter pills */}
      <div className="flex flex-wrap gap-2 items-center">
        <span className="text-xs text-stone-500 mr-1">Risque:</span>
        {riskPills.map((r) => (
          <button
            key={r}
            onClick={() => setSelectedRisk(r)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${
              selectedRisk === r
                ? "bg-red-900 border-red-700 text-white"
                : "bg-slate-900 border-slate-700 text-stone-400 hover:text-white"
            }`}
          >
            {r === "all" ? "Tous" : r}
          </button>
        ))}
        <span className="w-px h-5 self-center bg-slate-700" />
        <span className="text-xs text-stone-500 mr-1">Pays:</span>
        {countryPills.map((c) => (
          <button
            key={c}
            onClick={() => setSelectedCountry(c)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${
              selectedCountry === c
                ? "bg-red-900 border-red-700 text-white"
                : "bg-slate-900 border-slate-700 text-stone-400 hover:text-white"
            }`}
          >
            {c === "all" ? "Tous pays" : c}
          </button>
        ))}
      </div>

      {/* entity cards grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {filtered.map((e) => (
          <div
            key={e.entity_id}
            onClick={() => setSelectedEntity(e)}
            className="bg-slate-900 border border-red-900/30 rounded-xl p-4 cursor-pointer hover:border-red-700 transition-colors"
          >
            <div className="flex items-start justify-between mb-1">
              <span className="font-bold text-white text-sm">{e.entity_id}</span>
              <span className="text-xs text-stone-400">{e.country}</span>
            </div>
            <div className="text-sm text-red-300 font-medium mb-1 leading-snug">
              {e.name}
            </div>
            <div className="text-xs text-stone-400 mb-2">{e.sector}</div>
            <div className="flex gap-1 mb-3 flex-wrap">
              <span
                className={`px-2 py-0.5 rounded text-xs font-medium ${
                  RISK_BADGE[e.risk_level] || "bg-slate-700 text-slate-300"
                }`}
              >
                {e.risk_level}
              </span>
            </div>
            <div className="text-2xl font-black text-white mb-0.5">
              {e.composite_score.toFixed(1)}
            </div>
            <div className="text-xs text-stone-500 mb-2">
              Index: {e.estimated_taxjustice_index.toFixed(2)}/10
            </div>
            <div
              className={`text-xs font-medium mb-2 ${
                PAT_BADGE[e.primary_pattern]
                  ? "px-1.5 py-0.5 rounded inline-block " + PAT_BADGE[e.primary_pattern]
                  : "text-stone-400"
              }`}
            >
              {e.primary_pattern}
            </div>
            <div className="text-xs text-stone-500 leading-snug line-clamp-2 mt-1">
              {e.key_signals[0]}
            </div>
          </div>
        ))}
      </div>

      {/* footer: data sources */}
      <div className="text-xs text-stone-600 text-center py-2">
        Sources: {data.data_sources?.join(" · ")}
      </div>
    </div>
  );
}
