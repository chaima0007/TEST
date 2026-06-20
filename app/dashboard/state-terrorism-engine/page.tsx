"use client";
import { useState, useEffect } from "react";

const RC: Record<string, string> = {
  critique: "text-red-400",
  "élevé": "text-orange-400",
  modéré: "text-yellow-400",
  faible: "text-emerald-400",
};
const RB: Record<string, string> = {
  critique: "border-red-500/30 bg-red-500/10",
  "élevé": "border-orange-500/30 bg-orange-500/10",
  modéré: "border-yellow-500/30 bg-yellow-500/10",
  faible: "border-emerald-500/30 bg-emerald-500/10",
};

type STEntity = {
  entity_id: string;
  name: string;
  country: string;
  sector: string;
  composite_score: number;
  extrajudicial_killings_score: number;
  forced_disappearances_score: number;
  systematic_torture_score: number;
  political_mass_imprisonment_score: number;
  risk_level: string;
  primary_pattern: string;
  key_signals: string[];
  estimated_state_terrorism_index: number;
  last_updated: string;
};

type ApiResponse = {
  data?: STEntity[];
  [key: string]: unknown;
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
      <span className="text-xs text-[#dc2626]/70 text-center">{label}</span>
    </div>
  );
}

function DistBar({ items }: { items: { label: string; value: number; color: string }[] }) {
  const total = items.reduce((s, i) => s + i.value, 0) || 1;
  return (
    <div className="w-full">
      <div className="flex h-2 rounded-full overflow-hidden gap-0.5">
        {items.map((item) => (
          <div
            key={item.label}
            style={{ width: `${(item.value / total) * 100}%`, background: item.color }}
            title={`${item.label}: ${item.value}`}
          />
        ))}
      </div>
      <div className="flex gap-3 mt-1 flex-wrap">
        {items.map((item) => (
          <span key={item.label} className="text-xs text-slate-400 flex items-center gap-1">
            <span className="inline-block w-2 h-2 rounded-full" style={{ background: item.color }} />
            {item.label} ({item.value})
          </span>
        ))}
      </div>
    </div>
  );
}

const RISK_COLORS: Record<string, string> = {
  critique: "#ef4444",
  "élevé": "#f97316",
  modéré: "#eab308",
  faible: "#10b981",
};

const PATTERN_COLORS: Record<string, string> = {
  default: "#dc2626",
};

function patternColor(pattern: string): string {
  return PATTERN_COLORS[pattern] ?? PATTERN_COLORS.default;
}

function DetailModal({ entity, onClose }: { entity: STEntity; onClose: () => void }) {
  const [tab, setTab] = useState<"scores" | "signaux" | "actions">("scores");
  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm p-4"
      onClick={onClose}
    >
      <div
        className="bg-slate-900 border border-[#dc2626]/20 rounded-2xl w-full max-w-2xl max-h-[90vh] overflow-y-auto shadow-2xl"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="p-6 border-b border-slate-800 flex items-start justify-between gap-4">
          <div>
            <h2 className="text-xl font-bold text-white">{entity.name}</h2>
            <p className="text-sm text-slate-400 mt-0.5">
              {entity.country} · {entity.sector}
            </p>
          </div>
          <button
            onClick={onClose}
            className="text-slate-400 hover:text-white transition-colors text-2xl leading-none"
          >
            ×
          </button>
        </div>
        <div className="flex border-b border-slate-800">
          {(["scores", "signaux", "actions"] as const).map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`flex-1 py-3 text-sm font-medium transition-colors capitalize ${
                tab === t
                  ? "text-[#dc2626] border-b-2 border-[#dc2626]"
                  : "text-slate-400 hover:text-white"
              }`}
            >
              {t}
            </button>
          ))}
        </div>
        <div className="p-6">
          {tab === "scores" && (
            <div className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div className="bg-slate-800/50 rounded-xl p-4 text-center">
                  <div className="text-3xl font-bold text-[#dc2626]">
                    {entity.composite_score.toFixed(1)}
                  </div>
                  <div className="text-xs text-slate-400 mt-1">Score Composite</div>
                </div>
                <div className="bg-slate-800/50 rounded-xl p-4 text-center">
                  <div className="text-3xl font-bold text-[#dc2626]">
                    {entity.estimated_state_terrorism_index.toFixed(1)}
                  </div>
                  <div className="text-xs text-slate-400 mt-1">Index Terrorisme État</div>
                </div>
              </div>
              <div className="grid grid-cols-2 gap-3">
                {[
                  { label: "Exécutions Extrajudiciaires", value: entity.extrajudicial_killings_score },
                  { label: "Disparitions Forcées", value: entity.forced_disappearances_score },
                  { label: "Torture Systématique", value: entity.systematic_torture_score },
                  { label: "Emprisonnements Masse", value: entity.political_mass_imprisonment_score },
                ].map((s) => (
                  <div key={s.label} className="bg-slate-800/50 rounded-lg p-3">
                    <div className="text-lg font-bold text-white">{s.value.toFixed(1)}</div>
                    <div className="text-xs text-slate-400">{s.label}</div>
                  </div>
                ))}
              </div>
              <div className={`rounded-lg p-3 border ${RB[entity.risk_level] ?? "border-slate-700 bg-slate-800/30"}`}>
                <span className={`text-sm font-semibold capitalize ${RC[entity.risk_level] ?? "text-slate-300"}`}>
                  Niveau de risque : {entity.risk_level}
                </span>
              </div>
            </div>
          )}
          {tab === "signaux" && (
            <div className="space-y-4">
              <div className="bg-slate-800/50 rounded-xl p-4">
                <div className="text-xs text-slate-400 mb-1">Schéma Principal</div>
                <div
                  className="text-sm font-medium px-2 py-1 rounded inline-block"
                  style={{ color: patternColor(entity.primary_pattern), background: `${patternColor(entity.primary_pattern)}18` }}
                >
                  {entity.primary_pattern}
                </div>
              </div>
              <div className="bg-slate-800/50 rounded-xl p-4">
                <div className="text-xs text-slate-400 mb-3">Signaux Détectés</div>
                <ul className="space-y-2">
                  {entity.key_signals.map((sig, i) => (
                    <li key={i} className="flex items-start gap-2 text-sm text-slate-300">
                      <span className="mt-1 w-1.5 h-1.5 rounded-full bg-[#dc2626] flex-shrink-0" />
                      {sig}
                    </li>
                  ))}
                </ul>
              </div>
              <div className="text-xs text-slate-500">
                Dernière mise à jour : {new Date(entity.last_updated).toLocaleDateString("fr-FR")}
              </div>
            </div>
          )}
          {tab === "actions" && (
            <div className="space-y-3">
              {[
                "Saisir la Cour Pénale Internationale pour crimes contre l'humanité",
                "Documenter les preuves pour les juridictions universelles",
                "Alerter les mécanismes de protection des droits humains de l'ONU",
                "Coordonner avec les ONG de défense des droits fondamentaux",
                "Activer les sanctions internationales ciblées contre les responsables",
              ].map((action, i) => (
                <div
                  key={i}
                  className="flex items-center gap-3 bg-slate-800/50 rounded-lg p-3 text-sm text-slate-300"
                >
                  <span className="w-6 h-6 rounded-full bg-[#dc2626]/20 text-[#dc2626] flex items-center justify-center text-xs font-bold flex-shrink-0">
                    {i + 1}
                  </span>
                  {action}
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default function StateTerrorismEnginePage() {
  const [entities, setEntities] = useState<STEntity[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filter, setFilter] = useState("tous");
  const [selected, setSelected] = useState<STEntity | null>(null);

  useEffect(() => {
    setLoading(true);
    fetch("/api/state-terrorism-engine")
      .then((r) => r.json())
      .then((json: ApiResponse) => {
        const rows = json?.data ?? (Array.isArray(json) ? json : []);
        setEntities(rows as STEntity[]);
        setLoading(false);
      })
      .catch(() => {
        setError("Impossible de charger les données.");
        setLoading(false);
      });
  }, []);

  const filtered =
    filter === "tous" ? entities : entities.filter((e) => e.risk_level === filter);

  const avg = (arr: number[]) =>
    arr.length ? arr.reduce((a, b) => a + b, 0) / arr.length : 0;

  const avgComposite = avg(entities.map((e) => e.composite_score));
  const avgIndex = avg(entities.map((e) => e.estimated_state_terrorism_index));
  const countCritique = entities.filter((e) => e.risk_level === "critique").length;
  const countEleve = entities.filter((e) => e.risk_level === "élevé").length;
  const countModFaible = entities.filter(
    (e) => e.risk_level === "modéré" || e.risk_level === "faible"
  ).length;

  const avgExtrajudicial = avg(entities.map((e) => e.extrajudicial_killings_score));
  const avgDisappearances = avg(entities.map((e) => e.forced_disappearances_score));
  const avgTorture = avg(entities.map((e) => e.systematic_torture_score));
  const avgImprisonment = avg(entities.map((e) => e.political_mass_imprisonment_score));

  const distItems = [
    { label: "Critique", value: countCritique, color: "#ef4444" },
    { label: "Élevé", value: countEleve, color: "#f97316" },
    { label: "Modéré/Faible", value: countModFaible, color: "#10b981" },
  ];

  const filters = [
    { key: "tous", label: "Tous" },
    { key: "critique", label: "Critique" },
    { key: "élevé", label: "Élevé" },
    { key: "modéré", label: "Modéré" },
    { key: "faible", label: "Faible" },
  ];

  return (
    <div className="min-h-screen bg-slate-950 text-white p-6">
      {selected && (
        <DetailModal entity={selected} onClose={() => setSelected(null)} />
      )}

      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-2">
          <div className="w-2 h-8 rounded-full bg-[#dc2626]" />
          <h1 className="text-2xl font-bold text-white">State Terrorism Engine</h1>
        </div>
        <p className="text-slate-400 ml-5">
          Terrorisme d&apos;État, exécutions extrajudiciaires, disparitions forcées et torture institutionnalisée — Caelum Partners · Chaima Mhadbi, Fondatrice, Bruxelles
        </p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4 mb-8">
        {[
          { label: "Entités Analysées", value: entities.length, suffix: "" },
          { label: "Score Moyen", value: avgComposite.toFixed(1), suffix: "" },
          { label: "Index Terrorisme État Moyen", value: avgIndex.toFixed(1), suffix: "" },
          { label: "Critique", value: countCritique, suffix: "" },
          { label: "Élevé", value: countEleve, suffix: "" },
          { label: "Modéré/Faible", value: countModFaible, suffix: "" },
        ].map((kpi) => (
          <div
            key={kpi.label}
            className="bg-slate-900 border border-[#dc2626]/10 rounded-xl p-4 text-center"
          >
            <div className="text-2xl font-bold text-[#dc2626]">
              {kpi.value}{kpi.suffix}
            </div>
            <div className="text-xs text-slate-400 mt-1">{kpi.label}</div>
          </div>
        ))}
      </div>

      {/* Gauge Rings */}
      <div className="bg-slate-900 border border-[#dc2626]/10 rounded-2xl p-6 mb-8">
        <h2 className="text-sm font-semibold text-slate-300 mb-6">
          Scores Moyens par Dimension
        </h2>
        <div className="flex flex-wrap justify-around gap-6">
          <GaugeRing value={avgExtrajudicial} label="Exécutions Extrajudiciaires" color="#dc2626" />
          <GaugeRing value={avgDisappearances} label="Disparitions Forcées" color="#7c3aed" />
          <GaugeRing value={avgTorture} label="Torture Systématique" color="#0891b2" />
          <GaugeRing value={avgImprisonment} label="Emprisonnements Masse" color="#b45309" />
        </div>
      </div>

      {/* Distribution */}
      <div className="bg-slate-900 border border-[#dc2626]/10 rounded-2xl p-6 mb-8">
        <h2 className="text-sm font-semibold text-slate-300 mb-4">
          Distribution des Niveaux de Risque
        </h2>
        <DistBar items={distItems} />
      </div>

      {/* Filter pills */}
      <div className="flex gap-2 flex-wrap mb-6">
        {filters.map((f) => (
          <button
            key={f.key}
            onClick={() => setFilter(f.key)}
            className={`px-4 py-1.5 rounded-full text-sm font-medium transition-colors ${
              filter === f.key
                ? "bg-[#dc2626] text-white"
                : "bg-slate-800 text-slate-400 hover:text-white"
            }`}
          >
            {f.label}
          </button>
        ))}
      </div>

      {/* Entity Grid */}
      {loading ? (
        <div className="text-center text-slate-400 py-20">Chargement...</div>
      ) : error ? (
        <div className="text-center text-red-400 py-20">{error}</div>
      ) : filtered.length === 0 ? (
        <div className="text-center text-slate-500 py-20">Aucune entité trouvée.</div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {filtered.map((entity) => (
            <div
              key={entity.entity_id}
              onClick={() => setSelected(entity)}
              className={`bg-slate-900 border rounded-xl p-5 cursor-pointer hover:border-[#dc2626]/40 transition-all ${
                RB[entity.risk_level] ?? "border-slate-700"
              }`}
            >
              <div className="flex items-start justify-between gap-2 mb-3">
                <div>
                  <h3 className="font-semibold text-white text-sm">{entity.name}</h3>
                  <p className="text-xs text-slate-400 mt-0.5">
                    {entity.country} · {entity.sector}
                  </p>
                </div>
                <span
                  className={`text-xs font-medium px-2 py-0.5 rounded-full border capitalize flex-shrink-0 ${
                    RB[entity.risk_level] ?? "border-slate-700"
                  } ${RC[entity.risk_level] ?? "text-slate-400"}`}
                >
                  {entity.risk_level}
                </span>
              </div>
              <div className="flex items-center gap-4 mb-3">
                <div className="text-center">
                  <div className="text-lg font-bold text-[#dc2626]">
                    {entity.composite_score.toFixed(1)}
                  </div>
                  <div className="text-xs text-slate-500">Score</div>
                </div>
                <div className="text-center">
                  <div className="text-lg font-bold text-[#dc2626]">
                    {entity.estimated_state_terrorism_index.toFixed(1)}
                  </div>
                  <div className="text-xs text-slate-500">Index STE</div>
                </div>
              </div>
              <div
                className="text-xs px-2 py-1 rounded inline-block"
                style={{
                  color: patternColor(entity.primary_pattern),
                  background: `${patternColor(entity.primary_pattern)}18`,
                }}
              >
                {entity.primary_pattern}
              </div>
              {entity.key_signals?.length > 0 && (
                <div className="mt-2 flex flex-wrap gap-1">
                  {entity.key_signals.slice(0, 2).map((sig, i) => (
                    <span
                      key={i}
                      className="text-xs bg-slate-800 text-slate-400 px-2 py-0.5 rounded"
                    >
                      {sig}
                    </span>
                  ))}
                  {entity.key_signals.length > 2 && (
                    <span className="text-xs text-slate-500">
                      +{entity.key_signals.length - 2}
                    </span>
                  )}
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
