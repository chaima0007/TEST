"use client"
import { useEffect, useState } from "react"

const ACCENT = "#7c3aed"
const DOMAIN = "corporate-impunity-legal-gap-engine"

type Entity = {
  id: string; name: string; composite_score: number; risk_level: string
  corporate_liability_evasion_score: number
  victim_access_justice_barrier_score: number
  extraterritorial_jurisdiction_gap_score: number
  enforcement_capacity_deficit_score: number
  estimated_corporate_impunity_legal_gap_index: number
}
type Payload = { domain: string; generated_at: string; entities: Entity[]; avg_composite: number; risk_distribution: Record<string, number> }

function GaugeRing({ value, color }: { value: number; color: string }) {
  const r = 36, cx = 44, cy = 44, circ = 2 * Math.PI * r, pct = Math.min(Math.max(value, 0), 100) / 100
  return (
    <svg viewBox="0 0 88 88" width={88} height={88}>
      <circle cx={cx} cy={cy} r={r} fill="none" stroke="#1e293b" strokeWidth={8} />
      <circle cx={cx} cy={cy} r={r} fill="none" stroke={color} strokeWidth={8} strokeDasharray={`${pct * circ} ${circ}`} strokeLinecap="round" transform={`rotate(-90 ${cx} ${cy})`} />
      <text x={cx} y={cy + 5} textAnchor="middle" fontSize={14} fontWeight={700} fill={color}>{Math.round(value)}</text>
    </svg>
  )
}
function riskColor(l: string) { return l === "critique" ? "#ef4444" : l === "élevé" ? "#f97316" : l === "modéré" ? "#f59e0b" : "#10b981" }
function riskBg(l: string) { return l === "critique" ? { background: "#450a0a", color: "#fca5a5" } : l === "élevé" ? { background: "#431407", color: "#fdba74" } : l === "modéré" ? { background: "#451a03", color: "#fcd34d" } : { background: "#052e16", color: "#86efac" } }

export default function CorporateImpunityLegalGapDashboard() {
  const [data, setData] = useState<Payload | null>(null)
  const [loading, setLoading] = useState(true)
  const [selected, setSelected] = useState<Entity | null>(null)
  useEffect(() => { fetch(`/api/${DOMAIN}`).then(r => r.json()).then(d => { setData(d.payload ?? d); setLoading(false) }).catch(() => setLoading(false)) }, [])
  if (loading) return <div style={{ minHeight: "100vh", background: "#0f172a", display: "flex", alignItems: "center", justifyContent: "center" }}><div style={{ color: ACCENT, fontSize: 18 }}>Chargement...</div></div>
  if (!data) return <div style={{ minHeight: "100vh", background: "#0f172a", display: "flex", alignItems: "center", justifyContent: "center" }}><div style={{ color: "#ef4444", fontSize: 16 }}>Erreur de chargement.</div></div>
  const dist = data.risk_distribution ?? {}
  return (
    <div style={{ minHeight: "100vh", background: "#0f172a", color: "#f1f5f9", fontFamily: "system-ui, sans-serif", padding: "32px 24px" }}>
      <div style={{ marginBottom: 32 }}>
        <div style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 8 }}>
          <div style={{ width: 12, height: 12, borderRadius: "50%", background: ACCENT }} />
          <span style={{ color: "#94a3b8", fontSize: 13, letterSpacing: "0.08em", textTransform: "uppercase" }}>Impunité Corporative &amp; Lacunes Juridiques — Wave 194</span>
        </div>
        <h1 style={{ fontSize: 28, fontWeight: 700, color: "#f8fafc", margin: 0 }}>Impunit&eacute; Corporative &amp; Gap Juridique</h1>
        <p style={{ color: "#94a3b8", fontSize: 14, marginTop: 6 }}>Analyse des obstacles à la responsabilité juridique des entreprises pour violations droits humains — {data.entities.length} entités</p>
      </div>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))", gap: 16, marginBottom: 32 }}>
        {[["Score Moyen", data.avg_composite.toFixed(2), ACCENT], ["Critique", dist.critique ?? 0, "#ef4444"], ["Élevé", dist["élevé"] ?? 0, "#f97316"], ["Modéré/Faible", (dist.modéré ?? 0) + (dist.faible ?? 0), "#f59e0b"]].map(([label, val, color]) => (
          <div key={label as string} style={{ background: "#1e293b", borderRadius: 12, padding: "20px 24px", borderLeft: `4px solid ${color}` }}>
            <div style={{ color: "#94a3b8", fontSize: 12, textTransform: "uppercase", letterSpacing: "0.1em" }}>{label}</div>
            <div style={{ fontSize: 32, fontWeight: 700, color: color as string, marginTop: 4 }}>{val}</div>
          </div>
        ))}
      </div>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(340px, 1fr))", gap: 20, marginBottom: 32 }}>
        {data.entities.map(entity => (
          <div key={entity.id} onClick={() => setSelected(entity)} style={{ background: "#1e293b", borderRadius: 12, padding: 20, cursor: "pointer", border: "1px solid #334155" }} onMouseEnter={e => (e.currentTarget.style.borderColor = ACCENT)} onMouseLeave={e => (e.currentTarget.style.borderColor = "#334155")}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 16 }}>
              <div><div style={{ fontSize: 11, color: "#64748b", marginBottom: 4 }}>{entity.id}</div><div style={{ fontSize: 15, fontWeight: 600, color: "#f1f5f9", lineHeight: 1.3 }}>{entity.name}</div></div>
              <span style={{ ...riskBg(entity.risk_level), padding: "3px 10px", borderRadius: 20, fontSize: 11, fontWeight: 600, whiteSpace: "nowrap", marginLeft: 8 }}>{entity.risk_level}</span>
            </div>
            <div style={{ display: "flex", gap: 12, alignItems: "center" }}>
              <GaugeRing value={entity.composite_score} color={riskColor(entity.risk_level)} />
              <div style={{ flex: 1 }}>
                <div style={{ fontSize: 11, color: "#64748b", marginBottom: 8 }}>Sous-scores</div>
                {[["Évasion Responsabilité", entity.corporate_liability_evasion_score], ["Accès Justice Victimes", entity.victim_access_justice_barrier_score], ["Juridiction Extraterrit.", entity.extraterritorial_jurisdiction_gap_score], ["Capacité Enforcement", entity.enforcement_capacity_deficit_score]].map(([label, val]) => (
                  <div key={label as string} style={{ marginBottom: 5 }}>
                    <div style={{ display: "flex", justifyContent: "space-between", fontSize: 11, color: "#94a3b8", marginBottom: 2 }}><span>{label}</span><span>{val}</span></div>
                    <div style={{ height: 4, background: "#0f172a", borderRadius: 2 }}><div style={{ height: 4, borderRadius: 2, background: ACCENT, width: `${val as number}%` }} /></div>
                  </div>
                ))}
              </div>
            </div>
            <div style={{ marginTop: 12, paddingTop: 12, borderTop: "1px solid #334155", display: "flex", justifyContent: "space-between", alignItems: "center" }}>
              <span style={{ fontSize: 11, color: "#64748b" }}>Index Impunité Corporative</span>
              <span style={{ fontSize: 16, fontWeight: 700, color: ACCENT }}>{entity.estimated_corporate_impunity_legal_gap_index.toFixed(2)}</span>
            </div>
          </div>
        ))}
      </div>
      <div style={{ textAlign: "center", color: "#475569", fontSize: 12, paddingTop: 16, borderTop: "1px solid #1e293b" }}>Caelum Partners — Wave 194 · Corporate Impunity Legal Gap Engine · {new Date(data.generated_at).toLocaleDateString("fr-FR")}</div>
      {selected && (
        <div style={{ position: "fixed", inset: 0, background: "rgba(0,0,0,0.75)", zIndex: 50, display: "flex", alignItems: "center", justifyContent: "center" }} onClick={() => setSelected(null)}>
          <div style={{ background: "#1e293b", borderRadius: 16, padding: 32, maxWidth: 480, width: "90%", border: "1px solid #475569" }} onClick={e => e.stopPropagation()}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 20 }}>
              <div><div style={{ fontSize: 11, color: "#64748b", marginBottom: 4 }}>{selected.id}</div><h2 style={{ fontSize: 18, fontWeight: 700, color: "#f8fafc", margin: 0 }}>{selected.name}</h2></div>
              <button onClick={() => setSelected(null)} style={{ background: "none", border: "none", color: "#94a3b8", fontSize: 22, cursor: "pointer", lineHeight: 1 }}>×</button>
            </div>
            <div style={{ display: "flex", justifyContent: "center", marginBottom: 20 }}><GaugeRing value={selected.composite_score} color={riskColor(selected.risk_level)} /></div>
            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12, marginBottom: 20 }}>
              {[["Évasion Responsabilité", selected.corporate_liability_evasion_score], ["Accès Justice Victimes", selected.victim_access_justice_barrier_score], ["Juridiction Extraterrit.", selected.extraterritorial_jurisdiction_gap_score], ["Capacité Enforcement", selected.enforcement_capacity_deficit_score]].map(([label, val]) => (
                <div key={label as string} style={{ background: "#0f172a", borderRadius: 8, padding: "12px 16px" }}><div style={{ fontSize: 11, color: "#64748b", marginBottom: 4 }}>{label}</div><div style={{ fontSize: 22, fontWeight: 700, color: ACCENT }}>{val}</div></div>
              ))}
            </div>
            <div style={{ background: "#0f172a", borderRadius: 8, padding: "12px 16px", display: "flex", justifyContent: "space-between", alignItems: "center" }}>
              <span style={{ fontSize: 13, color: "#94a3b8" }}>Index Impunité Corporative</span>
              <span style={{ fontSize: 20, fontWeight: 700, color: ACCENT }}>{selected.estimated_corporate_impunity_legal_gap_index.toFixed(2)}</span>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
