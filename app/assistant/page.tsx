"use client"

import { useState, useRef, useEffect } from "react"
import Link from "next/link"

const ACCENT = "#6366f1"

interface Message {
  role: "user" | "assistant"
  content: string
  timestamp: Date
}

const KNOWLEDGE_BASE: Record<string, string> = {
  "csddd": `La **CSDDD** (Corporate Sustainability Due Diligence Directive) est la directive européenne adoptée en 2024 qui oblige les grandes entreprises à identifier et traiter leurs impacts négatifs sur les droits humains et l'environnement dans toute leur chaîne de valeur.

**Qui est concerné ?**
• Entreprises EU : +1 000 employés et +450M€ de CA (à partir de 2027)
• Entreprises hors EU : +450M€ de CA en UE (à partir de 2028)

**Obligations principales :**
1. Politique de due diligence documentée
2. Cartographie des risques (chaîne de valeur niveau 1 et 2)
3. Mesures préventives et correctives
4. Canal de signalement accessible
5. Rapport annuel public

**Sanctions :** Jusqu'à 5% du CA mondial + responsabilité civile`,

  "amende": `**Sanctions CSDDD — Calcul de votre exposition financière**

La directive prévoit des sanctions graduelles selon la taille de l'entreprise :

• **Pénalité maximale :** 5% du chiffre d'affaires mondial annuel
• **Responsabilité civile :** Les victimes peuvent intenter une action en justice directement
• **Publication obligatoire :** Liste publique des entreprises sanctionnées
• **Suspension marchés publics UE** possible

**Exemple concret :**
- CA mondial €500M → exposition max. **€25M**
- CA mondial €2Mds → exposition max. **€100M**
- CA mondial €10Mds → exposition max. **€500M**

Utilisez notre calculateur ROI pour estimer votre exposition précise.`,

  "chaine": `**Cartographie chaîne de valeur — Comment procéder ?**

La CSDDD impose d'analyser toute votre chaîne de valeur, pas seulement vos fournisseurs directs.

**Étape 1 — Niveau 1 (fournisseurs directs)**
• Inventaire complet de tous vos fournisseurs directs
• Questionnaire de due diligence envoyé à chacun
• Audit sur site pour les risques élevés

**Étape 2 — Niveau 2+ (sous-traitants)**
• Identification des zones géographiques à risque
• Focus sur les secteurs critiques : textile, électronique, agriculture
• Audit de second niveau si risques identifiés

**Étape 3 — Surveillance continue**
• Caelum monitore 180+ domaines de risque en temps réel
• Alertes automatiques si un fournisseur apparaît dans nos bases de données
• Rapport CSDDD généré automatiquement

Souhaitez-vous que j'analyse votre secteur spécifique ?`,

  "rapport": `**Rapport CSDDD annuel — Ce qu'il doit contenir**

Le rapport de due diligence doit être publié annuellement et contenir :

✓ **Description de l'entreprise** et de sa chaîne de valeur
✓ **Politique de due diligence** et gouvernance
✓ **Risques identifiés** : description et priorisation
✓ **Mesures prises** pour prévenir et atténuer
✓ **Résultats et indicateurs** de performance
✓ **Consultation des parties prenantes** (employés, communautés affectées)
✓ **Mécanisme de réclamation** disponible

**Caelum génère automatiquement** ce rapport en conformité avec les exigences CSDDD, ESRS et UN Guiding Principles.`,

  "fournisseur": `**Gestion des fournisseurs non conformes — Que faire ?**

La CSDDD ne vous oblige PAS à couper immédiatement les liens avec un fournisseur non conforme. Voici la procédure à suivre :

**1. Notification formelle**
Informez le fournisseur des lacunes identifiées et fixez un délai d'amélioration (généralement 6-12 mois).

**2. Plan d'action correctif**
Établissez un plan d'amélioration avec des jalons mesurables.

**3. Soutien et renforcement des capacités**
Proposez une formation ou un accompagnement technique si possible.

**4. Suspension puis résiliation**
Si aucune amélioration après le délai : suspension puis fin de contrat.

**Important :** Documentez tout. En cas de poursuite, votre historique de diligence est votre protection.`,
}

function getAIResponse(userMessage: string): string {
  const msg = userMessage.toLowerCase()

  if (msg.includes("csddd") || msg.includes("directive") || msg.includes("qu'est-ce") || msg.includes("c'est quoi")) {
    return KNOWLEDGE_BASE["csddd"]
  }
  if (msg.includes("amende") || msg.includes("sanction") || msg.includes("pénalité") || msg.includes("risque financier") || msg.includes("coût")) {
    return KNOWLEDGE_BASE["amende"]
  }
  if (msg.includes("chaîne") || msg.includes("chaine") || msg.includes("fournisseur") && msg.includes("cartographi")) {
    return KNOWLEDGE_BASE["chaine"]
  }
  if (msg.includes("rapport") || msg.includes("reporting") || msg.includes("document")) {
    return KNOWLEDGE_BASE["rapport"]
  }
  if (msg.includes("fournisseur") || msg.includes("supplier")) {
    return KNOWLEDGE_BASE["fournisseur"]
  }
  if (msg.includes("bonjour") || msg.includes("hello") || msg.includes("salut") || msg.includes("hi")) {
    return `Bonjour ! Je suis **CaelumAI**, l'assistant de conformité CSDDD de Caelum Partners.

Je peux vous aider à :
• Comprendre vos obligations CSDDD 2024
• Calculer votre exposition financière
• Cartographier vos risques fournisseurs
• Préparer votre rapport de due diligence
• Répondre à vos questions compliance

Quelle est votre question ?`
  }
  if (msg.includes("prix") || msg.includes("tarif") || msg.includes("combien") || msg.includes("coût caelum")) {
    return `**Tarifs Caelum — Plans disponibles**

| Plan | Prix | Entreprises |
|------|------|-------------|
| **Starter** | €200/mois | 100-500 employés |
| **Business** | €800/mois | 500-2000 employés |
| **Enterprise** | €2000+/mois | 2000+ employés |

Tous les plans incluent :
✓ Analyse continue de votre chaîne de valeur
✓ 180+ domaines de risque monitoriés
✓ Génération automatique rapports CSDDD
✓ Alertes en temps réel
✓ Support compliance dédié

**Contactez-nous** pour un devis personnalisé : retrouvetonsmile@gmail.com`
  }

  return `Merci pour votre question sur **"${userMessage}"**.

Je suis en train d'analyser cette problématique compliance. Pour une réponse précise et personnalisée, je vous recommande de :

1. **Consulter notre démo** pour voir l'analyse de votre situation spécifique → [Lancer la démo](/demo)
2. **Contacter notre équipe** pour un audit personnalisé : retrouvetonsmile@gmail.com

En attendant, voici les domaines CSDDD les plus fréquemment posés en question :
• Calcul de l'exposition financière aux sanctions
• Cartographie des fournisseurs niveau 2 et 3
• Rédaction du rapport de due diligence
• Mise en place du canal de signalement

Sur lequel souhaitez-vous que je me concentre ?`
}

const SUGGESTIONS = [
  "Qu'est-ce que la CSDDD exactement ?",
  "Quelles sont les amendes possibles ?",
  "Comment cartographier ma chaîne de valeur ?",
  "Que faire avec un fournisseur non conforme ?",
]

export default function AssistantPage() {
  const [messages, setMessages] = useState<Message[]>([
    {
      role: "assistant",
      content: `Bonjour ! Je suis **CaelumAI**, votre assistant de conformité CSDDD.

Je peux analyser vos risques droits humains, vous expliquer vos obligations légales et vous aider à préparer votre audit de due diligence.

**Comment puis-je vous aider aujourd'hui ?**`,
      timestamp: new Date(),
    }
  ])
  const [input, setInput] = useState("")
  const [isTyping, setIsTyping] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [messages])

  const sendMessage = async (text?: string) => {
    const msg = text || input.trim()
    if (!msg) return

    setInput("")
    setMessages(prev => [...prev, { role: "user", content: msg, timestamp: new Date() }])
    setIsTyping(true)

    await new Promise(r => setTimeout(r, 800 + Math.random() * 700))

    const response = getAIResponse(msg)
    setMessages(prev => [...prev, { role: "assistant", content: response, timestamp: new Date() }])
    setIsTyping(false)
  }

  const formatContent = (content: string) => {
    const escaped = content
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#x27;");
    return escaped
      .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
      .replace(/\n/g, "<br/>")
      .replace(/•/g, "•")
  }

  return (
    <div style={{ background: "#0f172a", minHeight: "100vh", display: "flex", flexDirection: "column", fontFamily: "system-ui, sans-serif" }}>
      {/* Header */}
      <div style={{ background: "#1e293b", borderBottom: "1px solid #334155", padding: "16px 24px", display: "flex", alignItems: "center", gap: 12 }}>
        <div style={{ background: ACCENT, borderRadius: 10, padding: 8 }}>
          <svg width={20} height={20} viewBox="0 0 24 24" fill="none" stroke="#fff" strokeWidth={2}>
            <path d="M12 2a10 10 0 1 0 10 10A10 10 0 0 0 12 2zm0 18a8 8 0 1 1 8-8 8 8 0 0 1-8 8z" />
            <path d="M12 6v6l4 2" />
          </svg>
        </div>
        <div>
          <h1 style={{ margin: 0, fontSize: 16, fontWeight: 700, color: "#f1f5f9" }}>CaelumAI — Assistant Compliance</h1>
          <div style={{ display: "flex", alignItems: "center", gap: 6 }}>
            <div style={{ width: 6, height: 6, background: "#22c55e", borderRadius: "50%" }} />
            <span style={{ color: "#64748b", fontSize: 12 }}>En ligne · Spécialiste CSDDD &amp; Droits Humains</span>
          </div>
        </div>
        <div style={{ marginLeft: "auto" }}>
          <Link href="/contact" style={{ background: ACCENT, color: "#fff", borderRadius: 8, padding: "8px 14px", fontSize: 12, fontWeight: 600, textDecoration: "none" }}>
            Lancer la démo →
          </Link>
        </div>
      </div>

      {/* Messages */}
      <div style={{ flex: 1, overflowY: "auto", padding: "24px", maxWidth: 760, width: "100%", margin: "0 auto", boxSizing: "border-box" }}>
        {messages.map((msg, i) => (
          <div key={i} style={{ marginBottom: 20, display: "flex", justifyContent: msg.role === "user" ? "flex-end" : "flex-start" }}>
            {msg.role === "assistant" && (
              <div style={{ width: 32, height: 32, background: ACCENT, borderRadius: "50%", display: "flex", alignItems: "center", justifyContent: "center", flexShrink: 0, marginRight: 10, marginTop: 4, fontSize: 14 }}>
                🤖
              </div>
            )}
            <div style={{
              maxWidth: "78%",
              background: msg.role === "user" ? ACCENT : "#1e293b",
              borderRadius: msg.role === "user" ? "16px 16px 4px 16px" : "16px 16px 16px 4px",
              padding: "12px 16px",
              border: msg.role === "assistant" ? "1px solid #334155" : "none",
            }}>
              <div style={{ color: "#f1f5f9", fontSize: 14, lineHeight: 1.6 }}
                dangerouslySetInnerHTML={{ __html: formatContent(msg.content) }} />
              <div style={{ color: msg.role === "user" ? "#a5b4fc" : "#475569", fontSize: 11, marginTop: 6 }}>
                {msg.timestamp.toLocaleTimeString("fr-FR", { hour: "2-digit", minute: "2-digit" })}
              </div>
            </div>
          </div>
        ))}
        {isTyping && (
          <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 20 }}>
            <div style={{ width: 32, height: 32, background: ACCENT, borderRadius: "50%", display: "flex", alignItems: "center", justifyContent: "center", fontSize: 14 }}>🤖</div>
            <div style={{ background: "#1e293b", borderRadius: "16px 16px 16px 4px", padding: "12px 16px", border: "1px solid #334155" }}>
              <div style={{ display: "flex", gap: 4, alignItems: "center" }}>
                {[0, 1, 2].map(j => (
                  <div key={j} style={{ width: 6, height: 6, background: "#6366f1", borderRadius: "50%", animation: `bounce 1.2s ease-in-out ${j * 0.2}s infinite` }} />
                ))}
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Suggestions */}
      {messages.length <= 1 && (
        <div style={{ padding: "0 24px 16px", maxWidth: 760, width: "100%", margin: "0 auto", boxSizing: "border-box" }}>
          <p style={{ color: "#475569", fontSize: 12, marginBottom: 8 }}>Questions fréquentes :</p>
          <div style={{ display: "flex", flexWrap: "wrap", gap: 8 }}>
            {SUGGESTIONS.map(s => (
              <button key={s} onClick={() => sendMessage(s)}
                style={{ background: "#1e293b", border: "1px solid #334155", borderRadius: 20, padding: "6px 14px", color: "#94a3b8", fontSize: 12, cursor: "pointer" }}>
                {s}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Input */}
      <div style={{ background: "#1e293b", borderTop: "1px solid #334155", padding: "16px 24px" }}>
        <div style={{ maxWidth: 760, margin: "0 auto", display: "flex", gap: 10 }}>
          <input
            value={input}
            onChange={e => setInput(e.target.value)}
            onKeyDown={e => e.key === "Enter" && !e.shiftKey && sendMessage()}
            placeholder="Posez votre question compliance CSDDD..."
            style={{ flex: 1, background: "#0f172a", border: "1px solid #334155", borderRadius: 10, padding: "12px 16px", color: "#f1f5f9", fontSize: 14, outline: "none" }}
          />
          <button onClick={() => sendMessage()}
            style={{ background: ACCENT, border: "none", borderRadius: 10, padding: "12px 18px", color: "#fff", fontSize: 14, fontWeight: 600, cursor: "pointer" }}>
            →
          </button>
        </div>
        <p style={{ textAlign: "center", color: "#334155", fontSize: 11, margin: "10px 0 0" }}>
          CaelumAI · Spécialiste CSDDD &amp; Droits Humains · Caelum Partners
        </p>
      </div>
      <style>{`@keyframes bounce { 0%, 60%, 100% { transform: translateY(0) } 30% { transform: translateY(-6px) } }`}</style>
    </div>
  )
}
