"use client";
import { useState, useEffect } from "react";

const RC: Record<string,string> = { critique:"text-red-400","élevé":"text-orange-400",modéré:"text-yellow-400",faible:"text-emerald-400" };
const RB: Record<string,string> = { critique:"border-red-500/30 bg-red-500/10","élevé":"border-orange-500/30 bg-orange-500/10",modéré:"border-yellow-500/30 bg-yellow-500/10",faible:"border-emerald-500/30 bg-emerald-500/10" };

const ACCENT = "#6b21a8";

interface Entity {
  entity_id: string;
  name: string;
  country: string;
  sector: string;
  composite_score: number;
  platform_blocking_scope_score: number;
  content_removal_political_score: number;
  algorithmic_suppression_score: number;
  user_data_state_access_score: number;
  estimated_social_media_censorship_index: number;
  risk_level: string;
  primary_pattern: string;
  key_signals: string[];
  last_updated: string;
  [key: string]: unknown;
}

interface DashData {
  total_entities: number;
  avg_composite: number;
  avg_estimated_social_media_censorship_index: number;
  risk_distribution: Record<string, number>;
  pattern_distribution: Record<string, number>;
  confidence_score: number;
  data_sources: string[];
  entities: Entity[];
  [key: string]: unknown;
}

function GaugeRing({ value, label }: { value: number; label: string }) {
  const r = 36;
  const circ = 226.19;
  const fill = circ * (1 - Math.min(value, 100) / 100);
  return (
    <div className="flex flex-col items-center gap-1">
      <svg width="88" height="88" viewBox="0 0 88 88">
        <circle cx="44" cy="44" r={r} fill="none" stroke="#1e293b" strokeWidth="8" />
        <circle
          cx="44" cy="44" r={r} fill="none" stroke={ACCENT} strokeWidth="8"
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

export default function Page() {
  const [data, setData] = useState<DashData | null>(null);
  const [filter, setFilter] = useState("tous");
  const [selected, setSelected] = useState<Entity | null>(null);
  const [tab, setTab] = useState(0);

  useEffect(() => {
    fetch("/api/social-media-censorship-engine")
      .then(r => r.json())
      .then(j => setData(j.payload ?? j.data ?? j));
  }, []);

  if (!data) return (
    <div className="bg-slate-950 min-h-screen flex items-center justify-center">
      <div className="text-purple-400 animate-pulse">Initialisation du Moteur Censure Réseaux Sociaux…</div>
    </div>
  );

  const filters = ["tous", "critique", "élevé", "modéré", "faible"];
  const allEntities: Entity[] = data.entities ?? [];
  const entities = allEntities.filter(e => filter === "tous" || e.risk_level === filter);
  const rd = data.risk_distribution ?? {};
  const critCount = rd["critique"] ?? 0;
  const sources = Array.isArray(data.data_sources) ? data.data_sources.length : 0;
  const confidence = typeof data.confidence_score === "number"
    ? `${(data.confidence_score * 100).toFixed(0)}%`
    : "—";
  const avgIndex = typeof data.avg_estimated_social_media_censorship_index === "number"
    ? data.avg_estimated_social_media_censorship_index.toFixed(2)
    : "—";

  const kpis = [
    { label: "Entités", value: data.total_entities ?? allEntities.length },
    { label: "Score moyen", value: typeof data.avg_composite === "number" ? data.avg_composite.toFixed(1) : "—" },
    { label: "Index Censure", value: avgIndex },
    { label: "Confiance", value: confidence },
    { label: "Critique", value: critCount },
    { label: "Sources", value: sources },
  ];

  return (
    <div className="bg-slate-950 min-h-screen text-slate-100 p-6 space-y-6">
      {/* Header */}
      <div>
        <div className="flex items-center gap-3 mb-1">
          <div className="w-3 h-3 rounded-full" style={{ background: ACCENT }} />
          <h1 className="text-2xl font-bold tracking-tight">Censure Réseaux Sociaux</h1>
        </div>
        <p className="text-slate-400 text-sm ml-6">
          Blocage de plateformes, suppression de contenus et surveillance étatique des réseaux sociaux
        </p>
      </div>

      {/* KPI Cards 3×2 */}
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
          {(() => {
            const avg = (key: keyof Entity) => {
              if (allEntities.length === 0) return 0;
              return allEntities.reduce((a, e) => a + (Number(e[key]) || 0), 0) / allEntities.length;
            };
            return [
              { label: "Blocage Plateformes", key: "platform_blocking_scope_score" as keyof Entity },
              { label: "Suppression Politique", key: "content_removal_political_score" as keyof Entity },
              { label: "Suppression Algorithmique", key: "algorithmic_suppression_score" as keyof Entity },
              { label: "Accès État aux Données", key: "user_data_state_access_score" as keyof Entity },
            ].map(s => (
              <GaugeRing key={s.key} value={avg(s.key)} label={s.label} />
            ));
          })()}
        </div>
      </div>

      {/* Filter pills */}
      <div className="flex gap-2 flex-wrap">
        {filters.map(f => (
          <button key={f} onClick={() => setFilter(f)}
            className={`px-4 py-1.5 rounded-full text-sm font-medium transition-all ${filter === f ? "text-white font-bold" : "bg-slate-800 text-slate-400 hover:bg-slate-700"}`}
            style={filter === f ? { background: ACCENT } : {}}>
            {f.charAt(0).toUpperCase() + f.slice(1)}
          </button>
        ))}
      </div>

      {/* Entity grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
        {entities.map(e => (
          <div key={e.entity_id} onClick={() => { setSelected(e); setTab(0); }}
            className={`border rounded-xl p-4 cursor-pointer hover:scale-[1.01] transition-transform ${RB[e.risk_level] ?? "border-slate-700 bg-slate-900"}`}>
            <div className="flex justify-between items-start mb-2">
              <div className="flex-1 min-w-0">
                <div className="font-semibold text-sm leading-tight truncate">{e.name}</div>
                <div className="text-xs text-slate-400 mt-1">{e.country}</div>
                <div className="text-xs text-slate-500 mt-0.5">{e.sector}</div>
              </div>
              <div className="text-right ml-3">
                <div className="text-xl font-bold text-white">{e.composite_score.toFixed(1)}</div>
                <div className={`text-xs font-bold uppercase mt-1 ${RC[e.risk_level] ?? "text-slate-400"}`}>{e.risk_level}</div>
              </div>
            </div>
            <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden mt-2">
              <div className="h-full rounded-full transition-all" style={{ width: `${Math.min(e.composite_score, 100)}%`, background: ACCENT }} />
            </div>
            <div className="text-xs text-slate-500 mt-2">
              Index Censure: <span className="font-medium text-purple-300">{e.estimated_social_media_censorship_index}</span>
            </div>
          </div>
        ))}
      </div>

      {entities.length === 0 && (
        <div className="text-center py-12 text-slate-500 text-sm">Aucune entité pour ce niveau de risque.</div>
      )}

      {/* Detail Modal */}
      {selected && (
        <div className="fixed inset-0 bg-black/70 flex items-center justify-center z-50 p-4" onClick={() => setSelected(null)}>
          <div className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-2xl max-h-[85vh] overflow-y-auto" onClick={e => e.stopPropagation()}>
            <div className="p-6 border-b border-slate-800 flex justify-between items-start">
              <div>
                <h3 className="font-bold text-lg">{selected.name}</h3>
                <div className="text-xs text-slate-400 mt-1">{selected.country} · {selected.sector}</div>
                <div className={`text-xs font-bold uppercase mt-1 ${RC[selected.risk_level] ?? "text-slate-400"}`}>{selected.risk_level}</div>
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
                    <div>
                      <div className="text-3xl font-bold text-white">{selected.composite_score.toFixed(1)}</div>
                      <div className="text-xs text-slate-400">Score composite</div>
                    </div>
                    <div className="ml-auto text-right">
                      <div className="text-lg font-bold text-purple-300">{selected.estimated_social_media_censorship_index}</div>
                      <div className="text-xs text-slate-500">Index Censure</div>
                    </div>
                  </div>
                  <div className="grid grid-cols-2 gap-3">
                    {[
                      { label: "Blocage Plateformes", value: selected.platform_blocking_scope_score },
                      { label: "Suppression Politique", value: selected.content_removal_political_score },
                      { label: "Suppression Algorithmique", value: selected.algorithmic_suppression_score },
                      { label: "Accès État aux Données", value: selected.user_data_state_access_score },
                    ].map(s => (
                      <div key={s.label} className="bg-slate-800 rounded-lg p-3">
                        <div className="text-xs text-slate-500 mb-1">{s.label}</div>
                        <div className="text-lg font-bold" style={{ color: ACCENT }}>
                          {typeof s.value === "number" ? s.value.toFixed(1) : "—"}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
              {tab === 1 && (
                <ul className="space-y-3">
                  {(selected.key_signals ?? []).map((s, i) => (
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
                  <div><span className="text-slate-500">Pattern: </span>{selected.primary_pattern}</div>
                  <div><span className="text-slate-500">Dernière MAJ: </span>{selected.last_updated}</div>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
