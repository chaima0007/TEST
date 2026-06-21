"use client"

import { useState } from "react"
import Link from "next/link"

// Données simulées pour la démo
const DEMO_COMPANIES = {
  default: {
    name: "Entreprise Exemple",
    sector: "Industrie Manufacturière",
    employees: "5 000+",
    score: 67,
    risk_level: "élevé",
    risks: [
      { area: "Chaîne d'approvisionnement", score: 72, issues: ["Fournisseurs niveau 2 non audités", "3 pays à risque identifiés"] },
      { area: "Droits du travail", score: 61, issues: ["Heures supplémentaires non conformes", "Absence de canal de signalement"] },
      { area: "Environnement", score: 58, issues: ["Déforestation fournisseurs", "Émissions non tracées"] },
      { area: "Gouvernance", score: 78, issues: ["Politique due diligence incomplète"] },
    ],
    recommendations: [
      "Audit immédiat des 47 fournisseurs niveau 2 en Asie du Sud-Est",
      "Mise en place canal signalement anonyme (obligation CSDDD Art. 9)",
      "Cartographie émissions scope 3 chaîne d'approvisionnement",
      "Nommer un Responsable Vigilance dédié",
    ],
    exposure: 2400000,
  }
}

const SECTORS = ["Industrie Manufacturière", "Mode & Textile", "Agroalimentaire", "Pharmaceutique", "Finance & Investissement", "Construction & BTP"]

export default function DemoPage() {
  const [company, setCompany] = useState("")
  const [sector, setSector] = useState(SECTORS[0])
  const [employees, setEmployees] = useState("500-1000")
  const [step, setStep] = useState<"form" | "scanning" | "results">("form")
  const [progress, setProgress] = useState(0)
  const [scanText, setScanText] = useState("")

  const ACCENT = "#6366f1"

  const startScan = () => {
    setStep("scanning")
    setProgress(0)
    const steps = [
      "Analyse des fournisseurs...",
      "Vérification conformité CSDDD...",
      "Scan droits humains...",
      "Évaluation risques environnementaux...",
      "Calcul exposition financière...",
      "Génération recommandations...",
    ]
    let i = 0
    const interval = setInterval(() => {
      if (i < steps.length) {
        setScanText(steps[i])
        setProgress(Math.round((i + 1) / steps.length * 100))
        i++
      } else {
        clearInterval(interval)
        setTimeout(() => setStep("results"), 500)
      }
    }, 600)
  }

  const data = DEMO_COMPANIES.default

  if (step === "form") return (
    <div style={{ background: "#0f172a", minHeight: "100vh", display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", padding: "40px 24px", fontFamily: "system-ui, sans-serif" }}>
      <div style={{ maxWidth: 560, width: "100%" }}>
        <div style={{ textAlign: "center", marginBottom: 40 }}>
          <div style={{ display: "inline-flex", alignItems: "center", gap: 8, background: "#6366f1", borderRadius: 8, padding: "6px 14px", marginBottom: 20 }}>
            <span style={{ color: "#fff", fontSize: 12, fontWeight: 700, letterSpacing: 1 }}>DÉMO GRATUITE</span>
          </div>
          <h1 style={{ margin: "0 0 12px", fontSize: 32, fontWeight: 800, color: "#f1f5f9", lineHeight: 1.2 }}>
            Analysez votre conformité<br /><span style={{ color: "#6366f1" }}>CSDDD en 30 secondes</span>
          </h1>
          <p style={{ margin: 0, color: "#94a3b8", fontSize: 16, lineHeight: 1.6 }}>
            Notre IA analyse votre exposition aux risques droits humains et environnementaux selon la directive européenne CSDDD 2024.
          </p>
        </div>
        <div style={{ background: "#1e293b", borderRadius: 16, padding: 32, border: "1px solid #334155" }}>
          <div style={{ marginBottom: 20 }}>
            <label style={{ display: "block", color: "#94a3b8", fontSize: 12, fontWeight: 600, marginBottom: 8, textTransform: "uppercase", letterSpacing: 0.5 }}>
              Nom de votre entreprise
            </label>
            <input
              value={company}
              onChange={e => setCompany(e.target.value)}
              placeholder="Ex: Acme Corp, Carrefour, ArcelorMittal..."
              style={{ width: "100%", background: "#0f172a", border: "1px solid #334155", borderRadius: 8, padding: "12px 16px", color: "#f1f5f9", fontSize: 14, outline: "none", boxSizing: "border-box" }}
            />
          </div>
          <div style={{ marginBottom: 20 }}>
            <label style={{ display: "block", color: "#94a3b8", fontSize: 12, fontWeight: 600, marginBottom: 8, textTransform: "uppercase", letterSpacing: 0.5 }}>
              Secteur d&apos;activité
            </label>
            <select
              value={sector}
              onChange={e => setSector(e.target.value)}
              style={{ width: "100%", background: "#0f172a", border: "1px solid #334155", borderRadius: 8, padding: "12px 16px", color: "#f1f5f9", fontSize: 14, outline: "none", boxSizing: "border-box" }}
            >
              {SECTORS.map(s => <option key={s} value={s}>{s}</option>)}
            </select>
          </div>
          <div style={{ marginBottom: 28 }}>
            <label style={{ display: "block", color: "#94a3b8", fontSize: 12, fontWeight: 600, marginBottom: 8, textTransform: "uppercase", letterSpacing: 0.5 }}>
              Nombre d&apos;employés
            </label>
            <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
              {["100-500", "500-1000", "1000-5000", "5000+"].map(opt => (
                <button key={opt} onClick={() => setEmployees(opt)}
                  style={{ padding: "8px 16px", borderRadius: 8, border: `1px solid ${employees === opt ? "#6366f1" : "#334155"}`, background: employees === opt ? "#6366f120" : "transparent", color: employees === opt ? "#6366f1" : "#94a3b8", fontSize: 13, fontWeight: 600, cursor: "pointer" }}>
                  {opt}
                </button>
              ))}
            </div>
          </div>
          <button onClick={startScan}
            style={{ width: "100%", background: "#6366f1", color: "#fff", border: "none", borderRadius: 10, padding: "14px", fontSize: 15, fontWeight: 700, cursor: "pointer", letterSpacing: 0.3 }}>
            Lancer l&apos;analyse CSDDD →
          </button>
          <p style={{ margin: "16px 0 0", textAlign: "center", color: "#475569", fontSize: 12 }}>
            Démo gratuite · Aucune installation · Résultats instantanés
          </p>
        </div>
        <div style={{ marginTop: 24, textAlign: "center" }}>
          <Link href="/" style={{ color: "#475569", fontSize: 13, textDecoration: "none" }}>← Retour à l&apos;accueil</Link>
        </div>
      </div>
    </div>
  )

  if (step === "scanning") return (
    <div style={{ background: "#0f172a", minHeight: "100vh", display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", padding: "40px 24px", fontFamily: "system-ui, sans-serif" }}>
      <div style={{ maxWidth: 480, width: "100%", textAlign: "center" }}>
        <div style={{ marginBottom: 32 }}>
          <div style={{ width: 72, height: 72, borderRadius: "50%", border: "3px solid #6366f1", borderTopColor: "transparent", margin: "0 auto 24px", animation: "spin 1s linear infinite" }} />
          <h2 style={{ color: "#f1f5f9", fontSize: 22, fontWeight: 700, margin: "0 0 8px" }}>Analyse en cours…</h2>
          <p style={{ color: "#6366f1", fontSize: 15, margin: 0, fontWeight: 600 }}>{scanText}</p>
        </div>
        <div style={{ background: "#1e293b", borderRadius: 10, height: 8, overflow: "hidden" }}>
          <div style={{ background: "#6366f1", height: "100%", width: `${progress}%`, transition: "width 0.5s ease", borderRadius: 10 }} />
        </div>
        <p style={{ color: "#475569", fontSize: 13, marginTop: 12 }}>{progress}% complété</p>
        <style>{`@keyframes spin { to { transform: rotate(360deg) } }`}</style>
      </div>
    </div>
  )

  // Results
  const scoreColor = data.score >= 70 ? "#ef4444" : data.score >= 40 ? "#f97316" : "#22c55e"
  const circumference = 2 * Math.PI * 54
  const filled = ((100 - data.score) / 100) * circumference

  return (
    <div style={{ background: "#0f172a", minHeight: "100vh", padding: "32px 24px", fontFamily: "system-ui, sans-serif" }}>
      <div style={{ maxWidth: 900, margin: "0 auto" }}>
        {/* Header */}
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 32, flexWrap: "wrap", gap: 12 }}>
          <div>
            <span style={{ background: "#ef444420", color: "#ef4444", borderRadius: 6, padding: "3px 10px", fontSize: 11, fontWeight: 700, textTransform: "uppercase", letterSpacing: 1 }}>
              RÉSULTATS DÉMO
            </span>
            <h1 style={{ margin: "8px 0 4px", fontSize: 26, fontWeight: 800, color: "#f1f5f9" }}>
              {company || "Votre entreprise"} — Analyse CSDDD
            </h1>
            <p style={{ margin: 0, color: "#64748b", fontSize: 14 }}>{sector} · {employees} employés · {new Date().toLocaleDateString("fr-FR")}</p>
          </div>
          <button onClick={() => setStep("form")} style={{ background: "#1e293b", border: "1px solid #334155", borderRadius: 8, padding: "8px 16px", color: "#94a3b8", fontSize: 13, cursor: "pointer" }}>
            Nouvelle analyse
          </button>
        </div>

        {/* Score global */}
        <div style={{ display: "grid", gridTemplateColumns: "auto 1fr", gap: 24, background: "#1e293b", borderRadius: 16, padding: 28, marginBottom: 24, border: "1px solid #334155", alignItems: "center" }}>
          <svg viewBox="0 0 120 120" width={120} height={120}>
            <circle cx={60} cy={60} r={54} fill="none" stroke="#0f172a" strokeWidth={10} />
            <circle cx={60} cy={60} r={54} fill="none" stroke={scoreColor} strokeWidth={10}
              strokeDasharray={`${circumference - filled} ${filled}`}
              transform="rotate(-90 60 60)" strokeLinecap="round" />
            <text x={60} y={55} textAnchor="middle" fill="#f1f5f9" fontSize={28} fontWeight="bold">{data.score}</text>
            <text x={60} y={75} textAnchor="middle" fill="#64748b" fontSize={11}>/100</text>
          </svg>
          <div>
            <div style={{ display: "inline-block", background: "#ef444420", color: "#ef4444", borderRadius: 6, padding: "3px 12px", fontSize: 12, fontWeight: 700, textTransform: "uppercase", marginBottom: 8 }}>
              Risque {data.risk_level}
            </div>
            <h2 style={{ margin: "0 0 8px", fontSize: 20, fontWeight: 700, color: "#f1f5f9" }}>Score de conformité CSDDD</h2>
            <p style={{ margin: "0 0 12px", color: "#94a3b8", fontSize: 14, lineHeight: 1.6 }}>
              Votre entreprise présente des lacunes significatives dans sa conformité à la directive CSDDD 2024. Une action immédiate est recommandée pour éviter des sanctions.
            </p>
            <div style={{ display: "flex", gap: 20 }}>
              <div>
                <div style={{ fontSize: 20, fontWeight: 700, color: "#ef4444" }}>€{(data.exposure / 1000000).toFixed(1)}M</div>
                <div style={{ fontSize: 11, color: "#64748b" }}>Exposition financière max.</div>
              </div>
              <div>
                <div style={{ fontSize: 20, fontWeight: 700, color: "#f97316" }}>4</div>
                <div style={{ fontSize: 11, color: "#64748b" }}>Zones à risque critique</div>
              </div>
              <div>
                <div style={{ fontSize: 20, fontWeight: 700, color: "#eab308" }}>47</div>
                <div style={{ fontSize: 11, color: "#64748b" }}>Fournisseurs à auditer</div>
              </div>
            </div>
          </div>
        </div>

        {/* Zones de risque */}
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(420px, 1fr))", gap: 16, marginBottom: 24 }}>
          {data.risks.map((risk) => {
            const rColor = risk.score >= 65 ? "#ef4444" : risk.score >= 45 ? "#f97316" : "#22c55e"
            const rCirc = 2 * Math.PI * 28
            const rFilled = ((100 - risk.score) / 100) * rCirc
            return (
              <div key={risk.area} style={{ background: "#1e293b", borderRadius: 12, padding: 20, border: "1px solid #334155", display: "flex", gap: 16, alignItems: "flex-start" }}>
                <svg viewBox="0 0 68 68" width={68} height={68} style={{ flexShrink: 0 }}>
                  <circle cx={34} cy={34} r={28} fill="none" stroke="#0f172a" strokeWidth={7} />
                  <circle cx={34} cy={34} r={28} fill="none" stroke={rColor} strokeWidth={7}
                    strokeDasharray={`${rCirc - rFilled} ${rFilled}`}
                    transform="rotate(-90 34 34)" strokeLinecap="round" />
                  <text x={34} y={38} textAnchor="middle" fill="#f1f5f9" fontSize={13} fontWeight="bold">{risk.score}</text>
                </svg>
                <div style={{ flex: 1 }}>
                  <h3 style={{ margin: "0 0 8px", fontSize: 14, fontWeight: 700, color: "#f1f5f9" }}>{risk.area}</h3>
                  {risk.issues.map(issue => (
                    <div key={issue} style={{ display: "flex", alignItems: "center", gap: 6, marginBottom: 4 }}>
                      <span style={{ color: rColor, fontSize: 14 }}>⚠</span>
                      <span style={{ color: "#94a3b8", fontSize: 12 }}>{issue}</span>
                    </div>
                  ))}
                </div>
              </div>
            )
          })}
        </div>

        {/* Recommandations */}
        <div style={{ background: "#1e293b", borderRadius: 16, padding: 24, marginBottom: 24, border: "1px solid #334155" }}>
          <h3 style={{ margin: "0 0 16px", fontSize: 16, fontWeight: 700, color: "#f1f5f9" }}>Recommandations prioritaires</h3>
          {data.recommendations.map((rec, i) => (
            <div key={i} style={{ display: "flex", alignItems: "flex-start", gap: 12, marginBottom: 12 }}>
              <div style={{ background: "#6366f1", borderRadius: "50%", width: 22, height: 22, display: "flex", alignItems: "center", justifyContent: "center", flexShrink: 0, fontSize: 11, fontWeight: 700, color: "#fff" }}>
                {i + 1}
              </div>
              <span style={{ color: "#cbd5e1", fontSize: 13, lineHeight: 1.5 }}>{rec}</span>
            </div>
          ))}
        </div>

        {/* CTA */}
        <div style={{ background: "linear-gradient(135deg, #6366f120, #8b5cf620)", borderRadius: 16, padding: 32, textAlign: "center", border: "1px solid #6366f130" }}>
          <h3 style={{ margin: "0 0 8px", fontSize: 20, fontWeight: 800, color: "#f1f5f9" }}>
            Ceci est une démo — Obtenez votre analyse complète
          </h3>
          <p style={{ margin: "0 0 24px", color: "#94a3b8", fontSize: 14, lineHeight: 1.6 }}>
            L&apos;analyse complète inclut 200+ points de contrôle, audit fournisseurs en temps réel, génération automatique des rapports CSDDD et suivi continu.
          </p>
          <div style={{ display: "flex", gap: 12, justifyContent: "center", flexWrap: "wrap" }}>
            <a href="mailto:retrouvetonsmile@gmail.com?subject=Demande démo CaelumSwarm&body=Bonjour, je souhaite une démonstration complète de CaelumSwarm."
              style={{ background: "#6366f1", color: "#fff", borderRadius: 10, padding: "12px 24px", fontSize: 14, fontWeight: 700, textDecoration: "none", display: "inline-block" }}>
              Demander une démo complète →
            </a>
            <Link href="/assistant"
              style={{ background: "#1e293b", color: "#94a3b8", border: "1px solid #334155", borderRadius: 10, padding: "12px 24px", fontSize: 14, fontWeight: 600, textDecoration: "none", display: "inline-block" }}>
              Parler à CaelumAI
            </Link>
          </div>
        </div>

        <div style={{ marginTop: 24, textAlign: "center" }}>
          <Link href="/" style={{ color: "#475569", fontSize: 13, textDecoration: "none" }}>← Retour à l&apos;accueil</Link>
        </div>
      </div>
    </div>
  )
}
