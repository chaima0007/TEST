"use client"
import { useEffect, useState } from "react"

const ACCENT = "#be185d"
const DOMAIN_SLUG = "gender-pay-gap-discrimination-engine"

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
  wave: number
  accent_color: string
  entities: Entity[]
  summary: Summary
}

const FALLBACK: EngineData = {
  engine: "GPG_ENGINE",
  wave: 198,
  accent_color: ACCENT,
  entities: [
    { id: "GPG_001", name: "Amazon", country: "US", composite_score: 88.2, severity: "critique", key_violation: "Écart salarial systémique — entrepôts vs sièges sociaux" },
    { id: "GPG_002", name: "Walmart", country: "US", composite_score: 85.0, severity: "critique", key_violation: "Discrimination salariale caissières vs managers masculins" },
    { id: "GPG_003", name: "Goldman Sachs", country: "US", composite_score: 82.5, severity: "critique", key_violation: "Finance — gap 30% pour postes équivalents" },
    { id: "GPG_004", name: "Apple", country: "US", composite_score: 78.9, severity: "critique", key_violation: "Tech — sous-représentation féminine & écart bonification" },
    { id: "GPG_005", name: "Microsoft", country: "US", composite_score: 57.2, severity: "élevé", key_violation: "Promotions biaisées — pipeline leadership féminin insuffisant" },
    { id: "GPG_006", name: "Google", country: "US", composite_score: 53.8, severity: "élevé", key_violation: "Procès collectifs internes — disparités rémunération variables" },
    { id: "GPG_007", name: "Salesforce", country: "US", composite_score: 29.4, severity: "modéré", key_violation: "Audits salariaux engagés — progrès partiels constatés" },
    { id: "GPG_008", name: "Buffer", country: "US", composite_score: 12.1, severity: "faible", key_violation: "Transparence salariale totale — meilleure pratique sectorielle" },
  ],
  summary: { avg_composite: 61.0, critique: 4, élevé: 2, modéré: 1, faible: 1 },
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

export default function GenderPayGapDiscriminationPage() {
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
  const EFFECTIVE_ACCENT = d.accent_color || ACCENT

  return (
    <main style={{ minHeight: "100vh", background: "#0f172a", color: "#f8fafc", padding: "2rem", fontFamily: "system-ui, sans-serif" }}>

      {/* Header */}
      <div style={{ marginBottom: "2rem" }}>
        <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 8 }}>
          <div style={{ width: 10, height: 10, borderRadius: "50%", background: EFFECTIVE_ACCENT }} />
          <span style={{ color: "#94a3b8", fontSize: 12, textTransform: "uppercase", letterSpacing: "0.08em" }}>
            Droits Humains — Wave {d.wave}
          </span>
        </div>
        <h1 style={{ fontSize: "1.75rem", fontWeight: "bold", color: EFFECTIVE_ACCENT, margin: 0, marginBottom: "0.5rem" }}>
          Discrimination Salariale de Genre
        </h1>
        <p style={{ color: "#94a3b8", fontSize: 14, margin: 0 }}>
          Wave {d.wave} · {d.summary.avg_composite.toFixed(2)} avg composite · {d.entities.length} entités analysées
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
        <div style={{ background: "#1e293b", border: `1px solid ${EFFECTIVE_ACCENT}40`, padding: "1rem 1.25rem", borderRadius: "0.75rem", textAlign: "center", minWidth: 110 }}>
          <div style={{ color: EFFECTIVE_ACCENT, fontSize: "1.5rem", fontWeight: "bold" }}>{d.summary.avg_composite.toFixed(1)}</div>
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
                <span style={{ fontSize: "0.75rem", color: "#64748b" }}>Score Discrimination</span>
                <span style={{ color: EFFECTIVE_ACCENT, fontWeight: "bold", fontSize: "1rem" }}>
                  {entity.composite_score.toFixed(1)}
                </span>
              </div>
            </div>
          )
        })}
      </div>

      {/* Footer */}
      <div style={{ textAlign: "center", color: "#475569", fontSize: 12, paddingTop: 24, marginTop: 32, borderTop: "1px solid #1e293b" }}>
        Caelum Partners — Wave {d.wave} · Gender Pay Gap Discrimination Engine
      </div>
    </main>
  )
}
