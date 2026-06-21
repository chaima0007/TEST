"use client"
import { useState, useEffect } from "react"

const ACCENT = "#a78bfa"

const RC: Record<string, string> = { critique: "text-red-400", "élevé": "text-orange-400", modéré: "text-yellow-400", faible: "text-emerald-400" }
const RB: Record<string, string> = { critique: "border-red-500/30 bg-red-500/10", "élevé": "border-orange-500/30 bg-orange-500/10", modéré: "border-yellow-500/30 bg-yellow-500/10", faible: "border-emerald-500/30 bg-emerald-500/10" }

function GaugeRing({ value, label }: { value: number; label: string }) {
  const r = 36
  const circ = 2 * Math.PI * r
  const fill = circ * (1 - Math.min(value, 100) / 100)
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
  )
}

interface Entity {
  id: string
  name: string
  composite_score: number
  risk_level: string
  estimated_statelessness_index: number
  [key: string]: unknown
}

interface DashData {
  domain?: string
  avg_composite?: number
  risk_distribution?: Record<string, number>
  entities?: Entity[]
  [key: string]: unknown
}

export default function StatelessPersonsDocumentationPage() {
  const [data, setData] = useState<DashData | null>(null)
  const [loading, setLoading] = useState(true)
  const [filter, setFilter] = useState("tous")

  useEffect(() => {
    fetch("/api/stateless-persons-documentation-engine")
      .then(r => r.json())
      .then(d => { setData(d.payload ?? d); setLoading(false) })
      .catch(() => { setLoading(false) })
  }, [])

  if (loading) {
    return (
      <div className="bg-slate-950 min-h-screen flex items-center justify-center">
        <div className="animate-pulse text-sm" style={{ color: ACCENT }}>Initialisation Apatridie &amp; Documentation des Personnes…</div>
      </div>
    )
  }

  if (!data) {
    return (
      <div className="bg-slate-950 min-h-screen flex items-center justify-center">
        <div className="text-red-400 text-sm">Données indisponibles</div>
      </div>
    )
  }

  const allEntities: Entity[] = data?.entities ?? []
  const filtered = filter === "tous" ? allEntities : allEntities.filter(e => e.risk_level === filter)
  const avg = (arr: number[]) => arr.length ? arr.reduce((a, b) => a + b, 0) / arr.length : 0
  const avgComposite = data?.avg_composite ?? avg(allEntities.map(e => e.composite_score))
  const avgIndex = avg(allEntities.map(e => e.estimated_statelessness_index))
  const rd = data?.risk_distribution ?? {}
  const countCritique = rd["critique"] ?? allEntities.filter(e => e.risk_level === "critique").length
  const countEleve = rd["élevé"] ?? allEntities.filter(e => e.risk_level === "élevé").length
  const countModere = rd["modéré"] ?? allEntities.filter(e => e.risk_level === "modéré").length
  const countFaible = rd["faible"] ?? allEntities.filter(e => e.risk_level === "faible").length

  const kpis = [
    { label: "Entités Analysées", value: allEntities.length },
    { label: "Score Composite Moyen", value: avgComposite.toFixed(2) },
    { label: "Indice apatridie", value: avgIndex.toFixed(2) },
    { label: "Critique", value: countCritique },
    { label: "Élevé", value: countEleve },
    { label: "Modéré / Faible", value: `${countModere} / ${countFaible}` },
  ]

  const filters = ["tous", "critique", "élevé", "modéré", "faible"]

  return (
    <div className="min-h-screen bg-slate-950 text-white p-6 space-y-6">
      {/* Header */}
      <div>
        <div className="flex items-center gap-3 mb-1">
          <div className="w-3 h-8 rounded-full" style={{ background: ACCENT }} />
          <h1 className="text-2xl font-bold tracking-tight">Apatridie &amp; Documentation des Personnes</h1>
        </div>
        <p className="text-slate-400 text-sm ml-6">
          Personnes sans nationalité — surveillance mondiale des droits
        </p>
      </div>

      {/* KPI Cards */}
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
        <h2 className="text-sm font-semibold text-slate-400 mb-4">Indicateurs Clés</h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
          <GaugeRing value={avgComposite} label="Score Composite" />
          <GaugeRing value={avgIndex * 10} label="Indice apatridie (×10)" />
          <GaugeRing value={(countCritique / Math.max(allEntities.length, 1)) * 100} label="% Critique" />
          <GaugeRing value={(countEleve / Math.max(allEntities.length, 1)) * 100} label="% Élevé" />
        </div>
      </div>

      {/* Risk Distribution */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
        <h2 className="text-sm font-semibold text-slate-400 mb-4">Distribution des Risques</h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="bg-red-950/40 border border-red-800/30 rounded-xl p-4 text-center">
            <div className="text-3xl font-bold text-red-400">{countCritique}</div>
            <div className="text-red-300/70 text-sm mt-1">Critique</div>
          </div>
          <div className="bg-orange-950/40 border border-orange-800/30 rounded-xl p-4 text-center">
            <div className="text-3xl font-bold text-orange-400">{countEleve}</div>
            <div className="text-orange-300/70 text-sm mt-1">Élevé</div>
          </div>
          <div className="bg-yellow-950/40 border border-yellow-800/30 rounded-xl p-4 text-center">
            <div className="text-3xl font-bold text-yellow-400">{countModere}</div>
            <div className="text-yellow-300/70 text-sm mt-1">Modéré</div>
          </div>
          <div className="bg-green-950/40 border border-green-800/30 rounded-xl p-4 text-center">
            <div className="text-3xl font-bold text-green-400">{countFaible}</div>
            <div className="text-green-300/70 text-sm mt-1">Faible</div>
          </div>
        </div>
      </div>

      {/* Filter Pills */}
      <div className="flex gap-2 flex-wrap">
        {filters.map(f => (
          <button key={f} onClick={() => setFilter(f)}
            className={`px-4 py-1.5 rounded-full text-sm font-medium transition-all ${filter === f ? "text-white font-bold" : "bg-slate-800 text-slate-400 hover:bg-slate-700"}`}
            style={filter === f ? { background: ACCENT } : {}}>
            {f.charAt(0).toUpperCase() + f.slice(1)}
          </button>
        ))}
      </div>

      {/* Entity Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
        {filtered.map(e => (
          <div key={e.id}
            className={`border rounded-xl p-4 ${RB[e.risk_level] ?? "border-slate-700 bg-slate-900"}`}>
            <div className="flex justify-between items-start mb-2">
              <div className="flex-1 min-w-0">
                <div className="font-semibold text-sm leading-tight">{e.name}</div>
                <div className="text-xs text-slate-500 mt-0.5">{e.id}</div>
              </div>
              <div className="text-right ml-3 flex-shrink-0">
                <div className="text-xl font-bold text-white">{e.composite_score.toFixed(1)}</div>
                <div className={`text-xs font-bold uppercase mt-1 ${RC[e.risk_level] ?? "text-slate-400"}`}>{e.risk_level}</div>
              </div>
            </div>
            <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden mt-2">
              <div className="h-full rounded-full transition-all" style={{ width: `${Math.min(e.composite_score, 100)}%`, background: ACCENT }} />
            </div>
            <div className="text-xs text-slate-500 mt-2">
              Indice apatridie: <span className="font-medium" style={{ color: ACCENT }}>{typeof e.estimated_statelessness_index === "number" ? e.estimated_statelessness_index.toFixed(2) : "—"}</span>
            </div>
          </div>
        ))}
      </div>

      {filtered.length === 0 && (
        <div className="text-center py-12 text-slate-500 text-sm">Aucune entité pour ce niveau de risque.</div>
      )}

      {/* Meta */}
      <div className="text-slate-600 text-xs text-right">
        Domaine : {data.domain} · Entités : {allEntities.length}
      </div>
    </div>
  )
}
