"use client";

import { useState, useEffect } from "react";

const ACCENT = "#ec4899";

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

function GaugeRing({ value, color }: { value: number; color: string }) {
  const R = 36;
  const C = 2 * Math.PI * R;
  const offset = C - (value / 100) * C;
  return (
    <svg viewBox="0 0 88 88" className="w-20 h-20">
      <circle cx="44" cy="44" r={R} fill="none" stroke="#1e293b" strokeWidth="8" />
      <circle
        cx="44"
        cy="44"
        r={R}
        fill="none"
        stroke={color}
        strokeWidth="8"
        strokeDasharray={C}
        strokeDashoffset={offset}
        strokeLinecap="round"
        transform="rotate(-90 44 44)"
      />
      <text x="44" y="49" textAnchor="middle" fontSize="14" fontWeight="bold" fill={color}>
        {value.toFixed(1)}
      </text>
    </svg>
  );
}

interface Entity {
  id: string;
  name: string;
  country?: string;
  risk_level: string;
  composite_score: number;
  child_labor_exploitation_score: number;
  child_soldier_recruitment_score: number;
  child_marriage_protection_score: number;
  education_healthcare_denial_score: number;
  signals?: string[];
  context?: string;
}

interface ApiData {
  entities: Entity[];
  total_entities: number;
  avg_composite: number;
  critique_count: number;
  eleve_count: number;
  avg_estimated_child_rights_index: number;
  avg_confidence: number;
}

interface DetailModalProps {
  entity: Entity;
  onClose: () => void;
}

function DetailModal({ entity, onClose }: DetailModalProps) {
  const [tab, setTab] = useState<"apercu" | "signaux" | "contexte">("apercu");

  const subScores = [
    { label: "Travail Enfants", value: entity.child_labor_exploitation_score },
    { label: "Enfants Soldats", value: entity.child_soldier_recruitment_score },
    { label: "Mariage Précoce", value: entity.child_marriage_protection_score },
    { label: "Déni Santé/Éducation", value: entity.education_healthcare_denial_score },
  ];

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60" onClick={onClose}>
      <div
        className="bg-slate-900 border border-slate-700 rounded-xl w-full max-w-lg mx-4 shadow-2xl"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="flex items-center justify-between p-5 border-b border-slate-800">
          <div>
            <h2 className="text-white font-bold text-lg">{entity.name}</h2>
            {entity.country && <p className="text-slate-400 text-sm">{entity.country}</p>}
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-white text-2xl leading-none">×</button>
        </div>

        <div className="flex border-b border-slate-800">
          {(["apercu", "signaux", "contexte"] as const).map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`flex-1 py-3 text-sm font-medium capitalize transition-colors ${
                tab === t ? "text-white border-b-2" : "text-slate-400 hover:text-white"
              }`}
              style={tab === t ? { borderColor: ACCENT } : {}}
            >
              {t === "apercu" ? "Aperçu" : t === "signaux" ? "Signaux" : "Contexte"}
            </button>
          ))}
        </div>

        <div className="p-5">
          {tab === "apercu" && (
            <div className="space-y-4">
              <div className="flex items-center gap-4">
                <GaugeRing value={entity.composite_score} color={ACCENT} />
                <div>
                  <p className="text-slate-400 text-sm">Score Composite</p>
                  <p className="text-white text-2xl font-bold">{entity.composite_score.toFixed(1)}</p>
                  <span className={`text-sm font-medium ${RC[entity.risk_level] ?? "text-slate-400"}`}>
                    {entity.risk_level}
                  </span>
                </div>
              </div>
              <div className="space-y-2">
                {subScores.map((s) => (
                  <div key={s.label}>
                    <div className="flex justify-between text-sm mb-1">
                      <span className="text-slate-400">{s.label}</span>
                      <span className="text-white font-medium">{(s.value ?? 0).toFixed(1)}</span>
                    </div>
                    <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
                      <div
                        className="h-full rounded-full"
                        style={{ width: `${Math.min(s.value ?? 0, 100)}%`, backgroundColor: ACCENT }}
                      />
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {tab === "signaux" && (
            <div className="space-y-2">
              {entity.signals && entity.signals.length > 0 ? (
                entity.signals.map((sig, i) => (
                  <div key={i} className="flex items-start gap-2">
                    <span className="mt-1.5 w-1.5 h-1.5 rounded-full flex-shrink-0" style={{ backgroundColor: ACCENT }} />
                    <p className="text-slate-300 text-sm">{sig}</p>
                  </div>
                ))
              ) : (
                <p className="text-slate-500 text-sm">Aucun signal disponible.</p>
              )}
            </div>
          )}

          {tab === "contexte" && (
            <p className="text-slate-300 text-sm leading-relaxed">
              {entity.context ?? "Aucun contexte disponible."}
            </p>
          )}
        </div>
      </div>
    </div>
  );
}

const FILTERS = ["tous", "critique", "élevé", "modéré", "faible"] as const;
type Filter = (typeof FILTERS)[number];

export default function ChildRightsEnginePage() {
  const [data, setData] = useState<ApiData | null>(null);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState<Filter>("tous");
  const [selected, setSelected] = useState<Entity | null>(null);

  useEffect(() => {
    fetch("/api/child-rights-engine")
      .then((r) => r.json())
      .then((d) => { setData(d); setLoading(false); })
      .catch(() => setLoading(false));
  }, []);

  const entities: Entity[] = data?.entities ?? [];

  const filtered = filter === "tous"
    ? entities
    : entities.filter((e) => e.risk_level === filter);

  const kpis = [
    { label: "Total Entités", value: data?.total_entities ?? 0, fmt: (v: number) => v.toString() },
    { label: "Avg Composite", value: data?.avg_composite ?? 0, fmt: (v: number) => v.toFixed(1) },
    { label: "Critique", value: data?.critique_count ?? 0, fmt: (v: number) => v.toString() },
    { label: "Élevé", value: data?.eleve_count ?? 0, fmt: (v: number) => v.toString() },
    { label: "Index Moyen", value: data?.avg_estimated_child_rights_index ?? 0, fmt: (v: number) => v.toFixed(1) },
    { label: "Confiance", value: data?.avg_confidence ?? 0, fmt: (v: number) => v.toFixed(1) },
  ];

  return (
    <div className="min-h-screen bg-slate-950 text-white p-6">
      {selected && <DetailModal entity={selected} onClose={() => setSelected(null)} />}

      <div className="mb-6">
        <h1 className="text-2xl font-bold" style={{ color: ACCENT }}>
          Child Rights Engine
        </h1>
        <p className="text-slate-400 text-sm mt-1">
          Analyse des violations des droits de l'enfant, du travail des mineurs et de la protection infantile
        </p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4 mb-6">
        {kpis.map((k) => (
          <div key={k.label} className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <p className="text-slate-400 text-xs mb-1">{k.label}</p>
            {loading ? (
              <div className="h-7 bg-slate-800 rounded animate-pulse" />
            ) : (
              <p className="text-white text-xl font-bold">{k.fmt(k.value)}</p>
            )}
          </div>
        ))}
      </div>

      {/* GaugeRing for index */}
      {!loading && data && (
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 mb-6 flex items-center gap-6">
          <GaugeRing value={data.avg_estimated_child_rights_index ?? 0} color={ACCENT} />
          <div>
            <p className="text-slate-400 text-sm">Index Moyen Child Rights</p>
            <p className="text-white text-3xl font-bold">{(data.avg_estimated_child_rights_index ?? 0).toFixed(1)}</p>
          </div>
        </div>
      )}

      {/* Filter Pills */}
      <div className="flex flex-wrap gap-2 mb-6">
        {FILTERS.map((f) => (
          <button
            key={f}
            onClick={() => setFilter(f)}
            className={`px-4 py-1.5 rounded-full text-sm font-medium border transition-colors ${
              filter === f
                ? "text-white border-transparent"
                : "text-slate-400 border-slate-700 hover:text-white hover:border-slate-500"
            }`}
            style={filter === f ? { backgroundColor: ACCENT, borderColor: ACCENT } : {}}
          >
            {f}
          </button>
        ))}
      </div>

      {/* Entity Grid */}
      {loading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {Array.from({ length: 6 }).map((_, i) => (
            <div key={i} className="bg-slate-900 border border-slate-800 rounded-xl p-4 animate-pulse">
              <div className="h-5 bg-slate-800 rounded mb-2 w-3/4" />
              <div className="h-4 bg-slate-800 rounded w-1/2" />
            </div>
          ))}
        </div>
      ) : filtered.length === 0 ? (
        <div className="text-slate-500 text-center py-16">Aucune entité trouvée.</div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {filtered.map((entity) => (
            <button
              key={entity.id}
              onClick={() => setSelected(entity)}
              className={`text-left bg-slate-900 border rounded-xl p-4 hover:border-slate-600 transition-colors ${
                RB[entity.risk_level] ?? "border-slate-800"
              }`}
            >
              <div className="flex items-start justify-between mb-3">
                <div className="flex-1 min-w-0">
                  <p className="text-white font-semibold truncate">{entity.name}</p>
                  {entity.country && (
                    <p className="text-slate-400 text-xs mt-0.5">{entity.country}</p>
                  )}
                </div>
                <span className={`ml-2 text-xs font-medium px-2 py-0.5 rounded-full border ${RB[entity.risk_level] ?? "border-slate-700"} ${RC[entity.risk_level] ?? "text-slate-400"}`}>
                  {entity.risk_level}
                </span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-slate-400 text-xs">Score composite</span>
                <span className="text-white font-bold">{entity.composite_score.toFixed(1)}</span>
              </div>
              <div className="mt-2 h-1.5 bg-slate-800 rounded-full overflow-hidden">
                <div
                  className="h-full rounded-full"
                  style={{ width: `${Math.min(entity.composite_score, 100)}%`, backgroundColor: ACCENT }}
                />
              </div>
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
