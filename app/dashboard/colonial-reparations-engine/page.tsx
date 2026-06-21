"use client";
import { useState, useEffect } from "react";

const RC: Record<string,string> = { critique:"text-red-400","élevé":"text-orange-400",modéré:"text-yellow-400",faible:"text-emerald-400" };
const RB: Record<string,string> = { critique:"border-red-500/30 bg-red-500/10","élevé":"border-orange-500/30 bg-orange-500/10",modéré:"border-yellow-500/30 bg-yellow-500/10",faible:"border-emerald-500/30 bg-emerald-500/10" };

interface Entity {
  id: string;
  name: string;
  country: string;
  composite_score: number;
  economic_extraction_scale_score: number;
  cultural_artifact_restitution_gap_score: number;
  structural_inequality_persistence_score: number;
  political_acknowledgment_refusal_score: number;
  risk_level: string;
  primary_pattern: string;
  estimated_colonial_reparations_index: number;
}

interface ApiData {
  total_entities: number;
  avg_composite: number;
  confidence_score: number;
  risk_distribution: Record<string, number>;
  top_risk_entities: Entity[];
  avg_estimated_colonial_reparations_index: number;
  entities: Entity[];
}

function GaugeRing({ value, max = 100, color }: { value: number; max?: number; color: string }) {
  const r = 36;
  const cx = 44;
  const cy = 44;
  const circumference = 226.19;
  const pct = Math.min(Math.max(value / max, 0), 1);
  const dash = pct * circumference;
  return (
    <svg viewBox="0 0 88 88" className="w-16 h-16">
      <circle cx={cx} cy={cy} r={r} fill="none" stroke="#1e293b" strokeWidth="8" />
      <circle
        cx={cx} cy={cy} r={r} fill="none"
        stroke="currentColor" strokeWidth="8"
        strokeDasharray={`${dash} ${circumference}`}
        strokeLinecap="round"
        transform="rotate(-90 44 44)"
        className={color}
      />
      <text x={cx} y={cy + 5} textAnchor="middle" className="fill-white text-xs font-bold" fontSize="12">
        {Math.round(value)}
      </text>
    </svg>
  );
}

function DetailModal({ entity, onClose }: { entity: Entity; onClose: () => void }) {
  const [tab, setTab] = useState<"apercu"|"signaux"|"contexte">("apercu");
  return (
    <div className="fixed inset-0 bg-black/70 flex items-center justify-center z-50 p-4" onClick={onClose}>
      <div className="bg-slate-900 border border-amber-500/30 rounded-xl w-full max-w-2xl p-6" onClick={e => e.stopPropagation()}>
        <div className="flex items-start justify-between mb-4">
          <div>
            <h2 className="text-xl font-bold text-white">{entity.name}</h2>
            <p className="text-slate-400 text-sm">{entity.country} · {entity.id}</p>
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-white text-2xl leading-none">&times;</button>
        </div>
        <div className={`inline-flex items-center px-3 py-1 rounded-full border text-xs font-semibold mb-4 ${RB[entity.risk_level] ?? ""} ${RC[entity.risk_level] ?? ""}`}>
          {entity.risk_level}
        </div>
        <div className="flex gap-2 mb-6">
          {(["apercu","signaux","contexte"] as const).map(t => (
            <button key={t} onClick={() => setTab(t)}
              className={`px-4 py-1.5 rounded-lg text-sm font-medium transition-colors ${tab === t ? "bg-amber-500/20 text-amber-400 border border-amber-500/40" : "text-slate-400 hover:text-white"}`}>
              {t === "apercu" ? "Aperçu" : t === "signaux" ? "Signaux" : "Contexte"}
            </button>
          ))}
        </div>
        {tab === "apercu" && (
          <div className="space-y-3">
            <div className="flex justify-between text-sm"><span className="text-slate-400">Score composite</span><span className="text-white font-semibold">{entity.composite_score?.toFixed(2)}</span></div>
            <div className="flex justify-between text-sm"><span className="text-slate-400">Indice réparations coloniales</span><span className="text-amber-400 font-semibold">{entity.estimated_colonial_reparations_index?.toFixed(2)}</span></div>
            <div className="flex justify-between text-sm"><span className="text-slate-400">Modèle principal</span><span className="text-white">{entity.primary_pattern}</span></div>
          </div>
        )}
        {tab === "signaux" && (
          <div className="space-y-3">
            <div className="flex justify-between text-sm"><span className="text-slate-400">Extraction économique</span><span className="text-white">{entity.economic_extraction_scale_score?.toFixed(2)}</span></div>
            <div className="flex justify-between text-sm"><span className="text-slate-400">Restitution artefacts culturels</span><span className="text-white">{entity.cultural_artifact_restitution_gap_score?.toFixed(2)}</span></div>
            <div className="flex justify-between text-sm"><span className="text-slate-400">Persistance inégalités structurelles</span><span className="text-white">{entity.structural_inequality_persistence_score?.toFixed(2)}</span></div>
            <div className="flex justify-between text-sm"><span className="text-slate-400">Refus reconnaissance politique</span><span className="text-white">{entity.political_acknowledgment_refusal_score?.toFixed(2)}</span></div>
          </div>
        )}
        {tab === "contexte" && (
          <div className="space-y-3">
            <div className="flex justify-between text-sm"><span className="text-slate-400">Pays</span><span className="text-white">{entity.country}</span></div>
            <div className="flex justify-between text-sm"><span className="text-slate-400">Niveau de risque</span><span className={RC[entity.risk_level] ?? "text-white"}>{entity.risk_level}</span></div>
            <div className="flex justify-between text-sm"><span className="text-slate-400">Modèle principal</span><span className="text-white">{entity.primary_pattern}</span></div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function ColonialReparationsEngine() {
  const [data, setData] = useState<ApiData | null>(null);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState<string>("tous");
  const [selected, setSelected] = useState<Entity | null>(null);

  useEffect(() => {
    fetch("/api/colonial-reparations-engine")
      .then(r => r.json())
      .then(d => { setData(d); setLoading(false); })
      .catch(() => setLoading(false));
  }, []);

  const entities: Entity[] = data?.entities ?? [];
  const filtered = filter === "tous" ? entities : entities.filter(e => e.risk_level === filter);

  return (
    <div className="min-h-screen bg-slate-950 text-white p-6">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-amber-400">Colonial Reparations Engine</h1>
          <p className="text-slate-400 mt-1">Analyse des dettes coloniales et indicateurs de réparations</p>
        </div>

        {loading && (
          <div className="flex items-center justify-center h-64">
            <div className="text-amber-400 text-lg">Chargement...</div>
          </div>
        )}

        {!loading && data && (
          <>
            {/* KPI Cards 3x2 */}
            <div className="grid grid-cols-3 gap-4 mb-8">
              <div className="bg-slate-900 border border-amber-500/30 rounded-xl p-5">
                <p className="text-slate-400 text-xs uppercase tracking-wider mb-2">Total entités</p>
                <div className="flex items-center gap-3">
                  <GaugeRing value={Math.min(data.total_entities, 100)} max={100} color="text-amber-400" />
                  <p className="text-3xl font-bold text-white">{data.total_entities}</p>
                </div>
              </div>
              <div className="bg-slate-900 border border-amber-500/30 rounded-xl p-5">
                <p className="text-slate-400 text-xs uppercase tracking-wider mb-2">Score composite moyen</p>
                <div className="flex items-center gap-3">
                  <GaugeRing value={data.avg_composite} max={100} color="text-amber-400" />
                  <p className="text-3xl font-bold text-white">{data.avg_composite?.toFixed(1)}</p>
                </div>
              </div>
              <div className="bg-slate-900 border border-amber-500/30 rounded-xl p-5">
                <p className="text-slate-400 text-xs uppercase tracking-wider mb-2">Score de confiance</p>
                <div className="flex items-center gap-3">
                  <GaugeRing value={data.confidence_score} max={100} color="text-amber-400" />
                  <p className="text-3xl font-bold text-white">{data.confidence_score?.toFixed(1)}</p>
                </div>
              </div>
              <div className="bg-slate-900 border border-red-500/30 rounded-xl p-5">
                <p className="text-slate-400 text-xs uppercase tracking-wider mb-2">Risque critique</p>
                <div className="flex items-center gap-3">
                  <GaugeRing value={data.risk_distribution?.critique ?? 0} max={Math.max(data.total_entities, 1)} color="text-red-400" />
                  <p className="text-3xl font-bold text-red-400">{data.risk_distribution?.critique ?? 0}</p>
                </div>
              </div>
              <div className="bg-slate-900 border border-amber-500/30 rounded-xl p-5">
                <p className="text-slate-400 text-xs uppercase tracking-wider mb-2">Entité à risque max</p>
                <p className="text-lg font-bold text-amber-400 truncate">{data.top_risk_entities?.[0]?.name ?? "—"}</p>
                <p className="text-slate-400 text-xs truncate">{data.top_risk_entities?.[0]?.country ?? ""}</p>
              </div>
              <div className="bg-slate-900 border border-amber-500/30 rounded-xl p-5">
                <p className="text-slate-400 text-xs uppercase tracking-wider mb-2">Indice réparations moy.</p>
                <div className="flex items-center gap-3">
                  <GaugeRing value={data.avg_estimated_colonial_reparations_index} max={100} color="text-amber-400" />
                  <p className="text-3xl font-bold text-white">{data.avg_estimated_colonial_reparations_index?.toFixed(1)}</p>
                </div>
              </div>
            </div>

            {/* Filter pills */}
            <div className="flex gap-2 mb-6 flex-wrap">
              {["tous","critique","élevé","modéré","faible"].map(f => (
                <button key={f} onClick={() => setFilter(f)}
                  className={`px-4 py-1.5 rounded-full text-sm font-medium border transition-colors ${filter === f ? "bg-amber-500/20 border-amber-500/50 text-amber-400" : "border-slate-700 text-slate-400 hover:text-white hover:border-slate-500"}`}>
                  {f}
                </button>
              ))}
            </div>

            {/* Entity grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {filtered.map(entity => (
                <div key={entity.id}
                  className={`bg-slate-900 border rounded-xl p-5 cursor-pointer hover:border-amber-500/50 transition-colors ${RB[entity.risk_level] ?? "border-slate-700"}`}
                  onClick={() => setSelected(entity)}>
                  <div className="flex items-start justify-between mb-3">
                    <div>
                      <p className="font-semibold text-white truncate">{entity.name}</p>
                      <p className="text-slate-400 text-xs">{entity.country}</p>
                    </div>
                    <span className={`text-xs font-semibold px-2 py-0.5 rounded-full border ${RB[entity.risk_level] ?? ""} ${RC[entity.risk_level] ?? ""}`}>
                      {entity.risk_level}
                    </span>
                  </div>
                  <div className="flex items-center gap-3">
                    <GaugeRing value={entity.composite_score ?? 0} max={100} color="text-amber-400" />
                    <div>
                      <p className="text-xs text-slate-400">Score composite</p>
                      <p className="text-lg font-bold text-white">{entity.composite_score?.toFixed(1)}</p>
                      <p className="text-xs text-slate-500 truncate">{entity.primary_pattern}</p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </>
        )}
      </div>

      {selected && <DetailModal entity={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
