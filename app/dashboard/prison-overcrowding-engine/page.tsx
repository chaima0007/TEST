"use client";
import { useState, useEffect } from "react";

// ─── Types ───────────────────────────────────────────────────────────────────
interface Entity {
  entity_id: string;
  name: string;
  country?: string;
  sector?: string;
  risk_level: string;
  composite_score: number;
  estimated_prison_overcrowding_index: number;
  occupancy_rate_excess_score: number;
  health_sanitation_failure_score: number;
  violence_inmate_death_score: number;
  reform_political_will_gap_score: number;
  primary_pattern?: string;
  key_signals?: string[];
  signals?: string[];
  context?: string;
  last_updated?: string;
  [key: string]: unknown;
}

interface EngineResult {
  total_entities: number;
  avg_composite: number;
  avg_estimated_prison_overcrowding_index: number;
  confidence_score: number;
  risk_distribution: Record<string, number>;
  data_sources: string[];
  entities: Entity[];
  [key: string]: unknown;
}

// ─── Color maps ───────────────────────────────────────────────────────────────
const RC: Record<string, string> = { critique: "text-red-400", "élevé": "text-orange-400", modéré: "text-yellow-400", faible: "text-emerald-400" };
const RB: Record<string, string> = { critique: "border-red-500/30 bg-red-500/10", "élevé": "border-orange-500/30 bg-orange-500/10", modéré: "border-yellow-500/30 bg-yellow-500/10", faible: "border-emerald-500/30 bg-emerald-500/10" };

const ACCENT = "#7f1d1d";

function GaugeRing({ value }: { value: number }) {
  const circumference = 2 * Math.PI * 36;
  const offset = circumference - (Math.min(value, 100) / 100) * circumference;
  return (
    <svg viewBox="0 0 88 88" className="w-full h-full">
      <circle cx="44" cy="44" r="36" fill="none" stroke="currentColor" strokeWidth="8" className="text-slate-800" />
      <circle
        cx="44" cy="44" r="36" fill="none"
        stroke={ACCENT} strokeWidth="8"
        strokeDasharray={circumference}
        strokeDashoffset={offset}
        strokeLinecap="round"
        transform="rotate(-90 44 44)"
      />
      <text x="44" y="49" textAnchor="middle" fill="white" fontSize="13" fontWeight="bold">
        {value.toFixed(1)}
      </text>
    </svg>
  );
}

function DetailModal({ entity, onClose }: { entity: Entity; onClose: () => void }) {
  const [tab, setTab] = useState(0);

  useEffect(() => {
    const h = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", h);
    return () => window.removeEventListener("keydown", h);
  }, [onClose]);

  const subScores = [
    { label: "Taux d'Occupation Excessif", value: entity.occupancy_rate_excess_score },
    { label: "Défaillance Santé & Hygiène", value: entity.health_sanitation_failure_score },
    { label: "Violence & Décès Détenus", value: entity.violence_inmate_death_score },
    { label: "Absence Volonté Réforme", value: entity.reform_political_will_gap_score },
  ];

  const signals = entity.key_signals ?? entity.signals ?? [];

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70" onClick={onClose}>
      <div
        className="bg-slate-900 border border-slate-700 rounded-xl w-full max-w-lg mx-4 shadow-2xl"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="flex items-center justify-between p-5 border-b border-slate-800">
          <div>
            <h2 className="text-white font-bold text-lg">{entity.name}</h2>
            {entity.country && <p className="text-slate-400 text-sm">{entity.country}</p>}
            <span className={`text-xs font-bold uppercase mt-1 inline-block ${RC[entity.risk_level] ?? "text-slate-400"}`}>
              {entity.risk_level}
            </span>
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-white text-2xl leading-none">×</button>
        </div>

        <div className="flex border-b border-slate-800">
          {["Aperçu", "Signaux", "Contexte"].map((t, i) => (
            <button
              key={t}
              onClick={() => setTab(i)}
              className={`flex-1 py-3 text-sm font-medium transition-colors ${tab === i ? "text-white border-b-2" : "text-slate-400 hover:text-white"}`}
              style={tab === i ? { borderColor: ACCENT, color: ACCENT } : {}}
            >
              {t}
            </button>
          ))}
        </div>

        <div className="p-5">
          {tab === 0 && (
            <div className="space-y-4">
              <div className="flex items-center gap-4">
                <div className="w-20 h-20 shrink-0">
                  <GaugeRing value={entity.estimated_prison_overcrowding_index ?? entity.composite_score} />
                </div>
                <div>
                  <p className="text-slate-400 text-sm">Index Surpopulation</p>
                  <p className="text-white text-2xl font-bold">
                    {(entity.estimated_prison_overcrowding_index ?? entity.composite_score).toFixed(1)}
                  </p>
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

          {tab === 1 && (
            <div className="space-y-2">
              {signals.length > 0 ? (
                signals.map((sig, i) => (
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

          {tab === 2 && (
            <div className="space-y-3 text-sm text-slate-300">
              {entity.country && <div><span className="text-slate-500">Pays: </span>{entity.country}</div>}
              {entity.sector && <div><span className="text-slate-500">Secteur: </span>{entity.sector}</div>}
              {entity.primary_pattern && (
                <div><span className="text-slate-500">Patron: </span>{entity.primary_pattern.replace(/_/g, " ")}</div>
              )}
              {entity.context ? (
                <p className="leading-relaxed">{entity.context}</p>
              ) : (
                <p className="text-slate-500">Aucun contexte disponible.</p>
              )}
              {entity.last_updated && (
                <div><span className="text-slate-500">Dernière MAJ: </span>{String(entity.last_updated)}</div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default function PrisonOvercrowdingEnginePage() {
  const [data, setData] = useState<EngineResult | null>(null);
  const [filter, setFilter] = useState("tous");
  const [selected, setSelected] = useState<Entity | null>(null);

  useEffect(() => {
    fetch("/api/prison-overcrowding-engine")
      .then((r) => r.json())
      .then((j) => setData(j.payload ?? j))
      .catch(console.error);
  }, []);

  if (!data) {
    return (
      <div className="bg-slate-950 min-h-screen flex items-center justify-center">
        <div className="text-slate-400 animate-pulse">Chargement du module Surpopulation Carcérale…</div>
      </div>
    );
  }

  const entities: Entity[] = data.entities ?? [];
  const filtered = filter === "tous" ? entities : entities.filter((e) => e.risk_level === filter);

  const kpis = [
    { label: "Entités analysées", value: data.total_entities },
    { label: "Score composite moyen", value: data.avg_composite?.toFixed(1) ?? "—" },
    { label: "Index Surpopulation", value: data.avg_estimated_prison_overcrowding_index?.toFixed(2) ?? "—" },
    { label: "Confiance", value: `${((data.confidence_score ?? 0) * 100).toFixed(0)}%` },
    { label: "Critique", value: data.risk_distribution?.critique ?? 0 },
    { label: "Sources données", value: data.data_sources?.length ?? 0 },
  ];

  return (
    <div className="bg-slate-950 min-h-screen text-slate-100 p-6">
      {selected && <DetailModal entity={selected} onClose={() => setSelected(null)} />}

      <div className="mb-8">
        <div className="flex items-center gap-3 mb-2">
          <div className="w-3 h-3 rounded-full" style={{ background: ACCENT }} />
          <h1 className="text-2xl font-bold tracking-tight">Surpopulation Carcérale</h1>
        </div>
        <p className="text-slate-400 text-sm ml-6">
          Occupation · Santé &amp; hygiène · Violence &amp; décès · Réforme politique — Caelum Partners
        </p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4 mb-8">
        {kpis.map((k) => (
          <div key={k.label} className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 mb-1">{k.label}</div>
            <div className="text-xl font-bold" style={{ color: ACCENT }}>{k.value}</div>
          </div>
        ))}
      </div>

      {/* GaugeRing */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 mb-6 flex items-center gap-6">
        <div className="w-20 h-20 shrink-0">
          <GaugeRing value={data.avg_composite ?? 0} />
        </div>
        <div>
          <p className="text-slate-400 text-sm">Score Composite Moyen</p>
          <p className="text-white text-3xl font-bold">{(data.avg_composite ?? 0).toFixed(1)}</p>
          <p className="text-slate-500 text-xs mt-1">
            Index Surpopulation: {(data.avg_estimated_prison_overcrowding_index ?? 0).toFixed(2)}
          </p>
        </div>
      </div>

      {/* Filtres */}
      <div className="flex flex-wrap gap-2 mb-6">
        {["tous", "critique", "élevé", "modéré", "faible"].map((f) => (
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
      {filtered.length === 0 ? (
        <div className="text-slate-500 text-center py-16">Aucune entité trouvée.</div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {filtered.map((entity) => (
            <button
              key={entity.entity_id}
              onClick={() => setSelected(entity)}
              className={`text-left border rounded-xl p-4 hover:border-slate-600 transition-colors ${RB[entity.risk_level] ?? "border-slate-800 bg-slate-900"}`}
            >
              <div className="flex items-start justify-between mb-3">
                <div className="flex-1 min-w-0">
                  <p className="text-white font-semibold truncate">{entity.name}</p>
                  {entity.country && <p className="text-slate-400 text-xs mt-0.5">{entity.country}</p>}
                  <p className="text-slate-500 text-xs mt-0.5">{entity.entity_id}</p>
                </div>
                <span className={`ml-2 text-xs font-bold uppercase ${RC[entity.risk_level] ?? "text-slate-400"}`}>
                  {entity.risk_level}
                </span>
              </div>
              <div className="flex items-center justify-between mb-2">
                <span className="text-slate-400 text-xs">Index Surpopulation</span>
                <span className="text-white font-bold">
                  {(entity.estimated_prison_overcrowding_index ?? entity.composite_score).toFixed(1)}
                </span>
              </div>
              <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
                <div
                  className="h-full rounded-full"
                  style={{ width: `${Math.min(entity.composite_score, 100)}%`, backgroundColor: ACCENT }}
                />
              </div>
              <div className="mt-2 grid grid-cols-2 gap-1 text-xs text-slate-500">
                <span>Occupation: {(entity.occupancy_rate_excess_score ?? 0).toFixed(1)}</span>
                <span>Santé: {(entity.health_sanitation_failure_score ?? 0).toFixed(1)}</span>
                <span>Violence: {(entity.violence_inmate_death_score ?? 0).toFixed(1)}</span>
                <span>Réforme: {(entity.reform_political_will_gap_score ?? 0).toFixed(1)}</span>
              </div>
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
