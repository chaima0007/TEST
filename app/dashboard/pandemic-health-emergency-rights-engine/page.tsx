"use client"
import { useEffect, useState } from "react"

function GaugeRing({ value, color }: { value: number; color: string }) {
  const r = 36, cx = 44, cy = 44, strokeWidth = 8
  const circumference = 2 * Math.PI * r
  const offset = circumference - (value / 100) * circumference
  return (
    <svg viewBox="0 0 88 88" className="w-24 h-24">
      <circle cx={cx} cy={cy} r={r} fill="none" stroke="#1e293b" strokeWidth={strokeWidth} />
      <circle cx={cx} cy={cy} r={r} fill="none" stroke={color} strokeWidth={strokeWidth}
        strokeDasharray={circumference} strokeDashoffset={offset}
        strokeLinecap="round" transform="rotate(-90 44 44)" />
      <text x={cx} y={cy} textAnchor="middle" dominantBaseline="middle"
        fill={color} fontSize="16" fontWeight="bold">{value}</text>
    </svg>
  )
}

interface Entity {
  entity_id: string
  name: string
  composite_score: number
  level: string
}

interface DomainData {
  domain: string
  entities: Entity[]
  avg_composite: number
  risk_distribution: Record<string, number>
}

export default function PandemicHealthEmergencyRightsDashboard() {
  const [data, setData] = useState<DomainData | null>(null)
  const color = "#06b6d4"

  useEffect(() => {
    fetch("/api/pandemic-health-emergency-rights-engine")
      .then(r => r.json())
      .then(d => setData(d.payload ?? d))
  }, [])

  if (!data) return <div className="min-h-screen bg-slate-950 flex items-center justify-center"><div className="text-slate-400 text-xl">Chargement...</div></div>

  return (
    <div className="min-h-screen bg-slate-950 text-white p-8">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-3xl font-bold mb-2" style={{ color }}>Urgences Sanitaires &amp; Droits Humains</h1>
        <p className="text-slate-400 mb-8">Score moyen : <span className="font-bold" style={{ color }}>{data.avg_composite.toFixed(2)}</span> / 100</p>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {data.entities.map(e => (
            <div key={e.entity_id} className="bg-slate-900 rounded-xl p-6 border border-slate-800">
              <div className="flex justify-center mb-4">
                <GaugeRing value={Math.round(e.composite_score)} color={
                  e.level === "critique" ? "#ef4444" :
                  e.level === "élevé" ? "#f97316" :
                  e.level === "modéré" ? "#eab308" : "#22c55e"
                } />
              </div>
              <p className="text-xs text-slate-500 font-mono mb-1">{e.entity_id}</p>
              <h3 className="font-semibold text-sm text-center mb-2">{e.name}</h3>
              <div className="text-center">
                <span className={`text-xs px-2 py-1 rounded-full ${
                  e.level === "critique" ? "bg-red-900 text-red-300" :
                  e.level === "élevé" ? "bg-orange-900 text-orange-300" :
                  e.level === "modéré" ? "bg-yellow-900 text-yellow-300" :
                  "bg-green-900 text-green-300"
                }`}>{e.level}</span>
              </div>
            </div>
          ))}
        </div>
        <div className="bg-slate-900 rounded-xl p-6 border border-slate-800">
          <h2 className="text-lg font-semibold mb-4" style={{ color }}>Distribution des risques</h2>
          <div className="flex gap-4 flex-wrap">
            {Object.entries(data.risk_distribution).map(([level, count]) => (
              <div key={level} className="flex items-center gap-2">
                <div className="w-3 h-3 rounded-full" style={{ backgroundColor:
                  level === "critique" ? "#ef4444" :
                  level === "élevé" ? "#f97316" :
                  level === "modéré" ? "#eab308" : "#22c55e"
                }} />
                <span className="text-sm text-slate-300">{level}: <strong>{String(count)}</strong></span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
