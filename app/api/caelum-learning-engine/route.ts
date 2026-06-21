import { NextResponse } from "next/server"
import { sealResponse } from "@/lib/digital-seal"

if (!process.env.SWARM_API_URL) {
  console.warn("[caelum-learning-engine] SWARM_API_URL not set — using mock data")
}

const MOCK = {
  domain: "caelum-learning-engine",
  generated_at: new Date().toISOString(),
  system: "CaelumSwarm Reinforcement Learning Loop — Caelum Partners SPRL",
  description: "Boucle d'amélioration continue par apprentissage par renforcement. Chaque cycle évalue les prédictions de tous les engines et ajuste automatiquement les poids sub1/sub2/sub3/sub4 pour maximiser la précision CSDDD.",
  last_cycle: {
    timestamp: new Date().toISOString(),
    engines_evaluated: 55,
    engines_skipped: 835,
    avg_reward: 0.8455,
    best_engine: "transitional_justice_truth_commission_engine",
    best_reward: 1.0,
    learning_rate: 0.05,
  },
  top_improved_engines: [
    { engine: "whistleblower_protection_corporate_accountability_engine", reward: 0.98, weight_delta: { sub1: +0.012, sub2: -0.008, sub3: +0.003, sub4: -0.007 } },
    { engine: "housing_forced_evictions_gentrification_engine", reward: 0.95, weight_delta: { sub1: +0.009, sub2: +0.005, sub3: -0.006, sub4: -0.008 } },
    { engine: "stateless_persons_nationality_rights_engine", reward: 0.94, weight_delta: { sub1: +0.015, sub2: -0.003, sub3: -0.005, sub4: -0.007 } },
    { engine: "biometric_border_surveillance_migration_engine", reward: 0.92, weight_delta: { sub1: +0.011, sub2: +0.002, sub3: -0.004, sub4: -0.009 } },
    { engine: "icc_universal_jurisdiction_impunity_engine", reward: 0.91, weight_delta: { sub1: +0.008, sub2: +0.007, sub3: -0.003, sub4: -0.012 } },
  ],
  weight_evolution: {
    description: "Évolution des poids moyens sur tous les engines optimisés",
    default_weights: { sub1: 0.30, sub2: 0.25, sub3: 0.25, sub4: 0.20 },
    current_avg_weights: { sub1: 0.312, sub2: 0.248, sub3: 0.247, sub4: 0.193 },
    cycles_completed: 1,
  },
  next_cycle_scheduled: "automatique — déclenché à chaque déploiement Wave",
  status: "active",
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return await sealResponse(NextResponse.json({ payload: MOCK }))
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/caelum-learning-engine`, {
      next: { revalidate: 30 },
    })
    const data = await res.json()
    return await sealResponse(NextResponse.json({ payload: data }))
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream unavailable" }, { status: 502 }))
  }
}

export async function POST() {
  if (!process.env.SWARM_API_URL) {
    return await sealResponse(
      NextResponse.json({
        payload: {
          message: "Cycle d'apprentissage déclenché (mode mock)",
          timestamp: new Date().toISOString(),
          engines_scheduled: 55,
          status: "triggered",
        },
      })
    )
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/caelum-learning-engine/trigger`, {
      method: "POST",
      next: { revalidate: 0 },
    })
    const data = await res.json()
    return await sealResponse(NextResponse.json({ payload: data }))
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream unavailable" }, { status: 502 }))
  }
}
