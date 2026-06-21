"use client";
import { useState, useEffect } from "react";

const ACCENT = "#f472b6";
const RC: Record<string, string> = { critique: "text-red-400", "élevé": "text-orange-400", modéré: "text-yellow-400", faible: "text-emerald-400" };
const RB: Record<string, string> = { critique: "border-red-500/30 bg-red-500/10", "élevé": "border-orange-500/30 bg-orange-500/10", modéré: "border-yellow-500/30 bg-yellow-500/10", faible: "border-emerald-500/30 bg-emerald-500/10" };

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

interface Entity {
  id: string;
  name: string;
  country: string;
  sector: string;
  composite_score: number;
  abstinence_only_policy_harm_scale_score: number;
  lgbtq_exclusion_curriculum_severity_score: number;
  reproductive_health_information_denial_score: number;
  school_dropout_unwanted_pregnancy_score: number;
  risk_level: string;
  primary_pattern: string;
  key_signals: string[];
  estimated_sex_education_rights_index: number;
  last_updated: string;
  [key: string]: unknown;
}

interface DashData {
  total_entities: number;
  avg_composite: number;
  risk_distribution: Record<string, number>;
  confidence_score: number;
  entities: Entity[];
  avg_estimated_sex_education_rights_index: number;
}

const SUB_SCORES = [
  { key: "abstinence_only_policy_harm_scale_score", label: "Politique Abstinence Seule" },
  { key: "lgbtq_exclusion_curriculum_severity_score", label: "Exclusion LGBT+ Curriculum" },
  { key: "reproductive_health_information_denial_score", label: "Déni Info Santé Reproductive" },
  { key: "school_dropout_unwanted_pregnancy_score", label: "Décrochage & Grossesses" },
];

export default function Page() {
  const [data, setData] = useState<DashData | null>(null);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState("tous");
  const [selected, setSelected] = useState<Entity | null>(null);
  const [tab, setTab] = useState(0);

  useEffect(() => {
    fetch("/api/sex-education-rights-engine").then(r => r.json()).then(d => { setData(d.payload ?? d); setLoading(false); });
  }, []);

  if (loading || !data) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-slate-400">Chargement...</div>
    </div>
  );

  const filtered = data.entities.filter(e => filter === "tous" || e.risk_level === filter);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-pink-400">Droits à l&apos;Éducation Sexuelle</h1>
        <p className="text-slate-400 mt-1">Sex Education Rights Engine</p>
      </div>

      {/* KPI Grid 3×2 */}
      <div className="grid grid-cols-3 gap-4 mb-8">
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
          <p className="text-xs text-slate-500 uppercase tracking-wide">Entités</p>
          <p className="text-3xl font-bold mt-1 text-pink-400">{data.total_entities}</p>
        </div>
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 flex flex-col items-center">
          <p className="text-xs text-slate-500 uppercase tracking-wide mb-2">Score Moyen</p>
          <GaugeRing value={data.avg_composite} stroke={ACCENT} />
        </div>
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
          <p className="text-xs text-slate-500 uppercase tracking-wide">Critique</p>
          <p className="text-3xl font-bold mt-1 text-red-400">{data.risk_distribution?.critique ?? 0}</p>
        </div>
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
          <p className="text-xs text-slate-500 uppercase tracking-wide">Élevé</p>
          <p className="text-3xl font-bold mt-1 text-orange-400">{data.risk_distribution?.["élevé"] ?? 0}</p>
        </div>
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
          <p className="text-xs text-slate-500 uppercase tracking-wide">Index Moyen</p>
          <p className="text-3xl font-bold mt-1 text-pink-400">{data.avg_estimated_sex_education_rights_index}</p>
        </div>
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
          <p className="text-xs text-slate-500 uppercase tracking-wide">Confidence</p>
          <p className="text-3xl font-bold mt-1 text-pink-400">{Math.round((data.confidence_score ?? 0) * 100)}%</p>
        </div>
      </div>

      {/* Filter pills */}
      <div className="flex gap-2 mb-6 flex-wrap">
        {["tous", "critique", "élevé", "modéré", "faible"].map(f => (
          <button key={f} onClick={() => setFilter(f)}
            className={`px-4 py-1.5 rounded-full text-sm font-medium border transition-colors ${filter === f ? "border-transparent text-white bg-pink-500" : "border-slate-700 text-slate-400 hover:border-slate-500"}`}>
            {f.charAt(0).toUpperCase() + f.slice(1)}
          </button>
        ))}
      </div>

      {/* Entity grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4 mb-8">
        {filtered.map(e => (
          <button key={e.id} onClick={() => { setSelected(e); setTab(0); }}
            className={`text-left border rounded-xl p-4 transition-all hover:scale-[1.01] ${RB[e.risk_level]}`}>
            <div className="flex justify-between items-start mb-2">
              <span className="text-xs font-mono text-slate-500">{e.id}</span>
              <span className={`text-xs font-semibold uppercase ${RC[e.risk_level]}`}>{e.risk_level}</span>
            </div>
            <p className="font-semibold text-sm text-slate-100 line-clamp-2 mb-2">{e.name}</p>
            <p className="text-xs text-slate-400">{e.country}</p>
            <div className="mt-3 flex items-center justify-between">
              <span className="text-xs text-slate-500">Score composite</span>
              <span className="text-lg font-bold text-pink-400">{e.composite_score}</span>
            </div>
          </button>
        ))}
      </div>

      {/* Detail Modal */}
      {selected && (
        <div className="fixed inset-0 bg-black/70 z-50 flex items-center justify-center p-4" onClick={() => setSelected(null)}>
          <div className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-2xl max-h-[85vh] overflow-y-auto"
            onClick={e => e.stopPropagation()}>
            <div className="p-6 border-b border-slate-800 flex justify-between items-start">
              <div>
                <span className={`text-xs font-semibold uppercase ${RC[selected.risk_level]}`}>{selected.risk_level}</span>
                <h2 className="text-lg font-bold text-slate-100 mt-1">{selected.name}</h2>
                <p className="text-sm text-slate-400">{selected.country}</p>
              </div>
              <button onClick={() => setSelected(null)} className="text-slate-500 hover:text-white text-xl">✕</button>
            </div>
            {/* Tabs */}
            <div className="flex border-b border-slate-800">
              {["Vue générale", "Sous-scores", "Alertes"].map((t, i) => (
                <button key={t} onClick={() => setTab(i)}
                  className={`flex-1 py-3 text-sm font-medium transition-colors ${tab === i ? "text-white border-b-2 border-pink-400" : "text-slate-400"}`}>
                  {t}
                </button>
              ))}
            </div>
            <div className="p-6">
              {tab === 0 && (
                <div className="space-y-4">
                  <div className="flex justify-between items-center">
                    <span className="text-slate-400">Score composite</span>
                    <span className="text-2xl font-bold text-pink-400">{selected.composite_score}/100</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-slate-400">Index éducation sexuelle</span>
                    <span className="text-slate-200">{selected.estimated_sex_education_rights_index}</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-slate-400">Patron principal</span>
                    <span className="text-slate-200">{selected.primary_pattern?.replace(/_/g, " ")}</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-slate-400">Secteur</span>
                    <span className="text-slate-200">{selected.sector}</span>
                  </div>
                </div>
              )}
              {tab === 1 && (
                <div className="space-y-3">
                  {SUB_SCORES.map(({ key, label }) => (
                    <div key={key}>
                      <div className="flex justify-between text-sm mb-1">
                        <span className="text-slate-400">{label}</span>
                        <span className="text-slate-200">{selected[key] as number}/100</span>
                      </div>
                      <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
                        <div className="h-full rounded-full bg-pink-400" style={{ width: `${selected[key] as number}%` }} />
                      </div>
                    </div>
                  ))}
                </div>
              )}
              {tab === 2 && (
                <ul className="space-y-3">
                  {(selected.key_signals ?? []).map((s, i) => (
                    <li key={i} className="flex gap-3 text-sm">
                      <span className="text-pink-400 mt-0.5 shrink-0">▸</span>
                      <span className="text-slate-300">{s}</span>
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
