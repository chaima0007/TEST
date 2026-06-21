"use client";
import { useState, useEffect } from "react";

const RC: Record<string,string> = { critique:"text-red-400","élevé":"text-orange-400",modéré:"text-yellow-400",faible:"text-emerald-400" };
const RB: Record<string,string> = { critique:"border-red-500/30 bg-red-500/10","élevé":"border-orange-500/30 bg-orange-500/10",modéré:"border-yellow-500/30 bg-yellow-500/10",faible:"border-emerald-500/30 bg-emerald-500/10" };

function GaugeRing({ value, stroke }: { value: number; stroke: string }) {
  const r = 36, cx = 44, cy = 44, circ = 2 * Math.PI * r;
  const pct = Math.min(Math.max(value, 0), 100) / 100;
  return (
    <svg viewBox="0 0 88 88" className="w-20 h-20">
      <circle cx={cx} cy={cy} r={r} fill="none" stroke="#1e293b" strokeWidth={8} />
      <circle cx={cx} cy={cy} r={r} fill="none" stroke={stroke} strokeWidth={8}
        strokeDasharray={circ} strokeDashoffset={circ * (1 - pct)}
        strokeLinecap="round" transform="rotate(-90 44 44)" />
      <text x={cx} y={cy} textAnchor="middle" dominantBaseline="central"
        fill="white" fontSize={14} fontWeight="bold">{Math.round(value)}</text>
    </svg>
  );
}

interface GDEntity {
  id: string;
  name: string;
  country: string;
  sector: string;
  composite_score: number;
  insurance_genetic_exclusion_severity_score: number;
  employment_dna_testing_coercion_scale_score: number;
  predictive_data_consent_absence_score: number;
  legal_protection_genetic_privacy_gap_score: number;
  estimated_genetic_discrimination_index: number;
  risk_level: string;
  primary_pattern: string;
  key_signals: string[];
  last_updated: string;
  [key: string]: unknown;
}

interface GDData {
  total_entities: number;
  avg_composite: number;
  risk_distribution: Record<string, number>;
  pattern_distribution: Record<string, number>;
  top_risk_entities: string[];
  critical_alerts: string[];
  last_analysis: string;
  confidence_score: number;
  data_sources: string[];
  entities: GDEntity[];
  avg_estimated_genetic_discrimination_index: number;
  engine_version: string;
  [key: string]: unknown;
}

export default function GeneticDiscriminationPage() {
  const [data, setData] = useState<GDData | null>(null);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState("tous");
  const [selected, setSelected] = useState<GDEntity | null>(null);
  const [tab, setTab] = useState(0);

  useEffect(() => {
    fetch("/api/genetic-discrimination-engine")
      .then(r => r.json())
      .then(d => { setData(d.payload ?? d); setLoading(false); });
  }, []);

  if (loading) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-slate-400 animate-pulse">Chargement des données de discrimination génétique…</div>
    </div>
  );
  if (!data) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-red-400">Données indisponibles</div>
    </div>
  );

  const filtered = filter === "tous" ? data.entities : data.entities.filter(e => e.risk_level === filter);

  const subKeys = [
    { key: "insurance_genetic_exclusion_severity_score", label: "Exclusion Assurance ADN" },
    { key: "employment_dna_testing_coercion_scale_score", label: "Coercition Tests ADN" },
    { key: "predictive_data_consent_absence_score", label: "Absence Consentement" },
    { key: "legal_protection_genetic_privacy_gap_score", label: "Lacunes Légales" },
  ];

  const avgSub = (key: string) => {
    const vals = data.entities.map(e => e[key] as number).filter(v => typeof v === "number");
    return vals.length ? Math.round(vals.reduce((a, b) => a + b, 0) / vals.length) : 0;
  };

  return (
    <div className="min-h-screen bg-slate-950 text-white p-6">
      {/* Header */}
      <div className="max-w-7xl mx-auto mb-8">
        <div className="flex items-center gap-3 mb-2">
          <div className="w-3 h-3 rounded-full bg-emerald-400" />
          <h1 className="text-2xl font-bold tracking-tight">Discrimination Génétique</h1>
        </div>
        <p className="text-slate-400 text-sm ml-6">Tests ADN, assurances, biobanques — vie privée génomique</p>
      </div>

      <div className="max-w-7xl mx-auto space-y-6">
        {/* KPI Cards — 3×2 */}
        <div className="grid grid-cols-3 gap-4">
          {[
            { label: "Score Moyen", value: data.avg_composite?.toFixed(1) },
            { label: "Entités Critiques", value: data.risk_distribution?.critique ?? 0 },
            { label: "Index Moyen", value: data.avg_estimated_genetic_discrimination_index ?? "—" },
            { label: "Confiance", value: `${Math.round((data.confidence_score ?? 0) * 100)}%` },
            { label: "Dernière Analyse", value: data.last_analysis ?? "—" },
            { label: "Version", value: data.engine_version ?? "—" },
          ].map(k => (
            <div key={k.label} className="bg-slate-900 border border-slate-800 rounded-xl p-4">
              <div className="text-xs text-slate-500 mb-1">{k.label}</div>
              <div className="text-xl font-bold text-emerald-400">{k.value}</div>
            </div>
          ))}
        </div>

        {/* Sub-scores gauges */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
          <h2 className="text-sm font-semibold text-slate-400 uppercase tracking-wider mb-4">Sous-scores Moyens</h2>
          <div className="flex flex-wrap justify-around gap-6">
            {subKeys.map(({ key, label }) => (
              <div key={key} className="flex flex-col items-center gap-2">
                <GaugeRing value={avgSub(key)} stroke="#34d399" />
                <span className="text-xs text-slate-400 text-center max-w-[100px]">{label}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Risk distribution */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
            <h2 className="text-sm font-semibold text-slate-400 uppercase tracking-wider mb-3">Distribution des Risques</h2>
            <div className="space-y-2">
              {[
                { label: "Critique", key: "critique", color: "#ef4444" },
                { label: "Élevé", key: "élevé", color: "#f97316" },
                { label: "Modéré", key: "modéré", color: "#eab308" },
                { label: "Faible", key: "faible", color: "#10b981" },
              ].map(({ label, key, color }) => {
                const val = data.risk_distribution?.[key] ?? 0;
                const pct = data.total_entities > 0 ? Math.round(val / data.total_entities * 100) : 0;
                return (
                  <div key={key} className="flex items-center gap-3">
                    <span className="text-xs text-slate-400 w-20 shrink-0">{label}</span>
                    <div className="flex-1 h-2.5 bg-slate-800 rounded-full overflow-hidden">
                      <div className="h-full rounded-full" style={{ width: `${pct}%`, backgroundColor: color }} />
                    </div>
                    <span className="text-xs text-slate-300 w-6 text-right">{val}</span>
                  </div>
                );
              })}
            </div>
          </div>
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
            <h2 className="text-sm font-semibold text-slate-400 uppercase tracking-wider mb-3">Patterns de Discrimination</h2>
            <div className="space-y-2">
              {Object.entries(data.pattern_distribution ?? {}).map(([k, v], i) => {
                const colors = ["#34d399", "#f97316", "#eab308", "#ef4444", "#818cf8"];
                const pct = data.total_entities > 0 ? Math.round((v as number) / data.total_entities * 100) : 0;
                return (
                  <div key={k} className="flex items-center gap-3">
                    <span className="text-xs text-slate-400 w-44 shrink-0 truncate">{k.replace(/_/g, " ")}</span>
                    <div className="flex-1 h-2.5 bg-slate-800 rounded-full overflow-hidden">
                      <div className="h-full rounded-full" style={{ width: `${pct}%`, backgroundColor: colors[i % colors.length] }} />
                    </div>
                    <span className="text-xs text-slate-300 w-6 text-right">{v as number}</span>
                  </div>
                );
              })}
            </div>
          </div>
        </div>

        {/* Critical alerts */}
        {(data.critical_alerts?.length ?? 0) > 0 && (
          <div className="border border-emerald-500/30 bg-emerald-500/10 rounded-xl p-4">
            <h2 className="text-sm font-semibold text-emerald-400 mb-2">Alertes Critiques</h2>
            <ul className="space-y-1">
              {data.critical_alerts.map((a, i) => (
                <li key={i} className="text-sm text-slate-300 flex items-center gap-2">
                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 shrink-0" />
                  {a}
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Filter pills */}
        <div className="flex gap-2 flex-wrap">
          {["tous", "critique", "élevé", "modéré", "faible"].map(f => (
            <button key={f} onClick={() => setFilter(f)}
              className={`px-4 py-1.5 rounded-full text-sm border transition-all capitalize ${filter === f ? "bg-emerald-500 border-emerald-400 text-white" : "bg-slate-800 border-slate-700 text-slate-400 hover:border-slate-500"}`}>
              {f}
            </button>
          ))}
        </div>

        {/* Entity grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {filtered.map(entity => (
            <div key={entity.id} onClick={() => { setSelected(entity); setTab(0); }}
              className={`bg-slate-900 border rounded-xl p-4 cursor-pointer hover:border-emerald-500/50 transition-all ${RB[entity.risk_level] ?? "border-slate-800"}`}>
              <div className="flex justify-between items-start mb-3">
                <div className="flex-1 min-w-0">
                  <p className="text-xs font-mono text-slate-500">{entity.id}</p>
                  <p className="text-sm font-semibold text-white truncate">{entity.name}</p>
                  <p className="text-xs text-slate-500">{entity.country}</p>
                </div>
                <GaugeRing value={entity.composite_score} stroke="#34d399" />
              </div>
              <div className="flex justify-between text-xs">
                <span className={RC[entity.risk_level]}>{entity.risk_level}</span>
                <span className="text-slate-500">idx {entity.estimated_genetic_discrimination_index}</span>
              </div>
            </div>
          ))}
        </div>

        <p className="text-xs text-slate-600 text-center">Caelum Partners · Discrimination Génétique · {data.last_analysis}</p>
      </div>

      {/* Detail Modal */}
      {selected && (
        <div className="fixed inset-0 bg-black/70 flex items-center justify-center z-50 p-4" onClick={() => setSelected(null)}>
          <div className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-2xl max-h-[85vh] overflow-y-auto" onClick={e => e.stopPropagation()}>
            <div className="p-6 border-b border-slate-800 flex justify-between items-start">
              <div>
                <p className="text-xs text-slate-500 mb-1">{selected.id}</p>
                <h3 className="font-bold text-lg">{selected.name}</h3>
                <p className="text-xs text-slate-400 mt-1">{selected.country} · {selected.sector}</p>
                <p className={`text-xs font-bold uppercase mt-1 ${RC[selected.risk_level]}`}>{selected.risk_level}</p>
              </div>
              <button onClick={() => setSelected(null)} className="text-slate-500 hover:text-white text-xl leading-none">×</button>
            </div>
            <div className="flex border-b border-slate-800">
              {["Aperçu", "Métriques", "Sources"].map((t, i) => (
                <button key={t} onClick={() => setTab(i)}
                  className={`px-6 py-3 text-sm font-medium transition-colors ${tab === i ? "border-b-2 border-emerald-500 text-emerald-400" : "text-slate-500 hover:text-slate-300"}`}>
                  {t}
                </button>
              ))}
            </div>
            <div className="p-6">
              {tab === 0 && (
                <div className="space-y-4">
                  <div className="flex items-center gap-4">
                    <GaugeRing value={selected.composite_score} stroke="#34d399" />
                    <div>
                      <div className="text-2xl font-bold text-emerald-400">{selected.composite_score.toFixed(1)}</div>
                      <div className="text-xs text-slate-400">Score composite</div>
                      <div className="text-xs text-slate-500 mt-1">Pattern: {selected.primary_pattern}</div>
                    </div>
                  </div>
                  <div className="bg-slate-800 rounded-lg p-3">
                    <div className="text-xs text-slate-500 mb-1">Index Discrimination Génétique</div>
                    <div className="text-lg font-bold text-emerald-400">{selected.estimated_genetic_discrimination_index}</div>
                  </div>
                </div>
              )}
              {tab === 1 && (
                <div className="space-y-3">
                  {subKeys.map(({ key, label }) => {
                    const val = selected[key] as number;
                    return (
                      <div key={key}>
                        <div className="flex justify-between text-xs text-slate-400 mb-1">
                          <span>{label}</span><span>{val}/100</span>
                        </div>
                        <div className="h-2 bg-slate-800 rounded-full">
                          <div className="h-full rounded-full bg-emerald-500" style={{ width: `${val}%` }} />
                        </div>
                      </div>
                    );
                  })}
                </div>
              )}
              {tab === 2 && (
                <ul className="space-y-2">
                  {(selected.key_signals ?? []).map((s, i) => (
                    <li key={i} className="flex gap-2 text-sm text-slate-300">
                      <span className="text-emerald-400 shrink-0 mt-0.5">▸</span>{s}
                    </li>
                  ))}
                </ul>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
