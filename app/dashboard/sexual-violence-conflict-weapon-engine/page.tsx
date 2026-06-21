"use client"
import { useState, useEffect } from "react"

const ACCENT = "#dc2626"

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
  estimated_conflict_sexual_violence_index: number
}

type DomainData = {
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

export default function SexualViolenceConflictWeaponDashboard() {
  const [data, setData] = useState<DomainData | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch("/api/sexual-violence-conflict-weapon-engine")
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
        <div className="text-red-400 text-lg">Erreur de chargement des données</div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center gap-3 mb-2">
            <div className="w-3 h-3 rounded-full" style={{ backgroundColor: ACCENT }} />
            <span className="text-sm font-medium uppercase tracking-widest" style={{ color: ACCENT }}>
              Wave 170 — Violence Sexuelle Conflit
            </span>
          </div>
          <h1 className="text-3xl font-bold text-white mb-1">
            Violence Sexuelle comme Arme de Conflit
          </h1>
          <p className="text-slate-400 text-sm">
            Monitoring &amp; évaluation de la violence sexuelle utilisée comme arme de guerre à l&apos;échelle mondiale
          </p>
        </div>

        {/* Stats Bar */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
          <div className="bg-slate-900 rounded-xl p-4 border border-slate-800">
            <div className="text-2xl font-bold" style={{ color: ACCENT }}>{data.avg_composite.toFixed(2)}</div>
            <div className="text-xs text-slate-400 mt-1">Score Moyen Composite</div>
          </div>
          <div className="bg-slate-900 rounded-xl p-4 border border-slate-800">
            <div className="text-2xl font-bold text-red-400">{data.risk_distribution.critique}</div>
            <div className="text-xs text-slate-400 mt-1">Niveau Critique</div>
          </div>
          <div className="bg-slate-900 rounded-xl p-4 border border-slate-800">
            <div className="text-2xl font-bold text-orange-400">{data.risk_distribution.élevé}</div>
            <div className="text-xs text-slate-400 mt-1">Niveau Élevé</div>
          </div>
          <div className="bg-slate-900 rounded-xl p-4 border border-slate-800">
            <div className="text-2xl font-bold text-slate-300">{data.entities.length}</div>
            <div className="text-xs text-slate-400 mt-1">Entités Analysées</div>
          </div>
        </div>

        {/* Entities Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-4">
          {data.entities.map((entity) => {
            const riskColor = RISK_COLORS[entity.risk_level] ?? ACCENT
            return (
              <div
                key={entity.entity_id}
                className="bg-slate-900 rounded-xl p-4 border border-slate-800 flex flex-col gap-3"
              >
                <div className="flex items-center justify-between">
                  <span className="text-xs font-mono text-slate-500">{entity.entity_id}</span>
                  <span
                    className="text-xs font-semibold px-2 py-0.5 rounded-full"
                    style={{ backgroundColor: `${riskColor}22`, color: riskColor }}
                  >
                    {entity.risk_level}
                  </span>
                </div>

                <div className="w-20 h-20 mx-auto relative">
                  <GaugeRing value={entity.composite_score} color={riskColor} />
                  <div className="absolute inset-0 flex items-center justify-center">
                    <span className="text-sm font-bold text-white">{entity.composite_score}</span>
                  </div>
                </div>

                <p className="text-xs text-slate-300 text-center leading-relaxed line-clamp-3">
                  {entity.name}
                </p>

                <div className="mt-auto pt-2 border-t border-slate-800 flex justify-between items-center">
                  <span className="text-xs text-slate-500">Index Violence Sexuelle</span>
                  <span className="text-sm font-bold" style={{ color: ACCENT }}>
                    {entity.estimated_conflict_sexual_violence_index.toFixed(2)}
                  </span>
                </div>
              </div>
            )
          })}
        </div>

        {/* Footer */}
        <div className="mt-8 text-center text-xs text-slate-600">
          Données générées le {new Date(data.generated_at).toLocaleString("fr-FR")} — Caelum Partners Intelligence
        </div>
      </div>
    </div>
  )
}
