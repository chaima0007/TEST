"use client"
import { useEffect, useState } from "react"

const ACCENT = "#d97706"
const RC: Record<string, string> = { critique: "#f87171", "élevé": "#fb923c", modéré: "#facc15", faible: "#34d399" }

interface Entity {
  id: string
  name: string
  country: string
  composite_score: number
  segregation_exclusion_score: number
  eviction_displacement_score: number
  anti_ziganism_state_complicity_score: number
  rights_protection_enforcement_deficit_score: number
  estimated_romani_rights_index: number
  risk_level: string
  primary_pattern: string
  last_updated: string
}

interface DomainData {
  domain: string
  generated_at: string
  entities: Entity[]
  avg_composite: number
  risk_distribution: Record<string, number>
  confidence_score?: number
  avg_estimated_romani_rights_index?: number
  data_sources?: string[]
}

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

function EntityCard({ entity, onClick }: { entity: Entity; onClick: () => void }) {
  return (
    <div onClick={onClick} style={{ background: "#0f172a", border: `1px solid ${RC[entity.risk_level]}33`, borderRadius: 12, padding: 16, cursor: "pointer" }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", gap: 12 }}>
        <div style={{ flex: 1 }}>
          <div style={{ fontWeight: 600, color: "#f1f5f9", fontSize: 14, marginBottom: 4 }}>{entity.name}</div>
          <div style={{ fontSize: 12, color: "#94a3b8", marginBottom: 6 }}>{entity.country}</div>
          <div style={{ fontSize: 11, color: "#64748b", lineHeight: 1.5 }}>{entity.primary_pattern}</div>
        </div>
        <div style={{ textAlign: "center", flexShrink: 0 }}>
          <GaugeRing score={entity.composite_score} />
          <div style={{ fontSize: 11, color: RC[entity.risk_level] ?? "#94a3b8", fontWeight: 600, marginTop: 4, textTransform: "uppercase" }}>{entity.risk_level}</div>
        </div>
      </div>
      <div style={{ marginTop: 10, display: "flex", gap: 8, flexWrap: "wrap" }}>
        <div style={{ background: "#1e293b", borderRadius: 6, padding: "4px 8px", fontSize: 11, color: "#94a3b8" }}>
          Index: <span style={{ color: ACCENT, fontWeight: 700 }}>{entity.estimated_romani_rights_index.toFixed(2)}</span>
        </div>
        <div style={{ background: "#1e293b", borderRadius: 6, padding: "4px 8px", fontSize: 11, color: "#94a3b8" }}>
          MàJ: {entity.last_updated}
        </div>
      </div>
    </div>
  )
}

function Modal({ entity, onClose }: { entity: Entity; onClose: () => void }) {
  const [tab, setTab] = useState<"apercu" | "metriques">("apercu")
  const subScores = [
    { label: "Ségrégation & Exclusion", value: entity.segregation_exclusion_score, weight: "0.30" },
    { label: "Expulsions & Déplacements", value: entity.eviction_displacement_score, weight: "0.25" },
    { label: "Anti-Tziganisme & Complicité État", value: entity.anti_ziganism_state_complicity_score, weight: "0.25" },
    { label: "Déficit Protection Droits", value: entity.rights_protection_enforcement_deficit_score, weight: "0.20" },
  ]
  return (
    <div style={{ position: "fixed", inset: 0, zIndex: 50, display: "flex", alignItems: "center", justifyContent: "center", background: "rgba(0,0,0,0.7)", backdropFilter: "blur(4px)", padding: 16 }} onClick={onClose}>
      <div style={{ background: "#0f172a", border: "1px solid #334155", borderRadius: 16, width: "100%", maxWidth: 640, maxHeight: "90vh", overflowY: "auto", boxShadow: "0 25px 50px rgba(0,0,0,0.5)" }} onClick={e => e.stopPropagation()}>
        <div style={{ padding: 24, borderBottom: "1px solid #1e293b", display: "flex", justifyContent: "space-between", alignItems: "flex-start" }}>
          <div>
            <h2 style={{ fontSize: 18, fontWeight: 700, color: "#f1f5f9", marginBottom: 4 }}>{entity.name}</h2>
            <p style={{ fontSize: 13, color: "#94a3b8" }}>{entity.country}</p>
            <span style={{ fontSize: 11, fontWeight: 700, textTransform: "uppercase", color: RC[entity.risk_level] ?? "#94a3b8", marginTop: 4, display: "inline-block" }}>{entity.risk_level}</span>
          </div>
          <button onClick={onClose} style={{ color: "#94a3b8", background: "none", border: "none", fontSize: 24, cursor: "pointer", lineHeight: 1 }}>&times;</button>
        </div>
        <div style={{ display: "flex", borderBottom: "1px solid #1e293b" }}>
          {(["apercu", "metriques"] as const).map(t => (
            <button key={t} onClick={() => setTab(t)} style={{ flex: 1, padding: "12px 0", fontSize: 13, fontWeight: 500, background: "none", border: "none", borderBottom: tab === t ? `2px solid ${ACCENT}` : "2px solid transparent", color: tab === t ? ACCENT : "#64748b", cursor: "pointer" }}>
              {t === "apercu" ? "Aperçu" : "Métriques"}
            </button>
          ))}
        </div>
        <div style={{ padding: 24 }}>
          {tab === "apercu" && (
            <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12 }}>
                <div style={{ background: "#1e293b", borderRadius: 12, padding: 16, textAlign: "center" }}>
                  <div style={{ fontSize: 28, fontWeight: 700, color: ACCENT }}>{entity.composite_score.toFixed(1)}</div>
                  <div style={{ fontSize: 11, color: "#64748b", marginTop: 4 }}>Score Composite</div>
                </div>
                <div style={{ background: "#1e293b", borderRadius: 12, padding: 16, textAlign: "center" }}>
                  <div style={{ fontSize: 28, fontWeight: 700, color: ACCENT }}>{entity.estimated_romani_rights_index.toFixed(2)}</div>
                  <div style={{ fontSize: 11, color: "#64748b", marginTop: 4 }}>Index Droits Roms</div>
                </div>
              </div>
              <div style={{ background: "#1e293b", borderRadius: 12, padding: 16 }}>
                <div style={{ fontSize: 12, color: "#94a3b8", marginBottom: 8, fontWeight: 600 }}>Patterns Documentés</div>
                <p style={{ fontSize: 13, color: "#cbd5e1", lineHeight: 1.6 }}>{entity.primary_pattern}</p>
              </div>
            </div>
          )}
          {tab === "metriques" && (
            <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
              {subScores.map(s => (
                <div key={s.label} style={{ background: "#1e293b", borderRadius: 10, padding: 14 }}>
                  <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 8 }}>
                    <span style={{ fontSize: 12, color: "#94a3b8" }}>{s.label}</span>
                    <span style={{ fontSize: 12, color: "#64748b" }}>poids {s.weight}</span>
                  </div>
                  <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
                    <div style={{ flex: 1, background: "#0f172a", borderRadius: 4, height: 6, overflow: "hidden" }}>
                      <div style={{ width: `${s.value}%`, background: ACCENT, height: "100%", borderRadius: 4 }} />
                    </div>
                    <span style={{ fontSize: 13, fontWeight: 700, color: ACCENT, minWidth: 36, textAlign: "right" }}>{s.value.toFixed(0)}</span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default function RomaniSintiAntiZiganismPage() {
  const [data, setData] = useState<DomainData | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [selected, setSelected] = useState<Entity | null>(null)

  useEffect(() => {
    fetch("/api/romani-sinti-anti-ziganism-rights-engine")
      .then(r => r.json())
      .then(d => { setData(d.payload ?? d); setLoading(false) })
      .catch(() => { setError("Erreur de chargement"); setLoading(false) })
  }, [])

  if (loading) return (
    <div style={{ minHeight: "100vh", background: "#020617", display: "flex", alignItems: "center", justifyContent: "center" }}>
      <div style={{ color: ACCENT, fontSize: 18 }}>Chargement...</div>
    </div>
  )
  if (error || !data) return (
    <div style={{ minHeight: "100vh", background: "#020617", display: "flex", alignItems: "center", justifyContent: "center" }}>
      <div style={{ color: "#f87171", fontSize: 18 }}>{error ?? "Données indisponibles"}</div>
    </div>
  )

  const critiques = data.entities?.filter(e => e.risk_level === "critique") ?? []
  const autres = data.entities?.filter(e => e.risk_level !== "critique") ?? []

  return (
    <div style={{ minHeight: "100vh", background: "#020617", color: "#f1f5f9", fontFamily: "system-ui, sans-serif" }}>
      <div style={{ maxWidth: 1200, margin: "0 auto", padding: "32px 16px" }}>
        {/* Header */}
        <div style={{ marginBottom: 32 }}>
          <div style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 12 }}>
            <div style={{ width: 4, height: 40, background: ACCENT, borderRadius: 2 }} />
            <div>
              <h1 style={{ fontSize: 28, fontWeight: 800, color: "#f1f5f9", margin: 0 }}>Droits Roms/Sinti & Anti-Tziganisme</h1>
              <p style={{ fontSize: 14, color: "#64748b", margin: 0, marginTop: 4 }}>Wave 184 — Surveillance discrimination systémique, ségrégation et anti-ziganism en Europe</p>
            </div>
          </div>
        </div>

        {/* Stats */}
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))", gap: 16, marginBottom: 32 }}>
          {[
            { label: "Score Moyen", value: data.avg_composite?.toFixed(2) ?? "—" },
            { label: "Entités Surveillées", value: data.entities?.length ?? 0 },
            { label: "Critique", value: data.risk_distribution?.critique ?? 0 },
            { label: "Élevé", value: data.risk_distribution?.["élevé"] ?? 0 },
            { label: "Modéré", value: data.risk_distribution?.modéré ?? 0 },
            { label: "Faible", value: data.risk_distribution?.faible ?? 0 },
          ].map(s => (
            <div key={s.label} style={{ background: "#0f172a", border: "1px solid #1e293b", borderRadius: 12, padding: 16, textAlign: "center" }}>
              <div style={{ fontSize: 24, fontWeight: 700, color: ACCENT }}>{s.value}</div>
              <div style={{ fontSize: 12, color: "#64748b", marginTop: 4 }}>{s.label}</div>
            </div>
          ))}
        </div>

        {/* Critique section */}
        {critiques.length > 0 && (
          <div style={{ marginBottom: 32 }}>
            <h2 style={{ fontSize: 16, fontWeight: 700, color: "#f87171", marginBottom: 16, textTransform: "uppercase", letterSpacing: "0.05em" }}>Niveau Critique</h2>
            <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(340px, 1fr))", gap: 16 }}>
              {critiques.map(e => <EntityCard key={e.id} entity={e} onClick={() => setSelected(e)} />)}
            </div>
          </div>
        )}

        {/* Others */}
        {autres.length > 0 && (
          <div style={{ marginBottom: 32 }}>
            <h2 style={{ fontSize: 16, fontWeight: 700, color: "#94a3b8", marginBottom: 16, textTransform: "uppercase", letterSpacing: "0.05em" }}>Autres Niveaux</h2>
            <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(340px, 1fr))", gap: 16 }}>
              {autres.map(e => <EntityCard key={e.id} entity={e} onClick={() => setSelected(e)} />)}
            </div>
          </div>
        )}

        {/* Footer */}
        <div style={{ borderTop: "1px solid #1e293b", paddingTop: 16, display: "flex", justifyContent: "space-between", alignItems: "center", flexWrap: "wrap", gap: 8 }}>
          <span style={{ fontSize: 12, color: "#475569" }}>Caelum Partners — Wave 184 — Droits Roms/Sinti & Anti-Tziganisme</span>
          <span style={{ fontSize: 12, color: "#475569" }}>Confiance: {((data.confidence_score ?? 0) * 100).toFixed(0)}%</span>
        </div>
      </div>

      {selected && <Modal entity={selected} onClose={() => setSelected(null)} />}
    </div>
  )
}
