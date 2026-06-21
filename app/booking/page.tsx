"use client"

import { useState } from "react"
import Link from "next/link"

const ACCENT = "#6366f1"

const SPECIALISTS = [
  {
    name: "Sarah Delacroix",
    title: "Senior Compliance Advisor",
    expertise: "CSDDD & Due Diligence",
    avatar: "SD",
    color: "#6366f1",
    available: true,
    slots_today: 3,
    languages: ["FR", "EN", "NL"],
  },
  {
    name: "Marcus Thielen",
    title: "Head of Supply Chain Risk",
    expertise: "Chaîne d'approvisionnement & Fournisseurs",
    avatar: "MT",
    color: "#0891b2",
    available: true,
    slots_today: 2,
    languages: ["EN", "DE", "FR"],
  },
  {
    name: "Amira Benali",
    title: "Human Rights Analyst",
    expertise: "Droits humains & Reporting ESG",
    avatar: "AB",
    color: "#8b5cf6",
    available: false,
    slots_today: 0,
    languages: ["FR", "EN", "AR"],
  },
  {
    name: "James Whitfield",
    title: "Enterprise Solutions Director",
    expertise: "Grands comptes & Intégration SAP",
    avatar: "JW",
    color: "#dc2626",
    available: true,
    slots_today: 1,
    languages: ["EN", "FR"],
  },
]

const TIME_SLOTS = [
  "09:00", "09:30", "10:00", "10:30", "11:00", "11:30",
  "14:00", "14:30", "15:00", "15:30", "16:00", "16:30", "17:00",
]

const SLOT_STATUS: Record<string, "available" | "taken" | "almost"> = {
  "09:00": "taken",
  "09:30": "taken",
  "10:00": "available",
  "10:30": "almost",
  "11:00": "available",
  "11:30": "taken",
  "14:00": "almost",
  "14:30": "available",
  "15:00": "taken",
  "15:30": "available",
  "16:00": "taken",
  "16:30": "available",
  "17:00": "almost",
}

function getDayLabel(offset: number) {
  const d = new Date()
  d.setDate(d.getDate() + offset)
  const days = ["Dim", "Lun", "Mar", "Mer", "Jeu", "Ven", "Sam"]
  const months = ["jan", "fév", "mar", "avr", "mai", "juin", "juil", "août", "sep", "oct", "nov", "déc"]
  return { day: days[d.getDay()], date: d.getDate(), month: months[d.getMonth()], full: d.toLocaleDateString("fr-FR") }
}

export default function BookingPage() {
  const [selectedSpecialist, setSelectedSpecialist] = useState(0)
  const [selectedDay, setSelectedDay] = useState(1)
  const [selectedSlot, setSelectedSlot] = useState<string | null>(null)
  const [name, setName] = useState("")
  const [email, setEmail] = useState("")
  const [company, setCompany] = useState("")
  const [topic, setTopic] = useState("Présentation générale CaelumSwarm")
  const [step, setStep] = useState<"pick" | "confirm" | "done">("pick")

  const days = [1, 2, 3, 4, 5].map(getDayLabel)
  const specialist = SPECIALISTS[selectedSpecialist]

  const handleConfirm = () => {
    if (!name || !email) return
    setStep("done")
  }

  if (step === "done") {
    const dayLabel = days[selectedDay - 1]
    return (
      <div style={{ background: "#0f172a", minHeight: "100vh", display: "flex", alignItems: "center", justifyContent: "center", padding: "40px 24px", fontFamily: "system-ui, sans-serif" }}>
        <div style={{ maxWidth: 520, width: "100%", textAlign: "center" }}>
          <div style={{ width: 72, height: 72, background: "#22c55e20", border: "2px solid #22c55e", borderRadius: "50%", display: "flex", alignItems: "center", justifyContent: "center", margin: "0 auto 24px", fontSize: 32 }}>
            ✓
          </div>
          <h1 style={{ margin: "0 0 12px", fontSize: 26, fontWeight: 800, color: "#f1f5f9" }}>Rendez-vous confirmé !</h1>
          <p style={{ margin: "0 0 24px", color: "#94a3b8", fontSize: 15, lineHeight: 1.6 }}>
            Votre réunion avec <strong style={{ color: "#f1f5f9" }}>{specialist.name}</strong> est planifiée pour le <strong style={{ color: "#6366f1" }}>{dayLabel.day} {dayLabel.date} à {selectedSlot}</strong>.
          </p>
          <div style={{ background: "#1e293b", borderRadius: 12, padding: 20, marginBottom: 24, border: "1px solid #334155", textAlign: "left" }}>
            <div style={{ display: "flex", gap: 12, marginBottom: 12 }}>
              <div style={{ width: 40, height: 40, background: specialist.color, borderRadius: "50%", display: "flex", alignItems: "center", justifyContent: "center", color: "#fff", fontWeight: 700, fontSize: 14 }}>
                {specialist.avatar}
              </div>
              <div>
                <div style={{ color: "#f1f5f9", fontWeight: 600, fontSize: 14 }}>{specialist.name}</div>
                <div style={{ color: "#64748b", fontSize: 12 }}>{specialist.title} · Caelum Partners</div>
              </div>
            </div>
            <div style={{ borderTop: "1px solid #334155", paddingTop: 12 }}>
              <div style={{ color: "#94a3b8", fontSize: 13 }}>📅 {dayLabel.day} {dayLabel.date} {dayLabel.month} · {selectedSlot}</div>
              <div style={{ color: "#94a3b8", fontSize: 13, marginTop: 4 }}>📋 {topic}</div>
              <div style={{ color: "#94a3b8", fontSize: 13, marginTop: 4 }}>🎥 Lien Google Meet envoyé à {email}</div>
            </div>
          </div>
          <p style={{ color: "#475569", fontSize: 13, marginBottom: 20 }}>
            Une invitation calendar et le lien de visioconférence ont été envoyés à votre adresse email. Notre équipe vous contactera 30 minutes avant la réunion.
          </p>
          <div style={{ display: "flex", gap: 12, justifyContent: "center" }}>
            <Link href="/demo" style={{ background: ACCENT, color: "#fff", borderRadius: 10, padding: "10px 20px", fontSize: 14, fontWeight: 600, textDecoration: "none" }}>
              Voir la démo →
            </Link>
            <Link href="/" style={{ background: "#1e293b", color: "#94a3b8", border: "1px solid #334155", borderRadius: 10, padding: "10px 20px", fontSize: 14, fontWeight: 600, textDecoration: "none" }}>
              Retour accueil
            </Link>
          </div>
        </div>
      </div>
    )
  }

  if (step === "confirm") return (
    <div style={{ background: "#0f172a", minHeight: "100vh", padding: "40px 24px", fontFamily: "system-ui, sans-serif" }}>
      <div style={{ maxWidth: 560, margin: "0 auto" }}>
        <button onClick={() => setStep("pick")} style={{ background: "none", border: "none", color: "#64748b", cursor: "pointer", fontSize: 14, marginBottom: 24, padding: 0 }}>
          ← Retour
        </button>
        <h1 style={{ margin: "0 0 8px", fontSize: 24, fontWeight: 800, color: "#f1f5f9" }}>Confirmer le rendez-vous</h1>
        <p style={{ margin: "0 0 28px", color: "#64748b", fontSize: 14 }}>
          {specialist.name} · {days[selectedDay - 1]?.day} {days[selectedDay - 1]?.date} · {selectedSlot}
        </p>
        <div style={{ background: "#1e293b", borderRadius: 16, padding: 28, border: "1px solid #334155" }}>
          <div style={{ marginBottom: 18 }}>
            <label style={{ display: "block", color: "#94a3b8", fontSize: 12, fontWeight: 600, marginBottom: 8, textTransform: "uppercase", letterSpacing: 0.5 }}>Votre nom *</label>
            <input value={name} onChange={e => setName(e.target.value)} placeholder="Prénom Nom"
              style={{ width: "100%", background: "#0f172a", border: "1px solid #334155", borderRadius: 8, padding: "11px 14px", color: "#f1f5f9", fontSize: 14, outline: "none", boxSizing: "border-box" }} />
          </div>
          <div style={{ marginBottom: 18 }}>
            <label style={{ display: "block", color: "#94a3b8", fontSize: 12, fontWeight: 600, marginBottom: 8, textTransform: "uppercase", letterSpacing: 0.5 }}>Email professionnel *</label>
            <input value={email} onChange={e => setEmail(e.target.value)} placeholder="vous@entreprise.com" type="email"
              style={{ width: "100%", background: "#0f172a", border: "1px solid #334155", borderRadius: 8, padding: "11px 14px", color: "#f1f5f9", fontSize: 14, outline: "none", boxSizing: "border-box" }} />
          </div>
          <div style={{ marginBottom: 18 }}>
            <label style={{ display: "block", color: "#94a3b8", fontSize: 12, fontWeight: 600, marginBottom: 8, textTransform: "uppercase", letterSpacing: 0.5 }}>Entreprise</label>
            <input value={company} onChange={e => setCompany(e.target.value)} placeholder="Nom de votre entreprise"
              style={{ width: "100%", background: "#0f172a", border: "1px solid #334155", borderRadius: 8, padding: "11px 14px", color: "#f1f5f9", fontSize: 14, outline: "none", boxSizing: "border-box" }} />
          </div>
          <div style={{ marginBottom: 24 }}>
            <label style={{ display: "block", color: "#94a3b8", fontSize: 12, fontWeight: 600, marginBottom: 8, textTransform: "uppercase", letterSpacing: 0.5 }}>Sujet de la réunion</label>
            <select value={topic} onChange={e => setTopic(e.target.value)}
              style={{ width: "100%", background: "#0f172a", border: "1px solid #334155", borderRadius: 8, padding: "11px 14px", color: "#f1f5f9", fontSize: 14, outline: "none", boxSizing: "border-box" }}>
              <option>Présentation générale CaelumSwarm</option>
              <option>Audit conformité CSDDD</option>
              <option>Cartographie fournisseurs</option>
              <option>Intégration & déploiement</option>
              <option>Tarifs & contrat entreprise</option>
              <option>Question technique</option>
            </select>
          </div>
          <a href={`mailto:retrouvetonsmile@gmail.com?subject=RDV CaelumSwarm — ${name} (${company}) — ${days[selectedDay-1]?.full} ${selectedSlot}&body=Bonjour,%0A%0AJe confirme mon rendez-vous avec ${specialist.name} le ${days[selectedDay-1]?.full} à ${selectedSlot}.%0A%0ANom: ${name}%0AEmail: ${email}%0AEntreprise: ${company}%0ASujet: ${topic}%0A%0ACordialement,%0A${name}`}
            onClick={handleConfirm}
            style={{ display: "block", width: "100%", background: ACCENT, color: "#fff", borderRadius: 10, padding: "13px", fontSize: 15, fontWeight: 700, textDecoration: "none", textAlign: "center", boxSizing: "border-box" }}>
            Confirmer le rendez-vous →
          </a>
        </div>
      </div>
    </div>
  )

  return (
    <div style={{ background: "#0f172a", minHeight: "100vh", padding: "32px 24px", fontFamily: "system-ui, sans-serif" }}>
      <div style={{ maxWidth: 900, margin: "0 auto" }}>
        {/* Header */}
        <div style={{ marginBottom: 36, textAlign: "center" }}>
          <div style={{ display: "inline-flex", alignItems: "center", gap: 8, background: "#22c55e20", border: "1px solid #22c55e40", borderRadius: 20, padding: "4px 14px", marginBottom: 16 }}>
            <div style={{ width: 7, height: 7, background: "#22c55e", borderRadius: "50%" }} />
            <span style={{ color: "#22c55e", fontSize: 12, fontWeight: 600 }}>Équipe disponible · Réponse sous 2h</span>
          </div>
          <h1 style={{ margin: "0 0 12px", fontSize: 30, fontWeight: 800, color: "#f1f5f9" }}>
            Réservez votre session<br /><span style={{ color: ACCENT }}>avec un expert CaelumSwarm</span>
          </h1>
          <p style={{ margin: 0, color: "#64748b", fontSize: 15, lineHeight: 1.6 }}>
            30 minutes gratuites avec un spécialiste compliance CSDDD · Disponible 24h/24 · Sans engagement
          </p>
        </div>

        {/* Stats bar */}
        <div style={{ display: "flex", gap: 0, marginBottom: 36, background: "#1e293b", borderRadius: 12, overflow: "hidden", border: "1px solid #334155" }}>
          {[
            { label: "Experts disponibles", value: "4", color: "#22c55e" },
            { label: "Créneaux cette semaine", value: "23", color: "#6366f1" },
            { label: "Délai moyen réponse", value: "< 2h", color: "#f59e0b" },
            { label: "Sessions réalisées", value: "140+", color: "#0891b2" },
          ].map((s, i) => (
            <div key={i} style={{ flex: 1, padding: "16px 20px", borderRight: i < 3 ? "1px solid #334155" : "none", textAlign: "center" }}>
              <div style={{ fontSize: 22, fontWeight: 700, color: s.color }}>{s.value}</div>
              <div style={{ fontSize: 11, color: "#64748b", marginTop: 2 }}>{s.label}</div>
            </div>
          ))}
        </div>

        <div style={{ display: "grid", gridTemplateColumns: "300px 1fr", gap: 24 }}>
          {/* Specialists */}
          <div>
            <h2 style={{ margin: "0 0 16px", fontSize: 14, fontWeight: 700, color: "#64748b", textTransform: "uppercase", letterSpacing: 0.5 }}>Choisir un expert</h2>
            <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
              {SPECIALISTS.map((s, i) => (
                <button key={i} onClick={() => s.available && setSelectedSpecialist(i)}
                  style={{ background: selectedSpecialist === i ? `${s.color}20` : "#1e293b", border: `1px solid ${selectedSpecialist === i ? s.color : "#334155"}`, borderRadius: 12, padding: "14px 16px", cursor: s.available ? "pointer" : "not-allowed", textAlign: "left", opacity: s.available ? 1 : 0.5 }}>
                  <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
                    <div style={{ width: 36, height: 36, background: s.color, borderRadius: "50%", display: "flex", alignItems: "center", justifyContent: "center", color: "#fff", fontWeight: 700, fontSize: 13, flexShrink: 0 }}>
                      {s.avatar}
                    </div>
                    <div style={{ minWidth: 0 }}>
                      <div style={{ color: "#f1f5f9", fontWeight: 600, fontSize: 13 }}>{s.name}</div>
                      <div style={{ color: "#64748b", fontSize: 11 }}>{s.expertise}</div>
                    </div>
                  </div>
                  <div style={{ display: "flex", justifyContent: "space-between", marginTop: 8, paddingTop: 8, borderTop: "1px solid #334155" }}>
                    <div style={{ display: "flex", gap: 4 }}>
                      {s.languages.map(l => (
                        <span key={l} style={{ background: "#334155", borderRadius: 4, padding: "1px 6px", fontSize: 10, color: "#94a3b8", fontWeight: 600 }}>{l}</span>
                      ))}
                    </div>
                    {s.available ? (
                      <span style={{ color: "#22c55e", fontSize: 11, fontWeight: 600 }}>● {s.slots_today} créneaux</span>
                    ) : (
                      <span style={{ color: "#64748b", fontSize: 11 }}>Complet</span>
                    )}
                  </div>
                </button>
              ))}
            </div>
          </div>

          {/* Calendar */}
          <div>
            <h2 style={{ margin: "0 0 16px", fontSize: 14, fontWeight: 700, color: "#64748b", textTransform: "uppercase", letterSpacing: 0.5 }}>Choisir un créneau</h2>
            {/* Day picker */}
            <div style={{ display: "flex", gap: 8, marginBottom: 20 }}>
              {days.map((d, i) => (
                <button key={i} onClick={() => setSelectedDay(i + 1)}
                  style={{ flex: 1, background: selectedDay === i + 1 ? ACCENT : "#1e293b", border: `1px solid ${selectedDay === i + 1 ? ACCENT : "#334155"}`, borderRadius: 10, padding: "10px 6px", cursor: "pointer", textAlign: "center" }}>
                  <div style={{ color: selectedDay === i + 1 ? "#fff" : "#64748b", fontSize: 11, fontWeight: 600, textTransform: "uppercase" }}>{d.day}</div>
                  <div style={{ color: selectedDay === i + 1 ? "#fff" : "#f1f5f9", fontSize: 18, fontWeight: 700, margin: "2px 0" }}>{d.date}</div>
                  <div style={{ color: selectedDay === i + 1 ? "#c7d2fe" : "#475569", fontSize: 10 }}>{d.month}</div>
                </button>
              ))}
            </div>
            {/* Time slots */}
            <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: 8 }}>
              {TIME_SLOTS.map(slot => {
                const status = selectedDay === 1 ? SLOT_STATUS[slot] : (Math.random() > 0.4 ? "available" : Math.random() > 0.5 ? "taken" : "almost")
                const isSelected = selectedSlot === slot
                const isTaken = status === "taken"
                return (
                  <button key={slot} onClick={() => !isTaken && setSelectedSlot(slot)} disabled={isTaken}
                    style={{
                      background: isSelected ? ACCENT : isTaken ? "#0f172a" : status === "almost" ? "#f59e0b10" : "#1e293b",
                      border: `1px solid ${isSelected ? ACCENT : isTaken ? "#1e293b" : status === "almost" ? "#f59e0b40" : "#334155"}`,
                      borderRadius: 8, padding: "10px 8px", cursor: isTaken ? "not-allowed" : "pointer",
                      color: isSelected ? "#fff" : isTaken ? "#334155" : status === "almost" ? "#f59e0b" : "#94a3b8",
                      fontSize: 13, fontWeight: 600, textDecoration: isTaken ? "line-through" : "none",
                    }}>
                    {slot}
                    {status === "almost" && !isTaken && !isSelected && (
                      <div style={{ fontSize: 9, color: "#f59e0b", marginTop: 2 }}>1 place</div>
                    )}
                  </button>
                )
              })}
            </div>

            {selectedSlot && (
              <div style={{ marginTop: 20, background: "#6366f110", border: "1px solid #6366f130", borderRadius: 12, padding: 16, display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                <div>
                  <div style={{ color: "#f1f5f9", fontWeight: 700, fontSize: 15 }}>
                    {days[selectedDay - 1]?.day} {days[selectedDay - 1]?.date} à {selectedSlot}
                  </div>
                  <div style={{ color: "#64748b", fontSize: 12 }}>avec {specialist.name} · 30 min · Visioconférence</div>
                </div>
                <button onClick={() => setStep("confirm")}
                  style={{ background: ACCENT, color: "#fff", border: "none", borderRadius: 10, padding: "10px 20px", fontSize: 14, fontWeight: 700, cursor: "pointer" }}>
                  Continuer →
                </button>
              </div>
            )}
          </div>
        </div>

        <div style={{ marginTop: 32, textAlign: "center" }}>
          <Link href="/" style={{ color: "#475569", fontSize: 13, textDecoration: "none" }}>← Retour à l&apos;accueil</Link>
        </div>
      </div>
    </div>
  )
}
