"use client";
import { useState, useEffect } from "react";

const RC: Record<string,string> = { critique:"text-red-400","élevé":"text-orange-400",modéré:"text-yellow-400",faible:"text-emerald-400" };
const RB: Record<string,string> = { critique:"border-red-500/30 bg-red-500/10","élevé":"border-orange-500/30 bg-orange-500/10",modéré:"border-yellow-500/30 bg-yellow-500/10",faible:"border-emerald-500/30 bg-emerald-500/10" };

interface CPSEEntity {
  entity_id: string;
  name: string;
  country: string;
  composite_score: number;
  material_deprivation_severity_score: number;
  education_access_barrier_score: number;
  healthcare_nutrition_denial_score: number;
  social_exclusion_stigma_score: number;
  risk_level: string;
  primary_pattern: string;
  estimated_child_poverty_social_exclusion_index: number;
  last_updated: string;
  [key: string]: unknown;
}

interface CPSESummary {
  agent: string;
  domain: string;
  total_entities: number;
  avg_composite: number;
  confidence_score: number;
  risk_distribution: Record<string, number>;
  pattern_distribution: Record<string, number>;
  top_risk_entities: string[];
  critical_alerts: string[];
  last_analysis: string;
  engine_version: string;
  avg_estimated_child_poverty_social_exclusion_index: number;
  data_sources: string[];
  entities: CPSEEntity[];
}

interface KPI {
  label: string;
  value: string | number;
}

interface ApiData {
  kpis?: KPI[];
  entities?: CPSEEntity[];
  summary?: CPSESummary;
}

function GaugeRing({ value, max = 100 }: { value: number; max?: number }) {
  const r = 36;
  const cx = 44;
  const cy = 44;
  const circumference = 226.19;
  const progress = Math.min(Math.max(value / max, 0), 1);
  const dash = progress * circumference;
  return (
    <svg width={88} height={88} viewBox="0 0 88 88" className="rotate-[-90deg]">
      <circle cx={cx} cy={cy} r={r} fill="none" stroke="#1e293b" strokeWidth={8} />
      <circle
        cx={cx}
        cy={cy}
        r={r}
        fill="none"
        stroke="#10b981"
        strokeWidth={8}
        strokeDasharray={`${dash} ${circumference}`}
        strokeLinecap="round"
      />
    </svg>
  );
}

function DetailModal({ entity, onClose }: { entity: CPSEEntity; onClose: () => void }) {
  const [tab, setTab] = useState(0);
  const tabs = ["Scores", "Indicateurs", "Contexte pauvreté"];
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm">
      <div className="w-full max-w-lg rounded-xl border border-slate-700/50 bg-slate-900 p-6 shadow-2xl">
        <div className="mb-4 flex items-start justify-between">
          <div>
            <h2 className="text-xl font-bold text-slate-100">{entity.name}</h2>
            <span className={`text-sm font-medium ${RC[entity.risk_level] ?? "text-slate-400"}`}>
              {entity.risk_level}
            </span>
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-slate-100 text-xl leading-none">
            ✕
          </button>
        </div>
        <div className="mb-4 flex gap-2">
          {tabs.map((t, i) => (
            <button
              key={t}
              onClick={() => setTab(i)}
              className={`rounded-md px-3 py-1 text-sm font-medium transition-colors ${
                tab === i
                  ? "bg-emerald-500/20 text-emerald-300 border border-emerald-500/30"
                  : "text-slate-500 hover:text-slate-300"
              }`}
            >
              {t}
            </button>
          ))}
        </div>
        {tab === 0 && (
          <div className="space-y-3">
            {[
              { label: "Privation Matérielle", value: entity.material_deprivation_severity_score },
              { label: "Barrière Éducation", value: entity.education_access_barrier_score },
              { label: "Santé & Nutrition", value: entity.healthcare_nutrition_denial_score },
              { label: "Exclusion Stigma", value: entity.social_exclusion_stigma_score },
            ].map((s) => (
              <div key={s.label} className="flex items-center justify-between rounded-lg border border-slate-700/40 bg-slate-800/50 px-4 py-2">
                <span className="text-sm text-slate-400">{s.label}</span>
                <span className="font-mono text-sm text-slate-200">{typeof s.value === "number" ? s.value.toFixed(2) : s.value}</span>
              </div>
            ))}
          </div>
        )}
        {tab === 1 && (
          <div className="flex flex-col items-center gap-4 py-4">
            <GaugeRing value={entity.estimated_child_poverty_social_exclusion_index} max={10} />
            <div className="text-center">
              <div className="text-3xl font-bold text-emerald-400">
                {typeof entity.estimated_child_poverty_social_exclusion_index === "number"
                  ? entity.estimated_child_poverty_social_exclusion_index.toFixed(1)
                  : entity.estimated_child_poverty_social_exclusion_index}
              </div>
              <div className="text-sm text-slate-500">Index Pauvreté Enfants</div>
            </div>
          </div>
        )}
        {tab === 2 && (
          <div className="rounded-lg border border-slate-700/40 bg-slate-800/50 p-4">
            <p className="text-sm leading-relaxed text-slate-400">
              Analyse du contexte de pauvreté et d&apos;exclusion sociale pour {entity.name}. Indice global&nbsp;:&nbsp;
              <span className="text-slate-200 font-medium">
                {typeof entity.estimated_child_poverty_social_exclusion_index === "number"
                  ? entity.estimated_child_poverty_social_exclusion_index.toFixed(2)
                  : entity.estimated_child_poverty_social_exclusion_index}
              </span>
              . Niveau de risque&nbsp;: <span className={RC[entity.risk_level]}>{entity.risk_level}</span>.
            </p>
          </div>
        )}
      </div>
    </div>
  );
}

export default function ChildPoveSocialExclusionEngine() {
  const [data, setData] = useState<ApiData>({});
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState("tous");
  const [selected, setSelected] = useState<CPSEEntity | null>(null);

  useEffect(() => {
    fetch("/api/child-poverty-social-exclusion-engine")
      .then((r) => r.json())
      .then((d) => { setData(d.payload ?? d); setLoading(false); })
      .catch(() => setLoading(false));
  }, []);

  const filters = ["tous", "critique", "élevé", "modéré", "faible"];
  const entities: CPSEEntity[] = (data.entities ?? []).filter(
    (e) => filter === "tous" || e.risk_level === filter
  );
  const kpis: KPI[] = data.kpis ?? [];

  return (
    <div className="min-h-screen bg-slate-950 p-6 text-slate-100">
      <div className="mx-auto max-w-7xl space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold tracking-tight text-slate-100">Child Poverty &amp; Social Exclusion Engine</h1>
            <p className="mt-1 text-sm text-slate-500">Analyse de la pauvreté des enfants et de l&apos;exclusion sociale — accès aux droits essentiels</p>
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
          {(kpis.length > 0 ? kpis : [
            { label: "Privation Matérielle", value: "—" },
            { label: "Barrière Éducation", value: "—" },
            { label: "Santé & Nutrition", value: "—" },
            { label: "Exclusion Stigma", value: "—" },
            { label: "Index Pauvreté Enfants", value: "—" },
            { label: "Entités Surveillées", value: entities.length || "—" },
          ]).slice(0, 6).map((kpi) => (
            <div
              key={kpi.label}
              className="rounded-xl border border-emerald-500/30 bg-emerald-500/10 p-4"
            >
              <div className="text-xs font-medium uppercase tracking-wide text-slate-500">{kpi.label}</div>
              <div className="mt-2 text-2xl font-bold text-emerald-400">
                {typeof kpi.value === "number" ? kpi.value.toFixed(2) : kpi.value}
              </div>
            </div>
          ))}
        </div>

        {/* Filter Pills */}
        <div className="flex flex-wrap gap-2">
          {filters.map((f) => (
            <button
              key={f}
              onClick={() => setFilter(f)}
              className={`rounded-full px-4 py-1.5 text-sm font-medium capitalize transition-all ${
                filter === f
                  ? "bg-emerald-500/20 text-emerald-300 border border-emerald-500/30"
                  : "border border-slate-700/40 text-slate-500 hover:text-slate-300 hover:border-slate-500/30"
              }`}
            >
              {f}
            </button>
          ))}
        </div>

        {/* Entity Grid */}
        {loading ? (
          <div className="flex h-48 items-center justify-center">
            <div className="h-8 w-8 animate-spin rounded-full border-2 border-emerald-500 border-t-transparent" />
          </div>
        ) : (
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {entities.map((entity) => (
              <button
                key={entity.entity_id}
                onClick={() => setSelected(entity)}
                className={`rounded-xl border p-4 text-left transition-all hover:scale-[1.02] ${RB[entity.risk_level] ?? "border-slate-700/40 bg-slate-800/50"}`}
              >
                <div className="mb-2 flex items-start justify-between">
                  <span className="font-semibold text-slate-100">{entity.name}</span>
                  <span className={`text-xs font-medium ${RC[entity.risk_level] ?? "text-slate-400"}`}>
                    {entity.risk_level}
                  </span>
                </div>
                <div className="mt-3 flex items-center justify-between">
                  <span className="text-xs text-slate-500">Pauvreté Index</span>
                  <span className="font-mono text-sm text-emerald-400">
                    {typeof entity.estimated_child_poverty_social_exclusion_index === "number"
                      ? entity.estimated_child_poverty_social_exclusion_index.toFixed(2)
                      : entity.estimated_child_poverty_social_exclusion_index}
                  </span>
                </div>
                <div className="mt-2 space-y-1">
                  {[
                    { key: "material_deprivation_severity_score", label: "Privation Matérielle" },
                    { key: "education_access_barrier_score", label: "Barrière Éducation" },
                    { key: "healthcare_nutrition_denial_score", label: "Santé & Nutrition" },
                    { key: "social_exclusion_stigma_score", label: "Exclusion Stigma" },
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
