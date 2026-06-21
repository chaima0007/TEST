"use client"
import { useState, useEffect } from "react"

const RC: Record<string, string> = { critique: "text-red-400", "élevé": "text-orange-400", modéré: "text-yellow-400", faible: "text-emerald-400" }
const RB: Record<string, string> = { critique: "border-red-500/30 bg-red-500/10", "élevé": "border-orange-500/30 bg-orange-500/10", modéré: "border-yellow-500/30 bg-yellow-500/10", faible: "border-emerald-500/30 bg-emerald-500/10" }

function GaugeRing({ score, color }: { score: number; color: string }) {
  const r = 36, circ = 2 * Math.PI * r
  const offset = circ - (score / 100) * circ
  return (
    <svg viewBox="0 0 88 88" className="w-20 h-20">
      <circle cx="44" cy="44" r={r} fill="none" stroke="#1e293b" strokeWidth="8" />
      <circle cx="44" cy="44" r={r} fill="none" stroke={color} strokeWidth="8"
        strokeDasharray={circ} strokeDashoffset={offset}
        strokeLinecap="round" transform="rotate(-90 44 44)" />
      <text x="44" y="49" textAnchor="middle" fontSize="14" fontWeight="700" fill={color}>{score.toFixed(0)}</text>
    </svg>
  )
}

interface Entity { entity_id: string; name: string; composite_score: number; risk_level: string; estimated_labor_rights_index?: number; [key: string]: unknown }
interface DashData { domain?: string; avg_composite?: number; risk_distribution?: Record<string, number>; entities?: Entity[]; [key: string]: unknown }

export default function LaborUnionCollectiveBargainingDashboard() {
  const [data, setData] = useState<DashData>({})
  const [filter, setFilter] = useState("tous")
  const [selected, setSelected] = useState<Entity | null>(null)
  const [tab, setTab] = useState(0)
  const [loading, setLoading] = useState(true)
  const ACCENT = "#f59e0b"

  useEffect(() => {
    fetch("/api/labor-union-collective-bargaining-engine")
      .then(r => r.json())
      .then(d => { setData(d.payload ?? d); setLoading(false) })
      .catch(() => setLoading(false))
  }, [])

  const entities: Entity[] = data.entities ?? []
  const filtered = filter === "tous" ? entities : entities.filter(e => e.risk_level === filter)

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
      <div className="mb-8">
        <h1 className="text-3xl font-bold" style={{ color: ACCENT }}>Droits Syndicaux &amp; Négociation Collective</h1>
        <p className="text-slate-400 mt-1">Labor Union Collective Bargaining Engine — Analyse des violations des droits syndicaux et de la négociation collective</p>
      </div>
      <div className="grid grid-cols-2 md:grid-cols-3 gap-4 mb-8">
        <div className="bg-slate-900 rounded-xl p-4 border border-slate-800">
          <p className="text-slate-400 text-sm">Entités Analysées</p>
          <p className="text-2xl font-bold mt-1" style={{ color: ACCENT }}>{loading ? "…" : (data.entities?.length ?? 0)}</p>
          <p className="text-slate-500 text-xs mt-1">acteurs</p>
        </div>
        <div className="bg-slate-900 rounded-xl p-4 border border-slate-800">
          <p className="text-slate-400 text-sm">Score Moyen</p>
          <p className="text-2xl font-bold mt-1" style={{ color: ACCENT }}>{loading ? "…" : data.avg_composite?.toFixed(1)}</p>
          <p className="text-slate-500 text-xs mt-1">/100</p>
        </div>
        <div className="bg-slate-900 rounded-xl p-4 border border-slate-800">
          <p className="text-slate-400 text-sm">Alertes Critiques</p>
          <p className="text-2xl font-bold mt-1 text-red-400">{loading ? "…" : data.risk_distribution?.critique}</p>
          <p className="text-slate-500 text-xs mt-1">entités</p>
        </div>
        <div className="bg-slate-900 rounded-xl p-4 border border-slate-800">
          <p className="text-slate-400 text-sm">Niveau Élevé</p>
          <p className="text-2xl font-bold mt-1 text-orange-400">{loading ? "…" : data.risk_distribution?.["élevé"]}</p>
          <p className="text-slate-500 text-xs mt-1">entités</p>
        </div>
        <div className="bg-slate-900 rounded-xl p-4 border border-slate-800">
          <p className="text-slate-400 text-sm">Niveau Modéré</p>
          <p className="text-2xl font-bold mt-1 text-yellow-400">{loading ? "…" : data.risk_distribution?.modéré}</p>
          <p className="text-slate-500 text-xs mt-1">entités</p>
        </div>
        <div className="bg-slate-900 rounded-xl p-4 border border-slate-800">
          <p className="text-slate-400 text-sm">Niveau Faible</p>
          <p className="text-2xl font-bold mt-1 text-emerald-400">{loading ? "…" : data.risk_distribution?.faible}</p>
          <p className="text-slate-500 text-xs mt-1">entités</p>
        </div>
      </div>
      <div className="flex gap-2 mb-6 flex-wrap">
        {["tous", "critique", "élevé", "modéré", "faible"].map(f => (
          <button key={f} onClick={() => setFilter(f)}
            className={`px-4 py-1.5 rounded-full text-sm font-medium transition-colors ${filter === f ? "text-white" : "bg-slate-800 text-slate-400 hover:bg-slate-700"}`}
            style={filter === f ? { backgroundColor: ACCENT } : {}}>
            {f.charAt(0).toUpperCase() + f.slice(1)}
          </button>
        ))}
      </div>
      <div className="grid gap-4 md:grid-cols-2">
        {filtered.map(e => (
          <div key={e.entity_id} onClick={() => { setSelected(e); setTab(0) }}
            className={`cursor-pointer rounded-xl border p-4 transition-all hover:scale-[1.01] ${RB[e.risk_level] ?? "border-slate-700 bg-slate-900"}`}>
            <div className="flex items-start gap-4">
              <GaugeRing score={e.composite_score} color={ACCENT} />
              <div className="flex-1 min-w-0">
                <p className="text-xs text-slate-400 mb-1">{e.entity_id}</p>
                <p className="font-semibold text-sm leading-snug line-clamp-2">{e.name}</p>
                <div className="flex items-center gap-2 mt-2">
                  <span className={`text-xs font-bold uppercase ${RC[e.risk_level]}`}>{e.risk_level}</span>
                  <span className="text-slate-600">·</span>
                  <span className="text-xs text-slate-400">index: {e.estimated_labor_rights_index?.toFixed(2)}/10</span>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
      {selected && (
        <div className="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center z-50 p-4" onClick={() => setSelected(null)}>
          <div className="bg-slate-900 rounded-2xl border border-slate-700 max-w-2xl w-full max-h-[85vh] overflow-y-auto" onClick={e => e.stopPropagation()}>
            <div className="p-6 border-b border-slate-800">
              <div className="flex items-start justify-between gap-4">
                <div>
                  <p className="text-xs text-slate-400 mb-1">{selected.entity_id}</p>
                  <h2 className="text-lg font-bold leading-snug">{selected.name}</h2>
                </div>
                <button onClick={() => setSelected(null)} className="text-slate-400 hover:text-white text-xl flex-shrink-0">✕</button>
              </div>
              <div className="flex items-center gap-3 mt-3">
                <span className={`text-sm font-bold uppercase ${RC[selected.risk_level]}`}>{selected.risk_level}</span>
                <GaugeRing score={selected.composite_score} color={ACCENT} />
              </div>
            </div>
            <div className="flex border-b border-slate-800">
              {["Aperçu", "Scores", "Contexte"].map((t, i) => (
                <button key={t} onClick={() => setTab(i)}
                  className={`px-6 py-3 text-sm font-medium transition-colors ${tab === i ? "border-b-2 text-white" : "text-slate-400 hover:text-white"}`}
                  style={tab === i ? { borderColor: ACCENT, color: ACCENT } : {}}>{t}</button>
              ))}
            </div>
            <div className="p-6">
              {tab === 0 && (
                <div className="space-y-3">
                  <div className="flex justify-between text-sm"><span className="text-slate-400">Score composite</span><span className="font-bold">{selected.composite_score}/100</span></div>
                  <div className="flex justify-between text-sm"><span className="text-slate-400">Niveau de risque</span><span className={`font-bold uppercase ${RC[selected.risk_level]}`}>{selected.risk_level}</span></div>
                  <div className="flex justify-between text-sm"><span className="text-slate-400">Indice droits syndicaux</span><span className="font-bold">{selected.estimated_labor_rights_index?.toFixed(2)}/10</span></div>
                </div>
              )}
              {tab === 1 && (
                <div className="space-y-3">
                  <div className="flex justify-between text-sm"><span className="text-slate-400">Score composite</span><span className="font-bold">{selected.composite_score}</span></div>
                  <div className="flex justify-between text-sm"><span className="text-slate-400">Index estimé</span><span className="font-bold">{selected.estimated_labor_rights_index?.toFixed(2)}</span></div>
                </div>
              )}
              {tab === 2 && (
                <div className="space-y-3 text-sm">
                  <div className="flex justify-between"><span className="text-slate-400">ID Entité</span><span className="font-mono">{selected.entity_id}</span></div>
                  <div className="flex justify-between"><span className="text-slate-400">Entité</span><span>{selected.name}</span></div>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
