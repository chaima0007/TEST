"use client"

import { useEffect, useState } from "react"

interface WeightDelta {
  sub1: number
  sub2: number
  sub3: number
  sub4: number
}

interface TopEngine {
  engine: string
  reward: number
  weight_delta: WeightDelta
}

interface LearningData {
  domain: string
  generated_at: string
  system: string
  description: string
  last_cycle: {
    timestamp: string
    engines_evaluated: number
    engines_skipped: number
    avg_reward: number
    best_engine: string
    best_reward: number
    learning_rate: number
  }
  top_improved_engines: TopEngine[]
  weight_evolution: {
    description: string
    default_weights: WeightDelta
    current_avg_weights: WeightDelta
    cycles_completed: number
  }
  next_cycle_scheduled: string
  status: string
}

const ACCENT = "#22d3ee"

function RewardBar({ value, max = 1.0 }: { value: number; max?: number }) {
  const pct = Math.round((value / max) * 100)
  const color = value >= 0.9 ? "#22c55e" : value >= 0.7 ? "#eab308" : "#ef4444"
  return (
    <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
      <div style={{ flex: 1, height: 8, background: "#1e293b", borderRadius: 4, overflow: "hidden" }}>
        <div style={{ width: `${pct}%`, height: "100%", background: color, borderRadius: 4, transition: "width 0.6s ease" }} />
      </div>
      <span style={{ fontSize: 13, fontWeight: 700, color, minWidth: 42 }}>{(value * 100).toFixed(0)}%</span>
    </div>
  )
}

function WeightChip({ label, value, defaultVal }: { label: string; value: number; defaultVal: number }) {
  const delta = value - defaultVal
  const color = delta > 0.005 ? "#22c55e" : delta < -0.005 ? "#f97316" : "#94a3b8"
  return (
    <div style={{ background: "#1e293b", borderRadius: 8, padding: "8px 14px", textAlign: "center", minWidth: 70 }}>
      <div style={{ fontSize: 11, color: "#64748b", marginBottom: 4 }}>{label}</div>
      <div style={{ fontSize: 18, fontWeight: 700, color: ACCENT }}>{(value * 100).toFixed(1)}%</div>
      <div style={{ fontSize: 10, color, marginTop: 2 }}>
        {delta >= 0 ? "+" : ""}{(delta * 100).toFixed(1)}%
      </div>
    </div>
  )
}

export default function CaelumLearningEnginePage() {
  const [data, setData] = useState<LearningData | null>(null)
  const [triggering, setTriggering] = useState(false)
  const [triggerMsg, setTriggerMsg] = useState("")

  useEffect(() => {
    fetch("/api/caelum-learning-engine")
      .then((r) => r.json())
      .then((d) => setData(d.payload ?? d))
  }, [])

  const triggerCycle = async () => {
    setTriggering(true)
    setTriggerMsg("")
    try {
      const res = await fetch("/api/caelum-learning-engine", { method: "POST" })
      const d = await res.json()
      const payload = d.payload ?? d
      setTriggerMsg(payload.message ?? "Cycle déclenché")
    } catch {
      setTriggerMsg("Erreur lors du déclenchement")
    } finally {
      setTriggering(false)
    }
  }

  if (!data) {
    return (
      <div style={{ background: "#0f172a", minHeight: "100vh", display: "flex", alignItems: "center", justifyContent: "center" }}>
        <div style={{ color: ACCENT, fontSize: 18 }}>Chargement boucle d&apos;apprentissage…</div>
      </div>
    )
  }

  const { last_cycle, top_improved_engines, weight_evolution } = data

  return (
    <div style={{ background: "#0f172a", minHeight: "100vh", padding: "32px 24px", fontFamily: "system-ui, sans-serif" }}>
      {/* Header */}
      <div style={{ maxWidth: 1100, margin: "0 auto 32px" }}>
        <div style={{ display: "flex", alignItems: "center", gap: 16, marginBottom: 8 }}>
          <div style={{ background: ACCENT, borderRadius: 12, padding: 12, flexShrink: 0 }}>
            <svg width={28} height={28} viewBox="0 0 24 24" fill="none" stroke="#0f172a" strokeWidth={2.5}>
              <path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83" />
            </svg>
          </div>
          <div>
            <h1 style={{ margin: 0, fontSize: 24, fontWeight: 800, color: "#f1f5f9" }}>
              CaelumSwarm — Boucle d&apos;Apprentissage par Renforcement
            </h1>
            <p style={{ margin: 0, color: "#94a3b8", fontSize: 14 }}>
              Amélioration continue automatique · Exclusivité Caelum Partners SPRL — Chaima Mhadbi
            </p>
          </div>
        </div>
        <p style={{ color: "#475569", fontSize: 13, margin: 0, lineHeight: 1.6 }}>{data.description}</p>
      </div>

      {/* Last cycle stats */}
      <div style={{ maxWidth: 1100, margin: "0 auto 28px" }}>
        <h2 style={{ color: "#94a3b8", fontSize: 13, fontWeight: 700, textTransform: "uppercase", letterSpacing: 1, marginBottom: 14 }}>
          Dernier Cycle — {new Date(last_cycle.timestamp).toLocaleString("fr-FR")}
        </h2>
        <div style={{ display: "flex", gap: 16, flexWrap: "wrap" }}>
          {[
            { label: "Engines évalués", value: last_cycle.engines_evaluated, color: ACCENT },
            { label: "Récompense moy.", value: `${(last_cycle.avg_reward * 100).toFixed(1)}%`, color: "#22c55e" },
            { label: "Meilleure récomp.", value: `${(last_cycle.best_reward * 100).toFixed(0)}%`, color: "#a855f7" },
            { label: "Taux apprentissage", value: last_cycle.learning_rate, color: "#f59e0b" },
            { label: "Cycles complétés", value: weight_evolution.cycles_completed, color: "#06b6d4" },
          ].map((s) => (
            <div key={s.label} style={{ background: "#1e293b", borderRadius: 10, padding: "14px 22px", minWidth: 120, borderTop: `3px solid ${s.color}` }}>
              <div style={{ fontSize: 22, fontWeight: 700, color: s.color }}>{s.value}</div>
              <div style={{ fontSize: 12, color: "#94a3b8", marginTop: 2 }}>{s.label}</div>
            </div>
          ))}
        </div>
      </div>

      {/* Weight evolution */}
      <div style={{ maxWidth: 1100, margin: "0 auto 28px", background: "#1e293b", borderRadius: 14, padding: 24, borderLeft: `4px solid ${ACCENT}` }}>
        <h2 style={{ color: "#f1f5f9", fontSize: 16, fontWeight: 700, margin: "0 0 16px" }}>
          Évolution des Poids — Formule ComplianceIQ™
        </h2>
        <p style={{ color: "#64748b", fontSize: 12, margin: "0 0 20px" }}>{weight_evolution.description}</p>
        <div style={{ display: "flex", gap: 12, flexWrap: "wrap" }}>
          {(["sub1", "sub2", "sub3", "sub4"] as const).map((k) => (
            <WeightChip
              key={k}
              label={k.replace("sub", "Sous-score ")}
              value={weight_evolution.current_avg_weights[k]}
              defaultVal={weight_evolution.default_weights[k]}
            />
          ))}
        </div>
        <p style={{ color: "#334155", fontSize: 11, margin: "16px 0 0" }}>
          Vert = poids augmenté · Orange = poids réduit · Gris = stable. Poids de référence : 30%/25%/25%/20%
        </p>
      </div>

      {/* Top engines */}
      <div style={{ maxWidth: 1100, margin: "0 auto 28px" }}>
        <h2 style={{ color: "#94a3b8", fontSize: 13, fontWeight: 700, textTransform: "uppercase", letterSpacing: 1, marginBottom: 14 }}>
          Top 5 Engines les Plus Améliorés
        </h2>
        <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
          {top_improved_engines.map((eng, i) => (
            <div key={eng.engine} style={{ background: "#1e293b", borderRadius: 12, padding: "18px 22px", borderLeft: `4px solid ${ACCENT}` }}>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 12 }}>
                <div>
                  <span style={{ color: ACCENT, fontSize: 11, fontWeight: 700 }}>#{i + 1}</span>
                  <span style={{ color: "#f1f5f9", fontSize: 13, fontWeight: 600, marginLeft: 10 }}>
                    {eng.engine.replace(/_/g, " ")}
                  </span>
                </div>
              </div>
              <RewardBar value={eng.reward} />
              <div style={{ display: "flex", gap: 12, marginTop: 12, flexWrap: "wrap" }}>
                {(["sub1", "sub2", "sub3", "sub4"] as const).map((k) => {
                  const delta = eng.weight_delta[k]
                  const color = delta > 0 ? "#22c55e" : delta < 0 ? "#f97316" : "#64748b"
                  return (
                    <span key={k} style={{ fontSize: 11, color, background: "#0f172a", padding: "2px 8px", borderRadius: 4 }}>
                      {k}: {delta >= 0 ? "+" : ""}{(delta * 100).toFixed(1)}%
                    </span>
                  )
                })}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Trigger button */}
      <div style={{ maxWidth: 1100, margin: "0 auto", textAlign: "center" }}>
        <button
          onClick={triggerCycle}
          disabled={triggering}
          style={{
            background: triggering ? "#334155" : ACCENT,
            color: triggering ? "#64748b" : "#0f172a",
            border: "none",
            borderRadius: 10,
            padding: "14px 36px",
            fontSize: 15,
            fontWeight: 700,
            cursor: triggering ? "not-allowed" : "pointer",
            transition: "all 0.2s",
          }}
        >
          {triggering ? "Cycle en cours…" : "Déclencher un Cycle d'Apprentissage"}
        </button>
        {triggerMsg && (
          <p style={{ color: "#22c55e", marginTop: 12, fontSize: 13 }}>{triggerMsg}</p>
        )}
        <p style={{ color: "#334155", fontSize: 11, marginTop: 16 }}>
          Prochain cycle automatique : {data.next_cycle_scheduled}
        </p>
        <p style={{ color: "#334155", fontSize: 11 }}>
          Dernière mise à jour : {new Date(data.generated_at).toLocaleString("fr-FR")} · Caelum Partners
        </p>
      </div>
    </div>
  )
}
