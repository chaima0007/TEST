"use client"
import { useEffect, useState } from "react"

const ACCENT = "#365314"
const DOMAIN_SLUG = "land-grabbing-agribusiness-engine"

type Entity = {
  id: string
  name: string
  country: string
  composite_score: number
  severity: string
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
  entities: Entity[]
  summary: Summary
}

const FALLBACK: EngineData = {
  engine: "LGA_ENGINE",
  entities: [
    { id: "LGA_001", name: "Cargill", country: "US", composite_score: 89.2, severity: "critique", key_violation: "Accaparement terres à grande échelle — déplacements forcés communautés paysannes Amérique Latine" },
    { id: "LGA_002", name: "ADM", country: "US", composite_score: 85.5, severity: "critique", key_violation: "Expansions soja/maïs — destruction forêts et expulsions populations autochtones" },
    { id: "LGA_003", name: "Bunge", country: "US", composite_score: 81.3, severity: "critique", key_violation: "Chaîne d&apos;approvisionnement liée à déforestation et violations droits fonciers" },
    { id: "LGA_004", name: "Louis Dreyfus", country: "NL", composite_score: 76.4, severity: "critique", key_violation: "Acquisition terres agricoles sans consentement préalable des communautés locales" },
    { id: "LGA_005", name: "Olam", country: "SG", composite_score: 57.8, severity: "élevé", key_violation: "Plantations Afrique — conditions travail précaires, restrictions liberté de mouvement" },
    { id: "LGA_006", name: "Wilmar", country: "SG", composite_score: 53.2, severity: "élevé", key_violation: "Huile de palme — conflits fonciers documentés malgré certifications RSPO" },
    { id: "LGA_007", name: "Danone", country: "FR", composite_score: 29.1, severity: "modéré", key_violation: "Politiques d&apos;approvisionnement partiellement améliorées — progrès insuffisants sur foncier" },
    { id: "LGA_008", name: "Rainforest Alliance", country: "US", composite_score: 11.4, severity: "faible", key_violation: "Certification rigoureuse — standards fonciers et droits communautaires vérifiables" },
  ],
  summary: { avg_composite: 60.49, critique: 4, élevé: 2, modéré: 1, faible: 1 },
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

export default function LandGrabbingAgribusinessPage() {
  const [data, setData] = useState<EngineData | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch(`/api/${DOMAIN_SLUG}`)
      .then(r => r.json())
      .then(d => { setData(d.payload ?? d); setLoading(false) })
      .catch(() => { setData(FALLBACK); setLoading(false) })
  }, [])

  if (loading) {
    return (
      <div style={{ minHeight: "100vh", background: "#0f172a", display: "flex", alignItems: "center", justifyContent: "center" }}>
        <div style={{ color: ACCENT, fontSize: 18, fontFamily: "system-ui, sans-serif" }}>Chargement...</div>
      </div>
    )
  }

  const d = data ?? FALLBACK

  return (
    <main style={{ minHeight: "100vh", background: "#0f172a", color: "#f8fafc", padding: "2rem", fontFamily: "system-ui, sans-serif" }}>

      {/* Header */}
      <div style={{ marginBottom: "2rem" }}>
        <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 8 }}>
          <div style={{ width: 10, height: 10, borderRadius: "50%", background: ACCENT }} />
          <span style={{ color: "#94a3b8", fontSize: 12, textTransform: "uppercase", letterSpacing: "0.08em" }}>
            Droits Humains — Wave 202
          </span>
        </div>
        <h1 style={{ fontSize: "1.75rem", fontWeight: "bold", color: ACCENT, margin: 0, marginBottom: "0.5rem" }}>
          Accaparement Terres Agricoles
        </h1>
        <p style={{ color: "#94a3b8", fontSize: 14, margin: 0 }}>
          Wave 202 · {d.summary.avg_composite.toFixed(2)} avg composite · {d.entities.length} entités analysées
        </p>
      </div>

      {/* Summary stats */}
      <div style={{ display: "flex", gap: "1rem", marginBottom: "2rem", flexWrap: "wrap" }}>
        {([
          ["Critique", d.summary.critique, "#dc2626", "#450a0a"],
          ["Élevé", d.summary.élevé, "#f97316", "#431407"],
          ["Modéré", d.summary.modéré, "#eab308", "#422006"],
          ["Faible", d.summary.faible, "#22c55e", "#052e16"],
        ] as [string, number, string, string][]).map(([label, count, color, bg]) => (
          <div key={label} style={{ background: bg, border: `1px solid ${color}40`, padding: "1rem 1.25rem", borderRadius: "0.75rem", textAlign: "center", minWidth: 90 }}>
            <div style={{ color, fontSize: "1.5rem", fontWeight: "bold" }}>{count}</div>
            <div style={{ color: "#94a3b8", fontSize: "0.75rem", marginTop: 2 }}>{label}</div>
          </div>
        ))}
        <div style={{ background: "#1e293b", border: `1px solid ${ACCENT}40`, padding: "1rem 1.25rem", borderRadius: "0.75rem", textAlign: "center", minWidth: 110 }}>
          <div style={{ color: ACCENT, fontSize: "1.5rem", fontWeight: "bold" }}>{d.summary.avg_composite.toFixed(1)}</div>
          <div style={{ color: "#94a3b8", fontSize: "0.75rem", marginTop: 2 }}>Score moyen</div>
        </div>
      </div>

      {/* Entity cards grid */}
      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(300px, 1fr))", gap: "1rem" }}>
        {d.entities.map(entity => {
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

              <div style={{ color: "#64748b", fontSize: "0.75rem", fontStyle: "italic", marginBottom: "0.75rem", lineHeight: 1.5 }}>
                {entity.key_violation}
              </div>

              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", paddingTop: "0.75rem", borderTop: "1px solid #334155" }}>
                <span style={{ fontSize: "0.75rem", color: "#64748b" }}>Score Violation</span>
                <span style={{ color: ACCENT, fontWeight: "bold", fontSize: "1rem" }}>
                  {entity.composite_score.toFixed(1)}
                </span>
              </div>
            </div>
          )
        })}
      </div>

      {/* Footer */}
      <div style={{ textAlign: "center", color: "#475569", fontSize: 12, paddingTop: 24, marginTop: 32, borderTop: "1px solid #1e293b" }}>
        CaelumSwarm™ — LGA Engine · Wave 202
      </div>
    </main>
  )
}
