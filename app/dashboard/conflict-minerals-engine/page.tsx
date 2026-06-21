"use client";
import { useState, useEffect } from "react";

const ACCENT = "#eab308";
const RC: Record<string,string> = { critique:"text-red-400","élevé":"text-orange-400",modéré:"text-yellow-400",faible:"text-emerald-400" };
const RB: Record<string,string> = { critique:"border-red-500/30 bg-red-500/10","élevé":"border-orange-500/30 bg-orange-500/10",modéré:"border-yellow-500/30 bg-yellow-500/10",faible:"border-emerald-500/30 bg-emerald-500/10" };

interface CMEEntity {
  id: string;
  name: string;
  country: string;
  sector: string;
  composite_score: number;
  armed_group_financing_scale_score: number;
  supply_chain_due_diligence_failure_score: number;
  civilian_exploitation_harm_score: number;
  corporate_accountability_gap_score: number;
  risk_level: string;
  primary_pattern: string;
  key_signals: string[];
  estimated_conflict_minerals_index: number;
  last_updated: string;
  [key: string]: unknown;
}

interface CMESummary {
  total_entities: number;
  avg_composite: number;
  avg_estimated_conflict_minerals_index: number;
  risk_distribution: Record<string, number>;
  pattern_distribution: Record<string, number>;
  confidence_score: number;
  critical_alerts: string[] | number;
  last_analysis: string;
  engine_version: string;
  data_sources: string[];
  entities: CMEEntity[];
}

interface CMEData {
  entities?: CMEEntity[];
  summary?: CMESummary;
  payload?: CMEData;
  [key: string]: unknown;
}

function GaugeRing({ value, max = 100 }: { value: number; max?: number }) {
  const r = 36;
  const circ = 2 * Math.PI * r;
  const pct = Math.min(Math.max(value / max, 0), 1);
  return (
    <svg width={88} height={88} viewBox="0 0 88 88">
      <circle cx="44" cy="44" r={r} fill="none" stroke="#1e293b" strokeWidth={8} />
      <circle
        cx="44" cy="44" r={r} fill="none" stroke={ACCENT} strokeWidth={8}
        strokeDasharray={`${pct * circ} ${circ}`} strokeLinecap="round"
        transform="rotate(-90 44 44)"
      />
      <text x="44" y="49" textAnchor="middle" fill="white" fontSize="13" fontWeight="bold">
        {value.toFixed(1)}
      </text>
    </svg>
  );
}

function DetailModal({ entity, onClose }: { entity: CMEEntity; onClose: () => void }) {
  const [tab, setTab] = useState(0);
  const tabs = ["Vue d'ensemble", "Indicateurs", "Analyse"];
  const rc = RC[entity.risk_level] ?? "text-slate-400";
  const rb = RB[entity.risk_level] ?? "border-slate-700/40 bg-slate-800/50";
  const scores = [
    { label: "Financement Armé", key: "armed_group_financing_scale_score" },
    { label: "Défaillance Chaîne", key: "supply_chain_due_diligence_failure_score" },
    { label: "Exploitation Civile", key: "civilian_exploitation_harm_score" },
    { label: "Gap Corporatif", key: "corporate_accountability_gap_score" },
  ];
  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm p-4"
      onClick={onClose}
    >
      <div
        className="bg-slate-900 border border-yellow-500/20 rounded-2xl w-full max-w-2xl max-h-[90vh] overflow-y-auto shadow-2xl"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="p-6 border-b border-slate-800 flex items-start justify-between gap-4">
          <div>
            <h2 className="text-xl font-bold text-white">{entity.name}</h2>
            <p className="text-sm text-slate-400 mt-0.5">{entity.country} &middot; {entity.sector}</p>
            <span className={`text-xs font-bold uppercase mt-1 inline-block ${rc}`}>{entity.risk_level}</span>
          </div>
          <button
            onClick={onClose}
            className="text-slate-400 hover:text-white transition-colors text-2xl leading-none"
          >
            &times;
          </button>
        </div>
        <div className="flex border-b border-slate-800">
          {tabs.map((t, i) => (
            <button
              key={t}
              onClick={() => setTab(i)}
              className={`flex-1 py-3 text-sm font-medium transition-colors ${
                tab === i
                  ? "border-b-2 text-white"
                  : "text-slate-500 hover:text-slate-300"
              }`}
              style={tab === i ? { borderColor: ACCENT, color: ACCENT } : {}}
            >
              {t}
            </button>
          ))}
        </div>
        <div className="p-6">
          {tab === 0 && (
            <div className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div className="bg-slate-800/50 rounded-xl p-4 text-center">
                  <div className="text-3xl font-bold" style={{ color: ACCENT }}>
                    {entity.composite_score.toFixed(1)}
                  </div>
                  <div className="text-xs text-slate-400 mt-1">Score Composite</div>
                </div>
                <div className="bg-slate-800/50 rounded-xl p-4 text-center">
                  <div className="text-3xl font-bold" style={{ color: ACCENT }}>
                    {entity.estimated_conflict_minerals_index.toFixed(1)}
                  </div>
                  <div className="text-xs text-slate-400 mt-1">Index Minerais Conflit</div>
                </div>
              </div>
              <div className="grid grid-cols-2 gap-3">
                {scores.map((s) => (
                  <div key={s.key} className="bg-slate-800/50 rounded-lg p-3">
                    <div className="text-lg font-bold text-white">
                      {typeof entity[s.key] === "number" ? (entity[s.key] as number).toFixed(1) : "—"}
                    </div>
                    <div className="text-xs text-slate-400">{s.label}</div>
                  </div>
                ))}
              </div>
              <div className={`rounded-lg p-3 border ${rb}`}>
                <span className={`text-sm font-semibold capitalize ${rc}`}>
                  Niveau de risque&nbsp;: {entity.risk_level}
                </span>
              </div>
            </div>
          )}
          {tab === 1 && (
            <div className="flex flex-col items-center gap-4 py-4">
              <GaugeRing value={entity.estimated_conflict_minerals_index} max={10} />
              <div className="text-center">
                <div className="text-3xl font-bold" style={{ color: ACCENT }}>
                  {entity.estimated_conflict_minerals_index.toFixed(2)}
                </div>
                <div className="text-sm text-slate-500 mt-1">Index Minerais Conflit</div>
              </div>
              <div className="w-full space-y-2 mt-2">
                {scores.map((s) => (
                  <div key={s.key} className="flex items-center justify-between rounded-lg border border-slate-700/40 bg-slate-800/50 px-4 py-2">
                    <span className="text-sm text-slate-400">{s.label}</span>
                    <span className="font-mono text-sm text-slate-200">
                      {typeof entity[s.key] === "number" ? (entity[s.key] as number).toFixed(2) : "—"}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          )}
          {tab === 2 && (
            <div className="space-y-3">
              <div className="rounded-lg border border-slate-700/40 bg-slate-800/50 p-4">
                <p className="text-sm leading-relaxed text-slate-400">
                  Analyse du financement des groupes armés et des chaînes d&apos;approvisionnement opaques pour{" "}
                  <span className="text-slate-200 font-medium">{entity.name}</span>. Indice global&nbsp;:&nbsp;
                  <span className="text-slate-200 font-medium">
                    {entity.estimated_conflict_minerals_index.toFixed(2)}
                  </span>
                  . Niveau de risque&nbsp;:{" "}
                  <span className={rc}>{entity.risk_level}</span>.
                </p>
              </div>
              <div className="bg-slate-800/50 rounded-xl p-4">
                <div className="text-xs text-slate-400 mb-1">Schéma Principal</div>
                <div className="text-sm font-medium" style={{ color: ACCENT }}>{entity.primary_pattern}</div>
              </div>
              {entity.key_signals?.length > 0 && (
                <div className="bg-slate-800/50 rounded-xl p-4">
                  <div className="text-xs text-slate-400 mb-3">Signaux Détectés</div>
                  <ul className="space-y-2">
                    {entity.key_signals.map((sig, i) => (
                      <li key={i} className="flex items-start gap-2 text-sm text-slate-300">
                        <span className="mt-1 w-1.5 h-1.5 rounded-full flex-shrink-0" style={{ background: ACCENT }} />
                        {sig}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
              <div className="text-xs text-slate-500">
                Pays&nbsp;: {entity.country} &middot; Dernière MAJ&nbsp;: {entity.last_updated}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default function ConflictMineralsEnginePage() {
  const [data, setData] = useState<CMEData>({});
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState("tous");
  const [selected, setSelected] = useState<CMEEntity | null>(null);

  useEffect(() => {
    fetch("/api/conflict-minerals-engine")
      .then((r) => r.json())
      .then((d) => { setData(d.payload ?? d); setLoading(false); })
      .catch(() => setLoading(false));
  }, []);

  const summary = (data as { summary?: CMESummary }).summary;
  const rawEntities: CMEEntity[] = (data as { entities?: CMEEntity[] }).entities ?? summary?.entities ?? [];

  const PATTERN_KEYS = [
    "armed_group_financing_scale",
    "supply_chain_due_diligence_failure",
    "civilian_exploitation_harm",
    "corporate_accountability_gap",
  ];

  const patternFilter = PATTERN_KEYS.includes(filter);
  const entities = rawEntities.filter((e) => {
    if (filter === "tous") return true;
    if (patternFilter) return e.primary_pattern === filter;
    return e.risk_level === filter;
  });

  const avg = (arr: number[]) => arr.length ? arr.reduce((a, b) => a + b, 0) / arr.length : 0;
  const avgComposite = avg(rawEntities.map((e) => e.composite_score));
  const avgIndex = avg(rawEntities.map((e) => e.estimated_conflict_minerals_index));
  const countCritique = rawEntities.filter((e) => e.risk_level === "critique").length;
  const patternsActive = Object.keys(
    rawEntities.reduce((acc, e) => { acc[e.primary_pattern] = true; return acc; }, {} as Record<string,boolean>)
  ).length;
  const confidence = summary?.confidence_score ?? 0;

  const kpis = [
    { label: "Total Entités", value: rawEntities.length },
    { label: "Score Moyen", value: avgComposite.toFixed(1) },
    { label: "Index Moyen", value: avgIndex.toFixed(2) },
    { label: "Entités Critiques", value: countCritique },
    { label: "Patterns Actifs", value: patternsActive },
    { label: "Confiance", value: confidence ? `${(confidence * 100).toFixed(0)}%` : "—" },
  ];

  const riskFilters = ["tous", "critique", "élevé", "modéré", "faible"];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
      <div className="mx-auto max-w-7xl space-y-6">

        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <div className="flex items-center gap-3 mb-1">
              <div className="w-3 h-3 rounded-full" style={{ background: ACCENT }} />
              <h1 className="text-2xl font-bold tracking-tight">Conflict Minerals Engine</h1>
            </div>
            <p className="text-slate-400 text-sm ml-6">
              Surveillance des minerais de conflit — financement groupes armés &amp; chaînes d&apos;approvisionnement opaques
            </p>
          </div>
          <div className="rounded-lg border border-slate-700/50 bg-slate-900/80 px-4 py-2">
            <span className="text-xs text-slate-500">Statut</span>
            <div className="flex items-center gap-2">
              <span className={`h-2 w-2 rounded-full ${loading ? "bg-yellow-400" : "bg-emerald-400"}`} />
              <span className="text-sm text-slate-300">{loading ? "Chargement…" : "Actif"}</span>
            </div>
          </div>
        </div>

        {/* KPI Grid 3×2 */}
        <div className="grid grid-cols-3 gap-4">
          {kpis.map((kpi) => (
            <div
              key={kpi.label}
              className="rounded-xl border border-yellow-500/30 bg-yellow-500/10 p-4"
            >
              <div className="text-xs font-medium uppercase tracking-wide text-slate-500">{kpi.label}</div>
              <div className="mt-2 text-2xl font-bold text-yellow-400">{kpi.value}</div>
            </div>
          ))}
        </div>

        {/* Risk Filter Pills */}
        <div className="flex flex-wrap gap-2">
          {riskFilters.map((f) => (
            <button
              key={f}
              onClick={() => setFilter(f)}
              className={`rounded-full px-4 py-1.5 text-sm font-medium capitalize transition-all ${
                filter === f
                  ? "text-slate-950 font-bold"
                  : "bg-slate-800 text-slate-400 hover:bg-slate-700"
              }`}
              style={filter === f ? { background: ACCENT } : {}}
            >
              {f.charAt(0).toUpperCase() + f.slice(1)}
            </button>
          ))}
        </div>

        {/* Pattern Filter Pills */}
        <div className="flex flex-wrap gap-2">
          {PATTERN_KEYS.map((p) => (
            <button
              key={p}
              onClick={() => setFilter(p)}
              className={`rounded-full px-4 py-1.5 text-sm font-medium transition-all border ${
                filter === p
                  ? "border-yellow-500/30 bg-yellow-500/10 text-yellow-400"
                  : "border-slate-700/40 text-slate-500 hover:text-slate-300 hover:border-slate-500/30"
              }`}
            >
              {p.replace(/_/g, " ")}
            </button>
          ))}
        </div>

        {/* Entity Grid */}
        {loading ? (
          <div className="flex h-48 items-center justify-center">
            <div className="h-8 w-8 animate-spin rounded-full border-2 border-t-transparent" style={{ borderColor: `${ACCENT} transparent transparent transparent` }} />
          </div>
        ) : (
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {entities.map((entity) => (
              <button
                key={entity.id}
                onClick={() => setSelected(entity)}
                className={`rounded-xl border p-4 text-left transition-all hover:scale-[1.02] ${RB[entity.risk_level] ?? "border-slate-700/40 bg-slate-800/50"}`}
              >
                <div className="mb-2 flex items-start justify-between">
                  <div className="min-w-0 flex-1">
                    <span className="font-semibold text-slate-100 block truncate">{entity.name}</span>
                    <span className="text-xs text-slate-400">{entity.country}</span>
                  </div>
                  <span className={`text-xs font-medium ml-2 flex-shrink-0 ${RC[entity.risk_level] ?? "text-slate-400"}`}>
                    {entity.risk_level}
                  </span>
                </div>
                <div className="mt-3 flex items-center justify-between">
                  <span className="text-xs text-slate-500">Index Minerais Conflit</span>
                  <span className="font-mono text-sm text-yellow-400">
                    {entity.estimated_conflict_minerals_index.toFixed(2)}
                  </span>
                </div>
                <div className="mt-2 space-y-1">
                  {[
                    { key: "armed_group_financing_scale_score", label: "Financement Armé" },
                    { key: "supply_chain_due_diligence_failure_score", label: "Défaillance Chaîne" },
                    { key: "civilian_exploitation_harm_score", label: "Exploitation Civile" },
                    { key: "corporate_accountability_gap_score", label: "Gap Corporatif" },
                  ].map(({ key, label }) => (
                    <div key={key} className="flex items-center justify-between text-xs">
                      <span className="text-slate-500">{label}</span>
                      <span className="font-mono text-slate-400">
                        {typeof entity[key] === "number" ? (entity[key] as number).toFixed(1) : "—"}
                      </span>
                    </div>
                  ))}
                </div>
              </button>
            ))}
            {entities.length === 0 && (
              <div className="col-span-3 flex h-32 items-center justify-center text-slate-600">
                Aucune entité pour ce filtre
              </div>
            )}
          </div>
        )}
      </div>

      {selected && <DetailModal entity={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
