"use client"
import { useState, useEffect } from "react"

const ACCENT = "#10b981"

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

type Entity = {
  entity_id: string
  name: string
  composite_score: number
  risk_level: string
  estimated_environmental_defenders_index: number
}

type DomainData = {
  domain: string
  generated_at: string
  entities: Entity[]
  avg_composite: number
  risk_distribution: Record<string, number>
}

const RISK_COLORS: Record<string, string> = {
  critique: "#ef4444",
  "élevé": "#f97316",
  modéré: "#eab308",
  faible: "#22c55e",
}

export default function EnvironmentalDefendersKillingsDashboard() {
  const [data, setData] = useState<DomainData | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch("/api/environmental-defenders-killings-engine")
      .then(r => r.json())
      .then(d => { setData(d.payload ?? d); setLoading(false) })
  }, [])

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center">
        <div className="text-slate-400 text-lg">Chargement...</div>
      </div>
    )
  }

  if (!data) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center">
        <div className="text-red-400 text-lg">Erreur de chargement des données.</div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold mb-2" style={{ color: ACCENT }}>
            Meurtres de Défenseurs Environnementaux
          </h1>
          <p className="text-slate-400 text-sm">
            Domaine : {data.domain} — Généré le {new Date(data.generated_at).toLocaleString("fr-FR")}
          </p>
        </div>

        {/* Score global */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-slate-900 rounded-xl p-6 flex flex-col items-center">
            <div className="w-28 h-28 mb-4">
              <GaugeRing value={data.avg_composite} color={ACCENT} />
            </div>
            <div className="text-2xl font-bold" style={{ color: ACCENT }}>{data.avg_composite.toFixed(2)}</div>
            <div className="text-slate-400 text-sm mt-1">Score composite moyen</div>
          </div>

          <div className="bg-slate-900 rounded-xl p-6">
            <h2 className="text-slate-300 font-semibold mb-4">Distribution des risques</h2>
            <div className="space-y-2">
              {Object.entries(data.risk_distribution).map(([level, count]) => (
                <div key={level} className="flex items-center justify-between">
                  <span className="text-sm" style={{ color: RISK_COLORS[level] ?? "#94a3b8" }}>
                    {level.charAt(0).toUpperCase() + level.slice(1)}
                  </span>
                  <span className="text-slate-300 font-mono">{count}</span>
                </div>
              ))}
            </div>
          </div>

          <div className="bg-slate-900 rounded-xl p-6">
            <h2 className="text-slate-300 font-semibold mb-4">À propos</h2>
            <p className="text-slate-400 text-sm leading-relaxed">
              Ce tableau de bord analyse les meurtres et persécutions de défenseurs de l&apos;environnement à travers le monde,
              mesurant l&apos;impunité, les menaces structurelles et les protections légales existantes.
            </p>
          </div>
        </div>

        {/* Entités */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {data.entities.map((entity) => (
            <div key={entity.entity_id} className="bg-slate-900 rounded-xl p-5 border border-slate-800">
              <div className="flex items-start justify-between gap-4 mb-3">
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-1">
                    <span className="text-xs font-mono text-slate-500">{entity.entity_id}</span>
                    <span
                      className="text-xs px-2 py-0.5 rounded-full font-medium"
                      style={{ backgroundColor: (RISK_COLORS[entity.risk_level] ?? "#94a3b8") + "22", color: RISK_COLORS[entity.risk_level] ?? "#94a3b8" }}
                    >
                      {entity.risk_level}
                    </span>
                  </div>
                  <p className="text-slate-200 text-sm leading-snug">{entity.name}</p>
                </div>
                <div className="w-16 h-16 shrink-0">
                  <GaugeRing value={entity.composite_score} color={RISK_COLORS[entity.risk_level] ?? ACCENT} />
                </div>
              </div>
              <div className="flex items-center justify-between text-xs text-slate-500">
                <span>Score : <span className="text-slate-300 font-mono">{entity.composite_score.toFixed(2)}</span></span>
                <span>Index défenseurs : <span className="font-mono" style={{ color: ACCENT }}>{entity.estimated_environmental_defenders_index.toFixed(2)}</span></span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
