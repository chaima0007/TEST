"use client";
import { useEffect, useState } from "react";

const ACCENT = "#ec4899";

const RC: Record<string, string> = { critique: "text-red-400", "élevé": "text-orange-400", modéré: "text-yellow-400", faible: "text-emerald-400" };
const RB: Record<string, string> = { critique: "border-red-500/30 bg-red-500/10", "élevé": "border-orange-500/30 bg-orange-500/10", modéré: "border-yellow-500/30 bg-yellow-500/10", faible: "border-emerald-500/30 bg-emerald-500/10" };

function GaugeRing({ value, max = 100 }: { value: number; max?: number }) {
  const r = 36, circ = 2 * Math.PI * r;
  const pct = Math.min(value / max, 1);
  return (
    <svg width="88" height="88" viewBox="0 0 88 88">
      <circle cx="44" cy="44" r={r} fill="none" stroke="#1e293b" strokeWidth="8" />
      <circle cx="44" cy="44" r={r} fill="none" stroke={ACCENT} strokeWidth="8"
        strokeDasharray={`${pct * circ} ${circ}`} strokeLinecap="round"
        transform="rotate(-90 44 44)" />
      <text x="44" y="49" textAnchor="middle" fill="white" fontSize="13" fontWeight="bold">
        {value.toFixed(1)}
      </text>
    </svg>
  );
}

interface Entity {
  id: string; name: string; country: string; sector: string;
  composite_score: number; risk_level: string; primary_pattern: string;
  key_signals: string[]; [key: string]: unknown;
}
interface DashData {
  total_entities: number; avg_composite: number;
  risk_distribution: Record<string, number>; pattern_distribution: Record<string, number>;
  top_risk_entities: string[]; critical_alerts: string[];
  last_analysis: string; confidence_score: number;
  data_sources: string[]; entities: Entity[]; [key: string]: unknown;
}

export default function Page() {
  const [data, setData] = useState<DashData | null>(null);
  const [filter, setFilter] = useState("tous");
  const [selected, setSelected] = useState<Entity | null>(null);
  const [tab, setTab] = useState(0);

  useEffect(() => {
    fetch("/api/psychological-warfare-engine").then(r => r.json()).then(j => setData(j.payload ?? j));
  }, []);

  if (!data) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-slate-400 animate-pulse">Chargement…</div>
    </div>
  );

  const PATTERN_LABELS: Record<string, string> = {
    desinformation_echelle_industrielle: "Désinformation Industrielle",
    terreur_psychologique_civils: "Terreur Psychologique",
    erosion_cohesion_sociale: "Érosion Cohésion Sociale",
    impunite_attribution_psyop: "Impunité Attribution PSYOP",
  };
  const SCORE_KEYS = [
    "disinformation_scale_sophistication_score",
    "civilian_psychological_terror_score",
    "social_cohesion_erosion_score",
    "psyop_impunity_attribution_score",
  ];
  const filters = ["tous", "critique", "élevé", "modéré", "faible"];
  const entities = data.entities.filter(e => filter === "tous" || e.risk_level === filter);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-2">
          <div className="w-3 h-3 rounded-full" style={{ background: ACCENT }} />
          <h1 className="text-2xl font-bold tracking-tight">Psychological Warfare Engine</h1>
        </div>
        <p className="text-slate-400 text-sm ml-6">Surveillance de la guerre psychologique, désinformation et PSYOP</p>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4 mb-8">
        {[
          { label: "Total Acteurs", value: data.total_entities },
          { label: "Risque Moyen", value: data.avg_composite?.toFixed(1) },
          { label: "Critiques", value: data.risk_distribution?.critique },
          { label: "Confidence", value: `${(data.confidence_score * 100).toFixed(0)}%` },
          { label: "Alertes", value: data.critical_alerts?.length },
          { label: "Dernière Analyse", value: data.last_analysis },
        ].map(k => (
          <div key={k.label} className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-500 mb-1">{k.label}</div>
            <div className="text-xl font-bold" style={{ color: ACCENT }}>{k.value}</div>
          </div>
        ))}
      </div>

      <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 mb-6">
        <h2 className="text-sm font-semibold text-slate-400 mb-3">Distribution des patterns</h2>
        <div className="flex flex-wrap gap-2">
          {Object.entries(data.pattern_distribution ?? {}).map(([k, v]) => (
            <span key={k} className="text-xs px-3 py-1 rounded-full bg-slate-800 text-slate-300">
              {PATTERN_LABELS[k] ?? k}: <span style={{ color: ACCENT }}>{v}</span>
            </span>
          ))}
        </div>
      </div>

      <div className="flex gap-2 mb-6 flex-wrap">
        {filters.map(f => (
          <button key={f} onClick={() => setFilter(f)}
            className={`px-4 py-1.5 rounded-full text-sm font-medium transition-all ${filter === f ? "text-slate-950 font-bold" : "bg-slate-800 text-slate-400 hover:bg-slate-700"}`}
            style={filter === f ? { background: ACCENT } : {}}>
            {f.charAt(0).toUpperCase() + f.slice(1)}
          </button>
        ))}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4 mb-8">
        {entities.map(e => (
          <div key={e.id} onClick={() => { setSelected(e); setTab(0); }}
            className={`border rounded-xl p-4 cursor-pointer hover:scale-[1.01] transition-transform ${RB[e.risk_level] ?? "border-slate-700 bg-slate-900"}`}>
            <div className="flex justify-between items-start mb-3">
              <div className="flex-1 min-w-0">
                <div className="text-xs text-slate-500 mb-1">{e.id}</div>
                <div className="font-semibold text-sm leading-tight truncate">{e.name}</div>
                <div className="text-xs text-slate-400 mt-1">{e.country}</div>
              </div>
              <GaugeRing value={e.composite_score} />
            </div>
            <div className={`text-xs font-bold uppercase ${RC[e.risk_level]}`}>{e.risk_level}</div>
          </div>
        ))}
      </div>

      {data.critical_alerts?.length > 0 && (
        <div className="bg-red-950/30 border border-red-500/20 rounded-xl p-4 mb-6">
          <h2 className="text-sm font-semibold text-red-400 mb-3">Alertes Critiques</h2>
          <ul className="space-y-1">
            {data.critical_alerts.map((a, i) => (
              <li key={i} className="text-xs text-slate-300 flex items-center gap-2">
                <span className="w-1.5 h-1.5 rounded-full bg-red-400 shrink-0" />
                {a}
              </li>
            ))}
          </ul>
        </div>
      )}

      {selected && (
        <div className="fixed inset-0 bg-black/70 flex items-center justify-center z-50 p-4" onClick={() => setSelected(null)}>
          <div className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-2xl max-h-[85vh] overflow-y-auto" onClick={e => e.stopPropagation()}>
            <div className="p-6 border-b border-slate-800 flex justify-between items-start">
              <div>
                <div className="text-xs text-slate-500 mb-1">{selected.id}</div>
                <h3 className="font-bold text-lg">{selected.name}</h3>
                <div className={`text-xs font-bold uppercase mt-1 ${RC[selected.risk_level]}`}>{selected.risk_level}</div>
              </div>
              <button onClick={() => setSelected(null)} className="text-slate-500 hover:text-white text-xl leading-none">×</button>
            </div>
            <div className="flex border-b border-slate-800">
              {["Aperçu", "Signaux", "Contexte"].map((t, i) => (
                <button key={t} onClick={() => setTab(i)}
                  className={`px-6 py-3 text-sm font-medium transition-colors ${tab === i ? "border-b-2 text-white" : "text-slate-500 hover:text-slate-300"}`}
                  style={tab === i ? { borderColor: ACCENT, color: ACCENT } : {}}>
                  {t}
                </button>
              ))}
            </div>
            <div className="p-6">
              {tab === 0 && (
                <div className="space-y-4">
                  <div className="flex items-center gap-4">
                    <GaugeRing value={selected.composite_score} />
                    <div>
                      <div className="text-2xl font-bold">{selected.composite_score.toFixed(1)}</div>
                      <div className="text-xs text-slate-400">Score composite</div>
                      <div className="text-xs text-slate-500 mt-1">Pattern: {PATTERN_LABELS[selected.primary_pattern] ?? selected.primary_pattern}</div>
                    </div>
                  </div>
                  <div className="grid grid-cols-2 gap-3 mt-4">
                    {SCORE_KEYS.map(key => (
                      <div key={key} className="bg-slate-800 rounded-lg p-3">
                        <div className="text-xs text-slate-500 mb-1">{key.replace(/_score$/, "").replace(/_/g, " ")}</div>
                        <div className="text-lg font-bold" style={{ color: ACCENT }}>{(selected[key] as number)?.toFixed(1) ?? "-"}</div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
              {tab === 1 && (
                <ul className="space-y-3">
                  {selected.key_signals?.map((s, i) => (
                    <li key={i} className="flex gap-2 text-sm text-slate-300">
                      <span style={{ color: ACCENT }} className="shrink-0 mt-0.5">▸</span>
                      {s}
                    </li>
                  ))}
                </ul>
              )}
              {tab === 2 && (
                <div className="space-y-3 text-sm text-slate-300">
                  <div><span className="text-slate-500">Pays: </span>{selected.country}</div>
                  <div><span className="text-slate-500">Secteur: </span>{selected.sector}</div>
                  <div><span className="text-slate-500">Dernière MAJ: </span>{String(selected.last_updated)}</div>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
