"use client"
import { useEffect, useState } from "react"

const ACCENT = "#ea580c"
const DOMAIN_SLUG = "child-agricultural-labor-engine"

type Entity = {
  id: string
  name: string
  country: string
  composite_score: number
  severity: string
  estimated_child_agricultural_labor_index: number
  key_violation: string
}

type Summary = {
  avg_composite: number
  critique: number
  élevé: number
  modéré: number
  faible: number
}

type EngineData = {
  engine: string
  wave: number
  accent_color: string
  entities: Entity[]
  summary: Summary
}

function GaugeRing({ score, accent }: { score: number; accent: string }) {
  const r = 36, cx = 44, cy = 44
  const circumference = 2 * Math.PI * r
  const offset = circumference - (Math.min(Math.max(score, 0), 100) / 100) * circumference
  return (
    <svg viewBox="0 0 88 88" style={{ width: 88, height: 88, flexShrink: 0 }}>
      <circle cx={cx} cy={cy} r={r} fill="none" stroke="#1e293b" strokeWidth={8} />
      <circle
        cx={cx} cy={cy} r={r} fill="none"
        stroke={accent} strokeWidth={8}
        strokeDasharray={circumference}
        strokeDashoffset={offset}
        strokeLinecap="round"
        transform="rotate(-90 44 44)"
      />
      <text x={cx} y={cy} textAnchor="middle" dominantBaseline="central"
        style={{ fill: "#f8fafc", fontSize: 16, fontWeight: "bold" }}>
        {Math.round(score)}
      </text>
    </svg>
  )
}

function severityColor(s: string): string {
  if (s === "critique") return "#dc2626"
  if (s === "élevé") return "#f97316"
  if (s === "modéré") return "#eab308"
  return "#22c55e"
}

function severityBg(s: string): string {
  if (s === "critique") return "#450a0a"
  if (s === "élevé") return "#431407"
  if (s === "modéré") return "#422006"
  return "#052e16"
}

export default function ChildAgriculturalLaborPage() {
  const [data, setData] = useState<EngineData | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch(`/api/${DOMAIN_SLUG}`)
      .then(r => r.json())
      .then(d => { setData(d.payload ?? d); setLoading(false) })
      .catch(() => setLoading(false))
  }, [])

  if (loading) {
    return (
      <div style={{ minHeight: "100vh", background: "#0f172a", display: "flex", alignItems: "center", justifyContent: "center" }}>
        <div style={{ color: ACCENT, fontSize: 18, fontFamily: "system-ui, sans-serif" }}>Chargement...</div>
      </div>
    )
  }

  if (!data) {
    return (
      <div style={{ minHeight: "100vh", background: "#0f172a", display: "flex", alignItems: "center", justifyContent: "center" }}>
        <div style={{ color: "#ef4444", fontSize: 16, fontFamily: "system-ui, sans-serif" }}>Erreur de chargement des données.</div>
      </div>
    )
  }

  const EFFECTIVE_ACCENT = data.accent_color || ACCENT

  return (
    <main style={{ minHeight: "100vh", background: "#0f172a", color: "#f8fafc", padding: "2rem", fontFamily: "system-ui, sans-serif" }}>

      {/* Header */}
      <div style={{ marginBottom: "2rem" }}>
        <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 8 }}>
          <div style={{ width: 10, height: 10, borderRadius: "50%", background: EFFECTIVE_ACCENT }} />
          <span style={{ color: "#94a3b8", fontSize: 12, textTransform: "uppercase", letterSpacing: "0.08em" }}>
            Droits Humains — Wave {data.wave}
          </span>
        </div>
        <h1 style={{ fontSize: "1.75rem", fontWeight: "bold", color: EFFECTIVE_ACCENT, margin: 0, marginBottom: "0.5rem" }}>
          Travail Agricole Enfants
        </h1>
        <p style={{ color: "#94a3b8", fontSize: 14, margin: 0 }}>
          Wave {data.wave} · {data.summary.avg_composite.toFixed(2)} avg composite · {data.entities.length} entités analysées
        </p>
      </div>

      {/* Summary stats */}
      <div style={{ display: "flex", gap: "1rem", marginBottom: "2rem", flexWrap: "wrap" }}>
        {([
          ["Critique", data.summary.critique, "#dc2626", "#450a0a"],
          ["Élevé", data.summary.élevé, "#f97316", "#431407"],
          ["Modéré", data.summary.modéré, "#eab308", "#422006"],
          ["Faible", data.summary.faible, "#22c55e", "#052e16"],
        ] as [string, number, string, string][]).map(([label, count, color, bg]) => (
          <div key={label} style={{ background: bg, border: `1px solid ${color}40`, padding: "1rem 1.25rem", borderRadius: "0.75rem", textAlign: "center", minWidth: 90 }}>
            <div style={{ color, fontSize: "1.5rem", fontWeight: "bold" }}>{count}</div>
            <div style={{ color: "#94a3b8", fontSize: "0.75rem", marginTop: 2 }}>{label}</div>
          </div>
        ))}
        <div style={{ background: "#1e293b", border: `1px solid ${EFFECTIVE_ACCENT}40`, padding: "1rem 1.25rem", borderRadius: "0.75rem", textAlign: "center", minWidth: 110 }}>
          <div style={{ color: EFFECTIVE_ACCENT, fontSize: "1.5rem", fontWeight: "bold" }}>{data.summary.avg_composite.toFixed(1)}</div>
          <div style={{ color: "#94a3b8", fontSize: "0.75rem", marginTop: 2 }}>Score moyen</div>
        </div>
      </div>

      {/* Entity cards grid */}
      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(300px, 1fr))", gap: "1rem" }}>
        {data.entities.map(entity => {
          const sc = severityColor(entity.severity)
          const sb = severityBg(entity.severity)
          return (
            <div
              key={entity.id}
              style={{
                background: "#1e293b",
                borderRadius: "0.75rem",
                padding: "1.5rem",
                border: `1px solid ${sc}40`,
              }}
            >
              {/* Card header: gauge + name/country/badge */}
              <div style={{ display: "flex", alignItems: "center", gap: "1rem", marginBottom: "1rem" }}>
                <GaugeRing score={entity.composite_score} accent={sc} />
                <div style={{ flex: 1, minWidth: 0 }}>
                  <div style={{ fontWeight: "bold", fontSize: "1rem", color: "#f8fafc", marginBottom: 2, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
                    {entity.name}
                  </div>
                  <div style={{ color: "#94a3b8", fontSize: "0.75rem", marginBottom: 6 }}>{entity.country}</div>
                  <span style={{
                    background: sb,
                    color: sc,
                    border: `1px solid ${sc}60`,
                    padding: "0.15rem 0.5rem",
                    borderRadius: "1rem",
                    fontSize: "0.7rem",
                    fontWeight: "bold",
                    textTransform: "uppercase",
                  }}>
                    {entity.severity}
                  </span>
                </div>
              </div>

              {/* Key violation */}
              <div style={{ color: "#64748b", fontSize: "0.75rem", fontStyle: "italic", marginBottom: "0.75rem", lineHeight: 1.5 }}>
                {entity.key_violation}
              </div>

              {/* Index */}
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", paddingTop: "0.75rem", borderTop: "1px solid #334155" }}>
                <span style={{ fontSize: "0.75rem", color: "#64748b" }}>Index Travail Agricole</span>
                <span style={{ color: EFFECTIVE_ACCENT, fontWeight: "bold", fontSize: "1rem" }}>
                  {entity.estimated_child_agricultural_labor_index}
                </span>
              </div>
            </div>
          )
        })}
      </div>

      {/* Footer */}
      <div style={{ textAlign: "center", color: "#475569", fontSize: 12, paddingTop: 24, marginTop: 32, borderTop: "1px solid #1e293b" }}>
        Caelum Partners — Wave {data.wave} · Child Agricultural Labor Engine
      </div>
    </main>
  )
}
