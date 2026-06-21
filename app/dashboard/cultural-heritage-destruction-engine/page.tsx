"use client"
import { useState, useEffect } from "react"

const ACCENT = "#d97706"
const RISK_CONFIG: Record<string, { label: string; color: string; bg: string; border: string; dot: string }> = {
  critique: { label: "Critique", color: "text-red-400", bg: "bg-red-500/10", border: "border-red-500/25", dot: "bg-red-500" },
  "élevé": { label: "Élevé", color: "text-orange-400", bg: "bg-orange-500/10", border: "border-orange-500/25", dot: "bg-orange-500" },
  modéré: { label: "Modéré", color: "text-yellow-400", bg: "bg-yellow-500/10", border: "border-yellow-500/25", dot: "bg-yellow-500" },
  faible: { label: "Faible", color: "text-emerald-400", bg: "bg-emerald-500/10", border: "border-emerald-500/25", dot: "bg-emerald-500" },
}
const FILTER_OPTIONS = [
  { key: "tous", label: "Tous" },
  { key: "critique", label: "Critique" },
  { key: "élevé", label: "Élevé" },
  { key: "modéré", label: "Modéré" },
  { key: "faible", label: "Faible" },
]

interface CulturalHeritageEntity {
  id: string
  name: string
  composite_score: number
  risk_level: string
  estimated_heritage_protection_index: number
}
interface CulturalHeritageData {
  entities: CulturalHeritageEntity[]
  avg_composite: number
  risk_distribution: Record<string, number>
  domain: string
}

function GaugeRing({ value, max, label, color }: { value: number; max: number; label: string; color: string }) {
  const pct = Math.min(100, Math.max(0, (value / max) * 100))
  const r = 36
  const circ = 226.19
  return (
    <div className="flex flex-col items-center gap-2">
      <svg width="88" height="88" viewBox="0 0 88 88">
        <circle cx="44" cy="44" r={r} fill="none" stroke="rgba(255,255,255,0.07)" strokeWidth="8" />
        <circle cx="44" cy="44" r={r} fill="none" stroke={color} strokeWidth="8" strokeLinecap="round"
          strokeDasharray={`${(pct / 100) * circ} ${circ}`}
          transform="rotate(-90 44 44)"
          style={{ transition: "stroke-dasharray 0.7s ease" }} />
        <text x="44" y="48" textAnchor="middle" fontSize="13" fontWeight="700" fill="white">{Math.round(value)}</text>
      </svg>
      <span className="text-xs text-gray-400 text-center leading-tight">{label}</span>
    </div>
  )
}

function DistBar({ label, count, total, color }: { label: string; count: number; total: number; color: string }) {
  const pct = total > 0 ? Math.round((count / total) * 100) : 0
  return (
    <div className="space-y-1">
      <div className="flex justify-between text-xs">
        <span className="text-gray-300">{label}</span>
        <span className="text-gray-400">{count} <span className="text-gray-600">({pct}%)</span></span>
      </div>
      <div className="h-2 bg-white/5 rounded-full overflow-hidden">
        <div className="h-full rounded-full transition-all duration-700" style={{ width: `${pct}%`, backgroundColor: color }} />
      </div>
    </div>
  )
}

function KpiCard({ label, value, sub, accent }: { label: string; value: string | number; sub?: string; accent?: string }) {
  return (
    <div className="bg-white/4 border border-white/10 rounded-xl px-5 py-4 hover:bg-white/6 transition-colors">
      <p className="text-xs text-gray-400 mb-1">{label}</p>
      <p className={`text-2xl font-bold ${accent ?? "text-white"}`}>{value}</p>
      {sub && <p className="text-xs text-gray-500 mt-0.5">{sub}</p>}
    </div>
  )
}

function EntityCard({ entity, onClick }: { entity: CulturalHeritageEntity; onClick: (e: CulturalHeritageEntity) => void }) {
  const cfg = RISK_CONFIG[entity.risk_level] ?? RISK_CONFIG.faible
  return (
    <button onClick={() => onClick(entity)}
      className={`w-full text-left bg-white/4 border ${cfg.border} rounded-xl p-4 hover:bg-white/7 transition-all`}>
      <div className="flex items-start justify-between gap-3 mb-3">
        <div className="min-w-0">
          <p className="font-semibold text-white truncate">{entity.name}</p>
          <p className="text-xs text-gray-400 mt-0.5">{entity.id}</p>
        </div>
        <span className={`shrink-0 text-xs font-medium px-2.5 py-1 rounded-full border ${cfg.bg} ${cfg.border} ${cfg.color}`}>
          {cfg.label}
        </span>
      </div>
      <div className="grid grid-cols-2 gap-2 mb-3">
        <div className="bg-white/4 rounded-lg p-2 text-center">
          <p className="text-sm font-bold text-white">{entity.composite_score}</p>
          <p className="text-[10px] text-gray-500">Score composite</p>
        </div>
        <div className="bg-white/4 rounded-lg p-2 text-center">
          <p className="text-sm font-bold text-white">{entity.estimated_heritage_protection_index}/10</p>
          <p className="text-[10px] text-gray-500">Indice patrimoine</p>
        </div>
      </div>
      <div className="flex items-center justify-between text-xs">
        <span className="text-gray-400">Risque: <span className={`font-bold ${cfg.color}`}>{cfg.label}</span></span>
      </div>
    </button>
  )
}

function DetailModal({ entity, onClose }: { entity: CulturalHeritageEntity; onClose: () => void }) {
  const cfg = RISK_CONFIG[entity.risk_level] ?? RISK_CONFIG.faible
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm" onClick={onClose}>
      <div className="w-full max-w-xl bg-slate-900 border border-white/12 rounded-2xl shadow-2xl overflow-hidden" onClick={(e) => e.stopPropagation()}>
        <div className="px-6 pt-6 pb-4 border-b border-white/8">
          <div className="flex items-start justify-between gap-4">
            <div>
              <h2 className="text-lg font-bold text-white">{entity.name}</h2>
              <p className="text-sm text-gray-400 mt-0.5">{entity.id}</p>
            </div>
            <div className="flex items-center gap-2">
              <span className={`text-xs font-medium px-2.5 py-1 rounded-full border ${cfg.bg} ${cfg.border} ${cfg.color}`}>{cfg.label}</span>
              <button onClick={onClose} className="text-gray-400 hover:text-white transition-colors ml-1">
                <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                  <path d="M5 5l10 10M15 5L5 15" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
                </svg>
              </button>
            </div>
          </div>
        </div>
        <div className="px-6 py-5 space-y-4">
          <div className="grid grid-cols-2 gap-3">
            {[
              { label: "Score Composite", value: `${entity.composite_score}/100` },
              { label: "Indice Protection Patrimoine", value: `${entity.estimated_heritage_protection_index}/10` },
              { label: "Niveau de risque", value: cfg.label },
              { label: "Identifiant", value: entity.id },
            ].map(({ label, value }) => (
              <div key={label} className="bg-white/4 rounded-lg p-3">
                <p className="text-[11px] text-gray-500 mb-0.5">{label}</p>
                <p className="text-sm font-semibold text-white">{value}</p>
              </div>
            ))}
          </div>
          <div className="bg-white/4 rounded-lg p-4">
            <div className="flex justify-between items-center mb-2">
              <span className="text-sm text-gray-300">Score Composite</span>
              <span className={`text-xl font-bold ${cfg.color}`}>{entity.composite_score}</span>
            </div>
            <div className="h-2 bg-white/5 rounded-full overflow-hidden">
              <div className="h-full rounded-full transition-all duration-700"
                style={{ width: `${Math.min(100, entity.composite_score)}%`, backgroundColor: ACCENT }} />
            </div>
            <p className="text-[11px] text-gray-500 mt-1.5">
              Destruction délibérée du patrimoine culturel de l&apos;humanité — sites UNESCO &amp; monuments historiques
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default function CulturalHeritageDestructionDashboard() {
  const [data, setData] = useState<CulturalHeritageData | null>(null)
  const [loading, setLoading] = useState(true)
  const [filter, setFilter] = useState("tous")
  const [selected, setSelected] = useState<CulturalHeritageEntity | null>(null)

  useEffect(() => {
    fetch("/api/cultural-heritage-destruction-engine")
      .then((r) => r.json())
      .then((d) => {
        const payload = d.payload ?? d
        setData(payload)
        setLoading(false)
      })
      .catch(console.error)
  }, [])

  const entities = data?.entities ?? []
  const filtered = filter === "tous" ? entities : entities.filter((e) => e.risk_level === filter)
  const dist = data?.risk_distribution ?? {}
  const total = entities.length
  const critiques = dist["critique"] ?? 0

  return (
    <div className="min-h-screen bg-slate-950 text-white">
      <div className="max-w-7xl mx-auto px-6 py-8 space-y-8">

        <div className="flex items-start justify-between gap-4">
          <div>
            <h1 className="text-2xl font-bold text-white">Destruction Patrimoine Culturel</h1>
            <p className="text-sm text-gray-400 mt-1">
              Destruction &amp; pillage du patrimoine culturel mondial — sites UNESCO &amp; monuments historiques
            </p>
          </div>
          <span className="text-xs text-gray-500 bg-white/5 border border-white/10 rounded-lg px-3 py-1.5">
            {total} entités analysées
          </span>
        </div>

        {loading && (
          <div className="flex items-center justify-center py-24">
            <div className="w-8 h-8 border-2 border-t-transparent rounded-full animate-spin" style={{ borderColor: ACCENT, borderTopColor: "transparent" }} />
          </div>
        )}

        {!loading && data && (
          <>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
              <KpiCard label="Entités analysées" value={total} sub="zones surveillées" />
              <KpiCard label="Score composite moyen" value={data.avg_composite?.toFixed(2) ?? "—"} sub="indice agrégé"
                accent={data.avg_composite >= 60 ? "text-red-400" : data.avg_composite >= 40 ? "text-orange-400" : "text-emerald-400"} />
              <KpiCard label="Cas critiques" value={critiques} sub="intervention urgente" accent="text-red-400" />
              <KpiCard label="Élevé" value={dist["élevé"] ?? 0} sub="risque élevé" accent="text-orange-400" />
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <div className="bg-white/4 border border-white/10 rounded-xl p-6">
                <h2 className="text-sm font-semibold text-gray-300 mb-6">Indicateurs Destruction Patrimoine</h2>
                <div className="grid grid-cols-4 gap-4">
                  <GaugeRing value={data.avg_composite} max={100} label="Score Moyen" color={ACCENT} />
                  <GaugeRing value={critiques} max={total} label="Critique" color="#ef4444" />
                  <GaugeRing value={dist["élevé"] ?? 0} max={total} label="Élevé" color="#fb923c" />
                  <GaugeRing value={dist["modéré"] ?? 0} max={total} label="Modéré" color="#fbbf24" />
                </div>
              </div>

              <div className="bg-white/4 border border-white/10 rounded-xl p-6">
                <h2 className="text-sm font-semibold text-gray-300 mb-6">Distribution par Niveau de Risque</h2>
                <div className="space-y-4">
                  <DistBar label="Critique" count={dist["critique"] ?? 0} total={total} color="#f87171" />
                  <DistBar label="Élevé" count={dist["élevé"] ?? 0} total={total} color="#fb923c" />
                  <DistBar label="Modéré" count={dist["modéré"] ?? 0} total={total} color="#fbbf24" />
                  <DistBar label="Faible" count={dist["faible"] ?? 0} total={total} color="#34d399" />
                </div>
              </div>
            </div>

            <div className="flex flex-wrap gap-2">
              {FILTER_OPTIONS.map((opt) => {
                const isActive = filter === opt.key
                const cfg = opt.key !== "tous" ? RISK_CONFIG[opt.key] : null
                const count = opt.key === "tous" ? total : (dist[opt.key] ?? 0)
                return (
                  <button key={opt.key} onClick={() => setFilter(opt.key)}
                    className={`px-4 py-1.5 rounded-full text-sm font-medium border transition-all ${isActive
                      ? cfg ? `${cfg.bg} ${cfg.border} ${cfg.color}` : "bg-white/10 border-white/20 text-white"
                      : "bg-transparent border-white/10 text-gray-400 hover:text-white hover:border-white/20"}`}>
                    {opt.label}
                    <span className="ml-1.5 text-xs opacity-70">{count}</span>
                  </button>
                )
              })}
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
              {filtered.map((entity) => (
                <EntityCard key={entity.id} entity={entity} onClick={setSelected} />
              ))}
              {filtered.length === 0 && (
                <div className="col-span-full text-center py-12 text-gray-400 text-sm">
                  Aucune entité dans ce niveau de risque
                </div>
              )}
            </div>

            {critiques > 0 && (
              <div className="rounded-xl px-5 py-4 flex items-start gap-3" style={{ backgroundColor: "rgba(217,119,6,0.08)", border: "1px solid rgba(217,119,6,0.2)" }}>
                <div className="w-2 h-2 rounded-full mt-1.5 shrink-0 animate-pulse" style={{ backgroundColor: ACCENT }} />
                <div>
                  <p className="text-sm font-medium" style={{ color: ACCENT }}>
                    {critiques} entité{critiques > 1 ? "s" : ""} en situation critique de destruction du patrimoine culturel
                  </p>
                  <p className="text-xs mt-0.5" style={{ color: `${ACCENT}b3` }}>
                    Intervention immédiate requise — protection du patrimoine de l&apos;humanité prioritaire
                  </p>
                </div>
              </div>
            )}
          </>
        )}
      </div>

      {selected && <DetailModal entity={selected} onClose={() => setSelected(null)} />}
    </div>
  )
}
