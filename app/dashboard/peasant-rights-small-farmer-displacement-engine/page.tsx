"use client"
import { useEffect, useState } from "react"

interface Entity {
  id: string
  name: string
  composite_score: number
  risk_level: string
  estimated_peasant_rights_index: number
}

interface DomainData {
  domain: string
  generated_at: string
  entities: Entity[]
  avg_composite: number
  risk_distribution: Record<string, number>
}

const ACCENT = "#16a34a"

function GaugeRing({ score }: { score: number }) {
  const r = 36, cx = 44, cy = 44
  const circumference = 2 * Math.PI * r
  const filled = (score / 100) * circumference
  return (
    <svg viewBox="0 0 88 88" width={88} height={88}>
      <circle cx={cx} cy={cy} r={r} fill="none" stroke="#1e293b" strokeWidth={8} />
      <circle
        cx={cx} cy={cy} r={r} fill="none" stroke={ACCENT} strokeWidth={8}
        strokeDasharray={`${filled} ${circumference - filled}`}
        transform="rotate(-90 44 44)" strokeLinecap="round"
      />
      <text x={cx} y={cy + 5} textAnchor="middle" fill="#f1f5f9" fontSize={14} fontWeight="bold">
        {score.toFixed(0)}
      </text>
    </svg>
  )
}

function RiskBadge({ level }: { level: string }) {
  const colors: Record<string, string> = {
    critique: "#ef4444",
    "élevé": "#f97316",
    modéré: "#eab308",
    faible: "#22c55e",
  }
  return (
    <span style={{
      background: colors[level] ?? "#64748b",
      color: "#fff",
      borderRadius: 6,
      padding: "2px 10px",
      fontSize: 11,
      fontWeight: 700,
      textTransform: "uppercase",
      letterSpacing: 0.5,
      whiteSpace: "nowrap",
    }}>
      {level}
    </span>
  )
}

export default function PeasantRightsSmallFarmerPage() {
  const [data, setData] = useState<DomainData | null>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetch("/api/peasant-rights-small-farmer-displacement-engine")
      .then((r) => r.json())
      .then((d) => setData(d.payload ?? d))
      .catch(() => setError("Erreur de chargement des données"))
  }, [])

  if (error) return (
    <div style={{ minHeight: "100vh", background: "#0f172a", color: "#f1f5f9", display: "flex", alignItems: "center", justifyContent: "center" }}>
      <p style={{ color: "#ef4444" }}>{error}</p>
    </div>
  )

  if (!data) return (
    <div style={{ minHeight: "100vh", background: "#0f172a", color: "#f1f5f9", display: "flex", alignItems: "center", justifyContent: "center" }}>
      <p style={{ color: "#94a3b8" }}>Chargement...</p>
    </div>
  )

  return (
    <div style={{ minHeight: "100vh", background: "#0f172a", color: "#f1f5f9", padding: "2rem" }}>
      {/* Header */}
      <div style={{ marginBottom: "2rem" }}>
        <div style={{ display: "flex", alignItems: "center", gap: "0.75rem", marginBottom: "0.5rem" }}>
          <div style={{ width: 12, height: 12, borderRadius: "50%", background: ACCENT }} />
          <span style={{ fontSize: 12, color: "#94a3b8", textTransform: "uppercase", letterSpacing: 1 }}>Wave 185 · Droits Humains</span>
        </div>
        <h1 style={{ fontSize: "1.75rem", fontWeight: 700, color: "#f1f5f9", margin: 0 }}>
          Droits Paysans & Déplacement des Petits Agriculteurs
        </h1>
        <p style={{ color: "#64748b", marginTop: "0.25rem", fontSize: 14 }}>
          Analyse mondiale des violations des droits agraires, accaparement des terres et déplacement des communautés rurales
        </p>
      </div>

      {/* Stats */}
      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))", gap: "1rem", marginBottom: "2rem" }}>
        <div style={{ background: "#1e293b", borderRadius: 12, padding: "1.25rem", borderLeft: `4px solid ${ACCENT}` }}>
          <p style={{ fontSize: 12, color: "#94a3b8", margin: 0, textTransform: "uppercase", letterSpacing: 0.5 }}>Score Moyen</p>
          <p style={{ fontSize: "2rem", fontWeight: 700, color: ACCENT, margin: "0.25rem 0 0" }}>{data.avg_composite.toFixed(1)}</p>
        </div>
        <div style={{ background: "#1e293b", borderRadius: 12, padding: "1.25rem", borderLeft: "4px solid #ef4444" }}>
          <p style={{ fontSize: 12, color: "#94a3b8", margin: 0, textTransform: "uppercase", letterSpacing: 0.5 }}>Critique</p>
          <p style={{ fontSize: "2rem", fontWeight: 700, color: "#ef4444", margin: "0.25rem 0 0" }}>{data.risk_distribution["critique"] ?? 0}</p>
        </div>
        <div style={{ background: "#1e293b", borderRadius: 12, padding: "1.25rem", borderLeft: "4px solid #f97316" }}>
          <p style={{ fontSize: 12, color: "#94a3b8", margin: 0, textTransform: "uppercase", letterSpacing: 0.5 }}>Élevé</p>
          <p style={{ fontSize: "2rem", fontWeight: 700, color: "#f97316", margin: "0.25rem 0 0" }}>{data.risk_distribution["élevé"] ?? 0}</p>
        </div>
        <div style={{ background: "#1e293b", borderRadius: 12, padding: "1.25rem", borderLeft: "4px solid #22c55e" }}>
          <p style={{ fontSize: 12, color: "#94a3b8", margin: 0, textTransform: "uppercase", letterSpacing: 0.5 }}>Entités</p>
          <p style={{ fontSize: "2rem", fontWeight: 700, color: "#22c55e", margin: "0.25rem 0 0" }}>{data.entities.length}</p>
        </div>
      </div>

      {/* Entities */}
      <div style={{ display: "grid", gap: "1rem" }}>
        {data.entities.map((entity) => (
          <div key={entity.id} style={{ background: "#1e293b", borderRadius: 12, padding: "1.25rem", display: "flex", alignItems: "center", gap: "1.25rem", border: "1px solid #334155" }}>
            <GaugeRing score={entity.composite_score} />
            <div style={{ flex: 1, minWidth: 0 }}>
              <div style={{ display: "flex", alignItems: "center", gap: "0.5rem", marginBottom: "0.4rem", flexWrap: "wrap" }}>
                <span style={{ fontSize: 11, color: "#475569", fontWeight: 600 }}>{entity.id}</span>
                <RiskBadge level={entity.risk_level} />
              </div>
              <p style={{ margin: 0, fontSize: 14, color: "#e2e8f0", lineHeight: 1.4 }}>{entity.name}</p>
              <p style={{ margin: "0.3rem 0 0", fontSize: 12, color: "#64748b" }}>
                Index droits paysans : <span style={{ color: ACCENT, fontWeight: 600 }}>{entity.estimated_peasant_rights_index.toFixed(2)}</span> / 10
              </p>
            </div>
          </div>
        ))}
      </div>

      {/* Footer */}
      <div style={{ marginTop: "2rem", paddingTop: "1rem", borderTop: "1px solid #1e293b", display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <span style={{ fontSize: 12, color: "#334155" }}>Wave 185 · Caelum Partners Swarm Intelligence</span>
        <span style={{ fontSize: 12, color: "#334155" }}>{new Date(data.generated_at).toLocaleString("fr-FR")}</span>
      </div>
    </div>
  )
}
