"use client"
import { useState, useEffect } from "react"

const ACCENT = "#16a34a"

function GaugeRing({ value, color }: { value: number; color: string }) {
  const r = 36, cx = 44, cy = 44
  const circ = 2 * Math.PI * r
  const offset = circ - (value / 100) * circ
  return (
    <svg viewBox="0 0 88 88" className="w-full h-full">
      <circle cx={cx} cy={cy} r={r} fill="none" stroke="#1e293b" strokeWidth={8} />
      <circle cx={cx} cy={cy} r={r} fill="none" stroke={color} strokeWidth={8}
        strokeDasharray={circ} strokeDashoffset={offset}
        strokeLinecap="round" transform="rotate(-90 44 44)" />
    </svg>
  )
}

interface Entity {
  id: string
  name: string
  composite_score: number
  risk_level: string
  estimated_land_rights_index: number
}

interface EngineData {
  domain: string
  generated_at: string
  entities: Entity[]
  avg_composite: number
  risk_distribution: { critique: number; élevé: number; modéré: number; faible: number }
}

const RISK_COLORS: Record<string, string> = {
  critique: "#ef4444",
  élevé: "#f97316",
  modéré: "#eab308",
  faible: "#22c55e",
}

export default function LandRightsEvictionIndigenousTerritoriesDashboard() {
  const [data, setData] = useState<EngineData | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetch("/api/land-rights-eviction-indigenous-territories-engine")
      .then((r) => r.json())
      .then((d) => {
        setData(d.payload ?? d)
        setLoading(false)
      })
      .catch(() => {
        setError("Erreur de chargement")
        setLoading(false)
      })
  }, [])

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center">
        <div className="text-slate-400 text-lg">Chargement...</div>
      </div>
    )
  }

  if (error || !data) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center">
        <div className="text-red-400 text-lg">{error ?? "Données indisponibles"}</div>
      </div>
    )
  }

  const composite = data.avg_composite ?? 0
  const avgIndex = data.entities?.length
    ? data.entities.reduce((s, e) => s + e.estimated_land_rights_index, 0) / data.entities.length
    : 0

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
      <div className="max-w-6xl mx-auto space-y-8">
        {/* Header */}
        <div className="border-l-4 pl-6" style={{ borderColor: ACCENT }}>
          <h1 className="text-3xl font-bold text-white">
            Droits Fonciers &amp; Expulsions Territoires Autochtones
          </h1>
          <p className="text-slate-400 mt-2">
            Land Rights · Indigenous Territories · Evictions · FPIC · Agribusiness
          </p>
          <p className="text-slate-500 text-sm mt-1">Domaine : {data.domain}</p>
        </div>

        {/* KPI Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Composite Score */}
          <div className="bg-slate-900 rounded-2xl p-6 flex flex-col items-center">
            <div className="w-32 h-32 mb-4">
              <GaugeRing value={composite} color={ACCENT} />
            </div>
            <div className="text-4xl font-bold text-white">{composite.toFixed(2)}</div>
            <div className="text-slate-400 text-sm mt-1">Score Composite Moyen</div>
          </div>

          {/* Land Rights Index */}
          <div className="bg-slate-900 rounded-2xl p-6 flex flex-col items-center">
            <div className="w-32 h-32 mb-4">
              <GaugeRing value={avgIndex * 10} color="#f97316" />
            </div>
            <div className="text-4xl font-bold text-white">{avgIndex.toFixed(2)}</div>
            <div className="text-slate-400 text-sm mt-1">Indice droits fonciers</div>
          </div>
        </div>

        {/* Risk Distribution */}
        <div className="bg-slate-900 rounded-2xl p-6">
          <h2 className="text-xl font-semibold text-white mb-4">Distribution des Risques</h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="bg-red-950/40 border border-red-800/30 rounded-xl p-4 text-center">
              <div className="text-3xl font-bold text-red-400">{data.risk_distribution.critique}</div>
              <div className="text-red-300/70 text-sm mt-1">Critique</div>
            </div>
            <div className="bg-orange-950/40 border border-orange-800/30 rounded-xl p-4 text-center">
              <div className="text-3xl font-bold text-orange-400">{data.risk_distribution["élevé"]}</div>
              <div className="text-orange-300/70 text-sm mt-1">Élevé</div>
            </div>
            <div className="bg-yellow-950/40 border border-yellow-800/30 rounded-xl p-4 text-center">
              <div className="text-3xl font-bold text-yellow-400">{data.risk_distribution.modéré}</div>
              <div className="text-yellow-300/70 text-sm mt-1">Modéré</div>
            </div>
            <div className="bg-green-950/40 border border-green-800/30 rounded-xl p-4 text-center">
              <div className="text-3xl font-bold text-green-400">{data.risk_distribution.faible}</div>
              <div className="text-green-300/70 text-sm mt-1">Faible</div>
            </div>
          </div>
        </div>

        {/* Entities Table */}
        <div className="bg-slate-900 rounded-2xl p-6">
          <h2 className="text-xl font-semibold text-white mb-4">Entités Analysées</h2>
          <div className="space-y-3">
            {data.entities.map((entity) => (
              <div key={entity.id} className="bg-slate-800/50 rounded-xl p-4 flex items-center justify-between gap-4">
                <div className="flex-1 min-w-0">
                  <div className="text-xs text-slate-500 mb-1">{entity.id}</div>
                  <div className="text-sm text-slate-200 leading-snug">{entity.name}</div>
                </div>
                <div className="flex items-center gap-4 shrink-0">
                  <div className="text-right">
                    <div className="text-lg font-bold text-white">{entity.composite_score.toFixed(1)}</div>
                    <div className="text-xs text-slate-500">score</div>
                  </div>
                  <div className="text-right">
                    <div className="text-lg font-bold" style={{ color: RISK_COLORS[entity.risk_level] ?? "#94a3b8" }}>
                      {entity.estimated_land_rights_index.toFixed(2)}
                    </div>
                    <div className="text-xs text-slate-500">indice</div>
                  </div>
                  <span
                    className="px-2 py-1 rounded-full text-xs font-semibold"
                    style={{
                      backgroundColor: (RISK_COLORS[entity.risk_level] ?? "#94a3b8") + "22",
                      color: RISK_COLORS[entity.risk_level] ?? "#94a3b8",
                    }}
                  >
                    {entity.risk_level}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Meta */}
        <div className="text-slate-600 text-xs text-right">
          Généré le : {data.generated_at ? new Date(data.generated_at).toLocaleString("fr-FR") : "—"} · Entités : {data.entities?.length ?? 0}
        </div>
      </div>
    </div>
  )
}
