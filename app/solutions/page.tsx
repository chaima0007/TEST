"use client"

import { useState } from "react"
import Link from "next/link"

const ACCENT = "#6366f1"

const INDUSTRIES = [
  {
    icon: "👗",
    name: "Mode & Textile",
    subtitle: "Fast fashion, vêtements, accessoires",
    risks: [
      "Travail des enfants en Asie du Sud",
      "Conditions de travail usines de confection",
      "Traçabilité coton et fibres naturelles",
      "Rejets chimiques teintureries",
    ],
    riskLevel: "Critique",
    riskColor: "#ef4444",
    highlight: "87% des marques mode ont des lacunes CSDDD nivel 2",
  },
  {
    icon: "🌾",
    name: "Agroalimentaire",
    subtitle: "Agriculture, transformation, distribution",
    risks: [
      "Déforestation liée à l'huile de palme et soja",
      "Droits des travailleurs agricoles migrants",
      "Utilisation pesticides interdits UE",
      "Accaparement terres communautés locales",
    ],
    riskLevel: "Très élevé",
    riskColor: "#f97316",
    highlight: "CSDDD impose traçabilité jusqu'au champ agricole",
  },
  {
    icon: "⚙️",
    name: "Industrie Manufacturière",
    subtitle: "Équipements, automobile, électronique",
    risks: [
      "Minerais de conflits (cobalt, coltan, étain)",
      "Conditions de travail sous-traitants niveau 3",
      "Émissions scope 3 chaîne logistique",
      "Respect normes OIT pays production",
    ],
    riskLevel: "Élevé",
    riskColor: "#f97316",
    highlight: "Réglementation minerais de conflits renforcée en 2024",
  },
  {
    icon: "📊",
    name: "Finance & ESG",
    subtitle: "Banques, fonds d'investissement, assurances",
    risks: [
      "Financement d'activités violant droits humains",
      "Portefeuilles exposés à entreprises non conformes",
      "SFDR et taxonomie verte européenne",
      "Devoir de vigilance sur participations",
    ],
    riskLevel: "Modéré",
    riskColor: "#eab308",
    highlight: "Les institutions financières concernées dès 2028",
  },
]

function ROICalculator() {
  const [employees, setEmployees] = useState(1000)

  const exposure = employees * 50000
  const caelumCost = employees < 500 ? 2400 : employees < 2000 ? 9600 : 24000
  const roi = Math.round((exposure / caelumCost) * 100) / 100

  const formatEur = (n: number) => {
    if (n >= 1000000) return `€${(n / 1000000).toFixed(1)}M`
    if (n >= 1000) return `€${(n / 1000).toFixed(0)}K`
    return `€${n}`
  }

  return (
    <div style={{ background: "#1e293b", borderRadius: 16, padding: 32, border: "1px solid #334155" }}>
      <h3 style={{ margin: "0 0 8px", fontSize: 20, fontWeight: 800, color: "#f1f5f9" }}>
        Calculateur ROI — Combien risquez-vous ?
      </h3>
      <p style={{ margin: "0 0 28px", color: "#94a3b8", fontSize: 14 }}>
        Estimez votre exposition aux sanctions CSDDD et comparez-la au coût de CaelumSwarm.
      </p>

      <div style={{ marginBottom: 28 }}>
        <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 10 }}>
          <label style={{ color: "#94a3b8", fontSize: 13, fontWeight: 600 }}>Nombre d&apos;employés</label>
          <span style={{ color: "#6366f1", fontSize: 16, fontWeight: 700 }}>{employees.toLocaleString("fr-FR")}</span>
        </div>
        <input
          type="range"
          min={100}
          max={10000}
          step={100}
          value={employees}
          onChange={e => setEmployees(Number(e.target.value))}
          style={{ width: "100%", accentColor: "#6366f1", cursor: "pointer" }}
        />
        <div style={{ display: "flex", justifyContent: "space-between", marginTop: 4 }}>
          <span style={{ color: "#475569", fontSize: 11 }}>100</span>
          <span style={{ color: "#475569", fontSize: 11 }}>10 000</span>
        </div>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(200px, 1fr))", gap: 16 }}>
        <div style={{ background: "#0f172a", borderRadius: 12, padding: 20, border: "1px solid #ef444430", textAlign: "center" }}>
          <div style={{ fontSize: 11, fontWeight: 700, color: "#ef4444", textTransform: "uppercase", letterSpacing: 1, marginBottom: 8 }}>
            Exposition CSDDD max.
          </div>
          <div style={{ fontSize: 28, fontWeight: 800, color: "#ef4444" }}>{formatEur(exposure)}</div>
          <div style={{ fontSize: 11, color: "#475569", marginTop: 4 }}>Sanctions potentielles/an</div>
        </div>
        <div style={{ background: "#0f172a", borderRadius: 12, padding: 20, border: "1px solid #6366f130", textAlign: "center" }}>
          <div style={{ fontSize: 11, fontWeight: 700, color: "#6366f1", textTransform: "uppercase", letterSpacing: 1, marginBottom: 8 }}>
            Coût CaelumSwarm/an
          </div>
          <div style={{ fontSize: 28, fontWeight: 800, color: "#6366f1" }}>{formatEur(caelumCost)}</div>
          <div style={{ fontSize: 11, color: "#475569", marginTop: 4 }}>Protection complète CSDDD</div>
        </div>
        <div style={{ background: "#0f172a", borderRadius: 12, padding: 20, border: "1px solid #22c55e30", textAlign: "center" }}>
          <div style={{ fontSize: 11, fontWeight: 700, color: "#22c55e", textTransform: "uppercase", letterSpacing: 1, marginBottom: 8 }}>
            ROI protection
          </div>
          <div style={{ fontSize: 28, fontWeight: 800, color: "#22c55e" }}>×{roi > 1000 ? "1000+" : roi.toFixed(0)}</div>
          <div style={{ fontSize: 11, color: "#475569", marginTop: 4 }}>Valeur protégée / investissement</div>
        </div>
      </div>

      <div style={{ marginTop: 20, background: "#6366f110", borderRadius: 10, padding: 14, border: "1px solid #6366f120" }}>
        <p style={{ margin: 0, color: "#a5b4fc", fontSize: 13, textAlign: "center", lineHeight: 1.5 }}>
          Pour {employees.toLocaleString("fr-FR")} employés, CaelumSwarm coûte{" "}
          <strong style={{ color: "#6366f1" }}>{formatEur(caelumCost)}/an</strong> et vous protège d&apos;une exposition de{" "}
          <strong style={{ color: "#ef4444" }}>{formatEur(exposure)}</strong> en sanctions CSDDD.
        </p>
      </div>
    </div>
  )
}

interface FormState {
  name: string
  email: string
  company: string
  message: string
}

function ContactForm() {
  const [form, setForm] = useState<FormState>({ name: "", email: "", company: "", message: "" })

  const handleChange = (field: keyof FormState) => (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setForm(prev => ({ ...prev, [field]: e.target.value }))
  }

  const mailtoLink = `mailto:retrouvetonsmile@gmail.com?subject=Demande CaelumSwarm - ${encodeURIComponent(form.company || "Votre entreprise")}&body=${encodeURIComponent(`Bonjour,\n\nNom: ${form.name}\nEmail: ${form.email}\nEntreprise: ${form.company}\n\nMessage:\n${form.message}\n\nCordialement`)}`

  const inputStyle = {
    width: "100%",
    background: "#0f172a",
    border: "1px solid #334155",
    borderRadius: 8,
    padding: "12px 16px",
    color: "#f1f5f9",
    fontSize: 14,
    outline: "none",
    boxSizing: "border-box" as const,
    marginTop: 6,
  }

  const labelStyle = {
    display: "block" as const,
    color: "#94a3b8",
    fontSize: 12,
    fontWeight: 600 as const,
    textTransform: "uppercase" as const,
    letterSpacing: 0.5,
  }

  return (
    <div style={{ background: "#1e293b", borderRadius: 16, padding: 32, border: "1px solid #334155" }}>
      <h3 style={{ margin: "0 0 8px", fontSize: 20, fontWeight: 800, color: "#f1f5f9" }}>
        Parler à un expert CSDDD
      </h3>
      <p style={{ margin: "0 0 24px", color: "#94a3b8", fontSize: 14 }}>
        Notre équipe répond sous 24h pour un audit de conformité personnalisé.
      </p>

      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16, marginBottom: 16 }}>
        <div>
          <label style={labelStyle}>Votre nom</label>
          <input value={form.name} onChange={handleChange("name")} placeholder="Jean Dupont" style={inputStyle} />
        </div>
        <div>
          <label style={labelStyle}>Email professionnel</label>
          <input value={form.email} onChange={handleChange("email")} type="email" placeholder="jean@entreprise.com" style={inputStyle} />
        </div>
      </div>

      <div style={{ marginBottom: 16 }}>
        <label style={labelStyle}>Entreprise</label>
        <input value={form.company} onChange={handleChange("company")} placeholder="Nom de votre entreprise" style={inputStyle} />
      </div>

      <div style={{ marginBottom: 24 }}>
        <label style={labelStyle}>Message</label>
        <textarea
          value={form.message}
          onChange={handleChange("message")}
          placeholder="Décrivez votre situation CSDDD, vos enjeux, vos questions..."
          rows={4}
          style={{ ...inputStyle, resize: "vertical" as const }}
        />
      </div>

      <a href={mailtoLink}
        style={{ display: "block", background: ACCENT, color: "#fff", borderRadius: 10, padding: "14px", fontSize: 15, fontWeight: 700, textDecoration: "none", textAlign: "center", cursor: "pointer" }}>
        Envoyer ma demande →
      </a>

      <p style={{ margin: "12px 0 0", textAlign: "center", color: "#475569", fontSize: 12 }}>
        Réponse garantie sous 24h · Audit initial gratuit · Aucun engagement
      </p>
    </div>
  )
}

export default function SolutionsPage() {
  const [activeIndustry, setActiveIndustry] = useState<string | null>(null)

  return (
    <div style={{ background: "#0f172a", minHeight: "100vh", fontFamily: "system-ui, sans-serif" }}>
      {/* Header */}
      <div style={{ background: "#1e293b", borderBottom: "1px solid #334155", padding: "20px 24px" }}>
        <div style={{ maxWidth: 1100, margin: "0 auto", display: "flex", justifyContent: "space-between", alignItems: "center", flexWrap: "wrap", gap: 12 }}>
          <div>
            <Link href="/" style={{ color: "#6366f1", fontSize: 13, textDecoration: "none", fontWeight: 600 }}>
              ← Caelum Partners
            </Link>
            <h1 style={{ margin: "4px 0 0", fontSize: 24, fontWeight: 800, color: "#f1f5f9" }}>
              Solutions CSDDD par Industrie
            </h1>
          </div>
          <div style={{ display: "flex", gap: 10 }}>
            <Link href="/demo" style={{ background: "#6366f1", color: "#fff", borderRadius: 8, padding: "9px 16px", fontSize: 13, fontWeight: 600, textDecoration: "none" }}>
              Démo gratuite
            </Link>
            <Link href="/assistant" style={{ background: "transparent", color: "#94a3b8", border: "1px solid #334155", borderRadius: 8, padding: "9px 16px", fontSize: 13, fontWeight: 600, textDecoration: "none" }}>
              CaelumAI
            </Link>
          </div>
        </div>
      </div>

      <div style={{ maxWidth: 1100, margin: "0 auto", padding: "48px 24px" }}>
        {/* Hero */}
        <div style={{ textAlign: "center", marginBottom: 56 }}>
          <div style={{ display: "inline-flex", alignItems: "center", gap: 8, background: "#6366f110", border: "1px solid #6366f130", borderRadius: 20, padding: "6px 16px", marginBottom: 20 }}>
            <span style={{ color: "#6366f1", fontSize: 12, fontWeight: 700, letterSpacing: 1 }}>SOLUTIONS SECTORIELLES</span>
          </div>
          <h2 style={{ margin: "0 0 16px", fontSize: 36, fontWeight: 800, color: "#f1f5f9", lineHeight: 1.2 }}>
            La CSDDD adaptée à<br /><span style={{ color: "#6366f1" }}>votre secteur d&apos;activité</span>
          </h2>
          <p style={{ margin: "0 auto", color: "#94a3b8", fontSize: 16, lineHeight: 1.7, maxWidth: 600 }}>
            Chaque industrie présente des risques droits humains et environnementaux différents. CaelumSwarm analyse les 180+ domaines de risque spécifiques à votre secteur.
          </p>
        </div>

        {/* Industries grid */}
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(480px, 1fr))", gap: 20, marginBottom: 64 }}>
          {INDUSTRIES.map(industry => (
            <div
              key={industry.name}
              style={{
                background: "#1e293b",
                borderRadius: 16,
                padding: 28,
                border: `1px solid ${activeIndustry === industry.name ? "#6366f1" : "#334155"}`,
                cursor: "pointer",
                transition: "border-color 0.2s",
              }}
              onClick={() => setActiveIndustry(activeIndustry === industry.name ? null : industry.name)}
            >
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 16 }}>
                <div style={{ display: "flex", gap: 12, alignItems: "center" }}>
                  <div style={{ fontSize: 32 }}>{industry.icon}</div>
                  <div>
                    <h3 style={{ margin: "0 0 2px", fontSize: 17, fontWeight: 700, color: "#f1f5f9" }}>{industry.name}</h3>
                    <p style={{ margin: 0, color: "#64748b", fontSize: 13 }}>{industry.subtitle}</p>
                  </div>
                </div>
                <span style={{ background: `${industry.riskColor}20`, color: industry.riskColor, borderRadius: 6, padding: "3px 10px", fontSize: 11, fontWeight: 700, textTransform: "uppercase", flexShrink: 0 }}>
                  {industry.riskLevel}
                </span>
              </div>

              <div style={{ background: "#0f172a", borderRadius: 8, padding: "8px 12px", marginBottom: 16, border: `1px solid ${industry.riskColor}20` }}>
                <p style={{ margin: 0, color: industry.riskColor, fontSize: 12, fontWeight: 600 }}>⚡ {industry.highlight}</p>
              </div>

              <div style={{ marginBottom: 16 }}>
                <p style={{ margin: "0 0 10px", color: "#64748b", fontSize: 11, fontWeight: 700, textTransform: "uppercase", letterSpacing: 0.5 }}>
                  Risques CSDDD identifiés
                </p>
                {industry.risks.map(risk => (
                  <div key={risk} style={{ display: "flex", alignItems: "flex-start", gap: 8, marginBottom: 6 }}>
                    <span style={{ color: industry.riskColor, fontSize: 12, marginTop: 1 }}>▸</span>
                    <span style={{ color: "#94a3b8", fontSize: 13 }}>{risk}</span>
                  </div>
                ))}
              </div>

              <div style={{ display: "flex", gap: 10 }}>
                <Link
                  href="/demo"
                  onClick={e => e.stopPropagation()}
                  style={{ flex: 1, background: ACCENT, color: "#fff", borderRadius: 8, padding: "10px", fontSize: 13, fontWeight: 600, textDecoration: "none", textAlign: "center", display: "block" }}>
                  Voir la solution {industry.name.split(" ")[0]} →
                </Link>
                <Link
                  href="/assistant"
                  onClick={e => e.stopPropagation()}
                  style={{ background: "#0f172a", color: "#64748b", border: "1px solid #334155", borderRadius: 8, padding: "10px 14px", fontSize: 13, fontWeight: 600, textDecoration: "none", display: "flex", alignItems: "center" }}>
                  Q&amp;A
                </Link>
              </div>
            </div>
          ))}
        </div>

        {/* Stats section */}
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(200px, 1fr))", gap: 16, marginBottom: 64 }}>
          {[
            { value: "180+", label: "Domaines de risque analysés", color: "#6366f1" },
            { value: "5%", label: "CA mondial — sanction maximale CSDDD", color: "#ef4444" },
            { value: "2027", label: "Entrée en vigueur pour les grandes entreprises", color: "#f97316" },
            { value: "98%", label: "Taux de conformité moyen après 6 mois CaelumSwarm", color: "#22c55e" },
          ].map(stat => (
            <div key={stat.label} style={{ background: "#1e293b", borderRadius: 12, padding: 20, border: "1px solid #334155", textAlign: "center" }}>
              <div style={{ fontSize: 32, fontWeight: 800, color: stat.color, marginBottom: 6 }}>{stat.value}</div>
              <div style={{ color: "#64748b", fontSize: 12, lineHeight: 1.4 }}>{stat.label}</div>
            </div>
          ))}
        </div>

        {/* ROI Calculator */}
        <div style={{ marginBottom: 48 }}>
          <ROICalculator />
        </div>

        {/* Process steps */}
        <div style={{ marginBottom: 64 }}>
          <h3 style={{ textAlign: "center", margin: "0 0 36px", fontSize: 24, fontWeight: 800, color: "#f1f5f9" }}>
            Comment CaelumSwarm vous protège
          </h3>
          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(220px, 1fr))", gap: 20 }}>
            {[
              { step: "01", title: "Analyse initiale", desc: "Audit complet de votre chaîne de valeur selon les 180+ domaines de risque CSDDD", icon: "🔍" },
              { step: "02", title: "Cartographie risques", desc: "Identification et priorisation des fournisseurs et zones géographiques à risque", icon: "🗺️" },
              { step: "03", title: "Plan d'action", desc: "Recommandations concrètes et plan de mise en conformité avec jalons mesurables", icon: "📋" },
              { step: "04", title: "Surveillance continue", desc: "Monitoring en temps réel + alertes automatiques + rapport CSDDD annuel généré", icon: "🛡️" },
            ].map(item => (
              <div key={item.step} style={{ background: "#1e293b", borderRadius: 12, padding: 24, border: "1px solid #334155", textAlign: "center" }}>
                <div style={{ fontSize: 28, marginBottom: 12 }}>{item.icon}</div>
                <div style={{ fontSize: 11, fontWeight: 700, color: "#6366f1", textTransform: "uppercase", letterSpacing: 1, marginBottom: 6 }}>
                  Étape {item.step}
                </div>
                <h4 style={{ margin: "0 0 8px", fontSize: 15, fontWeight: 700, color: "#f1f5f9" }}>{item.title}</h4>
                <p style={{ margin: 0, color: "#64748b", fontSize: 13, lineHeight: 1.5 }}>{item.desc}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Contact form */}
        <div style={{ marginBottom: 48 }}>
          <ContactForm />
        </div>

        {/* Footer nav */}
        <div style={{ textAlign: "center", paddingTop: 24, borderTop: "1px solid #1e293b" }}>
          <div style={{ display: "flex", gap: 24, justifyContent: "center", flexWrap: "wrap" }}>
            <Link href="/" style={{ color: "#475569", fontSize: 13, textDecoration: "none" }}>Accueil</Link>
            <Link href="/demo" style={{ color: "#475569", fontSize: 13, textDecoration: "none" }}>Démo</Link>
            <Link href="/assistant" style={{ color: "#475569", fontSize: 13, textDecoration: "none" }}>CaelumAI</Link>
            <a href="mailto:retrouvetonsmile@gmail.com" style={{ color: "#475569", fontSize: 13, textDecoration: "none" }}>Contact</a>
          </div>
          <p style={{ margin: "16px 0 0", color: "#334155", fontSize: 12 }}>
            © 2024 Caelum Partners · Plateforme CSDDD · Conformité droits humains et environnement
          </p>
        </div>
      </div>
    </div>
  )
}
