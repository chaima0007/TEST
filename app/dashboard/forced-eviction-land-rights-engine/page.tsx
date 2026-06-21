"use client"

import { useEffect, useState } from "react"

interface Entity {
  id: string
  name: string
  country: string
  sector: string
  composite_score: number
  severity: string
  estimated_forced_eviction_land_rights_index: number
  key_violation?: string
}

interface EngineData {
  engine: string
  wave: number
  accent_color: string
  entities: Entity[]
  summary: {
    avg_composite: number
    critique: number
    élevé: number
    modéré: number
    faible: number
    distribution_valid: boolean
  }
}

function GaugeRing({ score, accent }: { score: number; accent: string }) {
  const r = 36, cx = 44, cy = 44
  const circumference = 2 * Math.PI * r
  const offset = circumference - (score / 100) * circumference
  return (
    <svg viewBox="0 0 88 88" style={{ width: 88, height: 88 }}>
      <circle cx={cx} cy={cy} r={r} fill="none" stroke="#1e293b" strokeWidth={8} />
      <circle cx={cx} cy={cy} r={r} fill="none" stroke={accent} strokeWidth={8}
        strokeDasharray={circumference} strokeDashoffset={offset}
        strokeLinecap="round" transform="rotate(-90 44 44)" />
      <text x={cx} y={cy} textAnchor="middle" dominantBaseline="central"
        style={{ fill: "#f8fafc", fontSize: 16, fontWeight: "bold" }}>
        {Math.round(score)}
      </text>
    </svg>
  )
}

export default function ForcedEvictionLandRightsPage() {
  const [data, setData] = useState<EngineData | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch("/api/forced-eviction-land-rights-engine")
      .then(r => r.json())
      .then(d => { setData(d.payload ?? d); setLoading(false) })
      .catch(() => setLoading(false))
  }, [])

  if (loading) return (
    <div style={{ minHeight: "100vh", background: "#0f172a", display: "flex", alignItems: "center", justifyContent: "center", color: "#0f766e", fontSize: "1.2rem" }}>
      Chargement...
    </div>
  )
  if (!data) return (
    <div style={{ minHeight: "100vh", background: "#0f172a", display: "flex", alignItems: "center", justifyContent: "center", color: "#dc2626" }}>
      Erreur de chargement
    </div>
  )

  const ACCENT = data.accent_color || "#0f766e"

  const severityColor = (s: string) => {
    if (s === "critique") return "#dc2626"
    if (s === "élevé") return "#f97316"
    if (s === "modéré") return "#eab308"
    return "#22c55e"
  }

  return (
    <main style={{ minHeight: "100vh", background: "#0f172a", color: "#f8fafc", padding: "2rem", fontFamily: "system-ui, sans-serif" }}>
      {/* Header */}
      <div style={{ marginBottom: "2rem", borderBottom: `2px solid ${ACCENT}`, paddingBottom: "1rem" }}>
        <h1 style={{ fontSize: "1.75rem", fontWeight: "bold", color: ACCENT, margin: 0 }}>
          Expulsion Forc&eacute;e &amp; Droits Fonciers
        </h1>
        <p style={{ color: "#94a3b8", margin: "0.5rem 0 0" }}>
          Wave {data.wave} &middot; avg composite {data.summary.avg_composite.toFixed(2)} &middot; CSDDD Art.8-13
        </p>
      </div>

      {/* Summary badges */}
      <div style={{ display: "flex", gap: "1rem", marginBottom: "2rem", flexWrap: "wrap" }}>
        {[
          { label: "Critique", count: data.summary.critique, color: "#dc2626" },
          { label: "Élevé", count: data.summary.élevé, color: "#f97316" },
          { label: "Modéré", count: data.summary.modéré, color: "#eab308" },
          { label: "Faible", count: data.summary.faible, color: "#22c55e" },
        ].map(({ label, count, color }) => (
          <div key={label} style={{ background: "#1e293b", padding: "1rem 1.5rem", borderRadius: "0.75rem", textAlign: "center", minWidth: 80, border: `1px solid ${color}40` }}>
            <div style={{ color, fontSize: "2rem", fontWeight: "bold" }}>{count}</div>
            <div style={{ color: "#94a3b8", fontSize: "0.75rem" }}>{label}</div>
          </div>
        ))}
        <div style={{ background: "#1e293b", padding: "1rem 1.5rem", borderRadius: "0.75rem", textAlign: "center", border: `1px solid ${ACCENT}40` }}>
          <div style={{ color: ACCENT, fontSize: "2rem", fontWeight: "bold" }}>{data.summary.avg_composite.toFixed(1)}</div>
          <div style={{ color: "#94a3b8", fontSize: "0.75rem" }}>Score moyen</div>
        </div>
      </div>

      {/* Entity grid */}
      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(320px, 1fr))", gap: "1rem" }}>
        {data.entities.map(entity => (
          <div key={entity.id} style={{
            background: "#1e293b",
            borderRadius: "0.75rem",
            padding: "1.5rem",
            border: `1px solid ${severityColor(entity.severity)}30`
          }}>
            <div style={{ display: "flex", alignItems: "center", gap: "1rem", marginBottom: "1rem" }}>
              <GaugeRing score={entity.composite_score} accent={severityColor(entity.severity)} />
              <div style={{ flex: 1 }}>
                <div style={{ fontWeight: "bold", fontSize: "1rem", marginBottom: "0.25rem" }}>{entity.name}</div>
                <div style={{ color: "#64748b", fontSize: "0.75rem", marginBottom: "0.4rem" }}>{entity.country} · {entity.sector}</div>
                <span style={{
                  background: `${severityColor(entity.severity)}20`,
                  color: severityColor(entity.severity),
                  padding: "0.15rem 0.6rem",
                  borderRadius: "1rem",
                  fontSize: "0.7rem",
                  fontWeight: "bold",
                  textTransform: "uppercase" as const,
                }}>
                  {entity.severity}
                </span>
              </div>
            </div>
            {entity.key_violation && (
              <div style={{ color: "#94a3b8", fontSize: "0.75rem", fontStyle: "italic", marginBottom: "0.75rem", borderLeft: `3px solid ${severityColor(entity.severity)}`, paddingLeft: "0.75rem" }}>
                {entity.key_violation}
              </div>
            )}
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
              <span style={{ color: "#64748b", fontSize: "0.75rem" }}>Index FEL</span>
              <span style={{ color: ACCENT, fontWeight: "bold", fontSize: "1.1rem" }}>
                {entity.estimated_forced_eviction_land_rights_index}
              </span>
            </div>
          </div>
        ))}
      </div>

      {/* Footer */}
      <div style={{ marginTop: "3rem", padding: "1rem", background: "#1e293b", borderRadius: "0.5rem", display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <span style={{ color: "#64748b", fontSize: "0.75rem" }}>CaelumSwarm™ · Wave {data.wave} · Distribution valide: {data.summary.distribution_valid ? "✓" : "✗"}</span>
        <span style={{ color: ACCENT, fontSize: "0.75rem" }}>4 critique / 2 élevé / 1 modéré / 1 faible</span>
      </div>
    </main>
  )
}
