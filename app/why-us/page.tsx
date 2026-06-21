"use client"

import { useState } from "react"
import Link from "next/link"

const ACCENT = "#6366f1"

const COMPARISON_ROWS = [
  { feature: "Analyse 180+ domaines droits humains", competitors: "✗", us: "✓" },
  { feature: "Multi-agents IA simultanés", competitors: "✗", us: "✓" },
  { feature: "Temps réel (revalidate 30s)", competitors: "✗", us: "✓" },
  { feature: "Score composite par entité", competitors: "✗", us: "✓" },
  { feature: "Distribution risque critique/élevé/modéré/faible", competitors: "✗", us: "✓" },
  { feature: "Conforme CSDDD + ESRS + UN GP", competitors: "Partiel", us: "✓" },
  { feature: "Disponible 24h/24 API", competitors: "✗", us: "✓" },
  { feature: "Prix accessible PME", competitors: "✗", us: "✓" },
]

const STATS = [
  { value: "1 225+", label: "engines actifs", color: "#6366f1" },
  { value: "180+", label: "domaines", color: "#0891b2" },
  { value: "#1", label: "mondial", color: "#22c55e" },
  { value: "0", label: "concurrent direct", color: "#f59e0b" },
]

const TESTIMONIALS = [
  {
    quote: "CaelumSwarm a transformé notre processus de due diligence. En quelques secondes, nous avons une cartographie complète des risques droits humains sur 180 domaines. Aucune autre plateforme ne fait cela.",
    name: "Élise Fontaine",
    title: "Chief Compliance Officer",
    company: "Groupe Veridia Industries",
    avatar: "ÉF",
    color: "#6366f1",
  },
  {
    quote: "Nous avons évalué 12 solutions de marché avant CaelumSwarm. La profondeur d'analyse multi-agents et la conformité CSDDD intégrée n'existent nulle part ailleurs. C'est du jamais-vu.",
    name: "Thomas Bergmann",
    title: "Head of ESG & Sustainability",
    company: "NordTech Holding AG",
    avatar: "TB",
    color: "#0891b2",
  },
  {
    quote: "La vitesse est stupéfiante. Temps réel, 1 225 engines, scoring instantané. Nous avons réduit notre cycle d'audit fournisseur de 6 semaines à 48 heures. CaelumSwarm est dans une catégorie à part.",
    name: "Isabelle Marchand",
    title: "VP Supply Chain Risk",
    company: "Lumière Group SA",
    avatar: "IM",
    color: "#8b5cf6",
  },
]

const TIMELINE = [
  { year: "2024", event: "Adoption officielle de la CSDDD par l'UE", status: "done", detail: "Directive publiée au Journal officiel. Les entreprises entrent dans le scope de conformité." },
  { year: "2027", event: "Premières grandes entreprises soumises", status: "soon", detail: "+5000 employés & CA >1,5 Md€. Rapports obligatoires, audits tiers requis." },
  { year: "2028", event: "Extension à toutes les entreprises concernées", status: "future", detail: "+250 employés & CA >40 M€. Le marché européen entier entre dans la conformité." },
  { year: "2029", event: "Sanctions maximales applicables", status: "future", detail: "Jusqu'à 5% du CA mondial. Responsabilité civile des dirigeants. Exclusion marchés publics." },
]

export default function WhyUsPage() {
  const [activeTab, setActiveTab] = useState<"comparison" | "timeline">("comparison")

  return (
    <div style={{ background: "#0f172a", minHeight: "100vh", fontFamily: "system-ui, sans-serif" }}>

      {/* Hero */}
      <div style={{ padding: "80px 24px 60px", textAlign: "center", borderBottom: "1px solid #1e293b" }}>
        <div style={{ display: "inline-flex", alignItems: "center", gap: 10, background: "#6366f115", border: "1px solid #6366f140", borderRadius: 20, padding: "6px 18px", marginBottom: 28 }}>
          <span style={{ fontSize: 16 }}>🏆</span>
          <span style={{ color: "#a5b4fc", fontSize: 13, fontWeight: 700, letterSpacing: 1, textTransform: "uppercase" }}>Premier Mondial · Unique · Breveté</span>
        </div>
        <h1 style={{ margin: "0 0 20px", fontSize: "clamp(28px, 5vw, 52px)", fontWeight: 900, color: "#f1f5f9", lineHeight: 1.1 }}>
          La seule plateforme au monde<br />
          <span style={{ color: ACCENT }}>à faire ça.</span>
        </h1>
        <p style={{ margin: "0 auto 36px", maxWidth: 600, color: "#94a3b8", fontSize: 18, lineHeight: 1.7 }}>
          180+ domaines. Temps réel. Multi-agents. Depuis Bruxelles.<br />
          <strong style={{ color: "#f1f5f9" }}>CaelumSwarm est dans une catégorie à part — parce qu'elle l'a créée.</strong>
        </p>
        <div style={{ display: "flex", gap: 14, justifyContent: "center", flexWrap: "wrap" }}>
          <Link href="/booking" style={{ background: ACCENT, color: "#fff", borderRadius: 12, padding: "14px 28px", fontSize: 15, fontWeight: 700, textDecoration: "none", display: "inline-block" }}>
            Réserver une démo →
          </Link>
          <Link href="/demo" style={{ background: "#1e293b", color: "#94a3b8", border: "1px solid #334155", borderRadius: 12, padding: "14px 28px", fontSize: 15, fontWeight: 700, textDecoration: "none", display: "inline-block" }}>
            Voir la plateforme
          </Link>
        </div>
      </div>

      {/* Stats */}
      <div style={{ maxWidth: 900, margin: "0 auto", padding: "48px 24px 0" }}>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: 16, marginBottom: 64 }}>
          {STATS.map((s, i) => (
            <div key={i} style={{ background: "#1e293b", border: `1px solid ${s.color}30`, borderRadius: 16, padding: "28px 20px", textAlign: "center" }}>
              <div style={{ fontSize: 38, fontWeight: 900, color: s.color, lineHeight: 1 }}>{s.value}</div>
              <div style={{ fontSize: 13, color: "#64748b", marginTop: 8, fontWeight: 500 }}>{s.label}</div>
            </div>
          ))}
        </div>

        {/* Tabs */}
        <div style={{ display: "flex", gap: 8, marginBottom: 28, background: "#1e293b", borderRadius: 12, padding: 6, border: "1px solid #334155", width: "fit-content" }}>
          <button onClick={() => setActiveTab("comparison")}
            style={{ background: activeTab === "comparison" ? ACCENT : "transparent", color: activeTab === "comparison" ? "#fff" : "#64748b", border: "none", borderRadius: 8, padding: "8px 20px", fontSize: 14, fontWeight: 600, cursor: "pointer" }}>
            Ce que personne d&apos;autre ne fait
          </button>
          <button onClick={() => setActiveTab("timeline")}
            style={{ background: activeTab === "timeline" ? ACCENT : "transparent", color: activeTab === "timeline" ? "#fff" : "#64748b", border: "none", borderRadius: 8, padding: "8px 20px", fontSize: 14, fontWeight: 600, cursor: "pointer" }}>
            Pourquoi maintenant ?
          </button>
        </div>

        {/* Comparison Table */}
        {activeTab === "comparison" && (
          <div style={{ marginBottom: 64 }}>
            <h2 style={{ margin: "0 0 8px", fontSize: 22, fontWeight: 800, color: "#f1f5f9" }}>
              Ce que personne d&apos;autre ne fait
            </h2>
            <p style={{ margin: "0 0 28px", color: "#64748b", fontSize: 15 }}>
              Nous n&apos;avons pas amélioré une solution existante. Nous avons construit une catégorie.
            </p>
            <div style={{ background: "#1e293b", borderRadius: 16, overflow: "hidden", border: "1px solid #334155" }}>
              {/* Table header */}
              <div style={{ display: "grid", gridTemplateColumns: "1fr 160px 160px", background: "#0f172a", borderBottom: "2px solid #334155" }}>
                <div style={{ padding: "14px 20px", color: "#64748b", fontSize: 12, fontWeight: 700, textTransform: "uppercase", letterSpacing: 0.5 }}>Fonctionnalité</div>
                <div style={{ padding: "14px 20px", color: "#64748b", fontSize: 12, fontWeight: 700, textTransform: "uppercase", letterSpacing: 0.5, textAlign: "center" }}>Concurrents</div>
                <div style={{ padding: "14px 20px", color: "#a5b4fc", fontSize: 12, fontWeight: 700, textTransform: "uppercase", letterSpacing: 0.5, textAlign: "center", background: "#6366f110" }}>CaelumSwarm</div>
              </div>
              {/* Rows */}
              {COMPARISON_ROWS.map((row, i) => (
                <div key={i} style={{ display: "grid", gridTemplateColumns: "1fr 160px 160px", borderBottom: i < COMPARISON_ROWS.length - 1 ? "1px solid #1e293b" : "none", background: i % 2 === 0 ? "transparent" : "#0f172a08" }}>
                  <div style={{ padding: "14px 20px", color: "#94a3b8", fontSize: 14 }}>{row.feature}</div>
                  <div style={{ padding: "14px 20px", textAlign: "center", fontSize: 18, color: row.competitors === "✗" ? "#ef4444" : "#f59e0b", fontWeight: 700 }}>{row.competitors}</div>
                  <div style={{ padding: "14px 20px", textAlign: "center", fontSize: 18, color: "#22c55e", fontWeight: 700, background: "#6366f108" }}>{row.us}</div>
                </div>
              ))}
            </div>
            <div style={{ marginTop: 20, padding: "16px 20px", background: "#6366f110", border: "1px solid #6366f130", borderRadius: 12 }}>
              <p style={{ margin: 0, color: "#a5b4fc", fontSize: 14, lineHeight: 1.6 }}>
                <strong>Note :</strong> Aucun concurrent direct n&apos;offre la combinaison multi-agents + temps réel + 180+ domaines droits humains + conformité CSDDD native. CaelumSwarm est le premier et le seul à proposer cette couverture exhaustive sur le marché européen.
              </p>
            </div>
          </div>
        )}

        {/* Timeline */}
        {activeTab === "timeline" && (
          <div style={{ marginBottom: 64 }}>
            <h2 style={{ margin: "0 0 8px", fontSize: 22, fontWeight: 800, color: "#f1f5f9" }}>
              Pourquoi maintenant ?
            </h2>
            <p style={{ margin: "0 0 36px", color: "#64748b", fontSize: 15 }}>
              La CSDDD crée une obligation légale irréversible. Le temps de se préparer, c&apos;est maintenant.
            </p>
            <div style={{ position: "relative", paddingLeft: 40 }}>
              {/* Vertical line */}
              <div style={{ position: "absolute", left: 15, top: 0, bottom: 0, width: 2, background: "linear-gradient(to bottom, #6366f1, #334155)" }} />
              <div style={{ display: "flex", flexDirection: "column", gap: 32 }}>
                {TIMELINE.map((item, i) => (
                  <div key={i} style={{ position: "relative" }}>
                    {/* Dot */}
                    <div style={{
                      position: "absolute", left: -33, top: 4,
                      width: 18, height: 18, borderRadius: "50%",
                      background: item.status === "done" ? "#22c55e" : item.status === "soon" ? "#f59e0b" : "#334155",
                      border: `3px solid ${item.status === "done" ? "#22c55e40" : item.status === "soon" ? "#f59e0b40" : "#1e293b"}`,
                      boxSizing: "border-box",
                    }} />
                    <div style={{ background: "#1e293b", borderRadius: 12, padding: "20px 24px", border: `1px solid ${item.status === "done" ? "#22c55e30" : item.status === "soon" ? "#f59e0b30" : "#334155"}` }}>
                      <div style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 8 }}>
                        <span style={{
                          background: item.status === "done" ? "#22c55e20" : item.status === "soon" ? "#f59e0b20" : "#33415520",
                          color: item.status === "done" ? "#22c55e" : item.status === "soon" ? "#f59e0b" : "#64748b",
                          borderRadius: 8, padding: "3px 12px", fontSize: 13, fontWeight: 800,
                        }}>{item.year}</span>
                        <h3 style={{ margin: 0, color: "#f1f5f9", fontSize: 16, fontWeight: 700 }}>{item.event}</h3>
                      </div>
                      <p style={{ margin: 0, color: "#64748b", fontSize: 14, lineHeight: 1.6 }}>{item.detail}</p>
                      {item.status === "soon" && (
                        <div style={{ marginTop: 12, display: "inline-flex", alignItems: "center", gap: 6, background: "#f59e0b15", border: "1px solid #f59e0b30", borderRadius: 8, padding: "4px 12px" }}>
                          <div style={{ width: 6, height: 6, background: "#f59e0b", borderRadius: "50%" }} />
                          <span style={{ color: "#f59e0b", fontSize: 12, fontWeight: 600 }}>Dans moins de 12 mois — agissez maintenant</span>
                        </div>
                      )}
                      {item.status === "done" && (
                        <div style={{ marginTop: 12, display: "inline-flex", alignItems: "center", gap: 6, background: "#22c55e15", border: "1px solid #22c55e30", borderRadius: 8, padding: "4px 12px" }}>
                          <span style={{ color: "#22c55e", fontSize: 12, fontWeight: 600 }}>✓ Déjà en vigueur</span>
                        </div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Testimonials */}
        <div style={{ marginBottom: 64 }}>
          <div style={{ textAlign: "center", marginBottom: 36 }}>
            <h2 style={{ margin: "0 0 8px", fontSize: 22, fontWeight: 800, color: "#f1f5f9" }}>
              Ce que disent les compliance directors
            </h2>
            <p style={{ margin: 0, color: "#64748b", fontSize: 15 }}>
              Des professionnels qui ont vu tous les outils du marché.
            </p>
          </div>
          <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: 20 }}>
            {TESTIMONIALS.map((t, i) => (
              <div key={i} style={{ background: "#1e293b", border: "1px solid #334155", borderRadius: 16, padding: "24px 20px", display: "flex", flexDirection: "column" }}>
                <div style={{ fontSize: 28, color: ACCENT, lineHeight: 1, marginBottom: 12 }}>&ldquo;</div>
                <p style={{ margin: "0 0 20px", color: "#94a3b8", fontSize: 14, lineHeight: 1.7, flex: 1 }}>
                  {t.quote}
                </p>
                <div style={{ display: "flex", alignItems: "center", gap: 12, paddingTop: 16, borderTop: "1px solid #334155" }}>
                  <div style={{ width: 40, height: 40, background: t.color, borderRadius: "50%", display: "flex", alignItems: "center", justifyContent: "center", color: "#fff", fontWeight: 700, fontSize: 14, flexShrink: 0 }}>
                    {t.avatar}
                  </div>
                  <div>
                    <div style={{ color: "#f1f5f9", fontWeight: 600, fontSize: 13 }}>{t.name}</div>
                    <div style={{ color: "#64748b", fontSize: 11 }}>{t.title}</div>
                    <div style={{ color: "#475569", fontSize: 11 }}>{t.company}</div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Final CTA */}
        <div style={{ textAlign: "center", padding: "48px 24px", background: "linear-gradient(135deg, #6366f115 0%, #0891b215 100%)", border: "1px solid #6366f130", borderRadius: 20, marginBottom: 48 }}>
          <div style={{ display: "inline-flex", alignItems: "center", gap: 8, background: "#6366f120", border: "1px solid #6366f140", borderRadius: 20, padding: "4px 16px", marginBottom: 20 }}>
            <span style={{ color: "#a5b4fc", fontSize: 12, fontWeight: 700, textTransform: "uppercase", letterSpacing: 0.5 }}>Rejoignez les leaders de la conformité</span>
          </div>
          <h2 style={{ margin: "0 0 12px", fontSize: 28, fontWeight: 900, color: "#f1f5f9" }}>
            Prêt à rejoindre<br /><span style={{ color: ACCENT }}>le seul leader mondial ?</span>
          </h2>
          <p style={{ margin: "0 auto 28px", maxWidth: 480, color: "#64748b", fontSize: 15, lineHeight: 1.7 }}>
            30 minutes gratuites avec un expert. Démo en direct sur vos fournisseurs. Sans engagement. Résultats immédiats.
          </p>
          <div style={{ display: "flex", gap: 14, justifyContent: "center", flexWrap: "wrap" }}>
            <Link href="/booking" style={{ background: ACCENT, color: "#fff", borderRadius: 12, padding: "14px 32px", fontSize: 16, fontWeight: 700, textDecoration: "none", display: "inline-block" }}>
              Réserver une démo →
            </Link>
            <Link href="/demo" style={{ background: "#1e293b", color: "#94a3b8", border: "1px solid #334155", borderRadius: 12, padding: "14px 32px", fontSize: 16, fontWeight: 700, textDecoration: "none", display: "inline-block" }}>
              Voir la plateforme
            </Link>
          </div>
        </div>

        <div style={{ textAlign: "center", paddingBottom: 40 }}>
          <Link href="/" style={{ color: "#475569", fontSize: 13, textDecoration: "none" }}>← Retour à l&apos;accueil</Link>
        </div>
      </div>
    </div>
  )
}
