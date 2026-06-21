"use client";
import { useState, useEffect } from "react";

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

interface Entity {
  entity_id: string;
  name: string;
  country: string;
  composite_score: number;
  arbitrary_detention_scale_score: number;
  inhumane_conditions_score: number;
  legal_access_denial_score: number;
  pushback_refoulement_score: number;
  risk_level: string;
  primary_pattern: string;
  estimated_refugee_detention_index: number;
}

interface ApiData {
  total_entities: number;
  avg_composite: number;
  confidence_score: number;
  risk_distribution: Record<string, number>;
  top_risk_entities: string[];
  avg_estimated_refugee_detention_index: number;
  entities: Entity[];
}

function GaugeRing({ value, color }: { value: number; color: string }) {
  const r = 36;
  const cx = 44;
  const cy = 44;
  const circumference = 226.19;
  const offset = circumference - (value / 100) * circumference;
  return (
    <svg viewBox="0 0 88 88" className="w-20 h-20">
      <circle cx={cx} cy={cy} r={r} fill="none" stroke="#1e293b" strokeWidth="8" />
      <circle
        cx={cx}
        cy={cy}
        r={r}
        fill="none"
        stroke={color}
        strokeWidth="8"
        strokeDasharray={circumference}
        strokeDashoffset={offset}
        strokeLinecap="round"
        transform={`rotate(-90 ${cx} ${cy})`}
      />
      <text x={cx} y={cy + 5} textAnchor="middle" fill="white" fontSize="14" fontWeight="bold">
        {Math.round(value)}
      </text>
    </svg>
  );
}

function DetailModal({ entity, onClose }: { entity: Entity; onClose: () => void }) {
  const [tab, setTab] = useState<"apercu" | "signaux" | "contexte">("apercu");
  return (
    <div className="fixed inset-0 bg-black/70 flex items-center justify-center z-50 p-4">
      <div className="bg-slate-900 border border-slate-700 rounded-xl w-full max-w-lg">
        <div className="flex items-center justify-between p-5 border-b border-slate-700">
          <div>
            <h2 className="text-white font-bold text-lg">{entity.name}</h2>
            <p className="text-slate-400 text-sm">{entity.country}</p>
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-white text-xl font-bold">×</button>
        </div>
        <div className="flex border-b border-slate-700">
          {(["apercu", "signaux", "contexte"] as const).map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`flex-1 py-2 text-sm font-medium capitalize transition-colors ${tab === t ? "text-orange-400 border-b-2 border-orange-400" : "text-slate-400 hover:text-white"}`}
            >
              {t === "apercu" ? "Aperçu" : t.charAt(0).toUpperCase() + t.slice(1)}
            </button>
          ))}
        </div>
        <div className="p-5">
          {tab === "apercu" && (
            <div className="space-y-3">
              <div className="flex justify-between">
                <span className="text-slate-400 text-sm">Score composite</span>
                <span className="text-white font-semibold">{entity.composite_score.toFixed(2)}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400 text-sm">Niveau de risque</span>
                <span className={`font-semibold text-sm ${RC[entity.risk_level] || "text-slate-300"}`}>{entity.risk_level}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400 text-sm">Pattern primaire</span>
                <span className="text-white text-sm text-right max-w-xs">{entity.primary_pattern}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400 text-sm">Indice détention réfugiés</span>
                <span className="text-orange-400 font-semibold">{entity.estimated_refugee_detention_index.toFixed(2)}</span>
              </div>
            </div>
          )}
          {tab === "signaux" && (
            <div className="space-y-3">
              <div className="flex justify-between">
                <span className="text-slate-400 text-sm">Détention arbitraire (échelle)</span>
                <span className="text-white font-semibold">{entity.arbitrary_detention_scale_score.toFixed(2)}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400 text-sm">Conditions inhumaines</span>
                <span className="text-white font-semibold">{entity.inhumane_conditions_score.toFixed(2)}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400 text-sm">Déni d&apos;accès légal</span>
                <span className="text-white font-semibold">{entity.legal_access_denial_score.toFixed(2)}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400 text-sm">Refoulement / pushback</span>
                <span className="text-white font-semibold">{entity.pushback_refoulement_score.toFixed(2)}</span>
              </div>
            </div>
          )}
          {tab === "contexte" && (
            <div className="space-y-3">
              <div className="flex justify-between">
                <span className="text-slate-400 text-sm">Entité ID</span>
                <span className="text-slate-300 text-sm font-mono">{entity.entity_id}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400 text-sm">Pays</span>
                <span className="text-white text-sm">{entity.country}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400 text-sm">Indice détention réfugiés estimé</span>
                <span className="text-orange-400 font-semibold">{entity.estimated_refugee_detention_index.toFixed(2)}</span>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default function RefugeeDetentionEnginePage() {
  const [data, setData] = useState<ApiData | null>(null);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState<string>("tous");
  const [selected, setSelected] = useState<Entity | null>(null);

  useEffect(() => {
    fetch("/api/refugee-detention-engine")
      .then((r) => r.json())
      .then((d) => { setData(d); setLoading(false); })
      .catch(() => setLoading(false));
  }, []);

  const entities: Entity[] = data?.entities ?? [];
  const filtered = filter === "tous" ? entities : entities.filter((e) => e.risk_level === filter);

  return (
    <main className="min-h-screen bg-slate-950 text-white p-6">
      <div className="max-w-7xl mx-auto space-y-6">
        {/* Header */}
        <div className="flex items-center gap-3">
          <div className="w-2 h-8 bg-orange-500 rounded-full" />
          <h1 className="text-2xl font-bold text-white">Refugee Detention Engine</h1>
          <span className="ml-auto text-slate-500 text-sm">Wave 57</span>
        </div>

        {loading && (
          <div className="flex items-center justify-center h-48 text-slate-400">Chargement…</div>
        )}

        {!loading && data && (
          <>
            {/* KPI Cards 3×2 */}
            <div className="grid grid-cols-3 gap-4">
              <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
                <p className="text-slate-400 text-xs uppercase tracking-wider mb-1">Entités totales</p>
                <p className="text-3xl font-bold text-white">{data.total_entities}</p>
              </div>
              <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
                <p className="text-slate-400 text-xs uppercase tracking-wider mb-1">Score composite moyen</p>
                <p className="text-3xl font-bold text-orange-400">{data.avg_composite.toFixed(2)}</p>
              </div>
              <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
                <p className="text-slate-400 text-xs uppercase tracking-wider mb-1">Score de confiance</p>
                <div className="flex items-center gap-3 mt-1">
                  <GaugeRing value={data.confidence_score * 100} color="#fb923c" />
                  <span className="text-2xl font-bold text-orange-400">{(data.confidence_score * 100).toFixed(0)}%</span>
                </div>
              </div>
              <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
                <p className="text-slate-400 text-xs uppercase tracking-wider mb-1">Risque critique</p>
                <p className="text-3xl font-bold text-red-400">{data.risk_distribution?.critique ?? 0}</p>
              </div>
              <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
                <p className="text-slate-400 text-xs uppercase tracking-wider mb-1">Entité top risque</p>
                <p className="text-lg font-semibold text-white truncate">{data.top_risk_entities?.[0] ?? "—"}</p>
              </div>
              <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
                <p className="text-slate-400 text-xs uppercase tracking-wider mb-1">Indice détention réfugiés moy.</p>
                <p className="text-3xl font-bold text-orange-400">{data.avg_estimated_refugee_detention_index.toFixed(2)}</p>
              </div>
            </div>

            {/* Filter pills */}
            <div className="flex flex-wrap gap-2">
              {["tous", "critique", "élevé", "modéré", "faible"].map((f) => (
                <button
                  key={f}
                  onClick={() => setFilter(f)}
                  className={`px-4 py-1.5 rounded-full text-sm font-medium border transition-colors ${
                    filter === f
                      ? "bg-orange-500/20 border-orange-500/50 text-orange-300"
                      : "bg-slate-800 border-slate-700 text-slate-400 hover:text-white"
                  }`}
                >
                  {f.charAt(0).toUpperCase() + f.slice(1)}
                </button>
              ))}
              <span className="ml-auto text-slate-500 text-sm self-center">{filtered.length} entité{filtered.length !== 1 ? "s" : ""}</span>
            </div>

            {/* Entities grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
              {filtered.map((entity) => (
                <div
                  key={entity.entity_id}
                  onClick={() => setSelected(entity)}
                  className={`rounded-xl border p-4 cursor-pointer hover:brightness-110 transition-all ${RB[entity.risk_level] || "border-slate-700 bg-slate-800/50"}`}
                >
                  <div className="flex items-start justify-between mb-2">
                    <div className="flex-1 min-w-0">
                      <p className="text-white font-semibold truncate">{entity.name}</p>
                      <p className="text-slate-400 text-sm">{entity.country}</p>
                    </div>
                    <span className={`text-xs font-bold ml-2 shrink-0 ${RC[entity.risk_level] || "text-slate-300"}`}>
                      {entity.risk_level}
                    </span>
                  </div>
                  <div className="flex items-center justify-between mt-3">
                    <span className="text-slate-500 text-xs truncate max-w-[60%]">{entity.primary_pattern}</span>
                    <span className="text-orange-400 font-bold text-sm">{entity.composite_score.toFixed(2)}</span>
                  </div>
                </div>
              ))}
            </div>
          </>
        )}
      </div>

      {selected && <DetailModal entity={selected} onClose={() => setSelected(null)} />}
    </main>
  );
}
