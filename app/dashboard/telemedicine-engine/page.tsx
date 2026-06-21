"use client";
import { useEffect, useState } from "react";

type TLMEntity = {
  id: string;
  name: string;
  country: string;
  sector: string;
  composite_score: number;
  access_score: number;
  quality_score: number;
  security_score: number;
  adoption_score: number;
  risk_level: string;
  primary_pattern: string;
  pattern_severity: string;
  key_signals: string[];
  estimated_telemedicine_index: number;
  last_updated: string;
};

type TLMSummary = {
  total_entities: number;
  avg_composite: number;
  risk_distribution: Record<string, number>;
  pattern_distribution: Record<string, number>;
  top_risk_entities: Array<{ id: string; name: string; composite_score: number; risk_level: string }>;
  critical_alerts: string[];
  last_analysis: string;
  engine_version: string;
  domain: string;
  confidence_score: number;
  data_sources: string[];
  entities: TLMEntity[];
  avg_estimated_telemedicine_index: number;
};

type APIResponse = TLMSummary & { digital_seal?: unknown };

const RISK_COLORS: Record<string, string> = {
  critique: "#ef4444",
  "élevé": "#f97316",
  "modéré": "#eab308",
  faible: "#22c55e",
};

const RISK_BADGE: Record<string, string> = {
  critique: "bg-red-950 text-red-400 border border-red-700/40",
  "élevé": "bg-orange-950 text-orange-400 border border-orange-700/40",
  "modéré": "bg-yellow-950 text-yellow-400 border border-yellow-700/40",
  faible: "bg-emerald-950 text-emerald-400 border border-emerald-700/40",
};

const PATTERN_COLORS: Record<string, string> = {
  "Désert Médical Numérique": "#ef4444",
  "Fraude Téléconsultation": "#f97316",
  "Faille Sécurité Données Santé": "#8b5cf6",
  "Adoption Insuffisante": "#eab308",
  "Qualité Consultation Dégradée": "#22c55e",
};

const PATTERN_ACTIONS: Record<string, string> = {
  "Désert Médical Numérique":
    "Déploiement d'urgence d'infrastructures de télémédecine dans les zones non desservies. Partenariats avec les opérateurs télécoms pour étendre la couverture réseau. Programme d'équipement en dispositifs médicaux connectés subventionnés.",
  "Fraude Téléconsultation":
    "Audit immédiat des plateformes de téléconsultation et renforcement des contrôles d'identité. Mise en place d'un système de vérification biométrique des praticiens. Signalement aux autorités de santé compétentes.",
  "Faille Sécurité Données Santé":
    "Mise en conformité RGPD et chiffrement bout-en-bout des dossiers médicaux numériques. Déploiement d'une authentification multifacteur pour tous les accès distants. Audit de sécurité trimestriel des systèmes d'information de santé.",
  "Adoption Insuffisante":
    "Campagne de sensibilisation et programme de formation des professionnels de santé. Négociation de remboursements avec les organismes de sécurité sociale. Simplification des interfaces utilisateurs et accompagnement au changement.",
  "Qualité Consultation Dégradée":
    "Révision des protocoles de consultation à distance et amélioration des interfaces cliniques. Investissement dans des infrastructures réseau à faible latence. Formation des praticiens aux bonnes pratiques de la téléconsultation.",
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
          cx="44"
          cy="44"
          r={r}
          fill="none"
          stroke={color}
          strokeWidth="8"
          strokeDasharray={circ}
          strokeDashoffset={fill}
          strokeLinecap="round"
          transform="rotate(-90 44 44)"
        />
        <text x="44" y="49" textAnchor="middle" fill="white" fontSize="13" fontWeight="bold">
          {Math.round(value)}
        </text>
      </svg>
      <span className="text-xs text-stone-400 text-center">{label}</span>
    </div>
  );
}

function DistBar({
  label,
  value,
  max,
  color,
}: {
  label: string;
  value: number;
  max: number;
  color: string;
}) {
  const pct = max > 0 ? (value / max) * 100 : 0;
  return (
    <div className="flex items-center gap-3">
      <span className="text-xs text-slate-400 w-44 truncate shrink-0">{label}</span>
      <div className="flex-1 h-2 bg-slate-800 rounded overflow-hidden">
        <div
          className="h-2 rounded transition-all"
          style={{ width: `${pct}%`, backgroundColor: color }}
        />
      </div>
      <span className="text-xs text-slate-300 w-6 text-right shrink-0">{value}</span>
    </div>
  );
}

function DetailModal({ entity, onClose }: { entity: TLMEntity; onClose: () => void }) {
  const [tab, setTab] = useState<"scores" | "signaux" | "actions">("scores");

  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
    };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [onClose]);

  const scores: Array<[string, number, string]> = [
    ["Accès", entity.access_score, "#06b6d4"],
    ["Qualité", entity.quality_score, "#3b82f6"],
    ["Sécurité", entity.security_score, "#8b5cf6"],
    ["Adoption", entity.adoption_score, "#10b981"],
  ];

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/80"
      onClick={onClose}
    >
      <div
        className="bg-slate-950 border border-cyan-700/30 rounded-xl w-full max-w-lg p-6 shadow-2xl"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="flex items-start justify-between mb-4">
          <div>
            <div className="flex items-center gap-2">
              <span className="text-lg font-bold text-white">{entity.id}</span>
              <span
                className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[entity.risk_level] || "bg-slate-700 text-slate-300"}`}
              >
                {entity.risk_level}
              </span>
            </div>
            <div className="text-cyan-400 text-sm font-medium mt-0.5">{entity.name}</div>
            <div className="text-slate-500 text-xs mt-0.5">
              {entity.country} · {entity.sector}
            </div>
          </div>
          <button
            onClick={onClose}
            className="text-slate-500 hover:text-white text-xl leading-none mt-1"
          >
            ✕
          </button>
        </div>

        <div className="flex gap-2 mb-4">
          {(["scores", "signaux", "actions"] as const).map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`px-3 py-1 rounded text-xs font-medium transition-colors capitalize ${
                tab === t
                  ? "bg-cyan-900 text-white border border-cyan-700"
                  : "bg-slate-900 text-slate-400 border border-slate-700 hover:text-white"
              }`}
            >
              {t === "scores" ? "Scores" : t === "signaux" ? "Signaux" : "Actions"}
            </button>
          ))}
        </div>

        {tab === "scores" && (
          <div className="space-y-3">
            {scores.map(([label, value, color]) => (
              <div key={label} className="bg-slate-900 border border-cyan-700/20 rounded-lg p-3">
                <div className="flex items-center justify-between mb-1.5">
                  <span className="text-xs text-slate-400">{label}</span>
                  <span className="text-sm font-bold text-white">{value.toFixed(1)}</span>
                </div>
                <div className="h-2 bg-slate-800 rounded overflow-hidden">
                  <div
                    className="h-2 rounded"
                    style={{ width: `${Math.min(value, 100)}%`, backgroundColor: color }}
                  />
                </div>
              </div>
            ))}
            <div className="bg-slate-900 border border-cyan-700/20 rounded-lg p-3 flex items-center justify-between">
              <span className="text-xs text-slate-400">Score Composite</span>
              <span className="text-2xl font-black text-white">
                {entity.composite_score.toFixed(2)}
              </span>
            </div>
            <div className="bg-slate-900 border border-cyan-700/20 rounded-lg p-3 flex items-center justify-between">
              <span className="text-xs text-slate-400">Index Télémédecine</span>
              <span className="text-lg font-bold text-cyan-400">
                {entity.estimated_telemedicine_index.toFixed(2)} / 10
              </span>
            </div>
          </div>
        )}

        {tab === "signaux" && (
          <div className="space-y-3">
            <div className="bg-slate-900 border border-cyan-700/20 rounded-lg p-3">
              <div className="text-xs text-slate-400 mb-2">Patron Détecté</div>
              <div
                className="text-sm font-semibold"
                style={{ color: PATTERN_COLORS[entity.primary_pattern] || "#94a3b8" }}
              >
                {entity.primary_pattern}
              </div>
            </div>
            <div className="space-y-2">
              {entity.key_signals.map((signal, i) => (
                <div
                  key={i}
                  className="bg-slate-900 border border-cyan-700/20 rounded-lg p-3 flex gap-3"
                >
                  <span className="text-cyan-500 text-xs font-bold mt-0.5 shrink-0">
                    {String(i + 1).padStart(2, "0")}
                  </span>
                  <span className="text-sm text-slate-300 leading-relaxed">{signal}</span>
                </div>
              ))}
            </div>
          </div>
        )}

        {tab === "actions" && (
          <div className="space-y-3">
            <div className="bg-slate-900 border border-cyan-700/20 rounded-lg p-4">
              <div className="text-xs text-slate-400 mb-2">Patron</div>
              <div
                className="text-sm font-semibold mb-3"
                style={{ color: PATTERN_COLORS[entity.primary_pattern] || "#94a3b8" }}
              >
                {entity.primary_pattern}
              </div>
              <div className="text-xs text-slate-400 mb-1">Actions Recommandées</div>
              <div className="text-sm text-slate-200 leading-relaxed">
                {PATTERN_ACTIONS[entity.primary_pattern] ||
                  "Surveillance continue et rapport d'analyse approfondie recommandés."}
              </div>
            </div>
            <div className="bg-slate-900 border border-cyan-700/20 rounded-lg p-3">
              <div className="text-xs text-slate-400 mb-1">Mise à jour</div>
              <div className="text-sm text-slate-300">{entity.last_updated}</div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function TelemedicineDashboard() {
  const [data, setData] = useState<APIResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [riskFilter, setRiskFilter] = useState<string>("Tous");
  const [countryFilter, setCountryFilter] = useState<string>("Tous");
  const [selected, setSelected] = useState<TLMEntity | null>(null);

  useEffect(() => {
    fetch("/api/telemedicine-engine")
      .then((r) => {
        if (!r.ok) throw new Error(`HTTP ${r.status}`);
        return r.json();
      })
      .then((d: APIResponse) => {
        setData(d);
        setLoading(false);
      })
      .catch((err: unknown) => {
        setError(err instanceof Error ? err.message : "Erreur de chargement");
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center">
        <div className="text-cyan-400 text-lg animate-pulse">
          Initialisation du Telemedicine Engine...
        </div>
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center">
        <div className="bg-red-950 border border-red-700/40 rounded-xl p-8 text-center max-w-md">
          <div className="text-red-400 text-xl font-bold mb-2">Erreur de chargement</div>
          <div className="text-red-300/70 text-sm">{error || "Données indisponibles"}</div>
        </div>
      </div>
    );
  }

  const entities = data.entities;
  const countries = ["Tous", ...Array.from(new Set(entities.map((e) => e.country))).sort()];
  const riskLevels = ["Tous", "critique", "élevé", "modéré", "faible"];

  const filtered = entities.filter(
    (e) =>
      (riskFilter === "Tous" || e.risk_level === riskFilter) &&
      (countryFilter === "Tous" || e.country === countryFilter)
  );

  const avgAccess =
    entities.reduce((s, e) => s + e.access_score, 0) / (entities.length || 1);
  const avgQuality =
    entities.reduce((s, e) => s + e.quality_score, 0) / (entities.length || 1);
  const avgSecurity =
    entities.reduce((s, e) => s + e.security_score, 0) / (entities.length || 1);
  const avgAdoption =
    entities.reduce((s, e) => s + e.adoption_score, 0) / (entities.length || 1);

  const critiqueCount = data.risk_distribution["critique"] || 0;
  const eleveCount = data.risk_distribution["élevé"] || 0;

  const maxRisk = Math.max(...Object.values(data.risk_distribution));
  const maxPattern = Math.max(...Object.values(data.pattern_distribution));

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {selected && (
        <DetailModal entity={selected} onClose={() => setSelected(null)} />
      )}

      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-cyan-400">Telemedicine Engine</h1>
        <p className="text-slate-400 text-sm mt-1">
          Intelligence d&apos;analyse télémédecine · Accès · Qualité · Sécurité · Adoption — Caelum Partners
        </p>
        <div className="flex gap-3 mt-2 text-xs text-slate-500">
          <span>Dernière analyse : {data.last_analysis}</span>
          <span>·</span>
          <span>Version {data.engine_version}</span>
          <span>·</span>
          <span>Confiance : {Math.round(data.confidence_score * 100)}%</span>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {[
          ["Total Entités", data.total_entities, "text-cyan-400"],
          ["Critique", critiqueCount, "text-red-400"],
          ["Élevé", eleveCount, "text-orange-400"],
          ["Composite Moyen", data.avg_composite.toFixed(2), "text-blue-400"],
          [
            "Index Télémédecine",
            `${data.avg_estimated_telemedicine_index.toFixed(2)}/10`,
            "text-cyan-300",
          ],
          ["Score Accès Moyen", Math.round(avgAccess * 10) / 10, "text-emerald-400"],
        ].map(([label, value, color]) => (
          <div
            key={String(label)}
            className="bg-slate-900 border border-cyan-700/30 rounded-xl p-3 text-center"
          >
            <div className={`text-xl font-bold ${color}`}>{value}</div>
            <div className="text-xs text-slate-500 mt-0.5 leading-tight">{label}</div>
          </div>
        ))}
      </div>

      {/* Gauge Rings */}
      <div className="bg-slate-900 border border-cyan-700/30 rounded-xl p-5">
        <div className="text-xs text-slate-400 font-medium mb-4">Scores Moyens par Dimension</div>
        <div className="grid grid-cols-4 gap-4">
          <GaugeRing value={avgAccess} label="Accès" color="#06b6d4" />
          <GaugeRing value={avgQuality} label="Qualité" color="#3b82f6" />
          <GaugeRing value={avgSecurity} label="Sécurité" color="#8b5cf6" />
          <GaugeRing value={avgAdoption} label="Adoption" color="#10b981" />
        </div>
      </div>

      {/* Distribution Bars */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="bg-slate-900 border border-cyan-700/30 rounded-xl p-5 space-y-3">
          <div className="text-xs text-slate-400 font-medium mb-3">Distribution par Niveau de Risque</div>
          {Object.entries(data.risk_distribution).map(([k, v]) => (
            <DistBar
              key={k}
              label={k}
              value={v}
              max={maxRisk}
              color={RISK_COLORS[k] || "#475569"}
            />
          ))}
        </div>
        <div className="bg-slate-900 border border-cyan-700/30 rounded-xl p-5 space-y-3">
          <div className="text-xs text-slate-400 font-medium mb-3">Distribution par Patron</div>
          {Object.entries(data.pattern_distribution).map(([k, v]) => (
            <DistBar
              key={k}
              label={k}
              value={v}
              max={maxPattern}
              color={PATTERN_COLORS[k] || "#475569"}
            />
          ))}
        </div>
      </div>

      {/* Filter Pills */}
      <div className="flex flex-wrap gap-2 items-center">
        <span className="text-xs text-slate-500 font-medium">Risque:</span>
        {riskLevels.map((r) => (
          <button
            key={r}
            onClick={() => setRiskFilter(r)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${
              riskFilter === r
                ? "bg-cyan-900 border-cyan-700 text-white"
                : "bg-slate-900 border-cyan-700/30 text-slate-400 hover:text-white"
            }`}
          >
            {r}
          </button>
        ))}
        <span className="w-px h-5 self-center bg-cyan-700/30 mx-1" />
        <span className="text-xs text-slate-500 font-medium">Pays:</span>
        {countries.map((c) => (
          <button
            key={c}
            onClick={() => setCountryFilter(c)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${
              countryFilter === c
                ? "bg-blue-900 border-blue-700 text-white"
                : "bg-slate-900 border-cyan-700/30 text-slate-400 hover:text-white"
            }`}
          >
            {c}
          </button>
        ))}
      </div>

      {/* Entity Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {filtered.map((e) => (
          <div
            key={e.id}
            onClick={() => setSelected(e)}
            className="bg-slate-900 border border-cyan-700/30 rounded-xl p-4 cursor-pointer hover:border-cyan-500 transition-all hover:shadow-lg hover:shadow-cyan-900/20"
          >
            <div className="flex items-start justify-between mb-2">
              <div>
                <span className="font-bold text-white text-sm">{e.id}</span>
                <div className="text-xs text-slate-500 mt-0.5">
                  {e.country} · {e.sector}
                </div>
              </div>
              <span
                className={`px-2 py-0.5 rounded text-xs font-medium shrink-0 ${RISK_BADGE[e.risk_level] || "bg-slate-700 text-slate-300"}`}
              >
                {e.risk_level}
              </span>
            </div>
            <div className="text-sm font-semibold text-cyan-300 mb-2 leading-tight">{e.name}</div>
            <div
              className="text-xs font-medium mb-3"
              style={{ color: PATTERN_COLORS[e.primary_pattern] || "#94a3b8" }}
            >
              {e.primary_pattern}
            </div>
            <div className="flex items-end justify-between mb-3">
              <div>
                <div className="text-3xl font-black text-white leading-none">
                  {e.composite_score.toFixed(1)}
                </div>
                <div className="text-xs text-slate-500 mt-0.5">score composite</div>
              </div>
              <div className="text-right">
                <div className="text-lg font-bold text-cyan-400">
                  {e.estimated_telemedicine_index.toFixed(2)}
                </div>
                <div className="text-xs text-slate-500">/ 10</div>
              </div>
            </div>
            <div className="grid grid-cols-4 gap-1 mb-3">
              {[
                ["A", e.access_score, "#06b6d4"],
                ["Q", e.quality_score, "#3b82f6"],
                ["S", e.security_score, "#8b5cf6"],
                ["Ad", e.adoption_score, "#10b981"],
              ].map(([label, val, color]) => (
                <div key={String(label)} className="text-center">
                  <div className="text-xs font-bold" style={{ color: String(color) }}>
                    {Number(val).toFixed(0)}
                  </div>
                  <div className="text-xs text-slate-600">{label}</div>
                </div>
              ))}
            </div>
            <div className="text-xs text-slate-500 leading-relaxed line-clamp-2">
              {e.key_signals[0]}
            </div>
          </div>
        ))}
      </div>

      {filtered.length === 0 && (
        <div className="text-center text-slate-500 py-12">
          Aucune entité ne correspond aux filtres sélectionnés.
        </div>
      )}

      {/* Critical Alerts */}
      {data.critical_alerts.length > 0 && (
        <div className="bg-red-950/30 border border-red-700/40 rounded-xl p-5">
          <div className="text-sm font-semibold text-red-400 mb-3">
            Alertes Critiques ({data.critical_alerts.length})
          </div>
          <div className="space-y-2">
            {data.critical_alerts.map((alert, i) => (
              <div key={i} className="flex gap-2 items-start text-xs text-red-300/80">
                <span className="text-red-500 shrink-0 mt-0.5">⚠</span>
                <span>{alert}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Data Sources */}
      <div className="flex gap-2 flex-wrap items-center">
        <span className="text-xs text-slate-500">Sources :</span>
        {data.data_sources.map((src) => (
          <span
            key={src}
            className="px-2 py-0.5 rounded bg-slate-900 border border-cyan-700/20 text-xs text-slate-400"
          >
            {src}
          </span>
        ))}
      </div>
    </div>
  );
}
