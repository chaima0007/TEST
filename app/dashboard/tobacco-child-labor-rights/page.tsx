"use client";
import { useState, useEffect } from "react";

const RC: Record<string, string> = { critique: "text-red-400", "élevé": "text-orange-400", modéré: "text-yellow-400", faible: "text-emerald-400" };
const RB: Record<string, string> = { critique: "border-red-500/30 bg-red-500/10", "élevé": "border-orange-500/30 bg-orange-500/10", modéré: "border-yellow-500/30 bg-yellow-500/10", faible: "border-emerald-500/30 bg-emerald-500/10" };

const ACCENT = "#0891b2";

interface Entity {
  id: string;
  name: string;
  country: string;
  composite_score: number;
  child_labor_prevalence_hazard_score: number;
  green_tobacco_sickness_health_impact_score: number;
  enforcement_legal_protection_deficit_score: number;
  corporate_accountability_supply_chain_score: number;
  estimated_tobacco_child_labor_index: number;
  risk_level: string;
  primary_pattern: string;
  last_updated: string;
  [key: string]: unknown;
}

interface DashData {
  total_entities?: number;
  avg_composite?: number;
  avg_estimated_tobacco_child_labor_index?: number;
  risk_distribution?: Record<string, number>;
  confidence_score?: number;
  data_sources?: string[];
  entities?: Entity[];
  [key: string]: unknown;
}

function GaugeRing({ value, label }: { value: number; label: string }) {
  const r = 36;
  const circ = 2 * Math.PI * r;
  const fill = circ * (1 - Math.min(value, 100) / 100);
  return (
    <div className="flex flex-col items-center gap-1">
      <svg width="88" height="88" viewBox="0 0 88 88">
        <circle cx="44" cy="44" r={r} fill="none" stroke="#1e293b" strokeWidth={8} />
        <circle
          cx="44" cy="44" r={r} fill="none" stroke={ACCENT} strokeWidth={8}
          strokeDasharray={circ} strokeDashoffset={fill}
          strokeLinecap="round" transform="rotate(-90 44 44)"
        />
        <text x="44" y="49" textAnchor="middle" fill="white" fontSize="13" fontWeight="bold">
          {value.toFixed(1)}
        </text>
      </svg>
      <span className="text-xs text-slate-400 text-center">{label}</span>
    </div>
  );
}

function DetailModal({ entity, onClose }: { entity: Entity; onClose: () => void }) {
  const [tab, setTab] = useState<"apercu" | "metriques" | "sources">("apercu");
  const tabs: { key: "apercu" | "metriques" | "sources"; label: string }[] = [
    { key: "apercu", label: "Aperçu" },
    { key: "metriques", label: "Métriques" },
    { key: "sources", label: "Sources" },
  ];
  const subScores = [
    { label: "Prévalence & Danger Travail Enfant", value: entity.child_labor_prevalence_hazard_score, weight: "0.30" },
    { label: "Green Tobacco Sickness & Santé", value: entity.green_tobacco_sickness_health_impact_score, weight: "0.25" },
    { label: "Déficit Contrôle & Protection Légale", value: entity.enforcement_legal_protection_deficit_score, weight: "0.25" },
    { label: "Responsabilité Corporative Chaîne", value: entity.corporate_accountability_supply_chain_score, weight: "0.20" },
  ];
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm p-4" onClick={onClose}>
      <div className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-2xl max-h-[90vh] overflow-y-auto shadow-2xl" onClick={(e) => e.stopPropagation()}>
        <div className="p-6 border-b border-slate-800 flex items-start justify-between gap-4">
          <div>
            <h2 className="text-xl font-bold text-white">{entity.name}</h2>
            <p className="text-sm text-slate-400 mt-0.5">{entity.country}</p>
            <span className={`text-xs font-semibold uppercase mt-1 inline-block ${RC[entity.risk_level] ?? "text-slate-400"}`}>{entity.risk_level}</span>
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-white transition-colors text-2xl leading-none">&times;</button>
        </div>
        <div className="flex border-b border-slate-800">
          {tabs.map((t) => (
            <button key={t.key} onClick={() => setTab(t.key)}
              className={`flex-1 py-3 text-sm font-medium transition-colors ${tab === t.key ? "border-b-2 text-white" : "text-slate-500 hover:text-slate-300"}`}
              style={tab === t.key ? { borderColor: ACCENT, color: ACCENT } : {}}>
              {t.label}
            </button>
          ))}
        </div>
        <div className="p-6">
          {tab === "apercu" && (
            <div className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div className="bg-slate-800/50 rounded-xl p-4 text-center">
                  <div className="text-3xl font-bold" style={{ color: ACCENT }}>{entity.composite_score.toFixed(1)}</div>
                  <div className="text-xs text-slate-400 mt-1">Score Composite</div>
                </div>
                <div className="bg-slate-800/50 rounded-xl p-4 text-center">
                  <div className="text-3xl font-bold" style={{ color: ACCENT }}>{typeof entity.estimated_tobacco_child_labor_index === "number" ? entity.estimated_tobacco_child_labor_index.toFixed(2) : "—"}</div>
                  <div className="text-xs text-slate-400 mt-1">Index Travail Enfant Tabac</div>
                </div>
              </div>
              <div className={`rounded-lg p-3 border ${RB[entity.risk_level] ?? "border-slate-700 bg-slate-800/30"}`}>
                <span className={`text-sm font-semibold capitalize ${RC[entity.risk_level] ?? "text-slate-300"}`}>
                  Niveau de risque : {entity.risk_level}
                </span>
              </div>
              <div className="bg-slate-800/50 rounded-xl p-4">
                <div className="text-xs text-slate-400 mb-2">Pattern Principal</div>
                <div className="text-sm font-medium" style={{ color: ACCENT }}>{entity.primary_pattern}</div>
              </div>
            </div>
          )}
          {tab === "metriques" && (
            <div className="space-y-3">
              {subScores.map((s) => (
                <div key={s.label} className="bg-slate-800/50 rounded-lg p-3">
                  <div className="flex justify-between items-center mb-1.5">
                    <span className="text-sm text-slate-300">{s.label}</span>
                    <div className="flex items-center gap-2">
                      <span className="text-xs text-slate-500">×{s.weight}</span>
                      <span className="text-sm font-bold text-white">{typeof s.value === "number" ? s.value.toFixed(1) : "—"}</span>
                    </div>
                  </div>
                  <div className="h-2 bg-slate-700 rounded-full overflow-hidden">
                    <div className="h-full rounded-full" style={{ width: `${Math.min(typeof s.value === "number" ? s.value : 0, 100)}%`, background: ACCENT }} />
                  </div>
                </div>
              ))}
            </div>
          )}
          {tab === "sources" && (
            <div className="space-y-3">
              <div className="bg-slate-800/50 rounded-xl p-4">
                <div className="text-xs text-slate-400 mb-2">Dernière mise à jour</div>
                <div className="text-sm text-slate-300">{new Date(entity.last_updated).toLocaleDateString("fr-FR")}</div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default function TobaccoChildLaborRightsPage() {
  const [data, setData] = useState<DashData | null>(null);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState("tous");
  const [selected, setSelected] = useState<Entity | null>(null);

  useEffect(() => {
    fetch("/api/tobacco-child-labor-rights")
      .then(r => r.json())
      .then(d => { setData(d.payload ?? d); setLoading(false); })
      .catch(() => { setLoading(false); });
  }, []);

  if (loading) {
    return (
      <div className="bg-slate-950 min-h-screen flex items-center justify-center">
        <div className="animate-pulse text-sm" style={{ color: ACCENT }}>Initialisation Droits — Travail Enfant dans le Tabac…</div>
      </div>
    );
  }

  const allEntities: Entity[] = data?.entities ?? (Array.isArray(data) ? data as unknown as Entity[] : []);
  const filtered = filter === "tous" ? allEntities : allEntities.filter(e => e.risk_level === filter);
  const avg = (arr: number[]) => arr.length ? arr.reduce((a, b) => a + b, 0) / arr.length : 0;
  const avgComposite = data?.avg_composite ?? avg(allEntities.map(e => e.composite_score));
  const avgIndex = data?.avg_estimated_tobacco_child_labor_index ?? avg(allEntities.map(e => e.estimated_tobacco_child_labor_index));
  const rd = data?.risk_distribution ?? {};
  const countCritique = rd["critique"] ?? allEntities.filter(e => e.risk_level === "critique").length;
  const countEleve = rd["élevé"] ?? allEntities.filter(e => e.risk_level === "élevé").length;
  const sources = data?.data_sources ?? [];
  const confidence = typeof data?.confidence_score === "number" ? `${(data.confidence_score * 100).toFixed(0)}%` : "—";

  const avgChildLabor = avg(allEntities.map(e => e.child_labor_prevalence_hazard_score));
  const avgGTS = avg(allEntities.map(e => e.green_tobacco_sickness_health_impact_score));
  const avgEnforcement = avg(allEntities.map(e => e.enforcement_legal_protection_deficit_score));
  const avgCorporate = avg(allEntities.map(e => e.corporate_accountability_supply_chain_score));

  const kpis = [
    { label: "Entités Analysées", value: data?.total_entities ?? allEntities.length },
    { label: "Score Moyen", value: avgComposite.toFixed(1) },
    { label: "Index Travail Enfant Tabac", value: avgIndex.toFixed(2) },
    { label: "Confiance", value: confidence },
    { label: "Critique", value: countCritique },
    { label: "Élevé", value: countEleve },
  ];

  const filters = ["tous", "critique", "élevé", "modéré", "faible"];

  return (
    <div className="min-h-screen bg-slate-950 text-white p-6 space-y-6">
      {selected && <DetailModal entity={selected} onClose={() => setSelected(null)} />}

      {/* Header */}
      <div>
        <div className="flex items-center gap-3 mb-1">
          <div className="w-3 h-8 rounded-full" style={{ background: ACCENT }} />
          <h1 className="text-2xl font-bold tracking-tight">Droits — Travail Enfant dans le Tabac</h1>
        </div>
        <p className="text-slate-400 text-sm ml-6">
          Tobacco Child Labor Rights Engine · Wave 281 — Caelum Partners · Chaima Mhadbi, Fondatrice, Bruxelles
        </p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
        {kpis.map(k => (
          <div key={k.label} className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 mb-1">{k.label}</div>
            <div className="text-xl font-bold" style={{ color: ACCENT }}>{k.value}</div>
          </div>
        ))}
      </div>

      {/* Gauge Rings */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
        <h2 className="text-sm font-semibold text-slate-400 mb-4">Scores Moyens par Dimension</h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
          <GaugeRing value={avgChildLabor} label="Prévalence Travail Enfant" />
          <GaugeRing value={avgGTS} label="Green Tobacco Sickness" />
          <GaugeRing value={avgEnforcement} label="Déficit Protection Légale" />
          <GaugeRing value={avgCorporate} label="Responsabilité Corporative" />
        </div>
      </div>

      {/* Filter Pills */}
      <div className="flex gap-2 flex-wrap">
        {filters.map(f => (
          <button key={f} onClick={() => setFilter(f)}
            className={`px-4 py-1.5 rounded-full text-sm font-medium transition-all ${filter === f ? "text-white font-bold" : "bg-slate-800 text-slate-400 hover:bg-slate-700"}`}
            style={filter === f ? { background: ACCENT } : {}}>
            {f.charAt(0).toUpperCase() + f.slice(1)}
          </button>
        ))}
      </div>

      {/* Entity Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
        {filtered.map(e => (
          <div key={e.id} onClick={() => setSelected(e)}
            className={`border rounded-xl p-4 cursor-pointer hover:scale-[1.01] transition-transform ${RB[e.risk_level] ?? "border-slate-700 bg-slate-900"}`}>
            <div className="flex justify-between items-start mb-2">
              <div className="flex-1 min-w-0">
                <div className="font-semibold text-sm leading-tight truncate">{e.name}</div>
                <div className="text-xs text-slate-400 mt-1">{e.country}</div>
              </div>
              <div className="text-right ml-3 flex-shrink-0">
                <div className="text-xl font-bold text-white">{e.composite_score.toFixed(1)}</div>
                <div className={`text-xs font-bold uppercase mt-1 ${RC[e.risk_level] ?? "text-slate-400"}`}>{e.risk_level}</div>
              </div>
            </div>
            <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden mt-2">
              <div className="h-full rounded-full transition-all" style={{ width: `${Math.min(e.composite_score, 100)}%`, background: ACCENT }} />
            </div>
            <div className="text-xs text-slate-500 mt-2">
              Index Travail Enfant Tabac : <span className="font-medium" style={{ color: ACCENT }}>{typeof e.estimated_tobacco_child_labor_index === "number" ? e.estimated_tobacco_child_labor_index.toFixed(2) : "—"}</span>
            </div>
          </div>
        ))}
      </div>

      {filtered.length === 0 && (
        <div className="text-center py-12 text-slate-500 text-sm">Aucune entité pour ce niveau de risque.</div>
      )}

      {/* Sources */}
      {sources.length > 0 && (
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
          <h3 className="text-slate-400 text-xs uppercase tracking-wide mb-3">Sources de données</h3>
          <div className="flex flex-wrap gap-2">
            {sources.map((src) => (
              <span key={src} className="text-xs bg-slate-800 text-slate-400 px-3 py-1 rounded-full border border-slate-700/50">{src}</span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
