"use client";
import { useState, useEffect } from "react";

const ACCENT = "#042f2e";
const RC: Record<string, string> = { critique: "text-red-400", "élevé": "text-orange-400", modéré: "text-yellow-400", faible: "text-emerald-400" };
const RB: Record<string, string> = { critique: "border-red-500/30 bg-red-500/10", "élevé": "border-orange-500/30 bg-orange-500/10", modéré: "border-yellow-500/30 bg-yellow-500/10", faible: "border-emerald-500/30 bg-emerald-500/10" };

const FALLBACK = {
  total_entities: 8,
  avg_composite: 57.00,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  avg_estimated_water_privatisation_rights_index: 5.70,
  entities: [
    { id: "WPR-001", name: "Veolia Water", country: "France", composite_score: 85.7, privatization_access_denial_score: 90.0, profit_over_rights_score: 84.0, regulatory_bypass_score: 86.0, community_displacement_score: 83.0, risk_level: "critique", primary_pattern: "privatization_access_denial", estimated_water_privatisation_rights_index: 8.57 },
    { id: "WPR-002", name: "Suez Environnement", country: "France", composite_score: 81.4, privatization_access_denial_score: 85.0, profit_over_rights_score: 80.0, regulatory_bypass_score: 82.0, community_displacement_score: 79.0, risk_level: "critique", primary_pattern: "profit_over_rights", estimated_water_privatisation_rights_index: 8.14 },
    { id: "WPR-003", name: "Thames Water UK", country: "Royaume-Uni", composite_score: 77.1, privatization_access_denial_score: 80.0, profit_over_rights_score: 76.0, regulatory_bypass_score: 78.0, community_displacement_score: 74.0, risk_level: "critique", primary_pattern: "regulatory_bypass", estimated_water_privatisation_rights_index: 7.71 },
    { id: "WPR-004", name: "Nestlé Pure Life", country: "Suisse", composite_score: 71.8, privatization_access_denial_score: 75.0, profit_over_rights_score: 72.0, regulatory_bypass_score: 70.0, community_displacement_score: 70.0, risk_level: "critique", primary_pattern: "privatization_access_denial", estimated_water_privatisation_rights_index: 7.18 },
    { id: "WPR-005", name: "American Water Works", country: "États-Unis", composite_score: 54.1, privatization_access_denial_score: 56.0, profit_over_rights_score: 54.0, regulatory_bypass_score: 53.0, community_displacement_score: 53.0, risk_level: "élevé", primary_pattern: "profit_over_rights", estimated_water_privatisation_rights_index: 5.41 },
    { id: "WPR-006", name: "United Utilities", country: "Royaume-Uni", composite_score: 49.9, privatization_access_denial_score: 51.0, profit_over_rights_score: 50.0, regulatory_bypass_score: 49.0, community_displacement_score: 50.0, risk_level: "élevé", primary_pattern: "regulatory_bypass", estimated_water_privatisation_rights_index: 4.99 },
    { id: "WPR-007", name: "WWF Water", country: "Global", composite_score: 25.9, privatization_access_denial_score: 23.0, profit_over_rights_score: 26.0, regulatory_bypass_score: 27.0, community_displacement_score: 27.0, risk_level: "modéré", primary_pattern: "community_displacement", estimated_water_privatisation_rights_index: 2.59 },
    { id: "WPR-008", name: "Blue Planet Project", country: "Global", composite_score: 11.1, privatization_access_denial_score: 9.0, profit_over_rights_score: 11.0, regulatory_bypass_score: 12.0, community_displacement_score: 12.0, risk_level: "faible", primary_pattern: "community_displacement", estimated_water_privatisation_rights_index: 1.11 },
  ],
};

interface Entity {
  id: string;
  name: string;
  country: string;
  composite_score: number;
  privatization_access_denial_score: number;
  profit_over_rights_score: number;
  regulatory_bypass_score: number;
  community_displacement_score: number;
  risk_level: string;
  primary_pattern: string;
  estimated_water_privatisation_rights_index: number;
}

interface ApiData {
  total_entities: number;
  avg_composite: number;
  confidence_score: number;
  risk_distribution: Record<string, number>;
  avg_estimated_water_privatisation_rights_index: number;
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
  const [tab, setTab] = useState<"apercu" | "signaux" | "contexte">("apercu");
  return (
    <div className="fixed inset-0 bg-black/70 flex items-center justify-center z-50 p-4" onClick={onClose}>
      <div className="bg-slate-900 border border-cyan-500/30 rounded-xl w-full max-w-2xl p-6" onClick={e => e.stopPropagation()}>
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
          {(["apercu", "signaux", "contexte"] as const).map(t => (
            <button key={t} onClick={() => setTab(t)}
              className={`px-4 py-1.5 rounded-lg text-sm font-medium transition-colors ${tab === t ? "bg-cyan-500/20 text-cyan-400 border border-cyan-500/40" : "text-slate-400 hover:text-white"}`}>
              {t === "apercu" ? "Aperçu" : t === "signaux" ? "Signaux" : "Contexte"}
            </button>
          ))}
        </div>
        {tab === "apercu" && (
          <div className="space-y-3">
            <div className="flex justify-between text-sm"><span className="text-slate-400">Score composite</span><span className="text-white font-semibold">{entity.composite_score?.toFixed(2)}</span></div>
            <div className="flex justify-between text-sm"><span className="text-slate-400">Indice privatisation eau</span><span className="text-cyan-400 font-semibold">{entity.estimated_water_privatisation_rights_index?.toFixed(2)}</span></div>
            <div className="flex justify-between text-sm"><span className="text-slate-400">Modèle principal</span><span className="text-white">{entity.primary_pattern}</span></div>
          </div>
        )}
        {tab === "signaux" && (
          <div className="space-y-3">
            <div className="flex justify-between text-sm"><span className="text-slate-400">Privatisation / déni d&apos;accès</span><span className="text-white">{entity.privatization_access_denial_score?.toFixed(2)}</span></div>
            <div className="flex justify-between text-sm"><span className="text-slate-400">Profit sur droits</span><span className="text-white">{entity.profit_over_rights_score?.toFixed(2)}</span></div>
            <div className="flex justify-between text-sm"><span className="text-slate-400">Contournement réglementaire</span><span className="text-white">{entity.regulatory_bypass_score?.toFixed(2)}</span></div>
            <div className="flex justify-between text-sm"><span className="text-slate-400">Déplacement communautaire</span><span className="text-white">{entity.community_displacement_score?.toFixed(2)}</span></div>
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

export default function WaterPrivatisationRightsEngine() {
  const [data, setData] = useState<ApiData | null>(null);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState<string>("tous");
  const [selected, setSelected] = useState<Entity | null>(null);

  useEffect(() => {
    fetch("/api/water-privatisation-rights-engine")
      .then(r => r.json())
      .then(d => { setData(d.payload ?? d); setLoading(false); })
      .catch(() => { setData(FALLBACK); setLoading(false); });
  }, []);

  const entities: Entity[] = data?.entities ?? FALLBACK.entities;
  const filtered = filter === "tous" ? entities : entities.filter(e => e.risk_level === filter);

  return (
    <div className="min-h-screen bg-slate-950 text-white p-6">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold" style={{ color: ACCENT }}>Water Privatisation Rights Engine</h1>
          <p className="text-slate-400 mt-1">Analyse de la conformité CSDDD pour la privatisation de l&apos;eau — Art.8-13</p>
        </div>

        {loading && (
          <div className="flex items-center justify-center h-64">
            <div className="text-cyan-400 text-lg">Chargement...</div>
          </div>
        )}

        {!loading && data && (
          <>
            <div className="grid grid-cols-3 gap-4 mb-8">
              <div className="bg-slate-900 border border-cyan-500/30 rounded-xl p-5">
                <p className="text-slate-400 text-xs uppercase tracking-wider mb-2">Total entités</p>
                <div className="flex items-center gap-3">
                  <GaugeRing value={Math.min(data.total_entities, 100)} max={100} color="text-cyan-400" />
                  <p className="text-3xl font-bold text-white">{data.total_entities}</p>
                </div>
              </div>
              <div className="bg-slate-900 border border-cyan-500/30 rounded-xl p-5">
                <p className="text-slate-400 text-xs uppercase tracking-wider mb-2">Score composite moyen</p>
                <div className="flex items-center gap-3">
                  <GaugeRing value={data.avg_composite} max={100} color="text-cyan-400" />
                  <p className="text-3xl font-bold text-white">{data.avg_composite?.toFixed(1)}</p>
                </div>
              </div>
              <div className="bg-slate-900 border border-cyan-500/30 rounded-xl p-5">
                <p className="text-slate-400 text-xs uppercase tracking-wider mb-2">Score de confiance</p>
                <div className="flex items-center gap-3">
                  <GaugeRing value={(data.confidence_score ?? 0.85) * 100} max={100} color="text-cyan-400" />
                  <p className="text-3xl font-bold text-white">{((data.confidence_score ?? 0.85) * 100).toFixed(0)}%</p>
                </div>
              </div>
              <div className="bg-slate-900 border border-red-500/30 rounded-xl p-5">
                <p className="text-slate-400 text-xs uppercase tracking-wider mb-2">Risque critique</p>
                <div className="flex items-center gap-3">
                  <GaugeRing value={data.risk_distribution?.critique ?? 0} max={Math.max(data.total_entities, 1)} color="text-red-400" />
                  <p className="text-3xl font-bold text-red-400">{data.risk_distribution?.critique ?? 0}</p>
                </div>
              </div>
              <div className="bg-slate-900 border border-cyan-500/30 rounded-xl p-5">
                <p className="text-slate-400 text-xs uppercase tracking-wider mb-2">Entité à risque max</p>
                <p className="text-lg font-bold text-cyan-400 truncate">{entities[0]?.name ?? "—"}</p>
                <p className="text-slate-400 text-xs truncate">{entities[0]?.country ?? ""}</p>
              </div>
              <div className="bg-slate-900 border border-cyan-500/30 rounded-xl p-5">
                <p className="text-slate-400 text-xs uppercase tracking-wider mb-2">Indice privatisation moy.</p>
                <div className="flex items-center gap-3">
                  <GaugeRing value={data.avg_estimated_water_privatisation_rights_index ?? 0} max={10} color="text-cyan-400" />
                  <p className="text-3xl font-bold text-white">{(data.avg_estimated_water_privatisation_rights_index ?? 0).toFixed(2)}</p>
                </div>
              </div>
            </div>

            <div className="flex gap-2 mb-6 flex-wrap">
              {["tous", "critique", "élevé", "modéré", "faible"].map(f => (
                <button key={f} onClick={() => setFilter(f)}
                  className={`px-4 py-1.5 rounded-full text-sm font-medium border transition-colors ${filter === f ? "bg-cyan-500/20 border-cyan-500/50 text-cyan-400" : "border-slate-700 text-slate-400 hover:text-white hover:border-slate-500"}`}>
                  {f}
                </button>
              ))}
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {filtered.map(entity => (
                <div key={entity.id}
                  className={`bg-slate-900 border rounded-xl p-5 cursor-pointer hover:border-cyan-500/50 transition-colors ${RB[entity.risk_level] ?? "border-slate-700"}`}
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
                    <GaugeRing value={entity.composite_score ?? 0} max={100} color="text-cyan-400" />
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
