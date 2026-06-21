"use client"

import { useEffect, useState } from "react"

interface Entity {
  id: string
  name: string
  composite_score: number
  risk_level: string
  estimated_torture_solitary_index: number
}

interface DomainData {
  domain: string
  generated_at: string
  entities: Entity[]
  avg_composite: number
  risk_distribution: Record<string, number>
}

const ACCENT = "#475569"

function GaugeRing({ score }: { score: number }) {
  const r = 36, cx = 44, cy = 44
  const circumference = 2 * Math.PI * r
  const filled = (score / 100) * circumference
  return (
    <svg viewBox="0 0 88 88" width={88} height={88}>
      <circle cx={cx} cy={cy} r={r} fill="none" stroke="#1e293b" strokeWidth={8} />
      <circle cx={cx} cy={cy} r={r} fill="none" stroke={ACCENT} strokeWidth={8}
        strokeDasharray={`${filled} ${circumference - filled}`}
        transform="rotate(-90 44 44)" strokeLinecap="round" />
      <text x={cx} y={cy + 5} textAnchor="middle" fill="#f1f5f9" fontSize={14} fontWeight="bold">
        {score.toFixed(0)}
      </text>
    </svg>
  )
}

function RiskBadge({ level }: { level: string }) {
  const colors: Record<string, string> = { critique: "#ef4444", "élevé": "#f97316", modéré: "#eab308", faible: "#22c55e" }
  return (
    <span style={{ background: colors[level] ?? "#64748b", color: "#fff", borderRadius: 6, padding: "2px 10px", fontSize: 11, fontWeight: 700, textTransform: "uppercase", letterSpacing: 0.5, whiteSpace: "nowrap" }}>
      {level}
    </span>
  )
}

export default function SolitaryConfinementTortureMethodsPage() {
  const [data, setData] = useState<DomainData | null>(null)

  useEffect(() => {
    fetch("/api/solitary-confinement-torture-methods-engine")
      .then((r) => r.json())
      .then((d) => setData(d.payload ?? d))
  }, [])

  if (!data) return (
    <div style={{ background: "#0f172a", minHeight: "100vh", display: "flex", alignItems: "center", justifyContent: "center" }}>
      <div style={{ color: "#94a3b8", fontSize: 18 }}>Chargement...</div>
    </div>
  )

  return (
    <div style={{ background: "#0f172a", minHeight: "100vh", padding: "32px 24px", fontFamily: "system-ui, sans-serif" }}>
      <div style={{ maxWidth: 1100, margin: "0 auto", marginBottom: 32 }}>
        <div style={{ display: "flex", alignItems: "center", gap: 16 }}>
          <div style={{ background: ACCENT, borderRadius: 12, padding: 12, flexShrink: 0 }}>
            <svg width={28} height={28} viewBox="0 0 24 24" fill="none" stroke="#fff" strokeWidth={2}>
              <rect x="3" y="3" width="18" height="18" rx="2" />
              <path d="M9 3v18" />
              <path d="M9 12h12" />
            </svg>
          </div>
          <div>
            <h1 style={{ margin: 0, fontSize: 24, fontWeight: 800, color: "#f1f5f9" }}>Isolement Cellulaire &amp; Méthodes de Torture</h1>
            <p style={{ margin: 0, color: "#94a3b8", fontSize: 14 }}>Wave 180 — Indice mondial des droits humains · Caelum Partners</p>
          </div>
        </div>
        <div style={{ display: "flex", gap: 20, marginTop: 28, flexWrap: "wrap" }}>
          {[
            { label: "Score moyen", value: data.avg_composite.toFixed(2) },
            { label: "Critique", value: data.risk_distribution["critique"] ?? 0, color: "#ef4444" },
            { label: "Élevé", value: data.risk_distribution["élevé"] ?? 0, color: "#f97316" },
            { label: "Modéré", value: data.risk_distribution["modéré"] ?? 0, color: "#eab308" },
            { label: "Faible", value: data.risk_distribution["faible"] ?? 0, color: "#22c55e" },
          ].map((s) => (
            <div key={s.label} style={{ background: "#1e293b", borderRadius: 10, padding: "14px 22px", minWidth: 110, borderTop: `3px solid ${s.color ?? ACCENT}` }}>
              <div style={{ fontSize: 22, fontWeight: 700, color: s.color ?? ACCENT }}>{s.value}</div>
              <div style={{ fontSize: 12, color: "#94a3b8", marginTop: 2 }}>{s.label}</div>
            </div>
          ))}
        </div>
      </div>
      <div style={{ maxWidth: 1100, margin: "0 auto", display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(480px, 1fr))", gap: 20 }}>
        {data.entities.map((entity) => (
          <div key={entity.id} style={{ background: "#1e293b", borderRadius: 12, padding: 22, display: "flex", gap: 20, alignItems: "flex-start", borderLeft: `4px solid ${ACCENT}` }}>
            <div style={{ flexShrink: 0 }}><GaugeRing score={entity.composite_score} /></div>
            <div style={{ flex: 1, minWidth: 0 }}>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 8, gap: 8 }}>
                <span style={{ color: ACCENT, fontSize: 11, fontWeight: 700, letterSpacing: 1 }}>{entity.id}</span>
                <RiskBadge level={entity.risk_level} />
              </div>
              <p style={{ margin: "0 0 10px", fontSize: 13, color: "#cbd5e1", lineHeight: 1.5 }}>{entity.name}</p>
              <div style={{ display: "flex", gap: 16 }}>
                <div>
                  <div style={{ fontSize: 18, fontWeight: 700, color: ACCENT }}>{entity.estimated_torture_solitary_index.toFixed(2)}</div>
                  <div style={{ fontSize: 11, color: "#64748b" }}>Indice torture/isolement</div>
                </div>
                <div>
                  <div style={{ fontSize: 18, fontWeight: 700, color: "#f1f5f9" }}>{entity.composite_score.toFixed(2)}</div>
                  <div style={{ fontSize: 11, color: "#64748b" }}>Score composite</div>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
      <div style={{ maxWidth: 1100, margin: "40px auto 0", textAlign: "center", color: "#334155", fontSize: 12 }}>
        Dernière mise à jour : {new Date(data.generated_at).toLocaleString("fr-FR")} · Caelum Partners Wave 180
      </div>
    </div>
  )
}
